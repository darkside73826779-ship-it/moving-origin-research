# TASK BUILDER → ARCHITECT, through WORKFLOW COORDINATOR

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Diagnostic feasibility evidence for proposed native-CUDA L8 backend adoption; request for deterministic ARCHITECT specification followed by independent CRITIC review.

## Sender, receiver, and routing

- Sender: TASK BUILDER.
- Current routing recipient: WORKFLOW COORDINATOR.
- Next owner requested: ARCHITECT.
- Required subsequent recipient: fresh-context CRITIC for law-fidelity, scientific-equivalence, RNG, implementation, dependency, performance, and governance review.
- Final authority: Rebecca R. McClintic.

## Rebecca authorization provenance

Rebecca's direct authorizations and directions are recorded without reinterpretation in `docs/rulings/REBECCA_L8_NATIVE_CUDA_DIAGNOSTIC_AUTHORIZATION_RECORD_2026-08-21.md` on this branch. They authorize the completed diagnostic implementation and 1,000/10,000 native-CUDA comparisons and request this ARCHITECT → CRITIC routing.

## Authoritative inputs reviewed

- Parallel CPU oracle branch/result: `taskbuilder/l8-power-analysis` at `6d455bb`.
- CPU artifact: `diagnostics/l8_power_analysis_results.json` at `6d455bb`.
- CPU artifact raw SHA-256: `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`.
- Earlier serial CPU artifact: `a9816bd21e91d793113b073d9871c5fbbb73c88b`.
- CUDA compatibility base: `94e13b2b5bc554d8a4a9eb0867b7bcf9c6a5dcab`.
- Native CUDA implementation commit: `e5367fd4991713d20386619efc92afd3bd1cf76d`.
- Native CUDA 1,000 evidence commit: `e857908ceeaa25ebfff8351d8f34a3b99e9d8276`.
- Native CUDA 10,000 evidence commit: `9678713ef13af1d8746f9ecd9a04457a6461c270`.

## Files implemented

- `diagnostics/l8_legacy_cuda_compat.py`: paired legacy CPU/CUDA primitive-path compatibility adapter.
- `diagnostics/l8_native_cuda_prototype.py`: native CUDA Philox RNG and complete legacy scientific evaluator.
- `tests/test_l8_legacy_cuda_compat.py`: exact paired legacy CPU/CUDA tests across representative cells and both arms.
- `diagnostics/l8_native_cuda_1000_prototype.json` plus sidecar.
- `diagnostics/l8_native_cuda_10000_comparison.json` plus sidecar.
- Companion TASK BUILDER evidence handoffs.

## Verification before native execution

- Full repository battery: `51 passed in 93.43s`.
- Paired compatibility tests preserve legacy RNG draw order and alpha-bias semantics.
- Exact paired `d_seed` and validity masks; beta predicates agree within existing tolerance in the committed paired fixtures.
- Native CUDA RNG and scientific computation execute on GPU; no CPU-generated random tape is used in native mode.
- CPU handles configuration, launch, committed-oracle loading, result collection, and publication only.

## Native CUDA 1,000 result

- Workload: 1,000 repetitions × 240 cells × 2 arms; two complete executions.
- Runtime: `4.7994102999946335` and `4.5289277999982005` seconds.
- Scientific payload repeatability: byte-identical.
- Selected operating point: `(C_min, eta) = (0.5, 0.2)`, matching CPU.
- Aggregate informative cells: 16/16, matching CPU.
- Individual region agreement: 234/240.
- Instrument failures: zero.
- Artifact SHA-256: `f0752bfbe95f195eb4a2b75fb4d0375fb169bf7591247a2299cfccd438adc65a`.

## Apples-to-apples native CUDA 10,000 result

Both CPU and CUDA workloads use 10,000 repetitions for every one of 240 cells and both arms.

| Metric | Serial CPU | Parallel CPU | Native CUDA |
|---|---:|---:|---:|
| Runtime | 170.01 min | 22.63 min | 25.2627 sec |
| Speedup vs serial | — | 7.51x | 403.78x |
| Speedup vs parallel | — | — | 53.74x |
| Selected `(C_min, eta)` | `(0.5, 0.2)` | `(0.5, 0.2)` | `(0.5, 0.2)` |
| Five-seed false-kill | 0.0622267 | 0.0622267 | 0.0632600 |
| Any-seed false-kill | 0.7622733 | 0.7622733 | 0.7590133 |
| False-pass | 0.0257333 | 0.0257333 | 0.0262667 |
| Maximum grid false-kill | 0.4930 | 0.4930 | 0.5009 |
| Aggregate informative cells | 16/16 | 16/16 | 16/16 |
| Instrument failures | 0 | 0 | 0 |

- Individual region agreement: 239/240.
- Five-seed false-kill mean absolute difference over 240 cells: `0.00468208`; maximum `0.0230`.
- Any-seed false-kill mean absolute difference: `0.00399875`; maximum `0.0159`.
- False-pass mean absolute difference: `0.00204833`; maximum `0.0069`; mean signed difference `0.00000167`.
- Mean beta-star mean absolute difference: `0.00139998`; maximum `0.00690287`.
- Artifact SHA-256: `032787bc6a1625ad86b63295a03980e88f982723115452f8080e6c0d606936e2`.

## Findings requiring ARCHITECT specification

1. Define the native RNG identity and counter/domain-separation contract. The prototype uses deterministic Torch CUDA Philox with a SHA-256-derived per-cell/per-arm seed, but formal adoption must bind the exact generator/version/seed derivation and scheduling invariance.
2. Define prospective statistical-equivalence criteria. TASK BUILDER applied no invented threshold and makes no formal equivalence ruling.
3. Dispose the single individual-cell region-label disagreement while preserving the identical aggregate selection and 16/16 informative cells.
4. Define repeat-determinism, GPU/device/dependency identity, failure semantics, and publication/recovery schemas.
5. Define the backend-neutral M4 harness interface so the vetted parallel CPU oracle remains reference/fallback and native CUDA can serve as accelerated diagnostic backend.
6. Determine whether CuPy/NVRTC prototype tooling remains development-only. The executed native prototype itself uses the existing pinned Torch CUDA runtime and does not depend on CuPy.
7. Specify performance acceptance using the measured end-to-end 53.74x speedup over the same-length parallel CPU workload.
8. Route Rebecca's safety-scan workflow direction through the required amendment process for `PUBLIC_REPOSITORY_POLICY.md`; do not infer an operative policy-text change from this TASK BUILDER record.

## TASK BUILDER disposition

The native CUDA prototype is technically successful and materially faster, with the same aggregate scientific selection and small descriptive differences. It is proposed/inoperative pending ARCHITECT specification, CRITIC clearance, and Rebecca's adoption decision. TASK BUILDER does not score, judge equivalence, approve the backend, or merge.

## Explicit prohibitions

No scoring; no protected/hold-out/courier seed access; no rerun-on-failure; no negative renaming; no bar or control change; no G2–G4 freeze; no claim that descriptive similarity is formal equivalence; no M4 scoring use before approval; no merge to main; no L15/L16/L17 before M5. Rebecca remains sole gate and merge authority.

## Public-safety attestation

Under the currently operative repository policy, TASK BUILDER performed the required pre-push scan over the complete new commit: gitleaks, fixed-pattern credentials/private paths, `git diff --check`, and manual review. The exact new-commit range had zero gitleaks findings and no prohibited content. A separate full-working-tree scan reported one `generic-api-key` heuristic at pre-existing `src/test_m3_harness.py:158`; manual review established that the line contains only numeric `accuracy` and `access_count_delta` unit-test fields, not a credential or secret. It predates this work at `d27e44b7ea650a2acbe8fe88dd3fd8b2aa605c6b` and is classified acceptable/false-positive. Rebecca's direction to move safety scans to merge/pre-publication is separately recorded for formal policy amendment and was not silently treated as already operative.
