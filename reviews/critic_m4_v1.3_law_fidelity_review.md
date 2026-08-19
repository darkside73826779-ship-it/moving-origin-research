# CRITIC R2 Law-Fidelity Review — M4 Specification v1.3

**Gate served:** R2 — designated law-fidelity review of M4 spec v1.3 (Step 3 of Principal's resolution sequence)
**Reviewer:** CRITIC (re-initialized, fresh context)
**Date:** 2026-08-18 · **Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Review branch:** `critic/r2-m4-v1.3-law-fidelity`
**Spec under review:** `architect/m4-spec-v1.3` @ `c0a3413` — `specs/m4_specification.md` (+ `specs/m4_specification_changelog.md`)
**Constitution sources:** `docs/ARCHITECTURAL_CONSTITUTION.md` (v1, SHA-256 `509f11c3...`), `docs/ARCHITECTURAL_CONSTITUTION_v2.md` (§5 + Amendment 1)
**Provenance source:** `docs/rulings/provenance_log.md`
**Base main at review time:** `956a5e7` (handoff noted `e26d05f`; main has since moved through Entries 66–67 — does not affect this review's read-only scope, which is pinned to spec branch `c0a3413`)
**Role boundary:** Read-only review. No modification of spec, constitution, STATE.md, provenance log, or any artifact. No scoring, no seed execution, no hold-out exposure, no merge.

> **Revision note (2026-08-18):** This is the operative review. An initial draft issued CLEAR; on re-examination against the handoff's mandatory P3 check ("Verify every threshold carries a P3 source tag… No untagged numbers"), untagged thresholds were reclassified from non-blocking to a blocking P3 source-tag defect. The earlier CLEAR draft is superseded; this review is the R2 artifact of record.

---

## Verdict

### **BLOCK**

One blocking finding: **BF1 — P3 source-tag defect.** The spec contains thresholds that carry no P3 source-class tag, failing the handoff's mandatory P3 check ("No untagged numbers"). The law-diff (P2), provenance citations (P6), F1 corrections, locked bars, fences, and INSTRUMENT FAILURE discipline are all preserved and verified — the defect is narrowly scoped to source-class tagging on a small set of thresholds. Returns to the ARCHITECT (originating role) to add the missing tags; the fix is low-cost and does not touch any law text, bar, or scoring predicate.

---

## Blocking findings

### BF1 — P3 source-class tags missing on several thresholds (P3 violation)

The handoff's Step 1, item 2 makes P3 a mandatory pass criterion: "Verify every threshold carries a P3 source tag: [LAW-Lx], [BAR-Entry n], [OP-Entry n], [PROPOSED]. No untagged numbers." The following thresholds are untagged:

| # | Location | Untagged threshold | Required tag | Note |
|---|---|---|---|---|
| BF1.a | §3.3 (line 133) | "Define ≥ 1 homeostatic variable" — the "≥ 1" lower bound | `[LAW-L8]` | Sourced directly from L8 law text ("At least one homeostatic variable…"). The immediately following line ("≥ 3 dose levels [OP-Entry 11.7]") IS tagged, confirming the ARCHITECT applied tags in this section but missed this one. |
| BF1.b | §3.4 (lines 150–157) | All six L8 control-arm failure routings ("if any level deviates from baseline," "if monotonic trend persists," "if exceeds candidate at any level," "if no expected degradation pattern," "if naive outperforms candidate," "if frozen shows monotonic trend") | `[PROPOSED — requires Rebecca sign-off]` (or explicit source class) | §2.4 (L7) and §4.5 (L10) control arms carry a source-tag column with `[PROPOSED — requires Rebecca sign-off]` and explicit tolerances. §3.4 (L8) has no source column and no tags — inconsistent. The §12 BF1 resolution explicitly scoped numeric tolerances to L7/L10 only, but the failure-routing conditions themselves still require a source-class tag. |
| BF1.c | §9.2 (lines 347–348) | Timebox tripwires "2" (sessions) and "4" (days) | `[PROPOSED]` | Escalation thresholds. They inherit the enclosing `[PROPOSED — requires Rebecca approval]` timebox framing but lack individual tags, unlike the adjacent "4 sessions" / "8 days" values which ARE tagged. |

**Classification:** spec defect (source-tag / provenance-discipline), not a candidate failure, instrument failure, construction bug, or law-text reconstruction. No locked bar is moved, raised, lowered, renamed, or reinterpreted. No law text reconstructed. The defect is that traceability tags are absent on these thresholds.

**Remediation (for ARCHITECT):** Add the missing P3 source-class tags to the three locations above. Do not change any threshold value, bar, kill condition, or scoring predicate. The §12 BF1 resolution's scope (numeric tolerances for L7/L10) may be extended to cover L8 control-arm tolerances if Rebecca directs, but at minimum each L8 control-arm failure routing must carry a source-class tag.

---

## 1. Law-diff (P2 — mandatory, performed first) — PASS

Each quoted law in the spec was diffed against `docs/ARCHITECTURAL_CONSTITUTION.md` byte-for-byte. Line citations verified against the constitution file.

| Law | Spec § | Const. line | Verbatim match | Line citation | Verdict |
|---|---|---|---|---|---|
| L7 | §2.1 | 24 | Exact | 24 ✓ | PASS |
| L8 | §3.1 | 26 | Exact | 26 ✓ | PASS |
| L10 | §4.1 | 30 | Exact | 30 ✓ | PASS |
| L14 | §5.1 | 40 | Substantive exact; trailing whitespace omitted | 40 ✓ | PASS (NF1) |
| L18 | §6.1 | 52 | Exact | 52 ✓ | PASS |

No law text reconstructed (P1 satisfied). Where verbatim text is insufficient to operationalize a test, the spec flags the gap as a STOP/escalation trigger rather than reconstructing (§0, consistent with §5.2 ARCHITECT obligation).

---

## 2. Source-tag audit (P3) — FAIL (BF1)

Numeric thresholds that ARE correctly tagged (no issue):

| Threshold | Value | Tag | Verdict |
|---|---|---|---|
| L7 AUROC | ≥ 0.75 | [LAW-L7] | PASS |
| L7 ECE | ≤ 0.10 | [LAW-L7] | PASS |
| L7 margin | > 0 at p < .05 | [LAW-L7] | PASS |
| L7 seeds | 5 | [BAR-Entry 11.3] | PASS |
| L8 min dose levels | ≥ 3 | [OP-Entry 11.7] | PASS |
| L8 monotonic test | all-seeds-direction + bootstrap-CI | [BAR-Entry 11.3] | PASS |
| L8 seeds | 5 | [BAR-Entry 11.3] | PASS |
| L10 abstention (drift) | ≥ 50% | [BAR-Entry 11.6] | PASS |
| L10 abstention (clean) | ≤ 10% | [BAR-Entry 11.6] | PASS |
| L10 drifted-AUROC floor | ≥ 0.70 | [BAR-Entry 14] | PASS |
| L10 confidence threshold τ | 0.70 | [PROPOSED] | PASS |
| L10 seed count | 5 | [PROPOSED] | PASS |
| L14 effect size | d ≥ 0.5 | [BAR-Entry 11.4] | PASS |
| L14 correlation | corr ≥ 0.3 @ 3 seeds | [BAR-Entry 14] | PASS |
| L7 control tolerances | (various) | [PROPOSED] | PASS |
| L10 control tolerances | (various) | [PROPOSED] | PASS |
| Multiplicity alpha_family | 0.05 | [OP-Entry 11.7] | PASS |
| Multiplicity alpha_seed | 0.05/3 | [OP-Entry 11.7] | PASS |
| M4 timebox (sessions/days) | 4 / 8 | [PROPOSED] | PASS |

Untagged thresholds → blocking (see BF1): §3.3 "≥ 1 homeostatic variable" (BF1.a); §3.4 L8 control-arm failure routings, no source column (BF1.b); §9.2 timebox tripwires 2 / 4 (BF1.c).

**Note on derived/structural quantities (non-blocking):** §7.1 "Seed pools: 1 pool of 5 seeds" and "Total stochastic checks: 45" are marked "—" (explicitly no source). "1 pool" is a structural design choice and "45" is a derived count (3 laws × 3 families × 5 seeds); the explicit "—" indicates the author acknowledged these are derived rather than source-tagged thresholds. Acceptable, but the ARCHITECt may annotate for clarity.

---

## 3. Provenance citation verification (P6) — PASS

Every "Entry n said X" claim verified against `docs/rulings/provenance_log.md` actual entry text. All cited line numbers confirmed.

| Citation | Spec claim | Log verification | Line | Verdict |
|---|---|---|---|---|
| Entry 5 | JUDGE measurability assessment; L7 "fully numeric (judgeable now)"; assessment only, did NOT create bars | Entry 5 header; L7 under "Fully numeric (judgeable now)"; "The JUDGE does not propose thresholds" | 87 ✓ | PASS |
| Entry 8 | JUDGE ruling on plan; identified corrections (L7 controls mandatory, L10 needs kill condition); did NOT lock bars | Entry 8 header; correction 3 "L7 controls missing from M4 — constitutionally mandatory"; correction 5 "L10 needs an explicit kill/failure condition"; "no bars invented, lowered, reinterpreted, or raised" | 134 ✓ | PASS |
| Entry 11 | Bars locked by Rebecca | Entry 11 header "Rebecca's adopted M0 decisions"; bars marked LOCKED | 172 ✓ | PASS |
| Entry 11.3 | Seeds = 5; all-seeds-direction + bootstrap-CI fallback | 11.3 matches | — | PASS |
| Entry 11.4 | L14 d ≥ 0.5 | 11.4 matches | — | PASS |
| Entry 11.6 | L10 abstention 50% drift / 10% clean | 11.6 matches | — | PASS |
| Entry 11.7 | §9 operationalizations adopted (dose levels, alpha structure) | 11.7 "All nine §9 operationalizations ADOPTED" | — | PASS (NF2) |
| Entry 11.8 | L7 graveyard gate deferred — Rebecca signs with prior results | 11.8 "L7 … DEFERRED — Rebecca will sign each with the prior milestone's results in front of her" | — | PASS (NF3) |
| Entry 14 | Drifted-AUROC ≥ 0.70 floor; corr ≥ 0.3 at 3 seeds; W4 confidence threshold at M4 | Entry 14 item (4) "drifted-AUROC ≥ 0.70 floor"; watch-item 5 "corr ≥ 0.3 at 3 seeds"; watch-item 4 "L10 confidence threshold — pre-register at M4" | 253 ✓ | PASS |
| Entry 27 | Amendment 1 — L4/E1 test redefined | Entry 27 "L4 test redefined (constitution amendment signed)"; v2 Amendment Log line 70 "Amendment 1 — L4/E1 test redefined (Entry 27)" | 598 ✓ | PASS |
| Entry 52 | M3 INSTRUMENT FAILURE retained; provisional advancement; seeds 201–203/301–303 retained, never rerun | Entry 52 "INSTRUMENT FAILURE retained. … provisional advancement to M4"; "Seeds 201-203 and 301-303 retained, never rerun" | 1628 ✓ | PASS |

---

## 4. F1 correction verification — PASS

| # | Correction | Requirement | Spec location | Verdict |
|---|---|---|---|---|
| F1.1 | L8 respecified from verbatim | Homeostatic variable + regulation target; calibrated-noise injection into self-model; ≥3 dose levels; dose-dependent rise; "only then" specificity | §3.3 | PASS |
| F1.2 | L14 three couplings | (1) readable by self-model; (2) affected by memory quality; (3) predictive targets for thick present | §5.3 | PASS |
| F1.3 | L10 reporting rule | Drifted-regime AUROC is reported number; clean is a ceiling, not a claim | §4.7 | PASS |
| F1.4 | L7 portrait clause | "No margin over the peer = portrait, not mirror — reported as such"; routed as KILL not INSTRUMENT_FAILURE | §2.3 | PASS |
| F1.5 | §12 Entry 5 vs Entry 8 | L7 bars attributed to [LAW-L7] (constitution text), not Entry 5; Entry 5 = assessment; Entry 8 = corrections; bars locked by Entry 11 | §12 provenance note | PASS |
| F1.6 (W4) | Stale changelog line fixed | W4 stale "pending" framing removed; τ = 0.70 pre-registered as [PROPOSED — requires Rebecca sign-off] | §4.3, changelog F1.6 | PASS |

All F1 corrections confirmed against verbatim law text and provenance log. F1.1 (L8) and F1.2 (L14) correctly reverse prior v1.2 reconstruction errors by operationalizing directly from the verbatim law text.

---

## 5. Regression + compliance — PASS

| # | Check | Finding | Verdict |
|---|---|---|---|
| 10 | Falsifiability maintained; all laws can fail | L7 (AUROC/margin/ECE/portrait KILLs), L8 (non-monotonic/frozen-shows-response/non-self-model-noise KILLs), L10 (abstention/drifted-AUROC KILLs), L14 (d/corr/readability KILLs) — every tested law has a failure path | PASS |
| 11 | Locked bars preserved | L10 50%/10% [BAR-Entry 11.6]; L14 d ≥ 0.5 [BAR-Entry 11.4]; L7 0.75/0.10/margin [LAW-L7]; L10 drifted-AUROC ≥ 0.70 [BAR-Entry 14] | PASS |
| 12 | L15–L17 fence respected | §1.2 + §10: "No L15, L16, or L17 work authorized before M5." | PASS |
| 13 | P4 date and regime in header | "Date: 2026-08-18 · Regime: B (post-Entry 27; constitution v1 + Amendment 1; §5 binding)" | PASS |
| 14 | INSTRUMENT FAILURE preserved | §1.2 "INSTRUMENT FAILURE retained"; §11 "No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label" | PASS |

**Additional compliance confirmations:**
- **O-14 (no re-run-on-failure):** §1.2 + §11 — "Seeds 201–203 and 301–303 retained, never rerun [BAR-Entry 52, O-14]."
- **O-15 (development diagnostic-only):** §7.2 + §11 — development seeds 101–105 [OP-Entry 11.7, O-15].
- **Hold-out seed rule:** §7.2 — "≥ 2 seeds unseen in development per scoring run."
- **Reproducibility contract:** §6.3 — M4 harness must use repaired semantic digest.
- **L9 / D1–D5 / L18 binding:** §11 acknowledges all standing constraints binding. (L9 is a continuous invariant listed as binding in §11 but not separately tested in M4; this is a scoping decision consistent with M4's L7/L8/L10/L14 focus, not a fidelity violation.)
- **No mechanism before test harness / no component promoted as integrated without L15 ablation:** §0 role boundary — "The ARCHITECT proposes specification, bars, and sequencing only. No code, no execution, no mechanism implementation, no merge." Respected.

---

## 6. Non-blocking findings

| ID | Finding | Class | Recommendation |
|---|---|---|---|
| NF1 | L14 verbatim quote omits trailing whitespace from constitution line 40 | P2 whitespace-only | Align trailing whitespace for strict byte-match |
| NF2 | Entry 11.7 log text does not enumerate the nine §9 operationalizations; alpha_seed/V4.4 specifics not byte-verifiable against 11.7 text | P6 granularity | Cite M3 implementation entries for V4.4 specifics |
| NF3 | Graveyard-gate tag `[BAR-Entry 11.8]` imprecise; 11.8 is a gate decision (DEFERRED), not a bar | P3 source-class precision | Use a gate-decision source class or annotate |
| NF4 | §7.1 derived quantities "1 pool" / "45" marked "—" | P3 clarity | Annotate as derived for clarity |

None of the above block the gate. They are precision/consistency improvements and do not constitute law-text reconstruction, threshold invention, bar movement, or provenance misattribution.

---

## 7. Preserved evidence

The following remain valid and are NOT invalidated by BF1 (which is a source-tagging defect only):
- All verbatim law quotations (L7/L8/L10/L14/L18) match the constitution byte-for-byte (P2 PASS).
- All locked bars (L7 0.75/0.10/margin, L8 ≥3 dose levels, L10 50/10 + 0.70 floor, L14 d ≥ 0.5 / corr ≥ 0.3) preserved with correct values.
- All provenance citations (Entries 5/8/11.x/14/27/52) verified against log text (P6 PASS).
- All F1 corrections (L8 respecification, L14 three-coupling, L10 reporting rule, L7 portrait clause, §12 provenance, W4) confirmed.
- INSTRUMENT FAILURE label and M3 verdicts preserved without reinterpretation.
- O-14 / O-15 / D1–D5 / L9 / L18 / hold-out seed rules all acknowledged as binding.
- Falsifiability, locked bars, L15–L17 fence, P4 header all preserved.

---

## 8. Pre-push self-scan attestation

A pre-push scan was performed on the review file and commit contents before pushing to `critic/r2-m4-v1.3-law-fidelity`. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII were found. The review references only repository-relative paths (`docs/…`, `specs/…`, `reviews/…`) and SHAs already public in the repository. Findings: none. Classification: acceptable.

---

## 9. Prohibited-action confirmations

- No modification of the spec, constitution, STATE.md, provenance log, or any artifact under review. Only this review file was created and committed.
- No merge to main (branch `critic/r2-m4-v1.3-law-fidelity` only; Rebecca sole merge authority).
- No scoring, no seed execution, no hold-out seed exposure.
- No L15/L16/L17 work before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- No re-run-on-failure (O-14); development diagnostic-only (O-15) not violated.

---

## 10. Handoff (return to WORKFLOW COORDINATOR)

- **Gate served:** R2 — law-fidelity review of M4 spec v1.3
- **Inputs/SHAs reviewed:** spec `architect/m4-spec-v1.3` @ `c0a3413` (`specs/m4_specification.md`, `specs/m4_specification_changelog.md`); constitution v1 `docs/ARCHITECTURAL_CONSTITUTION.md`; constitution v2 `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; provenance `docs/rulings/provenance_log.md`. Base main `956a5e7`.
- **Verdict:** **BLOCK**
- **Blocking findings:** BF1 — P3 source-class tags missing on §3.3 "≥ 1 homeostatic variable," §3.4 L8 control-arm failure routings, and §9.2 timebox tripwires 2/4. Fails the handoff's mandatory P3 check ("No untagged numbers"). Spec defect (source-tag/provenance-discipline); no bar moved, no law text reconstructed.
- **Non-blocking findings:** NF1–NF4 (P2 whitespace, P6 granularity on Entry 11.7, P3 source-class precision on Entry 11.8 tag, P3 clarity on derived quantities).
- **Preserved evidence:** law-diff (P2 PASS), provenance (P6 PASS), F1 corrections (PASS), locked bars, INSTRUMENT FAILURE, fences, O-14/O-15/D1–D5/L9/L18/hold-out rules — all preserved (see §7). None invalidated by BF1.
- **Review committed:** `reviews/critic_m4_v1.3_law_fidelity_review.md` on branch `critic/r2-m4-v1.3-law-fidelity`.
- **Exact next authorized role:** ARCHITECT (originating role) — to add the missing P3 source-class tags at the three BF1 locations only, then resubmit for R2 re-review. No change to any threshold value, bar, kill condition, or scoring predicate.
- **Explicitly prohibited for ARCHITECT during remediation:** No modifying any locked bar, threshold value, kill condition, or scoring predicate (only add source-class tags). No reconstructing law text. No scoring seeds. No rerun of seeds 201–203/301–303. No L15/L16/L17 before M5. No modification of STATE.md or provenance_log.md. No renaming/reinterpreting negative results. No merge to main.
- **Coordinator note:** After ARCHITECT remediation and a successful R2 re-review (CLEAR), route to Rebecca per spec §9.1 Step 3 (approve M4 spec + L7 graveyard-gate sign-off + L10 threshold + timebox). The spec's §13 "Next recipient: Reviewer TBD per G0-3" is resolved by this R2 review.
- **Confirmation:** No scoring, no rerun, no hold-out seed exposure, and no unauthorized merge occurred during this review.
