# ARCHITECT Handoff — M3 Reproducibility-Contract Specification (v1.1)

**Gate served:** M3 reproducibility-contract design + stale label fixes
**Issued by:** ARCHITECT
**Date:** 2026-08-17 13:31 EDT

---

## Input SHAs reviewed

| File | SHA | Verified |
|---|---|---|
| `src/m3_harness.py` | `f9d16fa` | GitHub main, verified via `git ls-remote` |
| `src/m3_v44_artifacts.py` | `f9d16fa` | GitHub main |
| `reviews/critic_m3_v44_scoring_results_review.md` | `f9d16fa` | GitHub main |
| `state/STATE.md` | `f9d16fa` | GitHub main |
| `docs/rulings/provenance_log.md` | `f9d16fa` (through Entry 52) | GitHub main |

## Files changed/created

| File | Commit | Description |
|---|---|---|
| `specs/m3_reproducibility_contract_v1.md` | `e8204de` (v1.0), `3c8480c` (v1.1) | Reproducibility-contract specification (623 lines) |
| `specs/m3_reproducibility_contract_changelog.md` | `e8204de` (v1.0), `3c8480c` (v1.1) | Companion changelog (162 lines) |
| `handoffs/ARCHITECT_M3_REPRODUCIBILITY_CONTRACT_HANDOFF.md` | `88582f0` (v1.0), this commit (v1.1) | This handoff |

## Branch/result SHA

- **Branch:** `architect/m3-reproducibility-contract`
- **Result SHA:** `3c8480cc163251f88db2b70b921f65a31468cc17`
- **Base SHA:** `f9d16fa` (GitHub main)
- **Remote verification:** `git ls-remote origin architect/m3-reproducibility-contract` returns `3c8480cc163251f88db2b70b921f65a31468cc17` — VERIFIED

## Verdict/status

**Specification v1.1 complete. CRITIC BF1–BF4 resolved. Ready for CRITIC re-review.**

### BF1–BF4 resolution summary

**BF1 (Classification C invariant #1):** The invariant for `permuted.rho_null_1000_values` is corrected to `[abs(x) for x in rho_null_1000_values] == null_statistics`. The signed raw rho vector is distinguished from the absolute-valued canonical null distribution. The previous direct-equality invariant would always fail when any null rho is negative.

**BF2 (Classification A/C overlap):** `abs_rho_null_1000` and `null_max_1000` are removed from Classification A family-specific extras. They appear ONLY in Classification C. Every field is now assigned to exactly one classification.

**BF3 (Top-level digest circularity):** Two-digest architecture implemented per Rebecca's directive. The compared scoring-semantic digest contains only per-law results + configuration (fields independently available from both passes). `overall_verdict`, `interface_invariants`, `finite_numeric_results`, `l20_self_test`, and `raw_artifact_validation` are excluded from the compared digest. A separate non-compared final-report digest is computed once after reproducibility and artifact validation, providing tamper-evidence for the complete output bundle. The final-report digest cannot affect `overall_verdict`.

**BF4 (Provenance):** Branch pushed to GitHub. Result SHA `3c8480cc163251f88db2b70b921f65a31468cc17` verified via `git ls-remote` against `darkside73826779-ship-it/moving-origin-research`. All provenance references corrected.

### NF1–NF4 resolution summary

**NF1/NF4:** Canonicalization rationale documented in §3.3 — `ensure_ascii=True` chosen for consistency with `_v44_canonical_json_hash`; NFC normalization noted as belt-and-suspenders.

**NF2:** "Where present" fields clarified in §2.5 and §3.4 — conditionally absent fields do not trigger fail-closed.

**NF3:** `rho_null_1000_values` retained as Classification C with corrected absolute-value invariant.

## Blockers and non-blocking findings

**No blockers.** All four CRITIC blocking findings resolved. No code implemented, no seeds run, no bars/controls modified.

## Exact next recipient role

**CRITIC** — Re-review the v1.1 specification for:
- BF1: Invariant correctness (signed vs absolute-valued rho)
- BF2: No classification overlap remains
- BF3: Two-digest architecture — compared digest contains only both-pass fields; final-report digest cannot affect overall_verdict
- BF4: Remote SHA verified and correct
- NF1–NF4 resolutions

After CRITIC approval: **TASK BUILDER** (implement) → **CRITIC** (verify implementation) → **RECORDER/INTEGRATOR** (publish).

## Explicitly prohibited actions

- No implementation, scoring, seed execution, or merging (ARCHITECT role boundary).
- No modification of STATE.md or provenance_log.md (RECORDER/INTEGRATOR custody).
- No modification of any locked bar, threshold, or scoring predicate.
- No running of scoring seeds or seeds 201–203 or 301–303.
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
