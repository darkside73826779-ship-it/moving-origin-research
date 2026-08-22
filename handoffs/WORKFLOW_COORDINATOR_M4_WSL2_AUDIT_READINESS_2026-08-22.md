# WORKFLOW COORDINATOR M4 WSL2 Audit-readiness Return

**Date:** 2026-08-22

**Regime:** B

## Immutable inputs and result

- Immutable base: annotated tag `m4-wsl2-preexecution-testbed-v1.2`, tag
  object `1994709b41c8e108e0b6f9a15936681f596823af`, peeled commit
  `11ea682a7f0fadfa1437a12d882402d90ffd0579`.
- Substantive result branch:
  `coordinator/m4-wsl2-testbed-audit-readiness`.
- Substantive result commit:
  `52a399d108d0dc80759a0477816644362278ba20`.
- Recommended future immutable tag:
  `m4-wsl2-preexecution-testbed-v1.3`. No tag was created.

## Narrow result

The v1.2 dependency lock, setup scripts, governed image identity, and measured
30-second dual-instance diagnostic remain unchanged. This update closes only
the residual audit-hygiene gaps:

1. Active setup/runbook citations use the immutable v1.2 annotated tag object
   and peeled commit. The v1.1 crash-cart citation remains as immutable
   historical provenance.
2. A custody-free one-command readiness gate validates the existing diagnostic
   dependency lock, immutable checkout, LF/sidecar discipline, V1 compatibility,
   exact WSL/GPU/Docker/toolkit/OCI identities, focused public tests, and a
   mount-free/no-network/read-only GPU visibility smoke.
3. A deterministic sanitized report schema and BLOCKED construction example
   bind the report surface. They contain no private root, prompt, rendered text,
   token array, seed value, scoring input, or machine-private value.
4. A future downloadable bundle must be tag-derived and carry both the exact
   archive-byte SHA-256 and a canonical LF inventory-manifest SHA-256. No bundle
   is published by this result.

## Exact artifact identities

- Readiness command SHA-256:
  `9e045b1c40721619be23021c368ed7024fa4724f01fd7d423c9ac950bd242db4`.
- Focused test SHA-256:
  `19cad7a88561500bf408a3a6b6dc2f0e60a27e68a2976f77cb8f723f33a5f5aa`.
- Readiness contract SHA-256:
  `1fd9fc11c50c143151a27f615418d65e2216505441d3cf02c85cdca2c8f8876f`.
- Report schema SHA-256:
  `eff3e2a09145defa7831024d2ba8004f706b3cea596ffde40f875feedac146a1`.
- BLOCKED example SHA-256:
  `9a7576530270011d7dc68d63c887bd4a4f26620cedc8ba18e26f418ce1247c9e`.

## Verification and measured limitation

- `python -m py_compile tools/testbed/run_m4_wsl2_audit_readiness.py tests/test_m4_wsl2_audit_readiness.py`: PASS.
- Focused tests in the pinned governed OCI Python/jsonschema runtime: 8/8 PASS.
- Standalone governed-image GPU smoke with pull disabled, network none,
  read-only root, no repository/custody/model mounts: PASS; exact observed public
  runtime `torch 2.8.0+cu128`, GPU `NVIDIA GeForce RTX 5080`.
- Fresh native-WSL checkout at the substantive result: immutable tag, checkout,
  LF/sidecar, and Python 3.12.3 checks PASS. The default WSL system interpreter
  then stopped fail-closed at `PYTHON_PACKAGE_VERSION_MISMATCH`: it has
  jsonschema 4.10.3 and lacks the remaining locked diagnostic packages. No
  package installation or network access was attempted. Operators must first
  recreate and activate the already-committed exact diagnostic environment;
  the result does not pretend the default interpreter is ready.

This is diagnostic/non-scientific infrastructure only. No custody lookup,
model or tokenizer access, serving, inference, materialization, protected seed,
scoring, STATE/provenance mutation, merge, gate decision, or tag creation
occurred.
