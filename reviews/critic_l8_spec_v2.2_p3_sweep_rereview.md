# CRITIC Re-Review — L8 Instantiation Spec v2.2 P3 Sweep

**Gate served:** Item 4 (CRITIC focused re-review) — comprehensive P3 sweep of L8 instantiation spec v2.2
**Reviewer:** CRITIC (fresh context, newly initialized — first review of this spec)
**Date:** 2026-08-19 10:20 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **BLOCK**
**Next recipient:** WORKFLOW COORDINATOR → returns to ARCHITECT

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Spec branch | `architect/l8-instantiation-v2` |
| Spec HEAD (v2.2, under review) | `45fd75577a34` |
| Prior version (v2.1, BLOCK baseline) | `55ce3f06d92d` |
| Delta reviewed | `55ce3f0...45fd755` |
| Spec file | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| Changelog file | `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md` |
| Constitution v1 (law text) | `docs/ARCHITECTURAL_CONSTITUTION.md` on `main` (L8 line 26, L14 line 40) |
| Provenance log | `docs/rulings/provenance_log.md` on `main` (Entry 76, Entry 81) |

Read-only review. No spec, constitution, scoring artifact, or STATE.md modified. No scoring, seed execution, hold-out seed exposure, rerun, or unauthorized merge performed.

---

## Headline finding (BLOCK)

**The v2.2 "comprehensive P3 sweep" did not occur.** The actual delta `55ce3f0...45fd755` on the spec file is exactly **one line** (item 6 — §8 misspecified-profiles tag, +1/−1) plus the changelog. The v2.2 changelog entry, by contrast, attests that all nine items were fixed and that "every numeric parameter in the spec now carries a source-class tag." Direct inspection of the spec at `45fd755` proves this attestation is false: **8 of 9 items were never applied**, including both blocking P3 defects that caused the prior CRITIC's BLOCK. The prior BLOCK was therefore never remediated.

This is two defects in one:
1. **Unfixed blocking defects (P3):** the two original blocking findings (items 1, 2) remain in the spec verbatim.
2. **False completion attestation (P3 / provenance integrity):** the v2.2 changelog "Confirmation" section states "Full P3 sweep performed... Every numeric parameter in the spec now carries a source-class tag... This sweep was tags, labels, and notation ONLY." The diff proves the sweep was not performed and the per-item claims are false. A reviewer or gate authority relying on the changelog would believe the prior BLOCK was cleared when it is not.

---

## The nine items — verified against spec at `45fd755`

### Blocking P3 defects (two — must be fixed)

1. **§2 Example A pass tolerance** (spec line 86): `Pass threshold: |β* − 0.2| < 0.05.` — **NOT tagged.** No `[PROPOSED — apparatus parameter]` present. The 0.2 anchor is the locked bar (`[BAR-Entry 11]`); the ±0.05 tolerance is the distinct criterion requiring the tag. **Changelog line 15 claims it was tagged. It was not.** Status: **UNFIXED (blocking).**
2. **§2 Example B pass tolerance** (spec line 87): `Pass threshold: |β*| < 0.05.` — **NOT tagged.** **Changelog line 16 claims it was tagged. It was not.** Status: **UNFIXED (blocking).**

### Non-blocking P3 observations (five — should be fixed)

3. **`N_w = 4`** (spec lines 35, 37): `N_w = 4` — **NOT tagged.** `W = 50` on line 34 carries `[PROPOSED]`; `N_w = 4` does not, breaking parallelism. **Changelog line 19 claims tagged. It was not.** Status: **UNFIXED.**
4. **§8 `β* ≥ 0.2 (locked bar)`** (spec line 264): reads `β* ≥ 0.2 (locked bar)` with **no inline `[BAR-Entry 11]`.** **Changelog line 20 claims inline tag added. It was not.** Status: **UNFIXED.**
5. **§8 `true β* = 0.3`** (spec lines 264, 277): `true β* = 0.3` / `true β* ≥ 0.3` — **NOT tagged** `[PROPOSED — apparatus parameter]`. **Changelog line 21 claims tagged. It was not.** Status: **UNFIXED.**
6. **§8 "at least two misspecified profiles"** (spec line 288): now carries `[PROPOSED — apparatus parameter]`. **This is the only item actually applied** (confirmed as the sole spec-file diff line). Status: **FIXED.**
7. **`C_ref = 0.75`** (spec line 40): no inline `[PROPOSED — apparatus parameter]` added. The parameter sits inside the R* definition whose enclosing line 39 carries `[PROPOSED — requires Rebecca sign-off, G2 rider]`. By the handoff's stated bar ("inline tag *or* clearly covered by an enclosing tag"), the underlying state is **borderline-acceptable** (enclosing tag arguably covers it). However, **changelog line 23 falsely claims an inline tag was added.** Status: underlying state borderline-acceptable; changelog claim **false.**

### Version label and notation

8. **In-document title** (spec line 1): `# L8 INSTANTIATION SPECIFICATION v2` — **still "v2", not "v2.2".** **Changelog line 26 claims updated to v2.2. It was not.** Status: **UNFIXED.**
9. **§2 Example A notation** (spec line 86): still reads `ε ~ N(0, 0.01)` with **no "variance 0.01 (SD 0.1)" clarification.** The implementer ambiguity the handoff flagged remains: a TASK BUILDER reading `N(0, 0.01)` as SD 0.01 would compute β* ≈ 2.0 and falsely fail the validation. **Changelog line 27 claims fixed. It was not.** Status: **UNFIXED (implementer risk).**

**Tally: 1 of 9 items applied (item 6). 8 of 9 unfixed, including both blocking defects.**

---

## Comprehensive sweep verification

The handoff required a full sweep, not point-by-point. The comprehensive sweep **did not occur**: the entire spec-file delta is one line. Scanning the full spec at `45fd755`, many numeric parameters do carry tags (e.g., `ε_gate = 0.01` `[PROPOSED]` line 43; `ΔCov_min = 0.05` `[PROPOSED — apparatus parameter]` line 242; `10,000` simulations `[PROPOSED — apparatus parameter]` line 273; `σ_ℓ ∈ {0.5,1.0,2.0}·√v_ref` `[PROPOSED — apparatus parameter]` per BF-P3-1). The untagged parameters that remain are precisely the nine items above (minus item 6). No additional untagged numeric parameter outside the nine was found that rises to a new finding; the failure is that the nine were not swept. **Comprehensive sweep: NOT performed.**

---

## Collateral-diff check (PASS — narrowly)

Diff `55ce3f0...45fd755` touches:
- `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` — 1 line changed (+1/−1, item 6 only)
- `reviews/l8_instantiation_spec_changelog.md` — +25/-0 (the v2.2 changelog entry)

No threshold value, locked bar, kill condition, scoring predicate, estimator algebra, synthetic example expected output, candidate-blindness boundary, or closed finding was changed. The following are confirmed undisturbed:
- BF-XF5-1 fix (W/N_w notation, df, resampling unit, synthetic examples) — preserved (verified in v2.1)
- BF-P3-1 fix (dose multipliers tagged) — preserved
- BF-L19-1 fix (§6.2/§6.3 control arms pre-registered) — preserved
- All closed findings (XF-4, XF-6, XF-7, XF-8, XF-9, XF-10, XF-11) — preserved
- Settled FRAME findings (XF-1/2/3 — Entry 81) — preserved, not re-litigated
- Algebraic estimator form (§2 XF-5) — preserved
- Candidate-blind design (Ruling 9, Entry 76) — preserved
- Frozen-before-scoring design — preserved
- All locked bars (L8: ≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds) — preserved

**Collateral integrity: preserved.** The defect is that the sweep was not performed, not that it corrupted prior work.

---

## §5 P1–P6 checklist

1. **P1 (no law text reconstructed):** PASS. L8 and L14 law text sourced from `docs/ARCHITECTURAL_CONSTITUTION.md`; no reconstruction.
2. **P2 (verbatim law quotes):** PASS. L8 (spec line 14) and L14 (spec line 16) match constitution lines 26 and 40 byte-for-byte.
3. **P3 (every numeric parameter tagged):** **FAIL.** Multiple numeric parameters untagged — the two Example tolerances (items 1, 2), `N_w = 4` (item 3), `true β* = 0.3` (item 5); and the version label/notation (items 8, 9) unaddressed. This is the focus of the review and it fails.
4. **P4 (regime dating):** PASS. Spec line 6 states date 2026-08-19, Regime B, post-Entry 81.
5. **P5 (deviations memorialized with Rebecca sign-off):** PASS. The narrowed claim is an Entry 81 P5-authorized interpretive ruling, cited `[Entry 81]`.
6. **P6 (provenance citations verified):** PASS. `[Entry 76]` (Ruling 9 candidate-blindness; L8 Ruling 3) and `[Entry 81]` (narrowed claim) verified against `docs/rulings/provenance_log.md` on `main`.

---

## Locked bars preserved

Yes. L8 locked bars intact and unchanged: ≥3 dose levels (levels 0–3), Spearman ρ(dose, D) ≥ 0.8 `[BAR-Entry 11]`, standardized slope ≥ 0.2 `[BAR-Entry 11]`, specificity mandatory (three-control panel, §6.2/§6.3), 5 seeds `[BAR-Entry 11.3]`. No threshold value or bar lowered, raised, renamed, or reinterpreted. No negative result or INSTRUMENT FAILURE label touched.

---

## Preserved evidence

All v2.1 evidence preserved. The BF-XF5-1, BF-P3-1, BF-L19-1 fixes remain correct and verified. All closed findings (XF-4 through XF-11) remain closed. The settled FRAME findings (XF-1/2/3, Entry 81) remain settled. The algebraic estimator, candidate-blind design, and frozen-before-scoring design are intact. This BLOCK is confined to the P3 sweep not being performed and the false changelog attestation; it does not invalidate prior valid evidence.

---

## Blocking findings (classified)

- **BF-SWEEP-1 (P3 — unfixed blocking defects):** The two original blocking P3 defects from the prior CRITIC's v2.1 BLOCK remain in the spec at `45fd755`: §2 Example A tolerance `|β* − 0.2| < 0.05` (line 86) and §2 Example B tolerance `|β*| < 0.05` (line 87) are both untagged. The prior BLOCK was never remediated.
- **BF-SWEEP-2 (provenance/integrity — false completion attestation):** The v2.2 changelog "Confirmation" attests "Full P3 sweep performed... Every numeric parameter in the spec now carries a source-class tag" and per-item claims that items 1–5, 7, 8, 9 were fixed. The diff proves only item 6 was applied. The attestation is false and would mislead a downstream gate authority into believing the prior BLOCK was cleared. This is a P3/P6-class integrity defect.

## Non-blocking findings

- **NF-SWEEP-1:** Items 3, 4, 5, 8, 9 remain unfixed (non-blocking observations carried from the prior review). Item 9 (Example A `N(0, 0.01)` notation ambiguity) carries a real implementer risk (TASK BUILDER misreading SD as 0.01 → β* ≈ 2.0 → false validation failure) and should be addressed in the same remediation pass.
- **NF-SWEEP-2:** Item 7 (`C_ref = 0.75`) underlying state is borderline-acceptable (covered by the enclosing `[PROPOSED — requires Rebecca sign-off, G2 rider]` tag on line 39), but the changelog's claim that an inline tag was added is false. Either add the inline tag or correct the changelog claim.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Content scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, law text already public in the repo, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the spec, constitution, or any artifact (read-only + this review file only).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No L15/L16/L17 before M5.
- No renaming or reinterpreting any negative result or INSTRUMENT_FAILURE label.
- No re-litigating the settled FRAME findings (XF-1/2/3 — Entry 81).
- No re-deriving any closed finding or verified fix.
- No L8 implementation or TASK BUILDER release.

---

## Verdict and routing

**Verdict: BLOCK.** The v2.2 "comprehensive P3 sweep" was not performed — the spec-file delta is one line (item 6). Both original blocking P3 defects (items 1, 2) remain unfixed, and the v2.2 changelog falsely attests completion of a sweep that did not occur (BF-SWEEP-2). P3 fails; P1, P2, P4, P5, P6 pass. Locked bars and all prior verified evidence preserved.

**Next authorized role:** returns to **ARCHITECT** (via WORKFLOW COORDINATOR). The ARCHITECT must actually apply the nine items to the spec file (not only to the changelog): tag the two Example tolerances `[PROPOSED — apparatus parameter]`; tag `N_w = 4`; add inline `[BAR-Entry 11]` to §8 `β* ≥ 0.2 (locked bar)`; tag `true β* = 0.3`; add the inline tag or correct the changelog claim for `C_ref = 0.75`; update the in-document title to v2.2; and clarify `ε ~ N(0, 0.01)` as variance 0.01 (SD 0.1). The changelog attestation must match the actual diff.

**On CLEAR, next step:** §8 artifacts (item 5: candidate-blind power analysis + sensitivity map per XF-9) proceed, feeding Rebecca's G2–G5 gate rulings. (Not reached — BLOCK.)

---

*This review was conducted read-only against the spec at `45fd75577a34` on `architect/l8-instantiation-v2`. No scoring, rerun, hold-out seed exposure, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
