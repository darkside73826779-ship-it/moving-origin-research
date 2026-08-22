# CRITIC Rereview — M4 Tokenizer CRITIC-BLOCK Remediation

**Date:** 2026-08-21
**Regime:** B
**Gate served:** One integrated independent rereview of the three findings in the authoritative M4 tokenizer BF1–BF5 remediation BLOCK.

## Canonical intake

- Canonical implementation branch/head: `taskbuilder/m4-tokenizer-critic-block-remediation` at `b30b20775b9c501766fc120b5d871124f8d88a18`.
- Implementation result: `92de5048df4ed9ac024567da6619ae9884ac3679`.
- Handoff result: `88a2555f4b1d22ce3b9a7d4c8f9d9edeb17a527f`.
- Prior authoritative review/BLOCK: `critic/m4-tokenizer-bf1-bf5-remediation-review` at `856cb4da1c1688f90cbd6d8c11ea0ef57b11978d`.

The committed common handoff manifest validated with `tools/workflow_contract_validator.py`. An independent raw `git cat-file blob` inventory reproduced all 22 declared artifact SHA-256 values. The repository checkout helper created a fresh clean checkout of the exact canonical head. The implementation delta changes only `diagnostics/m4_tokenizer_materialization.py` and `tests/test_m4_tokenizer_materialization.py`; its routing tail adds only the formal handoff and manifest.

## Law fidelity and preservation

The specification's P1, P2, and P3 quotation remains verbatim against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1. No constitution, specification, contract, schema, scientific identity, source-class tag, STATE, provenance, or ledger artifact changed. BF3 atomic-pair recovery and BF5's single-`lstat` weight observation remain unchanged. The ten ordered NF2 pre-import negatives, exact normative identities, wrapper order, commands, pinned image controls, positive construction, and public field restrictions remain preserved.

**LAW_FIDELITY: CLEAR.**

## Resolved prior findings

### Governed invalid-request evidence — RESOLVED

The materializer now loads the immutable committed authority request as the public projection basis and converts absent, unreadable, digest-mismatched, duplicate-member, and noncanonical routed requests to `AUTHORITY_MISSING`. Independent no-custody execution reproduced status `BLOCKED`, exit `2`, terminal check `AUTHORITY`, no arrays, and a schema-valid published pair.

### Constructor mismatch projection — RESOLVED

The committed constructor is still hashed before custody environment lookup. Independent no-custody execution reproduced status `FAIL`, exit `3`, failure code `CONSTRUCTOR_IDENTITY_MISMATCH`, and terminal check `CONSTRUCTOR_IDENTITY` at ordinal 5.

## Batched blocking finding

### CR-RBF1 — The complete named negative matrix is still not realized through `materialize`

The suite has 30 test methods and adds useful materializer-path coverage for four invalid-request forms, six public identity categories, tokenizer/config file rejection, six custody-record forms plus a linked record, three chat-template variants, multi-token neutral input, all three encode/decode ordinals, and three stop-source variants. That is material progress, but it does not close the prior authoritative finding or the current handoff's requirement that the complete named matrix be realized through `materialize`.

The binding test contract names `absent_empty_or_symlink_handle`, but `test_materialize_publishes_governed_blocked_results` exercises only an absent environment value; no empty value or symlink custody-root realization calls `materialize`. The named `noncanonical_array_serialization` and `forbidden_path_host_text_or_token_array_field` cases remain direct `load`, `validate`, `failure_result`, or `publish` tests rather than failures reached through `materialize`. The required alternate-loading/runtime case also remains a static OCI-token assertion; no materializer-path realization proves its governed mapping. Directly constructing a failure projection or calling a helper cannot prove that production control flow selects the required code, status, check prefix, and exit. The two incorrect mappings found in the prior review while those helper tests passed demonstrate why this distinction is binding.

This is one residual coverage/executability finding and must be remediated as one batch; no serial finding loop is requested.

## Executability evidence

The exact OCI test command remains pinned to the declared Linux/amd64 digest with `--pull=never`, `--network none`, a read-only repository, no custody mount or environment, isolated `python3`, and the unchanged wrapper. Docker is unavailable on the CRITIC host, so the reported pinned-container 30/30 run could not be independently repeated. The available host interpreter lacks the pinned image's `jsonschema` dependency; that host limitation is not used as package evidence. Targeted no-custody calls with an isolated stub validator were used only to verify the two corrected control-flow projections above and accessed no custody/model/tokenizer data.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**
**COMBINED DISPOSITION: BLOCK.**

The first two prior findings are resolved, and BF3/BF5 plus banked evidence remain preserved. The complete named negative-matrix requirement is not closed.

**Exact next authorized route:** WORKFLOW COORDINATOR returns this single batched BLOCK for integrated remediation. No direct role-to-role ownership transfer is made by this review.

**Explicitly prohibited actions:** custody lookup; model/tokenizer access; OCI materialization; retry or fallback; inference/serving; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; merge; publication; rerun; or gate decision. The single materialization operation remains **UNCONSUMED**.

## Public-repository safety

Public-safety preflight: same-checkout `workflow_preflight.py --repo-root` with gitleaks `8.30.1`, complete resulting-file scanning, added-line patch scanning, and manual review returned zero findings. No custody/model/tokenizer data, private path, credential, task identifier, protected seed, scientific output, or prohibited durable-state mutation was introduced or accessed.
