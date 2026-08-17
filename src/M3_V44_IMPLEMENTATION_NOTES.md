# M3 V4.4 Integration Notes

`m3_harness.py` routes all nine stochastic families through the frozen V4.4
SHA-256 counter-mode RNG and writes complete per-draw raw declarations when an
output directory is supplied by `main`.

## Raw artifact custody

`m3_v44_artifacts.RawArtifactWriter` streams content-addressed numeric arrays
and NFC UTF-8 canonical JSON objects into `m3_v44_raw/objects`, then emits one
draw declaration per observed/null draw in `m3_v44_raw/draws`. Each declaration
contains the binding family field set plus RNG records. The final
`m3_v44_raw_manifest.json` contains hashes, shapes, dtypes, byte order, row
keys, ordering rules, byte lengths, finite status, and all draw declarations.
`validate_manifest` verifies custody, field coverage, and (for production
output) the observed plus null replicate coverage 0..999 for every family.

`run_l1`, `run_l3`, and `run_l5` permit no-output in-memory operation only for
focused unit tests. `main` always creates the writer and validates the complete
manifest before it presents output artifacts.

## Validation performed

Unit/static validation:

```
cd src && python -m unittest -v test_m3_v44_rng test_m3_harness
python -m py_compile m3_harness.py m3_v44_rng.py m3_v44_artifacts.py \
  test_m3_harness.py test_m3_v44_rng.py
git diff --check
```

The development-only direct-call battery ran each of L1/L3/L5/L6 exactly once
on seeds 101–105 and preserved its complete JSON/log under `diagnostics/`; all
20 calls passed. L5 exact-control code then changed, so a separately labeled
post-fix L5-only run executed once on seeds 101–105 and all five passed. No
scoring route or retained seed 201–203 was executed.

## Binding specification conflicts not resolved in code

- The inventory labels L1 rank rows `ranked_occurrences_500`, while the locked
  fixture has 100 candidate sets × 10 slots and 200 entries × 5 appearances:
  both imply 1,000 occurrence rows. The writer preserves all 1,000 occurrences
  under the inventory field name rather than silently dropping rows.
- The inventory uses `innovations_1010x8` and
  `train_validation_evaluation_indices`, while Contract 5 binds full
  `innovations_1110x8` plus fitting/buffer/evaluation index names and forbids
  train/validation field names. Emission follows the amended contract. The
  inventory/verifier needs an authoritative versioned reconciliation.

## Second-pass closure changes

- Retained seeds 201–203 are rejected before dispatch in every mode. This
  harness has no executable scoring-seed admission path; fresh supervised
  scoring requires a separate authorization/courier mechanism.
- Raw manifest validation now resolves every nested draw-field descriptor,
  verifies custody metadata and canonical text, validates protocol/key/subdraw
  RNG records and no-reuse, and requires selected family coverage per scoring
  seed (one observed and NULL 0..999). Validation failure is added to affected
  law results as `INSTRUMENT_FAILURE` before result/invariant serialization.
- L5 exact controls execute and gate full-scan path/delta=200, both oracle
  combination accuracies plus 40 path/count checks, actual shuffled query-order
  equality plus chain-edge derangement, and defined errors for both empty
  fixtures.

## Delivery boundary

This TASK BUILDER change provides producer-side custody/schema/RNG validation
and focused independent recomputation tests. A separate Phase-B JUDGE program
that consumes a future supervised scoring return and independently regenerates
all nine families is not part of this implementation handoff.
