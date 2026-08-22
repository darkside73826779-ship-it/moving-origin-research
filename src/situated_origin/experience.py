"""Fail-closed port for the future E3 experience-strip subsystem.

The alpha assembly names the E3 boundary without pretending that an experience
backend exists.  ``UnboundExperiencePort`` therefore implements the complete
surface and rejects every operation with one stable error code.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, NoReturn, Protocol, runtime_checkable

from .contracts import (
    CommittedOriginEvent,
    MemoryQuery,
    OriginStamp,
    ProvenanceHandle,
    SituatedOriginFrame,
)


class ExperiencePortError(RuntimeError):
    """Fail-closed E3 boundary error with a stable public code."""

    def __init__(self, code: str = "E3_EXPERIENCE_BACKEND_UNBOUND") -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class ExperienceWrite:
    content: bytes
    source: ProvenanceHandle
    context: Mapping[str, Any]
    origin: OriginStamp
    committed_event: CommittedOriginEvent | None = None
    importance: int | float = 1
    prediction_error: int | float = 0
    supersedes_event_id: str | None = None

    @classmethod
    def from_committed_event(
        cls,
        event: CommittedOriginEvent,
        *,
        importance: int | float = 1,
        prediction_error: int | float = 0,
        supersedes_event_id: str | None = None,
    ) -> "ExperienceWrite":
        """Build a port request without weakening the committed-event binding.

        The duplicated public fields are retained for the existing port surface;
        concrete ports can compare them with ``committed_event`` and reject any
        altered projection.
        """

        return cls(
            content=bytes(event.proposal.content),
            source=event.proposal.source,
            context=copy.deepcopy(dict(event.proposal.context)),
            origin=event.stamp,
            committed_event=copy.deepcopy(event),
            importance=importance,
            prediction_error=prediction_error,
            supersedes_event_id=supersedes_event_id,
        )


@dataclass(frozen=True)
class ExperienceRecord:
    experience_id: str
    content: bytes
    source: ProvenanceHandle
    encoding_origin: OriginStamp
    context: Mapping[str, Any]


@dataclass(frozen=True)
class ExperienceAdvanceReceipt:
    prior_origin: OriginStamp
    current_origin: OriginStamp
    receipt_sha256: str


@dataclass(frozen=True)
class ExperienceRetrieval:
    records: tuple[ExperienceRecord, ...]
    query_origin: SituatedOriginFrame
    receipt_sha256: str


@dataclass(frozen=True)
class ExperienceConsolidationReceipt:
    through_origin: OriginStamp
    consolidated_ids: tuple[str, ...]
    receipt_sha256: str


@dataclass(frozen=True)
class ExperienceLogComparison:
    experience_id: str
    event_id: str
    matches: bool
    receipt_sha256: str


@runtime_checkable
class ExperiencePort(Protocol):
    def write_experience(self, request: ExperienceWrite) -> ExperienceRecord: ...

    def advance_origin(
        self, prior: OriginStamp, current: OriginStamp
    ) -> ExperienceAdvanceReceipt: ...

    def retrieve_by_origin_distance(
        self, query: MemoryQuery, origin: SituatedOriginFrame, max_distance: int
    ) -> ExperienceRetrieval: ...

    def consolidate(self, through: OriginStamp) -> ExperienceConsolidationReceipt: ...

    def compare_to_log(
        self, experience_id: str, event: CommittedOriginEvent
    ) -> ExperienceLogComparison: ...


class UnboundExperiencePort:
    """Typed placeholder that can never fabricate an E3 success."""

    @staticmethod
    def _unavailable() -> NoReturn:
        raise ExperiencePortError()

    def write_experience(self, request: ExperienceWrite) -> ExperienceRecord:
        del request
        self._unavailable()

    def advance_origin(
        self, prior: OriginStamp, current: OriginStamp
    ) -> ExperienceAdvanceReceipt:
        del prior, current
        self._unavailable()

    def retrieve_by_origin_distance(
        self, query: MemoryQuery, origin: SituatedOriginFrame, max_distance: int
    ) -> ExperienceRetrieval:
        del query, origin, max_distance
        self._unavailable()

    def consolidate(self, through: OriginStamp) -> ExperienceConsolidationReceipt:
        del through
        self._unavailable()

    def compare_to_log(
        self, experience_id: str, event: CommittedOriginEvent
    ) -> ExperienceLogComparison:
        del experience_id, event
        self._unavailable()


__all__ = [
    "ExperienceAdvanceReceipt",
    "ExperienceConsolidationReceipt",
    "ExperienceLogComparison",
    "ExperiencePort",
    "ExperiencePortError",
    "ExperienceRecord",
    "ExperienceRetrieval",
    "ExperienceWrite",
    "UnboundExperiencePort",
]
