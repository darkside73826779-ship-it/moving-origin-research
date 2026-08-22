"""Bounded, ledger-grounded soft-prefix experience strip.

This module deliberately knows nothing about a model or tensor library.  A
caller injects an encoder and an opaque codec; the strip owns only committed
event binding, bounded placement, deterministic selection, and byte identities.
The bytes are a projection of the append-only ledger and never evidence by
themselves.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, replace
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
import tempfile
from threading import RLock
from typing import Any, Callable, Iterable, Mapping, Protocol

from .contracts import (
    CommittedOriginEvent,
    MemoryQuery,
    OriginStamp,
    SHA256_ZERO,
    SituatedOriginFrame,
    canonical_bytes,
    require_sha256,
    sha256_bytes,
    sha256_canonical,
    to_primitive,
)
from .experience import (
    ExperienceAdvanceReceipt,
    ExperienceConsolidationReceipt,
    ExperienceLogComparison,
    ExperiencePortError,
    ExperienceRecord,
    ExperienceRetrieval,
    ExperienceWrite,
)


_SCHEMA_VERSION = "situated-origin-soft-prefix-strip-v1"
_RECEIPT_VERSION = "situated-origin-soft-prefix-receipt-v1"


class OpaqueTraceCodec(Protocol):
    """Injected byte boundary for a caller-owned numeric or tensor value."""

    identity_sha256: str

    def to_bytes(self, value: object) -> bytes: ...

    def from_bytes(self, data: bytes) -> object: ...


@dataclass(frozen=True)
class OpaqueTraceUpdate:
    """An opaque update plus numeric budget metadata used in its receipt."""

    value: object
    update_norm: int | float | Decimal
    update_budget: int | float | Decimal


@dataclass(frozen=True)
class SoftPrefixTraceRecord(ExperienceRecord):
    """One active trace with exact source-event and encoded-byte identities."""

    event_id: str
    prior_event_sha256: str
    event_sha256: str
    source_event_bytes: bytes
    source_event_sha256: str
    trace_bytes: bytes
    trace_sha256: str
    codec_identity_sha256: str
    actuator_identity_sha256: str
    sequence: int
    slot: int
    importance: Decimal
    prediction_error: Decimal
    update_norm: Decimal
    update_budget: Decimal
    supersedes_event_id: str | None
    superseded_by_event_id: str | None
    write_receipt_sha256: str


@dataclass(frozen=True)
class SoftPrefixTraceRank:
    record: SoftPrefixTraceRecord
    origin_distance: int
    effective_importance: Decimal


@dataclass(frozen=True)
class SoftPrefixRetrieval(ExperienceRetrieval):
    rankings: tuple[SoftPrefixTraceRank, ...]
    selected_event_ids: tuple[str, ...]
    requested_event_ids: tuple[str, ...]
    source_log_head: str

    def __post_init__(self) -> None:
        require_sha256(self.receipt_sha256, "E3_RETRIEVAL_RECEIPT_INVALID")
        require_sha256(self.source_log_head, "E3_RETRIEVAL_SOURCE_HEAD_INVALID")
        if self.source_log_head != self.query_origin.stamp.log_head:
            raise ExperiencePortError("E3_VIEW_HEAD_STALE")
        if (
            tuple(item.record.event_id for item in self.rankings)
            != self.selected_event_ids
        ):
            raise ExperiencePortError("E3_RETRIEVAL_SELECTION_MISMATCH")
        if tuple(item.record for item in self.rankings) != self.records:
            raise ExperiencePortError("E3_RETRIEVAL_RECORD_MISMATCH")


@dataclass(frozen=True)
class SoftPrefixAdvanceReceipt(ExperienceAdvanceReceipt):
    prior_strip_head: str
    resulting_strip_head: str
    source_log_head: str


@dataclass(frozen=True)
class SoftPrefixConsolidationReceipt(ExperienceConsolidationReceipt):
    consolidated_event_ids: tuple[str, ...]
    source_event_sha256s: tuple[str, ...]
    prior_strip_head: str
    resulting_strip_head: str
    source_log_head: str


@dataclass(frozen=True)
class SoftPrefixCheckpointReceipt:
    strip_head: str
    source_log_head: str
    checkpoint_sha256: str
    byte_count: int
    receipt_sha256: str


class SoftPrefixExperienceStrip:
    """A bounded tape of opaque traces implementing :class:`ExperiencePort`.

    ``trace_encoder`` may return a Python numeric value, an array owned by a
    model backend, or any other object understood by ``codec``.  The object is
    never inspected, compared, copied, or persisted here.  Only the codec's
    exact bytes cross into strip state.
    """

    def __init__(
        self,
        life_id: str,
        *,
        capacity: int,
        trace_encoder: Callable[[ExperienceWrite], OpaqueTraceUpdate],
        codec: OpaqueTraceCodec,
        actuator_identity_sha256: str,
        epoch: int = 0,
        decay_factor: int | float | Decimal = Decimal("0.9"),
        max_trace_bytes: int = 1_048_576,
    ) -> None:
        if not life_id:
            raise ExperiencePortError("E3_LIFE_ID_REQUIRED")
        if type(epoch) is not int or epoch < 0:
            raise ExperiencePortError("E3_ORIGIN_EPOCH_INVALID")
        if type(capacity) is not int or capacity < 1:
            raise ExperiencePortError("E3_CAPACITY_INVALID")
        if type(max_trace_bytes) is not int or max_trace_bytes < 1:
            raise ExperiencePortError("E3_TRACE_BYTE_LIMIT_INVALID")
        if not callable(trace_encoder):
            raise ExperiencePortError("E3_TRACE_ENCODER_REQUIRED")
        if not callable(getattr(codec, "to_bytes", None)) or not callable(
            getattr(codec, "from_bytes", None)
        ):
            raise ExperiencePortError("E3_TRACE_CODEC_REQUIRED")
        codec_identity = getattr(codec, "identity_sha256", None)
        try:
            require_sha256(codec_identity, "E3_CODEC_IDENTITY_INVALID")
            require_sha256(
                actuator_identity_sha256, "E3_ACTUATOR_IDENTITY_INVALID"
            )
        except ValueError as exc:
            raise ExperiencePortError(str(exc)) from exc
        decay = _decimal(decay_factor, "E3_DECAY_FACTOR_INVALID")
        if decay < 0 or decay > 1:
            raise ExperiencePortError("E3_DECAY_FACTOR_INVALID")

        self._life_id = life_id
        self._epoch = epoch
        self._capacity = capacity
        self._max_trace_bytes = max_trace_bytes
        self._decay_factor = decay
        self._trace_encoder = trace_encoder
        self._codec = codec
        self._codec_identity_sha256 = codec_identity
        self._actuator_identity_sha256 = actuator_identity_sha256
        self._origin = OriginStamp(life_id, epoch, -1, -1, SHA256_ZERO)
        self._head = SHA256_ZERO
        self._records: dict[str, SoftPrefixTraceRecord] = {}
        self._event_index: dict[str, str] = {}
        self._next_sequence = 0
        self._next_slot = 0
        self._current_transition_prior_head: str | None = None
        self._current_event_id: str | None = None
        self._written_current_event_id: str | None = None
        self._last_advance_receipt: SoftPrefixAdvanceReceipt | None = None
        self._lock = RLock()

    @property
    def life_id(self) -> str:
        return self._life_id

    @property
    def epoch(self) -> int:
        return self._epoch

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def origin(self) -> OriginStamp:
        with self._lock:
            return self._origin

    @property
    def head(self) -> str:
        with self._lock:
            return self._head

    @property
    def source_log_head(self) -> str:
        with self._lock:
            return self._origin.log_head

    @property
    def last_advance_receipt(self) -> SoftPrefixAdvanceReceipt | None:
        with self._lock:
            return self._last_advance_receipt

    def advance_origin(
        self, prior: OriginStamp, current: OriginStamp
    ) -> SoftPrefixAdvanceReceipt:
        with self._lock:
            return self._advance_unlocked(prior, current)

    def write_experience(self, request: ExperienceWrite) -> SoftPrefixTraceRecord:
        event, source_event_bytes = _validate_bound_request(request)
        importance = _decimal(request.importance, "E3_IMPORTANCE_INVALID")
        prediction_error = _decimal(
            request.prediction_error, "E3_PREDICTION_ERROR_INVALID"
        )
        if importance < 0:
            raise ExperiencePortError("E3_IMPORTANCE_INVALID")
        if prediction_error < 0:
            raise ExperiencePortError("E3_PREDICTION_ERROR_INVALID")

        with self._lock:
            auto_advance = self._prepare_event_position(event)
            if self._written_current_event_id == event.event_id:
                raise ExperiencePortError("E3_EVENT_ALREADY_WRITTEN")
            if event.event_id in self._event_index:
                raise ExperiencePortError("E3_EVENT_ALREADY_WRITTEN")

            target: SoftPrefixTraceRecord | None = None
            if request.supersedes_event_id is not None:
                target = self._record_for_event(request.supersedes_event_id)
                if target.superseded_by_event_id is not None:
                    raise ExperiencePortError("E3_SUPERSESSION_TARGET_STALE")
                if target.event_id == event.event_id:
                    raise ExperiencePortError("E3_SUPERSESSION_CYCLE")

            # All injected work completes before an automatic origin advance or
            # any trace mutation, so encoder/codec failure cannot partly append.
            try:
                update = self._trace_encoder(request)
            except Exception as exc:
                raise ExperiencePortError("E3_TRACE_ENCODING_FAILED") from exc
            if not isinstance(update, OpaqueTraceUpdate):
                raise ExperiencePortError("E3_TRACE_UPDATE_REQUIRED")
            update_norm = _decimal(update.update_norm, "E3_UPDATE_NORM_INVALID")
            update_budget = _decimal(
                update.update_budget, "E3_UPDATE_BUDGET_INVALID"
            )
            if update_norm < 0:
                raise ExperiencePortError("E3_UPDATE_NORM_INVALID")
            if update_budget < 0 or update_norm > update_budget:
                raise ExperiencePortError("E3_UPDATE_BUDGET_EXCEEDED")
            try:
                trace_bytes = self._codec.to_bytes(update.value)
            except Exception as exc:
                raise ExperiencePortError("E3_TRACE_SERIALIZATION_FAILED") from exc
            if type(trace_bytes) is not bytes:
                raise ExperiencePortError("E3_TRACE_BYTES_REQUIRED")
            if len(trace_bytes) > self._max_trace_bytes:
                raise ExperiencePortError("E3_TRACE_BYTE_LIMIT_EXCEEDED")

            source_event_sha256 = sha256_bytes(source_event_bytes)
            trace_sha256 = sha256_bytes(trace_bytes)
            experience_id = _experience_id(
                event=event,
                source_event_sha256=source_event_sha256,
                trace_sha256=trace_sha256,
                codec_identity_sha256=self._codec_identity_sha256,
                actuator_identity_sha256=self._actuator_identity_sha256,
                importance=importance,
                prediction_error=prediction_error,
                update_norm=update_norm,
                update_budget=update_budget,
                supersedes_event_id=request.supersedes_event_id,
            )
            if experience_id in self._records:
                raise ExperiencePortError("E3_TRACE_IDENTITY_DUPLICATE")

            if auto_advance:
                self._advance_unlocked(self._origin, event.stamp)

            slot, evicted = self._allocate_slot()
            resulting = dict(self._records)
            if target is not None:
                updated_target = replace(
                    target, superseded_by_event_id=event.event_id
                )
                resulting[target.experience_id] = updated_target
            if evicted is not None:
                resulting.pop(evicted.experience_id, None)

            provisional = SoftPrefixTraceRecord(
                experience_id=experience_id,
                content=bytes(request.content),
                source=request.source,
                encoding_origin=request.origin,
                context=copy.deepcopy(dict(request.context)),
                event_id=event.event_id,
                prior_event_sha256=event.prior_event_sha256,
                event_sha256=event.event_sha256,
                source_event_bytes=source_event_bytes,
                source_event_sha256=source_event_sha256,
                trace_bytes=trace_bytes,
                trace_sha256=trace_sha256,
                codec_identity_sha256=self._codec_identity_sha256,
                actuator_identity_sha256=self._actuator_identity_sha256,
                sequence=self._next_sequence,
                slot=slot,
                importance=importance,
                prediction_error=prediction_error,
                update_norm=update_norm,
                update_budget=update_budget,
                supersedes_event_id=request.supersedes_event_id,
                superseded_by_event_id=None,
                write_receipt_sha256=SHA256_ZERO,
            )
            resulting[experience_id] = provisional
            prior_strip_head, resulting_strip_head = self._mutate_head(
                "write_experience",
                {
                    "source_log_head": self._origin.log_head,
                    "record": _record_identity(provisional),
                    "evicted_experience_id": (
                        None if evicted is None else evicted.experience_id
                    ),
                    "resulting_records": _state_record_identities(resulting),
                },
            )
            del prior_strip_head
            record = replace(
                provisional, write_receipt_sha256=resulting_strip_head
            )
            resulting[experience_id] = record
            self._records = resulting
            self._rebuild_event_index()
            self._next_sequence += 1
            self._next_slot = (slot + 1) % self._capacity
            self._written_current_event_id = event.event_id
            return _copy_record(record)

    def append_committed(
        self,
        event: CommittedOriginEvent,
        *,
        importance: int | float = 1,
        prediction_error: int | float = 0,
        supersedes_event_id: str | None = None,
    ) -> SoftPrefixTraceRecord:
        """Atomically advance when needed and append one committed event."""

        return self.write_experience(
            ExperienceWrite.from_committed_event(
                event,
                importance=importance,
                prediction_error=prediction_error,
                supersedes_event_id=supersedes_event_id,
            )
        )

    def retrieve_by_origin_distance(
        self,
        query: MemoryQuery,
        origin: SituatedOriginFrame,
        max_distance: int,
    ) -> SoftPrefixRetrieval:
        if not isinstance(query, MemoryQuery):
            raise ExperiencePortError("E3_MEMORY_QUERY_REQUIRED")
        if type(max_distance) is not int or max_distance < 0:
            raise ExperiencePortError("E3_ORIGIN_DISTANCE_INVALID")
        with self._lock:
            self._require_current_frame(origin)
            candidates = tuple(
                record
                for record in self._records.values()
                if origin.stamp.cycle - record.encoding_origin.cycle <= max_distance
                and (query.include_stale or record.superseded_by_event_id is None)
            )
            requested = tuple(
                item.event_id for item in sorted(candidates, key=lambda row: row.event_id)
            )
            return self._build_retrieval(
                candidates,
                origin,
                limit=query.limit,
                requested_event_ids=requested,
                query_identity={
                    "mode": "origin_distance",
                    "query": query,
                    "max_distance": max_distance,
                },
            )

    def retrieve_by_event_ids(
        self,
        event_ids: Iterable[str],
        origin: SituatedOriginFrame,
        *,
        include_superseded: bool = False,
        limit: int | None = None,
    ) -> SoftPrefixRetrieval:
        if type(include_superseded) is not bool:
            raise ExperiencePortError("E3_INCLUDE_SUPERSEDED_BOOLEAN_REQUIRED")
        if limit is None:
            limit = self._capacity
        if type(limit) is not int or limit < 1:
            raise ExperiencePortError("E3_RETRIEVAL_LIMIT_INVALID")
        requested: list[str] = []
        seen: set[str] = set()
        try:
            for event_id in event_ids:
                if type(event_id) is not str or not event_id:
                    raise ExperiencePortError("E3_EVENT_ID_INVALID")
                if event_id not in seen:
                    requested.append(event_id)
                    seen.add(event_id)
        except TypeError as exc:
            raise ExperiencePortError("E3_EVENT_IDS_REQUIRED") from exc

        with self._lock:
            self._require_current_frame(origin)
            candidates: list[SoftPrefixTraceRecord] = []
            for event_id in requested:
                experience_id = self._event_index.get(event_id)
                if experience_id is None:
                    continue
                record = self._records[experience_id]
                if include_superseded or record.superseded_by_event_id is None:
                    candidates.append(record)
            return self._build_retrieval(
                tuple(candidates),
                origin,
                limit=limit,
                requested_event_ids=tuple(requested),
                query_identity={
                    "mode": "event_ids",
                    "event_ids": tuple(requested),
                    "include_superseded": include_superseded,
                },
            )

    def materialize_trace(
        self, experience_id: str, *, source_log_head: str
    ) -> object:
        """Decode one trace and verify the codec reproduces its exact bytes."""

        with self._lock:
            if source_log_head != self._origin.log_head:
                raise ExperiencePortError("E3_VIEW_HEAD_STALE")
            record = self._require_record(experience_id)
            try:
                value = self._codec.from_bytes(bytes(record.trace_bytes))
                reproduced = self._codec.to_bytes(value)
            except Exception as exc:
                raise ExperiencePortError("E3_TRACE_DESERIALIZATION_FAILED") from exc
            if type(reproduced) is not bytes or reproduced != record.trace_bytes:
                raise ExperiencePortError("E3_TRACE_CODEC_NONCANONICAL")
            return value

    def consolidate(
        self, through: OriginStamp
    ) -> SoftPrefixConsolidationReceipt:
        """Release eligible projection traces with ledger-resolvable receipts.

        Consolidation does not synthesize a replacement fact from strip state.
        The returned source event IDs are the inputs a ledger-backed durable
        consolidator must resolve; this tape can then safely reuse their slots.
        """

        with self._lock:
            self._validate_consolidation_origin(through)
            eligible = tuple(
                sorted(
                    (
                        record
                        for record in self._records.values()
                        if record.encoding_origin.event_ordinal
                        <= through.event_ordinal
                    ),
                    key=lambda item: (item.sequence, item.event_id),
                )
            )
            resulting = dict(self._records)
            for record in eligible:
                resulting.pop(record.experience_id)
            prior_head, result_head = self._mutate_head(
                "consolidate",
                {
                    "through_origin": through,
                    "consolidated": tuple(
                        {
                            "experience_id": item.experience_id,
                            "event_id": item.event_id,
                            "event_sha256": item.event_sha256,
                            "source_event_sha256": item.source_event_sha256,
                            "trace_sha256": item.trace_sha256,
                        }
                        for item in eligible
                    ),
                    "resulting_records": _state_record_identities(resulting),
                },
            )
            self._records = resulting
            self._rebuild_event_index()
            return SoftPrefixConsolidationReceipt(
                through_origin=through,
                consolidated_ids=tuple(item.experience_id for item in eligible),
                receipt_sha256=result_head,
                consolidated_event_ids=tuple(item.event_id for item in eligible),
                source_event_sha256s=tuple(
                    item.source_event_sha256 for item in eligible
                ),
                prior_strip_head=prior_head,
                resulting_strip_head=result_head,
                source_log_head=self._origin.log_head,
            )

    def compare_to_log(
        self, experience_id: str, event: CommittedOriginEvent
    ) -> ExperienceLogComparison:
        event_bytes = _validate_committed_event(event)
        with self._lock:
            record = self._require_record(experience_id)
            matches = (
                record.event_id == event.event_id
                and record.event_sha256 == event.event_sha256
                and record.prior_event_sha256 == event.prior_event_sha256
                and record.source_event_bytes == event_bytes
            )
            receipt = sha256_canonical(
                {
                    "schema_version": _RECEIPT_VERSION,
                    "operation": "compare_to_log",
                    "strip_head": self._head,
                    "source_log_head": self._origin.log_head,
                    "experience_id": experience_id,
                    "stored_source_event_sha256": record.source_event_sha256,
                    "compared_event_id": event.event_id,
                    "compared_source_event_sha256": sha256_bytes(event_bytes),
                    "matches": matches,
                }
            )
            return ExperienceLogComparison(
                experience_id=experience_id,
                event_id=event.event_id,
                matches=matches,
                receipt_sha256=receipt,
            )

    def snapshot(self) -> tuple[SoftPrefixTraceRecord, ...]:
        with self._lock:
            return tuple(
                _copy_record(item)
                for item in sorted(
                    self._records.values(), key=lambda row: (row.sequence, row.event_id)
                )
            )

    def to_bytes(self) -> bytes:
        with self._lock:
            payload = self._checkpoint_payload()
            envelope = {
                "payload": payload,
                "state_sha256": sha256_canonical(payload),
            }
            return canonical_bytes(envelope)

    def checkpoint_receipt(self) -> SoftPrefixCheckpointReceipt:
        data = self.to_bytes()
        with self._lock:
            return _checkpoint_receipt(data, self._head, self._origin.log_head)

    def save(
        self, path: str | os.PathLike[str], *, overwrite: bool = False
    ) -> SoftPrefixCheckpointReceipt:
        if type(overwrite) is not bool:
            raise ExperiencePortError("E3_OVERWRITE_BOOLEAN_REQUIRED")
        target = Path(path)
        if target.exists() and not overwrite:
            raise ExperiencePortError("E3_CHECKPOINT_EXISTS")
        if not target.parent.is_dir():
            raise ExperiencePortError("E3_CHECKPOINT_PARENT_MISSING")
        data = self.to_bytes()
        temporary: str | None = None
        try:
            descriptor, temporary = tempfile.mkstemp(
                prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
            )
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, target)
            temporary = None
        except OSError as exc:
            raise ExperiencePortError("E3_CHECKPOINT_WRITE_FAILED") from exc
        finally:
            if temporary is not None:
                try:
                    Path(temporary).unlink()
                except OSError:
                    pass
        if target.read_bytes() != data:
            raise ExperiencePortError("E3_CHECKPOINT_BYTE_MISMATCH")
        with self._lock:
            return _checkpoint_receipt(data, self._head, self._origin.log_head)

    @classmethod
    def load(
        cls,
        path: str | os.PathLike[str],
        *,
        trace_encoder: Callable[[ExperienceWrite], OpaqueTraceUpdate],
        codec: OpaqueTraceCodec,
        actuator_identity_sha256: str,
        expected_checkpoint_sha256: str | None = None,
    ) -> "SoftPrefixExperienceStrip":
        try:
            data = Path(path).read_bytes()
        except OSError as exc:
            raise ExperiencePortError("E3_CHECKPOINT_READ_FAILED") from exc
        if (
            expected_checkpoint_sha256 is not None
            and sha256_bytes(data) != expected_checkpoint_sha256
        ):
            raise ExperiencePortError("E3_CHECKPOINT_DIGEST_MISMATCH")
        return cls.from_bytes(
            data,
            trace_encoder=trace_encoder,
            codec=codec,
            actuator_identity_sha256=actuator_identity_sha256,
        )

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
        *,
        trace_encoder: Callable[[ExperienceWrite], OpaqueTraceUpdate],
        codec: OpaqueTraceCodec,
        actuator_identity_sha256: str,
    ) -> "SoftPrefixExperienceStrip":
        if type(data) is not bytes:
            raise ExperiencePortError("E3_CHECKPOINT_BYTES_REQUIRED")
        try:
            envelope = _json_loads_strict(data)
            if canonical_bytes(envelope) != data:
                raise ExperiencePortError("E3_CHECKPOINT_NONCANONICAL")
            payload = envelope["payload"]
            if envelope["state_sha256"] != sha256_canonical(payload):
                raise ExperiencePortError("E3_CHECKPOINT_STATE_MISMATCH")
            if payload["schema_version"] != _SCHEMA_VERSION:
                raise ExperiencePortError("E3_CHECKPOINT_SCHEMA_UNSUPPORTED")
            if payload["codec_identity_sha256"] != getattr(
                codec, "identity_sha256", None
            ):
                raise ExperiencePortError("E3_CHECKPOINT_CODEC_MISMATCH")
            if payload["actuator_identity_sha256"] != actuator_identity_sha256:
                raise ExperiencePortError("E3_CHECKPOINT_ACTUATOR_MISMATCH")
            instance = cls(
                payload["life_id"],
                epoch=payload["epoch"],
                capacity=payload["capacity"],
                trace_encoder=trace_encoder,
                codec=codec,
                actuator_identity_sha256=actuator_identity_sha256,
                decay_factor=Decimal(payload["decay_factor"]),
                max_trace_bytes=payload["max_trace_bytes"],
            )
            instance._origin = OriginStamp(**payload["origin"])
            require_sha256(payload["strip_head"], "E3_STRIP_HEAD_INVALID")
            instance._head = payload["strip_head"]
            instance._next_sequence = payload["next_sequence"]
            instance._next_slot = payload["next_slot"]
            instance._current_transition_prior_head = payload[
                "current_transition_prior_head"
            ]
            instance._current_event_id = payload["current_event_id"]
            instance._written_current_event_id = payload[
                "written_current_event_id"
            ]
            records = tuple(_record_from_obj(row) for row in payload["records"])
            instance._records = {item.experience_id: item for item in records}
            instance._rebuild_event_index()
            instance._validate_loaded_state(records)
            if instance.to_bytes() != data:
                raise ExperiencePortError("E3_CHECKPOINT_ROUNDTRIP_MISMATCH")
            return instance
        except ExperiencePortError:
            raise
        except (KeyError, TypeError, ValueError, UnicodeError, InvalidOperation) as exc:
            raise ExperiencePortError("E3_CHECKPOINT_INVALID") from exc

    def _advance_unlocked(
        self, prior: OriginStamp, current: OriginStamp
    ) -> SoftPrefixAdvanceReceipt:
        if prior != self._origin:
            raise ExperiencePortError("E3_ORIGIN_PRIOR_MISMATCH")
        _validate_origin_transition(prior, current, self._life_id, self._epoch)
        prior_head, result_head = self._mutate_head(
            "advance_origin",
            {
                "prior_origin": prior,
                "current_origin": current,
                "records": _state_record_identities(self._records),
            },
        )
        self._origin = current
        self._current_transition_prior_head = prior.log_head
        self._current_event_id = _event_id_for_stamp(current)
        self._written_current_event_id = None
        receipt = SoftPrefixAdvanceReceipt(
            prior_origin=prior,
            current_origin=current,
            receipt_sha256=result_head,
            prior_strip_head=prior_head,
            resulting_strip_head=result_head,
            source_log_head=current.log_head,
        )
        self._last_advance_receipt = receipt
        return receipt

    def _prepare_event_position(self, event: CommittedOriginEvent) -> bool:
        if event.stamp.life_id != self._life_id or event.stamp.epoch != self._epoch:
            raise ExperiencePortError("E3_EVENT_ORIGIN_IDENTITY_MISMATCH")
        if event.stamp == self._origin:
            if (
                self._current_event_id != event.event_id
                or self._current_transition_prior_head
                != event.prior_event_sha256
            ):
                raise ExperiencePortError("E3_LEDGER_EVENT_NOT_CURRENT")
            return False
        if event.prior_event_sha256 != self._origin.log_head:
            raise ExperiencePortError("E3_LEDGER_CHAIN_MISMATCH")
        _validate_origin_transition(
            self._origin, event.stamp, self._life_id, self._epoch
        )
        return True

    def _allocate_slot(
        self,
    ) -> tuple[int, SoftPrefixTraceRecord | None]:
        occupied = {item.slot: item for item in self._records.values()}
        if len(occupied) < self._capacity:
            for offset in range(self._capacity):
                slot = (self._next_slot + offset) % self._capacity
                if slot not in occupied:
                    return slot, None
            raise ExperiencePortError("E3_CAPACITY_STATE_INVALID")
        try:
            return self._next_slot, occupied[self._next_slot]
        except KeyError as exc:
            raise ExperiencePortError("E3_CAPACITY_STATE_INVALID") from exc

    def _build_retrieval(
        self,
        candidates: tuple[SoftPrefixTraceRecord, ...],
        origin: SituatedOriginFrame,
        *,
        limit: int,
        requested_event_ids: tuple[str, ...],
        query_identity: Mapping[str, Any],
    ) -> SoftPrefixRetrieval:
        ranked = sorted(
            (
                (
                    record,
                    origin.stamp.cycle - record.encoding_origin.cycle,
                    record.importance
                    * (
                        self._decay_factor
                        ** (origin.stamp.cycle - record.encoding_origin.cycle)
                    ),
                )
                for record in candidates
            ),
            key=lambda row: (
                -row[2],
                row[1],
                -row[0].encoding_origin.event_ordinal,
                row[0].event_id,
            ),
        )[:limit]
        records = tuple(_copy_record(row[0]) for row in ranked)
        rankings = tuple(
            SoftPrefixTraceRank(records[index], row[1], row[2])
            for index, row in enumerate(ranked)
        )
        selected_event_ids = tuple(item.record.event_id for item in rankings)
        receipt = sha256_canonical(
            {
                "schema_version": _RECEIPT_VERSION,
                "operation": "retrieve",
                "strip_head": self._head,
                "source_log_head": self._origin.log_head,
                "query_origin": {
                    "stamp": origin.stamp,
                    "frame_sha256": origin.frame_sha256,
                },
                "query": query_identity,
                "requested_event_ids": requested_event_ids,
                "selected": tuple(
                    {
                        "experience_id": row.record.experience_id,
                        "event_id": row.record.event_id,
                        "trace_sha256": row.record.trace_sha256,
                        "origin_distance": row.origin_distance,
                        "effective_importance": _decimal_text(
                            row.effective_importance
                        ),
                    }
                    for row in rankings
                ),
            }
        )
        return SoftPrefixRetrieval(
            records=records,
            query_origin=origin,
            receipt_sha256=receipt,
            rankings=rankings,
            selected_event_ids=selected_event_ids,
            requested_event_ids=requested_event_ids,
            source_log_head=self._origin.log_head,
        )

    def _require_current_frame(self, origin: SituatedOriginFrame) -> None:
        if not isinstance(origin, SituatedOriginFrame):
            raise ExperiencePortError("E3_ORIGIN_FRAME_REQUIRED")
        if origin.stamp != self._origin:
            raise ExperiencePortError("E3_VIEW_HEAD_STALE")

    def _validate_consolidation_origin(self, through: OriginStamp) -> None:
        if not isinstance(through, OriginStamp):
            raise ExperiencePortError("E3_CONSOLIDATION_ORIGIN_REQUIRED")
        if through.life_id != self._life_id or through.epoch != self._epoch:
            raise ExperiencePortError("E3_CONSOLIDATION_ORIGIN_MISMATCH")
        if (
            through.event_ordinal > self._origin.event_ordinal
            or through.cycle > self._origin.cycle
        ):
            raise ExperiencePortError("E3_CONSOLIDATION_FUTURE_ORIGIN")
        known = through == self._origin or any(
            item.encoding_origin == through for item in self._records.values()
        )
        if not known:
            raise ExperiencePortError("E3_CONSOLIDATION_ORIGIN_UNRESOLVED")

    def _record_for_event(self, event_id: str) -> SoftPrefixTraceRecord:
        try:
            return self._records[self._event_index[event_id]]
        except KeyError as exc:
            raise ExperiencePortError("E3_SUPERSESSION_TARGET_UNKNOWN") from exc

    def _require_record(self, experience_id: str) -> SoftPrefixTraceRecord:
        try:
            return self._records[experience_id]
        except KeyError as exc:
            raise ExperiencePortError("E3_EXPERIENCE_NOT_FOUND") from exc

    def _rebuild_event_index(self) -> None:
        self._event_index = {
            item.event_id: item.experience_id for item in self._records.values()
        }

    def _mutate_head(
        self, operation: str, payload: Mapping[str, Any]
    ) -> tuple[str, str]:
        prior = self._head
        result = sha256_canonical(
            {
                "schema_version": _RECEIPT_VERSION,
                "operation": operation,
                "prior_strip_head": prior,
                "payload": payload,
            }
        )
        self._head = result
        return prior, result

    def _checkpoint_payload(self) -> dict[str, Any]:
        return {
            "schema_version": _SCHEMA_VERSION,
            "life_id": self._life_id,
            "epoch": self._epoch,
            "capacity": self._capacity,
            "max_trace_bytes": self._max_trace_bytes,
            "decay_factor": _decimal_text(self._decay_factor),
            "codec_identity_sha256": self._codec_identity_sha256,
            "actuator_identity_sha256": self._actuator_identity_sha256,
            "origin": to_primitive(self._origin),
            "strip_head": self._head,
            "next_sequence": self._next_sequence,
            "next_slot": self._next_slot,
            "current_transition_prior_head": self._current_transition_prior_head,
            "current_event_id": self._current_event_id,
            "written_current_event_id": self._written_current_event_id,
            "records": tuple(
                _record_to_obj(item)
                for item in sorted(
                    self._records.values(), key=lambda row: (row.sequence, row.event_id)
                )
            ),
        }

    def _validate_loaded_state(
        self, records: tuple[SoftPrefixTraceRecord, ...]
    ) -> None:
        if type(self._next_sequence) is not int or self._next_sequence < 0:
            raise ExperiencePortError("E3_CHECKPOINT_SEQUENCE_INVALID")
        if (
            type(self._next_slot) is not int
            or self._next_slot < 0
            or self._next_slot >= self._capacity
        ):
            raise ExperiencePortError("E3_CHECKPOINT_SLOT_INVALID")
        if len(records) > self._capacity:
            raise ExperiencePortError("E3_CHECKPOINT_CAPACITY_EXCEEDED")
        if len(self._records) != len(records) or len(self._event_index) != len(records):
            raise ExperiencePortError("E3_CHECKPOINT_DUPLICATE_RECORD")
        slots = {item.slot for item in records}
        if len(slots) != len(records) or any(
            type(slot) is not int or slot < 0 or slot >= self._capacity
            for slot in slots
        ):
            raise ExperiencePortError("E3_CHECKPOINT_SLOT_INVALID")
        if records and self._next_sequence <= max(item.sequence for item in records):
            raise ExperiencePortError("E3_CHECKPOINT_SEQUENCE_INVALID")
        for record in records:
            if record.encoding_origin.life_id != self._life_id or record.encoding_origin.epoch != self._epoch:
                raise ExperiencePortError("E3_CHECKPOINT_ORIGIN_MISMATCH")
            if record.encoding_origin.event_ordinal > self._origin.event_ordinal:
                raise ExperiencePortError("E3_CHECKPOINT_FUTURE_TRACE")
            if len(record.trace_bytes) > self._max_trace_bytes:
                raise ExperiencePortError("E3_TRACE_BYTE_LIMIT_EXCEEDED")
            if sha256_bytes(record.trace_bytes) != record.trace_sha256:
                raise ExperiencePortError("E3_TRACE_DIGEST_MISMATCH")
            if sha256_bytes(record.source_event_bytes) != record.source_event_sha256:
                raise ExperiencePortError("E3_SOURCE_EVENT_DIGEST_MISMATCH")
            if record.codec_identity_sha256 != self._codec_identity_sha256:
                raise ExperiencePortError("E3_CHECKPOINT_CODEC_MISMATCH")
            if record.actuator_identity_sha256 != self._actuator_identity_sha256:
                raise ExperiencePortError("E3_CHECKPOINT_ACTUATOR_MISMATCH")
            expected_id = _experience_id_from_record(record)
            if record.experience_id != expected_id:
                raise ExperiencePortError("E3_TRACE_IDENTITY_MISMATCH")
            require_sha256(
                record.write_receipt_sha256, "E3_WRITE_RECEIPT_INVALID"
            )
            _validate_source_event_projection(record)
        if self._origin.life_id != self._life_id or self._origin.epoch != self._epoch:
            raise ExperiencePortError("E3_CHECKPOINT_ORIGIN_MISMATCH")
        if self._current_event_id is not None:
            expected = _event_id_for_stamp(self._origin)
            if self._current_event_id != expected:
                raise ExperiencePortError("E3_CHECKPOINT_CURRENT_EVENT_INVALID")
        if self._current_transition_prior_head is not None:
            require_sha256(
                self._current_transition_prior_head,
                "E3_CHECKPOINT_PRIOR_HEAD_INVALID",
            )
        if self._written_current_event_id not in (None, self._current_event_id):
            raise ExperiencePortError("E3_CHECKPOINT_WRITTEN_EVENT_INVALID")


# Compact public name for callers that do not need the milestone-qualified name.
SoftPrefixStrip = SoftPrefixExperienceStrip


def _validate_bound_request(
    request: ExperienceWrite,
) -> tuple[CommittedOriginEvent, bytes]:
    if not isinstance(request, ExperienceWrite):
        raise ExperiencePortError("E3_EXPERIENCE_WRITE_REQUIRED")
    event = request.committed_event
    if not isinstance(event, CommittedOriginEvent):
        raise ExperiencePortError("E3_COMMITTED_EVENT_REQUIRED")
    event_bytes = _validate_committed_event(event)
    try:
        request_context = canonical_bytes(request.context)
        event_context = canonical_bytes(event.proposal.context)
    except (TypeError, ValueError) as exc:
        raise ExperiencePortError("E3_EVENT_CONTEXT_NONCANONICAL") from exc
    if (
        request.content != event.proposal.content
        or request.source != event.proposal.source
        or request_context != event_context
        or request.origin != event.stamp
    ):
        raise ExperiencePortError("E3_COMMITTED_EVENT_BINDING_MISMATCH")
    return event, event_bytes


def _validate_committed_event(event: CommittedOriginEvent) -> bytes:
    if not isinstance(event, CommittedOriginEvent):
        raise ExperiencePortError("E3_COMMITTED_EVENT_REQUIRED")
    expected_event_id = _event_id_for_stamp(event.stamp)
    expected_sha256 = sha256_canonical(
        {
            "event_id": event.event_id,
            "life_id": event.stamp.life_id,
            "epoch": event.stamp.epoch,
            "cycle": event.stamp.cycle,
            "event_ordinal": event.stamp.event_ordinal,
            "prior_event_sha256": event.prior_event_sha256,
            "proposal": event.proposal,
        }
    )
    if (
        event.event_id != expected_event_id
        or event.event_sha256 != expected_sha256
        or event.stamp.log_head != expected_sha256
    ):
        raise ExperiencePortError("E3_COMMITTED_EVENT_INVALID")
    try:
        return canonical_bytes(event)
    except (TypeError, ValueError) as exc:
        raise ExperiencePortError("E3_COMMITTED_EVENT_NONCANONICAL") from exc


def _validate_origin_transition(
    prior: OriginStamp, current: OriginStamp, life_id: str, epoch: int
) -> None:
    if not isinstance(prior, OriginStamp) or not isinstance(current, OriginStamp):
        raise ExperiencePortError("E3_ORIGIN_STAMP_REQUIRED")
    if (
        prior.life_id != life_id
        or current.life_id != life_id
        or prior.epoch != epoch
        or current.epoch != epoch
    ):
        raise ExperiencePortError("E3_ORIGIN_IDENTITY_MISMATCH")
    if current.event_ordinal != prior.event_ordinal + 1:
        raise ExperiencePortError("E3_EVENT_ORDINAL_DISCONTINUITY")
    if current.cycle not in (prior.cycle, prior.cycle + 1):
        raise ExperiencePortError("E3_ORIGIN_CYCLE_DISCONTINUITY")
    if prior.event_ordinal == -1 and current.cycle != 0:
        raise ExperiencePortError("E3_ORIGIN_INITIAL_CYCLE_INVALID")
    if current.log_head == prior.log_head:
        raise ExperiencePortError("E3_LOG_HEAD_DID_NOT_ADVANCE")


def _event_id_for_stamp(stamp: OriginStamp) -> str:
    return f"{stamp.life_id}:{stamp.epoch}:{stamp.event_ordinal:020d}"


def _decimal(value: object, code: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal, str)):
        raise ExperiencePortError(code)
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ExperiencePortError(code) from exc
    if not result.is_finite():
        raise ExperiencePortError(code)
    return result


def _decimal_text(value: Decimal) -> str:
    if value == 0:
        return "0"
    return format(value.normalize(), "f")


def _experience_id(
    *,
    event: CommittedOriginEvent,
    source_event_sha256: str,
    trace_sha256: str,
    codec_identity_sha256: str,
    actuator_identity_sha256: str,
    importance: Decimal,
    prediction_error: Decimal,
    update_norm: Decimal,
    update_budget: Decimal,
    supersedes_event_id: str | None,
) -> str:
    return sha256_canonical(
        {
            "schema_version": _SCHEMA_VERSION,
            "event_id": event.event_id,
            "event_sha256": event.event_sha256,
            "source_event_sha256": source_event_sha256,
            "trace_sha256": trace_sha256,
            "codec_identity_sha256": codec_identity_sha256,
            "actuator_identity_sha256": actuator_identity_sha256,
            "importance": _decimal_text(importance),
            "prediction_error": _decimal_text(prediction_error),
            "update_norm": _decimal_text(update_norm),
            "update_budget": _decimal_text(update_budget),
            "supersedes_event_id": supersedes_event_id,
        }
    )


def _experience_id_from_record(record: SoftPrefixTraceRecord) -> str:
    event_stub = type("EventIdentity", (), {})()
    event_stub.event_id = record.event_id
    event_stub.event_sha256 = record.event_sha256
    return _experience_id(
        event=event_stub,  # type: ignore[arg-type]
        source_event_sha256=record.source_event_sha256,
        trace_sha256=record.trace_sha256,
        codec_identity_sha256=record.codec_identity_sha256,
        actuator_identity_sha256=record.actuator_identity_sha256,
        importance=record.importance,
        prediction_error=record.prediction_error,
        update_norm=record.update_norm,
        update_budget=record.update_budget,
        supersedes_event_id=record.supersedes_event_id,
    )


def _record_identity(record: SoftPrefixTraceRecord) -> dict[str, Any]:
    return {
        "experience_id": record.experience_id,
        "event_id": record.event_id,
        "event_sha256": record.event_sha256,
        "source_event_sha256": record.source_event_sha256,
        "trace_sha256": record.trace_sha256,
        "codec_identity_sha256": record.codec_identity_sha256,
        "actuator_identity_sha256": record.actuator_identity_sha256,
        "sequence": record.sequence,
        "slot": record.slot,
        "importance": _decimal_text(record.importance),
        "prediction_error": _decimal_text(record.prediction_error),
        "update_norm": _decimal_text(record.update_norm),
        "update_budget": _decimal_text(record.update_budget),
        "supersedes_event_id": record.supersedes_event_id,
        "superseded_by_event_id": record.superseded_by_event_id,
    }


def _state_record_identities(
    records: Mapping[str, SoftPrefixTraceRecord],
) -> tuple[dict[str, Any], ...]:
    return tuple(
        _record_identity(item)
        for item in sorted(
            records.values(), key=lambda row: (row.slot, row.sequence, row.event_id)
        )
    )


def _copy_record(record: SoftPrefixTraceRecord) -> SoftPrefixTraceRecord:
    return replace(record, context=copy.deepcopy(dict(record.context)))


def _record_to_obj(record: SoftPrefixTraceRecord) -> dict[str, Any]:
    return {
        "experience_id": record.experience_id,
        "content_hex": record.content.hex(),
        "source": to_primitive(record.source),
        "encoding_origin": to_primitive(record.encoding_origin),
        "context": json.loads(canonical_bytes(record.context).decode("utf-8")),
        "event_id": record.event_id,
        "prior_event_sha256": record.prior_event_sha256,
        "event_sha256": record.event_sha256,
        "source_event_hex": record.source_event_bytes.hex(),
        "source_event_sha256": record.source_event_sha256,
        "trace_hex": record.trace_bytes.hex(),
        "trace_sha256": record.trace_sha256,
        "codec_identity_sha256": record.codec_identity_sha256,
        "actuator_identity_sha256": record.actuator_identity_sha256,
        "sequence": record.sequence,
        "slot": record.slot,
        "importance": _decimal_text(record.importance),
        "prediction_error": _decimal_text(record.prediction_error),
        "update_norm": _decimal_text(record.update_norm),
        "update_budget": _decimal_text(record.update_budget),
        "supersedes_event_id": record.supersedes_event_id,
        "superseded_by_event_id": record.superseded_by_event_id,
        "write_receipt_sha256": record.write_receipt_sha256,
    }


def _record_from_obj(obj: Mapping[str, Any]) -> SoftPrefixTraceRecord:
    from .contracts import ProvenanceHandle

    record = SoftPrefixTraceRecord(
        experience_id=obj["experience_id"],
        content=bytes.fromhex(obj["content_hex"]),
        source=ProvenanceHandle(**obj["source"]),
        encoding_origin=OriginStamp(**obj["encoding_origin"]),
        context=copy.deepcopy(obj["context"]),
        event_id=obj["event_id"],
        prior_event_sha256=obj["prior_event_sha256"],
        event_sha256=obj["event_sha256"],
        source_event_bytes=bytes.fromhex(obj["source_event_hex"]),
        source_event_sha256=obj["source_event_sha256"],
        trace_bytes=bytes.fromhex(obj["trace_hex"]),
        trace_sha256=obj["trace_sha256"],
        codec_identity_sha256=obj["codec_identity_sha256"],
        actuator_identity_sha256=obj["actuator_identity_sha256"],
        sequence=obj["sequence"],
        slot=obj["slot"],
        importance=Decimal(obj["importance"]),
        prediction_error=Decimal(obj["prediction_error"]),
        update_norm=Decimal(obj["update_norm"]),
        update_budget=Decimal(obj["update_budget"]),
        supersedes_event_id=obj["supersedes_event_id"],
        superseded_by_event_id=obj["superseded_by_event_id"],
        write_receipt_sha256=obj["write_receipt_sha256"],
    )
    for value, code in (
        (record.prior_event_sha256, "E3_PRIOR_EVENT_DIGEST_INVALID"),
        (record.event_sha256, "E3_EVENT_DIGEST_INVALID"),
        (record.source_event_sha256, "E3_SOURCE_EVENT_DIGEST_INVALID"),
        (record.trace_sha256, "E3_TRACE_DIGEST_INVALID"),
        (record.codec_identity_sha256, "E3_CODEC_IDENTITY_INVALID"),
        (record.actuator_identity_sha256, "E3_ACTUATOR_IDENTITY_INVALID"),
        (record.write_receipt_sha256, "E3_WRITE_RECEIPT_INVALID"),
    ):
        require_sha256(value, code)
    if type(record.sequence) is not int or record.sequence < 0:
        raise ExperiencePortError("E3_CHECKPOINT_SEQUENCE_INVALID")
    if record.importance < 0 or record.prediction_error < 0 or record.update_norm < 0:
        raise ExperiencePortError("E3_CHECKPOINT_NUMERIC_METADATA_INVALID")
    if record.update_budget < 0 or record.update_norm > record.update_budget:
        raise ExperiencePortError("E3_UPDATE_BUDGET_EXCEEDED")
    return record


def _validate_source_event_projection(record: SoftPrefixTraceRecord) -> None:
    event_obj = _json_loads_strict(record.source_event_bytes)
    if canonical_bytes(event_obj) != record.source_event_bytes:
        raise ExperiencePortError("E3_SOURCE_EVENT_NONCANONICAL")
    expected = {
        "event_id": record.event_id,
        "prior_event_sha256": record.prior_event_sha256,
        "event_sha256": record.event_sha256,
        "stamp": to_primitive(record.encoding_origin),
        "content": to_primitive(record.content),
        "source": to_primitive(record.source),
        "context": json.loads(canonical_bytes(record.context).decode("utf-8")),
    }
    try:
        actual = {
            "event_id": event_obj["event_id"],
            "prior_event_sha256": event_obj["prior_event_sha256"],
            "event_sha256": event_obj["event_sha256"],
            "stamp": event_obj["stamp"],
            "content": event_obj["proposal"]["content"],
            "source": event_obj["proposal"]["source"],
            "context": event_obj["proposal"]["context"],
        }
    except (KeyError, TypeError) as exc:
        raise ExperiencePortError("E3_SOURCE_EVENT_INVALID") from exc
    if actual != expected:
        raise ExperiencePortError("E3_SOURCE_EVENT_PROJECTION_MISMATCH")


def _checkpoint_receipt(
    data: bytes, strip_head: str, source_log_head: str
) -> SoftPrefixCheckpointReceipt:
    checkpoint_sha256 = sha256_bytes(data)
    body = {
        "schema_version": _RECEIPT_VERSION,
        "operation": "checkpoint",
        "strip_head": strip_head,
        "source_log_head": source_log_head,
        "checkpoint_sha256": checkpoint_sha256,
        "byte_count": len(data),
    }
    return SoftPrefixCheckpointReceipt(
        strip_head=strip_head,
        source_log_head=source_log_head,
        checkpoint_sha256=checkpoint_sha256,
        byte_count=len(data),
        receipt_sha256=sha256_canonical(body),
    )


def _json_loads_strict(data: bytes) -> Any:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ExperiencePortError("E3_CHECKPOINT_DUPLICATE_KEY")
            result[key] = value
        return result

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=no_duplicates)
    except ExperiencePortError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ExperiencePortError("E3_CHECKPOINT_INVALID_JSON") from exc


__all__ = [
    "OpaqueTraceCodec",
    "OpaqueTraceUpdate",
    "SoftPrefixAdvanceReceipt",
    "SoftPrefixCheckpointReceipt",
    "SoftPrefixConsolidationReceipt",
    "SoftPrefixExperienceStrip",
    "SoftPrefixRetrieval",
    "SoftPrefixStrip",
    "SoftPrefixTraceRank",
    "SoftPrefixTraceRecord",
]
