# CRITIC RE-REVIEW (v3) — E1 SPEC (Revised Draft v3, post-Rebecca-gate-ruling)

**Date:** 2026-08-15 · **Reviewer:** CRITIC · **Spec under review:** `e1_spec.md` (ARCHITECT, revised draft v3, 1037 lines)
**Prior reviews:** `critic_e1_spec_review.md` (v1: 5 BLOCKING + 12 NON-BLOCKING + 4 PENDING REBECCA), `critic_e1_spec_rereview.md` (v2: ALL BLOCKING CLEARED, 2 non-blocking)
**Authority:** Rebecca's E1 gate ruling (2026-08-15, binding). Center of gravity per Rebecca's directive: **the fair-naive definition and the state-dependent query battery.**

---

## Summary Verdict

**ALL BLOCKING CLEARED. 6 NON-BLOCKING observations remain (do not prevent the gate).**

The v3 revision correctly implements Rebecca's three-property test. The fair-naive arm is genuinely the strongest honest timestamps-and-scan implementation — full event-log access (including designation events), recompute-by-scan at query time, no maintained index state, expected to match the candidate on answers (confirming the theorem), used only as a cost-scaling baseline. No hidden handicap. The state-dependent query battery is well-specified — 5 history-size points, both scaling curves reported, collapse criterion unambiguous. The downstream consumer is a valid L15 miniature. Kill conditions are correctly retired, signed, and promoted. All locked bars are carried forward verbatim. No bar laundering.

The 6 non-blocking observations concern: (1) a new kill-condition trigger (the 0.5 scaling-collapse threshold) that is not acknowledged as a new bar in the scope fence, unlike the 0.05 degradation floor; (2) the 0.05 degradation floor as a new bar; (3) the downstream consumer's content-similarity function being underspecified for a TASK BUILDER; (4) the consumer testing only `coord_cycle_relative`, not `coord_landmark_relative`; (5) an unaddressed edge case in the state-dependent battery at history size 100; (6) timing-precision robustness of the collapse criterion. None of these prevent the gate — all are flagged for Rebecca's attention or BUILDER clarification.

---

## 1. The three-property test — verification

### (i) Correctness — VERIFIED ✓

**oracle_agreement = 1.0 on the full query battery, including deferred-designation queries?** Yes. §6.i specifies "the full query battery — 200 landmark-relative queries per seed, including the ~20% that involve deferred-designation landmarks (whose ground truth depends on designation events that occurred at different points in the history)." The bar is `oracle_agreement = 1.0` (strict, §4.1 E1-M1, §6.i). The oracle is the `oracle index` arm (§3 arm 3) — a perfect-knowledge log replay using `L.designated_at`. ✓

**Kill (f) SIGNED (not PENDING)?** Yes. §0.2: "SIGNED." §0.5: "SIGNED and PROMOTED." §5f: "SIGNED. No longer PENDING. Rebecca signed kill (f) at the gate (ruling §4 item 3)." The changelog V3-2 confirms: "SIGNED and PROMOTED." ✓

**Is it the PRIMARY correctness kill?** Yes. §5f: "SIGNED and PROMOTED to primary correctness kill condition (property (i))." §6.i: "This is the floor: a candidate that is wrong has no place, regardless of its operational or integrative properties." ✓

**Is the scoring arithmetic?** Yes. §6.i: "the JUDGE reads `oracle_agreement` (a float) from `e1_run_results.json`, applies the bar (`< 1.0` → kill (f) fires), and verifies the arithmetic from the per-query agreement arrays (which ship in the artifact). No judgment calls." ✓

### (ii) Operational distinctness (CENTER OF GRAVITY) — VERIFIED ✓

#### The fair-naive arm — VERIFIED ✓ (see §4 below for deep-dive)

**Reads the FULL event log (including designation events)?** Yes. §3 arm 4: "reads the FULL event log — including designation events (`event_type = 'designation'`, `ref`, `designated_at`) — exactly as the oracle does." §6.ii: "reads the SAME event log the candidate and oracle read — including append events AND designation events." ✓

**Recompute-by-scan/replay at query time?** Yes. §6.ii: "for each query, it scans the autobiography and computes `fair_naive_coord_landmark_relative(e, L_q) = BEFORE_L if e.cycle < L_q.designated_at`." ✓

**Has NO maintained index state?** Yes. §6.ii: "NO offset counter, NO landmark registry with pre-computed coordinates, NO incrementally re-resolved structure. It recomputes from scratch on every query." ✓

**MATCH the candidate's answers (expected — no longer a kill)?** Yes. §6.ii: "fair-naive ≡ oracle on answers… MATCHES the candidate on answers — this is EXPECTED and no longer a kill." The reported `equivalence_agreement` (§4.2) is a diagnostic, expected ≈ 1.0, carrying NO kill. ✓

**DIFFER in cost scaling?** Yes. §6.ii: fair-naive is O(n) per query (scans the log); candidate is O(1)/O(log n) per query (reads maintained state). ✓

#### The state-dependent query battery — VERIFIED ✓ (see §5 below for deep-dive)

**Multiple history sizes (5 points: 100, 250, 500, 750, 1000)?** Yes. §2.2: `N_state_dependent_query_points = 5`, history sizes {100, 250, 500, 750, 1000}. §6.ii confirms. ✓

**Does fair-naive's per-query cost provably scale with history length?** Yes. §6.ii: "The fair-naive's per-query cost is O(n) (it scans the full log, including designation events, to recompute the coordinate for each entry). So `fair_naive_slope > 0` (linear)." ✓

**Does the candidate answer from maintained state (O(1) or O(log n))?** Yes. §6.ii: "The candidate's `query_membership` is O(1)… `query_landmark_relative_bounded` is O(log n) or O(1)… Neither scales with history size. So `candidate_slope ≈ 0` (flat)." ✓

**Are BOTH scaling curves reported?** Yes. §4.2: "`candidate_scaling_curve` and `fair_naive_scaling_curve` — the per-query latency at each of the 5 history-size points, for both the candidate and the fair-naive arm, plus the fitted slopes. REPORTED so the JUDGE and CRITIC can inspect the scaling curves directly." ✓

**Is the collapse criterion clear?** Yes. §6.ii: "Fail (collapse — kill (d) d2 fires): `candidate_slope > 0.5 × fair_naive_slope` — the candidate scales nearly as steeply as fair-naive." The criterion is a single numeric comparison. ✓

**Is the locked latency bar (10× history ≤ 2× latency) still present and UNCHANGED?** Yes. §0.2: "UNCHANGED in value; PROMOTED to the operational-distinctness discriminator (property (ii)). Extended with a state-dependent query battery (§6.ii)." §4.1 E1-M2: "≤ 2.0." The VALUE is ≤ 2.0 (verbatim from M0); the ROLE is promoted; the EXTENSION (d2) is new. ✓

**What is the specific collapse threshold?** `candidate_slope > 0.5 × fair_naive_slope` (§4.1 E1-M2b, §6.ii). This IS a new bar — see §3 below for the new-bar assessment.

### (iii) Load-bearing coupling — VERIFIED ✓

**Is the minimal downstream consumer well-specified?** Yes, with one non-blocking gap (see §8, NB-3). §6.iii: "a toy recency-weighted retrieval implementing L1's access physics over the index's coordinates." The consumer uses `relevance(e, q_item) = exp(-coord_cycle_relative(e) / τ) * content_similarity(e.payload, q_item)` with τ=50, k=10. ✓

**Is it a toy recency-weighted retrieval implementing L1's access physics?** Yes. L1 (constitution §1): "Accessibility of every knowledge item is a monotonic decaying function of self-relative recency and use frequency." The consumer's `exp(-coord_cycle_relative(e) / τ)` is a monotonic decaying function of self-relative recency (`coord_cycle_relative = now - e.cycle`). The consumer does not include use frequency, but the spec acknowledges it as a "toy" — "NOT the full L1 system (L1 is M3)" (§6.iii, §8). This is consistent with L1 as a miniature. ✓

**Does it consume the index's coordinates?** Yes. §6.iii: "the consumer's retrieval depends on `coord_cycle_relative(e)`, which the candidate re-resolves as `now` advances." ✓ (See NB-4 for the observation that only `coord_cycle_relative` is consumed, not `coord_landmark_relative`.)

**Is the ablation test clear?** Yes. §6.iii: The consumer is run over (1) the candidate's re-resolved index and (2) the frozen-origin index (built at now=99, never re-resolved). The frozen index's `coord_cycle_relative` is `99 - e.cycle` (stale for entries after cycle 99 — negative, causing `exp()` to inflate relevance for stale entries). ✓

**Frozen-origin arm: downstream consumer degrades?** Yes. §6.iii: "If the candidate's re-resolution is ablated (frozen-origin arm), the consumer's `coord_cycle_relative` is frozen at the `now=99` values, so entries appended after cycle 99 have stale (too-large) recency weights, and recall@k degrades." ✓

**Effect direction consistent across seeds?** Yes. §6.iii: "degradation > 0 on ALL 3 seeds (effect direction consistent across seeds)." ✓

**What is the degradation threshold?** §6.iii: "mean_degradation ≥ floor across the 3 seeds. The floor is pre-registered at 0.05." This IS a new bar — see §3 below.

**Is this correctly framed as a miniature of L15?** Yes. §6.iii: "This is a miniature of the L15 test (which M5 will apply in full): ablate A (re-resolution), measure degradation of B (the consumer's law-compliance — here, retrieval quality)." The scope fence (§8) confirms: "The property (iii) load-bearing coupling test is a MINIATURE of the L15 test… M5 applies L15 in full." ✓

---

## 2. Kill conditions — verification

### Old kill (a) RETIRED with rationale logged? — VERIFIED ✓

§5a: "RETIRED per Rebecca's E1 gate ruling (§12). The informational collapse test (answer-agreement vs naive) is unsatisfiable by construction." §12.1 documents the retirement with rationale: "Unsatisfiable by construction (Rebecca's theorem: fair-naive ≡ oracle on answers; the pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable)." The metric `equivalence_agreement` is retained as a REPORTED diagnostic (§4.2), carrying NO kill and NO distinctness claim. ✓

### Kill (f) SIGNED and PROMOTED to primary correctness kill? — VERIFIED ✓

See §1(i) above. SIGNED, PROMOTED, primary correctness kill. ✓

### Kill (d) PROMOTED to discriminator? — VERIFIED ✓

§5d: "PROMOTED to operational-distinctness discriminator (property (ii))." The latency bar (≤ 2.0) is UNCHANGED. The d2 extension (scaling_collapse) is NEW. Both d1 and d2 are triggers for kill (d). ✓

### All other kills (b, c, e) unchanged? — VERIFIED ✓

- Kill (b) (chain integrity): §5b — LOCKED. Construction-bug-vs-mechanism-death guard applied (Rebecca ruling §4 item 4). Intermediate chain_integrity artifacts (N11). ✓
- Kill (c) (no shift): §5c — LOCKED. Wiring-defect-vs-mechanism-death guard applied (Rebecca ruling §4 item 5). Per-append shift artifacts (N12). ✓
- Kill (e) (wall-clock): §5e — LOCKED. Defensive check (N1 acknowledged). Construction-bug guard applied. ✓

### Construction-bug guard applied? — VERIFIED ✓

§5 (intro): "Construction-bug-vs-mechanism-death guard (Rebecca ruling §4 items 4–5, APPROVED with guard): Bug attribution requires the specific defect identified, fixed, and CRITIC-confirmed before any re-run escapes the D2 budget. 'Probably a bug' never does." Applied to kills (b), (c), and (e). ✓

### Are any NEW bars introduced? — YES (2 new bars; see §3 below)

---

## 3. New bars assessment

### NB-1 (NON-BLOCKING): The 0.5 scaling-collapse threshold is a NEW kill-condition trigger, not acknowledged as a new bar in the scope fence

**The bar:** §4.1 E1-M2b, §6.ii: `candidate_slope > 0.5 × fair_naive_slope` → kill (d) d2 fires.

**Is it new?** Yes. It is not in the M0 decision sheet (which locked: N=10, latency ≤ 2.0, equivalence ≤ 0.90 [retired], 3 seeds). Rebecca's ruling §2(ii) authorized the collapse CRITERION ("the candidate collapses if its own scaling matches recompute-by-scan") but did not specify the numeric threshold. The 0.5 ratio is the ARCHITECT's operationalization of "matches."

**Is it marked [PENDING REBECCA SIGN-OFF]?** No. It is not marked [PENDING REBECCA SIGN-OFF] anywhere in the spec.

**Is it acknowledged as new?** Inconsistently. The scope fence (§8) says: "No bar invention, lowering, or raising. All numeric values are locked from M0 (and Rebecca's ruling)." But the 0.5 IS invented — it's not from M0 and not numerically specified by Rebecca. The spec DOES acknowledge the 0.05 degradation floor as new ("The new property (iii) floor (0.05) is pre-registered here per L19") but does NOT give the same acknowledgment to the 0.5 threshold.

**Is the threshold reasonable?** Yes. A correct candidate has `candidate_slope ≈ 0` (flat, O(1) per query) and `fair_naive_slope > 0` (linear, O(n) per query), so `candidate_slope / fair_naive_slope ≈ 0`, well below 0.5. A scanning candidate has ratio ≈ 1.0, well above 0.5. The 0.5 threshold sits between the two regimes and is a reasonable discriminator. It does not unfairly kill a correct candidate.

**Assessment:** NON-BLOCKING. The threshold is reasonable and pre-registered (in the spec before any run). Rebecca will see it at the gate. The CRITIC is directed to assess it (§9 step 2). However, the spec should:
1. Explicitly acknowledge the 0.5 threshold as a new bar (as it does for the 0.05 floor).
2. Either mark it [PENDING REBECCA SIGN-OFF] or state that it is an ARCHITECT-proposed operationalization of Rebecca's authorized criterion, with the CRITIC assessing falsifiability.

The inconsistency between acknowledging the 0.05 floor as new but not acknowledging the 0.5 threshold as new should be corrected before the gate.

### NB-2 (NON-BLOCKING): The 0.05 degradation floor is a NEW bar, acknowledged as new but not marked [PENDING REBECCA SIGN-OFF]

**The bar:** §6.iii: "mean_degradation ≥ 0.05 (a conservative E1-scale miniature floor; Rebecca's L15 floor of d ≥ 0.5 applies at M5 in full, not at E1's miniature)."

**Is it new?** Yes. Rebecca's ruling §2(iii) says "must measurably degrade" and "effect direction consistent across seeds" but does not specify a magnitude floor. The 0.05 is the ARCHITECT's operationalization of "measurably." The M0 decision sheet set d ≥ 0.5 for L15 (M5), but nothing for E1.

**Is it marked [PENDING REBECCA SIGN-OFF]?** No. But it IS acknowledged as new: "The floor is pre-registered here per L19; the CRITIC assesses whether it is falsifiable (non-trivially above zero, not so high no honest candidate can pass)" (§6.iii). The scope fence (§8) also acknowledges it: "The new property (iii) floor (0.05) is pre-registered here per L19 (the CRITIC assesses its falsifiability)."

**Is the threshold reasonable?** Yes. The frozen-origin index gives `coord_cycle_relative = 99 - e.cycle` for entries after cycle 99, which is negative, causing `exp(-(99 - e.cycle) / 50) = exp((e.cycle - 99) / 50)` to grow exponentially for post-99 entries. This produces drastically wrong recency weights, so the degradation should be large — likely well above 0.05 for any reasonable content-similarity function. The 0.05 floor is conservative.

**Is it a kill condition?** No — it is a gate on the E1 pass verdict (property (iii) failure routing, §5). If it fails, the candidate is not dead but E1 is not-green. This is less severe than a kill condition.

**Assessment:** NON-BLOCKING. The floor is acknowledged as new, pre-registered per L19, conservative, and not a kill condition. Rebecca will see it at the gate. The acknowledgment is sufficient. Rebecca should confirm at the gate.

---

## 4. Fair-naive definition (CENTER OF GRAVITY — deep-dive)

### Is the fair-naive the STRONGEST honest timestamps-and-scan implementation? — VERIFIED ✓

The spec defines the fair-naive (§3 arm 4, §6.ii) as:

1. **Full event-log access:** reads the SAME event log as the candidate and oracle — including append events AND designation events. NOT handicapped. ✓
2. **Recompute-by-scan at query time:** for each query, scans the autobiography and computes `fair_naive_coord_landmark_relative(e, L_q) = BEFORE_L if e.cycle < L_q.designated_at`. Does NOT pre-compute or cache coordinates. ✓
3. **No maintained index state:** NO offset counter, NO landmark registry with pre-computed coordinates, NO incrementally re-resolved structure. Recomputes from scratch on every query. ✓
4. **Same answers as candidate and oracle:** by Rebecca's theorem, fair-naive ≡ oracle on answers. MATCHES the candidate — expected, no longer a kill. ✓
5. **Differs in cost scaling:** fair-naive is O(n) per query; candidate is O(1)/O(log n) per query. ✓

### Is there any hidden handicap? — NO ✓

I examined the fair-naive for potential handicaps:

1. **Could the fair-naive be given less information than the candidate?** No — it reads the same event log, including designation events. The old `naive now−created_at` arm was handicapped (no designation events); the fair-naive is not. ✓

2. **Could the fair-naive be given a slower algorithm than necessary?** No — it scans the log, which is the natural O(n) approach for a stateless implementation. A "stronger" implementation might use binary search or a temporary index, but that would be maintaining state (a sorted structure), which the fair-naive explicitly does not do. The fair-naive is the strongest HONEST timestamps-and-scan implementation — it doesn't maintain any index state across queries. ✓

3. **Could the fair-naive's per-query cost be artificially inflated?** No — it performs a simple comparison (`e.cycle < L_q.designated_at`) per entry, which is O(1) per entry, O(n) total. This is the natural cost of scanning. ✓

4. **Could the fair-naive cache results across queries?** The spec says "recompute from scratch on every query" — no caching. Even if it cached within a batch (building a dictionary of landmark → designated_at), the per-query cost is still O(n) because each unique query requires scanning all n entries to compute coordinates. The slope (cost vs. history size) is linear regardless. ✓

5. **Is the fair-naive's computation the SAME function as the candidate and oracle?** Yes. All three compute `BEFORE_L if e.cycle < L.designated_at`. Same inputs, same function, same answers. By Rebecca's theorem, fair-naive ≡ oracle. ✓

**Verdict: the fair-naive is correctly defined as the strongest honest timestamps-and-scan implementation. No hidden handicap. No strawman.** ✓

### Sanity check: the `equivalence_agreement` diagnostic

§4.2: `equivalence_agreement` (candidate vs fair-naive) is REPORTED as a diagnostic, expected ≈ 1.0. If it is NOT ≈ 1.0 (e.g., < 0.95), it indicates the fair-naive is handicapped (a BUILDER bug). This is a good sanity check — it confirms the theorem holds and the fair-naive is not a strawman. The CRITIC checks this at review. ✓

---

## 5. State-dependent query battery (CENTER OF GRAVITY — deep-dive)

### Are the queries genuinely state-dependent? — VERIFIED ✓

§6.ii: "the queries' ground truth depends on the state of the index at the time of the query — specifically, on the designation events that have occurred by that history size. At history size 100, only the 8 immediate landmarks are designated (the 2 deferred landmarks are designated at cycles 100–101, which are AFTER the initial 100). At history size 250+, all 10 landmarks are designated."

At history size 100, queries about the 2 deferred-designation landmarks return different results than at history size 250+ (where the designations have occurred). The answers change as `now` advances. The queries are genuinely state-dependent. ✓

### Does fair-naive's cost provably scale with history length? — VERIFIED ✓

The fair-naive scans the full event log for each query. At history size 100, it scans ~100 entries. At history size 1000, it scans ~1000 entries. Per-query cost is O(n). The fitted slope is positive (linear). ✓

### Could the candidate's cost also scale with history length? — VERIFIED ✓

Yes — if the candidate secretly replays (scans the log at query time instead of reading maintained state), its cost would also be O(n). This is exactly what the collapse criterion catches: `candidate_slope > 0.5 × fair_naive_slope` → the candidate is secretly replaying. ✓

### Is the collapse detection criterion unambiguous? — VERIFIED ✓

`candidate_slope > 0.5 × fair_naive_slope` is a single numeric comparison. §6.ii specifies the linear regression (latency on history size, 5 points), the fitted slopes, and the threshold. The JUDGE reads two floats and computes a ratio. No judgment calls. ✓

### Are there queries where the candidate's O(1) lookup is genuinely testable? — VERIFIED ✓

`query_membership(e, L, relation)` is O(1) — a single comparison of two integers from maintained state. `query_landmark_relative_bounded(L, relation, k=10)` is O(log n) or O(1) — a lookup over the indexed coordinate. Both are testable at all 5 history-size points. The candidate's flat scaling (slope ≈ 0) is distinguishable from the fair-naive's linear scaling (slope > 0). ✓

### NB-5 (NON-BLOCKING): Queries about deferred-designation landmarks at history size 100 are not explicitly addressed

At history size 100, the 2 deferred-designation landmarks have NOT been designated yet (they are designated at cycles 100–101). The 200 queries (§2.4) include queries about these 2 landmarks. At history size 100, a query about an undesignated landmark asks "return entries before L" where L has no `designated_at` value yet.

The spec does not explicitly state what happens:
- Does the fair-naive return empty (L is not a landmark yet)?
- Does the candidate return empty (L is not in the LandmarkRegistry yet)?
- Is the query skipped?

This is an implementation detail that should be clarified. The fair-naive's cost is still O(n) regardless (it must scan the log to determine that no designation event exists for L_q). The scaling curve is still linear. The collapse criterion is still valid. But the BUILDER needs guidance on the expected behavior.

**Assessment:** NON-BLOCKING. The scaling property holds regardless of the answer (O(n) per query either way). But the spec should clarify the behavior for reproducibility.

### NB-6 (NON-BLOCKING): Timing-precision robustness of the collapse criterion

At the scales involved (100–1000 entries, O(1) operations take microseconds), wall-clock timing can be noisy. The fair-naive's fitted slope should be clearly positive (the difference between scanning 100 and 1000 entries is measurable), but the candidate's flat slope (≈ 0) could be slightly positive or negative due to noise.

If the fair-naive's fitted slope is near zero (e.g., due to timing noise at very small scales), the collapse criterion `candidate_slope > 0.5 × fair_naive_slope` could become `candidate_slope > 0` (if fair_naive_slope ≈ 0), which could be triggered by noise in the candidate's slope.

The spec does not specify:
- A minimum fair_naive_slope below which the collapse criterion is reported as inconclusive.
- A warm-up period or minimum repetition count for timing measurements.

**Assessment:** NON-BLOCKING. At the scales involved (100–1000 entries, O(n) scan), the fair-naive's slope should be clearly positive and the candidate's slope should be clearly near-zero, so the criterion should be robust. But the spec should acknowledge the edge case and specify timing methodology for the BUILDER (e.g., minimum 100 repetitions per query, warm-up runs, or a minimum fair_naive_slope guard).

---

## 6. Bar laundering check — VERIFIED ✓

| Bar | Locked value (M0 / constitution) | Spec value (v3) | Preserved? |
|-----|----------------------------------|-----------------|------------|
| **Latency bar** | `10× history ≤ 2× 1× history` (≤ 2.0) | §0.2, §4.1 E1-M2: `≤ 2.0` | ✓ Verbatim. PROMOTED to discriminator role; VALUE unchanged. |
| **N (cycles for shift)** | `N = 10` | §0.2, §2.2: `N = 10` | ✓ Verbatim |
| **Chain-integrity bar** | `= 1.0` | §0.2, §4.1 E1-M3: `= 1.0` | ✓ Verbatim |
| **Seeds** | `3` (E1 not in 5-seed group) | §0.2, §2.2: `3` ([42, 43, 44]) | ✓ Verbatim |
| **Equivalence tolerance** | `≤ 0.90` | §0.2: **RETIRED** | ✓ RETIRED (not softened). Metric retained as diagnostic. Unsatisfiable by construction per Rebecca's theorem. |
| **Oracle agreement** | Not in M0 (PENDING in v2) | §0.2: `= 1.0`, SIGNED | ✓ PROMOTED (not invented). Rebecca signed it at the gate (ruling §4 item 3). |
| **Naive arm** | `naive now−created_at` (handicapped) | §0.4: `fair naive` (full event-log access) | ✓ STRENGTHENED (not softened). Renamed and redefined to read the full event log. |
| **Kill conditions** | `5 as locked` | §0.2, §5: 5 active (b, c, d, e, f) | ✓ Old (a) RETIRED. Kill (f) SIGNED. Kill (d) PROMOTED. Total active: 5. |

**No locked bar is flipped, softened, raised, lowered, or redefined.** The retired ≤ 0.90 bar is RETIRED (not softened — it is unsatisfiable by construction). The = 1.0 oracle-agreement bar is PROMOTED (not invented — Rebecca signed it). The naive arm is STRENGTHENED (not softened — it reads the full event log). ✓

**New bars (0.5 scaling-collapse threshold, 0.05 degradation floor):** Both are NEW — not from M0 and not numerically specified by Rebecca. Both are pre-registered (in the spec before any run). Neither replaces or softens a locked bar. Both are flagged for Rebecca's attention (see NB-1, NB-2). The 0.5 threshold should be acknowledged as new (see NB-1). ✓

---

## 7. Constitution compliance — VERIFIED ✓

| Law | Compliance | Notes |
|-----|------------|-------|
| **L2** (append-only hash-chained cadence) | ✓ Compliant | Append-only autobiography, SHA-256 chain, strictly monotone cycle counter. Designation events are also hash-chained (§1.2.1). `verify_chain()` audits (§1.2.2 operation 8). Chain integrity holds under append, re-resolution, and designation. |
| **L4** (egocentric index, AMENDED) | ✓ Compliant | The three-property test (§6) genuinely tests that the index does not collapse to recompute-by-scan in COST (property ii: candidate O(1)/O(log n) vs fair-naive O(n)) AND that its re-resolution is load-bearing for downstream consumers (property iii: ablation degrades the consumer). The old informational collapse test (answer-agreement vs naive) is retired — unsatisfiable by construction per Rebecca's theorem. Coordinates re-resolve as `now` advances (structural check c: +1 per append; property iii: ablation degrades consumer). L4 is satisfied under the amended test. |
| **L1** (access physics, miniature) | ✓ Compliant (toy) | The downstream consumer (§6.iii) implements L1's access physics as a toy: `exp(-coord_cycle_relative / τ)` is a monotonic decaying function of self-relative recency. Use frequency not included — acknowledged as a toy, not the full L1 system. Consistent with L1 as a miniature. |
| **L18** (control battery) | ⚠ Known gap (N7, acknowledged) | 6 arms: frozen, shuffled, oracle, fair-naive, empty, wall-clock. Missing distinct `permuted` arm (label/item permutation). `shuffled_cadence` partially serves the `permuted` role. Acknowledged in §0.4 as a known gap. Rebecca may add a 7th arm at the gate. |
| **L19** (pre-registration) | ✓ Compliant | §11 pre-registers graveyard classification, outcome base-rates (updated for three-property test), D3 convergence watch. New bars (0.5, 0.05) pre-registered. |
| **L20** (honest naming / drift) | ✓ Compliant | §7.3.5: profile vector (6 candidate metrics), drift criterion (Pearson < 0.70), self-test (two perturbations). NEW-1 zero-variance edge case addressed (§7.3.5: `pearson_corr(x, const) = 0.0`). Perturbation definitions precise (N5 fixed). |

---

## 8. Internal consistency — VERIFIED ✓

| Check | Result |
|-------|--------|
| §4 metrics match the three properties | ✓ E1-M1 → (i), E1-M2 + E1-M2b → (ii), E1-M6 → (iii), E1-M3/M4/M5 → structural |
| §5 kill conditions match §4 metrics | ✓ (b)→E1-M3, (c)→E1-M4, (d)→E1-M2+E1-M2b, (e)→E1-M5, (f)→E1-M1. Property (iii) failure → E1-M6 (gate, not kill). |
| §7 output schema sufficient for JUDGE | ✓ All metrics, per-seed arrays, scaling curves, degradation values, kill condition verdicts, three-property verdict objects, reproducibility, I3, L20 self-test. |
| Courier packet complete | ✓ One script + pinned deps + one command + 5 output files (§7). |
| §6.iv three-property verdict matches §5 kill conditions | ✓ (i)→kill (f), (ii)→kill (d), (iii)→not-green routing, structural→kills (b)/(c)/(e). |
| §10.3 delivery criteria match §6.iv | ✓ (a) no kill fires, (b) property (i) = 1.0, (c) property (ii) ≤ 2.0 AND ≤ 0.5, (d) property (iii) > 0 AND ≥ 0.05, (e) structural, (f) I3, (g) L20, (h) reproducibility, (i) STATE.md, (j) manifest. |
| §12 amendment log complete | ✓ §12.1 (what changed), §12.2 (why — theorem + program finding), §12.3 (authority), §12.4 (credit). |

---

## 9. New issues from the v3 revision

### NB-3 (NON-BLOCKING): The downstream consumer's content-similarity function and query items are underspecified

§6.iii specifies the consumer's relevance function: `relevance(e, q_item) = exp(-coord_cycle_relative(e) / τ) * content_similarity(e.payload, q_item)`, with τ=50 and k=10. However:

1. **Query items:** The spec says "for each query item `q_item`" but does not specify the set of query items — how many, what they are (random vectors? entries from the autobiography? new synthetic items?), or how they are generated.
2. **Content similarity:** The spec says "content_similarity is a deterministic similarity function (e.g., cosine similarity over a synthetic feature vector in the payload)." The "e.g." makes this a suggestion, not a specification. The payload is described as "an opaque content blob" (§1.2.1) — the spec does not specify how to extract a feature vector from it.

**Impact:** Different BUILDER implementations could produce different degradation values. A similarity function that weights recency heavily (small τ, weak content signal) would produce large degradation; one that weights content heavily (strong content signal) would produce small degradation. The 0.05 floor could be trivially passable or impossibly hard depending on the implementation.

**Mitigating factors:** τ=50 is pinned, and the frozen index's recency weights are drastically wrong (negative `coord_cycle_relative` for entries after cycle 99 causes `exp()` to blow up), so the degradation should be large and positive for ANY reasonable similarity function. The 0.05 floor is conservative.

**Assessment:** NON-BLOCKING. The key property (degradation > 0) should hold for any reasonable implementation. But the spec should specify the exact similarity function, feature vector dimension/generation, and the set of query items for reproducibility. A TASK BUILDER needs more guidance.

### NB-4 (NON-BLOCKING): The downstream consumer tests only `coord_cycle_relative`, not `coord_landmark_relative`

The downstream consumer uses `coord_cycle_relative(e) = now - e.cycle` (the offset counter, C1.1). It does NOT use `coord_landmark_relative(e, L)` (the designation tracking, C1.4). The frozen-origin ablation freezes BOTH coordinates, but the consumer's degradation comes only from the frozen `coord_cycle_relative`.

**Impact:** The consumer tests whether the offset counter's re-resolution is load-bearing. It does NOT test whether the landmark-relative re-resolution (the deferred-designation mechanism, C1.4 — the novel part of Candidate 1.1) is load-bearing. A candidate with no designation tracking at all (just an offset counter) would produce the same degradation.

**Mitigating factors:**
1. Rebecca's ruling (§2(iii)) says "over the index's coordinates" — the consumer uses one of the index's coordinates, which is a valid reading.
2. The consumer is a "toy" — the full L15 test at M5 would test all couplings.
3. The frozen-origin arm freezes the entire index, so the ablation affects both coordinates — even though only one is measured.
4. `coord_cycle_relative` IS part of the candidate's re-resolution mechanism; testing its load-bearing property is a valid miniature of L15.

**Assessment:** NON-BLOCKING. The consumer tests the load-bearing coupling of the re-resolution mechanism as a whole (via `coord_cycle_relative`). The designation tracking (C1.4) is tested by property (i) (correctness — the candidate must match the oracle on deferred-designation queries) and property (ii) (the state-dependent battery's material comes from deferred designations). A more complete consumer would use both coordinates, but the toy is a valid miniature. This should be noted for M5.

---

## 10. Comparison with prior reviews

### v1 review (critic_e1_spec_review.md): 5 BLOCKING + 12 NON-BLOCKING + 4 PENDING REBECCA

All 5 BLOCKING issues are resolved across v2 and v3:
- B1/B5 (equivalence test unsatisfiable / L4 violation): DISSOLVED by Rebecca's theorem. The three-property test replaces the equivalence test. ✓
- B2 (latency test unsatisfiable): FIXED in v2 (bounded-output queries), RETAINED in v3. ✓
- B3 (shuffled-cadence "OR"): FIXED in v2, RETAINED in v3. ✓
- B4 ("broken" state undefined): FIXED in v2 (kill (f)), SIGNED in v3. ✓

All 12 NON-BLOCKING issues are addressed (see changelog §v2 NON-BLOCKING table, v3 status column).

All 4 PENDING REBECCA items are RESOLVED (Rebecca ruled on all four at the gate).

### v2 re-review (critic_e1_spec_rereview.md): ALL BLOCKING CLEARED, 2 non-blocking

- NEW-1 (candidate_empty_swap zero-variance): ADDRESSED in v3 (§7.3.5: `pearson_corr(x, const) = 0.0`). ✓
- NEW-2 (§2.2 parenthetical imprecision): ADDRESSED in v3 (§2.2 now says "8 appends + 2 designations = 10 cycles"). ✓

### v3 new observations: 6 non-blocking (this review)

See NB-1 through NB-6 above. None are blocking. All are flagged for Rebecca's attention or BUILDER clarification.

---

## 11. Did the v3 revision introduce any new BLOCKING problems? — NO

The v3 revision correctly implements Rebecca's binding ruling:

1. **The three-property test is correctly implemented.** (i) Correctness (kill f, signed), (ii) operational distinctness (kill d, promoted, state-dependent battery), (iii) load-bearing coupling (new, L15 miniature). All three properties are satisfiable, genuine, and scored by arithmetic.

2. **The fair-naive arm is genuinely fair.** Full event-log access (including designation events), recompute-by-scan at query time, no maintained index state. No hidden handicap. No strawman. Expected to match the candidate on answers (confirming the theorem). Used only as a cost-scaling baseline.

3. **The state-dependent query battery is well-specified.** 5 history-size points, both scaling curves reported, collapse criterion unambiguous. The queries are genuinely state-dependent. The candidate's O(1)/O(log n) lookup is genuinely testable against the fair-naive's O(n) scan.

4. **All locked bars are carried forward verbatim.** No bar laundering. The retired ≤ 0.90 bar is RETIRED (not softened). The = 1.0 oracle-agreement bar is PROMOTED (not invented). The naive arm is STRENGTHENED (not softened).

5. **The constitution amendment is properly documented.** §12 logs what changed, why (the theorem + program finding), Rebecca's authority, and the credit/standing note.

6. **The output schema is sufficient for the JUDGE to score all three properties.** All metrics, per-seed arrays, scaling curves, degradation values, and kill condition verdicts are in the artifact.

7. **No new BLOCKING problems are introduced.** The 6 non-blocking observations (NB-1 through NB-6) are implementation details, edge cases, and new-bar acknowledgments that should be addressed but do not prevent the gate.

---

## Final Verdict

**ALL BLOCKING CLEARED. 6 NON-BLOCKING observations remain (do not prevent the gate).**

### Blocking issues: 0

No blocking issues remain. The three-property test is correctly implemented. The fair-naive is genuinely fair. The state-dependent battery is well-specified. All locked bars are carried forward verbatim. No bar laundering.

### Non-blocking observations: 6

| # | Observation | Severity | Recommendation |
|---|-------------|----------|----------------|
| **NB-1** | The 0.5 scaling-collapse threshold is a NEW kill-condition trigger, not acknowledged as a new bar in the scope fence (unlike the 0.05 floor). Inconsistent with §8's "no bar invention" claim. | Non-blocking | Acknowledge as new; either mark [PENDING REBECCA SIGN-OFF] or state it is an ARCHITECT-proposed operationalization of Rebecca's authorized criterion. Rebecca should explicitly confirm at the gate. |
| **NB-2** | The 0.05 degradation floor is a NEW bar, acknowledged as new and pre-registered per L19, but not marked [PENDING REBECCA SIGN-OFF]. | Non-blocking | Acceptable given the acknowledgment. Rebecca should explicitly confirm at the gate. |
| **NB-3** | The downstream consumer's content-similarity function and query items are underspecified ("e.g." cosine similarity; query item set not specified). A TASK BUILDER needs more guidance for reproducibility. | Non-blocking | Specify the exact similarity function, feature vector dimension/generation, and the set of query items. The degradation should be large for any reasonable implementation (frozen recency is drastically wrong), but the magnitude could vary. |
| **NB-4** | The downstream consumer tests only `coord_cycle_relative` (offset counter, C1.1), not `coord_landmark_relative` (designation tracking, C1.4). The novel mechanism's load-bearing property is not directly tested. | Non-blocking | Acceptable for a toy miniature (the full L15 at M5 tests all couplings). Note for M5: a more complete consumer would use both coordinates. |
| **NB-5** | The state-dependent battery doesn't explicitly address queries about deferred-designation landmarks at history size 100 (before designation). The fair-naive's cost is still O(n), but the expected behavior is unspecified. | Non-blocking | Clarify the expected behavior (return empty, skip query, etc.) for reproducibility. Does not affect the scaling property. |
| **NB-6** | The collapse criterion could be unstable if the fair-naive's fitted slope is near zero (timing noise at small scales). No minimum-slope guard or timing methodology specified. | Non-blocking | Specify timing methodology (warm-up, minimum repetitions) or a minimum fair_naive_slope guard below which the criterion is inconclusive. At the scales involved, the criterion should be robust, but the edge case should be acknowledged. |

### Recommendation

**The spec is ready for Rebecca's go/no-go gate.** The three-property test is correctly implemented. The fair-naive is genuinely the strongest honest timestamps-and-scan implementation. The state-dependent battery is well-specified. All locked bars are carried forward verbatim. The 6 non-blocking observations are implementation details and new-bar acknowledgments that Rebecca should note at the gate — particularly NB-1 (the 0.5 threshold should be acknowledged as a new bar) and NB-3 (the downstream consumer should be tightened for the BUILDER).

The center of gravity (fair-naive definition + state-dependent battery) holds: the fair-naive is not a strawman, the state-dependent queries are genuinely state-dependent, the collapse criterion is unambiguous, and the candidate's O(1)/O(log n) lookup is genuinely testable against the fair-naive's O(n) scan.

---

*Re-review (v3) ends. Hand to Rebecca for the E1 go/no-go gate (§9 step 3). The timebox clock starts at gate clearance (§10.2).*
