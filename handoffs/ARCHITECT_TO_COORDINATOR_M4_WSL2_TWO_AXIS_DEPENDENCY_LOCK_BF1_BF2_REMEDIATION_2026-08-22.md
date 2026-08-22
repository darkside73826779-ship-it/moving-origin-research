# FORMAL HANDOFF — ARCHITECT → WORKFLOW COORDINATOR — M4 WSL2 two-axis/dependency-lock BF1–BF2 remediation

Date: 2026-08-22 EDT

Status: COMPLETE — DIAGNOSTIC INFRASTRUCTURE ONLY — NO MODEL RERUN

## Result

BF1 and BF2 are remediated as one fail-closed package. The derivation now validates every source against the exact v1 schema, binds the exact nineteen-code v1 vocabulary, treats all eighteen non-replica codes as structural failures, rejects unknown codes, and maps metric-derived structural failures only to exact v1 names.

The v2 schema now enforces status/failure/count/list conditionals and exact vocabularies. The committed semantic validator additionally enforces count arithmetic, canonical unique ordered in-range mismatch ordinals, ordinal digest equality, structural-status consistency, and exact source binding. The single exact-replica consumer guard returns `REPLICA_CONSISTENCY_STOP` for `MISMATCH` and `NOT_RUN`, and permits only `MATCH` when exact replicas are required.

## Preservation

- Retained v1 report: exactly 123,507 bytes, SHA-256 `7dde0d1587b9205a339776ad04daecfe2bf160e8ecb9ff0504335f91b57a10bc`, unchanged `BLOCKED / OUTPUT_DIGEST_MISMATCH`.
- Retained v2 projection: exactly 1,019 bytes, SHA-256 `d071f44c5a18a40b75aee17700028417c9275c8146f6b1eee0e65159404ca185`, unchanged structural `PASS` / replica `MISMATCH` with 164 compared, 80 agreements, and 84 mismatches.
- Dependency exclusion, setup, runtime verifier, requirements, v1 schema/producer, and all untouched package evidence remain byte-identical.
- No model rerun, network acquisition, scoring, science, qualification, readiness claim, protected input, or custody access occurred.

## Immutable identities

- Authoritative CRITIC review: `critic/m4-wsl2-two-axis-dependency-lock-review @ 31dd464ad1bcdfcef713b4636b4df653782dc1c8`.
- Substantive remediation result: `4993711fa32ffe9ab3b2dabb2b5d5615182c6e90`.
- Updated complete eighteen-entry package inventory: `specs/data/m4_wsl2_two_axis_dependency_lock_package_v1.json`, raw SHA-256 `1955da3ddb823ae83efc2dbc096880544c7c8d88be8ffbefbfdf395c59916839`.

## Verification

- Pinned governed OCI image, network disabled, read-only repository, isolated unittest discovery: 34/34 PASS.
- Draft 2020-12 v2 metaschema: PASS.
- Exact retained report and projection byte/digest reproduction: PASS.
- All eighteen package path/mode/blob/byte/raw-SHA-256 entries and adjacent sidecars: PASS.
- Python compilation, diff check, LF/mode inspection, and no-rerun boundary: PASS.

Next event: WORKFLOW COORDINATOR validates the canonical manifest and routes this exact package once to persistent CRITIC for narrow BF1–BF2 rereview. No model execution, scoring, science, readiness, merge, or gate authority is inferred.
