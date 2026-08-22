"""Focused tests for canonical role-return publication preparation."""

import argparse
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_return", ROOT / "tools/workflow_return.py")
assert SPEC and SPEC.loader
RETURN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RETURN)


def run(*args: str, cwd: Path) -> str:
    return subprocess.run(list(args), cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class WorkflowReturnTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.remote = root / "remote.git"
        self.repo = root / "repo"
        self.external = root / "external"
        self.external.mkdir()
        run("git", "init", "--bare", "-q", str(self.remote), cwd=root)
        run("git", "init", "-q", str(self.repo), cwd=root)
        run("git", "config", "user.email", "tests@moving-origin-research.local", cwd=self.repo)
        run("git", "config", "user.name", "MOR Tests", cwd=self.repo)
        (self.repo / "specs").mkdir()
        (self.repo / "specs/base.txt").write_text("base\n", encoding="utf-8")
        run("git", "add", ".", cwd=self.repo)
        run("git", "commit", "-qm", "base", cwd=self.repo)
        run("git", "branch", "-M", "architect/result", cwd=self.repo)
        run("git", "remote", "add", "origin", str(self.remote), cwd=self.repo)
        run("git", "push", "-q", "-u", "origin", "architect/result", cwd=self.repo)
        self.base = run("git", "rev-parse", "HEAD", cwd=self.repo)
        (self.repo / "specs/result.txt").write_text("result\n", encoding="utf-8")
        run("git", "add", "specs/result.txt", cwd=self.repo)
        self.handoff = self.external / "handoff.md"
        self.handoff.write_text("formal return\n", encoding="utf-8")
        self.template = self.external / "manifest.json"
        self.template.write_text(json.dumps(self._template()), encoding="utf-8")
        self.classification = self.external / "classifications.json"

    def tearDown(self):
        self.temporary.cleanup()

    def _template(self):
        zero40 = "0" * 40
        return {
            "schema_version": "common-handoff-manifest-v1", "date": "2026-08-21",
            "regime": "B", "transfer_kind": "FORMAL_HANDOFF", "work_item": "return-helper-test",
            "gate": "test gate", "sender_role": "ARCHITECT", "receiver_role": "CRITIC",
            "authority_basis": [{"path": "specs/base.txt", "sha": self.base}],
            "remote_ref": "refs/heads/placeholder", "base_sha": zero40,
            "routing_ref_sha": zero40, "review_result_sha": zero40,
            "work_branch": "critic/test", "artifacts": {"specs/base.txt": "0" * 64},
            "checks_performed": ["helper"], "status": "READY", "findings": [],
            "scan_attestation": {"base_sha": zero40, "tip_sha": zero40, "tool_status": "clean",
                                 "manual_review": False, "findings": []},
            "next_event": "review", "prohibited_actions": ["force push"],
            "role_extension": {"role": "ARCHITECT", "changelog_paths": [], "diff_self_inspection": True},
        }

    def args(self, **updates):
        values = dict(
            repo_root=str(self.repo), remote="origin", base=self.base,
            result_branch="architect/result", routing_branch="architect/result-routing",
            manifest_branch="architect/result-manifest", work_branch="critic/test",
            handoff_source=str(self.handoff), handoff_path="handoffs/return.md",
            manifest_template=str(self.template), manifest_path="handoffs/return.manifest.json",
            classification_template=str(self.classification), result_message="result",
            routing_message="route", manifest_message="manifest",
            commit_date="2026-08-21T20:00:00-04:00", classifications=None,
            manual_review=False, push=False,
        )
        values.update(updates)
        return argparse.Namespace(**values)

    @staticmethod
    def clean_report(repo: Path, base: str, tip: str, label: str):
        return ({"status": "CLEAN", "findings": [], "base_sha": base, "tip_sha": tip}, "a" * 64)

    def test_prepares_distinct_topology_and_complete_inventory_without_push(self):
        with mock.patch.object(RETURN, "run_preflight", side_effect=self.clean_report):
            result = RETURN.publish(self.args())
        self.assertEqual(result["result_sha"], run("git", "rev-parse", "architect/result", cwd=self.repo))
        self.assertEqual(["handoffs/return.md"], run(
            "git", "diff", "--name-only", result["result_sha"], result["routing_sha"], cwd=self.repo
        ).splitlines())
        self.assertEqual(["handoffs/return.manifest.json"], run(
            "git", "diff", "--name-only", result["routing_sha"], result["manifest_sha"], cwd=self.repo
        ).splitlines())
        manifest = json.loads(run("git", "show", f"{result['manifest_sha']}:handoffs/return.manifest.json", cwd=self.repo))
        self.assertEqual({"handoffs/return.md", "specs/base.txt", "specs/result.txt"}, set(manifest["artifacts"]))
        self.assertEqual(result["routing_sha"], manifest["routing_ref_sha"])
        self.assertEqual("", run("git", "status", "--porcelain", cwd=self.repo))
        self.assertIsNone(RETURN._remote_oid(self.repo, "origin", "architect/result-routing"))

    def test_staged_handoff_is_rejected_without_ref_changes(self):
        (self.repo / "handoffs").mkdir()
        (self.repo / "handoffs/bad.md").write_text("bad\n", encoding="utf-8")
        run("git", "add", "handoffs/bad.md", cwd=self.repo)
        with self.assertRaises(RETURN.Stop):
            RETURN.publish(self.args())
        self.assertEqual(self.base, run("git", "rev-parse", "HEAD", cwd=self.repo))

    def test_findings_emit_classification_template_and_prevent_push(self):
        finding = {"detector": "fixed_regex", "class": "personal_contact", "path": "specs/result.txt"}
        blocked = ({"status": "BLOCKED", "findings": [finding]}, "b" * 64)
        with mock.patch.object(RETURN, "run_preflight", return_value=blocked), \
             mock.patch.object(RETURN, "_push") as push:
            with self.assertRaises(RETURN.Stop):
                RETURN.publish(self.args(push=True))
        push.assert_not_called()
        document = json.loads(self.classification.read_text(encoding="utf-8"))
        self.assertEqual(2, len(document["classifications"]))
        self.assertTrue(all(row["disposition"] == "UNCLASSIFIED" for row in document["classifications"]))
        self.assertEqual(self.base, run("git", "rev-parse", "HEAD", cwd=self.repo))

    def test_clean_push_uses_guarded_publisher(self):
        with mock.patch.object(RETURN, "run_preflight", side_effect=self.clean_report), \
             mock.patch.object(RETURN, "_push") as push:
            result = RETURN.publish(self.args(push=True, manual_review=True))
        push.assert_called_once()
        branches = push.call_args.args[2]
        self.assertEqual(result["result_sha"], branches["architect/result"])

    def test_explicit_complete_classification_permits_guarded_push(self):
        finding = {"detector": "fixed_regex", "class": "personal_contact", "path": "specs/result.txt"}
        blocked = ({"status": "BLOCKED", "findings": [finding]}, "b" * 64)
        with mock.patch.object(RETURN, "run_preflight", return_value=blocked):
            with self.assertRaises(RETURN.Stop):
                RETURN.publish(self.args(push=True, manual_review=True))
        approved = self.external / "approved.json"
        document = json.loads(self.classification.read_text(encoding="utf-8"))
        for row in document["classifications"]:
            row["disposition"] = "ACCEPTABLE_IMMUTABLE_IDENTITY"
            row["rationale"] = "Match is wholly inside a governed immutable commit identity."
        approved.write_text(json.dumps(document), encoding="utf-8")
        with mock.patch.object(RETURN, "run_preflight", return_value=blocked), \
             mock.patch.object(RETURN, "_push") as push:
            RETURN.publish(self.args(push=True, manual_review=True, classifications=str(approved)))
        push.assert_called_once()

    def test_push_requires_explicit_manual_review(self):
        with mock.patch.object(RETURN, "run_preflight", side_effect=self.clean_report), \
             mock.patch.object(RETURN, "_push") as push:
            with self.assertRaisesRegex(RETURN.Stop, "manual review"):
                RETURN.publish(self.args(push=True))
        push.assert_not_called()

    def test_classification_detector_and_class_are_identity_bound(self):
        finding = {"detector": "fixed_regex", "class": "personal_contact", "path": "specs/result.txt"}
        blocked = ({"status": "BLOCKED", "findings": [finding]}, "b" * 64)
        with mock.patch.object(RETURN, "run_preflight", return_value=blocked):
            with self.assertRaises(RETURN.Stop):
                RETURN.publish(self.args(push=True, manual_review=True))
        approved = self.external / "tampered.json"
        document = json.loads(self.classification.read_text(encoding="utf-8"))
        for row in document["classifications"]:
            row["disposition"] = "ACCEPTABLE_IMMUTABLE_IDENTITY"
            row["rationale"] = "Reviewed immutable identity."
        document["classifications"][0]["class"] = "private_key"
        approved.write_text(json.dumps(document), encoding="utf-8")
        with mock.patch.object(RETURN, "run_preflight", return_value=blocked), \
             mock.patch.object(RETURN, "_push") as push:
            with self.assertRaisesRegex(RETURN.Stop, "identity mismatch"):
                RETURN.publish(self.args(push=True, manual_review=True, classifications=str(approved)))
        push.assert_not_called()


if __name__ == "__main__":
    unittest.main()
