"""Stable public bi-temporal fact and supersession graph."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import OriginContractError, SHA256_ZERO, require_sha256, sha256_canonical


@dataclass(frozen=True)
class FactRevision:
    fact_id: str
    event_id: str
    content: bytes
    acquired_cycle: int
    valid_from: int
    valid_until: int | None
    supersedes: str | None


class BiTemporalFactGraph:
    def __init__(self) -> None:
        self._cycle = -1
        self._facts: dict[str, FactRevision] = {}
        self._superseded_by: dict[str, str] = {}
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
            raise OriginContractError("FACT_CLOCK_INVALID")
        require_sha256(source_log_head, "FACT_SOURCE_HEAD_INVALID")
        self._cycle = cycle
        self._source_log_head = source_log_head

    def require_source_head(self, source_log_head: str) -> None:
        if source_log_head != self._source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")

    def append(self, revision: FactRevision) -> None:
        if not revision.fact_id or not revision.event_id or type(revision.content) is not bytes:
            raise OriginContractError("FACT_REVISION_INVALID")
        if revision.fact_id in self._facts:
            raise OriginContractError("FACT_ID_DUPLICATE")
        if revision.acquired_cycle != self._cycle:
            raise OriginContractError("FACT_CLOCK_MISMATCH")
        if revision.valid_until is not None and revision.valid_until < revision.valid_from:
            raise OriginContractError("FACT_INTERVAL_INVALID")
        if revision.supersedes is not None:
            if revision.supersedes not in self._facts or revision.supersedes in self._superseded_by:
                raise OriginContractError("FACT_SUPERSESSION_INVALID")
            self._superseded_by[revision.supersedes] = revision.fact_id
        self._facts[revision.fact_id] = revision
        self._head = sha256_canonical({"prior": self._head, "revision": revision})

    def get(self, fact_id: str) -> FactRevision:
        try:
            return self._facts[fact_id]
        except KeyError as exc:
            raise OriginContractError("FACT_UNKNOWN") from exc

    def is_world_valid(self, fact_id: str, cycle: int) -> bool:
        fact = self.get(fact_id)
        return fact.valid_from <= cycle and (fact.valid_until is None or cycle <= fact.valid_until)

    def is_current(self, fact_id: str, cycle: int) -> bool:
        return self.is_world_valid(fact_id, cycle) and fact_id not in self._superseded_by

    def current(self, cycle: int, include_stale: bool = False) -> tuple[FactRevision, ...]:
        rows = []
        for key in sorted(self._facts):
            if include_stale or self.is_current(key, cycle):
                rows.append(self._facts[key])
        return tuple(rows)

    def walk(self, fact_id: str) -> tuple[str, ...]:
        if fact_id not in self._facts:
            raise OriginContractError("FACT_UNKNOWN")
        rows, current = [fact_id], fact_id
        while current in self._superseded_by:
            current = self._superseded_by[current]
            rows.append(current)
        return tuple(rows)

    def superseded_by(self, fact_id: str) -> str | None:
        self.get(fact_id)
        return self._superseded_by.get(fact_id)

    def for_event(self, event_id: str) -> FactRevision | None:
        matches = [item for item in self._facts.values() if item.event_id == event_id]
        if len(matches) > 1:
            raise OriginContractError("FACT_EVENT_AMBIGUOUS")
        return matches[0] if matches else None
