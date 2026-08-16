# M3/E2 Consolidated Specification V4.4 — Systemic Pre-Scoring Closure

**Status:** DRAFT FOR INDEPENDENT CRITIC REVIEW — no implementation or scoring authorization

**Date:** 2026-08-16

**Author:** ARCHITECT

**Gate served:** M3 V4.3 Systemic Pre-Scoring Closure Gate under Rebecca Entry 43

**Named base:** `8259e01a1dfac6a09074027d9a48f034bf51d9b9`

**CRITIC B1–B4 revision base:** `b6accaad3773468d54b2363a1072877554186265`

## 0. Consolidation, precedence, and no-change boundary

V4.4 consolidates the CRITIC-cleared V4 base, the governing V4.1 L3 correction, the governing V4.2 L1-permuted correction, the CRITIC-cleared V4.3 L1-shuffled amendment, and the systemic closure corrections required by Rebecca Entry 43 and CRITIC NB1–NB5. Where this document supplies replacement text, it supersedes the earlier layer. Every other V4/V4.1/V4.2/V4.3 fixture, candidate equation, candidate-facing bar, control transform, metric, verdict, artifact, law, and fence remains unchanged.

This document changes no production code and authorizes none. It uses no returned or fresh scoring statistic. Seeds 201–203 and their first-run `INSTRUMENT FAILURE` verdict remain retained; they may never be rerun. L1 candidate evidence and L3/L5/L6 PASS evidence remain preserved without reinterpretation. O-14, O-15, D1–D5, L9, full L18 treatment, the L15 integration fence, unseen-seed protection, and supervised execution remain binding. Any future run must use three fresh, unnamed authorized seeds after implementation clearance and Rebecca's separate authorization.

## 1. Systemic error-control rule

The unit of audit is one control arm's complete simultaneous check family across all bins/horizons/query subchecks and all three scoring seeds. Every family must be exactly one of:

1. `stochastic_empirical`: a calibrated randomization family with binding plus-one p-values and full-family FWFP at most 0.05; or
2. `deterministic`: an exact finite, algebraic, combinatorial, paired, interface, schema, or fixed-fixture predicate that is not a level-alpha hypothesis test. For such a family stochastic FWFP is inapplicable, its audit value is 0, and the artifact must prove why the predicate is exact.

Calling a stochastic outcome “expected,” “exact,” or “very likely” does not make it deterministic. An unproved stochastic bound has conservative pre-closure FWFP 1 and blocks scoring until calibrated. Multiplying deterministic report slots across seeds does not create statistical comparisons when the scoring seed does not enter the construction.

For every stochastic family, `R=1000`, `alpha_family=0.05`, and `alpha_seed=0.05/3`. The binding seed-level p-value is

`p_s = (1 + sum_r I[S_null(s,r) >= S_obs(s)]) / 1001`.

Ties count against the control. A seed passes iff `p_s > 0.05/3`; all three seeds must pass. At this discrete alpha, rejection occupies at most 16 of 1001 exchangeable ranks per seed, hence

`FWFP <= 3*(16/1001) = 48/1001 = 0.047952047952... < 0.05`

without an independence assumption. Sorted null order statistic 985 (one-indexed, no interpolation) may be reported as shorthand, but the p-value is binding.

## 2. L1 access physics — consolidated control text

### 2.9 Exact expected statistic, multiplicity control, and artifacts

The unchanged frozen, fair-naive, recency-only, rehearsal-only, permuted, shuffled, oracle, and empty transforms from V4/V4.2/V4.3 remain the eight L1 control families. Their binding closure treatment is:

| Arm | Binding family rule | Meaningful failure direction | Required scoring artifact |
|---|---|---|---|
| Frozen | Per seed, compare observed `R²` with 1000 exchangeable constant-priority/tie-break null `R²` values using the upper-tail plus-one p-value and `alpha_seed=0.05/3`. | Upper only: large `R²` leaks age; low values are stronger destruction. | Observed `R²`, 1000 null values, order statistic 985, exceed/tie count, p-value, RNG records. |
| Fair-naive | Same calibrated upper-tail rule, using exchangeable unrelated identifier permutations. | Upper only: large `R²` leaks age; low values are stronger destruction. | Same fields as frozen. |
| Recency-only | Exact fixed-fixture checks: `R²>=0.85`, `beta_age<0`, and all five `rho<0.6`. The scoring seed does not enter this arm; three result slots must be byte-identical. | Mixed exact: age present, rehearsal absent. | All seven values, fixture/schedule hashes, cross-slot identity, exact verdict. |
| Rehearsal-only | Exact fixed-fixture checks: `beta_age>=0` and all five `rho>=0.6`; cross-slot identity mandatory. | Mixed exact: age absent, rehearsal present. | Six values, fixture/schedule hashes, cross-slot identity, exact verdict. |
| Permuted (V4.2 statistic retained) | Per seed, compute the V4.2 200-entry `rho(age, accessibility)`. Use `S=abs(rho)` against 1000 exchangeable mapping-permutation null values, plus-one p-value, `alpha_seed=0.05/3`. The fixed `null_abs_rho_p95<=0.15` remains one pre-scoring power check, not three stochastic tests. | Two-sided magnitude: strong association of either sign means mapping permutation retained structure. | Observed rho, 1000 null absolute rhos, p95 and power verdict, exceed/tie count, p-value, RNG records. |
| Shuffled (V4.3) | Per seed, each null reassignment yields five bin rhos and `M_null=max_b rho_null[b]`; `M_obs=max_b rho_obs[b]`. Apply the upper-tail plus-one p-value and `alpha_seed=0.05/3`. | Upper only: excess positive rho retains rehearsal signal. Any value below the upper threshold, including below the former lower band, is `shuffle exceeded typical destruction — informational` and never fails. | Observed five rhos, 1000×5 null matrix, 1000 maxima, observed max, order statistic 985, exceed/tie count, p-value, informational labels, RNG records. |
| Oracle | Exact ground-truth fixture checks retained from V4: `R²>=0.85`, `beta_age<0`, five conditional tests pass, five `rho>=0.6`. | Mixed exact, fixed by oracle definition. | All underlying values, fixture hash, exact verdict. |
| Empty | Exact defined-error/no-numeric-result contract. | Exact mismatch. | Error tag and numeric-result-absent flag. |

The old frozen/fair-naive 95th-percentile-per-seed rules, the old V4.2 permuted 95% band per seed, and the old shuffled binwise band are superseded. The candidate-facing L1 PASS/KILL bars are not changed.

### 2.10 Full L18 battery checklist for L1 — harmonized

| Control | Exact consolidated pass condition |
|---|---|
| Empty | Defined error and no numeric statistic, exact. |
| Permuted | V4.2 200-entry absolute-rho plus-one p-value `>0.05/3` on all three seeds; single pre-scoring `null_abs_rho_p95<=0.15` power check. |
| Shuffled | V4.3 one-sided upper null-of-the-max plus-one p-value `>0.05/3` on all three seeds; lower values informational only. |
| Oracle | Exact V4 oracle predicates all pass. |
| Fair-naive | Upper-tail R² plus-one p-value `>0.05/3` on all three seeds. |
| Frozen | Upper-tail R² plus-one p-value `>0.05/3` on all three seeds. |
| Recency-only | Exact `R²>=0.85`, `beta_age<0`, all five `rho<0.6`, and cross-slot identity. |
| Rehearsal-only | Exact `beta_age>=0`, all five `rho>=0.6`, and cross-slot identity. |

This table, §2.9, and §2.11 use the same names, direction, p-value, alpha allocation, and lower-value disposition.

### 2.11 Verdict branches — consolidated

- **PASS:** all unchanged candidate-facing L1 conditions pass on all three fresh scoring seeds; both exact factor-isolation arms pass; and the frozen, fair-naive, permuted, and shuffled stochastic families each have all three `p_s>0.05/3`. Pre-scoring closure status must be `PASS`.
- **KILL:** unchanged from the governing positive-claim specification. No control-arm statistical outcome is a candidate KILL.
- **INSTRUMENT FAILURE:** any exact L1 control predicate fails; any frozen, fair-naive, permuted, or shuffled `p_s<=0.05/3`; any mandatory raw array, RNG record, family field, or arithmetic reproduction is missing/malformed; or the post-scoring JUDGE cannot reproduce a p-value from returned artifacts. A shuffled value below its upper threshold never enters this branch.
- **Reported only:** all earlier reported-only quantities remain non-gating.

## 3. L3 systemic correction

The V4.1 candidate definition and candidate-facing reduction bars remain unchanged. The five control families are frozen, oracle, permuted, shuffled, and empty. Only empty is deterministic. Frozen, oracle, permuted, and shuffled all consume a scoring-seed-specific noisy AR(3) sequence, fitted finite-sample models, and held-out losses; therefore all four are stochastic. Pairing and a numeric tolerance reduce variance but do not prove an inequality for every possible sequence.

For every stochastic L3 draw, the complete pipeline is rerun: innovations → 1,010×8 sequence → registered windows → design matrices and targets → fits → predictions → per-example component losses → five horizon reductions. Observed and null draws use the same pipeline and differ only in the frozen RNG domain described in §6.

### 3.1 Frozen

Retain the negative-control direction: positive state benefit is failure-relevant and smaller/negative reduction is stronger destruction. Each observed/null draw yields five `reduction_h`; define `S=max_h reduction_h`. Use 1000 exchangeable full-pipeline AR(3) null draws per seed, the upper-tail plus-one p-value, and `alpha_seed=0.05/3`. This replaces the unproved finite-sample `reduction_h<=0` instrument trigger; it does not alter any candidate bar.

### 3.2 Oracle

Retain both adopted validity anchors and directions. For every horizon define

`v_h = max(0.05 - oracle_reduction_h, oracle_reduction_h - 0.95)`.

Low reduction remains an ineffective-oracle direction; high reduction remains a ceiling/corner direction. Define `S=max_h v_h`. Use 1000 exchangeable full-pipeline oracle null draws per seed, the upper-tail plus-one rank of the two-sided interval-violation score, and `alpha_seed=0.05/3`. The anchors 0.05 and 0.95 are not moved or renamed; they define the score. The calibrated family asks whether the observed worst anchor violation is unusually large under the exact specified oracle apparatus.

### 3.3 Permuted

The V4/V4.1 claim `permuted reduction_h<=0` was explicitly unproved (NF8). For each seed, observed and 1000 null channel derangements are exchangeable draws from the uniform set of eight-channel derangements. Each yields five reductions; define `S=max_h reduction_h`. Apply the upper-tail plus-one p-value and `alpha_seed=0.05/3`. Positive benefit is the only meaningful failure direction; more-negative values are stronger destruction.

### 3.4 Shuffled

Retain the paired same-sequence frozen comparator and `+0.01` tolerance. For every horizon define

`d_h = shuffled_reduction_h - paired_shuffled_frozen_reduction_h - 0.01`.

Only large positive `d_h` undermines destruction; smaller values are stronger destruction. Observed and 1000 null cycle-order permutations are exchangeable draws using the identical shuffled/frozen fitting pipeline. Define `S=max_h d_h`; apply the upper-tail plus-one p-value and `alpha_seed=0.05/3`.

### 3.5 L3 family closure

For frozen, oracle, permuted, and shuffled the conservative pre-correction FWFP is 1 because no universal finite-sample proof or calibrated error rate existed. Each corrected family has per-seed size at most `16/1001` and three-seed FWFP at most `48/1001`. Empty remains an exact interface contract.

## 4. L5 systemic correction

The seven families are single-axis, full-scan, oracle, frozen, permuted, shuffled, and empty. All except the combination portion of permuted are exact finite/combinatorial/interface predicates retained unchanged.

For L5 permuted combination accuracy, replace the old per-seed 95% empirical band with an exchangeable two-sided randomization rank. Combine the observed accuracy and 1000 null derangement accuracies, compute their common arithmetic mean, and compute the absolute departure of each of the 1001 values from that common mean. The common transformation is permutation-symmetric. The plus-one p-value is the rank tail of observed absolute departure among the 1000 null departures, with ties counted against the control and `alpha_seed=0.05/3`. The chain-content mismatch rate remains exactly 1.00 and is not statistical.

Required fields: observed accuracy, 1000 null accuracies, pooled center, observed/null absolute departures, exceed/tie count, p-value, exact chain mismatch rate, alpha, verdict, and RNG records.

## 5. L6 systemic closure

The six families—empty, permuted, shuffled, oracle, frozen, and fair-naive—are exhaustive finite schema, equality, serialization, or namespace-enumeration predicates. None uses a percentile, sampling interval, or level-alpha decision. Their stochastic FWFP is inapplicable; every check and independent-verification field is frozen in the 26-family inventory. No L6 rule changes.

## 6. Frozen RNG protocol

**Protocol ID:** `M3-V4.4-SHA256-CTR-FY-v1`.

**Hash:** SHA-256 exactly as specified by FIPS 180-4.

**Root domain separator:** ASCII/UTF-8 bytes `MOVING-ORIGIN/M3/V4.4/CONTROL-RNG/v1` (hex `4d4f56494e472d4f524947494e2f4d332f56342e342f434f4e54524f4c2d524e472f7631`).

**Encoding:** law, arm, and draw role are Unicode NFC encoded as UTF-8, each preceded by its unsigned 16-bit big-endian byte length. The scoring seed is unsigned 64-bit big-endian; replicate and subdraw indices are unsigned 32-bit big-endian; stream counter is unsigned 64-bit big-endian.

**Key:** `SHA256(root_domain || 0x00 || enc(law) || enc(arm) || enc(draw_role) || u64be(scoring_seed) || u32be(replicate_index) || u32be(subdraw_index))`.

**Domains:** observed draws use role `OBSERVED`, replicate index 0. Null draws use role `NULL`, replicate indices 0..999. Subdraw index identifies the statistic component. A `(law,arm,role,seed,replicate,subdraw)` tuple may be consumed once only; reuse is an instrument failure.

**Stream:** `block_c=SHA256(key||u64be(c))`, `c=0,1,...`; concatenate. Consume non-overlapping unsigned 64-bit big-endian words. For modulus `m`, reject `x>=floor(2^64/m)*m`; otherwise return `x mod m`. Generate permutations with Fisher–Yates from `i=n-1` through 1. Generate a derangement by drawing consecutive full permutations from the same stream and accepting the first with no fixed point.

**Exchangeability:** OBSERVED and NULL use the identical sample space, stream construction, rejection sampler, and control transform. Only disjoint domain role/replicate inputs differ. Thus each is generated by the same uniform finite algorithm and the 1001 rank positions are exchangeable under the specified SHA-256 pseudorandom model. No platform RNG, language hash, native-endian conversion, floating draw, or percentile interpolation is allowed. Raw derived keys, accepted permutations, rejection counts, and stream-block counts ship for deterministic cross-platform reproduction.

No fresh seed identity is present in this specification or pre-scoring evidence.

## 6.1 Raw returned-artifact schemas for complete JUDGE recomputation

Summary statistics are never sufficient evidence for a stochastic family. For each observed and null draw, the returned artifact must contain the raw inputs, transform, intermediate observations, and component outputs named in `verification/m3_control_family_closure_inventory.json.raw_artifact_schemas`. The schema is binding and includes:

- **L1 frozen/fair-naive:** all 200 entry factor rows, all 100 candidate sets and 500 ranked occurrences, ranking permutation where applicable, per-entry accessibility contributions and aggregates, bin membership/means/age representatives, and reported R². JUDGE recomputes ranks, aggregation, OLS, and R².
- **L1 permuted:** all 200 entry IDs, original factor vectors, mapping permutation, accessibility vector, and complete 200 paired age/accessibility rows. JUDGE recomputes tied ranks and Spearman rho.
- **L1 shuffled:** all entry/bin rows, 1,200 priming queries and assignment, realized counts, candidate sets/ranks/accessibilities, and every within-bin rehearsal/accessibility pair for every observed/null draw. JUDGE recomputes all five rhos.
- **Every stochastic L3 family:** innovations, complete sequence, registered train/validation/evaluation indices, design matrices, targets, fitted weights, baseline/control predictions, per-example squared-error components, aggregate losses, reductions, and family-specific violation/difference scores for all five horizons and all 1001 draws. JUDGE can reproduce the generator, fits, predictions, losses, reductions, maxima, and p-values without trusting a supplied summary.
- **L5 permuted:** all 200 facts and truth labels, field derangement, every query prediction/correctness row, chain nodes/content derangement, returned and expected chain content. JUDGE recomputes accuracy, pooled departures, mismatch rate, and p-value.

Each raw artifact also carries the RNG derivation record and SHA-256 digest for every array. Numeric arrays use raw C-row-major little-endian two's-complement `int64`, IEEE-754 binary64, or boolean `uint8` restricted to 0/1, with no padding. The manifest supplies field name, relative path, shape, dtype, byte order, row key, ordering rule, byte length, and SHA-256. Strings are Unicode NFC/UTF-8. Every binary64 must be finite. Missing raw data, a mismatch between raw recomputation and a summary, or inability to reproduce any statistic is `INSTRUMENT FAILURE`.

## 7. Two-phase closure and custody

### 7.1 Phase A — pre-scoring specification closure (this gate)

Uses no observed fresh scoring statistic. It verifies exactly: 26-family inventory; complete check sets; directions; deterministic/stochastic classification; current error and pre-correction FWFP; correction method; corrected FWFP; artifacts; RNG protocol; exchangeability argument; schema; numerical satisfiability; and consistency of §§2.9–2.11. Its output is `verification/m3_control_family_closure_results.json`.

Phase A **must not** compute observed maxima, observed departures, exceed/tie counts, or per-seed p-values. Those fields are schema requirements only. Phase A PASS permits independent CRITIC review; it is not implementation or scoring clearance.

### 7.2 Phase B — post-scoring JUDGE verification

Only after implementation clearance and Rebecca's fresh-seed supervised run, JUDGE uses returned raw artifacts to recompute observed statistics, every null statistic, maxima/departures, exceed/tie counts, plus-one p-values, exact predicates, per-family verdicts, and cross-run consistency. JUDGE must also reproduce every RNG key and transform from the returned unnamed-at-spec-time seed identities. A mismatch is `INSTRUMENT FAILURE`, never a candidate KILL.

## 8. Machine-readable inventory and closure result

`verification/m3_control_family_closure_inventory.json` is binding for the 26-family audit details, classification evidence, and raw artifact schemas. `verification/verify_m3_control_family_closure.py` independently derives classification from explicit variability-source flags; it contains no hard-coded set of stochastic family IDs. It must fail unless all requirements in the task prompt and this specification are satisfied. Its checked-in result is specification evidence only.

Verifier custody hashes use canonical text bytes: decode UTF-8 (accept and remove one leading BOM), replace CRLF and lone CR with LF, remove all trailing LF bytes, append exactly one LF, re-encode UTF-8, then SHA-256. Raw working-tree newline representation is never hashed.

## 9. Verdict branches and remaining authorization blockers

- **PRE-SCORING CLOSURE PASS:** all specification checks pass and all stochastic corrected FWFP bounds are at most 0.05; proceed only to independent CRITIC review.
- **PRE-SCORING CLOSURE INSTRUMENT FAILURE:** any omission, inconsistency, unjustified direction, stochastic bound above 0.05, incomplete RNG rule, or deterministic family without an exactness rationale keeps scoring blocked.
- **SCORING:** remains blocked pending CRITIC clearance of V4.4, implementation by an authorized role, independent implementation clearance, courier update including mandatory round-trip log and mechanical ledger/manifest label fixes, and Rebecca's explicit fresh-seed supervised authorization.
- **MERGE:** Rebecca alone may authorize/perform gate merge. This ARCHITECT branch is not merged.

