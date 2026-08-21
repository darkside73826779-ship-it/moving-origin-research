# L8 GPU Diagnostic-Backend Adoption Specification — Changelog

**Date:** 2026-08-20

**Regime:** B

## v1.0 — initial pre-registration

- Limited adoption to candidate-blind O-15 diagnostics; CPU remains the reference and scoring is excluded.
- Added a committed, source-attested CPU calibration table and required exact frozen-calibration use.
- Defined separate CPU/GPU RNG namespaces, logical-seed identities, scheduling-independent result positions, and maximum-capacity parallel execution.
- Fixed the complete-verdict, legacy mean, any-seed, and null estimands without substituting one for another.
- Fixed the complete 240-cell workload and equal CPU/GPU sample sizes.
- Pre-registered cell-level Bonferroni equivalence intervals, aggregate intervals, map distances, and numeric margins.
- Made exact coordinate selection a diagnostic and added a pre-registered equivalence-set report for near ties.
- Retained native-calibration divergence and misspecification selection disagreements as negative findings; native GPU calibration is not adopted.
- Restricted `INSTRUMENT_FAILURE` to independent apparatus checks and added twelve failure/repeatability rehearsals.
- Defined two-commit implementation/evidence identity and transactional JSON/sidecar publication.
- Added the mandatory fresh-context law-fidelity → CRITIC → Rebecca → TASK BUILDER route.

All new criteria are `[PROPOSED]`. No locked bar was changed.
