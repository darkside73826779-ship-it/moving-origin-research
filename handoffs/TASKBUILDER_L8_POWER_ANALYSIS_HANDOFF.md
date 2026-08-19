# TASK BUILDER Handoff — §8 Power Analysis + R8 Guard

**To:** WORKFLOW COORDINATOR
**From:** TASK BUILDER
**Date:** 2026-08-19
**Gate served:** Item 5 of L8 cross-family directive — §8 candidate-blind power analysis (validation batch) + R8 fail-closed hold-out guard
**Authoritative base:** `e26d05f` (GitHub main)
**Repository:** `darkside73826779-ship-it/moving-origin-research`

## Disposition

**VALIDATION COMPLETE — awaiting routing decision for full run.**

## SHAs

| Item | SHA | Status |
|---|---|---|
| Base (GitHub main) | `e26d05f` | Verified |
| Branch | `taskbuilder/l8-power-analysis` | Pushed to GitHub |
| Branch HEAD | `c3a5d49` | Latest — includes refined calibration + smoke test |
| Initial implementation | `bf02958` | First commit (superseded by `c3a5d49`) |

## Files created/modified

| File | Action | Lines | Description |
|---|---|---|---|
| `diagnostics/l8_power_analysis.py` | Created | 1015 | §8 power analysis simulation |
| `src/e1_experiment.py` | Modified | +7 / -5 | R8 fail-closed hold-out guard |

## §8 Power Analysis — validation results

### Step 1: Estimator validation (§2 XF-5)

| Example | Mean β* | Anchor | Tolerance | Verdict |
|---|---|---|---|---|
| A (known positive slope) | 0.2114 | 0.2 `[BAR-Entry 11]` | ±0.05 `[PROPOSED]` | PASS |
| B (known zero slope) | 0.0014 | 0.0 | ±0.05 `[PROPOSED]` | PASS |

The β* estimator correctly recovers known effect sizes on synthetic validation examples. 10,000 trials per example; 0 instrument failures.

### Step 2: 100-simulation validation batch (3 representative combos)

Numbers below are from a fresh run against the latest code at `c3a5d49`:

| Combo | α | v_mult | C_min | η | Mean β* | Std | False-kill | Instr fail | Calib time |
|---|---|---|---|---|---|---|---|---|---|
| Low-noise | 0.0 | 0.5 | 0.5 | 0.01 | 0.3680 | 0.1192 | 0.050 | 0 | 34.65s |
| Mid (reference) | 0.1 | 1.0 | 0.7 | 0.1 | 0.3221 | 0.1111 | 0.140 | 0 |
| High-noise | 0.2 | 2.0 | 0.8 | 0.2 | 0.2212 | 0.0974 | 0.430 | 0 | 4.37s |

### Calibration details

σ_dose is calibrated per (α, v) pair via binary search at a reference operating point (C_min=0.7, η=0.1) to achieve true β* ≈ 0.3. Calibration time varies significantly by (α, v) pair — from ~4s (extreme corners) to ~35s (low-noise). The `--full` pipeline was verified via a 64-combo smoke test: sensitivity map, deterministic selection rule, and JSON serialization all produce valid output.

The mean β* varies across (C_min, η) combinations — this is expected, as different controller parameters produce different amounts of pipeline noise, which affects both the variance and the mean of β*_estimated. The false-kill rate is the key output, not the mean β* itself.

### Timing

- Per-simulation time: ~4.2 ms
- Estimated full run (10,000 × 240 combinations × 2 arms): **~5.6 hours** (20,009s)
- Sandbox limit: 10 minutes per command (2 vCPUs, 7.8 GB RAM)

### Recommendation

**Escalate to Rebecca's local system for the full run.** The 5.6-hour estimate far exceeds the sandbox's per-command timeout. Options:
1. Rebecca runs `python diagnostics/l8_power_analysis.py --full` locally
2. Split into sandbox batches: ~6 combos per batch (84s/combo × 6 = ~8.4 min), 40 batches total — feasible but tight against the 10-min limit
3. Reduce simulation count (if 5,000 per combo suffices, ~2.8 hours)

## R8: Fail-closed hold-out guard

- **Before:** Hold-out seeds (45, 46) in a non-scoring run produced a warning via `_tee()` and continued execution
- **After:** Raises `ValueError` with `[R3/R8 FAIL-CLOSED]` label
- **Verified:** Running with `--seeds 45,46` raises immediately
- **No scoring semantics touched**

## Compliance

- §5 P1–P6: P3 source tags throughout (`[BAR-Entry 11]`, `[PROPOSED]`, `[Sol-XF-5]`, `[Sol-XF-9]`, `[LAW-L19]`); P4 regime dating in header
- Candidate-blind (Ruling 9, Entry 76): simulation seeds are deterministic hashes of parameter combos, NOT candidate diagnostic seeds; no candidate output as input anywhere
- O-15 (diagnostic-only): synthetic simulation, not scoring; no scoring seeds used
- No locked bars changed (β* ≥ 0.2 is an input, not an output)
- No L15/L16/L17 before M5

## Blockers

None for the validation batch. The full run requires a decision on execution environment (sandbox batches vs. Rebecca's local system).

## Next recipient

**WORKFLOW COORDINATOR** — route to CRITIC for implementation review (§8 code + R8), then to Rebecca for the full-run decision (sandbox batches vs. local system). The full run feeds Rebecca's G2–G5 gate rulings.

## Explicitly prohibited actions

- No scoring runs, seed execution, or hold-out seed exposure
- No running of seeds 201–203 or 301–303 (O-14)
- No candidate output as input to the simulation (Ruling 9)
- No TASK BUILDER discretion over the selection rule, seeds, grid, profiles, or estimator
- No modification of the spec, constitution, STATE.md, or provenance_log.md
- No merging to main (Rebecca is sole merge authority)
- No L15/L16/L17 before M5
