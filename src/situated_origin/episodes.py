"""Public provenance-complete episodic ingestion, query, and serialization."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from .contracts import CommittedOriginEvent, OriginContractError, OriginStamp, ProvenanceHandle, canonical_bytes


@dataclass(frozen=True)
class EpisodeRecord:
    event_id: str
    content: bytes
    source: ProvenanceHandle
    encoding_stamp: OriginStamp
    prior_event_sha256: str
    event_sha256: str
    context: Mapping[str, Any]
    self_position_at_encoding: Mapping[str, Any]


class EpisodicStore:
    def __init__(self) -> None:
        self._records: dict[str, EpisodeRecord] = {}
        self._source_log_head = "0" * 64

    @property
    def source_log_head(self) -> str:
        return self._source_log_head

    def write(self, event: CommittedOriginEvent, self_position: Mapping[str, Any]) -> EpisodeRecord:
        if event.event_id in self._records:
            raise OriginContractError("EPISODE_DUPLICATE")
        if event.prior_event_sha256 != self._source_log_head:
            raise OriginContractError("EPISODE_SOURCE_CHAIN_INVALID")
        record = EpisodeRecord(
            event_id=event.event_id,
            content=event.proposal.content,
            source=event.proposal.source,
            encoding_stamp=event.stamp,
            prior_event_sha256=event.prior_event_sha256,
            event_sha256=event.event_sha256,
            context=dict(event.proposal.context),
            self_position_at_encoding=dict(self_position),
        )
        self._records[event.event_id] = record
        self._source_log_head = event.event_sha256
        return record

    def query(self, event_id: str, source_log_head: str) -> EpisodeRecord:
        if source_log_head != self._source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")
        try:
            return self._records[event_id]
        except KeyError as exc:
            raise OriginContractError("EPISODE_NOT_FOUND") from exc

    def to_bytes(self, record: EpisodeRecord) -> bytes:
        obj = {
            "event_id": record.event_id, "content_hex": record.content.hex(),
            "source": record.source, "encoding_stamp": record.encoding_stamp,
            "prior_event_sha256": record.prior_event_sha256, "event_sha256": record.event_sha256,
            "context": record.context, "self_position_at_encoding": record.self_position_at_encoding,
        }
        return canonical_bytes(obj)

    def from_bytes(self, data: bytes) -> EpisodeRecord:
        try:
            obj = json.loads(data.decode("utf-8"))
            content = bytes.fromhex(obj["content_hex"])
            source = ProvenanceHandle(**obj["source"])
            return EpisodeRecord(
                event_id=obj["event_id"], content=content, source=source,
                encoding_stamp=OriginStamp(**obj["encoding_stamp"]),
                prior_event_sha256=obj["prior_event_sha256"], event_sha256=obj["event_sha256"],
                context=obj["context"], self_position_at_encoding=obj["self_position_at_encoding"],
            )
        except (KeyError, TypeError, ValueError, UnicodeError) as exc:
            raise OriginContractError("EPISODE_SERIALIZATION_INVALID") from exc
