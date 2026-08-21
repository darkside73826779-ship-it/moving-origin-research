# WORKFLOW COORDINATOR → ARCHITECT Handoff — L8 GPU Adoption Spec Remediation (CRITIC BLOCK)

**Date:** 2026-08-20 · **Regime:** B `[P4]`
**Gate served:** ARCHITECT remediation of the L8 GPU diagnostic-backend adoption spec v1.1 after CRITIC BLOCK.
**Next recipient:** ARCHITECT (originating role). On completion, re-route to fresh-context CRITIC → Rebecca.

## Authority and scope

The fresh-context CRITIC reviewed the ARCHITECT's L8 GPU adoption spec v1.1 (`architect/l8-gpu-adoption-spec` @ `7c0a3c7`) and returned **BLOCK → ARCHITECT only** (Part A law-fidelity PASS; Part B substantive BLOCK). This handoff is prepared for Rebecca to transport to the ARCHITECT. Specification remediation + review only — no implementation, scoring, protected-seed exposure, or merger.

Authority chain: Rebecca > constitution laws > approved specifications > this handoff > agent judgment. The ARCHITECT specifies, not produces. If a directive conflicts with a locked law, STOP and report.

## Authoritative inputs

| Item | Value |
|---|---|
| GitHub main (base — **must rebase onto this**) | `b6d4556` (PR #105) |
| ARCHITECT branch (remediate here) | `architect/l8-gpu-adoption-spec` @ `7c0a3c7` |
| CRITIC review (binding findings B1–B8) | `reviews/critic_l8_gpu_adoption.md` @ `6e408ae` on `critic/l8-gpu-adoption-review` |
| Spec v1.1 + changelog + frozen-calibration artifact | `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.1.md`, `_CHANGELOG.md`, `specs/data/l8_cpu_frozen_calibration_v1.json` |
| GPU evidence (comparison results) | `1bf7654` |
| CPU comparator | `b139749` (does NOT compute per-seed ρ — the ARCHITECT's own STOP finding `dc3185a`) |
| Controlling (CPU) spec | `architect/l8-g2g4-minimal-fullscreen` @ `2082680` |
| Rebecca GPU rebuild ruling (must be in the tree — see B8) | `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` on main `b6d4556` |
| Rebecca Item-1 ρ authorization (must be in the tree — see B8) | `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` |
| Rebecca geometry-table freeze ruling | `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` on main |

**Read the CRITIC review (`6e408ae`) in full — it is the binding source of B1–B8 with exact recomputations.** Every CRITIC claim below was independently recomputed from committed artifacts, not commit messages.

## CRITIC verdict: BLOCK → ARCHITECT only

Part A (law-fidelity) PASS. Part B (substantive) BLOCK. The spec is internally consistent but **not executable end-to-end** and **does not preserve the controlling CPU spec's predicate semantics**.

## Blocking findings (as found by the CRITIC) — remediate all

- **B1 — locked-bar comparison semantics omitted.** The GPU spec v1.1 has zero occurrences of `RHO_COMPARE_EPS`, zero `undefined`, no comparison-tolerance rule; §5 is the bare conjunction `beta_star >= 0.2 AND rho >= 0.8`. The controlling CPU spec (`2082680:§5`) locks `ρ_s >= 0.8 OR abs(ρ_s − 0.8) <= RHO_COMPARE_EPS (1e-12)` + the no-softening test (0.8 − 2·eps fails). Implemented as written, the documented threshold case `D̄=[1,0,2,3]` (ρ = 0.7999999999999999) **passes** on CPU but **fails** on GPU — an upward movement of the locked 0.8 bar on the GPU path only (prohibited by §16 + Rebecca's Item-1 authorization). Also omits the `undefined ρ_s` disjunct Rebecca's directive fixes verbatim ("P(any seed has β*_s < 0.2 OR undefined ρ_s OR ρ_s < 0.8)"; "zero response-rank variance → ρ undefined → failure of the ρ predicate, not INSTRUMENT_FAILURE"). **Fix:** adopt the controlling spec's `RHO_COMPARE_EPS` comparison rule + no-softening test verbatim; add the undefined-ρ disposition (predicate failure, NOT INSTRUMENT_FAILURE) so the TASK BUILDER has no prohibited branch.
- **B2 — the designated CPU comparator cannot compute the compared endpoints.** §5 designates `b139749` as THE CPU comparator, but §9.1's primary family requires mean ρ, complete-verdict false-kill, and complete-verdict null false-pass — none of which `b139749` computes (zero occurrences of `rho`/`spearman`/`midrank`/`complete_verdict`/`any_seed`). This is the ARCHITECT's own STOP finding (`dc3185a`). The GPU side has a `_rho` implementation; the CPU side has none. **Fix:** either extend the CPU comparator to compute the ρ-bearing endpoints (under Rebecca's Item-1 ρ authorization), or designate a comparator that can; reconcile the asymmetry.
- **B3 — RNG logical-seed reduction guarantees duplicate seeds.** §6 SHA-256s an identity then reduces mod `2^31`; 28.8M identities → ~193,119 colliding pairs → P(no collision) ≈ 0. Either the uniqueness check (§11 check 3) guarantees `INSTRUMENT_FAILURE` by construction, or it's trivially satisfied with ~193,000 pairs silently sharing a generator seed (contradicting §6's "separate generator stream per logical seed"). **Fix:** use a 64-bit seed (`torch.Generator.manual_seed` accepts 64-bit) or a counter-based substream; resolve the uniqueness-check ambiguity.
- **B4 — L18 parity fixtures don't exist; the spec mandates a STOP.** §12 requires committed CPU definitions for empty/permuted/shuffled/oracle/frozen/naive; `b139749` has none (only reference/null/two-misspecified arms; no L18 control battery). The spec's own §12 mandates the TASK BUILDER STOP. **Fix:** either commit the L18 fixtures or scope §12 to arms that exist; don't mandate an unsatisfiable precondition.
- **B5 — fixtures, artifact pairs, schemas, expected digests deferred to the implementer.** §12/§13 name no rehearsal fixture (no W, N_w, coordinates, calibration source, repetition count, RNG namespace, result schema/ordering, expected canonical digest, sidecar filename, expected SHA-256). This is the v2.6 false-CLEAR defect class (the TASK BUILDER would have to invent them). **Fix:** fix every fixture, schema, field order, canonicalization, and expected digest in the spec.
- **B6 — per-logical-seed CUDA generator conflicts with mandated maximum-capacity parallelism.** §6 requires one `torch.Generator` per logical seed + maximum-capacity parallelism + "serial comparison prohibited"; 28.8M generator constructions with no batching/substream/counter mechanism. The committed GPU evidence used a single cell-wide CUDA stream; the TASK BUILDER proposed counter-based substreams — the pre-registered RNG architecture is untested and unreconciled. **Fix:** specify a batching/substream/counter mechanism reconciling per-seed isolation with device-saturating parallelism.
- **B7 — Wilson-derived interval prescribed under a no-Wilson constraint.** §9.1 prescribes `statsmodels.confint_proportions_2indep(method="newcomb", ...)`; the Newcombe hybrid-score interval is constructed from Wilson score intervals. The no-bootstrap/Wilson/quorum/fallback constraint + Rebecca's Item-1 authorization prohibit Wilson; no P5 deviation memorialization (Rebecca's signed waiver) exists. **Fix:** either cite the authorization scoping the prohibition to the predicate path, or specify a construction that does not rely on a prohibited procedure.
- **B8 — provenance: branch is not based on the named base; omits Rebecca's operative rulings.** The handoff names main `b6d4556` as base, but `b6d4556` is NOT an ancestor of `7c0a3c7` (actual merge-base `f4e2231`). The reviewed tree omits `REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md`, `REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md`, and `REBECCA_L8_GEOMETRY_TABLE_FREEZE.md`. **Fix:** rebase the branch onto `b6d4556` (or rebase onto main so the operative rulings are in the tree); correct the base citation.

## What NOT to change (CRITIC-verified, preserved)

- Part A PASS: the three law quotations (L8, L18, L19) are verbatim; source-class tags correct; Entry 11.3/12/22 provenance verified; locked bars (β* ≥ 0.2, ρ ≥ 0.8, ≥ 3 doses, 5 seeds) unchanged — do not move them.
- The frozen-calibration artifact (`specs/data/l8_cpu_frozen_calibration_v1.json`) — fully verified; keep.
- The retained `0.74999375` finding + the two misspecification-profile coordinate divergences — correctly NOT renamed/retrospective-toleranced; keep.

## Constraints

O-14, O-15 (diagnostic-only), D1–D5, L9, L18, candidate-blindness (Ruling 9), no-relabeling, no bootstrap/Wilson/quorum/fallback unless separately authorized (P5 memorialization), no scoring, no protected-seed access, no G2–G4 freeze, no merge to main, no L15/L16/L17 before M5, no native-GPU-calibration adoption as retrospective tolerance, no CPU replacement, no automatic rerun/fallback.

## Output expectations

Return handoff: (1) remediated spec v1.2 (B1–B8 fixed); (2) branch rebased onto `b6d4556` (B8); (3) confirmation the locked bars, law quotations, and frozen-calibration artifact are unchanged; (4) branch + commit SHA. **False-attestation guard:** the CRITIC recomputed every claim from artifacts, not commit messages — the ARCHITECT must ensure each fix is actually present in the diff, not just the changelog (prior v2.2 false-attestation precedent).

## Next handoff

ARCHITECT → fresh-context CRITIC → Rebecca. TASK BUILDER not released. Full-run release still requires ARCHITECT approval + CRITIC clearance + Rebecca's explicit release (GPU ruling PR #105).

## Pre-push safety scan attestation

Coordinator routing artifact. Contains only public repo SHAs, branch names, file paths, and CRITIC findings relayed. No credentials/secrets/PII/private paths. Scan result: **clean**.
