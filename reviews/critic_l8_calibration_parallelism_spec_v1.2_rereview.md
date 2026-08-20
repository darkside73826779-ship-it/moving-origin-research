# CRITIC Re-Review — L8 Calibration Parallelism Spec v1.2 (Failure-Path Determinism)

**Gate served:** CRITIC re-review of the v1.2 amendment — are all three failure-path gaps closed, is every failure path deterministic, are constraints preserved?
**Reviewer:** CRITIC (fresh-context, focused re-review of the v1.2 delta)
**Date:** 2026-08-19 22:25 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — on CLEAR, Rebecca approves → TASK BUILDER implements → CRITIC code review → Rebecca authorizes.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Spec branch | `architect/l8-calibration-parallelism-spec` |
| Amended HEAD (v1.2, under review) | `6979378` |
| Prior version (v1.1, CRITIC-cleared) | `b4419f9` |
| Delta reviewed | `b4419f9...6979378` — `specs/l8_calibration_parallelism_spec.md` +164/−19; changelog +63 |
| Prior CRITIC re-review (v1.1 CLEAR) | `reviews/critic_l8_calibration_parallelism_spec_v1.1_rereview.md` on `critic/l8-calibration-parallelism-spec-v1.1-rereview` (`5a16485`) |

Read-only review. No spec, code, constitution, or scoring artifact modified (read-only + own review/handoff files). No scoring, seed execution, hold-out seed exposure, implementation, or unauthorized merge performed.

---

## Headline finding (CLEAR)

All three failure-path gaps are genuinely closed, and the spec now leaves the TASK BUILDER nothing to infer on any failure path. The amendment provides binding normative code for the worker (`_worker_calibration`), the `CalibrationWorkerError` and `CalibrationIdentityError` contracts, the validation helper, the failure-record emitter, and the parent-owned boundary (`_run_calibration_phase`); a complete implementation-trace table (§4.2.3) covering all four failure paths; and a 14-point binding test contract (§6) that includes all 10 requested failure-path assertions. The fixed-message sanitization (`exception_message = "calibration worker failed"`) directly resolves my v1.1 NF-CPS-3 (sanitization-completeness) observation. No-retry (O-14), fail-closed, the calibration algorithm, all protected scientific logic, and candidate-blindness are preserved. P1–P6 maintained. Two carry-forward v1 P2/P6 imperfections remain non-blocking.

---

## The three gaps — all closed

### Gap 1 — Error sanitization is deterministic (CLOSED)

§4.2.1 now specifies `exception_message` is **always exactly the fixed string `"calibration worker failed"`** and MUST NOT vary by platform, process, task, or underlying exception. The worker catches `Exception` only (not `BaseException`) and raises `CalibrationWorkerError(...) from None` to suppress exception chaining. The original exception's message, `repr`, traceback, `__cause__`, `__context__`, `args`, and object are **never** stored, serialized, logged, or attached. The constructor passes exactly five fields to `Exception.__init__` so default pickling reconstructs the object with the required signature. Binding normative code in §4.2.1 enforces this. No regex redaction of arbitrary exception text; no alternate sanitizer permitted. ✓ This eliminates the sanitization-completeness concern I raised in v1.1 (NF-CPS-3) — since the message is a constant, there is nothing to leak. **NF-CPS-3 RESOLVED.**

### Gap 2 — The termination mechanism is named (CLOSED)

§4.2 "Termination mechanism" names **`SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]`** as the sole non-zero termination mechanism; no alternate exit code, return, or exception permitted. The parent boundary `_run_calibration_phase` raises `SystemExit(1)` immediately after emitting the failure record. ✓ A unit test can assert `SystemExit(1)`.

### Gap 3 — The identity-validation contract is specified (CLOSED)

§4.2.2 defines **`CalibrationIdentityError`** (top-level, picklable, name fixed) as the sole contract for identity-validation failures. Fixed public-safe message `"calibration identity validation failed"` (no raw returned records, no unexpected values). A 7-field identity failure record: `{phase, analysis_label, message, mismatch_kinds (sorted subset of ["duplicate","missing","unexpected"] in fixed order), expected_count, seen_count (= number of returned records, so duplicates visible), canonical_identities (frozen published synthetic params, not candidate data — Ruling 9)}`. The validation helper `_validate_calibration_identities` raises on any duplicate/missing/unexpected; malformed returned records (non-dict, missing `alpha`/`v_mult`, non-canonical values) are treated as `unexpected` via `TypeError`/`KeyError` around key extraction. The parent boundary catches `(CalibrationWorkerError, CalibrationIdentityError)`, emits the corresponding record, and raises `SystemExit(1)`. Binding normative code in §4.2.2. ✓

---

## Implementation trace (§4.2.3) — complete, every path deterministic

The §4.2.3 table traces all four failure paths (worker exception; identity validation; partial-result prevention; termination) across seven columns: input identity available at; object crossing process boundary; picklable under spawn; exact text reaching logs; parent exception/exit; partial results to simulation?; unit-test assertion contract. Every cell is concretely specified:

- **Worker exception:** identity at `_worker_calibration` scope; `CalibrationWorkerError(ordinal, alpha, v_mult, exception_type, exception_message)` crosses the boundary; picklable (top-level class, int/float/str fields, `from None`, default pickling via 5-arg constructor); logs see exactly `exception_type` (class name) and `exception_message` (`"calibration worker failed"`) — never repr/traceback/cause/context/args; parent catches `CalibrationWorkerError`, emits 7-field JSON line to stderr, raises `SystemExit(1)`; no partial results reach simulation (`pool.map` raises before returning; `SystemExit(1)` before table built); test asserts `SystemExit(1)`, exactly one 7-field JSON line with `exception_message == "calibration worker failed"`, original message absent from pickled exception/log/record. ✓
- **Identity validation:** identity at `_validate_calibration_identities` scope; success result dicts (JSON-safe) cross the boundary; picklable; logs see exactly `"calibration identity validation failed"`, `mismatch_kinds`, `expected_count`, `seen_count`, `canonical_identities` — never raw records or unexpected values; parent catches `CalibrationIdentityError`, emits 7-field JSON line, `SystemExit(1)`; validation runs before the table returns; test asserts `CalibrationIdentityError` with correct `mismatch_kinds` and `SystemExit(1)`. ✓
- **Partial-result prevention:** structural — calibration table returned only after `pool.map` succeeds AND identities validate; no simulation work item constructed before the table returns; test asserts no `_worker_combo`/`_worker_null_control` call after a calibration failure. ✓
- **Termination:** `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]` on any worker or identity failure; test asserts exit status 1, no return value, no alternate exception, no stdout. ✓

**The TASK BUILDER has nothing to invent on any failure path.** ✓

---

## The 10-point test contract (§6) — present (expanded to 14)

| # | Handoff-required assertion | Spec §6 item | Status |
|---|---|---|---|
| 1 | CalibrationWorkerError survives pickle with all five fields | §6.1 | ✓ |
| 2 | Worker failure carries correct identity | §6.2 | ✓ |
| 3 | exception_type is the class name | §6.3 | ✓ |
| 4 | exception_message exactly "calibration worker failed" even with private paths/hostnames/SIDs/emails/tokens/newlines | §6.4 | ✓ |
| 5 | Original message absent from pickled exception/log/record | §6.5 | ✓ |
| 6 | Failure record exactly seven fields, no traceback | §6.6 | ✓ |
| 7 | Parent terminates via the named mechanism | §6.7 (SystemExit(1)) | ✓ |
| 8 | No simulation after failure | §6.8 | ✓ |
| 9 | Identity-validation failures use the named contract | §6.9 | ✓ |
| 10 | Happy-path serial/parallel tables identical | §6.10 (a+b+c) | ✓ |

Plus §6.11 (genuine single-vs-multi, guards against BF-MP-1 vacuous recurrence), §6.12 (protected-logic static/diff check), §6.13 (process observation), §6.14 (no scoring). ✓ All 10 requested points present; the prior 9-item list is replaced by this 14-point binding contract.

---

## Binding normative code — leaves nothing to infer

The spec now provides binding normative Python for: `CalibrationWorkerError.__init__` (fixed message, 5-arg super().__init__); `_worker_calibration` (Exception-only catch, `from None`, fixed message); `CalibrationIdentityError.__init__`; `_emit_calibration_failure` (stderr JSON line, sort_keys, flush); `_validate_calibration_identities` (duplicate/missing/unexpected + malformed-as-unexpected); and `_run_calibration_phase` (build work items, min-cap workers, pool.map, validate, catch both exceptions, emit record, SystemExit(1), return table on success). The spec states the TASK BUILDER may not alter the field set, the fixed message, the `from None`, or the `Exception`-only catch. ✓

---

## Constraints preserved — VERIFIED

- **Calibration algorithm + all protected scientific logic:** unchanged — `calibrate_sigma_dose`, 15-element domain, one result per identity, `combo_seed` + per-simulation RNG, §2 XF-5 estimator, both false-kill aggregations, null-control, sensitivity map, selection rule, misspecified profiles, R8 guard, write-order fix, three NF-IMPL fixes, BF-MP-1 multiprocessing. ✓
- **Candidate-blindness (Ruling 9):** preserved — the exception channel carries only apparatus-parameter identity (ordinal, alpha, v_mult) + the fixed public-safe message `"calibration worker failed"` / `"calibration identity validation failed"`; `canonical_identities` are the frozen, already-published synthetic `ALPHAS × V_MULTS` parameters, not candidate output or private data. No candidate data crosses the channel. ✓
- **No-retry (O-14):** preserved — identity is carried by the exception (worker) / available from the returned results (validation); no re-execution to discover failure identity. ✓
- **Fail-closed:** preserved — first exception terminates; completed results discarded (`pool.map` returns no partial results on exception); no partial calibration table; no simulation work item built or dispatched after a calibration failure (`SystemExit(1)` before the table returns). ✓
- **R8 guard, write-order fix, NF-IMPL-1/2/3, BF-MP-1, 15-element domain, `pool.map` dispatch:** unchanged. ✓

---

## Scope check — PASS (surgical)

Diff `b4419f9...6979378` touches only `specs/l8_calibration_parallelism_spec.md` (+164/−19) and `specs/l8_calibration_parallelism_spec_changelog.md` (+63). No code, constitution, STATE.md, or provenance log. The amendments are confined to title/status, §4.1 (Exception catch narrowed to `Exception` not `BaseException`; original-exception fields never stored), §4.2 (parent-owned boundary, exact logging sink, termination mechanism, 7-field worker failure record), §4.2.1 (fixed message, original-exception handling, normative code), new §4.2.2 (identity-validation contract + parent boundary + normative code), new §4.2.3 (implementation trace), §6 (14-point test contract), §8 P3, §9, §10. v1.1 content outside these sections is byte-for-byte unchanged.

---

## §5 P1–P6 compliance

- **P1 (repo-first, no reconstruction):** PASS — no new law text; verbatim quotes retained from v1.
- **P2 (verbatim quotation):** PASS — v1 §2 quotes retained (amendment didn't touch §2). Carry-forward v1 non-blocking imperfections (truncated P1 quote — NF-CPS-1; paraphrased Ruling 9 quote — NF-CPS-2) unchanged, still non-blocking.
- **P3 (source-class tags):** PASS. No new scientific apparatus parameters or performance bars. The new `SystemExit(1)` termination mechanism is tagged `[PROPOSED — diagnostic termination mechanism]` (§4.2). `expected_count`/`seen_count` are diagnostic record fields derived from the frozen calibration domain, not thresholds or bars. `CalibrationWorkerError` and `CalibrationIdentityError` are implementation mechanisms (exception classes), not numeric thresholds/kill conditions/test criteria — P3 does not require tags for them. None of the tagged items gates a scientific result; all are offered for Rebecca's sign-off. No numeric performance/speedup bar introduced. ✓
- **P4 (regime dating):** PASS — date 2026-08-19, Regime B, post-Entry 81 (retained).
- **P5 (deviation memorialization):** N/A — no deviation from `[LAW]` text.
- **P6 (provenance citations):** PASS — citations unchanged from v1.

---

## Design soundness (fresh-eyes) — SOUND

- **Fixed-message sanitization is the right design:** by making `exception_message` a constant, the spec eliminates the entire class of sanitization-completeness risk (no regex to bypass, no hostile input to redact). `from None` suppresses `__cause__`/`__context__` chaining; `Exception`-only catch does not swallow `KeyboardInterrupt`/`SystemExit`. ✓
- **Parent-owned shared boundary is sound:** a single `_run_calibration_phase` used by both reference and misspecified analyses ensures they do not implement divergent failure handling; the boundary owns pool lifecycle, validation, failure emission, and termination. ✓
- **Identity validation is complete:** handles duplicates (`seen_count` > `expected_count`), missing (`seen_keys != canonical`), unexpected (key not in canonical), and malformed records (non-dict/missing keys → `unexpected` via `TypeError`/`KeyError`); `mismatch_kinds` is a sorted list because the conditions may co-occur. ✓
- **Picklability correctly reasoned:** top-level classes, JSON-safe scalar fields, default pickling via the 5-arg/5-field constructor, no numpy arrays/file handles/traceback objects. ✓
- **Stderr JSON sink is exactly specified:** one JSON line, `sort_keys=True`, flush, no other sink, no stdout, no traceback. ✓
- **`SystemExit(1)` as the sole termination** is testable and unambiguous. ✓
- **Every failure path is deterministic — the TASK BUILDER has nothing to invent.** ✓

---

## Non-blocking findings

- **NF-CPS-3 (v1.1 — RESOLVED):** my v1.1 observation that the §6.2 worker-exception test should also assert `exception_message` sanitization is now fully addressed: §6.4 requires `exception_message == "calibration worker failed"` even with hostile input (private paths/hostnames/SIDs/emails/tokens/newlines), and §6.5 requires the original message absent from pickled exception/log/record. Resolved. ✓
- **NF-CPS-1 (carry-forward from v1):** §5 P1 quote truncated (verbatim portion; omits trailing explanatory clause). Still non-blocking.
- **NF-CPS-2 (carry-forward from v1):** Ruling 9 quote paraphrased rather than verbatim from Entry 76. Citation accurate; meaning preserved. Still non-blocking.

---

## Preserved evidence

v1.1 spec content outside the amended sections is byte-for-byte unchanged. Base code (`7e296ec`) unchanged. Frozen L8 spec v2.2 (`c7d7bed`) cited as input only. All prior CRITIC CLEARs (v1 `a087654`; v1.1 `5a16485`) and the BF-MP-1 BLOCK findings remain valid. The amendment invalidates no prior evidence; it closes failure-path determinism gaps the v1.1 review did not require (the v1.1 review cleared the contradiction resolution but the TASK BUILDER then identified that sanitization/termination/identity-validation still left implementation decisions open — v1.2 closes them).

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure/code descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the spec, code, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No implementation (deferred to TASK BUILDER after Rebecca approves).
- No L15/L16/L17 before M5.
- No touching the calibration algorithm, combo seeds, estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, write-order fix, NF-IMPL-1/2/3 fixes, or BF-MP-1 multiprocessing (all preserved by the amendment).

---

## Verdict and routing

**Verdict: CLEAR.** All three failure-path gaps are closed (deterministic sanitization via fixed message; `SystemExit(1)` termination named; `CalibrationIdentityError` contract specified). The implementation trace (§4.2.3) covers every failure path; the 14-point test contract (§6) includes all 10 requested assertions. Binding normative code leaves the TASK BUILDER nothing to invent. No-retry (O-14), fail-closed, the calibration algorithm, all protected scientific logic, and candidate-blindness are preserved. P1–P6 maintained. NF-CPS-3 (v1.1) resolved; NF-CPS-1 and NF-CPS-2 carry forward, still non-blocking.

**Next authorized role:** WORKFLOW COORDINATOR → **Rebecca** (approve the spec) → **TASK BUILDER** (implement the approved spec, local frontier GPT) → **CRITIC** (code review: does the code match the approved spec? genuine reproducibility per §4.9/§6?) → **Rebecca** (authorize → rerun locally). Scoring remains gated behind the five standing M4 gates. Nothing herein authorizes scoring.

---

*This review was conducted read-only against the amended spec at `6979378` on `architect/l8-calibration-parallelism-spec`. No scoring, rerun, hold-out seed exposure, implementation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
