# TASK BUILDER Handoff — §8 Remediation (BF-IMPL-1 + NF-IMPL-1/2/3)

**To:** CRITIC (focused re-review)
**From:** TASK BUILDER
**Date:** 2026-08-19
**Gate served:** §8 implementation remediation — CRITIC BLOCK fix
**Authoritative base:** `e26d05f` (GitHub main)
**Repository:** `darkside73826779-ship-it/moving-origin-research`

## Disposition

**REMEDIATION COMPLETE — ready for CRITIC re-review.**

## SHAs

| Item | SHA | Status |
|---|---|---|
| Base (GitHub main) | `e26d05f` | Verified |
| Branch | `taskbuilder/l8-power-analysis` | Pushed to GitHub |
| Branch HEAD | `5c01d34` | Latest — includes all remediation |

## Fixes applied

### BF-IMPL-1 (blocking) — Misspecification stress-test implemented

**§8 item 9** now implemented as `run_misspecification_stress_test()` and `simulate_one_seed_misspecified()`.

- **Two misspecified profiles**, both genuinely different from the synthetic reference:
  1. `uniform_difficulty`: p_true ~ Uniform(0,1) instead of Beta(4.2,1.8) — flat difficulty distribution vs right-skewed
  2. `bimodal_difficulty`: 50% easy (p=0.9), 50% hard (p=0.3) — bimodal vs unimodal
- Full power analysis (estimator + false-kill + stability) run on each profile across a subset of the parameter grid
- Stability assessment: mean absolute difference in β* between misspecified and reference profiles; assessment = "stable" if mean abs diff < 0.1
- Candidate-blind (Ruling 9): profiles use known oracle ground truth, not candidate output
- Integrated into `main()` as Step 4; results included in `--full` JSON output
- P3 source tags: `[Sol-XF-9]`, `[PROPOSED — apparatus parameter, §8 item 9]`

### NF-IMPL-1 — Private absolute path fixed

- Replaced `/home/user/workspace/mor-repo/diagnostics/l8_power_analysis_results.json` with relative `diagnostics/l8_power_analysis_results.json`
- Works on Rebecca's local system without a workspace directory

### NF-IMPL-2 — Per-seed false-kill aggregation added

- `simulate_one_simulation` now returns `per_seed_betas` array alongside the 5-seed mean
- Both false-kill rates computed and reported in output:
  - `false_kill_rate`: P(mean of 5 β*_s < 0.2) — existing 5-seed mean aggregation
  - `false_kill_rate_per_seed`: P(any of 5 β*_s < 0.2) — matches per-seed scoring bar (spec §2)
- Both included in validation batch output and full-run JSON results
- **Flagged to Rebecca for ruling** on which is the G3-escalation input

### NF-IMPL-3 — Validation table regenerated

- Estimator validation confirmed against latest code:
  - Example A: β* = 0.2111 (anchor 0.2, PASS)
  - Example B: β* = 0.0045 (anchor 0.0, PASS)
- Validation batch numbers are from the latest code at `5c01d34`

## What was NOT touched (all verified CLEAR by CRITIC)

- The estimator (§2 XF-5) — unchanged
- 8 of 10 §8 protocol items (grid, seeds, false-kill, sensitivity map, selection rule, publication) — unchanged
- Candidate-blindness (Ruling 9) — no candidate-output path introduced
- R8 guard — unchanged (verified CLEAR)
- Estimator validation (Examples A/B) — unchanged

## File summary

| File | Lines | Changes |
|---|---|---|
| `diagnostics/l8_power_analysis.py` | 1214 (was 1015) | +209/-10: misspecification stress-test, per-seed false-kill, relative path |

## Compliance

- §5 P3 source tags on all new thresholds in misspecification code
- Candidate-blind throughout (Ruling 9, Entry 76)
- O-15 (diagnostic-only): synthetic simulation, not scoring
- No locked bars changed
- No L15/L16/L17 before M5

## Blockers

None.

## Next recipient

**CRITIC** — focused re-review of BF-IMPL-1 (misspecification stress-test) + NF-IMPL-1/2/3 fixes. On CLEAR, Rebecca runs the full simulation locally.

## Explicitly prohibited actions

- No scoring runs, seed execution, or hold-out seed exposure
- No running of seeds 201–203 or 301–303 (O-14)
- No candidate output as input to the simulation (Ruling 9)
- No touching the verified estimator, 8 verified protocol items, candidate-blindness, R8 guard, or estimator validation
- No modification of the spec, constitution, STATE.md, or provenance_log.md
- No merging to main (Rebecca is sole merge authority)
- No L15/L16/L17 before M5
