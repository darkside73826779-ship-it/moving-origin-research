# CRITIC REVIEW — E1 SPEC (The Moving-Origin Experiment)

**Date:** 2026-08-15 · **Reviewer:** CRITIC · **Spec under review:** `e1_spec.md` (ARCHITECT, 2026-08-15)
**Authority:** Rebecca standing instruction (Entry 25): §6 (equivalence test) is the review's center of gravity. Same falsifiability bar as M1.

---

## Summary Verdict

**NOT CLEARED — 5 BLOCKING + 12 NON-BLOCKING**

The spec is impressively structured — the candidate mechanism is explicitly distinct from the idea (§1), the D2 distinctness table is pre-registered (§1.2.3), the courier packet is fully specified (§7), the scope fence is tight (§8), and the L19 base-rate duty is satisfied (§11). The M0-locked numeric bars (N=10, latency ≤ 2×, equivalence ≤ 0.90, 3 seeds, 5 kill conditions) are all correctly carried forward.

However, **two of the five kill conditions are unsatisfiable for a correct candidate** — kill (a) (equivalence/collapse) and kill (d) (latency/scanning). A candidate that is implemented exactly as the spec defines it will trigger both by construction. This is not falsification; it is a foregone conclusion. The root cause is that the spec defines the candidate's coordinates as the *same computation* naive recomputation performs, and the latency test conflates algorithmic complexity with answer-set size.

Additionally, the "broken" state (distinguishable-but-wrong) has no defined verdict in the kill/delivery logic, and the shuffled-cadence arm contains an ambiguous "OR" between two non-equivalent implementations.

**The spec must be revised and re-reviewed before Rebecca's go/no-go gate.**

---

## BLOCKING Issues

### B1 — §6 (Equivalence test): The test is unsatisfiable; a correct candidate always collapses

**Classification:** BLOCKING (not falsifiable — the passing condition cannot be met by any correct implementation)

**The core problem:** The equivalence test compares the candidate's `coord_landmark_relative` answers to the naive arm's `now − created_at` recomputation. But the spec defines these as the *same computation*:

- **Candidate** (§1.2.1): `coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.cycle, AT_L if ==, AFTER_L if >`
- **Naive** (§6.1): `naive_coord_landmark_relative(e, L) = BEFORE_L if e.created_at < L.created_at else (AT_L if == else AFTER_L)`
- **Spec** (§1.2.1): "`e.created_at` — the autobiography position at append time (equals `e.cycle` at append)"

Since `e.created_at == e.cycle` and `L.created_at == L.cycle` by spec definition, the candidate and naive perform *the identical comparison*. A correctly-implemented candidate will **always** produce `agreement = 1.0`, triggering kill (a) (collapse, agreement > 0.90).

The spec acknowledges this in §6.5: "If the re-resolution is **correct**, they agree (agreement = 1.0 — and the candidate collapses, correctly). If the re-resolution is **incorrect** ... they differ (agreement < 1.0 — and the candidate is 'distinguishable' but **wrong**)."

This means:
- **Correct candidate** → agreement = 1.0 → collapse → kill (a) fires.
- **Buggy candidate** → agreement ≤ 0.90 → distinguishable → but oracle_agreement < 1.0 → "broken" (not coherent).

There is **no outcome** where `equivalence_agreement ≤ 0.90 AND oracle_agreement == 1.0` (the passing condition in §6.6). The test is unsatisfiable. A test that cannot be passed is not a falsification test — it is a foregone conclusion dressed as a gate.

**Why this happens:** The candidate's `coord_landmark_relative` is a *static* comparison of two fixed integers (`e.cycle` and `L.cycle`). It does **not** re-resolve as `now` advances — the spec itself states this (§1.2.1: "stays stable"). The only coordinate that genuinely re-resolves is `coord_cycle_relative = now − e.cycle`, but the offset-counter update produces the *same value* naive recomputation would (both compute `now − created_at`). The offset counter (C1.1) is a *performance optimization*, not a *semantic difference* — it computes the same answers, just in O(1) instead of O(n).

**Why "distinguishable from naive" is impossible without being wrong:** Both the candidate and naive read the same inputs (`e.cycle`/`e.created_at`, `L.cycle`/`L.created_at`, `now`). The candidate's coordinates are *defined* as functions of these same inputs. There is no additional information, no different computation, and no state the candidate carries that naive doesn't. A correct candidate using the same inputs will always produce the same answers as naive.

**Required fix:** The candidate must have coordinates that incorporate information *beyond* `now − created_at` — i.e., coordinates that legitimately differ from naive recomputation while remaining correct (matching oracle). Options:
1. **Redefine `coord_landmark_relative` to incorporate `now` in a non-canceling way** — e.g., "is e in the window between L and now" (changes as `now` advances), or a recency-weighted landmark relation.
2. **Test on `coord_cycle_relative` queries with a twist** — e.g., queries whose *ground truth* depends on `now` in a way that a `created_at` column alone cannot answer (multi-landmark joint coordinates, temporal windows relative to now).
3. **Acknowledge Candidate 1 is designed to collapse and reframe E1 as "death with diagnosis"** — not a pass/fail gate. But this contradicts the spec's delivery criteria (§10.3 requires "equivalence axis coherent" for green).

The ARCHITECT must redesign the candidate's coordinates so that a correct implementation can legitimately differ from naive recomputation, or redesign the equivalence test so it measures a dimension where the candidate adds information. As written, the test is vacuous in the worst direction: it kills every correct candidate.

---

### B2 — §4/§5(d) (Latency test): The test is unsatisfiable; answer-set size grows with history

**Classification:** BLOCKING (not falsifiable — kill (d) fires for any correct implementation)

**The problem:** The latency bar measures `latency(10×) / latency(1×)` on `query_landmark_relative` calls. The 200 queries are ~50/50 BEFORE_L / AFTER_L, with all landmarks in the initial build (entries 0–99). As history grows from 100 to 1000 entries:

- **BEFORE_L queries** return a constant-size set (entries before L are all in the initial build; new entries have higher cycles and are AFTER most landmarks).
- **AFTER_L queries** return a set that grows from ~50 entries (1×) to ~500–950 entries (10×).

The mean answer size grows ~10× (verified by computation: 49.5 → 499.5, ratio ≈ 10.1). Since `query_landmark_relative` materializes and returns the set of content_ids (§1.2.2 operation 3: "return the set of content_ids"), the latency is dominated by answer serialization, not by the lookup algorithm:

| Implementation | 1× latency ≈ | 10× latency ≈ | Ratio |
|---|---|---|---|
| O(1) indexed lookup | O(50) | O(500) | ~10× |
| O(n) scanning | O(150) | O(1500) | ~10× |

**Both exceed 2.0.** Kill (d) fires regardless of whether the index scans or uses O(1) lookup. The test cannot distinguish indexed from scanning (both are ~10× due to answer size), and it fires for a correct candidate.

**Required fix:** One of:
1. **Measure latency on queries with bounded answer size** — e.g., "return the k most recent entries before L" (bounded by k, constant at both scales), or "is entry e before L?" (O(1) answer).
2. **Measure BEFORE_L queries only** — their answer size is constant at both scales (~50), so the ratio isolates algorithmic complexity (indexed ≈ 1.0, scanning ≈ 10×).
3. **Normalize latency by answer size** — report latency-per-returned-element, so answer-size growth cancels out.
4. **Measure lookup time only** (not serialization) — if the index returns a reference/handle to the pre-computed set rather than materializing it. But the spec says "return the set of content_ids," so this requires a spec change.

As written, kill (d) is a foregone conclusion — the candidate is designed to fail it.

---

### B3 — §3 Arm 2 (shuffled cadence): Ambiguous "OR" between non-equivalent implementations

**Classification:** BLOCKING (not implementable — two valid readings produce different `chain_integrity` results)

**The problem:** The shuffled-cadence arm says: "Append the same 1000 entries but in a **shuffled order** ... The hash chain is therefore broken (entries' `prev_hash` no longer reference the actual predecessor in the shuffled order — **OR**, equivalently, the chain is built over the shuffled order, destroying the temporal cadence)."

These two options are **not equivalent**:

- **Option A** (broken chain): entries are stored in shuffled order, but `prev_hash` still references the original predecessor. `verify_chain()` walks storage order, finds mismatches → `chain_integrity = False`. ✓ Matches expected result ("Chain integrity check FAILS").
- **Option B** (valid chain over shuffled order): the chain is rebuilt over the shuffled append order (each entry's `prev_hash` references the previous entry in shuffled order). `verify_chain()` walks the shuffled chain → `chain_integrity = True`. ✗ Contradicts expected result.

The BUILDER could implement either. Option A makes kill (b) fire on the shuffled arm; Option B doesn't. The arm's purpose ("contamination control — cadence destroyed → chance") is undermined if the chain remains valid.

**Required fix:** Remove the "OR." Specify exactly one implementation. If the intent is that chain integrity fails (as the expected result states), specify: "Append entries in shuffled order; each entry's `prev_hash` references the predecessor in the *original* (unshuffled) order, so `verify_chain()` (which walks storage order) detects the mismatch." If the intent is that the chain is valid but the cadence is destroyed, change the expected result to `chain_integrity = True` and explain what the arm tests instead.

---

### B4 — §6.6 (Verdict logic): The "broken" state (distinguishable-but-wrong) has no defined verdict

**Classification:** BLOCKING (not falsifiable — a candidate can fall through the gaps of the kill/delivery logic)

**The problem:** §6.6 defines three states:
- **Coherent:** `equivalence_agreement ≤ 0.90 AND oracle_agreement == 1.0` → passes the equivalence axis.
- **Collapsed:** `equivalence_agreement > 0.90` → kill (a) fires.
- **Broken:** `equivalence_agreement ≤ 0.90 AND oracle_agreement < 1.0` → "NOT a kill condition as locked, but a defect."

The "broken" state is neither green (equivalence axis not coherent) nor red (no kill condition fires). The delivery criteria (§10.3) require "equivalence axis is coherent" for green. But if no kill condition fires and the equivalence axis is not coherent, what is the verdict?

- **Not green** (criterion b fails: equivalence axis not coherent).
- **Not red** (no kill condition fires; D1 says only kill conditions kill candidates).
- **Candidate status:** alive? dead? undefined.

The spec says "the JUDGE must report" the broken state, but does not define what happens to the candidate. Can the program proceed to M3? Can D2 retry? Is the candidate dead or alive?

**This is the loophole the ARCHITECT's PENDING REBECCA item 2 attempts to close.** A candidate that intentionally introduces noise to pass the collapse check (agreement ≤ 0.90) while being wrong (oracle_agreement < 1.0) would:
- Not trigger kill (a).
- Not trigger any other kill condition.
- Be "broken" — but with no defined verdict.

**Required fix:** Define the verdict for the "broken" state. Two options:
1. **Make `oracle_agreement < 1.0` a kill condition (the ARCHITECT's proposal, PENDING REBECCA item 2).** Then "broken" = kill (f) fires → candidate dead. This closes the loophole cleanly.
2. **Define "broken" as a non-green, non-red state with a specific routing** — e.g., "candidate survives but M2 is not delivered; the program pauses for Rebecca's decision (fix the re-resolver and re-run as a BUILDER fix, or treat as a candidate death)." But this risks interpretation at scoring time, which Rebecca's instruction forbids.

The CRITIC recommends option 1 (add `oracle_agreement < 1.0` as kill condition (f)). See PENDING REBECCA item 2 recommendation below.

---

### B5 — §1.2 (Candidate mechanism): The candidate violates L4 by construction

**Classification:** BLOCKING (violates a locked constitution law — L4)

**The problem:** L4 states: "A created_at column FAILS this law (coordinates never re-resolve)." The constitution's test requires that "the index does NOT collapse to recomputing `now − created_at`."

The spec's Candidate 1 IS a `created_at` column with a performance optimization:
- `coord_cycle_relative(e) = now − e.cycle` = `now − e.created_at` (the offset counter maintains this incrementally, but the *value* is identical to naive recomputation).
- `coord_landmark_relative(e, L) = e.cycle < L.cycle` = `e.created_at < L.created_at` (a static comparison that does not re-resolve for existing pairs).

The candidate's coordinates are *functions of the same inputs* naive recomputation uses. The offset counter (C1.1) is an O(1) update mechanism — it produces the same answers as naive, just faster. It adds no information beyond the timestamp column. The candidate collapses to recomputation *by design*.

**This is the root cause of B1.** The equivalence test catches this collapse — but since the candidate is *defined* to collapse, the test is a foregone conclusion, not a falsification.

**L4's requirement that coordinates "re-resolve as now advances"** is only partially met:
- `coord_cycle_relative` re-resolves (the value changes as `now` advances) — but the re-resolved value is `now − created_at`, which is what naive recomputes. Re-resolution without semantic difference is not what L4 requires.
- `coord_landmark_relative` does NOT re-resolve for existing (e, L) pairs (the spec admits this: "stays stable"). Only new pairs are computed — which naive also does correctly.

**Required fix:** Same as B1 — the candidate must have coordinates that carry information beyond `now − created_at`, so that re-resolution produces *different answers* than naive recomputation (while remaining correct). The ARCHITECT's own §6.5 admits this is impossible with the current candidate definition: "distinguishable from naive is NOT the same as better than naive." But if the candidate CAN'T be distinguishable from naive while being correct, then L4 is unfalsifiable for this candidate — the candidate fails L4 by construction.

Alternatively, the ARCHITECT may intend Candidate 1 as a deliberately minimal test case ("the simplest possible re-resolver; if the simplest dies, a learned re-resolver is a Candidate 2 option"). If so, the spec should state this explicitly and frame E1 as a *diagnostic* run (expected to collapse, with the diagnosis feeding the D2 retry decision) rather than a *pass/fail gate*. But this contradicts §10.3's delivery criteria (which require "equivalence axis coherent" for green).

---

## NON-BLOCKING Issues

### N1 — §3 Arm 6 (wall-clock-injection): Vacuous against the spec-defined candidate

**Classification:** NON-BLOCKING (robustness — the arm tests for a bug the spec prevents by construction)

The candidate's coordinate computations use `e.cycle` (§1.2.1: `coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.cycle`), not `e.created_at`. The wall-clock-injection arm "replaces `created_at` with a wall-clock timestamp" — but the candidate doesn't read `created_at` for its coordinates. The injection has no effect on the candidate's answers. Kill (e) cannot fire for a spec-compliant candidate.

The arm is a valid *defensive check* against a BUILDER who accidentally uses `created_at` (wall-clock-corruptible) instead of `e.cycle`. But since the spec defines `created_at = e.cycle` and the candidate uses `e.cycle`, the arm tests for an implementation deviation, not a mechanism-level L11 violation. The candidate has no path to a private clock by construction.

**Suggested fix:** If the intent is to test whether the candidate's *cycle counter* is wall-clock-derived (not just `created_at`), specify the injection as perturbing `e.cycle` itself (or the `now` value) and check whether coordinates shift. Otherwise, acknowledge the arm is a defensive check against implementation bugs, not a mechanism test.

---

### N2 — §4.1 (Oracle-vs-naive sanity check): Vacuous

**Classification:** NON-BLOCKING (PENDING REBECCA item 1 — recommend DROP)

Both the oracle and naive arms compute the ground truth correctly (oracle scans the autobiography; naive recomputes from `created_at`). Since `created_at == cycle`, they produce identical answers. `oracle_agreement_vs_naive = 1.0` always. The sanity check "oracle agreement with naive ≤ 0.90" always fails.

This vacuity is a *symptom* of B1: if oracle and naive always agree, and the candidate (when correct) always agrees with both, then the candidate-vs-naive test is also vacuous. Dropping the oracle-vs-naive sanity check is correct (it tests nothing), but the underlying problem (candidate-vs-naive is also vacuous) remains.

**Recommendation:** DROP the sanity check. But recognize that its vacuity signals the deeper problem in B1.

---

### N3 — §3 Arm 1 (frozen origin): Expected result has incorrect reasoning

**Classification:** NON-BLOCKING (clarity — the arm's expected result describes a scenario that doesn't occur)

The expected result says: "Frozen answers **diverge** from the candidate's re-resolved answers on queries whose landmark L was appended during the shift probe or 10× growth (frozen doesn't know about new landmarks)."

But all 10 landmarks are in the initial build (§2.3 step 1: landmarks are a "seeded random 10% subset" of the 100 initial entries). No landmark is "appended during the shift probe or 10× growth." The scenario the expected result describes doesn't occur.

The frozen arm *does* diverge from the candidate — but for a different reason: AFTER_L queries return more entries at 10× history (the candidate's re-resolved index knows about new entries; the frozen index doesn't). The frozen index returns only entries 0–99; the candidate returns entries 0–999. They diverge on AFTER_L queries (different set sizes), not because of "new landmarks."

**Suggested fix:** Correct the expected result: "Frozen answers diverge from the candidate on AFTER_L queries, because the frozen index (built at now=99) does not include entries 100–999, while the candidate's re-resolved index does. The frozen index returns a subset of the candidate's answer set."

---

### N4 — §7.3.2 (I3 contamination): Null distribution ambiguously specified

**Classification:** NON-BLOCKING (clarity — the null source is not explicitly stated)

The I3 method says: "estimate the chance arm's sampling distribution from >=100 seeded null replicates." But it doesn't specify *which arm* generates the null. The M1 precedent used "naive arm with ≥30 seeds" — but in M1, the naive arm was the *chance floor* (uniform random). In E1, the naive arm is a *correct recomputation* (oracle_agreement ≈ 1.0), not chance. Using the naive arm as the null in E1 would make every contamination arm fail I3 (their oracle_agreement is 0.0–0.5, far outside a null band centered at 1.0).

The intent appears to be: for each contamination arm, run ≥100 replicates of *that arm* with different seeds, compute the distribution, and check if the 3-seed mean falls in the 99% interval. This is a self-consistency check (not a chance-level verification, as L18 intends). The `empty` arm's check is additionally vacuous — `oracle_agreement = 0.0` deterministically (returns nothing, nothing matches), so the null distribution is degenerate [0.0, 0.0].

**Suggested fix:** Explicitly state which arm generates the null for each contamination arm. If the null is the contamination arm's own distribution (self-consistency), say so. If the intent is to verify "chance returns to chance," define what "chance" means for `oracle_agreement` (e.g., random set selection) and use that as the null. Clarify that the `empty` arm's I3 check is trivially satisfied (degenerate distribution).

---

### N5 — §7.3.5 (L20 drift self-test): Perturbation descriptions underspecified

**Classification:** NON-BLOCKING (clarity — the BUILDER could implement the perturbations differently)

The E1 profile lists two perturbations: `metric_block_reversal` and `candidate_empty_swap`. Unlike M1 (which precisely defined `full_arm_block_reversal` as reversing the arm-block order of the profile vector, with the exact before/after sequence), E1's perturbation descriptions are vague:
- "metric_block_reversal" — reverse the order of the 7 metrics? Reverse metric blocks within each arm? The profile is a single flat vector of 7 floats; "block reversal" is ambiguous.
- "candidate_empty_swap" — swap the candidate's metrics with the empty arm's metrics? But the profile vector doesn't include the empty arm's metrics (it includes `frozen_oracle_agreement`, not `empty_oracle_agreement`).

**Suggested fix:** Specify the exact vector transformation for each perturbation (before → after), as M1 did. E.g., "metric_block_reversal: reverse the 7-element profile vector [m0,m1,...,m6] → [m6,m5,...,m0]."

---

### N6 — No reproducibility check (I1-equivalent missing)

**Classification:** NON-BLOCKING (completeness — M1 had I1; E1 doesn't)

M1's invariant suite included I1 (reproducibility — bit-identical re-run, with per-seed `max_abs_diff` map). E1 has no equivalent within-run determinism check. The per-query agreement arrays ship in the artifact (§6.7), allowing the JUDGE to recompute aggregates — but there's no check that a re-run with the same seed produces identical results.

**Suggested fix:** Add a reproducibility invariant: re-run all 3 seeds a second time within the same process; verify bit-identical results; ship a per-seed `max_abs_diff` map (as M1 did). The cost is trivial.

---

### N7 — §3 (Control arms): `permuted` arm from L18 is missing

**Classification:** NON-BLOCKING (constitution compliance — L18 specifies empty/permuted/shuffled; E1 has empty/shuffled but not permuted)

L18 (constitution §4) requires "empty/permuted/shuffled → chance." M1 had all three contamination controls. E1's 6 arms include `empty` and `shuffled_cadence` but not a `permuted` arm (label/item permutation). The `wall-clock-injection` arm replaces it (as Rebecca specified), but wall-clock-injection is an L11 probe, not a contamination control.

The `shuffled_cadence` arm (order permutation) partially serves the `permuted` role, but it's a different kind of permutation (append-order, not label/item). E1 may be missing a distinct contamination dimension.

**Suggested fix:** If Rebecca's 6 arms are locked as-is, acknowledge that the `permuted` contamination dimension is not independently tested at E1 and log this as a known gap. Alternatively, add a `permuted` arm (permute content_id ↔ entry mapping) as a 7th control.

---

### N8 — §7.3.5 (Profile vector): Includes a control arm's metric

**Classification:** NON-BLOCKING (robustness — the profile mixes candidate and control metrics)

The 7-element profile vector includes `frozen_oracle_agreement` (the frozen arm's oracle_agreement) as the 7th element. The other 6 are candidate metrics. Including a control arm's metric in the candidate's naming profile may make the L20 drift test less focused — a drift in the frozen arm (a control) would trigger a drift flag on the candidate's name.

**Suggested fix:** Either (a) drop `frozen_oracle_agreement` from the profile vector (keep it as a reported metric, not a profile element), or (b) document why a control arm's metric belongs in the candidate's naming profile.

---

### N9 — §7.3.1 (Output schema): `arms` config includes "candidate" as a 7th entry

**Classification:** NON-BLOCKING (clarity — minor labeling inconsistency)

The `config.arms` array lists 7 entries: 6 control arms + "candidate." §3 says "6 control arms." The candidate is the system under test, not a control arm. This is a minor labeling inconsistency that could confuse the JUDGE.

**Suggested fix:** Either rename to `config.control_arms` (6 entries) + `config.candidate` (1 entry), or clarify in the schema that `arms` includes the candidate.

---

### N10 — §1.2.3 (D2 distinctness): C1.3 conflates chain construction and cycle counter

**Classification:** NON-BLOCKING (clarity — the kill condition diagnoses split C1.3 but the distinctness table doesn't)

The kill condition diagnoses (§5) reference C1.3a (SHA-256 chain) and C1.3b (cycle counter) as separate mechanistic choices. But the D2 distinctness table (§1.2.3) lists C1.3 as a single item: "Append-only hash-chained autobiography with a persisted monotone cycle counter." A Candidate 2 that changes only the hash function (C1.3a) or only the cycle counter type (C1.3b) might not be clearly "mechanistically distinct" under the current table.

**Suggested fix:** Split C1.3 into C1.3a (chain construction: SHA-256 vs Merkle tree) and C1.3b (cycle counter: integer increment vs Lamport logical clock) in the distinctness table, matching the kill condition diagnoses.

---

### N11 — §7.3.1 (Artifacts): No intermediate chain_integrity checks

**Classification:** NON-BLOCKING (completeness — needed to distinguish construction bugs from re-resolution corruption, PENDING REBECCA item 3)

The output schema reports `chain_integrity` as a single boolean per seed (after all stages). To distinguish "chain construction is wrong" (BUILDER defect) from "re-resolution corrupts the chain" (mechanism death) — which PENDING REBECCA item 3 asks Rebecca to rule on — the artifacts need `chain_integrity` at each stage: after initial build, after shift probe, after 10× growth.

**Suggested fix:** Add `chain_integrity_after_initial_build`, `chain_integrity_after_shift_probe`, `chain_integrity_after_10x_growth` (all booleans per seed) to the output schema. If the chain is valid after initial build but invalid after shift probe, the break is in re-resolution (mechanism death). If invalid from the start, it's a construction bug.

---

### N12 — §7.3.1 (Artifacts): No intermediate shift measurements

**Classification:** NON-BLOCKING (completeness — needed to distinguish wiring defects from mechanism death, PENDING REBECCA item 4)

The output schema reports `coordinate_shift` as a single boolean per seed. To distinguish "wiring defect" (offset counter not connected to append path) from "mechanism death" (re-resolution mechanism doesn't shift), the artifacts need per-append shift measurements.

**Suggested fix:** Add `shift_per_append` (array of 10 booleans, one per shift-probe append) per seed, showing whether each append produced the expected +1 shift. If all 10 are False, it's a wiring defect. If some are True and some False, it's a partial mechanism failure.

---

## Recommendations on the 4 PENDING REBECCA Items

### Item 1 (§4.1): Is the oracle-vs-naive sanity check vacuous?

**CRITIC assessment: YES, it is vacuous.** Both oracle and naive compute ground truth correctly and produce identical answers (`oracle_agreement_vs_naive = 1.0` always). The sanity check "oracle agreement with naive ≤ 0.90" always fails.

**Recommendation: DROP the sanity check.** It tests nothing. The equivalence test against the *candidate* is the load-bearing check.

**Critical caveat:** The vacuity of oracle-vs-naive is a *symptom* of B1. If oracle and naive always agree, and the candidate (when correct) always agrees with both, then the candidate-vs-naive test is equally vacuous. Dropping the oracle-vs-naive check removes a confusing non-test, but does not fix the fundamental unsatisfiability of the candidate-vs-naive equivalence test. See B1 for the required fix.

---

### Item 2 (§6.6): Should `oracle_agreement < 1.0` be a 6th kill condition?

**CRITIC assessment: YES, add it — but recognize it doesn't fix B1.**

Adding `oracle_agreement < 1.0` as kill condition (f) closes the "distinguishable but wrong" loophole (B4). Without it, a candidate that intentionally introduces noise to pass the collapse check (agreement ≤ 0.90) while being wrong (oracle_agreement < 1.0) falls through the gaps — no kill fires, but the equivalence axis is not coherent, leaving an undefined verdict.

**Recommendation: ADD kill condition (f): `oracle_agreement < 1.0` → candidate is broken (distinguishable from naive but wrong).** Trigger: `oracle_agreement < 1.0` (averaged over 3 seeds, with strict `== 1.0` required for coherence). This is a genuine loophole closure, not over-fencing — a correct candidate matches oracle exactly (oracle_agreement = 1.0), so this kill only fires for genuinely broken re-resolvers.

**However:** This does not fix B1. Even with kill (f) added, a correct candidate still triggers kill (a) (collapse, agreement = 1.0 > 0.90). The fundamental problem — that the candidate's coordinates are identical to naive recomputation by construction — remains. Kill (f) only prevents *buggy* candidates from passing as coherent; it doesn't make *correct* candidates pass.

---

### Item 3 (§11.2, kill b): Is a chain-break in construction a candidate death or a builder defect?

**CRITIC assessment: The distinction is valid and implementable — ACCEPT, with a required artifact addition (N11).**

A SHA-256 chain construction bug (C1.3a) is a BUILDER defect: the mechanism is sound, the implementation is wrong. Fixing it and re-running is NOT result laundering (the run never scored — per §0.7, only scoring runs through Rebecca's courier channel count; a construction bug would be caught in development runs). A re-resolution that corrupts the chain IS a mechanism death — the candidate's own re-resolution step breaks L2.

**Recommendation: ACCEPT the ARCHITECT's proposal.** Kill (b) is a candidate death only if the break is in re-resolution (chain was valid after construction, broke after re-resolution). A construction break is a BUILDER defect (fix and re-run, not result laundering).

**Required artifact (N11):** Add intermediate `chain_integrity` checks (after initial build, after shift probe, after 10× growth) to the output schema, so the JUDGE can determine *when* the chain broke. Without intermediate checks, the single boolean cannot distinguish construction defects from re-resolution corruption.

---

### Item 4 (§11.2, kill c): Is no-shift a wiring defect or mechanism death?

**CRITIC assessment: Same disposition as item 3 — ACCEPT, with a required artifact addition (N12).**

A no-shift result (the offset counter doesn't increment) could be:
- **Wiring defect:** the re-resolution step is not connected to the append path (BUILDER bug — the mechanism is sound, the wiring is wrong).
- **Mechanism death:** the re-resolution mechanism itself doesn't produce a shift (the offset-counter design is fundamentally broken).

**Recommendation: ACCEPT the same disposition as item 3.** Kill (c) is a candidate death only if the re-resolution mechanism is wired to the append path but doesn't shift. A wiring defect (re-resolution not called on append) is a BUILDER defect (fix and re-run).

**Required artifact (N12):** Add per-append shift measurements (`shift_per_append` array) to the output schema, so the JUDGE can distinguish "never shifts" (wiring defect) from "shifts partially" (mechanism failure). Additionally, the development runs (§0.7, non-scoring) should verify the re-resolution is wired before the scoring run.

---

## §6 Deep-Dive (Center of Gravity)

### What is reconstructed

§6.1 specifies: the naive reconstruction recomputes `coord_landmark_relative(e, L)` by scanning the autobiography's `created_at` column. For each query, it reads `created_at` for every entry, computes the landmark-relative relation, and returns matching content_ids.

**Assessment:** The reconstruction is *explicitly specified* — the formula, the inputs, and the output are all pinned. No ambiguity in *what* is reconstructed.

**However:** The reconstruction is *identical* to the candidate's computation (B1). The spec defines `coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.cycle`, and the naive recomputes `BEFORE_L if e.created_at < L.created_at`, where `created_at == cycle`. The "reconstruction" is not a different method — it is the same method applied at query time instead of append time. The test measures whether storing the result at append time (candidate) differs from computing it at query time (naive). For a correct implementation, they never differ.

### From what inputs

§6.2 specifies: both the candidate and naive read the same autobiography (same entries, same `created_at`, same landmarks, same `now`, same queries). The only difference is the method.

**Assessment:** The inputs are *fully specified and symmetric*. This is good experimental design — it isolates the test to the method, not the data.

**However:** because the inputs are identical and the candidate's coordinate functions are *defined* in terms of those same inputs, the candidate and naive *must* agree. The symmetry that makes the test clean also makes it vacuous.

### Agreement measured how

§6.3 specifies: per-query agreement is binary exact-set equality (`1 if candidate_answer(q) == naive_answer(q) else 0`). Aggregate agreement is the mean over 200 queries, averaged over 3 seeds. The formula is given explicitly.

**Assessment:** The agreement metric is *fully specified as a formula, not prose*. This satisfies Rebecca's instruction. No interpretation is left for scoring time — the JUDGE applies arithmetic to the per-query agreement arrays.

**However:** the metric is correct in form but vacuous in content. Exact-set equality will always be 1.0 for a correct candidate (same inputs, same computation → same outputs). The metric measures *whether the candidate is buggy*, not *whether the candidate is a genuine re-resolving index*.

### "Collapse" vs "coherent" — unambiguously defined?

§6.4 defines:
- **Collapse:** `equivalence_agreement > 0.90` → kill (a) fires.
- **Coherent:** `equivalence_agreement ≤ 0.90 AND oracle_agreement == 1.0`.

**Assessment:** The definitions are *unambiguous* — clear numeric thresholds, no prose interpretation. This satisfies Rebecca's instruction.

**However:** the definitions are *unsatisfiable*. "Coherent" requires `agreement ≤ 0.90` (distinguishable from naive) AND `oracle_agreement == 1.0` (correct). But:
- To be distinguishable from naive (agreement ≤ 0.90), the candidate must produce *different* answers than naive on >10% of queries.
- The candidate's coordinates are *defined* as the same computation naive performs.
- The only way to produce different answers is to be *buggy* (mis-compute coordinates).
- A buggy candidate won't match the oracle (oracle_agreement < 1.0).
- Therefore "coherent" (distinguishable AND correct) is impossible.

The definitions are unambiguous but describe a state that cannot exist for any implementation of the spec as written.

### Could "distinguishable but wrong" pass?

The ARCHITECT claims the oracle cross-check (§6.6) prevents this. **The logic is correct but incomplete:**

- The oracle cross-check requires `oracle_agreement == 1.0` for "coherent." A "distinguishable but wrong" candidate (agreement ≤ 0.90, oracle_agreement < 1.0) would NOT be "coherent" → would not pass the equivalence axis → would not be green.
- BUT: "distinguishable but wrong" is NOT a kill condition (as locked). So the candidate is not dead (D1: only kills kill candidates). It's in an undefined state — not green, not red. See B4.
- If Rebecca adds kill (f) (PENDING REBECCA item 2, recommended above), then "distinguishable but wrong" = kill (f) fires → candidate dead → the loophole is closed.

**Assessment:** The oracle cross-check *logic* is sound (it does prevent "distinguishable but wrong" from being called "coherent"). But without kill (f), the "broken" state has no verdict. The cross-check prevents false positives but creates an undefined state. Adding kill (f) closes this completely.

### Is the oracle-vs-naive distinction real?

**No.** Oracle and naive both compute the ground truth correctly. Oracle scans the autobiography; naive recomputes from `created_at`. Since `created_at == cycle`, both produce identical answers. `oracle_agreement_vs_naive = 1.0` always. The distinction is not real (see N2 / PENDING REBECCA item 1).

This is the canary for B1: if oracle and naive are indistinguishable, and the candidate is correct (matches oracle), then the candidate is also indistinguishable from naive. The equivalence test cannot distinguish a correct candidate from naive because they are the same computation.

### Is there any interpretation left for scoring time?

**No — the scoring is arithmetic (§6.7).** The JUDGE reads `equivalence_agreement` and `oracle_agreement` from the artifact, applies the locked bars, and checks the per-query agreement arrays. This is exemplary — no judgment calls, fully reproducible. The problem is not in the scoring procedure but in the *test design*: the scoring is correct arithmetic on a vacuous test.

### §6 verdict

§6 is *explicitly specified* (satisfying Rebecca's "fully explicit" instruction) but *unsatisfiable* (failing Rebecca's "no interpretation at scoring time" intent, because the only possible scores are "collapse" or "broken" — "coherent" is unreachable). The spec earns full marks for *explicitness* and zero marks for *falsifiability*. The test as written cannot be passed by any correct implementation of the candidate as defined.

The root cause is architectural, not notational: the candidate's coordinates are defined as the same computation naive performs. No amount of specification precision can make a vacuous test non-vacuous. The fix requires redesigning the candidate's coordinates (so a correct candidate legitimately differs from naive) or redesigning the equivalence test (so it measures a dimension where the candidate adds information). This is the ARCHITECT's job; the CRITIC flags the gap and the constraint.

---

## Constitution Compliance Summary

| Law | Compliance | Notes |
|---|---|---|
| **L2** (append-only hash-chained cadence) | ✓ Compliant | Append-only autobiography, SHA-256 chain, strictly monotone cycle counter, `verify_chain()` audit. Correctly specified. |
| **L4** (egocentric index) | ✗ **Violated by construction** (B5) | The candidate IS a `created_at` column with an O(1) optimization. Coordinates are identical to naive recomputation. L4 explicitly says "A created_at column FAILS this law." |
| **L10** (abstention under drift) | N/A | L10 is M4, explicitly out of scope for E1. No self-reports at E1. |
| **L11** (one clock) | ⚠ Partially tested (N1) | Wall-clock-injection arm is vacuous against the spec-defined candidate (candidate uses `e.cycle`, not `created_at`). The arm tests for implementation bugs, not mechanism-level L11 violations. |
| **L18** (control battery) | ⚠ Missing `permuted` (N7) | 6 arms include empty/shuffled but not permuted. Rebecca specified the arms; gap is logged. |
| **L19** (pre-registration) | ✓ Compliant | §11 pre-registers graveyard classification, outcome base-rates, D3 convergence watch. |
| **L20** (honest naming / drift) | ✓ Compliant (minor: N5) | Profile vector + drift self-test specified. Perturbation descriptions underspecified (N5). |

---

## Internal Consistency Checks

| Check | Result |
|---|---|
| §4 bars match M0 decision sheet | ✓ N=10, latency ≤ 2×, equivalence ≤ 0.90, 3 seeds, 5 kill conditions — all correctly carried forward |
| §5 kill conditions match §4 metrics | ✓ (a)→E1-M1, (b)→E1-M3, (c)→E1-M4, (d)→E1-M2, (e)→E1-M5 |
| §3 control arms match Rebecca's specification | ✓ 6 arms match Rebecca's E1 authorization (Entry 25) |
| Courier packet (§7) matches M1 structure | ✓ One script + pinned deps + one command + 5 output files |
| Timebox (§10) matches M1 budget | ✓ 3 sessions / 7 days |
| D2 retry budget = 3, spent 0 | ✓ Consistent throughout |

---

## Summary of Required Fixes (prioritized)

### Must fix before Rebecca's gate (BLOCKING):

1. **B1/B5: Redesign the candidate's coordinates or the equivalence test** so a correct candidate can legitimately differ from naive recomputation while remaining correct. As written, kill (a) is a foregone conclusion — the candidate collapses to naive by construction. This is the single most important fix.
2. **B2: Fix the latency test** so it measures algorithmic complexity, not answer-set size. Use bounded-answer queries, BEFORE_L-only queries, or normalize by answer size. As written, kill (d) fires for any correct implementation.
3. **B3: Remove the "OR" in the shuffled-cadence arm** and specify exactly one implementation.
4. **B4: Define the verdict for the "broken" state** — add kill (f) (`oracle_agreement < 1.0`) or define a specific routing for non-green-non-red candidates.

### Should fix before build (NON-BLOCKING, selected):

5. N3: Correct the frozen-origin arm's expected-result reasoning.
6. N4: Specify the I3 null distribution source explicitly.
7. N5: Specify L20 perturbation transformations precisely (as M1 did).
8. N6: Add a reproducibility check (I1-equivalent).
9. N11/N12: Add intermediate chain_integrity and shift measurements to artifacts (supports PENDING REBECCA items 3 and 4).

---

*Review ends. Hand back to ARCHITECT for revision, then to Rebecca for the E1 go/no-go gate. The center-of-gravity finding (B1/B5) is structural: the spec must either give the candidate coordinates that genuinely differ from naive recomputation, or acknowledge that Candidate 1 is designed to collapse and reframe E1 accordingly.*
