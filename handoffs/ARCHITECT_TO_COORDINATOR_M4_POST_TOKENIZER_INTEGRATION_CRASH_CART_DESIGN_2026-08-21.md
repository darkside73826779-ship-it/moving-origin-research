# ARCHITECT to WORKFLOW COORDINATOR — M4 Post-Tokenizer Integration Crash-Cart Design

Date: 2026-08-21 EDT
Regime: B
Status: COMPLETE / READY FOR ONE PERSISTENT-CRITIC REVIEW

## Immutable result

- Base: `cee97538893989e055f49a894f066d2083da4eb5`
- Review result: `d225cfd2f9fb8d61e8039cbf4cf4d1d6c1949079`
- Work branch: `architect/m4-post-tokenizer-integration-crash-cart-design`
- Later same-checkpoint authority: `coordinator/m4-scaffold-rerelease-tokenizer-custody @ 45d40d8b688fb7f44098d235df7f31cca1aa3b31`
- Audited tokenizer head only: `0c418ef6aa22535c15e08cf88b45d4ced9bbee55`; final construction requires its eventual persistent-CRITIC-cleared source head.

## Complete design closure

The package explicitly resolves the old different-training-instance rule in favor of the later Principal decision: candidate and peer are separate runtime sessions of the same immutable checkpoint and training identity. It specifies a fail-closed backend protocol/factory with candidate, peer, and control wrappers and no implicit synthetic fallback.

The normative lifecycle now supports multiple ordered requests in one episode and reset into later episodes. The private-token seam rederives arrays inside the authorized executor, verifies the sanitized length/digest before any backend call, fans out byte-identical private views to distinct candidate/peer sessions, and emits only sanitized receipts. No token IDs are published.

Imperative semantic validation closes schema-only gaps, including CLOSED/`closed` consistency and an exact unique law set (`L7`, `L8`, `L10`, `L14`, `L18`). The smallest synthetic fixture covers digest verification, identical-input fanout, request ordinals 0/1, reset, next-episode ordinal 0, exact-law validation, and no-mutation negatives.

The package binds one exact pinned, network-none, read-only OCI command using platform digest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`. It uses isolated Python plus an explicit repository path insertion, fixing the natural isolated-import gap without changing scaffold implementation.

Combined-main construction is path-selective overlay, never branch merge/cherry-pick: the scaffold/current-main and tokenizer histories have incompatible merge bases, and a whole-tree merge could delete workflow/scaffold artifacts. The deterministic `.gitattributes` union preserves the designated-main file order, appends only novel tokenizer rules in source order, rejects conflicts, and creates a new forward combined identity domain. Historical executable-package identities remain immutable; only the combined `.gitattributes` row and its direct cascade are rebound unless raw reproduction proves another change.

## Separated prerequisites

Mechanical implementation still needs the Coordinator-designated final combined-main base SHA, the final cleared tokenizer source head, and fixed implementation filenames for the final raw inventory. Q2, EF3, and L8 decisions are needed only for real-backend selection, scientific output meanings/thresholds, hook semantics, qualification, and native L8; they do not block the integration seam.

## Complete changed raw Git-blob inventory

| Mode | Git blob | Bytes | Raw SHA-256 | Path |
|---|---|---:|---|---|
| 100644 | `970c590541ebe8b79a52f27e95b16ce495bc563a` | 3197 | `9de833efed2647fbe5ad2cb6c16ef235d721c3b2a5f643335459d74c697274a6` | `.gitattributes` |
| 100644 | `51e21f82e945d687a354410f359c042f6da4b183` | 3056 | `6e7178bfd3fe2b0381928008fc0a70f3ba4e8fa3a8c5b6d87b715b700da4ce76` | `specs/data/m4_post_tokenizer_integration_contract_v1.json` |
| 100644 | `0d2cdfd8bb5878d6a8cd8efa63dfa83fb8e60af8` | 113 | `32a2a57e43304e6a4dbe534b3b93b5ac379153f97b239dbb8c1440e61acc0c38` | `specs/data/m4_post_tokenizer_integration_contract_v1.json.sha256` |
| 100644 | `3355a0b8f74509c5058e51f8e88722d2c14f1b48` | 1486 | `7eb67fbfdc2d6953045585b5d680dc4954ddcf05fe1046ecb50eafbb09e4804c` | `specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json` |
| 100644 | `0cce93690e34a1cd36d4cc57e7857d34290cfc37` | 122 | `4b08103c267114028d276b727f9fee31340612d4698d39b5cd551e273e395c12` | `specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json.sha256` |
| 100644 | `8fe9de550e41cc90a5d1dcf33b8893d812317af1` | 10751 | `f218f0ef6dbe41120eee49ab8111c632d7af1750fbb3836ad4b7c64c560f9caf` | `specs/m4_post_tokenizer_integration_crash_cart_spec_v1.md` |

JSON parses, both adjacent sidecars reproduce, the diff is design artifacts only, and the worktree is clean. No implementation or governed execution was performed. No custody/model/tokenizer access, scoring, seeds, science, STATE/provenance mutation, merge, or gate decision occurred.

## Requested next event

Route this exact package once to the authoritative persistent CRITIC for complete design review.
