# ARCHITECT Handoff — M4 Spec v1.4 (Step 6 Amendments)

**Gate served:** Step 6 of Principal's M4 gate resolution sequence
**Issued by:** ARCHITECT
**Date:** 2026-08-18 20:55 EDT
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)

---

## SHAs

| Item | SHA | Location |
|---|---|---|
| Base (v1.3.1, R2-CLEARED) | `94dcc43` | `architect/m4-spec-v1.3` |
| v1.4 HEAD | (to be verified after push) | `architect/m4-spec-v1.4` |
| Main HEAD | `1fda268` | `main` |

## Files

| File | Description |
|---|---|
| `specs/m4_specification.md` | M4 spec v1.4 (5 amendments applied) |
| `specs/m4_specification_changelog.md` | Changelog with v1.4 entry |

## Five amendments

### Amendment 1: FWFP closure deliverable (§7.3)

**Named deliverable:** M4 Pre-Scoring FWFP Closure Audit
**Owner:** TASK BUILDER (computation under O-15)
**Acceptance criteria:** (1) All stochastic families × checks per arm enumerated; (2) FWFP computed per arm; (3) Arms >5% corrected; (4) Corrected FWFP ≤5% all arms; (5) Documented in committed artifact; (6) CRITIC-reviewed before scoring.
**Corrected-alpha target:** ≤5% per arm [BAR-Entry 43]
**Build-sequence placement:** Step 8 (TASK BUILDER), pre-scoring sub-step. Must be CRITIC-cleared before Rebecca authorizes scoring.
**Role boundary:** ARCHITECT specifies the deliverable; TASK BUILDER computes and corrects.

### Amendment 2: Borderline pre-registration (§7.4)

Three draft options for Rebecca's ruling:
- **B1 (M3 precedent):** Label retained; provisional advancement possible [PROPOSED — requires Rebecca ruling]
- **B2 (Strict KILL):** Any borderline firing → KILL [PROPOSED — requires Rebecca ruling]
- **B3 (Conditional):** Rebecca rules at delivery gate [PROPOSED — requires Rebecca ruling]

Pre-registration requirement per [LAW-L19]. No option implemented.

### Amendment 3: L7 fallback clarification (§2.5)

All-seeds-direction + bootstrap-CI fallback [BAR-Entry 11.3] applies ONLY to direction tests (e.g., L8 monotonicity). L7 threshold bars (AUROC, ECE, margin) are per-seed: any-seed-fail → immediate KILL, no fallback.

### Amendment 4: L8 homeostatic-variable named prerequisite (§3.3.1)

Elevated from §12 line item to named prerequisite with dedicated CRITIC reviewer pass. Four criteria: regulable [LAW-L8], target defined [PROPOSED], calibratable noise dose [OP-Entry 11.7], constructible specificity control [LAW-L8]. Placed in build sequence after spec approval, before TASK BUILDER implementation.

### Amendment 5: §8 Option A amendment (Step 4 ruling [BAR-Entry 72])

L3 row changed from "Parallel, not blocking" to "Prerequisite for scoring." Build proceeds in parallel; scoring gated on L3 resolution on fresh seeds per governance paper §6.3(3). Sequencing note added with gate sequence. Governance paper unamended.

## Confirmation

- No locked bar, kill condition, or scoring predicate changed.
- No law text modified. No reconstruction.
- All new thresholds tagged [PROPOSED] or appropriate source class (P3).
- Provenance citations verified: Entry 43 (FWFP standing rule), Entry 72 (Step 4 ruling) (P6).
- Regime dating in header (P4).
- Law quotes unchanged from v1.3.1 (P2 — verbatim quotation maintained).

## Next recipient

**CRITIC** (fresh-context reviewer) for delta re-clear with law-diff table. Then **WORKFLOW COORDINATOR** for Step 7 package assembly.

## Explicitly prohibited

- No merging to main (Rebecca sole merge authority)
- No scoring, seed execution, or hold-out seed exposure
- No rerun of seeds 201–203 / 301–303 (O-14)
- No L15/L16/L17 work before M5
- No modification of STATE.md or provenance_log.md
- No amendment to governance paper §6.3 (Option A leaves it unamended)
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label
