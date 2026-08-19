# CRITIC Re-Review — L8 §8 Remediation (BF-IMPL-1 + NF-IMPL-1/2/3)

**Gate served:** Implementation review remediation — CRITIC re-review of BF-IMPL-1 + NF-IMPL-1/2/3
**Reviewer:** CRITIC (fresh-context, focused re-review of the remediation)
**Date:** 2026-08-19 13:11 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — on CLEAR, Rebecca runs the full simulation locally (`python diagnostics/l8_power_analysis.py --full`), producing the sensitivity map that feeds her G2–G5 gate rulings.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Code branch | `taskbuilder/l8-power-analysis` |
| Remediated HEAD (under review) | `61a2f8d` (fix commit `5c01d34` + handoff `61a2f8d`) |
| Prior version (BLOCK baseline) | `c3a5d49` |
| Delta reviewed | `c3a5d49...61a2f8d` — `diagnostics/l8_power_analysis.py` +209/−10; handoff docs |
| Prior CRITIC review (BLOCK) | `reviews/critic_l8_s8_implementation_review.md` on `critic/l8-s8-implementation-review` (`60d0a90`) — used as defect list |
| L8 spec v2.2 (frozen) | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` at `c7d7bed` — §8 item 9 is the requirement source |
| R8 guard | `src/e1_experiment.py` — confirmed untouched in this remediation |

Read-only review. No code, spec, constitution, or scoring artifact modified (read-only + this review file). No scoring, seed execution, hold-out seed exposure, full simulation run, or unauthorized merge performed.

---

## Headline finding (CLEAR)

All four findings from the prior BLOCK are remediated. The blocking defect (BF-IMPL-1: misspecification stress-test absent) is now implemented — the §8 item 9 requirement is satisfied with two genuinely different misspecified profiles, the identical §2 XF-5 estimator applied to each, false-kill computed, candidate-blindness preserved, and results committed to the `--full` JSON. The three non-blocking fixes (private path, per-seed false-kill, stale validation table) are all resolved. The estimator, the 8 verified §8 protocol items, candidate-blindness, and the R8 guard are all unchanged. **One non-blocking observation (NF-IMPL-4)** remains: the stress-test's stability report is partial — it checks mean-β* stability but does not run the full sensitivity map or assess (C_min, η) selection stability on misspecified profiles. This is flagged to Rebecca, not a block: the spec's literal §8 item 9 requirement is met.

---

## BF-IMPL-1 — misspecification stress-test (blocking) — REMEDIATED

The spec §8 item 9 requires running the power analysis on ≥2 misspecified profiles (different from the synthetic reference) to verify the estimator is not overfit. The code now implements this:

- **Two misspecified profiles**, both genuinely different from the reference (Beta(4.2, 1.8) right-skewed):
  1. `uniform_difficulty`: `p_true ~ Uniform(0,1)` — flat difficulty distribution. ✓ genuinely different
  2. `bimodal_difficulty`: 50% easy (p=0.9), 50% hard (p=0.3) — bimodal vs unimodal. ✓ genuinely different
  - These are non-trivial perturbations (different distribution shapes), not cosmetic. ✓
- **The identical estimator applied to each**: `run_misspecification_stress_test` builds `d_all` from `simulate_one_seed_misspecified` and calls `run_level_beta_star(d_all)` (the identical §2 XF-5 estimator). The estimator is not re-implemented for the stress-test; only the data-generating process changes. ✓
- **False-kill computed per combo per profile**: `fk = mean(valid < BETA_STAR_BAR)`. ✓
- **σ_dose calibrated via the same `calibrate_sigma_dose`** (calibrated on the reference profile, applied to the misspecified profiles — a reasonable "is the estimator overfit to the reference" probe). ✓
- **Stability report**: `mean_abs_diff_from_reference` (mean over combos of |misspec β* − ref β*|); assessment "stable" if < 0.1. ✓ (partial — see NF-IMPL-4)
- **Candidate-blind (Ruling 9)**: misspecified profiles use known oracle ground truth (`p_true` from uniform/bimodal, Bernoulli realization); simulation seeds are `combo_seed` hashes; no candidate output is an input. ✓
- **Results committed**: integrated into `main()` as Step 4; included in `--full` JSON (`full["misspecification_stress_test"]`). ✓ (L19 publication)

**Status: REMEDIATED.** The blocking defect (total absence) is fixed; the spec's literal §8 item 9 requirement is satisfied.

---

## NF-IMPL-1 — private absolute path — REMEDIATED

- Line 1187: `out_path = args.out or "diagnostics/l8_power_analysis_results.json"` — relative path. ✓
- Full-code grep for `/home`, `C:\Users`, `/Users/` returns no matches. **No private absolute paths remain anywhere in the committed code.** ✓
- The default now works on Rebecca's local system without a workspace directory. ✓

---

## NF-IMPL-2 — false-kill aggregation — REMEDIATED

- `simulate_one_simulation` now returns `(beta_stars, n_failures, per_seed_betas)` where `per_seed_betas` is `(n_sims, N_SEEDS)`, recording each seed's β*_s (computed via the identical `beta_star_for_seed`). ✓
- `run_power_analysis` computes and reports BOTH:
  - `false_kill_rate` = P(mean of 5 β*_s < 0.2) — the existing 5-seed-mean aggregation. ✓
  - `false_kill_rate_per_seed` = P(any of 5 β*_s < 0.2) via `np.any(valid_ps < BETA_STAR_BAR, axis=1)` — matches the per-seed scoring bar (spec §2: "standardized slope ≥ 0.2, per seed"). ✓
- Both reported in the full-run results dict and the validation-batch output. ✓
- **The estimator itself is unchanged** — `beta_star_for_seed` and `run_level_beta_star` are unmodified; only the per-seed recording and reporting were added. ✓
- Flagged to Rebecca for ruling on which aggregation is the G3-escalation input (inline comment: "Flagged to Rebecca for ruling on which is the G3 input"). ✓
- NaN handling is correct: per-seed values are recorded only in the non-fail branch (run-level not-fail ⟺ no seed has σ_pool=0 ⟺ all per-seed values are non-NaN); the `valid_ps = per_seed[~np.isnan(bs)]` selection is consistent. ✓

---

## NF-IMPL-3 — stale validation table — REMEDIATED

The 100-sim validation-batch table in `handoffs/TASKBUILDER_L8_POWER_ANALYSIS_HANDOFF.md` is regenerated against the latest code (`c3a5d49`), with a "fresh run" attestation:

| Combo | Mean β* (stale) | Mean β* (regenerated) | Consistent with 0.3 target? |
|---|---|---|---|
| Low-noise | 0.3425 | 0.3680 | — |
| Mid (reference op point) | 0.2392 | **0.3221** | ✓ within ~2 SE of 0.3 |
| High-noise | 0.1159 | 0.2212 | — |

The reference operating point (α=0.1, v=1.0, C_min=0.7, η=0.1) now reads 0.3221 — consistent with the 0.3 calibration target (the prior 0.2392 was ~6 SE below, not Monte-Carlo noise). **The stale-table discrepancy is resolved.** ✓ The regenerated numbers are valid for the remediated HEAD `61a2f8d` because the remediation did not change the simulation core (`beta_star_for_seed`, `run_level_beta_star`, `calibrate_sigma_dose`, `simulate_one_seed` are all unchanged); the per-seed return-value addition does not alter the run-level β* values.

---

## Non-blocking finding (new)

- **NF-IMPL-4 (stress-test stability report is partial):** The handoff's BF-IMPL-1 verification criteria elaborated that the stress-test should run "the full power analysis (estimator + false-kill + sensitivity map) on each misspecified profile" and report "whether the estimator and the (C_min, η) selection are stable." The implemented stress-test runs only a subset of 8 parameter combos per misspecified profile (computing mean β*, std, false-kill per combo) and reports only mean-β* stability (mean abs diff from reference < 0.1). It does **not** build the full 2D sensitivity map over (C_min, η) on misspecified profiles, nor run the deterministic selection rule on them, nor report (C_min, η) selection stability. The spec's literal §8 item 9 ("run the power analysis on ≥2 misspecified profiles to verify the estimator is not overfit") is satisfied — the estimator is applied to genuinely different profiles and mean-β* stability is reported — but the handoff's stricter elaboration is only partially met. Per the authority chain (approved specification > prompt), the binding requirement is the spec's item 9, which is met; the handoff's elaboration is a stricter prompt-level bar. **Class: scope-completeness (non-blocking).** Flagged to Rebecca: she should confirm whether the partial stress-test (mean-β* stability only) suffices for her G2–G5 rulings, or whether the TASK BUILDER should extend it to run the full sensitivity map + selection on misspecified profiles before she relies on it. This is not a candidate-blindness or score-chasing surface.

---

## Collateral check — PASS

Diff `c3a5d49...61a2f8d` touches only:
- `diagnostics/l8_power_analysis.py` (+209/−10)
- `handoffs/TASKBUILDER_L8_POWER_ANALYSIS_HANDOFF.md` (regenerated table)
- `handoffs/TASKBUILDER_L8_REMEDIATION_HANDOFF.md` (new remediation handoff)

**The R8 guard (`src/e1_experiment.py`) is untouched** — confirmed empty diff. ✓

Confirmed unchanged (the remediation did not touch):
- **The estimator (§2 XF-5)** — `beta_star_for_seed` and `run_level_beta_star` unmodified; not a reimplementation or approximation. ✓
- **The 8 verified §8 protocol items** — grid (240 combos), deterministic combo-hash seeds (mod 2^31), 10,000 sims/combo, false-kill (now with both aggregations), sensitivity map (3 regions), deterministic selection rule (informative → max min-distance → highest C_min → lowest η), publication via JSON — all structurally unchanged. ✓
- **Candidate-blindness (Ruling 9)** — no candidate-output path introduced; misspecified profiles use oracle ground truth and combo-hash seeds. ✓
- **R8 guard** — unchanged (raises, not warns; scoring semantics untouched). ✓
- **Estimator validation (Examples A/B)** — unchanged. ✓

The only structural addition is the misspecification stress-test (new functions `simulate_one_seed_misspecified`, `run_misspecification_stress_test`, Step 4 in `main`) and the per-seed return value — both additive, neither altering prior verified behavior.

---

## Scope check — PASS

The TASK BUILDER's remediation commits touch only `diagnostics/l8_power_analysis.py` and the two handoff docs. No spec, constitution, STATE.md, provenance log, R8 guard, or scoring artifact was modified. Scope is confined to the named files.

---

## §5 P3 / P6 compliance

- **P3 (source-class tags):** PASS. New thresholds in the misspecification code carry tags (`[Sol-XF-9]`, `[PROPOSED — apparatus parameter, §8 item 9]`); the per-seed false-kill field is tagged `[NF-IMPL-2, PROPOSED — flagged to Rebecca]`. All pre-existing tags retained.
- **P6 (provenance citations):** PASS. `[Sol-XF-9]`, `[Entry 76]`, `[BAR-Entry 11]` citations consistent with the provenance log and spec.

---

## Locked bars preserved

Yes. `BETA_STAR_BAR = 0.2 [BAR-Entry 11]` remains an input to the false-kill calculation (both aggregations), never an output. `N_SEEDS = 5 [BAR-Entry 11]` preserved. No L8 locked bar (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds) changed. R8 guard untouched. No negative result or INSTRUMENT_FAILURE label renamed or reinterpreted (zero-variance → INSTRUMENT_FAILURE preserved).

---

## Preserved evidence

The §2 XF-5 estimator, the candidate-blind design, the R8 guard, the estimator validation (Examples A/B), and the 8 verified §8 protocol items are all preserved and verified. The prior BLOCK's positive verifications remain valid. The remediation is additive and does not invalidate any prior evidence.

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
- No touching the R8 guard, the estimator, or the 8 verified protocol items (confirmed unchanged).
- No TASK BUILDER discretion granted over the selection rule, seeds, grid, profiles, or estimator.

---

## Verdict and routing

**Verdict: CLEAR.** All four findings remediated: BF-IMPL-1 (misspecification stress-test now implemented — spec §8 item 9 satisfied), NF-IMPL-1 (relative path, no private paths), NF-IMPL-2 (both false-kill aggregations reported, per-seed any-seed present, estimator unchanged), NF-IMPL-3 (validation table regenerated, reference op point now 0.3221 consistent with 0.3 target). The estimator, 8 protocol items, candidate-blindness, and R8 guard are all preserved. One non-blocking observation (NF-IMPL-4): the stress-test's stability report is partial (mean-β* only; no full sensitivity map or (C_min, η) selection stability on misspecified profiles) — flagged to Rebecca, not a block.

**Next authorized role:** WORKFLOW COORDINATOR. On CLEAR, Rebecca runs `python diagnostics/l8_power_analysis.py --full` locally, producing the sensitivity map and misspecification stress-test results that feed her G2–G5 gate rulings (G1 already resolved by Entry 81). Rebecca should also rule on the NF-IMPL-2 false-kill aggregation (which is the G3-escalation input) and consider whether the partial stress-test (NF-IMPL-4) suffices or should be extended. Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

---

*This review was conducted read-only against the code at `61a2f8d` on `taskbuilder/l8-power-analysis` and the spec at `c7d7bed`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
