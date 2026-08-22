from __future__ import annotations

import copy
import unittest

from src.situated_origin.experience import ExperiencePortError, UnboundExperiencePort
from src.situated_origin.vehicle import VehicleOrchestrator


class FakeClock:
    def __init__(self) -> None:
        self.now = 100
        self.waits: list[int] = []

    def clock(self) -> int:
        return self.now

    def sleep(self, target: int) -> None:
        self.waits.append(target)
        self.now = target


class Stateful:
    def __init__(self) -> None:
        self.values: list[object] = []
        self.barriers = 0

    def clean_barrier(self):
        self.barriers += 1


class FakeOrigin(Stateful):
    def __init__(self) -> None:
        super().__init__()
        self.aborts: list[str] = []
        self.infrastructure_events: list[dict] = []

    def commit_input(self, value):
        row = ("input", value["id"])
        self.values.append(row)
        return row

    def snapshot(self):
        return tuple(self.values)

    def commit_response(self, value):
        row = ("response", value["pair_id"])
        self.values.append(row)
        return row

    def abort_response(self, code):
        self.aborts.append(code)
        self.values.append(("TURN_ABORTED", code))

    def record_infrastructure_event(self, value):
        self.infrastructure_events.append(copy.deepcopy(value))


class FakeMemory(Stateful):
    def retrieve(self, origin_snapshot, request):
        self.values.append(("recall", request["id"]))
        return {"source": origin_snapshot, "id": request["id"]}


class FakeActuation(Stateful):
    def prepare(self, origin_snapshot, recall, request):
        capability = {"private_origin": origin_snapshot, "recall": recall}
        self.values.append(("act", request["id"]))
        return capability


class FakePair:
    def __init__(self, fail_id=None) -> None:
        self.fail_id = fail_id
        self.calls = []

    def dispatch(self, request, *, candidate_capability, peer_capability):
        if peer_capability is not None:
            raise AssertionError("peer received candidate capability")
        phase = "warmup" if candidate_capability is None else "measured"
        self.calls.append((request["id"], phase, candidate_capability, peer_capability))
        if request["id"] == self.fail_id:
            raise RuntimeError("PAIR_FAILED")
        return {"pair_id": request["id"], "status": "PASS"}


class FakeValidator:
    def __init__(self, reject_id=None) -> None:
        self.reject_id = reject_id

    def validate(self, stage, value):
        if value["pair_id"] == self.reject_id:
            raise RuntimeError("STAGED_OUTPUT_INVALID")
        return dict(value, stage=stage)


class FakePublisher:
    def __init__(self, *, fail_stage=False, fail_commit=False, fail_abort=False) -> None:
        self.staged = []
        self.committed = []
        self.aborted = []
        self.abort_rows = []
        self.fail_stage = fail_stage
        self.fail_commit = fail_commit
        self.fail_abort = fail_abort

    def stage(self, value):
        if self.fail_stage:
            raise RuntimeError("EVIDENCE_STAGE_FAILED")
        token = copy.deepcopy(value)
        self.staged.append(token)
        return token

    def commit(self, token, value):
        if self.fail_commit:
            raise RuntimeError("EVIDENCE_COMMIT_IO_FAILED")
        self.committed.append(copy.deepcopy(value))

    def abort(self, token):
        self.aborted.append(token)
        if self.fail_abort:
            raise RuntimeError("EVIDENCE_ABORT_FAILED")

    def publish_abort(self, value):
        self.abort_rows.append(dict(value))


class VehicleTests(unittest.TestCase):
    def build(
        self,
        *,
        fail_id=None,
        reject_id=None,
        fail_stage=False,
        fail_commit=False,
        fail_abort=False,
    ):
        origin, memory, actuation = FakeOrigin(), FakeMemory(), FakeActuation()
        pair = FakePair(fail_id)
        publisher = FakePublisher(
            fail_stage=fail_stage,
            fail_commit=fail_commit,
            fail_abort=fail_abort,
        )
        clock = FakeClock()
        cleaned = []
        vehicle = VehicleOrchestrator(
            origin=origin,
            memory=memory,
            actuation=actuation,
            pair=pair,
            validator=FakeValidator(reject_id),
            publisher=publisher,
            clock_ns=clock.clock,
            sleep_until_ns=clock.sleep,
            cleanup=lambda: cleaned.append(True),
        )
        return vehicle, origin, memory, actuation, pair, publisher, clock, cleaned

    def test_atomic_success_clean_barrier_and_peer_exclusion(self):
        vehicle, origin, memory, actuation, pair, publisher, clock, cleaned = self.build()
        result = vehicle.run(
            warmup_inputs=({"id": "w0"},),
            measured_inputs=({"id": "m0"}, {"id": "m1"}),
            schedule_offsets_ns=(5, 10),
            deadline_ns=50,
        )
        self.assertEqual("PASS", result.status)
        self.assertEqual(2, len(result.steps))
        self.assertTrue(all(step.evidence_finalized for step in result.steps))
        self.assertEqual(2, len(publisher.committed))
        self.assertIn("response_commit", publisher.committed[0])
        self.assertIn("response_commit", publisher.committed[1])
        self.assertEqual(1, origin.barriers)
        self.assertEqual(1, memory.barriers)
        self.assertEqual(1, actuation.barriers)
        self.assertEqual([105, 110], clock.waits)
        self.assertTrue(all(call[3] is None for call in pair.calls))
        self.assertIsNone(pair.calls[0][2])
        self.assertIsNotNone(pair.calls[1][2])
        self.assertEqual([True], cleaned)

    def test_pair_failure_preserves_input_and_records_next_durable_abort(self):
        vehicle, origin, memory, actuation, _, publisher, _, cleaned = self.build(fail_id="m1")
        result = vehicle.run(
            warmup_inputs=(),
            measured_inputs=({"id": "m0"}, {"id": "m1"}),
            schedule_offsets_ns=(1, 2),
            deadline_ns=20,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("RuntimeError", result.failure_code)
        self.assertEqual(1, len(result.steps))
        self.assertEqual(
            [
                ("input", "m0"),
                ("response", "m0"),
                ("input", "m1"),
                ("TURN_ABORTED", "RuntimeError"),
            ],
            origin.values,
        )
        self.assertNotIn(("response", "m1"), origin.values)
        self.assertEqual([("recall", "m0"), ("recall", "m1")], memory.values)
        self.assertEqual([("act", "m0"), ("act", "m1")], actuation.values)
        self.assertEqual(["RuntimeError"], origin.aborts)
        self.assertEqual(1, len(publisher.committed))
        self.assertEqual("RuntimeError", publisher.abort_rows[-1]["failure_code"])
        self.assertEqual([True], cleaned)

    def test_invalid_staged_output_never_commits_response_or_evidence(self):
        vehicle, origin, _, _, _, publisher, _, _ = self.build(reject_id="m0")
        result = vehicle.run(
            warmup_inputs=(), measured_inputs=({"id": "m0"},),
            schedule_offsets_ns=(1,), deadline_ns=20,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual((), result.steps)
        self.assertEqual(
            [("input", "m0"), ("TURN_ABORTED", "RuntimeError")],
            origin.values,
        )
        self.assertNotIn(("response", "m0"), origin.values)
        self.assertEqual([], publisher.committed)

    def test_evidence_stage_failure_aborts_open_turn_without_response(self):
        vehicle, origin, _, _, _, publisher, _, _ = self.build(fail_stage=True)
        result = vehicle.run(
            warmup_inputs=(), measured_inputs=({"id": "m0"},),
            schedule_offsets_ns=(1,), deadline_ns=20,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("RuntimeError", result.failure_code)
        self.assertEqual((), result.steps)
        self.assertEqual(
            [("input", "m0"), ("TURN_ABORTED", "RuntimeError")],
            origin.values,
        )
        self.assertEqual(["RuntimeError"], origin.aborts)
        self.assertEqual([], origin.infrastructure_events)
        self.assertEqual([], publisher.committed)
        self.assertEqual([None], publisher.aborted)
        self.assertEqual(
            [{"ordinal": 0, "failure_code": "RuntimeError"}],
            publisher.abort_rows,
        )

    def test_evidence_commit_failure_preserves_closed_response_and_reports_infrastructure(self):
        vehicle, origin, _, _, _, publisher, _, _ = self.build(fail_commit=True)
        result = vehicle.run(
            warmup_inputs=(), measured_inputs=({"id": "m0"},),
            schedule_offsets_ns=(1,), deadline_ns=20,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("EVIDENCE_FINALIZATION_FAILED", result.failure_code)
        self.assertEqual(1, len(result.steps))
        self.assertFalse(result.steps[0].evidence_finalized)
        self.assertEqual(
            [("input", "m0"), ("response", "m0")],
            origin.values,
        )
        self.assertEqual([], origin.aborts)
        self.assertEqual([], publisher.abort_rows)
        self.assertEqual(1, len(publisher.aborted))
        self.assertEqual(1, len(origin.infrastructure_events))
        event = origin.infrastructure_events[0]
        self.assertEqual("EVIDENCE_FINALIZATION_FAILED", event["kind"])
        self.assertEqual("RuntimeError", event["underlying_failure_code"])
        self.assertEqual(("response", "m0"), event["response_commit"])

    def test_publisher_abort_failure_never_prevents_origin_abort(self):
        vehicle, origin, _, _, _, publisher, _, _ = self.build(
            reject_id="m0", fail_abort=True
        )
        result = vehicle.run(
            warmup_inputs=(), measured_inputs=({"id": "m0"},),
            schedule_offsets_ns=(1,), deadline_ns=20,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("RuntimeError", result.failure_code)
        self.assertEqual(
            [("input", "m0"), ("TURN_ABORTED", "RuntimeError")],
            origin.values,
        )
        self.assertEqual(["RuntimeError"], origin.aborts)
        self.assertEqual([None], publisher.aborted)
        self.assertEqual(1, len(publisher.abort_rows))

    def test_answer_labels_are_rejected_before_any_dispatch(self):
        vehicle, origin, _, _, pair, publisher, _, cleaned = self.build()
        result = vehicle.run(
            warmup_inputs=(),
            measured_inputs=({"id": "m0", "ground_truth": "secret"},),
            schedule_offsets_ns=(1,), deadline_ns=20,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("GROUND_TRUTH_LABEL_FORBIDDEN", result.failure_code)
        self.assertEqual([], pair.calls)
        self.assertEqual([], origin.values)
        self.assertEqual([], publisher.committed)
        self.assertEqual([True], cleaned)

    def test_cleanup_runs_after_warmup_failure(self):
        vehicle, _, _, _, _, _, _, cleaned = self.build(fail_id="w0")
        result = vehicle.run(
            warmup_inputs=({"id": "w0"},), measured_inputs=(),
            schedule_offsets_ns=(), deadline_ns=20,
        )
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual([True], cleaned)

    def test_e3_placeholder_is_fail_closed_for_every_operation(self):
        port = UnboundExperiencePort()
        calls = (
            lambda: port.write_experience(None),
            lambda: port.advance_origin(None, None),
            lambda: port.retrieve_by_origin_distance(None, None, 1),
            lambda: port.consolidate(None),
            lambda: port.compare_to_log("experience", None),
        )
        for call in calls:
            with self.subTest(call=call):
                with self.assertRaisesRegex(
                    ExperiencePortError, "E3_EXPERIENCE_BACKEND_UNBOUND"
                ):
                    call()


if __name__ == "__main__":
    unittest.main()
