# CRITIC Re-Review — L8 Calibration Parallelism Spec v1.1 (§4.1/§4.2 Contradiction Resolution)

**Gate served:** Specification contradiction resolution re-review — §4.1 (worker exception handling) vs §4.2 (failure record identity)
**Reviewer:** CRITIC (fresh-context, re-review of the amended spec)
**Date:** 2026-08-19 22:01 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — on CLEAR, Rebecca re-approves the amended spec, then TASK BUILDER implements, then CRITIC code review, then Rebecca authorizes.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Spec branch | `architect/l8-calibration-parallelism-spec` |
| Amended HEAD (under review) | `b4419f9` (v1.1) |
| Prior version (v1, CRITIC-cleared) | `90d8835` |
| Delta reviewed | `90d8835...b4419f9` — `specs/l8_calibration_parallelism_spec.md` +20/−6; changelog +41 |
| Spec | `specs/l8_calibration_parallelism_spec.md` (v1.1) |
| Spec changelog | `specs/l8_calibration_parallelism_spec_changelog.md` (v1.1 entry) |
| Base code (unchanged) | `diagnostics/l8_power_analysis.py` at `7e296ec` on `taskbuilder/l8-power-analysis` |
| Prior CRITIC spec review (v1 CLEAR) | `reviews/critic_l8_calibration_parallelism_spec_review.md` on `critic/l8-calibration-parallelism-spec-review` (`a087654`) |
| ARCHITECT contradiction-resolution handoff | the attachment `ARCHITECT-Calibration-Contradiction-Resolution-Handoff-v1.1.md` |

Read-only review. No spec, code, constitution, or scoring artifact modified (read-only + own review/handoff files). No scoring, seed execution, hold-out seed exposure, implementation, or unauthorized merge performed.

---

## Headline finding (CLEAR)

The §4.1/§4.2 contradiction is genuinely resolved. The amendment is surgical (title/status, §4.1, §4.2, new §4.2.1, §5 row 2, §6 item 2); all other v1 content is byte-for-byte unchanged. The chosen resolution (Option 1 — identity-carrying picklable `CalibrationWorkerError`, narrowly wrapped and re-raised by the worker, caught by the parent solely to emit the failure record and terminate fail-closed) is sound, internally consistent, and the most constraint-preserving of the three options. No-retry (O-14), fail-closed, the calibration algorithm, all protected scientific logic, and candidate-blindness are preserved. P1–P6 maintained. One new trivial non-blocking observation (test-completeness) plus the two carry-forward v1 P2/P6 imperfections, none blocking.

---

## The contradiction (confirmed genuine)

- **§4.1 (v1)** required `_worker_calibration` to let exceptions propagate without catching.
- **§4.2 (v1)** required the parent to emit a failure record carrying the failed task's `ordinal`, `alpha`, `v_mult`, `exception_type`, `exception_message`.

**Why incompatible:** `multiprocessing.Pool.map` propagates a worker exception to the parent but does not surface the failed input tuple in structured form. The parent therefore could not reliably identify which of the 15 parallel work items failed without re-executing tasks — which would violate O-14 (no re-run-on-failure). The TASK BUILDER correctly stopped rather than infer a resolution. This is a real internal contradiction in v1; the ARCHITECT's amendment is warranted.

---

## The resolution (Option 1) — VERIFIED sound and internally consistent

A worker exception is narrowly wrapped (catch only around `calibrate_sigma_dose(alpha, v_mult)`, only to re-raise) in a top-level, picklable `CalibrationWorkerError` carrying the failed task's identity and a sanitized error descriptor, then re-raised. The exception propagates through `pool.map` to the parent; the parent catches it solely to emit the §4.2 failure record (identity sourced from the exception) and terminate fail-closed (non-zero).

### §4.1 (amended — wrap-and-re-raise)

The worker MUST catch exceptions only around `calibrate_sigma_dose(alpha, v_mult)` and only to re-raise a top-level, picklable `CalibrationWorkerError`. It MUST NOT swallow, MUST NOT return a result on failure, MUST NOT return `sigma_dose`, MUST NOT convert the exception into a usable calibration result, MUST NOT retry. The re-raised `CalibrationWorkerError` propagates through `pool.map` to the parent. (Input record and success-output contract from v1 unchanged.) ✓

This is internally consistent with §4.2: the worker no longer "must not catch" — it catches narrowly and re-raises a picklable, identity-carrying exception. The exception still propagates to the parent (as `CalibrationWorkerError`); the worker still returns no partial result. The contradiction is removed without weakening fail-closed semantics.

### §4.2 (amended — identity sourced from the exception)

The parent sources `ordinal`, `alpha`, `v_mult`, `exception_type`, `exception_message` from the propagated `CalibrationWorkerError` (§4.2.1) — not from `repr(e)`, traceback text, or re-execution. The parent catches `CalibrationWorkerError` solely to emit the record and terminate fail-closed (non-zero); must not produce a calibration result, must not log traceback text, must not retry or infer identity by re-execution. Sanitization expanded to "no remote-worker traceback." Failure-record fields unchanged from v1. ✓

### §4.2.1 (new — CalibrationWorkerError contract)

- **Class:** top-level, picklable `CalibrationWorkerError` (name fixed; TASK BUILDER may not choose alternative); sole channel for failed-task identity; raised by `_worker_calibration`, caught by parent. ✓
- **Constructor fields:** `CalibrationWorkerError(ordinal, alpha, v_mult, exception_type, exception_message)` — JSON-safe, sanitized. `exception_type` = original exception's class name; `exception_message` = sanitized message string (no traceback, no private paths, no hostnames/SIDs/PII). ✓
- **Picklability:** class and fields MUST be picklable (Python multiprocessing serializes the exception across the process boundary); MUST NOT carry non-picklable objects (numpy arrays, file handles, traceback objects). ✓ This is the key technical correctness point — without picklability, `pool.map` could not propagate the exception and the resolution would fail. Correctly specified.
- **Sanitization source:** parent builds the failure record from `CalibrationWorkerError` fields only — never `repr(e)`, `str(e.__cause__)`, or traceback text (multiprocessing may attach remote-worker traceback text containing private paths/identifiers). ✓ Good defensive design — prevents the private-path leak that logging the raw exception repr would cause.
- **No inference by re-execution:** identity is carried by the exception; parent MUST NOT identify a failed task by re-running or probing work items (O-14). ✓

### §5 table row 2 + §6 item 2 (consistency updates)

§5 row 2 updated to reflect wrap-and-re-raise via `CalibrationWorkerError` (top-level picklable `_worker_calibration`; on failure narrowly wraps and re-raises picklable `CalibrationWorkerError` carrying identity; no swallowing, no partial result). §6 item 2 updated to require a worker exception to raise `CalibrationWorkerError` and the parent to emit the exact §4.2 failure record with correct identity sourced from the exception, fail closed, discard all calibration results, dispatch no simulation. ✓ Both consistent with the amended §4.1/§4.2/§4.2.1.

---

## Why Option 1 over Options 2 and 3 — sound rationale

- **Option 2 (result-or-error protocol; worker never raises):** rejected — a larger worker-protocol change (worker catches all exceptions, returns a result-or-error record, waits for all calibrations to finish before parent-side failure handling, changes the dispatch mechanism away from plain `pool.map`). Sound rejection.
- **Option 3 (nullable identity fields when `pool.map` can't identify the failed task):** rejected — weakens the §4.2 failure record and accepts not knowing which task failed. Sound rejection.
- **Option 1** is the most constraint-preserving: `pool.map` remains the dispatch mechanism; failure stays exception-driven and fail-closed; no retry/re-execution to discover identity; no partial calibration table usable; surgical amendment rather than dispatch redesign. ✓

---

## Constraint preservation — VERIFIED

- **No-retry (O-14):** preserved — identity is carried by the exception; no re-execution to discover failure identity. No retry of calibration or simulation. ✓
- **Fail-closed:** preserved — first exception still terminates immediately; completed results discarded (pool.map does not return partial results on exception); no partial calibration table; no simulation work item built or dispatched after a calibration failure. Parent catches `CalibrationWorkerError` solely to emit the sanitized record and terminate non-zero. ✓
- **Calibration algorithm and all protected scientific logic:** unchanged — `calibrate_sigma_dose` numerical algorithm and return value; the 15-element calibration domain; one calibration result per `(alpha, v_mult)` identity; `combo_seed` and per-simulation RNG; the §2 XF-5 estimator; both false-kill aggregations; null-control; sensitivity-map construction; deterministic selection rule; misspecified profiles; R8 guard; write-order fix; three NF-IMPL fixes; BF-MP-1 multiprocessing. ✓
- **Candidate-blindness (Ruling 9, Entry 76):** preserved — calibration and simulation remain synthetic/oracle-only; no candidate output is an input. The exception channel carries only apparatus-parameter identity (ordinal, alpha, v_mult) and sanitized error text — no candidate data. ✓
- **Reproducibility (§4.9):** unaffected — the happy path (no exceptions) is unchanged; `sigma_dose` values and all downstream scientific fields remain identical between `workers=1` and `workers=N`. Failure handling is separate from the reproducibility standard. ✓
- **Artifact schema / JSON write order, O-15 diagnostic-only labeling, all fail-closed guards, all locked bars:** unchanged. ✓

---

## Scope check — PASS (surgical amendment)

Diff `90d8835...b4419f9` touches only `specs/l8_calibration_parallelism_spec.md` (+20/−6) and `specs/l8_calibration_parallelism_spec_changelog.md` (+41). No other files. The amendments are confined to title/status, §4.1, §4.2, new §4.2.1, §5 row 2, §6 item 2. The v1 content below the amended sections is byte-for-byte unchanged (confirmed by diff). No scope creep.

---

## §5 P1–P6 compliance

- **P1 (repo-first, no reconstruction):** PASS — no new law text; existing verbatim quotes retained from v1.
- **P2 (verbatim quotation):** PASS — the v1 §2 quotes (O-14, O-15, Ruling 9, §5 P1, §5 P3) are retained (the amendment did not touch §2). The v1 non-blocking P2 imperfections (truncated P1 quote — NF-CPS-1; paraphrased Ruling 9 quote — NF-CPS-2) carry forward unchanged; still non-blocking.
- **P3 (source-class tags):** PASS — no new numeric parameters, thresholds, kill conditions, or test criteria introduced. `CalibrationWorkerError` is an implementation mechanism (exception class), not a numeric threshold/kill condition/test criterion; P3 (which governs numeric thresholds) does not require a tag for it. Its constructor fields mirror the already-present v1 §4.2 failure-record fields. No new `[PROPOSED]` parameter. ✓
- **P4 (regime dating):** PASS — header states date 2026-08-19, Regime B, post-Entry 81 (retained).
- **P5 (deviation memorialization):** N/A — no deviation from `[LAW]` text (diagnostic scheduling optimization).
- **P6 (provenance citations):** PASS — citations unchanged from v1.

---

## Design soundness (fresh-eyes) — SOUND

- **The contradiction is real and the resolution addresses it directly:** pool.map propagates exceptions but not the failed input tuple; the identity-carrying picklable exception is the correct bridge — the worker attaches identity at the point of failure (where the input tuple is in scope), and the parent reads it from the propagated exception (without re-execution). ✓
- **Picklability correctly specified:** the requirement that `CalibrationWorkerError` and its fields be picklable (and must not carry numpy arrays/file handles/traceback objects) is the technical crux — without it, pool.map could not propagate the exception across the process boundary and the resolution would fail. Correctly identified and constrained. ✓
- **Sanitization is defensive and correct:** the parent builds the failure record from the `CalibrationWorkerError` fields only, never from `repr(e)`/`str(e.__cause__)`/traceback text — preventing the remote-worker traceback (which multiprocessing may attach and which can contain private paths/identifiers) from leaking into the O-15 log or artifact. This is the right pattern. ✓
- **Internally consistent and implementable:** §4.1 (wrap-and-re-raise) → §4.2.1 (exception contract) → §4.2 (parent sources identity from exception, emits record, terminates) form a coherent, unambiguous chain. The TASK BUILDER now has a single, unambiguous failure-identity handling path. No design decision is left to the TASK BUILDER (class name, constructor fields, picklability, sanitization source, no-re-execution all normatively fixed). ✓
- **Happy path unaffected:** the reproducibility standard (§4.9) and all downstream scientific fields are unchanged; failure handling is orthogonal. ✓

---

## Non-blocking findings

- **NF-CPS-3 (new, trivial — test-completeness suggestion):** §6 item 2 (fail-closed tests) requires the worker-exception test to assert the parent emits the exact §4.2 failure record with correct identity sourced from the exception, fails closed, discards results, dispatches no simulation. It does not explicitly require the test to assert that `exception_message` is sanitized (no private paths, no hostnames/SIDs/PII). The §4.2.1 normative sanitization requirement is clear; this is only a suggestion that the worker-exception test also assert sanitization completeness (e.g., that `exception_message` contains no `/home/...` path or hostname pattern). Not a spec defect; not a block.
- **NF-CPS-1 (carry-forward from v1):** the §5 P1 quote in §2 quotes the first sentence verbatim but omits the trailing clause " — the constitution is published; reconstruction is unnecessary and therefore prohibited." Quoted portion is exact. Still non-blocking (no law reconstruction; omitted clause is explanatory).
- **NF-CPS-2 (carry-forward from v1):** the Ruling 9 quote in §2 is a paraphrase rather than verbatim from Entry 76. Citation accurate; meaning preserved. Still non-blocking (P6 citation correctness holds; Ruling 9 is a provenance ruling, not constitutional law).

---

## Changelog attestation

The v1.1 changelog entry documents the contradiction, the Option 1 choice and rationale, the §4.1/§4.2/§4.2.1/§5-row-2/§6-item-2 amendments, the preserved constraints, and P1–P6 status. Matches the actual diff (verified: title/status, §4.1, §4.2, §4.2.1, §5 row 2, §6 item 2 amended; v1 content below unchanged). The changelog's pre-push-scan attestation correctly classifies the only pattern matches ("hostnames", "MAC addresses") as the spec's own sanitization prose, not actual identifiers. ✓

---

## Preserved evidence

The v1 spec content (except the surgically amended sections) is byte-for-byte unchanged. The base code (`7e296ec`) is unchanged. The frozen L8 instantiation spec v2.2 (`c7d7bed`) remains cited as input only. All prior CRITIC CLEARs (v1 spec review `a087654`) and the BF-MP-1 BLOCK findings remain valid. The amendment invalidates no prior evidence; it resolves an internal contradiction that the v1 review did not catch (the v1 review cleared §4.1/§4.2 individually but did not flag their interaction — the TASK BUILDER's stop-report surfaced it).

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

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

## Verdict and routing

**Verdict: CLEAR.** The §4.1/§4.2 contradiction is genuinely resolved via Option 1 (identity-carrying picklable `CalibrationWorkerError`). The amendment is surgical and internally consistent; the v1 content below the amended sections is byte-for-byte unchanged. No-retry (O-14), fail-closed, the calibration algorithm, all protected scientific logic, and candidate-blindness are preserved. P1–P6 maintained. The spec is now unambiguous and implementable on failure-identity handling; the TASK BUILDER receives no design decisions. One new trivial test-completeness observation (NF-CPS-3) plus the two carry-forward v1 P2/P6 imperfections, none blocking.

**Next authorized role:** WORKFLOW COORDINATOR → **Rebecca** (re-approve the amended spec) → **TASK BUILDER** (implement the approved spec) → **CRITIC** (code review: does the code match the approved spec? genuine reproducibility per §4.9/§6?) → **Rebecca** (authorize → rerun locally). Scoring remains gated behind the five standing M4 gates. Nothing herein authorizes scoring.

---

*This review was conducted read-only against the amended spec at `b4419f9` on `architect/l8-calibration-parallelism-spec`. No scoring, rerun, hold-out seed exposure, implementation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
