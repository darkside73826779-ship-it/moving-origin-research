"""Tests for the prospective two-axis report and text-only dependency lock.

Date: 2026-08-22
Regime: B
"""
from __future__ import annotations

import hashlib
import importlib.metadata as metadata
import json
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

import jsonschema

from tools.testbed import derive_m4_wsl2_two_axis_report as derive
from tools.testbed import verify_m4_wsl2_text_only_runtime as runtime

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "artifacts/m4_wsl2_preexecution_testbed/m4_wsl2_dual_model_probe_report_2026-08-22.json"
PROJECTION = ROOT / "artifacts/m4_wsl2_preexecution_testbed/m4_wsl2_dual_model_probe_two_axis_projection_2026-08-22.json"
SCHEMA = ROOT / "specs/data/m4_wsl2_dual_model_probe_two_axis_report_schema_v2.json"
LEGACY_SCHEMA = ROOT / "specs/data/m4_wsl2_dual_model_probe_report_schema_v1.json"
EXCLUSION = ROOT / "specs/data/m4_wsl2_text_only_dependency_exclusion_v1.json"
SETUP = ROOT / "tools/testbed/setup_m4_wsl2_diagnostic_runtime.sh"


class TwoAxisDependencyLockTests(unittest.TestCase):
    def matching_source(self) -> dict:
        source = json.loads(LEGACY.read_bytes())
        for row in source["windows"]:
            row["outputs_agree"] = True
        source["run"]["all_outputs_agree"] = True
        source["failure_codes"] = []
        source["status"] = "PASS"
        return source

    def assert_projection_rejected(self, report: dict) -> None:
        with self.assertRaises((jsonschema.ValidationError, ValueError)):
            derive.validate_projection(report)

    def test_legacy_v1_is_byte_preserved_and_blocked(self) -> None:
        raw = LEGACY.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), "7dde0d1587b9205a339776ad04daecfe2bf160e8ecb9ff0504335f91b57a10bc")
        report = json.loads(raw)
        self.assertEqual((report["status"], report["failure_codes"]), ("BLOCKED", ["OUTPUT_DIGEST_MISMATCH"]))
        jsonschema.Draft202012Validator(json.loads(LEGACY_SCHEMA.read_text())).validate(report)

    def test_retained_projection_has_independent_axes(self) -> None:
        report = json.loads(PROJECTION.read_text())
        jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text())).validate(report)
        self.assertEqual(report["structural_status"], "PASS")
        self.assertEqual(report["replica_consistency_status"], "MISMATCH")
        self.assertEqual(report["replica_consistency"]["compared_count"], 164)
        self.assertEqual(report["replica_consistency"]["agreement_count"], 80)
        self.assertEqual(report["replica_consistency"]["mismatch_count"], 84)
        self.assertEqual(report["consumer_rule"], "BYTE_IDENTICAL_REPLICA_CONSUMER_MUST_STOP_ON_MISMATCH")

    def test_projection_is_exact_derivation(self) -> None:
        expected = derive.canonical(derive.derive(LEGACY.read_bytes())) + b"\n"
        self.assertEqual(PROJECTION.read_bytes(), expected)

    def test_replica_not_run_projection(self) -> None:
        source = json.loads(LEGACY.read_bytes())
        source["windows"] = []
        source["run"].update(windows_produced=0, windows_consumed=0)
        result = derive.derive(derive.canonical(source) + b"\n")
        self.assertEqual(result["replica_consistency_status"], "NOT_RUN")
        self.assertEqual(result["structural_status"], "BLOCKED")

    def test_replica_match_projection(self) -> None:
        source = self.matching_source()
        result = derive.derive(derive.canonical(source) + b"\n")
        self.assertEqual(result["structural_status"], "PASS")
        self.assertEqual(result["replica_consistency_status"], "MATCH")
        self.assertEqual(result["replica_consistency"]["mismatch_count"], 0)

    def test_structural_failure_is_independent_of_replica_match(self) -> None:
        source = self.matching_source()
        source["status"] = "BLOCKED"
        source["failure_codes"] = ["CHILD_PROCESS_FAILURE"]
        result = derive.derive(derive.canonical(source) + b"\n")
        self.assertEqual(result["structural_status"], "BLOCKED")
        self.assertEqual(result["structural_failure_codes"], ["CHILD_PROCESS_FAILURE"])
        self.assertEqual(result["replica_consistency_status"], "MATCH")

    def test_every_exact_v1_failure_code_projects_fail_closed(self) -> None:
        schema_codes = set(json.loads(LEGACY_SCHEMA.read_text())["properties"]["failure_codes"]["items"]["enum"])
        self.assertEqual(derive.V1_FAILURE_CODES, schema_codes)
        self.assertEqual(derive.STRUCTURAL_FAILURE_CODES, schema_codes - {"OUTPUT_DIGEST_MISMATCH"})
        for code in sorted(derive.V1_FAILURE_CODES):
            with self.subTest(code=code):
                source = self.matching_source()
                source["status"] = "BLOCKED"
                source["failure_codes"] = [code]
                result = derive.derive(derive.canonical(source) + b"\n")
                expected = "PASS" if code == "OUTPUT_DIGEST_MISMATCH" else "BLOCKED"
                self.assertEqual(result["structural_status"], expected)
                if code != "OUTPUT_DIGEST_MISMATCH":
                    self.assertIn(code, result["structural_failure_codes"])

    def test_unknown_or_schema_invalid_v1_code_is_rejected(self) -> None:
        source = self.matching_source()
        source["status"] = "BLOCKED"
        source["failure_codes"] = ["CLEANUP_INCOMPLETE"]
        with self.assertRaises(jsonschema.ValidationError):
            derive.derive(derive.canonical(source) + b"\n")

    def test_metric_failures_use_exact_v1_vocabulary(self) -> None:
        cases = (
            ("active_duration_ns", 0, "ACTIVE_DURATION_SHORT"),
            ("dropped_windows", 1, "DROPPED_WINDOWS"),
            ("order_preserved", False, "FIFO_ORDER_MISMATCH"),
            ("all_executions_overlap", False, "EXECUTIONS_DID_NOT_OVERLAP"),
            ("producer_backpressure_observed", False, "NO_BACKPRESSURE_OBSERVED"),
            ("cleanup_gpu_used_mib", 1, "CLEANUP_VRAM_NONZERO"),
        )
        for field, value, code in cases:
            with self.subTest(field=field):
                source = self.matching_source()
                source["status"] = "BLOCKED"
                source["failure_codes"] = [code]
                source["run"][field] = value
                result = derive.derive(derive.canonical(source) + b"\n")
                self.assertEqual(result["structural_status"], "BLOCKED")
                self.assertIn(code, result["structural_failure_codes"])

    def test_v2_schema_and_semantics_reject_contradictions(self) -> None:
        valid = derive.derive(LEGACY.read_bytes())
        mutations = []
        item = deepcopy(valid); item["replica_consistency_status"] = "MATCH"; mutations.append(item)
        item = deepcopy(valid); item["replica_consistency"]["mismatch_count"] = 0; mutations.append(item)
        item = deepcopy(valid); item["replica_consistency"]["agreement_count"] += 1; mutations.append(item)
        item = deepcopy(valid); item["replica_consistency"]["mismatch_ordinals"] = item["replica_consistency"]["mismatch_ordinals"][:-1]; mutations.append(item)
        item = deepcopy(valid); item["replica_consistency"]["mismatch_ordinals"][1] = item["replica_consistency"]["mismatch_ordinals"][0]; mutations.append(item)
        item = deepcopy(valid); item["replica_consistency"]["mismatch_ordinals"][0] = item["replica_consistency"]["compared_count"]; mutations.append(item)
        item = deepcopy(valid); item["replica_consistency"]["mismatch_ordinals_sha256"] = "0" * 64; mutations.append(item)
        item = deepcopy(valid); item["structural_status"] = "PASS"; item["structural_failure_codes"] = ["CHILD_PROCESS_FAILURE"]; mutations.append(item)
        item = deepcopy(valid); item["source_v1"]["failure_codes"] = ["UNKNOWN"]; mutations.append(item)
        for ordinal, mutation in enumerate(mutations):
            with self.subTest(ordinal=ordinal):
                self.assert_projection_rejected(mutation)

    def test_source_binding_is_exact(self) -> None:
        report = derive.derive(LEGACY.read_bytes())
        report["source_v1"]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            derive.validate_projection(report, LEGACY.read_bytes())

    def test_exact_replica_consumer_guard(self) -> None:
        mismatch = derive.derive(LEGACY.read_bytes())
        with self.assertRaisesRegex(derive.ReplicaConsistencyStop, "REPLICA_CONSISTENCY_STOP"):
            derive.require_replica_match(mismatch, exact_replicas_required=True)
        self.assertEqual(derive.require_replica_match(mismatch, exact_replicas_required=False), "PROCEED")
        not_run_source = json.loads(LEGACY.read_bytes())
        not_run_source["windows"] = []
        not_run_source["run"].update(windows_produced=0, windows_consumed=0)
        not_run = derive.derive(derive.canonical(not_run_source) + b"\n")
        with self.assertRaisesRegex(derive.ReplicaConsistencyStop, "REPLICA_CONSISTENCY_STOP"):
            derive.require_replica_match(not_run, exact_replicas_required=True)
        matched = derive.derive(derive.canonical(self.matching_source()) + b"\n")
        self.assertEqual(derive.require_replica_match(matched, exact_replicas_required=True), "PROCEED")

    def test_exclusion_record_and_setup_are_exact(self) -> None:
        record = json.loads(EXCLUSION.read_text())
        self.assertEqual(record["excluded_distribution"], {"compiled_cuda_major": 13, "name": "torchaudio", "version": "2.11.0"})
        setup = SETUP.read_text()
        self.assertIn('actual != "2.11.0"', setup)
        self.assertIn('"libcudart.so.13" not in str(exc)', setup)
        self.assertIn("pip uninstall --yes torchaudio", setup)
        self.assertIn("verify_m4_wsl2_text_only_runtime.py", setup)

    @mock.patch("tools.testbed.verify_m4_wsl2_text_only_runtime.importlib.import_module")
    @mock.patch("tools.testbed.verify_m4_wsl2_text_only_runtime.platform.python_version", return_value="3.12.3")
    @mock.patch("tools.testbed.verify_m4_wsl2_text_only_runtime.metadata.version")
    def test_runtime_verifier_requires_absence_and_vllm_import(self, version, _python, import_module) -> None:
        def lookup(name: str) -> str:
            if name == "torchaudio":
                raise metadata.PackageNotFoundError
            return runtime.EXPECTED[name]
        version.side_effect = lookup
        runtime.verify()
        import_module.assert_called_once_with("vllm")

    @mock.patch("tools.testbed.verify_m4_wsl2_text_only_runtime.platform.python_version", return_value="3.12.3")
    @mock.patch("tools.testbed.verify_m4_wsl2_text_only_runtime.metadata.version", return_value="2.11.0")
    def test_runtime_verifier_rejects_residual_torchaudio(self, _version, _python) -> None:
        with self.assertRaisesRegex(RuntimeError, "TORCHAUDIO_EXCLUSION_FAILED"):
            runtime.verify()


if __name__ == "__main__":
    unittest.main()
