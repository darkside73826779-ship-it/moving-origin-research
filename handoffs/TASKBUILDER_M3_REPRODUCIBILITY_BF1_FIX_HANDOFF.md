# TASK BUILDER Handoff — CRITIC BF1 Fix

**To:** CRITIC (re-verification)
**From:** TASK BUILDER
**Date:** 2026-08-17
**Gate served:** M3 reproducibility-contract implementation — BF1 fix
**Authoritative base:** `a5e8a15` (GitHub main)
**Repository:** `darkside73826779-ship-it/moving-origin-research`

## Disposition

**BF1 FIXED — ready for CRITIC re-verification.**

## SHAs

| Item | SHA | Status |
|---|---|---|
| Base (GitHub main) | `a5e8a15` | Verified |
| Branch | `taskbuilder/m3-reproducibility-contract` | Pushed to GitHub |
| Branch HEAD | `e42dec5` | Latest — includes BF1 fix |

## BF1 fix

**Finding:** `v44_artifact_support` was incorrectly required for L3 and L5 despite being Classification B (optional per spec §4.1).

**Fix applied:**
- L3 (`_fail_closed_l3`): Removed `v44_artifact_support` from the required container set. Now `frozenset({'empty', 'v44_stochastic_controls'})` — `v44_artifact_support` accepted as optional Classification B.
- L5 (`_fail_closed_l5`): Removed `v44_artifact_support` from `_l5_required_arms`. Now matches L1 pattern where `v44_artifact_support` is in Classification B only.

**Verification:**
- Empirically tested: L3 result dict without `v44_artifact_support` is accepted without error (digest computed successfully).
- All 54 tests pass (34 new + 20 existing, 0 expected failures).
- No regressions.

## Non-blocking findings addressed

- NF3: Corrected line count in changes note (839 → 961)
- NF4: Corrected classification of `abs_rho_null_1000` and `null_max_1000` in changes note (Classification C, not A)

## Files changed in this fix

| File | Change |
|---|---|
| `src/m3_reproducibility.py` | 2 lines removed (v44_artifact_support from L3 and L5 required sets) |
| `src/M3_REPRODUCIBILITY_CONTRACT_CHANGES.md` | NF3/NF4 corrections |

## Next recipient

**CRITIC** — re-verify BF1 fix only. Implementation otherwise unchanged from prior review at `34dd17b`.

## Explicitly prohibited actions

- No scoring runs, seed execution, or hold-out seed exposure
- No running of seeds 201–203 or 301–303
- No modification of specifications, locked bars, kill conditions, or provenance log
- No merging to main (Rebecca is sole merge authority)
- No modification of STATE.md (INTEGRATOR custody)
- No L15/L16/L17 before M5
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label
