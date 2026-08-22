import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from src.m4_final_prescoring_crash_cart import *

ZERO_DIGEST = "0" * 64


def reset_receipt(role, prior, result, nonce):
    return {"status": "PASS", "backend_code": None, "session_id": role,
            "prior_backend_state_sha256": prior, "result_backend_state_sha256": result,
            "request_sha256": sha256(f"reset:{role}:{nonce}".encode()), "request_ordinal": None}


class FakeBackends:
    def __init__(self, events, role_failure=None, reset_fault=None, callback=None):
        self.events = events
        self.role_failure = role_failure
        self.reset_fault = reset_fault
        self.callback = callback
        self.states = {"candidate": ZERO_DIGEST, "peer": ZERO_DIGEST}
        self.reset_counts = {"candidate": 0, "peer": 0}
        self.requests = []
        self.role_receipts = []
        self.reset_receipts = []

    def role(self, name):
        def call(request):
            kind, ordinal = request["kind"], request["ordinal"]
            self.events.append((name, kind, ordinal))
            self.requests.append((name, copy.deepcopy(request)))
            if self.callback:
                self.callback(name, request)
            if self.role_failure == (name, kind, ordinal):
                raise RuntimeError("injected role failure")
            prior = self.states[name]
            result = sha256(f"{name}:{kind}:{ordinal}:{prior}".encode())
            self.states[name] = result
            receipt = {"status": "PASS", "backend_code": None, "session_id": name,
                       "prior_backend_state_sha256": prior, "result_backend_state_sha256": result,
                       "request_sha256": sha256(canonical_bytes(request)), "request_ordinal": ordinal}
            self.role_receipts.append((name, kind, ordinal, copy.deepcopy(receipt)))
            return receipt
        return call

    def reset(self, role):
        self.events.append(("reset", role))
        self.reset_counts[role] += 1
        count = self.reset_counts[role]
        prior = self.states[role]
        if self.reset_fault == (role, count, "raise"):
            raise RuntimeError("injected reset failure")
        result = sha256(f"{role}:reset:{count}".encode())
        receipt = reset_receipt(role, prior, result, count)
        if self.reset_fault == (role, count, "session"):
            receipt["session_id"] = "wrong-role"
        elif self.reset_fault == (role, count, "status"):
            receipt["status"] = "FAIL"
        elif self.reset_fault == (role, count, "prior"):
            receipt["prior_backend_state_sha256"] = "not-a-digest"
        elif self.reset_fault == (role, count, "digest"):
            receipt["result_backend_state_sha256"] = "not-a-digest"
        elif self.reset_fault == (role, count, "correlation"):
            receipt["request_ordinal"] = 0
        elif self.reset_fault == (role, count, "shape"):
            receipt.pop("request_sha256")
        if self.reset_fault == (role, count, "same"):
            receipt["result_backend_state_sha256"] = prior
        else:
            self.states[role] = result
        self.reset_receipts.append((role, count, copy.deepcopy(receipt)))
        return receipt


def role_observation(role, ordinal):
    digest = sha256(f"{role}:{ordinal}".encode())
    receipt = {"status": "PASS", "backend_code": None, "session_id": role,
               "prior_backend_state_sha256": digest, "result_backend_state_sha256": digest,
               "request_sha256": digest, "request_ordinal": ordinal}
    return {"runtime_id": role, "request_sha256": digest, "receipt": receipt,
            "output_text": "public", "output_sha256": digest, "input_token_count": 1,
            "output_token_count": 1, "stop_reason": None, "start_monotonic_ns": 0,
            "end_monotonic_ns": 1, "latency_ns": 1, "error": None, "retry_count": 0}


def warmup_complete():
    rows = []
    for ordinal, (digest, size) in enumerate(zip(WARMUP_DIGESTS, WARMUP_BYTES)):
        rows.append({"ordinal": ordinal, "prompt_sha256": digest, "prompt_bytes": size,
                     "candidate": role_observation("candidate", ordinal),
                     "peer": role_observation("peer", ordinal), "barrier_monotonic_ns": ordinal})
    return {"classification": "NON_SCORING_OPERATIONAL_WARMUP", "status": "PASS",
            "attempted_pair_count": 4, "observed_role_count": 8, "rows": rows,
            "clean_barrier_status": "PASS", "zero_active_requests": True,
            "residual_state_clear": True, "prefix_cache_disabled": True,
            "rng_independent_after_barrier": True}


def pair_rows():
    rows = []
    for item in fixture_inventory():
        ordinal = item["ordinal"]
        rows.append({"ordinal": ordinal, "fixture_id": item["fixture_id"],
                     "public_prompt_text": item["public_prompt_text"], "prompt_sha256": item["prompt_sha256"],
                     "candidate": role_observation("candidate", ordinal),
                     "peer": role_observation("peer", ordinal), "comparison": "MATCH",
                     "ordering_valid": True, "rollback_trace_ref": None})
    return rows


def samples():
    return [{"monotonic_ns": index * TELEMETRY_INTERVAL_NS, "gpu_utilization_percent": 0,
             "gpu_memory_used_bytes": 0, "host_ram_used_bytes": 0, "queue_depth_pairs": 0,
             "producer_blocked": False, "completed_pair_count": min(index, 64)} for index in range(121)]


def active_complete():
    return {"status": "PASS", "start_monotonic_ns": 0, "end_monotonic_ns": 30_000_000_000,
            "duration_ns": 30_000_000_000, "attempted_pair_count": 64,
            "observed_role_count": 128, "completed_pair_count": 64, "drop_count": 0,
            "producer_blocked_event_count": 0}


def cleanup(status="NOT_RUN", attempted=False):
    observed = True if status == "PASS" else None
    return {"status": status, "attempted": attempted, "engines_disposed": observed,
            "runtime_processes_absent": observed, "backend_gpu_allocations_absent": observed,
            "temp_files_absent": observed, "repository_clean": observed, "post_state_recorded": observed}


def replica(status="NOT_RUN"):
    complete = status == "MATCH"
    return {"status": status, "compared_count": 64 if complete else 0,
            "agreement_count": 64 if complete else 0, "mismatch_count": 0,
            "mismatch_ordinals": [], "exact_replica_consumer_stop": False}


def trends():
    distribution = {"count": 64, "min": 0, "mean": 0, "p50": 0, "p90": 0, "p95": 0, "max": 0}
    return {"classification": "NON_SCORING_EXPLORATORY_OBSERVATION",
            "candidate_latency_ns": distribution, "peer_latency_ns": distribution,
            "candidate_output_tokens": distribution, "peer_output_tokens": distribution,
            "throughput_one_second_bins": [64], "resource_sample_count": 121,
            "queue_block_ns": distribution, "agreement_count": 64, "disagreement_ordinals": [],
            "fixture_stability": [{} for _ in range(8)], "stop_counts": {}, "error_counts": {},
            "lexical_refusal_marker_counts": {}, "context_buckets": [{}], "decision_use": False}


def base_report(stage, failure_stage):
    failure = None if failure_stage is None else {"code": "SYNTHETIC_BLOCK", "stage": failure_stage,
                                                   "message": "custody-free test", "observed_monotonic_ns": 0,
                                                   "retry_count": 0}
    return {
        "schema_version": "m4-final-prescoring-full-stack-crash-cart-report-v1", "date": "2026-08-22",
        "regime": "B", "classification": "NON_SCORING_EXPLORATORY_OBSERVATION", "source_tag": "[PROPOSED]",
        "authority": {"path": "handoffs/REBECCA_M4_FINAL_PRESCORING_FULL_STACK_CRASH_CART_AND_EXPLORATORY_OBSERVATION_AUTHORITY_2026-08-22.md",
                      "commit": "8b4a383c450e8b29f2633f7e25107abcb62dd929", "bytes": 6087,
                      "sha256": "c759a99a563777a42ba42eb25f4679a40bb940a246bc002ef199c61e58721ecc",
                      "effect": "DESIGN_AND_IMPLEMENTATION_PREPARATION_ONLY_NO_RUN_AUTHORITY"},
        "evidence_stage": stage, "failure_stage": failure_stage, "failure": failure,
        "identities": {"released_checkout": "public-test"},
        "invocation": {"released": False, "started": False, "invocation_count": 0,
                       "retry_count": 0, "command_sha256": None},
        "negative_probes": [], "warmup": None, "active_window": None, "rows": [],
        "resource_samples": [], "trends": None, "laws": list(held_laws()),
        "structural_status": "BLOCKED" if failure else "PASS",
        "structural_failures": [failure["code"]] if failure else [], "replica_consistency": replica(),
        "cleanup": cleanup(),
        "public_safety": {"status": "NOT_RUN", "files_scanned": 0, "findings": 0,
                          "manual_classifications": 0, "silent_suppressions": 0},
        "export": {"status": "LOCAL_PARTIAL_RETAINED", "emitted_paths": [], "reproduction_equal": None}}


def valid_report(stage):
    if stage == "PRE_ACTIVE_TERMINAL":
        return base_report(stage, "PRE_START")
    if stage == "PARTIAL_WARMUP_TERMINAL":
        report = base_report(stage, "WARMUP")
        report["warmup"] = {"classification": "NON_SCORING_OPERATIONAL_WARMUP", "status": "FAIL",
                            "attempted_pair_count": 0, "observed_role_count": 0, "rows": [],
                            "clean_barrier_status": "NOT_REACHED", "zero_active_requests": None,
                            "residual_state_clear": None, "prefix_cache_disabled": None,
                            "rng_independent_after_barrier": None}
        return report
    if stage == "PARTIAL_ACTIVE_TERMINAL":
        report = base_report(stage, "ACTIVE_WINDOW")
        report["warmup"] = warmup_complete()
        report["active_window"] = {"status": "FAIL", "start_monotonic_ns": 0, "end_monotonic_ns": 1,
                                   "duration_ns": 1, "attempted_pair_count": 0, "observed_role_count": 0,
                                   "completed_pair_count": 0, "drop_count": 0,
                                   "producer_blocked_event_count": 0}
        return report
    report = base_report(stage, "CLEANUP" if stage == "POST_ACTIVE_TERMINAL" else None)
    report["warmup"], report["active_window"] = warmup_complete(), active_complete()
    report["rows"], report["resource_samples"] = pair_rows(), samples()
    if stage == "POST_ACTIVE_TERMINAL":
        report["cleanup"] = cleanup("FAIL", True)
        return report
    report["trends"], report["replica_consistency"] = trends(), replica("MATCH")
    report["cleanup"] = cleanup("PASS", True)
    report["public_safety"] = {"status": "CLEAR", "files_scanned": 1, "findings": 0,
                               "manual_classifications": 0, "silent_suppressions": 0}
    report["export"] = {"status": "EXPORTED", "emitted_paths": ["public.json"], "reproduction_equal": True}
    return report


class CrashCartBetaTests(unittest.TestCase):
    def test_warmup_exact(self):
        plan = warmup_plan()
        self.assertEqual([len(item["prompt"]) for item in plan], list(WARMUP_BYTES))
        self.assertEqual([item["prompt_sha256"] for item in plan], list(WARMUP_DIGESTS))

    def test_warmup_rejects_drift(self):
        with self.assertRaises(CrashCartError):
            warmup_prompt(0, 32)

    def test_schedule_and_fixtures(self):
        self.assertEqual((len(active_schedule()), active_schedule()[15], active_schedule()[16], active_schedule()[-1]),
                         (64, 0, 625_000_000, 30_000_000_000))
        self.assertEqual([public_fixture(i)["payload_bytes"] for i in range(8)], list(FIXTURE_SIZES))

    def test_held_laws_are_exact_and_non_scoring(self):
        laws = held_laws()
        self.assertEqual([item["law_id"] for item in laws], list(LAW_ORDER))
        self.assertTrue(all(not item["claim_made"] and item["evidence"] == [] and item["metrics"] == {} for item in laws))

    def test_pre_active_rejects_fabricated_rows(self):
        with self.assertRaises(CrashCartError):
            validate_terminal({"evidence_stage": "PRE_ACTIVE_TERMINAL", "warmup": None,
                               "active_window": None, "rows": [{}], "failure": {"retry_count": 0}})

    def test_complete_requires_full_evidence(self):
        with self.assertRaises(CrashCartError):
            validate_terminal({"evidence_stage": "COMPLETE_ACTIVE_TERMINAL", "warmup": {},
                               "active_window": {}, "rows": [], "failure": None,
                               "failure_stage": None, "structural_status": "PASS"})

    def test_replica_mismatch_stops_consumer(self):
        with self.assertRaisesRegex(CrashCartError, "EXACT_REPLICA"):
            exact_replica_consumer_stop({"status": "MISMATCH"})

    def test_wrapper_guard_never_starts_runtime(self):
        with self.assertRaisesRegex(CrashCartError, "RUN_AUTHORITY_ABSENT"):
            execution_guard(False)


class ProductionPathCorrectionTests(unittest.TestCase):
    def lifecycle(self, **kwargs):
        events = []
        backends = FakeBackends(events, role_failure=kwargs.get("role_failure"),
                                reset_fault=kwargs.get("reset_fault"), callback=kwargs.get("callback"))
        life = CrashCartLifecycle(backends.role("candidate"), backends.role("peer"), backends.reset,
                                  lambda: events.append(("cleanup",)), clock_ns=kwargs.get("clock"))
        return life, backends, events

    def test_candidate_warmup_zero_failure_rolls_back_resets_and_cleans(self):
        life, _, events = self.lifecycle(role_failure=("candidate", "warmup", 0))
        with self.assertRaises(CrashCartError):
            life.run()
        self.assertIn(("cleanup",), events)
        self.assertGreaterEqual(events.count(("reset", "candidate")), 2)
        self.assertGreaterEqual(events.count(("reset", "peer")), 2)

    def test_symmetric_barriers_resets_rng_no_priming_and_receipt_ordinals(self):
        life, _, _ = self.lifecycle()
        result = life.run()
        self.assertEqual(result["active_ordinals"], list(range(64)))
        self.assertEqual(result["warmup_ordinals"], list(range(4)))
        self.assertEqual(life.events.count("clean-barrier"), 1)
        self.assertLess(life.events.index("clean-barrier"), life.events.index("rng-after-clean-barrier"))

    def test_schedule_queue_deadline_and_telemetry(self):
        life, _, _ = self.lifecycle()
        result = life.run()
        self.assertEqual(result["dispatch_observed_ns"], list(active_schedule()))
        self.assertLessEqual(result["max_queue_depth"], QUEUE_CAPACITY)
        self.assertEqual([item["monotonic_ns"] for item in result["telemetry"]],
                         list(range(0, 30_000_000_001, TELEMETRY_INTERVAL_NS)))

    def test_invalid_receipt_fails_first_field_and_no_later_evidence(self):
        life, backends, events = self.lifecycle()
        def bad(request):
            events.append(("candidate", request["kind"], request["ordinal"]))
            return {"status": "PASS", "backend_code": "NON_NULL", "session_id": "SAME_SESSION",
                    "prior_backend_state_sha256": "bad", "result_backend_state_sha256": "bad",
                    "request_sha256": "wrong", "request_ordinal": request["ordinal"]}
        life.candidate = life.peer = bad
        with self.assertRaisesRegex(CrashCartError, "RECEIPT_BACKEND_CODE_INVALID"):
            life.run()
        self.assertIn(("cleanup",), events)
        self.assertFalse(any(event[1] == "active" for event in events if len(event) == 3))
        self.assertFalse(any(event.startswith("dispatch@") for event in life.events))
        self.assertGreaterEqual(backends.reset_counts["candidate"], 2)

    def test_inventory_is_committed_ordered_unique_and_exact(self):
        bound = json.loads(Path("specs/data/m4_final_prescoring_crash_cart_prompt_inventory_v1.json").read_text())["sha256"]
        actual = [item["prompt_sha256"] for item in fixture_inventory()]
        self.assertEqual(actual, bound)
        self.assertEqual(len(set(actual)), 64)

    def test_strict_schema_counterexamples(self):
        cases = [{"evidence_stage": stage} for stage in
                 ("PRE_ACTIVE_TERMINAL", "PARTIAL_ACTIVE_TERMINAL", "POST_ACTIVE_TERMINAL", "COMPLETE_ACTIVE_TERMINAL")]
        for case in cases:
            with self.subTest(stage=case["evidence_stage"]), self.assertRaises(CrashCartError):
                validate_terminal(case)

    def test_full_top_level_complete_schema_counterexample(self):
        report = valid_report("COMPLETE_ACTIVE_TERMINAL")
        report["schema_version"], report["classification"], report["identities"] = "WRONG", "SCORING_RESULT", {}
        with self.assertRaisesRegex(CrashCartError, "REPORT_SCHEMA_INVALID"):
            validate_terminal(report)

    def test_schema_accepts_all_five_stage_representatives(self):
        for stage in sorted(STAGES):
            with self.subTest(stage=stage):
                validate_terminal(valid_report(stage))

    def test_schema_rejects_min_properties_and_keyword_neighborhood(self):
        mutations = [
            ("minProperties", lambda r: r.__setitem__("identities", {})),
            ("required", lambda r: r["authority"].pop("path")),
            ("const", lambda r: r.__setitem__("schema_version", "wrong")),
            ("enum", lambda r: r.__setitem__("structural_status", "wrong")),
            ("type", lambda r: r["invocation"].__setitem__("invocation_count", "0")),
            ("pattern", lambda r: r["rows"][0]["candidate"].__setitem__("request_sha256", "z" * 64)),
            ("minimum", lambda r: r["active_window"].__setitem__("duration_ns", -1)),
            ("maximum", lambda r: r["invocation"].__setitem__("invocation_count", 2)),
            ("additionalProperties", lambda r: r["invocation"].__setitem__("extra", True)),
            ("oneOf", lambda r: r.__setitem__("failure", {})),
            ("conditional", lambda r: r["replica_consistency"].__setitem__("agreement_count", 63)),
            ("format", lambda r: r.__setitem__("date", "not-a-date")),
        ]
        for name, mutate in mutations:
            report = valid_report("COMPLETE_ACTIVE_TERMINAL")
            mutate(report)
            with self.subTest(keyword=name), self.assertRaisesRegex(CrashCartError, "REPORT_SCHEMA_INVALID"):
                validate_terminal(report)

    def test_schema_failure_precedes_semantics(self):
        report = valid_report("COMPLETE_ACTIVE_TERMINAL")
        report["identities"] = {}
        with patch("src.m4_final_prescoring_crash_cart.held_laws", side_effect=AssertionError("semantic path reached")):
            with self.assertRaisesRegex(CrashCartError, "REPORT_SCHEMA_INVALID"):
                validate_terminal(report)

    def test_each_incomplete_stage_rejects_an_otherwise_complete_nested_defect(self):
        cases = []
        pre = valid_report("PRE_ACTIVE_TERMINAL")
        pre["identities"] = {}
        cases.append(pre)
        warmup = valid_report("PARTIAL_WARMUP_TERMINAL")
        warmup["warmup"]["unexpected"] = True
        cases.append(warmup)
        active = valid_report("PARTIAL_ACTIVE_TERMINAL")
        active["failure"]["message"] = ""
        cases.append(active)
        post = valid_report("POST_ACTIVE_TERMINAL")
        post["cleanup"]["status"] = "WRONG"
        cases.append(post)
        complete = valid_report("COMPLETE_ACTIVE_TERMINAL")
        complete["rows"][0]["candidate"]["request_sha256"] = "not-a-sha"
        cases.append(complete)
        for report in cases:
            with self.subTest(stage=report["evidence_stage"]), self.assertRaisesRegex(CrashCartError, "REPORT_SCHEMA_INVALID"):
                validate_terminal(report)

    def test_reset_rebinds_fresh_measured_state_and_active_zero(self):
        life, backends, _ = self.lifecycle()
        result = life.run()
        active_zero = next(request for role, request in backends.requests
                           if role == "candidate" and request["kind"] == "active" and request["ordinal"] == 0)
        self.assertEqual(result["active_ordinals"][0], 0)
        self.assertEqual(backends.reset_counts, {"candidate": 2, "peer": 2})
        self.assertEqual(active_zero["ordinal"], 0)
        measured_reset = next(receipt for role, count, receipt in backends.reset_receipts
                              if role == "candidate" and count == 2)
        active_zero_receipt = next(receipt for role, kind, ordinal, receipt in backends.role_receipts
                                   if role == "candidate" and kind == "active" and ordinal == 0)
        self.assertEqual(active_zero_receipt["prior_backend_state_sha256"],
                         measured_reset["result_backend_state_sha256"])

    def test_reset_same_digest_is_valid(self):
        life, backends, _ = self.lifecycle(reset_fault=("candidate", 2, "same"))
        self.assertEqual(life.run()["active_ordinals"], list(range(64)))
        self.assertEqual(life._states, backends.states)

    def test_reset_malformed_mismatched_or_peer_failure_is_atomic_and_cleans(self):
        for fault in (("candidate", 2, "digest"), ("candidate", 2, "session"),
                      ("candidate", 2, "status"), ("candidate", 2, "prior"),
                      ("candidate", 2, "correlation"), ("peer", 2, "raise"),
                      ("peer", 2, "shape")):
            life, _, events = self.lifecycle(reset_fault=fault)
            with self.subTest(fault=fault), self.assertRaises(CrashCartError):
                life.run()
            self.assertIn(("cleanup",), events)
            self.assertFalse(any(event[1] == "active" for event in events if len(event) == 3))

    def test_rollback_reset_failure_projects_pair_rollback_and_still_cleans(self):
        events = []
        backends = FakeBackends(events, role_failure=("candidate", "warmup", 0))
        original_reset = backends.reset
        def reset(role):
            if role == "candidate" and backends.reset_counts[role] == 1:
                raise RuntimeError("rollback reset failed")
            return original_reset(role)
        life = CrashCartLifecycle(backends.role("candidate"), backends.role("peer"), reset,
                                  lambda: events.append(("cleanup",)))
        with self.assertRaisesRegex(CrashCartError, "PAIR_ROLLBACK"):
            life.run()
        self.assertIn(("cleanup",), events)

    def test_final_pair_deadline_below_exact_and_over_boundary(self):
        for terminal, should_pass in ((ACTIVE_DEADLINE_NS - 1, True), (ACTIVE_DEADLINE_NS, True),
                                      (ACTIVE_DEADLINE_NS + 1, False)):
            now = [0]
            def jump(role, request):
                if role == "peer" and request["kind"] == "active" and request["ordinal"] == 63:
                    now[0] = terminal
            life, _, events = self.lifecycle(clock=lambda: now[0], callback=jump)
            life.sleep_until_ns = lambda target: now.__setitem__(0, max(now[0], target))
            if should_pass:
                self.assertEqual(len(life.run()["active_ordinals"]), 64)
            else:
                with self.assertRaisesRegex(CrashCartError, "ACTIVE_WINDOW_TIMEOUT_NO_RETRY"):
                    life.run()
                self.assertIn(("cleanup",), events)

    def test_earlier_overrun_and_sleeper_underwait_fail_closed(self):
        now = [0]
        sampled = []
        def jump(role, request):
            if role == "peer" and request["kind"] == "active" and request["ordinal"] == 20:
                now[0] = ACTIVE_DEADLINE_NS + 1
        life, _, events = self.lifecycle(clock=lambda: now[0], callback=jump)
        life.sleep_until_ns = lambda target: now.__setitem__(0, max(now[0], target))
        life.sampler = lambda observed, completed: sampled.append(observed) or {
            "monotonic_ns": observed, "queue_depth_pairs": 0, "completed_pair_count": completed}
        with self.assertRaisesRegex(CrashCartError, "ACTIVE_WINDOW_TIMEOUT_NO_RETRY"):
            life.run()
        self.assertFalse(any(event[1] == "active" and event[2] > 20 for event in events if len(event) == 3))
        self.assertTrue(sampled)
        self.assertLess(max(sampled), ACTIVE_DEADLINE_NS)
        self.assertIn(("cleanup",), events)
        self.assertGreaterEqual(events.count(("reset", "candidate")), 3)
        self.assertGreaterEqual(events.count(("reset", "peer")), 3)
        underwait, _, under_events = self.lifecycle(clock=lambda: 0)
        underwait.sleep_until_ns = lambda target: None
        with self.assertRaisesRegex(CrashCartError, "SCHEDULE_BYPASS"):
            underwait.run()
        self.assertIn(("cleanup",), under_events)

    def test_governed_constants_and_every_warmup_request_are_exact(self):
        life, backends, _ = self.lifecycle()
        life.run()
        warmups = [request for _, request in backends.requests if request["kind"] == "warmup"]
        self.assertEqual(len(warmups), 8)
        self.assertTrue(all(request["controls"]["rng_domain"] == "M4_FINAL_CRASH_CART_WARMUP_V1" for request in warmups))
        contract = json.loads(Path("specs/data/m4_final_prescoring_crash_cart_beta_contract_v1.json").read_text())
        gate = json.loads(Path("specs/data/m4_final_prescoring_full_stack_crash_cart_gate_v1.json").read_text())
        launch = json.loads(Path("specs/data/m4_final_prescoring_full_stack_crash_cart_launch_contract_v1.json").read_text())
        self.assertEqual(QUEUE_CAPACITY, contract["active_window"]["queue_pairs"])
        self.assertEqual(ACTIVE_DEADLINE_NS, contract["active_window"]["deadline_ns"])
        self.assertEqual(TELEMETRY_INTERVAL_NS, contract["active_window"]["sample_interval_ns"])
        self.assertEqual(active_schedule(), tuple(0 if i < 16 else (i - 15) * 625_000_000 for i in range(64)))
        self.assertEqual(QUEUE_CAPACITY, launch["active_controls"]["queue_capacity_pairs"])
        self.assertEqual(ACTIVE_DEADLINE_NS, gate["active_schedule"]["hard_active_window_deadline_ns"])
        self.assertEqual(TELEMETRY_INTERVAL_NS, gate["resource_sampling"]["interval_ns"])
        governed = gate["warmup"]["generation_parameters"]
        for ordinal, item in enumerate(warmup_plan()):
            self.assertEqual(item["rng_domain"], governed["rng_domain"])
            self.assertEqual(item["max_output_tokens"], governed["max_output_tokens_by_ordinal"][ordinal])
            self.assertEqual(item["temperature"], governed["temperature_millionths"] / 1_000_000)
            self.assertEqual(item["top_p"], governed["top_p_millionths"] / 1_000_000)
            self.assertEqual(item["top_k"], governed["top_k"])
            self.assertEqual(item["seed"], governed["warmup_sampling_seed"])
            self.assertEqual(item["prefix_caching"], gate["warmup"]["prefix_caching"])
        self.assertEqual([item["ordinal"] for item in fixture_inventory()], list(range(64)))

    def test_invalid_telemetry_observation_fails_closed_and_cleans(self):
        life, _, events = self.lifecycle()
        life.sampler = lambda expected, completed: {
            "monotonic_ns": expected + 1, "queue_depth_pairs": 0,
            "completed_pair_count": completed}
        with self.assertRaisesRegex(CrashCartError, "TELEMETRY_OBSERVATION_INVALID"):
            life.run()
        self.assertIn(("cleanup",), events)


if __name__ == "__main__":
    unittest.main()
