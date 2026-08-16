CRITIC Review — ARCHITECT V4.3 L1 Shuffled-Arm Amendment
Commit: 5ba97f6cbee7bf4c85e01368d979a11dfa220879
Base: 8e9f83a6f7fac8dd6682a446c2730ed14752cc8c (Rebecca's ruling)
Scope: §2.9/§2.11 L1 shuffled-arm calibration only
Verdict: CLEARED — V4.3 targeted spec amendment
This is CLEAR for the amendment as a specification document. It is NOT clearance for fresh scoring. Scoring remains BLOCKED pending implementation, §2.10 harmonization, full 26-family closure audit, and Rebecca's fresh-seed supervised scoring authorization.
Four-part test compliance
PartRequirementAmendment evidenceVerdict
(a)
Defect demonstrable from spec alone, without observed values
§4: 1 − 0.95¹⁵ = 0.5367 is arithmetic on the pre-registered two-sided rule. No observed value referenced.
✅
(b)
Change cannot benefit candidate; corrected control equally or more sensitive in meaningful direction
§0: "No value from that run sets or tunes the corrected threshold." Candidate passed all bars; failures were below-band on a destroy-the-signal control. Upper-only null-of-the-max is more sensitive in the meaningful direction (excess positive association).
✅
(c)
Failed run retained; correction logged as post-scoring
§0: "The seeds 201–203 result remains retained under its original INSTRUMENT FAILURE label." §5: "Fresh scoring instrument failure: retain the fresh result under its original label."
✅
(d)
Fresh seeds, never re-run
§0: "Any later scoring is a new full M3 battery on three fresh seeds from the authorized scoring pool, through Rebecca's supervised executor; it is not a re-run." §5: "O-14 forbids re-running it."
✅
All four parts satisfied. The correction is authorized under Rebecca's standing law, not excepted from it.
Null-of-the-max multiplicity control — verified
ElementSpec valueVerification
Null replicates per seed
R = 1000
✅ Fixed, pre-registered
Bins per seed
5
✅
Max statistic
M[s,r] = max_b rho_null[s,r,b]
✅ Row maximum of 5 bin ρ values
Threshold
T_s = M_sorted[985] (1-indexed, no interpolation)
✅ 15 null maxima strictly above → 16/1001 tail bound
Plus-one p-value
p_s = (1 + #{M[s,r] ≥ M_obs}) / 1001
✅ Tie-conservative; binding over threshold shorthand
Per-seed alpha
0.05/3 (Bonferroni)
✅
Per-seed tail bound
16/1001 = 0.015984
✅ < 0.05/3 = 0.01667
Familywise bound
48/1001 = 0.047952
✅ < 0.05, no independence assumption (Boole's inequality)
Order statistic derivation
985 = 1000 − 15
✅ Tightest index satisfying the constraint
Arithmetic closure confirmed by independent execution of verify_m3_l1_shuffled_fwfp.py:
old_two_sided_fwfp=0.5367087698
one_sided_only_fwfp=0.3159793144
per_seed_tail_bound=16/1001=0.0159840160
familywise_union_bound=48/1001=0.0479520480
bar=1/20=0.0500000000
verdict=PASS
Directionality fix — verified
§1: "The only meaningful failure direction is excess positive residual rehearsal association" ✅
§1: "A value at or below the bound, including a value below the old lower band, means destruction was at least as strong as the null expectation and is never a failure." ✅
§2: "A shuffled rho at or below its calibrated upper threshold — including a value below the former lower band — is informational (shuffle exceeded typical destruction) and never enters PASS, KILL, or INSTRUMENT FAILURE." ✅
Artifact field: below_threshold_label: "shuffle exceeded typical destruction — informational" ✅
§2.11 replacement — verified
The amendment replaces exactly the shuffled clause ("OR any shuffled conditional rho falls outside its empirical-null band") with the new null-of-the-max trigger. All other INSTRUMENT FAILURE triggers (frozen, fair-naive, permuted, recency-only, rehearsal-only, empty) remain unchanged. PASS branch gains the shuffled null-of-the-max requirement. No candidate-facing KILL predicate is changed. ✅
Systemic closure audit (§3) — verified
The 26-family inventory (L1: 8 arms, L3: 5, L5: 7, L6: 6) with directionality justification and FWFP computation for every control arm is the correct implementation of Rebecca's §4 systemic fix. The JSON schema is well-formed. The L1.shuffled row is frozen exactly; the other 25 rows inherit unchanged checks and must be populated by the closure auditor. ✅
No-change audit — verified
Changelog confirms: no production code changed, no scoring run conducted, no seed named or exposed, no candidate-facing bar lowered/raised/renamed/reinterpreted, no L3/L5/L6/L9/L15-L18/L20/D1-D5/O-14/O-15 rule changed. ✅
Non-blocking findings (must be addressed before implementation/scoring)
NB1 — §2.10 checklist row inconsistent. The §2.10 summary table still reads "All 5 conditional ρ within shuffled-empirical-null band" for the shuffled arm. The binding conditions in §2.9/§2.11 now use null-of-the-max. This is a non-binding summary row, not a gating condition, but it must be harmonized or explicitly superseded before the consolidated spec is handed to implementation. Blocks integration clarity, not amendment clearance.
NB2 — Closure audit has two phases. Pre-scoring can verify family inventory completeness, directionality justifications, order statistic index, FWFP arithmetic, schema, and RNG derivation rules without exposing fresh seeds. Recomputing actual p_s from M_obs requires scoring output and belongs to JUDGE verification, unless performed wholly inside Rebecca's supervised executor. The amendment's §3 language partially mixes these phases. Binding clarification: the pre-scoring closure audit verifies the framework; per-seed p_s recomputation is scoring-output verification.
NB3 — Other arms may exceed 5% FWFP in closure audit. The frozen and fair-naive arms use a 95th-percentile bound with 3 seeds: FWFP = 1 − 0.95³ = 14.3%. The permuted arm (V4.2) uses a two-sided band with 3 seeds: FWFP = 1 − 0.95³ = 14.3%. The recency-only arm has 7 checks per seed (R², β_age, 5 ρ) × 3 seeds = 21 checks. The closure audit (§3 item 5) will flag these and block scoring until corrected. This is the systemic fix working as intended — but it means additional targeted amendments may be needed before fresh scoring can proceed. Not a defect in this amendment; flagging for sequencing awareness.
NB4 — Per-seed null generation is a new implementation requirement. The existing harness generates the shuffled null from the structural seed (shared across scoring seeds). The V4.3 amendment requires per-seed nulls with domain-separated RNG derived from the scoring seed and replicate index, with no reuse of the observed shuffled-assignment draw. The implementation must prove exchangeability: the observed shuffled assignment and the null replicates are draws from the same reassignment distribution, differing only in RNG seed. Implementation requirement for TASK BUILDER, not a spec defect.
NB5 — Null-replicate RNG derivation must be documented. The amendment requires "a documented domain-separated hash" but does not specify the hash function. The implementation must name the hash, the domain separator, and the seed-composition formula, and this must be verified by the closure audit. Implementation detail, not a spec gap.
Preserved evidence (unchanged)
Seeds 201–203 INSTRUMENT FAILURE label retained ✅
L3/L5/L6 PASS on all 3 seeds — valid scored evidence ✅
L1 candidate bars (R²=0.9857, β_age=−0.00150, all ρ≥0.6) — valid on all 3 seeds ✅
No kill conditions fire on any seed ✅
Reproducibility (bit_identical=True), L20 drift self-test, interface invariants — all PASS ✅
Summary
The V4.3 amendment faithfully implements Rebecca's ruling: one-sided upper bound (below-band = informational, never failure) AND null-of-the-max multiplicity control (exact 48/1001 = 0.04795 < 0.05 familywise, no independence assumption). All four parts of the post-scoring correction test are satisfied. No candidate-facing bar moves. O-14 is preserved. The systemic closure-audit requirement is correctly specified.
CLEARED as V4.3 targeted spec amendment. Scoring remains BLOCKED pending: (1) implementation of the per-seed null-of-the-max procedure, (2) §2.10 harmonization, (3) full 26-family closure audit with all arms at FWFP ≤ 5%, (4) Rebecca's fresh-seed supervised scoring authorization. The NB findings above are implementation and sequencing items, not amendment defects.
