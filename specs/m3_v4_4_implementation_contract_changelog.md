# M3 V4.4 Implementation-Completeness Amendment — Changelog

**Gate served:** M3 V4.4 Implementation-Completeness Amendment Gate

**Authoritative base:** `45736cb` (GitHub main)

**Date:** 2026-08-16

**Author:** ARCHITECT

---

## Origin

TASK BUILDER returned a SPECIFICATION BLOCK on the V4.4 amendment implementation, correctly stopping rather than inventing unauthorized specification rules. WORKFLOW COORDINATOR routed the block to ARCHITECT (per Rebecca's routing instruction, 2026-08-16 19:24 EDT) to prepare a narrow implementation-completeness amendment.

## Seven contracts defined

| # | Gap | Contract | Key decisions |
|---|---|---|---|
| 1 | Gaussian generation from SHA-256 stream (PRIMARY BLOCK) | §1 of amendment | Box–Muller transform: two 53-bit mantissa uniforms per pair, `z1=cos`, `z2=sin`, channel-major/time-major fill order, `u1=0` rejection, `sqrt(0.05)` scaling |
| 2 | AR(3) initialization | §2 of amendment | Zero initial conditions, 100-cycle burn-in from `t=0`, absolute pre-burn-in sinusoid time index, 8880 innovation values per draw |
| 3 | Subdraw registry | §3 of amendment | Complete table: L1 families = subdraw 0 only; L3.frozen/oracle = subdraw 0 (innovations); L3.permuted/shuffled OBSERVED = subdraw 0 (innovations) + subdraw 1 (perturbation); NULL = subdraw 0 (perturbation only, reuses observed sequence); L5.permuted = subdraw 0 + subdraw 1 (two derangements) |
| 4 | RNG artifact schema gaps | §4 of amendment | `accepted_permutation: null` explicitly authorized for Gaussian-innovation-only subdraws; rejection_count scoped per subdraw type |
| 5 | Validation-index naming | §5 of amendment | Frozen: `fitting_origin_indices`, `buffer_cycle_indices`, `evaluation_origin_indices`, `fit_target_indices_by_horizon`, `evaluation_target_indices_by_horizon`; "train"/"validation" terms eliminated from L3 artifacts |
| 6 | Cross-platform numerical contract | §6 of amendment | binary64; Box–Muller exact; trigonometric tolerance 1e-12; OLS via `numpy.linalg.lstsq rcond=None`, tolerance 1e-10 weights / 1e-8 predictions; SHA-256 and integer arithmetic bit-exact; verdict comparisons: exact for deterministic, 1e-8 for stochastic statistics |
| 7 | L3 lineage conflict | §7 of amendment | Binding ruling: L3 Repair Proposal (`src/m3_L3_REPAIR_PROPOSAL.md`) as implemented at `45736cb` governs V4.4. Channel-phased sinusoid (`phase_c = c·π/16`) and two-slot delay state (`A_i=[[0,0],[1,0]]`) supersede V4.1 text. Candidate-facing bars unchanged. |

## No-change audit

- No candidate-facing bar changed.
- No change that benefits the candidate (four-part test condition (b) stands).
- The three L1 V4.4 amendments are NOT reopened.
- No seed pool, hold-out rule, verdict rule, authorization boundary, or INSTRUMENT_FAILURE handling changed.
- No implementation, code execution, scoring, or seed exposure occurred.
- O-14, O-15, D1–D5, L9, L18 binding.
- Seeds 201–203 retained, never rerun.
- No B2 work addressed.

## Deliverable map

- Implementation contract: `specs/m3_v4_4_implementation_contract_amendment.md`
- Changelog: `specs/m3_v4_4_implementation_contract_changelog.md` (this file)
- Branch: `architect/m3-v4-4-implementation-completeness`
