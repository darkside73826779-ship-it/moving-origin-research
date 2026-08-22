# M4 post-tokenizer mutation-apparatus remediation quality trace

Date: 2026-08-22 EDT

Implementation commit: `6d4089ef95a14fb6b1d46c96ebf452733ff5cd98`

Production integration source remains byte-identical at raw SHA-256 `8964de5daf745226771818ab59f2cc75ef29ccbc5d09b43b6dae102b876b2f1b`.

## Requirement → apparatus branch → test → evidence

| Requirement | Executable apparatus branch | Apparatus-specific test or replay | Exact evidence |
|---|---|---|---|
| Exact target exists | `--probe-target` loads one fully qualified name; `_validate_common_probe` requires the exact discovered ID | `test_missing_target_is_instrument_failure`; canonical 15-mutant replay | Missing methods produce loader/discovery evidence and `INSTRUMENT_FAILURE`; all 15 contract targets name `RereviewRemediationTests` methods that exist. |
| Exact target is discovered and executed | `_suite_ids`, `probe_target`, and `_validate_common_probe` require `discovered_test_ids == [target]` and `tests_run == 1` | `test_probe_reports_exact_discovery_and_execution`; every baseline and mutant transcript row | Every committed row records one exact discovered ID and one execution for both unchanged and mutated source. |
| Unchanged baseline passes | `validate_baseline_probe` requires literal success with no failures, errors, skips, unexpected successes, loader errors, stdout, or stderr | `test_unchanged_baseline_must_pass`; 15 baseline transcript rows | All 15 unchanged baseline probes pass before mutation. A baseline assertion failure is classified as `INSTRUMENT_FAILURE`. |
| False code is temporary and custody-free | `execute` copies only public `src`, `tests`, `specs`, and `artifacts` into a temporary checkout; `restoration_guard` stages authenticated baseline bytes | canonical host and pinned-container replays | Mutations occur only beneath a disposable temporary root. No committed production source changes, private binding, custody, tokenizer/model data, or science is used. |
| KILLED requires the bound mutation-sensitive assertion | `classify_mutant_probe` accepts only assertion failures and requires the contract `expected_failure_regex` | `test_expected_assertion_is_killed`, `test_unrelated_assertion_is_instrument_failure`, `test_passing_mutant_is_survived_not_killed` | All 15 mutants are KILLED by their bound expected assertion text. A passing mutant is `SURVIVED`; an unrelated assertion is `INSTRUMENT_FAILURE`. |
| Discovery/import/syntax/environment/timeout/harness failures never count as kills | `run_probe`, `_validate_common_probe`, and `main` map nonzero probe processes, stderr, malformed/noncanonical JSON, loader errors, runtime errors, timeouts, and apparatus I/O to exit 2 | `test_error_is_never_a_kill`, `test_import_syntax_and_environment_errors_are_never_kills`, `test_harness_process_stderr_and_malformed_json_are_instrument_failures`, `test_timeout_is_instrument_failure` | The apparatus suite separately realizes every named class and proves none can produce `KILLED`. |
| Original source is restored byte-for-byte after every mutant | `restoration_guard` restores in `finally` and checks both byte equality and SHA-256 | `test_restoration_occurs_after_body_failure`; every transcript row carries identical baseline/restored SHA-256 | The authenticated production baseline SHA-256 is reproduced after every mutant, including a body failure. |
| Restoration or identity failure stops fail closed | baseline staging and final restoration wrap write/read errors and reject any byte or digest mismatch | `test_restoration_identity_failure_stops_fail_closed`, `test_restoration_write_failure_stops_fail_closed` | Corruption and restoration-write failure both produce `INSTRUMENT_FAILURE`; replay stops instead of recording a kill. |
| Exact commands and cross-runtime transcript are deterministic | contract validation binds the exact probe command; normalization removes only runtime root/interpreter spelling, slash form, timing, and Python caret-rendering lines | `test_contract_binds_exact_probe_command`, `test_normalization_removes_only_runtime_path_and_caret_rendering` | Windows fresh-checkout and pinned Linux OCI replay reproduce the same canonical transcript SHA-256 `f889582b8cabc1786729987b73f127dfa4b4db745a6bbca9439fcc74e3a99bce`. |

## Ordered execution and restoration trace

1. Authenticate the indexed canonical contract and indexed runner raw SHA-256.
2. Authenticate the indexed production baseline raw SHA-256.
3. Create a custody-free disposable checkout containing only committed public package trees.
4. Stage and re-hash the unchanged source.
5. Discover and execute the exact target once; require a clean baseline PASS.
6. Verify the exact old-code occurrence count, derive the predefined mutant bytes, and authenticate the mutant SHA-256.
7. Write only the disposable source and re-hash it.
8. Discover and execute the same exact target once.
9. Classify only the expected assertion failure as KILLED; map survival to exit 1 and every apparatus/unrelated failure to exit 2.
10. In `finally`, restore the original bytes and authenticate byte equality plus SHA-256 before continuing.

## Adversarial apparatus verification

- Exact discovery/execution, missing target, failed baseline, expected assertion, unrelated assertion, survivor, runtime error, import/syntax/environment errors, probe-process failure, stderr, malformed JSON, timeout, command drift, restoration after body failure, restoration corruption, restoration write failure, and cross-runtime normalization: 15/15 PASS.
- Deterministic predefined mutation replay: 15/15 KILLED; every baseline and mutant probe records the exact target and `tests_run=1`; every kill has assertion failures and zero errors.
- Raw combined inventory: 69/69 reproduced; governed sidecars: 27/27 preserved.

## Exact custody-free verification

- Fresh `core.autocrlf=true` checkout at the implementation commit: apparatus 15/15 PASS; mutation replay 15/15 KILLED; integration 49/49 PASS.
- Exact pinned WSL2-backed Linux/amd64 OCI image, `--pull=never`, network disabled, read-only checkout, all capabilities dropped, no-new-privileges, no custody: apparatus 15/15 PASS; mutation replay 15/15 KILLED with canonical transcript equality; integration 49/49 PASS; banked tokenizer suite 37/37 PASS.
- Mutation runner SHA-256: `9ec41f211bb3905dd4e30ca2c1d5573c889ea221320e5b2e7a3ecfa9d7542ac5`.
- Apparatus-test SHA-256: `469ba3d62c3d364488bb216f21228b7c09d5fc6f23e53c4339bf16226d6133ef`.
- Mutation contract SHA-256: `af5b660165a4c39922e23d3dfc79d61b015da3b696ee763aecf13d8e376b5367`.
- Mutation transcript SHA-256: `f889582b8cabc1786729987b73f127dfa4b4db745a6bbca9439fcc74e3a99bce`.
- Combined inventory SHA-256: `f4034166201fc57277657abfc44a5342b8e6c8b40dd1bf3ad627d7fb192c2cb5`.
- Launch-contract SHA-256: `f50080d221282d724f7fd5646fc9a7f4ca7fc12694dfc9eb29ded460d7825246`.
- `git diff --check` and `git fsck --full`: PASS; fsck reports only unreachable local development objects.
- Production integration source/test diff against input `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`: empty.
- Candidate/peer/model/tokenizer inference, tokenizer materialization, private custody, scoring, science, STATE/provenance mutation, merge, and publication: zero.
