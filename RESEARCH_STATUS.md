# Research Status

This page is a compact index of governing results. Detailed specifications, raw summaries, reviews, and rulings remain authoritative.

| Stage | Governing status | Supported conclusion | Principal limitation | Primary record |
|---|---|---|---|---|
| M1 | PASS | The measurement and scoring harness cleared its recorded validation gate. | This validates the instrument stage, not the full research claim. | [`reviews/judge_m1_run1_ruling.md`](reviews/judge_m1_run1_ruling.md) |
| E1 | PASS on seeds 42–46 | The candidate met the recorded correctness, operational-distinctness, and load-bearing-coupling bars. | Five seeds and a purpose-built experiment do not establish generality. | [`reviews/judge_e1_run2_ruling.md`](reviews/judge_e1_run2_ruling.md) |
| M3 V4.4 | Overall INSTRUMENT FAILURE | Every candidate-facing bar passed; L1/L5/L6 passed on all seeds; L3 passed on seeds 301/302. | One of 27 stochastic control checks failed: L3 frozen-control calibration on seed 303. L3 is unscoreable on that seed, blocking an overall PASS. | [`reviews/judge_m3_v44_scoring_ruling.md`](reviews/judge_m3_v44_scoring_ruling.md) |
| M3 reproducibility repair | CRITIC-CLEARED implementation | The code now compares scoring-semantic digests while separately recording final-report integrity. | The repair was completed after the historical run and was not used to rerun protected scoring seeds. | [`reviews/critic_m3_reproducibility_contract_bf1_reverification.md`](reviews/critic_m3_reproducibility_contract_bf1_reverification.md) |
| M4 tokenizer materialization | Engineering PASS; evidence CLEAR | The governed tokenizer construction passed all 18 checks through atomic publication, and its final evidence-preservation correction was independently cleared. | This establishes tokenizer construction and evidence integrity only. The operation is consumed; it is not a model-quality or scoring result. | [Final execution-evidence review](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/7274fbb1aef06d686efe07bb54b6828d0a5b41e2/reviews/critic_m4_tokenizer_pass_evidence_ex_pass2_final_rereview.md) |
| M4 post-tokenizer integration | JUDGE engineering-readiness CLEAR | The corrected mutation apparatus supplied fail-closed sensitivity evidence while the accepted production implementation and tests remained byte-identical. | The ruling returns the package to Rebecca for a separate integration decision. It is not merge, run, qualification, scoring, or science authority. | [Recorder-published ruling](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/3470ab1a032644eba30cbe6b4e361c9a9518d95e/docs/rulings/judge_m4_post_tokenizer_mutation_clear_readiness_reconsideration.md) |
| M4 WSL2 dual-runtime diagnostic | Structural PASS; replica MISMATCH | The paired public diagnostic compared 164 outputs, with 80 agreements and 84 mismatches, while preserving the original v1 blocked disposition. | Structural feasibility does not establish replica equivalence, model quality, qualification, scoring, science, or readiness. Exact-replica consumers must stop on mismatch. | [Two-axis review](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/4cdb5d89945b603c20cdd19233079be14b65946b/reviews/critic_m4_wsl2_two_axis_dependency_lock_bf1_bf2_rereview.md) |
| M4 public observation backend | Repository-quality CLEAR; `run_authorized=false` | The custody-free design and implementation are independently clear, including the fail-closed zero-count boundary. | No model observation run, qualification, scoring, science, readiness action, or gate decision has occurred. | [Implementation rereview](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/98b8f466db2ad8499ea5abab9111a68a9bd1e861/reviews/critic_m4_public_model_observation_backend_bf1_zero_count_rereview.md) |
| M4 final pre-scoring crash cart | v0.2-alpha under review | A corrected, versioned full-stack non-scoring rehearsal design exists with warmup, fail-closed staged reports, and explicit no-scoring boundaries. | v0.1-alpha remains blocked. v0.2-alpha is not yet cleared, promoted, implemented, runnable, or released. | [Versioned routing record](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/757dc3bf3b7eec554ee15882af94fce4a6ebb006/handoffs/ARCHITECT_TO_COORDINATOR_M4_FINAL_PRESCORING_CRASH_CART_BF1_BF4_VERSIONED_ROUTING_2026-08-22.md) |

## M3 control-check denominator

The 27 stochastic checks comprise:

- L1: four stochastic control families × three seeds = 12;
- L3: four stochastic control families × three seeds = 12;
- L5: one stochastic control family × three seeds = 3.

Twenty-six passed. The failed check was L3 frozen control on seed 303, with a plus-one p-value of `12/1001 ≈ 0.011988` against `alpha_seed = 0.05/3 ≈ 0.016667`.

That result is classified as an instrument failure because it concerns control calibration. The locked fail-closed protocol nevertheless prevents an overall M3 pass. Both facts are required for an accurate interpretation.

## Claims boundary

The present evidence supports further investigation of moving-origin temporal indexing. The M4 records above are engineering or diagnostic evidence unless explicitly stated otherwise. No protected-seed M4 scoring result or M4 scientific verdict exists. The evidence does not establish awareness, consciousness, AGI, sentience, or completion of the five-milestone program.
