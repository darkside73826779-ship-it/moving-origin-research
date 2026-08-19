# CRITIC Delta Re-Clear — M4 Specification v1.5

**Gate served:** Fresh-context law-fidelity + design-soundness review of spec v1.5 (advisor correction cycle)
**Reviewer:** CRITIC (freshly initialized — first review of this spec)
**Date:** 2026-08-18 · **Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Spec under review:** `architect/m4-spec-v1.5` at **`487843f`**
**Delta base:** `9dff1e5` (v1.4.1, prior CRITIC-cleared)
**Review surface:** `9dff1e5...487843f` — `specs/m4_specification.md` (+104/−25), `specs/m4_specification_changelog.md` (+42/−1), `handoffs/ARCHITECT_M4_SPEC_V1.5_HANDOFF.md` (+64)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this review > agent judgment. CRITIC does not speak for Rebecca.

---

## Verdict: CLEAR

No blocking findings. All six advisor findings are addressed with correct source tags; all quoted law text is byte-exact against the constitution; every new/changed threshold carries a P3 source tag; every provenance citation verifies against the log (P6); the delta is confined to the six findings + changelog + return handoff; no locked bar value, kill condition, or scoring predicate was changed beyond what the six findings require; the L7 inference tension (Finding 6) is correctly escalated as a STOP for Rebecca rather than resolved by reconstruction. Next role (WORKFLOW COORDINATOR) authorized to assemble the Step 7 gate package for Rebecca's ruling.

---

## Step 1 — Law-diff (§5.2 mandatory, completed before substantive review)

Method: a script extracted every blockquote law quote in `specs/m4_specification.md` (lines beginning `> **Lx —`) and compared the quoted body byte-for-byte against the canonical law line in `docs/ARCHITECTURAL_CONSTITUTION.md` on `main`.

| Law | Spec quote location | Constitution line | Result | Notes |
|---|---|---|---|---|
| L7 | §2.1, spec line 60 | line 24 | BYTE-EXACT | — |
| L8 | §3.1, spec line 136 | line 26 | BYTE-EXACT | — |
| L10 | §4.1, spec line 221 | line 30 | BYTE-EXACT | — |
| L14 | §5.1, spec line 285 | line 40 | EXACT-after-rstrip | Constitution line 40 carries one trailing whitespace char omitted in the spec quote. Substantive text identical. Non-blocking. |
| L18 | §6.1, spec line 325 | line 52 | BYTE-EXACT | — |

All five verbatim law quotations required by the handoff (L7, L8, L10, L14, L18 minimum) are byte-exact (L14 differs only by a single trailing space on the constitution side). P2 (verbatim quotation) satisfied. All line citations correct.

### P3 — source-class tags on thresholds

Every new or changed numeric threshold in the v1.5 delta carries a source tag. Verified:
- L10 calibration target (≥50% abstention under drift): `[BAR-Entry 11.6]` ✓
- L10 drifted-AUROC floor (≥0.70): `[BAR-Entry 14]` (preserved, not relinked to τ) ✓
- L8 zero-noise Level 0 reference: `[PROPOSED — requires Rebecca sign-off]` ✓
- L8 severity-matched specificity: `[LAW-L8]` + `[PROPOSED]` ✓; pre-registration `[LAW-L19]` ✓
- Borderline margin (p ∈ [α_corr×0.5, α_corr]): `[PROPOSED — requires Rebecca sign-off]` ✓
- FWFP milestone-wide ≤5%: `[BAR-Entry 43]` ✓
- L8 ≥3 doses tag refined `[OP-Entry 11.7]` → `[BAR-Entry 11]` (value unchanged; reconciliation documented in §3.2) ✓

No untagged new thresholds. P3 satisfied.

### P6 — provenance citation verification

Verified each cited entry against `docs/rulings/provenance_log.md` actual text:

| Citation | Spec claim | Verified against log |
|---|---|---|
| Entry 5 | "JUDGE's measurability assessment... classified L7 as 'fully numeric'" | Entry 5 at line 87: "Fully numeric (judgeable now): L7 (AUROC ≥ 0.75, ECE ≤ 0.10, margin > 0 at p < .05)..." ✓ |
| Entry 8 | "JUDGE's ruling on the plan... did not lock bars" | Entry 8 at line 134: "Applied pre-registered criteria only — no bars invented, lowered, reinterpreted, or raised." ✓ |
| Entry 11 | "Bars were locked by Rebecca in Entry 11" | Entry 11 at line 172: "Rebecca adopted 'the attached M0_DECISION_SHEET' as her pre-registration, in full" ✓ |
| Entry 11.3 | 5 seeds + all-seeds-direction + bootstrap-CI fallback | Entry 11.3: "Seeds raised to 5 for L7, L8, L15, with the all-seeds-direction + bootstrap-CI fallback." LOCKED ✓ |
| Entry 11.4 | L14 d ≥ 0.5 | Entry 11.4: "L14 effect-size floor raised to d ≥ 0.5." LOCKED ✓ |
| Entry 11.6 | L10 50%/10% abstention | Entry 11.6: "L10 abstention dual bar: 50% under drift / 10% clean." LOCKED ✓ |
| Entry 11.7 | §9 operationalizations (V4.4, ≥3 doses) | Entry 11.7: "All nine §9 operationalizations ADOPTED." ✓ |
| Entry 11.8 | L7 graveyard gate deferred | Entry 11.8: "L7... gates DEFERRED to their milestones" ✓ |
| Entry 14 | drifted-AUROC ≥0.70 floor; corr ≥0.3 watch W5 | Entry 14 cross-cutting (4) names "drifted-AUROC ≥ 0.70 floor"; watch item 5 names "L14 corr ≥ 0.3 at 3 seeds." ✓ (Entry 14 assesses/references; canonical locking is Entry 11 — see non-blocking note) |
| Entry 43 | FWFP closure standing rule, ≤5%, four-part test | Entry 43: "every scoring spec's closure audit must compute FWFP of each arm's full check battery and correct any control whose FWFP exceeds 5% BEFORE scoring." ✓ (verbatim) |
| Entry 52 | M3 INSTRUMENT FAILURE, provisional advancement | Entry 52: "INSTRUMENT FAILURE retained. Candidate-facing evidence sufficient for provisional advancement to M4." ✓ |
| Entry 70 | M0_DECISION_SHEET published; L8 bars [BAR-Entry 11] | Entry 70: "L8 bars confirmed: From the published sheet — ≥3 noise doses [BAR-Entry 11]..." ✓ |
| Entry 72 | Option A — M4 scoring gated on L3 resolution | Entry 72: "Rebecca chose OPTION A... M4 scoring is gated on prospective L3 calibration resolution on fresh seeds." ✓ |

Spec line-number citations for Entries 5/8/11 (lines 87/134/172) are correct. P6 satisfied.

---

## Step 2 — Finding-by-finding verification

| # | Finding | Required disposition | Evidence in v1.5 | Result |
|---|---|---|---|---|
| 1 | L7 peer baseline must match M0 line 20 + Constitution "matched model," quoted verbatim | §2.3 revised | §2.3 (spec lines 80–93): OLS fixed baseline superseded by matched-model peer; Constitution L7 quoted verbatim ("a peer-observer baseline (a matched model predicting this system from its outputs)" [LAW-L7, line 24]); M0 line 20 quoted verbatim ("Peer spec: same params/data/architecture, observation channel = behavioral outputs only, self-report channel excluded" [BAR-Entry 11]). Both quotes verified byte-exact against sources. | ADDRESSED ✓ |
| 2 | FWFP closure must cover milestone-wide family of ALL control-triggering tests; preserve [BAR-Entry 43], ≤5%, TASK BUILDER (O-15) | §7.3 extended | §7.3 (lines 380–386): milestone-wide family enumerated across L7/L8/L10/L14/L18 control arms; milestone-wide FWFP ≤5% [BAR-Entry 43] added as acceptance criterion alongside per-arm ≤5%; owner remains TASK BUILDER under O-15. Per-arm rule + ≤5% preserved. | ADDRESSED ✓ |
| 3 | Replace τ=0.70↔AUROC linkage with explicit definitions; preserve ≥0.70 floor [BAR-Entry 14] | §4.3 rewritten | §4.3 (lines 235–247): confidence definition (scalar [0,1] from self-model), threshold calibration method (held-out calibration set, τ chosen to produce ≥50% abstention under drift [BAR-Entry 11.6]), abstained-case treatment (excluded from AUROC; all-abstain → N/A not 1.0), AUROC population (non-abstained drifted cases across seeds). Drifted-AUROC floor ≥0.70 [BAR-Entry 14] explicitly preserved as locked; v1.4 τ=0.70 rationale withdrawn as unsupported. Floor value NOT changed. | ADDRESSED ✓ |
| 4 | L8 zero-noise baseline + severity-matched non-self-model specificity; preserve L8 locked bars [BAR-Entry 11] | §3.3 augmented | §3.3 (lines 177, 186–188): Level 0 zero-noise baseline as dose-response reference [PROPOSED]; severity-matched specificity leg (non-self-model perturbation magnitude = self-model dose magnitude at each level) [LAW-L8][PROPOSED]; severity-matching procedure pre-registered [LAW-L19]. L8 locked bars (≥3 doses, ρ≥0.8, slope≥0.2, specificity, 5 seeds) [BAR-Entry 11] preserved in §3.2. | ADDRESSED ✓ |
| 5 | Numerical definition of "borderline"; B1 drafted but tagged [PROPOSED — requires Rebecca ruling]; [LAW-L19] preserved | §7.5 added | §7.5 (lines 406–421): numerical definition p ∈ [α_corrected × 0.5, α_corrected]; margin pre-registered [LAW-L19][PROPOSED]; B1 drafted (label retained, M3/Entry 43 precedent) tagged [PROPOSED — requires Rebecca ruling]; advisor recommends B1 but "Rebecca rules the borderline handling." Authority correctly reserved to Rebecca. | ADDRESSED ✓ |
| 6 | Reconcile any-seed KILL vs 5-seed/bootstrap fallback vs M0 line 29; if interpretation required, flag STOP/escalation for Rebecca | §2.5 rewritten | §2.5 (lines 110–124): tension explicitly stated; resolving requires "substantive interpretation of which L7 bars are 'threshold bars' (any-seed KILL) vs 'direction tests' (5-seed/bootstrap fallback)" — declared "not resolvable from verbatim law text alone." Per §5.2 this is a STOP; ARCHITECT flags the gap and escalates rather than resolving by reconstruction. Explicit "Escalation question for Rebecca" posed. Conservative default (per-seed any-seed KILL) applied pending ruling — preserves candidate's burden without resolving the interpretive question. | ADDRESSED ✓ (STOP, not reconstruction) |

### Finding 6 discriminant (critical)

The handoff required: if substantive interpretation is needed to determine which L7 bars are "threshold" vs "direction," verify it is flagged as a STOP/escalation for Rebecca rather than resolved by reconstruction. If the ARCHITECT made a substantive interpretation, BLOCK.

**Finding:** The ARCHITECT did NOT resolve the tension by interpretation. §2.5 explicitly states the resolution "is not resolvable from verbatim law text alone" and escalates per §5.2, posing a precise question for Rebecca. The conservative per-seed default is a temporary placeholder that preserves (strictifies) the candidate's burden, not a determination of which bars are threshold vs direction. The v1.4 "Amendment 3" hard rule (threshold bars get no fallback) — itself an interpretation — is correctly retracted in favor of escalation. This is the correct §5.2 disposition. **Not a P1/P5 violation. Does not block.**

---

## Step 3 — Delta scope check

`git diff --stat 9dff1e5 487843f`:

```
 handoffs/ARCHITECT_M4_SPEC_V1.5_HANDOFF.md |  64 +++++++++++
 specs/m4_specification.md                  | 104 ++++++++-------
 specs/m4_specification_changelog.md        |  42 ++++-
 3 files changed, 185 insertions(+), 25 deletions(-)
```

Single commit (`487843f`). Changed files are exactly the three authorized: the spec, its changelog, and the ARCHITECT return handoff. **No file outside scope touched.**

Hunk-by-hunk: every spec change maps to one of the six findings or to required bookkeeping (header version/status/base-SHA bump, §9.1 step-1 deliverable version, §12 decision-item additions for the newly proposed items). No substantive change outside the six findings.

### Locked bar values — no change confirmed

| Locked bar | Value (v1.4.1) | Value (v1.5) | Changed? |
|---|---|---|---|
| L7 AUROC | ≥ 0.75 | ≥ 0.75 | No |
| L7 ECE | ≤ 0.10 | ≤ 0.10 | No |
| L7 margin | > 0 at p < .05 | > 0 at p < .05 | No |
| L8 doses | ≥ 3 | ≥ 3 | No (tag refined OP→BAR; value same) |
| L8 Spearman ρ | ≥ 0.8 | ≥ 0.8 | No |
| L8 slope | ≥ 0.2 | ≥ 0.2 | No |
| L8 specificity | mandatory | mandatory | No (strengthened: severity-matched) |
| L8 seeds | 5 | 5 | No |
| L10 abstain drift | ≥ 50% | ≥ 50% | No |
| L10 abstain clean | ≤ 10% | ≤ 10% | No |
| L10 AUROC floor | ≥ 0.70 | ≥ 0.70 | No (delinked from τ; value same) |
| L14 effect size | d ≥ 0.5 | d ≥ 0.5 | No |
| L14 correlation | corr ≥ 0.3 @ 3 seeds | corr ≥ 0.3 @ 3 seeds | No |

### Kill conditions / scoring predicates / fences

- L7 kill conditions: reframed as conservative-default-pending-Rebecca (Finding 6 escalation); bar values unchanged. No kill condition weakened — the interim default is stricter than the M0 fallback would be.
- L8 kill conditions (§3.5): unchanged.
- L10 kill conditions (§4.6): unchanged.
- L14 kill conditions (§5.4): unchanged.
- L3 pre-scoring gate (Option A, Entry 72): preserved in §8 and §11. ✓
- M3 INSTRUMENT FAILURE label: retained (§1.2). ✓
- Seeds 201–203 / 301–303: retained, never rerun [O-14] (§1.2, §11). ✓
- O-14 / O-15: preserved (§11). ✓
- L15/L16/L17 fence to M5: preserved (§10). ✓
- ≥2 unseen scoring seeds: preserved (§7.2). ✓

No locked bar lowered, raised, renamed, or silently replaced. No scoring predicate changed beyond what the six findings require. O-14 (no rerun-on-failure) honored — the CRITIC conducted no scoring, no rerun, no hold-out exposure.

---

## Step 4 — Design-soundness observations (fresh-eyes)

Beyond fidelity, the following scientific/design observations are noted. None rise to blocking because each is either pre-registered, Rebecca-gated, or correctly conservative.

1. **L7 matched-model peer (Finding 1) — sound.** A peer with identical params/data/architecture seeing only behavioral outputs is the correct falsification of the mirror claim: if privileged self-state access doesn't beat an identical architecture reading only outputs, the moving origin earns nothing. Alignment with M0 line 20 and the Constitution's "matched model" is correct. The peer's confidence method is [PROPOSED — Rebecca sign-off], appropriately deferred.

2. **FWFP milestone-wide (Finding 2) — sound.** Per-arm FWFP ≤5% does not bound the family across all controls; the milestone-wide audit closes this. Requiring both per-arm and milestone-wide ≤5% is conservative and correct. TASK BUILDER ownership under O-15 preserved.

3. **L10 abstention-exclusion from AUROC + ≥50% drift-abstention bar — potential gaming surface (NON-BLOCKING, Rebecca-gated).** Excluding abstained cases from AUROC means a candidate could abstain on the hardest drifted cases and compute AUROC over the easier remainder, inflating the metric while still meeting ≥50% abstention under drift. The drifted-AUROC ≥0.70 floor partially backstops this (the non-abstained remainder must still clear 0.70), and Entry 14 already flagged "the abstention trigger is an exploitable surface." Because §4.3 is tagged [PROPOSED — requires Rebecca sign-off], this is properly escalated, not a CRITIC block. **Recommend Rebecca consider, when ruling on §4.3, whether the AUROC floor should be evaluated over a fixed evaluation set (with abstentions scored as failures or imputed) rather than a self-selected non-abstained subset.** Flagged for Rebecca's attention; does not block this gate.

4. **L8 zero-noise baseline + severity-matched specificity (Finding 4) — sound.** A Level 0 reference is necessary to define "rise," and severity-matching the non-self-model perturbation to the self-model dose at each level is the correct control: without it, the specificity leg could fail trivially (more noise → more error) rather than because the stakes are self-model-specific. Pre-registration of the severity-matching procedure [LAW-L19] is correct.

5. **Borderline numerical definition (Finding 5) — sound.** p ∈ [α_corr×0.5, α_corr] is a reasonable, pre-registered, mechanically-applied margin. B1 (label retained, Entry 43 precedent) is correctly drafted with Rebecca ruling the handling — authority not usurped by the ARCHITECT.

6. **L7 inference escalation (Finding 6) — correct disposition.** The conservative default (per-seed any-seed KILL) preserves the candidate's burden pending Rebecca's ruling; the interpretive question is not prejudged.

No design gap, confound, or falsifiability weakness that would block progression. The one substantive concern (observation 3) is already Rebecca-gated and pre-registered.

---

## STOP / escalation triggers for Rebecca

The spec itself escalates the following to Rebecca (CRITIC concurs these are correctly Rebecca-ruled, not ARCHITECT-resolved):

- **L7 inference policy (Finding 6, §2.5):** does the M0 5-seed/bootstrap fallback apply to all L7 bars, or do AUROC/ECE function as per-seed threshold bars with only the margin test using fallback? **STOP per §5.2.** Rebecca must rule before the conservative default can be relaxed.
- **L10 confidence/threshold definitions (§4.3):** confidence definition, calibration method, abstained-case AUROC treatment, AUROC population — all [PROPOSED — requires Rebecca sign-off]. CRITIC draws Rebecca's attention to observation 3 (abstention-exclusion gaming surface) when ruling here.
- **L8 zero-noise baseline + severity-matched specificity (§3.3):** [PROPOSED — requires Rebecca sign-off].
- **Borderline numerical definition + B1 handling (§7.5):** [PROPOSED — requires Rebecca ruling].
- **L7 peer confidence method (§2.3):** [PROPOSED — requires Rebecca sign-off].
- **L7 graveyard-gate sign-off [BAR-Entry 11.8]:** Rebecca must sign with M3 results before M4 implementation.

None of these require CRITIC to block; all are properly pre-registered and Rebecca-gated.

---

## Preserved evidence

All prior valid evidence preserved. No law text, locked bar, prior provenance entry, run label, or verdict touched. M3 INSTRUMENT FAILURE retained. Seeds 201–203 / 301–303 never rerun. The CRITIC review is read-only with respect to the spec, constitution, scoring artifacts, and STATE.md.

---

## Prohibited-action confirmation

The CRITIC confirms:
- No modification of the spec, constitution, or any artifact (read-only + this review file only).
- No merge to main. Branch `critic/m4-v1.5-delta-review` created off `487843f`; review file committed only.
- No scoring, seed execution, or hold-out seed exposure.
- No L15/L16/L17 work before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- No re-run-on-failure (O-14); development diagnostic-only (O-15) honored.

---

## Public-repository pre-push scan attestation

Before pushing branch `critic/m4-v1.5-delta-review`, the CRITIC self-scanned the committed review file (`reviews/critic_m4_v1.5_delta_review.md`) and the staged diff for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII.

**Scan result:** No prohibited content found. The review file contains only SHA hashes, branch names, line numbers, and law/provenance text already public in the repository. No credentials, tokens, private absolute paths, hostnames, MAC addresses, SIDs, or PII present. **Classification: acceptable.** Attestation logged per `PUBLIC_REPOSITORY_POLICY.md` §3.

---

## Next authorized role

**Next recipient:** WORKFLOW COORDINATOR. On CLEAR, assemble the revised Step 7 gate package (spec v1.5 + changelog + this review + the six-finding advisor closure) and route to Rebecca for her rulings on the [PROPOSED] items, the L7 inference STOP (Finding 6), the L7 graveyard-gate sign-off, and the M4 timebox.

**Explicitly prohibited for the next role and downstream:**
- No modification of any locked bar, threshold, or scoring predicate.
- No scoring run, no fresh-seed execution, until Rebecca authorizes via courier.
- No rerun of seeds 201–203 or 301–303 (O-14).
- No L15/L16/L17 or M5 component work before M5.
- No resolution of the Finding 6 L7 inference question by ARCHITECT interpretation — it is a STOP for Rebecca.
- No merge to main except by Rebecca.

---

*Review committed at `reviews/critic_m4_v1.5_delta_review.md` on branch `critic/m4-v1.5-delta-review` (SHA recorded in handoff).*
