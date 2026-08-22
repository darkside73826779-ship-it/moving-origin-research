"""Production-entrypoint tests for the M4 post-tokenizer integration seam."""

from __future__ import annotations

import json
import threading
import unittest
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

import src.m4_post_tokenizer_integration as seam

from src.m4_post_tokenizer_integration import (
    AdapterFactory, CandidateAdapter, ControlAdapter, FanoutCoordinator, IntegrationError,
    PeerAdapter, PrivateTokenView, encode_private_view, held_law_projection,
    realize_launch_command, sha256_bytes, validate_laws, validate_pair_identity, validate_state,
    SyntheticFixtureDispatcher,
    LAW_ALLOWED_FAILURES, LAW_FAILURE_EVIDENCE, LAW_METRIC_SCHEMAS,
    LAW_NOT_RUN_EVIDENCE, LAW_REQUIRED_EVIDENCE,
)

ROOT = Path(__file__).resolve().parents[1]


def provider(key):
    if key == "stop":
        return [900000, 900017]
    return [((key * 17) + i * 31) % 32749 for i in range(key)]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def thaw(value):
    if isinstance(value, dict) or hasattr(value, "items"): return {k:thaw(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [thaw(v) for v in value]
    return value


class SpyBackend:
    def __init__(self, session="candidate-session-v1", behavior=None, restore_behavior="exact"):
        self.session, self.behavior, self.calls = session, behavior or {}, []
        self.restore_behavior = restore_behavior
        self.real_state = {"generation": 0, "payload": [], "live": True}

    def capture_state(self): return deepcopy(self.real_state)
    def restore_state(self, snapshot):
        if self.restore_behavior == "throw": raise RuntimeError("restore")
        if self.restore_behavior == "noop": return
        if self.restore_behavior == "partial": self.real_state["generation"] = snapshot["generation"]; return
        if self.restore_behavior == "wrong": self.real_state = {"generation": -1, "payload": ["wrong"], "live": True}; return
        self.real_state = deepcopy(snapshot)
    def session_identity(self): return self.session
    def dispose(self): self.real_state["live"] = False
    def is_live(self): return self.real_state["live"]

    def _receipt(self, operation, prior, request=None):
        self.calls.append(operation)
        action = self.behavior.get(operation)
        if isinstance(action, Exception): raise action
        self.real_state["generation"] += 1; self.real_state["payload"].append(operation)
        request = dict(request or request_fn(operation))
        receipt = {"status": "PASS", "backend_code": None, "session_id": self.session,
                   "prior_backend_state_sha256": prior,
                   "result_backend_state_sha256": sha256_bytes((prior + operation).encode()),
                   "request_sha256": sha256_bytes(json.dumps(request,sort_keys=True,separators=(",", ":")).encode()),
                   "request_ordinal": request.get("request_ordinal") if operation == "step" else None}
        if callable(action): return deepcopy(action(deepcopy(receipt)))
        if action is not None: return deepcopy(action)
        return receipt

    def describe(self, manifest, config, request): return self._receipt("describe", "0" * 64, request)
    def initialize(self, description, session, request):
        prior = sha256_bytes((("0" * 64) + "describe").encode())
        return self._receipt("initialize", prior, request)
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
    if "request_ordinal" in kwargs and "is_terminal_request" not in kwargs: kwargs["is_terminal_request"] = False
    return {"operation_id": operation_id, "caller_session_id": "caller-main",
            "caller_thread_id": "thread-0", **kwargs}


def request_fn(operation):
    return request(operation)


def initialized(role="candidate", backend=None):
    a, b = adapter(role, backend)
    a.describe(request("describe")); a.initialize(request("initialize"))
    return a, b


def ready(role="candidate", backend=None, episode="episode-a"):
    a, b = initialized(role, backend)
    a.reset_episode(request("reset", episode_id=episode, reset_ordinal=1))
    return a, b


def sanitized_rows():
    rows = []
    for n in (1024, 4096, 8192):
        digest = sha256_bytes(encode_private_view(provider(n)))
        rows.append({"context_length": n, "length": n, "sha256": digest, "expected_sha256": digest})
    return rows


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
        before, backend_before, count = a.durable_state(), b.capture_state(), len(b.calls)
        with self.assertRaisesRegex(IntegrationError, code):
            a.step(request("s", episode_id="episode-a", request_ordinal=0, context_length=1024), PrivateTokenView(1024, encode_private_view(provider(1024))))
        self.assertEqual((a.durable_state(), b.capture_state(), len(b.calls)), (before, backend_before, count + 1))

    def test_exception(self): self._step_failure(RuntimeError("boom"), "BACKEND_EXCEPTION")
    def test_missing_status(self): self._step_failure(lambda r: {k:v for k,v in r.items() if k != "status"}, "BACKEND_RECEIPT_INVALID")
    def test_unregistered_fail(self): self._step_failure(lambda r: {**r,"status":"FAIL","backend_code":"UNKNOWN"}, "BACKEND_RECEIPT_INVALID")
    def test_registered_fail(self): self._step_failure(lambda r: {**r,"status":"FAIL","backend_code":"SYNTHETIC_REJECTED"}, "BACKEND_DECLARED_FAILURE")
    def test_session_mismatch(self): self._step_failure(lambda r: {**r,"session_id":"wrong"}, "BACKEND_SESSION_MISMATCH")
    def test_state_mismatch(self): self._step_failure(lambda r: {**r,"prior_backend_state_sha256":"a"*64}, "BACKEND_STATE_MISMATCH")
    def test_response_correlation_mismatch(self): self._step_failure(lambda r: {**r,"request_ordinal":99}, "RESPONSE_CORRELATION_FAILURE")


class FactoryAndLawTests(unittest.TestCase):
    def test_factory_negatives(self):
        base = manifest(); config = {"backend_name":"real","implementation_sha256":"a"*64,
            "dependency_sha256":"b"*64,"model_sha256":base["checkpoint_sha256"],
            "tokenizer_sha256":base["tokenizer_sha256"],"adapter_instance_id":"a","production_path":True}
        factory = AdapterFactory({"real": (lambda: SpyBackend(), "a" * 64, "b" * 64, sha256_bytes(canonical(config))),
                                  "synthetic": (lambda: SpyBackend(), "a" * 64, "b" * 64, sha256_bytes(canonical(config)))})
        with self.assertRaisesRegex(IntegrationError, "ROLE_ARM_MISMATCH"): factory.create("peer", "candidate", b"{}", b"{}", provider)
        bad = deepcopy(config); bad["backend_name"]="missing"
        with self.assertRaisesRegex(IntegrationError, "BACKEND_NOT_REGISTERED"): factory.create("candidate","candidate",canonical(base),canonical(bad),provider)
        bad = deepcopy(config); bad["implementation_sha256"]="b"*64
        with self.assertRaisesRegex(IntegrationError, "REGISTRY_IDENTITY_MISMATCH"): factory.create("candidate","candidate",canonical(base),canonical(bad),provider)
        bad = deepcopy(config); bad["backend_name"]="synthetic"
        with self.assertRaisesRegex(IntegrationError, "SYNTHETIC_FALLBACK_FORBIDDEN"): factory.create("candidate","candidate",canonical(base),canonical(bad),provider)

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
        c,cb=ready("candidate");p,pb=ready("peer",SpyBackend("peer-session-v1",{"step":RuntimeError("x")}));before=(c.durable_state(),p.durable_state(),cb.capture_state(),pb.capture_state())
        with self.assertRaisesRegex(IntegrationError,"FANOUT_ATOMICITY_FAILURE"): FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((cb.calls.count("step"),pb.calls.count("step")),(1,1));self.assertEqual((c.durable_state(),p.durable_state(),cb.capture_state(),pb.capture_state()),before)

    def test_post_return_failure_restores_both_real_backends(self):
        c,p,cb,pb=self._pair();before=(c.durable_state(),p.durable_state(),cb.capture_state(),pb.capture_state())
        with self.assertRaisesRegex(IntegrationError,"PRIVATE_VIEW_MUTATED"):
            FanoutCoordinator(provider,post_return_probe=lambda _c,_p:True).step(sanitized_rows(),stop_row(),1024,self._req(),c,p)
        self.assertEqual((c.durable_state(),p.durable_state(),cb.capture_state(),pb.capture_state()),before)
        self.assertEqual((cb.calls.count("step"),pb.calls.count("step")),(1,1))


class RemediationProductionTests(unittest.TestCase):
    def test_launch_contract_realizes_exact_read_only_bind_before_process(self):
        contract=json.loads((ROOT/"specs/data/m4_post_tokenizer_integration_oci_launch_contract_v1.json").read_text())
        tokens=realize_launch_command(contract,str(ROOT.resolve()))
        self.assertIn(f"type=bind,src={ROOT.resolve()},dst=/workspace,readonly",tokens)
        self.assertEqual(tokens[0:2],("docker","run"));self.assertIn("--network",tokens);self.assertIn("none",tokens)
        for bad in ("", "relative", str(ROOT.resolve())+",bad"):
            with self.assertRaisesRegex(IntegrationError,"RELEASED_CHECKOUT_INVALID"):realize_launch_command(contract,bad)
        bad=deepcopy(contract);bad["command_tokens"]=[t.replace("${MOR_RELEASED_CHECKOUT}","") for t in bad["command_tokens"]]
        with self.assertRaisesRegex(IntegrationError,"LAUNCH_CONTRACT_INVALID"):realize_launch_command(bad,str(ROOT.resolve()))

    def _factory_pair(self):
        cman, pman = manifest("candidate"), manifest("peer")
        def cfg(name, man): return {"backend_name":name,"implementation_sha256":"a"*64,
            "dependency_sha256":"b"*64,"model_sha256":man["checkpoint_sha256"],
            "tokenizer_sha256":man["tokenizer_sha256"],"adapter_instance_id":name,"production_path":True}
        ccfg, pcfg = cfg("candidate-real", cman), cfg("peer-real", pman)
        registry = {
            "candidate-real": (lambda: SpyBackend("candidate-session-v1"),"a"*64,"b"*64,sha256_bytes(canonical(ccfg))),
            "peer-real": (lambda: SpyBackend("peer-session-v1"),"a"*64,"b"*64,sha256_bytes(canonical(pcfg))),
        }
        return AdapterFactory(registry).create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(pcfg),provider)

    def test_coupled_factory_canonical_config_dependency_and_pair(self):
        c, p = self._factory_pair(); self.assertIsInstance(c, CandidateAdapter); self.assertIsInstance(p, PeerAdapter)
        cman, pman = manifest("candidate"), manifest("peer")
        cfg = {"backend_name":"candidate-real","implementation_sha256":"a"*64,"dependency_sha256":"b"*64,
               "model_sha256":cman["checkpoint_sha256"],"tokenizer_sha256":cman["tokenizer_sha256"],
               "adapter_instance_id":"candidate-real","production_path":True}
        registry={"candidate-real":(lambda:SpyBackend(),"a"*64,"b"*64,sha256_bytes(canonical(cfg)))}
        factory=AdapterFactory(registry)
        for bad_manifest,bad_config in ((json.dumps(cman).encode(),canonical(cfg)),
                                        (canonical(cman),json.dumps(cfg).encode()),
                                        (canonical({**cman,"tokenizer_sha256":"0"*64}),canonical(cfg)),
                                        (canonical(cman),canonical({**cfg,"dependency_sha256":"c"*64}))):
            with self.subTest(),self.assertRaises(IntegrationError): factory.create("candidate","candidate",bad_manifest,bad_config,provider)
        bad_peer=deepcopy(pman); bad_peer["checkpoint_sha256"]="0"*64
        pcfg={**cfg,"backend_name":"peer-real","adapter_instance_id":"peer-real","model_sha256":bad_peer["checkpoint_sha256"]}
        both=AdapterFactory({**registry,"peer-real":(lambda:SpyBackend("peer-session-v1"),"a"*64,"b"*64,sha256_bytes(canonical(pcfg)))})
        with self.assertRaisesRegex(IntegrationError,"PAIR_IDENTITY_MISMATCH"):
            both.create_pair(canonical(cman),canonical(bad_peer),canonical(cfg),canonical(pcfg),provider)

    def test_complete_request_validation_precedes_every_backend_call(self):
        operations = (
            (lambda a,r:a.describe(r), request("d")),
            (lambda a,r:a.initialize(r), request("i")),
            (lambda a,r:a.reset_episode(r), request("r",episode_id="episode-a",reset_ordinal=1)),
        )
        for invoke, good in operations:
            for field in tuple(good):
                a,b=adapter();
                if good["operation_id"]!="d": a.describe(request("d"))
                if good["operation_id"]=="r": a.initialize(request("i"))
                bad=deepcopy(good); bad.pop(field)
                with self.subTest(operation=good["operation_id"],field=field),self.assertRaisesRegex(IntegrationError,"REQUEST_STRUCTURE_INVALID"):
                    invoke(a,bad)
                self.assertNotIn(good["operation_id"],b.calls)
        a,b=ready(); good=request("s",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False)
        for field in good:
            bad=deepcopy(good);bad.pop(field);before=len(b.calls)
            with self.subTest(field=field),self.assertRaisesRegex(IntegrationError,"REQUEST_STRUCTURE_INVALID"):
                a.step(bad,PrivateTokenView(1024,encode_private_view(provider(1024))))
            self.assertEqual(len(b.calls),before)

    def test_exact_receipt_shape_type_digest_and_correlation_mutations(self):
        mutations = {
            "omit":lambda r:{k:v for k,v in r.items() if k!="request_sha256"},
            "extra":lambda r:{**r,"extra":1}, "status_type":lambda r:{**r,"status":True},
            "backend_code":lambda r:{**r,"backend_code":"SYNTHETIC_REJECTED"},
            "token_length":lambda r:{**r,"result_backend_state_sha256":"a"*63},
            "ordinal_type":lambda r:{**r,"request_ordinal":False},
            "request_digest":lambda r:{**r,"request_sha256":"0"*64},
        }
        for name,mutation in mutations.items():
            b=SpyBackend("candidate-session-v1",{"step":mutation});a,_=ready(backend=b);before=(a.durable_state(),b.capture_state())
            expected="RESPONSE_CORRELATION_FAILURE" if name=="request_digest" else "BACKEND_RECEIPT_INVALID"
            with self.subTest(name=name),self.assertRaisesRegex(IntegrationError,expected):
                a.step(request("s",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False),PrivateTokenView(1024,encode_private_view(provider(1024))))
            self.assertEqual((a.durable_state(),b.capture_state()),before)

    def test_fixture_is_parsed_and_every_declared_row_and_sequence_executes(self):
        fixture=json.loads((ROOT/"specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json").read_text())
        self.assertEqual(fixture["sequence"],["reconcile_ordered_sanitized_result","verify_private_token_digests","fanout_episode_a_request_0","fanout_episode_a_request_1","exercise_close_paths","reset_episode_b","fanout_episode_b_request_0","validate_exact_ordered_law_set"])
        c,p=self._factory_pair()
        for a in (c,p): a.describe(request("d"));a.initialize(request("i"));a.reset_episode(request("r",episode_id="synthetic-episode-a",reset_ordinal=1))
        fan=FanoutCoordinator(provider)
        fan.step(sanitized_rows(),stop_row(),1024,request("a0",episode_id="synthetic-episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False),c,p)
        fan.step(sanitized_rows(),stop_row(),4096,request("a1",episode_id="synthetic-episode-a",request_ordinal=1,context_length=4096,is_terminal_request=True),c,p)
        for a in (c,p): a.reset_episode(request("rb",episode_id="synthetic-episode-b",reset_ordinal=2))
        receipt=fan.step(sanitized_rows(),stop_row(),8192,request("b0",episode_id="synthetic-episode-b",request_ordinal=0,context_length=8192,is_terminal_request=True),c,p)
        self.assertEqual((c.backend.calls.count("step"),p.backend.calls.count("step")),(3,3));self.assertTrue(receipt["equal"])
        executed={
            "tampered_private_rederivation":"TOKEN_ARRAY_DIGEST_MISMATCH","duplicate_or_skipped_ordinal":"REQUEST_ORDINAL_MISMATCH",
            "missing_sanitized_context":"SANITIZED_RESULT_MISSING_CONTEXT","duplicate_sanitized_context":"SANITIZED_RESULT_DUPLICATE_CONTEXT",
            "reordered_sanitized_context":"SANITIZED_RESULT_ORDER_MISMATCH","wrong_sanitized_length":"SANITIZED_RESULT_LENGTH_MISMATCH",
            "wrong_sanitized_digest":"SANITIZED_RESULT_DIGEST_MISMATCH","wrong_stop_digest":"SANITIZED_STOP_DIGEST_MISMATCH",
            "created_closed_true":"STATE_SEMANTIC_FAILURE","duplicate_l7":"LAW_SET_DUPLICATE","missing_l18":"LAW_SET_MISSING",
            "reordered_laws":"LAW_ORDER_MISMATCH","invalid_transition_after_close":"ADAPTER_LIFECYCLE_VIOLATION"}
        self.assertEqual({r["id"]:r["expected_code"] for r in fixture["negative_cases"]},executed)
        realized=set()
        def fan_case(case_id, code, rows=None, stop=None, supplied_provider=provider):
            ca,pa,_,_=FanoutTests()._pair()
            with self.assertRaisesRegex(IntegrationError,code):
                FanoutCoordinator(supplied_provider).step(rows or sanitized_rows(),stop or stop_row(),1024,FanoutTests()._req(),ca,pa)
            realized.add(case_id)
        def altered_prompt(key): return ([1]*key) if key != "stop" else provider(key)
        fan_case("tampered_private_rederivation","TOKEN_ARRAY_DIGEST_MISMATCH",supplied_provider=altered_prompt)
        rows=sanitized_rows();fan_case("missing_sanitized_context","SANITIZED_RESULT_MISSING_CONTEXT",rows=rows[:2])
        fan_case("duplicate_sanitized_context","SANITIZED_RESULT_DUPLICATE_CONTEXT",rows=[rows[0],rows[0],rows[2]])
        fan_case("reordered_sanitized_context","SANITIZED_RESULT_ORDER_MISMATCH",rows=[rows[1],rows[0],rows[2]])
        bad=deepcopy(rows);bad[0]["length"]-=1;fan_case("wrong_sanitized_length","SANITIZED_RESULT_LENGTH_MISMATCH",rows=bad)
        bad=deepcopy(rows);bad[0]["sha256"]="0"*64;fan_case("wrong_sanitized_digest","SANITIZED_RESULT_DIGEST_MISMATCH",rows=bad)
        bad=stop_row();bad["sha256"]="0"*64;fan_case("wrong_stop_digest","SANITIZED_STOP_DIGEST_MISMATCH",stop=bad)
        a,b=ready();a.step(request("s",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False),PrivateTokenView(1024,encode_private_view(provider(1024))))
        with self.assertRaisesRegex(IntegrationError,"REQUEST_ORDINAL_MISMATCH"):
            a.step(request("dup",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False),PrivateTokenView(1024,encode_private_view(provider(1024))))
        realized.add("duplicate_or_skipped_ordinal")
        state=json.loads(a.durable_state());state.update(lifecycle_state="CREATED",closed=True,episode_id=None)
        with self.assertRaisesRegex(IntegrationError,"STATE_SEMANTIC_FAILURE"):validate_state(state)
        realized.add("created_closed_true")
        laws=[dict(r) for r in held_law_projection()]
        for case_id,mutation,code in (("duplicate_l7",laws+[laws[0]],"LAW_SET_DUPLICATE"),("missing_l18",laws[:-1],"LAW_SET_MISSING"),("reordered_laws",[laws[1],laws[0],*laws[2:]],"LAW_ORDER_MISMATCH")):
            with self.assertRaisesRegex(IntegrationError,code):validate_laws(mutation)
            realized.add(case_id)
        closed,_=initialized();closed.close(request("close"))
        with self.assertRaisesRegex(IntegrationError,"ADAPTER_LIFECYCLE_VIOLATION"):closed.describe(request("again"))
        realized.add("invalid_transition_after_close")
        self.assertEqual(realized,set(executed))

    def test_stop_identity_unsupported_context_and_complete_receipt(self):
        c,p,_,_=FanoutTests()._pair();req=FanoutTests()._req()
        for bad,code in (({"sha256":stop_row()["sha256"],"expected_sha256":stop_row()["sha256"]},"SANITIZED_STOP_IDENTITY_INVALID"),
                         ({**stop_row(),"length":3},"SANITIZED_STOP_LENGTH_MISMATCH")):
            with self.subTest(code=code),self.assertRaisesRegex(IntegrationError,code): FanoutCoordinator(provider).step(sanitized_rows(),bad,1024,req,c,p)
        with self.assertRaisesRegex(IntegrationError,"UNSUPPORTED_CONTEXT_LENGTH"):
            FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),2048,{**req,"context_length":2048},c,p)
        c,p,_,_=FanoutTests()._pair();out=FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),1024,req,c,p)
        self.assertEqual(set(out),{"status","context_id","context_length","length","expected_sha256","candidate_sha256","peer_sha256","equal","runtime_instance_ids","request_sha256","stop_length","stop_sha256","candidate","peer","laws"})

    def test_law_all_status_semantics_and_field_mutations(self):
        held=thaw(held_law_projection())
        for index,base in enumerate(held):
            law=base["law_id"]
            for status in ("HELD","PASS","FAIL","NOT_RUN"):
                rows=deepcopy(held);row=rows[index]
                if status=="PASS":
                    metrics={key:(True if kind is bool else 6 if key=="arms_present" else 3 if kind is int else 0.5)
                             for key,kind in LAW_METRIC_SCHEMAS[law].items()}
                    row.update(status=status,claim_made=True,evidence=list(LAW_REQUIRED_EVIDENCE[law]),metrics=metrics,failure_code=None,held_reason=None)
                elif status=="FAIL":
                    row.update(status=status,claim_made=False,evidence=list(LAW_FAILURE_EVIDENCE[law]),metrics={},
                               failure_code=sorted(LAW_ALLOWED_FAILURES[law])[0],held_reason=None)
                elif status=="NOT_RUN":
                    row.update(status=status,claim_made=False,evidence=list(LAW_NOT_RUN_EVIDENCE[law]),metrics={},
                               failure_code=f"INSTRUMENT_FAILURE:{law}",held_reason=None)
                if status == "PASS":
                    with self.assertRaisesRegex(IntegrationError,"LAW_PASS_UNAVAILABLE"): validate_laws(rows)
                else:
                    validate_laws(rows)
                mutations={"meaning_source":"wrong","claim_made":not row["claim_made"],"evidence":["wrong"],
                           "metrics":{"extra":1},"failure_code":"WRONG","held_reason":"WRONG","status":"UNKNOWN"}
                for field,value in mutations.items():
                    bad=deepcopy(rows);bad[index][field]=value
                    with self.subTest(law=law,status=status,field=field),self.assertRaises(IntegrationError):validate_laws(bad)
                for field in tuple(row):
                    bad=deepcopy(rows);bad[index].pop(field)
                    with self.subTest(law=law,status=status,missing=field),self.assertRaises(IntegrationError):validate_laws(bad)
                bad=deepcopy(rows);bad[index]["extra"]=1
                with self.subTest(law=law,status=status,extra=True),self.assertRaisesRegex(IntegrationError,"LAW_PROJECTION_INVALID"):validate_laws(bad)
                if status=="PASS":
                    for metric,kind in LAW_METRIC_SCHEMAS[law].items():
                        bad=deepcopy(rows);bad[index]["metrics"][metric]=False if kind is not bool else 1
                        with self.subTest(law=law,metric=metric),self.assertRaisesRegex(IntegrationError,"LAW_PROJECTION_INVALID"):validate_laws(bad)
                        if kind is float:
                            bad=deepcopy(rows);bad[index]["metrics"][metric]=float("nan")
                            with self.subTest(law=law,metric=metric,nonfinite=True),self.assertRaisesRegex(IntegrationError,"LAW_PROJECTION_INVALID"):validate_laws(bad)


class RereviewRemediationTests(unittest.TestCase):
    @staticmethod
    def _pair_specs(candidate_ctor, peer_ctor, candidate_session="candidate-session-v1", peer_session="peer-session-v1"):
        cman,pman=manifest("candidate"),manifest("peer")
        def cfg(name,man):return {"backend_name":name,"implementation_sha256":"a"*64,"dependency_sha256":"b"*64,
            "model_sha256":man["checkpoint_sha256"],"tokenizer_sha256":man["tokenizer_sha256"],
            "adapter_instance_id":name,"production_path":True}
        ccfg,pcfg=cfg("candidate-real",cman),cfg("peer-real",pman)
        registry={"candidate-real":(candidate_ctor,"a"*64,"b"*64,sha256_bytes(canonical(ccfg))),
                  "peer-real":(peer_ctor,"a"*64,"b"*64,sha256_bytes(canonical(pcfg)))}
        return AdapterFactory(registry),cman,pman,ccfg,pcfg

    def test_pair_prevalidation_second_half_cleanup_session_binding_and_specific_codes(self):
        made=[]
        def ctor(session):
            def build():
                backend=SpyBackend(session);made.append(backend);return backend
            return build
        factory,cman,pman,ccfg,pcfg=self._pair_specs(ctor("candidate-session-v1"),ctor("peer-session-v1"))
        bad=deepcopy(pcfg);bad["dependency_sha256"]="c"*64
        with self.assertRaisesRegex(IntegrationError,"REGISTRY_IDENTITY_MISMATCH"):
            factory.create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(bad),provider)
        self.assertEqual(made,[])
        badman=deepcopy(pman);badman["checkpoint_sha256"]="0"*64
        badcfg={**pcfg,"model_sha256":"0"*64}
        pair_factory,_,_,_,_=self._pair_specs(ctor("candidate-session-v1"),ctor("peer-session-v1"))
        pair_factory._registry["peer-real"]=(ctor("peer-session-v1"),"a"*64,"b"*64,sha256_bytes(canonical(badcfg)))
        with self.assertRaisesRegex(IntegrationError,"PAIR_IDENTITY_MISMATCH"):
            pair_factory.create_pair(canonical(cman),canonical(badman),canonical(ccfg),canonical(badcfg),provider)
        self.assertEqual(made,[])
        role=deepcopy(pman);role["role"]="candidate"
        with self.assertRaisesRegex(IntegrationError,"ROLE_ARM_MISMATCH"):
            factory.create_pair(canonical(cman),canonical(role),canonical(ccfg),canonical(pcfg),provider)
        channel=deepcopy(pman);channel["channel_policy"]="FULL_AUTHORIZED"
        with self.assertRaisesRegex(IntegrationError,"PEER_CHANNEL_BYPASS"):
            factory.create_pair(canonical(cman),canonical(channel),canonical(ccfg),canonical(pcfg),provider)
        made.clear()
        def peer_raises(): raise RuntimeError("constructor")
        factory,_,_,ccfg,pcfg=self._pair_specs(ctor("candidate-session-v1"),peer_raises)
        with self.assertRaisesRegex(RuntimeError,"constructor"):
            factory.create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(pcfg),provider)
        self.assertEqual(len(made),1);self.assertFalse(made[0].is_live())
        made.clear()
        factory,_,_,ccfg,pcfg=self._pair_specs(ctor("candidate-session-v1"),ctor("wrong-session"))
        with self.assertRaisesRegex(IntegrationError,"BACKEND_SESSION_MISMATCH"):
            factory.create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(pcfg),provider)
        self.assertEqual(len(made),2);self.assertTrue(all(not backend.is_live() for backend in made))

    def test_state_machine_cross_field_mutations_and_public_prestate_gate(self):
        base=json.loads(adapter()[0].durable_state())
        mutations=[]
        for change in ({"lifecycle_state":"UNKNOWN"},{"closed":True},{"episode_id":"x"},{"episode_complete":True},
                       {"reset_ordinal":1},{"next_request_ordinal":1},{"snapshot_ordinal":1},{"last_response_sha256":"a"*64}):
            mutations.append({**base,**change})
        ready_state={**base,"lifecycle_state":"EPISODE_READY","episode_id":"x","reset_ordinal":1}
        for change in ({"episode_id":None},{"episode_complete":True},{"reset_ordinal":0},{"next_request_ordinal":1},{"last_response_sha256":"a"*64}):
            mutations.append({**ready_state,**change})
        stepped={**ready_state,"lifecycle_state":"STEPPED","next_request_ordinal":1,"last_response_sha256":"a"*64}
        for change in ({"next_request_ordinal":0},{"last_response_sha256":None},{"last_response_sha256":"bad"}):
            mutations.append({**stepped,**change})
        mutations.extend(({**base,"lifecycle_state":"CLOSED","closed":False},
                          {**base,"lifecycle_state":"CLOSED","closed":True,"episode_complete":True}))
        for ordinal,state in enumerate(mutations):
            with self.subTest(ordinal=ordinal),self.assertRaisesRegex(IntegrationError,"STATE_SEMANTIC_FAILURE"):validate_state(state)
        fixtures=[]
        a,b=adapter();fixtures.append((a,b,lambda x:x.describe(request("d"))))
        a,b=adapter();a.describe(request("d"));fixtures.append((a,b,lambda x:x.initialize(request("i"))))
        a,b=initialized();fixtures.append((a,b,lambda x:x.reset_episode(request("r",episode_id="x",reset_ordinal=1))))
        a,b=ready();fixtures.append((a,b,lambda x:x.step(request("s",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False),PrivateTokenView(1024,encode_private_view(provider(1024))))))
        a,b=ready();a.step(request("s",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False),PrivateTokenView(1024,encode_private_view(provider(1024))));fixtures.append((a,b,lambda x:x.snapshot(request("p",snapshot_ordinal=0))))
        for a,b,invoke in fixtures:
            a._state["closed"]=True;before=len(b.calls)
            with self.assertRaisesRegex(IntegrationError,"STATE_SEMANTIC_FAILURE"):invoke(a)
            self.assertEqual(len(b.calls),before)
        a,_=adapter();bad=a.capture();bad[0]["closed"]=True
        with self.assertRaisesRegex(IntegrationError,"STATE_SEMANTIC_FAILURE"):a.restore(bad)
        a,b=adapter();before=(a.durable_state(),b.capture_state())
        def reject_post(state):
            validate_state(state)
            if state["lifecycle_state"]=="DESCRIBED":raise IntegrationError("STATE_SEMANTIC_FAILURE")
        with patch("src.m4_post_tokenizer_integration.validate_state",side_effect=reject_post):
            with self.assertRaisesRegex(IntegrationError,"STATE_SEMANTIC_FAILURE"):a.describe(request("post-kill"))
        self.assertEqual((a.durable_state(),b.capture_state()),before)

    def test_rollback_identity_rejects_noop_partial_wrong_and_throwing_restorers_all_routes(self):
        modes=("noop","partial","wrong","throw")
        def raised(_receipt): raise RuntimeError("after-mutation")
        for mode in modes:
            routes=[]
            cb=SpyBackend("candidate-session-v1",{"step":lambda r:{**r,"extra":1}},mode);c,_=ready("candidate",cb);p,_=ready("peer")
            routes.append(lambda c=c,p=p:FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),1024,FanoutTests()._req(),c,p))
            cb=SpyBackend("candidate-session-v1",{"step":raised},mode);c,_=ready("candidate",cb);p,_=ready("peer")
            routes.append(lambda c=c,p=p:FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),1024,FanoutTests()._req(),c,p))
            c,_=ready("candidate");pb=SpyBackend("peer-session-v1",{"step":lambda r:{**r,"extra":1}},mode);p,_=ready("peer",pb)
            routes.append(lambda c=c,p=p:FanoutCoordinator(provider).step(sanitized_rows(),stop_row(),1024,FanoutTests()._req(),c,p))
            cb=SpyBackend("candidate-session-v1",restore_behavior=mode);c,_=ready("candidate",cb);p,_=ready("peer")
            routes.append(lambda c=c,p=p:FanoutCoordinator(provider,post_return_probe=lambda _c,_p:True).step(sanitized_rows(),stop_row(),1024,FanoutTests()._req(),c,p))
            for ordinal,route in enumerate(routes):
                with self.subTest(mode=mode,route=ordinal),self.assertRaisesRegex(IntegrationError,"BACKEND_ROLLBACK_FAILURE"):route()

    def test_exact_fixture_dispatch_and_all_negative_boundaries(self):
        fixture=json.loads((ROOT/"specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json").read_text())
        c,p=RemediationProductionTests()._factory_pair()
        for a in (c,p):a.describe(request("d"));a.initialize(request("i"));a.reset_episode(request("r",episode_id="synthetic-episode-a",reset_ordinal=1))
        ci,_=initialized();cr,_=ready("peer")
        control_manifest=manifest("candidate");control_manifest.update(role="control",scientific_arm="empty",runtime_instance_id="control-session-v1",
            access_policy_id="control-empty-v1",channel_policy="EMPTY_CONTROL",redaction_receipt_sha256="0"*64)
        cs=ControlAdapter("control","empty",control_manifest,{"adapter_instance_id":"control-adapter"},provider,SpyBackend("control-session-v1"))
        cs.describe(request("cd"));cs.initialize(request("ci"));cs.reset_episode(request("cr",episode_id="episode-a",reset_ordinal=1))
        cs.step(request("cs",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=False),PrivateTokenView(1024,encode_private_view(provider(1024))))
        dispatcher=SyntheticFixtureDispatcher(FanoutCoordinator(provider))
        trace=dispatcher.dispatch(fixture,sanitized_rows(),stop_row(),c,p,{"INITIALIZED":ci,"EPISODE_READY":cr,"STEPPED":cs},
                                  lambda:{"candidate":c.backend.calls.count("step"),"peer":p.backend.calls.count("step")})
        self.assertEqual(thaw(trace["sequence"]),fixture["sequence"]);self.assertEqual(thaw(trace["expected"]),fixture["expected"])
        self.assertEqual([row["role"] for row in trace["close_call_trace"]],["candidate","peer","control"])
        realized=[]
        for row in fixture["negative_cases"]:
            ca,pa,cb,pb=FanoutTests()._pair();rows=sanitized_rows();stop=stop_row();fan=FanoutCoordinator(provider);req=FanoutTests()._req()
            if row["id"]=="tampered_private_rederivation": fan=FanoutCoordinator(lambda key:([1]*key if key!="stop" else provider(key)));action=lambda:fan.step(rows,stop,1024,req,ca,pa)
            elif row["id"]=="duplicate_or_skipped_ordinal":
                ca.step(req,PrivateTokenView(1024,encode_private_view(provider(1024))));action=lambda:ca.step(req,PrivateTokenView(1024,encode_private_view(provider(1024))))
            elif row["id"]=="missing_sanitized_context": action=lambda:fan.step(rows[:2],stop,1024,req,ca,pa)
            elif row["id"]=="duplicate_sanitized_context": action=lambda:fan.step([rows[0],rows[0],rows[2]],stop,1024,req,ca,pa)
            elif row["id"]=="reordered_sanitized_context": action=lambda:fan.step([rows[1],rows[0],rows[2]],stop,1024,req,ca,pa)
            elif row["id"]=="wrong_sanitized_length": bad=deepcopy(rows);bad[0]["length"]-=1;action=lambda bad=bad:fan.step(bad,stop,1024,req,ca,pa)
            elif row["id"]=="wrong_sanitized_digest": bad=deepcopy(rows);bad[0]["sha256"]="0"*64;action=lambda bad=bad:fan.step(bad,stop,1024,req,ca,pa)
            elif row["id"]=="wrong_stop_digest": bad=deepcopy(stop);bad["sha256"]="0"*64;action=lambda bad=bad:fan.step(rows,bad,1024,req,ca,pa)
            elif row["id"]=="created_closed_true": bad=json.loads(adapter()[0].durable_state());bad["closed"]=True;action=lambda bad=bad:validate_state(bad)
            elif row["id"] in ("duplicate_l7","missing_l18","reordered_laws"):
                laws=[dict(x) for x in held_law_projection()];bad=laws+[laws[0]] if row["id"]=="duplicate_l7" else laws[:-1] if row["id"]=="missing_l18" else [laws[1],laws[0],*laws[2:]];action=lambda bad=bad:validate_laws(bad)
            else:
                closed,_=initialized();closed.close(request("close"));action=lambda:closed.describe(request("again"))
            identity=lambda:sha256_bytes(canonical({"candidate":json.loads(ca.durable_state()),"peer":json.loads(pa.durable_state()),"cb":cb.capture_state(),"pb":pb.capture_state()}))
            realized.append(thaw(dispatcher.realize_negative(row,action,lambda:len(cb.calls)+len(pb.calls),identity)))
        self.assertEqual([item["id"] for item in realized],[row["id"] for row in fixture["negative_cases"]])

    def test_frozen_phase_one_evidence_prevents_nondeterministic_provider_reread(self):
        counts={1024:0,"stop":0}
        def nondeterministic(key):
            if key in counts:counts[key]+=1
            if key==1024 and counts[key]>1:raise AssertionError("private prompt reread")
            if key=="stop" and counts[key]>1:raise AssertionError("private stop reread")
            return provider(key)
        c,p,_,_=FanoutTests()._pair();receipt=FanoutCoordinator(nondeterministic).step(sanitized_rows(),stop_row(),1024,FanoutTests()._req(),c,p)
        self.assertEqual(counts,{1024:1,"stop":1});self.assertEqual(receipt["length"],1024)
        self.assertEqual(receipt["expected_sha256"],sanitized_rows()[0]["expected_sha256"])

    def test_public_fanout_reconciles_fabricated_views_metadata_stop_and_request(self):
        self.assertFalse(hasattr(FanoutCoordinator,"step_verified"))
        self.assertNotIn("VerifiedFanoutInput",seam.__all__)
        request_a=FanoutTests()._req()
        coordinator=FanoutCoordinator(provider)
        seed_candidate,seed_peer,_,_=FanoutTests()._pair()
        verified=coordinator._phase_one(sanitized_rows(),stop_row(),1024,seed_candidate,seed_peer,request_a)
        altered=verified.candidate_view.bytes_view[:-1]+bytes([verified.candidate_view.bytes_view[-1]^1])
        cases=(
            (replace(verified,candidate_view=PrivateTokenView(1024,altered)),request_a,"FANOUT_RECEIVED_DIGEST_MISMATCH"),
            (replace(verified,length=1,expected_sha256="0"*64),request_a,"VERIFIED_FANOUT_IDENTITY_INVALID"),
            (replace(verified,stop_sha256="0"*64),request_a,"STOP_REDERIVATION_MISMATCH"),
            (verified,{**request_a,"operation_id":"drifted-operation"},"FANOUT_REQUEST_IDENTITY_MISMATCH"),
            (object(),request_a,"VERIFIED_FANOUT_IDENTITY_INVALID"),
        )
        for fabricated,actual_request,code in cases:
            candidate,peer,cb,pb=FanoutTests()._pair();before=(len(cb.calls),len(pb.calls))
            with self.subTest(code=code),patch.object(coordinator,"_phase_one",return_value=fabricated),self.assertRaisesRegex(IntegrationError,code):
                coordinator.step(sanitized_rows(),stop_row(),1024,actual_request,candidate,peer)
            self.assertEqual((len(cb.calls),len(pb.calls)),before)

    def test_pass_law_rows_fail_closed_without_full_artifacts_and_reject_domains(self):
        def pass_rows(law):
            rows=thaw(held_law_projection())
            row=rows[seam.LAW_ORDER.index(law)]
            metrics={key:(True if kind is bool else 6 if key=="arms_present" else 3 if kind is int else 0.5)
                     for key,kind in LAW_METRIC_SCHEMAS[law].items()}
            row.update(status="PASS",claim_made=True,evidence=list(LAW_REQUIRED_EVIDENCE[law]),metrics=metrics,
                       failure_code=None,held_reason=None)
            return rows
        for law in seam.LAW_ORDER:
            with self.subTest(law=law),self.assertRaisesRegex(IntegrationError,"LAW_PASS_UNAVAILABLE"): validate_laws(pass_rows(law))
        invalid={
            "L7": (("candidate_auroc",-0.01),("candidate_ece",1.01),("paired_peer_margin",-1.01)),
            "L8": (("regulation_error",-0.01),("dose_response_statistic",1.01),("specificity_statistic",-1.01)),
            "L10": (("drift_primary_metric",-0.01),("clean_secondary_metric",1.01),("abstention_rate",1.01)),
            "L14": (("self_model_visibility",-0.01),("memory_coupling",1.01),("thick_present_coupling",-1.01)),
            "L18": (("governed_seed_count",0),("governed_seed_count",2),("arms_present",0),("arms_present",5),("controls_passed",False)),
        }
        for law,mutations in invalid.items():
            index=seam.LAW_ORDER.index(law)
            for metric,value in mutations:
                rows=pass_rows(law);rows[index]["metrics"][metric]=value
                with self.subTest(law=law,metric=metric,value=value),self.assertRaisesRegex(IntegrationError,"LAW_PROJECTION_INVALID"):
                    validate_laws(rows)
            rows=pass_rows(law);rows[index]["claim_made"]=False
            with self.subTest(law=law,claim=False),self.assertRaisesRegex(IntegrationError,"LAW_PROJECTION_INVALID"):validate_laws(rows)

    def test_episode_history_is_durable_consistent_and_prevents_restored_reuse(self):
        adapter_a,backend_a=ready();state=json.loads(adapter_a.durable_state())
        self.assertEqual(state["used_episode_ids"],["episode-a"]);self.assertEqual(state["reset_ordinal"],1)
        snapshot=adapter_a.capture()
        malformed=[]
        for history in ([],["episode-b"],["episode-a","episode-a"],["episode-a",1]):
            bad=deepcopy(snapshot);bad[0]["used_episode_ids"]=history;malformed.append(bad)
        bad=deepcopy(snapshot);bad[0]["episode_id"]="episode-b";malformed.append(bad)
        bad=deepcopy(snapshot);bad[0]["reset_ordinal"]=2;malformed.append(bad)
        for ordinal,bad in enumerate(malformed):
            target,_=adapter()
            with self.subTest(ordinal=ordinal),self.assertRaisesRegex(IntegrationError,"STATE_SEMANTIC_FAILURE"):target.restore(bad)
        adapter_a.step(request("terminal",episode_id="episode-a",request_ordinal=0,context_length=1024,is_terminal_request=True),
                       PrivateTokenView(1024,encode_private_view(provider(1024))))
        completed=adapter_a.capture();target,target_backend=adapter();target.restore(completed);before=len(target_backend.calls)
        with self.assertRaisesRegex(IntegrationError,"EPISODE_ID_REUSE"):
            target.reset_episode(request("reuse",episode_id="episode-a",reset_ordinal=2))
        self.assertEqual(len(target_backend.calls),before)
        adapter_a.close(request("close"));closed=json.loads(adapter_a.durable_state())
        self.assertEqual(closed["used_episode_ids"],["episode-a"]);validate_state(closed)
        adapter_a._state["used_episode_ids"]=[];before=len(backend_a.calls)
        with self.assertRaisesRegex(IntegrationError,"STATE_SEMANTIC_FAILURE"):adapter_a.close(request("again"))
        self.assertEqual(len(backend_a.calls),before)

    def test_factory_requires_live_attestation_and_cleans_each_role(self):
        made=[]
        def ctor(session,mode="live"):
            def build():
                backend=SpyBackend(session)
                if mode=="dead":backend.real_state["live"]=False
                if mode=="throw":
                    backend.is_live=lambda:(_ for _ in ()).throw(RuntimeError("live probe"))
                made.append(backend);return backend
            return build
        factory,cman,pman,ccfg,pcfg=self._pair_specs(ctor("candidate-session-v1","dead"),ctor("peer-session-v1"))
        with self.assertRaisesRegex(IntegrationError,"CANDIDATE_BACKEND_NOT_LIVE"):
            factory.create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(pcfg),provider)
        self.assertEqual(len(made),1);self.assertFalse(made[0].real_state["live"])
        made.clear();factory,cman,pman,ccfg,pcfg=self._pair_specs(ctor("candidate-session-v1"),ctor("peer-session-v1","dead"))
        with self.assertRaisesRegex(IntegrationError,"PEER_BACKEND_NOT_LIVE"):
            factory.create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(pcfg),provider)
        self.assertEqual(len(made),2);self.assertTrue(all(not item.real_state["live"] for item in made))
        made.clear();factory,cman,pman,ccfg,pcfg=self._pair_specs(ctor("candidate-session-v1","throw"),ctor("peer-session-v1"))
        with self.assertRaisesRegex(IntegrationError,"CANDIDATE_BACKEND_NOT_LIVE"):
            factory.create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(pcfg),provider)
        self.assertEqual(len(made),1);self.assertFalse(made[0].real_state["live"])
        made.clear();factory,cman,pman,ccfg,pcfg=self._pair_specs(ctor("candidate-session-v1"),ctor("peer-session-v1"))
        candidate,peer=factory.create_pair(canonical(cman),canonical(pman),canonical(ccfg),canonical(pcfg),provider)
        self.assertTrue(candidate.backend.is_live());self.assertTrue(peer.backend.is_live())


if __name__ == "__main__":
    unittest.main()
