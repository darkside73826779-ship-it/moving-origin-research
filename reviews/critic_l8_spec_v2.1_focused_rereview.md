# CRITIC — Fresh-Context Focused Re-Review: L8 Instantiation Spec v2.1

**Role:** CRITIC (independent adversarial review; falsify, verify, block; never co-authors the work under review)
**Review type:** Fresh-context focused re-review of the v2 → v2.1 remediation (BF-XF5-1, BF-P3-1, BF-L19-1)
**Date:** 2026-08-19 · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 Versioned-Law Compliance Protocol binding) (P4)
**Gate served:** §12 sequencing step 1 — fresh-context CRITIC review of the L8 instantiation spec, input = this spec + the eight-document chain; scope = verify closure of XF-4–XF-9 and the CF riders, not to re-litigate the settled FRAME findings XF-1/2/3 (resolved by Entry 81).

**Spec under review:**
- Repository: `darkside73826779-ship-it/moving-origin-research`
- Branch: `architect/l8-instantiation-v2`
- HEAD SHA: `55ce3f06d92dc7f5b5a8f9aee7e6ccd9273cc88e` (v2.1)
- File: `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md`
- Prior v2 baseline: `06f388eff3c4` on the same branch
- Delta reviewed: `06f388e...55ce3f0`

**Sources consulted (read-only):** constitution v1 (`docs/ARCHITECTURAL_CONSTITUTION.md`, main) and v2 (`docs/ARCHITECTURAL_CONSTITUTION_v2.md`, main); provenance log (`docs/rulings/provenance_log.md`, main); M0 decision sheet (`docs/rulings/M0_DECISION_SHEET.md`, main); Sol cross-family review (`reviews/l8_crossfamily_review/SOL_CROSSFAMILY_L8_REVIEW.md`, main); prior CRITIC reviews 03/05; public-repository policy (`PUBLIC_REPOSITORY_POLICY.md`, main). No scoring seeds, hold-out seeds, or candidate outputs were present in any reviewed material.

---

## Verdict

**BLOCK.**

The three targeted v2 → v2.1 remediations (BF-XF5-1, BF-P3-1, BF-L19-1) are each verified correctly implemented. The residual BLOCK is narrowly scoped: the §5-P3 universal source-class tag audit — which is explicitly in this review's scope — finds untagged numeric test criteria in §2 (the synthetic-validation pass tolerances) that the three targeted fixes did not cover. Under §5-P3 ("A number without a tag is a review-blocking defect"), these block. The fix is a tag addition; no law text, locked bar, estimator algebra, synthetic example, candidate-blindness boundary, or closed finding is implicated.

---

## §5 P1–P6 checklist

### P1 — Repo-first law (no reconstruction)

All law text quoted in the spec was found verbatim in the committed constitution files; no constitutional text was reconstructed. ✓

### P2 — Verbatim law quotation (law-diff)

- **L8** (spec §1 quote) vs constitution v1 line 26: **verbatim match, byte-for-byte.** ✓
- **L14** (spec §1 quote) vs constitution v1 line 40: **verbatim match, byte-for-byte.** ✓
- **L19** (referenced via `[LAW-L19]` tags) vs constitution v1 line 53 / v2 §4: L19 reads "Pre-registration. Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings." L19 mandates **pre-registration only** — it does not set any numeric value. ✓

### P3 — Source-class tags (universal audit)

The four permitted classes are `[LAW-Lx]`, `[BAR-Entry n]`, `[OP-Entry n]`, `[PROPOSED]`. A threshold/kill condition/test criterion without one is a blocking defect. Audit of the committed spec:

**Tagged correctly (representative):** `W = 50` `[PROPOSED]` (line 34); `ε_gate = 0.01` `[PROPOSED]` (line 43); Spearman ρ ≥ 0.8 and standardized slope ≥ 0.2 `[BAR-Entry 11]` (line 44); `ΔECE_min = 0.01` and `δ_mono = 0.005` `[PROPOSED — apparatus parameter]` (§5); §6.1 memory potency and matching tolerance `[PROPOSED]`; §6 XF-6 bootstrap 5,000 resamples / 95% CI `[PROPOSED — apparatus parameter]` and 5 seeds `[BAR-Entry 11.3]`; §7 `ΔCov_min = 0.05` `[PROPOSED — apparatus parameter]`; §8 false-kill 0.10 `[PROPOSED]` and 10,000 simulations `[PROPOSED — apparatus parameter]`.

**BF-P3-1 (verified):** the §5 dose multipliers `σ_ℓ ∈ {0.5, 1.0, 2.0}·√v_ref` now carry `[PROPOSED — apparatus parameter]` (line 47). The prior v2 omission is closed. ✓

**Blocking P3 defects (untagged numeric test criteria):**

1. **§2 Example A pass threshold** — `|β* − 0.2| < 0.05` (line 86): the 0.05 validation tolerance is a pass/fail test criterion for the estimator's correctness validation. It carries no inline source-class tag. The trailing `[Sol-XF-5]` is a provenance citation (P6), not a P3 source-class tag, and does not cover the tolerance.
2. **§2 Example B pass threshold** — `|β*| < 0.05` (line 87): same defect — untagged pass/fail tolerance.

These are pre-registered pass/fail criteria that gate whether the estimator implementation is accepted; under P3 they require an inline tag (expected class: `[PROPOSED — apparatus parameter]`). The 0.2 anchor in Example A is the locked bar (`[BAR-Entry 11]`), but the ±0.05 validation tolerance is a distinct, untagged criterion.

**Non-blocking P3 observations (numeric parameters that should carry tags for completeness, but are design parameters, restatements, or simulation assumptions rather than gating criteria, or are covered by an enclosing tag):**

- `N_w = 4` (lines 35, 37): structural replicate-count / test-design parameter; its sibling `W = 50` is tagged `[PROPOSED]`, so the omission is an inconsistency rather than an ambiguity of intent. Recommend tagging for parallelism.
- §8 `β* ≥ 0.2 (locked bar)` (line 264): restatement of the §2 `[BAR-Entry 11]` bar; recommend an inline `[BAR-Entry 11]` for formal completeness.
- §8 `true β* = 0.3` (lines 264, 277): a power-analysis simulation assumption (input), not a gating criterion; recommend a `[PROPOSED — apparatus parameter]` for provenance completeness.
- §8 "at least two misspecified profiles" (line 288): a count; minor.
- `C_ref = 0.75` (line 39): covered by the enclosing `[PROPOSED — requires Rebecca sign-off, G2 rider]` tag on the R\* block.

### P4 — Regime dating

Spec header states date 2026-08-19 and Regime B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding). Consistent. ✓

### P5 — Deviation memorialization

The narrowed claim (§1) is a P5-authorized interpretive ruling: it deviates from the broader constitutional L8 language and is memorialized with Rebecca's sign-off per Entry 81. Verified against the provenance log — Entry 81 explicitly records the ruling as "a P5-authorized interpretive ruling (deviation from the broader constitutional L8 language, memorialized with Rebecca's sign-off)." ✓

### P6 — Provenance citation check

- `[Entry 76]` (Ruling 3 + Ruling 9): verified against `provenance_log.md` Entry 76. Ruling 3 = L8 zero-noise baseline + severity-matched specificity on a pre-registered standardized proximal-component effect; Ruling 9 = candidate-blind tolerance calibration (candidate diagnostic-seed results are not inputs). Spec citations "Ruling 3 + Ruling 9 (Entry 76)" and the Ruling-9 candidate-blindness invocations in §2/§5/§8 match the log. ✓
- `[Entry 81]` (narrowed claim): verified verbatim against Entry 81. Option A adopted — an L8 pass certifies externally-closed selective-risk regulation dependent specifically on the mirror relative to the pre-registered control set; Damasio/Seth demoted from claim to motivation; "and only then" operationalized as specificity relative to the three-control panel (memory, feedback-channel, task-difficulty). Spec §1 and §10.1 match. ✓
- `[Sol-XF-n]` (XF-4–XF-11): verified against `SOL_CROSSFAMILY_L8_REVIEW.md`. Each resolution condition the spec claims to close is present in the Sol review and is operationalized in the spec as written (see per-finding verification below). ✓

---

## Per-finding closure verification (XF-4–XF-9, XF-10, XF-11)

- **XF-4 (split Level-0 rule):** spec §2 splits into (1) pre-registered apparatus-validity conditions that alone yield INSTRUMENT_FAILURE, and (2) candidate FAIL — "not eligible for a dose-response pass" — when validity holds but the baseline bound is exceeded. Candidate failure is not relabeled. ✓
- **XF-5 (exact estimator):** spec §2 gives regression inputs, slope numerator `β_s = Cov_s(D̄, x)/Var(x)` (Var(x)=1.25 fixed), standardization denominator `σ_pool,s`, degrees of freedom, zero-variance behavior (→ INSTRUMENT_FAILURE), synthetic validation with expected numeric outputs, and requires the power analysis to use the identical estimator. ✓ (BF-XF5-1 details below.)
- **XF-6 (specificity estimand):** spec §6 defines the slope-difference estimand `Δβ_s = β*_s(candidate) − β*_s(control)` (same units, same estimator), direction of exclusion (Δβ > 0 all seeds + pooled paired-bootstrap 95% CI excludes zero), missing/degenerate case (σ_pool=0 → INSTRUMENT_FAILURE for that seed), and the complete three-condition conjunction for PASS. ✓
- **XF-7 (L14 coverage response):** spec §7 defines `ΔCov_{s,ℓ}`, expected direction (≤ 0), minimum effect (0.05), per-seed aggregation (5 seeds, all-seeds-direction), and the disposition when potency holds but coverage does not move (→ L14 FAIL, candidate failure not instrument failure). ✓
- **XF-8 (dose validity):** spec §5 pre-registers confidence clipping (`ε_c = 1e-6`, float64), the calibration metric `ΔECE_ℓ`, expected monotonic direction, minimum potency (0.01), monotonicity tolerance (0.005), disposition on violation (→ INSTRUMENT_FAILURE), and prohibits candidate-output tuning. ✓
- **XF-9 (power protocol + selection rule):** spec §8 defines the synthetic data-generating family, effect-size target (β* ≥ 0.2), parameter grid, simulation count (10,000, deterministic seeds), false-kill calculation, sensitivity map, a deterministic selection rule for (C_min, η), misspecification stress-test, and publication of code/seeds/grid/estimator/result-table. ✓
- **XF-10 (universal feedback channel):** spec §4 mandates the L7/L10 delta review, state-reset constraints (reset to post-training checkpoint between law batteries; no cross-law carryover), retention constraints (state carries within a single L8 battery across windows; no carry across dose levels within a seed), and upgrades the L7/L10 reconciliation from documentation-only to a semantic-equivalence demonstration that triggers a specification delta if any scored behavior changes. ✓
- **XF-11 (boundary annotation):** spec §6.4 preserves FAIL as the primary machine-readable and public verdict; the boundary condition is secondary diagnosis only; it may not authorize reruns or soften aggregate failure counts. ✓

The settled FRAME findings XF-1/2/3 are not re-litigated; their resolution via Entry 81 is reflected in §1 and §10.

---

## The three v2 → v2.1 remediations

### BF-XF5-1 — W notation disambiguated (§2, §8): VERIFIED

- `N_w = 4` (windows per dose) is introduced as distinct from `W = 50` (queries per window). Regression inputs now reference `w ∈ {1, ..., N_w}`.
- `σ_pool` degrees of freedom restated as `N_w − 1 = 3` per dose and `L × (N_w − 1) = 12` total.
- Bootstrap resampling unit corrected from the prior `W × L = 200` (query-level, internally inconsistent with the point estimator's window-level replicate structure) to `N_w × L = 16` window-level deviations per seed. This is a correction to the inferential (CI) procedure that aligns it with the point estimator's replicate unit — the correct closure of BF-XF5-1, not a new defect. The point-estimator algebra is unchanged.
- §8 effect-size target updated to reference `W = 50` queries/window and `N_w = 4` windows/dose consistently.
- Synthetic validation Examples A and B (expected outputs and pass thresholds) unchanged by the delta.

### BF-P3-1 — Dose multipliers tagged (§5): VERIFIED

- `[PROPOSED — apparatus parameter]` added to `σ_ℓ ∈ {0.5, 1.0, 2.0}·√v_ref` (line 47). The missing P3 tag is closed.

### BF-L19-1 — §6.2/§6.3 control arms fully pre-registered: VERIFIED

- §6.2 feedback-channel: potency floor specified as `mean |τ_drift_ℓ| ≥ 0.02`; tagged `[PROPOSED — apparatus parameter]` `[LAW-L19]`; INSTRUMENT_FAILURE on potency failure. The qualitative "e.g." placeholder is replaced with a concrete criterion.
- §6.3 task-difficulty: deterministic construction specified (retrieval-chain-length multipliers 1.5× / 2× / 3×); potency floor specified as oracle-accuracy drop ≥ 0.05; tagged `[PROPOSED — apparatus parameter]` `[LAW-L19]`; INSTRUMENT_FAILURE on potency failure. Qualitative placeholders replaced.

Note on `[LAW-L19]` beside `[PROPOSED]`: L19 mandates pre-registration of bars and kill conditions; these `[PROPOSED]` values are exactly the ones that must be frozen before scoring. The `[LAW-L19]` tag is therefore clarifying (it flags the pre-registration obligation) and not misleading, because `[PROPOSED]` correctly marks the value's class as unsigned. Not a P3 violation.

---

## Collateral-diff check (06f388e...55ce3f0)

The delta touches only: `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (hunks in §2, §5, §6.2, §6.3, §8) and `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md`. No closed finding (XF-4, XF-6, XF-7, XF-8, XF-9, XF-10, XF-11) was disturbed. No locked bar value changed. No estimator algebra changed. No synthetic validation changed. The changelog's "Confirmation" section (no locked bar changed; no algebraic form changed; no synthetic validation changed; no closed finding disturbed; L3/O-14/O-15/INSTRUMENT_FAILURE/seed custody/L15–L17 fence preserved; P1–P6 maintained) is accurate.

---

## Locked bars preserved

Against `M0_DECISION_SHEET.md` line 21 (L8 row): ≥3 noise doses (spec uses 4 levels, 0–3); Spearman ρ ≥ 0.8; standardized slope ≥ 0.2; specificity control mandatory; 5 seeds. The spec's `[BAR-Entry 11]` citations match. Against the inferential policy (line 29): 5 seeds + all-seed direction consistency + pooled bootstrap 95% CI excluding zero; the spec's §6 XF-6 `[BAR-Entry 11.3]` usage matches. No locked bar lowered, raised, renamed, reinterpreted, or silently replaced.

---

## Candidate-blindness (Ruling 9), O-14, O-15, L9, L18

- **Ruling 9 (candidate-blindness):** R\*, v_ref, the dose σ_ℓ values, the §8 power-analysis profiles, and all control-arm potency floors are derived from synthetic/oracle ground truth; no candidate output is an input anywhere. Preserved. ✓
- **O-14 (no re-run-on-failure):** the XF-4 split rule explicitly forbids relabeling a candidate baseline failure as instrument failure; no rerun is authorized on a failed run. ✓
- **O-15 (development runs diagnostic-only):** the §8 power analysis is candidate-blind synthetic simulation (diagnostic); development seeds 101–105 are O-15-labeled development-pool only. ✓
- **L9 (hard fence):** not implicated by this spec; not touched. ✓
- **L18 (contamination controls):** the L8 battery includes control arms (memory/feedback/task-difficulty) and apparatus-validity conditions; consistent with L18 at the design level. Full L18 verification is a scoring-gate concern, not this spec-design gate. ✓
- **L19 (pre-registration):** all bars and kill conditions are written before runs; `[PROPOSED]` values are explicitly reserved for Rebecca's sign-off before the pre-registration freeze. ✓
- **Seed rule (≥2 unseen scoring seeds):** scoring seeds are downstream and authorized only via Rebecca's courier channel; the pointer package confirms no scoring or hold-out seeds were exposed. ✓
- **No L15/L16/L17 before M5:** the spec does not invoke L15/L16/L17; no M5-only work authorized. ✓

---

## Blocking findings (classified)

1. **[SPEC DEFECT — P3 source-class tag]** §2 Example A pass tolerance `|β* − 0.2| < 0.05` (line 86): untagged numeric test criterion. The `[Sol-XF-5]` provenance citation does not satisfy P3.
2. **[SPEC DEFECT — P3 source-class tag]** §2 Example B pass tolerance `|β*| < 0.05` (line 87): untagged numeric test criterion.

Both are pre-registered pass/fail criteria for the estimator validation. Recommended class: `[PROPOSED — apparatus parameter]` (or, if Rebecca intends them as locked, `[BAR-Entry n]`). The 0.2 anchor in Example A is the locked bar; the ±0.05 tolerance is the untagged criterion.

## Non-blocking findings

1. **Version label mismatch:** the in-document title still reads "v2"; the commit, changelog, and handoff label the document "v2.1". Recommend aligning the title to v2.1 at the next touch.
2. **§2 Example A notation:** `ε ~ N(0, 0.01)` is ambiguous to readers using the SD convention. The spec's own expected `β* ≈ 0.02 / 0.1 = 0.2` disambiguates the author's intent as variance 0.01 (SD 0.1) under the standard N(μ, σ²) convention, so the example is internally consistent. Recommend stating "variance 0.01 (SD 0.1)" explicitly at the freeze to remove implementer ambiguity (a TASK BUILDER reading N(0, 0.01) as SD 0.01 would compute β* ≈ 2.0 and falsely fail the validation).
3. **P3 tag completeness (non-gating parameters):** `N_w = 4` (lines 35, 37) is untagged while its sibling `W = 50` is tagged; the §8 restatement `β* ≥ 0.2 (locked bar)` (line 264) and the simulation assumption `true β* = 0.3` (lines 264, 277) lack inline tags. Recommend tagging for provenance completeness.
4. **L14 coupling vs standalone L14 bars:** §7 operationalizes the L14 coupling conditions (readable / affected-by-memory / predictive-target) with a coverage-response acceptance test (`ΔCov ≥ 0.05`) and a prediction-vs-naive-baseline test, distinct from the M0 standalone L14 bars ("affected by" d ≥ 0.5; "predictive target" correlation ≥ 0.3). This is a proposed coupling operationalization reserved for Rebecca's G-gate ruling, not a replacement of the standalone L14 bars. Flag for Rebecca's attention at the Principal gate to confirm the coupling test is not weaker than the locked L14 bars intend.
5. **§8 list formatting:** the renumbering of item 2 to a dash is a cosmetic markdown inconsistency.

---

## Preserved evidence

INSTRUMENT_FAILURE retained; no scoring seed was rerun (O-14); all locked bars intact; no law text modified (P1 preserved); L3 pre-scoring gate preserved; the three v2.1 remediations do not disturb any prior valid evidence.

---

## Public-repository safety — pre-push scan attestation

**Public-safety scan:** manual regex + content review against `PUBLIC_REPOSITORY_POLICY.md` §3.2, scope = this review file (single new file `reviews/critic_l8_spec_v2.1_focused_rereview.md`). Patterns checked: API keys/tokens (`ghp_`, `sk-`, `AKIA`, `xox`, bearer, JWT), `.env` contents, service-account JSON, SSH private keys, cloud-provider tokens, email addresses, phone numbers, physical addresses, absolute paths (`/home/`, `/Users/`, `C:\Users\`, sandbox hostnames), environment-variable dumps. **Findings: 0.** No credentials, PII, machine identifiers, private absolute paths, scoring-seed identities, or raw model outputs are present. Rebecca's name appears only as it already appears in the public constitution, NOTICE, and provenance log. **Disposition: cleared to push to `critic/l8-spec-v2.1-rereview`.**

Branch-push workflow (§9.2): scan run and attestation recorded before push; push to `critic/l8-spec-v2.1-rereview`; no merge to main (Rebecca sole merge authority).

---

## Next authorized role / routing

**BLOCK → returns to ARCHITECT** (the originating role for the spec), routed via the WORKFLOW COORDINATOR. The ARCHITECT is authorized to add the missing P3 source-class tags to the §2 Example A / Example B pass tolerances (and to address the non-blocking tag-completeness items) and re-issue for a focused re-review. The three v2.1 remediations (BF-XF5-1, BF-P3-1, BF-L19-1) are verified correct and need no further change.

On a subsequent CLEAR: §8 power-analysis + sensitivity-map artifact production (candidate-blind, O-15 diagnostic) proceeds, feeding Rebecca's Principal gate rulings G2–G5 (G1 resolved by Entry 81).

## Explicitly prohibited actions

No modification of the spec, constitution, provenance log, M0 sheet, STATE.md, or any artifact other than this review file. No merging to main. No scoring, seed execution, hold-out seed exposure, or candidate-output tuning. No L15/L16/L17 before M5. No renaming or reinterpreting of INSTRUMENT_FAILURE or any negative result. No re-litigating the settled FRAME findings XF-1/2/3. No re-deriving the closed findings XF-4/6/7/8/9/10/11. No L8 implementation or TASK BUILDER release. No re-run-on-failure (O-14).

## Confirmation

No scoring, rerun, hold-out seed exposure, candidate-blindness breach, or unauthorized merge occurred. No public-repository push other than this review file to `critic/l8-spec-v2.1-rereview` (scan-attested, 0 findings). The CRITIC did not co-author, fix, or modify the spec under review; this review is the only file authored by the CRITIC.
