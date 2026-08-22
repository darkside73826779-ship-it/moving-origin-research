#!/usr/bin/env python3
"""Deterministically validate and replay the governed post-tokenizer mutants."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Iterator


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER_PATH = "tests/run_m4_post_tokenizer_mutation_tests.py"
CONTRACT = ROOT / "specs/data/m4_post_tokenizer_mutation_contract_v1.json"
TRANSCRIPT = ROOT / "artifacts/m4_post_tokenizer_mutation_transcript_v1.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PROBE_KEYS = {
    "captured_stderr", "captured_stdout", "discovered_test_ids", "errors", "failures",
    "loader_errors", "skipped", "successful", "target_test", "tests_run", "unexpected_successes",
}


class InstrumentFailure(RuntimeError):
    """The mutation apparatus could not establish valid mutation evidence."""


class MutantSurvived(RuntimeError):
    """The apparatus ran correctly but the intended test did not reject a mutant."""


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def indexed_blob(relative: str, root: pathlib.Path = ROOT) -> bytes:
    run = subprocess.run(["git", "show", ":" + relative], cwd=root, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, check=False)
    if run.returncode != 0:
        raise InstrumentFailure("indexed Git blob " + relative)
    return run.stdout


def _suite_ids(suite: unittest.TestSuite) -> list[str]:
    found: list[str] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            found.extend(_suite_ids(item))
        else:
            found.append(item.id())
    return found


def _result_rows(rows: list[tuple[unittest.case.TestCase, str]]) -> list[dict[str, str]]:
    return [{"test_id": test.id(), "traceback": traceback_text} for test, traceback_text in rows]


def probe_target(target_test: str) -> dict[str, object]:
    """Discover and execute one exact target, returning machine-classifiable evidence."""
    loader = unittest.TestLoader()
    captured_stdout, captured_stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
        suite = loader.loadTestsFromName(target_test)
        discovered = _suite_ids(suite)
        result = unittest.TestResult()
        suite.run(result)
    return {
        "captured_stderr": captured_stderr.getvalue(),
        "captured_stdout": captured_stdout.getvalue(),
        "discovered_test_ids": discovered,
        "errors": _result_rows(result.errors),
        "failures": _result_rows(result.failures),
        "loader_errors": list(loader.errors),
        "skipped": [{"reason": reason, "test_id": test.id()} for test, reason in result.skipped],
        "successful": result.wasSuccessful(),
        "target_test": target_test,
        "tests_run": result.testsRun,
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
    }


def _normalize_text(value: str, mutation_root: pathlib.Path) -> str:
    text = value.replace("\r\n", "\n").replace("\r", "\n").replace("\\", "/")
    for spelling in (str(mutation_root).replace("\\", "/"), sys.executable.replace("\\", "/")):
        text = text.replace(spelling, "<normalized-runtime>")
    text = re.sub(r"(?m)^[ \t]*[\^~]+[ \t]*\n", "", text)
    return re.sub(r"Ran (\d+) test(s?) in [0-9.]+s", r"Ran \1 test\2", text)


def normalize(value: object, mutation_root: pathlib.Path) -> object:
    if isinstance(value, str):
        return _normalize_text(value, mutation_root)
    if isinstance(value, list):
        return [normalize(item, mutation_root) for item in value]
    if isinstance(value, dict):
        return {key: normalize(item, mutation_root) for key, item in value.items()}
    return value


def run_probe(mutation_root: pathlib.Path, target_test: str, timeout_seconds: int) -> tuple[dict[str, object], list[str]]:
    command = [sys.executable, str(mutation_root / RUNNER_PATH), "--probe-target", target_test]
    try:
        run = subprocess.run(command, cwd=mutation_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=timeout_seconds, check=False)
    except subprocess.TimeoutExpired as exc:
        raise InstrumentFailure("target timeout " + target_test) from exc
    if run.returncode != 0:
        raise InstrumentFailure("probe process " + target_test)
    if run.stderr:
        raise InstrumentFailure("probe stderr " + target_test)
    try:
        probe = json.loads(run.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InstrumentFailure("probe JSON " + target_test) from exc
    if canonical(probe) != run.stdout:
        raise InstrumentFailure("probe canonical output " + target_test)
    return probe, ["python", RUNNER_PATH, "--probe-target", target_test]


def _validate_common_probe(probe: dict[str, object], target_test: str) -> None:
    if not isinstance(probe, dict) or set(probe) != PROBE_KEYS:
        raise InstrumentFailure("probe key set " + target_test)
    if (probe["target_test"] != target_test or probe["discovered_test_ids"] != [target_test] or
            probe["tests_run"] != 1 or probe["loader_errors"] != []):
        raise InstrumentFailure("target discovery/execution " + target_test)
    if (probe["errors"] != [] or probe["skipped"] != [] or probe["unexpected_successes"] != [] or
            probe["captured_stdout"] != "" or probe["captured_stderr"] != ""):
        raise InstrumentFailure("target error/skip/output " + target_test)


def validate_baseline_probe(probe: dict[str, object], target_test: str) -> None:
    _validate_common_probe(probe, target_test)
    if probe["successful"] is not True or probe["failures"] != []:
        raise InstrumentFailure("unchanged baseline failure " + target_test)


def classify_mutant_probe(probe: dict[str, object], target_test: str, expected_failure_regex: str) -> str:
    _validate_common_probe(probe, target_test)
    failures = probe["failures"]
    if probe["successful"] is True and failures == []:
        return "SURVIVED"
    if probe["successful"] is not False or not isinstance(failures, list) or not failures:
        raise InstrumentFailure("mutant result shape " + target_test)
    for failure in failures:
        if (not isinstance(failure, dict) or set(failure) != {"test_id", "traceback"} or
                not str(failure["test_id"]).startswith(target_test) or "AssertionError" not in failure["traceback"]):
            raise InstrumentFailure("non-assertion mutant failure " + target_test)
    combined = "\n".join(failure["traceback"] for failure in failures)
    try:
        matched = re.search(expected_failure_regex, combined, flags=re.DOTALL)
    except re.error as exc:
        raise InstrumentFailure("expected failure regex " + target_test) from exc
    if matched is None:
        raise InstrumentFailure("unrelated assertion failure " + target_test)
    return "KILLED"


@contextlib.contextmanager
def restoration_guard(target: object, baseline: bytes, baseline_sha256: str) -> Iterator[None]:
    try:
        target.write_bytes(baseline)
        staged = target.read_bytes()
    except Exception as exc:
        raise InstrumentFailure("baseline staging identity") from exc
    if staged != baseline or digest(staged) != baseline_sha256:
        raise InstrumentFailure("baseline staging identity")
    try:
        yield
    finally:
        try:
            target.write_bytes(baseline)
            restored = target.read_bytes()
        except Exception as exc:
            raise InstrumentFailure("restoration identity") from exc
        if restored != baseline or digest(restored) != baseline_sha256:
            raise InstrumentFailure("restoration identity")


def validate_contract(contract: dict[str, object]) -> None:
    required = {"baseline_sha256", "date", "mutants", "regime", "runner_sha256", "schema_version",
                "target_path", "timeout_seconds"}
    if not isinstance(contract, dict) or set(contract) != required:
        raise InstrumentFailure("mutation contract key set")
    if contract["schema_version"] != "m4-post-tokenizer-mutation-contract-v2" or contract["regime"] != "B":
        raise InstrumentFailure("mutation contract identity")
    if type(contract["timeout_seconds"]) is not int or not 1 <= contract["timeout_seconds"] <= 300:
        raise InstrumentFailure("mutation timeout")
    mutants = contract["mutants"]
    if not isinstance(mutants, list) or not mutants:
        raise InstrumentFailure("mutation set")
    ids: set[str] = set()
    required_mutant = {"expected_failure_regex", "expected_occurrences", "mutant_sha256", "mutation_id",
                       "new_utf8", "old_utf8", "probe_command", "target_test"}
    for mutant in mutants:
        if not isinstance(mutant, dict) or set(mutant) != required_mutant:
            raise InstrumentFailure("mutant key set")
        mutation_id, target_test = mutant["mutation_id"], mutant["target_test"]
        expected_command = ["python", RUNNER_PATH, "--probe-target", target_test]
        if (not isinstance(mutation_id, str) or not mutation_id or mutation_id in ids or
                not isinstance(target_test, str) or not target_test or mutant["probe_command"] != expected_command):
            raise InstrumentFailure("mutant identity/command")
        if (type(mutant["expected_occurrences"]) is not int or mutant["expected_occurrences"] < 1 or
                not isinstance(mutant["expected_failure_regex"], str) or not mutant["expected_failure_regex"]):
            raise InstrumentFailure("mutant occurrence/failure binding")
        ids.add(mutation_id)


def load_contract() -> tuple[dict[str, object], bytes]:
    raw = indexed_blob(CONTRACT.relative_to(ROOT).as_posix())
    try:
        contract = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InstrumentFailure("mutation contract JSON") from exc
    if b"\r" in raw or not raw.endswith(b"\n") or canonical(contract) != raw:
        raise InstrumentFailure("mutation contract canonical identity")
    validate_contract(contract)
    if digest(indexed_blob(RUNNER_PATH)) != contract["runner_sha256"]:
        raise InstrumentFailure("mutation runner identity")
    return contract, raw


def execute(contract: dict[str, object], contract_raw: bytes) -> dict[str, object]:
    baseline = indexed_blob(str(contract["target_path"]))
    baseline_sha256 = str(contract["baseline_sha256"])
    if digest(baseline) != baseline_sha256:
        raise InstrumentFailure("mutation baseline identity")
    records: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="m4-post-tokenizer-mutants-") as temporary:
        mutation_root = pathlib.Path(temporary) / "checkout"
        mutation_root.mkdir()
        for name in ("src", "tests", "specs", "artifacts"):
            shutil.copytree(ROOT / name, mutation_root / name)
        mutation_target = mutation_root / str(contract["target_path"])
        for mutant in contract["mutants"]:
            target_test = mutant["target_test"]
            with restoration_guard(mutation_target, baseline, baseline_sha256):
                baseline_probe, observed_command = run_probe(
                    mutation_root, target_test, int(contract["timeout_seconds"]))
                if observed_command != mutant["probe_command"]:
                    raise InstrumentFailure("observed probe command " + mutant["mutation_id"])
                validate_baseline_probe(baseline_probe, target_test)
                old = mutant["old_utf8"].encode("utf-8")
                new = mutant["new_utf8"].encode("utf-8")
                if baseline.count(old) != mutant["expected_occurrences"]:
                    raise InstrumentFailure("mutation occurrence " + mutant["mutation_id"])
                mutated = baseline.replace(old, new)
                if digest(mutated) != mutant["mutant_sha256"]:
                    raise InstrumentFailure("mutant identity " + mutant["mutation_id"])
                mutation_target.write_bytes(mutated)
                if digest(mutation_target.read_bytes()) != mutant["mutant_sha256"]:
                    raise InstrumentFailure("temporary mutant write " + mutant["mutation_id"])
                mutant_probe, repeated_command = run_probe(
                    mutation_root, target_test, int(contract["timeout_seconds"]))
                if repeated_command != observed_command:
                    raise InstrumentFailure("mutant probe command " + mutant["mutation_id"])
                classification = classify_mutant_probe(
                    mutant_probe, target_test, mutant["expected_failure_regex"])
                if classification != "KILLED":
                    raise MutantSurvived(mutant["mutation_id"])
            records.append({
                "baseline_probe": normalize(baseline_probe, mutation_root),
                "baseline_sha256": baseline_sha256,
                "classification": classification,
                "expected_failure_regex": mutant["expected_failure_regex"],
                "mutant_probe": normalize(mutant_probe, mutation_root),
                "mutant_sha256": mutant["mutant_sha256"],
                "mutation_id": mutant["mutation_id"],
                "probe_command": mutant["probe_command"],
                "restored_sha256": baseline_sha256,
                "target_test": target_test,
            })
    return {
        "baseline_sha256": baseline_sha256,
        "clean_baseline_passed_for_every_mutant": True,
        "clean_restoration_after_each_mutant": True,
        "contract_sha256": digest(contract_raw),
        "date": contract["date"],
        "mutant_count": len(records),
        "records": records,
        "regime": "B",
        "runner_command": ["python", RUNNER_PATH, "--verify"],
        "runner_sha256": contract["runner_sha256"],
        "schema_version": "m4-post-tokenizer-mutation-transcript-v2",
        "status": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", type=pathlib.Path)
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--probe-target")
    args = parser.parse_args()
    if args.probe_target is not None:
        sys.stdout.buffer.write(canonical(probe_target(args.probe_target)))
        return 0
    try:
        contract, raw = load_contract()
        observed = canonical(execute(contract, raw))
        if args.record is not None:
            args.record.write_bytes(observed)
        else:
            expected = indexed_blob(TRANSCRIPT.relative_to(ROOT).as_posix())
            if observed != expected:
                raise InstrumentFailure("mutation transcript mismatch")
    except MutantSurvived as exc:
        print("FAIL: MUTANT_SURVIVED: " + str(exc), file=sys.stderr)
        return 1
    except InstrumentFailure as exc:
        print("INSTRUMENT_FAILURE: " + str(exc), file=sys.stderr)
        return 2
    except OSError as exc:
        print("INSTRUMENT_FAILURE: apparatus I/O: " + str(exc), file=sys.stderr)
        return 2
    print(f"PASS: {len(contract['mutants'])}/{len(contract['mutants'])} mutants killed; transcript_sha256={digest(observed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
