# CRITIC M4 Topology Sequence + Negative-Evidence Rereview

Date: 2026-08-21 EDT  
Regime: B  
Role: authoritative persistent CRITIC  
Status: **COMBINED BLOCK**

## Immutable intake

- Substantive head: `architect/m4-tokenizer-topology-sequence-negative-remediation @ 0c418ef6aa22535c15e08cf88b45d4ced9bbee55`
- Review result: `8e5d303c4148f1656ecb81cbb8af7201006775c1`
- Base / prior CRITIC BLOCK: `732963988d051f4ce9f42ace2e0ce7118bf90780`
- Canonical manifest: `architect/m4-tokenizer-topology-sequence-negative-remediation-manifest @ 38ecdebafbaf358098ac0f9b68dbd5964680936b`
- Official test-bed authority: `coordinator/m4-wsl2-preexecution-testbed @ 0631a019a153ec89312938982c007cf94dd3f03e`, tag `m4-wsl2-preexecution-testbed-v1.1`
- Checkout: repository `tools/workflow_checkout.py`; receipt SHA-256 `ddb05da68cf2d2409d1874dae79b50f3bdf45f7726ac4b9b6a4e7ee4de40925c`

The canonical handoff manifest validates with `tools/workflow_contract_validator.py`. All 23 declared artifact SHA-256 values reproduce from raw Git blobs with zero mismatches.

## CR-MNT1 closure — banked

The durable wrapper-before-smoke sequence is now consistent in the active executable package, OCI success projections, test contract, principal specification clauses, wrapper tests, and durable return:

`VERIFY_FRESH_CHECKOUT_AND_IMAGE → RUN_PREIMPORT_TEST_WRAPPER → STOP_ON_NONZERO → RUN_CUSTODY_FREE_MOUNT_SMOKE → STOP_ON_NONZERO_OR_NONEMPTY_STAGE → SINGLE_MATERIALIZATION_RELEASE_CHECK`

- Wrapper exit `0` maps only to the custody-free smoke.
- Smoke exit `0` with an empty stage maps only to the separate materialization release check.
- Every other wrapper, engine, topology, or stage outcome stops fail closed with no retry and no consumption.
- No active smoke-before-wrapper pipeline binding remains outside preserved historical provenance.

Independent exact pinned Linux/amd64, pull-disabled, network-none, repository-read-only, no-custody wrapper: **35/35 PASS**, exit `0`.

## CR-MNT2 closure — banked

The new LF runner is Git mode `100755`, 4400 raw bytes, and SHA-256 `a0f4383913a38cdde9f93947865d990e36b41fb538ff1468b121f4b1db2b137a`. Independent execution after the wrapper reproduced:

| Case | Exact result | Governed disposition |
|---|---|---|
| positive repository-then-nested-output smoke | exit `0`; stage empty | proceed only to separate release check |
| absent marker/directory | engine exit `125`; stage empty | fail closed; no custody, retry, or consumption |
| nested output before repository | observed exit `0`; stage empty | forbidden topology maps fail closed regardless of engine exit |
| nonempty stage after smoke | exit `0`; exact fixed zero-byte sentinel observed and removed; stage empty after cleanup | fail closed; no custody, retry, or consumption |

The matrix terminal trace reports custody environment/mount/record false, model/tokenizer access false, materializer start false, operation consumption false, retry false, and cleanup complete. The command construction and runner contain no custody mount or materializer command. The checkout remained clean.

All nine executable-package entries reproduce their exact raw sizes, modes, and SHA-256 identities. The package and six relevant adjacent JSON sidecars bind exactly. The base-to-head delta contains only the thirteen declared sequence/topology remediation paths.

## Blocking finding

### CR-MNT3 — Active specification retains a superseded `.gitattributes` identity

`specs/m4_local_tokenizer_materialization_spec_v1.md` is internally contradictory:

- Its active runtime-checkout clause binds the current `.gitattributes` identity: 2459 LF bytes and SHA-256 `998b713a5094f924efa62fc0c65f1195f385ea08476ee1d150ea2527d6e04c4c`.
- Its later active “Normative LF Git-blob identities after executable-package closure” clause still binds the superseded identity: 2391 LF bytes and SHA-256 `68c528ede67720007d4ec15d15f6d723136a24b9a4662c94ad9cdfbbc158601d`.

The package, manifest, actual raw blob, and first clause all require the current identity. The stale normative clause can cause a conforming executor to reject the correct checkout or select incompatible evidence. Reconcile that clause and every affected specification identity; regenerate any changed manifest/handoff identity. Preserve the complete CR-MNT1/CR-MNT2 executable evidence and all other banked package identities.

## Law fidelity, safety, and holds

The finding is an active repository-source contradiction, so CRITIC does not choose a winner beyond identifying the exact current package/blob evidence and stops with BLOCK. No constitutional law was reconstructed or altered.

The review accessed no custody, model, tokenizer, protected seed, scientific, scoring, inference, serving, or qualification input. No materializer invocation or retry occurred. The single materialization operation remains **UNCONSUMED**.

Public-safety review found no credentials, private values or paths, PII, custody data, model/tokenizer bytes, token arrays, protected seeds, or scientific output. Preflight findings F000001-F000006 are three content occurrences duplicated across commit-parent and combined-range domains; every occurrence lies wholly inside a required public review-result, manifest, or test-bed authority commit identity. They are classified as non-secret reproducibility metadata and are not suppressed. Gitleaks findings: zero.

## Disposition

**COMBINED BLOCK.** Return through WORKFLOW COORDINATOR to ARCHITECT for the single residual CR-MNT3 stale-identity reconciliation. Preserve all CR-MNT1/CR-MNT2 closure evidence, no-access boundaries, failure mappings, cleanup behavior, and standing holds.
