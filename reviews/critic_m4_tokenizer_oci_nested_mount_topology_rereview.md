# CRITIC M4 OCI Nested-Mount Topology Rereview

Date: 2026-08-21 EDT  
Regime: B  
Role: authoritative persistent CRITIC  
Status: **COMBINED BLOCK**

## Immutable intake

- Substantive head: `architect/m4-tokenizer-oci-nested-mount-topology-remediation @ 64f8010c26abbc6f47c0acb38916a756d9a09ede`
- Review result: `3cbbc52b77b21b8092ff66bf1da8126d67b374b0`
- Base / prior instrument failure: `1f0f41b42e28b0edb8397db3681131755163f7b7`
- Canonical manifest: `architect/m4-tokenizer-oci-nested-mount-topology-remediation-manifest @ b0b1c405f77ee47b50ba18706d4005a5ec5bda86`
- Official test-bed authority: `coordinator/m4-wsl2-preexecution-testbed @ 1ee4a004bab575757e91918c5ef7c0ef694fddf7`, tag `m4-wsl2-preexecution-testbed-v1`
- Subsequent setup-script authority: `coordinator/m4-wsl2-preexecution-testbed @ 0631a019a153ec89312938982c007cf94dd3f03e`, tag `m4-wsl2-preexecution-testbed-v1.1`; its updated runbook retains the same wrapper-before-mount-smoke sequence
- Checkout: repository `tools/workflow_checkout.py`; receipt SHA-256 `4ae1ddcfddb27e40f1ab0c785e71d04fbbf2fd59a03aef61a33a91bf084abcf6`

The canonical handoff manifest validates with `tools/workflow_contract_validator.py`. All 24 declared artifact SHA-256 values reproduce from raw Git blobs with zero mismatches.

## Banked evidence

- The tracked marker is mode `100644`, empty-blob OID `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, zero bytes, and SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- All nine executable-package entries reproduce their exact modes, raw byte counts, and SHA-256 identities. The package and six affected adjacent JSON sidecars bind exactly.
- The base-to-head delta contains exactly the eleven authorized topology/package/specification/test/handoff paths. Unchanged package members retain their Git object identities. Superseded identities have no active binding.
- Repository-read-only then nested-output-writable mount token order is exact. The nested mount hides the marker; the required stage postcondition remains empty. The materializer preserves repository, custody, then nested-output order.
- Static Git mode `100644` and mounted regular/non-link/zero-byte semantics are correctly separated; the WSL mounted presentation is not substituted for Git mode.
- The prior engine-125 absent-marker event is valid dynamic negative evidence: the container process did not start, stage remained empty, and custody/materializer access and consumption did not occur.
- Independent exact pinned Linux/amd64, pull-disabled, network-none, repository-read-only, no-custody wrapper: **35/35 PASS**, exit `0`.
- Independent custody-free `/bin/true` smoke, run after the wrapper per the official runbook: exit `0`, stage exactly empty, temporary stage removed, checkout clean.

## Batched blocking findings

### CR-MNT1 — The active pre-operation sequence contradicts the cited durable test-bed authority

The official runbook at `1ee4a004bab575757e91918c5ef7c0ef694fddf7`, unchanged in this respect at setup-script authority `0631a019a153ec89312938982c007cf94dd3f03e`, requires: immutable checkout/image verification, then the exact no-custody wrapper, then the custody-free mount smoke, then stop on any mismatch. The reviewed active package reverses the two executable gates:

- `specs/data/m4_tokenizer_executable_package_v1.json` orders `RUN_CUSTODY_FREE_MOUNT_SMOKE` before `RUN_PREIMPORT_TEST_WRAPPER`.
- `specs/data/m4_tokenizer_oci_launch_contract_v1.json` maps smoke success to `PROCEED_TO_NO_CUSTODY_TEST_WRAPPER`.
- `specs/m4_local_tokenizer_materialization_spec_v1.md`, the test contract, and the durable return repeat smoke-before-wrapper.

This is a direct active-contract divergence from the exact authority the package cites and the Coordinator made binding for this rereview. Reconcile every active sequence/projection binding and affected identity/sidecar to wrapper-before-smoke. Preserve fail-closed stop behavior and the unconsumed operation.

### CR-MNT2 — Two named topology negatives lack production-realized evidence

`nested_output_before_repository` and `nonempty_stage_after_smoke` are declared in the OCI and test contracts, but the selected test only verifies their names and mapping strings. It does not realize either topology through the custody-free smoke path and assert the terminal no-custody/no-consumption projection. Only `absent_marker` has dynamic engine evidence.

Add exact custody-free realizations for reversed mount order and post-smoke nonempty stage. For each, prove the governed terminal mapping, no custody environment/mount/access, no materializer start, no operation consumption, and deterministic cleanup. Keep the positive smoke and all banked package evidence unchanged.

## Law fidelity, safety, and holds

The findings require no reconstruction or alteration of constitutional law. Thresholds and identities remain tied to repository sources. The review accessed no custody, model, tokenizer, protected seed, scientific, scoring, inference, serving, or qualification input. No materializer invocation or retry occurred; the single materialization operation remains **UNCONSUMED**.

Public-safety review found no credentials, private values or paths, PII, custody data, model/tokenizer bytes, token arrays, protected seeds, or scientific output. Preflight findings F000001-F000006 are three content occurrences duplicated across the commit-parent and combined-range scan domains; every occurrence lies wholly inside a required public prior-failure or test-bed authority commit identity. They are classified as non-secret reproducibility metadata and are not suppressed. Gitleaks findings: zero.

## Disposition

**COMBINED BLOCK.** Return through WORKFLOW COORDINATOR to ARCHITECT for one batched sequence-and-negative-evidence remediation. Preserve every banked identity, positive result, no-access boundary, failure mapping, and standing hold.
