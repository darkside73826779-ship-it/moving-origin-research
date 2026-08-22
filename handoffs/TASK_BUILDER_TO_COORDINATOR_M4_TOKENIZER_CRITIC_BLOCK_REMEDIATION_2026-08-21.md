# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER CRITIC BLOCK REMEDIATION

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

**Gate served:** One integrated CRITIC-block remediation before one persistent-CRITIC rereview

## Canonical intake

- Authoritative CRITIC BLOCK: `critic/m4-tokenizer-bf1-bf5-remediation-review` at `856cb4da1c1688f90cbd6d8c11ea0ef57b11978d`.
- Reviewed input: `taskbuilder/m4-tokenizer-bf1-bf5-remediation` at `b4837b6af3310afac36ff343e58490756cdf54cb`.
- Prior implementation result: `03cf97e0a8af4869a9cffe609c92f3896d30b62d`.
- Work branch: `taskbuilder/m4-tokenizer-critic-block-remediation`.

## Integrated correction

- Missing, unreadable, digest-invalid, duplicate-member, and noncanonical routed requests now publish the schema-valid sanitized pre-access `BLOCKED` projection with `AUTHORITY_MISSING` and exit 2.
- Constructor digest mismatch remains evaluated before custody lookup but now terminates at `CONSTRUCTOR_IDENTITY` as `FAIL`, with `CONSTRUCTOR_IDENTITY_MISMATCH` and exit 3. Only authority and handle failures remain `BLOCKED`.
- The selected suite now invokes `materialize` across request rejection, custody-attestation forms, repository/revision/quantization/weight/tokenizer/config identity mismatch, tokenizer/config byte mismatch, chat-template mismatch, multi-token neutral fragment, each encode/decode ordinal, and stop-source variants.
- Custody identity comparisons now retain their specific governed failure mapping before schema validation; malformed, extra, stale, or otherwise schema-invalid attestation remains `CUSTODY_ATTESTATION_INVALID`.
- BF3 atomic pair recovery, BF5 single-`lstat` weight observation, the pre-import runtime matrix, and all banked package evidence remain preserved.

## Files changed

- `diagnostics/m4_tokenizer_materialization.py`
- `tests/test_m4_tokenizer_materialization.py`

No specification, contract, schema, OCI launch contract, scientific artifact, custody record, STATE, provenance, or ledger file changed.

## Verification

- Implementation result: `92de5048df4ed9ac024567da6619ae9884ac3679`.
- Fresh workflow-helper-created exact-SHA checkout: clean.
- Exact Linux/amd64 pinned image digest: `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`.
- Prescribed no-custody controls: `--pull=never`, `--network none`, read-only repository, no custody mount or environment, no writable output mount, bounded private tmpfs.
- Exact command: `python3 -I tests/run_m4_tokenizer_materialization_tests.py`.
- Result: 30 tests run, 30 passed, exit 0.

## Preserved boundaries

- The single materialization operation remains **UNCONSUMED**.
- No routed custody lookup, custody/model/tokenizer access, OCI materialization, retry, fallback, inference, qualification, scoring, protected seeds, science, STATE/provenance mutation, merge, publication, or gate decision occurred.
- No Workflow Efficiency work was opened.

## Route

**Exact next recipient:** WORKFLOW COORDINATOR, then one persistent-CRITIC rereview of this integrated package.

**Explicitly prohibited:** materializer launch, custody/model/tokenizer access, retry, inference/serving, qualification, scoring, protected seeds, science, durable-state mutation, merge, publication, or gate decision.
