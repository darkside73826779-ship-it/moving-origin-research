# Changelog — L8 G2–G4 Minimal Full-Screen Specification

**Date:** 2026-08-20 · **Regime:** B · **Branch:** `architect/l8-g2g4-minimal-fullscreen`
**Base:** `main` at `f4e22317ebe0e3e1a7dbee0b81ef8c3fb9839b2b`
**Files changed:** created `specs/l8_g2g4_minimal_full_screen_spec.md`; created `specs/l8_g2g4_minimal_full_screen_CHANGELOG.md` (this file); created `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md`; created `specs/l8_g2g4_minimal_full_screen_EXECUTABILITY_TRACE.md`.

## What this is

A minimal executable specification for the L8 G2–G4 full battery-geometry screen: 20 geometries × 240 cells × 2,000 simulations per cell, evaluated with the existing direct false-kill calculation at `b139749`. Candidate-blind, O-15 diagnostic-only. Authorizes NO scoring.

## Decisions made by ARCHITECT (each tied to source text)

1. **20 geometries** copied verbatim from §8.2 of the L8 crossfamily spec — the Cartesian product `W ∈ {50,100,200,400}` × `N_w ∈ {4,8,16,32,64}`, ordered by `Q = W·N_w` asc, then larger `N_w`, then smaller `W`. Not redesigned. (Source: `06_l8_instantiation_spec.md` at `4463cbc` v2.4 §8.2 lines 276–280 — the only located repo source of the pre-registered 20-geometry list. The v2.4 Wilson/bootstrap §8.9 machinery in the same commit is prohibited and not invoked. Geometry-list authority flagged for CRITIC/Rebecca confirmation.)
2. **240 cells = 15 nuisance × 16 operating** copied exactly from `b139749` / v2.2 §8.3: `α ∈ {0.0,0.02,0.05,0.1,0.2}` × `v_mult ∈ {0.5,1.0,2.0}` × `C_min ∈ {0.5,0.6,0.7,0.8}` × `η ∈ {0.01,0.05,0.1,0.2}`.
3. **2,000 simulations per cell per arm**; **16 workers**; **~1.5–2 h** — Rebecca-established per the WORKFLOW COORDINATOR handoff.
4. **Direct false-kill calculation only; no bootstrap.** Uses `false_kill_rate` (5-seed mean) and `false_kill_rate_per_seed` (any-seed) as computed at `b139749`.
5. **PRIMARY = `false_kill_rate_per_seed`; DIAGNOSTIC = `false_kill_rate`.** Justification: the frozen v2.2 spec (c7d7bed, line 44) states the locked standardized-slope ≥ 0.2 bar runs "per seed," so the scoring-verdict-aligned direct false-kill estimate is the any-seed rate. This relabels output priority only; neither direct formula is altered.
6. **False-kill target = 0.10** (`FALSE_KILL_THRESHOLD`, v2.2 §8: false-kill exceeding 0.10 escalates to G3). Geometry acceptance: `max` over 240 cells of primary false-kill ≤ 0.10. Minimum acceptable battery = first geometry in §3 order meeting the target; STOP if none.
7. **Seed derivation preserved unchanged across geometries** — the frozen v2.2 spec defines no geometry seed dimension (only superseded v2.4 §8.9.3 machinery does). `combo_seed(α,v,C_min,η)` and the per-simulation derivation are reused as-is; geometry is distinguished by the `(W, N_w)` data shape. Known shared-seed property memorialized in §6.1.
8. **Two arms per cell preserved** (combo + null-control) per `b139749`'s verified `run_power_analysis`, to supply the false-pass rate.

## Mismatch memorialized (flagged for CRITIC / Rebecca)

The verified baseline `b139749` labels `false_kill_rate` (5-seed mean) as the key false-kill output and flags `false_kill_rate_per_seed` as "NF-IMPL-2: PROPOSED — flagged to Rebecca." This spec resolves label priority by applying the frozen spec's "per seed" locked-bar text, making the any-seed rate primary. CRITIC and Rebecca must review this mapping before TASK BUILDER implementation. Reference cell from `6d455bb` illustrating materiality: `false_kill_rate = 0.0565` (passes 0.10) vs `false_kill_rate_per_seed = 0.7483` (fails).

## Non-rules NOT introduced (scope held)

No bootstrap, no Wilson intervals, no `predicate_false_kill_rates`/`failure_mask_counts`/finalist 10,000-rep confirmation, no `resolved_config.json` manifest, no rehearsal fixtures, no fault injection, no sensitivity/misspecification recomputation, no `(C_min,η)` selection, no scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17, no INSTRUMENT_FAILURE reclassification.

## Provenance

- Frozen L8 v2.2 spec: `c7d7bed6...` (`reviews/l8_crossfamily_review/06_l8_instantiation_spec.md`).
- Pre-registered 20-geometry list: `4463cbc` v2.4 §8.2 (same path; only located repo source; v2.4 §8.9 machinery prohibited).
- Verified code: `diagnostics/l8_power_analysis.py` at `b1397498...`.
- Reference artifact: `6d455bb8...` (SHA-256 `978f21c0...`).
- Rebecca L8 feasibility ruling: `d08cb7e...` (superseded in part; this spec closes its two open execution details: 2,000 sims/cell/arm, and no bootstrap).
- Constitution v2 §5 P1–P6 binding; L8 law text verbatim (constitution v2 line 28).
- M4 spec / task spec / M0 decision sheet on `main` (`f4e22317`).
