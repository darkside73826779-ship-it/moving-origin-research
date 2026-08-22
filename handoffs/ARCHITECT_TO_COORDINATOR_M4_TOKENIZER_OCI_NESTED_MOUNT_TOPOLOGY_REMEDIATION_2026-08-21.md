# FORMAL RETURN — ARCHITECT → WORKFLOW COORDINATOR — M4 TOKENIZER OCI NESTED-MOUNT TOPOLOGY REMEDIATION

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

## Authority and observed failure

- Private-binding re-release: `coordinator/m4-tokenizer-private-binding-rerelease` at `a4d780b11c9719df77acd320212a296542e5871a`.
- TASK BUILDER failure routing head: `taskbuilder/m4-tokenizer-private-binding-materialization-execution` at `1f0f41b42e28b0edb8397db3681131755163f7b7`; substantive failure result `79fb90382a17087594f4ec9c81651fa3c02b6075`.
- Durable official WSL2 pre-execution test-bed authority and reproducibility lock: `coordinator/m4-wsl2-preexecution-testbed` at `1ee4a004bab575757e91918c5ef7c0ef694fddf7`.
- Single materialization operation: **UNCONSUMED**.

The released checkout lacked `artifacts/m4_tokenizer_materialization/`. With `/workspace` already mounted read-only, the OCI engine could not create the nested output destination and exited `125` before container creation. The stage remained empty; no materializer process or custody access occurred.

## Batched topology correction

1. Added the exact inert tracked marker `artifacts/m4_tokenizer_materialization/.gitkeep`: regular Git mode `100644`, `0` raw bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
2. Preserved repository-read-only first and nested-output-writable second. The empty private stage bind hides the marker; allowed stage files remain only `tokenizer_materialization.json` and its sidecar.
3. Added an exact mandatory custody-free mount-smoke gate before the no-custody wrapper and before any materializer release: pinned image, `--pull=never`, Linux/amd64, `--network none`, read-only root, dropped capabilities, no-new-privileges, repository bind then nested stage bind, bounded private tmpfs, `/bin/true`, no custody mount/environment, expected exit `0`, empty stage, clean checkout.
4. Bound absent marker, reversed mount order, nonempty post-smoke stage, or any nonzero result to `RUNTIME_IDENTITY_MISMATCH_NO_CUSTODY_NO_CONSUMPTION_STOP_NO_RETRY`.
5. Reconciled the OCI contract, test contract, selected static topology test, executable-package inventory, all adjacent sidecars, specification, and changelog in one batch.

## Complete executable-package raw identity table

| Ordinal | Role | Path | Git mode | Raw bytes | SHA-256 |
|---:|---|---|---:|---:|---|
| 0 | checkout identity | `.gitattributes` | `100644` | 2391 | `68c528ede67720007d4ec15d15f6d723136a24b9a4662c94ad9cdfbbc158601d` |
| 1 | nested output mountpoint marker | `artifacts/m4_tokenizer_materialization/.gitkeep` | `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | materializer | `diagnostics/m4_tokenizer_materialization.py` | `100644` | 21096 | `90e89b5a55ff80041a8e09c0d3e96208b6d8eff5c6b39eecd6366a1afb5289af` |
| 3 | constructor contract | `specs/data/m4_context_format_probe_contract_v1.json` | `100644` | 1821 | `eab77b9f44a4e9378f5889f5aa368eabd87959a5ddafab9ca38685228f12feec` |
| 4 | test contract | `specs/data/m4_tokenizer_materialization_test_contract_v1.json` | `100644` | 7672 | `596e028a61475227f10dd2379c19a8d8322eadeabd033b60d67a64ce3df95f3c` |
| 5 | OCI launch contract | `specs/data/m4_tokenizer_oci_launch_contract_v1.json` | `100644` | 5387 | `5cf1b86f281651d4724bc621878a9e5c1e8185b992e4fd28df3e24dbeeb64dd1` |
| 6 | test package marker | `tests/__init__.py` | `100644` | 69 | `6f56eb2128751f0c5c1ab27ff461b38565aa00a3dcd29c04ab8bd56c34f4a961` |
| 7 | pre-import test wrapper | `tests/run_m4_tokenizer_materialization_tests.py` | `100644` | 9062 | `29dc1c0d83e71c850e9eb3c423cfd359a6c557956d1eab1fa5d9beb049271d1d` |
| 8 | selected test module | `tests/test_m4_tokenizer_materialization.py` | `100644` | 56713 | `2203c36331f083ad9ab6d241b51a8b5e2cd8d75eb7c75365609ea9ab6aa39f49` |

All nine package entries independently match the exact Git blobs and modes. The package is `1950` LF bytes, SHA-256 `d9f464db598c8e95c8ee8e7e7cce49f3fd9574235cd2fad9799650d7f4da0546`; its adjacent sidecar matches those complete bytes.

## Negative evidence and active-binding sweep

- At the released input SHA, `git cat-file` and `git ls-tree` prove the marker path and its parent directory were absent.
- The incoming failure record proves repository-first read-only plus absent nested destination yielded engine exit `125` before process start; the private stage stayed empty.
- The feasibility record proves precreating the destination and using the identical custody-free mount topology with `/bin/true` exited `0` and left the stage empty.
- Static contract coverage now requires the marker identity, repository-before-nested-output order, no custody mount/environment, exact `/bin/true`, empty-stage success, and deterministic absent-marker/reordered-mount/nonempty-stage failures.
- Every active mount/output-stage binding in the OCI contract, test contract, package, selected test, specification, request output path, wrapper path, and sidecars was inspected. Superseded package/test/OCI sizes and digests occur only in preserved historical records and the changelog, not active governed inputs.

## Authorized verification

- Exact custody-free pinned-image mount smoke: PASS, exit `0`, stage empty, checkout clean before and after.
- Exact pinned-image, network-disabled, repository-read-only no-custody wrapper: **35/35 PASS**, exit `0`.
- The first test-bed pass caught a Windows-mounted permission-presentation mismatch (`0777` in WSL versus tracked Git mode `100644`). The test was corrected to validate Git mode as governed contract metadata while checking the mounted file for regular/non-link/empty-byte identity. The complete exact suite then passed.
- No materializer invocation occurred.

## Preserved holds

No materializer retry, custody/model/tokenizer access, inference/serving, qualification, diagnostics/scoring, protected seeds, science, STATE/provenance mutation, publication, merge, or gate decision occurred or is authorized. The operation remains **UNCONSUMED**.

**Exact next recipient:** WORKFLOW COORDINATOR for one persistent-CRITIC review of this exact package.
