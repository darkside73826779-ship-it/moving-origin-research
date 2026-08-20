# ARCHITECT → Fresh-Context CRITIC Handoff — L8 G2–G4 v2.7

> **SUPERSEDED FOR PRE-EXECUTION ROUTING:** Rebecca directly cleared v2.7.1. TASK BUILDER now follows the v2.7.1 execution handoff; fresh-context CRITIC review occurs after the authorized diagnostic evidence is produced.

**Date:** 2026-08-20 · **Regime:** B (constitution v2 §5 binding)

**Gate served:** Final deterministic closure for the authorized L8 1,000-repetition parallel feasibility diagnostic

**Input SHAs:** design `e2bd8242315cb3fee88fb2f8b98bdc77ccacf515`; authorization `d08cb7eefec67609a3ea3cee0eb20da22f78c40a`; baseline `b1397498ca369067e956479e6c2bd6b0793c3e89`

**Branch:** `architect/l8-g2g4-remediation`

## Files changed or created

- `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` — v2.7 §8.12 and sequencing
- `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md` — v2.7 entry
- `handoffs/ARCHITECT_L8_G2G4_V2_6_CRITIC_HANDOFF.md` — superseded
- `handoffs/ARCHITECT_L8_G2G4_V2_7_CRITIC_HANDOFF.md` — this handoff

## Three-item review charge

Review only the authorized closure:

1. Repetition allocation totals 1,000 exactly and fixes case/order/counts as `[167,167,167,167,166,166]`.
2. Every feasibility repetition fixes 5,000 valid bootstrap replicates and 5,500 maximum attempts while preserving existing algorithms.
3. Parallel-repeatability geometry/cell/calibration/repetitions/bootstrap/RNG/schema/comparison, the committed known-good pair, and the two estimator descriptor digests are executable without TASK BUILDER choices.

Begin with §5 P1–P6. Verify the estimator descriptor strings and SHA-256 values byte-for-byte. Confirm maximum-capacity frozen parallel execution and that no serial benchmark is reintroduced.

## Status

ARCHITECT verdict: **READY FOR ONE FRESH-CONTEXT CRITIC REVIEW.** No implementation or execution has occurred.

## Exact next recipient

Fresh-context **CRITIC** → **Rebecca clearance** → **TASK BUILDER** A1/A2 implementation and authorized execution.

## Explicitly prohibited actions

- No implementation or execution before CRITIC review and Rebecca clearance.
- No screening, scoring, protected seeds, G2–G4 freeze, 10,000 confirmation, sensitivity/stress rerun, or merge authority.
- No serial benchmark.

## Public-safety scan attestation

Public-safety scan: gitleaks plus regex/manual review over the complete v2.7 diff from `e2bd8242315cb3fee88fb2f8b98bdc77ccacf515`; zero prohibited findings; cleared. No credentials, contact details, machine identifiers, private absolute paths, environment dumps, or protected-seed identities were added.
