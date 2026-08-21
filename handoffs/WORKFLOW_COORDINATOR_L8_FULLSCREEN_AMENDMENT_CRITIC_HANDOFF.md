# WORKFLOW COORDINATOR → CRITIC Handoff — L8 Full-Screen Amended Spec Review

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** Fresh-context CRITIC review of the ARCHITECT's amended L8 G2–G4 minimal full-screen spec (Rebecca directive: Item 1 complete primary predicate + authorized per-seed ρ; Item 3 geometry authority + DRAFT PI ruling; 3 reconciliation rounds).
**Next recipient:** On CLEAR → **Rebecca** (signs the geometry-list adoption) → TASK BUILDER. On BLOCK → **ARCHITECT only**.

## Authority and scope

The ARCHITECT amended the spec per Rebecca's directive (accepting the third-party advisor's recommendations) and re-routes to a fresh-context CRITIC. This handoff is prepared for Rebecca to transport to CRITIC. This is an independent adversarial review — verify against the actual diff, not the commit message (false-attestation guard below).

Authority chain: Rebecca > constitution laws > approved specifications > this handoff > agent judgment. The CRITIC does not choose scientific rules; it verifies fidelity, consistency, executability, and law-compliance, and determines CLEAR/BLOCK on the whole amended artifact.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub main (base) | `f4e2231` |
| ARCHITECT branch + HEAD (amended) | `architect/l8-g2g4-minimal-fullscreen` @ `2082680` |
| Amendment commits (on top of `a7b38b3`) | `dc3185a` (STOP — b139749 lacks per-seed ρ), `69feed8` (amend per Rebecca directive + authorized per-seed ρ), `09f605e` + `e3bbd6c` + `17e8364` + `548d4b9` + `2082680` (advisor round-2 + 3 reconciliation rounds) |
| Diff range to review | `a7b38b3..2082680` (inspect each commit individually) |
| Spec (5 deliverables on branch) | `specs/l8_g2g4_minimal_full_screen_spec.md` (36,963B), `_CHANGELOG.md` (13,699B), `_EXECUTABILITY_TRACE.md` (8,411B), `_TASKBUILDER_HANDOFF.md` (8,745B); `handoffs/DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md` |
| Prior CRITIC re-review (CLEAR) | `reviews/critic_l8_g2g4_minimal_fullscreen_rereview.md` @ `ab0111c` on `critic/l8-g2g4-minimal-fullscreen-rereview` |
| Rebecca directive (Item 1 + Item 3) | `handoffs/WORKFLOW_COORDINATOR_L8_FULLSCREEN_ARCHITECT_AMENDMENT_HANDOFF.md` — file-repo `a644d01`; **on GitHub** branch `coordinator/l8-fullscreen-referenced-handoffs` (PR [#102](https://github.com/darkside73826779-ship-it/moving-origin-research/pull/102)) |
| Rebecca ρ authorization ruling (cited by spec §5.1) | `REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION` — verify it exists in-repo and is operative (Rebecca-signed) |
| Third-party advisor package | `handoffs/THIRD_PARTY_ADVISORY_L8_FULLSCREEN_DEFERRED_ITEMS.md` — file-repo `246bd84`; **on GitHub** branch `coordinator/l8-fullscreen-referenced-handoffs` (PR [#102](https://github.com/darkside73826779-ship-it/moving-origin-research/pull/102)) |
| Frozen L8 v2.2 (locked bars, line 44) | `c7d7bed`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (per-seed: ρ ≥ 0.8 AND standardized slope ≥ 0.2) |
| v2.4 geometry-list source | `4463cbc` on `architect/l8-g2g4-remediation` (§8.2 = 20-geometry `W×N_w` list + ordering) |
| Verified code baseline | `b139749` (computes per-seed β* and transient dose-level `D̄`; does NOT expose per-seed ρ — the reason for the STOP and the authorized direct-ρ extension) |
| Reference artifact / runtime basis | `6d455bb` (SHA-256 `978f21c0…`; cited as the timing/runtime basis) |

**Inspect all five deliverables** at `2082680`, and re-read every cited controlling document at its cited SHA.

## What the ARCHITECT asserts (verify each against the diff)

### Item 1 — primary metric (spec §5.1–§5.3, §5.5, §5.6, §7.1)
- **PRIMARY = `complete_verdict_false_kill_rate`** = `P(any seed s: β*_s < 0.2 OR ρ_s undefined OR ρ_s < 0.8)` — the complete frozen-v2.2 any-seed scoring-verdict false-kill rate (both bars per seed; any-seed aggregation).
- **Authorized direct per-seed Spearman ρ** (per `REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION`): Pearson correlation of dose ranks `(1,2,3,4)` vs response midranks of the four dose-level summaries `D̄_{s,ℓ}`; ties = mean of occupied ranks; computed in the same estimator path where `D̄` is available. Direct, deterministic, non-resampling.
- **Zero-variance → `ρ_s` undefined → ρ-predicate failure** (NOT `INSTRUMENT_FAILURE`); non-finite/structurally-invalid → §5.6 apparatus-validity decision tree (either apparatus-invalid exclusion or undefined-ρ predicate failure — not automatic INSTRUMENT_FAILURE).
- **`RHO_COMPARE_EPS = 1e-12`** floating-point tolerance for the locked `ρ_s ≥ 0.8` comparison: passes iff `ρ_s ≥ 0.8` OR `abs(ρ_s − 0.8) ≤ RHO_COMPARE_EPS`; a test asserts `0.8 − 2·RHO_COMPARE_EPS` **fails** (the locked 0.8 bar is not moved). Tie detection = exact binary64 equality (no separate tie tolerance).
- **Diagnostics demoted:** `diagnostic_beta_only_any_seed_false_kill_rate` (β*-only any-seed; lower bound on primary) and `diagnostic_five_seed_mean_false_kill_rate` (5-seed mean) — do NOT gate battery acceptance.
- **Null-control false-pass** = `null_control_false_pass_rate` = fraction of null-control sims where every seed satisfies BOTH predicates (β*_s ≥ 0.2 AND ρ_s ≥ 0.8).
- v2.4 §8.1 pooled-bootstrap predicate `[BAR-Entry 11.3]` is NOT part of this primary (frozen-v2.2 bars only).

### Item 3 — geometry authority (spec §0, §3, §5.4; DRAFT PI ruling)
- 20-geometry grid + ordering adopted ONLY from v2.4 `4463cbc` §8.2; v2.4 prohibited machinery NOT adopted.
- Acceptance per exact `(W, N_w)`, not just `Q`; deterministic `Q`-tie ordering ("larger `N_w`, then smaller `W`") made binding.
- **Boundary-escalation rule** (§5.4): if no geometry passes (`meets_target` false for all 20), OR the first passing geometry lies on a tested boundary (`W ∈ {50, 400}` or `N_w ∈ {4, 64}` — any edge of the `W×N_w` grid) → STOP, escalate to ARCHITECT/Rebecca; do not auto-accept a boundary solution.
- **DRAFT PI ruling** (`handoffs/DRAFT_PI_L8_GEOMETRY_TABLE_FREEZE_FOR_REBECCA_SIGNATURE.md`): prospectively freezes the geometry table before execution; marked "DRAFT — NOT OPERATIVE unless/until Rebecca signs"; does not claim prior PI approval/freezing.

### Reconciliation (3 rounds) and locked bars
- The ARCHITECT asserts 3 reconciliation rounds kept the changelog, executability trace, TASK BUILDER handoff, and DRAFT PI ruling consistent with the spec (schema fields: `complete_verdict`/diagnostics/null denominators/cell_apparatus_invalid/meets_target; `max_primary_false_kill` null-if-no-eligible-cells; tie-tolerance binding).
- The ARCHITECT asserts **locked bars unchanged throughout** (β* ≥ 0.2, ρ ≥ 0.8, ≥ 3 doses, 5 seeds) and that no quorum/fallback/bootstrap/Wilson was introduced.

## Review focus (verify each against the diff)

1. **Authorized per-seed ρ computation is within Rebecca's authorized scope.** Verify the ruling `REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION` exists in-repo and is operative (Rebecca-signed; P6 provenance). Confirm the per-seed Spearman ρ is a direct, deterministic, non-resampling statistic and does NOT introduce bootstrap/Wilson/quorum/fallback machinery (the directive's prohibition). Confirm the amendment does not exceed what Rebecca authorized.
   - **Source-authority for each post-STOP design choice:** verify authority/source tags for the direct Spearman ρ formula; zero-variance → undefined ρ → predicate failure; non-finite/structurally-invalid handling via §5.6; `RHO_COMPARE_EPS = 1e-12`; exact binary64 tie detection; the boundary-rule definition; separate true/null denominators; and apparatus-invalid geometry disqualification. If any lacks Rebecca authorization or proper `[PROPOSED]`/`[OP]` tagging, BLOCK or require explicit Rebecca gating.
2. **`RHO_COMPARE_EPS = 1e-12` does not soften the locked `ρ ≥ 0.8` bar.** Verify the test asserting `0.8 − 2·RHO_COMPARE_EPS` fails is present and correct; the tolerance only absorbs binary64 roundoff at the exact threshold (e.g., `0.7999999999999999` = roundoff of exactly `0.8`), not a material bar movement. This is the most consequential locked-bar-integrity check. **Note:** frozen v2.2 supplies the bars and per-seed structure (β* ≥ 0.2 and ρ ≥ 0.8, per seed); the handling of undefined ρ, non-finite inputs, and comparison tolerance are operationalizations / Rebecca-authorized additions, NOT literal frozen-v2.2 text — verify they do not alter the locked bars.
3. **No-relabeling preserved (§5.6 apparatus-validity decision tree).** Verify zero-variance/non-finite `ρ_s` cases route to predicate-failure or apparatus-invalid exclusion — NOT automatic `INSTRUMENT_FAILURE`. Per-seed statistical failures must remain predicate failures, not instrument failures.
4. **Item 3 geometry authority.** Verify the geometry grid comes only from `4463cbc` (not its machinery); exact-`(W,N_w)` acceptance; deterministic `Q`-tie; boundary-escalation with "tested boundary" defined exactly as `W ∈ {50,400}` or `N_w ∈ {4,64}`.
5. **DRAFT PI ruling.** Verify it is marked DRAFT (not operative until Rebecca signs), prospectively freezes the table (not claiming prior freezing), and includes the signature block. Until signed, it confers no authority.
6. **Reconciliation / internal consistency.** Verify all five deliverables are consistent (the 3 reconciliation rounds actually reconciled the schema fields, `max_primary_false_kill` null-handling, tie-tolerance binding, and the changelog's SUPERSEDED decisions).
7. **Locked bars unchanged.** Verify β* ≥ 0.2, ρ ≥ 0.8, ≥ 3 doses, 5 seeds are unaltered; `FALSE_KILL_THRESHOLD = 0.10` and the direct formulas unchanged; no locked bar lowered/raised/renamed/reinterpreted/silently replaced.
8. **End-to-end executability.** Verify the complete predicate + per-seed ρ is computable end-to-end (the STOP was resolved by computing ρ in the same estimator path where `D̄` is available, or by extending the per-seed result record); no implementer invention beyond the authorized computation. Re-verify the v2.6 false-CLEAR failure mode does not apply.
9. **Law-fidelity (P1–P6).** Verbatim law quotes (P2); source-class tags (P3) on all new thresholds (`RHO_COMPARE_EPS`, `RHO_BAR`, the diagnostic fields) — note `[PROPOSED]` items are not gating scoring; regime dating (P4); provenance (P6) for the ρ authorization ruling and all cited SHAs.
10. **False-attestation guard.** Verify every claimed fix/feature against the actual file contents at `2082680`, not the commit messages; inspect the 7 commits individually. If any claimed change is absent or superficial, BLOCK.

## Authorized scope

Review only. No scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17 before M5, no implementation, no rerun. Commit the review in-repo on a `critic/` branch per the CRITIC init obligation (PR #92). Include a pre-push scan attestation, branch name, commit SHA, and review file path.

## Output expectations

CLEAR or BLOCK with specific findings (file + §/line). On CLEAR, confirm: the authorized per-seed ρ is within scope and operative; `RHO_COMPARE_EPS` does not soften the locked bar; no-relabeling preserved; Item 3 + DRAFT PI ruling correct; reconciliation consistent; locked bars unchanged; executable end-to-end. The review must also state: whether the **draft PI ruling is suitable for Rebecca's signature**; whether **any remaining Rebecca ruling is needed before TASK BUILDER**; plus branch name, commit SHA, review file path, and pre-push scan attestation. On BLOCK, route back to ARCHITECT.

## Next handoff

- **On CLEAR → Rebecca.** Rebecca signs the geometry-list adoption (the DRAFT PI ruling → operative) — note her signature freezes **only the geometry table for this diagnostic execution**, NOT G2–G4 results, scoring, or final battery acceptance. Rebecca then **separately authorizes TASK BUILDER**; CRITIC CLEAR + the geometry-list signature do NOT automatically release TASK BUILDER without Rebecca's explicit authorization. TASK BUILDER is released only after BOTH (a) this CRITIC clearance AND (b) Rebecca's signature on the geometry-list adoption AND (c) Rebecca's explicit TASK BUILDER authorization. Route: CRITIC → Rebecca → TASK BUILDER.
- **On BLOCK → ARCHITECT only.**

## Pre-push safety scan attestation

Coordinator routing artifact in the project file repo. Contains only public repo SHAs, branch names, file paths, byte sizes, and CRITIC findings relayed from in-repo artifacts. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII. Scan result: **clean** — no blockers, no Rebecca-decision items, acceptable.
