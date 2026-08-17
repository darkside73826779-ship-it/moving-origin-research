# CRITIC Handoff — M3 Reproducibility-Contract Specification Review

**Gate served:** M3 reproducibility-contract specification review (ARCHITECT → CRITIC)
**Date:** 2026-08-17 13:25 EDT
**Verdict:** BLOCK

---

## Inputs/SHAs reviewed

| File | SHA | Source |
|---|---|---|
| `specs/m3_reproducibility_contract_v1.md` | (uploaded attachment) | ARCHITECT handoff |
| `specs/m3_reproducibility_contract_changelog.md` | (uploaded attachment) | ARCHITECT handoff |
| `src/m3_harness.py` | `f9d16fa` | GitHub main (fetched and verified) |
| `src/m3_v44_artifacts.py` | `f9d16fa` | GitHub main (fetched and verified) |
| `reviews/critic_m3_v44_scoring_results_review.md` | `f9d16fa` | Local checkout |
| `state/STATE.md` | `f9d16fa` | Local checkout |
| `docs/rulings/provenance_log.md` | `f9d16fa` (through Entry 52) | Local checkout |
| `handoffs/ARCHITECT_M3_REPRODUCIBILITY_CONTRACT_HANDOFF.md` | local checkout | WORKFLOW COORDINATOR routing |

**Base SHA verified:** `f9d16fa` exists on GitHub as `f9d16fad3061672c1646d8d05c19f6457bb30836`.

**Result SHA NOT verified:** `e8204de83019e1ad2b1edba70a15de3f466112d6` does not exist on GitHub. Branch `architect/m3-reproducibility-contract` does not exist on GitHub.

---

## Verdict: BLOCK

Four blocking findings. The specification is substantively accurate in its field enumeration, line references, and problem diagnosis, but contains spec-internal contradictions and a design gap that would force the TASK BUILDER to improvise.

---

## Blocking findings

### BF1 — Classification C invariant #1 is mathematically incorrect (spec defect)

**Location:** §2.5 Classification C, first row.

The spec states: `permuted.rho_null_1000_values` must equal `v44_stochastic_controls.permuted.null_statistics` element-wise.

**Code reality (verified at `f9d16fa`, lines 2450–2468, 2615):**
- `permuted.rho_null_1000_values` = `null_rhos` (raw signed Spearman rho values; can be negative)
- `v44_stochastic_controls.permuted.null_statistics` = `abs_null_rhos` (absolute values, because `_v44_summary` is called with `abs_null_rhos` as `null_values`)

These are NOT element-wise equal when any null rho is negative — which is expected behavior for Spearman correlation null distributions. The invariant as specified would always fail in practice, raising `ReproducibilityInvariantError` on every run.

**Required fix (ARCHITECT scope):** Either change the invariant to `[abs(x) for x in rho_null_1000_values] == null_statistics`, reclassify `rho_null_1000_values` as Classification B (non-digest, optional), or remove the field entirely (the ARCHITECT's own non-blocking finding already flags this field as potentially removable).

### BF2 — Classification A/C overlap violates "exactly one classification" rule (spec defect)

**Location:** §2.5 Classification A (family-specific extras) and §2.5 Classification C.

The spec states (§2.2): "Every field in the raw results dictionary must fall into exactly one of three classifications."

Two fields appear in BOTH Classification A and Classification C:

| Field | Classification A location | Classification C location |
|---|---|---|
| `v44_stochastic_controls.permuted.abs_rho_null_1000` | §2.5 permuted family extras (line 183) | §2.5 Classification C table (line 235) |
| `v44_stochastic_controls.shuffled.null_max_1000` | §2.5 shuffled family extras (line 184) | §2.5 Classification C table (line 236) |

This creates ambiguity for:
- Fail-closed traversal: which classification takes precedence?
- Mutation tests (§5.1): should mutating `abs_rho_null_1000` change the digest (because it's A) or trigger an invariant check (because it's C)? Both cannot apply simultaneously.
- §4.2 lists both as Classification A fields that must be retained, contradicting their Classification C designation.

**Required fix (ARCHITECT scope):** Assign each field to exactly one classification. Since both are derived duplicates with computable invariants, Classification C is the natural choice — remove them from the Classification A family-specific extras lists.

### BF3 — Top-level digest inputs not available from specified function signature (spec defect)

**Location:** §2.4, §3.1, §3.3.

The spec specifies `compute_scoring_semantic_digest(results, config)` as the digest function, and §3.3 shows the digest payload includes `"top_level": { "overall_verdict", "interface_invariants", "finite_numeric_results", "l20_self_test", "raw_artifact_validation" }`.

**Code reality (verified at `f9d16fa`, `main()` lines 3836–4063):**

Execution order in `main()`:
1. Line 3930: `interface_invariants = run_interface_invariants()` — computed BEFORE reproducibility check
2. Line 3935: `all_finite = _check_finite(all_results)` — BEFORE
3. Line 3979: `l20_result = l20_self_test(profile_vector)` — BEFORE
4. Lines 3984–4009: Reproducibility check (second pass + comparison)
5. Line 4027: `validate_manifest(output_dir)` — AFTER
6. Lines 4053–4063: `overall` verdict — AFTER

Problems:
- `raw_artifact_validation` and `overall_verdict` are computed AFTER the reproducibility check. They cannot be in the digest unless the execution order changes.
- The second pass (lines 3984–3998) only re-runs `run_l1`/`run_l3`/`run_l5`/`run_l6`. It does NOT re-compute `interface_invariants`, `finite_numeric_results`, `l20_self_test`, `raw_artifact_validation`, or `overall_verdict`. The digest for pass 2 cannot include these fields without additional computation.
- The function signature `(results, config)` does not accept these top-level values as parameters.

**Required fix (ARCHITECT scope):** Specify either (a) an expanded function signature that accepts the top-level fields as additional parameters, (b) which top-level fields are excluded from the digest (with rationale), or (c) a reordering of `main()` to compute all top-level fields before the reproducibility check, plus specification of which top-level fields the second pass must re-compute.

### BF4 — Result SHA and branch do not exist on GitHub (provenance defect)

**Location:** ARCHITECT handoff, "Branch/result SHA" section.

The handoff claims:
- Branch: `architect/m3-reproducibility-contract`
- Result SHA: `e8204de83019e1ad2b1edba70a15de3f466112d6`

Neither exists on GitHub (`darkside73826779-ship-it/moving-origin-research`). The specification files were provided as uploaded attachments, not committed to the repository.

The base SHA `f9d16fa` was verified correct. All line-number references in the spec were verified against the code at `f9d16fa`.

**Impact:** The CRITIC cannot independently verify that the provided attachments match a committed result SHA. The private repo is the single source of truth per the project's Persistence Doctrine. D1–D5 provenance is implicated.

**Required fix (ARCHITECT scope):** Commit the specification to the `architect/m3-reproducibility-contract` branch and push to GitHub. Re-issue the handoff with a verifiable result SHA.

---

## Non-blocking findings

### NF1 — Two canonicalization methods in the codebase

The spec §3.2 specifies `ensure_ascii=True` (matching `_v44_canonical_json_hash` in `m3_harness.py` line 2191), while `_canonical_json_bytes` in `m3_v44_artifacts.py` (line 100) uses `ensure_ascii=False`. This is a defensible design choice but creates two different canonicalization methods. Consider documenting the rationale for future maintainers.

### NF2 — Conditionally-present Classification A fields need fail-closed guidance

Fields marked "where present" in §2.5 (`cross_slot_hashes`, `all_exact_checks_pass`, `deterministic_reproduction_equal_across_seed_slots`) are conditionally absent. The spec's fail-closed enforcement (§3.4) says missing Classification A fields should raise `ReproducibilityProjectionError` (§5.2). The spec should clarify that "where present" fields are optionally absent without triggering fail-closed.

### NF3 — `rho_null_1000_values` removal opportunity

The ARCHITECT's own non-blocking finding flags `permuted.rho_null_1000_values` as potentially removable. Given BF1 (the invariant is incorrect), removing this field or reclassifying it as Classification B would resolve BF1 cleanly.

### NF4 — NFC normalization is redundant with `ensure_ascii=True`

With `ensure_ascii=True`, all non-ASCII characters are escaped as `\uXXXX` sequences. NFC normalization before JSON serialization still has an effect (ensuring consistent Unicode representation before escaping), but the spec should note this is belt-and-suspenders, not identical to either existing canonicalization method.

---

## Preserved evidence

- Base SHA `f9d16fa` verified on GitHub — all line-number references in the spec match exactly (15+ references checked).
- All field differences between pass 1 and pass 2 (§0) verified accurate against the code.
- All V44 constants and locked bar names exist in the code.
- `_v44_summary` structure, `_nfc()` function, `validate_manifest()`, `_v44_verify_l1_cross_slot_identity` output — all verified.
- Top-level output field structures (`interface_invariants`, `l20_self_test`, `raw_artifact_validation`) — all verified.
- L6 confirmed: no `artifact_writer`, no artifact-dependent fields, all fields deterministic.
- Stale labels confirmed hardcoded at lines 4078, 4167, 4168, 4204.
- No bars, controls, or scoring logic modified by the specification.
- No scoring run, seed execution, or hold-out seed exposure occurred.
- INSTRUMENT FAILURE label retained — not renamed or reinterpreted.

---

## Exact next authorized role

**ARCHITECT** — Resolve BF1–BF4, then re-submit for CRITIC review.

After CRITIC approval: **TASK BUILDER** (implement) → **CRITIC** (verify implementation) → **RECORDER/INTEGRATOR** (publish).

---

## Explicitly prohibited actions

- No implementation, scoring, seed execution, or merging (ARCHITECT role boundary).
- No modification of STATE.md or provenance_log.md (RECORDER/INTEGRATOR custody).
- No modification of any locked bar, threshold, or scoring predicate.
- No running of scoring seeds or seeds 201–203 or 301–303.
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.

---

## Confirmation

No scoring, rerun of failed scoring, hold-out seed exposure, or unauthorized merge occurred during this review. The CRITIC reviewed the specification read-only and did not modify any specification, implementation, scoring artifact, or STATE.md.

D1–D5 provenance is implicated by BF4 (missing result SHA). No other standing constraints were violated: O-14 (no re-run-on-failure) — not applicable; O-15 (development runs diagnostic-only) — mutation tests specified as diagnostic with synthetic fixtures or seeds 101–105; L9 (hard fence) — not touched; L18 (full battery) — not modified; ≥2 unseen scoring seeds — not applicable (no scoring run authorized); no L15/L16/L17 introduced.
