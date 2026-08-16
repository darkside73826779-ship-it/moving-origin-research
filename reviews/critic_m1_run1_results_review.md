# CRITIC Review — M1 RUN-1 Results

**Reviewer:** CRITIC (adversarial review of returned artifacts)
**Run reviewed:** `m1-20260815T194311Z`
**Artifacts reviewed:** `m1_run_results.json`, `m1_invariants.json`, `m1_manifest.json`, `m1_run.log`, `m1_profile.json`, `run1_roundtrip_log.txt`, `run1_deviations.txt`
**Date:** 2026-08-15

---

## VERDICT: RESULTS CLEAN

All seven artifacts are internally consistent and the invariant suite verdict (`invariant_suite_green = true`) is supported by the underlying data. No blocking concerns. Seven non-blocking notes are documented below for the JUDGE's awareness and for hardening future runs.

---

## 1. Internal numeric consistency — CLEAN

Cross-checks performed programmatically (computed from raw per-seed values in `m1_run_results.json` and compared to every downstream artifact):

| Check | Max abs error | Result |
|---|---|---|
| `profile_mean_over_seeds` recomputed from per-seed values | 5.6e-17 | PASS |
| `m1_run.log` per-seed values (4-dp rounded) vs JSON per-seed | 0 (within rounding) | PASS |
| I4 margins `oracle_mean − naive_mean` vs bar 0.30 | all margins ≥ 0.508 | PASS |
| I3 band containment for empty/permuted/shuffled 3-seed means | all IN band | PASS |
| `shuffled_post_fix_verification` equals `shuffled` mean | exact match all 4 metrics | PASS |
| `profile_vector` vs `profile_mean_over_seeds` | 0.0 | PASS |
| I1 per-seed max abs diff = 0.0 for seeds 42/43/44 | matches log + invariants | PASS |

The per-seed values reported in `m1_run.log` (rounded to 4 dp) match `m1_run_results.json` to displayed precision for all 3 seeds × 6 arms × 4 metrics. Means are exact. Invariant verdicts match the underlying numbers.

**I4 margins are not borderline** — smallest is auroc at 0.5078 vs the 0.30 bar (1.7× headroom). naive sits at chance on every metric (auroc 0.492, recall 0.167), oracle at 1.0, frozen correctly between (auroc 0.731, ndcg 0.707, spearman 0.426, recall 0.283).

---

## 2. Anomalies the JUDGE might miss — none blocking

Spot checks of every "barely" region:

- **Tightest I3 containment margin:** `empty/auroc` at 0.0705 from the upper band edge (0.5000 vs upper 0.5705). Not borderline; the next-tightest is `permuted/recall` at 0.0833. No value is within 0.07 of a band edge.
- **Discrimination:** all four metrics clear the 0.30 bar by ≥ 0.20 absolute. No near-misses.
- **I2 oracle ceiling:** exactly 1.0 on every metric/seed, floor 0.95. Not borderline (by construction).
- **L20 self-test:** `no_drift_corr = 1.0`; pert1 (arm-block reversal) corr −0.0218, pert2 (empty/oracle swap) corr 0.1659 — both well below the 0.5 self-test threshold and would also trip the 0.7 locked bar. Consistent with a profile that is genuinely sensitive to structural perturbation.

No invariant "passes but shouldn't" was found.

---

## 3. Python 3.12.10 deviation — NON-BLOCKING (properly handled)

`requirements.txt` pins `python==3.11`; runtime was 3.12.10. Assessment:

- **I1 (reproducibility)** is defined as *within-run* determinism (rerun in the same process). It passes with 0.0 diff on all seeds. The Python version is constant across the two within-run passes, so I1's validity is unaffected.
- **I2 (oracle ceiling), I4 (discrimination bar), I5 (frozen ordering)** are construction-determined (oracle ranks perfectly; naive is signal-free; frozen carries partial signal). None depend on Python-version-specific RNG behavior for their logical validity.
- **I3 (contamination floor)** builds its null from the naive arm over 30 seeds in the same process — internally consistent regardless of Python version.
- numpy 1.26.4 / scipy 1.13.1 control their own RNG streams, which are version-stable across CPython 3.11/3.12. The within-run I1 result (0.0 diff) corroborates determinism.

**Caveat (non-blocking):** cross-version reproducibility (3.11 vs 3.12) is *not* tested by any invariant. Since 3.11 was unavailable on the executor, this is an unverified property rather than a violation. The deviation is correctly logged in `run1_deviations.txt`, surfaced in the round-trip log, and is discoverable from the manifest itself via `python_version_runtime = "Python 3.12.10"` vs `deps.python = "3.11.x ..."`.

---

## 4. LOW-POWER flags on `ndcg_at_k` and `spearman_rho` (I3) — NON-BLOCKING, with a recommendation

`I3_contamination_floor` flags `low_power: true` for `ndcg_at_k` (band width 0.2345) and `spearman_rho` (band width 0.3206). The band is the central 99% interval of the naive arm over **30 null replicates**; with only 30 samples, the 0.5th/99.5th percentiles are effectively the observed min/max, so the band is wide and the test has low statistical power to detect *mild* contamination on those two metrics.

Assessment of the contamination verdict's trustworthiness:

- The two **non-low-power** metrics (`auroc` width 0.1971, `recall_at_k` width 0.2000) pass cleanly and independently confirm no contamination in the empty/permuted/shuffled arms.
- The **shuffled post-fix verification** — the strongest single piece of evidence — is comfortably at chance on *all four* metrics, including the two low-power ones: auroc 0.485, ndcg 0.467, spearman −0.030, recall 0.083. None are borderline (smallest margin to a band edge is 0.0833). This is independent corroboration that the fix removed signal.
- The empty and permuted arms also sit inside the band on all four metrics.

**Conclusion:** the contamination verdict is trustworthy. The low-power flag is honestly reported and does not hide a failure. **Recommendation (non-blocking):** raise the null replicate count to ≥ 100 in future runs so the 99% interval is narrower and I3 has meaningful power on ndcg/spearman, not just auroc/recall.

---

## 5. Empty `deviations_logged` in manifest vs external `run1_deviations.txt` — NON-BLOCKING (by design, but minor robustness gap)

`m1_manifest.json` has `"deviations_logged": []` while `run1_deviations.txt` documents the Python 3.12.10 deviation. This is not a true discrepancy: per the execution instructions, deviations are logged *externally* in the deviations file, not in the manifest field. The deviation is still fully discoverable from the manifest alone:

- `python_version_runtime: "Python 3.12.10"` (actual)
- `deps.python: "3.11.x (exact version recorded at runtime via python --version)"` (spec)

…plus the round-trip log line `Deviations: Python 3.12.10 used ... see run1_deviations.txt`.

**Recommendation (non-blocking):** for robustness against a reader who only opens the manifest, either populate `deviations_logged` with a one-line summary/reference (e.g. `["python==3.11 -> 3.12.10; see run1_deviations.txt"]`) or add an explicit `external_deviations_file` field. A naive automated parser that keys only on `deviations_logged` would miss the version mismatch.

---

## 6. Shuffled post-fix verification — genuine PASS, not borderline

Shuffled 3-seed means vs I3 band and vs chance:

| metric | shuffled mean | band | nearest-edge margin | vs chance |
|---|---|---|---|---|
| auroc | 0.4850 | [0.3734, 0.5705] | 0.0855 | ~0.5 ✓ |
| ndcg_at_k | 0.4666 | [0.3459, 0.5804] | 0.1138 | ~0.46 ✓ |
| spearman_rho | −0.0304 | [−0.1867, 0.1339] | 0.1563 | ~0 ✓ |
| recall_at_k | 0.0833 | [0.0000, 0.2000] | 0.0833 | ~0.078 (null mean) ✓ |

Every value is inside the band and at chance. The tightest margin (auroc, 0.0855 from the upper edge) is comfortable. This is a genuine pass: the post-fix shuffled arm carries no signal, confirming the contamination fix is effective.

---

## 7. I5 `recall_at_k` N/A — expected per pre-registered rule, NON-BLOCKING

I5 (naive < frozen < oracle) per-seed for `recall_at_k`:

| seed | naive | frozen | oracle | ordering |
|---|---|---|---|---|
| 42 | 0.10 | 0.20 | 1.00 | strict ✓ |
| 43 | 0.15 | 0.40 | 1.00 | strict ✓ |
| 44 | 0.25 | 0.25 | 1.00 | **tie (frozen == naive)** |

Seed 44 produces an exact tie (frozen = naive = 0.25), so strict per-seed ordering fails and the fallback is triggered, logging N/A. This is **expected**: `recall_at_k` with k=20 and n_relevant=20 is quantized in steps of 0.05, so ties are unavoidable and a strict per-seed rule is too aggressive for this metric. The conservative N/A (decline to assert rather than assert falsely) is the correct behavior and does not falsely pass.

The other three metrics (auroc, ndcg, spearman) satisfy strict naive < frozen < oracle on all three seeds, so I5 passes overall — consistent with `I5.passes = true` and `invariant_suite_green = true`.

**Minor note (non-blocking):** the rationale string `"N/A (frozen<=naive on some seed; fallback: non-strict not met -> N/A logged)"` is ambiguous. The data shows a *tie* (frozen == naive), and a non-strict `naive <= frozen <= oracle` reading would actually be satisfied on seed 44. The phrase "non-strict not met" does not transparently describe what was computed. The verdict (N/A) is appropriate; the *stated reason* could be clearer. Recommend the harness emit the explicit per-seed strict/non-strict table in the detail string.

---

## 8. Scope drift — none detected

The harness executes exactly M1's scope:

- **Config:** n_items=200, n_relevant=20, n_cycles=50, k=20, base_rate=0.1, seeds [42,43,44] — matches the M1 spec.
- **Arms:** empty, permuted, shuffled, oracle, naive, frozen — all within M1's control battery.
- **Metrics:** auroc, ndcg_at_k, spearman_rho, recall_at_k — the M1 metric set.
- **Invariants:** I1–I5 — the pre-registered M1 invariant suite. No extra invariants evaluated.
- **I3 null replicates** (30 seeds, 100–129) are part of I3's empirical-null method, within scope.
- **L20 profile + self-test** is the M1 profile artifact, within scope.

No out-of-scope testing, no extra arms, no extra metrics, no silent changes to thresholds (bar 0.3, I2 floor 0.95, L20 locked bar 0.7 / self-test 0.5 all as specified).

---

## Additional minor observations (non-blocking)

- **`m1_run.log` is not valid UTF-8.** Byte 0x97 (a Windows-1252 em-dash in `"M1 HARNESS — L18"`) at offset 85 causes strict UTF-8 parsers to fail. Cosmetic, but the log file is technically malformed. Recommend the harness write logs as UTF-8 (encode the em-dash as U+2014, 0xE2 0x80 0x94) or use an ASCII fallback like `--`.
- **`commit_hash: "pending — no git repo"`.** Provenance gap; non-blocking for M1 but recommend initializing a git repo so future runs carry a real commit hash.
- **Wall clock 0.0419 s.** Consistent with a synthetic in-process battery; no anomaly.

---

## Summary table

| # | Item | Concern level | Disposition |
|---|---|---|---|
| 1 | Internal numeric consistency | none | CLEAN |
| 2 | Hidden anomalies / borderline passes | none | CLEAN |
| 3 | Python 3.12.10 vs pinned 3.11 | non-blocking | Logged; invariants unaffected (I1 within-run; I2–I5 construction-determined) |
| 4 | LOW-POWER on ndcg/spearman (I3) | non-blocking | Verdict trustworthy; raise null replicates to ≥100 in future |
| 5 | Empty `deviations_logged` in manifest | non-blocking | By design; deviation discoverable via `python_version_runtime` + round-trip log |
| 6 | Shuffled post-fix verification | none | Genuine pass, not borderline |
| 7 | I5 recall_at_k N/A | non-blocking | Expected per pre-registered rule (seed-44 tie, coarse metric); rationale string could be clearer |
| 8 | Scope drift | none | CLEAN |

**Final verdict: RESULTS CLEAN.** No blocking concerns. The seven non-blocking notes are documented for the JUDGE's awareness and as hardening recommendations for RUN-2.
