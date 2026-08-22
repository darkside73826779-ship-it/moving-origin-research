"""Focused tests for the workflow preflight helper."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_preflight", ROOT / "tools/workflow_preflight.py")
assert SPEC and SPEC.loader
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class WorkflowPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "tests@moving-origin-research.local")
        git(self.repo, "config", "user.name", "MOR Tests")
        (self.repo / "specs/data").mkdir(parents=True)
        for name in ("workflow_preflight_patterns_v1.json", "workflow_preflight_report_schema_v2.json"):
            (self.repo / "specs/data" / name).write_bytes((ROOT / "specs/data" / name).read_bytes())
        (self.repo / "a.txt").write_text("base\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "base")
        self.base = git(self.repo, "rev-parse", "HEAD")
        self.root_patch = mock.patch.object(PREFLIGHT, "ROOT", self.repo)
        self.pattern_patch = mock.patch.object(PREFLIGHT, "PATTERNS", self.repo / "specs/data/workflow_preflight_patterns_v1.json")
        self.schema_patch = mock.patch.object(PREFLIGHT, "SCHEMA", self.repo / "specs/data/workflow_preflight_report_schema_v2.json")
        self.root_patch.start(); self.pattern_patch.start(); self.schema_patch.start()

    def tearDown(self):
        self.schema_patch.stop(); self.pattern_patch.stop(); self.root_patch.stop()
        self.temporary.cleanup()

    @mock.patch.object(PREFLIGHT, "_gitleaks", return_value=("test-gitleaks", 0, []))
    def test_history_events_and_endpoint_projection(self, _scanner):
        (self.repo / "a.txt").write_text("first\n", encoding="utf-8")
        (self.repo / "transient.txt").write_text("temporary\n", encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "add and modify")
        (self.repo / "a.txt").write_text("second\n", encoding="utf-8")
        (self.repo / "transient.txt").unlink()
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "delete and modify")
        tip = git(self.repo, "rev-parse", "HEAD")
        report, code = PREFLIGHT.build_report(self.base, tip)
        self.assertEqual(0, code)
        transient = [row["change_type"] for row in report["path_events"] if row["path"] == "transient.txt"]
        self.assertEqual(["added", "deleted"], transient)
        self.assertFalse(any(row["path"] == "transient.txt" for row in report["paths"]))
        self.assertEqual(list(range(1, len(report["path_events"]) + 1)), [row["event_index"] for row in report["path_events"]])

    @mock.patch.object(PREFLIGHT, "_gitleaks", return_value=("test-gitleaks", 0, []))
    def test_real_private_path_blocks(self, _scanner):
        prohibited_fixture = "location=/" + "home/alice/private/data\n"
        (self.repo / "leak.txt").write_text(prohibited_fixture, encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "leak")
        report, code = PREFLIGHT.build_report(self.base, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(2, code)
        matching = [item for item in report["findings"] if item["class"] == "private_absolute_paths" and item["path"] == "leak.txt"]
        self.assertTrue(matching)
        self.assertTrue(all(item["disposition"] == "BLOCKER" for item in matching))

    @mock.patch.object(PREFLIGHT, "_gitleaks", return_value=("test-gitleaks", 0, []))
    def test_removed_prohibited_content_does_not_block_cleanup(self, _scanner):
        prohibited_fixture = "location=/" + "home/alice/private/data\n"
        (self.repo / "leak.txt").write_text(prohibited_fixture, encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "historical leak")
        cleanup_base = git(self.repo, "rev-parse", "HEAD")
        (self.repo / "leak.txt").write_text("sanitized\n", encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "remove leak")
        report, code = PREFLIGHT.build_report(cleanup_base, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(0, code)
        self.assertEqual([], report["findings"])

    @mock.patch.object(PREFLIGHT, "_gitleaks", return_value=("test-gitleaks", 0, []))
    def test_phone_digit_run_inside_sha_is_not_contact(self, _scanner):
        phone_digits = "".join(("212", "555", "0100"))
        sha1 = "a" * 11 + phone_digits + "b" * 19
        sha256 = "a" * 17 + phone_digits + "b" * 37
        self.assertEqual((40, 64), (len(sha1), len(sha256)))
        (self.repo / "digest.txt").write_text(f"sha1={sha1}\nsha256={sha256}\n", encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "public digest")
        report, code = PREFLIGHT.build_report(self.base, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(0, code)
        self.assertFalse(any(item["class"] == "personal_contact" for item in report["findings"]))

    @mock.patch.object(PREFLIGHT, "_gitleaks", return_value=("test-gitleaks", 0, []))
    def test_genuine_phone_still_blocks(self, _scanner):
        synthetic_phone = "-".join(("212", "555", "0100"))
        (self.repo / "contact.txt").write_text(f"call {synthetic_phone}\n", encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "contact")
        report, code = PREFLIGHT.build_report(self.base, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(2, code)
        self.assertTrue(any(item["class"] == "personal_contact" for item in report["findings"]))

    @mock.patch.object(PREFLIGHT, "_gitleaks", return_value=("test-gitleaks", 0, []))
    def test_safe_provenance_append_does_not_rescan_historical_contact(self, _scanner):
        provenance = self.repo / "docs/rulings/provenance_log.md"
        provenance.parent.mkdir(parents=True)
        synthetic_phone = "-".join(("212", "555", "0100"))
        provenance.write_text(f"historical contact {synthetic_phone}\n", encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "historical provenance")
        append_base = git(self.repo, "rev-parse", "HEAD")
        with provenance.open("a", encoding="utf-8", newline="") as stream:
            stream.write("safe new attestation\n")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "append provenance")
        report, code = PREFLIGHT.build_report(append_base, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(0, code)
        self.assertEqual([], report["findings"])

    @mock.patch.object(PREFLIGHT, "_gitleaks", return_value=("test-gitleaks", 0, []))
    def test_modified_provenance_legacy_span_scans_complete_result(self, _scanner):
        provenance = self.repo / "docs/rulings/provenance_log.md"
        provenance.parent.mkdir(parents=True)
        synthetic_phone = "-".join(("212", "555", "0100"))
        provenance.write_text(f"historical contact {synthetic_phone}\nlegacy marker\n", encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "historical provenance")
        rewrite_base = git(self.repo, "rev-parse", "HEAD")
        provenance.write_text(f"historical contact {synthetic_phone}\nchanged marker\n", encoding="utf-8")
        git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "rewrite legacy span")
        report, code = PREFLIGHT.build_report(rewrite_base, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(2, code)
        matching = [item for item in report["findings"] if item["class"] == "personal_contact"]
        self.assertTrue(matching)
        self.assertTrue(any(item["path"] == "docs/rulings/provenance_log.md" for item in matching))

    def test_invalid_equal_range_is_exit_four(self):
        with self.assertRaises(PREFLIGHT.PreflightError) as caught:
            PREFLIGHT.build_report(self.base, self.base)
        self.assertEqual(4, caught.exception.code)

    def test_scanner_unavailable_is_exit_three(self):
        with mock.patch.object(PREFLIGHT.shutil, "which", return_value=None):
            with self.assertRaises(PREFLIGHT.PreflightError) as caught:
                PREFLIGHT._gitleaks("domain", [(None, b"safe")])
        self.assertEqual(3, caught.exception.code)

    def test_canonical_output_and_sidecar(self):
        output = "reports/preflight.json"
        PREFLIGHT.write_report({"z": 1, "a": "value"}, output)
        raw = (self.repo / output).read_bytes()
        self.assertEqual(b'{"a":"value","z":1}\n', raw)
        expected = __import__("hashlib").sha256(raw).hexdigest().encode("ascii") + b"  preflight.json\n"
        self.assertEqual(expected, (self.repo / f"{output}.sha256").read_bytes())

    def test_configure_root_targets_explicit_worktree(self):
        patterns = PREFLIGHT.PATTERNS
        schema = PREFLIGHT.SCHEMA
        PREFLIGHT.configure_root(self.repo)
        self.assertEqual(self.repo.resolve(), PREFLIGHT.ROOT)
        self.assertEqual(patterns, PREFLIGHT.PATTERNS)
        self.assertEqual(schema, PREFLIGHT.SCHEMA)

    def test_configure_root_rejects_subdirectory(self):
        child = self.repo / "child"
        child.mkdir()
        with self.assertRaises(PREFLIGHT.PreflightError) as caught:
            PREFLIGHT.configure_root(child)
        self.assertEqual(4, caught.exception.code)


if __name__ == "__main__":
    unittest.main()
