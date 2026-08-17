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
| Base (GitHub main) | `a5e8a15` | Verified — includes PR #18 + PR #19 |
| Spec content SHA | `3c8480c` | On branch `architect/m3-reproducibility-contract`; CRITIC-verified |
| Branch | `taskbuilder/m3-reproducibility-contract` | Pushed to GitHub |
| Result SHA (implementation) | `cb8d3d0` | First implementation commit |
| Result SHA (required-field fix) | `be4eaa0` | Amended commit with required-field validation |
| Branch HEAD | `be4eaa0` | Latest |

## Files changed/created

| File | Action | Description |
|---|---|---|
| `src/m3_reproducibility.py` | Created | Reproducibility contract module (classification tables, digests, fail-closed, mode labels) |
| `src/m3_harness.py` | Modified | Pruning fix, RNG summaries, two-digest architecture, mode-aware labels |
| `src/test_m3_reproducibility.py` | Created | 18 tests: mutation (§5.1–§5.4), stale label regression (§6.3) |
| `src/M3_REPRODUCIBILITY_CONTRACT_CHANGES.md` | Created | Implementation changelog |

## What was implemented

1. **`compute_scoring_semantic_digest(results, config)`** (§3.1) — Classification A extraction, Classification C invariant checks, fail-closed traversal with required-field validation, canonical digest
2. **`compute_final_report_digest(...)`** (§3.2) — non-compared integrity hash over complete output bundle
3. **Classification A field retention** (§4.2) — `null_statistics` and all Classification A fields retained in both passes; only Classification B fields pruned
4. **Normalized RNG derivation summaries** (§2.5) — built from `draw.artifact_record(...)` at draw time, independent of `artifact_writer`
5. **Mode-aware label helper** (§6.2) — `_mode_label(mode, key)` for manifest and ledger
6. **Mutation tests** (§5.1–§5.4) — automated leaf traversal, fail-closed, invariant, non-digest field, final-report digest
7. **Stale label regression tests** (§6.3)
8. **Required-field validation** — `_check_required` verifies all non-"where present" Classification A fields are present; raises `ReproducibilityProjectionError` on missing fields
9. **Recursive list-item fail-closed** — `_check_list_items` recursively checks fields in list-of-dicts items: `chain_walk_results`, `query_results_200`, `reachability_audit`, `attacks`, `paired_age_accessibility_200`, `rng_derivation_summaries`

## What was verified (diagnostic results)

- **Import:** Both modules import cleanly
- **Reproducibility check:** `digests_equal=True` on diagnostic run (seed 101, L1, `--verify-reproducibility`)
- **Output structure:** Matches §4.3 (checked, certification, pass1_digest, pass2_digest, digests_equal, projection_schema_version, projection_classification_failures, invariant_failures, final_report_digest)
- **Mode labels:** Development mode correct; scoring mode correct
- **Fail-closed:** `ReproducibilityProjectionError` raised on unclassified field and on missing required field
- **Test suite:** All 18 new tests pass (0 expected failures); all 20 existing tests pass; no regressions
- **Non-scoring per O-15:** Only seed 101 used in diagnostics

## Additional fix

- **Pre-existing variable shadowing bug:** `null_rhos` from L1 shuffled section overwrote L1 permuted section's value. Fixed by preserving signed rhos in `permuted_null_rhos_signed` before the shuffled section reuses the variable name.

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
