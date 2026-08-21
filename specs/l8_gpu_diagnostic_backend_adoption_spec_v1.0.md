# L8 GPU Diagnostic-Backend Adoption Specification v1.0

**Date:** 2026-08-20

**Regime:** B

**Status:** ARCHITECT proposal; every criterion tagged `[PROPOSED]` is inoperative until Rebecca signs it

**Gate served:** L8 GPU diagnostic-backend statistical-equivalence pre-registration

**Base:** `60c42025d50b3637b2a5aa19bb0ed1f83948c921`

**Controlling CPU implementation:** `b1397498ca369067e956479e6c2bd6b0793c3e89`

**Prior CPU evidence:** `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3`

**Prior GPU evidence:** `1bf7654533483cb704a7b8e0898dbbf5439b1552`

## 1. Constitutional basis

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` `[LAW-L8]`.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:54` `[LAW-L18]`.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:55` `[LAW-L19]`.

This specification changes no law, scientific estimator, locked bar, control, negative name, selection rule, or scoring rule. It defines whether a CUDA implementation may serve as an O-15 diagnostic execution backend. It does not establish an L8 scientific result.

## 2. Binding inherited rules

- Each simulation contains exactly five logical seeds `[BAR-Entry 11]`.
- The standardized-slope predicate remains `beta_star >= 0.2` `[BAR-Entry 11]`.
- Where the direct-rank path applies, its predicate remains `rho >= 0.8` `[BAR-Entry 11]`.
- Development execution is diagnostic-only and cannot feed an invariant, bar, scientific verdict, or scoring claim under O-15 `[OP-Entry 22]`.
- A failed run is never rerun, retried, rescored, or silently replaced to avoid its outcome under O-14 `[OP-Entry 22]` and D5 `[OP-Entry 12]`.
- Empty, permuted, shuffled, oracle, frozen, and naive controls remain required on every later positive L8 claim `[LAW-L18]`. GPU adoption neither waives nor satisfies a future claim's scoring battery.

Provenance was checked against `docs/rulings/provenance_log.md`: Entry 11.3 supplies the five-seed rule; Entry 22 supplies O-14/O-15; Entry 12 supplies D1–D5. No uncommitted ruling is used.

## 3. Scope and verdict vocabulary

The only permitted result values are:

- `EQUIVALENT_FOR_O15_DIAGNOSTICS` `[PROPOSED]`
- `NOT_EQUIVALENT` `[PROPOSED]`
- `INSTRUMENT_FAILURE` `[PROPOSED]`

`EQUIVALENT_FOR_O15_DIAGNOSTICS` authorizes neither scoring nor merger. It means only that Rebecca may, after CRITIC review, permit this GPU backend for candidate-blind synthetic development diagnostics `[PROPOSED]`.

The CPU implementation remains the scientific reference and rollback target `[PROPOSED]`. No automatic CPU fallback is permitted within a failed GPU run under O-14 `[OP-Entry 22]`.

## 4. Frozen-calibration primary arm

The immutable input is `specs/data/l8_cpu_frozen_calibration_v1.json`. Its required SHA-256 is `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e` `[PROPOSED]`. Its source is the committed CPU result at `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3:diagnostics/l8_power_analysis_results.json`, Git blob `ac691f74d283e545948422870753036dc94b905e` `[PROPOSED]`.

Before execution, the harness must:

1. verify the calibration file byte digest exactly `[PROPOSED]`;
2. require exactly fifteen entries in lexicographic numeric order by `(alpha, v_mult)` `[PROPOSED]`;
3. verify that each pair has exactly one entry and that all expected pairs are present `[PROPOSED]`;
4. load every number as binary64 without rounding or reserialization `[PROPOSED]`;
5. compare the loaded CPU and GPU calibration arrays bit-for-bit; the allowed primary-arm calibration difference is exactly zero `[PROPOSED]`.

Any failure of these independent checks is `INSTRUMENT_FAILURE` `[PROPOSED]`. Neither backend recalibrates in the primary arm `[PROPOSED]`.

## 5. Compared implementation and arithmetic

The CPU comparator is the implementation at `b1397498ca369067e956479e6c2bd6b0793c3e89`, Git blob `b3d4b52c5442f9a9bbeb5a65c7d81b15e5067522` `[PROPOSED]`. The GPU implementation begins from `diagnostics/l8_gpu_proposal.py` at `1bf7654533483cb704a7b8e0898dbbf5439b1552` `[PROPOSED]`.

The GPU path must import CPU scientific constants. It must use binary64 for state, controller updates, dose means, pooled variance, beta-star, rho, and reductions `[PROPOSED]`. Reduced-precision matrix modes, automatic mixed precision, and fast-math substitutions are forbidden `[PROPOSED]`. Exact equal values receive exact midranks `[PROPOSED]`.

The complete per-repetition verdict is:

`PASS iff, for every one of the five logical seeds, beta_star >= 0.2 AND rho >= 0.8` `[BAR-Entry 11]`.

Thus `complete_verdict_false_kill_rate` is the fraction of valid positive-arm repetitions for which that conjunction is false `[PROPOSED]`. Ordinary predicate failure is a statistical outcome, never `INSTRUMENT_FAILURE` `[PROPOSED]`.

The legacy `five_seed_mean_false_kill_rate` is the fraction for which the arithmetic mean of the five beta-star values is below `0.2` `[BAR-Entry 11]`; it remains diagnostic `[PROPOSED]`. `any_seed_false_kill_rate` is the fraction for which at least one seed has beta-star below `0.2` `[BAR-Entry 11]`; it remains diagnostic `[PROPOSED]`. Neither is substituted for the complete verdict.

## 6. RNG identities and parallel execution

The comparison is candidate-blind and uses no protected, hold-out, scoring, or courier seeds under O-15 `[OP-Entry 22]`.

Each backend receives a distinct namespace: ASCII `L8-EQ-CPU-v1` or `L8-EQ-GPU-v1` `[PROPOSED]`. For each arm, profile, parameter cell, repetition index, and logical seed index, form this UTF-8 identity with no spaces:

`namespace|arm|profile|alpha|v_mult|c_min|eta|repetition_index|seed_index` `[PROPOSED]`.

Numeric grid values use the exact decimal spellings in Section 7; `profile` is `reference`, `null`, `uniform_difficulty`, or `bimodal_difficulty`; `repetition_index` is zero-based; `seed_index` is zero through four `[PROPOSED]`. SHA-256 the identity and interpret the first eight digest bytes as an unsigned little-endian integer; reduce modulo `2^31` to obtain `logical_seed` `[PROPOSED]`.

The backend creates a separate generator stream for each logical seed. CUDA must use one independently seeded `torch.Generator(device="cuda")` per logical seed, call `manual_seed(logical_seed)`, and consume draws only for that logical seed `[PROPOSED]`. Logical results are written to their preallocated `(cell_ordinal, repetition_index, seed_index)` positions `[PROPOSED]`. Worker completion order may not determine RNG consumption or output ordering `[PROPOSED]`.

Execution uses the maximum available worker/device capacity selected once at startup; serial comparison is prohibited `[PROPOSED]`. CPU and GPU arms may run concurrently if resources permit `[PROPOSED]`. The artifact records worker count, device count, device model, CUDA runtime, driver, PyTorch, NumPy, and Python versions `[PROPOSED]`.

## 7. Frozen workload and ordering

The primary comparison uses the complete 240-cell Cartesian grid `[PROPOSED]`, ordered with the rightmost coordinate varying fastest:

- `alpha = [0.0, 0.02, 0.05, 0.1, 0.2]` `[PROPOSED]`
- `v_mult = [0.5, 1.0, 2.0]` `[PROPOSED]`
- `c_min = [0.5, 0.6, 0.7, 0.8]` `[PROPOSED]`
- `eta = [0.01, 0.05, 0.1, 0.2]` `[PROPOSED]`

For every cell and backend:

- reference positive arm: 10,000 repetitions `[PROPOSED]`;
- null arm: 10,000 repetitions `[PROPOSED]`;
- each of the two retained misspecification profiles: 2,000 repetitions `[PROPOSED]`.

The workload matches the completed CPU/GPU diagnostic lengths but is a new pre-registered comparison; prior evidence cannot satisfy this gate `[LAW-L19]`. No adaptive stopping, sample extension, or post-run substitution is permitted `[PROPOSED]`.

## 8. Required raw summaries

For every backend, arm, profile, and cell, the artifact must retain counts and sufficient statistics for:

- valid repetitions and apparatus-invalid repetitions `[PROPOSED]`;
- mean and sample variance of per-repetition five-seed mean beta-star `[PROPOSED]`;
- mean and sample variance of per-repetition five-seed mean rho `[PROPOSED]`;
- five-seed-mean false-kill count `[PROPOSED]`;
- complete-verdict false-kill count `[PROPOSED]`;
- any-seed false-kill count `[PROPOSED]`;
- null false-pass count under the complete verdict `[PROPOSED]`;
- the legacy beta-only null false-pass count, diagnostic only `[PROPOSED]`.

Rows are ordered by backend (`cpu`, then `gpu`), arm/profile in the order above, then the Section 7 cell order `[PROPOSED]`. JSON must reject NaN and Infinity `[PROPOSED]`.

## 9. Statistical-equivalence estimand

The estimand is the difference `GPU minus CPU` under the frozen calibration and the fixed workload `[PROPOSED]`. Statistical equivalence is not equality of random streams or equality of point estimates.

### 9.1 Cell-level family

The primary family contains, at each of the 240 reference cells, six endpoints: mean beta-star, mean rho, five-seed-mean false-kill, complete-verdict false-kill, any-seed false-kill, and complete-verdict null false-pass. The family therefore contains 1,440 endpoints `[PROPOSED]`.

Use a two-sided familywise alpha of `0.01` `[PROPOSED]`, Bonferroni-divided equally across the 1,440 endpoints `[PROPOSED]`. For mean endpoints, compute the unequal-variance Welch interval from the two backend sample means, sample variances, and valid counts `[PROPOSED]`. For rate endpoints, call `statsmodels.stats.proportion.confint_proportions_2indep(count1=gpu_count, nobs1=gpu_valid, count2=cpu_count, nobs2=cpu_valid, method="newcomb", compare="diff", correction=False, alpha=0.01/1440)` `[PROPOSED]`. Pin the reviewed Statsmodels version in Commit A; a version change requires CRITIC re-review `[PROPOSED]`. Implementations must use double precision and report the achieved interval level `[PROPOSED]`.

Every interval for mean beta-star and mean rho must lie strictly inside `[-0.04, +0.04]` `[PROPOSED]`. Every interval for the four rate endpoints must lie strictly inside `[-0.04, +0.04]` `[PROPOSED]`. A boundary touch is a failure `[PROPOSED]`.

### 9.2 Aggregate family

For each of the six endpoints, compute each backend's unweighted mean across the 240 cell estimates, then the 240 paired cell differences `[PROPOSED]`. Use a two-sided paired-t interval with familywise alpha `0.01/6` `[PROPOSED]`. Each interval must lie strictly inside `[-0.01, +0.01]` `[PROPOSED]`.

The cell is the aggregation unit; repetitions may not be pooled across cells to narrow this interval `[PROPOSED]`.

### 9.3 Map distances

For each of the sixteen `(c_min, eta)` locations, average each rate across the fifteen `(alpha, v_mult)` cells exactly as the CPU sensitivity-map algorithm does `[PROPOSED]`. For each of the four rate maps, report:

- `L_infinity = max absolute GPU-minus-CPU map-cell difference` `[PROPOSED]`;
- `L1_mean = mean absolute GPU-minus-CPU map-cell difference` `[PROPOSED]`.

Each `L_infinity` must be at most `0.03` `[PROPOSED]`; each `L1_mean` must be at most `0.01` `[PROPOSED]`. These map conditions are conjunctive with Sections 9.1 and 9.2 `[PROPOSED]`.

### 9.4 Selection and ties

The controlling CPU selection rule is unchanged. Exact GPU/CPU coordinate agreement is reported but is not an equivalence gate `[PROPOSED]`. A coordinate may change under statistically indistinguishable Monte Carlo maps.

For reporting only, define a backend's equivalence set as all informative operating points whose selection objective is within `0.01` of that backend's optimum `[PROPOSED]`. Report the intersection, each selected coordinate's membership in the other backend's set, and the existing deterministic tie-break result `[PROPOSED]`. No point outside the pre-registered set may be substituted after inspection `[LAW-L19]`.

The two historical misspecification selection disagreements remain named negative findings. Misspecification exact-coordinate agreement is diagnostic, never silently converted into a pass `[LAW-L19]`.

## 10. Native-calibration secondary arm

The completed native-GPU-calibration result at `1bf7654533483cb704a7b8e0898dbbf5439b1552`, artifact Git blob `4841deff6cf2342089014dce8bbf8ef3e0fa43d9`, is retained as secondary end-to-end evidence `[PROPOSED]`. It is not rerun for this adoption gate under O-14 `[OP-Entry 22]`.

Its calibration comparisons are descriptive only: exact-step agreement count, maximum absolute sigma difference, mean absolute sigma difference, and downstream selections `[PROPOSED]`. There is no native-calibration equivalence gate in v1.0 `[PROPOSED]`. The observed maximum difference `0.74999375` is a retained finding, not an acceptance tolerance `[LAW-L19]`.

Native GPU calibration is therefore not adopted. An operational GPU diagnostic must consume the frozen CPU calibration artifact `[PROPOSED]`. A later native-calibration proposal requires a separately pre-registered calibration study, fresh CRITIC review, and Rebecca's approval `[PROPOSED]`.

## 11. Independent apparatus validity and failure routing

`INSTRUMENT_FAILURE` is assigned exclusively by these independent checks `[PROPOSED]`:

1. required CUDA capability unavailable before simulation `[PROPOSED]`;
2. frozen-calibration path, digest, schema, order, or value check fails `[PROPOSED]`;
3. CPU/GPU constant binding, grid identity, workload count, RNG-identity uniqueness, or output-order check fails `[PROPOSED]`;
4. allocation, kernel, synchronization, process, or serialization crash occurs `[PROPOSED]`;
5. any supposedly valid estimator or summary is nonfinite, or pooled variance is zero where the controlling estimator declares apparatus invalid `[PROPOSED]`;
6. parallel repeatability, atomic-publication, checksum, or schema validation fails `[PROPOSED]`.

Any one apparatus failure terminates publication of an equivalence verdict and produces `INSTRUMENT_FAILURE` `[PROPOSED]`. Ordinary beta-star, rho, false-kill, false-pass, map, or selection outcomes never become apparatus failure `[PROPOSED]`; they yield `NOT_EQUIVALENT` when a Section 9 criterion fails `[PROPOSED]`.

There is no automatic retry, reduced workload, alternate seed, serial fallback, CPU replacement artifact, or result-file overwrite after failure under O-14 `[OP-Entry 22]`.

## 12. L18 and failure-injection battery

Before the statistical comparison, the same committed CPU and GPU implementations must pass one deterministic backend-parity fixture for each L18 category: empty, permuted, shuffled, oracle, frozen, and naive `[LAW-L18]`. These are implementation tests, not scientific scoring. Each fixture must preserve its existing CPU definition; if no committed CPU definition exists, TASK BUILDER must stop rather than invent one `[LAW-L19]`.

The following injected cases are mandatory, each in a fresh process and each producing the expected fail-closed status `[PROPOSED]`:

1. CUDA unavailable → `INSTRUMENT_FAILURE` `[PROPOSED]`;
2. allocation failure → `INSTRUMENT_FAILURE` `[PROPOSED]`;
3. invalid profile → `INSTRUMENT_FAILURE` `[PROPOSED]`;
4. zero or negative repetitions/windows → `INSTRUMENT_FAILURE` `[PROPOSED]`;
5. nonfinite intermediate → `INSTRUMENT_FAILURE` `[PROPOSED]`;
6. missing calibration file → `INSTRUMENT_FAILURE` `[PROPOSED]`;
7. calibration digest mismatch → `INSTRUMENT_FAILURE` `[PROPOSED]`;
8. duplicate logical RNG identity → `INSTRUMENT_FAILURE` `[PROPOSED]`;
9. shuffled completion order with unchanged logical identities → byte-identical ordered summaries `[PROPOSED]`;
10. interrupted run → incomplete artifact retained and no verdict `[PROPOSED]`;
11. schema/configuration mismatch → `INSTRUMENT_FAILURE` `[PROPOSED]`;
12. ordinary statistical predicate failure → valid `NOT_EQUIVALENT`, never `INSTRUMENT_FAILURE` `[PROPOSED]`.

The rehearsal fixture and known-good JSON/sidecar pair must be committed before execution and reviewed by CRITIC. If their exact schema and digest are absent, execution is blocked `[PROPOSED]`.

## 13. Artifacts and atomic publication

TASK BUILDER must define and CRITIC must approve exact JSON Schemas for configuration, raw backend results, equivalence results, and failure rehearsal before any run `[PROPOSED]`. All schemas reject unknown fields `[PROPOSED]`.

Each complete JSON is written to a same-directory temporary file, flushed and synchronized, validated, and atomically replaced; only then is a lowercase SHA-256 sidecar atomically published `[PROPOSED]`. A complete artifact is usable only when JSON and sidecar agree `[PROPOSED]`. A sidecar-publication failure leaves the new JSON marked incomplete and cannot restore or impersonate an older pair `[PROPOSED]`.

Implementation identity uses a two-commit sequence `[PROPOSED]`: Commit A freezes code, tests, schemas, configuration, and fixtures; Commit B contains only returned diagnostic evidence and handoff files and records Commit A's full SHA as `implementation_sha` `[PROPOSED]`. Commit A cannot contain its own SHA `[PROPOSED]`.

## 14. Adoption rule, promotion, and rollback

The result is `EQUIVALENT_FOR_O15_DIAGNOSTICS` only if all of these are true `[PROPOSED]`:

- all independent apparatus checks and failure rehearsals pass `[PROPOSED]`;
- the frozen calibration is exact `[PROPOSED]`;
- every cell-level interval passes Section 9.1 `[PROPOSED]`;
- every aggregate interval passes Section 9.2 `[PROPOSED]`;
- every map distance passes Section 9.3 `[PROPOSED]`;
- all required fields, counts, ordering, digests, and provenance validate `[PROPOSED]`.

If apparatus is valid and any statistical condition fails, the result is `NOT_EQUIVALENT` `[PROPOSED]`. All failures and historical stress-selection disagreements remain findings `[LAW-L19]`.

Even after an equivalence result, GPU use is limited to O-15 synthetic diagnostics and requires Rebecca's express clearance `[OP-Entry 22]`. CPU remains the reference. GPU scoring, courier packaging, protected-seed access, or replacement of CPU scoring requires a new specification, fresh-context law-fidelity review, CRITIC review, and Rebecca's separate authorization `[PROPOSED]`.

Any later reproducibility regression, apparatus failure, dependency incompatibility, or scientific-field mismatch suspends GPU diagnostic use and preserves the failed artifact `[PROPOSED]`. Suspension does not authorize rerunning the failed job; a later CPU diagnostic is a separately authorized run under O-14 `[OP-Entry 22]`.

## 15. Required review sequence

1. Fresh-context law-fidelity reviewer verifies every quotation, source tag, and provenance citation `[PROPOSED]`.
2. Fresh-context CRITIC attempts to falsify the RNG mapping, statistical power, multiplicity correction, tolerances, L18 routing, and failure semantics `[LAW-L19]`.
3. Rebecca alone decides whether to sign the `[PROPOSED]` criteria and release TASK BUILDER `[LAW-L19]`.
4. TASK BUILDER may implement and execute only after that clearance `[PROPOSED]`.

## 16. Explicit prohibitions

- No scoring, courier construction, protected-seed use or exposure, or scientific L8 verdict.
- No merge to `main`; Rebecca alone authorizes merges.
- No post-run tolerance selection, sample extension, alternate aggregation, or endpoint deletion.
- No serial comparison, automatic retry, automatic CPU fallback, or rerun-on-failure.
- No native GPU calibration adoption under this version.
- No changes to locked bars, controls, negative names, selection logic, or L8 scientific meaning.
- No L15/L16/L17 work before M5.
