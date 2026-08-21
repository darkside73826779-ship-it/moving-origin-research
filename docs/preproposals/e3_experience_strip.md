# E3 PRE-PROPOSAL — Sequential Fast-Weight Experience Strip ("the tape")
**Status:** IDEA-STAGE PRE-PROPOSAL — parked pending M4/M5 completion. Not a specification. Authorizes nothing.
**Author:** Advisor session, from the Principal's concept (weight-based sequential memory, revived from the glial-substrate program under its extracted findings)
**Date:** 2026-08-19
**Sequencing:** Blocked behind (1) M4 completion, (2) M5 completion, (3) the episodic log substrate (prerequisite P1 below). Target: first post-M5 E-series candidate.

---

## 1. Construct

A **dual-write memory architecture** for the harness organism:

- **System of record (the log):** append-only episodic store (data, not weights). Every event written raw with wall-clock stamp and origin-relative position at write time. Canonical, auditable, citable. This is Tier 1 of the tiered memory architecture; it is a *prerequisite*, not part of E3's novelty.
- **System of experience (the strip):** a logical line of N small plastic weight chunks (adapter-block scale) over a frozen backbone. A **write head** exposes exactly one chunk to plasticity at a time and advances along the line in sync with the moving origin. Events train the active chunk via cheap local updates (Hebbian/outer-product or light gradient steps on an experience-prediction loss). Reads occur via attention over chunk outputs, **gated by origin-distance** — temporal queries bias toward strip positions behind the arrow.
- **Sleep boundary:** when the head reaches end-of-strip (nominally end-of-day), consolidation runs: Tier 2 summaries are distilled **from the log** (preserving provenance), and the strip is released for overwrite. Strip overwrite is not memory loss; the strip was never the record.

**Claimed contribution:** the strip supplies fast, associative, recency-textured within-day recall (the experiential layer) that a query-driven log cannot supply at equivalent cost; the log supplies the verbatim, auditable record that weights cannot supply at all. Position-on-strip is temporally indexed *by construction*, making the write head a physical realization of the moving origin's arrow.

**Novel instrument:** the **tape–log divergence metric** — for a fixed probe set, the discrepancy between strip-mediated recall and log ground truth is a direct, quantitative measure of reconstructive memory distortion with verbatim ground truth. To our knowledge no clean artificial-system measurement of this exists.

## 2. Explicit non-claims (L20 discipline)

The strip is not the system of record and is never cited as evidence of what occurred. No claim of biological equivalence to hippocampal fast plasticity is made; the lineage (fast weights, NTM/DNC external-memory architectures, complementary-learning-systems theory) is motivation, not asserted mechanism. No consciousness or awareness claim attaches to any E3 outcome.

## 3. Inherited scar tissue (glial-substrate findings, binding)

The predecessor weight-memory program was terminated when its headline organization result proved entirely attributable to mean-centering, and components proved removable without mutual effect. E3 therefore inherits as **mandatory controls**:
- **C-MC (mean-centering control):** every organization/recall effect must survive the exact normalization ablation that killed the glial result. Pre-registered.
- **C-REM (removability):** the strip must fail the removability test — i.e., its removal must measurably degrade within-day function (see three-property bars). A strip that can be removed without effect is decorative and dies.
- **C-ILL (illusion audit):** any claimed structure on the strip (temporal gradient, chunk specialization) must be shown against shuffled-write and frozen-strip controls before being reported as organization.

## 4. Three-property test (pre-registration skeleton — bars TBD at spec stage)

Per the program's standing candidate test, the strip must show, against a no-strip baseline with identical log access:
1. **Correctness:** strip-mediated within-day associative recall (probe classes: recency-cued, content-resonance, sequence-order) exceeds baseline at bars to be locked at spec stage.
2. **Operational distinctness:** the advantage holds under a cost/latency envelope the log-query baseline cannot match as within-day history grows (scaling-separation design mirroring E1).
3. **Load-bearing coupling:** calibrated corruption of the strip (dose-graded noise on chunk weights; head desynchronization from the origin) degrades within-day performance dose-dependently. Frozen-strip and shuffled-write arms must not show the dose response (specificity).

**Kill conditions (draft):** failure of C-REM; any headline effect eliminated by C-MC; three-property failure on pre-registered bars. Negatives retained per standing rules.

## 5. Constitutional touchpoints (to be resolved at spec stage)

- **L14 (stakes touch everything or nothing):** a load-bearing strip makes memory quality intrinsically coupled to regulation — potentially converting the L8/L14 memory coupling from harness contrivance toward candidate-owned machinery (responsive to cross-family finding XF-1's ownership objection). This is an opportunity, not a claim; it must be argued at spec stage.
- **L16-class integration laws:** strip ↔ origin head synchronization is a new interface; ablation matrix required before any integration claim.
- **L19:** all probe classes, bars, dose schedules, and the divergence metric's definition pre-registered before data.
- **Ruling 9 pattern:** any calibration (dose magnitudes, probe difficulty) candidate-blind, from synthetic/oracle profiles.

## 6. Prerequisites and sequencing

- **P1 (blocking):** the episodic log substrate (Tier 0–2 tiered memory with origin-indexed bands) must exist in the harness first — the strip is meaningless without the record it runs beside. P1 is the natural first post-M5 integration milestone and is independently valuable.
- **P2:** M4's mirror/abstention machinery (recall-coverage honesty draws on it).
- E3 does not touch M4 scope, scoring seeds, or any active gate. This document parks the idea; it costs the program nothing until invoked.

## 7. Open design questions (the adversarial chain's starting ammunition)

1. Chunk count N, chunk capacity, and head advance policy (fixed clock vs. event-density adaptive) — and whether adaptive advance quietly reintroduces a tuned free parameter.
2. Write rule: Hebbian outer-product vs. gradient steps — cross-talk/interference characterization across chunk boundaries.
3. Read gating: exact form of origin-distance bias; risk that the gate alone (not stored content) produces the recency advantage — needs a gate-only control arm.
4. Divergence metric formalization: probe design that separates *distortion* from *absence*; scoring against verbatim log.
5. Whether the strip's advantage survives honest accounting of the log's own caching/indexing optimizations (the "fair-naive" problem, E1 edition).
6. Consolidation interaction: does distilling Tier 2 from the log (not the strip) discard genuinely strip-resident signal, and is that acceptable by design?

## 8. Disposition requested (when invoked)

Enter the standing design pipeline as the L8 chain did: advisor proposal → critic pass → advisor revision → critic re-review → cross-family review → ARCHITECT specification → fresh-context CRITIC → Principal gate → pre-registration freeze → build. The Principal remains sole gate authority throughout.
