"""Focused tests for the model-neutral soft-prefix experience strip."""

from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest

from src.situated_origin.contracts import (
    MemoryQuery,
    OriginEventProposal,
    ProvenanceHandle,
    canonical_bytes,
    sha256_bytes,
)
from src.situated_origin.experience import (
    ExperiencePort,
    ExperiencePortError,
    ExperienceWrite,
)
from src.situated_origin.kernel import SituatedOriginKernel
from src.situated_origin.soft_prefix_strip import (
    OpaqueTraceUpdate,
    SoftPrefixExperienceStrip,
)


def digest(label: str) -> str:
    return sha256_bytes(label.encode("utf-8"))


class TupleCodec:
    identity_sha256 = digest("focused-json-tuple-codec-v1")

    def to_bytes(self, value: object) -> bytes:
        if not isinstance(value, tuple):
            raise TypeError("tuple required")
        return json.dumps(
            list(value), sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")

    def from_bytes(self, data: bytes) -> object:
        value = json.loads(data.decode("utf-8"))
        if not isinstance(value, list):
            raise TypeError("list encoding required")
        return tuple(value)


class DeterministicEncoder:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, request: ExperienceWrite) -> OpaqueTraceUpdate:
        self.calls += 1
        return OpaqueTraceUpdate(
            value=(
                len(request.content),
                float(request.prediction_error),
                request.origin.cycle,
            ),
            update_norm=Decimal("0.25"),
            update_budget=Decimal("1"),
        )


def proposal(label: str) -> OriginEventProposal:
    return OriginEventProposal(
        kind="EXPERIENCE",
        content=label.encode("utf-8"),
        source=ProvenanceHandle(
            "focused-test", label, digest(f"source:{label}")
        ),
        context={"label": label, "ordinal_hint": int(label[1:])},
    )


def advance(kernel: SituatedOriginKernel, label: str):
    return kernel.advance_origin(proposal(label), expected_head=kernel.head)


def make_strip(
    encoder: DeterministicEncoder,
    *,
    capacity: int = 4,
    decay_factor: Decimal = Decimal("0.5"),
) -> SoftPrefixExperienceStrip:
    return SoftPrefixExperienceStrip(
        "soft-prefix-life",
        capacity=capacity,
        trace_encoder=encoder,
        codec=TupleCodec(),
        actuator_identity_sha256=digest("focused-soft-prefix-actuator-v1"),
        decay_factor=decay_factor,
        max_trace_bytes=256,
    )


class SoftPrefixExperienceStripTests(unittest.TestCase):
    def test_committed_event_binding_exact_bytes_and_opaque_materialization(self) -> None:
        kernel = SituatedOriginKernel("soft-prefix-life")
        encoder = DeterministicEncoder()
        strip = make_strip(encoder)
        event0 = advance(kernel, "e0")

        record = strip.append_committed(
            event0, importance=4, prediction_error=0.25
        )

        self.assertIsInstance(strip, ExperiencePort)
        self.assertEqual(record.event_id, event0.event_id)
        self.assertEqual(record.event_sha256, event0.event_sha256)
        self.assertEqual(record.prior_event_sha256, event0.prior_event_sha256)
        self.assertEqual(record.source, event0.proposal.source)
        self.assertEqual(record.source_event_bytes, canonical_bytes(event0))
        self.assertEqual(record.source_event_sha256, sha256_bytes(canonical_bytes(event0)))
        self.assertEqual(record.trace_sha256, sha256_bytes(record.trace_bytes))
        self.assertEqual(record.codec_identity_sha256, TupleCodec.identity_sha256)
        self.assertEqual(
            strip.materialize_trace(
                record.experience_id, source_log_head=kernel.head
            ),
            (len(event0.proposal.content), 0.25, 0),
        )
        self.assertTrue(strip.compare_to_log(record.experience_id, event0).matches)

        event1 = advance(kernel, "e1")
        self.assertFalse(strip.compare_to_log(record.experience_id, event1).matches)
        tampered = replace(
            ExperienceWrite.from_committed_event(event1), content=b"not-ledger-content"
        )
        with self.assertRaisesRegex(
            ExperiencePortError, "E3_COMMITTED_EVENT_BINDING_MISMATCH"
        ):
            strip.write_experience(tampered)
        self.assertEqual(encoder.calls, 1)

    def test_decay_importance_supersession_event_lookup_and_bounded_tape(self) -> None:
        kernel = SituatedOriginKernel("soft-prefix-life")
        encoder = DeterministicEncoder()
        strip = make_strip(encoder, capacity=3)
        event0 = advance(kernel, "e0")
        record0 = strip.append_committed(event0, importance=8)
        event1 = advance(kernel, "e1")
        strip.append_committed(
            event1, importance=2, supersedes_event_id=event0.event_id
        )
        event2 = advance(kernel, "e2")
        strip.append_committed(event2, importance=1)

        current = kernel.current()
        live = strip.retrieve_by_origin_distance(
            MemoryQuery("experience", limit=4), current, max_distance=99
        )
        self.assertEqual(live.selected_event_ids, (event2.event_id, event1.event_id))
        with_stale = strip.retrieve_by_origin_distance(
            MemoryQuery("experience", include_stale=True, limit=4),
            current,
            max_distance=99,
        )
        self.assertEqual(with_stale.selected_event_ids[0], event0.event_id)
        self.assertEqual(
            with_stale.rankings[0].effective_importance, Decimal("2.00")
        )
        self.assertEqual(
            with_stale.receipt_sha256,
            strip.retrieve_by_origin_distance(
                MemoryQuery("experience", include_stale=True, limit=4),
                current,
                max_distance=99,
            ).receipt_sha256,
        )

        selected = strip.retrieve_by_event_ids(
            (event0.event_id, event2.event_id), current
        )
        self.assertEqual(selected.selected_event_ids, (event2.event_id,))
        selected_stale = strip.retrieve_by_event_ids(
            (event0.event_id, event2.event_id),
            current,
            include_superseded=True,
        )
        self.assertEqual(selected_stale.selected_event_ids[0], event0.event_id)

        event3 = advance(kernel, "e3")
        strip.append_committed(event3, importance=1)
        self.assertEqual(len(strip.snapshot()), 3)
        self.assertNotIn(record0.experience_id, {row.experience_id for row in strip.snapshot()})
        after_overwrite = strip.retrieve_by_event_ids(
            (event0.event_id, event3.event_id),
            kernel.current(),
            include_superseded=True,
        )
        self.assertEqual(after_overwrite.selected_event_ids, (event3.event_id,))

    def test_replay_receipts_checkpoint_bytes_and_reload_are_identical(self) -> None:
        kernel = SituatedOriginKernel("soft-prefix-life")
        events = tuple(advance(kernel, f"e{index}") for index in range(3))
        first_encoder = DeterministicEncoder()
        first = make_strip(first_encoder)
        first_records = tuple(
            first.append_committed(
                event,
                importance=index + 1,
                prediction_error=index / 10,
            )
            for index, event in enumerate(events)
        )
        second = make_strip(DeterministicEncoder())
        second_records = tuple(
            second.append_committed(
                event,
                importance=index + 1,
                prediction_error=index / 10,
            )
            for index, event in enumerate(events)
        )
        self.assertEqual(
            tuple(row.experience_id for row in first_records),
            tuple(row.experience_id for row in second_records),
        )
        self.assertEqual(first.head, second.head)
        self.assertEqual(first.to_bytes(), second.to_bytes())

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "soft-prefix-checkpoint.json"
            saved = first.save(path)
            self.assertEqual(saved.checkpoint_sha256, sha256_bytes(path.read_bytes()))
            restored = SoftPrefixExperienceStrip.load(
                path,
                trace_encoder=DeterministicEncoder(),
                codec=TupleCodec(),
                actuator_identity_sha256=digest(
                    "focused-soft-prefix-actuator-v1"
                ),
                expected_checkpoint_sha256=saved.checkpoint_sha256,
            )
            self.assertEqual(restored.to_bytes(), path.read_bytes())
            self.assertEqual(restored.checkpoint_receipt(), saved)
            self.assertEqual(restored.snapshot(), first.snapshot())
            self.assertEqual(
                restored.materialize_trace(
                    first_records[1].experience_id,
                    source_log_head=kernel.head,
                ),
                first.materialize_trace(
                    first_records[1].experience_id,
                    source_log_head=kernel.head,
                ),
            )
            query = MemoryQuery("experience", include_stale=True, limit=4)
            self.assertEqual(
                restored.retrieve_by_origin_distance(
                    query, kernel.current(), 99
                ).receipt_sha256,
                first.retrieve_by_origin_distance(
                    query, kernel.current(), 99
                ).receipt_sha256,
            )

            envelope = json.loads(path.read_text(encoding="utf-8"))
            envelope["payload"]["records"][0]["trace_hex"] = "00"
            tampered = canonical_bytes(envelope)
            with self.assertRaisesRegex(
                ExperiencePortError, "E3_CHECKPOINT_STATE_MISMATCH"
            ):
                SoftPrefixExperienceStrip.from_bytes(
                    tampered,
                    trace_encoder=DeterministicEncoder(),
                    codec=TupleCodec(),
                    actuator_identity_sha256=digest(
                        "focused-soft-prefix-actuator-v1"
                    ),
                )

    def test_consolidation_releases_projection_but_not_ledger_history(self) -> None:
        kernel = SituatedOriginKernel("soft-prefix-life")
        strip = make_strip(DeterministicEncoder())
        events = []
        records = []
        for index in range(3):
            event = advance(kernel, f"e{index}")
            events.append(event)
            records.append(strip.append_committed(event, importance=index + 1))
        ledger_before = kernel.events()

        receipt = strip.consolidate(events[1].stamp)

        self.assertEqual(
            receipt.consolidated_ids,
            (records[0].experience_id, records[1].experience_id),
        )
        self.assertEqual(
            receipt.consolidated_event_ids,
            (events[0].event_id, events[1].event_id),
        )
        self.assertEqual(
            receipt.source_event_sha256s,
            (records[0].source_event_sha256, records[1].source_event_sha256),
        )
        self.assertEqual(receipt.resulting_strip_head, strip.head)
        self.assertEqual(
            tuple(row.event_id for row in strip.snapshot()), (events[2].event_id,)
        )
        self.assertEqual(kernel.events(), ledger_before)
        with self.assertRaisesRegex(ExperiencePortError, "E3_EXPERIENCE_NOT_FOUND"):
            strip.compare_to_log(records[0].experience_id, events[0])


if __name__ == "__main__":
    unittest.main()
