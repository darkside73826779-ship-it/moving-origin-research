"""Workflow contract validator regressions (2026-08-21, Regime B)."""

import base64
import copy
import hashlib
import importlib.util
import json
import re
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
CHECKOUT_SPEC = importlib.util.spec_from_file_location("workflow_checkout", ROOT / "tools/workflow_checkout.py")
if CHECKOUT_SPEC is None or CHECKOUT_SPEC.loader is None:
    raise RuntimeError("unable to load checkout helper")
CHECKOUT = importlib.util.module_from_spec(CHECKOUT_SPEC)
CHECKOUT_SPEC.loader.exec_module(CHECKOUT)


class WorkflowContractValidatorTests(unittest.TestCase):
    def handoff(self):
        authority_path = "handoffs/authority.md"
        return {
            "schema_version": "common-handoff-manifest-v1", "date": "2026-08-21", "regime": "B",
            "transfer_kind": "FORMAL_HANDOFF", "work_item": "validator-test", "gate": "schema",
            "sender_role": "WORKFLOW_COORDINATOR", "receiver_role": "ARCHITECT",
            "authority_basis": [{"path": authority_path, "sha": "a" * 40}],
            "remote_ref": "refs/heads/coordinator/validator-test", "base_sha": "b" * 40,
            "routing_ref_sha": "c" * 40, "review_result_sha": None,
            "work_branch": "architect/validator-test",
            "artifacts": {authority_path: "d" * 64}, "checks_performed": ["schema"], "status": "READY",
            "findings": [],
            "scan_attestation": {"base_sha": "b" * 40, "tip_sha": "c" * 40,
                                 "tool_status": "clean", "manual_review": True, "findings": []},
            "next_event": "review", "prohibited_actions": ["merge"],
            "role_extension": {"role": "WORKFLOW_COORDINATOR", "ball_recorded": True},
        }

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
            synthetic_email = "test@" + "example.invalid"
            subprocess.run(["git", "-C", str(root), "-c", "user.name=test", "-c", f"user.email={synthetic_email}",
                            "commit", "-qm", "state"], check=True)
            source = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
                                    text=True, stdout=subprocess.PIPE).stdout.strip()
            value = {"schema_version": "workflow-state-metadata-v1", "as_of_utc": "2026-08-21T21:00:00Z",
                     "source_commit": source, "document_path": "state/STATE.md",
                     "document_sha256": hashlib.sha256(b"state\n").hexdigest(), "supersedes_metadata_sha256": [],
                     "status": "current", "document_role": "durable_state", "owner_role": "INTEGRATOR"}
            MODULE.validate_metadata(value, root)
            document.write_bytes(b"changed worktree bytes\n")
            MODULE.validate_metadata(value, root)
            value["owner_role"] = "RECORDER"
            with self.assertRaises(MODULE.ContractError):
                MODULE.validate_metadata(value, root)

    def test_handoff_rejects_schema_fields_previously_unchecked(self):
        value = self.handoff()
        MODULE.validate_handoff(value)
        mutations = [
            ("date", "2026-02-30"),
            ("remote_ref", "coordinator/validator-test"),
            ("remote_ref", "refs/heads/coordinator/../escape"),
            ("work_branch", "-invalid"),
            ("work_branch", "architect/../escape"),
            ("checks_performed", [""]),
            ("status", "UNKNOWN"),
            ("prohibited_actions", []),
            ("status", []),
        ]
        for field, replacement in mutations:
            with self.subTest(field=field, replacement=replacement):
                bad = copy.deepcopy(value)
                bad[field] = replacement
                with self.assertRaises(MODULE.ContractError):
                    MODULE.validate_handoff(bad)

        bad = copy.deepcopy(value)
        bad["scan_attestation"]["manual_review"] = "yes"
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_handoff(bad)
        bad = copy.deepcopy(value)
        bad["authority_basis"][0]["unexpected"] = True
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_handoff(bad)
        bad = copy.deepcopy(value)
        bad["role_extension"]["ball_recorded"] = 1
        with self.assertRaises(MODULE.ContractError):
            MODULE.validate_handoff(bad)

    def test_handoff_ref_and_branch_rules_match_checkout_helper(self):
        schema = json.loads((ROOT / "specs/data/common_handoff_manifest_schema_v1.json").read_text(encoding="utf-8"))
        remote_pattern = schema["properties"]["remote_ref"]["pattern"]
        branch_pattern = schema["properties"]["work_branch"]["pattern"]
        remote_values = ["refs/heads/architect/work", "architect/work", "refs/heads/a/../b",
                         "refs/tags/a", "refs/heads/a//b", "refs/heads/a/"]
        for candidate in remote_values:
            checkout_accepts = bool(CHECKOUT.REF_RE.fullmatch(candidate)) and ".." not in candidate.split("/")
            validator_accepts = bool(MODULE.REMOTE_REF.fullmatch(candidate)) and ".." not in candidate.split("/")
            schema_accepts = bool(re.fullmatch(remote_pattern, candidate))
            self.assertEqual(checkout_accepts, validator_accepts, candidate)
            self.assertEqual(checkout_accepts, schema_accepts, candidate)
        branch_values = ["architect/work", "custom/work", "-bad", "x..y", "x/./y", "x.", "x/", "/x", "x//y"]
        for candidate in branch_values:
            checkout_accepts = (bool(CHECKOUT.BRANCH_RE.fullmatch(candidate))
                                and not candidate.endswith((".", "/")) and ".." not in candidate)
            validator_accepts = (bool(MODULE.WORK_BRANCH.fullmatch(candidate))
                                 and not candidate.endswith((".", "/")) and ".." not in candidate)
            schema_accepts = bool(re.fullmatch(branch_pattern, candidate))
            self.assertEqual(checkout_accepts, validator_accepts, candidate)
            self.assertEqual(checkout_accepts, schema_accepts, candidate)
    def test_metadata_rejects_schema_fields_previously_unchecked(self):
        value = {"schema_version": "workflow-state-metadata-v1", "as_of_utc": "2026-08-21T21:00:00Z",
                 "source_commit": "a" * 40, "document_path": "state/STATE.md",
                 "document_sha256": "b" * 64, "supersedes_metadata_sha256": ["c" * 64],
                 "status": "current", "document_role": "durable_state", "owner_role": "INTEGRATOR"}
        MODULE.validate_metadata(value)
        mutations = [
            ("as_of_utc", "2026-08-21 21:00:00Z"),
            ("status", "CURRENT"),
            ("supersedes_metadata_sha256", "c" * 64),
            ("supersedes_metadata_sha256", ["c" * 64, "c" * 64]),
            ("supersedes_metadata_sha256", [7]),
        ]
        for field, replacement in mutations:
            with self.subTest(field=field, replacement=replacement):
                bad = copy.deepcopy(value)
                bad[field] = replacement
                with self.assertRaises(MODULE.ContractError):
                    MODULE.validate_metadata(bad)

    def test_metadata_fails_closed_when_source_blob_is_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            value = {"schema_version": "workflow-state-metadata-v1", "as_of_utc": "2026-08-21T21:00:00Z",
                     "source_commit": "a" * 40, "document_path": "state/STATE.md",
                     "document_sha256": "b" * 64, "supersedes_metadata_sha256": [],
                     "status": "current", "document_role": "durable_state", "owner_role": "INTEGRATOR"}
            with self.assertRaisesRegex(MODULE.ContractError, "METADATA_SOURCE_COMMIT_MISSING"):
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

    def test_judge_envelope_rejects_schema_invalid_filename_and_length(self):
        raw = b"# Ruling\n"
        envelope = {"schema_version": "judge-custody-envelope-v1", "filename": "ruling.md",
                    "media_type": "text/markdown; charset=utf-8", "encoding": "base64-rfc4648-no-whitespace",
                    "byte_length": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                    "content_base64": base64.b64encode(raw).decode("ascii")}
        for field, replacement in (("filename", "../ruling.md"), ("byte_length", True),
                                   ("byte_length", 4194305), ("sha256", 7)):
            with self.subTest(field=field):
                bad = copy.deepcopy(envelope)
                bad[field] = replacement
                with self.assertRaises(MODULE.ContractError):
                    MODULE.validate_judge_envelope(bad)

    def test_loader_rejects_duplicate_keys_and_nonfinite_numbers(self):
        with tempfile.TemporaryDirectory() as folder:
            duplicate = Path(folder) / "duplicate.json"
            duplicate.write_bytes(b'{"a":1,"a":2}\n')
            with self.assertRaisesRegex(MODULE.ContractError, "DUPLICATE_JSON_KEY"):
                MODULE._load(duplicate)
            nonfinite = Path(folder) / "nonfinite.json"
            nonfinite.write_bytes(b'{"a":NaN}\n')
            with self.assertRaisesRegex(MODULE.ContractError, "NONFINITE_JSON_NUMBER"):
                MODULE._load(nonfinite)

    def test_rollback_cascade(self):
        contract = json.loads((ROOT / "specs/data/workflow_stage_rollback_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(["S3", "S4", "S5"], MODULE.rollback_cascade("S3", contract))
        self.assertEqual(["S5"], MODULE.rollback_cascade("S5", contract))


if __name__ == "__main__":
    unittest.main()
