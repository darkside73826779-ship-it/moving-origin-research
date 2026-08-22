from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from src.m4_post_tokenizer_integration import (
    CandidateAdapter,
    FanoutCoordinator,
    IntegrationError,
    PeerAdapter,
    canonical_bytes as m4_canonical_bytes,
    encode_private_view,
    sha256_bytes as m4_sha256,
)
from src.situated_origin.assembly import (
    AssemblyError,
    AssemblyOutputValidator,
    BackendSituatedContextBinding,
    M4VehiclePairDispatcher,
)
from src.situated_origin.contracts import SituatedContextPacket, sha256_bytes
from src.situated_origin.kernel import INPUT_COMMITTED, OUTPUT_COMMITTED, TURN_ABORTED
from src.situated_origin.m4_bridge import (
    LocalBehaviorCapture,
    M4BridgeError,
    SituatedM4Dispatcher,
)
from src.situated_origin.runtime import (
    RuntimeActuationPort,
    RuntimeMemoryPort,
    RuntimeOriginPort,
    SituatedRuntime,
)
from src.situated_origin.vehicle import VehicleOrchestrator


ROOT = Path(__file__).resolve().parents[1]


def provider(key):
    if key == "stop":
        return [710001, 710009]
    return [((key * 13) + ordinal * 19) % 32749 for ordinal in range(key)]


def rows():
    output = []
    for length in (1024, 4096, 8192):
        digest = m4_sha256(encode_private_view(provider(length)))
        output.append(
            {
                "context_length": length,
                "length": length,
                "sha256": digest,
                "expected_sha256": digest,
            }
        )
    return output


def stop():
    digest = m4_sha256(encode_private_view(provider("stop")))
    return {"length": 2, "sha256": digest, "expected_sha256": digest}


def manifest(role: str):
    pair = json.loads(
        (
            ROOT
            / "specs/data/m4_post_tokenizer_r_cc1_r_cc6_pair_fixture_v1.json"
        ).read_text(encoding="utf-8")
    )
    return deepcopy(pair[role]["artifact"])


def control_request(operation_id: str, **values):
    return {
        "operation_id": operation_id,
        "caller_session_id": "assembly-caller",
        "caller_thread_id": "assembly-thread",
        **values,
    }


def plain(value):
    if isinstance(value, dict) or hasattr(value, "items"):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [plain(item) for item in value]
    return value


class CapturingBackend:
    """Custody-free backend that emits behavior through the explicit channel."""

    def __init__(
        self,
        role: str,
        session_id: str,
        capture: LocalBehaviorCapture,
        *,
        fail_step: bool = False,
    ) -> None:
        self.role = role
        self.session_id = session_id
        self.capture = capture
        self.fail_step = fail_step
        self.state = {
            "generation": 0,
            "events": [],
            "live": True,
            "situated_context_identity": None,
            "situated_context": None,
        }
        self.audit_calls: list[str] = []
        self.token_digests: list[str] = []

    def capture_state(self):
        return deepcopy(self.state)

    def restore_state(self, snapshot):
        self.state = deepcopy(snapshot)

    def session_identity(self):
        return self.session_id

    def dispose(self):
        self.state["live"] = False

    def is_live(self):
        return self.state["live"]

    def bind_situated_context(self, packet: SituatedContextPacket, identity: str):
        self.state["situated_context_identity"] = identity
        self.state["situated_context"] = {
            "rendered_text": packet.rendered_text,
            "rendered_sha256": packet.rendered_sha256,
            "selected_event_ids": list(packet.selected_event_ids),
        }
        return identity

    def situated_context_identity(self):
        return self.state["situated_context_identity"]

    def clear_situated_context(self):
        self.state["situated_context_identity"] = None
        self.state["situated_context"] = None

    def _receipt(self, operation, prior, request):
        self.audit_calls.append(operation)
        self.state["generation"] += 1
        self.state["events"].append(operation)
        return {
            "status": "PASS",
            "backend_code": None,
            "session_id": self.session_id,
            "prior_backend_state_sha256": prior,
            "result_backend_state_sha256": m4_sha256(
                (prior + operation).encode("utf-8")
            ),
            "request_sha256": m4_sha256(m4_canonical_bytes(plain(request))),
            "request_ordinal": (
                request.get("request_ordinal") if operation == "step" else None
            ),
        }

    def describe(self, _manifest, _config, request):
        return self._receipt("describe", "0" * 64, request)

    def initialize(self, _description, _session, request):
        prior = m4_sha256((("0" * 64) + "describe").encode("utf-8"))
        return self._receipt("initialize", prior, request)

    def reset_episode(self, prior, request):
        return self._receipt("reset_episode", prior, request)

    def step(self, prior, request, tokens):
        self.audit_calls.append("step")
        self.token_digests.append(tokens.sha256)
        request_sha256 = m4_sha256(m4_canonical_bytes(plain(request)))
        if self.role == "candidate":
            context = self.state["situated_context"]
            if not isinstance(context, dict):
                raise AssertionError("candidate missing situated context")
            rendered = context["rendered_text"]
            observed = "blue" if "blue" in rendered.casefold() else "no-blue-memory"
            output = f"Candidate situated observation: {observed}."
        else:
            if self.state["situated_context"] is not None:
                raise AssertionError("peer received situated context")
            output = "Peer observation without situated memory."
        self.capture.record(
            self.role,
            self.session_id,
            request_sha256,
            output.encode("utf-8"),
        )
        if self.fail_step:
            raise IntegrationError("CUSTODY_FREE_BACKEND_FAILURE")
        self.state["generation"] += 1
        self.state["events"].append("step")
        return {
            "status": "PASS",
            "backend_code": None,
            "session_id": self.session_id,
            "prior_backend_state_sha256": prior,
            "result_backend_state_sha256": m4_sha256(
                (prior + "step").encode("utf-8")
            ),
            "request_sha256": request_sha256,
            "request_ordinal": request["request_ordinal"],
        }

    def snapshot(self, prior, request):
        return self._receipt("snapshot", prior, request)

    def close(self, prior, request):
        return self._receipt("close", prior, request)


def ready_adapter(role: str, capture: LocalBehaviorCapture, *, fail_step=False):
    role_manifest = manifest(role)
    backend = CapturingBackend(
        role,
        role_manifest["runtime_instance_id"],
        capture,
        fail_step=fail_step,
    )
    adapter_type = CandidateAdapter if role == "candidate" else PeerAdapter
    adapter = adapter_type(
        role,
        role,
        role_manifest,
        {"adapter_instance_id": f"{role}-assembly-adapter"},
        provider,
        backend,
    )
    adapter.describe(control_request(f"{role}-describe"))
    adapter.initialize(control_request(f"{role}-initialize"))
    adapter.reset_episode(
        control_request(
            f"{role}-reset",
            episode_id="assembly-episode",
            reset_ordinal=1,
        )
    )
    backend.audit_calls.clear()
    return adapter, backend


class Clock:
    def __init__(self) -> None:
        self.value = 1_000

    def now(self):
        return self.value

    def sleep(self, target):
        self.value = target


class EvidenceJournal:
    def __init__(self) -> None:
        self.staged = []
        self.committed = []
        self.aborted = []

    def stage(self, value):
        self.staged.append(value)
        return len(self.staged) - 1

    def commit(self, token, value):
        self.committed.append(deepcopy(dict(value)))

    def abort(self, token):
        self.aborted.append(token)

    def publish_abort(self, value):
        self.aborted.append(dict(value))


def public_request(request_id: str, content: str, question: str):
    return {
        "id": request_id,
        "content": content,
        "question": question,
        "features": [float(index + 1) for index in range(8)],
        "memory_limit": 6,
        "operation_id": f"assembly-step:{request_id}",
        "caller_session_id": "assembly-caller",
        "caller_thread_id": "assembly-thread",
        "episode_id": "assembly-episode",
        "request_ordinal": 0,
        "context_length": 1024,
        "is_terminal_request": True,
        "source": {
            "source_kind": "public-assembly-test",
            "source_id": request_id,
            "source_sha256": sha256_bytes(content.encode("utf-8")),
        },
    }


class SituatedOriginAssemblyTests(unittest.TestCase):
    def build(self, *, peer_fails=False):
        capture = LocalBehaviorCapture()
        candidate, candidate_backend = ready_adapter("candidate", capture)
        peer, peer_backend = ready_adapter("peer", capture, fail_step=peer_fails)
        result_rows = rows()
        result_stop = stop()
        bridge = SituatedM4Dispatcher(
            coordinator=FanoutCoordinator(provider),
            candidate=candidate,
            peer=peer,
            context_binding=BackendSituatedContextBinding(),
            behavior_capture=capture,
            token_counter=lambda text: len(text.split()),
            candidate_token_budget=4096,
            peer_token_budget=4096,
            expected_rows=result_rows,
            expected_stop=result_stop,
        )
        pair = M4VehiclePairDispatcher(
            dispatcher=bridge,
            rows=result_rows,
            stop=result_stop,
            default_context_length=1024,
        )
        runtime = SituatedRuntime("one-vehicle-assembly")
        publisher = EvidenceJournal()
        clock = Clock()
        cleanup = []
        vehicle = VehicleOrchestrator(
            origin=RuntimeOriginPort(runtime),
            memory=RuntimeMemoryPort(runtime),
            actuation=RuntimeActuationPort(runtime),
            pair=pair,
            validator=AssemblyOutputValidator(),
            publisher=publisher,
            clock_ns=clock.now,
            sleep_until_ns=clock.sleep,
            cleanup=lambda: cleanup.append(True),
        )
        return (
            runtime,
            vehicle,
            pair,
            capture,
            candidate_backend,
            peer_backend,
            publisher,
            cleanup,
        )

    def test_one_vehicle_commits_memory_conditioned_candidate_and_peer_evidence(self):
        (
            runtime,
            vehicle,
            pair,
            capture,
            candidate_backend,
            peer_backend,
            publisher,
            cleanup,
        ) = self.build()
        seed = public_request(
            "seed-turn",
            "Yesterday the workshop key was blue.",
            "What happened in the workshop yesterday?",
        )
        runtime.commit_input(seed)
        runtime.commit_response({"content": "The public seed event was recorded."})

        measured = public_request(
            "measured-turn",
            "Today the workshop question returned.",
            "What color was the workshop key?",
        )
        result = vehicle.run(
            warmup_inputs=(),
            measured_inputs=(measured,),
            schedule_offsets_ns=(0,),
            deadline_ns=1_000,
        )

        self.assertEqual("PASS", result.status)
        self.assertEqual(1, len(result.steps))
        self.assertEqual("Candidate situated observation: blue.", result.steps[0].response["output_text"])
        self.assertEqual([True], cleanup)
        self.assertEqual(1, len(publisher.committed))
        self.assertIn("response_commit", publisher.committed[0])
        self.assertTrue(capture.is_clear())
        self.assertIsNone(candidate_backend.situated_context_identity())
        self.assertIsNone(peer_backend.situated_context_identity())
        self.assertEqual(candidate_backend.token_digests, peer_backend.token_digests)
        self.assertEqual(["step"], candidate_backend.audit_calls)
        self.assertEqual(["step"], peer_backend.audit_calls)

        events = runtime.kernel.events()
        self.assertEqual(
            (INPUT_COMMITTED, OUTPUT_COMMITTED, INPUT_COMMITTED, OUTPUT_COMMITTED),
            tuple(event.proposal.kind for event in events),
        )
        output = events[-1]
        self.assertEqual(b"Candidate situated observation: blue.", output.proposal.content)
        evidence = output.proposal.context["m4_pair_evidence"]
        self.assertEqual(
            "Peer observation without situated memory.",
            evidence["peer_behavior"]["output_text"],
        )
        self.assertFalse(evidence["outputs_equal"])
        self.assertTrue(evidence["selected_event_ids"])

        runtime.verify()
        frame = runtime.snapshot().frame
        self.assertEqual(runtime.head, frame.stamp.log_head)
        self.assertEqual(runtime.head, runtime.access.source_log_head)
        self.assertEqual(runtime.head, runtime.present.source_log_head)
        self.assertEqual(runtime.head, runtime.facts.source_log_head)
        self.assertEqual(runtime.head, runtime.episodes.source_log_head)
        self.assertEqual(runtime.head, runtime.origin_index.source_log_head)
        replay = SituatedRuntime.replay("one-vehicle-assembly", events)
        self.assertEqual(runtime.head, replay.head)
        self.assertEqual(frame.frame_sha256, replay.snapshot().frame.frame_sha256)

    def test_peer_failure_records_abort_and_clears_uncommitted_behavior(self):
        (
            runtime,
            vehicle,
            pair,
            capture,
            candidate_backend,
            peer_backend,
            publisher,
            cleanup,
        ) = self.build(peer_fails=True)
        measured = public_request(
            "failed-turn",
            "A public failure-path observation.",
            "What does the origin remember?",
        )

        result = vehicle.run(
            warmup_inputs=(),
            measured_inputs=(measured,),
            schedule_offsets_ns=(0,),
            deadline_ns=1_000,
        )

        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("FANOUT_ATOMICITY_FAILURE", result.failure_code)
        self.assertEqual((), result.steps)
        self.assertEqual(
            (INPUT_COMMITTED, TURN_ABORTED),
            tuple(event.proposal.kind for event in runtime.kernel.events()),
        )
        self.assertTrue(capture.is_clear())
        self.assertIsNone(candidate_backend.situated_context_identity())
        self.assertIsNone(peer_backend.situated_context_identity())
        self.assertEqual([], publisher.committed)
        self.assertTrue(publisher.aborted)
        self.assertEqual([True], cleanup)
        runtime.verify()

    def test_local_behavior_channel_rejects_foreign_writer_and_clears(self):
        capture = LocalBehaviorCapture()
        request_sha256 = "a" * 64
        capture.begin_pair(request_sha256, "candidate-session", "peer-session")
        with self.assertRaises(M4BridgeError) as caught:
            capture.record(
                "candidate",
                "foreign-session",
                request_sha256,
                b"foreign output",
            )
        self.assertEqual("BEHAVIOR_CAPTURE_CORRELATION_FAILURE", caught.exception.code)
        capture.abort_pair(request_sha256)
        self.assertTrue(capture.is_clear())

    def test_output_validator_rejects_peer_behavior_digest_drift(self):
        runtime, vehicle, *_ = self.build()
        seed = public_request(
            "seed-turn",
            "Yesterday the workshop key was blue.",
            "What happened in the workshop yesterday?",
        )
        runtime.commit_input(seed)
        runtime.commit_response({"content": "The public seed event was recorded."})
        measured = public_request(
            "measured-turn",
            "Today the workshop question returned.",
            "What color was the workshop key?",
        )
        result = vehicle.run(
            warmup_inputs=(),
            measured_inputs=(measured,),
            schedule_offsets_ns=(0,),
            deadline_ns=1_000,
        )
        self.assertEqual("PASS", result.status)
        tampered = deepcopy(dict(result.steps[0].response))
        tampered["m4_pair_evidence"]["peer_behavior"]["output_text"] += " drift"
        with self.assertRaises(AssemblyError) as caught:
            AssemblyOutputValidator().validate("MEASURED", tampered)
        self.assertEqual("ASSEMBLY_OUTPUT_EVIDENCE_INVALID", caught.exception.code)

        source_drift = deepcopy(dict(result.steps[0].response))
        source_drift["source"]["source_id"] = "candidate:foreign:request"
        with self.assertRaises(AssemblyError) as caught:
            AssemblyOutputValidator().validate("MEASURED", source_drift)
        self.assertEqual("ASSEMBLY_OUTPUT_CORRELATION_FAILURE", caught.exception.code)


if __name__ == "__main__":
    unittest.main()
