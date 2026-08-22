# M4 Post-Tokenizer R-CC1–R-CC6 Remediation v1

Date: 2026-08-21
Regime: B
Status: design-only; no execution authority
Input: `9ea956a355aa4524c527ccf09ca1b2882e89c40b`
Authoritative review: `54c0a0d3fe156df9a31bd7a6b1d6f25e008e501d`
Test-bed evidence authority: `coordinator/m4-wsl2-preexecution-testbed @ 11ea682a7f0fadfa1437a12d882402d90ffd0579`, tag `m4-wsl2-preexecution-testbed-v1.2`

This document closes only R-CC1–R-CC6. The v1.2 test-bed package is corroborating synthetic/local diagnostic authority; it is not scoring, qualification, custody authority, kernel-overlap proof, or model selection.

## R-CC1 — complete backend receipt failures

The exact residual matrix is adjacent JSON. Factory and adapter prevalidation failures have backend-call delta zero. Receipt-derived failures have backend-call delta one and no public-state commit:

- delete `status` from a PASS receipt → `BACKEND_RECEIPT_INVALID`;
- replace `session_id` with a different registered session → `BACKEND_SESSION_MISMATCH`;
- replace `prior_backend_state_sha256` with a nonmatching digest → `BACKEND_STATE_MISMATCH`;
- registered receipt `{status: FAIL, backend_code: SYNTHETIC_REJECTED}` → `BACKEND_DECLARED_FAILURE` with sanitized backend code preserved;
- raised backend exception → `BACKEND_EXCEPTION`;
- valid receipt with wrong request/episode/ordinal correlation → `RESPONSE_CORRELATION_FAILURE`.

Each binds exact request/prior-token/receipt mutation, call delta one, first-failure code, and identical before/after durable-state bytes and digest. A malformed FAIL receipt without a registered backend code is `BACKEND_RECEIPT_INVALID`, not declared failure.

## R-CC2 — full lifecycle realizations and caller identity

The adjacent lifecycle artifact contains all 42 state-category × operation cells. Legal cells name the next state; every invalid cell names its exact code, call delta zero, and byte-identical state requirement. It includes repeated describe, initialize, and close; every operation after CLOSED; reset before completion; episode-id reuse/mismatch; request/reset/snapshot ordinal faults; and lifecycle-invalid snapshots.

Initialize, both resets, snapshot, all three close requests, their backend receipts/tokens, and three CLOSED states are canonical RFC-8785 objects with reproduced SHA-256 values. Each close path uses an independent adapter and session; its CLOSED trace includes the exact pre-state, request, session-specific backend receipt, post-state, and one close call. `m4_post_tokenizer_r_cc1_r_cc6_operation_cases_v1.json` supplies the three exact session-specific receipts and supersedes only the generic receipt-template references in the lifecycle artifact. Subsequent close and every other CLOSED operation are zero-call lifecycle failures.

`CallerIdentity` is exactly the RFC-8785 object `{adapter_instance_id,caller_session_id,caller_thread_id}`. The lock stores its SHA-256 plus `operation_id`. If the active identity digest equals the incoming identity digest, disposition is `ADAPTER_REENTRANCY_FORBIDDEN`; if it differs, disposition is `ADAPTER_OPERATION_IN_FLIGHT`. Comparison occurs before request parsing or backend invocation, so both outcomes are deterministic, zero-call, and byte-identical.

## R-CC3 — call-delta split and complete paired identity

Negatives are partitioned:

- `PRE_CALL_SUPPRESSION`: backend delta 0, no commit;
- `SINGLE_BACKEND_OBSERVED`: backend delta 1, no commit (`BACKEND_*` receipt/exception/correlation cases);
- `FANOUT_POST_CALL_ATOMIC`: exact per-adapter deltas stated in R-CC4, no commit.

The replacement candidate/peer manifests bind equality for checkpoint SHA-256, ordered weight hashes, training instance, tokenizer, architecture, parameter count, quantization, decoding, calibration, evaluation data, and binning. They bind differences for role, scientific arm, runtime instance, access policy, channel policy, and redaction receipt. A one-field mutation exists for every equality field (`PAIR_IDENTITY_MISMATCH`) and every required-difference field (`PAIR_ISOLATION_FIELD_NOT_DISTINCT`).

## R-CC4 — two-phase fanout and complete reconciliation matrix

Phase 1 validates the sanitized pair, rederives prompt and stop views, validates candidate and peer received hashes, checks immutability and context/request association, and snapshots both adapter states. No backend may run until all Phase-1 checks pass. Thus all six base reconciliation faults—missing context, duplicate context, reordered contexts, wrong length, wrong prompt digest, wrong sanitized stop digest—plus received divergence, mutation, association, and rederived-stop mismatch suppress both calls.

Phase 2 invokes candidate, then peer, without committing either public result. Candidate failure yields candidate delta 1, peer delta 0, the exact candidate failure code, and no commit. Candidate success followed by peer failure yields candidate delta 1, peer delta 1, terminal `FANOUT_ATOMICITY_FAILURE`, nested sanitized peer failure code, and restoration of both Phase-1 snapshots. Only two valid correlated receipts commit atomically. There is no scenario in which a “peer pre-call hash failure” follows candidate execution.

## R-CC5 — governing law version and L8 HELD projection

The active law artifact now binds `docs/ARCHITECTURAL_CONSTITUTION_v2.md` exactly: L7 line 26, L8 line 28, L10 line 32, L14 line 42, and L18 line 54. `L8_PREREQUISITE_HELD` is removed from FAIL codes. The L8 current projection is exactly `status=HELD`, `claim_made=false`, empty evidence and metrics, `failure_code=null`, `held_reason=L8_PREREQUISITE_UNCLEARED`. All other honest no-claim and scientific holds remain.

## R-CC6 — result-carrying overlay and seam LF bindings

The active frozen overlay is now 38 paths and adds the governed tokenizer result plus adjacent sidecar. Construction stops `CLEARED_TOKENIZER_RESULT_REQUIRED` unless `TOKENIZER_SHA` contains a persistent-CRITIC-cleared canonical PASS pair whose sidecar, schema, sanitized-only fields, ordered 1024/4096/8192 rows, and stop digest verify. A FAIL, BLOCKED, empty, partial, mismatched, or unreviewed pair is never an integration input.

The exact appended attributes block is now 43 rules: the prior 37, two result-pair rules, and four future seam rules for `src/__init__.py`, `src/m4_post_tokenizer_integration.py`, `src/test_m4_post_tokenizer_integration.py`, and `tests/run_m4_post_tokenizer_integration_tests.py`. Their raw identities remain publication prerequisites; LF checkout behavior is no longer platform-dependent. The rebinding cascade explicitly includes the result pair before the combined inventory.

## Holds

No implementation, OCI/materializer execution, custody/model/tokenizer access, scoring, seeds, science, qualification, durable-state mutation, publication, merge, or gate decision occurred. Q2, EF3, native L8, real-backend selection, and the active token-ID remediation remain separate.
