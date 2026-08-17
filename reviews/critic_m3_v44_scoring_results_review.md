# CRITIC M3 V4.4 Scoring Results Review

**Run:** Seeds 301, 302, 303 on commit `95440b4`
**Verdict: BLOCK — INSTRUMENT FAILURE confirmed**

---

## What happened

| Law | 301 | 302 | 303 |
|---|---|---|---|
| L1 | PASS | PASS | PASS |
| L3 | PASS | PASS | **INSTRUMENT_FAILURE** |
| L5 | PASS | PASS | PASS |
| L6 | PASS | PASS | PASS |

No kill conditions fire. Candidate passes all candidate-facing bars on all 3 seeds.

## L3 frozen arm failure (seed 303)

The V4.4 calibrated test caught a borderline case. The frozen state IS harmful (all reductions strongly negative: -1.42 to -2.04), but the observed max reduction (-1.419) is slightly less negative than the null 985th percentile (-1.437). Gap: 0.019.

- p-value: 12/1001 = 0.012
- alpha_seed: 0.05/3 = 0.0167
- 0.012 < 0.0167 → INSTRUMENT_FAILURE

**Classification:** Genuine borderline case within the pre-registered false-positive rate (48/1001 ≈ 4.8% familywise). Not a construction bug, not a spec defect, not a candidate failure. The V4.4 calibrated test is more sensitive than the old unproved "reduction_h ≤ 0%" check it replaced.

## Reproducibility failure — construction bug diagnosed

`bit_identical = False` is a false alarm. The second pass calls `run_l1(seed)` etc. without `artifact_writer`, while pass 1 passes it. This causes structural differences (different fields present/absent) that make the comparison always fail — not actual non-determinism.

**Impact on scored metrics:** None. P-values verified from integer counts.

**Fix:** Pass `artifact_writer` to the second pass, or strip artifact-dependent fields from the projection.

## V4.4 L1 fix worked

Shuffled p-value = 1.000 on all 3 seeds. The first run's L1 INSTRUMENT_FAILURE (seeds 201/203, two-sided band, 54% FWFP) is fully resolved by the one-sided null-of-the-max test.

## Cross-run consistency

- Candidate: PASS all bars in both runs (201-203, 301-303) — stable
- L1: first run failed (2/3), this run passes (3/3) — V4.4 fix resolved it
- L3: first run passed (unproved check), this run fails (calibrated check) — V4.4 is more sensitive
- L5, L6: consistent across both runs

## Non-blocking findings

- **NB1:** Reproducibility checker construction bug (see above)
- **NB2:** Phase B raw-artifact recomputation not completed (16.3 GB retained locally)
- **NB3:** Stale "development" scope label in seed ledger
- **NB4:** Stale "development" boilerplate in manifest

## Preserved evidence

- L1/L5/L6 PASS on all 3 seeds — valid scored evidence
- L3 candidate bars PASS on all 3 seeds
- L3 PASS on seeds 301/302 — valid scored evidence
- No kill conditions in either run
- Seeds 201-203 retained as INSTRUMENT FAILURE, never rerun
- Seeds 301-303 are scored evidence — fresh seeds required for any future run

## Recommendation

**M3 delivery remains BLOCKED.** The candidate is strong (passes everything in both scoring runs), but cannot deliver green because:

1. L3 seed 303 frozen arm is a governing instrument failure (pre-registered, within expected false-positive rate)
2. Reproducibility check failed (construction bug, but artifacts can't certify bit-identical)
3. Full Phase B raw recomputation outstanding

**If Rebecca authorizes another run:** fresh seeds only (never rerun 201-203 or 301-303). Fix the reproducibility bug first. The L3 frozen arm test is working correctly — no spec change is warranted.
