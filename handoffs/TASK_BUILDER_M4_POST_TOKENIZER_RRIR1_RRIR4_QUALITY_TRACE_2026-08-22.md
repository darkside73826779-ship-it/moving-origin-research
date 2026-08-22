# M4 post-tokenizer RRIR1–RRIR4 quality trace

Date: 2026-08-22 EDT

Implementation: `f44ad96b133096d0096a5c43574f47d69f489756`

## Requirement → production branch → test → evidence

| Requirement | Production branch | Production-path test | Evidence |
|---|---|---|---|
| RRIR1 eliminate the public verified-fanout bypass and reconcile the exact eventual request before calls | `FanoutCoordinator.step`, `_phase_one`, `_validate_verified`, `_step_verified`; `SyntheticFixtureDispatcher.dispatch` | `test_public_fanout_reconciles_fabricated_views_metadata_stop_and_request`; ordinary and fixture fanout tests | The capability class and execution method are internal and no longer exported/public. The frozen object binds canonical request SHA-256, candidate/peer byte identity, encoded lengths, expected digest, and frozen stop bytes/length/digest. Fabricated view, false length/digest, false stop metadata, foreign object, and request drift fail before either backend call. Fixture phase one now uses each exact eventual fanout operation ID. |
| RRIR2 prohibit false law claims and enforce row/domain/count/control relationships | `validate_laws`, `LAW_METRIC_DOMAINS` | `test_law_all_status_semantics_and_field_mutations`; `test_pass_law_rows_fail_closed_without_full_artifacts_and_reject_domains` | All five law rows retain exact status/claim/source/evidence/metric/failure/reason semantics. Numeric values must be finite and within law-specific domains. L18 requires at least three governed seeds, all six required arms, and `controls_passed=true`. The summary projection cannot authenticate the full per-seed/dose/dual-abstention/coupling/24-row artifacts, so even structurally plausible PASS rows fail closed as `LAW_PASS_UNAVAILABLE`; no summary-only scientific claim can be minted. |
| RRIR3 make episode history durable and consistent across validation, restore, reset, close, and every operation | `_initial_state`, `validate_state`; `BaseAdapter.durable_state`, `capture`, `restore`, `reset_episode`, all public pre-state checks | `test_episode_history_is_durable_consistent_and_prevents_restored_reuse`; complete lifecycle matrix | `used_episode_ids` is part of canonical durable state. It is an ordered, unique, nonempty-string history whose length equals `reset_ordinal`; the active episode must be the last history entry. Empty, duplicate, wrong-type, wrong-current, and ordinal-divergent restored histories fail before backend calls. A restored completed episode cannot reuse its ID, and close preserves the history. |
| RRIR4 require live backend attestation before exposing either pair half and clean failures | `AdapterFactory._construct`, `_attest_live`, `_dispose_verified`, `create_pair` | `test_factory_requires_live_attestation_and_cleans_each_role`; banked pair cleanup test | Candidate and peer constructors must return literal `is_live() is True`. Dead candidate, dead peer, and throwing-live candidate receive role-specific errors; every constructed backend is disposed and no live residue remains. Successful pair construction proves both sessions live before return. |

## Ordered boundary traces

1. Public fanout: pair identity → ordered sanitized rows → provider prompt rederivation → exact length/digest → stop rederivation → immutable candidate/peer projection → exact request digest freeze → complete frozen-capability reconciliation → transaction snapshots → candidate call → peer call → post-return mutation check → sanitized receipt from frozen identities.
2. Lifecycle: validate canonical state plus durable episode history → validate request → capture adapter/backend identity → call → derive post-state and append new episode atomically on reset → validate full post-state/history → commit. Every restore validates history/current/reset consistency before assignment.
3. Factory: validate both complete specs and pair identity → construct candidate → bind session → attest literal live → construct peer → bind session → attest literal live → expose pair. Any failure disposes all constructed sessions; dead/throwing-live branches leave zero residue.

## Executable mutation evidence

Each mutation was applied independently to an isolated checkout of the implementation commit. The named production test was executed with `python -m unittest <test>`; nonzero test exit killed the mutant, then the source was restored byte-for-byte before the next mutation. The mutation checkout finished clean.

| Mutation ID | Exact production mutation | Killing test | Result |
|---|---|---|---|
| RRIR1_VERIFIED_RECONCILIATION | replace `self._validate_verified(verified, request)` with `pass` | public fanout fabricated-view test | KILLED |
| RRIR1_REQUEST_BINDING | replace the request-digest mismatch condition with `if False` | public fanout request-drift test | KILLED |
| RRIR2_PASS_FAIL_CLOSED | replace `raise IntegrationError("LAW_PASS_UNAVAILABLE")` with a successful row return | law fail-closed/domain test | KILLED |
| RRIR2_METRIC_DOMAINS | replace the law-domain branch condition with `if False` | law fail-closed/domain test | KILLED |
| RRIR3_HISTORY_CURRENT_BINDING | replace both `history[-1] == state["episode_id"]` predicates with `True` | durable episode-history test | KILLED |
| RRIR4_LIVE_ATTESTATION | replace `self._attest_live(backend, role)` with `pass` | factory live-attestation test | KILLED |
| BANKED_ROLLBACK_IDENTITY | replace backend restore identity comparison with `if False` | rollback adversary test | KILLED |
| BANKED_FIXTURE_CLOSE_DISPATCH | disable the `exercise_close_paths` dispatch branch | exact fixture dispatch test | KILLED |
| BANKED_FROZEN_PROVIDER | add a provider reread after phase one | nondeterministic-provider test | KILLED |
| BANKED_PAIR_PREVALIDATION | replace pair identity validation with `pass` | pair prevalidation/cleanup test | KILLED |
| BANKED_STATE_VALIDATOR | return immediately from `validate_state` | state-machine mutation test | KILLED |

Mutation summary: 11/11 KILLED.

## Exact verification

- Fresh `core.autocrlf=true` identity-first wrapper: 49/49 PASS.
- Exact pinned WSL2-backed OCI image, network disabled, read-only checkout, no custody: integration 49/49 PASS.
- Same exact pinned OCI/no-custody controls: banked tokenizer suite 37/37 PASS.
- Complete lifecycle matrix: 42/42 cells PASS.
- Exact fixture: complete sequence plus 13/13 negatives through production paths.
- Raw committed inventory: 63/63 identities reproduce; contained sidecars: 25/25 reproduce.
- Source SHA-256: `9db0155a5de800774ff8476bf02993e340dfd785336890860587ab22daf2dfb7`.
- Test SHA-256: `4aa5690e9ccc8935b1d0753f11932754b69af539d9049a801d94a040770057d4`.
- Wrapper SHA-256: `bc955c2b8502387858092afd20313d2f09ac065749dc0fea2f709f36167fbede`.
- Combined inventory SHA-256: `9f53d4c214f11d8f04aad54ea17c8acb487b3c6fb24d70b464de57b2ac624bf5`.
- Integration launch-contract SHA-256: `edd2116c95aa48926dec4714c7f1c27712cc08b9750d67a861d4cc1472cd9772`.
- Tokenizer/materializer invocation and private custody/model/tokenizer access: zero.
