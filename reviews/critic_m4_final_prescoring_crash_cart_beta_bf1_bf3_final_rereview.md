# CRITIC final rereview — M4 crash-cart beta BF1–BF3

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

## Immutable intake

- Package ref/head: `taskbuilder/m4-final-prescoring-crash-cart-beta-implementation` at `4a58a1529a9cc74bd3f3a7c3d7dbc638f1b5b706`.
- Test-first failing checkpoint: `e82cf06c78ecc0f9a1d87b9f0df3aa299a07a433`.
- Substantive implementation: `3f9f685a1f88c9f18f916688ce9a574f19e246e8`.
- Final routing/manifest head: `4a58a1529a9cc74bd3f3a7c3d7dbc638f1b5b706`.
- Canonical manifest: `handoffs/manifests/m4_final_prescoring_crash_cart_beta_implementation/20260822T160000Z_task_builder_to_workflow_coordinator.json`.
- Prior authoritative rereview BLOCK: `critic/m4-final-prescoring-crash-cart-beta-bf1-bf4-rereview` at `3b62d8fa21deb51dfd6f8ca50577a33bee5dfb49`.
- BF4: banked CLEAR.

Remote identity and ancestry reproduce. The common handoff manifest validator returns `VERIFIED`; all 26 listed artifact hashes, sidecars, LF constraints, and changed-path inventory reproduce. The standard immutable-checkout helper does **not** accept the package unchanged: using the manifest's declared review result `3f9f685a1f88c9f18f916688ce9a574f19e246e8` stops with `routing-only range changes a non-handoffs path` because `.gitattributes` changes later at `bd5301d3485e673e1bfda1828ac95dbebf295b1b`.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

The committed test-first evidence materially improves the package, but it does not exercise or enforce the cleared schema, receipt, schedule, queue, deadline, or telemetry contracts. No design ambiguity requires a new design cycle.

## Batched executable findings

### BF1-R2 — lifecycle accepts invalid receipts and does not enforce governed active controls

**Production path and violated contract.** `src/m4_final_prescoring_crash_cart.py`, `CrashCartLifecycle._pair`, `active`, and `run` validate only exact receipt key names, `status=PASS`, and ordinal. They do not require `backend_code=null`, distinct bound role sessions, canonical request digest, 64-hex prior/result state digests, or prior-to-result state chaining. `_pair` receives only kind/ordinal/prompt digest rather than the full warmup controls or public fixture. `active()` iterates 64 pairs immediately; it does not consume `active_schedule()`, bound queue capacity eight, the 60-second deadline, or a telemetry sampler. `run()` returns the planned schedule and 241 generated timestamps as if they were execution evidence.

**Minimal reproducer.** Supply both role callbacks with seven-key `PASS` receipts containing `backend_code="NON_NULL"`, identical `session_id="SAME_SESSION"`, non-digest state strings, and `request_sha256="wrong"`, while preserving the requested ordinal. `CrashCartLifecycle.run()` accepts all 68 pairs. With instant callbacks it completed in approximately 0.014 seconds yet returned final scheduled offset `30000000000` and 241 telemetry timestamps.

**Expected terminal behavior and evidence.** The first invalid receipt must stop with the bound receipt/correlation failure, attempt paired rollback, reset both roles, execute cleanup exactly once in `finally`, and emit only actually observed staged evidence. No later pair, scheduled-offset claim, queue observation, or telemetry sample may be fabricated. A valid injected run must prove actual dispatch against offsets, bounded queue behavior, the hard deadline, observed 250-ms samples, complete role/session/state/request chains, and no retry/drop.

**Smallest correction.** Extend the injected seam with deterministic clock/sleeper, bounded queue, deadline, and telemetry-sampler interfaces; pass the full frozen request/control object into each role; validate backend code, role/session binding, canonical request digest, digest syntax, and exact prior/result chain before accepting each pair. Record actual dispatch/sample observations rather than returning `telemetry_schedule()` as evidence.

**Required committed closure test/mutation.** Add focused subtests that mutate each receipt field and chain link, reuse one session across roles, omit an offset wait, bypass the queue, exceed the fake-clock deadline, and return planned rather than sampled telemetry. Each mutation must be killed by an exact fail-closed code plus rollback/reset/cleanup and no-later-evidence assertions. Use a fake clock so no wall-clock 30-second run is needed.

### BF2-R2 — `_compose_schema` is a required-key check, not JSON Schema composition

**Production path and violated contract.** `src/m4_final_prescoring_crash_cart.py::_compose_schema` loads the committed schema but only checks that its top-level `required` names occur. It never applies types, constants, `additionalProperties`, `$defs`, `oneOf`, or conditional rules. The subsequent semantic checks accept deeply schema-invalid terminal evidence.

**Minimal counterexample.** A `COMPLETE_ACTIVE_TERMINAL` with all required top-level keys but `schema_version="WRONG"`, `regime="X"`, `classification="SCORING_RESULT"`, empty authority/identity/invocation objects, empty candidate/peer row objects, fabricated non-empty samples/trends, `structural_failures=["SHOULD_BE_EMPTY"]`, a status-only replica object, incomplete cleanup/public-safety/export objects, and otherwise satisfying the small semantic count checks is accepted.

**Expected terminal behavior and evidence.** Schema validation must reject this record before semantic acceptance with `REPORT_SCHEMA_INVALID`; no renderer/export/complete-terminal status is permitted. Every report accepted by `validate_terminal` must first validate against the exact committed schema, then pass cross-field semantic checks.

**Smallest correction.** Use a pinned, repository-supported Draft 2020-12 validator or implement the exact committed schema semantics without external acquisition. Run complete schema validation before stage semantics and map all validation failures deterministically to `REPORT_SCHEMA_INVALID` without leaking private values.

**Required committed closure test/mutation.** Commit the full-top-level counterexample above plus nested mutations for schema constants, additional properties, row/receipt objects, replica counts, laws, cleanup, public safety, and export. Add a mutation that replaces full schema validation with the present required-key loop; the focused target must kill it.

### BF3-R2 — focused evidence overclaims the corrected production paths

**Production path and violated contract.** `tests/test_m4_final_prescoring_crash_cart.py::test_schedule_queue_deadline_and_telemetry` asserts constants and the length of a generated tuple; it does not execute scheduling, queueing, deadlines, or sampling. `test_symmetric_barriers_resets_rng_no_priming_and_receipt_ordinals` checks returned ordinals and event ordering but not full control delivery, receipt/state chains, dispatch time, queue behavior, or observed telemetry. `test_strict_schema_counterexamples` uses reports missing required top-level keys, so the required-key loop rejects them before nested schema semantics are tested.

**Minimal evidence discrepancy.** The exact focused suite passes 13/13 and the pre-correction probe reports six failures, while the BF1 and BF2 counterexamples above are still accepted. Therefore the manifest claims for schedule/queue/deadline/telemetry and schema-composed staged negatives are not demonstrated by the committed tests.

**Expected terminal behavior and evidence.** The focused suite and pre-correction/mutation boundary must fail whenever either counterexample is reintroduced, and its named tests must execute the relevant production path rather than only assert constants.

**Smallest correction.** Replace the constant-only and missing-key adversaries with the BF1/BF2 injected production-path tests; retain the useful candidate-ordinal-0 cleanup test, ordered 64-digest inventory test, wrapper test, and prior-source probe.

**Required committed closure test/mutation.** The same committed focused suite must pass on the corrected source, fail on `ff1635412cab8a2754ecaeab14daf3c0d7892b65`, and kill at minimum required-key-only schema validation, invalid-receipt acceptance, schedule bypass, queue bypass, deadline bypass, and fabricated telemetry mutants with exact expected failure classifications.

### WF1 — declared review result is not helper-compatible

**Exact boundary.** The canonical manifest declares `review_result_sha=3f9f685a1f88c9f18f916688ce9a574f19e246e8`, but `.gitattributes` changes afterward at `bd5301d3485e673e1bfda1828ac95dbebf295b1b`; the standard helper therefore rejects the supposedly routing-only tail.

**Smallest packaging correction and regression.** Preserve substantive implementation identity `3f9f685a1f88c9f18f916688ce9a574f19e246e8`, but update the canonical helper review result to `bd5301d3485e673e1bfda1828ac95dbebf295b1b` (or a later exact commit after all non-`handoffs/` bytes). Revalidate the manifest and require the standard `workflow_checkout.py create` intake to pass unchanged before routing.

## Clear evidence and immutable preservation set

- From repository root, the focused target returns 13/13 PASS; the exact prior-source probe returns `PRECORRECTION_KILLED`, six failures; the wrapper exits 2 with `RUN_AUTHORITY_ABSENT`.
- The ordered 64-prompt digest inventory is exact, unique, sidecar-bound, and reproduced by `fixture_inventory()`.
- Candidate warmup ordinal-0 failure reaches peer, paired resets, rollback, and finally cleanup in the committed test.
- Correction-range preflight reports 64 fixed-regex matches and zero gitleaks findings. Every match is a substring of a public Git/SHA-256 identity or fixed public timing/count control; no prohibited content was found.
- `git diff --check` is clean. BF4 `.gitattributes` inventory closure remains banked.

The next correction must preserve byte-identical: the cleared design/schema/launch/gate artifacts and sidecars; beta/Rebecca/Coordinator authorities; BF4 inventory closure; the 64-entry prompt inventory and sidecar; literal-LF warmup identities; HELD-law projection; fail-closed wrapper; production integration seam; public model/runtime identities; and all no-run/no-custody/no-scoring/no-science holds. Preserve the useful 13-test and prior-probe evidence while strengthening only the affected tests and implementation paths above.

No model/tokenizer/OCI/WSL2/gofast workload, protected input, held access, custody, scoring, science, state/provenance mutation, merge, publication, readiness declaration, retry, or gate action occurred.

## Disposition

Return **COMBINED BLOCK** to **WORKFLOW COORDINATOR**. Exact next recipient: **TASK BUILDER** for one final test-first BF1-R2/BF2-R2/BF3-R2 plus WF1 packaging correction. All banked clear evidence and standing holds remain binding.
