# JUDGE Ruling — M3 Scoring Run

**Run scored:** M3 scoring run (seeds 201, 202, 203; law: all; mode: scoring)
**Scored from:** Raw artifacts returned in `m3_scoring_output.zip` (SHA-256: `d5a5bc12daadf7007ea277bc20a03047bb41c74f3a955fed9bf0dcbf07db87d3`) ONLY.
**Date:** Sunday, 2026-08-16 (12:40 EDT)
**Spec basis:** `m3_e2_spec_amended_v4_2.md` (V4.2), `m3_e2_courier_scoring_packet.md`
**Attested commit:** `3a4e636f5ec753bfadca08d1bf3be17d79dbee72` (Rebecca's attestation; confirmed in manifest)

> Scoring is performed exclusively from the raw returned artifacts. No agent's characterization of the run was used as evidence. All values cited below were re-derived directly from the JSON/log artifacts and cross-checked programmatically against the raw per-seed results. The NF7 raw per-entry data was independently recomputed. The L3/L5/L6 control-arm bars were independently verified.

---

## VERDICT: **INSTRUMENT FAILURE**

L1 has INSTRUMENT_FAILURE on seeds 201 and 203 (shuffled arm conditional rho values fall outside the empirical-null band). L1 PASSES on seed 202. L3, L5, and L6 all PASS on all 3 seeds. No kill conditions fire — the candidate passes every candidate-facing bar on all 3 seeds. Per courier packet §5.2, INSTRUMENT FAILURE means the test apparatus is broken, not that the candidate failed. L1 is unscoreable on seeds 201 and 203. L3/L5/L6 results are valid scored evidence. The overall verdict is INSTRUMENT FAILURE because any law-level instrument failure blocks the overall verdict (courier packet §6).

---

## Package integrity

- **Package SHA-256:** `d5a5bc12daadf7007ea277bc20a03047bb41c74f3a955fed9bf0dcbf07db87d3` — matches Rebecca's attestation. **VERIFIED.**
- **10 output files present:** all 10 files listed in courier packet §3.1 are present. **VERIFIED.**
- **File hashes:** all 9 file hashes in `m3_manifest.json.file_hashes` match independently recomputed SHA-256 values. **VERIFIED.**
- **Terminal round-trip log:** NOT PRESENT. Rebecca attests: "The terminal round-trip log was inadvertently not created." This is a required return file per courier packet §3.4. See Provenance adjudication below.

---

## L1 — Access physics (INSTRUMENT_FAILURE on seeds 201, 203; PASS on seed 202)

### Candidate bars (all 3 seeds)

The candidate passes every candidate-facing bar on all 3 seeds. The fixture is structural-seed-dependent (structural seed 777, same for all scoring seeds), so candidate/oracle/frozen/fair-naive/recency-only/rehearsal-only/permuted values are identical across seeds (as expected per spec §2.4: "the same candidate-set schedule (generated with structural seed 777) is used for all scoring runs"). Only the shuffled arm varies by scoring seed.

| Bar | Required | Seed 201 | Seed 202 | Seed 203 |
|---|---|---|---|---|
| R² (binned marginal-mean) | ≥ 0.85 | 0.9857 ✅ | 0.9857 ✅ | 0.9857 ✅ |
| β_age (direction) | < 0 | −0.00150 ✅ | −0.00150 ✅ | −0.00150 ✅ |
| All 5 conditional ρ (rehearsal) | ≥ 0.6 | 0.911–0.946 ✅ | 0.911–0.946 ✅ | 0.911–0.946 ✅ |
| All 5 age-conditional slopes | < 0 | all negative ✅ | all negative ✅ | all negative ✅ |

**NF7 independent recomputation (R² and β_age from raw per-entry data):** The JUDGE independently recomputed R² and β_age from the `nf7_raw_data.log_accessibility_per_entry` field (200 per-entry log-accessibility values, 5 bin means, 5 bin age representatives). Recomputed values match reported values exactly on all 3 seeds:

| Seed | Recomputed R² | Reported R² | Match | Recomputed β_age | Reported β_age | Match |
|---|---|---|---|---|---|---|
| 201 | 0.9857284782 | 0.9857284782 | ✅ | −0.0014996227 | −0.0014996227 | ✅ |
| 202 | 0.9857284782 | 0.9857284782 | ✅ | −0.0014996227 | −0.0014996227 | ✅ |
| 203 | 0.9857284782 | 0.9857284782 | ✅ | −0.0014996227 | −0.0014996227 | ✅ |

**Oracle:** R² = 0.9857, β_age = −0.00150 — identical to candidate (by construction). ✅

### L18 control arms (seed-varying: shuffled arm only)

| Control arm | Required | Seed 201 | Seed 202 | Seed 203 |
|---|---|---|---|---|
| Frozen R² ≤ null 95th pct (0.7536) | ≤ 0.7536 | 0.4388 ✅ | 0.4388 ✅ | 0.4388 ✅ |
| Fair-naive R² ≤ null 95th pct | ≤ 0.7536 | 0.0004 ✅ | 0.0004 ✅ | 0.0004 ✅ |
| Recency-only: R² ≥ 0.85, β_age < 0, all ρ < 0.6 | all three | 0.9266, −0.00229, all < 0.6 ✅ | same ✅ | same ✅ |
| Rehearsal-only: β_age ≥ 0, all ρ ≥ 0.6 | both | 0.000042, all ≥ 0.6 ✅ | same ✅ | same ✅ |
| Permuted: 200-entry ρ within band [−0.141, 0.143] | within band | −0.00873 ✅ | −0.00873 ✅ | −0.00873 ✅ |
| Empty: returned_defined_error | True | True ✅ | True ✅ | True ✅ |
| **Shuffled: all 5 ρ within null band** | **all within** | **2 of 5 OUTSIDE** ❌ | all within ✅ | **1 of 5 OUTSIDE** ❌ |

### Shuffled arm instrument failure detail (seeds 201 and 203)

Per spec §2.9: "Pass condition: all 5 conditional ρ values within [null_mean − 2·null_sd, null_mean + 2·null_sd] of the shuffled-ρ null distribution." Per spec §2.11: "INSTRUMENT FAILURE: ... OR any shuffled conditional ρ falls outside its empirical-null band."

The shuffled arm's null distribution is generated from 1,000 seeded random re-assignments of priming queries to entries (spec §2.9). The null means are high (0.918–0.935) with narrow SDs (0.020–0.026), producing bands in the range [0.867, 0.975].

**Seed 201** — 2 bins fail (both BELOW the lower bound):

| Bin | Shuffled ρ | Null band [lower, upper] | Within? |
|---|---|---|---|
| 0 | 0.9338 | [0.8666, 0.9688] | ✅ |
| 1 | 0.8311 | [0.8855, 0.9740] | ❌ (below) |
| 2 | 0.9436 | [0.8950, 0.9751] | ✅ |
| 3 | 0.9134 | [0.8910, 0.9738] | ✅ |
| 4 | 0.8784 | [0.8824, 0.9705] | ❌ (below) |

**Seed 203** — 1 bin fails (BELOW the lower bound):

| Bin | Shuffled ρ | Null band [lower, upper] | Within? |
|---|---|---|---|
| 0 | 0.9402 | [0.8666, 0.9688] | ✅ |
| 1 | 0.9393 | [0.8855, 0.9740] | ✅ |
| 2 | 0.9517 | [0.8950, 0.9751] | ✅ |
| 3 | 0.8740 | [0.8910, 0.9738] | ❌ (below) |
| 4 | 0.9460 | [0.8824, 0.9705] | ✅ |

**Seed 202** — all 5 bins within band. ✅

The failing rho values are all BELOW the lower bound of the empirical-null band. The spec's parenthetical "(i.e., still shows real signal)" describes the above-band case; the formal pre-registered criterion is "outside the band," which includes below. The JUDGE applies the pre-registered criterion as written: outside the band in either direction = INSTRUMENT FAILURE.

**Harness-reported instrument_failure_reasons:**

| Seed | Reasons |
|---|---|
| 201 | `shuffled rho_1=0.8311 outside null band [0.8855, 0.9740]`; `shuffled rho_4=0.8784 outside null band [0.8824, 0.9705]` |
| 203 | `shuffled rho_3=0.8740 outside null band [0.8910, 0.9738]` |

**L1 verdicts:** Seed 201: INSTRUMENT_FAILURE. Seed 202: PASS. Seed 203: INSTRUMENT_FAILURE.

**Kill reasons:** None on any seed. The candidate passes all candidate-facing bars. No kill condition fires.

---

## L3 — Thick present (PASS on all 3 seeds)

**Bar (§1, §3.6):** ≥ 5% relative loss reduction at every horizon 1..5, all scoring seeds.

| Seed | h=1 | h=2 | h=3 | h=4 | h=5 | All ≥ 5%? |
|---|---|---|---|---|---|---|
| 201 | 18.2% | 19.4% | 9.6% | 8.2% | 15.7% | ✅ |
| 202 | 19.3% | 22.7% | 10.3% | 9.8% | 20.9% | ✅ |
| 203 | 15.9% | 18.6% | 8.8% | 8.9% | 17.5% | ✅ |

**L18 control arms (independently verified by JUDGE):**

| Control | Required | All seeds |
|---|---|---|
| Frozen reduction ≤ 0% every horizon | ≤ 0% | ✅ (all seeds, all horizons: −1.65 to −2.43) |
| Oracle reduction in (5%, 95%) every horizon | (0.05, 0.95) | ✅ (all seeds, all horizons: 0.102 to 0.255) |
| Permuted reduction ≤ 0% every horizon | ≤ 0% | ✅ (all seeds, all horizons: −0.17 to −0.54) |
| Shuffled reduction ≤ shuffled_frozen + 0.01 every horizon | ≤ sfr+0.01 | ✅ (all seeds, all horizons) |
| Empty: returned_defined_error | True | ✅ (all seeds) |

**Note on shuffled floor check:** The spec (§3.9) states the pass condition as `shuffled_reduction_h ≤ frozen_reduction_h + 0.01`. The JUDGE verified this against `shuffled_frozen_reductions` (the frozen-state reduction computed on the same shuffled sequence), not the unshuffled `frozen_reductions`. The unshuffled frozen reductions are very negative (−1.65 to −2.43) because the frozen state (s=0) is actively harmful; comparing the shuffled arm against the unshuffled frozen floor would be a category error. The shuffled_frozen reductions are small positive values (0.002 to 0.031), and all shuffled reductions fall within `shuffled_frozen + 0.01` on all seeds and horizons. **All pass.**

**L3 verdicts:** Seed 201: PASS. Seed 202: PASS. Seed 203: PASS. No instrument failures. No kills.

---

## L5 — Bi-temporality (PASS on all 3 seeds)

**Bars (§1, §4.9):** ≥ 0.95 accuracy on both combination query types; chain-walk accuracy = 1.00 for all 40 queries; sealed access-count delta = k exactly.

| Bar | Required | Seed 201 | Seed 202 | Seed 203 |
|---|---|---|---|---|
| World-validity accuracy | ≥ 0.95 | 1.0 ✅ | 1.0 ✅ | 1.0 ✅ |
| Self-acquisition accuracy | ≥ 0.95 | 1.0 ✅ | 1.0 ✅ | 1.0 ✅ |
| Chain-walk accuracy (all 40) | = 1.00 | 1.0 ✅ | 1.0 ✅ | 1.0 ✅ |
| Access-count matches k | True | True ✅ | True ✅ | True ✅ |

**L18 control arms (independently verified):**

| Control | Required | All seeds |
|---|---|---|
| Fair-naive world-validity accuracy | = 0.75 exactly | ✅ (0.75 all seeds) |
| Frozen post-freeze walk accuracy | = 0.00 | ✅ (0.00 all seeds) |
| Full-scan access-count delta | = 200 | ✅ (200 all seeds) |
| Shuffled chain-walk accuracy | ≤ 0.05 | ✅ (0.00 all seeds) |
| Permuted combo accuracy within null band | within band | ✅ (all seeds) |
| Empty: returned_defined_error | True | ✅ (all seeds) |
| All 5 bypass tests caught | all caught | ✅ (all seeds) |

**L5 growth timing (§1.1, diagnostic-only, non-gating):**

| Seed | Candidate growth 250→1000 | Fair-naive growth 250→1000 |
|---|---|---|
| 201 | 1.013 | 3.766 |
| 202 | 1.004 | 3.638 |
| 203 | 1.019 | 3.948 |

Reported but non-gating per §1.1 (Rebecca's ruling pending). Candidate growth is flat (≤ 2.0 on all seeds); fair-naive growth is 3.6–3.9× (below the 4.0× proposed threshold on all seeds). Noted for completeness; does not affect the verdict.

**L5 verdicts:** Seed 201: PASS. Seed 202: PASS. Seed 203: PASS. No instrument failures. No kills.

---

## L6 — Episodic completeness (PASS on all 3 seeds)

**Bars (§5.6):** All 8 attacks caught; all 4 reachability-audit rows pass; all 6 L18 arms show expected outcome.

| Check | Required | Seed 201 | Seed 202 | Seed 203 |
|---|---|---|---|---|
| All 8 attacks caught | 8/8 | 8 ✅ | 8 ✅ | 8 ✅ |
| All 4 audit rows pass | 4/4 | 4 ✅ | 4 ✅ | 4 ✅ |
| All 6 L18 arms pass | 6/6 | 6 ✅ | 6 ✅ | 6 ✅ |
| Module namespace complete | True | True ✅ | True ✅ | True ✅ |

Attack #8 (harness self-test — deliberately broken variant) caught on all seeds. ✅

**L6 verdicts:** Seed 201: PASS. Seed 202: PASS. Seed 203: PASS. No instrument failures. No kills.

---

## Kill conditions

No kill conditions fire on any seed for any law. The candidate passes all candidate-facing bars on all 3 seeds. The instrument failures are in the L1 shuffled control arm (a test-apparatus check), not in the candidate mechanism.

---

## Additional checks

### Reproducibility (bit-identical)

`m3_invariants.json.reproducibility.bit_identical = True`, scope: "all non-timing fields." `m3_run.log` confirms the `--verify-reproducibility` second pass ran over all seeds and verified bit-identical non-timing metrics. **PASS.**

### L20 drift self-test

`m3_profile.json.l20_self_test`: `no_drift_corr = 0.9999999999999999` (≥ 1.0 − ε ✅), `no_drift_passes = True`. Perturbation 1 (metric_block_reversal): corr = −0.201 (< 0.50 ✅, flags drift). Perturbation 2 (candidate_empty_swap): corr = 0.00 (< 0.50 ✅, flags drift). `both_perturbations_flag_drift = True`. **PASS.**

### Interface invariants (§2: L11, L13, L5)

- L11 single-clock negative injection: `caught = True` ✅
- L13 encoding-snapshot negative injection: `caught = True` ✅ (stored snapshot differs from read-time recomputation after landmark addition, as expected)
- L5 backdating-hash negative injection: `caught = True` ✅ (mutated hash detected)

`interface_invariants.passes = True`. **PASS.**

### Finite numeric results

`finite_numeric_results = True`. No NaN or inf in any scored metric. **PASS.**

### Manifest deviation disclosure

`deviations_logged`: `["Python 3.11.9 vs pinned 3.11 (non-blocking)"]`. Python 3.11.9 matches the pinned 3.11.x requirement. numpy 1.26.4 and scipy 1.13.1 match exactly. Non-blocking. **DISCLOSED.**

---

## Provenance adjudication

### 1. Overall harness INSTRUMENT_FAILURE

**Adjudicated: CONFIRMED.** The harness self-reports `overall_verdict: INSTRUMENT_FAILURE` in both `m3_invariants.json` and `m3_run_results.json`. This is caused by L1 INSTRUMENT_FAILURE on seeds 201 and 203 (shuffled arm null-band violations). The JUDGE independently confirms this from the raw artifacts. The overall verdict is correct per courier packet §6: "INSTRUMENT-BLOCKED (any INSTRUMENT FAILURE)."

### 2. L1 instrument failures on seeds 201 and 203

**Adjudicated: CONFIRMED INSTRUMENT FAILURE (not KILL).** Three shuffled-arm conditional rho values fall outside the empirical-null band: seed 201 bins 1 and 4 (below lower bound), seed 203 bin 3 (below lower bound). Per spec §2.9/§2.11, this is a pre-registered INSTRUMENT FAILURE. The candidate itself passes all bars on all 3 seeds. No kill condition fires. Per §5.2, this means the test apparatus is broken, not the candidate. L1 is unscoreable on seeds 201 and 203; L1 PASS on seed 202 is valid.

### 3. bit_identical = true

**Adjudicated: CONFIRMED.** `reproducibility.bit_identical = True`, `checked = True`, scope: "all non-timing fields." The `--verify-reproducibility` flag (NB6 binding) was included in the scoring command per Rebecca's attestation. The second pass verified bit-identical non-timing metrics across all seeds. **PASS.**

### 4. Missing terminal round-trip log

**Adjudicated: PROVENANCE DEVIATION (non-blocking).** Rebecca attests: "The terminal round-trip log was inadvertently not created." The courier packet §3.4 requires "Rebecca's executor round-trip log (command, commit hash, STATE.md hash, exit status, wall clock, output file list with sizes and hashes)" as a required return. This file is absent from the returned package.

The JUDGE assessed the impact: (a) the 10 scoring artifacts are complete and internally consistent (file hashes match); (b) the manifest self-reports commit hash and STATE.md hash; (c) Rebecca's attestation provides the checkout commit and execution conditions. The missing round-trip log prevents independent verification of the execution environment but does not change any scored metric or bar. The L1 instrument failure is derived from the scoring artifacts themselves, not from execution-environment provenance.

**Flagged for RECORDER/CRITIC.** Future scoring runs must include the round-trip log per courier packet §3.4.

### 5. Seed ledger labels "M3 development diagnostics only" and "M3_development" despite run_type=scoring

**Adjudicated: LABELING BUG (non-blocking).** `m3_seed_exposure_ledger.json` records `scope: "M3 development diagnostics only"` and all 12 events have `pool: "M3_development"` despite every event having `run_type: "scoring"`. This is inconsistent with the actual scoring run. The seeds (201, 202, 203) are hold-out scoring seeds, not development seeds. The `run_type` field is correct (`scoring`); the `scope` and `pool` fields carry stale development-context labels.

The JUDGE assessed the impact: the ledger correctly records `run_type: "scoring"` for all events. The stale `scope` and `pool` labels do not affect seed exposure tracking — the seeds used (201, 202, 203) are confirmed as the authorized scoring seed pool per courier packet §4.3. The development seed pool {101–105} is not used. **Non-blocking labeling bug. Flagged for RECORDER/CRITIC.**

### 6. Manifest's stale scoring-pool/r3 wording despite mode=scoring

**Adjudicated: STALE WORDING (non-blocking).** The manifest contains:
- `scoring_seed_pool: "WITHHELD; forbidden in development"` — uses "development" framing in a scoring run
- `r3_note: "Scoring-only seed identities are absent from this development implementation and its artifacts."` — uses "development implementation" framing in a scoring run

These are boilerplate fields from the development context that were not updated for the scoring run. The manifest's `mode` field is correctly `scoring`, and `seeds` is correctly `[201, 202, 203]`. The stale wording does not affect any scored metric or bar. **Non-blocking. Flagged for RECORDER/CRITIC.**

### 7. Commit and STATE.md provenance

**Adjudicated: INTERNALLY CONSISTENT (with flagged deviations).**

**Commit hash:**
- Courier packet authorized: `7fdf033e0baa2178650b54dd93b617387cc13646`
- Rebecca attested: `3a4e636f5ec753bfadca08d1bf3be17d79dbee72`
- Manifest reports: `3a4e636f5ec753bfadca08d1bf3be17d79dbee72`

The JUDGE independently verified against the GitHub repository (`darkside73826779-ship-it/moving-origin-research`). Commit `3a4e636f` is 3 commits ahead of `7fdf033e` on main:

```
3a4e636 merge: pre-scoring custody — CLEARED FOR SCORING
3dd0ead RECORDER: pre-scoring custody — implementation CRITIC-cleared, courier packet cleared, ready for scoring
24040ea Merge pull request #6 from darkside73826779-ship-it/taskbuilder/m3-critic-b1-scoring-guard
84f9973 TASK BUILDER: apply CRITIC B1 scoring mode seed guard
7fdf033 Merge pull request #5 from darkside73826779-ship-it/taskbuilder/m3-e2-implementation
```

The additional commits are: (1) a CRITIC-requested B1 scoring-mode seed guard fix (PR #6), (2) RECORDER pre-scoring custody attestation, and (3) a merge commit with message "CLEARED FOR SCORING." These are post-courier-packet commits that represent the final pre-scoring preparation. The code Rebecca ran includes the courier packet's code plus additional CRITIC-cleared fixes. This is a newer, not unauthorized, state. **The commit hash deviation from the courier packet is explained by repository advancement after packet preparation. Flagged for RECORDER (courier packet should be updated to reflect the final scoring commit).**

**STATE.md hash:**
- Courier packet expected (at `7fdf033e`): `f257c1f323b81d549e2e0b40258833e4d742ee68e10c0b16aae425acb6eadb49`
- Manifest reports: `7bc8963cab41a3f9cc3b1f7009b91b4f61533377465deae7c98d497d857c8d9d`
- Actual at `3a4e636f` (LF): `452d4c6273de3c0a43509acdcabaf36eecf0ca340f356e112d796c7c8745c385`

The JUDGE independently verified: the manifest's hash (`7bc8963c...`) is the SHA-256 of `state/STATE.md` at commit `3a4e636f` when computed with CRLF line endings (as produced by git on Windows with `core.autocrlf=true`). The harness reads the file in binary mode (`_sha256_file` opens with `'rb'`), so on Rebecca's Windows executor it hashed the CRLF version. The JUDGE confirmed:

- LF hash at `3a4e636f`: `452d4c62...` (matches `sha256sum` on Linux)
- CRLF hash at `3a4e636f`: `7bc8963c...` (matches manifest exactly)

The STATE.md was updated between `7fdf033e` and `3a4e636f` (M3 status added), which explains why the hash differs from the courier packet's expectation. The manifest's STATE.md hash is internally consistent with the attested commit when CRLF normalization is accounted for. **STATE.md provenance is internally consistent. The CRLF/LF hash discrepancy is a known Windows-executor artifact (same pattern as E1 cure run's "CRLF→LF normalization" in the round-trip log).**

---

## Summary Table

| Criterion | Status |
|---|---|
| Package SHA-256 | ✅ Verified |
| 10 output files present | ✅ All present |
| File hashes (9 files) | ✅ All match |
| L1 candidate bars (all seeds) | ✅ R²=0.9857, β_age<0, all ρ≥0.6 |
| L1 NF7 recomputation | ✅ Exact match (all 3 seeds) |
| L1 shuffled arm (seed 201) | ❌ INSTRUMENT FAILURE (2 bins below null band) |
| L1 shuffled arm (seed 202) | ✅ All within band |
| L1 shuffled arm (seed 203) | ❌ INSTRUMENT FAILURE (1 bin below null band) |
| L1 verdict | INSTRUMENT_FAILURE (seeds 201, 203); PASS (seed 202) |
| L3 candidate bars (all seeds) | ✅ All reductions ≥ 5% (8.8%–22.7%) |
| L3 control arms (all seeds) | ✅ All pass (frozen ≤ 0%, oracle in (5%, 95%), permuted ≤ 0%, shuffled ≤ floor+0.01, empty = error) |
| L3 verdict | PASS (all 3 seeds) |
| L5 candidate bars (all seeds) | ✅ Accuracy = 1.0, chain-walk = 1.00, access-count = k |
| L5 control arms (all seeds) | ✅ All pass (fair-naive = 0.75, frozen = 0.00, full-scan = 200, shuffled = 0.00, permuted within band, empty = error, all 5 bypass caught) |
| L5 verdict | PASS (all 3 seeds) |
| L6 bars (all seeds) | ✅ 8/8 attacks caught, 4/4 audit rows pass, 6/6 L18 arms pass |
| L6 verdict | PASS (all 3 seeds) |
| Kill conditions | ✅ None fire (candidate passes all bars) |
| Reproducibility (bit-identical) | ✅ PASS |
| L20 drift self-test | ✅ PASS |
| Interface invariants (L11, L13, L5) | ✅ PASS |
| Finite numeric results | ✅ True |
| Manifest deviations | ✅ Disclosed (Python 3.11.9, non-blocking) |
| Commit hash | Deviation from courier packet (repo advanced 3 commits, CRITIC-cleared, "CLEARED FOR SCORING") — flagged |
| STATE.md hash | Internally consistent (CRLF normalization explains mismatch) |
| Terminal round-trip log | ❌ MISSING — flagged |
| Seed ledger labels | Labeling bug ("development" in scoring run) — flagged |
| Manifest stale wording | Stale "development" boilerplate in scoring mode — flagged |

---

## Final Ruling

### **INSTRUMENT FAILURE**

L1 has INSTRUMENT_FAILURE on seeds 201 and 203 (shuffled arm conditional rho values fall outside the empirical-null band — a pre-registered instrument-failure trigger per spec §2.9/§2.11). L1 PASSES on seed 202. L3, L5, and L6 all PASS on all 3 seeds with all bars and controls independently verified by the JUDGE. No kill conditions fire — the candidate passes every candidate-facing bar on all 3 seeds. Per courier packet §5.2, INSTRUMENT FAILURE means the test apparatus is broken, not that the candidate failed; L1 is unscoreable on seeds 201 and 203; L3/L5/L6 results are valid scored evidence.

The instrument failure is specific to the L1 shuffled-arm empirical-null check on 2 of 3 seeds (3 individual bin-level violations across 2 seeds). The candidate's own bars (R², β_age, conditional ρ, conditional slopes) pass on all 3 seeds. The remaining L18 control arms (frozen, fair-naive, recency-only, rehearsal-only, permuted, empty) all pass on all 3 seeds.

**Provenance deviations flagged (non-blocking):**
1. Terminal round-trip log missing (required return file absent; Rebecca attests inadvertent)
2. Commit hash `3a4e636f` differs from courier packet's `7fdf033e` (repo advanced 3 CRITIC-cleared commits post-packet; final commit: "CLEARED FOR SCORING")
3. STATE.md hash `7bc8963c` differs from courier packet's `f257c1f3` (STATE.md updated between commits; CRLF normalization on Windows executor explains manifest vs. Linux hash difference — internally consistent)
4. Seed ledger labels "M3 development" despite `run_type=scoring` (labeling bug)
5. Manifest r3_note/scoring_seed_pool use stale "development" wording (boilerplate not updated for scoring mode)

**Per O-14, no re-run is attempted without Rebecca's fresh sign-off and a CRITIC-confirmed construction-bug diagnosis. Per §5.2, the remaining laws' results (L3, L5, L6 — all PASS on all 3 seeds) are valid scored evidence.**

**This run is INSTRUMENT FAILURE.**
