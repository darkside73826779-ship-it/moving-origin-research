# M3/E2 V4.3 Targeted Amendment — L1 Shuffled-Arm Calibration

**Status:** AMENDED DRAFT — requires closure-audit evidence and independent CRITIC clearance before any fresh scoring run

**Date:** 2026-08-16

**Author:** ARCHITECT

**Gate served:** Rebecca's binding M3 Block Ruling, `docs/rulings/REBECCA_M3_BLOCK_RULING.md`

**Exact base commit:** `8e9f83a6f7fac8dd6682a446c2730ed14752cc8c`

## 0. Scope and authority

This is a narrow replacement of the L1 shuffled-arm text in §2.9 and the shuffled-arm clause in §2.11. All candidate-facing bars, all other L18 controls, the L15 integration fence, L9 fence, D1–D5, O-14, O-15, and the unseen-seed policy remain unchanged.

The correction is post-scoring and is authorized only under Rebecca's four-part test. The seeds 201–203 result remains retained under its original `INSTRUMENT FAILURE` label. No value from that run sets or tunes the corrected threshold. Any later scoring is a new full M3 battery on three fresh seeds from the authorized scoring pool, through Rebecca's supervised executor; it is not a re-run.

## 1. Replacement text for §2.9 — Shuffled row only

Replace the `Shuffled` row of §2.9 with:

| Arm | Exact expected statistic / bound | Artifact fields | Instrument-failure consequence if arm behaves otherwise |
|---|---|---|---|
| Shuffled | Realized rehearsal counts decorrelate from the age-bin/rehearsal-level design (§2.8). The only meaningful failure direction is **excess positive residual rehearsal association**: a conditional Spearman `rho` above its calibrated upper null bound means shuffling failed to destroy the intended association. A value at or below the bound, including a value below the old lower band, means destruction was at least as strong as the null expectation and is never a failure. For each scoring seed `s`, generate exactly `R=1000` pre-registered seeded null reassignments by the existing §2.9 shuffled-null procedure. Replicate `r` produces the five bin statistics `rho_null[s,r,b]`, `b in {0,...,4}`. Form the null-of-the-max statistic `M[s,r] = max_b rho_null[s,r,b]`. Let `M_sorted[s,1] <= ... <= M_sorted[s,1000]` be the nondecreasing order statistics and define the reported upper threshold `T_s = M_sorted[s,985]` (one-indexed; no percentile interpolation). For the observed shuffled arm, form `M_obs[s] = max_b rho_obs[s,b]` and the tie-conservative randomization p-value `p_s = (1 + sum_r I[M[s,r] >= M_obs[s]]) / 1001`. **Per-seed pass:** `p_s > 0.05/3`; equivalently in the no-tie case, `M_obs[s] <= T_s`. The p-value rule is binding if ties make the threshold shorthand differ. **Run-level pass:** all three seed-level tests pass. This controls all 15 shuffled checks (5 bins × 3 seeds) as one family: maximization controls the 5 bins within seed and Bonferroni controls the 3 seeds. The smallest rejecting tail has probability at most `16/1001` per seed, so `FWFP <= 3*(16/1001) = 48/1001 = 0.047952... < 0.05`, without assuming independence among bins or seeds. Age-conditional tests (§2.6) remain unchanged and must still pass because age is untouched. | `{arm:"shuffled", direction:"upper_only", bins:5, null_replicates:1000, multiplicity_family:{arms:["L1.shuffled"], scoring_seeds:3, bins_per_seed:5, total_checks:15}, rho_observed[5], rho_null[1000][5], null_max[1000], null_max_order_statistic_index_1based:985, upper_threshold, observed_max, exceed_or_tie_count, randomization_p_value, per_seed_alpha:0.016666666666666666, per_seed_pass, below_threshold_label, age_tests_pass}` plus run summary `{method:"null_of_max_plus_bonferroni", seed_p_values[3], familywise_bound_fraction:"48/1001", familywise_bound:0.04795204795204795, familywise_bar:0.05, familywise_pass}` | `p_s <= 0.05/3` for any scoring seed: **INSTRUMENT FAILURE** — shuffled assignment retains excessive positive rehearsal association after within-seed and across-seed multiplicity control. For every bin with `rho_obs <= T_s`, including any value below the former lower band, record `below_threshold_label:"shuffle exceeded typical destruction — informational"`; this label never gates. Missing/malformed null arrays, a count other than 1000 replicates × 5 finite rho values, an order-statistic index other than 985, failure to reproduce `p_s`, or closure-audit `familywise_pass != true`: **INSTRUMENT FAILURE**. |

### 1.1 Binding comparison rule

For each scoring seed, evaluate one seed-level hypothesis using `M_obs[s]`; do not evaluate five independent bin-level bands. The five observed `rho` values remain mandatory artifact data for diagnosis, but no individual lower-tail event can fail and no unadjusted bin-level upper comparison can fail.

### 1.2 Fixed constants and seeds

`R=1000`, five bins, three scoring seeds, `alpha_family=0.05`, `alpha_seed=0.05/3`, the plus-one randomization p-value, and order-statistic index 985 are fixed before fresh scoring. Null-replicate RNG identities must be deterministically derived from the scoring seed and replicate index under a documented domain-separated hash; they must not reuse the shuffled observed-assignment draw. The artifact records the derivation label and all 1000×5 null statistics, but the amendment does not name or expose any fresh scoring seed.

## 2. Replacement text for §2.11 — Shuffled clause only

In §2.11, replace:

> OR any shuffled conditional rho falls outside its empirical-null band

with:

> OR, for any scoring seed, the shuffled arm's upper-only null-of-the-max randomization test has `p_s <= 0.05/3` as defined in §2.9; OR the shuffled multiplicity artifact is missing, malformed, arithmetically irreproducible, or reports a run-level familywise bound above 0.05. A shuffled `rho` at or below its calibrated upper threshold — including a value below the former lower band — is informational (`shuffle exceeded typical destruction`) and never enters PASS, KILL, or INSTRUMENT FAILURE.

Add to §2.11's `PASS` branch:

> and all three shuffled seed-level null-of-the-max tests have `p_s > 0.05/3`, with closure-audit `familywise_pass = true`.

No shuffled-arm outcome is a candidate-facing KILL. All candidate PASS/KILL predicates are unchanged.

## 3. Mandatory pre-scoring closure audit

Before CRITIC clearance and before any fresh scoring packet is executable, the closure audit must:

1. Recompute `M[s,r]` from each raw 1000×5 null matrix and verify elementwise that it is the row maximum.
2. Recompute `T_s` as one-indexed order statistic 985 without interpolation.
3. Recompute each plus-one `p_s` from the raw null maxima and observed maximum.
4. Verify the per-seed rejection probability bound `16/1001` and run-family union bound `3*16/1001 = 48/1001 < 0.05`.
5. Report the complete battery family inventory (`arms × bins × scoring seeds`), directionality justification for every control, and computed FWFP for every arm's full check battery. Any control with FWFP above 0.05 blocks scoring and must be corrected under the standing ruling; it may not be waived or relabeled.
6. Emit `m3_control_familywise_closure.json` with schema:

The exact required control-family inventory is `L1.{frozen,fair_naive,recency_only,rehearsal_only,permuted,shuffled,oracle,empty}`, `L3.{frozen,oracle,permuted,shuffled,empty}`, `L5.{single_axis,full_scan,oracle,frozen,permuted,shuffled,empty}`, and `L6.{empty,permuted,shuffled,oracle,frozen,fair_naive}`: 26 family rows total. A family row may use an analytic bound, an exact deterministic bound, or an empirical-null bound, but must name the method and compute the full battery's FWFP. The L1 shuffled row below is frozen exactly; the other 25 rows inherit their checks and bars unchanged and must be populated by the closure auditor without changing them.

```json
{
  "schema_version": "m3-control-familywise-closure-v1",
  "spec_amendment": "m3_e2_spec_amendment_v4_3",
  "alpha_family": 0.05,
  "expected_family_count": 26,
  "family_inventory_complete": true,
  "families": [
    {
      "arm_id": "L1.shuffled",
      "meaningful_failure_direction": "upper",
      "direction_justification": "excess positive rho means shuffle retained rehearsal signal; lower rho means stronger destruction",
      "scoring_seed_count": 3,
      "checks_per_seed": 5,
      "total_checks": 15,
      "null_replicates_per_seed": 1000,
      "within_seed_method": "null_of_max",
      "across_seed_method": "bonferroni",
      "order_statistic_index_1based": 985,
      "per_seed_tail_bound_fraction": "16/1001",
      "familywise_bound_fraction": "48/1001",
      "familywise_bound": 0.04795204795204795,
      "bar": 0.05,
      "pass": true
    }
  ],
  "all_control_families_at_or_below_bar": true,
  "verdict": "PASS"
}
```

If any arithmetic, raw-array, directionality, family-inventory, or schema check fails, verdict is `INSTRUMENT FAILURE: CLOSURE AUDIT`, scoring remains blocked, and the negative label is retained.

## 4. Quantitative closure

The old independent two-sided 95% treatment across 15 checks has `FWFP = 1 - 0.95^15 = 0.5367087698`. The one-sided-only treatment identified in Rebecca's ruling has `FWFP = 1 - 0.975^15 = 0.3159793144`. Neither meets 0.05.

The amended finite randomization rule has per-seed size at most `16/1001 = 0.0159840160`; the union bound across three scoring seeds is `48/1001 = 0.0479520480`. Thus the specified family is quantitatively satisfiable below the binding 5% bar without any independence assumption. `verification/verify_m3_l1_shuffled_fwfp.py` independently checks these constants.

## 5. Verdict and custody branches

- **Closure PASS:** arithmetic, family inventory, directionality, and artifact schema all verify; amendment proceeds to independent CRITIC review. This is not CRITIC clearance or scoring authorization.
- **Closure INSTRUMENT FAILURE:** retain that label, keep scoring blocked, and return the evidence to ARCHITECT/CRITIC. Do not tune the percentile from observed scoring values.
- **Fresh scoring instrument failure:** retain the fresh result under its original label. O-14 forbids re-running it.
- **Fresh scoring candidate failure:** retain the failure; this amendment supplies no redesign branch and changes no candidate-facing bar.
- **Fresh scoring pass:** report cross-run consistency against the retained 201–203 evidence as Rebecca required; no integrated L15–L17 claim follows.
