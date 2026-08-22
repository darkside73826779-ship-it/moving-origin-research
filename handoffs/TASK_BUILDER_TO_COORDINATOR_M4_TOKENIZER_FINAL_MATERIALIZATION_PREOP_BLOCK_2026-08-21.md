# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER FINAL MATERIALIZATION PRE-OPERATION BLOCK

**Date:** 2026-08-21

**Regime:** B

**Status:** BLOCK

**Gate served:** Mandatory pre-operation identity gate for the single final bounded tokenizer materialization

## Canonical intake

- Final re-release: `coordinator/m4-tokenizer-final-materialization-rerelease` at `52b3ef2e85cb585f5dd81fc845bedfde00d42072`.
- Cleared implementation package: `taskbuilder/m4-tokenizer-cr-ffrbf1-imported-class-remediation` at `05a3e8a9abd398f1b8ce36838fcf533e46d50bd1`.
- Final persistent-CRITIC CLEAR: `critic/m4-tokenizer-cr-ffrbf1-final-rereview` at `472d4afeada549a939faaffa934083cdced9369c`.
- Work branch: `taskbuilder/m4-tokenizer-final-materialization-execution`.

## Blocking pre-operation finding

The committed executable-package identity manifest conflicts with the immutable released checkout in the binding raw Git-blob domain:

| Path | Manifest bytes / SHA-256 | Released raw Git blob bytes / SHA-256 |
|---|---|---|
| `diagnostics/m4_tokenizer_materialization.py` | `12634` / `42ffd11ac11ec882dc824906f2a9995b8d932094e4e01a8b36ee7911dd22d5af` | `21096` / `90e89b5a55ff80041a8e09c0d3e96208b6d8eff5c6b39eecd6366a1afb5289af` |
| `tests/test_m4_tokenizer_materialization.py` | `12302` / `8a40cc5956e413b3748775d83be18ae8bd91e9b3d2d791d9a032d299b1e39d80` | `54972` / `964ab5b8cb5ef63627c0ab07b3f0c4c867684d7add40576c3dd61494610e8613` |

The manifest is `specs/data/m4_tokenizer_executable_package_v1.json` at the exact released commit. The comparison independently hashes raw bytes returned by `git cat-file blob 52b3ef2e85cb585f5dd81fc845bedfde00d42072:<path>`; no worktree normalization or text conversion is involved.

The release requires the committed executable package and immutable cleared checkout to agree. Reconstructing or updating identity metadata is not authorized. The mandatory pre-operation gate therefore fails closed before the test wrapper and before materializer start.

## Requirement → production/gate → evidence trace

| Requirement | Gate branch | Evidence | Disposition |
|---|---|---|---|
| Fresh immutable release checkout | workflow checkout helper at exact release SHA | clean checkout at `52b3ef2e85cb585f5dd81fc845bedfde00d42072`; `git fsck --full` PASS | PASS |
| Committed executable package matches released bytes | compare manifest bytes/digests to raw Git blobs | both mutable executable entries mismatch as shown above | BLOCK |
| Run pre-import wrapper only after package identity PASS | execution order `VERIFY_FRESH_CHECKOUT_AND_IMAGE` before `RUN_PREIMPORT_TEST_WRAPPER` | wrapper was not invoked | NOT RUN, correct fail-closed behavior |
| Start one materializer only after all validation/tests PASS | execution order `STOP_ON_NONZERO` before `RUN_SINGLE_MATERIALIZER` | materializer was not started | NOT RUN; operation unconsumed |

## Ordered access-event trace

`release checkout verification → executable manifest read → raw Git-blob materializer identity mismatch → raw Git-blob selected-test identity mismatch → STOP`

No custody environment lookup, custody-root resolution, private-record read, weight observation, tokenizer/config read or copy, loader import, `from_pretrained`, output-stage creation, test-container launch, or materializer launch occurred.

## Preserved boundaries and route

- The single materialization operation remains **UNCONSUMED**.
- No routed custody/model/tokenizer access, OCI materialization, retry, fallback, inference, qualification, scoring, protected seeds, science, STATE/provenance mutation, model/tokenizer publication, merge, rerun, or gate decision occurred.
- **Exact next recipient:** WORKFLOW COORDINATOR for durable executable-package identity remediation/rerouting by authorized roles.
