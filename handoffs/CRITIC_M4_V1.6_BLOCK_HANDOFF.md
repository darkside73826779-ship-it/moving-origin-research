# CRITIC Handoff — Route to ARCHITECT: M4 Spec v1.6 BLOCK (provenance/tag-state correction)

**Gate served:** CRITIC fresh-context delta re-clear of M4 spec v1.6 (Rebecca's nine Step 7 gate rulings) — BLOCK returned for narrow mechanical correction
**Issued by:** CRITIC
**Date:** 2026-08-18 23:10 EDT
**Next recipient:** ARCHITECT
**Prior recipient:** WORKFLOW COORDINATOR (handed spec v1.6 to CRITIC for fresh-context review)

---

## Authorization

CRITIC (fresh-context reviewer per §5.2) reviewed M4 spec v1.6 at `b22609f` (delta base `487843f` = v1.5, prior CRITIC CLEAR `91c790a`). Rebecca's nine Step 7 gate rulings are recorded in provenance Entry 76 (logged 23:02 EDT). The substance of v1.6 verifies — all nine rulings implemented correctly, law-diff byte-exact, the two hard discriminants (Ruling 2 anti-gaming; Ruling 9 candidate-blind/frozen) both PASS, no locked bar value changed. The BLOCK is a governance/provenance/tag-state defect, not a scientific/design defect: the spec does not correctly memorialize the source authority for its own changes and carries contradictory approval states. It is correctable by a narrow mechanical ARCHITECT pass that leaves spec substance, locked bars, kill conditions, scoring predicates, and the nine rulings' implementations untouched.

**Authority chain:** Rebecca > constitution's laws > approved specifications > this handoff > ARCHITECT judgment. The ARCHITECT does not speak for Rebecca. Rebecca alone rules gates and merges.

---

## Verdict: BLOCK

**Block class:** provenance / tag-state defect (P3/P4/P6), governance — not scientific/design.

The spec is returned to ARCHITECT for mechanical correction of three blocking findings (BF-1, BF-2, BF-3). After correction, the spec returns to CRITIC for a fresh delta re-clear of the mechanical changes only.

---

## SHAs and sources

| Item | Location | Status |
|---|---|---|
| Spec v1.6 (under review) | `architect/m4-spec-v1.6` at **`b22609f`** | BLOCKED — returned to ARCHITECT |
| Delta base (prior CRITIC CLEAR) | `487843f` (v1.5) | CRITIC-cleared (`91c790a`) |
| CRITIC review (this BLOCK) | `reviews/critic_m4_v1.6_delta_review.md` on `critic/m4-v1.6-delta-review` at **`881195a`** | Committed + pushed |
| Constitution v1 | `docs/ARCHITECTURAL_CONSTITUTION.md` on main | Sole source for verbatim law text |
| M0 Decision Sheet | `docs/rulings/M0_DECISION_SHEET.md` on main | Pre-registration bars (line 20 L7 peer; line 29 inferential policy; line 21 L8) |
| Provenance log | `docs/rulings/provenance_log.md` on main | Through Entry 76 (Rebecca's nine rulings) |

---

## What PASSES (preserved evidence — do not re-litigate)

The following were verified PASS and are preserved. The ARCHITECT correction must not alter any of these:

1. **Law-diff (P2):** all five verbatim law quotations byte-exact against `docs/ARCHITECTURAL_CONSTITUTION.md` — L7 (spec:62↔con:24), L8 (spec:147↔con:26), L10 (spec:241↔con:30), L18 (spec:349↔con:52) BYTE-EXACT; L14 (spec:309↔con:40) EXACT-after-rstrip (one trailing space on the constitution side). All line citations correct.
2. **Nine rulings implemented correctly (P6 — verified against Entry 76):** R1 L7 Option C (Amendment 3 retracted, not silently restored); R2 L10 anti-gaming (primary AUROC over complete fixed drifted population using pre-abstention scores; answered-case AUROC secondary; all-abstain fails the ≥0.70 floor, not N/A; floor value preserved); R3 L8 zero-noise Level 0 + standardized proximal-component severity matching; R4 borderline B1 (0.5α–α band descriptive only, must not change verdict); R5 L7 peer 5 parity conditions (identical confidence calibration / evaluation data / ECE definition / binning; paired independently trained instances); R6 graveyard-gate implementation-only (scoring NOT authorized; downstream gates retained); R7 timebox 6 sessions/14 days tripwire 3/7; R8 L10 5 seeds confirmed; R9 tolerance calibration candidate-blind (seeds 101–105 NOT inputs; oracle/synthetic only) + frozen-before-scoring (no post-candidate adjustment).
3. **Ruling 2 anti-gaming discriminant — PASS:** the abstention-exclusion gaming surface flagged in v1.5 is closed. The headline AUROC cannot be gamed by abstention.
4. **Ruling 9 candidate-blind + frozen discriminant — PASS:** no latitude for the TASK BUILDER to adjust tolerances after candidate runs; candidate diagnostic seeds 101–105 are not inputs.
5. **Locked bar values unchanged:** L7 0.75/0.10/margin; L8 ≥3 doses/ρ≥0.8/slope≥0.2/specificity/5 seeds; L10 50%/10%/0.70 floor; L14 d≥0.5/corr≥0.3. The L10 0.70 floor value is preserved — only the population it is computed over changes (pre-abstention, complete fixed population).
6. **Delta scope:** 3 files, single commit (spec +107/−54, changelog +52/−2, handoff +63). No file outside scope.
7. **Fences preserved:** L3 pre-scoring gate (Option A, Entry 72); O-14/O-15; M3 INSTRUMENT FAILURE; seed custody (201–203 / 301–303 never rerun); L15–L17 fence to M5; ≥2 unseen scoring seeds.
8. **Design soundness:** nine rulings internally consistent; no residual score-chasing path.

---

## Blocking findings (ARCHITECT must correct all three)

### BF-3 (PRIMARY BLOCKER) — Stale provenance statement in §0 + Entry 76 not cited — P4/P6

§0 (spec line 17) states "Provenance reviewed through Entry 72." This is stale: Entry 75 (v1.5 advisor cycle) and Entry 76 (Rebecca's nine rulings) now exist on main, and v1.6 implements Entry 76's rulings. The spec implements the nine rulings but does not cite Entry 76 by number anywhere — it attributes the nine changes to "Per Rebecca's ruling" without a verifiable citation anchor. The rulings ARE verifiable against Entry 76 (P6 substantively satisfied), but the spec artifact itself does not correctly memorialize the source authority for its own changes.

**Why it blocks:** the next action on CLEAR is assembly of the formal Step 7 gate package for Rebecca's graveyard-gate signature. A spec that does not cite its own source authority (Entry 76) and carries a stale provenance statement ("through Entry 72") cannot be sent to Rebecca for signature. In this project provenance citations are governance controls, not cosmetic.

**Corrective (mechanical):**
- Update §0 "Provenance reviewed through Entry 72" → "Provenance reviewed through Entry 76."
- Cite Entry 76 explicitly as the source authority for the nine rulings wherever the spec says "Per Rebecca's ruling" / "Per Rebecca's ruling, L7 bars are split..." / "Per Rebecca's ruling, the following parity conditions..." etc. Use a source tag such as `[Entry 76 — Principal ruling: Step 7 gate]` on each of the nine ruling implementations (§2.3 R5, §2.5 R1, §3.3 R3, §4.3 R2, §7.5 R4, §1.3 R6, §9.2 R7, §4.2 R8, §7.6 R9), and reference Entry 76 in §0.
- Do not alter any ruling substance — only add the citation.

### BF-1 — Stale `[PROPOSED — requires Rebecca sign-off]` inline tags on L8 items already approved (Ruling 3) — P3

§3.3 still tags the following as `[PROPOSED — requires Rebecca sign-off]` even though Ruling 3 (Entry 76) approved them and the §12 decision-items table (lines 555–556) marks them RESOLVED/Rebecca-approved:
- Line 188: Level 0 zero-noise baseline
- Line 202: perturbation type/magnitude (standardized proximal-component effect)
- Line 203: calibration set
- Line 204: tolerance

These inline tags contradict Ruling 3 and the §12 table. A TASK BUILDER or INTEGRATOR reading §3.3 in isolation could misread them as "not yet approved — do not implement," creating ambiguity about implementation authorization — which directly conflicts with Ruling 6's implementation-only graveyard-gate signature.

**Corrective (mechanical):** update the §3.3 inline tags on lines 188, 202, 203, 204 from `[PROPOSED — requires Rebecca sign-off]` to `[Rebecca-approved (Ruling 3, Entry 76)]` / `[RESOLVED — Ruling 3]`, consistent with the §12 table. Do not change the substantive design (Level 0 baseline, standardized proximal-component severity matching, 4 predefinitions) — only the approval-status tag.

### BF-2 — Stale `[PROPOSED — requires Rebecca ruling]` tag on §7.4 Option B1 — P3

§7.4 (line 422) still tags Option B1 as `[PROPOSED — requires Rebecca ruling]` even though Ruling 4 (Entry 76) confirmed B1 and §7.5 (line 445) records "Rebecca confirmed B1." This is a contradictory approval state inside the spec.

**Corrective (mechanical):** update the §7.4 tag (line 422) to reflect Ruling 4's confirmation, consistent with §7.5 (e.g., `[Rebecca-confirmed B1 (Ruling 4, Entry 76)]`). Do not change the B1 substance — only the approval-status tag.

---

## Non-blocking finding (no correction required, noted for awareness)

### BF-4 — Tolerance-value `[PROPOSED]` tags (acceptable, transparently addressed)

The `[PROPOSED — requires Rebecca sign-off]` tags on individual control-arm tolerance values in §2.4 (lines 114–119), §3.4, and §4.5 (line 288) are acceptable: §7.6 (line 468) explicitly states these are "now governed by this procedure — the numbers will be computed by the TASK BUILDER under this procedure, not pre-specified by the ARCHITECT." This is transparent and consistent with Ruling 9 (Rebecca signs off on method/criterion, not numbers). No correction required. Optional: cross-reference §7.6 from the §2.4/§3.4/§4.5 tolerance tables for clarity. Non-blocking.

---

## ARCHITECT scope of work (narrow, mechanical only)

The ARCHITECT is authorized to make ONLY the following changes to `specs/m4_specification.md`:

1. **BF-3:** §0 provenance statement "Entry 72" → "Entry 76"; cite Entry 76 as source for the nine rulings (add `[Entry 76]` source tags on each ruling implementation + reference in §0).
2. **BF-1:** §3.3 lines 188, 202, 203, 204 — update stale `[PROPOSED — requires Rebecca sign-off]` tags to `[Rebecca-approved (Ruling 3, Entry 76)]` / `[RESOLVED — Ruling 3]`.
3. **BF-2:** §7.4 line 422 — update stale `[PROPOSED — requires Rebecca ruling]` to `[Rebecca-confirmed B1 (Ruling 4, Entry 76)]`.

No other changes. Produce v1.6.1 (or equivalent minor version) on `architect/m4-spec-v1.6` (or a successor branch), update the changelog to record the mechanical correction, and produce an ARCHITECT return handoff. Then route back to CRITIC for a fresh delta re-clear of the mechanical changes only.

---

## Explicitly prohibited

- **No change to spec substance** — the nine rulings' implementations, the L8 design (Level 0, standardized proximal-component severity matching, 4 predefinitions), the B1 handling, the L10 pre-abstention AUROC design, the tolerance-calibration procedure (§7.6), or any operational design. Only the provenance statement and approval-status tags change.
- **No change to any locked bar value, threshold value, kill condition, or scoring predicate.**
- **No change to the law-diff** (the five verbatim law quotations must remain byte-exact).
- **No modification of the constitution, M0 Decision Sheet, provenance log, STATE.md, scoring artifacts, or any prior review.**
- **No merge to main.** Branch-level work only. Rebecca alone merges to main.
- **No scoring, seed execution, or hold-out seed exposure.**
- **No rerun of seeds 201–203 or 301–303 (O-14).**
- **No L15/L16/L17 or M5 component work before M5.**
- **No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.**
- **No resolution of any item by ARCHITECT interpretation where the constitution/log is silent** — if a correction requires substantive interpretation, STOP and escalate to Rebecca per §5.2 (this correction is mechanical and should not require interpretation).

---

## Prohibited-action confirmation (CRITIC)

The CRITIC confirms that during this review:
- No modification of the spec, constitution, or any artifact occurred (read-only + the CRITIC review file and this handoff only).
- No merge to main occurred.
- No scoring, seed execution, or hold-out seed exposure occurred.
- No L15/L16/L17 work before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- O-14 (no re-run-on-failure) and O-15 (development diagnostic-only) were honored.
- A pre-push self-scan was performed on the CRITIC review file; no prohibited content (credentials, tokens, private absolute paths, hostnames, MAC addresses, SIDs, PII) was found. Attestation logged per `PUBLIC_REPOSITORY_POLICY.md` §3.

---

## Public-repository pre-push scan attestation (for this handoff)

Before pushing this handoff, the CRITIC self-scanned `handoffs/CRITIC_M4_V1.6_BLOCK_HANDOFF.md` for credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII.

**Scan result:** No prohibited content found. The handoff contains only SHA hashes, branch names, line numbers, spec/provenance text already public in the repository, and Entry 76 ruling references. No credentials, tokens, private absolute paths, hostnames, MAC addresses, SIDs, or PII present. **Classification: acceptable.** Attestation logged per `PUBLIC_REPOSITORY_POLICY.md` §3.

---

## Next authorized role

**Next recipient:** ARCHITECT — narrow mechanical correction of BF-1, BF-2, BF-3 only (§0 provenance statement → Entry 76 + cite Entry 76; update stale `[PROPOSED]` tags on Ruling 3 L8 items and Ruling 4 B1 to reflect approval). Produce v1.6.1 + changelog entry + return handoff.

After ARCHITECT correction: **returns to CRITIC** for a fresh delta re-clear of the mechanical changes only. On CLEAR: to WORKFLOW COORDINATOR for Step 7 package assembly and routing to Rebecca for her graveyard-gate signature (Ruling 6 — implementation-only authorization; scoring remains gated on L3 resolution, FWFP closure audit, CRITIC implementation review, Rebecca's tolerance-calibration method/criterion sign-off, and courier-channel authorization).
