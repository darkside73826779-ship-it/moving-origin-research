# CRITIC Handoff — M3 Reproducibility-Contract Implementation Verification

**Gate served:** M3 reproducibility-contract implementation verification (TASK BUILDER → CRITIC)
**Date:** 2026-08-17 14:06 EDT
**Verdict:** BLOCK

---

## Inputs/SHAs reviewed

| Item | SHA | Source |
|---|---|---|
| GitHub main (base) | `a5e8a15` | Verified on GitHub |
| TASK BUILDER branch | `taskbuilder/m3-reproducibility-contract` | Verified on GitHub |
| TASK BUILDER result SHA | `34dd17b` | Branch HEAD (verified via GitHub API) |
| Spec content SHA | `3c8480c` | `architect/m3-reproducibility-contract`; CRITIC-cleared v1.1 |

**Files reviewed:**

| File | Size | Source |
|---|---|---|
| `src/m3_reproducibility.py` | 961 lines | Fetched from `34dd17b` |
| `src/m3_harness.py` (modified) | 4380 lines (+126 from base 4254) | Fetched from `34dd17b`; diffed against base `a5e8a15` |
| `src/test_m3_reproducibility.py` | 824 lines | Fetched from `34dd17b` |
| `handoffs/TASKBUILDER_M3_REPRODUCIBILITY_CONTRACT_HANDOFF.md` | 75 lines | Fetched from `34dd17b` |
| `src/M3_REPRODUCIBILITY_CONTRACT_CHANGES.md` | 66 lines | Fetched from `34dd17b` |

---

## Verdict: BLOCK

One blocking finding. The implementation is substantively correct and faithful to the spec across nearly all dimensions. The blocking finding is a narrow spec-fidelity issue with zero practical impact in normal operation, but it violates the spec's explicit optionality requirement for Classification B fields.

---

## Blocking findings

### BF1 — `v44_artifact_support` required for L3 and L5 despite being Classification B (spec fidelity)

**Spec violation:** Spec §4.1 states: "Classification B fields are treated as optional: the projection function must accept their presence or absence without error." Spec §2.5 Classification B lists `v44_artifact_support` as optional.

**Implementation reality:**
- **L1:** Correctly treats `v44_artifact_support` as optional. It's in `_L1_TOP_LEVEL_B` and checked via `if key in _L1_TOP_LEVEL_A or key in _L1_TOP_LEVEL_B: continue`. Not in any required set. ✓
- **L3:** INCORRECTLY requires `v44_artifact_support`. Line 732 of `m3_reproducibility.py`:
  ```python
  _check_required(path, law_result, frozenset({'empty', 'v44_stochastic_controls', 'v44_artifact_support'}))
  ```
  If `v44_artifact_support` is absent, `ReproducibilityProjectionError` is raised with `MISSING_REQUIRED_FIELD`.
- **L5:** INCORRECTLY requires `v44_artifact_support`. Lines 761-765:
  ```python
  _l5_required_arms = frozenset({
      'candidate', 'fair_naive', 'frozen', 'oracle', 'permuted',
      'shuffled', 'full_scan', 'empty', 'v44_stochastic_controls',
      'v44_artifact_support',
  })
  ```

**Empirical verification:** Ran `compute_scoring_semantic_digest` with a synthetic L3 result dict lacking `v44_artifact_support`. Result: `ReproducibilityProjectionError: Unclassified field at '101.L3.v44_artifact_support' (type=MISSING_REQUIRED_FIELD)`.

**Practical impact:** Zero in normal operation — the harness always produces `v44_artifact_support` in both passes. However, the projection function must be robust to its absence per spec §4.1.

**Required fix (TASK BUILDER scope):** Remove `v44_artifact_support` from required sets for L3 and L5. Accept its presence or absence as Classification B, matching the L1 pattern.

---

## Non-blocking findings

### NF1 — Classification C field absence correctly handled

Verified: L1 results without `abs_rho_null_1000` and `null_max_1000` (Classification C) are accepted without error. Invariant checks only run when fields are present (matching the "if present" pattern). The harness retention fix ensures these fields are present in practice. Not a spec violation — the spec's §4.2 "must be retained" is a harness instruction, not a fail-closed requirement.

### NF2 — TASK BUILDER handoff SHA discrepancy

TASK BUILDER's handoff claims branch HEAD `e9c04a3`, but the actual branch HEAD is `34dd17b` (additional commits pushed after handoff was written). Code at `34dd17b` was reviewed.

### NF3 — Changes note line count discrepancy

Changes note says `m3_reproducibility.py` is 839 lines; actual file is 961 lines. Changes note may reflect an earlier version.

### NF4 — Changes note classification error

Changes note lists `abs_rho_null_1000` and `null_max_1000` as "Classification A fields" in the pruning fix description. They are Classification C. The implementation correctly classifies them; only the note is inaccurate.

### NF5 — Additional label fix beyond spec scope

TASK BUILDER also fixed `scoring_seed_policy` in the results config (line 4207), which was not in spec §6.1's three-label scope. Consistent and correct — same hardcoded value, same mode-aware fix.

### NF6 — Cross-slot identity applied to pass 2

`_v44_verify_l1_cross_slot_identity` is applied to pass 2 results (harness line ~4105). Not explicitly specified in the spec, but necessary for digest match — pass 1 gets this post-processing, pass 2 needs it too. Correct implementation decision.

### NF7 — `v44_artifact_support` present in both passes

As noted in spec re-review NF5, `v44_artifact_support` is present in both passes with different values (not "present in pass 1, absent in pass 2" as the spec states). The implementation correctly excludes it from the digest as Classification B.

---

## Verified correct (implementation matches spec v1.1)

1. **Canonical serialization (§3.3):** NFC normalization, `ensure_ascii=True`, `sort_keys=True`, `separators=(',', ':')`, `allow_nan=False`, SHA-256, NumPy `.item()`, float finiteness check. ✓
2. **Classification tables (§2.5–§2.8):** All L1, L3, L5, L6 fields match spec. `abs_rho_null_1000` and `null_max_1000` are Classification C only (BF2 resolution). ✓
3. **Classification C invariants (§2.5):** `rho_null_1000_values` uses `[abs(x) for x in signed_rhos] == null_statistics` (BF1 resolution). `r_squared_null_1000`, `abs_rho_null_1000`, `null_max_1000` invariants correct. ✓
4. **Two-digest architecture (§2.4, §3.1, §3.2):** Compared digest (per-law + config only); final-report digest (non-compared, after overall verdict, cannot affect it). ✓
5. **Fail-closed traversal (§3.4):** Unknown fields, missing required fields, missing containers/families, nested list-item schema checks, RNG summary record checks. "Where present" fields handled via optional sets. ✓
6. **Pruning fix (§4.2):** Only Classification B fields (`raw_draw_manifest_refs`, `rng_derivation_records`) are popped. All A and C fields retained regardless of `artifact_writer` state. ✓
7. **RNG derivation summaries (§2.5):** Built at draw time via `rng_artifact_records`, present in both passes, independent of `artifact_writer`. ✓
8. **Harness integration:** `_build_reproducibility_config` with all locked bars (§2.3). `_non_timing_projection` retained (backward compat). Variable shadowing fix (`permuted_null_rhos_signed`). Final-report digest integrated after overall verdict. Output structure matches §4.3. ✓
9. **Stale label fixes (§6):** `mode_label(mode, key)` for all three spec keys + additional `scoring_seed_policy`. Scoring and development mode strings match spec §6.2 exactly. ✓
10. **Mutation tests (§5):** 34 tests, ALL PASS. §5.1 leaf traversal (L1/L3/L5/L6), §5.2 fail-closed + C invariants, §5.3 non-digest, §5.4 final-report, §6.3 stale labels. Note: tests run with `m3_harness` import stubbed (harness dependencies not available in sandbox); harness integration verified via code inspection. ✓
11. **No unauthorized changes:** No locked bars, thresholds, or scoring predicates modified. No candidate-facing bars changed. No STATE.md or provenance_log.md modified. No L15/L16/L17 introduced. No M4 components. ✓
12. **O-15 compliance:** Only seed 101 development diagnostic used. No scoring or held-out seed execution. ✓

---

## Preserved evidence

- Base SHA `a5e8a15` verified on GitHub.
- TASK BUILDER branch `taskbuilder/m3-reproducibility-contract` at `34dd17b` verified on GitHub.
- Harness diff (base `a5e8a15` → `34dd17b`) fully reviewed — all changes match spec scope.
- `m3_reproducibility.py` (961 lines) fully read and verified against spec v1.1.
- Test suite (34 tests) independently executed — all pass.
- Classification B optionality empirically tested (L3 fails, L1 passes).
- Classification C retention empirically tested (passes — absence accepted).
- INSTRUMENT FAILURE label retained — not renamed or reinterpreted.
- No scoring run, seed execution, or hold-out seed exposure occurred.

---

## Exact next authorized role

**TASK BUILDER** — Fix BF1 (remove `v44_artifact_support` from required sets for L3 and L5), re-run tests, re-submit for CRITIC verification.

---

## Explicitly prohibited actions

- No modification of any locked bar, threshold, or scoring predicate.
- No running of any scoring seeds.
- No running of seeds 201–203 or 301–303.
- No implementing L7/L8/L10 or any M4 component.
- No modifying `STATE.md` or `docs/rulings/provenance_log.md` (RECORDER/INTEGRATOR custody).
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- No merging to main (Rebecca sole merge authority).

---

## Confirmation

No scoring, rerun of failed scoring, hold-out seed exposure, or unauthorized merge occurred during this review. The CRITIC reviewed the implementation read-only and did not modify any specification, implementation, scoring artifact, or STATE.md.

Standing constraints verified: O-14 (no re-run-on-failure) — not applicable; O-15 (development runs diagnostic-only) — TASK BUILDER used only seed 101 diagnostic; D1–D5 (Persistence Doctrine) — implementation on GitHub branch, no STATE.md or provenance_log.md modification; L9 (hard fence) — not touched; L18 (full battery) — not modified; no L15/L16/L17 introduced; Rebecca sole gate/merge authority — no merge performed or requested.
