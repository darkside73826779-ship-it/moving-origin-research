# REBECCA — L8 Geometry Table Freeze (Operative Ruling)

**Status:** **OPERATIVE** — signed by Rebecca, 2026-08-20.
**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Principal:** Rebecca R. McClintic (sole gate and merge authority)
**Recorded by:** WORKFLOW COORDINATOR at Rebecca's explicit direction ("Sign the geometry-table freeze ruling," 2026-08-20 20:02 EDT). The coordinator records this ruling at Rebecca's direction; **no agent speaks for Rebecca.** The signature below is Rebecca's, transcribed/recorded at her direction.

## Ruling

Rebecca **SIGNS** the L8 G2–G4 full-screen battery-geometry-table freeze ruling, making it **operative**. This prospectively freezes the 20-geometry `W × N_w` table and its deterministic ordering before execution, adopted **only** from v2.4 `4463cbc` §8.2 on `architect/l8-g2g4-remediation`:

- `W ∈ {50, 100, 200, 400}` `[PROPOSED — §8.2]`; `N_w ∈ {4, 8, 16, 32, 64}` `[PROPOSED — §8.2]`.
- Ordering: `Q = W × N_w` ascending, then larger `N_w`, then smaller `W` `[PROPOSED — §8.2]` (20-row authoritative table in `specs/l8_g2g4_minimal_full_screen_spec.md` §3).
- Acceptance applies to an exact `(W, N_w)` geometry (not merely `Q`); equal-`Q` geometries are distinguished and deterministically ordered, never merged or pooled.

## Scope of this freeze (binding)

This ruling freezes **only the geometry table for this diagnostic execution**. It does **NOT** freeze G2–G4 results, scoring, or final battery acceptance. It does **not** adopt v2.4's prohibited machinery (Wilson 95% interval; `predicate_false_kill_rates`/`failure_mask_counts`; finalist 10,000-rep confirmation; `resolved_config.json`; rehearsal fixtures; fault injection; sensitivity/misspecification recomputation; `(C_min, η)` selection; v2.4 §8.1 pooled-bootstrap predicate `[BAR-Entry 11.3]`) — those remain prohibited (spec §1.3/§9).

## Boundary-escalation rule (binding)

Per spec §5.4: if no geometry passes (`meets_target` false for all 20), OR the first geometry whose `meets_target` is true lies on a tested boundary (`W ∈ {50, 400}` or `N_w ∈ {4, 64}` — any edge of the `W × N_w` grid), STOP and escalate to ARCHITECT/Rebecca; do not auto-accept a boundary solution.

## Prior-freezing disclaimer

The table is **prospectively** adopted by this ruling. It was **not** previously PI-approved or frozen.

## References

- CRITIC-cleared DRAFT ruling (now signed/operative): `handoffs/DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md` @ `architect/l8-g2g4-minimal-fullscreen` `2082680`.
- CRITIC amendment review (CLEAR): `reviews/critic_l8_g2g4_minimal_fullscreen_amended_review.md` @ `20733d0` on `critic/l8-g2g4-minimal-fullscreen-amended-review`.
- Amended spec (CRITIC-cleared): `architect/l8-g2g4-minimal-fullscreen` @ `2082680`.
- ρ-authorization ruling (operative): `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md`.

## Signature

**Rebecca R. McClintic** (Principal; sole gate and merge authority) — **SIGNED 2026-08-20.**

*This ruling is operative upon Rebecca's signature. It satisfies the geometry-list-adoption gate (b). TASK BUILDER release additionally requires gate (c) — Rebecca's explicit TASK BUILDER authorization — recorded separately.*
