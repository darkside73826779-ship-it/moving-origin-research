# CRITIC Rereview — M4 Model-Agnostic Scaffold RF1–RF3 Remediation

**Timestamp:** 2026-08-21 07:07 EDT

**Regime:** B

**Gate served:** Persistent independent CRITIC rereview of RF1–RF3 deterministic remediation before Rebecca approval or implementation.

## Inputs and SHAs reviewed

- Coordinator authority: `coordinator/m4-cuda-ready-cpu-l8-directive` at `a4d8dc054d3944d3a0efbafeea955b3570f0a272`.
- Prior authoritative rereview: `critic/m4-model-agnostic-scaffold-bf1-bf4-rereview` at `6a56680bcdd8aa3c7460e66aa9ba8c42352db94f`.
- ARCHITECT branch/head: `architect/m4-model-agnostic-scaffold` at `9162cff769f7d20b811fb6fbfc5d572869bc42d5`.
- Remediation result/parent: `b776083d78e75e4562c76f49166f7ca1224e8807`, parent `a5716c18a54f3ef1d47778c158ae63d220c8f76d`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_SCAFFOLD_RF1_RF3_REMEDIATION_2026-08-21.md`.
- Supplemental fixture: `specs/data/m4_model_scaffold_rf1_rf3_fixture_v1.json`.
- Full RF1–RF3 delta, base executable fixture, schemas, task boundary, sidecars, law quotations/source tags, provenance Entries 11/76, and preserved Phase A authority.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

RF2 and RF3 are closed. RF1 is substantively constructed and its CUDA manifest/request/response digests match, but the custody record contains a self-included expected digest whose literal-object SHA-256 does not equal the committed value. The only matching calculation silently removes that field, an exclusion the contract never specifies. This is a narrow deterministic construction bug.

## First checklist item — law/source/provenance audit

- **P1/P2 CLEAR:** The quoted P1–P3 and L7/L8/L9/L14/L18/L19 text remains verbatim against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; this delta changes no quotation.
- **P3 CLEAR:** New projection, CUDA, frozen, run, and digest controls are `[PROPOSED]`; matched-peer and Entry 76 Ruling 3/5 authorities remain separately and correctly tagged.
- **P4 CLEAR:** New normative Markdown and JSON state 2026-08-21 and Regime B.
- **P5 CLEAR:** No law/bar deviation or waiver is claimed.
- **P6 CLEAR:** Entry 11 and Entry 76 Rulings 3/5 remain consistent with their actual committed text. BF1/BF4 law/provenance closures are preserved.

## RF1–RF3 independent reconstruction

- The supplemental raw file SHA-256 is `a3a423128f09fc927c28c21714988541bdeafa43136e26f9b46f2a9856774689`, matching its sidecar; its bound base raw digest also matches the base fixture.
- **RF1 partial:** The patched CUDA dependency, manifest, request, and internal positive response reconstruct to their exact committed digests. The manifest/request/response validate under the committed schemas. The CUDA negative is a single `synchronized:true→false` mutation on this CUDA base and its failure-result digest reconstructs. The custody-record digest defect remains below.
- **RF2 CLOSED:** The frozen manifest, three requests, three responses, and nine lifecycle results validate. Every expected digest matches. Episode-one payload digests are equal; request-correlated envelopes differ as specified; the post-reset episode-two payload differs. Both stored 17-artifact digest arrays match the reconstructed artifacts and are identical. Concatenated canonical artifact bytes plus LF hash to `fb80fa07998f7f6a676ff9e260551daf1c632a136ee07faa143dd1374aba2d0c` for both runs. The one-bit run-two confidence mutation produces the exact mutated response and run digests.
- **RF3 CLOSED:** Copying the four ordered pointers from the complete peer request produces the literal projection and SHA-256 `9391f4c9978bc311d10f91da6299009a87e77104a1a0955c1b3c7446362ed9f7`. It equals the receipt; the complete peer request digest also matches. The negative is non-no-op and has the exact committed `DIGEST_MISMATCH` result digest.

## Blocking finding

### RF1A — custody-record digest has no executable domain

**Classification:** construction bug / digest-contract executability defect.

`cuda_host_positive.custody_record` embeds `expected_sha256` inside the record. Under the fixture's stated subtree rule, hashing the literal RFC-8785 object yields:

`7af46d25559a84199c9365c372cdac0dde2759d1b8be9e90cf7552ed07159d47`

The embedded expected value is:

`7900b71e8acf4048ba3c5727f1ec9b2474de6f531a893035b071a3d5ff22d72c`

That expected value is obtained only by removing `/expected_sha256` before canonicalization. No rule, pointer list, wrapper constructor, or exclusion authorizes that removal. Other fixture objects place expected digests outside the constructed artifact, so their domains are unambiguous. TASK BUILDER must not infer a special self-field exclusion.

Remediation must either move `expected_sha256` outside the custody artifact (for example, an `artifact` plus sibling expected digest wrapper) or explicitly fix an exact projection/exclusion rule, then update the literal digest and any run binding. The custody artifact should also be validated under whatever exact record contract governs it.

## Non-blocking findings

None beyond RF1A.

## Preserved evidence

- BF1 and BF4 remain closed.
- RF2 and RF3 are closed by independent reconstruction.
- RF1's CUDA dependency, manifest, request, response, single custody mutation, and failure-result construction are preserved; only the positive custody-record digest domain remains invalid.
- All relevant JSON parses, adjacent sidecars match, and `git diff --check` passes.
- Model neutrality, scientific labels, L9/gofast boundaries, O-14/O-15/L18/seed fences, Phase A CLEAR, and all holds remain intact. No real model or final `gofast` identity was introduced.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to return RF1A to persistent ARCHITECT for minimal deterministic remediation. After a committed correction, Coordinator may route the exact package back to persistent CRITIC. Nothing routes to Rebecca as CLEAR, and no implementation role is released.

## Explicitly prohibited actions

No TASK BUILDER release; implementation; model selection/download/checkpoint binding/training/integration; diagnostics, compatibility, or scoring execution; protected/courier seed access or exposure; rerun; native-CUDA L8 adoption; `GO!` use; fallback; state/provenance mutation; merge; or gate decision. CRITIC did not edit or co-author the specification, schemas, fixtures, task boundary, implementation, scoring artifacts, or `STATE.md`.

## Public-repository safety attestation

Before push, CRITIC scanned the complete review commit and diff with gitleaks and manually checked for credentials, private keys, API tokens, passwords, personal contact details/PII, machine identifiers, environment dumps, protected-seed material, persistent task/session IDs, and private absolute paths. No prohibited content was found. Repository SHAs, repository-relative paths, canonical digests, and synthetic fixture values were classified acceptable. `git diff --check` passed.

## Execution confirmation

No implementation, model activity, compatibility/diagnostic/scoring execution, protected-seed access or exposure, rerun, CUDA-L8 adoption, fallback, state/provenance mutation, or unauthorized merge occurred.
