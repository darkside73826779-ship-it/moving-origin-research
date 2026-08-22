"""Durable-ID L4 origin index projected only from committed kernel events."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Iterable

from .contracts import (
    CommittedOriginEvent,
    OriginContractError,
    SHA256_ZERO,
    require_sha256,
    sha256_bytes,
    sha256_canonical,
    to_primitive,
)


BEFORE = "BEFORE_L"
AT = "AT_L"
AFTER = "AFTER_L"
RELATIONS = (BEFORE, AT, AFTER)

DESIGNATE_IMMEDIATE = "DESIGNATE_IMMEDIATE"
DESIGNATE_DEFERRED = "DESIGNATE_DEFERRED"
_ACTIONS = (DESIGNATE_IMMEDIATE, DESIGNATE_DEFERRED)


@dataclass(frozen=True)
class IndexedOriginEvent:
    event_id: str
    cycle: int
    event_ordinal: int
    source_kind: str
    content_sha256: str


@dataclass(frozen=True)
class LandmarkRecord:
    landmark_event_id: str
    designation_event_id: str
    mode: str
    designated_at_cycle: int
    designation_event_ordinal: int


@dataclass(frozen=True)
class OriginCoordinate:
    event_id: str
    encoding_cycle: int
    current_cycle: int
    cycle_relative_distance: int
    landmark_relations: tuple[tuple[str, str], ...]
    source_log_head: str


@dataclass(frozen=True)
class OriginIndexSnapshot:
    life_id: str
    epoch: int
    source_log_head: str
    current_cycle: int
    last_event_ordinal: int
    indexed_events: tuple[IndexedOriginEvent, ...]
    landmarks: tuple[LandmarkRecord, ...]
    snapshot_sha256: str


class OriginIndex:
    """Incremental self-relative index with no process-object identities.

    Designation is declared by committed event context:

    * ``origin_index_action=DESIGNATE_IMMEDIATE`` designates that same event.
    * ``origin_index_action=DESIGNATE_DEFERRED`` requires
      ``origin_index_target_event_id`` and treats the designation event as a
      control record, not a recalled experience.
    * ``origin_index_include`` may explicitly suppress a normal event.  It
      must be false (or absent) for a deferred designation.
    """

    def __init__(self, life_id: str, epoch: int = 0) -> None:
        if not life_id:
            raise OriginContractError("LIFE_ID_REQUIRED")
        if type(epoch) is not int or epoch < 0:
            raise OriginContractError("ORIGIN_EPOCH_INVALID")
        self._life_id = life_id
        self._epoch = epoch
        self._source_log_head = SHA256_ZERO
        self._current_cycle = -1
        self._last_event_ordinal = -1
        self._indexed: dict[str, IndexedOriginEvent] = {}
        self._landmarks: dict[str, LandmarkRecord] = {}
        self._lock = RLock()

    @property
    def source_log_head(self) -> str:
        with self._lock:
            return self._source_log_head

    @property
    def current_cycle(self) -> int:
        with self._lock:
            return self._current_cycle

    def ingest(self, event: CommittedOriginEvent) -> None:
        """Project exactly one next committed ledger event."""
        if type(event) is not CommittedOriginEvent:
            raise OriginContractError("COMMITTED_EVENT_REQUIRED")
        with self._lock:
            self._validate_next_event(event)
            context = event.proposal.context
            action = context.get("origin_index_action")
            if action is not None and action not in _ACTIONS:
                raise OriginContractError("LANDMARK_ACTION_INVALID")
            include = context.get("origin_index_include", action != DESIGNATE_DEFERRED)
            if type(include) is not bool:
                raise OriginContractError("ORIGIN_INDEX_INCLUDE_INVALID")
            if action == DESIGNATE_DEFERRED and include:
                raise OriginContractError("DEFERRED_DESIGNATION_MUST_NOT_INDEX")

            indexed = IndexedOriginEvent(
                event_id=event.event_id,
                cycle=event.stamp.cycle,
                event_ordinal=event.stamp.event_ordinal,
                source_kind=str(context.get("source_kind", event.proposal.kind)),
                content_sha256=sha256_bytes(event.proposal.content),
            )
            if include:
                self._indexed[event.event_id] = indexed

            if action == DESIGNATE_IMMEDIATE:
                target = context.get("origin_index_target_event_id", event.event_id)
                if target != event.event_id or not include:
                    raise OriginContractError("IMMEDIATE_LANDMARK_TARGET_INVALID")
                self._register_landmark(
                    target,
                    event,
                    mode="IMMEDIATE",
                )
            elif action == DESIGNATE_DEFERRED:
                target = context.get("origin_index_target_event_id")
                if type(target) is not str or target not in self._indexed:
                    raise OriginContractError("DEFERRED_LANDMARK_TARGET_INVALID")
                if self._indexed[target].cycle >= event.stamp.cycle:
                    raise OriginContractError("DEFERRED_LANDMARK_CYCLE_INVALID")
                self._register_landmark(
                    target,
                    event,
                    mode="DEFERRED",
                )

            self._source_log_head = event.event_sha256
            self._current_cycle = event.stamp.cycle
            self._last_event_ordinal = event.stamp.event_ordinal

    def coordinate(
        self, event_id: str, *, source_log_head: str
    ) -> OriginCoordinate:
        with self._lock:
            self._require_current_head(source_log_head)
            event = self._require_event(event_id)
            relations = tuple(
                (
                    landmark.landmark_event_id,
                    _relation(event.cycle, landmark.designated_at_cycle),
                )
                for landmark in self._ordered_landmarks()
            )
            return OriginCoordinate(
                event_id=event.event_id,
                encoding_cycle=event.cycle,
                current_cycle=self._current_cycle,
                cycle_relative_distance=self._current_cycle - event.cycle,
                landmark_relations=relations,
                source_log_head=self._source_log_head,
            )

    def relation(
        self,
        event_id: str,
        landmark_event_id: str,
        *,
        source_log_head: str,
    ) -> str:
        with self._lock:
            self._require_current_head(source_log_head)
            event = self._require_event(event_id)
            landmark = self._require_landmark(landmark_event_id)
            return _relation(event.cycle, landmark.designated_at_cycle)

    def query_landmark_relative(
        self,
        landmark_event_id: str,
        relation: str,
        *,
        limit: int,
        source_log_head: str,
    ) -> tuple[str, ...]:
        with self._lock:
            self._require_current_head(source_log_head)
            if relation not in RELATIONS:
                raise OriginContractError("LANDMARK_RELATION_INVALID")
            if type(limit) is not int or limit < 1:
                raise OriginContractError("ORIGIN_QUERY_LIMIT_INVALID")
            landmark = self._require_landmark(landmark_event_id)
            matches = [
                event
                for event in self._indexed.values()
                if _relation(event.cycle, landmark.designated_at_cycle) == relation
            ]
            matches.sort(key=lambda row: (row.cycle, row.event_ordinal), reverse=True)
            return tuple(row.event_id for row in matches[:limit])

    def query_cycle_relative(
        self,
        minimum_distance: int,
        maximum_distance: int,
        *,
        limit: int,
        source_log_head: str,
    ) -> tuple[str, ...]:
        with self._lock:
            self._require_current_head(source_log_head)
            if (
                type(minimum_distance) is not int
                or type(maximum_distance) is not int
                or minimum_distance < 0
                or maximum_distance < minimum_distance
            ):
                raise OriginContractError("CYCLE_DISTANCE_WINDOW_INVALID")
            if type(limit) is not int or limit < 1:
                raise OriginContractError("ORIGIN_QUERY_LIMIT_INVALID")
            matches = [
                event
                for event in self._indexed.values()
                if minimum_distance
                <= self._current_cycle - event.cycle
                <= maximum_distance
            ]
            matches.sort(key=lambda row: (row.cycle, row.event_ordinal), reverse=True)
            return tuple(row.event_id for row in matches[:limit])

    def snapshot(self) -> OriginIndexSnapshot:
        with self._lock:
            values = {
                "life_id": self._life_id,
                "epoch": self._epoch,
                "source_log_head": self._source_log_head,
                "current_cycle": self._current_cycle,
                "last_event_ordinal": self._last_event_ordinal,
                "indexed_events": tuple(
                    sorted(self._indexed.values(), key=lambda row: row.event_ordinal)
                ),
                "landmarks": self._ordered_landmarks(),
            }
            return OriginIndexSnapshot(
                **values, snapshot_sha256=sha256_canonical(values)
            )

    def verify(self, events: Iterable[CommittedOriginEvent]) -> None:
        reproduced = self.replay(self._life_id, events, epoch=self._epoch)
        if to_primitive(reproduced.snapshot()) != to_primitive(self.snapshot()):
            raise OriginContractError("ORIGIN_INDEX_REPLAY_MISMATCH")

    @classmethod
    def replay(
        cls,
        life_id: str,
        events: Iterable[CommittedOriginEvent],
        *,
        epoch: int = 0,
    ) -> "OriginIndex":
        index = cls(life_id, epoch)
        for event in events:
            index.ingest(event)
        return index

    def _validate_next_event(self, event: CommittedOriginEvent) -> None:
        if event.stamp.life_id != self._life_id or event.stamp.epoch != self._epoch:
            raise OriginContractError("ORIGIN_IDENTITY_MISMATCH")
        if event.prior_event_sha256 != self._source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")
        if event.stamp.event_ordinal != self._last_event_ordinal + 1:
            raise OriginContractError("EVENT_ORDINAL_DISCONTINUITY")
        if event.stamp.cycle not in (self._current_cycle, self._current_cycle + 1):
            raise OriginContractError("ORIGIN_CYCLE_DISCONTINUITY")
        if self._last_event_ordinal == -1 and event.stamp.cycle != 0:
            raise OriginContractError("ORIGIN_INITIAL_CYCLE_INVALID")
        expected_id = (
            f"{self._life_id}:{self._epoch}:{event.stamp.event_ordinal:020d}"
        )
        if event.event_id != expected_id:
            raise OriginContractError("EVENT_ID_MISMATCH")
        identity = {
            "event_id": event.event_id,
            "life_id": self._life_id,
            "epoch": self._epoch,
            "cycle": event.stamp.cycle,
            "event_ordinal": event.stamp.event_ordinal,
            "prior_event_sha256": event.prior_event_sha256,
            "proposal": event.proposal,
        }
        expected_digest = sha256_canonical(identity)
        if (
            event.event_sha256 != expected_digest
            or event.stamp.log_head != expected_digest
        ):
            raise OriginContractError("EVENT_DIGEST_MISMATCH")

    def _register_landmark(
        self, target: str, event: CommittedOriginEvent, *, mode: str
    ) -> None:
        if target in self._landmarks:
            raise OriginContractError("LANDMARK_ALREADY_DESIGNATED")
        self._landmarks[target] = LandmarkRecord(
            landmark_event_id=target,
            designation_event_id=event.event_id,
            mode=mode,
            designated_at_cycle=event.stamp.cycle,
            designation_event_ordinal=event.stamp.event_ordinal,
        )

    def _ordered_landmarks(self) -> tuple[LandmarkRecord, ...]:
        return tuple(
            sorted(
                self._landmarks.values(),
                key=lambda row: row.designation_event_ordinal,
            )
        )

    def _require_current_head(self, source_log_head: str) -> None:
        require_sha256(source_log_head, "VIEW_SOURCE_HEAD_INVALID")
        if source_log_head != self._source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")

    def _require_event(self, event_id: str) -> IndexedOriginEvent:
        event = self._indexed.get(event_id)
        if event is None:
            raise OriginContractError("ORIGIN_EVENT_NOT_FOUND")
        return event

    def _require_landmark(self, event_id: str) -> LandmarkRecord:
        landmark = self._landmarks.get(event_id)
        if landmark is None:
            raise OriginContractError("LANDMARK_NOT_FOUND")
        return landmark


def _relation(event_cycle: int, designated_at_cycle: int) -> str:
    if event_cycle < designated_at_cycle:
        return BEFORE
    if event_cycle == designated_at_cycle:
        return AT
    return AFTER
