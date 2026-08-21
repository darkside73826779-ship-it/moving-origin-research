# REBECCA APPROVAL AND FORMAL HANDOFF — M4 PHASE A AND CANDIDATE-MODEL BINDING

**Date:** 2026-08-21

**Regime:** B

## Rebecca decision

Rebecca R. McClintic approves the exact persistent-CRITIC-cleared M4 Phase A CUDA-ready / authoritative parallel-CPU-L8 (`gofast`) harness contract.

Approved package:

- ARCHITECT routing head: `architect/m4-cuda-ready-cpu-l8@e5edb1e804cc4a6553507c98140fa9fa49586a0d`.
- Design result: `e7419633f34c7eebadfe3cea33c84aff3883a4aa`.
- Persistent CRITIC review: `critic/m4-cuda-ready-cpu-l8-phase-a-bf7-executable-rereview@0790b4a24a868df84739199f1eab7bb16ebe0609`.
- Review artifact: `reviews/critic_m4_cuda_ready_cpu_l8_phase_a_bf7_executable_rereview.md`.
- Verdict: `LAW_FIDELITY CLEAR` and `SUBSTANTIVE CLEAR`; BF1–BF7 closed.

This approval adopts the Phase A architecture and contracts. It does not itself release implementation, training, execution, scoring, seed access, or merge.

## Delegated ARCHITECT decision scope

Rebecca assigns ARCHITECT—not Rebecca—to determine and specify the technically best candidate-model path for M4. ARCHITECT shall make the engineering/scientific design recommendation rather than asking Rebecca to guess among model brands or architectures.

ARCHITECT may select among a controlled custom model, matched fine-tuning from an open-weight pretrained checkpoint, or another technically justified locally reproducible architecture, provided the exact proposal:

1. satisfies the existing M4 candidate-versus-matched-peer requirements;
2. fixes the model family, exact checkpoint/weights/tokenizer identities and digests, license, precision/quantization, CUDA/runtime/dependency environment, resource envelope, and local executability;
3. defines two matched independently trained/fine-tuned instances with identical architecture, parameter count, initialization conditions, training data, optimization budget, calibration, and evaluation data, differing only in the authorized privileged-state access boundary;
4. specifies the moving-origin internal representation, self-model interface, confidence output, homeostatic variable, perturbation injection points, peer-observer channel exclusions, and contamination controls;
5. defines deterministic training/fine-tuning, checkpoint custody, randomness/domain separation, failure states, reproducibility, fixtures, acceptance tests, expected artifacts, and rollback;
6. preserves candidate blindness, O-14/O-15, L18, seed/courier fences, negative labels, locked bars, and Rebecca-only gate/merge authority;
7. keeps CUDA limited to model/harness computation and `gofast` as the sole authoritative L8 evaluator; `go faster` remains shelved and `GO!` unauthorized; and
8. includes the exact-SHA reconciliation inputs required to materialize the currently `PROVISIONAL_BLOCKED` M4 binding, or identifies any missing final `gofast` identity as an explicit STOP rather than inventing it.

ARCHITECT has authority to make the technical model-selection recommendation within these constraints. Any change to scientific bars, laws, negative labels, scoring authority, protected-seed policy, or backend authority remains outside this delegation and is a STOP to Rebecca.

## Required deliverables and route

ARCHITECT produces one committed candidate-model/training/binding specification, changelog, machine-readable manifests/schemas/fixtures as needed, exact implementation task boundary, and one formal handoff.

Required route:

`ARCHITECT → persistent fresh-context CRITIC → WORKFLOW COORDINATOR → Rebecca`.

Only after persistent CRITIC CLEAR and Rebecca's exact release may TASK BUILDER implement or train the candidate/peer models or build the production harness.

## Explicitly prohibited actions

No model download, training/fine-tuning, harness implementation, compatibility/diagnostic/scoring execution, protected/courier seed access or exposure, rerun, native-CUDA L8 adoption, fallback, state/provenance mutation, merge, or gate decision is authorized by this handoff.

## Next expected event

ARCHITECT acknowledges ownership, verifies the exact committed inputs, and begins candidate-model and exact-binding specification work in an isolated branch.
