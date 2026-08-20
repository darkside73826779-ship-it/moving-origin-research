# CRITIC Handoff — Return to WORKFLOW COORDINATOR: L8 Calibration Parallelism Spec v1.2 Re-Review

**From:** CRITIC (fresh-context, focused re-review of the v1.2 delta)
**To:** WORKFLOW COORDINATOR
**Date:** 2026-08-19 22:25 EDT
**Gate served:** CRITIC re-review of the v1.2 amendment — are all three failure-path gaps closed, is every failure path deterministic, are constraints preserved?
**Verdict:** **CLEAR**
**Review artifact:** `reviews/critic_l8_calibration_parallelism_spec_v1.2_rereview.md` on `critic/l8-calibration-parallelism-spec-v1.2-rereview` (SHA below)

---

## Authorization context

The TASK BUILDER found three failure-path gaps in v1.1: (1) error sanitization was not deterministic (relied on redacting arbitrary exception text); (2) the non-zero termination mechanism was not named; (3) the identity-validation failure contract was not specified. The ARCHITECT amended the spec to v1.2 (`6979378`) closing all three, adding binding normative code, an implementation-trace table, and a 14-point test contract. This handoff returns the CRITIC's focused re-review of the v1.2 delta.

---

## SHAs reviewed

| Item | Value |
|---|---|
| Spec branch | `architect/l8-calibration-parallelism-spec` |
| Amended HEAD (v1.2, under review) | `6979378` |
| Prior version (v1.1, CRITIC-cleared) | `b4419f9` |
| Delta reviewed | `b4419f9...6979378` — `specs/l8_calibration_parallelism_spec.md` +164/−19; changelog +63 |
| Prior CRITIC re-review (v1.1 CLEAR) | `reviews/critic_l8_calibration_parallelism_spec_v1.1_rereview.md` on `critic/l8-calibration-parallelism-spec-v1.1-rereview` (`5a16485`) |

---

## Verdict: CLEAR

All three failure-path gaps are genuinely closed, and the spec now leaves the TASK BUILDER nothing to infer on any failure path. Binding normative code, a complete implementation-trace table (§4.2.3), and a 14-point test contract (§6, including all 10 requested assertions) make every failure path deterministic. The fixed-message sanitization directly resolves my v1.1 NF-CPS-3 (sanitization-completeness) observation. No-retry (O-14), fail-closed, the calibration algorithm, all protected scientific logic, and candidate-blindness are preserved. P1–P6 maintained.

---

## The three gaps — all closed

- **Gap 1 — Error sanitization deterministic (CLOSED):** `exception_message` is always exactly the fixed string `"calibration worker failed"`, MUST NOT vary by platform/process/task/underlying exception. Worker catches `Exception` only (not `BaseException`), raises `CalibrationWorkerError(...) from None` (suppresses chaining). Original exception's message, repr, traceback, `__cause__`, `__context__`, `args`, and object are never stored/serialized/logged/attached. Binding normative code in §4.2.1. No regex redaction; no alternate sanitizer. ✓ Resolves v1.1 NF-CPS-3.
- **Gap 2 — Termination mechanism named (CLOSED):** `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]` is the sole non-zero termination mechanism; no alternate exit code/return/exception permitted. Parent boundary raises `SystemExit(1)` immediately after emitting the failure record. ✓
- **Gap 3 — Identity-validation contract specified (CLOSED):** `CalibrationIdentityError` (top-level picklable, name fixed), fixed message `"calibration identity validation failed"` (no raw records), 7-field identity record (`mismatch_kinds` sorted subset of `["duplicate","missing","unexpected"]`, `expected_count`, `seen_count` = number of returned records so duplicates visible, `canonical_identities` = frozen published synthetic params, not candidate data). Validation helper handles duplicate/missing/unexpected + malformed-as-unexpected (TypeError/KeyError). Parent boundary catches both exceptions, emits record, `SystemExit(1)`. Binding normative code in §4.2.2. ✓

---

## Implementation trace (§4.2.3) — complete; every path deterministic

The §4.2.3 table traces all four failure paths (worker exception; identity validation; partial-result prevention; termination) across seven columns (input identity available at; object crossing boundary; picklable under spawn; exact text reaching logs; parent exception/exit; partial results to simulation?; unit-test assertion contract). Every cell is concretely specified. **The TASK BUILDER has nothing to invent on any failure path.**

---

## The 10-point test contract (§6) — present (expanded to 14)

§6.1 CalibrationWorkerError pickle round-trip (5 fields); §6.2 worker failure carries correct identity; §6.3 exception_type = class name; §6.4 `exception_message == "calibration worker failed"` even with private paths/hostnames/SIDs/emails/tokens/newlines; §6.5 original message absent from pickled exception/log/record; §6.6 failure record exactly 7 fields, no traceback; §6.7 parent terminates via `SystemExit(1)`; §6.8 no simulation after failure; §6.9 identity-validation failures use `CalibrationIdentityError` (correct `mismatch_kinds`, `expected_count`, `seen_count`, `canonical_identities`, pickle-survives); §6.10 happy-path serial/parallel tables identical (sigma_dose == + byte-identical artifact excluding elapsed_seconds + downstream scientific equality). Plus §6.11 genuine single-vs-multi (guards BF-MP-1 vacuous recurrence), §6.12 protected-logic diff, §6.13 process observation, §6.14 no scoring. ✓ All 10 requested points present.

---

## Binding normative code — leaves nothing to infer

The spec provides binding Python for: `CalibrationWorkerError.__init__` (fixed message, 5-arg super); `_worker_calibration` (Exception-only catch, `from None`, fixed message); `CalibrationIdentityError.__init__`; `_emit_calibration_failure` (stderr JSON line, sort_keys, flush); `_validate_calibration_identities` (duplicate/missing/unexpected + malformed-as-unexpected); `_run_calibration_phase` (build work items, min-cap workers, pool.map, validate, catch both exceptions, emit record, SystemExit(1), return table on success). TASK BUILDER may not alter the field set, the fixed message, the `from None`, or the `Exception`-only catch. ✓

---

## Constraints preserved — VERIFIED

Calibration algorithm + all protected scientific logic unchanged (`calibrate_sigma_dose`, 15-element domain, one result per identity, `combo_seed` + RNG, §2 XF-5 estimator, both false-kill aggregations, null-control, sensitivity map, selection rule, misspecified profiles, R8 guard, write-order fix, three NF-IMPL fixes, BF-MP-1 multiprocessing). Candidate-blindness (Ruling 9) preserved — exception channel carries only apparatus-parameter identity + fixed public-safe message; `canonical_identities` are frozen published synthetic params, not candidate data. No-retry (O-14) preserved — identity carried by exception/available from returned results; no re-execution. Fail-closed preserved — first exception terminates; completed results discarded (pool.map returns no partial results on exception); no partial table; no simulation after failure (`SystemExit(1)` before table returns). R8 guard, write-order fix, NF-IMPL-1/2/3, BF-MP-1, 15-element domain, `pool.map` dispatch unchanged.

---

## Scope check — PASS (surgical)

Diff `b4419f9...6979378` touches only the two spec files. No code, constitution, STATE.md, or provenance log. Amendments confined to title/status, §4.1, §4.2, §4.2.1, new §4.2.2, new §4.2.3, §6, §8 P3, §9, §10. v1.1 content outside these sections byte-for-byte unchanged.

---

## §5 P1–P6 compliance

- **P1:** PASS — no new law text; verbatim quotes retained.
- **P2:** PASS — v1 §2 quotes retained (amendment didn't touch §2). Carry-forward v1 non-blocking imperfections (truncated P1 quote — NF-CPS-1; paraphrased Ruling 9 quote — NF-CPS-2) unchanged.
- **P3:** PASS — no new scientific apparatus parameters or performance bars. `SystemExit(1)` tagged `[PROPOSED — diagnostic termination mechanism]`. `expected_count`/`seen_count` are diagnostic record fields, not thresholds. `CalibrationWorkerError`/`CalibrationIdentityError` are implementation mechanisms (exception classes), not numeric thresholds — P3 doesn't require tags for them. None gates a scientific result; all offered for Rebecca's sign-off. No numeric performance/speedup bar.
- **P4:** PASS — date 2026-08-19, Regime B, post-Entry 81.
- **P5:** N/A — no deviation from `[LAW]` text.
- **P6:** PASS — citations unchanged from v1.

---

## Design soundness (fresh-eyes) — SOUND

Fixed-message sanitization eliminates the entire sanitization-completeness risk class (no regex to bypass, no hostile input to redact). `from None` suppresses chaining; `Exception`-only catch doesn't swallow `KeyboardInterrupt`/`SystemExit`. Parent-owned shared boundary (`_run_calibration_phase`) used by both reference and misspecified analyses prevents divergent failure handling. Identity validation is complete (duplicate/missing/unexpected + malformed-as-unexpected; `mismatch_kinds` as a sorted list since conditions may co-occur). Picklability correctly reasoned (top-level classes, JSON-safe scalars, default pickling). Stderr JSON sink exactly specified (one line, sort_keys, flush, no other sink, no stdout, no traceback). `SystemExit(1)` as sole termination is testable. Every failure path deterministic — the TASK BUILDER has nothing to invent.

---

## Non-blocking findings

- **NF-CPS-3 (v1.1 — RESOLVED):** my v1.1 suggestion that the worker-exception test also assert `exception_message` sanitization is now fully addressed by §6.4 (fixed message even with hostile input) and §6.5 (original message absent from pickled exception/log/record). Resolved. ✓
- **NF-CPS-1 (carry-forward from v1):** §5 P1 quote truncated (verbatim portion; omits trailing explanatory clause). Still non-blocking.
- **NF-CPS-2 (carry-forward from v1):** Ruling 9 quote paraphrased rather than verbatim from Entry 76. Citation accurate; meaning preserved. Still non-blocking.

---

## Preserved evidence

v1.1 spec content outside amended sections byte-for-byte unchanged. Base code (`7e296ec`) unchanged. Frozen L8 spec v2.2 (`c7d7bed`) cited as input only. All prior CRITIC CLEARs (v1 `a087654`; v1.1 `5a16485`) and BF-MP-1 BLOCK findings remain valid. The amendment invalidates no prior evidence; it closes failure-path determinism gaps the v1.1 review did not require (the TASK BUILDER identified that sanitization/termination/identity-validation still left implementation decisions open — v1.2 closes them).

---

## Pre-push scan attestation

A pre-push self-scan was performed on this handoff artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure/code descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the spec, code, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No implementation (deferred to TASK BUILDER after Rebecca approves).
- No L15/L16/L17 before M5.
- No touching the calibration algorithm, combo seeds, estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, write-order fix, NF-IMPL-1/2/3 fixes, or BF-MP-1 multiprocessing (all preserved by the amendment).

---

## Next authorized role / routing

**Next recipient:** WORKFLOW COORDINATOR → **Rebecca** (approve the spec) → **TASK BUILDER** (implement the approved spec, local frontier GPT) → **CRITIC** (code review: does the code match the approved spec? genuine reproducibility per §4.9/§6?) → **Rebecca** (authorize → rerun locally). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On CLEAR (this case), Rebecca approves the spec. On BLOCK, returns to ARCHITECT.

---

*This handoff was produced read-only against the amended spec at `6979378` on `architect/l8-calibration-parallelism-spec`. No scoring, rerun, hold-out seed exposure, implementation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
