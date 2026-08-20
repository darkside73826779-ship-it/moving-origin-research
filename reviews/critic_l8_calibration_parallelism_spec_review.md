# CRITIC Spec Review — L8 Calibration Parallelism Spec v1

**Gate served:** CRITIC spec design review — design soundness and constraint preservation of the calibration parallelism specification
**Reviewer:** CRITIC (fresh-context, spec design review — not a code review)
**Date:** 2026-08-19 21:44 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — on CLEAR, Rebecca approves the spec, then TASK BUILDER implements, then CRITIC code review, then Rebecca authorizes.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Spec branch | `architect/l8-calibration-parallelism-spec` |
| Spec HEAD (under review) | `90d8835` |
| Spec | `specs/l8_calibration_parallelism_spec.md` (+202/-0) |
| Spec changelog | `specs/l8_calibration_parallelism_spec_changelog.md` (+45/-0) |
| Base code (the code the spec governs) | `diagnostics/l8_power_analysis.py` at `7e296ec` on `taskbuilder/l8-power-analysis` |
| L8 instantiation spec v2.2 (frozen parent, cited as input only) | `c7d7bed` on `architect/l8-instantiation-v2.2-fresh` |
| Constitution v1 / v2 | `docs/ARCHITECTURAL_CONSTITUTION.md` / `_v2.md` on main |
| Prior CRITIC multiprocessing review (BF-MP-1) | `cade0c5` on `critic/l8-multiprocessing-rereview` |

Read-only review. No spec, code, constitution, or scoring artifact modified (read-only + own review/handoff files). No scoring, seed execution, hold-out seed exposure, implementation, or unauthorized merge performed.

---

## Headline finding (CLEAR)

The spec is design-sound, constraint-preserving, and scope-fenced. All 10 design decisions are resolved normatively. The spec authorizes ONLY changing the scheduling of 15 calibration calls from serial to parallel within `diagnostics/l8_power_analysis.py` — nothing else. It directly and explicitly addresses the prior BF-MP-1 defect (worker outputs discarded → vacuous reproducibility): §4.9 requires value equality + byte-identical artifact + downstream scientific equality, and §6.3 guards that "the prior BF-MP-1 defect (worker outputs discarded, making the reproducibility test vacuous) must not recur." The TASK BUILDER receives no design decisions. Two non-blocking P2/P6 fidelity observations (a truncated P1 quote; a paraphrased Ruling 9 quote) require no action for clearance.

---

## The 10 design decisions — all resolved

| # | Decision | Spec section | Status |
|---|---|---|---|
| 1 | Worker function + data contract | §4.1 | **Resolved.** Top-level picklable `_worker_calibration`; fixed input `(ordinal, alpha, v_mult)`; fixed output keys `{ordinal, alpha, v_mult, sigma_dose}`; worker must NOT catch exceptions or produce partial results. Name fixed (TASK BUILDER may not choose alternative). ✓ |
| 2 | Failure semantics | §4.2 | **Resolved.** First-exception fail-closed (relies on `pool.map` propagation); no retry (O-14); completed results discarded; no simulation after calibration failure; sanitized failure record (log-only, not in artifact JSON). ✓ |
| 3 | Pool lifecycle | §4.3 | **Resolved.** Separate, sequential, context-managed pools; calibration pool closed/joined before simulation pool; "no nested pools" is a LOCKED lifecycle requirement (not an impl detail); one explicit lifecycle per phase. ✓ |
| 4 | Worker allocation | §4.4 | **Resolved.** `min(requested_workers, 15)`; classified as resource hygiene (not a scientific bar); tagged `[PROPOSED — resource-hygiene implementation constraint; derived from frozen ALPHAS × V_MULTS]`. ✓ |
| 5 | Reference/stress reuse | §4.5 | **Resolved.** No cross-profile caching; each analysis independently invokes `calibrate_sigma_dose` (reuses the function, not a cached table) — preserves the "test estimator overfit" semantics. ✓ |
| 6 | Result identity validation | §4.6 | **Resolved.** Exact set equality of 15 `(alpha, v_mult)` identities; fail-closed before any simulation dispatch; order-preserving `pool.map` keyed by identity. ✓ |
| 7 | Progress reporting | §4.7 | **Resolved.** Separate O-15 calibration progress line; deterministic ordering (progress does not drive result order); diagnostic-log-only (not in artifact JSON). ✓ |
| 8 | Artifact compatibility | §4.8 | **Resolved.** Byte-compatible schema; no new subphase fields; `elapsed_seconds` unchanged (total run, inherently non-deterministic); timing/progress in logs only. ✓ |
| 9 | Reproducibility comparison | §4.9 | **Resolved (genuinely non-vacuous).** Requires BOTH (a) exact Python `==` equality of all 15 `sigma_dose` values AND (b) byte-identical serialized artifact (post-`_sanitize_nan`, `indent=2`, `allow_nan=False`, excluding `elapsed_seconds`) AND (c) exact downstream scientific equality (mean β*, std, both false-kill rates, false-pass, n_valid, instrument failures, region, min-distance, all sensitivity-map cells, selection). Exact standard — tolerance-based comparison not permitted. ✓ |
| 10 | Performance verification | §4.10 | **Resolved.** No numeric speedup/utilization bar; requires demonstrated non-serial calibration execution + process observation (>1 worker active during calibration on a multicore system), tagged `[PROPOSED — diagnostic implementation check]`; failure blocks implementation sign-off but is not a scientific result or bar. ✓ |

**All 10 resolved. No design decision left to the TASK BUILDER** (worker name, input/output shapes, failure semantics, pool lifecycle, allocation formula, reuse decision, identity validation, progress, artifact compatibility, reproducibility standard, performance verification are all normatively fixed).

---

## Constraint preservation — VERIFIED (§7, §1.3, §10)

The spec explicitly preserves, unchanged: `calibrate_sigma_dose` numerical algorithm and return value; the 15-element calibration domain (frozen `ALPHAS` × `V_MULTS`); one calibration result per `(alpha, v_mult)` identity reused by all 16 `(C_min, eta)` cells; `combo_seed` and all per-simulation RNG derivations; the §2 XF-5 estimator; both false-kill aggregations; the null-control calculation; the sensitivity-map construction; the deterministic selection rule; the misspecified profiles; candidate-blindness (Ruling 9); O-15 diagnostic-only labeling; all fail-closed guards; the JSON write order and artifact schema; the R8 guard; the write-order fix; and the three NF-IMPL fixes. No locked bar, control, selection logic, or scoring logic is changed. ✓

The spec is a pure scheduling optimization: parallelizing 15 mutually-independent, deterministic `(alpha, v_mult)` calibrations. Since each calibration's value depends only on its `(alpha, v_mult)` identity (seeded from `combo_seed(alpha, v_mult, CAL_REF_C_MIN, CAL_REF_ETA)`), parallelizing their invocation changes only scheduling, not values — the spec correctly identifies this in §3. ✓

---

## Scope fence — VERIFIED, no scope creep (§1.2, §1.3, §10)

The spec authorizes ONLY:
- Changing the scheduling of the 15 calibration calls from serial to parallel within `diagnostics/l8_power_analysis.py`
- A new top-level calibration worker (`_worker_calibration`)
- A separate calibration pool lifecycle
- Focused multiprocessing tests
- O-15 diagnostic progress

It must NOT be read to authorize modification of: the L8 instantiation spec, the constitution, STATE.md, the provenance log, `calibrate_sigma_dose` itself, `combo_seed`, any per-simulation RNG derivation, the §2 XF-5 estimator, the false-kill aggregations, the null-control calculation, the sensitivity-map construction, the deterministic selection rule, the misspecified profiles, the artifact schema or JSON write order, candidate-blindness, the R8 guard, the write-order fix, or the three NF-IMPL fixes. No locked bar, control, scoring logic, or scientific interpretation is changed. ✓

---

## Design soundness (fresh-eyes) — SOUND

- **Pool-lifecycle design:** Sound. Separate, sequential, context-managed pools; calibration pool closed/joined before simulation pool starts; "no nested pools" locked as a lifecycle requirement. This avoids nested-pool deadlocks and is the correct pattern for independent calibration work preceding simulation. ✓
- **Failure semantics:** Correct fail-closed. First-exception terminates (relies on `pool.map`'s built-in propagation — no custom retry); completed results discarded; no simulation after calibration failure; no partial calibration table; sanitized failure record log-only. Consistent with O-14 (no re-run-on-failure). ✓
- **Reproducibility comparison:** Genuinely non-vacuous — requires value equality + byte identity + downstream scientific equality, all exact (no tolerance). §6.3 explicitly guards against the prior BF-MP-1 vacuous-reproducibility defect ("using the actual consumed calibration table, not a vacuous comparison"). This directly closes the loophole I flagged in `cade0c5`. ✓
- **Reference/stress reuse:** Correct. No cross-profile caching — each analysis independently re-invokes `calibrate_sigma_dose`, preserving the "test estimator overfit to the reference profile" semantics (a cached reference table would change runtime behavior and is not authorized). ✓
- **No design decisions left to the TASK BUILDER:** The spec normatively fixes all 10 decisions (worker name, I/O shapes, failure semantics, pool lifecycle, allocation formula, reuse, identity validation, progress, artifact compatibility, reproducibility standard, performance verification). ✓

---

## §5 P1–P6 compliance

- **P1 (repo-first, no reconstruction):** PASS. All governance text quoted from repo sources (§2). No law text reconstructed. The P1 quote is a verbatim-portion (see NF-CPS-1), not a reconstruction.
- **P2 (verbatim quotation):** PASS with one non-blocking imperfection. O-14, O-15, §5.2 O-15, and §5 P3 quotes are verbatim (verified byte-for-byte against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` and `docs/rulings/REBECCA_M3_GO.md` / `REBECCA_M3_DELIVERY_RULING.md`). The §5 P1 quote is truncated — it quotes the first sentence verbatim but omits the trailing clause " — the constitution is published; reconstruction is unnecessary and therefore prohibited." (NF-CPS-1).
- **P3 (source-class tags):** PASS. The spec introduces no new scientific apparatus parameters or performance bars. All scientific counts derive from the frozen, already-tagged `ALPHAS` × `V_MULTS` domain. Two diagnostic implementation criteria are tagged: the worker-allocation cap `min(requested_workers, 15)` `[PROPOSED — resource-hygiene implementation constraint; derived from frozen ALPHAS × V_MULTS]` (§4.4) and the process-observation check `[PROPOSED — diagnostic implementation check]` (§4.10). Neither gates a scientific result. No numeric performance/speedup bar introduced. ✓
- **P4 (regime dating):** PASS. Header states date 2026-08-19, Regime B, post-Entry 81. ✓
- **P5 (deviation memorialization):** N/A. The spec deviates from no `[LAW]` text — it is a diagnostic scheduling optimization that does not operationalize a scientific law or alter any locked bar. ✓
- **P6 (provenance citations):** PASS with one non-blocking imperfection. The `[Entry 76]` citation (Ruling 9) is correct — Ruling 9 exists in Entry 76 and says what the spec represents. However, the Ruling 9 quote in §2 is a paraphrase, not verbatim from the log (actual: "candidate's diagnostic seeds 101–105 NOT inputs; oracle/synthetic-ground-truth only"; spec rewords to "the candidate's diagnostic-seed results 101-105 are NOT inputs; only oracle/synthetic-ground-truth is"). (NF-CPS-2).

---

## Non-blocking findings

- **NF-CPS-1 (P2 — truncated P1 quote):** The §5 P1 quote in §2 quotes the first sentence verbatim but omits the trailing clause " — the constitution is published; reconstruction is unnecessary and therefore prohibited." The quoted portion is exact (no paraphrase). For maximal P2 fidelity, quote the full sentence verbatim. Not a block — no law reconstruction occurred (P1 satisfied), and the omitted clause is explanatory, not operative.
- **NF-CPS-2 (P6 — paraphrased Ruling 9 quote):** The Ruling 9 quote in §2 is a paraphrase rather than verbatim from Entry 76 (the spec rewords "candidate's diagnostic seeds 101–105 NOT inputs; oracle/synthetic-ground-truth only" into "the candidate's diagnostic-seed results 101-105 are NOT inputs; only oracle/synthetic-ground-truth is" and adds "oracle/synthetic-grounded,"). The `[Entry 76]` citation is accurate and the meaning is preserved. For P6 fidelity, quote Entry 76 Ruling 9 verbatim. Not a block — the citation is correct, no law text reconstructed, and Ruling 9 is a provenance ruling (P6 governs citation accuracy, which holds) rather than constitutional law (P2 verbatim).

---

## Candidate redesign disposition (§5)

The TASK BUILDER's 8-point candidate redesign is adopted with 7 hardening modifications (§5 table): (i) input record carries `ordinal`; (ii) no nested pools is a locked requirement; (iii) worker-allocation cap classified as resource hygiene (no new scientific tag); (iv) no cross-profile calibration caching; (v) artifact schema byte-compatible, no new subphase fields; (vi) reproducibility requires both sigma_dose exact equality and byte-identical artifact plus downstream scientific equality; (vii) no numeric performance bar. The modifications sharpen the proposal and close the prior BF-MP-1 loophole. ✓

---

## Verification obligations (§6)

The TASK BUILDER's recommended verification list is adopted with modifications (sharpened reproducibility standard; no scoring). All verification is O-15 diagnostic-only: dispatch-once/consume-once, fail-closed tests (missing/duplicate/unexpected identity + worker exception), genuine single-vs-multi diagnostic using the actual consumed table, calibration value equality, artifact byte identity, downstream scientific equality, protected-logic static/diff check, process observation, no scoring. ✓ This is a sound, complete verification program that directly prevents the prior vacuous-reproducibility recurrence.

---

## Preserved evidence

The frozen L8 instantiation spec v2.2 (`c7d7bed`) is cited as input source only and is not modified. The base code (`7e296ec`) is the functional BF-MP-1 remediation baseline per the Coordinator handoff (the spec branches from it; it does not merge `7e296ec` and `c7d7bed`). All prior CRITIC CLEARs and the BF-MP-1 BLOCK findings remain valid. The spec does not invalidate any prior evidence.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the spec, code, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No implementation (deferred to TASK BUILDER after Rebecca approves the spec).
- No L15/L16/L17 before M5.
- No touching the calibration algorithm, combo seeds, estimator, false-kill formulas, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, write-order fix, or the three NF-IMPL fixes (all preserved by the spec).

---

## Verdict and routing

**Verdict: CLEAR.** The L8 calibration parallelism spec v1 is design-sound, constraint-preserving, and scope-fenced. All 10 design decisions are resolved normatively; the TASK BUILDER receives no design decisions. The spec authorizes only a diagnostic scheduling optimization (serial→parallel for 15 independent calibrations) and changes no scientific result, locked bar, or scoring logic. It directly addresses the prior BF-MP-1 defect (genuinely non-vacuous reproducibility standard in §4.9/§6.3). Two non-blocking P2/P6 fidelity observations (truncated P1 quote; paraphrased Ruling 9 quote) require no action for clearance but could be tightened to verbatim for full fidelity.

**Next authorized role:** WORKFLOW COORDINATOR → Rebecca (approve the spec) → TASK BUILDER (implement the approved spec, local frontier GPT) → CRITIC (code review: does the code match the approved spec? genuine reproducibility per §4.9/§6?) → Rebecca (authorize → rerun locally). The CRITIC sees the spec first (this design review), then the finished implementation (code review) — two passes on different artifacts, no double-dipping. Scoring remains gated behind the five standing M4 gates. Nothing herein authorizes scoring.

---

*This review was conducted read-only against the spec at `90d8835` on `architect/l8-calibration-parallelism-spec`. No scoring, rerun, hold-out seed exposure, implementation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
