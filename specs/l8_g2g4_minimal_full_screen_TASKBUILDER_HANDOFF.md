# TASK BUILDER Handoff — L8 G2–G4 Minimal Full-Screen

**Date:** 2026-08-20 · **Regime:** B
**From:** ARCHITECT (`architect/l8-g2g4-minimal-fullscreen`) **To:** Fresh-context CRITIC → Rebecca → TASK BUILDER
**Spec:** `specs/l8_g2g4_minimal_full_screen_spec.md` (this branch). **Changelog:** `specs/l8_g2g4_minimal_full_screen_CHANGELOG.md`. **Executability trace:** `specs/l8_g2g4_minimal_full_screen_EXECUTABILITY_TRACE.md`.

## Objective

Implement the minimal full screen: 20 battery geometries × 240 cells × 2,000 simulations per cell, using the existing direct false-kill calculation at `b139749`. Candidate-blind, O-15 diagnostic-only. Output one machine-readable JSON artifact and a short handoff.

## Authoritative inputs (read-only; import `b139749` and `6d455bb` read-only)

- Verified code: `diagnostics/l8_power_analysis.py` at `b1397498ca369067e956479e6c2bd6b0793c3e89` (reuse `_worker_combo`, `_worker_null_control`, `calibrate_sigma_dose`, `simulate_one_simulation`, `beta_star_for_seed`, `run_level_beta_star`, `combo_seed`, the §2 XF-5 estimator, and the multiprocessing path).
- Reference artifact: `6d455bb8...` (cross-check schema only; do not reproduce as output).
- **Provenance (single statement, reconciled with spec §0):** the 20-geometry `W×N_w` list (§8.2) and the `§8.3`/`§8.4` grids are in **v2.4 `4463cbc`** on `architect/l8-g2g4-remediation` (path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md`). The frozen **v2.2 `c7d7bed`** (same path) is cited **only** for: the §2 XF-5 estimator, the per-seed locked bar (line 44: standardized slope ≥ 0.2, per seed), and the 240-cell nuisance/operating grid (v2.2 §8 items 3–6). v2.2 has **no** §8.2/§8.3 subsections and **no** 20-geometry sweep — do not look for the geometry list there. (v2.4's Wilson/bootstrap §8.9 machinery is prohibited and not invoked.)

## What to build (minimal)

1. A geometry loop wrapping the existing `b139749` 240-cell `run_power_analysis` over the 20 `(W, N_w)` geometries in §3 order. For each geometry × cell, run 2,000 simulations per arm (combo + null-control), 16 workers, `multiprocessing.Pool`, chunksize 1.
2. Reuse `b139749`'s `false_kill_rate` (5-seed mean) and `false_kill_rate_per_seed` (any-seed) **unchanged**.
3. Designate **PRIMARY = `false_kill_rate_per_seed`**, **DIAGNOSTIC = `false_kill_rate`** (per the frozen v2.2 line-44 "per seed" locked bar; see spec §5.2–§5.3). **Scope:** `false_kill_rate_per_seed` is the **β*-predicate direct** false-kill rate only (standardized-slope < 0.2, any seed); it is a **lower bound** on the complete scoring-verdict false-kill rate, which also requires `ρ ≥ 0.8` per seed (and v2.4 §8.1 direction + pooled-bootstrap, omitted here). The primary metric is `[PROPOSED]` (NF-IMPL-2 in `b139749`); geometry acceptance is a `[PROPOSED]`-gated diagnostic selection requiring Rebecca sign-off before binding/downstream use.
4. Per geometry compute `max_primary_false_kill = max over 240 cells of false_kill_rate_per_seed` and `meets_target = (max_primary_false_kill ≤ 0.10)`. Minimum acceptable battery = first geometry in §3 order with `meets_target`; `null` (STOP) if none.
5. Write the single artifact `diagnostics/l8_g2g4_minimal_full_screen.json` with the exact schema in spec §7.1, atomically, after all 20 geometries complete. Write the short handoff `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md` (spec §7.2), including the **output artifact's own SHA-256** for reproducibility verification.

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
