# LOCAL EXECUTOR → WORKFLOW COORDINATOR Handoff — L8 §8 Power Analysis Results

**Date:** 2026-08-19  
**Regime:** B  
**Posture:** O-15 diagnostic-only; synthetic/candidate-blind; no scoring  
**Gate served:** Produce the §8 sensitivity map and misspecification-stability evidence for Rebecca’s G2–G5 rulings

## Inputs

- Branch: `taskbuilder/l8-power-analysis`
- Executed code SHA: `b1397498ca369067e956479e6c2bd6b0793c3e89`
- Command: `python diagnostics/l8_power_analysis.py --full --workers 16 --stress-test-sims 2000`
- Reference simulations: 10,000 per parameter combination
- Misspecification simulations: 2,000 per parameter combination per profile
- CPU allocation: 16 simulation workers; calibration capped at 15 workers

## Validation results

- Example A: mean beta-star `0.2135`, anchor `0.2`, tolerance `±0.05`, zero instrument failures — PASS.
- Example B: mean beta-star `0.0003`, anchor `0.0`, tolerance `±0.05`, zero instrument failures — PASS.

Representative 100-simulation batch:

| Combination | Mean beta-star | Five-seed-mean false-kill | Per-seed any-seed false-kill | Instrument failures |
|---|---:|---:|---:|---:|
| Low noise / low coverage / low gain | 0.3680 | 0.050 | 0.790 | 0 |
| Reference operating point | 0.3221 | 0.140 | 0.860 | 0 |
| High noise / high coverage / high gain | 0.2212 | 0.430 | 0.940 | 0 |

## Reference sensitivity-map result

- Deterministic selection: `(C_min=0.5, eta=0.2)`.
- Selected-cell five-seed-mean false-kill: `0.0622266666666667`.
- Selected-cell per-seed any-seed false-kill, averaged over the 15 `(alpha, v_mult)` rows: `0.762273333333333`.
- Selected-cell false-pass: `0.0257333333333333`.
- Selected-cell instrument failures: `0` true-effect and `0` null-control.
- Maximum false-kill across the grid: `0.4930`.
- Proposed G3 escalation condition: TRIGGERED because maximum grid false-kill exceeds `0.1` `[PROPOSED — apparatus parameter, §8]`. This is an input to Rebecca’s ruling, not a TASK BUILDER ruling.

Sensitivity-map boundaries:

- Abstention-escape: false-kill `>= 0.5` `[PROPOSED — apparatus parameter, §8.7]`.
- Trivial-pass: false-pass `>= 0.5` `[PROPOSED — apparatus parameter, §8.7]`.
- All 16 aggregated `(C_min, eta)` cells were classified informative; zero were classified abstention-escape or trivial-pass.

## Misspecification stress test

| Profile | Selected `(C_min, eta)` | Matches reference | Assessment | Selected mean false-kill | Selected mean false-pass |
|---|---|---|---|---:|---:|
| `uniform_difficulty` | `(0.6, 0.2)` | false | unstable | 0.0 | 0.0 |
| `bimodal_difficulty` | `(0.5, 0.1)` | false | unstable | 0.0 | 0.0317107786447883 |

Both misspecified profiles select a different operating point from the reference. The selection-stability result is therefore unstable and must be retained as a finding for advisor consultation before G4.

## Runtime and parallelism

- Reference full-run elapsed time: `1357.68297171593` seconds (`22.63` minutes).
- Uniform stress profile elapsed time: `157.224700689316` seconds.
- Bimodal stress profile elapsed time: `154.473311185837` seconds.
- Approximate complete execution time including validation and calibration: `28.5` minutes.
- Observed calibration processes: 16 total (one parent plus 15 workers).
- Observed simulation processes: 17 total (one parent plus 16 workers).
- Sampled simulation CPU load: 100%.

## Serial-versus-parallel comparison

The previous completed serial reference artifact is committed at `a9816bd21e91d793113b073d9871c5fbbb73c88b`.

| Metric | Serial | Parallel |
|---|---:|---:|
| Reference elapsed time | 170.01 min | 22.63 min |
| Speedup | — | 7.51x |
| Selected `(C_min, eta)` | `(0.5, 0.2)` | `(0.5, 0.2)` |
| Five-seed-mean false-kill | 0.0622267 | 0.0622267 |
| Per-seed any-seed false-kill | 0.7622733 | 0.7622733 |
| False-pass | 0.0257333 | 0.0257333 |
| Maximum grid false-kill | 0.4930 | 0.4930 |
| Instrument failures | 0 | 0 |

The full reference result table, sensitivity-map structure, and deterministic selection are exactly identical between the serial and parallel artifacts. The old serial artifact lacks the stress-test section because it predates the JSON write-order fix; no serial stress comparison is claimed.

## Artifact and write-order verification

- Artifact: `diagnostics/l8_power_analysis_results.json`.
- Size before commit: `297,936` bytes.
- SHA-256: `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`.
- Reference results, sensitivity map, selection, both false-kill aggregations, and both misspecified profiles are present.
- `misspecification_stress_test` is attached in the final JSON.
- Write-order completeness: PASS.
- Execution exit code: `0`.
- Runtime exceptions or unexpected scientific failures: none.

## Public-safety scan

Public-safety scan: gitleaks staged-change scan plus regex and manual content review of the generated JSON and this handoff; zero findings; cleared. No credentials, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, scoring-seed additions, or PII were found.

## Blockers

None in execution. The unstable misspecification selections and G3 escalation trigger are scientific gate inputs, not implementation blockers and not TASK BUILDER rulings.

## Exact next recipient

WORKFLOW COORDINATOR, to prepare the advisor consultation package and route the sensitivity-map and stability evidence to Rebecca for G2–G5 rulings.

## Explicitly prohibited actions

- No TASK BUILDER or LOCAL EXECUTOR ruling on G2–G5.
- No merge to `main` without Rebecca’s explicit authorization.
- No scoring, hold-out execution/exposure, or rerun of scoring seeds.
- No candidate output as input.
- No deletion, modification, or silent replacement of the committed result artifact.
- No modification of locked bars, controls, scoring logic, specification, constitution, `STATE.md`, or provenance log.
