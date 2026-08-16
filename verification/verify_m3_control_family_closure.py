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
    "Only empty is deterministic. Frozen, oracle, permuted, and shuffled all consume a scoring-seed-specific noisy AR(3) sequence",
    "Raw returned-artifact schemas for complete JUDGE recomputation",
    "contains no hard-coded set of stochastic family IDs",
    "replace CRLF and lone CR with LF",
]


def canonical_text_bytes(path: Path) -> bytes:
    """Canonical UTF-8/LF bytes, independent of checkout newline policy."""
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.rstrip("\n") + "\n"
    return text.encode("utf-8")


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_text_bytes(path)).hexdigest()


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

    classification_evidence = inventory.get("classification_evidence", {})
    if set(classification_evidence) != EXPECTED_IDS:
        fail(errors, "classification evidence must cover exactly all 26 families")
    variability_flags = {
        "scoring_seed_enters", "random_generator_enters", "fitted_model_enters",
        "sampled_observations_enter",
    }
    derived_types: dict[str, str] = {}
    for family_id, evidence in classification_evidence.items():
        if not variability_flags <= set(evidence) or "exact_basis" not in evidence:
            fail(errors, f"{family_id}: classification evidence incomplete")
            continue
        values = [evidence[key] for key in sorted(variability_flags)]
        if not all(isinstance(value, bool) for value in values):
            fail(errors, f"{family_id}: variability flags must be booleans")
            continue
        has_variability = any(values)
        exact_basis = evidence["exact_basis"]
        if has_variability:
            if exact_basis is not None:
                fail(errors, f"{family_id}: variable family cannot assert exact_basis without a universal proof schema")
            derived_types[family_id] = "stochastic_empirical"
        else:
            if not isinstance(exact_basis, str) or len(exact_basis.strip()) < 8:
                fail(errors, f"{family_id}: deterministic family needs a concrete exact_basis")
            derived_types[family_id] = "deterministic"

    raw_schemas = inventory.get("raw_artifact_schemas", {})
    common_raw_contract = inventory.get("raw_artifact_common_contract", {})
    required_common_raw = {
        "manifest_encoding", "numeric_array_encoding", "array_manifest_fields",
        "string_encoding", "finite_check", "judge_rule",
    }
    if required_common_raw - set(common_raw_contract):
        fail(errors, "raw artifact common binary contract incomplete")
    else:
        contract_blob = json.dumps(common_raw_contract, sort_keys=True).lower()
        for token in ("little-endian", "binary64", "int64", "uint8", "shape", "sha256", "finite", "row-major"):
            if token not in contract_blob:
                fail(errors, f"raw artifact common contract missing {token}")
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
        derived_type = derived_types.get(family_id)
        if reference_type != derived_type:
            fail(errors, f"{family_id}: declared {reference_type}, independently derived {derived_type}")
        pre = row["pre_correction_fwfp"]
        corrected = row["corrected_fwfp"]
        if reference_type == "stochastic_empirical":
            stochastic_count += 1
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
            schema = raw_schemas.get(family_id)
            if not isinstance(schema, dict):
                fail(errors, f"{family_id}: raw recomputation schema missing")
            else:
                raw_fields = schema.get("per_draw_required", [])
                if len(raw_fields) < 5 or not schema.get("judge_recomputes"):
                    fail(errors, f"{family_id}: raw schema insufficient")
                if f"raw_schema_id:{family_id}" not in row["artifact_fields"]:
                    fail(errors, f"{family_id}: artifact does not bind its raw schema")
            if pre.get("value", 0) > 0.05:
                corrections.append({
                    "family_id": family_id,
                    "pre_correction_fwfp": pre["value"],
                    "corrected_fwfp": value,
                    "method": row["corrective_method"],
                })
        elif reference_type == "deterministic":
            deterministic_count += 1
            if pre.get("applicable") or corrected.get("applicable"):
                fail(errors, f"{family_id}: deterministic stochastic FWFP must be inapplicable")
            if pre.get("value") != 0.0 or corrected.get("value") != 0.0:
                fail(errors, f"{family_id}: deterministic audit FWFP value must be zero")
        else:
            fail(errors, f"{family_id}: invalid reference_type {reference_type!r}")

    derived_stochastic_ids = {key for key, value in derived_types.items() if value == "stochastic_empirical"}
    if set(raw_schemas) != derived_stochastic_ids:
        fail(errors, "raw schema IDs must exactly equal independently derived stochastic families")

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
        "revision_base_commit": "b6accaad3773468d54b2363a1072877554186265",
        "command": "python verification/verify_m3_control_family_closure.py",
        "scope": "specification_only",
        "hash_canonicalization": "UTF-8 without BOM; CRLF/CR->LF; strip trailing LF; append exactly one LF; SHA-256",
        "inventory_sha256": canonical_sha256(inventory_path),
        "spec_sha256": canonical_sha256(spec_path),
        "summary": summary,
        "errors": errors,
        "verdict": "PASS" if not errors else "FAIL",
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
