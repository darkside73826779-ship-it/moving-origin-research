# TASK BUILDER Handoff — Multiprocessing + Write-Order Fix

**To:** CRITIC (focused re-review)
**From:** TASK BUILDER
**Date:** 2026-08-19
**Gate served:** §8 power analysis remediation — (1) CPU parallelism; (2) JSON write-order fix
**Authoritative base:** `e26d05f` (GitHub main)
**Repository:** `darkside73826779-ship-it/moving-origin-research`

## Disposition

**BOTH FIXES COMPLETE — ready for CRITIC re-review.**

## SHAs

| Item | SHA | Status |
|---|---|---|
| Base (GitHub main) | `e26d05f` | Verified |
| Branch | `taskbuilder/l8-power-analysis` | Pushed to GitHub |
| Branch HEAD | `fd5d5c1` | Latest — includes multiprocessing + write-order fix |
| Prior HEAD (CRITIC-cleared stress-test extension) | `cbe4dfb` | |

## Fix 1: CPU parallelism

### Implementation
- **`_worker_combo(args)`** — module-level worker function: runs one (combo, profile) pair independently. Takes (alpha, v_mult, c_min, eta, sigma_dose, n_sims, base_seed, profile_name). Returns per-combo result dict with mean β*, std, both false-kill rates, instrument-failure count.
- **`_worker_null_control(args)`** — module-level worker for null-control arm (σ_dose=0.0).
- **`run_power_analysis`** — pre-calibrates σ_dose for all 15 (α,v) pairs, then builds 240 work items, runs `multiprocessing.Pool(processes=N).map()`, collects results by combo-identity (sorted, not completion order).
- **`run_power_analysis_misspecified`** — same parallel approach, each work item includes the misspecified profile name.
- **`--workers N`** CLI parameter — defaults to `os.cpu_count()`. Set to 1 for single-threaded (reproducibility verification). Scalable to any core count.

### Deterministic-seed / reproducibility
- Each worker creates its own `np.random.Generator` from the combo seed — no shared RNG state.
- Combo seeds are `combo_seed(alpha, v, c, eta) = SHA-256(combo_string) mod 2^31` — deterministic, derived only from parameter combo, not worker/core.
- Results collected by combo-identity (dict/sorted), not completion order.
- No shared mutable arrays — workers return immutable result dicts.

### Reproducibility verification (performed by TASK BUILDER)
- Ran 3 representative combos with 10 sims each, single-threaded (`--workers 1`).
- Ran same 3 combos with 2 workers (`multiprocessing.Pool(2)`).
- Compared per-combo results: mean β*, false-kill (both aggregations), n_valid, instrument-failure count.
- **Result: byte-identical. Reproducibility: PASS.**

## Fix 2: JSON write-order

### Defect
The JSON was written before Step 4 (misspecification stress-test). Step 4 computed results in memory and attached them to the `full` dict, but the JSON file on disk was never rewritten.

### Fix
Moved `json.dump` to after Step 4 completes. The JSON now contains:
- Reference sensitivity map + selection + false-kill rates (both aggregations)
- Full misspecification stress-test results: sensitivity maps, selections, stability reports for both misspecified profiles

## What was NOT touched

- The estimator (§2 XF-5) — unchanged
- Combo seeds — unchanged (same formula)
- False-kill formulas (both aggregations) — unchanged
- Sensitivity map construction — unchanged
- Deterministic selection rule — unchanged
- Misspecified profiles (uniform, bimodal) — unchanged
- Candidate-blindness (Ruling 9) — no candidate-output path; parallelism introduces no candidate path
- R8 guard (`src/e1_experiment.py`) — unchanged
- NF-IMPL-1 (relative path), NF-IMPL-2 (per-seed false-kill), NF-IMPL-3 (regenerated table) — not reverted

## Diff self-inspection
- `git diff cbe4dfb..fd5d5c1` shows: +174/-13 lines in `diagnostics/l8_power_analysis.py` only
- No changes to `src/e1_experiment.py` or any other file
- Changes are: new `_worker_combo`/`_worker_null_control` functions, `multiprocessing` import, `--workers` CLI arg, parallelized loops in `run_power_analysis` and `run_power_analysis_misspecified`, JSON write moved to end of `main()`

## Compliance

- §5 P3 source tags: `[PROPOSED -- apparatus parameter, scalable parallelism]`
- Candidate-blind (Ruling 9): parallelism introduces no candidate-output path
- O-15 (diagnostic-only): synthetic simulation, not scoring
- No locked bars changed
- No L15/L16/L17 before M5
- Public-repo policy: no private absolute paths (NF-IMPL-1 fix preserved)

## File summary

| File | Lines | Changes |
|---|---|---|
| `diagnostics/l8_power_analysis.py` | 1596 (was 1435) | +174/-13: worker functions, multiprocessing, write-order fix |

## Next recipient

**CRITIC** — focused re-review of multiprocessing (reproducibility, no non-determinism, scalability) + write-order fix. On CLEAR, Rebecca reruns locally: `python diagnostics/l8_power_analysis.py --full --workers N [--stress-test-sims M]`.

## Explicitly prohibited actions

- No scoring, seed execution, or hold-out seed exposure
- No running of seeds 201–203 or 301–303 (O-14)
- No candidate output as input (Ruling 9)
- No touching the estimator, combo seeds, false-kill formulas, sensitivity map, selection rule, misspecified profiles, or R8 guard
- No changing deterministic seeds or introducing non-determinism
- No merging to main (Rebecca is sole merge authority)
- No L15/L16/L17 before M5
