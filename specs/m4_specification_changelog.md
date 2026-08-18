# M4 Specification — Changelog

**Spec:** `specs/m4_specification.md`
**Date:** 2026-08-18 · **Author:** ARCHITECT
**Base SHA:** `e26d05f` (GitHub main)
**Branch:** `architect/m4-spec-v1.3`
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)

---

## v1.3.1 — BF1 remediation + NF1–NF4 annotations (2026-08-18)

CRITIC R2 law-fidelity review returned BLOCK with one P3 violation (BF1: control-arm tolerance thresholds and other numeric values lacking source tags). All F1 corrections verified correct. All law quotes verbatim. All provenance citations verified.

### BF1.a: L8 §3.3 "≥ 1" homeostatic variable lower bound tagged

Added [LAW-L8] tag to "≥ 1" in §3.3, sourced from L8 verbatim: "At least one homeostatic variable…" [LAW-L8, line 26].

### BF1.b: L8 §3.4 control-arm failure routings tagged

Added Source column to L8 control table (§3.4). Five routings tagged [PROPOSED — requires Rebecca sign-off]. Frozen arm KILL routing tagged [LAW-L8] ("stakes decorative" is law text).

### BF1.c: §9.2 timebox tripwires tagged

Added [PROPOSED — requires Rebecca approval] to tripwire values "2" (sessions) and "4" (days), matching adjacent tagged values.

### NF1: L14 trailing whitespace

CRITIC verified L14 quote is byte-identical (trailing space is a constitution whitespace artifact, not a spec error). No change needed.

### NF2: V4.4 alpha_seed citation

Added note citing M3 implementation entries in provenance log for V4.4 alpha_seed specifics.

### NF3: Entry 11.8 graveyard-gate source class

Annotated [BAR-Entry 11.8] as (gate-decision) source class in §2.2.

### NF4: §7.1 derived quantities annotated

Taged "1 pool" as [PROPOSED — derived from single-pool design] and "45" as [PROPOSED — derived: 3 laws × 3 families × 5 seeds].

### Confirmation

No threshold value, bar, kill condition, or scoring predicate changed. Only source-class tags and annotations added.

---

## v1.3 — F1 reconstruction-infidelity correction + §5 compliance (2026-08-18)

First spec produced under §5 Versioned-Law Compliance Protocol. All law sections now open with verbatim quotes from `docs/ARCHITECTURAL_CONSTITUTION.md` (P2). All thresholds tagged with source class (P3). Regime and date in header (P4). All provenance citations verified against actual entry text (P6).

### F1.1: L8 respecified from verbatim text

**Before (v1.2):** L8 operationalized as prediction-horizon dose-response (h=1/h=3/h=5). This was a reconstruction error — the verbatim law text specifies a different test.

**After (v1.3):** L8 operationalized from verbatim text [LAW-L8, line 26]: homeostatic variable + calibrated noise injection into self-model at ≥3 dose levels [OP-Entry 11.7] + dose-dependent regulation error rise + "only then" specificity leg (non-self-model noise must NOT raise regulation error). h=1/3/5 design retained as supplementary probe only.

### F1.2: L14 rewritten as three couplings

**Before (v1.2):** L14 operationalized as correlation between self-reported state and ground-truth.

**After (v1.3):** L14 operationalized from verbatim text [LAW-L14, line 40] as three couplings: (1) homeostatic variables readable by self-model, (2) affected by memory quality, (3) predictive targets for thick present (L3). d ≥ 0.5 [BAR-Entry 11.4] and corr ≥ 0.3 [BAR-Entry 14] retained.

### F1.3: L10 reporting rule added

**Before (v1.2):** L10 reporting rule from verbatim text not included.

**After (v1.3):** Added [LAW-L10, line 30]: "drifted-regime AUROC is the reported number; the clean number is a ceiling, not a claim." Scoring report must report drifted AUROC as primary, clean as ceiling.

### F1.4: L7 portrait clause added

**Before (v1.2):** Portrait clause not explicitly stated.

**After (v1.3):** Added from verbatim text [LAW-L7, line 24]: "No margin over the peer = portrait, not mirror — reported as such." Routed as KILL, not INSTRUMENT_FAILURE.

### F1.5: §12 provenance corrected

**Before (v1.2):** L7 bars attributed to "Entry 5 (JUDGE measurability)." Entry 5 was an assessment, not bar-setting.

**After (v1.3):** L7 bars (AUROC ≥ 0.75, ECE ≤ 0.10, margin > 0 at p < .05) correctly attributed to [LAW-L7] (constitution text, line 24). Entry 5 [verified: provenance_log.md line 87] classified L7 as "fully numeric (judgeable now)" — assessment only. Entry 8 [verified: provenance_log.md line 134] identified corrections — not bar-setting. Bars locked by Rebecca in Entry 11 [verified: provenance_log.md line 172].

### F1.6: W4 stale changelog line fixed

W4 (L10 confidence threshold pre-registered at M4) was a watch item from Entry 14. In v1.2 it appeared in the changelog as a pending item. In v1.3, W4 is resolved: τ = 0.70 is pre-registered as [PROPOSED — requires Rebecca sign-off]. The stale "pending" framing is removed.

### P1–P6 compliance

- **P1 (repo-first):** All law text read from `docs/ARCHITECTURAL_CONSTITUTION.md` on main. No reconstruction.
- **P2 (verbatim quotation):** §2.1, §3.1, §4.1, §5.1, §6.1 each open with verbatim law quote, cited by file and line.
- **P3 (source-class tags):** Every threshold tagged: [LAW-Lx], [BAR-Entry n], [OP-Entry n], or [PROPOSED].
- **P4 (regime dating):** Header states date 2026-08-18, Regime B (post-Entry 27, v1 + Amendment 1, §5 binding).
- **P5 (deviation memorialization):** No deviations from law text. L8 respecification is a correction to match verbatim text, not a deviation.
- **P6 (provenance citation check):** All "Entry n said X" claims verified against actual provenance_log.md text at `e26d05f` before commit.

---

## v1.2 — CRITIC BF3 re-resolution + BF6 + NF4/NF5 (2026-08-18)

[See v1.2 changelog on architect/m4-specification branch at 5496a22]

## v1.1 — CRITIC BF1–BF5 + NF1–NF3 resolutions (2026-08-18)

[See v1.1 changelog on architect/m4-specification branch at 4a916e7]

## v1.0 — Initial specification (2026-08-18)

[See v1.0 changelog on architect/m4-specification branch at 0dc0860]
