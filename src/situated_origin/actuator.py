"""Ground-truth-free compilation of recalled memory into candidate context."""

from __future__ import annotations

from .contracts import (
    OriginContractError, RecallBundle, SituatedContextPacket, SituatedOriginFrame,
    sha256_bytes,
)


class CandidateContextActuator:
    def compile(
        self, shared_question: bytes, frame: SituatedOriginFrame, recall: RecallBundle
    ) -> SituatedContextPacket:
        if type(shared_question) is not bytes or not shared_question:
            raise OriginContractError("SHARED_QUESTION_REQUIRED")
        if recall.query_origin.frame_sha256 != frame.frame_sha256:
            raise OriginContractError("CONTEXT_FRAME_MISMATCH")
        if recall.source_log_head != frame.stamp.log_head:
            raise OriginContractError("VIEW_HEAD_STALE")
        rows = ["SITUATED_ORIGIN_MEMORY_V1"]
        for memory in recall.records:
            content = memory.content.decode("utf-8", errors="replace")
            rows.extend((
                f"event_id={memory.event_id}",
                f"content={content}",
                f"cycle_distance={memory.current_distance.cycle_distance}",
                f"state_divergence={memory.current_distance.state_divergence}",
                f"landmark_relations={','.join(memory.current_distance.landmark_relations)}",
                f"world_valid={str(memory.world_valid).lower()}",
                f"source={memory.source.source_kind}:{memory.source.source_id}:{memory.source.source_sha256}",
            ))
        if not recall.records:
            rows.append("abstain=true")
        rendered = "\n".join(rows)
        return SituatedContextPacket(
            shared_question_sha256=sha256_bytes(shared_question),
            frame_sha256=frame.frame_sha256,
            recall_receipt_sha256=recall.selection_receipt_sha256,
            rendered_text=rendered,
            rendered_sha256=sha256_bytes(rendered.encode("utf-8")),
            selected_event_ids=recall.selected_event_ids,
            source_log_head=recall.source_log_head,
        )
