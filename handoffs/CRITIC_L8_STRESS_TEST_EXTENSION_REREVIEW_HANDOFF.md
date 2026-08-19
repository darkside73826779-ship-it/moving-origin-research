# CRITIC Handoff — Return to WORKFLOW COORDINATOR: L8 §8 Stress-Test Extension Re-Review

**From:** CRITIC (fresh-context, focused re-review of the extension)
**To:** WORKFLOW COORDINATOR
**Date:** 2026-08-19 15:26 EDT
**Gate served:** CRITIC re-review of the §8 misspecification stress-test extension (NF-IMPL-4 scope extension)
**Verdict:** **CLEAR**
**Review artifact:** `reviews/critic_l8_stress_test_extension_rereview.md` on `critic/l8-stress-test-extension-rereview` (`ad3a405`)

---

## Authorization context

The CRITIC's prior §8 remediation re-review returned CLEAR but flagged NF-IMPL-4 (non-blocking): the misspec stress-test was partial (8-combo subset, mean-β* stability only). Rebecca chose the full version replicating the scoring run. The TASK BUILDER extended the stress-test to the full 2D sensitivity map + deterministic selection on each misspecified profile. This handoff returns the CRITIC's focused re-review of that extension.

---

## SHAs reviewed

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

---

## Verdict: CLEAR

NF-IMPL-4 is fully resolved. The stress-test now runs, for each of the two misspecified profiles, the full 240-combo 2D sensitivity map + the deterministic selection rule + a selection-stability report against the reference, with both false-kill aggregations, results in the `--full` JSON, and a `--stress-test-sims` runtime parameter. The extension is additive — the estimator, reference pipeline, selection rule, candidate-blindness, R8 guard, and the three prior fixes are all preserved.

---

## The extension — all six requirements verified

1. **Full 2D sensitivity map on each misspecified profile:** `run_power_analysis_misspecified` iterates the full 5×3×4×4 = 240 grid (not a subset), with true-effect arm (false-kill) + null-control arm (false-pass) under the same misspecified profile, three regions, §8.7 sensitivity map. ✓
2. **Deterministic selection rule on each misspecified profile:** `select_cmin_eta` (unmodified) runs on each misspecified profile's map, producing a (C_min, η) selection per profile. ✓
3. **Selection stability report:** compares each misspecified profile's (C_min, η) selection against the reference; reports `selection_matches_reference` and stable/unstable. This was the gap flagged in NF-IMPL-4 — now present. ✓
4. **Both false-kill aggregations on misspecified profiles:** `false_kill_rate` (5-seed mean) and `false_kill_rate_per_seed` (any-seed) both computed and carried into results_summary. ✓
5. **Results in `--full` JSON:** `full["misspecification_stress_test"]` set when `--full`. ✓
6. **`--stress-test-sims` parameter:** default 10000, reducible at runtime; both options flagged (full ~17h, reduced 2000 ~8h). ✓

---

## Candidate-blindness (Ruling 9) — VERIFIED preserved

Misspecified profiles use known oracle ground truth (Uniform / bimodal p_true + Bernoulli); simulation seeds are `combo_seed` hashes (SHA-256 of parameter string, mod 2^31); per-seed seeds derived deterministically from combo seed; σ_dose reused from reference calibration (tests estimator overfit, not re-calibration). No candidate-output path introduced anywhere. ✓

---

## Collateral check — PASS

Delta `61a2f8d...cbe4dfb` touches only `diagnostics/l8_power_analysis.py` (+298/−77) + the new handoff doc. Confirmed unchanged: the estimator (`beta_star_for_seed`, `run_level_beta_star`), the reference-profile pipeline (`run_power_analysis`, `simulate_one_seed/dose`, `simulate_one_simulation`, `calibrate_sigma_dose`), the selection rule (`select_cmin_eta`), `classify_region`/`min_distance_to_boundaries`, `validate_estimator`/`run_validation_batch`, candidate-blindness, the R8 guard (`src/e1_experiment.py` — empty diff), and the three prior fixes (NF-IMPL-1 relative path not reverted; NF-IMPL-2 both aggregations extended to misspecified profiles; NF-IMPL-3 table not affected). The extension introduces `run_power_analysis_misspecified` and rewrites `run_misspecification_stress_test` to use it — both additive, no protected function modified.

---

## Non-blocking observations (trivial — no action required for clearance)

- **NF-EXT-1 (trivial):** Step 4 is no longer gated by `--full` and defaults to 10000 sims, so a bare invocation would trigger the full stress-test (~17h). Rebecca uses `--full`/`--stress-test-sims` per the handoff. Could optionally gate Step 4 behind a flag.
- **NF-EXT-2 (trivial):** `run_power_analysis_misspecified` (like `simulate_one_simulation`) recomputes per-seed β*_s via a second `beta_star_for_seed` call after `run_level_beta_star` already computed them internally — redundant but not incorrect (identical values).

---

## P3 / P6 compliance

- **P3 (source-class tags):** PASS. New thresholds/functions tagged (`[Sol-XF-9]`, `[PROPOSED — apparatus parameter, §8 item 9]`); per-seed false-kill tagged `[NF-IMPL-2, PROPOSED — flagged to Rebecca]`.
- **P6 (provenance citations):** PASS. `[Sol-XF-9]`, `[Entry 76]`, `[BAR-Entry 11]` consistent with the provenance log and spec.

---

## Locked bars preserved

Yes. `BETA_STAR_BAR = 0.2 [BAR-Entry 11]` remains an input to the false-kill calculation (both aggregations, reference and misspecified profiles), never an output. `N_SEEDS = 5 [BAR-Entry 11]` preserved. No L8 locked bar (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds) changed. R8 guard untouched. No negative result or INSTRUMENT_FAILURE label renamed or reinterpreted.

---

## Preserved evidence

The §2 XF-5 estimator, the reference-profile pipeline, the deterministic selection rule, candidate-blindness, the R8 guard, the estimator validation (Examples A/B), and the three prior fixes (NF-IMPL-1/2/3) are all preserved and verified. The prior CLEAR's positive verifications remain valid. The extension is additive and does not invalidate any prior evidence.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this handoff artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, code-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the code, spec, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No running of the full simulation (deferred to Rebecca's local run after clearance).
- No L15/L16/L17 before M5.
- No renaming or reinterpreting any negative result or INSTRUMENT_FAILURE label.
- No touching the estimator, the reference-profile pipeline, the selection rule, the R8 guard, or the three applied fixes (all confirmed unchanged).

---

## Next authorized role / routing

**Next recipient:** WORKFLOW COORDINATOR. On CLEAR, Rebecca runs `python diagnostics/l8_power_analysis.py --full [--stress-test-sims N]` locally, producing the reference sensitivity map + misspecification stability report that feed her G2–G5 gate rulings (G1 already resolved by Entry 81). Rebecca should also rule on the NF-IMPL-2 false-kill aggregation (which is the G3-escalation input). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On BLOCK (not the case), returns to TASK BUILDER.

---

*This handoff was produced read-only against the code at `cbe4dfb` on `taskbuilder/l8-power-analysis` and the spec at `c7d7bed`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
