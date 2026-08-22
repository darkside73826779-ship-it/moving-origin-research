# CRITIC rereview — M4 crash-cart beta R3 closure

Date: 2026-08-22 EDT

Regime: B

Role: authoritative persistent CRITIC

## Immutable intake

- Package ref/head: `taskbuilder/m4-final-prescoring-crash-cart-beta-implementation` at `dd619714d15a2cdebafc14c67e55907282047269`.
- Substantive result: `56fadc894eb228927ba904b5c0db3e5032385259`.
- Routing result: `dd619714d15a2cdebafc14c67e55907282047269`.
- Canonical manifest: `handoffs/manifests/m4_final_prescoring_crash_cart_beta_implementation/20260822T160000Z_task_builder_to_workflow_coordinator.json`.
- Prior authoritative BLOCK: `critic/m4-final-prescoring-crash-cart-beta-r2-rereview` at `37e4a2e4f38c00b47065402d2d89cfd1c17ac3ca`.
- LAW_FIDELITY, WF1, BF4, and unchanged evidence: banked.

Remote identities and ancestry reproduce. The standard immutable-checkout helper accepts the exact substantive result and handoffs-only routing tail. The common handoff validator returns `VERIFIED`; the 28-entry raw artifact inventory, sidecars, LF constraints, and changed-path identities reproduce. `git diff --check` is clean.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

BF2-R3 Draft 2020-12 composition and `minProperties`, the pre/post-pair 60-second deadline boundary, and the exact warmup RNG domain are CLEAR. BF1-R3 remains BLOCKED by one directly executable reset-chain defect; BF3-R3 remains BLOCKED only for the missing regression/mutation evidence at that same boundary. No design ambiguity or new design cycle is required.

## Batched executable finding

### BF1-R3/BF3-R3 — a wrong but syntactically valid reset prior state is accepted

**Production path and violated contract.** `src/m4_final_prescoring_crash_cart.py::_validate_reset_receipt()` checks that `prior_backend_state_sha256` has lowercase SHA-256 syntax but never compares it with the role's currently bound `_states[role]`. `_reset_pair()` therefore accepts a reset receipt whose prior state is unrelated to the state being reset and commits its result state. This violates the gate's valid prior/result state-chain requirement and the package's claim that exact reset receipts are validated before atomic rebinding. The existing `prior` adversary supplies only `not-a-digest`, so it does not exercise state-chain equality.

**Minimal counterexample.** Construct a fresh `CrashCartLifecycle`, whose role states are each `"0" * 64`. Return exact seven-field PASS reset receipts with the correct role sessions, `request_ordinal=None`, valid request/result digests, but `prior_backend_state_sha256="f" * 64`. Calling `_reset_pair("probe")` succeeds and changes `_states` to the supplied results; the focused probe printed `ACCEPTED_WRONG_VALID_PRIOR` and exited 0.

**Expected terminal behavior and evidence.** The receipt must be rejected as `RESET_PRIOR_STATE_INVALID` before any state commit or active request. In the public `run()` path, no active row may be produced; paired rollback/reset and exactly-once `finally` cleanup must remain observable. A same-digest reset remains valid when the receipt prior equals the currently bound state.

**Smallest permitted correction.** Pass each role's expected pre-reset `_states[role]` into reset-receipt validation and require exact equality in addition to digest syntax. Retain the existing two-receipt collection, validate-before-commit atomicity, role/session/status/correlation checks, rebound result assignment, rollback precedence, and cleanup behavior.

**Required committed regression and mutation closure.** Add one production-path test using a different valid 64-hex prior digest for candidate and peer reset receipts; require `RESET_PRIOR_STATE_INVALID`, zero active rows, unchanged pre-rollback state, paired rollback, and cleanup. Add one deterministic mutant that removes or bypasses prior-state equality and require it to be killed. The corrected focused suite must kill exact substantive source `56fadc894eb228927ba904b5c0db3e5032385259`; retain all existing 27 passing tests, the banked `ba5ddda` pre-correction kill, and all ten current killed mutants.

## Reproduced and banked closure

- Focused production-path suite: 27/27 PASS.
- Exact `ba5ddda7811c776dc70347d3ae549b4c822c31be` pre-correction probe: `PRECORRECTION_KILLED`.
- Ten named invariant mutants: 10/10 KILLED, zero survivor or instrument failure.
- Wrapper: `RUN_AUTHORITY_ABSENT`, Python exit 2; no runtime start.
- Draft 2020-12 valid representatives and staged negatives, `minProperties`, post-pair deadline checks, exact `M4_FINAL_CRASH_CART_WARMUP_V1`, reset-result rebinding, ordered 64-prompt inventory, BF4, WF1, HELD law projections, and all no-run/no-custody/no-scoring/no-science boundaries otherwise remain banked.
- Full correction-range preflight has zero gitleaks findings. Its fixed-regex matches are repetitions of declared public Git/SHA-256 identities and fixed public timing/count values; manual classification found no prohibited content.

No model/tokenizer/OCI/WSL2/gofast workload, protected input, held access, custody, scoring, science, merge, project publication, readiness declaration, retry, or gate action occurred.

## Disposition

Return **COMBINED BLOCK** to **WORKFLOW COORDINATOR**. Exact next recipient: **TASK BUILDER** for the single BF1-R3/BF3-R3 equality regression above. Preserve byte-identical all banked LAW_FIDELITY, WF1, BF4, schema/deadline/RNG closure, design and authority artifacts, 64-prompt inventory, production seam, and standing holds.
