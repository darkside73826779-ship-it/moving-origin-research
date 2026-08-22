# TASK BUILDER M4 post-tokenizer integration quality trace

Date: 2026-08-22 EDT
Status: COMPLETE implementation verification; independent CRITIC review required
Release: `071392aadfcdf6c76b47f3f959578661658f7791`
Baseline: `cee97538893989e055f49a894f066d2083da4eb5`
Cleared design: `b5b8028a7126e838c239ba0927b526f9cec8b7e2`
Cleared tokenizer source: `ddae7c3b8f664cbc94654198916e1940c9006c1e`

## Requirement → production branch → test → evidence

| Requirement | Production branch | Production-path test/evidence |
|---|---|---|
| Exact role/arm factory and no implicit synthetic fallback | `AdapterFactory.create` schema → registry → role/arm → channel → construction order | `test_factory_negatives`; distinct `BACKEND_NOT_REGISTERED`, `SYNTHETIC_FALLBACK_FORBIDDEN`, `ROLE_ARM_MISMATCH`, and `REGISTRY_IDENTITY_MISMATCH` assertions |
| Candidate/peer same checkpoint and training identity, distinct isolation fields | `validate_pair_identity` checks all 12 equality fields before six difference fields and exact session/access/channel projections | positive pair fixture plus one adversarial mutation per equality and difference field |
| Complete public lifecycle and exact no-mutation failures | `BaseAdapter.describe/initialize/reset_episode/step/snapshot/close` | `test_full_42_cell_lifecycle_matrix_through_public_methods` executes all 42 cells; repeated, closed, completion, episode, reset/request/snapshot ordinal cases assert call deltas and byte-identical state |
| Caller-identity concurrency precedence | `_enter` compares the canonical caller identity before request parsing/backend invocation | `test_inflight_and_reentrant_precede_parsing` asserts same identity → `ADAPTER_REENTRANCY_FORBIDDEN`, different identity → `ADAPTER_OPERATION_IN_FLIGHT`, zero calls, identical state |
| Complete receipt failure projection | `_call` validates status, registered FAIL code, session, prior token, and request correlation after exactly one backend call and before state commit | seven production tests cover missing status, malformed/unregistered FAIL, registered FAIL, exception, session, state, and response ordinal; all assert one call and identical durable state |
| Canonical immutable private view | `encode_private_view` and `PrivateTokenView` implement the fixed ASCII/NUL/count/int64 domain | exact 1024/4096/8192/stop fixture digests reproduced; writable and mutation-evidence adversaries rejected pre-call |
| Ordered sanitized reconciliation and stop rederivation | `FanoutCoordinator._phase_one` performs missing → duplicate → order → length → prompt digest → sanitized stop → rederived stop → context → received hashes → immutability | each compound case is realized separately with zero candidate/peer step calls and identical pre/post snapshots |
| Two-phase candidate/peer fanout | `FanoutCoordinator.step` snapshots both adapters, calls candidate then peer, and commits only two valid receipts | positive rows independently execute 1024/4096/8192; candidate failure proves 1/0; peer failure proves 1/1, `FANOUT_ATOMICITY_FAILURE`, and exact restoration |
| Honest law projections | `held_law_projection` + `validate_laws` | exact L7/L8/L10/L14/L18 order; L8 reason `L8_PREREQUISITE_UNCLEARED`; duplicate, missing, reorder mutations rejected; every row is HELD/no-claim with empty evidence/metrics |
| Path-selective combined tree and PASS evidence | fixed 38-path overlay plus four seam files; rebinding changes only `.gitattributes`, the legacy wrapper constant, executable-package dependent row/sidecar, and new downstream inventory/launch artifacts | complete 63-row raw inventory records bytes, SHA-256, Git blob, mode, and source domain; tokenizer PASS pair/sidecar reproduced from the cleared source |
| Identity-first executable package | standard-library-only `tests/run_m4_post_tokenizer_integration_tests.py` verifies raw identities before adding `/workspace` and importing exactly the selected test module | fresh detached checkout passed 32/32; expected discovery count is bound to 32 |
| Banked tokenizer regression | rebound legacy wrapper retains all package rows except the directly affected checkout-identity and wrapper rows | exact pinned, network-none, read-only container passed 37/37; no custody environment/mount/output and no materializer invocation |

## Ordered access/event traces

Successful fanout trace:

1. validate ordered sanitized public rows;
2. rederive prompt and stop arrays through the injected process-local provider;
3. encode and verify length/digests;
4. validate context association;
5. construct immutable candidate and peer views;
6. independently hash both received views and validate mutation evidence;
7. snapshot both durable adapter states;
8. call candidate backend once without public commit;
9. call peer backend once without public commit;
10. commit both valid receipts atomically and emit only sanitized digest/length/runtime evidence.

Failure boundaries:

- Steps 1–6 failure: candidate 0, peer 0, control 0, identical durable states.
- Step 8 failure: candidate 1, peer 0, both snapshots authoritative.
- Step 9 failure: candidate 1, peer 1, `FANOUT_ATOMICITY_FAILURE`, both snapshots restored.
- Adapter receipt validation failure: exactly one backend call, no public-state commit.
- In-flight/reentrant/lifecycle/ordinal failure: zero backend calls, identical durable bytes and SHA-256.

## Adversarial gate

The suite separately mutates every paired equality/difference field; receipt status/session/prior token/failure code/response ordinal; each sanitized context cardinality/order/length/digest; stop metadata and rederivation; received-view equality/writability/mutation evidence; lifecycle state/completion/episode/ordinal; and law uniqueness/completeness/order. Each mutation is killed by the expected production branch and asserts its backend-call and state-preservation boundary.

## Exact execution evidence

- Fresh-checkout public wrapper: 32/32 PASS.
- Pinned OCI integration command: 32/32 PASS; `--pull=never`, Linux/amd64, network none, read-only root, all capabilities dropped, no-new-privileges, bounded noexec tmpfs, read-only repository, explicit Python entrypoint.
- Pinned OCI banked tokenizer suite: 37/37 PASS under the same custody-free controls.
- `git diff --cached --check`: PASS.
- Tokenizer materializer starts: zero.
- Custody/model/tokenizer access: zero.
- Scientific/scoring/seed/state/provenance actions: zero.

Aggregate counts are supplementary; the row-level assertions and event traces above are the completion evidence.
