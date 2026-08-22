# TASK BUILDER M4 public-model observation backend quality trace

Date: 2026-08-22

Regime: B

Result: COMPLETE — pending independent persistent-CRITIC review

Implementation: `b6fe5de15cca6aecd4883b1bc2e4907b58f85c08`

## Delta and dependency closure

The delta adds the control/naive-only public-model observation backend, identity-first custody-free test runner, six-mutant adversarial runner, implementation identity lock, and sanitized mutation transcript. The existing production seam `src/m4_post_tokenizer_integration.py` remains byte-identical to seam base `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`: 49,119 raw bytes, SHA-256 `8964de5daf745226771818ab59f2cc75ef29ccbc5d09b43b6dae102b876b2f1b`. No unchanged banked suite or tokenizer evidence was reopened.

## Requirement → production branch → test → evidence

| Requirement | Production branch | Production-path test/evidence |
|---|---|---|
| Control/naive only; reject every other registration before construction | `PublicObservationFactory.create/create_pair` | `test_registration_rejects_every_non_control_naive_before_construction`; ROLE_GUARD_WEAKENED killed |
| Exact zero-engine live constructor and protocol surface | `PublicModelObservationBackend.__init__`, `is_live`, `capture_state` | `test_constructor_live_without_engine_and_exact_protocol_surface` |
| Exact manifest/config/dependency/HELD identities; stage absolute, existing, non-link, empty, mode 0700 | `_validate_description`, `_validate_stage`, invalid-stage snapshot sentinel | `test_describe_is_seven_field_no_engine_and_dependency_stage_fail_closed`; separate absent/link/nonempty/wrong-mode cases; STAGE_MODE_INVERTED and LAW_STATUS_UNCHECKED killed |
| Runtime/model/namespace authentication precedes the only engine load | `_validate_runtime_identity`, `initialize` | `test_initialize_authenticates_identity_before_one_stub_load`; separate false/None/0 namespace cases; NAMESPACE_TRUTHINESS killed |
| Load failure has no retry or live residue | `initialize` through `_operate/restore_state` | `test_engine_load_failure_has_no_retry_or_residue`; FAILURE_CODE_UNREGISTERED killed |
| Three fixed prompts, one stored ordinal per episode, exact digest/order | `generate_public_prompt`, `_validate_prompt_request`, `reset_episode` | exact generator hashes plus three distinct ordinal/digest/order negatives |
| Authenticated private view remains process-local; exact framing/count/context/full ID-domain validation | `_decode_private_view`, `step` | separate bad magic, count, length, negative, nonmember, and context cases, all before stub generation |
| Exactly one deterministic stub generation; sanitize counts/hashes/timing; erase arrays | `step` generation and `finally` | three production adapter episodes; exception/multiple/raw-field negatives; input/output references all zero; OUTPUT_ZEROIZATION_REMOVED killed |
| Seven-field receipts only; internal reasons never published | `_receipt`, `_operate` | all positive receipts exact; failure code maps only to `SYNTHETIC_REJECTED`; unregistered-code mutation killed |
| Atomic local JSON+sidecar, LF/mode/semantic validation; no raw or private fields | `_validate_observation`, `_write_exclusive`, `_publish` | three schema-valid sanitized pairs; partial-write rollback; forbidden raw-field attempt; no Git artifact created by runtime |
| Every adapter rejection restores exact backend state and stage inventory | `capture_state`, `restore_state`, cleared adapter transaction | full receipt-rejection matrix plus no-op/partial/wrong/throwing restore adversaries |
| Close/dispose passes only after verified zero residue | `_shutdown_engine`, `close`, `dispose` | successful close plus surviving-engine cleanup failure with no close PASS |
| Exact five HELD laws only; no PASS/FAIL promotion | `held_law_rows`, `_validate_description` | exact 974-byte projection/digest and promotion adversary; LAW_STATUS_UNCHECKED killed |
| Run remains unauthorized; topology classifier exact | identity-first test runner and `classify_network_connect` | launch arguments return `RUN_AUTHORITY_ABSENT` exit 2 before environment access; errno 101→0, other errno→2, connect→3; pinned `/usr/bin/unshare` positive and outbound-denial smokes PASS |

## Ordered boundary traces

Registration: role/arm guard → constructor lookup → backend construction → literal-live attestation. Every rejected role/arm stops at the first event; constructed instance count remains zero.

Initialize: adapter request/schema/state authentication → backend prior-state authentication → exact model/runtime identity probe → literal namespace attestation → one injected stub loader → literal engine liveness → exact live-engine count → PASS receipt. False, `None`, and integer-zero namespace observations stop before loader; engine list remains empty.

Step: adapter request and private-view authentication → prior-state/episode/prompt identity checks → backend private framing/count/context/full-domain checks → one stub `generate` call → result shape/type checks → sanitized observation validation → temp JSON and sidecar fsync → atomic renames → directory durability → state-bound PASS receipt → adapter receipt/state/private-view postchecks. Any failure restores the exact pre-call state/inventory. Mutable prompt, input IDs, output IDs, and output text references are erased/released in `finally`.

No model, tokenizer, private custody, prompt seed, inference, scoring, qualification, or science operation occurred. Only fabricated token IDs and the deterministic stub engine were used.

## Exact verification

- Windows identity-first focused suite: 17 discovered, 16 executed PASS, one host-privilege symlink case skipped.
- Ubuntu 24.04 WSL2 identity-first focused suite: 17/17 PASS; directory-symlink case realized.
- Windows and WSL2 deterministic mutation runs: baseline PASS; 6/6 predefined mutants KILLED; no instrument failures; source restored byte-for-byte after each mutant.
- Pinned `/usr/bin/unshare`: 43,624 bytes, expected SHA-256; custody-free positive namespace smoke PASS; outbound IPv4 connect denied with governed errno 101 classifier PASS.
- Launch-form invocation against committed `run_authorized=false`: `RUN_AUTHORITY_ABSENT`, exit 2, before stage environment/model/tokenizer access.
- Python compilation, canonical JSON, LF and sidecar reproduction: PASS.

All runtime/science/scoring/private-access/merge/publication/gate holds remain binding.
