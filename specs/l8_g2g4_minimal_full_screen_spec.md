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
| M4 specification / task spec / M0 decision sheet / constitution v2 | on `main` (`f4e22317`): `specs/m4_specification.md`, `specs/m4_task_spec.md`, `docs/rulings/M0_DECISION_SHEET.md`, `docs/ARCHITECTURAL_CONSTITUTION_v2.md` |

## 1. Scope, authority, and prohibitions

### 1.1 What this spec is

A minimal, executable specification for one full screen: 20 battery geometries × 240 cells per geometry × 2,000 simulations per cell, evaluated with the **existing direct false-kill calculation at `b139749`**. Candidate-blind, synthetic/oracle-only, O-15 diagnostic-only. It authorizes NO scoring, NO G2–G4 freeze, NO protected-seed access.

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

**Prohibited machinery (not recreated, not invoked):** v2.3–v2.7 benchmark/bootstrap machinery; the 1,000-repetition feasibility benchmark; 48-billion-bootstrap workload; A1/A2/B lifecycle; rehearsal fixtures and 12-case fault-injection suite; serial benchmark; Wilson intervals and `predicate_false_kill_rates` / `failure_mask_counts` / finalist 10,000-rep confirmation / `resolved_config.json` manifest machinery from v2.4 §8.9.3–§8.9.4; sensitivity-map / misspecification-stress recomputation and `(C_min, η)` selection; scoring or protected-seed access; seeds 201–203 or 301–303; G2–G4 freeze or ruling by ARCHITECT; merge to main; L15/L16/L17 before M5; reclassification of ordinary statistical failures as INSTRUMENT_FAILURE.

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

The 20 geometries are the Cartesian product of `W ∈ {50, 100, 200, 400}` `[PROPOSED — §8.2]` and `N_w ∈ {4, 8, 16, 32, 64}` `[PROPOSED — §8.2]`, ordered by total queries per dose `Q = W × N_w` ascending, then by larger `N_w`, then by smaller `W` `[PROPOSED — §8.2]`. The grid is **not redesigned**; this table is the authoritative ordered list.

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

- **Combo arm:** calibrated `σ_dose` per `(α, v)` pair (calibrated once at the reference operating point `(C_min, η) = (0.7, 0.1)` `[PROPOSED — §8]`, then reused for all 16 operating cells of that pair). Computes the standardized slope `β*` via the identical §2 XF-5 estimator `[OP — Sol-XF-5, adopted operationalization]` `[BAR-Entry 11]` (5 seeds per simulation `[BAR-Entry 11]`; `β*_s = β_s / σ_pool,s`; zero-variance `σ_pool,s = 0` → `INSTRUMENT_FAILURE` `[OP — Sol-XF-5, adopted operationalization]`).
- **Null-control arm:** `σ_dose = 0.0` (no true effect). Computes the false-pass rate.

**P3 tag convention (per CRITIC NB4):** the inherited `[Sol-XF-5]` closure labels (from frozen v2.2 line 81 / the L8 crossfamily SOL review) are not one of the four P3 source classes (`[LAW-Lx]`/`[BAR-Entry n]`/`[OP-Entry n]`/`[PROPOSED]`). They are re-tagged here as `[OP — Sol-XF-5, adopted operationalization]` — i.e., adopted-operationalization (`[OP]`) class, with the crossfamily closure label `Sol-XF-5` retained for traceability. The numeric thresholds that matter (0.2, 0.10, 5 seeds, ρ ≥ 0.8) remain tagged `[BAR-Entry 11]` / `[PROPOSED]`.

### 5.1 The two direct false-kill rates (as computed at `b139749`)

- `false_kill_rate` = fraction of valid simulations where the **5-seed mean** `β*_run < BETA_STAR_BAR` (0.2) `[BAR-Entry 11]`. Handoff label: "five-seed aggregated verdict." `[PROPOSED — diagnostic; NF-IMPL-2 in b139749]`
- `false_kill_rate_per_seed` = fraction of valid simulations where **any seed** `β*_s < BETA_STAR_BAR` (0.2) `[BAR-Entry 11]` (`b139749` code line 808: `np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1))`). Handoff label: "any-seed." This is the **β*-predicate direct false-kill rate** — it captures only the standardized-slope < 0.2 predicate of the per-seed scoring verdict. It does **not** count runs killed by the `ρ < 0.8` predicate, which is also part of the per-seed scoring verdict (v2.2 line 44). It is therefore a **lower bound on the complete scoring-verdict false-kill rate**, not the full rate. The complete verdict also requires (in v2.4 §8.1) direction + pooled-bootstrap interval `[BAR-Entry 11.3]`, which this minimal spec deliberately does not compute (no bootstrap; §1.3). `[PROPOSED — primary metric; NF-IMPL-2 in b139749]`

`BETA_STAR_BAR = 0.2` `[BAR-Entry 11]`. `FALSE_KILL_THRESHOLD = 0.10` `[PROPOSED — apparatus parameter, §8]`.

### 5.2 Scoring-verdict alignment — PRIMARY and DIAGNOSTIC designation

The frozen L8 v2.2 spec states the locked standardized-slope bar runs **per seed**:

> "The locked bars run on D: Spearman ρ(dose, D) ≥ 0.8 `[BAR-Entry 11]` and standardized slope ≥ 0.2 `[BAR-Entry 11]`, per seed."
> — `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (c7d7bed), line 44.

A candidate run fails the scoring verdict if **any seed** fails **either** predicate (ρ < 0.8 **or** β*_s < 0.2). The false-kill rate corresponding to that verdict is therefore the **any-seed** rate. Of the two rates computable by the direct `b139749` calculation, the any-seed rate is the one that aligns with the per-seed scoring verdict. Designation:

- **PRIMARY = `false_kill_rate_per_seed`** (per-seed / any-seed; matches the "per seed" locked bar). `[PROPOSED — primary metric, flagged to Rebecca in b139749 (NF-IMPL-2)]`
- **DIAGNOSTIC = `false_kill_rate`** (5-seed mean).

**Scope of the primary metric (per CRITIC B2):** `false_kill_rate_per_seed` is the **β*-predicate direct false-kill rate** only (standardized-slope < 0.2, per seed). It is a **lower bound** on the complete scoring-verdict false-kill rate, which also includes the `ρ ≥ 0.8` per-seed predicate (and, in v2.4 §8.1, direction + pooled-bootstrap). This minimal spec deliberately computes only the β*-predicate direct rate (no bootstrap; §1.3); the complete-verdict rate is out of scope and not computed. Rebecca's §5.3 review is therefore of the β*-predicate direct rate as the primary battery-sizing metric, not of the complete-verdict rate.

**Corroborating source (per CRITIC NB1):** v2.4 §8.1 (`4463cbc`) independently resolves the same direction — primary = complete-verdict any-seed rate; "the former five-seed-mean measure… may not gate battery size or selection." v2.2 line 44 remains the primary frozen authority; v2.4 §8.1 is corroborating only (v2.4 is a remediation draft whose own authority is flagged for Rebecca confirmation, §0). Note v2.4 §8.1's complete verdict includes a pooled-bootstrap predicate `[BAR-Entry 11.3]` that this minimal spec deliberately omits in favor of `b139749`'s β*-only direct calculation.

This changes output priority and the geometry-acceptance metric only; it does not alter either direct formula, the `BETA_STAR_BAR`, or the `FALSE_KILL_THRESHOLD`.

### 5.3 Mismatch memorialization (flagged for CRITIC / Rebecca)

The verified baseline `b139749` labels `false_kill_rate` (5-seed mean) as the key false-kill output and flags `false_kill_rate_per_seed` as "NF-IMPL-2: PROPOSED — flagged to Rebecca." This minimal spec resolves the label priority by applying the frozen spec's "per seed" locked-bar text, which makes the any-seed **β*-predicate direct** rate the primary battery-sizing metric. **CRITIC and Rebecca must specifically review this primary/diagnostic mapping before TASK BUILDER implementation**, noting that the primary metric is the β*-predicate direct rate — a **lower bound** on the complete scoring-verdict false-kill rate (which also includes the ρ ≥ 0.8 per-seed predicate; see §5.2 scope). A reference cell (`α=0.0, v_mult=0.5, C_min=0.5, η=0.01`, `N_w=4`) from `6d455bb` illustrates the materiality: `false_kill_rate = 0.0565` (passes 0.10) vs `false_kill_rate_per_seed = 0.7483` (fails). The primary choice is consequential and is the reason the frozen-bar text, not the implementation's convenience label, controls.

### 5.4 False-kill target and geometry acceptance

The applicable false-kill target is `FALSE_KILL_THRESHOLD = 0.10` `[PROPOSED — apparatus parameter, §8]` (v2.2 §8: false-kill probability exceeding 0.10 escalates battery size to G3). For each geometry:

- **geometry-level maximum primary false-kill** = `max` over its 240 cells of `false_kill_rate_per_seed`.
- **meets_target** = `geometry-level maximum primary false-kill ≤ 0.10` (does not exceed the threshold).

**P3 / O-15 gating note (per CRITIC NB2):** the primary metric `false_kill_rate_per_seed` is `[PROPOSED]` (flagged to Rebecca in `b139749`, NF-IMPL-2), and geometry acceptance (`meets_target` / minimum acceptable battery) is a `[PROPOSED]`-gated **diagnostic selection**, not a scoring verdict. Because the run is O-15 diagnostic-only and authorizes no scoring, no `[PROPOSED]` value gates scoring here; however, the minimum-acceptable-battery determination requires **Rebecca sign-off before any binding or downstream use**. The TASK BUILDER shall record the output artifact's own SHA-256 in the run handoff (§7.2) for reproducibility verification.

**Minimum acceptable battery** = the first geometry in the §3 ordering whose `meets_target` is true. **If no tested geometry meets the target, STOP:** return the sweep to ARCHITECT/Rebecca; TASK BUILDER may not extend the grid or invent a battery `[PROPOSED — §8.2]`.

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
      "BETA_STAR_BAR": 0.2, "FALSE_KILL_THRESHOLD": 0.10, "V_REF": 1.0,
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
      "max_primary_false_kill": <float max over 240 cells of false_kill_rate_per_seed>,
      "meets_target": <bool max_primary_false_kill <= 0.10>,
      "cells": [
        { "geometry_index": <int>, "W": <int>, "N_w": <int>,
          "alpha": <float>, "v_mult": <float>, "c_min": <float>, "eta": <float>,
          "base_seed": <int>,
          "n_sims_attempted": 2000, "n_valid": <int>, "n_instrument_failures": <int>,
          "primary_false_kill_rate": <float false_kill_rate_per_seed>,
          "diagnostic_false_kill_rate": <float false_kill_rate>,
          "false_pass_rate": <float from null arm>,
          "n_instrument_failures_null": <int>,
          "mean_beta_star": <float>, "mean_beta_star_null": <float> }
        // ...exactly 240 ordered cells: for alpha in alphas: for v_mult in v_mults: for c_min in c_mins: for eta in etas
      ]
    }
    // ...exactly 20 geometries in §3 order
  ],
  "selection": {
    "false_kill_target": 0.10,
    "primary_metric": "false_kill_rate_per_seed",
    "diagnostic_metric": "false_kill_rate",
    "minimum_geometry_satisfying_target": <{geometry_index,W,N_w,Q_per_dose} | null>,
    "rule": "first geometry in §3 Q-ordering whose max_primary_false_kill <= 0.10; null if none (STOP)",
    "scoring_verdict_alignment_note": "per-seed locked bar (v2.2 line 44); see §5.2-§5.3"
  }
}
```

Cell ordering within each geometry is the nested loop order `alpha → v_mult → c_min → eta` (15 × 16 = 240), matching `b139749`'s `work_items` construction. The artifact is written once, atomically, after all 20 geometries complete.

### 7.2 Short human-readable run handoff

Path: `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md` `[PROPOSED]`. Contents: regime header; `code_baseline_sha` and `reference_artifact_sha`; the **output artifact's own SHA-256** (computed over the canonical JSON written by the atomic write, for reproducibility verification — per CRITIC NB2); 20-row geometry table with `Q`, `max_primary_false_kill`, `meets_target`; the `minimum_geometry_satisfying_target` or explicit STOP; total elapsed seconds; instrument-failure total count; the §5.3 mismatch memorialization verbatim; "Diagnostic-only (O-15). This authorizes NO scoring."

## 8. Candidate-blind and O-15 labeling

All simulations are candidate-blind `[OP-Entry 76]` (Ruling 9): simulation seeds derive from parameter-combo hashes only; no candidate output is an input anywhere. The entire run is O-15 diagnostic-only and labeled as such in the artifact header and handoff `[OP — O-15]`. No artifact from this run is scoring evidence.

## 9. Explicitly prohibited (TASK BUILDER)

No bootstrap, no Wilson intervals, no `predicate_false_kill_rates`/`failure_mask_counts`/finalist confirmation, no `resolved_config.json` manifest, no rehearsal fixtures, no fault injection, no sensitivity/misspecification recomputation, no `(C_min,η)` selection, no scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17, no reclassification of statistical failures as INSTRUMENT_FAILURE, no extension of the geometry grid beyond the 20 in §3.
