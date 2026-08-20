# CRITIC Review — L8 G2–G4 Minimal Full-Screen Specification

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**CRITIC commit identity:** `role@moving-origin-research.local` / `MOR ROLE`
**Gate served:** Fresh-context CRITIC review of the ARCHITECT's minimal L8 G2–G4 full-screen specification — internal consistency, end-to-end executability, and law-fidelity (P1–P6). Independent adversarial review; no co-authoring of the work under review.

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| GitHub main (base) | `f4e22317ebe0e3e1a7dbee0b81ef8c3fb9839b2b` |
| ARCHITECT branch + HEAD | `architect/l8-g2g4-minimal-fullscreen` @ `8f3e1098d140c184a49c6d8670cd13b7a97d3db3` |
| ARCHITECT commits | `66808c5` (spec) + `8f3e109` (amendment) |
| Spec | `specs/l8_g2g4_minimal_full_screen_spec.md` (20,813 bytes) |
| Changelog | `specs/l8_g2g4_minimal_full_screen_CHANGELOG.md` (4,788 bytes) |
| TASK BUILDER handoff | `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` (4,471 bytes) |
| Executability trace | `specs/l8_g2g4_minimal_full_screen_EXECUTABILITY_TRACE.md` (5,178 bytes) |
| Frozen L8 v2.2 spec (cited) | `c7d7bed6b259fb5163fb610098ea12aed1d3d65e` on `architect/l8-instantiation-v2.2-fresh`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| Pre-registered 20-geometry list source | `4463cbc` on `architect/l8-g2g4-remediation` (v2.4); same path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| Verified code baseline | `b1397498ca369067e956479e6c2bd6b0793c3e89` on `taskbuilder/l8-power-analysis` (`diagnostics/l8_power_analysis.py`) |
| Reference artifact | `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3` (`diagnostics/l8_power_analysis_results.json`, SHA-256 `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`) |
| Rebecca L8 feasibility ruling | `d08cb7eefec67609a3ea3cee0eb20da22f78c40a` (`docs/rulings/REBECCA_L8_1000_REP_FEASIBILITY_AUTHORIZATION.md`) |
| Constitution v2 | `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on `main` (`f4e22317`) |

All four ARCHITECT files inspected, plus every cited controlling document re-read at its cited SHA (law-diff and provenance verification performed against actual repo text, not asserted provenance).

## Verdict

**BLOCK.** Returns to **ARCHITECT only** (originating role). No downstream role starts early; Rebecca does not gate on a blocked artifact.

The BLOCK is **not** because `PRIMARY = false_kill_rate_per_seed` (any-seed) is the wrong designation — that designation is textually grounded and consistent with the frozen controlling document (see Preserved evidence §E1, §E2). The BLOCK is for (B1) a false provenance/source citation in the TASK BUILDER handoff — a required file — that would direct the implementer to the wrong controlling document, and (B2) an overstatement in the main spec that mischaracterizes what the primary metric measures.

## Blocking findings (classified)

### B1 — PROVENANCE / INTERNAL-CONSISTENCY DEFECT (TASK BUILDER handoff, required file #3 of 4)

`specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md`, "Authoritative inputs" (read-only) section, states:

> "Frozen v2.2 spec: `c7d7bed6...` for the §8.2 geometry list and §8.3 grids."

This is **false**. Verified against the cited SHA `c7d7bed6` (frozen v2.2 spec) on `architect/l8-instantiation-v2.2-fresh`:

- v2.2 §8 is titled `## §8 Power analysis and sensitivity map — protocol and selection rule (XF-9 closure)` (line 252). It is a flat numbered list (items 1–9: synthetic data-generating family; parameter grid = the 240-cell α×v×C_min×η grid; 10,000 sims/combo; estimator; false-kill calculation; sensitivity map; selection rule; stress-test). v2.2 has **no `§8.2` subsection and no 20-geometry W×N_w battery sweep**.
- The `§8.2 Candidate-blind battery-size sweep` containing the 20-geometry list (`W ∈ {50,100,200,400}` × `N_w ∈ {4,8,16,32,64}`, ordered by `Q = W·N_w`) and the `§8.3`/`§8.4` subsection structure were **added in v2.4** at `4463cbc` on `architect/l8-g2g4-remediation`.
- The main spec §0 correctly identifies `4463cbc` (v2.4) as the "only located repo source" of the pre-registered 20-geometry list. The TASK BUILDER handoff contradicts the main spec §0 on the same point.

**Why blocking:** The handoff under review explicitly directs the CRITIC to "inspect all four ARCHITECT files," and §5 P6 (provenance citation check) is binding: "Any claim of the form 'Entry n said X' must be verified against the entry's actual text before commit." A TASK BUILDER following the handoff's "Authoritative inputs" to read the §8.2 geometry list at v2.2 `c7d7bed` would **not find it there** — it would find only the 240-cell parameter grid. This is both a P6 provenance defect and an executability defect (the implementer is pointed at a source that does not contain the cited content). The main spec §0 has the provenance right; the TASK BUILDER handoff does not. The two required files are internally inconsistent on a cited SHA.

**Classification:** PROVENANCE / INTERNAL-CONSISTENCY. Blocking.

**Remediation (for ARCHITECT — not performed by CRITIC):** Correct `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` "Authoritative inputs" so the §8.2 geometry-list and §8.3 grid source is cited as v2.4 `4463cbc` on `architect/l8-g2g4-remediation` (matching spec §0), with the frozen v2.2 `c7d7bed` cited only for the §2 XF-5 estimator, the per-seed locked bar (line 44), and the 240-cell nuisance/operating grid (§8 items 3–6). Reconcile all four files to a single provenance statement.

### B2 — ACCURACY / MISCHARACTERIZATION DEFECT (main spec §5.2–§5.3)

Spec §5.2 states `false_kill_rate_per_seed` is "the direct false-kill rate corresponding to the actual scoring verdict," and §5.3 frames it as "the scoring-verdict-aligned (primary) estimate." Verified against the actual scoring verdict:

- v2.2 line 44 (the locked scoring bars): "Spearman ρ(dose, D) ≥ 0.8 `[BAR-Entry 11]` and standardized slope ≥ 0.2 `[BAR-Entry 11]`, per seed." A candidate run is killed if **any seed** fails **either** predicate (ρ < 0.8 **or** β*_s < 0.2).
- `false_kill_rate_per_seed` as computed at `b139749` (code line 808: `np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1))`) is `P(any seed β*_s < 0.2)` — the **β*-predicate portion only**. It does **not** count runs killed by the ρ < 0.8 predicate. It is therefore a **lower bound** on the full scoring-verdict false-kill rate, not the full rate.

The spec cannot compute the full verdict without the prohibited bootstrap/predicate machinery (§1.3), so reusing `b139749`'s β*-only direct calculation is defensible. But §5.2/§5.3's unqualified claim that the metric "corresponds to the actual scoring verdict" overstates what it measures. This bears directly on the §5.3 mismatch-memorialization Rebecca is asked to review: Rebecca would be deciding on a metric described as "the scoring-verdict-aligned rate" when it is in fact the β*-predicate direct rate.

**Classification:** ACCURACY / MISCHARACTERIZATION. Blocking (because it is in the main spec, not a side note, and bears on Rebecca's §5.3 decision).

**Remediation (for ARCHITECT):** Qualify §5.2/§5.3 to state that `false_kill_rate_per_seed` is the **β*-predicate direct false-kill rate** (per `b139749`), capturing only the standardized-slope < 0.2 predicate of the per-seed scoring verdict; the full scoring verdict also requires ρ ≥ 0.8 per seed (and, in v2.4 §8.1, direction + pooled-bootstrap interval), which this minimal spec deliberately does not compute. State explicitly that this is a lower bound on the complete-verdict false-kill rate.

## Non-blocking findings

### NB1 — CITED JUSTIFICATION IS THE WEAKER SOURCE (main spec §5.2)

The ARCHITECT cites v2.2 line 44 ("per seed") as the justification for `PRIMARY = false_kill_rate_per_seed`. Line 44 does support the per-seed reading (the locked bars run per seed → a run fails if any seed fails), and the designation is therefore **consistent** with the frozen controlling document (not a block — see §E1). However, the explicit any-seed-primary / 5-seed-mean-diagnostic resolution is in **v2.4 §8.1** (`4463cbc`): "The primary false-kill rate is [complete-verdict any-seed rate]… The former five-seed-mean measure is retained as `diagnostic_false_kill_rate_mean_beta` and may not gate battery size or selection." The ARCHITECT did not cite v2.4 §8.1. Recommend the ARCHITECT cite v2.4 §8.1 as corroborating context, noting that §8.1's complete verdict includes a pooled-bootstrap predicate (`[BAR-Entry 11.3]`) that this minimal spec deliberately omits in favor of `b139749`'s β*-only direct calculation. Note: v2.4 is a remediation draft whose own authority is flagged for Rebecca confirmation (spec §0), so v2.2 line 44 remains the primary frozen authority and v2.4 §8.1 corroborating only.

### NB2 — P3 SOURCE-CLASS CLARIFICATION (main spec §5.1, §5.4)

The primary metric `false_kill_rate_per_seed` is labeled `NF-IMPL-2: Per-seed false-kill rate [PROPOSED -- flagged to Rebecca]` in the `b139749` baseline (code line 804), and v2.4 §8.1 tags the complete-verdict primary false-kill rate `[PROPOSED — G3 operating criterion]`. Spec §5.4 uses `false_kill_rate_per_seed` to gate geometry acceptance (`meets_target = max_primary_false_kill ≤ 0.10`; minimum acceptable battery = first geometry meeting target). Because the run is O-15 diagnostic-only and authorizes no scoring, and §5.3 routes the primary/diagnostic mapping to Rebecca before TASK BUILDER, **P3 is not strictly violated** (no `[PROPOSED]` value gates scoring; per coordinator focus #6). Recommend the spec make explicit that the primary metric is `[PROPOSED]` (flagged to Rebecca in `b139749`) and that geometry acceptance is a `[PROPOSED]`-gated diagnostic selection requiring Rebecca sign-off before any binding/downstream use. §5.3 partially does this; strengthen. Separately: recommend the TASK BUILDER record the output artifact's own SHA-256 in the run handoff for reproducibility verification (the spec fixes schema/canonicalization/seed derivation, but does not require recording the output digest; inherent to stochastic artifacts, non-blocking).

### NB3 — PROVENANCE FRAMING IMPRECISION (main spec §1.3)

Spec §1.3 states: "Where `d08cb7e` required the two execution details (repetition allocation; bootstrap budget), this spec closes them: 2,000 simulations per cell per arm, and no bootstrap." Verified against `d08cb7e`: that ruling's two open execution details concerned the **1,000-repetition feasibility diagnostic** (allocation of 1,000 reps across sentinel cells/geometries; full-5,000-valid-bootstrap verdict vs. reduced benchmark bootstrap budget) — a different workload from the 9.6M screening run. The screening-run parameters come from the later WORKFLOW COORDINATOR handoff, not from closing `d08cb7e`'s feasibility-diagnostic details. The spec's authorization-boundary claim (`d08cb7e` did not authorize the 9.6M screening run, 10K confirmation, bootstrap, scoring, etc.) is **correct** and verified against `d08cb7e` "Authorization boundary." Only the "closes the two details" framing is imprecise. Recommend correcting the framing so it does not imply the screening run closes the feasibility-diagnostic's open details.

### NB4 — P3 TAG CONVENTION (main spec §5)

Kill conditions in §5 carry `[Sol-XF-5]` closure-labels (e.g., "zero-variance `σ_pool,s = 0` → `INSTRUMENT_FAILURE` `[Sol-XF-5]`"). These are inherited verbatim from frozen v2.2 (line 81). P3 specifies "one of exactly four" source-class tags (`[LAW-Lx]`, `[BAR-Entry n]`, `[OP-Entry n]`, `[PROPOSED]`); `[Sol-XF-5]` is not one of the four. The tag is present (not "without a tag"), inherited from frozen v2.2, and the numeric thresholds that matter (0.2, 0.10, 5 seeds, 0.8 ρ) are all correctly tagged `[BAR-Entry 11]` or `[PROPOSED]`. Recommend the ARCHITECT either re-tag the inherited `[Sol-XF-*]` kill conditions as `[OP-Entry n]` (adopted operationalization) or confirm `[Sol-XF-*]` is an adopted `[OP]`-class closure label. Non-blocking because no threshold is untagged and the rule is faithful to frozen v2.2.

## Preserved evidence (verified, not blocking)

### E1 — Scoring-verdict designation is textually grounded (review focus #1, decisive — NOT a block)

The ARCHITECT's designation `PRIMARY = false_kill_rate_per_seed` (any-seed) / `DIAGNOSTIC = false_kill_rate` (5-seed mean) is **consistent with the frozen controlling document**:

- v2.2 line 44: the locked scoring bars run "**per seed**" — each seed must clear ρ ≥ 0.8 and β* ≥ 0.2; a candidate run fails the scoring verdict if **any seed** fails. The false-kill rate corresponding to that verdict is therefore the **any-seed** rate. The ARCHITECT's any-seed designation follows the frozen text; it did not need to STOP.
- v2.4 §8.1 (`4463cbc`) independently and explicitly confirms the direction: primary = complete-verdict any-seed rate; "The former five-seed-mean measure… may not gate battery size or selection."
- The `b139749` baseline's `[PROPOSED -- flagged to Rebecca]` label on `false_kill_rate_per_seed` is implementer caution (NF-IMPL-2), not a textual ambiguity in v2.2; it does not override the frozen "per seed" text. (It does require P3 handling — see NB2 — but does not make the designation wrong.)

The decisive review item (#1) is therefore **resolved consistent** with the ARCHITECT, not a STOP-worthy ambiguity. (B2 qualifies *how* the metric is described, not *which* metric is primary.)

### E2 — P2 law-diff PASSES (first checklist item)

Spec §1.2 verbatim quotes of L8 and §5 P1–P6 were diffed against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on `main` (`f4e22317`):

- L8 (constitution line 28): quoted verbatim in spec §1.2. Match exact.
- §5 5.1 P1–P6 (constitution lines 131–136): all six (P1 repo-first, P2 verbatim, P3 source-class, P4 regime dating, P5 deviation memorialization, P6 provenance check) quoted verbatim in spec §1.2. Match exact.
- §5.2 ARCHITECT per-role obligation (constitution line 139): first sentence quoted verbatim.

No reconstruction of constitutional text. P2 satisfied.

### E3 — Two-arm workload accounting and timing CORRECT (review focus #2)

The ARCHITECT's 19.2M two-arm accounting and ~4× linear timing estimate (90.5 min, 1.5–2 h) are **correct**. Verified against `b139749` code and reference artifact `6d455bb`:

- `b139749` `run_power_analysis` dispatches **both** arms per cell at equal `n_sims`: `work_items` (combo, `n_sims`) and `null_items` (null-control, same `n_sims`) via `pool.map` (code lines ~901, ~910). So a cell runs `n_sims` combo + `n_sims` null.
- Reference `6d455bb`: `n_sims_per_combo=10000`, `n_combos=240`, `elapsed_seconds=1357.68` (22.63 min) for the single smallest geometry (W=50, N_w=4). That run executed 240 × (10000 combo + 10000 null) = 4.8M arm-sims in 22.63 min.
- Spec: 20 geometries × 240 cells × (2000 combo + 2000 null) = 19.2M arm-sims. Ratio 19.2M / 4.8M = 4×. 4 × 22.63 min ≈ 90.5 min. Estimate holds.

The ARCHITECT's correction of the coordinator's 9.6M (combo-arm-only) count to 19.2M (both arms) is accurate. The spec appropriately flags the two-arm workload accounting and the "single 2,000-per-cell budget shared across arms" alternative for Rebecca confirmation (§2). Non-blocking Rebecca-decision item, properly routed.

### E4 — Geometry-list provenance CORRECT in main spec (review focus #3)

v2.4 §8.2 at `4463cbc` **does** contain the pre-registered 20-geometry list (`W ∈ {50,100,200,400}` × `N_w ∈ {4,8,16,32,64}`, ordered by `Q = W·N_w`). Reusing the **geometry grid** does not invoke the prohibited Wilson/bootstrap machinery: those are in v2.4 §8.2's reporting-requirements ("two-sided Wilson 95% interval," "predicate-specific failure rate") and §8.9, which the spec §1.3/§9 explicitly drops. The main spec §0 correctly identifies `4463cbc` (v2.4) as the only located repo source and correctly flags geometry-list authority for Rebecca confirmation. (The TASK BUILDER handoff's misstatement of this same provenance is B1.)

### E5 — No prohibited machinery recreated (review focus #5)

Spec §1.3/§9 and executability trace §6 confirm the absence of: bootstrap; Wilson intervals; `predicate_false_kill_rates`/`failure_mask_counts`; finalist 10,000-rep confirmation; `resolved_config.json` manifest; rehearsal fixtures; fault injection; sensitivity/misspecification recomputation; `(C_min,η)` selection; scoring; protected-seed access; seeds 201–203/301–303; G2–G4 freeze; merge to main; L15/L16/L17; INSTRUMENT_FAILURE reclassification of statistical failures. The TASK BUILDER handoff's "Prohibited" list matches the spec's. PASS.

### E6 — End-to-end executability PASSES (review focus #7)

The spec fixes every input the TASK BUILDER must supply: exact JSON schema, field order, types, NaN→null sanitization, single atomic write, paths (`diagnostics/l8_g2g4_minimal_full_screen.json`, `_HANDOFF.md`), cell ordering (`alpha → v_mult → c_min → eta`), deterministic seed derivation (`combo_seed` sha256-based; per-sim seed `(base_seed + i·N_SEEDS + s) % 2^31`), calibration reference point (`C_min=0.7, η=0.1`), 16 workers, `multiprocessing.Pool`, chunksize 1. The reference artifact `6d455bb` (SHA-256 `978f21c0…`) provides the cross-check baseline. No implementer invention required beyond the flagged primary/diagnostic designation (routed to Rebecca). The v2.6 false-CLEAR failure mode (undefined fixture / committed artifact pair / estimator realizations) does **not** apply: fixture (W=50, N_w=4 reference), schema (§7.1 exact), seed derivation, and reference digest are all concretely specified. The spec is executable end-to-end. (B1 is a provenance pointer defect, not a missing-input defect; B2 is a description defect, not an executability gap.)

## Exact next authorized role

**ARCHITECT only** (originating role). On BLOCK, the route is CRITIC → ARCHITECT. No TASK BUILDER, no Rebecca gate, no implementation. ARCHITECT corrects B1 and B2 (and addresses NB1–NB4), then re-routes to fresh-context CRITIC → Rebecca → TASK BUILDER.

## Explicitly prohibited actions

No scoring. No protected-seed access. No seeds 201–203 / 301–303. No G2–G4 freeze or ruling by ARCHITECT. No merge to main (CRITIC commits only to `critic/l8-g2g4-minimal-fullscreen`). No L15/L16/L17 before M5. No implementation. No rerun. No exposing of hold-out seeds. No rerunning of failed scoring. No lowering, raising, renaming, reinterpreting, or silently replacing a locked bar. CRITIC did not edit the spec, changelog, TASK BUILDER handoff, executability trace, or STATE.md. CRITIC did not co-author, fix, or modify the work under review.

## Confirmation

No scoring was conducted. No hold-out or protected seeds were accessed or exposed. No failed scoring was rerun. No merge to `main` occurred. No verdict was returned before the review was committed in-repo and pushed. The CRITIC's review is backed by a committed artifact on `critic/l8-g2g4-minimal-fullscreen` (see commit SHA in handoff).

## Pre-push self-scan attestation

A pre-push self-scan was performed on the review artifact and the branch contents for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths (e.g. `/home/user/workspace/...`), environment dumps, and PII.

Findings: **none.** The review contains only public repo SHAs, branch names, file paths, byte sizes, verbatim constitutional/spec text already in the public repo, and CRITIC analysis. No private paths, credentials, or PII. Scan result: **clean — no blockers, no Rebecca-decision items, acceptable.**

---

*CRITIC review complete and committed in-repo. This file is the binding artifact; the handoff message is a pointer to it.*
