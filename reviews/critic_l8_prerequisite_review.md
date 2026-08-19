# CRITIC L8 Homeostatic-Variable Prerequisite Review

**Gate served:** L8 implementation prerequisite gate (spec v1.6.2 §3.3.1, task spec §7) — must be cleared BEFORE the TASK BUILDER begins L8 implementation
**Reviewer:** CRITIC (fresh-context; prior reviews v1.5 CLEAR, v1.6 BLOCK→v1.6.1→v1.6.2 CLEAR)
**Date:** 2026-08-18 23:47 EDT
**Spec under review:** `specs/m4_specification.md` on main at **`90a7e56`** (v1.6.2, merged PR #59); `specs/m4_task_spec.md` on main at **`d5f7b0f`** (PR #62)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this review > agent judgment. CRITIC does not speak for Rebecca.

---

## Verdict: BLOCK

The L8 prerequisite is **not cleared**. The prerequisite artifact (spec §3.3.1 + task spec §3.2/§7) does not yet instantiate the approved L8 framework: it gives examples and "predefine X" requirements, but does not provide the concrete definitions a TASK BUILDER needs to implement L8 without making design decisions. The TASK BUILDER remains held from L8 implementation. The L8 definition returns to the ARCHITECT for a narrow refinement; the regulation target specifically requires Rebecca sign-off per the existing `[PROPOSED]` tag.

This is a design-readiness block, not a law-fidelity defect. Law fidelity for L8 was cleared in the v1.6.2 delta review (verbatim L8 quote byte-exact; L8 locked bars preserved). The four criteria below are about implementation-readiness: is the definition complete enough that a TASK BUILDER can implement it without making design decisions?

**Line between implementation detail and design decision (the discriminator):** implementation detail = code structure, data plumbing, function names, numerical computation mechanics that preserve already-specified semantics. Design decision = anything that determines the construct being tested or that could change whether L8 passes/fails — the homeostatic variable, target/setpoint, regulation-error formula, self-model noise mechanism, dose magnitudes/calibration rule, non-self component, severity-matching calibration set, tolerance. Those must be specified/pre-registered before the TASK BUILDER begins.

---

## The four criteria

### Criterion 1 — Regulable [LAW-L8] — CRITERION GAP

Spec/task-spec text: "Define ≥ 1 [LAW-L8] homeostatic variable with a regulation target. The candidate maintains this variable (e.g., a resource level, error budget, or calibration metric) that should stay within bounds for healthy operation." "Regulation error" is defined as "how far it deviates from its target."

**Gap:** no homeostatic variable is named — only a list of examples ("resource level, error budget, or calibration metric"). No setpoint, no bounds, no "healthy operation" range. "Regulation error = distance from target" is only operational once a specific variable and target exist. Since no variable or target is defined, "regulable" cannot be verified concretely. This criterion depends on Criterion 2 (the target).

### Criterion 2 — Target defined [PROPOSED — requires Rebecca sign-off] — CRITERION GAP (PRIMARY BLOCKER)

Spec text: "The regulation target is a specific numeric value or bound, not a vague aspiration." Task spec §2.4 lists "L8 homeostatic variable regulation target | Specific numeric value or bound | [PROPOSED — requires Rebecca sign-off] | Spec §3.3.1."

**Gap (primary blocker):** the target is not a specific numeric value or bound — it is a list of examples with no named variable, no setpoint, no quantifiable target. The spec itself tags this `[PROPOSED — requires Rebecca sign-off]`, acknowledging the target is not yet defined and requires Rebecca's sign-off. This cannot be cleared by the CRITIC and cannot be filled by the TASK BUILDER — it requires Rebecca to name/approve the specific homeostatic variable and its regulation target. This is the primary blocker; Criteria 1, 3, and 4 are dependent on or additional to it.

### Criterion 3 — Calibratable noise dose [OP-Entry 11.7] — CRITERION GAP (partial)

Spec text: "Inject calibrated noise into the self-model (the L7 mirror component — the candidate's self-state representation) at ≥ 3 dose levels": Level 0 (zero-noise), Level 1 (low, "small perturbation"), Level 2 (medium, "moderate perturbation"), Level 3 (high, "large perturbation").

**Gap:** the dose levels are defined ordinally (0/1/2/3) but (a) the noise injection MECHANISM is unspecified — "inject calibrated noise into the self-model" does not state what calibrated noise is operationally (additive Gaussian on weights? multiplicative? activation perturbation? dropout?); and (b) dose magnitudes are qualitative only ("small/moderate/large"). The noise channel/mechanism and dose-setting rule affect the test's validity — they are the independent variable of the L8 dose-response test — so the TASK BUILDER choosing them would be a design decision, not an implementation detail. (Note: the Ruling 9 tolerance-calibration procedure, §7.6, computes control-arm false-positive-rate tolerances under O-15; it does not define the L8 dose magnitudes or noise mechanism, so it does not close this gap.)

### Criterion 4 — Constructible specificity control [LAW-L8] — CRITERION GAP

Spec text (Ruling 3, standardized proximal-component effect): "Predefine the comparison component…", "Predefine the perturbation type and magnitude…", "Predefine the calibration set…", "Predefine the tolerance…"

**Gap:** these four items are framed as requirements to predefine, not as actual predefinitions. No non-self-model component is named; no perturbation type/magnitude is specified; no calibration set is defined; no tolerance is given. The tags `[Rebecca-approved (Ruling 3, Entry 76)]` mean the APPROACH (standardized proximal-component effect, predefining these four) is approved — not that the four predefinitions are provided. A requirement to predefine is not the predefinition. The TASK BUILDER cannot construct the specificity control without making design decisions (which component, what perturbation, etc.).

### Ruling 3 implementation check — NOT concrete enough for implementation

The four predefinitions (comparison component, perturbation, calibration set, tolerance) are tagged `[Rebecca-approved (Ruling 3, Entry 76)]` (approach approved) but are NOT concretely provided in the spec or task spec. They are stated as "to be pre-registered before any data exists" with no specified author or values. This is not concrete enough for implementation — the approved framework is not yet instantiated.

---

## Recommendation: return to ARCHITECT for narrow refinement

The ARCHITECT must concretely instantiate the approved L8 framework by supplying:

1. **Named homeostatic variable** (closes C1) — a specific variable, not an example list.
2. **Numeric target/bound + regulation-error formula** (closes C2) — a specific setpoint or bound and the formula computing regulation error. This requires Rebecca sign-off per the existing `[PROPOSED — requires Rebecca sign-off]` tag (C2 is the primary blocker; Rebecca must name/approve the specific target).
3. **Self-model noise injection mechanism + dose calibration rule** (closes C3) — what "calibrated noise" is operationally and how dose magnitudes are set across levels 0–3.
4. **The four Ruling-3 predefinitions** (closes C4) — actual comparison component, perturbation, calibration set, and tolerance (or a candidate-blind, oracle-grounded procedure for setting them consistent with Ruling 9's candidate-blind principle; note these must be pre-registered before any data exists per [LAW-L19]).

The CRITIC does not fill these gaps (role boundary: no design decisions). After ARCHITECT refinement (and Rebecca sign-off on the target), the L8 prerequisite returns to CRITIC for re-clear.

---

## STOP / escalation triggers

- **C2 (regulation target) requires Rebecca sign-off** per the existing `[PROPOSED — requires Rebecca sign-off]` tag. Rebecca must name/approve the specific homeostatic variable and its regulation target. This is the primary blocker and cannot be resolved by the ARCHITECT or CRITIC alone.
- Task spec §11 STOP trigger (line 409): "If the homeostatic variable cannot meet all four prerequisite criteria, STOP and escalate to ARCHITECT for revision." — invoked.

---

## Preserved evidence

Law fidelity for L8 remains cleared (v1.6.2): verbatim L8 quote byte-exact against constitution line 26; L8 locked bars preserved (≥3 doses, ρ≥0.8, slope≥0.2, specificity, 5 seeds); Ruling 3 APPROVED the standardized proximal-component approach (Entry 76). This block is about implementation-readiness (the framework is approved but not instantiated), not about law fidelity or the ruling. No locked bar, kill condition, or scoring predicate is in question.

---

## Prohibited-action confirmation (CRITIC)

No modification of the spec, task spec, constitution, or any artifact (read-only + this review file only); no merge to main; no implementation/scoring/seed execution/hold-out seed exposure; no L15/L16/L17 before M5; no design decisions (gaps flagged, not filled); O-14/O-15 honored. The TASK BUILDER remains held from L8 implementation pending re-clear.

---

## Public-repository pre-push scan attestation

Before pushing this review, the CRITIC self-scanned `reviews/critic_l8_prerequisite_review.md` for credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII.

**Scan result:** No prohibited content found. The review contains only SHA hashes, branch names, line numbers, and spec/provenance text already public in the repository. No credentials, tokens, private absolute paths, hostnames, MAC addresses, SIDs, or PII present. **Classification: acceptable.** Attestation logged per `PUBLIC_REPOSITORY_POLICY.md` §3.

---

## Next authorized role

**Next recipient:** ARCHITECT — narrow refinement of the L8 homeostatic-variable definition to instantiate the approved framework: named variable (C1), numeric target/bound + regulation-error formula requiring Rebecca sign-off (C2, primary), self-model noise mechanism + dose calibration rule (C3), and the four Ruling-3 predefinitions (C4). After ARCHITECT refinement and Rebecca sign-off on the target, returns to CRITIC for re-clear.

The TASK BUILDER is held from L8 implementation until the prerequisite is re-cleared. (Other M4 harness work not blocked by this prerequisite — scaffold, L7, L10, L14, L18, FWFP closure audit — may proceed per the WORKFLOW COORDINATOR's sequencing; only L8 implementation is gated on this prerequisite.)

**Explicitly prohibited downstream:** no modification of locked bars/threshold values/kill conditions/scoring predicates; no scoring run or fresh-seed execution until Rebecca authorizes via courier; no rerun of seeds 201–203/301–303 (O-14); no L15/L16/L17 before M5; no design decisions by the TASK BUILDER on the L8 construct (variable/target/noise-mechanism/specificity-component) — these are ARCHITECT + Rebecca decisions; no post-candidate tolerance adjustment (Ruling 9); no candidate diagnostic seeds 101–105 as tolerance-calibration inputs (Ruling 9); no merge to main except by Rebecca.
