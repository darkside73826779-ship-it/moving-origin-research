# CRITIC rereview — M4 crash-cart beta BF1-R2/BF2-R2/BF3-R2 and WF1

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

## Immutable intake

- Package ref/head: `taskbuilder/m4-final-prescoring-crash-cart-beta-implementation` at `cc55da04c0689c30b6d52c2aefcd1986f1c03da2`.
- Substantive result: `ba5ddda7811c776dc70347d3ae549b4c822c31be`.
- Routing result: `cc55da04c0689c30b6d52c2aefcd1986f1c03da2`.
- Canonical manifest: `handoffs/manifests/m4_final_prescoring_crash_cart_beta_implementation/20260822T160000Z_task_builder_to_workflow_coordinator.json`.
- Prior authoritative BLOCK: `critic/m4-final-prescoring-crash-cart-beta-bf1-bf3-final-rereview` at `e84ebc2611f2337058a630b077241aff38b836da`.
- BF4 and unchanged evidence: banked.

Remote identity, ancestry, and helper-compatible checkout reproduce. The standard `workflow_checkout.py create` accepts substantive result `ba5ddda7811c776dc70347d3ae549b4c822c31be` with a handoffs-only tail, closing WF1. The common handoff validator returns `VERIFIED`; all 28 listed artifact hashes, sidecars, LF constraints, and the exact changed-path inventory reproduce.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

WF1 is CLEAR. The original invalid-backend-code, full top-level schema counterexample, schedule-wait, queue-bound, deadline-constant, and fabricated-telemetry mutants are killed. Three directly affected boundary conditions remain unbound or fail-open; the cleared contract is not ambiguous.

## Batched executable findings

### BF1-R3 — clean-reset state, terminal deadline, and RNG-domain boundaries remain incorrect

**Production path and violated contract.** In `src/m4_final_prescoring_crash_cart.py`, `CrashCartLifecycle.warmup()` calls the post-warmup reset but does not replace internal `_states`; active ordinal 0 is therefore required to chain from the final warmup result, preserving exactly the state carryover the clean measured-episode reset must remove. `active()` checks the hard deadline before each pair but not after the pair returns, so the final pair can cross 60 seconds and still succeed. `warmup_plan()` binds RNG domain `PUBLIC_WARMUP_V1`, not the banked exact `M4_FINAL_CRASH_CART_WARMUP_V1`.

**Minimal reproducers.** (1) Use role callbacks whose state is reset to the initial digest when the injected reset callback is invoked. Warmup succeeds, the correct fresh active-episode receipt for ordinal 0 uses that reset digest, and `run()` incorrectly stops with `RECEIPT_PRIOR_STATE_INVALID`; rollback and cleanup occur. (2) Use an injected clock/sleeper and advance the clock to `61000000000` ns inside both role callbacks for active ordinal 63. The run is accepted with 64 active ordinals instead of timing out. (3) Read `warmup_plan()[0]["rng_domain"]`; it returns the wrong domain identity.

**Expected terminal behavior and evidence.** A successful clean reset must bind the post-reset state digest for each role, active ordinal 0 must chain from those fresh digests, and no warmup state may carry forward. Any pair completion after the hard deadline must produce `ACTIVE_WINDOW_TIMEOUT_NO_RETRY`, paired rollback/reset, exactly-once finally cleanup, and only observed partial-active evidence. Warmup requests must carry the exact banked RNG-domain identity.

**Smallest correction.** Make the injected reset return or otherwise expose each role's exact post-reset state digest and assign `_states` from it after both warmup and measured resets. Check the injected clock again immediately after every `_pair` and before terminal success. Replace the RNG-domain constant with `M4_FINAL_CRASH_CART_WARMUP_V1`.

**Required committed regression/mutation closure.** Add tests for a reset callback that genuinely resets role state and verify active ordinal 0 uses the fresh chain; a final-ordinal callback that advances the fake clock beyond 60 seconds and must fail closed; and exact RNG-domain equality. Kill mutants that retain warmup `_states`, omit the post-pair deadline check, and substitute any RNG-domain string.

### BF2-R3 — the in-repository Draft 2020-12 validator omits `minProperties`

**Production path and violated contract.** `_draft_validate()` implements the schema keywords used by the committed report schema except object `minProperties`. The schema binds `identities` as an object with `minProperties: 1`, but the validator accepts an empty object.

**Minimal counterexample.** Construct an otherwise schema-valid `PRE_ACTIVE_TERMINAL`/`PRE_START` report with exact authority, invocation, failure, HELD laws, NOT_RUN replica/cleanup/public-safety/export projections, empty rows/samples, and `identities={}`. `validate_terminal()` accepts it.

**Expected terminal behavior and evidence.** The report must stop with `REPORT_SCHEMA_INVALID` before stage semantics or export. No accepted report may omit every bound identity.

**Smallest correction.** In the object branch of `_draft_validate`, enforce `len(value) >= schema.get("minProperties", 0)`. Retain the current required, additional-properties, and max-properties checks.

**Required committed regression/mutation closure.** Commit the exact PRE_ACTIVE counterexample and a deterministic mutation that removes or bypasses `minProperties`; both the focused target and mutation runner must reject/kill it with `REPORT_SCHEMA_INVALID`.

### BF3-R3 — the focused and mutation evidence does not cover the remaining boundaries

**Exact discrepancy.** The focused target returns 15/15, the exact prior-source probe is killed, and all six named mutants are killed, yet the three BF1/BF2 reproducers above still fail or are accepted. The current deadline mutant changes the global deadline to 1 ns and exercises a pre-dispatch check; it does not cover a final pair crossing the deadline. No test models a reset callback that changes backend state, asserts the exact banked RNG domain, or mutates `minProperties`.

**Smallest evidence correction.** Add only the three production-path tests and four mutations specified above. Preserve the existing 15 tests, prior-source probe, and six killed mutants; do not broaden the suite.

**Required terminal evidence.** The same committed focused suite must pass on the corrected source, fail on `ba5ddda7811c776dc70347d3ae549b4c822c31be`, and report all ten boundary mutants killed with zero survivor or instrument failure.

## Cleared delta and immutable preservation set

- WF1 helper create/cleanup passes with a handoffs-only routing tail.
- Repository-root focused target: 15/15 PASS. Exact reviewed pre-correction probe: KILLED. Six deterministic boundary mutants: KILLED. Wrapper: exit 2 `RUN_AUTHORITY_ABSENT`.
- The prior invalid-backend-code receipt fails before active work with rollback/reset/cleanup; the full top-level COMPLETE counterexample is schema-rejected; observed dispatch/sample evidence replaces the prior planned tuples.
- The ordered 64-prompt digest inventory, BF4 `.gitattributes` closure, HELD projection, production seam, and all banked identities remain byte-identical.
- Correction-range preflight reports 26 fixed-regex matches and zero gitleaks findings. Manual review maps every match to public Git/SHA-256 identity or fixed timing/count controls; no prohibited content is present.
- `git diff --check` is clean.

The next correction must preserve byte-identical: the cleared design/schema/launch/gate artifacts and sidecars; beta/Rebecca/Coordinator authorities; BF4 and WF1 closure; the 64-prompt inventory and sidecar; literal-LF warmup bytes/digests; HELD-law projection; fail-closed wrapper; production integration seam; public model/runtime identities; the 15-test/prior-probe/six-mutant evidence; and all no-run/no-custody/no-scoring/no-science holds.

No model/tokenizer/OCI/WSL2/gofast workload, protected input, held access, custody, scoring, science, state/provenance mutation, merge, publication, readiness declaration, retry, or gate action occurred.

## Disposition

Return **COMBINED BLOCK** to **WORKFLOW COORDINATOR**. Exact next recipient: **TASK BUILDER** for one final BF1-R3/BF2-R3/BF3-R3 test-first correction. WF1 remains banked CLEAR; no design cycle is required.
