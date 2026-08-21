# REBECCA SCOPE CORRECTION — M4 MODEL SELECTION SEQUENCING

**Date:** 2026-08-21

**Regime:** B

## Correction

Rebecca R. McClintic corrects the scope of `handoffs/REBECCA_M4_PHASE_A_APPROVAL_AND_MODEL_BINDING_ARCHITECT_HANDOFF_2026-08-21.md`.

M4 Phase A approval remains valid. ARCHITECT remains responsible for determining the technically sound path forward, but ARCHITECT shall **not select, pin, download, or bind a specific real candidate model or checkpoint yet**. A concrete model choice before the model-agnostic harness scaffold exists would be premature.

Where the prior handoff asked ARCHITECT to fix a model family, exact checkpoint, weights, tokenizer, and related concrete identities now, that requirement is deferred to a later separately authorized model-selection/binding gate.

## Current ARCHITECT scope

ARCHITECT shall specify:

1. a model-agnostic candidate/peer adapter contract with exact inputs, outputs, schemas, lifecycle, and failure states;
2. the privileged-state boundary separating the candidate from the matched peer;
3. confidence, moving-origin internal representation, self-model, homeostatic-variable, perturbation-hook, and CUDA resource-reporting interfaces without choosing a model brand;
4. synthetic/stub candidate, peer, oracle, empty, permuted, shuffled, naive, and frozen adapters sufficient to build and validate harness control flow before a real model is introduced;
5. model-independent CUDA/host synchronization, artifact custody, reproducibility, determinism, checkpoint metadata, and `gofast` boundary requirements;
6. an executable harness-scaffold verification contract and exact negative fixtures;
7. a later candidate-model qualification and selection procedure, including required capabilities, resource limits, licensing, reproducibility, matched-training feasibility, internal-state/perturbation access, evaluation criteria, and STOP conditions; and
8. the exact sequencing and authority boundary for the later model-selection, download, binding, training/fine-tuning, and integration gates.

The selection procedure must allow ARCHITECT to recommend the best compatible model later without requiring Rebecca to guess among model brands. It must not name or privilege a specific model based on unexecuted assumptions unless a brand-neutral interface requirement logically forces that conclusion and the issue is returned to Rebecca.

## Required build sequence

1. ARCHITECT model-agnostic adapter/scaffold specification.
2. Persistent fresh-context CRITIC review.
3. Rebecca approval and exact TASK BUILDER release for model-agnostic scaffold implementation only.
4. TASK BUILDER implements and validates the scaffold with committed synthetic/stub adapters.
5. Persistent CRITIC implementation review and Rebecca acceptance.
6. Later ARCHITECT candidate-model qualification/selection against the accepted scaffold.
7. Persistent CRITIC review and Rebecca approval before any model download, binding, training/fine-tuning, or real-model integration.

## Preserved architecture and holds

CUDA remains the model/harness compute environment. Canonical parallel-CPU L8 (`gofast`) remains the sole authoritative L8 evaluator. Native-CUDA L8 (`go faster`) remains shelved and serial CPU (`GO!`) remains unauthorized for M4.

No model selection, model download, weights/tokenizer binding, training/fine-tuning, real-model integration, harness implementation, compatibility/diagnostic/scoring execution, seed access/exposure, rerun, native-CUDA L8 adoption, state/provenance mutation, merge, or gate decision is authorized by this correction.

## Required route

`ARCHITECT → persistent fresh-context CRITIC → WORKFLOW COORDINATOR → Rebecca`.

No surrogate-role review may substitute for the persistent CRITIC.
