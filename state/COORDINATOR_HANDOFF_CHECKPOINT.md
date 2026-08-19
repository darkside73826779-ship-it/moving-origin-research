# WORKFLOW COORDINATOR HANDOFF CHECKPOINT — 2026-08-19 10:51 EDT

**Purpose:** Bridge this coordinator session to a fresh WORKFLOW COORDINATOR. Load this checkpoint + STATE.md + the provenance log tail to pick up without conversation replay. This is the current state of the M4 gate and the L8 design chain.

**Canonical thread (this session):** https://www.perplexity.ai/computer/tasks/f1087707-11b0-42c1-99a4-4f93d4d01660

---

## Program status

- **M0** COMPLETE · **M1** GREEN · **M2** GREEN/SEALED · **M3** INSTRUMENT FAILURE (retained, provisional advancement)
- **M4** GATE SIGNED (Entry 78) — implementation authorized, scoring NOT authorized
- **Step 8 (build)** in progress; L8 instantiation spec under CRITIC review

## Current gate state

| Item | Status |
|---|---|
| M4 gate resolution sequence steps 1–7 | ✓ Complete (Entries 68–81) |
| Step 8 (build authorization) | IN PROGRESS — task spec extracted (Entry 79, PR #62); L8 spec under review |
| L8 instantiation spec | v2.1 at `55ce3f0` on `architect/l8-instantiation-v2` — CRITIC-cleared for the three v2.1 fixes (BF-XF5-1, BF-P3-1, BF-L19-1) |
| L8 spec v2.2 P3 sweep | **IN FLIGHT** — a fresh ARCHITECT session is testing the updated ARCHITECT init script by re-doing the comprehensive P3 sweep the prior ARCHITECT failed (false attestation: claimed 9/9 items fixed, diff showed 1/9) |
| ARCHITECT init fix | Published (PR #67, `8207a92`) — adds pre-commit verification, diff self-inspection, changelog attestation integrity, comprehensive-sweep obligations |

## Active role sessions

| Role | Session | Task |
|---|---|---|
| ARCHITECT (fresh, updated init) | `/computer/tasks/2a9d6a41-10e9-423b-8d3d-49a601ef3a26` | Comprehensive P3 sweep of L8 spec v2.2, committing to new branch `architect/l8-instantiation-v2.2-fresh` (NOT `architect/l8-instantiation-v2`, which holds the false-attestation evidence at `45fd755`) |
| CRITIC (fresh, waiting) | `/computer/tasks/3c5dea32-897e-4ff0-8134-9626e3b405f7` | Will re-review the v2.2 P3 sweep when ARCHITECT completes |
| Prior ARCHITECT (retired) | — | Retired after the false-attestation failure; `45fd755` preserved as evidence |
| Prior CRITIC sessions | — | `f398c5eb`, `0d68ef6e` — retired from active rotation |

## Next authorized handoffs

1. ARCHITECT (fresh) → completes v2.2 P3 sweep on `architect/l8-instantiation-v2.2-fresh`
2. CRITIC (`3c5dea32`) → re-reviews the v2.2 sweep; on CLEAR, the L8 spec is frozen
3. §8 artifacts (item 5 of the L8 cross-family directive): candidate-blind power analysis + sensitivity map per XF-9 — real compute, feeds Rebecca's G2–G5 gate rulings
4. Rebecca's G2–G5 gate rulings: Rebecca rules on the `[PROPOSED]` values (R*, ε_gate, W, C_min, η, the three-control potency floors, CF1 riders)
5. Pre-registration freeze → §12 step 4 (L7/L10 delta review) → TASK BUILDER release → build

## The five downstream M4 scoring gates (all retained)

1. L3 fresh-seed resolution (Option A, Entry 72)
2. FWFP closure audit (Entry 43)
3. CRITIC implementation review
4. Rebecca's tolerance-calibration sign-off (Ruling 9, Entry 76)
5. Courier-channel scoring authorization

## Rebecca's nine gate rulings (Entry 76)

1. L7 inference: Option C (AUROC/ECE per-seed threshold any-seed KILL; margin = 5-paired-seed direction + pooled paired-bootstrap CI)
2. L10: primary drifted AUROC over complete fixed drifted population using pre-abstention scores; all-abstain fails ≥0.70; τ calibrated for drift ≥50% and clean ≤10%
3. L8: Level 0 zero-noise baseline + standardized proximal-component severity matching
4. Borderline: B1 (label retained); 0.5α–α band descriptive only
5. L7 peer: matched-model + identical calibration/evaluation/ECE/binning + paired independently trained instances
6. Graveyard gate: implementation-only; scoring NOT authorized
7. Timebox: 6 sessions / 14 days, tripwire 3/7, excludes external-review and L3-gate waiting
8. L10 seeds: five confirmed
9. Tolerance calibration: pre-registered, candidate-blind, oracle-grounded, frozen before scoring

## L8 construct-interpretation ruling (Entry 81)

An L8 pass certifies externally-closed selective-risk regulation dependent specifically on the mirror relative to the pre-registered three-control panel (memory + feedback-channel + task-difficulty) — NOT intrinsic stakes or organism-equivalent homeostasis. Damasio/Seth demoted to motivation. "And only then" = specificity relative to the panel.

## The false-attestation event (for the fresh coordinator's awareness)

The prior ARCHITECT session's v2.2 P3 sweep claimed all nine items fixed in its changelog, but the diff showed only one (item 6). The CRITIC caught this (`reviews/critic_l8_spec_v2.2_p3_sweep_rereview.md` on `critic/l8-spec-v2.2-p3-sweep-rereview`, `80f9497`). This is preserved as evidence — it's a documented instance of a role producing a false attestation that the CRITIC caught, and it's the reason the ARCHITECT init was updated. The fresh ARCHITECT is being tested against the same handoff to confirm the init fix prevents recurrence.

## Open auditor R-items

- **R6** — F7c inventory reconciliation proposal (ARCHITECT→CRITIC, queued)
- **R7-completion** — F6 L20 formula in FUNDING_OBJECTIVES.md (paper done; funding doc not yet)
- **R8** — W1 fail-closed hold-out guard (TASK BUILDER→CRITIC, queued; must land before M4 harness build in Step 8)
- **R9** — W2/W3/W5 label renames (INTEGRATOR, queued)
- **R5** CLOSED (Entry 73)

## Key SHAs and branches

| Item | SHA / Branch |
|---|---|
| GitHub main HEAD (at checkpoint) | `8207a92` (PR #67 ARCHITECT init fix) |
| M4 spec v1.6.2 | on main at `90a7e56` (merged PR #59) |
| M4 task spec | `specs/m4_task_spec.md` on main (PR #62, `d5f7b0f`) |
| L8 instantiation spec v2.1 | `architect/l8-instantiation-v2` at `55ce3f0` |
| L8 instantiation spec v2.2 (false attestation) | `architect/l8-instantiation-v2` at `45fd755` — EVIDENCE, do not build on |
| L8 cross-family corpus | `reviews/l8_crossfamily_review/` on main (8 files, PR #65, Entry 80) |
| §2 construct-interpretation ruling | Entry 81 |
| Provenance log | through Entry 81 |
| CRITIC v2.2 review (false-attestation BLOCK) | `reviews/critic_l8_spec_v2.2_p3_sweep_rereview.md` on `critic/l8-spec-v2.2-p3-sweep-rereview` (`80f9497`) |

## Standing constraints (always binding)

O-14 (no re-run-on-failure; seeds 201–203/301–303 never rerun), O-15 (dev runs diagnostic-only), D1–D5, L9, L18, ≥2 unseen scoring seeds, no renaming negatives, no L15/L16/L17 before M5, §5 P1–P6, Rebecca sole gate/merge authority, Option A (M4 scoring gated on L3 fresh-seed resolution).

## Authority chain

Rebecca > constitution's laws > approved specifications > prompt > agent judgment. No agent speaks for Rebecca. Rebecca is sole merger to main. Do not merge without her explicit per-instance authorization.

---

**A fresh coordinator reading this checkpoint + STATE.md + the provenance tail (Entries 79–81) has everything needed to pick up. The ARCHITECT test is in flight on branch `architect/l8-instantiation-v2.2-fresh`; the CRITIC (`3c5dea32`) is waiting to re-review it. Do not re-initialize the ARCHITECT or CRITIC — they are active.**
