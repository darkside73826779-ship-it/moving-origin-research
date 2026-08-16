# CRITIC RE-REVIEW — E1 SPEC (Revised Draft v2, post-CRITIC-review)

**Date:** 2026-08-15 · **Reviewer:** CRITIC · **Spec under review:** `e1_spec.md` (ARCHITECT, revised draft v2)
**Prior review:** `critic_e1_spec_review.md` (5 BLOCKING + 12 NON-BLOCKING + 4 PENDING REBECCA)
**Authority:** Rebecca standing instruction (Entry 25) — §6 (equivalence test) is the review's center of gravity; same falsifiability bar as M1.

---

## Summary Verdict

**ALL BLOCKING CLEARED. 2 minor non-blocking observations remain (do not prevent the gate).**

The ARCHITECT's revision is substantive and correct. The root cause of B1/B5 — that the candidate's `coord_landmark_relative` was *defined* as the same computation naive recomputation performs — is genuinely fixed by introducing **landmark designation as a deferred event** (a separate `designate_landmark()` operation recorded in the append-only history). The candidate's `coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.designated_at` now depends on the *designation event*, which a `created_at` column cannot recover. The existence proof (§6.5) is non-vacuous: the candidate matches the oracle (correct) AND differs from naive (distinguishable) on deferred-designation landmarks. The simulation confirms `equivalence_agreement ≈ 0.77–0.84` (below the 0.90 bar, not trivially 0.0) with `oracle_agreement = 1.0` across seeds 42/43/44.

The latency test (B2) is redesigned on bounded-output queries, isolating algorithmic complexity from answer-set size. The shuffled-cadence "OR" (B3) is removed. The "broken" state (B4) is routed to kill (f) `[PENDING REBECCA SIGN-OFF]`. The candidate no longer violates L4 (B5). All 12 non-blocking issues are addressed. All locked bars are carried forward verbatim — no bar laundering.

The spec is **ready for Rebecca's go/no-go gate** (with the 4 PENDING REBECCA items for her ruling).

---

## BLOCKING Issues — Verification (5/5 RESOLVED)

### B1/B5 — Equivalence test unsatisfiable / candidate violates L4 → **RESOLVED**

**The fix:** Landmark designation is now a **deferred event** (§1.2.1, §1.2.2 operation 6 `designate_landmark`). The candidate's `coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.designated_at` (designation event). Naive uses `L.created_at` (= `L.cycle`, the append position) — the only timestamp a `created_at` column has. When designation is deferred (`L.designated_at > L.cycle`), entries in `[L.cycle, L.designated_at)` are `BEFORE_L` for the candidate/oracle but `AFTER_L` for naive.

**Existence proof verified (§6.5):** Concrete instance — L appended at cycle 10, designated at cycle 15; entry f appended at cycle 12. Query "entries before L":
- Oracle: `f.cycle (12) < L.designated_at (15)` → BEFORE_L → includes f. ✓
- Candidate: `12 < 15` → BEFORE_L → includes f. **Matches oracle (correct).** ✓
- Naive: `f.created_at (12) < L.created_at (10)` → FALSE → AFTER_L → excludes f. **Differs from candidate (distinguishable).** ✓

`candidate == oracle` (correct) AND `candidate != naive` (distinguishable). The "coherent" state is reachable.

**Simulation run (`verify_existence_proof_v2.py`):** I executed the ARCHITECT's simulation. Results for Scenario C (8 immediate + 2 deferred landmarks, matching the spec's `N_landmarks_immediate=8`, `N_landmarks_deferred=2`):

| Seed | `equivalence_agreement` | `oracle_agreement` |
|------|------------------------|--------------------|
| 42   | 0.770                  | 1.000              |
| 43   | 0.835                  | 1.000              |
| 44   | 0.810                  | 1.000              |

Mean `equivalence_agreement ≈ 0.805` — **below the 0.90 collapse bar** (not trivially 0.0), with `oracle_agreement = 1.0` on all seeds. The "coherent" state (`agreement ≤ 0.90 AND oracle_agreement == 1.0`) is **genuinely reachable and non-trivial**.

**Is this a genuine semantic difference or a trick?** This is the central question, and I assess it is **genuine, not a trick**:

- The naive arm is defined as "a `created_at` column + scan" (§3 arm 4, §6.1). A `created_at` column records, by definition, the append position of each entry. It does NOT record subsequent events — including when an entry was *later designated* a landmark. Designation is a separate event class from append (§1.2.1: "The autobiography records TWO classes of events: (i) append events, (ii) designation events").
- The naive arm's input restriction (§6.2: "naive does NOT receive `designated_at` — it only has the append-position timestamp") is a **faithful representation of what a `created_at` column has**, not an artificial data-stripping. A timestamp column at append time genuinely cannot recover designation timing.
- The candidate's index tracks designation events (C1.4) via the `LandmarkRegistry` — information a `created_at` column structurally cannot carry. This is the information that makes the candidate non-collapsible.
- The oracle arm (§3 arm 3) has perfect knowledge including designation events, and the candidate matches it — confirming the candidate is *correct*, not just *different*.

The test now has three genuine, reachable outcomes:
1. **Correct candidate that tracks designation** → matches oracle, differs from naive on deferred landmarks → **coherent** (passes). ✓
2. **Candidate that ignores designation (uses `L.cycle` instead of `L.designated_at`)** → matches naive, differs from oracle → **collapse** → kill (a) fires. ✓
3. **Buggy candidate** → differs from both → **broken** → kill (f) fires. ✓

This is a legitimate falsification test, not a foregone conclusion.

**Does the candidate still violate L4?** No. L4 states: "A `created_at` column FAILS this law (coordinates never re-resolve)." The candidate's `coord_landmark_relative` depends on `L.designated_at` — a designation-event timestamp that a `created_at` column cannot recover. A `created_at` column + scan CANNOT answer "what did I hold before L **became a landmark**?" correctly when designation is deferred; it can only answer "what did I hold before L was **appended**?" — a different question. The `designated_at` distinction makes the candidate genuinely more than a `created_at` column. **L4 is satisfied. B5 is resolved.**

**Re-resolution check (L4 "coordinates re-resolve as now advances"):**
- `coord_cycle_relative(e) = now − e.cycle` re-resolves on every cycle (increases by 1). ✓
- `coord_landmark_relative(e, L)` re-resolves when new landmarks are designated (designation advances `now`; existing entries gain new landmark-relative coordinates relative to the newly designated landmark). In E1, 2 landmarks are designated during the N=10 shift probe, so existing entries gain 2 new landmark-relative coordinates — a measurable shift. ✓

**Verdict: B1 and B5 are RESOLVED.**

---

### B2 — Latency test unsatisfiable (answer-set size grows ~10×) → **RESOLVED**

**The fix (§4.1, §4.2):** The latency bar (E1-M2) is now measured on **bounded-output queries**:
- `query_membership(e, L, relation)` — O(1) answer (single boolean).
- `query_landmark_relative_bounded(L, relation, k=10)` — bounded by k=10 (returns at most 10 entries).

Neither query type materializes an unbounded answer set, so the latency ratio isolates the lookup algorithm's complexity, not answer-set serialization.

**Verification of the four B2 sub-questions:**

1. **Is the latency test on bounded-output queries?** Yes (§4.1, §5d). Both query types have bounded output. ✓
2. **Does the ratio isolate algorithmic complexity from answer-set size?** Yes. `query_membership` returns 1 boolean; `query_landmark_relative_bounded` returns ≤10 entries. Neither grows with history. ✓
3. **Are raw materialization sizes still reported (just not barred)?** Yes (§4.2: `raw_answer_size_1x`, `raw_answer_size_10x`, `raw_answer_size_ratio` — expected ~10×, reported in the artifact §7.3.1, explicitly "REPORTED, not BARRED"). ✓
4. **Can an O(1) indexed implementation pass (ratio ≤ 2.0) while an O(n) scanning implementation fails (ratio > 2.0)?**
   - **Indexed:** `query_membership` is O(1) at both scales → ratio ≈ 1.0. `query_landmark_relative_bounded` is O(k) or O(log n + k) → ratio ≈ 1.0. Both ≤ 2.0. **Passes.** ✓
   - **Scanning:** `query_landmark_relative_bounded` requires scanning all entries to find the k most recent matches → O(n) at 1× (100 entries) vs O(10n) at 10× (1000 entries) → ratio ≈ 10× > 2.0. **Fails.** ✓

   The test distinguishes indexed from scanning. ✓

**Note:** `query_membership` is O(1) for *any* implementation (it's a single comparison of two integers), so it does not by itself distinguish indexed from scanning. The distinguishing power comes from `query_landmark_relative_bounded`. This is not a problem — the bar requires *both* to pass, and `query_landmark_relative_bounded` is the probe that catches scanning. `query_membership` is a redundant but harmless additional probe.

**Verdict: B2 is RESOLVED.**

---

### B3 — Shuffled-cadence arm ambiguous "OR" → **RESOLVED**

**The fix (§3 arm 2):** The "OR" is removed. Exactly one implementation is specified: "each entry's `prev_hash` references the predecessor in the **original (unshuffled) order**, so the entries are stored in shuffled order but their `prev_hash` fields point to the original predecessors. `verify_chain()` walks storage (shuffled) order, finds that each entry's `prev_hash` does NOT match the actual predecessor in shuffled order → `chain_integrity = False`."

**Verification:**
- Is the "OR" removed? Yes. §3 arm 2 specifies exactly one implementation. ✓
- Is exactly ONE implementation specified? Yes. ✓
- Does it produce the expected result (`chain_integrity = False`)? Yes — `verify_chain` walks shuffled storage order, finds `prev_hash` mismatches → `chain_integrity = False`. Matches the expected result ("Chain integrity check FAILS"). ✓

**Verdict: B3 is RESOLVED.**

---

### B4 — "Broken" state undefined → **RESOLVED**

**The fix (§0.5, §5f, §6.4, §6.6):** Kill condition (f) is added: `oracle_agreement < 1.0` → candidate is "broken" (distinguishable from naive but wrong). The "broken" state now has a verdict: kill (f) fires → candidate dead.

**Verification:**
- Is the "broken" state routed to a kill condition? Yes — §6.4 defines "Broken" as `equivalence_agreement ≤ 0.90 AND oracle_agreement < 1.0` → kill (f) fires. ✓
- Is kill (f) (`oracle_agreement < 1.0`) marked `[PENDING REBECCA SIGN-OFF]`? Yes — throughout §0.2, §0.5, §5f, §6.4, §6.6, §7.3.1, §7.3.2, §10.3a, and the consolidated PENDING REBECCA list at the end of the spec. ✓
- Is the fallback (if Rebecca does NOT sign off) defined? Yes — §0.5: "the candidate survives but M2 is not delivered green; the program pauses for Rebecca's decision." This is a non-green, non-red pause, not an undefined state. ✓

**Verdict: B4 is RESOLVED** (with kill (f) pending Rebecca's sign-off, as the CRITIC originally recommended).

---

## NON-BLOCKING Issues — Verification (12/12 ADDRESSED)

| # | Issue | Status | Evidence |
|---|-------|--------|----------|
| **N1** | Wall-clock-injection arm vacuous | **ADDRESSED** (acknowledged as defensive check) | §3 arm 6, §5e: the candidate uses `e.cycle` and `L.designated_at` (both autobiography-position-derived), not `created_at`. The arm is a defensive check against a BUILDER implementation bug, not a mechanism-level L11 test. Disposition parallels kill (b)/(c), marked `[PENDING REBECCA SIGN-OFF]`. |
| **N2** | Oracle-vs-naive sanity check vacuous | **ADDRESSED** (dropped) | §4.2, §7.3.2: the oracle-vs-naive sanity check is dropped per CRITIC recommendation. The equivalence test against the candidate (§6) is the load-bearing check. |
| **N3** | Frozen-origin expected-result reasoning incorrect | **ADDRESSED** (fixed) | §3 arm 1: corrected reasoning — frozen diverges on AFTER_L queries because the frozen index (built at now=99) does not include entries 100–999, and does not know about the 2 deferred landmarks designated at cycles 100–101. |
| **N4** | I3 null distribution ambiguously specified | **ADDRESSED** (fixed) | §0.9, §7.3.2: null generated by running ≥100 seeded replicates of **that same arm** (self-consistency null), NOT the naive arm. `empty` arm's null is degenerate [0.0, 0.0] — trivially in-band. Explicit per-arm null source listed. |
| **N5** | L20 perturbation descriptions underspecified | **ADDRESSED** (fixed) | §7.3.5: both perturbations have exact before→after vector transformations. `metric_block_reversal`: reverse 6-element vector [m0..m5] → [m5..m0]. `candidate_empty_swap`: swap candidate's 6 metrics with empty arm's 6 (all zeros) → [0,0,0,0,0,0]. |
| **N6** | No reproducibility check (I1-equivalent) | **ADDRESSED** (added) | §7.3.1 `reproducibility` object, §10.3e: re-run all 3 seeds a second time within the same process; verify bit-identical; ship per-seed `max_abs_diff` map. Added to delivery (green) criteria. |
| **N7** | Missing `permuted` arm from L18 | **ADDRESSED** (acknowledged as gap) | §0.4: L18 gap acknowledged. `shuffled_cadence` partially serves the `permuted` role. Rebecca specified 6 arms as-is (Entry 25). Logged per L19 pre-registration. Rebecca may add a 7th arm at the gate. |
| **N8** | Profile vector includes control arm metric | **ADDRESSED** (fixed) | §7.3.5: `frozen_oracle_agreement` dropped from the profile vector. Profile now has 6 elements — all candidate metrics. `frozen_oracle_agreement` remains a reported metric, not a profile element. |
| **N9** | `arms` config includes candidate as 7th entry | **ADDRESSED** (fixed) | §7.3.1: `config.control_arms` lists 6 control arms; `config.candidate` is a separate field. |
| **N10** | D2 distinctness conflates C1.3a/C1.3b | **ADDRESSED** (fixed) | §1.2.3: C1.3 split into C1.3a (SHA-256 vs Merkle tree) and C1.3b (integer vs Lamport). New row C1.4 (landmark designation as deferred event) added. Table now has 5 rows. |
| **N11** | No intermediate chain_integrity checks | **ADDRESSED** (added) | §5b, §7.3.1: `chain_integrity_after_initial_build`, `chain_integrity_after_shift_probe`, `chain_integrity_after_10x_growth` reported per seed. Supports PENDING REBECCA item 3. |
| **N12** | No intermediate shift measurements | **ADDRESSED** (added) | §5c, §7.3.1: `shift_per_append` (array of 8 booleans) reported per seed. Supports PENDING REBECCA item 4. |

---

## New-Issue Check

### Is the `designate_landmark()` operation fully specified?

**Yes.** §1.2.2 operation 6 specifies: increment the cycle counter; record a designation event in the autobiography (`event_type = "designation"`, `ref = entry`, `designated_at = new_now`); register in `LandmarkRegistry` with `L.designated_at = new_now`; then re-resolve the index (compute `coord_landmark_relative(e, L_new)` for all existing entries `e`). The operation is concrete and implementable. ✓

### Is the D2 distinctness table updated for Candidate 1.1?

**Yes.** §1.2.3 has 5 rows (C1.1, C1.2, C1.3a, C1.3b, C1.4). §1.2.4 has the distinctness note comparing original Candidate 1 (withdrawn) to Candidate 1.1, with a clear table of material changes. The retry budget is correctly tracked: 3, spent 0 (Candidate 1.1 is a pre-build revision, not a D2 retry). ✓

### Are the intermediate chain_integrity and shift measurements added to the output schema?

**Yes.** §7.3.1 `e1_run_results.json` includes `chain_integrity_after_initial_build`, `chain_integrity_after_shift_probe`, `chain_integrity_after_10x_growth` (booleans per seed), and `shift_per_append` (array of 8 booleans per seed). Also surfaced in `e1_invariants.json` (§7.3.2). ✓

### Is the I1-equivalent reproducibility check added?

**Yes.** §7.3.1 `reproducibility` object: re-runs all 3 seeds a second time within the same process, verifies bit-identical results, ships `max_abs_diff_per_seed`. Added to delivery criteria (§10.3e). ✓

### Is the I3 null distribution source now explicit?

**Yes.** §0.9, §7.3.2: per-arm null source explicitly listed (`shuffled_cadence`: self; `empty`: self, degenerate [0.0, 0.0]; `wall_clock_injection`: self). The naive arm is NOT used as the null. ✓

### Did the revision introduce any new problems?

Two **minor non-blocking** observations:

**NEW-1 (non-blocking): `candidate_empty_swap` perturbation produces a zero-variance vector, making Pearson correlation undefined.**

§7.3.5 defines `candidate_empty_swap` as swapping the candidate's 6-metric profile vector with the empty arm's 6 metrics (all zeros) → resulting vector `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`. The L20 drift criterion uses `pearson_corr(profile_vector, new_profile_vector)`. Pearson correlation with a constant (zero-variance) vector is mathematically undefined (0/0 → NaN). In most implementations, `NaN < 0.50` evaluates to `False`, so the perturbation would NOT flag drift — contradicting the spec's assertion that `both_perturbations_flag_drift: true`.

This is a BUILDER implementation edge case, not a falsifiability problem for the candidate. The fix is trivial: the spec should specify that `pearson_corr(x, const)` is defined as `0.0` (or `-∞`) when the second vector has zero variance, which trivially satisfies `< 0.50` and flags drift. The BUILDER can handle this; it does not affect the candidate's kill conditions or the equivalence test. **Non-blocking.**

**NEW-2 (non-blocking, cosmetic): §2.2 parenthetical imprecision.**

§2.2 states: "`N_cycles = 10` (the locked N — the number of appends after the initial build; the 'shift' is measured over these 10 cycles)." But §2.3 step 2 specifies that 2 of the 10 cycles are designation events and only 8 are appends. So "the number of appends" should read "the number of cycles" (8 appends + 2 designations = 10 cycles). The shift measurement (`shift_per_append`, 8 booleans) is internally consistent with §2.3. The parenthetical in §2.2 is imprecise but does not affect the test's validity. **Non-blocking.**

**No other new issues found.** The revision does not introduce any new blocking problems. The `designated_at` distinction is consistently applied throughout (§1, §3, §5, §6, §7). The candidate mechanism is fully specified and internally consistent.

---

## Bar-Laundering Check

| Bar | Locked value (M0 / constitution) | Spec value | Preserved? |
|-----|----------------------------------|------------|------------|
| Collapse bar | `equivalence_agreement ≤ 0.90` | §0.2, §6.4: `≤ 0.90` | ✓ Verbatim |
| Latency bar | `10× history ≤ 2× 1× history` | §0.2, §4.1: `≤ 2.0` | ✓ Verbatim (measured on bounded-output queries — instrumentation change, not bar change) |
| Shift bar | `N = 10 cycles` | §0.2, §2.2: `N = 10` | ✓ Verbatim |
| Chain-integrity bar | `= 1.0` | §0.2, §4.1: `= 1.0` | ✓ Verbatim |
| Seeds | `3` (L4 not in 5-seed group) | §0.2, §2.2: `3` ([42, 43, 44]) | ✓ Verbatim |
| Kill conditions | `5 as locked` | §0.2, §5: 5 locked + 1 proposed `[PENDING REBECCA]` | ✓ Verbatim (kill (f) is explicitly proposed, not silently added) |
| Naive arm name | `naive now−created_at` | §0.4, §3 arm 4, §6.1: `naive now−created_at` | ✓ Preserved |
| Naive arm definition | recompute from `created_at` by scanning | §3 arm 4, §6.1: store `created_at` column, recompute by scanning, no re-resolving index, no designation tracking | ✓ Preserved |

**No bar is flipped, softened, raised, lowered, renamed, or redefined.** The revision changes the *candidate mechanism* (so the collapse bar is reachable) and the *test instrumentation* (so the latency bar measures algorithmic complexity), NOT the bars themselves. The naive arm keeps its name and definition. ✓

---

## §6 Center-of-Gravity Check

### Is the equivalence test still fully explicit?

**Yes.** §6.1 (what is reconstructed), §6.2 (from what inputs), §6.3 (agreement formula), §6.4 (collapse/coherent/broken definitions), §6.5 (existence proof), §6.6 (coherence cross-check), §6.7 (scoring is arithmetic). Every term is pinned — formula, inputs, output, thresholds. No ambiguity in *what* is reconstructed or *how* agreement is measured. ✓

### Is the scoring still arithmetic (no interpretation at scoring time)?

**Yes.** §6.7: the JUDGE reads `equivalence_agreement` and `oracle_agreement` floats from `e1_run_results.json`, applies the locked bars (`> 0.90` → kill (a); `≤ 0.90 AND == 1.0` → coherent; `≤ 0.90 AND < 1.0` → kill (f)), and verifies the arithmetic from the per-query agreement arrays (which ship in the artifact). No judgment calls. ✓

### Does the `designated_at` distinction create any new ambiguities in scoring?

**No.** The scoring reads pre-computed answer-sets from the artifact. The candidate's, naive's, and oracle's answer-sets are deterministic given their respective inputs (candidate: index with `designated_at`; naive: `created_at` column without `designated_at`; oracle: full autobiography with `designated_at`). The per-query agreement arrays are binary set-equalities. The `designated_at` distinction affects *what answers each arm produces* (a property of the implementation, not the scoring), not *how the JUDGE scores them*. No new ambiguity is introduced. ✓

### Is the naive arm's input restriction (no `designated_at`) defensible?

**Yes.** §6.2 explicitly justifies: "the fact that a `created_at` column (the naive arm's only structure) does NOT record designation events. Designation is a separate event class from append; a timestamp column at append time cannot recover when an entry was LATER designated a landmark." This is structurally correct — a `created_at` column records append positions, not subsequent designation events. The restriction faithfully represents what a `created_at` column has. It is not a data-stripping trick. ✓

### Is the "coherent" state genuinely reachable (not rigged)?

**Yes.** The 8-immediate / 2-deferred landmark mix produces `equivalence_agreement ≈ 0.80` — comfortably below the 0.90 bar (not marginally below), and not trivially 0.0. The mix is a pre-registered constant in the spec (§2.2), not a BUILDER-tunable parameter. The mix is the ARCHITECT's legitimate design choice to make the test non-vacuous (all-immediate → unsatisfiable; all-deferred → trivially 0.0; 8/2 → meaningful). This is not bar laundering — the bar (0.90) is unchanged; the test fixture is designed so the bar is reachable by a correct candidate. ✓

---

## Constitution Compliance (Re-verified)

| Law | Compliance | Notes |
|-----|------------|-------|
| **L2** (append-only hash-chained cadence) | ✓ Compliant | Append-only autobiography, SHA-256 chain, strictly monotone cycle counter (increments on both append AND designation events), `verify_chain()` audit. Designation events are also hash-chained (§1.2.1). |
| **L4** (egocentric index) | ✓ **Compliant** (was ✗ in v1) | Candidate's `coord_landmark_relative` depends on `L.designated_at` (designation event), NOT recoverable from a `created_at` column. Coordinates re-resolve as `now` advances (cycle-relative on every cycle; landmark-relative on new designations). L4 satisfied. |
| **L11** (one clock) | ✓ Defensive check (N1 acknowledged) | Candidate uses `e.cycle` and `L.designated_at` (both autobiography-position-derived). Wall-clock-injection arm is a defensive check against implementation bugs. |
| **L18** (control battery) | ⚠ Known gap (N7 acknowledged) | 6 arms include `empty`/`shuffled` but not a distinct `permuted`. Logged per L19. Rebecca may add a 7th arm at the gate. |
| **L19** (pre-registration) | ✓ Compliant | §11 pre-registers graveyard classification, outcome base-rates (updated for B1/B5 and B2 fixes), D3 convergence watch. |
| **L20** (honest naming / drift) | ✓ Compliant (minor: NEW-1) | Profile vector (6 candidate metrics) + drift self-test specified. Perturbation definitions precise (N5 fixed). Minor: `candidate_empty_swap` zero-variance edge case (NEW-1, non-blocking). |

---

## PENDING REBECCA Items (4 — CRITIC dispositions)

| # | Item | CRITIC disposition | Spec status |
|---|------|--------------------|-------------|
| 1 | Oracle-vs-naive sanity check | **DROP** (vacuous) | Dropped (§4.2, §7.3.2). ✓ |
| 2 | Kill condition (f): `oracle_agreement < 1.0` | **ADD** (closes B4 loophole) | Added, marked `[PENDING REBECCA SIGN-OFF]` throughout. ✓ |
| 3 | Construction-bug-vs-mechanism-death (kill b) | **ACCEPT** (with N11 artifacts) | Added with intermediate `chain_integrity` artifacts. ✓ |
| 4 | Wiring-defect-vs-mechanism-death (kill c) | **ACCEPT** (with N12 artifacts) | Added with `shift_per_append` artifacts. ✓ |

All four are incorporated with the CRITIC's original recommendations. Rebecca rules at the gate.

---

## Final Verdict

**ALL BLOCKING CLEARED. 2 minor non-blocking observations remain (do not prevent the gate).**

### Blocking issues: 5/5 RESOLVED

- **B1/B5** (equivalence test unsatisfiable / L4 violation): **RESOLVED.** The existence proof holds — the candidate tracks designation events that a `created_at` column cannot recover, making it genuinely distinguishable from naive while remaining correct (matching the oracle). Simulation confirms `equivalence_agreement ≈ 0.80` (below 0.90) with `oracle_agreement = 1.0`. L4 is satisfied.
- **B2** (latency test unsatisfiable): **RESOLVED.** Latency measured on bounded-output queries; raw materialization sizes reported separately, not barred. An O(1) indexed implementation passes; an O(n) scanning implementation fails.
- **B3** (shuffled-cadence "OR"): **RESOLVED.** "OR" removed; one implementation (broken chain, `chain_integrity = False`).
- **B4** ("broken" state undefined): **RESOLVED.** Routed to kill (f) `[PENDING REBECCA SIGN-OFF]`.

### Non-blocking issues: 12/12 ADDRESSED

All 12 non-blocking issues (N1–N12) are fixed or acknowledged.

### New issues: 2 minor non-blocking (do not prevent the gate)

- **NEW-1** (non-blocking): `candidate_empty_swap` perturbation produces a zero-variance vector → Pearson correlation undefined. The spec should specify the edge-case handling (define `pearson(x, const) = 0.0`, which trivially flags drift). BUILDER implementation detail.
- **NEW-2** (non-blocking, cosmetic): §2.2 parenthetical says "the number of appends" but 2 of the 10 cycles are designations (8 appends). Cosmetic imprecision; does not affect test validity.

### Bar laundering: NONE

All locked bars carried forward verbatim. Naive arm name and definition preserved. No bar flipped, softened, raised, lowered, renamed, or redefined.

### Recommendation

**The spec is ready for Rebecca's go/no-go gate.** The 4 PENDING REBECCA items are incorporated with the CRITIC's recommendations. The 2 minor non-blocking observations (NEW-1, NEW-2) can be noted for the BUILDER but do not block the gate or the build. The center of gravity (§6 equivalence test) is fully explicit, satisfiable, and scored by arithmetic — no interpretation at scoring time.

---

*Re-review ends. Hand to Rebecca for the E1 go/no-go gate (§9 step 3).*
