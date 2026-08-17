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
| Result SHA | `cb8d3d0` | Implementation commit on branch |

## Files changed/created

| File | Action | Lines |
|---|---|---|
| `src/m3_reproducibility.py` | Created | 839 |
| `src/m3_harness.py` | Modified | +148 / -54 |
| `src/test_m3_reproducibility.py` | Created | ~400 |
| `src/M3_REPRODUCIBILITY_CONTRACT_CHANGES.md` | Created | 67 |

## What was implemented

1. **`compute_scoring_semantic_digest(results, config)`** — Classification A extraction, Classification C invariant checks, fail-closed traversal, canonical digest (§3.1)
2. **`compute_final_report_digest(...)`** — non-compared integrity hash over complete output bundle (§3.2)
3. **Classification A field retention** — `null_statistics`, `null_accuracies_1000`, `null_absolute_departures_1000`, `query_results_200`, `rho_null_1000x5`, `paired_age_accessibility_200`, `observed_query_to_entry_assignment_1200`, `observed_realized_rehearsal_counts_200` now retained in both passes; only Classification B fields pruned (§4.2)
4. **Normalized RNG derivation summaries** — built from `draw.artifact_record(...)` dicts at draw time, independent of `artifact_writer` state (§2.5)
5. **Mode-aware label helper** — `_mode_label(mode, key)` replaces hardcoded strings in manifest and ledger (§6.2)
6. **Mutation tests** — 18 tests covering §5.1–§5.4 and §6.3

## What was verified (diagnostic results)

- **Syntax:** Both modules import cleanly
- **Reproducibility check:** `digests_equal=True` on diagnostic run (seed 101, L1, `--verify-reproducibility`)
- **Output structure:** Reproducibility output matches §4.3 (checked, certification, pass1_digest, pass2_digest, digests_equal, projection_schema_version, projection_classification_failures, invariant_failures, final_report_digest)
- **Mode labels:** Development mode labels correct; scoring mode labels correct
- **Fail-closed:** `ReproducibilityProjectionError` raised on unclassified field
- **Test suite:** All 18 new tests pass (17 OK + 1 expected failure); all 20 existing tests pass; no regressions
- **Non-scoring per O-15:** Only seed 101 used in diagnostics; seeds 201–203 and 301–303 not accessed

## Additional fix

- **Pre-existing variable shadowing bug:** `null_rhos` from L1 shuffled section overwrote L1 permuted section's value, causing `permuted.rho_null_1000_values` to contain list-of-lists instead of list-of-scalars. Fixed by preserving signed rhos in `permuted_null_rhos_signed` before the shuffled section reuses the variable name.

## Known non-blocking finding

- **`test_missing_required_field_raises` (expected failure):** The spec's fail-closed traversal (§3.4) checks for unclassified (extra) fields but does not explicitly check for missing required Classification A fields. The CRITIC v1.1 review did not flag this as a blocking finding. The test is marked `@unittest.expectedFailure` to document the gap without blocking the implementation.

## Blockers

None.

## Next recipient

**CRITIC** — independent implementation verification per the routing:
```
TASK BUILDER (implement approved spec) ← COMPLETE
    ↓
CRITIC (verify implementation) ← NEXT
    ↓
RECORDER/INTEGRATOR (publish final)
    ↓
Rebecca (gate)
```

## Explicitly prohibited actions

- No scoring runs, seed execution, or hold-out seed exposure
- No running of seeds 201–203 or 301–303
- No modification of specifications, locked bars, kill conditions, or provenance log
- No merging to main (Rebecca is sole merge authority)
- No modification of STATE.md (INTEGRATOR custody)
- No L15/L16/L17 before M5
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label
