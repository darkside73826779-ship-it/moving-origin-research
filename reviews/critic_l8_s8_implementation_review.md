# CRITIC Implementation Review — L8 §8 Power Analysis + R8 Guard

**Gate served:** Implementation review of the first M4-era code — §8 candidate-blind power analysis simulation + R8 fail-closed hold-out guard
**Reviewer:** CRITIC (fresh-context, code-vs-spec fidelity review)
**Date:** 2026-08-19 12:48 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **BLOCK**
**Next recipient:** WORKFLOW COORDINATOR → returns to TASK BUILDER

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Code branch | `taskbuilder/l8-power-analysis` |
| Branch HEAD (under review) | `c3a5d49` |
| §8 power analysis code | `diagnostics/l8_power_analysis.py` (1015 lines) |
| R8 guard | `src/e1_experiment.py` (+6/-5) |
| TASK BUILDER handoff | `handoffs/TASKBUILDER_L8_POWER_ANALYSIS_HANDOFF.md` |
| L8 spec v2.2 (frozen, the spec to check against) | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` at `c7d7bed` on `architect/l8-instantiation-v2.2-fresh` — §8 protocol, §2 estimator |
| Constitution v1 | `docs/ARCHITECTURAL_CONSTITUTION.md` on main |
| Provenance log | `docs/rulings/provenance_log.md` on main (Entry 76, Entry 81) |

Read-only review. No code, spec, constitution, or scoring artifact modified (read-only + this review file). No scoring, seed execution, hold-out seed exposure, full simulation run, or unauthorized merge performed. The estimator-validation and validation-batch results were verified by code inspection against the TASK BUILDER's reported numbers; the code was not executed by the CRITIC.

---

## Headline finding (BLOCK)

The code faithfully implements the §2 XF-5 estimator and most of the §8 protocol (grid, seeds, false-kill, sensitivity map, selection rule, publication), and the R8 guard is correct. **However, §8 item 9 — the misspecification stress-test — is not implemented at all.** There is no function, no call site, and no mention in the TASK BUILDER's handoff. The handoff's own review checklist lists "misspecification stress-test" as a required protocol element to verify. The delivered code therefore does not faithfully implement the full §8 protocol. This is a fidelity defect → BLOCK.

---

## Code-vs-spec fidelity

### The estimator (§2 XF-5) — VERIFIED faithful

`beta_star_for_seed(d_seed)` (lines 200–228) implements the exact specified estimator:
- Per-dose means `D̄_{s,ℓ} = mean_w d_{s,ℓ,w}` (line 209). ✓
- Slope numerator `β_s = Cov(D̄, x) / Var(x)` with `Var(x) = Var({0,1,2,3}) = 1.25` (lines 214–215, 196). ✓
- Standardization `σ_pool,s = sqrt(Σ(d − D̄)² / (L·(N_w−1)))` with `L·(N_w−1) = 12` df (lines 219–222). ✓
- `β*_s = β_s / σ_pool,s` (line 228). ✓
- Zero-variance behavior: `σ_pool,s = 0 → INSTRUMENT_FAILURE` (lines 224–226). ✓
- `W = 50` and `N_w = 4` are distinct symbols, not overloaded (lines 58–59). ✓
- The estimator is the identical one used at scoring (not a reimplementation or approximation). ✓

### The protocol (§8) — PARTIAL (8 of 10 items; item 9 missing)

| §8 item | Implementation | Status |
|---|---|---|
| 1. Synthetic data-generating family P(α, v) | `simulate_dose` / `simulate_one_seed` (lines 279–371); mirror profiles are parameterized scalar distributions, not model forward passes | ✓ |
| 2. (parameter grid — see item 3) | — | — |
| 3. Parameter grid α{0,0.02,0.05,0.1,0.2} × v{0.5,1.0,2.0}×v_ref × C_min{0.5,0.6,0.7,0.8} × η{0.01,0.05,0.1,0.2} = 240 | `ALPHAS/V_MULTS/C_MINS/ETAS` (lines 136–139) | ✓ 240 combos |
| 4. 10,000 sims per combo, deterministic seed = hash(combo) mod 2^31 | `combo_seed` (lines 152–162), `N_SIMS_FULL=10_000` (line 123) | ✓ |
| 5. Identical β* estimator | uses `beta_star_for_seed` | ✓ |
| 6. False-kill = fraction where β*_est < 0.2 when true β* ≥ 0.3 | lines 662–668 | ✓ (see NF-IMPL-2 on aggregation) |
| 7. Sensitivity map 2D over (C_min, η), 3 regions | `classify_region` / sensitivity-map build (lines 561–570, 729–762) | ✓ |
| 8. Deterministic selection rule (informative → max min-distance → highest C_min → lowest η) | `select_cmin_eta` (lines 587–621) | ✓ no discretion |
| **9. Misspecification stress-test (≥2 profiles ≠ reference)** | **NOT IMPLEMENTED** — no function, no call, not in handoff | **✗ MISSING (BLOCK)** |
| 10. Publication (code, seeds, grid, profiles, estimator, machine-readable table before freeze) | JSON result table written by `main --full` (lines 1003–1007) | ✓ (see NF-IMPL-1 on path) |

### Candidate-blindness (Ruling 9, Entry 76) — VERIFIED

- Simulation seeds are `combo_seed(alpha, v_mult, c_min, eta)` = SHA-256 of the canonical parameter string, mod 2^31 (lines 152–162). They are derived only from apparatus parameters, never candidate data. ✓
- Per-seed seeds are `base_seed + i*N_SEEDS + s` (line 399) — a deterministic function of the combo seed only. ✓
- No candidate diagnostic seeds (101–105) are used anywhere. ✓
- The synthetic profiles use known oracle ground truth (`p_true` from a Beta distribution, Bernoulli realization — lines 297–300); no candidate output is an input at any point in the simulation or the (C_min, η) selection. ✓
- **There is no path by which candidate behavior could influence the simulation or the selection.** ✓

### R8 fail-closed guard — VERIFIED

`src/e1_experiment.py` diff (+6/-5): the hold-out-seed guard at the run-setup block changes its action from `_tee("[R3 WARNING] ...")` (continue) to `raise ValueError("[R3/R8 FAIL-CLOSED] ...")` (lines 2395–2403). The gating condition (`holdout_in_run and not is_scoring_run`) is unchanged. Consequences:
- **Raises, does not warn.** ✓
- Label is `[R3/R8 FAIL-CLOSED]`. ✓
- The legitimate 5-seed scoring run (`is_scoring_run = set(seeds) == set(SCORING_SEEDS)`) is unaffected — the guard does not fire for the scoring run, so 45/46 may appear there. ✓
- **Scoring semantics untouched** — the guard sits before the log file is opened; the rest of the run logic is unchanged. ✓
- Consistent with the TASK BUILDER's claim that `--seeds 45,46` raises immediately. ✓

### Validation results — consistent (estimator validation); batch table stale (see NF-IMPL-3)

- **Example A** (d = 0.02·ℓ + ε, ε~N(0,0.01)): reported mean β* = 0.2114, anchor 0.2, |0.2114−0.2| = 0.0114 < 0.05 → PASS. The slight upward bias is consistent with the ratio-estimator property E[β_s/σ_pool] ≥ E[β_s]/E[σ_pool]. ✓
- **Example B** (d = ε, ε~N(0,0.01)): reported mean β* = 0.0014, anchor 0.0, |0.0014| < 0.05 → PASS. ✓
- 0 instrument failures in both (σ_pool = SD of ε = 0.1 ≠ 0). ✓
- The estimator validation uses `beta_star_for_seed` directly (per-seed, no 5-seed averaging) — correct for the validation examples. ✓

---

## Blocking findings (classified)

- **BF-IMPL-1 (protocol fidelity — §8 item 9 absent):** The spec §8 item 9 requires: "Run the power analysis on at least two misspecified profiles (different from the synthetic reference that defines R* and dose) to verify the estimator is not overfit to the reference profile." The code contains **no** misspecification stress-test — no function, no call site, and no mention in the TASK BUILDER's handoff or compliance section. The handoff's own checklist lists "misspecification stress-test" as a required §8 protocol element to verify. The delivered code therefore does not faithfully implement the full §8 protocol. The misspecification stress-test is material: it guards against the sensitivity map and (C_min, η) selection being artifacts of estimator overfit to the single synthetic reference profile — exactly the kind of validity check that should run before results feed Rebecca's G2–G5 rulings. **Class: construction defect (missing protocol element).** Returns to TASK BUILDER to implement item 9 against the frozen spec.

## Non-blocking findings

- **NF-IMPL-1 (public-repo policy violation + bug — private absolute path):** Line 1003 hardcodes the default output path as `/home/user/workspace/mor-repo/diagnostics/l8_power_analysis_results.json`. This (a) violates `PUBLIC_REPOSITORY_POLICY.md` §2 (private absolute paths are prohibited content in the public repo) — the path leaks workspace/machine structure into public code; and (b) is a bug — the path will not exist on Rebecca's local system, so `python diagnostics/l8_power_analysis.py --full` without `--out` would raise `FileNotFoundError` and discard the ~6-hour run's results. Recommend: default to a relative path (e.g. `diagnostics/l8_power_analysis_results.json`) or `None`. Must be fixed before Rebecca's full run. **Class: public-repo hygiene + code-quality.**
- **NF-IMPL-2 (false-kill aggregation semantics — spec ambiguity, underestimates):** The false-kill rate is computed on the 5-seed-averaged β* (`run_level_beta_star`, lines 231–244) — i.e. P(mean of 5 β*_s < 0.2) — rather than per-seed P(any seed < 0.2). The L8 scoring bar is per-seed ("standardized slope ≥ 0.2 [BAR-Entry 11], per seed", spec §2). Averaging 5 seeds reduces variance by ~√5, so the code's false-kill is the smallest of the plausible readings and underestimates the false-kill relative to the per-seed scoring bar; this could in principle suppress a warranted G3 escalation. The spec §8 false-kill formula does mention "5 seeds," making 5-seed aggregation defensible, but does not specify which aggregate (mean vs any-seed). The estimator itself is identical and correctly used; only the aggregation is in question. **Class: spec ambiguity / statistical-interpretation.** Recommend Rebecca confirm the intended false-kill semantics (per-seed P(any seed < 0.2) vs 5-seed mean) before relying on the G3-escalation number. Not a candidate-blindness or score-chasing surface.
- **NF-IMPL-3 (attestation inconsistency — stale validation batch table):** The TASK BUILDER handoff's 100-sim batch table reports the reference operating point (α=0.1, v_mult=1.0, C_min=0.7, η=0.1) as mean β* = 0.2392. The `c3a5d49` commit message claims the refined calibration gives β* = 0.304 at that same reference point. These are inconsistent (0.2392 vs 0.304 is ~6 SE apart at std 0.107, n=100 — not Monte-Carlo noise). The handoff was not updated after the `c3a5d49` calibration refinement (that commit touched only the `.py` file). The estimator validation (Examples A/B) is internally consistent, but the validation-batch table is stale relative to the final code. **Class: attestation consistency.** Recommend the TASK BUILDER regenerate the validation-batch table against the final (`c3a5d49`) code so the reported numbers match, before Rebecca's run.

---

## Scope check

The TASK BUILDER's three commits (`bf02958`, `d4c7da4`, `c3a5d49`) touch exactly:
- `diagnostics/l8_power_analysis.py` (the code under review)
- `handoffs/TASKBUILDER_L8_POWER_ANALYSIS_HANDOFF.md` (the TASK BUILDER's own handoff)
- `src/e1_experiment.py` (the R8 guard)

The broader `main...c3a5d49` diff also lists `state/COORDINATOR_*.md` and init-script files, but those are COORDINATOR commits (ledger discipline, checkpoint, init), not the TASK BUILDER's work. **The TASK BUILDER's scope is clean — only the two named files plus its own handoff.** No spec, constitution, STATE.md, provenance log, or scoring artifact was modified by the TASK BUILDER.

---

## §5 P3 / P6 compliance

- **P3 (source-class tags):** PASS. Every numeric threshold in the code carries an inline tag (`[BAR-Entry 11]`, `[PROPOSED — apparatus parameter]`, `[Sol-XF-5]`, `[Sol-XF-9]`, `[LAW-L19]`); the header documents the four tag classes (lines 17–23). Constants W, N_W, L_DOSES, N_SEEDS, R_STAR, TRUE_BETA_STAR, BETA_STAR_BAR, FALSE_KILL_THRESHOLD, EPS_C, grid values, sim counts, calibration params, region boundaries — all tagged. The sensitivity-map region boundaries (FK_BOUNDARY=0.5, FP_BOUNDARY=0.5) are operationalizations of the underspecified §8.7 regions, tagged `[PROPOSED — apparatus parameter, §8.7 operationalization]` — a reasonable, transparent operationalization.
- **P6 (provenance citations):** PASS. `[Entry 76]` (Ruling 9 candidate-blindness), `[Entry 81]`, `[Sol-XF-5]`, `[Sol-XF-9]`, `[BAR-Entry 11]` are cited and consistent with the provenance log and spec.

---

## Locked bars preserved

Yes. `BETA_STAR_BAR = 0.2 [BAR-Entry 11]` (line 71) is an input to the false-kill calculation, never an output; it is not lowered, raised, renamed, or reinterpreted. `N_SEEDS = 5 [BAR-Entry 11]` (line 61) preserved. No L8 locked bar (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds) is changed. The R8 guard touches no scoring semantics. No negative result or INSTRUMENT_FAILURE label is renamed or reinterpreted (zero-variance → INSTRUMENT_FAILURE preserved, line 224–226).

---

## Preserved evidence

The §2 XF-5 estimator implementation is faithful and verified. The candidate-blind design is intact (no candidate-output path). The R8 guard is correct. The estimator validation (Examples A/B) is consistent. All of these are preserved. The BLOCK is confined to the missing §8 item 9 misspecification stress-test; it does not invalidate the estimator, the candidate-blindness, the R8 guard, or the validation results.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, code-structure descriptions, and review analysis. No private absolute paths (the path `/home/user/workspace/mor-repo/...` referenced in NF-IMPL-1 is quoted from the code under review as a finding, not as the review's own path), no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the code, spec, constitution, or any artifact (read-only + this review file).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No running of the full simulation (deferred to Rebecca's local run after clearance).
- No L15/L16/L17 before M5.
- No renaming or reinterpreting any negative result or INSTRUMENT_FAILURE label.
- No TASK BUILDER discretion granted over the selection rule, seeds, grid, profiles, or estimator (verified, not granted).
- No L8 implementation release.

---

## Verdict and routing

**Verdict: BLOCK.** The §2 XF-5 estimator, the candidate-blind design, the R8 guard, and the estimator validation are all correct and verified. However, §8 item 9 (the misspecification stress-test) is not implemented — the code does not faithfully implement the full §8 protocol. Three non-blocking findings also require remediation before Rebecca's full run: the private absolute path (NF-IMPL-1, a public-repo policy violation and a run-breaking bug), the false-kill aggregation semantics (NF-IMPL-2), and the stale validation-batch table (NF-IMPL-3).

**Next authorized role:** returns to **TASK BUILDER** (via WORKFLOW COORDINATOR). The TASK BUILDER must: (1) implement §8 item 9 — the misspecification stress-test on ≥2 profiles different from the synthetic reference, verifying the estimator is not overfit; (2) replace the hardcoded private absolute path (line 1003) with a relative default; (3) reconcile the false-kill aggregation with the per-seed scoring bar or document Rebecca-approved semantics; (4) regenerate the validation-batch table against the final code. On re-clearance, Rebecca runs `python diagnostics/l8_power_analysis.py --full` locally, producing the sensitivity map that feeds her G2–G5 gate rulings. Scoring remains gated behind the five standing M4 gates. Nothing herein authorizes scoring.

---

*This review was conducted read-only against the code at `c3a5d49` on `taskbuilder/l8-power-analysis` and the spec at `c7d7bed`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
