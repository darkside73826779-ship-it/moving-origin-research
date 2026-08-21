# REBECCA DIRECTIVE — CUDA-READY M4 HARNESS WITH AUTHORITATIVE PARALLEL-CPU L8

**Date:** 2026-08-21

**Regime:** B

## Authority and decision

Rebecca R. McClintic directs that the native-CUDA L8 simulator adoption path be shelved as a possible future path. The approved parallel-CPU L8 simulator remains the sole authoritative L8 simulation/evaluation backend for the current M4 program.

The M4 harness must nevertheless be designed to function well in a CUDA environment because its intended future use includes harnessing AI models. This means CUDA-capable model execution and harness orchestration must coexist with an explicit, fail-closed parallel-CPU L8 evaluation boundary. It does not authorize the shelved native-CUDA L8 simulator, a silent CUDA L8 substitute, or a silent CPU/CUDA fallback.

## Gate served

Prospective M4 Phase A architectural redirection and BF1–BF5 remediation before any harness implementation.

## Authoritative inputs

- M4 Phase A design: `architect/m4-harness-contract@60e515c4b14160d282c5ba0b7b6b8c2a8f63dd54`.
- M4 Phase A design result: `76fb37ee359abf2539131c854befe0f695178036`.
- CRITIC combined BLOCK: `critic/m4-harness-cuda-l8-phase-a-review@4a581cb5e793579e5c98478e36cc9d5e8210ff43`.
- Review artifact: `reviews/critic_m4_harness_cuda_l8_phase_a_review.md`.
- Previously approved L8 v1.5 lineage remains evidence for applicable evaluator semantics, but no native-CUDA L8 adoption result becomes operative.

## Authorized ARCHITECT scope

ARCHITECT shall produce a narrow revised M4 contract that:

1. designates the approved parallel-CPU L8 implementation as the sole current authoritative L8 backend;
2. removes native-CUDA L8 adoption and native-CUDA L8 exact-SHA reconciliation as prerequisites for current M4 implementation;
3. preserves a versioned backend boundary so a future separately approved L8 backend can be added without changing scientific bars, labels, custody, or scoring semantics;
4. specifies CUDA-capable AI-model execution and harness orchestration, including the exact device boundary, tensor/data transfer, synchronization, serialization, determinism, resource/failure, and custody contracts needed to call the parallel-CPU L8 evaluator safely;
5. fails closed on any attempt to use an unapproved L8 backend, including the shelved native-CUDA simulator;
6. replaces former Phase B native-CUDA reconciliation with exact-SHA compatibility reconciliation against the final approved parallel-CPU L8 implementation used by M4;
7. minimally remediates CRITIC BF1–BF5 under the revised CPU-L8/CUDA-ready architecture: correct provenance tags, commit the runtime configuration template, realize all executable fixtures, define exact compatibility-report/failure outputs and digests, and represent valid zero-variance statistical failures consistently; and
8. preserves O-14/O-15, L18, all locked M4 bars and controls, negative labels, five downstream scoring gates, seed protection, public-repository safety, fresh-context review, and Rebecca's sole gate/merge authority.

ARCHITECT must explicitly distinguish CUDA use for AI-model/harness computation from L8 simulator authority. Any material scientific or equivalence choice not already fixed is a STOP to Rebecca.

## Status of native-CUDA L8 work item

The native-CUDA L8 adoption item is `SHELVED/INOPERATIVE`. Its implementation and diagnostic evidence remain preserved historical feasibility evidence. No further remediation, implementation, qualifying execution, adoption routing, M4 dependency, or merge is authorized unless Rebecca explicitly reopens that work item.

## Required route

`ARCHITECT → fresh-context CRITIC → WORKFLOW COORDINATOR → Rebecca`.

TASK BUILDER remains held until the revised contract receives CRITIC CLEAR and Rebecca's exact implementation release. Exact-SHA reconciliation against the final approved parallel-CPU L8 implementation remains mandatory before M4 implementation release.

## Explicitly prohibited actions

No harness implementation, native-CUDA L8 remediation/adoption, diagnostic execution, scoring, protected/hold-out/courier seed access or exposure, rerun, negative renaming, bar/control change, G2–G4 freeze, L15/L16/L17 work, durable-state/provenance mutation, public-status flip, merge, or gate decision is authorized by this directive.

## Next expected event

ARCHITECT acknowledges ownership of the revised M4 Phase A design task, commits and pushes one narrow revised package, and formally hands it through the WORKFLOW COORDINATOR to a fresh-context CRITIC.
