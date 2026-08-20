# CRITIC Handoff — Return to WORKFLOW COORDINATOR: L8 Calibration Parallelism Spec Review

**From:** CRITIC (fresh-context, spec design review)
**To:** WORKFLOW COORDINATOR
**Date:** 2026-08-19 21:44 EDT
**Gate served:** CRITIC spec design review — design soundness and constraint preservation of the calibration parallelism specification
**Verdict:** **CLEAR**
**Review artifact:** `reviews/critic_l8_calibration_parallelism_spec_review.md` on `critic/l8-calibration-parallelism-spec-review` (SHA below)

---

## Authorization context

The ARCHITECT drafted the L8 calibration parallelism spec v1, resolving the 10 design decisions the TASK BUILDER identified. This is the design review pass (is the design correct and safe?), not a code review (no code exists yet). The CRITIC sees the finished implementation in a second pass after the TASK BUILDER implements the approved spec.

---

## SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Spec branch | `architect/l8-calibration-parallelism-spec` |
| Spec HEAD (under review) | `90d8835` |
| Spec | `specs/l8_calibration_parallelism_spec.md` (+202/-0) |
| Spec changelog | `specs/l8_calibration_parallelism_spec_changelog.md` (+45/-0) |
| Base code (the code the spec governs) | `diagnostics/l8_power_analysis.py` at `7e296ec` on `taskbuilder/l8-power-analysis` |
| L8 instantiation spec v2.2 (frozen parent, cited as input only) | `c7d7bed` on `architect/l8-instantiation-v2.2-fresh` |
| Prior CRITIC multiprocessing review (BF-MP-1) | `cade0c5` on `critic/l8-multiprocessing-rereview` |

---

## Verdict: CLEAR

The spec is design-sound, constraint-preserving, and scope-fenced. All 10 design decisions are resolved normatively. The spec authorizes ONLY changing the scheduling of 15 calibration calls from serial to parallel within `diagnostics/l8_power_analysis.py` — nothing else. It directly and explicitly addresses the prior BF-MP-1 defect (worker outputs discarded → vacuous reproducibility): §4.9 requires value equality + byte-identical artifact + downstream scientific equality, and §6.3 guards that the prior BF-MP-1 defect must not recur. The TASK BUILDER receives no design decisions. Two non-blocking P2/P6 fidelity observations require no action for clearance.

---

## All 10 design decisions — resolved

1. Worker function + data contract (§4.1): `_worker_calibration`, top-level picklable, fixed input `(ordinal, alpha, v_mult)`, fixed output keys `{ordinal, alpha, v_mult, sigma_dose}`, no exception catching. ✓
2. Failure semantics (§4.2): first-exception fail-closed (relies on `pool.map` propagation), no retry (O-14), discard completed results, no simulation after failure, sanitized failure record log-only. ✓
3. Pool lifecycle (§4.3): separate sequential context-managed pools; calibration pool closed before simulation pool; "no nested pools" locked as a lifecycle requirement. ✓
4. Worker allocation (§4.4): `min(requested_workers, 15)`; classified as resource hygiene (not a scientific bar); tagged `[PROPOSED — resource-hygiene implementation constraint]`. ✓
5. Reference/stress reuse (§4.5): no cross-profile caching; each analysis independently re-invokes `calibrate_sigma_dose` (preserves overfit-test semantics). ✓
6. Result identity validation (§4.6): exact set equality of 15 identities; fail-closed before simulation; order-preserving `pool.map` keyed by identity. ✓
7. Progress reporting (§4.7): separate O-15 calibration progress; deterministic ordering; diagnostic-log-only. ✓
8. Artifact compatibility (§4.8): byte-compatible schema; no new subphase fields; `elapsed_seconds` unchanged; timing in logs only. ✓
9. Reproducibility comparison (§4.9): genuinely non-vacuous — BOTH value equality (15 `sigma_dose` `==`) AND byte-identical artifact (excluding `elapsed_seconds`) AND exact downstream scientific equality; exact standard, no tolerance. ✓
10. Performance verification (§4.10): no numeric speedup bar; demonstrated non-serial execution + process observation (>1 worker active); tagged `[PROPOSED — diagnostic implementation check]`. ✓

**No design decision left to the TASK BUILDER.**

---

## Constraint preservation — VERIFIED

The spec preserves, unchanged: `calibrate_sigma_dose` algorithm/return, the 15-element domain, one result per identity reused by 16 cells, `combo_seed` + all per-simulation RNG, the §2 XF-5 estimator, both false-kill aggregations, null-control, sensitivity-map construction, deterministic selection rule, misspecified profiles, candidate-blindness (Ruling 9), O-15 labeling, fail-closed guards, JSON write order/schema, R8 guard, write-order fix, three NF-IMPL fixes. No locked bar, control, selection logic, or scoring logic changed. The spec is a pure scheduling optimization: parallelizing 15 mutually-independent deterministic calibrations changes only scheduling, not values.

---

## Scope fence — VERIFIED, no scope creep

Authorizes ONLY: serial→parallel scheduling of 15 calibrations within `l8_power_analysis.py`, a new top-level `_worker_calibration`, a separate calibration pool lifecycle, focused tests, O-15 progress. Does NOT authorize modification of the spec, constitution, STATE.md, provenance log, `calibrate_sigma_dose` itself, `combo_seed`, RNG, estimator, false-kill formulas, null-control, sensitivity map, selection rule, profiles, artifact schema, JSON write order, candidate-blindness, R8 guard, write-order fix, or the three NF-IMPL fixes.

---

## Design soundness (fresh-eyes) — SOUND

- Pool-lifecycle: separate sequential context-managed pools; no nested pools locked — avoids deadlocks. ✓
- Failure semantics: first-exception fail-closed, no retry (O-14), no partial table, no simulation after failure — correct fail-closed. ✓
- Reproducibility: genuinely non-vacuous (value + byte + downstream scientific equality, exact, no tolerance); §6.3 explicitly guards against the prior BF-MP-1 vacuous-reproducibility recurrence. ✓
- Reference/stress reuse: no cross-profile caching — preserves the overfit-test semantics. ✓
- No design decisions left to the TASK BUILDER. ✓

---

## §5 P1–P6 compliance

- **P1:** PASS — no law reconstruction; governance quoted from repo.
- **P2:** PASS (one non-blocking imperfection — NF-CPS-1). O-14, O-15, §5.2 O-15, §5 P3 verified verbatim byte-for-byte. The §5 P1 quote is truncated (verbatim portion; omits trailing explanatory clause).
- **P3:** PASS — no new scientific apparatus parameters or performance bars; two diagnostic implementation criteria tagged `[PROPOSED]`; neither gates a scientific result.
- **P4:** PASS — date 2026-08-19, Regime B, post-Entry 81.
- **P5:** N/A — no deviation from `[LAW]` text (diagnostic scheduling optimization).
- **P6:** PASS (one non-blocking imperfection — NF-CPS-2). The `[Entry 76]` citation (Ruling 9) is correct; the Ruling 9 quote is a paraphrase rather than verbatim from the log.

---

## Non-blocking findings

- **NF-CPS-1 (P2 — truncated P1 quote):** The §5 P1 quote quotes the first sentence verbatim but omits the trailing clause " — the constitution is published; reconstruction is unnecessary and therefore prohibited." The quoted portion is exact. For maximal P2 fidelity, quote the full sentence verbatim. Not a block — no law reconstruction (P1 satisfied); omitted clause is explanatory.
- **NF-CPS-2 (P6 — paraphrased Ruling 9 quote):** The Ruling 9 quote is a paraphrase rather than verbatim from Entry 76 (spec rewords "candidate's diagnostic seeds 101–105 NOT inputs; oracle/synthetic-ground-truth only"). The `[Entry 76]` citation is accurate and meaning preserved. For P6 fidelity, quote Entry 76 Ruling 9 verbatim. Not a block — citation correct, no law reconstructed, Ruling 9 is a provenance ruling (P6 governs citation accuracy, which holds).

---

## Candidate redesign + verification obligations

The TASK BUILDER's 8-point candidate redesign is adopted with 7 hardening modifications (ordinal field; no-nested-pools locked; cap as resource hygiene; no cross-profile caching; byte-compatible schema; both value + byte + downstream scientific reproducibility; no numeric performance bar). The §6 verification program (dispatch-once/consume-once, fail-closed tests, genuine single-vs-multi using the consumed table, value/byte/scientific equality, protected-logic diff check, process observation, no scoring) is sound and complete — directly prevents the prior vacuous-reproducibility recurrence.

---

## Preserved evidence

The frozen L8 instantiation spec v2.2 (`c7d7bed`) is cited as input only and not modified. The base code (`7e296ec`) is the functional BF-MP-1 remediation baseline per the Coordinator handoff (the spec branches from it; does not merge `7e296ec` and `c7d7bed`). All prior CRITIC CLEARs and the BF-MP-1 BLOCK findings remain valid. The spec invalidates no prior evidence.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this handoff artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the spec, code, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No implementation (deferred to TASK BUILDER after Rebecca approves the spec).
- No L15/L16/L17 before M5.
- No touching the calibration algorithm, combo seeds, estimator, false-kill formulas, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, write-order fix, or the three NF-IMPL fixes (all preserved by the spec).

---

## Next authorized role / routing

**Next recipient:** WORKFLOW COORDINATOR → **Rebecca** (approve the spec) → **TASK BUILDER** (implement the approved spec, local frontier GPT) → **CRITIC** (code review: does the code match the approved spec? genuine reproducibility per §4.9/§6?) → **Rebecca** (authorize → rerun locally).

The CRITIC sees the spec first (this design review), then the finished implementation (code review) — two passes on different artifacts, no double-dipping. On CLEAR (this case), Rebecca approves the spec. On BLOCK, returns to ARCHITECT. Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

---

*This handoff was produced read-only against the spec at `90d8835` on `architect/l8-calibration-parallelism-spec`. No scoring, rerun, hold-out seed exposure, implementation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
