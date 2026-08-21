# TASK BUILDER → WORKFLOW COORDINATOR — L8 native CUDA 10,000 comparison

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Rebecca-authorized diagnostic-only, same-length native-CUDA comparison with the committed parallel CPU reference [PROPOSED].

## Inputs and artifacts

- Native CUDA implementation: `e5367fd4991713d20386619efc92afd3bd1cf76d`
- CPU oracle: `6d455bb`; artifact SHA-256 `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`.
- CUDA artifact: `diagnostics/l8_native_cuda_10000_comparison.json`.
- CUDA artifact SHA-256: `032787bc6a1625ad86b63295a03980e88f982723115452f8080e6c0d606936e2`.

## Same-length comparison

Both backends ran 10,000 repetitions for each of 240 cells and both arms.

- Parallel CPU runtime: `1357.6829717159271` seconds.
- Native CUDA runtime: `25.2627186000027` seconds.
- CUDA speedup over parallel CPU: `53.74255214622001x`.
- CUDA speedup over serial CPU: `403.7807712428427x`.
- Selected operating point: CPU and CUDA both `(C_min, eta) = (0.5, 0.2)`.
- Aggregate informative cells: CPU and CUDA both 16/16.
- Individual region labels: 239/240 match.
- Instrument failures: CPU and CUDA both zero.

| Quantity | Mean absolute difference | RMSE | Maximum absolute difference | Mean signed difference |
|---|---:|---:|---:|---:|
| Five-seed-mean false-kill | 0.00468208 | 0.00645774 | 0.0230 | 0.00125042 |
| Any-seed false-kill | 0.00399875 | 0.00517263 | 0.0159 | 0.00028792 |
| False-pass | 0.00204833 | 0.00256663 | 0.0069 | 0.00000167 |
| Mean beta-star | 0.00139998 | 0.00180857 | 0.00690287 | -0.00042770 |
| Mean null beta-star | 0.00115282 | 0.00145380 | 0.00419181 | -0.00003694 |

Selected-cell CPU false-kill/false-pass: `0.06222667 / 0.02573333`. Selected-cell CUDA false-kill/false-pass: `0.06326000 / 0.02626667`. CUDA selected-cell any-seed false-kill: `0.75901333`; CPU: `0.76227333`. CUDA maximum grid false-kill: `0.5009`; CPU: `0.4930`.

These are descriptive native-RNG results. No formal statistical-equivalence threshold was invented or applied.

## Safety and holds

Pre-push gitleaks, fixed-pattern credential/private-path scan, diff check, and manual review found no prohibited content. No scoring, protected-seed access, negative renaming, bar change, G2–G4 freeze, merge, or formal equivalence ruling occurred. Next recipient: WORKFLOW COORDINATOR for routing to ARCHITECT/CRITIC and Rebecca.
