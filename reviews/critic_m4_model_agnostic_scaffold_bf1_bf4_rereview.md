# CRITIC Rereview — M4 Model-Agnostic Scaffold BF1–BF4 Remediation

**Timestamp:** 2026-08-21 06:56 EDT

**Regime:** B

**Gate served:** Persistent independent CRITIC rereview of deterministic BF1–BF4 remediation before Rebecca approval or implementation.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-cuda-ready-cpu-l8-directive` at `a4d8dc054d3944d3a0efbafeea955b3570f0a272`.
- Prior authoritative review: `critic/m4-model-agnostic-scaffold-v1-review` at `528810f403350fd2023c32f83992064e16226cc1`.
- ARCHITECT branch/head: `architect/m4-model-agnostic-scaffold` at `a5716c18a54f3ef1d47778c158ae63d220c8f76d`.
- Remediation result/parent: `697e0343457cd1d0619a34053574b63385204c35`, parent `7afa624093e6cc69c7a5e9f1a4d8dff13f2b729d`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_SCAFFOLD_BF1_BF4_REMEDIATION_2026-08-21.md`.
- Primary spec and executable fixture: `specs/m4_model_agnostic_scaffold_spec_v1.md` and `specs/data/m4_model_scaffold_executable_fixture_v1.json`.
- Full remediation delta, all six Draft 2020-12 schemas, task boundary, sidecars, constitution §5 and quoted laws, provenance Entries 11/76, and preserved Phase A authority.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

BF1 and BF4 are closed. The main BF2/BF3 construction is substantially improved, but the contract still requires executions for which no concrete fixture realization exists: CUDA-host orchestration, a second frozen request, and the two-run repeatability comparison. The peer redaction receipt also lacks a deterministic digest projection. TASK BUILDER would have to invent these inputs and expected bytes.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** The P1–P3 and L7/L8/L9/L14/L18/L19 quotations remain verbatim against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; no law text changed in the remediation.
- **P3 CLEAR:** The confidence-domain constraint is corrected to `[PROPOSED]`. Entry 11 continues to source matched-peer bars; Entry 76 separately sources Ruling 5 parity and Ruling 3 specificity. Numeric scaffold sizes and acceptance mechanics remain `[PROPOSED]`.
- **P4 CLEAR:** Amended normative Markdown and JSON artifacts state 2026-08-21 and Regime B.
- **P5 CLEAR:** No law/bar deviation or waiver is claimed.
- **P6 CLEAR:** Entry 11 and Entry 76 Rulings 3/5 were checked against their committed text. The amended prose and parity fields now preserve their distinct provenance.

## Independent verification and BF1–BF4 reconciliation

- **BF1 CLOSED:** All six schemas pass `Draft202012Validator.check_schema`. Both complete requests validate, top-level `$defs` resolves, and `ground_truth`, `perturbation`, and `semantic_probe` occupy valid required/property locations.
- **BF2 PARTIAL / BLOCK:** Both manifests and requests, all nine constructed responses, all six operation results, and the checkpoint validate against their schemas. I independently reconstructed RFC-8785 bytes and matched every committed manifest/request/response/operation/checkpoint/failure digest and the published candidate JSON+LF digest. However, required CUDA, frozen-second-request, and fresh-process realizations remain absent; see RF1–RF2.
- **BF3 PARTIAL / BLOCK:** The repaired validation-stage order makes the typed peer-private, peer-confidence, retrieval, hook, dimension, digest, model, scoring, and checkpoint mutations structurally reachable. The nonfinite bit-pattern boundary is now pre-serialization and all 17 failure-result digests reconstruct. The CUDA and repeatability rows still lack the correct executable bases; see RF1–RF2.
- **BF4 CLOSED:** Candidate and peer manifests validate. Their equality fields now bind architecture, parameter count, initialization, data, schedule, calibration, confidence calibration, evaluation data, ECE definition, binning, paired-training contract, dimensions, and dtypes. Only role, scientific arm, and non-null training-instance identity differ, exactly as declared.

## Blocking findings

### RF1 — required CUDA-host scaffold and custody failure have no CUDA realization

**Classification:** specification/executability defect; residual BF2/BF3.

Spec §9 requires the scaffold to run under both `CPU_STUB` and `CUDA_STUB_HOST_ORCHESTRATION`. The sole candidate manifest, peer manifest, response constructor, dependency manifest, and every positive response are `CPU_STUB`; `cuda_host_orchestration` is false and no CUDA manifest/request/internal response/custody record or canonical expected digest is committed.

The `cuda_custody` negative names a “constructed candidate response internal object” but that only construct is CPU-backed. Its single mutation changes `synchronized` to false without first selecting a CUDA-host policy or committing the device-to-host record. Therefore `CUDA_HOST_CUSTODY_FAILURE` is not semantically grounded in the required CUDA path. TASK BUILDER would have to invent the CUDA base, resource/custody fields, and expected positive bytes. A complete CUDA-host positive fixture plus a single-mutation negative and exact expected digests are required.

### RF2 — frozen-state and two-fresh-process requirements lack executable sequences

**Classification:** specification/executability defect; residual BF2.

The fixture contains only request ordinal zero and one frozen response row. It contains no second request in the same episode, no exact second frozen response/state digest, no reset-and-second-episode sequence, and no byte-array/digest representing either complete fresh-process run. Thus it cannot execute or verify:

- frozen returning the first complete response on a later request;
- frozen cache reset only at `reset_episode`;
- two fresh-process response sequences being byte-identical with identical state digests; or
- the committed nondeterminism mutation against a fixed run-two artifact.

The operation-result constructor alone does not supply the missing step requests or response sequences. These realizations, order, canonical bytes, and expected digests must be committed rather than invented by TASK BUILDER.

### RF3 — peer redaction-receipt digest input is undefined

**Classification:** semantic-validator executability defect; residual BF2.

Spec §4 requires the peer redaction receipt to bind “the public request digest.” The fixture commits receipt value `9391f4c...` but never defines the exact source subtree/projection or constructor that hashes to it. It is neither the committed candidate request digest (`66e029...`) nor peer request digest (`fafc619...`). Without an explicit repository-relative JSON pointer or literal digest-input object and algorithm, the semantic validator must invent which public fields are covered. Commit the exact projection/object, its canonical digest, and a negative mutation proving the binding.

## Non-blocking findings

None beyond the blocking residuals.

## Preserved evidence

- All six schemas pass Draft 2020-12 metaschema validation.
- All reconstructed positive objects and failure-result objects validate; all their committed digests match independently computed RFC-8785 bytes.
- All model JSON sidecars match raw bytes, all JSON parses, and `git diff --check` passes.
- BF1 and BF4 are closed; corrected source classification, candidate/peer privilege boundary, Entry 76 parity fields, typed mutation vocabulary, schema-first/internal-output boundaries, model neutrality, negative names, L9/gofast/host custody intent, O-14/O-15/L18/seed fences, and Phase A CLEAR remain valid evidence where not dependent on RF1–RF3.
- No real model identity, checkpoint, download/training choice, or final `gofast` identity was introduced.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to return RF1–RF3 to persistent ARCHITECT for deterministic remediation. After a committed correction, Coordinator may route the exact package back to persistent CRITIC. Nothing routes to Rebecca as a CLEAR package, and no implementation role is released.

## Explicitly prohibited actions

No TASK BUILDER release; scaffold implementation; real-model selection/download/checkpoint binding/training/integration; diagnostics, compatibility, or scoring execution; protected/courier seed access or exposure; rerun; native-CUDA L8 adoption; `GO!` use; fallback; state/provenance mutation; merge; or gate decision. CRITIC did not edit or co-author the specification, schemas, fixtures, task boundary, implementation, scoring artifacts, or `STATE.md`.

## Public-repository safety attestation

Before push, CRITIC scanned the complete review commit and diff with gitleaks and manually checked for credentials, private keys, API tokens, passwords, personal contact details/PII, machine identifiers, environment dumps, protected-seed material, persistent task/session IDs, and private absolute paths. No prohibited content was found. Repository SHAs, repository-relative paths, schema identifiers, and synthetic fixture values were classified acceptable. `git diff --check` passed.

## Execution confirmation

No implementation, model activity, compatibility/diagnostic/scoring execution, protected-seed access or exposure, rerun, CUDA-L8 adoption, fallback, state/provenance mutation, or unauthorized merge occurred.
