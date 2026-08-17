# ARCHITECT Handoff — M3 Reproducibility-Contract Specification

**Gate served:** M3 reproducibility-contract design + stale label fixes
**Issued by:** ARCHITECT
**Date:** 2026-08-17 12:50 EDT

---

## Input SHAs reviewed

| File | SHA |
|---|---|
| `src/m3_harness.py` | `f9d16fa` (base) |
| `src/m3_v44_artifacts.py` | `f9d16fa` (base) |
| `reviews/critic_m3_v44_scoring_results_review.md` | `f9d16fa` (base) |
| `state/STATE.md` | `f9d16fa` (base) |
| `docs/rulings/provenance_log.md` | `f9d16fa` (base, through Entry 52) |

## Files created

| File | Description |
|---|---|
| `specs/m3_reproducibility_contract_v1.md` | Reproducibility-contract specification (572 lines) |
| `specs/m3_reproducibility_contract_changelog.md` | Companion changelog (111 lines) |

## Branch/result SHA

- **Branch:** `architect/m3-reproducibility-contract`
- **Result SHA:** `e8204de83019e1ad2b1edba70a15de3f466112d6`
- **Base SHA:** `f9d16fa` (GitHub main)

## Verdict/status

**Specification complete. Ready for CRITIC review.**

The specification defines:
1. A versioned reproducibility projection (`m3_scoring_semantic_reproducibility_v1`) with three-class field classification (A=digest-included, B=explicit non-digest, C=derived duplicates with invariant checks).
2. An allowlist-based fail-closed enforcement: any unclassified field triggers an error, not silent exclusion.
3. A canonical SHA-256 digest over NFC-normalized, sorted-key, compact-separator, `allow_nan=False` JSON.
4. Requirements to preserve `null_statistics` and all Classification A fields in both passes (before artifact-mode pruning).
5. Normalized RNG derivation summaries built at draw time, independent of artifact writer state.
6. Top-level configuration block and output fields (`overall_verdict`, `interface_invariants`, `finite_numeric_results`, `l20_self_test`, `raw_artifact_validation`) in the digest.
7. Output label: "bit-identical scoring-semantic reproducibility."
8. Mutation test requirements: automated leaf traversal, fail-closed tests, non-digest field tests, key-order tests.
9. Stale label fix: mode-aware helper for three fields (ledger `scope`, manifest `scoring_seed_pool`, manifest `r3_note`), with regression tests.
10. Raw-artifact manifest validation continues separately and unchanged.

## Blockers and non-blocking findings

**No blockers.** The specification is design-only; no code was implemented, no seeds were run, no bars or controls were modified.

**Non-blocking findings:**
- The specification requires TASK BUILDER to restructure the artifact-mode pruning so Classification A fields are retained in the results dictionary regardless of `artifact_writer` state. This is a code change, not a spec change — it falls within TASK BUILDER's implementation scope.
- The specification identifies `permuted.rho_null_1000_values` (L1 top-level) as a Classification C duplicate of `v44_stochastic_controls.permuted.null_statistics`. The TASK BUILDER should verify whether this field is still needed or can be removed in favor of the canonical location.
- Future extension (hash-only artifact writer, §8) is explicitly out of scope.

## Exact next recipient role

**CRITIC** — Review the reproducibility-contract specification for:
- Correctness of the allowlist (every scoring-relevant field included; no scoring field silently excluded)
- Completeness of fail-closed coverage (every possible field path classified)
- Correctness of Classification C invariant checks
- Correctness of the canonical digest method
- Completeness of mutation test requirements
- Correctness of stale label fix specification
- No bars, controls, or scoring logic modified
- No standing constraints violated (O-14, O-15, D1–D5, L9, L18)

After CRITIC approval: **TASK BUILDER** (implement) → **CRITIC** (verify implementation) → **RECORDER/INTEGRATOR** (publish).

## Explicitly prohibited actions

- No implementation, scoring, seed execution, or merging (ARCHITECT role boundary).
- No modification of STATE.md or provenance_log.md (RECORDER/INTEGRATOR custody).
- No modification of any locked bar, threshold, or scoring predicate.
- No running of scoring seeds or seeds 201–203 or 301–303.
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
