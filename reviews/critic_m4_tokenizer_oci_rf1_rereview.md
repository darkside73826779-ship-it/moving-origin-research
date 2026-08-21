# CRITIC Rereview — M4 Tokenizer OCI RF1

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Narrow independent RF1 rereview of the pure no-process-spawn launcher-disposition contract before any re-release of the still-unconsumed tokenizer materialization operation.

## Inputs and lineage reviewed

- Authorities: `coordinator/m4-tokenizer-oci-environment-release@2e7fb9ee1f9643405d7fbc40120c7dc383abf9a3` and `coordinator/m4-tokenizer-materialization-release@9007260570235c1b06b104d78106ba32e8a4e9dd`.
- Prior BLOCK: `critic/m4-tokenizer-oci-command-runtime-rereview@dc381602576ce5cbeb75881efbf0f7e4802e360e`.
- Prior input: `architect/m4-tokenizer-materialization-spec@cd17bb336b4be0920c16b81b12fe09005aead47f`.
- Remediated input: `architect/m4-tokenizer-materialization-spec@404add8e67b2937f9b53af99e4aeb585bfdf3073`.
- Handoff: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_OCI_RF1_REMEDIATION_2026-08-21.md`.
- Reviewed the complete `cd17bb336b4be0920c16b81b12fe09005aead47f..404add8e67b2937f9b53af99e4aeb585bfdf3073` delta. No OCI, model, tokenizer, custody, or execution environment was accessed.

## First checklist item — Versioned-Law Compliance Protocol

The delta changes no constitutional quotation, source-tagged scientific threshold, bar, scoring criterion, provenance claim, or waiver. Its new callable and test criteria remain `[PROPOSED]`. The prior P1/P2/P3/P5/P6 evidence remains valid.

P4 states verbatim in `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1: “**P4 — Regime dating.** Every new artifact states its date and regime in its header. Acts are judged only against their own regime's text; later text is never applied backward.” The new handoff and changelog satisfy this rule, but both new JSON artifacts omit both `date` and `regime`:

- `specs/data/m4_tokenizer_runtime_unavailable_interpreter_fixture_v1.json`
- `specs/data/m4_tokenizer_runtime_unavailable_interpreter_expected_v1.json`

Their `schema_version` values do not state the act date or governing regime. **LAW_FIDELITY: BLOCK.**

## Independent RF1 executability verification

- The pure callable signature fixes four typed positional inputs and expressly forbids process launch, filesystem/environment lookup, custody lookup, and publication.
- The singleton fixture fixes `requested_executable=python`, `process_started=false`, `engine_error_class=EXECUTABLE_NOT_FOUND`, and `custody_lookup_performed=false`.
- Independent application of the four-step validation/mapping order returns exactly the committed expected object.
- The expected object expressly distinguishes launcher evidence from project output: `OCI_PROCESS_CREATION`, `PROCESS_NOT_STARTED`, `RUNTIME_IDENTITY_MISMATCH`, no custody lookup, and `project_result_artifact_expected=false`.
- The unit-test operation fixes the fixture path, positional binding order, test ID `test_unavailable_python_launcher_disposition`, RFC 8785 UTF-8/no-LF comparison, exact field set, invalid-input behavior, and no materialization-output pre/post condition.
- The test-contract row binds the callable, fixture, expected artifact, operation, test ID, and absence of a project result artifact. No mock, OCI invocation, wrapper, or error-mapping invention remains.
- The fixture, expected artifact, and revised test contract each parse as JSON. Their normalized committed LF SHA-256 values independently reproduce as `048a2990d116b280c26e5ab4d9b182d42da9bfe2ac289d6258d97a429e0b2cd3`, `55756f379dd2def1e28e91c96b24661146caa10987d2384c912ae6902a37d411`, and `aba1438c34acdc33468c4a5460e94648ad51ca0d674876eac3eb50e3dd87f8a4`; all match their sidecars.
- The two positive `python3 -I` command values, pinned image/index/platform identities, scripts/modules, arguments, custody construction, and holds are unchanged.
- `git diff --check` passes.

**RF1 substantive closure: CLEAR.** The prior executable-negative blocker is closed.

## Blocking findings

### LF1 — Provenance/law-compliance defect: new executable JSON artifacts violate P4

Both new artifacts are normative executable inputs/outputs, but neither states its date nor Regime B. This is a direct P4 failure, not a defect in the classifier mapping. Until the committed artifacts themselves carry the required metadata and all affected expected bytes/digests/bindings are reconciled, the package cannot receive combined CLEAR.

## Preserved evidence

- RF1's callable, singleton realization, deterministic mapping, expected sanitized artifact, test identity, and no-project-output boundary are substantively closed.
- Both positive `python3 -I` commands and the prior command/runtime evidence remain preserved.
- All prior tokenizer identity, constructor, schema, custody, RF2/RF3/PF1, Q2/EF3, protected-boundary, and unconsumed-operation evidence remains uninvalidated.

## Non-blocking findings

None within the authorized scope.

## Verdict and routing

**SUBSTANTIVE: CLEAR.**  
**COMBINED DISPOSITION: BLOCK.** RF1 is executable, but LAW_FIDELITY is BLOCK on P4.

**Exact next authorized role:** WORKFLOW COORDINATOR receives this review and returns the package only to persistent ARCHITECT for LF1/P4 remediation. Rebecca re-release and TASK BUILDER execution are not authorized.

**Explicitly prohibited actions:** Custody/model/tokenizer access; OCI execution or modification; inference; Q2/EF3; scoring or protected seeds; scientific change; STATE/provenance mutation; publication; rerun; merge; and gate decision.

## Public-repository safety and prohibited-run confirmation

Public-safety scan: gitleaks 8.30.1 over the complete remediation commit range and this review artifact, required regex checks, and manual content inspection; 0 findings, cleared. No custody lookup, model/tokenizer/OCI access, execution, scoring, rerun, protected-seed exposure, state/provenance mutation, publication, or unauthorized merge occurred.
