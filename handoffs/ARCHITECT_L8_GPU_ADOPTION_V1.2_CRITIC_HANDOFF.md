# ARCHITECT → Fresh-Context CRITIC — L8 GPU Adoption v1.2

**Date:** 2026-08-20

**Regime:** B

- **Gate served:** remediation of CRITIC blockers B1–B8 for the L8 GPU diagnostic-backend equivalence gate.
- **Input SHAs reviewed:** prior spec `7c0a3c728cb69f6a7aea964810bcd423e320117f`; CRITIC review `6e408aece2836d07a5a21b716e1f7c3b7db5bc04`; required base `b6d4556021ad38199d3bfa90fdb3ef9a99988790`; controlling CPU spec `2082680a7caba85c46e637b3b38d679fa7f80599`; CPU implementation `b1397498ca369067e956479e6c2bd6b0793c3e89`; CPU evidence `6d455bb878f4b52a5b5564afac38d6fb3a20d4b3`; GPU evidence `1bf7654533483cb704a7b8e0898dbbf5439b1552`; Item-1 ruling source `69feed8d353662c60fe9025b0f3c91dc80b9d1e3`; geometry ruling `5306c3025a6018a4947c97b8f498f811ef7580ba`.
- **Files created/revised:** `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.2.md`; companion changelog; `specs/data/l8_gpu_adoption_known_good_v1.json` and sidecar; this handoff. The Item-1 ruling, controlling CPU-spec package, and geometry ruling were preserved from their committed source commits.
- **Branch/specification SHA:** `architect/l8-gpu-adoption-spec`; v1.2 specification commit `e247c6b8f527470cab65a61f1c8de094b28283eb`.
- **Verdict/status:** REMEDIATED SPECIFICATION PROPOSED; TASK BUILDER remains held.

## Blocker closure map

- **B1:** controlling rho comparison, undefined-rho disposition, no-softening test, and complete predicate restored in §§3 and 6.
- **B2:** CPU comparator is now explicitly `b139749` plus only the Rebecca-authorized direct-rho/complete-verdict extension.
- **B3:** controlling CPU seed formula restored; uniqueness applies to identity tuples, while reduced-seed collisions are counted rather than confused with duplicate identities.
- **B4:** backend equivalence uses the controlling comparator's combo/null controls plus frozen/naive/oracle roles; nonexistent L8 empty/permuted/shuffled fixtures are not invented, and future L8 scientific claims retain the full L18 obligation.
- **B5:** exact known-good pair, sentinel geometry/cells/workload, schemas/order/canonicalization, sidecar convention, publication recovery, and twelve rehearsals are fixed.
- **B6:** maximum-capacity NumPy producers emit primitive stochastic tapes; batched GPU work retains mirror, degradation, controller, estimator, and verdict computation. A factored CPU evaluator must first reproduce the unmodified baseline. No per-logical-seed CUDA generator or serial path remains.
- **B7:** Wilson/Newcombe and all unpaired interval machinery are removed. Same-input paired value/predicate equivalence controls.
- **B8:** branch was rebased onto `b6d4556`; the GPU ruling is present from base, and the committed Item-1 and geometry rulings are present in-tree.

## Required CRITIC review

1. Report `LAW_FIDELITY: PASS|BLOCK` first: law-diff, source tags, and provenance/source-SHA verification.
2. Only after Part A passes, report `SUBSTANTIVE: CLEAR|BLOCK` after attempting to falsify every B1–B8 closure, especially the primitive-tape equivalence boundary, baseline-to-factored-CPU identity check, maximum-capacity pipeline, exact schema, recovery procedure, and L18 scope.
3. Overall `CLEAR` requires both Part A PASS and Part B CLEAR.

- **Locked-content confirmation:** L8/L18/L19 quotations are unchanged; beta-star `0.2`, rho `0.8`, at least three doses, five seeds, specificity control, and `RHO_COMPARE_EPS=1e-12` semantics are preserved; `specs/data/l8_cpu_frozen_calibration_v1.json` is unchanged.
- **Retained findings:** native GPU calibration differs at four of fifteen pairs; exact maximum absolute difference `0.7499937499999998`, second magnitude `0.18749843749999995`, mean absolute difference `0.1624986458333333`; two misspecification profiles retain different exact selections.
- **Exact next recipient:** fresh-context CRITIC, then Rebecca. TASK BUILDER is not released before both clearances.
- **Explicitly prohibited:** implementation, execution, scoring, protected-seed access/exposure, full-screen release, G2–G4 freeze, post-run tolerances, native GPU calibration/RNG adoption, automatic retry/fallback, CPU replacement, merge to main, or L15/L16/L17 before M5.
- **Public-safety scan:** gitleaks scanned every rebased-branch commit and the handoff; credential/PII/private-path regex plus manual review covered all new or restored artifacts. Zero findings. No blocker, Rebecca-decision item, protected-seed exposure, or acceptable exception was found.
