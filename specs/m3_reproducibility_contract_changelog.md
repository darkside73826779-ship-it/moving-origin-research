# M3 Reproducibility-Contract Specification — Changelog

**Spec:** `specs/m3_reproducibility_contract_v1.md`
**Date:** 2026-08-17 · **Author:** ARCHITECT
**Base SHA:** `f9d16fa` (GitHub main)
**Branch:** `architect/m3-reproducibility-contract`

---

## v1.1 — CRITIC BF1–BF4 resolutions (2026-08-17)

### BF1: Classification C invariant #1 corrected

**Before:** `permuted.rho_null_1000_values` must equal `v44_stochastic_controls.permuted.null_statistics` element-wise.

**After:** `[abs(x) for x in rho_null_1000_values] == null_statistics` element-wise.

**Rationale:** The canonical `null_statistics` stores absolute-valued rhos (because `_v44_summary` is called with `abs_null_rhos` at line 2467). The duplicate `rho_null_1000_values` stores the signed raw Spearman rho values. The signed vector and its absolute-valued derivative are now distinguished. The previous invariant would always fail when any null rho is negative.

### BF2: Classification A/C overlap eliminated

**Before:** `abs_rho_null_1000` and `null_max_1000` appeared in both Classification A (family-specific extras) and Classification C (derived duplicates).

**After:** Both fields are removed from Classification A. They appear ONLY in Classification C. Every field is now assigned to exactly one classification, resolving the ambiguity for fail-closed traversal and mutation tests.

### BF3: Two-digest architecture

**Before:** A single digest included `overall_verdict`, `interface_invariants`, `finite_numeric_results`, `l20_self_test`, and `raw_artifact_validation`. These are not available from both passes and some are computed after the reproducibility check.

**After:**
- **Digest 1 (compared scoring-semantic digest):** Contains only per-law results + configuration. This is what pass1_digest == pass2_digest compares.
- **Digest 2 (non-compared final-report digest):** Computed once after reproducibility and artifact validation. Contains the compared digest payload + reproducibility result + all top-level output fields. Provides tamper-evidence, not reproducibility evidence. Cannot affect `overall_verdict`.

Per Rebecca's directive: "a compared scoring-semantic digest containing only fields independently available from both passes, followed by a separate non-compared final-report digest after reproducibility and artifact validation."

### BF4: Branch pushed to GitHub; SHA verified

**Before:** The branch `architect/m3-reproducibility-contract` and result SHA `e8204de` did not exist on GitHub. The specification files were local only.

**After:** The branch is pushed to GitHub. The result SHA is verified via `git ls-remote` against the remote repository. All provenance references in the handoff are corrected to the verified remote SHA.

### NF1/NF4: Canonicalization rationale documented

§3.3 now documents why `ensure_ascii=True` was chosen (consistency with `_v44_canonical_json_hash` at line 2191) and notes that NFC normalization with `ensure_ascii=True` is belt-and-suspenders — it ensures consistent Unicode representation before ASCII escaping.

### NF2: "Where present" fields clarified

§2.5 and §3.4 now explicitly state that fields marked "where present" are conditionally absent based on arm type or seed-slot count. Their absence is valid and does NOT trigger fail-closed. Only the presence of an unclassified (unknown) field triggers fail-closed.

### NF3: `rho_null_1000_values` resolution

Given BF1's invariant fix, `rho_null_1000_values` remains as Classification C with the corrected absolute-value invariant. The field is not removed — it provides a useful diagnostic cross-check between the signed raw rho vector and the absolute-valued canonical null distribution.

---

## v1.0 — Initial specification (2026-08-17)

### What this specification does

Defines a versioned, allowlist-based reproducibility projection (`m3_scoring_semantic_reproducibility_v1`) that replaces the current field-by-field JSON comparison in the `--verify-reproducibility` second pass. Also specifies mode-aware label fixes for the seed exposure ledger and manifest.

### What this specification does NOT do

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
- **A (digest-included):** Every scoring-relevant value — candidate metrics, control statistics, null distributions, p-values, exceed/tie counts, predicates, verdicts, RNG derivation summaries, non-timing configuration, deterministic control hashes, cross-slot identity evidence.
- **B (explicit non-digest):** Artifact paths, `v44_artifact_support`, `raw_draw_manifest_refs`, `rng_derivation_records` (full artifact records). Each with stated rationale. Treated as optional: present in pass 1, absent in pass 2, both valid. Validated separately where applicable.
- **C (derived duplicates):** Fields like `permuted.rho_null_1000_values`, `r_squared_null_1000`, `abs_rho_null_1000`, `null_max_1000` that duplicate canonical `null_statistics` or other Classification A fields. Invariant check, not independent digest. Each field appears in exactly one classification (BF2 resolution).

### 3. Preserves null_statistics and all Classification A fields in both passes

**Current:** When `artifact_writer is not None`, L1/L3/L5 pop `null_statistics` and other scoring-relevant fields from V4.4 control summaries. This makes them absent in pass 1 but present in pass 2.

**New:** The TASK BUILDER shall ensure Classification A fields are retained in the results dictionary regardless of `artifact_writer` state. Artifact-mode pruning may only remove Classification B fields (`raw_draw_manifest_refs`, `rng_derivation_records`).

Fields that must be preserved (currently popped when writer is present):
- L1: `null_statistics` (all families), `rho_null_1000x5`, `paired_age_accessibility_200`, `observed_query_to_entry_assignment_1200`, `observed_realized_rehearsal_counts_200`
- L3: `null_statistics` (all families)
- L5: `null_statistics`, `null_accuracies_1000`, `null_absolute_departures_1000`, `query_results_200`

Classification C fields must also be preserved for invariant checking:
- L1: `abs_rho_null_1000`, `null_max_1000`

### 4. Normalized RNG derivation summaries built at draw time

**Current:** `rng_derivation_records` contains full artifact record objects (with file paths, content-addressed references) when present, and is popped when `artifact_writer is not None` for L3/L5.

**New:** A normalized RNG derivation summary (protocol, law/arm, draw role, seed, replicate/subdraw indexes, derived-key/digest, rejection/block/word counts, accepted-transform) is built directly from the RNG draw objects at draw time, independent of artifact writer state. This satisfies Rebecca's requirement that "RNG derivation summaries" be in the projection.

### 5. Top-level configuration block and two-digest architecture

**Current:** No configuration or top-level output fields are included in the reproducibility comparison.

**New:** A configuration block (projection version, mode, seeds, laws, protocol ID, null replicate count, alpha values, complete locked bars/thresholds/fixture sizes/seed constants, stochastic families, seed policy) is prepended to the compared digest payload. A two-digest architecture (§2.4) separates the compared scoring-semantic digest (per-law results + config only) from the non-compared final-report digest (everything, computed after reproducibility + artifact validation).

### 6. Output label

**Current:** `"bit_identical": True/False` with scope `"all non-timing fields"`.

**New:** `"certification": "bit-identical scoring-semantic reproducibility"` with `pass1_digest`, `pass2_digest`, `digests_equal`, projection schema version, invariant failures, and `final_report_digest`.

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
- D1–D5 (Persistence Doctrine): Specification committed to GitHub branch; no STATE.md or provenance_log.md modification.
- L9 (hard fence: no learned/nonlinear retrieval): Not touched.
- L18 (full battery on every claim): Not modified.
- ≥2 unseen scoring seeds: Not applicable (no scoring run authorized).
- No renaming negatives: INSTRUMENT FAILURE label retained.
- No L15/L16/L17 before M5: Not introduced.
- Rebecca sole gate/merge authority: Specification routes to CRITIC, then Rebecca gates.
