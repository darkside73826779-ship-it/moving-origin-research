# CRITIC Analysis — E1-RUN-1 Crash

**Reviewer:** CRITIC
**Subject run:** E1-RUN-1 (commit `f9dc658f40291a026769474fe3dd6ff9dfc86fe6`), seeds 42,43,44,45,46
**Files reviewed:**
- `/home/user/workspace/e1_run1_return/e1_crash_stderr.txt`
- `/home/user/workspace/e1_run1_return/e1_roundtrip_log.txt`
- `/home/user/workspace/e1_run1_return/e1_scoring_output/e1_run.log`
- `/home/user/workspace/e1_experiment.py` (lines 1207–1232, 1327–1330, 1383–1386, 2140–2222)

---

## 1. Is the diagnosis correct?

**Yes, confirmed line-for-line against the code.** The causal chain is:

1. **Timing primitive (`e1_experiment.py:1207-1232`, `measure_latency_median_iqr`)** uses `time.monotonic_ns()` to bracket a single call to the query function (membership lookup or bounded-k lookup), over 100 repetitions with the first 10% discarded as warm-up, then reports the median. This is exactly as documented (NB-6 methodology comment at line 1205).

2. On the executor's Windows machine (confirmed by `C:\Users\darks\...` paths in `e1_crash_stderr.txt` and `e1_roundtrip_log.txt`), `time.monotonic_ns()` is backed by `GetTickCount64`/`QueryPerformanceCounter`-independent OS tick, which historically has ~15.6ms granularity unless the process raises the system timer resolution. The operations being timed — `query_membership` (`e1_experiment.py:1199-1200`) and `query_landmark_relative_bounded` (`e1_experiment.py:1196-1197`) — are O(1)/O(log n) set/dict lookups on a small index, almost certainly sub-microsecond. With a 15ms clock granularity, the overwhelming majority of the 90 non-warm-up single-call measurements land on `t1 - t0 == 0`, so `np.median(arr) == 0.0`.

3. This directly produces the observed **`lat_ratio_mem=inf lat_ratio_bk=inf`** for every seed: at `e1_experiment.py:1327-1330`, `latency_ratio_membership = latency_10x/latency_1x if latency_1x > 0 else inf`, and since `latency_1x_membership` (and likely `latency_10x_membership`) are `0.0`, the guard falls to `float("inf")`. Same mechanism for `lat_ratio_bk`.

4. The **`cand_growth=inf fn_growth=inf`** values come from the analogous guard at `e1_experiment.py:1383-1386`: `candidate_scaling_curve[-1] / candidate_scaling_curve[0] if candidate_scaling_curve[0] > 0 else inf`. The state-dependent scaling battery (`_measure_state_dependent_candidate`, line 1590+) uses the same `measure_latency_median_iqr` primitive, so its first scaling-curve point is also `0.0`, triggering the same `inf` fallback.

5. These `inf` values flow into the 6-element profile vector at `build_profile_vector()` (`e1_experiment.py:2210-2222`): element 1 is `latency_ratio_membership` and element 2 is `candidate_latency_growth_10x` — both `inf` for every seed, hence `inf` in the seed-mean and in `pv`.

6. In `l20_self_test` (`e1_experiment.py:2179-2207`), `pv` (containing `inf`s) is passed to `_safe_pearson(pv, pv)` (line 2189). `_safe_pearson` (`e1_experiment.py:2166-2176`) guards only against **zero variance** (`np.std(a) == 0.0`), not against non-finite values. `np.std()` on an array containing `inf` returns `nan` (visible in the stderr `RuntimeWarning: invalid value encountered in subtract` from `numpy/core/_methods.py` and `scipy/stats/_stats_py.py`), and `nan == 0.0` is `False` in Python/NumPy, so the guard does **not** trip and execution falls through to `pearsonr(a, b)` → `scipy.linalg.norm` → `np.asarray_chkfinite` → `ValueError: array must not contain infs or NaNs`. This matches the traceback exactly (`e1_crash_stderr.txt` lines 7–28).

Every link in this chain is verifiable directly in the source and the log. **The diagnosis is correct.**

---

## 2. Root cause classification

**Root cause: clock-resolution/timing-methodology defect, not an algorithmic or correctness defect in the candidate index.** The measured *operations themselves* are not misbehaving — `query_membership` and `query_landmark_relative_bounded` return correct answers (Property (i) oracle_agreement = 1.0 confirms this independently). The defect is purely in the **instrument**: `measure_latency_median_iqr()` assumes `time.monotonic_ns()` has resolution well below the duration of the operation being timed, which is false on this Windows executor for these particular operations. Two secondary, compounding code defects also surface:

- `_safe_pearson`'s zero-variance guard doesn't cover the non-finite case, so a defensive function that was specifically hardened against one edge case (constant-vector correlation, "NEW-1 fix") is not hardened against a different, related edge case (non-finite input). This is what actually turns a benign-looking `inf` in one column into a hard crash in an unrelated self-test.
- The ratio/growth guards (`> 0 else inf`) treat "zero" as an error signal conflated with "unmeasurably fast," when a genuine zero-latency floor and a clock-resolution artifact are indistinguishable under the current instrumentation.

This is a **specific, narrow, and mechanically-identified defect** — not a design-level flaw in the experiment, not a data/seed issue, and not an environment failure outside the code's control (the code should tolerate its own execution environment).

---

## 3. Are ALL latency values `inf`?

**Confirmed yes.** Every one of the 10 seed-lines in `e1_run.log` (5 seeds × 2 runs for reproducibility check) shows:
```
lat_ratio_mem=inf lat_ratio_bk=inf cand_growth=inf fn_growth=inf
```
with no exceptions across seeds 42, 43, 44, 45, 46, in both run 1 and run 2 (reproducibility re-run). This is also reflected in `[kill d] fires=True d1_lat_mem=inf d1_lat_bk=inf d2_cand_growth=inf d2_fn_growth=inf instrument_failure=False` (line 87) — the kill-condition evaluator saw the same `inf`s and (correctly, given the guard logic) flagged kill condition (d) as firing, though it did **not** set `instrument_failure=True`, which is itself worth flagging (see §4) since this is precisely an instrument-failure scenario, not a genuine candidate-dead signal.

---

## 4. Are the non-latency results valid?

**Yes — validated independently of the timing subsystem.**

- **Property (i) oracle_agreement = 1.0000** on all 5 seeds (`e1_run.log` lines 14, 21, 28, 35, 42, and confirmed at aggregate level line 81: `[property i] oracle_agreement=1.0000 passes=True`). This property depends only on set-equality of query answers vs. the oracle — it does not touch `time.monotonic_ns()` at all.
- **Property (iii) degradation**: all 5 seeds > 0.05 (0.1220, 0.0980, 0.0920, 0.1200, 0.1060), aggregate `degradation_mean=0.1076 consistent=True passes=True` (line 83). This property is computed by `run_downstream_consumer()`, which is a quality/degradation computation independent of latency timing.
- **Kill conditions (b), (c), (e), (f)** all `fires=False` (lines 85, 86, 88, 89) — none of these depend on the timing subsystem.
- **Kill condition (d)** does fire, but only because it directly inspects the `inf` latency/growth values — this is the same instrument artifact, not new information.
- **Reproducibility**: `bit_identical=True max_abs_diff_per_seed={'42': 0.0, '43': 0.0, '44': 0.0, '45': 0.0, '46': 0.0}` (line 79) across the two full re-runs — every deterministic metric (including, notably, the `inf` latency ratios themselves, which reproduced identically) is bit-for-bit stable.
- **I3 empirical-null self-consistency**: all three arms (`shuffled_cadence`, `empty`, `wall_clock_injection`) report `in_band=True` (line 95), completed successfully before the crash.

The crash occurred only in the **L20 drift self-test**, which is the last stage of the pipeline (line 96, `[L20] running drift self-test...`, immediately followed by the traceback). Everything upstream of L20 — build, chain integrity, all 5 seeds' full query batteries, all three properties, all 5 kill conditions, reproducibility check, and I3 — completed successfully and produced internally consistent output.

---

## 5. Hold-out seeds 45/46 vs. development seeds 42/43/44

| Seed | Role | oracle_agreement | degradation | CU_deg | RD_deg | frozen_cu | frozen_rd |
|------|------|------|------|------|------|------|------|
| 42 | dev | 1.0 | 0.1220 | 0.0033 | 0.3000 | 0.997 | 0.700 |
| 43 | dev | 1.0 | 0.0980 | 0.0067 | 0.2350 | 0.993 | 0.765 |
| 44 | dev | 1.0 | 0.0920 | 0.0000 | 0.2300 | 1.000 | 0.770 |
| 45 | hold-out | 1.0 | 0.1200 | 0.0000 | 0.3000 | 1.000 | 0.700 |
| 46 | hold-out | 1.0 | 0.1060 | 0.0033 | 0.2600 | 0.997 | 0.740 |

**Consistent — no distributional break.** The hold-out seeds fall squarely inside the range spanned by the development seeds:
- Degradation: dev range [0.0920, 0.1220], hold-out range [0.1060, 0.1200] — hold-out values sit inside the dev interior, not at or beyond either extreme.
- Mean across all 5 = 0.1076, which matches the logged `degradation_mean=0.1076` exactly (verified by direct computation).
- `oracle_agreement` is 1.0 uniformly across all 5 seeds — no degradation of correctness on unseen seeds.
- `frozen_cu`/`frozen_rd` for the hold-out seeds (1.000/0.700 and 0.997/0.740) are within the same band as dev seeds (0.993–1.000 / 0.700–0.770).

This indicates the candidate's behavior generalizes cleanly to seeds not used during development — there is no sign of overfitting to seeds 42-44, and the crash is unrelated to seed selection.

---

## 6. Is the fix straightforward?

**Yes.** This is a narrow, well-understood instrumentation bug with a small blast radius (confined to `measure_latency_median_iqr` and, defensively, `_safe_pearson`). Recommended fix, in order of preference:

1. **Primary fix — switch to `time.perf_counter_ns()`.** `time.perf_counter_ns()` is explicitly designed for benchmarking short durations and uses the highest-resolution timer available on the platform (on Windows, backed by `QueryPerformanceCounter`, sub-microsecond resolution), unlike `time.monotonic_ns()`, whose resolution is platform- and implementation-dependent and can be as coarse as the system tick on Windows. This is a one-line change at `e1_experiment.py:1219` and `:1221` (`t0 = time.perf_counter_ns()`, `t1 = time.perf_counter_ns()`) and preserves monotonicity (perf_counter is also monotonic) and the rest of the methodology (median, warm-up exclusion, IQR) unchanged.
2. **Secondary, complementary fix — batch calls per measurement.** For genuinely sub-nanosecond-timer-resolution operations, wrap `query_fn()` in an inner loop of, e.g., 100–1000 calls per timed interval and divide by the batch size. This provides headroom against any timer, not just the current Windows tick issue, and is good practice regardless of which clock is used.
3. **Defensive fix — harden `_safe_pearson` against non-finite input.** Independently of the timing fix, `_safe_pearson` (`e1_experiment.py:2166-2176`) should check `np.all(np.isfinite(a)) and np.all(np.isfinite(b))` before calling `pearsonr`, returning a sentinel (e.g., `0.0` or `nan` with an explicit flag) rather than crashing. This is good defensive practice on a shared self-test utility even after the timing fix, since ratio/growth guards elsewhere in the file (lines 1327-1330, 1383-1386) are designed to *produce* `inf` under a documented "cannot measure" condition — the self-test should not assume every producer of the profile vector guarantees finiteness.

Options 1+3 together fully resolve the crash and are low-risk, localized changes that do not touch the correctness-critical index logic (chain integrity, query answering, property (i)/(iii) computation) at all.

---

## 7. Does the crash affect the validity of the non-latency results?

**No.** As detailed in §4, Property (i) (oracle agreement) and Property (iii) (downstream degradation) completed successfully on all 5 seeds, with internally consistent, reproducible (bit-identical across two independent re-runs) values, and the I3 empirical-null self-consistency check also completed and passed for all three contamination arms. The crash is isolated to the L20 drift self-test, which runs *after* all substantive scientific measurements were already computed and logged. Property (ii) (latency/state-dependent scaling) is the only property genuinely compromised — it explicitly reports `latency_passes=False state_dependent_passes=False instrument_failure=False` (line 82) — and that failure is exactly the same instrumentation artifact under discussion, not a new independent problem.

One note for the record: line 82 reports `instrument_failure=False` for property (ii) despite the values being uninterpretable `inf`s caused by a clock-resolution artifact. Given this analysis, that flag arguably *should* have read `True` — this is worth flagging to Rebecca as a related (but non-blocking) labeling inconsistency to fix alongside the main defect, since "instrument failure" is precisely what occurred.

---

## 8. Is this a D2 retry situation under Rebecca's construction-bug guard?

**Yes — this satisfies all three conditions of the construction-bug guard:**

1. **Specific defect identified**: `measure_latency_median_iqr()` (`e1_experiment.py:1207-1232`) uses `time.monotonic_ns()`, whose resolution on the Windows executor is too coarse (~15ms) relative to the sub-microsecond operations being timed, producing systematic `0.0` medians that cascade through documented `if > 0 else inf` guards (lines 1327-1330, 1383-1386) into the profile vector, and `_safe_pearson`'s zero-variance guard (lines 2171-2172) does not cover the non-finite case that results, causing `pearsonr` → `asarray_chkfinite` to raise.
2. **Fix is clear and localized**: switch `time.monotonic_ns()` to `time.perf_counter_ns()` in `measure_latency_median_iqr` (plus optionally a batching safety net), and add a finiteness check to `_safe_pearson`. Both are small, mechanical, low-risk changes confined to the timing/self-test utilities — no changes needed to the candidate index, oracle, or scoring logic.
3. **CRITIC-confirmed before re-run**: this document constitutes that confirmation — the diagnosis has been independently traced through the source code and cross-checked against the log and stderr output line-by-line, with no gaps or alternative explanations found.

Since all three conditions of the construction-bug guard are met, this failure **escapes the D2 budget** per Rebecca's stated policy, and a fixed re-run should proceed without counting against D2.

---

## Verdict

# CONSTRUCTION BUG CONFIRMED

**Root cause:** `measure_latency_median_iqr()` (`e1_experiment.py:1207-1232`) times sub-microsecond query operations using `time.monotonic_ns()`, whose resolution on the Windows executor is too coarse to resolve these durations, yielding `0.0` medians for essentially all measurements. This trips the `if > 0 else float("inf")` guards for `latency_ratio_membership`/`latency_ratio_bounded_k` (lines 1327-1330) and `candidate_latency_growth_10x`/`fair_naive_latency_growth_10x` (lines 1383-1386) on every seed, injecting `inf` into the 6-element profile vector (`build_profile_vector`, lines 2210-2222). `_safe_pearson`'s zero-variance guard (lines 2166-2176) does not cover non-finite inputs, so `l20_self_test`'s `no_drift = _safe_pearson(pv, pv)` call (line 2189) falls through to `scipy.stats.pearsonr`, which raises `ValueError: array must not contain infs or NaNs` via `np.asarray_chkfinite`.

**Fix:** (1) Replace `time.monotonic_ns()` with `time.perf_counter_ns()` in `measure_latency_median_iqr`, and/or add call-batching so each timed interval exceeds clock resolution; (2) harden `_safe_pearson` to check `np.isfinite` before calling `pearsonr`. Both changes are small, localized, and do not touch correctness-critical index/oracle/scoring logic.

**Impact on existing results:** None of the completed measurements are invalidated. Property (i) (oracle_agreement=1.0, all 5 seeds), Property (iii) (degradation mean=0.1076, all 5 seeds passing, consistent across dev and hold-out seeds), reproducibility (bit-identical across two full re-runs), and I3 empirical-null self-consistency (all three arms in-band) are all valid and unaffected. Only Property (ii) (latency/scaling) and the downstream L20 self-test are compromised, both by the same single root cause.

**Hold-out generalization:** Seeds 45/46 produce oracle_agreement=1.0 and degradation values (0.1200, 0.1060) squarely within the range set by development seeds 42-44 (0.0920–0.1220), with no evidence of overfitting or distributional break.

**Recommendation:** Apply the two-part fix above, re-run E1-RUN-1 under the D2 construction-bug exception (does not consume D2 budget), and additionally correct the `instrument_failure=False` mislabeling on Property (ii) noted in §7 while making the fix.
