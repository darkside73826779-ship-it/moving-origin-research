# CRITIC Review — M4 Exact-Matched-Peer Model-Selection Ladder

**Timestamp:** 2026-08-21 EDT

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Persistent independent CRITIC review of the exact-matched-peer M4 qualification ladder and claimed nine-class executor-input closure, before Rebecca signature or any acquisition/preflight/qualification release.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-model-selection-ladder-directive` at `9f79bdcaa029aba14308d2daad92519811303af6`.
- ARCHITECT branch/head: `architect/m4-model-selection-ladder` at `77df0887570f60cbaa86b1548526a86a513b6bd9`.
- Specification result: `7b5f818f994a6c89c737fd1322f0b5b1c6affb64`, direct parent `9f79bdcaa029aba14308d2daad92519811303af6`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_MODEL_SELECTION_LADDER_2026-08-21.md`.
- Primary ladder spec; M4 spec/changelog delta; seven schemas, three bound control artifacts, and ten sidecars named by the handoff.
- Principal exact-peer amendment, qualification-ladder directive, and local-only custody directive at the authority commit.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

The exact-Qwen peer amendment, upstream identities, local-only custody, frozen ladder, and STOP state are sound. The package does not close end-to-end executor invention: result schemas and probe construction remain underdetermined, and the qualification battery/Q2 inputs are intentionally absent. It returns through WORKFLOW COORDINATOR to ARCHITECT; no executor role is released.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** I byte-compared the quoted P1–P3 and L7/L18/L19 text against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; it is verbatim. No reconstructed law text was used.
- **P3 CLEAR:** L7 bars and peer parity are tagged `[LAW-L7]`/`[BAR-Entry 11]`; development seeds use `[OP-Entry 11.7]`; all new model, runtime, resource, selector, calibration-algorithm, and Q2 criteria are `[PROPOSED]`, with Q2 expressly pending Rebecca's signature. No locked bar was silently changed.
- **P4 CLEAR:** The spec and all new JSON artifacts state 2026-08-21 and Regime B.
- **P5 CLEAR:** The exact-same-checkpoint peer differs from Entry 76's earlier independently trained-instance formulation, but this is not an unwaived silent deviation: Rebecca's later committed principal exact-peer amendment expressly supersedes the prior peer ladder and requires a separate runtime instance of identical revision and weight bytes. Constitutional L7's matched-model requirement is preserved.
- **P6 CLEAR:** The specification's authority claims match the committed principal ladder, exact-peer, and local-custody directives. The exact-peer equality list, Llama removal, Q2 signature requirement, frozen-backbone rule, and local-only model custody are accurately transcribed.

## Independently verified closures

- Official Qwen repository records corroborate the named primary/fallback repositories as Qwen-published Apache-2.0 FP8 checkpoints. The primary revision and its sole weight SHA-256, and the fallback revision and named shard SHA-256 values checked, match the committed manifest. No model was downloaded.
- Candidate and peer are specified as separate instances of the same rung's exact repository, revision, weight array, tokenizer, architecture, parameterization, quantization, decoding, calibration, evaluation, and binning; only instance identity and observable-only access differ. No Llama model remains binding or diagnostic.
- The ladder is ordered primary then fallback, backbones are frozen, decoding is fixed, Q4/QLoRA/out-of-ladder substitutions fail closed, and no failed stage is retried or adaptively modified.
- Acquisition uses immutable revisions, stored-order allow-lists, exact file-set/byte checks, all-weight hashes, an OCI-contained client, and sanitized repository-only custody metadata. The local-only several-gigabyte artifact rule is explicit.
- Seven Draft 2020-12 schemas pass metaschema validation. The three bound control artifacts validate against their schemas. All ten committed Git-blob sidecars exactly match their LF-terminated raw bytes. Singleton raw-byte equality protects the three controls from schema-valid substitution.
- The current status `BLOCKED_PENDING_BATTERY_SHA_AND_REBECCA_Q2_SIGNATURE` correctly prevents qualification from consuming invented batteries or unsigned Q2 values.

## Blocking findings

### EF1 — Spec defect: published result schemas leave executor-chosen structures and bytes

The contract publishes custody, preflight, qualification, and Phase A artifacts, but supplies no committed valid artifact/sidecar pairs or expected canonical digests for those outputs. More importantly, the schemas leave their central payloads structurally open:

- preflight `stack`, `co_residency`, and `swap` are unconstrained objects, while `fp8_checks` and `context_checks` have unconstrained array items;
- qualification `attempted_stages` and `failures` are arrays of unconstrained objects;
- Phase A `public_input_projection` is an unconstrained object, so the schema itself cannot enforce the observable-only boundary or exact peer projection;
- no exact ordering, constructor, semantic-validator algorithm, complete PASS/BLOCKED/FAIL realizations, canonical bytes, or expected digests are committed for these outputs.

An executor must invent field names, nested schemas, ordering, failure evidence, and canonical result bytes. This violates the binding result-schema/artifact-pair executability rule and prevents verification of positive and negative reachability.

### EF2 — Spec defect: the supposedly fixed context/format probe is not a deterministic realization

The spec names an ASCII instruction and token-count targets, but it does not fix the exact chat-template invocation/messages, template revision-to-bytes binding, insertion pointer/order for repeated ` x` tokens, exact rendered prompt/token-ID arrays at 992/4064/8160 tokens, stop-token array, or complete expected probe request/response artifacts and digests. Saying to “render” and insert repetitions before the final instruction leaves multiple conforming constructions.

The executor must choose the prompt envelope and derive unpublished realizations. The probe therefore cannot serve as byte-exact evidence for context support, deterministic decoding, format reachability, or peer equality.

### EF3 — Missing executable inputs: standard/harder batteries and Q2 authority are unresolved

Both battery bindings are null/`UNBOUND_REQUIRES_REBECCA_RELEASE`, and the Q2 numeric band remains `PROPOSED_PENDING_REBECCA_SIGNATURE`. The fail-closed status is correct and preserved; these are not hidden defaults. They nevertheless mean the qualification contract is not executable end to end today. Under the executable-input rule, a package presented as executor-input closure cannot receive substantive CLEAR while exact prompt/label/sample manifests, their SHAs, and the governing Q2 signature are absent.

These inputs require a separately committed reconciliation and persistent-CRITIC verification. They must never be filled by TASK BUILDER or the executor.

## Non-blocking findings

- The OCI index/platform digests are concretely pinned and the contract requires registry resolution before use. Their runtime compatibility remains prospective evidence for the authorized preflight, not evidence produced by this specification review.
- Q2 is a qualification-only material choice and does not alter scoring tau or constitutional L7/L10 bars.

## Material choices requiring Rebecca

1. Sign, reject, or revise the exact Q2 numeric band as one frozen package.
2. Release exact standard and harder battery manifests and SHA-256 bindings after persistent-CRITIC reconciliation.
3. After EF1–EF3 remediation and CLEAR, separately approve the exact model identities/serving-preflight package and separately authorize acquisition/preflight and qualification operations. None of these choices authorizes scaffold implementation or scoring.

## Preserved evidence

- Exact matched-peer identity, Llama exclusion, official Qwen FP8 provenance, immutable revision/weight custody, local-only model-artifact prohibition, deterministic decoding, FP8 floor, frozen backbones, nonadaptive escalation, O-14/O-15 fences, and the explicit BLOCKED status remain valid.
- The seven metaschema checks, three input validations, ten sidecar checks, and singleton raw-byte controls remain valid.
- Missing battery/Q2 inputs are preserved as explicit governed holds, not reclassified or silently filled.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify lineage and route this BLOCK to persistent ARCHITECT for deterministic remediation of EF1–EF2 while preserving EF3 as a Rebecca-gated reconciliation. The corrected package must return through Coordinator to persistent CRITIC. No TASK BUILDER/executor release follows from this review.

## Explicitly prohibited actions

No model download, installation, preflight, qualification, scaffold implementation, diagnostics, scoring, protected-seed access, adaptive change, model-artifact publication, L8 backend change, state/provenance mutation, rerun, merge, or gate decision. CRITIC did not edit/co-author the specification, schemas, controls, scoring artifacts, implementation, or `STATE.md`.

## Public-repository and model-custody safety attestation

Before push, CRITIC scanned the review commit and complete delta with gitleaks and manually checked for credentials, signed URLs/tokens, PII, private paths, host/user/machine identifiers, environment dumps, protected seeds, model binaries/caches/adapters, reconstructive dumps, and model-related Git LFS pointers. No prohibited content was found. Public repository identities, revisions, filenames, byte sizes, SHA-256 values, license/source references, repository-relative paths, and specification evidence were classified acceptable. `git diff --check` passed.

## Execution confirmation

No model artifact was downloaded, read, staged, committed, or published. No preflight, qualification, implementation, diagnostic/scoring execution, protected-seed access/exposure, rerun, adaptive change, state/provenance mutation, or unauthorized merge occurred.
