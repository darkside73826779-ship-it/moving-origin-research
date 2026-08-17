# Research Status

This page is a compact index of governing results. Detailed specifications, raw summaries, reviews, and rulings remain authoritative.

| Stage | Governing status | Supported conclusion | Principal limitation | Primary record |
|---|---|---|---|---|
| M1 | PASS | The measurement and scoring harness cleared its recorded validation gate. | This validates the instrument stage, not the full research claim. | [`reviews/judge_m1_run1_ruling.md`](reviews/judge_m1_run1_ruling.md) |
| E1 | PASS on seeds 42–46 | The candidate met the recorded correctness, operational-distinctness, and load-bearing-coupling bars. | Five seeds and a purpose-built experiment do not establish generality. | [`reviews/judge_e1_run2_ruling.md`](reviews/judge_e1_run2_ruling.md) |
| M3 V4.4 | Overall INSTRUMENT FAILURE | Every candidate-facing bar passed; L1/L5/L6 passed on all seeds; L3 passed on seeds 301/302. | One of 27 stochastic control checks failed: L3 frozen-control calibration on seed 303. L3 is unscoreable on that seed, blocking an overall PASS. | [`reviews/judge_m3_v44_scoring_ruling.md`](reviews/judge_m3_v44_scoring_ruling.md) |
| M3 reproducibility repair | CRITIC-CLEARED implementation | The code now compares scoring-semantic digests while separately recording final-report integrity. | The repair was completed after the historical run and was not used to rerun protected scoring seeds. | [`reviews/critic_m3_reproducibility_contract_bf1_reverification.md`](reviews/critic_m3_reproducibility_contract_bf1_reverification.md) |

## M3 control-check denominator

The 27 stochastic checks comprise:

- L1: four stochastic control families × three seeds = 12;
- L3: four stochastic control families × three seeds = 12;
- L5: one stochastic control family × three seeds = 3.

Twenty-six passed. The failed check was L3 frozen control on seed 303, with a plus-one p-value of `12/1001 ≈ 0.011988` against `alpha_seed = 0.05/3 ≈ 0.016667`.

That result is classified as an instrument failure because it concerns control calibration. The locked fail-closed protocol nevertheless prevents an overall M3 pass. Both facts are required for an accurate interpretation.

## Claims boundary

The present evidence supports further investigation of moving-origin temporal indexing. It does not establish awareness, consciousness, AGI, sentience, or completion of the five-milestone program.
