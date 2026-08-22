# ARCHITECT → WORKFLOW COORDINATOR — M4 Topology Absent-Marker Fixture Reconciliation

**Date:** 2026-08-21 EDT  
**Regime:** B  
**Terminal state:** **COMPLETE**

## Intake and scope

- Input release: `coordinator/m4-tokenizer-private-binding-corrective-release @ 1e2e910adff95ce47bcbef1c28eff8213b71acae`.
- Authoritative BLOCK: `taskbuilder/m4-tokenizer-private-binding-corrective-execution @ 960a988f08e029e5e89913a6a744145c52481baf`.
- Sanitized result: `e391c0d681c780993f2516590c55075ba1bd7827`.
- Correction is confined to construction of the custody-free absent-marker negative in a disposable snapshot.

## Exact correction

The runner now deletes the copied snapshot subtree with exact command `rm -rf -- "$snapshot/artifacts/m4_tokenizer_materialization"`. It no longer removes only `.gitkeep` and then applies `rmdir`. The source checkout remains immutable, and the preserved historical result pair remains byte-identical. Runner identity is Git mode `100755`, 4,330 raw LF bytes, SHA-256 `860cf3a7522e0c9806c100fdb4d61b47b9c98f7fdb74a0fe62f672c253a2dfde`.

The OCI contract, test contract, static regression, executable-package inventory, sidecars, and normative specification bind the same whole-subtree disposable-snapshot construction. Wrapper-before-smoke order, positive case, reversed-mount negative, nonempty-stage negative, cleanup, zero-access assertions, failure mapping, and no-retry behavior are unchanged.

## Verification

- `bash -n tools/testbed/run_m4_tokenizer_topology_smoke_matrix.sh`: PASS.
- Focused contract/static topology test within the 37-test WSL host run: PASS.
- The full host run was not accepted as governed OCI evidence: 23 tests passed and 14 tests were blocked by the unpinned host environment (missing `transformers` metadata and release-runtime identity differences). No OCI or materializer command was run.
- JSON canonical byte form, all three adjacent sidecars, package entries, runner exact command, forbidden stale construction, `git diff --check`, workflow preflight, Git integrity, and remote equality are required before delivery.

## Complete changed-byte inventory

| Path | Mode | Bytes | SHA-256 |
|---|---:|---:|---|
| `specs/data/m4_tokenizer_executable_package_v1.json` | `100644` | 1948 | `bf1a99cb6d3047a8dafed9a56031b7254a881b0b09bb10b0d38f1318829d672d` |
| `specs/data/m4_tokenizer_executable_package_v1.json.sha256` | `100644` | 106 | `4f13b589bd3afe35d5f06f8987575a80d707b9f8ad24cc5ee3578ff4d6fa15e2` |
| `specs/data/m4_tokenizer_materialization_test_contract_v1.json` | `100644` | 8826 | `79aef0ab5c5b832868dedb0d5b61a6b11ee81c726fcf195d0e1c5d8f35a0eeaa` |
| `specs/data/m4_tokenizer_materialization_test_contract_v1.json.sha256` | `100644` | 117 | `88a63d36252ad31d0b85ca314a0644942601a6150fbd0f46427845e3b6ae5926` |
| `specs/data/m4_tokenizer_oci_launch_contract_v1.json` | `100644` | 6874 | `0a5d65e04c55896f603b3a9c611096a242f19b2e293ce356313a22c6e891d9c4` |
| `specs/data/m4_tokenizer_oci_launch_contract_v1.json.sha256` | `100644` | 107 | `b245473cec2bc3188c12266c1070468be607d869aeb4b3392c66b9c7765339e5` |
| `specs/m4_local_tokenizer_materialization_spec_v1.md` | `100644` | 33386 | `e0b660bc81b297ad8b7c0b7932076abab82349f1ad350c8c1f8934b1086c24f0` |
| `tests/test_m4_tokenizer_materialization.py` | `100644` | 65877 | `3930fdb47986850f4c6c47e5ec1479136c96b74ab51a1c46615591477fb58c1d` |
| `tools/testbed/run_m4_tokenizer_topology_smoke_matrix.sh` | `100755` | 4330 | `860cf3a7522e0c9806c100fdb4d61b47b9c98f7fdb74a0fe62f672c253a2dfde` |

Historical manifests, reviews, handoffs, changelog/provenance, and the consumed historical result pair are unchanged. The corrected new operation remains **UNCONSUMED**. No custody/model/tokenizer access, OCI/materializer execution, retry, scoring, seeds, science, durable-state mutation, publication, merge, or gate decision occurred.
