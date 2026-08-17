# M3 Reproducibility-Contract Specification — Changelog

**Spec:** `specs/m3_reproducibility_contract_v1.md`
**Date:** 2026-08-17 · **Author:** ARCHITECT
**Base SHA:** `f9d16fa` (GitHub main)
**Branch:** `architect/m3-reproducibility-contract`

---

## What this specification does

Defines a versioned, allowlist-based reproducibility projection (`m3_scoring_semantic_reproducibility_v1`) that replaces the current field-by-field JSON comparison in the `--verify-reproducibility` second pass. Also specifies mode-aware label fixes for the seed exposure ledger and manifest.

## What this specification does NOT do

- Does not modify any locked bar, threshold, scoring predicate, or control.
- Does not alter candidate-facing scoring logic.
- Does not re-run any seeds.
- Does not implement code (ARCHITECT role boundary).
- Does not modify STATE.md or provenance_log.md (RECORDER/INTEGRATOR custody).
- Does not implement the future hash-only artifact writer extension (§8).

---

## Changes from current implementation

### 1. Replaces `_non_timing_projection()` with `compute_scoring_semantic_digest()`

**Current:** `_non_timing_projection(results)` strips only `L1.reported_only.retrieval_timing` and `L5.growth`, then compares full JSON dumps. This misses all artifact-dependent fields, causing the comparison to always fail when pass 1 has `artifact_writer` and pass 2 does not.

**New:** `compute_scoring_semantic_digest(results, config)` extracts only Classification A (scoring-semantic) fields per an explicit allowlist, computes a canonical SHA-256 digest, and fails closed on any unclassified field.

### 2. Three-class field classification

**Current:** Two implicit categories — "timing fields to strip" and "everything else."

**New:** Three explicit classifications:
- **A (digest-included):** Every scoring-relevant value — candidate metrics, control statistics, null distributions, p-values, exceed/tie counts, predicates, verdicts, RNG derivation summaries, non-timing configuration, deterministic control hashes, cross-slot identity evidence, interface invariants, finite-numeric check, L20 self-test, raw-artifact validation status.
- **B (explicit non-digest):** Artifact paths, `v44_artifact_support`, `raw_draw_manifest_refs`, `rng_derivation_records` (full artifact records). Each with stated rationale. Treated as optional: present in pass 1, absent in pass 2, both valid. Validated separately where applicable.
- **C (derived duplicates):** Fields like `permuted.rho_null_1000_values`, `r_squared_null_1000`, `abs_rho_null_1000`, `null_max_1000` that duplicate canonical `null_statistics` or other Classification A fields. Invariant check, not independent digest.

### 3. Preserves null_statistics and all Classification A fields in both passes

**Current:** When `artifact_writer is not None`, L1/L3/L5 pop `null_statistics` and other scoring-relevant fields from V4.4 control summaries. This makes them absent in pass 1 but present in pass 2.

**New:** The TASK BUILDER shall ensure Classification A fields are retained in the results dictionary regardless of `artifact_writer` state. Artifact-mode pruning may only remove Classification B fields (`raw_draw_manifest_refs`, `rng_derivation_records`).

Fields that must be preserved (currently popped when writer is present):
- L1: `null_statistics` (all families), `abs_rho_null_1000`, `paired_age_accessibility_200`, `rho_null_1000x5`, `null_max_1000`, `observed_query_to_entry_assignment_1200`, `observed_realized_rehearsal_counts_200`
- L3: `null_statistics` (all families)
- L5: `null_statistics`, `null_accuracies_1000`, `null_absolute_departures_1000`, `query_results_200`

### 4. Normalized RNG derivation summaries built at draw time

**Current:** `rng_derivation_records` contains full artifact record objects (with file paths, content-addressed references) when present, and is popped when `artifact_writer is not None` for L3/L5.

**New:** A normalized RNG derivation summary (protocol, law/arm, draw role, seed, replicate/subdraw indexes, derived-key/digest, rejection/block/word counts, accepted-transform) is built directly from the RNG draw objects at draw time, independent of artifact writer state. This satisfies Rebecca's requirement that "RNG derivation summaries" be in the projection.

### 5. Top-level configuration and output block

**Current:** No configuration or top-level output fields are included in the reproducibility comparison.

**New:** A configuration block (projection version, mode, seeds, laws, protocol ID, null replicate count, alpha values, complete locked bars/thresholds/fixture sizes/seed constants, stochastic families, seed policy) is prepended to the digest payload. Top-level output fields that affect the overall verdict (`overall_verdict`, `interface_invariants`, `finite_numeric_results`, `l20_self_test`, `raw_artifact_validation`) are also included as Classification A.

### 6. Output label

**Current:** `"bit_identical": True/False` with scope `"all non-timing fields"`.

**New:** `"certification": "bit-identical scoring-semantic reproducibility"` with `pass1_digest`, `pass2_digest`, `digests_equal`, projection schema version, and any classification/invariant failures.

### 7. Stale label fixes (Task 2)

**Current:** Three labels are hardcoded to development-mode boilerplate regardless of `mode`:
- Ledger `scope`: always `"M3 development diagnostics only"`
- Manifest `scoring_seed_pool`: always `"WITHHELD; forbidden in development"`
- Manifest `r3_note`: always references "development"

**New:** A single mode-aware label helper returns the correct string per mode. Scoring mode emits scoring language (including reference to courier and seed ledger); development mode retains diagnostic language. Regression tests verify both modes.

---

## Field classification derivation

The Classification A allowlist was derived by tracing every field in the V4.4 results dictionaries for L1 (`run_l1`, line 2361), L3 (`run_l3`, line 2960), L5 (`run_l5`, line 3171), and L6 (`run_l6`, line 3390) in `src/m3_harness.py` at `f9d16fa`. The V4.4 stochastic control summary structure was traced from `_v44_summary` (line 2129). The V4.4 deterministic control cross-slot identity additions were traced from `_v44_verify_l1_cross_slot_identity` (line 364). Top-level output fields were traced from `main()` (line 3836). The artifact-dependent field differences were traced from the conditional branches at lines 2420–2421, 2426–2429, 2486–2491, 2552–2559, 2614–2615, 2994–2997, 3030–3033, 3241–3247, and 3373.

---

## Inputs reviewed

| File | SHA | Purpose |
|---|---|---|
| `src/m3_harness.py` | `f9d16fa` | Harness with reproducibility check and label locations |
| `src/m3_v44_artifacts.py` | `f9d16fa` | Artifact writer, canonical JSON, manifest validation |
| `reviews/critic_m3_v44_scoring_results_review.md` | `f9d16fa` | CRITIC diagnosis of the construction bug |
| `state/STATE.md` | `f9d16fa` | Current operational state |
| `docs/rulings/provenance_log.md` | `f9d16fa` | Provenance through Entry 52 |

---

## Standing constraints verified

- O-14 (no re-run-on-failure): No seeds rerun. No scoring seeds exposed.
- O-15 (development runs diagnostic-only): Mutation tests use synthetic fixtures or development seeds 101–105 only.
- D1–D5 (Persistence Doctrine): Specification persisted to repo branch; no STATE.md or provenance_log.md modification.
- L9 (hard fence: no learned/nonlinear retrieval): Not touched.
- L18 (full battery on every claim): Not modified.
- ≥2 unseen scoring seeds: Not applicable (no scoring run authorized).
- No renaming negatives: INSTRUMENT FAILURE label retained.
- No L15/L16/L17 before M5: Not introduced.
- Rebecca sole gate/merge authority: Specification routes to CRITIC, then Rebecca gates.
