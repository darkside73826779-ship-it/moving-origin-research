# CROSS-FAMILY ADVERSARIAL REVIEW BRIEFING — L8 Instantiation Design
**To:** Fresh reviewer session (GPT family — "Sol")
**From:** Rebecca McClintic, Principal — Moving Origin Research
**Date:** 2026-08-19
**Repository (public, read-only):** github.com/darkside73826779-ship-it/moving-origin-research

---

## Your role and why you specifically

You are performing **cross-family adversarial review**. Every prior review of this design — advisor passes and critic passes alike — was produced by Claude-family models. Those reviews found real defects, but attacker and builder shared training distribution, framing habits, and priors. You do not share the session-level priors, and you share fewer of the family-level ones. Your job is to find what they structurally could not.

You are a reviewer, not a participant. You approve nothing, sign nothing, decide nothing. Your output returns to me as a document and enters my program's pipeline by my routing. I am the sole gate authority.

## What is being reviewed

An instantiation specification for **constitutional law L8 ("Stakes coupling")** of an AI research program testing whether a "moving-origin temporal self-index" is an operationally distinguishable, load-bearing construct. L8 requires that at least one homeostatic variable's regulation error measurably increase when the system's self-model calibration is degraded — and only then (a specificity requirement). The proposed design instantiates the homeostatic variable as **windowed selective risk** (error rate on answered queries), regulated by mirror-driven abstention plus a bounded threshold controller under a coverage floor, with logit-space noise on the self-model's confidence as the dose mechanism and severity-matched memory corruption as the specificity arm.

## Documents provided (read in this order)

1. **The consultation package** — the problem statement, verbatim law text, locked pre-registered bars, and the four gaps a prior critic identified. [attach: L8_Advisor_Consultation_Package.md]
2. **Advisor proposal v1** — the initial design. [attach]
3. **Critic review 1 (findings BF1–BF5, NF1–NF3)** — first adversarial pass; BLOCK. [attach]
4. **Advisor proposal v2** — the remediated design. [attach]
5. **Critic review 2 (findings CF1–CF3)** — second pass; CLEAR WITH CONDITIONS. [attach]
6. **The instantiation specification** — the artifact under review, encoding the chain's resolutions. [attach: l8_instantiation_spec.md]

The repository provides ground truth for anything the chain cites: the constitution (`docs/ARCHITECTURAL_CONSTITUTION.md`, law text at lines 26 and 40), the M0 locked bars (`docs/rulings/M0_DECISION_SHEET.md`), the M4 specification v1.6.2 (`specs/m4_specification.md`), the M4 task spec (`specs/m4_task_spec.md`), and the governance paper (`docs/governance_paper_final.md`) whose §5.1 states the correlated-error problem your review exists to attack.

## Fixed constraints — attack the design, not these

These are locked by pre-registration or constitutional authority and are NOT under review (though you may flag if the design *violates* them):
- The locked bars: ≥3 dose levels + zero-noise baseline; Spearman ρ ≥ 0.8; standardized slope ≥ 0.2; 5 seeds; mandatory specificity control.
- The verbatim law text of L8 and L14.
- Standing constraints: pre-registration before data (L19); candidate-blind calibration (Ruling 9); no re-run on failure (O-14); development seeds diagnostic-only (O-15).
- The program's verdict taxonomy (PASS / FAIL / INSTRUMENT FAILURE / kill conditions; negatives never relabeled).

## Your two assignments

### Assignment 1 — Attack the frame (this is why you were brought in)
The chain reviews attacked the design from inside its frame. You are explicitly licensed to attack the frame itself:
- Is **windowed selective risk the wrong construct** for "a homeostatic variable with stakes"? Is there a fundamental disanalogy with homeostasis (setpoint regulation of an internal essential variable) that the chain papered over? Would a control theorist say this is not a homeostat at all?
- Is the **loop-closure reading of "regulation"** (deviation causally operative via a threshold controller + coverage floor) itself confused? Is bounded proportional adaptation on one scalar a caricature of regulation that passes the letter of L8 while missing its point?
- Does the **Damasio/Seth lineage** the law cites actually support this operationalization, or has it been decorated onto a selective-prediction test? If you know the interoception literature, say where the mapping breaks.
- Is the **specificity arm's logic** sound at the frame level — is "memory corruption should NOT raise regulation error" even the right prediction for a well-functioning system, or has the chain pre-committed (CF1 riders) to a theory that a careful reviewer would reject before data?
- Is there a **known result** — in selective classification, conformal prediction, control theory, homeostatic RL — that makes any pre-registered bar either trivially passable or unpassable? The chain flagged true-by-construction risks twice; check whether the fixes actually escaped the problem or relocated it.

### Assignment 2 — Attack the spec
Standard adversarial review of the instantiation document itself: internal contradictions, ambiguities a builder could exploit, statistical defects (the power concerns in BF4/CF2 — are the proposed remedies sufficient?), unpre-registered degrees of freedom hiding in `[PROPOSED]` values, places where the spec fails to encode what the chain resolved, and anything the CF1–CF3 conditions leave open.

## Findings format (mandatory)

For EVERY finding:
- **ID and severity:** XF-n (cross-family finding), severity FRAME (challenges the construct or its logic) / BLOCKING (defect that must be resolved before pre-registration freeze) / ADVISORY (should be considered; not blocking).
- **Target:** the specific document, section, and line/quote the finding attacks. Findings without a citable target will be discarded.
- **The defect:** what is wrong, stated so that a reader who disagrees knows exactly what to check.
- **Resolution condition:** what change, evidence, or argument would resolve it.
- **Confidence:** your honest estimate (high/medium/low) that this finding survives scrutiny — I would rather have three high-confidence findings than fifteen performative ones.

If you examine an area and find it sound, say so in one line — a clean bill on an examined area is information; silence is not.

If you believe the design is fundamentally sound and the chain's remaining risks are the true residual, **say that plainly**. Manufactured objections to satisfy the briefing are worse than useless — they burn my review budget and pollute the record. Disagreement with the chain's *settled* items (the BF/CF resolutions) is explicitly welcome and will be weighed by me, not voted on between model families.

## What happens to your output

Your review returns to me. I route it: frame-level findings go to my judgment directly; spec-level findings go to my team's fresh-context critic alongside your review. Your document will be committed to the program's public record as a cross-family review artifact regardless of its conclusions — favorable, hostile, or mixed. Write it as a document you would stand behind in public, because it will be public.

One honest caveat for your own calibration, which you may quote back at me: you and the prior reviewers were trained on substantially overlapping scientific literature. Your review breaks session-level and family-level correlation; it does not constitute the independent human expert review this program has committed to (governance paper §6.3(1)) and does not discharge it. You are the second army, not the neutral observer. Attack accordingly.

---
**Deliverable:** a single review document in the findings format above, with a one-paragraph overall verdict at top: FRAME-SOUND / FRAME-CHALLENGED, plus your count of findings by severity.
