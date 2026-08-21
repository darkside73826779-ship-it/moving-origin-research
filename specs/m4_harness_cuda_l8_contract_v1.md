# M4 Harness Contract v1 — CUDA L8 Compatibility

**Date:** 2026-08-21

**Regime:** B

**Status:** Phase A contract-first design `[PROPOSED]`; no implementation or execution authority

**Gate served:** M4 harness design/readiness against approved L8 GPU v1.5

**Base:** `7d6e499cb8a0cf9859cc05b37ec4e97767c4839e`

**Directive:** `coordinator/m4-harness-architect-intake@b32992e7162e129312d2b2493ddbea18b234db81`

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

This contract changes no locked bar, predicate, negative label, seed rule, or scientific arm. L8 uses beta-star `>=0.2`, rho `>=0.8`, at least three doses, five scoring seeds, and the specificity leg `[BAR-Entry 11]`. M4 continues to use exactly the scientific arms `candidate, empty, permuted, shuffled, oracle, naive, frozen, specificity` in that order `[LAW-L18] [LAW-L8]`; the approved backend's `combo` and `null_control` names remain backend-parity identities and are never substituted for or published as M4 negative labels `[PROPOSED]`.

## 2. Authority and immutable identities

The binding manifest must validate against `specs/data/m4_l8_binding_manifest_schema_v1.json`; schema-only validity never overrides its fail-closed provisional status `[PROPOSED]`.

The stable Phase A authority set is `[PROPOSED]`:

1. M4 specification `specs/m4_specification.md` and task specification `specs/m4_task_spec.md` at base `7d6e499cb8a0cf9859cc05b37ec4e97767c4839e`.
2. Approved L8 routing head `e05550f494b2c6dffb2ea9645067395beaf56fe1`, design result `a25398e599622c09d130b597b7bc83ce62a966d5`, CRITIC CLEAR `e0aad1dabde9546e0074a7a375135eb92ee2072a`, and Rebecca release `50260d3288a1bb24581ae0fe4b7f1883d03f5db9`.
3. L8 v1.5 read together with its v1.4 base `4c84248897fe7c0b10f669bba352a05e3268edf2` and CPU baseline `b1397498ca369067e956479e6c2bd6b0793c3e89`.

`specs/data/m4_l8_binding_manifest_v1.json` is the sole adapter-binding authority. In Phase A its status is `PROVISIONAL_BLOCKED` and final implementation/review fields are null. Any attempt to construct the adapter in that state is `INSTRUMENT_FAILURE/M4_L8_BINDING_UNRECONCILED` `[PROPOSED]`. Phase B replaces only provisional fields after the final L8 implementation and independent implementation review exist; ARCHITECT verifies every binding, CRITIC clears the delta, and Rebecca approves it. The future harness accepts exactly the recorded implementation commit, code-tree digest, dependency-manifest digest, configuration-schema digest, and adapter symbol map. It rejects ancestry-only, branch-name-only, dirty-tree, version-range, duck-typed, translated, or fallback identities `[PROPOSED]`.

## 3. Harness architecture

The harness has five layers in fixed order `[PROPOSED]`:

1. `preflight`: validate all raw sidecars, schemas, authority SHAs, clean implementation tree, dependency provenance, mode authorization, seed-custody token, and Phase B binding.
2. `producer_cpu`: construct M4 candidate/system trajectories, homeostatic targets, calibrated perturbations, L18 arms, oracle correctness, primitive NumPy tapes, and CPU calibrations.
3. `l8_adapter_v1`: expose the approved estimator/evaluator semantics through the request/response schemas below.
4. `law_aggregator_cpu`: apply M4 per-seed/all-seed, L18, FWFP, borderline-reporting, and negative-label rules without altering adapter outputs.
5. `publisher`: validate and atomically publish canonical result/evidence pairs.

The adapter is not a scoring authority. It returns measurements and predicates; the CPU law aggregator alone assigns M4 `PASS`, `KILL`, or `INSTRUMENT_FAILURE` under the approved M4 specification `[PROPOSED]`.

## 4. Exact adapter interface

### 4.1 Runtime call

The primitive-tape call is exactly:

`evaluate_l8_v1(request_json_bytes, p_true_f64, correct_bool, xi_f64, xi_l_f64) -> response_json_bytes` `[PROPOSED]`.

The estimator-only call is exactly `evaluate_l8_estimator_v1(estimator_request_json_bytes) -> response_json_bytes`; its input validates against `m4_l8_estimator_request_schema_v1.json` and embeds the complete finite `d_seed` matrix plus the SHA-256 of RFC-8785 canonical `d_seed` bytes `[PROPOSED]`. It never receives or fabricates primitive buffers.

JSON bytes validate against `m4_l8_adapter_request_schema_v1.json` and are RFC 8785 canonical UTF-8 without BOM. Array buffers are immutable, C-contiguous, little-endian; float buffers are IEEE-754 binary64 and the boolean buffer is one byte per element with values zero or one `[PROPOSED]`. Each has shape `(dose_count, windows_per_dose, queries_per_window)` and axis order `dose,window,query`. Buffer byte lengths must equal the shape product times element width. Their lowercase raw SHA-256 values must match the request. Nonfinite float input, nonzero padding, mutation, aliasing between buffers, shape/digest mismatch, or unknown fields fail before CUDA launch `[PROPOSED]`.

The approved four-dose realization uses dose indices `[0,1,2,3]` `[PROPOSED]`; this does not replace the locked at-least-three-dose bar `[BAR-Entry 11]`. CPU seed derivation, NumPy draw order, positive-zero dose-zero `xi_l`, separate candidate/specificity tapes, controller reset per dose, and identity restoration follow approved L8 v1.5/v1.4 exactly `[PROPOSED]`.

The response validates against `m4_l8_adapter_response_schema_v1.json`. It contains complete ordered window deviations `d_seed`, dose summaries, beta-star, rho, defined mask, beta/rho/complete predicates, coverage-index digest, and apparatus status. No rounding, aggregation across seeds, verdict naming, or omitted failed predicate is permitted `[PROPOSED]`.

### 4.2 Real estimator semantics

For each seed, `d_seed` has shape `(4,N_w)` `[PROPOSED]`. Dose summary is the binary64 arithmetic mean over windows. Beta-star is the population-covariance slope of dose summaries on dose indices divided by pooled within-dose sample standard deviation with `4*(N_w-1)` degrees of freedom, using the controlling CPU operation order `[PROPOSED]`. Zero pooled variance is an apparatus fault only when an independent apparatus check proves it; otherwise the statistical predicate fails and the seed remains included `[PROPOSED]`.

Rho uses ascending one-based midranks and binary64 Pearson correlation against dose ranks `(1,2,3,4)` `[PROPOSED]`. Exact finite ties receive the mean occupied rank. Undefined rho fails its predicate without becoming apparatus failure absent independent proof. Rho passes iff `rho>=0.8 OR abs(rho-0.8)<=1e-12` `[BAR-Entry 11] [PROPOSED]`; beta passes iff `beta_star>=0.2` `[BAR-Entry 11]`. The five-seed complete L8 verdict fails when any seed fails beta, has undefined rho, or fails rho `[BAR-Entry 11]`.

Coverage ordering is `(descending c_prime, ascending zero-based query_index)` with exact binary64 ties; the first `max(1,ceil(c_min*W))` indices form the floor and later indices enter only when `c_prime>tau` `[PROPOSED]`. This is the Rebecca-approved v1.5 B11 rule. The adapter may not call NumPy default quicksort or CUDA `topk` where tie order can differ `[PROPOSED]`.

### 4.3 M4 arm/backend mapping

Arm construction and scientific identity remain CPU/M4 responsibilities. Candidate self-model perturbation may invoke the approved CUDA primitive-tape evaluator with backend arm identity `combo`; the severity-matched specificity leg may invoke backend identity `null_control` only if Phase B proves byte/semantic identity to the approved implementation's no-`xi_l` path `[PROPOSED]`. This mapping is provisional and blocked in the Phase A manifest.

The remaining L18 arms are not present in the approved backend contract. They are constructed by the M4 producer and evaluated by the same **real estimator semantics** through operation `ESTIMATOR_ONLY`, which consumes committed `d_seed` profiles rather than inventing GPU perturbation behavior `[PROPOSED]`. Phase B must bind that operation to a reviewed implementation symbol or STOP. No empty/permuted/shuffled/oracle/naive/frozen arm may be renamed `combo` or `null_control`, and no positive claim may omit any arm `[LAW-L18]`.

## 5. CPU/CUDA responsibility boundary

CPU exclusively owns: seed custody and derivation; NumPy RNG and primitive tapes; all candidate/system and L18-arm construction; geometry-aware `calibrate_sigma_dose`; standardized specificity calibration; M4 tolerance/FWFP calibration; identity/order restoration; five-seed aggregation; negative labels; canonicalization; digests; atomic publication; and failure routing `[PROPOSED]`.

CUDA exclusively owns, after a valid request: mirror confidence, approved dose degradation, threshold and coverage selection, regulation-error/controller path, estimator kernel if bound in Phase B, and per-seed response construction `[PROPOSED]`. CUDA must not generate scientific RNG, calibrate sigma/tolerances, assign M4 verdicts, publish, or access protected seed identities `[PROPOSED]`.

CUDA unavailability, allocation failure, dependency mismatch, unsupported operation, or binding mismatch is `INSTRUMENT_FAILURE`; there is no CPU fallback for a request configured for CUDA and no native GPU calibration `[PROPOSED]`. A separately configured CPU-reference compatibility request is diagnostic evidence only and cannot silently service a CUDA request `[PROPOSED]`.

## 6. O-15 compatibility gate

Before any M4 implementation release, TASK BUILDER must execute exactly one candidate-blind compatibility suite in `O-15-diagnostic-only` mode after Phase B authorization `[PROPOSED]`. This is not scoring and consumes no protected/courier seed.

The suite uses `specs/data/m4_l8_compatibility_fixture_v1.json` and performs, in fixed order `[PROPOSED]`:

1. seven rho cases and four complete-verdict cases copied from approved known-good fixture raw digest `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7`;
2. the two B11 cutoff-straddling fixtures copied from approved tie fixture at design result `a25398e599622c09d130b597b7bc83ce62a966d5`;
3. one request-schema rejection, one digest mismatch, one dependency mismatch, one CUDA-unavailable injection, one nondeterministic-repeat injection, and one unsupported-arm injection.

Every positive row must match all literal expected fields; beta/rho absolute difference may be at most `1e-12` while predicate, undefined-mask, coverage order, and canonical response bytes must be exact `[PROPOSED]`. Run zero and a fresh-process run one must yield byte-identical canonical response arrays; no third run is permitted `[PROPOSED]`. Any failure yields `INSTRUMENT_FAILURE`, preserves the diagnostic, and blocks M4 release without retry or replacement `[PROPOSED]`.

The report validates against `m4_l8_compatibility_report_schema_v1.json`, publishes at `diagnostics/m4_l8_compatibility_report.json` plus sidecar, and contains no candidate observations or protected seed identity `[PROPOSED]`.

## 7. Harness configuration, result, custody, and failure

Runtime configuration validates against `m4_harness_config_schema_v1.json`. It is materialized from a committed template by replacing only implementation/result identity placeholders, then RFC-8785 canonicalized; `config_sha256` hashes those canonical bytes `[PROPOSED]`. Unknown/duplicate keys, NaN/Infinity, unapproved identity, absent sidecar, or schema drift fails before RNG construction `[PROPOSED]`.

In that schema, `m4_spec_sha` and `m4_task_spec_sha` are full Git commit identities, not blob hashes; Phase A requires both to equal `7d6e499cb8a0cf9859cc05b37ec4e97767c4839e`, and any later controlling-spec amendment requires a fresh ARCHITECT/CRITIC/Rebecca reconciliation `[PROPOSED]`. Raw file digests are recorded in the handoff artifact inventory rather than substituted for these commit fields.

Top-level M4 results use `m4_harness_result_schema_v1.json`. Law order is `L7,L8,L10,L14,L18`; each law record points to a separately validated `m4_law_artifact_schema_v1.json` canonical artifact and raw sidecar. The law schema fixes all per-seed metrics, predicate arrays, L8 arm order, three L14 couplings, and twenty-four L18 law/arm control records `[PROPOSED]`. Status vocabulary is exactly `PASS,KILL,INSTRUMENT_FAILURE,NOT_RUN` `[PROPOSED]`; existing negative names are never changed. `NOT_RUN` is permitted only after an earlier independently recorded apparatus failure and never converts to PASS/KILL `[PROPOSED]`.

O-15 publication paths are exactly `diagnostics/m4_harness/result.json`, `diagnostics/m4_harness/law_l7.json`, `law_l8.json`, `law_l10.json`, `law_l14.json`, and `law_l18.json`, each with adjacent `.sha256` `[PROPOSED]`. Scoring paths are exactly the same basenames under `runs/m4_scoring/` `[PROPOSED]`. A pre-existing complete scoring pair is a STOP; it is never overwritten or used to justify a rerun `[PROPOSED]`. Temporary, previous, and incomplete suffix behavior follows the atomic-pair rule below.

The scoring gate object records exactly the five retained gates in M4 task specification §1.3: L3 fresh-seed resolution `[BAR-Entry 72]`, FWFP closure `[BAR-Entry 43]`, CRITIC implementation review, Rebecca tolerance-calibration sign-off, and Rebecca courier-channel scoring authorization. Scoring mode is rejected unless all five are true `[PROPOSED]`.

Failure stage is exactly `preflight,producer_cpu,l8_adapter_cuda,estimator,law_aggregator,compatibility,custody,publisher` and message code is exactly one enum in the result schema `[PROPOSED]`. Ordinary per-seed predicate failures are KILL evidence, never apparatus failure. Apparatus failure requires an independent configuration, digest, dependency, finite-input, process, CUDA, nondeterminism, or publication check `[PROPOSED]`.

JSON is RFC 8785 canonical UTF-8 without BOM plus exactly one LF. Sidecars contain lowercase SHA-256, two spaces, basename, LF. Publication uses temp JSON fsync, validation, digest, temp-sidecar fsync, previous-valid-pair preservation, two atomic replacements, and restoration/`.incomplete` retention on interruption `[PROPOSED]`.

## 8. Implementation order and fixed tests

Implementation is forbidden until Phase B is complete. After release, order is `[PROPOSED]`:

1. schemas, strict parser, canonicalizer, sidecar and atomic-pair utilities;
2. binding validator and dependency/source-policy preflight;
3. CPU real-estimator reference and literal fixtures;
4. versioned adapter with no fallback;
5. CPU producer and arm constructors;
6. aggregator/result publisher;
7. failure injection and fresh-process repeatability;
8. O-15 compatibility suite;
9. fresh-context CRITIC implementation review;
10. Rebecca implementation release.

`specs/data/m4_harness_executability_matrix_v1.json` fixes every required test ID, fixture, assertion, and failure. Every row must collect exactly once and pass. Semantic validators must also reject cross-field inconsistencies that JSON Schema cannot express `[PROPOSED]`.

## 9. Phase B reconciliation

Phase B begins only after a formal handoff supplies the final L8 implementation routing head, exact implementation result, independent implementation-review SHA/artifact, dependency manifest and sidecar, configuration schema, public adapter symbols, tests, and evidence digests `[PROPOSED]`. ARCHITECT checks out that exact head in isolation and records for every provisional binding: symbol/path, signature, dtype/shape/order, error behavior, dependency identity, result field mapping, and fixture result `[PROPOSED]`.

Any missing symbol, changed field, new translation, changed dependency, changed tie/RNG/calibration/result semantics, or inability to support `ESTIMATOR_ONLY` is a STOP—not permission to modify M4 or L8. The Phase B delta updates the binding manifest and changelog only as far as exact compatibility permits, then routes ARCHITECT → fresh-context CRITIC → Rebecca. M4 implementation remains held until both clear it `[PROPOSED]`.

## 10. Rollback and prohibitions

Implementation commits are staged: contract/schema, adapter, harness, diagnostic evidence. A failure suspends the failed stage and all descendants; evidence is retained. ARCHITECT specifies an inverse-commit plan, fresh-context CRITIC reviews it, Rebecca alone authorizes it, TASK BUILDER applies exact inverse mechanical commits, CRITIC verifies, and Rebecca alone releases the rollback `[PROPOSED]`. Reset, force push, deletion of negative evidence, automatic retry, fallback, or reuse of a failed diagnostic is prohibited `[PROPOSED]`.

No harness implementation, diagnostic execution, scoring, protected/hold-out/courier seed access or exposure, rerun, L8 execution change, G2–G4 freeze, L15/L16/L17 work, state/provenance mutation, merge, or gate decision is authorized by this Phase A contract. The five downstream M4 scoring gates remain binding. Rebecca remains sole gate and merge authority.
