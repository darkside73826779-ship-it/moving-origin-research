# WORKFLOW COORDINATOR → ARCHITECT Handoff — L8 Full-Screen Spec Remediation (CRITIC BLOCK)

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** ARCHITECT remediation of the L8 G2–G4 minimal full-screen spec after a fresh-context CRITIC BLOCK.
**Next recipient:** ARCHITECT (originating role). On completion, re-route to fresh-context CRITIC → Rebecca → TASK BUILDER.

## Authority and scope

The fresh-context CRITIC reviewed the ARCHITECT's minimal L8 full-screen spec (`architect/l8-g2g4-minimal-fullscreen` @ `8f3e109`) and returned **BLOCK → ARCHITECT only**. This handoff is prepared for Rebecca to transport to ARCHITECT. The ARCHITECT corrects the two blocking findings (B1, B2) and addresses four non-blocking findings (NB1–NB4), then re-routes to a fresh-context CRITIC.

Authority chain: Rebecca > constitution laws > approved specifications > this handoff > agent judgment. The ARCHITECT specifies, not produces. **Do not change the PRIMARY designation (E1)** — the CRITIC verified it is textually grounded and consistent with frozen v2.2 line 44; the ARCHITECT did not need to STOP and must not re-designate or STOP now.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub main (base) | `f4e2231` |
| ARCHITECT branch (continue here) | `architect/l8-g2g4-minimal-fullscreen` @ `8f3e109` (commits `66808c5` + `8f3e109`) |
| ARCHITECT spec files | `specs/l8_g2g4_minimal_full_screen_spec.md`; `_CHANGELOG.md`; `_TASKBUILDER_HANDOFF.md`; `_EXECUTABILITY_TRACE.md` |
| CRITIC review (binding artifact) | `reviews/critic_l8_g2g4_minimal_fullscreen.md` at `02a7443` on `critic/l8-g2g4-minimal-fullscreen` |
| Frozen L8 v2.2 (cited) | `c7d7bed`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (line 44 = per-seed locked bar; §8 items 3–6 = 240-cell grid; **no** §8.2/§8.3 subsections, **no** 20-geometry list) |
| v2.4 geometry-list source | `4463cbc` on `architect/l8-g2g4-remediation` (§8.2 = the 20-geometry `W×N_w` list; §8.3 grids) |
| Verified code baseline | `b139749` (`false_kill_rate_per_seed` = `P(any seed β*_s < 0.2)`, β*-predicate only; code line 808) |
| Reference artifact | `6d455bb` (SHA-256 `978f21c0…`) |
| Rebecca feasibility ruling | `d08cb7e` |

## CRITIC verdict: BLOCK → ARCHITECT only

No downstream role starts early; Rebecca does not gate on a blocked artifact. The BLOCK is **not** because `PRIMARY = false_kill_rate_per_seed` is wrong — that designation is textually grounded (E1). The BLOCK is for B1 (false provenance in the TASK BUILDER handoff) and B2 (overstatement in the main spec §5.2/§5.3).

## Blocking findings (as found by the CRITIC) — fix both

### B1 — PROVENANCE / INTERNAL-CONSISTENCY (TASK BUILDER handoff, required file #3 of 4)

The TASK BUILDER handoff "Authoritative inputs" states the §8.2 geometry list and §8.3 grids are in frozen v2.2 (`c7d7bed`). The CRITIC verifies this is false: v2.2 §8 is a flat numbered list (items 1–9) with **no** `§8.2`/`§8.3` subsections and **no** 20-geometry `W×N_w` sweep — those were added in v2.4 (`4463cbc`). The main spec §0 has the provenance right; the TASK BUILDER handoff contradicts it on the same point.

**Remediation (for ARCHITECT):** Correct `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` "Authoritative inputs" so the §8.2 geometry-list and §8.3 grid source is cited as v2.4 `4463cbc` on `architect/l8-g2g4-remediation` (matching spec §0), with frozen v2.2 `c7d7bed` cited only for the §2 XF-5 estimator, the per-seed locked bar (line 44), and the 240-cell nuisance/operating grid (§8 items 3–6). Reconcile all four files to a single provenance statement.

### B2 — ACCURACY / MISCHARACTERIZATION (main spec §5.2–§5.3)

Spec §5.2 states `false_kill_rate_per_seed` is "the direct false-kill rate corresponding to the actual scoring verdict," and §5.3 frames it as "the scoring-verdict-aligned (primary) estimate." The CRITIC verifies against `b139749` (code line 808: `np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1))`) that `false_kill_rate_per_seed` = `P(any seed β*_s < 0.2)` — the **β*-predicate portion only**. It does **not** count runs killed by the `ρ < 0.8` predicate. It is a **lower bound** on the full scoring-verdict false-kill rate, not the full rate.

**Remediation (for ARCHITECT):** Qualify §5.2/§5.3 to state that `false_kill_rate_per_seed` is the **β*-predicate direct false-kill rate** (per `b139749`), capturing only the standardized-slope < 0.2 predicate of the per-seed scoring verdict; the full scoring verdict also requires `ρ ≥ 0.8` per seed (and, in v2.4 §8.1, direction + pooled-bootstrap interval), which this minimal spec deliberately does not compute. State explicitly that this is a lower bound on the complete-verdict false-kill rate.

## Non-blocking findings (as found by the CRITIC) — address

- **NB1 (spec §5.2):** the ARCHITECT cited v2.2 line 44 as justification; v2.4 §8.1 (`4463cbc`) is the explicit any-seed-primary / 5-seed-mean-diagnostic resolution. Recommend citing v2.4 §8.1 as corroborating context, noting §8.1's complete verdict includes a pooled-bootstrap predicate (`[BAR-Entry 11.3]`) this minimal spec deliberately omits in favor of `b139749`'s β*-only direct calculation. v2.2 line 44 remains the primary frozen authority; v2.4 §8.1 corroborating only.
- **NB2 (spec §5.1, §5.4):** make explicit that the primary metric is `[PROPOSED]` (flagged to Rebecca in `b139749`, NF-IMPL-2) and that geometry acceptance (`meets_target` / minimum acceptable battery) is a `[PROPOSED]`-gated diagnostic selection requiring Rebecca sign-off before binding/downstream use. Recommend the TASK BUILDER record the output artifact's own SHA-256 in the run handoff.
- **NB3 (spec §1.3):** correct the "closes the two `d08cb7e` details" framing — `d08cb7e`'s open details concerned the 1,000-repetition feasibility diagnostic (a different workload); the screening-run parameters come from the later WORKFLOW COORDINATOR handoff, not from closing `d08cb7e`'s feasibility-diagnostic details.
- **NB4 (spec §5):** the inherited `[Sol-XF-5]` closure-labels are not one of the four P3 source-class tags (`[LAW-Lx]`/`[BAR-Entry n]`/`[OP-Entry n]`/`[PROPOSED]`). Either re-tag as `[OP-Entry n]` (adopted operationalization) or confirm `[Sol-XF-*]` is an adopted `[OP]`-class closure label.

## What NOT to change (CRITIC-verified, E1–E6)

- **E1:** `PRIMARY = false_kill_rate_per_seed` (any-seed) is textually grounded and consistent with frozen v2.2 line 44; the ARCHITECT did not need to STOP. Do not re-designate or STOP.
- **E2:** P2 law-diff PASSES (L8 + §5 P1–P6 verbatim). Do not alter verbatim quotes.
- **E3:** the 19.2M two-arm accounting and ~90.5 min (1.5–2 h) timing are CORRECT (verified against `b139749` + `6d455bb`: reference 4.8M arm-sims in 22.63 min; 19.2M / 4.8M = 4×). Do not revert to 9.6M.
- **E4:** geometry-list provenance is CORRECT in main spec §0 (`4463cbc`, v2.4). Reusing the geometry grid does not invoke prohibited Wilson/bootstrap machinery. Do not change §0.
- **E5:** no prohibited machinery recreated. PASS.
- **E6:** end-to-end executability PASSES (schema, seed derivation, paths, cell ordering all fixed). Do not add fixtures/artifacts.

## Authorized scope

Correct B1 and B2; address NB1–NB4. Do **not** change the PRIMARY designation, the verbatim law quotes, the two-arm/timing, or the geometry-list provenance in §0. Preserve schema structure, paths, field order, and metric identity unless a minimal label/note clarification is required to fix B2. Commit to an `architect/` branch (continue `architect/l8-g2g4-minimal-fullscreen` or a new branch). Re-route to fresh-context CRITIC.

## Constraints

O-14 (no re-run; seeds 201–203/301–303 never rerun), O-15 (diagnostic-only), D1–D5, L9, L18, ≥2 unseen scoring seeds, no scoring, no protected-seed access, no G2–G4 freeze, no merge to main, no L15/L16/L17 before M5, no implementation, no lowering/raising/renaming/reinterpreting a locked bar, no reclassification of statistical failures as INSTRUMENT_FAILURE.

## Output expectations

Return handoff: (1) corrected spec + TASK BUILDER handoff (B1, B2 fixed); (2) NB1–NB4 addressed; (3) confirmation the PRIMARY designation and the E1–E6 verified items are unchanged; (4) branch + commit SHA.

## Next handoff

ARCHITECT → fresh-context CRITIC → Rebecca → TASK BUILDER.

## Pre-push safety scan attestation

Coordinator routing artifact in the project file repo. Contains only public repo SHAs, branch names, file paths, and CRITIC findings relayed from the in-repo review. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII. Scan result: **clean** — no blockers, no Rebecca-decision items, acceptable.
