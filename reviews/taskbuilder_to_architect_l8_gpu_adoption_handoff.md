# TASK BUILDER → ARCHITECT — L8 GPU Adoption Approval Handoff

**Date:** 2026-08-20

**Regime:** B

**Status:** Proposed adoption design; implementation and full O-15 comparison evidence complete; no scoring or merge approval

**Gate served:** L8 GPU diagnostic-backend adoption design and statistical-equivalence approval

## 1. Constitutional basis — verbatim

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` `[LAW-L8]`.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:54` `[LAW-L18]`.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

Source: `docs/ARCHITECTURAL_CONSTITUTION_v2.md:55` `[LAW-L19]`.

No constitutional text is reconstructed or modified. No waiver is requested. This handoff proposes an execution-backend change while preserving the controlling L8 equations, controls, and locked bars.

## 2. Principal Authorization Record — repo-first memorialization

**Principal:** Rebecca R. McClintic

**Directive date:** 2026-08-20

**Source:** Direct instructions to TASK BUILDER in the project execution thread. The quotations below preserve Rebecca's text as issued; spelling and capitalization are not normalized.

### 2.1 GPU proposal authorization

> "if you can build a scientifically equivalent gpu version that will get us the same results just faster im authorizing it now it will be provided on the basis that this code will go through the approval channel after you present it as proposed code change"

Recorded scope: authorization to build proposed GPU code for approval-channel review. This does not authorize unilateral adoption or merge.

### 2.2 Equivalence model ruling

> "statistical equivalence is the most obvious path since what im reading is that a byte for byte is nearly impossible and would probably be nearly impossible for even seperate cpu runs"

Recorded scope: statistical equivalence, rather than byte-for-byte identity, is the controlling comparison model.

### 2.3 Dependency installation authorization

> "yes install any dependencies please and ill authorize any pop up prompts for approval"

Recorded scope: installation of dependencies needed for the local GPU proposal and diagnostics. No dependency artifact, environment dump, or machine-private path is authorized for publication.

### 2.4 Bounded equivalence-test authorization

> "im authorizing you to do a short test run just long enough to verify its equivalence"

Recorded scope: a bounded O-15 comparison diagnostic. This did not authorize scoring.

### 2.5 Capability-parity directive

> "yes lets ensure we have the same capabilities minus the speed boost in place and the appropriate adjustments required to ensure gpu products are scientifically equivalent as possible"

Recorded scope: preserve CPU scientific capabilities and make backend-specific adjustments needed for the closest practicable scientific equivalence.

### 2.6 Equal-length full-comparison authorization

> "im authorizing on full run comparison that matches the same length of outputs as the cpu runs so if the cpu runs were 1000 or 10,000 etc then the gpu run should also be done just the same"

Recorded scope: full O-15 GPU comparison using the same workload counts as the completed CPU diagnostic, including inherited calibration and simulation lengths. This did not authorize scoring, protected seeds, or merge.

### 2.7 Reuse-existing-rules clarification

> "i understand you cant invent scientific rules but you can use the old ones and imlement the equivalent gpu versions"

Recorded scope: existing CPU scientific rules control the GPU implementation; TASK BUILDER may implement backend-equivalent mechanisms but may not invent new scientific criteria.

### 2.8 Authorization boundary

Together these directives authorize the proposed implementation, local dependencies, bounded diagnostic, and completed equal-length O-15 comparison. They do not approve statistical-equivalence tolerances, scoring-backend adoption, CPU-reference replacement, a scientific gate verdict, or merge. Those remain in the approval channel, with Rebecca R. McClintic as sole gate and merge authority.

## 3. Inputs and custody

- Controlling CPU implementation: `b1397498ca369067e956479e6c2bd6b0793c3e89`
- Completed CPU evidence and handoff: `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3`
- Initial GPU proposal: `15639451c59c7cffb6133296f257720bdca38845`
- GPU parity hardening: `78aeee29948955f80a45156dedb4bb547fb61f93`
- Equal-length GPU runner: `83760c501d216b8eb402c338737556e6e9182700`
- Completed GPU evidence: `1bf7654533483cb704a7b8e0898dbbf5439b1552`
- Branch: `proposal/l8-gpu-statistical-equivalence`
- Constitution source reviewed directly: `docs/ARCHITECTURAL_CONSTITUTION_v2.md`, Regime B
- Public policy reviewed directly: `PUBLIC_REPOSITORY_POLICY.md`

## 4. Existing implementation

The proposed CUDA implementation is in:

- `diagnostics/l8_gpu_proposal.py`
- `diagnostics/l8_gpu_full_comparison.py`
- `tests/test_l8_gpu_proposal.py`

It preserves:

- CPU-owned scientific constants by importing them directly rather than duplicating them.
- Four dose levels and five-seed grouping `[BAR-Entry 11]`.
- Standardized slope bar `beta-star >= 0.2` `[BAR-Entry 11]`.
- Direct rank-correlation bar `rho >= 0.8` `[BAR-Entry 11]` when the direct-rho path is used.
- Exact tied midranks and the CPU pooled within-dose standard-deviation estimator.
- Windowed controller ordering, reset behavior, coverage floor, null arm, and legacy misspecification profiles.
- Binary64/float64 simulation state and estimator reductions `[PROPOSED — backend-equivalence implementation]`.
- Candidate-blind simulation inputs and O-15 labeling.
- Fail-closed CUDA-unavailable, invalid-profile, invalid-repetition, and invalid-window guards.

The CUDA RNG is distributionally matched but not byte-identical to NumPy. Byte identity is neither claimed nor used as evidence.

## 5. Equal-length evidence

The completed GPU diagnostic used:

- 1,000 calibration pilots `[PROPOSED — inherited CPU apparatus workload]`.
- 10,000 reference repetitions per cell `[PROPOSED — inherited CPU apparatus workload]`.
- 10,000 null repetitions per cell `[PROPOSED — inherited CPU apparatus workload]`.
- 240 parameter cells `[PROPOSED — inherited CPU apparatus grid]`.
- 2,000 repetitions per cell for each legacy misspecification profile `[PROPOSED — inherited CPU diagnostic workload]`.

### 5.1 Reference results

| Metric | Serial CPU | Parallel CPU | GPU | GPU minus CPU |
|---|---:|---:|---:|---:|
| Selected `(C_min, eta)` | `(0.5, 0.2)` | `(0.5, 0.2)` | `(0.5, 0.2)` | exact agreement |
| Five-seed-mean false-kill | 0.0622267 | 0.0622267 | 0.0668800 | +0.0046533 |
| Per-seed any-seed false-kill | 0.7622733 | 0.7622733 | 0.7675200 | +0.0052467 |
| False-pass | 0.0257333 | 0.0257333 | 0.0261000 | +0.0003667 |
| Maximum grid false-kill | 0.4930 | 0.4930 | 0.4907 | -0.0023 |
| Instrument failures, reference plus null | 0 | 0 | 0 | exact agreement |

These are diagnostic observations, not proposed acceptance thresholds and not a TASK BUILDER equivalence ruling.

### 5.2 Calibration finding

- GPU and CPU calibration outputs were identical at 11 of 15 `(alpha, v_mult)` pairs.
- Four pairs landed on different accepted bisection steps.
- Maximum absolute `sigma_dose` difference: 0.74999375.
- The downstream reference selection nevertheless remained `(0.5, 0.2)` on both backends.

This identifies calibration stochasticity as the largest removable source of backend-comparison variance.

### 5.3 Misspecification finding retained as a negative

| Profile | CPU selection | GPU selection | Shared conclusion |
|---|---|---|---|
| `uniform_difficulty` | `(0.6, 0.2)` | `(0.6, 0.01)` | unstable versus reference |
| `bimodal_difficulty` | `(0.5, 0.1)` | `(0.6, 0.2)` | unstable versus reference |

Exact stress-profile selections differ. This negative is retained. The stress maps contain near-ties, so exact coordinate selection is sensitive to independent Monte Carlo streams. TASK BUILDER does not decide whether map-level agreement is sufficient.

### 5.4 Runtime

- Serial CPU reference: 170.01 minutes.
- Parallel CPU reference: 22.63 minutes.
- GPU reference: 26.30 seconds.
- Complete GPU calibration, reference/null, and two-profile stress workload: 33.33 seconds.
- GPU reference speedup: 51.62x over parallel CPU and 387.85x over serial CPU.

Runtime is a diagnostic observation, not an acceptance bar.

## 6. Recommended adoption design for ARCHITECT ruling

### 6.1 Primary backend-equivalence arm — frozen calibration `[PROPOSED]`

Use the already-completed CPU calibration table as immutable input to both CPU and GPU simulations. Do not recalibrate either backend in this arm.

Purpose: isolate CUDA simulation, controller, estimator, aggregation, and output-schema equivalence from calibration Monte Carlo variation.

Required provenance: the frozen table must be extracted from the committed CPU result artifact, accompanied by its source SHA and digest. No hand-copied table is permitted.

### 6.2 Secondary end-to-end arm — native GPU calibration `[PROPOSED]`

Run GPU calibration independently using the unchanged CPU calibration rule, then run the complete GPU workload.

Purpose: verify that the GPU backend supports the complete operational pipeline, while reporting calibration differences separately from backend-equivalence differences.

The completed result at `1bf7654` supplies this secondary-arm evidence.

### 6.3 Logical RNG substream parity `[PROPOSED]`

Replace the single cell-wide CUDA stream with deterministic counter-based substreams keyed by the existing CPU logical identity:

`base_seed + simulation_index * N_SEEDS + seed_index (mod 2^31)` `[PROPOSED — inherited CPU RNG identity rule; GPU mapping requires approval]`.

This preserves the CPU independence structure and scheduling invariance without claiming NumPy/CUDA byte identity. No candidate, scoring, protected, or hold-out seed may enter this mapping.

### 6.4 Precision and estimator requirements `[PROPOSED]`

- Float64 simulation state, controller state, dose means, pooled variance, slope, rho, and aggregation.
- Exact equality ties receive exact midranks.
- Nonfinite estimator output and zero pooled variance fail closed as instrument failure.
- GPU reductions must not use reduced-precision or fast-math substitutions.
- CPU scientific constants remain the single source of truth.

### 6.5 Output compatibility `[PROPOSED]`

The adopted GPU artifact should preserve every scientific field in the controlling CPU JSON. Backend identity, device metadata, RNG family, implementation SHA, dependency versions, and artifact digest may be additive provenance fields. No existing negative field may be renamed or omitted.

### 6.6 Failure routing `[PROPOSED]`

- CUDA unavailable, out-of-memory, nonfinite output, schema mismatch, or failed self-test terminates the run as instrument failure.
- No automatic CPU rerun or GPU retry occurs after failure.
- Any later CPU diagnostic is a separately authorized run and never silently replaces the failed GPU artifact.
- Partial artifacts are marked incomplete and cannot be treated as completed comparison evidence.

## 7. Acceptance protocol ARCHITECT must finish

TASK BUILDER requests an executable specification defining, without post-run tuning:

1. The frozen CPU calibration artifact and digest used by the primary arm.
2. The exact fixed comparison cells or confirmation that the complete 240-cell grid is controlling `[PROPOSED — comparison scope]`.
3. Sample sizes for primary and secondary arms `[PROPOSED]`.
4. Statistical equivalence method and multiplicity handling `[PROPOSED]`.
5. Numeric equivalence tolerances for calibration, mean beta-star, mean rho, five-seed-mean false-kill, complete-verdict false-kill, any-seed false-kill, false-pass, and map-level distances `[PROPOSED]`.
6. Whether exact deterministic selection agreement is a gate or a separately reported diagnostic `[PROPOSED]`.
7. Treatment of undefined/all-instrument-failure cells `[PROPOSED — recommended: preserve existing CPU exclusion rule]`.
8. Required failure-injection cases and expected fail-closed outputs `[PROPOSED]`.
9. Whether approval is limited to O-15 diagnostics or extends to scoring/courier execution `[PROPOSED — TASK BUILDER recommends diagnostic-only adoption first]`.
10. The promotion and rollback conditions, including the CPU reference remaining available until GPU adoption is independently verified `[PROPOSED]`.

No acceptance tolerance is invented in this handoff. ARCHITECT must source-tag every adopted threshold, and CRITIC must falsify the resulting protocol before Rebecca rules.

## 8. Required validation battery after specification approval

### Structural and numerical tests

- CPU-constant binding.
- Estimator identity on fixed arrays, including zero variance.
- Exact rho behavior for perfect, decreasing, tied, constant, and nonfinite dose means.
- Controller update order, dose reset, threshold comparison, and coverage-floor behavior.
- Null-arm identity.
- Both legacy misspecification profiles.
- Fixed logical seed replay and scheduling invariance.
- JSON field parity and strict no-NaN serialization.

### Failure injection

- CUDA unavailable.
- Simulated allocation failure.
- Invalid profile.
- Invalid repetition/window count.
- Nonfinite intermediate or estimator result.
- Missing or digest-mismatched frozen calibration artifact.
- Interrupted run and incomplete artifact.

### Statistical comparison

- Frozen-calibration CPU versus GPU primary arm.
- Native-calibration GPU secondary arm.
- Reference, null, and complete sensitivity-map comparisons.
- Exact selection comparison reported independently from map-level comparison.
- Negative misspecification differences retained in the final handoff.

All development diagnostics remain O-15-labeled and development-pool-only. No protected or scoring seeds are authorized.

## 9. Evidence artifacts

- GPU result: `diagnostics/l8_gpu_full_comparison_results.json`
- GPU result SHA-256: `037bde001f2749e9612f0140505541d4e5a4ffbdf5d09b35232f2475964e5aa0`
- Prior execution handoff: `reviews/taskbuilder_l8_gpu_full_comparison_handoff.md`
- GPU proposal: `docs/proposals/L8_GPU_STATISTICAL_EQUIVALENCE_PROPOSAL.md`
- Regression tests: `tests/test_l8_gpu_proposal.py`
- Test result: five passed, zero failed.

## 10. Requested ARCHITECT output

Return a tagged, executable GPU-adoption specification and TASK BUILDER handoff that:

- Rules on Sections 6 and 7 above.
- Preserves all existing bars, controls, negative names, and scoring logic.
- Defines every implementation detail needed for counter-based substreams and frozen-calibration provenance.
- Defines the statistical equivalence calculations and numeric tolerances before the next comparison run.
- Separates diagnostic-backend adoption from any later scoring-backend approval.
- Routes the completed specification through fresh-context law-fidelity review and CRITIC review before Rebecca's gate.

## 11. Public-repository safety

Before push, TASK BUILDER must run gitleaks over staged content and the resulting commit, plus regex/manual review for credentials, secrets, PII, machine identifiers, private absolute paths, environment dumps, and protected-seed exposure. Findings must be classified and blocking findings removed before push.

Pre-push attestation: staged-content gitleaks and regex/manual review were performed. Zero findings were identified in this handoff; no blocker or Rebecca-classification decision was required. The quoted Principal directives contain Rebecca's authorized public project name but no personal contact details or other PII.

## 12. Blockers

No implementation or hardware blocker. Approval is blocked only on the missing pre-registered statistical-equivalence tolerances, counter-based RNG substream specification, and adoption-scope ruling.

## 13. Exact next recipients

1. ARCHITECT — produce the executable adoption specification.
2. Fresh-context law-fidelity reviewer — verify P1–P6 and verbatim law text.
3. CRITIC — attempt to falsify the equivalence protocol and failure routing.
4. Rebecca R. McClintic — sole authority for the adoption gate and any merge authorization.

## 14. Explicitly prohibited actions

- No scoring or courier construction.
- No protected or hold-out seed execution or exposure.
- No TASK BUILDER equivalence ruling.
- No post-run selection of tolerances.
- No alteration of bars, controls, scoring logic, or negative names.
- No automatic rerun on failure.
- No replacement of the CPU reference before approval.
- No merge to `main` without Rebecca's explicit authorization.
