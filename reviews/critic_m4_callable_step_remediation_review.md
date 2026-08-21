# CRITIC Review — M4 Callable-Step Digest Remediation

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Independent law-fidelity, substantive, executability, regression, and public-safety review of Work Item A before scaffold implementation may resume

## Inputs and lineage reviewed

- Coordinator authority: `coordinator/m4-scaffold-rerelease-tokenizer-custody@45d40d8b688fb7f44098d235df7f31cca1aa3b31`
- Originating TASK BUILDER block named by the handoff: `taskbuilder/m4-scaffold-rerelease@2c3312b13c5e968519f6a9d9e9bf0afaf84f8f0d`
- Preserved base: `ade99fc13dc750b789d254316b9a7dc5de2eae8b`
- ARCHITECT specification result: `e1bdf5126dbea51256c089ecc43c79d5b6404a1f`
- ARCHITECT routing head: `architect/m4-scaffold-callable-step-remediation@b467b0a1094904077414058f0bbf56b81c43e2d2`
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_CALLABLE_STEP_REMEDIATION_2026-08-21.md`
- Controlling amendment: `specs/data/m4_callable_step_digest_amendment_v1.json`
- Amended specification: `specs/m4_model_agnostic_scaffold_spec_v1.md`

The named commits and remote-tracking ref were present in this isolated CRITIC repository. The earlier inability to access them was an instrument/access failure and did not become a specification verdict.

## First checklist item — versioned-law compliance

### Law quotation diff

I compared every quoted law and P1–P3 protocol line in the specification's opening law section against `docs/ARCHITECTURAL_CONSTITUTION_v2.md`. The quoted P1–P3 text and L7, L8, L9, L14, L18, and L19 law text are verbatim. The reviewed delta adds only §8.2 and does not alter any quotation. P1 and P2 pass.

### Source-tag audit

The new construction order, digest domains, fixed fixtures, failure condition, and release condition are tagged `[PROPOSED]`. The delta introduces no scientific threshold, locked bar, kill condition, scoring predicate, or untagged numeric acceptance criterion. Existing constitutional thresholds remain attached to their `[LAW-Lx]` quotations. P3 passes.

### Regime, deviation, and provenance

The amended spec, changelog, handoff, and machine-readable amendment state date 2026-08-21 and Regime B. No law deviation is introduced. The delta makes no new claim of the form “Entry n said X”; preserved Entry 76 citations were checked against `docs/rulings/provenance_log.md`, including Rulings 3 and 5. P4–P6 pass.

**LAW_FIDELITY: CLEAR.**

## Independent substantive and executability review

### Canonical artifacts and digest chain

I independently reconstructed the amendment from the preserved callable fixture and executable scaffold fixture, without executing the amendment builder or changing specification files. Results:

- The base callable fixture's Git-blob SHA-256 is exactly `a7a3f2a2b9dd562e06db7f8b73b52b40f5c8eaa7dc6f2af9a474978040ceb0e5`.
- The amendment Git blob's raw SHA-256 is exactly `03fbcfcd1ff39bc27ead3496197fcdd8e6994bb3587d5a7be838d470beb70f0c`, matching its sidecar.
- All nine wrappers reproduce both their canonical UTF-8 base64 and SHA-256 values: varying response; stepped-state projection; complete stepped state; step result; snapshot request; snapshotted state; snapshot result; closed state; close result.
- The complete ready/pre-state digest is `cf16e09282530ea32e8d5a775962ea06f28013117b0942faf637e48deda0add8`.
- Deleting exactly `/last_response_sha256` from the constructed post-state produces projection digest `5929bffe4cbddd3eff45d2148d45d28a2e87b7a3d244f7683c47f2b6ac3644f4`.
- The complete response digest is `190b49b15d5dd0b5adb693056b5781a0ac8b0cd227dd2d445bac2dd02f2f3e33`; that exact value is inserted into the complete stepped, snapshotted, and closed states.
- The complete stepped-state digest is `f1a740defb2ee5fe6ad484195af3eebd8c2c69735ff0ba3fdaa264f4018a7021`; the snapshotted-state digest is `5a364f4c2b31db0c12bac3c39ff739e0d1a0e2aa7df994dccf0713d117e8bc1b`; the closed-state digest is `fd37cc26f31cd4e47e078383e19e46007f9cd529e3e7d5914d4c45178f0f4790`.

The callable request, response, and ready state all use `callable-episode-0`, with request/next-request ordinal zero before the step. `state_before_sha256` binds the complete ready state; `state_after_sha256` binds the precisely defined projection; and the operation result binds the complete post-state. Because the response does not hash a state containing its own digest, no fixed-point or placeholder remains.

### Schemas and lifecycle regression

The varying response validates against the response schema; stepped, snapshotted, and closed states validate against the state schema; the three operation results validate against the operation-result schema; and the snapshot request validates against the snapshot-request schema. The projection is deliberately not asserted to be a complete state and is used only in its separately specified digest domain.

The delta does not modify `m4_model_callable_fixture_v1.json` or any of its describe, initialize, or reset artifacts. The precedence declaration replaces only the named first-step response digest, three state wrappers, three operation-result wrappers, and snapshot request/digest. Thus the verified describe/initialize/reset prefix and all unlisted fixtures remain operative. `git diff --check` passes.

### End-to-end implementer inputs and fences

The base commit/path/raw digest, ordered construction, one-field projection, complete literal wrappers, canonicalization rule, exact digests, schemas, and precedence are committed. TASK BUILDER can copy the prescribed bytes and need not invent an episode identity, state digest domain, response digest, transition artifact, schema, ordering, or expected digest.

All prior scope fences remain: Work Item B is untouched; the amendment grants no model/tokenizer access, diagnostics, scoring, protected-seed access, L8 change, state/provenance mutation, rerun, merge, or gate decision. It explicitly remains held after this review until Rebecca re-releases the exact operative amendment.

**SUBSTANTIVE: CLEAR.**

## Findings

### Blocking findings

None.

### Non-blocking findings

- The pre-existing Python audit helper could not import its JSON Schema dependency in the restored environment. This was an instrument defect. Independent canonical reconstruction plus PowerShell's JSON Schema validator supplied the required review evidence; it does not affect the contract.
- `gitleaks` was unavailable in this CRITIC environment. The mandatory fallback full-history regex and manual review were therefore used and are recorded below.

## Preserved evidence

- Prior callable-contract closures and the byte-identical describe/initialize/reset prefix remain valid.
- The TASK BUILDER's durable block remains preserved as the reason this amendment was required; it is not reclassified or erased.
- All prior scientific, O-14/O-15, L9, L18, protected-seed, custody, publication, and role-independence fences remain unchanged.
- Work Item B, Q2, EF3, model/tokenizer custody, and their holds are outside this review and remain unchanged.

## Combined disposition and next route

**Combined verdict: CLEAR.**

Exact next authorized role: **WORKFLOW COORDINATOR**, which must verify this committed lineage and stop for Rebecca's explicit decision on re-releasing the exact amendment. This CLEAR does not itself release TASK BUILDER or implementation.

Explicitly prohibited: direct routing around the Coordinator; implementation or tests/diagnostics execution; model/tokenizer access; scoring or protected-seed exposure; L8 or Work Item B changes; state/provenance mutation; rerun; merge; or any gate decision by CRITIC.

## Public-repository safety and process attestation

Before push I scanned every introduced commit and intermediate diff in `ade99fc13dc750b789d254316b9a7dc5de2eae8b..b467b0a1094904077414058f0bbf56b81c43e2d2`, then scanned this review diff. Checks covered credential/token/key patterns, private keys, emails, private absolute paths, host/user/machine identifiers, environment assignments/dumps, Git LFS pointers, protected seeds, model/tokenizer binaries or reconstructive content, and manual content review. `gitleaks` was unavailable. The only email-shaped match was the required synthetic CRITIC Git identity `role@moving-origin-research.local`; it is not personal contact information and is acceptable. No prohibited content was found.

No scoring, failed-scoring rerun, protected/hold-out seed exposure, implementation, model/tokenizer access, state/provenance mutation, unauthorized merge, or gate decision occurred during this review.
