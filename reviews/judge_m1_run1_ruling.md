# JUDGE Ruling — M1 RUN-1

**Judge:** JUDGE subagent
**Run scored:** M1 RUN-1 (run_id `m1-20260815T194311Z`)
**Scored from:** Raw artifacts returned by Rebecca at `/home/user/workspace/run1_returned/` ONLY.
**Date:** Saturday, 2026-08-15 (15:47 EDT)

> Scoring is performed exclusively from the raw artifacts. No agent's characterization of the run was used as evidence. All values cited below were re-derived directly from the JSON/log artifacts and cross-checked programmatically against the raw per-seed results.

---

## (a) Invariant suite green (I1–I5 all pass) — **PASS**

Top-level `invariant_suite_green` in `m1_invariants.json` = `true`. Each invariant verified individually against the raw per-seed results in `m1_run_results.json`:

### I1 — Reproducibility — **PASS**
`m1_invariants.json` → `I1_reproducibility.per_seed_max_abs_diff` = `{"42": 0.0, "43": 0.0, "44": 0.0}`. All three seeds exactly 0.0. The run log confirms a second run ("re-running all seeds (run 2)") with identical values. **PASS.**

### I2 — Oracle ceiling — **PASS**
`I2_oracle_ceiling.per_metric` = `{auroc: 1.0, ndcg_at_k: 1.0, spearman_rho: 1.0, recall_at_k: 1.0}`, floor = 0.95. Cross-check against raw results: oracle = 1.0 on **every metric, every seed** (42/43/44), so ≥ 0.95 holds universally. **PASS.**

### I3 — Contamination floor (empirical-null method) — **PASS**
`I3_contamination_floor.passes` = `true`, `method` = `empirical_null`, `null_replicate_count` = 30 (seeds 100–129). `per_arm_per_metric_in_band` shows all 12 cells (3 arms × 4 metrics) = `true`. Cross-check recomputed each arm's 3-seed mean and confirmed it falls within the logged empirical band for every arm×metric:
- empty: auroc 0.5000∈[0.3734,0.5705], ndcg 0.4862∈[0.3459,0.5804], spearman 0.0000∈[-0.1867,0.1339], recall 0.1333∈[0.0,0.2]
- permuted: auroc 0.4634∈band, ndcg 0.5054∈band, spearman 0.0104∈band, recall 0.0833∈band
- shuffled: auroc 0.4850∈band, ndcg 0.4666∈band, spearman -0.0304∈band, recall 0.0833∈band

All contamination arms (empty, permuted, shuffled) pass all metrics via the empirical-null method. **PASS.**

### I4 — Discrimination bar (conjunctive: mean ≥ 0.30 AND every seed) — **PASS**
`I4_discrimination_bar.passes` = `true`, bar = 0.3. Per-metric margins and per-seed flags (cross-checked against raw oracle−naive per seed):

| metric | oracle_mean | naive_mean | margin | per-seed margins (42/43/44) | all ≥ 0.30? |
|---|---|---|---|---|---|
| auroc | 1.0 | 0.4922 | 0.5078 | 0.4806 / 0.5725 / 0.4703 | yes |
| ndcg_at_k | 1.0 | 0.4334 | 0.5666 | 0.5969 / 0.5610 / 0.5420 | yes |
| spearman_rho | 1.0 | -0.0530 | 1.0530 | 1.0338 / 1.1706 / 0.9546 | yes |
| recall_at_k | 1.0 | 0.1667 | 0.8333 | 0.9000 / 0.8500 / 0.7500 | yes |

`passes_per_seed` = `[true, true, true]` on every metric, and `passes` = `true` on every metric. Conjunctive requirement satisfied. **PASS.**

### I5 — Frozen ordering (with pre-registered fallback for recall_at_k) — **PASS**
`I5_frozen_ordering.passes` = `true`. Per-metric logged status:
- auroc: `naive<frozen<oracle` — strict on all 3 seeds (means 0.4922 < 0.7315 < 1.0). ✓
- ndcg_at_k: `naive<frozen<oracle` — strict on all 3 seeds (0.4334 < 0.7071 < 1.0). ✓
- spearman_rho: `naive<frozen<oracle` — strict on all 3 seeds (-0.0530 < 0.4259 < 1.0). ✓
- recall_at_k: `N/A (frozen<=naive on some seed; fallback: non-strict not met -> N/A logged)` — strict ordering fails on seed 44 (frozen=0.25, naive=0.25, i.e. frozen ≤ naive). The pre-registered fallback was invoked and the non-passing case explicitly logged as N/A rather than silently marked pass. The frozen arm's 3-seed mean (0.2833) still exceeds the naive mean (0.1667), so the non-strict (mean-level) condition is in fact met, even though the logged wording says "non-strict not met." (See Concern #1 below.) The invariant is marked `passes=true` with the fallback applied as pre-registered. **PASS (with fallback invoked for recall_at_k).**

**Invariant suite: I1–I5 all PASS → criterion (a) PASS.**

---

## (b) M1 discrimination bar met (oracle ≥ naive + 0.30 on every metric, 3 seeds) — **PASS**

`m1_run_results.json` → `discrimination` section. Every metric: `margin ≥ 0.30` AND `passes_per_seed = [true, true, true]` AND `passes = true`:

| metric | margin | bar | passes_per_seed | passes |
|---|---|---|---|---|
| auroc | 0.5078 | 0.3 | [T,T,T] | true |
| ndcg_at_k | 0.5666 | 0.3 | [T,T,T] | true |
| spearman_rho | 1.0530 | 0.3 | [T,T,T] | true |
| recall_at_k | 0.8333 | 0.3 | [T,T,T] | true |

Cross-checked independently: every per-seed oracle−naive margin ≥ 0.30 (minimum is auroc seed 44 = 0.4703). **PASS.**

---

## (c) STATE.md current — **operational — INTEGRATOR maintains**

This is an operational criterion, not scored from run artifacts. Noted as INTEGRATOR's responsibility. Not scored by JUDGE.

---

## Additional checks

### L20 self-test — **PASS**
`m1_profile.json` → `l20_self_test`:
- `no_drift_corr` = `1.0` ✓ (exactly 1.0)
- `perturbation_1_corr` (full_arm_block_reversal) = `-0.02176…` < 0.50 ✓
- `perturbation_2_corr` (empty_oracle_swap) = `0.16594…` < 0.50 ✓
- `both_perturbations_flag_drift` = `true` ✓

All four L20 self-test conditions met.

### Profile vector — **PASS**
`m1_profile.json` → `profile_vector` contains exactly **24 floats**. `arm_order` = `[empty, permuted, shuffled, oracle, naive, frozen]` (6 arms), `metric_order` = `[auroc, ndcg_at_k, spearman_rho, recall_at_k]` (4 metrics) → 6×4 = 24. Programmatic cross-check: the 24-vector exactly equals the flattened `profile_mean_over_seeds` in arm×metric order (no mismatch to 1e-12). Order and values correct.

### Manifest completeness — **PASS (with two non-blocking concerns)**
All required fields are present in `m1_manifest.json`:
- `command` ✓ — `python m1_harness.py --seeds 42,43,44 --output-dir ./m1_output`
- `commit_hash` ✓ — `pending — no git repo` (acceptable: no git repo present)
- `purpose` ✓
- `bar` ✓
- `seeds` ✓ — `[42, 43, 44]`
- `wall_clock_seconds` ✓ — `0.04192…` s (field is named `wall_clock_seconds`, not the task-spec's `wall_clock`; semantically equivalent and present — see Concern #2)
- `deps` ✓ — python 3.11.x (target), numpy 1.26.4, scipy 1.13.1
- `python_version_runtime` ✓ — `Python 3.12.10`
- `output_files` ✓ — all 5 files listed
- `deviations_logged` ✓ present (value `[]` — see Concern #3)

### Deviation assessment — **non-blocking**
Python 3.12.10 was used instead of the requested 3.11.x because 3.11 was not installed (`run1_deviations.txt`, `run1_roundtrip_log.txt`). Impact analysis:
- **I1** is within-run determinism (the harness re-runs the same seeds in the same process and compares). Python version does not affect I1 validity — the comparison is internal to one runtime.
- **I2/I3/I4/I5** are construction-determined (oracle/naive/frozen/contamination arm definitions and empirical-null band from the naive arm). These depend on harness logic and the pinned `numpy 1.26.4` / `scipy 1.13.1`, which are identical to the 3.11.x plan. No float-format or RNG-behavior divergence is expected at this scale between 3.11.x and 3.12.10 for these operations.
- The deviation was properly logged in `run1_deviations.txt` and the round-trip log, and `python_version_runtime` records the actual runtime.

**Conclusion: the Python 3.12.10 deviation does not invalidate any invariant.** Non-blocking.

---

## Concerns / anomalies for CRITIC review (non-blocking)

1. **I5 recall_at_k fallback wording is internally contradictory.** The logged string is `"N/A (frozen<=naive on some seed; fallback: non-strict not met -> N/A logged)"`, but the non-strict (mean-level) condition **is** met: frozen mean recall (0.2833) > naive mean recall (0.1667). The phrase "non-strict not met" appears to be a stale/templated message that does not match the actual computed means. The invariant is still correctly marked `passes=true` (the pre-registered fallback permits N/A on a per-metric basis), but the explanatory text is misleading. CRITIC should confirm the fallback semantics: is "N/A" an acceptable pass state for I5, and should the wording be corrected to reflect that the mean-level non-strict condition actually held?

2. **Manifest field naming: `wall_clock_seconds` vs task-spec `wall_clock`.** The manifest uses `wall_clock_seconds`; the task's required-field list says `wall_clock`. The value is present and unambiguous (units in the name). Likely a naming-convention mismatch, not a missing field. CRITIC should decide whether to standardize the field name.

3. **`deviations_logged` in manifest is `[]` despite a real deviation.** The Python 3.12.10 deviation is documented in `run1_deviations.txt` and `run1_roundtrip_log.txt`, but the manifest's `deviations_logged` array is empty. The deviation is recorded externally but not reflected in the manifest field whose purpose is to log deviations. CRITIC should assess whether the manifest field should have referenced the deviation file/entry (e.g., `["python_version: 3.12.10 != 3.11.x (see run1_deviations.txt)"]`).

4. **Two `low_power` bands in I3.** `ndcg_at_k` (width 0.2345) and `spearman_rho` (width 0.3206) are flagged `low_power: true` in the empirical-null bands. All arms still fall in-band, so I3 passes, but the wider/low-power bands reduce the test's sensitivity for those two metrics. Noted for transparency; not a failure.

5. **`commit_hash` = `pending — no git repo`.** Acceptable given no git repo, but means the run is not pinned to a specific code commit. CRITIC may want to confirm the harness source is otherwise integrity-anchored (e.g., by hash of the harness file).

6. **`m1_run.log` is not valid UTF-8** (1 invalid byte at index 85 — likely a Windows path separator or smart-quote in the `pending — no git repo` em-dash echoed into the log, or a `\` path). The log is still fully readable after sanitization and its contents match the JSON artifacts. Non-blocking, but the harness should write UTF-8 logs.

---

## Overall verdict

# **M1 DELIVERED GREEN**

All three delivery criteria scored from artifacts hold:
- **(a) Invariant suite green:** I1, I2, I3, I4, I5 all PASS (I5 with pre-registered fallback invoked for recall_at_k). `invariant_suite_green = true`.
- **(b) M1 discrimination bar met:** oracle − naive ≥ 0.30 on every metric, every seed (minimum per-seed margin 0.4703 on auroc seed 44; all `passes_per_seed = [T,T,T]`).
- **(c) STATE.md current:** operational — INTEGRATOR maintains (not scored from artifacts).

Additional checks: L20 self-test PASS, profile vector (24 floats, correct arm×metric order) PASS, manifest complete PASS, Python 3.12.10 deviation non-blocking and properly logged externally.

**M1 RUN-1 is DELIVERED GREEN.**

Six non-blocking concerns (I5 fallback wording, manifest field naming, empty `deviations_logged`, two low-power I3 bands, missing commit hash, non-UTF-8 run log) are flagged above for CRITIC review.
