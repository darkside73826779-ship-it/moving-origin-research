"""Production-entrypoint tests for the M4 post-tokenizer integration seam."""

from __future__ import annotations

import json
import threading
import unittest
from copy import deepcopy
from pathlib import Path

from src.m4_post_tokenizer_integration import (
    AdapterFactory, CandidateAdapter, FanoutCoordinator, IntegrationError,
    PeerAdapter, PrivateTokenView, encode_private_view, held_law_projection,
    sha256_bytes, validate_laws, validate_pair_identity,
)

ROOT = Path(__file__).resolve().parents[1]


def provider(key):
    if key == "stop":
        return [900000, 900017]
    return [((key * 17) + i * 31) % 32749 for i in range(key)]


class SpyBackend:
    def __init__(self, session="candidate-session-v1", behavior=None):
        self.session, self.behavior, self.calls = session, behavior or {}, []

    def _receipt(self, operation, prior, request=None):
        self.calls.append(operation)
        action = self.behavior.get(operation)
        if isinstance(action, Exception): raise action
        if action is not None: return deepcopy(action)
        receipt = {"status": "PASS", "backend_code": None, "session_id": self.session,
                   "prior_backend_state_sha256": prior,
                   "result_backend_state_sha256": sha256_bytes((prior + operation).encode())}
        if request:
            for key in ("episode_id", "request_ordinal"):
                if key in request: receipt[key] = request[key]
        return receipt

    def describe(self, manifest, config): return self._receipt("describe", "0" * 64)
    def initialize(self, description, session):
        prior = sha256_bytes((("0" * 64) + "describe").encode())
        return self._receipt("initialize", prior)
    def reset_episode(self, prior, request): return self._receipt("reset_episode", prior, request)
    def step(self, prior, request, tokens): return self._receipt("step", prior, request)
    def snapshot(self, prior, request): return self._receipt("snapshot", prior, request)
    def close(self, prior, request): return self._receipt("close", prior, request)


def manifest(role="candidate", session="candidate-session-v1"):
    pair = json.loads((ROOT / "specs/data/m4_post_tokenizer_r_cc1_r_cc6_pair_fixture_v1.json").read_text())
    return deepcopy(pair[role]["artifact"])


def adapter(role="candidate", backend=None):
    m = manifest(role, f"{role}-session-v1")
    b = backend or SpyBackend(m["runtime_instance_id"])
    cls = CandidateAdapter if role == "candidate" else PeerAdapter
    a = cls(role, role, m, {"adapter_instance_id": role + "-adapter"}, provider, b)
    return a, b


def request(operation_id, **kwargs):
    return {"operation_id": operation_id, "caller_session_id": "caller-main",
            "caller_thread_id": "thread-0", **kwargs}


def initialized(role="candidate", backend=None):
    a, b = adapter(role, backend)
    a.describe(request("describe")); a.initialize(request("initialize"))
    return a, b


def ready(role="candidate", backend=None, episode="episode-a"):
    a, b = initialized(role, backend)
    a.reset_episode(request("reset", episode_id=episode, reset_ordinal=1))
    return a, b


def sanitized_rows():
    return [{"context_length": n, "length": n, "sha256": sha256_bytes(encode_private_view(provider(n)))}
            for n in (1024, 4096, 8192)]


def stop_row():
    digest = sha256_bytes(encode_private_view(provider("stop")))
    return {"length": 2, "sha256": digest, "expected_sha256": digest}


class EncodingAndIdentityTests(unittest.TestCase):
    def test_exact_private_view_digests(self):
        expected = {
            1024: "c96f4755a75ea441eafdea6412a641b2758338d4f2cbfa30b896c6cbfc9e6d69",
            4096: "a1f986f189fb077f1384df22d23ed4281eb2c8f5649ce66f4be8036beff1f72e",
            8192: "33a4f1905df626e464be9b801e8e3d0abf702ae6597f0813b31bfb2eee5eb26f",
        }
        for n, digest in expected.items(): self.assertEqual(sha256_bytes(encode_private_view(provider(n))), digest)
        self.assertEqual(sha256_bytes(encode_private_view(provider("stop"))), "fb9543fe31b55a34dbb69924e05690c75589208063637bbd08e5092d1cbb2a62")

    def test_pair_identity_positive(self): validate_pair_identity(manifest("candidate"), manifest("peer"))
    def test_each_equality_field_mutation_fails(self):
        c, p = manifest("candidate"), manifest("peer")
        for field in ("checkpoint_sha256", "checkpoint_revision", "weight_hashes", "training_instance_sha256",
                      "tokenizer_sha256", "architecture_sha256", "parameter_count", "quantization_sha256",
                      "decoding_sha256", "calibration_contract_sha256", "evaluation_data_sha256", "binning_definition_sha256"):
            bad = deepcopy(p); bad[field] = "different" if not isinstance(bad[field], list) else ["different"]
            with self.subTest(field=field), self.assertRaisesRegex(IntegrationError, "PAIR_IDENTITY_MISMATCH"):
                validate_pair_identity(c, bad)
    def test_each_difference_field_collapse_fails(self):
        c, p = manifest("candidate"), manifest("peer")
        for field in ("role", "scientific_arm", "runtime_instance_id", "access_policy_id", "channel_policy", "redaction_receipt_sha256"):
            bad = deepcopy(p); bad[field] = c[field]
            with self.subTest(field=field), self.assertRaises(IntegrationError): validate_pair_identity(c, bad)


class LifecycleTests(unittest.TestCase):
    def test_full_42_cell_lifecycle_matrix_through_public_methods(self):
        legal = {
            "CREATED": {"describe"}, "DESCRIBED": {"initialize"},
            "INITIALIZED": {"reset_episode", "close"}, "EPISODE_READY": {"step", "close"},
            "STEPPED_INCOMPLETE": {"step", "snapshot", "close"},
            "STEPPED_COMPLETE": {"reset_episode", "snapshot", "close"}, "CLOSED": set(),
        }
        def at(category):
            a,b=adapter()
            if category=="CREATED": return a,b
            a.describe(request("d"))
            if category=="DESCRIBED": return a,b
            a.initialize(request("i"))
            if category=="INITIALIZED": return a,b
            a.reset_episode(request("r",episode_id="episode-a",reset_ordinal=1))
            if category=="EPISODE_READY": return a,b
            view=PrivateTokenView(1024,encode_private_view(provider(1024)))
            a.step(request("s",episode_id="episode-a",request_ordinal=0,context_length=1024,
                           is_terminal_request=category=="STEPPED_COMPLETE"),view)
            if category in ("STEPPED_INCOMPLETE","STEPPED_COMPLETE"): return a,b
            a.close(request("c")); return a,b
        for category in legal:
            for operation in ("describe","initialize","reset_episode","step","snapshot","close"):
                a,b=at(category); before,count=a.durable_state(),len(b.calls)
                if operation=="describe": invoke=lambda: a.describe(request("d2"))
                elif operation=="initialize": invoke=lambda: a.initialize(request("i2"))
                elif operation=="reset_episode": invoke=lambda: a.reset_episode(request("r2",episode_id="episode-b",reset_ordinal=2 if category.startswith("STEPPED") else 1))
                elif operation=="step":
                    ordinal=1 if category=="STEPPED_INCOMPLETE" else 0
                    invoke=lambda ordinal=ordinal: a.step(request("s2",episode_id="episode-a",request_ordinal=ordinal,context_length=1024,is_terminal_request=True),PrivateTokenView(1024,encode_private_view(provider(1024))))
                elif operation=="snapshot": invoke=lambda: a.snapshot(request("p",snapshot_ordinal=0))
                else: invoke=lambda: a.close(request("c2"))
                if operation in legal[category]:
                    invoke(); self.assertEqual(len(b.calls),count+1,(category,operation))
                else:
                    expected = "EPISODE_NOT_COMPLETE" if category=="STEPPED_INCOMPLETE" and operation=="reset_episode" else "EPISODE_ALREADY_COMPLETE" if category=="STEPPED_COMPLETE" and operation=="step" else "ADAPTER_LIFECYCLE_VIOLATION"
                    with self.subTest(category=category,operation=operation),self.assertRaisesRegex(IntegrationError,expected): invoke()
                    self.assertEqual((a.durable_state(),len(b.calls)),(before,count))

    def test_complete_two_episode_sequence(self):
        a, b = ready()
        for ordinal, terminal in ((0, False), (1, False), (2, True)):
            a.step(request(f"step-{ordinal}", episode_id="episode-a", request_ordinal=ordinal,
                           context_length=1024, is_terminal_request=terminal), PrivateTokenView(1024, encode_private_view(provider(1024))))
        a.reset_episode(request("reset-b", episode_id="episode-b", reset_ordinal=2))
        a.step(request("step-b", episode_id="episode-b", request_ordinal=0, context_length=1024,
                       is_terminal_request=True), PrivateTokenView(1024, encode_private_view(provider(1024))))
        self.assertEqual(json.loads(a.durable_state())["lifecycle_state"], "STEPPED")
        self.assertEqual(b.calls.count("step"), 4)

    def test_close_from_all_three_states(self):
        a, _ = initialized(); a.close(request("close-i"))
        a, _ = ready(); a.close(request("close-r"))
        a, _ = ready(); a.step(request("s", episode_id="episode-a", request_ordinal=0, context_length=1024,
                                        is_terminal_request=False), PrivateTokenView(1024, encode_private_view(provider(1024)))); a.close(request("close-s"))

    def test_all_operations_after_close_fail_without_call(self):
        a, b = initialized(); a.close(request("close")); before, count = a.durable_state(), len(b.calls)
        operations = [lambda: a.describe(request("d")), lambda: a.initialize(request("i")),
                      lambda: a.reset_episode(request("r", episode_id="x", reset_ordinal=1)),
                      lambda: a.step(request("s", episode_id="x", request_ordinal=0, context_length=1024), PrivateTokenView(1024, b"")),
                      lambda: a.snapshot(request("p", snapshot_ordinal=0)), lambda: a.close(request("c"))]
        for operation in operations:
            with self.assertRaisesRegex(IntegrationError, "ADAPTER_LIFECYCLE_VIOLATION"): operation()
            self.assertEqual((a.durable_state(), len(b.calls)), (before, count))

    def test_reset_requires_complete_episode(self):
        a, b = ready(); a.step(request("s", episode_id="episode-a", request_ordinal=0, context_length=1024,
                                      is_terminal_request=False), PrivateTokenView(1024, encode_private_view(provider(1024))))
        before, count = a.durable_state(), len(b.calls)
        with self.assertRaisesRegex(IntegrationError, "EPISODE_NOT_COMPLETE"):
            a.reset_episode(request("r", episode_id="episode-b", reset_ordinal=2))
        self.assertEqual((a.durable_state(), len(b.calls)), (before, count))

    def test_ordinal_episode_and_terminal_negatives(self):
        for code, change in (
            ("REQUEST_ORDINAL_MISMATCH", {"request_ordinal": 1}),
            ("EPISODE_ID_MISMATCH", {"episode_id": "wrong"}),
            ("CONTEXT_REQUEST_MISMATCH", {"context_length": 4096}),
        ):
            a, b = ready(); before, count = a.durable_state(), len(b.calls)
            kwargs = {"episode_id": "episode-a", "request_ordinal": 0, "context_length": 1024, "is_terminal_request": False}; kwargs.update(change)
            with self.subTest(code=code), self.assertRaisesRegex(IntegrationError, code):
                a.step(request("s", **kwargs), PrivateTokenView(1024, encode_private_view(provider(1024))))
            self.assertEqual((a.durable_state(), len(b.calls)), (before, count))
        a, b = ready(); view = PrivateTokenView(1024, encode_private_view(provider(1024)))
        a.step(request("s", episode_id="episode-a", request_ordinal=0, context_length=1024, is_terminal_request=True), view)
        with self.assertRaisesRegex(IntegrationError, "EPISODE_ALREADY_COMPLETE"):
            a.step(request("s2", episode_id="episode-a", request_ordinal=1, context_length=1024), view)

    def test_reset_reuse_and_ordinal_negatives(self):
        a, b = initialized(); before, count = a.durable_state(), len(b.calls)
        with self.assertRaisesRegex(IntegrationError, "RESET_ORDINAL_MISMATCH"):
            a.reset_episode(request("r", episode_id="a", reset_ordinal=2))
        self.assertEqual((a.durable_state(), len(b.calls)), (before, count))
        a.reset_episode(request("r", episode_id="a", reset_ordinal=1)); view = PrivateTokenView(1024, encode_private_view(provider(1024)))
        a.step(request("s", episode_id="a", request_ordinal=0, context_length=1024, is_terminal_request=True), view)
        with self.assertRaisesRegex(IntegrationError, "EPISODE_ID_REUSE"):
            a.reset_episode(request("r2", episode_id="a", reset_ordinal=2))

    def test_snapshot_ordinal(self):
        a, b = ready(); view = PrivateTokenView(1024, encode_private_view(provider(1024)))
        a.step(request("s", episode_id="episode-a", request_ordinal=0, context_length=1024), view)
        before, count = a.durable_state(), len(b.calls)
        with self.assertRaisesRegex(IntegrationError, "SNAPSHOT_ORDINAL_MISMATCH"): a.snapshot(request("p", snapshot_ordinal=1))
        self.assertEqual((a.durable_state(), len(b.calls)), (before, count)); a.snapshot(request("p", snapshot_ordinal=0))

    def test_inflight_and_reentrant_precede_parsing(self):
        a, b = adapter(); identity = a._caller_digest(request("outer")); a._active_identity = identity
        before, count = a.durable_state(), len(b.calls)
        with self.assertRaisesRegex(IntegrationError, "ADAPTER_REENTRANCY_FORBIDDEN"): a.describe(request("outer"))
        with self.assertRaisesRegex(IntegrationError, "ADAPTER_OPERATION_IN_FLIGHT"):
            a.describe({"operation_id": "other", "caller_session_id": "other", "caller_thread_id": "other"})
        self.assertEqual((a.durable_state(), len(b.calls)), (before, count)); a._active_identity = None


class BackendFailureTests(unittest.TestCase):
    def _step_failure(self, action, code):
        b = SpyBackend("candidate-session-v1", {"step": action}); a, _ = ready(backend=b)
        before, count = a.durable_state(), len(b.calls)
        with self.assertRaisesRegex(IntegrationError, code):
            a.step(request("s", episode_id="episode-a", request_ordinal=0, context_length=1024), PrivateTokenView(1024, encode_private_view(provider(1024))))
        self.assertEqual((a.durable_state(), len(b.calls)), (before, count + 1))

    def test_exception(self): self._step_failure(RuntimeError("boom"), "BACKEND_EXCEPTION")
    def test_missing_status(self): self._step_failure({}, "BACKEND_RECEIPT_INVALID")
    def test_unregistered_fail(self): self._step_failure({"status": "FAIL", "backend_code": "UNKNOWN"}, "BACKEND_RECEIPT_INVALID")
    def test_registered_fail(self): self._step_failure({"status": "FAIL", "backend_code": "SYNTHETIC_REJECTED"}, "BACKEND_DECLARED_FAILURE")
    def test_session_mismatch(self):
        self._step_failure({"status":"PASS","session_id":"wrong","prior_backend_state_sha256":"x","result_backend_state_sha256":"y"}, "BACKEND_SESSION_MISMATCH")
    def test_state_mismatch(self):
        self._step_failure({"status":"PASS","session_id":"candidate-session-v1","prior_backend_state_sha256":"x","result_backend_state_sha256":"y"}, "BACKEND_STATE_MISMATCH")
    def test_response_correlation_mismatch(self):
        self._step_failure({"status":"PASS","session_id":"candidate-session-v1","prior_backend_state_sha256":sha256_bytes((sha256_bytes((sha256_bytes((("0"*64)+"describe").encode())+"initialize").encode())+"reset_episode").encode()),"result_backend_state_sha256":"y","episode_id":"episode-a","request_ordinal":99}, "RESPONSE_CORRELATION_FAILURE")


class FactoryAndLawTests(unittest.TestCase):
    def test_factory_negatives(self):
        factory = AdapterFactory({"real": (lambda: SpyBackend(), "a" * 64), "synthetic": (lambda: SpyBackend(), "a" * 64)})
        base = manifest(); config = {"backend_name":"real","implementation_sha256":"a"*64,"adapter_instance_id":"a"}
        with self.assertRaisesRegex(IntegrationError, "ROLE_ARM_MISMATCH"): factory.create("peer", "candidate", b"{}", b"{}", provider)
        bad = deepcopy(config); bad["backend_name"]="missing"
        with self.assertRaisesRegex(IntegrationError, "BACKEND_NOT_REGISTERED"): factory.create("candidate","candidate",json.dumps(base).encode(),json.dumps(bad).encode(),provider)
        bad = deepcopy(config); bad["implementation_sha256"]="b"*64
        with self.assertRaisesRegex(IntegrationError, "REGISTRY_IDENTITY_MISMATCH"): factory.create("candidate","candidate",json.dumps(base).encode(),json.dumps(bad).encode(),provider)
        bad = deepcopy(config); bad["backend_name"]="synthetic"
        with self.assertRaisesRegex(IntegrationError, "SYNTHETIC_FALLBACK_FORBIDDEN"): factory.create("candidate","candidate",json.dumps(base).encode(),json.dumps(bad).encode(),provider)

    def test_held_laws_exact(self):
        rows = held_law_projection(); self.assertEqual([r["law_id"] for r in rows], ["L7","L8","L10","L14","L18"])
        self.assertEqual(rows[1]["held_reason"], "L8_PREREQUISITE_UNCLEARED")
        self.assertTrue(all(r["status"] == "HELD" and not r["claim_made"] for r in rows))
    def test_law_duplicate_missing_and_order(self):
        rows = [dict(r) for r in held_law_projection()]
        for mutation, code in ((rows + [rows[0]], "LAW_SET_DUPLICATE"), (rows[:-1], "LAW_SET_MISSING"),
                               ([rows[1],rows[0],*rows[2:]], "LAW_ORDER_MISMATCH")):
            with self.subTest(code=code), self.assertRaisesRegex(IntegrationError, code): validate_laws(mutation)


class FanoutTests(unittest.TestCase):
    def _pair(self):
        c, cb = ready("candidate"); p, pb = ready("peer"); return c, p, cb, pb
    def _req(self, context=1024): return request("fanout", episode_id="episode-a", request_ordinal=0, context_length=context, is_terminal_request=False)

    def test_positive_all_contexts_independent(self):
        for context in (1024,4096,8192):
            c,p,cb,pb=self._pair(); result=FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),context,self._req(context),c,p)
            self.assertEqual(result["status"],"PASS"); self.assertEqual((cb.calls.count("step"),pb.calls.count("step")),(1,1))

    def test_each_sanitized_negative_zero_calls_and_state(self):
        cases=[]; rows=sanitized_rows()
        cases.append((rows[:2],"SANITIZED_RESULT_MISSING_CONTEXT"))
        cases.append(([rows[0],rows[0],rows[2]],"SANITIZED_RESULT_DUPLICATE_CONTEXT"))
        cases.append(([rows[1],rows[0],rows[2]],"SANITIZED_RESULT_ORDER_MISMATCH"))
        bad=deepcopy(rows);bad[0]["length"]-=1;cases.append((bad,"SANITIZED_RESULT_LENGTH_MISMATCH"))
        bad=deepcopy(rows);bad[0]["sha256"]="0"*64;cases.append((bad,"SANITIZED_RESULT_DIGEST_MISMATCH"))
        for changed,code in cases:
            c,p,cb,pb=self._pair(); before=(c.durable_state(),p.durable_state()); counts=(len(cb.calls),len(pb.calls))
            with self.subTest(code=code),self.assertRaisesRegex(IntegrationError,code): FanoutCoordinator(provider).step(changed,stop_row(),1024,self._req(),c,p)
            self.assertEqual((c.durable_state(),p.durable_state()),before);self.assertEqual((len(cb.calls),len(pb.calls)),counts)

    def test_wrong_stop_zero_calls(self):
        c,p,cb,pb=self._pair(); bad=stop_row();bad["sha256"]="0"*64; counts=(len(cb.calls),len(pb.calls))
        with self.assertRaisesRegex(IntegrationError,"SANITIZED_STOP_DIGEST_MISMATCH"): FanoutCoordinator(provider).step(sanitized_rows(),bad,1024,self._req(),c,p)
        self.assertEqual((len(cb.calls),len(pb.calls)),counts)

    def test_rederived_stop_mismatch_zero_calls(self):
        def divergent(key): return [1, 2] if key == "stop" else provider(key)
        c,p,cb,pb=self._pair(); counts=(len(cb.calls),len(pb.calls))
        with self.assertRaisesRegex(IntegrationError,"STOP_REDERIVATION_MISMATCH"): FanoutCoordinator(divergent).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((len(cb.calls),len(pb.calls)),counts)

    def test_received_divergence_zero_calls(self):
        def project(role, length, raw): return PrivateTokenView(length, raw if role == "candidate" else raw + b"x")
        c,p,cb,pb=self._pair(); counts=(len(cb.calls),len(pb.calls))
        with self.assertRaisesRegex(IntegrationError,"FANOUT_RECEIVED_DIGEST_MISMATCH"): FanoutCoordinator(provider,project).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((len(cb.calls),len(pb.calls)),counts)

    def test_writable_view_zero_calls(self):
        def project(role, length, raw): return PrivateTokenView(length, bytearray(raw))
        c,p,cb,pb=self._pair(); counts=(len(cb.calls),len(pb.calls))
        with self.assertRaisesRegex(IntegrationError,"PRIVATE_VIEW_MUTATION_ATTEMPT"): FanoutCoordinator(provider,project).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((len(cb.calls),len(pb.calls)),counts)

    def test_precall_mutation_evidence_zero_calls(self):
        c,p,cb,pb=self._pair(); counts=(len(cb.calls),len(pb.calls))
        with self.assertRaisesRegex(IntegrationError,"PRIVATE_VIEW_MUTATED"): FanoutCoordinator(provider,mutation_probe=lambda view: True).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((len(cb.calls),len(pb.calls)),counts)

    def test_candidate_failure_one_zero_and_no_commit(self):
        c,cb=ready("candidate",SpyBackend("candidate-session-v1",{"step":RuntimeError("x")}));p,pb=ready("peer")
        before=(c.durable_state(),p.durable_state())
        with self.assertRaisesRegex(IntegrationError,"BACKEND_EXCEPTION"): FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((cb.calls.count("step"),pb.calls.count("step")),(1,0));self.assertEqual((c.durable_state(),p.durable_state()),before)

    def test_peer_failure_one_one_atomic_restore(self):
        c,cb=ready("candidate");p,pb=ready("peer",SpyBackend("peer-session-v1",{"step":RuntimeError("x")}));before=(c.durable_state(),p.durable_state())
        with self.assertRaisesRegex(IntegrationError,"FANOUT_ATOMICITY_FAILURE"): FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((cb.calls.count("step"),pb.calls.count("step")),(1,1));self.assertEqual((c.durable_state(),p.durable_state()),before)


if __name__ == "__main__":
    unittest.main()
