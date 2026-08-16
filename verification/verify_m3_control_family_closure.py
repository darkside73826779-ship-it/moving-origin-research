"""Specification-only verifier for the M3 V4.4 systemic closure gate.

This verifier reads specifications and the 26-family inventory only. It does
not import or execute the M3 harness and it consumes no scoring seed or output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED_IDS = {
    "L1.frozen", "L1.fair_naive", "L1.recency_only",
    "L1.rehearsal_only", "L1.permuted", "L1.shuffled", "L1.oracle",
    "L1.empty", "L3.frozen", "L3.oracle", "L3.permuted",
    "L3.shuffled", "L3.empty", "L5.single_axis", "L5.full_scan",
    "L5.oracle", "L5.frozen", "L5.permuted", "L5.shuffled", "L5.empty",
    "L6.empty", "L6.permuted", "L6.shuffled", "L6.oracle", "L6.frozen",
    "L6.fair_naive",
}
EXPECTED_COUNTS = {"L1": 8, "L3": 5, "L5": 7, "L6": 6}
REQUIRED_FAMILY_KEYS = {
    "family_id", "law", "arm", "checks", "seeds", "comparisons_per_seed",
    "simultaneous_comparisons", "meaningful_failure_direction",
    "direction_justification", "reference_type", "reference",
    "current_per_check_error_rate", "pre_correction_fwfp",
    "corrective_method", "corrected_fwfp", "artifact_fields",
}
REQUIRED_RNG_KEYS = {
    "id", "hash", "root_domain_ascii", "root_domain_hex",
    "integer_encoding", "component_encoding", "key_formula",
    "observed_role", "null_role", "stream_formula", "uniform_integer",
    "permutation", "derangement", "rng_reuse_prohibited",
    "cross_platform_rule", "exchangeability", "required_artifact_fields",
}
STOCHASTIC_IDS = {
    "L1.frozen", "L1.fair_naive", "L1.permuted", "L1.shuffled",
    "L3.permuted", "L5.permuted",
}
SPEC_MARKERS = [
    "### 2.9 Exact expected statistic, multiplicity control, and artifacts",
    "### 2.10 Full L18 battery checklist for L1 — harmonized",
    "### 2.11 Verdict branches — consolidated",
    "V4.3 one-sided upper null-of-the-max plus-one p-value",
    "p_s = (1 + sum_r I[S_null(s,r) >= S_obs(s)]) / 1001",
    "48/1001 = 0.047952047952",
    "Phase A — pre-scoring specification closure",
    "Phase B — post-scoring JUDGE verification",
    "Phase A **must not** compute observed maxima",
    "M3-V4.4-SHA256-CTR-FY-v1",
    "MOVING-ORIGIN/M3/V4.4/CONTROL-RNG/v1",
    "Fisher–Yates",
    "reuse is an instrument failure",
    "Seeds 201–203 and their first-run `INSTRUMENT FAILURE` verdict remain retained",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(inventory: dict[str, Any], spec_text: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    families = inventory.get("families", [])
    ids = [row.get("family_id") for row in families]

    if len(families) != 26:
        fail(errors, f"expected 26 families, found {len(families)}")
    if set(ids) != EXPECTED_IDS:
        fail(errors, f"family ID mismatch: missing={sorted(EXPECTED_IDS-set(ids))}, extra={sorted(set(ids)-EXPECTED_IDS)}")
    duplicates = sorted(k for k, v in Counter(ids).items() if v != 1)
    if duplicates:
        fail(errors, f"families not present exactly once: {duplicates}")
    law_counts = Counter(row.get("law") for row in families)
    if dict(law_counts) != EXPECTED_COUNTS:
        fail(errors, f"law counts mismatch: {dict(law_counts)}")

    stochastic_count = 0
    deterministic_count = 0
    corrections: list[dict[str, Any]] = []
    for row in families:
        family_id = row.get("family_id", "<missing>")
        missing = REQUIRED_FAMILY_KEYS - set(row)
        if missing:
            fail(errors, f"{family_id}: missing keys {sorted(missing)}")
            continue
        if not row["checks"] or not all(isinstance(x, str) and x.strip() for x in row["checks"]):
            fail(errors, f"{family_id}: checks must be a nonempty string list")
        if row["seeds"] != 3:
            fail(errors, f"{family_id}: seeds must equal 3")
        if row["simultaneous_comparisons"] != row["seeds"] * row["comparisons_per_seed"]:
            fail(errors, f"{family_id}: simultaneous comparison arithmetic mismatch")
        if not str(row["meaningful_failure_direction"]).strip() or len(row["direction_justification"].strip()) < 20:
            fail(errors, f"{family_id}: missing/weak direction justification")
        if not row["artifact_fields"] or not all(isinstance(x, str) and x.strip() for x in row["artifact_fields"]):
            fail(errors, f"{family_id}: required artifact fields undefined")
        if not row["corrective_method"].strip():
            fail(errors, f"{family_id}: corrective method undefined")

        reference_type = row["reference_type"]
        pre = row["pre_correction_fwfp"]
        corrected = row["corrected_fwfp"]
        if reference_type == "stochastic_empirical":
            stochastic_count += 1
            if family_id not in STOCHASTIC_IDS:
                fail(errors, f"{family_id}: unexpected stochastic classification")
            if row["current_per_check_error_rate"] is None:
                fail(errors, f"{family_id}: stochastic per-check error rate missing")
            if not pre.get("applicable") or not corrected.get("applicable"):
                fail(errors, f"{family_id}: stochastic FWFP must be applicable")
            value = corrected.get("value")
            if not isinstance(value, (int, float)) or value > 0.05 or not corrected.get("le_0_05"):
                fail(errors, f"{family_id}: corrected FWFP is not <= 0.05")
            if abs(value - 48 / 1001) > 1e-15:
                fail(errors, f"{family_id}: corrected finite bound must be 48/1001")
            joined_fields = " ".join(row["artifact_fields"])
            for token in ("plus_one_p_value", "rng_derivation_records"):
                if token not in joined_fields:
                    fail(errors, f"{family_id}: stochastic artifact missing {token}")
            if pre.get("value", 0) > 0.05:
                corrections.append({
                    "family_id": family_id,
                    "pre_correction_fwfp": pre["value"],
                    "corrected_fwfp": value,
                    "method": row["corrective_method"],
                })
        elif reference_type == "deterministic":
            deterministic_count += 1
            if family_id in STOCHASTIC_IDS:
                fail(errors, f"{family_id}: required stochastic family classified deterministic")
            if pre.get("applicable") or corrected.get("applicable"):
                fail(errors, f"{family_id}: deterministic stochastic FWFP must be inapplicable")
            if pre.get("value") != 0.0 or corrected.get("value") != 0.0:
                fail(errors, f"{family_id}: deterministic audit FWFP value must be zero")
            rationale = (row["reference"] + " " + pre.get("derivation", "")).lower()
            if not any(word in rationale for word in ("exact", "fixed", "finite", "paired", "combinatorial", "contract", "oracle")):
                fail(errors, f"{family_id}: deterministic exactness rationale missing")
        else:
            fail(errors, f"{family_id}: invalid reference_type {reference_type!r}")

    if STOCHASTIC_IDS != {row["family_id"] for row in families if row.get("reference_type") == "stochastic_empirical"}:
        fail(errors, "stochastic family set mismatch")

    rng = inventory.get("rng_protocol", {})
    missing_rng = REQUIRED_RNG_KEYS - set(rng)
    if missing_rng:
        fail(errors, f"RNG protocol missing keys {sorted(missing_rng)}")
    else:
        if rng["hash"] != "SHA-256":
            fail(errors, "RNG hash must be SHA-256")
        expected_hex = rng["root_domain_ascii"].encode("ascii").hex()
        if rng["root_domain_hex"] != expected_hex:
            fail(errors, "RNG domain ASCII/hex mismatch")
        if rng["rng_reuse_prohibited"] is not True:
            fail(errors, "RNG reuse prohibition missing")
        rng_blob = json.dumps(rng, sort_keys=True)
        for token in ("OBSERVED", "NULL", "uint64", "uint32", "Fisher-Yates", "no fixed point", "big-endian", "exchangeab"):
            if token.lower() not in rng_blob.lower():
                fail(errors, f"RNG derivation incomplete: missing {token}")

    for marker in SPEC_MARKERS:
        if marker not in spec_text:
            fail(errors, f"spec consistency marker missing: {marker}")
    stale_210 = "All 5 conditional ρ within shuffled-empirical-null band"
    if stale_210 in spec_text:
        fail(errors, "stale §2.10 shuffled wording remains")
    if inventory.get("phase") != "pre_scoring_specification_only" or inventory.get("fresh_scoring_values_used") is not False:
        fail(errors, "inventory phase improperly requires scoring values")

    summary = {
        "family_count": len(families),
        "law_counts": dict(sorted(law_counts.items())),
        "stochastic_family_count": stochastic_count,
        "deterministic_family_count": deterministic_count,
        "correction_count": len(corrections),
        "corrections": corrections,
        "max_corrected_stochastic_fwfp": max(
            (row["corrected_fwfp"]["value"] for row in families
             if row.get("reference_type") == "stochastic_empirical"),
            default=0.0,
        ),
        "all_corrected_stochastic_fwfp_le_0_05": all(
            row["corrected_fwfp"]["value"] <= 0.05
            for row in families
            if row.get("reference_type") == "stochastic_empirical"
        ),
        "fresh_scoring_values_used": False,
        "m3_harness_run": False,
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="verification/m3_control_family_closure_inventory.json")
    parser.add_argument("--spec", default="specs/m3_e2_spec_amended_v4_4.md")
    parser.add_argument("--output", default="verification/m3_control_family_closure_results.json")
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    spec_path = Path(args.spec)
    output_path = Path(args.output)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    spec_text = spec_path.read_text(encoding="utf-8")
    errors, summary = validate(inventory, spec_text)
    result = {
        "schema_version": "m3-control-family-closure-results-v1",
        "gate": "M3 V4.3 Systemic Pre-Scoring Closure Gate",
        "base_commit": "8259e01a1dfac6a09074027d9a48f034bf51d9b9",
        "command": "python verification/verify_m3_control_family_closure.py",
        "scope": "specification_only",
        "inventory_sha256": sha256(inventory_path),
        "spec_sha256": sha256(spec_path),
        "summary": summary,
        "errors": errors,
        "verdict": "PASS" if not errors else "FAIL",
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
