"""Origin-distance recall that returns useful memory content and provenance."""

from __future__ import annotations

from .access import AccessLedger
from .contracts import (
    GroundedMemory, MemoryQuery, OriginContractError, OriginDistance, RecallBundle,
    SituatedOriginFrame, Unavailable, sha256_canonical,
)
from .episodes import EpisodicStore
from .facts import BiTemporalFactGraph
from .origin_index import OriginIndex


class OriginDistanceRecall:
    def __init__(
        self,
        access: AccessLedger,
        facts: BiTemporalFactGraph,
        episodes: EpisodicStore,
        origin_index: OriginIndex | None = None,
    ) -> None:
        self.access, self.facts, self.episodes = access, facts, episodes
        self.origin_index = origin_index

    def recall(
        self,
        query: MemoryQuery,
        frame: SituatedOriginFrame,
        event_ids: tuple[str, ...],
        source_log_head: str,
    ) -> RecallBundle:
        if source_log_head != frame.stamp.log_head:
            raise OriginContractError("VIEW_HEAD_STALE")
        if self.access.cycle != frame.stamp.cycle or self.facts.cycle != frame.stamp.cycle:
            raise OriginContractError("SUBSYSTEM_CLOCK_MISMATCH")
        self.access.require_source_head(source_log_head)
        self.facts.require_source_head(source_log_head)
        if self.episodes.source_log_head != source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")
        if self.origin_index is not None and self.origin_index.source_log_head != source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")
        terms = tuple(term.lower() for term in query.text.split() if term.strip())
        indexed_event_ids = (
            {item.event_id for item in self.origin_index.snapshot().indexed_events}
            if self.origin_index is not None else None
        )
        candidates: list[tuple[int, float, float, GroundedMemory]] = []
        for event_id in event_ids:
            if indexed_event_ids is not None and event_id not in indexed_event_ids:
                continue
            episode = self.episodes.query(event_id, source_log_head)
            fact = self.facts.for_event(event_id)
            valid = fact is None or self.facts.is_world_valid(fact.fact_id, frame.stamp.cycle)
            superseded = self.facts.superseded_by(fact.fact_id) if fact is not None else None
            if not query.include_stale and (not valid or superseded is not None):
                continue
            text = episode.content.decode("utf-8", errors="replace")
            lexical = sum(1 for term in terms if term in text.lower())
            score = self.access.priority(event_id, frame.stamp.cycle)
            if self.origin_index is None:
                cycle_distance = frame.stamp.cycle - episode.encoding_stamp.cycle
                relations = tuple(
                    str(episode.self_position_at_encoding.get("landmark_relative", {}).get(item, "UNKNOWN"))
                    for item in query.landmark_ids
                )
            else:
                coordinate = self.origin_index.coordinate(event_id, source_log_head=source_log_head)
                cycle_distance = coordinate.cycle_relative_distance
                relations = tuple(
                    self.origin_index.relation(
                        event_id, item, source_log_head=source_log_head
                    )
                    for item in query.landmark_ids
                )
            encoded_state = episode.self_position_at_encoding.get("thick_present_state")
            if (
                not isinstance(encoded_state, (tuple, list))
                or len(encoded_state) != len(frame.retention)
            ):
                divergence = 0.0
            else:
                divergence = round(
                    sum(abs(float(left) - float(right)) for left, right in zip(encoded_state, frame.retention))
                    / max(1, len(frame.retention)),
                    12,
                )
            distance = OriginDistance(
                cycle_distance=cycle_distance,
                landmark_relations=relations,
                acquisition_chain_distance=(len(self.facts.walk(fact.fact_id)) - 1 if fact is not None else 0),
                world_validity_relation="CURRENT" if valid and superseded is None else "STALE",
                task_phase_distance=Unavailable("TASK_PHASE_NOT_BOUND"),
                environment_relation=Unavailable("ENVIRONMENT_NOT_BOUND"),
                state_divergence=divergence,
            )
            memory = GroundedMemory(
                event_id=event_id, content=episode.content, source=episode.source,
                encoding_stamp=episode.encoding_stamp, current_distance=distance,
                context=episode.context, world_valid=valid, superseded_by=superseded,
                access_score=score,
            )
            candidates.append((lexical, divergence, score, memory))
        candidates.sort(key=lambda row: (-row[0], row[1], -row[2], row[3].event_id))
        records = tuple(row[3] for row in candidates[: query.limit])
        selected = tuple(item.event_id for item in records)
        receipt = sha256_canonical({
            "query": query, "frame_sha256": frame.frame_sha256,
            "selected_event_ids": selected, "source_log_head": source_log_head,
        })
        return RecallBundle(
            records=records, selected_event_ids=selected, query_origin=frame,
            confidence=None, abstention=not records, source_log_head=source_log_head,
            selection_receipt_sha256=receipt,
        )
