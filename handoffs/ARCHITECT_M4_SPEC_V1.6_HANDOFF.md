# ARCHITECT Handoff — M4 Spec v1.6 (Rebecca's Nine Gate Rulings)

**Gate served:** Step 7 gate rulings implementation (v1.5 → v1.6)
**Issued by:** ARCHITECT
**Date:** 2026-08-18 22:55 EDT
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)

---

## SHAs

| Item | SHA | Location |
|---|---|---|
| Base (v1.5, CRITIC-cleared) | `487843f` | `architect/m4-spec-v1.5` |
| v1.6 HEAD | (to be verified after push) | `architect/m4-spec-v1.6` |

## Nine rulings implemented

### Ruling 1 — L7 inference (§2.5)
AUROC/ECE = per-seed threshold bars (any-seed KILL, no fallback). Margin = direction test (5 paired seeds, all-seed direction + pooled paired-bootstrap 95% CI excluding zero). v1.4 Amendment 3 retracted. v1.5 STOP resolved. [BAR-Entry 11.3] [LAW-L7]

### Ruling 2 — L10 threshold and AUROC (§4.3)
Primary drifted AUROC over complete fixed population using pre-abstention scores. All-abstain = failure. τ dual-calibrated (drift ≥50%, clean ≤10%). Floor ≥0.70 [BAR-Entry 14] preserved — value unchanged.

### Ruling 3 — L8 zero-noise + severity matching (§3.3)
Level 0 approved. Severity matching via pre-registered standardized proximal-component effect (4 predefinitions). L8 bars [BAR-Entry 11] preserved.

### Ruling 4 — Borderline B1 confirmed (§7.5)
B1 confirmed. 0.5α–α band descriptive only — does not change verdict. [BAR-Entry 43] [LAW-L19]

### Ruling 5 — L7 peer parity conditions (§2.3)
Identical confidence calibration, evaluation data, ECE definition, binning. Paired independently trained instances. [BAR-Entry 11]

### Ruling 6 — L7 graveyard-gate (§1.3)
Signed for implementation only — not scoring. Downstream gates retained. [BAR-Entry 11.8]

### Ruling 7 — M4 timebox (§9.2)
6 sessions / 14 days, tripwire 3/7. Waiting time excluded. [Rebecca-approved]

### Ruling 8 — L10 seeds (§4.2)
5 seeds confirmed. Tag updated to [BAR-Entry 11.3]. Value unchanged.

### Ruling 9 — Tolerance calibration (§7.6)
New §7.6: pre-registered, candidate-blind, oracle/synthetic-grounded, frozen-before-scoring. ARCHITECT specifies procedure; TASK BUILDER computes under O-15; CRITIC verifies; Rebecca signs off on method/criterion. [BAR-Entry 43]

## Confirmation

No locked bar value changed (L7 0.75/0.10/margin, L8 ≥3/ρ≥0.8/slope≥0.2/specificity, L10 50%/10%/0.70 floor, L14 d≥0.5/corr≥0.3). L3 pre-scoring gate preserved. O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved. P1–P6 maintained. P5: all deviations from prior [PROPOSED] items authorized by Rebecca's nine rulings.

## Next recipient

**CRITIC** (fresh-context reviewer) for delta re-clear with law-diff table. Then **WORKFLOW COORDINATOR** for formal Step 7 gate package to Rebecca for graveyard-gate signature (implementation-only authorization).

## Explicitly prohibited

- No merging to main
- No scoring, seed execution, or hold-out seed exposure
- No rerun of seeds 201–203 / 301–303 (O-14)
- No L15/L16/L17 work before M5
- No modification of STATE.md or provenance_log.md
- No implementation, diagnostic execution, or mechanism construction
- No self-selecting tolerance numbers (ARCHITECT specifies procedure; TASK BUILDER computes)
- No renaming or reinterpreting any negative result or INSTRUMENT FAILURE label
