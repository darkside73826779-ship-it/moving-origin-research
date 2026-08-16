# CRITIC Review — E1-RUN-2 Results

**Reviewer role:** CRITIC (results review, not implementation review)
**Artifacts reviewed:**
- `/home/user/workspace/e1_run2_return/e1_scoring_output/e1_run.log`
- `/home/user/workspace/e1_run2_return/e1_scoring_output/e1_invariants.json`
- `/home/user/workspace/e1_run2_return/e1_scoring_output/e1_run_results.json`
- `/home/user/workspace/e1_run2_return/e1_scoring_output/e1_manifest.json`
- `/home/user/workspace/e1_run2_return/e1_scoring_output/e1_profile.json`
- `/home/user/workspace/e1_run2_return/e1_run_2_roundtrip_log.txt`
- `/home/user/workspace/e1_run2_return/e1_scoring_output/critic_independent_rerderivation.py` (executed independently)

## VERDICT: **ISSUES FOUND (non-blocking)**

The run's own reported verdict, `e1_verdict = PASS`, is **substantively correct** — no kill condition fires, oracle_agreement is 1.0 on all seeds, the R4 arithmetic is fully auditable and verified independently, and the hold-out seeds are consistent with development seeds. However, several data-hygiene and self-consistency issues were found that a careful review should surface even though none of them flip the verdict.

---

## 1. Data integrity

- **All 5 seeds present:** Confirmed. Seeds 42, 43, 44, 45, 46 all appear in `e1_run_results.json` → `results`, `e1_invariants.json` per-seed dicts, and both run-1 and run-2 passes of `e1_run.log`.
- **NaN/inf scan:** A full recursive scan of every float value in both `e1_run_results.json` and `e1_invariants.json` found **zero NaN/inf values**. This confirms the E1-RUN-1 crash cause (non-finite latency) does not recur.
- **bit_identical = True:** Confirmed in `e1_run_results.json.reproducibility` and `e1_invariants.json.reproducibility`, with `max_abs_diff_per_seed = 0.0` for all 5 seeds.
  - **⚠️ ISSUE:** This claim is true for the *scored* metrics (oracle_agreement, degradation, chain integrity, etc.) but is **not** true for the raw timing diagnostics. Comparing run-1 vs run-2 lines in `e1_run.log`, `fair_naive_latency_growth_10x` differs between the two passes for 3 of 5 seeds:
    - seed 42: 6.813 (run1) vs 6.750 (run2)
    - seed 44: 6.750 (run1) vs 7.200 (run2)
    - seed 46: 7.133 (run1) vs 6.968 (run2)
    - (seeds 43, 45 matched exactly across runs)
  - This is expected and benign — wall-clock timing is inherently non-deterministic at nanosecond/microsecond resolution, and the JSON explicitly labels these fields as "REPORTED diagnostic ONLY; never a trigger." But the artifact package should be explicit that `bit_identical` is scoped to the *non-timing* scored fields, since a naive reader comparing the two `e1_run.log` blocks by eye will see it is **not** bit-identical for timing fields. Recommend the JUDGE confirm this scoping is intentional and documented, not an oversight.

## 2. Property (i) — Correctness

- `oracle_agreement = 1.0000` confirmed on all 5 seeds in the log (both run-1 and run-2 passes) and in `e1_invariants.json.property_i_correctness` (`"oracle_agreement": 1.0, "passes": true`).
- Kill (f) — the primary correctness kill — is confirmed `fires: false`, and is marked `"signed": true` (signed by Rebecca per ruling section 4 item 3).
- **No issues found here.**

## 3. Property (ii) — Operational distinctness

- **Latency values are finite** on all seeds — confirmed via full NaN/inf scan (see §1). This resolves the E1-RUN-1 crash cause.
- `candidate_latency_growth_10x = 1.0` on all 5 seeds (≤ 2.0 bar met with large margin).
- `fair_naive_latency_growth_10x` ranges 6.6875–7.1333 across seeds (≥ 4.0 bar met with large margin); mean = 6.89.
- `battery_valid = True`, `instrument_failure = False` confirmed in both JSON artifacts and log.
- **⚠️ ISSUE — timing methodology plausibility:** The candidate's per-seed latency scaling curve is **flat and effectively zero-variance**:
  - `candidate_scaling_curve` = `[2e-07, 2e-07, 2e-07, 2e-07, 2e-07]` seconds (200 ns) at **all 5** growth points (1x through 10x data size) on **every seed**.
  - `candidate_latency_iqr_per_point` = `[0.0, 0.0, 0.0, 0.0, 0.0]` on 4 of 5 seeds (seed 43 shows one point at `1e-07`).
  - This produces `candidate_latency_growth_10x = 1.0` exactly on every seed — a suspiciously "too clean" result.
  - By contrast, `fair_naive_scaling_curve` shows genuine, monotonically increasing values (e.g., seed 42: `1.6e-06 → 3.2e-06 → 5.7e-06 → 8.25e-06 → 1.09e-05`), consistent with real O(n)-ish measurement.
  - The config's stated methodology is "median, warm-up excluded, perf_counter_ns high-resolution monotonic clock **with batch fallback for sub-clock-resolution operations**, IQR reported." A 200 ns per-op time is below or at the edge of reliable `perf_counter_ns` resolution on many platforms, so the "batch fallback" is presumably active — but the artifacts do not show the *raw* batch size, batch total time, or per-batch spread that would let a reviewer confirm the fallback actually engaged rather than the harness silently returning a floor/clamped value. A flat 200 ns curve with zero IQR across a 10x data-size range is the same pattern one would see from a broken timer *or* from a legitimately O(1) candidate operation measured via batching — the artifacts do not by themselves distinguish these. Given this was the exact class of bug that crashed E1-RUN-1, this warrants an explicit sanity note in the writeup (e.g., raw batch size and total batch wall-time) rather than resting on "kill(d) doesn't fire" alone. This is a **methodology-confidence flag, not a verdict-changing issue** — the reported numbers are internally consistent and pass the stated bars, but the near-1.0 candidate growth ratio is legitimately worth a second look before being treated as strong evidence the candidate scales O(1).
- `scaling_collapse_ratio_diagnostic = 0.0` — reported as diagnostic only, correctly carries no kill, consistent with `candidate_slope = 0.0` (flat curve → zero slope, self-consistent with the flat-curve observation above).

## 4. Property (iii) — Load-bearing coupling

- `downstream_degradation` > 0 on **all 5 seeds** (0.122, 0.098, 0.092, 0.120, 0.106) — confirmed.
- Mean degradation = 0.1076 ≥ 0.05 floor — confirmed, with comfortable margin (~2.15x the floor).
- **R1 (component-wise reporting):** CU degradation, RD degradation, and aggregate are reported separately per seed in both `e1_run_results.json` (per-seed `downstream_degradation_cu` / `_rd` / `_aggregate`) and `e1_invariants.json` (`downstream_degradation_cu_per_seed`, `_rd_per_seed`). Confirmed present and separated as required.
- **R2 (0.4 ceiling / specificity control):**
  - `aggregate_true_ceiling = 0.4` is explicitly stated.
  - Frozen CU recall (specificity control) = 0.9973 mean, ranging 0.9933–1.0 per seed — high, as pre-registered, supporting the claim that degradation is specific to destroyed temporal organization rather than general breakage.
  - **⚠️ ISSUE — CU degradation is not exactly 0.000 in practice, contradicting its own "by construction" label.** The note states: *"CU degradation is 0.000 BY CONSTRUCTION (bucket size = k)."* But the actual per-seed data shows:
    - seed 42: CU degradation = 0.0033
    - seed 43: CU degradation = 0.0067 (2 of 30 CU queries show 0.1 degradation each — verified directly against the per-query recall table)
    - seed 44: CU degradation = 0.0000
    - seed 45: CU degradation = 0.0000
    - seed 46: CU degradation = 0.0033
    - Mean CU degradation = 0.00267, not 0.0.
  - This is a small magnitude and does not threaten any floor or kill condition, but the "BY CONSTRUCTION" language over-claims exactness. The likely cause is a tie-breaking edge case in top-k selection (bucket size exactly equals k, so ties at the k-th rank boundary can flip membership under floating-point noise) — this is a plausible and benign explanation, but the artifacts do not state it, and the note should read "≈0" or explain the tie-breaking edge case rather than asserting exact-zero.
- **Hold-out seed consistency (45, 46) vs. development seeds (42, 43, 44):**
  - Dev seed degradation range: 0.092–0.122 (mean 0.104, stdev ≈0.016).
  - Seed 45 = 0.1200 — within dev range.
  - Seed 46 = 0.1060 — within dev range.
  - **No red flag** — hold-out seeds are consistent with, not wildly different from, development seeds, supporting genuine out-of-sample validity.

## 5. Kill conditions

All 5 active kill conditions (b, c, d, e, f) are cross-checked directly against raw per-seed values:

| Kill | Fires? | Cross-check |
|---|---|---|
| (b) chain integrity | False | `chain_integrity_final = 1.0` confirmed on all seeds in `e1_run_results.json`; log shows `initial=True, shift=True, 10x=True` on every seed, both runs. |
| (c) coordinate shift | False | `coordinate_shift = 1.0`; `shift_per_append` = all `True` (8/8) on every seed, both runs. |
| (d) latency/scaling | False | `candidate_growth ≤ 2.0` (=1.0 on all seeds) and `fair_naive_growth ≥ 4.0` (6.69–7.13 across seeds) — both confirmed directly against per-seed raw values (see §3). |
| (e) wall-clock independence | False | `wall_clock_shift_detected = 0.0` confirmed on all seeds. |
| (f) correctness | False | `oracle_agreement = 1.0` strict on all seeds (see §2), signed. |

`(a)` is correctly marked RETIRED with rationale ("unsatisfiable by construction per Rebecca's theorem"). No discrepancies found between the kill-condition summary block and the underlying per-seed raw data.

## 6. I3 contamination

- All three arms (`shuffled_cadence`, `empty`, `wall_clock_injection`) report `in_band: true`.
- `null_replicate_count: 100` confirmed for the method description.
- **⚠️ MINOR ISSUE — stale wording:** The I3 method's `rules` field states *"The 3-seed mean must fall in the band"* — this run uses **5 seeds** (42–46), not 3. This looks like leftover language from before hold-out seeds 45/46 were added to scoring. It does not appear to affect the actual computation (the in-band checks pass regardless of seed count), but the documentation is stale and should be updated to "5-seed mean" for consistency with R3's stated scoring-seed set.

## 7. L20 self-test

- `no_drift_corr = 1.0`, `no_drift_passes = True` — confirmed in `e1_profile.json` and `e1_run.log`.
- Perturbation 1 (`metric_block_reversal`): corr = -0.20, correctly flagged as drift (< 0.5 threshold).
- Perturbation 2 (`candidate_empty_swap`): corr = 0.0, correctly flagged as drift (< 0.5 threshold).
- `both_perturbations_flag_drift = True` — confirmed.
- **No issues found here.**

## 8. R4 — Auditable arithmetic

Independently recomputed the aggregate, CU, and RD degradation from the raw `per_query_recall_tables` in `e1_invariants.json` for all 5 seeds:

| Seed | Recomputed agg | Reported agg | Match | Recomputed CU | Reported CU | Match | Recomputed RD | Reported RD | Match |
|---|---|---|---|---|---|---|---|---|---|
| 42 | 0.122000 | 0.122000 | ✅ | 0.003333 | 0.003333 | ✅ | 0.300000 | 0.300000 | ✅ |
| 43 | 0.098000 | 0.098000 | ✅ | 0.006667 | 0.006667 | ✅ | 0.235000 | 0.235000 | ✅ |
| 44 | 0.092000 | 0.092000 | ✅ | 0.000000 | 0.000000 | ✅ | 0.230000 | 0.230000 | ✅ |
| 45 | 0.120000 | 0.120000 | ✅ | 0.000000 | 0.000000 | ✅ | 0.300000 | 0.300000 | ✅ |
| 46 | 0.106000 | 0.106000 | ✅ | 0.003333 | 0.003333 | ✅ | 0.260000 | 0.260000 | ✅ |

All values match exactly. Additionally executed `critic_independent_rerderivation.py` (the CRITIC's from-scratch implementation of the Option E spec, independent of the ARCHITECT's code path) for the 3 development seeds — it reproduced RD/CU/aggregate values consistent with the reported results (within expected rounding: the script's own printed 3-seed values 0.120/0.094/0.092 differ trivially from the reported 0.1220/0.0980/0.0920 by ≤0.004, well within its own stated tolerance and not a discrepancy in the underlying mechanism). **R4 is fully satisfied** — the aggregate is genuinely reconstructable from raw per-query values by an independent party, and the CRITIC's from-scratch script corroborates the CU≈0/RD>0 pattern.

- **Minor cosmetic note:** `critic_independent_rerderivation.py`'s docstring states "per-seed 0.120/0.094/0.092" as the target values to confirm, which are the script's own generated-and-rounded outputs rather than the exact reported 0.1220/0.0980/0.0920 — harmless but could confuse a future reader comparing docstring numbers to the official results.

## 9. Environment

- Python 3.12.10 confirmed identically across `e1_manifest.json` (`python_version_runtime`), `e1_run_2_roundtrip_log.txt`, and the `e1_run.log` header. Correctly logged as a self-detected deviation from the pinned 3.11.x, marked non-blocking.
- numpy 1.26.4 and scipy 1.13.1 confirmed matching the pin in all three locations.
- **⚠️ ISSUE — commit hash not recorded in the manifest itself:** `e1_manifest.json.commit_hash` literally contains the string `"pending -- no git repo"`, **not** the actual commit hash. The correct hash (`1d13105e8163859d7972705b731ba8c24a272276`) only appears in the separate `e1_run_2_roundtrip_log.txt` under "Scored commit." This means the primary scoring artifact (`e1_manifest.json`) does not self-certify its own commit provenance — a reviewer relying on the manifest alone would see a placeholder, not a hash. Recommend the manifest be regenerated to populate `commit_hash` directly, rather than depending on an external round-trip log to supply it.
- SHA-256 integrity: independently recomputed SHA-256 hashes for all 6 files listed in the round-trip log's hash table and confirmed byte-for-byte match against the claimed hashes and file sizes (`critic_independent_rerderivation.py`, `e1_invariants.json`, `e1_manifest.json`, `e1_profile.json`, `e1_run.log`, `e1_run_results.json`). All 6 matched exactly. **No tampering or corruption detected.**

## 10. Hold-out seed integrity

- Confirmed exact match to the task's stated values: seed 45 degradation = 0.1200 (CU=0.0000, RD=0.3000); seed 46 degradation = 0.1060 (CU=0.0033, RD=0.2600); dev seeds 42/43/44 = 0.1220/0.0980/0.0920.
- Both hold-out seeds fall within the development seed range (0.092–0.122) — no evidence of distributional shift or cherry-picking. This supports genuine out-of-sample generalization for property (iii).

---

## Summary of issues (none verdict-changing, all worth JUDGE attention)

1. **`bit_identical=True` is scoped to non-timing metrics only** — timing diagnostics genuinely differ between run-1 and run-2 passes (expected for wall-clock measurements, but not explicitly called out as excluded from the bit-identical claim).
2. **Candidate latency curve is suspiciously flat (exactly 200ns, zero IQR, growth=1.0 on every single seed)** — internally consistent and passes all bars, but the artifacts don't expose raw batch-fallback diagnostics (batch size, total batch time) needed to fully rule out timer-floor artifacts versus genuine O(1) behavior. This is the same failure class that crashed E1-RUN-1, so extra scrutiny is warranted even though nothing is broken this time.
3. **"CU degradation = 0.000 BY CONSTRUCTION" is not exactly true empirically** — 3 of 5 seeds show small nonzero CU degradation (0.0033–0.0067), likely a top-k tie-breaking edge case. Magnitude is negligible and doesn't affect any floor, but the "BY CONSTRUCTION" (i.e., mathematically guaranteed) language over-claims.
4. **I3 method documentation says "3-seed mean"** but the run uses 5 scoring seeds — stale wording, not a computational error.
5. **`e1_manifest.json.commit_hash` field is a placeholder ("pending -- no git repo")** rather than the actual commit hash; the real hash only lives in the separate round-trip log.

## Confirmed clean (no issues)

- All 5 seeds present and consistent.
- Zero NaN/inf anywhere in either JSON artifact.
- oracle_agreement = 1.0 on all seeds, both log and JSON.
- All 5 kill conditions (b–f) correctly report `fires=False`, cross-verified against raw values.
- I3: all arms in-band, 100 replicates/arm as specified.
- L20: no_drift_corr ≈ 1.0, both perturbations correctly flag drift, no_drift_passes=True.
- R4: aggregate/CU/RD degradation independently recomputed from per-query tables and matched exactly on all 5 seeds; independent from-scratch re-derivation script corroborates the mechanism.
- Hold-out seeds 45/46 consistent with development seeds 42–44 — no distributional red flag.
- Python/numpy/scipy versions consistently reported across all artifacts; deviation correctly self-flagged as non-blocking.
- SHA-256 hashes and file sizes for all 6 output files independently verified to match the round-trip log's claims exactly.

**Net assessment:** The PASS verdict is well-supported by the data. The issues above are documentation/rigor gaps (stale wording, an over-precise "by construction" claim, a manifest field left as a placeholder, and a legitimate-but-unproven flat timing curve) rather than errors that would change the outcome. Recommend the JUDGE note issue #2 (timing plausibility) as the highest-priority item for any follow-up, since it touches the exact failure mode that caused E1-RUN-1 to crash.
