# CRITIC Ruling — M3 V4.4 B1–B4 Independent Re-Review

**Gate served:** M3 V4.4 B1–B4 Independent Re-Review

**Verdict:** **CLEAR**

## Custody, lineage, scope

- Current main: `8259e01a1dfac6a09074027d9a48f034bf51d9b9` (verified against live `origin/HEAD`)
- Corrected result: `9fb186263e6aa63919e784bc81fb096907f6af30`
- Branch: `architect/m3-v4-4-critic-b1-b4`
- Direct parent of result: `b6accaad3773468d54b2363a1072877554186265` (the prior blocked result) — **confirmed**
- Merge-base with main: exactly `8259e01…` — clean linear ancestry
- Merge status: **not merged**; contained only in its own branch
- Diff vs main: exactly the five expected files added; no `state/STATE.md`, `src/`, or scoring artifacts touched
- Diff vs prior blocked result: five files, +235/−52, specification-only
- Review used a fresh clean clone, detached HEAD, working tree clean before and after verifier run

## B1 — L3 stochastic classification and FWFP closure → **RESOLVED**

- `L3.frozen`, `L3.oracle`, `L3.permuted`, `L3.shuffled` are now classified `stochastic_empirical`, each carrying `fitted_model_enters: true` plus seed/generator/sampled-observation flags.
- Independent derivation from the `classification_evidence` flags reproduces exactly **9 stochastic / 17 deterministic** with **zero** declared-vs-derived mismatches.
- No stochastic family retains deterministic FWFP zero. The four L3 families and `L5.permuted` all carry honest `pre_correction_fwfp = 1.0` (or `0.142625`) and calibrated `corrected_fwfp = 48/1001`.
- Each stochastic family uses a within-seed null-of-the-max (or two-sided violation) plus-one p-value with `alpha_seed = 0.05/3`, controlling the complete check-family, not merely each check.
- Candidate-facing bars unchanged; corrections are specification-only arithmetic preserving meaningful failure direction.

## B2 — Raw-artifact sufficiency → **RESOLVED**

- `raw_artifact_schemas` now specify per-draw **raw inputs**, not precomputed summaries: e.g. L3 families supply `innovations_1010x8`, `sequence`, `design_matrices_by_horizon`, `targets_by_horizon`, fitted weights, per-example squared errors; L1 families supply raw entries/ages/rehearsals, permutations, paired observations, within-bin rows; `L5.permuted` supplies facts, truth labels, predictions, and query results.
- A common binary contract (`shape/dtype/byte_order/row_key/ordering_rule/sha256`, finite-check, sorted-key JSON) plus a `judge_rule` requiring recomputation **without importing producer summaries** is present.
- JUDGE can therefore recompute R², correlations, predictions, component losses, reductions, accuracies, null statistics, ranks, maxima, thresholds, p-values, and verdicts. Schema-ID binding to each stochastic family is enforced.

## B3 — Verifier independence → **RESOLVED**

- The hard-coded `STOCHASTIC_IDS` allowlist and rationale-keyword test are gone.
- Classification is now **derived** from the four boolean variability flags; the verifier fails any family whose declared `reference_type` disagrees with the flag-derived type, any variable family asserting an `exact_basis`, and requires `raw_artifact_schemas` keys to exactly equal the independently derived stochastic set.
- I reproduced the verifier's derivation independently: identical result, no circular acceptance. `EXPECTED_IDS` remains a pure 26-membership check, not a classification oracle.

## B4 — Canonical hashing → **RESOLVED**

- `canonical_text_bytes` strips BOM, maps CRLF and lone CR to LF, normalizes trailing newline, then SHA-256s UTF-8 bytes; the procedure is documented in the results artifact.
- Independent recomputation matches the committed hashes exactly, and **LF and CRLF representations produce identical canonical hashes**:
  - inventory `a0d91675cd516ba2e703e4e8aad404271f8caf89b20f72d2816a8d7331d4b0e9`
  - spec `d8930baebbf493c5f042fe194cc3a42bdf4dd1e7b7f95c5d8497c3f39ccb0c2c`
- Malformed encodings raise on decode (cannot silently pass).

## New blocking findings

None.

## Non-blocking findings

- **NB1 (Documentation-only):** internal `gate` strings and `schema_version` still read "M3 V4.3" / `...-v2` while this gate is V4.4. Harmless labeling lag; recommend alignment at next revision.

## Independent FWFP arithmetic and final classification

- `1 − 0.95³ = 0.142625`; `1 − 0.95¹⁵ = 0.536708769840247`
- Largest numerator `k` with `k/1001 ≤ 1/60` is `16`; per-seed `16/1001`; three-seed union `48/1001 = 0.047952047952… ≤ 0.05`
- **Maximum corrected FWFP across all 26 families = `48/1001 ≈ 0.047952`**
- Final classification: **9 stochastic** (`L1.frozen, L1.fair_naive, L1.permuted, L1.shuffled, L3.frozen, L3.oracle, L3.permuted, L3.shuffled, L5.permuted`) / **17 deterministic**; 26 families, L1:8 L3:5 L5:7 L6:6, each exactly once.

## Verification-command result and verifier assessment

- `python verification/verify_m3_control_family_closure.py` → `verdict: PASS`, `errors: []`, `correction_count: 9`, stochastic 9 / deterministic 17, `max_corrected_stochastic_fwfp = 0.047952`.
- I did not rely on its self-report: I re-derived classification, hashes (LF+CRLF), and arithmetic independently and reproduced every material result. No discrepancy between verifier output and independent review.

## Preserved evidence

Confirmed intact: seeds 201–203 retained as INSTRUMENT FAILURE and never rerun; prior L3/L5/L6 PASS evidence; L1 candidate-facing bar evidence and no-kill finding; Rebecca Entry 43 four-part test; O-14/O-15, D1–D5, L9, L18, L15, unseen-seed and supervised-execution boundaries. No candidate-facing bar changed. Phase A / Phase B separation preserved.

## Authorization boundary

Scoring and implementation **remain blocked**. This CLEAR verdict certifies pre-scoring specification-framework closure only; it does not itself authorize scoring, implementation, seed exposure, or courier construction.

**Exact next authorized role:** **Rebecca** (sole gate/custody authority) — to accept this CLEAR and decide whether to merge `architect/m3-v4-4-critic-b1-b4` and authorize the next phase (TASK BUILDER / implementation) under a fresh prompt.

## Prohibited actions (for all roles pending Rebecca)

No specification/code/verifier edits, no TASK BUILDER work, no courier scoring packet, no fresh-seed exposure or selection, no scoring, no rerun of seeds 201–203, no STATE.md/provenance edits, no PR merge.

## Merge recommendation

**Recommend merge**, at Rebecca's discretion and by her hand, into `main` via a Rebecca-gated PR. The branch is specification-only, cleanly rooted at current main, and passes independent verification; NB1 may be folded into a later routine revision and is not a merge blocker.
