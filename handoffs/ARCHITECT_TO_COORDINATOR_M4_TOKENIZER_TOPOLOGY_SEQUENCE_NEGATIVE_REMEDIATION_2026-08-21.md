# FORMAL RETURN — ARCHITECT → WORKFLOW COORDINATOR — M4 TOPOLOGY SEQUENCE + NEGATIVE-EVIDENCE REMEDIATION

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

## Canonical intake

- Input topology package: `architect/m4-tokenizer-oci-nested-mount-topology-remediation` at `64f8010c26abbc6f47c0acb38916a756d9a09ede`.
- Authoritative CRITIC BLOCK: `critic/m4-tokenizer-oci-nested-mount-topology-rereview` at `732963988d051f4ce9f42ace2e0ce7118bf90780`.
- Official test-bed authority/tag: `coordinator/m4-wsl2-preexecution-testbed` at `0631a019a153ec89312938982c007cf94dd3f03e`, `m4-wsl2-preexecution-testbed-v1.1`.
- Single materialization operation: **UNCONSUMED**.

The banked zero-byte marker, nine package entries, positive mount topology, hidden-marker/empty-stage semantics, absent-marker exit-125 evidence, prior wrapper and positive-smoke results, no-stale-identity result, and authorized delta were preserved.

## CR-MNT1 — durable wrapper-first sequence

Every active sequence and success-projection binding now requires:

`VERIFY_FRESH_CHECKOUT_AND_IMAGE → RUN_PREIMPORT_TEST_WRAPPER → STOP_ON_NONZERO → RUN_CUSTODY_FREE_MOUNT_SMOKE → STOP_ON_NONZERO_OR_NONEMPTY_STAGE → SINGLE_MATERIALIZATION_RELEASE_CHECK`

- Wrapper exit `0` maps only to `PROCEED_TO_CUSTODY_FREE_MOUNT_SMOKE`.
- Smoke exit `0` plus empty stage maps only to `PROCEED_TO_SINGLE_MATERIALIZATION_RELEASE_CHECK`.
- Every other wrapper, engine, process, mount-order, or stage result stops fail closed with no retry and no consumption.
- Complete active-order sweep found **NO ACTIVE SMOKE-BEFORE-WRAPPER BINDING**. The prior return retains its superseded wording only as historical provenance.

## CR-MNT2 — exact custody-free production realizations

Added exact Git mode `100755` runner `tools/testbed/run_m4_tokenizer_topology_smoke_matrix.sh`, `4400` LF bytes, SHA-256 `a0f4383913a38cdde9f93947865d990e36b41fb538ff1468b121f4b1db2b137a`. `.gitattributes` binds its mounted bytes as `text eol=lf`.

The OCI/test contracts bind each exact test ID, command or sole command delta, engine result, relative stage evidence, terminal mapping, and cleanup:

| Case | Exact realization | Observed result | Governed mapping |
|---|---|---|---|
| `test_mount_smoke_positive_repository_then_nested_output` | repository read-only bind, then empty nested stage; `/bin/true` | exit `0`; stage empty | `PROCEED_TO_SINGLE_MATERIALIZATION_RELEASE_CHECK` |
| `mount_smoke_negative_absent_marker_engine_125` | exact positive command against custody-free snapshot with only tracked marker/directory absent | exit `125`; stage empty | `RUNTIME_IDENTITY_MISMATCH_NO_CUSTODY_NO_CONSUMPTION_STOP_NO_RETRY` |
| `test_mount_smoke_negative_nested_output_before_repository` | swap only the nested-output and repository mount pairs | exit `0`; stage empty | same fail-closed mapping regardless of engine exit |
| `test_mount_smoke_negative_nonempty_stage_after_smoke` | exact positive smoke, then inject fixed zero-byte `unexpected-after-smoke.txt` before governed postcheck | exit `0`; exact singleton observed; fixture removed; stage empty | same fail-closed mapping |

The runner explicitly unsets custody coordination and contains no custody mount/record, materializer command, model/tokenizer access, private path output, retry, or consumption. All temporary snapshots, stages, engine stderr, and the public sentinel are removed deterministically.

## Official test-bed evidence — exact production order

1. Exact pinned-image, network-none, repository-read-only no-custody wrapper: **35/35 PASS**, exit `0`.
2. Positive smoke and all three topology negatives: **PASS** with the exact results in the table.
3. Matrix terminal assertions: `custody_environment=false`, `custody_mount=false`, `custody_record=false`, `model_tokenizer_access=false`, `materializer_started=false`, `operation_consumed=false`, `retry=false`, `cleanup=complete`.
4. Checkout clean before and after the complete sequence.

## Complete nine-entry executable-package identity table

| Ordinal | Path | Mode | Raw bytes | SHA-256 |
|---:|---|---:|---:|---|
| 0 | `.gitattributes` | `100644` | 2459 | `998b713a5094f924efa62fc0c65f1195f385ea08476ee1d150ea2527d6e04c4c` |
| 1 | `artifacts/m4_tokenizer_materialization/.gitkeep` | `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | `diagnostics/m4_tokenizer_materialization.py` | `100644` | 21096 | `90e89b5a55ff80041a8e09c0d3e96208b6d8eff5c6b39eecd6366a1afb5289af` |
| 3 | `specs/data/m4_context_format_probe_contract_v1.json` | `100644` | 1821 | `eab77b9f44a4e9378f5889f5aa368eabd87959a5ddafab9ca38685228f12feec` |
| 4 | `specs/data/m4_tokenizer_materialization_test_contract_v1.json` | `100644` | 8648 | `561bae3e04ce81422b73601b0ae9e6835522919dc10e340fcc39e4b03791a1c2` |
| 5 | `specs/data/m4_tokenizer_oci_launch_contract_v1.json` | `100644` | 6529 | `ca465aa11dbafff74a62126c3e263dda547796cd9003983c93a015ae74bca0e9` |
| 6 | `tests/__init__.py` | `100644` | 69 | `6f56eb2128751f0c5c1ab27ff461b38565aa00a3dcd29c04ab8bd56c34f4a961` |
| 7 | `tests/run_m4_tokenizer_materialization_tests.py` | `100644` | 9062 | `4f4aa5a873f59c3dbc368c550a84f61564c181f5570fdbcb2e54b6b8f8f8d734` |
| 8 | `tests/test_m4_tokenizer_materialization.py` | `100644` | 58906 | `79f319c9dcb7129332f4cc03d47415b1d2cbb2d3e4a993f20bf73e899f3da0ea` |

All nine raw identities and modes reproduce exactly. The reconciled package is `1950` LF bytes, SHA-256 `1f726f6a01cae44595beafcf96baa8c6fded3263173d9a4dcfbc2a6c4681c4d4`; its sidecar matches.

## Preserved holds

No materializer retry, custody/model/tokenizer access, inference/serving, qualification, diagnostics/scoring, protected seeds, science, STATE/provenance mutation, publication, merge, or gate decision occurred. The single operation remains **UNCONSUMED**.

**Exact next recipient:** WORKFLOW COORDINATOR for one persistent-CRITIC rereview of this exact package.
