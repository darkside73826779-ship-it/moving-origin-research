# CRITIC Delta Re-Clear Review — M4 Spec v1.4 (Step 6 Exit)

**Gate served:** Step 6 exit criterion — delta re-clear of spec v1.4 by the G0-3 reviewer, with law-diff table
**Reviewer:** CRITIC (re-initialized, fresh-context reviewer — same session as R2 review and re-review)
**Date:** 2026-08-18 · **Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Review branch:** `critic/r2-m4-v1.3-law-fidelity`
**Spec under review:** `architect/m4-spec-v1.4` @ `8740c46` (delta from R2-cleared baseline `94dcc43`, v1.3.1)
**Constitution source:** `docs/ARCHITECTURAL_CONSTITUTION.md` (v1, SHA-256 `509f11c3…`)
**Pre-registration source:** `docs/rulings/M0_DECISION_SHEET.md` (published Entry 70, G0-4)
**Provenance source:** `docs/rulings/provenance_log.md` (reviewed through Entry 72)
**Role boundary:** Read-only review. No modification of spec, constitution, STATE.md, provenance log, or any artifact. No scoring, no seed execution, no hold-out exposure, no merge.

---

## Verdict

### **BLOCK**

One blocking finding: **BF1 — L8 locked-bar omission (spec-completeness / locked-bar preservation defect).** The v1.4 spec's L8 §3.2 locked-bars table omits two locked L8 bars — **Spearman ρ ≥ 0.8** and **standardized slope ≥ 0.2** — that Rebecca pre-registered in the M0_DECISION_SHEET (line 21) and that Entry 70 confirms as locked bars sourced `[BAR-Entry 11]`. The handoff's own checklist item 5 lists "L8 ≥3 doses/ρ ≥ 0.8/slope ≥ 0.2" as locked bars to confirm intact. A spec that omits locked bars cannot be cleared as preserving all locked bars — the JUDGE cannot apply bars absent from the spec.

The five authorized amendments (1–5) are all correctly implemented, in-scope, P3-tagged, and P6-verified. The law-diff (P2) is unchanged PASS. The delta scope is clean (only the five amendments + changelog + return handoff; no bar/kill/predicate/law-text changed). The blocker is a current spec-completeness defect exposed by the publication of the M0_DECISION_SHEET (Entry 70) and explicitly placed in scope by the handoff. It is NOT a delta-scope violation and NOT candidate/instrument/construction failure. Returns to the ARCHITECT to add the two missing locked L8 bars.

---

## Blocking findings

### BF1 — L8 locked bars ρ ≥ 0.8 and slope ≥ 0.2 omitted from the spec (P3/P6 spec-completeness defect)

**Primary source (verified directly):** `docs/rulings/M0_DECISION_SHEET.md` line 21, L8 row:

> "**L8** | ≥3 noise doses; Spearman ρ ≥ 0.8 monotonic; standardized slope ≥ 0.2 (ARCHITECT's candidate accepted); specificity control mandatory (self-irrelevant dose must NOT move regulation error). Seeds: 5."

**Provenance confirmation:** Entry 70 (G0-4) states: "L8 bars confirmed: From the published sheet — ≥3 noise doses [BAR-Entry 11]; Spearman ρ ≥ 0.8 monotonic [BAR-Entry 11]; standardized slope ≥ 0.2 [BAR-Entry 11]; specificity control mandatory [BAR-Entry 11]; seeds: 5 [BAR-Entry 11.3]."

**Spec defect:** The v1.4 spec's L8 §3.2 locked-bars table contains (grep-confirmed) zero mentions of ρ, Spearman, slope, 0.8, or 0.2. It lists only:
- Minimum dose levels: ≥ 3 `[OP-Entry 11.7]`
- Monotonic test: all-seeds-direction + bootstrap-CI fallback `[BAR-Entry 11.3]`
- Seeds: 5 `[BAR-Entry 11.3]`
- Specificity ("only then"): `[LAW-L8]`

The "all-seeds-direction + bootstrap-CI" entry is the **inferential policy** for L8 (per M0_DECISION_SHEET line 29: "effect direction consistent in all seeds AND pooled bootstrap 95% CI excluding zero"), sourced `[BAR-Entry 11.3]`. The **effect-size locked bars** — Spearman ρ ≥ 0.8 and standardized slope ≥ 0.2 — are absent. The spec lists the inferential policy but omits the effect-size bars that the inferential policy is meant to test. The JUDGE at scoring time cannot apply bars that are not in the spec.

**Classification:** spec-completeness / locked-bar preservation defect (P3 source-tag + P6 provenance fidelity). Not candidate failure, not instrument failure, not construction bug, not an unauthorized delta edit. No locked bar was moved, raised, lowered, renamed, or reinterpreted — two are simply absent. Pre-existing since v1.3 (not introduced by the v1.4 amendments); newly exposed by the publication of the M0_DECISION_SHEET (Entry 70) and explicitly placed in scope by the handoff's item 5.

**Remediation (for ARCHITECT):** Add Spearman ρ ≥ 0.8 and standardized slope ≥ 0.2 to the L8 §3.2 locked-bars table, sourced `[BAR-Entry 11]` (citing Entry 70 / M0_DECISION_SHEET line 21). Do not change any existing threshold value, bar, kill condition, or scoring predicate beyond adding the two missing locked bars and their source tags. Reconcile the ≥3-dose source tag (spec: `[OP-Entry 11.7]`; sheet/Entry 70: `[BAR-Entry 11]`) — `[OP-Entry 11.7]` may remain supplemental if explained, but the canonical sheet attribution is `[BAR-Entry 11]`.

---

## 1. Law-diff (P2) — PASS (unchanged from R2)

The v1.4 delta did not modify any verbatim law quote. The five amendments touched §0, §2.5, §3.3.1, §7.3, §7.4, §8, §9.1, §12, §13 — none of the verbatim law-quote sections (§2.1, §3.1, §4.1, §5.1, §6.1). Law-diff carried forward from R2 review (all match constitution v1 byte-for-byte, line citations 24/26/30/40/52 correct).

| Law | Spec § | Const. line | Verbatim match | Verdict |
|---|---|---|---|---|
| L7 | §2.1 | 24 | Exact | PASS |
| L8 | §3.1 | 26 | Exact | PASS |
| L10 | §4.1 | 30 | Exact | PASS |
| L14 | §5.1 | 40 | Substantive exact (trailing whitespace only — NF1, non-blocking) | PASS |
| L18 | §6.1 | 52 | Exact | PASS |

No law text reconstructed (P1 preserved).

---

## 2. Amendment-by-amendment verification (1–5) — ALL PASS

### Amendment 1 — FWFP closure deliverable (§7.3) — PASS
- Named deliverable: "M4 Pre-Scoring FWFP Closure Audit." ✓
- Standing rule source: Entry 43 `[BAR-Entry 43]` — verified against provenance log Entry 43 "Systemic fix (standing): every scoring spec's closure audit must compute FWFP of each arm's full check battery and correct any control whose FWFP exceeds 5% BEFORE scoring." ✓ (P6 verified)
- Owner: TASK BUILDER (computation under O-15 diagnostic-only); ARCHITECT specifies, TASK BUILDER produces. ✓ Role-boundary preserved — the ARCHITECT did NOT perform the FWFP computation.
- Acceptance criteria: 6 items; each control arm's full check-battery FWFP ≤ 5%; corrected-alpha target "≤ 5% [BAR-Entry 43]." ✓
- Corrected-alpha target specified, not pre-computed: "The specific corrected alpha for each arm is determined by the TASK BUILDER's computation, not pre-specified by the ARCHITECT — the ARCHITECT specifies the target (≤ 5%), not the method." ✓ (role-boundary check item 6 — PASS)
- Design-validation arithmetic (permitted by handoff): "~53% familywise" = 1−(1−0.05/3)^45 ≈ 53% ✓; "≈ 1 − 0.95⁹ ≈ 37%" ✓. Both verified correct. These are illustrative motivation figures within a `[BAR-Entry 43]`-tagged context paragraph, not operational thresholds — acceptable per handoff authorization.

### Amendment 2 — Borderline pre-registration (§7.4) — PASS
- Three draft options: B1 (M3 precedent — label retained), B2 (Strict KILL), B3 (Conditional — Rebecca gate). ✓
- All tagged `[PROPOSED — requires Rebecca ruling]`. ✓
- No option self-selected (handoff item 7 — PASS): the spec presents three options without selecting one; §9.1 Step 4 and §12 route the ruling to Rebecca. ✓
- Pre-registration requirement tagged `[LAW-L19]`: "Whichever option Rebecca rules, the ruling is pre-registered in the spec before any data exists. The JUDGE at scoring time applies the pre-registered rule, not an ad-hoc judgment." ✓

### Amendment 3 — L7 fallback clarification (§2.5) — PASS
- "Threshold bars (AUROC, ECE, margin): Evaluated per-seed. Any-seed-fail → KILL. The all-seeds-direction + bootstrap-CI fallback [BAR-Entry 11.3] does NOT apply to threshold bars — it applies only to direction tests (e.g., L8 dose-response monotonicity). A threshold bar failure on any single seed is an immediate KILL with no fallback." ✓
- Resolves the §2.5 "on any seed → KILL" tension: threshold bars = per-seed any-seed-fail KILL (no fallback); direction tests (L8 monotonicity) = all-seeds-direction + bootstrap-CI fallback. No ambiguity left for the JUDGE. ✓

### Amendment 4 — L8 homeostatic-variable named prerequisite (§3.3.1) — PASS
- Named prerequisite with dedicated reviewer pass. ✓
- Four criteria, all tagged: Regulable `[LAW-L8]`, Target defined `[PROPOSED — requires Rebecca sign-off]`, Calibratable noise dose `[OP-Entry 11.7]`, Constructible specificity control `[LAW-L8]`. ✓
- Reviewer pass: dedicated CRITIC review before implementation; if any criterion unmet, BLOCKED and returned to ARCHITECT. ✓
- Placement: after spec approval (Step 7), before TASK BUILDER (Step 8); sub-step of build sequence, not a scoring gate. ✓
- Elevated from §12 line item to named prerequisite (§12 row updated). ✓

### Amendment 5 — §8 Option A amendment — PASS
- L3 row replaced: "Prerequisite for scoring | M4 scoring is gated on prospective L3 calibration resolution on fresh seeds, per governance paper §6.3(3). [BAR-Entry 72]" ✓
- Sequencing note: gate sequence (1) L3 resolution; (2) M4 scoring authorization via courier; (3) M4 scoring execution. Tagged `[BAR-Entry 72]`. ✓
- Matches the ruled Option A text (handoff item 8 — PASS): Entry 72 "RULING: Rebecca chose OPTION A. M4 spec §8 is to be amended: M4 build (implementation, diagnostic runs under O-15) proceeds in parallel; M4 scoring is gated on prospective L3 calibration resolution on fresh seeds per governance paper §6.3(3)." The spec's §8 amendment matches. ✓ (P6 verified)

---

## 3. P3 source-tag audit (new/changed thresholds) — PASS (BF1 aside)

All new/changed thresholds in the v1.4 delta carry P3 source tags:
- §3.3.1 criteria: `[LAW-L8]`, `[PROPOSED]`, `[OP-Entry 11.7]`, `[LAW-L8]`. ✓
- §7.3 FWFP: "FWFP ≤ 5% `[BAR-Entry 43]`"; corrected-alpha target "≤ 5% `[BAR-Entry 43]`." ✓
- §7.4 borderline: B1/B2/B3 all `[PROPOSED — requires Rebecca ruling]`; pre-registration requirement `[LAW-L19]`. ✓
- §8 L3 row + sequencing note: `[BAR-Entry 72]`. ✓
- §2.5 fallback clarification: `[BAR-Entry 11.3]`. ✓
- §12 borderline row: `[PROPOSED — requires Rebecca ruling]`; L8 homeostatic row: `[PROPOSED — resolved by §3.3.1]`. ✓

Design-validation figures (~53%, ~37%) are within a `[BAR-Entry 43]`-tagged context paragraph and authorized by the handoff; not untagged operational thresholds. Acceptable.

**Non-blocking source-tag note (NF1):** The spec tags L8 "≥ 3 dose levels" as `[OP-Entry 11.7]`, while the M0_DECISION_SHEET and Entry 70 attribute the L8 bars (including ≥3 doses) to `[BAR-Entry 11]`. The ≥3-doses value appears in both contexts (§9 operationalization adopted at 11.7 AND a Rebecca-locked bar at Entry 11). The canonical sheet framing is `[BAR-Entry 11]`; the spec's `[OP-Entry 11.7]` tag is supplemental but should be reconciled with the sheet. Non-blocking; folds into BF1 remediation.

---

## 4. P6 provenance verification (new citations) — PASS

| Citation | Spec claim | Log/sheet verification | Verdict |
|---|---|---|---|
| Entry 43 | FWFP closure standing rule: "every scoring spec's closure audit must compute FWFP of each arm's full check battery and correct any control whose FWFP exceeds 5% BEFORE scoring" | Entry 43 "Systemic fix (standing): every scoring spec's closure audit must compute FWFP of each arm's full check battery and correct any control whose FWFP exceeds 5% BEFORE scoring." | PASS |
| Entry 72 | Option A ruling: M4 scoring gated on L3 resolution; build parallel | Entry 72 "RULING: Rebecca chose OPTION A. M4 spec §8 is to be amended: M4 build proceeds in parallel; M4 scoring is gated on prospective L3 calibration resolution on fresh seeds per governance paper §6.3(3)." | PASS |
| Entry 70 / M0_DECISION_SHEET | L8 locked bars: ≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity, seeds 5 | M0_DECISION_SHEET.md line 21 (L8 row) states exactly these bars; Entry 70 confirms `[BAR-Entry 11]`. | PASS (and the basis for BF1) |

All prior R2 provenance citations (Entries 5/8/11.x/14/27/52) remain verified (carried from R2 review).

---

## 5. Delta scope check — CLEAN (no delta-scope violation)

Diff `94dcc43..8740c46` (3 files, +200/−24):

| File | Change | Scope |
|---|---|---|
| `specs/m4_specification.md` | Five amendments (§0, §2.5, §3.3.1, §7.3, §7.4, §8, §9.1, §12, §13) | Authorized (amendments 1–5) |
| `specs/m4_specification_changelog.md` | v1.4 changelog entry | Authorized (changelog) |
| `handoffs/ARCHITECT_M4_SPEC_V1.4_HANDOFF.md` | New return handoff | Authorized (return handoff) |

**Confirmed:** changes are confined to the five authorized amendments + changelog + return handoff. No change outside that scope. No locked bar, kill condition, or scoring predicate was changed by the delta (the L8 §3.2 table was not modified by v1.4 — BF1 is an omission, not a delta edit). P1 preserved (no law-text modification/reconstruction). The five-amendment delta itself is clean; BF1 is a current spec-completeness defect, not a delta-scope violation.

---

## 6. Compliance — PASS (BF1 aside)

| # | Check | Finding | Verdict |
|---|---|---|---|
| 9 | §5 P1–P6 maintained; P4 header updated for v1.4 | Header: "M4 Specification v1.4"; Date 2026-08-18; Regime B; Base SHA `94dcc43` (v1.3.1, R2-CLEARED); provenance reviewed through Entry 72. P1 (no reconstruction), P2 (verbatim quotes), P4 (date+regime) maintained. P3/P6 — see BF1 and §3. | PASS (P3/P6 defect = BF1) |
| 10 | L15–L17 fence, O-14/O-15, INSTRUMENT FAILURE, hold-out seed rule | §10 L15–L17 fence; §11 O-14/O-15/D1–D5/L9/L18/hold-out binding; INSTRUMENT FAILURE retained (§1.2); §8 L3 scoring gated on fresh seeds (O-14 preserved — no rerun). | PASS |

---

## 7. Non-blocking findings

| ID | Finding | Class | Recommendation |
|---|---|---|---|
| NF1 | L8 "≥ 3 dose levels" tagged `[OP-Entry 11.7]` in spec vs `[BAR-Entry 11]` in M0_DECISION_SHEET/Entry 70 | P3 source-tag reconciliation | Reconcile with sheet attribution during BF1 remediation |
| NF2 | L14 verbatim quote trailing-whitespace-only difference (carried from R2) | P2 whitespace | Align for strict byte-match in a future revision |
| NF3 | Entry 11.7 log text doesn't enumerate the nine §9 operationalizations (carried from R2) | P6 granularity | Cite M3 implementation entries for V4.4 specifics |
| NF4 | Graveyard-gate tag `[BAR-Entry 11.8]` imprecise (gate decision, not bar) (carried from R2) | P3 source-class precision | Annotate as gate-decision |

None block independently of BF1.

---

## 8. Preserved evidence

- Five authorized amendments (1–5) all correctly implemented, in-scope, P3-tagged, P6-verified.
- Law-diff (P2): L7/L8/L10/L14/L18 verbatim match constitution v1; line citations correct.
- Provenance (P6): Entries 5/8/11.x/14/27/43/52/70/72 verified against log/sheet text.
- Locked bars (other than the BF1 omissions): L7 0.75/0.10/margin, L10 50%/10% + 0.70 floor, L14 d≥0.5 / corr≥0.3 preserved, values unchanged.
- INSTRUMENT FAILURE label and M3 verdicts preserved.
- L15–L17 fence respected; P4 v1.4 header present; O-14/O-15/D1–D5/L9/L18/hold-out rules binding.
- FWFP deliverable specified, not performed (role-boundary preserved).
- Borderline options presented without self-selection.

---

## 9. Pre-push self-scan attestation

A pre-push scan was performed on this review file and commit contents. No credentials, API keys, tokens, passwords, secrets, PII, machine identifiers, or private absolute paths found. Only repository-relative paths and already-public SHAs referenced. Findings: none. Classification: acceptable.

---

## 10. Prohibited-action confirmations

- No modification of the spec, constitution, STATE.md, provenance log, or any artifact under review. Only this review file was created and committed.
- No merge to main (branch `critic/r2-m4-v1.3-law-fidelity` only; Rebecca sole merge authority).
- No scoring, no seed execution, no hold-out seed exposure.
- No L15/L16/L17 work before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- No re-run-on-failure (O-14); development diagnostic-only (O-15) not violated.

---

## 11. Handoff (return to WORKFLOW COORDINATOR)

- **Gate served:** Step 6 exit — delta re-clear of M4 spec v1.4.
- **Inputs/SHAs reviewed:** spec `architect/m4-spec-v1.4` @ `8740c46` (delta from `94dcc43`); constitution v1; M0_DECISION_SHEET `docs/rulings/M0_DECISION_SHEET.md`; provenance log (through Entry 72). Prior R2/R2-re-review reviews on `critic/r2-m4-v1.3-law-fidelity`.
- **Verdict:** **BLOCK**
- **Blocking finding:** BF1 — L8 §3.2 locked-bars table omits Spearman ρ ≥ 0.8 and standardized slope ≥ 0.2, both confirmed locked bars per M0_DECISION_SHEET line 21 and Entry 70 `[BAR-Entry 11]`. Spec-completeness / locked-bar preservation defect. Not a delta-scope violation; the five-amendment delta is clean.
- **Amendment verification (1–5):** all PASS (FWFP specified-not-performed; borderline options no self-selection; L7 fallback resolves §2.5 tension; L8 prerequisite with reviewer pass; §8 matches Option A Entry 72).
- **Law-diff (P2):** PASS (unchanged).
- **P6 provenance:** Entries 43, 72 verified PASS.
- **Delta scope check:** CLEAN — only the five amendments + changelog + return handoff; no bar/kill/predicate/law-text changed.
- **Non-blocking findings:** NF1 (≥3-dose source-tag reconciliation), NF2 (L14 whitespace), NF3 (Entry 11.7 granularity), NF4 (Entry 11.8 source-class).
- **Preserved evidence:** all amendments, law-diff, provenance, locked bars (except BF1 omissions), INSTRUMENT FAILURE, fences, standing constraints — preserved (see §8).
- **Review committed:** `reviews/critic_m4_v1.4_delta_review.md` on branch `critic/r2-m4-v1.3-law-fidelity`.
- **Exact next authorized role:** ARCHITECT (originating role) — add Spearman ρ ≥ 0.8 and standardized slope ≥ 0.2 to the L8 §3.2 locked-bars table, sourced `[BAR-Entry 11]` (Entry 70 / M0_DECISION_SHEET line 21), and reconcile the ≥3-dose source tag (NF1). No change to any threshold value, bar, kill condition, or scoring predicate beyond adding the two missing locked bars and their source tags. Then resubmit for delta re-clear.
- **Explicitly prohibited for ARCHITECT during remediation:** No modifying existing threshold values/bars/kill conditions/scoring predicates (add the two missing locked bars + source tags only); no reconstructing law text; no scoring seeds; no rerun of seeds 201–203/301–303; no L15/L16/L17 before M5; no modification of STATE.md or provenance_log.md; no renaming/reinterpreting negative results; no merge to main.
- **Coordinator note:** On a subsequent CLEAR, Step 6 exits and the coordinator assembles the Step 7 M4 gate package for Rebecca's ruling (spec approval + L7 graveyard-gate sign-off + L10 threshold + borderline ruling + timebox).
- **Confirmation:** No scoring, no rerun, no hold-out seed exposure, and no unauthorized merge occurred during this review.
