# Rebecca M4 Model-Selection Qualification-Ladder Directive

Date: 2026-08-21
Regime: B
Authority class: Principal directive and M4 model-selection ruling

## Decision

M4 model selection is a pre-registered qualification ladder, not a single unconditional model choice. This ruling supersedes any prior assumption of training-based integration. It must be incorporated into the binding M4 specification and provenance now so the logging and serving contracts are built against it rather than retrofitted.

## 1. Pre-registered selection ladder

### Candidate primary

Qwen3-4B Instruct, FP8.

Rationale: Apache 2.0; family continuity with vetted tooling and hash discipline; approximately 4–5 GB footprint enabling co-residency; throughput advantage across all batteries; and an L8-specific need for natural accuracy in an informative middle band rather than at ceiling, leaving selective risk room to express dose-response.

### Candidate fallback

Qwen3-8B Instruct, FP8. It is invoked only upon qualification failure of the 4B under §2. No model beyond the 8B is in scope without a new Principal ruling.

### Peer observer

Llama 3.2 3B Instruct, FP8. The peer is deliberately cross-family under the program's correlated-error findings: its errors must not share family with the candidate whose correctness it predicts.

Peer fallback: Llama 3.1 8B if the 3B fails its lighter qualification of format compliance or non-degenerate correctness predictions on development transcripts.

## 2. Qualification gate

Qualification uses development seeds 101–105 and is diagnostic-only under O-15. The ladder selector is evidence, not preference. Checks occur in this order:

1. **Q1 — Format compliance.** The candidate reliably emits the harness answer structure under prompting/few-shot scaffolding alone.
2. **Q2 — Informative band.** Natural accuracy lands in a pre-registered informative band: the region where the confidence distribution has substantive mass around abstention threshold tau and realized selective risk is bounded away from both zero and chance. ARCHITECT proposes the numeric band; Rebecca must sign it before diagnostic execution.
3. **Q3 — Mirror calibratability.** A calibration head fitted on frozen outputs reaches L7-bar-plausible ECE on development data.

Escalation rules:

- Q2 ceiling failure: battery-difficulty adjustment using pre-registered task-generation parameters is the first lever; the 8B rung is second.
- Q1 failure: move directly to the 8B rung; there is no fine-tuning detour.
- The qualification report must state which rung was selected and why. It is the record intended for external review.

## 3. Serving architecture

### Primary

Co-resident candidate and peer on the single RTX 5080, with parallel phases restored. The 4B + 3B FP8 pair is expected to fit with KV-cache headroom, subject to the required preflight.

### Fallback

If the 8B rung is selected or memory pressure prevents co-residency, use phased sequential serving:

- Phase A: candidate battery with full-observable logging.
- Phase B: peer predictions replayed over Phase A transcripts.
- Phase C: scoring.

The Phase A logging contract must pre-register every observable over which the peer prediction task is defined: prompts, outputs, logits/confidences, self-state vector, timing, and oracle correctness. The phased design is also evidence of candidate/peer isolation.

Run sequencing is fixed in advance. Scoring follows each run. Nothing is adaptive between runs, and no result from run N may inform configuration of run N+1.

## 4. Standing rules

- **Pin and hash.** Record exact checkpoint revisions. Verify SHA-256 for all weights, including base weights and any adapters, at every session start. This is the permanent rule arising from the model-substitution incident; there are no exceptions.
- **Deterministic decoding.** Use temperature zero or fixed-seed sampling, pre-registered and uniform across arms.
- **Quantization floor.** FP8, not Q4, for any model whose logits feed the mirror. Calibration integrity outranks memory savings because aggressive quantization perturbs the logit distributions used by L7/L8 machinery.
- **Backbones frozen.** No gradient updates to any backbone; prompting only. A deviation such as format-competence QLoRA requires Rebecca's explicit sign-off, a documented dataset disjoint from scoring content, an adapter frozen and hashed before scoring, and persistent-CRITIC review of the contamination argument. This path is closed by default and opens only through a gate.

## 5. Immediate executor actions

These actions may proceed as a separate, non-scoring preflight while scaffold specification work continues:

- Pull the Qwen3-4B, Qwen3-8B, and Llama 3.2 3B checkpoints; record exact revisions and SHA-256 weight hashes for provenance.
- Extend environment preflight to the serving stack: verify FP8 support, test co-residency memory at target context lengths, and document one dry run of the fallback swap procedure.

Checkpoint acquisition and preflight do not select a rung, authorize candidate diagnostics, expose protected seeds, authorize scoring, or permit backbone updates.

## Required routing

- **ARCHITECT:** after completing and formally returning its currently active CF1–CF3 remediation, incorporate this ladder, qualification gate, serving/logging contracts, standing rules, exact executor contract, and Rebecca-gated Q2 numeric-band proposal into the binding prospective M4 specification. Route the committed amendment through WORKFLOW COORDINATOR to the established persistent CRITIC. Do not interrupt or blend the current CF1–CF3 work item.
- **RECORDER:** append a provenance entry identifying this directive as the M4 model-selection ruling and noting that it supersedes any prior assumption of training-based integration.
- **TASK BUILDER/executor:** perform only the checkpoint-custody and serving-stack preflight actions in §5 under an exact isolated non-scoring handoff; report ambiguities rather than inventing repository IDs, revisions, formats, target context lengths, or procedures.

## Holds

Scoring remains gated behind all standing M4 gates. This directive does not authorize scoring, protected-seed access, adaptive between-run changes, backbone training, QLoRA, selection beyond the named ladder, native-CUDA L8 adoption, scientific threshold changes, state mutation, or merge. O-14, O-15, P1–P6, L9, L18, candidate/peer independence, negative preservation, public-repository safety, exact-SHA provenance, and Rebecca's sole gate/merge authority remain binding.
