# M4 Post-Tokenizer RR-CC1–RR-CC3 Design Reconciliation v1

**Date:** 2026-08-21 EDT  
**Regime:** B  
**Status:** DESIGN ONLY `[PROPOSED]`

## Scope and precedence

This reconciliation closes only RR-CC1 through RR-CC3 from the persistent-CRITIC rereview at `ba19982f7b165821d4c207ea05d047212feb7950`. It preserves the banked R-CC4 two-phase fanout closure, R-CC5 constitutional law semantics, R-CC6 overlay/rebinding closure, paired-manifest evidence, caller identity, and every unaffected byte at input `94c9a833fdaf872584ea863391c21927bdb704d2`.

The exact active replacement order is `specs/data/m4_post_tokenizer_rr_cc2_precedence_map_v1.json`. Where an older fixture or trace conflicts with an RR artifact, the named RR artifact controls. No unnamed historical or provenance artifact is rewritten.

## RR-CC1 — executable receipt realizations

`specs/data/m4_post_tokenizer_rr_cc1_receipt_realizations_v1.json` binds canonical request, prior backend-state token, and PASS receipt objects for initialize, reset, snapshot, step, and close operation families. Each object digest is SHA-256 over its RFC 8785-subset canonical UTF-8 bytes without a terminal LF. The registered FAIL code set is exactly `SYNTHETIC_REJECTED`.

Every receipt-derived negative binds its base receipt reference, exact resulting receipt object and digest, request and prior-token references, observed call delta, first failure, and before/after durable-state identities. `registered_fail` changes both `status` to `FAIL` and `backend_code` to `SYNTHETIC_REJECTED`. `fail_without_registered_code` derives from that exact registered-FAIL receipt by removing only `backend_code`. All receipt-derived rows observe exactly one backend call and make no durable commit.

## RR-CC2 — one active call-count model

The precedence map explicitly replaces the older universal `backend_call_delta=0` for all backend rows. Pre-call suppression remains delta zero; receipt validation, registered backend FAIL, backend exception, and response-correlation failure are delta one. It also replaces the older `reset_b` zero-call trace: candidate and peer each make exactly one backend reset call and validate exactly one role-specific reset receipt for both reset A and reset B. Candidate receipts bind `candidate-session-v1`; peer receipts bind `peer-session-v1`. Close paths use their exact receipts rather than the earlier generic template.

## RR-CC3 — 42 canonical lifecycle cells

`specs/data/m4_post_tokenizer_rr_cc3_lifecycle_realizations_v1.json` contains exactly 42 state-category × operation cells in deterministic state-major and operation-major order. Every cell binds a canonical pre-state reference/digest, canonical request reference/digest, exact expected result, backend-call delta, and canonical post-state reference/digest. Invalid cells are mechanically byte-identical because their pre/post references and digests are equal. The artifact includes an exact canonical INITIALIZED pre-state.

Legal close cells and the three independently named close traces bind exact INITIALIZED, EPISODE_READY, and STEPPED_COMPLETE pre-states, state-specific close requests, operation-case receipt references, and exact CLOSED post-state identities. STEPPED_INCOMPLETE close is likewise fully bound in its matrix cell. Reset A and reset B bind exact per-adapter call counts, request references, role-specific receipt objects/digests, and distinct candidate/peer session identities.

## Boundaries

This package defines executable design objects only. It authorizes no implementation, OCI/materializer execution, custody/model/tokenizer access, scoring, seeds, science, Q2/EF3/native-L8 decision, STATE/provenance mutation, publication, merge, or gate decision.
