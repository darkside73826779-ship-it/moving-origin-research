"""Canonical value objects shared by every situated-origin subsystem."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
from typing import Any, Mapping


SHA256_ZERO = "0" * 64


class OriginContractError(ValueError):
    """Fail-closed contract error with a stable public code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class Unavailable:
    reason: str

    def __post_init__(self) -> None:
        if not self.reason:
            raise OriginContractError("UNAVAILABLE_REASON_REQUIRED")


@dataclass(frozen=True)
class ProvenanceHandle:
    source_kind: str
    source_id: str
    source_sha256: str

    def __post_init__(self) -> None:
        if not self.source_kind or not self.source_id:
            raise OriginContractError("PROVENANCE_SOURCE_REQUIRED")
        require_sha256(self.source_sha256, "PROVENANCE_DIGEST_INVALID")


@dataclass(frozen=True)
class OriginStamp:
    life_id: str
    epoch: int
    cycle: int
    event_ordinal: int
    log_head: str

    def __post_init__(self) -> None:
        if not self.life_id:
            raise OriginContractError("LIFE_ID_REQUIRED")
        if type(self.epoch) is not int or self.epoch < 0:
            raise OriginContractError("ORIGIN_EPOCH_INVALID")
        if type(self.cycle) is not int or self.cycle < -1:
            raise OriginContractError("ORIGIN_CYCLE_INVALID")
        if type(self.event_ordinal) is not int or self.event_ordinal < -1:
            raise OriginContractError("EVENT_ORDINAL_INVALID")
        require_sha256(self.log_head, "LOG_HEAD_INVALID")


@dataclass(frozen=True)
class EnvironmentFrame:
    runtime_place: str | Unavailable
    interaction_place: str | Unavailable
    world_place: str | Unavailable
    active_task: str | Unavailable


@dataclass(frozen=True)
class SituatedOriginFrame:
    stamp: OriginStamp
    environment: EnvironmentFrame
    active_episode: str
    retention: tuple[float, ...]
    protention: tuple[float, ...] | Unavailable
    fact_graph_head: str
    access_ledger_head: str
    homeostasis: Mapping[str, float] | Unavailable
    experience_strip: Mapping[str, Any] | Unavailable
    provenance_root: str
    frame_sha256: str

    def __post_init__(self) -> None:
        if not self.active_episode:
            raise OriginContractError("ACTIVE_EPISODE_REQUIRED")
        if not self.retention:
            raise OriginContractError("RETENTION_REQUIRED")
        for value in self.retention:
            if type(value) not in (int, float):
                raise OriginContractError("RETENTION_VALUE_INVALID")
        for code, value in (
            ("FACT_GRAPH_HEAD_INVALID", self.fact_graph_head),
            ("ACCESS_LEDGER_HEAD_INVALID", self.access_ledger_head),
            ("PROVENANCE_ROOT_INVALID", self.provenance_root),
            ("FRAME_DIGEST_INVALID", self.frame_sha256),
        ):
            require_sha256(value, code)


@dataclass(frozen=True)
class OriginEventProposal:
    kind: str
    content: bytes
    source: ProvenanceHandle
    context: Mapping[str, Any]
    valid_from: int | None = None
    valid_until: int | None = None
    supersedes: str | None = None
    observed_environment: str | Unavailable = Unavailable("NOT_OBSERVED")
    observed_space: str | Unavailable = Unavailable("NOT_OBSERVED")

    def __post_init__(self) -> None:
        if not self.kind:
            raise OriginContractError("EVENT_KIND_REQUIRED")
        if type(self.content) is not bytes:
            raise OriginContractError("EVENT_CONTENT_BYTES_REQUIRED")
        if self.valid_from is not None and type(self.valid_from) is not int:
            raise OriginContractError("VALID_FROM_INVALID")
        if self.valid_until is not None and type(self.valid_until) is not int:
            raise OriginContractError("VALID_UNTIL_INVALID")
        if (
            self.valid_from is not None
            and self.valid_until is not None
            and self.valid_until < self.valid_from
        ):
            raise OriginContractError("FACT_INTERVAL_INVALID")


@dataclass(frozen=True)
class CommittedOriginEvent:
    event_id: str
    stamp: OriginStamp
    proposal: OriginEventProposal
    prior_event_sha256: str
    event_sha256: str

    def __post_init__(self) -> None:
        if not self.event_id:
            raise OriginContractError("EVENT_ID_REQUIRED")
        require_sha256(self.prior_event_sha256, "PRIOR_EVENT_DIGEST_INVALID")
        require_sha256(self.event_sha256, "EVENT_DIGEST_INVALID")
        if self.stamp.log_head != self.event_sha256:
            raise OriginContractError("EVENT_LOG_HEAD_MISMATCH")


@dataclass(frozen=True)
class OriginDistance:
    cycle_distance: int
    landmark_relations: tuple[str, ...]
    acquisition_chain_distance: int
    world_validity_relation: str
    task_phase_distance: int | Unavailable
    environment_relation: str | Unavailable
    state_divergence: float | Unavailable


@dataclass(frozen=True)
class MemoryQuery:
    text: str
    landmark_ids: tuple[str, ...] = ()
    include_stale: bool = False
    limit: int = 4

    def __post_init__(self) -> None:
        if not self.text:
            raise OriginContractError("MEMORY_QUERY_REQUIRED")
        if type(self.limit) is not int or self.limit < 1:
            raise OriginContractError("MEMORY_QUERY_LIMIT_INVALID")


@dataclass(frozen=True)
class GroundedMemory:
    event_id: str
    content: bytes
    source: ProvenanceHandle
    encoding_stamp: OriginStamp
    current_distance: OriginDistance
    context: Mapping[str, Any]
    world_valid: bool
    superseded_by: str | None
    access_score: float


@dataclass(frozen=True)
class RecallBundle:
    records: tuple[GroundedMemory, ...]
    selected_event_ids: tuple[str, ...]
    query_origin: SituatedOriginFrame
    confidence: float | None
    abstention: bool
    source_log_head: str
    selection_receipt_sha256: str

    def __post_init__(self) -> None:
        require_sha256(self.source_log_head, "RECALL_SOURCE_HEAD_INVALID")
        require_sha256(self.selection_receipt_sha256, "RECALL_RECEIPT_INVALID")
        if self.source_log_head != self.query_origin.stamp.log_head:
            raise OriginContractError("VIEW_HEAD_STALE")
        if tuple(item.event_id for item in self.records) != self.selected_event_ids:
            raise OriginContractError("RECALL_SELECTION_MISMATCH")


@dataclass(frozen=True)
class SituatedContextPacket:
    shared_question_sha256: str
    frame_sha256: str
    recall_receipt_sha256: str
    rendered_text: str
    rendered_sha256: str
    selected_event_ids: tuple[str, ...]
    source_log_head: str

    def __post_init__(self) -> None:
        for code, value in (
            ("SHARED_QUESTION_DIGEST_INVALID", self.shared_question_sha256),
            ("CONTEXT_FRAME_DIGEST_INVALID", self.frame_sha256),
            ("CONTEXT_RECALL_DIGEST_INVALID", self.recall_receipt_sha256),
            ("CONTEXT_RENDER_DIGEST_INVALID", self.rendered_sha256),
            ("CONTEXT_SOURCE_HEAD_INVALID", self.source_log_head),
        ):
            require_sha256(value, code)


@dataclass(frozen=True)
class ClaimReceipt:
    status: str
    claim_kind: str
    supporting_event_ids: tuple[str, ...]
    reason: str | None
    receipt_sha256: str

    def __post_init__(self) -> None:
        if self.status not in ("GROUNDED", "UNSUPPORTED"):
            raise OriginContractError("CLAIM_STATUS_INVALID")
        if self.status == "GROUNDED" and not self.supporting_event_ids:
            raise OriginContractError("CLAIM_SUPPORT_REQUIRED")
        if self.status == "UNSUPPORTED" and not self.reason:
            raise OriginContractError("CLAIM_REJECTION_REASON_REQUIRED")
        require_sha256(self.receipt_sha256, "CLAIM_RECEIPT_INVALID")


def require_sha256(value: str, code: str) -> None:
    if (
        type(value) is not str
        or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise OriginContractError(code)


def to_primitive(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_primitive(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): to_primitive(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))}
    if isinstance(value, (tuple, list)):
        return [to_primitive(item) for item in value]
    if isinstance(value, bytes):
        return {"encoding": "utf-8-or-hex", "value": _bytes_text(value)}
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        to_primitive(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_canonical(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def _bytes_text(value: bytes) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError:
        return value.hex()
