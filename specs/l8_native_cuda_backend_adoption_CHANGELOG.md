# L8 Native-CUDA Backend Adoption — Changelog

**Date:** 2026-08-21

**Regime:** B

## v1

- Converted committed prototype evidence into an inoperative, Rebecca-gated design; made no adoption or formal consistency ruling.
- Froze native Philox seed identity, exact draw schedule, single-stream scheduling invariance, dependency/device identity, and no-fallback behavior.
- Retained ordinal 47's region disagreement as `UNRESOLVED_BOUNDARY_CELL`; current evidence is explicitly non-qualifying and cannot be retroactively passed.
- Added prospective conclusion-preservation, narrow boundary-consistency, and one-sided regression criteria. Improvements over CPU are permitted; regressions are bounded independently.
- Added repeatability, failure, canonical publication/recovery, performance, CuPy/NVRTC exclusion, implementation/review, and rollback contracts.
- Added a backend-neutral M4 boundary while keeping native CUDA unavailable to M4 until adoption and Phase B reconciliation.
- Preserved the CPU oracle, approved tape-backed CUDA v1.5 contract, O-14/O-15, L18, negative labels, seed fences, and Rebecca's sole authority.
