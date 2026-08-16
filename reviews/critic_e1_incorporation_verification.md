# CRITIC Verification — E1 v3 GO Ruling Incorporations

**Date:** 2026-08-15 · **Verifier:** CRITIC · **Scope:** Verification that the ARCHITECT correctly incorporated Rebecca's E1 v3 GO ruling items (Q2 replacement + Q3 completions + NB-4/5/6 resolutions) into `e1_spec.md`. This is an incorporation-completion verification within the approved v3 structure, NOT a full re-review.

**Sources verified:**
- `/home/user/workspace/e1_spec.md` (the updated spec, 1137 lines)
- `/home/user/workspace/e1_spec_CHANGES.md` (the changelog)
- `/home/user/workspace/uploaded_attachments/7b9d3c33e58d485f8a8c8bd5957fc915/REBECCA_E1_V3_GO.md` (Rebecca's binding ruling — source of truth)

---

## Checklist

### 1. Q2: 0.5 slope-ratio REPLACED with battery-validity approach — VERIFIED

- **Slope-ratio no longer a trigger (diagnostic only):** VERIFIED. §4.2 (line 336) states `scaling_collapse_ratio` is "RETAINED as a REPORTED diagnostic ONLY, never a trigger (resolves NB-1)." §6.ii (lines 462–464) restructure note confirms "The 0.5 slope-ratio collapse trigger … is NOT SIGNED and is REPLACED … The slope ratio is RETAINED as a reported diagnostic ONLY, never a trigger." §6.ii (lines 496–501) keeps the regression fit but states it "carries NO kill and is NEVER a trigger." Matches ruling Q2 item 3 verbatim.
- **Candidate side kill (d) at ≤ 2.0× (unchanged locked bar):** VERIFIED. §6.ii component 1 (lines 468–473): `candidate_latency_growth_10x = latency(1000)/latency(100)`, bar `≤ 2.0`, "SAME locked bar as d1 … UNCHANGED — it is carried forward from M0." §0.2 (line 30) confirms latency bar UNCHANGED in value.
- **Battery-validity requirement: fair-naive ≥ 4.0× growth:** VERIFIED. §6.ii component 2 (lines 475–480): `fair_naive_latency_growth_10x ≥ 4.0`. Matches ruling Q2 item 2 exactly.
- **Instrument-failure path (run unscoreable, battery revised, no kill/retry touched):** VERIFIED. §6.ii component 2 (line 480): "INSTRUMENT failure: the run is unscoreable, the battery is revised, and no kill condition or retry budget is touched … routed to the ARCHITECT/CRITIC for battery revision, NOT to kill (d)." §5(d) (line 377) restates identical routing. §6.iv verdict table (line 579) confirms "If battery invalid → instrument failure, run unscoreable." Matches ruling Q2 item 2 verbatim.
- **Collapse = candidate failing ≤ 2.0× on validated battery:** VERIFIED. §6.ii component 3 (line 482): "Collapse = the candidate failing bar (1) (growth > 2.0×) on a battery validated by (2) (fair-naive growth ≥ 4.0×)." Matches ruling Q2 item 3.

### 2. Timing methodology mandated (resolves NB-6) — VERIFIED

- **Median over repeated executions, warm-up excluded, monotonic clock, dispersion reported:** VERIFIED. §6.ii component 4 (lines 484–488): (i) median over ≥100 repetitions per query per point; (ii) warm-up excluded (first 10% discarded); (iii) monotonic clock (`time.monotonic_ns()`); (iv) dispersion (IQR/SD) per point. §5(d) (line 383) restates all four identically. Matches ruling Q2 item 4 verbatim. NB-6 resolved note present (§6.ii line 492).
- **Alongside every latency figure:** VERIFIED. §6.ii component 4(iv) (line 488) states "Dispersion reported alongside every latency figure." Schema ships `candidate_latency_iqr_per_point` and `fair_naive_latency_iqr_per_point` per seed (lines 659, 682) and as means (lines 748–749).

### 3. Downstream consumer FULLY SPECIFIED (NB-3 promoted to required-before-build) — VERIFIED

- **Similarity function exactly specified (formula, not "e.g."):** VERIFIED. §6.iii (lines 521–525): `content_similarity(e, q_item) = dot(v(e), q_item)` — "NOT cosine similarity — dot product." Explicit formula, no "e.g." in the definition.
- **Query set exactly specified (count, generation, per-seed):** VERIFIED. §6.iii (line 527): `N_consumer_queries = 50`, each `q_j = rng_q.standard_normal(32)` where `rng_q = numpy.random.default_rng(seed * 1000000 + 1000 + j)`. Fresh synthetic vectors (NOT autobiography entries). Fully pinned per-seed generation.
- **How the consumer uses coord_cycle_relative specified:** VERIFIED. §6.iii (lines 529–533): `relevance(e, q_item) = exp(-coord_cycle_relative(e) / τ) * dot(v(e), q_item)` with `τ = 50`, top-k=10 retrieval. Exact.
- **Degradation measured under frozen-origin ablation specified:** VERIFIED. §6.iii (lines 535–541): consumer run over candidate's re-resolved index AND frozen-origin index; `coord_cycle_relative` frozen at `99 - e.cycle`; recall@k vs oracle top-k; `degradation = quality_candidate - quality_frozen`. Exact.
- **Remaining "e.g." or vague specifications in the consumer:** NONE in the consumer's definitional text. The only "e.g." occurrences in §6.iii are in illustrative explanatory passages (e.g., line 560 'inspect the ACTUAL magnitude (e.g., "degradation = 0.34")' — an example value, not a vague spec). The spec header explicitly states "no 'e.g.', no unspecified query items" (line 517). VERIFIED.

### 4. Report observed degradation magnitude (Q3 attachment 2) — VERIFIED

- **Per-seed and mean magnitude reported (not just floor-clearance):** VERIFIED. §6.iii (line 560): "the spec REQUIRES reporting the observed degradation magnitude, not merely whether it clears the 0.05 floor." Schema (lines 755–762) ships `downstream_degradation_per_seed` (3 floats), `downstream_degradation_mean`, `downstream_quality_candidate_per_seed`, `downstream_quality_frozen_per_seed`. §7.3.1 also ships per-seed `downstream_degradation` and `downstream_degradation_magnitude_reported` (lines 672–673). Matches ruling Q3 attachment 2 ("the floor is a floor, not a finding") — phrase quoted verbatim in §6.iii (line 560) and schema note (line 758).

### 5. NB-5 resolved — VERIFIED

- **At each history size, query battery includes only landmarks designated by that point:** VERIFIED. §6.ii NB-5 note (line 453): "At each history size, the query battery includes only landmarks designated by that point in the run." Concrete example: "At history size 100, only the 8 immediate landmarks are in the query battery (the 2 deferred landmarks enter the battery at history size 250+)." Matches ruling verbatim.
- **Deferred-designation queries against not-yet-designated landmarks excluded by construction:** VERIFIED. §6.ii (line 453): "Deferred-designation queries against not-yet-designated landmarks are ill-posed and excluded by construction — a query about a landmark L that has not yet been designated … such queries are NOT issued."
- **Pre-designation window described as shift-measurement material (AFTER_L → BEFORE_L flip):** VERIFIED. §6.ii (line 455): "entries whose e.cycle falls in [L.cycle, L.designated_at) shift from AFTER_L to BEFORE_L upon designation … this AFTER_L → BEFORE_L flip is exactly the shift that kill (c)'s per-append shift artifacts (§5c, N12) capture … The pre-designation window is not an edge case to be worked around — it is the shift-measurement material itself." Matches ruling verbatim.

### 6. NB-4 standing note — VERIFIED

- **Consumer exercises cycle-relative only, accepted for E1 scope, full landmark-relative coupling at M5:** VERIFIED. §6.iii standing note (line 570): "the downstream consumer exercises coord_cycle_relative (the offset counter, C1.1) ONLY — not coord_landmark_relative … Full landmark-relative coupling belongs to the L15 matrix at M5. A more complete consumer at M5 would use both coordinates." §8 (line 979) restates: "NB-4 standing note: the consumer exercises coord_cycle_relative only … accepted for E1 scope; full landmark-relative coupling belongs to the L15 matrix at M5." Matches ruling Standing section verbatim.

### 7. No structural changes — VERIFIED

- **Three-property test structure unchanged:** VERIFIED. §2.1 (lines 222–237) retains the three properties (i) correctness, (ii) operational distinctness, (iii) load-bearing coupling as approved in v3. No fourth property added; no property removed.
- **Locked bars unchanged (latency ≤ 2.0×, N=10, chain_integrity = 1.0, 3 seeds):** VERIFIED. §0.2 (lines 29–33): N=10 UNCHANGED; latency bar UNCHANGED in value; chain_integrity bar UNCHANGED; seeds = 3 UNCHANGED. "No bar laundering" note (line 36) reaffirms all carried forward verbatim. Changelog Q2-1 confirms "the SAME locked bar as d1."
- **Fair-naive definition unchanged:** VERIFIED. §6.ii fair-naive definition (lines 439–445) identical to v3: full event-log access including designation events, recompute-by-scan at query time, no maintained index state, matches candidate on answers. Not altered by Q2/Q3.
- **Slope ratio RETAINED as a diagnostic (not removed):** VERIFIED. §4.2 (line 336) and §6.ii (lines 496–501) retain the regression fit and `scaling_collapse_ratio` as a reported diagnostic. Schema retains `scaling_collapse_ratio` (line 744) and `scaling_collapse_ratio_diagnostic` (line 833) with explicit "never a trigger" notes.

### 8. Internal consistency — VERIFIED

- **JSON schemas include the new fields:**
  - *battery_validity:* `battery_valid` present in `mean_over_seeds.candidate` (line 707), `property_ii_operational_distinctness` (line 737), `kill_conditions.(d)` (line 768), and `e1_invariants.json` kill (d) (line 809). `instrument_failure` present in `property_ii` (line 741), `kill_conditions.(d)` (line 768), and invariants kill (d) (line 809). VERIFIED.
  - *timing dispersion:* `candidate_latency_iqr_per_point` (line 659), `fair_naive_latency_iqr_per_point` (line 682), means (lines 748–749); `timing_methodology` string in property_ii (line 750) and invariants (line 835); config `timing_repetitions`/`timing_methodology` (lines 638–639). VERIFIED.
  - *degradation magnitude:* `downstream_degradation_magnitude_reported` per-seed (line 673), `downstream_degradation_magnitude_note` (line 758), `downstream_degradation_per_seed` + `downstream_degradation_mean` + quality arrays per-seed (lines 755–762); mirrored in `e1_invariants.json` property_iii (lines 840–843). VERIFIED.
- **Profile vector still works with the changes:** VERIFIED. §7.3.5 (lines 919–921): 6-element vector uses `candidate_latency_growth_10x` (replacing the retired slope-ratio trigger), order pinned. N8 note (line 937) explicitly documents the swap and confirms `scaling_collapse_ratio` is NOT in the vector (diagnostic only). Perturbation definitions (lines 927, 930) updated for the 6-element vector. Consistent.
- **Kill conditions correctly mapped:** VERIFIED. §5(d) (lines 374–383) maps d1 (latency_ratio > 2.0) OR d2 (candidate_latency_growth_10x > 2.0 on valid battery) → kill (d); battery-invalid → instrument failure (not a kill). §6.iv verdict table (lines 576–583) maps each property/bar/kill consistently. `kill_conditions.(d)` schema object (line 768) encodes the trigger string, both bars (2.0 / 4.0), `battery_valid`, and `instrument_failure`. Internally consistent.

---

## Additional consistency check (not on checklist, noted for completeness)

- **Timebox clock-start wording:** Rebecca's v3 GO ruling (Q4) states the clock starts "when decomposition (with this ruling's items incorporated) clears CRITIC verification." The spec line 1136 states "the timebox clock starts when the CRITIC clears them (§10.2)" — consistent. §10.2 (line 1016) says "clock starts when the revised spec clears Rebecca's gate (§9 step 3)"; since Rebecca's v3 GO ruling IS that gate clearance, these are reconcilable (the gate is already cleared; the remaining gate is CRITIC incorporation verification). This is a wording nuance, NOT a missing or incorrect incorporation — the timebox itself is unchanged (3 sessions / 7 days, SIGNED) and was not an item Rebecca asked the ARCHITECT to change. No action required; noted only for transparency.

---

## Verdict

**VERIFIED.**

All eight checklist items are correctly and completely incorporated into `e1_spec.md`, consistent with Rebecca's binding E1 v3 GO ruling (Q2 replacement, Q3 attachments 1 & 2, NB-3 promotion, NB-4 standing note, NB-5 resolution, NB-6 resolution). The incorporations are specification completions within the approved v3 structure — the three-property test structure, all locked numeric bars (latency ≤ 2.0×, N=10, chain_integrity = 1.0, 3 seeds), and the fair-naive definition are unchanged; the slope ratio is retained as a diagnostic, not removed. The JSON output schemas include the new fields (battery_validity, timing dispersion, degradation magnitude) and the profile vector and kill-condition mappings are internally consistent.

**The timebox clock is cleared to start.** Decomposition may proceed to the TASK BUILDER with the spec as written.
