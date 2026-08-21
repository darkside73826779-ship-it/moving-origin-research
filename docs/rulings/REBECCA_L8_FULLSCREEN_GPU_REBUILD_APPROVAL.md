# REBECCA — L8 Full-Screen GPU Rebuild Approval (Operative Ruling)

**Status:** **OPERATIVE** — Rebecca-approved, 2026-08-20.
**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Principal:** Rebecca R. McClintic (sole gate and merge authority)
**Recorded by:** WORKFLOW COORDINATOR at Rebecca's explicit direction (2026-08-20 20:40 EDT). No agent speaks for Rebecca; this records Rebecca's in-session approval.

## Factual finding

Rebecca/TASK BUILDER runtime finding: the L8 G2–G4 full-screen run (19.2M arm-simulations, 20 geometries × 240 cells × 2,000 sims × 2 arms) is expected to require approximately **9 hours** on the CPU path (16 workers, `multiprocessing.Pool`), not the 1.5–2 h linear estimate in the amended spec §2. This corrects the timing estimate and motivates the GPU rebuild.

## Approval

Rebecca **APPROVES** a TASK BUILDER rebuild of the implementation to utilize **GPU processing** on Rebecca's workstation, to reduce runtime. This is a **performance optimization only** — NOT a scientific change. The TASK BUILDER is creating the GPU-equivalent code now (under Rebecca's approval).

## Route (Rebecca-approved)

TASK BUILDER creates the GPU-equivalent code → **ARCHITECT equivalence/design approval** (not co-authoring code) → **fresh-context CRITIC** review → Rebecca.

- **ARCHITECT approval scope:** an equivalence/design approval, NOT co-authoring code. If the ARCHITECT finds non-equivalence or missing spec authority → return to TASK BUILDER or STOP to Rebecca. If the ARCHITECT believes the spec itself must change → route an ARCHITECT amendment → CRITIC before implementation proceeds.
- **Full-run release:** the GPU rebuild + equivalence validation are authorized now. The full 19.2M GPU diagnostic execution requires ARCHITECT approval AND CRITIC clearance AND Rebecca's explicit release — this approval does NOT auto-release the full run post-clear.

## Equivalence constraints (binding — the GPU implementation must preserve)

- Same **PRIMARY = `complete_verdict_false_kill_rate`** = `P(any seed: β*_s < 0.2 OR ρ_s undefined OR ρ_s < 0.8)`; same diagnostics (β*-only any-seed, 5-seed-mean); same null-control false-pass.
- Same §7.1 output schema (fields, order, types, NaN→null, atomic write); same output paths (`diagnostics/l8_g2g4_minimal_full_screen.json` + `_HANDOFF.md`).
- Same **locked bars** (β* ≥ 0.2, ρ ≥ 0.8, ≥ 3 doses, 5 seeds) — unchanged; no lowering/raising/renaming/reinterpreting/silently replacing.
- Same 7 deterministic tests + 2a no-softening subtest (§5.5) — must pass identically on GPU.
- Same **seed derivation** (candidate-blind, Ruling 9 — seeds from parameter-combo hashes; no candidate output is an input). **The GPU path must reproduce the CPU path's per-seed `β*` and `ρ` values for identical seeds** — bit-for-bit, or provably-equivalent within the locked-bar comparison tolerance (`RHO_COMPARE_EPS = 1e-12`); if it cannot, STOP and escalate to Rebecca — do not silently diverge.
- No-relabeling (per-seed statistical failures are predicate failures, NOT `INSTRUMENT_FAILURE`; §5.6 apparatus-validity decision tree).
- **No bootstrap/Wilson/quorum/fallback** (only the Rebecca-authorized direct per-seed Spearman ρ).
- O-15 diagnostic-only; no scoring, no protected-seed exposure, no G2–G4 freeze, no L15/L16/L17 before M5. (The "no merge to main" constraint applies to the GPU implementation/results — Rebecca separately authorized merging THIS approval ruling to main.)
- Boundary-escalation (`W ∈ {50,400}` or `N_w ∈ {4,64}` → STOP, escalate).

## CPU↔GPU equivalence verification (required before any full GPU screen)

Before any full GPU screen, the TASK BUILDER must produce an equivalence packet:
- The 7 deterministic-test categories + 2a no-softening test pass on GPU.
- CPU vs GPU comparison on a small fixed sentinel subset covering: combo + null arms; tie cases; boundary ρ; zero-variance ρ; non-finite / apparatus-validity paths; and a few ordinary cells.
- A repeat GPU run on the same sentinel subset to verify determinism/reproducibility.
- Same seed derivation and RNG semantics; if the GPU uses a different RNG/order and cannot reproduce the CPU β*/ρ within the allowed comparison tolerance (`RHO_COMPARE_EPS = 1e-12`), STOP and return to ARCHITECT/Rebecca.
- Output schema/canonicalization unchanged except runtime metadata.

## Public-repo safety (binding)

Any GPU documentation is non-identifying only. Forbid hostnames, usernames, private paths, MAC addresses, device IDs, and environment dumps. Non-identifying GPU model/driver/library versions are acceptable only if needed for reproducibility.

## Authoritative spec (unchanged)

The amended spec `architect/l8-g2g4-minimal-fullscreen` @ `2082680` remains the authoritative specification. The GPU implementation is a performance-equivalent reimplementation subject to ARCHITECT equivalence approval + CRITIC review. The 9h CPU finding does not alter the spec's science (predicate, bars, schema); it corrects the timing estimate and motivates the GPU performance rebuild.

## Signature

**Rebecca R. McClintic** (Principal; sole gate and merge authority) — **APPROVED 2026-08-20.**

*This ruling is operative upon Rebecca's approval. It authorizes the GPU rebuild and its route (TASK BUILDER → ARCHITECT → CRITIC). It does NOT authorize scoring, protected-seed exposure, or merge of results to main.*
