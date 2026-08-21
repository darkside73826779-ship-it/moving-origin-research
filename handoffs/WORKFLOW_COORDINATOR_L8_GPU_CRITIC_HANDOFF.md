# WORKFLOW COORDINATOR → CRITIC Handoff — L8 GPU Diagnostic-Backend Adoption Review

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** Fresh-context CRITIC review of the ARCHITECT's L8 GPU diagnostic-backend adoption spec (Part A law-fidelity + Part B substantive + CPU↔GPU equivalence).
**Next recipient:** On CLEAR → **Rebecca** (clears the reviewed spec; full-run release requires her explicit release per the GPU rebuild ruling PR #105). On BLOCK → **ARCHITECT only**.

## Authority and scope

The ARCHITECT completed the L8 GPU diagnostic-backend adoption spec and routed it for fresh-context CRITIC review. This handoff is prepared for Rebecca to transport to the CRITIC. Independent adversarial review — verify against the actual diff, not commit messages (false-attestation guard below).

Authority chain: Rebecca > constitution laws > approved specifications > this handoff > agent judgment. The CRITIC does not choose scientific rules; it verifies fidelity, equivalence, consistency, and executability.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub main (base) | `b6d4556` (PR #105 merged) |
| ARCHITECT branch + HEAD | `architect/l8-gpu-adoption-spec` @ `7c0a3c7` |
| ARCHITECT commits | `1bf7654` (full GPU L8 comparison results), `60c4202` (GPU adoption approval handoff), `afc5492` (GPU diagnostic equivalence gate), `8f945c7` (route for review), `60a5acf` (combine law+substantive review; spec v1.1), `7c0a3c7` (route through fresh-context CRITIC) |
| ARCHITECT's CRITIC handoff | `handoffs/ARCHITECT_L8_GPU_ADOPTION_CRITIC_HANDOFF.md` @ `7c0a3c7` (specifies Part A + Part B) |
| GPU adoption spec (v1.1) | `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.1.md` (v1.1 commit `60a5acf`) |
| Changelog | `specs/l8_gpu_diagnostic_backend_adoption_spec_CHANGELOG.md` |
| Frozen-calibration artifact | `specs/data/l8_cpu_frozen_calibration_v1.json` |
| GPU evidence (CPU↔GPU comparison packet) | `1bf7654` |
| CPU implementation | `b139749` |
| CPU evidence (reference) | `6d455bb` (SHA-256 `978f21c0…`) |
| Rebecca GPU rebuild ruling | `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` on main |
| Amended (CPU) spec (authoritative) | `architect/l8-g2g4-minimal-fullscreen` @ `2082680` |

**Inspect the spec v1.1, changelog, frozen-calibration artifact, and the ARCHITECT's CRITIC handoff at `7c0a3c7`.**

## What the ARCHITECT asserts (verify each against the diff)

- The spec v1.1 is **PROPOSED**; inoperative pending the combined CRITIC ruling and Rebecca's clearance.
- **CPU↔GPU equivalence:** native GPU calibration differed from CPU at 4 of 15 pairs, maximum absolute sigma difference `0.74999375`; two misspecification profiles selected different exact coordinates. The ARCHITECT asserts **neither negative is renamed or used as a retrospective tolerance**.
- The GPU path reproduces CPU β*/ρ within the locked-bar comparison tolerance (`RHO_COMPARE_EPS = 1e-12`) for identical seeds; repeat-run determinism.

## Review focus (verify each against the diff)

1. **Part A — law fidelity (before substantive review):** diff the three law quotations in the spec against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; verify every numeric threshold, kill condition, and test criterion has an allowed source tag (`[LAW-Lx]`/`[BAR-Entry n]`/`[OP-Entry n]`/`[PROPOSED]`); verify Entry 11, Entry 12, and Entry 22 claims against `docs/rulings/provenance_log.md`. Report exactly `LAW_FIDELITY: PASS` or `LAW_FIDELITY: BLOCK` (a block stops clearance).
2. **Part B — substantive falsification (only after Part A passes):** falsify the logical RNG mapping; one-generator-per-logical-seed feasibility; maximum-capacity parallelism; Bonferroni family definition; interval algorithms; numeric margins; complete-verdict implementation; map and tie handling; L18 fixture availability; apparatus-failure exclusivity; atomic sidecar semantics; two-commit identity; and absence of unresolved TASK BUILDER choices. Report exactly `SUBSTANTIVE: CLEAR` or `SUBSTANTIVE: BLOCK`.
3. **CPU↔GPU equivalence is genuine:** verify the 4/15 native-calibration difference (max `0.74999375`) and the two misspecification-profile coordinate divergences are correctly handled — **not renamed, not used as a retrospective tolerance** (no-relabeling; anti-score-chasing). Verify the GPU reproduces CPU β*/ρ within `RHO_COMPARE_EPS` for identical seeds and that repeat-run determinism holds.
4. **Equivalence to the amended (CPU) spec:** the GPU spec must preserve the same PRIMARY (`complete_verdict_false_kill_rate`), schema, locked bars (β* ≥ 0.2, ρ ≥ 0.8, ≥ 3 doses, 5 seeds), 7 tests + 2a, seed derivation, no-relabeling, no bootstrap/Wilson/quorum/fallback, O-15, no scoring — per the GPU rebuild ruling.
5. **False-attestation guard:** verify every claimed result/fix against the actual file contents at `7c0a3c7`, not the commit messages; inspect the 6 commits individually. If any claimed change is absent or superficial, BLOCK.

## Constraints (binding)

O-14 (no re-run; seeds 201–203/301–303 never rerun), O-15 (diagnostic-only), D1–D5, L9, L18, candidate-blindness (Ruling 9), no-relabeling, no bootstrap/Wilson/quorum/fallback, no scoring, no protected-seed access/exposure, no merge to main, no L15/L16/L17 before M5, no native-GPU-calibration adoption as a retrospective tolerance, no CPU replacement, no automatic rerun/fallback. Commit the review in-repo on a `critic/` branch per the CRITIC init obligation (PR #92). Include a pre-push scan attestation, branch name, commit SHA, and review file path.

## Combined ruling

CRITIC may return overall `CLEAR` only with `LAW_FIDELITY: PASS` AND `SUBSTANTIVE: CLEAR`. Findings must be labeled blocking or non-blocking; negative evidence must remain named.

## Next handoff

- **On CLEAR → Rebecca.** Rebecca clears the reviewed spec. The full 19.2M GPU diagnostic execution requires ARCHITECT approval (done) + CRITIC clearance + Rebecca's explicit release (per the GPU rebuild ruling PR #105 — does NOT auto-release post-clear). Route: CRITIC → Rebecca → (release) → TASK BUILDER run → INTEGRATOR → CRITIC (impl review) → RECORDER → Rebecca.
- **On BLOCK → ARCHITECT only.**

## Pre-push safety scan attestation

Coordinator routing artifact. Contains only public repo SHAs, branch names, file paths, and the ARCHITECT's findings relayed. No credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, or PII. Scan result: **clean** — no blockers, no Rebecca-decision items, acceptable.
