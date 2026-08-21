# FORMAL HANDOFF — ARCHITECT → WORKFLOW COORDINATOR — WORK ITEM A ONLY

**Date:** 2026-08-21

**Regime:** B

## Gate served

Deterministic closure of the M4 scaffold first-callable-step response/state digest contradictions before implementation resumes.

## Input SHAs reviewed

- Rebecca re-release authority: `coordinator/m4-scaffold-rerelease-tokenizer-custody@45d40d8b688fb7f44098d235df7f31cca1aa3b31`
- Cleared ARCHITECT lineage/result: `ade99fc13dc750b789d254316b9a7dc5de2eae8b` / `7f3db1f9552cf87de205b0635882402e0e1be5d4`
- Persistent-CRITIC CLEAR: `deb49bb342a39d3ec25834a4a59b5b21a697d966`
- TASK BUILDER durable block: `taskbuilder/m4-scaffold-rerelease@2c3312b13c5e968519f6a9d9e9bf0afaf84f8f0d`

## Files changed/created

- Amended `specs/m4_model_agnostic_scaffold_spec_v1.md` with §8.2.
- Added `specs/data/m4_callable_step_digest_amendment_v1.json` and sidecar.
- Added exact reproducibility builder `specs/tools/build_m4_callable_step_amendment_v1.mjs`.
- Added companion `specs/m4_callable_step_digest_changelog.md`.

## Branch/result SHA

- Branch: `architect/m4-scaffold-callable-step-remediation`
- Specification result: `e1bdf5126dbea51256c089ecc43c79d5b6404a1f`

## Verdict/status

`READY_FOR_PERSISTENT_CRITIC_REVIEW`; implementation remains held pending CLEAR and Rebecca re-release.

The overlay fixes exactly the four contradictions: callable request/response episode identity, callable pre-state binding, actual varying-response digest in post-state, and the response/post-state cycle. Response `state_after_sha256` now hashes the constructed post-state projection with exactly `/last_response_sha256` deleted. The complete response is then hashed and inserted into the complete post-state; the operation result hashes the complete post-state. No placeholder or fixed-point operation exists.

Nine complete canonical wrappers cover the varying response, post-state projection, stepped state/result, snapshot request/state/result, and close state/result. The overlay's exact precedence list preserves the verified describe/initialize/reset prefix and every unlisted fixture.

## Blockers and non-blocking findings

- This is an operative callable-contract change. Rebecca must explicitly re-release the exact amendment after persistent-CRITIC CLEAR.
- Work Item B was not modified. Q2/EF3 and all model/tokenizer holds are unaffected.

## Verification/public-safety attestation

- All nine wrappers independently reproduce their RFC-8785 SHA-256 and base64 bytes.
- Response, state, operation-result, and snapshot-request artifacts validate against their committed schemas.
- All five non-cycle invariants are true; overlay sidecar matches; `git diff --check` passed.
- Complete delta scanned for secrets/credentials, PII/contact details, private paths, host/user/machine identifiers, environment dumps, protected seeds, model/tokenizer bytes/caches/adapters, and Git LFS pointers. Zero prohibited findings.

## Exact next recipient role

WORKFLOW COORDINATOR verifies lineage and routes this exact result to the established persistent CRITIC. After review, Coordinator stops for Rebecca because explicit re-release is required.

## Explicitly prohibited actions

No surrogate-role review; implementation or tests/diagnostics execution; model/tokenizer access; scoring; protected seeds; L8 change; Work Item B change; state/provenance mutation; merge; or gate decision.
