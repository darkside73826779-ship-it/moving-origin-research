# CRITIC Review — M4 Model-Agnostic Adapter and Synthetic Scaffold v1

**Timestamp:** 2026-08-21 06:39 EDT

**Regime:** B

**Gate served:** Persistent independent CRITIC review of the model-agnostic candidate/peer adapter and deterministic synthetic-scaffold specification before Rebecca approval or any mechanical implementation.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-cuda-ready-cpu-l8-directive` at `a4d8dc054d3944d3a0efbafeea955b3570f0a272`.
- ARCHITECT branch/head: `architect/m4-model-agnostic-scaffold` at `7afa624093e6cc69c7a5e9f1a4d8dff13f2b729d`.
- Specification result: `09980ffc3b421a8112ed35d653f88213109c1faa`.
- Primary spec: `specs/m4_model_agnostic_scaffold_spec_v1.md`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_MODEL_AGNOSTIC_SCAFFOLD_2026-08-21.md`.
- Approved Phase A head/result and persistent CLEAR: `e5edb1e804cc4a6553507c98140fa9fa49586a0d` / `e7419633f34c7eebadfe3cea33c84aff3883a4aa` / `0790b4a24a868df84739199f1eab7bb16ebe0609`.
- Full specification delta, six Draft 2020-12 schemas, fixture/task-boundary artifacts and sidecars, constitution §5 and L7/L8/L9/L14/L18/L19, M4 task/spec authority, provenance Entries 11 and 76, and standing governance fences.

## Verdict

- **LAW_FIDELITY: BLOCK**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

The package is not executable. One mandatory schema fails its metaschema and cannot resolve its own references; the committed fixtures are partial descriptions rather than executable artifact pairs; several promised semantic failures cannot be reached under the stated schema-first order. A threshold/source tag also cites authority that does not contain that rule.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** I byte-compared the quoted P1–P3 and L7/L8/L9/L14/L18/L19 text against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; the quotations are verbatim and no constitutional text was reconstructed.
- **P3 BLOCK:** Spec §5 tags the requirement that confidence be finite and in `[0,1]` as `[BAR-Entry 11]`. Entry 11 contains no confidence-domain rule. The existing M4 provenance treats confidence definition/method separately; the scaffold's numeric domain is a new proposed interface constraint and must not be represented as a Rebecca-locked Entry 11 bar. The same line correctly tags self-state probabilities `[PROPOSED]`, demonstrating the required source class is available.
- **P4 CLEAR:** New normative Markdown and JSON artifacts state 2026-08-21 and Regime B.
- **P5 CLEAR:** No waiver or direct change to constitutional law is claimed.
- **P6 BLOCK through P3:** Entry 11 and Entry 76 were checked against their actual committed text. Entry 76 Ruling 3 supports the non-self specificity hook. Entry 11 supports matched-peer construction, but not the `[0,1]` confidence-domain attribution above.

## Blocking findings

### BF1 — request schema is not a valid Draft 2020-12 schema

**Classification:** construction bug / executability defect.

`m4_model_adapter_request_schema_v1.json` places `$defs` and `allOf` inside `properties`; it also places `ground_truth` and `perturbation` inside the `retrieval` schema rather than declaring them as top-level properties. Independent `Draft202012Validator.check_schema` fails because `properties.allOf` is an array where a property schema must be an object or boolean. Runtime validation raises `PointerToNowhere` for `#/$defs/sha256`. Moreover, top-level `required` names `ground_truth` and `perturbation`, but neither exists in top-level `properties` while `additionalProperties=false`. No conforming request can be constructed. This directly contradicts the handoff's metaschema/executability claim.

### BF2 — the fixture does not commit complete executable inputs or exact outputs

**Classification:** specification/executability defect.

The spec says `m4_model_scaffold_fixtures_v1.json` fixes a complete request and exact outputs. It does not commit a complete schema-valid manifest, candidate request, peer request, response, operation-result sequence, checkpoint object, publication pair, dependency manifest, or CUDA-host custody record. Its `exact_expected` members are partial projections: required response fields such as schema/date/regime/adapter/episode/role/arm, hook receipts, resource report, state digests, and failure code are absent; several adapters contain only selected fields or prose aliases such as `equals`. No canonical expected response bytes or SHA-256 values are committed for the nine outputs. TASK BUILDER would have to invent the missing envelopes, state transitions, digests, receipts, and ordering. This violates the binding executable-fixture and expected-digest requirements.

The 17 negative fixtures likewise store prose mutation strings, not exact typed mutations against fixed base artifacts and pointers. There are no literal expected failure objects/bytes/digests or exact base selector for each case. Consequently the claimed one-collection-per-row suite cannot be independently reproduced.

### BF3 — semantic failure reachability contradicts schema-first routing

**Classification:** construction bug / validator-order defect.

The spec requires JSON decode and structural schema validation before semantic validation. At least these committed expectations cannot follow that route:

- `cuda_custody` mutates `synchronized=false`, but the response schema structurally fixes `synchronized` to `true`; schema-first processing returns `SCHEMA_DRIFT`, not `CUDA_HOST_CUSTODY_FAILURE`.
- `peer_confidence_leak` says a peer request “includes candidate confidence,” but the request schema declares no such field and has `additionalProperties=false`; once BF1 is repaired without expressly admitting this semantic-negative field, the mutation is structurally rejected rather than reaching `PRIVILEGED_STATE_LEAK`.
- `nonfinite` sets JSON confidence to `NaN`. RFC 8785/JSON has no NaN value; JSON decoding/canonicalization cannot produce the promised later `NONFINITE_OUTPUT` path. An internal adapter-output injection boundary would need a separately specified non-JSON realization.

The package must align each negative with its actual validation stage, or structurally admit a precisely scoped negative representation so the intended semantic code is reachable. It must then commit exact expected failure objects and order.

### BF4 — matched-peer authority is incompletely bound in the machine contract

**Classification:** provenance-backed substantive omission.

Entry 76 Ruling 5 requires identical confidence calibration, evaluation data, ECE definition, and binning, plus paired independently trained instances. The prose mentions a calibration-contract digest and evaluation stream, but the manifest schema has no explicit evaluation-data, ECE-definition, or binning identities, and the fixture supplies no candidate/peer manifest pair proving all required equalities while restricting the difference to the privileged channel. The stated semantic validator therefore lacks complete machine-readable inputs for the locked peer comparison.

## Non-blocking findings

None; all material findings above block executability or law fidelity.

## Preserved evidence

- Five of six schemas independently pass Draft 2020-12 metaschema validation; only the request schema fails.
- All eight new JSON artifacts parse, and every adjacent SHA-256 sidecar matches its raw artifact bytes. `git diff --check` passes.
- The model-neutral intent, nine stored adapter names, scientific negative labels, L9 fence, host-only `gofast` boundary, real-model prohibition, checkpoint/publication custody intent, qualification gating, O-14/O-15/L18/seed fences, and Rebecca-only authority are preserved as valid design evidence where not dependent on BF1–BF4.
- No real model/checkpoint/download/training choice or final `gofast` implementation identity was introduced.
- The approved Phase A CLEAR at `0790b4a24a868df84739199f1eab7bb16ebe0609` remains valid; this BLOCK concerns the later scaffold package.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to return BF1–BF4 to persistent ARCHITECT for remediation. After a committed correction, Coordinator may route the exact package back to persistent CRITIC. Nothing routes to Rebecca as a CLEAR package, and no implementation role is released.

## Explicitly prohibited actions

No TASK BUILDER release; scaffold implementation; real-model selection, naming, download, checkpoint binding, training/fine-tuning, or integration; diagnostics, compatibility, or scoring execution; protected/courier seed access or exposure; rerun; native-CUDA L8 adoption; `GO!` use; fallback; state/provenance mutation; merge; or gate decision. CRITIC did not modify or co-author the specification, schemas, fixtures, task boundary, implementation, scoring artifacts, or `STATE.md`.

## Public-repository safety attestation

Before push, CRITIC scanned the complete review commit and diff with gitleaks and manually checked for credentials, private keys, API tokens, passwords, personal contact details/PII, machine identifiers, environment dumps, protected-seed material, persistent task/session IDs, and private absolute paths. No prohibited content was found. Repository SHAs, repository-relative paths, schema error names, and synthetic fixture values were classified acceptable. `git diff --check` passed.

## Execution confirmation

No implementation, model activity, compatibility/diagnostic/scoring execution, protected-seed access or exposure, rerun, CUDA-L8 adoption, fallback, state/provenance mutation, or unauthorized merge occurred.
