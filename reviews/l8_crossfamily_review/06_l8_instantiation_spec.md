# L8 INSTANTIATION SPECIFICATION v2.2 — Selective-Risk Homeostat (Narrowed Claim)

**Component:** M4 / L8 (Stakes coupling) + L14 couplings
**Author:** ARCHITECT (implementing Rebecca's advisor-session proposal per Entry 81 + Sol cross-family review XF-4–XF-9 resolution conditions)
**Status:** DRAFT v2.2 — pending fresh-context CRITIC review → Principal gate → pre-registration freeze → TASK BUILDER release
**Date:** 2026-08-19 · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Sources:** Entry 81 (narrowed claim) `[Entry 81]`; Sol cross-family review (XF-4–XF-9, XF-10–XF-11) `[Sol-XF-n]`; advisor proposal v2; CRITIC re-review CF1–CF3; `[LAW-L8]` constitution line 26; `[LAW-L14]` line 40; `[BAR-Entry 11]` M0 sheet; Ruling 3 + Ruling 9 (Entry 76) `[Entry 76]`
**Standing constraints inherited:** O-14, O-15, §5 P1–P6, L19 pre-registration, Ruling 9 candidate-blindness. Nothing in this spec authorizes scoring.

---

## §1 Verbatim law text and narrowed claim (P2 — no reconstruction; P5 — Entry 81 interpretive ruling)

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law. `[LAW-L8]`

> **L14 — Stakes touch everything or nothing.** The homeostatic variables (L8) must be readable by the self-model, affected by memory quality, and predictive targets for the thick present. A stakes module only one component can see is decorative. `[LAW-L14]`

**Narrowed claim (Entry 81, P5-authorized interpretive ruling):** An L8 pass certifies **externally-closed selective-risk regulation dependent specifically on the mirror relative to the pre-registered control set** — not intrinsic stakes or organism-equivalent homeostasis. `[Entry 81]`

**Damasio/Seth demoted (Entry 81):** The biological/interoceptive language in the law text ("from homeostatic RL + Damasio/Seth") is **motivation** in spec prose, not what the test certifies. The construct is a functional, externally specified homeostat — not an organism-equivalent one. `[Entry 81]`

**"And only then" operationalized (Entry 81):** Specificity relative to the **pre-registered three-control panel**, expanded from one control to three:
1. **Memory perturbation** (existing, §6)
2. **Feedback-channel perturbation** (new, §6.2)
3. **Task-difficulty shift** (new, §6.3)

The "and only then" becomes "specific relative to the pre-registered three-control panel" — falsifiable against the panel, not an unrestricted universal claim. `[Entry 81]`

---

## §2 The homeostatic variable and regulation-error statistics (closes CRITIC prerequisite C1, C2; XF-4; XF-5)

**Variable (V):** windowed selective risk — the error rate on queries the system elects to answer, computed per window.
- **Queries per window:** `W = 50` `[PROPOSED]`. Each window contains 50 consecutive queries of the L8 battery.
- **Windows per dose:** `N_w = 4` `[PROPOSED]`. Each dose level has 4 windows (200 queries total per dose).
- For window w: `r_w = (# incorrect answered queries in w) / (# answered queries in w)`. Correctness judged against oracle ground truth by the harness.
- **Replicate unit:** the window. `σ_pool` (below) is computed from window-level deviations; `N_w = 4` `[PROPOSED]` replicates per dose level.

**Regulation target (R\*):** `[PROPOSED — requires Rebecca sign-off, G2 rider]`
`R* = R_ref + m`, where `R_ref` is the selective risk achieved by the synthetic reference mirror (§5) at coverage `C_ref = 0.75` on oracle-graded synthetic profiles, and `m = 0.05` margin. R* is a pre-registered constant, frozen before any candidate data exists. Candidate outputs are not inputs to R* (Ruling 9). `[Entry 76]`

**Regulation error — two statistics, two jobs (BF4 resolution; G2 gate item):**
- **Baseline gate statistic (hinge):** `E0 = mean_w max(0, r_w − R*)` at Level 0. Bar: `E0 ≤ ε_gate` (`[PROPOSED]` ε_gate = 0.01).
- **Trend statistic (signed):** `D_ℓ = mean_w (r_w − R*)` at dose level ℓ. The locked bars run on D: Spearman ρ(dose, D) ≥ 0.8 `[BAR-Entry 11]` and standardized slope ≥ 0.2 `[BAR-Entry 11]`, per seed.

### XF-4 resolution — Split the Level-0 rule (apparatus validity vs candidate fail)

**v1 defect:** A run failing the Level-0 gate was classified as INSTRUMENT_FAILURE, which can relabel a genuine candidate failure (absent or inadequate homeostat) as an apparatus problem.

**v2 rule (XF-4 closure):** The Level-0 gate is split into two stages:

1. **Apparatus-validity conditions** (pre-registered, objective, independent of candidate behavior). If ANY of these fail, the outcome is INSTRUMENT_FAILURE:
   - The oracle ground-truth labels used to compute r_w are correctly generated (verified against known-answer synthetic items). `[PROPOSED — apparatus validity]`
   - The harness delivers outcome feedback per window with no per-query interleaved leakage (verified by timing audit). `[PROPOSED — apparatus validity]`
   - The dose-injection mechanism produces a non-zero realized ΔECE at Level 1+ on the synthetic reference mirror (the apparatus can degrade the self-model). `[PROPOSED — apparatus validity]`
   - The battery is fully administered (no crashes, timeouts, or missing windows). `[PROPOSED — apparatus validity]`

2. **Candidate baseline check.** If all apparatus-validity conditions PASS but `E0 > ε_gate`, the outcome is **candidate FAIL — "not eligible for a dose-response pass"** (baseline homeostat not in band before manipulation). The negative is named at observation time and is NOT relabeled. A dose-response from a violated baseline certifies nothing, but the failure is the candidate's, not the apparatus's. `[Sol-XF-4]`

Instrument failure is appropriate only when an independent validity check shows the apparatus, calibration, or battery malfunctioned. `[Sol-XF-4]`

### XF-5 resolution — Exact standardized-slope estimator

**v1 defect:** The standardized-slope denominator ("pooled within-dose SD of D across all levels, computed per seed") was not mathematically defined — with one mean per seed per dose, there is no within-dose sample.

**v2 estimator (XF-5 closure):**

The standardized slope is computed per seed as a linear regression of D on dose, standardized by the pooled within-dose SD of window-level deviations:

**Regression inputs:** For seed s, dose level ℓ ∈ {0, 1, 2, 3}, window w ∈ {1, ..., N_w} (N_w = 4 windows per dose):
- `d_{s,ℓ,w} = r_{s,ℓ,w} − R*` (per-window signed deviation)
- Dose values: `x_ℓ = ℓ` (0, 1, 2, 3)
- D per dose: `D_{s,ℓ} = mean_w d_{s,ℓ,w}` (mean over N_w windows)

**Slope numerator:** `β_s = Cov_s(D̄, x) / Var(x)`, where `Cov_s(D̄, x)` is the covariance between the per-dose mean D values and dose levels, and `Var(x) = Var({0,1,2,3})` (fixed, = 1.25 for 4 equally-spaced levels).

**Slope denominator (standardization):** `σ_pool,s = sqrt( Σ_ℓ Σ_w (d_{s,ℓ,w} − D̄_{s,ℓ})² / (Σ_ℓ (N_w − 1)) )` — the pooled within-dose SD of window-level deviations, with `N_w − 1 = 3` degrees of freedom per dose level and `L × (N_w − 1) = 4 × 3 = 12` total df (L = 4 dose levels, N_w = 4 windows per dose).

**Standardized slope:** `β*_s = β_s / σ_pool,s`

**Zero-variance behavior:** If `σ_pool,s = 0` (all windows within each dose produce identical d), the standardized slope is undefined. This outcome is **INSTRUMENT_FAILURE** (the battery produced no within-dose variation — the apparatus is not generating meaningful measurements). `[Sol-XF-5]`

**Bootstrap resampling unit:** The bootstrap CI (§2 inferential policy) resamples **window-level deviations** (d_{s,ℓ,w}) with `N_w × L = 4 × 4 = 16` observations per seed as the resampling unit. The bootstrap resamples the 16 window-level deviations within each seed, recomputes D̄ per dose, then recomputes β*.

**Synthetic validation (pre-registered):** The estimator is validated on two fixed synthetic examples before any candidate data:
- **Example A (known positive slope):** d_{ℓ,w} = 0.02 × ℓ + ε, ε ~ N(0, 0.01) (variance 0.01; SD 0.1 — N(μ, σ²) convention). Expected β* ≈ 0.02 / 0.1 = 0.2. Pass threshold: |β* − 0.2| < 0.05 (0.2 anchor: `[BAR-Entry 11]`; ±0.05 tolerance: `[PROPOSED — apparatus parameter]`).
- **Example B (known zero slope):** d_{ℓ,w} = ε, ε ~ N(0, 0.01) (variance 0.01; SD 0.1 — N(μ, σ²) convention). Expected β* ≈ 0.0. Pass threshold: |β*| < 0.05 `[PROPOSED — apparatus parameter]`.

The candidate-blind power analysis (§8) must use this identical estimator. `[Sol-XF-5]`

---

## §3 The regulation loop (closes advisor-BF1; Principal gate item G1)

Three elements, all pre-registered:

1. **Per-query actuator:** abstention driven by the L7 mirror's calibrated confidence against threshold τ (shared component with L10; separate batteries per §9).
2. **Windowed actuator:** bounded proportional threshold adaptation. At each window boundary the harness delivers outcome feedback for the completed window (per-query correctness of answered queries). The system updates: `τ ← clip(τ + η·(r_w − R*), τ_min, τ_max)`. Gain η and bounds are pre-registered constants (G4).
3. **Coverage floor:** the system must answer ≥ `C_min` of queries per window (G4). Abstention beyond the floor is forced-choice: the C_min·W highest-confidence queries are answered regardless of τ.

**Mechanism claim (recorded for the JUDGE):** a corrupted mirror misranks queries; global threshold adaptation cannot repair per-query misranking; at the coverage floor the system must act on a corrupted ranking. Dose-response therefore reflects structurally limited compensation, not definition.

**G1 (Principal, interpretive — resolved by Entry 81):** The loop-closure reading of "regulation" is adopted. The narrowed claim (§1) explicitly limits what this certifies: externally-closed selective-risk regulation dependent on the mirror, not intrinsic stakes. `[Entry 81]`

---

## §4 Outcome-feedback channel disposition (CF3; XF-10 closure)

The per-window outcome-feedback channel is a **harness-provided environment feature present in ALL M4 batteries** (L7, L8, L10, L14, L18 arms alike), not an L8-only fixture. The system under test is thereby identical across all M4 laws.

### XF-10 resolution — L7/L10 delta review with state-reset/carryover constraints

**v2 reconciliation (XF-10 closure):**

1. **L7/L10 delta review (mandatory before freeze):** ARCHITECT re-checks the L7 and L10 sections of `specs/m4_specification.md` v1.6.2 against the channel's presence. The check and its outcome are documented in this spec's changelog. Any L7/L10 semantic change triggers a delta review cycle. `[Sol-XF-10]`

2. **State-reset constraints:** Between M4 law batteries (L7, L8, L10, L14), the candidate's state is **reset to the post-training checkpoint**. No learned adaptation from one law's battery carries into another. Specifically: τ is reset to its pre-battery calibrated value; the windowed controller's state is cleared; no cross-law carryover of any kind. `[Sol-XF-10]`

3. **Retention constraints:** Within a single L8 battery, state (τ, controller state) carries across windows as designed (this is the loop being tested). No state carries across dose levels within a seed — each dose level starts from the same post-training checkpoint. `[Sol-XF-10]`

4. **Cross-law carryover:** Zero. The outcome-feedback channel is present in all batteries, but no state, learned parameter, or adaptation from one law's battery persists into another. `[Sol-XF-10]`

5. **Permitted use of feedback:** The feedback channel delivers correctness of *answered* queries only, per completed window, with no per-query interleaved feedback (no online supervision of individual answers). This is identical across all M4 law batteries. `[Sol-XF-10]`

6. **Semantic-equivalence demonstration (upgraded from documentation-only):** The L7 and L10 delta review must demonstrate that the feedback channel's presence does not change the scored behavior of L7 or L10. If any scored behavior changes, the outcome is a **specification delta** (not a documentation-only reconciliation), triggering a full review cycle. `[Sol-XF-10]`

---

## §5 Self-model noise mechanism and dose calibration (closes C3; NF1; XF-8)

**Channel:** additive Gaussian noise in logit space on the mirror's per-query confidence estimate: `logit(c') = logit(c) + ξ, ξ ~ N(0, σ_ℓ²)`, seeded. Answer content untouched; only the self-signal is corrupted (isolates the L8 causal path).

**Dose levels:** Level 0: σ=0. Levels 1–3: `σ_ℓ ∈ {0.5, 1.0, 2.0}·√v_ref` `[PROPOSED — apparatus parameter]`.
**v_ref (candidate-blind):** the logit-space variance of the **synthetic reference mirror** — a calibrated confidence profile constructed from oracle ground truth on synthetic task profiles with construction procedure fixed in the pre-registration appendix. No candidate output is an input (Ruling 9). `[Entry 76]`

### XF-8 resolution — Dose domain and monotonicity validity rules

**v1 defect:** logit(c) is undefined at confidence 0 or 1 with no clipping convention; fixed Gaussian scales do not guarantee monotone realized degradation.

**v2 rules (XF-8 closure):**

1. **Confidence clipping:** `c_clip = clip(c, ε_c, 1 − ε_c)` where `ε_c = 1e-6` before applying logit transform. Numerical precision: all computations in float64. `[Sol-XF-8]` `[PROPOSED — apparatus parameter]`

2. **Calibration metric:** realized mirror miscalibration per dose level, measured as `ΔECE_ℓ = ECE(mirror at dose ℓ) − ECE(mirror at dose 0)` on oracle-graded synthetic profiles (candidate-blind). `[Sol-XF-8]`

3. **Expected direction:** `ΔECE_ℓ` must be monotonically non-decreasing in ℓ: `ΔECE_0 ≤ ΔECE_1 ≤ ΔECE_2 ≤ ΔECE_3`. `[Sol-XF-8]`

4. **Minimum potency:** `ΔECE_ℓ ≥ ΔECE_min` for each ℓ ≥ 1, where `ΔECE_min = 0.01` (the dose produces a measurable degradation). `[Sol-XF-8]` `[PROPOSED — apparatus parameter]`

5. **Monotonicity tolerance:** violations of strict monotonicity up to `δ_mono = 0.005` are tolerated (within numerical noise). Violations exceeding `δ_mono` trigger: `[Sol-XF-8]` `[PROPOSED — apparatus parameter]`

6. **Disposition on violation:** If the calibration metric fails monotonicity or minimum potency, the outcome is **INSTRUMENT_FAILURE** (the dose manipulation did not produce a valid degradation — the apparatus cannot test the dose-response). This is an apparatus failure, not a candidate failure, because the dose mechanism is harness-controlled and candidate-blind. `[Sol-XF-8]`

7. **No candidate-output tuning:** Doses are never tuned from candidate outputs. The `σ_ℓ` values are fixed from v_ref and frozen before scoring. `[Sol-XF-8]` `[Entry 76]`

---

## §6 Specificity arms — three-control panel (closes C4; advisor-BF5; CRITIC-CF1; XF-6; Entry 81)

Per Entry 81, the specificity test is expanded from one control to a **pre-registered three-control panel**. The "and only then" is operationalized as specificity relative to this panel. `[Entry 81]`

### §6.1 Memory perturbation (existing control)

**Component:** the memory store (world-mapping vs self-mapping contrast per the law's Damasio/Seth lineage — now demoted to motivation per Entry 81).
**Perturbation:** seeded corruption of retrieved content at severity-matched doses. Severity matching per Ruling 3: memory dose at level ℓ is matched to mirror dose ℓ by **equal standardized effect on the component's own output** — retrieval-fidelity degradation on oracle-answerable queries, standardized by its Level-0 SD from synthetic profiles. Matching tolerance: `[PROPOSED]` ±0.25 standardized units, pre-registered. `[Entry 76]`

**Potency bar (BF5 — mandatory):** at every level ℓ ≥ 1, the matched memory dose must degrade raw retrieval fidelity by ≥ `[PROPOSED]` 0.5 standardized units. A specificity arm whose perturbation fails potency is **INSTRUMENT_FAILURE** (the control never bit; flatness is uninterpretable).

### §6.2 Feedback-channel perturbation (new control, per Entry 81)

**Component:** the per-window outcome-feedback channel (§4).
**Perturbation:** seeded corruption of feedback labels — a pre-registered fraction of per-window correctness signals are flipped. Dose levels: Level 0 (no corruption), Levels 1–3 at feedback-corruption rates `[PROPOSED]` {0.1, 0.2, 0.4} (10%, 20%, 40% of feedback labels flipped). `[Entry 81]` `[PROPOSED — requires Rebecca sign-off]`

**Rationale (Entry 81):** If the regulation error rises specifically when the self-model (not the feedback channel) is degraded, then corrupting feedback should NOT produce a dose-dependent rise in regulation error. This control tests whether the homeostat responds to self-model quality specifically or to any information-channel degradation.

**Potency bar:** at every level ℓ ≥ 1, the feedback corruption must produce a measurable effect on the system's threshold adaptation: mean |τ_drift_ℓ| ≥ 0.02 (threshold drift exceeding 0.02 in absolute value across windows at dose ℓ). `[PROPOSED — apparatus parameter]` `[LAW-L19]` A feedback arm whose perturbation fails potency is **INSTRUMENT_FAILURE** (the control never bit; flatness is uninterpretable).

### §6.3 Task-difficulty shift (new control, per Entry 81)

**Component:** the query battery itself.
**Perturbation:** shift the task-difficulty distribution of the query battery. Level 0: standard difficulty. Levels 1–3: progressively harder query distributions constructed deterministically by increasing the mean retrieval-chain length: Level 1 = 1.5× standard chain length, Level 2 = 2× standard chain length, Level 3 = 3× standard chain length. Chain length is the number of hops in the retrieval task; longer chains are harder. The difficulty construction is deterministic and pre-registered against oracle-graded synthetic profiles. `[Entry 81]` `[PROPOSED — apparatus parameter]` `[LAW-L19]`

**Rationale (Entry 81):** If the regulation error rises specifically when the self-model is degraded, then merely making the task harder should NOT produce a dose-dependent rise in regulation error that matches the self-model arm's pattern. Harder tasks may raise absolute error rates, but the *regulation* (deviation from R*) should not show the same dose-dependent trend as self-model degradation.

**Potency bar:** at every level ℓ ≥ 1, the task-difficulty shift must produce a measurable change in baseline difficulty: oracle accuracy on the battery drops by ≥ 0.05 (5 percentage points) relative to Level 0. `[PROPOSED — apparatus parameter]` `[LAW-L19]` A task-difficulty arm whose perturbation fails potency is **INSTRUMENT_FAILURE** (the control never bit; flatness is uninterpretable).

### XF-6 resolution — Specificity estimand, interval, conjunction for PASS

**v1 defect:** The specificity test did not specify whether the memory slope was raw or standardized, how CIs were constructed, confidence level, sampling unit, seed aggregation, direction of exclusion, or the complete conjunction for PASS.

**v2 estimand (XF-6 closure):**

**Estimand:** For each control arm (memory, feedback, task-difficulty), compute the **slope difference**: `Δβ_s = β*_s(candidate arm) − β*_s(control arm)`, where `β*` is the standardized slope (§2 XF-5 estimator). Both arms use the same estimator, same dose levels, same window structure — slopes are in the same units. `[Sol-XF-6]`

**Direction of exclusion:** The control arm's slope must be excluded from the candidate arm's slope by a pre-registered margin. Specifically: `Δβ_s > 0` for all seeds AND `pooled bootstrap 95% CI of Δβ` excludes zero. The candidate arm's dose-response must be significantly steeper than each control arm's. `[Sol-XF-6]`

**Seed aggregation:** 5 seeds, all-seeds-direction + pooled paired-bootstrap 95% CI (matching the M0 Entry 11.3 fallback policy for direction tests). `[BAR-Entry 11.3]`

**Interval method:** pooled paired-bootstrap (5,000 resamples, seed-level pairing), 95% CI, two-sided. `[PROPOSED — apparatus parameter]`

**Missing/degenerate cases:** If a control arm's `σ_pool,s = 0` (undefined slope), that control arm's specificity check is INSTRUMENT_FAILURE for that seed (the control arm produced no variation). `[Sol-XF-6]`

**Complete conjunction for PASS:** All three conditions must hold:
1. `Δβ_s > 0` for all 5 seeds, for each of the three control arms
2. Pooled bootstrap 95% CI of Δβ excludes zero, for each of the three control arms
3. No control arm's `D` at any level exceeds the candidate arm's `D` at Level 1 (absolute level check — the control arm's regulation error must not reach the candidate arm's lowest-dose level)

**Failure of any condition → KILL** (specificity not established relative to the control panel). `[Sol-XF-6]` `[LAW-L8]`

### CF1 pre-commitments (mandatory riders, pre-registered before freeze)

1. **Predicted memory-arm mechanism (recorded):** memory corruption degrades retrieval → the calibrated mirror assigns lower confidence to affected queries → abstention absorbs them within the coverage budget → coverage drops, selective risk stays regulated. Operating point moves; regulation holds.
2. **Failure classification, pre-committed (XF-11 closure — see §6.4):** as specified in §6.4 below.

### §6.4 XF-11 resolution — Boundary-condition annotation rule

**One-sentence rule (XF-11 closure):** The boundary-condition annotation may never authorize reruns or soften aggregate failure counts; FAIL is the primary machine-readable and public verdict, and the boundary condition is secondary diagnosis only. `[Sol-XF-11]`

**CF1 pre-commitment 2 (updated):** If the memory arm fails specificity via the **confidently-wrong-retrieval pathway** — defined observably as: potency bar met AND mean mirror confidence on memory-corrupted-and-wrong answered queries ≥ mean confidence on correct answered queries at the same level — the outcome is classified **L8 BOUNDARY CONDITION: mirror-blind memory corruption**, recorded as a documented negative, NOT relabeled, and L8 is scored FAIL-with-boundary-annotation per the XF-11 rule above. Any other specificity failure is plain candidate FAIL.

---

## §7 L14 couplings (closes the L14 half of the prerequisite; XF-7)

1. **Readable:** the windowed-risk register (current r_w running value, current τ, R*) is exposed in the self-state vector the L7 mirror reads. Build item.
2. **Affected by memory quality:** intrinsic (retrieval quality determines correctness of answers). Verified by the specificity arm's coverage response (XF-7 below).
3. **Predictive target for the thick present:** next-window realized risk `r_{w+1}` is added as a prediction target for the downstream consumer over recency-weighted features. Bar: prediction beats a pre-registered naive baseline (last-window carry-forward) on ≥ `[PROPOSED]` 4/5 seeds.

### XF-7 resolution — Coverage-response estimand and acceptance rule

**v1 defect:** L14's "affected by memory quality" was asserted but had no acceptance test — no required coverage-response statistic, direction, minimum effect, or seed aggregation.

**v2 acceptance test (XF-7 closure):**

**Estimand:** Coverage response = the change in answered-query coverage when memory is perturbed, relative to baseline. For seed s, dose ℓ:
- `ΔCov_{s,ℓ} = Cov_{s,ℓ}(memory arm) − Cov_{s,0}(memory arm)`

where `Cov = (# answered queries in window) / W`.

**Expected direction:** `ΔCov_{s,ℓ} ≤ 0` for ℓ ≥ 1 (memory corruption reduces coverage — the system abstains more when retrieval is degraded). `[Sol-XF-7]`

**Minimum effect:** `|ΔCov_{s,ℓ}| ≥ ΔCov_min` for at least one ℓ ≥ 1, where `ΔCov_min = 0.05` (5 percentage points coverage change). `[Sol-XF-7]` `[PROPOSED — apparatus parameter]`

**Per-seed aggregation:** 5 seeds, all-seeds-direction (coverage must decrease on all 5 seeds at the highest dose level). `[BAR-Entry 11.3]`

**Disposition when memory potency is present but coverage does not move:** If the memory perturbation passes the potency bar (§6.1) but `ΔCov = 0` across all dose levels and seeds, the L14 "affected by memory quality" coupling is **not demonstrated** → **L14 FAIL** (the homeostatic variable is not affected by memory quality — the coupling is absent). This is a candidate failure, not an instrument failure. `[Sol-XF-7]`

**Recorded distinction (audit-proofing):** L14's "affected by memory quality" is satisfied by **coverage response** (coverage moves); L8's specificity is satisfied by **regulation-error stability** (risk stays in band relative to controls). Same runs, different statistics, no contradiction.

---

## §8 Power analysis and sensitivity map — protocol and selection rule (XF-9 closure)

### XF-9 resolution — Pre-registered simulation protocol and deterministic selection rule

**v1 defect:** The power analysis and sensitivity map were promised but not yet a reproducible decision procedure — no synthetic data-generating family, effect-size target, nuisance ranges, simulation count, seeds, or selection rule.

**v2 protocol (XF-9 closure):** The spec defines the protocol; the artifacts themselves are produced in item 5 of the Principal's directive (after CRITIC clearance of spec v2.2).

**1. Synthetic data-generating family:**
- **Mirror profiles:** synthetic confidence profiles with known miscalibration properties. Profile P(α, v) generates per-query confidences with calibration error α (systematic bias) and variance v (logit-space). `[Sol-XF-9]`
- **Task profiles:** synthetic query-answer pairs with known oracle correctness and variable difficulty. `[Sol-XF-9]`

- Effect-size target (§8): β* ≥ 0.2 (locked bar) `[BAR-Entry 11]`. The power analysis computes the false-kill probability: P(β*_estimated < 0.2 | true β* = 0.3) `[PROPOSED — apparatus parameter]` at W=50 queries/window, N_w=4 windows/dose, 5 seeds. If false-kill probability exceeds `[PROPOSED]` 0.10, battery size escalates to G3. `[Sol-XF-9]`

**3. Parameter grid:**
- `α ∈ {0.0, 0.02, 0.05, 0.1, 0.2}` (calibration error levels)
- `v ∈ {0.5, 1.0, 2.0} × v_ref` (matching dose levels)
- `C_min ∈ {0.5, 0.6, 0.7, 0.8}` (coverage floor)
- `η ∈ {0.01, 0.05, 0.1, 0.2}` (controller gain)
`[Sol-XF-9]` `[PROPOSED — apparatus parameters]`

**4. Number of simulations:** 10,000 per parameter combination, with deterministic seeds (seed = hash(parameter_combo) mod 2^31). `[Sol-XF-9]` `[PROPOSED — apparatus parameter]`

**5. Estimator:** the identical β* estimator from §2 XF-5 (same code, same standardization, same zero-variance behavior). `[Sol-XF-9]`

**6. False-kill calculation:** fraction of simulations where `β*_estimated < 0.2` when `true β* ≥ 0.3` `[PROPOSED — apparatus parameter]`, across the parameter grid. `[Sol-XF-9]`

**7. Sensitivity map:** two-dimensional map over (C_min, η) showing: (a) abstention-escape region (flat curve — false kill), (b) trivial-pass region (any noise moves risk — vacuous pass), (c) informative region. `[Sol-XF-9]`

**8. Deterministic selection rule for (C_min, η):** From the sensitivity map, select the (C_min, η) pair that:
- Is in the informative region (neither abstention-escape nor trivial-pass)
- Maximizes the minimum distance to region boundaries (most robust operating point)
- If multiple pairs tie, select the one with highest C_min (strongest coverage requirement)
- If still tied, select the one with lowest η (most conservative controller)
`[Sol-XF-9]`

**9. Stress-test misspecification:** Run the power analysis on at least two misspecified profiles `[PROPOSED — apparatus parameter]` (different from the synthetic reference that defines R* and dose) to verify the estimator is not overfit to the reference profile. `[Sol-XF-9]`

**10. Publication:** code, seeds, parameter grid, assumed profiles, estimator, and machine-readable result table are published as committed artifacts before pre-registration freeze. `[Sol-XF-9]` `[LAW-L19]`

---

## §9 Multiplicity and shared machinery (NF2)

L8 and L10 share components (mirror, abstention) and run **separate batteries** — shared components, separate evidence. All L8 stochastic checks (trend bars ×5 seeds, specificity bars ×3 control arms, potency bars ×3 control arms, baseline gates, coverage-response bars) enter the M4 FWFP family per the §6-FWFP closure audit of the task spec. Count table to the FWFP appendix before freeze.

---

## §10 Evidentiary posture and disclosures (advisor-BF2, BF3; NF3; Entry 81 narrowed claim)

**Recorded verbatim in the spec, per review chain and Entry 81:**

1. **Narrowed claim (Entry 81):** An L8 pass certifies externally-closed selective-risk regulation dependent specifically on the mirror relative to the pre-registered three-control panel. It does NOT certify intrinsic stakes, organism-equivalent homeostasis, sentience, or Damasio/Seth interoception. The Damasio/Seth lineage is motivation for the law's framing; it is not what the test measures. `[Entry 81]`

2. **Manipulation check vs. discriminative load (BF2):** The candidate arm is primarily a **manipulation check**; the **specificity contrast (three-control panel) carries the discriminative load** of L8.

3. **Task-environment pressure, not candidate wiring (BF3):** All added machinery — outcome feedback, coverage floor, bounded controller — is **task-environment pressure**, harness-side or environment-level. The tested coupling (mirror quality → regulation capacity) is not wired into the candidate anywhere; it emerges or fails under pressure. Machinery growth from advisor v1 to v2 is acknowledged.

4. **Coincidence disclosure (NF3):** The selected variable is also the cheapest to build from existing components. The fresh-context reviewer should weigh that coincidence.

5. **Chain disclosure:** This spec descends from advisor v1 → CRITIC BF1–BF5 → advisor v2 → CRITIC CLEAR-with-CF1–CF3 → Sol cross-family review (XF-1–XF-11) → Entry 81 narrowed claim → spec v2.2. The full eight-document chain accompanies this spec to the external human reviewer **before fresh-seed scoring** (recommended sequencing, §12).

---

## §11 Principal gate items (all rulings required before pre-registration freeze)

| # | Item | Decision |
|---|---|---|
| G1 | Interpretive: "regulation" = loop-closure reading; narrowed claim adopted | RESOLVED — Entry 81 `[Entry 81]` |
| G2 | Regulation-error definition: hinge for baseline gate, signed deviation for trend bars; W=50; ε_gate | Ruling on locked-bar terms `[PROPOSED — requires Rebecca sign-off]` |
| G3 | Battery size, IF power analysis (§8.1) shows false-kill > threshold | 200 / escalated size `[PROPOSED]` |
| G4 | C_min and η (+ bounds), selected from the §8 sensitivity map's informative region via deterministic selection rule | Constants (selected per §8 XF-9 rule) `[PROPOSED — requires Rebecca sign-off]` |
| G5 | CF1 riders: memory-arm mechanism prediction + pre-committed boundary-condition classification (§6.4) + three-control panel (§6.2, §6.3) | Ratify verbatim `[Entry 81]` |

---

## §12 Sequencing (binding order)

1. This spec v2.2 → **fresh-context CRITIC** review (input: this spec + the full eight-document chain, per §10.5 — review starts from the objections, briefed to verify closure of XF-4–XF-9 and CF riders, not to re-litigate settled XF-1/2/3).
2. §8 power analysis + sensitivity map produced (candidate-blind, per §8 XF-9 protocol).
3. **Principal gate:** G2–G5 ruled with §8 artifacts in hand (G1 resolved by Entry 81).
4. §4 L7/L10 reconciliation check documented; any delta → review cycle.
5. Pre-registration freeze (L19): all `[PROPOSED]` values resolved, appendix committed, hash-attested.
6. TASK BUILDER released for L8 implementation.
7. **External human review of the L8 design chain (recommended before any fresh-seed exposure)** — L8 is the constitution's most philosophically loaded law; a design flaw found post-scoring costs unrecoverable seeds.
8. Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

---

*Every `[PROPOSED]` tag is a number offered for ruling, not a decision made. Per the CRITIC's standing distinction: this document specifies constructs; the TASK BUILDER receives no design decisions. The narrowed claim (Entry 81) is a P5-authorized interpretive ruling — the deviation from broader constitutional L8 language is memorialized with Rebecca's sign-off.*
