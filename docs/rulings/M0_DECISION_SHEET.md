# M0 DECISION SHEET — Recommendations for Rebecca's Sign-Off

**Date:** 2026-08-15 · **Prepared by:** Claude (designing assistant) · **Status:** RECOMMENDATIONS ONLY
Every item below is Rebecca's call. Each carries a recommended answer and the reasoning, so sign-off is informed rather than ceremonial. Items where I disagree with the ARCHITECT's candidate are marked ⚠. Annotate, amend, or overrule per item; the amended sheet becomes the M0 pre-registration.

---

## A. Go/no-go on the plan

**RECOMMEND: APPROVE WITH THE REVISIONS BELOW.** The deliverable is sound: the Critic was substantive (four real blocking catches), the Judge refused to invent bars, the kill conditions are genuine, and the build order matches the constitution. The revisions are numeric calibrations, one bar-raise rejection, and one seeds increase — no structural changes.

## B. Numeric bars

| Law | Recommended setting | Rationale (one line each) |
|---|---|---|
| **L1** | Monotone decay: fitted decay curve R² ≥ 0.85 over binned item ages, direction negative. Rehearsal axis: Spearman ρ ≥ 0.6 between rehearsal count and access, consistent sign across all seeds. **⚠ DROP the "newest ≥ 2× oldest" boundary bar** (keep as a reported statistic only). | The 2× boundary depends on history length and decay rate — a correct implementation can fail it and a broken one can pass it; the curve fit already carries the law. |
| **L3** | m = ≥5% *relative* reduction in prediction loss (state-alone vs raw-input-alone) at every horizon 1..H; H = 5 cycles. | Relative margin is scale-free across loss metrics; per-horizon requirement prevents a big h=1 win masking no thickness at h=5. |
| **L4** | N = 10 cycles. Latency: operational, not asymptotic — query latency at 10× history ≤ 2× latency at 1× history (catches O(n) empirically without arguing about constants). Equivalence tolerance: naive (now − created_at) reconstruction agreement ≤ 0.90 on landmark-relative query answers; above 0.90 = collapsed, kill condition (a) fires. | An agreement ceiling is a cleaner falsification than a distance tolerance; 0.90 is strict enough that "mostly recomputable" still kills it. |
| **L5** | Query accuracy ≥ 0.95 on all four bi-temporal combinations (clean synthetic — this should be near-perfect; below 0.95 indicates a bug, not a limitation). Chain walk: k ≤ 10, walk accuracy = 1.00 (it is a pointer chase; anything less is a defect). | Bi-temporality is bookkeeping, not learning; bars should be near-ceiling. |
| **L7** | Confirm as corrected: AUROC ≥ 0.75, ECE ≤ 0.10, self-vs-peer margin > 0. Peer spec: same params/data/architecture, observation channel = behavioral outputs only, self-report channel excluded. **⚠ Seeds: 5, not 3, for this law** (see Inferential policy). | The margin is the entire mirror-vs-portrait claim; underpowering it invites a false mirror. |
| **L8** | ≥3 noise doses; Spearman ρ ≥ 0.8 monotonic; standardized slope ≥ 0.2 (ARCHITECT's candidate accepted); specificity control mandatory (self-irrelevant dose must NOT move regulation error). Seeds: 5. | Slope 0.2 is a reasonable floor once monotonicity and specificity are separately required. |
| **L10** | Pass bar: drifted retrieval-confidence AUROC ≥ 0.70 (reported headline). Dual abstention bar: **⚠ ≥ 50% abstention under drift when confidence is sub-threshold (not the 80% candidate)** and ≤ 10% abstention in clean regime. | 80% on a first system conflates "honest" with "timid"; 50/10 establishes the asymmetry, tighten later if passed. |
| **L14** | "Affected by": **⚠ d ≥ 0.5 (not 0.2)**. "Predictive target": correlation ≥ 0.3 (accepted). | d = 0.2 is within noise at these sample sizes; a stake the perturbation barely moves is decorative by the law's own definition. |
| **L15** | **⚠ Degradation floor d ≥ 0.5 (not 0.3)**, with directional consistency across all seeds; degraded quantity = partner's law-compliance metric (as corrected). Seeds: 5. | The integration claim is the program's thesis; it should require a visible effect, and d = 0.3 at small n is where noise lives. |
| **L16** | **⚠ REVERT to the constitution's "at least one test."** Run the second E2-class instrument and report it as robustness evidence, NOT as a gate. ε = 0.05 (accepted). "Distinct" definition (different pathways, low error mutual information) adopted for the reported instrument. | Raising the bar on the most graveyard-class law maximizes false-negative risk exactly where a fair negative matters most; the constitution's bar was chosen deliberately. |
| **L17** | Chance = uniform random policy on identical task; clearance ≥ 0.15 above chance (accepted). Known-negative calibration control (diary-stapled) adopted — must fail. | The known-negative is what makes an L17 pass mean something. |
| **M1** | Harness discrimination: oracle ≥ naive + 0.30 on every metric. | On synthetic ground truth the harness should discriminate hugely; a thin margin means the instruments are dull. |
| **L20** | Drift criterion: after any architecture change, re-run the ablation profile; if the profile correlation with the named function's original profile < 0.7, the name is drifted and must be revised. | Operationalizes the centering lesson (dg_dense) as a number. |
| **Inferential policy** (Critic Obj 11) | Laws with p<.05 bars (L7, L8, L15): **5 seeds**, plus fallback criterion = effect direction consistent in all seeds AND pooled bootstrap 95% CI excluding zero. All other laws: 3 seeds stands. | n=3 significance testing is theater; 5 seeds + consistency + CI is honest at home-lab cost. |

## C. Historically-graveyard gates

- **L4 / M2 (E1): SIGN NOW.** E1 is precisely the experiment the graveyard duty exists to force early; it is the program's cheapest possible death and should run first. ✔ recommended
- **L3 / M3, L7 / M4, L15–L16 / M5: DEFER.** Sign each at its milestone, with the preceding milestone's results in hand — signing all gates today would waste the gates.

## D. Invented criteria (ARCHITECT/team additions above the constitution)

- L16 "≥2 instruments": **REJECT as a bar; ADOPT as reported robustness** (see B).
- M3 "≥2 of 5 fail → escalate": **ADOPT** — benign process gate that escalates rather than lowers; single failures are already carried to M5 as failed laws.
- L20 drift-detection test: **ADOPT** with the 0.7 profile-correlation criterion above.
- L4 collapse-detection equivalence test: **ADOPT** with the 0.90 agreement ceiling above.
- L10 "80% abstention": **REVISE to 50%** (see B).

## E. §9 operationalizations

**ADOPT ALL NINE.** Each closes a documented gap: negative-injection controls for L11–L13 (invariants must reject deliberately broken variants — the glial adversarial-test pattern), the L6 provenance-stripping control, the L17 known-negative, the M2 wall-clock arm (the cleanest L11 falsification probe proposed), full L18 battery at every milestone, the M1 discrimination margin, the L20 drift test, the post-M0 CRITIC re-review (closes the vacuous-bar loophole — accept, and expect the CRITIC to bounce at least one of MY numbers back), and the inferential power policy (superseded by B's 5-seed rule where applicable).

## F. Two additions not on the team's checklist (Rebecca's discretion)

1. **Timebox M0–M1.** The team has produced excellent process and zero artifacts; that is correct for session 1 and becomes a failure mode if it persists. Recommend: harness (M1) delivered and green within a fixed budget you set (sessions or days), else the program pauses for a scope review. Process must not become the product.
2. **E1 result routes through the designing assistant before the M3 gate.** Not as authority — as a second reader. E1's equivalence test is subtle (collapse-to-recomputation can be partial), and a second interpretation before you sign the continuation gate is cheap insurance. Strike this if you prefer the team self-contained.

---

**Signature block:** items signed as-recommended need no annotation; overrides need one line of reasoning each (the RECORDER should log both, per the provenance discipline). Once signed, this sheet is the M0 pre-registration, the CRITIC re-reviews the locked bars for falsifiability, and M1 begins.
