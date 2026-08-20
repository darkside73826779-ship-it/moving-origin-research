# L8 G2–G4 Minimal Full-Screen Specification

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** Minimal executable specification for the L8 G2–G4 full battery-geometry screen (WORKFLOW COORDINATOR → ARCHITECT handoff, 2026-08-20).
**Authority chain:** Rebecca > constitution laws > approved specifications > this handoff > agent judgment. This spec is a minimal delta; it does not recreate superseded v2.3–v2.7 machinery. It authorizes NO scoring.
**Status:** ARCHITECT draft, routed to fresh-context CRITIC → Rebecca → TASK BUILDER.

## 0. Provenance and source SHAs (P6 — verified against repo)

| Item | Value |
|---|---|
| GitHub repository | `darkside73826779-ship-it/moving-origin-research` |
| Main when issued | `f4e22317ebe0e3e1a7dbee0b81ef8c3fb9839b2b` |
| Frozen L8 v2.2 spec | `c7d7bed6b259fb5163fb610098ea12aed1d3d65e` on `architect/l8-instantiation-v2.2-fresh`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| Pre-registered 20-geometry list (§8.2) | `4463cbc` on `architect/l8-g2g4-remediation`; same path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (v2.4). This is the **only located repo source** of the pre-registered 20-geometry list; the v2.4 Wilson/bootstrap §8.9 machinery in the same commit is **prohibited** and is not invoked. Geometry-list authority flagged for CRITIC/Rebecca confirmation. |
| Verified executable code baseline | `diagnostics/l8_power_analysis.py` at `b1397498ca369067e956479e6c2bd6b0793c3e89` on `taskbuilder/l8-power-analysis` |
| Verified reference artifact | `diagnostics/l8_power_analysis_results.json` at `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3` (SHA-256 `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`) |
| Rebecca L8 feasibility ruling | `docs/rulings/REBECCA_L8_1000_REP_FEASIBILITY_AUTHORIZATION.md` at `d08cb7eefec67609a3ea3cee0eb20da22f78c40a` (superseded in part — see §1.3) |
| Rebecca Item 1 ρ authorization (this amendment) | `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` — authorizes the direct per-seed Spearman ρ calculation (resolving the prior STOP; see §5.3). Recorded by ARCHITECT at Rebecca's direction. |
| Prospective geometry-list adoption (DRAFT, Rebecca signature gate) | `handoffs/DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md` — **DRAFT**, not operative unless/until Rebecca signs. The geometry list is **prospectively** adopted, not previously PI-approved/frozen. |
| M4 specification / task spec / M0 decision sheet / constitution v2 | on `main` (`f4e22317`): `specs/m4_specification.md`, `specs/m4_task_spec.md`, `docs/rulings/M0_DECISION_SHEET.md`, `docs/ARCHITECTURAL_CONSTITUTION_v2.md` |

## 1. Scope, authority, and prohibitions

### 1.1 What this spec is

A minimal, executable specification for one full screen: 20 battery geometries × 240 cells per geometry × 2,000 simulations per cell, evaluated with the direct false-kill calculation at `b139749` **plus the direct per-seed Spearman ρ calculation authorized by Rebecca** (`REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION`) to compute the complete frozen-v2.2 scoring predicate (β* AND ρ, any-seed). Candidate-blind, synthetic/oracle-only, O-15 diagnostic-only. It authorizes NO scoring, NO G2–G4 freeze, NO protected-seed access.

### 1.2 Verbatim law text (P2)

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

*Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md`, line 28 `[LAW-L8]` (v2 Regime B semantics; v1 text at `docs/ARCHITECTURAL_CONSTITUTION.md` line 26 is unchanged).*

> **§5 Versioned-Law Compliance Protocol — 5.1 Universal rules (all roles, all artifacts), quoted verbatim:**
>
> - **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
> - **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
> - **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.
> - **P4 — Regime dating.** Every new artifact states its date and regime in its header. Acts are judged only against their own regime's text; later text is never applied backward.
> - **P5 — Deviation memorialization.** Any deviation from `[LAW]` text — however sensible, however disclosed — is inoperative for scoring until Rebecca has signed a waiver or amendment recorded in the v2 amendment log. Disclosure in a spec is necessary but not sufficient.
> - **P6 — Provenance citation check.** Any claim of the form "Entry n said X" must be verified against the entry's actual text before commit.

*Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md`, §5 5.1 (lines 130–135) `[LAW-§5]`. (ARCHITECT per-role obligation, §5 5.2 line 139: "P1/P2/P3 in every spec. A law section that cannot be written from verbatim text is a STOP, not a reconstruction.")*

### 1.3 Relationship to prior rulings and superseded machinery

Rebecca's L8 feasibility ruling (`d08cb7e`) authorized only a 1,000-repetition parallel feasibility diagnostic and explicitly did **not** authorize the 9.6M screening run, a 10,000-repetition confirmation, or any bootstrap. This minimal spec is issued under the later WORKFLOW COORDINATOR handoff (2026-08-20), by which Rebecca established the full-screen run parameters (§2). (Note: `d08cb7e`'s two open execution details concerned the **1,000-repetition feasibility diagnostic** — allocation of 1,000 reps across sentinel cells/geometries, and full-5,000-valid-bootstrap verdict vs. reduced benchmark bootstrap budget — a different workload from this 9.6M screening run. The screening-run parameters here come from the later COORDINATOR handoff, not from closing `d08cb7e`'s feasibility-diagnostic details. `d08cb7e`'s authorization boundary — no 9.6M run, no 10K confirmation, no bootstrap, no scoring — remains correct and verified.) This spec uses 2,000 simulations per cell per arm and **no bootstrap** — the direct false-kill calculation only.

**Prohibited machinery (not recreated, not invoked):** v2.3–v2.7 benchmark/bootstrap machinery; the 1,000-repetition feasibility benchmark; 48-billion-bootstrap workload; A1/A2/B lifecycle; rehearsal fixtures and 12-case fault-injection suite; serial benchmark; Wilson intervals and `predicate_false_kill_rates` / `failure_mask_counts` / finalist 10,000-rep confirmation / `resolved_config.json` manifest machinery from v2.4 §8.9.3–§8.9.4; the v2.4 §8.1 pooled-bootstrap predicate `[BAR-Entry 11.3]`; sensitivity-map / misspecification-stress recomputation and `(C_min, η)` selection; scoring or protected-seed access; seeds 201–203 or 301–303; G2–G4 freeze or ruling by ARCHITECT; merge to main; L15/L16/L17 before M5; reclassification of ordinary statistical failures as INSTRUMENT_FAILURE. **Not prohibited:** the direct per-seed Spearman ρ calculation (§5.1), authorized by Rebecca — it is a direct, deterministic, non-resampling statistic (not a quorum/fallback/bootstrap/Wilson procedure) and is the minimum computation required for the complete frozen-v2.2 predicate.

## 2. Rebecca-established run parameters

Exactly this full screen (all values `[PROPOSED — apparatus parameter, §8.2/§8]` unless tagged otherwise):

| Parameter | Value | Source tag |
|---|---|---|
| Battery geometries | 20 | `[PROPOSED — §8.2]` |
| Cells per geometry | 240 (= 15 nuisance × 16 operating) | `[PROPOSED — §8.2/§8.4]` |
| Simulations per cell (combo arm) | 2,000 | `[PROPOSED — §8.2]` |
| Workers | 16 | `[PROPOSED — Rebecca-established]` |
| Total combo-arm simulations | 20 × 240 × 2,000 = 9,600,000 | `[PROPOSED — §8.2]` |
| Total actual simulations (both arms) | 20 × 240 × 2,000 × 2 = 19,200,000 (combo 9.6M + null-control 9.6M) | `[PROPOSED — §8.2]` |
| Estimated wall-clock | ~1.5–2 h (linear estimate 4 × 22.63 min ≈ 90.5 min + overhead) | `[PROPOSED — §8]` |
| Parallel execution path | `multiprocessing.Pool`, chunksize 1, results keyed by cell identity not completion order (as verified at `b139749`) | `[PROPOSED — b139749 verified]` |

**Reference timing basis (P6 — verified against `6d455bb`):** `n_sims_per_combo=10000`, `n_combos=240`, `elapsed_seconds=1357.6829717159271` (22.63 min). The reference run executes two arms per cell (combo + null-control; see §5); the 4× linear estimate (90.5 min) holds because the reference also ran two arms. Operational estimate including overhead: 1.5–2 h.

**Workload accounting (flagged for CRITIC/Rebecca confirmation):** Rebecca's established count is 20 × 240 × 2,000 = 9.6M, which is the **combo-arm** count. The false-pass rate requires the preserved null-control arm (§5), which adds a matched 9.6M, for 19.2M actual arm-simulations. The 1.5–2 h timing estimate holds because the verified reference run (`6d455bb`) also executed both arms in 22.63 min, so 4× the reference is ~90.5 min. CRITIC/Rebecca must confirm this two-arm workload accounting is the intended reading; if Rebecca intended a single 2,000-per-cell budget shared across arms, the false-pass rate must be dropped or recomputed and this spec amended.

## 3. Battery geometries (§8.2 — copied verbatim from the pre-registered list)

The 20 geometries are the Cartesian product of `W ∈ {50, 100, 200, 400}` `[PROPOSED — §8.2]` and `N_w ∈ {4, 8, 16, 32, 64}` `[PROPOSED — §8.2]`, ordered by total queries per dose `Q = W × N_w` ascending, then by larger `N_w`, then by smaller `W` `[PROPOSED — §8.2]`. The grid is **not redesigned**; this table is the authoritative ordered list, **prospectively adopted** from `4463cbc` §8.2 (not previously PI-approved/frozen; Rebecca's signature on `DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md` is the gate before execution — see §0). Acceptance (§5.4) applies to an **exact `(W, N_w)` geometry**, not merely to total query count `Q`; geometries tied on `Q` are distinguished and ordered deterministically by the tie-break above (larger `N_w`, then smaller `W`) and are **not** merged or pooled. `[PROPOSED — §8.2, Rebecca directive]`

| idx | W | N_w | Q = W·N_w | queries per 5-seed run (W·N_w·4·5) |
|---|---|---|---|---|
| 1 | 50 | 4 | 200 | 4,000 |
| 2 | 50 | 8 | 400 | 8,000 |
| 3 | 100 | 4 | 400 | 8,000 |
| 4 | 50 | 16 | 800 | 16,000 |
| 5 | 100 | 8 | 800 | 16,000 |
| 6 | 200 | 4 | 800 | 16,000 |
| 7 | 50 | 32 | 1,600 | 32,000 |
| 8 | 100 | 16 | 1,600 | 32,000 |
| 9 | 200 | 8 | 1,600 | 32,000 |
| 10 | 400 | 4 | 1,600 | 32,000 |
| 11 | 50 | 64 | 3,200 | 64,000 |
| 12 | 100 | 32 | 3,200 | 64,000 |
| 13 | 200 | 16 | 3,200 | 64,000 |
| 14 | 400 | 8 | 3,200 | 64,000 |
| 15 | 100 | 64 | 6,400 | 128,000 |
| 16 | 200 | 32 | 6,400 | 128,000 |
| 17 | 400 | 16 | 6,400 | 128,000 |
| 18 | 200 | 64 | 12,800 | 256,000 |
| 19 | 400 | 32 | 12,800 | 256,000 |
| 20 | 400 | 64 | 25,600 | 512,000 |

Locked dose requirement preserved: four dose levels `{0, 1, 2, 3}`; the sweep shall not reduce noise doses below the locked minimum of three `[BAR-Entry 11]`.

## 4. The 240 cells: nuisance grid × operating grid (copied exactly from `b139749` / v2.2 §8)

- **Nuisance combinations (15):** `α ∈ {0.0, 0.02, 0.05, 0.1, 0.2}` (5) × `v_mult ∈ {0.5, 1.0, 2.0}` (3) = 15 `[PROPOSED — §8.3]`. `v_logit = v_mult × V_REF` with `V_REF = 1.0` `[PROPOSED — §5 XF-8]`.
- **Operating cells (16):** `C_min ∈ {0.5, 0.6, 0.7, 0.8}` (4) × `η ∈ {0.01, 0.05, 0.1, 0.2}` (4) = 16 `[PROPOSED — §8.3]`.
- 15 × 16 = 240 cells per geometry `[PROPOSED — §8.3]`.

## 5. Scientific calculation — direct false-kill, no bootstrap

Use the existing direct false-kill calculation implemented at `b139749` (`_worker_combo`, `_worker_null_control`, `run_power_analysis`). Two arms per cell, both at 2,000 simulations:

- **Combo arm:** calibrated `σ_dose` per `(α, v)` pair (calibrated once at the reference operating point `(C_min, η) = (0.7, 0.1)` `[PROPOSED — §8]`, then reused for all 16 operating cells of that pair). Per seed `s`, computes **two** direct statistics from the same four dose-level regulation-error summaries `D̄_{s,ℓ} = mean_w (r_{s,ℓ,w} − R*)` (ℓ ∈ {0,1,2,3}) already used by the β* estimator: (i) the standardized slope `β*_s = β_s / σ_pool,s` via the identical §2 XF-5 estimator `[OP — Sol-XF-5, adopted operationalization]` `[BAR-Entry 11]` (5 seeds per simulation `[BAR-Entry 11]`; zero-variance `σ_pool,s = 0` → `INSTRUMENT_FAILURE` `[OP — Sol-XF-5, adopted operationalization]`); and (ii) the per-seed Spearman ρ `ρ_s` defined in §5.1 (direct calculation, authorized per `REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION`).
- **Null-control arm:** `σ_dose = 0.0` (no true effect). Computes the false-pass rate.

**P3 tag convention (per CRITIC NB4):** the inherited `[Sol-XF-5]` closure labels (from frozen v2.2 line 81 / the L8 crossfamily SOL review) are not one of the four P3 source classes (`[LAW-Lx]`/`[BAR-Entry n]`/`[OP-Entry n]`/`[PROPOSED]`). They are re-tagged here as `[OP — Sol-XF-5, adopted operationalization]` — i.e., adopted-operationalization (`[OP]`) class, with the crossfamily closure label `Sol-XF-5` retained for traceability. The numeric thresholds that matter (0.2, 0.10, 5 seeds, ρ ≥ 0.8) remain tagged `[BAR-Entry 11]` / `[PROPOSED]`.

### 5.1 Direct calculations: per-seed Spearman ρ, complete-verdict primary, diagnostics, null false-pass

**Per-seed Spearman ρ (direct calculation, authorized per `REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION`):** for each seed `s`, from the four dose-level regulation-error summaries `D̄_{s,ℓ}` (ℓ ∈ {0,1,2,3}) already used by the β* estimator:

- **Dose ranks:** `(1, 2, 3, 4)` (one per dose level, in dose order). `[PROPOSED — §8]`
- **Response ranks:** ascending midranks of `D̄_{s,ℓ}`; tied values receive the arithmetic mean of their occupied one-based ranks. `[PROPOSED — §8]`
- **Statistic:** the Pearson correlation between the dose ranks and the response midranks. `[PROPOSED — §8]`
- **Locked predicate:** `ρ_s ≥ 0.8` `[BAR-Entry 11]` (frozen v2.2 line 44).
- **Zero response-rank variance:** if all `D̄_{s,ℓ}` are equal (the response-rank vector has zero variance), `ρ_s` is **undefined** and counts as a **failure of the ρ predicate** (not `INSTRUMENT_FAILURE`). `[PROPOSED — §8, Rebecca directive]`
- **Non-finite or structurally invalid inputs:** routed through the §5.6 decision tree; the disposition is **either** apparatus-invalid exclusion (independent apparatus fault) **or** undefined-`ρ_s` predicate failure (no apparatus fault) — not a direct predicate pass/fail and not automatic `INSTRUMENT_FAILURE`. `[PROPOSED — §8, Rebecca directive]`
- **Floating-point tolerance (locked-bar comparison):** the locked predicate comparison is `ρ_s >= 0.8` `[BAR-Entry 11]` with a **minimal, explicit, tested** comparison tolerance `RHO_COMPARE_EPS = 1e-12` `[PROPOSED — §8, Rebecca directive]`. Predicate **passes** iff `ρ_s >= 0.8` **OR** `abs(ρ_s - 0.8) <= RHO_COMPARE_EPS`. This tolerance exists only to absorb binary64 roundoff at the exact-threshold value (e.g., the `[1,0,2,3]` case computes to `0.7999999999999999`, the roundoff representation of exactly `0.8`); it must **not** materially soften the bar. A test shall assert that `ρ = 0.8 - 2·RHO_COMPARE_EPS` **fails** (so the locked 0.8 bar is not moved). Tie detection for midranks is **binding** as exact finite binary64 equality — no separate tie tolerance, no implementer discretion.

The `b139749` baseline computes per-seed `β*_s` (and transiently the dose-level summaries `D̄_{s,ℓ}` inside `beta_star_for_seed`) but does **not** expose per-seed `ρ_s` or durable `D̄` arrays. This spec adds the direct per-seed Spearman ρ calculation per Rebecca's authorization: the TASK BUILDER shall compute `ρ_s` in the same estimator path where `D̄` is available (reusing the four dose-level summaries already computed for `β*_s`), or extend the per-seed result record to return `ρ_s`. This is the minimum computation required for the complete frozen-v2.2 predicate; it is a direct, deterministic, non-resampling statistic — not a quorum/fallback/bootstrap/Wilson procedure.

**Rates (per cell):**

- **PRIMARY (complete-verdict any-seed false-kill rate):** `complete_verdict_false_kill_rate` = `P(any seed s has β*_s < 0.2 OR ρ_s undefined OR ρ_s < 0.8)`, i.e. the fraction of valid simulations in which **any** of the 5 seeds fails **either** per-seed predicate (β*_s < 0.2 `[BAR-Entry 11]` OR ρ_s undefined OR ρ_s < 0.8 `[BAR-Entry 11]`). This is the complete frozen-v2.2 any-seed scoring-verdict false-kill rate. `[PROPOSED — primary metric]`
- **DIAGNOSTIC (β*-only any-seed):** `diagnostic_beta_only_any_seed_false_kill_rate` = `P(any seed β*_s < 0.2)` (the `b139749` `false_kill_rate_per_seed`, code line 808). Captures only the β*-predicate; a **lower bound** on the complete-verdict primary. `[PROPOSED — diagnostic; NF-IMPL-2 in b139749]`
- **DIAGNOSTIC (five-seed mean):** `diagnostic_five_seed_mean_false_kill_rate` = `P(5-seed mean β* < 0.2)` (the `b139749` `false_kill_rate`). `[PROPOSED — diagnostic; NF-IMPL-2 in b139749]`
- **Null-control false-pass:** `null_control_false_pass_rate` = fraction of valid null-control simulations in which **every** seed satisfies **both** predicates (β*_s ≥ 0.2 `[BAR-Entry 11]` AND ρ_s ≥ 0.8 `[BAR-Entry 11]`). `[PROPOSED — Rebecca directive]`

`BETA_STAR_BAR = 0.2` `[BAR-Entry 11]`. `RHO_BAR = 0.8` `[BAR-Entry 11]`. `FALSE_KILL_THRESHOLD = 0.10` `[PROPOSED — apparatus parameter, §8]`.

### 5.2 PRIMARY and DIAGNOSTIC designation

The frozen L8 v2.2 spec states the locked bars run **per seed**:

> "The locked bars run on D: Spearman ρ(dose, D) ≥ 0.8 `[BAR-Entry 11]` and standardized slope ≥ 0.2 `[BAR-Entry 11]`, per seed."
> — `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (c7d7bed), line 44.

A candidate run fails the scoring verdict if **any seed** fails **either** predicate (ρ < 0.8 **or** β*_s < 0.2). Designation:

- **PRIMARY = `complete_verdict_false_kill_rate`** — the complete frozen-v2.2 any-seed scoring-verdict false-kill rate (any seed fails β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8). `[PROPOSED — primary metric, Rebecca-authorized]`
- **DIAGNOSTIC = `diagnostic_beta_only_any_seed_false_kill_rate`** (β*-only any-seed; a lower bound on the primary).
- **DIAGNOSTIC = `diagnostic_five_seed_mean_false_kill_rate`** (5-seed mean).

This completes (does not reverse) the prior any-seed designation direction: the primary is now the **complete** frozen-v2.2 predicate (β* AND ρ, any-seed), where previously the β*-only any-seed rate stood in as a lower-bound surrogate pending the ρ calculation. The β*-only and 5-seed-mean rates are retained as diagnostics and **do not gate** battery acceptance or selection. This designates the primary metric and recomputes acceptance against it; it does not alter the locked bars (β* ≥ 0.2, ρ ≥ 0.8), `FALSE_KILL_THRESHOLD`, or either direct formula. The v2.4 §8.1 pooled-bootstrap predicate `[BAR-Entry 11.3]` is **not** part of this primary metric (frozen-v2.2 bars only, per Rebecca's directive).

### 5.3 STOP resolution and mismatch memorialization (flagged for CRITIC / Rebecca)

The prior ARCHITECT STOP (`handoffs/ARCHITECT_L8_FULLSCREEN_STOP_ITEM1_RHO.md`) correctly identified that `b139749` does not compute per-seed Spearman ρ, so the complete frozen-v2.2 predicate was not computable from existing arrays. Rebecca authorized the direct per-seed Spearman ρ calculation (`docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md`); this spec adds that direct calculation (§5.1) and designates the complete any-seed predicate as primary (§5.2). **CRITIC and Rebecca must specifically review** the per-seed ρ definition (§5.1), the complete-verdict primary designation (§5.2), and the apparatus-validity rules (§5.6) before TASK BUILDER implementation. The `b139749` baseline's `false_kill_rate` (5-seed mean) as the prior key output and `false_kill_rate_per_seed` (β*-only, NF-IMPL-2) are both retained as diagnostics. A reference cell from `6d455bb` (`α=0.0, v_mult=0.5, C_min=0.5, η=0.01`, `N_w=4`) illustrates the materiality of the β*-predicate portion alone: `false_kill_rate = 0.0565` (passes 0.10) vs `false_kill_rate_per_seed = 0.7483` (fails) — the complete-verdict primary (which also includes the ρ predicate) is expected to differ further and is the consequential battery-sizing metric.

### 5.4 False-kill target, geometry acceptance, and boundary escalation

The applicable false-kill target is `FALSE_KILL_THRESHOLD = 0.10` `[PROPOSED — apparatus parameter, §8]` (v2.2 §8: false-kill probability exceeding 0.10 escalates battery size to G3). For each geometry:

- **geometry-level maximum primary false-kill** = `max` over its 240 cells of `complete_verdict_false_kill_rate` (only over cells with no apparatus-invalid repetition; apparatus-invalid cells are excluded and flagged).
- **meets_target** = `(no apparatus-invalid cells in the geometry) AND (geometry-level maximum primary false-kill ≤ 0.10)`. A geometry with any apparatus-invalid cell cannot qualify. Acceptance applies to an **exact `(W, N_w)` geometry** (not merely total query count `Q`).

**Minimum acceptable battery** = the first geometry in the §3 ordering whose `meets_target` is true. **Boundary-escalation rule (Rebecca directive, Item 3):** if **no** geometry passes (`meets_target` false for all 20), **OR** the first geometry whose `meets_target` is true lies on a tested boundary, **STOP** and escalate to ARCHITECT/Rebecca — do not auto-accept a boundary solution; return for a ruling. A geometry lies on a **tested boundary** iff its `W` is the minimum (50) or maximum (400) of the `W ∈ {50,100,200,400}` set, **or** its `N_w` is the minimum (4) or maximum (64) of the `N_w ∈ {4,8,16,32,64}` set (i.e., any edge of the `W×N_w` grid). `[PROPOSED — §8.2, Rebecca directive]` (The CRITIC verifies this exact definition of "tested boundary.")

**P3 / O-15 gating note:** the primary metric `complete_verdict_false_kill_rate` is `[PROPOSED]`, and geometry acceptance (`meets_target` / minimum acceptable battery) is a `[PROPOSED]`-gated **diagnostic selection**, not a scoring verdict. Because the run is O-15 diagnostic-only and authorizes no scoring, no `[PROPOSED]` value gates scoring here; however, the minimum-acceptable-battery determination (and any boundary-escalation ruling) requires **Rebecca sign-off before any binding or downstream use**. The TASK BUILDER shall record the output artifact's own SHA-256 in the run handoff (§7.2) for reproducibility verification.

### 5.5 Deterministic tests (required)

The implementation SHALL include deterministic tests with assertions covering each case below. No test may be a no-op or unconditional pass; each must assert the exact outcome against a pre-computed expected value. `[PROPOSED — Rebecca directive]` Cases 1–5 are **ρ unit tests** (dose ranks `[1,2,3,4]` fixed; only `D̄` varies); `β*` is not asserted from `D̄` alone (it depends on window-level deviations and `σ_pool`). The locked predicate comparison uses `RHO_COMPARE_EPS = 1e-12` as defined in §5.1 (pass iff `ρ_s >= 0.8` OR `abs(ρ_s - 0.8) <= RHO_COMPARE_EPS`); deterministic test value checks may use a fixed numeric tolerance such as `abs(actual − expected) <= 1e-12` `[PROPOSED — §8]`.

1. **Perfect increasing monotonicity:** `D̄ = [0, 1, 2, 3]` → response ranks `[1,2,3,4]` → `ρ_s = 1.0` → **passes** the ρ predicate.
2. **Adjacent-inversion / threshold case:** `D̄ = [1, 0, 2, 3]` → response ranks `[2,1,3,4]` → `ρ_s = 0.8` (computed `0.7999999999999999`, the binary64 roundoff of exactly `0.8`) → **passes** the ρ predicate via `abs(ρ_s - 0.8) <= RHO_COMPARE_EPS` (at the locked threshold).
2a. **Threshold-tolerance (no-softening) test:** assert that `ρ = 0.8 - 2·RHO_COMPARE_EPS` **fails** the ρ predicate, confirming the tolerance does not materially move the 0.8 bar. `[PROPOSED — §8]`
3. **Tied responses:** `D̄ = [0, 0, 2, 3]` → midranks `[1.5, 1.5, 3, 4]` → `ρ_s = sqrt(0.9) ≈ 0.9486832980505138` → **passes** the ρ predicate.
4. **Constant responses:** `D̄ = [c, c, c, c]` (zero response-rank variance) → `ρ_s = undefined` → **failure of the ρ predicate** (not `INSTRUMENT_FAILURE`).
5. **Decreasing responses:** `D̄ = [3, 2, 1, 0]` → response ranks `[4,3,2,1]` → `ρ_s = -1.0` → **fails** the ρ predicate (`< 0.8`).
6. **Non-finite inputs:** a `D̄` containing `NaN`/`inf` is routed through the §5.6 apparatus-validity decision tree (not scored directly as a predicate pass/fail); assert the correct disposition (apparatus-invalid if an independent apparatus fault; otherwise `ρ_s` undefined → ρ-predicate failure).
7. **Complete-verdict aggregation across five seeds:** an aggregation-unit test over precomputed per-seed stats `(β*_s, ρ_s)` (full window-level fixtures are required if the `β*` estimator itself is exercised). Exact cases:
   - **All-pass:** five seeds `(β*=0.25, ρ=0.8)`, `(0.25, 0.8)`, `(0.25, 0.8)`, `(0.25, 0.8)`, `(0.25, 0.8)` → `complete_verdict_false_kill_rate` outcome = **pass**.
   - **Fail (β* predicate):** seeds `(0.25, 0.8)`, `(0.19, 0.8)`, `(0.25, 0.8)`, `(0.25, 0.8)`, `(0.25, 0.8)` — one seed `β*=0.19 < 0.2` → complete verdict **fails**.
   - **Fail (undefined ρ):** seeds `(0.25, 0.8)`, `(0.25, undefined)`, `(0.25, 0.8)`, `(0.25, 0.8)`, `(0.25, 0.8)` — one seed `ρ` undefined → complete verdict **fails**.
   - **Fail (ρ < 0.8):** seeds `(0.25, 0.8)`, `(0.25, 0.8)`, `(0.25, 0.79)`, `(0.25, 0.8)`, `(0.25, 0.8)` — one seed `ρ=0.79 < 0.8` → complete verdict **fails**.
   Assert `complete_verdict_false_kill_rate` = fail iff **any** seed fails **either** predicate.

### 5.6 Apparatus-validity rules for non-finite or structurally invalid inputs (Rebecca directive)

Non-finite (`NaN`/`inf`) or structurally invalid (wrong length/shape) per-seed `D̄_{s,ℓ}` inputs are routed through this decision tree (not scored directly as a predicate pass/fail, and not automatically `INSTRUMENT_FAILURE`). `[PROPOSED — Rebecca directive]`

1. **Apparatus fault:** if the non-finite/invalid input arises from an independent apparatus-validity failure (e.g., the simulation produced no valid dose-level summary), the repetition is **apparatus-invalid**: excluded from the false-kill/false-pass denominators, counted and reported separately; if any apparatus-invalid repetition occurs for a cell, that cell is `apparatus-invalid` and cannot qualify a geometry.
2. **No apparatus fault, non-finite/invalid input:** if the non-finite/invalid input arises **without** an independent apparatus fault, the repetition is **retained in the denominator** and the seed's `ρ_s` is **undefined** (a Pearson correlation cannot be computed) → **failure of the ρ predicate** for that seed (and, if `β*_s` is also undefined, failure of the β* predicate); this contributes to `complete_verdict_false_kill_rate` — **not** `INSTRUMENT_FAILURE`.
3. **Finite, shape-valid, zero response-rank variance:** if all `D̄_{s,ℓ}` are finite and shape-valid but equal (the response-rank vector has zero variance), `ρ_s` is **undefined** → **failure of the ρ predicate** — **not** `INSTRUMENT_FAILURE`.

Ordinary per-seed statistical failures (`β*_s < 0.2`, `ρ_s < 0.8`, `ρ_s` undefined) are **never** reclassified as `INSTRUMENT_FAILURE` (no-relabeling rule; O-14/D1/D5). `complete_verdict_false_kill_rate` uses the valid true-effect denominator (apparatus-invalid repetitions excluded); `null_control_false_pass_rate` uses the valid null-control denominator.

## 6. Preserved verified behavior (do not modify)

From `b139749`: `calibrate_sigma_dose` numerical algorithm; §2 XF-5 estimator; combo-seed and per-simulation RNG derivation; direct false-kill formulas; null-control calculation; sensitivity-map logic except where the battery-geometry loop necessarily wraps the existing cell loop; misspecification profiles; R8 guard; JSON write-order fix; functional calibration and simulation multiprocessing.

### 6.1 Seed derivation across the 20 geometries (rule closure)

The frozen v2.2 spec defines **no geometry seed dimension** (only superseded v2.4 §8.9.3 machinery does, which is prohibited). Therefore the existing combo-seed and per-simulation RNG derivation is **reused unchanged** across all 20 geometries:

- `base_seed = combo_seed(α, v_mult, C_min, η)` = `int.from_bytes(sha256("alpha=…|vmult=…|cmin=…|eta=…").digest()[:8], "little") % 2^31` `[PROPOSED — §8.4, b139749]`.
- per-simulation seed = `(base_seed + i·N_SEEDS + s) % 2^31` `[PROPOSED — §8.4, b139749]`.

The geometry is distinguished by the `(W, N_w)` data shape (the simulation consumes `W` queries × `N_w` windows × 4 doses × 5 seeds of RNG draws); the seed derivation itself is not extended and no new geometry seed namespace is introduced. **Known, accepted property:** cells sharing `(α, v, C_min, η)` across geometries share `base_seed`, so their first per-simulation RNG draws coincide before the `W`/`N_w`-dependent draw counts diverge. This is a deliberate preservation of the verified derivation per the handoff ("do not modify combo-seed and per-simulation RNG derivation"); CRITIC should confirm this is acceptable for the screen's false-kill rate estimates (aggregated over 2,000 independent simulations per cell per geometry).

## 7. Output requirements

### 7.1 Single machine-readable artifact

Path: `diagnostics/l8_g2g4_minimal_full_screen.json` `[PROPOSED]`. Exact schema, field order, and types (unknown fields fail validation; `NaN` sanitized to `null`):

```
{
  "header": {
    "schema_version": "l8-g2g4-minimal-fullscreen-v1",   // [PROPOSED]
    "artifact_date": "2026-08-20",                       // [OP — P4]
    "regime": "B",
    "spec_regime": "L8 v2.2 (c7d7bed) + minimal full-screen spec (this commit)",
    "code_baseline_sha": "b1397498ca369067e956479e6c2bd6b0793c3e89",
    "reference_artifact_sha": "6d455bb878f4b52a5b5564afac38d6fb3a20d4b3",
    "constants": {
      "W_set": [50,100,200,400], "N_w_set": [4,8,16,32,64],
      "alphas": [0.0,0.02,0.05,0.1,0.2], "v_mults": [0.5,1.0,2.0],
      "c_mins": [0.5,0.6,0.7,0.8], "etas": [0.01,0.05,0.1,0.2],
      "N_SEEDS": 5, "L_DOSES": 4, "R_STAR": 0.1, "TRUE_BETA_STAR": 0.3,
      "BETA_STAR_BAR": 0.2, "RHO_BAR": 0.8, "RHO_COMPARE_EPS": 1e-12, "FALSE_KILL_THRESHOLD": 0.10, "V_REF": 1.0,
      "CAL_REF_C_MIN": 0.7, "CAL_REF_ETA": 0.1
    },
    "run_config": {
      "n_geometries": 20, "n_cells_per_geometry": 240,
      "n_sims_per_cell_per_arm": 2000, "arms": ["combo","null_control"],
      "n_workers": 16, "pool": "multiprocessing.Pool", "chunksize": 1
    },
    "compliance": {
      "P3_source_tags": "all thresholds tagged",
      "P4_regime_dating": "header states date and regime",
      "candidate_blind": "seeds from parameter-combo hashes only; no candidate data",
      "O_15": "diagnostic-only; authorizes no scoring"
    }
  },
  "geometries": [
    {
      "geometry_index": <int 0..19>, "W": <int>, "N_w": <int>,
      "Q_per_dose": <int W*Nw>, "queries_per_five_seed_run": <int W*Nw*4*5>,
      "max_primary_false_kill": <float max over 240 cells of complete_verdict_false_kill_rate>,
      "has_apparatus_invalid_cell": <bool: any cell in this geometry is apparatus-invalid>,
      "meets_target": <bool (no apparatus-invalid cells) AND max_primary_false_kill <= 0.10>,
      "on_tested_boundary": <bool: W is min(50) or max(400), or N_w is min(4) or max(64)>,
      "cells": [
        { "geometry_index": <int>, "W": <int>, "N_w": <int>,
          "alpha": <float>, "v_mult": <float>, "c_min": <float>, "eta": <float>,
          "base_seed": <int>,
          "cell_apparatus_invalid": <bool: any apparatus-invalid repetition in this cell>,
          "n_sims_attempted_true_effect": 2000, "n_valid_true_effect": <int>,
          "n_apparatus_invalid_true_effect": <int>, "n_instrument_failures_true_effect": <int>,
          "n_sims_attempted_null_control": 2000, "n_valid_null_control": <int>,
          "n_apparatus_invalid_null_control": <int>, "n_instrument_failures_null_control": <int>,
          "complete_verdict_false_kill_rate": <float PRIMARY: valid-true-effect denominator, P(any seed β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8)>,
          "diagnostic_beta_only_any_seed_false_kill_rate": <float valid-true-effect denominator, P(any seed β*_s<0.2)>,
          "diagnostic_five_seed_mean_false_kill_rate": <float valid-true-effect denominator, P(5-seed mean β*<0.2)>,
          "null_control_false_pass_rate": <float valid-null-control denominator, P(every seed β*_s>=0.2 AND ρ_s>=0.8)>,
          "mean_beta_star": <float>, "mean_beta_star_null": <float> }
        // ...exactly 240 ordered cells: for alpha in alphas: for v_mult in v_mults: for c_min in c_mins: for eta in etas
      ]
    }
    // ...exactly 20 geometries in §3 order
  ],
  "selection": {
    "false_kill_target": 0.10,
    "primary_metric": "complete_verdict_false_kill_rate",
    "diagnostic_metrics": ["diagnostic_beta_only_any_seed_false_kill_rate", "diagnostic_five_seed_mean_false_kill_rate"],
    "minimum_geometry_satisfying_target": <{geometry_index,W,N_w,Q_per_dose} | null>,
    "first_passing_on_tested_boundary": <bool | null>,
    "rule": "first geometry in §3 Q-ordering whose max_primary_false_kill <= 0.10; null if none (STOP); if first passing geometry is on a tested boundary, STOP and escalate (§5.4)",
    "scoring_verdict_alignment_note": "primary is the complete frozen-v2.2 any-seed scoring-verdict false-kill rate (β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8); frozen-v2.2 bars only; no pooled-bootstrap predicate; see §5.1-§5.3"
  }
}
```

Cell ordering within each geometry is the nested loop order `alpha → v_mult → c_min → eta` (15 × 16 = 240), matching `b139749`'s `work_items` construction. The artifact is written once, atomically, after all 20 geometries complete.

### 7.2 Short human-readable run handoff

Path: `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md` `[PROPOSED]`. Contents: regime header; `code_baseline_sha` and `reference_artifact_sha`; the **output artifact's own SHA-256** (computed over the canonical JSON written by the atomic write, for reproducibility verification — per CRITIC NB2); 20-row geometry table with `Q`, `max_primary_false_kill` (= max over cells of `complete_verdict_false_kill_rate`), `meets_target`, `on_tested_boundary`; the `minimum_geometry_satisfying_target` or explicit STOP / boundary-escalation STOP (§5.4); total elapsed seconds; instrument-failure total count; the §5.3 STOP-resolution/mismatch memorialization verbatim; "Diagnostic-only (O-15). This authorizes NO scoring."

## 8. Candidate-blind and O-15 labeling

All simulations are candidate-blind `[OP-Entry 76]` (Ruling 9): simulation seeds derive from parameter-combo hashes only; no candidate output is an input anywhere. The entire run is O-15 diagnostic-only and labeled as such in the artifact header and handoff `[OP — O-15]`. No artifact from this run is scoring evidence.

## 9. Explicitly prohibited (TASK BUILDER)

No bootstrap, no Wilson intervals, no `predicate_false_kill_rates`/`failure_mask_counts`/finalist confirmation, no `resolved_config.json` manifest, no rehearsal fixtures, no fault injection, no sensitivity/misspecification recomputation, no `(C_min,η)` selection, no scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17, no reclassification of statistical failures as INSTRUMENT_FAILURE, no extension of the geometry grid beyond the 20 in §3.
