# L8 GPU Diagnostic-Backend Adoption Specification v1.4

**Date:** 2026-08-20

**Regime:** B

**Status:** ARCHITECT remediation proposal; inoperative pending fresh-context CRITIC clearance and Rebecca's release

**Gate served:** CPU↔GPU equivalence design required before the L8 full-screen GPU diagnostic may be released

**Base:** `b6d4556021ad38199d3bfa90fdb3ef9a99988790`

## 1. Constitutional basis

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` `[LAW-L8]`.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:54` `[LAW-L18]`.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:55` `[LAW-L19]`.

This contract concerns backend equivalence only. It makes no L8 scientific claim, satisfies no future scoring battery, and changes no scientific bar or control.

## 2. Operative authority and inputs

The following committed artifacts control, in descending order after the constitution:

1. `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` at base `b6d4556`.
2. `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md`, copied into this branch from committed source `69feed8d353662c60fe9025b0f3c91dc80b9d1e3`.
3. `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md`, copied into this branch from committed source `5306c3025a6018a4947c97b8f498f811ef7580ba`.
4. Controlling CPU specification `specs/l8_g2g4_minimal_full_screen_spec.md`, source SHA `2082680a7caba85c46e637b3b38d679fa7f80599` `[PROPOSED]`.
5. CPU implementation baseline `b1397498ca369067e956479e6c2bd6b0793c3e89` plus only the direct per-seed rho extension required by Items 1–4 `[PROPOSED]`.
6. Frozen calibration `specs/data/l8_cpu_frozen_calibration_v1.json`, committed-LF SHA-256 `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e` `[PROPOSED]`. `.gitattributes` fixes this file to LF on checkout `[PROPOSED]`.

The Item-1 ruling and controlling CPU specification close the old `b139749` rho gap. The CPU comparator for this gate is therefore not bare `b139749`; it is `b139749` with the exact direct-rho and complete-verdict extension specified in Section 3 `[PROPOSED]`. No other CPU scientific behavior may change `[PROPOSED]`.

## 3. Exact scientific predicate

For each seed, use the four dose-level regulation-error summaries already used by the beta-star estimator `[PROPOSED]`.

- Dose ranks are `(1, 2, 3, 4)` `[PROPOSED]`.
- Response ranks are ascending one-based midranks; exact finite binary64 ties receive the arithmetic mean of occupied ranks `[PROPOSED]`.
- Rho is the binary64 Pearson correlation between dose ranks and response ranks `[PROPOSED]`.
- `RHO_COMPARE_EPS = 1e-12` `[PROPOSED]`.
- `RHO_TEST_VALUE_EPS = 1e-12` controls deterministic-test value comparison only `[PROPOSED]`.
- The rho predicate passes iff `rho >= 0.8 OR abs(rho - 0.8) <= RHO_COMPARE_EPS` `[BAR-Entry 11]`.
- `rho = 0.8 - 2*RHO_COMPARE_EPS` must fail `[PROPOSED]`.
- Finite, shape-valid constant responses produce undefined rho and a rho-predicate failure, not `INSTRUMENT_FAILURE` `[PROPOSED]`.

The complete true-effect verdict is false-kill iff any of five seeds has `beta_star < 0.2`, undefined rho, or a failing rho predicate `[BAR-Entry 11]`. Null false-pass occurs iff every one of five seeds satisfies both predicates `[BAR-Entry 11]`. The beta-only any-seed and five-seed-mean rates remain diagnostics `[PROPOSED]`.

Nonfinite or structurally invalid inputs are `INSTRUMENT_FAILURE` only when an independent apparatus check proves an apparatus fault. Without such proof, the repetition remains in the denominator and the affected statistical predicate fails `[PROPOSED]`.

Deterministic finite-rho value checks pass iff `abs(observed_rho - expected_rho) <= RHO_TEST_VALUE_EPS` `[PROPOSED]`. This comparison is distinct from `RHO_COMPARE_EPS`: it accommodates valid binary64 evaluation-order differences such as `0.7999999999999998`, `0.7999999999999999`, and `0.8`, while predicate outcomes must still be exactly identical `[PROPOSED]`. Undefined expected rho passes the value check only when observed rho is also undefined `[PROPOSED]`.

Inherited bars are unchanged: beta-star at least `0.2`, rho at least `0.8`, at least three doses, exactly five seeds, and the specificity control `[BAR-Entry 11]`. This gate uses four doses `[BAR-Entry 11]`.

## 4. Equivalence model and verdicts

The operative GPU ruling requires same-seed CPU↔GPU reproduction, not an unpaired distributional equivalence study. The v1.1 Wilson/Newcombe intervals, Bonferroni families, aggregate margins, map distances, and equivalence-set rule are retired before execution `[PROPOSED]`. No bootstrap, Wilson, quorum, or fallback procedure is permitted `[PROPOSED]`.

Permitted gate results are:

- `EQUIVALENT_FOR_O15_DIAGNOSTICS` `[PROPOSED]`
- `NOT_EQUIVALENT` `[PROPOSED]`
- `INSTRUMENT_FAILURE` `[PROPOSED]`

For every paired valid seed in the sentinel packet:

- CPU and GPU beta-star values must be bit-identical, or have absolute difference at most `1e-12` `[PROPOSED]`;
- CPU and GPU finite rho values must be bit-identical, or have absolute difference at most `1e-12` `[PROPOSED]`;
- undefined-rho masks must be identical `[PROPOSED]`;
- beta, rho, complete-verdict, and null-control predicate booleans must be exactly identical `[PROPOSED]`;
- all counts and rates must be exactly identical `[PROPOSED]`.

A numeric value within tolerance but producing a different predicate boolean is `NOT_EQUIVALENT` `[PROPOSED]`. Tolerance never overrides predicate parity `[PROPOSED]`.

## 5. RNG and maximum-capacity GPU mechanism

CPU seed derivation is preserved exactly `[PROPOSED]`:

`key = f"alpha={alpha:.6f}|vmult={v_mult:.6f}|cmin={c_min:.6f}|eta={eta:.6f}"` encoded as UTF-8, then `base_seed = int.from_bytes(sha256(key).digest()[:8], "little") mod 2^31` `[PROPOSED]`. The six-decimal formatting, field names, separators, field order, and lowercase spellings are digest input and may not vary `[PROPOSED]`.

For zero-based repetition `i` and seed index `s` in `0..4`, `seed_int = (base_seed + i*5 + s) mod 2^31` `[PROPOSED]`. Uniqueness is asserted over the identity tuple `(cell_ordinal, arm_ordinal, repetition_index, seed_index)`, not over the reduced integer value `[PROPOSED]`. A repeated identity tuple is `INSTRUMENT_FAILURE`; equal derived integers from distinct tuples are reported as `derived_seed_collision_count` and are not relabeled as identity duplication `[PROPOSED]`.

To preserve NumPy RNG semantics while saturating the GPU, the implementation uses this fixed primitive-draw-tape pipeline `[PROPOSED]`:

1. CPU producer processes use `numpy.random.default_rng(seed_int)` with the pinned NumPy version and execute the baseline sampling calls in their original order `[PROPOSED]`.
2. Each producer emits one arm-scoped immutable primitive tape per seed: clipped `p_true` binary64 tensor `(4,N_w,W)`; realized `correct` boolean tensor `(4,N_w,W)`; mirror-normal `xi` binary64 tensor `(4,N_w,W)`; and dose-normal `xi_l` binary64 tensor `(4,N_w,W)`, with exact positive zero at dose zero `[PROPOSED]`. Tensor axes are dose, window, query `[PROPOSED]`. Combo and null tapes are not shared: the null arm follows the baseline by consuming no `xi_l` draws and storing positive-zero `xi_l` values, while the combo arm consumes positive-dose `xi_l` draws in baseline order `[PROPOSED]`.
3. The tape records values after NumPy's beta/normal/random transforms but before mirror confidence, dose degradation, thresholding, coverage-floor selection, regulation-error calculation, controller update, beta-star, rho, predicates, or aggregation `[PROPOSED]`.
4. A factored CPU evaluator and the GPU evaluator consume the identical tape and perform all downstream scientific operations in the baseline order `[PROPOSED]`.
5. On the complete sentinel, the factored CPU evaluator must reproduce the unmodified `b139749` simulation path bit-for-bit for every `d_seed`, beta-star value, and diagnostic verdict before CPU↔GPU comparison is allowed `[PROPOSED]`.

This compares the GPU mirror, degradation, controller, estimator, and verdict path while holding the authorized CPU stochastic distributions and RNG exactly fixed. It does not claim that the existing torch-native RNG proposal is equivalent; that proposal remains unadopted `[PROPOSED]`.

Work items are fixed blocks of thirty-two consecutive repetitions for one `(cell, arm)` pair `[PROPOSED]`. CPU producer worker count is `os.cpu_count()` and must be at least two; otherwise `INSTRUMENT_FAILURE` `[PROPOSED]`. `multiprocessing.Pool(...).imap_unordered(..., chunksize=1)` supplies blocks to a bounded pinned-memory queue of depth `4*os.cpu_count()` `[PROPOSED]`. The GPU processes every available full block as one batch; the final partial batch is forbidden because the sentinel repetition count is divisible by thirty-two `[PROPOSED]`. Results are restored by identity tuple, never completion order `[PROPOSED]`. No serial benchmark or serial fallback is permitted `[PROPOSED]`.

## 6. Frozen sentinel workload

The known-good contract is `specs/data/l8_gpu_adoption_known_good_v1.json`, raw committed-LF file SHA-256 `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7` `[PROPOSED]`, with sidecar `specs/data/l8_gpu_adoption_known_good_v1.json.sha256` `[PROPOSED]`. The fixture and frozen-calibration digests cover their committed UTF-8/LF file bytes, not RFC 8785 reserialization `[PROPOSED]`.

The stochastic sentinel uses exact geometry `(W=100, N_w=16)` and `Q=1600` queries per dose `[PROPOSED]`. It runs exactly 256 repetitions per cell per arm `[PROPOSED]`, five seeds per repetition `[BAR-Entry 11]`, combo then null-control arms `[PROPOSED]`, and these cells in order `[PROPOSED]`:

1. `(alpha=0.0, v_mult=0.5, c_min=0.5, eta=0.01)` `[PROPOSED]`
2. `(alpha=0.1, v_mult=1.0, c_min=0.7, eta=0.1)` `[PROPOSED]`
3. `(alpha=0.2, v_mult=2.0, c_min=0.8, eta=0.2)` `[PROPOSED]`

The combo arm loads sigma from the frozen CPU calibration artifact; the null arm uses `sigma_dose=0.0` `[PROPOSED]`. No calibration executes `[PROPOSED]`. Total sentinel repetitions are `3*2*256 = 1,536` and total logical seeds are `7,680` `[PROPOSED]`.

The known-good contract contains six rho categories plus the no-softening subtest, and four complete-verdict cases; together these cover the controlling CPU specification's seven deterministic categories plus case 2a `[PROPOSED]`. Nonfinite JSON fixture input uses `null` solely as the serialized representation of undefined/nonfinite test input; the in-memory test injects binary64 NaN `[PROPOSED]`.

The entire GPU sentinel is executed twice from a fresh process with identical configuration `[PROPOSED]`. Using exactly the §8.4 construction, the second canonical scientific payload must be byte-identical to the first `[PROPOSED]`. Failure produces `INSTRUMENT_FAILURE`; no third execution is permitted `[OP-Entry 22]`.

## 7. L18 scope

This backend gate makes no positive L8 scientific claim. For backend parity only, the CPU comparator is the reference, the unextended beta-only `b139749` output is a diagnostic comparator, the deterministic rho/aggregation contract supplies expected values, and combo/null are the paired simulation arms `[PROPOSED]`. These are backend-parity roles, not renamed L18 controls. Empty/permuted/shuffled scientific arms are not present in the controlling L8 comparator and are not invented here `[LAW-L19]`.

This narrow backend-equivalence battery does not waive L18 for a later L8 positive claim. Any scoring or scientific claim must run the full controlling L18 battery under a separately approved specification `[LAW-L18]`.

## 8. Exact schemas and canonicalization

All JSON uses UTF-8 without BOM and RFC 8785 JSON Canonicalization Scheme bytes `[PROPOSED]`. Unknown fields, duplicate keys, NaN, and Infinity are rejected `[PROPOSED]`. Object key order in the human-readable source is the order below; canonical bytes follow RFC 8785 `[PROPOSED]`.

### 8.1 Configuration object

Required keys, in source order and with no additions `[PROPOSED]`:

1. `schema_version` string, literal `l8-gpu-adoption-config-v1`;
2. `date` string, literal `2026-08-20`;
3. `regime` string, literal `B`;
4. `implementation_sha` forty-character lowercase hexadecimal string naming Commit A;
5. `mode` string, literal `O-15-diagnostic-only`;
6. `cpu_baseline_sha` string, literal full `b1397498ca369067e956479e6c2bd6b0793c3e89`;
7. `cpu_spec_sha` string, literal full `2082680a7caba85c46e637b3b38d679fa7f80599`;
8. `frozen_calibration` object with `path`, `sha256`;
9. `known_good_fixture` object with `path`, `sha256`, `sidecar_path`;
10. `geometry` object with integer `W`, `N_w`, `Q_per_dose`;
11. `repetitions_per_cell_per_arm` integer;
12. `arms` array exactly `['combo','null_control']`;
13. `cells` array exactly matching the known-good contract;
14. `rng` object with `family='numpy-default_rng'`, `seed_formula='alpha={alpha:.6f}|vmult={v_mult:.6f}|cmin={c_min:.6f}|eta={eta:.6f}'`, `identity_fields=['cell_ordinal','arm_ordinal','repetition_index','seed_index']`, `expected_derived_seed_collision_count=3840`;
15. `parallel` object with `producer_workers='os.cpu_count()'`, `pool='multiprocessing.Pool'`, `chunksize=1`, `block_repetitions=32`, `queue_depth_formula='4*os.cpu_count()'`.

Literal strings and numeric values above are `[PROPOSED]`.

### 8.2 Result object

Required top-level keys in source order `[PROPOSED]`: `header`, `deterministic_tests`, `runs`, `equivalence`, `failure_rehearsal`, `verdict`.

- `header`: exact configuration object plus `numpy_version`, `torch_version`, `cuda_runtime_version`, `gpu_model`, `producer_worker_count`, and `derived_seed_collision_count` `[PROPOSED]`.
- `deterministic_tests`: ordered rows matching known-good `rho_cases` then `complete_verdict_cases`; each row has `id`, `cpu_observed`, `gpu_observed`, `cpu_predicate`, `gpu_predicate`, `pass` `[PROPOSED]`.
- `runs`: exactly two rows, `run_ordinal` zero then one; each has `scientific_payload_sha256`, `elapsed_seconds`, and ordered `cells` `[PROPOSED]`.
- each cell has, in order, `cell_ordinal`, `alpha`, `v_mult`, `c_min`, `eta`, `base_seed`, then `arms` in combo/null order `[PROPOSED]`.
- each arm has `arm`, `n_attempted`, `n_valid`, `n_apparatus_invalid`, `mean_beta_star_cpu`, `mean_beta_star_gpu`, `mean_rho_cpu`, `mean_rho_gpu`, `complete_verdict_count_cpu`, `complete_verdict_count_gpu`, `diagnostic_beta_only_count_cpu`, `diagnostic_beta_only_count_gpu`, `diagnostic_five_seed_mean_count_cpu`, `diagnostic_five_seed_mean_count_gpu`, `max_abs_beta_delta`, `max_abs_rho_delta`, `undefined_rho_masks_equal`, `predicate_vectors_equal` `[PROPOSED]`.
- `equivalence`: `all_deterministic_tests_pass`, `all_numeric_tolerances_pass`, `all_predicates_equal`, `all_counts_equal`, `repeat_payloads_equal` `[PROPOSED]`.
- `failure_rehearsal`: twelve ordered rows defined in Section 9 `[PROPOSED]`.
- `verdict`: one permitted Section 4 value `[PROPOSED]`.

### 8.3 Publication pair

Result path is `diagnostics/l8_gpu_adoption_equivalence.json` and sidecar path is `diagnostics/l8_gpu_adoption_equivalence.json.sha256` `[PROPOSED]`. A sidecar is one lowercase SHA-256, two ASCII spaces, basename, and LF `[PROPOSED]`. JSON temporary suffix is `.tmp`; sidecar temporary suffix is `.sha256.tmp` `[PROPOSED]`.

Write and fsync JSON temp, validate, compute digest, write and fsync sidecar temp, then atomically replace JSON and sidecar `[PROPOSED]`. Before replacement, rename any existing valid pair to `.previous.json` and `.previous.json.sha256`; if either replacement fails, restore that pair and retain temps with `.incomplete` suffixes `[PROPOSED]`. A result is complete only when JSON validates and its sidecar matches `[PROPOSED]`.

Commit A freezes code, schemas, configuration, dependencies, fixtures, and tests. Commit B contains only returned evidence and handoff, and records Commit A as `implementation_sha` `[PROPOSED]`.

### 8.4 Canonical scientific payload and repeat digest

For each run, construct a new object containing exactly these keys in this source order and no others `[PROPOSED]`:

1. `schema_version`, literal `l8-gpu-adoption-scientific-payload-v1`;
2. `implementation_sha`, copied from the validated configuration;
3. `config_sha256`, SHA-256 of the RFC 8785 canonical configuration object;
4. `fixture_sha256`, literal `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7`;
5. `frozen_calibration_sha256`, literal `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e`;
6. `geometry`, copied exactly from configuration;
7. `repetitions_per_cell_per_arm`, copied exactly from configuration;
8. `arms`, copied exactly from configuration;
9. `cells_config`, copied exactly from configuration;
10. `derived_seed_collision_count`;
11. `deterministic_tests`, the complete ordered array defined in §8.2;
12. `cells`, the complete ordered run-specific cell array defined in §8.2, including every arm-level count, mean, maximum delta, undefined-mask equality, and predicate-vector equality field.

All literals and test criteria in this list are `[PROPOSED]`.

Serialize that object with RFC 8785 and compute lowercase SHA-256 over those canonical bytes; this is `scientific_payload_sha256` `[PROPOSED]`. The complete canonical payload bytes must be retained in memory until the containing result validates; they are not published as a separate file `[PROPOSED]`.

The digest domain excludes exactly: top-level `header`; top-level `equivalence`; top-level `failure_rehearsal`; top-level `verdict`; each run's `run_ordinal`, `scientific_payload_sha256`, and `elapsed_seconds`; and all environment/runtime fields `numpy_version`, `torch_version`, `cuda_runtime_version`, `gpu_model`, and `producer_worker_count` `[PROPOSED]`. No field inside `deterministic_tests` or `cells` may be removed, masked, rounded, normalized, or reordered before hashing `[PROPOSED]`.

Run zero and run one pass repeatability iff their canonical payload byte arrays are byte-identical and their `scientific_payload_sha256` strings are identical `[PROPOSED]`. Case 9 applies the same construction after reversed completion delivery `[PROPOSED]`. Any mismatch is `INSTRUMENT_FAILURE`; no third run occurs `[OP-Entry 22]`.

## 9. Twelve-case failure rehearsal

Each case starts from the committed known-good JSON/sidecar pair, runs in a fresh process, preserves the input pair, and emits one ordered row with `case_id`, `injected_boundary`, `expected_status`, `observed_status`, `preserved_paths`, `assertion_pass` `[PROPOSED]`.

1. `cuda_unavailable`: preflight capability hook; expect `INSTRUMENT_FAILURE` `[PROPOSED]`.
2. `allocation_failure`: first GPU batch allocation hook; expect `INSTRUMENT_FAILURE` `[PROPOSED]`.
3. `invalid_profile`: configuration arm changed to `invalid`; expect schema rejection and `INSTRUMENT_FAILURE` `[PROPOSED]`.
4. `invalid_repetitions`: repetitions changed to zero; expect schema rejection and `INSTRUMENT_FAILURE` `[PROPOSED]`.
5. `nonfinite_estimator`: post-estimator finite-check hook; expect `INSTRUMENT_FAILURE` only when hook marks independent apparatus fault `[PROPOSED]`.
6. `missing_calibration`: calibration-open hook; expect `INSTRUMENT_FAILURE` `[PROPOSED]`.
7. `calibration_digest_mismatch`: calibration-verify hook; expect `INSTRUMENT_FAILURE` `[PROPOSED]`.
8. `duplicate_identity_tuple`: result-index hook duplicates one full identity tuple; expect `INSTRUMENT_FAILURE` `[PROPOSED]`.
9. `completion_order_shuffle`: reverse completed block delivery; expect identical canonical scientific payload `[PROPOSED]`.
10. `interrupted_publication`: terminate after JSON-temp fsync; expect prior pair preserved and temp renamed `.incomplete` `[PROPOSED]`.
11. `configuration_mismatch`: change fixture digest by one hexadecimal digit; expect `INSTRUMENT_FAILURE` `[PROPOSED]`.
12. `ordinary_predicate_failure`: use known-good `rho_failure`; expect valid statistical failure, never `INSTRUMENT_FAILURE` `[PROPOSED]`.

No failure case is retried. The prior pair comprises the committed `specs/data/l8_gpu_adoption_known_good_v1.json` and its sidecar; preserved paths are those two exact paths for every case `[PROPOSED]`.

## 10. Adoption rule and routing

`EQUIVALENT_FOR_O15_DIAGNOSTICS` requires every deterministic test, numeric tolerance, predicate equality, count equality, repeat-payload equality, schema check, digest check, and failure rehearsal to pass `[PROPOSED]`.

An independently valid apparatus with any parity failure yields `NOT_EQUIVALENT` `[PROPOSED]`. A failure of an independent apparatus check yields `INSTRUMENT_FAILURE` `[PROPOSED]`. Ordinary statistical failures never become apparatus failure `[PROPOSED]`.

Native torch RNG calibration divergence remains an observed named negative: four of fifteen pairs differ; the exact maximum absolute difference is `0.7499937499999998`, the other nonzero magnitude is `0.18749843749999995`, and mean absolute difference is `0.1624986458333333`. The two misspecification-profile coordinate disagreements remain named negative findings `[LAW-L19]`. Native GPU calibration and torch-native RNG are not adopted `[PROPOSED]`.

Define `derived_seed_collision_count = sum_z m_z*(m_z-1)/2`, where `m_z` is the number of distinct full identity tuples whose derived `seed_int` equals integer `z`; equivalently it counts unordered pairs of distinct identity tuples sharing a derived integer `[PROPOSED]`. For this exact sentinel it must equal `3840` `[PROPOSED]`: each of the `3*256*5 = 3840` cell/repetition/seed values appears once in each arm, with no additional collision among the three cell ranges `[PROPOSED]`. Any other count is `INSTRUMENT_FAILURE` `[PROPOSED]`.

Any later full-screen GPU run remains bound to the controlling §7.1 schema, field order, types, NaN-to-null handling, atomic write, and output paths `diagnostics/l8_g2g4_minimal_full_screen.json` and `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md` `[PROPOSED]`. This equivalence-packet schema does not replace or amend that full-screen contract `[PROPOSED]`.

One fresh-context CRITIC performs law fidelity first and substantive falsification second. Overall clearance requires `LAW_FIDELITY: PASS` and `SUBSTANTIVE: CLEAR` `[PROPOSED]`. The packet then returns to Rebecca. TASK BUILDER is not released by this specification alone `[PROPOSED]`.

## 11. Explicit prohibitions

- No implementation or execution by ARCHITECT.
- No scoring, courier construction, protected-seed use/exposure, G2–G4 freeze, or full-screen release.
- No bootstrap, Wilson, quorum, fallback, unpaired equivalence interval, or post-run tolerance choice.
- No serial benchmark, automatic retry, CPU fallback, or failed-run replacement.
- No native GPU calibration or torch-native RNG adoption.
- No change to bars, controls, negative names, geometry table, CPU scientific equations, or selection semantics.
- No merge to `main`; Rebecca alone authorizes merges.
- No L15/L16/L17 before M5.
