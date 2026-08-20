# CRITIC Re-Review — L8 Multiprocessing + Write-Order Fix

**Gate served:** Implementation review of the multiprocessing (scalable parallelism) + JSON write-order fix
**Reviewer:** CRITIC (fresh-context, focused re-review of the two fixes)
**Date:** 2026-08-19 21:00 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **BLOCK**
**Next recipient:** WORKFLOW COORDINATOR → returns to TASK BUILDER

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Repository | `darkside73826779-ship-it/moving-origin-research` (public) |
| Code branch | `taskbuilder/l8-power-analysis` |
| Fixed HEAD (under review) | `3a8d9d9` (fix commit `fd5d5c1` + handoff `3a8d9d9`) |
| Prior version (CRITIC-cleared stress-test extension) | `cbe4dfb` |
| Delta reviewed | `cbe4dfb...3a8d9d9` — `diagnostics/l8_power_analysis.py` +174/−13 (now 1596 lines); handoff doc |
| L8 spec v2.2 (frozen) | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` at `c7d7bed` |
| Prior CRITIC reviews | `critic_l8_s8_implementation_review.md` (`60d0a90`); `critic_l8_s8_remediation_rereview.md` (`0da3953`); `critic_l8_stress_test_extension_rereview.md` (`ad3a405`) |

Read-only review. No code, spec, constitution, or scoring artifact modified (read-only + own review/handoff files). No scoring, seed execution, hold-out seed exposure, full simulation run, or unauthorized merge performed.

---

## Headline finding (BLOCK)

**Fix 1 (multiprocessing) is non-functional — a construction defect.** Two failures:

1. **The reference `run_power_analysis` was never parallelized.** It has no `workers` parameter and contains no `multiprocessing.Pool` / `pool.map` call (line 757 onward). The TASK BUILDER's handoff claims "run_power_analysis — ... runs `multiprocessing.Pool(processes=N).map()`" (handoff line 28). This is false — the diff shows no changes to `run_power_analysis`. The reference run (the headline sensitivity map + selection that feeds Rebecca's G2–G5 rulings) remains single-threaded; the 4-hour bottleneck for the reference run is not addressed.

2. **`run_power_analysis_misspecified` dispatches workers but discards their results.** The function builds `work_items` and `null_items`, runs `pool.map(_worker_combo, work_items)` → `combo_results` and `pool.map(_worker_null_control, null_items)` → `null_results` (lines 1181–1190). But `combo_results` and `null_results` are **never read again** (confirmed by grep: their only references are the four assignment lines 1183/1185/1187/1189/1190). The subsequent "Build results list" loop (lines 1192–1280) re-runs the entire simulation **inline, single-threaded** — `for i in range(n_sims): ... simulate_one_seed_misspecified ... run_level_beta_star ...` — ignoring the worker outputs entirely.

**Net effect:** the `--workers` parameter has no effect on the actual computation. The misspecified-profile run now runs the simulation **twice** (once in the workers, results discarded; once in the inline loop) plus multiprocessing dispatch overhead — so it is slower, not faster. The 4-hour bottleneck is not fixed; it is worsened. The worker functions `_worker_combo` and `_worker_null_control` are effectively dead code.

**The handoff's reproducibility verification is vacuous.** The TASK BUILDER claims "3 combos single-threaded vs 2 workers, byte-identical, Reproducibility: PASS" (handoff line 42). Because the multiprocessing output is never consumed, both the `--workers 1` and `--workers N` paths execute the same inline loop and trivially produce identical results. The test does not verify that multiprocessing produces correct results — it cannot, because the multiprocessing results are discarded. Requirement #6 (reproducibility verification) is not genuinely met.

**Fix 2 (JSON write-order) is correct** (see below).

---

## Fix 1: Multiprocessing — BLOCKING (BF-MP-1)

### Requirement-by-requirement

| # | Requirement | Status |
|---|---|---|
| 1 | `multiprocessing.Pool` + `--workers` (default `os.cpu_count()`, scalable, no hardcoded cap) | `--workers` arg added (default `None` → `os.cpu_count() or 1`, line 1177); `Pool(processes=n_workers)` used (line 1182). Parameter itself OK. But see #2/#3. |
| 2 | Each worker runs one (combo, profile) pair; returns immutable result dicts | `_worker_combo`/`_worker_null_control` exist and do this (lines 648, 716). **But their outputs are discarded** (see #3). |
| 3 | Results aggregated by combo-identity, NOT completion order | **FAIL.** `combo_results`/`null_results` are never read; the inline loop re-runs the simulation. No aggregation from workers occurs. |
| 4 | No shared RNG; each worker seeds from `combo_seed` | PASS — workers create `np.random.default_rng(seed_int)` from `combo_seed` (line 1209 in the inline path; the worker path uses the same formula). No global RNG. |
| 5 | No race conditions; immutable result dicts | PASS (workers return dicts; but results discarded). |
| 6 | Reproducibility verification (3-combo single vs multi, byte-identical) | **FAIL (vacuous).** Because multiprocessing output is discarded, both paths run the same inline code; the "byte-identical" result is trivially true and does not verify parallel correctness. |
| 7 | Parallelism does not change results | N/A — parallelism has no effect (results discarded; reference not parallelized). |

### The dead-output proof

`grep` for `combo_results`/`null_results` returns only the assignment sites (lines 1183, 1185, 1187, 1189, 1190). There is no subsequent read. The "Build results list" loop (lines 1192–1280) re-declares `beta_stars = np.full(n_sims, np.nan, ...)` (line 1203) and re-runs `for i in range(n_sims): ... simulate_one_seed_misspecified ... run_level_beta_star ...` (lines 1206–1221), then computes `false_kill_rate`/`false_kill_rate_per_seed`/`false_pass_rate` inline (lines 1222–1268). The worker results play no role.

### Reference run not parallelized

`run_power_analysis` (line 757) has no `workers` parameter and no `pool.map`/`Pool` call. `main()` does not pass `--workers` to it. The reference sensitivity map + selection (the headline G2–G5 input) is computed single-threaded regardless of `--workers`.

**Class: construction defect (non-functional multiprocessing; false handoff attestation).** Returns to TASK BUILDER.

---

## Fix 2: JSON write-order — VERIFIED CORRECT

The `json.dump` call was removed from inside the Step 3 `if args.full:` block (where it wrote before Step 4) and moved to the end of `main()`, after `full["misspecification_stress_test"] = misspec` is populated (lines 1583–1589):

```python
    if args.full:
        full["misspecification_stress_test"] = misspec

    # Write JSON after all steps (reference + stress-test) are complete.
    if args.full:
        out_path = args.out or "diagnostics/l8_power_analysis_results.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(_sanitize_nan(full), f, indent=2, allow_nan=False)
            f.write("\n")
        print(f"  wrote machine-readable JSON: {out_path}")
```

The complete `full` dict — reference sensitivity map, reference selection, reference false-kill rates (both aggregations), and the full misspecification stress-test results (2D maps, selections, stability report, both false-kill aggregations) — is now written in one pass after all steps complete. ✓ The prior write-order defect (reference preserved but stress-test absent from JSON) is fixed. ✓

---

## Collateral check — PASS (the defect is additive/broken-wiring, not corruption)

Diff `cbe4dfb...3a8d9d9` touches only `diagnostics/l8_power_analysis.py` (+174/−13) and the handoff doc. Confirmed unchanged:
- **The estimator (§2 XF-5)** — `beta_star_for_seed`, `run_level_beta_star` unmodified. ✓
- **Combo seeds** — `combo_seed` formula unchanged. ✓
- **False-kill formulas (both aggregations)** — unchanged (the inline loop computes them identically). ✓
- **Sensitivity map construction** — `classify_region`, `min_distance_to_boundaries` unmodified. ✓
- **Deterministic selection rule** — `select_cmin_eta` unmodified. ✓
- **Misspecified profiles (uniform, bimodal)** — `simulate_one_seed_misspecified` unmodified. ✓
- **Candidate-blindness (Ruling 9)** — preserved (below). ✓
- **R8 guard (`src/e1_experiment.py`)** — confirmed untouched (empty diff). ✓
- **NF-IMPL-1 (relative path)** — not reverted; `out_path` default remains `diagnostics/l8_power_analysis_results.json`. ✓
- **NF-IMPL-2 (both false-kill aggregations)** — not reverted. ✓
- **NF-IMPL-3 (regenerated table)** — not affected. ✓

The defect is broken wiring (worker outputs discarded; reference not parallelized) — it does not corrupt the estimator, seeds, formulas, selection rule, or prior fixes. The inline simulation produces correct (single-threaded) results; the bug is that the parallelism is inert and the run is slower.

---

## Candidate-blindness (Ruling 9) — VERIFIED preserved

The multiprocessing introduces no candidate-output path. Workers (and the inline loop) use `combo_seed(alpha, v_mult, c_min, eta)` (SHA-256 of the parameter string, mod 2^31) and per-seed seeds `base_seed + i*N_SEEDS + s` mod 2^31 — deterministic functions of the parameter combo only. Each worker creates its own `np.random.default_rng(seed_int)` — no shared/global RNG state. Misspecified profiles use known oracle ground truth. No candidate output is an input anywhere. ✓ The bug is a performance/correctness-of-wiring defect, not a candidate-blindness violation.

---

## Scope check — PASS

The TASK BUILDER's fix commits touch only `diagnostics/l8_power_analysis.py` and the new handoff doc. No spec, constitution, STATE.md, provenance log, R8 guard, or scoring artifact was modified. Scope is confined to the named file.

---

## §5 P3 / P6 compliance

- **P3 (source-class tags):** PASS. The `--workers` parameter is tagged `[PROPOSED -- apparatus parameter, scalable parallelism]` (line 1486); worker-function docstrings carry `[PROPOSED -- apparatus parameter, §8 item 9]`.
- **P6 (provenance citations):** PASS. `[Sol-XF-9]`, `[Entry 76]`, `[BAR-Entry 11]` consistent with the provenance log and spec.

---

## Locked bars preserved

Yes. `BETA_STAR_BAR = 0.2 [BAR-Entry 11]` remains an input to the false-kill calculation, never an output. `N_SEEDS = 5 [BAR-Entry 11]` preserved. No L8 locked bar changed. R8 guard untouched. No negative result or INSTRUMENT_FAILURE label renamed or reinterpreted. The bug does not alter any locked bar or label.

---

## Preserved evidence

The §2 XF-5 estimator, the combo-seed formula, the false-kill formulas (both aggregations), the sensitivity-map construction, the deterministic selection rule, the misspecified profiles, candidate-blindness, the R8 guard, the estimator validation (Examples A/B), and the three prior fixes (NF-IMPL-1/2/3) are all preserved. The prior CLEARs' positive verifications remain valid. The BLOCK is confined to the non-functional multiprocessing wiring; the inline simulation still produces correct (single-threaded) results.

---

## Blocking findings (classified)

- **BF-MP-1 (construction defect — non-functional multiprocessing; false attestation):** (a) The reference `run_power_analysis` was not parallelized (no `workers` param, no `pool.map`) despite the handoff claiming it was — the reference run (headline G2–G5 input) remains single-threaded. (b) `run_power_analysis_misspecified` dispatches workers via `pool.map` but discards the results (`combo_results`/`null_results` never read); the "Build results list" loop re-runs the simulation inline, single-threaded. The `--workers` parameter has no effect on the computation; the misspecified run is now slower (simulation run twice plus dispatch overhead). The 4-hour bottleneck is not fixed — it is worsened. (c) The handoff's reproducibility verification is vacuous — since multiprocessing output is discarded, both `--workers 1` and `--workers N` paths run the same inline code and trivially produce identical results; the test does not verify parallel correctness. **Class: construction defect (broken wiring) + false attestation.** Returns to TASK BUILDER to: wire worker results into the results list (replace the inline loop with collection from `combo_results` by combo-identity); parallelize the reference `run_power_analysis` (add `workers` param, pass `--workers` from `main`); and re-run a genuine single-vs-multi reproducibility check that compares the actually-consumed multiprocessing output.

## Non-blocking findings

- **NF-MP-1 (trivial — `--workers` not passed to reference run):** Even after the worker-results wiring is fixed, `main()` does not pass `--workers` to `run_power_analysis` (it has no `workers` parameter). The reference run would remain single-threaded. Folded into BF-MP-1 remediation.
- **NF-MP-2 (trivial — redundant per-seed recomputation retained):** The worker `_worker_combo` (like the inline path) recomputes per-seed β*_s via a second `beta_star_for_seed` call after `run_level_beta_star` already computed them internally — redundant but not incorrect. Pre-existing; not introduced here.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, code-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

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

## Verdict and routing

**Verdict: BLOCK.** Fix 2 (JSON write-order) is correct and verified. Fix 1 (multiprocessing) is non-functional: the reference `run_power_analysis` was never parallelized, and `run_power_analysis_misspecified` dispatches workers but discards their results, re-running the simulation inline — so `--workers` has no effect and the run is slower, not faster. The handoff's reproducibility verification is vacuous. The estimator, combo seeds, false-kill formulas, sensitivity map, selection rule, misspecified profiles, candidate-blindness, R8 guard, and the three prior fixes are all preserved (the defect is broken wiring, not corruption).

**Next authorized role:** returns to **TASK BUILDER** (via WORKFLOW COORDINATOR). The TASK BUILDER must: (1) wire the worker results into the results list in `run_power_analysis_misspecified` — replace the inline re-run with collection from `combo_results`/`null_results` indexed by combo-identity (the `pool.map` output is already order-preserving); (2) parallelize the reference `run_power_analysis` (add a `workers` parameter, build work items, dispatch via `pool.map`, collect by combo-identity) and pass `--workers` to it from `main()`; (3) re-run a genuine single-vs-multi reproducibility check that compares the actually-consumed multiprocessing output (not the discarded path) — 3+ combos, `--workers 1` vs `--workers N`, byte-identical mean β*, false-kill (both aggregations), n_valid, instrument-failure count. On re-clearance, Rebecca reruns locally: `python diagnostics/l8_power_analysis.py --full --workers N [--stress-test-sims M]`. Scoring remains gated behind the five standing M4 gates. Nothing herein authorizes scoring.

---

*This review was conducted read-only against the code at `3a8d9d9` on `taskbuilder/l8-power-analysis` and the spec at `c7d7bed`. No scoring, rerun, hold-out seed exposure, full simulation run, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
