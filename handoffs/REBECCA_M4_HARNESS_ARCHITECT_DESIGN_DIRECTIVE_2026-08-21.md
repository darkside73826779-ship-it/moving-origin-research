# Rebecca Directive — M4 Harness Architecture with CUDA L8 Compatibility

**Date:** 2026-08-21  
**Regime:** B  
**Authority:** Rebecca R. McClintic  
**Status:** ARCHITECT design authorization only

## Direction

While TASK BUILDER separately works with Rebecca on the approved L8 GPU/CUDA v1.5 implementation, ARCHITECT is authorized to begin a separate M4 harness-design work item so the workflow can continue.

ARCHITECT must design the M4 harness to work correctly with the approved CUDA L8 contract. This is specification and readiness work only; ARCHITECT does not implement the harness.

## Authoritative inputs

- M4 specification: `specs/m4_specification.md` on `main`
- M4 task specification: `specs/m4_task_spec.md` on `main`
- Approved L8 GPU/CUDA design: `architect/l8-gpu-adoption-spec` routing head `e05550f494b2c6dffb2ea9645067395beaf56fe1`, design result `a25398e599622c09d130b597b7bc83ce62a966d5`
- Independent L8 CLEAR: `critic/l8-gpu-v1.5-bf1-bf5-rereview` @ `e0aad1dabde9546e0074a7a375135eb92ee2072a`
- Rebecca L8 approval/release: `coordinator/l8-gpu-v1.5-rebecca-approval-intake` @ `50260d3`

## Required CUDA-L8 compatibility design

ARCHITECT must specify, without implementer invention:

1. The exact interface between the M4 harness's real estimator and the approved CUDA L8 producer/evaluator/result contracts.
2. Exact schemas, field names/types/order, identities, canonicalization, digests, configuration provenance, and failure routing at the interface.
3. How the harness consumes or reproduces the approved L8 β*, rho, predicate, calibration, geometry/cell/arm, and result-order semantics without changing any locked bar or negative label.
4. A diagnostic-only O-15 compatibility check that feeds the approved L8 synthetic profiles and identities through the harness's real estimator and verifies agreement with the approved L8 contract before any scoring authorization.
5. CPU↔GPU/CUDA boundary behavior, including which steps remain CPU responsibilities, which are CUDA evaluator responsibilities, and the prohibition on silent CPU fallback or native GPU calibration where the L8 contract forbids them.
6. Exact fail-closed behavior for missing/mismatched executable inputs, dependency or configuration mismatch, digest mismatch, nondeterminism, schema drift, CUDA unavailability, and any divergence from the approved L8 result semantics.
7. The implementation order, tests, fixtures, expected values/digests, custody artifacts, review points, and rollback plan needed for TASK BUILDER to implement later without guessing.

ARCHITECT must use the committed approved L8 v1.5 contract as authority. It must not depend on uncommitted or unstable implementation details from TASK BUILDER's active workspace. If the approved contracts do not supply a required interface input, ARCHITECT must STOP and escalate the exact gap; it may not invent or silently change L8.

## Two-phase compatibility rule while L8 implementation is active

The L8 CUDA implementation is still under active TASK BUILDER development and may change before its implementation commit and independent review are final. Therefore:

1. **Phase A — contract-first design now:** ARCHITECT designs against the approved, committed L8 v1.5 contract and defines a versioned adapter/interface boundary. It must separate stable contract requirements from implementation-specific bindings and label every latter binding provisional.
2. **No moving-code dependency:** ARCHITECT must not cite TASK BUILDER working-tree code, transient filenames, uncommitted APIs, or observed local behavior as authoritative. Consultation may identify risks, but only committed artifacts may enter the design authority chain.
3. **Phase B — mandatory final reconciliation:** after TASK BUILDER commits the final L8 implementation and CRITIC completes its implementation review, ARCHITECT must perform a narrow exact-SHA compatibility reconciliation between the M4 harness design and the final cleared L8 implementation. Any changed interface, schema, digest, dependency, failure contract, or execution boundary returns through CRITIC and Rebecca before M4 implementation release.
4. **Release gate:** M4 harness implementation is not released until Phase B records the final L8 implementation SHA, verifies every adapter binding, closes all compatibility deltas, and receives fresh-context CRITIC CLEAR plus Rebecca approval.
5. **Fail-closed versioning:** the future harness must reject an L8 implementation/configuration identity other than the exact approved compatible version; no permissive fallback, duck typing, or silent field translation is allowed.

## Concurrency and isolation

- L8 implementation remains owned by TASK BUILDER under its separate formal handoff.
- M4 harness design is owned by ARCHITECT as a separate work item.
- Workspaces, branches, artifacts, and ownership remain isolated.
- Consultation is permitted, but does not transfer either ball and may not cause cross-role editing or co-authorship.

## Holds

- No harness implementation is authorized by this directive.
- No scoring, protected/hold-out/courier seed access or exposure, rerun, L8 execution change, G2–G4 freeze, merge, or gate decision is authorized.
- The five downstream M4 scoring gates remain binding.
- O-14, O-15, P1–P6, L9, L18, negative preservation, exact-SHA provenance, public-safety scanning, fresh-context CRITIC review, and Rebecca's sole gate/merge authority remain unchanged.

## Route

ARCHITECT → fresh-context CRITIC → Rebecca. TASK BUILDER may implement the M4 harness only after this exact design is CRITIC-cleared and Rebecca explicitly releases implementation.
