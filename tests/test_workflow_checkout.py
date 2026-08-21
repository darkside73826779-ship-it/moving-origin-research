"""Focused integration tests for immutable workflow checkout creation."""

import argparse
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_checkout", ROOT / "tools/workflow_checkout.py")
assert SPEC and SPEC.loader
CHECKOUT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKOUT)


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(list(args), cwd=cwd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class WorkflowCheckoutTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        base = Path(self.temporary.name)
        self.remote = base / "remote.git"
        self.seed = base / "seed"
        self.clone = base / "clone"
        self.workspace = base / "workspace"
        run("git", "init", "--bare", "-q", str(self.remote))
        run("git", "init", "-q", str(self.seed))
        run("git", "config", "user.email", "tests@moving-origin-research.local", cwd=self.seed)
        run("git", "config", "user.name", "MOR Tests", cwd=self.seed)
        (self.seed / "result.txt").write_text("result\n", encoding="utf-8")
        run("git", "add", ".", cwd=self.seed); run("git", "commit", "-qm", "result", cwd=self.seed)
        self.review = run("git", "rev-parse", "HEAD", cwd=self.seed)
        (self.seed / "handoffs").mkdir()
        (self.seed / "handoffs/route.md").write_text("route\n", encoding="utf-8")
        run("git", "add", ".", cwd=self.seed); run("git", "commit", "-qm", "route", cwd=self.seed)
        self.routing = run("git", "rev-parse", "HEAD", cwd=self.seed)
        run("git", "branch", "-M", "intake", cwd=self.seed)
        run("git", "remote", "add", "origin", str(self.remote), cwd=self.seed)
        run("git", "push", "-q", "origin", "refs/heads/intake", cwd=self.seed)
        run("git", "clone", "-q", str(self.remote), str(self.clone))
        self.workspace.mkdir()
        (self.workspace / ".mor-workspace-root").write_bytes(CHECKOUT.MARKER)

    def tearDown(self):
        self.temporary.cleanup()

    def args(self, **updates):
        values = dict(repo=str(self.clone.resolve()), remote="origin", ref="refs/heads/intake",
                      ref_head=self.routing, review_result=self.review, base=self.review,
                      work_branch="critic/review", workspace_root=str(self.workspace.resolve()), work_item="mechanical-review")
        values.update(updates)
        return argparse.Namespace(**values)

    def test_create_receipt_then_cleanup(self):
        receipt = CHECKOUT.create(self.args())
        self.assertTrue(receipt.is_file())
        document = json.loads(receipt.read_text(encoding="utf-8"))
        worktree = Path(document["worktree_path"])
        self.assertEqual(self.routing, run("git", "rev-parse", "HEAD", cwd=worktree))
        self.assertEqual("critic/review", run("git", "branch", "--show-current", cwd=worktree))
        CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self.assertFalse(receipt.exists())
        self.assertFalse(worktree.exists())

    def test_missing_marker_stops(self):
        (self.workspace / ".mor-workspace-root").unlink()
        with self.assertRaises((CHECKOUT.Stop, FileNotFoundError)):
            CHECKOUT.create(self.args())

    def test_non_handoff_routing_commit_stops(self):
        (self.seed / "result.txt").write_text("changed after review\n", encoding="utf-8")
        run("git", "add", ".", cwd=self.seed); run("git", "commit", "-qm", "bad route", cwd=self.seed)
        bad = run("git", "rev-parse", "HEAD", cwd=self.seed)
        run("git", "push", "-q", "origin", "HEAD:refs/heads/bad", cwd=self.seed)
        with self.assertRaises(CHECKOUT.Stop):
            CHECKOUT.create(self.args(ref="refs/heads/bad", ref_head=bad, work_branch="critic/bad"))

    def test_existing_local_branch_stops_before_worktree(self):
        run("git", "branch", "critic/review", self.routing, cwd=self.clone)
        with self.assertRaises(CHECKOUT.Stop):
            CHECKOUT.create(self.args())


if __name__ == "__main__":
    unittest.main()
