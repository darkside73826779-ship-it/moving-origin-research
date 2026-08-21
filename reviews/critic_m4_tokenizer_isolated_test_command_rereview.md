# CRITIC Rereview — M4 Tokenizer Isolated Test Command

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Independent law-fidelity, isolated unittest-discovery executability, regression, and public-safety rereview before any exact re-release of the still-unconsumed tokenizer materialization operation.

## Inputs and lineage reviewed

- Authority: `coordinator/m4-tokenizer-exact-image-corrective-rerelease@d7f9e984052af3088662be852bbdb0cbb5069f45`.
- Prior cleared input: `architect/m4-tokenizer-materialization-spec@d94c059645dba018bbf2d9adf1b31c388dfcd2a3`.
- Remediated input: `architect/m4-tokenizer-materialization-spec@82c31bdd3affd9481f89dc16753fcddcfd1b78db`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_ISOLATED_TEST_COMMAND_REMEDIATION_2026-08-21.md`.
- Reviewed the complete `d94c059645dba018bbf2d9adf1b31c388dfcd2a3..82c31bdd3affd9481f89dc16753fcddcfd1b78db` delta. No OCI, model, tokenizer, custody, or materialization operation was accessed or executed.

## First checklist item — Versioned-Law Compliance Protocol

The delta changes no constitutional quotation and introduces no reconstructed law, scientific threshold, bar, scoring criterion, provenance citation, or waiver. The discovery command and every new execution criterion carry `[PROPOSED]`; the handoff and changed artifacts remain dated under Regime B. Prior P1–P6 evidence remains unmodified.

**LAW_FIDELITY: CLEAR.**

## Independent command and regression verification

- The new literal command is `python3 -I -m unittest discover -s tests -t . -p test_m4_tokenizer_materialization.py` from the mounted repository root.
- The test contract fixes isolated mode, standard-library discovery, start directory `tests`, top-level directory `.`, exact filename pattern, singleton selected path, exit code 0, no custody lookup, and no materialization output.
- The spec forbids `PYTHONPATH`, installation, `.pth`, aliases/symlinks, image modification, alternate runtime, fallback, and application-written `sys.path` mutation.
- The revised test-contract committed LF SHA-256 independently reproduces as `799435d725468cf1ff848e351e7bbab0252e851710a8ad0601464a94dc1686cd`, matching its sidecar and specification/handoff bindings.
- The exact materializer command is unchanged. The banked launcher-disposition fixture and expected artifact have identical Git blob IDs before and after this delta. Pinned image/interpreter, custody, schema, fixture, RF1, and LF1/P4 evidence is otherwise untouched.
- `git diff --check` passes.

## Blocking findings

### IF1 — Specification/executability defect: discovery start-directory importability is not constructed

The prescribed command supplies `-s tests -t .`. Standard-library `unittest` discovery requires a start directory below an explicitly different top-level directory to be importable. For the specified layout, that requires the `tests` directory to be a package under the pinned runtime's discovery semantics, conventionally through `tests/__init__.py`; otherwise discovery stops with `ImportError: Start directory is not importable` before it selects or runs the named test.

No `tests/__init__.py` exists at the reviewed input, and the specification, test contract, and handoff neither prescribe that file nor bind its exact bytes/digest. Only `tests/test_m4_tokenizer_materialization.py` is named as the future singleton test path. TASK BUILDER must therefore invent an additional package-marker artifact (or choose an alternate import construction, which is forbidden) to make the exact command reach the suite. The claimed import mechanism is not executable end-to-end as committed.

This is a construction/specification defect, not a candidate failure and not a reason to rerun the prior failed invocation.

## Preserved evidence

- The revised test command, discovery flags, intended singleton path, and test-contract sidecar are internally consistent apart from IF1.
- The materializer command, positive `python3` identity, pinned OCI identities, RF1 classifier, LF1/P4 metadata, custody/schema/fixture identities, and single unconsumed operation remain preserved.
- No prior negative or instrument failure is renamed or rerun.

## Non-blocking findings

None within the authorized scope.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**  
**COMBINED DISPOSITION: BLOCK.** Law fidelity clears, but the exact isolated discovery path still requires implementer invention.

**Exact next authorized role:** WORKFLOW COORDINATOR receives this review and returns the package only to persistent ARCHITECT for IF1 importability construction remediation. Rebecca re-release and TASK BUILDER execution are not authorized.

**Explicitly prohibited actions:** Custody/model/tokenizer access; OCI execution or modification; inference/serving; Q2/EF3; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; publication; rerun; merge; and gate decision.

## Public-repository safety and prohibited-run confirmation

Public-safety scan: gitleaks 8.30.1 over the complete remediation commit range and this review artifact, required regex checks, and manual content inspection; 0 findings, cleared. No custody/model/tokenizer access, OCI or materialization execution, scoring, rerun, protected-seed exposure, state/provenance mutation, publication, or unauthorized merge occurred.
