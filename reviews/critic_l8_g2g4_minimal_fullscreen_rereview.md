# CRITIC Re-Review — L8 G2–G4 Minimal Full-Screen Specification (post-remediation)

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**CRITIC commit identity:** `role@moving-origin-research.local` / `MOR ROLE`
**Gate served:** Fresh-context CRITIC re-review of the ARCHITECT's remediation of the L8 G2–G4 minimal full-screen spec after CRITIC BLOCK (`02a7443`). Independent adversarial re-review; no co-authoring of the work under review.
**Branch:** `critic/l8-g2g4-minimal-fullscreen-rereview` (review artifact committed here; branched from `architect/l8-g2g4-minimal-fullscreen` @ `a7b38b3`).

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| GitHub main (base) | `f4e22317ebe0e3e1a7dbee0b81ef8c3fb9839b2b` |
| ARCHITECT branch + HEAD (remediated) | `architect/l8-g2g4-minimal-fullscreen` @ `a7b38b30d5b5875c96b88f32fb80c823c81a992c` |
| Remediation commits | `874097a` (B1 + B2 + NB1–NB4) + `a7b38b3` (B2 wording finalization + §7.1 note) — on top of `8f3e109` |
| ARCHITECT spec files (4) | `specs/l8_g2g4_minimal_full_screen_spec.md`, `_CHANGELOG.md`, `_TASKBUILDER_HANDOFF.md`, `_EXECUTABILITY_TRACE.md` |
| Original CRITIC review (binding findings B1/B2/NB1–NB4) | `reviews/critic_l8_g2g4_minimal_fullscreen.md` @ `02a7443` on `critic/l8-g2g4-minimal-fullscreen` |
| Frozen L8 v2.2 (cited) | `c7d7bed6...` on `architect/l8-instantiation-v2.2-fresh`; path `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` |
| v2.4 geometry-list source | `4463cbc` on `architect/l8-g2g4-remediation` (same path; §8.2 = 20-geometry list; §8.1 = corroborating any-seed-primary text) |
| Verified code baseline | `b1397498...` on `taskbuilder/l8-power-analysis` (`diagnostics/l8_power_analysis.py`) |
| Reference artifact | `6d455bb8...` (`diagnostics/l8_power_analysis_results.json`, SHA-256 `978f21c0…`) |
| Constitution v2 | `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on `main` (`f4e22317`) |

All four ARCHITECT files were inspected at `a7b38b3`, the diff range `8f3e109..a7b38b3` was reviewed, commits `874097a` and `a7b38b3` were inspected individually, and every cited controlling document was re-read at its cited SHA (law-diff and provenance verification performed against actual repo text, not asserted provenance). The original CRITIC review (`02a7443`) was read in full as the binding source of B1/B2/NB1–NB4.

## Verdict

**CLEAR → Rebecca.** No blocking findings remain. B1 and B2 are substantively fixed; NB1–NB4 are addressed; E1–E6 are preserved (verified unchanged). The artifact is internally consistent and executable end-to-end.

The route is CRITIC → Rebecca → TASK BUILDER (Rebecca gates before TASK BUILDER; not CRITIC → TASK BUILDER directly).

## Verification of blocking findings fixed

### B1 — PROVENANCE / INTERNAL-CONSISTENCY (TASK BUILDER handoff) — FIXED

`874097a` corrected `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` "Authoritative inputs" (+3/-3): the §8.2 geometry list and §8.3/§8.4 grids are now cited as **v2.4 `4463cbc`** on `architect/l8-g2g4-remediation`, with frozen **v2.2 `c7d7bed`** cited only for the §2 XF-5 estimator, the per-seed locked bar (line 44), and the 240-cell nuisance/operating grid (§8 items 3–6). The handoff now explicitly states "v2.2 has no §8.2/§8.3 subsections and no 20-geometry sweep — do not look for the geometry list there." Verified against the actual v2.2 `c7d7bed` (§8 is a flat numbered list, no §8.2/§8.3) and v2.4 `4463cbc` (§8.2 line 270 = the 20-geometry `W ∈ {50,100,200,400}` × `N_w ∈ {4,8,16,32,64}` list). The false mis-cite is gone.

The `EXECUTABILITY_TRACE.md` (+6/-6) primary/diagnostic metric rows and the `CHANGELOG.md` (+13) remediation entry are reconciled to the same provenance statement. All four files now carry a single, consistent provenance statement matching spec §0. B1 closed.

### B2 — ACCURACY / MISCHARACTERIZATION (main spec §5.1–§5.3, §7.1) — FIXED

`874097a` qualified §5.1/§5.2/§5.3 (+16/-8) and `a7b38b3` removed the last residual "false-kill rate corresponding to that verdict" wording (+2/-2) and updated the §7.1 `scoring_verdict_alignment_note` schema value. Verified:

- §5.1: `false_kill_rate_per_seed` is now described as the **β\*-predicate direct false-kill rate** — it captures only the standardized-slope < 0.2 predicate of the per-seed scoring verdict. It does **not** count runs killed by the `ρ < 0.8` predicate. It is a **lower bound on the complete scoring-verdict false-kill rate**, not the full rate. The complete verdict also requires (in v2.4 §8.1) direction + pooled-bootstrap interval `[BAR-Entry 11.3]`, which this minimal spec deliberately does not compute (no bootstrap; §1.3). `[PROPOSED — primary metric; NF-IMPL-2 in b139749]`.
- §5.2: a "Scope of the primary metric" note and a "Corroborating source" note (v2.4 §8.1 corroborating only; v2.2 line 44 primary) are added.
- §5.3: the mismatch-memorialization now states the primary metric is the β\*-predicate direct rate — a lower bound on the complete scoring-verdict rate — and flags this for Rebecca's §5.3 review.
- §7.1: `scoring_verdict_alignment_note` value changed to "primary is the β\*-predicate direct any-seed rate; seed aggregation follows v2.2 line 44; lower bound on complete-verdict false-kill rate; see §5.2-§5.3."

Verified against `b139749` code line 808: `false_kill_rate_per_seed = float(np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1)))` = `P(any seed β*_s < 0.2)` — the β\*-predicate portion only. The spec's characterization now matches what the code computes. No residual overstatement ("corresponds to the actual scoring verdict" / "scoring-verdict-aligned") remains in the diff. B2 closed.

## Verification of non-blocking findings addressed

- **NB1 (spec §5.2):** v2.4 §8.1 (`4463cbc`, line 266) is now cited as corroborating context ("The primary false-kill rate is [complete-verdict any-seed rate]… The former five-seed-mean measure… may not gate battery size or selection"), with v2.2 line 44 remaining the primary frozen authority and v2.4 §8.1 corroborating only; the pooled-bootstrap predicate `[BAR-Entry 11.3]` is noted as deliberately omitted. Verified against v2.4 source. Addressed.
- **NB2 (spec §5.1, §5.4, §7.2):** the primary metric is now tagged `[PROPOSED]` (NF-IMPL-2 in `b139749`), and geometry acceptance (`meets_target` / minimum acceptable battery) is explicitly stated to be a `[PROPOSED]`-gated diagnostic selection requiring Rebecca sign-off before binding/downstream use. The TASK BUILDER is instructed to record the output artifact's own SHA-256 in the run handoff (§7.2). Addressed.
- **NB3 (spec §1.3):** the "closes the two `d08cb7e` details" framing is corrected — it now states `d08cb7e`'s two open execution details concerned the 1,000-repetition feasibility diagnostic (a different workload), and the screening-run parameters come from the later COORDINATOR handoff; `d08cb7e`'s authorization boundary remains correct. Addressed.
- **NB4 (spec §5, §1.3):** the inherited `[Sol-XF-5]` closure labels are re-tagged as `[OP — Sol-XF-5, adopted operationalization]` (an adopted `[OP]`-class closure label, with the crossfamily closure label `Sol-XF-5` retained for traceability). This is one of the two remediation options the original CRITIC review (NB4) explicitly offered ("either re-tag as `[OP-Entry n]` (adopted operationalization) or confirm `[Sol-XF-*]` is an adopted `[OP]`-class closure label"). The numeric thresholds (0.2, 0.10, 5 seeds, ρ ≥ 0.8) remain `[BAR-Entry 11]` / `[PROPOSED]`. Addressed; not a P3 block.

## Preserved evidence (verified unchanged)

- **E1 — PRIMARY designation.** `PRIMARY = false_kill_rate_per_seed` (any-seed) / `DIAGNOSTIC = false_kill_rate` (5-seed mean) is textually grounded (v2.2 line 44 "per seed"; corroborated by v2.4 §8.1). The ARCHITECT did not re-designate or STOP. Verified unchanged in the diff. The remediation only qualified *how* the primary metric is described (B2), not *which* metric is primary.
- **E2 — P2 law-diff.** Spec §1.2 verbatim quotes of L8 and §5 P1–P6 are unchanged by the remediation. Re-diffed against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on `main` (`f4e22317`): §5 5.1 P1–P6 (constitution lines 130–135) and L8 (constitution line 28) match character-for-character. No reconstruction of constitutional text. P2 satisfied.
- **E3 — Two-arm workload and timing.** The 19.2M two-arm accounting (9.6M combo + 9.6M null) and ~90.5 min / 1.5–2 h timing are unchanged in the diff. (Previously verified against `b139749` code and reference artifact `6d455bb`; not altered by the remediation, which is confined to B1/B2/NB1–NB4 areas.) Verified unchanged.
- **E4 — Geometry-list provenance in §0.** Spec §0 still correctly identifies `4463cbc` (v2.4) as the only located repo source of the pre-registered 20-geometry list. Verified unchanged; B1 fixed the handoff's contradiction of §0, not §0 itself.
- **E5 — No prohibited machinery.** No bootstrap, Wilson, A1/A2/B, rehearsal, fault-injection, sensitivity-map, `(C_min,η)` selection, scoring, or protected-seed machinery was added. The diff introduces only provenance corrections, scope/accuracy qualifications, tag changes, and additive notes. PASS.
- **E6 — End-to-end executability.** Schema structure, field order, paths, cell ordering, deterministic seed derivation, calibration reference point, worker count, and the reference artifact SHA-256 are unchanged. The only schema-value change is the `scoring_verdict_alignment_note` string (§7.1) and additive `P3_source_tags`/tag-convention notes. The v2.6 false-CLEAR failure mode (undefined fixture / committed artifact pair / estimator realizations) does not apply: the fixture (W=50, N_w=4 reference), the exact JSON schema (§7.1), the seed derivation, and the reference digest are all concretely specified. The spec remains executable end-to-end with no implementer invention beyond the flagged primary/diagnostic designation (routed to Rebecca). PASS.

## Diff scope confirmation

The diff `8f3e109..a7b38b3` touches exactly four files, with change volumes confined to the B1/B2/NB1–NB4 fix areas: `spec.md` +17/-9, `CHANGELOG.md` +13/-0, `EXECUTABILITY_TRACE.md` +6/-6, `TASKBUILDER_HANDOFF.md` +3/-3. No new files, no schema structure / path / field order / metric identity / formula changes. The remediation did not alter E1–E5, the verbatim law quotes, or the executable core.

## False-attestation guard

Every claimed fix was verified against the actual file contents at `a7b38b3`, not the commit message. The two commits were inspected individually: `874097a` (B1 + B2 + NB1–NB4 across four files) and `a7b38b3` (B2 wording finalization, spec +2/-2 only). The ARCHITECT init's verification obligations (pre-commit verification, diff self-inspection, attestation integrity) held here — the changelog's claimed fixes match the diff. The false-attestation pattern (prior v2.2 ARCHITECT) did not recur.

## Explicitly prohibited actions

No scoring. No protected-seed access. No seeds 201–203 / 301–303. No G2–G4 freeze or ruling by ARCHITECT. No merge to main (CRITIC commits only to `critic/l8-g2g4-minimal-fullscreen-rereview`). No L15/L16/L17 before M5. No implementation. No rerun. No exposing of hold-out seeds. No rerunning of failed scoring. No lowering, raising, renaming, reinterpreting, or silently replacing a locked bar. CRITIC did not edit the spec, changelog, TASK BUILDER handoff, executability trace, or STATE.md. CRITIC did not co-author, fix, or modify the work under review.

## Confirmation

No scoring was conducted. No hold-out or protected seeds were accessed or exposed. No failed scoring was rerun. No merge to `main` occurred. No verdict was returned before the review was committed in-repo and pushed. The CRITIC's review is backed by a committed artifact on `critic/l8-g2g4-minimal-fullscreen-rereview` (see commit SHA in handoff). Law-diff (P1/P2), source-class tags (P3), regime dating (P4), no-deviation (P5), and provenance-citation verification (P6) were performed as the first checklist item.

## Pre-push self-scan attestation

A pre-push self-scan was performed on the review artifact and the branch contents for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths (e.g., `/home/user/workspace/...`), environment dumps, and PII.

Findings: **none.** The review contains only public repo SHAs, branch names, file paths, byte sizes, verbatim constitutional/spec text already in the public repo, and CRITIC analysis. No private paths, credentials, or PII. Scan result: **clean — no blockers, no Rebecca-decision items, acceptable.**

---

*CRITIC re-review complete and committed in-repo. This file is the binding artifact; the handoff message is a pointer to it.*
