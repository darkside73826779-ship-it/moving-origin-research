# L8 INSTANTIATION SPECIFICATION v2.7.1 — Selective-Risk Homeostat (Rebecca-Cleared Feasibility Execution)

**Component:** M4 / L8 (Stakes coupling) + L14 couplings
**Author:** ARCHITECT (implementing Rebecca's advisor-session proposal per Entry 81 + Sol cross-family review XF-4–XF-9 resolution conditions)
**Status:** v2.7.1 — Rebecca cleared staged diagnostic implementation/execution under the merged 1,000-repetition authorization; G2–G4 not frozen and screening not released
**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Sources:** Entry 81 (narrowed claim) `[Entry 81]`; Sol cross-family review (XF-4–XF-9, XF-10–XF-11) `[Sol-XF-n]`; advisor proposal v2; CRITIC re-review CF1–CF3; `[LAW-L8]` `docs/ARCHITECTURAL_CONSTITUTION_v2.md` line 28; `[LAW-L14]` line 42; `[BAR-Entry 11]` M0 sheet; Ruling 3 + Ruling 9 (Entry 76) `[Entry 76]`
**Standing constraints inherited:** O-14, O-15, §5 P1–P6, L19 pre-registration, Ruling 9 candidate-blindness. Nothing in this spec authorizes scoring, protected-seed exposure, the 10,000-simulation stress rerun, G2–G4 freeze, final L8 scoring implementation, or merger.

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

**Zero-variance behavior (v2.3 correction):** If `σ_pool,s = 0` in an ordinary candidate or control observation, `β*_s` is undefined and that seed does not clear the trend verdict; it is an ordinary statistical FAIL, not INSTRUMENT FAILURE. INSTRUMENT FAILURE is available only when an independent apparatus-validity check in §8.6 demonstrates a fault. `[PROPOSED — remediation operationalization]`

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

6. **Disposition on independent pre-candidate validation:** If the synthetic-reference calibration metric fails monotonicity or minimum potency before any candidate/control observation, the independent apparatus check fails and the outcome is **INSTRUMENT FAILURE**. The same statistical pattern in an ordinary seed is not reclassified and follows §8.6. `[PROPOSED — v2.3 clarification of Sol-XF-8]`

7. **No candidate-output tuning:** Doses are never tuned from candidate outputs. The `σ_ℓ` values are fixed from v_ref and frozen before scoring. `[Sol-XF-8]` `[Entry 76]`

---

## §6 Specificity arms — three-control panel (closes C4; advisor-BF5; CRITIC-CF1; XF-6; Entry 81)

Per Entry 81, the specificity test is expanded from one control to a **pre-registered three-control panel**. The "and only then" is operationalized as specificity relative to this panel. `[Entry 81]`

### §6.1 Memory perturbation (existing control)

**Component:** the memory store (world-mapping vs self-mapping contrast per the law's Damasio/Seth lineage — now demoted to motivation per Entry 81).
**Perturbation:** seeded corruption of retrieved content at severity-matched doses. Severity matching per Ruling 3: memory dose at level ℓ is matched to mirror dose ℓ by **equal standardized effect on the component's own output** — retrieval-fidelity degradation on oracle-answerable queries, standardized by its Level-0 SD from synthetic profiles. Matching tolerance: `[PROPOSED]` ±0.25 standardized units, pre-registered. `[Entry 76]`

**Potency bar (BF5 — mandatory):** at every level ℓ ≥ 1, the matched memory dose must degrade raw retrieval fidelity by ≥ `[PROPOSED]` 0.5 standardized units. Failure on an independent pre-candidate synthetic apparatus fixture is INSTRUMENT FAILURE; failure in an ordinary arm/seed is a statistical FAIL and is not reclassified. `[PROPOSED — v2.3 disposition]`

### §6.2 Feedback-channel perturbation (new control, per Entry 81)

**Component:** the per-window outcome-feedback channel (§4).
**Perturbation:** seeded corruption of feedback labels — a pre-registered fraction of per-window correctness signals are flipped. Dose levels: Level 0 (no corruption), Levels 1–3 at feedback-corruption rates `[PROPOSED]` {0.1, 0.2, 0.4} (10%, 20%, 40% of feedback labels flipped). `[Entry 81]` `[PROPOSED — requires Rebecca sign-off]`

**Rationale (Entry 81):** If the regulation error rises specifically when the self-model (not the feedback channel) is degraded, then corrupting feedback should NOT produce a dose-dependent rise in regulation error. This control tests whether the homeostat responds to self-model quality specifically or to any information-channel degradation.

**Potency bar:** at every level ℓ ≥ 1, the feedback corruption must produce a measurable effect on the system's threshold adaptation: mean |τ_drift_ℓ| ≥ 0.02 (threshold drift exceeding 0.02 in absolute value across windows at dose ℓ). `[PROPOSED — apparatus parameter]` `[LAW-L19]` Failure on an independent pre-candidate synthetic apparatus fixture is INSTRUMENT FAILURE; ordinary arm/seed failure is statistical FAIL. `[PROPOSED — v2.3 disposition]`

### §6.3 Task-difficulty shift (new control, per Entry 81)

**Component:** the query battery itself.
**Perturbation:** shift the task-difficulty distribution of the query battery. Level 0: standard difficulty. Levels 1–3: progressively harder query distributions constructed deterministically by increasing the mean retrieval-chain length: Level 1 = 1.5× standard chain length, Level 2 = 2× standard chain length, Level 3 = 3× standard chain length. Chain length is the number of hops in the retrieval task; longer chains are harder. The difficulty construction is deterministic and pre-registered against oracle-graded synthetic profiles. `[Entry 81]` `[PROPOSED — apparatus parameter]` `[LAW-L19]`

**Rationale (Entry 81):** If the regulation error rises specifically when the self-model is degraded, then merely making the task harder should NOT produce a dose-dependent rise in regulation error that matches the self-model arm's pattern. Harder tasks may raise absolute error rates, but the *regulation* (deviation from R*) should not show the same dose-dependent trend as self-model degradation.

**Potency bar:** at every level ℓ ≥ 1, the task-difficulty shift must produce a measurable change in baseline difficulty: oracle accuracy on the battery drops by ≥ 0.05 (5 percentage points) relative to Level 0. `[PROPOSED — apparatus parameter]` `[LAW-L19]` Failure on an independent pre-candidate synthetic apparatus fixture is INSTRUMENT FAILURE; ordinary arm/seed failure is statistical FAIL. `[PROPOSED — v2.3 disposition]`

### XF-6 resolution — Specificity estimand, interval, conjunction for PASS

**v1 defect:** The specificity test did not specify whether the memory slope was raw or standardized, how CIs were constructed, confidence level, sampling unit, seed aggregation, direction of exclusion, or the complete conjunction for PASS.

**v2 estimand (XF-6 closure):**

**Estimand:** For each control arm (memory, feedback, task-difficulty), compute the **slope difference**: `Δβ_s = β*_s(candidate arm) − β*_s(control arm)`, where `β*` is the standardized slope (§2 XF-5 estimator). Both arms use the same estimator, same dose levels, same window structure — slopes are in the same units. `[Sol-XF-6]`

**Direction of exclusion:** The control arm's slope must be excluded from the candidate arm's slope by a pre-registered margin. Specifically: `Δβ_s > 0` for all seeds AND `pooled bootstrap 95% CI of Δβ` excludes zero. The candidate arm's dose-response must be significantly steeper than each control arm's. `[Sol-XF-6]`

**Seed aggregation:** 5 seeds, all-seeds-direction + pooled paired-bootstrap 95% CI (matching the M0 Entry 11.3 fallback policy for direction tests). `[BAR-Entry 11.3]`

**Interval method:** pooled paired-bootstrap (5,000 resamples, seed-level pairing), 95% CI, two-sided. `[PROPOSED — apparatus parameter]`

**Missing/degenerate cases (v2.3 correction):** If a control arm's `σ_pool,s = 0`, that seed fails the applicable statistical condition. It is not INSTRUMENT FAILURE absent an independently established §8.6 apparatus fault. `[PROPOSED — remediation operationalization]`

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

## §8 G2–G4 remediation protocol — verdict alignment, battery sweep, and deferred selection

### 8.1 Exact L8 trend verdict and primary estimand

The governing verdict is **all-seeds independently passing, plus the pooled interval condition**; it is not a five-seed-mean threshold. Entry 11.3 states “Seeds raised to 5 for L7, L8, L15, with the all-seeds-direction + bootstrap-CI fallback.” `[BAR-Entry 11.3]` The committed M4 specification and task specification implement this as a KILL when the dose-response is non-monotonic on any seed and require all-seed direction. The L8 v2.2 statement that the locked Spearman and standardized-slope bars run “per seed” remains controlling. `[BAR-Entry 11]` `[BAR-Entry 11.3]`

For every simulated five-seed run, the harness and power analysis SHALL execute the same complete trend predicate used by scoring:

1. compute `ρ_s` and `β*_s` separately for each of the five seeds;
2. require `ρ_s ≥ 0.8` for every seed `[BAR-Entry 11]`;
3. require `β*_s ≥ 0.2` for every seed `[BAR-Entry 11]`;
4. require positive dose-response direction on every seed and the pre-registered pooled bootstrap interval condition from Entry 11.3 `[BAR-Entry 11.3]`; and
5. count the simulated run as a false kill if any required trend predicate fails while the synthetic ground truth satisfies the pre-registered positive-effect profile. `[PROPOSED — power-analysis estimand]`

The **primary false-kill rate** is `number of valid simulated five-seed runs failing that complete verdict / number of valid simulated five-seed runs`. `[PROPOSED — G3 operating criterion]` The former five-seed-mean measure is retained as `diagnostic_false_kill_rate_mean_beta` and may not gate battery size or selection. `[PROPOSED — diagnostic only]`

The existing artifact's labels are corrected as follows: for each `(α,v,C_min,η)` combination, `false_kill_rate` is the fraction of repetitions whose mean `β*` across five seeds is below 0.2; `false_kill_rate_per_seed` is the fraction whose five-seed vector contains at least one `β*_s < 0.2`. A sensitivity-map cell is the arithmetic mean of the 15 corresponding per-combination rates across the five `α` values and three `v` multipliers. Thus the selected cell's reported 6.22% and 76.23% are both means across 15 decision-level rates; neither is a fraction of parameter combinations. The 76.23% measure is closer to the governing aggregation but remains incomplete because it omits `ρ` and the pooled interval. `[PROPOSED — verified diagnostic description]`

### 8.2 Candidate-blind battery-size sweep

The TASK BUILDER SHALL implement a synthetic/oracle-only sweep. Candidate outputs, candidate diagnostic seeds 101–105, protected seeds, and prior candidate results are forbidden inputs. `[OP-Entry 76]` (Ruling 9) All runs are O-15 diagnostic-only and cannot alter or excuse any prior result. `[BAR-Entry 52]` (O-14)

The locked dose requirement is preserved: four levels `{0,1,2,3}` remain; the sweep SHALL NOT reduce the number of noise doses below the locked minimum of three. `[BAR-Entry 11]`

Sweep geometry (all values proposed apparatus parameters):

- queries per window `W ∈ {50, 100, 200, 400}` `[PROPOSED]`;
- windows per dose `N_w ∈ {4, 8, 16, 32, 64}` `[PROPOSED]`;
- evaluate the Cartesian product, ordered by total queries per dose `Q = W × N_w`, then by larger `N_w`, then by smaller `W` `[PROPOSED]`;
- retain the v2.2 synthetic reference family, nuisance grid, five-seed grouping, identical estimator, and deterministic combo-derived simulation seeds `[PROPOSED]`; and
- use a staged Monte Carlo budget of 2,000 repetitions per combination for screening and 10,000 repetitions only for finalist geometries after aggregation is CRITIC-verified `[PROPOSED]`. This finalist confirmation is not the prohibited full sensitivity/misspecification stress rerun.

For every geometry, report the primary complete-verdict false-kill rate, its two-sided Wilson 95% interval, the mean-β diagnostic, each predicate-specific failure rate (`ρ`, `β*`, direction, pooled interval), instrument-failure count, and cost in queries per dose and per five-seed run. `[PROPOSED]`

Operational acceptance is the upper bound of the primary 95% interval below 0.10 `[PROPOSED]`; the preferred target is an upper bound below 0.05 `[PROPOSED]`. The minimum acceptable battery is the first geometry in the ordering above that meets the <0.10 criterion. If one or more geometries meet the preferred <0.05 criterion at the same minimum `Q`, restrict selection to those geometries. If no tested geometry meets <0.10, STOP and return the sweep to ARCHITECT/Rebecca; TASK BUILDER may not extend the grid or invent a battery. `[PROPOSED]`

### 8.3 Sensitivity-map classification reconciliation

The old “informative” boundary `false-kill < 0.50` is retired for operational selection. It allowed a cell with 43.22% false-kill to be called informative even though nearly half of true-positive runs would be killed. Such a cell may be statistically nondegenerate but is **operationally unacceptable**.

The recomputed map SHALL use four non-overlapping labels: `apparatus-invalid` when §8.6 fails; `operationally-unacceptable` when the primary false-kill interval upper bound is ≥0.10; `trivial-pass` when the pre-registered null false-pass boundary is met; and `operationally-informative` only when apparatus checks pass, the primary upper bound is <0.10, and the null false-pass boundary is not met. `[PROPOSED]` The <0.05 preferred subset is reported separately and does not silently replace the <0.10 acceptance criterion. `[PROPOSED]`

### 8.4 Deferred sensitivity map and `(C_min, η)` selection

No sensitivity map, misspecification stress map, or `(C_min,η)` selection may be recomputed in this remediation run. After Rebecca freezes (a) the all-seeds verdict aggregation and (b) the battery geometry, TASK BUILDER may run the existing candidate-blind nuisance grid at that frozen geometry, using the complete-verdict primary estimand and §8.3 labels. `[PROPOSED — sequencing gate]`

The later recomputation SHALL preserve the v2.2 grids `α ∈ {0.0,0.02,0.05,0.1,0.2}`, `v ∈ {0.5,1.0,2.0}×v_ref`, `C_min ∈ {0.5,0.6,0.7,0.8}`, and `η ∈ {0.01,0.05,0.1,0.2}`, plus the two misspecified profiles, unless Rebecca separately approves an amendment. `[PROPOSED — preserved apparatus grid]`

### 8.5 Pre-registered equivalence set and selector

Before the deferred recomputation, freeze the equivalence margin `δ_eq = 0.01` absolute false-kill probability `[PROPOSED]`. Let `p_i` be a cell's primary false-kill estimate and `CI_i` its two-sided Wilson 95% interval `[PROPOSED]`. Two operationally-informative cells are indistinguishable when `|p_i-p_j| ≤ δ_eq` **and** their 95% intervals overlap. `[PROPOSED]`

Construct the equivalence set from all operationally-informative cells indistinguishable from the cell with the lowest primary false-kill estimate. Do not rank within this set by sub-margin Monte Carlo noise. Select the highest `C_min` (strongest coverage requirement); if still tied, select the lowest `η` (most conservative controller). `[PROPOSED]` Report the complete equivalence set, estimates, intervals, and selected secondary criterion. If the relation is non-transitive, use membership relative to the single lowest-rate reference cell rather than pairwise chaining. `[PROPOSED]`

More simulations narrow Monte Carlo uncertainty; they do not necessarily increase the estimated false-kill rate. The equivalence rule is frozen before the later recomputation and may not be fitted to observed cell ordering. `[PROPOSED]`

### 8.6 Exclusive INSTRUMENT FAILURE definition

INSTRUMENT FAILURE means an independently demonstrated apparatus fault, never an unfavorable candidate/control statistic. It is available only when at least one pre-registered check, run independently of the ordinary seed verdict, fails:

- known-answer label and oracle checksum validation fails `[PROPOSED]`;
- estimator validation on fixed synthetic fixtures fails its pre-registered expected-value/tolerance contract `[PROPOSED]`;
- RNG reproducibility differs between two executions of the frozen parallel scoring path after removal of the explicitly excluded timing field `[PROPOSED]`;
- the resolved configuration manifest or digest differs from the frozen aggregation, battery geometry, dose grid, seed manifest, or estimator version `[PROPOSED]`;
- artifact integrity fails (schema, completeness, atomic-write checksum, or parse validation) `[PROPOSED]`; or
- the pre-candidate synthetic dose/calibration apparatus fails its pre-registered convergence or potency validation `[PROPOSED]`.

An ordinary per-seed failure of `ρ`, `β*`, direction, interval, specificity, potency, baseline, or zero-variance behavior is a statistical FAIL/KILL under its applicable rule and SHALL NOT be reclassified. `[PROPOSED — no-relabeling rule]` Once a scoring failure exists, O-14/D1/D5 prohibit rerun, rescoring, or reframing it to avoid the negative. `[BAR-Entry 52]` (O-14) `[OP-Entry 12]` (D1/D5)

### 8.7 Failure-injection tests and complete diagnostic rehearsal

Before CRITIC review, TASK BUILDER SHALL add genuine automated tests with assertions and perform one candidate-blind diagnostic rehearsal covering:

1. **Incomplete output:** suppress a required section; assert schema failure, nonzero exit, no artifact promoted, and no success attestation. `[PROPOSED]`
2. **Corruption/partial write:** inject malformed JSON and a truncated temporary file; assert parse/checksum failure and preservation of the last complete artifact through atomic temp-file-then-rename publication. `[PROPOSED]`
3. **Nondeterminism:** run the same small synthetic fixture twice through the frozen parallel scoring path; after removing only `elapsed_seconds`, assert byte-identical canonical JSON and identical resolved seeds. `[PROPOSED]`
4. **Configuration mismatch:** separately alter aggregation, `W`, `N_w`, dose grid, and seed manifest; assert each digest mismatch fails closed before simulation begins. `[PROPOSED]`
5. **Crash recovery:** inject calibration worker and identity failures; assert `CalibrationWorkerError`/`CalibrationIdentityError` route to exit code 1, no partial result table is published, no post-calibration simulation executes, and a later fresh diagnostic invocation starts from the frozen manifest rather than silently resuming partial state. `[PROPOSED]`

The rehearsal report SHALL list injected fault, expected assertion, observed exit/disposition, artifact path/hash, and pass/fail. No test may be a no-op, unconditional pass, or mock that bypasses the production error path. `[PROPOSED]`

### 8.8 Publication and prohibited computation

Publish code, simulation-seed derivation, frozen manifests, sweep table, uncertainty intervals, test results, and rehearsal report as committed diagnostic artifacts before any G2–G4 request. `[LAW-L19]` Do not run the prior full 10,000-simulation sensitivity/misspecification stress analysis until aggregation and battery size are frozen. No artifact from this cycle is scoring evidence. `[O-15]`

### 8.9 Deterministic implementation contract (v2.4 STOP closure)

This subsection resolves the TASK BUILDER STOP recorded against v2.3. Where §8.1–§8.8 is less specific, §8.9 controls. Every new value or mechanism below is `[PROPOSED]` and cannot gate scoring unless Rebecca approves it.

#### 8.9.1 Complete trend-verdict algorithms

For each seed, compute the four dose means `D_{s,ℓ}` in IEEE-754 binary64. Spearman `ρ_s` is the Pearson correlation of midranks: dose ranks are `(1,2,3,4)` and tied `D` values receive the arithmetic mean of their occupied one-based ranks. Sorting is ascending and stable; exact binary64 equality defines a tie. Compute covariance and variance with divisor four; the common divisor cancels in the correlation. If either rank vector has zero variance, `ρ_s` is undefined and the seed fails the Spearman predicate. `[PROPOSED — algorithm]`

“Positive dose-response direction” means the unstandardized OLS slope `β_s > 0` for every seed. `[PROPOSED — direction predicate]` This is reported independently even though `β*_s ≥ 0.2` normally implies it. No strict adjacent-increase predicate is added.

The pooled bootstrap statistic is `T = mean_s(β*_s)` across the five seeds. `[PROPOSED — bootstrap estimand]` Each bootstrap replicate independently resamples, with replacement, the `N_w` window deviations **within every `(seed,dose)` stratum**, preserving five seeds, four doses, and `N_w` observations per stratum. Recompute `D`, `σ_pool`, `β`, `β*`, then `T`. Do not resample seeds or pool windows across doses. `[PROPOSED — resampling rule]`

Use 5,000 valid bootstrap replicates, a two-sided 95% percentile interval, and endpoints at probabilities 0.025 and 0.975 using NumPy-style linear quantile interpolation `h=(n−1)q`, between `floor(h)` and `ceil(h)`. `[PROPOSED]` The bootstrap predicate passes only when the lower endpoint is strictly greater than zero. `[PROPOSED]` It does not require the lower endpoint to exceed 0.2; the locked 0.2 bar is applied per seed. `[BAR-Entry 11]`

Bootstrap RNG identity is derived as specified in §8.9.3 with namespace `bootstrap`, including the complete simulation identity and repetition index. If a bootstrap draw produces any undefined `β*`, discard that draw and deterministically continue through at most 5,500 attempted draws to obtain 5,000 valid draws. `[PROPOSED]` Failure to obtain 5,000 valid draws is an ordinary bootstrap-predicate failure, not INSTRUMENT FAILURE.

A simulated repetition enters the denominator whenever all independent apparatus checks pass. Undefined `ρ`, undefined `β*`, or an invalid/insufficient bootstrap sample counts as a false kill and remains in that denominator. Apparatus-invalid repetitions are excluded, counted, and reported separately; if any apparatus-invalid repetition occurs for a combination, that combination is `apparatus-invalid` and cannot qualify a geometry. `[PROPOSED]`

Predicate-specific false-kill rates are **overlapping marginal rates**: for each predicate, count every repetition in which it fails, irrespective of other failures, divided by the same valid-repetition denominator. Also report a bit-mask frequency table over all predicate-failure combinations; do not assign an exclusive “cause.” `[PROPOSED]`

#### 8.9.2 Sweep operating points, aggregation, calibration, and finalists

The screening sweep evaluates all 20 geometries from §8.2 at all 240 pre-registered cells: 15 `(α,v)` nuisance combinations times 16 `(C_min,η)` operating points. `[PROPOSED]` No old reference or selected operating point substitutes for this grid. This preserves G4 deferral.

For each geometry and each of its 240 cells, compute a separate complete-verdict false-kill estimate and Wilson interval. A geometry-level primary value is the **maximum cell-level Wilson upper endpoint**; geometry acceptance is the conjunction that all 240 upper endpoints are below 0.10. `[PROPOSED]` Preferred status is the conjunction that all 240 upper endpoints are below 0.05. `[PROPOSED]` Do not pool repetitions or average rates across cells for acceptance. Report arithmetic means and quantiles across cells as diagnostics only.

Use Wilson score intervals with `z = 1.959963984540054`, `n` equal to apparatus-valid repetitions, and the standard closed form `center=(p+z²/(2n))/(1+z²/n)`, `half=z/(1+z²/n)·sqrt(p(1−p)/n+z²/(4n²))`. `[PROPOSED]` Zero failures use the same formula without a special case. If `n=0`, the cell is apparatus-invalid. Intervals are cell-level; no interval is computed from averaged or pooled cell counts.

Re-run synthetic-reference `σ_dose` calibration independently for every `(W,N_w,α,v)` tuple. `[PROPOSED]` Calibration uses the existing fixed reference operating point `(C_min,η)=(0.7,0.1)` only to determine dose strength; that point is not used to judge battery acceptance. Calibration RNG identities include geometry. Cached calibration is permitted only when the full tuple and calibration-manifest digest match exactly.

After 2,000-repetition screening, finalist geometries are precisely the geometries satisfying the <0.10 conjunction. `[PROPOSED]` Restrict finalists to the smallest total queries per dose `Q`; if multiple remain, retain all tied geometries for 10,000-repetition confirmation. Preferred status does not remove an otherwise acceptable geometry unless tied at the same minimum `Q`, in which case retain preferred geometries only. If no geometry qualifies, there is no finalist and the process STOPS.

This implementation cycle, once Rebecca approves diagnostic compute, runs all 20 screening geometries. `[PROPOSED]` It does not run 10,000-repetition finalist confirmation. That confirmation requires the screening artifact, fresh-context CRITIC verification, and separate Rebecca authorization. It is distinct from—and does not authorize—the deferred full sensitivity/misspecification stress rerun.

#### 8.9.3 Configuration, serialization, identity, and seed manifests

The resolved configuration file is `diagnostics/l8_g2g4/resolved_config.json`. `[PROPOSED]` It is a JSON object with exactly these required top-level fields: `schema_version`, `artifact_date`, `regime`, `design_sha`, `implementation_sha`, `mode`, `aggregation`, `spearman`, `bootstrap`, `battery_geometries`, `dose_levels`, `n_seeds`, `nuisance_grid`, `operating_grid`, `calibration`, `screening_repetitions`, `wilson`, `instrument_checks`, `estimator_version`, and `seed_derivation`. Unknown fields fail schema validation. `[PROPOSED]`

Nested schemas are exact: `aggregation={primary,diagnostic,predicate_rates}`; `spearman={algorithm,tie_rule,undefined_rule,threshold}`; `bootstrap={statistic,resampling_strata,valid_replicates,max_attempts,confidence_level,interval_method,quantile_method,pass_rule}`; each `battery_geometries` entry is `{W,N_w}`; `nuisance_grid={alphas,v_mults}`; `operating_grid={c_mins,etas}`; `calibration={per_geometry,reference_c_min,reference_eta,cache_key_fields}`; `wilson={z,accept_upper_lt,preferred_upper_lt}`; `instrument_checks` is the ordered array of the six identifiers `{oracle_checksum,estimator_fixtures,rng_reproducibility,config_digest,artifact_integrity,dose_calibration}`; and `seed_derivation={hash,encoding,namespace_separator,integer_rule,identity_fields}`. `[PROPOSED]` Each object permits exactly the listed keys; scalar values must equal §8.9, and arrays preserve the stated order.

Set `schema_version="l8-g2g4-config-v1"`, `mode="diagnostic-screening"`, and `estimator_version="xf5-beta-star-v2.4"`. `[PROPOSED]` `design_sha` is the exact approved ARCHITECT commit; `implementation_sha` is the tested TASK BUILDER commit. Every numeric array is ordered exactly as written in §8.2 and §8.4.

Canonical JSON is UTF-8, Unicode NFC, sorted object keys, no insignificant whitespace, separators `(',',':')`, JSON booleans/null, finite numbers only, and one trailing LF. `[PROPOSED]` Digests use SHA-256 over these canonical bytes and lowercase hexadecimal. `[PROPOSED]` The configuration digest is stored in `diagnostics/l8_g2g4/resolved_config.sha256` as `<64-lowercase-hex><two spaces>resolved_config.json<LF>`. `[PROPOSED]`

Seed identity is `SHA256(UTF8-NFC(namespace + "\n" + canonical_json(identity_object)))`. `[PROPOSED]` The identity object contains `config_digest`, `W`, `N_w`, `alpha`, `v_mult`, `c_min`, `eta`, `repetition_index`, `seed_index`, and, when applicable, `bootstrap_attempt_index`. The executable RNG integer is the unsigned big-endian value of the first eight digest bytes modulo `2^63−1`. `[PROPOSED]`

Publish `diagnostics/l8_g2g4/seed_manifest.json` with `schema_version`, `derivation`, `config_digest`, and ordered `entries`; each entry contains the identity fields, full lowercase `seed_digest`, and derived integer labeled `synthetic_diagnostic_seed`. `[PROPOSED]` These are candidate-blind synthetic simulation seeds, not protected scoring seeds. No scoring-seed manifest or courier material is read or written.

#### 8.9.4 Output schemas and atomic publication

The screening artifact is `diagnostics/l8_g2g4/battery_sweep.json`; its checksum sidecar is `battery_sweep.sha256`. `[PROPOSED]` Required top-level fields are `schema_version`, `artifact_date`, `regime`, `design_sha`, `implementation_sha`, `config_digest`, `estimator_version`, `status`, `geometries`, `finalists`, `instrument_failure_count`, and `prohibitions`. `[PROPOSED]` `schema_version="l8-g2g4-sweep-v1"`. Each geometry contains exactly `W`, `N_w`, `queries_per_dose`, `queries_per_five_seed_run`, `screening_repetitions`, `status`, `max_wilson_upper`, `all_cells_below_0_10`, `all_cells_below_0_05`, `diagnostics`, and `cells`; `diagnostics={mean_primary_rate,median_primary_rate,p95_primary_rate,mean_mean_beta_diagnostic}`; and `cells` has exactly 240 ordered entries. Each cell contains exactly `W`, `N_w`, `alpha`, `v_mult`, `c_min`, `eta`, `attempted_repetitions`, `valid_repetitions`, `false_kill_count`, `primary_false_kill_rate`, `wilson_lower`, `wilson_upper`, `mean_beta_false_kill_rate`, `predicate_false_kill_rates`, `failure_mask_counts`, and `apparatus_invalid_count`. `[PROPOSED]` `predicate_false_kill_rates` has exactly `{spearman,beta_star,direction,bootstrap}`; `failure_mask_counts` maps four-bit strings in `0000..1111` to nonnegative counts, with bit order `(spearman,beta_star,direction,bootstrap)`.

Required completeness predicates are: exact schema; exact config digest; 20 unique geometries; 240 unique ordered cells per complete geometry; 2,000 attempted repetitions per cell; denominator plus apparatus-invalid count equals attempts; finite bounded rates/intervals; Wilson recomputation match within `1e-15`; geometry summaries recompute exactly from cells; finalists recompute exactly from the rule; no unknown fields. `[PROPOSED]`

Publish atomically in the destination directory: write canonical bytes to `<filename>.tmp`, flush, call `fsync`, validate by re-reading, then replace the destination with a same-filesystem atomic rename. `[PROPOSED]` Never delete or truncate an existing complete destination before validation. On Windows use replace-existing atomic rename semantics; on POSIX use `os.replace`. A failed publication preserves the prior complete artifact, retains the invalid temp file by renaming it `<filename>.failed.<UTC-basic-timestamp>.<sha256-prefix>`, and exits per §8.9.5. `[PROPOSED]` The sidecar is produced only after the JSON replacement succeeds, using the same atomic protocol. A sidecar mismatch makes the artifact incomplete; it does not destroy the last known-good pair.

#### 8.9.5 Production-path faults, exceptions, exits, and recovery

Production code SHALL expose one internal dependency object `DiagnosticFaultHooks`, defaulting to no faults; tests inject hook implementations directly. `[PROPOSED]` No public CLI fault flags or environment-variable backdoors are permitted. Hooks exist only at named production boundaries: `after_calibration`, `before_artifact_section`, `after_temp_write`, `before_parallel_collect`, and `before_atomic_replace`. Test-only hook implementations live under `tests/` and are unreachable from the production CLI.

Exception/exit contracts are: `DiagnosticSchemaError` exit 20; `DiagnosticChecksumError` exit 21; `DiagnosticConfigMismatchError` exit 22; `DiagnosticNondeterminismError` exit 23; existing `CalibrationWorkerError` or `CalibrationIdentityError` exit 1; unexpected exceptions exit 70. `[PROPOSED]` Every failure writes one structured diagnostic to stderr, publishes no new success artifact or success attestation, and leaves the prior complete artifact untouched.

Crash recovery applies only to candidate-blind synthetic diagnostic invocations and is not a rerun of candidate/scoring evidence. `[PROPOSED]` O-14 remains absolute for scoring runs. A fresh diagnostic invocation validates the frozen manifest, ignores all `.tmp` and `.failed.*` files as inputs, preserves them for audit, and recomputes from repetition zero; no partial simulation state or counts are resumed. `[PROPOSED]` Existing complete artifacts may be replaced only after a new complete artifact validates under the identical approved config digest; replacement is recorded in the rehearsal report. No partial file is silently deleted or overwritten.

#### 8.9.6 Independent apparatus fixtures and rehearsal report

Independent checks use fixed synthetic fixtures committed under `tests/fixtures/l8_g2g4/`. `[PROPOSED]` `known_answers_v1.json` contains exactly 32 objects ordered by integer `i=0..31`: `{"item_id":"fixture-II","oracle_input":{"truth_bit":i mod 2},"expected_label":i mod 2}`, where `II` is zero-padded to two digits. `[PROPOSED]` The oracle production path consumes `oracle_input` and must return `expected_label`. The check canonicalizes the ordered projected list `[{"item_id":"fixture-II","label":i mod 2}, ...]` with the §8.9.3 rules; its expected SHA-256 is `a38ba6a7b6236be756a318cfbab5e97b3c616882d65f8b6bce6452be7d62a141`. `[PROPOSED]` The estimator fixtures are the §2 positive and zero-slope fixtures, evaluated under the already specified tolerances. Dose validation uses the synthetic reference mirror and requires the existing monotonicity/potency conditions before candidate/control observations. `[PROPOSED]`

Configuration mismatch tests mutate, one at a time, `aggregation`, `W`, `N_w`, dose levels, seed derivation, and estimator version after digest creation; each must raise `DiagnosticConfigMismatchError` before calibration or simulation. `[PROPOSED]` Artifact completeness uses every predicate in §8.9.4. Serial/parallel comparison canonicalizes complete small-fixture result objects after removing exactly the top-level `elapsed_seconds` field; byte equality, config digest equality, ordered seed-manifest equality, and checksum equality are required. `[PROPOSED]`

The rehearsal artifact is `diagnostics/l8_g2g4/diagnostic_rehearsal.json` with sidecar `diagnostic_rehearsal.sha256`. `[PROPOSED]` Required fields are `schema_version`, `artifact_date`, `regime`, `design_sha`, `implementation_sha`, `config_digest`, `fixture_digests`, `overall_status`, and ordered `cases`. Each case contains exactly `case_id`, `injected_boundary`, `expected_exception`, `expected_exit_code`, `observed_exception`, `observed_exit_code`, `assertions`, `prior_artifact_digest`, `result_artifact_digest`, `preserved_files`, and `status`. `[PROPOSED]` Each `assertions` entry is exactly `{assertion_id,expected,observed,status}`; `preserved_files` is an ordered array of relative repository paths; digests are lowercase SHA-256 hex or JSON null when no artifact exists. Required `case_id` values are ordered as `incomplete_output`, `malformed_json`, `truncated_temp`, `parallel_repeatability`, `aggregation_mismatch`, `W_mismatch`, `N_w_mismatch`, `dose_grid_mismatch`, `seed_manifest_mismatch`, `estimator_version_mismatch`, `calibration_worker_crash`, and `calibration_identity_crash`. `[PROPOSED]` `overall_status="PASS"` only when every required case passes every assertion; otherwise it is `FAIL`. Publication follows §8.9.4.

#### 8.9.7 Repository routing

TASK BUILDER creates `taskbuilder/l8-g2g4-diagnostic-remediation` from the approved ARCHITECT v2.5 result SHA. `[PROPOSED — branch routing]` It imports `diagnostics/l8_power_analysis.py` from `b1397498ca369067e956479e6c2bd6b0793c3e89` as the executable implementation baseline; `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3` is read-only historical result context and is not copied forward as a new result. `[PROPOSED]` If either source path/blob differs from the reviewed SHA, STOP. The TASK BUILDER changes only diagnostic code, tests/fixtures, and `diagnostics/l8_g2g4/` artifacts authorized here; it does not modify the ARCHITECT specification.

### 8.10 v2.5 determinism and feasibility amendment

This subsection supersedes conflicting or incomplete text in §8.2 and §8.9. It closes the second TASK BUILDER STOP. All mechanics remain `[PROPOSED]` pending CRITIC review and Rebecca approval.

#### 8.10.1 Bootstrap RNG and seed-manifest scope

Each bootstrap attempt uses **20 independent RNG streams**, one for every `(seed_index,dose_index)` stratum. `[PROPOSED]` `seed_index` is the integer `0..4`; `dose_index` is the integer `0..3`; both are required in the bootstrap identity object. The identity is `{config_digest,W,N_w,alpha,v_mult,c_min,eta,repetition_index,seed_index,dose_index,bootstrap_attempt_index}` with namespace `bootstrap`. Each stream draws exactly `N_w` indices uniformly with replacement from `0..N_w−1`. No replicate-level shared RNG exists.

The seed manifest does not enumerate individual simulation, calibration, or bootstrap seeds. Its exact schema is `{schema_version,derivation,config_digest,simulation_derivation_roots,calibration_derivation_roots,bootstrap_derivation_roots}` with no unknown fields and `schema_version="l8-g2g4-seeds-v2"`. `[PROPOSED]`

- `derivation={hash:"sha256",encoding:"utf-8-nfc",canonicalization:"json-sorted-compact-lf-v1",namespace_separator:"LF",integer_rule:"first-8-bytes-big-endian-mod-2^63-minus-1"}`.
- Each `simulation_derivation_roots` item is `{W,N_w,alpha,v_mult,c_min,eta,root_digest,repetition_index_range,seed_index_range}` with `repetition_index_range=[0,1999]` and `seed_index_range=[0,4]`. `root_digest` hashes the identity with the varying indices replaced by those literal ranges.
- Each `calibration_derivation_roots` item is `{W,N_w,alpha,v_mult,root_digest,pilot_repetition_index_range,seed_index_range}` with `pilot_repetition_index_range=[0,999]` and `seed_index_range=[0,4]`.
- Each `bootstrap_derivation_roots` item is `{W,N_w,alpha,v_mult,c_min,eta,repetition_index,root_digest,attempt_range,seed_index_range,dose_index_range}` where `attempt_range=[0,5499]`, `seed_index_range=[0,4]`, and `dose_index_range=[0,3]`. `root_digest` hashes the identity with the three varying indices replaced by those literal ranges. Every individual seed remains reproducible from the published rule without a manifest containing millions or billions of rows. `[PROPOSED]`

#### 8.10.2 Exact resolved-config values

The following literal values are mandatory:

- `aggregation={primary:"complete-five-seed-verdict-false-kill",diagnostic:"mean-beta-star-below-0.2",predicate_rates:"overlapping-marginal-with-four-bit-mask"}`;
- `spearman={algorithm:"pearson-correlation-of-ascending-midranks-binary64",tie_rule:"exact-binary64-equality-average-one-based-ranks",undefined_rule:"statistical-fail-retained-in-denominator",threshold:0.8}`;
- `bootstrap={statistic:"mean-five-seed-beta-star",resampling_strata:"independent-within-seed-dose",valid_replicates:5000,max_attempts:5500,confidence_level:0.95,interval_method:"two-sided-percentile",quantile_method:"linear-h-equals-n-minus-1-times-q",pass_rule:"lower-endpoint-strictly-greater-than-zero"}`;
- `calibration={per_geometry:true,reference_c_min:0.7,reference_eta:0.1,cache_key_fields:["config_digest","W","N_w","alpha","v_mult","estimator_version","calibration_algorithm_version"]}`;
- `seed_derivation={hash:"sha256",encoding:"utf-8-nfc",namespace_separator:"LF",integer_rule:"first-8-bytes-big-endian-mod-2^63-minus-1",identity_fields:["config_digest","W","N_w","alpha","v_mult","c_min","eta","repetition_index","seed_index","dose_index","bootstrap_attempt_index"]}`. Fields inapplicable to a namespace are omitted, never null.

`battery_sweep.prohibitions` is the ordered array `[
"diagnostic-only-o15",
"no-candidate-data",
"no-protected-seeds",
"no-scoring",
"no-g2-g4-freeze",
"no-10000-confirmation",
"no-sensitivity-or-misspecification-rerun",
"no-merge-authority"
]`. `[PROPOSED]`

#### 8.10.3 Status vocabulary and apparatus-failure routing

Top-level sweep `status` is exactly one of `COMPLETE`, `NO_FINALIST`, or `ABORTED`; only `COMPLETE` and `NO_FINALIST` may be published as evidence artifacts. Geometry `status` is exactly `ACCEPTABLE`, `PREFERRED`, or `REJECTED`. Cell `status` is exactly `VALID` or `APPARATUS_INVALID`. `[PROPOSED]` Assignment rules: a valid geometry is `PREFERRED` when all cell upper bounds are below 0.05, else `ACCEPTABLE` when all are below 0.10, else `REJECTED`; any apparatus-invalid cell makes its geometry `REJECTED`. A successful sweep with at least one finalist is `COMPLETE`; a successful sweep with none is `NO_FINALIST`. `ABORTED` is stderr/rehearsal vocabulary only and is never promoted as `battery_sweep.json`.

All six apparatus checks are run-level, not repetition-level:

1. `oracle_checksum`: at process startup, run the 32 known-answer fixtures through the production oracle and compare the projected-list digest exactly.
2. `estimator_fixtures`: immediately after oracle validation, run the fixed positive/zero fixtures and require their existing tolerances.
3. `config_digest`: before calibration, schema-validate canonical bytes, recompute the config digest, and compare the sidecar and CLI-supplied expected digest.
4. `dose_calibration`: before screening each geometry, complete and validate all 15 calibration entries under §8.10.4.
5. `rng_reproducibility`: before full screening, execute the specified small fixture twice through the frozen parallel path and require canonical byte equality.
6. `artifact_integrity`: after staging and before promotion, enforce every completeness/checksum predicate and re-read both staged files.

Failure of checks 1–5 aborts the whole invocation before evidence publication; failure of check 6 aborts promotion and restores/preserves the prior pair. `[PROPOSED]` No published successful artifact may contain an apparatus-invalid repetition, so every published cell has `apparatus_invalid_count=0` and `valid_repetitions=attempted_repetitions`. `instrument_failure_count` is zero in published sweep evidence. Apparatus failures appear only in stderr and the rehearsal artifact. The `APPARATUS_INVALID` cell status is reserved for an in-memory aborted record used by tests; it cannot appear in promoted evidence. Ordinary undefined/statistical outcomes remain false kills, not apparatus failures.

#### 8.10.4 Generalized calibration and cache contract

Generalize the reviewed baseline algorithm without changing its numerical constants. For each `(W,N_w,alpha,v_mult)`, use 1,000 five-seed pilot repetitions at `(C_min,eta)=(0.7,0.1)`, target mean `β*=0.3`, tolerance `0.01`, search interval `[0.0001,12.0]`, and at most 40 bisection iterations. `[PROPOSED]` Simulation and estimator logic are identical to screening except for the pilot count and reference operating point. Evaluate the high endpoint first and clamp high if below target; evaluate low and clamp low if at/above target; otherwise bisect, returning the first midpoint within tolerance or the final midpoint after 40 iterations. Every evaluation reuses the same geometry-aware pilot seed identities (common random numbers across sigma values).

Calibration seed namespace is `calibration`; identity is `{config_digest,W,N_w,alpha,v_mult,pilot_repetition_index,seed_index}`. No `c_min`, `eta`, dose index, or bootstrap index is present. `[PROPOSED]`

Cache path is `diagnostics/l8_g2g4/cache/<config_digest>/calibration_manifest.json` with sidecar `calibration_manifest.sha256`. `[PROPOSED]` Exact top-level schema is `{schema_version,config_digest,estimator_version,calibration_algorithm_version,entries}`; fixed values are `schema_version="l8-g2g4-calibration-v1"`, `estimator_version="xf5-beta-star-v2.4"`, and `calibration_algorithm_version="geometry-bisection-v1"`. Each of the 300 ordered entries contains exactly `{W,N_w,alpha,v_mult,sigma_dose,termination,iterations,final_mean_beta_star,seed_root_digest}`. `termination` is one of `CLAMP_HIGH`, `CLAMP_LOW`, `WITHIN_TOLERANCE`, or `MAX_ITERATIONS`. The manifest and sidecar use §8.9.3 canonicalization/digest rules.

Cache reuse requires schema validity, sidecar match, exact config/estimator/algorithm identity, exactly 300 unique ordered entries, finite sigma values in range, permitted termination, and recomputed seed-root equality. Any mismatch raises `DiagnosticConfigMismatchError` before screening; no partial cache is used. Cache publication uses the pair transaction in §8.10.6.

#### 8.10.5 Exact rehearsal fixtures and injection mapping

`fixture_digests` is exactly `{known_answers_v1,estimator_positive_v1,estimator_zero_v1,parallel_repeatability_v1}`, each value lowercase SHA-256 hex. `[PROPOSED]`

The twelve rehearsal cases use the following fixed setup. Before each case, copy a committed valid small-fixture artifact pair into an isolated temporary directory as the prior pair; `prior_artifact_digest` is its JSON digest. Expected/observed scalar values are JSON strings, numbers, booleans, or null; compound values are canonical JSON strings. `preserved_files` lists relative paths in lexical order. `[PROPOSED]`

| case_id | injected boundary/method | assertion IDs | expected exception / exit | required preservation |
|---|---|---|---|
| incomplete_output | hook `before_artifact_section` omits `finalists` | `schema_reject`, `no_promote`, `prior_pair_equal` | `DiagnosticSchemaError` / 20 | prior JSON+sidecar, failed temp |
| malformed_json | hook `after_temp_write` replaces final byte with `{` | `parse_reject`, `no_promote`, `prior_pair_equal` | `DiagnosticSchemaError` / 20 | prior pair, failed temp |
| truncated_temp | hook `after_temp_write` truncates at half length | `parse_reject`, `no_promote`, `prior_pair_equal` | `DiagnosticSchemaError` / 20 | prior pair, failed temp |
| parallel_repeatability | hook `before_parallel_collect` reverses one result in the second parallel execution | `byte_mismatch`, `seed_order_mismatch`, `no_screen` | `DiagnosticNondeterminismError` / 23 | prior pair only |
| aggregation_mismatch | validator input mutates `aggregation.primary` after digest | `digest_mismatch`, `before_calibration` | `DiagnosticConfigMismatchError` / 22 | prior pair only |
| W_mismatch | validator input mutates first geometry `W` after digest | `digest_mismatch`, `before_calibration` | same / 22 | prior pair only |
| N_w_mismatch | validator input mutates first geometry `N_w` after digest | same IDs | same / 22 | prior pair only |
| dose_grid_mismatch | validator input mutates `dose_levels` after digest | same IDs | same / 22 | prior pair only |
| seed_manifest_mismatch | validator input changes first seed digest | `seed_digest_mismatch`, `before_calibration` | same / 22 | prior pair only |
| estimator_version_mismatch | validator input changes estimator version | `version_mismatch`, `before_calibration` | same / 22 | prior pair only |
| calibration_worker_crash | hook `after_calibration` raises worker error before manifest promotion | `exit_one`, `no_screen`, `no_promote` | `CalibrationWorkerError` / 1 | prior pair, failed calibration temp |
| calibration_identity_crash | hook `after_calibration` duplicates one identity before validation | `identity_reject`, `exit_one`, `no_screen` | `CalibrationIdentityError` / 1 | prior pair, failed calibration temp |

Validator-input mutation is dependency injection into the production validator, not a CLI flag or environment backdoor. The five hook boundaries remain the only executable fault hooks; cases that test validators call production validators with mutated in-memory inputs and need no hook.

#### 8.10.6 Transactional JSON-plus-sidecar publication

Treat JSON and sidecar as one recoverable pair under an exclusive destination lock. `[PROPOSED]` Stage and validate both `.tmp` files first. If a prior complete pair exists, atomically rename JSON and sidecar to `.previous.json` and `.previous.sha256` under the lock. Promote staged JSON, then staged sidecar. Re-read and validate the promoted pair. Only after success rename prior files to timestamped audit backups; do not delete them.

If any operation fails after either prior file moved or new JSON promoted, restore both prior files with `os.replace` while holding the lock, move every new/staged file to `.failed.<UTC-basic-timestamp>.<sha256-prefix>`, re-read the restored pair, then raise the applicable exception. If restoration itself fails, raise `DiagnosticChecksumError` exit 21, retain all files, and emit `manual_recovery_required=true`; no complete-artifact attestation is emitted. With no prior pair, remove nothing: quarantine all staged/promoted fragments and leave the canonical destinations absent.

#### 8.10.7 Implementation/evidence commit lifecycle

The implementation/evidence lifecycle is defined exclusively by §8.11.1 (A1 implementation, A2 frozen configuration, then evidence). `[PROPOSED]`

#### 8.10.8 Feasibility gate — screening authorization withdrawn pending benchmark

The full design entails 20 geometries × 240 cells × 2,000 repetitions = 9.6 million cell repetitions and, absent short-circuiting, 48 billion **valid** bootstrap replicates or up to 52.8 billion bootstrap **attempts** at the 5,500-attempt ceiling. `[PROPOSED — workload accounting]` This is materially larger than the reviewed baseline and is not authorized merely because “2,000-repetition screening” was previously stated.

Commit A1 must include a deterministic feasibility benchmark mode that runs **no scientific screening**: the 1,000 repetitions allocated in §8.12.1 across the three fixed cells `(alpha,v_mult,C_min,eta)={(0.0,0.5,0.5,0.01),(0.05,1.0,0.7,0.1),(0.2,2.0,0.8,0.2)}` and geometries `(W,N_w)=(50,4)` and `(400,64)`, with the full 5,000-valid-bootstrap verdict. `[PROPOSED — Rebecca-authorized diagnostic workload]` Report wall time, CPU time, peak memory, bootstrap attempts, and deterministic extrapolations for the 9.6-million-repetition screen. This benchmark is O-15 synthetic diagnostic rehearsal, not battery evidence.

Route the benchmark and implementation review to fresh-context CRITIC and Rebecca. Rebecca must then separately choose one of: authorize the full screen; approve an amended sequential/reduced design; or stop. `[PROPOSED — feasibility gate]` Until that ruling, TASK BUILDER may implement and test Commit A only; it may not execute the 2,000-repetition screen, create Commit B screening evidence, or describe screening as authorized.

### 8.11 v2.6 Commit identity and parallel feasibility-benchmark contract

This subsection supersedes conflicting lifecycle and benchmark text in §8.9.7, §8.10.5, §8.10.7, and §8.10.8. All mechanics are `[PROPOSED]` pending CRITIC review and Rebecca approval.

#### 8.11.1 Non-self-referential commit lifecycle

TASK BUILDER uses three stages:

1. **Commit A1 — implementation:** code, tests, and fixtures only; no `resolved_config.json` and no generated evidence.
2. **Commit A2 — frozen configuration:** adds `resolved_config.json` and its sidecar only. Its `implementation_sha` is Commit A1's full Git SHA; its `config_parent_sha` is also Commit A1's full SHA. Commit A2 makes no code/test/fixture change. `config_commit_sha` is not stored inside the config.
3. **Commit B — evidence:** generated rehearsal/benchmark artifacts and handoff only. Every artifact stores `implementation_sha=A1`, `config_digest` from A2, and `config_source_sha=A2`. Commit B makes no implementation or configuration change.

CRITIC verifies that `git diff A1..A2` contains only the frozen config pair and that `git diff A2..B` contains only authorized evidence/handoff files. Any implementation change after A1 or configuration change after A2 invalidates the evidence and requires new staged commits. `[PROPOSED]`

#### 8.11.2 Parallelism parity — no serial benchmark or serial reproducibility pass

Benchmark and reproducibility checks use the same multiprocessing contract intended for screening and scoring: `backend="multiprocessing.Pool"`, `start_method="spawn"`, `chunksize=1`, and `worker_count=min(32,logical_cpu_count)`, where `logical_cpu_count=os.cpu_count()` and a null or value below one is a configuration failure. `[PROPOSED]` The resolved integer is frozen in `resolved_config.parallelism={mode:"scoring-parity",backend:"multiprocessing.Pool",start_method:"spawn",chunksize:1,logical_cpu_count:<resolved>,worker_count:<resolved>}`. Screening and scoring must use that frozen worker count unless Rebecca approves a later amendment.

No serial feasibility benchmark is run. The former cross-mode reproducibility check is superseded by **parallel repeatability**: execute the same small fixture twice through the frozen multiprocessing path and require byte-identical canonical results after removing exactly `elapsed_seconds`. `[PROPOSED]` The rehearsal `case_id` is `parallel_repeatability`; inject the mismatch at `before_parallel_collect` on the second parallel execution. All other assertions and exit 23 remain.

#### 8.11.3 Benchmark inputs, RNG, and calibration timing

The benchmark contains the six fixed cases formed by geometries `(50,4)` and `(400,64)` crossed with the three sentinel cells already specified in §8.10.8. Case repetition counts are exactly the §8.12.1 allocation and sum to 1,000; every repetition includes up to 5,500 bootstrap attempts through the frozen multiprocessing path. `[PROPOSED — Rebecca-authorized diagnostic workload]`

Benchmark simulation RNG namespace is `feasibility-benchmark`; identity is `{config_digest,W,N_w,alpha,v_mult,c_min,eta,repetition_index,seed_index}`. Bootstrap streams retain namespace `bootstrap` but add `run_mode:"feasibility-benchmark"` to their identity. Calibration RNG namespace is `feasibility-calibration`; identity is `{config_digest,W,N_w,alpha,v_mult,pilot_repetition_index,seed_index}`. `[PROPOSED]`

Run six full, uncached geometry/nuisance calibrations—one for each benchmark case's `(W,N_w,alpha,v_mult)`—using §8.10.4. Calibration runs first and is timed/reported separately. Benchmark case timing excludes calibration and cache I/O but includes simulation, bootstrap, worker dispatch/collection, and result canonicalization. `[PROPOSED]` The six resulting sigma values are used only by their matching cases and are not promoted as the 300-entry screening cache.

#### 8.11.4 Time and memory measurement

Parent wall time uses `time.perf_counter_ns()` around the entire six-case parallel batch, including pool creation/destruction. `[PROPOSED]` Each worker returns `process_cpu_ns=time.process_time_ns(end)−time.process_time_ns(start)` for its assigned case. Parent CPU is measured by the same function around the batch. `total_process_tree_cpu_ns = parent_cpu_ns + sum(worker process_cpu_ns)`; no system-wide CPU time is used.

Peak memory is sampled aggregate resident-set size (RSS), not Python allocation peak. A parent sampler polls every 10 milliseconds from immediately before pool creation through pool join, using `psutil.Process(parent_pid).memory_info().rss` plus RSS for all recursive live children, deduplicated by PID. `[PROPOSED]` `peak_aggregate_rss_bytes` is the maximum sampled sum; `memory_sampling_interval_ms=10`; missing/disappeared processes contribute zero only after a second lookup confirms they exited. The benchmark records `psutil_version` and platform string. Failure to sample is `DiagnosticSchemaError` exit 20; no estimate substitutes.

#### 8.11.5 Deterministic extrapolation

Each worker reports `case_service_wall_ns` around its assigned case repetitions. For case `i` with fixed count `n_i` from §8.12.1, `service_seconds_per_repetition_i = case_service_wall_ns/(n_i×10^9)`. `[PROPOSED]` Let `s_max=max_i(service_seconds_per_repetition_i)`, `s_mean=mean_i(...)`, `B=parent_batch_wall_seconds`, `S=sum_i(case_service_wall_seconds)`, and `P=resolved worker_count`. Define observed parallel efficiency `E=min(1,S/(P×B))`; if `E≤0`, the benchmark fails schema validation.

Primary conservative screening projection is `projected_screen_wall_seconds = (9,600,000×s_max)/(P×E)`. `[PROPOSED]` Diagnostic central projection replaces `s_max` with `s_mean`. Calibration projection uses the six measured full-calibration service times: `projected_calibration_wall_seconds=(300×max_calibration_service_seconds)/(P×E)`. Total conservative projection is the sum of screening and calibration projections. No geometry weighting, six-case raw mean, or alternative extrapolation may be substituted.

#### 8.11.6 Exact benchmark artifact

Publish `diagnostics/l8_g2g4/feasibility_benchmark.json` with sidecar `feasibility_benchmark.sha256`. `[PROPOSED]` It uses §8.9.3 canonical JSON, SHA-256 sidecar format, schema/unknown-field rejection, and the transactional pair publication/restore rules of §8.10.6.

Top-level fields are exactly `{schema_version,artifact_date,regime,design_sha,implementation_sha,config_source_sha,config_digest,estimator_version,status,parallelism,calibration_cases,benchmark_cases,measurements,extrapolations,prohibitions}` with `schema_version="l8-g2g4-feasibility-v1"` and `status` exactly `COMPLETE` or `ABORTED`; only `COMPLETE` is promoted. `[PROPOSED]`

- `artifact_date` is UTC `YYYY-MM-DD`; `regime` is the exact string from the approved spec header; SHA fields are 40-lowercase-hex; digests are 64-lowercase-hex.
- `parallelism` is exactly the frozen object from §8.11.2 plus `{parallel_repeatability_status}`.
- Each of six ordered `calibration_cases` is exactly `{case_id,W,N_w,alpha,v_mult,sigma_dose,termination,iterations,service_wall_ns,process_cpu_ns,status}`.
- Each of six ordered `benchmark_cases` is exactly `{case_id,W,N_w,alpha,v_mult,c_min,eta,repetitions,valid_bootstrap_replicates,max_bootstrap_attempts,case_service_wall_ns,process_cpu_ns,service_seconds_per_repetition,status}`.
- `measurements={parent_batch_wall_ns,parent_cpu_ns,total_process_tree_cpu_ns,peak_aggregate_rss_bytes,memory_sampling_interval_ms,psutil_version,platform}`.
- `extrapolations={s_max_seconds_per_repetition,s_mean_seconds_per_repetition,parallel_efficiency,projected_screen_wall_seconds_conservative,projected_screen_wall_seconds_central,projected_calibration_wall_seconds,projected_total_wall_seconds_conservative}`.
- `prohibitions` is the exact ordered array from §8.10.2 plus `"no-screening-from-benchmark-approval"` as its final element.

All six calibration cases and six benchmark cases must be `PASS`; parallel repeatability must be `PASS`; all counts/coordinates must match the frozen config; formulas must recompute within `1e-12` relative tolerance; timing integers must be positive; memory must be positive; unknown fields fail. `[PROPOSED]`

#### 8.11.7 Authorization boundary

Rebecca's approval of v2.6 authorizes A1/A2 implementation, tests, failure rehearsal, two parallel-repeatability fixture executions, six uncached calibrations, and the six-case parallel feasibility benchmark only. `[PROPOSED]` It does not authorize the 2,000-repetition screen, Commit B screening evidence, 10,000 confirmation, sensitivity/misspecification work, scoring, or protected seeds. Benchmark results return through fresh-context CRITIC to Rebecca for the separate workload ruling.

### 8.12 v2.7 final closure for the authorized 1,000-repetition parallel feasibility diagnostic

**Authorization source:** `docs/rulings/REBECCA_L8_1000_REP_FEASIBILITY_AUTHORIZATION.md` at merged main SHA `d08cb7eefec67609a3ea3cee0eb20da22f78c40a`. Rebecca authorized the candidate-blind, synthetic, O-15 1,000-repetition parallel feasibility workload and retained the v2.6 multiprocessing path. This subsection supplies only the three execution closures required by that ruling. `[PROPOSED — Rebecca-authorized diagnostic workload]`

#### 8.12.1 Exact repetition allocation and case ordering

Case order is geometry-major, then sentinel-cell order exactly as listed in v2.6: low, central, high. Allocation is fixed as follows and totals exactly 1,000. `[PROPOSED — Rebecca-authorized diagnostic workload]`

| ordinal | case_id | W | N_w | alpha | v_mult | C_min | eta | repetitions |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | `g0_low` | 50 | 4 | 0.0 | 0.5 | 0.5 | 0.01 | 167 |
| 1 | `g0_central` | 50 | 4 | 0.05 | 1.0 | 0.7 | 0.1 | 167 |
| 2 | `g0_high` | 50 | 4 | 0.2 | 2.0 | 0.8 | 0.2 | 167 |
| 3 | `g1_low` | 400 | 64 | 0.0 | 0.5 | 0.5 | 0.01 | 167 |
| 4 | `g1_central` | 400 | 64 | 0.05 | 1.0 | 0.7 | 0.1 | 166 |
| 5 | `g1_high` | 400 | 64 | 0.2 | 2.0 | 0.8 | 0.2 | 166 |

The ordered `benchmark_cases` array uses ordinals 0–5 above. Each case's `repetition_index` is zero-based and local to that case. Parallel scheduling may complete out of order; collection and canonical publication are sorted by `(ordinal,repetition_index)` before statistics or hashing. No dynamic reallocation, early stopping, replacement, or work stealing may alter counts. `[PROPOSED]`

#### 8.12.2 Feasibility bootstrap depth

Every feasibility repetition requires exactly 5,000 valid bootstrap replicates and permits at most 5,500 attempted replicates. `[PROPOSED]` This **retains and makes binding for the authorized 1,000-repetition feasibility workload** the v2.6 values; it does not reduce them. The stratified bootstrap algorithm, 20-stream `(seed,dose)` RNG construction, invalid-draw handling, percentile interval, quantile convention, lower-bound pass rule, and complete statistical verdict are unchanged.

For feasibility bootstrap identities, `run_mode="feasibility-benchmark"`, `case_ordinal`, and case-local `repetition_index` are included in addition to the v2.5 bootstrap fields. `case_ordinal` is 0–5; this prevents two cases sharing coordinates in a future amendment from sharing streams. The published benchmark case records must state `valid_bootstrap_replicates=5000` and `max_bootstrap_attempts=5500`; any repetition that cannot obtain 5,000 valid draws in 5,500 attempts is an ordinary statistical false kill, not INSTRUMENT FAILURE. `[PROPOSED]`

#### 8.12.3 Fully frozen parallel-repeatability fixture

The repeatability fixture is:

- `case_id="parallel_repeatability_v1"`;
- geometry `(W,N_w)=(50,4)`;
- cell `(alpha,v_mult,C_min,eta)=(0.05,1.0,0.7,0.1)`;
- 32 complete five-seed repetitions, local indices `0..31` `[PROPOSED]`;
- 5,000 valid bootstrap replicates and at most 5,500 attempts per repetition `[PROPOSED]`;
- `sigma_dose` loaded from the freshly computed, uncached `g0_central` feasibility calibration from the same invocation and verified against its calibration record digest; no cache or hard-coded sigma is permitted;
- simulation RNG namespace `parallel-repeatability`, identity `{config_digest,case_id,W,N_w,alpha,v_mult,c_min,eta,repetition_index,seed_index}`; and
- bootstrap namespace `bootstrap`, with the v2.5 per-`(seed,dose)` identity plus `run_mode="parallel-repeatability"` and `case_id`.

Both executions use the frozen scoring-parity pool (`spawn`, chunksize one, maximum-capacity frozen worker count) and the same identities. Each produces exactly:

`{schema_version,config_digest,implementation_sha,config_source_sha,case,parallelism,results,elapsed_seconds}` with `schema_version="l8-parallel-repeatability-v1"`; `case={case_id,W,N_w,alpha,v_mult,c_min,eta,repetitions,valid_bootstrap_replicates,max_bootstrap_attempts,sigma_source_case_id,sigma_record_digest}`; `parallelism` is the exact frozen object; and `results` is an array ordered by `repetition_index`. `[PROPOSED]`

Each result is exactly `{repetition_index,seeds,bootstrap,complete_verdict}`. `seeds` is ordered by `seed_index` and each item is exactly `{seed_index,rho,beta,beta_star,direction_pass,spearman_pass,beta_star_pass}`. `bootstrap={valid_replicates,attempts,lower,upper,pass}`. `complete_verdict` is boolean. Finite floats use the canonical JSON rules; no unknown fields are permitted.

Comparison removes exactly the top-level `elapsed_seconds` field from each object, canonicalizes both objects, and requires byte identity and SHA-256 identity. Also compare ordered RNG-root digests and the calibration-record digest separately. Any mismatch raises `DiagnosticNondeterminismError` exit 23. Neither execution is serial. `[PROPOSED]`

#### 8.12.4 Committed known-good rehearsal pair

The 12-case failure rehearsal uses this committed pair only:

- `tests/fixtures/l8_g2g4/known_good_pair_v1.json`
- `tests/fixtures/l8_g2g4/known_good_pair_v1.sha256`

The JSON canonical bytes are exactly `{"artifact_kind":"l8-g2g4-rehearsal-prior","payload":{"generation":1,"status":"COMPLETE"},"schema_version":"l8-g2g4-known-good-pair-v1"}` followed by LF. Its SHA-256 is `36d07e6b515031d38c7f8e88a94e8c0128bf7256e9c4ba0c327cb44213e885e6`. The sidecar bytes are exactly `36d07e6b515031d38c7f8e88a94e8c0128bf7256e9c4ba0c327cb44213e885e6  known_good_pair_v1.json` followed by LF. `[PROPOSED]` Tests copy both files byte-for-byte into the isolated prior-pair location; no test generates or modifies the source fixture.

#### 8.12.5 Frozen estimator-fixture descriptor digests

The fixture generator is the reviewed `validate_estimator` procedure in `diagnostics/l8_power_analysis.py` at `b1397498ca369067e956479e6c2bd6b0793c3e89`: `np.random.default_rng(12345)`, 200,000 trials, positive then zero-slope `(4,4)` draws within every trial, binary64, variance 0.01. `[PROPOSED]` ARCHITECT does not execute the trials; the frozen digests identify the exact generator descriptors that TASK BUILDER executes after approval.

- Positive descriptor canonical bytes: `{"draw_order":"positive-then-zero","dtype":"float64","generator":"np.random.default_rng","n_trials":200000,"noise_variance":0.01,"seed":12345,"shape":[4,4],"slope":0.02,"stream_position":"first-draw-each-trial"}` plus LF. SHA-256: `e9ac5654d788367f7c98cc861ec99e39c587be20ac1fe1135863e106a5be3b30`.
- Zero-slope descriptor canonical bytes: `{"draw_order":"positive-then-zero","dtype":"float64","generator":"np.random.default_rng","n_trials":200000,"noise_variance":0.01,"seed":12345,"shape":[4,4],"slope":0.0,"stream_position":"second-draw-each-trial"}` plus LF. SHA-256: `db57e8d3d0111162ebe193d9f66cbb0c96dd73900450810436cad270daf71b5b`.

`fixture_digests.estimator_positive_v1` and `fixture_digests.estimator_zero_v1` equal those values. TASK BUILDER verifies descriptor bytes before running the single shared RNG loop; it then applies the existing mean/tolerance assertions from the baseline. A descriptor mismatch is `DiagnosticChecksumError` exit 21. `[PROPOSED]`

#### 8.12.6 Authorization boundary

After fresh-context CRITIC review and Rebecca clearance of this closure, TASK BUILDER may implement and execute only the staged A1/A2 path, fixed apparatus/failure rehearsal, two parallel-repeatability executions, six uncached calibrations, and the exactly 1,000-repetition parallel feasibility diagnostic above. No screening, scoring, protected seeds, G2–G4 freeze, 10,000 confirmation, sensitivity/misspecification stress rerun, or merge authority is granted. `[PROPOSED — authorization boundary]`

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
| G2 | Regulation-error definition plus exact all-seeds verdict aggregation | OPEN — v2.4 §8 must be CRITIC-reviewed, Rebecca-approved, implemented diagnostically, re-reviewed, and ruled by Rebecca `[PROPOSED]` |
| G3 | Minimum battery geometry under the primary complete-verdict false-kill criterion | OPEN — candidate-blind sweep §8.2; <0.10 required, <0.05 preferred `[PROPOSED]` |
| G4 | C_min and η (+ bounds), selected only after aggregation and battery freeze | DEFERRED — no recomputation or selection in this cycle `[PROPOSED]` |
| G5 | CF1 riders: memory-arm mechanism prediction + pre-committed boundary-condition classification (§6.4) + three-control panel (§6.2, §6.3) | Ratify verbatim `[Entry 81]` |

---

## §12 Sequencing (binding order)

1. ARCHITECT v2.7 final three-item closure and changelog committed; no computation.
2. Rebecca directly cleared this executable closure on 2026-08-20 under her merged authorization at `d08cb7eefec67609a3ea3cee0eb20da22f78c40a`. The screening run remains unauthorized.
3. TASK BUILDER produces A1/A2, tests them, and runs only the fixed rehearsal/repeatability and 1,000-repetition parallel feasibility evidence commit; no screening evidence.
4. Fresh-context CRITIC reviews A1/A2, tests, failure rehearsal, parallel repeatability, and benchmark. Rebecca then decides whether to authorize the full screen, amend/reduce it, or stop.
5. Only if separately authorized, TASK BUILDER runs screening and produces a separate screening-evidence commit; fresh-context CRITIC reviews it. Return design, screening analysis, and CRITIC ruling to Rebecca. Only Rebecca may freeze aggregation or battery size or decide G2/G3.
6. After Rebecca freezes aggregation and battery geometry, TASK BUILDER recomputes the sensitivity and misspecification maps under §8.3–§8.5; fresh-context CRITIC reviews; Rebecca alone decides G4.
7. §4 L7/L10 reconciliation check documented; any delta triggers a review cycle.
8. Pre-registration freeze (L19): all `[PROPOSED]` values resolved, appendix committed, hash-attested.
9. Final L8 scoring implementation release requires a separate Rebecca authorization. Protected seeds remain unexposed.
10. Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

---

*Every `[PROPOSED]` tag is a number offered for ruling, not a decision made. The TASK BUILDER receives diagnostic implementation instructions only. The narrowed claim (Entry 81) is a P5-authorized interpretive ruling — the deviation from broader constitutional L8 language is memorialized with Rebecca's sign-off.*
