# DRAFT — PI L8 Geometry Table Freeze (For Rebecca's Signature)

**Status:** **DRAFT — NOT OPERATIVE unless/until Rebecca signs.** No agent speaks for Rebecca; the ARCHITECT drafts/supports this ruling; Rebecca's signed adoption remains the gate before TASK BUILDER execution.
**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Prepared by:** ARCHITECT (for Rebecca R. McClintic's signature)
**Authorizing directive:** Rebecca directive (2026-08-20), Item 3: "Prepare the geometry-list adoption for Rebecca's signature before execution."

## What this freezes (prospective)

This ruling, when signed by Rebecca, **prospectively freezes** the L8 G2–G4 full-screen battery-geometry table before execution. The table is the 20-geometry `W × N_w` list and its deterministic ordering, adopted **only** from v2.4 `4463cbc` §8.2 (`architect/l8-g2g4-remediation`):

- `W ∈ {50, 100, 200, 400}` `[PROPOSED — §8.2]`
- `N_w ∈ {4, 8, 16, 32, 64}` `[PROPOSED — §8.2]`
- Ordering: `Q = W × N_w` ascending, then larger `N_w`, then smaller `W` `[PROPOSED — §8.2]` (the 20-row authoritative table is in `specs/l8_g2g4_minimal_full_screen_spec.md` §3).
- Acceptance applies to an exact `(W, N_w)` geometry (not merely `Q`); equal-`Q` geometries are distinguished and deterministically ordered, never merged or pooled. `[PROPOSED — §8.2, Rebecca directive]`

## What is NOT adopted (prohibited v2.4 machinery)

This adoption takes **only** the 20-geometry grid and ordering. It does **not** adopt v2.4's prohibited machinery: the Wilson 95% interval; `predicate_false_kill_rates` / `failure_mask_counts`; finalist 10,000-rep confirmation; `resolved_config.json` manifest; rehearsal fixtures; fault injection; sensitivity/misspecification recomputation; `(C_min, η)` selection; or the v2.4 §8.1 pooled-bootstrap predicate `[BAR-Entry 11.3]`. (See spec §1.3/§9.) These remain prohibited.

## Boundary-escalation rule (adopted by reference)

Per spec §5.4: if no geometry passes (`meets_target` false for all 20), OR the first geometry whose `meets_target` is true lies on a tested boundary (`W` = min(50) or max(400), or `N_w` = min(4) or max(64) — any edge of the `W × N_w` grid), STOP and escalate to ARCHITECT/Rebecca; do not auto-accept a boundary solution.

## Prior-freezing disclaimer

This table is **prospectively** adopted by this ruling. It was **not** previously PI-approved or frozen. Until Rebecca signs this ruling, the geometry list has no operative freeze status; TASK BUILDER does not execute the screen.

## Signature block

- **Rebecca R. McClintic** (Principal; sole gate and merge authority): ____________________  Date: ____________
- On signature, this ruling becomes operative, freezing the geometry table before execution, and the screen may proceed to fresh-context CRITIC → Rebecca → TASK BUILDER (TASK BUILDER released only after BOTH fresh-context CRITIC clearance AND this signature).

*Until signed, this document is a DRAFT and confers no authority.*
