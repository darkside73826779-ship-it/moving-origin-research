# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER MATERIALIZATION FAIL

**Date:** 2026-08-21

**Regime:** B

**Status:** FAIL

**Materializer exit:** `3`

**Governed failure:** `CONSTRUCTOR_INVARIANT_FAILURE` at `ARRAY_1024`

## Canonical intake

- Topology-clear re-release: `coordinator/m4-tokenizer-topology-clear-rerelease` at `5e6a6eb4d7de5c634c5b9a5881076d066c397c7c`.
- Cleared package: `architect/m4-tokenizer-cr-mnt3-identity-reconciliation` at `522b01d42ceef90ee2390c169f29fb163e610470`.
- Package result: `f845e9e4390c16f28f305b1394f0a84704e8721d`.
- Persistent-CRITIC COMBINED CLEAR: `critic/m4-tokenizer-cr-mnt3-final-identity-rereview` at `41d844063416b68090c933a76f31e82c4d83e458`.
- Official WSL2 test bed: `coordinator/m4-wsl2-preexecution-testbed` at `0631a019a153ec89312938982c007cf94dd3f03e`, tag `m4-wsl2-preexecution-testbed-v1.1`.
- Work branch: `taskbuilder/m4-tokenizer-topology-clear-materialization-execution`.

## Terminal execution result

Every committed pre-operation gate passed in the required order. TASK BUILDER then started exactly one materializer invocation using the exact pinned image, immutable checkout, private binding, and committed launch command. The process returned exit `3` and atomically published the exact two-file sanitized pair.

The result records ordered PASS checks `AUTHORITY`, `CUSTODY_HANDLE`, `CUSTODY_ATTESTATION`, `TOKENIZER_ORIGINAL`, `TOKENIZER_COPY`, `CONSTRUCTOR_IDENTITY`, `BASE_TEMPLATE`, `INSERTION_UNIQUENESS`, and `NEUTRAL_FRAGMENT`, followed by FAIL at `ARRAY_1024`. The governed failure code is `CONSTRUCTOR_INVARIANT_FAILURE`. The arrays field is empty; no complete token arrays or private values are present.

The canonical result SHA-256 is `10a14c1a4f7b257aa195636ab86b7a85a68fc084af13bead7b5d4b3ecfa55728`.

No retry, fallback, alternate runtime, alternate topology, alternate custody root, or additional diagnostic execution occurred. The single operation is **CONSUMED**.

## Requirement → production/gate → evidence trace

| Requirement | Production/gate branch | Evidence | Disposition |
|---|---|---|---|
| Fresh immutable released checkout | helper-created checkout at exact release SHA | clean checkout at `5e6a6eb4d7de5c634c5b9a5881076d066c397c7c`; `git fsck --full --strict` PASS | PASS |
| Exact cleared executable package | raw Git-blob byte-count, mode, and SHA-256 comparison | all nine entries and package sidecar match, including the zero-byte mode-100644 mount marker | PASS |
| Exact pinned runtime and image | WSL2-backed Docker and local image inspection | client/server `29.1.3`, `linux/amd64`, exact platform digest, pull disabled | PASS |
| Exact no-custody wrapper first | pinned network-disabled read-only production wrapper | 35 tests run, 35 passed, exit `0` | PASS |
| Exact custody-free topology matrix second | committed four-case runner | positive, absent-marker, reversed-order, and nonempty-stage cases matched; cleanup complete; exit `0` | PASS |
| Private binding and output-stage preconditions | presence, canonical kind, fixed-record kind, distinct empty stage | passed without publishing private values | PASS |
| Exactly one materializer invocation | exact committed production command | process started once; exit `3`; no retry | PASS |
| Governed constructor checks | production materializer ordered checks | checks 0–8 PASS; `ARRAY_1024` FAIL with `CONSTRUCTOR_INVARIANT_FAILURE` | FAIL |
| Atomic sanitized publication | schema, canonical JSON, sidecar, file-kind, and public-safety validation | exactly two regular non-link files; schema-valid canonical JSON; matching sidecar; exact-byte repository copy | PASS |

## Ordered execution and access trace

`release/identity verification → no-custody wrapper 35/35 PASS → topology matrix PASS and cleanup → private root/record kind verification → empty distinct output stage → single materializer start → authority and custody checks PASS → tokenizer original/copy checks PASS → constructor/base/insertion/neutral checks PASS → ARRAY_1024 FAIL → atomic sanitized pair publication → schema/canonical/sidecar/public-safety validation → exact-byte repository copy → STOP`

No inference, serving, qualification, diagnostics/scoring, protected seeds, Q2/EF3, scientific execution, STATE/provenance mutation, model/tokenizer publication, merge, rerun, or further operation occurred.

## Published artifacts and route

- `artifacts/m4_tokenizer_materialization/tokenizer_materialization.json`
- `artifacts/m4_tokenizer_materialization/tokenizer_materialization.json.sha256`
- This formal return and its canonical manifest.
- **Exact next recipient:** WORKFLOW COORDINATOR for routing of the exact sanitized execution package to the authoritative persistent CRITIC for independent execution review.
