# REBECCA L8 FEASIBILITY-WORKLOAD AUTHORIZATION

**Date:** 2026-08-20

**Regime:** B (post-Entry 81; constitution v2 §5 binding)

**Authority:** Rebecca

**Serves:** L8 G2–G4 diagnostic feasibility gate

**Repository basis:** L8 diagnostic specification v2.6 at `e2bd8242315cb3fee88fb2f8b98bdc77ccacf515`

## Authorization recorded

Rebecca authorized replacing the presently specified 60-repetition feasibility workload (six cases × 10 repetitions) with a **1,000-repetition feasibility diagnostic**. The diagnostic is intended to measure parallel service time and support straightforward extrapolation to the proposed full-screen workload. `[PROPOSED — diagnostic workload; Rebecca-authorized for feasibility measurement]`

Rebecca also directed that diagnostic computation use parallel processing rather than repeating a full serial run. The implementation must retain the v2.6 scoring-parity multiprocessing contract unless a subsequent approved amendment changes it: `multiprocessing.Pool`, spawn start method, chunksize one, and worker count `min(32, logical CPU count)`. `[PROPOSED — diagnostic scheduling; Rebecca-authorized]`

The authorizing instruction was:

> “if the idea is to run the test to determine if a certain number of runs is appropriate or not i will judge that by doing the 1000 run test and we can use simple math to estimate the full test”

Rebecca then explicitly stated:

> “im authorizing it please document my authorization push and merge my documented authorization”

## Required specification closure before execution

This ruling authorizes the 1,000-repetition parallel feasibility workload. It does not invent the two remaining execution details that were not stated in the authorization:

1. allocation of the 1,000 repetitions across the approved sentinel cells and geometries; and
2. whether each repetition uses the full 5,000-valid-bootstrap verdict or an explicitly reduced benchmark bootstrap budget.

The ARCHITECT must record those two details deterministically in a repository specification amendment, route it through the required review, and return an executable handoff to TASK BUILDER. This closure is implementation routing, not a second decision about whether a 1,000-repetition parallel feasibility diagnostic is authorized.

## Authorization boundary

This ruling authorizes only candidate-blind, synthetic, O-15-labeled feasibility computation after the two execution details above are frozen. It does not authorize:

- the 9.6-million-repetition screening run;
- screening evidence or a G2–G4 freeze;
- final scoring or protected-seed access;
- a 10,000-repetition confirmation;
- sensitivity or misspecification reruns;
- rerunning failed scoring evidence; or
- L15/L16/L17 work before M5.

O-14 remains absolute for scoring. Statistical failures must not be relabeled as INSTRUMENT FAILURE. Rebecca remains the sole authority for the later workload and gate decisions.

## Next recipient

WORKFLOW COORDINATOR → ARCHITECT for the two-item deterministic amendment → fresh-context CRITIC → TASK BUILDER.
