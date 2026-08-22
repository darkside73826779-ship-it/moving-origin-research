"""Provenance guard for claims derived from recalled memories."""

from __future__ import annotations

from .contracts import ClaimReceipt, RecallBundle, sha256_canonical


class ProvenanceClaimGuard:
    def assess(
        self, claim_kind: str, supporting_event_ids: tuple[str, ...], recall: RecallBundle
    ) -> ClaimReceipt:
        selected = {item.event_id: item for item in recall.records}
        supported = bool(supporting_event_ids) and all(
            event_id in selected and selected[event_id].world_valid and selected[event_id].superseded_by is None
            for event_id in supporting_event_ids
        )
        status = "GROUNDED" if supported else "UNSUPPORTED"
        reason = None if supported else "PROVENANCE_SUPPORT_UNAVAILABLE"
        payload = {
            "status": status, "claim_kind": claim_kind,
            "supporting_event_ids": supporting_event_ids, "reason": reason,
            "recall_receipt_sha256": recall.selection_receipt_sha256,
        }
        return ClaimReceipt(status, claim_kind, supporting_event_ids, reason, sha256_canonical(payload))
