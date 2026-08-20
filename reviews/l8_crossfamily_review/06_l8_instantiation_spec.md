# L8 INSTANTIATION SPECIFICATION v2.3 — Selective-Risk Homeostat (G2–G4 Remediation)

**Component:** M4 / L8 (Stakes coupling) + L14 couplings
**Author:** ARCHITECT (implementing Rebecca's advisor-session proposal per Entry 81 + Sol cross-family review XF-4–XF-9 resolution conditions)
**Status:** DRAFT v2.3 — remediation design only; pending TASK BUILDER diagnostic implementation → fresh-context CRITIC → Rebecca; G2–G4 not frozen and scoring implementation not released
**Date:** 2026-08-19 · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Sources:** Entry 81 (narrowed claim) `[Entry 81]`; Sol cross-family review (XF-4–XF-9, XF-10–XF-11) `[Sol-XF-n]`; advisor proposal v2; CRITIC re-review CF1–CF3; `[LAW-L8]` constitution line 26; `[LAW-L14]` line 40; `[BAR-Entry 11]` M0 sheet; Ruling 3 + Ruling 9 (Entry 76) `[Entry 76]`
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
- RNG reproducibility differs between serial and parallel execution after removal of the explicitly excluded timing field `[PROPOSED]`;
- the resolved configuration manifest or digest differs from the frozen aggregation, battery geometry, dose grid, seed manifest, or estimator version `[PROPOSED]`;
- artifact integrity fails (schema, completeness, atomic-write checksum, or parse validation) `[PROPOSED]`; or
- the pre-candidate synthetic dose/calibration apparatus fails its pre-registered convergence or potency validation `[PROPOSED]`.

An ordinary per-seed failure of `ρ`, `β*`, direction, interval, specificity, potency, baseline, or zero-variance behavior is a statistical FAIL/KILL under its applicable rule and SHALL NOT be reclassified. `[PROPOSED — no-relabeling rule]` Once a scoring failure exists, O-14/D1/D5 prohibit rerun, rescoring, or reframing it to avoid the negative. `[BAR-Entry 52]` (O-14) `[OP-Entry 12]` (D1/D5)

### 8.7 Failure-injection tests and complete diagnostic rehearsal

Before CRITIC review, TASK BUILDER SHALL add genuine automated tests with assertions and perform one candidate-blind diagnostic rehearsal covering:

1. **Incomplete output:** suppress a required section; assert schema failure, nonzero exit, no artifact promoted, and no success attestation. `[PROPOSED]`
2. **Corruption/partial write:** inject malformed JSON and a truncated temporary file; assert parse/checksum failure and preservation of the last complete artifact through atomic temp-file-then-rename publication. `[PROPOSED]`
3. **Nondeterminism:** run the same small synthetic fixture serially and in parallel; after removing only `elapsed_seconds`, assert byte-identical canonical JSON and identical resolved seeds. `[PROPOSED]`
4. **Configuration mismatch:** separately alter aggregation, `W`, `N_w`, dose grid, and seed manifest; assert each digest mismatch fails closed before simulation begins. `[PROPOSED]`
5. **Crash recovery:** inject calibration worker and identity failures; assert `CalibrationWorkerError`/`CalibrationIdentityError` route to exit code 1, no partial result table is published, no post-calibration simulation executes, and a later fresh diagnostic invocation starts from the frozen manifest rather than silently resuming partial state. `[PROPOSED]`

The rehearsal report SHALL list injected fault, expected assertion, observed exit/disposition, artifact path/hash, and pass/fail. No test may be a no-op, unconditional pass, or mock that bypasses the production error path. `[PROPOSED]`

### 8.8 Publication and prohibited computation

Publish code, simulation-seed derivation, frozen manifests, sweep table, uncertainty intervals, test results, and rehearsal report as committed diagnostic artifacts before any G2–G4 request. `[LAW-L19]` Do not run the prior full 10,000-simulation sensitivity/misspecification stress analysis until aggregation and battery size are frozen. No artifact from this cycle is scoring evidence. `[O-15]`

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
| G2 | Regulation-error definition plus exact all-seeds verdict aggregation | OPEN — v2.3 §8.1 must be implemented diagnostically, CRITIC-reviewed, and ruled by Rebecca `[PROPOSED]` |
| G3 | Minimum battery geometry under the primary complete-verdict false-kill criterion | OPEN — candidate-blind sweep §8.2; <0.10 required, <0.05 preferred `[PROPOSED]` |
| G4 | C_min and η (+ bounds), selected only after aggregation and battery freeze | DEFERRED — no recomputation or selection in this cycle `[PROPOSED]` |
| G5 | CF1 riders: memory-arm mechanism prediction + pre-committed boundary-condition classification (§6.4) + three-control panel (§6.2, §6.3) | Ratify verbatim `[Entry 81]` |

---

## §12 Sequencing (binding order)

1. ARCHITECT v2.3 remediation design and changelog committed; no computation.
2. TASK BUILDER implements only the all-seeds estimand, battery sweep, failure-injection tests, and diagnostic rehearsal in §8.1–§8.2 and §8.6–§8.7. It does not implement final L8 scoring or run the deferred map.
3. Fresh-context CRITIC reviews the v2.3 design, implementation delta, sweep artifact, and rehearsal evidence, beginning with §5 P1–P6 compliance.
4. Return the revised design, power analysis/sweep, and CRITIC ruling to Rebecca. Only Rebecca may freeze aggregation or battery size or decide G2/G3.
5. After Rebecca freezes aggregation and battery geometry, TASK BUILDER recomputes the sensitivity and misspecification maps under §8.3–§8.5; fresh-context CRITIC reviews; Rebecca alone decides G4.
6. §4 L7/L10 reconciliation check documented; any delta triggers a review cycle.
7. Pre-registration freeze (L19): all `[PROPOSED]` values resolved, appendix committed, hash-attested.
8. Final L8 scoring implementation release requires a separate Rebecca authorization. Protected seeds remain unexposed.
9. Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

---

*Every `[PROPOSED]` tag is a number offered for ruling, not a decision made. The TASK BUILDER receives diagnostic implementation instructions only. The narrowed claim (Entry 81) is a P5-authorized interpretive ruling — the deviation from broader constitutional L8 language is memorialized with Rebecca's sign-off.*
