# WORKFLOW COORDINATOR → CRITIC Handoff — L8 Full-Screen Spec Re-Review (post-remediation)

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** Fresh-context CRITIC re-review of the ARCHITECT's remediation of the L8 G2–G4 minimal full-screen spec after CRITIC BLOCK (`02a7443`).
**Next recipient:** On CLEAR → **Rebecca** (gate before TASK BUILDER). On BLOCK → **ARCHITECT only**.

## Authority and scope

The ARCHITECT remediated the spec per the CRITIC's BLOCK (`02a7443`, branch `critic/l8-g2g4-minimal-fullscreen`) and re-routes to a fresh-context CRITIC for re-review. This handoff is prepared for Rebecca to transport to CRITIC. This is an independent adversarial re-review — verify against the actual diff, not the commit message (see false-attestation guard below).

Authority chain: Rebecca > constitution laws > approved specifications > this handoff > agent judgment. The CRITIC does not choose scientific rules; it verifies fidelity, consistency, and executability, and determines CLEAR/BLOCK on the whole remediated artifact.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub main (base) | `f4e2231` |
| ARCHITECT branch + HEAD (remediated) | `architect/l8-g2g4-minimal-fullscreen` @ `a7b38b3` |
| Remediation commits | `874097a` (B1 + B2 + NB1–NB4) + `a7b38b3` (B2 wording finalization + §7.1 note) — on top of `8f3e109` |
| ARCHITECT spec files (4) | `specs/l8_g2g4_minimal_full_screen_spec.md`, `_CHANGELOG.md`, `_TASKBUILDER_HANDOFF.md`, `_EXECUTABILITY_TRACE.md` |
| CRITIC original review (binding findings B1/B2/NB1–NB4) | `reviews/critic_l8_g2g4_minimal_fullscreen.md` @ `02a7443` on `critic/l8-g2g4-minimal-fullscreen` |
| Frozen L8 v2.2 (cited) | `c7d7bed`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (line 44 = per-seed locked bar; §8 items 3–6 = 240-cell grid; **no** §8.2/§8.3, **no** 20-geometry list) |
| v2.4 geometry-list source | `4463cbc` on `architect/l8-g2g4-remediation` (§8.2 = 20-geometry list; §8.3 grids) |
| Verified code baseline | `b139749` (`false_kill_rate_per_seed` = `P(any seed β*_s < 0.2)`, β*-predicate only; line 808) |
| Reference artifact | `6d455bb` (SHA-256 `978f21c0…`) |

**Inspect all four ARCHITECT files** at `a7b38b3`, and re-read every cited controlling document at its cited SHA. **Review the diff range `8f3e109..a7b38b3`; inspect commits `874097a` and `a7b38b3` individually.** The CRITIC's original review (`02a7443`) is the binding source of the findings to verify fixed. (File-change stats noted below are observed diffs in expected areas; the CRITIC must verify the fixes are substantive.)

## What the ARCHITECT asserts it remediated (verify each against the diff)

- **B1 (PROVENANCE):** `874097a` modified the TASK BUILDER handoff (+3/-3) to a reconciled provenance statement citing v2.4 `4463cbc` for §8.2/§8.3 and citing v2.2 `c7d7bed` only for §2 XF-5, line-44 bar, 240-cell grid. **Verify** the handoff no longer mis-cites v2.2 for the geometry list, that all four files carry a single reconciled provenance statement, and that the EXECUTABILITY_TRACE (+6/-6) and CHANGELOG (+13) are consistent with it.
- **B2 (ACCURACY):** `874097a` modified the spec §5.2/§5.3 (+16/-8) and `a7b38b3` removed lingering "false-kill rate corresponding to that verdict" wording (+2/-2) and updated §7.1 `scoring_verdict_alignment_note`. **Verify** §5.2/§5.3 now qualify `false_kill_rate_per_seed` as the **β*-predicate direct false-kill rate / lower bound** (captures only standardized-slope < 0.2; the full verdict also requires ρ ≥ 0.8 per seed), and that no residual overstatement remains.
- **NB1–NB4:** `874097a` asserts NB1 (cite v2.4 §8.1 corroborating), NB2 (mark primary/acceptance `[PROPOSED]` + Rebecca-gated, record artifact SHA-256), NB3 (correct `d08cb7e` framing), NB4 (re-tag `[Sol-XF-5]` → `[OP]`-class). **Verify** each is actually addressed in the diff.
- **E1–E6 unchanged:** the ARCHITECT asserts PRIMARY=`false_kill_rate_per_seed` (E1), verbatim law quotes (E2), two-arm 19.2M / 4× timing (E3), geometry-list provenance in §0 (E4), no prohibited machinery (E5), and executability/schema (E6) are unchanged — except minimal §7.1 label/note clarification required to fix B2. **Verify** the remediation did not alter E1–E5, nor schema structure, paths, field order, or metric identity; diff scope should be confined to the B1/B2/NB1–NB4 fixes.

## False-attestation guard (binding)

Verify every claimed fix against the actual file contents at `a7b38b3`, not the commit message. The prior L8 v2.2 ARCHITECT session produced a false attestation (changelog claimed all 9 items fixed; diff showed 1/9). The updated ARCHITECT init (PR #67 `8207a92`) added verification obligations; confirm they held here. If any claimed fix is absent or only superficially present in the diff, BLOCK.

## Authorized scope

Re-review only. No scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17 before M5, no implementation, no rerun. Commit the review in-repo on a `critic/` branch per the CRITIC init obligation (PR #92).

## Output expectations

CLEAR or BLOCK with specific findings (file + §/line). On CLEAR, confirm B1 and B2 are substantively fixed, NB1–NB4 addressed, and E1–E5 plus schema structure/paths/field order/metric identity unchanged. The re-review output must include its own pre-push scan attestation, branch name, commit SHA, and review file path. On BLOCK, route back to ARCHITECT.

## Next handoff

- **On CLEAR → Rebecca.** Rebecca gates before TASK BUILDER. Route: CRITIC → Rebecca → TASK BUILDER.
- **On BLOCK → ARCHITECT only.**

## Pre-push safety scan attestation

Coordinator routing artifact in the project file repo. Contains only public repo SHAs, branch names, file paths, and CRITIC findings relayed from in-repo reviews. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII. Scan result: **clean** — no blockers, no Rebecca-decision items, acceptable.
