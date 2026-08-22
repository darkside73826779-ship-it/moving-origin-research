#!/usr/bin/env python3
"""Identity-first custody-free validation for the public observation backend."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IDENTITY_PATHS = (
    "specs/data/m4_public_model_observation_backend_contract_v1.json",
    "specs/data/m4_public_model_observation_backend_test_contract_v1.json",
    "specs/data/m4_public_model_observation_launch_contract_v1.json",
    "specs/data/m4_public_model_observation_prompt_contract_v1.json",
    "specs/data/m4_public_model_local_observation_schema_v1.json",
    "specs/data/m4_public_model_observation_backend_implementation_v1.json",
    "src/m4_public_model_observation_backend.py",
    "tests/test_m4_public_model_observation_backend.py",
    "tests/run_m4_public_model_observation_backend_tests.py",
    "tests/run_m4_public_model_observation_backend_mutations.py",
)


def _verify_sidecar(relative: str) -> None:
    path = ROOT / relative
    sidecar = path.with_name(path.name + ".sha256")
    if not path.is_file() or path.is_symlink() or not sidecar.is_file() or sidecar.is_symlink():
        raise RuntimeError("IDENTITY_FILE_MISSING_OR_NONCANONICAL")
    raw = path.read_bytes()
    expected = f"{hashlib.sha256(raw).hexdigest()}  {path.name}\n".encode("ascii")
    if sidecar.read_bytes() != expected or b"\r" in raw:
        raise RuntimeError("IDENTITY_DIGEST_OR_LF_MISMATCH")


def _load_json(relative: str) -> dict:
    raw = (ROOT / relative).read_bytes()
    value = json.loads(raw)
    if (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
            != raw):
        raise RuntimeError("NONCANONICAL_JSON")
    return value


def validate_identities() -> tuple[dict, dict]:
    for relative in IDENTITY_PATHS:
        _verify_sidecar(relative)
    test_contract = _load_json(IDENTITY_PATHS[1])
    launch_contract = _load_json(IDENTITY_PATHS[2])
    expected_command = ["python3", "-I", "tests/run_m4_public_model_observation_backend_tests.py"]
    if test_contract.get("implementation_command") != expected_command:
        raise RuntimeError("TEST_TARGET_BINDING_MISMATCH")
    if launch_contract.get("run_authorized") is not False:
        raise RuntimeError("UNEXPECTED_RUN_AUTHORITY")
    return test_contract, launch_contract


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--contract")
    parser.add_argument("--prompt-contract")
    parser.add_argument("--local-stage-env")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validate_identities()
    except Exception as exc:
        print(f"INSTRUMENT_FAILURE: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if any((args.contract, args.prompt_contract, args.local_stage_env)):
        # The committed launch contract is deliberately not executable.  This stop
        # precedes environment lookup, model/tokenizer import, or process start.
        print("RUN_AUTHORITY_ABSENT", file=sys.stderr)
        return 2
    sys.path.insert(0, str(ROOT))
    suite = unittest.defaultTestLoader.loadTestsFromName(
        "tests.test_m4_public_model_observation_backend"
    )
    if suite.countTestCases() != 17:
        print("INSTRUMENT_FAILURE: TEST_DISCOVERY_COUNT_MISMATCH", file=sys.stderr)
        return 2
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
