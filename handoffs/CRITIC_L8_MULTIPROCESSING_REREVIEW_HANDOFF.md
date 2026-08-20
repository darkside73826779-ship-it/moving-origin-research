# CRITIC Handoff — Return to WORKFLOW COORDINATOR: Multiprocessing + Write-Order Re-Review

**From:** CRITIC (fresh-context, focused re-review of the two fixes)
**To:** WORKFLOW COORDINATOR
**Date:** 2026-08-19 21:00 EDT
**Gate served:** Implementation review of the multiprocessing (scalable parallelism) + JSON write-order fix
**Verdict:** **BLOCK**
**Review artifact:** `reviews/critic_l8_multiprocessing_rereview.md` on `critic/l8-multiprocessing-rereview` (SHA below)

---

## Authorization context

The §8 power analysis ran successfully but had two defects: (1) single-threaded execution (4-hour bottleneck), and (2) a JSON write-order bug (stress-test results attached in memory after JSON was written → committed artifact incomplete). The TASK BUILDER claimed both fixed. This handoff returns the CRITIC's focused re-review.

---

## SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Code branch | `taskbuilder/l8-power-analysis` |
| Fixed HEAD (under review) | `3a8d9d9` (fix commit `fd5d5c1` + handoff `3a8d9d9`) |
| Prior version (CRITIC-cleared stress-test extension) | `cbe4dfb` |
| Delta reviewed | `cbe4dfb...3a8d9d9` — `diagnostics/l8_power_analysis.py` +174/−13 (now 1596 lines); handoff doc |
| L8 spec v2.2 (frozen) | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` at `c7d7bed` |
| Prior CRITIC reviews | `critic_l8_s8_implementation_review.md` (`60d0a90`); `critic_l8_s8_remediation_rereview.md` (`0da3953`); `critic_l8_stress_test_extension_rereview.md` (`ad3a405`) |

---

## Verdict: BLOCK

**Fix 1 (multiprocessing) is non-functional — a construction defect. Fix 2 (write-order) is correct.**

---

## Blocking finding (BF-MP-1)

**Multiprocessing does not work; the handoff's claims are false.** Two failures:

1. **The reference `run_power_analysis` was never parallelized.** It has no `workers` parameter and no `multiprocessing.Pool`/`pool.map` call (line 757 onward). The handoff claims "run_power_analysis — ... runs `multiprocessing.Pool(processes=N).map()`" — this is false; the diff shows no changes to `run_power_analysis`. The reference run (headline sensitivity map + selection feeding Rebecca's G2–G5) remains single-threaded; the 4-hour bottleneck for the reference run is not addressed.

2. **`run_power_analysis_misspecified` dispatches workers but discards their results.** It runs `pool.map(_worker_combo, work_items)` → `combo_results` and `pool.map(_worker_null_control, null_items)` → `null_results` (lines 1181–1190), but `combo_results`/`null_results` are **never read again** (grep confirms only the assignment sites). The subsequent "Build results list" loop (lines 1192–1280) re-runs the entire simulation **inline, single-threaded**, ignoring the worker outputs.

**Net effect:** the `--workers` parameter has no effect on the computation. The misspecified-profile run now runs the simulation **twice** (once in workers, discarded; once inline) plus dispatch overhead — slower, not faster. The 4-hour bottleneck is worsened, not fixed. The worker functions `_worker_combo`/`_worker_null_control` are effectively dead code.

**The handoff's reproducibility verification is vacuous.** Because multiprocessing output is discarded, both `--workers 1` and `--workers N` paths run the same inline code and trivially produce identical results. The "byte-identical, Reproducibility: PASS" claim does not verify parallel correctness — it cannot, because the multiprocessing results are never consumed.

---

## Fix 2 (write-order) — VERIFIED CORRECT

The `json.dump` was moved from inside the Step 3 `if args.full:` block to the end of `main()`, after `full["misspecification_stress_test"] = misspec` is populated. The complete `full` dict (reference + stress-test) is now written in one pass. The prior write-order defect is fixed. ✓

---

## Collateral check — PASS (defect is broken wiring, not corruption)

Only `diagnostics/l8_power_analysis.py` (+174/−13) + handoff doc touched. Confirmed unchanged: the estimator (`beta_star_for_seed`, `run_level_beta_star`), combo seeds (`combo_seed` formula), false-kill formulas (both aggregations), sensitivity map (`classify_region`, `min_distance_to_boundaries`), selection rule (`select_cmin_eta`), misspecified profiles (`simulate_one_seed_misspecified`), candidate-blindness, the R8 guard (`src/e1_experiment.py` — empty diff), and the three prior fixes (NF-IMPL-1 relative path, NF-IMPL-2 both aggregations, NF-IMPL-3 regenerated table). The inline simulation still produces correct single-threaded results; the bug is that parallelism is inert.

---

## Candidate-blindness (Ruling 9) — VERIFIED preserved

The multiprocessing introduces no candidate-output path. Workers and the inline loop use `combo_seed` (SHA-256 of parameter string, mod 2^31) and per-seed seeds `base_seed + i*N_SEEDS + s` mod 2^31 — deterministic functions of the parameter combo only. Each worker creates its own `np.random.default_rng(seed_int)` — no shared/global RNG. Misspecified profiles use known oracle ground truth. No candidate output is an input anywhere. The bug is a performance/wiring defect, not a candidate-blindness violation. ✓

---

## P3 / P6 compliance

- **P3:** PASS — `--workers` tagged `[PROPOSED -- apparatus parameter, scalable parallelism]`; worker docstrings tagged.
- **P6:** PASS — `[Sol-XF-9]`, `[Entry 76]`, `[BAR-Entry 11]` consistent with provenance log and spec.

---

## Locked bars preserved

Yes — `BETA_STAR_BAR = 0.2 [BAR-Entry 11]` remains an input (never an output); `N_SEEDS = 5 [BAR-Entry 11]` preserved; no L8 locked bar changed; R8 untouched; INSTRUMENT_FAILURE label preserved.

---

## Preserved evidence

Estimator, combo seeds, false-kill formulas, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, estimator validation, and the three prior fixes all preserved. Prior CLEARs' positive verifications remain valid.

---

## Non-blocking findings

- **NF-MP-1 (trivial):** `main()` does not pass `--workers` to `run_power_analysis` (no `workers` param). Even after wiring is fixed, the reference run would remain single-threaded unless parallelized. Folded into BF-MP-1 remediation.
- **NF-MP-2 (trivial):** Worker `_worker_combo` (like the inline path) recomputes per-seed β*_s via a second `beta_star_for_seed` call after `run_level_beta_star` already computed them internally — redundant but not incorrect. Pre-existing.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this handoff artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, code-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the code, spec, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No scoring, seed execution, or hold-out seed exposure.
- No running of the full simulation (deferred to Rebecca's local run after clearance).
- No L15/L16/L17 before M5.
- No renaming or reinterpreting any negative result or INSTRUMENT_FAILURE label.
- No touching the estimator, combo seeds, false-kill formulas, sensitivity map, selection rule, misspecified profiles, R8 guard, or the relative-path fix (all confirmed unchanged).
- No introducing non-determinism (none introduced — the bug is inert multiprocessing, not non-determinism).

---

## Next authorized role / routing

**Next recipient:** WORKFLOW COORDINATOR → returns to **TASK BUILDER**.

The TASK BUILDER must:
1. **Wire worker results into the results list** in `run_power_analysis_misspecified` — replace the inline re-run with collection from `combo_results`/`null_results` indexed by combo-identity (`pool.map` output is already order-preserving).
2. **Parallelize the reference `run_power_analysis`** — add a `workers` parameter, build work items, dispatch via `pool.map`, collect by combo-identity. Pass `--workers` to it from `main()`.
3. **Re-run a genuine single-vs-multi reproducibility check** comparing the actually-consumed multiprocessing output (not the discarded path) — 3+ combos, `--workers 1` vs `--workers N`, byte-identical mean β*, false-kill (both aggregations), n_valid, instrument-failure count.

On re-clearance, Rebecca reruns locally: `python diagnostics/l8_power_analysis.py --full --workers N [--stress-test-sims M]`, producing the complete artifact with both reference and stress-test results feeding her G2–G5 gate rulings. Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On BLOCK (this case), returns to TASK BUILDER.

---

*This handoff was produced read-only against the code at `3a8d9d9` on `taskbuilder/l8-power-analysis` and the spec at `c7d7bed`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
