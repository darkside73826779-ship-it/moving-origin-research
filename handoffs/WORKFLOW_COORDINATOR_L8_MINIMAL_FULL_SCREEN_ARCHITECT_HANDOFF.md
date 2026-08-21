# WORKFLOW COORDINATOR → ARCHITECT Handoff — Minimal L8 Full-Screen Specification

**Date:** 2026-08-20  
**Regime:** B  
**Gate served:** Minimal executable specification for the L8 G2–G4 full battery-geometry screen  
**Next recipient:** Freshly reinitialized ARCHITECT  
**Required route after ARCHITECT:** Fresh-context CRITIC → Rebecca → TASK BUILDER  

## Authority and scope

Rebecca has established the full-screen run parameters. This handoff authorizes a **minimal specification delta only**. Do not recreate the superseded v2.3–v2.7 benchmark, bootstrap, rehearsal-fixture, fault-injection, canonical-artifact, or A1/A2/B machinery.

Authority chain: Rebecca > constitution laws > this handoff > agent judgment. If the requested minimal contract conflicts with a locked law or an unresolved scoring-verdict rule, STOP and report the exact conflict. Do not invent.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub repository | `darkside73826779-ship-it/moving-origin-research` |
| Current main when issued | `f4e22317ebe0e3e1a7dbee0b81ef8c3fb9839b2b` |
| Frozen L8 v2.2 base | `c7d7bed6b259fb5163fb610098ea12aed1d3d65e` on `architect/l8-instantiation-v2.2-fresh` |
| Frozen L8 spec path | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| Verified executable baseline | `diagnostics/l8_power_analysis.py` at `b1397498ca369067e956479e6c2bd6b0793c3e89` on `taskbuilder/l8-power-analysis` |
| Verified complete reference artifact | `diagnostics/l8_power_analysis_results.json` at `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3` |
| Reference artifact SHA-256 | `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21` |
| Rebecca feasibility ruling | `docs/rulings/REBECCA_L8_1000_REP_FEASIBILITY_AUTHORIZATION.md` at `d08cb7eefec67609a3ea3cee0eb20da22f78c40a` |
| M4 specification | `specs/m4_specification.md` on main |
| M4 task specification | `specs/m4_task_spec.md` on main |
| L8 locked bars | `docs/rulings/M0_DECISION_SHEET.md` on main |
| Constitution | `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on main |
| Provenance | `docs/rulings/provenance_log.md` on main |

## Rebecca-established run

Specify exactly this full screen:

- **20 battery geometries**
- **240 cells per geometry**
  - 15 nuisance combinations
  - 16 `(C_min, eta)` operating cells
- **2,000 simulations per cell**
- Total: **20 × 240 × 2,000 = 9,600,000 simulations**
- Use the verified parallel execution path.
- Operational worker setting: **16 workers**.
- Estimated wall-clock runtime from the verified reference run: **approximately 1.5–2 hours**.

Reference timing:

- `6d455bb`: 240 cells × 10,000 simulations = 2,400,000 simulations
- Runtime: 1,357.6829717159271 seconds = 22.63 minutes
- Full screen: 9,600,000 / 2,400,000 = 4× the reference simulation count
- Linear estimate: 4 × 22.63 minutes = approximately 90.5 minutes
- Operational estimate including overhead: **1.5–2 hours**

## Scientific calculation

Use the **existing direct false-kill calculation implemented at `b139749`**.

- No bootstrap.
- No 5,000-valid-bootstrap predicate.
- No 5,500-attempt rule.
- No pooled bootstrap confidence interval.
- No feasibility benchmark before the full screen.
- No serial benchmark.

The existing verified code calculates:

- `false_kill_rate`: direct false-kill rate under the five-seed aggregated verdict.
- `false_kill_rate_per_seed`: direct any-seed false-kill diagnostic.

The ARCHITECT must verify the actual M4 scoring-verdict rule against the M4 specification, task specification, M0 decision sheet, and controlling rulings:

1. Designate the direct false-kill rate corresponding to the actual scoring verdict as **primary**.
2. Retain the other direct false-kill rate as a **diagnostic**.
3. If the controlling documents do not resolve the scoring-verdict rule unambiguously, STOP and identify the exact conflicting text for Rebecca. Do not choose a rule.

## Minimal specification requirements

The specification must define only what TASK BUILDER needs to implement the full screen:

1. The exact 20 battery geometries, copied from the authoritative pre-registered geometry list. Do not redesign the geometry set.
2. The existing 15 nuisance combinations and 16 operating cells, copied exactly from the verified baseline/specification.
3. The 2,000-simulation count per cell.
4. The verified parallel path and 16-worker run setting.
5. The actual scoring-verdict-aligned primary false-kill calculation and the secondary diagnostic calculation.
6. Output requirements sufficient to report, for every geometry and cell:
   - attempted and valid simulations;
   - primary false-kill rate;
   - diagnostic false-kill rate;
   - false-pass rate;
   - instrument-failure count;
   - geometry-level maximum primary false-kill;
   - the minimum geometry satisfying the applicable false-kill target, if any.
7. A single machine-readable output artifact and a short human-readable run handoff.
8. Candidate-blind, O-15 diagnostic labeling.

## Executability obligation

Apply the updated ARCHITECT initialization script on main/project files.

Before claiming the minimal spec is executable:

- Trace every value the TASK BUILDER must supply.
- Confirm every grid, geometry, threshold, field, ordering, and output path is explicit.
- Do not use phrases such as “the same fixture” or “as appropriate.”
- Do not add fixtures, artifact pairs, stochastic fixture digests, fault hooks, rehearsal cases, bootstrap mechanics, publication transactions, or commit-lifecycle machinery unless they are strictly necessary to execute this full screen. They are not authorized by this handoff.
- If the TASK BUILDER would need to invent a rule, the specification is incomplete. Close only that rule; do not expand scope.

## Preserved verified behavior

Do not modify:

- `calibrate_sigma_dose` numerical algorithm;
- §2 XF-5 estimator;
- combo-seed and per-simulation RNG derivation;
- direct false-kill formulas;
- null-control calculation;
- sensitivity-map logic except where the battery-geometry loop necessarily wraps the existing cell loop;
- misspecification profiles;
- R8 guard;
- JSON write-order fix;
- functional calibration and simulation multiprocessing at `b139749`.

## Explicitly prohibited

- No v2.3–v2.7 benchmark or bootstrap machinery.
- No 1,000-repetition feasibility benchmark.
- No 48-billion-bootstrap workload.
- No A1/A2/B lifecycle.
- No rehearsal fixture or 12-case fault-injection suite.
- No serial benchmark.
- No scoring or protected-seed access.
- No seeds 201–203 or 301–303.
- No sensitivity/misspecification rerun in this step.
- No G2–G4 freeze or ruling by ARCHITECT.
- No merge to main.
- No L15/L16/L17 before M5.
- No reclassification of ordinary statistical failures as INSTRUMENT FAILURE.

## Required ARCHITECT output

Commit to a new `architect/` branch and return:

1. A short minimal full-screen specification.
2. A companion changelog.
3. A TASK BUILDER implementation handoff.
4. An executability trace showing that every required implementation value is explicit.
5. Confirmation that no prohibited machinery was added.
6. Branch name and commit SHA.

**Next recipient:** Fresh-context CRITIC. The CRITIC must review both internal consistency and end-to-end executability under the updated CRITIC initialization script. On CLEAR, return to Rebecca before TASK BUILDER implementation.
