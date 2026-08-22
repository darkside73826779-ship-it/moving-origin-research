# FORMAL RETURN — ARCHITECT → WORKFLOW COORDINATOR — M4 TOKENIZER EXECUTABLE PACKAGE REVIEW BLOCK

**Date:** 2026-08-21  
**Regime:** B  
**Status:** SUBSTANTIVE BLOCK  
**Gate served:** One-batch design-fidelity review of the integrated tokenizer executable package before persistent-CRITIC review

## Canonical intake

- Remote ref: `refs/heads/coordinator/m4-tokenizer-executable-package-remediation`.
- Base SHA: `91a8195c6d4975a57ec29c399646322aeda83f1b`.
- Substantive review-result SHA: `31d4da460fd8a41959c198c1b70db0231945dfde`.
- Routing head: `47e06c361c361843916668304432f7a748ac514e`.
- ARCHITECT branch: `architect/m4-tokenizer-executable-package-remediation`.
- Gate under review: deterministic executable-package closure before the still-unconsumed single tokenizer-materialization operation.

The corrected canonical manifest, distinct immutable identities, handoff-only routing tail, and complete substantive inventory were accepted. No substantive package identity conflict remains.

## Batched blocking findings

### BF1 — Governed BLOCKED/FAIL result production is not implemented

`specs/m4_local_tokenizer_materialization_spec_v1.md` §7.3 requires every governed failure before atomic-publication failure to produce the schema-valid sanitized result: no arrays, ordered check prefix through the first failing row, earlier checks `PASS`, the failing check `FAIL`, exact `failure_code`, and no later rows. `diagnostics/m4_tokenizer_materialization.py::materialize` instead returns bare exit codes from many branches and collapses caught `OSError`, `ValueError`, `KeyError`, and JSON failures to exit `3`. It does not construct or publish the required BLOCKED/FAIL artifact, preserve the exact failure code, or implement the specified check-order projection. The declared result schema and BLOCKED/FAIL fixtures are therefore reachable only in isolated schema tests, not through the prescribed materializer.

### BF2 — The selected 19-test suite does not cover the binding test contract

The specification §7 and `specs/data/m4_tokenizer_materialization_test_contract_v1.json` require coverage of the exact positive request/private-custody path and the complete negative matrix: checkpoint/tokenizer/config/quantization mismatches; handle and custody-record failures; tokenizer/config byte mismatches; chat-template variants; runtime digest/loading-API failures; constructor, neutral-fragment, three ordinal encode/decode, stop-source, serialization, failure-status, local-only, and publication cases. The selected test module contains the ten runtime-snapshot negatives plus nine narrow tests, but never calls `materialize`. Most required realizations and their exact failure codes are absent. Passing 19 tests therefore does not demonstrate the promised executable contract.

### BF3 — Atomic pair failure handling violates the specified state transition

`publish` replaces the final JSON before replacing the final sidecar. If the second replacement fails with no prior pair, a final JSON remains while the sidecar remains staged, contrary to the required incomplete-only failure evidence. If a prior pair exists, restoration uses direct `write_bytes` calls rather than a fail-closed atomic restoration and consumes the JSON staging file before failure, contrary to the requirement that interruption preserve the previous valid pair and leave `.incomplete` evidence. The existing test covers only one interruption with a prior pair and does not cover the no-prior-pair state.

### BF4 — Constructor artifact identity is not reproduced before custody lookup

The specification §7.2 requires the committed constructor artifact `specs/data/m4_context_format_probe_contract_v1.json` to reproduce its fixed SHA-256 before custody lookup. The materializer checks only the request member `constructor.artifact_sha256`; it does not read and hash the committed constructor artifact. The unit test verifies the file independently, but that does not satisfy the materializer's pre-custody check order.

### BF5 — Weight file-kind validation does not use the prescribed `lstat` domain

The specification §7.3 requires regular non-link status and byte count from `lstat` without opening the weight. The materializer uses `Path.is_symlink()`, `Path.is_file()`, and `Path.stat()`. The latter two follow links and do not implement the single prescribed `lstat` file-kind/size observation as specified. The exact no-open check must be made directly from one `lstat` result.

## Required remediation

Route the exact package to TASK BUILDER for one implementation batch that closes BF1–BF5 together and extends the selected singleton test module with every missing contract realization. The batch must preserve all existing immutable scientific identities, constructor logic, OCI launch contract, runtime pre-import negatives, source-class tags, and public-safety rules. After implementation and exact non-custody pinned-container verification, return through WORKFLOW COORDINATOR for one persistent-CRITIC review.

## Verification and scope

- Reviewed the complete integrated package against the governing tokenizer materialization specification and test contract.
- Confirmed the single operation remains unconsumed.
- Did not invoke the materializer, resolve custody, mount custody, access tokenizer/model bytes, or run the OCI materialization command.
- The host interpreter cannot import the pinned image's `jsonschema` dependency; that host-only result is not used as package evidence and does not replace the already reported pinned-container 19/19 result.
- No specification, implementation, test, constructor, executable identity, launch contract, STATE, provenance, ledger, scientific artifact, or custody record was modified.

## Diff self-inspection

ARCHITECT inspected the complete branch diff. The only ARCHITECT-authored changes are this consolidated BLOCK handoff and its canonical manifest. No package byte was modified.

## Holds

No custody lookup, tokenizer/model access, materialization, inference, qualification, Q2/EF3, diagnostics, scoring, protected seeds, science, STATE/provenance mutation, merge, publication, retry, fallback, or gate decision is authorized. The single materialization operation remains **UNCONSUMED**.

**Exact next recipient:** WORKFLOW COORDINATOR, then TASK BUILDER for one BF1–BF5 implementation batch; afterward WORKFLOW COORDINATOR routes the complete package to persistent CRITIC.
