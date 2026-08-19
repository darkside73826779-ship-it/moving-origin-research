# CRITIC Re-Review — L8 Instantiation Spec v2.2 (Fresh ARCHITECT Sweep)

**Gate served:** Item 4 (CRITIC focused re-review) — comprehensive P3 sweep by a fresh ARCHITECT session
**Reviewer:** CRITIC (fresh-context, newly initialized)
**Date:** 2026-08-19 11:15 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — §8 artifacts (item 5: candidate-blind power analysis + sensitivity map per XF-9) proceed, feeding Rebecca's G2–G5 gate rulings.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Spec branch (fresh ARCHITECT) | `architect/l8-instantiation-v2.2-fresh` |
| Spec HEAD (under review) | `c7d7bed6b259` |
| Base (v2.1, CRITIC-cleared baseline) | `55ce3f06d92d` on `architect/l8-instantiation-v2` |
| Delta reviewed | `55ce3f0...c7d7bed` |
| Spec file | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| Changelog file | `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md` |
| Prior CRITIC review (false-attestation BLOCK) | `reviews/critic_l8_spec_v2.2_p3_sweep_rereview.md` on `critic/l8-spec-v2.2-p3-sweep-rereview` (`80f9497`) — used as itemized defect list |
| Constitution v1 (law text) | `docs/ARCHITECTURAL_CONSTITUTION.md` on `main` (L8 line 26, L14 line 40) |
| Provenance log | `docs/rulings/provenance_log.md` on `main` (Entry 76, Entry 81) |

Read-only review. No spec, constitution, scoring artifact, or STATE.md modified. No scoring, seed execution, hold-out seed exposure, rerun, or unauthorized merge performed.

---

## Headline finding (CLEAR)

The fresh ARCHITECT's sweep is genuine and complete. The delta `55ce3f0...c7d7bed` on the spec file is 24 lines (11 additions, 13 deletions) — all tag, label, or notation — plus a 45-line changelog entry. **All nine items from the prior CRITIC's false-attestation BLOCK are now fixed**, including both blocking P3 defects. The changelog attestation matches the actual diff (unlike the prior ARCHITECT's false attestation). The prior false-attestation branch (`45fd755` on `architect/l8-instantiation-v2`) was correctly preserved as evidence and not built upon — the fresh sweep is rebased on the v2.1 CRITIC-cleared baseline `55ce3f0`.

---

## The nine items — verified against spec at `c7d7bed`

### Blocking P3 defects (two — must be fixed)

1. **§2 Example A pass tolerance** (spec line 86): Now reads `Pass threshold: |β* − 0.2| < 0.05 (0.2 anchor: [BAR-Entry 11]; ±0.05 tolerance: [PROPOSED — apparatus parameter]).` **FIXED.** The 0.2 locked-bar anchor is tagged `[BAR-Entry 11]`; the ±0.05 tolerance is tagged `[PROPOSED — apparatus parameter]`. ✓
2. **§2 Example B pass tolerance** (spec line 87): Now reads `Pass threshold: |β*| < 0.05 [PROPOSED — apparatus parameter].` **FIXED.** ✓

### Non-blocking P3 observations (five — should be fixed)

3. **`N_w = 4`** (spec lines 35, 37): Now tagged `[PROPOSED]` in both locations, parallel with `W = 50` `[PROPOSED]`. **FIXED.** ✓
4. **§8 `β* ≥ 0.2 (locked bar)`** (spec line 264): Now carries inline `[BAR-Entry 11]`. **FIXED.** ✓
5. **§8 `true β* = 0.3` / `true β* ≥ 0.3`** (spec lines 264, 277): Both now carry `[PROPOSED — apparatus parameter]`. **FIXED.** ✓
6. **§8 "at least two misspecified profiles"** (spec line 288): Now carries `[PROPOSED — apparatus parameter]`. **FIXED** (retained from prior; reads as a protocol criterion). ✓
7. **`C_ref = 0.75`** (spec line 40): No inline tag added; sits inside the R* definition whose enclosing line 39 carries `[PROPOSED — requires Rebecca sign-off, G2 rider]`, which clearly covers `C_ref = 0.75` and `m = 0.05`. Per the handoff's stated bar ("inline tag **or** clearly covered by an enclosing tag"), this is **acceptable**. The changelog transparently states no inline tag was added and explains the enclosing-tag coverage — correcting the prior false attestation, which had claimed an inline tag was added when none was. **Acceptable (covered by enclosing tag); changelog accurate.** ✓

### Version label and notation

8. **In-document title** (spec line 1): Now reads `v2.2`; status field (line 5) `DRAFT v2.2`; narrative version references in §8 (line 258), §10 (line 312), and §12 (line 330) all updated `spec v2` → `spec v2.2`. **FIXED.** ✓
9. **§2 Example A notation** (spec line 86): Now reads `ε ~ N(0, 0.01) (variance 0.01; SD 0.1 — N(μ, σ²) convention)`. The same clarification was applied to Example B (line 87) for consistency. Expected outputs unchanged: `β* ≈ 0.02 / 0.1 = 0.2` (Example A) and `β* ≈ 0.0` (Example B). The implementer ambiguity is resolved — a TASK BUILDER can no longer misread `N(0, 0.01)` as SD 0.01 (which would compute β* ≈ 2.0 and falsely fail the validation). **FIXED.** ✓

**Tally: 9 of 9 items addressed. Both blocking defects fixed.**

---

## Comprehensive sweep verification (PASS)

The handoff required a full sweep, not point-by-point. A full numeric-token scan of the spec at `c7d7bed` was performed. Every numeric parameter now carries a source-class tag (inline or via a clearly-covering enclosing tag):

- §2: `W = 50` `[PROPOSED]`, `N_w = 4` `[PROPOSED]`, `R*`/`C_ref = 0.75`/`m = 0.05` (enclosing `[PROPOSED — requires Rebecca sign-off, G2 rider]`), `ε_gate = 0.01` `[PROPOSED]`, `ρ ≥ 0.8` `[BAR-Entry 11]`, `slope ≥ 0.2` `[BAR-Entry 11]`, Example tolerances `[PROPOSED — apparatus parameter]` / `[BAR-Entry 11]`.
- §5: `σ_ℓ ∈ {0.5,1.0,2.0}·√v_ref` `[PROPOSED — apparatus parameter]`, `ε_c = 1e-6` `[PROPOSED]`, `ΔECE_min = 0.01` `[PROPOSED]`, `δ_mono = 0.005` `[PROPOSED]`.
- §6: matching tolerance ±0.25 `[PROPOSED]`, potency ≥ 0.5 `[PROPOSED]`, feedback-corruption rates {0.1, 0.2, 0.4} `[PROPOSED]`, `|τ_drift| ≥ 0.02` `[PROPOSED]`, chain multipliers 1.5×/2×/3× `[PROPOSED]`, oracle drop ≥ 0.05 `[PROPOSED]`, 5 seeds `[BAR-Entry 11.3]`, 5,000 resamples / 95% CI `[PROPOSED]`, 4/5 seeds `[PROPOSED]`.
- §7: `ΔCov_min = 0.05` `[PROPOSED]`, 5 seeds `[BAR-Entry 11.3]`.
- §8: `β* ≥ 0.2` `[BAR-Entry 11]`, `true β* = 0.3` `[PROPOSED — apparatus parameter]`, false-kill 0.10 `[PROPOSED]`, 10,000 sims `[PROPOSED]`, parameter grid `[PROPOSED]`, misspecified profiles `[PROPOSED]`.

Untagged numeric tokens that remain are: (a) restatements of already-tagged parameters, (b) derived arithmetic (degrees of freedom `N_w − 1 = 3`, `L × (N_w − 1) = 12`, `N_w × L = 16`; `Var(x) = 1.25` for {0,1,2,3}), or (c) synthetic-data coefficients within the validation examples (`0.02 × ℓ`) whose expected outputs are unchanged and whose tolerances are now tagged. These do not require source-class tags. **No additional untagged numeric parameter outside the nine was found. Comprehensive sweep confirmed.**

---

## Changelog attestation verification (PASS — true attestation)

The v2.2 changelog entry accurately matches the actual diff:

- Correctly states the base is `55ce3f0` (v2.1, CRITIC-cleared) and explicitly disclaims building on `45fd755` (the prior false-attestation branch, preserved as evidence). Provenance hygiene correct.
- Per-item claims (items 1–9) all match the diff, including line numbers.
- Item 7 is accurately described: "no inline tag added; enclosing tag clearly covers C_ref = 0.75 and m = 0.05" — this corrects the prior false attestation. Matches the diff.
- "Confirmation" section claims scope was tags/labels/notation only and no threshold value, locked bar, estimator algebra, synthetic-example expected output, closed finding, or verified fix changed. The diff confirms this.
- Includes a pre-push scan attestation (clean).

Unlike the prior ARCHITECT's false attestation (changelog claimed 9/9 fixed; diff showed 1/9), this changelog's claims are all borne out by the diff. **Attestation is true.**

---

## Collateral-diff check (PASS)

Delta `55ce3f0...c7d7bed` touches only:
- `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` — 24 lines (tags/labels/notation only)
- `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md` — +45/-0

No threshold value, locked bar, kill condition, scoring predicate, estimator algebra, synthetic-example expected output, candidate-blindness boundary, closed finding, or verified fix changed. Confirmed undisturbed:
- BF-XF5-1 fix (W/N_w notation, df, resampling unit, synthetic examples) — preserved
- BF-P3-1 fix (dose multipliers tagged) — preserved
- BF-L19-1 fix (§6.2/§6.3 control arms pre-registered) — preserved
- All closed findings (XF-4, XF-6, XF-7, XF-8, XF-9, XF-10, XF-11) — preserved
- Settled FRAME findings (XF-1/2/3 — Entry 81) — preserved, not re-litigated
- Algebraic estimator form (§2 XF-5) — preserved (expected outputs β* ≈ 0.2 / 0.0 unchanged)
- Candidate-blind design (Ruling 9, Entry 76) — preserved
- Frozen-before-scoring design — preserved

Law text (L8 line 14, L14 line 16) confirmed untouched by the sweep (no diff lines touch the law quotes).

---

## §5 P1–P6 checklist

1. **P1 (no law text reconstructed):** PASS. L8/L14 law text sourced from the constitution file; no reconstruction.
2. **P2 (verbatim law quotes byte-for-byte):** PASS. L8 (spec line 14) and L14 (spec line 16) match constitution lines 26 and 40 byte-for-byte; the sweep did not touch the law-quote lines.
3. **P3 (every numeric parameter tagged):** PASS. Every numeric parameter now carries a source-class tag (inline or via a clearly-covering enclosing tag). The two blocking defects and all non-blocking observations are resolved.
4. **P4 (regime dating):** PASS. Spec line 6 states date 2026-08-19, Regime B, post-Entry 81.
5. **P5 (deviations memorialized with Rebecca sign-off):** PASS. The narrowed claim is an Entry 81 P5-authorized interpretive ruling, cited `[Entry 81]`.
6. **P6 (provenance citations verified):** PASS. `[Entry 76]` (Ruling 9 candidate-blindness; L8 Ruling 3) and `[Entry 81]` (narrowed claim) verified against `docs/rulings/provenance_log.md` on `main`.

---

## Locked bars preserved

Yes. L8 locked bars intact and unchanged: ≥3 dose levels (levels 0–3), Spearman ρ(dose, D) ≥ 0.8 `[BAR-Entry 11]`, standardized slope ≥ 0.2 `[BAR-Entry 11]`, specificity mandatory (three-control panel, §6.2/§6.3), 5 seeds `[BAR-Entry 11.3]`. No threshold value or bar lowered, raised, renamed, reinterpreted, or silently replaced. No negative result or INSTRUMENT_FAILURE label touched.

---

## Preserved evidence

All prior evidence preserved. The prior false-attestation branch (`45fd755`) is preserved as evidence on `architect/l8-instantiation-v2` and correctly not built upon. BF-XF5-1, BF-P3-1, BF-L19-1 remain correct. All closed findings (XF-4–XF-11) remain closed. The settled FRAME findings (XF-1/2/3, Entry 81) remain settled. The algebraic estimator, candidate-blind design, and frozen-before-scoring design are intact.

---

## Non-blocking findings

None blocking. One observation for the record (not a defect):

- **NF-FRESH-1 (record):** Item 7 (`C_ref = 0.75` and `m = 0.05`) is resolved by enclosing-tag coverage rather than an inline tag. This satisfies the handoff's stated bar and is consistent with P3's allowance for clearly-covering enclosing tags. If a future reviewer prefers explicit inline tags on every numeric token for maximal implementer clarity, that is a stylistic enhancement, not a compliance requirement. No action required for this gate.

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

**Verdict: CLEAR.** The fresh ARCHITECT's comprehensive P3 sweep was genuinely performed — 9 of 9 items fixed (including both blocking defects), the changelog attestation matches the actual diff, no collateral disturbance, P1–P6 all pass, locked bars and all prior verified evidence preserved. The prior false-attestation BLOCK is resolved.

**Next authorized role:** WORKFLOW COORDINATOR. On CLEAR, §8 artifacts (item 5: candidate-blind power analysis + sensitivity map per XF-9 protocol) proceed, feeding Rebecca's G2–G5 gate rulings (G1 already resolved by Entry 81). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

---

*This review was conducted read-only against the spec at `c7d7bed6b259` on `architect/l8-instantiation-v2.2-fresh`. No scoring, rerun, hold-out seed exposure, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
