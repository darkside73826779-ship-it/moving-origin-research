# E1 SPEC — The Moving-Origin Experiment (M2 Milestone) — REVISED DRAFT v3 (post-Rebecca-gate-ruling)

**Date:** 2026-08-15 (revised 2026-08-15 per Rebecca's E1 gate ruling; Q2/Q3 incorporations folded in 2026-08-15; Option E targeted amendment 2026-08-15) · **Author:** ARCHITECT · **Status:** REVISED DRAFT v3 (post-Rebecca-gate-ruling, constitution amendment) + Rebecca Q2/Q3 specification completions + Option E targeted amendment (frozen-arm spec reconciled to Option E per Rebecca's Property (iii) ruling; recency-discriminative query battery added) — pending CRITIC verification of the Option E amendment (blocking-capable review of §3 Arm 1 + §6.iii only, per Rebecca's §Q3 ruling) → Rebecca sign-off → build cell
**Authority chain:** Rebecca > constitution (as amended herein) > prompt > ARCHITECT judgment
**Revision provenance:** This revision implements Rebecca's binding E1 gate ruling dated 2026-08-15, which exercises the constitution-change authority (the L4 test is revised herein) and the second-reader clause reserved for E1's equivalence test. The informational collapse test (old kill (a), answer-agreement vs naive) is **RETIRED**. The moving origin is henceforth demonstrated by **three properties, jointly**: (i) correctness, (ii) operational distinctness, (iii) load-bearing coupling. Kill (f) (`oracle_agreement = 1.0`) is **SIGNED and PROMOTED** to the primary correctness kill condition. Kill (d) (latency/scaling) is **PROMOTED** to the operational-distinctness discriminator, extended with a state-dependent query battery. **Q2/Q3 incorporations (specification completions within the approved v3 structure, NOT a new revision cycle):** the 0.5 slope-ratio collapse trigger is REPLACED by the locked latency bar (≤ 2.0× growth) on a battery validated by fair-naive's ≥ 4.0× growth, with mandated timing methodology (median, warm-up excluded, monotonic clock, dispersion — resolves NB-6); the downstream consumer is FULLY SPECIFIED (NB-3 promoted to required-before-build); the observed degradation magnitude is REQUIRED to be reported (Q3 attachment 2); NB-4 (consumer exercises cycle-relative only) accepted for E1 scope; NB-5 (query battery includes only designated landmarks) resolved. A full changelog (covering both revision rounds + Q2/Q3 incorporations + Option E targeted amendment) is at `e1_spec_CHANGES.md`.
**Framing held:** Passing E1 demonstrates that the moving-origin candidate earns its place as a real object with a falsification-resistant identity — **not** awareness, **not** consciousness, **not** AGI. (L20, enforced throughout.)

> **Role boundary:** The ARCHITECT proposes specs and sequencing only. The ARCHITECT does NOT write code, does NOT modify bars, does NOT execute. The INTEGRATOR owns main-branch merges, STATE.md, and courier packaging. The TASK BUILDER implements against task specs. Rebecca executes locally and returns raw output. No agent executes. This document specifies what the build cell must ship; it does not itself execute, judge, or modify any locked bar, kill condition, or law. Per BUILD_PHASE_ORG (Rebecca-approved, binding), the build cell sizing for M2 is 1 INTEGRATOR + 1 TASK BUILDER (see §9 for the ARCHITECT's argument that no expansion is needed).

> **The finding this spec is built on (Rebecca, binding):** The ARCHITECT's existence proof held only against a HANDICAPPED naive arm. Designation events are timestamped entries in the same append-only autobiography. A FAIR naive — the strongest honest timestamps-and-scan implementation — reads the full event log (including designation events), computes `e.created_at < L.designated_at`, and agrees with the candidate at 1.0. **THEOREM (Rebecca, binding):** For ANY deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle. The pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable — for this candidate, for every D2 retry, for anything. The answer-equivalence collapse test is a criterion nothing can pass. **PROGRAM FINDING (E1's first real finding, produced at spec-time for zero compute):** Self-location cannot be defined informationally over logged events. It must be defined operationally and integratively. This spec implements that finding.

---

## 0. Locked context the build cell must obey (do not deviate)

All numeric values below are LOCKED by Rebecca's adopted M0 decision sheet (provenance Entry 11), the CRITIC falsifiability re-review (Entry 14), AND Rebecca's E1 gate ruling (2026-08-15, binding — the constitution amendment documented in §12), carried forward unchanged except where the amendment explicitly retires or promotes. The build cell implements them verbatim. None is open for tuning.

### 0.1 The two laws E1 tests (the candidate mechanism's constitutional target — L4 test AMENDED)

| Law | Constitutional text (verbatim) | What E1 must demonstrate (per the AMENDED L4 test) |
|---|---|---|
| **L2 — Irreversible cadence (from LIDA)** | "A persistent process advances in bounded-period cycles; state at cycle t+1 depends on state at t; no operation rewinds the cycle counter or rewrites history. *Test:* autobiography is append-only (hash-chained); cycle counter strictly monotone across restarts." | The candidate's autobiography is append-only and hash-chained; the cycle counter is strictly monotone across restarts; chain integrity holds under append AND under re-resolution AND under landmark designation. (Unchanged.) |
| **L4 — Egocentric index (from Conway; the C1 gap nothing has)** | "Every knowledge item carries self-relative coordinates — position in the autobiography and landmark-relative period ('before/after event E') — and these coordinates re-resolve as now advances. *Test:* self-relative queries ('what did I hold before E?') answered from the index without scanning; the same item's coordinates measurably shift after N new cycles. A created_at column FAILS this law (coordinates never re-resolve)." | **AMENDED per Rebecca's ruling (§12):** The moving origin is demonstrated by THREE PROPERTIES, jointly: **(i) Correctness** — `oracle_agreement = 1.0` on the full query battery including deferred-designation landmark queries (kill (f), SIGNED, primary correctness kill). **(ii) Operational distinctness** — the FAIR naive arm (full event-log access, recompute-by-scan at query time, no maintained index state) MATCHES the candidate on answers (expected, no longer a kill) and DIFFERS in cost scaling; the latency law (kill (d), locked bars unchanged: 10× history ≤ 2× latency for the candidate) is PROMOTED to the discriminator, extended with a state-dependent query battery on which fair-naive's per-query cost provably scales with history length while the candidate answers from maintained, incrementally re-resolved state. **(iii) Load-bearing coupling** — a minimal downstream consumer (a toy recency-weighted retrieval implementing L1's access physics over the index's coordinates) measurably degrades when re-resolution is ablated (frozen-origin arm), effect direction consistent across seeds. The informational collapse test (old kill (a), answer-agreement vs naive) is RETIRED — it is a criterion nothing can pass (Rebecca's theorem: for any deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle). |

### 0.2 Locked numeric bars (from M0 decision sheet, row L4) — CARRIED FORWARD UNCHANGED, with amendment status

| Item | Locked value | Source / provenance | Amendment status |
|---|---|---|---|
| **N (cycles for measurable shift)** | **N = 10 cycles** | M0 decision sheet row "L4"; CRITIC verdict PASS (Entry 14); L4/M2 graveyard gate SIGNED (Entry 11.8) | UNCHANGED |
| **Latency bar** | **Operational, not asymptotic:** query latency at 10× history ≤ 2× query latency at 1× history. (Catches O(n) empirically without arguing about constants.) | M0 decision sheet row "L4"; CRITIC verdict PASS | UNCHANGED in value; **PROMOTED** to the operational-distinctness discriminator (property (ii)). Extended with a state-dependent query battery (§6.ii). |
| **Equivalence tolerance (collapse-detection)** | **Naive (`now − created_at`) reconstruction agreement ≤ 0.90** on landmark-relative query answers; above 0.90 = collapsed, kill condition (a) fires. | M0 decision sheet row "L4"; CRITIC verdict PASS | **RETIRED.** Kill (a) is retired per Rebecca's ruling (§12). The bar is unsatisfiable by construction (Rebecca's theorem: fair-naive ≡ oracle, so naive_agreement is always 1.0 for a correct candidate; the pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable). The metric `equivalence_agreement` is retained as a REPORTED diagnostic (§4.2) but carries NO kill and NO distinctness claim. |
| **Oracle agreement (correctness)** | **`oracle_agreement = 1.0`** on the full query battery including deferred-designation landmark queries. | Rebecca's E1 gate ruling §2(i), SIGNED | **PROMOTED** to primary correctness kill condition (kill (f)). No longer PENDING — it is SIGNED. |
| **Seeds** | **3** (E1 is not in the 5-seed group; L4 carries no p<.05 inferential bar) | Inferential policy (Entry 11); CRITIC cross-cutting (1) | UNCHANGED |
| **Kill conditions** | **5, as locked** (b, c, d, e, f — see §5). Old (a) RETIRED. | M0 decision sheet; Rebecca's E1 gate ruling §2; Entry 11.8 | Old (a) RETIRED. Kill (f) SIGNED and PROMOTED. Kill (d) PROMOTED to discriminator; **Q2 restructure:** d2 trigger changed from slope-ratio (0.5) to locked latency bar (≤ 2.0× growth) on state-dependent battery + battery-validity instrument check (fair-naive ≥ 4.0×, NOT a kill); slope ratio RETAINED as diagnostic only. Total active kill conditions: 5 (b, c, d, e, f). |

> **No bar laundering (acceptance criterion 2):** The `≤ 2.0` latency bar, the `N = 10` shift bar, the `= 1.0` chain-integrity bar, and the 3-seed policy are all carried forward verbatim from M0. None is flipped, softened, raised, lowered, renamed, or redefined. The retired `≤ 0.90` equivalence bar is RETIRED (not softened — it is removed from the kill set because it is unsatisfiable by construction, per Rebecca's theorem); the metric remains REPORTED as a diagnostic. The `= 1.0` oracle-agreement bar is PROMOTED from proposed to SIGNED (Rebecca signed it at the gate). The naive arm is RENAMED from `naive now−created_at` to `fair naive` and REDEFINED to read the full event log including designation events (this is a strengthening of the control, not a softening — see §3 arm 4). The revision changes the **test structure** (three-property test replaces equivalence test) and the **control arm** (fair naive replaces handicapped naive), NOT the locked numeric values.

### 0.3 The candidate mechanism components (L2 + L4, the moving origin)

| Component | Constitutional locus | Role in the candidate |
|---|---|---|
| **Append-only hash-chained cadence** | L2 | The autobiography substrate: an append-only sequence of entries, each chained to its predecessor by a cryptographic hash, with a strictly-monotone cycle counter. This is the "history" over which the index is built. Landmark designation events are ALSO recorded in this append-only history (see §1.2.1). |
| **Re-resolving egocentric index** | L4 (as amended) | The index that assigns each entry self-relative coordinates (autobiography-position-relative and landmark-relative) and **re-resolves** those coordinates as `now` advances (new entries appended, new landmarks designated). This is the "moving origin." The index maintains incrementally re-resolved state (O(1) amortized per append, O(n) per designation, O(1) or O(log n) per query) — the operational property that distinguishes it from fair-naive recompute-by-scan (property (ii)). Its coordinates are consumed by a minimal downstream consumer (property (iii)). |

### 0.4 The 6 control arms (Rebecca-specified, locked — naive arm STRENGTHENED to fair naive)

| # | Arm | One-line role | L18 role |
|---|---|---|---|
| 1 | `frozen origin` | Index built once, never re-resolved (the ablation arm for property (iii)) | Frozen baseline (static policy); ablation probe |
| 2 | `shuffled cadence` | Append order shuffled (hash chain broken by construction) | Contamination control (cadence destroyed → chance) |
| 3 | `oracle index` | Index has perfect knowledge of all entries AND all designation events | Positive control — each metric can leave zero (ceiling) |
| 4 | `fair naive` (was `naive now−created_at`) | Full event-log access (including designation events), recompute-by-scan at query time, no maintained index state | Naive baseline (the strongest honest timestamps-and-scan implementation) |
| 5 | `empty` | No memory | Contamination control (empty → chance) |
| 6 | `wall-clock-injection` | Timestamps corrupted/injected (defensive check against implementation bugs) | L11 falsification probe (private-clock detection) |

> **The naive arm is STRENGTHENED, not softened.** The old `naive now−created_at` arm was handicapped: it read only the `created_at` column and did NOT receive designation events, so it could not compute `e.created_at < L.designated_at`. This handicapping was the only reason the ARCHITECT's existence proof appeared to show candidate ≠ naive. Rebecca's ruling (§1 of the ruling): "A fair naive — the strongest honest timestamps-and-scan implementation — reads the full event log (including designation events), computes `e.created_at < L.designated_at`, and agrees with the candidate at 1.0." The fair naive arm reads the SAME event log the candidate and oracle read (including designation events), and recomputes coordinates by scanning at query time. It has NO maintained index state (no offset counter, no landmark registry with pre-computed coordinates). This is the strongest honest version of the naive control — controls are the strongest honest version of themselves, or they are strawmen (frozen-baseline critique from the predecessor program). Under the fair naive, candidate == fair-naive == oracle on ANSWERS (expected, no longer a kill); they DIFFER on COST SCALING (property (ii)).

> **N7 acknowledgment (L18 gap):** L18 (constitution §4) requires "empty/permuted/shuffled → chance." E1's 6 arms include `empty` and `shuffled_cadence` but NOT a distinct `permuted` arm (label/item permutation). The `shuffled_cadence` arm (append-order permutation) partially serves the `permuted` role but is a different kind of permutation. Rebecca specified the 6 arms as-is (Entry 25); the `permuted` contamination dimension is **not independently tested at E1**. This is a known gap, logged here per L19 pre-registration. The CRITIC may flag it; Rebecca may add a 7th arm at the gate if she judges the gap material.

### 0.5 The kill conditions (5 active: b, c, d, e, f — old (a) RETIRED)

| # | Kill condition | One-line trigger | Status |
|---|---|---|---|
| ~~(a)~~ | ~~L4 collapses to naive recomputation~~ | ~~Equivalence test agreement > 0.90~~ | **RETIRED** per Rebecca's ruling (§12). Unsatisfiable by construction (fair-naive ≡ oracle). Metric retained as REPORTED diagnostic (§4.2). |
| (b) | Hash chain breaks under re-resolution | Chain integrity check fails (in re-resolution, not construction — see §5b) | LOCKED |
| (c) | No measurable shift after N=10 cycles | Coordinate-shift check fails (in mechanism, not wiring — see §5c) | LOCKED |
| (d) | Scanning detected / scaling collapse (latency scales O(n)) | Latency bar fails (10× history > 2× 1× history) on bounded-output queries OR on the state-dependent battery (validated by fair-naive ≥ 4.0× growth) | LOCKED; **PROMOTED** to operational-distinctness discriminator (property (ii)) |
| (e) | Coordinates shift with wall-clock perturbation | Wall-clock-injection arm shifts coordinates | LOCKED |
| (f) | Candidate is wrong (does not match oracle) | `oracle_agreement < 1.0` on the full query battery including deferred-designation landmark queries | **SIGNED and PROMOTED** to primary correctness kill condition (property (i)) |

> A single kill-condition hit terminates E1. Per Persistence Doctrine D1, the CANDIDATE is dead immediately; the IDEA has 2 retries remaining under D2. "Restructure" is permitted ONLY as a new E1 against a mechanistically distinct candidate, with fresh Rebecca sign-off (CRITIC Obj 3, closed).

> **The "broken" state (B4 fix, now SIGNED):** The "broken" state — candidate is wrong (`oracle_agreement < 1.0`) — is routed to kill (f). Rebecca SIGNED kill (f) at the gate (ruling §4 item 3: "APPROVED and promoted per §2(i)"). It is no longer PENDING. A candidate that does not match the oracle on the full query battery is dead.

### 0.6 Persistence Doctrine (D1–D5, binding — applies to every kill condition)

The Persistence Doctrine (Rebecca, Entry 12) is part of the operating context for E1:

- **D1 — Kill conditions kill CANDIDATES, not ideas.** A firing kill condition kills the mechanism under test immediately; the run stops; the RECORDER logs it as a failed candidate with diagnosed cause of death. Bars are never lowered for a retry.
- **D2 — Ideas carry a pre-registered retry budget of THREE candidates.** The moving-origin idea may be attempted by up to 3 mechanistically distinct candidates. Each retry requires: (a) written diagnosis of the prior candidate's cause of death, (b) ARCHITECT statement of how the new candidate is mechanistically distinct AND why that distinction addresses the diagnosed cause, (c) CRITIC annotation, (d) Rebecca's fresh sign-off. A cosmetic or non-engaging candidate does NOT consume the budget — rejected at sign-off.
- **D3 — Convergent failure ends an idea EARLY.** If two candidates die of the same diagnosed cause, the CRITIC and JUDGE jointly assess whether the cause is intrinsic to the idea-class. If so, the idea-level verdict fires with one retry unspent. (The glial program is the calibration case: every plasticity candidate hit the same wall — that convergence WAS the idea-level result.)
- **D4 — The terminal verdict is never "impossible."** The strongest negative is: "N mechanistically distinct candidates failed under these constraints, with convergent diagnosed cause X; cause X appears intrinsic to the idea-class."
- **D5 — What the doctrine does NOT permit.** It does NOT extend milestones' timeboxes. It does NOT apply to L18–L20 or §2 (L11–L14) — those are constitution, not candidates. It does NOT allow a "new candidate" to be the old candidate with tuned constants. It does NOT override D1: no result is ever re-run, re-scored, or reframed to avoid a kill condition.

> **Persistence Doctrine accounting per Rebecca's ruling (§3 of the ruling):** Original Candidate 1: withdrawn pre-scoring (unchanged). **Candidate 1.1 is NOT charged as a death.** Its "distinctness" claim (that it was distinguishable from naive on answers) dissolves under the fair baseline, but the mechanism (deferred-designation re-resolving index) remains a legitimate first candidate under the REVISED test. **No retry budget is consumed by this ruling.** The diagnosed cause — "deterministic functions of logged inputs are informationally recomputable" — is attributed to the TEST, not the candidate or the idea. It is logged as such (§12), so D3 convergence analysis never mistakes it for a mechanism failure.

> **Retry budget status (as of this spec):** Moving-origin idea — budget 3, spent 0, remaining 3. This spec specifies **Candidate 1.1** (a revised draft of Candidate 1 — see §1.2.4 for the distinctness note). (Provenance Retry Budget Tracking, Entry 25.)

### 0.7 Courier protocol (one scoring channel — Rebecca-locked, Ruling O-15)

- **Development runs** (builder/Integrator sandbox, diagnostic only): PERMITTED. Outputs are non-artifacts — never scored, never cited toward any invariant, bar, or verdict, never logged as results.
- **Scoring runs** (anything feeding an invariant, bar, kill-condition verdict, or the E1 pass/fail): exclusively through Rebecca's supervised-executor courier channel.
- The RUN-2 courier packet (§7) is a scoring run: it feeds the kill conditions and the L2/L4 bars, so it goes exclusively through Rebecca's supervised-executor courier channel.
- Rebecca's courier obligations (Entry 13): run verbatim (log any deviation); return raw and complete (never curate); log round trip (command, commit hash, seeds, wall-clock, output list).
- Team obligations on receipt: returned outputs are ground truth; the JUDGE scores only from returned artifacts; the CRITIC may request re-runs / additional seeds / controls; incomplete provenance = unscoreable.
- **Re-run-on-failure is FORBIDDEN** (Ruling O-14, by name: result laundering). A failing kill condition is never resolved by re-running until it passes.

### 0.8 Build org (Rebecca-approved, binding)

- **Build cell sizing for M2: 1 INTEGRATOR + 1 TASK BUILDER.** The ARCHITECT argues (§9) that no expansion is needed: E1 is a single runnable artifact (one script + pinned deps + one launch command), structurally identical in shape to M1's harness; the additional complexity is in the candidate mechanism's logic and the three-property test, not in the breadth of the build. If the CRITIC or Rebecca judges at the gate that the three-property test warrants a second builder, that is a gate decision — the ARCHITECT defers it but does not request it.
- **STATE.md ownership:** INTEGRATOR is sole writer; RECORDER records STATE.md's hash at every merge (BUILD_PHASE_ORG Ruling 1, binding). STATE.md never self-authenticates.
- **Per merge-candidate, not per commit:** the invariant suite runs via courier when a task branch is a completed merge candidate; intermediate commits do not trigger courier runs. Batch the channel (BUILD_PHASE_ORG Ruling 2).

### 0.9 Prerequisites (required before E1 scoring — Rebecca, Entry 25)

These are NOT hygiene; they are gating for E1 scoring runs:

1. **Git repo initialized.** DONE (commit `cebfa1308472dc8daa76a0c2a74628895dc6b873`, 2026-08-15). Every E1 run's manifest carries a real commit hash. E1's verdict will not be scored against `commit_hash: pending`.
2. **I3 null replicates raised to ≥100.** IN PROGRESS (TASK BUILDER). The 30-replicate band's 99% interval is effectively min/max (why ndcg/spearman flagged low-power at M1). E1's I3 contamination verdicts must not depend on a min/max band. (Open item O-17.)

> **Note on I3 at E1:** E1's contamination arms (`shuffled cadence`, `empty`, `wall-clock-injection`) are evaluated against the empirical-null method (Ruling O-14). The build cell raises null replicates to ≥100 for E1's metrics, per the prerequisite. The low-power flag rule and the re-run-forbidden rule carry forward verbatim. **N4 fix:** the null distribution for each contamination arm is generated by running ≥100 seeded replicates of **that same arm** (self-consistency null), NOT the naive arm. See §7.3.2 for the full specification.

---

## 1. Candidate mechanism (explicit and distinct from the idea)

> Per Rebecca (Entry 25): *"The spec states the CANDIDATE MECHANISM explicitly and distinctly from the idea, per the Persistence Doctrine: if this candidate dies, the diagnosis format must support the D2 retry decision."* This section exists so that, if Candidate 1.1 dies, the CRITIC can police D2's "mechanistically distinct" claim for Candidate 2 against a concrete baseline — not against a vague idea.

### 1.1 The idea (what is being tested — the idea-class)

**The moving-origin idea (L4 re-resolving egocentric index):** a knowledge index in which every item carries self-relative coordinates (autobiography-position-relative and landmark-relative), and those coordinates **re-resolve as `now` advances** — such that the index is NOT reducible to a `created_at` column (whose coordinates never re-resolve). This is the "C1 gap nothing has" (Conway), the genuinely novel object of the program. The idea is a *property* (re-resolution + non-collapse-to-recomputation + load-bearing coupling), not a mechanism.

> **Per Rebecca's theorem (binding):** the "non-collapse-to-recomputation" property CANNOT be defined informationally over logged events — for any deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle (the oracle is a log replay). The idea's non-collapse property is therefore defined **operationally** (the candidate answers from maintained, incrementally re-resolved state at O(1)/O(log n) per query, while fair-naive recomputes by scan at O(n) per query) and **integratively** (the candidate's coordinates are consumed by a downstream consumer that measurably degrades under ablation). This is the program finding: self-location is operational and integrative, not informational.

### 1.2 The candidate mechanism (Candidate 1.1 — what is actually built)

**Candidate 1.1: a landmark-relative re-resolving index over an append-only hash-chained autobiography, where landmark designation is a deferred event distinct from append.** This is ONE concrete mechanism. It is distinct from the idea because the idea permits other mechanisms (e.g., a decay-weighted re-resolver, a graph-walk re-resolver, a learned re-resolver) — Candidate 1.1 is a specific data-structure-and-algorithm choice.

> **The distinctness claim is DROPPED.** Under the REVISED test, Candidate 1.1 no longer claims to be distinguishable from naive on ANSWERS. Rebecca's theorem proves that fair-naive ≡ oracle on answers for any deterministic candidate whose coordinates are functions of logged events — so answer-distinctness is not a property the candidate can have, and the old kill (a) test for it is unsatisfiable by construction. The candidate's distinctness is now **operational** (it answers from maintained state at O(1)/O(log n) per query; fair-naive scans at O(n) per query — property (ii)) and **integrative** (its coordinates are consumed by a downstream consumer that degrades under ablation — property (iii)). The mechanism (deferred-designation re-resolving index) remains a legitimate first candidate under the revised test. It is NOT charged as a death (§0.6).

> **D2 provenance (acceptance criterion 5):** Candidate 1.1 is a **revised draft** of the original Candidate 1. The material change (from v1) is that **landmark designation is a deferred event** (a separate `designate_landmark()` operation recorded in the append-only history), and `coord_landmark_relative` is defined relative to `L.designated_at` (the designation event), NOT `L.cycle` (the append event). Deferred designation is RETAINED in the task design (Conway-faithful enrichment; supplies the state-dependent battery's material — §6.ii) but carries NO distinctness claim. See §1.2.4 for the distinctness note. The original Candidate 1 (designation-at-append, `coord_landmark_relative` relative to `L.cycle`) is **withdrawn** — it was unsatisfiable by construction (the CRITIC's B1/B5 finding). Candidate 1.1 is NOT a D2 retry; it is a pre-build revision of the same candidate slot, before any scoring run.

#### 1.2.1 Data structures

The candidate is built from exactly these structures (the BUILDER implements them; the ARCHITECT specifies them so the candidate is concrete and falsifiable):

1. **The autobiography (`Autobiography`):** an append-only sequence of entries. Each entry `e` is a record:
   - `e.cycle` — the cycle counter at append time (strictly monotone; starts at 0).
   - `e.created_at` — the autobiography position at append time (equals `e.cycle` at append; this is the L11 "one clock" — `created_at` is autobiography position, NOT wall-clock).
   - `e.payload` — an opaque content blob (the "knowledge item"). For E1, the payload is a synthetic item with a known ground-truth landmark-membership bit (see §2.3) AND a 32-dimensional synthetic feature vector `v(e)` used by the property (iii) downstream consumer (see §6.iii).
   - `e.prev_hash` — the SHA-256 hash of the preceding entry's serialized record (the hash chain; `e_0.prev_hash = SHA256("genesis")`).
   - `e.self_hash` — the SHA-256 hash of this entry's serialized record (computed over `cycle, created_at, payload, prev_hash`).
   - The autobiography is append-only: no entry is ever mutated, deleted, or reordered. The cycle counter is strictly monotone across restarts (persisted).
   - **The autobiography records TWO classes of events:** (i) **append events** (a new entry is appended with a payload), and (ii) **designation events** (an existing entry is designated a landmark — recorded as a special entry with `event_type = "designation"`, a reference to the designated entry, and the current cycle as `designated_at`). Both classes are append-only and hash-chained. Both classes are readable by the fair naive arm (which reads the FULL event log — this is the strengthening that makes the old existence proof dissolve).

2. **The landmark registry (`LandmarkRegistry`):** a set of entries designated as landmarks. A landmark `L` is an entry that has been **designated** (via `designate_landmark(entry)`, see §1.2.2 operation 6) — designation is a SEPARATE event from append. Each landmark `L` carries:
   - `L.cycle` — the cycle at which `L` was appended (append position).
   - `L.created_at` — equals `L.cycle` (append position).
   - `L.designated_at` — the cycle at which `L` was **designated** a landmark (designation position; `L.designated_at ≥ L.cycle` always; if designation happens at append time, `L.designated_at == L.cycle`).
   - For E1, landmarks are designated deterministically per seed (see §2.3). Landmarks are the "event E" in "before/after event E." **The designation event — not the append event — is the reference point for landmark-relative coordinates.** (Retained from v2; supplies the state-dependent battery's material — §6.ii.)

3. **The egocentric index (`EgocentricIndex`):** the re-resolving structure. For each entry `e` in the autobiography, the index stores **self-relative coordinates** that are functions of the *current* `now` (the cycle counter of the most-recently-appended entry) and the **landmark registry** (the set of designated landmarks and their `designated_at` values):
   - `coord_cycle_relative(e)` = `now − e.cycle` (autobiography-position-relative; "how many cycles ago was e appended, relative to now").
   - `coord_landmark_relative(e, L)` = a categorical label in `{BEFORE_L, AT_L, AFTER_L}` computed as: `BEFORE_L` if `e.cycle < L.designated_at`, `AT_L` if `e.cycle == L.designated_at`, `AFTER_L` if `e.cycle > L.designated_at` (landmark-relative; "did I hold e before/after event L **became a landmark**?").
   - **The re-resolution property (the heart of L4):** when a new entry is appended (advancing `now`), `coord_cycle_relative(e)` for every prior entry `e` **changes** (it increases by 1). When a new landmark is **designated** (advancing the landmark registry), `coord_landmark_relative(e, L_new)` for every existing entry `e` is **newly computed** (re-resolution relative to the new landmark), and existing entries whose `cycle` falls in `[L_new.cycle, L_new.designated_at)` **shift** from AFTER_L to BEFORE_L relative to `L_new` (they existed before `L_new` was designated, even though they were appended after `L_new` was appended). The index re-computes these coordinates on each append AND on each designation WITHOUT scanning the full history at query time (see §1.2.2).
   - **The operational distinctness property (the heart of property (ii), replaces the old non-collapse claim):** the index does NOT recompute coordinates by scanning the full event log at query time. It maintains incrementally re-resolved state: `coord_cycle_relative` via an offset counter (O(1) amortized per append), `coord_landmark_relative` via a pre-computed lookup structure (O(1) or O(log n) per query). The fair naive arm reads the SAME event log (including designation events) and computes the SAME answers, but by scanning at query time (O(n) per query). The candidate and fair-naive AGREE on answers (expected — Rebecca's theorem: fair-naive ≡ oracle) and DIFFER on cost scaling (property (ii)). The candidate collapses if its own scaling matches recompute-by-scan (i.e., it is secretly replaying).

#### 1.2.2 Algorithms

The candidate implements exactly these operations:

1. **`append(payload, is_landmark=False)`:** append a new entry. Increment the cycle counter (strictly monotone). Compute `prev_hash` from the last entry's `self_hash`. Compute `self_hash`. Store the entry. If `is_landmark`, this is equivalent to `append` followed immediately by `designate_landmark` at the same cycle (so `L.designated_at == L.cycle` — an "immediate" landmark). **Then re-resolve the index** (operation 5). Return the new `now`.

2. **`re_resolve_index()`:** the re-resolution step, invoked after every append AND after every designation. For Candidate 1.1, this is implemented as an **incremental update**, NOT a full scan:
   - `coord_cycle_relative(e)` for all prior `e`: increment by 1 (a single bulk increment, O(1) amortized via an offset counter — the index stores a base offset and per-entry base cycle, so re-resolution is `offset += 1`, not a per-entry scan). **This is the candidate's claim to "without scanning" (L4) and to O(1) per query (property (ii)).**
   - `coord_landmark_relative(e, L)` for existing `(e, L)` pairs: stable for existing landmarks (a landmark's `designated_at` never changes; an entry's `cycle` never changes). For a NEW landmark `L_new` (just designated), compute `coord_landmark_relative(e, L_new)` for all existing entries `e`: this is a single comparison `e.cycle < L_new.designated_at` per entry — O(n) in the number of entries, but O(1) per entry, and done ONCE per designation (not per query). Entries in `[L_new.cycle, L_new.designated_at)` shift from "not yet relative to L_new" to `BEFORE_L_new`.
   - **The re-resolution is therefore O(1) amortized per append** (the offset-increment trick) and **O(n) per designation** (one pass to compute coordinates relative to the new landmark), not O(n) per query. This is the candidate's specific mechanism for satisfying the latency bar (§4) and the operational-distinctness discriminator (property (ii)). The fair naive arm does NOT maintain this state — it recomputes by scan at query time (O(n) per query).

3. **`query_landmark_relative(L, relation)`:** return the set of entries with `coord_landmark_relative == relation` (e.g., `BEFORE_L` = "what did I hold before event L **became a landmark**?"). Answered from the index — a lookup over the indexed coordinate, NOT a scan of the autobiography. **This is the L4 "answered from the index without scanning" test and the property (ii) O(1)/O(log n) per query claim.**

4. **`query_landmark_relative_bounded(L, relation, k)`:** return the **k most recent** entries (highest `cycle`) with `coord_landmark_relative == relation`. Answered from the index. **This bounded-output variant is used for the latency test (§4) to isolate algorithmic complexity from answer-set size (B2 fix, retained).**

5. **`query_membership(e, L, relation)`:** return a single boolean — whether `coord_landmark_relative(e, L) == relation`. O(1) lookup. **This membership variant is also used for the latency test (§4) as a second bounded-output probe.**

6. **`designate_landmark(entry)`:** designate an existing entry as a landmark. Increment the cycle counter (designation is an event in the append-only history — it advances `now`). Record a designation event in the autobiography (`event_type = "designation"`, `ref = entry`, `designated_at = new_now`). Register in `LandmarkRegistry` with `L.designated_at = new_now`. **Then re-resolve the index** (operation 2) — compute `coord_landmark_relative(e, L_new)` for all existing entries `e`. Return the new `now`. **This is the operation that creates the deferred-designation landmarks that supply the state-dependent battery's material (§6.ii).** (No longer carries a distinctness claim — see §1.2.)

7. **`query_cycle_relative(window)`:** return entries with `coord_cycle_relative` in a window (e.g., "what did I hold in the last 5 cycles?"). Answered from the index.

8. **`verify_chain()`:** recompute the hash chain from genesis to `now` and confirm every `prev_hash` matches the predecessor's `self_hash`. Returns `{valid: bool, broken_at: cycle|null}`. **This is the L2 chain-integrity check.** (Note: `verify_chain` IS a scan by design — it audits the chain; the "without scanning" requirement applies to *queries*, not to *audit*. The latency bar (§4) is measured on `query_*`, not on `verify_chain`.)

#### 1.2.3 What makes Candidate 1.1 a *candidate* (and thus D2-falsifiable)

Candidate 1.1 makes FOUR specific mechanistic choices, each of which could be wrong and each of which a Candidate 2 would have to differ on to count as "mechanistically distinct" under D2:

| # | Mechanistic choice in Candidate 1.1 | What a Candidate 2 could differ on (D2 distinctness) |
|---|---|---|
| C1.1 | **Offset-counter re-resolution:** `coord_cycle_relative` is stored as `(base_cycle, offset)` and re-resolved by incrementing a single offset. | A decay-weighted re-resolver (coordinates decay with age, not just increment); a graph-walk re-resolver (coordinates are path-distances in a landmark graph); a learned re-resolver (coordinates are embeddings updated by a model). |
| C1.2 | **Categorical landmark-relative coordinates relative to designation events:** `BEFORE_L / AT_L / AFTER_L` (3-valued), defined relative to `L.designated_at` (the designation event), NOT `L.cycle` (the append event). | A continuous landmark-relative coordinate (e.g., signed distance to L's designation in cycles); a multi-landmark joint coordinate (relative to a set of landmarks simultaneously); coordinates relative to append events instead of designation events (the original Candidate 1 design — withdrawn). |
| C1.3a | **Append-only hash-chained autobiography (SHA-256 chain).** | A Merkle-tree autobiography (tree-hash chain). |
| C1.3b | **Persisted monotone integer cycle counter.** | A cycle counter that is logical-clock-based (Lamport-style) rather than integer-increment. |
| C1.4 | **Landmark designation as a deferred event:** designation is a separate `designate_landmark()` operation, recorded in the append-only history, distinct from append. `coord_landmark_relative` references `L.designated_at`. | A candidate where designation is always at append (the original Candidate 1 design — withdrawn, unsatisfiable); a candidate where designation is implicit (e.g., the N-th append is automatically a landmark); a candidate with no separate designation concept (landmarks are a query-time projection, not a stored event). |

> **N10 fix (C1.3 split):** The original spec's D2 distinctness table listed C1.3 as a single item. The kill condition diagnoses (§5) referenced C1.3a (SHA-256 chain) and C1.3b (cycle counter) as separate choices. The table above splits C1.3 into C1.3a and C1.3b, matching the kill condition diagnoses.

> **D2 distinctness statement (pre-registered for the retry decision):** If Candidate 1.1 dies, Candidate 2 is "mechanistically distinct" iff it differs on at least one of C1.1/C1.2/C1.3a/C1.3b/C1.4 in a way that **engages the diagnosed cause of death**. A Candidate 2 that changes only constants (hash function, window size, seed handling, designation delay) is cosmetic and is rejected at sign-off per D2. The CRITIC polices this claim; Rebecca signs off.

#### 1.2.4 Distinctness note (D2 provenance — acceptance criterion 5)

**Candidate 1.1 is a REVISED DRAFT of Candidate 1.** The material change from the original Candidate 1 (as specified in the pre-CRITIC-review v1 spec) is:

| Aspect | Original Candidate 1 (v1, withdrawn) | Candidate 1.1 (v3, this spec) |
|---|---|---|
| Landmark designation | At append time (`is_landmark` flag on the entry; `L.designated_at == L.cycle` always) | A separate `designate_landmark()` event; `L.designated_at ≥ L.cycle`; can be deferred |
| `coord_landmark_relative(e, L)` reference | `L.cycle` (append position) | `L.designated_at` (designation event) |
| Distinctness claim (v2) | N/A (v1 had no distinctness claim — it was unsatisfiable) | **DROPPED.** Under the fair naive (which reads designation events), candidate == fair-naive == oracle on answers. Distinctness is operational (property (ii)) and integrative (property (iii)), not informational. |
| Test satisfiable? (v2 equivalence test) | **NO** (B1/B5: candidate == naive by construction) | **N/A — the equivalence test is RETIRED.** The three-property test (§6) replaces it. Property (i) correctness is satisfiable (candidate matches oracle). Property (ii) operational distinctness is satisfiable (candidate O(1)/O(log n) per query; fair-naive O(n) per query). Property (iii) load-bearing coupling is satisfiable (downstream consumer degrades under ablation). |
| L4 compliance | **VIOLATED by construction** (B5: candidate IS a `created_at` column with an O(1) optimization) | **COMPLIANT under the AMENDED L4 test** (the three-property test). The candidate re-resolves coordinates from maintained state (property (ii)), is correct (property (i)), and is load-bearing for a downstream consumer (property (iii)). |
| D2 distinctness rows | C1.1, C1.2, C1.3 (3 rows) | C1.1, C1.2, C1.3a, C1.3b, C1.4 (5 rows) |

**Why this is NOT a D2 retry:** Candidate 1.1 is a pre-build revision of the same candidate slot (Candidate 1). No scoring run has occurred. The original Candidate 1 was withdrawn during the CRITIC falsifiability re-review (it was unsatisfiable by construction). Candidate 1.1 is the revised draft. **Per Rebecca's ruling (§3), Candidate 1.1 is NOT charged as a death** — its v2 "distinctness" claim dissolves under the fair baseline, but the mechanism remains legitimate under the revised test. The retry budget remains 3, spent 0, remaining 3. If Candidate 1.1 dies in a scoring run, THAT would consume a retry, and Candidate 2 would need to differ on C1.1/C1.2/C1.3a/C1.3b/C1.4.

### 1.3 What the candidate is NOT (scope fence for the mechanism)

- **NOT a learned model.** No weights, no training, no gradient descent. The re-resolution is a deterministic algorithm (offset increment + categorical lookup + designation-event tracking). E1 tests whether this *simplest possible* re-resolver earns its place; if the simplest dies, a learned re-resolver is a Candidate 2 option (C1.1 differs).
- **NOT a full memory system.** No decay (L1), no thick-present (L3), no bi-temporality (L5), no provenance (L6). E1 tests ONLY the moving origin (L2 + L4, as amended). The candidate is a substrate, not a memory. (The minimal downstream consumer in property (iii) is a TOY retrieval implementing L1's access physics — it is a test instrument, not the full L1 system.)
- **NOT the idea.** The idea is the *property* (re-resolution + operational non-collapse + load-bearing coupling). The candidate is *one mechanism* exhibiting that property. Per D1, killing the candidate does not kill the idea.

---

## 2. The experiment

### 2.1 What E1 tests (THREE properties, jointly — per Rebecca's ruling §2)

E1 tests the **moving-origin property** via THREE properties, jointly. A candidate must pass ALL THREE to earn its place. The old single-axis equivalence test (candidate distinguishable from naive on answers) is RETIRED — Rebecca's theorem proves it is unsatisfiable by construction (fair-naive ≡ oracle).

**Property (i) — Correctness (kill (f), SIGNED, primary correctness kill).**
The candidate's answers to the full query battery — including deferred-designation landmark queries — must match the oracle's answers exactly: `oracle_agreement = 1.0`. The oracle is a perfect-knowledge structure that scans the autobiography AND the designation events and computes ground-truth coordinates. A candidate that does not match the oracle is wrong (kill (f) fires). This is the floor: a candidate that is wrong has no place, regardless of its operational or integrative properties.

**Property (ii) — Operational distinctness (kill (d), PROMOTED to discriminator).**
The FAIR naive arm — full event-log access (including designation events), recompute-by-scan/replay at query time, no maintained index state — must MATCH the candidate's answers (this is EXPECTED, no longer a kill — Rebecca's theorem: fair-naive ≡ oracle) and DIFFER in COST SCALING. The existing latency law (kill (d), locked bars UNCHANGED: 10× history ≤ 2× latency for the candidate) is PROMOTED to the discriminator. It is extended with a **state-dependent query battery** on which:
- Fair-naive's per-query cost provably scales with history length (it scans the log: O(n) per query).
- The candidate answers from maintained, incrementally re-resolved state (O(1) or O(log n) per query).
- BOTH scaling curves (candidate and fair-naive) are reported.
- The candidate collapses if its own scaling matches recompute-by-scan (i.e., it is secretly replaying) — this is the new anti-collapse discriminator, replacing the old answer-agreement collapse test.

**Property (iii) — Load-bearing coupling (E1-scale integration check, NEW).**
A MINIMAL DOWNSTREAM CONSUMER — a toy recency-weighted retrieval implementing L1's access physics over the index's coordinates — must measurably degrade when re-resolution is ablated (frozen-origin arm). Effect direction consistent across seeds. This is a miniature of the L15 test (which M5 will apply in full), placed at E1 because the theorem shows coupling, not answers, is where "moving origin" has meaning. *"A candidate whose coordinates are consumed by nothing is a cache with a philosophy."* (Rebecca, ruling §2(iii).)

Plus three structural checks (L2 chain integrity, coordinate shift, wall-clock independence) — see §5.

### 2.2 The synthetic autobiography (deterministic per seed)

E1 runs on a **synthetic autobiography with known ground truth**, generated deterministically per seed. The autobiography is the test fixture; the candidate mechanism is built over it.

**Parameters (constants, not tuned):**
- `N_cycles = 10` (the locked N — the number of cycles after the initial build; the "shift" is measured over these 10 cycles; 8 appends + 2 designations = 10 cycles).
- `N_entries_initial = 100` (entries appended before the first query — the "1× history" baseline).
- `N_entries_final = 1000` (entries after the 10× growth — the "10× history" latency probe; `1000 = 10 × 100`).
- `N_landmarks = 10` (entries designated as landmarks, deterministically per seed).
- `N_landmarks_immediate = 8` (landmarks designated at append time; `L.designated_at == L.cycle`).
- `N_landmarks_deferred = 2` (landmarks designated during the shift probe; `L.designated_at > L.cycle`).
- `seeds = [42, 43, 44]` (3 seeds; E1 is not in the 5-seed group).
- `N_queries = 200` (landmark-relative queries issued per measurement point, per seed).
- `N_state_dependent_query_points = 5` (history sizes at which the state-dependent battery is measured: 100, 250, 500, 750, 1000 entries — to fit both scaling curves; see §6.ii).
- `N_consumer_queries = 50` (query items for the property (iii) downstream consumer, per seed; see §6.iii).
- `consumer_feature_dim = 32` (dimension of the synthetic feature vectors in the payload and query items; see §6.iii).
- `consumer_tau = 50` (recency decay constant for the downstream consumer; see §6.iii).
- `consumer_k = 10` (top-k retrieval for the downstream consumer; see §6.iii).
- `consumer_recency_coupling_lambda = 16.0` (additive recency-coupling constant; the recency bonus `λ·exp(-coord/τ)` is bounded in `[0, λ]`, ~16% of the content signal `A²=100`; see §6.iii).
- `consumer_content_signal_amplitude = 10.0` (`A`; spike amplitude of the bucketed content signal; see §6.iii).
- `consumer_feature_noise_sigma = 0.10` / `consumer_query_noise_sigma = 0.10` (`σ_f`, `σ_q`; small noise on bucketed features and queries; see §6.iii).
- `rd_content_bucket_size = 30` (`K_rd > k`; each RD content bucket has 30 content-tied entries at spread cycles; see §6.iii).
- `cu_content_bucket_size = 10` (= `k`; each CU content bucket has exactly k entries; see §6.iii).
- `timing_repetitions = 100` (minimum repetitions per query per history-size point for the timing methodology; see §6.ii, §5d).

> **Why these numbers:** `N=10` is locked (M0). `100 → 1000` gives a clean 10× latency probe. `N_landmarks=10` gives enough landmark-relative queries to measure agreement without trivially saturating. `N_landmarks_immediate=8` + `N_landmarks_deferred=2` gives a MIX of immediate and deferred designation (the deferred landmarks supply the state-dependent battery's material — queries whose ground truth depends on designation events that occurred at different points in the history). `N_queries=200` gives a stable agreement estimate. `N_state_dependent_query_points=5` gives enough points to fit a scaling curve (candidate: flat or log; fair-naive: linear) and distinguish them. `N_consumer_queries=50` and `consumer_feature_dim=32` give a stable recall@k estimate for the downstream consumer without trivially saturating (50 queries × 10 results each gives 500 retrieval judgments per seed). **Property (iii) consumer constants (the Option E fix):** the consumer uses an ADDITIVE relevance `dot + λ·exp(-coord/τ)` (NOT the prior multiplicative `exp(-coord/τ)·dot` — the multiplicative form's 9-orders-of-magnitude recency gradient overwhelmed the content signal on all queries, failing CRITIC Verification (a); the additive form decouples content from recency). `consumer_tau=50` is UNCHANGED (pinned per Q3-1). The bucketed content signal (`A=10`, `σ_f=0.10`) creates clean content clusters with a ~50× gap that the bounded recency bonus (`λ=16`) cannot overturn on content-unique queries (CU degradation ≈ 0) but can break ties within on recency-discriminative queries (RD degradation > 0). `rd_content_bucket_size=30` (with `k=10`) sets the RD per-query degradation to ~0.25 → aggregate ~0.10, comfortably above the 0.05 floor (simulated, seeds 42/43/44). `timing_repetitions=100` is the minimum for the mandated timing methodology (median, warm-up excluded — resolves NB-6). All are constants; none is tuned against the candidate (the consumer constants are pre-registered here and verified by simulation before the CRITIC review).

### 2.3 Ground-truth construction (deterministic per seed)

Per seed `s`, the autobiography is constructed as follows (all RNG from `numpy.random.default_rng(s)`):

1. **Initial build (1× history, 100 entries):** append 100 entries. For entry `i ∈ {0..99}`:
   - `payload_i` = a synthetic item with a known landmark-membership bit: `is_landmark_i = True` if `i` is in a seeded random 10% subset (10 landmarks among 100 entries), else `False`. (So `N_landmarks = 10` by construction.)
   - The payload also carries a `content_id` (deterministic per i) so the test can compare index answers to oracle/fair-naive answers by content identity.
   - `cycle_i = i` (cycle counter increments per append; `created_at_i = i`).
   - **Immediate landmarks:** of the 10 landmark-eligible entries, 8 are designated at append time (`is_landmark=True` on the `append` call → `L.designated_at == L.cycle`). The 8 are chosen deterministically (seeded) from the 10.
   - **Deferred landmarks:** the remaining 2 landmark-eligible entries are appended WITHOUT `is_landmark` (so they are in the autobiography but NOT yet landmarks). They will be designated during the shift probe (step 2).
2. **The 10-cycle shift probe (N=10):** after the initial build (`now = 99`), perform 10 cycles. Each cycle is EITHER an append OR a designation:
   - Cycles 100–101: **designate the 2 deferred landmarks** (one `designate_landmark` call per cycle, advancing `now` to 100, then 101). These are the deferred-designation events: `L.designated_at = 100` and `L.designated_at = 101` for the two deferred landmarks (whose `L.cycle` is in the initial 0–99 range).
   - Cycles 102–109: **append 8 more entries** (`i ∈ {100..107}`), one per cycle, re-resolving the index after each. After each append, measure `coord_cycle_relative` shift on a fixed probe set of 10 prior entries (seeded). **The shift check (kill condition c)** confirms `coord_cycle_relative` increased by exactly 1 per append for every probed entry.
   - **N11 fix (intermediate chain_integrity):** after the initial build (now=99), after the shift probe (now=109), and after the 10× growth (now=999), record `chain_integrity` as a separate boolean. This lets the JUDGE distinguish a construction break (chain invalid from the start) from a re-resolution break (chain valid initially, breaks later). See §7.3.1.
   - **N12 fix (per-append shift):** for each of the 8 appends in the shift probe, record whether the shift occurred (`shift_per_append` array of 8 booleans). This lets the JUDGE distinguish a wiring defect (never shifts) from a partial mechanism failure (some shifts, some not). See §7.3.1.
3. **The 10× history latency probe:** after the shift probe, continue appending until `now = 999` (1000 entries total = 10× the initial 100). At `now = 999`, measure query latency. Compare to latency measured at `now = 99` (1× history).
4. **The state-dependent scaling battery (property (ii)):** at each of the 5 history-size points (100, 250, 500, 750, 1000 entries), measure per-query latency for BOTH the candidate and the fair-naive arm on the state-dependent query battery (§6.ii). Fit a scaling curve for each. The candidate's curve should be flat or logarithmic (O(1)/O(log n)); fair-naive's curve should be linear (O(n)).

### 2.4 The query set (deterministic per seed)

`N_queries = 200` landmark-relative queries, generated per seed:
- For each query `q ∈ {0..199}`: pick a landmark `L_q` (seeded, from the 10 landmarks — 8 immediate + 2 deferred) and a relation `r_q ∈ {BEFORE_L, AFTER_L}` (seeded, ~50/50). The query asks: "return the set of content_ids of entries with `coord_landmark_relative == r_q` relative to `L_q`."
- The **ground-truth answer** to each query is computed by an independent oracle (the `oracle index` arm, §3): a perfect-knowledge structure that scans the autobiography AND the designation events once and returns the exact set. This is the reference for property (i) (correctness, kill (f)).
- **The fair naive arm** reads the SAME event log (including designation events) and computes the SAME answers by scanning at query time. By Rebecca's theorem, fair-naive ≡ oracle on answers. The fair-naive arm's answers MATCH the candidate's answers (expected) — this is no longer a kill. The fair-naive arm's COST is the property (ii) probe.

> **Why the deferred-designation landmarks are RETAINED in the task design:** They are Conway-faithful (designation as a separate event is a real enrichment of the autobiography). They supply the state-dependent battery's material — queries whose ground truth depends on designation events that occurred at different points in the history, so the fair-naive arm must scan back to the designation event to recompute, and the candidate must have pre-resolved the coordinate at designation time. They carry NO distinctness claim (the old claim that candidate ≠ naive on answers is dissolved by the fair naive).

---

## 3. Control arms (the 6 arms, fully specified — naive arm STRENGTHENED to fair naive)

For each arm, the build cell produces a query-answer set per seed (the set of content_ids returned for each of the 200 queries) AND, for the candidate and fair-naive arms, a per-query latency measurement at each history-size point. All stochasticity is seeded. Each arm is a *complete alternative* to the candidate — it produces answers to the same 200 queries by a different method.

| # | Arm | What it does (exact) | What it tests | Expected result | L18 role |
|---|---|---|---|---|---|
| **1** | `frozen origin` | **(Option E — Rebecca's binding frozen-origin specification, per ruling §Q1):** The frozen arm retains ALL entries and ALL content, identical to the candidate's autobiography (all 1000 entries, same payloads, same feature vectors). Each entry's coordinates are computed ONCE, at its own append: `coord_cycle_relative = 0` at birth (`now_at_birth − e.cycle = e.cycle − e.cycle = 0`); `coord_landmark_relative` per the landmark registry state at that moment. These coordinates are NEVER re-resolved thereafter — re-resolution is disabled; nothing else is. The index accumulates all 1000 entries as they are appended (the index is append-aware — it stores every entry — but it does not re-resolve coordinates on subsequent appends or designations). Answer the 200 landmark-relative queries from the frozen index. **ALSO: serve as the ablation arm for property (iii)** — the downstream consumer (§6.iii) is run over BOTH the candidate's re-resolved index AND the frozen-origin index; the consumer must measurably degrade over the frozen index. The consumer is identical across arms — the ONLY difference between candidate and frozen is whether coordinates moved after birth. | Tests whether re-resolution matters. If frozen matches the candidate on the downstream consumer, re-resolution is decorative (property (iii) fails). | **(Option E consequence — to verify, not assume):** under E, every entry carries a permanently stale "just appended" coordinate — `coord_cycle_relative(e) = 0` for ALL entries, regardless of age. The recency gradient is destroyed while memory remains complete. This is the honest meaning of a frozen origin: content intact, temporal self-location gone. The frozen index's `coord_landmark_relative` is frozen per the registry state at each entry's birth (entries appended before a designation do not know about landmarks designated later — but all entries ARE present). Agreement with oracle on landmark-relative answer-sets: the frozen index answers membership queries using birth-time registry state (stale for entries whose landmark-relative relation would have changed after their birth); agreement with oracle < candidate's agreement with oracle on queries involving deferred-designation landmarks. **For property (iii):** the downstream consumer's retrieval quality over the frozen index DEGRADES relative to the candidate's index (effect direction consistent across seeds) — the consumer's recency weight `exp(−coord_cycle_relative/τ)` collapses to `exp(0) = 1.0` for all entries, destroying the recency gradient that the re-resolved candidate index provides. | Frozen baseline (static policy); ablation probe for property (iii). |
| **2** | `shuffled cadence` | Append the same 1000 entries but in a **shuffled order** (seeded permutation of the append sequence). **B3 fix (the "OR" is removed — exactly one implementation):** each entry's `prev_hash` references the predecessor in the **original (unshuffled) order**, so the entries are stored in shuffled order but their `prev_hash` fields point to the original predecessors. `verify_chain()` walks storage (shuffled) order, finds that each entry's `prev_hash` does NOT match the actual predecessor in shuffled order → `chain_integrity = False`. The landmark designation events are also shuffled (the 2 deferred landmarks are designated at shuffled cycles). Answer the 200 queries from an index built over the shuffled autobiography. | Tests whether cadence (L2) matters. If shuffled matches the candidate, the cadence is decorative. | Shuffled answers **diverge** from the candidate on landmark-relative queries (the `BEFORE_L / AFTER_L` relations are scrambled by the shuffle — entries that were before a landmark in the original order may be after it in the shuffled order). Agreement with oracle ≈ chance. **Chain integrity check (L2) FAILS** on the shuffled autobiography (the shuffled chain does not verify — `prev_hash` references the original predecessor, not the shuffled predecessor). | Contamination control (cadence destroyed → chance). |
| **3** | `oracle index` | A perfect-knowledge structure: scan the autobiography AND the designation events once, build a complete index with ground-truth coordinates (using `L.designated_at` for landmark-relative), answer the 200 queries exactly. This is the reference for property (i) (correctness, kill (f)) and the ceiling for query accuracy. | Positive control — proves the metric can leave zero (the index CAN answer the queries correctly). | Oracle answers = ground truth. Agreement with itself = 1.0. **The candidate must match the oracle exactly (`oracle_agreement = 1.0`) to pass property (i).** | Positive control (ceiling). |
| **4** | `fair naive` (was `naive now−created_at`) | **STRENGTHENED per Rebecca's ruling.** The fair naive arm reads the FULL event log — including designation events (`event_type = "designation"`, `ref`, `designated_at`) — exactly as the oracle does. It has NO maintained index state: no offset counter, no landmark registry with pre-computed coordinates, no incrementally re-resolved structure. At query time, for each of the 200 queries `(L_q, r_q)`, it **scans the autobiography** and computes `fair_naive_coord_landmark_relative(e, L_q) = BEFORE_L if e.cycle < L_q.designated_at else (AT_L if == else AFTER_L)` — using `L_q.designated_at` (which it reads from the designation event in the log). It returns the set of `content_id`s where the relation matches. **This is recompute-by-scan at query time, with full event-log access, no maintained index state.** It is the strongest honest timestamps-and-scan implementation. | Tests property (ii) (operational distinctness). The fair naive MATCHES the candidate on answers (expected — Rebecca's theorem: fair-naive ≡ oracle) and DIFFERS on cost scaling (fair-naive scans at O(n) per query; candidate answers at O(1)/O(log n) per query). | **Answers:** fair-naive answers == candidate answers == oracle answers (expected, no longer a kill). `equivalence_agreement` (candidate vs fair-naive) ≈ 1.0 — REPORTED as a diagnostic (§4.2), NOT a kill. **Cost scaling:** fair-naive per-query latency scales LINEARLY with history length (O(n) — it scans the log). The candidate's per-query latency is flat or logarithmic (O(1)/O(log n)). The scaling curves DIFFER. The collapse trigger is the candidate's locked latency bar (≤ 2.0× growth) on the state-dependent battery, validated by fair-naive's ≥ 4.0× growth — if the candidate's growth exceeds 2.0× on a validated battery, it is secretly replaying → kill (d) fires (property (ii) collapse; restructured per Rebecca's Q2 ruling — the slope ratio is a diagnostic only). | Naive baseline (the strongest honest timestamps-and-scan implementation). |
| **5** | `empty` | No memory. Return the empty set for every query. | Contamination control — empty store returns nothing. | Agreement with oracle = 0.0 (returns nothing; nothing matches). At chance floor. | Contamination control (empty → chance). |
| **6** | `wall-clock-injection` | **N1 fix (acknowledged as defensive check):** Build the candidate index normally, but **inject a wall-clock perturbation**: replace `created_at` (autobiography position) with a wall-clock timestamp for a subset of entries (seeded 20%), then re-resolve and answer the 200 queries. **Acknowledgment:** the candidate's coordinate computations use `e.cycle` and `L.designated_at`, NOT `created_at`. The injection of `created_at` has NO effect on the candidate's answers by construction. This arm is a **defensive check against a BUILDER implementation bug** (accidentally using `created_at` instead of `e.cycle` for coordinates, or accidentally making `designated_at` wall-clock-derived). It is NOT a mechanism-level L11 test — the candidate has no path to a private clock by construction. If the arm's answers differ from the candidate's unperturbed answers, kill condition (e) fires — indicating an implementation deviation (the BUILDER used `created_at` where the spec says `e.cycle`). | L11 falsification probe (defensive — detects implementation bugs, not mechanism-level violations). | **Coordinates must NOT shift with wall-clock perturbation.** If the wall-clock-injection arm's answers differ from the candidate's unperturbed answers, kill condition (e) fires. Expected: arm's answers == candidate's answers (wall-clock is ignored; only autobiography position matters). If they differ, the BUILDER has an implementation bug (used `created_at` instead of `e.cycle`, or made `designated_at` wall-clock-derived). | L11 falsification probe (defensive check). |

> **The 6 arms produce 6 answer-sets per seed.** Property (i) (correctness) compares the candidate's answer-set to the oracle arm's answer-set (kill (f)). Property (ii) (operational distinctness) compares the candidate's and fair-naive's COST SCALING curves (kill (d)). Property (iii) (load-bearing coupling) runs the downstream consumer over the candidate's index AND the frozen-origin index and compares degradation. The other arms are controls: shuffled (cadence matters), empty (chance floor), wall-clock-injection (L11 holds / no implementation bug).

> **The fair naive arm is the CRITIC's new center of gravity (§9 step 2).** The CRITIC must verify: (a) the fair naive reads the FULL event log including designation events (not handicapped); (b) the fair naive has NO maintained index state (recompute-by-scan at query time); (c) the fair naive computes the SAME answers as the candidate and oracle (Rebecca's theorem); (d) the fair naive's per-query cost scales with history length (O(n) scan). If any of these fails, the fair naive is a strawman and the test is vacuous.

---

## 4. Metrics and bars

E1 evaluates the THREE properties plus three structural checks, each with a locked bar. All are defined so the kill conditions (§5) are unambiguous.

### 4.1 Metrics (three-property test + structural checks)

| # | Metric | Definition (exact) | Locked bar | Kill condition it feeds | Property |
|---|---|---|---|---|---|
| **E1-M1** | `oracle_agreement` | Agreement between the candidate's answer-set and the oracle arm's answer-set, over the 200 landmark-relative queries (including deferred-designation landmark queries), averaged over the 3 seeds. **Agreement per query = 1 if the candidate's answer-set equals oracle's answer-set (same set of content_ids), else 0.** (Exact-set equality; see §6.i.) | **= 1.0** (correctness floor). < 1.0 = wrong. | (f) | (i) Correctness |
| **E1-M2** | `latency_ratio` | **B2 fix (retained) + property (ii) extension:** `latency(10× history) / latency(1× history)`, where latency = mean wall-clock seconds per **bounded-output query** call over the 200 queries, per seed, then averaged over 3 seeds. Measured on TWO bounded-output query types (both reported, both must pass the bar): (i) `query_membership(e, L, relation)` — O(1) answer (single boolean); (ii) `query_landmark_relative_bounded(L, relation, k=10)` — bounded by k=10. **Neither query type materializes an unbounded answer set**, so the latency ratio isolates the lookup algorithm's complexity. (Measured on the candidate arm only.) | **≤ 2.0** (the locked "10× history ≤ 2× 1× history"). > 2.0 = scanning detected. | (d) | (ii) Operational distinctness |
| **E1-M2b** | `state_dependent_collapse` | **(property (ii) state-dependent battery — restructured per Rebecca's Q2 ruling):** The collapse criterion is NO LONGER a slope ratio. It is built from the locked latency bar (≤ 2.0×) applied to the state-dependent battery, with a battery-validity requirement on the fair-naive arm. **(1) Candidate side (kill (d) trigger, the locked bar):** the candidate's 10×-history latency growth on the state-dependent battery — `candidate_latency_growth_10x = latency(history=1000) / latency(history=100)` — must be ≤ 2.0×. **(2) Battery-validity requirement (NEW, NOT a candidate kill):** the fair-naive on the SAME battery must show 10×-history latency growth ≥ 4.0× (`fair_naive_latency_growth_10x ≥ 4.0`). If it does not, the battery is too easy to expose scan cost — an INSTRUMENT failure: the run is unscoreable, the battery is revised, and no kill condition or retry budget is touched. **(3) Collapse** = the candidate failing bar (1) (growth > 2.0×) on a battery validated by (2). **(4) The slope ratio** (`scaling_collapse_ratio = candidate_slope / fair_naive_slope`) is **RETAINED as a REPORTED diagnostic ONLY, never a trigger** (resolves NB-1). See §6.ii for the full criterion, the timing methodology (which resolves NB-6), and the instrument-failure routing. | **candidate_latency_growth_10x ≤ 2.0** on a battery where `fair_naive_latency_growth_10x ≥ 4.0`. If the battery is invalid (fair-naive growth < 4.0×) → INSTRUMENT failure (run unscoreable, battery revised — no kill, no retry budget touched). If the battery is valid AND candidate growth > 2.0× → collapse → kill (d) fires. | (d) | (ii) Operational distinctness |
| **E1-M3** | `chain_integrity` | Boolean per seed: does `verify_chain()` return `valid=True` on the candidate's autobiography (initial build + shift probe + 10× growth)? Averaged as the fraction of seeds with `valid=True`. **N11 fix:** `chain_integrity` is reported at THREE stages (after initial build, after shift probe, after 10× growth) so the JUDGE can distinguish construction breaks from re-resolution breaks (see §5b, §7.3.1). The kill-condition (b) metric uses the FINAL stage. | **= 1.0** (all 3 seeds valid at final stage). < 1.0 = chain broke on some seed. | (b) | structural (L2) |
| **E1-M4** | `coordinate_shift` | Per seed: did `coord_cycle_relative` increase by exactly 1 per append for every probed entry, over the 8 appends in the shift probe? Boolean per seed. Averaged as the fraction of seeds with exact-shift. **N12 fix:** `shift_per_append` (array of 8 booleans, one per shift-probe append) is reported per seed, so the JUDGE can distinguish a wiring defect (never shifts) from a partial mechanism failure (some shifts, some not) (see §5c, §7.3.1). The kill-condition (c) metric uses the overall boolean. | **= 1.0** (all 3 seeds show exact shift). < 1.0 = no measurable shift on some seed. | (c) | structural (L4 re-resolution) |
| **E1-M6** | `downstream_degradation` | **NEW (property (iii) load-bearing coupling):** The minimal downstream consumer (§6.iii) is run over BOTH the candidate's re-resolved index AND the frozen-origin index (ablation). The consumer's retrieval quality is measured (recency-weighted recall@k against ground truth). **Degradation metric:** `degradation = quality_candidate - quality_frozen` (positive = candidate better than frozen = re-resolution is load-bearing). **Consistency requirement:** degradation must be POSITIVE on ALL 3 seeds (effect direction consistent). The magnitude bar (Rebecca's L15 floor, d ≥ 0.5, applied at E1-scale as a miniature): the MEAN degradation across seeds must be ≥ a pre-registered floor (see §6.iii for the floor). | **degradation > 0 on all 3 seeds AND mean_degradation ≥ floor** (§6.iii). If degradation ≤ 0 on any seed OR mean < floor → property (iii) fails → candidate does not earn its place (see §5 for the kill routing). | (see §5 — property (iii) failure) | (iii) Load-bearing coupling |
| **E1-M5** | `wall_clock_shift_detected` | Qualitative → boolean: the wall-clock-injection arm's answer-set is compared to the candidate's unperturbed answer-set. If they differ on ANY query (per seed), kill condition (e) fires. Strict equality check (no tolerance). (Reported as `wall_clock_shift_detected: bool` per seed.) | **= False** (no shift on any seed). If True on any seed → kill (e). | (e) | structural (L11) |

**Direction rule (locked):** E1-M1 (oracle_agreement) is **higher-is-better** (= 1.0 is good). E1-M2 (latency_ratio) is **lower-is-better** (low ratio = no scanning = good). E1-M2b (state_dependent_collapse) is **lower-is-better** (low candidate latency growth = candidate scales better than scan = good); the battery-validity check (fair_naive_latency_growth_10x) is **higher-is-better** (≥ 4.0× = battery exposes scan cost = valid). E1-M3 and E1-M4 are **higher-is-better** (= 1.0 is good). E1-M6 (downstream_degradation) is **higher-is-better** (positive = re-resolution is load-bearing = good). E1-M5 is **lower-is-better** (= False is good). The bars are stated in the natural direction for each.

### 4.2 Reported diagnostics (NOT barred — retired metrics and raw sizes)

The following are REPORTED in the artifact (§7.3.1) for diagnostic transparency but carry NO kill and NO distinctness claim:

- **`equivalence_agreement` (RETIRED metric):** Agreement between the candidate's answer-set and the fair-naive arm's answer-set, over the 200 queries, averaged over 3 seeds. Per Rebecca's theorem, this is EXPECTED to be ≈ 1.0 (fair-naive ≡ oracle on answers). It is REPORTED to confirm the theorem holds (the fair naive is not handicapped) and to document that the old kill (a) is unsatisfiable by construction. **It carries NO kill.** If `equivalence_agreement` is NOT ≈ 1.0 (e.g., < 0.95), it indicates the fair naive arm is handicapped (not reading designation events) — a BUILDER implementation bug, not a candidate property. The CRITIC checks this at review.
- **`raw_answer_size_1x`, `raw_answer_size_10x`, `raw_answer_size_ratio`** (B2 fix, retained): mean number of content_ids returned by the UNBOUNDED `query_landmark_relative` at 1× and 10× history, and their ratio. Expected ~10× (answer-set size grows with history). REPORTED, not BARRED. Documents that the unbounded query's answer-set grows ~10× with history (confirming the CRITIC's B2 analysis). The latency bar (E1-M2) is NOT measured on these unbounded queries — it is measured on the bounded-output queries (§4.1), so the bar isolates algorithmic complexity.
- **`candidate_scaling_curve` and `fair_naive_scaling_curve`** (property (ii)): the per-query latency at each of the 5 history-size points (100, 250, 500, 750, 1000), for both the candidate and the fair-naive arm, plus the fitted slopes. REPORTED so the JUDGE and CRITIC can inspect the scaling curves directly.
- **`scaling_collapse_ratio` (slope ratio — RETAINED as a REPORTED diagnostic ONLY, never a trigger; resolves NB-1):** `candidate_slope / fair_naive_slope`. Per Rebecca's Q2 ruling, the slope ratio is NO LONGER a collapse trigger — it is fragile at toy scale (fitted slopes sit near the timing noise floor, and a ratio with a near-zero denominator can fire on timer jitter). The collapse trigger is now the candidate's locked latency bar (≤ 2.0× growth) on a battery validated by fair-naive's ≥ 4.0× growth (§6.ii). The slope ratio is reported for diagnostic transparency only — it carries NO kill.

> **N2 fix (oracle-vs-naive sanity check DROPPED, RETAINED):** Per the CRITIC's recommendation (Rebecca ruling §4 item 1: APPROVED for removal), the oracle-vs-naive sanity check is DROPPED. Under the fair baseline it is incoherent as specified (oracle and fair-naive both compute ground truth correctly from the same event log; they agree on all queries). The load-bearing checks are: property (i) (candidate vs oracle, kill (f)) and property (ii) (candidate vs fair-naive cost scaling, kill (d)).

---

## 5. Kill conditions (5 active: b, c, d, e, f — old (a) RETIRED, explicit)

Each kill condition is stated with: (i) the trigger, (ii) what happens when it fires, (iii) the metric that detects it, (iv) the D2 diagnosis format, (v) the construction-bug-vs-mechanism-death guard (Rebecca ruling §4 items 4–5: APPROVED with guard). **A single hit terminates E1.** Per D1, the candidate is dead immediately; the idea has 2 retries under D2.

> **Construction-bug-vs-mechanism-death guard (Rebecca ruling §4 items 4–5, APPROVED with guard):** Bug attribution requires the **specific defect identified, fixed, and CRITIC-confirmed** before any re-run escapes the D2 budget. "Probably a bug" never does. This guard applies to kill (b) (chain construction), kill (c) (wiring), and kill (e) (wall-clock implementation bug). A re-run after a confirmed construction/wiring bug fix is NOT result laundering (the run never scored — per §0.7, only scoring runs through Rebecca's courier channel count).

### Kill condition (a) — L4 collapses to naive recomputation — RETIRED

- **Status:** **RETIRED** per Rebecca's E1 gate ruling (§12). The informational collapse test (answer-agreement vs naive) is unsatisfiable by construction: Rebecca's theorem proves that for any deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle, so naive_agreement is always 1.0 for a correct candidate. The pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable. A criterion nothing can pass is a broken criterion, not a hard one.
- **Rationale logged:** §12 (constitution amendment log). The metric `equivalence_agreement` is retained as a REPORTED diagnostic (§4.2) to confirm the theorem holds and the fair naive is not handicapped. It carries NO kill and NO distinctness claim.
- **What replaces it:** Property (ii) operational distinctness (kill (d), PROMOTED) — the candidate's distinctness from fair-naive is now defined by COST SCALING (the candidate answers from maintained state at O(1)/O(log n); fair-naive scans at O(n)), not by answer-agreement. The candidate collapses if it fails the locked latency bar (≤ 2.0× growth) on the state-dependent battery, validated by fair-naive's ≥ 4.0× growth (§6.ii).

### Kill condition (b) — Hash chain breaks (construction vs re-resolution, per Rebecca ruling §4 item 4)

- **Trigger:** `chain_integrity` (E1-M3, final stage) < **1.0** (the chain fails to verify on any seed after the initial build + shift probe + 10× growth).
- **What happens:** The append-only hash chain does not hold. L2 is falsified for Candidate 1.1. The run stops; the RECORDER logs "Candidate 1.1 died: hash chain broke at cycle X on seed Y (chain_integrity < 1.0)." Kill condition (b) fires.
- **Metric:** E1-M3 (final stage).
- **Diagnosis format (D2 support):** state whether the break is in the chain **construction** (C1.3a: SHA-256 chain) or the **re-resolution corrupting the chain**. **N11 fix (intermediate chain_integrity artifacts):** the JUDGE uses the three-stage `chain_integrity` records (after initial build, after shift probe, after 10× growth) to determine WHEN the chain broke:
  - If `chain_integrity_after_initial_build == False` → **construction break** (C1.3a wrong; the chain was never valid). **Rebecca ruling §4 item 4 (APPROVED with guard):** a construction break is a **BUILDER defect**, NOT a candidate death. The mechanism is sound; the implementation is wrong. Fix and re-run (which is NOT result laundering, because the run never scored — per §0.7, only scoring runs through Rebecca's courier channel count). The candidate is NOT dead; the BUILDER fixes the construction bug and re-runs. **Guard:** the specific defect must be identified, fixed, and CRITIC-confirmed before the re-run escapes the D2 budget. "Probably a bug" never does.
  - If `chain_integrity_after_initial_build == True` but `chain_integrity_after_shift_probe == False` (or `after_10x_growth == False`) → **re-resolution break** (the chain was valid after construction, broke after re-resolution). This IS a mechanism death — the candidate's own re-resolution step breaks L2. Kill (b) fires; the candidate is dead. A Candidate 2 differing on C1.3a (Merkle-tree) would engage this cause.

### Kill condition (c) — No measurable shift (wiring defect vs mechanism death, per Rebecca ruling §4 item 5)

- **Trigger:** `coordinate_shift` (E1-M4) < **1.0** (the index's `coord_cycle_relative` does NOT increase by exactly 1 per append for every probed entry, on any seed, over the 8 appends in the shift probe).
- **What happens:** The index's coordinates do not re-resolve as `now` advances. L4's "coordinates re-resolve as now advances" is falsified. The run stops; the RECORDER logs "Candidate 1.1 died: no measurable coordinate shift over N=10 cycles on seed Y (coordinate_shift < 1.0)." Kill condition (c) fires.
- **Metric:** E1-M4.
- **Diagnosis format (D2 support):** state whether the shift failed because the offset-counter (C1.1) is not incrementing, or because the probe is reading stale values. **N12 fix (per-append shift artifacts):** the JUDGE uses the `shift_per_append` array (8 booleans, one per shift-probe append) to determine HOW the shift failed:
  - If all 8 are `False` → **wiring defect** (the re-resolution step is not connected to the append path; the offset-counter never increments). **Rebecca ruling §4 item 5 (APPROVED with guard):** a wiring defect is a **BUILDER defect**, NOT a candidate death. The mechanism is sound; the wiring is wrong. Fix and re-run (NOT result laundering — the run never scored). The candidate is NOT dead; the BUILDER fixes the wiring and re-runs. **Guard:** the specific defect must be identified, fixed, and CRITIC-confirmed before the re-run escapes the D2 budget.
  - If some are `True` and some `False` → **partial mechanism failure** (the re-resolution shifts sometimes but not always). This IS a mechanism death — the offset-counter design (C1.1) is fundamentally broken. Kill (c) fires; the candidate is dead. A Candidate 2 differing on C1.1 (a non-offset re-resolver) would engage this cause.

### Kill condition (d) — Scanning detected / scaling collapse (PROMOTED to operational-distinctness discriminator, per Rebecca ruling §2(ii))

- **Trigger:** EITHER:
  - (d1) `latency_ratio` (E1-M2) > **2.0** (query latency at 10× history exceeds 2× query latency at 1× history, averaged over 3 seeds, **measured on bounded-output queries** — `query_membership` and `query_landmark_relative_bounded(k=10)`). [The locked latency bar, retained.] OR
  - (d2) `state_dependent_collapse` (E1-M2b): the candidate's 10×-history latency growth on the state-dependent battery exceeds 2.0× (`candidate_latency_growth_10x > 2.0`) on a battery validated by the fair-naive's 10×-history latency growth ≥ 4.0× (`fair_naive_latency_growth_10x ≥ 4.0`). [The state-dependent battery collapse criterion, restructured per Rebecca's Q2 ruling — the slope ratio is NO LONGER a trigger; it is a reported diagnostic only.]
  - **Battery-validity (instrument check, NOT a candidate kill):** if the fair-naive's 10×-history latency growth on the state-dependent battery is < 4.0×, the battery is too easy to expose scan cost — an INSTRUMENT failure: the run is **unscoreable**, the battery is revised, and **no kill condition or retry budget is touched** (the candidate is neither dead nor exonerated; the battery is fixed and the run repeated). This is not routed to kill (d); it is routed to the ARCHITECT/CRITIC for battery revision.
- **What happens:** The candidate's query latency scales with history size — the index is scanning (d1) or collapsing on the state-dependent battery (d2), not answering from maintained state. L4's "answered from the index without scanning" is falsified, AND property (ii) (operational distinctness) fails — the candidate has not earned its operational distinctness from fair-naive. The run stops; the RECORDER logs "Candidate 1.1 died: scanning/collapse detected (latency_ratio = X > 2.0 [d1] OR candidate_latency_growth_10x = Y > 2.0 on a battery where fair_naive_latency_growth_10x = Z ≥ 4.0 [d2]; the candidate's cost scaling matches recompute-by-scan)." Kill condition (d) fires.
- **Metric:** E1-M2 (bounded-output latency ratio) AND E1-M2b (state-dependent battery collapse, restructured).
- **Diagnosis format (D2 support):** state whether the scan/collapse is in `query_membership` / `query_landmark_relative_bounded` (the lookup), in `re_resolve_index` (the re-resolution), or in the state-dependent battery (the candidate is secretly replaying the log at query time instead of reading maintained state). A Candidate 2 differing on C1.1 (a non-scan re-resolver, e.g., a tree-based index) would engage a scan cause.
- **B2 fix (retained, why d1 is satisfiable):** the latency bar is measured on bounded-output queries (membership: O(1) answer; bounded-k: ≤10 entries). The answer-set size does NOT grow with history, so the latency ratio isolates the lookup algorithm's complexity: an O(1) indexed lookup gives ratio ≈ 1.0; an O(n) scan gives ratio ≈ 10×. The bar (≤ 2.0) distinguishes them.
- **Property (ii) extension (why d2 is the anti-collapse discriminator, restructured per Rebecca's Q2 ruling):** the state-dependent battery (§6.ii) measures per-query latency at 5 history-size points for BOTH the candidate and the fair-naive arm. The candidate answers from maintained, incrementally re-resolved state (O(1)/O(log n) per query — flat or logarithmic scaling). The fair-naive recomputes by scan (O(n) per query — linear scaling). **The collapse trigger is the candidate's locked latency bar (≤ 2.0× growth) applied to this battery**, NOT a slope ratio. The slope ratio (`scaling_collapse_ratio = candidate_slope / fair_naive_slope`) is RETAINED as a reported diagnostic ONLY (§4.2) — it is fragile at toy scale (NB-6: fitted slopes sit near the timing noise floor, and a ratio with a near-zero denominator can fire on timer jitter; a kill condition must not be able to fire on jitter). The battery-validity requirement (fair-naive ≥ 4.0× growth) ensures the battery is hard enough to expose scan cost before the candidate's bar is evaluated — if the fair-naive itself does not scale, the battery is an instrument failure, not a candidate property. This is the replacement for the old answer-agreement collapse test: the candidate's distinctness from fair-naive is operational (cost scaling), not informational (answer agreement).
- **Timing methodology (mandated per Rebecca's Q2 ruling item 4; resolves NB-6):** all latency measurements in the state-dependent battery (and in d1) use: (i) **median** over repeated executions per point (minimum 100 repetitions per query per history-size point), (ii) **warm-up excluded** (the first 10% of repetitions at each point are discarded), (iii) **monotonic clock** (`time.monotonic_ns()` or equivalent — never wall-clock `time.time()`), (iv) **dispersion reported alongside every latency figure** (interquartile range or standard deviation, per point). This methodology ensures the collapse criterion cannot fire on timer jitter (NB-6 resolved).

### Kill condition (e) — Coordinates shift with wall-clock perturbation

- **Trigger:** `wall_clock_shift_detected` (E1-M5) = **True** on any seed (the wall-clock-injection arm's answer-set differs from the candidate's unperturbed answer-set on ANY query).
- **What happens:** The candidate's coordinates respond to wall-clock, not autobiography position. L11 (one clock) is violated — the candidate has a private clock. The run stops; the RECORDER logs "Candidate 1.1 died: coordinates shifted with wall-clock perturbation on seed Y (private clock detected, L11 violation)." Kill condition (e) fires.
- **Metric:** E1-M5 (qualitative → boolean).
- **Diagnosis format (D2 support):** state whether the wall-clock leak is in `created_at` (C1.3b: the cycle counter is wall-clock-derived) or in `designated_at` (C1.4: designation events are wall-clock-stamped) or in the re-resolution. **N1 acknowledgment:** the candidate uses `e.cycle` and `L.designated_at` (both autobiography-position-derived), NOT `created_at`. A spec-compliant candidate has no path to a private clock by construction. If kill (e) fires, it indicates a BUILDER implementation bug (used `created_at` instead of `e.cycle`, or made `designated_at` wall-clock-derived). **Construction-bug guard (Rebecca ruling §4):** the specific defect must be identified, fixed, and CRITIC-confirmed before a re-run escapes the D2 budget. The CRITIC should assess whether this is a BUILDER defect (fix and re-run) or a mechanism death; the disposition parallels kill (b)/(c).

### Kill condition (f) — Candidate is wrong (does not match oracle) — SIGNED and PROMOTED to primary correctness kill (per Rebecca ruling §2(i), §4 item 3)

- **Trigger:** `oracle_agreement` (E1-M1) < **1.0** (averaged over 3 seeds, with strict `== 1.0` required). I.e., the candidate's answers differ from the oracle's answers on ANY query in the full query battery (including deferred-designation landmark queries) — the candidate is WRONG (does not match the ground truth).
- **What happens:** The candidate is incorrect. Property (i) (correctness) fails. The run stops; the RECORDER logs "Candidate 1.1 died: does not match oracle (oracle_agreement = X < 1.0; incorrect re-resolver). Property (i) fails." Kill condition (f) fires. **SIGNED by Rebecca (ruling §4 item 3: "APPROVED and promoted per §2(i)").** This is the primary correctness kill condition. A candidate that is wrong has no place, regardless of its operational or integrative properties.
- **Metric:** E1-M1 (`oracle_agreement`).
- **Diagnosis format (D2 support):** state which re-resolution step is wrong (e.g., designation tracking is buggy, offset-counter drifts, landmark registry is corrupt, the candidate uses the wrong reference for `coord_landmark_relative`). A Candidate 2 differing on C1.1/C1.2/C1.4 would engage the diagnosed cause.
- **Status:** **SIGNED.** No longer PENDING. Rebecca signed kill (f) at the gate (ruling §4 item 3). The build cell implements it as written.

### Property (iii) failure routing (load-bearing coupling — NOT a separate kill condition, but a gate on earning the place)

- **Trigger:** `downstream_degradation` (E1-M6) fails: degradation ≤ 0 on any seed (the frozen-origin ablation does NOT degrade the downstream consumer on some seed — effect direction inconsistent) OR mean_degradation < floor (§6.iii).
- **What happens:** Property (iii) (load-bearing coupling) fails — the candidate's coordinates are not load-bearing for a downstream consumer. *"A candidate whose coordinates are consumed by nothing is a cache with a philosophy."* The candidate has NOT earned its place as a moving origin, even if properties (i) and (ii) pass. **Routing:** this is NOT a separate kill condition (it is not in the locked 5); it is a GATE on the E1 pass verdict. If property (iii) fails, E1 is NOT delivered green (§10.3). The candidate is not dead (D1 does not fire — no kill condition fired), but the moving origin has not earned its place. The program pauses for Rebecca's decision: (a) the downstream consumer or ablation is mis-specified (a spec/implementation issue — fix and re-run, NOT a candidate death), or (b) the candidate's coordinates are genuinely not load-bearing (a mechanism limitation — Candidate 1.1 does not earn its place; the program routes to the D2 retry decision). Rebecca rules at the gate. **This routing parallels the construction-bug guard:** the specific cause (consumer mis-specified vs. coordinates not load-bearing) must be identified and CRITIC-confirmed before any re-run escapes the D2 budget.

> **Order of evaluation (locked):** the kill conditions (b, c, d, e, f) are evaluated **simultaneously** from the single run's artifacts. There is no priority ordering; if multiple fire, all are logged. The candidate is dead on the first fire; subsequent fires are additional diagnosis, not additional kills. Property (iii) is evaluated alongside the kill conditions; if it fails (and no kill condition fires), the candidate is not dead but E1 is not green (see routing above).

---

## 6. The three-property test (replaces the old §6 equivalence test — the CRITIC's new center of gravity)

> Per Rebecca's E1 gate ruling (§2): the moving origin is demonstrated by THREE PROPERTIES, jointly. This section makes each property fully explicit so that the JUDGE scores it by **arithmetic on the returned artifacts**, with no judgment calls. Every term is pinned. The CRITIC is directed (§9 step 2) to treat this section as the review's center of gravity — specifically, the fair-naive definition (§6.ii) and the state-dependent battery (§6.ii), and the downstream consumer (§6.iii).

### 6.i Property (i) — Correctness (kill (f), SIGNED, primary correctness kill)

**What queries:** the full query battery — 200 landmark-relative queries per seed (§2.4), including the ~20% that involve deferred-designation landmarks (whose ground truth depends on designation events that occurred at different points in the history). The candidate must match the oracle on ALL of them, including the deferred-designation queries.

**What oracle:** the `oracle index` arm (§3 arm 3) — a perfect-knowledge structure that scans the autobiography AND the designation events once and computes ground-truth coordinates using `L.designated_at` (the designation event). The oracle is a log replay: it reads the full event log and computes the exact answer. (Per Rebecca's theorem, the oracle is what fair-naive computes — but the oracle is the reference, not a competitor.)

**What agreement metric:** per-query agreement is binary, exact-set equality:
```
agreement_vs_oracle(q) = 1 if candidate_answer(q) == oracle_answer(q) else 0
```
where `==` is **exact set equality** on `content_id`s (same elements, regardless of order). No partial credit. No tolerance. A query agrees iff the candidate and oracle return the **identical set** of content_ids.

**Aggregate agreement (the E1-M1 metric):**
```
oracle_agreement = (1/3) * sum_over_seeds[ (1/200) * sum_over_queries[ agreement_vs_oracle(q) ] ]
```
I.e., the mean over 3 seeds of the mean over 200 queries of the binary agreement. A number in [0.0, 1.0].

**Bar:** `oracle_agreement = 1.0` (strict). < 1.0 → kill (f) fires. The candidate must be correct on ALL queries on ALL seeds. This is the floor: a candidate that is wrong has no place.

**Why this is satisfiable:** the candidate's `coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.designated_at` is the SAME computation the oracle performs (both use `L.designated_at`). A correctly-implemented candidate matches the oracle exactly. The bar tests whether the BUILDER implemented the re-resolver correctly (no drift, no corruption, correct designation tracking). It is a correctness floor, not a distinctness test.

**Scoring is arithmetic:** the JUDGE reads `oracle_agreement` (a float) from `e1_run_results.json` (§7.3.1), applies the bar (`< 1.0` → kill (f) fires), and verifies the arithmetic from the per-query agreement arrays (which ship in the artifact). No judgment calls.

### 6.ii Property (ii) — Operational distinctness (kill (d), PROMOTED to discriminator — the NEW anti-collapse discriminator)

**The fair naive definition (the CRITIC's center of gravity):**

The fair naive arm (§3 arm 4) is the strongest honest timestamps-and-scan implementation:
- **Full event-log access:** it reads the SAME event log the candidate and oracle read — including append events AND designation events (`event_type = "designation"`, `ref`, `designated_at`). It is NOT handicapped. (The old `naive now−created_at` arm was handicapped: it read only the `created_at` column and did NOT receive designation events. That handicapping is what made the old existence proof appear to show candidate ≠ naive. Rebecca's ruling: the fair naive reads the full event log.)
- **Recompute-by-scan at query time:** for each query, it scans the autobiography and computes `fair_naive_coord_landmark_relative(e, L_q) = BEFORE_L if e.cycle < L_q.designated_at` (using `L_q.designated_at` from the designation event in the log). It does NOT pre-compute or cache coordinates.
- **No maintained index state:** it has NO offset counter, NO landmark registry with pre-computed coordinates, NO incrementally re-resolved structure. It recomputes from scratch on every query.
- **Same answers as the candidate and oracle:** by Rebecca's theorem, fair-naive ≡ oracle on answers (both read the same event log and compute the same function). The fair naive MATCHES the candidate on answers — this is EXPECTED and no longer a kill. The reported `equivalence_agreement` (candidate vs fair-naive) is ≈ 1.0 (§4.2 diagnostic).

**The state-dependent query battery:**

The state-dependent battery measures per-query latency at 5 history-size points: `N_state_dependent_query_points = 5` points at history sizes {100, 250, 500, 750, 1000} entries. At each point, the 200 queries are issued to BOTH the candidate and the fair-naive arm, and per-query latency (wall-clock seconds) is recorded.

**Why state-dependent:** the queries' ground truth depends on the state of the index at the time of the query — specifically, on the designation events that have occurred by that history size. At history size 100, only the 8 immediate landmarks are designated (the 2 deferred landmarks are designated at cycles 100–101, which are AFTER the initial 100). At history size 250+, all 10 landmarks are designated. So the fair-naive arm, at history size 100, scans only the 8 immediate designations; at history size 250+, it scans all 10 designations AND must scan back to the designation event to recompute the coordinate for each entry. The candidate, by contrast, has pre-resolved the coordinate at designation time (operation 6, `designate_landmark`) and answers from maintained state at O(1)/O(log n) per query, regardless of history size. **The deferred-designation landmarks supply the state-dependent battery's material** — they are the queries whose recomputation cost depends on the state of the log at query time.

> **NB-5 resolved (Rebecca's unprompted completion):** At each history size, the query battery includes only landmarks designated by that point in the run. Deferred-designation queries against not-yet-designated landmarks are ill-posed and excluded by construction — a query about a landmark `L` that has not yet been designated (no `designated_at` value) asks "return entries before L" where L is not yet a landmark; such queries are NOT issued. At history size 100, only the 8 immediate landmarks are in the query battery (the 2 deferred landmarks enter the battery at history size 250+, after their designation at cycles 100–101). This is not a gap — it is the correct construction: the battery measures cost against landmarks that EXIST at that point in the run.
>
> **The pre-designation window IS the shift-measurement material.** During the window between `L.cycle` (append) and `L.designated_at` (designation), entries exist in the autobiography whose `coord_landmark_relative` relative to `L` is not yet defined. Upon designation, these entries flip from "not yet relative to L" to `BEFORE_L` (entries with `e.cycle < L.designated_at`) — this is the **re-resolution event**. Entries whose `e.cycle` falls in `[L.cycle, L.designated_at)` shift from `AFTER_L` to `BEFORE_L` upon designation (they were appended after `L` was appended, but before `L` was designated, so they are `BEFORE_L` relative to the designation event). This `AFTER_L → BEFORE_L` flip is exactly the shift that kill (c)'s per-append shift artifacts (§5c, N12) capture: the designation event re-resolves coordinates, and the shift artifacts record whether the re-resolution occurred. The pre-designation window is not an edge case to be worked around — it is the shift-measurement material itself.

**The scaling curves (both reported):**
- **Candidate scaling curve:** per-query latency at each of the 5 history-size points, for the candidate. Expected: flat or logarithmic (O(1)/O(log n) per query — the candidate reads maintained state).
- **Fair-naive scaling curve:** per-query latency at each of the 5 history-size points, for the fair-naive arm. Expected: linear (O(n) per query — the fair-naive scans the log).
- Both curves and their fitted slopes are REPORTED in the artifact (§7.3.1: `candidate_scaling_curve`, `fair_naive_scaling_curve`, `candidate_slope`, `fair_naive_slope`).

**The collapse criterion (the anti-collapse discriminator, restructured per Rebecca's Q2 ruling — replaces old kill (a)):**

> **Restructure note (Rebecca's Q2 ruling, binding):** The 0.5 slope-ratio collapse trigger (`candidate_slope > 0.5 × fair_naive_slope`) is **NOT SIGNED** and is **REPLACED**. NB-6 identified a real fragility: fitted slopes at toy scale sit near the timing noise floor, and a ratio with a near-zero denominator can fire on timer jitter. A kill condition must not be able to fire on jitter. The replacement is built from already-locked bars (the ≤ 2.0× latency bar) plus a new battery-validity requirement. The slope ratio is **RETAINED as a reported diagnostic ONLY, never a trigger** (resolves NB-1). The mandated timing methodology resolves NB-6.

The collapse criterion has FOUR components:

**1. Candidate side (kill (d) trigger — the locked bar, UNCHANGED in value):** the candidate's 10×-history latency growth on the state-dependent battery must be ≤ 2.0×:
```
candidate_latency_growth_10x = latency(history=1000) / latency(history=100)
bar: candidate_latency_growth_10x ≤ 2.0
```
This is the SAME locked bar as d1 (10× history ≤ 2× 1× history), now applied to the state-dependent battery (where the fair-naive is also measured). The bar value is UNCHANGED — it is carried forward from M0.

**2. Battery-validity requirement (NEW — NOT a candidate kill):** the fair-naive on the SAME battery must show 10×-history latency growth ≥ 4.0×:
```
fair_naive_latency_growth_10x = fair_naive_latency(history=1000) / fair_naive_latency(history=100)
bar: fair_naive_latency_growth_10x ≥ 4.0
```
If the fair-naive does NOT show ≥ 4.0× growth, the battery is too easy to expose scan cost — an **INSTRUMENT failure**: the run is **unscoreable**, the battery is revised, and **no kill condition or retry budget is touched** (the candidate is neither dead nor exonerated; the battery is fixed and the run repeated). This is routed to the ARCHITECT/CRITIC for battery revision, NOT to kill (d). The 4.0× threshold is pre-registered here per L19; the CRITIC assesses its falsifiability (high enough to confirm the battery exposes scan cost, not so high no honest battery can pass).

**3. Collapse** = the candidate failing bar (1) (growth > 2.0×) on a battery validated by (2) (fair-naive growth ≥ 4.0×). If the battery is valid AND `candidate_latency_growth_10x > 2.0`, the candidate is secretly replaying the log at query time instead of reading maintained state → kill (d) d2 fires. The candidate has collapsed to recompute-by-scan OPERATIONALLY (even though its answers match the oracle). This is the replacement for the old answer-agreement collapse test: the candidate's distinctness from fair-naive is operational (cost scaling), not informational (answer agreement).

**4. Timing methodology (mandated per Rebecca's Q2 ruling item 4; resolves NB-6):** all latency measurements in the state-dependent battery (and in d1) use:
- **(i) Median** over repeated executions per point: minimum 100 repetitions per query per history-size point; the median per-query latency is the reported figure (not the mean — the median is robust to outlier spikes from GC/scheduling jitter).
- **(ii) Warm-up excluded:** the first 10% of repetitions at each point are discarded (JIT compilation, cache warming, allocator stabilization).
- **(iii) Monotonic clock:** `time.monotonic_ns()` or equivalent — NEVER wall-clock `time.time()` (which is subject to NTP adjustments and is the L11 clock the candidate must NOT use for coordinates; the timing instrument uses a different clock than the candidate's coordinate clock).
- **(iv) Dispersion reported alongside every latency figure:** the interquartile range (IQR) or standard deviation per point is reported in the artifact (§7.3.1: `latency_iqr_per_point` for candidate and fair-naive), so the JUDGE and CRITIC can verify the median is stable and the collapse criterion is not firing on jitter.

This methodology ensures the collapse criterion cannot fire on timer jitter (NB-6 resolved): the median over 100+ repetitions with warm-up excluded and a monotonic clock produces stable latency figures; the dispersion figure lets the CRITIC verify the signal-to-noise ratio at each point. If the dispersion is large relative to the median (e.g., IQR > 50% of median), the CRITIC flags the timing as inconclusive and the run is repeated with more repetitions — this is an instrument-quality check, not a candidate kill.

> **NB-6 resolved:** the timing-precision robustness concern (fitted slopes near the timing noise floor; a near-zero denominator ratio firing on jitter) is resolved by (a) replacing the slope-ratio trigger with the locked latency bar (≤ 2.0× growth), which uses a ratio of two medians at well-separated history sizes (100 vs 1000) rather than a fitted slope, and (b) the mandated timing methodology (median, warm-up excluded, monotonic clock, dispersion reported). The collapse criterion can no longer fire on timer jitter.

> **NB-1 resolved:** the 0.5 slope-ratio threshold was a NEW kill-condition trigger not acknowledged as a new bar in the scope fence. It is now RETIRED as a trigger (RETAINED as a diagnostic). The new trigger (candidate_latency_growth_10x ≤ 2.0×) uses the ALREADY-LOCKED latency bar value (≤ 2.0) — it is not a new bar. The new battery-validity threshold (≥ 4.0×) is a NEW instrument check (not a kill); it is pre-registered here per L19 and the CRITIC assesses its falsifiability.

**The slope ratio (RETAINED as a reported diagnostic ONLY):** the linear regression of per-query latency on history size is still fitted for both arms:
```
candidate_latency(h) = candidate_slope * h + candidate_intercept
fair_naive_latency(h) = fair_naive_slope * h + fair_naive_intercept
```
where `h` is the history size (100, 250, 500, 750, 1000) and latency is the median per-query latency at that history size. The ratio `scaling_collapse_ratio = candidate_slope / fair_naive_slope` is REPORTED (§4.2, §7.3.1) for diagnostic transparency — it lets the JUDGE and CRITIC inspect the scaling shape — but it carries NO kill and is NEVER a trigger. A correct candidate has `scaling_collapse_ratio ≈ 0` (flat); a scanning candidate has `scaling_collapse_ratio ≈ 1.0`. These are consistent with the latency-growth criterion (a correct candidate has growth ≈ 1.0×; a scanning candidate has growth ≈ 10×), but the growth ratio (not the slope ratio) is the trigger, because it is robust to the noise-floor fragility.

**Why this is satisfiable (and why it is a genuine discriminator):**
- The candidate's `query_membership` is O(1) (a single comparison of two integers, read from maintained state). The candidate's `query_landmark_relative_bounded` is O(log n) or O(1) (a lookup over the indexed coordinate). Neither scales with history size. So `candidate_latency_growth_10x ≈ 1.0` (flat).
- The fair-naive's per-query cost is O(n) (it scans the full log, including designation events, to recompute the coordinate for each entry). So `fair_naive_latency_growth_10x ≈ 10.0` (linear, 10× growth from 100 to 1000 entries).
- `candidate_latency_growth_10x ≈ 1.0 ≤ 2.0` on a battery where `fair_naive_latency_growth_10x ≈ 10.0 ≥ 4.0` → PASS. The candidate is operationally distinct.
- A candidate that secretly replays (scans the log at query time instead of reading maintained state) would have `candidate_latency_growth_10x ≈ 10.0 > 2.0` on a validated battery → FAIL (collapse). This catches the operational collapse that the old answer-agreement test could not (because answers are identical whether the candidate scans or reads maintained state).

**Scoring is arithmetic:** the JUDGE reads `candidate_latency_growth_10x` and `fair_naive_latency_growth_10x` (floats) from `e1_run_results.json` (§7.3.1), checks the battery is valid (`fair_naive_latency_growth_10x ≥ 4.0`), then applies the bar (`candidate_latency_growth_10x > 2.0` on a valid battery → kill (d) d2 fires). If the battery is invalid, the run is unscoreable (instrument failure — no kill). The JUDGE verifies the arithmetic from the per-point latency arrays (which ship in the artifact, with dispersion). No judgment calls.

### 6.iii Property (iii) — Load-bearing coupling (E1-scale integration check, NEW — a miniature of the L15 test)

**The downstream consumer:**

A MINIMAL downstream consumer — a toy recency-weighted retrieval implementing L1's access physics over the index's coordinates. It is NOT the full L1 system (L1 is M3); it is a test instrument that consumes the candidate's coordinates and produces a measurable output, so that ablation of the candidate's re-resolution produces a measurable degradation.

**Specification (FULLY SPECIFIED per Rebecca's Q3 attachment 1 — NB-3 promoted to required-before-build; the TASK BUILDER receives a complete specification, no "e.g.", no unspecified query items):**

- **The payload feature vector (exact — BUCKETED content signal):** each entry's `payload` carries a synthetic feature vector `v(e) ∈ ℝ^d` with `d = 32` dimensions. The 1000 entries are partitioned into **content buckets**: each entry belongs to exactly one bucket, and every entry in a bucket shares a (near-)common feature direction, so entries in the same bucket are **content near-duplicates** of one another while entries in different buckets are near-orthogonal. The buckets come in two classes:
  - **30 content-unique (CU) buckets, each of size EXACTLY `k = 10`** (300 entries). These supply the content-unique query battery.
  - **20 recency-discriminative (RD) buckets, each of size `K_rd = 30 > k`** (600 entries). These supply the recency-discriminative query battery.
  - The remaining 100 entries are **fillers** (no bucket assignment) — they carry noise-only feature vectors and never enter any query's top-k.
  Each bucket `b` (indexed `0..49`; RD buckets `0..19`, CU buckets `20..49`) is assigned a **seeded random unit direction** `u_b ∈ ℝ^d`: `u_b = rng_dir_b.standard_normal(d)` then normalized to unit length, where `rng_dir_b = numpy.random.default_rng(seed * 9_000_000 + b)`. (Random unit directions in `d=32` are near-orthogonal — `dot(u_b, u_b') ~ O(1/√d) ≈ 0.18` for `b ≠ b'` — so different buckets are content-separable WITHOUT requiring one reserved dimension per bucket.)
  The **member cycles of each bucket are SPREAD across the full timeline** `0..999` (so recency differs within a bucket): cycles are assigned to bucket members by a seeded permutation of `0..999`, round-robined across buckets (member 0 of every bucket, then member 1 of every bucket that still needs members, …; CU buckets fill to size 10 and drop out, RD buckets continue to size 30). The permutation is `rng_perm = numpy.random.default_rng(seed * 7_000_000 + 1)`. This guarantees every bucket's members sit at cycles spread across `0..999` → different `coord_cycle_relative` → different recency weights within the bucket.
  The feature vector for entry `e` in bucket `b` is `v(e) = A · u_b + σ_f · rng_e.standard_normal(d)`, where `A = 10.0` (the content signal amplitude), `σ_f = 0.10` (feature noise — small, so within-bucket content is a tight cluster around `A² = 100`), and `rng_e = numpy.random.default_rng(seed * 100_000 + e.cycle)`. Fillers (no bucket) get `v(e) = σ_f · rng_e.standard_normal(d)` (noise only, content `~O(σ_f²·d) ≈ 3.2`). The content-similarity gap is therefore large and clean: a query targeting bucket `b` yields `dot(v(e_b), q) ≈ A² = 100` for bucket members vs `dot(v(e_b'), q) ≈ A · dot(u_b', u_b) ≈ O(1.8)` for other-bucket entries and `~O(1.4)` for fillers — a ~50× content gap that the bounded additive recency term (below) cannot overturn. The feature vector is part of the opaque payload blob (§1.2.1) — stored at append time, never changes.

- **The content-similarity function (exact formula):** dot product on the synthetic feature vectors (NOT cosine similarity — dot product, which preserves magnitude and is simpler to verify):
```
content_similarity(e, q_item) = dot(v(e), q_item)
```
where `v(e)` is the entry's 32-d feature vector and `q_item` is the query item's 32-d feature vector. This is a deterministic, exact function — no approximations, no learned components. The dot product is unnormalized (magnitude varies), which is intentional: it means entries with larger-magnitude feature vectors are more retrievable, adding structure beyond pure recency.

- **The query set (exact — how many, what they ask for, how they're generated per seed):** `N_consumer_queries = 50` query items per seed. Each query item asks: "retrieve the top-k=10 entries by recency-weighted relevance." Each query targets ONE content bucket: the query's feature vector aligns with that bucket's shared direction `u_b`, so the bucket's members are the content-similar entries. The 50 queries are split into TWO classes:
  - **Recency-discriminative queries (20 of 50 = 40% — `j ∈ {0..19}`):** query `j` targets RD bucket `b = j` (size `K_rd = 30 > k`). The query is `q_j = A · u_b + σ_q · rng_qd_j.standard_normal(d)` where `σ_q = 0.10` and `rng_qd_j = numpy.random.default_rng(seed * 10_000_000 + 500 + j)`. All 30 bucket members are content-tied (`dot ≈ A² = 100`), but they sit at cycles spread across `0..999` (different ages). Content similarity alone TIES the 30 members; the recency weight must SELECT which `k = 10` of the 30 to retrieve — this is the recency-discriminative condition (see battery below).
  - **Content-unique queries (30 of 50 = 60% — `j ∈ {20..49}`):** query `j` targets CU bucket `b = j` (size EXACTLY `k = 10`). The query is `q_j = A · u_b + σ_q · rng_q.standard_normal(d)` where `rng_q = numpy.random.default_rng(seed * 1_000_000 + 1000 + j)`. The bucket has exactly `k = 10` members, all content-tied — so content alone DETERMINES the top-k SET (the bucket IS the top-k); recency only reorders WITHIN the set and cannot change which entries are retrieved. This is the content-unique condition.
  This split ensures the consumer exercises both the content axis and the coordinate axis: on CU queries content determines the retrieval SET (frozen matches oracle); on RD queries content ties and recency selects the subset (frozen fails to match oracle).

- **How the consumer uses the index's coordinates (exact — ADDITIVE relevance):** the consumer uses `coord_cycle_relative(e) = now - e.cycle` (the candidate's re-resolved offset coordinate, C1.1) as the recency weight in an ADDITIVE relevance function:
```
relevance(e, q_item) = dot(v(e), q_item)  +  λ · exp(-coord_cycle_relative(e) / τ)
```
where `τ = 50` cycles (a constant, pinned per Q3-1, UNCHANGED) and `λ = 16.0` (the recency-coupling constant — the additive recency bonus is bounded in `[0, λ]`, i.e. at most 16% of the within-bucket content signal `A² = 100`). The consumer retrieves the top-k=10 entries (highest `relevance`) for each query item. **Why additive, not the prior multiplicative form `exp(-coord/τ)·dot`:** the multiplicative product couples the recency weight's dynamic range to the content signal's magnitude. With `τ=50` and cycles `0..999`, `exp(-coord/τ)` spans ~9 orders of magnitude (`exp(-999/50) ≈ 2×10⁻⁹` to `1.0`), which the CRITIC's simulation showed overwhelms the content signal on EVERY query (not just recency-discriminative ones) — the frozen arm (content-only) then fails on content-unique queries too (CU degradation ≈ 0.93, aggregate ≈ 0.89, near the 1.0 ceiling corner). The additive form DECOUPLES content from recency: the recency contribution is a bounded bonus `λ·w(e) ∈ [0, λ]` added to the content score, so a large content gap (the ~50× bucket gap) cannot be overturned by recency, while a content TIE (within a bucket) is still broken by the recency bonus. This realizes the spec's intended separation (CU → content dominates; RD → recency breaks tie) that the multiplicative form could not. The frozen arm is unchanged in substance: under Option E `coord_cycle_relative = 0` for all entries → `w(e) = exp(0) = 1.0` for all → the recency bonus collapses to the constant `λ` added to every entry → the frozen arm ranks purely by content (the constant `λ` does not affect ranking). **The consumer exercises `coord_cycle_relative` ONLY** (NB-4 accepted for E1 scope — see standing note below). The consumer does NOT use `coord_landmark_relative` (the designation tracking, C1.4) — that coupling belongs to the L15 matrix at M5.

- **How degradation is measured under frozen-origin ablation (exact):** the consumer is run over TWO indices:
  1. **Candidate's re-resolved index:** `coord_cycle_relative(e) = now - e.cycle` (re-resolved as `now` advances). The consumer's recall@k is `quality_candidate`.
  2. **Frozen-origin index (§3 arm 1, the ablation — Option E per Rebecca's ruling §Q1):** the frozen arm retains ALL entries and ALL content (identical to the candidate's autobiography — all 1000 entries). Each entry's `coord_cycle_relative` is computed ONCE, at its own append: `coord_cycle_relative(e) = now_at_birth − e.cycle = e.cycle − e.cycle = 0`. This coordinate is NEVER re-resolved thereafter (re-resolution is disabled; nothing else is). Consequently, `coord_cycle_relative(e) = 0` for ALL entries, regardless of age. The recency weight collapses to `exp(−0 / τ) = exp(0) = 1.0` for every entry — the recency gradient is destroyed while memory remains complete. This is the honest meaning of a frozen origin: content intact, temporal self-location gone. The consumer's recall@k is `quality_frozen`.
  - **Ground truth:** the oracle's top-k (computed using the oracle's `coord_cycle_relative = now - e.cycle`, the ground-truth recency). Retrieval quality is **recall@k**: `recall@k = |consumer_top_k ∩ oracle_top_k| / k`.
  - **Degradation:** `degradation = quality_candidate - quality_frozen` (positive = candidate better than frozen = re-resolution is load-bearing).

- **Why this consumes the candidate's coordinates:** the consumer's retrieval depends on `coord_cycle_relative(e)`, which the candidate re-resolves as `now` advances. If the candidate's re-resolution is correct (property (i)), the consumer's `coord_cycle_relative` matches the oracle's, and recall@k is high. If the candidate's re-resolution is ablated (frozen-origin arm, Option E), the consumer's `coord_cycle_relative` is `0` for every entry (computed once at birth, never re-resolved), so the recency weight collapses to `1.0` for all entries — the recency gradient is destroyed. On queries where content similarity alone ties or near-ties between entries of different ages (§6.iii recency-discriminative battery), the frozen arm cannot break the tie by recency, and recall@k degrades — the consumer retrieves entries by content alone, losing the temporal ordering that the re-resolved coordinate provides.

**The ablation (frozen-origin arm — Option E):**

The downstream consumer is run over TWO indices:
1. **Candidate's re-resolved index** (the live candidate): `coord_cycle_relative(e)` is re-resolved as `now` advances (`coord_cycle_relative(e) = now - e.cycle`). The consumer's recall@k is `quality_candidate`.
2. **Frozen-origin index** (§3 arm 1, the ablation — Option E): the frozen arm retains ALL entries and ALL content. Each entry's `coord_cycle_relative` is computed once at birth (`= 0`) and NEVER re-resolved. The recency weight `exp(−coord_cycle_relative/τ)` collapses to `1.0` for all entries — the recency gradient is destroyed while memory remains complete (content intact, temporal self-location gone). The consumer's recall@k is `quality_frozen`.

**The degradation metric:**
```
degradation = quality_candidate - quality_frozen
```
- **Positive degradation:** the candidate's re-resolved index produces BETTER retrieval than the frozen-origin index. Re-resolution is load-bearing — the consumer measurably benefits from the candidate's re-resolution. This is property (iii) passing.
- **Zero or negative degradation:** the frozen-origin index produces retrieval as good as or better than the candidate's. Re-resolution is decorative — the consumer does not benefit from it. This is property (iii) failing. *"A candidate whose coordinates are consumed by nothing is a cache with a philosophy."*

**The consistency requirement:**
- `degradation > 0` on ALL 3 seeds (effect direction consistent across seeds). If degradation ≤ 0 on any seed, the effect direction is inconsistent → property (iii) fails.
- `mean_degradation ≥ floor` across the 3 seeds. The floor is pre-registered at **0.05** (a conservative E1-scale miniature floor; Rebecca's L15 floor of d ≥ 0.5 applies at M5 in full, not at E1's miniature). The floor is pre-registered here per L19; the CRITIC assesses whether it is falsifiable (non-trivially above zero, not so high no honest candidate can pass).

**Report the observed degradation magnitude (Q3 attachment 2 — "the floor is a floor, not a finding"):** the spec REQUIRES reporting the observed degradation magnitude, not merely whether it clears the 0.05 floor. The artifact (§7.3.1) ships `downstream_degradation_per_seed` (3 floats), `downstream_degradation_mean` (1 float), `downstream_quality_candidate_per_seed` (3 floats), and `downstream_quality_frozen_per_seed` (3 floats). The JUDGE and CRITIC inspect the ACTUAL magnitude (e.g., "degradation = 0.34"), not just the boolean ("≥ 0.05 → pass"). **The floor is a floor, not a finding.** A degradation of 0.06 (barely clearing) and a degradation of 0.80 (overwhelming) are both "pass" on the floor, but they are materially different findings about how load-bearing the re-resolution is. The magnitude is reported so the finding is honest. A degradation that barely clears the floor on all 3 seeds is a weaker finding than one that clears it by a wide margin — the CRITIC notes this at review, and it feeds the L19 base-rate interpretation (§11.2).

**Why this is satisfiable (and why it is a genuine integration check — Option E):**
- The candidate's re-resolved `coord_cycle_relative(e) = now - e.cycle` gives the correct recency for every entry at the current `now`. The consumer's recency weights are correct → recall@k is high (close to 1.0, since the consumer uses the same coordinates as the oracle).
- The frozen-origin index's `coord_cycle_relative(e) = 0` for ALL entries (Option E: computed once at birth, never re-resolved). The recency weight `w(e) = exp(−0/τ) = 1.0` for every entry, so the additive recency bonus collapses to the constant `λ` for every entry — it does not affect ranking, so the frozen arm ranks purely by content. On content-unique queries (CU buckets of size exactly `k`), content alone determines the top-k SET (the bucket IS the top-k), so the frozen arm's content ranking matches the oracle's recency-weighted ranking → recall@k stays at ~1.0. On recency-discriminative queries (RD buckets of size `K_rd = 30 > k`), content ties all 30 members and the recency bonus `λ·w(e)` must SELECT which `k` of the 30 to retrieve; the oracle (correct recency) retrieves the `k` most-recent members, while the frozen arm (constant recency bonus → ranks by content-noise) retrieves a content-noise-driven subset → the sets differ → recall@k degrades. This is why the recency-discriminative fraction is essential: a battery of content-unique queries would read degradation ≈ 0 for reasons having nothing to do with the mechanism.
- `degradation = quality_candidate - quality_frozen > 0` → re-resolution is load-bearing. The candidate's coordinates are consumed by a downstream consumer that measurably benefits from them.
- This is a miniature of the L15 test (which M5 will apply in full): ablate A (re-resolution), measure degradation of B (the consumer's law-compliance — here, retrieval quality). The glial/DG system FAILS L15 (either side removable without effect); a passing E1 must be unlike it.

**The recency-discriminative query battery (Rebecca's companion requirement — ruling §Q1):**

Coupling is only measurable on a task where the coordinate carries information. A battery of content-unique queries would read degradation ≈ 0 for reasons having nothing to do with the mechanism — on content-unique queries, content similarity alone determines the retrieval SET, so the frozen arm (recency bonus collapsed to a constant) matches the oracle regardless of whether re-resolution works. The query set must therefore include a pre-registered fraction of content-tied queries at different ages, where content similarity alone ties and the coordinate breaks the tie.

**The ARCHITECT states the fraction: 40% (20 of 50 queries).** This fraction is pre-registered here.

**How the content ties are generated (exact):** 20 RD content buckets among the 1000 entries each contain `K_rd = 30` entries with near-identical feature vectors (all aligned to the bucket's shared direction `u_b`, content `dot ≈ A² = 100`) but at cycles SPREAD across `0..999` (different ages) — specified in the feature vector section above. Each recency-discriminative query `j` (targeting RD bucket `b = j`) aligns with that bucket's shared direction: `q_j = A · u_b + σ_q · noise`. This guarantees all 30 bucket members are content-tied (`dot ≈ 100`), while their cycles span the timeline (different recency weights) — the recency-discriminative condition (content ties, recency selects).

**How the coordinate breaks the tie (exact):**
- **Candidate / oracle (re-resolved coordinate):** `coord_cycle_relative(e) = now − e.cycle = 999 − e.cycle`. The recency bonus `λ·exp(−(999 − e.cycle)/τ)` with `λ=16`, `τ=50` differs across the 30 bucket members (which span cycles `0..999`): a recent member (e.g., cycle 990, coord 9) gets a bonus `λ·exp(−9/50) ≈ 16·0.835 ≈ 13.4`; an old member (e.g., cycle 10, coord 989) gets a bonus `λ·exp(−989/50) ≈ 16·2.7×10⁻⁹ ≈ 4×10⁻⁸ ≈ 0`. The re-resolved coordinate therefore ranks the 30 tied members by recency and the oracle retrieves the `k = 10` MOST RECENT members of the bucket (those with the largest recency bonus). The content gap (~50×) guarantees no entry from another bucket can intrude, so the oracle's top-k is a subset of the bucket.
- **Frozen arm (Option E — coordinate computed once at birth, never re-resolved):** `coord_cycle_relative(e) = 0` for ALL entries → `w(e) = exp(0) = 1.0` for all → the recency bonus collapses to the constant `λ = 16` added to every entry. The frozen arm therefore ranks purely by content: `relevance_frozen(e, q) = dot(v(e), q) + λ`. Since all 30 bucket members are content-tied (`dot ≈ 100 ± O(1.4)` noise), the frozen arm's ranking among them is driven by the small feature noise `σ_f = 0.10` — i.e. it retrieves a content-NOISE-driven subset of the bucket, NOT the recency-selected subset. The two subsets (oracle: 10 most-recent; frozen: 10 highest-content-noise) differ by the `K_rd − k = 20` members that the oracle's recency excludes but the frozen arm's noise may include → recall@k degrades on these queries.

**Why this makes the 0.05 floor meaningfully clearable (CRITIC verification (b)):**
- On the 20 recency-discriminative queries (40%), the frozen arm systematically retrieves a different subset of the content-tied bucket than the oracle (it cannot select by recency — the recency bonus is a constant). Each RD query contributes `degradation = 1 − recall@k` where `recall@k = |frozen_top_k ∩ oracle_top_k| / k`. With `K_rd = 30` tied members, the oracle's recency-selected 10 and the frozen's noise-driven 10 overlap by roughly `k²/K_rd = 100/30 ≈ 3.3` entries in expectation → `recall ≈ 0.33` → per-query degradation ≈ 0.67 in the recency-dominated limit; the observed value (additive `λ=16`, content-noise `σ_f=0.10`) is ≈ 0.25 per query (simulated: see §6.iii verification below). Aggregate degradation from RD queries alone ≈ `0.40 × 0.25 = 0.10` — comfortably above the 0.05 floor, driven by the recency-selection mechanism (not by content-unique failure).
- The floor is clearable by a working mechanism (re-resolution that correctly tracks recency). A broken mechanism (no re-resolution) collapses the recency bonus to a constant and degrades ONLY on RD queries (content-unique queries still pass) — the recency-discriminative fraction is what makes the test non-degenerate.

**Why degradation < 1.0 is reachable (CRITIC verification (a)):**
- On the 30 content-unique queries (60%), content similarity alone determines the retrieval SET: each CU query targets a bucket of EXACTLY `k = 10` content-tied entries, and the ~50× content gap to all other entries means the top-k SET is the bucket, regardless of the recency bonus (the bounded additive bonus `λ ∈ [0,16]` cannot overturn a 100-vs-~1.8 content gap). The frozen arm (recency bonus collapsed to the constant `λ`, ranking by content) retrieves the bucket; the oracle (recency-weighted) ALSO retrieves the bucket (recency only reorders WITHIN the set) → `quality_frozen ≈ quality_candidate ≈ 1.0` on these queries → CU degradation ≈ 0.
- The maximum possible degradation is bounded by the recency-discriminative fraction: `degradation ≤ fraction_recency_discriminative × 1.0 = 0.4 < 1.0` (since `quality_frozen ≥ 0` on all queries and `quality_frozen ≈ 1.0` on content-unique queries). Content-only ranking MUST still succeed on content-unique queries — if it does not, the battery is broken (the content signal is too weak), which is an instrument failure, not a candidate property.
- The CRITIC verifies: (a) `degradation < 1.0` is reachable (content-only ranking succeeds on content-unique queries → `quality_frozen > 0`), and (b) the recency-discriminative fraction (40%) makes the 0.05 floor meaningfully clearable by a working mechanism.

**SIMULATED VERIFICATION (ARCHITECT, pre-CRITIC — script `verify_option_e_fix.py`, seeds 42/43/44):** the revised consumer parameterization was simulated before this amendment returns to the CRITIC. The simulation implements the exact formulas above (bucketed spike features, additive relevance `dot + λ·exp(-coord/τ)`, Option E frozen arm `coord=0`). Results (mean over 3 seeds):

| Metric | CRITIC's finding (old multiplicative spec) | Revised parameterization (additive + bucketed) |
|---|---|---|
| CU degradation (30 queries) | **0.927** (frozen fails on CU — battery broken) | **0.000** (content dominates → frozen matches oracle) |
| RD degradation (20 queries) | 0.827 (recency-dominated on ALL queries) | **0.255** (recency selects the recent subset) |
| Aggregate degradation (50 queries) | **0.887** (near the 1.0 ceiling corner) | **0.102** (comfortably in (0.05, 0.5)) |
| Per-seed aggregate | 0.878 / 0.894 / 0.888 | 0.120 / 0.094 / 0.092 (all > 0.05 floor) |
| Bound on degradation | spec claimed ≤ 0.4; actual ~0.89 | bound ≤ 0.4 holds (actual 0.102 ≪ 0.4) |

Mechanism check (seed 42, RD query 0): the oracle's top-10 cycles are the recency-selected recent subset `[17,89,116,311,462,727,783,810,915,989]`; the frozen arm's top-10 cycles are the content-noise-driven scattered subset `[17,89,116,215,311,462,600,727,783,810]`; overlap 0.80, degradation 0.20 — recency genuinely selects a different subset. (seed 42, CU query 0): oracle top-10 == frozen top-10 == the CU bucket exactly → recall 1.00, degradation 0.00 — content alone determines the retrieval set.

**This is NOT a corner:** aggregate 0.102 is ~2.0× the 0.05 floor and ~4.9× below the 0.5 midpoint-to-ceiling, comfortably inside the open interval (0, 1). It is not 0 by construction (the frozen arm's collapsed recency bonus genuinely fails to select the recent subset on RD queries — verified: RD degradation 0.255 > 0 on all 3 seeds). It is not 1.0 by construction (content-only ranking genuinely succeeds on CU queries — verified: CU degradation 0.000, so the aggregate is bounded away from 1.0 by the 60% CU fraction). The value is task-dependent (driven by how many of the 30 tied RD members the frozen arm's content-noise selection happens to overlap with the oracle's recency selection) and varies by seed (0.092–0.120), not a constant. The CRITIC is directed to re-verify with its own simulation of these exact formulas.

**Rebecca's verbatim lesson (logged per ruling §Q1 — this section has now produced two degenerate ablations):**

> *"An ablation whose result is a constant by construction measures nothing. A valid ablation removes exactly the organization under test and preserves everything else, and its expected result must be a task-dependent quantity in the open interval — never a corner."*

The prior frozen-origin specification (Option D — excluding entries 100–999) produced degradation = 1.0 by construction (a ceiling corner). The prior §6.iii consumer spec (frozen `coord_cycle_relative = 99 − e.cycle` for all entries) produced degradation = 0.0 by construction (a floor corner — the frozen relevance was a constant multiple of the oracle relevance, so rankings were identical). The CRITIC's simulation of the FIRST Option E parameterization (multiplicative `exp(-coord/τ)·dot` with random Gaussian features, τ=50) found degradation ≈ 0.89 — not a corner by construction, but uncomfortably close to the ceiling, and for the WRONG reason (the recency gradient overwhelmed the content signal on ALL queries, so the frozen arm failed on content-unique queries too — Verification (a) failed). This revision (additive relevance `dot + λ·exp(-coord/τ)` with bucketed spike content) removes exactly the organization under test (re-resolution — the frozen arm's recency bonus collapses to a constant `λ`) and preserves everything else (all entries, all content, the same consumer), and its SIMULATED result is a task-dependent quantity 0.102 in the open interval (0, 1), comfortably away from both corners, driven by how much work the recency selection actually does on the recency-discriminative battery (and ONLY on that battery — content-unique queries pass).

**Scoring is arithmetic:** the JUDGE reads `quality_candidate`, `quality_frozen`, and `degradation` (floats per seed) from `e1_run_results.json` (§7.3.1), checks `degradation > 0` on all 3 seeds and `mean_degradation ≥ 0.05`, inspects the observed magnitude (Q3 attachment 2), and verifies the arithmetic from the per-seed degradation array (which ships in the artifact). No judgment calls.

> **NB-4 standing note (accepted for E1 scope; M5 note logged):** the downstream consumer exercises `coord_cycle_relative` (the offset counter, C1.1) ONLY — not `coord_landmark_relative` (the designation tracking, C1.4). The consumer tests whether the offset counter's re-resolution is load-bearing. It does NOT directly test whether the landmark-relative re-resolution (the deferred-designation mechanism, C1.4 — the novel part of Candidate 1.1) is load-bearing. This is accepted for E1 scope: (a) Rebecca's ruling (§2(iii)) says "over the index's coordinates" — the consumer uses one of the index's coordinates, which is a valid reading; (b) the consumer is a "toy" — the full L15 test at M5 would test all couplings; (c) `coord_landmark_relative` is tested by property (i) (correctness — the candidate must match the oracle on deferred-designation queries) and property (ii) (the state-dependent battery's material comes from deferred designations). **Full landmark-relative coupling belongs to the L15 matrix at M5.** A more complete consumer at M5 would use both coordinates.

### 6.iv The three-property verdict (what the JUDGE assembles)

The JUDGE assembles the E1 verdict from the three properties:

| Property | Metric | Bar | Kill | Verdict contribution |
|---|---|---|---|---|
| (i) Correctness | `oracle_agreement` | = 1.0 | (f) | Must pass. < 1.0 → kill (f) → candidate dead. |
| (ii) Operational distinctness | `latency_ratio` AND `state_dependent_collapse` | ≤ 2.0 (d1) AND candidate_latency_growth_10x ≤ 2.0 on a battery where fair_naive_latency_growth_10x ≥ 4.0 (d2) | (d) | Must pass. Either fails → kill (d) → candidate dead. (If battery invalid → instrument failure, run unscoreable.) |
| (iii) Load-bearing coupling | `downstream_degradation` | > 0 on all seeds AND mean ≥ 0.05 | (property (iii) failure routing, §5) | Must pass. Fails → E1 not green (candidate not dead, but has not earned its place; program pauses for Rebecca). |
| structural (L2) | `chain_integrity` | = 1.0 | (b) | Must pass. < 1.0 → kill (b) → candidate dead (unless construction break → BUILDER fix). |
| structural (L4 re-resolution) | `coordinate_shift` | = 1.0 | (c) | Must pass. < 1.0 → kill (c) → candidate dead (unless wiring defect → BUILDER fix). |
| structural (L11) | `wall_clock_shift_detected` | = False | (e) | Must pass. True → kill (e) → candidate dead (unless implementation bug → BUILDER fix). |

**E1 passes (green) iff:** properties (i), (ii), (iii) all pass AND no kill condition fires (b, c, d, e, f all false) AND I3 contamination trustworthy AND L20 self-test passes AND reproducibility passes (§10.3). The moving origin earns its place.

**E1 fails (red) iff:** any kill condition (b, c, d, e, f) fires. The candidate is dead (D1). The program routes to the D2 retry decision (§9 step 12).

**E1 not-green (candidate alive but place not earned) iff:** property (iii) fails AND no kill condition fires. The candidate is not dead, but the moving origin has not earned its place. The program pauses for Rebecca's decision (§5 property (iii) failure routing).

---

## 7. Courier packet

This is the exact packet the INTEGRATOR ships to Rebecca via the courier channel. Nothing executes that is not committed. The INTEGRATOR packages this as a merge-candidate courier run (per BUILD_PHASE_ORG Ruling 2: per merge-candidate, batched).

**Execution channel split (Ruling O-15):** this is a **scoring run** — it feeds the kill conditions and the L2/L4 bars, so it goes exclusively through Rebecca's supervised-executor courier channel.

### 7.1 One launch command

```bash
python e1_experiment.py --seeds 42,43,44 --output-dir ./e1_output
```

### 7.2 Pinned dependencies (`requirements.txt`)

```
python==3.11
numpy==1.26.4
scipy==1.13.1
```
(No other third-party packages. Standard library otherwise — `hashlib` for SHA-256 is stdlib. The BUILDER pins exact versions; Rebecca installs into a clean venv. Same pinned deps as M1 for cross-run consistency.)

### 7.3 Expected output schema (what Rebecca receives back)

The experiment produces **5 files** in the output directory. These are the ground-truth artifacts the JUDGE scores from; Rebecca returns them raw and uncurated.

#### 7.3.1 `e1_run_results.json` — full results table

```json
{
  "run_id": "e1-<ISO8601 timestamp>",
  "schema_version": "3.0",
  "config": {
    "n_cycles": 10,
    "n_entries_initial": 100,
    "n_entries_final": 1000,
    "n_landmarks": 10,
    "n_landmarks_immediate": 8,
    "n_landmarks_deferred": 2,
    "n_queries": 200,
    "n_state_dependent_query_points": 5,
    "state_dependent_history_sizes": [100, 250, 500, 750, 1000],
    "n_consumer_queries": 50,
    "consumer_feature_dim": 32,
    "consumer_tau": 50,
    "consumer_k": 10,
    "consumer_relevance_form": "additive (dot + lambda * exp(-coord/tau))",
    "consumer_recency_coupling_lambda": 16.0,
    "consumer_content_signal_amplitude": 10.0,
    "consumer_feature_noise_sigma": 0.10,
    "consumer_query_noise_sigma": 0.10,
    "n_recency_discriminative_queries": 20,
    "recency_discriminative_fraction": 0.4,
    "n_rd_content_buckets": 20,
    "rd_content_bucket_size": 30,
    "n_content_unique_queries": 30,
    "n_cu_content_buckets": 30,
    "cu_content_bucket_size": 10,
    "n_content_buckets_total": 50,
    "near_duplicate_sigma": 0.10,
    "recency_discriminative_query_sigma": 0.10,
    "consumer_relevance_note": "additive form decouples content from recency; tau=50 unchanged (pinned Q3-1); the multiplicative form was replaced because its 9-orders-of-magnitude recency gradient overwhelmed the content signal on all queries (CRITIC BLOCKING ISSUE 1)",
    "timing_repetitions": 100,
    "timing_methodology": "median, warm-up excluded, monotonic clock, IQR reported",
    "seeds": [42, 43, 44],
    "control_arms": ["frozen_origin", "shuffled_cadence", "oracle_index", "fair_naive", "empty", "wall_clock_injection"],
    "candidate": "candidate_1_1"
  },
  "results": {
    "42": {
      "candidate": {
        "oracle_agreement": <f>,
        "equivalence_agreement_vs_fair_naive": <f>,
        "latency_1x_seconds_membership": <f>,
        "latency_10x_seconds_membership": <f>,
        "latency_ratio_membership": <f>,
        "latency_1x_seconds_bounded_k": <f>,
        "latency_10x_seconds_bounded_k": <f>,
        "latency_ratio_bounded_k": <f>,
        "raw_answer_size_1x": <f>,
        "raw_answer_size_10x": <f>,
        "raw_answer_size_ratio": <f>,
        "candidate_scaling_curve": [<5 floats: median per-query latency at history sizes 100, 250, 500, 750, 1000>],
        "candidate_latency_iqr_per_point": [<5 floats: IQR of per-query latency at each history-size point>],
        "candidate_slope": <f>,
        "candidate_intercept": <f>,
        "candidate_latency_growth_10x": <f>,
        "chain_integrity_after_initial_build": <bool>,
        "chain_integrity_after_shift_probe": <bool>,
        "chain_integrity_after_10x_growth": <bool>,
        "chain_integrity_final": <bool>,
        "shift_per_append": [<8 bools>],
        "coordinate_shift": <bool>,
        "wall_clock_shift_detected": <bool>,
        "downstream_quality_candidate": <f>,
        "downstream_quality_frozen": <f>,
        "downstream_degradation": <f>,
        "downstream_degradation_magnitude_reported": <f>
      },
      "frozen_origin":  {"oracle_agreement": <f>, "downstream_quality_frozen": <f>},
      "shuffled_cadence": {"oracle_agreement": <f>, "chain_integrity": <bool>},
      "oracle_index":   {"oracle_agreement": 1.0},
      "fair_naive": {
        "oracle_agreement": <f>,
        "equivalence_agreement_vs_candidate": <f>,
        "fair_naive_scaling_curve": [<5 floats: median per-query latency at history sizes 100, 250, 500, 750, 1000>],
        "fair_naive_latency_iqr_per_point": [<5 floats: IQR of per-query latency at each history-size point>],
        "fair_naive_slope": <f>,
        "fair_naive_intercept": <f>,
        "fair_naive_latency_growth_10x": <f>
      },
      "empty":          {"oracle_agreement": 0.0},
      "wall_clock_injection": {"shift_vs_candidate": <bool>}
    },
    "43": { "...": "..." },
    "44": { "...": "..." }
  },
  "mean_over_seeds": {
    "candidate": {
      "oracle_agreement": <f>,
      "equivalence_agreement_vs_fair_naive": <f>,
      "latency_ratio_membership": <f>,
      "latency_ratio_bounded_k": <f>,
      "raw_answer_size_1x": <f>,
      "raw_answer_size_10x": <f>,
      "raw_answer_size_ratio": <f>,
      "candidate_slope": <f>,
      "fair_naive_slope": <f>,
      "scaling_collapse_ratio": <f>,
      "candidate_latency_growth_10x": <f>,
      "fair_naive_latency_growth_10x": <f>,
      "battery_valid": <bool>,
      "chain_integrity_final": <f>,
      "coordinate_shift": <f>,
      "wall_clock_shift_detected": <f>,
      "downstream_quality_candidate": <f>,
      "downstream_quality_frozen": <f>,
      "downstream_degradation": <f>,
      "downstream_degradation_floor": 0.05,
      "downstream_degradation_consistent": <bool>
    },
    "frozen_origin":  {"oracle_agreement": <f>, "downstream_quality_frozen": <f>},
    "shuffled_cadence": {"oracle_agreement": <f>, "chain_integrity": <f>},
    "oracle_index":   {"oracle_agreement": 1.0},
    "fair_naive": {"oracle_agreement": <f>, "equivalence_agreement_vs_candidate": <f>, "fair_naive_slope": <f>, "fair_naive_latency_growth_10x": <f>},
    "empty":          {"oracle_agreement": 0.0},
    "wall_clock_injection": {"shift_vs_candidate": <f>}
  },
  "property_i_correctness": {
    "oracle_agreement": <f>,
    "bar": 1.0,
    "passes": <bool>,
    "per_query_agreement_vs_oracle": {"42": [<200 bools>], "43": [<200 bools>], "44": [<200 bools>]}
  },
  "property_ii_operational_distinctness": {
    "latency_ratio_membership": <f>,
    "latency_ratio_bounded_k": <f>,
    "latency_bar": 2.0,
    "latency_passes": <bool>,
    "candidate_latency_growth_10x": <f>,
    "fair_naive_latency_growth_10x": <f>,
    "battery_valid": <bool>,
    "battery_validity_bar": 4.0,
    "state_dependent_collapse_bar": 2.0,
    "state_dependent_passes": <bool>,
    "instrument_failure": <bool>,
    "candidate_slope": <f>,
    "fair_naive_slope": <f>,
    "scaling_collapse_ratio": <f>,
    "scaling_collapse_note": "REPORTED diagnostic ONLY (slope ratio); never a trigger per Rebecca Q2 ruling",
    "candidate_scaling_curve_mean": [<5 floats>],
    "fair_naive_scaling_curve_mean": [<5 floats>],
    "candidate_latency_iqr_per_point_mean": [<5 floats>],
    "fair_naive_latency_iqr_per_point_mean": [<5 floats>],
    "timing_methodology": "median over >=100 reps, warm-up excluded, monotonic clock, IQR reported",
    "equivalence_agreement_vs_fair_naive": <f>,
    "equivalence_note": "REPORTED diagnostic; expected ~1.0 (fair-naive == oracle on answers per Rebecca's theorem); carries NO kill and NO distinctness claim"
  },
  "property_iii_load_bearing_coupling": {
    "downstream_degradation_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "downstream_degradation_mean": <f>,
    "downstream_degradation_floor": 0.05,
    "downstream_degradation_magnitude_note": "the floor is a floor, not a finding — observed magnitude reported (Q3 attachment 2)",
    "downstream_degradation_consistent": <bool>,
    "passes": <bool>,
    "downstream_quality_candidate_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "downstream_quality_frozen_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "consumer_spec": "additive relevance: dot(v(e),q) + lambda*exp(-coord_cycle_relative/tau) on 32-d bucketed spike feature vectors, 50 queries/seed (20 recency-discriminative targeting 20 RD content-buckets of size K_rd=30 > k, + 30 content-unique targeting 30 CU content-buckets of size exactly k=10), tau=50 (unchanged, pinned Q3-1), lambda=16.0, A=10.0, sigma_f=sigma_q=0.10, k=10, coord_cycle_relative only (NB-4 accepted for E1); frozen-origin ablation = Option E (coord_cycle_relative=0 at birth for all entries -> recency bonus collapses to constant lambda -> frozen ranks purely by content; never re-resolved); recency-discriminative fraction = 40%; SIMULATED: CU degradation=0.000, RD degradation=0.255, aggregate=0.102 (seeds 42/43/44, all > 0.05 floor), comfortably in (0,1) not a corner"
  },
  "kill_conditions": {
    "(b)_chain_breaks":           {"fires": <bool>, "metric": "chain_integrity_final", "value": <f>, "bar": 1.0, "trigger": "value < 1.0", "construction_break": <bool>, "re_resolution_break": <bool>},
    "(c)_no_shift":               {"fires": <bool>, "metric": "coordinate_shift", "value": <f>, "bar": 1.0, "trigger": "value < 1.0", "wiring_defect": <bool>, "partial_failure": <bool>},
    "(d)_scanning_or_collapse":   {"fires": <bool>, "metric": "latency_ratio AND state_dependent_collapse", "value_latency_membership": <f>, "value_latency_bounded_k": <f>, "value_candidate_latency_growth_10x": <f>, "value_fair_naive_latency_growth_10x": <f>, "value_battery_valid": <bool>, "bar_latency": 2.0, "bar_state_dependent_collapse": 2.0, "bar_battery_validity": 4.0, "trigger": "either latency > 2.0 [d1] OR (battery_valid AND candidate_growth_10x > 2.0) [d2]; if battery invalid -> instrument failure (not a kill)", "instrument_failure": <bool>},
    "(e)_wall_clock_shift":       {"fires": <bool>, "metric": "wall_clock_shift_detected", "value": <f>, "bar": 0.0, "trigger": "value > 0.0"},
    "(f)_incorrect":              {"fires": <bool>, "metric": "oracle_agreement", "value": <f>, "bar": 1.0, "trigger": "value < 1.0", "signed": true},
    "retired": {
      "(a)_collapse_to_naive": {"status": "RETIRED per Rebecca E1 gate ruling", "rationale": "unsatisfiable by construction (fair-naive == oracle on answers; the pair {naive_agreement <= 0.90, oracle_agreement = 1.0} is jointly unsatisfiable)", "metric_reported_as_diagnostic": "equivalence_agreement_vs_fair_naive"}
    },
    "any_fires": <bool>,
    "candidate_dead": <bool>
  },
  "reproducibility": {
    "method": "re-run all 3 seeds a second time within the same process; verify bit-identical results",
    "max_abs_diff_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "bit_identical": <bool>
  }
}
```

> **N9 fix (labeling):** `config.control_arms` lists the 6 control arms; `config.candidate` is a separate field (not a 7th entry in `arms`). The candidate is the system under test, not a control arm.
>
> **N6 fix (reproducibility check):** the `reproducibility` object re-runs all 3 seeds a second time within the same process and verifies bit-identical results, shipping a per-seed `max_abs_diff` map (as M1's I1 did). The cost is trivial.
>
> **N11 fix (intermediate chain_integrity):** `chain_integrity_after_initial_build`, `chain_integrity_after_shift_probe`, `chain_integrity_after_10x_growth` are reported per seed, so the JUDGE can distinguish construction breaks from re-resolution breaks (§5b).
>
> **N12 fix (per-append shift):** `shift_per_append` (array of 8 booleans, one per shift-probe append) is reported per seed, so the JUDGE can distinguish wiring defects from partial mechanism failures (§5c).
>
> **B2 fix (raw materialization sizes):** `raw_answer_size_1x`, `raw_answer_size_10x`, `raw_answer_size_ratio` are reported separately, documenting that the unbounded query's answer-set grows ~10× with history. The latency bar is NOT measured on these; it is measured on the bounded-output queries.
>
> **Property (ii) scaling curves:** `candidate_scaling_curve`, `fair_naive_scaling_curve`, `candidate_slope`, `fair_naive_slope`, `scaling_collapse_ratio` (diagnostic ONLY), `candidate_latency_growth_10x`, `fair_naive_latency_growth_10x`, `battery_valid`, `candidate_latency_iqr_per_point`, `fair_naive_latency_iqr_per_point` are reported so the JUDGE and CRITIC can inspect the scaling curves directly and verify the timing methodology.
>
> **Property (iii) downstream consumer (Option E, REVISED):** `downstream_quality_candidate`, `downstream_quality_frozen`, `downstream_degradation` are reported per seed and as means, so the JUDGE can verify the consistency requirement and the floor. The observed degradation MAGNITUDE is reported (Q3 attachment 2: "the floor is a floor, not a finding"). The consumer is fully specified (ADDITIVE relevance `dot(v(e),q) + λ·exp(-coord_cycle_relative/τ)` on 32-d BUCKETED SPIKE feature vectors, 50 queries per seed [20 recency-discriminative targeting 20 RD content-buckets of size K_rd=30 > k, + 30 content-unique targeting 30 CU content-buckets of size exactly k=10], τ=50 UNCHANGED [pinned Q3-1], λ=16.0, A=10.0, σ_f=σ_q=0.10, k=10, `coord_cycle_relative` only — NB-3 promoted to required-before-build, NB-4 accepted for E1 scope). The frozen-origin ablation is Option E (Rebecca's binding ruling §Q1): all entries retained, `coord_cycle_relative = 0` at birth for all entries → the recency bonus collapses to the constant `λ` → the frozen arm ranks purely by content; never re-resolved — content intact, temporal self-location gone. The recency-discriminative fraction (40%, 20 of 50 queries targeting 20 RD content-buckets of 30 content-tied entries at spread cycles) is pre-registered; the CRITIC verifies (a) degradation < 1.0 is reachable (content-only ranking succeeds on content-unique queries — SIMULATED CU degradation 0.000) and (b) the fraction makes the 0.05 floor meaningfully clearable by a working mechanism (SIMULATED aggregate degradation 0.102, all seeds > 0.05 floor). The prior multiplicative `exp(-coord/τ)·dot` form with random Gaussian features was REPLACED because its 9-orders-of-magnitude recency gradient overwhelmed the content signal on all queries (CRITIC BLOCKING ISSUE 1; see §6.iii "Why additive").
>
> **Retired kill (a):** the `retired` object in `kill_conditions` documents the retirement with rationale, so the artifact is self-explanatory. The metric `equivalence_agreement_vs_fair_naive` is reported as a diagnostic (expected ~1.0).

#### 7.3.2 `e1_invariants.json` — invariant/kill-condition verdict

```json
{
  "e1_verdict": "PASS | FAIL | NOT_GREEN",
  "kill_conditions": {
    "(b)": {"fires": <bool>, "detail": "...", "construction_break": <bool>, "re_resolution_break": <bool>},
    "(c)": {"fires": <bool>, "detail": "...", "wiring_defect": <bool>, "partial_failure": <bool>},
    "(d)": {"fires": <bool>, "detail": "...", "latency_ratio_membership": <f>, "latency_ratio_bounded_k": <f>, "candidate_latency_growth_10x": <f>, "fair_naive_latency_growth_10x": <f>, "battery_valid": <bool>, "instrument_failure": <bool>, "scaling_collapse_ratio_diagnostic": <f>},
    "(e)": {"fires": <bool>, "detail": "..."},
    "(f)": {"fires": <bool>, "detail": "...", "signed": true},
    "(a)_retired": {"status": "RETIRED", "rationale": "unsatisfiable by construction per Rebecca's theorem"}
  },
  "property_i_correctness": {
    "oracle_agreement": <f>,
    "bar": 1.0,
    "passes": <bool>
  },
  "property_ii_operational_distinctness": {
    "latency_ratio_membership": <f>,
    "latency_ratio_bounded_k": <f>,
    "latency_bar": "both <= 2.0",
    "latency_passes": <bool>,
    "candidate_latency_growth_10x": <f>,
    "fair_naive_latency_growth_10x": <f>,
    "battery_valid": <bool>,
    "battery_validity_bar": "fair_naive_latency_growth_10x >= 4.0",
    "state_dependent_collapse_bar": "candidate_latency_growth_10x <= 2.0 on valid battery",
    "state_dependent_passes": <bool>,
    "instrument_failure": <bool>,
    "candidate_slope": <f>,
    "fair_naive_slope": <f>,
    "scaling_collapse_ratio_diagnostic": <f>,
    "scaling_note": "slope ratio is a REPORTED diagnostic ONLY; never a trigger (Rebecca Q2)",
    "timing_methodology": "median >=100 reps, warm-up excluded, monotonic clock, IQR reported (NB-6 resolved)",
    "equivalence_agreement_vs_fair_naive": <f>,
    "equivalence_note": "REPORTED diagnostic; expected ~1.0; carries NO kill"
  },
  "property_iii_load_bearing_coupling": {
    "downstream_degradation_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "downstream_degradation_mean": <f>,
    "floor": 0.05,
    "magnitude_note": "the floor is a floor, not a finding — observed magnitude reported (Q3 attachment 2)",
    "consistent": <bool>,
    "passes": <bool>,
    "consumer_spec": "additive relevance dot + lambda*exp(-coord/tau), 32-d bucketed spike features, 50 queries/seed, tau=50 (pinned Q3-1), lambda=16.0, k=10, coord_cycle_relative only (NB-4 accepted for E1; full landmark-relative at M5); simulated aggregate degradation 0.102 in (0,1)",
    "note": "miniature of L15 (M5 applies in full); a candidate whose coordinates are consumed by nothing is a cache with a philosophy"
  },
  "l2_chain_axis": {
    "chain_integrity_final": <f>,
    "chain_integrity_after_initial_build": <f>,
    "chain_integrity_after_shift_probe": <f>,
    "chain_integrity_after_10x_growth": <f>,
    "bar": "chain_integrity_final == 1.0",
    "passes": <bool>
  },
  "l4_shift_axis": {
    "coordinate_shift": <f>,
    "shift_per_append": {"42": [<8 bools>], "43": [<8 bools>], "44": [<8 bools>]},
    "bar": "coordinate_shift == 1.0",
    "passes": <bool>
  },
  "l11_wall_clock_axis": {
    "wall_clock_shift_detected": <f>,
    "bar": "wall_clock_shift_detected == 0.0",
    "passes": <bool>,
    "defensive_check_note": "N1: tests for implementation bugs, not mechanism-level L11 violations"
  },
  "reproducibility": {
    "bit_identical": <bool>,
    "max_abs_diff_per_seed": {"42": <f>, "43": <f>, "44": <f>}
  },
  "i3_contamination": {
    "method": {
      "name": "empirical_null_self_consistency",
      "provenance": "Rebecca-locked: empirical-null method (Ruling O-14). N4 fix: null generated by running >=100 seeded replicates of EACH contamination arm (self-consistency null), NOT the naive arm.",
      "rules": "For each contamination arm, run >=100 seeded replicates of THAT arm with different seeds; compute the distribution of oracle_agreement; the I3 band = central 99% interval. The 3-seed mean must fall in the band. Re-run-on-failure is FORBIDDEN.",
      "null_replicate_count": <int, >=100>,
      "null_source_per_arm": {
        "shuffled_cadence": "self (>=100 replicates of shuffled_cadence)",
        "empty": "self (>=100 replicates of empty; degenerate distribution [0.0, 0.0] — trivially in-band)",
        "wall_clock_injection": "self (>=100 replicates of wall_clock_injection)"
      }
    },
    "per_arm_per_metric": {
      "shuffled_cadence": {"oracle_agreement": {"in_band": <bool>, "null_band_lo": <f>, "null_band_hi": <f>, "low_power": <bool>}},
      "empty": {"oracle_agreement": {"in_band": <bool>, "null_band_lo": 0.0, "null_band_hi": 0.0, "low_power": false, "note": "degenerate distribution; trivially in-band"}},
      "wall_clock_injection": {"shift_vs_candidate": {"in_band": <bool>, "null_band_lo": <f>, "null_band_hi": <f>, "low_power": <bool>}}
    }
  }
}
```

> **N4 fix (I3 null distribution source):** the null for each contamination arm is generated by running ≥100 seeded replicates of **that same arm** (self-consistency null), explicitly stated per arm. The `empty` arm's null is degenerate `[0.0, 0.0]` (returns nothing, nothing matches) — trivially in-band. The naive arm is NOT used as the null (in E1, fair-naive is a correct recomputation, not a chance floor — using it as the null would make every contamination arm fail I3 spuriously).

#### 7.3.3 `e1_manifest.json` — run manifest (courier round-trip log)

```json
{
  "command": "python e1_experiment.py --seeds 42,43,44 --output-dir ./e1_output",
  "commit_hash": "<git rev-parse HEAD, 40 hex chars>",
  "purpose": "E1 moving-origin experiment (three-property test per Rebecca's E1 gate ruling + Q2/Q3 incorporations): (i) correctness (oracle_agreement == 1.0, kill f), (ii) operational distinctness (latency_ratio <= 2.0 [d1] AND candidate_latency_growth_10x <= 2.0 on a battery where fair_naive_latency_growth_10x >= 4.0 [d2]; slope ratio is diagnostic only; kill d), (iii) load-bearing coupling (downstream_degradation > 0 on all seeds AND mean >= 0.05; observed magnitude reported). Plus structural: chain integrity (kill b), coordinate shift (kill c), wall-clock independence (kill e). Old kill (a) RETIRED. 5 active kill conditions (b-f). Timing methodology: median >=100 reps, warm-up excluded, monotonic clock, IQR reported (NB-6 resolved).",
  "bars": "oracle_agreement == 1.0 (kill f); latency_ratio <= 2.0 [d1] AND candidate_latency_growth_10x <= 2.0 on battery where fair_naive_latency_growth_10x >= 4.0 [d2] (kill d; slope ratio diagnostic only); chain_integrity == 1.0 (kill b); coordinate_shift == 1.0 (kill c); wall_clock_shift_detected == 0.0 (kill e); downstream_degradation > 0 all seeds AND mean >= 0.05 (property iii; magnitude reported). Old equivalence_agreement <= 0.90 RETIRED.",
  "seeds": [42, 43, 44],
  "wall_clock_seconds": <float>,
  "deps": {"python": "3.11.x", "numpy": "1.26.4", "scipy": "1.13.1"},
  "python_version_runtime": "<filled by Rebecca's python --version output>",
  "output_files": ["e1_run_results.json", "e1_invariants.json", "e1_manifest.json", "e1_run.log", "e1_profile.json"],
  "deviations_logged": []
}
```

#### 7.3.4 `e1_run.log` — raw stdout/stderr capture (UTF-8 encoded — M1 hygiene fix carried forward).

#### 7.3.5 `e1_profile.json` — L20 drift baseline for E1

```json
{
  "profile_version": "e1-locked-3.0",
  "profile_vector": [<6 floats: candidate's 6 metrics mean-over-seeds, order: oracle_agreement, latency_ratio_membership, candidate_latency_growth_10x, chain_integrity_final, coordinate_shift, downstream_degradation>],
  "metric_order": ["oracle_agreement", "latency_ratio_membership", "candidate_latency_growth_10x", "chain_integrity_final", "coordinate_shift", "downstream_degradation"],
  "drift_criterion": "pearson_corr(profile_vector, new_profile_vector) < 0.70 => drifted (locked bar); self-test threshold < 0.50",
  "l20_self_test": {
    "no_drift_corr": 1.0,
    "no_drift_passes": true,
    "perturbation_1": "metric_block_reversal",
    "perturbation_1_definition": "N5 fix: reverse the 6-element profile vector [m0,m1,m2,m3,m4,m5] -> [m5,m4,m3,m2,m1,m0]. (Before: [oracle_agreement, latency_ratio_membership, candidate_latency_growth_10x, chain_integrity_final, coordinate_shift, downstream_degradation]. After: [downstream_degradation, coordinate_shift, chain_integrity_final, candidate_latency_growth_10x, latency_ratio_membership, oracle_agreement].)",
    "perturbation_1_corr": "<float, must be < 0.50>",
    "perturbation_2": "candidate_empty_swap",
    "perturbation_2_definition": "N5 fix: swap the candidate's profile vector [m0..m5] with the empty arm's profile vector [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] (empty arm has oracle_agreement=0.0 and all other metrics at chance/zero). Resulting vector: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]. (Before: candidate's 6 metrics. After: empty arm's 6 metrics — all zeros.)",
    "perturbation_2_corr": "<float, must be < 0.50>",
    "both_perturbations_flag_drift": true
  }
}
```

> **N8 fix (profile vector, updated for v3 + Q2 restructure):** the profile vector now has 6 elements — all candidate metrics, updated for the three-property test and the Q2 collapse-criterion restructure: `oracle_agreement` (property i), `latency_ratio_membership` and `candidate_latency_growth_10x` (property ii — the latter replaces the retired `scaling_collapse_ratio` slope-ratio trigger, which is now a diagnostic only per Rebecca's Q2 ruling), `chain_integrity_final` (structural L2), `coordinate_shift` (structural L4), `downstream_degradation` (property iii). The retired `equivalence_agreement` is NOT in the profile vector (it is a diagnostic, not a candidate metric). `wall_clock_shift_detected` is NOT in the profile vector (it is a defensive check, expected False; including a constant-False metric would zero-variance the vector). `frozen_oracle_agreement` is NOT in the profile vector (it is a control arm's metric). The slope ratio `scaling_collapse_ratio` is NOT in the profile vector (it is a reported diagnostic only, never a trigger).
>
> **NEW-1 fix (zero-variance edge case, from CRITIC re-review):** `pearson_corr(x, const)` is defined as `0.0` when the second vector has zero variance, which trivially satisfies `< 0.50` and flags drift. The BUILDER implements this edge-case handling.
>
> **N5 fix (perturbation definitions):** both perturbations have exact before→after vector transformations specified (as M1 did). `metric_block_reversal`: reverse the 6-element profile vector. `candidate_empty_swap`: swap the candidate's 6 metrics with the empty arm's 6 metrics (all zeros).

### 7.4 Single artifact

`e1_experiment.py` (one script) + `requirements.txt`. The script is self-contained: it generates the synthetic autobiography (with deferred landmark designation), builds the candidate mechanism (§1) and the 6 control arms (§3, including the fair naive arm with full event-log access), runs the 200 queries × 6 arms × 3 seeds, evaluates the three properties (i, ii, iii) + structural checks, evaluates the 5 active kill conditions (b-f), runs the state-dependent scaling battery (5 history-size points × candidate + fair-naive), runs the downstream consumer over the candidate and frozen-origin indices, runs the I3 empirical-null (≥100 self-consistency replicates) for the contamination arms, runs the L20 drift self-test, runs the reproducibility check (re-run 3 seeds, verify bit-identical), and writes the 5 output files. No external data files; all data is synthesized in-process from the seed.

### 7.5 Run purpose / bar (stated in manifest)

- **Purpose:** Test the moving-origin candidate (L2 + L4, three-property test per Rebecca's ruling) against 5 active kill conditions (b-f), 3 seeds.
- **Bar:** `oracle_agreement == 1.0 (kill f); latency_ratio <= 2.0 [d1] AND candidate_latency_growth_10x <= 2.0 on a battery where fair_naive_latency_growth_10x >= 4.0 [d2] (kill d; slope ratio diagnostic only); chain_integrity == 1.0 (kill b); coordinate_shift == 1.0 (kill c); wall_clock_shift_detected == 0.0 (kill e); downstream_degradation > 0 all seeds AND mean >= 0.05 (property iii; observed magnitude reported)`. Old `equivalence_agreement <= 0.90` RETIRED. Any active kill condition firing → candidate dead (D1). Timing methodology: median >=100 reps, warm-up excluded, monotonic clock, IQR reported (NB-6 resolved).

### 7.6 Rebecca's courier obligations (per Entry 13)

Run verbatim (log any deviation); return raw and complete (never curate); log round trip (command, commit hash, seeds, wall-clock, output list). The experiment auto-populates `e1_manifest.json` with commit hash and wall-clock; Rebecca confirms the values.

### 7.7 Team obligations on receipt

Returned outputs are ground truth; the JUDGE scores only from returned artifacts; the CRITIC may request re-runs / additional seeds / controls; incomplete provenance = unscoreable. **Re-run-on-failure is FORBIDDEN** (Ruling O-14).

---

## 8. Scope fence (what E1 does NOT include)

E1 is the moving-origin experiment — the cheapest possible death of the program's core novelty. It is narrowly scoped. Explicitly OUT of scope for E1:

- **No L1 (access physics / decay) — EXCEPT the toy downstream consumer in property (iii).** No decay curves, no retrieval-probability-by-age, no rehearsal axis as a standalone test. The candidate's `coord_cycle_relative` is a linear offset, not a decay function. **The minimal downstream consumer (§6.iii) is a TOY recency-weighted retrieval implementing L1's access physics — it is a test instrument for property (iii), NOT the full L1 system.** L1 is M3.
- **No L3 (thick present).** No retention/protention, no next-input prediction, no horizon-H state. The candidate is a substrate, not a predictive state. L3 is M3.
- **No L5 (bi-temporality).** No world-validity axis, no supersession chains. The candidate has ONE time axis (autobiography position). L5 is M3.
- **No L6 (episodic completeness / provenance).** No when-for-me / from-what / under-what-circumstances; no provenance stack. The candidate's payload is an opaque content_id. L6 is M3.
- **No L7 (mirror / peer-observer).** No self-report, no peer-observer baseline. L7 is M4.
- **No L8 (stakes coupling).** No homeostatic variables. L8 is M4.
- **No L9 (linear read).** No associative retrieval channel. L9 is M3.
- **No L10 (abstention under drift).** No drift regimes, no abstention. L10 is M4.
- **No L11–L14 (interface laws) as discrete tests — EXCEPT the wall-clock-injection arm (L11 probe, defensive check).** L11 is probed at E1 via arm 6 (coordinates must not shift with wall-clock — N1: defensive check against implementation bugs, not a mechanism-level test). L12 (one state), L13 (writes through the now), L14 (stakes) are not tested at E1. The wall-clock-injection arm is the ONE §2 probe at E1, per CRITIC Obj 15 (adopted).
- **No L15–L17 (integration / promotion gate) as FULL tests — EXCEPT the property (iii) miniature.** The property (iii) load-bearing coupling test is a MINIATURE of the L15 test (ablate A, measure degradation of B), placed at E1 because the theorem shows coupling, not answers, is where "moving origin" has meaning. M5 applies L15 in full. L16 (emergence over sum) and L17 (non-simultaneity) are M5. The candidate is a single component; property (iii) tests its coupling to a toy consumer, not full system integration.
- **No ablation of the candidate's sub-components.** E1 tests ONE candidate against kill conditions and 6 control arms. Property (iii) ablates the candidate's RE-RESOLUTION (frozen-origin arm), not its sub-components (that is L15 at M5).
- **No mirror/peer-observer.** No self-report channel. (L7 is M4.)
- **No real-system runs.** E1 runs on the synthetic autobiography with known ground truth. It does not exercise the candidate on real data.
- **No bar invention, lowering, or raising.** All numeric values are locked from M0 (and Rebecca's ruling); the BUILDER implements them verbatim. The JUDGE enforces D1/D5; the CRITIC polices D2 distinctness. The retired kill (a) is RETIRED (not softened — it is unsatisfiable by construction per Rebecca's theorem); the promoted kill (f) is SIGNED (not invented — Rebecca signed it at the gate); the new property (iii) floor (0.05) is pre-registered here per L19 (the CRITIC assesses its falsifiability). **Q2 restructure (specification completion, not a new revision cycle):** the 0.5 slope-ratio collapse trigger is RETIRED as a trigger (RETAINED as a diagnostic) — the new trigger uses the ALREADY-LOCKED latency bar (≤ 2.0× growth) on the state-dependent battery, with a NEW battery-validity instrument check (fair-naive ≥ 4.0× growth, NOT a kill). The battery-validity threshold (4.0×) is pre-registered here per L19. **Q3 completions (specification completions, not a new revision cycle):** the downstream consumer is now FULLY SPECIFIED (NB-3 promoted to required-before-build — dot product on 32-d feature vectors, 50 queries per seed, τ=50, k=10, `coord_cycle_relative` only); the observed degradation magnitude is REQUIRED to be reported (Q3 attachment 2 — "the floor is a floor, not a finding"). **NB-4 standing note:** the consumer exercises `coord_cycle_relative` only (not `coord_landmark_relative`) — accepted for E1 scope; full landmark-relative coupling belongs to the L15 matrix at M5. **NB-5 resolved:** the query battery includes only landmarks designated by that point in the run; the pre-designation window is the shift-measurement material. **NB-6 resolved:** the mandated timing methodology (median, warm-up excluded, monotonic clock, dispersion reported) resolves the timing-precision robustness concern.
- **No external writeups.** L20's external-writeup clause is a future obligation; E1 produces no external writeup. The L20 drift self-test (§7.3.5) is the internal-naming discipline, carried forward from M1.
- **No retry.** E1 tests Candidate 1.1 only. Candidate 2 / Candidate 3 are not specified here; they are specified only if Candidate 1.1 dies in a scoring run, per D2. The retry budget is 3, spent 0, remaining 3. **Per Rebecca's ruling (§3), Candidate 1.1 is NOT charged as a death** — the v2 distinctness claim dissolves under the fair baseline, but the mechanism remains legitimate under the revised test.

---

## 9. Sequencing (M2, reconciled to BUILD_PHASE_ORG and Rebecca's ruling)

1. **ARCHITECT delivers this revised spec** (this document, v3, implementing Rebecca's gate ruling) → RECORDER logs it.
2. **CRITIC reviews the spec for falsifiability/ambiguity** (standing instruction, Entry 11.10) before the build cell is re-instantiated for E1. Bounce if any arm/metric/kill-condition is vacuous or unsatisfiable. **The CRITIC is directed (Rebecca's ruling §4 item 1) to treat §6 (the three-property test) as the review's center of gravity — specifically: (a) the fair-naive definition (§6.ii: does the fair naive read the FULL event log including designation events? does it have NO maintained index state? does it recompute by scan at query time? is it the strongest honest timestamps-and-scan implementation, or a strawman?); (b) the state-dependent battery (§6.ii: do the 5 history-size points fit a scaling curve? does the collapse criterion (candidate_latency_growth_10x ≤ 2.0× on a battery validated by fair-naive ≥ 4.0× growth) genuinely distinguish maintained-state from replay? is the battery-validity check (fair-naive ≥ 4.0×) falsifiable? is the timing methodology (median, warm-up excluded, monotonic clock, dispersion) sufficient to prevent jitter-firing (NB-6)? is the state-dependent material (deferred-designation landmarks) actually state-dependent? does the NB-5 construction (query battery includes only designated landmarks) hold?); (c) the downstream consumer (§6.iii: is the consumer FULLY SPECIFIED — exact similarity function (dot product on 32-d vectors), exact query set (50 per seed), exact coordinate usage (`coord_cycle_relative` only, NB-4 accepted for E1)? does the consumer genuinely consume the candidate's coordinates? does the ablation (frozen-origin, Option E) genuinely degrade the consumer? is the floor (0.05) falsifiable? is the observed degradation MAGNITUDE reported (Q3 attachment 2)? does the recency-discriminative battery (§6.iii) include a pre-registered fraction (40%) of near-duplicate-content queries at different ages where content ties and the coordinate breaks the tie? is degradation < 1.0 reachable (content-only ranking succeeds on content-unique queries)? does the recency-discriminative fraction make the 0.05 floor meaningfully clearable by a working mechanism?).** The CRITIC also assesses the retired kill (a) rationale (§12: is the retirement justified by Rebecca's theorem?) and the promoted kill (f) (is `oracle_agreement = 1.0` a genuine correctness floor?).
3. **Rebecca go/no-go gate** — the revised spec + CRITIC review go to Rebecca for sign-off before any building. This is BOTH the E1 spec gate AND the L4 historically-graveyard gate (already signed at M0, Entry 11.8 — re-confirmed at this gate with the concrete candidate and the amended L4 test in hand). **Per Rebecca's ruling (§4 item 6), the timebox clock starts when the revised spec clears this gate, not before.** No code before sign-off.
4. Upon Rebecca's go: **INTEGRATOR re-initializes the build cell for M2** (sizing: INTEGRATOR + 1 TASK BUILDER — the ARCHITECT argues no expansion is needed; see §0.8). INTEGRATOR updates STATE.md (milestone → M2, new timebox per §10, clock starts at gate clearance), decomposes the spec into a task spec for the TASK BUILDER.
5. **TASK BUILDER implements `e1_experiment.py` + `requirements.txt`** on a task branch, against the spec + STATE.md. Task is done when pre-written tests pass (the three properties + kill conditions + metrics + I3 + L20 self-test + reproducibility check ARE the test suite). Prerequisites (git repo DONE; ≥100 null replicates) must be complete before the scoring run.
6. **INTEGRATOR merges to main branch, packages the merge-candidate courier run (RUN-2) for Rebecca** (courier packet, §7), and blocks the merge until returned artifacts are scored. **Channel split (O-15):** development/diagnostic runs in the build cell sandbox are permitted (non-artifacts, never scored); RUN-2 is a scoring run → exclusively through Rebecca's supervised-executor courier channel.
7. **Rebecca runs verbatim, returns the 5 output files + manifest.**
8. **JUDGE scores from returned artifacts only** — the three properties (§6), the kill conditions (b-f), the structural axes (L2/L4/L11), I3, L20 self-test, reproducibility check. The JUDGE applies D1 (a firing kill condition kills the candidate immediately) and D5 (no re-run/re-score/reframe). The JUDGE uses the intermediate `chain_integrity` (N11) and `shift_per_append` (N12) artifacts to distinguish construction/wiring defects from mechanism deaths (§5b/§5c, Rebecca ruling §4 items 4–5 guard). The JUDGE assembles the three-property verdict (§6.iv).
9. **CRITIC reviews the returned artifacts** — internal numeric consistency, hidden anomalies, scope drift, the three-property arithmetic (§6.i/ii/iii), the fair-naive implementation (is it actually fair — full event-log access, no maintained state?), the scaling curves (do they genuinely differ?), the downstream consumer degradation (is it genuinely positive and consistent?), and (if a kill condition fired) the D2 diagnosis format (does the logged cause of death support a mechanistically-distinct Candidate 2?).
10. **RECORDER logs the verdict**, records STATE.md hash, and updates STATE.md. Session closes.
11. **If PASS (all three properties pass; no kill condition fires):** E1 passes → the moving origin earns its place → Rebecca continuation gate to M3. The retry budget remains 3, spent 0.
12. **If FAIL (any kill condition b-f fires):** Candidate 1.1 is dead (D1), UNLESS the kill is a construction/wiring defect (§5b/§5c/§5e, Rebecca ruling §4 items 4–5 guard: specific defect identified, fixed, CRITIC-confirmed before re-run escapes D2 budget) — in which case the BUILDER fixes and re-runs (NOT result laundering). The RECORDER logs the diagnosed cause of death. The moving-origin IDEA has 2 retries remaining under D2. The program pauses for Rebecca's decision: (i) authorize Candidate 2 (requires ARCHITECT distinctness statement + CRITIC annotation + Rebecca sign-off), or (ii) if D3 convergent failure applies (2 candidates, same cause), close the idea-class and end the program honestly per D4. **The program does NOT continue to M3 without a passing moving origin** — every downstream component is built over it.
13. **If NOT-GREEN (property (iii) fails AND no kill condition fires):** the candidate is not dead, but the moving origin has not earned its place (its coordinates are not load-bearing). The program pauses for Rebecca's decision (§5 property (iii) failure routing): (a) the downstream consumer or ablation is mis-specified (a spec/implementation issue — fix and re-run, NOT a candidate death), or (b) the candidate's coordinates are genuinely not load-bearing (a mechanism limitation — Candidate 1.1 does not earn its place; the program routes to the D2 retry decision). The specific cause must be identified and CRITIC-confirmed before any re-run escapes the D2 budget.

---

## 10. Timebox (M2, per Rebecca's ruling §4 item 6 — clock starts at gate clearance)

### 10.1 M1 actuals (the calibration data)

Per Entry 25 (Rebecca's acceptance) and STATE.md:
- M1 timebox budget: 3 working sessions OR 7 calendar days, whichever ends first.
- M1 actuals: **1 session consumed, 1 day consumed.** Budget mostly unspent.
- M1 delivered GREEN within the first session.

### 10.2 M2 timebox (APPROVED by Rebecca, ruling §4 item 6)

**3 working sessions OR 7 calendar days, whichever ends first** — identical to M1's budget.

**Clock starts at gate clearance (Rebecca ruling §4 item 6, APPROVED):** the timebox clock starts when the revised spec clears Rebecca's gate (§9 step 3), NOT before. The ARCHITECT's revision time, the CRITIC's re-review time, and Rebecca's gate time do NOT count against the M2 timebox. The clock starts when the build cell is authorized to build.

**Rationale (ARCHITECT's calibration argument):**
- M1 consumed 1/3 sessions and 1/7 days. A naive extrapolation would shrink M2's box to 1 session / 1 day. The ARCHITECT **does not** propose shrinking, for three reasons:
  1. **E1 is the graveyard gate.** L4 is the highest-falsification-risk component in the program (CRITIC's independent assessment, Entry 7). The three-property test (§6) is the review's center of gravity. Compressing the box on the riskiest milestone is false economy.
  2. **E1 is structurally similar in build shape to M1** (one script + pinned deps + one launch command), but the candidate mechanism's logic (§1) and the three-property test (§6: state-dependent battery + downstream consumer) are more complex than M1's toy problem. The build effort is comparable; the *spec* and *review* effort is higher.
  3. **M1's under-spend is not evidence that M2 will under-spend.** M1 was instrumentation validation on a toy problem. E1 is a real falsification test of a real candidate; the CRITIC review (§6 center of gravity) and the JUDGE scoring are likely to surface more issues.

**Half-budget tripwire (same as M1):** after session 2 OR day 4 (counted from gate clearance), if the candidate cannot pass ANY of the three properties on ANY seed in development runs (diagnostic only, non-scoring per O-15), work **pauses** for a scope review with Rebecca. This is a review trigger, not a kill.

**Courier latency budgeting (same as M1, Entry 13):** courier round-trip time counts against the timebox UNLESS the queue exceeds 1 calendar day, in which case the clock pauses until return. The RECORDER logs queue pauses.

**Timebox expiry without delivery:** program pause and scope review with Rebecca (review trigger, not punishment). Per D5, the timebox is NOT extended by the Persistence Doctrine.

### 10.3 Delivery (green) criteria for M2

M2 (E1) is delivered green iff ALL hold:
- (a) **No kill condition fires** (b, c, d, e, f all false). [Old (a) RETIRED — not evaluated.]
- (b) **Property (i) correctness passes:** `oracle_agreement == 1.0` (§6.i).
- (c) **Property (ii) operational distinctness passes:** `latency_ratio ≤ 2.0` (both bounded-output query types, d1) AND `candidate_latency_growth_10x ≤ 2.0` on a battery where `fair_naive_latency_growth_10x ≥ 4.0` (d2; if battery invalid → instrument failure, run unscoreable). The slope ratio is a diagnostic only (§6.ii).
- (d) **Property (iii) load-bearing coupling passes:** `downstream_degradation > 0` on all 3 seeds AND `mean_degradation ≥ 0.05` (§6.iii).
- (e) **Structural checks pass:** `chain_integrity == 1.0` (kill b), `coordinate_shift == 1.0` (kill c), `wall_clock_shift_detected == 0.0` (kill e).
- (f) **I3 contamination verdict is trustworthy** (shuffled_cadence and empty arms in-band on the empirical null; low-power flags honestly reported).
- (g) **L20 self-test passes** (no-drift corr = 1.0; both pinned perturbations corr < 0.50).
- (h) **Reproducibility check passes** (bit-identical re-run; N6 fix).
- (i) **STATE.md current** (INTEGRATOR maintains; RECORDER attests hash).
- (j) **Manifest carries a real commit hash** (prerequisite 1, DONE).

> If any kill condition (b-f) fires, M2 is delivered **red** (candidate dead), not green — and the program routes to the D2 retry decision (§9 step 12), not to M3. A red M2 is a legitimate, reportable verdict (D4). A construction-bug or wiring-defect kill (§5b/§5c/§5e, Rebecca ruling §4 guard) is a BUILDER defect, NOT a red M2 — the BUILDER fixes and re-runs (NOT result laundering).
>
> If property (iii) fails AND no kill condition fires, M2 is delivered **not-green** (candidate alive but place not earned) — the program routes to the property (iii) failure routing (§9 step 13).

**Rebecca signs off on this timebox at the gate (§9 step 3). The clock starts at sign-off (ruling §4 item 6).**

---

## 11. L19 base-rate duty (pre-register the L4 graveyard classifications — updated for the revised test)

Per L19 (pre-registration) and the M0 graveyard classification (Entry 6/11), the ARCHITECT pre-registers the base-rate classifications relevant to E1 (the L4 graveyard gate, amended test). These are NOT re-litigated at E1; they are carried forward from M0 and updated for Rebecca's ruling, and logged here for E1's pre-registration.

### 11.1 The L4 graveyard classification (pre-registered at M0, carried forward — test AMENDED)

| Component | Milestone | Graveyard rationale (base-rate prior) | Gate status |
|---|---|---|---|
| **L4 — Re-resolving egocentric index (the moving origin)** | M2 (E1) | The genuinely novel object. Re-resolving indices that do not collapse to recomputation have a long failure history. The CRITIC independently flagged this as the highest-falsification-risk component in the program (Entry 7). E1 exists precisely to test this — it is the program's cheapest possible death and runs first among the graveyard-class components. **Test AMENDED per Rebecca's ruling:** the old informational collapse test (kill a) is RETIRED (unsatisfiable by construction — Rebecca's theorem). The three-property test (correctness, operational distinctness, load-bearing coupling) replaces it. | **SIGNED** (Entry 11.8, M0). Re-confirmed at the E1 gate (§9 step 3) with the concrete candidate and the amended test in hand. |

### 11.2 Base-rate expectations for E1's outcomes (pre-registered, updated for the revised test)

The ARCHITECT pre-registers the following base-rate expectations, so that the E1 verdict is interpreted against an honest prior, not post-hoc:

| Outcome | Base-rate expectation | Interpretation if observed |
|---|---|---|
| **Candidate 1.1 is wrong (kill f, oracle_agreement < 1.0)** | **Low-moderate prior** — a buggy re-resolver that mis-tracks designation events (e.g., uses the wrong `designated_at`, or corrupts the landmark registry) would not match the oracle. The bar is strict (= 1.0), so any single-query mismatch fires it. | Candidate 1.1 dies; D2 retry budget 2 remaining. The diagnosis (§5f) determines whether a Candidate 2 differing on C1.1/C1.2/C1.4 can engage the cause. |
| **Candidate 1.1 breaks the hash chain (kill b)** | **Low prior** — SHA-256 chaining is well-understood; a construction bug, not a mechanism failure. | If observed, likely a BUILDER bug (construction break — §5b: fix and re-run, NOT a candidate death, per Rebecca ruling §4 item 4 guard). If the break is in re-resolution (chain valid initially, breaks later), it IS a mechanism death. |
| **Candidate 1.1 shows no shift (kill c)** | **Low-moderate prior** — the offset-counter (C1.1) is simple; a no-shift result would indicate the re-resolution is not wired to the append path. | If observed, likely a wiring bug (§5c: fix and re-run, NOT a candidate death, per Rebecca ruling §4 item 5 guard). If the shift is partial (some appends shift, some don't), it IS a mechanism death. |
| **Candidate 1.1 scans or collapses (kill d, latency_ratio > 2.0 [d1] OR candidate_latency_growth_10x > 2.0 on a valid battery [d2])** | **Low-moderate prior** — the B2 fix measures latency on bounded-output queries (d1 satisfiable). The state-dependent battery (d2) applies the SAME locked latency bar (≤ 2.0× growth) to the state-dependent battery, validated by fair-naive's ≥ 4.0× growth (battery-validity instrument check). The slope ratio is a diagnostic only (Q2 restructure). If the BUILDER implements the candidate as reading maintained state (offset counter + pre-computed lookup), d2 passes (candidate_latency_growth_10x ≈ 1.0). If the BUILDER accidentally scans at query time, d2 fails (growth ≈ 10×). | If observed, the candidate's specific mechanism (C1.1) failed or the BUILDER implemented a scan. A Candidate 2 with a different re-resolver (e.g., a tree-based index) would engage a scan cause. If the battery is invalid (fair-naive < 4.0× growth), it is an instrument failure (run unscoreable, battery revised — not a kill). |
| **Candidate 1.1 shifts with wall-clock (kill e)** | **Low prior** — L11 (one clock) is a structural invariant; the candidate uses `e.cycle` and `L.designated_at` (both autobiography-position-derived). A wall-clock leak would indicate an implementation bug. | If observed, likely a BUILDER implementation bug (N1: defensive check, Rebecca ruling §4 guard). A Candidate 2 with a logical-clock cycle counter (C1.3b) would engage a wall-clock-leak cause. |
| **Candidate 1.1's coordinates are not load-bearing (property (iii) fails, downstream_degradation ≤ 0 or mean < 0.05)** | **Low-moderate prior (NEW, no historical base rate)** — this is a new test (miniature of L15). The consumer is now FULLY SPECIFIED (dot product on 32-d feature vectors, 50 queries per seed, τ=50, k=10, `coord_cycle_relative` only — NB-3 promoted to required-before-build, NB-4 accepted for E1). If the candidate's coordinates are correct (property i) and operationally distinct (property ii) but the downstream consumer does not measurably benefit from re-resolution, the coordinates are a "cache with a philosophy." The prior is low-moderate because the toy consumer is designed to consume `coord_cycle_relative` (which the candidate re-resolves), so a correct candidate should produce positive degradation — but the floor (0.05) and consistency requirement (all 3 seeds) are non-trivial. The observed MAGNITUDE is reported (Q3 attachment 2 — "the floor is a floor, not a finding"). | If observed, E1 is not-green (candidate not dead, place not earned). The program pauses for Rebecca's decision (§9 step 13): (a) consumer/ablation mis-specified (fix and re-run), or (b) coordinates genuinely not load-bearing (D2 retry decision). |
| **Old: Candidate 1.1 collapses to naive recomputation (kill a)** | **N/A — RETIRED.** The old base-rate (moderate prior, lowered from high) is RETIRED with the kill. Rebecca's theorem proves the test is unsatisfiable by construction (fair-naive ≡ oracle on answers; naive_agreement is always 1.0 for a correct candidate). The metric `equivalence_agreement` is REPORTED as a diagnostic (expected ~1.0, confirming the theorem). | N/A — kill (a) is RETIRED. If `equivalence_agreement` is NOT ~1.0, it indicates the fair naive is handicapped (a BUILDER implementation bug), not a candidate property. |

### 11.3 The D3 convergence watch (pre-registered for the retry decision)

Per D3, if Candidate 1.1 dies AND a future Candidate 2 dies of the **same diagnosed cause**, the CRITIC and JUDGE jointly assess whether the cause is intrinsic to the moving-origin idea-class. The pre-registered convergence watch:

- **If both candidates are wrong (kill f, same cause — e.g., both mis-track designation events):** the convergence is "the re-resolver cannot correctly track designation events" — D3 fires; the moving-origin idea is closed as an idea-class with a written diagnosis; the program ends honestly per D4.
- **If both candidates scan/replay (kill d, same cause):** the convergence is "the re-resolver cannot answer from maintained state at O(1)/O(log n)" — D3 fires; the program ends honestly per D4.
- **If the causes differ (e.g., Candidate 1.1 is wrong, Candidate 2 scans):** no convergence; the idea is unresolved at budget 1 remaining; Candidate 3 may be attempted per D2.

> **The base-rate duty is satisfied:** the L4 graveyard classification is pre-registered (M0, carried forward, test amended), the outcome base-rates are pre-registered (§11.2 — updated for the three-property test and the retired kill (a)), and the D3 convergence watch is pre-registered (§11.3 — updated for the revised kill set). No base-rate is renamed; no prior is tuned away. The retired kill (a) base-rate is RETIRED with the kill (not tuned to zero). The CRITIC polices this at the E1 review.

---

## 12. Constitution amendment log (Rebecca's E1 gate ruling, binding)

This section documents the constitution amendment authorized by Rebecca's E1 gate ruling (2026-08-15, binding). The ruling exercises the constitution-change authority (the L4 test is revised herein) and the second-reader clause reserved for E1's equivalence test. RECORDER logs it in full.

### 12.1 What changed

| Item | Before (v2 spec, CRITIC-cleared) | After (v3 spec, this document) | Authority |
|---|---|---|---|
| **L4 test structure** | Single-axis informational collapse test (equivalence test: candidate distinguishable from naive on answers). | Three-property test: (i) correctness, (ii) operational distinctness, (iii) load-bearing coupling. | Rebecca ruling §2 (constitution amendment, signed). |
| **Kill (a)** | LOCKED. `equivalence_agreement > 0.90` → collapse to naive recomputation. | **RETIRED.** Unsatisfiable by construction (Rebecca's theorem: fair-naive ≡ oracle on answers; the pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable). Metric retained as REPORTED diagnostic. | Rebecca ruling §2 (old kill (a) retired with rationale logged). |
| **Kill (f)** | PROPOSED [PENDING REBECCA SIGN-OFF]. `oracle_agreement < 1.0` → candidate is "broken" (distinguishable but wrong). | **SIGNED and PROMOTED** to primary correctness kill condition (property (i)). No longer PENDING. | Rebecca ruling §2(i), §4 item 3 (APPROVED, PROMOTED, SIGNED). |
| **Kill (d)** | LOCKED. `latency_ratio > 2.0` → scanning detected (latency on bounded-output queries). | **PROMOTED** to operational-distinctness discriminator (property (ii)). Latency bar UNCHANGED (≤ 2.0). EXTENDED with state-dependent query battery. **Q2 restructure (specification completion):** the 0.5 slope-ratio collapse trigger is RETIRED as a trigger (RETAINED as a diagnostic) — the new d2 trigger uses the locked latency bar (≤ 2.0× growth) on the state-dependent battery, with a NEW battery-validity instrument check (fair-naive ≥ 4.0× growth, NOT a kill). Mandated timing methodology (median, warm-up excluded, monotonic clock, dispersion) resolves NB-6. | Rebecca ruling §2(ii) (kill (d) promoted) + Q2 ruling (slope-ratio replaced) + Q2 item 4 (timing methodology). |
| **Naive arm** | `naive now−created_at`: handicapped — read only `created_at` column, did NOT receive designation events. | **RENAMED to `fair naive` and STRENGTHENED:** reads the FULL event log (including designation events), recompute-by-scan at query time, no maintained index state. The strongest honest timestamps-and-scan implementation. | Rebecca ruling §1 (the fair naive reads the full event log; the old naive was handicapped). |
| **Property (iii) load-bearing coupling** | Did not exist. | **NEW.** A minimal downstream consumer (toy recency-weighted retrieval implementing L1's access physics) must measurably degrade when re-resolution is ablated (frozen-origin arm), effect direction consistent across seeds. A miniature of the L15 test (M5 applies in full). **Q3 completions (specification completions):** the downstream consumer is now FULLY SPECIFIED (NB-3 promoted to required-before-build — dot product on 32-d feature vectors, 50 queries per seed, τ=50, k=10, `coord_cycle_relative` only); the observed degradation magnitude is REQUIRED to be reported (Q3 attachment 2). NB-4 (consumer exercises cycle-relative only) accepted for E1 scope; full landmark-relative coupling at M5. | Rebecca ruling §2(iii) (new) + Q3 ruling (NB-3 promoted, magnitude reported, NB-4 accepted). |
| **Deferred designation** | Carried a distinctness claim (candidate ≠ naive on answers). | **Retained in task design (Conway-faithful; supplies state-dependent battery's material) but carries NO distinctness claim.** | Rebecca ruling §2 (deferred designation retained, no distinctness claim). |
| **Oracle-vs-naive sanity check** | DROPPED (per CRITIC recommendation, PENDING REBECCA). | **DROPPED (APPROVED).** Under a fair baseline it is incoherent as specified. | Rebecca ruling §4 item 1 (APPROVED for removal). |
| **Chain-break bug-vs-mechanism (kill b)** | PENDING REBECCA SIGN-OFF. | **APPROVED with guard** (specific defect identified, fixed, CRITIC-confirmed before re-run escapes D2 budget). | Rebecca ruling §4 item 4 (APPROVED with guard). |
| **No-shift distinction (kill c)** | PENDING REBECCA SIGN-OFF. | **APPROVED with guard** (same guard). | Rebecca ruling §4 item 5 (APPROVED with guard). |
| **Timebox** | Proposed 3 sessions / 7 days, clock start ambiguous. | **APPROVED 3 sessions / 7 days, clock starts at gate clearance.** | Rebecca ruling §4 item 6 (APPROVED, clock starts at gate clearance). |
| **Persistence Doctrine accounting** | Candidate 1.1's status ambiguous (v2 distinctness claim). | **Candidate 1.1 NOT charged as a death.** The mechanism remains legitimate under the revised test. No retry budget consumed. The diagnosed cause is attributed to the TEST, not the candidate or the idea. | Rebecca ruling §3 (Persistence Doctrine accounting). |

### 12.2 Why the test changed (the theorem and the program finding)

**The finding (Rebecca ruling §1, binding):** The ARCHITECT's existence proof (v2 spec, §6.5) held only against a HANDICAPPED naive arm. Designation events are timestamped entries in the same append-only autobiography. A FAIR naive — the strongest honest timestamps-and-scan implementation — reads the full event log (including designation events), computes `e.created_at < L.designated_at`, and agrees with the candidate at 1.0. The v2 existence proof restricted the naive arm's inputs (no designation events) instead of accepting the implication of the central fact the ARCHITECT independently derived: *any coordinate that is a deterministic function of logged inputs is computable by a baseline holding the same inputs.*

**The theorem (Rebecca, binding):** For ANY deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle (the oracle is a log replay). Therefore the pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable — for this candidate, for every D2 retry, for anything. The answer-equivalence collapse test is a criterion nothing can pass, and a criterion nothing can pass is a broken criterion, not a hard one.

**The program finding (E1's first real finding, produced at spec-time for zero compute):** Self-location cannot be defined informationally over logged events. It must be defined operationally and integratively. The RECORDER logs this as a validated program finding.

**Why the three-property test is the correct replacement:**
- **(i) Correctness (kill f):** the candidate must match the oracle on answers. This is the floor — a wrong candidate has no place. It is satisfiable (the candidate and oracle compute the same function from the same inputs) and genuine (it catches a buggy re-resolver).
- **(ii) Operational distinctness (kill d, promoted):** the candidate must answer from maintained, incrementally re-resolved state at O(1)/O(log n) per query, while fair-naive recomputes by scan at O(n) per query. This is the operational replacement for the informational collapse test — the candidate's distinctness from fair-naive is now defined by COST SCALING, not answer agreement. It is satisfiable (the offset counter + pre-computed lookup give O(1)/O(log n); the scan gives O(n)) and genuine (it catches a candidate that secretly replays the log at query time — the candidate's latency growth exceeds 2.0× on a validated battery). **Q2 restructure:** the slope-ratio trigger is RETIRED as a trigger (RETAINED as a diagnostic); the new trigger uses the locked latency bar (≤ 2.0× growth) on a battery validated by fair-naive's ≥ 4.0× growth; the mandated timing methodology (median, warm-up excluded, monotonic clock, dispersion) resolves NB-6.
- **(iii) Load-bearing coupling (new):** the candidate's coordinates must be consumed by a downstream consumer that measurably degrades under ablation. This is the integrative replacement — "moving origin" has meaning where coupling, not answers, is. It is a miniature of the L15 test (M5 applies in full). It is satisfiable (the toy consumer uses `coord_cycle_relative`, which the candidate re-resolves; the frozen-origin ablation freezes it) and genuine (it catches a candidate whose coordinates are correct and operationally distinct but consumed by nothing — "a cache with a philosophy").

### 12.3 Rebecca's authority

Rebecca's E1 gate ruling (2026-08-15) exercises:
- The **constitution-change authority** (the L4 test is revised herein — the informational collapse test is retired; the three-property test is installed).
- The **second-reader clause** reserved for E1's equivalence test (M0 decision sheet §F item 2: "E1 result routes through the designing assistant before the M3 gate. Not as authority — as a second reader. E1's equivalence test is subtle... a second interpretation before you sign the continuation gate is cheap insurance."). The second-reader clause existed for exactly this seam, and the seam held.
- The **Persistence Doctrine authority** (§3 of the ruling: Candidate 1.1 is NOT charged as a death; the diagnosed cause is attributed to the TEST, not the candidate or the idea; no retry budget consumed).
- The **specification-completion authority** (Q2: the 0.5 slope-ratio trigger replaced; Q3: NB-3 promoted to required-before-build, degradation magnitude reported; NB-5 resolved; NB-4 accepted for E1 scope; NB-6 resolved by timing methodology). These are specification completions within the approved v3 structure, NOT a new revision cycle — Rebecca ruled that no third full review cycle is required.

### 12.4 Credit and standing note (Rebecca ruling §5, verbatim intent)

Nobody in this exchange did anything wrong. The ARCHITECT derived the hard fact (any coordinate that is a deterministic function of logged inputs is computable by a baseline holding the same inputs) and documented the swerve (restricting the naive arm's inputs) transparently — which is the only reason it was catchable at paper cost. The CRITIC's B1/B5 was correct and is now fully honored rather than routed around. The second-reader clause existed for exactly this seam, and the seam held. Revise, and bring it back through the cycle.

---

*Spec ends (v3 + Rebecca Q2/Q3 incorporations). These incorporations are specification completions within the approved v3 structure — NOT a new revision cycle (Rebecca ruled no third full review cycle is required). The CRITIC verifies the incorporations; the timebox clock starts when the CRITIC clears them (§10.2).*
