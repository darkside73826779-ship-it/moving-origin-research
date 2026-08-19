# CRITIC Handoff — Route to ARCHITECT: L8 Homeostatic-Variable Prerequisite BLOCK

**Gate served:** L8 implementation prerequisite gate (spec v1.6.2 §3.3.1, task spec §7) — BLOCK returned; TASK BUILDER held from L8 implementation
**Issued by:** CRITIC
**Date:** 2026-08-18 23:47 EDT
**Next recipient:** ARCHITECT
**Prior recipient:** WORKFLOW COORDINATOR (handed L8 prerequisite review to CRITIC)

---

## Authorization

CRITIC conducted the L8 homeostatic-variable prerequisite review (spec §3.3.1 + task spec §3.2/§7). This is a design-readiness gate, not a law-fidelity review (L8 law fidelity was cleared in v1.6.2: verbatim L8 quote byte-exact, L8 locked bars preserved, Ruling 3 APPROVED the standardized proximal-component approach). The prerequisite is **not cleared**: the approved L8 framework is not yet instantiated — the artifact gives examples and "predefine X" requirements, not the concrete definitions a TASK BUILDER needs to implement L8 without making design decisions. Returns to ARCHITECT for a narrow refinement; the regulation target specifically requires Rebecca sign-off per the existing `[PROPOSED]` tag.

**Authority chain:** Rebecca > constitution's laws > approved specifications > this handoff > ARCHITECT judgment. The ARCHITECT does not speak for Rebecca. Rebecca alone rules gates and merges.

---

## Verdict: BLOCK

**Block class:** design-readiness (the approved L8 framework is not yet instantiated), not law-fidelity.

The L8 definition returns to ARCHITECT for a narrow refinement. The TASK BUILDER remains held from L8 implementation until the prerequisite is re-cleared.

---

## SHAs and sources

| Item | Location | Status |
|---|---|---|
| M4 spec v1.6.2 | `specs/m4_specification.md` on main at `90a7e56` (PR #59) | §3.3.1 L8 prerequisite — BLOCKED |
| M4 task spec | `specs/m4_task_spec.md` on main at `d5f7b0f` (PR #62) | §3.2/§7 L8 — BLOCKED |
| CRITIC review | `reviews/critic_l8_prerequisite_review.md` on `critic/l8-prerequisite-review` | Committed + pushed |
| Constitution v1 | `docs/ARCHITECTURAL_CONSTITUTION.md` on main | Verbatim L8 law text (line 26) |
| M0 Decision Sheet | `docs/rulings/M0_DECISION_SHEET.md` on main | L8 bars (line 21) |
| Provenance log | `docs/rulings/provenance_log.md` on main | Through Entry 79 |
| Entry 76 | Provenance log | Ruling 3 (L8 zero-noise + severity-matched specificity) |

---

## Discriminator (implementation detail vs. design decision)

The review's test: is the definition complete enough that a TASK BUILDER can implement L8 without making design decisions?

- **Implementation detail** (TASK BUILDER may decide): code structure, data plumbing, function names, numerical computation mechanics that preserve already-specified semantics.
- **Design decision** (ARCHITECT + Rebecca must specify/pre-register before TASK BUILDER begins): anything that determines the construct being tested or could change whether L8 passes/fails — the homeostatic variable, target/setpoint, regulation-error formula, self-model noise mechanism, dose magnitudes/calibration rule, non-self component, severity-matching calibration set, tolerance.

---

## Four-criteria findings

### Criterion 1 — Regulable [LAW-L8] — CRITERION GAP

No homeostatic variable is named — only examples ("resource level, error budget, or calibration metric"). No setpoint, no bounds, no "healthy operation" range. "Regulation error = distance from target" is only operational once a specific variable and target exist. Depends on Criterion 2.

### Criterion 2 — Target defined [PROPOSED — requires Rebecca sign-off] — CRITERION GAP (PRIMARY BLOCKER)

No specific numeric value or bound — only a list of examples. The spec itself tags this `[PROPOSED — requires Rebecca sign-off]`, acknowledging the target is not yet defined. This cannot be cleared by the CRITIC and cannot be filled by the TASK BUILDER — Rebecca must name/approve the specific homeostatic variable and its regulation target. **Primary blocker.**

### Criterion 3 — Calibratable noise dose [OP-Entry 11.7] — CRITERION GAP (partial)

Dose levels 0/1/2/3 are ordinal with qualitative descriptors (none/small/moderate/large). BUT: (a) the noise injection MECHANISM is unspecified ("inject calibrated noise into the self-model" — additive Gaussian? multiplicative? activation perturbation? dropout?); (b) dose magnitudes are qualitative only. The noise channel/mechanism and dose-setting rule are the independent variable of the L8 dose-response test and affect the test's validity — the TASK BUILDER choosing them would be a design decision. (The Ruling 9 tolerance-calibration procedure §7.6 computes control-arm false-positive-rate tolerances, not L8 dose magnitudes or the noise mechanism — it does not close this gap.)

### Criterion 4 — Constructible specificity control [LAW-L8] — CRITERION GAP

The four Ruling-3 predefinitions are framed as "Predefine the comparison component…", "Predefine the perturbation type and magnitude…", "Predefine the calibration set…", "Predefine the tolerance…" — requirements to predefine, not actual predefinitions. No non-self-model component is named; no perturbation specified; no calibration set; no tolerance. The `[Rebecca-approved (Ruling 3, Entry 76)]` tags mean the APPROACH is approved, not that the four predefinitions are provided. A requirement to predefine is not the predefinition.

### Ruling 3 implementation check — NOT concrete enough

The four predefinitions are tagged [Rebecca-approved (Ruling 3, Entry 76)] (approach approved) but are NOT concretely provided. They are "to be pre-registered before any data exists" with no specified author or values. The approved framework is not yet instantiated.

---

## ARCHITECT scope of work (narrow refinement to instantiate the approved framework)

The ARCHITECT must supply:

1. **Named homeostatic variable** (closes C1) — a specific variable, not an example list.
2. **Numeric target/bound + regulation-error formula** (closes C2) — a specific setpoint or bound and the formula computing regulation error. **Requires Rebecca sign-off** per the existing `[PROPOSED — requires Rebecca sign-off]` tag (C2 is the primary blocker; Rebecca must name/approve the specific target).
3. **Self-model noise injection mechanism + dose calibration rule** (closes C3) — what "calibrated noise" is operationally and how dose magnitudes are set across levels 0–3.
4. **The four Ruling-3 predefinitions** (closes C4) — actual comparison component, perturbation, calibration set, and tolerance (or a candidate-blind, oracle-grounded procedure for setting them, consistent with Ruling 9's candidate-blind principle; all pre-registered before any data exists per [LAW-L19]).

After ARCHITECT refinement and Rebecca sign-off on the target, the L8 prerequisite returns to CRITIC for re-clear.

---

## STOP / escalation triggers for Rebecca

- **C2 (regulation target) requires Rebecca sign-off** per the existing `[PROPOSED — requires Rebecca sign-off]` tag. Rebecca must name/approve the specific homeostatic variable and its regulation target. This is the primary blocker and cannot be resolved by the ARCHITECT or CRITIC alone.
- Task spec §11 STOP trigger invoked: "If the homeostatic variable cannot meet all four prerequisite criteria, STOP and escalate to ARCHITECT for revision."

---

## Preserved evidence

L8 law fidelity remains cleared (v1.6.2): verbatim L8 quote byte-exact against constitution line 26; L8 locked bars preserved (≥3 doses, ρ≥0.8, slope≥0.2, specificity, 5 seeds); Ruling 3 APPROVED the standardized proximal-component approach (Entry 76). This block is about implementation-readiness (the framework is approved but not instantiated), not about law fidelity or the ruling. No locked bar, kill condition, or scoring predicate is in question.

---

## Prohibited-action confirmation (CRITIC)

No modification of the spec, task spec, constitution, or any artifact (read-only + this handoff and the review file only); no merge to main; no implementation/scoring/seed execution/hold-out seed exposure; no L15/L16/L17 before M5; no design decisions (gaps flagged, not filled); O-14/O-15 honored. The TASK BUILDER remains held from L8 implementation pending re-clear.

---

## Public-repository pre-push scan attestation

Before pushing this handoff, the CRITIC self-scanned `handoffs/CRITIC_L8_PREREQUISITE_BLOCK_HANDOFF.md` for credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII.

**Scan result:** No prohibited content found. The handoff contains only SHA hashes, branch names, line numbers, and spec/provenance text already public in the repository. No credentials, tokens, private absolute paths, hostnames, MAC addresses, SIDs, or PII present. **Classification: acceptable.** Attestation logged per `PUBLIC_REPOSITORY_POLICY.md` §3.

---

## Next authorized role

**Next recipient:** ARCHITECT — narrow refinement of the L8 homeostatic-variable definition to instantiate the approved framework: named variable (C1), numeric target/bound + regulation-error formula requiring Rebecca sign-off (C2, primary), self-model noise mechanism + dose calibration rule (C3), and the four Ruling-3 predefinitions (C4). After ARCHITECT refinement and Rebecca sign-off on the target, returns to CRITIC for re-clear.

The TASK BUILDER is held from L8 implementation until the prerequisite is re-cleared. (Other M4 harness work not blocked by this prerequisite — scaffold, L7, L10, L14, L18, FWFP closure audit — may proceed per the WORKFLOW COORDINATOR's sequencing; only L8 implementation is gated on this prerequisite.)

**Explicitly prohibited downstream:** no modification of locked bars/threshold values/kill conditions/scoring predicates; no scoring run or fresh-seed execution until Rebecca authorizes via courier; no rerun of seeds 201–203/301–303 (O-14); no L15/L16/L17 before M5; no design decisions by the TASK BUILDER on the L8 construct (variable/target/noise-mechanism/specificity-component) — these are ARCHITECT + Rebecca decisions; no post-candidate tolerance adjustment (Ruling 9); no candidate diagnostic seeds 101–105 as tolerance-calibration inputs (Ruling 9); no merge to main except by Rebecca.
