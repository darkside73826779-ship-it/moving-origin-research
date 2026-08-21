# TASK BUILDER → ARCHITECT — L8 GPU v1.4 SPECIFICATION BLOCK

**Date:** 2026-08-21

**Regime:** B (post-Entry 81; `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5 binding) `[P4]`

**Gate served:** Executability verification before Commit A and before either permitted sentinel execution for the Rebecca-released L8 full-screen GPU diagnostic.

**Status:** SPECIFICATION BLOCK. No implementation commit, sentinel execution, failure rehearsal, or full-screen execution occurred.

## Authority and inputs reviewed

- Rebecca release ruling: `fcaaa38` on `coordinator/rebecca-l8-gpu-prereg-release`; routing head `ecb3cf2`.
- Operative adoption specification v1.4: `4c84248897fe7c0b10f669bba352a05e3268edf2`; Architect routing head `530104a9886b44e633b7a6cd9ac71877082e0fc6`.
- CRITIC v1.4 CLEAR: `62a612fea91546089031b12e5e73a227a2cdc665`.
- Controlling CPU specification package: `2082680a7caba85c46e637b3b38d679fa7f80599`.
- CPU implementation baseline: `b1397498ca369067e956479e6c2bd6b0793c3e89`.
- GPU rebuild ruling: `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md`.
- Geometry freeze ruling: `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md`.
- Item-1 rho authorization: `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md`.
- Frozen calibration digest verified by prior CRITIC: `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e`.
- Known-good fixture digest verified by prior CRITIC: `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7`.

The implementation base was checked out exactly at the operative specification commit `4c84248897fe7c0b10f669bba352a05e3268edf2` on branch `taskbuilder/l8-gpu-fullscreen-release`.

## Why STOP is mandatory

The release handoff states: “If any executable input is genuinely undefined, STOP and route back (do not invent — the stop discipline is the correct behavior).” TASK BUILDER's initialization independently requires a SPECIFICATION BLOCK whenever implementation would require inventing a numerical algorithm, data format, field name, or RNG rule.

The issues below require choices that affect hashed scientific payload bytes, result interpretation, failure classification, or the released 19.2M execution. They cannot be filled by TASK BUILDER judgment.

## B1 — Sentinel count-field polarity and arm semantics are undefined

Specification v1.4 §8.2 requires:

- `complete_verdict_count_cpu` / `complete_verdict_count_gpu`
- `diagnostic_beta_only_count_cpu` / `diagnostic_beta_only_count_gpu`
- `diagnostic_five_seed_mean_count_cpu` / `diagnostic_five_seed_mean_count_gpu`

The specification does not define whether each field counts predicate passes or predicate failures. It also does not define whether the same polarity applies to both arms.

This is materially ambiguous:

- In the combo arm, the controlling full-screen quantities are false-kill counts.
- In the null arm, the controlling quantity is a false-pass count.
- “complete verdict count” could consistently mean complete passes, or could mean the arm-specific adverse event.

These fields are included in the canonical scientific payload and repeat digest, so TASK BUILDER cannot choose a convention.

**Required ARCHITECT closure:** define the exact event counted by all six fields, separately for `combo` and `null_control`, including denominator and treatment of undefined rho/apparatus-invalid repetitions.

## B2 — Exact result-header topology is undefined

Specification v1.4 §8.2 says `header` is the “exact configuration object plus” six runtime fields, but does not state whether:

1. the configuration keys are flattened directly into `header`; or
2. the configuration is nested under a named object inside `header`.

CRITIC recorded this as NB-L but did not resolve it. Unknown fields are forbidden and exact source order is binding. TASK BUILDER therefore cannot choose the topology or invent a nesting field name.

**Required ARCHITECT closure:** provide the complete literal `header` schema, key order, nesting, and types.

## B3 — Commit-A configuration/self-SHA construction is undefined

Specification v1.4 §8.1 requires `implementation_sha` inside the exact configuration object. Section 8.3 says Commit A freezes the configuration but cannot contain its own SHA, while Commit B records Commit A as `implementation_sha`.

CRITIC recorded this as NB-M. The specification does not define:

- whether Commit A contains a configuration template with a placeholder, an omitted field, or no serialized configuration;
- when and by what exact operation the forty-character SHA is inserted;
- whether `config_sha256` hashes a runtime-emitted object or a committed file;
- what validates that the runtime SHA equals the actual checked-out Commit A.

Because `config_sha256` is included in the canonical scientific payload, the choice changes hashed scientific bytes.

**Required ARCHITECT closure:** specify the committed configuration-template representation, runtime materialization rule, SHA validation rule, and exact object hashed as `config_sha256`.

## B4 — Deterministic-test row value types and predicate polarity are incomplete

Specification v1.4 §8.2 names `cpu_observed`, `gpu_observed`, `cpu_predicate`, `gpu_predicate`, and `pass`, but does not define their exact JSON types and meanings across both fixture families:

- rho rows can observe a finite number or undefined value;
- `no_softening` supplies `direct_rho` rather than `responses`;
- complete-verdict rows observe a false-kill outcome rather than a rho value;
- it is unspecified whether `cpu_predicate=true` means “rho predicate passes,” “complete verdict passes,” or “expected false-kill is true” for complete-verdict rows;
- the exact content of `cpu_observed`/`gpu_observed` for a five-seed complete-verdict fixture is unspecified.

These complete rows are included in the canonical payload and unknown fields are forbidden.

**Required ARCHITECT closure:** provide one literal example row for every deterministic category, including exact types, null encoding, predicate polarity, and `pass` calculation.

## B5 — Failure-rehearsal status vocabulary and row types are undefined

Specification v1.4 §9 requires each rehearsal row to contain `case_id`, `injected_boundary`, `expected_status`, `observed_status`, `preserved_paths`, and `assertion_pass`, but does not define:

- the permitted literal status strings;
- the status for `ordinary_predicate_failure`, which must be a valid statistical failure but is neither assigned a Section 4 gate-result literal nor another exact literal;
- whether schema rejection is itself a status or is translated to `INSTRUMENT_FAILURE`;
- whether `preserved_paths` is an ordered array, object, string, or another type;
- exact `injected_boundary` strings;
- whether `assertion_pass` requires byte identity, digest identity, existence, or a combination for preserved paths.

These rows are part of the published result schema. TASK BUILDER cannot invent their data format or status names.

**Required ARCHITECT closure:** provide the exact twelve-row expected schema with literal `case_id`, `injected_boundary`, `expected_status`, `preserved_paths` representation, and the assertion calculation for each case.

## B6 — Rehearsal publication-pair identity conflicts with result publication semantics

Specification v1.4 §8.3 defines the publication pair at:

- `diagnostics/l8_gpu_adoption_equivalence.json`
- `diagnostics/l8_gpu_adoption_equivalence.json.sha256`

Section 9 then states that every rehearsal starts from the committed known-good fixture pair and that “the prior pair comprises” the fixture and its sidecar in `specs/data/`; those exact fixture paths must appear as preserved paths for every case.

For `interrupted_publication`, §8.3 recovery semantics concern replacement of an existing result pair, while §9 identifies a different, read-only fixture pair as the prior pair. The specification does not state whether the rehearsal:

- copies the fixture to the result publication paths;
- performs recovery in a temporary directory;
- attempts publication beside the committed fixture; or
- validates fixture preservation independently from result-pair recovery.

Choosing among these changes `preserved_paths`, filesystem effects, and the assertion.

**Required ARCHITECT closure:** define the exact rehearsal filesystem layout, initial pair, target pair, temporary paths, incomplete paths, and before/after digest assertions for all publication cases.

## B7 — Fresh-process repeat custody is undefined

Specification v1.4 requires the sentinel to execute twice from a fresh process, requires both canonical payload byte arrays to be retained in memory until the containing result validates, and requires byte-array plus digest equality. CRITIC recorded the missing comparing-process definition as NB-K.

The specification does not identify:

- the parent/child process responsible for holding both byte arrays;
- the process boundary over which canonical bytes are transported;
- whether the child returns canonical bytes, a digest only, or a full run object;
- when “the containing result validates” occurs relative to child termination.

A digest-only child return cannot satisfy byte-array comparison. Persisting bytes would violate the “not published as a separate file” rule. TASK BUILDER cannot select an unregistered custody mechanism for the repeatability gate.

**Required ARCHITECT closure:** define the parent/child protocol and explicitly name the process that retains and compares both canonical byte arrays.

## B8 — Full-screen use of the adoption pipeline is underdefined

Specification v1.4 fully defines the primitive-tape pipeline for the sentinel, then says a later full-screen run remains bound to the controlling §7.1 output contract. The Rebecca release authorizes both in one TASK BUILDER task, but the documents do not explicitly define for the full screen:

- whether the full screen must use the same NumPy primitive-tape producers and GPU downstream evaluator;
- whether the factored CPU evaluator also runs for all 19.2M arm-simulations, or only the GPU evaluator runs after sentinel equivalence;
- whether the full screen uses the frozen CPU calibration artifact or executes the controlling CPU calibration algorithm (native GPU calibration is prohibited, but these are not the only two possibilities);
- how the fixed thirty-two-repetition block rule handles 2,000 repetitions, which leaves a sixteen-repetition final block, while §5 only explicitly forbids a partial block for the divisible sentinel workload;
- whether the full-screen producer count is `os.cpu_count()` from the adoption pipeline or the literal sixteen workers required by the controlling full-screen schema (they coincide on the current workstation but remain distinct configuration rules);
- whether full-screen primitive-tape result restoration uses the adoption identity tuple including `arm_ordinal`, despite the controlling full-screen artifact exposing only `base_seed`.

Each choice affects computation, RNG consumption/order, runtime, and possibly the output. TASK BUILDER cannot infer that sentinel implementation details automatically extend to the full screen where the contract did not say so.

**Required ARCHITECT closure:** add an explicit full-screen execution subsection covering evaluator(s), calibration source, producer rule, partial-block rule, identity restoration, and confirmation that the exact controlling §7.1 artifact remains unchanged.

## B9 — Apparatus-invalid versus instrument-failure counters are not mapped for sentinel output

The sentinel arm schema exposes only `n_attempted`, `n_valid`, and `n_apparatus_invalid`. Section 4 permits the top-level result `INSTRUMENT_FAILURE`, and the controlling full-screen schema separately exposes both apparatus-invalid and instrument-failure counts.

The adoption specification does not define whether an independently proven apparatus failure inside an otherwise completed sentinel run:

- increments `n_apparatus_invalid` and permits an arm row;
- terminates the entire sentinel as top-level `INSTRUMENT_FAILURE` without a completed arm row; or
- does both.

Nor does it define the invariant relating `n_attempted`, `n_valid`, and `n_apparatus_invalid` when an instrument failure terminates a block.

**Required ARCHITECT closure:** define sentinel counter invariants and the exact interaction between per-arm apparatus-invalid counts and the top-level `INSTRUMENT_FAILURE` verdict.

## B10 — Dependency freeze lacks the required committed dependency contract

Specification v1.4 requires CPU producers to use a pinned NumPy version and requires Commit A to freeze dependencies, but it does not name:

- the dependency-manifest path and format;
- the pinned NumPy version;
- the pinned torch/CUDA package version;
- the RFC 8785 implementation/version;
- whether the existing `src/requirements.txt` (`numpy==1.26.4`) controls this diagnostic or only the `src` package.

Different NumPy versions can change transformed primitive draws, which directly affects same-seed parity and fixture payloads. This is not merely an environment note.

**Required ARCHITECT closure:** specify the committed dependency manifest and exact versions required for Commit A, including the package source/index needed for the CUDA wheel if applicable.

## Required response

Return a minimally amended, source-tagged executable specification that closes B1–B10 without changing scientific bars, controls, geometry, seed derivation, negative names, or authorization boundaries. Route the amendment through fresh-context law-fidelity and substantive CRITIC review, then Rebecca as required by P5 and the release chain.

The amended TASK BUILDER handoff must name the new operative specification SHA and explicitly re-release implementation/execution if the amendment changes the signed v1.4 text.

## Branch and files

- Branch: `taskbuilder/l8-gpu-fullscreen-release`
- Base: `4c84248897fe7c0b10f669bba352a05e3268edf2`
- File created: `handoffs/TASK_BUILDER_L8_GPU_V1.4_SPECIFICATION_BLOCK.md`

## Verification and execution status

- Operative spec, controlling CPU spec, fixture, frozen calibration, CRITIC CLEAR, and Rebecca release chain were reviewed.
- No protected, hold-out, courier, or scoring seed was accessed or executed.
- Neither permitted sentinel execution was consumed.
- No failure rehearsal was executed.
- The 19.2M full-screen diagnostic was not started.
- No scoring, G2–G4 freeze, CPU replacement, native GPU calibration, torch-native RNG adoption, retry, or fallback occurred.

## Exact next recipient

ARCHITECT, via WORKFLOW COORDINATOR, for specification remediation; then fresh-context CRITIC → Rebecca → TASK BUILDER.

## Explicitly prohibited actions while blocked

- No implementation beyond this executability audit.
- No sentinel or full-screen execution.
- No choosing count polarity, schema topology, status vocabulary, dependency versions, or full-screen pipeline behavior by TASK BUILDER judgment.
- No spec-text modification by TASK BUILDER.
- No scoring, protected-seed access, failed-run rerun, automatic retry/fallback, native GPU calibration, torch-native RNG, CPU replacement, G2–G4 freeze, merge to main, or L15/L16/L17 work before M5.

## Public-repository safety attestation

Public-safety scan: gitleaks plus credential/PII/private-path regex and manual review, complete staged handoff, zero findings, cleared. No credential, personal contact detail, machine identifier, private absolute path, environment dump, or protected-seed exposure is present. Public repository SHAs, repository-relative paths, approved fixture digests, and candidate-blind workload counts were classified as acceptable.
