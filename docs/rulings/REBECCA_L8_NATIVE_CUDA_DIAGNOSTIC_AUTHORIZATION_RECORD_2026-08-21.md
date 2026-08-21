# Rebecca L8 native-CUDA diagnostic authorization record

**Date:** 2026-08-21  
**Regime:** B  
**Recorder:** TASK BUILDER, recording Rebecca R. McClintic's direct instructions for provenance; this artifact does not speak or rule for Rebecca.

## Recorded directions

Rebecca R. McClintic directly authorized and directed the following during the TASK BUILDER session:

1. Dependency installation: “install whatever you need for the best results”.
2. Native-CUDA objective: “ok lets just get the cuda version equivalent then”.
3. Development testing: “test it as needed to ensure its equivalent”.
4. Fast native prototype: “lets do the fastet route to getting a cuda sim going then we check its results against the cpu results i think a shorter 1000 run should go by in minutes and tell us what we need to know”.
5. Same-length comparison: “ok so lets see the 10,000 run now so we have an apples to apples parallel to gpu comparison”.
6. Review routing: “write it up for architect then critic approval ensure my authorization for the changes you made are or have been documented for refrencing then pass to architect through workflow”.
7. Safety-workflow direction: “safety scans are now for merges to public not for pre public pushes”. This direction is recorded for policy amendment/review. TASK BUILDER continued the currently binding pre-push scan procedure pending an operative amendment to `PUBLIC_REPOSITORY_POLICY.md`.

## Scope actually exercised

- Implemented a diagnostic-only native CUDA prototype using Torch CUDA Philox RNG.
- Installed custom-CUDA development dependencies only in an isolated environment outside the repository; the governed pinned v1.5 runtime was not changed by those prototype packages.
- Executed two 1,000-repetition native-CUDA prototype runs across all 240 legacy cells and both arms.
- Executed one 10,000-repetition native-CUDA comparison across all 240 legacy cells and both arms.
- Compared results with the committed CPU oracle at `6d455bb` without rerunning that CPU workload.

No scoring, protected-seed access, negative renaming, bar change, G2–G4 freeze, or merge was authorized or performed.
