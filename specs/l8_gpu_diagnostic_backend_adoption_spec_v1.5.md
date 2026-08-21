# L8 GPU Diagnostic-Backend Adoption Specification v1.5 — Executability Amendment

**Date:** 2026-08-21

**Regime:** B

**Status:** ARCHITECT remediation proposal; inoperative pending fresh-context CRITIC law-fidelity/substantive clearance and Rebecca's re-release

**Gate served:** Deterministic closure of TASK BUILDER B1–B11 before Commit A or either authorized sentinel execution

**Amends:** `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.4.md` at `4c84248897fe7c0b10f669bba352a05e3268edf2`

## 1. Constitutional basis and amendment rule

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` `[LAW-L8]`.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:54` `[LAW-L18]`.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:55` `[LAW-L19]`.

This amendment is read together with v1.4. Where it supplies a replacement clause, this amendment controls; all unmentioned v1.4 clauses remain unchanged `[PROPOSED]`. Every number and test criterion below is `[PROPOSED]` unless explicitly tagged otherwise. The locked beta-star `0.2`, rho `0.8`, at-least-three-dose, and five-seed requirements remain `[BAR-Entry 11]`. This diagnostic's exact four-dose realization is an inherited operational choice `[PROPOSED]`, not a locked Entry 11 bar; this sentence supersedes every v1.4 attribution of **exactly four** doses to `[BAR-Entry 11]` while leaving Entry 11's at-least-three-dose bar unchanged `[PROPOSED]`. This amendment authorizes no implementation, execution, scoring, protected-seed access, freeze, or merge `[PROPOSED]`.

## 2. B1 — exact sentinel count semantics

An **included repetition** is one for which the independent apparatus checks pass. `n_valid` is the number of included repetitions; an apparatus-invalid repetition is excluded from all six count numerators and their denominator and increments `n_apparatus_invalid` `[PROPOSED]`. Undefined rho without an independent apparatus fault remains included and is a rho-predicate failure `[PROPOSED]`.

Every count below is an integer in `[0,n_valid]`; its associated rate, when needed for comparison, is `count/n_valid`. If `n_valid=0`, no rate is formed and the run is `INSTRUMENT_FAILURE` `[PROPOSED]`.

For `arm="combo"` `[PROPOSED]`:

- `complete_verdict_count_cpu/gpu`: included repetitions in which **any** of five seeds has `beta_star < 0.2`, undefined rho, or a failing rho predicate; this is the complete false-kill count `[BAR-Entry 11]`.
- `diagnostic_beta_only_count_cpu/gpu`: included repetitions in which **any** of five seeds has `beta_star < 0.2`; this is the beta-only any-seed false-kill count `[BAR-Entry 11]`.
- `diagnostic_five_seed_mean_count_cpu/gpu`: included repetitions in which the arithmetic mean of the five finite beta-star values is `< 0.2`; this is the five-seed-mean beta false-kill diagnostic `[BAR-Entry 11]`. A nonfinite beta-star is handled by the apparatus decision rule before this event is evaluated.

For `arm="null_control"` `[PROPOSED]`:

- `complete_verdict_count_cpu/gpu`: included repetitions in which **every** seed has `beta_star >= 0.2`, defined rho, and a passing rho predicate; this is the complete false-pass count `[BAR-Entry 11]`.
- `diagnostic_beta_only_count_cpu/gpu`: included repetitions in which **every** seed has `beta_star >= 0.2`; this is the beta-only all-seed false-pass count `[BAR-Entry 11]`.
- `diagnostic_five_seed_mean_count_cpu/gpu`: included repetitions in which the arithmetic mean of the five finite beta-star values is `>= 0.2`; this is the five-seed-mean beta false-pass diagnostic `[BAR-Entry 11]`.

CPU and GPU calculate the same named event independently. `all_counts_equal` requires equality of each CPU/GPU pair for all six cells/arms in both runs `[PROPOSED]`.

## 3. B2/B3 — literal header and configuration lifecycle

### 3.1 Committed template and runtime configuration

Commit A SHALL contain `specs/data/l8_gpu_adoption_config_template_v1.json` and its `.sha256` sidecar `[PROPOSED]`. The template uses the exact runtime configuration schema and key order from v1.4 §8.1, except its `implementation_sha` value is the literal string `COMMIT_A_SHA` `[PROPOSED]`. That literal is legal only in the committed template and is illegal in a runtime configuration or result `[PROPOSED]`.

At process startup, before CUDA initialization or any RNG construction, the parent obtains `HEAD` using `git rev-parse --verify HEAD`, strips the single trailing line ending, and requires exactly forty lowercase hexadecimal characters `[PROPOSED]`. It requires `git diff --quiet --exit-code`, `git diff --cached --quiet --exit-code`, and no untracked files under `diagnostics/`, `specs/data/`, or `tests/` except the two declared result publication paths and rehearsal-root paths in §6 `[PROPOSED]`. It reads and raw-digest-validates the template, parses with duplicate-key/unknown-field rejection, copies keys in template source order, and replaces only the value `COMMIT_A_SHA` with the obtained HEAD `[PROPOSED]`. The result is the in-memory runtime configuration; it is never written as a separate configuration file `[PROPOSED]`.

Commit B may add only evidence and its handoff. Its evidence `implementation_sha` is therefore the actual Commit A HEAD used above, not Commit B `[PROPOSED]`. `config_sha256` is lowercase SHA-256 of RFC 8785 canonical bytes of the fully materialized **runtime configuration object**, not of the template file `[PROPOSED]`. Startup independently requires the materialized `implementation_sha` to equal both the checked-out HEAD and the handoff-declared Commit A SHA before either permitted execution `[PROPOSED]`.

### 3.2 Complete header topology

`header` is an object with exactly these keys, order, and types; configuration keys are not flattened `[PROPOSED]`:

1. `configuration`: the exact validated runtime configuration object from §3.1;
2. `numpy_version`: string, exactly `numpy.__version__`;
3. `torch_version`: string, exactly `torch.__version__`;
4. `cuda_runtime_version`: string, exactly `torch.version.cuda` and non-null;
5. `gpu_model`: string, exactly `torch.cuda.get_device_name(0)`;
6. `producer_worker_count`: integer, the actual created producer-process count;
7. `derived_seed_collision_count`: integer, calculated by v1.4 §10.

Unknown, omitted, flattened, or additional header fields fail schema validation and produce `INSTRUMENT_FAILURE` `[PROPOSED]`.

## 4. B4 — deterministic-test row schema and polarity

The ordered deterministic rows are the seven `rho_cases` followed by the four `complete_verdict_cases` in the known-good fixture `[PROPOSED]`. Every row has exactly these keys in order: `id` string; `family` enum `rho|complete_verdict`; `cpu_observed`; `gpu_observed`; `cpu_predicate` boolean; `gpu_predicate` boolean; `pass` boolean `[PROPOSED]`.

For `family="rho"`, each observed value is a finite JSON number or `null`; `null` means undefined rho. Each predicate is **true iff the rho predicate passes**. For response cases the evaluator computes rho; for `no_softening`, it evaluates the fixture's `direct_rho` without constructing response ranks. `pass` is true iff CPU and GPU observed values each equal the fixture expectation under v1.4's deterministic value rule, their predicate booleans each equal `expected_predicate`, and the CPU/GPU predicate booleans are identical `[PROPOSED]`.

Literal rho rows are `[PROPOSED]`:

```json
{"id":"perfect_increasing","family":"rho","cpu_observed":1,"gpu_observed":1,"cpu_predicate":true,"gpu_predicate":true,"pass":true}
{"id":"adjacent_inversion_threshold","family":"rho","cpu_observed":0.7999999999999999,"gpu_observed":0.7999999999999999,"cpu_predicate":true,"gpu_predicate":true,"pass":true}
{"id":"no_softening","family":"rho","cpu_observed":0.799999999998,"gpu_observed":0.799999999998,"cpu_predicate":false,"gpu_predicate":false,"pass":true}
{"id":"tied_responses","family":"rho","cpu_observed":0.9486832980505138,"gpu_observed":0.9486832980505138,"cpu_predicate":true,"gpu_predicate":true,"pass":true}
{"id":"constant_responses","family":"rho","cpu_observed":null,"gpu_observed":null,"cpu_predicate":false,"gpu_predicate":false,"pass":true}
{"id":"decreasing_responses","family":"rho","cpu_observed":-1,"gpu_observed":-1,"cpu_predicate":false,"gpu_predicate":false,"pass":true}
{"id":"nonfinite_without_apparatus_fault","family":"rho","cpu_observed":null,"gpu_observed":null,"cpu_predicate":false,"gpu_predicate":false,"pass":true}
```

For `family="complete_verdict"`, each observed value is an object with exactly `beta_star` (array of five finite numbers), `rho` (array of five finite numbers or nulls), and `false_kill` boolean, in that order. Each predicate is **true iff the complete true-effect verdict passes**, i.e. `!false_kill`. `pass` is true iff both observed objects exactly equal the fixture arrays and derived `expected_false_kill`, both predicates equal `!expected_false_kill`, and the two observed objects and predicates are pairwise identical `[PROPOSED]`.

Literal complete-verdict rows are `[PROPOSED]`:

```json
{"id":"all_pass","family":"complete_verdict","cpu_observed":{"beta_star":[0.25,0.25,0.25,0.25,0.25],"rho":[0.8,0.8,0.8,0.8,0.8],"false_kill":false},"gpu_observed":{"beta_star":[0.25,0.25,0.25,0.25,0.25],"rho":[0.8,0.8,0.8,0.8,0.8],"false_kill":false},"cpu_predicate":true,"gpu_predicate":true,"pass":true}
{"id":"beta_failure","family":"complete_verdict","cpu_observed":{"beta_star":[0.25,0.19,0.25,0.25,0.25],"rho":[0.8,0.8,0.8,0.8,0.8],"false_kill":true},"gpu_observed":{"beta_star":[0.25,0.19,0.25,0.25,0.25],"rho":[0.8,0.8,0.8,0.8,0.8],"false_kill":true},"cpu_predicate":false,"gpu_predicate":false,"pass":true}
{"id":"undefined_rho","family":"complete_verdict","cpu_observed":{"beta_star":[0.25,0.25,0.25,0.25,0.25],"rho":[0.8,null,0.8,0.8,0.8],"false_kill":true},"gpu_observed":{"beta_star":[0.25,0.25,0.25,0.25,0.25],"rho":[0.8,null,0.8,0.8,0.8],"false_kill":true},"cpu_predicate":false,"gpu_predicate":false,"pass":true}
{"id":"rho_failure","family":"complete_verdict","cpu_observed":{"beta_star":[0.25,0.25,0.25,0.25,0.25],"rho":[0.8,0.8,0.79,0.8,0.8],"false_kill":true},"gpu_observed":{"beta_star":[0.25,0.25,0.25,0.25,0.25],"rho":[0.8,0.8,0.79,0.8,0.8],"false_kill":true},"cpu_predicate":false,"gpu_predicate":false,"pass":true}
```

## 5. B5/B6 — typed rehearsal and isolated filesystem

The normative twelve-row contract is `specs/data/l8_gpu_adoption_rehearsal_contract_v1.json` plus its raw-byte `.sha256` sidecar `[PROPOSED]`. Unknown fields and row reordering fail validation `[PROPOSED]`. Permitted `expected_status`/`observed_status` strings are exactly `INSTRUMENT_FAILURE`, `SCHEMA_REJECTED`, `PAYLOAD_IDENTICAL`, `INTERRUPTED_RECOVERED`, and `STATISTICAL_FAILURE` `[PROPOSED]`. Schema-rejection cases are caught by the rehearsal harness and recorded as `SCHEMA_REJECTED`; they do not become a scientific or apparatus result `[PROPOSED]`.

Every `preserved_paths` value is the same ordered array `["specs/data/l8_gpu_adoption_known_good_v1.json","specs/data/l8_gpu_adoption_known_good_v1.json.sha256","specs/data/l8_gpu_adoption_rehearsal_prior_v1.json","specs/data/l8_gpu_adoption_rehearsal_prior_v1.json.sha256"]` `[PROPOSED]`. For each case, `assertion_pass` is true iff: observed status equals expected status; every preserved path exists before and after and has byte-identical content and identical raw SHA-256; and its case-specific assertion in the contract is true `[PROPOSED]`.

Each case runs in a fresh spawned process under the repository-relative root `diagnostics/.l8_gpu_adoption_rehearsal/<two-digit-row-ordinal>-<case_id>/` `[PROPOSED]`. Before injection, the child creates that directory and copies the committed rehearsal-prior JSON bytes to `result.json`; it writes `result.json.sha256` in the required sidecar format using basename `result.json` `[PROPOSED]`. Target paths are `result.json` and `result.json.sha256`; temporary paths are `result.json.tmp` and `result.json.sha256.tmp`; previous paths are `result.previous.json` and `result.previous.json.sha256`; incomplete paths are `result.json.tmp.incomplete` and `result.json.sha256.tmp.incomplete` `[PROPOSED]`. The committed known-good scientific fixture is never copied to a publication target and remains read-only `[PROPOSED]`.

`l8_gpu_adoption_rehearsal_prior_v1.json` is a rehearsal-only valid publication payload; it is not the §8.2 scientific result schema and cannot satisfy or replace a sentinel result `[PROPOSED]`. Publication cases exercise only the byte-pair transaction. `interrupted_publication` starts with the valid target pair, terminates after fsync of `result.json.tmp` and before sidecar-temp creation, then recovery renames the temp to `.incomplete`; the original target JSON and sidecar must remain byte-identical and digest-valid, both `.previous` paths must be absent, and exactly the JSON incomplete path must exist `[PROPOSED]`. Every case directory is retained until its row validates; after the containing result validates, only the containing result is published and rehearsal directories may be removed `[PROPOSED]`.

## 6. B7 — fresh-process custody protocol

One parent orchestrator owns repeatability custody `[PROPOSED]`. It materializes and validates configuration, then creates run-zero child and run-one child **sequentially as separate fresh processes** using Python's `multiprocessing` `spawn` context; this process isolation rule is not a serial benchmark and does not change the maximum-capacity parallel execution inside each child `[PROPOSED]`. The parent never starts a third child `[PROPOSED]`. This exact two-child cap is adopted here for the repeatability gate and is not attributed to Entry 22; O-14 independently forbids re-run-on-failure `[PROPOSED]`. This sentence supersedes every v1.4 `[OP-Entry 22]` attribution attached to a no-third-run/no-third-child rule; those caps remain proposed here rather than sourced to Entry 22 `[PROPOSED]`.

Each child uses a dedicated one-way `multiprocessing.Connection` and sends exactly two `send_bytes` frames in order: (1) the complete RFC 8785 canonical scientific-payload bytes; (2) RFC 8785 canonical bytes of its validated §8.2 run object `[PROPOSED]`. It then closes the connection and exits zero. The parent calls `recv_bytes` twice, requires EOF before any third frame, requires a zero exit code, parses and schema-validates frame two, verifies its digest against frame one, and retains both frame-one byte arrays in parent memory until the complete top-level result validates `[PROPOSED]`. A timeout, extra/missing frame, parse failure, nonzero child exit, or digest mismatch is `INSTRUMENT_FAILURE` and is not retried `[PROPOSED]`.

Only after both children exit and both byte arrays are retained does the parent construct `runs`, compare the two byte arrays and digests, execute/collect the twelve fresh-process rehearsals, construct the containing result, validate it, and publish the atomic pair `[PROPOSED]`. The child payload bytes and frames are never persisted as standalone files `[PROPOSED]`.

## 7. B8 — exact full-screen execution contract

After—and only after—the re-released sentinel returns `EQUIVALENT_FOR_O15_DIAGNOSTICS`, the separately authorized full screen uses the same NumPy primitive-tape producers and the same GPU downstream evaluator defined by v1.4 §5 `[PROPOSED]`. The factored CPU evaluator does **not** evaluate the 19.2 million full-screen arm-simulations; it is used only in deterministic tests and the sentinel equivalence gate `[PROPOSED]`. There is no serial path or CPU fallback `[PROPOSED]`.

Full-screen calibration is performed by the controlling CPU `calibrate_sigma_dose` algorithm, on CPU with the pinned NumPy dependency, once for every controlling `(geometry,alpha,v_mult)` calibration identity and at the controlling reference operating point; the resulting CPU sigma is supplied to the GPU evaluator for all sixteen operating cells of that identity `[PROPOSED]`. The sentinel-only frozen calibration file is not substituted for geometry-aware full-screen calibration. Native GPU calibration remains prohibited `[PROPOSED]`.

The full-screen producer count is exactly the controlling schema's literal `16` workers, regardless of `os.cpu_count()`; preflight requires at least sixteen logical CPUs or returns `INSTRUMENT_FAILURE` before RNG construction `[PROPOSED]`. Each 2,000-repetition `(geometry,cell,arm)` stream is partitioned into sixty-two consecutive blocks of thirty-two and one final block of sixteen, in that order `[PROPOSED]`. The final block is processed at its true size with no padding, duplicated work, discarded work, retry, or altered RNG consumption `[PROPOSED]`.

For the full screen, the producer-to-GPU queue is a blocking bounded queue with hard `maxsize=2` tape blocks `[PROPOSED]`. A producer may not retain a completed tape after a successful `put`; when two blocks are resident, further `put` calls block until the GPU consumer removes one `[PROPOSED]`. No auxiliary pending list, unbounded executor-result buffer, or serialized tape copy may bypass this bound `[PROPOSED]`. Producer completion order may vary, but the collector restores the identity order below; backpressure may change wall time only and may not change RNG, block membership, evaluation, or publication order `[PROPOSED]`. The sentinel retains v1.4's queue-depth formula because its fixed geometry is materially smaller `[PROPOSED]`.

Internal restoration uses the full tuple `(geometry_ordinal,cell_ordinal,arm_ordinal,repetition_index,seed_index)` in controlling geometry/cell/arm order `[PROPOSED]`. This ordering key does not enter seed derivation: the controlling seed formula remains unchanged and geometry is not added to its digest input `[PROPOSED]`. The published `base_seed` remains exactly the controlling value and no internal ordinal is added to the artifact `[PROPOSED]`.

The resulting full-screen JSON and handoff remain exactly bound to controlling CPU specification §7.1: same paths, schema, field order, types, null handling, formulas, aggregation, and selection semantics; this amendment changes only the execution backend after parity clearance `[PROPOSED]`.

## 8. B9 — sentinel counters and top-level instrument failure

For every **completed** arm row, `n_attempted`, `n_valid`, and `n_apparatus_invalid` are nonnegative integers and must satisfy `n_attempted = 256`, `n_valid + n_apparatus_invalid = n_attempted`, and `n_valid > 0` `[PROPOSED]`. Ordinary statistical predicate failures increment the appropriate B1 count while remaining valid and never increment `n_apparatus_invalid` `[PROPOSED]`.

An independently proven repetition-scoped apparatus fault increments `n_apparatus_invalid`; the arm completes all 256 planned repetitions without retry, and any nonzero `n_apparatus_invalid` forces the containing top-level verdict to `INSTRUMENT_FAILURE` after both permitted runs finish `[PROPOSED]`. Such repetitions are excluded from count/rate/mean/max comparisons. CPU and GPU exclusion masks must be identical or the verdict is `NOT_EQUIVALENT` when apparatus checks themselves remain valid `[PROPOSED]`.

A process-, block-, allocation-, configuration-, or publication-scoped apparatus failure aborts the current child without retry. No partial arm row is published; therefore the completed-arm invariant is never applied to a partial row `[PROPOSED]`. For `INSTRUMENT_FAILURE`, `runs` is an ordered array of zero or more **fully validated completed** run objects (maximum two); for either non-instrument verdict it contains exactly run zero and run one `[PROPOSED]`. The top-level result additionally contains `failure` immediately before `verdict`: `null` for non-instrument verdicts, otherwise an object with exactly `stage`, `case_id`, and `message_code`, in that order `[PROPOSED]`. `stage` is exactly one of `preflight`, `deterministic_tests`, `producer`, `gpu_evaluator`, `collector`, `repeat_custody`, `failure_rehearsal`, or `publisher`; `case_id` is a rehearsal-contract case string or null; `message_code` is exactly one of `CUDA_UNAVAILABLE`, `GPU_ALLOCATION_FAILED`, `CONFIG_SCHEMA_REJECTED`, `NONFINITE_APPARATUS`, `CALIBRATION_MISSING`, `CALIBRATION_DIGEST_MISMATCH`, `DUPLICATE_IDENTITY`, `CHILD_PROTOCOL_FAILURE`, `PAYLOAD_REPEAT_MISMATCH`, `PUBLICATION_INTERRUPTED`, `DEPENDENCY_MISMATCH`, or `QUEUE_PROTOCOL_FAILURE` `[PROPOSED]`. Free-form exception text and any other literal are prohibited `[PROPOSED]`. This replaces v1.4's unconditional “runs exactly two” rule and adds no field to the canonical scientific payload `[PROPOSED]`.

## 9. B10 — dependency freeze

Commit A SHALL contain and validate `specs/data/l8_gpu_adoption_dependencies_v1.json` and its raw-byte `.sha256` sidecar `[PROPOSED]`. Required runtime versions are CPython `3.11.9`, NumPy `1.26.4`, SciPy `1.13.1`, PyTorch `2.13.0+cu130`, bundled CUDA runtime `13.0`, and `rfc8785` `0.1.4` `[PROPOSED]`. Each direct package is installed from the manifest's exact HTTPS wheel URL containing its SHA-256 fragment; no sdist or alternate wheel is permitted `[PROPOSED]`.

Source-policy verification uses PEP 610, not `pip freeze` inference `[PROPOSED]`. For each direct distribution, startup reads `<distribution>.dist-info/direct_url.json` through `importlib.metadata.Distribution.read_text("direct_url.json")`; top level must contain exactly `url` and `archive_info`, and `archive_info` may contain only `hash` and `hashes` `[PROPOSED]`. `url` must equal the manifest URL with its fragment removed. At least one of `archive_info.hash == "sha256=<manifest sha256>"` or `archive_info.hashes.sha256 == <manifest sha256>` must exist and be true; if both exist, both must be true; any other hash algorithm/key is rejected `[PROPOSED]`. A missing/duplicate record, unrecognized field, or mismatch fails `[PROPOSED]`. Startup separately requires `importlib.metadata.version(name)` to equal the manifest version and hashes the installed `direct_url.json` bytes into the Commit B handoff `[PROPOSED]`. Installation must therefore use the exact direct URLs; an index-selected installation, even at the same version, fails closed as `DEPENDENCY_MISMATCH` before RNG construction `[PROPOSED]`. `src/requirements.txt` does not control this diagnostic except where the same NumPy pin is repeated `[PROPOSED]`.

The manifest is the complete direct scientific-runtime dependency contract. Transitive wheel dependencies may not provide NumPy, SciPy, torch, CUDA runtime, or RFC 8785 behavior and are captured for provenance by an exact sorted `python -m pip freeze --all` text embedded in the Commit B handoff; they do not permit substitution of a direct dependency `[PROPOSED]`. Installation may use parallel download/build facilities, but no version resolver choice may alter the direct manifest `[PROPOSED]`.

## 10. Executability controls preventing recurrence

Commit A is forbidden until a generated **contract coverage test** proves every row below has: a normative section; an exact schema/type definition; a fixture or literal expected value; a failure disposition; and a fixed test identifier `[PROPOSED]`. V1.5 BF3 supersedes the descriptive v1 matrix with `specs/data/l8_gpu_adoption_executability_matrix_v2.json`; the test validates each row's exact seven-key schema and literal values against `specs/data/l8_gpu_adoption_expected_trace_v1.json` `[PROPOSED]`. Missing, reordered, descriptive, unknown, or additional values fail closed; v1 remains preserved evidence but is not executable authority `[PROPOSED]`.

Required matrix controls are: `COUNT_EVENT_POLARITY`, `HEADER_TOPOLOGY`, `CONFIG_SELF_IDENTITY`, `DETERMINISTIC_ROW_TYPES`, `REHEARSAL_STATUS_ENUM`, `REHEARSAL_FILESYSTEM`, `REPEAT_CUSTODY`, `FULLSCREEN_PIPELINE`, `COUNTER_INVARIANTS`, `DEPENDENCY_FREEZE`, `RNG_IDENTITY`, `COVERAGE_TIE_RULE`, `QUEUE_RESIDENCY_BOUND`, `LOCKED_BAR_LITERAL`, `UNKNOWN_FIELD_REJECTION`, `ATOMIC_PAIR_RECOVERY`, and `AUTHORIZATION_BOUNDARY` `[PROPOSED]`.

Each matrix row has exactly, in order: `control_id` string, `spec_section` string, `schema_ref` string, `fixture_or_manifest` repository-relative path/string, `expected_assertion` literal string, `implementation_test` fixed pytest node ID, and `failure_status` permitted status string `[PROPOSED]`. TASK BUILDER must generate `diagnostics/l8_gpu_adoption_executability_trace.json` raw-byte identical to `specs/data/l8_gpu_adoption_expected_trace_v1.json`; every named pytest node must exist, collect exactly once, execute, and pass `[PROPOSED]`. The generated trace's raw SHA-256 must equal literal `531148c6f1927c9b3f9f7946ec931ac9f16e6a82716619b881fcf4854c6f28ff` and its sidecar `[PROPOSED]`. All seventeen rows must pass before Commit A; the fresh-context CRITIC checks the matrix and implementation mapping before Rebecca may release execution `[PROPOSED]`. This is an executability completeness control, not a new scientific bar `[PROPOSED]`.

### 10.1 B11 — coverage-floor exact-tie ordering

The baseline's unspecified `np.argsort(-c_prime)` quicksort tie order is not a portable CPU↔GPU contract. For both the factored CPU comparator and GPU evaluator, answered-query ordering SHALL be the total lexicographic order `(descending c_prime, ascending zero-based query_index)` `[PROPOSED]`. The first `n_min=max(1,ceil(c_min*W))` entries are the coverage-floor set; subsequent entries are included in that same order exactly when `c_prime > tau` `[PROPOSED]`. Exact confidence equality means exact binary64 equality after clipping; no tie tolerance is introduced `[PROPOSED]`.

This clause expressly supersedes v1.4 §5 step 5's bit-for-bit reproduction requirement **only for baseline selections containing equal `c_prime` keys** `[PROPOSED]`. For all selections without equal keys, every `d_seed`, beta-star, and diagnostic verdict must still reproduce the unmodified `b139749` path bit-for-bit before CPU↔GPU comparison `[PROPOSED]`. For selections with equal keys, the factored CPU adapter implementing this clause—not NumPy default quicksort's unspecified tie order—is the reference, and CPU/GPU ordered indices and all downstream outputs must be identical under the v1.4 tolerances and predicate-parity rule `[PROPOSED]`. Because this is a comparator behavior change, it is inoperative unless Rebecca expressly approves it in the v1.5 re-release `[PROPOSED]`.

The two mandatory cutoff-straddling fixtures are committed, fully realized, and ordered in `specs/data/l8_gpu_adoption_tie_fixtures_v1.json` `[PROPOSED]`. Its exact schema, constants (`EPS_C=0.000001`, `R_STAR=0.1`, four dose indices, four windows), inputs, expected coverage/answered-correctness/risk/deviation, complete `d_seed`, dose summaries, beta-star, rho, beta/rho predicates, and complete predicate are normative; its raw-byte sidecar must match before testing `[PROPOSED]`. CPU and GPU must reproduce every literal expected field using the baseline estimator operations and v1.4 tolerances `[PROPOSED]`. Swapping the tied indices changes the correctness label and must make `tests/test_l8_gpu_adoption.py::test_coverage_tie_rule` fail `[PROPOSED]`. The rule changes no locked numeric bar or non-tied ordering `[PROPOSED]`.

## 11. Routing and prohibitions

This amendment and changelog go to one fresh-context CRITIC for mandatory law-fidelity review first and substantive review second. Only `LAW_FIDELITY: PASS` plus `SUBSTANTIVE: CLEAR` may route to Rebecca `[PROPOSED]`. Because signed v1.4 text is amended, Rebecca must explicitly re-release both implementation and the two permitted executions; prior release does not activate v1.5 `[PROPOSED]`.

TASK BUILDER remains held. No sentinel has been consumed and no full screen may start. No scoring, protected/hold-out seed access or exposure, G2–G4 freeze, confirmation/sensitivity/stress rerun, automatic retry, failed-run replacement, CPU fallback, native GPU calibration, torch-native RNG, bar/control/negative renaming, merge to main, or L15/L16/L17 work before M5 is authorized `[PROPOSED]`.
