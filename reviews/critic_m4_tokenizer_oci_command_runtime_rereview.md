# CRITIC Rereview — M4 Tokenizer OCI Command/Runtime Delta

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Independent law-fidelity, command/runtime executability, regression, custody-boundary, and public-safety rereview before any re-release of the still-unconsumed tokenizer materialization operation.

## Inputs and lineage reviewed

- OCI environment authority: `coordinator/m4-tokenizer-oci-environment-release@2e7fb9ee1f9643405d7fbc40120c7dc383abf9a3`.
- Preserved materialization release: `coordinator/m4-tokenizer-materialization-release@9007260570235c1b06b104d78106ba32e8a4e9dd`.
- Prior cleared contract/CLEAR: `architect/m4-tokenizer-materialization-spec@ed25e3b4811a9024c8b7d7a0120a8fc073748004` / `critic/m4-tokenizer-rf1-final-combined-rereview@ff3976dd58009a8c6d0d8fd2cddc787fc96b63bc`.
- TASK BUILDER specification block: `taskbuilder/m4-tokenizer-materialization@c19b830547a6551657cd0fab6e3fe581cfc06983`.
- Remediated input: `architect/m4-tokenizer-materialization-spec@cd17bb336b4be0920c16b81b12fe09005aead47f`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_OCI_COMMAND_RUNTIME_REMEDIATION_2026-08-21.md`.
- Reviewed the complete `ed25e3b4811a9024c8b7d7a0120a8fc073748004..cd17bb336b4be0920c16b81b12fe09005aead47f` delta and the cited committed authority/block artifacts. No OCI, model, tokenizer, or custody artifact was accessed.

## First checklist item — Versioned-Law Compliance Protocol

The delta changes no constitutional quotation and introduces no reconstructed law, scientific threshold, bar, scoring criterion, provenance claim, or waiver. The new interpreter/negative-test rules carry `[PROPOSED]`; date and Regime B are present. The prior contract's P1–P6 law diff, source-tag audit, and provenance verification remain unmodified.

**LAW_FIDELITY: CLEAR.**

## Independent command/runtime and regression verification

- The pinned OCI image name, parent index digest `sha256:607442e407b0fea97f8a132a78b787c121a996dd4de181fa08e8da06e71ec2db`, and Linux/amd64 manifest digest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6` are unchanged.
- The committed TASK BUILDER block records that this exact manifest's image configuration declares `python3` as its entrypoint and that the configured PATH has no `python` executable. The prior exact `python -I` attempt failed at OCI process creation before any container code or custody lookup ran. The remediation's positive `python3 -I` prefix is therefore consistent with the committed runtime evidence and forbids aliases, symlinks, image modification, or host substitution.
- Both operative command prefixes change only from `python -I` to `python3 -I`. The unittest module, materialization script, request path, custody handle, output path, and argument order are unchanged.
- The test contract now binds both full commands literally. Its committed LF bytes hash to `f713bbc55a4eabd9a8c77ce9f0c0b27977c5694c24507eb7d013c1291bedef45`, matching its sidecar.
- The delta changes only the spec, test contract/sidecar, changelog, and handoff. All prior identity, construction, custody, Q2/EF3, scoring/seed, publication, and single-operation holds remain stated.
- `git diff --check` passes.

## Blocking findings

### RF1 — Specification/executability defect: unavailable-`python` negative has no executable construction

The remediation adds the test-contract row `unavailable_python_executable_name → RUNTIME_IDENTITY_MISMATCH` and requires that result “before custody lookup,” but it does not define an executable fixture, callable input, harness operation, or expected artifact for that negative.

The committed evidence establishes the underlying conflict: invoking absent `python` fails during OCI process creation, before the diagnostic script or unit-test module starts. A process that never starts cannot itself return the contract's `RUNTIME_IDENTITY_MISMATCH` result or construct its sanitized failure artifact. The specified callable `materialize(contract_path, custody_handle, output_path)` also has no interpreter-name argument through which this negative can be injected.

Consequently, TASK BUILDER would have to invent whether the unit test mocks process creation, validates a command string in a separate harness, interprets an OCI executable-not-found error, or expects a project result artifact despite no process. The required failure ordering and exact expected output are likewise absent. A negative-case name is not an executable realization. Under the binding end-to-end executability rule, this is a BLOCK.

## Preserved evidence

- The `python3 -I` positive verification and materialization command prefixes are consistent with the committed pinned-image evidence.
- Exact OCI index/platform identities and all command arguments after the interpreter prefix remain unchanged.
- The revised test-contract Git-blob sidecar independently verifies.
- The prior combined contract CLEAR remains preserved for every area outside this delta; RF1 does not reopen tokenizer identity, constructors, schemas, custody, or banked RF2/RF3/PF1 findings.
- The single authorized operation remains unconsumed.

## Non-blocking findings

None within the authorized scope.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**  
**COMBINED DISPOSITION: BLOCK.** Law fidelity clears, but the new mandatory negative test is not executable without implementer invention.

**Exact next authorized role:** WORKFLOW COORDINATOR receives this review and returns the command/runtime package only to persistent ARCHITECT for RF1 remediation. Rebecca re-release and TASK BUILDER execution are not authorized.

**Explicitly prohibited actions:** Custody/model/tokenizer access; OCI execution or modification; inference/serving; Q2/EF3; qualification; diagnostics/scoring; protected seeds; scientific change; STATE/provenance mutation; publication; rerun; merge; and gate decision.

## Public-repository safety and prohibited-run confirmation

Public-safety scan: gitleaks 8.30.1 over the complete remediation commit range and this review artifact, required regex checks, and manual content inspection; 0 findings, cleared. No custody lookup, tokenizer/model/OCI access, execution, scoring, rerun, protected-seed exposure, state/provenance mutation, publication, or unauthorized merge occurred during this rereview.
