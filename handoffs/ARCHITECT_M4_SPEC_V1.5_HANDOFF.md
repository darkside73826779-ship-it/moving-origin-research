# ARCHITECT Handoff — M4 Spec v1.5 (Advisor Correction Cycle)

**Gate served:** Pre-gate correction cycle per outside-advisor review
**Issued by:** ARCHITECT
**Date:** 2026-08-18 21:55 EDT
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)

---

## SHAs

| Item | SHA | Location |
|---|---|---|
| Base (v1.4.1, CRITIC-cleared) | `9dff1e5` | `architect/m4-spec-v1.4` |
| v1.5 HEAD | (to be verified after push) | `architect/m4-spec-v1.5` |
| Main HEAD | `eab3fbe` | `main` |

## Six findings applied

### Finding 1: L7 peer baseline reconciliation (§2.3)
Replaced fixed OLS baseline with matched-model peer per Constitution L7 ("matched model") and M0 Decision Sheet line 20 ("same params/data/architecture, observation channel = behavioral outputs only, self-report channel excluded"). All peer spec items tagged [BAR-Entry 11]. Peer confidence method tagged [PROPOSED].

### Finding 2: FWFP milestone-wide family (§7.3)
Extended FWFP closure to also cover milestone-wide family of ALL control-triggering tests across M4. Both per-arm and milestone-wide FWFP ≤ 5% [BAR-Entry 43] are acceptance criteria. Owner: TASK BUILDER (O-15).

### Finding 3: L10 threshold definitions (§4.3)
Replaced unsupported τ=0.70 ↔ AUROC 0.70 linkage with explicit definitions: confidence, calibration method, abstained-case treatment, AUROC population. Drifted-AUROC floor ≥0.70 [BAR-Entry 14] preserved — not linked to τ. τ value determined by calibration, not pre-specified.

### Finding 4: L8 zero-noise baseline + severity-matched specificity (§3.3)
Added Level 0 (zero-noise baseline) as reference point. Added severity-matched specificity: non-self-model noise equals self-model dose magnitude at each level. L8 locked bars [BAR-Entry 11] preserved.

### Finding 5: Borderline numerical definition + B1 draft (§7.5)
Added numerical definition: borderline = p ∈ [α_corr × 0.5, α_corr]. Added B1 draft (advisor recommendation): label retained, provisional advancement possible, correction via Entry 43 four-part test. Tagged [PROPOSED — requires Rebecca ruling].

### Finding 6: L7 inference reconciliation (§2.5) — STOP/escalation
Tension between v1.4 §2.5 (any-seed KILL) and M0 line 29 (5-seed/bootstrap fallback for L7). Flagged as STOP per §5.2 — not resolvable from verbatim law text. Escalation question for Rebecca. Conservative default (any-seed KILL) applies until ruled.

## STOP/escalation trigger

**Finding 6** is flagged as a STOP per §5.2. The tension between the M0 inferential policy (line 29: 5 seeds + all-seeds-direction + bootstrap-CI fallback for L7) and the v1.4 any-seed-KILL rule for L7 threshold bars cannot be resolved from verbatim law text. The Constitution L7 text states the bars but not the inferential policy; the M0 sheet states the inferential policy but does not distinguish "threshold" vs "direction" bars. Rebecca must rule.

## Confirmation

- No locked bar value changed (L7 0.75/0.10/margin, L8 ≥3/ρ≥0.8/slope≥0.2/specificity, L10 50%/10%/0.70 floor, L14 d≥0.5/corr≥0.3)
- No kill condition or scoring predicate changed beyond what the six findings require
- L3 pre-scoring gate (Option A, Entry 72) preserved
- O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved
- P1–P6 maintained throughout
- Finding 6 flagged as STOP/escalation per §5.2

## Next recipient

**CRITIC** (fresh-context reviewer) for delta re-clear with law-diff table. Then **WORKFLOW COORDINATOR** for revised Step 7 gate package to Rebecca.

## Explicitly prohibited

- No merging to main
- No scoring, seed execution, or hold-out seed exposure
- No rerun of seeds 201–203 / 301–303 (O-14)
- No L15/L16/L17 work before M5
- No modification of STATE.md or provenance_log.md
- No amendment to governance paper §6.3
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label
- No self-selecting the borderline ruling (B1 is advisor recommendation; Rebecca rules)
