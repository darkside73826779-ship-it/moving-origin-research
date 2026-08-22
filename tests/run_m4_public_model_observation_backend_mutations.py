#!/usr/bin/env python3
"""Deterministic custody-free adversarial mutations for observation boundaries."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("src/m4_public_model_observation_backend.py")
MUTANTS = (
    ("ROLE_GUARD_WEAKENED",
     'if role != "control" or scientific_arm != "naive":\n            raise IntegrationError("ROLE_ARM_MISMATCH")\n        return self._factory.create(role, scientific_arm,',
     'if False:\n            raise IntegrationError("ROLE_ARM_MISMATCH")\n        return self._factory.create("control", "naive",',
     "test_registration_rejects_every_non_control_naive_before_construction"),
    ("STAGE_MODE_INVERTED", 'self._deps.stage_mode_probe(stage) != 0o700',
     'self._deps.stage_mode_probe(stage) == 0o700',
     "test_stage_absent_linked_and_wrong_mode_are_separate_fail_closed_cases"),
    ("NAMESPACE_TRUTHINESS", 'self._deps.namespace_probe() is not True',
     'self._deps.namespace_probe() is False',
     "test_initialize_authenticates_identity_before_one_stub_load"),
    ("LAW_STATUS_UNCHECKED", 'laws = held_law_rows()\n        if (',
     'laws = held_law_rows()\n        if False and (',
     "test_law_projection_cannot_be_promoted"),
    ("FAILURE_CODE_UNREGISTERED", 'REGISTERED_FAILURE_CODE = "SYNTHETIC_REJECTED"',
     'REGISTERED_FAILURE_CODE = "OBSERVATION_GENERATION_FAILED"',
     "test_engine_load_failure_has_no_retry_or_residue"),
    ("OUTPUT_ZEROIZATION_REMOVED", 'for index in range(len(output_ids)):\n                    output_ids[index] = 0',
     'for index in range(0):\n                    output_ids[index] = 0',
     "test_three_stub_only_episodes_publish_sanitized_pairs_and_zeroize_arrays"),
    ("ZERO_COUNT_LOWER_BOUND_REMOVED", 'min(count, tokens.context_length) < 1',
     'min(count, tokens.context_length) < 0',
     "test_zero_count_private_view_is_rejected_before_engine_and_restored_exactly"),
)


def validate_contract(original_sha256: str) -> bool:
    path = ROOT / "specs/data/m4_public_model_observation_backend_mutation_contract_v1.json"
    raw = path.read_bytes()
    contract = json.loads(raw)
    expected_rows = [
        {"expected_exit": 1, "id": mutant_id,
         "new_text_sha256": hashlib.sha256(new.encode()).hexdigest(),
         "old_text_sha256": hashlib.sha256(old.encode()).hexdigest(), "target": target}
        for mutant_id, old, new, target in MUTANTS
    ]
    expected_closure = [str(path).replace("\\", "/") for path in (
        SOURCE, Path("src/m4_post_tokenizer_integration.py"), Path("tests/__init__.py"),
        Path("tests/test_m4_public_model_observation_backend.py"),
    )]
    return (json.dumps(contract, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n" == raw and
            contract.get("mutants") == expected_rows and
            contract.get("copy_dependency_closure") == expected_closure and
            contract.get("restoration", {}).get("original_source_sha256") == original_sha256 and
            contract.get("baseline", {}).get("expected_tests") == 19)


def main() -> int:
    original = (ROOT / SOURCE).read_bytes()
    original_sha256 = hashlib.sha256(original).hexdigest()
    if not validate_contract(original_sha256):
        print("INSTRUMENT_FAILURE MUTATION_CONTRACT", file=sys.stderr)
        return 2
    baseline = subprocess.run(
        [sys.executable, "-I", "tests/run_m4_public_model_observation_backend_tests.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    if baseline.returncode != 0:
        print("INSTRUMENT_FAILURE BASELINE", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="m4-observation-mutants-") as temporary:
        disposable = Path(temporary) / "repo"
        (disposable / "src").mkdir(parents=True)
        (disposable / "tests").mkdir()
        for relative in (
            SOURCE,
            Path("src/m4_post_tokenizer_integration.py"),
            Path("tests/__init__.py"),
            Path("tests/test_m4_public_model_observation_backend.py"),
        ):
            shutil.copy2(ROOT / relative, disposable / relative)
        for mutant_id, old, new, target in MUTANTS:
            path = disposable / SOURCE
            text = original.decode("utf-8")
            if text.count(old) != 1:
                print(f"INSTRUMENT_FAILURE {mutant_id} PATCH_CARDINALITY", file=sys.stderr)
                return 2
            path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
            command = [sys.executable, "-m", "unittest", "-v",
                       f"tests.test_m4_public_model_observation_backend.PublicObservationBackendTests.{target}"]
            result = subprocess.run(command, cwd=disposable, capture_output=True, text=True, timeout=60)
            output = result.stdout + result.stderr
            if result.returncode != 1 or target not in output or "FAILED" not in output:
                print(f"INSTRUMENT_FAILURE {mutant_id} UNEXPECTED_EXIT_OR_OUTPUT", file=sys.stderr)
                return 2
            print(f"KILLED {mutant_id} target={target} exit=1")
            path.write_bytes(original)
            if hashlib.sha256(path.read_bytes()).hexdigest() != original_sha256:
                print(f"INSTRUMENT_FAILURE {mutant_id} RESTORE_IDENTITY", file=sys.stderr)
                return 2
    if hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest() != original_sha256:
        print("INSTRUMENT_FAILURE ORIGINAL_IDENTITY", file=sys.stderr)
        return 2
    print(f"PASS baseline=19/19 mutants={len(MUTANTS)}/{len(MUTANTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
