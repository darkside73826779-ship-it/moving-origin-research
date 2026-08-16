# CRITIC Review — Option E Amendment (E1 §3 Arm 1 + §6.iii + dependent §7/§9)

**Verifier:** CRITIC · **Date:** 2026-08-15 · **Subject:** ARCHITECT's Option E targeted amendment to the E1 spec (v3+Option E), per Rebecca's binding Property (iii) ruling (Option D REJECTED; Option E ordered).

**Scope:** §3 Arm 1 (frozen-origin arm), §6.iii (property (iii) consumer + recency-discriminative battery), and dependent text in §7 (output schema) and §9 (CRITIC verification checklist). Properties (i) and (ii) are OUT OF SCOPE (unchanged by this amendment).

---

## VERDICT: BLOCKING ISSUES REMAIN

The Option E frozen-arm specification is faithful to Rebecca's binding ruling (all entries retained, coordinates computed once at birth, consumer identical across arms). Rebecca's verbatim lesson is logged. The output schema and §9 checklist capture the new battery. **However, Verification (a) FAILS**: the spec's central mathematical claim — that content-only ranking succeeds on content-unique queries, bounding degradation by the recency-discriminative fraction (≤ 0.4) — is **false**. Direct simulation of the spec's exact formulas shows actual mean degradation ≈ **0.89** (not 0.12–0.20), driven by the frozen arm failing on **content-unique queries** (CU degradation ≈ 0.94, not ~0). The root cause is that τ=50 creates a recency weight spanning **nine orders of magnitude** (exp(−999/50) ≈ 2×10⁻⁹ to 1.0), which overwhelms the content signal (dot product of 32-d unit-variance vectors, dynamic range ~1 order of magnitude). The degradation is close to the 1.0 ceiling corner that Rebecca explicitly warned against.

---

## Rebecca's Two Required Verifications (BLOCKING)

### Verification (a): degradation < 1.0 is reachable — **FAILS**

**The spec's claim (§6.iii lines 587–590):**
> "On the 30 content-unique queries (60%), content similarity alone determines the ranking — one entry clearly has the highest dot product. The frozen arm (content-only ranking) matches the oracle (recency-weighted ranking) because the recency weight does not overturn a strong, unambiguous content signal."
> "The maximum possible degradation is bounded by the recency-discriminative fraction: `degradation ≤ fraction_recency_discriminative × 1.0 = 0.4 < 1.0` (since `quality_frozen ≥ 0` on all queries and `quality_frozen ≈ 1.0` on content-unique queries)."

**Direct simulation (seeds 42/43/44, exact spec formulas):**

| Metric | Spec claims | Actual (simulated) |
|---|---|---|
| Mean degradation (all 50 queries) | 0.12–0.20 | **0.887** |
| Mean degradation (20 RD queries) | 0.3–0.5 per query → 0.12–0.20 aggregate | **0.827** |
| Mean degradation (30 CU queries) | ≈ 0 | **0.927** |
| Mean quality_frozen (CU queries) | ≈ 1.0 | **0.07** |
| Bound on degradation | ≤ 0.4 | **~0.89** |

Per-seed: degradation = 0.888 / 0.894 / 0.878 (all > 0, all well above 0.05 floor). The test would technically PASS. But it passes for the **wrong reason** and with a magnitude wildly different from the spec's stated expectation.

**Root cause:** The consumer's relevance function is `relevance(e, q) = exp(−coord_cycle_relative(e) / τ) · dot(v(e), q)` with τ=50 and now=999. The recency weight `exp(−(999 − e.cycle) / 50)` ranges from `exp(−999/50) ≈ 2.1×10⁻⁹` (cycle 0) to `exp(0) = 1.0` (cycle 999) — a factor of ~5×10⁸. The content signal `dot(v(e), q)` for random 32-d unit-variance vectors has std ≈ √32 ≈ 5.66, with the top-1 over 1000 entries ≈ 17 and top-2 ≈ 16 (ratio ~1.06). The recency weight ratio (~10⁸) exceeds the content ratio (~1.06) by **seven orders of magnitude**. The oracle's ranking is therefore **recency-dominated on ALL queries, not just recency-discriminative ones**. The frozen arm (recency weight = 1.0 for all, ranking purely by content) picks high-dot-product entries of any age, while the oracle's top-k is drawn almost exclusively from recent cycles (observed: oracle top-k cycles ≈ 930–999; frozen top-k cycles scattered across 0–999). Overlap is near zero → CU degradation ≈ 0.94.

**The spec's logic is incorrect.** "Content similarity alone determines the ranking" on content-unique queries is false — the recency weight dominates the content signal on every query. The claim that "the recency weight does not overturn a strong, unambiguous content signal" is false — there is no content signal strong enough to withstand a 10⁸× recency gradient with 32-d random Gaussian features. The bound "degradation ≤ 0.4" does not hold; actual degradation ≈ 0.89.

**Could the frozen arm fail on content-unique queries?** YES — it does, on 26 of 30 CU queries (degradation = 1.0, zero overlap). This is exactly the condition the task says indicates "the battery is broken."

**Is the maximum possible degradation bounded by the recency-discriminative fraction (0.4 < 1.0)?** NO — actual degradation is ~0.89, far exceeding 0.4. The bound only holds if `quality_frozen ≈ 1.0` on CU queries, which is false.

**A τ sweep confirms the problem is structural, not a tuning accident:**

| τ | RD degradation | CU degradation | All degradation |
|---|---|---|---|
| 50 (spec) | 0.827 | 0.927 | 0.887 |
| 100 | 0.790 | 0.882 | 0.845 |
| 200 | 0.755 | 0.830 | 0.800 |
| 500 | 0.652 | 0.699 | 0.680 |
| 1000 | 0.450 | 0.542 | 0.505 |

Even at τ=1000 (where the recency weight spans only ~0.5 orders of magnitude), CU degradation is still 0.54 — the content signal of random 32-d Gaussian vectors is never strong enough to let the frozen arm match the oracle on content-unique queries. The spec's intended separation (CU → content dominates; RD → recency breaks ties) is **not achievable** with the current relevance function and feature/query distribution at any reasonable τ.

### Verification (b): the 0.05 floor is meaningfully clearable — **Technically passes, but for the wrong reason**

- **Does the candidate/oracle's re-resolved coordinate genuinely break the tie on RD queries?** YES — the recency weight favors the recent pair member by a factor of ~10⁷–10⁸. The oracle consistently ranks the recent member (oracle picks `e_new_p` on all 20 RD queries). ✓
- **Does the frozen arm's stale coordinate (0 for all) fail to break the tie?** YES — recency weight = 1.0 for all, so it ranks by content alone (near-tied). ✓
- **Is the expected aggregate degradation (≈ 0.12–0.20) genuinely above 0.05?** The actual degradation (0.887) IS above 0.05, but the spec's claimed 0.12–0.20 is wrong by ~5–7×. The floor is cleared not because RD queries contribute 0.12–0.20, but because **CU queries contribute 0.56** (0.60 × 0.927) — the frozen arm fails on CU queries too.
- **Is there a plausible scenario where degradation falls below 0.05?** No — degradation is ~0.89, well above 0.05. But this robustness comes from the frozen arm failing everywhere, not from the intended RD mechanism. The floor is trivially clearable, which is the opposite problem from the floor corner.

The floor IS clearable, but not for the reason the spec describes. The spec's quantitative predictions (RD per-query 0.3–0.5; CU per-query ~0; aggregate 0.12–0.20) are all wrong. The RD per-query degradation is actually 0.70–0.90 (not 0.3–0.5), and CU per-query degradation is 0.80–1.00 (not ~0).

---

## Additional Checks

### 1. Option E compliance — PASS

The frozen-arm specification (§3 Arm 1, §6.iii) matches Rebecca's binding Option E exactly:
- **ALL entries and ALL content retained?** YES — "retains ALL entries and ALL content, identical to the candidate's autobiography (all 1000 entries, same payloads, same feature vectors)." ✓
- **Coordinates computed ONCE at append, never re-resolved?** YES — "coord_cycle_relative = 0 at birth (now_at_birth − e.cycle = e.cycle − e.cycle = 0)... NEVER re-resolved thereafter." ✓
- **Consumer identical across arms?** YES — "The consumer is identical across arms — the ONLY difference between candidate and frozen is whether coordinates moved after birth." ✓
- **Only difference is whether coordinates moved after birth?** YES. ✓

The prior internal contradiction (Arm 1 said "excludes entries 100–999" [Option D]; §6.iii said "frozen coord = 99 − e.cycle for all") is resolved. Both sections now consistently describe Option E.

### 2. No corners — CONCERNING

- **Not 0 by construction?** YES — the frozen arm differs from the candidate (recency weight collapsed), so degradation > 0. ✓
- **Not 1 by construction?** Technically yes — degradation = 0.887, not 1.0, and it varies by seed (0.878–0.894). It is not a constant by construction. ✓ (in the strict sense)
- **BUT:** the degradation is close to 1.0 (0.89), and the reason it's not 1.0 is incidental (occasional overlap between the frozen arm's content-based top-k and the oracle's recency-based top-k), not by design. Rebecca's lesson warns that "corners measure nothing." While 0.89 is not exactly a corner, it is uncomfortably close to the ceiling, and the spec's claimed bound (≤ 0.4) gives a false sense of margin. The spec explicitly states the expected result is "in the open interval (0, 1)" — 0.89 is technically in that interval, but the spec's reasoning for WHY it's below 1.0 is wrong.

### 3. Near-duplicate generation — PASS (well-specified)

- **How are pairs selected?** 20 pairs: old member at cycle `p` (cycles 0–19), new member at cycle `900+p` (cycles 900–919). Deterministic. ✓
- **How are near-identical features generated?** `v_base_p = rng_pair_p.standard_normal(32)`; `v(e_old_p) = v_base_p`; `v(e_new_p) = v_base_p + σ_nd · rng_pair_p.standard_normal(32)` with `σ_nd = 0.05`. ✓
- **Is it deterministic per seed?** YES — all RNGs seeded with `seed * 10_000_000 + p` (pair base), `seed * 10_000_000 + 500 + j` (RD query). ✓
- **How are queries generated?** RD query `j`: `q_j = v_base_p + σ_q · rng_qd_j.standard_normal(32)` with `σ_q = 0.05`. CU query `j`: `q_j = rng_q.standard_normal(32)`. ✓

The generation is fully specified and deterministic. No ambiguity for the TASK BUILDER.

### 4. Recency-discriminative fraction (40%) — Moot

The spec chooses 40% (20 of 50). The spec's reasoning is that this gives aggregate degradation 0.12–0.20 (0.40 × 0.3–0.5). But since CU queries also degrade (CU degradation ≈ 0.94), the fraction is **irrelevant** to the aggregate — the CU queries dominate. Whether the fraction is 10%, 40%, or 80%, the aggregate degradation would be ≈ 0.89 because the CU queries contribute ~0.56 regardless. The fraction's only effect is on the marginal RD contribution. The fraction is not "too high" or "too low" — it's **moot** because the spec's intended CU/RD separation doesn't hold.

### 5. No bar laundering — PASS

- **Locked bars unchanged?** YES — latency ≤ 2.0, N=10, chain_integrity = 1.0, 3-seed policy all carried forward. ✓
- **0.05 floor unchanged?** YES — `downstream_degradation_floor: 0.05` in §7.3.1, unchanged from Rebecca's sign-off. ✓
- **τ=50 unchanged?** YES — pinned per Q3-1, not modified by this amendment. ✓

### 6. Lesson logged — PASS

Rebecca's verbatim lesson is present in §6.iii (line 594):
> *"An ablation whose result is a constant by construction measures nothing. A valid ablation removes exactly the organization under test and preserves everything else, and its expected result must be a task-dependent quantity in the open interval — never a corner."*

The lesson is contextualized with the two prior degenerate ablations (Option D → 1.0 ceiling; prior §6.iii → 0.0 floor) and Option E's intended position in (0, 1). ✓

### 7. Consistency (§7 output schema + §9 checklist) — PASS

- **§7.3.1 config** includes `n_recency_discriminative_queries`, `recency_discriminative_fraction`, `n_near_duplicate_pairs`, `near_duplicate_sigma`, `recency_discriminative_query_sigma`. ✓
- **§7.3.1 property_iii** `consumer_spec` string updated to describe Option E + recency-discriminative battery. ✓
- **§7.3.1 notes** (line 832) updated for Option E with the two CRITIC verifications stated. ✓
- **§9 step 2** (line 1023) includes both verifications: "is degradation < 1.0 reachable (content-only ranking succeeds on content-unique queries)? does the recency-discriminative fraction make the 0.05 floor meaningfully clearable by a working mechanism?" ✓

The schema and checklist correctly reference the new battery. ✓

---

## BLOCKING ISSUES

### BLOCKING ISSUE 1: Verification (a) fails — the frozen arm does NOT succeed on content-unique queries

**The spec's central mathematical claim is false.** The spec states (§6.iii lines 588–589):

> "On the 30 content-unique queries (60%), content similarity alone determines the ranking — one entry clearly has the highest dot product. The frozen arm (content-only ranking) matches the oracle (recency-weighted ranking) because the recency weight does not overturn a strong, unambiguous content signal."
> "The maximum possible degradation is bounded by the recency-discriminative fraction: `degradation ≤ 0.4 < 1.0`."

**Direct simulation of the spec's exact formulas** (3 seeds, 50 queries each) shows:
- CU degradation = **0.927** (spec claims ≈ 0). On 26 of 30 CU queries, the frozen arm has **zero overlap** with the oracle's top-k (degradation = 1.0).
- Mean degradation = **0.887** (spec claims 0.12–0.20; spec claims bound ≤ 0.4).
- The oracle's top-k is drawn from cycles ~930–999 (recency-dominated); the frozen arm's top-k is scattered across cycles 0–999 (content-dominated). They rarely overlap.

**Root cause:** τ=50 with now=999 and cycles 0–999 creates a recency weight `exp(−(999−e.cycle)/50)` spanning ~9 orders of magnitude (2×10⁻⁹ to 1.0). The content signal (dot product of 32-d random Gaussian vectors, std ≈ 5.66) has a dynamic range of ~1 order of magnitude. The recency weight overwhelms the content signal on **every** query, not just recency-discriminative ones. The spec's intended separation — CU queries where content dominates, RD queries where recency breaks ties — **does not hold**.

**Why this is blocking:**
1. Rebecca's companion requirement (ruling §Q1) explicitly states: "content-only ranking must still succeed on content-unique queries" and "the CRITIC verifies that (a) degradation < 1.0 is reachable (content-only ranking must still succeed on content-unique queries)." The CRITIC's verification finds that content-only ranking does NOT succeed on content-unique queries. This is the exact failure condition Rebecca named.
2. The spec's quantitative predictions (0.12–0.20 aggregate; ≤ 0.4 bound; CU ≈ 0; RD 0.3–0.5 per query) are wrong by 5–7×. The JUDGE and CRITIC are told to expect ~0.12–0.20 but will observe ~0.89 — a major discrepancy that undermines the test's interpretability.
3. The actual degradation (0.89) is close to the 1.0 ceiling corner. While not exactly 1.0 by construction, the margin (0.89 vs 1.0) is thin and incidental, not by design. Rebecca's lesson warns that corners measure nothing; 0.89 is uncomfortably close to "nothing."
4. The τ sweep (τ=50 to 1000) shows the problem is **structural** — no value of τ makes CU degradation ≈ 0 with 32-d random Gaussian features. The content signal is never strong enough to overcome any recency gradient.

**Recommended fix (for the ARCHITECT to propose, Rebecca to approve):**

The core requirement is: on content-unique queries, the content signal must be strong enough that the frozen arm (content-only) matches the oracle (recency-weighted). This requires the content signal's dynamic range to exceed the recency weight's dynamic range among the top candidates. Options:

(a) **Make content-unique queries strongly peaked** — e.g., each CU query is a (near-)copy of one specific entry's feature vector plus small noise, so one entry clearly dominates by content and recency cannot overturn it. This mirrors the RD design (near-duplicate content) but with a single dominant entry rather than a pair. The recency weight would not overturn a content signal with ratio >> 10⁸.

(b) **Reduce the recency weight's dynamic range** — e.g., measure degradation at a smaller `now` (so coord_cycle_relative spans fewer cycles), or use a different relevance function where content and recency are combined additively or with a bounded weight.

(c) **Increase the content signal's dynamic range** — e.g., higher-dimensional features (d=128+) or scaled features with larger magnitude variance, so the top-1 dot product dominates by many orders of magnitude.

Option (a) is the most targeted: it preserves the product relevance function and τ=50, and it makes the CU queries genuinely content-determined (the entry copied by the query has a dot product ~32 while the next-best has ~5.66, a ratio of ~5.6× — still not enough to overcome 10⁸× recency). Actually, option (a) alone may not suffice unless the content signal ratio exceeds the recency weight ratio. A combination of (a) and (c) may be needed: peaked queries AND stronger content signal.

**The ARCHITECT should simulate the proposed fix before bringing it to Rebecca**, to verify that CU degradation ≈ 0 and RD degradation ≈ 0.3–0.5, giving aggregate ≈ 0.12–0.20 (matching the spec's stated expectation). The CRITIC will re-verify.

---

## Summary Table

| Check | Verdict | Notes |
|---|---|---|
| Verification (a): degradation < 1.0 reachable | **FAILS** | CU degradation = 0.927 (not ~0); actual degradation = 0.887 (not ≤ 0.4). Recency weight dominates content on ALL queries. |
| Verification (b): 0.05 floor clearable | Passes (wrong reason) | Degradation 0.887 > 0.05, but driven by CU failure, not RD mechanism. Quantitative claims wrong by 5–7×. |
| Option E compliance | PASS | All entries retained, coords computed once at birth, consumer identical. |
| No corners | CONCERNING | 0.89 is technically in (0,1) but close to ceiling; spec's bound (≤0.4) is false. |
| Near-duplicate generation | PASS | Fully specified, deterministic. |
| Recency-discriminative fraction (40%) | Moot | Fraction irrelevant — CU queries dominate degradation. |
| No bar laundering | PASS | Locked bars and 0.05 floor unchanged. |
| Lesson logged | PASS | Rebecca's verbatim lesson present in §6.iii. |
| §7 output schema consistency | PASS | New battery fields present. |
| §9 checklist includes both verifications | PASS | Both verifications referenced in step 2. |

---

## VERDICT: BLOCKING ISSUES REMAIN

**One blocking issue:**

1. **Verification (a) fails.** The spec's claim that "content-only ranking succeeds on content-unique queries" (bounding degradation by 0.4) is mathematically false. Direct simulation shows CU degradation ≈ 0.93 and aggregate degradation ≈ 0.89 — close to the 1.0 ceiling corner. The root cause is that τ=50 creates a recency gradient (9 orders of magnitude) that overwhelms the content signal (1 order of magnitude) on all queries. The spec's quantitative predictions (0.12–0.20) are wrong by 5–7×. The frozen arm fails on content-unique queries, which is the exact failure condition Rebecca named ("content-only ranking must still succeed on content-unique queries").

The non-blocking items (the spec's wrong quantitative claims, the moot recency-discriminative fraction, the concerning proximity to the ceiling) all stem from this single root cause and would be resolved by fixing it.

**The revised sections are NOT ready for Rebecca's sign-off.** The ARCHITECT must revise the consumer's query/feature design so that content-only ranking genuinely succeeds on content-unique queries (CU degradation ≈ 0), making the spec's claimed bounds (≤ 0.4) and quantitative predictions (0.12–0.20) actually hold. The ARCHITECT should simulate the proposed fix before returning to the CRITIC. This is a targeted fix within the Option E amendment scope (§6.iii consumer query/feature spec only); it does not touch the frozen-arm specification (which is correct), the locked bars, or properties (i)/(ii).
