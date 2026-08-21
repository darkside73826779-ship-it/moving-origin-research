# WORKFLOW COORDINATOR → TASK BUILDER Handoff — L8 Full-Screen Implementation Authorization

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** TASK BUILDER implementation + run of the CRITIC-cleared amended L8 G2–G4 minimal full-screen spec (Rebecca-authorized).
**Next recipient:** TASK BUILDER. Route after: INTEGRATOR → CRITIC (implementation review) → RECORDER → Rebecca.

## Authorization

Rebecca **AUTHORIZES** the TASK BUILDER to implement the CRITIC-cleared amended spec and run the 19.2M diagnostic screen. This is the final release gate (gate c). All three gates are now satisfied:

- **(a) Fresh-context CRITIC clearance** — ✓ `reviews/critic_l8_g2g4_minimal_fullscreen_amended_review.md` @ `20733d0` (`critic/l8-g2g4-minimal-fullscreen-amended-review`); CLEAR; all 10 review-focus items verified.
- **(b) Rebecca's signed geometry-list adoption** — ✓ `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` (operative, Rebecca-signed 2026-08-20; freezes only the geometry table for this diagnostic execution).
- **(c) Rebecca's explicit TASK BUILDER authorization** — ✓ this handoff.

## Authoritative inputs

| Item | Value |
|---|---|
| Amended spec (CRITIC-cleared) | `architect/l8-g2g4-minimal-fullscreen` @ `2082680` (5 deliverables: spec, changelog, TASK BUILDER handoff, executability trace, DRAFT PI ruling) |
| TASK BUILDER build handoff (ARCHITECT-prepared) | `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` @ `2082680` |
| CRITIC amendment review (CLEAR) | `reviews/critic_l8_g2g4_minimal_fullscreen_amended_review.md` @ `20733d0` |
| Operative geometry ruling | `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` (Rebecca-signed; on GitHub branch `coordinator/l8-geometry-ruling-taskbuilder-auth`, PR [#104](https://github.com/darkside73826779-ship-it/moving-origin-research/pull/104)) |
| ρ-authorization ruling | `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` (operative) |
| Verified code baseline | `b139749` (`diagnostics/l8_power_analysis.py`; reuse `_worker_combo`, `_worker_null_control`, `calibrate_sigma_dose`, `beta_star_for_seed`, `combo_seed`, the §2 XF-5 estimator, the multiprocessing path) |
| Reference artifact | `6d455bb` (cross-check schema only; do not reproduce as output) |
| Frozen L8 v2.2 (locked bars, line 44) | `c7d7bed`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| v2.4 geometry-list source | `4463cbc` on `architect/l8-g2g4-remediation` (§8.2 = 20-geometry list + ordering) |

**Read the ARCHITECT's TASK BUILDER handoff (`specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` @ `2082680`) for the full build instructions, the spec §5.1–§5.6 for the per-seed ρ + complete-verdict predicate, and §7.1/§7.2 for the exact output schema.**

## Authorized scope

Implement the amended spec per the TASK BUILDER handoff: 20 geometries × 240 cells × 2,000 sims/cell × 2 arms = **19.2M** arm-simulations, 16 workers, `multiprocessing.Pool`, chunksize 1, ~1.5–2 h. **PRIMARY = `complete_verdict_false_kill_rate`** = `P(any seed: β*_s < 0.2 OR ρ_s undefined OR ρ_s < 0.8)` (complete frozen-v2.2 any-seed predicate; β*-only + 5-seed-mean are diagnostics). Add the Rebecca-authorized direct per-seed Spearman ρ (Pearson dose-ranks vs response midranks; `RHO_COMPARE_EPS = 1e-12`; zero-variance → undefined → ρ-predicate failure NOT INSTRUMENT_FAILURE). Output the single JSON artifact `diagnostics/l8_g2g4_minimal_full_screen.json` (exact schema §7.1) + handoff `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md` (§7.2), including the **output artifact's own SHA-256**. Include the 7 deterministic-test categories + the no-softening subtest (2a) (§5.5).

## Constraints (binding)

O-14 (no re-run; seeds 201–203/301–303 never rerun), O-15 (diagnostic-only), D1–D5, L9, L18, ≥2 unseen scoring seeds, candidate-blindness (Ruling 9 — seeds from parameter-combo hashes only; no candidate output is an input), no-relabeling (ordinary per-seed statistical failures are predicate failures, NOT INSTRUMENT_FAILURE; apparatus-validity decision tree §5.6), **no bootstrap/Wilson/quorum/fallback** (only the Rebecca-authorized direct per-seed ρ), no scoring, no protected-seed access, no G2–G4 freeze, no merge to main, no L15/L16/L17 before M5, no extension of the geometry grid beyond the 20 in §3, no lowering/raising/renaming/reinterpreting a locked bar.

## Scoring NOT authorized

This authorizes the diagnostic screen only (O-15). Scoring remains gated on the five downstream gates (all required): (1) L3 fresh-seed resolution; (2) FWFP closure audit; (3) CRITIC implementation review; (4) Rebecca's tolerance-calibration sign-off (Ruling 9 — candidate-blind / oracle-grounded / frozen-before-scoring); (5) courier-channel authorization. No protected-seed exposure, no rerun.

## Input-resolution STOP condition

If the TASK BUILDER cannot resolve any authoritative input above by branch/SHA/path, **STOP and return to the coordinator** — do not invent or substitute. Every input listed is resolvable on GitHub (branch `architect/l8-g2g4-minimal-fullscreen` @ `2082680` for the spec/handoff/ruling; `critic/l8-g2g4-minimal-fullscreen-amended-review` @ `20733d0` for the CRITIC review; `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` and `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` for the rulings — see PR below).

## RECORDER (later, not a gate)

RECORDER must later record the signed geometry ruling and this TASK BUILDER authorization in `docs/rulings/provenance_log.md` (provenance entry) — but that is a post-implementation housekeeping step, not a gate before TASK BUILDER begins.

## Boundary-escalation

Per spec §5.4 + the operative geometry ruling: if no geometry passes (`meets_target` false for all 20), OR the first passing geometry lies on a tested boundary (`W ∈ {50,400}` or `N_w ∈ {4,64}`), STOP and escalate to ARCHITECT/Rebecca — do not auto-accept a boundary solution; do not extend the grid.

## Output expectations

Return handoff: (1) the JSON artifact `diagnostics/l8_g2g4_minimal_full_screen.json` (exact §7.1 schema; atomic write; NaN→null); (2) the run handoff `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md` (§7.2) including the output artifact's own SHA-256; (3) the 7 deterministic-test results (§5.5, including 2a no-softening); (4) the `minimum_geometry_satisfying_target` or explicit STOP/escalation; (5) branch + commit SHA.

## Next handoff

TASK BUILDER → INTEGRATOR (STATE reconciliation) → CRITIC (implementation review) → RECORDER (provenance) → Rebecca. Scoring remains behind the five downstream gates.

## Pre-push safety scan attestation

Coordinator routing artifact in the project file repo. Contains only public repo SHAs, branch names, file paths, and Rebecca's authorization relayed. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII. Scan result: **clean** — no blockers, no Rebecca-decision items, acceptable.
