# ARCHITECT → Fresh-Context CRITIC Handoff — L8 G2–G4 v2.6

> **SUPERSEDED:** Rebecca authorized the 1,000-repetition feasibility workload at `d08cb7e`; use the v2.7 closure handoff. This handoff authorizes nothing.

**Date:** 2026-08-20 · **Regime:** B (constitution v2 §5 binding)

**Gate served:** Staged Commit A implementation and parallel feasibility-benchmark design

**Input SHA:** `081df58131d880e2a1180ef508c35467415f07e4`

**Branch:** `architect/l8-g2g4-remediation`

## Files changed or created

- `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` — v2.6 §8.11 and sequencing amendment
- `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md` — v2.6 entry
- `handoffs/ARCHITECT_L8_G2G4_V2_5_1_CRITIC_REVIEW_HANDOFF.md` — superseded
- `handoffs/ARCHITECT_L8_G2G4_V2_6_CRITIC_HANDOFF.md` — this handoff

## Review charge

Perform §5 P1–P6 checks first. Then verify closure of all nine TASK BUILDER gaps:

- A1 implementation / A2 frozen-config / evidence identity lifecycle;
- exact benchmark JSON and sidecar schemas/publication;
- exact extrapolation formulas;
- multiprocessing CPU and aggregate-RSS definitions;
- scoring-parity worker/start/chunk policy;
- benchmark/bootstrap/calibration RNG identities;
- six uncached calibration behavior and timing separation; and
- unchanged benchmark-only authorization boundary.

The user explicitly rejected serial operation. Confirm v2.6 requires no serial benchmark and replaces serial-versus-parallel validation with two identical executions through the frozen parallel scoring path.

## Status

ARCHITECT verdict: **READY FOR FRESH-CONTEXT CRITIC REVIEW; NOT READY FOR TASK BUILDER.** All v2.6 mechanics are `[PROPOSED]`.

## Blockers

- CRITIC review and Rebecca approval precede A1/A2 implementation or any diagnostic execution.
- The 2,000-repetition screen remains withdrawn pending benchmark evidence and a separate Rebecca ruling.
- Confirmation, sensitivity, misspecification, scoring, and protected-seed work remain prohibited.

## Exact next recipient

Fresh-context **CRITIC**, then **Rebecca**. If approved, TASK BUILDER may build A1/A2 and run only the parallel repeatability/rehearsal and fixed six-case feasibility benchmark.

## Explicitly prohibited actions

- No implementation, calibration, repeatability, benchmark, or screening before Rebecca approval.
- No serial benchmark.
- No 2,000 screen, 10,000 confirmation, sensitivity/misspecification run, scoring, protected seeds, G2–G4 freeze/ruling, or merge.

## Public-safety scan attestation

Public-safety scan: gitleaks plus regex/manual review over the complete v2.6 diff from `081df58131d880e2a1180ef508c35467415f07e4`; zero prohibited findings; cleared. No credentials, contact details, machine identifiers, private absolute paths, environment dumps, or protected-seed identities were added.
