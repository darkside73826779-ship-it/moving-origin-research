# ARCHITECT Handoff — L8 Instantiation Spec v2 (Narrowed Claim + XF-4–XF-9 + Riders)

**Gate served:** Item 3 of Principal's L8 cross-family review routing directive — spec v2
**Issued by:** ARCHITECT
**Date:** 2026-08-19 01:30 EDT
**Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)

---

## SHAs

| Item | SHA | Location |
|---|---|---|
| Base (v1 on main) | `e8c7386` | `main` |
| v2 HEAD | (to be verified after push) | `architect/l8-instantiation-v2` |

## Files

| File | Description |
|---|---|
| `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` | L8 instantiation spec v2 (340 lines) |
| `reviews/l8_crossfamily_review/06_l8_instantiation_spec_changelog.md` | Changelog (65 lines) |

## Summary of changes

### §1/§10 — Narrowed claim (Entry 81)
L8 pass certifies externally-closed selective-risk regulation dependent on mirror relative to pre-registered control set. Damasio/Seth demoted to motivation. Three-control panel: memory + feedback-channel + task-difficulty. `[Entry 81]` (P5-authorized)

### XF-4 — Level-0 rule split (§2)
Apparatus-validity conditions (INSTRUMENT_FAILURE) separated from candidate baseline check (candidate FAIL — "not eligible for dose-response pass"). No relabeling. `[Sol-XF-4]`

### XF-5 — Exact slope estimator (§2)
Full equation: regression of D on dose, standardized by pooled within-dose SD of window-level deviations. Zero-variance → INSTRUMENT_FAILURE. Two synthetic validation examples. `[Sol-XF-5]`

### XF-6 — Specificity estimand (§6)
Slope-difference Δβ = β*(candidate) − β*(control), same units. All-seeds-direction + pooled bootstrap 95% CI. Three-condition conjunction for PASS. Failure → KILL. `[Sol-XF-6]`

### XF-7 — L14 coverage-response (§7)
ΔCov estimand, direction (≤0), minimum effect (0.05), all-seeds-direction. Potency present but coverage unmoved → L14 FAIL. `[Sol-XF-7]`

### XF-8 — Dose validity (§5)
Confidence clipping, ΔECE calibration metric, monotonicity tolerance, minimum potency, INSTRUMENT_FAILURE disposition, no candidate tuning. `[Sol-XF-8]`

### XF-9 — Power/sensitivity protocol (§8)
Simulation family, parameter grid, 10K sims/combo, deterministic seeds, identical estimator, false-kill calculation, sensitivity map, deterministic selection rule, misspecification stress-test. Artifacts produced in item 5. `[Sol-XF-9]`

### XF-10 — L7/L10 delta + state constraints (§4)
State-reset between batteries, retention within battery, zero cross-law carryover, semantic-equivalence demonstration. `[Sol-XF-10]`

### XF-11 — Boundary-condition rule (§6.4)
One sentence: boundary annotation never authorizes reruns or softens failure counts. `[Sol-XF-11]`

## Confirmation

- No locked bar value changed (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity mandatory, 5 seeds)
- L3 pre-scoring gate preserved
- O-14/O-15, M3 INSTRUMENT FAILURE, seed custody, L15–L17 fence all preserved
- P1–P6 maintained. P5: narrowed claim is Entry 81-authorized
- XF-1/2/3 not re-litigated (settled by Entry 81)
- All new thresholds tagged [PROPOSED] or appropriate source class

## Next recipient

**Fresh-context CRITIC** (new session — COORDINATOR will initialize) for delta review of spec v2 with the full eight-document chain attached, briefed to verify closure of XF-4–XF-9 and CF riders, not to re-litigate settled XF-1/2/3.

## Explicitly prohibited

- No merging to main
- No scoring, seed execution, or hold-out seed exposure
- No rerun of seeds 201–203 / 301–303 (O-14)
- No L15/L16/L17 work before M5
- No modification of STATE.md or provenance_log.md
- No re-litigating settled FRAME findings (XF-1/2/3 — settled by Entry 81)
- No L8 implementation or TASK BUILDER release
- No tuning doses from candidate outputs (XF-8)
- No renaming or reinterpreting any negative result or INSTRUMENT FAILURE label
