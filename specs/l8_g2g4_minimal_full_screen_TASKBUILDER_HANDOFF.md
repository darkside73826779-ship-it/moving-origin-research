# TASK BUILDER Handoff — L8 G2–G4 Minimal Full-Screen

**Date:** 2026-08-20 · **Regime:** B
**From:** ARCHITECT (`architect/l8-g2g4-minimal-fullscreen`) **To:** Fresh-context CRITIC → Rebecca → TASK BUILDER
**Spec:** `specs/l8_g2g4_minimal_full_screen_spec.md` (this branch). **Changelog:** `specs/l8_g2g4_minimal_full_screen_CHANGELOG.md`. **Executability trace:** `specs/l8_g2g4_minimal_full_screen_EXECUTABILITY_TRACE.md`.

## Objective

Implement the minimal full screen: 20 battery geometries × 240 cells × 2,000 simulations per cell, using the `b139749` β* direct path plus the Rebecca-authorized direct per-seed Spearman ρ calculation (to compute the complete frozen-v2.2 scoring predicate). Candidate-blind, O-15 diagnostic-only. Output one machine-readable JSON artifact and a short handoff.

## Authoritative inputs (read-only; import `b139749` and `6d455bb` read-only)

- Verified code: `diagnostics/l8_power_analysis.py` at `b1397498ca369067e956479e6c2bd6b0793c3e89` (reuse `_worker_combo`, `_worker_null_control`, `calibrate_sigma_dose`, `simulate_one_simulation`, `beta_star_for_seed`, `run_level_beta_star`, `combo_seed`, the §2 XF-5 estimator, and the multiprocessing path).
- Reference artifact: `6d455bb8...` (cross-check schema only; do not reproduce as output).
- **Provenance (single statement, reconciled with spec §0):** the 20-geometry `W×N_w` list (§8.2) and the `§8.3`/`§8.4` grids are in **v2.4 `4463cbc`** on `architect/l8-g2g4-remediation` (path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md`). The frozen **v2.2 `c7d7bed`** (same path) is cited **only** for: the §2 XF-5 estimator, the per-seed locked bar (line 44: standardized slope ≥ 0.2, per seed), and the 240-cell nuisance/operating grid (v2.2 §8 items 3–6). v2.2 has **no** §8.2/§8.3 subsections and **no** 20-geometry sweep — do not look for the geometry list there. (v2.4's Wilson/bootstrap §8.9 machinery is prohibited and not invoked.)

## What to build (minimal)

1. A geometry loop wrapping the existing `b139749` 240-cell `run_power_analysis` over the 20 `(W, N_w)` geometries in §3 order. For each geometry × cell, run 2,000 simulations per arm (combo + null-control), 16 workers, `multiprocessing.Pool`, chunksize 1.
2. Reuse `b139749`'s per-seed `β*_s` and the 5-seed mean **unchanged**; the dose-level summaries `D̄_{s,ℓ}` are already produced by `b139749`.
3. **Add the direct per-seed Spearman ρ calculation** (spec §5.1, Rebecca-authorized): for each seed, Pearson correlation of dose ranks `(1,2,3,4)` vs ascending midranks of `D̄_{s,ℓ}` (ties = arithmetic mean of occupied ranks); `ρ_s` locked predicate `≥ 0.8` `[BAR-Entry 11]`; comparison tolerance `RHO_COMPARE_EPS = 1e-12` (pass iff `ρ_s ≥ 0.8` OR `abs(ρ_s − 0.8) ≤ RHO_COMPARE_EPS`; absorbs binary64 roundoff at exact threshold only; a test asserts `0.8 − 2·RHO_COMPARE_EPS` fails); tie detection = exact finite binary64 equality; zero response-rank variance → `ρ_s` undefined → ρ-predicate failure (not INSTRUMENT_FAILURE); non-finite/structurally invalid → §5.6 apparatus-validity decision tree (apparatus-invalid exclusion OR undefined-ρ predicate failure). This is a direct, non-resampling statistic — NOT a quorum/fallback/bootstrap/Wilson procedure. Implement the exact §5.1/§5.4/§7.1 schema.
4. Designate **PRIMARY = `complete_verdict_false_kill_rate` = `P(any seed: β*_s < 0.2 OR ρ_s undefined OR ρ_s < 0.8)`** (complete frozen-v2.2 any-seed predicate). DIAGNOSTICS (do not gate): `diagnostic_beta_only_any_seed_false_kill_rate` (= `b139749` `false_kill_rate_per_seed`), `diagnostic_five_seed_mean_false_kill_rate` (= `b139749` `false_kill_rate`). Null-control false-pass = `null_control_false_pass_rate` = fraction where every seed satisfies both predicates. Distinct schema fields (spec §7.1). See spec §5.2–§5.3.
5. Per geometry compute `max_primary_false_kill = max over 240 cells of complete_verdict_false_kill_rate` (apparatus-invalid cells excluded), `has_apparatus_invalid_cell`, `meets_target = (no apparatus-invalid cells) AND (max ≤ 0.10)` (exact `(W,N_w)` geometry), and `on_tested_boundary` (`W∈{50,400}` or `N_w∈{4,64}`). Minimum acceptable battery = first geometry in §3 order with `meets_target`; **STOP / escalate** if none pass OR first passing is on a tested boundary (spec §5.4). Use separate true-effect / null-control denominator fields (`n_valid_true_effect`, `n_valid_null_control`, `n_apparatus_invalid_true_effect/null_control`, `cell_apparatus_invalid`); a geometry with any apparatus-invalid cell cannot qualify.
6. **Include the 7 deterministic tests** (spec §5.5) with assertions against pre-computed expected values; no no-op / unconditional-pass tests.
7. Write the single artifact `diagnostics/l8_g2g4_minimal_full_screen.json` with the exact schema in spec §7.1 (distinct complete-verdict / diagnostic / null-false-pass fields; `on_tested_boundary`; `first_passing_on_tested_boundary`), atomically, after all 20 geometries complete. Write the short handoff `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md` (spec §7.2), including the **output artifact's own SHA-256** for reproducibility verification.

**TASK BUILDER release gate:** TASK BUILDER does **not** execute until BOTH (a) fresh-context CRITIC clearance of this amended spec, AND (b) Rebecca's signature on `handoffs/DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md` (the prospective geometry-list freeze). The geometry list is **prospectively** adopted, not previously frozen.

## Seed rule (do not invent; closure in spec §6.1)

Reuse `b139749`'s `combo_seed(α, v_mult, C_min, η)` and per-simulation derivation **unchanged** across geometries. The geometry is distinguished by the `(W, N_w)` data shape. Do not introduce a geometry seed namespace. (The frozen v2.2 spec defines none; v2.4 §8.9.3's is prohibited.)

## Preserved verified behavior (do not modify)

`calibrate_sigma_dose`; §2 XF-5 estimator; combo-seed and per-simulation RNG derivation; direct false-kill formulas; null-control calculation; misspecification profiles; R8 guard; JSON write-order fix; functional calibration and simulation multiprocessing at `b139749`.

## Prohibited

No bootstrap, no Wilson, no `predicate_false_kill_rates`/`failure_mask_counts`/finalist confirmation, no `resolved_config.json`, no rehearsal fixtures, no fault injection, no sensitivity/misspecification recomputation, no `(C_min,η)` selection, no scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17, no INSTRUMENT_FAILURE reclassification, no grid extension beyond the 20 geometries.

## Acceptance checks (TASK BUILDER self-verification before returning)

- Exactly 20 geometries, 240 ordered cells each, 2,000 attempted per cell per arm; `n_valid + n_instrument_failures = n_sims_attempted` per cell (and analogously for the null arm).
- Every cell has `primary_false_kill_rate`, `diagnostic_false_kill_rate`, `false_pass_rate`, `n_instrument_failures`.
- `max_primary_false_kill` per geometry recomputes exactly as the max of its cells' `primary_false_kill_rate`; `meets_target` matches; `minimum_geometry_satisfying_target` recomputes from the rule.
- JSON validates against the schema (unknown fields fail); `NaN` sanitized to `null`; single atomic write.
- O-15 label present in header and handoff; "authorizes NO scoring" stated.

## Return to

Fresh-context CRITIC first. CRITIC reviews internal consistency **and** end-to-end executability under the updated CRITIC initialization script. On CLEAR, return to Rebecca before TASK BUILDER implementation. No merge to main.
