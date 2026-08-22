"""Construction tests for the custody-free dual-model crash-cart package.

Date: 2026-08-21
Regime: B
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import jsonschema

from tools.testbed import run_m4_wsl2_dual_model_probe as probe


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "specs/data/m4_wsl2_dual_model_probe_report_schema_v1.json"
FIXTURE = ROOT / "specs/data/m4_wsl2_dual_model_probe_synthetic_fixture_v1.json"
MEASURED_REPORT = (
    ROOT
    / "artifacts/m4_wsl2_preexecution_testbed/"
    "m4_wsl2_dual_model_probe_report_2026-08-21.json"
)


class DualModelProbeConstructionTests(unittest.TestCase):
    def test_exact_public_prompt_zero_digest(self) -> None:
        self.assertEqual(
            hashlib.sha256(probe.prompt_for(0)).hexdigest(),
            "13921e81adf8b123ab5158ccb9323f9411305f2d3093f8ee31351e20f73e0e7b",
        )

    def test_synthetic_fixture_validates(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(fixture)
        probe.validate_report_semantics(fixture)

    def test_semantic_count_mismatch_rejects(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        fixture["run"]["windows_produced"] = 1
        with self.assertRaises(probe.ProbeFailure) as caught:
            probe.validate_report_semantics(fixture)
        self.assertEqual(caught.exception.code, "REPORT_SCHEMA_VALIDATION_FAILED")

    def test_semantic_full_queue_requires_positive_block_time(self) -> None:
        report = probe.base_report()
        row = {
            "candidate": {
                "completed_ns": 30,
                "output_sha256": "a" * 64,
                "output_token_count": 1,
                "started_ns": 10,
            },
            "consumption_ordinal": 0,
            "dequeued_ns": 8,
            "dropped": False,
            "enqueue_ns": 5,
            "execution_overlap_ns": 19,
            "execution_overlapped": True,
            "launch_skew_ns": 1,
            "ordinal": 0,
            "order_preserved": True,
            "outputs_agree": True,
            "peer": {
                "completed_ns": 31,
                "output_sha256": "a" * 64,
                "output_token_count": 1,
                "started_ns": 11,
            },
            "producer_block_ns": 0,
            "producer_observed_full": True,
            "prompt_sha256": hashlib.sha256(probe.prompt_for(0)).hexdigest(),
            "queue_wait_ns": 3,
        }
        report["windows"] = [row]
        report["run"].update(
            {
                "all_executions_overlap": True,
                "all_outputs_agree": True,
                "max_launch_skew_ns": 1,
                "producer_backpressure_observed": True,
                "producer_blocked_count": 1,
                "windows_consumed": 1,
                "windows_produced": 1,
            }
        )
        with self.assertRaises(probe.ProbeFailure):
            probe.validate_report_semantics(report)

    def test_intermediate_symlink_root_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            actual = base / "actual"
            actual.mkdir()
            linked = base / "linked"
            linked.symlink_to(actual, target_is_directory=True)
            with self.assertRaises(probe.ProbeFailure) as caught:
                probe.verify_model_root(str(linked))
            self.assertEqual(caught.exception.code, "MODEL_ROOT_IDENTITY_MISMATCH")

    def test_cross_root_hardlink_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root_a = Path(raw) / "a"
            root_b = Path(raw) / "b"
            root_a.mkdir()
            root_b.mkdir()
            name = next(iter(probe.MODEL_FILES))
            (root_a / name).write_bytes(b"synthetic")
            os.link(root_a / name, root_b / name)
            with self.assertRaises(probe.ProbeFailure) as caught:
                probe.verify_distinct_model_roots(root_a, root_b)
            self.assertEqual(caught.exception.code, "MODEL_ROOTS_NOT_DISTINCT")

    @unittest.skipUnless(os.name == "posix", "process-group signal semantics are POSIX")
    def test_supervisor_terminates_process_group(self) -> None:
        process = mock.Mock()
        process.pid = 1234
        process.poll.return_value = None
        process.wait.return_value = 0
        with mock.patch("os.killpg") as killpg:
            probe.terminate_process_group(process)
        killpg.assert_called_once_with(1234, probe.signal.SIGTERM)

    def test_fixture_has_no_private_path_or_rendered_output_fields(self) -> None:
        raw = FIXTURE.read_text(encoding="utf-8")
        self.assertNotIn("/mnt/", raw)
        self.assertNotIn("\\\\", raw)
        fixture = json.loads(raw)
        serialized_keys = set()

        def collect(value: object) -> None:
            if isinstance(value, dict):
                serialized_keys.update(value)
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(fixture)
        self.assertFalse({"model_a", "model_b", "output_text", "prompt_text"} & serialized_keys)

    def test_schema_rejects_unrequested_private_path_field(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        fixture["model_root"] = "/private/model/root"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(schema).validate(fixture)

    def test_measured_report_validates_and_matches_identity(self) -> None:
        report = json.loads(MEASURED_REPORT.read_text(encoding="utf-8"))
        probe.validate_report(report, SCHEMA)
        self.assertEqual(
            hashlib.sha256(MEASURED_REPORT.read_bytes()).hexdigest(),
            "1f42c9e4ccc1b140e62e32fedcbf75124fbb514f2ae5129781183da12a8093ac",
        )
        self.assertEqual(report["run"]["windows_produced"], len(report["windows"]))
        self.assertEqual(report["run"]["windows_consumed"], len(report["windows"]))

    def test_missing_private_root_fails_without_disclosure(self) -> None:
        with self.assertRaises(probe.ProbeFailure) as caught:
            probe.verify_model_root(None)
        self.assertEqual(caught.exception.code, "MODEL_ROOT_MISSING")


if __name__ == "__main__":
    unittest.main()
