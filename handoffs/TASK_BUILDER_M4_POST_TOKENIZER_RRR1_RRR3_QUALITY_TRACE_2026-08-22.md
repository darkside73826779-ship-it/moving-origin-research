# M4 post-tokenizer RRR1–RRR3 quality trace

Date: 2026-08-22 EDT

Implementation: `1663d6d46b96412373af610bf3c83f397a2dfc0b`

## Requirement → production branch → test → evidence

| Requirement | Production branch | Production-path test | Evidence |
|---|---|---|---|
| RRR1 make the verified fanout capability unusable outside the exact phase-one path and bind the eventual request | `FanoutCoordinator._phase_one`, sole public `FanoutCoordinator.step`, and `SyntheticFixtureDispatcher.dispatch` | `test_public_fanout_reconciles_fabricated_views_metadata_stop_and_request`; ordinary and exact-fixture fanout tests | `_VerifiedFanoutInput`, `_validate_verified`, and `_step_verified` no longer exist. Phase one returns no reusable executable capability. The only call path snapshots the eventual request, rederives prompt and stop through the provider, reconciles ordered sanitized metadata, and supplies the same snapshot to both adapters and the receipt. A fabricated self-consistent prompt/stop attempt must call the provider and makes zero backend calls; caller drift during candidate execution cannot alter the frozen request identity. |
| RRR2 distinguish verified cleanup from ordinary NOT_LIVE after a throwing liveness probe | `AdapterFactory._attest_live` through `_dispose_verified`; `_construct` and `create_pair` cleanup routes | `test_factory_requires_live_attestation_and_cleans_each_role`; banked pair cleanup test | A throwing probe invokes disposal and a second liveness observation. Only a verifiably non-live backend receives the role-specific NOT_LIVE projection. No-op, partial, throwing, or unobservable disposal projects `BACKEND_ROLLBACK_FAILURE`. Candidate, peer, and control adversaries assert real backend residue and role ordering; successful pairs remain live before exposure. |
| RRR3 replace prose mutation claims with deterministic executable evidence | `tests/run_m4_post_tokenizer_mutation_tests.py`; canonical mutation contract and transcript | runner `--verify` in the exact pinned read-only OCI image | The runner authenticates raw indexed Git blobs, independently writes each exact mutant into an isolated temporary checkout, executes one fully qualified production test, records exit/stdout/stderr, restores the baseline byte-for-byte, and compares the complete canonical transcript. Fourteen of fourteen exact mutants are killed. |
| Preserve RRIR2 law fail-closed and numeric/domain semantics | `validate_laws`, `LAW_METRIC_DOMAINS` | `test_pass_law_rows_fail_closed_without_full_artifacts_and_reject_domains`; law field-mutation suite | Exact PASS/FAIL/HELD/NOT_RUN row semantics, all five numeric/domain projections, L18 relationships, and `LAW_PASS_UNAVAILABLE` remain production-covered. |
| Preserve RRIR3 episode history/current-state consistency | `validate_state`; restore/reset/close and public pre-state gates | `test_episode_history_is_durable_consistent_and_prevents_restored_reuse`; 42-cell lifecycle matrix | History uniqueness, length/ordinal/current binding, restored-state validation, non-reuse, and close preservation remain covered before backend calls. |
| Preserve rollback, fixture, frozen-provider, pair-prevalidation, tokenizer, and identity banks | transaction restore; fixture dispatcher; pair factory; wrappers and inventories | rollback adversaries; exact fixture and 13 negatives; nondeterministic provider; pair cleanup; integration and tokenizer wrappers | All previously banked production tests pass unchanged in the fresh and pinned-container runs. The tokenizer package and `.gitattributes` identities remain byte-for-byte unchanged. |

## Ordered boundary traces

1. Public fanout: pair identity → request type → deep-copy exact eventual request → ordered sanitized rows → provider prompt rederivation → prompt length/digest → provider stop rederivation → stop length/digest → immutable candidate/peer views → transaction snapshots → candidate call with snapshot → peer call with the same snapshot → post-return mutation check → receipt digest from that snapshot.
2. Forgery adversary: arbitrary self-consistent public rows/stop/request → sole public `step` → provider invocation → rejection before snapshots or backend calls. There is no object or method that can accept an externally fabricated verified capability.
3. Factory success: validate both specs and pair identity → construct candidate → bind session → literal-live attestation → construct peer → bind session → literal-live attestation → expose pair.
4. Throwing liveness probe: probe throws → dispose → second probe. Verified false → role-specific NOT_LIVE; true, throwing, partial, no-op, or throwing disposal → `BACKEND_ROLLBACK_FAILURE`. Pair construction also disposes the already-live first half and verifies zero residue.
5. Mutation replay: authenticate contract/runner/baseline indexed blobs → isolated checkout → exact one-occurrence replacement → mutant SHA-256 → fully qualified test → nonzero kill record → exact baseline restoration → next mutant → canonical transcript equality.

## Executable mutation evidence

Canonical contract: `specs/data/m4_post_tokenizer_mutation_contract_v1.json` (`1de6c4b453d8b90625ce253cf0fef15b7765403c2b5a8e6a4409a42da86ad1a4`).

Canonical transcript: `artifacts/m4_post_tokenizer_mutation_transcript_v1.json` (`2882a172d9f0ca76bb698a00ca50aebc7d253519aa60e31a12094cd60c352cfd`).

Exact killed mutants: `RRR1_NO_CALLABLE_CAPABILITY`, `RRR1_PROVIDER_SANITIZED_RECONCILIATION`, `RRR1_EXACT_EVENTUAL_REQUEST_SNAPSHOT`, `RRR2_THROWING_LIVENESS_CLEANUP_VERIFICATION`, `RRR2_DISPOSAL_POSTCONDITION`, `RRIR2_PASS_FAIL_CLOSED`, `RRIR2_METRIC_DOMAINS`, `RRIR3_HISTORY_CURRENT_BINDING`, `RRIR4_LIVE_ATTESTATION`, `BANKED_ROLLBACK_IDENTITY`, `BANKED_FIXTURE_CLOSE_DISPATCH`, `BANKED_FROZEN_PROVIDER`, `BANKED_PAIR_PREVALIDATION`, and `BANKED_STATE_VALIDATOR`.

Mutation summary: 14/14 KILLED. The contract contains every exact old/new patch, occurrence count, mutant SHA-256, fully qualified command, and expected exit. The transcript contains each observed exit and normalized stdout/stderr plus clean-restoration evidence; there are no placeholder commands or identities.

## Exact verification

- Fresh `core.autocrlf=true` identity-first integration wrapper: 49/49 PASS.
- Exact pinned WSL2-backed OCI image, network disabled, read-only checkout, no custody: integration 49/49 PASS.
- Same exact pinned OCI/no-custody controls: mutation replay 14/14 KILLED and transcript equality PASS.
- Same exact pinned OCI/no-custody controls: banked tokenizer suite 37/37 PASS.
- Complete lifecycle matrix: 42/42 cells PASS.
- Exact fixture: complete sequence plus 13/13 negatives through production paths.
- Raw committed combined inventory: 68/68 identities reproduce; contained sidecars: 27/27.
- Source SHA-256: `54ecc77b9062683f56043984b297c1472f781797e1e5af4af861e069418a5d47`.
- Test SHA-256: `5d46c7a39d61fee888b5948e026e8b887235af8c5c46f17386f30d87b07f4227`.
- Integration wrapper SHA-256: `09e1f4182e41c3507de89f570a1839fe951c4e74d79f28f70806aa78b4a8e21c`.
- Mutation runner SHA-256: `9e8e49a5c1df139508d60ded33e50170b3ed940c1096e3d2e8afe32c6b2281f5`.
- Combined inventory SHA-256: `60abf1dd5f70c06059754ba23126e2a9463cd48cbee2ef228e611df69082eb27`.
- Integration launch-contract SHA-256: `2d1e288c533945295929737e17109113f304c91ac9a41c98d30a4cd498b2f1de`.
- `git diff --check` and `git fsck --full`: PASS; fsck reports only unreachable local development objects.
- Tokenizer/materializer invocation and private custody/model/tokenizer access: zero.

One initial custody-free OCI command did not create a container because PowerShell removed a shell variable and Docker treated Python's `-I` as its own option. The exact literal-token command was then used; this was pre-container instrumentation correction, not a package execution or held operation.
