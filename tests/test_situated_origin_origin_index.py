"""Focused tests for the durable-ID situated-origin L4 projection."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import types
import unittest

from src.situated_origin.contracts import (
    OriginContractError,
    OriginEventProposal,
    ProvenanceHandle,
    SHA256_ZERO,
    canonical_bytes,
    sha256_bytes,
    to_primitive,
)
from src.situated_origin.kernel import SituatedOriginKernel
from src.situated_origin.origin_index import (
    AFTER,
    AT,
    BEFORE,
    DESIGNATE_DEFERRED,
    DESIGNATE_IMMEDIATE,
    OriginIndex,
)


def load_e1_mechanisms():
    """Load committed E1 classes without invoking its numerical experiment."""
    unavailable = lambda *_args, **_kwargs: (_ for _ in ()).throw(
        RuntimeError("E1_NUMERICAL_PATH_OUT_OF_SCOPE")
    )
    numpy_stub = types.ModuleType("numpy")
    scipy_stub = types.ModuleType("scipy")
    stats_stub = types.ModuleType("scipy.stats")
    numpy_stub.__getattr__ = lambda _name: unavailable  # type: ignore[attr-defined]
    stats_stub.pearsonr = unavailable
    scipy_stub.stats = stats_stub
    prior = {name: sys.modules.get(name) for name in ("numpy", "scipy", "scipy.stats")}
    sys.modules["numpy"] = numpy_stub
    sys.modules["scipy"] = scipy_stub
    sys.modules["scipy.stats"] = stats_stub
    try:
        path = Path(__file__).parents[1] / "src" / "e1_experiment.py"
        spec = importlib.util.spec_from_file_location(
            "situated_origin_e1_equivalence", path
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("E1_IMPORT_UNAVAILABLE")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, previous in prior.items():
            if previous is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous


e1 = load_e1_mechanisms()


def provenance() -> ProvenanceHandle:
    return ProvenanceHandle(
        "synthetic",
        "origin-index-focused-test",
        sha256_bytes(b"origin-index-focused-test"),
    )


def proposal(label: str, context: dict[str, object] | None = None) -> OriginEventProposal:
    return OriginEventProposal(
        kind="EXPERIENCE",
        content=label.encode("utf-8"),
        source=provenance(),
        context=dict(context or {}),
    )


def advance(
    kernel: SituatedOriginKernel,
    index: OriginIndex,
    label: str,
    context: dict[str, object] | None = None,
):
    event = kernel.advance_origin(proposal(label, context), expected_head=kernel.head)
    index.ingest(event)
    return event


def relation_from_e1(index: e1.EgocentricIndex, event, landmark) -> str:
    for relation in (e1.BEFORE_L, e1.AT_L, e1.AFTER_L):
        if index.query_membership(event, landmark, relation):
            return relation
    raise AssertionError("E1 relation missing")


class OriginIndexTests(unittest.TestCase):
    def test_cycle_distance_reresolves_and_stale_heads_reject(self) -> None:
        kernel = SituatedOriginKernel("life-index")
        index = OriginIndex("life-index")
        first = advance(kernel, index, "event-0")
        initial = index.coordinate(first.event_id, source_log_head=kernel.head)
        self.assertEqual(initial.encoding_cycle, 0)
        self.assertEqual(initial.current_cycle, 0)
        self.assertEqual(initial.cycle_relative_distance, 0)
        self.assertEqual(initial.source_log_head, kernel.head)

        stale = kernel.head
        advance(kernel, index, "event-1")
        shifted = index.coordinate(first.event_id, source_log_head=kernel.head)
        self.assertEqual(shifted.cycle_relative_distance, 1)
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            index.coordinate(first.event_id, source_log_head=stale)

    def test_immediate_deferred_relations_and_bounded_queries(self) -> None:
        kernel = SituatedOriginKernel("life-index")
        index = OriginIndex("life-index")
        events = []
        for ordinal in range(5):
            context = (
                {"origin_index_action": DESIGNATE_IMMEDIATE}
                if ordinal == 2
                else None
            )
            events.append(advance(kernel, index, f"event-{ordinal}", context))
        deferred_target = events[1]
        designation = advance(
            kernel,
            index,
            "deferred-designation",
            {
                "origin_index_action": DESIGNATE_DEFERRED,
                "origin_index_target_event_id": deferred_target.event_id,
                "origin_index_include": False,
            },
        )
        events.extend(
            [
                advance(kernel, index, "event-5"),
                advance(kernel, index, "event-6"),
            ]
        )
        immediate = events[2]

        self.assertEqual(
            index.relation(events[0].event_id, immediate.event_id, source_log_head=kernel.head),
            BEFORE,
        )
        self.assertEqual(
            index.relation(immediate.event_id, immediate.event_id, source_log_head=kernel.head),
            AT,
        )
        self.assertEqual(
            index.relation(events[-1].event_id, immediate.event_id, source_log_head=kernel.head),
            AFTER,
        )
        self.assertEqual(
            index.relation(
                deferred_target.event_id,
                deferred_target.event_id,
                source_log_head=kernel.head,
            ),
            BEFORE,
        )
        # The deferred control event advances the origin but is not recallable.
        queried = index.query_cycle_relative(
            0, 99, limit=99, source_log_head=kernel.head
        )
        self.assertNotIn(designation.event_id, queried)
        recent_after = index.query_landmark_relative(
            immediate.event_id,
            AFTER,
            limit=2,
            source_log_head=kernel.head,
        )
        self.assertEqual(recent_after, (events[-1].event_id, events[-2].event_id))

    def test_snapshot_and_replay_are_deterministic_and_use_durable_ids(self) -> None:
        kernel = SituatedOriginKernel("life-index", epoch=4)
        index = OriginIndex("life-index", epoch=4)
        first = advance(kernel, index, "event-0")
        advance(
            kernel,
            index,
            "event-1",
            {"origin_index_action": DESIGNATE_IMMEDIATE},
        )
        advance(kernel, index, "event-2")
        replayed = OriginIndex.replay(
            "life-index", kernel.events(), epoch=4
        )
        self.assertEqual(to_primitive(replayed.snapshot()), to_primitive(index.snapshot()))
        self.assertEqual(
            canonical_bytes(replayed.snapshot()), canonical_bytes(index.snapshot())
        )
        self.assertEqual(
            replayed.snapshot().indexed_events[0].event_id,
            first.event_id,
        )
        self.assertTrue(
            all(
                row.landmark_event_id.startswith("life-index:4:")
                for row in replayed.snapshot().landmarks
            )
        )
        index.verify(kernel.events())

    def test_rejects_non_ledger_writes_and_out_of_order_events(self) -> None:
        kernel = SituatedOriginKernel("life-index")
        index = OriginIndex("life-index")
        with self.assertRaisesRegex(OriginContractError, "COMMITTED_EVENT_REQUIRED"):
            index.ingest(proposal("raw-write"))  # type: ignore[arg-type]

        first = kernel.advance_origin(proposal("event-0"), expected_head=kernel.head)
        second = kernel.advance_origin(proposal("event-1"), expected_head=kernel.head)
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            index.ingest(second)
        index.ingest(first)
        index.ingest(second)
        self.assertEqual(index.source_log_head, kernel.head)

    def test_equivalence_with_committed_e1_immediate_and_deferred_behavior(self) -> None:
        kernel = SituatedOriginKernel("life-equivalence")
        origin = OriginIndex("life-equivalence")
        durable_events = []

        autobiography = e1.Autobiography()
        legacy = e1.EgocentricIndex(autobiography)
        legacy_events = []
        immediate_legacy = None
        immediate_durable = None

        for ordinal in range(5):
            legacy_event = autobiography.append(
                f"event-{ordinal}", content_id=f"event-{ordinal}"
            )
            legacy_events.append(legacy_event)
            legacy.re_resolve_index()
            context = None
            if ordinal == 2:
                legacy.designate_immediate(legacy_event)
                immediate_legacy = legacy_event
                context = {"origin_index_action": DESIGNATE_IMMEDIATE}
            durable = advance(kernel, origin, f"event-{ordinal}", context)
            durable_events.append(durable)
            if ordinal == 2:
                immediate_durable = durable

        deferred_legacy = legacy_events[1]
        legacy.designate_landmark(deferred_legacy)
        advance(
            kernel,
            origin,
            "deferred-designation",
            {
                "origin_index_action": DESIGNATE_DEFERRED,
                "origin_index_target_event_id": durable_events[1].event_id,
                "origin_index_include": False,
            },
        )

        for ordinal in range(5, 7):
            legacy_event = autobiography.append(
                f"event-{ordinal}", content_id=f"event-{ordinal}"
            )
            legacy_events.append(legacy_event)
            legacy.re_resolve_index()
            durable_events.append(advance(kernel, origin, f"event-{ordinal}"))

        assert immediate_legacy is not None and immediate_durable is not None
        for legacy_event, durable_event in zip(legacy_events, durable_events):
            self.assertEqual(
                origin.coordinate(
                    durable_event.event_id, source_log_head=kernel.head
                ).cycle_relative_distance,
                legacy.coord_cycle_relative(legacy_event),
            )
            self.assertEqual(
                origin.relation(
                    durable_event.event_id,
                    immediate_durable.event_id,
                    source_log_head=kernel.head,
                ),
                relation_from_e1(legacy, legacy_event, immediate_legacy),
            )
            self.assertEqual(
                origin.relation(
                    durable_event.event_id,
                    durable_events[1].event_id,
                    source_log_head=kernel.head,
                ),
                relation_from_e1(legacy, legacy_event, deferred_legacy),
            )

        for durable_landmark, legacy_landmark in (
            (immediate_durable, immediate_legacy),
            (durable_events[1], deferred_legacy),
        ):
            for relation in (BEFORE, AT, AFTER):
                durable_ids = origin.query_landmark_relative(
                    durable_landmark.event_id,
                    relation,
                    limit=3,
                    source_log_head=kernel.head,
                )
                durable_cycles = [
                    origin.coordinate(item, source_log_head=kernel.head).encoding_cycle
                    for item in durable_ids
                ]
                legacy_cycles = [
                    item.cycle
                    for item in legacy.query_landmark_relative_bounded(
                        legacy_landmark, relation, 3
                    )
                ]
                self.assertEqual(durable_cycles, legacy_cycles)


if __name__ == "__main__":
    unittest.main()
