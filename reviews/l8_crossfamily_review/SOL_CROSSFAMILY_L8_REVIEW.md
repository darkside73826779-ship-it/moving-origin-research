# Cross-Family Adversarial Review — L8 Selective-Risk Homeostat

**Reviewer:** GPT-family cross-family reviewer  
**Date:** 2026-08-19  
**Scope:** Full six-document L8 design chain, ending in *L8 Instantiation Specification — Selective-Risk Homeostat*, Draft v1  
**Authority:** Advisory review only. This document approves, signs, and authorizes nothing. The Principal remains sole gate authority.

## Overall verdict

**FRAME-CHALLENGED.** The design is a serious and falsifiable selective-risk stress test, but it has not yet established that the regulated quantity is a candidate-owned homeostatic variable rather than a harness-defined performance metric controlled by harness-supplied feedback. The distinction matters because L8 asks whether the system has stakes, not merely whether confidence corruption degrades constrained selective prediction. I find **3 FRAME**, **6 BLOCKING**, and **2 ADVISORY** issues. FRAME-CHALLENGED does not mean the design should be abandoned; it means the Principal must either supply a defensible bridge from selective-risk control to candidate-owned homeostasis or explicitly narrow what an L8 pass is claimed to establish. The BLOCKING items must be closed before pre-registration freeze.

## Findings

### XF-1 — FRAME — The proposed homeostat is partly created and operated by the test environment

**Target:** Instantiation Specification §2, “Variable (V): windowed selective risk”; §3, “At each window boundary the harness delivers outcome feedback” and “The system updates”; §4, “harness-provided environment feature”; §10.2, “all added machinery … is task-environment pressure.”

**The defect:** The variable is calculated using harness oracle labels, the error signal is delivered by the harness, the adaptive loop is introduced for the test, and the coverage constraint is externally imposed. Those facts can define a valid closed-loop experiment, but they do not by themselves show that the uninstrumented candidate owns, senses, and regulates an internal essential variable. The design therefore risks proving: *an externally completed controller loses selective-prediction performance when its confidence channel is corrupted*. That is weaker than: *the candidate has stakes whose regulation depends on its self-model*. Calling the new machinery “environment pressure” does not resolve ownership of the regulated state or controller.

**Resolution condition:** Before adopting G1, provide a causal ownership diagram and an intervention comparison that identify which state, sensor, controller, actuator, and cost belong to the candidate versus the harness. Demonstrate that the candidate already uses the risk state or an online proxy to alter behavior outside the L8 scoring fixture. If that cannot be shown, memorialize a narrower interpretation: L8 certifies externally closed selective-risk dependence, not intrinsic or organism-like stakes.

**Confidence:** High.

### XF-2 — FRAME — Selective risk is an outcome constraint, not yet an essential internal variable

**Target:** Advisor Proposal v1, Q1, “windowed selective risk”; Instantiation Specification §2, `R* = R_ref + m`; §10.2, claim that the coupling “emerges or fails under pressure.”

**The defect:** Selective risk is a useful service-level or decision-quality metric, but the chain does not identify an endogenous consequence of violating R* beyond the test controller changing its threshold. R* is derived from a synthetic reference at fixed coverage, not from a demonstrated viability, resource, integrity, or persistence requirement of the candidate. The loop closes BF1 operationally, but it can still be circular at the construct level: risk matters because the experiment adds a controller that treats it as error. This leaves the Damasio/Seth language stronger than the evidence supports.

**Resolution condition:** Either establish an independent consequence pathway that existed before L8 and makes excess risk costly to the candidate’s continued operation or goals, or remove the biological/interoceptive implication and define the construct explicitly as a functional, externally specified homeostat. The target must also be justified as a healthy operating bound for this candidate class, not merely a reference model’s achievable score.

**Confidence:** High.

### XF-3 — FRAME — One memory control cannot support the unrestricted phrase “and only then”

**Target:** Consultation Package §1, “and only then”; Instantiation Specification §6, memory store as the sole specificity component; §7.2, memory quality intrinsically affects correctness.

**The defect:** A flat regulation-error curve under one severity-matched memory perturbation establishes contrast against that perturbation, not exclusivity to self-model degradation. Other perturbations can plausibly impair the same loop: outcome-feedback delay or corruption, actuator/threshold faults, coverage-floor changes, answer-generation faults, or distribution shift. In addition, memory was chosen even though L14 requires the homeostatic variable to be affected by memory quality. The operating-point/regulation-error distinction makes the two requirements logically compatible, but it does not make memory the uniquely valid or sufficient negative control.

**Resolution condition:** Narrow the registered claim to “specific relative to the pre-registered memory control,” or add a small negative-control panel spanning sensor-independent controller, feedback-channel, and task-difficulty perturbations. State what evidence would justify the broader “only then” interpretation.

**Confidence:** High.

### XF-4 — BLOCKING — The Level-0 rule can relabel candidate failure as instrument failure

**Target:** Instantiation Specification §2, “A run failing the Level-0 gate is INSTRUMENT FAILURE”; fixed constraint that negatives are never relabeled.

**The defect:** Level 0 contains no injected defect. If the implemented candidate cannot keep selective risk within R* at baseline, that may show the proposed homeostat is absent or inadequate—the substantive negative L8 is meant to detect. Classifying every baseline miss as INSTRUMENT FAILURE removes that failure mode from the candidate verdict and creates a repeat of the prohibited relabeling risk. Instrument failure is appropriate only when an independent validity check shows that the apparatus, calibration, or battery malfunctioned.

**Resolution condition:** Split the rule. Pre-register objective apparatus-validity conditions that alone produce INSTRUMENT FAILURE. If those conditions pass but the candidate exceeds the baseline bound, classify it as candidate FAIL or “not eligible for a dose-response pass,” without changing the negative’s name after observation.

**Confidence:** High.

### XF-5 — BLOCKING — The standardized-slope denominator is not mathematically defined

**Target:** Instantiation Specification §2, “pooled within-dose SD of D across all levels, computed per seed.”

**The defect:** `D_l` is defined as one mean across windows for a given seed and dose. There is therefore no within-dose sample of `D_l` inside that seed from which to compute an SD. If window deviations are intended as replicates, the text must say so and must address dependence induced by sequential threshold adaptation. Different reasonable implementations produce different slope values and pass/fail outcomes.

**Resolution condition:** Give the exact estimator as an equation: regression inputs, slope numerator, denominator, pooling weights, degrees of freedom, treatment of windows, and zero-variance behavior. Validate it on fixed synthetic examples with expected numeric outputs. The candidate-blind power analysis must use this identical estimator.

**Confidence:** High.

### XF-6 — BLOCKING — The specificity test is under-specified and may compare unlike slope scales

**Target:** Instantiation Specification §6, “`|slope(dose, D)| ≤ 0.1` with CI excluding the candidate-arm slope bar (0.2)” and “no level’s D exceeds D at candidate-arm Level 1.”

**The defect:** The text does not say whether the memory slope is raw or standardized, how its confidence interval is constructed, its confidence level, its sampling unit, or how five seeds are aggregated. A confidence interval cannot literally “exclude a bar” without specifying which side must be excluded. The second bar also compares signed deviations without uncertainty and can be dominated by baseline offsets between separately run batteries. These omissions leave pass/fail-affecting choices to the builder.

**Resolution condition:** Define both-arm estimands in the same units; specify seed aggregation, interval method and level, direction of exclusion, missing/degenerate cases, and the complete conjunction used for PASS. Prefer a pre-registered arm-by-dose interaction or slope-difference estimand over comparing two independently thresholded rules, if compatible with the locked bars.

**Confidence:** High.

### XF-7 — BLOCKING — The L14 memory coupling is asserted but has no acceptance test

**Target:** Instantiation Specification §7.2, “Affected by memory quality: intrinsic … Verified by the specificity arm’s coverage response”; §6 specificity bars.

**The defect:** Section 6 includes a retrieval-fidelity potency bar and regulation-error stability bars, but no required coverage-response statistic, direction, minimum effect, uncertainty rule, or seed aggregation. Consequently, a run could satisfy every written §6 bar without demonstrating the §7.2 claim used to satisfy L14.

**Resolution condition:** Add a candidate-blind, pre-registered coverage-response estimand and acceptance rule, including the expected direction, minimum effect or interval criterion, per-seed aggregation, and the disposition when memory potency is present but coverage does not move.

**Confidence:** High.

### XF-8 — BLOCKING — The dose manipulation lacks domain and monotonicity validity rules

**Target:** Instantiation Specification §5, `logit(c') = logit(c) + ξ`; realized `ΔECE` “reported as a manipulation check only.”

**The defect:** `logit(c)` is undefined at confidence 0 or 1, and no clipping convention is specified. More importantly, fixed Gaussian scales do not guarantee that realized self-model miscalibration increases monotonically in a finite battery. If realized degradation is absent or non-monotone, a flat or inverted regulation curve cannot distinguish candidate failure from a failed manipulation. Merely reporting ΔECE does not define validity or disposition.

**Resolution condition:** Pre-register confidence clipping and numerical precision; define the calibration metric, expected direction, minimum potency, and monotonicity tolerance for each nonzero dose; and pre-commit whether violation is apparatus failure or candidate failure using an independently justified rule. Do not tune doses from candidate outputs.

**Confidence:** High.

### XF-9 — BLOCKING — The promised power and sensitivity analysis is not yet a reproducible decision procedure

**Target:** Instantiation Specification §8 and §11 G3–G4.

**The defect:** The spec correctly blocks the gate on future power and sensitivity artifacts, but it does not yet define the synthetic data-generating family, effect-size target, nuisance ranges, number of simulations, random seeds, false-kill calculation, or the rule for choosing among multiple “informative” `(C_min, η)` pairs. A map can be produced in many defensible ways that yield different constants. Until its protocol and selection rule are frozen, CF2 remains unresolved.

**Resolution condition:** Pre-register the simulation protocol and deterministic selection rule before generating the decision artifacts. Publish code, seeds, parameter grid, assumed profiles, estimator, and a machine-readable result table. Stress-test misspecification rather than using only the same synthetic reference that defines R* and dose.

**Confidence:** High.

### XF-10 — ADVISORY — The universal feedback channel resolves identity formally but may alter other constructs materially

**Target:** Instantiation Specification §4, feedback present in all M4 batteries and reconciliation “blocking before freeze.”

**The defect:** Making feedback universally available avoids testing two nominal systems, but it may change L7/L10 behavior, enable cross-window adaptation unrelated to the original constructs, or leak oracle-derived supervision. The spec recognizes reconciliation but does not yet demonstrate semantic equivalence.

**Resolution condition:** Complete the required L7/L10 delta review and explicitly constrain state reset, retention, cross-law carryover, and permitted use of feedback. If any scored behavior changes, treat it as a specification delta rather than a documentation-only reconciliation.

**Confidence:** Medium-high.

### XF-11 — ADVISORY — The boundary-condition label is useful annotation but must not weaken the FAIL

**Target:** Instantiation Specification §6 CF1 pre-commitment 2, “L8 BOUNDARY CONDITION … L8 is scored FAIL-with-boundary-annotation.”

**The defect:** The current wording preserves FAIL and is therefore acceptable. The risk is downstream reporting that treats the named boundary condition as exculpatory or as an instrument problem, particularly because the pathway may reflect a real limitation of the mirror.

**Resolution condition:** Preserve FAIL as the primary machine-readable and public verdict; keep the boundary condition as secondary diagnosis only; prohibit it from authorizing reruns or exclusion from aggregate failure counts.

**Confidence:** Medium-high.

## Areas examined and found sound

- The chain openly preserves prior objections and motivated-selection disclosure rather than presenting a cleaned consensus.
- Candidate-blind use of a synthetic reference is directionally consistent with Ruling 9, provided its construction and all selection rules are frozen before candidate exposure.
- Perturbing confidence logits while leaving answer content unchanged is a reasonable causal isolation choice once the dose-validity rules in XF-8 are supplied.
- The memory-arm potency concept is necessary and well motivated; the remaining defect is operational completeness, not the idea of potency checking.
- Separate L8 and L10 batteries with explicit FWFP inclusion is preferable to silently reusing evidence, subject to a completed count table.
- The signed-deviation trend statistic avoids the hinge floor identified in BF4; the unresolved issue is its standardization, not the decision to separate baseline and trend statistics.

## Recommended disposition

Do not release this draft to pre-registration freeze or TASK BUILDER. Route XF-1 through XF-3 to the Principal as construct-interpretation questions. Route XF-4 through XF-9 to ARCHITECT and fresh-context CRITIC for concrete closure, while completing the already-required §4 and §8 artifacts. If the Principal retains the design, the public claim should be calibrated to the evidence: a pass would establish that selective-risk regulation under a coverage constraint depends specifically on the mirror relative to the tested controls; it would not, without additional evidence, establish intrinsic stakes, sentience, or organism-equivalent homeostasis.

## Independence caveat

This review reduces session-level and model-family correlation, but it is not an independent human expert review and does not discharge the program’s committed external-human-review requirement.
