# CRITIC Review — M4 Tokenizer BF1–BF5 Remediation

**Date:** 2026-08-21
**Regime:** B
**Gate served:** One independent implementation, executability, regression, law-fidelity, and public-safety review of the integrated M4 tokenizer executable-package BF1–BF5 remediation.

## Canonical intake

- Canonical return: `taskbuilder/m4-tokenizer-bf1-bf5-remediation` at `b4837b6af3310afac36ff343e58490756cdf54cb`.
- Implementation result: `03cf97e0a8af4869a9cffe609c92f3896d30b62d`.
- Handoff result: `69135dee519bab81653e4c3ff020ce02adacb093`.
- Input Architect BLOCK: `architect/m4-tokenizer-executable-package-remediation` at `bdbc1ad0eead7ff8dafd5e38b667f5a5810b5212`.
- Architect review result: `0a8c738d6b730f4f2da9fcd333e68467bd669158`.
- Base: `47e06c361c361843916668304432f7a748ac514e`.

The committed common handoff manifest validated with `tools/workflow_contract_validator.py`. An independent raw `git cat-file blob` inventory reproduced all 20 declared artifact SHA-256 values. The repository checkout helper created a fresh clean checkout of the exact canonical head. The substantive implementation delta changes only `diagnostics/m4_tokenizer_materialization.py` and `tests/test_m4_tokenizer_materialization.py`; the following two commits add only the formal handoff and manifest.

## Versioned-law fidelity

The specification's P1, P2, and P3 quotation matches `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1. The implementation delta changes no constitution, specification, contract, schema, scientific identity, source-class tag, STATE, provenance, or ledger artifact. No law reconstruction, bar laundering, threshold change, or unauthorized gate claim was found.

**LAW_FIDELITY: CLEAR.**

## Independent implementation and regression review

BF3's ordinary second-replacement interruption cases now return the new JSON to `.incomplete`, preserve both incomplete evidence files, and restore a prior pair through replacement staging. BF5 now derives weight kind and size from one `os.lstat` observation without opening the weight. The constructor file is hashed before environment lookup. The ten ordered pre-import NF2 negative realizations, wrapper order, exact normative identities, commands, pinned image controls, positive construction, and public field restrictions remain unchanged.

The exact OCI command is correctly pinned to the Linux/amd64 digest with `--pull=never`, `--network none`, a read-only repository, no custody mount or environment during tests, and isolated `python3`. Docker is unavailable on the CRITIC host, so the claimed pinned-container 26/26 run could not be independently repeated here. The unchanged wrapper was invoked with host isolated Python, but the host lacks the pinned image's `jsonschema` dependency; its resulting import error is an environment limitation and is not package evidence.

## Batched blocking findings

### CR-BF1 — Missing or invalid request does not produce the governed BLOCKED result

`materialize` loads the request before entering any governed authority projection. An absent, unreadable, digest-mismatched, duplicate-member, or noncanonical request is caught by the generic exception branch while `request` is still `None`; it returns exit `3` and creates no result artifact. A direct no-custody realization with a missing contract independently reproduced `exit=3` and `artifact=false`. This contradicts the binding rule that a pre-access missing authority/handle/contract is BLOCKED and BF1's requirement that every governed pre-publication failure produce the sanitized schema-valid projection. The remediation therefore leaves a bare-return path that BF1 was specifically intended to remove.

### CR-BF2 — Constructor mismatch has the wrong status, exit, and terminal check

The constructor byte digest is now evaluated before custody lookup, but the failure is raised as `GovernedFailure("AUTHORITY", "CONSTRUCTOR_IDENTITY_MISMATCH", True)`. Independent no-custody execution reproduced status `BLOCKED`, exit `2`, and terminal check `AUTHORITY`. The binding executable-package rule says BLOCKED applies only to authority/handle failures; constructor identity is its own ordered check and later governed failures are FAIL. The result must therefore terminate at `CONSTRUCTOR_IDENTITY` with `CONSTRUCTOR_IDENTITY_MISMATCH`, status `FAIL`, and exit `3`, while retaining the required pre-custody evaluation order.

### CR-BF3 — The selected suite still does not realize the complete binding negative matrix

The module contains 26 test methods, but the added coverage does not execute the complete cases required by §7 and `m4_tokenizer_materialization_test_contract_v1.json`. `test_failure_projection_covers_every_governed_code` directly constructs results rather than reaching those failures through `materialize`; `test_private_numeric_hash_and_extra_rejected` only validates two schema objects; and the synthetic materializer tests cover PASS, non-unique insertion, and one stop mismatch. There are no direct `materialize` realizations for the required wrong repository/revision/quantization identities; absent, linked, noncanonical, duplicate-member, extra-field, stale, or schema-invalid custody records; tokenizer/config name, size, digest, or Git-blob mismatches; missing/null/non-string/unequal chat templates; multi-token neutral fragment; each of the three encode/decode ordinals; duplicate/reordered stop sources; serialization ambiguity; or alternate loading/runtime failures. The suite can pass while those mappings regress, as the two incorrect governed projections above demonstrate.

These are one integrated executable-package remediation batch. No serial one-finding route is requested.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**
**COMBINED DISPOSITION: BLOCK.**

BF3's tested interruption scenario and BF5's single-`lstat` observation are resolved, and the NF2/positive package remains preserved. BF1/BF4 failure semantics and BF2's complete binding coverage are not closed.

**Exact next authorized route:** WORKFLOW COORDINATOR returns this single batched BLOCK for integrated remediation. No direct role-to-role transfer is made by this review.

**Explicitly prohibited actions:** custody lookup; model/tokenizer access; OCI materialization; retry or fallback; inference/serving; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; merge; publication; rerun; or gate decision. The single materialization operation remains **UNCONSUMED**.

## Public-repository safety

Public-safety preflight: same-checkout `workflow_preflight.py --repo-root` with gitleaks `8.30.1`, complete resulting-file scanning, and added-line patch scanning returned two duplicate-domain `personal_contact` findings. Both matches occur wholly inside the required immutable public base commit on line 14; manual inspection classifies them as public reproducibility metadata, not personal-contact data. Gitleaks returned zero findings, and manual review found no custody/model/tokenizer data, private path, credential, task identifier, protected seed, scientific output, or prohibited durable-state mutation. The scanner findings are explicitly retained and classified, not silently suppressed.
