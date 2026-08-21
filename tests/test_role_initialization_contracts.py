"""Mechanical consistency checks for all seven role initializations."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLE_DIR = ROOT / "state/role_initialization"
ROLES = ("WORKFLOW_COORDINATOR", "ARCHITECT", "CRITIC", "TASK_BUILDER", "INTEGRATOR", "RECORDER", "JUDGE")


class RoleInitializationContractTests(unittest.TestCase):
    def test_universal_current_contracts(self):
        for role in ROLES:
            text = (ROLE_DIR / f"{role}_INITIALIZATION.md").read_text(encoding="utf-8")
            with self.subTest(role=role):
                self.assertIn("current ledger metadata", text)
                self.assertIn("tools/workflow_contract_validator.py", text)
                self.assertIn("tools/workflow_preflight.py", text)
                self.assertIn("specs/data/workflow_routing_table_v1.json", text)
                self.assertIn("common_handoff_manifest_schema_v1.json", text)
                self.assertIn("workflow_stage_rollback_v1.json", text)
                if role == "WORKFLOW_COORDINATOR":
                    self.assertIn("directly to the authorized persistent role", text)
                else:
                    self.assertIn("directly to WORKFLOW COORDINATOR", text)
                self.assertIn("same-role", text.lower())
                self.assertIn("task/thread/session", text.lower())
                self.assertNotIn("Clone or checkout the named base", text)
                self.assertNotIn("courier-only scoring", text)

    def test_role_specific_owner_fences(self):
        integrator = (ROLE_DIR / "INTEGRATOR_INITIALIZATION.md").read_text(encoding="utf-8")
        recorder = (ROLE_DIR / "RECORDER_INITIALIZATION.md").read_text(encoding="utf-8")
        judge = (ROLE_DIR / "JUDGE_INITIALIZATION.md").read_text(encoding="utf-8")
        critic = (ROLE_DIR / "CRITIC_INITIALIZATION.md").read_text(encoding="utf-8")
        self.assertIn("sole writer of `state/STATE.md`", integrator)
        self.assertIn("RECORDER-owned custody/provenance", recorder)
        self.assertIn("already-used/invalid filename", recorder)
        self.assertIn("does not push its ruling", judge)
        self.assertIn("do not branch from `base_sha`", critic)


if __name__ == "__main__":
    unittest.main()
