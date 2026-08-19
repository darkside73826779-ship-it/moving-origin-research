# CRITIC Delta Re-Clear — M4 Specification v1.6

**Gate served:** Fresh-context law-fidelity + design-soundness review of spec v1.6 (Rebecca's nine Step 7 gate rulings)
**Reviewer:** CRITIC (fresh-context; prior review was v1.5 advisor-cycle CLEAR at `91c790a`)
**Date:** 2026-08-18 · **Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Spec under review:** `architect/m4-spec-v1.6` at **`b22609f`**
**Delta base:** `487843f` (v1.5, prior CRITIC-cleared)
**Review surface:** `487843f...b22609f` — `specs/m4_specification.md` (+107/−54), `specs/m4_specification_changelog.md` (+52/−2), `handoffs/ARCHITECT_M4_SPEC_V1.6_HANDOFF.md` (+63)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this review > agent judgment. CRITIC does not speak for Rebecca.

---

## Verdict: BLOCK

**Block class: provenance / tag-state defect (governance), not scientific/design.**

The substance is strong and verifies: all nine of Rebecca's Step 7 gate rulings (Entry 76) are implemented correctly; all five verbatim law quotations are byte-exact against the constitution; every new/changed threshold carries a P3 source tag; the two hard discriminants both pass — Ruling 2 closes the abstention-exclusion gaming surface (primary AUROC uses pre-abstention scores over the complete fixed drifted population; all-abstain fails the ≥0.70 floor), and Ruling 9's tolerance calibration is explicitly candidate-blind (seeds 101–105 not inputs) and frozen-before-scoring (no post-candidate adjustment); the delta is confined to the nine rulings + changelog + handoff; no locked bar value changed (the L10 0.70 floor is preserved — only the population it is computed over changes); the L3 pre-scoring gate, O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, and the L15–L17 fence are all preserved. The nine rulings are internally consistent with no residual score-chasing path.

**Why BLOCK, not CLEAR:** the next authorized action on CLEAR is assembly of the formal Step 7 gate package for Rebecca's graveyard-gate signature. The spec under review is not in a consistent approval state for that signature: its §0 provenance statement is stale (says "reviewed through Entry 72" while Entry 75–76 exist and v1.6 implements Entry 76's rulings); it does not cite Entry 76 as the source authority for the nine rulings it attributes to "Per Rebecca's ruling"; and it retains stale `[PROPOSED — requires Rebecca sign-off]` / `[PROPOSED — requires Rebecca ruling]` tags on items Rebecca has already approved (Ruling 3 L8 design elements; Ruling 4 B1). In this project source-class and approval-status tags are governance controls, not cosmetic labels — contradictory approval states inside the spec cannot be sent to Rebecca for signature. These are correctable by a narrow mechanical ARCHITECT pass; they do not touch spec substance, locked bars, kill conditions, or the nine rulings' implementations. Returns to ARCHITECT for correction, then re-clear.

---

## Step 1 — Law-diff (§5.2 mandatory, completed before substantive review)

Method: script extracted every blockquote law quote in `specs/m4_specification.md` (lines beginning `> **Lx —`) and compared byte-for-byte against the canonical law line in `docs/ARCHITECTURAL_CONSTITUTION.md` on `main`.

| Law | Spec quote location | Constitution line | Result | Notes |
|---|---|---|---|---|
| L7 | §2.1, spec line 62 | 24 | BYTE-EXACT | — |
| L8 | §3.1, spec line 147 | 26 | BYTE-EXACT | — |
| L10 | §4.1, spec line 241 | 30 | BYTE-EXACT | — |
| L14 | §5.1, spec line 309 | 40 | EXACT-after-rstrip | Constitution line 40 carries one trailing whitespace char omitted in the spec quote. Substantive text identical. Non-blocking. |
| L18 | §6.1, spec line 349 | 52 | BYTE-EXACT | — |

All five required verbatim quotations byte-exact (L14 differs only by one trailing space on the constitution side). P2 satisfied. All line citations correct.

### P3 — source-class tags on thresholds

Every new or changed threshold in the v1.6 delta carries a source tag. Verified, including the new Ruling-2/Ruling-9 constructs:
- Primary pre-abstention drifted AUROC: `[BAR-Entry 14] [LAW-L10]` ✓
- All-abstain = floor failure: `[BAR-Entry 14]` ✓
- τ calibration (drift ≥50% / clean ≤10%): `[BAR-Entry 11.6] [BAR-Entry 11]` ✓
- L7 inference Option C (per-seed threshold / paired-bootstrap margin): `[LAW-L7] [BAR-Entry 11]` / `[BAR-Entry 11.3]` ✓
- L8 standardized severity-matching predefinitions: `[PROPOSED — requires Rebecca sign-off] [LAW-L19]` (see non-blocking finding NB-1: tags stale) ✓ present
- FWFP milestone-wide + tolerance calibration: `[BAR-Entry 43]` ✓
- Timebox: `[Rebecca-approved]` ✓
- L10 seeds: `[BAR-Entry 11.3] (v1.6 Ruling 8)` ✓

No untagged new thresholds. P3 satisfied (tag-class precision issues noted as non-blocking NB-1/NB-2).

### P6 — provenance citation verification

Rebecca's nine rulings are recorded in **Entry 76** (`docs/rulings/provenance_log.md` line 2106: "Principal rulings: M4 Step 7 gate — nine items ruled (advisor-assisted)", dated 2026-08-18, rulings decided 22:54 EDT / logged 23:02 EDT). Each ruling in Entry 76 was verified against the spec's implementation (see Step 2). Reused citations re-verified:

| Citation | Verified |
|---|---|
| Entry 11.3 (5 seeds + all-seeds-direction + bootstrap-CI fallback) | Entry 11.3 line 186 ✓ |
| Entry 11.8 (graveyard gate deferred) | Entry 11.8 ✓ |
| Entry 14 (drifted-AUROC ≥0.70 floor; corr ≥0.3 W5) | Entry 14 ✓ |
| Entry 43 (FWFP ≤5% standing rule; four-part test) | Entry 43 ✓ |
| Entry 52 (M3 INSTRUMENT FAILURE, provisional advancement) | Entry 52 ✓ |
| Entry 72 (Option A — L3 pre-scoring gate) | Entry 72 ✓ |
| M0 Decision Sheet line 20 (peer spec), line 21 (L8 bars), line 29 (inferential policy) | verified verbatim ✓ |
| **Entry 76 (nine rulings)** | line 2106 ✓ — all nine match spec implementation |

P6 satisfied: every ruling the spec attributes to "Per Rebecca's ruling" is verifiable against Entry 76 text, and the rulings match the spec's implementation.

---

## Step 2 — Ruling-by-ruling verification (1–9)

| # | Ruling (Entry 76) | Spec implementation | Result |
|---|---|---|---|
| 1 | L7 inference Option C: AUROC/ECE per-seed threshold bars (any-seed KILL, no fallback); margin = direction test (5 paired seeds, all-seed direction + pooled paired-bootstrap 95% CI excl. zero, M0 Entry 11.3 fallback); v1.4 "Amendment 3" retracted | §2.5 lines 123–135: AUROC/ECE per-seed threshold no-fallback; margin direction test with paired-bootstrap CI; "The v1.4 'Amendment 3' hard rule (no fallback for any L7 bar) is retracted. The v1.5 STOP/escalation is resolved by this ruling. [P5 — authorized by Rebecca's ruling]". Amendment 3 retracted, not silently restored. | ADDRESSED ✓ |
| 2 | L10: primary drifted AUROC over complete fixed drifted population using pre-abstention scores; answered-case AUROC secondary; all-abstain fails ≥0.70 floor (not N/A); τ calibrated to satisfy drift ≥50% AND clean ≤10% on held-out data; floor ≥0.70 preserved (value unchanged) | §4.3 lines 259–269: "Primary drifted AUROC: Computed over the complete fixed drifted population using pre-abstention scores — the candidate's confidence/ranking before abstention is applied. This closes the abstention-exclusion gaming surface"; "All-abstain AUROC... fails the ≥ 0.70 floor... All-abstain is not N/A — it is a failure"; answered-case AUROC "not the headline"; floor "≥ 0.70... value unchanged." **Anti-gaming discriminant PASS.** | ADDRESSED ✓ |
| 3 | L8: Level 0 zero-noise baseline; replace raw-magnitude severity matching with pre-registered standardized proximal-component effect (predefine component, perturbation, calibration set, tolerance); L8 locked bars preserved | §3.3 lines 188, 197–206: Level 0 zero-noise baseline as reference; standardized proximal-component severity matching with 4 predefinitions (component, perturbation type/magnitude, calibration set, tolerance) all pre-registered [LAW-L19]. L8 locked bars (§3.2) preserved. | ADDRESSED ✓ (see NB-1: inline tags stale) |
| 4 | Borderline B1 (label retained); 0.5α–α band descriptive only, must NOT change verdict; [LAW-L19] preserved | §7.5 lines 430–445: B1 confirmed (Rebecca); "The 0.5α–α band is descriptive only... must NOT change the verdict"; [LAW-L19] preserved. | ADDRESSED ✓ (see NB-2: §7.4 B1 tag stale) |
| 5 | L7 peer: matched-model + identical pre-registered confidence calibration, evaluation data, ECE definition, binning; paired independently trained instances; cite L7 line 24 + M0 line 20 | §2.3 lines 97–105: five parity conditions (identical confidence calibration, evaluation data, ECE definition, binning; paired independently trained instances) all tagged [BAR-Entry 11]; sources Constitution L7 line 24 [LAW-L7] + M0 line 20 [BAR-Entry 11]. | ADDRESSED ✓ |
| 6 | Graveyard-gate: implementation-only; scoring NOT authorized; L3/FWFP/impl-review/courier gates retained | §1.3 lines 50–54: "signed the graveyard gate for M4 implementation only... does NOT authorize scoring"; downstream gates retained (L3 Entry 72, FWFP Entry 43, CRITIC impl review, courier authorization). **Implementation-only discriminant PASS.** | ADDRESSED ✓ |
| 7 | Timebox 6 sessions / 14 days; tripwire 3 sessions / 7 days; excludes external-review and L3-gate waiting time | §9.2 line 515 + line 548: 6 sessions/14 days, tripwire 3/7, exclusions (external-review + L3-gate waiting), tagged [Rebecca-approved]. | ADDRESSED ✓ |
| 8 | L10 seeds: five confirmed (was [PROPOSED]); value 5 unchanged | §4.2 line 252: "5 (confirmed by Rebecca, matching L7/L8 5-seed policy) [BAR-Entry 11.3] (v1.6 Ruling 8)". Value unchanged. | ADDRESSED ✓ |
| 9 | Tolerance calibration: pre-registered, candidate-blind (101–105 NOT inputs; oracle/synthetic only), frozen-before-scoring; ARCHITECT specifies procedure (method/data source/acceptance criterion); TASK BUILDER computes under O-15; CRITIC verifies; Rebecca signs off on method/criterion not numbers; acceptance = each arm FP rate ≤ pre-specified threshold consistent with FWFP; existing failure routings preserved | §7.6 lines 447–468: "pre-registered, candidate-blind, oracle/synthetic-grounded, frozen-before-scoring"; "candidate's diagnostic-seed results (seeds 101–105 under O-15) are NOT inputs... Only oracle/synthetic ground-truth is used"; "Once computed and CRITIC-verified, the tolerances are locked and cannot be adjusted after the candidate runs. Any post-candidate adjustment is prohibited"; role boundary (ARCHITECT procedure / TASK BUILDER O-15 numbers / CRITIC verify / Rebecca method-criterion); existing failure routings preserved (line 468). **Candidate-blind + frozen discriminant PASS — no latitude for post-candidate adjustment.** | ADDRESSED ✓ |

### Ruling 2 — anti-gaming discriminant (critical)

The handoff required BLOCK if the headline AUROC can still be gamed by abstention. **PASS:** §4.3 line 259 defines the primary drifted AUROC as computed over the complete fixed drifted population using pre-abstention scores (the candidate's confidence/ranking before abstention is applied). Abstention does not remove a case from the primary AUROC. Answered-case AUROC is secondary/report-only (line 261) and cannot satisfy the floor. All-abstain fails the ≥0.70 floor, not N/A (line 263). The ≥0.70 floor value is preserved; only the population and anti-gaming design change (line 269). The abstention-exclusion gaming surface the CRITIC flagged in v1.5 is closed.

### Ruling 9 — candidate-blind + frozen discriminant (critical)

The handoff required BLOCK if the TASK BUILDER has latitude to adjust tolerances after candidate runs, or if candidate diagnostic seeds (101–105) are inputs. **PASS:** §7.6 line 455 explicitly states seeds 101–105 are NOT inputs — only oracle/synthetic ground-truth is used; "The candidate's behavior cannot influence its own control thresholds." Line 457: "Once computed and CRITIC-verified, the tolerances are locked and cannot be adjusted after the candidate runs. Any post-candidate adjustment is prohibited and would be visible in the provenance." Role boundary correct (ARCHITECT specifies procedure; TASK BUILDER computes numbers under O-15; CRITIC verifies; Rebecca signs off on method/criterion, not numbers). Existing failure-routing rules preserved (line 468). No latitude for post-candidate adjustment.

---

## Step 3 — Delta scope check

`git diff --stat 487843f b22609f`:

```
 handoffs/ARCHITECT_M4_SPEC_V1.6_HANDOFF.md |  63 +++++++++
 specs/m4_specification.md                  | 161 +++++++++++++++----------
 specs/m4_specification_changelog.md        |  54 ++++++++-
 3 files changed, 222 insertions(+), 56 deletions(-)
```

Single commit (`b22609f`). Changed files are exactly the three authorized: spec, changelog, architect handoff. **No file outside scope touched.**

Every spec change maps to one of the nine rulings or to required bookkeeping (header version/status/base-SHA bump; §9.1 step-1 deliverable; §12 decision-item table updated to mark items RESOLVED). No substantive change outside the nine rulings.

### Locked bar values — no change confirmed

| Locked bar | Value (v1.5) | Value (v1.6) | Changed? |
|---|---|---|---|
| L7 AUROC | ≥ 0.75 | ≥ 0.75 | No (split into per-seed threshold; value same) |
| L7 ECE | ≤ 0.10 | ≤ 0.10 | No |
| L7 margin | > 0 at p < .05 | > 0 (direction test, paired-bootstrap CI) | No (inferential method specified; value/bar same) |
| L8 doses | ≥ 3 | ≥ 3 | No |
| L8 Spearman ρ | ≥ 0.8 | ≥ 0.8 | No |
| L8 slope | ≥ 0.2 | ≥ 0.2 | No |
| L8 specificity | mandatory | mandatory | No (strengthened: standardized) |
| L8 seeds | 5 | 5 | No |
| L10 abstain drift | ≥ 50% | ≥ 50% | No |
| L10 abstain clean | ≤ 10% | ≤ 10% | No |
| L10 AUROC floor | ≥ 0.70 | ≥ 0.70 | No (population changed to pre-abstention/fixed; value same) |
| L14 effect size | d ≥ 0.5 | d ≥ 0.5 | No |
| L14 correlation | corr ≥ 0.3 @ 3 seeds | corr ≥ 0.3 @ 3 seeds | No |

### Kill conditions / scoring predicates / fences

- L7 kill conditions (§2.5): reframed per Option C (AUROC/ECE per-seed no-fallback; margin direction test). Bar values unchanged; Amendment 3 retracted per Rebecca's ruling. No kill condition weakened.
- L8 / L10 / L14 kill conditions: unchanged.
- L3 pre-scoring gate (Option A, Entry 72): preserved (§1.3, §8, §11). ✓
- M3 INSTRUMENT FAILURE: retained (§1.2). ✓
- Seeds 201–203 / 301–303: retained, never rerun [O-14] (§1.2, §11). ✓
- O-14 / O-15: preserved (§11; §7.6 TASK BUILDER under O-15). ✓
- L15/L16/L17 fence to M5: preserved (§10). ✓
- ≥2 unseen scoring seeds: preserved (§7.2). ✓

No locked bar lowered, raised, renamed, or silently replaced. No scoring predicate changed beyond what the nine rulings specify. O-14 honored — no scoring, no rerun, no hold-out exposure.

---

## Step 4 — Design-soundness observations (fresh-eyes)

### Internal consistency of the nine rulings

The nine rulings are internally consistent; no two create a tension or contradiction:
- R1 (paired-bootstrap margin) and R5 (paired independently trained instances) are mutually reinforcing — the paired-bootstrap CI for the margin operates on the paired candidate–peer seeds R5 defines.
- R2 (pre-abstention AUROC) and R9 (candidate-blind tolerance calibration) close two distinct score-chasing surfaces without overlap: R2 prevents gaming the headline metric via abstention; R9 prevents gaming the control thresholds via candidate behavior.
- R3's L8 severity-matching calibration set ("separate from scoring seeds") is consistent with R9's candidate-blind principle (calibration sets do not use candidate diagnostic seeds for control thresholds).

### Residual score-chasing path analysis (Step 4, item 15)

The CRITIC examined whether a residual score-chasing path remains:
- **Control-arm tolerances (R9):** fully closed — oracle/synthetic-grounded, candidate-blind, frozen. The candidate cannot influence its own falsification thresholds. ✓
- **τ calibration (R2):** τ is calibrated on held-out calibration data separate from scoring seeds. This is the candidate's own calibration parameter (standard train/calibrate/test split), tuned on development data — not a falsification threshold. Overfitting τ to dev data would hurt, not help, on fresh scoring seeds. No gaming surface. ✓
- **Pre-abstention AUROC (R2):** abstention cannot remove hard cases from the headline metric; the candidate is scored on all drifted cases via pre-abstention scores. No residual abstention-gaming path. ✓

The design correctly distinguishes candidate-calibrated parameters (τ, dev-grounded) from candidate-blind falsification thresholds (control tolerances, oracle-grounded). This is the right separation. No residual score-chasing path identified.

### Non-blocking design observations

None that block. The one substantive design concern raised in v1.5 (abstention-exclusion gaming surface) is now closed by Ruling 2.

---

## Blocking findings (require ARCHITECT correction, then re-clear)

These are P3/P4/P6 provenance/tag-state defects — the spec does not correctly memorialize the source authority for its own changes and carries contradictory approval states. They are governance defects, not scientific/design defects: no bar, kill condition, ruling substance, or authorization boundary is changed by the substantive review (all pass). They block because the next action on CLEAR is sending the spec to Rebecca for her signature, and the spec is not in a consistent approval state for that signature. Correctable by a narrow mechanical ARCHITECT pass that leaves spec substance and locked bars unchanged.

### BF-1 (was NB-1) — Stale `[PROPOSED — requires Rebecca sign-off]` inline tags on L8 items already approved (Ruling 3) — BLOCKING

§3.3 still tags the following as `[PROPOSED — requires Rebecca sign-off]` even though Ruling 3 (Entry 76) approved them and the §12 table (lines 555–556) marks them RESOLVED/Rebecca-approved:
- Line 188: Level 0 zero-noise baseline
- Line 202: perturbation type/magnitude (standardized proximal-component effect)
- Line 203: calibration set
- Line 204: tolerance

These inline tags contradict Ruling 3 and the §12 table. A TASK BUILDER or INTEGRATOR reading §3.3 in isolation could misread them as "not yet approved — do not implement," creating ambiguity about implementation authorization. **Corrective:** update the §3.3 inline tags to `[Rebecca-approved (Ruling 3)]` / `[RESOLVED — Ruling 3]` to match the §12 table and Entry 76.

### BF-2 (was NB-2) — Stale `[PROPOSED — requires Rebecca ruling]` tag on §7.4 Option B1 — BLOCKING

§7.4 line 422 still tags Option B1 as `[PROPOSED — requires Rebecca ruling]` even though Ruling 4 (Entry 76) confirmed B1 and §7.5 line 445 records "Rebecca confirmed B1." **Corrective:** update the §7.4 tag to reflect Ruling 4's confirmation.

### BF-3 (was NB-3) — Stale provenance statement in §0 + Entry 76 not cited — BLOCKING (primary blocker)

§0 (line 17) states "Provenance reviewed through Entry 72." This is stale: Entry 75 (v1.5 advisor cycle) and Entry 76 (Rebecca's nine rulings) now exist on main. The spec implements Entry 76's rulings but does not cite Entry 76 by number anywhere — it attributes the nine changes to "Per Rebecca's ruling." The rulings ARE verifiable against Entry 76 (P6 satisfied substantively), but the spec should cite Entry 76 explicitly and update the §0 statement to "reviewed through Entry 76." **Corrective:** cite Entry 76 as the source for the nine rulings; update §0 provenance statement to Entry 76.

### BF-4 (was NB-4) — Tolerance-value [PROPOSED] tags (acceptable, transparently addressed — non-blocking)

The [PROPOSED — requires Rebecca sign-off] tags on individual control-arm tolerance values in §2.4 (lines 114–119), §3.4, and §4.5 (line 288) are acceptable: §7.6 line 468 explicitly states these are "now governed by this procedure — the numbers will be computed by the TASK BUILDER under this procedure, not pre-specified by the ARCHITECT." This is transparent and consistent with Ruling 9 (Rebecca signs off on method/criterion, not numbers). No correction required, but the §2.4/§3.4/§4.5 tables could cross-reference §7.6 for clarity. Non-blocking.

---

## STOP / escalation triggers for Rebecca

None new. The nine rulings resolve all v1.5 STOP/escalation items:
- The v1.5 Finding 6 L7 inference STOP is **resolved** by Ruling 1 (Option C) — no longer a STOP.
- The v1.5 abstention-exclusion gaming observation is **resolved** by Ruling 2.
- All [PROPOSED] items the v1.5 review escalated are now ruled (Rulings 1–9) and recorded in Entry 76.

The graveyard-gate signature (Ruling 6) authorizes M4 implementation only; scoring remains gated on L3 resolution, FWFP closure audit, CRITIC implementation review, Rebecca's tolerance-calibration method/criterion sign-off (Ruling 9), and courier-channel authorization.

---

## Preserved evidence

All prior valid evidence preserved. No law text, locked bar, prior provenance entry, run label, or verdict touched. M3 INSTRUMENT FAILURE retained; seeds 201–203 / 301–303 never rerun. The CRITIC review is read-only with respect to the spec, constitution, scoring artifacts, and STATE.md.

---

## Prohibited-action confirmation

The CRITIC confirms:
- No modification of the spec, constitution, or any artifact (read-only + this review file only).
- No merge to main. Branch `critic/m4-v1.6-delta-review` created off `b22609f`; review file committed only.
- No scoring, seed execution, or hold-out seed exposure.
- No L15/L16/L17 work before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- No re-run-on-failure (O-14); development diagnostic-only (O-15) honored.

---

## Public-repository pre-push scan attestation

Before pushing branch `critic/m4-v1.6-delta-review`, the CRITIC self-scanned the committed review file (`reviews/critic_m4_v1.6_delta_review.md`) and the staged diff for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII.

**Scan result:** No prohibited content found. The review file contains only SHA hashes, branch names, line numbers, law/provenance text already public in the repository, and Entry 76 ruling text. No credentials, tokens, private absolute paths, hostnames, MAC addresses, SIDs, or PII present. **Classification: acceptable.** Attestation logged per `PUBLIC_REPOSITORY_POLICY.md` §3.

---

## Next authorized role

**Next recipient:** ARCHITECT — for a narrow mechanical correction of the blocking findings (BF-1, BF-2, BF-3) only. The ARCHITECT must NOT touch spec substance, locked bars, kill conditions, scoring predicates, or the nine rulings' implementations — only the stale provenance statement and stale approval-status tags.

**Required corrections (ARCHITECT, mechanical only):**
- **BF-3 (primary):** update §0 "Provenance reviewed through Entry 72" → "through Entry 76"; cite Entry 76 explicitly as the source authority for the nine rulings wherever the spec says "Per Rebecca's ruling."
- **BF-1:** update §3.3 stale `[PROPOSED — requires Rebecca sign-off]` inline tags on Level 0 (line 188), perturbation type/magnitude (line 202), calibration set (line 203), and tolerance (line 204) to reflect Ruling 3 approval (match the §12 table: `[Rebecca-approved (Ruling 3)]` / `[RESOLVED — Ruling 3]`).
- **BF-2:** update §7.4 Option B1 tag (line 422) from `[PROPOSED — requires Rebecca ruling]` to reflect Ruling 4's confirmation (match §7.5).
- Leave BF-4 as-is (acceptable).
- Do not change any locked bar value, kill condition, scoring predicate, or the nine rulings' substantive implementations.

After ARCHITECT correction, the spec returns to CRITIC for a fresh delta re-clear of the mechanical changes only, then (on CLEAR) to WORKFLOW COORDINATOR for Step 7 package assembly and routing to Rebecca for her graveyard-gate signature (Ruling 6 — implementation-only authorization).

**Explicitly prohibited for the next role and downstream:**
- No modification of any locked bar, threshold value, kill condition, or scoring predicate.
- No change to the nine rulings' substantive implementations — only the provenance statement and approval-status tags.
- No scoring run, no fresh-seed execution, until Rebecca authorizes via courier.
- No rerun of seeds 201–203 or 301–303 (O-14).
- No L15/L16/L17 or M5 component work before M5.
- No adjustment of tolerance numbers by the TASK BUILDER after candidate runs (Ruling 9 — frozen before scoring).
- No use of candidate diagnostic seeds (101–105) as inputs to tolerance calibration (Ruling 9 — candidate-blind).
- No merge to main except by Rebecca.

---

*Review committed at `reviews/critic_m4_v1.6_delta_review.md` on branch `critic/m4-v1.6-delta-review` (SHA recorded in handoff).*
