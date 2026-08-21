# M4 Specification — Changelog

**Spec:** `specs/m4_specification.md`
**Date:** 2026-08-18 · **Author:** ARCHITECT
**Base SHA:** `487843f` (v1.5, CRITIC-cleared)
**Branch:** `architect/m4-spec-v1.6`
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)

## v1.7 — Exact-matched-peer model-selection qualification ladder (2026-08-21)

- Incorporated Rebecca's Qwen3-4B FP8 primary and Qwen3-8B FP8 fallback qualification ladder.
- Replaced the superseded cross-family peer proposal with a separate byte-identical instance of the selected Qwen checkpoint, differing only by its observable-only channel.
- Added immutable model/revision/weight identities, local-only custody, exact serving-stack identity, deterministic session verification, FP8 verification, context, co-residency, and phased-swap contracts.
- Added fixed Q1–Q3 sequencing, non-adaptive escalation, Phase A transcript logging, qualification-report schemas, and closed-by-default QLoRA handling.
- Proposed a numeric Q2 informative band as `[PROPOSED]`; it remains inoperative pending Rebecca's explicit signature.
- Preserved every locked L7/L8/L10/L14/L18 bar, O-14/O-15, negative labels, scoring-seed fences, and Rebecca-only gate/merge authority.


---

## v1.6.2 — CRITIC residual BLOCK remediation: line 8 provenance + §12 L8 entry (2026-08-18)

CRITIC residual re-clear found two residuals of the same class as v1.6.1. Both are ultra-narrow mechanical corrections.

### BF-A: Line 8 provenance clause

Line 8 "Provenance log reviewed through Entry 72" → "through Entry 76" — now consistent with §0 line 17.

### BF-B: §12 L8 standardized specificity entry removed

Removed "L8 standardized specificity" from "Items still requiring Rebecca sign-off" list — Ruling 3 (Entry 76) approved the approach; specific values are CRITIC-reviewed under §3.3.1, not separately by Rebecca. Entry contradicted §3.3 lines 203–206 and §12 line 558 (both RESOLVED). Tolerance calibration entry (Ruling 9) left unchanged — correct per Entry 76.

### Confirmation

No spec substance, locked bar, kill condition, scoring predicate, or ruling implementation changed. Two lines changed (line 8 provenance clause, §12 entry removed). Mechanical correction only.

---

## v1.6.1 — CRITIC BLOCK remediation: provenance + tag-state correction (2026-08-18)

CRITIC fresh-context delta re-clear of v1.6 returned BLOCK with three mechanical provenance/tag-state findings. Spec substance, locked bars, kill conditions, scoring predicates, and all nine ruling implementations verified PASS — not altered.

### BF-3: §0 provenance statement updated + Entry 76 cited

Updated §0 "Provenance reviewed through Entry 72" → "through Entry 76." Added Entry 76 as source authority for the nine rulings in §0. Added [Entry 76] source tags on each ruling implementation (§1.3 R6, §2.3 R5, §2.5 R1, §3.3 R3, §4.2 R8, §4.3 R2, §7.5 R4, §7.6 R9, §9.2 R7).

### BF-1: Stale [PROPOSED] tags on L8 items updated

Updated §3.3 lines 190, 203–206 from [PROPOSED — requires Rebecca sign-off] to [Rebecca-approved (Ruling 3, Entry 76)] — consistent with Ruling 3 approval and §12 table.

### BF-2: Stale [PROPOSED] tag on §7.4 B1 updated

Updated §7.4 Option B1 tag from [PROPOSED — requires Rebecca ruling] to [Rebecca-confirmed B1 (Ruling 4, Entry 76)] — consistent with Ruling 4 confirmation and §7.5.

### Confirmation

No spec substance, locked bar, kill condition, scoring predicate, or ruling implementation changed. Only provenance statement, Entry 76 citations, and approval-status tags updated. Law-diff unchanged (byte-exact). Mechanical correction only.

---

## v1.6 — Rebecca's nine gate rulings implemented (2026-08-18)

All nine Step 7 gate items ruled by Rebecca. Implemented as spec language. No locked bar value changed. L3 pre-scoring gate preserved. O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved.

### Ruling 1: L7 inference (§2.5)

Replaced v1.5 STOP/escalation with Option C: AUROC and ECE are per-seed threshold bars (any-seed fail → KILL, no fallback); candidate–peer margin is a direction test (5 paired seeds, all-seed direction + pooled paired-bootstrap 95% CI excluding zero). v1.4 Amendment 3 hard rule retracted. [BAR-Entry 11.3] [LAW-L7]

### Ruling 2: L10 threshold and AUROC definitions (§4.3)

Primary drifted AUROC computed over complete fixed drifted population using pre-abstention scores. Answered-case AUROC reported separately (not headline). All-abstain = failure (not N/A). τ dual-calibrated (drift ≥50%, clean ≤10%) on held-out data. Drifted-AUROC floor ≥0.70 [BAR-Entry 14] preserved — value unchanged, population and anti-gaming design changed. [BAR-Entry 14] [BAR-Entry 11.6]

### Ruling 3: L8 zero-noise baseline + severity-matched specificity (§3.3)

Level 0 zero-noise baseline approved as dose-response reference. Severity matching replaced with pre-registered standardized proximal-component effect (4 predefinitions: comparison component, perturbation type/magnitude, calibration set, tolerance). L8 locked bars [BAR-Entry 11] preserved. [LAW-L19]

### Ruling 4: Borderline numerical definition + B1 handling (§7.5)

B1 confirmed (label retained, provisional advancement possible). 0.5α–α band is descriptive only — must NOT change the verdict. Margin pre-registered. [BAR-Entry 43] [LAW-L19]

### Ruling 5: L7 peer confidence method (§2.3)

Added peer-observer parity conditions: identical confidence calibration, identical evaluation data, identical ECE definition, identical binning, paired independently trained instances. [BAR-Entry 11] [LAW-L7]

### Ruling 6: L7 graveyard-gate sign-off (§1.3)

Signed for M4 implementation only — authorizes build, not scoring. All downstream gates retained (L3, FWFP, CRITIC, courier). [BAR-Entry 11.8]

### Ruling 7: M4 timebox (§9.2)

6 sessions / 14 days, tripwire 3 sessions / 7 days. External-review and L3-gate waiting time excluded from clock. [Rebecca-approved]

### Ruling 8: L10 scoring seeds (§4.2)

5 seeds confirmed by Rebecca. Tag updated from [PROPOSED] to [BAR-Entry 11.3]. Value unchanged.

### Ruling 9: Control-arm tolerance calibration (§7.6)

New §7.6: pre-registered, candidate-blind, oracle/synthetic-grounded, frozen-before-scoring procedure. ARCHITECT specifies procedure; TASK BUILDER computes numbers under O-15; CRITIC verifies; Rebecca signs off on method/criterion. Existing failure-routing rules preserved. [BAR-Entry 43] [LAW-L19]

### §12 decision list updated

All nine items marked RESOLVED with ruling number. Two items remain for method/criterion sign-off (L8 specificity predefinitions, tolerance calibration method).

### Confirmation

No locked bar value changed (L7 0.75/0.10/margin, L8 ≥3/ρ≥0.8/slope≥0.2/specificity, L10 50%/10%/0.70 floor, L14 d≥0.5/corr≥0.3). L3 pre-scoring gate preserved. O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved. P1–P6 maintained. P5: all deviations from prior [PROPOSED] items are authorized by Rebecca's nine rulings.

---

## v1.5 — Advisor correction cycle: six findings (2026-08-18)

Outside advisor reviewed M4 gate package (spec v1.4.1 at `9dff1e5`, CRITIC-cleared) against GitHub repo. Six design-completeness findings — not law-fidelity failures. All locked bars, O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence, and L3 pre-scoring gate preserved.

### Finding 1: L7 peer baseline reconciliation (§2.3)

Replaced fixed OLS baseline with matched-model peer per Constitution L7 ("matched model") and M0 Decision Sheet line 20 ("same params/data/architecture, observation channel = behavioral outputs only, self-report channel excluded"). OLS baseline (v1.1–v1.4) was an ARCHITECT design choice that did not match the Constitution or M0 sheet. Corrected. All peer spec items tagged [BAR-Entry 11]. Peer confidence method tagged [PROPOSED].

### Finding 2: FWFP milestone-wide family (§7.3)

Extended FWFP closure deliverable scope from per-arm only to also cover milestone-wide family of ALL control-triggering tests across M4. Both per-arm and milestone-wide FWFP ≤ 5% [BAR-Entry 43] are acceptance criteria. Owner remains TASK BUILDER (O-15).

### Finding 3: L10 threshold definitions (§4.3)

Replaced unsupported τ=0.70 ↔ AUROC 0.70 linkage with explicit definitions: (a) confidence = scalar [0,1] from self-model; (b) threshold calibrated on held-out set to achieve ≥50% abstention under drift; (c) abstained cases excluded from AUROC; (d) AUROC population = non-abstained drifted cases. Drifted-AUROC floor ≥0.70 [BAR-Entry 14] preserved — not linked to τ. τ value not pre-specified; determined by calibration.

### Finding 4: L8 zero-noise baseline + severity-matched specificity (§3.3)

Added Level 0 (zero-noise baseline) as reference point for dose-response. Added severity-matched specificity intervention: noise injected into non-self-model component must equal perturbation magnitude at each dose level. L8 locked bars (≥3 doses, ρ≥0.8, slope≥0.2, specificity, 5 seeds) [BAR-Entry 11] preserved.

### Finding 5: Borderline numerical definition + B1 draft (§7.5)

Added numerical definition: borderline = p ∈ [α_corr × 0.5, α_corr]. Added B1 draft implementation (advisor recommendation): label retained, full context reported, provisional advancement possible, correction via Entry 43 four-part test. Tagged [PROPOSED — requires Rebecca ruling]. Pre-registration per [LAW-L19].

### Finding 6: L7 inference reconciliation (§2.5) — STOP/escalation

Identified tension between v1.4 §2.5 (any-seed KILL, no fallback for threshold bars) and M0 Decision Sheet line 29 (5 seeds + all-seeds-direction + bootstrap-CI fallback for L7). Flagged as STOP per §5.2 — not resolvable from verbatim law text. Escalation question for Rebecca: does M0 fallback apply to all L7 bars or only direction tests? Conservative default (any-seed KILL) applies until Rebecca rules.

### §12 decision list updated

Added: L10 confidence/threshold definitions, borderline numerical definition, L7 inference policy (escalation), L7 peer confidence method, L8 zero-noise baseline, L8 severity-matched specificity.

### Confirmation

No locked bar value changed (L7 0.75/0.10/margin, L8 ≥3/ρ≥0.8/slope≥0.2/specificity, L10 50%/10%/0.70 floor, L14 d≥0.5/corr≥0.3). No kill condition or scoring predicate changed beyond what the six findings require. L3 pre-scoring gate preserved. O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved. P1–P6 maintained. Finding 6 flagged as STOP/escalation per §5.2.

---

## v1.4.1 — BF1 remediation: missing L8 locked bars added + ≥3-doses tag reconciled (2026-08-18)

CRITIC v1.4 delta re-clear returned BLOCK with one finding (BF1): L8 §3.2 locked-bars table omitted two effect-size bars that Rebecca pre-registered in the M0_DECISION_SHEET (line 21, published via G0-4, Entry 70).

### Two missing locked L8 bars added

- **Spearman ρ ≥ 0.8 monotonic** — sourced [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70)
- **Standardized slope ≥ 0.2** — sourced [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70)

M0_DECISION_SHEET quotation included in §3.2 for fidelity.

### ≥3-doses tag reconciled

Previously tagged [OP-Entry 11.7] (supplemental). Reconciled to [BAR-Entry 11] as primary tag per M0_DECISION_SHEET canonical attribution. [OP-Entry 11.7] retained as §9 operationalization record only.

### Confirmation

No existing threshold value, locked bar, kill condition, or scoring predicate changed. No law text modified. No reconstruction. Only two missing bars added and one tag reconciled.

---

## v1.4 — Step 6 amendments: FWFP closure, borderline pre-registration, L7 fallback, L8 prerequisite, §8 Option A (2026-08-18)

Five amendments per WORKFLOW COORDINATOR Step 6 handoff. No locked bar, kill condition, or scoring predicate changed. No law text modified. No reconstruction.

### Amendment 1: FWFP closure deliverable (§7.3)

Added §7.3 — M4 Pre-Scoring FWFP Closure Audit. Named deliverable with owner (TASK BUILDER), acceptance criteria (6 items), corrected-alpha target (≤ 5% per arm [BAR-Entry 43]), and build-sequence placement (Step 8, pre-scoring). The ARCHITECT specifies the deliverable; computation and correction are TASK BUILDER scope under O-15. Context: current alpha_seed = 0.05/3 across 45 checks does not demonstrate closure (~53% naive familywise; ~37% per-family odds). Entry 43 standing rule: FWFP of each arm's full check battery computed and corrected before scoring.

### Amendment 2: Borderline pre-registration (§7.4)

Added §7.4 — draft options for Rebecca's ruling on how a within-FWFP borderline control firing is labeled and handled at the delivery gate. Three options: B1 (M3 precedent — label retained, provisional advancement possible), B2 (strict KILL), B3 (conditional — Rebecca rules at gate). All tagged [PROPOSED — requires Rebecca ruling]. Pre-registration requirement per [LAW-L19]. No option implemented.

### Amendment 3: L7 fallback clarification (§2.5)

Clarified that the all-seeds-direction + bootstrap-CI fallback [BAR-Entry 11.3] applies only to direction tests (e.g., L8 dose-response monotonicity), NOT to L7 threshold bars (AUROC, ECE, margin). Threshold bars are evaluated per-seed: any-seed-fail → immediate KILL with no fallback. Resolves the tension between §2.2 inferential policy and §2.5 kill conditions.

### Amendment 4: L8 homeostatic-variable named prerequisite (§3.3.1)

Elevated L8 homeostatic-variable definition from a §12 decision item to a named prerequisite (§3.3.1) with its own dedicated reviewer pass. Four criteria: regulable [LAW-L8], target defined [PROPOSED], calibratable noise dose [OP-Entry 11.7], constructible specificity control [LAW-L8]. Reviewer pass by CRITIC before implementation. Removed from §12 decision list.

### Amendment 5: §8 Option A amendment (Step 4 ruling implementation)

Replaced L3 row in §8 per Step 4 ruling [BAR-Entry 72]: L3 disposition changed from "Parallel, not blocking" to "Prerequisite for scoring" — build proceeds in parallel, scoring gated on prospective L3 calibration resolution on fresh seeds per governance paper §6.3(3). Added sequencing note with gate sequence: (1) L3 resolution; (2) scoring authorization via courier; (3) scoring execution. Governance paper stands unamended.

### §9.1 sequencing plan updated

Updated role assignments to reflect new steps: CRITIC delta re-clear (Step 2), WORKFLOW COORDINATOR package assembly (Step 3), L8 prerequisite review (Step 6), FWFP closure audit (Step 7), L3 scoring gate (Step 10).

### §12 decision list updated

Removed L8 homeostatic variable (elevated to §3.3.1). Added borderline control firing handling [PROPOSED — requires Rebecca ruling].

### Confirmation

No threshold value, bar, kill condition, or scoring predicate changed. No law text modified. No reconstruction. All new thresholds tagged [PROPOSED] or appropriate source class. Provenance citations verified (P6).

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
