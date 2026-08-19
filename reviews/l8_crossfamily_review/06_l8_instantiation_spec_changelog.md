# L8 Instantiation Specification — Changelog

**Spec:** `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md`
**Date:** 2026-08-19 · **Author:** ARCHITECT
**Branch:** `architect/l8-instantiation-v2`
**Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)

---

## v2 — Narrowed claim (Entry 81) + XF-4–XF-9 closure + riders (2026-08-19)

Full rewrite of v1 implementing Rebecca's narrowed claim (Entry 81) and closing all six BLOCKING findings (XF-4–XF-9) and two ADVISORY riders (XF-10, XF-11) from the Sol cross-family review.

### §1/§10: Narrowed claim rewrite (Entry 81)

§1 rewritten: L8 pass certifies externally-closed selective-risk regulation dependent specifically on the mirror relative to the pre-registered control set — not intrinsic stakes or organism-equivalent homeostasis. Damasio/Seth demoted from claim to motivation. "And only then" operationalized as specificity relative to three-control panel (memory + feedback-channel + task-difficulty). `[Entry 81]` (P5-authorized interpretive ruling)

§10 rewritten: Evidentiary posture updated to reflect narrowed claim. Manipulation-check/discriminative-load distinction preserved. Chain disclosure updated to include Sol review and Entry 81.

### XF-4: Level-0 rule split (§2)

Split the Level-0 gate into apparatus-validity conditions (INSTRUMENT_FAILURE) and candidate baseline check (candidate FAIL — "not eligible for a dose-response pass"). Apparatus-validity conditions: oracle labels correct, feedback timing audit, dose mechanism produces ΔECE on synthetic reference, battery fully administered. Candidate baseline miss is NOT relabeled. `[Sol-XF-4]`

### XF-5: Exact standardized-slope estimator (§2)

Defined the exact estimator as an equation: regression of D on dose, standardized by pooled within-dose SD of window-level deviations. Specified: slope numerator (Cov(D̄, x)/Var(x)), denominator (pooled within-dose SD with W−1 df per dose, L×(W−1) total df), zero-variance behavior (INSTRUMENT_FAILURE), degrees of freedom for CI (W×L=200 per seed). Two synthetic validation examples with expected numeric outputs. Power analysis must use identical estimator. `[Sol-XF-5]`

### XF-6: Specificity estimand and conjunction (§6)

Defined slope-difference estimand: Δβ = β*(candidate) − β*(control), same units, same estimator. Direction: Δβ > 0 all seeds + pooled bootstrap 95% CI excludes zero. Seed aggregation: 5 seeds, all-seeds-direction + pooled paired-bootstrap. Interval: 5,000 resamples, 95% CI, two-sided. Missing/degenerate: σ_pool=0 → INSTRUMENT_FAILURE for that seed. Complete conjunction for PASS: 3 conditions (all-seeds direction, CI excludes zero, absolute level check). Failure → KILL. `[Sol-XF-6]`

### XF-7: L14 coverage-response acceptance test (§7)

Added coverage-response estimand: ΔCov = Cov(memory arm, dose ℓ) − Cov(memory arm, dose 0). Expected direction: ΔCov ≤ 0 (memory corruption reduces coverage). Minimum effect: |ΔCov| ≥ 0.05. Per-seed: all-seeds-direction at highest dose. Disposition when potency present but coverage unmoved: L14 FAIL (coupling absent, candidate failure). `[Sol-XF-7]`

### XF-8: Dose domain and monotonicity validity (§5)

Added: confidence clipping (ε_c = 1e-6), calibration metric (ΔECE on synthetic profiles), expected direction (monotone non-decreasing), minimum potency (ΔECE_min = 0.01), monotonicity tolerance (δ_mono = 0.005), disposition (INSTRUMENT_FAILURE on violation — apparatus, not candidate), no candidate-output tuning. `[Sol-XF-8]`

### XF-9: Power/sensitivity protocol and selection rule (§8)

Defined: synthetic data-generating family (mirror profiles P(α,v) + task profiles), effect-size target (β* ≥ 0.2, false-kill at β* = 0.3), parameter grid (α × v × C_min × η), 10,000 simulations per combo with deterministic seeds, identical β* estimator, false-kill calculation, sensitivity map (3 regions), deterministic selection rule (informative region → max distance to boundaries → highest C_min → lowest η), misspecification stress-test, publication of code/seeds/grid/results. Artifacts produced in item 5 after CRITIC clearance. `[Sol-XF-9]`

### XF-10: L7/L10 delta review + state-reset/carryover constraints (§4)

Added: state-reset constraints (reset to post-training checkpoint between law batteries), retention constraints (state carries within L8 battery across windows, not across dose levels), zero cross-law carryover, permitted use of feedback (answered queries only, per-window, no per-query interleaved), semantic-equivalence demonstration (if scored behavior changes → specification delta, not documentation-only). `[Sol-XF-10]`

### XF-11: Boundary-condition annotation rule (§6.4)

Added one-sentence rule: boundary-condition annotation may never authorize reruns or soften aggregate failure counts; FAIL is primary verdict; boundary condition is secondary diagnosis only. `[Sol-XF-11]`

### Three-control panel (§6.2, §6.3 — Entry 81)

Added feedback-channel perturbation control (§6.2: seeded feedback-label corruption at {10%, 20%, 40%}). Added task-difficulty shift control (§6.3: progressively harder query distributions). Both pre-registered, with potency bars. Specificity now tested against all three controls per XF-6 estimand. `[Entry 81]`

### Confirmation

No locked bar value changed (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds). L3 pre-scoring gate preserved. O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved. P1–P6 maintained. P5: narrowed claim is Entry 81-authorized. XF-1/2/3 not re-litigated (settled by Entry 81). All new thresholds tagged [PROPOSED] or appropriate source class.

---

## v1 — Initial instantiation specification (2026-08-19)

[See v1 on main via PR #65, Entry 80]
