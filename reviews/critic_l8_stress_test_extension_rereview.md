# CRITIC Re-Review — L8 §8 Stress-Test Extension (NF-IMPL-4)

**Gate served:** CRITIC re-review of the §8 misspecification stress-test extension (NF-IMPL-4 scope extension)
**Reviewer:** CRITIC (fresh-context, focused re-review of the extension)
**Date:** 2026-08-19 15:21 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — on CLEAR, Rebecca runs the full simulation locally (`python diagnostics/l8_power_analysis.py --full [--stress-test-sims N]`), producing the reference sensitivity map + misspecification stability report feeding her G2–G5 gate rulings.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Code branch | `taskbuilder/l8-power-analysis` |
| Extended HEAD (under review) | `cbe4dfb` (extension commit `5343fc9` + handoff `cbe4dfb`) |
| Prior version (CRITIC-cleared remediation) | `61a2f8d` |
| Delta reviewed | `61a2f8d...cbe4dfb` — `diagnostics/l8_power_analysis.py` +298/−77; handoff doc |
| §8 power analysis code | `diagnostics/l8_power_analysis.py` (1435 lines, was 1214) |
| L8 spec v2.2 (frozen) | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` at `c7d7bed` — §8 item 9 |
| Prior CRITIC reviews | `critic_l8_s8_implementation_review.md` (`60d0a90`); `critic_l8_s8_remediation_rereview.md` (`0da3953`) |

Read-only review. No code, spec, constitution, or scoring artifact modified (read-only + this review file). No scoring, seed execution, hold-out seed exposure, full simulation run, or unauthorized merge performed.

---

## Headline finding (CLEAR)

The NF-IMPL-4 non-blocking observation is fully resolved. The stress-test now runs, for each of the two misspecified profiles, the **full 240-combo 2D sensitivity map + the deterministic selection rule + a selection-stability report against the reference**, with both false-kill aggregations, results in the `--full` JSON, and a `--stress-test-sims` runtime parameter. The extension is additive: it introduces `run_power_analysis_misspecified` (mirroring `run_power_analysis` but using `simulate_one_seed_misspecified`) and rewrites `run_misspecification_stress_test` to use it. The estimator, the reference-profile pipeline, the deterministic selection rule, candidate-blindness, the R8 guard, and the three prior fixes (NF-IMPL-1/2/3) are all preserved.

---

## The extension — verified against the handoff's six requirements

1. **Full 2D sensitivity map on each misspecified profile — VERIFIED.** `run_power_analysis_misspecified(profile_name, n_sims)` iterates the complete grid `for alpha in ALPHAS: for v_mult in V_MULTS: for c_min in C_MINS: for eta in ETAS` — the full 5×3×4×4 = 240 combinations, not a subset. It computes both the true-effect arm (false-kill) and the null-control arm (σ_dose=0.0, false-pass) under the same misspecified profile, classifies the three regions via `classify_region`, and builds the §8.7 sensitivity map (cells over (C_min, η), aggregated across (α, v) pairs). ✓

2. **Deterministic selection rule on each misspecified profile — VERIFIED.** `selection = select_cmin_eta(sensitivity_map)` runs the identical §8.8 selection rule (informative → max min-distance → highest C_min → lowest η) on each misspecified profile's sensitivity map, producing a (C_min, η) selection per profile. `select_cmin_eta` is called unmodified (the code comment notes "not modified here per constraints"). ✓

3. **Selection stability report — VERIFIED.** `run_misspecification_stress_test` accepts `reference_selection` (passed from `full.get("selection")` in `main` when `--full`), normalizes both the reference and each misspecified profile's selection via `_flat_sel`, and reports `selection_matches_reference` (True iff both C_min and η match) plus `assessment` = "stable"/"unstable" (or "no_reference" if no reference was passed). This is the selection-stability report the prior review flagged as missing — now present. ✓

4. **Both false-kill aggregations on misspecified profiles — VERIFIED.** `run_power_analysis_misspecified` computes both `false_kill_rate` (5-seed mean: P(mean of 5 < 0.2)) and `false_kill_rate_per_seed` (any-seed: P(any of 5 < 0.2) via `np.any(..., axis=1)`), and both are carried into the `results_summary` of the stress-test output. ✓ (NF-IMPL-2 extended to the misspecified profiles.)

5. **Results in the `--full` JSON — VERIFIED.** `full["misspecification_stress_test"] = misspec` (set when `--full`). ✓ (L19 publication.)

6. **`--stress-test-sims` parameter — VERIFIED.** Added to the argument parser, default 10000, reducible at runtime. The Step-4 note flags both options: "full 10,000 per combo triples total runtime (~17h). Use --stress-test-sims 2000 for ~8h." ✓ Consistent with the handoff's stated options (full ~17h, reduced ~8h).

---

## Candidate-blindness (Ruling 9) — VERIFIED preserved

The extended stress-test remains candidate-blind:
- Misspecified profiles (`uniform_difficulty`: p_true ~ Uniform(0,1); `bimodal_difficulty`: 50% p=0.9 / 50% p=0.3) use known oracle ground truth with Bernoulli realizations — no candidate output. ✓
- Simulation seeds are `combo_seed(alpha, v_mult, c_min, eta)` (SHA-256 of the canonical parameter string, mod 2^31); per-seed seeds are `base_seed + i*N_SEEDS + s` mod 2^31 — deterministic functions of the parameter combo only, never candidate data. ✓
- σ_dose is reused from the reference calibration (`calibrate_sigma_dose`); the test probes whether the estimator is overfit to the reference profile, not re-calibrating from candidate output. ✓
- **No candidate-output path is introduced anywhere in the extended stress-test.** ✓

---

## Collateral check — PASS

Diff `61a2f8d...cbe4dfb` touches only:
- `diagnostics/l8_power_analysis.py` (+298/−77)
- `handoffs/TASKBUILDER_L8_STRESS_TEST_EXTENSION_HANDOFF.md` (new)

Confirmed unchanged (the extension is additive; the diff introduces `run_power_analysis_misspecified` and rewrites `run_misspecification_stress_test`; no protected function is modified):
- **The estimator (§2 XF-5)** — `beta_star_for_seed`, `run_level_beta_star` unmodified. ✓
- **The reference-profile pipeline** — `run_power_analysis`, `simulate_one_seed`, `simulate_dose`, `simulate_one_simulation`, `calibrate_sigma_dose` unmodified. ✓
- **The deterministic selection rule** — `select_cmin_eta` unmodified; called on misspecified-profile maps as-is. ✓
- **`classify_region`, `min_distance_to_boundaries`** — unmodified. ✓
- **`validate_estimator`, `run_validation_batch`** — unmodified. ✓
- **Candidate-blindness (Ruling 9)** — preserved (above). ✓
- **R8 guard (`src/e1_experiment.py`)** — confirmed untouched (empty diff). ✓
- **NF-IMPL-1 (relative path)** — not reverted; `out_path` default remains `diagnostics/l8_power_analysis_results.json`. ✓
- **NF-IMPL-2 (both false-kill aggregations)** — not reverted; extended to the misspecified profiles. ✓
- **NF-IMPL-3 (regenerated validation table)** — not affected by this delta. ✓

---

## Scope check — PASS

The TASK BUILDER's extension commits touch only `diagnostics/l8_power_analysis.py` and the new handoff doc. No spec, constitution, STATE.md, provenance log, R8 guard, or scoring artifact was modified. Scope is confined to the named files.

---

## §5 P3 / P6 compliance

- **P3 (source-class tags):** PASS. New thresholds and functions in the extension carry tags (`[Sol-XF-9]`, `[PROPOSED — apparatus parameter, §8 item 9]`); the per-seed false-kill field is tagged `[NF-IMPL-2, PROPOSED — flagged to Rebecca]`. All pre-existing tags retained.
- **P6 (provenance citations):** PASS. `[Sol-XF-9]`, `[Entry 76]`, `[BAR-Entry 11]` citations consistent with the provenance log and spec.

---

## Locked bars preserved

Yes. `BETA_STAR_BAR = 0.2 [BAR-Entry 11]` remains an input to the false-kill calculation (both aggregations, on reference and misspecified profiles), never an output. `N_SEEDS = 5 [BAR-Entry 11]` preserved. No L8 locked bar (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds) changed. R8 guard untouched. No negative result or INSTRUMENT_FAILURE label renamed or reinterpreted (zero-variance → INSTRUMENT_FAILURE preserved).

---

## Preserved evidence

The §2 XF-5 estimator, the reference-profile pipeline, the deterministic selection rule, candidate-blindness, the R8 guard, the estimator validation (Examples A/B), and the three prior fixes (NF-IMPL-1/2/3) are all preserved and verified. The prior CLEAR's positive verifications remain valid. The extension is additive and does not invalidate any prior evidence.

---

## Non-blocking observations (trivial — no action required)

- **NF-EXT-1 (trivial — Step 4 runs unconditionally):** Step 4 (`run_misspecification_stress_test`) is no longer gated by `--full` and defaults to `--stress-test-sims 10000`, so a bare `python diagnostics/l8_power_analysis.py` invocation would now trigger the full stress-test (2 profiles × 240 combos × 10000 sims ≈ 17h). Rebecca will invoke with `--full` (and optionally `--stress-test-sims`) per the handoff, so this is a usability note, not a defect. If desired, the TASK BUILDER could gate Step 4 behind `--full` or a `--stress-test` flag. No action required for clearance.
- **NF-EXT-2 (trivial — redundant per-seed recomputation):** `run_power_analysis_misspecified` (like `simulate_one_simulation`) recomputes per-seed β*_s via a second `beta_star_for_seed(d_all[s])` call after `run_level_beta_star` already computed them internally and discarded them. This is redundant (the estimator runs twice per seed) but not incorrect — it produces identical values. No action required for clearance.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, code-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the code, spec, constitution, or any artifact (read-only + this review file).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No running of the full simulation (deferred to Rebecca's local run after clearance).
- No L15/L16/L17 before M5.
- No renaming or reinterpreting any negative result or INSTRUMENT_FAILURE label.
- No touching the estimator, the reference-profile pipeline, the selection rule, the R8 guard, or the three applied fixes (all confirmed unchanged).

---

## Verdict and routing

**Verdict: CLEAR.** NF-IMPL-4 is fully resolved: the stress-test now runs the full 240-combo 2D sensitivity map + the deterministic selection rule + a selection-stability report against the reference on each of the two misspecified profiles, with both false-kill aggregations, results in the `--full` JSON, and a `--stress-test-sims` runtime parameter. The extension is additive — the estimator, reference pipeline, selection rule, candidate-blindness, R8 guard, and the three prior fixes are all preserved. Two trivial non-blocking observations (Step 4 not gated by `--full`; redundant per-seed recomputation) require no action for clearance.

**Next authorized role:** WORKFLOW COORDINATOR. On CLEAR, Rebecca runs `python diagnostics/l8_power_analysis.py --full [--stress-test-sims N]` locally, producing the reference sensitivity map + misspecification stability report that feed her G2–G5 gate rulings (G1 resolved by Entry 81). Rebecca should also rule on the NF-IMPL-2 false-kill aggregation (which is the G3-escalation input). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

---

*This review was conducted read-only against the code at `cbe4dfb` on `taskbuilder/l8-power-analysis` and the spec at `c7d7bed`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
