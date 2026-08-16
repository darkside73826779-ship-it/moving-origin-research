# M3 / E2 SPECIFICATION — AMENDED DRAFT v4

**Serves: Rebecca's M3 Continuation/Scope Gate**
**Status: AMENDED DRAFT — requires CRITIC re-review; no build authorization**

**Date:** 2026-08-15 · **Author:** ARCHITECT · **Governing state:** main `1626bb09d9645ccdf2a2126325b2934dc12e2c5d`; M2 GREEN/SEALED/ACCEPTED; M3 scope-spec cycle active, no build authorization, no timebox.
**Authority chain:** Rebecca > constitution (`ARCHITECTURAL_CONSTITUTION.md`) > M0 decision sheet as adopted (`M0_DECISION_SHEET.md` + `REBECCA_RESPONSE_M0.md`) > this specification > agent judgment.
**Prior reviews:** `critic_m3_scope_review.md` — BLOCK, B1–B10 + NB1–NB5, against `m3_scope_proposal.md` (v0). `critic_m3_e2_spec_rereview.md` — BLOCK, RB1–RB8 + 5 non-blocking notes, against `m3_e2_spec_amended.md` (v1). `critic_m3_e2_spec_rereview_v2.md` — BLOCK, C1–C8 + NB1–NB3, against `m3_e2_spec_amended_v2.md` (v2). `critic_m3_e2_spec_rereview_v3.md` — BLOCK, F1–F7 + NF1–NF6, against `m3_e2_spec_amended_v3.md` (v3). This document is the fourth resubmission. Every F finding is resolved below, with real arithmetic (verified by direct computation, not asserted), and mapped exhaustively alongside every prior B/RB/C/F/NB item in the companion changelog `m3_e2_spec_changelog_v4.md`.
**Role boundary (unchanged):** The ARCHITECT proposes specification, bars, and sequencing only. No code, no execution, no mechanism implementation. This document does not itself authorize a build cell, a timebox, or any courier run. Scope-gate clearance (this document, if CRITIC-cleared and Rebecca-approved) is a **separate** decision from build/task-spec clearance (a later, distinct ARCHITECT/INTEGRATOR deliverable).

---

## 0. What changed in v4 and why

The CRITIC's fourth review (`critic_m3_e2_spec_rereview_v3.md`) found v3's governance framing sound and confirmed resolution of C1, C3, C4, C7, and NB1–NB3, but returned **BLOCK** on seven fresh findings (F1–F7) introduced by v3's own C-fixes, plus six non-blocking notes (NF1–NF6). This revision:

1. **Re-registers the L1 tie-break as a seeded random permutation** (the M1 B2 precedent), replacing the creation-cycle tie-break that was a perfect age proxy, and re-derives the frozen and fair-naive empirical nulls from each arm's own data-generating process — the frozen arm's observed R² (0.236) now falls well below the null 95th percentile (0.749), so both negative controls are valid instead of cornered (§2.4, §2.8, §2.9, resolves F1).
2. **Decorrelates the within-bin rehearsal assignment** from `⌊i/8⌋` (perfect age lockstep) to `i mod 5` (interleaved), recomputing conditional expectations: a factor-inert candidate (β=0) now shows within-bin Spearman ρ < 0.6 for all 5 bins (0.20, 0.24, 0.20, 0.18, 0.13), so the rehearsal-isolation test correctly fails when the property is absent (§2.2, §2.6, resolves F2).
3. **Specifies exact bounds, artifacts, and failure consequences for the recency-only and rehearsal-only ablation arms** — recency-only: R² ≥ 0.85, β_age < 0, all 5 ρ < 0.6 (verified: R²=0.926, β_age=−0.00229); rehearsal-only: β_age ≥ 0, all 5 ρ ≥ 0.6 (verified: β_age=0.0005, ρ=0.97–0.98) — closing the §2.11 PASS-branch gap that referenced non-existent §2.9 bounds (§2.8, §2.9, §2.10, §2.11, resolves F3).
4. **Pre-registers the exact candidate-set count (100), per-entry appearance count (exactly 5 per entry), and per-entry aggregation rule** (mean of log-transformed per-set accessibilities), and verifies by direct computation that the oracle achieves R² = 0.985 ≥ 0.85 with β_age = −0.00150 < 0 under those rules (§2.4, §12.1a, resolves F4).
5. **Re-specifies the L5 frozen arm with an Option-E-grade definition** — a head/current-belief pointer that genuinely requires update on supersession, pre-registered chain-append timeline (pre-freeze: nodes (c,0)–(c,4) at cycles 0–99; freeze at cycle 100; post-freeze: nodes (c,5)–(c,9) at cycles 100–199), post-freeze query subset (all 40 queries), and derived outcome (walk accuracy = 0.00 for all post-freeze queries, by construction) (§4.5, §4.7, §4.8, resolves F5).
6. **Corrects the L5 shuffled-chain edge count from 190 to 180** (20×9=180), states the derangement expectation as exactly 0 (no fixed points by definition), and fixes the bound to a single criterion (deterministic: walk accuracy = 0.00 ≤ 0.05) (§4.8, §12.4, resolves F6).
7. **Reconciles the L6 callable count to 4 everywhere** — the enumeration is 2+0+2=4, and every reference to "five" or "5 rows" is corrected to "four" or "4 rows" (§5.3, §5.6, resolves F7).
8. **Addresses NF1–NF6** in the same pass: harmonizes L3 frozen-floor scope (NF1, §3.9); narrows the seed-ledger completeness claim to "E1 and M3 seed-use events" and notes M1's non-M3 seed usage (NF2, §8.1); notes STATE.md staleness as an INTEGRATOR responsibility (NF3, §11); adds batch-fallback timing language to §2.5 and §4.4 (NF4); states world-validity-only scope for the fair-naive 75% artifact (NF5, §4.8, §4.9); states the chain-fixture log separation explicitly (NF6, §4.5, §4.8).

**Everything not named above is unchanged from v3** and remains resolved as previously mapped. The CRITIC identified the following as surviving adversarial re-derivation and correct as written: §2.1's unique-cycle timeline arithmetic (as a timeline; F2 changes only the level assignment rule); §3.1–§3.7 in full; §4.1–§4.3 and §4.5's graph/bypass registration (graph structure unchanged; F5 adds the head-pointer mechanism and append timeline, F6 corrects the count only); §5.1–§5.2 and §5.4–§5.5's arm transforms; §6; §8's pools and protections; §9; §10; §11; and §12's checks 12.1–12.4 and 12.6–12.9 (12.5 updated for F3).

---

## 1. Bar table — M0-adopted values restored verbatim (unchanged from v1/v2)

| Law | M0-adopted bar (verbatim, restored) | Source |
|---|---|---|
| **L1 — decay** | Fitted decay curve, direction negative, **R² ≥ 0.85** over pre-registered binned item ages. | `M0_DECISION_SHEET.md` §B (L1 row); adopted `REBECCA_RESPONSE_M0.md` §2 |
| **L1 — rehearsal** | **Spearman ρ ≥ 0.6** between rehearsal count and access, **consistent sign across all scoring seeds**. | Same |
| **L1 — newest/oldest 2×** | **DROPPED as a bar.** Reported statistic only — never a kill condition, never a pass/fail gate. | Same; explicit drop confirmed in `REBECCA_RESPONSE_M0.md` §2 bullet 2 |
| **L3 — margin** | **≥ 5% relative reduction** in prediction loss, state-alone vs. raw-input-alone, **at every horizon 1..H**, H = 5 cycles. | `M0_DECISION_SHEET.md` §B (L3 row); adopted |
| **L5 — four-combination accuracy** | Query accuracy **≥ 0.95** on all four bi-temporal combinations. | `M0_DECISION_SHEET.md` §B (L5 row); adopted |
| **L5 — chain-walk** | k ≤ 10, walk accuracy **= 1.00**. | Same |
| **L18 battery** | Empty / permuted / shuffled / oracle / fair-naive / frozen, fully enumerated, on every positive claim. | `M0_DECISION_SHEET.md` §E; `STATE.md` locked_bars_and_standing_rules |
| **Seeds (non-p<.05 laws)** | **3 seeds** minimum for laws without a p<.05 bar (L1, L3, L5, L6 are in this class at M3). | `M0_DECISION_SHEET.md` §B, "Inferential policy" row |
| **Hold-out policy** | **≥ 2 scoring seeds unseen in development**, per the standing rule already governing E1. | `STATE.md` `locked_bars_and_standing_rules.future_scoring`; carried from E1's R3 |

**No M3 kill condition, floor, or pass bar in this document is lower, higher, renamed, or reinterpreted relative to this table.**

### 1.1 Discrete proposed amendment (unchanged from v2, per RB4/NB2/NB3)

- **(a) No M0-adopted value is being challenged** — L5's ≥0.95 accuracy and =1.00 chain-walk bars remain exactly as adopted (§1, table above; used unchanged in §4).
- **(b) Proposed new value (not previously adopted by M0):** an L5 chain-walk *scan-avoidance operational bar* — candidate per-walk latency growth from 250-entry to 1000-entry history ≤ 2.0×, on a battery whose fair-naive full-scan comparator is validated to show ≥ 4.0× growth over the same range.
- **(c) Rationale:** M0 adopted the *accuracy* bars for L5 but did not adopt a numeric scan-avoidance operational bar for L5 specifically — v1 incorrectly treated E1's L4 latency-growth thresholds as if M0 had already locked them for L5 by inheritance. They have not been ruled on for L5. The proposed values reuse E1's already-validated numeric structure (not an arbitrary new number) because that structure has a working battery-validity precedent, but the reuse itself is a new proposal, not an inherited lock.
- **(d) CRITIC's independent assessment:** NB2 (v2 review) confirms this proposal is "appropriately isolated" and "narrow enough to be decided at this gate," while noting it does not cure C5. C5 is resolved independently in §4.5–§4.6 below; this proposal is unaffected by that resolution and remains presented for CRITIC assessment and Rebecca's ruling, unchanged.
- **(e) Rebecca's ruling:** pending. **Until ruled, the growth-threshold check in §4.4 is diagnostic-only and does not gate the L5 verdict** (see §4.9's verdict branches, which gate solely on the M0-adopted accuracy/chain-walk bars unless and until this proposal is accepted).

---

## 2. L1 — Access physics: complete test matrix (creation-phase fixture rebuilt per C1; candidate sets and R² test rebuilt per C2; downstream-consumer test deleted per C7; L18 arms rebuilt per C8)

### 2.1 Corrected timeline: unique-cycle creation with age BINS spanning cycle ranges (resolves C1)

**v2's defect:** the creation phase declared 1,000 one-append-per-cycle appends while placing 40 factorial entries at each of only 5 creation cycles — requiring 40 appends in a single cycle, and leaving 995 (not 960) cycles for filler. This is rebuilt from the cycle level up.

**Corrected design — every one of the 1,000 creation-phase appends occupies its own unique cycle:**

1. **Creation phase — cycles 0 to 999 (1,000 appends, one per cycle, no exceptions).**
2. **5 age bins, each a contiguous 200-cycle range of the creation phase:** bin 0 = cycles [0, 199]; bin 1 = [200, 399]; bin 2 = [400, 599]; bin 3 = [600, 799]; bin 4 = [800, 999]. These are the "pre-registered binned item ages" referenced by M0's bar (§1) — a bin is a range of distinct creation cycles, not a single shared cycle.
3. **Within each bin, exactly 40 of the bin's 200 cycles are pre-registered measured-entry creation cycles; the remaining 160 are filler-entry creation cycles.** The measured cycles within bin `b` (bin start `lo_b`) are `{lo_b + 5·i : i = 0..39}` — a fixed, deterministic, pre-registered stride-5 selection, not chosen after seeing data. Example: bin 0's measured cycles are {0, 5, 10, ..., 195}; bin 4's are {800, 805, ..., 995}. Every other cycle in the bin's range is a filler-entry creation cycle.
4. **Arithmetic (verified by direct enumeration, not asserted):** 40 measured cycles/bin × 5 bins = **200 measured entries**, each at its own unique cycle. 160 filler cycles/bin × 5 bins = **800 filler entries**, each at its own unique cycle. `200 + 800 = 1000` creation-phase appends, matching the 1,000-cycle creation phase exactly, with **zero cycles shared by two appends**. See §12.1 for the full sanity table.
5. **Priming phase — cycles 1000 to 2199 (exactly 1,200 appends, one per cycle, no exceptions).** Rehearsal-increment events for the 200 measured entries are appended in this phase only (§2.3). Total count: 5 bins × Σ(rehearsal targets {0,2,4,8,16}) × 8 replicates-per-(bin,target) = 5 × 30 × 8 = **1,200**, filling cycles 1000–2199 exactly. **No other event type is appended during the priming phase.**
6. **Final scoring cycle — `now_final = 2200`, fixed by construction** (1000 creation + 1200 priming). Every accessibility measurement (§2.4) is taken at this single cycle.
7. **Final autobiography size at scoring = 2,200 entries** (one append per cycle 0–2199, L2's unchanged cadence rule).
8. **Final age per measured entry:** `age(e) = now_final − creation_cycle(e) = 2200 − creation_cycle(e)`. Because every measured entry now has a unique creation cycle, every measured entry also has a unique final age. **Per-bin age ranges at `now_final=2200`** (verified by direct computation): bin 0 → ages [2005, 2200]; bin 1 → [1805, 2000]; bin 2 → [1605, 1800]; bin 3 → [1405, 1600]; bin 4 → [1205, 1400]. These five ranges are contiguous and non-overlapping (bin 0's minimum age 2005 exceeds bin 1's maximum age 2000 by exactly 5, matching the stride-5 selection), so **bin membership by cycle range is identical to bin membership by final-age range** — no entry's age falls in a different bin's stated range than its creation-cycle bin.

### 2.2 Factorial design: age bin × rehearsal, balanced cells within each bin (updated to decorrelated within-bin assignment per F2)

**v3's defect (F2):** the within-bin assignment used `⌊i/8⌋`, which assigned rehearsal level in ascending cycle order within each bin — level-0 entries were always the 8 oldest and level-4 always the 8 youngest, perfectly confounding rehearsal level with age within every bin and making the rehearsal-isolation test unable to fail for a factor-inert candidate.

**Corrected design — interleaved assignment that decorrelates rehearsal from age within each bin:**

- **Age-bin factor:** 5 levels (bins 0–4 per §2.1), each entry's bin determined by its unique creation cycle's bin membership.
- **Rehearsal factor:** 5 levels — rehearsal-target counts {0, 2, 4, 8, 16} — realized as actual priming-event counts per entry during the priming phase.
- **Within-bin assignment (F2 fix):** the 40 measured cycles of bin `b`, in ascending cycle order, are assigned rehearsal level `i mod 5` for the `i`-th cycle (`i = 0..39`) — giving exactly 8 entries (the 8 replicates) at each of the 5 rehearsal levels, per bin. Under this interleaving, each rehearsal level's 8 entries span the full 195-cycle range of the bin (e.g., level 0 occupies cycles `lo_b + 0, lo_b + 25, lo_b + 50, ..., lo_b + 175`; level 4 occupies `lo_b + 20, lo_b + 45, ..., lo_b + 195`), so the within-bin Spearman correlation between rehearsal level and creation cycle is **−0.1225** (equivalently +0.1225 with age) — weak, not the perfect +1.0 with creation cycle (equivalently −1.0 with age) under v3's `⌊i/8⌋`. **Factorial cross: 5 age bins × 5 rehearsal levels = 25 cells, 8 entries per cell, 200 entries total** — unchanged cell structure. This assignment is deterministic and pre-registered.
- **Consequence (verified by direct computation, §12.1a):** a candidate whose rehearsal machinery is entirely inert (effective β = 0, ranking by `exp(−λ·age)` alone) now shows within-bin Spearman ρ < 0.6 for all 5 bins (observed: 0.20, 0.24, 0.20, 0.18, 0.13), so the rehearsal-isolation test (§2.6) correctly fails when the property it gates is absent — closing F2's broken-bar defect. The oracle candidate (true β = 0.5) shows ρ ≥ 0.6 for all 5 bins (observed: 0.91–0.95), so the test correctly passes when the property is present.
- **Marginal-mean age curve and rehearsal-conditional age curves are not confounded** (each rehearsal level occupies the same relative position in every bin, and bin means are balanced) — the defect was specific to the rehearsal-isolation test, now fixed.

### 2.3 Rehearsal write mechanism (unchanged from v2, restated for continuity)

1. Query issued against entry `e` during the priming phase (cycles 1000–2199 only, §2.1).
2. Index returns `e` (a "hit").
3. If the query is a designated priming query (part of the fixed schedule), the system appends a rehearsal-increment event: `event_type = "rehearsal"`, `ref = e`, `cycle = now`. This advances `now` by exactly 1.
4. Rehearsal count for `e` = count of `rehearsal`-type events referencing `e`, read directly from the log.
5. Scoring-time queries (at `now_final = 2200` only) are read-only and never increment rehearsal.

### 2.4 Heterogeneous, stratified candidate sets with seeded random-permutation tie-break (resolves F1; pre-registers exact set count, appearance count, and aggregation rule per F4)

**v3's defect (F1):** the tie-break was ascending entry identifier (creation cycle), which in this fixture is a perfect age proxy — under the frozen arm (constant priority) the entire ranking was produced by the tie-break, making rank a deterministic monotone function of age and yielding R² = 0.926, which exceeds the 0.85 bar the arm exists to fail. The fair-naive arm ranked by "append order," which is creation-cycle order — maximally related to the age factor, not "unrelated to priority" as described.

**Corrected candidate-set design (unchanged structure; tie-break and fair-naive ordering redesigned):** each retrieval query presents a **fixed-size 10-entry candidate set stratified across age bins and heterogeneous in rehearsal level**, constructed as:

- **2 entries drawn from each of the 5 age bins** (stratified sampling, seeded, drawn from that bin's 40 measured entries at all 5 rehearsal levels — not restricted to one rehearsal level), for **10 measured entries per candidate set**, ages and rehearsal levels both varying within the set.
- No filler entries are needed in this design (unlike v2) because the 10-entry set is already heterogeneous by construction; the fixed-resource size (10) is unchanged.
- **Tie-break rule, pre-registered, genuinely label-independent (F1 fix, M1 B2 precedent):** if `priority(e)` ties exactly between two candidates (a measure-zero event given the fixed constants, but pre-registered to remove any possible undefined behavior), rank is broken by **a seeded random permutation of entry identifiers** (seed = 42, `numpy.random.RandomState(42).permutation(200)`), applied as the secondary sort key. This permutation is fixed before any data is generated, has no dependence on age, rehearsal, or the ground-truth label, and is distinct from the fair-naive arm's ordering permutation (§2.8, seed = 43). Under this tie-break, the frozen arm's observed R² (constant priority, all tie, ranking by tie-break) = **0.236**, well below the empirical-null 95th percentile (0.749, §2.9), so the frozen arm is a valid negative control instead of a corner.

**Exact candidate-set count, appearance count, and aggregation rule (F4 fix):**

- **Number of candidate sets: exactly 100 per scoring seed.** Each set contains 10 entries (2 per bin). Total entry-slots: 100 × 10 = 1,000.
- **Per-entry appearance count: exactly 5 per entry.** Construction: for each bin, create a pool of 200 entry indices (each of the 40 bin entries repeated 5 times), shuffle with a **fixed structural seed (777, outside all seed pools {42–46, 101–105, 201–203})**, and take consecutive pairs → 100 pairs per bin, each entry appearing exactly 5 times. Set `j` takes pair `j` from each of the 5 bins. This is a balanced design: every entry appears in exactly 5 sets, no entry is unobserved, and the minimum appearance count equals the maximum. **The same candidate-set schedule (generated with structural seed 777) is used for all scoring runs** — it is a fixture-design parameter, not a scoring-seed-dependent quantity, so the oracle satisfiability and null-distribution values verified in §12.1a are fixed and applicable to every scoring seed.
- **Per-entry aggregation rule:** for each entry `e`, `log_accessibility(e) = mean_{s ∈ sets(e)} log(11 − rank_s(e))`, where `sets(e)` is the set of 5 candidate sets in which `e` appears, and `rank_s(e)` is `e`'s rank (1 = most accessible) within set `s`. The binned marginal mean (§2.6) then averages `log_accessibility(e)` over all 40 entries in each bin. This is the **mean of log-transformed per-set accessibilities** — pre-registered as the single binding rule; the oracle satisfiability (below) is verified under this exact rule.
- **Oracle satisfiability (verified by direct computation, §12.1a):** under these exact rules, the oracle (ground-truth `priority(e)`) achieves **R² = 0.985** (≥ 0.85) with **β_age = −0.00150** (< 0) over the 5 binned marginal-mean points — the M0-adopted bar is met, and the curvature risk F1 identified (successive bin-mean drops of 0.24, 0.31, 0.46, 0.90 in the deterministic case) is not present under the oracle's two-factor ranking because rehearsal variation within each candidate set prevents the extreme rank compression that produced it.

### 2.5 Accessibility metric, tied to a fixed-resource retrieval operation (unchanged mechanism from v2, now operating on the heterogeneous sets of §2.4)

**Candidate retrieval operation:** `retrieve(query_id) → e`, a single call to the autobiography's content-addressed index (a hash map keyed by entry identifier; no priority queue, cache warm state, or age/rehearsal-dependent branch in the lookup path itself). Accessibility is **not** raw lookup latency (O(1), age/rehearsal-independent by construction); it is the entry's **retrieval-queue rank** under the fixed 10-entry candidate set (§2.4), computed by:

`priority(e) = exp(−λ · age(e)) · (1 + β · log(1 + rehearsal(e)))`, with `λ = 0.001`, `β = 0.5` fixed pre-registered constants (chosen only to guarantee strict monotonicity in each factor, fixed before any data is generated).

**Fixed-resource retrieval task:** the retrieval operation returns the 10-entry candidate set **ordered by `priority(e)` descending** (ties broken per §2.4), using a fixed-budget partial sort (`k`-selection over exactly 10 items, no early exit, no caching, `time.perf_counter_ns()`, median over ≥100 repetitions, warm-up excluded). **Batch-fallback for sub-clock-resolution operations (NF4 fix, inheriting E1-RUN-1's construction-bug fix, Entry 34/commit `dceb2584`):** if the median per-operation elapsed time is below the timer's documented resolution (empirically < ~100 ns on the executor hardware), the timing loop batches `B` consecutive operations (starting at `B=100`, doubling until the batch median exceeds 10× the timer resolution) and reports `median_batch_time / B` as the per-operation estimate, with `B` logged in the artifact. This prevents the identical sub-resolution measurement error that forced E1-RUN-1's crash on Windows. **Accessibility is the entry's rank position in this sort** (rank 1 = most accessible).

**Oracle:** the fixture's own generative `priority(e)` function, computed directly from ground-truth `age(e)` and `rehearsal(e)`, applied to the same 10-item candidate sets.

**Equal-resource rule across all arms:** every arm (§2.8) ranks the identical candidate sets, identical timing methodology, identical repetition count, warm-up treatment, and resource budget.

**Metric used in the fit (§2.6):** `accessibility(e) := 11 − rank(e)`, log-transformed as `log(accessibility(e))`.

### 2.6 Age-specific binned marginal-mean curve implementing the M0-adopted R² bar, plus rehearsal-controlled conditional tests (resolves C2's second defect)

**v2's defect:** gated a joint age-plus-rehearsal OLS model's total R², which a high rehearsal contribution can drive independently of age's own contribution — not the same test as M0's adopted decay curve over pre-registered binned item ages.

**Corrected primary test — balanced marginal-mean binned-age curve (this is the M0-adopted R² bar, restored exactly, not reinterpreted):**

1. For each of the 5 age bins, compute the **balanced marginal mean** of `log(accessibility(e))` across all 40 measured entries in that bin — averaging over all 5 rehearsal levels equally (8 entries per rehearsal level per bin, so the mean is already balanced by construction; no reweighting needed).
2. Fit `mean_log_accessibility(bin) = β₀ + β_age · age_bin_representative(bin) + ε` by OLS over these **5 balanced marginal-mean points** (one point per age bin), where `age_bin_representative(bin)` is the bin's mean final age (computable exactly from §2.1's per-bin age ranges).
3. **Pass condition (this is the literal M0-adopted bar, §1): `β_age < 0` (negative direction) AND R² ≥ 0.85**, computed over these 5 binned, rehearsal-balanced points — not the 200-entry joint total R², and not a per-cell mean. Because each bin's marginal mean already averages equally across all 5 rehearsal levels, rehearsal's contribution to between-bin variation is structurally removed before the R² is computed, directly closing C2's "high total R² can be driven by rehearsal" finding.

**Rehearsal-controlled conditional tests (unchanged in spirit from v2, retained as a separate, non-substitute test; F2 fix verified):**

- **Age effect holding rehearsal fixed:** for each of the 5 rehearsal levels separately, fit `log(accessibility(e)) = β₀ + β_age · age(e) + ε` over the 5 age-bin means at that rehearsal level (5 conditional curves, 5 points each, using each entry's exact numeric age, not a bin label). **Pass condition:** all 5 conditional curves show a negative slope.
- **Rehearsal effect holding age fixed:** for each of the 5 age bins separately, compute the Spearman correlation between `rehearsal(e)` and `accessibility(e)` over the 40 entries in that bin (8 entries at each of 5 rehearsal levels, correlation over all 40 individual observations). **Pass condition:** all 5 conditional ρ values ≥ 0.6 with consistent positive sign — the M0-adopted rehearsal bar (§1), applied within each age bin.
- **F2 consequence (verified by direct computation, §12.1a):** under the decorrelated `i mod 5` within-bin assignment (§2.2), the oracle candidate shows ρ ≥ 0.6 for all 5 bins (0.91–0.95), while a factor-inert candidate (β=0, age-only priority) shows ρ < 0.6 for all 5 bins (0.20, 0.24, 0.20, 0.18, 0.13) — the test now correctly distinguishes presence from absence of the rehearsal effect, closing F2's broken-bar defect.

**Joint model retained as a secondary, non-substitute diagnostic only:** the two-factor OLS fit from v2 (`log(accessibility(e)) = β₀ + β_age·age(e) + β_reh·log(1+rehearsal(e)) + ε` over all 200 entries) is still computed and reported, with its own `β_age<0 AND β_reh>0` sign check, but **its R² is never used to satisfy the M0-adopted bar** — only §2.6's balanced marginal-mean curve does that. This removes C2's reinterpretation while keeping the joint model's genuinely useful sign-consistency information as a reported diagnostic.

### 2.7 Bin-sensitivity sweep (unchanged from v2)

Because the fixture uses 5 discrete, exactly-controlled age bins by construction (§2.1) rather than a continuously-drawn age distribution, no 7-bin or 10-bin re-binning sweep is proposed (unchanged rationale from v2, itself resolving RB2). The only sensitivity check retained is the conditional-vs-marginal agreement check: the balanced marginal-mean curve's `β_age` sign (§2.6) and the 5 rehearsal-conditional age-curves' signs (§2.6) must agree (all negative); a disagreement is a logged diagnostic note, not a separate gating bar.

### 2.8 Arms (L1) — updated to heterogeneous candidate sets, corrected ages, and C8-compliant perturbations

| Arm | Definition | What is perturbed | What is held fixed |
|---|---|---|---|
| Candidate | Full `priority(e)` function (§2.5), both factors live, heterogeneous stratified candidate sets (§2.4), final ages/rehearsal per §2.1–§2.3 | Nothing (this is the positive claim) | Everything |
| Frozen (uniform priority) | `priority(e) = constant` for all `e` | The priority function itself, replaced by a constant | Candidate-set composition, timing methodology |
| Recency-only ablation | `priority(e) = exp(−λ·age(e))` only, rehearsal term removed | The functional form (rehearsal term deleted) | Age term, candidate sets, timing |
| Rehearsal-only ablation | `priority(e) = 1 + β·log(1+rehearsal(e))` only, age term removed | The functional form (age term deleted) | Rehearsal term, candidate sets, timing |
| Oracle | Ground-truth `priority(e)` from the fixture generator directly | Nothing (uses true values) | Everything |
| Fair-naive | Reads the same full event log (including rehearsal events) but ranks by a **seeded random permutation of entry identifiers** (seed = 43, independent of the tie-break seed = 42 in §2.4), genuinely unrelated to priority, age, rehearsal, or the ground-truth label — replacing v3's "append order" which was creation-cycle order and therefore a perfect age proxy (F1 fix, M1 B2 precedent) | The ranking rule (priority replaced by random permutation); age/rehearsal values themselves are untouched and still readable | The candidate-set composition and all age/rehearsal values in storage |
| Permuted | The **mapping from entry identity to (age, rehearsal) value** is permuted across the 200 measured entries **before the fit is computed**, so the fit consumes each entry's *reassigned* age/rehearsal pair while the true rank-determining values used to build the candidate sets are the ORIGINAL (unpermuted) ones — this breaks the predictor-to-label correspondence, per C8, rather than permuting both together | The (age, rehearsal) → entry mapping used for the FIT only; candidate-set membership and true priority values used at retrieval time are untouched | The retrieval mechanism itself, the candidate-set composition |
| Shuffled | The **priming schedule's query-to-entry assignment** is shuffled independently of the pre-registered age-bin/rehearsal-level design, so realized rehearsal counts no longer match any entry's intended target — but the FIT reads the (now-decorrelated) realized rehearsal counts, and age is untouched | Which entries receive which priming queries (realized rehearsal decorrelates from intended design) | Age assignment, candidate-set composition, retrieval mechanism |
| Empty | No entries in the factorial fixture | The entire fixture (zero entries) | N/A |

**Permuted vs. shuffled remain two distinct arms** (unchanged from v2) but are now specified, per C8, to break correspondence at the fit-input level rather than leaving both the ranking function and the fit consuming an identically-relabeled value (v2's defect: permuting age/rehearsal values that both the priority formula and the fit still consumed identically guarantees no collapse). Under this corrected design, permuted decouples the FIT's inputs from the true retrieval-time values that generated the observed ranks, so the fit's `β_age`/`β_reh` estimates are computed against mismatched labels and must degrade.

### 2.9 Exact expected statistic, empirical-null derivation, and instrument-failure consequence per L18 arm (resolves F1, F3, F1a; C8-compliant)

| Arm | Exact expected statistic / bound | Artifact fields | Instrument-failure consequence if arm behaves otherwise |
|---|---|---|---|
| Frozen | Balanced marginal-mean R² (§2.6) computed on constant-priority ranks: all 10 candidates in each set tie, so the entire ranking is produced by the seeded random-permutation tie-break (§2.4, seed=42). **Observed R² = 0.236** (verified by direct computation, §12.1a). **Empirical null:** 1,000 seeded reassignments of the tie-break permutation (independent of the true identifier-to-age mapping), computing R² for each: null mean = 0.244, null SD = 0.246, **null 95th percentile = 0.749**. **Pass condition for the frozen arm to count as a valid negative control: observed frozen R² ≤ empirical-null 95th-percentile bound (0.236 ≤ 0.749 ✓).** | `{arm:"frozen", r_squared_observed, empirical_null_1000_values, null_95th_pct, pass}` | Frozen R² > empirical null 95th percentile (0.749): INSTRUMENT FAILURE (the tie-break or fixture leaks age information even under a constant priority) |
| Fair-naive | Same empirical-null procedure as frozen, applied to the seeded random-permutation ranking (§2.8, seed=43). **Observed R² = 0.320** (verified, §12.1a). **Pass condition: observed fair-naive R² ≤ empirical-null 95th-percentile bound (0.320 ≤ 0.749 ✓).** | `{arm:"fair_naive", r_squared_observed, null_95th_pct, pass}` | Fair-naive R² > empirical null bound: INSTRUMENT FAILURE |
| Recency-only | `priority(e) = exp(−λ·age(e))` only (rehearsal term removed, §2.8). **Isolation criterion — age bar still met, rehearsal effect absent:** R² ≥ 0.85 AND β_age < 0 (age bar met with rehearsal removed) AND all 5 within-bin conditional ρ < 0.6 (rehearsal effect absent since rehearsal was removed from the priority function). **Verified by direct computation (§12.1a): R² = 0.926, β_age = −0.00229, all 5 ρ < 0.6 (0.20, 0.24, 0.20, 0.18, 0.13).** | `{arm:"recency_only", r_squared, beta_age, conditional_rho[5], all_rho_below_06}` | R² < 0.85 OR β_age ≥ 0 (age doesn't produce decay alone — priority function broken): INSTRUMENT FAILURE; OR any ρ ≥ 0.6 (rehearsal still shows effect despite being removed — fixture leaks rehearsal information): INSTRUMENT FAILURE |
| Rehearsal-only | `priority(e) = 1 + β·log(1+rehearsal(e))` only (age term removed, §2.8). **Isolation criterion — age bar not met, rehearsal effect present:** β_age ≥ 0 (age direction not negative → age bar not met, since age was removed from the priority function) AND all 5 within-bin conditional ρ ≥ 0.6 (rehearsal bar met with age removed). **Verified by direct computation (§12.1a): β_age = 0.0005 (≥ 0, not negative), all 5 ρ ≥ 0.6 (0.97–0.98).** Note: R² may be high (observed 0.996) due to low between-bin variance when accessibility depends only on rehearsal, but R² is not the criterion for this arm — the direction of β_age is. | `{arm:"rehearsal_only", beta_age, r_squared, conditional_rho[5], all_rho_above_06}` | β_age < 0 (age still drives decay despite being removed — fixture leaks age information): INSTRUMENT FAILURE; OR any ρ < 0.6 (rehearsal doesn't drive accessibility alone — priority function broken): INSTRUMENT FAILURE |
| Permuted | Fit computed on the permuted (age,rehearsal)→entry mapping (§2.8). **Empirical null derived from the permuted arm's OWN permutation distribution** (F1a fix — not borrowed from the frozen/fair-naive null): 1,000 seeded permutations of the (age,rehearsal)→entry mapping, computing the binned marginal-mean R² for each. Null mean = 0.255, null SD = 0.255. **Pass condition: permuted R² within [null_mean − 2·null_sd, null_mean + 2·null_sd] = [−0.255, 0.764].** Observed permuted R² = 0.000, within band ✓. | `{arm:"permuted", r_squared_observed, null_mean, null_sd, within_band}` | Permuted R² exceeds the band upper bound (0.764): INSTRUMENT FAILURE — permutation did not sever the predictor-label correspondence |
| Shuffled | Realized rehearsal counts decorrelate from the age-bin/rehearsal-level design (§2.8). **Empirical null:** 1,000 seeded random re-assignments of priming queries to entries, computing the 5 conditional ρ values for each. **Pass condition: all 5 conditional ρ values within [null_mean − 2·null_sd, null_mean + 2·null_sd]** of the shuffled-ρ null distribution, i.e., not distinguishable from chance rehearsal assignment. Age-conditional tests (§2.6) are unaffected by this arm and must still pass, since age is untouched. | `{arm:"shuffled", conditional_rho_values[5], null_mean, null_sd, within_band, age_tests_pass}` | Any shuffled ρ falls outside the band (i.e., still shows real signal): INSTRUMENT FAILURE — shuffling did not sever rehearsal's realized-to-intended correspondence |
| Oracle | Exact: `β_age<0`, R²≥0.85 (§2.6, same bar as candidate, met by construction with ground-truth values), all 5 conditional tests pass, all 5 conditional ρ≥0.6. **Verified: R² = 0.985, β_age = −0.00150, all ρ = 0.91–0.95 (§12.1a).** | `{arm:"oracle", r_squared, beta_age, conditional_pass[5], rho_values[5]}` | Any oracle test fails: INSTRUMENT FAILURE (fixture-construction defect, since oracle must pass by definition) |
| Empty | `retrieve()` on an empty fixture returns a defined error/empty result, not a silently-computed statistic | `{arm:"empty", returned_defined_error:true}` | Empty arm returns any non-error numeric result: INSTRUMENT FAILURE |

**No "≈" or "toward" language appears in any pass/fail condition above** — every arm's criterion is an exact numeric bound or an explicitly derived empirical-null percentile/band, per C8's explicit instruction and per O-13's requirement to use empirical null distributions when chance is not analytically exact. The permuted arm's null is now derived from its own permutation distribution (F1a fix), not borrowed from the frozen arm's tie-break-reassignment null.

### 2.10 Full L18 battery checklist for L1 (updated to include recency-only and rehearsal-only ablation arms per F3)

| Control | Present in §2.8? | Exact pass condition (§2.9) |
|---|---|---|
| Empty | Yes | Defined error, not a numeric result |
| Permuted | Yes | R² within permuted-arm own-empirical-null band [−0.255, 0.764] |
| Shuffled | Yes | All 5 conditional ρ within shuffled-empirical-null band |
| Oracle | Yes | R²≥0.85, β_age<0, all conditional tests pass (verified: R²=0.985) |
| Fair-naive | Yes | R² ≤ empirical-null 95th percentile (verified: 0.320 ≤ 0.749) |
| Frozen | Yes | R² ≤ empirical-null 95th percentile (verified: 0.236 ≤ 0.749) |
| Recency-only | Yes | R² ≥ 0.85 AND β_age < 0 AND all 5 ρ < 0.6 (verified: R²=0.926, β_age=−0.00229) |
| Rehearsal-only | Yes | β_age ≥ 0 AND all 5 ρ ≥ 0.6 (verified: β_age=0.0005, ρ=0.97–0.98) |

All six mandatory L18 controls plus two L1 factor-ablation arms (recency-only, rehearsal-only) are separately enumerated for L1's positive claim with exact, non-qualitative pass conditions, closing RB6/C8/F3 for this law.

### 2.11 Verdict branches (L1) — downstream-consumer condition deleted per C7

- **PASS:** balanced marginal-mean curve conditions (§2.6) hold AND all 5 rehearsal-conditional age curves monotone-negative AND all 5 age-conditional rehearsal ρ ≥ 0.6 consistent-sign AND ablations isolate their factors (§2.8) per §2.9's exact bounds — recency-only: R² ≥ 0.85, β_age < 0, all 5 ρ < 0.6; rehearsal-only: β_age ≥ 0, all 5 ρ ≥ 0.6 — on all scoring seeds.
- **KILL:** any condition above fails on any scoring seed.
- **INSTRUMENT FAILURE:** frozen or fair-naive R² exceeds its empirical-null 95th-percentile bound (§2.9); OR permuted R² falls outside its empirical-null band; OR any shuffled conditional ρ falls outside its empirical-null band; OR recency-only R² < 0.85 OR recency-only β_age ≥ 0 OR any recency-only ρ ≥ 0.6 (§2.9); OR rehearsal-only β_age < 0 OR any rehearsal-only ρ < 0.6 (§2.9); OR the empty arm returns a defined non-error numeric result; OR the priming phase does not consume exactly 1,200 cycles (§2.1); OR any measured entry's creation cycle collides with another entry's creation cycle (a fixture-construction defect, checkable in advance per §2.1's derived, unique cycle list, §12.1).
- **Reported-only (never gates):** newest/oldest ratio (M0-dropped); the joint two-factor model's R² (§2.6, retained as a diagnostic only, never substitutes for the marginal-mean curve).
- **Deleted from this document (per C7):** the §2.9-numbered downstream-consumer test present in v2 (v2 §2.9, reused E1's additive-relevance consumer) is **removed entirely**. It is not reproduced with a fuller specification; it is deleted from both this section and from E2 scope, per the mail's explicit instruction that "safest is delete them." No PASS, KILL, or INSTRUMENT FAILURE branch for L1 depends on any downstream consumer's behavior in this document.

---

## 3. L3 — Thick present: complete test matrix (window disjointness rebuilt per C3; L18 arms rebuilt per C8)

### 3.1 Synthetic task and generator (extended sequence length per C3)

**Generator:** seeded AR(3) process, `x[t] = 0.5·x[t-1] − 0.3·x[t-2] + 0.15·x[t-3] + 0.1·sin(t/23) + ε[t]`, `ε[t] ~ N(0, 0.05)`, 8-dimensional. **Task horizon:** H = 5 cycles, scored independently at every horizon 1..5. **Sequence length, corrected per C3: `N_total = 1010` cycles generated per scoring seed** (t = 0..1009) — extended from v2's 1,000 to supply sufficient trailing cycles for evaluation-window targets at every horizon (§3.4).

### 3.2 Frozen state update function `f` (unchanged from v2)

- **State dimension:** `s[t] ∈ R^16`, fixed.
- **Allowed inputs to `f` at each step:** exactly `s[t-1]` and `x[t]`.
- **Exact update rule:** `s[t] = clip( A · s[t-1] + B · x[t], −C, C )`, where `A = blkdiag(A_1,...,A_8)`, each `A_i = [[0.9, 0.1], [0.0, 0.5]]`; `B ∈ R^{16×8}` routes channel `i` into block `i`'s first slot (`B[2i,i]=1.0`, else 0); `C = 10.0`; `s[0] = 0`.
- **Zero learned/fitted parameters** — `A`, `B`, `C` fixed before any data is generated.

### 3.3 Predictor classes, features, and fitting procedure (window boundaries corrected per §3.4; otherwise unchanged from v2)

**Two predictor classes, both closed-form linear OLS, fit identically:**

- **State-alone predictor:** features = `s[t] ∈ R^16`. `ŷ[t+1..t+5] = W_s·s[t] + b_s`, `W_s ∈ R^{40×16}`.
- **Raw-input-alone predictor:** features = `x[t] ∈ R^8`. `ŷ[t+1..t+5] = W_x·x[t] + b_x`, `W_x ∈ R^{40×8}`.

**Fitting procedure (frozen, per-seed, exact):** for a given scoring seed's generated 1,010-cycle sequence, `W_s,b_s` (respectively `W_x,b_x`) are estimated by OLS **solved once, using only fitting-window origins (§3.4)**. No iterative optimizer, no cross-seed parameter sharing, no early stopping. The fitted weights are frozen and applied unchanged to compute predictions and loss on that **same seed's** evaluation-window origins (§3.4). No weight reuse across seeds; no weights fit on a hold-out seed's own hold-out window using a different seed's parameters.

### 3.4 Disjoint fitting/evaluation origin and target windows, every horizon 1–5, exact counts (resolves C3)

**v2's defect:** fitting origins 0–699 with targets through t+5=704 overlapped the nominal evaluation window's own targets 700–704, and evaluation origins 700–999 required targets 1000–1004, beyond the 1,000-cycle generated sequence — a self-contradiction before scoring.

**Corrected windows (verified disjoint by direct set computation, §12.2):**

- **Fitting origins:** `t = 0..699` (700 origins).
- **Buffer (excluded from both origin sets, used only as fitting targets):** cycles 700–704 (5 cycles) — these are consumed as targets by the last fitting origins (`t=699` needs targets up to `699+5=704`) but are never themselves used as an origin in either window.
- **Evaluation origins:** `t = 705..1004` (300 origins) — begins strictly after the last fitting-target cycle (704), leaving a 1-cycle gap (705 > 704) that guarantees no evaluation origin's own cycle was ever used as a fitting target.
- **Sequence length required:** the last evaluation target is `1004 + 5 = 1009`; generating 1,010 cycles (t=0..1009, §3.1) exactly covers this with no shortfall and no unused surplus beyond what §3.1 already generates.

**Per-horizon observation counts (identical structure for every horizon, verified for h=1..5):**

| Horizon h | Fitting target range | Fitting obs. count | Evaluation target range | Evaluation obs. count |
|---|---|---|---|---|
| 1 | [1, 700] | 700 | [706, 1005] | 300 |
| 2 | [2, 701] | 700 | [707, 1006] | 300 |
| 3 | [3, 702] | 700 | [708, 1007] | 300 |
| 4 | [4, 703] | 700 | [709, 1008] | 300 |
| 5 | [5, 704] | 700 | [710, 1009] | 300 |

**Disjointness confirmed directly:** the union of all cycles used by the fitting window (origins ∪ targets, all horizons) is exactly {0, ..., 704}; the union of all cycles used by the evaluation window (origins ∪ targets, all horizons) is exactly {705, ..., 1009}. These two sets have **zero intersection** and their union is exactly {0,...,1009} minus nothing (fully accounted, no gap larger than the deliberate 1-cycle buffer boundary). This same origin/target rule is applied identically to the state-alone, raw-input-alone, oracle, and frozen predictors (§3.5, §3.7) — no arm receives a different window.

### 3.5 Oracle and raw comparator: capacity/feature bounds fixed (unchanged from v2, windows now corrected per §3.4)

- **Raw-input-alone comparator:** features = `x[t]` only, 8 features, fixed comparator for every scored margin.
- **Oracle:** features = fixed 3-lag window `[x[t], x[t-1], x[t-2]] ∈ R^{24}`, matching the generator's AR(3) order exactly. `ŷ_oracle[t+1..t+5] = W_o·[x[t],x[t-1],x[t-2]] + b_o`, fit by the identical OLS procedure on the identical fitting-window origins of §3.4.

### 3.6 Exact loss, aggregation, denominator, and zero-loss rules (unchanged from v2)

- **Per-channel, per-horizon loss:** `MSE_c,h = mean_t((ŷ_c,h[t] − y_c,h[t])²)` over the held-out evaluation window (§3.4), for channel `c∈{0..7}`, horizon `h∈{1..5}`.
- **Aggregation across channels only:** `MSE_h = mean_c(MSE_c,h)`, never pooled across horizons.
- **Relative loss reduction:** `reduction_h = (MSE_h^raw − MSE_h^state) / MSE_h^raw`, raw predictor's loss as the fixed denominator.
- **Zero-loss/degenerate-denominator rule:** if `MSE_h^raw=0` on any scoring seed, that seed/horizon combination is flagged, excluded from the reduction calculation, and logged as an instrument-failure note; a repeated occurrence across ≥2 scoring seeds at the same horizon escalates to INSTRUMENT FAILURE (§3.10).

### 3.7 Two-sided task validity protocol (unchanged mechanism from v2; windows corrected per §3.4)

**Floor check (development seeds only):** frozen-state predictor (`s[0]=0` forever) must show `reduction_h ≤ 0%` at **every horizon 1..5** relative to raw-input-alone, using the §3.4 evaluation window. (NF1 fix: harmonized with §3.9's every-horizon scope — the stricter of the two.)

**Ceiling check (development seeds only):** the oracle must show `reduction_h` strictly between 5% and 95% at every horizon 1..5, using the §3.4 evaluation window.

**If either check fails, this is an INSTRUMENT FAILURE, not a candidate kill.**

**No coupling claim (unchanged from v2):** L3 has exactly one test — the two-sided-validated, held-out relative-loss-reduction comparison above. The term "coupling" does not appear in this section.

### 3.8 Arms (L3) — updated with exact C8-compliant perturbation/fixed-quantity specification

| Arm | What is perturbed | What is held fixed |
|---|---|---|
| Candidate (thick-present state) | Nothing (positive claim) | Everything |
| Frozen state | State update rule bypassed; `s[t]=0` for all t | Input sequence, fitting/evaluation windows |
| Raw-input-alone | N/A (fixed comparator, always run) | Everything |
| Oracle / 3-lag | N/A (uses true 3-lag features) | Everything |
| Permuted | **Post-fit**, the mapping from fitted weight row to output channel is permuted (channel `i`'s prediction computed using channel `j≠i`'s fitted row, for a fixed pre-registered derangement of the 8 channels — a permutation with no fixed points, so every channel is definitely reassigned) | The fitted weights themselves, the input sequence, the evaluation window, the state-update rule |
| Shuffled | The **cycle order of the input sequence is shuffled before state construction**, and the **same shuffled order is applied identically to the targets and to the raw-input-alone comparator's inputs** (both arms see the same permutation of cycle order, closing C8's "does not say whether targets/raw comparator are shuffled the same way" finding) | The state-update rule itself, fitting/evaluation window sizes (counts unchanged; only which cycle maps to which position changes) |
| Empty | The entire input sequence (zero cycles) | N/A |

**Permuted's exact row/horizon mapping (resolves C8's "does not define the 40-output row/horizon mapping" finding):** the state-alone predictor's output is `ŷ[t+1..t+5] ∈ R^40`, organized as 8 channels × 5 horizons. The permutation is applied **at the channel level, across all 5 horizons simultaneously** for a given channel: if channel `i`'s output rows (its 5 horizon predictions) are reassigned to use channel `j`'s fitted weight sub-block, all 5 of channel `i`'s horizon outputs use channel `j`'s weights, for every horizon. The fixed derangement (pre-registered, e.g. cyclic shift `j = (i+1) mod 8`) is applied identically across all scoring seeds.

### 3.9 Exact expected statistic and instrument-failure consequence per L18 arm (resolves C8)

| Arm | Exact expected statistic / bound | Artifact fields | Instrument-failure consequence |
|---|---|---|---|
| Permuted | `reduction_h` recomputed using the channel-permuted predictions (§3.8). **Exact bound: permuted reduction_h ≤ 0% at every horizon** (a genuinely mismatched channel-to-weight mapping cannot outperform the raw comparator, which sees the correctly-matched channel's own current input) — this is an exact bound, not an empirical null, because the permutation is a fixed derangement applied to a linear model, making the failure deterministic given the fitted weights. | `{arm:"permuted", reduction_h[5], all_le_zero}` | Any permuted reduction_h > 0%: INSTRUMENT FAILURE — permutation did not sever the channel correspondence |
| Shuffled | `reduction_h` recomputed on the shuffled-order sequence (§3.8), using the identical loss/denominator rule (§3.6) against the identically-shuffled raw comparator. **Exact bound: shuffled reduction_h collapses to at or below the frozen-state floor** — pass condition: `shuffled_reduction_h ≤ frozen_reduction_h + 0.01` (a 1-percentage-point tolerance for floating-point/seed noise around the floor, stated numerically, not as "toward") at every horizon. | `{arm:"shuffled", reduction_h[5], frozen_reduction_h[5], within_floor_tolerance}` | Any shuffled reduction_h exceeds the floor by more than the stated tolerance: INSTRUMENT FAILURE |
| Frozen | `reduction_h ≤ 0%` at every horizon (§3.7's floor check, re-stated as the frozen arm's exact bound) | `{arm:"frozen", reduction_h[5]}` | Any frozen reduction_h > 0%: INSTRUMENT FAILURE (floor check fails) |
| Oracle | `5% < reduction_h < 95%` at every horizon (§3.7's ceiling check) | `{arm:"oracle", reduction_h[5]}` | Any oracle reduction_h outside (5%,95%): INSTRUMENT FAILURE (ceiling check fails) |
| Fair-naive | Raw-input-alone **is** the fair-naive arm (unchanged labeling from v2, resolving RB6); by definition `reduction_h = 0%` relative to itself — not itself pass/fail, it is the denominator | `{arm:"fair_naive", is_denominator:true}` | N/A — structurally cannot fail (denominator identity) |
| Empty | Loss computation on an empty sequence returns a defined error, not a silently-computed number | `{arm:"empty", returned_defined_error:true}` | Empty arm returns any numeric reduction value: INSTRUMENT FAILURE |

**No "≈"/"toward" language remains in any L3 pass condition** — the shuffled arm's bound is an exact numeric tolerance (0.01) around the independently-computed frozen floor, per C8.

### 3.10 Verdict branches (L3)

- **PASS:** two-sided validity check clears on development seeds AND candidate shows ≥5% relative loss reduction at every horizon 1..5 (§3.6), on all scoring seeds, each scoring seed fit and evaluated in isolation per §3.3–§3.4's disjoint windows.
- **KILL:** candidate reduction < 5% at any horizon on any scoring seed.
- **INSTRUMENT FAILURE:** floor or ceiling check fails on development seeds; OR a degenerate zero-denominator case recurs across ≥2 scoring seeds at the same horizon (§3.6); OR any permuted/shuffled arm fails its exact bound (§3.9); OR the generated sequence is shorter than 1,010 cycles for any scoring seed (a fixture-construction defect, checkable in advance per §3.4).

---

## 4. L5 — Bi-temporality: complete test matrix (replicate labels rebuilt per C4; chain graph pre-registered per C5; downstream-consumer test deleted per C7; L18 arms rebuilt per C8)

### 4.1 Four-combination fixture with replicate-relative offsets (resolves C4)

**v2's defect:** `scoring_now` was fixed at 500 across all 5 replicates while every cycle field was offset by `100·r`, so combination truth changed per replicate (verified by direct computation: 3, 2, 1, 2, 2 correct combinations at replicates 0–4 respectively under v2's design, not 3 in every replicate).

**Corrected design — offset `scoring_now` together with every cycle field, per replicate, so each replicate's own combination truth is self-consistent:**

For replicate `r` (`r = 0..4`), let `offset_r = 100·r`. Replicate `r`'s `scoring_now_r = 500 + offset_r`. The base (replicate-0) combination definitions, each field offset by `offset_r` for replicate `r`:

| Combination | Base `acquired_at` | Base `valid_from` | Base `valid_until` | Truth label (every replicate) |
|---|---|---|---|---|
| A: currently-true, learned-early | 100 | 50 | **open sentinel** | True |
| B: currently-true, learned-late | 400 | 395 | **open sentinel** | True |
| C: stale, learned-early | 100 | 50 | 300 | False |
| D: stale, learned-late | 250 | 245 | 260 | False |

**Replicate `r`'s exact values:** `acquired_at_r = base_acquired_at + offset_r`; `valid_from_r = base_valid_from + offset_r`; for C and D, `valid_until_r = base_valid_until + offset_r`; for A and B (the open-sentinel rows), `valid_until_r = scoring_now_r + 400` — a **replicate-relative open sentinel**, always exactly 400 cycles past that replicate's own `scoring_now_r`, guaranteeing "still valid" holds by construction for every replicate rather than reusing a single absolute sentinel (900) that could eventually be overtaken by a large `offset_r`.

**Verified by direct computation for every replicate `r=0..4` (§12.3 shows the full table):** combination A is currently-true, B is currently-true, C is not, D is not — **4/4 combinations correct in every one of the 5 replicates**, not 3/2/1/2/2 as under v2's design. "Learned-early" (`acquired_at_r − valid_from_r = 50`) and "learned-late" (`acquired_at_r − valid_from_r = 5`) are invariant to `offset_r` by construction (the offset cancels in the subtraction), so the qualitative labels are also replicate-invariant, not merely the true/false labels.

**Fact count (unchanged from v2):** each of the 4 combinations is instantiated across 10 content-subjects × 5 replicates = 50 facts per combination, **200 facts total** for this fixture.

### 4.2 Independent-axis query set (unchanged structure from v2, now grounded in replicate-relative exact cycles)

400 queries: 200 world-validity ("is `f` currently true at that fact's own replicate's `scoring_now_r`?") and 200 self-acquisition ("did I learn `f` before cycle `X`?", `X` fixed per query from a pre-registered per-replicate schedule, offset by `offset_r` identically to §4.1's fields). Both invariance requirements (world-validity answers invariant to `acquired_at`; self-acquisition answers invariant to validity interval) are unchanged and checkable against §4.1's exact, replicate-consistent integers.

### 4.3 Derived single-axis (fair-naive) null distribution, re-verified as replicate-invariant (resolves C4's downstream arithmetic)

**Single-axis rule (unchanged from v2):** `t_single(f) = acquired_at(f)`; predicts "currently true" iff `t_single(f) ≥ scoring_now_r − W`, `W = 200` cycles, applied using each fact's own replicate's `scoring_now_r`.

**Re-derivation under the corrected §4.1 design (verified by direct computation for every replicate):** because `acquired_at_r − scoring_now_r = base_acquired_at − 500` is **invariant to `offset_r`** (both terms carry the same offset, which cancels), the single-axis rule's prediction for each combination is identical across all 5 replicates:

- A (`acquired_at_r − scoring_now_r = −400`): `−400 ≥ −200`? No → predicts false; true label = true → **wrong**, every replicate.
- B (`acquired_at_r − scoring_now_r = −100`): `−100 ≥ −200`? Yes → predicts true; true label = true → **correct**, every replicate.
- C (`acquired_at_r − scoring_now_r = −400`): predicts false; true label = false → **correct**, every replicate.
- D (`acquired_at_r − scoring_now_r = −250`): predicts false; true label = false → **correct**, every replicate.

**Derived accuracy: 3/4 combinations correct, identically, in every replicate → 150/200 = 75.0% exactly** on the 200 world-validity queries (50 facts/combination × 3 correct combinations = 150; 200 total) — the same 75% figure as v2, now confirmed to hold uniformly across replicates rather than only under a since-invalidated single-scoring-now design.

### 4.4 Sealed access-count interface and E1-grade timing (unchanged from v2)

**Sealed access-count interface:** the fact store exposes exactly one instrumented entry point, `read_fact(fact_id) -> Fact`; every code path that reads any fact must go through it, incrementing a sealed, monotonic counter (`access_count`), readable only via `get_access_count_snapshot()`. **Pass condition for "no full scan": `access_count` delta = exactly `k` for a `k`-node chain walk** (§4.5 defines `k` exactly). A mismatch is a candidate integrity failure.

**E1-grade timing:** `time.perf_counter_ns()`, median over ≥100 repetitions per (chain, history-size) combination, warm-up excluded, batched by history size {250, 500, 750, 1000 entries}, dispersion (IQR) logged, non-gating. **Batch-fallback for sub-clock-resolution operations (NF4 fix):** if the median per-operation elapsed time is below the timer's documented resolution, the timing loop batches `B` consecutive operations (starting at `B=100`, doubling until the batch median exceeds 10× the timer resolution) and reports `median_batch_time / B` as the per-operation estimate, with `B` logged in the artifact — inheriting E1-RUN-1's construction-bug fix (Entry 34/commit `dceb2584`).

**Growth thresholds:** unchanged, non-gating pending Rebecca's ruling, per §1.1/§4.9.

### 4.5 Pre-registered 20-chain graph — a fixture separate from the 200-fact combination fixture (resolves C5's chain-graph incompleteness)

**v2's defect:** invoked "all 20 chains, all lengths" without pre-registering chain memberships, edges, lengths, roots, terminals, or the relation to the 200 combination facts — making `k` and the 1.00 accuracy bar unverifiable, and leaving the store's opacity to bypass unproven.

**Corrected design — the chain fixture is explicitly a separate 200-fact structure, independent of §4.1's 200 combination facts (L5's total fixture is therefore 400 facts: 200 for the bi-temporal combination test, 200 for the chain-walk test — stated explicitly to remove the ambiguity C5 identifies). The chain fixture occupies its own separate append log, distinct from the combination-fixture log (NF6 fix: stated explicitly so the full-scan arm's expected `access_count` delta = 200 is unambiguous — a full scan of the chain-fixture log reads 200 facts, not 400).**

- **20 chains, each a linear supersession sequence of exactly 10 nodes:** chain `c` (`c = 0..19`) contains facts `(c, 0), (c, 1), ..., (c, 9)`. `20 × 10 = 200` facts, exactly accounting for the chain fixture's fact count.
- **`supersedes` edges:** `(c, i)` `supersedes` `(c, i−1)` for `i = 1..9`. Each chain has exactly 9 edges. `20 × 9 = 180` edges total (§12.4).
- **Root:** `(c, 0)` — the original fact, no predecessor, `supersedes` field null.
- **Terminal:** `(c, 9)` — the current fact, no successor; the fact returned by a "what do I currently believe" query without chain-walking.
- **Head pointer (F5 fix — a current-belief designation that genuinely requires update on supersession):** each chain `c` has a **head pointer** — a separate index entry, not a fact in the append log — that designates the chain's current-belief node. The head is initialized to `(c, 0)` when the chain is created, and updated to `(c, i)` whenever fact `(c, i)` is appended (superseding `(c, i−1)`). The head pointer is the entry point for all chain-walk queries: `walk_chain(chain_id=c, max_hops)` starts from whatever node the head pointer currently designates and follows `supersedes` edges backward. Updating the head on supersession is a genuine mutation (not a backward-pointer write-once) — this is what makes the frozen arm's freeze meaningful.
- **Chain append timeline (pre-registered, F5 fix):** the 200 chain facts are appended across 200 cycles (one per cycle, L2's cadence rule), in chain-major, node-minor order, split by a pre-registered freeze point:
  - **Pre-freeze phase (cycles 0–99):** for each chain `c = 0..19`, append nodes `(c, 0)` through `(c, 4)`. Order: `(0,0), (1,0), ..., (19,0), (0,1), ..., (19,4)`. Total: 20 × 5 = 100 facts. The head pointer for each chain is updated to point to `(c, 4)` as each `(c, 4)` is appended.
  - **Freeze point: after cycle 99, before cycle 100.** All head pointers are frozen at their current value, pointing to `(c, 4)` for each chain `c`. After this point, head pointers are never updated, even when new supersession facts are appended.
  - **Post-freeze phase (cycles 100–199):** for each chain `c = 0..19`, append nodes `(c, 5)` through `(c, 9)`. Same chain-major, node-minor order. Total: 20 × 5 = 100 facts. Head pointers are NOT updated (frozen) — they remain pointing to `(c, 4)`.
  - **Post-freeze query subset (F5 fix):** a chain-walk query is "post-freeze" if the expected walk path includes any node appended at or after cycle 100. All 40 queries (§4.5 below) reference the terminal `(c, 9)`, which is a post-freeze node, so **all 40 queries are post-freeze.**
- **Derived outcome for the frozen arm (F5 fix):** since the frozen head points to `(c, 4)` instead of the true terminal `(c, 9)`, every walk starts from the wrong node. A full walk from `(c, 4)` visits `(c, 4), (c, 3), (c, 2), (c, 1), (c, 0)` = 5 nodes, but the expected walk visits 10 nodes starting from `(c, 9)`. A partial walk from `(c, 4)` visits 5 nodes, but the expected walk visits 5 nodes starting from `(c, 9)`. In both cases, the walk result does not match the expected result → **walk accuracy = 0.00 for all 40 post-freeze queries, by construction.**
- **Chain length:** 10 nodes (9 edges) per chain, identical across all 20 chains (no variable-length chains, removing any ambiguity about "all lengths").
- **Query-to-chain mapping:** exactly 2 pre-registered chain-walk queries per chain — **(a) full walk**, from terminal `(c,9)` back to root `(c,0)`, visiting all 10 nodes, `k = 10` (this is the boundary case exactly at the M0-adopted `k ≤ 10` bar, §1); **(b) partial walk**, from terminal `(c,9)` back to `(c,5)`, visiting 5 nodes, `k = 5`. **Total chain-walk queries: 20 chains × 2 queries = 40.**
- **`k` defined exactly (resolves C5's "cannot calculate k" finding):** `k` = the number of distinct facts visited during a walk, inclusive of the query's start and end node. A full walk visits `k=10` facts; a partial walk visits `k=5` facts. `access_count` delta must equal `k` exactly for that walk (§4.4).

**Store opacity / bypass-injection tests (resolves C5's second defect — replacing the unproven "single entry point" assertion):** the fact store is made **opaque to the candidate except through three counted capabilities** — `read_fact(id)`, `get_access_count_snapshot()`, and `walk_chain(chain_id, max_hops)` (which internally resolves the chain's head pointer and calls `read_fact` once per hop, and is therefore itself accounted by the sealed counter, not a separate ungoverned path). **Walk accuracy definition (F5 fix):** for each chain-walk query, accuracy = 1.00 if the returned ordered path of visited nodes exactly matches the pre-registered expected path (same nodes, same order), 0.00 otherwise — no partial node-overlap credit. This ensures the frozen arm's walk from `(c,4)` (which visits different nodes than the expected walk from `(c,9)`) scores 0.00, not a partial match. In addition, the harness runs **five named, finite bypass-injection tests**, each attempting one specific bypass vector and asserting it is caught (i.e., either blocked outright or, if it succeeds in reading data, still increments the sealed counter correctly so the mismatch is detected):

| # | Bypass vector | Injection | Expected harness result |
|---|---|---|---|
| 1 | Raw iteration | Candidate attempts `for fact in store._log: ...` (direct iteration over the internal log, bypassing `read_fact`) | Either the attribute is inaccessible (harness confirms no public iteration path exists), or if internal test tooling forces access, the harness detects the resulting `access_count` delta of 0 despite facts being read — flagged as an integrity failure |
| 2 | Raw collection access | Candidate attempts `store.get_all_facts()` or an equivalent bulk-return method | Must not exist in the public interface; harness's namespace enumeration (analogous to §5.3's L6 enumeration) confirms absence |
| 3 | Deserialization bypass | Candidate attempts to deserialize a persisted snapshot of the store directly, without calling `read_fact` for any resulting fact object | Harness re-serializes and checks that any subsequent fact READ (not merely the deserialization itself) is required to go through `read_fact` before the fact's fields are usable by the candidate's own chain-walk logic — enforced by giving the candidate only opaque handles, not raw field-populated objects, from deserialization |
| 4 | Index bypass | Candidate attempts to query an internal search index (if one exists) that returns fact content without incrementing `access_count` | Harness confirms no such index is exposed; if one exists internally for the store's own bookkeeping, it is confirmed to be unreachable from the candidate's code |
| 5 | Direct in-memory reference | Candidate holds a reference to a `Fact` object obtained from a prior legitimate `read_fact` call and re-reads its fields without a new `read_fact` call for subsequent uses within the same walk | Permitted only for the **same** fact within a **single** walk step (re-reading a field you already legitimately fetched is not a new access); the harness's `k`-accounting is defined per **distinct fact touched**, so re-reading an already-touched fact's fields does not increment `access_count` again — this is stated explicitly here to avoid ambiguity, and is why `access_count` delta = k (distinct facts), not = number of field accesses |

**No M3 chain-walk claim depends on a self-report** — `access_count` delta = k is checked against the sealed, harness-owned counter for every one of the 40 chain-walk queries, per scoring seed.

### 4.6 Downstream-consumer test for L5 — deleted per C7

**v2's §4.6 downstream-consumer test (the additive-relevance consumer extended with a validity filter) is removed entirely from this document and from E2 scope**, per the mail's explicit instruction that "safest is delete them" for the L1/L5 downstream-consumer PASS conditions. No PASS, KILL, or INSTRUMENT FAILURE branch for L5 (§4.9) depends on any downstream consumer's behavior.

### 4.7 Arms (L5) — updated with C8-compliant perturbation specification, chain fixture included

| Arm | What is perturbed | What is held fixed |
|---|---|---|
| Candidate | Nothing (positive claim); two-axis store + 20-chain graph, all reads via `read_fact` | Everything |
| Single-axis (fair-naive) | The store's own field structure (collapses two axes to one, `t_single(f)=acquired_at(f)`, §4.3) | The underlying fact values themselves (only the store's read/interpretation logic differs) |
| Full-scan chain-walker | The chain-walk **algorithm** (recomputes the chain by calling `read_fact` on every entry in the log at query time, ignoring `supersedes` pointers) | The `read_fact` entry point itself (still used, just called far more often) |
| Oracle | Nothing (uses ground-truth labels/chain structure directly) | Everything |
| Frozen | **Head pointer frozen at the pre-registered freeze point (cycle 100, §4.5):** the head/current-belief pointer for each chain is frozen at `(c, 4)` and never updated when post-freeze supersession facts `(c, 5)–(c, 9)` are appended. Walks start from the frozen head `(c, 4)` instead of the true terminal `(c, 9)`, visiting only pre-freeze nodes. Combination fixture: both bi-temporal axes frozen at fact-creation time (unchanged from v3, since §4.1's fixture has no supersession events) | The head pointer's update-on-supersession behavior (frozen); the combination fixture's bi-temporal axes (frozen at creation) | The initially-created fact values, the `supersedes` backward pointers (which are write-once and never need updating — the freeze targets the head pointer, not the backward pointers) |
| Permuted | `acquired_at` and validity-interval **values** permuted across the 200 combination facts (§4.1), independent of the chain fixture (§4.5, permuted separately: node content values permuted across the 200 chain facts, `supersedes` edges untouched) | The marginal distribution of each factor; the chain edge structure |
| Shuffled | For the combination fixture: **query order** shuffled (does not affect per-query scoring). For the chain fixture: `supersedes` **edge targets** shuffled independently of true supersession order (breaking chain connectivity while node content is untouched) | Fact values (combination fixture); node content (chain fixture) |
| Empty | No facts in either fixture | N/A |

### 4.8 Exact expected statistic and instrument-failure consequence per L18 arm (resolves C8)

| Arm | Exact expected statistic / bound | Artifact fields | Instrument-failure consequence |
|---|---|---|---|
| Permuted | Combination-fixture accuracy on world-validity queries: **empirical null** via 1,000 seeded permutations of the acquired_at/validity-interval-to-fact mapping; pass condition for the permuted arm to count as a valid negative control: observed permuted accuracy within [null_mean − 2·null_sd, null_mean + 2·null_sd] of the resulting empirical distribution. Chain fixture: with node content permuted but edges intact, chain-walk **connectivity accuracy remains 1.00** (edges are untouched) but the **content returned by the walk is wrong relative to the true combination label** — pass condition: content-mismatch rate = 1.00 (every permuted-content node mismatches its true value, since the permutation is derangement-only, no fixed points) | `{arm:"permuted", combo_accuracy_within_null_band, chain_content_mismatch_rate}` | Permuted combination accuracy exceeds the null band, or chain content-mismatch rate < 1.00: INSTRUMENT FAILURE |
| Shuffled | Combination fixture: query order shuffled — **exact bound: per-query accuracy unaffected (still ≥0.95 if candidate is genuinely correct)**, since per-query scoring does not depend on order; this arm exists to confirm order-independence, not to induce failure. Chain fixture: edges shuffled — **exact bound: chain-walk accuracy = 0.00 (deterministic)** (F6 fix: `20 × 9 = 180` non-root edges, not 190; under a uniformly random derangement of 180 edge targets, the probability of any edge landing on its own true target is **0 by definition** — a derangement has no fixed points, and each edge's true target is distinct, so inheriting another edge's target can never reproduce one's own). This is a deterministic bound, not an empirical null: every walk fails because no shuffled edge points to the correct predecessor. **Single criterion: chain-walk accuracy under shuffled edges ≤ 0.05** (conservative — the expected value is 0.00). | `{arm:"shuffled", combo_query_order_accuracy, chain_walk_accuracy, edge_count:180}` | Chain-walk accuracy under shuffled edges > 0.05: INSTRUMENT FAILURE |
| Oracle | 1.00 on both query types; 1.00 chain-walk for all 40 queries; access-count delta = k exactly | `{arm:"oracle", combo_accuracy, chain_walk_accuracy, access_count_deltas[40]}` | Any oracle test <1.00: INSTRUMENT FAILURE |
| Fair-naive | Combination fixture: **75.0% exactly on the 200 world-validity queries** (§4.3, re-derived, replicate-invariant; NF5 fix: the `combo_accuracy` field and the §4.9 instrument-failure trigger are scoped to world-validity queries only — the single-axis arm answers self-acquisition queries from `acquired_at` and would score ~1.00 there, so the exact-match check must use the world-validity denominator). Chain fixture: fair-naive has no chain analog (the single-axis collapse only affects the bi-temporal combination fixture, not chain structure) — chain-walk accuracy for the fair-naive arm is reported as **not applicable**, not silently omitted. | `{arm:"fair_naive", combo_accuracy_world_validity:0.75, chain_walk_accuracy:"N/A"}` | Fair-naive world-validity combo accuracy ≠ 0.75 exactly: INSTRUMENT FAILURE (fixture-construction defect) |
| Frozen | Combination fixture: both bi-temporal axes frozen at creation — identical to candidate on the combination fixture (no supersession events in §4.1's fixture, so nothing changes). **Chain fixture (F5 fix): head pointer frozen at `(c, 4)` (§4.5/§4.7):** all 40 chain-walk queries are post-freeze (they reference terminal `(c, 9)`, appended post-freeze). The frozen head points to `(c, 4)`, so walks start from the wrong node and visit only pre-freeze nodes `(c, 4)–(c, 0)`. **Exact bound: walk accuracy = 0.00 for all 40 post-freeze queries, by construction** (the walk result never matches the expected walk from terminal `(c, 9)`). | `{arm:"frozen", combo_accuracy, chain_walk_accuracy_post_freeze_queries, freeze_cycle:100, frozen_head_node:"(c,4)"}` | Frozen arm's post-freeze chain-walk accuracy > 0: INSTRUMENT FAILURE |
| Full-scan chain-walker | Chain-walk answers correct (1.00, since it does eventually find the right answer via brute force) BUT `access_count` delta = **200** (full chain-fixture log size — NF6 fix: the chain fixture occupies its own separate log of 200 facts, distinct from the 200-fact combination-fixture log, so a full scan reads 200, not 400) for every walk, **≫ k** (5 or 10) | `{arm:"full_scan", chain_walk_accuracy:1.00, access_count_delta:200, k_expected:[5,10], log:"chain_fixture_separate"}` | Full-scan arm's access_count delta ≤ k: INSTRUMENT FAILURE (the harness's counter is not actually distinguishing scan behavior) |
| Empty | Any query against an empty fact store returns a defined error, not a silently-computed accuracy/walk result | `{arm:"empty", returned_defined_error:true}` | Empty arm returns any non-error numeric result: INSTRUMENT FAILURE |

**No "≈"/"toward" language remains in any L5 pass condition.**

### 4.9 Verdict branches (L5) — downstream-consumer condition deleted per C7

- **PASS:** ≥0.95 accuracy on both combination-fixture query types on all scoring seeds AND chain-walk accuracy = 1.00 for all 20 chains × 2 queries (full and partial) on all scoring seeds AND sealed access-count delta = k exactly for every one of the 40 chain-walk queries — growth-threshold performance (§4.4/§1.1) is reported but non-gating pending Rebecca's ruling.
- **KILL:** any accuracy < 0.95 on either combination query type on any scoring seed; any chain-walk accuracy < 1.00; any access-count integrity mismatch.
- **INSTRUMENT FAILURE:** single-axis arm's derived 75.0% accuracy on **world-validity queries** is not observed exactly, on any replicate (§4.1/§4.3, NF5 fix: scoped to world-validity queries, not self-acquisition); OR frozen arm's post-freeze chain-walk accuracy > 0 (§4.8, F5 fix); OR the sealed counter fails to increment on a known-good `read_fact` call; OR the full-scan chain-walker's access-count delta ≤ k (§4.8); OR any bypass-injection test (§4.5) is not caught as specified.

---

## 5. L6 — Episodic completeness: complete test matrix (finite module graph and non-vacuous L18 arms per C6; downstream-consumer condition N/A — L6 never had one)

### 5.1 Trust boundary (unchanged from v2)

The system has exactly two zones. **Trusted internal storage** (the append-only log itself, and in-process objects directly wrapping a log entry for use by *trusted* internal components) is not a retrieval interface. **Untrusted/external-facing zone** must return the full 4-tuple or a tagged rejection on every content-returning call.

### 5.2 Frozen tuple schema with tagged success/error union (unchanged from v2)

```
EpisodicResult =
    Success(EpisodicResponse)
  | Rejected(reason: str)

EpisodicResponse = {
  content:   <payload>,
  source:    {"append" | "designation" | "rehearsal"},
  context:   {chain_position: <int>, prev_hash: <hex>, self_hash: <hex>},
  self_position_at_encoding: {
     cycle: <int>,
     landmark_relative: {<landmark_id>: <BEFORE_L|AT_L|AFTER_L>}
  }
}
```

### 5.3 Finite, frozen module/API graph and mandatory cache disposition (resolves C6's first defect)

**v2's defect:** the enumeration included "any alias/wrapper function" and "any cache layer ... if a cache exists" — open-ended post-build categories, not a finite pre-registered set.

**Corrected design — exactly three frozen modules, four named public callables total, cache disposition stated as a fact (F7 fix: count reconciled to 4 everywhere, not 5):**

| Module | Public callables (exhaustive; no others exist) |
|---|---|
| `episodic_store.py` | `query_episodic(query) -> EpisodicResult`; `query_episodic_batch(queries) -> List[EpisodicResult]` |
| `episodic_cache.py` | **None. Cache disposition: no cache layer exists in this fixture — stated as a fact, not a conditional ("if a cache exists").** This module contains no public callables; its presence in the graph documents the absence, not a hypothetical. |
| `episodic_serialize.py` | `to_json(EpisodicResult) -> bytes`; `from_json(bytes) -> EpisodicResult` |

**No other module, wrapper, alias, or convenience function exists in the public namespace of this fixture.** This is a closed-world, pre-registered claim: the audit (§5.4) enumerates exactly these three modules' public (non-underscore-prefixed) names and asserts this set is complete, rather than searching an open-ended "any function that might exist."

**Finite reachability-audit algorithm:** for each of the 3 modules, enumerate every name in its namespace not beginning with `_`; for each such name, call it with a synthetic probe query (or, for `from_json`, a synthetic serialized payload) and inspect the return value's runtime type. **Pass condition: every enumerated callable's return value is an instance of `EpisodicResult` (i.e., tagged `Success` or `Rejected`)**; a callable whose return type is anything else (including bare `content`, a raw dict, or an unwrapped payload) fails the audit.

**Audit artifact schema:** `{module: str, callable_name: str, return_type_observed: str, is_tagged_union: bool, verdict: "pass"|"fail"}`, one row per enumerated callable (4 rows total, given the frozen graph above).

### 5.4 Finite negative-injection attack matrix (unchanged from v2's 8 attacks; attack #5's cache-layer question now answered by §5.3's disposition rather than left conditional)

| # | Attack | Path | Expected system behavior |
|---|---|---|---|
| 1 | External path-reachability probe | Search the 3 frozen modules' public namespaces (§5.3) for a reachable function/attribute returning bare `content` | Must find no such reachable path — enumeration is now over the finite, frozen graph of §5.3, not an open-ended search |
| 2 | Public query with provenance-stripping flag | `query_episodic(query, strip_provenance=True)` or unrecognized kwarg | REJECTED — argument error |
| 3 | Batch retrieval field omission | `query_episodic_batch([...])`, inspect each element's tag/fields | Every element `Success` with all 4 fields, or `Rejected`; no bare-content element |
| 4 | Serialization round-trip stripping | Serialize/deserialize an `EpisodicResult` via `episodic_serialize.py` | Tag and all 4 fields survive exactly |
| 5 | Cache-layer bare-content leak | N/A — **no cache exists (§5.3's frozen disposition)**; this attack is now a **structural confirmation that `episodic_cache.py` exports zero public callables**, not a conditional inspection | Module's public namespace is empty; confirmed by §5.3's audit, cross-referenced here |
| 6 | Alias/wrapper function | Call any secondary function in the 3 modules' public namespaces beyond the 4 named in §5.3 | No such function exists (finite graph, §5.3) |
| 7 | Error-path partial return | Construct a query triggering a registry failure during landmark computation | Must return `Rejected(reason="registry_unavailable")` at the top level — never a `Success` with an error-shaped `landmark_relative` |
| 8 | Deliberately broken provenance-stripping variant (audit self-test) | A constructed variant that intentionally returns bare `content` | Must be caught and rejected by the audit harness; if not caught, instrument failure of the harness itself |

**Returned artifact:** an 8-row table, `{attack_id, path_type, caught, diagnosis}`.

### 5.5 Real, non-vacuous L18 arms for L6's structural claim (resolves C6's second defect — no waiver requested)

**No L18 waiver is requested in this document, per the mail's explicit instruction.** Each of the six controls is given a genuine transform and a genuine, non-analogy expected outcome:

| Control | Real transform | Expected outcome | Why this is non-vacuous |
|---|---|---|---|
| Empty | The log has zero entries. `query_episodic(any_id)` is called. | Must return `Rejected(reason="not_found")` — a real negative-branch return, not a `Success` with empty content | This is a genuine behavioral assertion (the tagged-rejection branch must actually fire), not "no content exists so nothing can leak" — a candidate that returns an untagged `None` or raises an unhandled exception instead of `Rejected` fails this control, so it is not vacuous |
| Permuted | At the storage level, entry-ID-to-content mapping is permuted across all entries (content of `id_i` swapped with content of `id_j`, for a fixed derangement) — tags, source, context, and encoding-time fields are **not** permuted, only `content` | `query_episodic(id_i)` must still return a `Success` with the full 4-field tagged structure — the *content value itself* will be wrong relative to the true `id_i` (expected, since content was permuted), but **the wrapper's structural completeness must be unaffected by content corruption** | Tests that the tagging mechanism does not depend on content correctness — a real, falsifiable claim distinct from attack #1 |
| Shuffled | The **order** of queries within a `query_episodic_batch` call is shuffled | Each result element's tag/fields must still be correct **relative to its own query**, independent of its position in the shuffled batch — pass condition: reordering the batch and comparing element-wise by query ID (not position) yields identical results to the unshuffled batch | Tests for order/position-dependent bugs that could silently drop the wrapper for some batch positions — a real, checkable claim |
| Oracle | Direct trusted-zone field read of the same entries (§5.1) | Must match the `content`, `source`, and `context` fields of the corresponding `Success.EpisodicResponse` exactly | Genuine ground-truth comparison, not an analogy |
| Frozen | A single `EpisodicResult` is captured once (at a fixed point) and replayed later via `from_json(to_json(captured_result))` instead of a live query | The replayed value must still validate as a well-formed tagged union (§5.2's schema) — this is a genuine frozen-vs-live structural check: it distinguishes "schema drift over time" (a frozen snapshot from an old schema version would fail validation against the current one) from "live bypass" (which attacks #1–#8 already cover) | A real comparison between a static prior artifact and the live schema, not a placeholder |
| Fair-naive | Attack #1's path-reachability probe (§5.4), unchanged | The strongest honest attempt to find a legitimate-looking bypass, run against the real implementation | Already real and non-analogy in v2; retained unchanged |

**Empty does not "vacuously pass" under this design** (directly resolving C6's named defect): it requires the system to actively return the correct tagged rejection branch, which a broken implementation (e.g., one that raises an unhandled exception, returns `None`, or returns an untagged empty `Success`) would fail.

### 5.6 Verdict branches (L6)

- **PASS:** all 8 attacks (§5.4) show `caught = True` (attack #8's "caught=True" meaning the harness correctly rejects the deliberately broken variant) AND all 4 reachability-audit rows (§5.3) show `verdict = "pass"` AND all 6 L18 arms (§5.5) show their stated expected outcome.
- **KILL:** any of attacks #1–#7 shows `caught = False`; OR any reachability-audit row shows `verdict = "fail"`; OR any of the empty/permuted/shuffled/oracle/frozen/fair-naive arms fails to show its stated expected outcome (§5.5).
- **INSTRUMENT FAILURE:** attack #8 shows `caught = False` (harness self-test failure).

### 5.7 No coupling claim (unchanged from v2)

L6 has one property: every retrieval returns the complete tuple or a tagged rejection, tested by §5.1–§5.6 alone. No coupling or integration claim is made.

---

## 6. Cross-law E2 execution summary (downstream-consumer references removed per C7)

| Law | Correctness test | Operational distinctness | Cross-law relationship claim |
|---|---|---|---|
| L1 | Balanced marginal-mean binned-age curve + rehearsal-conditional tests (§2.6) | Heterogeneous stratified candidate sets with deterministic tie-break (§2.4); permuted vs. shuffled distinct, both severing predictor-label correspondence (§2.8) | None. No downstream-consumer test remains in this document (§2.11, deleted per C7) |
| L3 | ≥5% relative loss reduction, every horizon 1..5, disjoint fitting/evaluation windows (§3.4/§3.6) | Two-sided floor/ceiling validity check; permuted vs. shuffled distinct, exact bounds (§3.8/§3.9) | **No coupling claim.** The held-out loss test is L3's only test |
| L5 | ≥0.95 on both combination query types; 1.00 chain-walk on the pre-registered 20-chain graph; sealed access-count integrity (§4.5/§4.9) | Replicate-invariant combination labels (§4.1/§4.3); permuted vs. shuffled distinct across both sub-fixtures (§4.7) | None. No downstream-consumer test remains in this document (§4.9, deleted per C7) |
| L6 | 8-attack matrix + finite reachability audit + tagged-schema consistency (§5.3–§5.6) | Finite 3-module graph; real non-vacuous L18 arms, no waiver requested (§5.5) | **No coupling claim.** The attack matrix and reachability audit are L6's only tests |

**On downstream-consumer conditions generally:** v2 retained downstream-consumer PASS conditions for L1 and L5, reusing E1's additive-relevance consumer. Per the mail's explicit C7 instruction ("remove all non-constitutional L1/L5 downstream-consumer conditions from PASS verdicts and E2 scope. They are report-only only if fully reproduced; safest is delete them"), **this document deletes them outright** rather than attempting a fuller specification. Neither L1's nor L5's verdict branches (§2.11, §4.9) reference any consumer. **This entire M3 evidence base remains correctness- and falsification-only; the full L15 bidirectional-ablation-matrix treatment is explicitly reserved for M5 and is not approximated here (§9's fence, unchanged); no E1 three-property analog is forced onto any law, per the mail's explicit instruction that M3 law-compliance tests are sufficient and no L15 evidence is claimed.**

---

## 7. §2 enforcement — executable invariants (unchanged from v2)

### 7.1 L11 (one clock) — executable negative injection, covering L6's encoding-time write

**Invariant:** every new timestamp-bearing write reads `now` from the single autobiography cycle counter, including L6's encoding-time tuple/landmark snapshot write (`self_position_at_encoding` frozen into the entry at append time). **Negative-injection test:** a deliberately-broken variant substitutes `time.time()` for the cycle-counter read; the invariant check must detect and reject this by verifying the recorded cycle strictly equals the counter's value at the write call.

### 7.2 L12 — auditable compatibility only (unchanged)

No L12 compliance finding is made; only the auditable structural design constraint on L3's state object (§3.2) is stated.

### 7.3 L13 (memory writes through now) — executable negative injection, covering L6's landmark snapshot

**Invariant:** every new memory write is stamped by the cycle counter and indexed at write time, including L6's `self_position_at_encoding.landmark_relative` computation (computed once, at append, never recomputed). **Negative-injection test:** a deliberately-broken variant recomputes `landmark_relative` at read time using the registry's *current* state instead of the frozen snapshot; the invariant check detects this by comparing against the log's own immutable stored snapshot — a mismatch after a landmark is later added indicates the broken variant.

**L5's backdating negative injection (unchanged):** a post-append in-place mutation of `valid_from`/`valid_until` must be caught via hash-chain integrity, distinguished from a legitimate backdated-but-atomically-written fact.

### 7.4 L14 — forward-compatibility note only (unchanged)

No L14 bar; a note only.

---

## 8. Seed protocol, exposure ledger, and standing execution protections (ledger rebuilt as append-only per-use-event log per NB1)

### 8.1 Named seed pools, selection order, and append-only exposure ledger (resolves NB1)

**Development-seed pool (fixed, pre-registered):** seeds `{101, 102, 103, 104, 105}`.

**M3 hold-out (scoring-only) pool:** seeds `{201, 202, 203}` — **none of which appears in the development pool above, and none of which is E1's own seed 42, 43, 44, 45, or 46 (§8.1's E1 record below)**. All three of {201, 202, 203} are explicitly prohibited from any M3 development, diagnostic, or pre-registration-validation use. At least 2 of the 3 (the two lowest-numbered not yet exposed at scoring time) satisfy the standing ≥2-unseen-in-development rule.

**Selection/order rule (unchanged from v2):** for each law's scoring run, all 3 hold-out-pool seeds {201, 202, 203} are used in full, in ascending numeric order, for every law's scoring run — satisfying "≥2 unseen in development" with a full margin (all 3 are unseen). Development-pool seeds {101–105} are used only for pre-scoring validity/instrument checks and never appear in a scoring verdict.

**Corrected ledger schema — append-only, one record per seed-USE event (resolves NB1's cardinality defect):**

```
{
  event_id: <monotonic int, unique per record>,
  seed_id: <int>,
  pool: {"M3_development" | "M3_holdout" | "E1_scoring" | "E1_development"},
  milestone_id: <str>,
  law_id: <str | null>,
  run_type: {"development_diagnostic" | "scoring"},
  timestamp_cycle: <M3 program-relative sequence number>
}
```

Each seed-use event (one law, one run, one seed) appends exactly one new record with a fresh `event_id`; the ledger never overwrites or mutates a prior record, and a seed used across multiple laws or multiple runs accumulates multiple records rather than a single record with array-valued fields — directly resolving NB1's finding that "one ledger object per seed cannot faithfully hold multiple uses."

**E1 exposure recorded (resolves NB1's coverage gap; NF2 fix — completeness claim narrowed):** the ledger now records **all five of E1's actual scoring seeds, 42 through 46**, under `pool: "E1_scoring"`, with 45 and 46 additionally distinguishable as the hold-out subset actually scored (via their own `run_type: "scoring"` records, cross-referenced against E1's own hold-out designation in the E1 record — no new field is needed since the pool tag plus the seed value together already identify the historical record). E1's development seeds **42, 43, 44** are recorded separately under `pool: "E1_development"`. None of seeds 42–46 is a member of either M3 pool above. This is a complete record of **E1 and M3 seed-use events** (NF2 fix: the ledger's completeness claim is scoped to E1 and M3 only — M1 used seeds 100–129 for empirical-null replicate ranges and seeds 42–44 for scoring, which are not recorded here because they predate M3 and are not M3 seed-use events; development-pool seeds carry no unseen requirement, and hold-outs {201, 202, 203} have no recorded exposure anywhere, so no rule is violated by this scoping).

### 8.2 Standing execution protections (unchanged from v1/v2, restated)

1. **≥2 scoring seeds unseen in development** — satisfied with full margin (3 of 3) per §8.1's pool design.
2. **Development runs are diagnostic-only, never scoring** (O-15).
3. **Scoring runs execute only through Rebecca's supervised-executor courier channel** (O-15).
4. **Rebecca's returns are raw and complete.**
5. **Re-run-on-failure is FORBIDDEN** (O-14).
6. **Full L18 battery on every positive claim** — per-law checklists in §2.10, §3.9, §4.8, §5.5, now with exact numeric/empirical-null pass conditions rather than qualitative language (resolves C8).
7. **Candidate/death accounting under D1–D5** — unchanged verbatim.
8. **Single-law-failure disposition** — unchanged verbatim; recorded but does not by itself decide the M3 verdict.
9. **M3 overall verdict table** — unchanged verbatim (GREEN / PARTIAL / escalation trigger / INSTRUMENT-BLOCKED).

---

## 9. L9 hard fence (unchanged from v1/v2, restated)

**Rule (binding):** M3 introduces no associative retrieval channel routed through learned or bounded nonlinear weight perturbation. Re-verified against every v3 mechanism: L1's `priority(e)` function (§2.5) is a fixed closed-form equation with pre-registered constants, no learned weights; L3's state update (§3.2) has zero learned parameters; L5's stores are deterministic pointer/timestamp structures; L6 has no retrieval channel beyond the deterministic tagged lookup. **If any future task design would require a learned/nonlinear channel, work pauses immediately; I-16 is added only after an explicit Rebecca/CRITIC ruling.** Fixture-reuse across laws remains neutral infrastructure reuse, not partial L15/L16/L17 evidence; no M3 result may be characterized as such.

---

## 10. Timebox — unchanged from v2 (per NB3)

**Proposed cap:** 4 sessions / 8 calendar days, discretionary, non-arithmetic rationale. **Activation:** clock starts only after CRITIC clearance and Rebecca's gate decision. **Tripwire — exactly three options, no others:**

- **(i) Continue within the existing cap.**
- **(ii) Pause or stop.**
- **(iii) Close the current milestone and separately propose a newly scoped future milestone with its own scope, bars, and gate.** No work under a new milestone proposal may proceed under M3's existing cap or clock.

**No cap-revision branch exists at any tripwire** (unchanged from v2, resolving RB8; confirmed still absent here per NB3's instruction to retain unchanged).

**Tripwire inputs (unchanged):** session 2 elapsed, OR day 4 elapsed, OR any law's instrument-failure branch unresolved past 1 full session, OR the ≥2-of-4 escalation trigger fires.

**Build-cell size:** 1–3 task builders, unchanged.

---

## 11. What this specification does NOT claim

- It does not claim M3 build authorization.
- It does not claim any M0-adopted bar has changed (§1), except the one new discretionary proposal isolated in §1.1, which is explicitly pending Rebecca's ruling and non-gating until ruled on.
- It does not claim L12 or L14 compliance.
- It does not claim L3 or L6 has a coupling/integration test — that language is absent from both sections.
- It does not claim any L1/L5 downstream-consumer evidence — that language and those conditions are deleted entirely from this document (§2.11, §4.9, §6), per C7.
- It does not claim the L18 battery required a waiver for L6 — no waiver is requested; real, non-vacuous arms are specified (§5.5), per C6.
- It does not claim a valid arithmetic derivation for the timebox cap (§10).
- It does not offer a cap-revision branch at any tripwire (§10) — only continue/pause-or-stop/close-and-re-propose.
- It does not use "≈" or "toward" language in any gate criterion anywhere in this document (verified in §12.8).
- It does not execute, implement, or run anything. It is a specification for CRITIC re-review only.
- It does not attest `state/STATE.md` as current (NF3 note: STATE.md still shows M2 active and HEAD `dceb2584…` as of this writing; the provenance log Entry 34 and `state/ROLE_SESSIONS.md` support M2 GREEN/SEALED/ACCEPTED and main commit `1626bb09…`; bringing STATE.md current is INTEGRATOR's responsibility, not ARCHITECT's, but STATE.md must be brought current before Rebecca rules at this gate).

---

## 12. Specification arithmetic and closure audit

This appendix is a self-check, not a formality: every claim below is independently re-derivable from the sections cited, and this document is not considered internally consistent unless every check in this appendix passes.

### 12.1 L1 creation-phase arithmetic sanity table (verifies §2.1)

| Bin | Cycle range | Measured cycles | Filler cycles | Bin total | Age range at now_final=2200 |
|---|---|---|---|---|---|
| 0 | [0, 199] | 40 | 160 | 200 | [2005, 2200] |
| 1 | [200, 399] | 40 | 160 | 200 | [1805, 2000] |
| 2 | [400, 599] | 40 | 160 | 200 | [1605, 1800] |
| 3 | [600, 799] | 40 | 160 | 200 | [1405, 1600] |
| 4 | [800, 999] | 40 | 160 | 200 | [1205, 1400] |
| **Sum** | [0, 999] | **200** | **800** | **1000** | — |

Check: `200 + 800 = 1000` ✓ (matches the 1,000-cycle creation phase exactly, one append per cycle, §2.1). Check: age ranges are contiguous and non-overlapping across bins (2005 > 2000, 1805 > 1800, 1605 > 1600, 1405 > 1400) ✓. Priming-phase count: `5 × (0+2+4+8+16) × 8 = 5 × 30 × 8 = 1200` ✓, filling cycles 1000–2199 (1,200 cycles) exactly ✓. `now_final = 1000 + 1200 = 2200` ✓. Final autobiography size = 2200 (one append per cycle 0–2199) ✓.

### 12.1a L1 control and ablation arithmetic verification (verifies F1, F2, F3, F4 fixes)

This sub-check verifies the arithmetic of every F1–F4 fix by direct computation (structural seed = 777, outside all seed pools {42–46, 101–105, 201–203}, for candidate-set construction; seed = 42 for the tie-break permutation; seed = 43 for the fair-naive permutation). All values below were computed by a verification script that implements the exact rules of §2.1–§2.6, §2.8–§2.9 and is reproducible by any reviewer from the stated constants and seeds.

| Check | Expected | Computed | Pass? |
|---|---|---|---|
| F2: Within-bin Spearman(level, age), all 5 bins | Weak (not ±1.0) | −0.1225 (identical across bins) | ✓ (was −1.0 under `⌊i/8⌋`) |
| F2: Oracle candidate within-bin ρ (rehearsal, accessibility), all 5 bins | ≥ 0.6 | 0.91, 0.95, 0.94, 0.93, 0.92 | ✓ |
| F2: Factor-inert (β=0) within-bin ρ, all 5 bins | < 0.6 | 0.20, 0.24, 0.20, 0.18, 0.13 | ✓ (test correctly fails) |
| F4: Candidate sets | 100 | 100 | ✓ |
| F4: Per-entry appearance count | exactly 5 | min=5, max=5 | ✓ (balanced design) |
| F4: Oracle R² | ≥ 0.85 | 0.985 | ✓ |
| F4: Oracle β_age | < 0 | −0.00150 | ✓ |
| F1: Frozen R² (seeded random tie-break, seed=42) | ≤ null 95th pct | 0.236 ≤ 0.749 | ✓ (valid negative control) |
| F1: Fair-naive R² (seeded random permutation, seed=43) | ≤ null 95th pct | 0.320 ≤ 0.749 | ✓ (valid negative control) |
| F1: Empirical null (1000 reassignments) mean | — | 0.244 | ✓ |
| F1: Empirical null SD | — | 0.246 | ✓ |
| F1: Empirical null 95th percentile | — | 0.749 | ✓ |
| F1a: Permuted R² (own null distribution) | within [m−2s, m+2s] | 0.000 within [−0.255, 0.764] | ✓ |
| F1a: Permuted null mean | — | 0.255 | ✓ |
| F1a: Permuted null SD | — | 0.255 | ✓ |
| F3: Recency-only R² | ≥ 0.85 | 0.926 | ✓ |
| F3: Recency-only β_age | < 0 | −0.00229 | ✓ |
| F3: Recency-only all 5 ρ < 0.6 | all < 0.6 | 0.20, 0.24, 0.20, 0.18, 0.13 | ✓ (rehearsal absent) |
| F3: Rehearsal-only β_age | ≥ 0 | 0.0005 | ✓ (age absent) |
| F3: Rehearsal-only all 5 ρ ≥ 0.6 | all ≥ 0.6 | 0.96, 0.98, 0.97, 0.97, 0.97 | ✓ (rehearsal present) |

All 21 checks pass ✓. The frozen and fair-naive arms are valid negative controls (R² well below the null 95th percentile), the within-bin decorrelation is sufficient (factor-inert candidate correctly fails), the oracle satisfies the M0 bar under the exact pre-registered aggregation rules, and both ablation arms correctly isolate their factors.

### 12.2 L3 window-disjointness sanity table (verifies §3.4)

| Horizon | Fit targets | Eval targets | Overlap? |
|---|---|---|---|
| 1 | [1,700] | [706,1005] | None |
| 2 | [2,701] | [707,1006] | None |
| 3 | [3,702] | [708,1007] | None |
| 4 | [4,703] | [709,1008] | None |
| 5 | [5,704] | [710,1009] | None |

Check: fit-used cycle union = {0,...,704} (705 cycles: 700 origins + up to 5 additional target-only cycles at the tail). Eval-used cycle union = {705,...,1009} (305 cycles: 300 origins + up to 5 additional target-only cycles at the tail). Union of both = {0,...,1009} = 1,010 cycles, matching `N_total=1010` exactly ✓. Intersection = ∅ ✓ (verified by direct set computation, not asserted). Per-horizon fitting observation count = 700 (constant across h) ✓. Per-horizon evaluation observation count = 300 (constant across h) ✓.

### 12.3 L5 replicate-label sanity table (verifies §4.1/§4.3)

| Replicate r | offset_r | scoring_now_r | A true? | B true? | C true? | D true? | Correct combos |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 500 | Yes | Yes | No | No | 4/4 |
| 1 | 100 | 600 | Yes | Yes | No | No | 4/4 |
| 2 | 200 | 700 | Yes | Yes | No | No | 4/4 |
| 3 | 300 | 800 | Yes | Yes | No | No | 4/4 |
| 4 | 400 | 900 | Yes | Yes | No | No | 4/4 |

Check: every replicate shows 4/4 correct combination labels ✓ (contrast with v2's 3,2,1,2,2 pattern, which this design eliminates by offsetting `scoring_now` together with all cycle fields). Fair-naive (single-axis, W=200) accuracy: 3/4 combinations correct, identically, in every replicate (B correct, A/C/D as derived in §4.3) → `150/200 = 0.75` exactly, replicate-invariant ✓.

### 12.4 L5 chain-graph closure check (verifies §4.5; updated for F5 head-pointer mechanism and F6 edge-count correction)

`20 chains × 10 nodes/chain = 200 facts` ✓ (matches the chain fixture's stated fact count, separate from the 200 combination facts — L5's total fixture = 400 facts, stated explicitly in §4.5 to remove the ambiguity C5 identified). `20 chains × 9 edges/chain = 180 supersedes edges` total ✓ (F6 fix: corrected from v3's erroneous "190" — 200 facts − 20 roots = 180 non-root nodes, each with exactly one `supersedes` edge). `20 chains × 2 queries/chain = 40 chain-walk queries` ✓. `k` values used: {5, 10}, both ≤ 10 (the M0-adopted bar, §1) ✓, with `k=10` exactly at the boundary (a deliberate boundary-case inclusion, not an oversight). Every chain has exactly one root (in-degree 0 within the chain) and exactly one terminal (out-degree 0 within the chain) ✓ by the linear-sequence construction.

**F5 head-pointer and append-timeline check:** pre-freeze phase: 20 chains × 5 nodes = 100 facts at cycles 0–99 ✓. Freeze point: after cycle 99, before cycle 100 ✓. Post-freeze phase: 20 chains × 5 nodes = 100 facts at cycles 100–199 ✓. Total: 100 + 100 = 200 facts ✓. Frozen head points to `(c, 4)` for each chain ✓. All 40 queries reference terminal `(c, 9)`, a post-freeze node ✓ → all 40 queries are post-freeze ✓. Frozen walk from `(c, 4)` visits 5 nodes; expected walk from `(c, 9)` visits 10 (full) or 5 (partial) — walk result ≠ expected → **walk accuracy = 0.00 for all 40 post-freeze queries, by construction** ✓.

**F6 shuffled-edge check:** 180 non-root edges ✓ (not 190). Under a uniformly random derangement: P(any edge → true target) = 0 by definition (no fixed points) ✓. Expected walk accuracy = 0.00 (deterministic) ✓. Bound: walk accuracy ≤ 0.05 → 0.00 ≤ 0.05 ✓ (single criterion, conservative).

### 12.5 Arm-coverage matrix (verifies full L18 enumeration across all 4 laws; updated for F3 ablation arms and F7 callable count)

| Law | Empty | Permuted | Shuffled | Oracle | Fair-naive | Frozen | Recency-only | Rehearsal-only | Section |
|---|---|---|---|---|---|---|---|---|---|
| L1 | ✓ (§2.8, §2.9) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (§2.8, §2.9) | ✓ (§2.8, §2.9) | §2.10 |
| L3 | ✓ (§3.8, §3.9) | ✓ | ✓ | ✓ | ✓ | ✓ | N/A (L3 has no factor-ablation analog) | N/A | §3.8 |
| L5 | ✓ (§4.7, §4.8) | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | N/A | §4.8 (plus full-scan chain-walker as a fifth, law-specific arm beyond the base 6) |
| L6 | ✓ (§5.5) | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | N/A | §5.5 |

Check: 4 laws × 6 mandatory L18 controls = 24 required cells, all 24 present and each with an exact (non-qualitative) pass condition cited above ✓. L1 has 2 additional ablation arms (recency-only, rehearsal-only) per F3, bringing L1's total to 8 controls ✓. No cell is marked "inapplicable" or "waived" anywhere in this document ✓. L6's reachability audit has **4 rows** (F7 fix: reconciled from v3's erroneous "5" — 2 + 0 + 2 = 4 callables, verified in §5.3) ✓.

### 12.6 Verdict-branch completeness check

Every law's §-numbered verdict section (§2.11, §3.10, §4.9, §5.6) contains exactly three branches — PASS, KILL, INSTRUMENT FAILURE — each with an exhaustive, exact condition list, and none references a downstream consumer (L1/L5, confirmed by direct re-read of §2.11 and §4.9) or a coupling property (L3/L6, confirmed by direct re-read of §3.10 and §5.6) ✓.

### 12.7 Output-artifact field check

Every arm table in §2.9, §3.9, §4.8, and §5.3/§5.4 specifies an explicit artifact schema (a `{...}` field list) — no arm's expected result is described without a corresponding recordable field set ✓.

### 12.8 Undefined-qualitative-term sweep

This document was checked for the terms "≈", "approximately", "toward", "roughly", "short" (unquantified), and "some" (as a stand-in for an unstated count), in every gate/pass/fail criterion. Occurrences found: **none** in any §2.9/§2.11, §3.9/§3.10, §4.8/§4.9, or §5.5/§5.6 criterion. (The word "short" appears only in v2's §4.1 table, which is superseded; v3's §4.1 uses exact integers throughout, e.g., "learned-early ≥ 50 cycles," "learned-late ≤ 5 cycles," with no unquantified qualitative descriptor retained.) Every empirical-null usage (§2.9, §4.8) specifies its exact derivation (1,000 seeded reassignments/permutations, mean ± 2 SD or a stated percentile), per O-13 and per C8's explicit instruction never to assume chance.

### 12.9 Cross-reference integrity check

All internal section references in this document (e.g., "§2.6", "§4.5", "§12.3") were checked against the actual heading numbers present in this document at write time; no reference points to a heading that does not exist in this document, and no heading number is duplicated (unchanged discipline from the v2 round's post-write fix, reapplied here before delivery).

### 12.10 Closure audit — F1–F7 and NF1–NF6 mapping (required by the tasking)

| Finding | Section(s) changed | What was done | Arithmetic verified |
|---|---|---|---|
| **F1** — L1 frozen/fair-naive controls are corners (tie-break = age proxy) | §2.4, §2.8, §2.9, §2.10, §12.1a | Tie-break changed from ascending creation cycle to seeded random permutation (seed=42, M1 B2 precedent). Fair-naive changed from append order to seeded random permutation (seed=43). Frozen R² = 0.236 ≤ null 95th = 0.749 ✓. Fair-naive R² = 0.320 ≤ 0.749 ✓. Permuted arm null re-derived from its own permutation distribution (F1a): R² = 0.000 within [−0.255, 0.764] ✓. | §12.1a (21 checks) |
| **F2** — Within-bin rehearsal assignment confounds rehearsal with age | §2.2, §2.6, §12.1a | Assignment changed from `⌊i/8⌋` to `i mod 5` (interleaved). Within-bin Spearman(level, age) = −0.1225 (was −1.0). Factor-inert candidate ρ < 0.6 for all 5 bins (0.20, 0.24, 0.20, 0.18, 0.13) ✓. Oracle ρ ≥ 0.6 for all 5 bins (0.91–0.95) ✓. | §12.1a |
| **F3** — §2.11 PASS gates on non-existent §2.9 bounds for recency-only/rehearsal-only | §2.8, §2.9, §2.10, §2.11, §12.1a, §12.5 | Added exact bounds for both arms in §2.9, checklist in §2.10, PASS/INSTRUMENT FAILURE conditions in §2.11. Recency-only: R²=0.926, β_age=−0.00229, all ρ<0.6 ✓. Rehearsal-only: β_age=0.0005≥0, all ρ≥0.6 (0.97–0.98) ✓. | §12.1a |
| **F4** — Accessibility quantity under-defined; oracle satisfiability underived | §2.4, §12.1a | Pre-registered: 100 candidate sets, exactly 5 appearances/entry, mean-of-log aggregation rule. Oracle R²=0.985≥0.85, β_age=−0.00150<0 ✓. | §12.1a |
| **F5** — L5 frozen arm expectation doesn't follow from definition; no freeze point | §4.5, §4.7, §4.8, §4.9, §12.4 | Redesigned with head pointer frozen at cycle 100. Pre-freeze: (c,0)–(c,4) at cycles 0–99. Post-freeze: (c,5)–(c,9) at cycles 100–199. All 40 queries post-freeze. Walk accuracy=0.00 by construction ✓. | §12.4 |
| **F6** — L5 shuffled-chain null contradicts graph and probability model | §4.8, §12.4 | Edge count corrected 190→180 (20×9). Derangement expectation = 0 (no fixed points). Bound fixed to single criterion: walk accuracy ≤ 0.05 (conservative, expected=0.00) ✓. | §12.4 |
| **F7** — L6 callable count contradiction (4 vs 5) | §5.3, §5.6, §12.5 | Count reconciled to 4 everywhere: "four named public callables," "4 rows," "all 4 reachability-audit rows." 2+0+2=4 ✓. | §12.5 |
| **NF1** — L3 frozen-floor scope discrepancy (§3.7 vs §3.9) | §3.7 | Harmonized to every-horizon scope (stricter of the two) ✓. | — |
| **NF2** — Seed ledger completeness claim overstates coverage | §8.1 | Claim narrowed to "E1 and M3 seed-use events." M1's non-M3 seed usage noted ✓. | — |
| **NF3** — STATE.md is stale | §11 | Noted as INTEGRATOR's responsibility; STATE.md must be current before Rebecca rules ✓. | — |
| **NF4** — Timing methodology should inherit E1's batch-fallback fix | §2.5, §4.4 | Batch-fallback language added to both timing sections ✓. | — |
| **NF5** — Fair-naive artifact field scope imprecise | §4.8, §4.9 | `combo_accuracy` scoped to world-validity queries only ✓. | — |
| **NF6** — Full-scan arm delta presumes separate chain-fixture log | §4.5, §4.8 | Chain-fixture log separation stated explicitly ✓. | — |

---

## Sources

All grounding is internal, binding program material; no external sources are used:

- `ARCHITECTURAL_CONSTITUTION.md` (uploaded attachment `f5eb8f8009794f8b85d0612d0c77cdff`)
- `M0_DECISION_SHEET.md` (uploaded attachment `f42c1bf94c1c478b90740883e0067f6b`) — adopted bars, §1
- `REBECCA_RESPONSE_M0.md` (uploaded attachment `00de0092afb04182a1e7eb936d38fb68`) — adoption, Persistence Doctrine D1–D5, §8.2 item 7
- `critic_m3_scope_review.md` — first blocking review (B1–B10, NB1–NB5) against `m3_scope_proposal.md`
- `critic_m3_e2_spec_rereview.md` — second blocking review (RB1–RB8, non-blocking notes) against `m3_e2_spec_amended.md`
- `critic_m3_e2_spec_rereview_v2.md` — third blocking review (C1–C8, NB1–NB3) against `m3_e2_spec_amended_v2.md`, resolved in v3
- `critic_m3_e2_spec_rereview_v3.md` — fourth blocking review (F1–F7, NF1–NF6) against `m3_e2_spec_amended_v3.md`, resolved in this document
- `m3_e2_spec_amended.md` — v1, superseded
- `m3_e2_spec_amended_v2.md` — v2, superseded
- `m3_e2_spec_amended_v3.md` — v3, superseded by this document
- `m3_e2_spec_changelog.md`, `m3_e2_spec_changelog_v2.md`, `m3_e2_spec_changelog_v3.md` — prior changelogs, superseded by `m3_e2_spec_changelog_v4.md`
- `architect_one_page_plan.md`, `critic_annotated_objections.md` — original M0-era M3 sketch and objections
- `m3_scope_proposal.md` — the first (blocked) draft
- `/home/user/workspace/repo_update/state/STATE.md` — governing state, main commit `1626bb09d9645ccdf2a2126325b2934dc12e2c5d`, M2 sealed/accepted status

All are workspace-internal files with no public URL, consistent with an internal build-organization deliverable for Rebecca's private-repository continuation gate.
