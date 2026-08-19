# TASK BUILDER Handoff — Misspec Stress-Test Extension (NF-IMPL-4)

**To:** CRITIC (focused re-review of extended stress-test)
**From:** TASK BUILDER
**Date:** 2026-08-19
**Gate served:** NF-IMPL-4 scope extension — full 240-combo sensitivity map + deterministic selection on misspecified profiles
**Authoritative base:** `e26d05f` (GitHub main)
**Repository:** `darkside73826779-ship-it/moving-origin-research`

## Disposition

**EXTENSION COMPLETE — ready for CRITIC re-review.**

## SHAs

| Item | SHA | Status |
|---|---|---|
| Base (GitHub main) | `e26d05f` | Verified |
| Branch | `taskbuilder/l8-power-analysis` | Pushed to GitHub |
| Branch HEAD | `5343fc9` | Latest — includes full stress-test extension |
| Prior CRITIC-cleared HEAD | `61a2f8d` | Remediation (BF-IMPL-1 + NF-IMPL-1/2/3) |

## What was extended

### New function: `run_power_analysis_misspecified(profile_name, n_sims, ...)`

Mirrors `run_power_analysis` but uses `simulate_one_seed_misspecified` per seed:
- Full 240-combination grid (α × v × C_min × η)
- Both false-kill aggregations (5-seed mean + per-seed any-seed) [NF-IMPL-2]
- Null-control arm with σ_dose=0.0 under the same misspecified profile
- Sensitivity map (§8.7) aggregated across (α,v) pairs
- Deterministic selection rule (§8.8) via `select_cmin_eta` (unchanged)
- Reuses reference calibration `calibrate_sigma_dose(alpha, v_mult)` — tests estimator overfit, not re-calibration
- P3 source tags throughout: `[Sol-XF-9]`, `[PROPOSED — apparatus parameter, §8 item 9]`

### Replaced: `run_misspecification_stress_test(n_sims=10000, reference_selection=None)`

Full version replacing the partial 8-combo subset:
- Runs complete power analysis on each misspecified profile (uniform_difficulty, bimodal_difficulty)
- Reports selection stability vs reference: (C_min, η) match/mismatch
- Both false-kill aggregations reported on misspecified profiles
- Results included in `--full` JSON

### New CLI parameter: `--stress-test-sims N`

- Defaults to 10,000 (full, matching reference)
- Rebecca can reduce at runtime (e.g., `--stress-test-sims 2000` for ~8h total vs ~17h at full)

### Simulation count options flagged to Rebecca

- **Full 10,000 per combo** on misspecified profiles: ~17 hours total (reference + 2 misspecified). Most rigorous.
- **Reduced 2,000 per combo**: ~8 hours total. Stress-test is a stability check, not the headline sensitivity map.

## Verification

- Syntax: `ast.parse` OK
- Estimator validation: Example A β*=0.2111 (PASS), Example B β*=0.0045 (PASS) — unchanged
- `--help` shows new `--stress-test-sims` parameter
- `git diff` confirms: only `run_misspecification_stress_test` replaced, only new functions added, no protected functions modified

## What was NOT touched (all verified)

- The estimator (§2 XF-5) — unchanged
- `run_power_analysis` (reference-profile pipeline) — unchanged
- `select_cmin_eta` (deterministic selection rule) — unchanged
- `classify_region`, `min_distance_to_boundaries` — unchanged
- `beta_star_for_seed`, `run_level_beta_star`, `calibrate_sigma_dose`, `validate_estimator` — unchanged
- Candidate-blindness (Ruling 9) — no candidate-output path introduced
- R8 guard (`src/e1_experiment.py`) — unchanged
- NF-IMPL-1 (relative path), NF-IMPL-2 (per-seed false-kill), NF-IMPL-3 (regenerated table) — not reverted

## File summary

| File | Lines | Changes |
|---|---|---|
| `diagnostics/l8_power_analysis.py` | 1435 (was 1214) | +298/-77: full misspec pipeline, `--stress-test-sims`, stability report |

## Compliance

- §5 P3 source tags on all new parameters and functions
- Candidate-blind (Ruling 9, Entry 76) throughout
- O-15 (diagnostic-only): synthetic simulation, not scoring
- No locked bars changed
- No L15/L16/L17 before M5
- Public-repo policy: no private absolute paths

## Blockers

None.

## Next recipient

**CRITIC** — focused re-review of the extended stress-test. On CLEAR, Rebecca runs `python diagnostics/l8_power_analysis.py --full [--stress-test-sims N]` locally, producing the reference sensitivity map + misspecification stability report feeding her G2–G5 gate rulings.

## Explicitly prohibited actions

- No scoring runs, seed execution, or hold-out seed exposure
- No running of seeds 201–203 or 301–303 (O-14)
- No candidate output as input (Ruling 9)
- No touching the estimator, reference-profile pipeline, selection rule, R8 guard, or the three applied fixes
- No modification of the spec, constitution, STATE.md, or provenance_log.md
- No merging to main (Rebecca is sole merge authority)
- No L15/L16/L17 before M5
