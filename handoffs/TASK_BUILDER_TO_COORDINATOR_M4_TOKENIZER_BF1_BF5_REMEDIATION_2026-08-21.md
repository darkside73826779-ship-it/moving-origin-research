# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER BF1–BF5 REMEDIATION

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

**Gate served:** One-batch BF1–BF5 executable-package remediation before persistent-CRITIC review

## Canonical intake

- ARCHITECT substantive input: `architect/m4-tokenizer-executable-package-remediation` at `bdbc1ad0eead7ff8dafd5e38b667f5a5810b5212`.
- Review result: `0a8c738d6b730f4f2da9fcd333e68467bd669158`.
- Input base: `47e06c361c361843916668304432f7a748ac514e`.
- Canonical manifest: `architect/m4-tokenizer-executable-package-remediation-manifest` at `66af3ff9fd1a039004b3c6aeb9d86703317d1740`.
- Work branch: `taskbuilder/m4-tokenizer-bf1-bf5-remediation`.

The incoming manifest and every inventoried raw committed Git-blob SHA-256 were independently verified before editing.

## Integrated correction

### BF1 — Governed failure artifacts

- Added schema-valid sanitized BLOCKED/FAIL result construction.
- Every result contains no partial arrays, the exact ordered check prefix, earlier PASS rows, one terminal FAIL row, the exact failure code, and no later rows.
- Authority and handle failures return BLOCKED/exit 2; later governed failures return FAIL/exit 3.
- Unexpected governed exceptions publish sanitized `INTERNAL_ERROR` evidence when safe.

### BF2 — Complete non-custody synthetic suite

- Expanded the selected singleton test module from 19 to 26 tests.
- Tests now invoke `materialize` through authority, handle, constructor, weight, synthetic PASS, constructor-invariant, and stop-array paths without routed custody.
- Added schema validation of every governed failure projection and retained the full ten-case pre-import runtime snapshot matrix.
- Synthetic files and injected tokenizer objects exist only in private temporary test directories; no routed custody environment or model/tokenizer bytes are used.

### BF3 — Atomic pair recovery

- On second-replacement interruption, the new JSON is returned to `.incomplete` evidence.
- With no prior pair, neither final JSON nor final sidecar remains.
- With a prior pair, both prior files are restored through replacement staging while both new `.incomplete` files remain for review.
- Added separate tests for interruption with and without a previous valid pair.

### BF4 — Constructor digest before custody

- The materializer now hashes `specs/data/m4_context_format_probe_contract_v1.json` and reproduces the fixed constructor SHA-256 before reading the custody environment variable.
- A mismatch produces governed `CONSTRUCTOR_IDENTITY_MISMATCH` evidence without custody lookup.

### BF5 — One weight `lstat` observation

- Weight regular-file kind and schema-bound byte count are derived from one `os.lstat` result.
- The weight file is never opened, and no link-following `is_file` or `stat` call is used for that decision.
- A synthetic test proves exactly one weight-path `lstat` observation.

## Files changed

- `diagnostics/m4_tokenizer_materialization.py`
- `tests/test_m4_tokenizer_materialization.py`

No specification, contract, schema, constructor, OCI launch contract, scientific artifact, custody record, STATE, provenance, or ledger file changed.

## Verification

- Result commit: `03cf97e0a8af4869a9cffe609c92f3896d30b62d`.
- Fresh workflow-helper-created exact-SHA checkout: clean.
- `.gitattributes` and `tests/__init__.py`: `text: set`, `eol: lf`.
- OCI image: exact Linux/amd64 manifest digest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`.
- Prescribed container controls: `--pull=never`, `--network none`, read-only repository, no custody mount, no custody environment, no writable output mount, bounded private tmpfs.
- Exact command: `python3 -I tests/run_m4_tokenizer_materialization_tests.py`.
- Result: 26 tests run, 26 passed, exit 0.

## Preserved boundaries

- The single materialization operation remains **UNCONSUMED**.
- No routed custody lookup, custody/model/tokenizer access, OCI materialization, retry, fallback, inference, serving, Q2/EF3, qualification, scoring, protected seeds, science, STATE/provenance mutation, merge, or gate decision occurred.
- No Workflow Efficiency maintenance was opened.

## Route

**Exact next recipient:** WORKFLOW COORDINATOR, then one persistent-CRITIC review of the integrated BF1–BF5 package.

**Explicitly prohibited:** materializer launch, custody/model/tokenizer access, retry, inference/serving, qualification, scoring, protected seeds, science, durable-state mutation, merge, or gate decision.
