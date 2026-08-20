# WORKFLOW COORDINATOR → ARCHITECT Handoff — L8 Full-Screen Spec Amendment (Rebecca Directive)

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** ARCHITECT amendment of the L8 G2–G4 minimal full-screen spec per Rebecca's directive on the two deferred gate items (Item 1 primary metric; Item 3 geometry authority + acceptance/tie/boundary/escalation rules).
**Next recipient:** Fresh-context CRITIC. Route: ARCHITECT → fresh-context CRITIC → Rebecca (signs geometry-list adoption) → TASK BUILDER.

## Authority and scope

Rebecca accepts the third-party advisor's recommendations in principle and directs this amendment. This handoff is prepared for Rebecca to transport to the ARCHITECT. **Authorized: specification remediation and review only.** NOT authorized: implementation, scoring, protected-seed exposure, merger, or any new bootstrap/Wilson/quorum/fallback machinery unless separately authorized through a specification amendment.

Authority chain: Rebecca > constitution laws > approved specifications > this handoff > agent judgment. The ARCHITECT specifies, not produces. If a directive item conflicts with a locked law or an unresolved scoring-verdict rule, STOP and report the exact conflict. Do not invent.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub main (base) | `f4e2231` |
| ARCHITECT branch (continue here) | `architect/l8-g2g4-minimal-fullscreen` @ `a7b38b3` (CRITIC-cleared re-review `ab0111c`) |
| Spec + 3 companion files | `specs/l8_g2g4_minimal_full_screen_spec.md`, `_CHANGELOG.md`, `_TASKBUILDER_HANDOFF.md`, `_EXECUTABILITY_TRACE.md` |
| CRITIC re-review (CLEAR) | `reviews/critic_l8_g2g4_minimal_fullscreen_rereview.md` @ `ab0111c` on `critic/l8-g2g4-minimal-fullscreen-rereview` |
| Third-party advisor package | `handoffs/THIRD_PARTY_ADVISORY_L8_FULLSCREEN_DEFERRED_ITEMS.md` @ `246bd84` |
| Frozen L8 v2.2 (locked bars, line 44) | `c7d7bed`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` ("per seed": ρ ≥ 0.8 AND standardized slope ≥ 0.2) |
| v2.4 geometry-list source | `4463cbc` on `architect/l8-g2g4-remediation` (§8.2 = the 20-geometry `W×N_w` list + ordering) |
| Verified code baseline | `b139749` (computes per-seed ρ and β*; current `false_kill_rate_per_seed` = β*-predicate only, line 808) |
| Reference artifact | `6d455bb` (SHA-256 `978f21c0…`) |

## Rebecca's directive — Item 1 (primary metric)

The current primary `false_kill_rate_per_seed` (β*-only any-seed rate, a lower bound on the complete scoring-verdict false-kill rate) is NOT sufficient for battery acceptance. Amend the screen's primary metric to the **complete frozen-v2.2 scoring predicate**:

> **PRIMARY = `P(∃ seed s: β*_s < 0.2 OR ρ_s < 0.8)`** — the complete frozen-v2.2 any-seed scoring-verdict false-kill rate (a run fails if any seed `s` has `β*_s < 0.2` OR `ρ_s < 0.8`; both bars per seed `[BAR-Entry 11]`; any-seed aggregation; the frozen v2.2 line-44 scoring verdict).

Retain as **DIAGNOSTICS only** (do not gate battery acceptance):
- β*-only any-seed false-kill (`false_kill_rate_per_seed`).
- Five-seed-mean false-kill (`false_kill_rate`).

**Computation constraint:** the complete predicate must be computed directly from the existing per-seed ρ and β* arrays in `b139749` (direct calculation). **Do NOT introduce a quorum, fallback, bootstrap, or Wilson procedure** unless separately authorized through a specification amendment. (The v2.4 §8.1 pooled-bootstrap predicate `[BAR-Entry 11.3]` is NOT part of this primary metric — Rebecca's directive uses the frozen-v2.2 bars only.)

### ARCHITECT must amend (Item 1)
- **§5.1:** add the complete-predicate primary rate; reclassify `false_kill_rate_per_seed` and `false_kill_rate` as diagnostics.
- **§5.2:** re-designate PRIMARY = complete any-seed scoring-verdict rate; DIAGNOSTIC = β*-only any-seed + 5-seed-mean. Remove the prior "lower bound" framing as the primary characterization (the primary is now the complete rate; the β*-only rate becomes a diagnostic that is a lower bound on the primary).
- **§5.3:** update the mismatch memorialization — the primary is the complete frozen-v2.2 predicate, not the β*-predicate lower bound. Rebecca's §5.3 review is of the complete-predicate primary.
- **§5.4:** geometry acceptance (`meets_target` / minimum acceptable battery) gates on the NEW primary (complete any-seed rate). `[PROPOSED]`-gated; Rebecca sign-off before binding (unchanged).
- **§7.1 schema:** use unambiguous field names that clearly distinguish (a) the complete any-seed primary false-kill rate, (b) the β*-only any-seed diagnostic, (c) the five-seed-mean diagnostic — do NOT reuse ambiguous `primary_false_kill_rate` wording without an explicit definition. TASK BUILDER records output artifact SHA-256 (unchanged, NB2).
- Confirm the complete predicate is computable from `b139749`'s per-seed ρ and β* without new machinery; if not, STOP and report.

## Rebecca's directive — Item 3 (geometry authority)

- Adopt **only** the 20-geometry grid and ordering from v2.4 commit `4463cbc` §8.2; **do not** adopt v2.4's prohibited Wilson/bootstrap machinery (§8.9.3–§8.9.4 and reporting-requirements remain prohibited).
- **Do not characterize the list as previously PI-approved or frozen.** A PI ruling prospectively freezes the geometry table before execution (the geometry-list adoption is a Rebecca signature gate before TASK BUILDER — see Next handoff). The amendment must reference this prospective PI ruling and must not claim prior freezing.
- **Acceptance applies to an exact `(W, N_w)` geometry**, not merely total query count `Q`.
- **Deterministic treatment of geometries tied on `Q`** — make the §3 tie-break ("then by larger `N_w`, then by smaller `W`") explicit and binding as the deterministic ordering.
- **Escalation rule:** if NO geometry passes (`meets_target` false for all 20), OR if the first passing geometry lies on a tested boundary (e.g., min/max `W` or `N_w`, or an edge of the `W×N_w` grid), STOP and escalate to ARCHITECT/Rebecca — do not auto-accept a boundary solution; return for a ruling.

### ARCHITECT must amend (Item 3)
- **Draft PI ruling deliverable:** prepare `handoffs/DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md` — a clearly labeled **DRAFT** that prospectively freezes the geometry table before execution, for Rebecca's signature. Mark it: **DRAFT — not operative unless/until Rebecca signs.** Do not commit it as an operative `REBECCA_...` ruling unless Rebecca provides/signs the final text. (No agent speaks for Rebecca; the ARCHITECT drafts/supports the ruling; Rebecca's signed adoption remains the gate before TASK BUILDER.)
- **§0:** retain `4463cbc` (v2.4) as the geometry-list source; reference the prospective PI ruling; do not claim prior PI approval/freezing.
- **§3:** affirm the exact-`(W,N_w)` acceptance basis and the deterministic `Q`-tie ordering.
- **§5.4:** add the boundary-escalation rule — if NO geometry passes (`meets_target` false for all 20), OR if the first passing geometry lies on a tested boundary → STOP and escalate to ARCHITECT/Rebecca. The ARCHITECT must define "tested boundary" exactly (not merely as an example — e.g., min/max `W` or `N_w`, or a grid edge of the `W×N_w` table); the CRITIC will verify that definition.
- **§1.3/§9:** confirm v2.4 prohibited machinery remains prohibited (geometry list only is reused).

## What NOT to change (CRITIC-verified, preserved)

- The PRIMARY designation direction (any-seed, per frozen v2.2 line 44) is unchanged in spirit — the amendment COMPLETES it (adds the ρ-predicate), it does not reverse it.
- Verbatim law quotes (P2, E2); two-arm 19.2M / 4× timing (E3); no prohibited machinery beyond the Item 1/3 changes (E5); end-to-end executability (E6) — re-verify executability after the primary-metric change (the complete predicate must be computable end-to-end).
- Locked bars (ρ ≥ 0.8, standardized slope ≥ 0.2, ≥ 3 doses, 5 seeds) — unchanged. No lowering/raising/renaming/reinterpreting a locked bar.

## Constraints

O-14 (no re-run; seeds 201–203/301–303 never rerun), O-15 (diagnostic-only), D1–D5, L9, L18, ≥2 unseen scoring seeds, candidate-blindness (Ruling 9), no-relabeling (no per-seed statistical failure reclassified as INSTRUMENT_FAILURE), no bootstrap/Wilson/quorum/fallback unless separately authorized, no scoring, no protected-seed access, no G2–G4 freeze, no merge to main, no L15/L16/L17 before M5, no implementation.

## Output expectations

Return handoff: (1) amended spec (§0, §3, §5.1–§5.4, §7.1, §1.3/§9, changelog) + updated executability trace + TASK BUILDER handoff reconciled; (2) confirmation the complete primary predicate is computable from `b139749` per-seed ρ and β* without new machinery; (3) the boundary-escalation and exact-`(W,N_w)`/deterministic-tie rules specified; (4) confirmation locked bars, verbatim quotes, two-arm/timing, and prohibited-machinery exclusions are preserved; (5) branch + commit SHA.

## Next handoff

ARCHITECT → fresh-context CRITIC → Rebecca → TASK BUILDER. **TASK BUILDER remains held** until BOTH: (a) fresh-context CRITIC clearance of the amended spec, AND (b) Rebecca signs the geometry-list adoption (the prospective PI ruling freezing the geometry table). This authorizes specification remediation and review only — not implementation, scoring, protected-seed exposure, or merger.

## Pre-push safety scan attestation

Coordinator routing artifact in the project file repo. Contains only public repo SHAs, branch names, file paths, and Rebecca's directive relayed verbatim. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII. Scan result: **clean** — no blockers, no Rebecca-decision items, acceptable.
