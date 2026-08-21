# CRITIC Rereview — M4 Tokenizer Normative JSON LF Byte Domain

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Independent law-fidelity, nine-pair normative JSON worktree-byte-domain, fail-closed executability, IF2 regression, and public-safety rereview before any re-release of the still-unconsumed tokenizer materialization operation.

## Inputs and lineage reviewed

- Authority: `coordinator/m4-tokenizer-if2-execution-rerelease@902df984a2e689d41954d749fcf06570b42d9c4b`.
- Prior CLEAR: `critic/m4-tokenizer-if2-byte-domain-rereview@617d13e267b75d78c50cdb776985d35f5f8b1c5d`.
- Prior input: `architect/m4-tokenizer-materialization-spec@619ff927131222071bdc168f38f40a9760fd5476`.
- Remediated input: `architect/m4-tokenizer-materialization-spec@903a0c3a032b672a6b9a3a32bb53f66b4f1f07f5`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_NORMATIVE_JSON_LF_BYTE_DOMAIN_REMEDIATION_2026-08-21.md`.
- Instrument evidence was described as local-only and was not used as repository authority.
- Reviewed the complete `619ff927131222071bdc168f38f40a9760fd5476..903a0c3a032b672a6b9a3a32bb53f66b4f1f07f5` delta. No OCI, model, tokenizer, custody, or materialization operation was accessed or executed.

## First checklist item — Versioned-Law Compliance Protocol

The delta changes no constitutional quotation and introduces no reconstructed law, scientific threshold, bar, scoring criterion, provenance citation, or waiver. The expanded `.gitattributes`, handoff, specification, and test contract remain dated under Regime B, and every new path/validation/failure criterion remains `[PROPOSED]`. Prior P1–P6 evidence remains intact.

**LAW_FIDELITY: CLEAR.**

## Independent positive-path and regression verification

- The test contract contains exactly nine ordered, unique normative JSON paths. Each has exactly one adjacent `<path>.sha256` sidecar, producing the prescribed 9+9 set.
- `.gitattributes` names all 18 paths individually with `text eol=lf`; it uses no wildcard for this set.
- Independent normalized LF identities reproduce as:
  - `.gitattributes`: 1,458 bytes, SHA-256 `9e0a51a872ca1c4ab6a09f06dbfaf82ced32490b86bfa7675087ea10a6463b8f`;
  - test contract: 4,757 bytes, SHA-256 `ee12037da08c8841a2983e72834dc96b6a7c8138b58ad3366fbb671d141ee9f9`.
- The test-contract hash matches its adjacent sidecar and all specification/handoff bindings.
- I independently created a fresh clean detached worktree at exact SHA `903a0c3a032b672a6b9a3a32bb53f66b4f1f07f5`. For every ordered pair, both paths were regular non-links, `git check-attr` returned `text: set` and `eol: lf`, raw bytes were UTF-8/no-BOM, CR-free with exactly one final LF, every JSON parsed, every sidecar matched the exact lowercase-hex/two-space/basename/LF grammar, and every raw JSON SHA-256 matched its sidecar. The temporary worktree was removed after verification.
- The marker IF2 construction, isolated discovery command, materializer command, pinned image/runtime, RF1/LF1, custody/schema/fixture identities, and single unconsumed operation remain unchanged.
- `git diff --check` passes.

This positive evidence is valid and preserved.

## Blocking findings

### NF1 — Specification/executability defect: the mandatory pre-import validator has no executable entrypoint

The specification requires all 18 custom checks to run “before test-module import and before custody lookup.” The only authorized test invocation remains:

`python3 -I -m unittest discover -s tests -t . -p test_m4_tokenizer_materialization.py`

That command transfers control directly to the standard-library `unittest` discovery loader, which discovers and imports the selected test module. The standard library does not know this project-specific nine-pair contract. No wrapper executable, pre-import hook, command argument, startup module, or callable invocation is prescribed to execute the custom validator before `unittest` imports the test module. Application `sys.path` mutation, installation, `.pth`, image modification, and alternate commands are forbidden.

Putting validation in the test module cannot satisfy the stated ordering because its code runs only as that module is imported. TASK BUILDER must therefore invent a wrapper/hook or violate the required “before test-module import” order. The positive byte algorithm is deterministic, but it is unreachable at its mandated point in the exact command path.

### NF2 — Specification/executability defect: fail-closed negatives are enumerated but not realized

The delta mandates failures for missing/extra ordered paths, attribute mismatch, links, CR, BOM, terminal-LF errors, sidecar grammar, basename, and digest mismatches. It provides no exact committed negative fixtures, mutation bases/operations, test IDs, validation sequence outputs, or expected canonical failure artifacts for these new classes. The test contract adds a descriptive `verification` string and failure code only.

Under the binding executability rule, a list of distributions or mutation categories is not a concrete test realization. TASK BUILDER would have to choose which of 18 files to mutate, exact bytes/links/attributes to construct, ordering when multiple defects coexist, and what output/assertion proves pre-import fail-closed behavior. NF2 independently prevents CLEAR.

Both findings are specification/construction defects, not candidate failures, and authorize no rerun.

## Preserved evidence

- The exact positive 9+9 path set, LF checkout behavior, grammar rules, and committed digests independently verify.
- Prior IF2/IF1, both commands, pinned OCI identities, RF1/LF1, custody/schema/fixture contracts, and the single unconsumed operation remain preserved.
- The local-only instrument failure remains an instrument event and is neither renamed nor rerun.

## Non-blocking findings

None within the authorized scope.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**  
**COMBINED DISPOSITION: BLOCK.** Law fidelity and the positive byte construction clear, but NF1 and NF2 leave the mandated fail-closed path non-executable without implementer invention.

**Exact next authorized role:** WORKFLOW COORDINATOR receives this review and returns the package only to persistent ARCHITECT for NF1/NF2 remediation. Rebecca re-release and TASK BUILDER execution are not authorized.

**Explicitly prohibited actions:** Custody/model/tokenizer access; OCI or materialization execution/modification; inference/serving; Q2/EF3; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; publication; rerun; merge; and gate decision.

## Public-repository safety and prohibited-run confirmation

Public-safety scan: gitleaks 8.30.1 over the complete remediation commit range and this review artifact, required regex checks, and manual content inspection; 0 findings, cleared. No custody/model/tokenizer access, OCI or materialization execution, scoring, rerun, protected-seed exposure, state/provenance mutation, publication, or unauthorized merge occurred.
