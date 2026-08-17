# CRITIC Handoff — M3 Reproducibility-Contract Specification v1.1 Re-Review

**Gate served:** M3 reproducibility-contract specification re-review (ARCHITECT v1.1 → CRITIC)
**Date:** 2026-08-17 13:47 EDT
**Verdict:** CLEAR

---

## Inputs/SHAs reviewed

| File | SHA | Source |
|---|---|---|
| `specs/m3_reproducibility_contract_v1.md` | `3c8480c` | GitHub branch `architect/m3-reproducibility-contract`; matches uploaded attachment (diff verified clean) |
| `specs/m3_reproducibility_contract_changelog.md` | `3c8480c` | GitHub branch; matches uploaded attachment |
| `handoffs/ARCHITECT_M3_REPRODUCIBILITY_CONTRACT_HANDOFF.md` | `af6678a` (branch HEAD) | GitHub branch |
| `src/m3_harness.py` | `f9d16fa` | GitHub main (fetched and verified in prior review) |
| `src/m3_v44_artifacts.py` | `f9d16fa` | GitHub main (fetched and verified in prior review) |
| `reviews/critic_m3_reproducibility_contract_spec_review.md` | local checkout | CRITIC v1.0 review (BLOCK, BF1–BF4) |

**Base SHA:** `f9d16fa` (GitHub main) — verified.

**Reviewed spec content SHA:** `3c8480cc163251f88db2b70b921f65a31468cc17` — exists on GitHub, in branch history.

**Branch HEAD:** `af6678a9809de5abfeb30505c52e50f09a48ffeb` — one commit ahead of `3c8480c`. The delta (`3c8480c...af6678a`) modifies only `handoffs/ARCHITECT_M3_REPRODUCIBILITY_CONTRACT_HANDOFF.md` (84 line changes). The spec files and changelog are identical at both commits. The branch HEAD is a handoff re-issue, not a spec change.

---

## Verdict: CLEAR

All four blocking findings (BF1–BF4) from the v1.0 review are resolved. All four non-blocking findings (NF1–NF4) are addressed. No new blocking findings introduced. The specification is approved for TASK BUILDER implementation.

---

## BF1–BF4 resolution verification

### BF1 — Classification C invariant #1 corrected — RESOLVED

**Spec v1.1 §2.5 Classification C (line 264):** The invariant is now `[abs(x) for x in rho_null_1000_values] == null_statistics` element-wise.

**Code verification (at `f9d16fa`):**
- Line 2455: `null_rhos.append(rho)` — `rho_null_1000_values` stores signed Spearman rho values
- Line 2466: `abs_null_rhos = [abs(value) for value in null_rhos]`
- Line 2467–2468: `_v44_summary(abs(observed_rho), abs_null_rhos, ...)` — `null_statistics` = `abs_null_rhos`
- Line 2615: `results['permuted']['rho_null_1000_values'] = null_rhos` (signed)

The invariant `[abs(x) for x in null_rhos] == abs_null_rhos` is mathematically correct. The signed vector and its absolute-valued derivative are properly distinguished. The mutation test (§5.2 line 516) correctly tests the invariant with `[abs(x) for x in rho_null_1000_values] != null_statistics`.

### BF2 — Classification A/C overlap eliminated — RESOLVED

**Spec v1.1 §2.5 (line 211):** "Note: `abs_rho_null_1000` and `null_max_1000` are NOT in Classification A — they are Classification C derived duplicates."

Verified: Neither field appears in the Classification A family-specific extras (lines 206–209). Both appear ONLY in the Classification C table (lines 266–267). §2.2 (line 86) now explicitly states "No field may appear in more than one classification." §4.2 (line 450) correctly notes these fields must be retained for invariant checking but are not independently digested.

### BF3 — Two-digest architecture — RESOLVED

**Spec v1.1 §2.4 (lines 120–155):** Two distinct digests:

1. **Digest 1 (compared):** Per-law results + configuration only. `compute_scoring_semantic_digest(results, config)` (§3.1 line 399) explicitly does NOT accept `overall_verdict`, `interface_invariants`, `finite_numeric_results`, `l20_self_test`, or `raw_artifact_validation`. These are excluded because they are either computed after the reproducibility check or not re-computed in pass 2.

2. **Digest 2 (non-compared):** `compute_final_report_digest(...)` (§3.2 line 411) is computed once after reproducibility and artifact validation. Contains the compared digest payload + reproducibility result + all top-level output fields. Does NOT affect `overall_verdict`.

**Code verification:** The execution order in `main()` at `f9d16fa` confirms:
- `interface_invariants` (line 3930), `finite_numeric_results` (line 3935), `l20_self_test` (line 3979) are computed before the reproducibility check
- `raw_artifact_validation` (line 4027) and `overall_verdict` (lines 4053–4063) are computed after
- The second pass (lines 3984–3998) only re-runs law functions, not top-level computations

The two-digest architecture correctly avoids circularity: `overall_verdict` depends on the reproducibility result, so it cannot be an input to the digest that determines reproducibility.

### BF4 — Branch pushed to GitHub; SHA verified — RESOLVED

- Branch `architect/m3-reproducibility-contract` exists on GitHub
- Result SHA `3c8480c` exists and is in branch history
- Uploaded spec matches remote spec at `3c8480c` (diff verified clean)
- Branch HEAD is `af6678a` (one commit ahead — handoff re-issue only, no spec changes)

---

## NF1–NF4 resolution verification

- **NF1/NF4:** §3.3 documents `ensure_ascii=True` rationale and NFC belt-and-suspenders note. RESOLVED.
- **NF2:** §2.5 (line 247) and §3.4 (line 430) clarify "where present" fields are conditionally absent without triggering fail-closed. RESOLVED.
- **NF3:** `rho_null_1000_values` retained as Classification C with corrected absolute-value invariant. RESOLVED.

---

## Non-blocking findings

### NF5 — `v44_artifact_support` presence description inaccurate

**Spec v1.1 §2.5 Classification B (line 253):** States `v44_artifact_support` is "Optional: present in pass 1, absent in pass 2."

**Code reality:** `v44_artifact_support` is present in BOTH passes, with different values:
- Pass 1: `status = 'complete_streaming_raw_artifacts'`, `full_per_draw_raw_schema_complete = True`
- Pass 2: `status = 'in_memory_test_mode'`, `full_per_draw_raw_schema_complete = False`

The field is correctly excluded as Classification B and its differing values do not affect the digest (since it's not digested). But the "present in pass 1, absent in pass 2" rationale is inaccurate. The TASK BUILDER should be aware that `v44_artifact_support` differs between passes (not absent in pass 2). The Classification B exclusion still works correctly regardless.

### NF6 — Final-report digest behavior when reproducibility not checked

**Spec v1.1 §4.3 (lines 480–488):** When `--verify-reproducibility` is not requested, the output includes `final_report_digest`. The spec does not explicitly specify what the final-report digest payload contains in this case (no `pass1_digest`, `pass2_digest`, or `digests_equal` values exist). The TASK BUILDER should clarify whether these are set to `null` or omitted from the final-report digest payload.

### NF7 — `compute_final_report_digest(...)` parameter list

The function signature uses `...` (§3.2 line 411). The spec describes what it accepts (compared digest payload, reproducibility result, top-level output fields) but leaves the exact parameter list to the TASK BUILDER. This is acceptable for a design spec.

---

## Preserved evidence

- All v1.0 verified evidence remains valid (base SHA `f9d16fa` unchanged, all line-number references match, all field differences confirmed, all function structures verified).
- BF1 invariant correction verified mathematically against code.
- BF2 classification overlap eliminated — every field in exactly one classification.
- BF3 two-digest architecture verified against code execution order — no circularity.
- BF4 branch and result SHA verified on GitHub; uploaded spec matches remote.
- No bars, controls, or scoring logic modified by the specification.
- No scoring run, seed execution, or hold-out seed exposure occurred.
- INSTRUMENT FAILURE label retained — not renamed or reinterpreted.
- v1.0 review findings (BF1–BF4, NF1–NF4) fully addressed.

---

## Exact next authorized role

**TASK BUILDER** — Implement the approved specification:
1. `compute_scoring_semantic_digest(results, config)` — Classification A extraction, Classification C invariant checks, fail-closed traversal, canonical digest
2. `compute_final_report_digest(...)` — Non-compared integrity hash
3. Classification A field retention before artifact-mode pruning
4. Normalized RNG derivation summaries built at draw time
5. Mode-aware label helper (`_mode_label(mode, key)`)
6. Mutation tests (§5.1–§5.4)
7. Stale label regression tests (§6.3)

After TASK BUILDER implementation: **CRITIC** (verify implementation) → **RECORDER/INTEGRATOR** (publish).

---

## Explicitly prohibited actions

- No modification of any locked bar, threshold, or scoring predicate.
- No running of any scoring seeds.
- No running of seeds 201–203 or 301–303.
- No implementing L7/L8/L10 or any M4 component.
- No modifying `STATE.md` or `docs/rulings/provenance_log.md` (RECORDER/INTEGRATOR custody).
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- No L15/L16/L17 before M5.

---

## Confirmation

No scoring, rerun of failed scoring, hold-out seed exposure, or unauthorized merge occurred during this review. The CRITIC reviewed the specification read-only and did not modify any specification, implementation, scoring artifact, or STATE.md.

Standing constraints verified: O-14 (no re-run-on-failure) — not applicable; O-15 (development runs diagnostic-only) — mutation tests specified as diagnostic with synthetic fixtures or seeds 101–105; D1–D5 (Persistence Doctrine) — specification committed to GitHub branch, no STATE.md or provenance_log.md modification; L9 (hard fence) — not touched; L18 (full battery) — not modified; ≥2 unseen scoring seeds — not applicable (no scoring run authorized); no L15/L16/L17 introduced; Rebecca sole gate/merge authority — specification routes to TASK BUILDER, then CRITIC verification, then Rebecca gates.
