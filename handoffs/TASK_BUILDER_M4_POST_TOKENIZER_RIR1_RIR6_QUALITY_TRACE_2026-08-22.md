# M4 post-tokenizer RIR1–RIR6 quality trace

Date: 2026-08-22 EDT

Implementation: `cf80b99862cf8bd1f6ee3145e98f543f61121daa`

This trace records production-entrypoint evidence for every authorized rereview finding. Helper-level tests are supplementary only; each closing test invokes the public factory, adapter, coordinator, dispatcher, or law validator that governs the behavior.

## Requirement → production branch → test → evidence

| Requirement | Production branch | Production-path test | Evidence |
|---|---|---|---|
| RIR1 full-pair validation before construction; actual backend-session binding; specific role/channel codes; zero residue | `AdapterFactory.create_pair`, `_construct`, `_dispose_verified` | `test_pair_prevalidation_second_half_cleanup_session_binding_and_specific_codes` | Invalid second halves construct neither backend. Second-constructor and peer-session failures dispose all constructed sessions and verify none remain live. Role/channel failures retain their specific codes. |
| RIR2 validate every operation against the exact lifecycle and cross-field state machine, including post-state and restore | `validate_state`; `BaseAdapter.capture`, `restore`, `_call`, `describe`, `initialize`, `reset_episode`, `step`, `close`, `durable_state` | `test_state_machine_cross_field_mutations_and_public_prestate_gate`; existing complete lifecycle matrix | Every public operation rejects corrupted pre-state before backend calls; every successful transition validates its post-state; invalid post-state rolls back. All 42 lifecycle cells pass. |
| RIR3 canonical rollback receipts and verified backend-state restoration across all rollback routes | `capture_transaction`, `restore_transaction`, `_call`; `FanoutCoordinator.step_verified` rollback branches | `test_rollback_identity_rejects_noop_partial_wrong_and_throwing_restorers_all_routes` | Canonical backend snapshot digest is frozen before mutation. Restore re-captures and compares backend identity. No-op, partial, wrong, and throwing restorers are rejected as `BACKEND_ROLLBACK_FAILURE` on candidate, peer, and post-return routes. |
| RIR4 exact law-specific PASS/FAIL/HELD/NOT_RUN schemas for L7/L8/L10/L14/L18 | `validate_laws`, `held_law_projection` | `test_law_all_status_semantics_and_field_mutations` | Every status for all five laws passes only with exact meaning source, evidence tuple, metric keys/types/domain, failure code, reason, and claim flag; every field is independently mutated and rejected. |
| RIR5 execute the parsed fixture sequence including close paths and compare the complete realized trace; execute all negative rows | `SyntheticFixtureDispatcher.dispatch`, `realize_negative` | `test_exact_fixture_dispatch_and_all_negative_boundaries`; `test_fixture_is_parsed_and_every_declared_row_and_sequence_executes` | The exact committed sequence is dispatched, candidate/peer/control close paths execute, full realized trace equals every expected fixture field, and all 13 negatives verify exact code, backend-call count, and mutation expectation. |
| RIR6 freeze verified phase-one context length/digest and forbid provider re-read drift | `VerifiedFanoutInput`; `FanoutCoordinator.verify`, `step`, `step_verified` | `test_frozen_phase_one_evidence_prevents_nondeterministic_provider_reread` | Context length, context digest, stop length/digest, and private views are captured once and used unchanged for publication. A provider that fails on any second read completes with exactly one prompt and one stop read. |

## Ordered construction, access, rollback, and publication traces

1. Pair construction: canonical parse → schema/dependency/identity validation of candidate → schema/dependency/identity validation of peer → pair role/channel validation → candidate constructor → candidate session-identity bind → peer constructor → peer session-identity bind → return pair. Any construction-phase failure disposes every created backend and confirms `is_live() == false`.
2. Adapter operation: validate current adapter state → validate complete request → capture adapter and real-backend transaction snapshot plus canonical digest → call backend → validate exact receipt → derive and validate post-state → commit adapter identity. Any backend, receipt, or post-state failure restores both adapter and backend and verifies the recaptured backend identity.
3. Fanout: use frozen phase-one input → capture candidate and peer transactions → candidate call → peer call → construct sanitized receipt from frozen context/stop identities → return. Candidate, peer, or post-return failure restores every affected backend and verifies exact state identity before surfacing the governed failure.
4. Fixture: parse committed fixture → dispatch each literal sequence entry → realize all declared fanout/close/law actions → execute each negative independently → compare the complete realized trace to the fixture expectation.

## Adversarial audit

Six selected production mutations were independently applied and each was killed by the governed suite: bypass pair prevalidation; bypass state validation; bypass rollback identity comparison; loosen law metric exactness; skip close-path dispatch; re-read the provider after phase one. Result: 6/6 killed.

## Exact verification summary

- Fresh `core.autocrlf=true` identity-first wrapper: 45/45 PASS.
- Exact pinned network-disabled, read-only, no-custody OCI integration suite: 45/45 PASS.
- Exact pinned network-disabled, read-only, no-custody banked tokenizer suite: 37/37 PASS.
- Complete lifecycle matrix: 42/42 cells PASS.
- Synthetic fixture negatives: 13/13 realized through production dispatch.
- Combined inventory: 63 entries; all governed JSON sidecars reproduce raw-byte SHA-256.
- Source SHA-256: `f56746688c296260071cfb13eab8a771335bc3c4cb6dd0a247e0e3d7aa46516f`.
- Test SHA-256: `e1807a5755f2b39d5112fefde4bf0d2970d1533854f7fa639a4cdc8e1a9788e5`.
- Combined inventory SHA-256: `6e2265535975dd96a922a6a6afa4a925d02a396e6f4a8f2573556bc64d69e078`.
- Integration launch-contract SHA-256: `34abb1107a555b18010b6987dff5de96d6e63c20c20675422a1697b732792607`.
- Materializer/tokenizer invocation and private custody/model/tokenizer access: zero.
