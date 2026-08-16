# CRITIC Verification — Property (iii) Failure (E1)

**Verifier:** CRITIC · **Date:** 2026-08-15 · **Subject:** TASK BUILDER's finding that property (iii) fails due to a spec design flaw, not an implementation bug.

---

## VERDICT: SPEC DESIGN FLAW CONFIRMED (goes to Rebecca per §5.iii routing, case (a))

Property (iii) fails with `downstream_degradation = 0.0` on all 3 seeds, no kill condition fires, and the verdict is `NOT_GREEN`. The TASK BUILDER's root-cause analysis is **mathematically correct**, the implementation **matches the spec verbatim**, and the failure is a **spec design flaw** (an internal contradiction plus a mathematical error in the spec's stated mechanism), **not an implementation bug**. The correct routing per §5.iii (e1_spec.md line 403 / task_spec_e1.md line 359) is **case (a): consumer/ablation mis-specified → fix and re-run, NOT a candidate death.**

---

## 1. Is the degradation really 0.0? — YES

Confirmed from both output files:

- `e1_output/e1_invariants.json` → `property_iii_load_bearing_coupling.downstream_degradation_per_seed = {"42": 0.0, "43": 0.0, "44": 0.0}`, `downstream_degradation_mean = 0.0`, `passes = false`, `consistent = false`.
- `e1_output/e1_run_results.json` → per-seed `downstream_quality_candidate = 1.0` and `downstream_quality_frozen = 1.0` on all 3 seeds → `downstream_degradation = 1.0 - 1.0 = 0.0` on every seed.

`quality_candidate = 1.0` is itself guaranteed by the spec: the candidate's re-resolved `coord_cycle_relative = now - e.cycle` is *identical* to the oracle's ground-truth `coord_cycle_relative = now - e.cycle`, so the candidate's top-k *is* the oracle's top-k by construction. The only question is whether `quality_frozen < 1.0`. It is not — it is also exactly 1.0.

---

## 2. Is the TASK BUILDER's analysis correct? — YES, exactly

The TASK BUILDER's claim: the frozen recency `exp((e.cycle-99)/50)` and oracle/candidate recency `exp((e.cycle-999)/50)` are the same monotonic transform of `e.cycle` (differing only by a constant factor), so they produce identical top-k rankings → `degradation = 0` by construction.

**Verified by direct calculation.** The consumer's relevance function (e1_experiment.py lines 1405–1414, matching e1_spec.md line 531 / task_spec_e1.md line 338 verbatim):

```
relevance(e, q) = exp(-coord_cycle_relative(e) / τ) · dot(v(e), q),   τ = 50
```

- Oracle/candidate: `coord_cycle_relative = now - e.cycle = 999 - e.cycle` → `relevance_o = exp((e.cycle - 999)/50) · dot`
- Frozen: `coord_cycle_relative = 99 - e.cycle` → `relevance_f = exp((e.cycle - 99)/50) · dot`

The ratio is constant across all entries:

```
relevance_f / relevance_o = exp((e.cycle - 99)/50) / exp((e.cycle - 999)/50)
                          = exp((999 - 99)/50)
                          = exp(900/50)
                          = exp(18) ≈ 6.566 × 10^7   (a CONSTANT, independent of e.cycle)
```

Confirmed numerically: across 1000 synthetic entries, `min(relevance_f/relevance_o) = max(...) = exp(18)` to floating-point precision. Because `np.argsort` is invariant to any positive multiplicative constant, the oracle, candidate, and frozen indices produce **byte-identical top-k rankings** → `recall@k` identical → `quality_candidate = quality_frozen = 1.0` → `degradation = 0.0`.

The TASK BUILDER's parenthetical that the two recencies "differ only by a constant factor" is precisely correct. The constant is `exp(18)`.

**The spec's stated mechanism is mathematically wrong.** e1_spec.md line 537 / task_spec_e1.md line 190 claim "stale entries get inflated recency weights" and line 541/564 claim "the consumer retrieves stale entries instead of recent ones." The inflation is real in *absolute* terms (every frozen weight is `exp(18)` ≈ 6.5×10⁷ times its oracle counterpart), but it is **uniform across all entries**, so it does **not** change which entries are most relevant. The spec conflates *absolute inflation* with *relative re-ordering*. The pairwise ratio `relevance(e₁)/relevance(e₂) = exp((e₁.cycle - e₂.cycle)/50) · dot₁/dot₂` is **identical** for oracle and frozen — the recency gradient between any two entries is preserved exactly.

---

## 3. Is this a spec design flaw or an implementation bug? — SPEC DESIGN FLAW

### 3.1 The implementation matches the spec verbatim

The consumer code (e1_experiment.py lines 1385–1424) implements exactly:
- `oracle_cr = now - cycles` (now = 999) — line 1394
- `candidate_cr = oracle_cr.copy()` (identical to oracle) — line 1396
- `frozen_cr = 99.0 - cycles` — line 1398
- `relevance = exp(-cr / 50) * dots`, top-k via `np.argsort(-relevance)[:10]` — lines 1405–1414
- recall@k = `|consumer_top_k ∩ oracle_top_k| / 10` — lines 1417–1418
- `degradation = quality_candidate - quality_frozen` — line 1174

Every term is pinned by the spec (e1_spec.md §6.iii lines 519–539; task_spec_e1.md §6.iii lines 318–348). The frozen index evaluates **all 1000 entries** with the stale coordinate, exactly as e1_spec.md line 537 / task_spec_e1.md line 345 require ("For entries appended after cycle 99 (entries 100–999), frozen `coord_cycle_relative` is `99 - e.cycle`"). No bar was invented, lowered, or raised.

### 3.2 The TASK BUILDER could NOT have avoided this within the spec

The spec pins the relevance formula, τ=50, the candidate coordinate (`now - e.cycle`), the frozen coordinate (`99 - e.cycle`), and explicitly requires the frozen index to evaluate entries 100–999. Any deviation that would break the ranking invariance — capping the frozen coordinate at 0, using a different τ for the frozen arm, or excluding entries 100–999 from the frozen retrieval set — would alter a pinned formula and violate §0.5 ("No bar invention, lowering, or raising"). The TASK BUILDER correctly followed the more specific, "exact" §6.iii consumer specification.

### 3.3 The spec is internally contradictory (the design flaw)

The spec contains two mutually inconsistent descriptions of the frozen-origin arm:

- **Arm 1 description** (task_spec_e1.md line 188; e1_spec.md line 298): *"Frozen answers diverge from candidate on AFTER_L queries (frozen index **doesn't include entries 100–999**)"* and *"the frozen index (built at `now=99`, never re-resolved) **does not include entries 100–999**"*. This says the frozen index only holds the first 100 entries.
- **§6.iii consumer spec** (task_spec_e1.md line 345; e1_spec.md line 537): *"For entries appended after cycle 99 (entries 100–999), frozen `coord_cycle_relative` is `99 - e.cycle`"*. This says the frozen index *does* evaluate entries 100–999 (with stale coordinates).

These cannot both be true. The TASK BUILDER resolved the contradiction in favor of the §6.iii consumer spec (the "FULLY SPECIFIED", "exact" section — task_spec_e1.md line 315; e1_spec.md §6.iii header), which is the defensible choice. But that choice is the one that produces `degradation = 0`, because evaluating all 1000 entries with a coordinate that differs only by a constant shift cannot change the ranking.

Had the TASK BUILDER instead followed the Arm 1 description (frozen index excludes entries 100–999), the frozen retrieval set would be the first 100 entries only, the oracle's top-k would draw from all 1000 (and be dominated by recent, post-99 entries), and `quality_frozen` would be ~0.0 → `degradation ≈ 1.0` (verified numerically: Option D below gives `degradation = 1.0` on all 3 seeds). The Arm 1 description is the version under which the spec's stated mechanism ("retrieves stale entries instead of recent ones") actually holds.

**This is the design flaw:** the spec's property (iii) mechanism is only mathematically sound under the Arm 1 description (frozen index excludes post-99 entries), but the §6.iii consumer spec — the "exact" section the TASK BUILDER is instructed to follow — specifies the version (frozen index evaluates post-99 entries with stale coords) under which the mechanism is a no-op.

### 3.4 The prior CRITIC review endorsed the flawed reasoning

critic_e1_spec_rereview_v3.md lines 137 and 287 explicitly endorsed the spec's mechanism: *"the frozen index's recency weights are drastically wrong (negative `coord_cycle_relative` for entries after cycle 99 causes `exp()` to blow up), so the degradation should be large and positive for ANY reasonable similarity function."* This is the same mathematical error — conflating absolute blow-up (`exp(18)`) with relative re-ordering (which does not occur). The prior review's confidence that "the key property (degradation > 0) should hold for any reasonable implementation" (line 289) was misplaced; it holds for no implementation that follows the §6.iii consumer spec verbatim.

---

## 4. Does the spec's routing handle this? — YES, correctly

§5.iii (e1_spec.md line 403; task_spec_e1.md line 359) is explicit:

> "Property (iii) fails — the candidate's coordinates are not load-bearing... NOT a separate kill condition (it is not in the locked 5); it is a GATE on the E1 pass verdict. If property (iii) fails, E1 is NOT delivered green. The candidate is not dead (D1 does not fire — no kill condition fired)... The program pauses for Rebecca's decision: **(a) the downstream consumer or ablation is mis-specified (a spec/implementation issue — fix and re-run, NOT a candidate death)**, or (b) the candidate's coordinates are genuinely not load-bearing (a mechanism limitation... D2 retry decision). Rebecca rules at the gate."

The observed state matches the precondition exactly:
- Property (iii) fails (`degradation = 0.0 ≤ 0` on all seeds; `mean = 0.0 < 0.05` floor).
- No kill condition fires (b, c, d, e, f all `false`; `candidate_dead = false`).
- Verdict = `NOT_GREEN`.

The routing to Rebecca is therefore correct. The cause is **case (a)** — the downstream consumer/ablation is mis-specified (internal contradiction + the §6.iii "exact" formula is a ranking-invariant no-op). This is a fix-and-re-run, NOT a candidate death. The TASK BUILDER's routing conclusion is correct.

---

## 5. What would fix it? — Two viable options (for Rebecca's decision)

The root requirement: the frozen relevance must **not** be a constant multiple of the oracle relevance. Verified numerically across seeds 42/43/44:

| Fix | Mechanism | degradation (seed 42/43/44) | Reliable? |
|---|---|---|---|
| **Option D — frozen index excludes entries 100–999** (follow the Arm 1 description) | Frozen retrieval set = first 100 entries only; oracle draws top-k from all 1000 (dominated by recent entries) → `quality_frozen ≈ 0.0` | **+1.000 / +1.000 / +1.000** | **YES** — large, positive, consistent |
| Option B — cap frozen `coord_cycle_relative` at 0 | Post-99 entries all get weight `exp(0) = 1.0`, losing the recency gradient among them | +0.000 / +0.000 / +0.000 | NO — still 0 (content signal alone picks the same top-k) |
| (Option C — different τ for frozen vs oracle) | Breaks the constant-ratio property | not tested | likely yes, but changes a pinned constant |

**Recommended fix: Option D.** It reconciles the spec's internal contradiction by making the §6.iii consumer spec consistent with the Arm 1 description ("frozen index doesn't include entries 100–999"). Under Option D, the spec's stated mechanism ("the consumer retrieves stale entries instead of recent ones") becomes literally true: the frozen index physically cannot return the recent entries the oracle returns, so `quality_frozen` collapses and `degradation` is large and positive. This is the smallest change that makes the spec self-consistent and the property satisfiable, and it requires no new bars.

Option B (cap) is *not* a reliable fix: with τ=50 over 1000 cycles, the recency gradient among the top content matches is weak, so flattening it (all post-99 entries at weight 1.0) leaves the content signal `dot(v(e), q)` to drive the same top-10 as the oracle — `degradation` stays 0. NB-4 (cycle-relative only) rules out switching to `coord_landmark_relative` for E1.

---

## 6. Are properties (i) and (ii) passing correctly? — YES

Confirmed from `e1_output/e1_invariants.json` and `e1_output/e1_run_results.json`:

### Property (i) — Correctness (kill (f), SIGNED)
- `oracle_agreement = 1.0` (bar = 1.0, strict) → **PASSES**
- Per-seed: {42: 1.0, 43: 1.0, 44: 1.0} — all 200 queries per seed match the oracle exactly (per-query agreement arrays are all 1s).
- Kill (f) does not fire (`fires = false`, `signed = true`).

### Property (ii) — Operational distinctness (kill (d))
- `latency_ratio_membership = 1.023` (bar ≤ 2.0) → passes
- `latency_ratio_bounded_k = 1.093` (bar ≤ 2.0) → passes
- `candidate_latency_growth_10x = 1.133` (bar ≤ 2.0) → **passes** (state-dependent collapse)
- `fair_naive_latency_growth_10x = 6.552` (bar ≥ 4.0) → **battery valid**
- `instrument_failure = false`
- Kill (d) does not fire. → **PASSES**

### Structural axes (all pass)
- L2 chain: `chain_integrity_final = 1.0` (after initial build, shift probe, and 10× growth all = 1.0) → passes; kill (b) does not fire.
- L4 shift: `coordinate_shift = 1.0`, `shift_per_append` = all True on all seeds → passes; kill (c) does not fire.
- L11 wall-clock: `wall_clock_shift_detected = 0.0` → passes; kill (e) does not fire.
- Reproducibility: `bit_identical = true`, `max_abs_diff = 0.0` on all seeds → passes.
- I3 contamination: all arms in-band → passes.
- L20 drift self-test: no-drift corr = 1.0; both perturbations < 0.50 → passes.

### Verdict
- All 5 kill conditions (b–f): `fires = false`. `candidate_dead = false`.
- Properties (i) and (ii): PASS. Property (iii): FAIL.
- `e1_verdict = NOT_GREEN` — exactly the §5.iii precondition.

---

## 7. Summary

| Question | Answer |
|---|---|
| Is `downstream_degradation = 0.0` across all seeds? | **YES** (0.0 on 42/43/44; mean 0.0) |
| Is the TASK BUILDER's constant-ratio analysis correct? | **YES** — ratio = exp(18), constant; rankings identical |
| Is the recency weight really just a constant shift? | **YES** — `frozen_cr − oracle_cr = 99 − 999 = −900` (constant) |
| Spec design flaw or implementation bug? | **SPEC DESIGN FLAW** — internal contradiction (Arm 1 vs §6.iii) + mathematical error in the stated mechanism |
| Could the TASK BUILDER have avoided it within the spec? | **NO** — §6.iii pins the formula; any fix would alter a pinned value (§0.5 violation) |
| Is the frozen index supposed to have all 1000 or only 100 entries? | **The spec contradicts itself** — Arm 1 says 100; §6.iii says 1000. §6.iii (the "exact" section) was followed → degradation 0 |
| Does §5.iii routing handle this? | **YES** — NOT_GREEN → Rebecca decides; case (a) = consumer/ablation mis-specified → fix and re-run, not a candidate death |
| What fixes it? | **Option D** (frozen index excludes entries 100–999, matching Arm 1) → degradation = 1.0 on all seeds. Option B (cap) does NOT fix it. |
| Properties (i) and (ii) passing? | **YES** — oracle_agreement = 1.0; candidate growth 1.13× on valid battery (fair-naive 6.55×) |

**VERDICT: SPEC DESIGN FLAW CONFIRMED.** The property (iii) failure is caused by a spec design flaw (an internal contradiction between the Arm 1 description and the §6.iii consumer spec, compounded by a mathematical error — conflating absolute recency inflation with relative re-ordering — that the prior CRITIC review endorsed). The implementation is faithful to the §6.iii "exact" specification. The correct routing is §5.iii case (a): the consumer/ablation is mis-specified → Rebecca rules at the gate → fix (recommended: Option D, reconcile §6.iii with the Arm 1 description) and re-run. This is **not** a candidate death and does not consume a D2 retry.
