#!/usr/bin/env python3
"""Deterministically reapply and verify the governed post-tokenizer mutants."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "specs/data/m4_post_tokenizer_mutation_contract_v1.json"
TRANSCRIPT = ROOT / "artifacts/m4_post_tokenizer_mutation_transcript_v1.json"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalize(output: str, mutation_root: pathlib.Path) -> str:
    text = output.replace("\r\n", "\n").replace("\r", "\n")
    for spelling in (str(mutation_root), str(mutation_root).replace("\\", "/"), sys.executable):
        text = text.replace(spelling, "<normalized-runtime>")
    text = re.sub(r"Ran (\d+) test(s?) in [0-9.]+s", r"Ran \1 test\2", text)
    return text


def indexed_blob(relative: str) -> bytes:
    run = subprocess.run(["git", "show", ":" + relative], cwd=ROOT, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, check=False)
    if run.returncode != 0:
        raise SystemExit("INSTRUMENT_FAILURE: indexed Git blob " + relative)
    return run.stdout


def load_contract() -> tuple[dict, bytes]:
    raw = indexed_blob(CONTRACT.relative_to(ROOT).as_posix())
    if b"\r" in raw or not raw.endswith(b"\n") or canonical(json.loads(raw)) != raw:
        raise SystemExit("INSTRUMENT_FAILURE: mutation contract canonical identity")
    contract = json.loads(raw)
    if contract.get("schema_version") != "m4-post-tokenizer-mutation-contract-v1":
        raise SystemExit("INSTRUMENT_FAILURE: mutation contract schema")
    if digest(indexed_blob(pathlib.Path(__file__).resolve().relative_to(ROOT).as_posix())) != contract.get("runner_sha256"):
        raise SystemExit("INSTRUMENT_FAILURE: mutation runner identity")
    return contract, raw


def execute(contract: dict, contract_raw: bytes) -> dict:
    baseline = indexed_blob(contract["target_path"])
    if digest(baseline) != contract["baseline_sha256"]:
        raise SystemExit("INSTRUMENT_FAILURE: mutation baseline identity")
    records = []
    with tempfile.TemporaryDirectory(prefix="m4-post-tokenizer-mutants-") as temporary:
        mutation_root = pathlib.Path(temporary) / "checkout"
        mutation_root.mkdir()
        for name in ("src", "tests", "specs", "artifacts"):
            shutil.copytree(ROOT / name, mutation_root / name)
        mutation_target = mutation_root / contract["target_path"]
        for mutant in contract["mutants"]:
            mutation_target.write_bytes(baseline)
            old = mutant["old_utf8"].encode("utf-8")
            new = mutant["new_utf8"].encode("utf-8")
            occurrences = baseline.count(old)
            if occurrences != mutant["expected_occurrences"]:
                raise SystemExit("INSTRUMENT_FAILURE: mutation occurrence " + mutant["mutation_id"])
            mutated = baseline.replace(old, new)
            if digest(mutated) != mutant["mutant_sha256"]:
                raise SystemExit("INSTRUMENT_FAILURE: mutant identity " + mutant["mutation_id"])
            mutation_target.write_bytes(mutated)
            command = mutant["command"]
            if command[:3] != ["python", "-m", "unittest"] or len(command) != 4:
                raise SystemExit("INSTRUMENT_FAILURE: mutation command " + mutant["mutation_id"])
            run = subprocess.run([sys.executable, *command[1:]], cwd=mutation_root, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            record = {
                "command": command,
                "exit_code": run.returncode,
                "mutation_id": mutant["mutation_id"],
                "mutant_sha256": digest(mutated),
                "normalized_stderr": normalize(run.stderr, mutation_root),
                "normalized_stdout": normalize(run.stdout, mutation_root),
                "result": "KILLED" if run.returncode == mutant["expected_exit_code"] else "UNEXPECTED",
            }
            if record["result"] != "KILLED":
                raise SystemExit("INSTRUMENT_FAILURE: surviving mutant " + mutant["mutation_id"])
            records.append(record)
            mutation_target.write_bytes(baseline)
            if digest(mutation_target.read_bytes()) != contract["baseline_sha256"]:
                raise SystemExit("INSTRUMENT_FAILURE: restoration " + mutant["mutation_id"])
    return {
        "baseline_sha256": contract["baseline_sha256"],
        "clean_restoration_after_each_mutant": True,
        "contract_sha256": digest(contract_raw),
        "date": contract["date"],
        "mutant_count": len(records),
        "records": records,
        "regime": "B",
        "runner_command": ["python", "tests/run_m4_post_tokenizer_mutation_tests.py", "--verify"],
        "runner_sha256": contract["runner_sha256"],
        "schema_version": "m4-post-tokenizer-mutation-transcript-v1",
        "status": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", type=pathlib.Path)
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    contract, raw = load_contract()
    observed = canonical(execute(contract, raw))
    if args.record is not None:
        args.record.write_bytes(observed)
    else:
        expected = indexed_blob(TRANSCRIPT.relative_to(ROOT).as_posix())
        if observed != expected:
            raise SystemExit("INSTRUMENT_FAILURE: mutation transcript mismatch")
    print(f"PASS: {len(contract['mutants'])}/{len(contract['mutants'])} mutants killed; transcript_sha256={digest(observed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
