# TASK BUILDER Handoff — M3 Reproducibility-Contract Implementation

**To:** CRITIC (implementation verification)
**From:** TASK BUILDER
**Date:** 2026-08-17
**Gate served:** M3 reproducibility-contract implementation (Rebecca-authorized, 2026-08-17 15:07 EDT)
**Authoritative base:** `a5e8a15` (GitHub main)
**Repository:** `darkside73826779-ship-it/moving-origin-research`

## Disposition

**IMPLEMENTATION COMPLETE — ready for CRITIC implementation verification.**

## SHAs

| Item | SHA | Status |
|---|---|---|
| Base (GitHub main) | `a5e8a15` | Verified |
| Spec content SHA | `3c8480c` | CRITIC-verified |
| Branch | `taskbuilder/m3-reproducibility-contract` | Pushed to GitHub |
| Branch HEAD | `e9c04a3` | Latest |

## Files changed/created

| File | Action |
|---|---|
| `src/m3_reproducibility.py` | Created — classification tables, digests, fail-closed, mode labels |
| `src/m3_harness.py` | Modified — pruning fix, RNG summaries, two-digest architecture, mode-aware labels |
| `src/test_m3_reproducibility.py` | Created — 34 tests |
| `src/M3_REPRODUCIBILITY_CONTRACT_CHANGES.md` | Created — changelog |

## What was implemented

1. `compute_scoring_semantic_digest(results, config)` (§3.1) — Classification A extraction, C invariant checks, fail-closed with required-field validation, canonical digest
2. `compute_final_report_digest(...)` (§3.2) — non-compared integrity hash
3. Classification A field retention (§4.2) — only Classification B fields pruned
4. Normalized RNG derivation summaries (§2.5) — built at draw time
5. `mode_label(mode, key)` (§6.2) — stale scoring label fix
6. Required-field validation — checks all non-"where present" Classification A fields are present
7. Recursive list-item fail-closed — checks fields in chain_walk_results, query_results_200, reachability_audit, attacks, paired_age_accessibility_200, rng_derivation_summaries, l18_arms
8. Required container/family checks — verifies all required sub-dicts (candidate, v44_stochastic_controls, etc.) and V4.4 families (frozen, permuted, shuffled, etc.) are present
9. 34 tests covering §5.1–§5.4 and §6.3

## What was verified

- **Import:** Both modules import cleanly
- **Reproducibility check:** `digests_equal=True` on diagnostic run (seed 101, L1, `--verify-reproducibility`)
- **Output structure:** Matches §4.3
- **Mode labels:** Development and scoring mode correct
- **Fail-closed:** `ReproducibilityProjectionError` raised on unclassified fields, missing required fields, and missing required containers/families
- **Nested fail-closed:** Errors raised for unexpected/missing fields in list items and row dicts
- **Test suite:** All 34 new tests pass (0 expected failures); all 20 existing tests pass; no regressions
- **Non-scoring per O-15:** Only seed 101 development diagnostic used; no scoring or held-out seed execution

## Additional fix

- Fixed pre-existing `null_rhos` variable shadowing bug in L1 permuted arm

## Blockers

None.

## Next recipient

**CRITIC** — independent implementation verification.

## Explicitly prohibited actions

- No scoring runs, seed execution, or hold-out seed exposure
- No running of seeds 201–203 or 301–303
- No modification of specifications, locked bars, kill conditions, or provenance log
- No merging to main (Rebecca is sole merge authority)
- No modification of STATE.md (INTEGRATOR custody)
- No L15/L16/L17 before M5
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label
