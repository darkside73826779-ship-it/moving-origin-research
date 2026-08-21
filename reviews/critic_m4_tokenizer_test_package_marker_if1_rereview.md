# CRITIC Rereview — M4 Tokenizer Test Package-Marker IF1

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Narrow independent IF1 package-marker identity/importability, isolated-discovery regression, law-fidelity, and public-safety rereview before any re-release of the still-unconsumed tokenizer materialization operation.

## Inputs and lineage reviewed

- Authority: `coordinator/m4-tokenizer-exact-image-corrective-rerelease@d7f9e984052af3088662be852bbdb0cbb5069f45`.
- Prior BLOCK: `critic/m4-tokenizer-isolated-test-command-rereview@560b9fc9d47d1ecdafc0e54695864a0b5afd515e`.
- Prior input: `architect/m4-tokenizer-materialization-spec@82c31bdd3affd9481f89dc16753fcddcfd1b78db`.
- Remediated input: `architect/m4-tokenizer-materialization-spec@6d040083a7fe7dddfda351e863dc8940ca25689f`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_TEST_PACKAGE_MARKER_IF1_REMEDIATION_2026-08-21.md`.
- Reviewed the complete `82c31bdd3affd9481f89dc16753fcddcfd1b78db..6d040083a7fe7dddfda351e863dc8940ca25689f` delta and both the committed Git object and checked-out marker bytes. No OCI, model, tokenizer, custody, or materialization operation was accessed or executed.

## First checklist item — Versioned-Law Compliance Protocol

The delta changes no constitutional quotation and introduces no reconstructed law, scientific threshold, bar, scoring criterion, provenance citation, or waiver. The marker text itself states `Date: 2026-08-21` and `Regime: B`; all new marker/test criteria are `[PROPOSED]`. Prior P1–P6 evidence remains intact.

**LAW_FIDELITY: CLEAR.**

## Independent IF1 and regression verification

- `tests/__init__.py` is committed as a regular Git mode `100644` blob, not a link.
- Its committed LF blob is exactly 69 bytes and hashes to `6f56eb2128751f0c5c1ab27ff461b38565aa00a3dcd29c04ab8bd56c34f4a961`, matching the literal spec text, test-contract marker identity, and handoff.
- The marker contains the prescribed date and Regime B metadata and makes `tests` a Python package for the declared `-s tests -t .` discovery layout.
- The revised test-contract LF SHA-256 independently reproduces as `99199e6ad49aeb8711e1f7d267145ea10624f2179258fe6b23010fb0c8df7803`, matching its sidecar and specification/handoff binding.
- The isolated discovery command and materializer command are exactly unchanged from `82c31bd`. Pinned image/interpreter, RF1 classifier, LF1/P4 metadata, custody/schema/fixture identities, and the unconsumed operation remain unchanged.
- `git diff --check` passes.

**Prior IF1 importability closure:** The missing package marker is supplied and fully bound at the Git-object level.

## Blocking findings

### IF2 — Construction/specification defect: runtime marker-byte domain is ambiguous and not checkout-stable

The specification requires, before discovery, an exact regular non-link `tests/__init__.py` with UTF-8/no-BOM, LF-only bytes, one final LF, byte count 69, and the fixed SHA-256. It later calls this a “Git-blob identity,” but does not say whether the pre-discovery validation hashes the committed Git blob or the mounted worktree file. Those domains are not interchangeable.

No `.gitattributes` rule or other committed checkout/construction mechanism fixes LF materialization for this path. In the reviewed Windows checkout, Git's text conversion produces a regular worktree file of 74 bytes with CRLF line endings, while normalizing it back to LF produces the bound 69-byte digest. Thus the exact committed input already demonstrates two different byte realizations:

- committed Git blob: 69 LF bytes, bound SHA-256;
- mounted-worktree candidate in this checkout: 74 CRLF bytes, not the bound SHA-256.

The OCI command operates on the mounted repository root, so TASK BUILDER must invent whether to validate via `git cat-file`, require a particular Git checkout configuration, normalize/copy the marker, or hash the mounted file and fail. The contract forbids alternate/path mutation and expects successful discovery, but fixes none of those constructions. Consequently, package importability is solved while end-to-end deterministic execution is still not.

This is a specification/construction defect, not a candidate failure, and it does not authorize another invocation.

## Preserved evidence

- The package marker's committed identity and Python-package function are valid and banked.
- Both commands, test-contract content apart from marker binding, pinned OCI identities, RF1/LF1 evidence, custody/schema/fixture contracts, and single unconsumed operation remain preserved.
- No prior instrument failure is renamed or rerun.

## Non-blocking findings

None within the authorized scope.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**  
**COMBINED DISPOSITION: BLOCK.** Law fidelity clears and the original missing-marker issue is closed, but IF2 leaves the runtime byte-validation construction dependent on checkout behavior and implementer choice.

**Exact next authorized role:** WORKFLOW COORDINATOR receives this review and returns the package only to persistent ARCHITECT for IF2 byte-domain/checkout construction remediation. Rebecca re-release and TASK BUILDER execution are not authorized.

**Explicitly prohibited actions:** Custody/model/tokenizer access; OCI or materialization execution/modification; inference/serving; Q2/EF3; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; publication; rerun; merge; and gate decision.

## Public-repository safety and prohibited-run confirmation

Public-safety scan: gitleaks 8.30.1 over the complete remediation commit range and this review artifact, required regex checks, and manual content inspection; 0 findings, cleared. No custody/model/tokenizer access, OCI or materialization execution, scoring, rerun, protected-seed exposure, state/provenance mutation, publication, or unauthorized merge occurred.
