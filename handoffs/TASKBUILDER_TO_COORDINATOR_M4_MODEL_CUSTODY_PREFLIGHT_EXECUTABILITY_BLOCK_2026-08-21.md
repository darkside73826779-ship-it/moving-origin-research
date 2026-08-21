# TASK BUILDER to WORKFLOW COORDINATOR — M4 Model-Custody Preflight Executability Block

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Separate non-scoring M4 model-checkpoint custody and serving-stack preflight

## Authority reviewed

- Repository authority: `coordinator/m4-model-selection-ladder-directive` at `0c191211d5e3ed8e0eedf59bb9955e01f35ab5e5`.
- Directive artifact: `handoffs/REBECCA_M4_MODEL_SELECTION_QUALIFICATION_LADDER_DIRECTIVE_2026-08-21.md`.
- Principal authority: Rebecca R. McClintic.

## Disposition

**EXECUTABILITY/SPECIFICATION BLOCK — no acquisition, installation, environment mutation, or preflight execution started.**

The directive names three model/quantization targets but expressly forbids the executor from inventing repository identities, revisions, FP8 sources, custody fields, target context lengths, measurement methods, or swap procedures. Those executable inputs are not committed in the reviewed authority.

## Missing executable inputs

1. Exact, case-sensitive model repository IDs are absent for Qwen3-4B Instruct FP8, Qwen3-8B Instruct FP8, and Llama 3.2 3B Instruct FP8.
2. The directive does not identify whether each required FP8 checkpoint is an official upstream artifact or an approved derived quantization, nor the authorized publisher/source for any derived FP8 artifact.
3. Exact immutable repository/checkpoint revisions are absent for all three checkpoints.
4. The checkpoint acquisition and custody contract is incomplete: no committed download mechanism, allowed file set, required-vs-excluded file classification, license-file custody fields, artifact schema, canonicalization rule, output path, or failure codes are defined.
5. The serving stack is not identified by product/package, immutable source revision, dependency manifest, installation source, or exact configuration.
6. “Verify FP8 support” has no committed verification procedure, test input, required evidence fields, expected output, or acceptance/failure criterion.
7. Target context lengths are absent for the candidate-primary and peer-primary co-residency test.
8. The co-residency memory test has no committed load order, cache/batch/concurrency configuration, warm-up rule, measurement source, sampling interval, peak-memory calculation, repetition rule, output schema, or acceptance threshold.
9. The fallback swap-procedure dry run has no committed procedure, initial/final state, ordered operations, synchronization/custody requirements, evidence schema, or pass/failure criterion.

## Work and verification status

- Checkpoints downloaded: none.
- External model repositories contacted: none.
- Packages or serving stacks installed: none.
- Environment checks or GPU measurements run: none.
- Qualification Q1–Q3, diagnostics, candidate runs, and scoring: none.
- Seeds accessed or exposed: none.
- Scaffold implementation resumed: no.
- Scientific specifications, thresholds, state, or provenance modified: none.
- Files created by TASK BUILDER: this durable block only.

## Holds and prohibited actions

No checkpoint substitution, quantization substitution, repository/revision selection, download, serving-stack installation, environment mutation, co-residency run, swap dry run, scaffold implementation, qualification Q1–Q3, development/protected-seed access, scoring, adaptive selection, backbone update, QLoRA, out-of-ladder model, native-CUDA L8, state/provenance mutation, merge, or gate decision is authorized while these inputs are absent.

## Exact next recipient and route

Return to **WORKFLOW COORDINATOR** for verification and routing to the appropriate persistent specification role. TASK BUILDER may resume only from committed executable authority that closes the missing inputs and is expressly released through the required governance path.

## Public-repository safety attestation

Public-safety scan: gitleaks scanned the complete introduced commit and found zero leaks. Credential, secret, private-key, environment-dump, and private-absolute-path regex review found zero prohibited content. Email-pattern review found two commit-metadata matches for the non-personal TASK BUILDER role identity; they were classified acceptable, not personal contact details. Manual content review found only public repository authority, governance terms, named public model families, and the executability block, all classified acceptable. `git diff --check` passed.
