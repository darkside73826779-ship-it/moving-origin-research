"""Custody-free validation tests for the M4 mutation apparatus itself."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests import run_m4_post_tokenizer_mutation_tests as apparatus


PASS_TARGET = "tests.test_m4_post_tokenizer_mutation_runner.ProbeFixtures.case_pass"
FAIL_TARGET = "tests.test_m4_post_tokenizer_mutation_runner.ProbeFixtures.case_expected_failure"
ERROR_TARGET = "tests.test_m4_post_tokenizer_mutation_runner.ProbeFixtures.case_error"


class ProbeFixtures(unittest.TestCase):
    def case_pass(self):
        self.assertTrue(True)

    def case_expected_failure(self):
        self.fail("mutation-sensitive-sentinel")

    def case_error(self):
        raise RuntimeError("unrelated-environment-sentinel")


class FakeTarget:
    def __init__(self, baseline: bytes, corrupt_restoration: bool = False,
                 raise_on_restoration: bool = False):
        self.raw = baseline
        self.writes = 0
        self.corrupt_restoration = corrupt_restoration
        self.raise_on_restoration = raise_on_restoration

    def write_bytes(self, raw: bytes) -> None:
        self.writes += 1
        if self.raise_on_restoration and self.writes >= 3:
            raise OSError("restoration-write-sentinel")
        self.raw = b"corrupt" if self.corrupt_restoration and self.writes >= 3 else raw

    def read_bytes(self) -> bytes:
        return self.raw


class MutationRunnerApparatusTests(unittest.TestCase):
    def test_probe_reports_exact_discovery_and_execution(self):
        probe = apparatus.probe_target(PASS_TARGET)
        apparatus.validate_baseline_probe(probe, PASS_TARGET)
        self.assertEqual(probe["discovered_test_ids"], [PASS_TARGET])
        self.assertEqual(probe["tests_run"], 1)

    def test_missing_target_is_instrument_failure(self):
        target = "tests.test_m4_post_tokenizer_mutation_runner.ProbeFixtures.case_missing"
        with self.assertRaisesRegex(apparatus.InstrumentFailure, "target discovery/execution"):
            apparatus.validate_baseline_probe(apparatus.probe_target(target), target)

    def test_unchanged_baseline_must_pass(self):
        with self.assertRaisesRegex(apparatus.InstrumentFailure, "unchanged baseline failure"):
            apparatus.validate_baseline_probe(apparatus.probe_target(FAIL_TARGET), FAIL_TARGET)

    def test_expected_assertion_is_killed(self):
        probe = apparatus.probe_target(FAIL_TARGET)
        self.assertEqual(apparatus.classify_mutant_probe(
            probe, FAIL_TARGET, r"AssertionError: mutation-sensitive-sentinel"), "KILLED")

    def test_passing_mutant_is_survived_not_killed(self):
        probe = apparatus.probe_target(PASS_TARGET)
        self.assertEqual(apparatus.classify_mutant_probe(
            probe, PASS_TARGET, r"mutation-sensitive-sentinel"), "SURVIVED")

    def test_unrelated_assertion_is_instrument_failure(self):
        probe = apparatus.probe_target(FAIL_TARGET)
        with self.assertRaisesRegex(apparatus.InstrumentFailure, "unrelated assertion failure"):
            apparatus.classify_mutant_probe(probe, FAIL_TARGET, r"different-assertion")

    def test_error_is_never_a_kill(self):
        probe = apparatus.probe_target(ERROR_TARGET)
        with self.assertRaisesRegex(apparatus.InstrumentFailure, "target error/skip/output"):
            apparatus.classify_mutant_probe(probe, ERROR_TARGET, r"anything")

    def test_import_syntax_and_environment_errors_are_never_kills(self):
        base = apparatus.probe_target(PASS_TARGET)
        for label in ("ImportError", "SyntaxError", "EnvironmentError"):
            probe = dict(base)
            probe["successful"] = False
            probe["errors"] = [{"test_id": PASS_TARGET, "traceback": label + ": sentinel"}]
            with self.subTest(label=label),self.assertRaisesRegex(
                    apparatus.InstrumentFailure, "target error/skip/output"):
                apparatus.classify_mutant_probe(probe, PASS_TARGET, r"sentinel")

    def test_harness_process_stderr_and_malformed_json_are_instrument_failures(self):
        completed = subprocess.CompletedProcess(["python"], 3, stdout=b"", stderr=b"harness")
        with patch.object(apparatus.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(apparatus.InstrumentFailure, "probe process"):
                apparatus.run_probe(Path("unused"), PASS_TARGET, 1)
        completed = subprocess.CompletedProcess(["python"], 0, stdout=b"not-json", stderr=b"")
        with patch.object(apparatus.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(apparatus.InstrumentFailure, "probe JSON"):
                apparatus.run_probe(Path("unused"), PASS_TARGET, 1)

    def test_timeout_is_instrument_failure(self):
        with patch.object(apparatus.subprocess, "run", side_effect=subprocess.TimeoutExpired(["python"], 1)):
            with self.assertRaisesRegex(apparatus.InstrumentFailure, "target timeout"):
                apparatus.run_probe(Path("unused"), PASS_TARGET, 1)

    def test_normalization_removes_only_runtime_path_and_caret_rendering(self):
        root = Path("C:/temporary/mutants")
        rendered = (
            '  File "C:\\temporary\\mutants\\src\\case.py", line 7\n'
            '    with self.assertRaises(AssertionError):\n'
            '         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
            'AssertionError: sentinel\n'
        )
        self.assertEqual(
            apparatus._normalize_text(rendered, root),
            '  File "<normalized-runtime>/src/case.py", line 7\n'
            '    with self.assertRaises(AssertionError):\n'
            'AssertionError: sentinel\n',
        )

    def test_contract_binds_exact_probe_command(self):
        contract = json.loads(apparatus.CONTRACT.read_bytes())
        invalid = copy.deepcopy(contract)
        invalid["mutants"][0]["probe_command"] = ["python", "-m", "unittest"]
        with self.assertRaisesRegex(apparatus.InstrumentFailure, "mutant identity/command"):
            apparatus.validate_contract(invalid)

    def test_restoration_occurs_after_body_failure(self):
        baseline = b"baseline"
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target.py"
            with self.assertRaisesRegex(RuntimeError, "body failure"):
                with apparatus.restoration_guard(target, baseline, apparatus.digest(baseline)):
                    target.write_bytes(b"mutated")
                    raise RuntimeError("body failure")
            self.assertEqual(target.read_bytes(), baseline)

    def test_restoration_identity_failure_stops_fail_closed(self):
        baseline = b"baseline"
        target = FakeTarget(baseline, corrupt_restoration=True)
        with self.assertRaisesRegex(apparatus.InstrumentFailure, "restoration identity"):
            with apparatus.restoration_guard(target, baseline, apparatus.digest(baseline)):
                target.write_bytes(b"mutated")

    def test_restoration_write_failure_stops_fail_closed(self):
        baseline = b"baseline"
        target = FakeTarget(baseline, raise_on_restoration=True)
        with self.assertRaisesRegex(apparatus.InstrumentFailure, "restoration identity"):
            with apparatus.restoration_guard(target, baseline, apparatus.digest(baseline)):
                target.write_bytes(b"mutated")


if __name__ == "__main__":
    unittest.main()
