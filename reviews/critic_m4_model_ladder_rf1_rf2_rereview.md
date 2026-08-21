# CRITIC Rereview — M4 Model Ladder RF1–RF2

**Timestamp:** 2026-08-21 EDT

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Persistent independent CRITIC rereview of M4 exact-peer ladder RF1–RF2 remediation, with tokenizer materialization and EF3 preserved as governed holds.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-model-selection-ladder-directive` at `9f79bdcaa029aba14308d2daad92519811303af6`.
- Prior authoritative rereview: `critic/m4-model-ladder-ef1-ef2-rereview` at `507fea656b67eecceb4c01242822a99240bc60bb`.
- ARCHITECT branch/head: `architect/m4-model-selection-ladder` at `4e36466159744d622370ac0a9198cdf71836d354`.
- Remediation result: `7a8239e9735042cddd94899ffaeaab53acf331fb`, direct parent `51b6e15aa9ba722da3ae06002d66dbe400c429fa`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_MODEL_LADDER_RF1_RF2_2026-08-21.md`.
- Corrected Phase A fixture/sidecar, preflight schema and three fixtures/sidecars, canonical fixture builder, specification/changelog delta, and preserved prior evidence.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: CLEAR**
- **Combined disposition: CLEAR**

RF1 and RF2 are closed. This CLEAR applies to the deterministic remediation package only. It does not release acquisition, preflight, qualification, implementation, or scoring; tokenizer-array materialization and EF3 remain mandatory governed inputs requiring later verification and Rebecca release.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** The delta changes no quoted law. Previously byte-verified P1–P3 and L7/L18/L19 quotations remain unchanged and verbatim against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`.
- **P3 CLEAR:** The corrected projection seal, ten-row topology, builder, ordering rules, fixtures, and failure semantics remain `[PROPOSED]`. No scientific threshold, locked bar, kill condition, or source classification changed.
- **P4 CLEAR:** The spec, schema, fixtures, builder context, and changelog remain dated 2026-08-21 under Regime B.
- **P5 CLEAR:** Rebecca's committed exact-peer amendment remains the explicit later authority for the same-checkpoint peer; no new deviation or waiver claim appears.
- **P6 CLEAR:** Exact-peer, tokenizer-reconciliation, EF3, local-only custody, and separate-operation authority claims remain faithful to the committed directives. No provenance citation changed.

## RF1 independent verification

- I reconstructed the Phase A peer projection by copying the fifteen fields in the fixture's fixed `peer_projection_order`, retaining their values and using RFC-8785 canonical object bytes without LF.
- The independent SHA-256 is `49bbf38b93bafdaeb6f7e8e38712d88686f15f9ab98034d95c1678036f989c51`, exactly matching the corrected fixture, specification, and builder constant.
- The corrected Phase A artifact is schema-valid and RFC-8785 canonical plus one LF. Its raw SHA-256 matches its adjacent sidecar. The projection excludes `candidate_self_state_vector` and all fields outside the fixed projection order.
- No other normative artifact contains a conflicting projection seal.

## RF2 independent verification

- The preflight PASS schema requires exactly ten rows by `minItems=10`, `maxItems=10`, and ordered `prefixItems` constraints.
- Required order and ordinals are exactly: `STACK_INDEX`/0, `STACK_PLATFORM`/1, `CHECKPOINT_FILES`/2, `CANDIDATE_PEER_EQUALITY`/3, `FP8_METADATA`/4, `FP8_FINITE_LOGITS`/5, `FORMAT_JSON`/6, `CONTEXT_1024`/7, `CONTEXT_4096`/8, and `CONTEXT_8192`/9. Every PASS row is constrained to `status=PASS`.
- The committed PASS fixture satisfies all ten rows and includes exact expected/observed evidence, including `{"answer":"A"}` for `FORMAT_JSON`.
- Independent negative mutations produced schema rejection for: one-row omission, duplicate replacement, adjacent reorder, ordinal mismatch, and `NOT_RUN` in PASS.
- BLOCKED and FAIL fixtures remain schema-valid with empty `checks`, preserve their prior status/failure meanings, and reproduce their canonical LF-terminated bytes and sidecars.
- Inspection of the committed builder confirms that its literal transforms append rows in the prescribed order, do not sort received evidence into compliance, and specify canonical JSON plus LF with matching sidecar generation. The schema and all four corrected JSON fixtures are Draft 2020-12/schema-valid as applicable and canonical; `git diff --check` passes.

## Blocking findings

None within RF1–RF2.

## Non-blocking findings

None.

## Preserved governed holds and material decisions

- Tokenizer-derived expanded arrays/hashes remain an authorized-local-materialization input. Before preflight, sanitized lengths/digests must be committed, persistently CRITIC-verified, and explicitly released by Rebecca. No executor may derive or approve them autonomously.
- EF3 remains unresolved by design: standard/harder battery manifests and SHAs are absent, and the Q2 band lacks Rebecca's signature. Qualification remains blocked.
- Rebecca must separately decide/release the Q2 band, battery bindings, tokenizer reconciliation, and any acquisition/preflight or qualification operation. None releases scaffold implementation or scoring.
- All prior valid exact-peer identity, Qwen custody, Llama exclusion, local-only model, schema/sidecar, deterministic ladder, FP8, frozen-backbone, nonadaptive, O-14/O-15, and public-safety evidence remains preserved.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify lineage and route the exact CLEAR package to Rebecca for her decisions while preserving the tokenizer and EF3 holds. No TASK BUILDER/executor role is released by CRITIC.

## Explicitly prohibited actions

No tokenizer/model access or download; acquisition; preflight; qualification; implementation; diagnostics/scoring; protected-seed access; adaptive change; model publication; L8 change; state/provenance mutation; rerun; merge; or gate decision other than Rebecca's authorized decisions. CRITIC did not edit/co-author the specification, schemas, controls, fixtures, builder, implementation, scoring artifacts, or `STATE.md`.

## Public-repository and local-model safety attestation

Before push, CRITIC scanned the review commit and complete delta with gitleaks and manually checked for credentials, signed URLs/tokens, PII, private paths, host/user/machine identifiers, environment dumps, protected seeds, model/tokenizer binaries or caches, adapters, reconstructive dumps, and model-related Git LFS pointers. No prohibited content was found. Public identities, revisions, filenames, byte sizes, SHA-256 values, repository-relative paths, synthetic fixtures, and source code were classified acceptable. `git diff --check` passed.

## Execution confirmation

No tokenizer or model artifact was accessed, read, downloaded, staged, committed, or published. No preflight, qualification, implementation, diagnostic/scoring execution, protected-seed access/exposure, adaptive change, rerun, state/provenance mutation, or unauthorized merge occurred.
