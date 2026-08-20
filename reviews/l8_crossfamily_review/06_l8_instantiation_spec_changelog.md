# L8 Instantiation Specification — Changelog

**Spec:** `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md`
**Date:** 2026-08-20 · **Author:** ARCHITECT
**Branch:** `architect/l8-g2g4-remediation` (v2.5.1/v2.5/v2.4/v2.3); `architect/l8-instantiation-v2.2-fresh` (v2.2); v2.1/v2 on `architect/l8-instantiation-v2`
**Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)

---

## v2.5.1 — CRITIC provenance-pointer remediation (2026-08-20)

**Base:** `5209f3317232679a3c676af7944a4cc5dcdeed00`. **Review verdict:** BLOCK on one provenance-citation defect.

- Corrected the Sources pointer for `[LAW-L8]` from constitution line 26 to `docs/ARCHITECTURAL_CONSTITUTION_v2.md` line 28.
- Corrected the Sources pointer for `[LAW-L14]` from line 40 to line 42.
- Reconciled the non-blocking feasibility count to 48 billion valid bootstrap replicates and up to 52.8 billion attempted replicates at the 5,500-attempt ceiling. `[PROPOSED]`

No law text, locked bar, estimator, predicate, schema, seed rule, apparatus rule, workload gate, or sequencing rule changed. No implementation, benchmark, screening, scoring, protected-seed exposure, G2–G4 ruling, or merge occurred.

---

## v2.5 — Second TASK BUILDER STOP: determinism and feasibility (2026-08-20)

**Base:** `4463cbc1799a6c41512bfef2be28315bea84d475`. **Gate served:** deterministic implementation contract and feasibility review before screening.

- Fixed bootstrap RNG at one stream per `(attempt,seed,dose)` and defined seed-manifest scope without enumerating billions of bootstrap seeds. `[PROPOSED]`
- Supplied literal config values, nested seed-derivation schema, prohibition array, status vocabulary, and assignment rules. `[PROPOSED]`
- Made apparatus checks run-level and fail-closed: a failed apparatus check aborts publication; it is never diluted into per-repetition counts. `[PROPOSED]`
- Generalized the reviewed calibration algorithm across geometry, with exact seeds, manifest/cache schema, digest, validation, and reuse rules. `[PROPOSED]`
- Defined rehearsal fixture-digest schema, all twelve exact case setups, injection boundaries, assertion IDs, exit contracts, and preservation requirements. `[PROPOSED]`
- Added recoverable JSON-plus-sidecar pair publication and explicit Commit A (implementation) / Commit B (evidence) lifecycle. `[PROPOSED]`
- Recorded workload: 9.6 million cell repetitions and up to 48 billion bootstrap replicates. Added a fixed feasibility benchmark and withdrew full-screen authorization pending benchmark review and a separate Rebecca ruling. `[PROPOSED]`

No implementation, benchmark, screening, simulation, artifact, scoring, protected-seed access, G2–G4 decision, or merge occurred. Locked bars remain unchanged. `[BAR-Entry 11]` `[BAR-Entry 11.3]`

---

## v2.4 — Deterministic implementation amendment after TASK BUILDER STOP (2026-08-20)

**Base:** `2819bf7731b86ef730a867671217aa9d1dba2de7` (v2.3). **Gate served:** deterministic diagnostic contract before implementation or compute.

- Defined exact midrank Spearman, positive-direction, pooled-bootstrap statistic, stratified resampling, percentile interval, quantile convention, RNG derivation, invalid-replicate handling, denominator, and overlapping predicate-rate accounting. `[PROPOSED]`
- Required all 20 battery geometries across all 240 nuisance/operating cells; acceptance is the conjunction of cell-level Wilson upper bounds, not a mean or pooled rate. `[PROPOSED]`
- Defined Wilson constants/formula, geometry-aware calibration/seeds, finalists, and the authorization boundary between 2,000-repetition screening and 10,000-repetition confirmation. `[PROPOSED]`
- Defined resolved-config and seed-manifest schemas, canonical JSON, SHA-256 digests, estimator identity, output paths/schemas, completeness predicates, and atomic publication/recovery. `[PROPOSED]`
- Defined internal production-path fault hooks, exception/exit contracts, O-14-safe synthetic recovery, independent fixed fixtures, serial/parallel comparison, and rehearsal-report schema. `[PROPOSED]`
- Fixed repository routing: TASK BUILDER destination branch from the approved v2.4 result, executable baseline `b1397498ca369067e956479e6c2bd6b0793c3e89`, historical result `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3` read-only. `[PROPOSED]`
- Sequencing corrected to ARCHITECT → fresh-context CRITIC → Rebecca approval → TASK BUILDER diagnostic implementation/screening → fresh-context CRITIC → Rebecca.

No implementation, test, fixture, simulation, diagnostic artifact, scoring action, seed exposure, G2–G4 decision, or merge occurred. All locked L8 bars remain unchanged. `[BAR-Entry 11]` `[BAR-Entry 11.3]`

---

## v2.3 — L8 G2–G4 aggregation and battery-size remediation (2026-08-19)

**Base:** `c7d7bed6b259` (v2.2). **Gate served:** remediation design before any G2–G4 decision.

### Verdict and estimand alignment

- Verified from M0 Entry 11.3, M4 spec §3.2/§3.5, and M4 task spec §3.2 that L8 uses all-seeds-direction across five seeds, not a five-seed-mean threshold. `[BAR-Entry 11.3]`
- Defined the complete simulated trend verdict as the conjunction of per-seed Spearman, per-seed standardized-slope, all-seed direction, and pooled bootstrap interval conditions. `[BAR-Entry 11]` `[BAR-Entry 11.3]`
- Made false kill of that complete five-seed verdict primary. Retained the five-seed-mean false-kill measure as diagnostic only. `[PROPOSED]`
- Corrected both aggregation descriptions: each cell value is the mean across 15 `(α,v)` combination-level decision rates; the any-seed quantity is not the fraction of combinations with any failure.

### Battery-size sweep and deferred map

- Added candidate-blind `W × N_w` sweep, ordered by total queries per dose, with operational false-kill upper-bound target below 10% and preferred target below 5%. `[PROPOSED]`
- Preserved four dose levels and all locked L8 bars. `[BAR-Entry 11]`
- Deferred sensitivity/misspecification-map recomputation and `(C_min,η)` selection until Rebecca freezes verdict aggregation and battery geometry.
- Replaced the operational use of the 50% “informative” false-kill boundary; a 43.22% false-kill cell is now explicitly operationally unacceptable. `[PROPOSED]`

### Equivalence, apparatus failure, and diagnostic integrity

- Added pre-registered `δ_eq = 0.01` absolute false-kill equivalence margin plus overlapping 95% intervals, with highest-coverage then lowest-gain selection inside the equivalence set. `[PROPOSED]`
- Restricted INSTRUMENT FAILURE to independent apparatus-validity failures. Ordinary per-seed statistical failures and zero variance are not reclassified. `[PROPOSED]`
- Added failure-injection and diagnostic-rehearsal contracts for incomplete output, corruption/partial writes, serial/parallel nondeterminism, configuration mismatch, and crash recovery. `[PROPOSED]`
- Corrected the Monte Carlo statement: more simulations narrow uncertainty; the point estimate need not increase.

### Sequencing and authorization

- Route is ARCHITECT → TASK BUILDER diagnostic implementation/sweep → fresh-context CRITIC → Rebecca.
- G2–G4 remain open. No protected seeds, scoring, final L8 scoring implementation, 10,000-simulation stress rerun, freeze, merge, or TASK BUILDER release beyond the diagnostic remediation scope is authorized.

### Locked-bar confirmation

No locked bar was lowered, raised, renamed, or replaced: ≥3 noise doses, Spearman `ρ ≥ 0.8`, standardized slope `≥ 0.2`, specificity mandatory, and five seeds are preserved. `[BAR-Entry 11]` `[BAR-Entry 11.3]`

---

## v2.2 — Comprehensive P3 source-class sweep (2026-08-19)

**Base:** `55ce3f0` (v2.1, CRITIC-cleared baseline for BF-XF5-1 / BF-P3-1 / BF-L19-1). **Not** built on `45fd755` (prior v2.2 false attestation — preserved as evidence on `architect/l8-instantiation-v2`). Fresh comprehensive sweep on new branch `architect/l8-instantiation-v2.2-fresh`.

**Scope:** Tags, labels, and notation ONLY. No threshold value, locked bar, kill condition, scoring predicate, estimator algebra, synthetic-example expected output, candidate-blindness boundary, closed finding, or verified fix changed.

### Comprehensive sweep — every numeric parameter now carries a source-class tag

A full numeric-token sweep of the spec was performed (not point-by-point). The remaining CRITIC sweep items were exactly the nine listed items; the true untagged numeric-parameter defects among them were corrected, and item 7 was resolved by the clearly-covering enclosing tag. No additional untagged numeric parameter outside the nine was found. Every numeric token in the spec is now either (a) explicitly source-class tagged, (b) a restatement of an already-tagged parameter, (c) derived arithmetic (degrees of freedom, counts), or (d) a law/section/version/list identifier.

### Items applied (all nine)

**Blocking P3 (two):**
1. §2 Example A pass tolerance `|β* − 0.2| < 0.05` (line 86): added `[PROPOSED — apparatus parameter]` to the ±0.05 tolerance; the 0.2 anchor tagged `[BAR-Entry 11]`.
2. §2 Example B pass tolerance `|β*| < 0.05` (line 87): added `[PROPOSED — apparatus parameter]`.

**Non-blocking P3 (five):**
3. `N_w = 4` (lines 35, 37): added `[PROPOSED]` for parallelism with `W = 50` `[PROPOSED]`.
4. §8 `β* ≥ 0.2 (locked bar)` (line 264): added inline `[BAR-Entry 11]`.
5. §8 `true β* = 0.3` / `true β* ≥ 0.3` (lines 264, 277): added `[PROPOSED — apparatus parameter]`.
6. §8 "at least two misspecified profiles" (line 288): added `[PROPOSED — apparatus parameter]` (reads as a protocol criterion).
7. `C_ref = 0.75` (line 40): **no inline tag added.** The enclosing `[PROPOSED — requires Rebecca sign-off, G2 rider]` tag on the R* block (line 39) clearly covers `C_ref = 0.75` and `m = 0.05`. Per the handoff conditional ("add an inline tag if the enclosing tag does not clearly cover it"), no separate inline tag is required. This corrects the prior false attestation, which claimed an inline tag was added when none was.

**Version label:**
8. In-document title (line 1) `v2` → `v2.2`; status field (line 5) `DRAFT v2` → `DRAFT v2.2`; narrative version references in §8 (line 258), §10 (line 312), and §12 (line 330) `spec v2` → `spec v2.2` (these refer to the current spec, not merely lineage nodes).

**Example A notation:**
9. §2 Example A `ε ~ N(0, 0.01)` (line 86): clarified as "variance 0.01; SD 0.1 — N(μ, σ²) convention." The same clarification was applied to Example B (line 87) for consistency (identical notation, identical implementer-ambiguity risk). No expected output changed: `β* ≈ 0.02 / 0.1 = 0.2` (Example A) and `β* ≈ 0.0` (Example B) are unchanged.

### Confirmation

- All nine items addressed (two blocking P3 + five non-blocking P3 + version label + Example A notation).
- No threshold value, locked bar, kill condition, scoring predicate, estimator algebra, synthetic-example expected output, candidate-blindness boundary, closed finding, or verified fix changed. This sweep was tags, labels, and notation ONLY.
- A full P3 sweep was performed (not point-by-point): every numeric parameter in the spec now carries a source-class tag (inline or via a clearly-covering enclosing tag).
- P1 (no law reconstruction), P2 (verbatim law), P4 (regime dating), P5 (Entry 81 deviation memorialized), P6 (provenance citations) all maintained.
- Locked bars preserved: ≥3 dose levels, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds. No bar lowered, raised, renamed, or reinterpreted. No negative result or INSTRUMENT_FAILURE label touched.

### Pre-push scan attestation

A pre-push self-scan was performed on all changed content before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. Changed content is spec/changelog text, source-class tags, and SHAs only. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## v2.1 — CRITIC BLOCK remediation: BF-XF5-1 + BF-P3-1 + BF-L19-1 (2026-08-19)

CRITIC fresh-context delta review of v2 returned BLOCK with three targeted findings. Seven of eight findings (XF-4, XF-6, XF-7, XF-8, XF-9, XF-10, XF-11) verified CLOSED; settled XF-1/2/3 reflected per Entry 81. No locked bar, algebraic estimator form, synthetic validation, candidate-blindness, or closed finding touched.

### BF-XF5-1: W notation disambiguated (§2, §8)

Introduced `N_w = 4` (windows per dose) as distinct from `W = 50` (queries per window). Regression inputs now reference `w ∈ {1,...,N_w}`. σ_pool df restated as `N_w − 1 = 3` per dose, `L × (N_w − 1) = 12` total. Bootstrap resampling unit restated as window-level deviations with `N_w × L = 16` observations per seed. §8 effect-size target updated to reference W=50 queries/window, N_w=4 windows/dose consistently.

### BF-P3-1: Dose multipliers tagged (§5)

Added `[PROPOSED — apparatus parameter]` source tag to `σ_ℓ ∈ {0.5, 1.0, 2.0}·√v_ref` in §5.

### BF-L19-1: §6.2/§6.3 control arms fully pre-registered (§6.2, §6.3)

§6.2 feedback-channel: potency floor specified as mean |τ_drift| ≥ 0.02. Tagged [PROPOSED — apparatus parameter] [LAW-L19]. INSTRUMENT_FAILURE on potency failure.
§6.3 task-difficulty: deterministic construction specified (retrieval-chain length multiplier: 1.5×, 2×, 3×). Potency floor specified as oracle accuracy drop ≥ 0.05. Tagged [PROPOSED — apparatus parameter] [LAW-L19]. INSTRUMENT_FAILURE on potency failure. Qualitative "e.g." placeholders replaced.

### Confirmation

No locked bar value changed. No algebraic estimator form changed. No synthetic validation changed. No closed finding disturbed. L3 gate preserved. O-14/O-15, INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved. P1–P6 maintained.

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
