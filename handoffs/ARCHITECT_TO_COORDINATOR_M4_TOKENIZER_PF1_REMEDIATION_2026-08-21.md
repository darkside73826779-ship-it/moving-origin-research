# FORMAL HANDOFF — ARCHITECT → WORKFLOW COORDINATOR

**Timestamp:** 2026-08-21 EDT
**Regime:** B
**Work item/gate:** Work Item B PF1 only — Git-blob sidecar custody repair

## Inputs

- Prior ARCHITECT result: `architect/m4-tokenizer-materialization-spec@fae97293f5f986b5d5bc4b16015819cbf6056341`.
- Persistent CRITIC partial BLOCK: `critic/m4-tokenizer-rf2-rf3-partial-rereview@5a32742d6bfa4f0a1dca5d87d59ff1d9f90c39c7`.
- Review: `reviews/critic_m4_tokenizer_rf2_rf3_partial_rereview.md`.

## Exact remediation

- Replaced `m4_tokenizer_materialization_result_schema_v1.json.sha256` with the SHA-256 of the committed LF Git-blob bytes: `428575a832fe05238c1b652067a9fdf45c8daa963f788ab8fff4f8ef70c06366`.
- Replaced `m4_tokenizer_materialization_test_contract_v1.json.sha256` with the SHA-256 of the committed LF Git-blob bytes: `f5596ef417624ad60d7a6434df75db9b848caff82607d78ae61abac7946ba100`.
- Schemas, fixtures, test contract, specification, and RF2/RF3 predicates are unchanged.

## Status

- PF1 remediated and ready for persistent-CRITIC narrow rereview.
- RF2 remains closed and banked.
- RF3 correctness is preserved; package closure awaits PF1 rereview.
- RF1 remains independently BLOCKED pending repository-authoritative tokenizer-config digest/provenance or bounded derivation authority.

## Verification

- All affected sidecars were checked against committed/staged Git-blob bytes, not Windows worktree bytes.
- Complete diff inspected; only the two named sidecars and this handoff were introduced.
- `git diff --check` passed.

## Public-safety scan

Pre-push gitleaks plus targeted changed-file review covered the complete commit delta; zero prohibited credentials, secrets, PII, private paths, machine identifiers, environment dumps, protected seeds, task IDs, or tokenizer/model/OCI bytes were found. Public repository identities and cryptographic digests are acceptable reproducibility metadata.

## Next owner/event

WORKFLOW COORDINATOR, to acknowledge receipt and route the exact commit to persistent CRITIC for PF1-only rereview. No combined CLEAR or materialization release is implied.

## Holds

No RF1 edit; tokenizer/model/OCI access or download; materialization; Q2/EF3 change; execution; scoring; protected-seed access; state/provenance mutation; merge; or gate decision.
