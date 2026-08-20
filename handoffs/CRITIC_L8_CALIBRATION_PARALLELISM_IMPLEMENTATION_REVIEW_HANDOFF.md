# CRITIC Handoff — Return to WORKFLOW COORDINATOR: L8 Calibration Parallelism Implementation Review

**From:** CRITIC (fresh-context, code review — the second pass on the calibration parallelism work)
**To:** WORKFLOW COORDINATOR
**Date:** 2026-08-19 22:47 EDT
**Gate served:** CRITIC implementation review — does the code match the approved spec v1.2? Is the reproducibility genuine? Do all tests pass? Is protected logic preserved?
**Verdict:** **CLEAR**
**Review artifact:** `reviews/critic_l8_calibration_parallelism_implementation_review.md` on `critic/l8-calibration-parallelism-implementation-review` (SHA below)

---

## Authorization context

The TASK BUILDER (local frontier GPT) implemented the approved calibration parallelism spec v1.2 (`6979378`) at `7934c85`, branch HEAD `b139749` on `taskbuilder/l8-power-analysis`, base `7e296ec`. The TASK BUILDER reports all verification passed. This handoff returns the CRITIC's code review (the second pass) — verifying the claims against the actual diff and results, not just accepting the attestation.

---

## SHAs reviewed

| Item | Value |
|---|---|
| Code branch | `taskbuilder/l8-power-analysis` |
| Implementation commit | `7934c85` |
| Final branch HEAD (with handoff) | `b139749` |
| Base (before implementation) | `7e296ec` |
| Delta reviewed | `7e296ec...b139749` — 5 files, +492/−10 |
| Approved spec v1.2 (the spec the code must match) | `specs/l8_calibration_parallelism_spec.md` at `6979378` on `architect/l8-calibration-parallelism-spec` |
| CRITIC v1.2 spec re-review (the CLEAR) | `reviews/critic_l8_calibration_parallelism_spec_v1.2_rereview.md` on `critic/l8-calibration-parallelism-spec-v1.2-rereview` (`e44d27b`) |
| Reproducibility results | `diagnostics/l8_calibration_parallelism_results_2026-08-19.txt` |
| Test files | `tests/test_l8_calibration_parallelism.py` (8 methods); `tests/test_l8_multiprocessing.py` (2 methods) |

---

## Verdict: CLEAR

The implementation genuinely matches the approved spec v1.2. All six binding normative components are implemented verbatim; the serial calibration loops are removed from both analysis paths and replaced with `calibrations = _run_calibration_phase(...)` (worker results consumed); the simulation worker results are consumed via `zip(combo_results, null_results)` in both the reference and misspecified paths. **The prior BF-MP-1 defect (discarded worker results, vacuous reproducibility) is genuinely fixed** — the 2 regression tests verify single==multi on the actually-consumed output. Reproducibility is genuine. All 10 tests are real, not no-ops. Protected logic is byte-for-byte unchanged. Pools are separate and sequential. The TASK BUILDER's claims are verified against the diff and the results.

---

## The BF-MP-1 defect is genuinely FIXED

The prior BF-MP-1 BLOCK (at `3a8d9d9`) had: (a) reference `run_power_analysis` not parallelized; (b) `run_power_analysis_misspecified` discarding `combo_results` (inline re-run); (c) vacuous reproducibility. All three fixed:

- **Serial calibration loops removed.** Both `run_power_analysis` (line 887) and `run_power_analysis_misspecified` (line 1234) now invoke the shared parallel calibration phase `_run_calibration_phase`. The serial loops are deleted from both paths.
- **Calibration worker results consumed.** `_run_calibration_phase` returns `{(alpha, v_mult): sigma_dose}` built from the consumed `pool.map` output.
- **Simulation worker results consumed.** Both `run_power_analysis` (line ~918) and `run_power_analysis_misspecified` (line ~1266) build the results list from the actually-consumed worker output via `zip(combo_results, null_results)`. The misspecified path's inline re-run is gone; the comment explicitly reads "Build results list from the actually-consumed worker output. pool.map is order-preserving."
- **Reference now parallelized.** `run_power_analysis` has `workers=None` (line 869); `main` passes `workers=args.workers` to it (line 1541) and to `run_misspecification_stress_test` (line 1570).

---

## 1. Code matches spec v1.2 binding normative code — VERIFIED

All six components in `diagnostics/l8_power_analysis.py` match the spec's binding code exactly: `CalibrationWorkerError` (top-level picklable, 5 fields, fixed message `"calibration worker failed"`, 5-arg super); `_worker_calibration` (Exception-only catch, `from None`, fixed message, exact success record); `CalibrationIdentityError` (top-level picklable, fixed message `"calibration identity validation failed"`); `_emit_calibration_failure` (one sorted JSON line to stderr, flush); `_validate_calibration_identities` (duplicate/missing/unexpected + malformed-as-unexpected via TypeError/KeyError; raises CalibrationIdentityError); `_run_calibration_phase` (canonical ordered work, min(workers, 15) cap, dedicated context-managed pool, ordered pool.map, identity validation, exact failure records for both exceptions, SystemExit(1), returns table on success). The TASK BUILDER did not alter the field set, the fixed message, the `from None`, or the Exception-only catch.

---

## 2. Reproducibility is genuine (not vacuous) — VERIFIED

`diagnostics/l8_calibration_parallelism_results_2026-08-19.txt` shows the actual reproducibility check, run on the consumed parallel output:

- Serial (`workers=1`) and parallel (`workers=15`) `sigma_dose` tables printed for all 15 identities and identical.
- `calibration_value_equality: True` (15 sigma_dose byte-identical).
- `artifact_byte_identity_excluding_elapsed_seconds: True`.
- `downstream_scientific_equality: True`.
- **Honest "verifier correction" note:** the first verifier attempt compared raw Python structures and returned False because `NaN != NaN`, while the approved sanitized artifact-byte comparison was already True. The verifier was corrected to compare `_sanitize_nan`-normalized downstream structures exactly (no tolerance); the corrected run passed. This transparency is itself evidence the check is genuine and was actually run on the consumed output — not a vacuous pass.

The reproducibility is run on the **actually-consumed** parallel calibration output (sigma_dose values come from `_run_calibration_phase`, which consumes `pool.map` results). This is the BF-MP-1 failure mode's exact negation.

---

## 3. The 10 tests pass and are genuine (not no-ops) — VERIFIED

`tests/test_l8_calibration_parallelism.py` (8 methods) + `tests/test_l8_multiprocessing.py` (2 methods) = 10 tests, matching the results txt "Ran 10 tests in 89.995 seconds, Result: OK." All genuine with real assertions:

- `test_worker_error_pickle_round_trip` — CalibrationWorkerError survives pickle with 5 fields. ✓
- `test_worker_failure_identity_type_fixed_message_and_no_leak` — correct identity; `exception_type == "ValueError"`; `exception_message == "calibration worker failed"`; **HOSTILE input** (private Windows path, hostname, SID, email `@example.test`, fake token `ghp_FAKE_TOKEN`, newline) absent from `pickle.dumps(error)`. ✓
- `test_worker_failure_record_and_system_exit` — 7-field record to stderr; `SystemExit(1)`; HOSTILE absent; no "Traceback". ✓
- `test_no_simulation_dispatch_after_calibration_failure` — after calibration failure, `_worker_combo`/`_worker_null_control` `assert_not_called()`. ✓
- `test_identity_error_pickle_round_trip` — CalibrationIdentityError survives pickle. ✓
- `test_duplicate_missing_unexpected_and_malformed_contracts` — 5 subTests (duplicate, missing, unexpected, malformed-as-unexpected); correct `mismatch_kinds`/`expected_count`/`seen_count`. ✓
- `test_identity_failure_record_and_system_exit` — 7-field identity record; `SystemExit(1)`; `mismatch_kinds == ["missing"]`; `seen_count == 14`. ✓
- `test_dispatch_once_consume_once_and_worker_cap` — with `workers=64`, `FakePool.processes_seen == [15]` (cap `min(64,15)=15`); table has 15 canonical identities. ✓
- `test_reference_consumed_output_is_identical` — `run_power_analysis` `workers=1` vs `workers=2`; `normalized_metrics(single) == normalized_metrics(multi)` on the **actually-consumed** output. ✓ (BF-MP-1 vacuous-reproducibility guard)
- `test_misspecified_consumed_output_is_identical` — same for `run_power_analysis_misspecified` (uniform_difficulty). ✓ (guards the prior BF-MP-1 defect location)

The 2 regression tests use a `normalized_metrics` helper that maps `NaN` → `"NaN"` string (the "verifier correction"), so the comparison is exact without the `NaN != NaN` false-negative. Tests use `FakePool` to inject errors/malformed results deterministically — real, not no-ops.

---

## 4. Multicore use confirmed — VERIFIED

Results txt: 16 Python processes (1 parent + 15 calibration workers), 62% CPU during the 15-worker calibration phase; classified `[PROPOSED — diagnostic implementation check]`, not a performance bar. This is the approved §4.10 process-observation check.

---

## 5. Protected logic preserved — VERIFIED

Diff `7e296ec...b139749` against `diagnostics/l8_power_analysis.py` adds only the six binding components (+`import sys`) and removes the two serial calibration loops (replaced with `_run_calibration_phase` calls). Grep confirms `calibrate_sigma_dose`, `combo_seed`, `beta_star_for_seed`, `select_cmin_eta` are NOT in the diff (byte-for-byte unchanged). The simulation workers (`_worker_combo`, `_worker_null_control`), `run_level_beta_star`, `simulate_one_seed`/`simulate_one_seed_misspecified`, `classify_region`, `min_distance_to_boundaries`, `validate_estimator`, the JSON write order, the R8 guard, the NF-IMPL-1/2/3 fixes, and the BF-MP-1 simulation multiprocessing are all unchanged.

---

## 6. Pools separate and sequential — VERIFIED

`_run_calibration_phase` opens its own context-managed pool (line 563), runs the 15 calibrations, closes/joins it (context-manager exit), and returns the calibrations table. Only then does the caller build simulation work items and open a **separate** simulation pool (line 907 reference; line 1256 misspecified). Calibration pool closes before simulation pool opens — separate, sequential, no nested pools. Each analysis independently invokes the shared calibration phase (no cross-profile caching).

---

## 7. Diff self-inspection genuine — VERIFIED

The TASK BUILDER's claimed diff self-inspection (serial loops removed; worker results consumed; identity validation before simulation work construction; failure field sets/fixed messages/`from None`/`Exception`-only catch/stderr sink/`SystemExit(1)` match spec) is borne out by the actual diff.

---

## 8. Public-safety scan — clean (with one test-fixture note)

No private absolute paths, credentials, secrets, machine identifiers, or PII in the production code. One note: `tests/test_l8_calibration_parallelism.py` contains a `HOSTILE` test fixture with a fake token (`ghp_FAKE_TOKEN`), private Windows path, SID, and email (`@example.test`). These are **intentional synthetic test inputs** used to verify sanitization prevents leaks (the tests assert these do NOT appear in the pickled exception or stderr). Clearly fake. A naive gitleaks scan might flag the token string, but it is a test fixture, not a real secret. Acceptable.

---

## §5 compliance

- **P3:** PASS — no new numeric parameters introduced by the implementation. `SystemExit(1)` tagged `[PROPOSED — diagnostic termination mechanism]` (carried from spec). Fixed messages and exception classes are implementation mechanisms, not numeric thresholds; P3 doesn't require tags for them.
- **Candidate-blind (Ruling 9):** preserved — exception channel carries only apparatus-parameter identity (ordinal, alpha, v_mult) + fixed public-safe messages; `canonical_identities` are frozen published synthetic `ALPHAS × V_MULTS` parameters. No candidate data crosses the channel.
- **O-15 (diagnostic-only):** preserved — all verification O-15 diagnostic-only; no scoring, no hold-out-seed exposure.

---

## Non-blocking findings

- **NF-IMPL-CP-1 (trivial — handoff test-count label imprecise):** the COORDINATOR's review handoff labeled the tests as "8 failure-contract tests + 10 multiprocessing regression tests (14 verification-contract items)." The actual test files contain 8 contract methods + 2 regression methods = 10 tests total (matching the results txt "Ran 10 tests"). The "10 multiprocessing regression tests" should read "2." Labeling imprecision in the handoff, not a defect — the tests exist, are genuine, and pass. No action required.
- **NF-IMPL-CP-2 (trivial — test fixture contains fake-secret patterns):** the `HOSTILE` test fixture contains `ghp_FAKE_TOKEN`, a private Windows path, a SID, and an email. These are intentional synthetic inputs (clearly fake) used to verify sanitization prevents leaks. Not a real secret; flagged only so a future naive secret-scan doesn't false-positive on the test file. No action required.

---

## Preserved evidence

The implementation is additive to `7e296ec` (the functional BF-MP-1 remediation baseline): adds the six binding components and replaces the serial calibration loops with parallel `_run_calibration_phase` calls. All protected scientific logic byte-for-byte unchanged. Prior CRITIC CLEARs (v1 `a087654`; v1.1 `5a16485`; v1.2 `e44d27b`) and the BF-MP-1 BLOCK (`cade0c5`) findings remain valid. The implementation invalidates no prior evidence; it implements the approved spec v1.2 faithfully and resolves the BF-MP-1 discarded-results/vacuous-reproducibility defect.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this handoff artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, code/test-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the code, spec, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No running of the full simulation (deferred to Rebecca's local run after authorization).
- No L15/L16/L17 before M5.
- No touching the calibration algorithm, `combo_seed`, estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, write-order fix, NF-IMPL-1/2/3 fixes, or BF-MP-1 simulation multiprocessing (all confirmed unchanged).

---

## Next authorized role / routing

**Next recipient:** WORKFLOW COORDINATOR → **Rebecca** (authorize the local rerun: `python diagnostics/l8_power_analysis.py --full --workers N [--stress-test-sims M]`), producing the complete artifact (reference sensitivity map + selection + misspecification stability report, both false-kill aggregations) feeding her G2–G5 gate rulings (G1 resolved by Entry 81). Rebecca should also rule on the NF-IMPL-2 false-kill aggregation (which is the G3-escalation input). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On CLEAR (this case), Rebecca authorizes the local rerun. On BLOCK, returns to TASK BUILDER.

---

*This handoff was produced read-only against the implementation at `b139749` on `taskbuilder/l8-power-analysis` and the approved spec at `6979378`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
