# E1 SPEC — CHANGELOG (v1 → v2 → v3, ARCHITECT revisions)

**Date:** 2026-08-15 · **Author:** ARCHITECT · **Revisions:** v1 (pre-CRITIC-review) → v2 (post-CRITIC-review) → v3 (post-Rebecca-gate-ruling, constitution amendment) → v3+Q2/Q3 (Rebecca's GO ruling incorporations, specification completions, this file)
**v2 Trigger:** CRITIC review dated 2026-08-15 — 5 BLOCKING + 12 NON-BLOCKING issues + 4 PENDING REBECCA items.
**v3 Trigger:** Rebecca's E1 gate ruling dated 2026-08-15 (binding) — NO-GO AS CONSTITUTED; test redefined; one revision cycle authorized. The ruling retires the informational collapse test (old kill (a)), promotes kill (f) to primary correctness kill, promotes kill (d) to operational-distinctness discriminator, and adds property (iii) load-bearing coupling. The naive arm is strengthened to fair naive. Candidate 1.1 is NOT charged as a death.
**v3+Q2/Q3 Trigger:** Rebecca's E1 v3 GO ruling dated 2026-08-15 (binding) — GO, with one replacement (Q2) and three completions (Q3). These are specification completions within the approved v3 structure, NOT a new revision cycle. Rebecca ruled that no third full review cycle is required. The CRITIC verifies the incorporations; the timebox clock starts when the CRITIC clears them.

---

## Summary of v3 (the Rebecca-gate-ruling revision)

The v2 spec's equivalence test (§6) — the center of gravity — was built on an existence proof that held only against a HANDICAPPED naive arm. The naive arm was specified as "no designation tracking," but designation events are timestamped entries in the same append-only autobiography the candidate reads. A FAIR naive — the strongest honest timestamps-and-scan implementation — reads the full event log (including designation events), computes `e.created_at < L.designated_at`, and agrees with the candidate at 1.0.

**THEOREM (Rebecca, binding):** For ANY deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle (the oracle is a log replay). Therefore the pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable — for this candidate, for every D2 retry, for anything. The answer-equivalence collapse test (old kill (a)) is a criterion nothing can pass, and a criterion nothing can pass is a broken criterion, not a hard one.

**PROGRAM FINDING (E1's first real finding, produced at spec-time for zero compute):** Self-location cannot be defined informationally over logged events. It must be defined operationally and integratively.

The v3 revision implements Rebecca's ruling by replacing the single-axis informational collapse test with a **three-property test**: (i) correctness (kill (f), SIGNED, PROMOTED), (ii) operational distinctness (kill (d), PROMOTED, extended with a state-dependent query battery), (iii) load-bearing coupling (NEW, a miniature of the L15 test). The naive arm is strengthened to fair naive. The locked numeric bars (latency ≤ 2.0, N = 10, chain_integrity = 1.0, 3 seeds) are carried forward UNCHANGED. The retired equivalence bar (≤ 0.90) is RETIRED (not softened — it is unsatisfiable by construction). Candidate 1.1 is NOT charged as a death; the mechanism remains legitimate under the revised test.

---

## v3 CHANGES (Rebecca-gate-ruling revision — constitution amendment)

### V3-1 — Old kill (a) RETIRED (the informational collapse test is unsatisfiable by construction)

**Root cause:** The v2 existence proof (§6.5) held only because the naive arm was handicapped (it did not receive designation events). Rebecca's theorem proves that for any deterministic candidate whose coordinates are functions of logged events, fair-naive ≡ oracle on answers. The pair {naive_agreement ≤ 0.90, oracle_agreement = 1.0} is jointly unsatisfiable. The answer-equivalence collapse test is a criterion nothing can pass.

**Fix:** Kill (a) is RETIRED (§0.2, §0.5, §5(a), §12). The metric `equivalence_agreement` is retained as a REPORTED diagnostic (§4.2) — expected ≈ 1.0 (confirming the theorem holds and the fair naive is not handicapped). It carries NO kill and NO distinctness claim. The retirement is documented in the constitution amendment log (§12.1) with rationale.

### V3-2 — Kill (f) SIGNED and PROMOTED to primary correctness kill (property (i))

**Root cause:** In v2, kill (f) was PROPOSED [PENDING REBECCA SIGN-OFF] — a candidate that is "distinguishable from naive but wrong" (oracle_agreement < 1.0). Rebecca SIGNED it at the gate (ruling §4 item 3: "APPROVED and promoted per §2(i)").

**Fix:** Kill (f) is SIGNED and PROMOTED to the primary correctness kill condition (§0.2, §0.5, §5(f), §6.i, §12.1). It is no longer PENDING. The trigger is `oracle_agreement < 1.0` on the full query battery including deferred-designation landmark queries. This is property (i) (correctness) — the floor: a candidate that is wrong has no place, regardless of its operational or integrative properties.

### V3-3 — Kill (d) PROMOTED to operational-distinctness discriminator (property (ii)), extended with state-dependent query battery

**Root cause:** In v2, kill (d) was a latency-only check (latency_ratio > 2.0 on bounded-output queries). Rebecca's ruling (§2(ii)) promotes it to the operational-distinctness discriminator — the NEW anti-collapse discriminator that replaces the retired informational collapse test.

**Fix:** Kill (d) is PROMOTED (§0.2, §0.5, §5(d), §6.ii, §12.1). The latency bar (≤ 2.0) is UNCHANGED. Kill (d) is EXTENDED with a state-dependent query battery (§6.ii):
- Per-query latency measured at 5 history-size points (100, 250, 500, 750, 1000) for BOTH the candidate and the fair-naive arm.
- Both scaling curves reported (candidate: flat/logarithmic O(1)/O(log n); fair-naive: linear O(n)).
- Collapse criterion (d2, NEW): `candidate_slope > 0.5 × fair_naive_slope` → the candidate is secretly replaying the log at query time → kill (d) fires.
- The candidate collapses if its own scaling matches recompute-by-scan (i.e., it is secretly replaying) — this is the operational replacement for the old answer-agreement collapse test.

### V3-4 — Property (iii) load-bearing coupling added (NEW — a miniature of the L15 test)

**Root cause:** Rebecca's ruling (§2(iii)): "A candidate whose coordinates are consumed by nothing is a cache with a philosophy." The theorem shows coupling, not answers, is where "moving origin" has meaning.

**Fix:** Property (iii) is added (§0.1, §2.1, §6.iii, §12.1). A minimal downstream consumer — a toy recency-weighted retrieval implementing L1's access physics over the index's coordinates — is run over BOTH the candidate's re-resolved index AND the frozen-origin index (ablation). The consumer's retrieval quality (recall@k against the oracle) must measurably degrade over the frozen index: `downstream_degradation = quality_candidate - quality_frozen > 0` on all 3 seeds (effect direction consistent) AND `mean_degradation ≥ 0.05` (pre-registered floor). This is a miniature of the L15 test (M5 applies in full). Property (iii) failure is NOT a separate kill condition (it is not in the locked 5); it is a GATE on the E1 pass verdict (§5 property (iii) failure routing, §9 step 13): if it fails and no kill condition fires, E1 is not-green (candidate alive but place not earned); the program pauses for Rebecca's decision.

### V3-5 — Naive arm STRENGTHENED to fair naive (the CRITIC's new center of gravity)

**Root cause:** The v2 naive arm (`naive now−created_at`) was handicapped: it read only the `created_at` column and did NOT receive designation events. This handicapping was the only reason the v2 existence proof appeared to show candidate ≠ naive. Rebecca's ruling (§1): "A fair naive — the strongest honest timestamps-and-scan implementation — reads the full event log (including designation events), computes `e.created_at < L.designated_at`, and agrees with the candidate at 1.0."

**Fix:** The naive arm is RENAMED to `fair naive` and STRENGTHENED (§0.4, §3 arm 4, §6.ii, §12.1):
- Full event-log access (including designation events) — NOT handicapped.
- Recompute-by-scan at query time — no maintained index state (no offset counter, no landmark registry with pre-computed coordinates).
- Same answers as the candidate and oracle (Rebecca's theorem: fair-naive ≡ oracle on answers) — MATCHES the candidate on answers (expected, no longer a kill).
- DIFFERS on cost scaling (fair-naive scans at O(n) per query; candidate answers at O(1)/O(log n) per query) — this is the property (ii) probe.
- The CRITIC's new center of gravity (§9 step 2): verify the fair naive is genuinely fair (full event-log access, no maintained state, recompute-by-scan) and not a strawman.

### V3-6 — Candidate 1.1 NOT charged as a death; distinctness claim DROPPED

**Root cause:** Rebecca's ruling (§3): Candidate 1.1's v2 "distinctness" claim (candidate ≠ naive on answers) dissolves under the fair baseline, but the mechanism (deferred-designation re-resolving index) remains a legitimate first candidate under the REVISED test. No retry budget is consumed. The diagnosed cause ("deterministic functions of logged inputs are informationally recomputable") is attributed to the TEST, not the candidate or the idea.

**Fix:** Candidate 1.1's distinctness claim is DROPPED (§1.2, §1.2.4, §12.1). The candidate is NOT charged as a death (§0.6). The retry budget remains 3, spent 0. The mechanism's distinctness is now operational (property (ii): O(1)/O(log n) vs O(n)) and integrative (property (iii): load-bearing coupling), not informational. Deferred designation is RETAINED in the task design (Conway-faithful; supplies the state-dependent battery's material) but carries NO distinctness claim.

### V3-7 — Oracle-vs-naive sanity check DROPPED (APPROVED)

**Root cause:** Rebecca's ruling (§4 item 1): "APPROVED for removal — under a fair baseline it is incoherent as specified."

**Fix:** The oracle-vs-naive sanity check is DROPPED (§4.2, §12.1). Under the fair baseline, oracle and fair-naive both compute ground truth correctly from the same event log; they agree on all queries. The load-bearing checks are property (i) (candidate vs oracle, kill (f)) and property (ii) (candidate vs fair-naive cost scaling, kill (d)).

### V3-8 — Chain-break bug-vs-mechanism distinction APPROVED with guard (kill b)

**Root cause:** In v2, this was PENDING REBECCA SIGN-OFF. Rebecca's ruling (§4 item 4): "APPROVED, with guard: bug attribution requires the specific defect identified, fixed, and CRITIC-confirmed before any re-run escapes the D2 budget. 'Probably a bug' never does."

**Fix:** The construction-bug-vs-mechanism-death distinction for kill (b) is APPROVED with guard (§5(b), §12.1). A construction break (chain invalid from the start) is a BUILDER defect (fix and re-run, NOT result laundering). A re-resolution break (chain valid initially, breaks later) IS a mechanism death. The guard: the specific defect must be identified, fixed, and CRITIC-confirmed before the re-run escapes the D2 budget.

### V3-9 — No-shift distinction APPROVED with guard (kill c)

**Root cause:** In v2, this was PENDING REBECCA SIGN-OFF. Rebecca's ruling (§4 item 5): "APPROVED, same guard."

**Fix:** The wiring-defect-vs-mechanism-death distinction for kill (c) is APPROVED with guard (§5(c), §12.1). A wiring defect (re-resolution not connected to append path; all 8 shift_per_append False) is a BUILDER defect (fix and re-run). A partial mechanism failure (some shifts, some not) IS a mechanism death. Same guard as V3-8.

### V3-10 — Timebox APPROVED at 3 sessions / 7 days, clock starts at gate clearance

**Root cause:** In v2, the timebox was proposed at 3 sessions / 7 days but the clock start was ambiguous. Rebecca's ruling (§4 item 6): "APPROVED at 3 sessions / 7 days; the clock starts when the revised spec clears my gate, not before."

**Fix:** The timebox is APPROVED at 3 sessions / 7 days (§10.2, §12.1). The clock starts at gate clearance (§9 step 3), NOT before. The ARCHITECT's revision time, the CRITIC's re-review time, and Rebecca's gate time do NOT count against the M2 timebox.

### V3-11 — Constitution amendment log added (§12, NEW)

**Fix:** A new §12 documents the constitution amendment (§12.1 what changed, §12.2 why the test changed — the theorem and the program finding, §12.3 Rebecca's authority, §12.4 credit and standing note). This satisfies the requirement that the amendment be documented with rationale, authority, the theorem, and the program finding.

### V3-12 — Output schema updated for the three-property test

**Fix:** The `e1_run_results.json` schema (§7.3.1) is updated:
- `schema_version` → "3.0".
- `config.control_arms` → `["frozen_origin", "shuffled_cadence", "oracle_index", "fair_naive", "empty", "wall_clock_injection"]` (naive renamed to fair_naive).
- `config.n_state_dependent_query_points` and `config.state_dependent_history_sizes` added.
- Candidate results: `oracle_agreement` (was `equivalence_agreement_vs_naive`), `equivalence_agreement_vs_fair_naive` (diagnostic), `candidate_scaling_curve`, `candidate_slope`, `candidate_intercept`, `downstream_quality_candidate`, `downstream_quality_frozen`, `downstream_degradation` added.
- Fair-naive results: `oracle_agreement`, `equivalence_agreement_vs_candidate`, `fair_naive_scaling_curve`, `fair_naive_slope`, `fair_naive_intercept` added.
- `property_i_correctness`, `property_ii_operational_distinctness`, `property_iii_load_bearing_coupling` objects added (replacing the old `equivalence` object).
- `kill_conditions` updated: (a) moved to `retired` object with rationale; (d) updated with `scaling_collapse_ratio`; (f) marked `signed: true`.
- `e1_invariants.json` (§7.3.2) updated similarly; `e1_verdict` now "PASS | FAIL | NOT_GREEN".
- `e1_profile.json` (§7.3.5) profile vector updated for the three-property test (6 candidate metrics: oracle_agreement, latency_ratio_membership, scaling_collapse_ratio, chain_integrity_final, coordinate_shift, downstream_degradation).

### V3-13 — Scope fence updated (§8)

**Fix:** The scope fence (§8) is updated: L1 is now probed via the toy downstream consumer (property (iii)) — a test instrument, not the full L1 system. L15–L17 are now probed via the property (iii) miniature — not the full integration test (M5). The retired kill (a) and the not-green verdict are documented.

### V3-14 — L19 base-rate duty updated (§11)

**Fix:** The L19 base-rate duty (§11) is updated: the L4 graveyard classification is carried forward with the test AMENDED. The outcome base-rates (§11.2) are updated for the three-property test (kill f, kill d scaling_collapse, property (iii) failure) and the retired kill (a) base-rate is RETIRED with the kill. The D3 convergence watch (§11.3) is updated for the revised kill set.

### V3-15 — Sequencing updated (§9)

**Fix:** The sequencing (§9) is updated: the CRITIC's center of gravity is now the fair-naive definition + state-dependent battery + downstream consumer (§6.ii/iii). Step 13 is added for the not-green verdict (property (iii) failure routing). The timebox clock starts at gate clearance (step 3).

---

## v3+Q2/Q3 CHANGES (Rebecca's GO ruling incorporations — specification completions within the approved v3 structure, NOT a new revision cycle)

**Authority:** Rebecca's E1 v3 GO ruling dated 2026-08-15 (binding). Rebecca ruled GO on the v3 spec, with one replacement (Q2) and three completions (Q3), plus an unprompted NB-5 resolution and a standing NB-4 note. These are specification completions within the approved v3 structure — NOT a new revision cycle. No third full review cycle is required; the CRITIC verifies the incorporations.

**Constraints honored:** The three-property test structure is UNCHANGED (already approved). No locked bar is changed (latency ≤ 2.0, N=10, chain_integrity = 1.0, 3 seeds). The fair-naive definition is UNCHANGED (already approved). No new revision cycle is introduced. The slope ratio is RETAINED as a diagnostic, not removed — just no longer a trigger.

### Q2-1 — 0.5 slope-ratio collapse trigger REPLACED (Rebecca Q2, NOT SIGNED → replaced)

**Root cause:** NB-6 identified a real fragility: fitted slopes at toy scale sit near the timing noise floor, and a ratio with a near-zero denominator can fire on timer jitter. A kill condition must not be able to fire on jitter. Rebecca did NOT sign the 0.5 slope-ratio trigger.

**Fix:** The collapse criterion is restructured into four components (§4.1 E1-M2b, §5(d), §6.ii):
1. **Candidate side (kill (d) trigger — the locked bar, UNCHANGED in value):** the candidate's 10×-history latency growth on the state-dependent battery (`candidate_latency_growth_10x = latency(1000)/latency(100)`) must be ≤ 2.0×. This is the SAME locked bar as d1, applied to the state-dependent battery.
2. **Battery-validity requirement (NEW — NOT a candidate kill):** the fair-naive on the SAME battery must show 10×-history latency growth ≥ 4.0× (`fair_naive_latency_growth_10x ≥ 4.0`). If it does not, the battery is too easy to expose scan cost — an INSTRUMENT failure: the run is unscoreable, the battery is revised, and no kill condition or retry budget is touched.
3. **Collapse** = the candidate failing bar (1) (growth > 2.0×) on a battery validated by (2). The slope ratio is RETAINED as a reported diagnostic ONLY, never a trigger.
4. **Timing methodology (mandated):** median over repeated executions per point (minimum 100 repetitions), warm-up excluded (first 10% discarded), monotonic clock (`time.monotonic_ns()`), dispersion (IQR) reported alongside every latency figure.

**What changed in the spec:**
- §4.1 E1-M2b: metric renamed to `state_dependent_collapse`; bar redefined from `candidate_slope ≤ 0.5 × fair_naive_slope` to `candidate_latency_growth_10x ≤ 2.0` on a battery where `fair_naive_latency_growth_10x ≥ 4.0`.
- §4.2: `scaling_collapse_ratio` explicitly marked as a REPORTED diagnostic ONLY (resolves NB-1).
- §5(d): d2 trigger rewritten; battery-validity instrument-failure routing added; timing methodology mandated.
- §6.ii: collapse criterion section fully rewritten with the four components; NB-6 resolved note added; NB-1 resolved note added.
- §0.5, §0.2, §3 arm 4, §6.iv, §7.3.1, §7.3.2, §7.3.5, §7.5, §8, §9, §10.3, §11.2, §12.1, §12.2: all references updated to the new criterion.
- §7.3.5 profile vector: `scaling_collapse_ratio` replaced by `candidate_latency_growth_10x` (the actual trigger metric); perturbation definitions updated.

### Q2-2 — NB-6 resolved (timing methodology)

**Root cause:** NB-6 flagged that the collapse criterion could be unstable if the fair-naive's fitted slope is near zero (timing noise at small scales).

**Fix:** The mandated timing methodology (median, warm-up excluded, monotonic clock, dispersion reported) is specified in §5(d) and §6.ii. The collapse trigger now uses a ratio of two medians at well-separated history sizes (100 vs 1000) rather than a fitted slope, which is robust to noise. The dispersion figure lets the CRITIC verify the signal-to-noise ratio. **NB-6 is resolved.**

### Q3-1 — Downstream consumer FULLY SPECIFIED (Rebecca Q3 attachment 1; NB-3 promoted to required-before-build)

**Root cause:** NB-3 flagged that the downstream consumer's content-similarity function ("e.g., cosine similarity") and query items were underspecified. A TASK BUILDER improvising the consumer is a test the Builder authored — property (iii) must never be that.

**Fix:** The consumer is now fully specified in §6.iii (no "e.g.", no unspecified query items):
- **Feature vector:** 32-dimensional synthetic vector `v(e) = rng.standard_normal(32)`, generated deterministically per seed.
- **Similarity function:** dot product `dot(v(e), q_item)` (NOT cosine — dot product, preserving magnitude).
- **Query set:** 50 query items per seed, each a 32-d vector generated deterministically per seed (`rng_q.standard_normal(32)`). Query items are fresh synthetic vectors (NOT autobiography entries).
- **Coordinate usage:** `coord_cycle_relative(e) = now - e.cycle` only (the candidate's re-resolved offset coordinate, C1.1). Relevance: `exp(-coord_cycle_relative(e) / τ) * dot(v(e), q_item)` with τ=50, k=10.
- **Degradation measurement:** recall@k against oracle's top-k, run over candidate's re-resolved index AND frozen-origin index.
- Parameters added to §2.2 (`N_consumer_queries=50`, `consumer_feature_dim=32`, `consumer_tau=50`, `consumer_k=10`); payload description in §1.2.1 updated to mention the feature vector.

### Q3-2 — Report observed degradation magnitude (Rebecca Q3 attachment 2; "the floor is a floor, not a finding")

**Root cause:** The spec required only floor-clearance (degradation ≥ 0.05), not the observed magnitude.

**Fix:** The spec now REQUIRES reporting the observed degradation magnitude (§6.iii, §7.3.1, §7.3.2). The artifact ships per-seed degradation, quality_candidate, quality_frozen, and the mean. The JUDGE and CRITIC inspect the ACTUAL magnitude (e.g., "degradation = 0.34"), not just the boolean. "The floor is a floor, not a finding." A degradation that barely clears the floor is a weaker finding than one that clears it by a wide margin — the CRITIC notes this, and it feeds the L19 base-rate interpretation.

### Q3-3 — NB-5 resolved (unprompted completion)

**Root cause:** NB-5 flagged that the state-dependent battery doesn't explicitly address queries about deferred-designation landmarks at history size 100 (before designation).

**Fix:** Added to §6.ii: At each history size, the query battery includes only landmarks designated by that point in the run. Deferred-designation queries against not-yet-designated landmarks are ill-posed and excluded by construction. At history size 100, only the 8 immediate landmarks are in the battery (the 2 deferred enter at 250+). The pre-designation window is explicitly the shift-measurement material: entries flipping AFTER_L → BEFORE_L upon designation is the re-resolution event that kill (c)'s per-append shift artifacts capture. **NB-5 is resolved.**

### Q3-4 — NB-4 standing note (accepted for E1 scope)

**Root cause:** NB-4 flagged that the downstream consumer tests only `coord_cycle_relative` (C1.1), not `coord_landmark_relative` (C1.4 — the novel designation tracking).

**Fix:** Added a standing note to §6.iii and §8: NB-4 is accepted for E1 scope. The consumer exercises `coord_cycle_relative` only. Full landmark-relative coupling belongs to the L15 matrix at M5. The consumer uses one of the index's coordinates (valid per Rebecca's ruling §2(iii)); `coord_landmark_relative` is tested by property (i) (correctness on deferred-designation queries) and property (ii) (state-dependent battery material). A more complete consumer at M5 would use both coordinates.

### Q3-5 — Output schema updated for Q2/Q3 incorporations

**Fix:** The JSON schemas (§7.3.1, §7.3.2) are updated:
- `candidate_latency_growth_10x`, `fair_naive_latency_growth_10x`, `battery_valid`, `instrument_failure` added to candidate/fair-naive results and kill_conditions.(d).
- `candidate_latency_iqr_per_point`, `fair_naive_latency_iqr_per_point` added (timing methodology dispersion).
- `scaling_collapse_ratio` retained but marked as diagnostic (`scaling_collapse_note`, `scaling_collapse_ratio_diagnostic`).
- `downstream_degradation_magnitude_note`, `consumer_spec` added to property_iii.
- `timing_methodology` field added to property_ii.
- Config: `n_consumer_queries`, `consumer_feature_dim`, `consumer_tau`, `consumer_k`, `timing_repetitions`, `timing_methodology` added.
- §7.3.5 profile vector: `scaling_collapse_ratio` → `candidate_latency_growth_10x`; perturbation definitions updated.
- Manifest purpose/bars strings updated.

### Q3-6 — Amendment log and scope fence updated

**Fix:** §12.1 amendment log rows for kill (d) and property (iii) updated with Q2/Q3 incorporations. §12.2 property (ii) description updated. §12.3 authority extended with specification-completion authority. §8 scope fence updated with Q2 restructure, Q3 completions, NB-4/5/6 resolutions. §9 sequencing step 2 (CRITIC center of gravity) updated. §10.3 delivery criteria updated. §11.2 base-rates updated. Spec header updated.

---

## v2 CHANGES (CRITIC-review revision — retained in v3 where not retired)

### Summary of v2

The CRITIC identified that the original spec's equivalence test (§6) and latency test (§4) were **unsatisfiable by construction** — a correct candidate would always trigger kill (a) (collapse) and kill (d) (scanning), making the test a foregone conclusion rather than a falsification. The root cause (B1/B5) was that the candidate's `coord_landmark_relative` was defined as the *same computation* naive recomputation performs (`e.cycle < L.cycle` == `e.created_at < L.created_at` because `created_at == cycle`).

The v2 revision introduced **landmark designation as a deferred event** (a separate `designate_landmark()` operation, recorded in the append-only history, distinct from append). The candidate's `coord_landmark_relative` was redefined relative to `L.designated_at` (the designation event), NOT `L.cycle` (the append event). A `created_at` column cannot recover designation timing (designation is not an append), so the candidate carried information naive did not — making the candidate **distinguishable from naive while remaining correct** (matching the oracle). The "coherent" state was reachable.

The locked numeric bars (§0.2) were carried forward **UNCHANGED** — no bar flipped, softened, raised, lowered, renamed, or redefined.

> **v3 note:** The v2 "distinguishable from naive" claim is DISSOLVED in v3 by Rebecca's theorem (fair-naive ≡ oracle on answers). The v2 mechanism (deferred designation) is RETAINED in v3 (Conway-faithful; supplies the state-dependent battery's material) but carries NO distinctness claim. The v2 fixes that are NOT about the distinctness claim (B2 latency isolation, B3 shuffled-cadence, B4 broken-state routing, N1–N12 non-blocking) are RETAINED in v3.

### v2 BLOCKING Issues (5 fixed in v2; status in v3)

### B1 — Equivalence test unsatisfiable → FIXED in v2 (existence proof) → DISSOLVED in v3 (Rebecca's theorem)

**v2 fix:** Landmark designation as a deferred event; `coord_landmark_relative` relative to `L.designated_at`; naive uses `L.created_at`. Existence proof (§6.5): candidate matches oracle AND differs from naive on deferred-designation landmarks.

**v3 status:** DISSOLVED. Rebecca's theorem proves the v2 existence proof held only against a handicapped naive. The fair naive reads designation events and agrees with the candidate at 1.0. The equivalence test is RETIRED (V3-1). The three-property test replaces it.

### B2 — Latency test unsatisfiable (answer-set size grows ~10×) → FIXED in v2 (RETAINED in v3)

**v2 fix:** The latency bar (E1-M2) is measured on bounded-output queries (membership + bounded-k). Raw materialization sizes reported separately, not barred.

**v3 status:** RETAINED (§4.1 E1-M2, §6.ii). The bounded-output latency bar is the d1 trigger for kill (d) (PROMOTED to property (ii) discriminator). The B2 fix is the foundation for the state-dependent battery (d2).

### B3 — Shuffled-cadence arm ambiguous "OR" → FIXED in v2 (RETAINED in v3)

**v2 fix:** The "OR" is removed. Exactly one implementation: broken chain (`chain_integrity = False`).

**v3 status:** RETAINED (§3 arm 2).

### B4 — "Broken" state has no defined verdict → FIXED in v2 (kill f, PENDING) → SIGNED in v3

**v2 fix:** Kill condition (f) added: `oracle_agreement < 1.0` → candidate is "broken." Marked [PENDING REBECCA SIGN-OFF].

**v3 status:** SIGNED and PROMOTED (V3-2). Kill (f) is the primary correctness kill condition (property (i)). No longer PENDING.

### B5 — Candidate violates L4 by construction → FIXED in v2 (same as B1) → DISSOLVED in v3

**v2 fix:** Same as B1. The candidate's `coord_landmark_relative` depends on `L.designated_at`, which a `created_at` column cannot recover. L4 satisfied.

**v3 status:** DISSOLVED (same as B1). The L4 test is AMENDED (§0.1). The candidate's L4 compliance is now demonstrated by the three-property test (operational + integrative), not by the informational non-collapse claim.

### v2 NON-BLOCKING Issues (12 fixed in v2; status in v3)

| # | v2 Issue | v2 Fix | v3 Status |
|---|---|---|---|
| N1 | Wall-clock-injection arm vacuous | Acknowledged as defensive check | RETAINED (§3 arm 6, §5e). Construction-bug guard added (V3-8/9). |
| N2 | Oracle-vs-naive sanity check vacuous | DROPPED | RETAINED (§4.2). APPROVED by Rebecca (V3-7). |
| N3 | Frozen-origin expected-result reasoning incorrect | Fixed | RETAINED (§3 arm 1). Extended: frozen-origin is now the ablation arm for property (iii). |
| N4 | I3 null distribution ambiguously specified | Fixed (self-consistency null) | RETAINED (§0.9, §7.3.2). |
| N5 | L20 perturbation descriptions underspecified | Fixed (exact transformations) | RETAINED (§7.3.5). Profile vector updated for v3 (V3-12). |
| N6 | No reproducibility check | Added (I1-equivalent) | RETAINED (§7.3.1, §10.3h). |
| N7 | Missing `permuted` arm from L18 | Acknowledged as gap | RETAINED (§0.4). |
| N8 | Profile vector includes control arm metric | Fixed (dropped frozen_oracle_agreement) | RETAINED (§7.3.5). Profile vector updated for v3 (V3-12). |
| N9 | `arms` config includes candidate as 7th entry | Fixed | RETAINED (§7.3.1). |
| N10 | D2 distinctness table conflates C1.3a/C1.3b | Fixed (split) | RETAINED (§1.2.3). |
| N11 | No intermediate chain_integrity checks | Added | RETAINED (§5b, §7.3.1). |
| N12 | No intermediate shift measurements | Added | RETAINED (§5c, §7.3.1). |

### v2 PENDING REBECCA Items (4; status in v3)

| # | v2 Item | v2 Disposition | v3 Status |
|---|---|---|---|
| 1 | Oracle-vs-naive sanity check | DROP | APPROVED (V3-7). DROPPED. |
| 2 | Kill (f): `oracle_agreement < 1.0` | ADD [PENDING] | SIGNED and PROMOTED (V3-2). No longer PENDING. |
| 3 | Chain-break bug-vs-mechanism (kill b) | ACCEPT with N11 [PENDING] | APPROVED with guard (V3-8). |
| 4 | Wiring-defect-vs-mechanism (kill c) | ACCEPT with N12 [PENDING] | APPROVED with guard (V3-9). |

### v2 D2 Provenance (Acceptance Criterion 5)

The v2 candidate mechanism was materially revised from the original C1.1/C1.2/C1.3 design. The revised candidate was labeled Candidate 1.1 (a revised draft of Candidate 1), with a distinctness note in §1.2.4. This was NOT a D2 retry — it was a pre-build revision of the same candidate slot (no scoring run had occurred). The retry budget remained 3, spent 0.

**v3 status:** RETAINED (§1.2.4). Candidate 1.1 remains a revised draft of Candidate 1. The v2 distinctness claim (candidate ≠ naive on answers) is DROPPED (V3-6). The retry budget remains 3, spent 0. Candidate 1.1 is NOT charged as a death (Rebecca ruling §3).

### v2 Acceptance Criteria Verification (status in v3)

1. **Existence proof (§6.5):** v2 ✓ (candidate matches oracle AND differs from naive). **v3: DISSOLVED** — the existence proof held only against a handicapped naive. The three-property test (§6) replaces it. Property (i) correctness is satisfiable (candidate matches oracle). Property (ii) operational distinctness is satisfiable (candidate O(1)/O(log n); fair-naive O(n)). Property (iii) load-bearing coupling is satisfiable (downstream consumer degrades under ablation).
2. **No bar laundering (§0.2):** v2 ✓ (all bars carried forward verbatim). **v3: ✓** — the ≤ 2.0 latency bar, N = 10, = 1.0 chain-integrity, 3-seed policy carried forward verbatim. The retired ≤ 0.90 equivalence bar is RETIRED (not softened — unsatisfiable by construction). The = 1.0 oracle-agreement bar is PROMOTED (not invented — Rebecca signed it). The naive arm is STRENGTHENED (not softened — fair naive reads the full event log).
3. **Latency isolation (§4, §4.2):** v2 ✓ (bounded-output queries). **v3: RETAINED** (§4.1, §6.ii). Extended with the state-dependent battery.
4. **B3/B4 fixes (§3 arm 2, §5f):** v2 ✓. **v3: RETAINED** (B3) and SIGNED (B4/kill f, V3-2).
5. **D2 provenance (§1.2.4):** v2 ✓. **v3: RETAINED** with distinctness claim DROPPED (V3-6).

---

## v3+OPTION E AMENDMENT (Rebecca's Property (iii) Ruling — Option D REJECTED; Option E Ordered)

**Date:** 2026-08-15 · **Author:** ARCHITECT · **Authority:** Rebecca's binding Property (iii) ruling (Option E), dated 2026-08-15.
**Trigger:** Property (iii) failed with `downstream_degradation = 0.0` on all 3 seeds (CRITIC-verified spec design flaw). The prior frozen-origin specification produced two degenerate ablations: Option D (excluding entries 100–999 → degradation = 1.0 by construction, a ceiling corner) and the §6.iii consumer spec (frozen `coord_cycle_relative = 99 − e.cycle` for all entries → degradation = 0.0 by construction, a floor corner — the frozen relevance was a constant multiple `exp(18)` of the oracle relevance, so rankings were identical). Both are constants by construction; neither measures anything.
**Scope:** Targeted amendment — ONLY §3 Arm 1, §6.iii, and directly dependent text in §7 (output schema) and §9 (CRITIC verification) revised. Properties (i) and (ii) UNCHANGED. Fair-naive definition UNCHANGED. Locked bars UNCHANGED. Three-property test structure UNCHANGED. No new revision cycle.

### OE-1 — Frozen-arm specification reconciled to Option E (§3 Arm 1 + §6.iii)

**Root cause:** The spec contained two mutually inconsistent descriptions of the frozen-origin arm: the Arm 1 description (Option D — frozen index excludes entries 100–999) and the §6.iii consumer spec (frozen `coord_cycle_relative = 99 − e.cycle` for all entries). The §6.iii version was followed by the TASK BUILDER and produced degradation = 0.0 (the frozen relevance was a constant multiple of the oracle relevance, so argsort rankings were identical). Option D was Rebecca-rejected as a ceiling corner.

**Fix (Option E — Rebecca's binding specification):**
1. The frozen arm retains ALL entries and ALL content, identical to the candidate's autobiography (all 1000 entries).
2. Each entry's coordinates are computed ONCE, at its own append (`coord_cycle_relative = 0` at birth; landmark-relative per the registry state at that moment), and NEVER re-resolved thereafter. Re-resolution is disabled; nothing else is.
3. The consumer is identical across arms. The only difference between candidate and frozen is whether coordinates moved after birth.
4. Consequence: under E, every entry carries a permanently stale "just appended" coordinate — the recency gradient is destroyed while memory remains complete. Content intact, temporal self-location gone.

**What changed in the spec:**
- §3 Arm 1 (line 298): entire row replaced with Option E description. Removed "frozen index doesn't include entries 100–999" (Option D — REJECTED). Removed "coord_cycle_relative frozen at now=99 values" (the version that produced degradation=0). Added: all entries retained, coordinates computed once at birth, never re-resolved, consumer identical across arms.
- §6.iii (lines 535–596): frozen-origin ablation description replaced with Option E. `coord_cycle_relative(e) = 0` for ALL entries (not `99 − e.cycle`). Recency weight collapses to `exp(0) = 1.0` for all entries. The "Why this is satisfiable" section, "The ablation" section, and "Why this consumes coordinates" section all updated.

### OE-2 — Recency-discriminative query battery added (§6.iii)

**Root cause:** Under Option E, the frozen arm's recency weight is `1.0` for all entries, so the frozen ranking is purely by content (dot product). A battery of content-unique queries would read degradation ≈ 0 — content similarity alone determines the ranking, so the frozen arm matches the oracle regardless of whether re-resolution works. Coupling is only measurable on a task where the coordinate carries information.

**Fix (Rebecca's companion requirement):** the consumer's query set now includes a pre-registered fraction of near-duplicate-content queries at different ages, where content similarity alone ties or near-ties and the coordinate breaks the tie.

- **Fraction chosen by the ARCHITECT: 40% (20 of 50 queries).** Pre-registered.
- **Near-duplicate generation:** 20 pairs of entries (40 of 1000) have near-identical feature vectors (`v(e_new) = v(e_old) + σ_nd · noise`, `σ_nd = 0.05`) but very different cycles (one at cycle `p ∈ [0,19]`, one at cycle `900+p ∈ [900,919]`). Each recency-discriminative query aligns with its pair's shared feature direction (`q = v_base + σ_q · noise`, `σ_q = 0.05`), creating a content tie while the ages differ enormously.
- **How the coordinate breaks the tie:** the candidate/oracle's re-resolved `coord_cycle_relative = 999 − e.cycle` gives a recency weight that favors the recent pair member by a factor of ~10⁷–10⁸ → oracle ranks the recent entry. The frozen arm's `coord_cycle_relative = 0` for all entries gives recency weight `1.0` for both → the frozen arm ranks purely by content (near-tied) → cannot distinguish recent from old by recency → picks the wrong entry → recall@k degrades.
- **Content-unique queries (60%):** independent random query vectors; content similarity alone determines the ranking → frozen arm matches oracle → degradation ≈ 0 on these.
- **Why degradation < 1.0 is reachable:** bounded by the recency-discriminative fraction (`degradation ≤ 0.4 < 1.0`) since content-only ranking succeeds on content-unique queries.
- **Why the 0.05 floor is clearable:** on recency-discriminative queries, per-query degradation ≈ 0.3–0.5 → aggregate ≈ 0.12–0.20, comfortably above 0.05.

**What changed in the spec:**
- §6.iii feature vector spec: 20 near-duplicate pairs added (deterministic generation, `σ_nd = 0.05`).
- §6.iii query set spec: split into 20 recency-discriminative (40%) + 30 content-unique (60%).
- §6.iii new subsection: "The recency-discriminative query battery" — full specification of near-duplicate generation, fraction, tie-breaking, and the two CRITIC verifications ((a) degradation < 1.0 reachable, (b) 0.05 floor clearable).
- §7.3.1 config: `n_recency_discriminative_queries`, `recency_discriminative_fraction`, `n_near_duplicate_pairs`, `near_duplicate_sigma`, `recency_discriminative_query_sigma` added.
- §7.3.1 property_iii: `consumer_spec` string updated.
- §7.3.1 notes: Property (iii) downstream consumer note updated for Option E + recency-discriminative battery.
- §9 step 2: CRITIC verification list extended with recency-discriminative battery checks.

### OE-3 — Rebecca's verbatim lesson logged (§6.iii)

**Fix:** Rebecca's verbatim lesson is added to §6.iii: *"An ablation whose result is a constant by construction measures nothing. A valid ablation removes exactly the organization under test and preserves everything else, and its expected result must be a task-dependent quantity in the open interval — never a corner."* The lesson is contextualized: Option D produced degradation = 1.0 (ceiling corner); the prior §6.iii spec produced degradation = 0.0 (floor corner); Option E removes exactly re-resolution and preserves everything else, with an expected result in the open interval (0, 1).

---

## Files

- `/home/user/workspace/e1_spec.md` — the revised spec (v3 + Q2/Q3 + Option E amendment)
- `/home/user/workspace/e1_spec_CHANGES.md` — this changelog (v1 → v2 → v3 → v3+Q2/Q3 → v3+Option E)
- `/home/user/workspace/existence_proof_analysis.md` — working notes on the v2 existence proof (now dissolved by Rebecca's theorem)
- `/home/user/workspace/verify_existence_proof.py` — simulation verifying the v2 existence proof (3-entry toy; the v2 proof held only against the handicapped naive)
- `/home/user/workspace/verify_existence_proof_v2.py` — simulation verifying the v2 existence proof (full 200-query, 3-seed scenario; the v2 proof held only against the handicapped naive)
- `/home/user/workspace/uploaded_attachments/1d28d250041d41c6bd424d3d33df500f/REBECCA_E1_GATE_RULING.md` — Rebecca's binding E1 gate ruling (the authority for v3)
- `/home/user/workspace/uploaded_attachments/7b9d3c33e58d485f8a8c8bd5957fc915/REBECCA_E1_V3_GO.md` — Rebecca's binding E1 v3 GO ruling (the authority for Q2/Q3 incorporations)
- `/home/user/workspace/critic_e1_spec_rereview_v3.md` — the CRITIC's re-review (v3) with NB-1 through NB-6 (the non-blocking items resolved by Q2/Q3)

---

## v3+Option E FIX (ARCHITECT, post-CRITIC-BLOCKING — consumer parameterization fix, 2026-08-15)

**Trigger:** CRITIC review of the Option E amendment (`critic_e1_option_e_review.md`) found ONE BLOCKING ISSUE: Verification (a) FAILS. The spec's central claim — that content-only ranking succeeds on content-unique (CU) queries, bounding degradation by the recency-discriminative fraction (≤ 0.4) — is mathematically FALSE. Direct simulation of the spec's exact formulas (seeds 42/43/44, script `verify_option_e.py`) shows CU degradation ≈ 0.927 (spec claims ≈ 0) and aggregate degradation ≈ 0.887 (spec claims 0.12–0.20) — close to the 1.0 ceiling corner Rebecca warned against. The test would technically PASS (> 0.05 floor) but for the WRONG reason (the frozen arm fails on CU queries too, not just RD).

**Root cause:** the consumer's relevance function was MULTIPLICATIVE: `relevance(e,q) = exp(-coord_cycle_relative(e)/τ) · dot(v(e), q)` with τ=50 and now=999. The recency weight `exp(-(999-e.cycle)/50)` spans ~9 orders of magnitude (`exp(-999/50) ≈ 2×10⁻⁹` to `1.0`), while the content signal (dot product of 32-d random Gaussian vectors) has a dynamic range of ~1 order of magnitude (top-2:top-10 content ratio ≈ 1.06). The recency weight overwhelms the content signal on EVERY query, not just recency-discriminative ones — the oracle is recency-dominated everywhere, the frozen arm (content-only) fails on CU queries. A τ sweep (τ=50→1000, `verify_option_e_tau_sweep.py`) confirmed the problem is STRUCTURAL: no value of τ makes CU degradation ≈ 0 with random Gaussian features, because the content signal among ranks 2-10 of the top-k is intrinsically too flat for any recency gradient to not overturn.

**The frozen-arm spec (Option E, §3 Arm 1) is CORRECT and UNCHANGED.** The fix is ENTIRELY within the consumer's query/feature parameterization (§6.iii). Rebecca's binding Option E ruling is honored: all entries retained, coordinates computed once at birth (`coord_cycle_relative = 0`), never re-resolved, consumer identical across arms. The locked bars (latency ≤ 2.0, N=10, chain_integrity = 1.0, 3-seed policy, 0.05 floor) and `consumer_tau = 50` (pinned per Q3-1) are ALL UNCHANGED. Properties (i) and (ii) are out of scope.

### FIX-1 — Relevance function: MULTIPLICATIVE → ADDITIVE (§6.iii)

**Fix:** the relevance function changes from `exp(-coord/τ) · dot` to ADDITIVE:
```
relevance(e, q) = dot(v(e), q)  +  λ · exp(-coord_cycle_relative(e) / τ)
```
with `λ = 16.0` (the recency-coupling constant; the additive recency bonus is bounded in `[0, λ]`, ~16% of the content signal `A²=100`), `τ = 50` (UNCHANGED). **Why:** the multiplicative product couples the recency weight's 9-orders-of-magnitude dynamic range to the content signal's magnitude, so recency overwhelms content on every query. The additive form DECOUPLES content from recency: the recency contribution is a bounded bonus `λ·w(e) ∈ [0, λ]` added to the content score, so a large content gap cannot be overturned by recency, while a content TIE is still broken by the recency bonus. This realizes the spec's intended separation (CU → content dominates; RD → recency breaks tie) that the multiplicative form could not. **The frozen arm is unchanged in substance:** under Option E `coord_cycle_relative = 0` for all → `w(e) = exp(0) = 1.0` for all → the recency bonus collapses to the constant `λ` added to every entry (does not affect ranking) → the frozen arm ranks purely by content, exactly as Option E intends (content intact, temporal self-location gone).

### FIX-2 — Feature vectors: random Gaussian → BUCKETED SPIKE content (§6.iii)

**Fix:** the 1000 entries are partitioned into 50 **content buckets** (30 CU buckets of size exactly `k=10`, 20 RD buckets of size `K_rd=30 > k`, 100 fillers). Each bucket `b` gets a seeded random unit direction `u_b ∈ ℝ³²` (random directions in d=32 are near-orthogonal, so buckets are content-separable without one reserved dimension per bucket). Entry `e` in bucket `b` has `v(e) = A·u_b + σ_f·noise` (`A=10`, `σ_f=0.10`); a query targeting bucket `b` is `q = A·u_b + σ_q·noise` (`σ_q=0.10`). This yields a large, clean content gap: `dot(v(e_b), q_b) ≈ A²=100` for bucket members vs `≈ O(1.8)` for other buckets — a ~50× gap the bounded additive recency bonus (`λ ≤ 16`) cannot overturn. **Why:** random Gaussian features give a flat content signal (ranks 2-10 ratio ≈ 1.06) that ANY recency gradient overturns — the CRITIC showed this is structural at every τ. The bucketed spike creates clean content CLUSTERS so that on CU queries content determines the top-k SET (the bucket IS the top-k; recency only reorders within the set, preserving recall@k), while on RD queries content TIES the `K_rd` members and recency must SELECT which `k` to retrieve. Bucket members' cycles are SPREAD across 0..999 (seeded round-robin permutation) so recency differs within every bucket.

### FIX-3 — Query battery: near-duplicate PAIRS → content BUCKETS (§6.iii)

**Fix:** the 20 RD queries each target an RD content bucket of size `K_rd=30 > k` (content ties 30 entries; recency selects the k=10 most-recent). The 30 CU queries each target a CU content bucket of size exactly `k=10` (content determines the top-k SET; recency cannot change it). The 40% RD fraction is UNCHANGED. **Why:** with buckets of size exactly `k`, recall@k is set-preserved on CU (degradation 0) regardless of recency strength; with buckets of size `K_rd > k`, the oracle's recency-selected k and the frozen's content-noise-driven k differ (degradation > 0). This is the clean separation the prior near-duplicate-pair design could not achieve because the pair (2 members) never occupied enough of the top-k to matter against the recency-crushed ranks 2-10.

### FIX-4 — Simulation added (§6.iii "SIMULATED VERIFICATION")

**Fix:** the spec now includes a simulation-results table (script `verify_option_e_fix.py`, seeds 42/43/44) showing: CU degradation 0.000, RD degradation 0.255, aggregate 0.102 (per-seed 0.092–0.120, all > 0.05 floor), with a mechanism check (oracle retrieves the recency-selected recent subset; frozen retrieves the content-noise subset; they differ on RD, match on CU). The spec states this is NOT a corner (0.102 is ~2× the floor, ~4.9× below the ceiling, task-dependent, varies by seed). The CRITIC is directed to re-verify with its own simulation.

**Config (§7.3.1) changes:** added `consumer_relevance_form`, `consumer_recency_coupling_lambda`, `consumer_content_signal_amplitude`, `consumer_feature_noise_sigma`, `consumer_query_noise_sigma`, `n_rd_content_buckets`, `rd_content_bucket_size`, `n_content_unique_queries`, `n_cu_content_buckets`, `cu_content_bucket_size`, `n_content_buckets_total`; removed `n_near_duplicate_pairs`; `near_duplicate_sigma` and `recency_discriminative_query_sigma` updated to 0.10. `consumer_tau=50` UNCHANGED.

**What is NOT changed:** the frozen-arm spec (§3 Arm 1, Option E) — coord computed once at birth, never re-resolved; all locked bars (latency, N, chain_integrity, 3-seed, 0.05 floor); `consumer_tau=50`; `consumer_feature_dim=32`; `consumer_k=10`; `N_consumer_queries=50`; the 40% RD fraction; properties (i)/(ii); Rebecca's verbatim lesson.

**Files:**
- `/home/user/workspace/e1_spec.md` — revised (§6.iii, §2.2, §7.3.1 config + consumer_spec strings)
- `/home/user/workspace/e1_spec_CHANGES.md` — this changelog (appended FIX-1..4)
- `/home/user/workspace/verify_option_e_fix.py` — the ARCHITECT's simulation script (bucketed + additive; sweeps + final config + mechanism check + results JSON)
- `/home/user/workspace/verify_option_e_fix_results.json` — saved simulation results
