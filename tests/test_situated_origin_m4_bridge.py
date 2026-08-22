from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from src.m4_post_tokenizer_integration import (
    CandidateAdapter,
    FanoutCoordinator,
    IntegrationError,
    PeerAdapter,
    encode_private_view,
    sha256_bytes as m4_sha256,
)
from src.situated_origin.contracts import SituatedContextPacket, sha256_bytes
from src.situated_origin.m4_bridge import M4BridgeError, SituatedM4Dispatcher


ROOT = Path(__file__).resolve().parents[1]


def provider(key):
    if key == "stop":
        return [900000, 900017]
    return [((key * 17) + index * 31) % 32749 for index in range(key)]


def request(operation_id: str, **values):
    return {
        "operation_id": operation_id,
        "caller_session_id": "bridge-caller",
        "caller_thread_id": "bridge-thread",
        **values,
    }


def manifest(role: str):
    pair = json.loads(
        (ROOT / "specs/data/m4_post_tokenizer_r_cc1_r_cc6_pair_fixture_v1.json").read_text(
            encoding="utf-8"
        )
    )
    return deepcopy(pair[role]["artifact"])


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


class StrictBackend:
    def __init__(self, role: str, session: str):
        self.role = role
        self.session = session
        self.state = {
            "generation": 0,
            "events": [],
            "live": True,
            "bound_context_identity": None,
            "bound_packet": None,
        }
        self.calls: list[str] = []
        self.step_observations: list[dict[str, object]] = []
        self.fail_step = False
        self.drift_context_on_step = False

    def capture_state(self):
        return deepcopy(self.state)

    def restore_state(self, snapshot):
        self.state = deepcopy(snapshot)

    def session_identity(self):
        return self.session

    def dispose(self):
        self.state["live"] = False

    def is_live(self):
        return self.state["live"]

    def _receipt(self, operation, prior, req):
        self.calls.append(operation)
        self.state["generation"] += 1
        self.state["events"].append(operation)
        return {
            "status": "PASS",
            "backend_code": None,
            "session_id": self.session,
            "prior_backend_state_sha256": prior,
            "result_backend_state_sha256": m4_sha256((prior + operation).encode("utf-8")),
            "request_sha256": m4_sha256(
                json.dumps(dict(req), sort_keys=True, separators=(",", ":")).encode("utf-8")
            ),
            "request_ordinal": req.get("request_ordinal") if operation == "step" else None,
        }

    def describe(self, _manifest, _config, req):
        return self._receipt("describe", "0" * 64, req)

    def initialize(self, _description, _session, req):
        prior = m4_sha256((("0" * 64) + "describe").encode("utf-8"))
        return self._receipt("initialize", prior, req)

    def reset_episode(self, prior, req):
        return self._receipt("reset_episode", prior, req)

    def step(self, prior, req, tokens):
        self.calls.append("step")
        saw_context = self.state["bound_context_identity"] is not None
        self.step_observations.append(
            {
                "token_sha256": tokens.sha256,
                "saw_context": saw_context,
                "context_identity": self.state["bound_context_identity"],
            }
        )
        if self.role == "candidate" and not saw_context:
            raise AssertionError("candidate context was not bound")
        if self.role == "peer" and saw_context:
            raise AssertionError("peer received candidate capability")
        if self.fail_step:
            raise IntegrationError("STRICT_PEER_FAILURE")
        self.state["generation"] += 1
        self.state["events"].append("step")
        if self.drift_context_on_step:
            self.state["bound_context_identity"] = "f" * 64
        return {
            "status": "PASS",
            "backend_code": None,
            "session_id": self.session,
            "prior_backend_state_sha256": prior,
            "result_backend_state_sha256": m4_sha256((prior + "step").encode("utf-8")),
            "request_sha256": m4_sha256(
                json.dumps(dict(req), sort_keys=True, separators=(",", ":")).encode("utf-8")
            ),
            "request_ordinal": req["request_ordinal"],
        }

    def snapshot(self, prior, req):
        return self._receipt("snapshot", prior, req)

    def close(self, prior, req):
        return self._receipt("close", prior, req)


class StrictBinding:
    def __init__(self):
        self.return_wrong_identity = False

    def bind_candidate(self, backend, packet, packet_identity):
        backend.state["bound_packet"] = {
            "packet_identity": packet_identity,
            "rendered_sha256": packet.rendered_sha256,
        }
        backend.state["bound_context_identity"] = packet_identity
        return "f" * 64 if self.return_wrong_identity else packet_identity

    def candidate_identity(self, backend):
        return backend.state["bound_context_identity"]

    def peer_is_unbound(self, backend):
        return (
            backend.state["bound_context_identity"] is None
            and backend.state["bound_packet"] is None
        )

    def clear_candidate(self, backend):
        backend.state["bound_context_identity"] = None
        backend.state["bound_packet"] = None


def ready_adapter(role: str):
    backend = StrictBackend(role, manifest(role)["runtime_instance_id"])
    adapter_type = CandidateAdapter if role == "candidate" else PeerAdapter
    adapter = adapter_type(
        role,
        role,
        manifest(role),
        {"adapter_instance_id": f"{role}-bridge-adapter"},
        provider,
        backend,
    )
    adapter.describe(request(f"{role}-describe"))
    adapter.initialize(request(f"{role}-initialize"))
    adapter.reset_episode(
        request(f"{role}-reset", episode_id="bridge-episode", reset_ordinal=1)
    )
    backend.calls.clear()
    return adapter, backend


class SituatedM4BridgeTests(unittest.TestCase):
    def setUp(self):
        self.rows = rows()
        self.stop = stop()
        self.candidate, self.candidate_backend = ready_adapter("candidate")
        self.peer, self.peer_backend = ready_adapter("peer")
        self.binding = StrictBinding()
        self.shared_prompt = "Public diagnostic question?"
        rendered = "Autobiographical context without answer labels."
        self.packet = SituatedContextPacket(
            shared_question_sha256=sha256_bytes(self.shared_prompt.encode("utf-8")),
            frame_sha256="1" * 64,
            recall_receipt_sha256="2" * 64,
            rendered_text=rendered,
            rendered_sha256=sha256_bytes(rendered.encode("utf-8")),
            selected_event_ids=("event-1",),
            source_log_head="3" * 64,
        )
        self.step_request = request(
            "bridge-step",
            episode_id="bridge-episode",
            request_ordinal=0,
            context_length=1024,
            is_terminal_request=True,
        )

    def dispatcher(self, *, coordinator=None, candidate_budget=100, peer_budget=100):
        return SituatedM4Dispatcher(
            coordinator=coordinator or FanoutCoordinator(provider),
            candidate=self.candidate,
            peer=self.peer,
            context_binding=self.binding,
            token_counter=lambda text: len(text.split()),
            candidate_token_budget=candidate_budget,
            peer_token_budget=peer_budget,
            expected_rows=self.rows,
            expected_stop=self.stop,
        )

    def test_real_fanout_uses_identical_shared_view_and_candidate_only_context(self):
        result = self.dispatcher().dispatch(
            request=self.step_request,
            packet=self.packet,
            shared_public_prompt=self.shared_prompt,
            rows=self.rows,
            stop=self.stop,
            context_length=1024,
        )

        self.assertEqual(result.fanout_receipt["status"], "PASS")
        self.assertEqual(result.fanout_execution_model, "SEQUENTIAL_CANDIDATE_THEN_PEER")
        self.assertEqual(self.candidate_backend.calls, ["step"])
        self.assertEqual(self.peer_backend.calls, ["step"])
        candidate_seen = self.candidate_backend.step_observations[0]
        peer_seen = self.peer_backend.step_observations[0]
        self.assertEqual(candidate_seen["token_sha256"], peer_seen["token_sha256"])
        self.assertTrue(candidate_seen["saw_context"])
        self.assertFalse(peer_seen["saw_context"])
        self.assertNotEqual(
            result.candidate_effective_prompt_sha256, result.peer_effective_prompt_sha256
        )
        self.assertGreater(
            result.candidate_effective_prompt_token_count,
            result.peer_effective_prompt_token_count,
        )
        self.assertIsNone(self.candidate_backend.state["bound_context_identity"])

    def test_wrong_rows_oversized_prompt_and_bad_binding_stop_before_backend_access(self):
        bad_rows = deepcopy(self.rows)
        bad_rows[0]["length"] -= 1
        cases = [
            (self.dispatcher(), {"rows": bad_rows}, "SHARED_ROWS_IDENTITY_MISMATCH"),
            (self.dispatcher(candidate_budget=1), {}, "EFFECTIVE_PROMPT_TOKEN_BUDGET_EXCEEDED"),
        ]
        for dispatcher, changes, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaises(M4BridgeError) as caught:
                    dispatcher.dispatch(
                        request=self.step_request,
                        packet=self.packet,
                        shared_public_prompt=self.shared_prompt,
                        rows=changes.get("rows", self.rows),
                        stop=self.stop,
                        context_length=1024,
                    )
                self.assertEqual(caught.exception.code, expected)
                self.assertEqual(self.candidate_backend.calls, [])
                self.assertEqual(self.peer_backend.calls, [])

        self.binding.return_wrong_identity = True
        with self.assertRaises(M4BridgeError) as caught:
            self.dispatcher().dispatch(
                request=self.step_request,
                packet=self.packet,
                shared_public_prompt=self.shared_prompt,
                rows=self.rows,
                stop=self.stop,
                context_length=1024,
            )
        self.assertEqual(caught.exception.code, "SITUATED_CONTEXT_BINDING_MISMATCH")
        self.assertEqual(self.candidate_backend.calls, [])
        self.assertEqual(self.peer_backend.calls, [])

    def test_wrong_prompt_identity_and_answer_label_stop_before_backend_access(self):
        with self.assertRaises(M4BridgeError) as caught:
            self.dispatcher().dispatch(
                request={**self.step_request, "ground_truth": "secret"},
                packet=self.packet,
                shared_public_prompt=self.shared_prompt,
                rows=self.rows,
                stop=self.stop,
                context_length=1024,
            )
        self.assertEqual(caught.exception.code, "ANSWER_OR_CONTROL_LABEL_FORBIDDEN")

        with self.assertRaises(M4BridgeError) as caught:
            self.dispatcher().dispatch(
                request=self.step_request,
                packet=self.packet,
                shared_public_prompt="different question",
                rows=self.rows,
                stop=self.stop,
                context_length=1024,
            )
        self.assertEqual(caught.exception.code, "SHARED_QUESTION_IDENTITY_MISMATCH")
        self.assertEqual(self.candidate_backend.calls, [])
        self.assertEqual(self.peer_backend.calls, [])

    def test_peer_failure_restores_both_real_backends_and_adapters(self):
        candidate_adapter_before = self.candidate.capture()
        peer_adapter_before = self.peer.capture()
        candidate_backend_before = self.candidate_backend.capture_state()
        peer_backend_before = self.peer_backend.capture_state()
        self.peer_backend.fail_step = True

        with self.assertRaises(IntegrationError) as caught:
            self.dispatcher().dispatch(
                request=self.step_request,
                packet=self.packet,
                shared_public_prompt=self.shared_prompt,
                rows=self.rows,
                stop=self.stop,
                context_length=1024,
            )
        self.assertEqual(caught.exception.code, "FANOUT_ATOMICITY_FAILURE")
        self.assertEqual(self.candidate.capture(), candidate_adapter_before)
        self.assertEqual(self.peer.capture(), peer_adapter_before)
        self.assertEqual(self.candidate_backend.capture_state(), candidate_backend_before)
        self.assertEqual(self.peer_backend.capture_state(), peer_backend_before)
        self.assertEqual(self.candidate_backend.calls, ["step"])
        self.assertEqual(self.peer_backend.calls, ["step"])

    def test_post_return_probe_restores_both_roles(self):
        candidate_adapter_before = self.candidate.capture()
        peer_adapter_before = self.peer.capture()
        candidate_backend_before = self.candidate_backend.capture_state()
        peer_backend_before = self.peer_backend.capture_state()
        coordinator = FanoutCoordinator(provider, post_return_probe=lambda _c, _p: True)

        with self.assertRaises(IntegrationError) as caught:
            self.dispatcher(coordinator=coordinator).dispatch(
                request=self.step_request,
                packet=self.packet,
                shared_public_prompt=self.shared_prompt,
                rows=self.rows,
                stop=self.stop,
                context_length=1024,
            )
        self.assertEqual(caught.exception.code, "PRIVATE_VIEW_MUTATED")
        self.assertEqual(self.candidate.capture(), candidate_adapter_before)
        self.assertEqual(self.peer.capture(), peer_adapter_before)
        self.assertEqual(self.candidate_backend.capture_state(), candidate_backend_before)
        self.assertEqual(self.peer_backend.capture_state(), peer_backend_before)

    def test_candidate_context_drift_after_call_restores_both_roles(self):
        candidate_adapter_before = self.candidate.capture()
        peer_adapter_before = self.peer.capture()
        candidate_backend_before = self.candidate_backend.capture_state()
        peer_backend_before = self.peer_backend.capture_state()
        self.candidate_backend.drift_context_on_step = True

        with self.assertRaises(M4BridgeError) as caught:
            self.dispatcher().dispatch(
                request=self.step_request,
                packet=self.packet,
                shared_public_prompt=self.shared_prompt,
                rows=self.rows,
                stop=self.stop,
                context_length=1024,
            )
        self.assertEqual(caught.exception.code, "SITUATED_CONTEXT_POST_RETURN_DRIFT")
        self.assertEqual(self.candidate.capture(), candidate_adapter_before)
        self.assertEqual(self.peer.capture(), peer_adapter_before)
        self.assertEqual(self.candidate_backend.capture_state(), candidate_backend_before)
        self.assertEqual(self.peer_backend.capture_state(), peer_backend_before)


if __name__ == "__main__":
    unittest.main()
