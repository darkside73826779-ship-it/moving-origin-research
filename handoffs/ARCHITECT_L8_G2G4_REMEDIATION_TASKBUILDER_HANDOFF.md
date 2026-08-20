# ARCHITECT → TASK BUILDER Handoff — L8 G2–G4 Remediation Diagnostics

> **SUPERSEDED / DO NOT IMPLEMENT:** TASK BUILDER's deterministic STOP against v2.3 is valid. This handoff is suspended by specification v2.4. Route v2.4 to fresh-context CRITIC, then Rebecca; TASK BUILDER proceeds only if Rebecca approves the proposed diagnostic method and compute scope. The destination branch and implementation-source rules are now in v2.4 §8.9.7.

**Date:** 2026-08-19 · **Regime:** B (post-Entry 81; constitution v2 §5 binding)

**Gate served:** Remediation design before any G2–G4 decision

**Branch:** `architect/l8-g2g4-remediation`

**Base:** `c7d7bed6b259fb5163fb610098ea12aed1d3d65e`

## Input SHAs reviewed

- L8 instantiation specification v2.2: `c7d7bed6b259fb5163fb610098ea12aed1d3d65e`
- Power-analysis code: `b1397498ca369067e956479e6c2bd6b0793c3e89`
- Power-analysis artifact: `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3` (artifact SHA-256 supplied in the coordinator handoff: `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`)
- Calibration-parallelism specification: `6979378e701804476a7d4c6d32c24dc0afc1df6b`
- Governing main snapshot: `2370fcdb3b58da75c93e6e7fbc689a665d0efcf8`
- Provenance verified against Entries 11, 12, 43, 76, and 81.

## Files changed or created

- `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` — amended to v2.3
- `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md` — v2.3 entry added
- `handoffs/ARCHITECT_L8_G2G4_REMEDIATION_TASKBUILDER_HANDOFF.md` — this handoff

## Verified verdict rule

The L8 trend verdict is **all five seeds independently satisfying the applicable trend predicates, plus the pooled bootstrap interval condition**. It is not a threshold on the five-seed mean. Entry 11.3 locks five seeds with all-seeds-direction and bootstrap-CI treatment `[BAR-Entry 11.3]`; the M4 specification and task specification make a non-monotonic result on any seed a KILL; L8 v2.2 applies Spearman `ρ ≥ 0.8` and standardized slope `β* ≥ 0.2` per seed `[BAR-Entry 11]`.

Implement one shared pure verdict function used by both the diagnostic power analysis and the future harness interface. For each simulated five-seed run it must evaluate per-seed `ρ`, per-seed `β*`, direction on all seeds, and the pooled bootstrap interval. The power-analysis primary false-kill event is failure of that complete verdict under a known-positive synthetic profile. Do not implement final scoring mode in this task.

## Aggregation correction

- Primary: false-kill rate of the complete five-seed verdict described above. `[PROPOSED]`
- Diagnostic: false-kill rate of the mean `β*` across five seeds. `[PROPOSED]`
- Existing artifact verification: for each `(α,v,C_min,η)` combination, `false_kill_rate` is the repetition fraction where mean five-seed `β* < 0.2`; `false_kill_rate_per_seed` is the repetition fraction where any of the five `β*_s < 0.2`. Each sensitivity cell averages 15 such combination-level rates. At `(C_min,η)=(0.5,0.2)`, these are 6.22% and 76.23%, respectively. The latter is closer to the governing verdict but incomplete because it omits Spearman and the pooled interval.

## Authorized TASK BUILDER work

Implement only the diagnostic remediation specified in v2.3 §8:

1. Complete-verdict primary estimand and separately named mean-aggregation diagnostic.
2. Candidate-blind battery sweep over `W ∈ {50,100,200,400}` and `N_w ∈ {4,8,16,32,64}` `[PROPOSED]`, preserving four dose levels and all locked bars.
3. Ordered minimum-battery selection by total queries per dose, then larger window count, then smaller queries per window; accept only when the upper endpoint of the primary Wilson 95% interval is below 0.10, with below 0.05 reported as preferred. `[PROPOSED]`
4. Predicate-specific failure accounting and both false-kill aggregations.
5. Failure-injection tests and one complete diagnostic rehearsal for incomplete output, malformed/truncated output, serial/parallel nondeterminism, configuration mismatch, and crash recovery.
6. Independent apparatus-validity checks and exclusive INSTRUMENT FAILURE routing. Ordinary per-seed statistical failures remain FAIL/KILL and cannot be relabeled.

Use 2,000 repetitions per combination for screening and 10,000 only for finalist battery geometries after the aggregation implementation is reviewed. `[PROPOSED]` This is not authorization to rerun the old full sensitivity or misspecification stress analysis.

## Required artifacts

Return code, tests, resolved configuration manifest/digest, candidate-blind seed derivation, battery-sweep table with Wilson intervals, predicate-specific rates, test report, and diagnostic-rehearsal report. Artifacts must clearly state O-15 diagnostic-only status and that they are not scoring evidence.

## Deferred work

Do not recompute the sensitivity map, misspecification maps, or `(C_min,η)` selection. Those run only after Rebecca freezes aggregation and battery geometry. The later design uses v2.3's operational classification and pre-registered equivalence set; it is outside this TASK BUILDER handoff.

## Verdict/status

ARCHITECT design: **READY FOR TASK BUILDER DIAGNOSTIC IMPLEMENTATION, SUBJECT TO FRESH-CONTEXT CRITIC REVIEW BEFORE REBECCA'S G2–G4 DECISION.** This is not a G2–G4 ruling or freeze.

## Blockers and non-blocking findings

- Blocker to G2–G4: no revised sweep artifact or fresh-context CRITIC ruling exists yet.
- Blocker to G4: aggregation and battery geometry are not frozen.
- Non-blocking: the old 50% “informative” boundary described statistical nondegeneracy but admitted false-kill rates up to 43.22%; v2.3 replaces it for operational selection.
- Non-blocking: more simulations narrow Monte Carlo uncertainty; they do not necessarily increase the point estimate.

## Exact next recipient

**TASK BUILDER** for the diagnostic implementation and sweep described above; then **fresh-context CRITIC**; then **Rebecca** before any G2–G4 decision.

## Explicitly prohibited actions

- No scoring, protected-seed exposure, or use of candidate outputs/seeds as calibration inputs.
- No G2–G4 freeze or ruling; no final L8 scoring implementation release.
- No rerun of the old full 10,000-simulation sensitivity/misspecification stress analysis.
- No sensitivity-map or `(C_min,η)` recomputation in this cycle.
- No reclassification of ordinary statistical failures as INSTRUMENT FAILURE.
- No rerun, rescore, or reframing of any failed scoring result (O-14; D1/D5).
- No L15/L16/L17 work before M5.
- No merge to main; Rebecca alone authorizes gates and merges.
- No change to locked L8 bars, protected scientific logic, combo seeds, or estimator except the explicitly specified aggregation/battery diagnostic amendments.

## Public-safety scan attestation

Public-safety scan: pre-push secret scanner plus regex/manual review, complete branch diff from `c7d7bed6b259` including the handoff, zero prohibited findings, cleared. The only identity in new content is Rebecca's public role name in governance context; no contact details, credentials, machine identifiers, private paths, environment dumps, or new protected-seed identities are present.
