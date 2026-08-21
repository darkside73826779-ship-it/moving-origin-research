# TASK BUILDER → WORKFLOW COORDINATOR — L8 GPU Full Comparison

**Date:** 2026-08-20

**Regime:** B

**Posture:** O-15 diagnostic-only; synthetic/candidate-blind; no scoring

**Gate served:** Equal-length CPU/GPU L8 power-analysis comparison authorized by Rebecca R. McClintic

## Inputs

- CPU implementation SHA: `b1397498ca369067e956479e6c2bd6b0793c3e89`
- CPU result SHA reviewed: `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3`
- GPU implementation branch: `proposal/l8-gpu-statistical-equivalence`
- Workload: 1,000 calibration pilots; 10,000 reference and null repetitions at each of 240 cells; 2,000 repetitions at each cell for each of two misspecification profiles
- GPU arithmetic: float64 simulation state and estimator reductions
- RNG posture: statistically comparable CUDA stream; not byte-identical to NumPy

## Reference comparison

| Metric | Serial CPU | Parallel CPU | GPU |
|---|---:|---:|---:|
| Selected `(C_min, eta)` | `(0.5, 0.2)` | `(0.5, 0.2)` | `(0.5, 0.2)` |
| Five-seed-mean false-kill | 0.0622267 | 0.0622267 | 0.0668800 |
| Per-seed any-seed false-kill | 0.7622733 | 0.7622733 | 0.7675200 |
| False-pass | 0.0257333 | 0.0257333 | 0.0261000 |
| Maximum grid false-kill | 0.4930 | 0.4930 | 0.4907 |
| Instrument failures, reference + null | 0 | 0 | 0 |
| Reference runtime | 170.01 min | 22.63 min | 26.30 s |

GPU reference speedup was 51.62x over the 16-worker parallel CPU reference and 387.85x over the serial CPU reference.

Calibration outputs were identical at 11 of 15 `(alpha, v_mult)` pairs. Four pairs differed within the legacy bisection's coarse accepted steps; the maximum absolute sigma difference was 0.74999375. The downstream reference selection remained identical.

## Misspecification comparison

| Profile | CPU selection | GPU selection | Reference-selection stability conclusion |
|---|---|---|---|
| `uniform_difficulty` | `(0.6, 0.2)` | `(0.6, 0.01)` | unstable on both backends |
| `bimodal_difficulty` | `(0.5, 0.1)` | `(0.6, 0.2)` | unstable on both backends |

The exact stress-profile selections differ under independent CPU and CUDA random streams. Both backends preserve the governing diagnostic conclusion that misspecification selection is unstable. TASK BUILDER makes no statistical-equivalence ruling; tolerances remain for the approval channel.

## Verification

- Five CUDA regression tests passed.
- End-to-end output contains 240 reference rows, 16 sensitivity cells, and both stress profiles.
- GPU total runtime, including calibration and both stress profiles: 33.33 seconds.
- Result artifact: `diagnostics/l8_gpu_full_comparison_results.json`
- Result artifact SHA-256: `037bde001f2749e9612f0140505541d4e5a4ffbdf5d09b35232f2475964e5aa0`
- Result artifact size: 542,181 bytes.
- A wrapper defect found during the first diagnostic attempt was corrected before publication: undefined all-instrument-failure cells are now excluded from sensitivity aggregation exactly as in the CPU implementation. The final artifact is from a fresh complete diagnostic execution of the corrected code.

## Public-safety attestation

Pre-push gitleaks staged/commit scanning plus regex and manual review were performed. Any finding is classified before push. No credentials, secrets, personal contact information, machine identifiers, private absolute paths, environment dumps, protected seeds, or PII are permitted in the pushed artifact or handoff.

## Blockers

No execution blocker. Formal acceptance tolerances and any decision to promote the GPU backend remain approval-channel decisions.

## Exact next recipient

WORKFLOW COORDINATOR, for ARCHITECT and CRITIC review of statistical equivalence and the stress-selection differences.

## Explicitly prohibited actions

- No scoring or protected-seed execution.
- No TASK BUILDER equivalence or gate ruling.
- No replacement of the CPU reference without approval.
- No merge to `main` without Rebecca's explicit authorization.
- No modification of locked bars, controls, scoring logic, constitution, or provenance ledger.
