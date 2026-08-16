# M3 / E2 SPECIFICATION — CHANGELOG v4

**Serves: Rebecca's M3 Continuation/Scope Gate**
**Status: AMENDED DRAFT — requires CRITIC re-review; no build authorization**

**Maps:** `critic_m3_e2_spec_rereview_v3.md` findings F1–F7 (blocking) and NF1–NF6 (non-blocking), issued against `m3_e2_spec_amended_v3.md` (v3), to their exact resolution in `m3_e2_spec_amended_v4.md` (v4) — with real arithmetic verified by direct computation, not asserted — **and** carries forward the disposition of every prior B1–B10/NB1–NB5 (v0→v1), RB1–RB8/NB1–NB5 (v1→v2), and C1–C8/NB1–NB3 (v2→v3) finding, using the prior changelogs' own disposition tables as the bridge, so this single document is a complete four-generation audit trail.

**Per the tasking's explicit instruction, no item below is marked "resolved" without citing the exact v4 section(s) and the specific arithmetic/mechanism that constitutes the evidence.**

---

## Part A — F1–F7 (blocking findings against v3)

### F1 — L1's frozen and fair-naive controls are corners: the tie-break key is a perfect age proxy, so both arms fire INSTRUMENT FAILURE by construction

**Finding:** v3's §2.4 pre-registered the tie-break as ascending entry identifier (creation cycle). §2.8 defined the frozen arm as constant priority and the fair-naive arm as ranking by append order — which in this fixture is creation-cycle order, i.e., the identifier order itself. Under constant priority every candidate ties, so the entire ranking is produced by the tie-break; under append-order ranking the ranking is the identifier order. In both arms, rank is a deterministic monotone function of age, yielding R² = 0.926 — exceeding the 0.85 bar the arm exists to fail. Two adjacent defects: (a) the permuted arm's pass band was borrowed from the frozen null instead of its own permutation distribution; (b) the fair-naive arm's description ("unrelated to priority") was false on its face.

**Resolution in v4:**
- §2.4 replaces the tie-break with a **seeded random permutation of entry identifiers** (seed = 42, `numpy.random.RandomState(42).permutation(200)`), following the M1 B2 precedent. This permutation is genuinely label-independent — no dependence on age, rehearsal, or the ground-truth label.
- §2.8 replaces the fair-naive arm's ranking rule from "append order" to a **separate seeded random permutation** (seed = 43), genuinely unrelated to priority, age, rehearsal, or the ground-truth label.
- §2.9 re-derives the frozen and fair-naive empirical nulls: **frozen R² = 0.236** (constant priority, all tie, ranking by seeded random tie-break), **fair-naive R² = 0.320** (seeded random permutation ranking). Both fall well below the empirical-null 95th percentile (**0.749**, computed from 1,000 seeded reassignments of the tie-break permutation) — both arms are now valid negative controls instead of corners.
- §2.9 fixes the permuted arm's null (F1a): the pass band is now derived from the **permuted arm's own permutation distribution** (1,000 seeded permutations of the (age,rehearsal)→entry mapping), not borrowed from the frozen arm's tie-break-reassignment null. Permuted null: mean = 0.255, SD = 0.255, band = [−0.255, 0.764]. Observed permuted R² = 0.000, within band ✓.

**Evidence of closure:** §12.1a's 21-check verification table shows frozen R² = 0.236 ≤ 0.749 ✓, fair-naive R² = 0.320 ≤ 0.749 ✓, permuted R² = 0.000 within [−0.255, 0.764] ✓ — all computed by a verification script implementing the exact rules of §2.1–§2.6, §2.8–§2.9, reproducible by any reviewer from the stated constants and seeds.

**Status: RESOLVED — control redesign, full re-review required.**

### F2 — L1's within-bin assignment perfectly confounds rehearsal level with age, so the gating "rehearsal effect holding age fixed" test cannot fail

**Finding:** v3's §2.2 assigned rehearsal level `⌊i/8⌋` to the i-th measured cycle in ascending cycle order within each bin — level-0 entries always the 8 oldest, level-4 always the 8 youngest — perfectly rank-correlating rehearsal level with creation cycle (and hence age) within every bin. A factor-inert candidate (β=0) would still pass the rehearsal-isolation test because age ordering is the rehearsal-level ordering under this assignment.

**Resolution in v4:**
- §2.2 changes the within-bin assignment from `⌊i/8⌋` to **`i mod 5`** (interleaved), the critic's own suggested fix. Under this assignment, each rehearsal level's 8 entries span the full 195-cycle range of the bin (e.g., level 0 occupies cycles `lo_b + 0, lo_b + 25, ..., lo_b + 175`; level 4 occupies `lo_b + 20, lo_b + 45, ..., lo_b + 195`), so the within-bin Spearman correlation between rehearsal level and age is **−0.1225** — weak, not the perfect +1.0 under v3's `⌊i/8⌋`.
- §2.6 and §12.1a verify the consequence: the oracle candidate (true β = 0.5) shows within-bin ρ ≥ 0.6 for all 5 bins (0.91–0.95), while a factor-inert candidate (β = 0, age-only priority) shows ρ < 0.6 for all 5 bins (0.20, 0.24, 0.20, 0.18, 0.13) — the test now correctly distinguishes presence from absence of the rehearsal effect.

**Evidence of closure:** §12.1a's verification table shows all three F2 checks pass: within-bin Spearman = −0.1225 (was +1.0), oracle ρ ≥ 0.6 for all bins, inert ρ < 0.6 for all bins.

**Status: RESOLVED — fixture redesign, full re-review required.**

### F3 — §2.11's PASS branch gates on "§2.9's exact bounds" for the recency-only and rehearsal-only ablations, but §2.9 defines no bound, artifact, or failure consequence for either arm

**Finding:** v3's §2.8 listed recency-only and rehearsal-only ablations as arms, but §2.9's table had no rows for either — no expected statistic, no artifact schema, no instrument-failure consequence. The PASS branch therefore referenced bounds that did not exist.

**Resolution in v4:**
- §2.9 adds two new rows:
  - **Recency-only** (`priority(e) = exp(−λ·age(e))` only): isolation criterion is R² ≥ 0.85 AND β_age < 0 (age bar met with rehearsal removed) AND all 5 within-bin ρ < 0.6 (rehearsal effect absent). Verified: R² = 0.926, β_age = −0.00229, all ρ < 0.6 (0.20, 0.24, 0.20, 0.18, 0.13). INSTRUMENT FAILURE if R² < 0.85, β_age ≥ 0, or any ρ ≥ 0.6.
  - **Rehearsal-only** (`priority(e) = 1 + β·log(1+rehearsal(e))` only): isolation criterion is β_age ≥ 0 (age direction not negative → age bar not met) AND all 5 within-bin ρ ≥ 0.6 (rehearsal bar met). Verified: β_age = 0.0005 (≥ 0), all ρ ≥ 0.6 (0.97–0.98). INSTRUMENT FAILURE if β_age < 0 or any ρ < 0.6. (Note: R² may be high — observed 0.996 — due to low between-bin variance when accessibility depends only on rehearsal, but R² is not the criterion for this arm; the direction of β_age is.)
- §2.10 adds both arms to the L18 battery checklist with exact pass conditions.
- §2.11 updates the PASS branch to reference the new §2.9 bounds explicitly ("recency-only: R² ≥ 0.85, β_age < 0, all 5 ρ < 0.6; rehearsal-only: β_age ≥ 0, all 5 ρ ≥ 0.6") and the INSTRUMENT FAILURE branch to include both arms' failure conditions.

**Evidence of closure:** §12.1a's verification table shows all 6 F3 checks pass (3 per arm). §12.5's arm-coverage matrix shows both arms present for L1.

**Status: RESOLVED — score definition, full re-review required.**

### F4 — The score-defining L1 accessibility quantity is not fully defined, and the satisfiability of the R² bar on rank-derived data is asserted, not derived

**Finding:** v3's §2.4 had every measured entry appear "across multiple sets" without pre-registering the set count or appearance count, and §2.6 fit `log(accessibility(e))` as a single per-entry quantity without defining how one value per entry is obtained from multiple per-set ranks. The oracle's claim that it "must pass by definition" (R² ≥ 0.85) was nowhere derived or computed.

**Resolution in v4:**
- §2.4 pre-registers the exact quantities:
  - **Number of candidate sets: exactly 100 per scoring seed.**
  - **Per-entry appearance count: exactly 5 per entry** (balanced design: for each bin, a pool of 200 entry indices — each of 40 entries repeated 5 times — is shuffled with structural seed 777 and paired; every entry appears in exactly 5 sets; the same schedule is used for all scoring runs).
  - **Per-entry aggregation rule:** `log_accessibility(e) = mean_{s ∈ sets(e)} log(11 − rank_s(e))` — the mean of log-transformed per-set accessibilities, pre-registered as the single binding rule; the oracle satisfiability is verified under this exact rule.
- §2.4 and §12.1a verify by direct computation: the oracle achieves **R² = 0.985** (≥ 0.85) with **β_age = −0.00150** (< 0) under these exact rules — the M0-adopted bar is met, and the curvature risk F1 identified (successive bin-mean drops of 0.24, 0.31, 0.46, 0.90 in the deterministic case) is not present under the oracle's two-factor ranking.

**Evidence of closure:** §12.1a's verification table shows all 4 F4 checks pass: 100 sets, 5 appearances/entry (min=max=5), oracle R² = 0.985 ≥ 0.85, oracle β_age = −0.00150 < 0.

**Status: RESOLVED — score definition, full re-review required.**

### F5 — L5's frozen arm's chain-fixture expectation does not follow from its own definition; no freeze point or append timeline is pre-registered

**Finding:** v3's §4.7 defined the frozen arm as "both axes fixed at fact-creation time; `supersedes` pointers never updated on later supersession appends." But in §4.5's graph, each `supersedes` pointer is a backward pointer written once at the superseding fact's own append and never requires later update — so the frozen arm's walks would be correct (accuracy 1.00), contradicting §4.8's claim of 0.00. No freeze point, no definition of post-freeze queries, and no append timeline were pre-registered.

**Resolution in v4:**
- §4.5 introduces a **head pointer** — a separate index entry designating each chain's current-belief node, updated on supersession (a genuine mutation, not a backward-pointer write-once). This is what makes the freeze meaningful.
- §4.5 pre-registers the **chain-append timeline**:
  - Pre-freeze phase (cycles 0–99): nodes (c,0)–(c,4), 100 facts. Head updated to (c,4).
  - Freeze point: after cycle 99. Head pointers frozen at (c,4).
  - Post-freeze phase (cycles 100–199): nodes (c,5)–(c,9), 100 facts. Head NOT updated.
- §4.5 defines the **post-freeze query subset**: all 40 queries reference terminal (c,9), a post-freeze node → all 40 are post-freeze.
- §4.5 and §4.8 derive the **outcome**: frozen head at (c,4) → walks start from wrong node → walk result ≠ expected → **walk accuracy = 0.00 for all 40 post-freeze queries, by construction.**
- §4.7 redefines the frozen arm's "what is perturbed" to the head pointer freeze.
- §4.8 updates the frozen arm row with the new expected statistic, artifact fields, and consequence.
- §4.9 adds the frozen arm's instrument-failure condition.

**Evidence of closure:** §12.4 verifies: pre-freeze 100 facts at cycles 0–99 ✓, post-freeze 100 facts at cycles 100–199 ✓, total 200 ✓, frozen head at (c,4) ✓, all 40 queries post-freeze ✓, walk accuracy = 0.00 ✓.

**Status: RESOLVED — control redesign, full re-review required.**

### F6 — L5's shuffled-chain null derivation contradicts the pre-registered graph and its own probability model

**Finding:** v3's §4.8 derived the shuffled bound from "190 non-root edges" with "probability 1/189" — both wrong: §4.5 and §12.4 pre-register 20×9 = 180 edges, and under a derangement the probability of any edge landing on its true target is 0 by definition (no fixed points). The passage was also internally ambiguous about whether the bound was fixed 0.05 or per-seed "computed."

**Resolution in v4:**
- §4.8 corrects the edge count to **180** (20×9 = 180, not 190).
- §4.8 states the derangement expectation as **exactly 0** (by definition: a derangement has no fixed points; each edge's true target is distinct, so inheriting another edge's target can never reproduce one's own).
- §4.8 fixes the bound to a **single criterion**: chain-walk accuracy ≤ 0.05 (deterministic bound — the expected value is 0.00, which is ≤ 0.05; no per-seed computation needed).
- §12.4 verifies: 180 edges ✓, derangement expectation = 0 ✓, expected walk accuracy = 0.00 ✓, bound 0.00 ≤ 0.05 ✓.

**Evidence of closure:** §12.4's F6 shuffled-edge check confirms all corrections. The bound is conservative and salvageable, as the critic noted.

**Status: RESOLVED — mechanical fix, verified without separate review cycle.**

### F7 — L6's closed-world enumeration contradicts its own count: 4 callables enumerated, "5" claimed

**Finding:** v3's §5.3 enumerated exactly four public callables (query_episodic, query_episodic_batch, to_json, from_json) but claimed "five named public callables" and "5 rows." §5.4 attack #6 said "the 4 named," while §5.6 required "all 5 reachability-audit rows." 2+0+2 = 4.

**Resolution in v4:**
- §5.3 corrects "five named public callables total" → **"four named public callables total"** and "5 rows total" → **"4 rows total."**
- §5.6 corrects "all 5 reachability-audit rows" → **"all 4 reachability-audit rows."**
- §5.4's attack #6 already said "the 4 named in §5.3" — correct, no change needed.
- §12.5 verifies: 2+0+2 = 4 callables, 4 audit rows ✓.

**Evidence of closure:** §12.5's arm-coverage matrix confirms "4 rows" (F7 fix).

**Status: RESOLVED — mechanical fix, verified without separate review cycle.**

---

## Part B — NF1–NF6 (non-blocking findings against v3)

### NF1 — L3 frozen-floor scope discrepancy (§3.7 vs §3.9)

**Finding:** §3.7 required frozen `reduction_h ≤ 0%` at h=5 only; §3.9 extended it to every horizon. Both route to INSTRUMENT FAILURE (conservative direction), but the two texts defined different tripwires.

**Resolution in v4:** §3.7 harmonized to **every horizon 1..5** (the stricter of the two scopes), matching §3.9's existing text. No candidate-pass laxity is introduced; the change only makes the tripwire consistent across both sections.

**Status: RESOLVED — harmonized to one scope.**

### NF2 — Seed ledger's completeness claim overstates its coverage

**Finding:** §8.1 claimed to be "a complete historical record" but omitted M1's scoring exposure of seeds 42–44 and M1's empirical-null replicate ranges (seeds 100–129, overlapping the M3 development pool). No rule is violated, but the claim was inaccurate.

**Resolution in v4:** §8.1 narrows the completeness claim to **"a complete record of E1 and M3 seed-use events"** and explicitly notes M1's non-M3 seed usage (seeds 100–129 for empirical-null replicates, 42–44 for scoring) as outside this ledger's scope, with the rationale that development-pool seeds carry no unseen requirement and hold-outs {201, 202, 203} have no recorded exposure anywhere.

**Status: RESOLVED — claim narrowed to accurate scope.**

### NF3 — STATE.md is stale relative to the governing state the spec cites

**Finding:** STATE.md still shows M2 active and HEAD `dceb2584…`, not the M2 GREEN/SEALED/ACCEPTED status or main commit `1626bb09…` the v3 header cites. This is an INTEGRATOR's state-hygiene gap, not ARCHITECT's.

**Resolution in v4:** §11 adds a non-claim noting STATE.md's staleness as INTEGRATOR's responsibility and stating that STATE.md must be brought current before Rebecca rules at this gate. The spec does not itself attest STATE.md as current.

**Status: ADDRESSED — noted as INTEGRATOR's responsibility; flagged for pre-gate resolution.**

### NF4 — Timing methodology should inherit E1's clock-resolution construction-bug fix

**Finding:** §2.5 and §4.4 mandated `time.perf_counter_ns()` with median ≥100 reps but omitted the batch-fallback for sub-clock-resolution operations that E1-RUN-1's crash forced.

**Resolution in v4:** §2.5 and §4.4 both add **batch-fallback language**: if the median per-operation elapsed time is below the timer's documented resolution, the timing loop batches B consecutive operations (starting at B=100, doubling until the batch median exceeds 10× the timer resolution) and reports `median_batch_time / B` as the per-operation estimate, with B logged — inheriting E1-RUN-1's construction-bug fix (Entry 34/commit `dceb2584`).

**Status: RESOLVED — batch-fallback language added to both timing sections.**

### NF5 — Fair-naive artifact field scope imprecise

**Finding:** §4.3 derived the 75.0% for the 200 world-validity queries, but §4.8's `combo_accuracy: 0.75` and §4.9's trigger didn't state the world-validity-only scope. The single-axis arm answers self-acquisition queries from `acquired_at` and would score ~1.00 there.

**Resolution in v4:** §4.8 renames the artifact field to `combo_accuracy_world_validity: 0.75` and §4.9's instrument-failure trigger is scoped to "world-validity queries" explicitly. The exact-match check now uses the correct denominator.

**Status: RESOLVED — scope stated explicitly.**

### NF6 — Full-scan arm's delta presumes a separate chain-fixture log

**Finding:** §4.8 expected `access_count` delta = 200 for the full-scan walker, which is only correct if the 200-fact chain fixture occupies its own log (else a full scan reads 400).

**Resolution in v4:** §4.5 states explicitly that **the chain fixture occupies its own separate append log, distinct from the combination-fixture log.** §4.8's full-scan row adds `log: "chain_fixture_separate"` to the artifact and notes that the delta = 200 is the chain-fixture log size (not 400).

**Status: RESOLVED — separation stated explicitly.**

---

## Part C — Carried-forward disposition of B1–B10/NB1–NB5 (v0→v1), RB1–RB8/NB1–NB5 (v1→v2), and C1–C8/NB1–NB3 (v2→v3)

The v3 changelog's own disposition table (`m3_e2_spec_changelog_v3.md`, Part C) is the authoritative bridge for generations 0–2; v4's changes do not reopen any item that table marked "Resolved," and the items it marked "Partly resolved" are exactly the C1–C8 items resolved in v3. The v3 critic re-review confirmed C1, C3, C4, C7, and NB1–NB3 as resolved, with C2, C5, C6, and C8 partly resolved (now fully resolved in v4 via the F-fixes). For completeness, the full four-generation lineage:

| Original finding | v1 disposition | v2 disposition | v3 disposition | v4 disposition |
|---|---|---|---|---|
| B1 / RB4 — adopted bars, L5 growth numbers | Resolved (v1) | Partly resolved (→ C2) | C2 resolved (v3) | **C2 fully resolved** (F1/F4 fixes complete the rank-accessibility derivation) |
| B2 — complete scoreable contract | Not resolved (→ RB1–RB8) | Not resolved (→ C1–C8) | C1–C8 resolved (v3) | **F1–F7 resolved** (v4); contract now scoreable in every named respect |
| B3 / RB1–RB2 — L1 and W1 | Resolved (v1) → RB1–RB2 | Not resolved (→ C1, C2) | C1, C2 resolved (v3) | **C1 retained resolved** (timeline unchanged); **C2 fully resolved** (F1/F2/F4) |
| B4 / RB3 — L3 | Resolved (v1) → RB3 | Partly resolved (→ C3) | C3 resolved (v3) | **C3 retained resolved**; NF1 harmonized |
| B5 — fair controls / downstream tests | Resolved (v1) | Not resolved (→ C7) | C7 resolved by deletion (v3) | **C7 retained resolved** (deletion unchanged) |
| B6 / RB4 — L5 | Resolved (v1) → RB4 | Not resolved (→ C4, C5) | C4, C5 resolved (v3) | **C4 retained resolved**; **C5 fully resolved** (F5/F6 fix the chain-arm defects C5's resolution introduced) |
| B7 / RB5 — L6 | Resolved (v1) → RB5 | Partly resolved (→ C6) | C6 resolved (v3) | **C6 fully resolved** (F7 fixes the count contradiction C6's resolution introduced) |
| B8 / RB7 — §2 and execution | Resolved (v1) → RB7 | Partly resolved (→ NB1) | NB1 resolved (v3) | **NB1 retained resolved**; NF2 narrows claim |
| B9 — L9 and integration fence | Resolved (v1) | Resolved | Retained resolved (v3) | **Retained resolved** (§9, re-verified against every v4 mechanism) |
| B10 / RB8 — timebox | Resolved (v1) → RB8 | Resolved | Retained resolved (v3) | **Retained resolved** (§10, unchanged per NB3) |
| NB1–NB5 (v0→v1) | Mostly resolved (v1) | Mostly resolved | Resolved (v3) | **Retained resolved** |

---

## Part D — What survived review unchanged from v3

Per the CRITIC's v3 re-review (Part 4, "What should NOT change on resubmission"), the following were verified by adversarial re-derivation and are correct as written in v3 — they are preserved unchanged in v4 except where a named F/NF finding required a specific correction:

- §2.1's unique-cycle timeline arithmetic (as a timeline; F2 changes only the level assignment rule within §2.2)
- §3.1–§3.7 in full (NF1 harmonizes §3.7's scope to match §3.9; no mechanism change)
- §4.1–§4.3 (replicate-relative offsets, 75% derivation — unchanged; NF5 scopes the artifact field only)
- §4.5's graph/bypass registration (graph structure unchanged; F5 adds the head-pointer mechanism and append timeline, F6 corrects the edge count only)
- §5.1–§5.2 and §5.4–§5.5's arm transforms (unchanged; F7 corrects the count in §5.3 and §5.6 only)
- §6 (cross-law summary — unchanged)
- §8's pools and protections (unchanged; NF2 narrows a claim only)
- §9, §10, §11 (unchanged; NF3 adds a note, NF4 adds timing language)
- §12's checks 12.1–12.4 and 12.6–12.9 (12.5 updated for F3/F7; 12.1a, 12.4, and 12.10 added/updated for F1–F7/NF1–NF6)

---

## Summary of v4 section changes relative to v3

| v3 section | v4 section | Change |
|---|---|---|
| §0 | §0 | Rebuilt: describes F1–F7/NF1–NF6 resolutions |
| Header | Header | Updated: v4, fourth resubmission, references v3 critic re-review |
| §2.2 | §2.2 | F2: within-bin assignment changed from `⌊i/8⌋` to `i mod 5` |
| §2.4 | §2.4 | F1: tie-break changed to seeded random permutation (seed=42); F4: pre-registers 100 sets, 5 appearances/entry, mean-of-log aggregation rule, oracle R²=0.985 |
| §2.5 | §2.5 | NF4: batch-fallback timing language added |
| §2.6 | §2.6 | F2: conditional test expectations recomputed and verified |
| §2.8 | §2.8 | F1: fair-naive arm changed from append order to seeded random permutation (seed=43) |
| §2.9 | §2.9 | F1: frozen/fair-naive nulls re-derived (R²=0.236/0.320, null 95th=0.749); F1a: permuted null from own distribution; F3: recency-only and rehearsal-only rows added |
| §2.10 | §2.10 | F3: recency-only and rehearsal-only added to checklist |
| §2.11 | §2.11 | F3: PASS and INSTRUMENT FAILURE updated for ablation arm bounds |
| §3.7 | §3.7 | NF1: frozen-floor scope harmonized to every horizon |
| §4.4 | §4.4 | NF4: batch-fallback timing language added |
| §4.5 | §4.5 | F5: head pointer, append timeline, freeze point, post-freeze subset added; NF6: chain-fixture log separation stated; F6: edge count corrected to 180 |
| §4.7 | §4.7 | F5: frozen arm redefined with head-pointer freeze |
| §4.8 | §4.8 | F5: frozen arm row updated; F6: shuffled arm edge count/derangement/bound corrected; NF5: fair-naive scope stated; NF6: full-scan log separation stated |
| §4.9 | §4.9 | F5: frozen arm instrument-failure added; NF5: fair-naive scope stated |
| §5.3 | §5.3 | F7: "five" → "four," "5 rows" → "4 rows" |
| §5.6 | §5.6 | F7: "all 5" → "all 4" |
| §8.1 | §8.1 | NF2: completeness claim narrowed |
| §11 | §11 | NF3: STATE.md staleness noted |
| §12.1 | §12.1 | Unchanged (timeline arithmetic) |
| — (new) | §12.1a | F1/F2/F3/F4: 21-check verification table |
| §12.4 | §12.4 | F5: head-pointer/append-timeline check; F6: shuffled-edge check |
| §12.5 | §12.5 | F3: ablation arms in coverage matrix; F7: callable count = 4 |
| — (new) | §12.10 | Closure audit mapping F1–F7 and NF1–NF6 |
| Sources | Sources | Updated: v3 critic re-review and v3 spec added |

---

## Sources

- `critic_m3_e2_spec_rereview_v3.md` — fourth blocking review (F1–F7, NF1–NF6), resolved above
- `critic_m3_e2_spec_rereview_v2.md` — third blocking review (C1–C8, NB1–NB3), carried forward via Part C
- `critic_m3_e2_spec_rereview.md` — second blocking review (RB1–RB8, NB1–NB5), carried forward via Part C
- `critic_m3_scope_review.md` — first blocking review (B1–B10, NB1–NB5), carried forward via Part C
- `m3_e2_spec_amended_v3.md` — v3, superseded by `m3_e2_spec_amended_v4.md`
- `m3_e2_spec_amended_v2.md` — v2, superseded
- `m3_e2_spec_amended.md` — v1, superseded
- `m3_e2_spec_changelog_v3.md`, `m3_e2_spec_changelog_v2.md`, `m3_e2_spec_changelog.md` — prior changelogs
- `M0_DECISION_SHEET.md`, `REBECCA_RESPONSE_M0.md`, `ARCHITECTURAL_CONSTITUTION.md` — governing adopted material, unchanged by this round
