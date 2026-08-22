"""Tests for the prospective two-axis report and text-only dependency lock.

Date: 2026-08-22
Regime: B
"""
from __future__ import annotations

import hashlib
import importlib.metadata as metadata
import json
import unittest
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
        source = json.loads(LEGACY.read_bytes())
        for row in source["windows"]:
            row["outputs_agree"] = True
        source["run"]["all_outputs_agree"] = True
        source["failure_codes"] = []
        result = derive.derive(derive.canonical(source) + b"\n")
        self.assertEqual(result["structural_status"], "PASS")
        self.assertEqual(result["replica_consistency_status"], "MATCH")
        self.assertEqual(result["replica_consistency"]["mismatch_count"], 0)

    def test_structural_failure_is_independent_of_replica_match(self) -> None:
        source = json.loads(LEGACY.read_bytes())
        source["failure_codes"] = ["CLEANUP_INCOMPLETE"]
        source["run"]["cleanup_gpu_used_mib"] = 1
        result = derive.derive(derive.canonical(source) + b"\n")
        self.assertEqual(result["structural_status"], "BLOCKED")
        self.assertEqual(result["replica_consistency_status"], "MISMATCH")

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
