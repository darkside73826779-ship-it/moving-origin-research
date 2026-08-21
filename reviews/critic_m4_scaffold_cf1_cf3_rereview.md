# CRITIC Rereview — M4 Scaffold Callable-State CF1–CF3

**Timestamp:** 2026-08-21 EDT

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Persistent independent CRITIC rereview of the M4 scaffold callable-state CF1–CF3 remediation, before Rebecca re-release or implementation.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-scaffold-rebecca-implementation-release` at `81bc7991b8c05672b84cc5b52a3a6a321fa047c2`.
- Prior authoritative review: `critic/m4-scaffold-callable-remediation-review` at `3f937c7a03e7ffcc10ac45a84609f5c80cb39a92`.
- ARCHITECT branch/head: `architect/m4-model-agnostic-scaffold` at `ade99fc13dc750b789d254316b9a7dc5de2eae8b`.
- Remediation result: `7f3db1f9552cf87de205b0635882402e0e1be5d4`, direct parent `de4c661a3d9c6caaa9be53d14bc6035b559aaa70`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_SCAFFOLD_CF1_CF3_REMEDIATION_2026-08-21.md`.
- Narrow six-file remediation delta plus named lifecycle schemas, fixtures, wrappers, sidecars, and preserved-closure evidence.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: CLEAR**
- **Combined disposition: CLEAR**

CF1–CF3 are closed. This CLEAR returns only to WORKFLOW COORDINATOR and then Rebecca. It does not release TASK BUILDER: the operative callable contract changed after the prior release and still requires Rebecca's explicit re-release of the exact cleared result.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** The remediation changes no quoted law. I confirmed the specification's P1–P3 and L7/L8/L9/L14/L18/L19 quotations remain byte-identical to `docs/ARCHITECTURAL_CONSTITUTION_v2.md`.
- **P3 CLEAR:** The new lifecycle state, result fields, tuple contract, fixture constants, and digests remain `[PROPOSED]`. No locked threshold, kill condition, scientific criterion, or source classification changed.
- **P4 CLEAR:** The amended spec, schema, fixture, and changelog retain 2026-08-21 and Regime B.
- **P5 CLEAR:** No deviation from law or locked bar is claimed; no waiver is required.
- **P6 CLEAR:** Entry 76 citations and their substance are unchanged. Previously verified Rulings 3 and 5 provenance remains accurate; this narrow state-contract delta introduces no new provenance claim.

## CF1–CF3 independent verification

- **CF1 closed:** `lifecycle_state_contract.states.closed` is a complete state-schema-valid terminal realization. Its RFC-8785/no-LF bytes reproduce the committed base64 and SHA-256 `a5a56b4a83e6e0c522d82bd416579d438a2dad31f4bc4c1e440f8c0345f2df08`. It retains the specified snapshotted fields, sets `lifecycle_state=CLOSED`, `closed=true`, and `frozen_payload_sha256=null`.
- **CF2 closed:** The operation-result schema requires exactly one of the paired callable form (`prior_state_sha256` plus `post_state_sha256`) or the legacy single `state_sha256` form. All six callable PASS artifacts validate, omit the legacy field, reproduce their canonical bytes/digests, and link exactly across `created → described → initialized → ready → stepped → snapshotted → closed`. The committed FAIL artifact validates with both hashes equal to the unchanged initialized-state digest and `result_state=FAILED`.
- **Legacy isolation verified:** The spec mandates the paired form and prohibits `state_sha256` for every v1.5 callable result. Independently reconstructing the six legacy lifecycle rows and seventeen legacy negative results from the base fixture produced 23 schema-valid artifacts with all stored digests unchanged. Thus regression evidence remains readable without making the legacy form callable authority.
- **CF3 closed:** `describe()` now has one signature only: `(manifest_bytes, operation_result_bytes)`. The tuple order is fixed. The manifest source is exactly `specs/data/m4_model_scaffold_executable_fixture_v1.json#/manifest_pair/candidate`; its canonical bytes reproduce the committed base64 and digest `536b15adc66e92c164a84b9c5473faca91473b53dbfd0caf393fc1ad87926ebd`. The second tuple member is the complete validated `describe` PASS artifact with digest `ef9f21b2285421d07b6c6ec69db1f2aed577738a329c24a23fcaaa8d48033633`.
- The operation-result schema and callable fixture both pass Draft 2020-12/meta-validation as applicable; their adjacent sidecars match. A full regression audit found all thirteen schemas metaschema-valid, all twenty-five callable wrappers byte/digest-correct, and all seventeen relevant JSON sidecars correct. `git diff --check` passed.

## Blocking findings

None.

## Non-blocking findings

None.

## Preserved evidence

- All valid evidence preserved in review `3f937c7a03e7ffcc10ac45a84609f5c80cb39a92` remains valid, including closures 1–6 and 8, schema/sidecar integrity, reset/snapshot, dependency and control constructors, varying inputs, hooks, atomic publication, CUDA-host custody, peer redaction, determinism, model neutrality, O-14/O-15/L18, and protected boundaries.
- No real model identity, checkpoint, download/training choice, backend authority, scientific threshold, scoring input, or protected seed was introduced.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify committed lineage and present this exact CLEAR package to Rebecca for her explicit re-release decision. TASK BUILDER remains held unless and until Rebecca re-releases the exact amended contract.

## Explicitly prohibited actions

No TASK BUILDER implementation/tests; model selection/download/checkpoint binding/training/integration; diagnostics or scoring; protected/courier seed access or exposure; L8 backend changes; rerun; state/provenance mutation; merge; or gate decision other than Rebecca's authorized re-release decision. CRITIC did not edit or co-author the specification, schemas, fixtures, task boundary, implementation, scoring artifacts, or `STATE.md`.

## Public-repository safety attestation

Before push, CRITIC scanned the complete review diff with gitleaks and manually checked for credentials, secrets, personal contact details/PII, machine identifiers, environment dumps, protected-seed material, persistent task/session IDs, and private absolute paths. No prohibited content was found. Repository SHAs, repository-relative paths, canonical digests, and synthetic fixture values were classified acceptable. `git diff --check` passed.

## Execution confirmation

No implementation, test/diagnostic/scoring execution, model activity, protected-seed access or exposure, rerun, L8 backend change, state/provenance mutation, or unauthorized merge occurred.
