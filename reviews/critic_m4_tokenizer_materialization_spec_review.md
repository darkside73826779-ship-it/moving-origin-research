# CRITIC Review — M4 Bounded Local Tokenizer Materialization

**Timestamp:** 2026-08-21 EDT

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Work Item B only — persistent independent CRITIC review of the bounded local tokenizer-materialization specification before any tokenizer access or materialization.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-scaffold-rerelease-tokenizer-custody` at `45d40d8b688fb7f44098d235df7f31cca1aa3b31`.
- Originating TASK BUILDER block: `taskbuilder/m4-tokenizer-custody` at `ad8c6013f6efaa3e2cad2e248c9d90f890537aa3`.
- ARCHITECT branch/head: `architect/m4-tokenizer-materialization-spec` at `68b063cb7cd5857b2104fdee85902a0ccc3f810f`.
- Specification result: `e3f0d331cb1e1b0672cd3ef2c016f97ebaaeb8d6`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_MATERIALIZATION_SPEC_2026-08-21.md`.
- Work Item B spec/changelog; singleton request, result schema, synthetic PASS/BLOCKED/FAIL fixtures, test contract, and all six sidecars.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

Several missing classes are now fixed, but the bounded action remains non-executable without invention. The only authorized payload is `tokenizer.json`, while the contract requires an exact chat template and tokenizer metadata that are not bound or readable; the private custody-record lookup is also undefined. Work Item B returns through Coordinator to persistent ARCHITECT. No tokenizer access/materialization is released.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** I byte-compared the quoted P1–P3 text against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; it is verbatim. This custody-only work item operationalizes no scientific law text.
- **P3 CLEAR:** Every identity, byte count, hash, target length, context length, token ID, command, exit code, and test criterion introduced by the specification is tagged `[PROPOSED]`. Q2 is expressly unsigned and no locked scientific bar is changed.
- **P4 CLEAR:** The spec and all six JSON artifacts state 2026-08-21 and Regime B.
- **P5 CLEAR:** No constitutional or locked-bar deviation is claimed.
- **P6 CLEAR:** The bounded read, immutable preserved artifact, isolated copy, sanitized-metadata-only publication, later CRITIC verification/Rebecca release, and continuing holds accurately reflect authority `45d40d8...`. The referenced ladder constructor path/commit/digest is exact.

## Independently verified closures

- The request fixes the official primary Qwen repository, immutable revision, FP8 identity, weight filename/bytes/SHA-256, `tokenizer.json` filename/bytes/SHA-256, public custody handle, constructor commit/path/digest, three array identities and lengths, digest domain, output path, and blocked status.
- The result schema passes Draft 2020-12 metaschema validation. Synthetic PASS, BLOCKED, and FAIL fixtures validate; deleting one PASS array causes rejection.
- All six JSON files parse and all six adjacent sidecars match their exact raw Git blobs. The stop-array RFC-8785/no-LF digest independently reproduces as `580af853441f1d705732a492fe363f022bdd177c37d2b8f82035cbdf9a604b8c` for `[151645]`.
- The schema excludes private paths, rendered text, and token arrays. The public repository/revision/file hashes are sanitized reproducibility and integrity metadata, not credentials or secret material.
- The three array construction formula, encode/decode equality, stop-source order/deduplication, result path, publication encoding, callable name, command, exit codes, and named positive/negative test classes are materially specified.

## Blocking findings

### TF1 — Missing executable input: the authorized tokenizer payload cannot supply the mandated chat template

Section 2 permits reading only `tokenizer.json` and forbids every other tokenizer file. Sections 4–5 nevertheless require `apply_chat_template(...)`, `eos_token_id`, and exact `<|im_end|>` resolution. The specification does not commit or authorize a `tokenizer_config.json`, chat-template string/digest, special-token configuration, or an exact constructor that instantiates a tokenizer and injects those values from committed public metadata.

`tokenizer.json` binds tokenization vocabulary/model data, but the contract supplies no executable source for the exact chat-template bytes used by `apply_chat_template`. The referenced ladder constructor itself says tokenizer and chat-template bytes come from the verified rung revision; it does not embed them. TASK BUILDER must therefore choose a template/config source or broaden the read scope, both unauthorized inventions. The three arrays cannot be deterministically materialized under the stated custody boundary.

### TF2 — Missing executable input: private custody-record resolution remains undefined

The environment variable resolves a private root, but the contract says only that the root “must contain a private custody record.” It fixes no repository-relative-to-root filename, byte format/schema, required field names/order, canonicalization, digest, uniqueness rule, or resolver algorithm. It also does not define how “multiple resolution” is detected.

The executor must choose where and how to find and parse the record that authorizes the tokenizer read. An opaque public handle correctly avoids publishing a private path, but it does not eliminate the need for a deterministic private resolver contract. This leaves the custody gate non-executable and makes positive/negative custody reachability implementation-defined.

### TF3 — Spec defect: PASS does not schema-bind the exact stop digest

The prose requires the sole stop array `[151645]` and its exact digest, but the PASS schema constrains `stop_array_length` to one while accepting any lowercase 64-hex `stop_array_sha256`. The real digest appears only in the synthetic fixture. A schema-valid published PASS can therefore assert a different stop digest.

The PASS branch must require the literal digest `580af853441f1d705732a492fe363f022bdd177c37d2b8f82035cbdf9a604b8c` (or apply an equally exact semantic validator whose algorithm, failure code, and negative fixture are committed). Otherwise exact stop construction is not fail-closed.

### TF4 — Executability/provenance defect: runtime dependency identity is absent

The callable relies on Python tokenizer behavior (`apply_chat_template`, encode, decode, token conversion), but no sealed Python/tokenizer-library version, dependency manifest/hash, constructor implementation identity, or allowed loading API is specified. Different compatible library versions can interpret template flags and special tokens differently. The prescribed command names a future file but does not bind the implementation/runtime that will execute the contract.

This omission is material because the output is precisely the library-derived arrays and hashes. TASK BUILDER would have to select packages and loading behavior. The deterministic contract must bind the dependency/runtime identity or provide an implementation whose behavior is fully independent of such choices.

## Non-blocking findings

- Synthetic all-zero array digests are clearly labeled topology-only and non-publishable. They are not misrepresented as materialization evidence.
- Q2 and EF3 are outside Work Item B and remain correctly held.

## Preserved evidence

- Exact Qwen identity metadata, opaque handle name, constructor identity, array names/formula, encode/decode criterion, stop value/digest, sanitized path/schema, integer-array digest domain, invocation/test vocabulary, local-only custody, immutable-source/isolated-copy policy, and public-safety controls remain valid where not dependent on TF1–TF4.
- Request status remains `BLOCKED_PENDING_REBECCA_EXECUTION_RELEASE`. No result digest has been fabricated or treated as evidence.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify lineage and route this BLOCK to persistent ARCHITECT for deterministic remediation of TF1–TF4. The corrected package must return through Coordinator to persistent CRITIC. Only a future combined CLEAR may route to Rebecca for an explicit execution release.

## Explicitly prohibited actions

No tokenizer/model access or download; materialization; package/environment mutation; acquisition; preflight; qualification; implementation; diagnostics/scoring; protected-seed access; scaffold or Work Item A edits; model publication; state/provenance mutation; rerun; merge; or gate decision. CRITIC did not edit/co-author the specification, schemas, fixtures, contracts, implementation, scoring artifacts, or `STATE.md`.

## Public-repository and local-custody safety attestation

Before push, CRITIC scanned the review commit and complete delta with gitleaks and manually checked for credentials, private custody values, signed URLs/tokens, PII, private paths, host/user/machine identifiers, environment dumps, protected seeds, tokenizer/model bytes or caches, adapters, reconstructive dumps, and model-related Git LFS pointers. Public tokenizer/weight SHA-256 values were classified as permissible reproducibility metadata, not secrets. No prohibited content was found. `git diff --check` passed.

## Execution confirmation

No tokenizer/model artifact was accessed, read, downloaded, copied, hashed, staged, committed, or published. No materialization, environment mutation, preflight, qualification, implementation, diagnostic/scoring execution, protected-seed access/exposure, Work Item A change, state/provenance mutation, rerun, or unauthorized merge occurred.
