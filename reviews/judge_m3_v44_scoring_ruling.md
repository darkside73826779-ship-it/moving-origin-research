# JUDGE Ruling — M3 V4.4 Fresh-Seed Scoring Run

**Run scored:** M3 V4.4 scoring run (seeds 301, 302, 303; law: all; mode: scoring)
**Scored from:** Raw artifacts in `runs/m3-scoring-v44-301-303/` (project file repo) + `m3_scoring_roundtrip_log.txt` ONLY.
**Date:** Sunday, 2026-08-16 (23:18 EDT)
**Spec basis:** `m3_e2_spec_amended_v4_4.md` (V4.4), `m3_e2_courier_scoring_packet.md` (as updated)
**Attested commit:** `95440b4792d1eb100b3b1d015eb02b6dbf92ecc3` (manifest; confirmed on GitHub main)
**Authorized seed edits:** 3 minimal seed-enablement edits to `src/m3_harness.py` (documented in `RUN_PROVENANCE_AND_LOCAL_RETENTION.md`, attested by Rebecca's supervised scoring authorization)

> Scoring is performed exclusively from the raw returned artifacts. No agent's characterization of the run was used as evidence. All p-values, integer counts, and scored metrics were independently verified from the summary artifacts. The V4.4 Phase B raw-artifact recomputation (full RNG reproduction from 257,636 raw files) was not completed — the raw artifact tree is retained locally on Rebecca's system and available on request. The ruling is based on the returned summary artifacts and integer p-value fields, which are sufficient for the decisive verdict.

---

## VERDICT: **INSTRUMENT FAILURE**

L3 has INSTRUMENT_FAILURE on seed 303 (frozen arm plus-one p-value 0.012 < alpha_seed 0.0167). L1, L5, and L6 all PASS on all 3 seeds. No kill conditions fire — the candidate passes every candidate-facing bar on all 3 seeds. Per courier packet §5.2, INSTRUMENT FAILURE means the test apparatus is broken, not that the candidate failed. L1/L5/L6 results are valid scored evidence. The overall verdict is INSTRUMENT FAILURE because any law-level instrument failure blocks the overall verdict (courier packet §6).

---

## Package integrity

- **Commit hash:** `95440b4792d1eb100b3b1d015eb02b6dbf92ecc3` — independently verified on GitHub main (commit message: "merge: M3 V4.4 implementation — ARCHITECT implementation-completeness amendment + TASK BUILDER V4.4 stochastic controls (CRITIC-CLEARED, 3 parallel reviews PASS)"). **VERIFIED.**
- **STATE.md SHA-256:** Manifest reports `01b9e8a4...`; actual file at commit `95440b4` has LF hash `b161a2e5...` and CRLF hash `01b9e8a4...` — match confirmed with CRLF normalization (same Windows-executor pattern as all prior runs). **VERIFIED.**
- **Round-trip log:** Present (`m3_scoring_roundtrip_log.txt`, 41.3 MB), contains SHA-256 inventory of all 257,647 files (257,636 raw artifacts + 11 summary files). **VERIFIED.** Improvement over first scoring run (where round-trip log was missing).
- **File hashes:** All 10 file hashes in `m3_manifest.json` match the CRLF-normalized versions of the project-repo files. Files in the project repo are stored with LF line endings; the manifest hashes (generated on Windows with CRLF) match after CRLF restoration. **VERIFIED.**
- **11 output files present:** All 10 files listed in courier packet §3.1 plus `m3_v44_raw_manifest.json` (raw artifact index). **VERIFIED.**

---

## Authorized seed-enablement edits

The harness at commit `95440b4` is designed to fail closed in scoring mode — `_allowed_seeds_for_mode('scoring')` returns `set()`, blocking all seeds. The `RUN_PROVENANCE_AND_LOCAL_RETENTION.md` documents three authorized edits to enable fresh-seed scoring:

1. `SCORING_SEEDS = [301, 302, 303]` (was `[201, 202, 203]`)
2. `RETAINED_INSTRUMENT_FAILURE_SEEDS = frozenset({201, 202, 203})` (was `frozenset(SCORING_SEEDS)`)
3. `_allowed_seeds_for_mode('scoring')` returns `set(SCORING_SEEDS)` (was `return set()`)

**Base `src/m3_harness.py` Git blob:** `6374359b1dec48d01c49cbc9d256350995abe039` — independently verified via `git hash-object` at commit `95440b4`. **VERIFIED.**

**Executed `src/m3_harness.py` SHA-256:** `408450a59aa5bf6354503317412ff62673c5f34c5a5919acccb1bf562d588d60` — attested in the provenance document; the JUDGE could not independently reconstruct the locally edited file to verify this hash, so this is accepted as documented/attested rather than independently proven.

**Assessment:** The three edits are seed-enablement changes only — they do not modify any bar, control, logic, constant, or scoring path. The base harness code (bars, controls, V4.4 stochastic families, RNG protocol) is unchanged. The edits enable seeds 301–303 while keeping retained instrument-failure seeds 201–203 permanently blocked. **Accepted as documented.**

---

## L1 — Access physics (PASS on all 3 seeds)

### Candidate bars (all 3 seeds)

| Bar | Required | Seed 301 | Seed 302 | Seed 303 |
|---|---|---|---|---|
| R² (binned marginal-mean) | ≥ 0.85 | 0.9854 ✅ | 0.9854 ✅ | 0.9854 ✅ |
| β_age (direction) | < 0 | −0.00150 ✅ | −0.00150 ✅ | −0.00150 ✅ |
| All 5 conditional ρ (rehearsal) | ≥ 0.6 | 0.912–0.946 ✅ | 0.912–0.946 ✅ | 0.912–0.946 ✅ |
| All 5 age-conditional slopes | < 0 | all negative ✅ | all negative ✅ | all negative ✅ |

### V4.4 stochastic controls (L1)

Per V4.4 §2.9, each stochastic family uses R=1000, alpha_seed=0.05/3≈0.01667, plus-one p-value: `p_s = (1 + exceed_or_tie_count) / 1001`. Pass condition: `p_s > 0.05/3`.

| Family | Seed 301 p | Seed 301 pass | Seed 302 p | Seed 302 pass | Seed 303 p | Seed 303 pass |
|---|---|---|---|---|---|---|
| Frozen (upper-tail R²) | 0.838 | ✅ | 0.570 | ✅ | 0.743 | ✅ |
| Fair-naive (upper-tail R²) | 0.283 | ✅ | 0.750 | ✅ | 0.973 | ✅ |
| Permuted (abs-ρ upper-tail) | 0.107 | ✅ | 0.216 | ✅ | 0.686 | ✅ |
| Shuffled (null-of-the-max upper-tail) | 1.000 | ✅ | 1.000 | ✅ | 1.000 | ✅ |

**V4.3/V4.4 shuffled arm fix confirmed:** The first scoring run (seeds 201–203) had INSTRUMENT_FAILURE on L1 seeds 201 and 203 due to shuffled-arm null-band violations (values below the lower bound). V4.4 replaced the two-sided band with a one-sided upper-tail null-of-the-max test (§2.9: "Any value below the upper threshold, including below the former lower band, is 'shuffle exceeded typical destruction — informational' and never fails"). The shuffled p-value is 1.000 on all 3 seeds. **The fix worked.**

### Exact L18 control arms (all seeds)

| Control | Status |
|---|---|
| Empty: returned_defined_error | ✅ (all seeds) |
| Recency-only: R² ≥ 0.85, β_age < 0, all ρ < 0.6 | ✅ (all seeds, identical across seeds — structural seed 777) |
| Rehearsal-only: β_age ≥ 0, all ρ ≥ 0.6 | ✅ (all seeds, identical across seeds) |
| Oracle: R² ≥ 0.85, β_age < 0, all ρ ≥ 0.6 | ✅ (all seeds) |

**L1 verdicts:** Seed 301: PASS. Seed 302: PASS. Seed 303: PASS. No instrument failures. No kills.

---

## L3 — Thick present (INSTRUMENT_FAILURE on seed 303; PASS on seeds 301, 302)

### Candidate bars (all 3 seeds)

**Bar (§1, §3.6):** ≥ 5% relative loss reduction at every horizon 1..5, all scoring seeds.

| Seed | h=1 | h=2 | h=3 | h=4 | h=5 | All ≥ 5%? |
|---|---|---|---|---|---|---|
| 301 | 22.0% | 21.3% | 13.9% | 11.3% | 21.5% | ✅ |
| 302 | 20.7% | 22.7% | 13.5% | 11.9% | 21.2% | ✅ |
| 303 | 19.8% | 22.9% | 14.0% | 12.2% | 20.9% | ✅ |

**Candidate passes the L3 bar on all 3 seeds.** No KILL.

### V4.4 stochastic controls (L3)

Per V4.4 §3, the L3 frozen, oracle, permuted, and shuffled arms are stochastic families with plus-one p-values and alpha_seed=0.05/3. The statistic S = max_h (family-specific score) over 5 horizons.

| Family | Seed 301 p | Seed 301 pass | Seed 302 p | Seed 302 pass | Seed 303 p | Seed 303 pass |
|---|---|---|---|---|---|---|
| Frozen (S=max_h reduction_h, upper-tail) | 0.491 | ✅ | 0.362 | ✅ | **0.012** | **❌** |
| Oracle (S=max_h v_h, upper-tail) | 0.351 | ✅ | 0.206 | ✅ | 0.783 | ✅ |
| Permuted (S=max_h reduction_h, upper-tail) | 0.970 | ✅ | 0.305 | ✅ | 0.228 | ✅ |
| Shuffled (S=max_h d_h, upper-tail) | 0.606 | ✅ | 0.758 | ✅ | 0.037 | ✅ |

### L3 frozen arm INSTRUMENT_FAILURE on seed 303 — detail

**V4.4 §3.1:** "Each observed/null draw yields five `reduction_h`; define `S=max_h reduction_h`. Use 1000 exchangeable full-pipeline AR(3) null draws per seed, the upper-tail plus-one p-value, and `alpha_seed=0.05/3`."

| Field | Value | Source |
|---|---|---|
| Observed frozen reductions (h=1..5) | −2.036, −1.544, −1.973, −1.970, −1.419 | `m3_l3_results.json` → `results.303.frozen_reductions` |
| S_observed (max_h reduction_h) | −1.4187189383223997 | `v44_stochastic_controls.frozen.observed_statistic` |
| Null 985th order statistic | −1.4374012771028852 | `v44_stochastic_controls.frozen.null_upper_order_statistic_985` |
| Exceed-or-tie count | 11 of 1000 | `v44_stochastic_controls.frozen.exceed_or_tie_count` |
| Plus-one p-value | (1 + 11) / 1001 = 12/1001 = 0.011988 | `v44_stochastic_controls.frozen.plus_one_p_value` |
| Alpha_seed | 0.05 / 3 = 0.016667 | `v44_stochastic_controls.frozen.alpha_seed` |
| Per-seed pass | False (0.011988 ≤ 0.016667) | `v44_stochastic_controls.frozen.per_seed_pass` |

**JUDGE independent verification of p-value computation:**
- S_observed = max(−2.036, −1.544, −1.973, −1.970, −1.419) = −1.419 ✅
- p_s = (1 + 11) / 1001 = 12/1001 = 0.011988... ✅ (verified from integer count)
- alpha_seed = 0.05/3 = 0.016667 ✅
- 0.011988 ≤ 0.016667 → per_seed_pass = False ✅

**Interpretation:** The frozen arm's observed max reduction (−1.419, the least negative frozen reduction at horizon 5) is slightly less negative than the null 985th percentile (−1.437). The frozen state on seed 303 is slightly less harmful than expected under the null distribution. All frozen reductions are strongly negative (−1.42 to −2.04), confirming the frozen state is actively harmful — but the calibrated null distribution expects it to be even more harmful. The p-value is below the pre-registered alpha_seed threshold. **Per V4.4 §2.11/§3.1, this is a pre-registered INSTRUMENT FAILURE.**

**Note on L3 shuffled arm (seed 303):** The shuffled p-value (0.037) is above alpha_seed (0.0167) and passes, but is relatively low compared to seeds 301 (0.606) and 302 (0.758). This indicates seed 303's AR(3) sequence produces less stable control-arm behavior overall, which is consistent with the frozen arm's borderline failure.

**L3 verdicts:** Seed 301: PASS. Seed 302: PASS. Seed 303: INSTRUMENT_FAILURE. No kills.

---

## L5 — Bi-temporality (PASS on all 3 seeds)

### Candidate bars (all 3 seeds)

| Bar | Required | Seed 301 | Seed 302 | Seed 303 |
|---|---|---|---|---|
| World-validity accuracy | ≥ 0.95 | 1.0 ✅ | 1.0 ✅ | 1.0 ✅ |
| Self-acquisition accuracy | ≥ 0.95 | 1.0 ✅ | 1.0 ✅ | 1.0 ✅ |
| Chain-walk accuracy (all 40) | = 1.00 | 1.0 ✅ | 1.0 ✅ | 1.0 ✅ |
| Access-count matches k | True | True ✅ | True ✅ | True ✅ |

### L18 control arms (all seeds)

| Control | Required | All seeds |
|---|---|---|
| Fair-naive world-validity accuracy | = 0.75 exactly | ✅ (0.75 all seeds) |
| Frozen post-freeze walk accuracy | = 0.00 | ✅ (0.00 all seeds) |
| Full-scan access-count delta (40 queries) | = 200 all | ✅ (200 all seeds, all 40 queries) |
| Shuffled chain-walk accuracy | ≤ 0.05 | ✅ (0.00 all seeds) |
| Permuted chain content mismatch rate | = 1.00 | ✅ (1.00 all seeds) |
| Empty: returned_defined_error | True | ✅ (all seeds) |
| All 5 bypass tests caught | all caught | ✅ (all seeds) |

### V4.4 stochastic control (L5 permuted)

Per V4.4 §4, L5 permuted combination accuracy uses a two-sided randomization rank p-value with alpha_seed=0.05/3.

| Seed | p-value | Pass |
|---|---|---|
| 301 | 0.543 | ✅ |
| 302 | 0.536 | ✅ |
| 303 | 0.721 | ✅ |

**L5 verdicts:** Seed 301: PASS. Seed 302: PASS. Seed 303: PASS. No instrument failures. No kills.

---

## L6 — Episodic completeness (PASS on all 3 seeds)

| Check | Required | Seed 301 | Seed 302 | Seed 303 |
|---|---|---|---|---|
| All 8 attacks caught | 8/8 | 8 ✅ | 8 ✅ | 8 ✅ |
| All 4 audit rows pass | 4/4 | 4 ✅ | 4 ✅ | 4 ✅ |
| All 6 L18 arms pass | 6/6 | 6 ✅ | 6 ✅ | 6 ✅ |
| Module namespace complete | True | True ✅ | True ✅ | True ✅ |

**L6 verdicts:** Seed 301: PASS. Seed 302: PASS. Seed 303: PASS. No instrument failures. No kills.

---

## Kill conditions

No kill conditions fire on any seed for any law. The candidate passes all candidate-facing bars on all 3 seeds. The L3 instrument failure is in the frozen-arm stochastic control (a test-apparatus check), not in the candidate mechanism.

---

## Reproducibility

### bit_identical = False

`m3_invariants.json.reproducibility`: `{"checked": true, "bit_identical": false, "scope": "all non-timing fields"}`. `m3_run.log` confirms: `checked=True bit_identical=False (non-timing metrics)`.

**Assessment:** This is a failed reproducibility check. The `--verify-reproducibility` second pass found non-identical non-timing fields between pass 1 and pass 2. The returned summary artifacts do not localize which specific fields differ — no diff field, mismatch list, or per-field comparison is present in the artifacts. Per courier packet §5.4: "If reproducibility fails, the run is flagged but does not automatically trigger INSTRUMENT FAILURE — the JUDGE and CRITIC assess the discrepancy from the returned artifacts."

The JUDGE cannot certify bit-identical reproducibility. The scored metrics (L1, L3, L5, L6 bars and p-values) are derived from deterministic computations using the V4.4 SHA-256 RNG protocol (§6), which should produce identical results across passes. The non-identity likely originates from V4.4 raw-artifact metadata that varies between passes (e.g., file paths, pass numbers, or embedded timestamps in the 257,636-file raw artifact tree), but this cannot be confirmed without the diff details.

**Impact on ruling:** The reproducibility failure does not change the headline verdict — L3 INSTRUMENT_FAILURE on seed 303 is the governing result, derived from the summary artifacts' p-value fields. However, the JUDGE cannot certify reproducibility, and this failure is **flagged for CRITIC investigation**. The CRITIC should request the harness's internal diff log or the pass-specific outputs to identify the differing fields and assess whether any scored metric is affected.

---

## Additional checks

### L20 drift self-test

`no_drift_corr = 0.9999999999999999` (≥ 1.0 − ε ✅), `no_drift_passes = True`. Perturbation 1: corr = −0.246 (< 0.50 ✅, flags drift). Perturbation 2: corr = 0.00 (< 0.50 ✅, flags drift). `both_perturbations_flag_drift = True`. **PASS.**

### Interface invariants (L11, L13, L5)

- L11 single-clock negative injection: `caught = True` ✅
- L13 encoding-snapshot negative injection: `caught = True` ✅
- L5 backdating-hash negative injection: `caught = True` ✅

`interface_invariants.passes = True`. **PASS.**

### Finite numeric results

`finite_numeric_results = True`. No NaN or inf in any scored metric. **PASS.**

### Raw artifact validation

`raw_artifact_validation`: `{"passed": true, "manifest": "m3_v44_raw_manifest.json", "error": null}`. The harness validated its own raw artifact manifest. **PASS.**

### Manifest deviation disclosure

`deviations_logged`: `["Python 3.11.9 vs pinned 3.11 (non-blocking)"]`. Python 3.11.9 matches pinned 3.11.x. numpy 1.26.4 and scipy 1.13.1 match exactly. **DISCLOSED.**

### Seed exposure ledger

Pool label: `"M3_fresh_supervised_scoring"` — improved from the first scoring run's `"M3_development"`. However, `scope` field still says `"M3 development diagnostics only"` (stale). `run_type` is correctly `"scoring"` on all 12 events. **Stale scope label flagged.**

### Manifest stale wording

`r3_note` and `scoring_seed_pool` still use "development" boilerplate despite `mode: scoring`. Same issue as first scoring run. **Flagged.**

---

## Provenance adjudication

### Commit hash

- Manifest reports: `95440b4792d1eb100b3b1d015eb02b6dbf92ecc3`
- GitHub main verified: commit exists, message "merge: M3 V4.4 implementation — CRITIC-CLEARED, 3 parallel reviews PASS"
- This is the authorized V4.4 implementation commit. **VERIFIED.**

### STATE.md hash

- Manifest reports: `01b9e8a47c5b51211dcd788279947f5bcba7840f5cf03e96e101e450eeee7be4`
- Actual at `95440b4` (LF): `b161a2e5...`
- CRLF-normalized: `01b9e8a4...` — matches manifest exactly. **VERIFIED (CRLF normalization).**

### Round-trip log

- Present (41.3 MB), contains SHA-256 inventory of all 257,647 files, exact command, commit hash, exit status (1), wall clock (852.6s). **VERIFIED.** Improvement over first scoring run.

### File hashes

All 10 manifest file hashes match the CRLF-normalized versions of the project-repo files. Files in the project repo are stored with LF; manifest hashes were generated on Windows with CRLF. **VERIFIED after CRLF restoration.**

### Authorized seed-enablement edits

- Base `src/m3_harness.py` Git blob `6374359b1dec48d01c49cbc9d256350995abe039` — independently verified via `git hash-object` at commit `95440b4`. **VERIFIED.**
- Three edits (SCORING_SEEDS, RETAINED_INSTRUMENT_FAILURE_SEEDS, _allowed_seeds_for_mode) are seed-enablement only — no bars, controls, logic, or constants modified. **Accepted as documented/attested** (executed file SHA-256 `408450a5...` not independently reconstructed by JUDGE).
- Seeds 201–203 confirmed blocked (retained instrument-failure seeds). **VERIFIED.**

---

## Cross-run consistency

| Law | First run (201–203) | This run (301–303) | Cross-run finding |
|---|---|---|---|
| L1 candidate bars | PASS all seeds | PASS all seeds | Consistent — candidate mechanism is stable |
| L1 shuffled arm | INSTRUMENT_FAILURE seeds 201, 203 | PASS all seeds | V4.4 fix (one-sided null-of-the-max) resolved the first run's failure |
| L3 candidate bars | PASS all seeds | PASS all seeds | Consistent |
| L3 frozen arm | PASS all seeds (V4.2 unproved ≤0% check) | INSTRUMENT_FAILURE seed 303 (V4.4 calibrated p-value) | V4.4 replaced the unproved check with a calibrated stochastic test; the calibrated test caught a borderline case on seed 303 |
| L5 | PASS all seeds | PASS all seeds | Consistent |
| L6 | PASS all seeds | PASS all seeds | Consistent |
| Reproducibility | bit_identical = True | bit_identical = False | New issue — flagged for CRITIC |

**Key cross-run finding:** The V4.4 systemic closure fixed the L1 shuffled-arm false-positive pattern (the first run's INSTRUMENT_FAILURE on seeds 201/203 was caused by a two-sided band that flagged below-band values as failures; V4.4's one-sided upper-tail test correctly treats below-band shuffled values as informational). However, the V4.4 L3 frozen-arm calibrated test introduced a new borderline INSTRUMENT_FAILURE on seed 303. The candidate mechanism itself passes all candidate-facing bars on all seeds in both runs.

---

## Summary Table

| Criterion | Status |
|---|---|
| Package integrity (commit, STATE.md, round-trip log, file hashes) | ✅ Verified (CRLF-normalized) |
| Authorized seed-enablement edits | ✅ Accepted as documented (3 minimal edits, base blob verified) |
| L1 candidate bars (all seeds) | ✅ R²=0.9854, β_age<0, all ρ≥0.6 |
| L1 V4.4 stochastic controls (all 4 families × 3 seeds) | ✅ All p > 0.05/3 |
| L1 verdict | PASS (all 3 seeds) |
| L3 candidate bars (all seeds) | ✅ All reductions ≥ 5% (11.3%–22.9%) |
| L3 V4.4 frozen arm (seed 303) | ❌ INSTRUMENT FAILURE (p=0.012 < alpha_seed=0.0167) |
| L3 V4.4 other controls (all seeds) | ✅ All pass |
| L3 verdict | INSTRUMENT_FAILURE (seed 303); PASS (seeds 301, 302) |
| L5 candidate bars + controls (all seeds) | ✅ All verified |
| L5 V4.4 permuted stochastic (all seeds) | ✅ All p > 0.05/3 |
| L5 verdict | PASS (all 3 seeds) |
| L6 bars (all seeds) | ✅ 8/8 attacks, 4/4 audit, 6/6 L18 arms |
| L6 verdict | PASS (all 3 seeds) |
| Kill conditions | ✅ None fire |
| Reproducibility (bit_identical) | ❌ False — failed check, diff fields not localized in artifacts |
| L20 drift self-test | ✅ PASS |
| Interface invariants (L11, L13, L5) | ✅ PASS |
| Finite numeric results | ✅ True |
| Raw artifact validation | ✅ Passed |
| Manifest deviations | ✅ Disclosed (Python 3.11.9, non-blocking) |
| Seed ledger scope label | Stale "development" scope despite scoring run — flagged |
| Manifest stale wording | Stale "development" boilerplate — flagged |
| Phase B raw-artifact recomputation | Not completed — raw artifacts retained locally, available on request |

---

## Final Ruling

### **INSTRUMENT FAILURE**

L3 has INSTRUMENT_FAILURE on seed 303 (frozen arm plus-one p-value 12/1001 = 0.012 ≤ alpha_seed 0.05/3 = 0.0167 — a pre-registered V4.4 stochastic control failure per §3.1/§2.11). The observed frozen max reduction (−1.419) is slightly less negative than the null 985th percentile (−1.437), placing it in the upper rejection tail. All frozen reductions are strongly negative (−1.42 to −2.04), confirming the frozen state is harmful — but the calibrated null distribution expects it to be even more harmful on seed 303.

L1, L5, and L6 all PASS on all 3 seeds with all bars and V4.4 stochastic controls independently verified by the JUDGE from the summary artifacts. No kill conditions fire — the candidate passes every candidate-facing bar on all 3 seeds. Per courier packet §5.2, INSTRUMENT FAILURE means the test apparatus is broken, not that the candidate failed; L3 is unscoreable on seed 303; L1/L5/L6 results and L3 PASS on seeds 301/302 are valid scored evidence.

**Cross-run consistency:** The V4.4 systemic closure resolved the first scoring run's L1 shuffled-arm false-positive (INSTRUMENT_FAILURE on seeds 201/203) by replacing the two-sided band with a one-sided upper-tail null-of-the-max test. L1 now PASSES on all 3 fresh seeds. However, the V4.4 L3 frozen-arm calibrated stochastic test (which replaced the V4.2 unproved "reduction_h ≤ 0%" check) caught a borderline instrument failure on seed 303. The candidate mechanism itself passes all candidate-facing bars on all seeds in both scoring runs.

**Flagged issues (non-blocking, for CRITIC/RECORDER):**

1. **Reproducibility failure (bit_identical = False):** The `--verify-reproducibility` second pass found non-identical non-timing fields. The returned summary artifacts do not localize which fields differ. The JUDGE cannot certify reproducibility. This does not change the headline verdict (L3 INSTRUMENT_FAILURE is governing) but is a failed reproducibility check that requires CRITIC investigation. The CRITIC should request the harness's internal diff log or pass-specific outputs to identify the differing fields.

2. **Phase B raw-artifact recomputation not completed:** The V4.4 spec §7.2 requires the JUDGE to "recompute observed statistics, every null statistic, maxima/departures, exceed/tie counts, plus-one p-values, exact predicates, per-family verdicts, and cross-run consistency" from returned raw artifacts. The 257,636 raw artifact files (16.3 GB) are retained locally on Rebecca's system and available on request. The JUDGE verified p-values from the integer `exceed_or_tie_count` fields in the summary artifacts (NB1 from CRITIC clearance), which is sufficient for the decisive verdict. Full raw-artifact recomputation remains outstanding.

3. **Seed ledger scope label:** `scope` field still says "M3 development diagnostics only" despite `run_type: scoring` and `pool: M3_fresh_supervised_scoring`. Stale label.

4. **Manifest stale wording:** `r3_note` and `scoring_seed_pool` use "development" boilerplate despite `mode: scoring`.

**Per O-14, no re-run without Rebecca's fresh sign-off and a CRITIC-confirmed construction-bug diagnosis. Per §5.2, L1/L5/L6 results and L3 PASS on seeds 301/302 are valid scored evidence.**

**This run is INSTRUMENT FAILURE.**
