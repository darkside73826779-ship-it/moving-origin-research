# TASK BUILDER Handoff — L8 Calibration Parallelism v1.2

**Date:** 2026-08-19  
**Regime:** B  
**Gate served:** Implementation of the CRITIC-cleared, Rebecca-approved L8 calibration parallelism specification v1.2  
**Diagnostic posture:** O-15 diagnostic-only; synthetic/candidate-blind; no scoring

## Input SHAs reviewed

- Code base: `7e296ec`
- Approved specification v1.2: `6979378`
- Implementation result: `7934c854e840ded8423ba39f7ccda2bc2d2c4891`

## Files changed or created

- `diagnostics/l8_power_analysis.py`
- `diagnostics/l8_calibration_parallelism_check.py`
- `diagnostics/l8_calibration_parallelism_results_2026-08-19.txt`
- `tests/test_l8_calibration_parallelism.py`

## What was implemented

- Top-level, picklable `CalibrationWorkerError` with the exact five-field contract and fixed public-safe message.
- `_worker_calibration` with the binding `Exception`-only catch, fixed message, and `raise ... from None` behavior.
- Top-level, picklable `CalibrationIdentityError` with the fixed identity-failure contract.
- Exact stderr JSON-line `_emit_calibration_failure` sink.
- `_validate_calibration_identities` covering duplicate, missing, unexpected, and malformed results.
- Shared `_run_calibration_phase` boundary: canonical ordered work items, worker cap, dedicated calibration pool, ordered `pool.map`, identity validation, exact failure records, `SystemExit(1)`, and table return only after complete success.
- Both reference and misspecified analyses independently invoke the shared parallel calibration phase before constructing simulation work.
- No cross-profile caching and no nested pools.

## Genuine reproducibility results

The committed O-15 diagnostic computed all 15 calibration identities with one worker and 15 workers. Every `sigma_dose` value was exactly equal:

```text
(0.0,0.5)=1.3125890624999998  (0.0,1.0)=2.25008125  (0.0,2.0)=12.0
(0.02,0.5)=1.3125890624999998 (0.02,1.0)=3.000075 (0.02,2.0)=12.0
(0.05,0.5)=1.3125890624999998 (0.05,1.0)=3.000075 (0.05,2.0)=12.0
(0.1,0.5)=1.3125890624999998  (0.1,1.0)=3.000075  (0.1,2.0)=12.0
(0.2,0.5)=1.3125890624999998  (0.2,1.0)=3.000075  (0.2,2.0)=12.0
```

- Calibration value equality: PASS (`True`)
- Serialized artifact byte identity after `_sanitize_nan`, excluding only `header.elapsed_seconds`: PASS (`True`)
- Downstream scientific equality for results, sensitivity-map cells, and deterministic selection: PASS (`True`)

The first verifier attempt compared raw structures and returned a false inequality because Python defines `NaN != NaN`, while the approved sanitized artifact-byte comparison already passed. This verifier defect is retained in the diagnostic record. The verifier was corrected to compare `_sanitize_nan`-normalized structures exactly, without tolerance; the corrected run passed.

## Fourteen-point test contract

1. `CalibrationWorkerError` pickle round-trip: PASS.
2. Worker failure identity: PASS.
3. Original exception class name: PASS.
4. Fixed message under hostile input: PASS.
5. Original message absent from pickled exception/log/record: PASS.
6. Exact seven-field worker failure record and no traceback: PASS.
7. `SystemExit(1)` termination: PASS.
8. No simulation dispatch after calibration failure: PASS.
9. Duplicate/missing/unexpected/malformed identity contract, record, termination, and pickling: PASS.
10. Serial/parallel calibration values, artifact bytes, and downstream outputs: PASS.
11. Genuine consumed-table single-vs-multi diagnostic: PASS.
12. Protected-logic static/diff check: PASS.
13. Multicore observation: PASS — 16 Python processes observed (one parent plus 15 calibration workers); sampled CPU load was 62%. `[PROPOSED — diagnostic implementation check]`; no numeric performance bar applied.
14. No scoring or hold-out exposure: PASS.

Executable verification:

- Focused failure-contract suite: 8 tests passed.
- Combined new and prior multiprocessing suites: 10 tests passed in 89.995 seconds.
- `py_compile`: PASS.
- `git diff --check`: PASS.

## Diff self-inspection

Relevant post-edit lines were read. The complete diff was inspected. It shows the serial calibration loops removed from both analyses and replaced by the shared parallel boundary; calibration worker outputs are consumed; identity validation occurs before simulation work construction; failure identity, fixed messages, field sets, `from None`, `Exception`-only catch, stderr sink, and `SystemExit(1)` match the binding specification.

Confirmed unchanged against `7e296ec`: `calibrate_sigma_dose`, `combo_seed`, all per-simulation RNG derivations, estimator, both false-kill formulas, null-control calculation, sensitivity-map construction, deterministic selection rule, misspecified profiles, candidate-blindness, R8 guard, JSON write-order fix, NF-IMPL-1/2/3, and BF-MP-1 simulation multiprocessing.

## Public-safety scan

Public-safety scan: gitleaks staged-change scan plus regex/content review of all implementation files; zero new findings; cleared. A repository-wide scan reported one preserved historical match outside this change, not introduced or modified here. The synthetic hostile-input fixture is constructed without publishing a private path, email, token, or SID literal. No credentials, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII were added.

## Blockers

None.

## Exact next recipient role

CRITIC for implementation review against approved specification v1.2. Rebecca remains sole gate and merge authority.

## Explicitly prohibited actions

- No merge to `main`.
- No scoring, hold-out execution/exposure, or rerun of scoring seeds.
- No candidate output as input.
- No L15/L16/L17 before M5.
- No changes to locked bars, controls, scoring logic, protected scientific functions, spec, constitution, `STATE.md`, or provenance log.
