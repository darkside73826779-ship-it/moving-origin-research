# CRITIC Residual Re-Clear — M4 Spec v1.6 (ARCHITECT BF-1/BF-2/BF-3 correction)

**Gate served:** Fresh-context delta re-clear of the ARCHITECT's mechanical correction of the prior CRITIC BLOCK (BF-1/BF-2/BF-3)
**Reviewer:** CRITIC
**Date:** 2026-08-18 23:13 EDT
**Spec under review:** ARCHITECT-corrected M4 spec v1.6 ("BF-1 BF-2 BF-3 resolved"), supplied as attachment (not yet committed to a branch the CRITIC could verify a SHA for — the ARCHITECT should commit it and supply the SHA/branch)
**Delta base:** `b22609f` (v1.6, prior CRITIC BLOCK at `881195a` on `critic/m4-v1.6-delta-review`)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this review > agent judgment. CRITIC does not speak for Rebecca.

---

## Verdict: BLOCK (residual mechanical — tag-state/provenance)

**Block class:** provenance / tag-state defect (governance), not scientific/design. Same class as the prior BLOCK; the ARCHITECT resolved the three cited findings at their cited locations but left two residuals of the same class.

The substance remains clean and is preserved: BF-1, BF-2, BF-3 are resolved at their cited locations; the law-diff is byte-exact (the corrections did not touch any law quote); Ruling 2 anti-gaming and Ruling 9 candidate-blind/frozen remain PASS; no locked bar value, kill condition, scoring predicate, or ruling implementation was changed. The diff is 18 insertions / 16 deletions, all confined to provenance-statement and approval-status tag changes — no spec substance touched.

**Why BLOCK, not CLEAR:** the next action on CLEAR is sending the Step 7 package to Rebecca for her graveyard-gate signature. The §12 "Items requiring Rebecca's decision" table is the authoritative summary of what still needs Rebecca's sign-off. It currently tells Rebecca two contradictory approval states for the same L8 item: §12 line 558 marks "L8 severity-matched specificity" as RESOLVED (Ruling 3), while §12 line 561 lists the same four L8 predefinitions (comparison component, perturbation type, calibration set, tolerance) as `[PROPOSED — requires Rebecca sign-off]` — contradicting both §3.3 lines 203–206 (now `[Rebecca-approved (Ruling 3, Entry 76)]`) and §12 line 558. A spec that tells Rebecca she still must sign off on an item she already approved cannot go to her for signature. This is a residual mechanical correction, not a failure of the substantive correction.

---

## What is RESOLVED and preserved (do not re-litigate)

1. **BF-3 (resolved at cited location):** §0 line 17 now "Provenance reviewed through Entry 76 (Rebecca's nine Step 7 gate rulings)"; new §0 line 23 cites Entry 76 as the Step 7 source; `[Entry 76]` tag added to all nine ruling headers (§1.3, §2.3, §2.5, §3.3, §4.2, §4.3, §7.5, §7.6, §9.2). ✓
2. **BF-1 (resolved at cited location):** §3.3 lines 190, 203, 204, 205, 206 changed from `[PROPOSED — requires Rebecca sign-off]` to `[Rebecca-approved (Ruling 3, Entry 76)]`. ✓
3. **BF-2 (resolved at cited location):** §7.4 line 424 changed from `[PROPOSED — requires Rebecca ruling]` to `[Rebecca-confirmed B1 (Ruling 4, Entry 76)]`. ✓
4. **Law-diff:** still byte-exact (L7/L8/L10/L18 BYTE-EXACT; L14 trailing-whitespace-only). The corrections did not touch any law quote. ✓
5. **Ruling 2 anti-gaming / Ruling 9 candidate-blind+frozen:** unchanged, still PASS. ✓
6. **Locked bar values / kill conditions / scoring predicates / ruling implementations:** unchanged. ✓
7. **Delta scope of the correction:** 18 ins / 16 del, all tag/provenance-statement changes, no spec substance. ✓

---

## Residual blocking findings (ARCHITECT ultra-narrow mechanical correction)

### BF-A (residual) — Line 8 "Prior context" still says "Entry 72" — P4

Line 8 ("Prior context") still states "Provenance log reviewed through Entry 72." The ARCHITECT fixed §0 line 17 to "Entry 76" but missed the line 8 summary, so the spec now internally contradicts itself on provenance-review depth (line 8 says 72; line 17 says 76).

**Corrective (mechanical):** update line 8 "Provenance log reviewed through Entry 72" → "through Entry 76" (or remove the clause, since §0 line 17 is the authoritative statement). Do not change anything else in line 8.

### BF-B (residual, PRIMARY) — §12 line 561 contradicts §3.3 and §12 line 558 — P3

§12 line 561 (under "Items still requiring Rebecca sign-off (method/criterion, not numbers)") lists:
> "L8 standardized specificity: comparison component, perturbation type, calibration set, tolerance — pre-registered [PROPOSED — requires Rebecca sign-off] (Ruling 3)"

This contradicts:
- **§3.3 lines 203–206:** the same four predefinitions are now tagged `[Rebecca-approved (Ruling 3, Entry 76)]`.
- **§12 line 558:** "L8 severity-matched specificity | Standardized proximal-component effect (4 predefinitions) | [LAW-L19] — RESOLVED (Ruling 3)".

Entry 76 Ruling 3 APPROVED the standardized proximal-component approach with the four predefinitions. The specific pre-registered values are reviewed by CRITIC under the §3.3.1 homeostatic-variable prerequisite review (a CRITIC or Rebecca-delegated pass), not individually by Rebecca. So the four L8 predefinitions do NOT require a separate Rebecca ruling — they are approved (approach) and CRITIC-reviewed (specific values).

**Corrective (mechanical):** remove the "L8 standardized specificity" entry from the "Items still requiring Rebecca sign-off" list (§12 lines 560–562), OR rewrite it to state: the specific L8 predefinitions are pre-registered before any data exists and CRITIC-reviewed under §3.3.1, with no additional Rebecca ruling required unless escalated as a STOP per §5.2. The entry must not say `[PROPOSED — requires Rebecca sign-off]` for items Ruling 3 already approved.

**Do NOT touch the "Tolerance calibration: method and acceptance criterion — [PROPOSED — requires Rebecca sign-off] (Ruling 9)" entry (§12 line 562):** that is correct per Entry 76 Ruling 9 ("Rebecca signs off on the method and criterion, not the numbers"). Leave it.

---

## ARCHITECT scope of work (ultra-narrow, mechanical only)

1. **BF-A:** line 8 "Entry 72" → "Entry 76" (or remove the clause).
2. **BF-B:** §12 line 561 — remove the "L8 standardized specificity" entry from "Items still requiring Rebecca sign-off," or rewrite to reflect §3.3.1 CRITIC-review (no additional Rebecca ruling unless escalated). Leave the Ruling 9 tolerance-calibration entry (line 562) unchanged.

No other changes. Commit the corrected spec (supply branch + SHA), update the changelog to record the residual mechanical correction, and route back to CRITIC for re-clear.

---

## Explicitly prohibited

- No change to spec substance, locked bars, kill conditions, scoring predicates, law quotes, or ruling implementations — only the line 8 provenance clause and the §12 line 561 entry.
- No modification of the constitution, M0 Decision Sheet, provenance log, STATE.md, scoring artifacts, or prior reviews.
- No merge to main. Branch-level only. Rebecca alone merges.
- No scoring, seed execution, or hold-out seed exposure.
- No rerun of seeds 201–203 or 301–303 (O-14).
- No L15/L16/L17 before M5.
- No renaming/reinterpreting negatives or INSTRUMENT FAILURE.
- No resolution by ARCHITECT interpretation where the constitution/log is silent — STOP and escalate per §5.2 (this correction is mechanical and should not require interpretation).

---

## Prohibited-action confirmation (CRITIC)

No modification of the spec, constitution, or any artifact (read-only + this review file only); no merge to main; no scoring/seed execution/hold-out exposure; no L15/L16/L17 before M5; no renaming/reinterpreting negatives or INSTRUMENT FAILURE; O-14/O-15 honored.

---

## Public-repository pre-push scan attestation

Before pushing this review, the CRITIC self-scanned `reviews/critic_m4_v1.6_residual_reclear.md` for credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII.

**Scan result:** No prohibited content found. The review contains only SHA hashes, branch names, line numbers, and spec/provenance text already public in the repository. No credentials, tokens, private absolute paths, hostnames, MAC addresses, SIDs, or PII present. **Classification: acceptable.** Attestation logged per `PUBLIC_REPOSITORY_POLICY.md` §3.

---

## Next authorized role

**Next recipient:** ARCHITECT — ultra-narrow mechanical correction of BF-A (line 8) and BF-B (§12 line 561) only. Commit the corrected spec (supply branch + SHA), update changelog, route back to CRITIC for re-clear. On CLEAR: to WORKFLOW COORDINATOR for Step 7 package assembly and routing to Rebecca for her graveyard-gate signature (Ruling 6 — implementation-only authorization).
