# M4 Post-Tokenizer Crash-Cart CC1–CC6 Remediation v1

Date: 2026-08-21
Regime: B
Status: design-only; no execution or implementation authority
Base package: `390b06dadd2a364160d851c19cf85927465213d0`
Authoritative review: `1cd82cfda155381fae1a1d9e176a1fe67c265dae`

This document closes CC1–CC6 without changing the banked same-checkpoint rule, no-custody boundary, ordered tokenizer reconciliation, first-failure behavior, pinned runtime, path-selective construction, or scientific holds. It supersedes only underspecified portions of the base design.

## CC1 — mechanically complete backend and factory contract

### Exact role-to-arm table

| Role | Allowed scientific arms |
|---|---|
| `candidate` | `candidate` |
| `peer` | `peer` |
| `control` | `empty`, `permuted`, `shuffled`, `oracle`, `naive`, `frozen`, `specificity` |

Every other pair fails `ROLE_ARM_MISMATCH`. Candidate and peer checkpoint, training, tokenizer, architecture, parameter, quantization, decoding, calibration, evaluation, and binning identities are equal. Their `runtime_instance_id`, `access_policy_id`, role, arm, and channel policy are distinct. Controls use an explicitly registered transform and cannot inherit a candidate or peer channel.

### Immutable types and signatures

All byte inputs are immutable `bytes`; mappings are recursively frozen, string-keyed, and canonically encoded as RFC 8785 UTF-8 without LF when hashed. `PrivateTokenView` is the canonical byte string in CC4 and exposes only `context_length`, `byte_length`, `sha256`, and read-only bytes.

```text
RealBackendProtocol.describe(manifest: FrozenManifest, config: FrozenBackendConfig) -> BackendDescription
RealBackendProtocol.initialize(description: BackendDescription, session: SessionIdentity) -> BackendInitReceipt
RealBackendProtocol.reset_episode(prior: BackendStateToken, request: ResetRequest) -> BackendResetReceipt
RealBackendProtocol.step(prior: BackendStateToken, request: StepMetadata, tokens: PrivateTokenView) -> BackendStepReceipt
RealBackendProtocol.snapshot(prior: BackendStateToken, request: SnapshotRequest) -> BackendSnapshotReceipt
RealBackendProtocol.close(prior: BackendStateToken, request: CloseRequest) -> BackendCloseReceipt
AdapterFactory.create(role: Role, scientific_arm: ScientificArm, manifest_bytes: bytes, backend_config_bytes: bytes, private_token_provider: PrivateTokenProvider) -> ModelAdapterProtocol
```

The backend owns only its opaque `BackendStateToken` and one distinct session. The adapter owns public lifecycle state, ordinals, request correlation, canonical hashing, channel projection, private-token verification, response validation, and failure projection. The provider owns private rederivation and zeroization. The factory owns registry lookup, identity verification, role/arm enforcement, construction, and proof that candidate/peer session and access identities differ. No component may repair another component's invalid input.

Every backend receipt is a frozen record containing `status`, `backend_code`, `session_id`, `prior_backend_state_sha256`, `result_backend_state_sha256`, and operation-specific payload. `status=FAIL` requires a registered backend code and no adapter-state commit. Exceptions, malformed receipts, session mismatch, state-token mismatch, or response-correlation mismatch map respectively to `BACKEND_EXCEPTION`, `BACKEND_RECEIPT_INVALID`, `BACKEND_SESSION_MISMATCH`, `BACKEND_STATE_MISMATCH`, or `RESPONSE_CORRELATION_FAILURE`.

Factory/production negatives, all before a usable adapter is returned: unknown backend `BACKEND_NOT_REGISTERED`; synthetic entry on production path `SYNTHETIC_FALLBACK_FORBIDDEN`; invalid role/arm `ROLE_ARM_MISMATCH`; registry/config/implementation identity error `REGISTRY_IDENTITY_MISMATCH`; candidate/peer inequality `PAIR_IDENTITY_MISMATCH`; equal runtime session ids `SESSION_ISOLATION_FAILURE`; equal access-policy ids `ACCESS_ISOLATION_FAILURE`; peer privileged-channel exposure `PEER_CHANNEL_BYPASS`; invalid backend receipt/correlation uses the codes above. The synthetic fixture binds one row per code.

## CC2 — complete lifecycle, completion, and concurrency semantics

Public lifecycle state is one of CREATED, DESCRIBED, INITIALIZED, EPISODE_READY, STEPPED, CLOSED. Orthogonal fields are `operation_active: bool`, `active_operation_id: string|null`, `episode_complete: bool`, and monotonically increasing reset, request, and snapshot ordinals. A reset request carries a never-before-used episode id. A step request carries `is_terminal_request`; a successful terminal step sets `episode_complete=true`. A nonterminal step leaves it false. Snapshot does not complete an episode. Close is terminal.

Before any operation, the adapter atomically compares-and-sets `operation_active` from false to true and records the operation id. Failure to acquire returns `ADAPTER_OPERATION_IN_FLIGHT`, performs zero backend calls, and leaves the complete serialized state byte-identical. Reentrant calls on the same thread/session return `ADAPTER_REENTRANCY_FORBIDDEN` under the same rule. The flag and id are transient lock metadata excluded from durable state hashes and are cleared in a finally boundary. At most one backend call may exist per adapter instance; different adapter instances may proceed independently.

| Operation | Legal prior condition | Result/effect | Otherwise |
|---|---|---|---|
| describe | CREATED, inactive | DESCRIBED | `ADAPTER_LIFECYCLE_VIOLATION` |
| initialize | DESCRIBED, inactive | INITIALIZED | same |
| reset_episode | INITIALIZED, or STEPPED with `episode_complete=true`; inactive; fresh episode id; exact next reset ordinal | EPISODE_READY, complete=false, request=0, last response cleared | lifecycle, `EPISODE_NOT_COMPLETE`, `EPISODE_ID_REUSE`, or `RESET_ORDINAL_MISMATCH` |
| step | EPISODE_READY or STEPPED with complete=false; inactive; current episode; exact next request ordinal | STEPPED; increment request; copy terminal flag to completion | lifecycle, `EPISODE_ALREADY_COMPLETE`, `EPISODE_ID_MISMATCH`, or `REQUEST_ORDINAL_MISMATCH` |
| snapshot | STEPPED, inactive; exact next snapshot ordinal | STEPPED; increment snapshot only | lifecycle or `SNAPSHOT_ORDINAL_MISMATCH` |
| close | INITIALIZED, EPISODE_READY, or STEPPED; inactive | CLOSED, closed=true | lifecycle |

Repeated describe/initialize/close, reset before a terminal step, reset after a nonterminal step, step after terminal completion, reused episode ids, ordinal skips/duplicates, calls in flight, reentrancy, and every call after CLOSED are explicit negatives. Each records the exact code, zero backend calls, identical pre/post durable-state bytes and SHA-256, and unchanged ordinals. Backend failure after a legal transition attempt also commits no public state.

The complete state/operation matrix is below; `LEGAL` means the additional condition and ordinal checks above still apply. Every cell is evaluated only after the universal in-flight/reentrancy guard.

| Prior state | describe | initialize | reset | step | snapshot | close |
|---|---|---|---|---|---|---|
| CREATED | LEGAL | lifecycle violation | lifecycle violation | lifecycle violation | lifecycle violation | lifecycle violation |
| DESCRIBED | lifecycle violation | LEGAL | lifecycle violation | lifecycle violation | lifecycle violation | lifecycle violation |
| INITIALIZED | lifecycle violation | lifecycle violation | LEGAL | lifecycle violation | lifecycle violation | LEGAL |
| EPISODE_READY | lifecycle violation | lifecycle violation | lifecycle violation | LEGAL | lifecycle violation | LEGAL |
| STEPPED, incomplete | lifecycle violation | lifecycle violation | `EPISODE_NOT_COMPLETE` | LEGAL | LEGAL | LEGAL |
| STEPPED, complete | lifecycle violation | lifecycle violation | LEGAL | `EPISODE_ALREADY_COMPLETE` | LEGAL | LEGAL |
| CLOSED | lifecycle violation | lifecycle violation | lifecycle violation | lifecycle violation | lifecycle violation | lifecycle violation |

## CC3 — independently reproducible synthetic fixture

The adjacent fixture is executable data, not labels. Its generator is:

```text
token[i] = (context_length * 17 + i * 31) mod 32749, for i=0..context_length-1
stop[i] = 900000 + i * 17, for i=0..1
```

Canonical private bytes are defined in CC4. The exact byte lengths and SHA-256 values are:

| Kind | Count | Bytes | SHA-256 |
|---|---:|---:|---|
| prompt | 1024 | 8215 | `c96f4755a75ea441eafdea6412a641b2758338d4f2cbfa30b896c6cbfc9e6d69` |
| prompt | 4096 | 32791 | `a1f986f189fb077f1384df22d23ed4281eb2c8f5649ce66f4be8036beff1f72e` |
| prompt | 8192 | 65559 | `33a4f1905df626e464be9b801e8e3d0abf702ae6597f0813b31bfb2eee5eb26f` |
| stop | 2 | 39 | `fb9543fe31b55a34dbb69924e05690c75589208063637bbd08e5092d1cbb2a62` |

Fixture JSON supplies canonical manifest/config/request/state/receipt objects and each object's expected RFC-8785 SHA-256. Main candidate and peer instances each perform initialize; episode A nonterminal steps at ordinals 0 and 1; a terminal step at ordinal 2; reset to episode B; and a terminal step at ordinal 0. Thus each main backend has four step calls and two reset calls. Candidate and peer counts are independent, not pooled. Three additional adapter instances independently exercise close from INITIALIZED, EPISODE_READY, and STEPPED; none is reused after close. Every negative starts from a named immutable fixture state and declares expected backend-call delta zero and identical state digest.

## CC4 — canonical fanout and complete upstream suppression

Canonical `PrivateTokenView` bytes are exactly:

```text
ASCII("M4_PRIVATE_VIEW_V1") || 0x00 || uint32_be(item_count) || int64_be_twos_complement(item[0]) || ... || int64_be_twos_complement(item[n-1])
```

No BOM, delimiter, padding, native-width integer, platform endianness, or alternate encoding is allowed. Prompt and stop views use the same domain; context association lives in signed request metadata, not in the byte string. After sanitized reconciliation, the provider rederives both prompt and stop views, verifies both, freezes them, and supplies read-only views to candidate and peer. Each adapter independently hashes received bytes before its backend call.

Negatives are: candidate or peer received digest divergence `FANOUT_RECEIVED_DIGEST_MISMATCH`; writable view or mutation attempt `PRIVATE_VIEW_MUTATION_ATTEMPT`; post-return mutation evidence `PRIVATE_VIEW_MUTATED`; context/request mismatch `CONTEXT_REQUEST_MISMATCH`; rederived stop mismatch with otherwise valid sanitized stop metadata `STOP_REDERIVATION_MISMATCH`; sanitized missing/duplicate/reorder/length/array-digest/stop-digest faults; state, identity, lifecycle, role/arm, peer-channel, and response-correlation faults. Every upstream failure suppresses candidate, peer, control, and real-backend calls universally, emits only sanitized failure evidence, and preserves all adapter durable states byte-for-byte. If candidate succeeds but peer pre-call hashing fails, neither result is committed and the coordinator returns `FANOUT_ATOMICITY_FAILURE`; both initial snapshots remain authoritative.

## CC5 — exact law meanings and honest projections

The source authority is `docs/ARCHITECTURAL_CONSTITUTION.md`: L7 line 24, L8 line 26, L10 line 30, L14 line 40, and L18 line 52. This design neither changes those meanings nor selects held thresholds.

Every row contains `law_id`, `status`, `claim_made`, `meaning_source`, `evidence`, `metrics`, `failure_code`, and `held_reason`. Order is exactly L7, L8, L10, L14, L18. PASS requires `claim_made=true`, all law-specific evidence keys and metrics, no failure or held reason. FAIL requires `claim_made=false`, a law-specific failure, and the evidence that supports failure. HELD requires `claim_made=false`, empty metrics/evidence arrays, null failure, and one enumerated held reason. NOT_RUN is allowed only for instrument failure, also makes no claim, and cites the instrument-failure artifact.

| Law | Exact meaning and required PASS evidence shape | Deterministic law failures |
|---|---|---|
| L7 | Candidate self-report is calibrated against ground-truth internals and beats the matched peer observer; peer has behavioral outputs only; empty/permuted/shuffled contamination rows are present. Evidence keys: candidate/peer manifests, channel/redaction receipt, ground-truth receipt, AUROC, ECE, paired margin, contamination battery. | `L7_CALIBRATION_FAIL`, `L7_PEER_MARGIN_FAIL`, `L7_PEER_CHANNEL_INVALID`, `L7_CONTAMINATION_FAIL` |
| L8 | Regulation error responds dose-dependently when mirror calibration is degraded and satisfies the governed specificity controls; Level 0 and every governed dose are represented. Evidence keys: variable identity, dose schedule, mirror degradation receipt, regulation-error series, dose-response statistic, specificity panel. | `L8_DOSE_RESPONSE_FAIL`, `L8_SPECIFICITY_FAIL`, `L8_PREREQUISITE_HELD` |
| L10 | Below-threshold retrieval abstains rather than blending; the primary claim is evaluated under drift, with clean performance only a ceiling/context. Evidence keys: threshold identity, complete drift population, pre-abstention scores, abstention decisions, drift metric, clean secondary metric. | `L10_BLEND_BELOW_THRESHOLD`, `L10_DRIFT_METRIC_FAIL`, `L10_ABSTENTION_CALIBRATION_FAIL` |
| L14 | The same stakes variables are visible to the self-model, affected by memory quality, and targets for the thick present. Evidence keys: shared variable identity, visibility receipt, memory perturbation linkage, thick-present target linkage, coupling metrics. | `L14_VISIBILITY_FAIL`, `L14_MEMORY_COUPLING_FAIL`, `L14_THICK_PRESENT_FAIL` |
| L18 | Every positive claim has empty/permuted/shuffled negative controls, oracle positive control, frozen and naive baselines, and at least three governed seeds. Evidence keys: claim inventory, six-arm matrix, transforms, oracle reachability, seed-count receipt. | `L18_ARM_MISSING`, `L18_CONTROL_BEHAVIOR_FAIL`, `L18_ORACLE_FAIL`, `L18_SEED_REQUIREMENT_FAIL` |

Honest current projection is HELD for all five laws: Q2/EF3/scoring authority is absent; L8 additionally requires its prerequisite and native-L8 decision where applicable. In particular, L10 is present as a held retrieval-honesty claim, not silently omitted or structurally marked PASS. Allowed held reasons are `Q2_UNSIGNED`, `EF3_ABSENT`, `SCORING_UNAUTHORIZED`, `L8_PREREQUISITE_UNCLEARED`, and `NATIVE_L8_UNDECIDED`.

## CC6 — exact combined-tree construction and identity cascade

Implementation publication first requires Coordinator designation of exact `MAIN_SHA` and final cleared `TOKENIZER_SHA`. Both must be full remote-equal commits. The overlay is frozen in this order:

1. `artifacts/m4_tokenizer_materialization/.gitkeep`
2. `diagnostics/m4_tokenizer_materialization.py`
3. `specs/data/m4_context_format_probe_contract_v1.json`
4. `specs/data/m4_context_format_probe_contract_v1.json.sha256`
5. `specs/data/m4_tokenizer_executable_package_v1.json`
6. `specs/data/m4_tokenizer_executable_package_v1.json.sha256`
7. `specs/data/m4_tokenizer_materialization_blocked_v1.json`
8. `specs/data/m4_tokenizer_materialization_blocked_v1.json.sha256`
9. `specs/data/m4_tokenizer_materialization_fail_v1.json`
10. `specs/data/m4_tokenizer_materialization_fail_v1.json.sha256`
11. `specs/data/m4_tokenizer_materialization_request_v1.json`
12. `specs/data/m4_tokenizer_materialization_request_v1.json.sha256`
13. `specs/data/m4_tokenizer_materialization_result_schema_v1.json`
14. `specs/data/m4_tokenizer_materialization_result_schema_v1.json.sha256`
15. `specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json`
16. `specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json.sha256`
17. `specs/data/m4_tokenizer_materialization_test_contract_v1.json`
18. `specs/data/m4_tokenizer_materialization_test_contract_v1.json.sha256`
19. `specs/data/m4_tokenizer_oci_launch_contract_v1.json`
20. `specs/data/m4_tokenizer_oci_launch_contract_v1.json.sha256`
21. `specs/data/m4_tokenizer_private_custody_record_schema_v1.json`
22. `specs/data/m4_tokenizer_private_custody_record_schema_v1.json.sha256`
23. `specs/data/m4_tokenizer_runtime_unavailable_interpreter_expected_v1.json`
24. `specs/data/m4_tokenizer_runtime_unavailable_interpreter_expected_v1.json.sha256`
25. `specs/data/m4_tokenizer_runtime_unavailable_interpreter_fixture_v1.json`
26. `specs/data/m4_tokenizer_runtime_unavailable_interpreter_fixture_v1.json.sha256`
27. `specs/data/m4_tokenizer_runtime_validation_negative_cases_v1.json`
28. `specs/data/m4_tokenizer_runtime_validation_negative_cases_v1.json.sha256`
29. `specs/data/m4_tokenizer_runtime_validation_negative_expected_v1.json`
30. `specs/data/m4_tokenizer_runtime_validation_negative_expected_v1.json.sha256`
31. `specs/m4_local_tokenizer_materialization_changelog.md`
32. `specs/m4_local_tokenizer_materialization_spec_v1.md`
33. `tests/__init__.py`
34. `tests/run_m4_tokenizer_materialization_tests.py`
35. `tests/test_m4_tokenizer_materialization.py`
36. `tools/testbed/run_m4_tokenizer_topology_smoke_matrix.sh`

No glob, extra path, deletion, rename, or whole-tree merge is permitted. Every source blob and mode must equal `TOKENIZER_SHA`; every non-overlay base path must equal `MAIN_SHA`.

The `.gitattributes` base must end in exactly one LF and contain no tokenizer-overlay heading. Otherwise construction stops. Append these exact ASCII bytes, beginning with one LF and ending with one LF:

```text

# M4 tokenizer overlay
.gitattributes text eol=lf
artifacts/m4_tokenizer_materialization/.gitkeep text eol=lf
diagnostics/m4_tokenizer_materialization.py text eol=lf
specs/data/m4_context_format_probe_contract_v1.json text eol=lf
specs/data/m4_context_format_probe_contract_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_executable_package_v1.json text eol=lf
specs/data/m4_tokenizer_executable_package_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_materialization_blocked_v1.json text eol=lf
specs/data/m4_tokenizer_materialization_blocked_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_materialization_fail_v1.json text eol=lf
specs/data/m4_tokenizer_materialization_fail_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_materialization_request_v1.json text eol=lf
specs/data/m4_tokenizer_materialization_request_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_materialization_result_schema_v1.json text eol=lf
specs/data/m4_tokenizer_materialization_result_schema_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json text eol=lf
specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_materialization_test_contract_v1.json text eol=lf
specs/data/m4_tokenizer_materialization_test_contract_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_oci_launch_contract_v1.json text eol=lf
specs/data/m4_tokenizer_oci_launch_contract_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_private_custody_record_schema_v1.json text eol=lf
specs/data/m4_tokenizer_private_custody_record_schema_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_runtime_unavailable_interpreter_expected_v1.json text eol=lf
specs/data/m4_tokenizer_runtime_unavailable_interpreter_expected_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_runtime_unavailable_interpreter_fixture_v1.json text eol=lf
specs/data/m4_tokenizer_runtime_unavailable_interpreter_fixture_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_runtime_validation_negative_cases_v1.json text eol=lf
specs/data/m4_tokenizer_runtime_validation_negative_cases_v1.json.sha256 text eol=lf
specs/data/m4_tokenizer_runtime_validation_negative_expected_v1.json text eol=lf
specs/data/m4_tokenizer_runtime_validation_negative_expected_v1.json.sha256 text eol=lf
specs/m4_local_tokenizer_materialization_changelog.md text eol=lf
specs/m4_local_tokenizer_materialization_spec_v1.md text eol=lf
tests/__init__.py text eol=lf
tests/run_m4_tokenizer_materialization_tests.py text eol=lf
tests/test_m4_tokenizer_materialization.py text eol=lf
tools/testbed/run_m4_tokenizer_topology_smoke_matrix.sh text eol=lf
```

Before implementation publication the seam filenames are frozen as `src/__init__.py`, `src/m4_post_tokenizer_integration.py`, `src/test_m4_post_tokenizer_integration.py`, and `tests/run_m4_post_tokenizer_integration_tests.py`. Their modes, byte counts, raw SHA-256, and Git blobs must be added to the combined inventory; until those bytes exist, publication is blocked rather than guessed.

The exact topological rebinding cascade is: combined `.gitattributes` → wrapper attribute constants; wrapper plus attributes → executable-package rows; executable package → package sidecar; package/constructor/test/OCI identities → combined integration inventory; implementation module, marker, wrapper, selected tests, contract, fixture, and their sidecars → combined integration inventory; combined inventory → inventory sidecar and integration launch contract; launch contract → launch sidecar and terminal handoff manifest. At each node, recompute the complete raw identity and reject any unlisted changed dependency. Historical artifacts are never rewritten.

## Holds and exit

Q2, EF3, native L8, scientific thresholds, scoring, seeds, qualification, and real-backend selection remain separate. This design performed no implementation, OCI/materializer execution, custody/model/tokenizer access, durable-state mutation, publication, merge, or gate decision.
