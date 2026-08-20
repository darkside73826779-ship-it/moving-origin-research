# CRITIC Implementation Review — L8 Calibration Parallelism (Code vs Spec v1.2)

**Gate served:** CRITIC implementation review — does the code match the approved spec v1.2? Is the reproducibility genuine? Do all tests pass? Is protected logic preserved?
**Reviewer:** CRITIC (fresh-context, code review — the second pass on the calibration parallelism work)
**Date:** 2026-08-19 22:47 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — on CLEAR, Rebecca authorizes the local rerun.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Code branch | `taskbuilder/l8-power-analysis` |
| Implementation commit | `7934c85` |
| Final branch HEAD (with handoff) | `b139749` |
| Base (before implementation) | `7e296ec` |
| Delta reviewed | `7e296ec...b139749` — 5 files, +492/−10 |
| Approved spec v1.2 (the spec the code must match) | `specs/l8_calibration_parallelism_spec.md` at `6979378` on `architect/l8-calibration-parallelism-spec` |
| CRITIC v1.2 spec re-review (the CLEAR) | `reviews/critic_l8_calibration_parallelism_spec_v1.2_rereview.md` on `critic/l8-calibration-parallelism-spec-v1.2-rereview` (`e44d27b`) |
| TASK BUILDER handoff (implementation report) | `reviews/taskbuilder_l8_calibration_parallelism_handoff.md` |
| Reproducibility results | `diagnostics/l8_calibration_parallelism_results_2026-08-19.txt` |
| Test files | `tests/test_l8_calibration_parallelism.py` (8 methods); `tests/test_l8_multiprocessing.py` (2 methods) |

Read-only review. No code, spec, constitution, or scoring artifact modified (read-only + own review/handoff files). No scoring, seed execution, hold-out seed exposure, or unauthorized merge performed. The tests were inspected (not executed by the CRITIC); the TASK BUILDER's reported results were verified against the actual code and artifacts.

---

## Headline finding (CLEAR)

The implementation genuinely matches the approved spec v1.2. All six binding normative components are implemented verbatim; the serial calibration loops are removed from both analysis paths and replaced with `calibrations = _run_calibration_phase(...)` (worker results consumed); the simulation worker results are consumed via `zip(combo_results, null_results)` in both the reference and misspecified paths. **The prior BF-MP-1 defect (discarded worker results, vacuous reproducibility) is genuinely fixed** — the 2 regression tests verify single==multi on the actually-consumed output. Reproducibility is genuine (15 sigma_dose values byte-identical; artifact byte identity; downstream scientific equality; all True). All 10 tests (8 contract + 2 regression) are real, not no-ops. Protected logic is byte-for-byte unchanged. Pools are separate and sequential. The TASK BUILDER's claims are verified against the diff and the results.

---

## 1. Code matches spec v1.2 binding normative code — VERIFIED

All six components in `diagnostics/l8_power_analysis.py` match the spec's binding code exactly:

- **`CalibrationWorkerError`** (top-level, picklable, 5 fields, fixed message `"calibration worker failed"`, 5-arg `super().__init__`). ✓
- **`_worker_calibration`** (catches `Exception` only around `calibrate_sigma_dose`, raises `CalibrationWorkerError(...) from None` with `type(original).__name__` and the fixed message, returns the exact success record `{ordinal, alpha, v_mult, sigma_dose}`). ✓
- **`CalibrationIdentityError`** (top-level, picklable, fixed message `"calibration identity validation failed"`, fields `mismatch_kinds/expected_count/seen_count/canonical_identities/message`). ✓
- **`_emit_calibration_failure`** (exactly one `json.dumps(record, sort_keys=True)` line to `sys.stderr`, flush). ✓
- **`_validate_calibration_identities`** (duplicate/missing/unexpected + malformed-as-unexpected via `TypeError`/`KeyError`; raises `CalibrationIdentityError`). ✓
- **`_run_calibration_phase`** (canonical ordered work items; `min(workers or os.cpu_count() or 1, len(work_items))` cap = 15; dedicated context-managed pool; ordered `pool.map`; identity validation; both `CalibrationWorkerError` and `CalibrationIdentityError` caught with exact failure records; `SystemExit(1)`; returns the calibrations table on success). ✓

The TASK BUILDER did not alter the field set, the fixed message, the `from None`, or the `Exception`-only catch. ✓

---

## 2. The BF-MP-1 defect is genuinely FIXED (worker results consumed)

The prior BF-MP-1 BLOCK (at `3a8d9d9`) had: (a) the reference `run_power_analysis` not parallelized; (b) `run_power_analysis_misspecified` dispatching workers but discarding `combo_results` (the "Build results list" loop re-ran the simulation inline); (c) a vacuous reproducibility check. All three are fixed:

- **Serial calibration loops removed.** Both `run_power_analysis` (line 887: `calibrations = _run_calibration_phase("reference", workers)`) and `run_power_analysis_misspecified` (line 1234: `calibrations = _run_calibration_phase(f"misspec:{profile_name}", workers)`) now invoke the shared parallel calibration phase. The serial `for alpha in ALPHAS: for v_mult in V_MULTS: calibrations[...] = calibrate_sigma_dose(...)` loops are deleted from both paths. ✓
- **Calibration worker results consumed.** `_run_calibration_phase` returns `{(alpha, v_mult): sigma_dose for r in results}` built from the consumed `pool.map` output. ✓
- **Simulation worker results consumed.** Both `run_power_analysis` (line ~918: `for combo_result, null_result in zip(combo_results, null_results):`) and `run_power_analysis_misspecified` (line ~1266: `for done, (combo_result, null_result) in enumerate(zip(combo_results, null_results), start=1):`) build the results list from the actually-consumed worker output. The misspecified path's inline re-run is gone; the comment explicitly reads "Build results list from the actually-consumed worker output. pool.map is order-preserving." ✓
- **Reference now parallelized.** `run_power_analysis` has `workers=None` (line 869); `main` passes `workers=args.workers` to it (line 1541) and to `run_misspecification_stress_test` (line 1570). ✓

---

## 3. Reproducibility is genuine (not vacuous) — VERIFIED

`diagnostics/l8_calibration_parallelism_results_2026-08-19.txt` shows the actual reproducibility check, run on the consumed parallel output:

- Serial (`workers=1`) and parallel (`workers=15`) `sigma_dose` tables are printed for all 15 identities and are identical. ✓
- `calibration_value_equality: True` (15 `sigma_dose` values byte-identical between `workers=1` and `workers=15`). ✓
- `artifact_byte_identity_excluding_elapsed_seconds: True`. ✓
- `downstream_scientific_equality: True`. ✓
- **Honest "verifier correction" note:** the first verifier attempt compared raw Python structures and returned False because `NaN != NaN`, while the approved sanitized artifact-byte comparison was already True. The verifier was corrected to compare `_sanitize_nan`-normalized downstream structures exactly (no tolerance); the corrected run passed. This transparency is itself evidence the check is genuine and was actually run on the consumed output — not a vacuous pass. ✓

The reproducibility is run on the **actually-consumed** parallel calibration output (the `sigma_dose` values come from `_run_calibration_phase`, which consumes `pool.map` results). This is the BF-MP-1 failure mode's exact negation. ✓

---

## 4. The 10 tests pass and are genuine (not no-ops) — VERIFIED

`tests/test_l8_calibration_parallelism.py` (8 methods) + `tests/test_l8_multiprocessing.py` (2 methods) = 10 tests, matching the results txt "Ran 10 tests in 89.995 seconds, Result: OK." All are genuine with real assertions:

- `test_worker_error_pickle_round_trip` — `CalibrationWorkerError` survives `pickle.dumps/loads` with all 5 fields identical. ✓ (§6.1)
- `test_worker_failure_identity_type_fixed_message_and_no_leak` — worker failure carries correct `(ordinal, alpha, v_mult)`; `exception_type == "ValueError"`; `exception_message == "calibration worker failed"`; **HOSTILE input** (private Windows path, hostname, SID, email `@example.test`, fake token `ghp_FAKE_TOKEN`, newline) does NOT appear in `pickle.dumps(error)`. ✓ (§6.2, §6.3, §6.4, §6.5)
- `test_worker_failure_record_and_system_exit` — parent emits exactly the 7-field record to stderr; `SystemExit(1)` (code 1); HOSTILE absent from stderr; no "Traceback" in stderr; exactly one progress line. ✓ (§6.6, §6.7)
- `test_no_simulation_dispatch_after_calibration_failure` — after a calibration failure, `_worker_combo` and `_worker_null_control` are `assert_not_called()`. ✓ (§6.8)
- `test_identity_error_pickle_round_trip` — `CalibrationIdentityError` survives pickle with all fields. ✓ (§6.9)
- `test_duplicate_missing_unexpected_and_malformed_contracts` — 5 subTests covering duplicate, missing, unexpected, malformed-as-unexpected (non-dict `None`, missing keys, non-canonical values); asserts correct `mismatch_kinds`, `expected_count`, `seen_count`. ✓ (§6.9)
- `test_identity_failure_record_and_system_exit` — identity failure emits the 7-field record; `SystemExit(1)`; `mismatch_kinds == ["missing"]`; `seen_count == 14`. ✓ (§6.9)
- `test_dispatch_once_consume_once_and_worker_cap` — with `workers=64`, `FakePool.processes_seen == [15]` (cap applied: `min(64, 15) = 15`); table has 15 entries with all canonical identities. ✓ (dispatch-once/consume-once; §4.4 cap)
- `test_reference_consumed_output_is_identical` — `run_power_analysis` with `workers=1` vs `workers=2`; asserts `normalized_metrics(single) == normalized_metrics(multi)` on the **actually-consumed** output. ✓ (§6.10/§6.11 — the BF-MP-1 vacuous-reproducibility guard)
- `test_misspecified_consumed_output_is_identical` — same for `run_power_analysis_misspecified` (uniform_difficulty) with `workers=1` vs `workers=2`. ✓ (§6.10/§6.11 — guards the prior BF-MP-1 defect location)

The 2 regression tests use a `normalized_metrics` helper that maps `NaN` → `"NaN"` string (the "verifier correction"), so the comparison is exact without the `NaN != NaN` false-negative. The tests use `FakePool` to inject errors/malformed results deterministically — they are real, not no-ops. ✓

---

## 5. Multicore use confirmed — VERIFIED

The results txt reports: 16 Python processes (1 parent + 15 calibration workers) and 62% CPU sampled during the 15-worker calibration phase; classified `[PROPOSED — diagnostic implementation check]`, not a performance bar. This is the approved §4.10 process-observation check, not a numeric speedup bar. ✓

---

## 6. Protected logic preserved — VERIFIED

Diff `7e296ec...b139749` against `diagnostics/l8_power_analysis.py` adds only the six binding components (+`import sys`) and removes the two serial calibration loops (replaced with `_run_calibration_phase` calls). Grep confirms `calibrate_sigma_dose`, `combo_seed`, `beta_star_for_seed`, `select_cmin_eta` are NOT in the diff (byte-for-byte unchanged). The simulation workers (`_worker_combo`, `_worker_null_control`), `run_level_beta_star`, `simulate_one_seed`/`simulate_one_seed_misspecified`, `classify_region`, `min_distance_to_boundaries`, `validate_estimator`, the JSON write order, the R8 guard, the NF-IMPL-1/2/3 fixes, and the BF-MP-1 simulation multiprocessing are all unchanged. ✓

---

## 7. Pools separate and sequential — VERIFIED

`_run_calibration_phase` opens its own context-managed pool (`with multiprocessing.Pool(...) as pool:` at line 563), runs the 15 calibrations, closes/joins it (context-manager exit), and returns the calibrations table. Only then does the caller build simulation work items and open a **separate** simulation pool (`with multiprocessing.Pool(...) as pool:` at line 907 for reference; line 1256 for misspecified). Calibration pool closes before simulation pool opens — separate, sequential, no nested pools. ✓ Each analysis (reference and each misspecified profile) independently invokes the shared calibration phase (no cross-profile caching). ✓

---

## 8. Diff self-inspection genuine — VERIFIED

The TASK BUILDER's claimed diff self-inspection (serial loops removed; worker results consumed; identity validation before simulation work construction; failure field sets/fixed messages/`from None`/`Exception`-only catch/stderr sink/`SystemExit(1)` match spec) is borne out by the actual diff. ✓

---

## 9. Public-safety scan — clean (with one test-fixture note)

The implementation introduces no private absolute paths, credentials, secrets, machine identifiers, or PII in the production code. One note: `tests/test_l8_calibration_parallelism.py` contains a `HOSTILE` test fixture with a fake GitHub token (`ghp_FAKE_TOKEN`), a private Windows path (`C:\Users\private\secret.txt`), a SID (`S-1-5-21-123`), and an email (`person@example.test`). These are **intentional synthetic test inputs** used to verify the sanitization prevents leaks (the tests assert these do NOT appear in the pickled exception or stderr). They are clearly fake (`@example.test` domain, `ghp_FAKE_TOKEN` literal). A naive gitleaks scan might flag the token string, but it is a test fixture, not a real secret. Acceptable. No real secrets, no private paths in production code, no PII. ✓

---

## §5 compliance

- **P3 (source-class tags):** PASS — no new numeric parameters introduced by the implementation. The `SystemExit(1)` termination mechanism is tagged `[PROPOSED — diagnostic termination mechanism]` (carried from the spec). The fixed messages and exception classes are implementation mechanisms, not numeric thresholds; P3 does not require tags for them. ✓
- **Candidate-blind (Ruling 9):** preserved — the exception channel carries only apparatus-parameter identity (ordinal, alpha, v_mult) + the fixed public-safe messages `"calibration worker failed"` / `"calibration identity validation failed"`; `canonical_identities` are the frozen published synthetic `ALPHAS × V_MULTS` parameters. No candidate data crosses the channel. ✓
- **O-15 (diagnostic-only):** preserved — all verification is O-15 diagnostic-only; no scoring, no hold-out-seed exposure. ✓

---

## Non-blocking findings

- **NF-IMPL-CP-1 (trivial — handoff test-count label imprecise):** the COORDINATOR's review handoff labeled the tests as "8 failure-contract tests + 10 multiprocessing regression tests (14 verification-contract items)." The actual test files contain 8 contract methods + 2 regression methods = 10 tests total (matching the results txt "Ran 10 tests"). The "10 multiprocessing regression tests" should read "2." This is a labeling imprecision in the handoff, not a defect — the tests exist, are genuine, and pass. No action required.
- **NF-IMPL-CP-2 (trivial — test fixture contains fake-secret patterns):** the `HOSTILE` test fixture contains `ghp_FAKE_TOKEN`, a private Windows path, a SID, and an email. These are intentional synthetic inputs (clearly fake) used to verify sanitization prevents leaks. Not a real secret; flagged only so a future naive secret-scan doesn't false-positive on the test file. No action required.

---

## Preserved evidence

The implementation is additive to `7e296ec` (the functional BF-MP-1 remediation baseline): it adds the six binding components and replaces the serial calibration loops with parallel `_run_calibration_phase` calls. All protected scientific logic is byte-for-byte unchanged. The prior CRITIC CLEARs (v1 `a087654`; v1.1 `5a16485`; v1.2 `e44d27b`) and the BF-MP-1 BLOCK (`cade0c5`) findings remain valid. The implementation invalidates no prior evidence; it implements the approved spec v1.2 faithfully and resolves the BF-MP-1 discarded-results/vacuous-reproducibility defect.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, code/test-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. (The `HOSTILE` fixture contents referenced in NF-IMPL-CP-2 are quoted from the test file under review as a finding, not as the review's own content.) Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the code, spec, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No running of the full simulation (deferred to Rebecca's local run after authorization).
- No L15/L16/L17 before M5.
- No touching the calibration algorithm, `combo_seed`, estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, write-order fix, NF-IMPL-1/2/3 fixes, or BF-MP-1 simulation multiprocessing (all confirmed unchanged).

---

## Verdict and routing

**Verdict: CLEAR.** The implementation genuinely matches the approved spec v1.2: all six binding components are verbatim; the serial calibration loops are removed and worker results consumed (calibration via `_run_calibration_phase` return; simulation via `zip` in both paths). The prior BF-MP-1 defect (discarded results, vacuous reproducibility) is genuinely fixed — the 2 regression tests verify single==multi on the actually-consumed output. Reproducibility is genuine (15 sigma_dose byte-identical; artifact byte identity; downstream scientific equality; all True; honest verifier-correction note). All 10 tests (8 contract + 2 regression) are real, not no-ops. Multicore use confirmed (16 processes, 62% CPU, `[PROPOSED — diagnostic implementation check]`). Protected logic byte-for-byte unchanged. Pools separate and sequential. Candidate-blindness preserved. The TASK BUILDER's claims are verified against the diff and the results.

**Next authorized role:** WORKFLOW COORDINATOR → **Rebecca** (authorize the local rerun: `python diagnostics/l8_power_analysis.py --full --workers N [--stress-test-sims M]`), producing the complete artifact (reference sensitivity map + selection + misspecification stability report, both false-kill aggregations) feeding her G2–G5 gate rulings (G1 resolved by Entry 81). Rebecca should also rule on the NF-IMPL-2 false-kill aggregation (which is the G3-escalation input). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On BLOCK (not the case), returns to TASK BUILDER.

---

*This review was conducted read-only against the implementation at `b139749` on `taskbuilder/l8-power-analysis` and the approved spec at `6979378`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
