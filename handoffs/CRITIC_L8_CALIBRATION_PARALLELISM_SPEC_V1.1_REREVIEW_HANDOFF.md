# CRITIC Handoff — Return to WORKFLOW COORDINATOR: L8 Calibration Parallelism Spec v1.1 Re-Review

**From:** CRITIC (fresh-context, re-review of the amended spec)
**To:** WORKFLOW COORDINATOR
**Date:** 2026-08-19 22:01 EDT
**Gate served:** Specification contradiction resolution re-review — §4.1 (worker exception handling) vs §4.2 (failure record identity)
**Verdict:** **CLEAR**
**Review artifact:** `reviews/critic_l8_calibration_parallelism_spec_v1.1_rereview.md` on `critic/l8-calibration-parallelism-spec-v1.1-rereview` (SHA below)

---

## Authorization context

The TASK BUILDER stopped before implementing the v1 spec, reporting a contradiction: §4.1 required the worker to let exceptions propagate without catching, while §4.2 required the parent to emit a failure record carrying the failed task's identity — but `multiprocessing.Pool.map` propagates a worker exception without surfacing the failed input tuple, so the parent could not identify the failed task without re-executing (violating O-14). The ARCHITECT resolved it via Option 1 (identity-carrying picklable `CalibrationWorkerError`). This handoff returns the CRITIC's re-review of the amended v1.1 spec.

---

## SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Spec branch | `architect/l8-calibration-parallelism-spec` |
| Amended HEAD (under review) | `b4419f9` (v1.1) |
| Prior version (v1, CRITIC-cleared) | `90d8835` |
| Delta reviewed | `90d8835...b4419f9` — `specs/l8_calibration_parallelism_spec.md` +20/−6; changelog +41 |
| Base code (unchanged) | `diagnostics/l8_power_analysis.py` at `7e296ec` on `taskbuilder/l8-power-analysis` |
| Prior CRITIC spec review (v1 CLEAR) | `reviews/critic_l8_calibration_parallelism_spec_review.md` on `critic/l8-calibration-parallelism-spec-review` (`a087654`) |

---

## Verdict: CLEAR

The §4.1/§4.2 contradiction is genuinely resolved. The amendment is surgical (title/status, §4.1, §4.2, new §4.2.1, §5 row 2, §6 item 2); all other v1 content is byte-for-byte unchanged. The Option 1 resolution (identity-carrying picklable `CalibrationWorkerError`, narrowly wrapped and re-raised by the worker, caught by the parent solely to emit the failure record and terminate fail-closed) is sound, internally consistent, and the most constraint-preserving of the three options. No-retry (O-14), fail-closed, the calibration algorithm, all protected scientific logic, and candidate-blindness are preserved. P1–P6 maintained.

---

## The resolution (Option 1) — VERIFIED sound

- **§4.1 (amended — wrap-and-re-raise):** worker catches exceptions only around `calibrate_sigma_dose(alpha, v_mult)` and only to re-raise a top-level, picklable `CalibrationWorkerError` carrying identity + sanitized error descriptor. MUST NOT swallow, return a result, return `sigma_dose`, convert into a usable result, or retry. The re-raised `CalibrationWorkerError` propagates through `pool.map` to the parent. ✓
- **§4.2 (amended — identity from the exception):** parent sources `ordinal`, `alpha`, `v_mult`, `exception_type`, `exception_message` from the propagated `CalibrationWorkerError` — not from `repr(e)`, traceback text, or re-execution. Catches it solely to emit the record and terminate fail-closed (non-zero). Sanitization expanded to "no remote-worker traceback." Failure-record fields unchanged from v1. ✓
- **§4.2.1 (new — CalibrationWorkerError contract):** top-level picklable exception class (name fixed); constructor fields `(ordinal, alpha, v_mult, exception_type, exception_message)` JSON-safe/sanitized; MUST be picklable (must not carry numpy arrays/file handles/traceback objects — the technical crux for cross-process propagation); parent builds the record from these fields only (never `repr(e)`/`str(e.__cause__)`/traceback); no inference by re-execution (O-14). ✓
- **§5 row 2 + §6 item 2:** updated for consistency with the amended §4.1/§4.2/§4.2.1. ✓

The contradiction is removed without weakening fail-closed semantics: the worker catches narrowly and re-raises (still returns no partial result); the exception still propagates to the parent (as `CalibrationWorkerError`); identity is available at the point of failure (where the input tuple is in scope) and read by the parent from the propagated exception (no re-execution).

---

## Why Option 1 — sound rationale

Option 2 (result-or-error protocol; worker never raises) rejected as a larger worker-protocol/dispatch-mechanism change that waits for all calibrations before parent-side failure handling. Option 3 (nullable identity fields) rejected as weakening the failure record and accepting not knowing which task failed. Option 1 is the most constraint-preserving: `pool.map` remains the dispatch mechanism; failure stays exception-driven and fail-closed; no retry/re-execution to discover identity; no partial calibration table usable; surgical amendment.

---

## Constraint preservation — VERIFIED

- **No-retry (O-14):** preserved — identity carried by the exception; no re-execution to discover failure identity. ✓
- **Fail-closed:** preserved — first exception terminates immediately; completed results discarded (pool.map returns no partial results on exception); no partial calibration table; no simulation after calibration failure; parent catches `CalibrationWorkerError` solely to emit the sanitized record and terminate non-zero. ✓
- **Calibration algorithm + all protected scientific logic:** unchanged — `calibrate_sigma_dose`, 15-element domain, one result per identity, `combo_seed` + RNG, §2 XF-5 estimator, both false-kill aggregations, null-control, sensitivity map, selection rule, misspecified profiles, R8 guard, write-order fix, three NF-IMPL fixes, BF-MP-1 multiprocessing. ✓
- **Candidate-blindness (Ruling 9):** preserved — synthetic/oracle-only; the exception channel carries only apparatus-parameter identity + sanitized error text, no candidate data. ✓
- **Reproducibility (§4.9):** unaffected — happy path unchanged; `sigma_dose` and all downstream scientific fields identical between `workers=1` and `workers=N`; failure handling is orthogonal. ✓
- **Artifact schema / JSON write order, O-15 labeling, fail-closed guards, locked bars:** unchanged. ✓

---

## Scope check — PASS (surgical)

Diff `90d8835...b4419f9` touches only the two spec files. Amendments confined to title/status, §4.1, §4.2, new §4.2.1, §5 row 2, §6 item 2. v1 content below the amended sections is byte-for-byte unchanged. No scope creep.

---

## §5 P1–P6 compliance

- **P1:** PASS — no new law text; verbatim quotes retained from v1.
- **P2:** PASS — v1 §2 quotes retained (amendment didn't touch §2). Carry-forward v1 non-blocking imperfections (truncated P1 quote — NF-CPS-1; paraphrased Ruling 9 quote — NF-CPS-2) unchanged, still non-blocking.
- **P3:** PASS — no new numeric parameters/thresholds/kill conditions/test criteria. `CalibrationWorkerError` is an implementation mechanism (exception class), not a numeric threshold; P3 doesn't require a tag for it. Fields mirror the v1 failure-record fields. No new `[PROPOSED]` parameter.
- **P4:** PASS — date 2026-08-19, Regime B, post-Entry 81 (retained).
- **P5:** N/A — no deviation from `[LAW]` text.
- **P6:** PASS — citations unchanged from v1.

---

## Design soundness (fresh-eyes) — SOUND

- The contradiction is real; the identity-carrying picklable exception is the correct bridge (worker attaches identity at the point of failure where the input tuple is in scope; parent reads it from the propagated exception without re-execution). ✓
- Picklability correctly specified — the technical crux for cross-process propagation via `pool.map`; must not carry numpy arrays/file handles/traceback objects. ✓
- Sanitization is defensive — parent builds the record from `CalibrationWorkerError` fields only, never `repr(e)`/traceback (prevents remote-worker traceback leaking private paths/identifiers). ✓
- Internally consistent and implementable — §4.1 → §4.2.1 → §4.2 form a coherent, unambiguous chain; the TASK BUILDER receives no design decisions (class name, fields, picklability, sanitization source, no-re-execution all fixed). ✓
- Happy path unaffected — §4.9 reproducibility and downstream scientific fields unchanged; failure handling orthogonal. ✓

---

## Non-blocking findings

- **NF-CPS-3 (new, trivial — test-completeness):** §6 item 2's worker-exception test asserts the parent emits the exact failure record with correct identity, fails closed, discards results, dispatches no simulation — but doesn't explicitly assert that `exception_message` is sanitized (no private paths/hostnames/PII). The §4.2.1 normative sanitization requirement is clear; this is only a suggestion that the test also assert sanitization completeness. Not a spec defect; not a block.
- **NF-CPS-1 (carry-forward from v1):** §5 P1 quote truncated (verbatim portion; omits trailing explanatory clause). Still non-blocking.
- **NF-CPS-2 (carry-forward from v1):** Ruling 9 quote paraphrased rather than verbatim from Entry 76. Citation accurate; meaning preserved. Still non-blocking.

---

## Preserved evidence

v1 spec content (except the surgically amended sections) byte-for-byte unchanged. Base code (`7e296ec`) unchanged. Frozen L8 spec v2.2 (`c7d7bed`) cited as input only. All prior CRITIC CLEARs (v1 `a087654`) and BF-MP-1 BLOCK findings remain valid. The amendment invalidates no prior evidence; it resolves an internal contradiction the v1 review did not catch (the v1 review cleared §4.1/§4.2 individually but did not flag their interaction — the TASK BUILDER's stop-report surfaced it).

---

## Pre-push scan attestation

A pre-push self-scan was performed on this handoff artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the spec, code, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No implementation of calibration parallelism (deferred to TASK BUILDER after CRITIC re-review and Rebecca re-approval).
- No L15/L16/L17 before M5.
- No touching the calibration algorithm, `combo_seed`, estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, R8 guard, write-order fix, NF-IMPL-1/2/3 fixes, or BF-MP-1 multiprocessing (all preserved by the amendment).
- No leaving the contradiction unresolved — the amended spec is unambiguous on failure-identity handling.

---

## Next authorized role / routing

**Next recipient:** WORKFLOW COORDINATOR → **Rebecca** (re-approve the amended spec) → **TASK BUILDER** (implement the approved spec) → **CRITIC** (code review: does the code match the approved spec? genuine reproducibility per §4.9/§6?) → **Rebecca** (authorize → rerun locally). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On CLEAR (this case), Rebecca re-approves the amended spec. On BLOCK, returns to ARCHITECT.

---

*This handoff was produced read-only against the amended spec at `b4419f9` on `architect/l8-calibration-parallelism-spec`. No scoring, rerun, hold-out seed exposure, implementation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
