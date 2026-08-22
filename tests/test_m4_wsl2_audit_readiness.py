"""Custody-free construction tests for the WSL2 audit-readiness command."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "m4_wsl2_audit_readiness",
    ROOT / "tools/testbed/run_m4_wsl2_audit_readiness.py",
)
assert SPEC and SPEC.loader
READINESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(READINESS)
SCHEMA = ROOT / "specs/data/m4_wsl2_audit_readiness_report_schema_v1.json"
EXAMPLE = ROOT / "specs/data/m4_wsl2_audit_readiness_blocked_example_v1.json"
CONTRACT = ROOT / "specs/data/m4_wsl2_audit_readiness_contract_v1.json"


class M4Wsl2AuditReadinessTests(unittest.TestCase):
    def test_schema_and_blocked_example(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(example)

    def test_contract_binds_immutable_v12_and_recommended_v13(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(READINESS.BASE_TAG, contract["immutable_base"]["tag"])
        self.assertEqual(READINESS.BASE_TAG_OBJECT, contract["immutable_base"]["tag_object_sha1"])
        self.assertEqual(READINESS.BASE_COMMIT, contract["immutable_base"]["peeled_commit_sha1"])
        self.assertEqual(READINESS.RECOMMENDED_TAG, contract["recommended_tag"])
        READINESS.check_immutable_locks(ROOT, contract)

    def test_existing_diagnostic_dependency_lock_is_complete(self) -> None:
        lock = {}
        for row in (ROOT / "tools/testbed/requirements-m4-wsl2-diagnostic.txt").read_text(encoding="utf-8").splitlines():
            if row.startswith("--"):
                continue
            name, version = row.split("==", 1)
            lock[name] = version
        self.assertEqual(READINESS.DIAGNOSTIC_PACKAGES, lock)

    def test_gpu_smoke_is_no_network_read_only_and_mount_free(self) -> None:
        command = READINESS.gpu_smoke_command()
        joined = "\0".join(command)
        self.assertIn("--pull=never", command)
        self.assertIn("--read-only", command)
        self.assertIn("--network\0none", joined)
        for forbidden in ("--mount", "--volume", "--env", "-v", "-e"):
            self.assertNotIn(forbidden, command)

    def test_report_has_no_private_input_surface(self) -> None:
        report = READINESS.base_report()
        raw = json.dumps(report, sort_keys=True)
        for forbidden in ("model_root", "tokenizer", "prompt", "seed_value", "score", "/mnt/", "C:\\\\"):
            self.assertNotIn(forbidden, raw)

    def test_schema_rejects_unrequested_private_path_field(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        example["model_root"] = "/private/model"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(schema).validate(example)

    def test_lf_validator_rejects_crlf(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "bad.json").write_bytes(b"{}\r\n")
            with mock.patch.object(READINESS, "run") as mocked_run, self.assertRaises(READINESS.ReadinessStop) as raised:
                READINESS.check_lf_and_sidecars(root, {"lf_paths": ["bad.json"]})
            mocked_run.assert_not_called()
            self.assertEqual("LF_BYTES_MISMATCH", raised.exception.code)

    def test_check_order_is_exact(self) -> None:
        self.assertEqual(READINESS.CHECK_IDS, [check_id for check_id, _ in READINESS.CHECKS])
        example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        READINESS.validate_report_semantics(example)
        example["checks"][0], example["checks"][1] = example["checks"][1], example["checks"][0]
        with self.assertRaises(READINESS.ReadinessStop):
            READINESS.validate_report_semantics(example)


if __name__ == "__main__":
    unittest.main()
