# AUDITOR Return Handoff — Versioned-Law Compliance Audit

**Issued by:** External AUDITOR (independent, one-time; no prior involvement; no continuing role)
**Date:** 2026-08-18 15:02 EDT
**Next recipient:** WORKFLOW COORDINATOR (for routing)
**Pairs with:** `handoffs/AUDITOR_VERSIONED_LAW_COMPLIANCE_AUDIT_HANDOFF.md` (inbound)
**Deliverables of record:** `audits/AUDITOR_COMPLIANCE_MATRIX.md` (one row per artifact) and `audits/AUDITOR_FINDINGS_SUMMARY.md` (F1–F7, W1–W5, dispositions)

**Authority note.** Per the authority chain (Rebecca > constitution > prompt > agent judgment): everything in §3 below that requires a ruling is BLOCKED until Rebecca rules. This handoff routes work; it does not authorize any disposition. No agent speaks for Rebecca, including the auditor.

---

## 1. Audit record (summary)

- **Scope:** every artifact in the CRITIC's source-bundle manifest, M0 → M4 spec v1.2. Main HEAD `3f44caf` verified; M4 branch `5496a22` verified; constitution v1 SHA-256 verified (`509f11c3…f93b19`); v2 law text confirmed byte-identical to v1.
- **Regimes applied:** A = pre-Entry-27, v1 verbatim; B = Entry 27 onward, v1 + Amendment 1 with Entry 29 supersession. Every artifact regime-dated before judgment.
- **Tally:** 78 COMPLIANT · 9 RECONSTRUCTION-INFIDELITY · 5 PROCESS-BREACH (two shared findings) · 3 UNRESOLVABLE.
- **Directional check: CLEAN.** No artifact predating Entry 27 references the three-property test, fair-naive arm, battery-validity, or amended kills.
- **Structurally sound throughout:** no JUDGE ever lowered a bar; no negative was ever renamed (E1-RUN-1 crash, M3 201–203 and 301–303 INSTRUMENT FAILURE, `bit_identical=false` all retain original labels); both reruns used Rebecca's signed exception paths (Entry 27 ruling 4; Entry 43 four-part test); Entry 11.4's d ≥ 0.5 is fully compliant pre-registration (Known Instance 2 resolved COMPLIANT).

### Findings index (details in `audits/AUDITOR_FINDINGS_SUMMARY.md`)

| ID | Finding | Verdict | Materiality |
|---|---|---|---|
| F1 | M4 spec (v1.0–v1.2 + changelog): L8 test substituted (stakes/difficulty→performance instead of calibrated-noise→homeostatic regulation error); L14 operationalization contains no homeostatic couplings; L10 reporting rule absent; L7 reporting clause absent; Entry 5/8 tier misattribution in §12 | RECONSTRUCTION-INFIDELITY | HIGH prospective, zero retrospective (nothing has run against it) |
| F2 | E1 L18 battery has no distinct permuted arm; E1 GREEN scored on six-arm battery. Disclosed (§N7), pre-registered, Principal-gated — never memorialized as waiver/amendment | PROCESS-BREACH (narrow) | MODERATE |
| F3 | All three M4 CRITIC reviews conducted pre-publication against the same reconstruction; Entry 5/8 misattribution missed three times | RECONSTRUCTION-INFIDELITY | MODERATE |
| F4 | Regime A: kill (a) presented as L4 law text (critic_e1_spec_review, existence_proof_analysis) | RECONSTRUCTION-INFIDELITY | LOW — self-cured by Entry 27 |
| F5 | "Never recomputed" folded into L13's requirement text (m3_e2_implementation_task_spec) | RECONSTRUCTION-INFIDELITY | LOW — editorial |
| F6 | L20 first-statement formula absent from governance paper opening and FUNDING_OBJECTIVES entirely | PROCESS-BREACH (minor) | LOW — one-line fixes |
| F7a–e | UNRESOLVABLE cluster: M0_DECISION_SHEET absent (O-6); executed M3 harness SHA vs checked-in source; two acknowledged inventory/contract discrepancies; m3_run_results.json LFS/local-retention; five undated review files | UNRESOLVABLE | Record-closure items |
| W1–W5 | Watch items: warn-only R3 guard; "L20_drift" label; M3 GO face-date; stale changelog line; manifest regime label for e1_spec.md | — | Hygiene |

---

## 2. Root-cause statement (what the team must internalize)

Every deviation found reduces to two causes:

1. **Binding text outside the repo.** F1, F3, and F7a all trace to constitutional/pre-registration text living as attachments unavailable to fresh sessions. Agents have no memory; the repo is their only inheritance. Text that is not in the repo does not exist for the next session.
2. **Source-class conflation.** F4, F5, W2, and the F1 §12 misattribution are all the same error: a locked bar, adopted operationalization, or provenance phrase stated as if it were constitutional law text. Nobody violated a bar; people mislabeled where bars come from.

The compliance protocol in §4 is built to eliminate exactly these two causes.

---

## 3. Resolution ladder — items blocking forward motion

**Ordering is binding-as-proposed: Gate 0 first; R-items only after their gating ruling exists. M4 build authorization should not be requested until R1–R4 are closed.**

### Gate 0 — Rebecca rulings required (BLOCKING; nothing below proceeds without its ruling)

| # | Decision needed | Options on the table |
|---|---|---|
| G0-1 | F1 disposition: authorize M4 spec correction cycle from verbatim law text | Approve correction scope per F1 items 1–6 (respecify §3/L8 from blank page; rewrite §5/L14 couplings; add §4/L10 reporting rule; add §2/L7 portrait clause; fix §12 provenance; fix W4 stale line) |
| G0-2 | F2 disposition: E1 permuted-arm gap | (a) Signed waiver/amendment-log note memorializing the six-arm E1 battery as accepted, OR (b) mandate a distinct permuted arm in all future E1-class scoring. Neither option relabels E1 GREEN |
| G0-3 | F3 disposition: reviewer for the corrected M4 spec | Fresh-context reviewer (auditor's recommendation, given CRITIC conflict-of-interest and three-time miss) vs. standing CRITIC with mandatory law-diff checklist (§4) |
| G0-4 | F7a: publish M0_DECISION_SHEET (or a Rebecca-attested extract) to close O-6 | Publication decision is Rebecca's (ownership/privacy review noted in GOVERNANCE_SOURCE_MAP) |
| G0-5 | Adopt (or amend) the §4 Compliance Protocol below as binding standing process | Adopt / amend / reject per section |

### R-items — routed work (owner → verifier), each conditioned on its Gate 0 ruling

| # | Blocked by | Owner | Task | Done when |
|---|---|---|---|---|
| R1 | G0-1 | ARCHITECT | M4 spec v1.3: respecify L8 from published verbatim text (define ≥1 homeostatic variable + regulation target; calibrated-noise injection into self-model at ≥3 dose levels; measure regulation error; dose-dependent rise + "only then" specificity leg); rewrite L14 as the three couplings of those variables (d ≥ 0.5 Entry 11.4 and corr ≥ 0.3 Entry 14 retained as bars); add L10 reporting rule and L7 portrait clause verbatim; correct §12 (Entry 5 vs Entry 8) and W4. The h=1/3/5 design may survive only as a supplementary probe, never carrying the L8 claim | v1.3 committed on branch with changelog; every law section opens with the verbatim law quote per §4.1-P2 |
| R2 | G0-3, R1 | Reviewer per G0-3 | Post-publication law-fidelity review of v1.3: diff every quoted law against `docs/ARCHITECTURAL_CONSTITUTION.md` byte-for-byte; verify every threshold carries a source tag; verify provenance citations against the log | CLEAR issued with an explicit law-diff table in the review |
| R3 | G0-2 | RECORDER | Record the F2 ruling: waiver note in the amendment log of v2 (option a) or standing-rule entry (option b); provenance entry either way | Entry appended; STATE.md reconciled by INTEGRATOR |
| R4 | — (no ruling needed) | RECORDER | Commit `audits/AUDITOR_COMPLIANCE_MATRIX.md`, `audits/AUDITOR_FINDINGS_SUMMARY.md`, and this handoff to the public repo via PR (Rebecca merges); provenance entry for audit receipt | Audit artifacts on main; entry logged |
| R5 | — | RECORDER | F7b: custody attestation of the executed M3 harness SHA-256 against the local retention copy per `RUN_PROVENANCE_AND_LOCAL_RETENTION.md`; F7e: date-stamp addendum for the five undated review files | Attestation + addendum committed |
| R6 | — | ARCHITECT → CRITIC | F7c: one-paragraph reconciliation ruling proposal for the two acknowledged inventory/contract discrepancies (`ranked_occurrences_500` vs 1000 rows; L3 `innovations_1010x8` vs `1110x8`); CRITIC verifies; Rebecca signs | Reconciliation on record |
| R7 | — | ARCHITECT | F6: add the one-sentence L20 formula as the first substantive statement of `docs/governance_paper_final.md` and `FUNDING_OBJECTIVES.md` (optionally README/RESEARCH_STATUS for uniformity) | Edits committed |
| R8 | — | TASK BUILDER → CRITIC | W1: make the R3 hold-out guard in `e1_experiment.py` (and any M4 harness descendant) fail-closed; CRITIC verifies; no scoring semantics touched | Guard raises instead of warning; CRITIC verification note |
| R9 | — | INTEGRATOR | W2: rename `L20_drift`/"L20 self-test" labels to operationalization names that do not carry a law number (e.g., `OP_drift_selftest`), with a mapping note preserving history — labels only, no bar or threshold changes; W5: correct the manifest regime label for `specs/e1_spec.md` (Regime B); W3: date-label note on `REBECCA_M3_GO.md` | STATE.md + labels reconciled; RECORDER hash-attests |
| R10 | G0-4 | RECORDER | Publish M0_DECISION_SHEET (or attested extract); close O-6; resolve corr ≥ 0.3 binding-bar status on the record | O-6 closed in provenance log |

**Sequencing note for the COORDINATOR:** R4, R5, R7, R8, R9 are parallel-safe immediately. R1→R2 is the critical path to the M4 gate. R3 and R10 follow their rulings. Recommend requesting all five Gate 0 rulings from Rebecca in a single package to avoid serial round-trips.

---

## 4. Standing method: Versioned-Law Compliance Protocol (proposed as binding; requires G0-5)

### 4.1 Universal rules (all roles, all artifacts)

- **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. **Reconstruction of constitutional text is forbidden** — the honest move that produced F1 is now unnecessary (the constitution is published) and therefore prohibited.
- **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
- **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization, e.g. Entry 11.7's §9 set), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.
- **P4 — Regime dating.** Every new artifact states its date and regime in its header. Acts are judged only against their own regime's text; later text is never applied backward.
- **P5 — Deviation memorialization.** Any deviation from `[LAW]` text — however sensible, however disclosed — is inoperative for scoring until Rebecca has signed a waiver or amendment recorded in the v2 amendment log. Disclosure in a spec (the F2 pattern) is necessary but no longer sufficient.
- **P6 — Provenance citation check.** Any claim of the form "Entry n said X" must be verified against the entry's actual text before commit. (The Entry 5/8 confusion survived four documents because nobody re-opened Entry 8.)

### 4.2 Per-role obligations

- **ARCHITECT:** P1/P2/P3 in every spec. A law section that cannot be written from verbatim text is a STOP, not a reconstruction. Gap flags are escalation triggers, not permissions to proceed.
- **CRITIC:** First checklist item of every review, before substance: (i) diff every quoted law against the constitution file; (ii) verify every threshold's source tag; (iii) verify every provenance citation against the log. A review that skips the law-diff is incomplete. The existing bar-laundering check stays as is.
- **JUDGE:** Before scoring, verify each applied bar traces to a `[LAW]` or `[BAR]` tag. Refuse to score any run whose bars include untagged or `[PROPOSED]` criteria. (Unchanged: never lower, never soften, negatives retained.)
- **TASK BUILDER:** Implement only tagged criteria. All protective guards (hold-out seeds, scoring-mode routing) fail-closed. Diagnostic runs stay O-15-labeled, development-pool-only.
- **INTEGRATOR:** STATE.md entries carry source tags; `locked_bars` may contain only `[LAW]`/`[BAR]`/`[OP]` items, with `[PROPOSED]` quarantined in a separate block. STATE.md keeps its non-constitutional disclaimer.
- **RECORDER:** Every milestone package includes a custody line verifying the constitution file's SHA-256 unchanged. All new artifacts date-stamped at creation. Amendment log is the sole registry of waivers (P5).
- **WORKFLOW COORDINATOR:** (i) Enforce Gate 0 ordering in §3; (ii) route every new milestone spec and every constitutional document through the G0-3-designated fresh-context law-fidelity review before Rebecca's gate — standing CRITIC review does not substitute for it; (iii) at each milestone gate, commission a lightweight fresh-context compliance spot-check (this audit's method, scoped to the milestone's new artifacts) rather than deferring to a single end-of-program audit; (iv) reject any handoff that asks a role to proceed on non-repo text.

### 4.3 What this protocol deliberately does NOT do

It adds no new bars, no new doctrine, and no new document classes beyond the tags and the law-diff step. Consistent with the audit's advice to Rebecca: after R1–R10, the governance layer should be starved of further expansion until M4 produces a scored result. Process is not the product.

---

## 5. Constraints restated (unchanged and binding)

O-14 no rerun-on-failure · O-15 diagnostics non-scoring/non-cited · D1–D5 · L9 fence · L18 full battery on every positive claim · no L15/L16/L17 before M5 · ≥2 hold-out seeds unseen in development · no renaming negatives · scoring only via Rebecca's courier channel · Rebecca sole gate and merge authority.

## 6. Auditor's exit statement

The auditor's engagement ends with this handoff. The audit artifacts are assessments, not rulings; nothing herein authorizes action absent Rebecca's Gate 0 decisions. The auditor modified no artifact, merged nothing, renamed nothing, executed no scoring, and holds no continuing authority. Conflict-of-interest note for the record: the audit's evidence extraction used four parallel read-only passes whose non-compliant proposals were each re-verified against primary sources by the auditor; five extraction-stage proposals were overturned on primary evidence, documented in `audits/AUDITOR_FINDINGS_SUMMARY.md` §Method.

**Routing:** WORKFLOW COORDINATOR → Rebecca (Gate 0 package, all five rulings) → route R-items per §3 → R2 CLEAR → Rebecca M4 gate.
