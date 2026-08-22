# CRITIC M4 Post-Tokenizer Integration Crash-Cart Design Review

Date: 2026-08-21 EDT  
Regime: B  
Role: authoritative persistent CRITIC  
Status: **COMBINED BLOCK**

## Immutable intake and validation

- Substantive head: `architect/m4-post-tokenizer-integration-crash-cart-design @ 390b06dadd2a364160d851c19cf85927465213d0`
- Review result: `fa64e01dfca6485220b8040c4369e14f3f3ca55f`
- Base: `cee97538893989e055f49a894f066d2083da4eb5`
- Canonical manifest: `architect/m4-post-tokenizer-integration-crash-cart-design-manifest-v2 @ 2d9f5e8446ff28ffee093b20c00a96d40ad4c23c`
- Checkout: repository `tools/workflow_checkout.py`; receipt SHA-256 `b857f4f35efe2b579890a36bffcb4fdd90a96378468d4f54aafe56489f4b51df`

The canonical manifest validates with `tools/workflow_contract_validator.py`. All eight manifest artifact SHA-256 values reproduce from raw Git blobs; both adjacent sidecars bind exact JSON bytes. The base-to-head delta is exactly the eight declared design-only paths. Superseded pre-addendum identities remain only in the preserved initial handoff; active manifest/specification/JSON/sidecar bindings are current.

## Banked design decisions

- The later Principal decision at `45d40d8b688fb7f44098d235df7f31cca1aa3b31` controls the older different-training rule. Candidate and peer are distinct runtime sessions of the same immutable checkpoint and training identity; runtime role/access/channel identities differ.
- Production construction forbids implicit synthetic fallback and separates candidate, peer, and control wrappers.
- Private reconciliation is ordered 1024/4096/8192 plus stop digest, with digest verification before fanout and sanitized evidence only.
- The high-level lifecycle permits multiple requests, later episodes, snapshot, and close, with first-failure precedence and byte-identical failure state.
- The pinned OCI topology is network-none, repository-read-only, no-custody, and isolated Python; it cannot invoke tokenizer materialization.
- Combined-tree construction is path-selective and rejects whole-tree merge/cherry-pick. Q2/EF3/native-L8 science remains separated from the mechanical seam.
- No private paths, token arrays, tokenizer/model bytes, custody values, credentials, seeds, or scientific results occur in the package.

## Batched blocking findings

### CC1 — Factory, real-backend, and role-adapter contracts are not mechanically complete

The factory must “enforce the exact role/arm map,” but neither the specification nor contract enumerates the allowed `role → scientific_arm` pairs or the deterministic failure codes for invalid combinations. `RealBackendProtocol` is described only as consuming a private array view and returning a payload; exact method signatures, request/response types, initialization/reset/snapshot/close responsibilities, error projections, and ownership of session state are absent. The design also lacks exact negatives for unknown backend, implicit fallback, invalid role/arm, registry/identity mismatch, unequal candidate/peer identity, non-distinct sessions/access identities, peer-channel bypass, backend failure, and response-correlation failure.

Bind a complete role/arm table, structural callable signatures and immutable input/output forms, responsibility boundaries, deterministic codes, and an exact production-path negative matrix.

### CC2 — Episode completion and in-flight lifecycle semantics are unrepresentable

`reset_episode` is allowed from every `STEPPED` state, while the prose limits reset to a “completed stepped episode.” No state field, transition, terminal request signal, or backend result marks an episode complete. Reset is therefore equally legal after request 0 of an unfinished multi-request episode. “Reset from an active call” is prohibited, but no in-flight state, serialization/locking rule, reentrancy rule, or concurrent-call disposition exists.

Define episode completion and active-call state mechanically. Enumerate every operation/state transition, including repeated describe/initialize/close, reset before/after completion, episode-id reuse, snapshot ordinals, request/reset ordinal faults, calls during an active backend operation, and every operation after close. Each negative must bind exact code, backend-call count, and byte-identical state evidence.

### CC3 — The synthetic fixture is not independently reproducible and its lifecycle sequences are ambiguous

The fixture supplies labels and expected call counts but no sanitized 1024/4096/8192 record lengths/digests, stop digest, deterministic process-local array generator, canonical private-array bytes, manifest/config request bytes, state requests, or expected before/after state and receipt digests. An implementer must invent the very values required to prove digest-before-fanout. Its main sequence enters close-path exercises before episode B, yet CLOSED is terminal; it does not say that the three close paths use independent adapters. Candidate/peer call count `3` is therefore not traceable to one exact set of instances and operations.

Bind the smallest complete deterministic fixture: generator/inputs, sanitized rows, expected digests, exact requests/states/receipts, per-instance sequences and call counts, and independent close-path fixtures.

### CC4 — Private-fanout and seam negative coverage is incomplete

The design covers sanitized-row corruption and one tampered rederivation but not candidate/peer received-digest divergence, mutable-view or backend mutation attempts, wrong context-to-request association, rederived stop-array mismatch distinct from sanitized stop-digest corruption, or backend suppression for every upstream semantic/identity failure. The canonical byte encoding of the immutable private array view is referenced indirectly rather than bound at this seam.

Bind the exact canonical view encoding and production-path negatives proving identical immutable fanout, independent adapter hashing, first-failure precedence, zero backend calls, and byte-identical state.

### CC5 — Exact L7/L8/L10/L14/L18 result semantics are not bound

The package binds only the ordered law identifiers and generic status/failure/evidence consistency. It does not bind each row to the exact repository law meaning: L7 mirror/peer and contamination requirements; L8 dose-dependent stakes coupling; L10 drifted-regime retrieval abstention; L14 stakes visibility/memory/thick-present coupling; and L18 contamination, oracle, frozen/naive, and seed requirements. Law-specific row shapes, allowed statuses, evidence references, not-run/held projections, and deterministic failures are absent. L10 is otherwise unmentioned in the design.

Bind verbatim/source-referenced law semantics and exact law-specific validation without selecting held Q2/EF3 thresholds or implementing native L8 science. Held scientific rows must have an explicit honest non-claim projection rather than a structurally valid generic row.

### CC6 — Future combined-tree raw construction remains underdetermined

The design defines the union concept but not the exact bytes of the appended tokenizer section: section heading/comment bytes, blank-line normalization, and terminal-LF behavior when the preserved base already has or lacks separators are not fully specified. “All `m4_tokenizer_*` JSON and sidecars” is a pattern rather than a frozen enumerated path inventory, and “direct downstream cascade” is not an exact dependency list. The wrapper and `src/__init__.py` paths are named, but their modes/bytes/digests and the selected implementation module set remain deferred.

Preserve the candid prerequisites, then require a Coordinator-designated pair of source SHAs, an explicit ordered overlay list, an exact byte-level union algorithm, fixed seam filenames, and a complete dependency/rebinding inventory before implementation publication.

## Law fidelity, public safety, and holds

The package correctly keeps Q2, EF3, real-backend selection, native L8, qualification, scoring, and scientific meanings held. The blocking findings require more mechanical design; they do not authorize those scientific choices. No constitutional text is reconstructed or changed.

Public-safety review found no prohibited content. Review preflight findings F000001-F000004 are two content occurrences duplicated across commit-parent and combined-range domains, wholly inside required public substantive/base commit identities on lines 10 and 12; they are classified as non-secret reproducibility metadata and are not suppressed. Manifest scanner findings on immutable public commit/artifact identities and the explicitly public `audit_tokenizer_sha` field likewise require manual classification. Gitleaks findings: zero. No implementation or governed execution was performed.

## Disposition

**COMBINED BLOCK.** Return through WORKFLOW COORDINATOR to ARCHITECT for one batched crash-cart design remediation covering CC1–CC6. Preserve the banked identity, supersession, no-custody, separation, and public-safety evidence. This review is independent of the active single materializer execution and does not affect its ownership or consumption state.
