"""Exact Git-blob sidecar checks for workflow contracts (2026-08-21, Regime B)."""

import hashlib
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git_blob(path: str) -> bytes:
    for name in (f":{path}", f"HEAD:{path}"):
        result = subprocess.run(["git", "-C", str(ROOT), "show", name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout
    raise AssertionError(f"missing Git blob: {path}")


class WorkflowSidecarTests(unittest.TestCase):
    def test_all_workflow_contract_sidecars(self):
        names = {
            *ROOT.glob("specs/data/workflow_*.json.sha256"),
            *ROOT.glob("specs/data/common_handoff_manifest_schema_v1.json.sha256"),
            *ROOT.glob("specs/data/executability_trace*_v1.json.sha256"),
            *ROOT.glob("state/*.metadata.json.sha256"),
        }
        self.assertTrue(names)
        for sidecar in sorted(names):
            relative_sidecar = sidecar.relative_to(ROOT).as_posix()
            relative_target = relative_sidecar.removesuffix(".sha256")
            line = git_blob(relative_sidecar).decode("ascii")
            self.assertRegex(line, r"^[0-9a-f]{64}  [^\r\n]+\n$")
            claimed, basename = line.rstrip("\n").split("  ", 1)
            self.assertEqual(Path(relative_target).name, basename)
            self.assertEqual(claimed, hashlib.sha256(git_blob(relative_target)).hexdigest(), relative_target)


if __name__ == "__main__":
    unittest.main()
