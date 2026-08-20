# L8 §8 Calibration Parallelism Spec — Changelog

**Spec:** `specs/l8_calibration_parallelism_spec.md`
**Date:** 2026-08-19 · **Author:** ARCHITECT
**Branch:** `architect/l8-calibration-parallelism-spec` (from `7e296ec` on `taskbuilder/l8-power-analysis`)
**Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)

---

## v1.2 — Close failure-path determinism gaps (2026-08-19)

**Base:** advances from v1.1 (`b4419f9`) on `architect/l8-calibration-parallelism-spec`. No rebase; same branch.

**Gaps found by the TASK BUILDER (third stop, not implemented):** v1.1 left three failure-path mechanisms under-specified, so the TASK BUILDER would have had to invent rules. v1.2 closes all three in one pass so the spec leaves the TASK BUILDER nothing to infer.

### Gap 1 — Error sanitization made deterministic

`exception_message` is now fixed at exactly `"calibration worker failed"`; `exception_type` = `type(original).__name__`. The worker catches `Exception` only (not `BaseException`) and raises `CalibrationWorkerError(...) from None`. The original exception's message, `repr`, traceback, `__cause__`, `__context__`, `args`, and object are never stored, serialized, logged, or attached. No regex sanitizer or redaction rule is permitted. Rationale: task identity is already carried by `ordinal`/`alpha`/`v_mult`; a fixed message is deterministic, picklable, JSON-safe, and platform-independent; a regex sanitizer would need its own spec and could still have omissions.

### Gap 2 — Termination mechanism named

The parent raises `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]` immediately after emitting the failure record. It is the sole non-zero termination mechanism; no alternate exit code, return, or exception is permitted.

### Gap 3 — Identity-validation failure contract specified

A new top-level picklable `CalibrationIdentityError` (fixed message `"calibration identity validation failed"`) is the sole contract for identity-validation failures, raised by `_validate_calibration_identities`. The identity failure record has exactly seven fields (`phase`, `analysis_label`, `message`, `mismatch_kinds`, `expected_count`, `seen_count`, `canonical_identities`). `mismatch_kinds` is a sorted list (subset of `["duplicate","missing","unexpected"]` in that fixed order) because duplicate/missing/unexpected may co-occur. `canonical_identities` are the frozen, already-published synthetic apparatus parameters `ALPHAS × V_MULTS` (`[PROPOSED — apparatus parameter, §8]`) — public-safe, not candidate data (Ruling 9); raw returned records and raw unexpected values are NOT logged. `seen_count` is the number of returned result records (not unique identities), so duplicates are visible (15 canonical + 1 duplicate → `seen_count` = 16). Malformed returned records (non-dict, missing `alpha`/`v_mult`, or non-canonical values) are treated as `unexpected` (caught via `TypeError`/`KeyError` around key extraction) and never logged raw. `CalibrationIdentityError` passes all four data fields plus the fixed message to `Exception.__init__` so it survives `pickle.dumps`/`pickle.loads` with fields preserved.

### Parent boundary + normative code

A shared `_run_calibration_phase(analysis_label, workers) -> dict` is the parent-owned failure boundary used by the reference and each misspecified analysis: it builds the work list, opens the calibration pool, calls `pool.map(_worker_calibration, work_items)`, validates identities, catches `(CalibrationWorkerError, CalibrationIdentityError)`, emits the corresponding failure record (one JSON line to `sys.stderr` via `json.dumps(record, sort_keys=True)`), and raises `SystemExit(1)`; returns the table only on full success. Normative code blocks for `CalibrationWorkerError` + `_worker_calibration` (§4.2.1) and `CalibrationIdentityError` + `_validate_calibration_identities` + `_run_calibration_phase` + `_emit_calibration_failure` (§4.2.2) are binding — the TASK BUILDER may not alter the field set, fixed messages, `from None`, `Exception`-only catches, `SystemExit(1)` termination, or the stderr JSON sink.

### Implementation trace (new §4.2.3)

A trace table is added for every failure path (worker exception, identity validation, partial-result prevention, termination): input-identity location, object crossing the process boundary, picklability under spawn, exact text reaching logs, parent exception/exit, partial-results-to-simulation prevention point, and the unit-test assertion contract.

### Test contract (§6 expanded to 14 items)

The 10 TASK BUILDER failure-path tests are adopted (pickle round-trip; worker-failure identity; `exception_type`; fixed message under hostile input; original message absent; 7-field record; `SystemExit(1)` termination; no simulation after failure; `CalibrationIdentityError` contract; happy-path equality) plus the v1.1 reproducibility/protected-logic/process-observation/no-scoring items.

### Mechanisms chosen

- Fixed worker message: `"calibration worker failed"`.
- Termination type: `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]`.
- Identity-error class: top-level picklable `CalibrationIdentityError` (fixed message `"calibration identity validation failed"`).
- Logging sink: one JSON line to `sys.stderr` via `json.dumps(record, sort_keys=True) + "\n"` then `sys.stderr.flush()`.

### Preserved

- **No-retry (O-14):** identity is carried by the exception; no re-execution to discover failure identity.
- **Fail-closed:** first exception terminates; completed results discarded; no partial calibration table; no simulation after calibration failure.
- **Calibration algorithm, combo seeds, estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, R8 guard, write-order fix, three NF-IMPL fixes, BF-MP-1 multiprocessing, 15-element domain, `pool.map` dispatch:** unchanged.
- **Candidate-blindness (Ruling 9):** the exception/failure-record channel carries only apparatus-parameter identity + fixed public-safe messages + frozen canonical identities; no candidate data.
- **Reproducibility (§4.9):** unaffected — happy path unchanged.

### New parameters introduced

No new scientific apparatus parameters or performance bars. New `[PROPOSED]`-tagged diagnostic implementation criteria: the `SystemExit(1)` termination mechanism `[PROPOSED — diagnostic termination mechanism]` (joining the v1 cap and process-observation check). `expected_count`/`seen_count` are diagnostic record fields derived from the frozen calibration domain, not thresholds or bars. P3 unchanged.

### §5 P1–P6

- P1/P2: PASS — no new law text; existing verbatim quotes retained.
- P3: PASS — no new scientific parameters; `SystemExit(1)` tagged `[PROPOSED — diagnostic termination mechanism]`; `expected_count`/`seen_count` are diagnostic fields not bars.
- P4: PASS — header states 2026-08-19, Regime B.
- P5: N/A — no deviation from `[LAW]` text.
- P6: PASS — citations unchanged.

### Pre-push scan attestation

A pre-push self-scan was performed on the amended content before commit. Scanned for credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, and PII. **Findings:** none — only descriptive attestation/sanitization prose matched (the words "hostnames"/"MAC addresses"/"private absolute path" inside the spec's own sanitization rules and the changelog's attestation paragraph). No actual hostnames, private paths, secrets, or PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## v1.1 — §4.1/§4.2 contradiction resolution (2026-08-19)

**Base:** advances from v1 (`90d8835`) on `architect/l8-calibration-parallelism-spec`. No rebase; same branch.

**Contradiction found by the TASK BUILDER (stop, not implemented):** §4.1 required `_worker_calibration` to let exceptions propagate without catching, while §4.2 required the parent to emit a failure record carrying the failed task's `ordinal`/`alpha`/`v_mult`. These are incompatible under plain `multiprocessing.Pool.map`, which propagates a worker exception to the parent but does not give the parent the failed input tuple — so the parent could not identify which work item failed without re-executing (forbidden by O-14).

**Resolution chosen: Option 1 (identity-carrying exception, narrowly wrapped and re-raised).** Rationale: it is the most constraint-preserving — `pool.map` remains the dispatch mechanism, failure stays exception-driven and fail-closed, no retry/re-execution is needed to discover identity, no partial calibration table is usable, and it is a surgical amendment rather than a dispatch redesign. Option 2 (result-or-error protocol) was rejected as a larger worker-protocol change that waits for all calibrations to finish before parent-side failure handling; Option 3 (nullable identity) was rejected as weakening the failure record.

### Amendments applied

- **§4.1 (Exceptions):** amended from "must NOT catch exceptions" to permit narrow wrap-and-re-raise. The worker MUST catch exceptions **only** around the `calibrate_sigma_dose(alpha, v_mult)` call and **only** to re-raise a top-level, picklable **`CalibrationWorkerError`** carrying the failed task's identity and a sanitized error descriptor. It MUST NOT swallow, MUST NOT return a result / `sigma_dose` on failure, MUST NOT convert the exception into a usable calibration result, and MUST NOT retry.
- **§4.2 (Failure record):** amended so the parent sources `ordinal`, `alpha`, `v_mult`, `exception_type`, and `exception_message` from the propagated `CalibrationWorkerError` object — not from `repr(e)`, traceback text, or re-execution. The parent catches `CalibrationWorkerError` solely to emit the sanitized failure record and terminate fail-closed (non-zero); it must not produce a calibration result, must not log traceback text, and must not retry or infer identity by re-execution.
- **§4.2.1 (new):** `CalibrationWorkerError` contract — top-level picklable exception class (name fixed), constructor `CalibrationWorkerError(ordinal, alpha, v_mult, exception_type, exception_message)` with JSON-safe sanitized fields, picklability requirement (no numpy arrays / file handles / traceback objects), sanitization sourced from the exception fields only (never `repr(e)`/`str(e.__cause__)`/traceback, because multiprocessing may attach remote-worker traceback text), and no inference by re-execution (O-14).
- **§5 table row 2:** updated to reflect the wrap-and-re-raise via `CalibrationWorkerError` (no swallowing, no partial result).
- **§6 item 2 (fail-closed tests):** updated to require that a worker exception raises `CalibrationWorkerError` and the parent emits the exact §4.2 failure record with correct identity sourced from the exception.

### Preserved

- **No-retry (O-14):** preserved — identity is carried by the exception; no re-execution to discover failure identity.
- **Fail-closed:** preserved — the first exception still terminates the diagnostic; completed results discarded; no partial calibration table; no simulation after calibration failure.
- **Calibration algorithm, combo seeds, estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, R8 guard, write-order fix, three NF-IMPL fixes, candidate-blindness (Ruling 9), O-15 diagnostic-only labeling, artifact schema/JSON write order, and all locked bars:** unchanged.
- **Reproducibility (§4.9):** unaffected — the happy path (no exceptions) is unchanged; `sigma_dose` values and downstream scientific fields remain identical between `workers=1` and `workers=N`.

### New parameters introduced

None beyond v1. The `CalibrationWorkerError` constructor fields mirror the v1 §4.2 failure-record fields (already present); no new numeric parameters, no new scientific apparatus parameters, no new performance bars. P3 unchanged.

### §5 P1–P6

- P1/P2: PASS — no new law text; existing verbatim quotes retained.
- P3: PASS — no new numeric parameters; `CalibrationWorkerError` fields mirror the already-tagged v1 failure record.
- P4: PASS — header states 2026-08-19, Regime B.
- P5: N/A — no deviation from `[LAW]` text.
- P6: PASS — citations unchanged from v1.

### Pre-push scan attestation

A pre-push self-scan was performed on the amended content before commit. Scanned for credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, and PII. **Findings:** none — only descriptive attestation prose matched. No private paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## v1 — Initial specification (2026-08-19)

**Base:** `7e296ec` (functional L8 multiprocessing remediation, BF-MP-1 remediation baseline per Coordinator handoff). The frozen L8 instantiation spec v2.2 (`c7d7bed`) is an input source only; `7e296ec` and `c7d7bed` are divergent and are not merged.

**Scope:** A standalone ARCHITECT specification for parallelizing the 15 independent `(alpha, v_mult)` sigma-dose calibrations in `diagnostics/l8_power_analysis.py` (`run_power_analysis` and `run_power_analysis_misspecified`). Scheduling optimization only — no scientific result, locked bar, control, scoring logic, or protected function is changed.

### What the spec defines

- Resolves all 10 TASK BUILDER design decisions (worker contract; failure semantics; pool lifecycle; worker allocation; reference/stress reuse; result identity validation; progress reporting; artifact compatibility; reproducibility comparison; performance verification).
- Adopts the TASK BUILDER's candidate redesign with modifications (ordinal in input record; no-nested-pools locked as a lifecycle requirement; worker-allocation cap classified as resource hygiene, not a bar; no cross-profile calibration caching; byte-compatible artifact schema with no new subphase fields; reproducibility requires both sigma_dose exact equality and byte-identical artifact plus downstream scientific equality; no numeric performance bar).
- Adopts the TASK BUILDER's verification obligations with the reproducibility standard sharpened (genuine single-vs-multi diagnostic; both value equality and byte identity; downstream scientific equality; process observation; no scoring).

### New parameters introduced

No new scientific apparatus parameters or performance bars. Two diagnostic implementation criteria are introduced and tagged: the worker-allocation cap `min(requested_workers, 15)` `[PROPOSED — resource-hygiene implementation constraint; derived from frozen ALPHAS × V_MULTS]` (§4.4) and the process-observation check `[PROPOSED — diagnostic implementation check]` (§4.10). Neither gates a scientific result; both are offered for Rebecca's sign-off. No numeric speedup/utilization bar is introduced.

### Constraints preserved

The `calibrate_sigma_dose` algorithm and return value; the 15-element calibration domain; one calibration result per `(alpha, v_mult)` identity; `combo_seed` and per-simulation RNG; the §2 XF-5 estimator; both false-kill aggregations; the null-control calculation; the sensitivity-map construction; the deterministic selection rule; the misspecified profiles; candidate-blindness (Ruling 9); O-15 diagnostic-only labeling; all fail-closed guards; the JSON write order and artifact schema; the R8 guard; the write-order fix; and the three NF-IMPL fixes. No locked bar, control, selection logic, or scoring logic changed.

### §5 P1–P6

- P1 (no reconstruction): PASS — governance text quoted verbatim from repo.
- P2 (verbatim quotation): PASS — O-14, O-15, Ruling 9, §5 P1, §5 P3 quoted with file/line citations.
- P3 (source-class tags): PASS — no new scientific apparatus parameters or performance bars; two diagnostic implementation criteria (worker-allocation cap, process-observation check) tagged `[PROPOSED — ...]`; neither gates a scientific result.
- P4 (regime dating): PASS — header states 2026-08-19, Regime B.
- P5 (deviation memorialization): N/A — no deviation from `[LAW]` text.
- P6 (provenance citations): PASS — `[Entry 76]` consistent with frozen L8 spec v2.2; O-14/O-15 cited from Rebecca rulings.

### Pre-push scan attestation

A pre-push self-scan was performed on the spec and changelog before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. Content is specification text, verbatim governance quotes, code line/SHA citations, and source-class tags only. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

*This spec is a diagnostic scheduling optimization. It changes no scientific result, locked bar, or scoring logic. Rebecca is sole gate and merge authority.*
