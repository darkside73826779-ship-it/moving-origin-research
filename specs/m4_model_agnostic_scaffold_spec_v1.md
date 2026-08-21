# M4 Model-Agnostic Adapter and Scaffold Specification v1

**Date:** 2026-08-21

**Regime:** B

**Status:** `[PROPOSED]`; scaffold specification only; no implementation, model selection, download, training, integration, or execution authority

**Gate served:** M4 model-agnostic adapter/scaffold design following approved Phase A

**Authority:** `coordinator/m4-cuda-ready-cpu-l8-directive@a4d8dc054d3944d3a0efbafeea955b3570f0a272`; approved Phase A ARCHITECT head/result `e5edb1e804cc4a6553507c98140fa9fa49586a0d` / `e7419633f34c7eebadfe3cea33c84aff3883a4aa`; persistent CRITIC CLEAR `0790b4a24a868df84739199f1eab7bb16ebe0609`

## 1. Versioned-law compliance

The binding protocol is quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md:130-135`:

> - **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
> - **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
> - **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.

Relevant laws, quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md:26,28,30,42,54-55`:

> **L7 — Mirror standard (from the introspection literature).** Self-reports about internal state must be calibrated against ground-truth internals AND must beat a peer-observer baseline (a matched model predicting this system from its outputs). *Test:* AUROC ≥ 0.75 and ECE ≤ 0.10 on self-state prediction, with the self-vs-peer margin > 0 at p < .05. No margin over the peer = portrait, not mirror — reported as such. Contamination controls (permuted/empty/shuffled) mandatory.

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

> **L9 — Linear read (I-16, inherited verbatim from the glial project).** Any associative retrieval channel is linear end-to-end from stored code to output injection; no retrieval routes through bounded nonlinear weight perturbation. *Test:* the existing I-16 invariant, unchanged.

> **L14 — Stakes touch everything or nothing.** The homeostatic variables (L8) must be readable by the self-model, affected by memory quality, and predictive targets for the thick present. A stakes module only one component can see is decorative.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

This specification changes no scientific bar, verdict rule, negative label, seed rule, or backend authority. All numeric interface sizes, fixture values, resource ceilings, and scaffold acceptance criteria below are `[PROPOSED]` and cannot gate scoring until Rebecca approves them.

## 2. Scope and selected abstraction

The immediate artifact is a model-neutral protocol and deterministic synthetic scaffold. It names no model family, checkpoint, tokenizer, weight source, or training recipe. A real model is inadmissible until the later qualification gate in §12 `[PROPOSED]`.

The canonical adapter ID is `m4-model-adapter-v1`. An implementation must expose exactly these methods in order `[PROPOSED]`:

1. `describe() -> canonical manifest bytes`;
2. `initialize(manifest_bytes, dependency_manifest_bytes) -> initialization receipt`;
3. `reset_episode(reset_request_bytes) -> reset receipt`;
4. `step(step_request_bytes) -> step response bytes`;
5. `snapshot(snapshot_request_bytes) -> checkpoint metadata bytes`;
6. `close() -> close receipt`.

Calling out of order returns `ADAPTER_LIFECYCLE_VIOLATION`; no implicit initialize, reset, retry, fallback, or state carryover is permitted `[PROPOSED]`.

## 3. Manifest and declared dimensions

Every adapter validates against `specs/data/m4_model_adapter_manifest_schema_v1.json`. It declares role, scientific arm, implementation identity, parameter count, model/checkpoint/tokenizer identities, license, dimensions, dtypes, device policy, hook support, checkpoint support, and resource limits `[PROPOSED]`.

The pair validator walks `manifest_pair.equality_fields` in stored order and requires JSON-value identity at every pointer. It then requires every `required_difference_fields` pointer to differ, requires both training-instance digests to be non-null, and rejects any additional candidate/peer manifest difference except role, scientific arm, and training-instance digest. The executable fixture supplies the schema-valid positive pair and exact pair digests `[OP-Entry 76] [PROPOSED]`.

The scaffold profile is exactly `SYNTHETIC_STUB_V1` with public width `4`, privileged width `4`, internal width `4`, self-state target width `2`, behavioral-output width `4`, one confidence scalar, one abstention boolean, one homeostatic value, and one homeostatic action `[PROPOSED]`. These sizes test protocol topology only and do not constrain a later real model; a later model must declare fixed positive sizes and pass the same semantic validators before selection `[PROPOSED]`.

Real-model manifest fields remain null and status `UNBOUND_MODEL_SELECTION_REQUIRED`. A manifest with a real brand, repository, checkpoint, tokenizer, weight digest, or license identity before the later Rebecca gate is rejected as `PREMATURE_MODEL_BINDING` `[PROPOSED]`.

## 4. Candidate/peer privileged-state boundary

Requests validate against `m4_model_adapter_request_schema_v1.json`. The ordered input is public history, then privileged packet, then perturbation declaration `[PROPOSED]`.

- `candidate`: privileged packet is required, `access_granted=true`, and packet role is `MOVING_ORIGIN_STATE`.
- `peer`: privileged packet values must be absent, `access_granted=false`, and a redaction receipt binds the public request digest. The peer receives candidate behavioral outputs, append-log events, external events, and query history only `[LAW-L7] [BAR-Entry 11]`.
- candidate and peer manifests must later have identical architecture fingerprint, parameter count, initialization digest, training-data digest, optimizer schedule digest, and declared dimensions; only privileged access and the resulting independently trained instance may differ `[BAR-Entry 11]`.
- Entry 76 Ruling 5 additionally requires identical confidence-calibration, evaluation-data, ECE-definition, binning-definition, and paired-training-contract digests. `training_instance_sha256` must differ while every preceding equality field matches `[OP-Entry 76]`.
- No peer request may carry an internal representation, self-report, confidence payload, homeostatic hidden value, gradients, device pointer, checkpoint tensor, or perturbation realization. The mandatory semantic-probe sentinel is `candidate_confidence_present=false,candidate_confidence=null`; changing either to convey a value is `PRIVILEGED_STATE_LEAK` `[PROPOSED]`.

The moving-origin packet is ordered as `origin_ordinal, origin_age, internal_state_vector, memory_quality, homeostatic_value, prior_calibration_error` and includes its canonical SHA-256 `[PROPOSED]`. Retrieval selection is fixed chronological append-log truncation declared in the request; learned/nonlinear retrieval, reranking, embedding search, or adaptive retrieval is `L9_RETRIEVAL_FENCE_VIOLATION` `[LAW-L9]`.

## 5. Outputs and semantic invariants

Responses validate against `m4_model_adapter_response_schema_v1.json` and contain, in order `[PROPOSED]`:

- behavioral output vector;
- moving-origin internal representation vector;
- self-state probabilities, each finite and in `[0,1]` `[PROPOSED]`;
- confidence, finite and in `[0,1]` `[PROPOSED]`;
- pre-abstention score and abstention decision;
- homeostatic value, target, regulation error, and action;
- hook receipts;
- resource report;
- state-before and state-after digests.

Every lifecycle method returns `m4_model_adapter_operation_result_schema_v1.json`. Validation order is fixed: JSON decoding and input structural-schema validation; input digest validation; manifest/request cross-validation; privilege/retrieval/hook/mode/checkpoint semantic validation; adapter operation; internal-output semantic validation (finite values, dimensions, resource envelope, CUDA-host synchronization); response serialization; response structural-schema validation; determinism/publication validation. The first failure in that order is the sole emitted code. Fields intentionally admitted structurally for a negative semantic test remain forbidden by the semantic validator. A nonfinite injection exists only at the tagged pre-serialization internal-output boundary and is represented in the fixture by its IEEE-754 bit pattern, never as invalid JSON `[PROPOSED]`.

`regulation_error` equals `abs(homeostatic_value-homeostatic_target)` exactly in binary64 `[PROPOSED]`. Candidate confidence must be generated from the candidate internal-state path; peer confidence uses the same method signature but only its public observation path `[BAR-Entry 11]`. The scaffold verifies routing, not scientific performance; no stub output may be cited as M4 evidence `[PROPOSED]`.

## 6. Perturbation hooks

Every compatible real adapter must expose two distinct post-normalization, pre-head hooks `[PROPOSED]`:

1. `SELF_MODEL_REPRESENTATION`: candidate-only internal representation hook used for L8 dose perturbation;
2. `NON_SELF_PROXIMAL_COMPONENT`: a declared non-self component hook used for the standardized specificity leg under Entry 76 Ruling 3 `[OP-Entry 76]`.

Each hook receipt records hook ID, tensor shape/dtype, pre/post raw digest, perturbation identity, dose ordinal, and standardized proximal-effect summary `[PROPOSED]`. A hook applied at an undeclared location, before normalization, after output generation, to the peer's prohibited private channel, or without a receipt is `PERTURBATION_BOUNDARY_MISMATCH` `[PROPOSED]`. Hook payloads are supplied by the harness; adapters never derive scoring RNG or select dose magnitude `[PROPOSED]`.

## 7. Homeostatic interface

At least one homeostatic variable is required by law `[LAW-L8]`. The adapter interface declares one or more named variables with binary64 current value, numeric target or closed bound, regulation error, read permission for the self-model, memory-quality dependency ID, thick-present prediction target ID, and action channel ID `[LAW-L8] [LAW-L14] [PROPOSED]`.

The scaffold variable is `stub_reserve`, target `0.5`, domain `[0,1]`, and regulation error `abs(value-0.5)` `[PROPOSED]`. It exists only to test interface propagation. A later real variable requires separate ARCHITECT specification and persistent CRITIC review; reusing `stub_reserve` as a scientific variable is `STUB_AS_SCIENCE_PROHIBITED` `[PROPOSED]`.

## 8. Synthetic adapters

`specs/data/m4_model_scaffold_executable_fixture_v1.json` fixes complete schema-valid candidate/peer manifests and requests, dependency/checkpoint/publication bases, six lifecycle results, nine canonical response constructors and SHA-256 values, and seventeen typed mutations with canonical failure-result SHA-256 values. Its stored adapter order is `[PROPOSED]`:

1. `candidate`: reads the privileged vector;
2. `peer`: reads public history only;
3. `oracle`: emits ground-truth self-state and correctness;
4. `empty`: emits neutral probabilities/confidence and no private state;
5. `permuted`: applies the committed privileged-index permutation;
6. `shuffled`: applies the committed public-history permutation;
7. `naive`: uses the last public observation only;
8. `frozen`: repeats the first complete response for the episode;
9. `specificity`: candidate path with perturbation only at `NON_SELF_PROXIMAL_COMPONENT`.

Scientific published labels remain exactly `candidate,empty,permuted,shuffled,oracle,naive,frozen,specificity`; `peer` is the L7 matched comparator and is never renamed into a control arm `[LAW-L7] [LAW-L18] [PROPOSED]`.

Stub functions are arithmetic specified by the fixture, use no learned parameter, network, filesystem, clock, entropy source, or GPU kernel, and must produce canonical byte-identical outputs on CPU and CUDA-host orchestration `[PROPOSED]`.

## 9. CUDA, host custody, and resource reporting

CUDA is permitted only for model/harness computation. Every device output is synchronized, copied into a new host allocation, normalized to declared little-endian C-contiguous dtype/shape, checked finite/range-valid, hashed, frozen, and then handed to the harness `[PROPOSED]`. Device pointers, DLPack capsules, unified memory, live pinned views, and in-flight buffers cannot cross the custody boundary `[PROPOSED]`.

Each response reports device class, compute capability, runtime/dependency-manifest digest, allocated/reserved/peak bytes, host-transfer bytes, stream/event ordinals, synchronization completion, and deterministic-mode receipt `[PROPOSED]`. Machine-unique identifiers, hostnames, serial numbers, usernames, and environment dumps are prohibited from public artifacts `[PROPOSED]`.

The scaffold must run with `CPU_STUB` and `CUDA_STUB_HOST_ORCHESTRATION`; the latter may allocate only fixture tensors and cannot invoke a real model `[PROPOSED]`. Resource-limit violation is `RESOURCE_ENVELOPE_EXCEEDED`, never automatic model fallback `[PROPOSED]`.

## 10. Determinism, checkpoint metadata, and publication

Scaffold adapters are stateless except `frozen`, whose first-response cache is reset only by `reset_episode`. Two fresh-process runs over the fixture sequence must yield byte-identical canonical responses and identical state digests; O-14 prohibits a third run after failure and O-15 keeps both runs diagnostic-only `[PROPOSED]`.

Checkpoint metadata schema records adapter manifest digest, implementation SHA, attempt ID, training status, step, data/schedule/initialization digests, candidate/peer parity digest, tensor-index digest, and parent checkpoint digest `[PROPOSED]`. For the scaffold, `training_status=NOT_APPLICABLE_STUB`, step `0`, and tensor index is empty `[PROPOSED]`. Checkpoint files from a future real model are forbidden until the later gate.

Canonical JSON is RFC 8785 UTF-8 without BOM plus one LF; sidecars are lowercase SHA-256, two spaces, basename, LF. Publication uses validated temp JSON, fsync, temp sidecar, previous-pair preservation, two atomic replacements, and restoration plus `.incomplete` retention after interruption `[PROPOSED]`.

## 11. Scaffold verification and failure injection

TASK BUILDER, only after a future exact release, must implement the scaffold and collect each stored row in `m4_model_scaffold_executable_fixture_v1.json` exactly once `[PROPOSED]`. Required tests are `[PROPOSED]`:

- strict schema accept and unknown-field reject;
- lifecycle order and episode reset;
- exact candidate/private and peer/redacted routing;
- all nine adapters in fixed order;
- exact stub output fields and canonical digests;
- fresh-process repeatability;
- self-model versus non-self hook separation;
- homeostatic propagation and exact error identity;
- CUDA-to-host custody record;
- resource-limit failure;
- incomplete output, corruption/digest mismatch, nondeterminism, configuration mismatch, crash/recovery, privileged leak, undeclared hook, learned-retrieval request, premature real-model binding, and atomic-publication interruption.

Every injected failure has one expected code fixed by the fixture. Ordinary scientific predicate failures are not apparatus failures. A scaffold failure preserves artifacts, blocks descendants, and, under O-14, receives no retry/replacement run `[PROPOSED]`.

`specs/data/m4_model_scaffold_task_boundary_v1.json` is the exact machine-readable future implementation boundary. It is presently `HELD_PENDING_CRITIC_AND_REBECCA`; its allowed operations do not take effect unless Rebecca releases that exact artifact `[PROPOSED]`.

## 12. Later brand-neutral model qualification

After scaffold implementation, persistent CRITIC implementation CLEAR, and Rebecca acceptance, ARCHITECT may begin a separately authorized qualification design. It compares candidates only against these brand-neutral mandatory capabilities `[PROPOSED]`:

1. local reproducibility with immutable source/checkpoint/tokenizer/license/dependency digests;
2. exact adapter-schema compliance without semantic translation;
3. fixed chronological retrieval compatible with the L9 fence;
4. declared moving-origin representation and both perturbation hooks;
5. candidate/peer architecture and parameter parity with channel-only access difference;
6. deterministic initialization/training feasibility and separately custodied checkpoints;
7. full-precision confidence/pre-abstention/self-state/homeostatic outputs;
8. candidate-blind calibration and protected-seed exclusion;
9. CUDA resource feasibility under a predeclared local envelope with no backend fallback;
10. license permitting local use, derived checkpoints, evidence retention, and public manifest disclosure.

Qualification stages are paper preflight, license/provenance review, resource estimate, stub-conformance plan, and ARCHITECT recommendation. No download or execution occurs during qualification unless Rebecca separately authorizes it `[PROPOSED]`. A missing immutable identity, inaccessible internal state/hook, learned retrieval requirement, unequal peer, unverifiable license, unverifiable data provenance, cloud-only dependency, hidden API, resource overflow, nondeterministic-only training path, or required scientific translation is a STOP `[PROPOSED]`.

## 13. Exact future gate sequence

1. This ARCHITECT specification → persistent fresh-context CRITIC → WORKFLOW COORDINATOR → Rebecca.
2. Rebecca may release TASK BUILDER for scaffold-with-stubs implementation only.
3. Persistent CRITIC reviews implementation; Rebecca accepts or returns it.
4. Coordinator routes a new model-qualification handoff to ARCHITECT.
5. ARCHITECT commits a brand-neutral comparison and one recommended exact model/checkpoint package.
6. Persistent CRITIC reviews; Rebecca alone may authorize download.
7. Download custody records raw digests without loading weights; CRITIC verifies; Rebecca alone may authorize binding/training.
8. Matched candidate/peer training or fine-tuning occurs under one pre-registered attempt, with no score-seed access and no rerun on failure.
9. Persistent CRITIC reviews training and integration evidence; Rebecca alone may release O-15 compatibility diagnostics.
10. Exact final `gofast` reconciliation must separately clear before any M4 implementation can leave `PROVISIONAL_BLOCKED` `[PROPOSED]`.

## 14. Current STOPs and prohibitions

The final parallel-CPU L8 routing/result/review/dependency/config/symbol identities remain unavailable in the approved binding manifest. This is `M4_CPU_L8_BINDING_UNRECONCILED` and remains a STOP `[PROPOSED]`.

No real model identity may be populated now. No TASK BUILDER release, scaffold implementation, model selection, download, training/fine-tuning, real-model integration, compatibility/diagnostic/scoring execution, protected/courier seed access or exposure, rerun, native-CUDA L8 adoption, `GO!` use, fallback, state/provenance mutation, merge, or gate decision is authorized. `gofast` remains the sole authoritative L8 evaluator; `go faster` remains shelved. Rebecca remains sole gate and merge authority.
