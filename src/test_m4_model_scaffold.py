"""Synthetic-only verification for the M4 callable scaffold (2026-08-21, Regime B)."""

import base64
import copy
import json
import unittest

from src import m4_model_scaffold as m4


class M4CallableFixtureTests(unittest.TestCase):
    def test_all_released_wrappers_and_schemas_reconstruct(self):
        results = m4.verify_released_fixtures()
        self.assertEqual(results["varying_response"], "190b49b15d5dd0b5adb693056b5781a0ac8b0cd227dd2d445bac2dd02f2f3e33")
        self.assertEqual(results["stepped_state"], "f1a740defb2ee5fe6ad484195af3eebd8c2c69735ff0ba3fdaa264f4018a7021")
        self.assertEqual(results["closed_state"], "fd37cc26f31cd4e47e078383e19e46007f9cd529e3e7d5914d4c45178f0f4790")

    def test_complete_callable_chain(self):
        adapter = m4.SyntheticCallableAdapter()
        manifest, described = adapter.describe()
        self.assertEqual(m4.digest_bytes(manifest), m4.BASE["manifest_pair"]["candidate_expected_sha256"])
        self.assertEqual(m4.digest_bytes(described), m4.CALLABLE["lifecycle_state_contract"]["operation_results"]["describe"]["expected_sha256"])

        dependency = base64.b64decode(m4.CALLABLE["dependency_manifest"]["canonical_utf8_base64"])
        initialized = adapter.initialize(manifest, dependency)
        self.assertEqual(m4.digest_bytes(initialized), m4.CALLABLE["lifecycle_state_contract"]["operation_results"]["initialize"]["expected_sha256"])

        reset = base64.b64decode(m4.CALLABLE["reset_fixture"]["canonical_utf8_base64"])
        reset_result = adapter.reset_episode(reset)
        self.assertEqual(m4.digest_bytes(reset_result), m4.CALLABLE["lifecycle_state_contract"]["operation_results"]["reset_episode"]["expected_sha256"])

        request = base64.b64decode(m4.CALLABLE["varying_candidate"]["canonical_request_utf8_base64"])
        response, stepped = adapter.step(request, b"")
        self.assertEqual(m4.digest_bytes(response), m4.AMENDMENT["varying_response"]["expected_sha256"])
        self.assertEqual(m4.digest_bytes(stepped), m4.AMENDMENT["step_operation_result"]["expected_sha256"])
        self.assertEqual(m4.digest(adapter.state), m4.AMENDMENT["stepped_state"]["expected_sha256"])

        snapshot_request = base64.b64decode(m4.AMENDMENT["snapshot_request"]["canonical_utf8_base64"])
        checkpoint, snapshot_result = adapter.snapshot(snapshot_request)
        self.assertEqual(m4.digest_bytes(checkpoint), m4.BASE["checkpoint"]["expected_sha256"])
        self.assertEqual(m4.digest_bytes(snapshot_result), m4.AMENDMENT["snapshot_operation_result"]["expected_sha256"])
        self.assertEqual(m4.digest(adapter.state), m4.AMENDMENT["snapshotted_state"]["expected_sha256"])

        close_result = adapter.close()
        self.assertEqual(m4.digest_bytes(close_result), m4.AMENDMENT["close_operation_result"]["expected_sha256"])
        self.assertEqual(m4.digest(adapter.state), m4.AMENDMENT["closed_state"]["expected_sha256"])

    def test_noncyclic_digest_domains(self):
        response = m4.AMENDMENT["varying_response"]["artifact"]
        stepped = m4.AMENDMENT["stepped_state"]["artifact"]
        projection = copy.deepcopy(stepped)
        del projection["last_response_sha256"]
        self.assertEqual(response["state_after_sha256"], m4.digest(projection))
        self.assertEqual(stepped["last_response_sha256"], m4.digest(response))
        self.assertEqual(m4.AMENDMENT["step_operation_result"]["artifact"]["post_state_sha256"], m4.digest(stepped))

    def test_failure_does_not_mutate_state(self):
        adapter = m4.SyntheticCallableAdapter()
        before = copy.deepcopy(adapter.state)
        response, result = adapter.step(b"{}", b"")
        self.assertEqual(response, b"")
        failure = json.loads(result)
        self.assertEqual(failure["failure_code"], "ADAPTER_LIFECYCLE_VIOLATION")
        self.assertEqual(failure["prior_state_sha256"], failure["post_state_sha256"])
        self.assertEqual(adapter.state, before)

    def test_schema_and_canonical_input_fail_closed(self):
        adapter = m4.SyntheticCallableAdapter()
        manifest, _ = adapter.describe()
        dependency = base64.b64decode(m4.CALLABLE["dependency_manifest"]["canonical_utf8_base64"])
        noncanonical = dependency + b"\n"
        failure = json.loads(adapter.initialize(manifest, noncanonical))
        self.assertEqual(failure["failure_code"], "SCHEMA_DRIFT")
        self.assertEqual(adapter.state["lifecycle_state"], "DESCRIBED")

    def test_amendment_base_mismatch_fails_closed(self):
        original = m4.AMENDMENT["base"]["raw_sha256"]
        try:
            m4.AMENDMENT["base"]["raw_sha256"] = "0" * 64
            with self.assertRaises(m4.ContractError) as caught:
                m4.verify_released_fixtures()
            self.assertEqual(caught.exception.code, "CONFIGURATION_MISMATCH")
        finally:
            m4.AMENDMENT["base"]["raw_sha256"] = original

    def test_reset_digest_mismatch_preserves_initialized_state(self):
        adapter = m4.SyntheticCallableAdapter()
        manifest, _ = adapter.describe()
        dependency = base64.b64decode(m4.CALLABLE["dependency_manifest"]["canonical_utf8_base64"])
        adapter.initialize(manifest, dependency)
        before = copy.deepcopy(adapter.state)
        request = copy.deepcopy(m4.CALLABLE["reset_fixture"]["request"])
        request["prior_state_sha256"] = "0" * 64
        failure = json.loads(adapter.reset_episode(m4.canonical_json(request)))
        self.assertEqual(failure["failure_code"], "DIGEST_MISMATCH")
        self.assertEqual(adapter.state, before)

    def test_snapshot_digest_mismatch_preserves_stepped_state(self):
        adapter = m4.SyntheticCallableAdapter()
        manifest, _ = adapter.describe()
        dependency = base64.b64decode(m4.CALLABLE["dependency_manifest"]["canonical_utf8_base64"])
        adapter.initialize(manifest, dependency)
        adapter.reset_episode(base64.b64decode(m4.CALLABLE["reset_fixture"]["canonical_utf8_base64"]))
        adapter.step(base64.b64decode(m4.CALLABLE["varying_candidate"]["canonical_request_utf8_base64"]), b"")
        before = copy.deepcopy(adapter.state)
        request = copy.deepcopy(m4.AMENDMENT["snapshot_request"]["artifact"])
        request["expected_state_sha256"] = "0" * 64
        checkpoint, failure_bytes = adapter.snapshot(m4.canonical_json(request))
        self.assertEqual(checkpoint, b"")
        self.assertEqual(json.loads(failure_bytes)["failure_code"], "DIGEST_MISMATCH")
        self.assertEqual(adapter.state, before)

    def test_close_out_of_order_preserves_state(self):
        adapter = m4.SyntheticCallableAdapter()
        before = copy.deepcopy(adapter.state)
        failure = json.loads(adapter.close())
        self.assertEqual(failure["failure_code"], "ADAPTER_LIFECYCLE_VIOLATION")
        self.assertEqual(adapter.state, before)

    def test_wrapper_tamper_is_digest_mismatch(self):
        wrapper = copy.deepcopy(m4.AMENDMENT["varying_response"])
        wrapper["artifact"]["confidence"] = 0.5
        with self.assertRaises(m4.ContractError) as caught:
            m4.verify_wrapper(wrapper)
        self.assertEqual(caught.exception.code, "DIGEST_MISMATCH")


if __name__ == "__main__":
    unittest.main()
