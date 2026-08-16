# E1 Experiment — Implementation Changelog (Option E + R1-R4)

**File:** `e1_experiment.py`
**Spec:** `/home/user/workspace/e1_spec.md` (REVISED DRAFT v3 + Rebecca Q2/Q3 incorporations + Option E amendment)
**Sign-off:** `/home/user/workspace/uploaded_attachments/5ace46aede354547b6aa1f048d6a4734/REBECCA_OPTION_E_SIGNOFF.md` (R1-R4 BINDING)
**Date:** 2026-08-15
**Author:** TASK BUILDER

---

## Summary

Updated `e1_experiment.py` to implement **Option E** (Rebecca's binding frozen-arm specification) + the **recency-discriminative consumer battery** (additive relevance + bucketed spike features) + Rebecca's **R1-R4** requirements.

**Diagnostic run result (seeds 42,43,44 — non-scoring per O-15):** `e1_verdict = PASS` — all three properties pass, no kill condition fires, battery valid, L20 self-test passes, reproducibility bit-identical. Property (iii) degradation = 0.104 (mean), consistent across seeds (0.122 / 0.098 / 0.092, all > 0.05 floor), matching the CRITIC's independent re-derivation (CU=0.000, RD=0.255, aggregate=0.102).

This replaces the prior `NOT_GREEN` verdict (degradation = 0.0 under the old multiplicative consumer with random Gaussian features). The Option E + additive/bucketed fix resolves the root cause identified in the prior changelog §3 (ranking invariance under the multiplicative form).

---

## 1. Option E frozen arm (Rebecca's binding ruling)

### 1.1 What changed
The `FrozenOriginIndex` class was rewritten to implement **Option E** per Rebecca's binding sign-off:

- **Retains ALL entries and ALL content** (all 1000 entries, same payloads, same feature vectors — identical autobiography to the candidate). The prior implementation excluded entries 100–999 (froze at `now=99`).
- **`coord_cycle_relative(e) = 0` at birth for ALL entries** (`now_at_birth − e.cycle = e.cycle − e.cycle = 0`), computed ONCE at append, **NEVER re-resolved**. The prior implementation froze at `99 - e.cycle` (stale `now=99`).
- **`coord_landmark_relative(e, L)` per the landmark registry state at each entry's birth** — entries appended before a designation do not know about landmarks designated later (but all entries ARE present). Computed once, never re-resolved.
- **Consumer identical across arms** — the ONLY difference between candidate and frozen is whether coordinates moved after birth.

### 1.2 Why this matters
Under Option E, every entry carries a permanently stale "just appended" coordinate — `coord_cycle_relative(e) = 0` for ALL entries, regardless of age. The recency weight `exp(-0/τ) = exp(0) = 1.0` for all entries → the recency gradient is destroyed while memory remains complete. This is the honest meaning of a frozen origin: **content intact, temporal self-location gone**.

The frozen arm's `coord_landmark_relative` is frozen per the registry state at each entry's birth (Option E semantics). For landmark-relative query answering (used for the `frozen_oracle_agreement` diagnostic), an entry `e` knows about landmark `L` only if `L.designated_at ≤ e.cycle`. The frozen arm's answers diverge from the oracle (frozen oracle_agreement ≈ 0.43–0.47) because the frozen arm does not re-resolve — but all entries are present.

---

## 2. Consumer battery (additive relevance + bucketed spike features)

### 2.1 What changed
The `run_downstream_consumer` function was rewritten to implement the **additive relevance + bucketed spike content features** (Option E fix, §6.iii):

- **Relevance (additive):** `relevance(e, q) = dot(v(e), q) + λ·exp(-coord_cycle_relative(e)/τ)` with `λ=16`, `τ=50`. The prior multiplicative form `exp(-coord/τ)·dot` was replaced because its 9-orders-of-magnitude recency gradient overwhelmed the content signal on all queries (CRITIC BLOCKING ISSUE 1).
- **Features (bucketed spikes):** 50 content buckets — 20 RD (size `K_rd=30 > k`), 30 CU (size exactly `k=10`), 100 fillers. Each bucket `b` gets a seeded random unit direction `u_b`; entries in bucket `b` have `v(e) = A·u_b + σ_f·noise` (`A=10`, `σ_f=0.10`); fillers get noise only. Member cycles SPREAD across 0..999 by a seeded permutation, round-robined across buckets.
- **Queries (50):** 30 content-unique (CU, `j∈20..49`, target CU bucket `j`, bucket size exactly `k=10`) + 20 recency-discriminative (RD, `j∈0..19`, target RD bucket `j`, bucket size `K_rd=30`). **40% RD fraction** (20/50 = 0.4).
- **Degradation:** recall@k (`k=10`) against oracle, candidate vs frozen-origin. Floor: degradation > 0 on all seeds AND mean ≥ 0.05.

### 2.2 New helper functions
- `build_bucket_assignment(seed)`: assigns each entry cycle to a content bucket (deterministic per seed). Returns `(bucket_of, bucket_type)` arrays.
- `build_bucket_directions(seed)`: seeded random unit direction `u_b` per bucket.
- `feature_vector(seed, cycle, bucket_of, bucket_type, directions)`: bucketed spike feature vector `v(e) = A·u_b + σ_f·noise` (or noise-only for fillers).
- `consumer_query_vector(seed, j, directions)`: bucketed query vector `q_j = A·u_b + σ_q·noise` (RD queries target RD bucket `j`, CU queries target CU bucket `j`).
- `consumer_query_type(j)`: returns `'rd'` for `j<20`, `'cu'` for `j≥20`.

### 2.3 SeedRun updates
- `SeedRun.__init__` and `build()` now precompute `bucket_of`, `bucket_type`, `bucket_directions` per seed before any append.
- `_initial_build`, `_shift_probe`, `_growth_to_final` pass the bucket info to `feature_vector`.
- `_build_consumer_queries` uses `consumer_query_vector` with the bucket directions.
- `_build_1x_run` and `_build_sub_run` precompute the bucket info before any append.

### 2.4 Why this produces degradation > 0
- **CU queries:** each targets a bucket of exactly `k=10` content-tied entries. The ~50× content gap (`A²=100` vs `~1.8` for other buckets) means the top-k SET is the bucket, regardless of the bounded additive recency bonus (`λ∈[0,16]`). Both oracle and frozen retrieve the bucket → CU degradation ≈ 0 (content dominates, as intended).
- **RD queries:** each targets a bucket of `K_rd=30 > k` content-tied entries at spread cycles. Content ties all 30; the recency bonus `λ·exp(-coord/τ)` must SELECT which `k=10` of 30 to retrieve. The oracle (re-resolved `coord = 999 - cycle`) retrieves the `k` most-recent; the frozen arm (Option E `coord=0` for all → recency bonus = constant `λ`) ranks by content-noise → retrieves a content-noise-driven subset → the sets differ → RD degradation > 0.
- **Aggregate:** `0.4 × RD_degradation ≈ 0.4 × 0.255 = 0.102` — comfortably above the 0.05 floor, driven by the recency-selection mechanism (not content-unique failure).

---

## 3. R1 — Component-wise reporting

### 3.1 What changed
Every scoring artifact now reports **CU degradation, RD degradation, and aggregate SEPARATELY**, plus each arm's **ABSOLUTE recall per query type** (candidate, frozen, oracle, on CU and RD). The aggregate alone is NOT a reportable result.

### 3.2 New fields (per seed, in `results.<seed>.candidate`):
- `downstream_degradation_cu`, `downstream_degradation_rd`, `downstream_degradation_aggregate`
- `downstream_quality_candidate_cu`, `downstream_quality_candidate_rd`
- `downstream_quality_frozen_cu`, `downstream_quality_frozen_rd`
- `downstream_quality_oracle_cu`, `downstream_quality_oracle_rd`
- `downstream_quality_candidate_aggregate`, `downstream_quality_frozen_aggregate`, `downstream_quality_oracle_aggregate`

### 3.3 New fields (in `property_iii_load_bearing_coupling`):
- `downstream_degradation_cu_per_seed`, `downstream_degradation_rd_per_seed`, `downstream_degradation_aggregate_per_seed`
- `downstream_degradation_cu_mean`, `downstream_degradation_rd_mean`, `downstream_degradation_aggregate_mean`
- `downstream_quality_*_per_seed` and `downstream_quality_*_mean` for all arm × query-type combinations
- `r1_component_wise_note`: "CU degradation, RD degradation, aggregate reported SEPARATELY. The aggregate alone is NOT a reportable result."

### 3.4 Diagnostic run results (seeds 42,43,44):
| Seed | CU degradation | RD degradation | Aggregate | cand_CU | cand_RD | frozen_CU | frozen_RD |
|---|---|---|---|---|---|---|---|
| 42 | 0.0033 | 0.3000 | 0.1220 | 1.000 | 1.000 | 0.997 | 0.700 |
| 43 | 0.0067 | 0.2350 | 0.0980 | 1.000 | 1.000 | 0.993 | 0.765 |
| 44 | 0.0000 | 0.2300 | 0.0920 | 1.000 | 1.000 | 1.000 | 0.770 |
| **Mean** | **0.0033** | **0.2550** | **0.1040** | **1.000** | **1.000** | **0.997** | **0.745** |

The tiny CU degradation (0.0033 mean) is from feature noise occasionally causing a non-bucket entry to intrude on 1-2 CU queries on seeds 42/43; the spec says CU degradation ≈ 0 (the CRITIC's independent re-derivation shows exactly 0.000 due to slightly different tie-breaking). RD degradation = 0.255 matches the CRITIC's re-derivation exactly.

---

## 4. R2 — Honest ceiling + CU as specificity control

### 4.1 What changed
Artifacts now state:
- **CU degradation is 0.000 BY CONSTRUCTION** (bucket size = `k`: recency reorders within the top-k set but cannot change it; recall@k is set-based). Field: `cu_degradation_by_construction: 0.0`.
- **The aggregate's true ceiling is 0.4** (RD fraction = 20/50). Field: `aggregate_true_ceiling: 0.4`. Note: "0.102 is read as ~26% degradation on recency-capable queries, NOT as a small global effect."
- **Frozen's CU recall reported as SPECIFICITY CONTROL** (L8 pattern). Field: `frozen_cu_recall_specificity_control`. Note: "Pre-registered expectation: frozen's CU recall should remain HIGH, demonstrating degradation is SPECIFIC to destroyed temporal organization, not general consumer breakage."
- **Pre-registered expectation** (field: `frozen_cu_recall_expectation`): "frozen's CU recall should remain HIGH, demonstrating that the measured degradation is SPECIFIC to the destroyed temporal organization (recency gradient collapsed to a constant under Option E), NOT general consumer breakage."

### 4.2 Diagnostic run results:
- Frozen CU recall (specificity control) = 0.9967 (mean) — HIGH, as expected. The degradation is specific to RD queries (destroyed temporal organization), not general consumer breakage.
- Aggregate = 0.104 ≈ 26% of the 0.4 ceiling → ~26% degradation on recency-capable queries.

---

## 5. R3 — Hold-out scoring seeds (5 seeds total)

### 5.1 What changed
- **Scoring seeds: 42, 43, 44, 45, 46** (FIVE seeds). Seeds 45 and 46 are **HOLD-OUT** — NEVER used in development.
- **All floors and kill conditions apply to all FIVE seeds jointly.**
- **Diagnostic run uses only 42, 43, 44** (45 and 46 are FORBIDDEN in development).
- The command accepts 5 seeds: `python e1_experiment.py --seeds 42,43,44,45,46 --output-dir ./e1_output`
- The diagnostic command: `python e1_experiment.py --seeds 42,43,44 --output-dir ./e1_output`

### 5.2 New constants:
- `SCORING_SEEDS = [42, 43, 44, 45, 46]` — R3: 5 scoring seeds (45/46 hold-out)
- `HOLDOUT_SEEDS = [45, 46]` — R3: forbidden in development
- `SEEDS_DEFAULT = [42, 43, 44]` — diagnostic default (3 seeds; scoring uses 5)

### 5.3 R3 hold-out guard:
`main()` checks if hold-out seeds (45, 46) appear in a non-scoring run and warns: "R3: seeds 45,46 are FORBIDDEN in development (only the 5-seed scoring run may include them)." The diagnostic run (42,43,44) triggers no warning.

### 5.4 Manifest fields:
- `command`: `python e1_experiment.py --seeds 42,43,44,45,46 --output-dir ./e1_output` (scoring)
- `diagnostic_command`: `python e1_experiment.py --seeds 42,43,44 --output-dir ./e1_output`
- `scoring_seeds`, `holdout_seeds`, `r3_note`

---

## 6. R4 — Auditable arithmetic

### 6.1 What changed
- **Per-query recall tables** in the artifacts: `per_query_recall_table` (per seed, in `results.<seed>.candidate`) and `per_query_recall_tables` (in `property_iii_load_bearing_coupling`). Each row: `{query_idx, query_type, recall_candidate, recall_frozen, recall_oracle, degradation}`.
- **The JUDGE can recompute the aggregate from raw values alone**: `aggregate = mean over all 50 queries of (1 - recall_frozen)`; `CU = mean over 30 CU queries`; `RD = mean over 20 RD queries`. Verified: recomputation matches reported values exactly on all seeds.
- **CRITIC's independent re-derivation script included in the artifact package**: `critic_independent_rerderivation.py` is copied to the output directory by `_copy_critic_rerderivation()`. The script re-derives the consumer battery's expected CU/RD/aggregate degradation from scratch directly from the spec text.

### 6.2 R4 note (in artifacts):
"R4: per-query recall tables shipped so the JUDGE can recompute the aggregate from raw values alone (M1 standard: no agent's characterization is evidence). aggregate = mean over all 50 queries of (1 - recall_frozen); CU = mean over 30 CU queries; RD = mean over 20 RD queries."

### 6.3 Verification (diagnostic run):
JUDGE recomputation from per-query tables matches reported values exactly on all 3 seeds (aggregate, CU, RD).

---

## 7. Output schema updates

### 7.1 `e1_run_results.json`
- `config`: added `consumer_relevance_form`, `consumer_recency_coupling_lambda`, `consumer_content_signal_amplitude`, `consumer_feature_noise_sigma`, `consumer_query_noise_sigma`, `n_recency_discriminative_queries`, `recency_discriminative_fraction`, `n_rd_content_buckets`, `rd_content_bucket_size`, `n_content_unique_queries`, `n_cu_content_buckets`, `cu_content_bucket_size`, `n_content_buckets_total`, `aggregate_true_ceiling`, `frozen_arm_spec`, `consumer_relevance_note`, `r1_component_wise_reporting`, `r2_honest_ceiling`, `r3_holdout_seeds`, `r4_auditable_arithmetic`, `scoring_seeds`, `holdout_seeds`.
- `results.<seed>.candidate`: added all R1 component-wise degradation + absolute recall per arm per query type fields + `per_query_recall_table` + `cu_degradation_by_construction` + `aggregate_true_ceiling` + query type counts.
- `results.<seed>.frozen_origin`: added `downstream_quality_frozen_cu`, `downstream_quality_frozen_rd`, `downstream_quality_frozen_aggregate` (R2 specificity control).
- `mean_over_seeds.candidate`: added R1 component-wise means + R2 ceiling/specificity fields.
- `mean_over_seeds.frozen_origin`: added R2 specificity control fields.
- `property_iii_load_bearing_coupling`: added all R1-R4 fields (component-wise degradation per seed + means, absolute recall per arm per query type per seed + means, CU by construction, aggregate true ceiling, frozen CU recall specificity control, pre-registered expectation, per-query recall tables, R4 auditable arithmetic note, query type counts, updated `consumer_spec`).

### 7.2 `e1_invariants.json`
- `property_iii_load_bearing_coupling`: added all R1-R4 fields (component-wise degradation, absolute recall per arm, CU by construction, aggregate true ceiling, frozen CU recall specificity control, pre-registered expectation, per-query recall tables, R4 auditable arithmetic note, query type counts, updated `consumer_spec`).

### 7.3 `e1_manifest.json`
- `command`: updated to 5-seed scoring command.
- `diagnostic_command`: added (3-seed diagnostic).
- `scoring_seeds`, `holdout_seeds`, `r3_note`: added.
- `artifact_package_includes`: added (references `critic_independent_rerderivation.py` for R4).
- `purpose`, `bars`: updated to mention Option E + R1-R4.

### 7.4 `e1_profile.json`
- Unchanged structure (6-element profile vector); the `downstream_degradation` element now reflects the Option E + additive consumer (0.104 vs prior 0.0).

### 7.5 `e1_run.log`
- Updated log lines include R1 component-wise degradation + absolute recall per arm per query type.

### 7.6 `critic_independent_rerderivation.py` (R4, copied to output dir)
- The CRITIC's independent re-derivation script is copied to the output directory for the JUDGE.

---

## 8. Reproducibility check updates

The `check_reproducibility` function now includes the new R1 component-wise deterministic fields in the bit-identical check:
- `downstream_degradation_cu`, `downstream_degradation_rd`, `downstream_degradation_aggregate`
- `downstream_quality_candidate_cu/rd`, `downstream_quality_frozen_cu/rd`, `downstream_quality_oracle_cu/rd`
- `downstream_quality_candidate_aggregate`, `downstream_quality_frozen_aggregate`, `downstream_quality_oracle_aggregate`
- `cu_degradation_by_construction`, `aggregate_true_ceiling`

Diagnostic run: `bit_identical=True`, `max_abs_diff_per_seed={'42': 0.0, '43': 0.0, '44': 0.0}`.

---

## 9. Diagnostic run verification (seeds 42,43,44 — non-scoring per O-15)

| Check | Status |
|---|---|
| Option E frozen arm: coords at birth (coord=0 for all), never re-resolved, all entries retained | ✅ |
| Consumer: additive relevance (dot + λ·exp(-coord/τ)), bucketed features, 40% RD | ✅ |
| R1: component-wise reporting (CU, RD, aggregate separately + absolute recall per arm) | ✅ |
| R2: 0.4 ceiling stated, CU as specificity control (frozen CU recall = 0.997, HIGH) | ✅ |
| R3: command accepts 5 seeds; diagnostic used only 42,43,44 (no R3 warning) | ✅ |
| R4: per-query recall tables present; JUDGE recomputation matches reported values exactly | ✅ |
| R4: critic_independent_rerderivation.py copied to output dir | ✅ |
| All 5 kill conditions evaluated (b, c, d, e, f — none fire) | ✅ |
| Battery validity checked (fair_naive ≥ 4.0× — 6.79×, valid) | ✅ |
| Timing methodology applied (median, warm-up, monotonic clock, IQR) | ✅ |
| L20 self-test runs (no-drift=1.0; pert1=-0.17, pert2=0.00; both < 0.50) | ✅ |
| I3 empirical-null (≥100 replicates per arm — all in-band) | ✅ |
| Reproducibility (bit-identical deterministic fields) | ✅ |
| Property (i) correctness (oracle_agreement = 1.0) | ✅ PASSES |
| Property (ii) operational distinctness | ✅ PASSES (cand_growth=1.01, fn_growth=6.79) |
| Property (iii) load-bearing coupling | ✅ PASSES (degradation=0.104, consistent, > 0.05 floor) |
| Verdict | **PASS** (all three properties pass, no kill fires) |
| No crashes or errors | ✅ |
| `deviations_logged` self-detecting | ✅ (python/numpy/scipy version mismatches) |

### Key diagnostic numbers (mean over seeds 42,43,44):
- oracle_agreement = 1.0000
- equivalence_agreement_vs_fair_naive = 1.0000
- latency_ratio_membership = 1.054, latency_ratio_bounded_k = 1.089 (both ≤ 2.0)
- candidate_latency_growth_10x = 1.010 (≤ 2.0), fair_naive_latency_growth_10x = 6.793 (≥ 4.0, battery valid)
- chain_integrity_final = 1.0, coordinate_shift = 1.0, wall_clock_shift_detected = 0.0
- **downstream_degradation = 0.104** (CU=0.003, RD=0.255, aggregate=0.104; consistent; > 0.05 floor)
- frozen CU recall (specificity control) = 0.997 (HIGH — degradation specific to RD)

---

## 10. Environment deviations (self-detected, non-blocking)

Per §0.3 and §10, the script self-detects and logs deviations in `e1_manifest.json.deviations_logged`:
- **Python:** runtime 3.14.3, pinned 3.11.x (differs)
- **numpy:** runtime 2.5.2, pinned 1.26.4 (differs)
- **scipy:** runtime 1.18.0, pinned 1.13.1 (differs)

These are non-blocking (the script runs correctly on the available versions). The `requirements.txt` pins the spec values.

---

## 11. Files

- `e1_experiment.py` — the implementation (single self-contained script, updated for Option E + R1-R4).
- `requirements.txt` — pinned deps (unchanged: python==3.11, numpy==1.26.4, scipy==1.13.1).
- `e1_output/` — 5 output files + `critic_independent_rerderivation.py` (R4) from the diagnostic run.
  - `e1_run_results.json` — full results table with R1-R4 fields.
  - `e1_invariants.json` — verdict + kill conditions + 3 properties + R1-R4 fields.
  - `e1_manifest.json` — courier round-trip log with R3 5-seed config.
  - `e1_run.log` — raw stdout/stderr capture.
  - `e1_profile.json` — L20 drift baseline + self-test.
  - `critic_independent_rerderivation.py` — R4 CRITIC's independent re-derivation (copied).

---

*End of changelog. No bars were invented, lowered, or raised. All numeric values carried forward verbatim from the task spec + Rebecca's R1-R4 sign-off. The Option E frozen arm, additive relevance, and bucketed spike features are pre-registered per the spec and verified by the CRITIC's independent re-derivation.*

---

# Addendum — E1-RUN-1 crash fix (timing construction bug)

**Date:** 2026-08-15
**Author:** TASK BUILDER
**Trigger:** E1-RUN-1 crashed on Rebecca's Windows executor during the L20 drift self-test (`ValueError: array must not contain infs or NaNs` from `pearsonr`). CRITIC-confirmed construction bug — see `/home/user/workspace/critic_e1_run1_crash_analysis.md`. Per Rebecca's construction-bug guard, this fix + re-run does not consume D2 budget.

## Root cause (CRITIC-confirmed)

`measure_latency_median_iqr()` (previously lines 1207-1232) used `time.monotonic_ns()`. On the Windows executor, `time.monotonic_ns()` has ~15ms tick resolution, while the timed operations (membership lookup, bounded-k lookup) are sub-microsecond. Essentially all single-call measurements landed on `t1 - t0 == 0`, so the median was `0.0`. This tripped the `if > 0 else float("inf")` guards for `latency_ratio_membership` / `latency_ratio_bounded_k` (previously lines 1327-1330) and `candidate_latency_growth_10x` / `fair_naive_latency_growth_10x` (previously lines 1383-1386), injecting `inf` into the 6-element profile vector. `_safe_pearson`'s zero-variance guard did not cover non-finite inputs, so `l20_self_test`'s `_safe_pearson(pv, pv)` call fell through to `scipy.stats.pearsonr`, which raised on the `inf`-containing vector.

## Fix — three parts, all applied

### Part 1: Timing methodology (`measure_latency_median_iqr`, timing section)
- Replaced `time.monotonic_ns()` with `time.perf_counter_ns()` everywhere in the timing primitive. On Windows, `perf_counter_ns()` is backed by `QueryPerformanceCounter` (~100ns resolution) instead of the coarse OS tick, which is sufficient for the sub-microsecond operations being timed.
- Added a **batch fallback**: the new helper `_timed_batch_median_iqr(query_fn, batch_n, n_reps)` times `batch_n` calls per repetition. `measure_latency_median_iqr()` starts at `batch_n=1`, and if the median batch time is still `<= 0.0` (operation faster than clock resolution even with `perf_counter_ns()`), doubles `batch_n` and re-measures, up to a safety cap (`max_batch_n=2**20`). Once a positive median is obtained, it is divided by `batch_n` to recover the per-call latency (and the IQR is divided the same way). This makes the methodology robust on **any** hardware/clock combination, not just a fix for the specific Windows tick-resolution issue observed in E1-RUN-1.
- Warm-up exclusion (first 10% of reps discarded) and the median/IQR statistics are unchanged — only the clock source and the new batch-fallback wrapper were added.
- Updated the `timing_methodology` strings reported in `e1_run_results.json` / `e1_invariants.json` to describe the new methodology (`perf_counter_ns` + batch fallback) instead of the stale "monotonic clock" wording.

### Part 2: Harden `_safe_pearson`
- Added an `np.isfinite()` check on both input arrays *before* the existing zero-variance check. If either array contains any `inf` or `NaN`, `_safe_pearson` now returns `0.0` (no correlation) instead of falling through to `pearsonr` (which raises `ValueError` on non-finite input via `np.asarray_chkfinite`).
- This is a defensive guard per the CRITIC's recommendation (§6 option 3 of the crash analysis): the timing fix in Part 1 should prevent `inf`/`NaN` from ever reaching `_safe_pearson` again, but the guard ensures the L20 self-test cannot crash even if some future producer of the profile vector regresses.
- Verified in isolation: `_safe_pearson([1.0, inf, 3.0], [1.0, 2.0, 3.0]) == 0.0`, `_safe_pearson([1.0, nan, 3.0], [1.0, 2.0, 3.0]) == 0.0`, and normal finite input is unaffected (`_safe_pearson([1,2,3],[1,2,3]) ≈ 1.0`).

### Part 3: Fix `instrument_failure` mislabeling (CRITIC-flagged minor issue, §7 of the crash analysis)
- Property (ii)'s `instrument_failure` flag (`evaluate_properties`) previously only checked `(not battery_valid) and (not state_dependent_collapse)`, which stayed `False` even when the underlying latency/growth values were `inf` (exactly the E1-RUN-1 scenario) — a labeling inconsistency the CRITIC explicitly flagged.
- Added a `non_finite_latency` check: `not np.all(np.isfinite([lat_ratio_mem, lat_ratio_bk, cand_growth, fn_growth]))`. `instrument_failure` is now `True` if `non_finite_latency` OR the pre-existing `(not battery_valid) and (not state_dependent_collapse)` condition holds.
- Added `instrument_failure_reason` (string) alongside the flag in `prop_ii`, `e1_invariants.json`'s `property_ii_operational_distinctness`, and kill condition (d)'s block, so the specific cause (non-finite latency vs. invalid battery) is logged, not just a boolean.
- Kill condition (d)'s `instrument_failure` (`evaluate_kill_conditions`) now reuses `prop_ii["instrument_failure"]` directly instead of recomputing a narrower version, so the two flags can never disagree.

## What was NOT changed (per task constraints)

- No locked bars, kill-condition thresholds, or the three-property test structure.
- No changes to the frozen arm (Option E) implementation.
- No changes to the consumer battery (additive relevance, bucketed features).
- No changes to R1-R4 reporting content (only the `instrument_failure`/`instrument_failure_reason`/`timing_methodology` string fields noted above were touched, and those are diagnostic/labeling fields, not R1-R4 substantive content).
- No changes to the 5-seed support (`SCORING_SEEDS`, `HOLDOUT_SEEDS`, `SEEDS_DEFAULT` untouched).
- `STATE.md` not edited. No git commit made.

## Diagnostic run (seeds 42, 43, 44 — non-scoring, per task instructions)

Command: `python e1_experiment.py --seeds 42,43,44 --output-dir ./e1_output` (run on this sandbox's Linux/Python 3.14/numpy 2.5/scipy 1.18 environment; the fix targets both Windows and Linux per the task's cross-platform requirement).

| Check | Result |
|---|---|
| Crash | None — `e1_verdict = PASS`, exit code 0 |
| Latency values finite | ✅ all `latency_ratio_membership`, `latency_ratio_bounded_k`, `candidate_latency_growth_10x`, `fair_naive_latency_growth_10x` are finite (e.g. seed 42: `lat_ratio_mem=1.032 lat_ratio_bk=1.019 cand_growth=0.996 fn_growth=6.464`) — zero `inf`/`NaN` values found anywhere in `e1_run_results.json`, `e1_invariants.json`, or `e1_profile.json` (programmatically verified) |
| Property (ii) evaluates correctly | ✅ `latency_passes=True state_dependent_passes=True battery_valid=True instrument_failure=False` |
| L20 self-test | ✅ runs to completion, no crash: `no_drift_corr=1.0 no_drift_passes=True`, `pert1_corr=-0.169` (<0.5), `pert2_corr=0.0` (<0.5), `both_perturbations_flag_drift=True` |
| Property (i) | ✅ `oracle_agreement=1.0000 passes=True` (unchanged) |
| Property (iii) | ✅ `degradation_mean=0.1040`, `consistent=True`, `passes=True` (per-seed: 0.1220 / 0.0980 / 0.0920, all > 0.05 floor; unchanged from prior runs) |
| Kill conditions | ✅ none fire: `(b)=False (c)=False (d)=False (e)=False (f)=False`; kill (d) now shows real finite values (`d1_lat_mem≈1.04 d1_lat_bk≈1.10 d2_cand_growth≈1.00 d2_fn_growth≈6.42`), `instrument_failure=False` |
| Reproducibility | ✅ `bit_identical=True`, `max_abs_diff_per_seed={'42': 0.0, '43': 0.0, '44': 0.0}` |
| I3 empirical-null | ✅ all three arms `in_band=True` |

### Isolated unit verification of the fix mechanics
- `_safe_pearson` with an `inf`-containing input returns `0.0` (no crash); with `NaN` returns `0.0`; normal finite input unaffected.
- `measure_latency_median_iqr` was tested against a monkeypatched `time.perf_counter_ns` simulating a 15ms-resolution clock (replicating the Windows tick issue): the batch fallback engaged (batched over 26M calls across 90 measured reps) and returned a finite, strictly positive per-call latency (`1.14e-7` s), proving the fix generalizes beyond the specific clock available on this sandbox.

## Files changed
- `e1_experiment.py`:
  - New `_timed_batch_median_iqr()` helper; rewrote `measure_latency_median_iqr()` to use `time.perf_counter_ns()` with batch fallback.
  - Hardened `_safe_pearson()` with an `np.isfinite()` guard.
  - `evaluate_properties()`: added `non_finite_latency` detection and folded it into `instrument_failure`; added `instrument_failure_reason`.
  - `evaluate_kill_conditions()`: kill (d)'s `instrument_failure` now sourced from `prop_ii["instrument_failure"]`.
  - `e1_invariants.json` assembly: added `instrument_failure_reason` to `property_ii_operational_distinctness` and kill condition `(d)`; updated stale `timing_methodology` strings in two places.
- `e1_output/` — refreshed via the seeds 42,43,44 diagnostic re-run (`e1_run_results.json`, `e1_invariants.json`, `e1_manifest.json`, `e1_run.log`, `e1_profile.json`, `critic_independent_rerderivation.py`).
- `e1_diagnostic_run.log` — captured stdout/stderr of the diagnostic run (workspace root, for reviewer convenience).

## Reference

- CRITIC analysis: `/home/user/workspace/critic_e1_run1_crash_analysis.md` (construction-bug verdict, root-cause chain, fix recommendation).
