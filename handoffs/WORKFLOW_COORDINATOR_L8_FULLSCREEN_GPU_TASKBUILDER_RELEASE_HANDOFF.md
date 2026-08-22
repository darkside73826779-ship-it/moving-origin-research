# WORKFLOW COORDINATOR → TASK BUILDER Handoff — L8 Full-Screen GPU Diagnostic Release (Rebecca-authorized)

**Date:** 2026-08-21 · **Regime:** B (post-Entry 81; `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5 binding) `[P4]`
**Gate served:** TASK BUILDER release to execute the 19.2M full-screen GPU diagnostic under the operative L8 GPU adoption pre-registration.
**Next recipient:** TASK BUILDER. Route after the run: TASK BUILDER → INTEGRATOR → CRITIC (implementation review) → RECORDER → Rebecca.

---

## Authorization (Rebecca, 2026-08-21 00:54–00:56 EDT)

All three release gates are satisfied:

1. **Pre-registration SIGNED** — Rebecca approved the L8 GPU adoption `[PROPOSED]` criteria as a pre-registration (2026-08-21 00:54 EDT). The contract (spec v1.4) is operative.
2. **Full-screen GPU run RELEASED** — Rebecca's explicit release under the GPU rebuild ruling ([PR #105](https://github.com/darkside73826779-ship-it/moving-origin-research/pull/105)) (2026-08-21 00:56 EDT).
3. **TASK BUILDER RELEASED** — Rebecca's explicit TASK BUILDER authorization (distinct gate per the geometry-table freeze ruling, `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md`) (2026-08-21 00:56 EDT).

Rebecca's approval ruling is recorded at `docs/rulings/REBECCA_L8_GPU_PREREG_AND_FULLSCREEN_RELEASE.md` (companion commit to this handoff).

## Authoritative inputs

| Item | Value |
|---|---|
| Operative pre-registration (spec v1.4, CRITIC-cleared) | `architect/l8-gpu-adoption-spec` (v1.4, the SHA named in the ARCHITECT's v1.4 return handoff) |
| CRITIC v1.4 re-clear (CLEAR) | `reviews/critic_l8_gpu_adoption_v1.4_rereview.md` on `critic/l8-gpu-adoption-v1.4-rereview` |
| Controlling (CPU) spec | `architect/l8-g2g4-minimal-fullscreen` @ `2082680` |
| GPU rebuild ruling | `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` (main, PR #105) |
| Geometry-table freeze ruling | `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` (main) |
| Item-1 ρ authorization | `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` |
| CPU comparator baseline | `b139749` |

## Authorized scope

- Implement and execute exactly what the operative v1.4 pre-registration specifies: the CPU↔GPU equivalence sentinel (including the repeat-determinism gate and rehearsals) and the 19.2M full-screen GPU diagnostic on Rebecca's workstation.
- **Diagnostic-only (O-15).** Outputs are advisory inputs; synthetic candidate-blind seeds only.
- Follow the pre-registration's committed fixtures, schemas, digests, seed derivation, RNG identity, publication and recovery semantics exactly — the spec is executable end-to-end; there is nothing to invent. If any executable input is genuinely undefined, STOP and route back (do not invent — the stop discipline is the correct behavior).

## Explicitly prohibited

No scoring. No scoring-mode execution. No protected/hold-out/courier seed access (seeds 201–203 and 301–303 never accessed or rerun — O-14). No re-run of any failed run (O-14; the sentinel's own no-third-execution rule applies as specified). No renaming of negatives. No relabeling of statistical failures as INSTRUMENT_FAILURE (apparatus-validity checks only). No bar moved, raised, lowered, renamed, or reinterpreted. No spec-text changes (P5 — signed waiver required). No native GPU calibration or torch-native RNG adoption. No CPU replacement. No automatic retry/fallback. No G2–G4 freeze. No merge to main. No L15/L16/L17 work before M5.

## Output expectations (return handoff)

1. Branch + result SHA with the committed run artifacts per the pre-registration's schemas and output paths.
2. Sentinel/equivalence packet results (all cases, repeat-determinism verdict) and the full-screen results artifact with digests.
3. Any STOP events, deviations, or apparatus findings — named plainly, nothing renamed.
4. Public-repo safety scan attestation (no credentials/PII/machine identifiers/private paths/protected seeds).

## Next handoff chain

TASK BUILDER → INTEGRATOR → CRITIC (implementation review) → RECORDER → Rebecca.

## Pre-push safety scan attestation

Coordinator routing artifact. Contains only public repo SHAs, branch names, file paths, ruling references, and routing instructions. No credentials/secrets/PII/private paths. Scan result: **clean**.
