# Executability Trace — L8 G2–G4 Minimal Full-Screen Specification

**Date:** 2026-08-20 · **Regime:** B · **Spec:** `specs/l8_g2g4_minimal_full_screen_spec.md`

This trace confirms every executable input the TASK BUILDER must supply is concretely specified. A value marked ✓ is explicit in the spec; a value the implementer would otherwise have to invent is listed and closed.

## 1. Battery geometry (§3)

| Input | Value | Explicit? |
|---|---|---|
| W set | {50, 100, 200, 400} | ✓ §3, copied from §8.2 |
| N_w set | {4, 8, 16, 32, 64} | ✓ §3, copied from §8.2 |
| count | 4 × 5 = 20 | ✓ |
| ordering | Q = W·N_w asc, then larger N_w, then smaller W | ✓ §3 (20-row table is authoritative) |

No implementer invention. The geometry set is pre-registered and copied verbatim.

## 2. Cells per geometry (§4)

| Input | Value | Explicit? |
|---|---|---|
| α (5) | {0.0, 0.02, 0.05, 0.1, 0.2} | ✓ copied from b139749 |
| v_mult (3) | {0.5, 1.0, 2.0} | ✓ |
| C_min (4) | {0.5, 0.6, 0.7, 0.8} | ✓ |
| η (4) | {0.01, 0.05, 0.1, 0.2} | ✓ |
| nuisance combos | 5 × 3 = 15 | ✓ |
| operating cells | 4 × 4 = 16 | ✓ |
| total cells | 15 × 16 = 240 | ✓ |
| cell ordering | α → v_mult → C_min → η (nested loop, matches b139749 work_items) | ✓ §7.1 |

## 3. Simulation and computation (§2, §5)

| Input | Value | Explicit? |
|---|---|---|
| sims per cell per arm | 2,000 | ✓ §2 |
| arms | combo + null-control (σ_dose=0) | ✓ §5, §7.1 |
| workers | 16 | ✓ §2 |
| pool / chunksize | multiprocessing.Pool / 1 | ✓ §2 |
| N_SEEDS | 5 | ✓ §7.1 (b139749) |
| L_DOSES | 4 ({0,1,2,3}) | ✓ §7.1 |
| estimator | §2 XF-5 (reused from b139749) | ✓ §5 |
| σ_dose calibration | per (α,v) at ref op point (C_min=0.7, η=0.1) | ✓ §5, §7.1 |
| combo_seed | sha256("alpha=…|vmult=…|cmin=…|eta=…")[:8] little-endian % 2^31 | ✓ §6.1 |
| per-sim seed | (base_seed + i·N_SEEDS + s) % 2^31 | ✓ §6.1 |
| seed across geometries | reused unchanged; geometry by (W,N_w) data shape | ✓ §6.1 (rule closure) |
| false_kill_rate (5-seed mean) | P(mean β* < 0.2) | ✓ §5.1 (b139749) |
| false_kill_rate_per_seed (any-seed) | P(any β*_s < 0.2) | ✓ §5.1 (b139749) |
| BETA_STAR_BAR | 0.2 [BAR-Entry 11] | ✓ |
| FALSE_KILL_THRESHOLD | 0.10 [PROPOSED — §8] | ✓ |
| primary metric | complete_verdict_false_kill_rate = P(any seed: β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8) | ✓ §5.1/§5.2 |
| diagnostic metrics | diagnostic_beta_only_any_seed_false_kill_rate (β*-only any-seed); diagnostic_five_seed_mean_false_kill_rate (5-seed mean) | ✓ §5.1 |
| null-control false-pass | null_control_false_pass_rate = fraction every seed satisfies both predicates | ✓ §5.1 |
| per-seed Spearman ρ | Pearson corr of dose ranks (1,2,3,4) vs response midranks; ties=mean of occupied ranks; ρ_s locked predicate ≥0.8 [BAR-Entry 11] | ✓ §5.1 |
| RHO_BAR | 0.8 [BAR-Entry 11] | ✓ |
| RHO_COMPARE_EPS | 1e-12 [PROPOSED — §8]; predicate pass iff ρ_s≥0.8 OR abs(ρ_s−0.8)≤RHO_COMPARE_EPS; absorbs binary64 roundoff at exact threshold | ✓ §5.1 |
| tie detection | exact finite binary64 equality (no separate tie tolerance unless chosen/tested) | ✓ §5.1 |
| no-softening test | ρ = 0.8 − 2·RHO_COMPARE_EPS must fail (bar not moved) | ✓ §5.5 (2a) |
| denominators | complete_verdict_false_kill_rate over valid true-effect; null_control_false_pass_rate over valid null-control; apparatus-invalid excluded | ✓ §5.6/§7.1 |
| schema fields | cell_apparatus_invalid; has_apparatus_invalid_cell; n_valid_true_effect/null_control; n_apparatus_invalid_true_effect/null_control | ✓ §7.1 |
| geometry-level primary | max over 240 cells of complete_verdict_false_kill_rate (apparatus-invalid cells excluded) | ✓ §5.4 |
| meets_target | (no apparatus-invalid cells in geometry) AND max_primary_false_kill ≤ 0.10 | ✓ §5.4 |
| minimum battery | first §3 geometry with meets_target; null if none | ✓ §5.4 |

## 4. Output (§7)

| Input | Value | Explicit? |
|---|---|---|
| JSON path | diagnostics/l8_g2g4_minimal_full_screen.json | ✓ §7.1 |
| schema_version | l8-g2g4-minimal-fullscreen-v1 | ✓ §7.1 |
| per-cell fields | geometry_index, W, N_w, alpha, v_mult, c_min, eta, base_seed, n_sims_attempted, n_valid, n_instrument_failures, primary_false_kill_rate, diagnostic_false_kill_rate, false_pass_rate, n_instrument_failures_null, mean_beta_star, mean_beta_star_null | ✓ §7.1 (exact) |
| per-geometry fields | geometry_index, W, N_w, Q_per_dose, queries_per_five_seed_run, max_primary_false_kill, meets_target, cells[240] | ✓ §7.1 |
| selection fields | false_kill_target, primary_metric, diagnostic_metric, minimum_geometry_satisfying_target, rule, scoring_verdict_alignment_note | ✓ §7.1 |
| NaN handling | sanitized to null | ✓ §7.1 |
| write | single atomic write after all 20 geometries | ✓ §7.1 |
| handoff path | diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md | ✓ §7.2 |

## 5. Open rule the implementer would otherwise invent — CLOSED

| Rule | Closure | Where |
|---|---|---|
| Which false-kill rate is primary? | complete_verdict_false_kill_rate = P(any seed: β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8) — the complete frozen-v2.2 any-seed predicate (β* AND ρ). Authorized by Rebecca (ρ calculation added; b139749 had no ρ). | §5.1/§5.2 |
| Is per-seed Spearman ρ computable? | YES — direct calculation added per Rebecca authorization (Pearson corr of dose ranks (1,2,3,4) vs response midranks; ties=mean of occupied ranks; zero variance→undefined→ρ-predicate failure; non-finite→§5.6 apparatus rules). NOT a quorum/fallback/bootstrap/Wilson procedure. | §5.1/§5.6 |
| What is the false-kill target? | 0.10; acceptance = max cell primary ≤ 0.10 (exact (W,N_w) geometry; PROPOSED-gated diagnostic selection; Rebecca sign-off required) | §5.4 |
| Boundary escalation? | STOP if no geometry passes OR first passing geometry on a tested boundary (W∈{50,400} or N_w∈{4,64}) | §5.4 |
| Deterministic tests? | 7 required cases (perfect monotonicity; adjacent-inversion; tied; constant; decreasing; non-finite; 5-seed aggregation) | §5.5 |
| Does the seed include geometry? | No; derivation reused unchanged; geometry by data shape | §6.1 |
| How many arms? | Two (combo + null-control), both 2,000/cell | §5, §7.1 |
| What is the minimum battery if none meet target? | null → STOP, return to Rebecca; grid not extendable | §5.4 |

## 6. No prohibited machinery added

Confirmed absent from the spec: bootstrap; Wilson intervals; `predicate_false_kill_rates`; `failure_mask_counts`; finalist 10,000-rep confirmation; `resolved_config.json` manifest; rehearsal fixtures; fault injection; sensitivity/misspecification recomputation; `(C_min,η)` selection; scoring; protected-seed access; seeds 201–203/301–303; G2–G4 freeze; merge to main; L15/L16/L17; INSTRUMENT_FAILURE reclassification. (Spec §1.3, §9.) Inherited `[Sol-XF-5]` closure labels re-tagged to P3 `[OP]`-class (NB4); numeric thresholds (0.2, 0.10, 5 seeds, ρ≥0.8) remain `[BAR-Entry 11]`/`[PROPOSED]`.

## 7. Verdict

Every executable input is explicit. The specification is executable end-to-end with no implementer invention required. The complete-verdict primary predicate is now computable: `b139749` provides per-seed `β*_s` and the dose-level summaries `D̄_{s,ℓ}`; the direct per-seed Spearman ρ calculation (§5.1, Rebecca-authorized) is added to compute `ρ_s`, and `complete_verdict_false_kill_rate = P(any seed: β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8)` is computable directly (no bootstrap/Wilson/quorum/fallback). Flagged for CRITIC/Rebecca review: (1) the per-seed ρ definition (§5.1) and apparatus-validity rules (§5.6); (2) the complete-verdict primary designation (§5.2); (3) the boundary-escalation rule and "tested boundary" definition (§5.4); (4) the 7 deterministic tests (§5.5). Locked bars unchanged.
