# M3 Reproducibility-Contract Specification v1

**Serves:** M3 reproducibility-contract clarification (Rebecca's binding design direction, 2026-08-17)
**Status:** ARCHITECT specification — requires CRITIC review before TASK BUILDER implementation
**Date:** 2026-08-17 · **Author:** ARCHITECT
**Base SHA:** `f9d16fa` (GitHub main)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this specification > agent judgment
**Prior reviews:** CRITIC M3 V4.4 scoring results review (`reviews/critic_m3_v44_scoring_results_review.md`) — diagnosed the construction bug. Rebecca M3 delivery gate ruling (`docs/rulings/REBECCA_M3_DELIVERY_RULING.md`) — authorized provisional M4 advancement, required this fix before future scoring. Provenance log reviewed through Entry 52.
**Role boundary:** The ARCHITECT specifies the contract. No code implementation, no scoring, no seed execution, no merge.

---

## 0. Problem statement

The `--verify-reproducibility` second pass calls `run_l1(seed)`, `run_l3(seed)`, `run_l5(seed)` without `artifact_writer`, while pass 1 passes `artifact_writer=raw_artifact_writer`. This creates structural differences in the result dictionaries:

### Fields that differ between pass 1 (with writer) and pass 2 (without writer)

**All laws (L1, L3, L5):**
- `v44_artifact_support.status`: `'complete_streaming_raw_artifacts'` (pass 1) vs `'in_memory_test_mode'` (pass 2)
- `v44_artifact_support.full_per_draw_raw_schema_complete`: `True` (pass 1) vs `False` (pass 2)

**L1:**
- `permuted.rho_null_1000_values`: absent in pass 1, present in pass 2 (added only when `artifact_writer is None`)
- `v44_stochastic_controls.{frozen,fair_naive}.r_squared_null_1000`: absent in pass 1, present in pass 2
- `v44_stochastic_controls.{frozen,fair_naive}.null_statistics`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.{frozen,fair_naive}.rng_derivation_records`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.null_statistics`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.abs_rho_null_1000`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.paired_age_accessibility_200`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.rng_derivation_records`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.shuffled.null_statistics`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.shuffled.rho_null_1000x5`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.shuffled.null_max_1000`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.shuffled.observed_query_to_entry_assignment_1200`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.shuffled.observed_realized_rehearsal_counts_200`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.shuffled.rng_derivation_records`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.*.raw_draw_manifest_refs`: present in pass 1, absent in pass 2

**L3:**
- `v44_stochastic_controls.*.null_statistics`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.*.rng_derivation_records`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.*.raw_draw_manifest_refs`: present in pass 1, absent in pass 2

**L5:**
- `v44_stochastic_controls.permuted.null_statistics`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.rng_derivation_records`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.null_accuracies_1000`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.null_absolute_departures_1000`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.query_results_200`: absent in pass 1 (popped), present in pass 2
- `v44_stochastic_controls.permuted.raw_draw_manifest_refs`: present in pass 1, absent in pass 2

**Impact on scored metrics:** None. No candidate bars, p-values, or verdicts are affected. The comparison fails because of structural dictionary differences, not non-determinism.

### What was rejected (for the record)

- **Option A (full artifact reproduction):** Doubling execution, I/O, file count, and storage adds substantial failure surface without improving confidence proportionally.
- **Loose Option B (recursive field stripping):** Could silently hide future nondeterminism by stripping fields without an explicit allowlist.

---

## 1. Design direction (Rebecca-binding)

Rebecca directed a strict version of "strip fields" (Option B) with the following binding requirements:

1. Define an explicit, versioned reproducibility projection containing every scoring-relevant value.
2. Compute a canonical digest from that projection in both passes.
3. Fail closed if an unclassified field appears — allowlist, not recursive deletion.
4. Add mutation tests proving that changing any scoring field changes the digest.
5. Continue validating the first pass's complete raw-artifact manifest separately.
6. The output label should say exactly what it certifies: "bit-identical scoring-semantic reproducibility."
7. Future extension (not for this fix): hash-only artifact writer.

---

## 2. Versioned reproducibility projection

### 2.1 Projection identity

**Projection name:** `m3_scoring_semantic_reproducibility`
**Projection version:** `v1`
**Binding to:** M3 V4.4 harness (`src/m3_harness.py` at `f9d16fa`)

### 2.2 Three classifications

Every field in the raw results dictionary must fall into exactly one of three classifications. Any field not found in any classification triggers a fail-closed error.

#### Classification A — Required semantic digest fields

These fields are included in the canonical digest. They encompass every value that influences scoring decisions: candidate metrics, control statistics, integer exceed/tie counts, p-values, exact predicates, verdicts, failure reasons, RNG derivation summaries, null distributions, non-timing configuration, deterministic control hashes, and cross-slot identity evidence.

#### Classification B — Explicit non-digest fields

These fields are excluded from the digest with a stated rationale. They are validated separately where applicable (e.g., raw-artifact manifest validation) but do not participate in the semantic digest comparison. These fields are treated as optional: their presence (pass 1) or absence (pass 2) does not affect the digest.

#### Classification C — Derived duplicate fields with invariant checks

These fields are duplicates of canonical semantic fields in Classification A. They are not independently digested. Instead, an invariant check asserts equality to their canonical source. If the duplicate value differs from the canonical value, the reproducibility check fails.

### 2.3 Top-level configuration block

The projection includes a top-level configuration block that is itself a digest input. This prevents two runs with identical law results but different configuration from producing the same digest.

**Configuration fields (Classification A):**

| Field | Source | Description |
|---|---|---|
| `projection_schema_version` | Fixed: `"m3_scoring_semantic_reproducibility_v1"` | Versioned projection identity |
| `mode` | `args.mode` | Run mode: `development` or `scoring` |
| `seeds` | `seeds` (ordered list) | Ordered seed list used in the run |
| `laws_selected` | `laws_to_run` | Ordered law selection |
| `protocol_id` | `V44_PROTOCOL_ID` | V4.4 stochastic protocol identifier |
| `null_replicate_count` | `V44_NULL_REPLICATES` | Number of null replicates (1000) |
| `alpha_family` | `V44_ALPHA_FAMILY` | Familywise alpha (0.05) |
| `alpha_seed` | `V44_ALPHA_SEED` | Per-seed alpha (0.05/3) |
| `locked_bars` | All L1/L3/L5/L6 locked bar constants | Complete locked numeric configuration: L1 (R2_BAR, RHO_BAR, LAMBDA, BETA, NOW_FINAL, N_BINS, BIN_SIZE, MEASURED_PER_BIN, STRIDE, N_CANDIDATE_SETS, SET_SIZE, APPEARANCES_PER_ENTRY, TIEBREAK_SEED, FAIR_NAIVE_SEED, PERMUTED_SEED, STRUCTURAL_SEED, N_MEASURED, REHEARSAL_TARGETS, N_REPLICATES, PRIMING_COUNT), L3 (REDUCTION_BAR, HORIZON, SEQUENCE_LENGTH, STATE_DIM, INPUT_DIM, OUTPUT_DIM, FIT_ORIGINS, EVAL_ORIGINS_START, EVAL_ORIGINS_END, N_EVAL, C_CLIP), L5 (ACCURACY_BAR, CHAIN_WALK_ACCURACY_BAR, N_CHAINS, CHAIN_LENGTH, N_COMBINATION_FACTS, N_CHAIN_FACTS, N_REPLICATES, N_SUBJECTS, FREEZE_CYCLE, W, N_QUERIES, N_CHAIN_QUERIES), L6 (N_ATTACKS, N_AUDIT_ROWS), V44 constants (NULL_REPLICATES, ALPHA_FAMILY, ALPHA_SEED, PROTOCOL_ID), growth thresholds (GROWTH_CANDIDATE_BAR, GROWTH_FAIR_NAIVE_BAR), timing config (TIMING_REPETITIONS, WARMUP_FRACTION, GROWTH_HISTORY_SIZES) |
| `stochastic_families_by_law` | `STOCHASTIC_FAMILIES_BY_LAW` | Law-to-family mapping |
| `seed_policy` | Mode-aware string | Development: list of development seeds. Scoring: `"WITHHELD; supplied by courier"` |

### 2.4 Top-level output fields (beyond per-law results)

The following top-level output fields that affect the overall verdict are Classification A:

| Field | Source | Description |
|---|---|---|
| `overall_verdict` | Computed from all law verdicts | Overall PASS/KILL/INSTRUMENT_FAILURE |
| `interface_invariants` | `run_interface_invariants()` | L11/L13/backdating injection results (full dict: `L11_single_clock_negative_injection`, `L13_encoding_snapshot_negative_injection`, `L5_backdating_hash_negative_injection`, `passes`) |
| `finite_numeric_results` | `_check_finite(all_results)` | Boolean: all numeric results finite |
| `l20_self_test` | `l20_self_test(profile_vector)` | Full result dict: `no_drift_corr`, `no_drift_passes`, `pert1_corr`, `pert1_flags_drift`, `pert2_corr`, `pert2_flags_drift`, `both_perturbations_flag_drift`, `passes` |
| `raw_artifact_validation` | `validate_manifest()` | Dict: `passed` (bool), `manifest` (filename), `error` (string or null) |

### 2.5 Per-law projection — L1

#### Classification A (digest-included)

**Top-level L1 result fields:**
- `seed`
- `law`
- `verdict`
- `kill_reasons` (list of strings)
- `instrument_failure_reasons` (list of strings)

**Candidate arm (and identically structured arms: `oracle`, `frozen`, `fair_naive`, `recency_only`, `rehearsal_only`, `shuffled`):**
- `r_squared`
- `beta_age`
- `bin_means` (list of 5 floats)
- `bin_age_representatives` (list of 5 floats)
- `conditional_rhos` (list of 5 floats)
- `age_conditional_slopes` (list of 5 floats)
- `log_accessibility` (dict: entry_id → float)
- `priority_values` (list of 200 floats)
- `per_set_ranks` (dict: set_id → list of (entry_id, rank) tuples; present in `candidate` and `oracle` only)

**Permuted arm:**
- `spearman_rho_200entry`
- `rho_null_p95`
- `null_p95_le_0_15`
- `plus_one_p_value`
- `within_mean_pm_2sd_band`
- `diagnostic_5bin_r_squared_non_gating`

**Empty arm:**
- `returned_defined_error`
- `observed` (dict: `error` key)

**V4.4 stochastic controls (per family: `frozen`, `fair_naive`, `permuted`, `shuffled`):**

Base summary fields (all families):
- `protocol_id`
- `null_replicate_count`
- `meaningful_failure_direction`
- `observed_statistic`
- `null_statistics` (list of 1000 floats — the empirical null distribution)
- `null_upper_order_statistic_985`
- `exceed_or_tie_count`
- `plus_one_p_value`
- `alpha_family`
- `alpha_seed`
- `per_seed_pass`

Family-specific extra fields:
- **frozen, fair_naive:** `r_squared_observed`, `draw_role_observed` (dict: `ranking_permutation_200`, `r_squared`)
- **permuted:** `spearman_rho_200entry`, `abs_rho_null_1000` (list of 1000 floats), `null_abs_rho_p95`, `null_p95_le_0_15`, `observed_mapping_permutation_200` (list of 200 ints), `paired_age_accessibility_200` (list of dicts: `entry_id`, `age`, `accessibility`)
- **shuffled:** `conditional_rho_values_5` (list of 5 floats), `rho_null_1000x5` (list of 1000×5), `null_max_1000` (list of 1000 floats), `observed_max`, `age_tests_pass`, `below_threshold_labels` (list of strings), `observed_query_to_entry_assignment_1200` (list of 1200 ints), `observed_realized_rehearsal_counts_200` (list of 200 ints)

RNG derivation summaries (per family):

For each V4.4 stochastic family, a normalized RNG summary is included in the projection. This summary is built directly from the RNG draw objects at draw time (e.g., `observed_draw.artifact_record(...)`), independent of whether the artifact writer is present. The `rng_derivation_records` field in the V4.4 summary may be popped when `artifact_writer is not None`, but the normalized summary must be retained. The normalized summary per record contains:
- `rng_protocol_id`
- `hash`
- `root_domain_hex`
- `law`
- `arm`
- `draw_role`
- `scoring_seed`
- `replicate_index`
- `subdraw_index`
- `derived_key_hex`
- `stream_key_hex`
- `accepted_permutation` (or `null` for Gaussian draws)
- `rejection_count`
- `stream_block_count`
- `stream_word_count`
- `sha256_digest`

The full ordered list of these summaries is digested as `rng_derivation_summaries` per family.

**V4.4 deterministic controls (per arm: `recency_only`, `rehearsal_only`, `oracle`, `empty`):**
- `r_squared` (where present)
- `beta_age` (where present)
- `conditional_rho_5` (where present)
- `structural_fixture_hash`
- `candidate_set_schedule_hash`
- `deterministic_reproduction_equal_across_seed_slots` (where present; also set by `_v44_verify_l1_cross_slot_identity` when 3 seed slots are present)
- `cross_slot_hashes` (list of per-slot canonical hashes; added by `_v44_verify_l1_cross_slot_identity` when 3 L1 seed slots exist)
- `all_exact_checks_pass` (where present)
- `returned_defined_error` (empty arm only)
- `numeric_result_absent` (empty arm only)

#### Classification B (explicit non-digest, with rationale)

| Field | Rationale |
|---|---|
| `v44_artifact_support` | Artifact-mode indicator; differs by pass construction. Not scoring-relevant. Optional: present in pass 1, absent in pass 2. |
| `v44_stochastic_controls.*.raw_draw_manifest_refs` | File paths and content-addressed references to raw artifact objects. Validated by `validate_manifest()` separately. Optional: present in pass 1, absent in pass 2. |
| `v44_stochastic_controls.*.rng_derivation_records` | Full artifact record objects. Replaced by normalized RNG summary in Classification A. Optional: present in pass 2, absent in pass 1. |
| `per_set_ranks` in non-candidate/non-oracle arms | Excluded by harness construction in those arms. Not independently scoring-relevant. |

#### Classification C (derived duplicates with invariant checks)

| Duplicate field | Canonical source | Invariant |
|---|---|---|
| `permuted.rho_null_1000_values` (L1 top-level, present only when `artifact_writer is None`) | `v44_stochastic_controls.permuted.null_statistics` | If present, must equal `null_statistics` element-wise. If absent, no check. |
| `v44_stochastic_controls.{frozen,fair_naive}.r_squared_null_1000` (present only when `artifact_writer is None`) | `v44_stochastic_controls.{frozen,fair_naive}.null_statistics` | If present, must equal `null_statistics` element-wise. If absent, no check. |
| `v44_stochastic_controls.permuted.abs_rho_null_1000` | `v44_stochastic_controls.permuted.null_statistics` | Must equal `[abs(x) for x in null_statistics]` element-wise. |
| `v44_stochastic_controls.shuffled.null_max_1000` | `v44_stochastic_controls.shuffled.rho_null_1000x5` | Must equal `[max(row) for row in rho_null_1000x5]` element-wise. |

### 2.6 Per-law projection — L3

#### Classification A (digest-included)

**Top-level L3 result fields:**
- `seed`
- `law`
- `verdict`
- `kill_reasons`
- `instrument_failure_reasons`

**Candidate reductions:**
- `reductions` (dict: horizon → float)
- `frozen_reductions` (dict: horizon → float)
- `oracle_reductions` (dict: horizon → float)
- `permuted_reductions` (dict: horizon → float)
- `shuffled_reductions` (dict: horizon → float)
- `shuffled_frozen_reductions` (dict: horizon → float)

**Empty arm:**
- `returned_defined_error`

**V4.4 stochastic controls (per family: `frozen`, `oracle`, `permuted`, `shuffled`):**

Base summary fields: same as L1 §2.5.

Family-specific extras:
- All four families: `observed_reductions_5` (list of 5 floats), `observed_violation_score_5` (list of 5 floats or null)

RNG derivation summaries: same normalized format as L1 §2.5.

#### Classification B (explicit non-digest)

Same as L1 §2.5 Classification B.

### 2.7 Per-law projection — L5

#### Classification A (digest-included)

**Top-level L5 result fields:**
- `seed`
- `law`
- `verdict`
- `kill_reasons`
- `instrument_failure_reasons`

**Candidate arm:**
- `world_validity_accuracy`
- `self_acquisition_accuracy`
- `chain_walk_accuracy`
- `access_count_matches_k`

**Fair-naive arm:**
- `combo_accuracy_world_validity`
- `chain_walk_accuracy` (string `"N/A"`)

**Frozen arm:**
- `chain_walk_accuracy_post_freeze`
- `label`
- `chain_walk_results` (list of dicts, each: `chain_id`, `query_type`, `k`, `visited` (list of fact_ids), `expected` (list of fact_ids), `accuracy`, `access_count_delta`, `access_count_matches_k`)

**Oracle arm:**
- `world_validity_accuracy`
- `self_acquisition_accuracy`
- `chain_walk_accuracy`
- `chain_walk_results` (same row schema as frozen)

**Permuted arm:**
- `combo_accuracy`
- `chain_content_mismatch_rate`
- `plus_one_p_value`
- `pooled_center`

**Shuffled arm:**
- `combo_query_order_accuracy`
- `self_acquisition_query_order_accuracy`
- `query_order_equal_to_original`
- `chain_walk_accuracy`
- `edge_count`
- `chain_walk_results` (same row schema as frozen)

**Full-scan arm:**
- `chain_walk_accuracy`
- `access_count_deltas` (list of ints)
- `chain_walk_results` (same row schema as frozen)
- `log`

**Empty arm:**
- `combination_returned_defined_error`
- `chain_returned_defined_error`

**V4.4 stochastic controls (family: `permuted` only):**

Base summary fields: same as L1 §2.5.

Family-specific extras:
- `observed_accuracy`
- `null_accuracies_1000` (list of 1000 floats)
- `pooled_center`
- `observed_absolute_departure`
- `null_absolute_departures_1000` (list of 1000 floats)
- `chain_content_mismatch_rate`
- `field_mapping_derangement_200` (list of 200 ints)
- `chain_content_derangement_200` (list of 200 ints)
- `query_results_200` (list of per-query dicts: `query_id`, `prediction`, `truth`, `correct`)

RNG derivation summaries: same normalized format as L1 §2.5.

#### Classification B (explicit non-digest)

Same as L1 §2.5 Classification B. Note: `null_accuracies_1000`, `null_absolute_departures_1000`, and `query_results_200` are Classification A (scoring-relevant). The projection must be constructed before artifact-mode pruning removes them.

### 2.8 Per-law projection — L6

L6 does not use `artifact_writer` and has no artifact-dependent fields. All L6 result fields are Classification A:

- `seed`, `law`
- `reachability_audit` (list of dicts, each: `module`, `callable_name`, `return_type_observed`, `is_tagged_union`, `verdict`)
- `module_public_names` (dict: module → sorted list of names)
- `module_namespace_complete`
- `attacks` (list of dicts, each: `attack_id`, `path_type`, `caught`, `diagnosis`)
- `l18_arms` (dict: arm_name → dict with `expected`, `observed`, `pass`)
- `verdict`, `kill_reasons`, `instrument_failure_reasons`

---

## 3. Canonical digest method

### 3.1 Projection construction

The TASK BUILDER shall implement a function `compute_scoring_semantic_digest(results, config)` that:

1. Constructs the projection dictionary by extracting only Classification A fields from the raw results, following the field paths in §2.3–§2.8.
2. Validates Classification C invariant checks (§2.5).
3. Fails closed if any field in the raw results is not found in Classification A, B, or C.
4. Prepends the configuration block (§2.3) and top-level output fields (§2.4).
5. Serializes and hashes per §3.2.

### 3.2 Canonical serialization

The canonical digest is computed as follows:

1. **NFC normalization:** All string values are Unicode NFC-normalized (matching `_nfc()` in `m3_v44_artifacts.py`).
2. **Numeric normalization:** NumPy scalar types are converted to Python native types via `.item()`. Floats are checked for finiteness; `NaN` or `Inf` cause immediate failure (`allow_nan=False`).
3. **JSON serialization:** `json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')`
   - `ensure_ascii=True` for consistency with the existing `_v44_canonical_json_hash` in `m3_harness.py` (line 2191).
   - `sort_keys=True` ensures dict key order does not affect the digest.
   - Compact separators eliminate whitespace variation.
4. **Hash:** `hashlib.sha256(canonical_bytes).hexdigest()`

### 3.3 Digest payload structure

```json
{
  "projection_schema_version": "m3_scoring_semantic_reproducibility_v1",
  "config": { ... },
  "top_level": { "overall_verdict", "interface_invariants", "finite_numeric_results", "l20_self_test", "raw_artifact_validation" },
  "results": {
    "<seed>": {
      "L1": { ... Classification A fields ... },
      "L3": { ... },
      "L5": { ... },
      "L6": { ... }
    }
  }
}
```

The digest is computed over the entire payload. Both passes must produce identical digests.

### 3.4 Fail-closed enforcement

The projection function must:

1. Traverse every field in the raw results dictionary recursively.
2. For each leaf or container, check whether its path matches a Classification A, B, or C entry.
3. If a field is not found in any classification, raise `ReproducibilityProjectionError` with the field path and value type.
4. If a Classification C invariant check fails, raise `ReproducibilityInvariantError` with the duplicate field path, canonical source path, and both values.

This is an allowlist, not recursive deletion. Any future field added to the results without updating the projection will cause a fail-closed error, not silent exclusion.

---

## 4. Reproducibility check integration

### 4.1 Both passes use the same projection; pass 2 runs without artifact_writer

Pass 1 runs with `artifact_writer` (unchanged). Pass 2 runs **without** `artifact_writer` (unchanged from current behavior — no I/O doubling). The projection's Classification B exclusion of `v44_artifact_support`, `raw_draw_manifest_refs`, and `rng_derivation_records` means their presence (pass 1) or absence (pass 2) does not affect the digest. Classification B fields are treated as optional: the projection function must accept their presence or absence without error.

Both passes produce a `scoring_semantic_digest` via `compute_scoring_semantic_digest()`. The comparison is `pass1_digest == pass2_digest`.

### 4.2 Null statistics and RNG summaries preserved before pruning

The current harness pops `null_statistics` and other Classification A fields from V4.4 control summaries when `artifact_writer is not None`. The projection must have access to these fields in both passes.

**Specification requirement:** The TASK BUILDER shall ensure that Classification A fields (including `null_statistics`, `null_accuracies_1000`, `null_absolute_departures_1000`, `query_results_200`, `abs_rho_null_1000`, `rho_null_1000x5`, `null_max_1000`, `paired_age_accessibility_200`, `observed_query_to_entry_assignment_1200`, `observed_realized_rehearsal_counts_200`) are retained in the results dictionary regardless of `artifact_writer` state. The artifact-mode pruning may only remove Classification B fields (`raw_draw_manifest_refs`, `rng_derivation_records`).

The normalized RNG derivation summary (§2.5) must also be retained in both passes. It is built directly from the RNG draw objects at draw time, not from `rng_derivation_records` which may be popped.

### 4.3 Output label

The reproducibility output shall use this exact label:

```
"bit-identical scoring-semantic reproducibility"
```

The reproducibility result dictionary shall be restructured to:

```json
{
  "checked": true,
  "certification": "bit-identical scoring-semantic reproducibility",
  "pass1_digest": "<hex>",
  "pass2_digest": "<hex>",
  "digests_equal": true|false,
  "projection_schema_version": "m3_scoring_semantic_reproducibility_v1",
  "projection_classification_failures": [],
  "invariant_failures": []
}
```

When `--verify-reproducibility` is not requested:
```json
{
  "checked": false,
  "certification": null,
  "projection_schema_version": "m3_scoring_semantic_reproducibility_v1"
}
```

### 4.4 Raw-artifact validation (unchanged, separate)

The first pass's raw-artifact manifest validation (`validate_manifest()`) continues to run and is not replaced by the semantic digest. The semantic digest certifies scoring-semantic reproducibility only. Raw-artifact custody, schema, and RNG domain-use validation remain binding and separate. A raw-artifact validation failure continues to set `overall = 'INSTRUMENT_FAILURE'`.

---

## 5. Mutation test requirements

The TASK BUILDER shall implement automated mutation tests that traverse every Classification A leaf in a synthetic fixture and verify that mutating its value changes the digest. These tests are diagnostic (O-15) and use development seeds 101–105 only if live execution is required; synthetic fixtures are preferred.

### 5.1 Automated leaf traversal

For each law (L1, L3, L5, L6), construct a synthetic result dictionary matching the V4.4 structure. Traverse every Classification A leaf path. For each leaf:

1. Record the original digest.
2. Mutate the leaf value (for numbers: add epsilon; for booleans: negate; for strings: append a character; for lists: modify one element; for dicts: modify one value).
3. Recompute the digest.
4. Assert `mutated_digest != original_digest`.
5. Restore the original value.

### 5.2 Fail-closed tests

- **Unknown field:** Add a field `unexpected_field` to a result dictionary. Assert `compute_scoring_semantic_digest()` raises `ReproducibilityProjectionError`.
- **Missing required field:** Remove a Classification A field from a result dictionary. Assert `compute_scoring_semantic_digest()` raises `ReproducibilityProjectionError`.
- **Classification C invariant violation:** Set `permuted.rho_null_1000_values` to a value differing from `v44_stochastic_controls.permuted.null_statistics`. Assert the invariant check raises `ReproducibilityInvariantError`.

### 5.3 Non-digest field tests

- **Artifact field change does not alter digest:** Change `v44_artifact_support.status` or add/remove `raw_draw_manifest_refs`. Assert the digest is unchanged.
- **Key order does not alter digest:** Shuffle dict key order in a result dictionary. Assert the digest is unchanged.

### 5.4 Mutation test coverage

The mutation tests must cover at minimum:
- Every top-level field in each law's result dictionary.
- Every arm within each law (candidate, oracle, frozen, fair_naive, recency_only, rehearsal_only, permuted, shuffled, empty, full_scan).
- Every V4.4 stochastic control summary field, including all family-specific extras.
- Every V4.4 deterministic control field, including `cross_slot_hashes`.
- Every configuration block field.
- Every top-level output field (§2.4): `overall_verdict`, `interface_invariants`, `finite_numeric_results`, `l20_self_test`, `raw_artifact_validation`.

---

## 6. Stale label fix specification (Task 2)

### 6.1 Problem

Three output labels use development-mode boilerplate regardless of run mode:

1. **Seed exposure ledger** (`m3_seed_exposure_ledger.json`): `scope` field is hardcoded to `"M3 development diagnostics only"` (line 4204), even when `mode: scoring`.
2. **Manifest** (`m3_manifest.json`): `scoring_seed_pool` is hardcoded to `"WITHHELD; forbidden in development"` (line 4167), even when `mode: scoring`.
3. **Manifest** (`m3_manifest.json`): `r3_note` is hardcoded to reference "development" (lines 4168–4171), even when `mode: scoring`.

### 6.2 Specification

The TASK BUILDER shall implement a single mode-aware label helper, e.g. `_mode_label(mode, key)`, that returns the correct string for each mode:

| Key | Development mode | Scoring mode |
|---|---|---|
| `scope` (ledger) | `"M3 development diagnostics only"` | `"M3 supervised scoring run"` |
| `scoring_seed_pool` (manifest) | `"WITHHELD; forbidden in development"` | `"WITHHELD; supplied by courier, recorded in this artifact; future scoring seed pools remain withheld"` |
| `r3_note` (manifest) | `"Scoring-only seed identities are absent from this development implementation and its artifacts."` | `"Scoring seed identities were supplied by Rebecca's supervised-executor courier channel and recorded in the seed exposure ledger; future scoring seed pools remain withheld."` |

All three fields must be populated from this helper, not from hardcoded strings.

### 6.3 Regression tests

- **Scoring mode:** Assert ledger `scope` does not contain "development". Assert manifest `scoring_seed_pool` and `r3_note` do not contain "development" or "forbidden in development".
- **Development mode:** Assert ledger `scope` contains "development diagnostics only". Assert manifest `scoring_seed_pool` contains "WITHHELD; forbidden in development".

---

## 7. Constraints

- No bars, controls, or scoring logic modified.
- No scoring run, no fresh seeds, no hold-out seed exposure.
- No rerun of seeds 201–203 or 301–303.
- No M4 work — M4 starts separately with ARCHITECT.
- Development seeds 101–105 only for any diagnostics.
- O-14 (no re-run-on-failure), O-15 (development runs diagnostic-only), D1–D5, L9, L18 all binding.
- L15/L16/L17 forbidden before M5.

---

## 8. Future extension (not for this fix)

If full artifact reproducibility is later required, add a hash-only artifact writer that regenerates artifact bytes and computes hashes without retaining a second 16GB tree. This would provide Option A's strength without duplicating storage. This is explicitly out of scope for this specification.

---

## 9. Implementation handoff

**Next recipient:** CRITIC (review this specification for correctness, completeness, and fail-closed coverage).

After CRITIC approval: **TASK BUILDER** (implement the approved design) → **CRITIC** (verify implementation) → **RECORDER/INTEGRATOR** (publish).

**Explicitly prohibited actions for TASK BUILDER:**
- Modifying any locked bar, threshold, or scoring predicate.
- Running any scoring seeds.
- Running seeds 201–203 or 301–303.
- Implementing L7/L8/L10 or any M4 component.
- Modifying `STATE.md` or `docs/rulings/provenance_log.md` (RECORDER/INTEGRATOR custody).
- Renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
