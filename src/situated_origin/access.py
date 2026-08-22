"""Persistent same-clock access priority for situated-origin memories."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .contracts import OriginContractError, SHA256_ZERO, require_sha256, sha256_canonical


@dataclass(frozen=True)
class AccessRecord:
    event_id: str
    encoded_cycle: int
    rehearsal_count: int
    last_access_cycle: int | None


class AccessLedger:
    """L1 priority ledger whose clock is supplied by the origin kernel."""

    def __init__(self, decay: float = 0.001, rehearsal_weight: float = 0.5) -> None:
        if decay < 0 or rehearsal_weight < 0:
            raise OriginContractError("ACCESS_PARAMETER_INVALID")
        self.decay = float(decay)
        self.rehearsal_weight = float(rehearsal_weight)
        self._cycle = -1
        self._records: dict[str, AccessRecord] = {}
        self._head = SHA256_ZERO
        self._source_log_head = SHA256_ZERO

    @property
    def cycle(self) -> int:
        return self._cycle

    @property
    def head(self) -> str:
        return self._head

    @property
    def source_log_head(self) -> str:
        return self._source_log_head

    def advance_to(self, cycle: int, source_log_head: str) -> None:
        if type(cycle) is not int or cycle < self._cycle:
            raise OriginContractError("ACCESS_CLOCK_INVALID")
        require_sha256(source_log_head, "ACCESS_SOURCE_HEAD_INVALID")
        self._cycle = cycle
        self._source_log_head = source_log_head

    def register(self, event_id: str, encoded_cycle: int) -> None:
        if not event_id or type(encoded_cycle) is not int or encoded_cycle < 0:
            raise OriginContractError("ACCESS_RECORD_INVALID")
        if encoded_cycle > self._cycle:
            raise OriginContractError("ACCESS_FUTURE_EVENT")
        if event_id in self._records:
            raise OriginContractError("ACCESS_EVENT_DUPLICATE")
        self._records[event_id] = AccessRecord(event_id, encoded_cycle, 0, None)
        self._rehash("register", event_id)

    def rehearse(self, event_id: str, cycle: int) -> None:
        self._require_same_clock(cycle)
        record = self._require(event_id)
        self._records[event_id] = AccessRecord(
            event_id, record.encoded_cycle, record.rehearsal_count + 1, cycle
        )
        self._rehash("rehearse", event_id)

    def priority(self, event_id: str, cycle: int) -> float:
        self._require_same_clock(cycle)
        record = self._require(event_id)
        age = cycle - record.encoded_cycle
        return math.exp(-self.decay * age) * (
            1.0 + self.rehearsal_weight * math.log1p(record.rehearsal_count)
        )

    def require_source_head(self, source_log_head: str) -> None:
        if source_log_head != self._source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")

    def rank(self, event_ids: tuple[str, ...], cycle: int) -> tuple[str, ...]:
        self._require_same_clock(cycle)
        return tuple(sorted(event_ids, key=lambda item: (-self.priority(item, cycle), item)))

    def snapshot(self) -> tuple[AccessRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))

    def _require(self, event_id: str) -> AccessRecord:
        try:
            return self._records[event_id]
        except KeyError as exc:
            raise OriginContractError("ACCESS_EVENT_UNKNOWN") from exc

    def _require_same_clock(self, cycle: int) -> None:
        if type(cycle) is not int or cycle != self._cycle:
            raise OriginContractError("ACCESS_CLOCK_MISMATCH")

    def _rehash(self, operation: str, event_id: str) -> None:
        self._head = sha256_canonical({
            "prior": self._head,
            "operation": operation,
            "event_id": event_id,
            "cycle": self._cycle,
            "records": self.snapshot(),
        })
