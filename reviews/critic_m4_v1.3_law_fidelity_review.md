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

---

## Verdict

### **CLEAR**

No blocking findings. The M4 spec v1.3 is law-fidelity compliant under the §5 Versioned-Law Compliance Protocol (P1–P6). All verbatim law quotations match the constitution byte-for-byte (one whitespace-only non-substance difference on L14). All numeric thresholds carry P3 source-class tags. All provenance citations verified against actual entry text. All six F1 corrections confirmed. Falsifiability, locked bars, the L15–L17 fence, P4 regime dating, and the INSTRUMENT FAILURE label are all preserved. Next authorized role may proceed.

---

## 1. Law-diff (P2 — mandatory, performed first)

Each quoted law in the spec was diffed against `docs/ARCHITECTURAL_CONSTITUTION.md` byte-for-byte. Line citations were verified against the constitution file.

| Law | Spec § | Const. line | Verbatim match | Line citation | Verdict |
|---|---|---|---|---|---|
| L7 | §2.1 | 24 | Exact | 24 ✓ | PASS |
| L8 | §3.1 | 26 | Exact | 26 ✓ | PASS |
| L10 | §4.1 | 30 | Exact | 30 ✓ | PASS |
| L14 | §5.1 | 40 | Substantive exact; trailing whitespace omitted | 40 ✓ | PASS (NF1) |
| L18 | §6.1 | 52 | Exact | 52 ✓ | PASS |

**NF1 (non-blocking):** The L14 quote (§5.1) omits the trailing whitespace present on constitution line 40 ("decorative. " → "decorative."). This is a whitespace-only, non-substantive difference; no law text reconstructed. Recommend the ARCHITECT align trailing whitespace for a strict byte-match in a future revision. Not a P2 violation.

No law text was reconstructed (P1 satisfied). Where the verbatim text is insufficient to fully operationalize a test, the spec flags the gap as a STOP/escalation trigger rather than filling it by reconstruction (§0, consistent with §5.2 ARCHITECT obligation).

---

## 2. Source-tag audit (P3)

Every numeric threshold in the spec carries a P3 source-class tag. No untagged numeric thresholds found in any law or bar section.

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
| L7/L8 control tolerances | (various) | [PROPOSED] | PASS |
| L10 control tolerances | (various) | [PROPOSED] | PASS |
| Multiplicity alpha_family | 0.05 | [OP-Entry 11.7] | PASS |
| Multiplicity alpha_seed | 0.05/3 | [OP-Entry 11.7] | PASS |
| M4 timebox | 4 sessions / 8 days | [PROPOSED] | PASS |

**NF2 (non-blocking — P3 consistency):** The L8 control-arm failure routings (§3.4) lack P3 source-class tags and numeric tolerances, whereas the L7 (§2.4) and L10 (§4.5) control arms carry `[PROPOSED — requires Rebecca sign-off]` tags with explicit tolerances. The §12 BF1 resolution explicitly scoped numeric tolerances to L7 and L10 only. The L8 control arms carry no numeric thresholds (their routings are qualitative: "if any level deviates from baseline," "if monotonic trend persists," etc.), so P3's "no untagged numbers" is not strictly violated, and the arms are structurally present (L18 satisfied). Recommend the ARCHITECT tag the L8 control-arm routings for source-class consistency in a future revision.

**NF3 (non-blocking — P3 on timebox tripwires):** The timebox tripwire values (§9.2: sessions = 2, days = 4) lack individual source tags. These inherit the enclosing `[PROPOSED — requires Rebecca approval]` framing of the timebox block, so they are implicitly proposed. Non-blocking; recommend explicit tagging for completeness.

---

## 3. Provenance citation verification (P6)

Every "Entry n said X" claim was verified against `docs/rulings/provenance_log.md` actual entry text. All cited line numbers confirmed against the file.

| Citation | Spec claim | Log verification | Line | Verdict |
|---|---|---|---|---|
| Entry 5 | JUDGE measurability assessment; classified L7 "fully numeric (judgeable now)"; assessment only, did NOT create bars | Entry 5 header "JUDGE produced bar measurability assessment"; L7 listed under "Fully numeric (judgeable now)"; "The JUDGE does not propose thresholds" | 87 ✓ | PASS |
| Entry 8 | JUDGE ruling on plan; identified corrections (L7 controls mandatory, L10 needs kill condition); did NOT lock bars | Entry 8 header "JUDGE produced bar measurability ruling on the plan"; correction 3 "L7 permuted/empty/shuffled controls missing from M4 — constitutionally mandatory"; correction 5 "L10 needs an explicit kill/failure condition"; "no bars invented, lowered, reinterpreted, or raised" | 134 ✓ | PASS |
| Entry 11 | Bars locked by Rebecca | Entry 11 header "Rebecca's adopted M0 decisions"; bars marked LOCKED | 172 ✓ | PASS |
| Entry 11.3 | Seeds = 5; all-seeds-direction + bootstrap-CI fallback | 11.3 "Seeds raised to 5 … all-seeds-direction + bootstrap-CI fallback" | — | PASS |
| Entry 11.4 | L14 d ≥ 0.5 | 11.4 "L14 effect-size floor raised to d ≥ 0.5" | — | PASS |
| Entry 11.6 | L10 abstention 50% drift / 10% clean | 11.6 "L10 abstention dual bar: 50% under drift / 10% clean" | — | PASS |
| Entry 11.7 | §9 operationalizations adopted (dose levels, alpha structure) | 11.7 "All nine §9 operationalizations ADOPTED" | — | PASS (NF4) |
| Entry 11.8 | L7 graveyard gate deferred — Rebecca signs with prior results | 11.8 "L7 … gates DEFERRED — Rebecca will sign each with the prior milestone's results in front of her" | — | PASS (NF5) |
| Entry 14 | Drifted-AUROC ≥ 0.70 floor; corr ≥ 0.3 at 3 seeds; W4 confidence threshold at M4 | Entry 14 item (4) "backstopped by the drifted-AUROC ≥ 0.70 floor"; watch-item 5 "L14 corr ≥ 0.3 at 3 seeds"; watch-item 4 "L10 confidence threshold — pre-register at M4" | 253 ✓ | PASS |
| Entry 27 | Amendment 1 — L4/E1 test redefined | Entry 27 "L4 test redefined (constitution amendment signed)"; v2 Amendment Log line 70 "Amendment 1 — L4/E1 test redefined (Entry 27)" | 598 ✓ | PASS |
| Entry 52 | M3 INSTRUMENT FAILURE retained; provisional advancement; seeds 201–203/301–303 retained, never rerun | Entry 52 "INSTRUMENT FAILURE retained. … provisional advancement to M4"; "Seeds 201-203 and 301-303 retained, never rerun" | 1628 ✓ | PASS |

**NF4 (non-blocking — P6 granularity):** Entry 11.7's log text records only "All nine §9 operationalizations ADOPTED (Closes O-5)" without enumerating them. The specific alpha_seed = 0.05/3 formula and V4.4 framework details (1000 null replicates, plus-one upper-tail, alpha_family = 0.05) therefore cannot be byte-verified against Entry 11.7's text — only the adoption of "§9 operationalizations" is verifiable. Attribution points to the correct entry and is consistent with "as implemented at M3." Non-blocking; the ARCHITECT may cite the M3 implementation entries for the V4.4 specifics in a future revision.

**NF5 (non-blocking — source-class precision):** The graveyard-gate requirement (§2.2) is tagged `[BAR-Entry 11.8]`, but Entry 11.8 is a gate decision (DEFERRED/SIGNED), not a locked bar. The substantive content is correctly cited; the source-class tag is imprecise. Non-blocking.

---

## 4. F1 correction verification

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

## 5. Regression + compliance

| # | Check | Finding | Verdict |
|---|---|---|---|
| 10 | Falsifiability maintained; all laws can fail | L7 (AUROC/margin/ECE/portrait KILLs), L8 (non-monotonic/frozen-shows-response/non-self-model-noise KILLs), L10 (abstention/drifted-AUROC KILLs), L14 (d/corr/readability KILLs) — every tested law has a failure path | PASS |
| 11 | Locked bars preserved | L10 50%/10% [BAR-Entry 11.6] preserved; L14 d ≥ 0.5 [BAR-Entry 11.4] preserved; L7 0.75/0.10/margin [LAW-L7] preserved; L10 drifted-AUROC ≥ 0.70 [BAR-Entry 14] preserved | PASS |
| 12 | L15–L17 fence respected | §1.2 + §10: "No L15, L16, or L17 work authorized before M5. This spec does not propose integration tests, mechanisms, or claims." | PASS |
| 13 | P4 date and regime in header | Header: "Date: 2026-08-18 · Regime: B (post-Entry 27; constitution v1 + Amendment 1; §5 binding)" | PASS |
| 14 | INSTRUMENT FAILURE preserved | §1.2 "INSTRUMENT FAILURE retained"; §11 "No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label" | PASS |

**Additional compliance confirmations:**
- **O-14 (no re-run-on-failure):** §1.2 + §11 — "Seeds 201–203 and 301–303 retained, never rerun [BAR-Entry 52, O-14]." Preserved.
- **O-15 (development diagnostic-only):** §7.2 + §11 — development seeds 101–105 [OP-Entry 11.7, O-15]; "Development runs diagnostic-only [O-15]." Preserved.
- **Hold-out seed rule:** §7.2 — "≥ 2 seeds unseen in development per scoring run. Development seeds: 101–105." Preserved.
- **Reproducibility contract:** §6.3 — M4 harness must use repaired semantic digest. Consistent with the two-digest, three-class-field architecture.
- **L9 / D1–D5 / L18 binding:** §11 acknowledges all standing constraints binding.
- **No mechanism before test harness / no component promoted as integrated without L15 ablation:** Spec proposes specification only; role boundary (§0) — "The ARCHITECT proposes specification, bars, and sequencing only. No code, no execution, no mechanism implementation, no merge." Respected.

---

## 6. Non-blocking findings summary

| ID | Finding | Class | Recommendation |
|---|---|---|---|
| NF1 | L14 verbatim quote omits trailing whitespace from constitution line 40 | P2 whitespace-only | Align trailing whitespace for strict byte-match |
| NF2 | L8 control-arm failure routings (§3.4) lack P3 source tags and numeric tolerances, unlike L7 (§2.4) / L10 (§4.5) | P3 consistency | Tag L8 control-arm routings; consider whether qualitative tolerances need Rebecca sign-off |
| NF3 | Timebox tripwire values (§9.2: 2 / 4) lack individual source tags | P3 completeness | Explicitly tag tripwire values |
| NF4 | Entry 11.7 log text does not enumerate the nine §9 operationalizations; alpha_seed/V4.4 specifics not byte-verifiable against 11.7 text | P6 granularity | Cite M3 implementation entries for V4.4 specifics |
| NF5 | Graveyard-gate tag `[BAR-Entry 11.8]` imprecise; 11.8 is a gate decision, not a bar | P3 source-class precision | Use a gate-decision source class or annotate |

None of the above block the gate. All are precision/consistency improvements for a future revision and do not constitute law-text reconstruction, threshold invention, bar movement, or provenance misattribution.

---

## 7. Preserved evidence

- All locked bars (L7, L8 dose levels, L10 50/10 + 0.70 floor, L14 d ≥ 0.5 / corr ≥ 0.3) preserved with correct source tags.
- All F1 corrections (L8 respecification, L14 three-coupling, L10 reporting rule, L7 portrait clause, §12 provenance, W4) confirmed.
- INSTRUMENT FAILURE label and M3 verdicts preserved without reinterpretation.
- O-14 / O-15 / D1–D5 / L9 / L18 / hold-out seed rules all acknowledged as binding.
- The prior off-repo CRITIC clear carries no R2 weight (per Principal's resolution sequence Step 3); this in-repo review is the operative R2 artifact.

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
- **Verdict:** **CLEAR**
- **Blocking findings:** None.
- **Non-blocking findings:** NF1–NF5 (P2 whitespace, P3 consistency on L8 control arms and timebox tripwires, P6 granularity on Entry 11.7 enumeration, P3 source-class precision on Entry 11.8 tag). Recommendations for a future revision; do not block the gate.
- **Preserved evidence:** All locked bars, F1 corrections, INSTRUMENT FAILURE label, O-14/O-15/D1–D5/L9/L18/hold-out rules preserved (see §7).
- **Review committed:** `reviews/critic_m4_v1.3_law_fidelity_review.md` on branch `critic/r2-m4-v1.3-law-fidelity`.
- **Next authorized role:** WORKFLOW COORDINATOR (for Step 6 sequencing) → per spec §9.1, Step 3 is Rebecca (approve M4 spec + L7 graveyard-gate sign-off + L10 threshold + timebox). The spec's §13 "Next recipient: Reviewer TBD per G0-3" is now resolved by this R2 review; coordinator should route to Rebecca for the approval gate.
- **Explicitly prohibited for next roles:** No modification of locked bars/thresholds/scoring predicates; no scoring seeds; no rerun of seeds 201–203/301–303; no L15/L16/L17 before M5; no modification of STATE.md or provenance_log.md; no renaming/reinterpreting negative results; no merge to main without Rebecca's explicit authorization.
- **Confirmation:** No scoring, no rerun, no hold-out seed exposure, and no unauthorized merge occurred during this review.
