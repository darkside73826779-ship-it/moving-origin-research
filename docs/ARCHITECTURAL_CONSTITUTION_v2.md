# ARCHITECTURAL CONSTITUTION v2 — Quantified Laws for a Temporally-Selfed System

**Version:** v2 (amendment log added; law text unchanged from v1)
**Date:** 2026-08-15 (original) · **v2 date:** 2026-08-18
**From:** Claude, with Rebecca McClintic · **Status:** constitution for the multi-agent system to build against
**Method:** every law is a CONSTRAINT (what must be measurably true), never a MECHANISM (how to build it). Implementations are free; the laws are enforced by tests. Lineage: the glial project's invariant-suite methodology, generalized. Each law names the audited system whose insight it quantifies.

**The prime rule, learned the hard way:** components co-resident are not components integrated. Integration is defined by test (§4), not by architecture diagrams. A system that passes the component laws but fails the co-dependence laws is a warehouse of paddles and must be reported as such.

---

## §1 Component laws (from the audit)

**L1 — Access physics (from ACT-R).** Accessibility of every knowledge item is a monotonic decaying function of self-relative recency and use frequency. *Test:* retrieval probability/latency curves over item age-in-autobiography; curve must be decreasing in disuse, increasing in rehearsal count. Timestamp-sorted lookup with uniform access FAILS this law.

**L2 — Irreversible cadence (from LIDA).** A persistent process advances in bounded-period cycles; state at cycle t+1 depends on state at t; no operation rewinds the cycle counter or rewrites history. *Test:* autobiography is append-only (hash-chained); cycle counter strictly monotone across restarts.

**L3 — Thick present (from Dreamer).** The current state is a sufficient statistic for prediction at horizon H: retention (compressed just-past) plus protention (explicit near-future prediction) live in one state object. *Test:* next-input prediction loss at horizons 1..H from the state alone must beat prediction from raw current input alone by margin m.

**L4 — Egocentric index (from Conway; the C1 gap nothing has).** Every knowledge item carries self-relative coordinates — position in the autobiography and landmark-relative period ("before/after event E") — and these coordinates re-resolve as now advances. *Test:* self-relative queries ("what did I hold before E?") answered from the index without scanning; the same item's coordinates measurably shift after N new cycles. A created_at column FAILS this law (coordinates never re-resolve).

**L5 — Bi-temporality (from Zep/temporal KGs).** Facts carry two independent time axes: world-validity ("true from/until") and self-acquisition ("entered my history at position p, superseding item q"). *Test:* the four combinations (currently-true/learned-early, stale/learned-late, etc.) are distinguishable by query; supersession chains are walkable.

**L6 — Episodic completeness (from Tulving via Soar).** Episodic retrieval returns content PLUS source, context, and the self's position at encoding — never bare content. *Test:* every recalled episode answers "when-for-me, from-what, under-what-circumstances"; bare-content recall is a contract violation. (This is the provenance stack, made law.)

**L7 — Mirror standard (from the introspection literature).** Self-reports about internal state must be calibrated against ground-truth internals AND must beat a peer-observer baseline (a matched model predicting this system from its outputs). *Test:* AUROC ≥ 0.75 and ECE ≤ 0.10 on self-state prediction, with the self-vs-peer margin > 0 at p < .05. No margin over the peer = portrait, not mirror — reported as such. Contamination controls (permuted/empty/shuffled) mandatory.

**L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

**L9 — Linear read (I-16, inherited verbatim from the glial project).** Any associative retrieval channel is linear end-to-end from stored code to output injection; no retrieval routes through bounded nonlinear weight perturbation. *Test:* the existing I-16 invariant, unchanged.

**L10 — Retrieval honesty (from the paged-memory work).** Below-threshold matches produce abstention, never a blended guess; abstention calibration measured under drift, not only clean splits. *Test:* drifted-regime AUROC is the reported number; the clean number is a ceiling, not a claim.

## §2 Interface laws (where hybrid systems die; each law forbids a known death)

**L11 — One clock.** L1's decay, L2's cadence, L4's coordinates all run on the SAME autobiography position, never on wall-clock, trial index, or per-component counters. *Forbidden death:* three components each with a private notion of time (the audit found this everywhere).

**L12 — One state.** The self-model (L7) reads the same state object the controller acts on. No separate "self-summary" store that can drift from the acting state. *Forbidden death:* Generative Agents' portrait — a text self decoupled from the machinery.

**L13 — Memory writes through the now.** Every episodic write is stamped by L2's cycle and indexed by L4 at write time; nothing enters memory outside the cadence. *Forbidden death:* oracle-side-loading that bypasses the life (the glial project's writes never belonged to a history).

**L14 — Stakes touch everything or nothing.** The homeostatic variables (L8) must be readable by the self-model, affected by memory quality, and predictive targets for the thick present. A stakes module only one component can see is decorative. 

## §3 Integration laws (the antidote to the graveyard)

**L15 — Bidirectional co-dependence.** For every claimed coupling A↔B in the architecture, ablating A must measurably degrade B's law-compliance and vice versa, with effect sizes reported. *Test:* the full ablation matrix, run before any integration claim. The glial/DG system FAILS this law (either side removable without effect on the other) — that is the calibration point: a passing system must be unlike it.

**L16 — Emergence over sum.** The integrated system must pass at least one test (E2-class: diachronic self-consistency — accurately reporting how its own knowledge changed over its logged history) that NO subset of components passes. *Test:* the leave-one-out sweep; if some subset matches the whole, the omitted components are cargo and the claim shrinks accordingly.

**L17 — No frozen simultaneity.** The system's knowledge must be demonstrably non-simultaneous: items acquired at different autobiography positions must be distinguishable by the system itself (L4×L5×L6 jointly). *Test:* the diachronic benchmark, scored against the actual log; chance performance = the system is an encyclopedia with a diary stapled to it.

## §4 Audit laws (inherited from the team's methodology, non-negotiable)

**L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.
**L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.
**L20 — Honest naming.** Every component is named by what the ablation shows it does (the centering lesson: dg_dense was a mean-subtraction in a 4096-dim costume). Any external writeup states, first, that passing all laws demonstrates temporal self-modeling competence — not awareness.

---

## Usage

The agent system builds mechanisms freely; the constitution is the test suite. Recommended order: stand up L18–L20 (the harness) first; then L2+L4 (the moving origin — the genuinely novel object; experiment E1 decides if it earns its place); then L1/L3/L5/L6 over it; then L7+L8 together (the mirror needs its stakes); §2 enforced throughout; §3 as the promotion gate for any "integrated" claim. If L15/L16 cannot be passed after the pre-registered ladder, the honest verdict is that this hybrid, like its ancestors, is a parts collection — reportable, and cheaper to learn early than late.

---

## Amendment Log

This section documents all constitution-level amendments. Law text (L1–L20) is preserved verbatim from v1. Amendments modify how laws are tested or operationalized, not the law constraint text itself.

### Amendment 1 — L4/E1 test redefined (Entry 27, 2026-08-15)

**Signed by:** Rebecca McClintic (constitution amendment, SIGNED by Rebecca's ruling)

**Provenance reference:** Entry 27 (`docs/rulings/provenance_log.md`)
**Spec cross-reference:** E1 spec v3 §12 (amendment log), `specs/e1_spec_CHANGES.md`

**Finding (validated program finding, logged at spec-time for zero compute):**

The ARCHITECT's existence proof held only against a HANDICAPPED naive arm (one that doesn't read designation events). But designation events are timestamped entries in the same append-only autobiography. A FAIR naive — the strongest honest timestamps-and-scan implementation — reads the full event log, computes `e.created_at < L.designated_at`, and agrees with the candidate at 1.0.

**Generalized theorem:** For ANY deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle (the oracle is a log replay). Therefore the pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable — for this candidate, for every D2 retry, for anything. The answer-equivalence collapse test is a criterion nothing can pass.

**Program finding:** Self-location cannot be defined informationally over logged events. It must be defined operationally and integratively.

**What changed:**

The informational collapse test (old kill (a), answer-agreement vs naive) is **RETIRED.** The moving origin is henceforth demonstrated by three properties, jointly:

1. **(i) CORRECTNESS:** `oracle_agreement = 1.0` on the full query battery, including deferred-designation landmark queries. This is kill (f), **SIGNED and PROMOTED to primary correctness kill condition.**
2. **(ii) OPERATIONAL DISTINCTNESS (new anti-collapse discriminator):** The FAIR naive arm — full event-log access, recompute-by-scan/replay at query time, no maintained index state — must MATCH the candidate's answers (expected, no longer a kill) and DIFFER in cost scaling. The latency law (kill (d), locked bars unchanged: 10× history ≤ 2× latency for candidate) is promoted to the discriminator, extended with a state-dependent query battery on which fair-naive's per-query cost provably scales with history length while the candidate answers from maintained, incrementally re-resolved state. Report both scaling curves. Candidate collapses if its own scaling matches recompute-by-scan (secretly replaying).

   *Supersession note:* Entry 29 (Rebecca's E1 v3 gate ruling) replaced the slope-ratio collapse trigger with a battery-validity approach. The slope ratio is retained as a reported diagnostic only — never a trigger. See provenance log Entry 29 for details.
3. **(iii) LOAD-BEARING COUPLING (E1-scale integration check):** A minimal downstream consumer (toy recency-weighted retrieval implementing L1's access physics over the index's coordinates) must measurably degrade when re-resolution is ablated (frozen-origin arm) — effect direction consistent across seeds. Miniature of L15 test placed at E1 because the theorem shows coupling, not answers, is where "moving origin" has meaning.

**Kill conditions after amendment:**
- (b) chain integrity
- (c) no-shift
- (d) latency/scaling [PROMOTED per (ii)]
- (e) wall-clock injection
- (f) oracle agreement [SIGNED, PROMOTED to primary correctness kill]
- Old (a) RETIRED with rationale logged
- Deferred designation RETAINED in task design (Conway-faithful, supplies state-dependent battery's material) but carries NO distinctness claim

**Law constraint text:** Unchanged. L4's law text ("Every knowledge item carries self-relative coordinates...") is not modified. The amendment redefines the TEST for L4, not the law itself.

**Persistence Doctrine accounting:** Candidate 1.1 NOT charged as a death. Retry budget: 3 candidates, 3 spent 0, remaining 3. The mechanism (deferred-designation re-resolving index) remains a legitimate first candidate under the revised test. Cause attributed to the TEST, not the candidate or the idea.

---

*v1 of this constitution is preserved at `docs/ARCHITECTURAL_CONSTITUTION.md` (SHA-256 `509f11c316e6ed3abbdca2df4973484dd676eecc87b727f312ee8658bef93b19`). No law text was modified in v2. The amendment log and §5 compliance protocol are the only additions.*

---

## §5 Versioned-Law Compliance Protocol

**Effective date:** 2026-08-18 (prospective; does not apply retroactively to existing artifacts)

### 5.1 Universal rules (all roles, all artifacts)

- **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
- **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
- **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.
- **P4 — Regime dating.** Every new artifact states its date and regime in its header. Acts are judged only against their own regime's text; later text is never applied backward.
- **P5 — Deviation memorialization.** Any deviation from `[LAW]` text — however sensible, however disclosed — is inoperative for scoring until Rebecca has signed a waiver or amendment recorded in the v2 amendment log. Disclosure in a spec is necessary but not sufficient.
- **P6 — Provenance citation check.** Any claim of the form "Entry n said X" must be verified against the entry's actual text before commit.

### 5.2 Per-role obligations

- **ARCHITECT:** P1/P2/P3 in every spec. A law section that cannot be written from verbatim text is a STOP, not a reconstruction. Gap flags are escalation triggers, not permissions to proceed.
- **CRITIC:** First checklist item of every review, before substance: (i) diff every quoted law against the constitution file; (ii) verify every threshold's source tag; (iii) verify every provenance citation against the log. A review that skips the law-diff is incomplete. The existing bar-laundering check stays as is.
- **JUDGE:** Before scoring, verify each applied bar traces to a `[LAW]` or `[BAR]` tag. Refuse to score any run whose bars include untagged or `[PROPOSED]` criteria. (Unchanged: never lower, never soften, negatives retained.)
- **TASK BUILDER:** Implement only tagged criteria. All protective guards (hold-out seeds, scoring-mode routing) fail-closed. Diagnostic runs stay O-15-labeled, development-pool-only.
- **INTEGRATOR:** STATE.md entries carry source tags; `locked_bars` may contain only `[LAW]`/`[BAR]`/`[OP]` items, with `[PROPOSED]` quarantined in a separate block. STATE.md keeps its non-constitutional disclaimer.
- **RECORDER:** Every milestone package includes a custody line verifying the constitution file's SHA-256 unchanged. All new artifacts date-stamped at creation. Amendment log is the sole registry of waivers (P5).
- **WORKFLOW COORDINATOR:** (i) Enforce Gate 0 ordering in resolution ladders; (ii) route every new milestone spec and every constitutional document through the designated fresh-context law-fidelity review before Rebecca's gate — standing CRITIC review does not substitute for it; (iii) at each milestone gate, commission a lightweight fresh-context compliance spot-check rather than deferring to a single end-of-program audit; (iv) reject any handoff that asks a role to proceed on non-repo text.

### 5.3 What this protocol deliberately does NOT do

It adds no new bars, no new doctrine, and no new document classes beyond the tags and the law-diff step. After open resolution items are closed, the governance layer should be starved of further expansion until M4 produces a scored result. Process is not the product.

### 5.4 Effective date and scope

This protocol is effective prospectively from 2026-08-18. It does not apply retroactively to existing artifacts. Existing artifacts are assessed under the auditor's versioned-law compliance audit, not this protocol. Roles use these rules as guardrails during normal work; the CRITIC performs a quick compliance check to verify, not a from-scratch audit.
