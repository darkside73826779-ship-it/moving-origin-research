from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.situated_origin.contracts import SituatedContextPacket, sha256_bytes, sha256_canonical
from src.situated_origin.kernel import INPUT_COMMITTED, OUTPUT_COMMITTED, TURN_ABORTED
from src.situated_origin.origin_index import DESIGNATE_DEFERRED, DESIGNATE_IMMEDIATE
from src.situated_origin.runtime import (
    RuntimeActuationPort, RuntimeMemoryPort, RuntimeOriginPort, SituatedRuntime,
)
from src.situated_origin.vehicle import VehicleOrchestrator


class Clock:
    def __init__(self) -> None: self.value = 100
    def now(self) -> int: return self.value
    def sleep(self, target: int) -> None: self.value = target


class Pair:
    def __init__(self, fail_id: str | None = None) -> None:
        self.fail_id = fail_id
        self.calls = []

    def dispatch(self, request, *, candidate_capability, peer_capability):
        self.calls.append((copy.deepcopy(request), candidate_capability, peer_capability))
        if peer_capability is not None:
            raise AssertionError("peer capability leak")
        if request["id"] == self.fail_id:
            raise RuntimeError("PAIR_FAILURE")
        if candidate_capability is None:
            return {"status": "PASS", "pair_id": request["id"], "output_text": "warmup"}
        if not isinstance(candidate_capability, SituatedContextPacket):
            raise AssertionError("candidate packet missing")
        return {
            "status": "PASS", "pair_id": request["id"],
            "output_text": "The recalled workshop key memory is grounded.",
            "claim_kind": "memory-recall",
            "supporting_event_ids": candidate_capability.selected_event_ids[:1],
        }


class Validator:
    def validate(self, stage, value):
        if value.get("status") != "PASS": raise RuntimeError("OUTPUT_INVALID")
        return dict(value, stage=stage)


class Publisher:
    def __init__(self) -> None:
        self.staged, self.committed, self.aborts = [], [], []
    def stage(self, value): self.staged.append(value); return len(self.staged) - 1
    def commit(self, token, value): self.committed.append(copy.deepcopy(value))
    def abort(self, token): self.aborts.append(token)
    def publish_abort(self, value): self.aborts.append(dict(value))


def request(request_id: str, color: str) -> dict:
    content = f"the workshop key is {color}"
    return {
        "id": request_id,
        "content": content,
        "question": "What color is the workshop key?",
        "features": [float(index + (1 if color == "green" else 0)) for index in range(8)],
        "fact": {"fact_id": f"fact-{request_id}", "valid_from": None, "valid_until": None},
        "source": {
            "source_kind": "public-test", "source_id": request_id,
            "source_sha256": sha256_bytes(content.encode()),
        },
    }


class SituatedRuntimeTests(unittest.TestCase):
    def build(self, *, fail_id=None):
        runtime = SituatedRuntime("runtime-test")
        pair, publisher, clock, cleanup = Pair(fail_id), Publisher(), Clock(), []
        vehicle = VehicleOrchestrator(
            origin=RuntimeOriginPort(runtime), memory=RuntimeMemoryPort(runtime),
            actuation=RuntimeActuationPort(runtime), pair=pair,
            validator=Validator(), publisher=publisher, clock_ns=clock.now,
            sleep_until_ns=clock.sleep, cleanup=lambda: cleanup.append(True),
        )
        return runtime, vehicle, pair, publisher, cleanup

    def test_real_ports_end_to_end_success_views_packet_peer_and_replay(self) -> None:
        runtime, vehicle, pair, publisher, cleanup = self.build()
        result = vehicle.run(
            warmup_inputs=({"id": "warmup", "content": "public warmup"},),
            measured_inputs=(request("turn-0", "blue"), request("turn-1", "green")),
            schedule_offsets_ns=(0, 5), deadline_ns=100,
        )
        self.assertEqual("PASS", result.status)
        self.assertEqual(2, len(result.steps))
        self.assertEqual([True], cleanup)
        self.assertEqual(1, runtime.barrier_count)
        self.assertEqual(4, len(runtime.kernel.events()))
        self.assertEqual(
            (INPUT_COMMITTED, OUTPUT_COMMITTED, INPUT_COMMITTED, OUTPUT_COMMITTED),
            tuple(item.proposal.kind for item in runtime.kernel.events()),
        )
        frame = runtime.snapshot().frame
        self.assertEqual(runtime.head, frame.stamp.log_head)
        self.assertEqual(runtime.head, runtime.access.source_log_head)
        self.assertEqual(runtime.head, runtime.present.source_log_head)
        self.assertEqual(runtime.head, runtime.facts.source_log_head)
        self.assertEqual(runtime.head, runtime.episodes.source_log_head)
        self.assertEqual(runtime.head, runtime.origin_index.source_log_head)
        self.assertEqual(runtime.access.head, frame.access_ledger_head)
        self.assertEqual(runtime.facts.head, frame.fact_graph_head)
        self.assertEqual(tuple(runtime.present.state), frame.retention)
        values = {
            "stamp": frame.stamp, "environment": frame.environment,
            "active_episode": frame.active_episode, "retention": frame.retention,
            "protention": frame.protention, "fact_graph_head": frame.fact_graph_head,
            "access_ledger_head": frame.access_ledger_head, "homeostasis": frame.homeostasis,
            "experience_strip": frame.experience_strip, "provenance_root": frame.provenance_root,
        }
        self.assertEqual(sha256_canonical(values), frame.frame_sha256)
        measured_calls = [row for row in pair.calls if row[1] is not None]
        self.assertEqual(2, len(measured_calls))
        self.assertTrue(all(isinstance(row[1], SituatedContextPacket) for row in measured_calls))
        self.assertTrue(all(row[2] is None for row in measured_calls))
        self.assertIn("workshop key", measured_calls[-1][1].rendered_text)
        self.assertTrue(measured_calls[-1][1].selected_event_ids)
        self.assertEqual(2, len(publisher.committed))
        access_records = {item.event_id: item for item in runtime.access.snapshot()}
        selected_across_steps = {
            event_id
            for step in result.steps
            for event_id in step.recall.selected_event_ids
        }
        self.assertTrue(selected_across_steps)
        self.assertTrue(
            all(access_records[event_id].rehearsal_count >= 1 for event_id in selected_across_steps)
        )
        runtime.verify()
        replay = SituatedRuntime.replay("runtime-test", runtime.kernel.events())
        self.assertEqual(runtime.head, replay.head)
        self.assertEqual(frame.frame_sha256, replay.snapshot().frame.frame_sha256)
        self.assertEqual(runtime.access.snapshot(), replay.access.snapshot())
        self.assertEqual(runtime.access.head, replay.access.head)

    def test_pair_failure_preserves_input_and_appends_provenance_complete_abort(self) -> None:
        runtime, vehicle, pair, publisher, cleanup = self.build(fail_id="turn-fail")
        result = vehicle.run(
            warmup_inputs=(), measured_inputs=(request("turn-fail", "blue"),),
            schedule_offsets_ns=(0,), deadline_ns=100,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual(0, len(result.steps))
        events = runtime.kernel.events()
        self.assertEqual(2, len(events))
        self.assertEqual((INPUT_COMMITTED, TURN_ABORTED), tuple(item.proposal.kind for item in events))
        self.assertEqual(events[0].stamp.cycle, events[1].stamp.cycle)
        abort_episode = runtime.episodes.query(events[1].event_id, runtime.head)
        self.assertEqual(events[1].event_sha256, abort_episode.event_sha256)
        self.assertEqual(events[0].event_sha256, abort_episode.prior_event_sha256)
        self.assertEqual(runtime.head, runtime.snapshot().frame.stamp.log_head)
        self.assertEqual(runtime.head, runtime.access.source_log_head)
        self.assertEqual(runtime.head, runtime.facts.source_log_head)
        self.assertEqual(runtime.head, runtime.present.source_log_head)
        self.assertEqual(runtime.head, runtime.episodes.source_log_head)
        self.assertEqual(runtime.head, runtime.origin_index.source_log_head)
        self.assertEqual([True], cleanup)
        self.assertTrue(publisher.aborts)
        runtime.verify()
        replay = SituatedRuntime.replay("runtime-test", events)
        self.assertEqual(runtime.snapshot().frame.frame_sha256, replay.snapshot().frame.frame_sha256)

    def test_post_response_infrastructure_failure_is_a_new_durable_cycle(self) -> None:
        runtime = SituatedRuntime("infrastructure-test")
        input_event = runtime.commit_input(request("turn-0", "blue"))
        output_event = runtime.commit_response({
            "output_text": "A grounded response was produced.",
            "status": "PASS",
        })
        infrastructure_event = RuntimeOriginPort(runtime).record_infrastructure_event({
            "kind": "EVIDENCE_FINALIZATION_FAILED",
            "failure_code": "EVIDENCE_FINALIZATION_FAILED",
            "underlying_failure_code": "EVIDENCE_COMMIT_IO_FAILED",
            "ordinal": 0,
            "response_commit": output_event,
        })

        self.assertEqual(input_event.stamp.cycle, output_event.stamp.cycle)
        self.assertEqual(output_event.stamp.cycle + 1, infrastructure_event.stamp.cycle)
        self.assertEqual("CADENCE_COMMITTED", infrastructure_event.proposal.kind)
        self.assertEqual(
            "EVIDENCE_FINALIZATION_FAILED",
            infrastructure_event.proposal.context["source_kind"],
        )
        self.assertEqual(
            output_event.event_id,
            infrastructure_event.proposal.context["response_commit_event_id"],
        )
        self.assertEqual(
            output_event.event_sha256,
            infrastructure_event.proposal.context["response_commit_sha256"],
        )
        runtime.verify()
        replay = SituatedRuntime.replay(
            "infrastructure-test", runtime.kernel.events()
        )
        self.assertEqual(runtime.head, replay.head)

    def test_direct_runtime_rejects_answer_fields_before_commit(self) -> None:
        runtime = SituatedRuntime("runtime-test")
        with self.assertRaisesRegex(Exception, "GROUND_TRUTH_LABEL_FORBIDDEN"):
            runtime.commit_input({"id": "bad", "content": "x", "ground_truth": "secret"})
        self.assertEqual((), runtime.kernel.events())

    def test_l4_landmark_perturbation_changes_grounded_candidate_context(self) -> None:
        def build_packet(designate_second: bool):
            runtime = SituatedRuntime("l4-second" if designate_second else "l4-first")
            first = request("turn-0", "blue")
            second = request("turn-1", "green")
            target = second if designate_second else first
            target["origin_index_action"] = DESIGNATE_IMMEDIATE
            first_event = runtime.commit_input(first)
            runtime.commit_response({"content": "first public response"})
            second_event = runtime.commit_input(second)
            runtime.commit_response({"content": "second public response"})
            landmark_id = second_event.event_id if designate_second else first_event.event_id
            snapshot = runtime.snapshot()
            recall = runtime.retrieve(snapshot, {
                "question": "workshop key", "landmark_ids": (landmark_id,),
                "include_stale": True, "memory_limit": 1,
            })
            return runtime, runtime.prepare(snapshot, recall, {"question": "workshop key"})

        first_runtime, first_packet = build_packet(False)
        second_runtime, second_packet = build_packet(True)
        self.assertEqual(first_runtime.head, first_runtime.origin_index.source_log_head)
        self.assertEqual(second_runtime.head, second_runtime.origin_index.source_log_head)
        self.assertIn("landmark_relations=AFTER_L", first_packet.rendered_text)
        self.assertIn("landmark_relations=AT_L", second_packet.rendered_text)
        self.assertNotEqual(first_packet.rendered_sha256, second_packet.rendered_sha256)
        self.assertNotIn("DISABLED", first_packet.rendered_text + second_packet.rendered_text)

    def test_deferred_landmark_control_is_materialized_but_not_recalled(self) -> None:
        runtime = SituatedRuntime("l4-deferred")
        target = runtime.commit_input(request("turn-0", "blue"))
        runtime.commit_response({"content": "first public response"})
        designation = request("turn-1", "green")
        designation.update({
            "origin_index_action": DESIGNATE_DEFERRED,
            "origin_index_target_event_id": target.event_id,
            "origin_index_include": False,
        })
        control = runtime.commit_input(designation)
        runtime.commit_response({"content": "second public response"})
        record = runtime.episodes.query(control.event_id, runtime.head)
        self.assertFalse(record.self_position_at_encoding["indexed"])
        self.assertEqual(control.event_sha256, record.self_position_at_encoding["source_log_head"])
        snapshot = runtime.snapshot()
        recall = runtime.retrieve(snapshot, {
            "question": "workshop key", "include_stale": True, "memory_limit": 8,
        })
        self.assertNotIn(control.event_id, recall.selected_event_ids)
        runtime.verify()


if __name__ == "__main__":
    unittest.main()
