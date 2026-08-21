# CRITIC Review — M4 Scaffold Callable Remediation

**Timestamp:** 2026-08-21 EDT

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Persistent independent CRITIC review of the M4 model-agnostic scaffold callable-contract and executable-input remediation after the durable TASK BUILDER specification block, before any renewed Rebecca release or implementation.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-scaffold-rebecca-implementation-release` at `81bc7991b8c05672b84cc5b52a3a6a321fa047c2`.
- Durable TASK BUILDER BLOCK: `taskbuilder/m4-model-agnostic-scaffold` at `cb43b7a94ef8ea54d6e689398f68cec793707005`; `handoffs/TASKBUILDER_TO_COORDINATOR_M4_MODEL_SCAFFOLD_SPECIFICATION_BLOCK_2026-08-21.md`.
- ARCHITECT branch/head: `architect/m4-model-agnostic-scaffold` at `de4c661a3d9c6caaa9be53d14bc6035b559aaa70`.
- Specification result: `c33a5e0c94610b47dda783b18af06ca0472edd69`; reviewed through routing commits `44667f651147a5c28a107cc4a00a479267b3197f` and `de4c661a3d9c6caaa9be53d14bc6035b559aaa70`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_MODEL_SCAFFOLD_CALLABLE_REMEDIATION_2026-08-21.md`.
- Primary spec, changelog, task boundary, callable/base/supplemental fixtures, all named schemas, and adjacent sidecars at the routing head.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

The amendment closes most of the durable TASK BUILDER gaps, but the callable lifecycle remains non-executable without implementer invention. The package returns through WORKFLOW COORDINATOR to ARCHITECT. The operative contract change requires a new persistent-CRITIC CLEAR and Rebecca's explicit re-release of the exact corrected result before TASK BUILDER may resume; authority `81bc7991b8c05672b84cc5b52a3a6a321fa047c2` does not release this amended contract.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** I independently byte-compared every quoted P1–P3 and L7/L8/L9/L14/L18/L19 passage in the specification against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`. The quotations are verbatim and their cited line locations contain the quoted text; no constitutional reconstruction was used.
- **P3 CLEAR:** I audited the amendment's numeric criteria and source tags. Interface dimensions, fixture constants, arithmetic rules, and scaffold acceptance conditions are explicitly `[PROPOSED]`; L7 peer parity is sourced to `[BAR-Entry 11]` and `[OP-Entry 76]`; the L8 specificity operationalization is `[OP-Entry 76]`; constitutional requirements carry `[LAW-Lx]`. No changed locked threshold or untagged gating threshold was found.
- **P4 CLEAR:** The spec, fixtures, and schemas identify 2026-08-21 and Regime B.
- **P5 CLEAR:** The amendment claims no deviation from constitutional text or locked bar and therefore requires no waiver.
- **P6 CLEAR:** I checked the Entry 76 Rulings 3 and 5 citations against `docs/rulings/provenance_log.md` Entry 76. The standardized proximal-component specificity approach and the candidate/peer calibration/evaluation/ECE/binning/paired-training conditions are accurately attributed. No provenance citation was altered into a stronger authority claim.

## Independent executable-input verification

- All thirteen model-scaffold Draft 2020-12 schemas validate against the Draft 2020-12 metaschema.
- All seventeen `artifact` wrappers in `specs/data/m4_model_callable_fixture_v1.json` independently reproduce their RFC-8785/no-LF SHA-256 and canonical base64 bytes.
- All seventeen relevant adjacent JSON sidecars independently match their files, and the callable fixture's bound raw digest for `m4_model_scaffold_executable_fixture_v1.json` matches the actual base file.
- Reset and snapshot requests are complete, schema-valid, canonically encoded, digest-bound inputs with fixed single-mutation failures.
- The dependency manifest and remaining control manifest/request constructors are repository-relative, ordered, and digest-fixed. The varying-request row establishes behavior outside a lookup table. The two hook payload/output/receipt domains and atomic-publication request/result/layout/recovery artifacts are concretely fixed.
- These checks preserve the valid portions of closures 1–6 and 8. They do not cure the lifecycle defects below.

## Blocking findings

### CF1 — Construction bug: the required close state has no normative state object or digest

Section 2 requires `close() -> operation_result_bytes`. Section 10 says close sets the callable state closed, requires `frozen_payload_sha256` to be null after close, and declares the fixture's exact pre/post objects normative. Yet `lifecycle_state_contract.states` contains only `created`, `described`, `initialized`, `ready`, `stepped`, and `snapshotted`. It contains no complete `CLOSED` object and no canonical digest for it.

The state schema permits `lifecycle_state="CLOSED"` and `closed=true`, but a schema is not a realization. TASK BUILDER must choose the remaining field values and generate previously unspecified canonical bytes and a digest. That directly violates the executable-input rule and leaves closure 7 open.

### CF2 — Spec defect: operation-result construction cannot express the mandated pre/post hashes

Section 10 requires the implementer to construct each operation result "with the pre/post hashes." The normative `m4_model_adapter_operation_result_schema_v1.json` has only one digest field, `state_sha256`, plus symbolic `prior_state` and `result_state`; it has no pre-state digest and post-state digest fields. The callable fixture also supplies no complete operation-result artifacts, per-transition constructor, canonical bytes, or expected operation-result digests.

It is therefore undefined whether `state_sha256` means the pre-state hash, the post-state hash, or some other digest, and it is impossible for a schema-valid result to carry both hashes as written. The prior stored lifecycle rows are expressly excluded as a callable algorithm. TASK BUILDER must invent the representation and expected bytes, so the lifecycle contract is not executable end to end.

### CF3 — Spec defect: `describe()` has mutually incompatible return contracts

Section 2 specifies `describe() -> canonical manifest bytes`. Section 5 states, without an exception, that every lifecycle method returns `m4_model_adapter_operation_result_schema_v1.json`. No tuple, wrapper, or alternate signature reconciles those requirements, and the fixture supplies no exact `describe` return artifact resolving them. An implementation cannot satisfy both literal contracts. This must be resolved and bound to exact canonical output before release.

## Non-blocking findings

None. The three findings above are independently sufficient to block the package.

## Preserved evidence

- Prior persistent-CRITIC law-fidelity, BF1/BF4/RF2/RF3/RF1A, schema, CUDA-host custody, peer-redaction, deterministic-run, model-neutrality, O-14/O-15/L18, protected-boundary, and publication evidence remains valid except where a complete callable lifecycle result depends on CF1–CF3.
- The reset request, snapshot request, generic dependency manifest, remaining-control constructors, varying-input arithmetic contract, positive hook payloads/receipts, and atomic-publication artifacts materially close their corresponding TASK BUILDER gaps.
- No real model identity, checkpoint, download, training choice, final `gofast` identity, scientific threshold change, or protected scoring input was introduced.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify this review's lineage and route the BLOCK to the persistent ARCHITECT for narrow deterministic remediation of CF1–CF3. After remediation, the package must return through Coordinator to persistent CRITIC. Even a later CLEAR routes to Rebecca for explicit re-release; TASK BUILDER is not released directly by this review.

## Explicitly prohibited actions

No TASK BUILDER implementation or tests; model selection/download/checkpoint binding/training/integration; compatibility, diagnostic, or scoring execution; protected/courier seed access or exposure; native-CUDA or serial L8 work; science/threshold change; retry or rerun; state/provenance mutation; merge; or gate decision. CRITIC did not edit or co-author the specification, schemas, fixtures, task boundary, implementation, scoring artifacts, or `STATE.md`.

## Public-repository safety attestation

Before push, CRITIC scanned the complete review diff with gitleaks and manually checked it for credentials, private keys, API tokens, passwords, personal contact details/PII, machine identifiers, environment dumps, protected-seed material, persistent task/session IDs, and private absolute paths. No prohibited content was found. Repository SHAs, repository-relative paths, canonical digests, and synthetic fixture values were classified acceptable. `git diff --check` passed.

## Execution confirmation

No implementation, test, model activity, compatibility/diagnostic/scoring execution, protected-seed access or exposure, rerun, CUDA-L8/serial-L8 execution, fallback, state/provenance mutation, or unauthorized merge occurred.
