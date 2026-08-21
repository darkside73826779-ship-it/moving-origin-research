# CRITIC Rereview — M4 Model Ladder EF1–EF2

**Timestamp:** 2026-08-21 EDT

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Persistent independent CRITIC rereview of M4 exact-peer ladder EF1–EF2 remediation, with EF3 and tokenizer materialization preserved as governed inputs.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-model-selection-ladder-directive` at `9f79bdcaa029aba14308d2daad92519811303af6`.
- Prior authoritative review: `critic/m4-model-selection-ladder-review` at `6c0785398406812b6109c373d6cca7d7da6f52e6`.
- ARCHITECT branch/head: `architect/m4-model-selection-ladder` at `51b6e15aa9ba722da3ae06002d66dbe400c429fa`.
- Remediation result: `748eb8e45c89c438f8684399f602455200538554`, direct parent `77df0887570f60cbaa86b1548526a86a513b6bd9`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_MODEL_LADDER_EF1_EF2_2026-08-21.md`.
- Twenty-one named JSON schemas/controls/contracts/fixtures and all adjacent sidecars; narrow specification/changelog delta; preserved prior-review evidence.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

EF2's constructor is deterministically specified up to a correctly governed tokenizer-derived reconciliation, but EF1 remains open: the committed Phase A positive fixture violates its own projection-digest invariant, and the preflight PASS evidence omits prescribed checks. No executor/preflight/qualification role is released.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** The remediation changes no quoted law. Previously byte-verified P1–P3 and L7/L18/L19 quotations remain unchanged and verbatim against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`.
- **P3 CLEAR:** New schema fields, fixtures, context constructor, reconciliation conditions, and failure semantics remain `[PROPOSED]`. No locked scientific threshold, kill condition, or source classification changed.
- **P4 CLEAR:** The amended specification and JSON artifacts retain 2026-08-21 and Regime B.
- **P5 CLEAR:** Rebecca's committed exact-peer amendment remains the explicit later authority for the same-checkpoint peer; no new deviation or waiver claim was introduced.
- **P6 CLEAR:** Exact-peer, Q2-signature, battery-release, tokenizer-custody, local-only artifact, and separate-operation authority claims match the committed principal directives. No provenance citation changed.

## Independent validation and preserved closures

- All twenty-one named JSON files parse. Seven schemas pass Draft 2020-12 metaschema validation. The three singleton controls and all ten new custody/preflight/qualification/Phase A fixtures validate against their named schemas.
- All twenty-one adjacent sidecars match the exact LF-terminated Git blobs. All ten output fixtures are RFC-8785 canonical JSON plus one LF. `git diff --check` passes.
- Custody PASS/BLOCKED/FAIL and qualification selected/BLOCKED/exhausted structures are now exhaustively typed at their nested levels. Preflight nested objects/rows are typed, and the Phase A `public_input_projection` admits only `input_text`, `option_labels`, and `history_sha256`; `candidate_self_state_vector` cannot enter that object.
- The exact context constructor fixes the chat-template call, sole user message, flags, neutral fragment, unique insertion location, target lengths, token-array hash domain, decode/encode identity, stop-array source/order, output object, and member order.
- Exact-peer identity, official Qwen/revision/weight custody, Llama exclusion, local-only model rule, frozen ladder, deterministic decoding, FP8 floor, nonadaptive escalation, O-14/O-15, and explicit inoperative status remain preserved.

## Blocking findings

### RF1 — Construction bug: the committed Phase A “valid” fixture has an invalid peer-projection digest

The spec requires construction of the peer projection by copying the fifteen fields in `peer_projection_order`, in that order, then hashing the RFC-8785 object without LF. Independently applying that exact algorithm to `m4_phase_a_transcript_valid_v1.json` yields:

`49bbf38b93bafdaeb6f7e8e38712d88686f15f9ab98034d95c1678036f989c51`

The committed fixture instead stores sixty-four zeroes in `peer_projection_sha256`. The spec states fixture zero hashes are literal synthetic values, not wildcards; therefore the constructor cannot replace this discrepancy without contradicting the claimed complete positive artifact. The fixture is structurally schema-valid but semantically invalid, so positive projection reachability and the observable-only sealing evidence are not established.

### RF2 — Spec defect: the preflight PASS schema/fixture cannot record the complete prescribed check sequence

The preflight procedure prescribes stack index/platform verification, checkpoint files, candidate/peer equality, FP8 metadata, finite logits, JSON format, and three context checks. The check enum names all ten, but the result topology provides only:

- a `stack` status object;
- `fp8_checks` capped at two rows; and
- `context_checks` capped at three rows.

The committed PASS fixture consequently contains only FP8 metadata/finite-logit rows and the three context rows. It contains no `FORMAT_JSON` row and no ordered rows for `STACK_INDEX`, `STACK_PLATFORM`, `CHECKPOINT_FILES`, or `CANDIDATE_PEER_EQUALITY`. The separate stack/custody fields do not encode expected/observed evidence for all those checks, and nothing encodes the required exact JSON parse result.

Thus a schema-valid PASS can omit mandatory checks, and the claimed complete procedural ordering/positive reachability is false. The schema, constructor, and PASS/BLOCKED/FAIL fixtures must make every applicable prescribed check explicit and fail closed on omission, duplication, reordering, or `NOT_RUN` in PASS.

## Tokenizer materialization determination

The deferred expanded token arrays/hashes are a **correctly fail-closed governed input**, not executor invention, because:

- their source tokenizer is bound to the exact rung repository/revision and custody checks;
- their derivation algorithm and hash domain are fixed;
- the current role is expressly forbidden to read/download the tokenizer;
- an authorized local custody step must commit only sanitized lengths/digests, followed by persistent-CRITIC verification and Rebecca release; and
- preflight remains prohibited until that reconciliation.

This determination does not make preflight executable today and does not release it. If the future materialization produces ambiguity, non-unique insertion, failed encode/decode identity, or differing arrays, it must STOP rather than alter the constructor.

## EF3 and material decisions preserved

- EF3 remains governed: standard/harder battery manifests and SHAs are unbound, and the Q2 band lacks Rebecca's signature. Qualification remains `BLOCKED_PENDING_BATTERY_SHA_AND_REBECCA_Q2_SIGNATURE`.
- Rebecca must decide the exact Q2 band, release exact battery bindings after reconciliation, release the tokenizer-array reconciliation after CRITIC verification, and separately authorize any acquisition/preflight or qualification operation.
- None of those decisions authorizes scaffold implementation or scoring.

## Non-blocking findings

None beyond the correctly governed pending inputs described above.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify lineage and route this BLOCK to persistent ARCHITECT for deterministic RF1–RF2 remediation. The corrected package must return through Coordinator to persistent CRITIC. EF3 and tokenizer materialization remain separate governed inputs; no executor role is released.

## Explicitly prohibited actions

No tokenizer/model read or download; preflight; qualification; implementation; diagnostics; scoring; protected-seed access; adaptive change; model publication; L8 change; state/provenance mutation; rerun; merge; or gate decision. CRITIC did not edit/co-author the specification, schemas, controls, fixtures, implementation, scoring artifacts, or `STATE.md`.

## Public-repository and local-model safety attestation

Before push, CRITIC scanned the review commit and complete delta with gitleaks and manually checked for credentials, signed URLs/tokens, PII, private paths, host/user/machine identifiers, environment dumps, protected seeds, model/tokenizer binaries or caches, adapters, reconstructive dumps, and model-related Git LFS pointers. No prohibited content was found. Public identities, revisions, filenames, byte sizes, SHA-256 values, repository-relative paths, and synthetic fixtures were classified acceptable. `git diff --check` passed.

## Execution confirmation

No tokenizer or model artifact was read, downloaded, staged, committed, or published. No preflight, qualification, implementation, diagnostic/scoring execution, protected-seed access/exposure, adaptive change, rerun, state/provenance mutation, or unauthorized merge occurred.
