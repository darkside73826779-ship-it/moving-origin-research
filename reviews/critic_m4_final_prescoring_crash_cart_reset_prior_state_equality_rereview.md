# CRITIC rereview — M4 reset prior-state equality closure

Date: 2026-08-22 EDT

Regime: B

Role: authoritative persistent CRITIC

## Immutable intake

- Package ref/head: `taskbuilder/m4-final-prescoring-crash-cart-beta-implementation` at `abc4e0098294b209b53a0c95e5b9645a745a4b80`.
- Substantive result: `f9d5541b327f65b730b2a73735b8be3fc4f0f8e0`.
- Routing result: `abc4e0098294b209b53a0c95e5b9645a745a4b80`.
- Canonical manifest: `handoffs/manifests/m4_final_prescoring_crash_cart_beta_implementation/20260822T160000Z_task_builder_to_workflow_coordinator.json`.
- Prior authoritative BLOCK: `critic/m4-final-prescoring-crash-cart-beta-r3-closure-rereview` at `8cc646d9880a1bdf5f6788460b9604f52b44abbc`.

The remote ref/head, ancestry from `dd619714d15a2cdebafc14c67e55907282047269`, substantive result, and helper-compatible handoffs-only routing tail reproduce. The common handoff validator returns `VERIFIED`. The manifest's 28 raw artifact identities reproduce, and the five changed implementation/test artifacts plus sidecars are byte-correct and LF-only. `git diff --check` is clean.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: CLEAR**
- **COMBINED VERDICT: CLEAR**

The single BF1-R3/BF3-R3 reset prior-state equality finding is closed. `_validate_reset_receipt()` now requires the syntactically valid prior digest to equal the role's currently bound `_states[role]`. `_reset_pair()` still collects both receipts, validates both against the pre-reset states, and commits neither result until the complete validation comprehension succeeds.

## Focused independent evidence

- `test_reset_valid_wrong_prior_is_atomic_rolls_back_and_cleans`: PASS, including candidate-first and peer-second valid-wrong-prior subcases, direct atomic-boundary checks, and public-run rollback/cleanup checks.
- Exact reviewed substantive `56fadc894eb228927ba904b5c0db3e5032385259`: `PRECORRECTION_KILLED` by that regression.
- Equality-bypass mutant only: `KILLED reset_prior_equality` with no survivor or instrument failure.
- Expected projection is `RESET_PRIOR_STATE_INVALID`; no active dispatch or measured-reset event is accepted, invalid receipt results are not committed, paired rollback occurs, and cleanup remains exactly once. The banked same-digest success boundary is unchanged.

Only `src/m4_final_prescoring_crash_cart.py`, the focused test and three runners, and their five sidecars changed substantively. The routing tail changes only the canonical manifest, quality trace, and formal handoff. All banked BF2-R3/schema, deadline, RNG-domain, LAW_FIDELITY, WF1, BF4, 64-prompt inventory, HELD-law, wrapper, production-seam, and public-identity bytes remain preserved; no unchanged broad suite was rerun.

Changed-range preflight reports zero gitleaks findings. Fixed-regex matches are confined to declared public Git/SHA-256 identities in the probe, handoff, quality trace, and manifest; manual classification found no prohibited content.

No model/tokenizer/OCI/WSL2/gofast workload, protected input, held access, custody, scoring, science, merge, project publication, readiness declaration, retry, or gate action occurred.

## Disposition

Return **COMBINED CLEAR** to **WORKFLOW COORDINATOR**. Exact next recipient: **WORKFLOW COORDINATOR** for integration sequencing under the standing scope freeze and all existing holds.
