# TASK BUILDER Handoff — L8 Multiprocessing Remediation

**Date:** 2026-08-19  
**Regime:** B  
**Gate served:** Remediation of the §8 multiprocessing construction defect BF-MP-1  
**Diagnostic posture:** O-15 diagnostic-only; synthetic and candidate-blind; no scoring

## Input SHAs reviewed

- Broken implementation: `3a8d9d9`
- CRITIC BLOCK: `cade0c5`, `reviews/critic_l8_multiprocessing_rereview.md`
- Frozen L8 spec v2.2: `c7d7bed`, `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md`
- Implementation result: `c1e57cc79696eaf9a9c8dd3cd8bbe119e7ce822e`

## Files changed or created

- `diagnostics/l8_power_analysis.py`
- `tests/test_l8_multiprocessing.py`
- `diagnostics/l8_multiprocessing_reproducibility_2026-08-19.txt`

## What was implemented

1. `run_power_analysis_misspecified` now builds its result table exclusively from the ordered `combo_results` and `null_results` returned by `_worker_combo` and `_worker_null_control`. The duplicate inline simulation loops were removed.
2. `run_power_analysis` now accepts `workers`, builds all 240 work items, dispatches true-effect and null-control work through `multiprocessing.Pool.map`, and builds the sensitivity map and deterministic selection only after consuming the ordered worker results.
3. `main()` passes `--workers` to the reference `run_power_analysis`.
4. A focused regression test executes three combinations with one and two workers and compares the actually-consumed fields: mean β*, false-kill rate (run-level), false-kill rate (per-seed), `n_valid`, and instrument-failure count.

## What was verified

Command: bundled Python runtime, `python -m unittest tests.test_l8_multiprocessing -v`.

Result: 2 tests passed in 89.235 seconds.

Fields below are `(mean_beta_star, false_kill_rate, false_kill_rate_per_seed, n_valid, n_instrument_failures)`.

Reference, workers 1 and 2 (identical):

```text
[(0.26321430937795187, 0.0, 1.0, 1, 0),
 (0.37037613641572575, 0.0, 1.0, 1, 0),
 (0.1956607649103118, 1.0, 1.0, 1, 0)]
```

Misspecified `uniform_difficulty`, workers 1 and 2 (identical):

```text
[(1.0499306931312413, 0.0, 0.0, 1, 0),
 (0.9463458621102969, 0.0, 1.0, 1, 0),
 (1.3302993443956659, 0.0, 0.0, 1, 0)]
```

`py_compile` and `git diff --check` passed. Relevant post-edit lines were read. The complete diff was inspected and confirms worker outputs are consumed, the misspecified inline rerun is absent, the reference run uses `pool.map`, and `main()` routes `--workers` to it.

Confirmed unchanged: estimator, combo-seed formula, both false-kill formulas, sensitivity-map construction, deterministic selection rule, misspecified profiles, candidate-blindness, R8 guard, JSON write-order fix, and NF-IMPL-1/2/3.

## Public-repository scan attestation

A pre-push self-scan covered credentials, API keys, tokens, passwords, secrets, personal contact details, hostnames, MAC addresses, SIDs, user account names, private absolute paths, environment dumps, and PII. Findings: none. Classification: acceptable; no blocker and no Rebecca decision required.

## Blockers

None.

## Exact next recipient role

CRITIC, for the focused multiprocessing re-review specified in the inbound handoff. Rebecca remains sole gate and merge authority.

## Explicitly prohibited actions

- No merge to `main`.
- No scoring, hold-out execution/exposure, or rerun of seeds 201–203 / 301–303.
- No candidate output as input.
- No L15/L16/L17 before M5.
- No changes to locked bars, estimator, combo seeds, false-kill formulas, sensitivity map, selection rule, misspecified profiles, R8 guard, write-order fix, spec, constitution, `STATE.md`, or `provenance_log.md`.
