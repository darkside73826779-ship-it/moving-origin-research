# CRITIC Partial Rereview — M4 Tokenizer RF2/RF3

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Narrow RF2/RF3 schema, fixture, sidecar, regression, law-fidelity, and public-safety rereview only

## Inputs reviewed

- Prior BLOCK: `critic/m4-tokenizer-tf1-tf4-rereview@2fea8e071ead56da2c6597727c2af9f01f831643`
- ARCHITECT head: `architect/m4-tokenizer-materialization-spec@fae97293f5f986b5d5bc4b16015819cbf6056341`
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_RF2_RF3_PARTIAL_REMEDIATION_2026-08-21.md`

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE PARTIAL: BLOCK**
- **Combined disposition: BLOCK**

RF2's type defect closes and can be banked. RF3's type predicate is corrected, but RF3/package closure cannot be banked because two committed sidecars do not match their Git blobs. RF1 remains independently BLOCKED.

## Law/source/provenance first

The delta changes no law quotation, locked threshold, bar, scoring predicate, negative label, or authority. New numeric-negative criteria remain `[PROPOSED]`; date and Regime B are present. No law deviation or false Entry citation was introduced. P1–P6 remain satisfied.

## Verified evidence

- `/tokenizer_config/sha256` now has `type: string` plus the 64-lowercase-hex pattern.
- `$defs.array.properties.sha256` now has `type: string` plus the same pattern.
- A complete otherwise-valid custody record with numeric `7` at `/tokenizer_config/sha256` is rejected.
- The complete synthetic PASS result with numeric `7` at `/arrays/0/sha256` is rejected.
- The test contract fixes both base identities, JSON Pointers, numeric replacement `7`, schemas, and `SCHEMA_INVALID` expectations.
- The private-custody schema Git blob matches its sidecar at `c0b18f83595c27758153d998c498b96a7029f3e7eb54907d83cd6858cdb0bb93`.
- Gitleaks found zero findings; the content delta is scope-clean.

## Blocking finding

### PF1 — Result-schema and test-contract sidecars hash worktree CRLF bytes, not committed Git blobs

Independent Git-blob hashing produced:

- `m4_tokenizer_materialization_result_schema_v1.json`: committed Git-blob SHA-256 `428575a832fe05238c1b652067a9fdf45c8daa963f788ab8fff4f8ef70c06366`; sidecar claims `06d9993bf77f52869da87f4064f4ff3745b826688b7ad9e832d5d2566718de95`.
- `m4_tokenizer_materialization_test_contract_v1.json`: committed Git-blob SHA-256 `f5596ef417624ad60d7a6434df75db9b848caff82607d78ae61abac7946ba100`; sidecar claims `c0677d6aa1bca270486c37c4cea7c982d92cda2411f3c461cd50fbf223b00afe`.

The claimed values match the Windows CRLF worktree materializations, not the repository artifacts. The handoff assertion that all three changed JSON sidecars match raw file bytes is therefore false for two pairs. Exact artifact custody and reproducibility fail.

**Classification:** construction/provenance defect. RF3's predicate correction is valid evidence, but complete RF3 artifact/fixture closure remains blocked until both sidecars are regenerated from committed LF Git-blob bytes (or exact repository-normalized bytes under an explicit contract) and verified.

## Preserved evidence

- RF2 is closed and banked.
- RF3's `type:string` predicate and numeric rejection are substantively correct, but its package is not cleared.
- RF1 remains BLOCKED pending repository-authoritative tokenizer-config digest/provenance or bounded derivation authority.
- TF3, TF4, Q2, EF3, custody, scoring, seed, model/tokenizer/OCI, and merge holds remain unchanged.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to return this BLOCK to persistent ARCHITECT for PF1 sidecar remediation while preserving RF2 closure and RF1's independent BLOCK. No combined CLEAR or materialization release is authorized.

## Public-safety and execution attestation

Gitleaks and manual review covered the exact delta and this review; zero prohibited findings. No tokenizer/model/OCI access, download, materialization, environment mutation, acquisition, qualification, diagnostics/scoring, protected seeds, Work Item A change, STATE/provenance mutation, rerun, merge, or gate decision occurred.
