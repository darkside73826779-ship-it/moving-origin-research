# CRITIC M4 Post-Tokenizer RR-CC1–RR-CC3 Final Rereview

Date: 2026-08-21 EDT  
Regime: B  
Role: authoritative persistent CRITIC  
Terminal state: **COMBINED BLOCK**

## Immutable intake and validation

- Substantive/routing head: `architect/m4-post-tokenizer-rr-cc1-rr-cc3-reconciliation @ 73c8394994aa172727ffff93dc42ade4348d4823`
- Review result: `d643b65852dbc5e32e7f11ce0e0cb15c8561ed0d`
- Base: `94c9a833fdaf872584ea863391c21927bdb704d2`
- Canonical manifest head: `3d035ed935e844a682d57f05399672a6d040c2f6`
- Prior authoritative BLOCK: `critic/m4-post-tokenizer-r-cc1-r-cc6-rereview @ ba19982f7b165821d4c207ea05d047212feb7950`
- Helper-managed checkout receipt SHA-256: `b3e533c151a135a98cb8211a2f8bffdc7a6895a26fad7fb0e7f039fa43fce73f`

The canonical handoff manifest validates with the repository workflow contract validator. All ten declared raw Git-blob identities reproduce exactly. The substantive delta is exactly the nine declared design/routing paths. All three JSON sidecars bind their raw bytes and all 42 embedded canonical-object SHA-256 values reproduce.

## Banked closure

RR-CC1's receipt realizations are now self-contained for the six negative rows. The five operation families bind canonical requests, prior tokens, and PASS receipts. Mechanical comparison proves the exact result deltas:

- delete only `status`;
- replace only `session_id`;
- replace only `prior_backend_state_sha256`;
- registered FAIL changes exactly `status: PASS→FAIL` and `backend_code: null→SYNTHETIC_REJECTED`;
- missing-code derives from that exact registered-FAIL receipt by deleting only `backend_code`;
- response-correlation changes only `request_ordinal: 0→99`.

Every row binds one observed backend call and equal before/after durable-state identities. The registered code set is exact.

RR-CC2 now supplies an explicit active-artifact replacement order. It correctly supersedes the obsolete universal zero-call rule for receipt/exception/correlation cases, gives pre-call cases delta zero and observed cases delta one, replaces label-only lifecycle bindings, replaces the old reset-B zero-call trace, and prevents older universal/label bindings from overriding the active artifacts.

RR-CC3 contains 42 unique state-category × operation cells over the exact seven categories and six operations. Every cell's pre/request/post references resolve to the declared canonical objects and exact digests. Every invalid zero-call cell is byte-identical before/after. The canonical INITIALIZED state, four CLOSED variants, state-specific close requests, three close traces, and reset call rows are present. Banked R-CC4 fanout, R-CC5 law, R-CC6 overlay/rebinding, pair/caller identities, holds, and public-safety evidence remain byte-unchanged.

## Residual RR-F1 — Peer reset rows bind candidate-session receipts

The precedence map correctly requires each adapter to make one reset call and validate one receipt for reset A and reset B, but the exact reset realizations do not preserve session isolation:

- candidate and peer `reset_a` both reference `rr_cc1.operation_families.pass_receipts.reset`; that canonical receipt has `session_id="candidate-session-v1"`;
- candidate and peer `reset_b` both reference `lifecycle_v1.canonical_objects.reset_b_receipt`; that canonical receipt also has `session_id="candidate-session-v1"`.

The banked paired manifest binds the peer runtime/session identity as `peer-session-v1`, and the active backend contract requires one distinct session and maps a receipt-session mismatch to `BACKEND_SESSION_MISMATCH`. A peer adapter therefore cannot validate either referenced receipt as its own successful reset receipt. The handoff claim that each candidate/peer reset validates one exact receipt is false for both peer rows.

Bind separate canonical candidate and peer reset-A/reset-B receipts (or a role-parameterized construction with exact resulting objects/digests), with `candidate-session-v1` and `peer-session-v1` respectively. Update the four reset realization references and affected sidecars/manifest. Preserve the now-correct one-call totals and all banked evidence.

## Law fidelity, public safety, and disposition

This is a narrow executable-design identity defect. It authorizes no implementation, backend selection, OCI/materializer execution, custody/model/tokenizer access, scoring, seeds, science, Q2/EF3/native-L8 work, durable-state mutation, publication, merge, or gate decision. The separate tokenizer execution release was not accessed or inferred.

Public-safety review found no credentials, personal contact data, private paths, custody values, model/tokenizer bytes, token arrays, seeds, scores, or scientific output. Preflight findings F000001–F000231 are fixed-regex duplicate-domain matches wholly inside required immutable public object/artifact/sidecar/commit digests; all 231 are non-contact reproducibility metadata, manually classified here, and none is silently suppressed. Gitleaks findings are zero.

**COMBINED BLOCK.** Return through WORKFLOW COORDINATOR for one exact RR-F1 peer-reset receipt identity correction. Preserve all banked RR-CC1 receipt mutation closure, RR-CC2 precedence/call-count closure, RR-CC3 cell/reference closure, and R-CC4–R-CC6 evidence.
