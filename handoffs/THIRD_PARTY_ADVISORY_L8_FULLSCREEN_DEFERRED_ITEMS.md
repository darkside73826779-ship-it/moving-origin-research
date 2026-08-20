# Third-Party Advisory Request — L8 Full-Screen Spec: Two Deferred Gate Items

## Context

You are advising the principal investigator (PI) of a research program testing whether a "moving-origin temporal self-index" — a data structure that maintains and re-resolves temporal coordinates as new events arrive — can be empirically distinguished from simpler alternatives. The program is governed by a 20-law constitution with pre-registered numeric bars (`[BAR-Entry n]`), adversarial CRITIC review, independent JUDGE scoring, candidate-blind calibration (Ruling 9), and a strict no-re-run-on-failure doctrine (O-14). The PI is the sole authority for gate decisions and main-branch merges. Development runs are diagnostic-only (O-15); nothing is scoring evidence until run through the PI's supervised-executor courier channel.

This request concerns the **L8 law** (stakes coupling): *at least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then).* The L8 test injects calibrated noise into the self-model and checks dose-dependent regulation-error rise. A candidate mechanism must show its "stakes" respond to self-model quality; decorative stakes fail the law.

## What the L8 full-screen spec is

A minimal, executable specification for one diagnostic "full screen": **20 battery geometries × 240 cells per geometry × 2,000 simulations per cell**, evaluated with an existing direct false-kill calculation (code at `b139749`). It is **candidate-blind, synthetic/oracle-only, O-15 diagnostic-only**. It authorizes **no scoring, no G2–G4 freeze, no protected-seed access, no merge to main**.

- The 20 geometries are query-budget shapes `W ∈ {50,100,200,400}` × `N_w ∈ {4,8,16,32,64}`, ordered by total queries per dose `Q = W·N_w`.
- Each of 240 cells = 15 nuisance combinations (noise `α` × effect-multiplier `v`) × 16 operating points (`C_min × η`).
- Two arms per cell: a **combo arm** (true calibrated effect; the true-effect synthetic case should pass the L8 bars — the apparatus should not falsely kill it) and a **null-control arm** (`σ_dose = 0`, no true effect; should fail). The PI has confirmed the two-arm interpretation: 9.6M combo + 9.6M null = **19.2M actual simulations**, ~1.5–2 h on 16 workers.
- **No bootstrap, no Wilson intervals, no benchmark/rehearsal/fault-injection machinery** — direct false-kill calculation only. (Earlier v2.3–v2.7 bootstrap/benchmark machinery was superseded and is prohibited here.)

### Glossary

- **combo arm:** synthetic true-effect arm. A **false-kill** is when a combo-arm simulation fails the relevant bar (the apparatus wrongly rejects a true-effect case).
- **null-control arm:** zero-effect arm. A **false-pass** is when a null-control simulation passes the bar (the apparatus wrongly accepts a no-effect case).
- **false_kill_rate:** 5-seed-mean β*-predicate false-kill rate (the combo arm's 5-seed mean `β*` below the bar).
- **false_kill_rate_per_seed:** any-seed β*-predicate false-kill rate (any one of the 5 seeds below the bar). Designated **PRIMARY**; a **lower bound** on the complete scoring-verdict false-kill rate (the complete verdict also counts ρ < 0.8 per-seed failures).
- **β\*:** standardized slope estimator (`β*_s = β_s / σ_pool,s`) from the §2 XF-5 estimator.
- **battery / geometry:** a query-budget shape `(W, N_w)`; the screen seeks the minimum battery whose worst-cell primary false-kill ≤ 0.10.

The screen's purpose: find the minimum battery (query budget) whose worst-cell false-kill rate is within the 0.10 target — i.e., a battery at which the L8 test is discriminating enough. This feeds the PI's later G2–G5 gate rulings (the false-kill aggregation choice and battery size were found to be entangled in a prior advisor consultation).

## Status of the spec

The spec was produced by the ARCHITECT, reviewed by a fresh-context CRITIC (BLOCK on two defects), remediated by the ARCHITECT, and re-reviewed CLEAR by a fresh-context CRITIC. The CRITIC verified every claimed fix against the actual diff (false-attestation guard held; a prior ARCHITECT session had falsely attested fixes). The spec is committed at `architect/l8-g2g4-minimal-fullscreen` @ `a7b38b3`; the CRITIC re-review is at `reviews/critic_l8_g2g4_minimal_fullscreen_rereview.md` @ `ab0111c`.

The PI has confirmed one gate item (two-arm workload) and **deferred two items** for external advisory consultation. Those two items follow. The PI has **not** authorized the TASK BUILDER to implement; implementation is held until these resolve.

---

## Deferred Item 1 — Primary/diagnostic metric mapping (spec §5.1–§5.4)

### The decision

Which false-kill rate is the **primary** metric for the battery-acceptance screen, and is the spec's characterization of it accurate enough to proceed?

### What the spec designates (verbatim, post-remediation)

> **§5.1.** `false_kill_rate` = fraction of valid simulations where the **5-seed mean** `β*_run < BETA_STAR_BAR` (0.2) `[BAR-Entry 11]`. Handoff label: "five-seed aggregated verdict." `[PROPOSED — diagnostic; NF-IMPL-2 in b139749]`
> `false_kill_rate_per_seed` = fraction of valid simulations where **any seed** `β*_s < BETA_STAR_BAR` (0.2) `[BAR-Entry 11]` (`b139749` code line 808: `np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1))`). Handoff label: "any-seed." This is the **β\*-predicate direct false-kill rate** — it captures only the standardized-slope < 0.2 predicate of the per-seed scoring verdict. It does **not** count runs killed by the `ρ < 0.8` predicate, which is also part of the per-seed scoring verdict (v2.2 line 44). It is therefore a **lower bound on the complete scoring-verdict false-kill rate**, not the full rate. The complete verdict also requires (in v2.4 §8.1) direction + pooled-bootstrap interval `[BAR-Entry 11.3]`, which this minimal spec deliberately does not compute (no bootstrap; §1.3). `[PROPOSED — primary metric; NF-IMPL-2 in b139749]`

> **§5.2.** The frozen L8 v2.2 spec states the locked standardized-slope bar runs **per seed**: "The locked bars run on D: Spearman ρ(dose, D) ≥ 0.8 `[BAR-Entry 11]` and standardized slope ≥ 0.2 `[BAR-Entry 11]`, per seed." — `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (`c7d7bed`), line 44. A candidate run fails the scoring verdict if **any seed** fails **either** predicate (ρ < 0.8 **or** β*_s < 0.2). Among the two β\*-predicate direct rates available from `b139749`, the rate with the seed aggregation matching the per-seed scoring verdict is the any-seed rate. Designation: **PRIMARY = `false_kill_rate_per_seed`** (per-seed / any-seed; matches the "per seed" locked bar) `[PROPOSED — primary metric, flagged to Rebecca in b139749 (NF-IMPL-2)]`; **DIAGNOSTIC = `false_kill_rate`** (5-seed mean).

> **§5.3.** The verified baseline `b139749` labels `false_kill_rate` (5-seed mean) as the key false-kill output and flags `false_kill_rate_per_seed` as "NF-IMPL-2: PROPOSED — flagged to Rebecca." This minimal spec resolves the label priority by applying the frozen spec's "per seed" locked-bar text, which makes the any-seed β\*-predicate direct rate the primary battery-sizing metric. **CRITIC and Rebecca must specifically review this primary/diagnostic mapping before TASK BUILDER implementation**, noting that the primary metric is the β\*-predicate direct rate — a **lower bound** on the complete scoring-verdict false-kill rate (which also includes the ρ ≥ 0.8 per-seed predicate). A reference cell (`α=0.0, v_mult=0.5, C_min=0.5, η=0.01`, `N_w=4`) from `6d455bb` illustrates the materiality: `false_kill_rate = 0.0565` (passes 0.10) vs `false_kill_rate_per_seed = 0.7483` (fails). The primary choice is consequential.

> **§5.4.** The applicable false-kill target is `FALSE_KILL_THRESHOLD = 0.10` `[PROPOSED — apparatus parameter, §8]` (v2.2 §8: false-kill probability exceeding 0.10 escalates battery size to G3). For each geometry: geometry-level maximum primary false-kill = `max` over its 240 cells of `false_kill_rate_per_seed`; `meets_target` = geometry-level maximum primary false-kill ≤ 0.10. Minimum acceptable battery = the first geometry in the §3 ordering whose `meets_target` is true. If no tested geometry meets the target, STOP. The primary metric is `[PROPOSED]` and geometry acceptance is a `[PROPOSED]`-gated diagnostic selection requiring **Rebecca sign-off before any binding or downstream use**.

### Controlling documents (as verified by the CRITIC)

- **Frozen L8 v2.2 line 44** (`c7d7bed`): the locked bars run per seed — `ρ ≥ 0.8` AND standardized slope `≥ 0.2`, per seed. A run fails if any seed fails either predicate.
- **Verified code `b139749` line 808**: `false_kill_rate_per_seed = np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1))` = `P(any seed β*_s < 0.2)` — the β*-predicate portion only; does not count ρ-failures.
- **v2.4 §8.1** (`4463cbc`, corroborating only; CRITIC summary, not verbatim): the primary false-kill rate is the complete-verdict any-seed rate; the former five-seed-mean measure may not gate battery size or selection. (v2.4 is itself a remediation draft whose authority is flagged for PI confirmation — see Item 3.)
- **M0 decision sheet line 21**: the locked bars (Spearman ρ ≥ 0.8, standardized slope ≥ 0.2, ≥ 3 doses, 5 seeds).

### CRITIC's verified findings on this item

- **E1 (designation is textually grounded, NOT a block):** the ARCHITECT's `PRIMARY = false_kill_rate_per_seed` (any-seed) follows the frozen v2.2 "per seed" text; the ARCHITECT did not need to STOP. v2.4 §8.1 independently confirms the direction.
- **B2 (now fixed):** the original spec overstated `false_kill_rate_per_seed` as "the scoring-verdict-aligned rate"; the remediation qualified it as the β*-predicate direct rate / lower bound on the complete-verdict rate (which also requires ρ ≥ 0.8 per seed). The CRITIC verified the spec's characterization now matches what the code computes.
- **NB1:** the ARCHITECT now cites v2.4 §8.1 as corroborating context (with v2.2 line 44 primary). **NB2:** the primary metric is tagged `[PROPOSED]`; geometry acceptance is `[PROPOSED]`-gated and requires PI sign-off before binding/downstream use.

### Why it matters (the entanglement)

In a prior advisor consultation, the PI found the false-kill aggregation choice and battery size are **entangled**: under the 5-seed-mean aggregation the reference operating point's false-kill was **6.22%** (passes 0.10); under the any-seed aggregation it was **76.23%** (fails 0.10 → G3 triggered). Which rate is "primary" determines whether the current battery passes or whether a larger query budget is needed. The screen sweeps 20 geometries precisely to find one where the primary (any-seed) rate drops below 0.10. Note the any-seed β*-predicate rate is a **lower bound** on the complete scoring-verdict false-kill rate (the complete verdict also rejects runs failing the ρ < 0.8 predicate, so it is at least as high).

### Options as currently framed

- **(a) Approve the mapping** — `false_kill_rate_per_seed` (any-seed, β*-predicate direct rate / lower bound) as primary; `false_kill_rate` (5-seed mean) as diagnostic; geometry acceptance `[PROPOSED]`-gated, PI sign-off before binding. Proceed to TASK BUILDER.
- **(b) Change the primary metric** — e.g., require the complete-verdict rate (β* AND ρ per seed) as primary. This would require a new ARCHITECT amendment and CRITIC review; the TASK BUILDER may not invent it under the current minimal spec.
- **(c) Hold.**

### Questions for the advisor

1. Is the any-seed β*-predicate direct rate the correct primary metric for battery sizing, given that (i) the frozen law text says the bars run "per seed" (so any-seed failure kills a run) but (ii) this rate is a **lower bound** on the complete scoring-verdict false-kill rate (it omits the ρ < 0.8 per-seed kills)? If the intended target is complete-verdict false-kill ≤ 0.10, does using the β*-predicate lower bound risk accepting a battery the complete verdict would reject?
2. The 5-seed-mean rate (6.22%) passes 0.10 while the any-seed rate (76.23%) fails badly. Is the any-seed aggregation the right reading of "per seed," or is there a defensible intermediate (e.g., requiring a quorum of seeds, or a margin/bootstrap fallback) that the law text supports without reconstruction?
3. The complete-verdict rate would require the ρ-predicate (and, in v2.4, a pooled-bootstrap interval), which this minimal spec deliberately omits (no bootstrap). Is it sound to size the battery on the β*-predicate lower bound now and defer the complete-verdict confirmation, or should the complete verdict be computed before any battery is accepted?
4. Geometry acceptance is `[PROPOSED]`-gated and requires PI sign-off before binding. Is that the right gate placement — i.e., is it acceptable to *run* the screen on the `[PROPOSED]` primary metric (diagnostic-only, no scoring) and gate only the *binding* of results on PI sign-off?
5. What would you recommend?

---

## Deferred Item 3 — Geometry-list authority (spec §0, §3)

### The decision

Is v2.4 §8.2 at commit `4463cbc` the authoritative pre-registered 20-geometry list for this screen?

### What the spec says (verbatim, post-remediation)

> **§0.** Pre-registered 20-geometry list (§8.2): `4463cbc` on `architect/l8-g2g4-remediation`; same path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (v2.4). This is the **only located repo source** of the pre-registered 20-geometry list; the v2.4 Wilson/bootstrap §8.9 machinery in the same commit is **prohibited** and is not invoked. Geometry-list authority flagged for CRITIC/Rebecca confirmation.

> **§3.** The 20 geometries are the Cartesian product of `W ∈ {50, 100, 200, 400}` and `N_w ∈ {4, 8, 16, 32, 64}`, ordered by total queries per dose `Q = W × N_w` ascending, then by larger `N_w`, then by smaller `W`. The grid is **not redesigned**; this table is the authoritative ordered list. Locked dose requirement preserved: four dose levels `{0, 1, 2, 3}`; the sweep shall not reduce noise doses below the locked minimum of three `[BAR-Entry 11]`.

(The full 20-row table: idx 1–20 spanning `Q` from 200 to 25,600; queries per 5-seed run from 4,000 to 512,000.)

### The boundary condition

The 20-geometry list lives in **v2.4** (`4463cbc`), which is a remediation draft — and v2.4's surrounding machinery (Wilson bootstrap intervals, `predicate_false_kill_rates`/`failure_mask_counts`, finalist 10,000-rep confirmation, `resolved_config.json` manifest, §8.9.3–§8.9.4) is **prohibited** in this minimal spec. So the screen reuses the geometry *list* from v2.4 while explicitly **not invoking** v2.4's *machinery*. v2.4's own authority is itself flagged for PI confirmation (§0) — it is not yet a frozen, PI-signed spec.

### CRITIC's verified findings on this item

- **E4 (geometry-list provenance correct in spec §0):** v2.4 §8.2 at `4463cbc` does contain the pre-registered 20-geometry list (`W ∈ {50,100,200,400}` × `N_w ∈ {4,8,16,32,64}`, ordered by `Q = W·N_w`). Reusing the geometry grid does **not** invoke the prohibited Wilson/bootstrap machinery (those are in v2.4 §8.2's reporting-requirements and §8.9, which the spec §1.3/§9 drops). The main spec §0 correctly identifies `4463cbc` as the only located repo source and flags authority for PI confirmation.
- **B1 (now fixed):** the original TASK BUILDER handoff falsely cited the geometry list as being in frozen v2.2 (`c7d7bed`); the remediation corrected it to v2.4 `4463cbc` and reconciled all four spec files to a single provenance statement. (Frozen v2.2 §8 is a flat numbered list with **no** §8.2/§8.3 subsections and **no** 20-geometry sweep; the geometry list is genuinely a v2.4 addition.)

### Options as currently framed

- **(a) Confirm `4463cbc` §8.2** as the authoritative pre-registered 20-geometry list; proceed (the spec reuses only the list, not the prohibited machinery).
- **(b) Identify a different authoritative source** for the pre-registered geometry list (if one exists that the spec missed); amend if so.
- **(c) Hold.**

### Questions for the advisor

1. Is it methodologically sound to source the pre-registered geometry list from a remediation draft (v2.4) whose own machinery is simultaneously being excluded as prohibited — i.e., reusing the *list* but not the *machinery* from the same commit? Does this create any pre-registration-integrity concern (e.g., the geometry set being co-located with machinery that was later judged inappropriate)?
2. The v2.4 spec is not yet PI-signed/frozen (its authority is flagged for confirmation). Is it acceptable to treat its geometry list as pre-registered authority for a diagnostic screen now, with the understanding that the screen's *results* only bind after PI sign-off — or should the geometry list be frozen/signed before the screen runs at all?
3. Is the 20-geometry `W × N_w` grid an appropriate coverage of the query-budget design space for sizing the L8 battery, or is there an obvious gap (e.g., missing a regime where the false-kill behavior is qualitatively different)?
4. What would you recommend?

---

## Requested output from the advisor

Please return a concise answer in this shape:

- Recommended ruling for **Item 1** (primary/diagnostic mapping).
- Recommended ruling for **Item 3** (geometry-list authority).
- Whether any **spec amendment** is required before TASK BUILDER implementation.
- Whether the TASK BUILDER may **proceed** if the PI accepts the recommendation.
- **Confidence / key caveats.**

The PI retains sole gate authority; the advisor recommends, the PI rules.

---

## Guardrails in force (binding)

- **O-14:** no re-run-on-failure; scoring seeds 201–203 / 301–303 are never rerun. A failed scoring run is permanent.
- **O-15:** development runs are diagnostic-only; nothing here is scoring evidence.
- **Candidate-blindness (Ruling 9):** simulation seeds derive from parameter-combo hashes only; no candidate output is an input anywhere.
- **No-relabeling:** INSTRUMENT_FAILURE stays INSTRUMENT_FAILURE; no negative is renamed, reinterpreted, or silently replaced. Ordinary per-seed statistical failures are predicate failures, NOT INSTRUMENT_FAILURE.
- **Anti-score-chasing posture:** pre-registration before data exists; candidate-blind calibration; frozen before scoring; courier-only scoring; no post-hoc threshold adjustment. If a design choice smells like "correct until it passes," it should be flagged.
- **`[PROPOSED]` cannot gate scoring** unless the PI signs. The screen is diagnostic-only; its results bind only on PI sign-off.
- **No bootstrap, no Wilson, no benchmark/rehearsal/fault-injection machinery** in this spec.
- **No G2–G4 freeze or ruling by the ARCHITECT.** No merge to main. No L15/L16/L17 before M5.

## Scope of this request

The PI seeks advisory guidance on the proper decision for **Item 1 (primary/diagnostic mapping)** and **Item 3 (geometry-list authority)**. The PI retains sole gate authority; the advisor recommends, the PI rules. No implementation, scoring, or merge is authorized by this request.
