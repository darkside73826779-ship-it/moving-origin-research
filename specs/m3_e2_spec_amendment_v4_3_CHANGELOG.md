# M3/E2 V4.3 Targeted Amendment — Companion Changelog

**Base:** `8e9f83a6f7fac8dd6682a446c2730ed14752cc8c`

**Gate served:** Rebecca M3 Block Ruling

**Scope:** §2.9 and §2.11 L1 shuffled-arm calibration only

## Finding-to-section map

| Requested or governing finding | Exact resolution |
|---|---|
| Two-sided shuffled band treats stronger-than-expected destruction as failure | Amendment §1 makes the test upper-only; §2 removes the old outside-band clause; §1 artifact field `below_threshold_label` preserves below-threshold observations as informational. |
| One-sided alone leaves unacceptable multiplicity | Amendment §1 defines a five-bin null-of-the-max test; §1 and §3 apply Bonferroni across three scoring seeds. |
| Familywise false-positive must be ≤5% across all shuffled checks | Amendment §1 derives `48/1001 = 0.047952...`; §3 makes direct closure verification and the JSON evidence mandatory; §4 records numerical closure. |
| Exact fixtures/equations/metrics/thresholds required | Amendment §1 fixes 1000 replicates, five conditional Spearman statistics, `M=max rho`, plus-one p-value, `alpha/3`, and order statistic 985. |
| Exact verdict branches and instrument-failure branches required | Amendment §2 replaces §2.11's shuffled clause; §5 enumerates closure and scoring outcomes. |
| Exact artifact fields required | Amendment §1 provides per-seed/run fields; §3 freezes `m3_control_familywise_closure.json`. |
| Standing systemic closure-audit requirement | Amendment §3 item 5 requires family inventory, directionality, and FWFP for every control arm before scoring. |
| O-14 and fresh-seed protection | Amendment §0 and §5 retain the failed result and prohibit re-run; fresh scoring uses three unnamed fresh authorized seeds via the supervised executor. |
| Preserve candidate bars and unrelated law | Amendment §0 and §2 state that no candidate PASS/KILL predicate or unrelated control/law changes. |
| Preserve negative and instrument-failure labels | Amendment §0 and §5 require original labels to remain. |

## Evidence read

- Binding ruling: `docs/rulings/REBECCA_M3_BLOCK_RULING.md` at the exact base commit.
- Governing state: `state/STATE.md` at the exact base commit.
- Governing L1 text available in the base tree: `specs/m3_e2_spec_amended_v4.md`, §§2.9 and 2.11.
- Retained scoring review: `reviews/judge_m3_scoring_ruling.md` on `origin/recorder/m3-scoring-return-custody`; it records three below-lower-bound shuffled violations across seeds 201 and 203, candidate bars passing, and the original `INSTRUMENT FAILURE` verdict.
- The binding ruling refers to “the Critic's narrowest remedy” but no standalone post-run CRITIC review is present at the base commit, on the scoring-return custody ref, in PR #8, or on any fetched remote ref. This changelog therefore cites only the CRITIC disposition actually preserved by the binding ruling: one-sided treatment was proposed and Rebecca required one-sided plus multiplicity control. No absent review text is reconstructed or attributed.

## Quantitative verification map

| Check | Expected | Evidence |
|---|---:|---|
| Old 15-check two-sided FWFP | `0.5367087698` | `verification/verify_m3_l1_shuffled_fwfp.py` |
| One-sided-only FWFP from ruling | `0.3159793144` | same |
| Per-seed finite randomization size bound | `16/1001 = 0.0159840160` | same |
| Three-seed familywise union bound | `48/1001 = 0.0479520480` | same |
| Binding bar | `0.05` | ruling §2 |

## No-change audit

- No production or experiment code changed.
- No scoring or diagnostic run was conducted.
- No fresh or withheld scoring seed was named, accessed, or exposed.
- No candidate-facing bar was lowered, raised, renamed, or reinterpreted.
- No L3, L5, L6, L9, L15–L18, L20, Persistence Doctrine, O-14, or O-15 rule changed.
- No authorization to score, merge, or claim CRITIC/Rebecca approval is asserted.
