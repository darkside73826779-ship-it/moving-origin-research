# L8 §8 Calibration Parallelism Spec — Changelog

**Spec:** `specs/l8_calibration_parallelism_spec.md`
**Date:** 2026-08-19 · **Author:** ARCHITECT
**Branch:** `architect/l8-calibration-parallelism-spec` (from `7e296ec` on `taskbuilder/l8-power-analysis`)
**Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)

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
