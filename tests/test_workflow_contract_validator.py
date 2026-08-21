"""Workflow contract validator regressions (2026-08-21, Regime B)."""

import base64
import copy
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_contract_validator", ROOT / "tools/workflow_contract_validator.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load validator")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WorkflowContractValidatorTests(unittest.TestCase):
    def trace(self):
        row = {
            "input_id": "INPUT_A", "kind": "fixture", "repository_path": "specs/data/a.json",
            "producer_role": "ARCHITECT", "consumer_roles": ["CRITIC", "TASK_BUILDER"],
            "exact_value_or_schema_source": "literal", "canonicalization": "rfc8785",
            "expected_sha256": "1" * 64, "creation_phase": "specification", "status": "READY",
            "architect_verification_id": "A-1", "critic_verification_id": "C-1",
            "taskbuilder_verification_id": "T-1", "failure_disposition": "SPECIFICATION_STOP",
        }
        return {"schema_version": "executability-trace-v1", "date": "2026-08-21", "regime": "B", "specification_path": "specs/a.md", "specification_sha": "a" * 40, "rows": [row]}

    def test_disposition_binds_order_digest_and_role_id(self):
        trace = self.trace()
        raw = MODULE.canonical_bytes(trace)
        result = {
            "schema_version": "executability-trace-disposition-v1", "date": "2026-08-21", "regime": "B",
            "reviewer_role": "CRITIC", "source_trace_path": "specs/data/trace.json",
            "source_trace_sha256": hashlib.sha256(raw).hexdigest(), "source_specification_sha": "a" * 40,
            "rows": [{"input_id": "INPUT_A", "source_row_sha256": hashlib.sha256(MODULE.canonical_bytes(trace["rows"][0])).hexdigest(),
                      "verification_id": "C-1", "disposition": "VERIFIED", "evidence_paths": [], "finding": None}],
            "overall_disposition": "VERIFIED",
        }
        MODULE.validate_disposition(result, trace, raw)
        bad = copy.deepcopy(result)
        bad["rows"][0]["verification_id"] = "T-1"
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_disposition(bad, trace, raw)

    def test_metadata_owner_and_exact_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "state").mkdir()
            document = root / "state/STATE.md"
            document.write_bytes(b"state\n")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "state/STATE.md"], check=True)
            value = {"schema_version": "workflow-state-metadata-v1", "as_of_utc": "2026-08-21T21:00:00Z",
                     "source_commit": "a" * 40, "document_path": "state/STATE.md",
                     "document_sha256": hashlib.sha256(b"state\n").hexdigest(), "supersedes_metadata_sha256": [],
                     "status": "current", "document_role": "durable_state", "owner_role": "INTEGRATOR"}
            MODULE.validate_metadata(value, root)
            value["owner_role"] = "RECORDER"
            with self.assertRaises(MODULE.ContractError):
                MODULE.validate_metadata(value, root)

    def test_judge_envelope_exact_bytes(self):
        raw = b"# Ruling\n"
        envelope = {"schema_version": "judge-custody-envelope-v1", "filename": "ruling.md",
                    "media_type": "text/markdown; charset=utf-8", "encoding": "base64-rfc4648-no-whitespace",
                    "byte_length": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                    "content_base64": base64.b64encode(raw).decode("ascii")}
        self.assertEqual(raw, MODULE.validate_judge_envelope(envelope))
        envelope["content_base64"] = base64.b64encode(b"# Changed\n").decode("ascii")
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_judge_envelope(envelope)

    def test_rollback_cascade(self):
        contract = json.loads((ROOT / "specs/data/workflow_stage_rollback_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(["S3", "S4", "S5"], MODULE.rollback_cascade("S3", contract))
        self.assertEqual(["S5"], MODULE.rollback_cascade("S5", contract))


if __name__ == "__main__":
    unittest.main()
