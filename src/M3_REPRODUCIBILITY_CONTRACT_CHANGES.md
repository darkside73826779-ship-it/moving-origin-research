# M3 Reproducibility-Contract Implementation Changelog

**Date:** 2026-08-17
**Implemented by:** TASK BUILDER
**Gate served:** M3 reproducibility-contract implementation (Rebecca-authorized, 2026-08-17 15:07 EDT)
**Base SHA:** `a5e8a15` (GitHub main)
**Spec implemented:** `specs/m3_reproducibility_contract_v1.md` at `3c8480c` (CRITIC-CLEARED v1.1)

## Files created

- `src/m3_reproducibility.py` (961 lines) — reproducibility contract module
- `src/test_m3_reproducibility.py` — mutation tests and stale label regression tests

## Files modified

- `src/m3_harness.py` — reproducibility check integration, pruning fix, mode-aware labels

## What was implemented

### 1. Reproducibility projection and digests (`m3_reproducibility.py`)

- `ReproducibilityProjectionError` and `ReproducibilityInvariantError` exceptions
- Canonical serialization per §3.3: NFC normalization, `ensure_ascii=True`, `sort_keys=True`, `allow_nan=False`, SHA-256
- `compute_scoring_semantic_digest(results, config)` (§3.1): Classification A extraction, Classification C invariant checks, fail-closed traversal, canonical digest
- `compute_final_report_digest(...)` (§3.2): non-compared integrity hash over complete output bundle
- `mode_label(mode, key)` (§6.2): mode-aware label helper for stale scoring labels
- `build_rng_derivation_summaries(records)` (§2.5): normalized RNG derivation summaries from artifact record dicts
- Classification tables for L1, L3, L5, L6 (§2.5–§2.8) — declarative field sets for Classifications A, B, C
- Fail-closed traversal: recursively verifies every field in results dict is classified; raises `ReproducibilityProjectionError` on unclassified fields

### 2. Harness integration (`m3_harness.py`)

- **Pruning fix (§4.2):** Changed artifact-mode pruning to only remove Classification B fields (`rng_derivation_records`, `raw_draw_manifest_refs`). Classification A fields (`null_statistics`, `null_accuracies_1000`, `null_absolute_departures_1000`, `query_results_200`, `rho_null_1000x5`, `paired_age_accessibility_200`, `observed_query_to_entry_assignment_1200`, `observed_realized_rehearsal_counts_200`) are now retained in both passes regardless of `artifact_writer` state. Classification C fields (`abs_rho_null_1000`, `null_max_1000`, `rho_null_1000_values`, `r_squared_null_1000`) are also retained for invariant checking.
- **RNG derivation summaries (§2.5):** Added `rng_derivation_summaries` to all V4.4 stochastic control summaries. Built from `draw.artifact_record(...)` dicts collected at draw time, independent of `artifact_writer` presence.
- **Reproducibility check replacement (§4.1):** Replaced `_non_timing_projection` + JSON string comparison with `compute_scoring_semantic_digest` two-digest architecture. Pass 1 and pass 2 produce scoring-semantic digests; comparison is `pass1_digest == pass2_digest`.
- **Final-report digest (§3.2):** Added `compute_final_report_digest` call after overall verdict computation; stored as `reproducibility.final_report_digest`.
- **Output structure (§4.3):** Updated reproducibility output to match spec: `checked`, `certification`, `pass1_digest`, `pass2_digest`, `digests_equal`, `projection_schema_version`, `projection_classification_failures`, `invariant_failures`, `final_report_digest`.
- **Mode-aware labels (§6.2):** Replaced hardcoded label strings in manifest (`scoring_seed_pool`, `r3_note`) and ledger (`scope`) with `_mode_label(mode, key)` calls.
- **Cross-slot identity fix:** Applied `_v44_verify_l1_cross_slot_identity` to pass 2 results so both passes have identical post-processing modifications.
- **Variable shadowing bug fix:** Fixed pre-existing bug where `null_rhos` variable from L1 shuffled section overwrote L1 permuted section's value, causing `permuted.rho_null_1000_values` to contain list-of-lists instead of list-of-scalars.

### 3. Tests (`test_m3_reproducibility.py`)

- Mutation tests (§5.1): automated leaf traversal for L1, L3, L5, L6
- Fail-closed tests (§5.2): unknown field, missing required field, Classification C invariant violations
- Non-digest field tests (§5.3): artifact field changes, key ordering, Classification C mutations
- Final-report digest tests (§5.4): mutating top-level output fields changes the digest
- Stale label regression tests (§6.3): scoring mode and development mode label correctness

## What was NOT modified

- No locked bars, thresholds, or scoring predicates changed
- No candidate-facing bars modified
- No scoring run, fresh-seed exposure, or hold-out seed access
- No `STATE.md` or `docs/rulings/provenance_log.md` modified
- No L15/L16/L17 introduced
- No M4 components implemented

## Constraints honored

- O-14 (no re-run-on-failure): not applicable
- O-15 (development runs diagnostic-only): all verification runs used seeds 101–105 only
- D1–D5 (Persistence Doctrine): binding
- L9 (hard fence): not touched
- L18 (full battery): not modified
- Rebecca sole gate/merge authority: no merge performed
