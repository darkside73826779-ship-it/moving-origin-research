# CRITIC Rereview — M4 Tokenizer Materialization TF1–TF4

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Work Item B only — independent law-fidelity, executability, custody, regression, and public-safety rereview before any tokenizer materialization

## Inputs and SHAs reviewed

- Authority: `coordinator/m4-scaffold-rerelease-tokenizer-custody@45d40d8b688fb7f44098d235df7f31cca1aa3b31`
- Prior authoritative review: `critic/m4-tokenizer-materialization-spec-review@b1af0158eb9a002aaf515eed0374967e38fb0523`
- ARCHITECT branch/head: `architect/m4-tokenizer-materialization-spec@63a104ac78d025e2fdff42518d32f6f81ba9fc67`
- Specification result: `419151e61227b6e60efa837cb10ee4a79252ed1b`
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_TF1_TF4_REMEDIATION_2026-08-21.md`
- Specification: `specs/m4_local_tokenizer_materialization_spec_v1.md`
- Seven tokenizer request/schema/fixture/test JSON artifacts and their sidecars under `specs/data/`

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

TF3 and the contract portion of TF4 close. TF1 and TF2 remain non-executable/fail-open, and independent schema validation found a separate published-result digest type defect. No tokenizer access or execution is released.

## First checklist item — law, tags, and provenance

- **P1/P2 CLEAR:** I compared the quoted P1–P3 text against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; it is verbatim. The remediation changes no quoted law.
- **P3 CLEAR:** New identities, sizes, hashes, runtime digests, failure rules, commands, and acceptance criteria are tagged `[PROPOSED]`. No locked scientific threshold or bar changes.
- **P4 CLEAR:** The amended spec, changelog, handoff, schemas, and fixtures state 2026-08-21 and Regime B through their headers or schema metadata.
- **P5 CLEAR:** No constitutional deviation or scoring authorization is asserted.
- **P6 CLEAR:** The bounded local read, immutable preserved source, isolated copy, sanitized-only publication, later persistent-CRITIC verification, Rebecca release, Q2 deferral, and EF3 hold match authority `45d40d8...`. The delta adds no false “Entry n said X” claim.

## Independently verified closures

### TF3 — closed

Canonical UTF-8 bytes without LF for `[151645]` independently hash to `580af853441f1d705732a492fe363f022bdd177c37d2b8f82035cbdf9a604b8c`. The PASS branch requires that literal digest and length one. A mutated all-zero stop digest is rejected.

### TF4 — contract closure preserved

The spec binds one OCI index digest, one Linux/amd64 platform digest, one exact `AutoTokenizer.from_pretrained` call with fixed arguments, the isolated Python invocation, and `RUNTIME_IDENTITY_MISMATCH` before custody lookup for alternate environments or loading APIs. The three result fixtures and result schema consistently bind both OCI digests. No registry, tokenizer, model, image, or local runtime was accessed during this review.

### Fixtures, schemas, and sidecars

- Synthetic PASS, BLOCKED, and FAIL fixtures validate against the result schema.
- All seven JSON Git blobs have matching adjacent SHA-256 sidecars.
- The request sidecar remains `85f7eba2c872fc10fba00f088c1bbf6f6334ee69cfe35a856364e58d949a98b2`.
- The result schema loads under the available Draft-compatible validator, and its ordered PASS rows/checks remain enforced.

## Blocking findings

### RF1 — TF1 remains unbound: tokenizer-config identity is self-attested and absent from the public result

The selected revision, `tokenizer_config.json` filename, and byte count are fixed, but its SHA-256 is not. The private schema accepts any syntactically matching digest, and §3 makes that same private record the authority for the file digest. There is no independently bound expected config digest against which that attestation is checked. The sanitized request and result also omit `tokenizer_config_sha256`, although Rebecca's authority permits sanitized filename/size/hash metadata.

Consequently, two different 9,377-byte `tokenizer_config.json` files can each be self-attested by changing the private record, load different templates or special-token declarations, and still produce schema-valid public results. Template equality proves equality only to the unbound local file, not to the exact immutable-revision configuration. This leaves the executable source for the chat template and special tokens without a fixed identity and prevents later CRITIC verification from determining which configuration produced the arrays.

**Classification:** specification/executability and provenance defect. TF1 is not closed.

### RF2 — TF2 custody schema accepts a non-string SHA-256

`m4_tokenizer_private_custody_record_schema_v1.json` defines `/tokenizer_config/sha256` with a regex `pattern` but omits `"type":"string"`. Under Draft 2020-12, `pattern` does not reject non-strings. I constructed a complete otherwise-valid custody record with numeric `sha256: 7`; the committed schema accepted it.

The record therefore does not enforce the promised lowercase 64-hex digest or provide a deterministic digest-comparison input. The required negative fixture/test for this type error is also absent.

**Classification:** construction/schema defect. TF2 is not closed.

### RF3 — Published PASS array digests are not type-safe

The result schema's `$defs.array.properties.sha256` likewise supplies `pattern` without `"type":"string"`. I changed the first PASS array digest to numeric `7`; the complete PASS artifact remained schema-valid. A published PASS can therefore contain a non-digest value even though the contract requires three SHA-256 strings.

This defect predates the narrow TF remediation but is within the required independent schema validation and directly affects the artifact that a future persistent CRITIC must verify.

**Classification:** construction/schema and publication-custody defect.

## Non-blocking findings

- The TF4 OCI identifiers are exact and internally consistent, but their external registry existence was not queried because this review expressly prohibited image acquisition/preflight and excluded the Coordinator's non-authoritative local fact-finding.
- `git diff --check` reports Markdown trailing spaces on the handoff date line; they are a rendering convention and do not affect the contract.
- Gitleaks reported three `generic-api-key` findings, all the same committed public tokenizer SHA-256 in the PASS/BLOCKED/FAIL fixtures. These are permitted reproducibility metadata, not credentials.

## Preserved evidence

- Prior LAW_FIDELITY CLEAR remains valid.
- TF3 is closed.
- TF4's fixed runtime/loading contract is preserved where it does not depend on RF1–RF3.
- Exact Qwen repository/revision, weight identity, tokenizer.json identity, public handle, constructor identity, array names/formula, encode/decode rule, stop construction, result path, local-only custody, immutable-source/isolated-copy policy, Q2 deferral, EF3 hold, and execution prohibitions remain valid.
- The request remains `BLOCKED_PENDING_REBECCA_EXECUTION_RELEASE`; no materialized result was fabricated.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify lineage and return this BLOCK to persistent ARCHITECT for narrow remediation of RF1–RF3. The corrected package must return through Coordinator to persistent CRITIC. Rebecca execution release and TASK BUILDER remain held.

## Explicitly prohibited actions

No tokenizer/model/image access or download; materialization; package/environment mutation; acquisition; preflight; qualification; implementation; diagnostics/scoring; protected-seed access; Work Item A edits; state/provenance mutation; rerun; merge; gate decision; or TASK BUILDER release. CRITIC did not edit or co-author the specification, schemas, fixtures, implementation, scoring artifacts, or `STATE.md`.

## Public-repository safety attestation

Before push, CRITIC scanned all three introduced commits and every intermediate diff in `e3f0d331cb1e1b0672cd3ef2c016f97ebaaeb8d6..63a104ac78d025e2fdff42518d32f6f81ba9fc67`, plus this review. Gitleaks and targeted regex/manual checks covered credentials, tokens, keys, PII/contact details, private paths, host/user/machine identifiers, environment dumps, protected seeds, tokenizer/model/image bytes or caches, adapters, reconstructive dumps, and prohibited Git LFS pointers. Three gitleaks findings were the public tokenizer SHA-256 and were classified acceptable reproducibility metadata. Email-shaped matches were the synthetic role identity. No prohibited finding remains.

## Execution confirmation

No tokenizer/model/OCI artifact was accessed, read, downloaded, copied, hashed, staged, committed, or published. No materialization, environment mutation, acquisition, preflight, qualification, implementation, diagnostic/scoring execution, protected-seed exposure, Work Item A change, state/provenance mutation, rerun, unauthorized merge, or gate decision occurred.
