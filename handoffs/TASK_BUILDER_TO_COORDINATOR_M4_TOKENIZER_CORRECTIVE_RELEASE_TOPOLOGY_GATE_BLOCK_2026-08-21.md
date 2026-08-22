# TASK BUILDER → WORKFLOW COORDINATOR — M4 Corrective Release Topology-gate BLOCK

**Date:** 2026-08-21 EDT
**Regime:** B
**Terminal state:** **BLOCK**
**Governed mapping:** `RUNTIME_IDENTITY_MISMATCH_NO_CUSTODY_NO_CONSUMPTION_STOP_NO_RETRY`
**Failure class:** `TOPOLOGY_ABSENT_MARKER_FIXTURE_STALE_OUTPUT_CONFLICT`

## Immutable intake

- Corrective release: `coordinator/m4-tokenizer-private-binding-corrective-release @ 1e2e910adff95ce47bcbef1c28eff8213b71acae`
- New-operation release: `coordinator/m4-tokenizer-full-domain-new-operation-release @ ec3226f9d95aae28b813abf011b2a0f3b267f9e6`
- Corrected package: `taskbuilder/m4-tokenizer-full-token-id-domain-remediation @ 9d3e123948dfdca111dc730501475ed875abb00a`
- Persistent-CRITIC COMBINED CLEAR: `critic/m4-tokenizer-full-token-id-domain-rereview @ 482bdeceea8461438c516dcb8944bbaa21e5192c`
- Prior binding-absence BLOCK: `taskbuilder/m4-tokenizer-full-domain-new-operation-execution @ 242f33813f407e4528d75be37ab5856208bc2192`
- Work branch: `taskbuilder/m4-tokenizer-private-binding-corrective-execution`

A fresh helper-managed checkout was created at the exact corrective release. The checkout remained immutable and clean throughout the governed gates.

## Gate result

The mandatory public gates ran in the committed order:

1. Raw committed package identities: **PASS** — all nine executable-package entries and five governed adjacent sidecars reproduced exactly.
2. WSL2-backed Docker identity: **PASS** — client/server `29.1.3`, `linux/amd64`, exact locally present platform image digest, pull disabled.
3. Exact pinned network-disabled, read-only, no-custody wrapper: **PASS** — 37 tests run, 37 passed, exit `0`.
4. Committed custody-free topology matrix: **BLOCK** during construction of the absent-marker negative fixture.

The topology runner's positive repository-then-nested-output case passed with an empty stage. The next case copies the released checkout, removes only `artifacts/m4_tokenizer_materialization/.gitkeep`, and then requires that directory to be removable. The corrective release necessarily preserves the historical consumed result pair in the same directory. The directory therefore remains nonempty and `rmdir` exits nonzero before the absent-marker Docker invocation.

This is a deterministic executable test-fixture incompatibility with the required preserved evidence, not a custody or model failure. The gate stopped fail-closed. No private binding was emitted or used, no custody root or record was accessed, and the materializer process did not start.

## Proposed minimal remediation and feasibility evidence

In the runner's disposable `mktemp` snapshot only, replace:

```bash
rm -f -- "$snapshot/artifacts/m4_tokenizer_materialization/.gitkeep"
rmdir -- "$snapshot/artifacts/m4_tokenizer_materialization"
```

with:

```bash
rm -rf -- "$snapshot/artifacts/m4_tokenizer_materialization"
```

This removes the entire copied output subtree from the disposable negative fixture, which directly realizes the contract's absent-marker/absent-mountpoint condition while leaving the immutable released checkout and preserved historical pair untouched.

TASK BUILDER tested only this one-line fixture correction in a disposable checkout at the exact release. `bash -n` passed, then all four custody-free topology cases passed with cleanup complete and the runner emitted `TOPOLOGY_SMOKE_MATRIX_PASS`. The disposable checkout was removed. This feasibility result is diagnostic only; it is not a governed execution retry and does not authorize modifying the released command.

## Ordered execution and zero-access trace

`fresh release checkout → raw identity PASS → exact OCI identity PASS → pinned no-custody wrapper 37/37 PASS → topology positive PASS/empty stage → absent-marker fixture construction encounters preserved historical pair → runner nonzero → STOP`

No private root/record verification, output stage for materialization, custody lookup, weight observation, tokenizer/config read or copy, loader import, `from_pretrained`, or materializer process occurred.

## Operation and route

The corrected new operation remains **UNCONSUMED**. The prior historical FAIL remains **CONSUMED** and unchanged. No retry, fallback, alternate runtime/topology/command, inference, qualification, scoring, protected seeds, science, STATE/provenance mutation, model/tokenizer publication, merge, or gate decision occurred.

Required next route: WORKFLOW COORDINATOR should route the exact fixture defect and tested minimal proposal through the established ARCHITECT → persistent-CRITIC correction path before any new exact execution release.
