# Changelog — L8 G2–G4 Minimal Full-Screen Specification

**Date:** 2026-08-20 · **Regime:** B · **Branch:** `architect/l8-g2g4-minimal-fullscreen`
**Base:** `main` at `f4e22317ebe0e3e1a7dbee0b81ef8c3fb9839b2b`
**Files changed:** created `specs/l8_g2g4_minimal_full_screen_spec.md`; created `specs/l8_g2g4_minimal_full_screen_CHANGELOG.md` (this file); created `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md`; created `specs/l8_g2g4_minimal_full_screen_EXECUTABILITY_TRACE.md`.

## What this is

A minimal executable specification for the L8 G2–G4 full battery-geometry screen: 20 geometries × 240 cells × 2,000 simulations per cell, evaluated with the `b139749` β* direct path plus the Rebecca-authorized direct per-seed Spearman ρ calculation (to compute the complete frozen-v2.2 scoring predicate). Candidate-blind, O-15 diagnostic-only. Authorizes NO scoring.

## Advisor round-2 cleanup (numerical/qualification semantics)

- Corrected ρ deterministic-test expected values (Python-verified): `[1,0,2,3]` → `0.8` (passes at threshold); `[0,0,2,3]` → `sqrt(0.9)≈0.9487`; `[3,2,1,0]` → `-1.0`.
- Added `RHO_COMPARE_EPS = 1e-12` locked-bar comparison tolerance: ρ predicate passes iff `ρ_s ≥ 0.8` OR `abs(ρ_s − 0.8) ≤ RHO_COMPARE_EPS` (absorbs binary64 roundoff at exact threshold only); no-softening test asserts `0.8 − 2·RHO_COMPARE_EPS` fails. Tie detection = exact finite binary64 equality.
- §5.1 non-finite bullet reconciled with §5.6 decision tree (disposition = apparatus-invalid exclusion OR undefined-ρ predicate failure).
- §5.5 test 7 made concrete (aggregation-unit over precomputed per-seed `(β*_s, ρ_s)` tuples: all-pass; fail-β*; fail-undefined-ρ; fail-ρ<0.8).
- §5.4/schema: apparatus-invalid cell disqualifies a geometry — added `cell_apparatus_invalid`, `has_apparatus_invalid_cell`; `meets_target = (no apparatus-invalid cells) AND max_primary_false_kill ≤ 0.10`.
- §7.1 schema: separate true-effect / null-control denominator fields (`n_valid_true_effect`, `n_valid_null_control`, `n_apparatus_invalid_true_effect/null_control`).
- `b139749` not overstated: computes `β*_s` and transiently `D̄` inside `beta_star_for_seed`; does NOT expose per-seed `ρ_s` or durable `D̄` arrays — TASK BUILDER computes `ρ_s` in the same estimator path or extends the per-seed result record.
- Reconciled companion files (executability trace, TASK BUILDER handoff, changelog) with the round-2 spec changes. Locked bars unchanged.

## Amendment (Rebecca directive, 2026-08-20) — Item 1 (primary metric) + Item 3 (geometry authority)

Rebecca authorized the direct per-seed Spearman ρ calculation (`docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md`), resolving the prior ARCHITECT STOP (`handoffs/ARCHITECT_L8_FULLSCREEN_STOP_ITEM1_RHO.md` — `b139749` computes β* but not ρ). Changes applied:

### Item 1 — primary metric completed to the full frozen-v2.2 predicate

- **§5.1:** added the direct per-seed Spearman ρ calculation: inputs = the four dose-level regulation-error summaries `D̄_{s,ℓ}` already used by the β* estimator; dose ranks `(1,2,3,4)`; response ranks = ascending midranks, ties = arithmetic mean of occupied ranks; statistic = Pearson correlation between dose ranks and response midranks; locked predicate `ρ_s ≥ 0.8` `[BAR-Entry 11]`; zero response-rank variance → `ρ_s` undefined → failure of the ρ predicate (not INSTRUMENT_FAILURE); non-finite/structurally invalid → apparatus-validity rules (§5.6); FP tolerance minimal/explicit/tested, must not change the 0.8 bar.
- **PRIMARY** re-designated to **`complete_verdict_false_kill_rate` = `P(any seed: β*_s < 0.2 OR ρ_s undefined OR ρ_s < 0.8)`** (complete frozen-v2.2 any-seed scoring-verdict false-kill rate). `diagnostic_beta_only_any_seed_false_kill_rate` (= `b139749` `false_kill_rate_per_seed`) and `diagnostic_five_seed_mean_false_kill_rate` (= `b139749` `false_kill_rate`) retained as diagnostics (do not gate). Null-control false-pass = `null_control_false_pass_rate` = fraction where every seed satisfies both predicates. Distinct schema fields (§7.1).
- **§5.5:** added 7 required deterministic tests (perfect monotonicity; adjacent-inversion/threshold; tied responses; constant responses; decreasing responses; non-finite inputs; 5-seed complete-verdict aggregation).
- **§5.6:** added apparatus-validity rules for non-finite/structurally invalid inputs (no automatic INSTRUMENT_FAILURE; apparatus-fault vs no-fault disposition; no-relabeling).
- The ρ calculation is a direct, deterministic, non-resampling statistic — NOT a quorum/fallback/bootstrap/Wilson procedure; the v2.4 §8.1 pooled-bootstrap predicate `[BAR-Entry 11.3]` is NOT part of this primary (frozen-v2.2 bars only).

### Item 3 — geometry authority + acceptance/boundary rules

- **§0:** added Rebecca Item 1 ρ authorization ruling + the prospective DRAFT PI geometry-list adoption (`handoffs/DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md` — DRAFT, Rebecca signature gate).
- **§3:** prospectively adopted only the 20-geometry list + ordering from `4463cbc` §8.2 (not previously PI-approved/frozen); acceptance applies to exact `(W, N_w)`; equal-`Q` geometries deterministically ordered (larger `N_w`, then smaller `W`), never merged/pooled.
- **§5.4:** added boundary-escalation rule — STOP if no geometry passes OR first passing geometry on a tested boundary; "tested boundary" defined exactly as `W` ∈ {50, 400} or `N_w` ∈ {4, 64} (any edge of the `W×N_w` grid).
- **§1.3/§9:** confirmed v2.4 prohibited machinery (Wilson, pooled-bootstrap, etc.) remains prohibited; the per-seed ρ is an authorized direct calculation, not prohibited machinery.

### Preserved (unchanged)

Locked bars (β* ≥ 0.2, ρ ≥ 0.8, ≥3 doses, 5 seeds) `[BAR-Entry 11]`; verbatim L8 + §5 P1–P6 quotes (E2); 19.2M two-arm / ~90.5 min/1.5–2 h timing (E3); no prohibited machinery beyond the authorized ρ calculation (E5); end-to-end executability re-verified — the complete predicate is now computable via the direct per-seed ρ (E6). No merge to main. TASK BUILDER remains held until fresh-context CRITIC clearance AND Rebecca's geometry-list signature.

> **Historical note:** the sections below ("Remediation" and "Decisions made by ARCHITECT") record the **original pre-amendment** spec state. Where any statement below names `false_kill_rate_per_seed` as PRIMARY or uses "any-seed rate primary" / "scoring-verdict-aligned" wording, it is **superseded** by the "Amendment (Rebecca directive, Item 1)" section above: the current PRIMARY is `complete_verdict_false_kill_rate = P(any seed: β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8)`; `false_kill_rate_per_seed` (β*-only any-seed) and `false_kill_rate` (5-seed mean) are diagnostics. They are retained here as a historical record only.

## Remediation (CRITIC BLOCK → ARCHITECT, 2026-08-20)

Fresh-context CRITIC BLOCK (`critic/l8-g2g4-minimal-fullscreen` @ `02a7443`) returned to ARCHITECT only. PRIMARY designation (E1) preserved — CRITIC-verified textually grounded (v2.2 line 44). Fixes applied:

- **B1 (provenance):** corrected `…_TASKBUILDER_HANDOFF.md` "Authoritative inputs" — the §8.2 geometry list and §8.3/§8.4 grids are in **v2.4 `4463cbc`** on `architect/l8-g2g4-remediation`; frozen **v2.2 `c7d7bed`** is cited only for the §2 XF-5 estimator, the per-seed locked bar (line 44), and the 240-cell grid (§8 items 3–6). v2.2 has no §8.2/§8.3 and no 20-geometry sweep. All four files reconciled to a single provenance statement matching spec §0.
- **B2 (accuracy):** qualified §5.2/§5.3 — `false_kill_rate_per_seed` is the **β*-predicate direct** false-kill rate only (standardized-slope < 0.2, any seed; `b139749` line 808); it is a **lower bound** on the complete scoring-verdict false-kill rate, which also requires `ρ ≥ 0.8` per seed (and v2.4 §8.1 direction + pooled-bootstrap, omitted). Removed the unqualified "corresponds to the actual scoring verdict" / "scoring-verdict-aligned" overstatement.
- **NB1:** cited v2.4 §8.1 (`4463cbc`) as corroborating context for the any-seed-primary resolution (v2.2 line 44 remains primary frozen authority; v2.4 §8.1 corroborating only; its pooled-bootstrap predicate `[BAR-Entry 11.3]` deliberately omitted).
- **NB2:** marked primary metric `false_kill_rate_per_seed` `[PROPOSED]` (NF-IMPL-2 in `b139749`); geometry acceptance is a `[PROPOSED]`-gated diagnostic selection requiring Rebecca sign-off before binding/downstream use; TASK BUILDER to record the output artifact's own SHA-256 in the run handoff (§7.2).
- **NB3:** corrected §1.3 — `d08cb7e`'s two open details were for the 1,000-repetition feasibility diagnostic (different workload); screening-run parameters come from the later COORDINATOR handoff, not from closing `d08cb7e`'s feasibility-diagnostic details. `d08cb7e`'s authorization boundary remains correct.
- **NB4:** re-tagged inherited `[Sol-XF-5]` closure labels as `[OP — Sol-XF-5, adopted operationalization]` (P3 `[OP]`-class; crossfamily closure label retained for traceability). Numeric thresholds (0.2, 0.10, 5 seeds, ρ≥0.8) remain `[BAR-Entry 11]`/`[PROPOSED]`.

**Unchanged (CRITIC-verified E1–E6):** PRIMARY designation (E1); verbatim L8 + §5 P1–P6 quotes (E2); 19.2M two-arm accounting + ~90.5 min/1.5–2 h timing (E3); §0 geometry-list provenance `4463cbc` (E4); no prohibited machinery (E5); end-to-end executability (E6). No merge to main.

## Decisions made by ARCHITECT (each tied to source text)

1. **20 geometries** copied verbatim from §8.2 of the L8 crossfamily spec — the Cartesian product `W ∈ {50,100,200,400}` × `N_w ∈ {4,8,16,32,64}`, ordered by `Q = W·N_w` asc, then larger `N_w`, then smaller `W`. Not redesigned. (Source: `06_l8_instantiation_spec.md` at `4463cbc` v2.4 §8.2 lines 276–280 — the only located repo source of the pre-registered 20-geometry list. The v2.4 Wilson/bootstrap §8.9 machinery in the same commit is prohibited and not invoked. Geometry-list authority flagged for CRITIC/Rebecca confirmation.)
2. **240 cells = 15 nuisance × 16 operating** copied exactly from `b139749` / v2.2 §8.3: `α ∈ {0.0,0.02,0.05,0.1,0.2}` × `v_mult ∈ {0.5,1.0,2.0}` × `C_min ∈ {0.5,0.6,0.7,0.8}` × `η ∈ {0.01,0.05,0.1,0.2}`.
3. **2,000 simulations per cell per arm**; **16 workers**; **~1.5–2 h** — Rebecca-established per the WORKFLOW COORDINATOR handoff.
4. **Direct false-kill calculation only; no bootstrap.** Uses the `b139749` β* direct path plus the Rebecca-authorized direct per-seed Spearman ρ calculation. `[SUPERSEDED by the Amendment (Item 1) — the β*-only `false_kill_rate`/`false_kill_rate_per_seed` are now diagnostics; PRIMARY is `complete_verdict_false_kill_rate`.]`
5. **PRIMARY = `false_kill_rate_per_seed`; DIAGNOSTIC = `false_kill_rate`.** `[SUPERSEDED by the Amendment (Item 1) — see §"Amendment" above: PRIMARY is now `complete_verdict_false_kill_rate = P(any seed: β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8)`; `diagnostic_beta_only_any_seed_false_kill_rate` and `diagnostic_five_seed_mean_false_kill_rate` are diagnostics.]`
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
