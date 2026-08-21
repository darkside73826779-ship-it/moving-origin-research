# REBECCA — Authorization to Resolve L8 Full-Screen Item 1 STOP (Direct Per-Seed Spearman ρ)

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding)
**Authority:** Rebecca R. McClintic (Principal; sole gate and merge authority)
**Serves:** L8 G2–G4 minimal full-screen specification — Item 1 (primary metric) STOP resolution
**Recorded by:** ARCHITECT at Rebecca's direction ("record this as my authorization"). This artifact transcribes Rebecca's authorization verbatim; the ARCHITECT does not speak for Rebecca.

## Authorization

Rebecca R. McClintic authorized the ARCHITECT to amend the diagnostic specification to define the direct per-seed Spearman ρ calculation required by frozen L8 v2.2, resolving the ARCHITECT's STOP (handoffs/ARCHITECT_L8_FULLSCREEN_STOP_ITEM1_RHO.md, branch `architect/l8-g2g4-minimal-fullscreen` @ `dc3185a`). The ARCHITECT's STOP was confirmed correct: `b139749` does not compute per-seed Spearman ρ, so the complete frozen-v2.2 predicate was not computable from existing arrays. This ruling authorizes the addition of a direct (non-bootstrap, non-Wilson, non-quorum, non-fallback) per-seed Spearman ρ calculation to the specification.

## Rebecca's directive (verbatim, transcribed by ARCHITECT at her direction)

> ARCHITECT Handoff — Resolve L8 Full-Screen Item 1 STOP
>
> Your STOP was correct. You are now authorized to amend the diagnostic specification to define the direct per-seed Spearman ρ calculation required by frozen L8 v2.2.
>
> Specify:
> Inputs: four dose-level regulation-error summaries already used by the β* estimator.
> Dose ranks: (1, 2, 3, 4).
> Response ranks: ascending midranks; ties receive the arithmetic mean of occupied ranks.
> Statistic: Pearson correlation between dose ranks and response midranks.
> Locked predicate: ρ_s ≥ 0.8.
> Zero response-rank variance: ρ is undefined and counts as failure of the ρ predicate, not INSTRUMENT_FAILURE.
> Non-finite or structurally invalid inputs: disposition separately through explicit apparatus-validity rules.
> Any floating-point tolerance must be minimal, explicit, tested, and must not change the locked 0.8 bar.
>
> Define the primary true-effect false-kill rate as:
> P(any seed has β*_s < 0.2 OR undefined ρ_s OR ρ_s < 0.8)
>
> Define null-control false-pass as the fraction of simulations in which every seed satisfies both predicates.
>
> Retain the β*-only any-seed and five-seed-mean measures as diagnostics. Specify distinct schema fields for complete-verdict and diagnostic metrics.
>
> Require deterministic tests covering:
> Perfect increasing monotonicity
> Adjacent-inversion/threshold case
> Tied responses
> Constant responses
> Decreasing responses
> Non-finite inputs
> Complete-verdict aggregation across five seeds
>
> Then complete Item 3:
> Prospectively adopt only the 20-geometry list and ordering from 4463cbc.
> State that prohibited v2.4 machinery is not adopted.
> Make acceptance apply to an exact (W, N_w) geometry.
> Specify deterministic handling of equal-Q geometries.
> Define escalation if no geometry passes or the first acceptable result lies on a tested boundary.
> Prepare the geometry-list adoption for Rebecca's signature before execution.
> Return the amended specification through fresh-context CRITIC before TASK BUILDER release.
>
> This authorizes specification remediation and review only. It does not authorize implementation, bootstrap/Wilson procedures, quorum or fallback rules, scoring, protected-seed access, locked-bar changes, merger, or G2–G4 freeze.

## Authorization boundary

This authorizes specification remediation and review only. It does **not** authorize: implementation; bootstrap/Wilson procedures; quorum or fallback rules; scoring; protected-seed access; locked-bar changes (ρ ≥ 0.8, standardized slope ≥ 0.2, ≥3 doses, 5 seeds — all `[BAR-Entry 11]` — unchanged); merger to main; G2–G4 freeze; L15/L16/L17 before M5; reclassification of statistical failures as INSTRUMENT_FAILURE; rerun (O-14); or any scoring-mode execution (O-15 diagnostic-only).

The per-seed Spearman ρ calculation authorized here is a **direct, deterministic, non-resampling statistic** (Pearson correlation of dose ranks and response midranks). It is **not** a quorum, fallback, bootstrap, or Wilson procedure, and introduces none of those. It is the minimum computation required to compute the complete frozen-v2.2 scoring predicate; it does not alter the locked bars.

## P5 memorialization

This is a Principal-gated authorization recorded per §5 P5 (deviation memorialization). It registers Rebecca's authorization to add the direct per-seed Spearman ρ calculation (resolving the Item 1 STOP) and the Item 3 geometry-list prospective adoption; it does not alter any law's constraint text. Locked bars are unchanged. Rebecca R. McClintic remains the sole authority for the later workload, gate, and geometry-list-signature decisions.

## Next recipient

ARCHITECT (to amend the specification), then fresh-context CRITIC → Rebecca (geometry-list signature) → TASK BUILDER. TASK BUILDER remains held until BOTH fresh-context CRITIC clearance AND Rebecca's geometry-list signature.
