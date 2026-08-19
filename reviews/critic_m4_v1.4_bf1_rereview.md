# CRITIC BF1 Re-Review — M4 Spec v1.4 Remediation (Step 6 Exit)

**Gate served:** Step 6 delta re-clear exit — CRITIC re-review of ARCHITECT's BF1 remediation
**Reviewer:** CRITIC (re-initialized, fresh-context reviewer — same session as v1.4 BLOCK review)
**Date:** 2026-08-18 · **Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Review branch:** `critic/r2-m4-v1.3-law-fidelity`
**Baseline (prior v1.4 BLOCK):** `reviews/critic_m4_v1.4_delta_review.md` @ `c95f9db` — verdict BLOCK, finding BF1
**Spec under re-review:** `architect/m4-spec-v1.4` @ `9dff1e5` (remediation commit `9dff1e5`; baseline `8740c46`, v1.4)
**Pre-registration source:** `docs/rulings/M0_DECISION_SHEET.md` line 21 (published Entry 70, G0-4)
**Provenance source:** `docs/rulings/provenance_log.md` (Entry 70)
**Role boundary:** Read-only re-review. No modification of spec, constitution, STATE.md, provenance log, or any artifact. No scoring, no seed execution, no hold-out exposure, no merge.

---

## Verdict

### **CLEAR**

The ARCHITECT remediated BF1 within the exact authorized scope. Both missing L8 locked bars (Spearman ρ ≥ 0.8, standardized slope ≥ 0.2) are added to the L8 §3.2 locked-bars table with correct values matching the M0_DECISION_SHEET exactly, sourced `[BAR-Entry 11]` (Entry 70 / sheet line 21). The ≥3-doses tag is reconciled to `[BAR-Entry 11]` as primary, with `[OP-Entry 11.7]` retained as supplemental §9 operationalization record. The scope-violation check confirms the delta `8740c46..9dff1e5` touches only the BF1 items + changelog — no other threshold, locked bar, kill condition, scoring predicate, law text, or v1.4 amendment changed. Changelog v1.4.1 entry present. Step 6 exit criterion met.

---

## 1. BF1 remediation verification — ALL REMEDIATED

### BF1.a — Spearman ρ ≥ 0.8 added — PASS

Added to L8 §3.2 locked-bars table:
> | Spearman ρ (monotonic) | ≥ 0.8 | [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70) |

**Value match (sheet line 21):** M0_DECISION_SHEET states "Spearman ρ ≥ 0.8 monotonic." Spec value ρ ≥ 0.8 matches exactly — not raised, lowered, or reinterpreted. ✓
**Source tag:** `[BAR-Entry 11]` (Entry 70 / M0_DECISION_SHEET line 21). Correct per Entry 70's confirmation that L8 bars are sourced `[BAR-Entry 11]`. ✓

### BF1.b — Standardized slope ≥ 0.2 added — PASS

Added to L8 §3.2 locked-bars table:
> | Standardized slope | ≥ 0.2 | [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70) |

**Value match (sheet line 21):** M0_DECISION_SHEET states "standardized slope ≥ 0.2 (ARCHITECT's candidate accepted)." Spec value slope ≥ 0.2 matches exactly — not raised, lowered, or reinterpreted. ✓
**Source tag:** `[BAR-Entry 11]` (Entry 70 / M0_DECISION_SHEET line 21). Correct. ✓

### BF1.c — ≥3-doses tag reconciled — PASS

> | Minimum dose levels | ≥ 3 | [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70) |

Previously `[OP-Entry 11.7] (adopted from CRITIC Risk 2, Entry 7)`; now `[BAR-Entry 11]` (primary). Value ≥ 3 unchanged. ✓
**Reconciliation note (in spec):** "The ≥3-doses bar was previously tagged [OP-Entry 11.7] (supplemental). The M0_DECISION_SHEET (published via G0-4, Entry 70) attributes all L8 bars including ≥3 doses to [BAR-Entry 11] as Rebecca-locked bars. The sheet's framing is canonical; [BAR-Entry 11] is now the primary tag. [OP-Entry 11.7] remains as the §9 operationalization record that adopted the ≥3-level requirement from CRITIC Risk 2 (Entry 7) into the spec." ✓ — matches the remediation guidance: `[OP-Entry 11.7]` retained as supplemental only, canonical attribution `[BAR-Entry 11]`.

### M0_DECISION_SHEET quotation (fidelity) — PASS

The spec now includes the sheet's L8 row verbatim (line 21) for fidelity:
> "**L8** | ≥3 noise doses; Spearman ρ ≥ 0.8 monotonic; standardized slope ≥ 0.2 (ARCHITECT's candidate accepted); specificity control mandatory (self-irrelevant dose must NOT move regulation error). Seeds: 5." [BAR-Entry 11]

Verified against the actual `docs/rulings/M0_DECISION_SHEET.md` line 21 — exact match. ✓

### Unchanged L8 rows (preserved)

- Monotonic test: All-seeds-direction + bootstrap-CI fallback `[BAR-Entry 11.3]` — unchanged. ✓
- Seeds: 5 `[BAR-Entry 11.3]` — unchanged. ✓
- Specificity ("only then"): `[LAW-L8]` — unchanged. ✓

---

## 2. Scope-violation check — CLEAN

Diff `8740c46..9dff1e5` (2 files, +28/−1):

| File | Change | Scope |
|---|---|---|
| `specs/m4_specification.md` | L8 §3.2 table: two bars added, ≥3-doses tag reconciled, M0_DECISION_SHEET quotation + reconciliation note added (+8/−1) | Authorized (BF1.a/b/c) |
| `specs/m4_specification_changelog.md` | v1.4.1 changelog entry (+21) | Authorized (changelog) |

**Confirmed NO changes to:** any other threshold value, locked bar, kill condition, scoring predicate, law text, or any of the five v1.4 amendments (FWFP closure, borderline pre-reg, L7 fallback, L8 prerequisite, §8 Option A — all previously cleared). The delta is confined to the L8 §3.2 table region only. No law text modified (P1 preserved — the M0_DECISION_SHEET quotation is a pre-registration citation, not constitution law text).

---

## 3. Changelog — PASS

`specs/m4_specification_changelog.md` v1.4.1 entry present, documenting:
- Two missing locked L8 bars added (Spearman ρ ≥ 0.8, standardized slope ≥ 0.2), sourced `[BAR-Entry 11]`.
- M0_DECISION_SHEET quotation included for fidelity.
- ≥3-doses tag reconciled to `[BAR-Entry 11]` (primary); `[OP-Entry 11.7]` retained as §9 operationalization record.
- Confirmation: "No existing threshold value, locked bar, kill condition, or scoring predicate changed. No law text modified. No reconstruction. Only two missing bars added and one tag reconciled." ✓

---

## 4. Preserved evidence (carried from v1.4 review, unaffected by remediation)

The BF1 remediation added two locked bars + reconciled one tag only; it did not alter any prior-verified evidence:
- Five v1.4 amendments (1–5): all previously cleared — FWFP specified-not-performed; borderline options no self-selection; L7 fallback resolves §2.5 tension; L8 prerequisite with reviewer pass; §8 matches Option A (Entry 72).
- Law-diff (P2): L7/L8/L10/L14/L18 verbatim match constitution v1; line citations correct.
- P6 provenance: Entries 5/8/11.x/14/27/43/52/70/72 verified against log/sheet text.
- Other locked bars (L7 0.75/0.10/margin, L10 50%/10% + 0.70 floor, L14 d≥0.5 / corr≥0.3, L8 ≥3 doses/ρ≥0.8/slope≥0.2) — all now present and correctly valued.
- INSTRUMENT FAILURE label and M3 verdicts preserved.
- L15–L17 fence respected; P4 v1.4 header present; O-14/O-15/D1–D5/L9/L18/hold-out rules binding.

The two newly added L8 bars bring the spec's L8 locked-bars table into agreement with the M0_DECISION_SHEET (the canonical pre-registration). The JUDGE can now apply all L8 bars.

---

## 5. Pre-push self-scan attestation

A pre-push scan was performed on this re-review file and commit contents. No credentials, API keys, tokens, passwords, secrets, PII, machine identifiers, or private absolute paths found. Only repository-relative paths and already-public SHAs referenced. Findings: none. Classification: acceptable.

---

## 6. Prohibited-action confirmations

- No modification of the spec, constitution, STATE.md, provenance log, or any artifact under review. Only this re-review file was created and committed (the spec file was not touched on this branch — review-only commit).
- No merge to main (branch `critic/r2-m4-v1.3-law-fidelity` only; Rebecca sole merge authority).
- No scoring, no seed execution, no hold-out seed exposure.
- No L15/L16/L17 work before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- No re-run-on-failure (O-14); development diagnostic-only (O-15) not violated.

---

## 7. Handoff (return to WORKFLOW COORDINATOR)

- **Gate served:** Step 6 delta re-clear exit — BF1 re-review of v1.4 remediation.
- **Inputs/SHAs reviewed:** spec `architect/m4-spec-v1.4` @ `9dff1e5` (delta from `8740c46`); M0_DECISION_SHEET `docs/rulings/M0_DECISION_SHEET.md` line 21; provenance Entry 70. Prior v1.4 BLOCK review @ `c95f9db`.
- **Verdict:** **CLEAR**
- **BF1 remediation verification:** BF1.a (Spearman ρ ≥ 0.8, `[BAR-Entry 11]`, value matches sheet) PASS; BF1.b (standardized slope ≥ 0.2, `[BAR-Entry 11]`, value matches sheet) PASS; BF1.c (≥3-doses tag reconciled to `[BAR-Entry 11]` primary, `[OP-Entry 11.7]` retained supplemental) PASS. M0_DECISION_SHEET quotation included and matches sheet exactly.
- **Scope-violation check:** CLEAN. Delta `8740c46..9dff1e5` touches only the L8 §3.2 table (two bars + tag reconciliation + quotation + note) and changelog. No other threshold, locked bar, kill condition, scoring predicate, law text, or v1.4 amendment changed. P1 preserved.
- **Changelog:** v1.4.1 entry present and accurate. PASS.
- **Preserved evidence:** all five v1.4 amendments, law-diff, provenance, other locked bars, INSTRUMENT FAILURE, fences, standing constraints remain valid (see §4).
- **Re-review committed:** `reviews/critic_m4_v1.4_bf1_rereview.md` on branch `critic/r2-m4-v1.3-law-fidelity`.
- **Next authorized role:** WORKFLOW COORDINATOR. On CLEAR, **Step 6 exits** and the COORDINATOR assembles the Step 7 M4 gate package for Rebecca's ruling (spec approval + L7 graveyard-gate sign-off + L10 threshold + borderline ruling + timebox). M4 spec v1.4.1 is now delta re-cleared by the G0-3 reviewer with law-diff table (Step 6 exit criterion met).
- **Explicitly prohibited for next roles:** No modifying locked bars/threshold values/kill conditions/scoring predicates; no scoring seeds; no rerun of seeds 201–203/301–303; no L15/L16/L17 before M5; no modification of STATE.md or provenance_log.md; no renaming/reinterpreting negative results; no merge to main without Rebecca's explicit authorization.
- **Confirmation:** No scoring, no rerun, no hold-out seed exposure, and no unauthorized merge occurred during this re-review.
