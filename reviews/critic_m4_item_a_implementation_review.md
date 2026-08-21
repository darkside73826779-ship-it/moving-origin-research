# CRITIC Review — M4 Item A Callable-Step Implementation

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Independent code-versus-cleared-specification, synthetic executability, regression, failure-state preservation, test-adequacy, law-fidelity, and public-safety implementation review

## Inputs and SHAs reviewed

- Rebecca re-release: `coordinator/m4-item-a-implementation-rerelease@2a38ecc4e389be8c6c698e476cf88d581b0fa280`
- Cleared design head/result: `b467b0a1094904077414058f0bbf56b81c43e2d2` / `e1bdf5126dbea51256c089ecc43c79d5b6404a1f`
- Prior design CLEAR: `critic/m4-callable-step-remediation-review@a3dee46ea9157a99d2cfdc88a89ead862e838a6a`
- Implementation branch/head: `taskbuilder/m4-item-a-implementation@517555ebd3cfdb1c2037a1457fd52b780c5a478b`
- Implementation commit: `e0da37bb931997c7d881e52acb4b5c522a14b360`
- Handoff: `handoffs/TASKBUILDER_TO_COORDINATOR_M4_ITEM_A_IMPLEMENTATION_2026-08-21.md`
- Code/tests: `src/m4_model_scaffold.py`, `src/test_m4_model_scaffold.py`

## Verdict

- **LAW_FIDELITY: CLEAR**
- **IMPLEMENTATION: BLOCK**
- **Combined disposition: BLOCK**

The exact happy-path digest chain reproduces, but successful lifecycle methods do not enforce the specification's validate-before-commit rule. An invalid operation result can be returned after the state has already advanced.

## First checklist item — law, tags, provenance

- P1/P2: the implementation reconstructs no law text and changes no quoted law; the controlling spec's law quotations remain byte-identical to the constitution.
- P3: no scientific threshold, bar, kill condition, or scoring predicate is introduced or changed. Constants implement the `[PROPOSED]` synthetic contract.
- P4: module/test headers and handoffs state 2026-08-21, Regime B.
- P5: no deviation from law or locked scoring semantics is claimed.
- P6: the implementation lineage and released scope match the committed Rebecca re-release. No false provenance claim was found.

## Verified implementation evidence

- `python -m py_compile src/m4_model_scaffold.py src/test_m4_model_scaffold.py`: PASS.
- `python -m unittest -v src.test_m4_model_scaffold`: 10/10 PASS.
- All released prefix and amendment wrappers reproduce canonical bytes and digests.
- The callable happy path reproduces describe → initialize → reset → step → snapshot → close and the exact response/projection/full-state digest chain.
- Request canonicalization, base mismatch, wrapper tamper, out-of-order lifecycle, reset digest mismatch, snapshot digest mismatch, and tested failure-state immutability paths fail as reported.
- The custom validator implements the JSON Schema keywords exercised by the named released schemas.

## Blocking finding

### IF1 — Success paths commit state before validating the operation result

The cleared specification requires: construct and validate the next complete state; hash it; construct the operation result with exact pre/post hashes; validate that result; only then commit state. The implementation does not follow that custody order:

- `step()` assigns `self.state = post` and then serializes the literal step result without validating its schema, wrapper digest, prior-state digest, post-state digest, or correspondence to the state just committed.
- `snapshot()` and `close()` likewise assign the next state and return literal operation results without validating the next state/result or exact transition bindings.
- `describe()`, `initialize()`, and `reset_episode()` also advance state before validating their returned success result.
- `verify_released_fixtures()` can detect malformed governed literals, but it is a separate optional function; adapter construction and lifecycle calls do not require it.

Independent negative reproduction: after changing only the in-memory step operation-result status to the schema-invalid string `INVALID`, a valid step returned that invalid result and left adapter state committed as `STEPPED`. No exception or failure result was produced. This directly falsifies fail-closed result validation and failure-state preservation.

The existing ten tests do not inject a malformed success state/result or assert that validation occurs before mutation, so the defect is not covered.

**Classification:** implementation construction bug and test-adequacy defect. The candidate implementation fails the cleared callable state-custody contract.

## Non-blocking findings

- The restricted `canonical_json` implementation is sufficient for the committed fixture domain tested here; it should not be represented as a general RFC-8785 implementation outside that domain.
- Git LF normalization for the amendment file is handled deterministically and does not alter committed specification bytes.

## Preserved evidence

- Design CLEAR `a3dee46...` remains valid; this is an implementation failure, not a specification defect.
- The happy-path non-cyclic response/projection/full-state construction is correct.
- All passing compile, fixture reconstruction, digest, schema, and tested failure evidence remains preserved except where IF1 shows missing coverage.
- Work Item B and all model/tokenizer/OCI, scoring, seed, L8, science, STATE/provenance, rerun, and merge holds remain unchanged.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to verify lineage and return this BLOCK to the originating persistent TASK BUILDER for narrow IF1 remediation and a negative validate-before-commit regression test. The corrected implementation returns through Coordinator to persistent CRITIC. Do not route to Rebecca on this BLOCK.

## Explicitly prohibited actions

No model/tokenizer/OCI access; serving; qualification; diagnostics/scoring; protected seeds; serial/native-CUDA L8; scientific/bar/control/battery changes; Work Item B changes; STATE/provenance mutation; rerun; merge; gate decision; or implementation release by CRITIC.

## Public-repository safety attestation

Before push, CRITIC scanned all three introduced commits and intermediate diffs in `b467b0a1094904077414058f0bbf56b81c43e2d2..517555ebd3cfdb1c2037a1457fd52b780c5a478b`, plus this review, using gitleaks and targeted manual checks for credentials, keys/tokens, PII, private paths, machine identifiers, environment dumps, protected seeds, model/tokenizer/OCI artifacts, caches, and Git LFS pointers. Gitleaks reported zero findings. No prohibited content was found; `git diff --check` passed.

## Execution confirmation

Only the authorized synthetic compile/unit tests and an in-memory negative lifecycle construction were run. No model/tokenizer/OCI access, serving, qualification, diagnostics/scoring, protected-seed exposure, L8 activity, Work Item B change, STATE/provenance mutation, rerun, unauthorized merge, or gate decision occurred.
