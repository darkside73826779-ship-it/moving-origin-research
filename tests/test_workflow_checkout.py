"""Focused integration tests for immutable workflow checkout creation."""

import argparse
import hashlib
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
        run("git", "config", "user.email", "tests@moving-origin-research.local", cwd=self.clone)
        run("git", "config", "user.name", "MOR Tests", cwd=self.clone)
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
        self.assertEqual("origin", document["remote"])
        worktree = Path(document["worktree_path"])
        self.assertEqual(self.routing, run("git", "rev-parse", "HEAD", cwd=worktree))
        self.assertEqual("critic/review", run("git", "branch", "--show-current", cwd=worktree))
        CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self.assertFalse(receipt.exists())
        self.assertFalse(worktree.exists())

    def _created(self):
        receipt = CHECKOUT.create(self.args())
        document = json.loads(receipt.read_text(encoding="utf-8"))
        return receipt, document, Path(document["worktree_path"])

    def _discard(self, receipt: Path, worktree: Path):
        run("git", "worktree", "remove", "--force", str(worktree), cwd=self.clone)
        if receipt.exists():
            receipt.unlink()

    def _advance_and_publish(self, worktree: Path):
        (worktree / "review.txt").write_text("reviewed\n", encoding="utf-8")
        run("git", "add", "review.txt", cwd=worktree)
        run("git", "commit", "-qm", "review result", cwd=worktree)
        head = run("git", "rev-parse", "HEAD", cwd=worktree)
        run("git", "push", "-qu", "origin", "HEAD:refs/heads/critic/review", cwd=worktree)
        return head

    def test_cleanup_accepts_exact_published_fast_forward(self):
        receipt, _, worktree = self._created()
        self._advance_and_publish(worktree)
        CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self.assertFalse(receipt.exists())
        self.assertFalse(worktree.exists())

    def test_cleanup_accepts_legacy_receipt_with_unique_exact_remote(self):
        receipt, document, worktree = self._created()
        document.pop("remote")
        payload = dict(document)
        payload.pop("receipt_sha256")
        document["receipt_sha256"] = hashlib.sha256(CHECKOUT._canonical(payload)).hexdigest()
        receipt.write_bytes(CHECKOUT._canonical(document) + b"\n")
        self._advance_and_publish(worktree)
        CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self.assertFalse(worktree.exists())

    def test_cleanup_rejects_unpublished_fast_forward(self):
        receipt, _, worktree = self._created()
        (worktree / "review.txt").write_text("local only\n", encoding="utf-8")
        run("git", "add", "review.txt", cwd=worktree)
        run("git", "commit", "-qm", "local only", cwd=worktree)
        with self.assertRaises(CHECKOUT.Stop):
            CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self._discard(receipt, worktree)

    def test_cleanup_rejects_published_diverged_tip(self):
        receipt, _, worktree = self._created()
        tree = run("git", "rev-parse", "HEAD^{tree}", cwd=worktree)
        unrelated = run("git", "commit-tree", tree, "-m", "unrelated", cwd=worktree)
        run("git", "reset", "--hard", "-q", unrelated, cwd=worktree)
        run("git", "push", "-q", "origin", "+HEAD:refs/heads/critic/review", cwd=worktree)
        with self.assertRaises(CHECKOUT.Stop):
            CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self._discard(receipt, worktree)

    def test_cleanup_rejects_branch_identity_change(self):
        receipt, _, worktree = self._created()
        run("git", "branch", "-m", "critic/renamed", cwd=worktree)
        with self.assertRaises(CHECKOUT.Stop):
            CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self._discard(receipt, worktree)

    def test_cleanup_rejects_dirty_worktree(self):
        receipt, _, worktree = self._created()
        (worktree / "untracked.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaises(CHECKOUT.Stop):
            CHECKOUT.cleanup(argparse.Namespace(receipt=str(receipt.resolve())))
        self._discard(receipt, worktree)

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
