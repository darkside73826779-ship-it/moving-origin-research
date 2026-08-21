# Rebecca M4 Model-Agnostic Scaffold Implementation Release

Date: 2026-08-21
Regime: B
Gate served: M4 model-agnostic candidate/peer adapter and synthetic-scaffold implementation release

## Authority and decision

Rebecca R. McClintic expressly approved release of the persistent-CRITIC-cleared M4 model-agnostic scaffold-with-stubs specification to TASK BUILDER for implementation.

This record is routing authority only. It does not amend the specification or authorize a gate ruling beyond the exact implementation release below.

## Authoritative inputs

- Approved Phase A design head/result: `e5edb1e804cc4a6553507c98140fa9fa49586a0d` / `e7419633f34c7eebadfe3cea33c84aff3883a4aa`
- Phase A persistent-CRITIC CLEAR: `0790b4a24a868df84739199f1eab7bb16ebe0609`
- Model-agnostic scaffold ARCHITECT head: `2c655fbb1bac6ba419327198062c5230e87c44db`
- RF1A result: `b84f470af415ead5ae36ca01bb1d8e7394e7cc97`
- Final persistent-CRITIC CLEAR: `e76ecb98e80e5bded57afe3d318a32fcfbbfe463`
- Final review: `reviews/critic_m4_model_agnostic_scaffold_rf1a_rereview.md`
- Primary specification: `specs/m4_model_agnostic_scaffold_spec_v1.md`
- Executable fixtures: `specs/data/m4_model_scaffold_executable_fixture_v1.json` and `specs/data/m4_model_scaffold_rf1_rf3_fixture_v1.json`

## Released TASK BUILDER scope

Implement the exact cleared model-agnostic scaffold-with-stubs contract, including:

- model-neutral candidate/peer adapter framework;
- CUDA-ready candidate/peer and harness interfaces;
- the synchronized host boundary to authoritative parallel-CPU L8 (`gofast`);
- deterministic synthetic stub adapters and committed fixtures;
- specified validation, failure handling, custody, reproducibility, and peer-redaction behavior;
- only the implementation checks and synthetic tests prescribed by the cleared specification.

The TASK BUILDER must not invent missing behavior. Any specification ambiguity or missing executable input is a formal stop returned through WORKFLOW COORDINATOR to ARCHITECT.

## Holds and prohibitions

This release does not authorize:

- selecting, pinning, downloading, binding, training, or fine-tuning a real model;
- compatibility, diagnostic, candidate, or scoring execution beyond the specification's synthetic scaffold tests;
- protected-seed access or exposure;
- native-CUDA L8 (`go faster`) adoption or execution;
- use of serial-CPU L8 (`GO!`);
- scientific-specification changes, threshold changes, state/provenance mutation, gate decisions, or merge.

O-14, O-15, P1-P6, L9, L18, candidate/peer independence, negative preservation, public-repository safety, and Rebecca's sole gate/merge authority remain binding.

## Required route

TASK BUILDER implements and verifies the exact released scope on an isolated `taskbuilder/*` branch, commits and pushes the result, and returns one formal handoff to WORKFLOW COORDINATOR. Coordinator then routes the exact committed implementation to the established persistent CRITIC for independent implementation review. Any CRITIC BLOCK returns through Coordinator to TASK BUILDER unless the review identifies a specification defect, in which case it returns to ARCHITECT. A CRITIC CLEAR returns through Coordinator to Rebecca. No implementation merge is authorized by this release.
