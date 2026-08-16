# M3 / E2 IMPLEMENTATION TASK SPECIFICATION

**Serves: M3 Build/Task-Specification Clearance Gate**
**Status: DRAFT — requires independent CRITIC review; no build authorization**

**Date:** 2026-08-15 · **Author:** INTEGRATOR · **Governing state:** main `856c1868a78a2b0c87275ed53120677cce236fc7`; M2 GREEN/SEALED/ACCEPTED; M3/E2 V4 CRITIC CLEAR; Rebecca M3 GO ruling issued (docs/rulings/REBECCA_M3_GO.md).
**Authority chain:** Rebecca > constitution (`ARCHITECTURAL_CONSTITUTION.md`) > M0 decision sheet as adopted (`M0_DECISION_SHEET.md` + `REBECCA_RESPONSE_M0.md`) > approved M3/E2 V4 specification (`specs/m3_e2_spec_amended_v4.md`) > this task specification > agent judgment.
**Source specification:** `specs/m3_e2_spec_amended_v4.md` (768 lines) — this document extracts all implementable details from that specification for the TASK BUILDER. Every requirement below is traceable to a V4 section citation `[V4 §X.Y]`. Where this document and V4 differ, V4 is authoritative.
**Role boundary:** INTEGRATOR issues this task specification. TASK BUILDER implements against it. CRITIC reviews independently. This document does not itself authorize a build cell, a timebox, or any courier run. No implementation, code changes, diagnostic execution, scoring execution, or hold-out seed exposure is authorized by this document. Build authorization returns to Rebecca only after CRITIC clears this task specification.

---

## 0. Authorization basis

This task specification is prepared per Rebecca's M3 GO ruling (docs/rulings/REBECCA_M3_GO.md), Authorization boundary item 2: "INTEGRATOR to prepare the self-contained M3 implementation task specification and courier architecture only."

The ruling explicitly does NOT authorize:
- implementation or code changes;
- activation of a build cell or TASK BUILDER;
- diagnostic execution;
- scoring execution or a courier scoring run;
- exposure or use of hold-out seeds; or
- any L15–L17 integration claim.

The task specification must receive independent CRITIC clearance before any build authorization returns to Rebecca.

**Timebox (from Rebecca's ruling):** 4 sessions / 8 calendar days, starting 2026-08-15. Tripwire at: session 2, day 4, unresolved instrument-failure past one session, or ≥2-of-4 escalation. No cap-revision branch.

---

## 1. Scope: four laws tested at M3

M3 tests L1, L3, L5, and L6. No coupling or integration claim is made (L15–L17 reserved for M5) `[V4 §6, §9]`.

| Law | What is tested | M0-adopted bar `[V4 §1]` | Scoring seeds |
|---|---|---|---|
| L1 — Access physics (decay + rehearsal) | Binned-age decay curve + rehearsal-conditional effects | R² ≥ 0.85, β_age < 0; Spearman ρ ≥ 0.6 consistent sign | 3 minimum (non-p<.05 class) |
| L3 — Thick present | Relative loss reduction: state-alone vs raw-input-alone | ≥ 5% relative reduction at every horizon 1..5 | 3 minimum |
| L5 — Bi-temporality | Four-combination accuracy + chain-walk integrity | ≥ 0.95 accuracy; chain-walk k ≤ 10, accuracy = 1.00 | 3 minimum |
| L6 — Episodic completeness | Tagged-union return on every retrieval | 8-attack matrix + 4-row audit + 6 L18 arms | 3 minimum |

**L1 newest/oldest 2× bar:** DROPPED as a bar. Reported statistic only `[V4 §1]`.

**Hold-out policy:** ≥2 scoring seeds unseen in development, per standing rule `[V4 §1, §8.1]`. Development pool: {101, 102, 103, 104, 105}. Hold-out pool: {201, 202, 203}. All three hold-out seeds are used in full, in ascending order, for every scoring run. Hold-out seeds are forbidden in development, diagnostic, or pre-registration-validation use `[V4 §8.1]`.

---

## 2. §1.1 L5 growth-bar proposal — diagnostic-only, non-gating

The proposed L5 scan-avoidance operational bar (candidate per-walk latency growth from 250→1000-entry history ≤ 2.0×; fair-naive full-scan comparator growth ≥ 4.0× over the same range) is **diagnostic-only and non-gating** until Rebecca rules on it separately `[V4 §1.1(e), REBECCA_M3_GO.md §"L5 §1.1 proposal"]`.

Implementation: compute and report the growth measurements per `[V4 §4.4]`, but the L5 verdict branches `[V4 §4.9]` gate solely on the M0-adopted accuracy/chain-walk bars. The growth-threshold check must not gate any PASS/KILL/INSTRUMENT FAILURE branch.

---

## 3. L1 — Complete implementation contract `[V4 §2]`

### 3.1 Timeline and fixture `[V4 §2.1]`

- Creation phase: cycles 0–999 (1,000 appends, one per cycle).
- 5 age bins, each contiguous 200-cycle range: bin 0 = [0,199], bin 1 = [200,399], bin 2 = [400,599], bin 3 = [600,799], bin 4 = [800,999].
- Within each bin, 40 measured cycles (stride-5: `{lo_b + 5·i : i=0..39}`) + 160 filler cycles = 200 per bin.
- Priming phase: cycles 1000–2199 (1,200 rehearsal-increment events). 5 bins × 30 × 8 = 1,200 exactly.
- `now_final = 2200`. Final autobiography size = 2,200 entries.
- Every measured entry has a unique creation cycle → unique final age.

### 3.2 Factorial design `[V4 §2.2]`

- 5 age bins × 5 rehearsal levels (targets {0, 2, 4, 8, 16}) = 25 cells, 8 entries/cell, 200 measured entries total.
- Within-bin assignment: `i mod 5` for the i-th measured cycle in ascending order (F2 fix — decorrelates rehearsal from age, Spearman = −0.1225, not ±1.0).
- Rehearsal write mechanism: designated priming query → rehearsal-increment event appended `[V4 §2.3]`.

### 3.3 Candidate sets and tie-break `[V4 §2.4]`

- 10-entry stratified sets: 2 entries per age bin, heterogeneous rehearsal levels.
- **Tie-break:** seeded random permutation (seed=42, `numpy.random.RandomState(42).permutation(200)`) — genuinely label-independent (F1 fix, M1 B2 precedent).
- **Exactly 100 candidate sets per scoring seed.** Each entry appears exactly 5 times (balanced design, structural seed 777).
- **Per-entry aggregation:** `log_accessibility(e) = mean_{s ∈ sets(e)} log(11 − rank_s(e))`.
- Oracle satisfiability verified: R² = 0.985 (≥ 0.85), β_age = −0.00150 (< 0).

### 3.4 Accessibility metric and timing `[V4 §2.5]`

- `priority(e) = exp(−λ · age(e)) · (1 + β · log(1 + rehearsal(e)))`, λ = 0.001, β = 0.5 (fixed pre-registered).
- Retrieval: fixed-budget partial sort over 10 items, `time.perf_counter_ns()`, median ≥100 reps, warm-up excluded.
- **Batch-fallback (NF4 fix):** if median < timer resolution, batch B consecutive operations (start B=100, double until batch median > 10× resolution), report `median_batch_time / B`, log B. Inherits E1-RUN-1 construction-bug fix (commit dceb2584).

### 3.5 Primary test — binned marginal-mean curve `[V4 §2.6]`

1. Per bin: balanced marginal mean of `log(accessibility(e))` over 40 entries.
2. OLS fit: `mean_log_accessibility(bin) = β₀ + β_age · age_bin_representative(bin) + ε` over 5 points.
3. **Pass:** β_age < 0 AND R² ≥ 0.85.

Rehearsal-conditional tests:
- Age effect holding rehearsal fixed: 5 conditional curves, all negative slope.
- Rehearsal effect holding age fixed: 5 bin-level Spearman ρ ≥ 0.6, consistent sign.

### 3.6 L1 arms (L18 battery) `[V4 §2.8, §2.9, §2.10]`

| Arm | Definition | Pass condition |
|---|---|---|
| Candidate | Full priority(e), both factors | β_age < 0, R² ≥ 0.85, all ρ ≥ 0.6 |
| Frozen | priority(e) = constant | R² ≤ null 95th pct (0.749) |
| Recency-only | exp(−λ·age) only | R² ≥ 0.85, β_age < 0, all ρ < 0.6 |
| Rehearsal-only | 1 + β·log(1+rehearsal) only | β_age ≥ 0, all ρ ≥ 0.6 |
| Oracle | Ground-truth priority | R² ≥ 0.85, β_age < 0, all pass |
| Fair-naive | Seeded random permutation (seed=43) | R² ≤ null 95th pct (0.749) |
| Permuted | (age, rehearsal)→entry mapping permuted before fit | R² within own null band [−0.255, 0.764] |
| Shuffled | Priming query-to-entry assignment shuffled | All 5 ρ within shuffled null band |
| Empty | No entries | Defined error returned |

### 3.7 L1 verdict branches `[V4 §2.11]`

- **PASS:** marginal-mean curve conditions + rehearsal-conditional tests + ablation isolation criteria, all scoring seeds.
- **KILL:** any condition fails on any scoring seed.
- **INSTRUMENT FAILURE:** any L18 arm fails its exact bound; or priming ≠ 1,200 cycles; or cycle collision.
- **Reported-only:** newest/oldest ratio; joint model R².

---

## 4. L3 — Complete implementation contract `[V4 §3]`

### 4.1 Generator and state `[V4 §3.1, §3.2]`

- Seeded AR(3): `x[t] = 0.5·x[t-1] − 0.3·x[t-2] + 0.15·x[t-3] + 0.1·sin(t/23) + ε[t]`, 8-dimensional, ε ~ N(0, 0.05).
- Horizon H = 5, scored at every h=1..5.
- Sequence length: 1,010 cycles per seed.
- State: s[t] ∈ R^16, `s[t] = clip(A·s[t-1] + B·x[t], −C, C)`, A = blkdiag(8×[[0.9,0.1],[0,0.5]]), B[2i,i]=1.0, C=10.0, s[0]=0. Zero learned parameters.

### 4.2 Predictors and fitting `[V4 §3.3, §3.4]`

- State-alone: features = s[t] ∈ R^16, W_s ∈ R^{40×16}, OLS.
- Raw-input-alone: features = x[t] ∈ R^8, W_x ∈ R^{40×8}, OLS.
- Oracle: 3-lag features [x[t],x[t-1],x[t-2]] ∈ R^{24}.
- Fitting origins: t=0..699 (700). Buffer: 700–704. Evaluation origins: t=705..1004 (300). Disjoint windows, zero intersection.

### 4.3 Loss and bar `[V4 §3.6]`

- Per-channel per-horizon MSE, aggregated across channels only.
- `reduction_h = (MSE_h^raw − MSE_h^state) / MSE_h^raw`.
- **Pass:** ≥ 5% relative reduction at every horizon 1..5, all scoring seeds.

### 4.4 L3 arms and verdict `[V4 §3.8, §3.9, §3.10]`

- Floor check: frozen state reduction_h ≤ 0% at every horizon (dev seeds).
- Ceiling check: oracle 5% < reduction_h < 95% at every horizon (dev seeds).
- Permuted: channel-to-weight derangement, reduction_h ≤ 0% (exact bound).
- Shuffled: cycle order shuffled (both targets and raw comparator identically), reduction_h ≤ frozen + 0.01.
- **PASS:** two-sided validity clears + ≥ 5% reduction all horizons all scoring seeds.
- **KILL:** reduction < 5% any horizon any seed.
- **INSTRUMENT FAILURE:** floor/ceiling fails; zero-denominator across ≥2 seeds; permuted/shuffled fails bounds; sequence < 1,010 cycles.

**NF8 operational handling:** The L3 permuted arm's exact bound (reduction_h ≤ 0%) is very likely correct for all possible fitted weights but not rigorously proven for the full weight matrix W_s ∈ R^{40×16}. If it fails for some seed, INSTRUMENT FAILURE fires (not a candidate kill). The builder must implement the derangement exactly as specified (cyclic shift `j = (i+1) mod 8`) and route any violation to INSTRUMENT FAILURE, never to KILL.

---

## 5. L5 — Complete implementation contract `[V4 §4]`

### 5.1 Combination fixture `[V4 §4.1]`

- 4 combinations (A: currently-true/learned-early, B: currently-true/learned-late, C: stale/learned-early, D: stale/learned-late).
- 5 replicates with replicate-relative offsets (offset_r = 100·r, scoring_now_r = 500 + offset_r).
- 10 content-subjects × 5 replicates × 4 combinations = 200 facts. All 4/4 correct in every replicate.
- Open sentinel for A/B: `valid_until_r = scoring_now_r + 400`.

### 5.2 Queries and fair-naive `[V4 §4.2, §4.3]`

- 400 queries: 200 world-validity + 200 self-acquisition.
- Single-axis (fair-naive): `t_single(f) = acquired_at(f)`, predicts true iff `t_single ≥ scoring_now_r − 200`.
- Derived accuracy: 75.0% exactly on world-validity queries (3/4 correct, replicate-invariant).

### 5.3 Chain fixture `[V4 §4.5]`

- Separate 200-fact structure (total L5 fixture = 400 facts: 200 combination + 200 chain).
- 20 chains × 10 nodes = 200 facts. 20 × 9 = 180 edges.
- **Head pointer (F5 fix):** current-belief designation, updated on supersession. Freeze at cycle 100 → head frozen at (c,4), post-freeze nodes (c,5)–(c,9) appended but head not updated.
- 40 chain-walk queries: 20 full walks (k=10) + 20 partial walks (k=5).
- `walk_chain(chain_id, max_hops)` starts from head pointer, follows supersedes backward.
- Walk accuracy: 1.00 if exact path match, 0.00 otherwise.
- Frozen arm: walk accuracy = 0.00 for all 40 post-freeze queries (head at (c,4), expected from (c,9)).
- 5 bypass-injection tests `[V4 §4.5]`.

### 5.4 Sealed access-count and timing `[V4 §4.4]`

- `read_fact(fact_id)` increments sealed counter. `get_access_count_snapshot()` reads it.
- Pass for no-scan: access_count delta = k exactly.
- Timing: perf_counter_ns, median ≥100 reps, warm-up excluded, batched by history size {250,500,750,1000}, IQR logged, non-gating.

**NF9 operational handling:** The L5 frozen arm's walk accuracy is binary (0.00 or 1.00), not in the open interval (0,1). This is acceptable because the L5 frozen arm is an L18 negative control, not a property (iii)-style continuous degradation measure. The builder must implement the exact-match walk accuracy definition (no partial node-overlap credit) and label the frozen arm as "L18 negative control" in the artifact, not as a continuous degradation measure.

### 5.5 L5 arms and verdict `[V4 §4.7, §4.8, §4.9]`

- **PASS:** ≥ 0.95 on both query types + chain-walk = 1.00 for all 40 + access-count delta = k, all scoring seeds.
- **KILL:** accuracy < 0.95 any query type; chain-walk < 1.00; access-count mismatch.
- **INSTRUMENT FAILURE:** fair-naive ≠ 75.0% on world-validity; frozen post-freeze walk accuracy > 0; sealed counter fails; full-scan delta ≤ k; bypass test not caught.
- Growth thresholds: reported, non-gating (§1.1).

---

## 6. L6 — Complete implementation contract `[V4 §5]`

### 6.1 Schema and module graph `[V4 §5.2, §5.3]`

- `EpisodicResult = Success(EpisodicResponse) | Rejected(reason: str)`.
- `EpisodicResponse` = {content, source, context, self_position_at_encoding}.
- 3 frozen modules, **4 public callables** (F7 fix):
  - `episodic_store.py`: `query_episodic(query)`, `query_episodic_batch(queries)`.
  - `episodic_cache.py`: None (no cache exists — stated as fact).
  - `episodic_serialize.py`: `to_json(EpisodicResult)`, `from_json(bytes)`.

### 6.2 Attacks and L18 arms `[V4 §5.4, §5.5]`

- 8 named attack vectors. 4-row reachability audit (one per callable).
- 6 L18 arms: Empty, Permuted, Shuffled, Oracle, Frozen, Fair-naive — each with real transform and expected outcome.
- Empty requires `Rejected(reason="not_found")` to actually fire (not vacuous).

### 6.3 L6 verdict `[V4 §5.6]`

- **PASS:** all 8 attacks caught + all 4 audit rows pass + all 6 L18 arms show expected outcome.
- **KILL:** any attack #1–#7 not caught; any audit row fails; any L18 arm fails.
- **INSTRUMENT FAILURE:** attack #8 not caught (harness self-test).

---

## 7. §2 interface laws `[V4 §7]`

- L11: single-clock invariant — all timestamp-bearing writes read `now` from the cycle counter, including L6's encoding-time snapshot. Negative-injection test required.
- L13: memory writes stamped at write time — `landmark_relative` computed once at append, never recomputed. Negative-injection test required.
- L5 backdating: post-append mutation of `valid_from`/`valid_until` caught via hash-chain integrity.

---

## 8. Seed protocol and execution protections `[V4 §8]`

- Development pool: {101, 102, 103, 104, 105} — for pre-scoring validity/instrument checks only.
- Hold-out pool: {201, 202, 203} — all 3 used in full, ascending order, for every scoring run. Forbidden in development.
- Append-only exposure ledger: one record per seed-USE event `[V4 §8.1]`.
- O-14: re-run-on-failure FORBIDDEN.
- O-15: development runs diagnostic-only; scoring only through Rebecca's supervised-executor courier channel.
- ≥2 scoring seeds unseen in development (satisfied: 3 of 3).
- Full L18 battery on every positive claim.
- L9 hard fence: no learned/nonlinear retrieval channel.
- D1–D5 Persistence Doctrine binding.
- No L15–L17 integration claim.

---

## 9. NF7–NF10 operational handling

These non-blocking findings from the CRITIC V4 review (reviews/critic_m3_e2_spec_rereview_v4.md) require operational handling in the implementation:

### NF7 — R² reproducibility

Three printed R² values (frozen 0.236, fair-naive 0.320, rehearsal-only 0.996) were not independently reproducible by CRITIC's from-scratch implementation. None affects any branch-defining predicate.

**Operational requirement:** the implementation must emit the raw per-entry accessibility values, per-set ranks, and the exact candidate-set construction (structural seed 777 schedule) in the artifact, so that any reviewer can independently recompute the R² values from the raw data. The implementation must also include or reference the exact numpy call sequence used for candidate-set construction, shuffling, and tie-break application. If the verification script is included in the artifact package, it must be deterministic and reproducible from the stated constants and seeds alone.

### NF8 — L3 permuted arm bound

The exact bound (permuted reduction_h ≤ 0%) is very likely correct but not rigorously proven for all possible fitted weights.

**Operational requirement:** the builder must implement the derangement exactly as specified (cyclic shift j = (i+1) mod 8) and route any violation to INSTRUMENT FAILURE, never to KILL. The artifact must report the permuted reduction_h values per horizon per seed. If a false positive occurs, it triggers INSTRUMENT FAILURE (not a candidate kill), which is investigated under the construction-bug guard without consuming D2 budget.

### NF9 — L5 binary walk accuracy

The L5 frozen arm's walk accuracy is binary (0.00 or 1.00), a corner by the Option E lesson's letter but acceptable for an L18 negative control.

**Operational requirement:** the builder must implement the exact-match walk accuracy definition (no partial node-overlap credit). The artifact must label the L5 frozen arm as "L18 negative control" and note that the binary outcome is inherent to the chain-walk accuracy definition and acceptable because the contrast between candidate (1.00) and frozen (0.00) is the measurement, not a continuous degradation value.

### NF10 — STATE.md currency (in progress)

STATE.md has been updated to reflect the V4 CRITIC CLEAR, Rebecca's M3 GO ruling (active timebox 4 sessions / 8 days), the INTEGRATOR's task-spec and courier-architecture submission, and the CRITIC's narrow BLOCK on B1-B3. The governing commit has been updated to verified GitHub main `856c1868a78a2b0c87275ed53120677cce236fc7` (verified 2026-08-15T23:53Z). However, the RECORDER has not yet extended the provenance log with entries for Rebecca's M3 GO ruling, the INTEGRATOR's deliverable submission, the CRITIC's narrow BLOCK, or the B1-B3 fixes. NF10 remains in progress until RECORDER completes provenance attestation.

**Operational requirement:** the artifact package presented to Rebecca at the M3 Build/Task-Specification Clearance Gate must include the current STATE.md hash (attested by RECORDER) and the verified repository main commit as attestation basis. The RECORDER must attest the updated STATE.md hash and extend the provenance log before focused CRITIC re-review.

---

## 10. Output artifact requirements

Each law's scoring run must produce artifacts sufficient for independent JUDGE scoring from returned artifacts only. At minimum:

- Per-law results JSON with all arm-level statistics, pass/fail/KILL/INSTRUMENT FAILURE verdicts per seed.
- L18 battery checklist results with exact numeric bounds.
- Manifest with commit hash, scoring seeds, deviation log, wall-clock.
- Profile vector for L20 drift self-test.
- Reproducibility check (bit-identical on non-timing metrics).
- Raw per-entry/per-query data sufficient for independent recomputation (NF7).
- Seed-exposure ledger entries for the scoring run.

The exact artifact schema is specified in V4 §2.9, §3.9, §4.8, §5.3 (per-arm artifact fields) and V4 §8.1 (ledger).

---

## 11. What this task specification does NOT authorize

- No build cell activation.
- No TASK BUILDER assignment.
- No diagnostic execution.
- No scoring execution.
- No hold-out seed exposure.
- No courier scoring packet creation.
- No M3 timebox activation by this document. (Rebecca's M3 GO ruling activates the timebox; this document does not.)
- No L15–L17 integration claim.

This document is a specification for independent CRITIC review only. Build authorization returns to Rebecca only after CRITIC clears this task specification.

---

## 12. Source manifest

| Document | Project Files path |
|---|---|
| Rebecca M3 GO ruling | `docs/rulings/REBECCA_M3_GO.md` |
| M3/E2 V4 specification | `specs/m3_e2_spec_amended_v4.md` |
| M3/E2 V4 changelog | `specs/m3_e2_spec_changelog_v4.md` |
| CRITIC V4 review (CLEAR) | `reviews/critic_m3_e2_spec_rereview_v4.md` |
| STATE.md (current) | `state/STATE.md` |
| Provenance log | `docs/rulings/provenance_log.md` |
| ROLE_SESSIONS.md | `state/ROLE_SESSIONS.md` |
| Courier architecture | `specs/m3_e2_courier_architecture.md` |
| GitHub repository | `darkside73826779-ship-it/moving-origin-research` (main `856c1868`) |

---

— INTEGRATOR, 2026-08-15
