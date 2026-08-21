# Rebecca M4 Exact-Matched-Peer Amendment

Date: 2026-08-21
Regime: B
Authority class: Principal amendment to the M4 model-selection qualification-ladder directive
Amends: `handoffs/REBECCA_M4_MODEL_SELECTION_QUALIFICATION_LADDER_DIRECTIVE_2026-08-21.md`

## Decision

M4 uses an exact matched peer: a separate loaded instance of the same checkpoint as the selected candidate rung. This amendment supersedes the prior binding cross-family Llama peer ladder.

## Candidate-primary peer

The peer for candidate primary is a separate loaded instance of the exact same `Qwen/Qwen3-4B-Instruct-2507-FP8` checkpoint revision used by candidate primary, with identical weight-file hashes.

## Candidate-fallback peer

The peer for candidate fallback is a separate loaded instance of the exact same `Qwen/Qwen3-8B-FP8` checkpoint revision used by candidate fallback, with identical weight-file hashes.

## Required equality

Candidate and peer must have no difference in:

- checkpoint revision or weight-file content;
- tokenizer;
- architecture or parameterization;
- quantization;
- decoding configuration;
- calibration procedure;
- evaluation procedure; or
- binning procedure.

The peer differs only through its locked observable-only input channel and the exclusion of self-report and internal-state access. It is a separate runtime instance, not an independently trained or altered checkpoint.

The prospective binding specification must define exact identity checks and fail-closed evidence proving candidate/peer checkpoint revision and every weight-file SHA-256 are identical at session start.

## Superseded peer ladder

Llama 3.2 3B Instruct and Llama 3.1 8B are removed from the binding L7 peer ladder. They are not gating peers. They may not be restored, including as diagnostics, without a separate Rebecca ruling that explicitly defines their non-gating scope and safeguards.

## Rationale

This amendment resolves the conflict between the earlier cross-family peer instruction and constitutional L7's matched-model requirement together with the M0/Entry 76 equality contract for parameters, data, and architecture. It also aligns peer custody with the frozen-backbone and no-training ruling: there is no independently trained peer checkpoint.

## Consequential specification requirements

ARCHITECT must reconcile the model-selection ladder, serving architecture, memory/co-residency preflight, phased fallback, checkpoint custody, logging, qualification, and executor contracts against exact candidate/peer identity. Any resource estimate or co-residency procedure premised on a Qwen-plus-Llama pair is superseded and must be recomputed for two separate instances of the applicable Qwen rung.

The observable-only peer channel, self-report/internal-state exclusion, candidate/peer isolation evidence, deterministic decoding, FP8 floor, exact revision/hash verification, frozen backbones, fixed run sequencing, and local-only multi-gigabyte model custody remain binding.

## Holds

This amendment authorizes specification reconciliation only. It does not authorize model download, serving preflight, qualification, diagnostics, scoring, protected-seed access, training, adapters, implementation, merge, or gate decision. The scaffold implementation re-release is a separate Rebecca decision and is not granted here.
