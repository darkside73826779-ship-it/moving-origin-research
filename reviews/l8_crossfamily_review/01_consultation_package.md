# L8 HOMEOSTATIC-VARIABLE PREREQUISITE — ADVISOR CONSULTATION PACKAGE

**To:** Science Advisor (read-only GitHub access to `darkside73826779-ship-it/moving-origin-research`)
**From:** Rebecca McClintic, Principal — Moving Origin Research
**Date:** 2026-08-18
**Purpose:** Rebecca needs scientific advice on defining the L8 homeostatic variable and its regulation target. This is the primary blocker on M4 implementation (the CRITIC BLOCKed the L8 prerequisite because the framework is approved but not instantiated). The advisor's review does NOT discharge §6.3(1) of the governance paper. Rebecca remains sole gate authority.

**How to use this document:** Every claim cites the repository file and line it comes from. You can verify any item directly in the GitHub repo. Return your recommendations to Rebecca. You are not asked to approve, sign, or authorize anything — only to advise on the scientific design of the L8 test.

---

## 1. What L8 is

L8 ("Stakes coupling") is one of five laws tested at M4. It tests whether the system has "stakes" — whether a homeostatic variable's regulation error measurably increases when the system's self-model calibration is degraded. The theoretical basis is homeostatic RL and the Damasio/Seth line on interoception/feelings: a system with real stakes has variables it must keep within bounds, and its ability to regulate those variables depends on the quality of its self-model.

### The verbatim law text (constitution line 26, `[LAW-L8]`)

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

### What L8 tests (in plain terms)

The system has a "self-model" (its L7 mirror component — its internal representation of its own state). L8 asks: does the system have a variable it cares about (a homeostatic variable with a regulation target), and does its ability to regulate that variable degrade when its self-model is corrupted? If the variable's regulation error rises dose-dependently as self-model noise increases, the system has real stakes — its self-model quality matters for something it needs to maintain. If regulation error doesn't rise (or rises for non-self-model noise too), the stakes are "decorative" and L8 fails.

### The "only then" specificity requirement

The law says regulation error must rise when self-model calibration is degraded "and only then." So the same noise injected into a non-self-model component must NOT raise regulation error. This is the specificity control: it proves the regulation error responds to self-model quality specifically, not to general system perturbation.

### Related law — L14 (line 40)

> **L14 — Stakes touch everything or nothing.** The homeostatic variables (L8) must be readable by the self-model, affected by memory quality, and predictive targets for the thick present. A stakes module only one component can see is decorative.

L14 (tested at M4 alongside L8) requires the L8 homeostatic variables to be: (1) readable by the self-model, (2) affected by memory quality, and (3) predictive targets for the "thick present" (the moving-origin temporal self-index). So whatever homeostatic variable is chosen for L8 must also satisfy these L14 coupling requirements.

---

## 2. The locked bars (already pre-registered — NOT under review)

| Bar | Value | Source |
|---|---|---|
| Minimum dose levels | ≥ 3 (plus Level 0 zero-noise baseline) | `[BAR-Entry 11]` (M0 sheet line 21) |
| Spearman ρ (monotonic dose-response) | ≥ 0.8 | `[BAR-Entry 11]` (M0 sheet line 21) |
| Standardized slope | ≥ 0.2 | `[BAR-Entry 11]` (M0 sheet line 21) |
| Specificity control | mandatory — self-irrelevant dose must NOT move regulation error | `[LAW-L8]` |
| Seeds | 5 | `[BAR-Entry 11.3]` |

These bars are locked. The question is not whether these thresholds are right — it's what the homeostatic variable and regulation target actually are.

---

## 3. What the CRITIC found (the blocker)

The CRITIC's L8 prerequisite review (`reviews/critic_l8_prerequisite_review.md` on `critic/l8-prerequisite-review`, commit `dd099bd`) returned BLOCK. The L8 framework is approved (Ruling 3, Entry 76) but **not instantiated** — the spec gives examples and "predefine X" requirements but does not provide the concrete definitions a TASK BUILDER needs to implement L8 without making design decisions.

Four criteria, all with gaps:

### Criterion 1 — Regulable `[LAW-L8]` — GAP
The spec says "Define ≥ 1 homeostatic variable with a regulation target (e.g., a resource level, error budget, or calibration metric)." But no homeostatic variable is named — only a list of examples. No setpoint, no bounds, no "healthy operation" range. "Regulation error = distance from target" is only operational once a specific variable and target exist.

### Criterion 2 — Target defined `[PROPOSED — requires Rebecca sign-off]` — GAP (PRIMARY BLOCKER)
The spec says "The regulation target is a specific numeric value or bound, not a vague aspiration." But the target is not a specific value — it's a list of examples with no named variable, no setpoint, no quantifiable target. The spec itself tags this `[PROPOSED — requires Rebecca sign-off]`, acknowledging the target is not yet defined and requires Rebecca's decision. **This is the primary blocker. Rebecca must name/approve the specific homeostatic variable and its regulation target.**

### Criterion 3 — Calibratable noise dose `[OP-Entry 11.7]` — GAP (partial)
The dose levels are defined ordinally (Level 0 zero-noise, Level 1 low, Level 2 medium, Level 3 high) but: (a) the noise injection MECHANISM is unspecified — "inject calibrated noise into the self-model" does not state what calibrated noise is operationally (additive Gaussian on weights? multiplicative? activation perturbation? dropout?); (b) dose magnitudes are qualitative only ("small/moderate/large"). The noise channel/mechanism and dose-setting rule are the independent variable of the L8 dose-response test — the TASK BUILDER choosing them would be a design decision, not an implementation detail.

### Criterion 4 — Constructible specificity control `[LAW-L8]` — GAP
Ruling 3's four predefinitions (comparison component, perturbation type/magnitude, calibration set, tolerance) are framed as requirements to predefine, not as actual predefinitions. No non-self-model component is named; no perturbation type/magnitude is specified; no calibration set is defined; no tolerance is given. The tags `[Rebecca-approved (Ruling 3, Entry 76)]` mean the APPROACH (standardized proximal-component effect, predefining these four) is approved — not that the four predefinitions are provided.

### The CRITIC's key distinction
**Implementation detail** (TASK BUILDER's job): code structure, data plumbing, function names, numerical computation mechanics that preserve already-specified semantics.
**Design decision** (ARCHITECT + Rebecca's job): anything that determines the construct being tested or that could change whether L8 passes/fails — the homeostatic variable, target/setpoint, regulation-error formula, self-model noise mechanism, dose magnitudes/calibration rule, non-self component, severity-matching calibration set, tolerance.

---

## 4. What Rebecca needs to decide (the primary blocker — Criterion 2)

Rebecca must name/approve a specific homeostatic variable and its regulation target. The variable must be:

1. **A real variable in the moving-origin temporal self-index system** that the system maintains (not a synthetic add-on)
2. **Homeostatic** — it has a regulation target (setpoint or bounds) it should stay within for healthy operation
3. **Regulable** — the system can deviate from the target (so regulation error is measurable) and can act to reduce deviation
4. **Coupled to self-model quality** — the system's ability to regulate it depends on its self-model (L7 mirror) calibration, so degrading the self-model raises regulation error (this is what L8 tests)
5. **Satisfying L14** — the variable is readable by the self-model, affected by memory quality, and a predictive target for the thick present

### The spec's examples (what the spec currently offers, none of which is instantiated)

The spec says the homeostatic variable is "e.g., a resource level, error budget, or calibration metric." These are categories, not specific variables. Rebecca needs to choose (or define) a specific variable.

### What "regulation target" means concretely

A specific numeric value or bound that the homeostatic variable should stay at/near/within. For example:
- A resource level that should stay within [lower, upper] bounds
- An error budget that should stay below a threshold
- A calibration metric that should stay within a tolerance of a setpoint

"Regulation error" is then operationally defined as the distance from the target (how far the variable deviates from its setpoint or how far outside its bounds it goes).

---

## 5. What the ARCHITECT will instantiate after Rebecca's decision (Criteria 1, 3, 4)

Once Rebecca names the homeostatic variable and regulation target, the ARCHITECT will concretely instantiate:

1. **The named variable and target** (closes C1 and C2) — using Rebecca's decision
2. **The self-model noise injection mechanism + dose calibration rule** (closes C3) — what "calibrated noise" is operationally and how dose magnitudes are set across levels 0–3. This must be pre-registered before any data exists (`[LAW-L19]`) and must be candidate-blind per Ruling 9 (the candidate's diagnostic-seed results 101–105 are NOT inputs to the calibration; only oracle/synthetic ground-truth is)
3. **The four Ruling-3 predefinitions** (closes C4) — the comparison component, perturbation, calibration set, and tolerance for the specificity control. These must be pre-registered (`[LAW-L19]`) and candidate-blind (Ruling 9)

The ARCHITECT specifies these; the CRITIC re-clears the instantiated prerequisite; then the TASK BUILDER is released for L8 implementation.

---

## 6. Standing constraints (binding, not under review)

- **O-14:** No re-run-on-failure. Seeds 201–203 and 301–303 retained, never rerun.
- **O-15:** Development runs diagnostic-only.
- **§5 P1–P6:** No law-text reconstruction; verbatim quotation; source-class tags; regime dating; deviation memorialization requires Rebecca sign-off; provenance citation verification.
- **No renaming negatives:** INSTRUMENT FAILURE stays INSTRUMENT FAILURE.
- **Pre-registration (`[LAW-L19]`):** All design decisions about the L8 construct (variable, target, noise mechanism, dose magnitudes, specificity component) must be pre-registered before any data exists.
- **Candidate-blind (Ruling 9, Entry 76):** Tolerance calibration must be candidate-blind (candidate diagnostic seeds 101–105 NOT inputs; oracle/synthetic ground-truth only) and frozen before scoring.

---

## 7. Advisor questions

1. **Homeostatic variable selection:** Given the moving-origin temporal self-index (a system that maintains a temporal self-model and uses it to predict/act), what is a natural, real homeostatic variable the system maintains that has a regulation target? The variable must be something the system genuinely needs to keep within bounds, and its regulation must depend on self-model quality. The spec's examples are "resource level, error budget, or calibration metric" — which of these (or what else) is the right choice for this system?

2. **Regulation target:** For the chosen variable, what is the appropriate regulation target (setpoint or bounds)? How should "regulation error" be operationally defined (distance from setpoint? time outside bounds? integrated deviation?)?

3. **Self-model noise mechanism:** What is the right way to operationally define "calibrated noise injected into the self-model"? The self-model is the L7 mirror component (the candidate's internal self-state representation). Options include additive Gaussian on the self-model's state estimates, multiplicative perturbation, activation perturbation, dropout on self-model internals. Which preserves the test's validity (degrades self-model calibration in a dose-dependent, measurable way)?

4. **Dose calibration:** How should the dose magnitudes (Level 1 low, Level 2 medium, Level 3 high) be calibrated? Should they be relative to the self-model's natural operating variance? Fixed magnitudes? Calibrated against oracle ground-truth? The calibration must be pre-registered and candidate-blind (Ruling 9).

5. **Specificity control component:** What is the right non-self-model component for the "only then" specificity test? The spec mentions "the controller's action selection, or the memory store." Which component is appropriate, and how should the severity-matched perturbation be standardized (Ruling 3: pre-registered standardized proximal-component effect)?

6. **L14 coupling:** Does the chosen homeostatic variable satisfy L14's requirements (readable by the self-model, affected by memory quality, predictive target for the thick present)? Or does the choice create an L14 problem?

7. **Falsifiability:** Is the L8 test as designed genuinely falsifiable? Can it fail? What would a "decorative stakes" system look like that passes the test without real stakes — and does the specificity control prevent that?

8. **Anything else:** Any concern, gap, or risk the advisor identifies that is not captured above.

---

## 8. Program context

Moving Origin Research tests whether a "moving-origin temporal self-index" can be distinguished from alternatives, under a 20-law constitution with role-separated AI agents and Rebecca as sole human gate authority.

- **M0** COMPLETE (pre-registration: `docs/rulings/M0_DECISION_SHEET.md`)
- **M1** GREEN (harness delivered, discrimination bar met)
- **M2 (E1)** GREEN/SEALED (six-arm battery; waiver per Constitution v2 Amendment 2)
- **M3 (E2)** INSTRUMENT FAILURE (retained). Seeds 201–203 and 301–303 never rerun (O-14). Provisional advancement to M4.
- **M4** GATE SIGNED — implementation authorized (scoring gated). Currently in Step 8 (build). L8 implementation is BLOCKed pending this prerequisite resolution.

**Repo:** `github.com/darkside73826779-ship-it/moving-origin-research` (public)

**Authority chain:** Rebecca > constitution's laws > approved specifications > agent judgment. No agent speaks for Rebecca.

---

**Return your recommendations to Rebecca. This consultation does not authorize, approve, or sign anything. Rebecca remains sole gate authority. The L8 construct decisions (variable, target, noise mechanism, dose magnitudes, specificity component) must be pre-registered before any data exists and must be candidate-blind.**
