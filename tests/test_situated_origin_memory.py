from __future__ import annotations

import hashlib
import inspect
from dataclasses import replace
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.situated_origin.access import AccessLedger
from src.situated_origin.actuator import CandidateContextActuator
from src.situated_origin.claims import ProvenanceClaimGuard
from src.situated_origin.contracts import (
    CommittedOriginEvent, EnvironmentFrame, MemoryQuery, OriginContractError,
    OriginEventProposal, OriginStamp, ProvenanceHandle, SituatedOriginFrame,
    Unavailable, sha256_bytes,
)
from src.situated_origin.episodes import EpisodicStore
from src.situated_origin.facts import BiTemporalFactGraph, FactRevision
from src.situated_origin.present import ThickPresent
from src.situated_origin.retrieval import OriginDistanceRecall


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def event(event_id: str, content: bytes, cycle: int, prior: str) -> CommittedOriginEvent:
    source = ProvenanceHandle("public-fixture", event_id, digest(f"source:{event_id}"))
    proposal = OriginEventProposal("memory", content, source, {"fixture": event_id})
    event_sha = digest(f"event:{event_id}:{cycle}:{prior}:{content.hex()}")
    stamp = OriginStamp("test-life", 0, cycle, cycle, event_sha)
    return CommittedOriginEvent(event_id, stamp, proposal, prior, event_sha)


def frame(
    cycle: int, log_head: str, fact_head: str, access_head: str,
    retention: tuple[float, ...] = (1.0, 0.5),
) -> SituatedOriginFrame:
    stamp = OriginStamp("test-life", 0, cycle, cycle, log_head)
    env = EnvironmentFrame(
        Unavailable("NOT_OBSERVED"), Unavailable("NOT_OBSERVED"),
        Unavailable("NOT_OBSERVED"), "memory-test",
    )
    return SituatedOriginFrame(
        stamp=stamp, environment=env, active_episode="test-episode",
        retention=retention, protention=Unavailable("NOT_BOUND"),
        fact_graph_head=fact_head, access_ledger_head=access_head,
        homeostasis=Unavailable("NOT_BOUND"), experience_strip=Unavailable("NOT_BOUND"),
        provenance_root=digest("provenance"), frame_sha256=digest(f"frame:{cycle}:{log_head}:{fact_head}:{access_head}"),
    )


class SituatedOriginMemoryTests(unittest.TestCase):
    def test_l1_persistent_same_clock_and_semantic_ranking(self) -> None:
        ledger = AccessLedger()
        ledger.advance_to(0, digest("head-0"))
        ledger.register("a", 0)
        ledger.register("b", 0)
        baseline = ledger.rank(("a", "b"), 0)
        ledger.rehearse("b", 0)
        changed = ledger.rank(("a", "b"), 0)
        self.assertEqual(baseline, ("a", "b"))
        self.assertEqual(changed, ("b", "a"))
        with self.assertRaisesRegex(OriginContractError, "ACCESS_CLOCK_MISMATCH"):
            ledger.priority("a", 1)

    def test_l3_incremental_equals_independent_batch_reference(self) -> None:
        rows = ((1.0, 2.0), (3.0, 5.0), (8.0, 13.0))
        present = ThickPresent(2)
        incremental = tuple(present.advance(index, row, digest(f"head-{index}")) for index, row in enumerate(rows))
        self.assertEqual(incremental, ThickPresent.batch_reference(rows))
        perturbed = (rows[0], (3.0, 6.0), rows[2])
        self.assertNotEqual(ThickPresent.batch_reference(rows), ThickPresent.batch_reference(perturbed))

    def test_l5_stable_bitemporal_supersession_graph(self) -> None:
        graph = BiTemporalFactGraph()
        identity = id(graph)
        graph.advance_to(0, digest("head-0"))
        graph.append(FactRevision("f0", "e0", b"old blue fact", 0, 0, 10, None))
        graph.advance_to(1, digest("head-1"))
        graph.append(FactRevision("f1", "e1", b"new green fact", 1, 1, None, "f0"))
        self.assertEqual(id(graph), identity)
        self.assertEqual(graph.walk("f0"), ("f0", "f1"))
        self.assertFalse(graph.is_current("f0", 1))
        self.assertTrue(graph.is_current("f1", 1))
        self.assertEqual(tuple(item.fact_id for item in graph.current(1)), ("f1",))

    def test_l6_public_provenance_complete_roundtrip(self) -> None:
        item = event("e0", b"binary\x00memory", 0, "0" * 64)
        store = EpisodicStore()
        record = store.write(item, {"cycle": 0, "landmark_relative": {"L": "BEFORE_L"}})
        restored = store.from_bytes(store.to_bytes(record))
        self.assertEqual(restored, record)
        self.assertEqual(restored.encoding_stamp.log_head, item.event_sha256)
        self.assertEqual(restored.prior_event_sha256, item.prior_event_sha256)
        self.assertEqual(restored.source, item.proposal.source)

    def test_every_materialized_view_rejects_stale_source_head(self) -> None:
        head = digest("current-head")
        stale = digest("stale-head")
        access = AccessLedger(); access.advance_to(0, head)
        present = ThickPresent(1); present.advance(0, (1.0,), head)
        facts = BiTemporalFactGraph(); facts.advance_to(0, head)
        item = event("e0", b"memory", 0, "0" * 64)
        episodes = EpisodicStore(); episodes.write(item, {"cycle": 0})
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            access.require_source_head(stale)
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            present.require_source_head(stale)
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            facts.require_source_head(stale)
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            episodes.query("e0", stale)

    def _vehicle(
        self,
        *,
        e0_state: tuple[float, ...] | None = None,
        e1_state: tuple[float, ...] | None = None,
        retention: tuple[float, ...] = (1.0, 0.5),
    ):
        e0 = event("e0", b"the workshop key is blue", 0, "0" * 64)
        e1 = event("e1", b"the workshop key is green", 1, e0.event_sha256)
        access = AccessLedger()
        access.advance_to(0, e0.event_sha256); access.register("e0", 0)
        access.advance_to(1, e1.event_sha256); access.register("e1", 1); access.rehearse("e1", 1)
        facts = BiTemporalFactGraph()
        facts.advance_to(0, e0.event_sha256); facts.append(FactRevision("f0", "e0", e0.proposal.content, 0, 0, None, None))
        facts.advance_to(1, e1.event_sha256); facts.append(FactRevision("f1", "e1", e1.proposal.content, 1, 1, None, "f0"))
        episodes = EpisodicStore()
        episodes.write(e0, {
            "cycle": 0, "landmark_relative": {"L": "BEFORE_L"},
            **({"thick_present_state": e0_state} if e0_state is not None else {}),
        })
        episodes.write(e1, {
            "cycle": 1, "landmark_relative": {"L": "AFTER_L"},
            **({"thick_present_state": e1_state} if e1_state is not None else {}),
        })
        view = frame(1, e1.event_sha256, facts.head, access.head, retention)
        recall = OriginDistanceRecall(access, facts, episodes)
        return e0, e1, facts, view, recall

    def test_origin_distance_recall_content_staleness_and_fact_ablation(self) -> None:
        e0, e1, facts, view, recall = self._vehicle()
        query = MemoryQuery("workshop key", landmark_ids=("L",), limit=4)
        result = recall.recall(query, view, ("e0", "e1"), view.stamp.log_head)
        self.assertEqual(result.selected_event_ids, ("e1",))
        self.assertIn(b"green", result.records[0].content)
        stale_included = recall.recall(
            MemoryQuery("workshop key", landmark_ids=("L",), include_stale=True, limit=4),
            view, ("e0", "e1"), view.stamp.log_head,
        )
        self.assertNotEqual(stale_included.selected_event_ids, result.selected_event_ids)
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            recall.recall(query, view, ("e0", "e1"), digest("stale"))

    def test_claim_guard_and_ground_truth_free_actuator(self) -> None:
        _, e1, _, view, recall = self._vehicle()
        result = recall.recall(MemoryQuery("workshop key"), view, ("e0", "e1"), view.stamp.log_head)
        guard = ProvenanceClaimGuard()
        self.assertEqual(guard.assess("key-color", ("e1",), result).status, "GROUNDED")
        self.assertEqual(guard.assess("key-color", ("missing",), result).status, "UNSUPPORTED")
        actuator = CandidateContextActuator()
        packet = actuator.compile(b"What color is the workshop key?", view, result)
        self.assertIn("the workshop key is green", packet.rendered_text)
        self.assertEqual(packet.selected_event_ids, ("e1",))
        self.assertNotIn("ground_truth", inspect.signature(actuator.compile).parameters)
        self.assertNotIn("DISABLED", packet.rendered_text)

    def test_semantic_access_and_l5_ablations_change_context_without_markers(self) -> None:
        _, _, _, view, recall = self._vehicle()
        query = MemoryQuery("workshop key", include_stale=True)
        base = recall.recall(query, view, ("e0", "e1"), view.stamp.log_head)
        actuator = CandidateContextActuator()
        base_packet = actuator.compile(b"question", view, base)
        # L5 semantic ablation: normal query excludes the superseded memory.
        filtered = recall.recall(MemoryQuery("workshop key"), view, ("e0", "e1"), view.stamp.log_head)
        filtered_packet = actuator.compile(b"question", view, filtered)
        self.assertNotEqual(base_packet.selected_event_ids, filtered_packet.selected_event_ids)
        self.assertNotEqual(base_packet.rendered_sha256, filtered_packet.rendered_sha256)
        self.assertNotIn("DISABLED", base_packet.rendered_text + filtered_packet.rendered_text)

    def test_l6_provenance_perturbation_changes_actuated_context(self) -> None:
        _, _, _, view, recall = self._vehicle()
        result = recall.recall(MemoryQuery("workshop key"), view, ("e0", "e1"), view.stamp.log_head)
        packet = CandidateContextActuator().compile(b"question", view, result)
        altered_source = ProvenanceHandle("public-fixture", "altered-source", digest("altered-source"))
        altered_memory = replace(result.records[0], source=altered_source)
        altered_recall = replace(result, records=(altered_memory,))
        altered_packet = CandidateContextActuator().compile(b"question", view, altered_recall)
        self.assertEqual(packet.selected_event_ids, altered_packet.selected_event_ids)
        self.assertNotEqual(packet.rendered_sha256, altered_packet.rendered_sha256)
        self.assertNotIn("DISABLED", altered_packet.rendered_text)

    def test_l3_state_perturbation_changes_useful_memory_selection_and_context(self) -> None:
        _, _, _, view, recall = self._vehicle(
            e0_state=(1.0, 0.5), e1_state=(9.0, 9.0)
        )
        query = MemoryQuery("workshop key", include_stale=True, limit=1)
        near_first = recall.recall(query, view, ("e0", "e1"), view.stamp.log_head)
        shifted_view = replace(view, retention=(9.0, 9.0), frame_sha256=digest("shifted-l3-frame"))
        near_second = recall.recall(query, shifted_view, ("e0", "e1"), shifted_view.stamp.log_head)
        first_packet = CandidateContextActuator().compile(b"question", view, near_first)
        second_packet = CandidateContextActuator().compile(b"question", shifted_view, near_second)
        self.assertEqual(("e0",), first_packet.selected_event_ids)
        self.assertEqual(("e1",), second_packet.selected_event_ids)
        self.assertNotEqual(first_packet.rendered_sha256, second_packet.rendered_sha256)
        self.assertIn("state_divergence=", first_packet.rendered_text)
        self.assertNotIn("DISABLED", first_packet.rendered_text + second_packet.rendered_text)


if __name__ == "__main__":
    unittest.main()
