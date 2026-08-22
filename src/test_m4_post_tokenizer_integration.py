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
    realize_launch_command, sha256_bytes, validate_laws, validate_pair_identity, validate_state,
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
    def __init__(self, session="candidate-session-v1", behavior=None):
        self.session, self.behavior, self.calls = session, behavior or {}, []
        self.real_state = {"generation": 0, "payload": []}

    def capture_state(self): return deepcopy(self.real_state)
    def restore_state(self, snapshot): self.real_state = deepcopy(snapshot)

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
        for status in ("PASS","FAIL","NOT_RUN"):
            rows=deepcopy(held);row=rows[0];row["status"]=status;row["held_reason"]=None
            if status=="PASS": row.update(claim_made=True,evidence=["candidate_manifest","peer_manifest","channel_redaction_receipt","ground_truth_receipt","candidate_auroc","candidate_ece","paired_peer_margin","empty_permuted_shuffled_rows"])
            elif status=="FAIL": row.update(evidence=["failure-receipt"],failure_code="L7_CALIBRATION_FAIL")
            else: row.update(evidence=["instrument-receipt"],failure_code="INSTRUMENT_FAILURE:synthetic")
            validate_laws(rows)
            for field,value in (("meaning_source","wrong"),("claim_made",not row["claim_made"]),("evidence",[]),("failure_code","WRONG"),("held_reason","WRONG")):
                bad=deepcopy(rows);bad[0][field]=value
                with self.subTest(status=status,field=field),self.assertRaisesRegex(IntegrationError,"LAW_PROJECTION_INVALID"): validate_laws(bad)


if __name__ == "__main__":
    unittest.main()
