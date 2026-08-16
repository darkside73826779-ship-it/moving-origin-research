# CRITIC Re-Review — Option E Fix (additive relevance + bucketed spike content)

**Verifier:** CRITIC · **Date:** 2026-08-15 · **Subject:** ARCHITECT's revised consumer parameterization for the Option E property (iii) ablation (FIX-1..4 in `e1_spec_CHANGES.md`), responding to the CRITIC's prior BLOCKING ISSUE 1 (`critic_e1_option_e_review.md`: recency weight overwhelming the content signal → CU degradation ≈ 0.93, aggregate ≈ 0.89 near the ceiling corner).

**Scope:** §6.iii (consumer relevance form + feature/query distribution), §2.2 (consumer constants), §7.3.1 (output schema), §9 (CRITIC checklist). The frozen-arm specification (§3 Arm 1, Option E) and properties (i)/(ii) are OUT OF SCOPE per the amendment.

---

## VERDICT: CLEARED

The ARCHITECT's fix is sound, the prior blocking issue is resolved, both of Rebecca's required verifications pass, and the result is not a corner. The revised sections are ready for Rebecca's sign-off.

The fix is **entirely within the consumer's parameterization** (relevance function + feature/query distribution), exactly as the prior review recommended ("a targeted fix within the Option E amendment scope (§6.iii consumer query/feature spec only); it does not touch the frozen-arm specification"). The frozen-arm spec (Option E), all locked bars, `consumer_tau=50`, and properties (i)/(ii) are unchanged.

---

## Verification (a): degradation < 1.0 is reachable — **PASSES**

**Claim:** CU degradation = 0.000 (content-only ranking succeeds on content-unique queries).

### (a.1) Independent re-derivation reproduces the claim exactly

I implemented the consumer from scratch directly from the spec text (`critic_independent_rerderivation.py`), NOT by importing the ARCHITECT's `verify_option_e_fix.py`. Results over seeds 42/43/44:

| Seed | RD degradation | CU degradation | Aggregate |
|---|---|---|---|
| 42 | 0.3000 | 0.0000 | 0.1200 |
| 43 | 0.2350 | 0.0000 | 0.0940 |
| 44 | 0.2300 | 0.0000 | 0.0920 |
| **MEAN** | **0.2550** | **0.0000** | **0.1020** |

This matches the ARCHITECT's `verify_option_e_fix_results.json` exactly (CU=0.000, RD=0.255, ALL=0.102). CU degradation is **exactly 0.000 on all three seeds** (every CU query has zero per-query degradation — the frozen top-k == oracle top-k == the CU bucket). ✓

### (a.2) The additive relevance form is correct for ensuring content dominates on CU queries

The relevance function is now `relevance(e, q) = dot(v(e), q) + λ·exp(-coord_cycle_relative(e)/τ)` with λ=16, τ=50. This **decouples content from recency**: the recency contribution is a bounded bonus `λ·w(e) ∈ [0, λ]` added to the content score, so it cannot overturn a content gap larger than λ.

- On CU queries, each query targets a CU bucket of **exactly k=10** members. Bucket members have `dot(v(e_b), q_b) ≈ A² = 100`; all other entries have `dot ≈ A·dot(u_b', u_b) ≈ O(1.8)` (random directions in d=32 are near-orthogonal) or `≈ 1.4` for fillers. The content gap is ~50× — far larger than the maximum recency bonus λ=16.
- Therefore **both the oracle and the frozen arm retrieve exactly the CU bucket as the top-k SET**; recency only reorders within the set (which doesn't change recall@k). → CU degradation = 0, exactly as claimed. ✓

This is mathematically tight, not empirical luck: the bucket of size exactly k is the top-k set by construction of the content gap, and adding any bounded constant/bonus to a set whose members all share the dominant content signal cannot push a non-member in.

### (a.3) Under Option E (frozen: coord=0 for all → recency bonus = λ constant), the frozen arm ranks purely by content

Under Option E, `coord_cycle_relative(e) = 0` for ALL entries → `w(e) = exp(0) = 1.0` for all → the recency bonus is the **constant `λ = 16` added to every entry**. Adding a constant to every element of an array does not change `argsort`. Therefore the frozen arm's ranking is **identical to ranking by content alone** (`argsort(content + λ) == argsort(content)`). Confirmed numerically: the frozen top-k equals the content-only top-k. ✓ This is the honest meaning of Option E ("content intact, temporal self-location gone") and the constant-λ collapse is the intended ablation, not a degenerate artifact.

### (a.4) The maximum degradation is bounded by the RD fraction (0.4 < 1.0)

Because CU degradation = 0 exactly (verified) and RD per-query degradation ∈ [0, 1]:

`aggregate = (30·0 + 20·d_rd)/50 = 0.4·d_rd ≤ 0.4·1.0 = 0.4 < 1.0`

The bound holds **exactly** (not approximately). Actual aggregate = 0.102 ≪ 0.4. ✓ This is the spec's claim (§6.iii line 600), now mathematically true. (The prior multiplicative spec's bound was false because CU degradation was ~0.93, not 0; the additive + bucketed fix makes CU degradation genuinely 0, so the bound holds.)

---

## Verification (b): the 0.05 floor is meaningfully clearable — **PASSES**

**Claim:** RD degradation = 0.255, aggregate = 0.102 (per-seed 0.120/0.094/0.092, all > 0.05).

### (b.1) RD degradation is genuinely > 0 (re-derived)

RD degradation = 0.255 mean (0.300/0.235/0.230 per seed), all > 0. ✓

### (b.2) The oracle's re-resolved coordinate genuinely selects different items than the frozen arm's stale coordinate

Mechanism check (seed 42, RD query 0, reproduced by my independent script and by the ARCHITECT's):
- RD bucket 0 has 30 members at cycles spread across 0..999.
- **Oracle** (re-resolved `coord = 999 − cycle`): recency bonus `λ·exp(-(999-cycle)/50)` is large only for the few most-recent members (coord < ~100); the oracle retrieves the 10 members with the largest recency bonus → the **recent subset**.
- **Frozen** (coord = 0 for all): recency bonus = constant λ → ranks by content-noise → retrieves the 10 members with the highest feature-noise alignment → a **content-noise-driven subset**.
- Overlap 0.80 → degradation 0.20 on this query. The two selection criteria (recency vs content-noise) are genuinely different, so the subsets differ. ✓

The recency bonus `λ·exp(-coord/τ)` genuinely depends on the re-resolved coordinate (it varies from ~16 for recent to ~0 for old), so the oracle's selection is coordinate-driven; the frozen arm's selection is not (constant bonus). This is exactly the load-bearing coupling property (iii) is meant to detect.

### (b.3) The aggregate degradation (0.102) is genuinely above 0.05

0.102 > 0.05, with ~2× margin. ✓

### (b.4) All per-seed values are above 0.05

Per-seed aggregate: 0.120 / 0.094 / 0.092 — all > 0.05. The minimum (0.092) clears the floor with ~1.8× margin. ✓

### (b.5) Is there a plausible scenario where degradation falls below 0.05?

I ran the consumer over **200 random seeds** (`critic_independent_rerderivation.py`): **0 of 200** produced aggregate < 0.05. The aggregate is `0.4·d_rd`; for it to fall below 0.05 requires `d_rd < 0.125` (recall > 0.875 on RD), i.e. the frozen arm's content-noise top-k must overlap the oracle's recency top-k by ≥ 9 of 10 — possible in principle but highly improbable, because the recency bonus strongly distinguishes the few most-recent members (coord < ~100, ~3 of 30) whose content-noise is independent of their recency. The ARCHITECT's λ×K_rd sweep confirms robustness: even at K_rd=20 (smaller than the chosen 30), aggregate = 0.056 (just above floor); the chosen K_rd=30 gives 0.102, a deliberate ~2× margin, not a razor-edge pass. ✓ The floor is meaningfully clearable, not trivially and not impossibly.

---

## Additional checks

### 1. Is the frozen-arm spec (Option E) still correct and unchanged? — **PASS**

§3 Arm 1 and §6.iii both consistently describe Option E: all entries retained, `coord_cycle_relative = 0` at birth (computed once, never re-resolved), consumer identical across arms, the only difference being whether coordinates moved after birth. The prior internal contradiction (Arm 1 said Option D "excludes entries 100–999"; §6.iii said "frozen coord = 99 − e.cycle") is resolved — both now describe Option E. The FIX-1..4 changelog explicitly states "The frozen-arm spec (§3 Arm 1, Option E) is CORRECT and UNCHANGED." Confirmed by reading §3 Arm 1 (line 303) and §6.iii (lines 549–561). ✓

### 2. Are the bucketed spike features well-specified and deterministic per seed? — **PASS**

Every RNG is pinned to an exact seed formula (§6.iii lines 528–540):
- Bucket directions: `rng_dir_b = default_rng(seed * 9_000_000 + b)`, normalized.
- Cycle spread permutation: `rng_perm = default_rng(seed * 7_000_000 + 1)`, round-robined across buckets.
- Per-entry feature noise: `rng_e = default_rng(seed * 100_000 + e.cycle)`.
- RD query noise: `rng_qd_j = default_rng(seed * 10_000_000 + 500 + j)`.
- CU query noise: `rng_q = default_rng(seed * 1_000_000 + 1000 + j)`.

The bucket assignment (50 buckets: 20 RD of size 30, 30 CU of size 10, 100 fillers), the round-robin cycle spreading, the direction normalization, and the feature/query formulas are all fully specified — no "e.g.", no unspecified items. My independent re-derivation reproduced the ARCHITECT's numbers bit-for-bit using only the spec text. ✓

(Minor note, non-blocking: the spec text says `rng_e = default_rng(seed * 100_000 + e.cycle)` while the ARCHITECT's script uses `seed * 100_000 + e` (entry index). These are **equivalent** because in the autobiography `cycles = arange(N)`, so `e.cycle == e` for every entry. No discrepancy in effect; the spec phrasing is if anything more precise.)

### 3. Is the additive relevance form a legitimate specification choice (not a trick to make the test pass)? — **PASS**

The additive form `dot + λ·exp(-coord/τ)` is a **standard** retrieval formulation — content score plus a bounded recency boost (analogous to BM25 + recency boost, a common production pattern). The prior **multiplicative** form `exp(-coord/τ)·dot` was the unusual one, and the CRITIC's prior review showed it was structurally broken (the 9-orders-of-magnitude recency gradient overwhelmed the content signal on every query at every reasonable τ). The additive form is the natural, principled fix: it decouples the content signal's dynamic range from the recency weight's dynamic range, which is exactly what the spec's *intended* CU/RD separation requires. The fix is responsive to the specific failure mode the CRITIC identified, is pre-registered with all constants pinned (λ=16, A=10, σ_f=σ_q=0.10, K_rd=30), and is verified by simulation before this review — not reverse-engineered to barely clear the floor (0.102 has ~2× margin; the design would also pass at λ=8 or K_rd=25, per the ARCHITECT's sweep). ✓

### 4. Is the 0.05 floor still the same bar Rebecca signed? — **PASS**

§6.iii line 572: `mean_degradation ≥ floor` with `floor = 0.05`. §7.3.1 `downstream_degradation_floor: 0.05` (lines 785, 828). The FIX changelog explicitly states "0.05 floor UNCHANGED." ✓

### 5. Is the 40% RD fraction unchanged? — **PASS**

20 of 50 queries = 0.4 (§6.iii line 586, §7.3.1 `recency_discriminative_fraction: 0.4`). The FIX changelog states "The 40% RD fraction is UNCHANGED." ✓

### 6. Are locked bars unchanged? — **PASS**

Latency ≤ 2.0, N=10, chain_integrity = 1.0, 3-seed policy, 0.05 floor, `consumer_tau=50` (pinned Q3-1), `consumer_feature_dim=32`, `consumer_k=10`, `N_consumer_queries=50` — all carried forward verbatim. The FIX changelog lists each as UNCHANGED. Properties (i) and (ii) are out of scope and untouched. ✓

### 7. Is Rebecca's verbatim lesson still in the spec? — **PASS**

§6.iii line 619, verbatim: *"An ablation whose result is a constant by construction measures nothing. A valid ablation removes exactly the organization under test and preserves everything else, and its expected result must be a task-dependent quantity in the open interval — never a corner."* The lesson is contextualized with all three prior degenerate/near-degenerate ablations (Option D → 1.0 ceiling; prior §6.iii multiplicative-constant → 0.0 floor; first Option E parameterization → 0.89 near-ceiling for the wrong reason) and the current revision's position at 0.102 in the open interval. ✓

### 8. Does the output schema capture the new parameters (λ, τ, bucket count, etc.)? — **PASS**

§7.3.1 `config` (lines 693–707) includes: `consumer_relevance_form`, `consumer_recency_coupling_lambda` (16.0), `consumer_content_signal_amplitude` (10.0), `consumer_feature_noise_sigma` (0.10), `consumer_query_noise_sigma` (0.10), `n_recency_discriminative_queries` (20), `recency_discriminative_fraction` (0.4), `n_rd_content_buckets` (20), `rd_content_bucket_size` (30), `n_content_unique_queries` (30), `n_cu_content_buckets` (30), `cu_content_bucket_size` (10), `n_content_buckets_total` (50), plus `consumer_tau` (50) and `consumer_k` (10) carried forward. The `property_iii_load_bearing_coupling` object (lines 825–835) captures per-seed degradation, mean, floor, consistency, the magnitude-reporting note, per-seed quality_candidate/quality_frozen, and a `consumer_spec` string describing the full additive+bucketed design. The §9 step-2 CRITIC checklist (line 1059) references both verifications (a) and (b) and the recency-discriminative battery. ✓

(Minor note, non-blocking: the schema retains vestigial `near_duplicate_sigma` and `recency_discriminative_query_sigma` fields at 0.10 from the prior near-duplicate-pair design; the functional noise params are now `consumer_feature_noise_sigma`/`consumer_query_noise_sigma`. The legacy fields are harmless duplicates, not a correctness issue.)

---

## Critical: is this still not a corner?

Rebecca's lesson: *"An ablation whose result is a constant by construction measures nothing."*

- **Is degradation = 0.102 a task-dependent quantity (varies by seed) or a constant?** It **varies by seed**: 0.120 / 0.094 / 0.092 (RD degradation 0.300 / 0.235 / 0.230). The variation is driven by how many of the 30 RD bucket members the frozen arm's content-noise selection happens to overlap with the oracle's recency selection — a genuine task-dependent quantity, not a constant. ✓
- **Could degradation be 0 by construction?** **No.** RD degradation > 0 on all 3 seeds (0.230–0.300). The frozen arm's constant-λ recency bonus genuinely cannot select the recent subset, so the oracle (recency-selected) and frozen (content-noise-selected) top-k genuinely differ on RD queries. CU queries contribute 0 by design (the intended content-dominates separation), but the RD battery ensures the aggregate is not forced to 0. ✓
- **Could degradation be 1.0 by construction?** **No.** CU degradation = 0 exactly on all seeds (content determines the top-k set; recency cannot overturn the 50× content gap), so the aggregate is bounded at `0.4 × 1.0 = 0.4 < 1.0`. Actual is 0.102, ~4.9× below the 0.5 midpoint-to-ceiling. ✓

The result is a task-dependent quantity (0.102, varying 0.092–0.120) comfortably inside the open interval (0, 1), driven by how much work the recency selection actually does on the recency-discriminative battery and ONLY on that battery (content-unique queries pass). This is exactly the "never a corner" condition Rebecca's lesson requires.

---

## Note on a minor imprecision in the spec's heuristic reasoning (non-blocking)

§6.iii line 595 offers a heuristic: "overlap by roughly `k²/K_rd = 100/30 ≈ 3.3` entries in expectation → recall ≈ 0.33 → per-query degradation ≈ 0.67 in the recency-dominated limit." This heuristic **overstates** the expected RD degradation (observed is 0.25, recall 0.75, not 0.33). The reason: the recency bonus `λ·exp(-coord/50)` is appreciable only for the ~3 most-recent members (coord < ~100); the remaining ~27 members have bonus ≈ 0, so both arms select the bulk of their top-k by the **shared** content-noise signal, inflating overlap well above the independent-random `k²/K` estimate. The spec correctly labels this as "in the recency-dominated limit" and immediately gives the authoritative **simulated** value (≈ 0.25), which is what binds. The heuristic is a rough upper-bound intuition, not a load-bearing claim; the simulated value is correct and verified. Non-blocking — the spec could tighten the heuristic, but it does not affect the test, the bars, or the verdict.

---

## Summary table

| Check | Verdict | Notes |
|---|---|---|
| (a) degradation < 1.0 reachable | **PASS** | CU degradation = 0.000 exactly (re-derived independently); bound ≤ 0.4 holds exactly. |
| (a) additive form correct for content dominance | **PASS** | Bounded bonus `λ∈[0,16]` cannot overturn 50× content gap; constant-λ under Option E doesn't change argsort. |
| (a) frozen arm ranks purely by content | **PASS** | `argsort(content + λ) == argsort(content)`; confirmed numerically. |
| (b) RD degradation > 0 | **PASS** | 0.255 mean (0.230–0.300); oracle recency-selects, frozen content-noise-selects; subsets differ. |
| (b) aggregate > 0.05 | **PASS** | 0.102, ~2× floor; all per-seed (0.120/0.094/0.092) > 0.05. |
| (b) plausible < 0.05 scenario | **No** | 0/200 random seeds below floor; K_rd=30 chosen for ~2× margin. |
| Not a corner | **PASS** | Task-dependent (varies by seed); not 0 by construction (RD>0); not 1.0 by construction (CU=0 bounds at 0.4). |
| Frozen-arm spec (Option E) unchanged | **PASS** | §3 Arm 1 + §6.iii consistent; FIX changelog confirms unchanged. |
| Bucketed features deterministic | **PASS** | All RNGs pinned; independent re-derivation reproduces numbers. |
| Additive form legitimate (not a trick) | **PASS** | Standard retrieval formulation; responsive to identified failure; pre-registered; ~2× margin. |
| 0.05 floor unchanged | **PASS** | §6.iii line 572; schema lines 785/828. |
| 40% RD fraction unchanged | **PASS** | 20/50 = 0.4. |
| Locked bars unchanged | **PASS** | Latency, N, chain_integrity, 3-seed, 0.05, τ=50, dim=32, k=10, N_q=50 all verbatim. |
| Rebecca's verbatim lesson present | **PASS** | §6.iii line 619, contextualized. |
| Output schema captures new params | **PASS** | λ, A, σ_f, σ_q, K_rd, bucket counts, relevance_form, consumer_spec string all in §7.3.1. |
| §9 checklist includes both verifications | **PASS** | Step 2 references (a) and (b) + recency-discriminative battery. |

---

## VERDICT: CLEARED

The ARCHITECT's revised consumer parameterization (FIX-1 additive relevance, FIX-2 bucketed spike features, FIX-3 bucket-targeted queries, FIX-4 simulation) resolves the prior BLOCKING ISSUE 1. Both of Rebecca's required verifications pass, confirmed by an independent from-scratch re-derivation that reproduces the ARCHITECT's numbers exactly (CU=0.000, RD=0.255, aggregate=0.102, per-seed 0.120/0.094/0.092 all > 0.05). The result is a task-dependent quantity (0.092–0.120) comfortably inside the open interval (0, 1), not a corner — not 0 by construction (RD degradation > 0 on all seeds), not 1.0 by construction (CU degradation = 0 bounds the aggregate at 0.4). The frozen-arm spec (Option E), all locked bars, `consumer_tau=50`, and properties (i)/(ii) are unchanged. The additive relevance form is a legitimate, standard specification choice responsive to the identified structural failure, not a trick to pass the test.

**The revised sections (§6.iii, §2.2, §7.3.1) are ready for Rebecca's sign-off.** No blocking issues remain. (One non-blocking note: the spec's `k²/K_rd ≈ 3.3 → recall ≈ 0.33` heuristic on line 595 overstates expected RD degradation and could be tightened, but the simulated value it cites is correct and is what binds.)
