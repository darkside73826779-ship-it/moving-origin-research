# M4 Harness Contract v1.1 — CUDA-Ready Harness with Authoritative Parallel-CPU L8

**Date:** 2026-08-21

**Regime:** B

**Status:** Revised Phase A contract-first design `[PROPOSED]`; no implementation or execution authority

**Gate served:** CUDA-ready M4 harness design with the parallel-CPU L8 evaluator as the sole current authoritative L8 backend

**Base:** `7d6e499cb8a0cf9859cc05b37ec4e97767c4839e`

**Directive:** `coordinator/m4-harness-architect-intake@b32992e7162e129312d2b2493ddbea18b234db81`

**Revised directive:** `coordinator/m4-cuda-ready-cpu-l8-directive@d821a5c534f1c4547b99a2fb0079266497ddd537`

## 1. Versioned-law compliance

The binding protocol is quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md:130-135`:

> - **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
> - **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
> - **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.
> - **P4 — Regime dating.** Every new artifact states its date and regime in its header. Acts are judged only against their own regime's text; later text is never applied backward.
> - **P5 — Deviation memorialization.** Any deviation from `[LAW]` text — however sensible, however disclosed — is inoperative for scoring until Rebecca has signed a waiver or amendment recorded in the v2 amendment log. Disclosure in a spec is necessary but not sufficient.
> - **P6 — Provenance citation check.** Any claim of the form "Entry n said X" must be verified against the entry's actual text before commit.

Relevant laws, quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28,54-55`:

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

This contract changes no locked bar, predicate, negative label, seed rule, or scientific arm. L8 uses beta-star `>=0.2`, rho `>=0.8`, and at least three doses `[BAR-Entry 11]`; five scoring seeds and the all-seeds-direction rule are `[BAR-Entry 11.3]`; the standardized proximal-component specificity design is `[OP-Entry 76 Ruling 3]`. M4 continues to use exactly the scientific arms `candidate, empty, permuted, shuffled, oracle, naive, frozen, specificity` in that order `[LAW-L18] [LAW-L8]`; the approved backend's `combo` and `null_control` names remain backend-parity identities and are never substituted for or published as M4 negative labels `[PROPOSED]`.

## 2. Authority, shelved native CUDA, and immutable identities

The binding manifest must validate against `specs/data/m4_l8_binding_manifest_schema_v1.json`; schema-only validity never overrides its fail-closed provisional status `[PROPOSED]`.

The stable revised Phase A authority set is `[PROPOSED]`:

1. M4 specification `specs/m4_specification.md` and task specification `specs/m4_task_spec.md` at base `7d6e499cb8a0cf9859cc05b37ec4e97767c4839e`.
2. Rebecca's CPU-L8 redirection `d821a5c534f1c4547b99a2fb0079266497ddd537` and codename directive at coordinator head `4de2ace8dfba59dd5cd6698bf90bb26307b0194f`.
3. Parallel-CPU semantic baseline `b1397498ca369067e956479e6c2bd6b0793c3e89` and completed CPU evidence `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3`. These identify the reviewed lineage, not the still-pending final implementation reconciliation.
4. Approved L8 v1.5/v1.4 artifacts remain applicable evidence for estimator, tie, calibration, and failure semantics only where they do not make native CUDA an M4 dependency.

`specs/data/m4_l8_binding_manifest_v1.json` is the sole adapter-binding authority. Its only authorized backend is `PARALLEL_CPU_L8_EXACT_SHA`; `NATIVE_CUDA_L8` is listed as `SHELVED/INOPERATIVE` and cannot satisfy the binding `[PROPOSED]`. In revised Phase A the manifest is `PROVISIONAL_BLOCKED` and all final parallel-CPU implementation/review fields are null. Any adapter construction is then `INSTRUMENT_FAILURE/M4_CPU_L8_BINDING_UNRECONCILED` `[PROPOSED]`. Exact-SHA CPU-L8 reconciliation replaces the former native-CUDA Phase B dependency: after the final approved parallel-CPU implementation and independent review exist, ARCHITECT records the exact routing head, result, review, code-tree/dependency/config digests, adapter symbols, and implementation-owned parallelism; fresh-context CRITIC clears and Rebecca approves. The harness rejects branch-name, ancestry-only, dirty-tree, version-range, duck-typed, translated, shelved-native-CUDA, or fallback identities `[PROPOSED]`.

Human-facing aliases are adjacent labels only: `gofast` means `PARALLEL_CPU_L8_EXACT_SHA`, `GO!` means the serial-CPU evaluator, and `go faster` means the shelved native-CUDA evaluator. Only `gofast`'s canonical backend is authorized here; aliases never replace machine identifiers, SHAs, digests, scientific labels, negative classifications, or failure enums `[PROPOSED]`.

## 3. Harness architecture

The harness has seven layers in fixed order `[PROPOSED]`:

1. `preflight`: validate all raw sidecars, schemas, authority SHAs, clean implementation tree, dependency provenance, mode authorization, seed-custody token, and final parallel-CPU binding reconciliation.
2. `model_executor`: run the configured AI model on `CUDA_AI_MODEL` or `CPU_AI_MODEL`; this layer never evaluates L8.
3. `device_to_host`: for CUDA output, wait for the producing event, perform a blocking copy, synchronize, normalize and validate host dtype/layout, hash the completed host bytes, and freeze them; CPU-model output enters the same host validation path.
4. `producer_cpu`: construct host-side M4 requests, homeostatic targets, calibrated perturbations, L18 arms, oracle correctness, primitive tapes, and calibrations without changing model output bytes.
5. `l8_adapter_v1_parallel_cpu`: receive only fully synchronized immutable host buffers and invoke only the exact reconciled parallel-CPU evaluator.
6. `law_aggregator_cpu`: apply M4 per-seed/all-seed, L18, FWFP, borderline-reporting, and negative-label rules without altering adapter outputs.
7. `publisher`: validate and atomically publish canonical result/evidence pairs.

The adapter is not a scoring authority. It returns measurements and predicates; the CPU law aggregator alone assigns M4 `PASS`, `KILL`, or `INSTRUMENT_FAILURE` under the approved M4 specification `[PROPOSED]`.

## 4. Exact adapter interface

### 4.1 Runtime call

The M4-side parallel-CPU adapter call is exactly:

`evaluate_l8_parallel_cpu_v1(request_json_bytes, p_true_f64_host, correct_bool_host, xi_f64_host, xi_l_f64_host) -> response_json_bytes` `[PROPOSED]`.

The estimator-only call is exactly `evaluate_l8_parallel_cpu_estimator_v1(estimator_request_json_bytes) -> response_json_bytes`; its input validates against `m4_l8_estimator_request_schema_v1.json` and embeds the complete finite `d_seed` matrix plus the SHA-256 of RFC-8785 canonical `d_seed` bytes `[PROPOSED]`. It never receives or fabricates primitive buffers.

JSON bytes validate against `m4_l8_adapter_request_schema_v1.json`, declare `l8_backend=PARALLEL_CPU_L8_EXACT_SHA` and `buffer_location=HOST`, and are RFC 8785 canonical UTF-8 without BOM. Array buffers are immutable host allocations, C-contiguous, little-endian; float buffers are IEEE-754 binary64 and the boolean buffer is one byte per element with values zero or one `[PROPOSED]`. Each has shape `(dose_count, windows_per_dose, queries_per_window)` and axis order `dose,window,query`. Buffer byte lengths equal shape product times element width; lowercase raw SHA-256 values match the request. Device pointers, managed/shared GPU memory, nonfinite float input, nonzero padding, mutation, aliasing, shape/digest mismatch, or unknown fields fail before parallel-CPU dispatch `[PROPOSED]`.

The approved four-dose realization uses dose indices `[0,1,2,3]` `[PROPOSED]`; this does not replace the locked at-least-three-dose bar `[BAR-Entry 11]`. CPU seed derivation, NumPy draw order, positive-zero dose-zero `xi_l`, separate candidate/specificity tapes, controller reset per dose, and identity restoration follow approved L8 v1.5/v1.4 exactly `[PROPOSED]`.

The response validates against `m4_l8_adapter_response_schema_v1.json`. It contains complete ordered window deviations `d_seed`, dose summaries, beta-star, rho, defined mask, beta/rho/complete predicates, coverage-index digest, and apparatus status. No rounding, aggregation across seeds, verdict naming, or omitted failed predicate is permitted `[PROPOSED]`.

### 4.2 Real estimator semantics

For each seed, `d_seed` has shape `(4,N_w)` `[PROPOSED]`. Dose summary is the binary64 arithmetic mean over windows. Beta-star is the population-covariance slope of dose summaries on dose indices divided by pooled within-dose sample standard deviation with `4*(N_w-1)` degrees of freedom, using the controlling CPU operation order `[PROPOSED]`. Zero pooled variance is an apparatus fault only when an independent apparatus check proves it; otherwise the response records `beta_star=null`, `beta_defined=false`, `statistical_failure_code=ZERO_POOLED_VARIANCE`, `beta_predicate=false`, `complete_predicate=false`, `apparatus_status=VALID`, and `failure_code=null`; the seed remains included and its M4 per-law status is `KILL` `[PROPOSED]`. The published L8 seed record uses the identical nullable beta, defined flag, statistical failure code, false predicates, and non-apparatus representation. No validator may convert this case to `INSTRUMENT_FAILURE`.

Rho uses ascending one-based midranks and binary64 Pearson correlation against dose ranks `(1,2,3,4)` `[PROPOSED]`. Exact finite ties receive the mean occupied rank. Undefined rho fails its predicate without becoming apparatus failure absent independent proof. Rho passes iff `rho>=0.8 OR abs(rho-0.8)<=1e-12` `[BAR-Entry 11] [PROPOSED]`; beta passes iff `beta_star>=0.2` `[BAR-Entry 11]`. The five-seed complete L8 verdict fails when any seed fails beta, has undefined rho, or fails rho `[BAR-Entry 11.3]`.

Coverage ordering is `(descending c_prime, ascending zero-based query_index)` with exact binary64 ties; the first `max(1,ceil(c_min*W))` indices form the floor and later indices enter only when `c_prime>tau` `[PROPOSED]`. This is the Rebecca-approved v1.5 B11 rule. The adapter may not use a different unstable ordering or any GPU `topk` path `[PROPOSED]`.

### 4.3 M4 arm/backend mapping

Arm construction and scientific identity remain M4 producer responsibilities. Candidate and severity-matched specificity primitive tapes cross the host boundary and invoke the exact reconciled parallel-CPU evaluator. Its internal arm identities, if required, are bound during CPU-L8 exact-SHA reconciliation and may never replace published M4 labels `[PROPOSED]`.

All L18 arms are constructed by the M4 producer and evaluated by the same **real parallel-CPU estimator semantics** through `PRIMITIVE_TAPE` where a primitive realization exists or `ESTIMATOR_ONLY` for committed `d_seed` profiles `[PROPOSED]`. CPU-L8 reconciliation must bind both operations to reviewed symbols or STOP. No empty/permuted/shuffled/oracle/naive/frozen arm may be renamed to a backend identity, and no positive claim may omit any arm `[LAW-L18]`.

## 5. CUDA AI-model / host-transfer / parallel-CPU L8 boundary

The AI-model executor may be `CUDA_AI_MODEL` or `CPU_AI_MODEL`, selected before model initialization. It owns model forward computation only. CUDA model tensors never enter L8. For each declared model output, the harness waits for the producing stream/event, performs a blocking device-to-host copy (`non_blocking=false`) into a newly allocated host tensor/array with the target dtype, synchronizes the device, converts to little-endian C-contiguous NumPy-compatible bytes, verifies finite/range/shape invariants, hashes raw bytes, and only then constructs an L8 request `[PROPOSED]`. No DLPack/device pointer, asynchronous host view, unified memory, pinned buffer still owned by an in-flight transfer, or mutable model tensor crosses the boundary.

The harness CPU side exclusively owns: seed custody/derivation; primitive-tape and L18-arm construction; geometry-aware calibration; standardized specificity calibration; M4 tolerance/FWFP calibration; host-transfer validation; identity/order restoration; aggregation; negative labels; canonicalization; digests; publication; and failure routing `[PROPOSED]`. The reconciled parallel-CPU L8 implementation exclusively owns its evaluator/estimator computation and internal worker scheduling. The harness calls it once per declared request and never shards, pads, retries, or changes its worker policy.

If `CUDA_AI_MODEL` is configured, CUDA unavailability, allocation/transfer/synchronization failure, dependency mismatch, or nondeterministic exported bytes is `INSTRUMENT_FAILURE`; there is no silent CPU-model fallback `[PROPOSED]`. This does not change L8 authority: L8 remains parallel CPU whether model execution is CUDA or CPU. Any request for `NATIVE_CUDA_L8`, any GPU L8 dispatch, or any unbound L8 implementation is `INSTRUMENT_FAILURE/UNAPPROVED_L8_BACKEND`, with no fallback. GPU and CPU resource pools are separately bounded; the L8 process receives only completed host buffers, and CUDA memory may be released only after transfer synchronization and host digest verification.

`specs/data/m4_cuda_ai_cpu_l8_boundary_schema_v1.json` is the exact boundary-record schema `[PROPOSED]`. One record is emitted per transfer in request order. It binds model backend/device identity, producing stream/event ordinal, synchronization status, source/target dtype and shape, host byte length/digest, L8 backend, request digest, and custody status. Boundary records are canonical evidence inputs; they contain no protected seed value.

## 6. O-15 compatibility gate

Before any M4 implementation release, TASK BUILDER must execute exactly one candidate-blind compatibility suite in `O-15-diagnostic-only` mode after CPU-L8 exact-SHA reconciliation and Rebecca authorization `[PROPOSED]`. This is not scoring and consumes no protected/courier seed.

The suite uses `specs/data/m4_l8_compatibility_fixture_v1.json`, `specs/data/m4_harness_executable_fixtures_v1.json`, and `specs/data/m4_l8_compatibility_expected_responses_v1.json` and performs, in fixed order `[PROPOSED]`:

1. seven rho cases and four complete-verdict cases copied from approved known-good fixture raw digest `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7`;
2. the two B11 cutoff-straddling fixtures copied from approved tie fixture at design result `a25398e599622c09d130b597b7bc83ce62a966d5`;
3. one request-schema rejection, one host-buffer digest mismatch, one CPU-L8 dependency mismatch, one configured CUDA-AI-model-unavailable injection, one nondeterministic-repeat injection, and one shelved-native-CUDA-L8 request injection.

Every positive row must match all literal expected fields; beta/rho absolute difference may be at most `1e-12` while predicate, undefined-mask, coverage order, and canonical response bytes must be exact `[PROPOSED]`. Run zero and a fresh-process run one must yield byte-identical canonical response arrays; no third run is permitted `[PROPOSED]`. Any failure yields `INSTRUMENT_FAILURE`, preserves the diagnostic, and blocks M4 release without retry or replacement `[PROPOSED]`.

The report validates against `m4_l8_compatibility_report_schema_v1.json`, has exactly the thirteen ordered rows and six ordered failure injections committed in `m4_l8_compatibility_expected_report_v1.json`, publishes at `diagnostics/m4_l8_compatibility_report.json` plus sidecar, and contains no candidate observations or protected seed identity `[PROPOSED]`. Each row's observed object is RFC-8785 canonicalized and its raw SHA-256 must equal the row's committed expected-response digest. Before reconciliation, the expected-report envelope and primitive fixture are templates and do not validate as runtime artifacts. Each source artifact contains exactly one occurrence of each placeholder it declares. Reconciliation replaces `IMPLEMENTATION_COMMIT_PLACEHOLDER` in both artifacts with the same final implementation SHA, replaces `IMPLEMENTATION_REVIEW_COMMIT_PLACEHOLDER` once with the final review SHA, constructs the report, hashes its RFC-8785 bytes plus LF, and replaces `EXPECTED_REPORT_DIGEST_PLACEHOLDER` once with that lowercase digest. Replacement occurs on parsed string values, never global byte substitution; each token must be the entire value at its named field. Missing, duplicate, malformed, or residual tokens are `INSTRUMENT_FAILURE/CONFIGURATION_MISMATCH`. The committed pre-reconciliation test vector is diagnostic only and proves the constructor still yields 11,483 bytes and digest `1d72ec9423306ae4c022a0f6ee4afb25fc2651d2cdce7fc292baecf5733bca3d` `[PROPOSED]`.

## 7. Harness configuration, result, custody, and failure

Runtime configuration validates against `m4_harness_config_schema_v1.json`. Its sole source is `specs/data/m4_harness_config_template_v1.json`; its raw template digest is fixed by the adjacent sidecar `[PROPOSED]`. Materialization replaces each exact placeholder token once: `IMPLEMENTATION_COMMIT_PLACEHOLDER`, `RESULT_DIGEST_PLACEHOLDER`, and `DEPENDENCY_DIGEST_PLACEHOLDER`. No other byte/value/order changes. Fixed fields declare `model_execution_backend=CUDA_AI_MODEL`, `l8_backend=PARALLEL_CPU_L8_EXACT_SHA`, blocking synchronized host export, and no fallback. The resulting object is RFC-8785 canonicalized; `config_sha256` hashes those canonical bytes `[PROPOSED]`. A missing, duplicate, malformed, or extra placeholder; unknown/duplicate key; NaN/Infinity; unapproved identity; absent sidecar; or schema drift fails before model/RNG construction `[PROPOSED]`.

In that schema, `m4_spec_sha` and `m4_task_spec_sha` are full Git commit identities, not blob hashes; Phase A requires both to equal `7d6e499cb8a0cf9859cc05b37ec4e97767c4839e`, and any later controlling-spec amendment requires a fresh ARCHITECT/CRITIC/Rebecca reconciliation `[PROPOSED]`. Raw file digests are recorded in the handoff artifact inventory rather than substituted for these commit fields.

Top-level M4 results use `m4_harness_result_schema_v1.json`. Law order is `L7,L8,L10,L14,L18`; each law record points to a separately validated `m4_law_artifact_schema_v1.json` canonical artifact and raw sidecar. The schema fixes field shapes and vocabularies; the mandatory semantic validator contract, complete schema-valid L8/L14/L18 mutation bases, and all positive/negative identities are committed in `m4_law_identity_mutation_bases_v1.json` and `m4_law_identity_validation_fixtures_v1.json` `[PROPOSED]`. Each test deep-copies its declared base and applies exactly one mutation. Schema validation runs first: the four removals violate fixed `minItems` and deterministically return `INSTRUMENT_FAILURE/SCHEMA_DRIFT` at their committed array pointer; the identity validator does not run. Schema-valid duplication and reorder cases then invoke `validate_m4_law_identities_v1`, which compares without sorting: L8 arms exactly `candidate,empty,permuted,shuffled,oracle,naive,frozen,specificity`; every L8 arm's seeds exactly `0,1,2,3,4`; L14 couplings exactly `self_model_readable,memory_quality,thick_present_target`; and L18 controls exactly the law-major Cartesian order `L7,L8,L10,L14`, each with arms `empty,permuted,shuffled,oracle,naive,frozen`. It stops at the first mismatch and returns `INSTRUMENT_FAILURE/LAW_IDENTITY_ORDER_MISMATCH` with the fixture's exact pointer/expected/observed object. No sorting, repair, alias, deduplication, or negative omission is permitted `[PROPOSED]`. Status vocabulary is exactly `PASS,KILL,INSTRUMENT_FAILURE,NOT_RUN` `[PROPOSED]`; existing negative names are never changed. `NOT_RUN` is permitted only after an earlier independently recorded apparatus failure and never converts to PASS/KILL `[PROPOSED]`.

O-15 publication paths are exactly `diagnostics/m4_harness/result.json`, `diagnostics/m4_harness/law_l7.json`, `law_l8.json`, `law_l10.json`, `law_l14.json`, and `law_l18.json`, each with adjacent `.sha256` `[PROPOSED]`. Scoring paths are exactly the same basenames under `runs/m4_scoring/` `[PROPOSED]`. A pre-existing complete scoring pair is a STOP; it is never overwritten or used to justify a rerun `[PROPOSED]`. Temporary, previous, and incomplete suffix behavior follows the atomic-pair rule below.

The scoring gate object records exactly the five retained gates in M4 task specification §1.3: L3 fresh-seed resolution `[BAR-Entry 72]`, FWFP closure `[BAR-Entry 43]`, CRITIC implementation review, Rebecca tolerance-calibration sign-off, and Rebecca courier-channel scoring authorization. Scoring mode is rejected unless all five are true `[PROPOSED]`.

Failure stage is exactly `preflight,model_executor,device_to_host,producer_cpu,l8_adapter_parallel_cpu,estimator,law_aggregator,compatibility,custody,publisher` and message code is exactly one enum in the result schema `[PROPOSED]`. Ordinary per-seed predicate failures are KILL evidence, never apparatus failure. Apparatus failure requires an independent configuration, digest, dependency, finite-input, process, CUDA-model, transfer/synchronization, CPU-L8 binding, nondeterminism, or publication check `[PROPOSED]`.

JSON is RFC 8785 canonical UTF-8 without BOM plus exactly one LF. Sidecars contain lowercase SHA-256, two spaces, basename, LF. Publication uses temp JSON fsync, validation, digest, temp-sidecar fsync, previous-valid-pair preservation, two atomic replacements, and restoration/`.incomplete` retention on interruption `[PROPOSED]`.

## 8. Implementation order and fixed tests

Implementation is forbidden until parallel-CPU L8 exact-SHA reconciliation is complete. After release, order is `[PROPOSED]`:

1. schemas, strict parser, canonicalizer, sidecar and atomic-pair utilities;
2. binding validator and dependency/source-policy preflight;
3. CPU real-estimator reference and literal fixtures;
4. CUDA/CPU AI-model executor and synchronized host-transfer boundary;
5. versioned parallel-CPU L8 adapter with no fallback;
6. CPU producer and arm constructors;
7. aggregator/result publisher;
8. failure injection and fresh-process repeatability;
9. O-15 compatibility suite;
10. fresh-context CRITIC implementation review;
11. Rebecca implementation release.

`specs/data/m4_harness_executability_matrix_v1.json` fixes every required test ID, committed fixture path/case ID, literal mutation, expected enum/object/digest, and failure. `specs/data/m4_harness_executable_fixtures_v1.json` includes the complete primitive-tape request plus literal base64 buffer bytes and raw digests; no constructor input is external. Every row must collect exactly once and pass. Semantic validators must also reject cross-field inconsistencies that JSON Schema cannot express `[PROPOSED]`.

## 9. Parallel-CPU L8 exact-SHA reconciliation

Reconciliation begins only after a formal handoff supplies the final approved parallel-CPU L8 routing head, exact implementation result, independent implementation-review SHA/artifact, dependency manifest and sidecar, configuration schema, public adapter symbols, tests, worker-policy ownership, and evidence digests `[PROPOSED]`. ARCHITECT checks out that exact head in isolation and records for every provisional binding: CPU symbol/path, signature, host dtype/shape/order, error behavior, dependency identity, parallelism ownership, result-field mapping, and fixture result. No native-CUDA L8 artifact can satisfy a field `[PROPOSED]`.

Any missing CPU symbol, changed field, new translation, changed dependency, changed tie/RNG/calibration/result semantics, worker-policy conflict, device-buffer requirement, or inability to support `ESTIMATOR_ONLY` is a STOP—not permission to modify M4 or L8. The reconciliation delta updates the binding manifest and changelog only as far as exact compatibility permits, then routes ARCHITECT → fresh-context CRITIC → Rebecca. M4 implementation remains held until both clear it `[PROPOSED]`.

## 10. Rollback and prohibitions

Implementation commits are staged: contract/schema, adapter, harness, diagnostic evidence. A failure suspends the failed stage and all descendants; evidence is retained. ARCHITECT specifies an inverse-commit plan, fresh-context CRITIC reviews it, Rebecca alone authorizes it, TASK BUILDER applies exact inverse mechanical commits, CRITIC verifies, and Rebecca alone releases the rollback `[PROPOSED]`. Reset, force push, deletion of negative evidence, automatic retry, fallback, or reuse of a failed diagnostic is prohibited `[PROPOSED]`.

Native-CUDA L8 adoption is `SHELVED/INOPERATIVE`; its historical feasibility artifacts are retained but are not a current prerequisite, backend, fallback, or reconciliation input. No harness implementation, diagnostic execution, scoring, protected/hold-out/courier seed access or exposure, rerun, native-CUDA adoption work, L8 execution change, G2–G4 freeze, L15/L16/L17 work, state/provenance mutation, merge, or gate decision is authorized by this revised Phase A contract. The five downstream M4 scoring gates remain binding. Rebecca remains sole gate and merge authority.
