# WORKFLOW COORDINATOR → CRITIC Handoff — L8 G2–G4 Minimal Full-Screen Spec Review

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** Fresh-context CRITIC review of the ARCHITECT's minimal L8 G2–G4 full-screen specification — internal consistency, end-to-end executability, and law-fidelity (P1–P6).
**Next recipient:** On CLEAR → **Rebecca** (she gates before TASK BUILDER). On BLOCK → **ARCHITECT only** (originating role).

## Authority and scope

Rebecca transported the WORKFLOW COORDINATOR → ARCHITECT handoff (`0c11a8b`, 2026-08-20 11:22 EDT). The ARCHITECT is complete. This handoff routes the ARCHITECT's output to a fresh-context CRITIC under the updated CRITIC initialization script (binding commit-and-push obligation; reviews must be in-repo on a `critic/` branch, not attachments — PR #92 `edf7a78`).

Authority chain: Rebecca > constitution laws > approved specifications > this handoff > agent judgment. **The CRITIC does not choose scientific rules.** It verifies fidelity, consistency, and executability, and determines CLEAR/BLOCK on the whole artifact. If a controlling document the ARCHITECT treated as resolved is in fact ambiguous, BLOCK and route back to ARCHITECT.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub main (base) | `f4e2231` |
| ARCHITECT branch + HEAD | `architect/l8-g2g4-minimal-fullscreen` @ `8f3e109` |
| ARCHITECT commits | `66808c5` (spec) + `8f3e109` (amendment: geometry-list provenance, verbatim §5 P1–P6, two-arm workload flag, changelog fix) |
| Spec | `specs/l8_g2g4_minimal_full_screen_spec.md` (20,813 bytes) |
| Changelog | `specs/l8_g2g4_minimal_full_screen_CHANGELOG.md` (4,788 bytes) |
| TASK BUILDER handoff | `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` (4,471 bytes) |
| Executability trace | `specs/l8_g2g4_minimal_full_screen_EXECUTABILITY_TRACE.md` (5,178 bytes) |
| Frozen L8 v2.2 spec (cited by ARCHITECT) | `c7d7bed` on `architect/l8-instantiation-v2.2-fresh`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (line 44 = the "per seed" locked bar) |
| Verified code baseline | `b139749` |
| Reference artifact | `6d455bb` (SHA-256 `978f21c0…`) |

**The CRITIC must inspect all four ARCHITECT files** (spec, changelog, TASK BUILDER handoff, executability trace), not only the main spec.

## What the ARCHITECT delivered (as asserted by the ARCHITECT — not coordinator-verified)

- A minimal spec for one full screen: 20 geometries × 240 cells × 2,000 sims, using the existing direct false-kill calculation at `b139749`. Candidate-blind, synthetic/oracle-only, O-15 diagnostic-only.
- The ARCHITECT designates **PRIMARY = `false_kill_rate_per_seed`** (per-seed / any-seed), **DIAGNOSTIC = `false_kill_rate`** (5-seed mean), citing frozen L8 v2.2 line 44 ("per seed") verbatim. The ARCHITECT did **not** STOP — it asserts the controlling docs resolve the scoring-verdict rule to per-seed.
- The ARCHITECT flags two-arm workload accounting: 9.6M combo + 9.6M null = **19.2M actual** arm-simulations (the coordinator→ARCHITECT handoff stated 9.6M, combo-arm only).
- The ARCHITECT flags that the only located repo source of the pre-registered 20-geometry list is v2.4 §8.2 at `4463cbc`, which also contains prohibited Wilson/bootstrap machinery.

The coordinator takes no position on whether these assertions are correct. They are review targets.

## Review focus (items the ARCHITECT itself flagged, plus executability)

1. **Scoring-verdict-rule designation (spec §5.2–§5.3).** The coordinator→ARCHITECT handoff (`0c11a8b`) instructed: "Designate the direct false-kill rate corresponding to the actual scoring verdict as primary; if the controlling documents do not resolve the scoring-verdict rule unambiguously, STOP and identify the exact conflicting text — do not choose a rule." The ARCHITECT designated rather than STOPping. **CRITIC must determine whether frozen L8 v2.2 line 44 actually resolves the scoring verdict to per-seed any-seed-kills (→ consistent with the ARCHITECT's designation) or is ambiguous (→ the ARCHITECT should have STOPped; BLOCK).** This is consequential: it flips which false-kill rate (6.22% 5-seed-mean vs 76.23% any-seed at the reference point) is primary. CLEAR/BLOCK depends on the whole artifact, not this issue alone.
2. **Two-arm workload accounting and timing (spec §2).** Verify whether the spec's 19.2M two-arm accounting is consistent with the coordinator handoff's 9.6M count, the reference artifact's runtime basis at `6d455bb`, and the TASK BUILDER's execution budget. The ARCHITECT asserts the 4× linear estimate (~90.5 min, 1.5–2 h) holds because the reference also ran two arms — verify this against the reference artifact's actual `n_sims` semantics before accepting the runtime estimate. If Rebecca intended a single 2,000-per-cell budget shared across arms, the false-pass rate handling must change.
3. **Pre-registered 20-geometry list provenance (spec §0, §3).** The geometry list is being reused from v2.4 §8.2 at `4463cbc` while the surrounding v2.4 Wilson/bootstrap §8.9 machinery is prohibited. Verify `4463cbc` §8.2 is the authoritative pre-registered geometry list and that reusing the geometry list does not invoke the prohibited machinery. This is a real boundary condition.
4. **Geometry seed sharing (spec §6.1).** The ARCHITECT asserts cells sharing `(α, v, C_min, η)` across geometries share `base_seed` (first RNG draws coincide before `W`/`N_w` divergence), and that this is acceptable for aggregated false-kill estimates. Verify whether this is acceptable for the screen's false-kill rate estimates, or whether it requires Rebecca confirmation. Do not assert acceptable/unacceptable.
5. **No-prohibited-machinery (spec §1.3, §9).** Verify the spec does not recreate v2.3–v2.7 benchmark/bootstrap/Wilson/A1-A2-B/rehearsal/fault-injection machinery. Confirm the TASK BUILDER handoff matches the spec and does not reintroduce prohibited machinery.
6. **`[PROPOSED]` tagging (P3).** Verify all `[PROPOSED]` values are tagged as such and are not treated as scoring gates or Rebecca approvals. No `[PROPOSED]` value may gate scoring unless Rebecca signs.
7. **End-to-end executability.** Verify the executability trace shows every value the TASK BUILDER must supply is explicit — no "as appropriate" / "the same fixture" hand-waving. If the TASK BUILDER would need to invent a rule, the spec is incomplete.
8. **Law-fidelity (P1–P6).** Verbatim law quotation (P2) for L8 and §5; source-class tags (P3) on all thresholds; regime dating (P4); provenance citations (P6) verified against actual entry text. Reject any proceeding on non-repo text.

## Authorized scope

Review only. No scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17 before M5, no implementation, no rerun. Commit the review in-repo on a `critic/` branch per the CRITIC init obligation.

## Output expectations

CLEAR or BLOCK with specific findings (spec §/line references). On BLOCK, route back to ARCHITECT (originating role) — no downstream role starts early.

## Next handoff

- **On CLEAR → Rebecca.** Rebecca gates before TASK BUILDER. The route is CRITIC → Rebecca → TASK BUILDER, **not** CRITIC → TASK BUILDER directly.
- **On BLOCK → ARCHITECT only.**

## Pre-push safety scan attestation

This handoff is a coordinator routing artifact in the project file repo. It contains only public repo SHAs, branch names, file paths, and byte sizes. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII. Scan result: **clean** — no blockers, no Rebecca-decision items, acceptable.
