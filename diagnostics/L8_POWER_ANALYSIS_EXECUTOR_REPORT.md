# L8 §8 Power Analysis — Local Executor Report

**Execution date:** 2026-08-19

**Source branch:** `taskbuilder/l8-power-analysis`

**Source commit:** `cbe4dfb87a08fa24c072ec0bd94c719aad547c3b`

**Script SHA-256:** `8D0046897A6AA1FB301D14B4F7DFE3D9050F30E87E97B0CB943F6B8314DFEEFC`

**Command:** `python diagnostics/l8_power_analysis.py --full --stress-test-sims 2000`

**Classification:** Candidate-blind synthetic diagnostic only (O-15). This run authorizes no scoring.

## Execution result

The process completed with exit code 0. No source code was modified. No scoring or protected seeds were used.

### Estimator validation

- Example A: mean β* = 0.2135; expected approximately 0.2; PASS; 0 instrument failures.
- Example B: mean β* = 0.0003; expected approximately 0.0; PASS; 0 instrument failures.
- Validation elapsed: 4.88 seconds.

### 100-simulation validation batch

| Case | Mean β* | False-kill, five-seed mean | False-kill, any seed | Instrument failures |
|---|---:|---:|---:|---:|
| Low noise / low coverage / low gain | 0.3680 | 0.050 | 0.790 | 0 |
| Mid/reference | 0.3221 | 0.140 | 0.860 | 0 |
| High noise / high coverage / high gain | 0.2212 | 0.430 | 0.940 | 0 |

Mean measured time was 2.437 ms per simulation.

## Full reference sensitivity map

- Simulations: 10,000 per combination; 240 combinations; two arms.
- Main-analysis elapsed: 10,200.4 seconds.
- Deterministic selection: `C_min = 0.5`, `η = 0.2`.
- Selected-cell mean five-seed false-kill rate: 0.0622266666666667.
- Selected-cell mean any-seed false-kill rate: 0.762273333333333.
- Selected-cell mean false-pass rate: 0.0257333333333333.
- Selected-cell minimum distance to classification boundaries: 0.43777333333333335.
- All 16 aggregated `(C_min, η)` cells were classified `informative`.
- Maximum individual false-kill rate across the 240-point grid: 0.4930. This exceeds the proposed 0.10 threshold and prints `ESCALATE to G3`.
- Total candidate-arm instrument failures: 0.
- Total null-arm instrument failures: 0.

## Reduced misspecification stress test

Each profile used 2,000 simulations per combination across the full 240-combination map.

| Profile | Selected `(C_min, η)` | Matches reference `(0.5, 0.2)` | Assessment |
|---|---|---|---|
| Uniform difficulty | `(0.6, 0.2)` | No | Unstable |
| Bimodal difficulty | `(0.5, 0.1)` | No | Unstable |

Approximate profile runtimes were 1,098.4 seconds and 1,109.0 seconds, respectively.

## Output artifact

- File: `diagnostics/l8_power_analysis_results.json`
- Size: 164,720 bytes.
- SHA-256: `F45D2814A3E86571CD9BD34F02D1CE34A0C293F85E4E1FE4D8D9B56356DF249E`.

## Unexpected behavior requiring TASK BUILDER disposition

The script writes `l8_power_analysis_results.json` at the end of Step 3. It then runs Step 4 and attaches `misspecification_stress_test` to the in-memory `full` object, but it does not rewrite the JSON afterward. Consequently, the reference results are present in the JSON, while the completed stress-test maps are absent. The two stress-test selections and stability assessments above are preserved from successful console output.

No workaround, source modification, or rerun was performed. TASK BUILDER should correct the output-write ordering, and CRITIC should determine the appropriate artifact-recovery or rerun disposition.
