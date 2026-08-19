# L8 INSTANTIATION SPECIFICATION — Selective-Risk Homeostat

**Component:** M4 / L8 (Stakes coupling) + L14 couplings
**Author:** ARCHITECT (advisor-session draft — enters pipeline as ARCHITECT proposal, subject to full review chain)
**Status:** DRAFT v1 — pending fresh-context CRITIC review → Principal gate (five items G1–G5) → pre-registration freeze → TASK BUILDER release
**Sources:** Advisor consultation return v2 (2026-08-18/19); CRITIC re-review CLEAR WITH CONDITIONS (CF1–CF3); `[LAW-L8]` constitution line 26; `[LAW-L14]` line 40; `[BAR-Entry 11]` M0 sheet; Ruling 3 + Ruling 9 (Entry 76)
**Standing constraints inherited:** O-14, O-15, §5 P1–P6, L19 pre-registration, Ruling 9 candidate-blindness. Nothing in this spec authorizes scoring.

---

## §1 Verbatim law text (P2 — no reconstruction)

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law. `[LAW-L8]`

> **L14 — Stakes touch everything or nothing.** The homeostatic variables (L8) must be readable by the self-model, affected by memory quality, and predictive targets for the thick present. A stakes module only one component can see is decorative. `[LAW-L14]`

---

## §2 The homeostatic variable (closes CRITIC prerequisite C1, C2)

**Variable (V):** windowed selective risk — the error rate on queries the system elects to answer, computed per window.
- Window: W consecutive queries of the L8 battery; `[PROPOSED]` W = 50 (four windows per 200-query battery).
- For window w: `r_w = (# incorrect answered queries in w) / (# answered queries in w)`. Correctness judged against oracle ground truth by the harness.

**Regulation target (R*):** `[PROPOSED — requires Rebecca sign-off, G2 rider]`
`R* = R_ref + m`, where `R_ref` is the selective risk achieved by the synthetic reference mirror (§5) at coverage `C_ref = 0.75` on oracle-graded synthetic profiles, and `m = 0.05` margin. R* is a pre-registered constant, frozen before any candidate data exists. Candidate outputs are not inputs to R* (Ruling 9).

**Regulation error — two statistics, two jobs (BF4 resolution; G2 gate item):**
- **Baseline gate statistic (hinge):** `E0 = mean_w max(0, r_w − R*)` at Level 0. Bar: `E0 ≤ ε_gate` (`[PROPOSED]` ε_gate = 0.01). A run failing the Level-0 gate is **INSTRUMENT FAILURE** (homeostat not in band before manipulation — dose-response from a violated baseline certifies nothing), not candidate failure.
- **Trend statistic (signed):** `D_ℓ = mean_w (r_w − R*)` at dose level ℓ. The locked bars run on D: Spearman ρ(dose, D) ≥ 0.8 and standardized slope ≥ 0.2, per seed, per `[BAR-Entry 11]`. Slope standardization: pooled within-dose SD of D across all levels, computed per seed.
- **Rationale (recorded):** hinge has a floor (point mass at zero for low doses → Spearman ties, undefined standardization); signed deviation is a legitimate reading of "distance from target" with defined variance. This dual definition fixes the operational meaning of a locked bar's terms and therefore requires Principal ruling (G2).

---

## §3 The regulation loop (closes advisor-BF1; Principal gate item G1)

Three elements, all pre-registered:

1. **Per-query actuator:** abstention driven by the L7 mirror's calibrated confidence against threshold τ (shared component with L10; separate batteries per §9).
2. **Windowed actuator:** bounded proportional threshold adaptation. At each window boundary the harness delivers outcome feedback for the completed window (per-query correctness of answered queries). The system updates: `τ ← clip(τ + η·(r_w − R*), τ_min, τ_max)`. Gain η and bounds are pre-registered constants (G4).
3. **Coverage floor:** the system must answer ≥ `C_min` of queries per window (G4). Abstention beyond the floor is forced-choice: the C_min·W highest-confidence queries are answered regardless of τ.

**Mechanism claim (recorded for the JUDGE):** a corrupted mirror misranks queries; global threshold adaptation cannot repair per-query misranking; at the coverage floor the system must act on a corrupted ranking. Dose-response therefore reflects structurally limited compensation, not definition.

**G1 (Principal, interpretive):** this spec adopts the loop-closure reading of "regulation" (deviation is causally operative via actuator 2 + the floor). The weaker feedforward-only reading was considered and rejected by advisor v2; the interpretive choice is constitutionally the Principal's and is memorialized at her gate.

---

## §4 Outcome-feedback channel disposition (CF3 — mandatory)

The per-window outcome-feedback channel is a **harness-provided environment feature present in ALL M4 batteries** (L7, L8, L10, L14, L18 arms alike), not an L8-only fixture. The system under test is thereby identical across all M4 laws.
- **Reconciliation requirement (blocking before freeze):** ARCHITECT re-checks the L7 and L10 sections of `specs/m4_specification.md` v1.6.2 against the channel's presence; the check and its outcome are documented in this spec's changelog. Any L7/L10 semantic change triggers a delta review cycle.
- The channel delivers correctness of *answered* queries only, per completed window, with no per-query interleaved feedback (no online supervision of individual answers).

---

## §5 Self-model noise mechanism and dose calibration (closes C3; NF1)

**Channel:** additive Gaussian noise in logit space on the mirror's per-query confidence estimate: `logit(c') = logit(c) + ξ, ξ ~ N(0, σ_ℓ²)`, seeded. Answer content untouched; only the self-signal is corrupted (isolates the L8 causal path).

**Dose levels:** Level 0: σ=0. Levels 1–3: `σ_ℓ ∈ {0.5, 1.0, 2.0}·√v_ref`.
**v_ref (candidate-blind):** the logit-space variance of the **synthetic reference mirror** — a calibrated confidence profile constructed from oracle ground truth on synthetic task profiles with construction procedure fixed in the pre-registration appendix. No candidate output is an input (Ruling 9). Realized ΔECE per dose is computed and **reported as a manipulation check only** — never a tuning input.

---

## §6 Specificity arm (closes C4; advisor-BF5; CRITIC-CF1)

**Component:** the memory store (world-mapping vs self-mapping contrast per the law's Damasio/Seth lineage).
**Perturbation:** seeded corruption of retrieved content at severity-matched doses. Severity matching per Ruling 3: memory dose at level ℓ is matched to mirror dose ℓ by **equal standardized effect on the component's own output** — retrieval-fidelity degradation on oracle-answerable queries, standardized by its Level-0 SD from synthetic profiles. Matching tolerance: `[PROPOSED]` ±0.25 standardized units, pre-registered.

**Potency bar (BF5 — mandatory):** at every level ℓ ≥ 1, the matched memory dose must degrade raw retrieval fidelity by ≥ `[PROPOSED]` 0.5 standardized units. A specificity arm whose perturbation fails potency is **INSTRUMENT FAILURE** (the control never bit; flatness is uninterpretable).

**Specificity bars (full-curve, not single-point):** across levels 0–3 in the memory arm, (a) trend statistic D stays in band: `|slope(dose, D)|` ≤ `[PROPOSED]` 0.1 with CI excluding the candidate-arm slope bar (0.2); (b) no level's D exceeds D at candidate-arm Level 1.

**CF1 pre-commitments (mandatory riders, pre-registered before freeze):**
1. **Predicted memory-arm mechanism (recorded):** memory corruption degrades retrieval → the calibrated mirror assigns lower confidence to affected queries → abstention absorbs them within the coverage budget → coverage drops, selective risk stays regulated. Operating point moves; regulation holds.
2. **Failure classification, pre-committed:** if the memory arm fails specificity via the **confidently-wrong-retrieval pathway** — defined observably as: potency bar met AND mean mirror confidence on memory-corrupted-and-wrong answered queries ≥ mean confidence on correct answered queries at the same level (the mirror did not see the corruption) — the outcome is classified **L8 BOUNDARY CONDITION: mirror-blind memory corruption**, recorded as a documented negative, NOT relabeled, and L8 is scored FAIL-with-boundary-annotation. Any other specificity failure is plain candidate FAIL. This classification is fixed now, before data, precisely so it cannot be chosen after.

---

## §7 L14 couplings (closes the L14 half of the prerequisite)

1. **Readable:** the windowed-risk register (current r_w running value, current τ, R*) is exposed in the self-state vector the L7 mirror reads. Build item.
2. **Affected by memory quality:** intrinsic (retrieval quality determines correctness of answers). Verified by the specificity arm's coverage response.
3. **Predictive target for the thick present:** next-window realized risk `r_{w+1}` is added as a prediction target for the downstream consumer over recency-weighted features. Bar: prediction beats a pre-registered naive baseline (last-window carry-forward) on ≥ `[PROPOSED]` 4/5 seeds.
**Recorded distinction (audit-proofing):** L14's "affected by memory quality" is satisfied by **operating-point response** (coverage moves); L8's specificity is satisfied by **regulation-error stability** (risk stays in band). Same runs, different statistics, no contradiction.

---

## §8 Power analysis and sensitivity map (advisor-BF4; CRITIC-CF2 — blocking before Principal gate)

Delivered to the Principal WITH gate items G1–G5, all candidate-blind on synthetic profiles:
1. **Power analysis:** false-kill probability of the ρ ≥ 0.8 (four-point) + slope ≥ 0.2 joint bar at W=50, 4 windows/seed, 5 seeds, across plausible effect sizes. If false-kill probability at target effect exceeds `[PROPOSED]` 0.10, battery size escalates to G3.
2. **Sensitivity map (CF2):** two-dimensional map over (C_min, η) showing regions where (a) the system abstains its way out (flat curve — false kill), (b) the test trivializes (any noise moves risk — vacuous pass), (c) the informative region. G4's ruling selects from this characterized space, not from bare numbers.

---

## §9 Multiplicity and shared machinery (NF2)

L8 and L10 share components (mirror, abstention) and run **separate batteries** — shared components, separate evidence. All L8 stochastic checks (trend bars ×5 seeds, specificity bars, potency bars, baseline gates) enter the M4 FWFP family per the §6-FWFP closure audit of the task spec. Count table to the FWFP appendix before freeze.

---

## §10 Evidentiary posture and disclosures (advisor-BF2, BF3; NF3)

**Recorded verbatim in the spec, per review chain:**
1. The candidate arm is primarily a **manipulation check**; the **specificity contrast carries the discriminative load** of L8. (BF2)
2. Design principle applied: all added machinery — outcome feedback, coverage floor, bounded controller — is **task-environment pressure**, harness-side or environment-level. The tested coupling (mirror quality → regulation capacity) is not wired into the candidate anywhere; it emerges or fails under pressure. Index-staleness was rejected because it required candidate-side wiring of the coupling itself. Machinery growth from advisor v1 to v2 is acknowledged. (BF3)
3. Disclosure: the selected variable is also the cheapest to build from existing components. The fresh-context reviewer should weigh that coincidence. (NF3)
4. Chain disclosure: this spec descends from advisor v1 → CRITIC BF1–BF5 → advisor v2 → CRITIC CLEAR-with-CF1–CF3, all within one model family. The full four-document chain accompanies this spec to the external human reviewer **before fresh-seed scoring** (recommended sequencing, §12).

---

## §11 Principal gate items (all rulings required before pre-registration freeze)

| # | Item | Decision |
|---|---|---|
| G1 | Interpretive: "regulation" = loop-closure reading (deviation causally operative) | Adopt / reject (reject → feedforward petition, redesign) |
| G2 | Regulation-error definition: hinge for baseline gate, signed deviation for trend bars; W=50; ε_gate | Ruling on locked-bar terms |
| G3 | Battery size, IF power analysis (§8.1) shows false-kill > threshold | 200 / escalated size |
| G4 | C_min and η (+ bounds), selected from the §8.2 sensitivity map's informative region | Constants |
| G5 | CF1 riders: memory-arm mechanism prediction + pre-committed boundary-condition classification (§6) | Ratify verbatim |

---

## §12 Sequencing (binding order)

1. This spec → **fresh-context CRITIC** review (input: this spec + the full advisor/CRITIC chain, per §10.4 — review starts from the objections).
2. §8 power analysis + sensitivity map produced (candidate-blind).
3. **Principal gate:** G1–G5 ruled with §8 artifacts in hand.
4. §4 L7/L10 reconciliation check documented; any delta → review cycle.
5. Pre-registration freeze (L19): all `[PROPOSED]` values resolved, appendix committed, hash-attested.
6. TASK BUILDER released for L8 implementation.
7. **External human review of the L8 design chain (recommended before any fresh-seed exposure)** — L8 is the constitution's most philosophically loaded law; a design flaw found post-scoring costs unrecoverable seeds.
8. Scoring remains gated behind the five standing M4 gates. Nothing herein authorizes scoring.

---

*Every `[PROPOSED]` tag is a number offered for ruling, not a decision made. Per the CRITIC's standing distinction: this document specifies constructs; the TASK BUILDER receives no design decisions.*
