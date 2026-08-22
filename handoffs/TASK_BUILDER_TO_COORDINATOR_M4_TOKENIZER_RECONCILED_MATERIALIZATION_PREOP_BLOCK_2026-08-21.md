# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER RECONCILED MATERIALIZATION PRE-OPERATION BLOCK

**Date:** 2026-08-21

**Regime:** B

**Status:** BLOCK

**Gate served:** Mandatory pre-operation identity, executable, runtime, and host-input gate for the single reconciled bounded tokenizer materialization

## Canonical intake

- Reconciled re-release: `coordinator/m4-tokenizer-reconciled-materialization-rerelease` at `ed31a60b5b3f7a15591525f1ddfc3f8190a2e5e5`.
- Reconciled package: `architect/m4-tokenizer-executable-package-identity-reconciliation` at `bc2b82b87185d50fbdb4d77ce4482100de6feaa0`.
- Reconciled result: `b9757e324eb2ee3f366b776fc2489dbf5a4690c1`.
- Canonical reconciled manifest: `architect/m4-tokenizer-executable-package-identity-reconciliation-manifest` at `37e63b7ff096ddd9a243ed76d52112a468e0171e`.
- Persistent-CRITIC CLEAR: `critic/m4-tokenizer-executable-package-identity-rereview` at `6b78259830c0aa5c7c24f71bd768745aab2a0706`.
- Work branch: `taskbuilder/m4-tokenizer-reconciled-materialization-execution`.

## Blocking pre-operation finding

The committed OCI launch contract requires the private host input `MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1` before the mandatory custody-root precondition can be validated. That variable is absent from both the TASK BUILDER Windows process and the WSL execution context. Only presence was tested; no value, path, directory search, custody lookup, or private artifact access occurred.

The public release and preserved authorities provide no alternate binding mechanism and prohibit directory search, fallback, generated governed inputs, normalization/copy, or invention. TASK BUILDER therefore cannot prove the required custody root is an existing canonical regular non-link directory, distinct from the immutable checkout and private empty output stage. The gate fails closed before the no-custody test wrapper and before materializer start.

## Requirement → production/gate → evidence trace

| Requirement | Gate branch | Evidence | Disposition |
|---|---|---|---|
| Fresh immutable release checkout | `workflow_checkout.py create` at exact release SHA | isolated clean checkout at `ed31a60b5b3f7a15591525f1ddfc3f8190a2e5e5`; `git fsck --full --strict` PASS | PASS |
| Reconciled package and canonical inventory match released bytes | raw Git-blob SHA-256 and byte-count comparison | all 23 canonical-manifest entries, all eight executable-package entries, and adjacent sidecars match | PASS |
| Exact WSL2-backed OCI runtime and image | Docker client/server identity plus local image inspection | Docker `29.1.3`, server `linux/amd64`, exact platform digest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6` | PASS |
| Required private custody host input exists before custody-root validation | presence-only host/WSL environment check | required variable absent in both execution contexts | BLOCK |
| Custody root is canonical, regular, non-link, and distinct | prescribed precondition after host-input binding | cannot be evaluated without the required binding; no search or invention authorized | NOT RUN, correct fail-closed behavior |
| Run pre-import wrapper only after all identity and host-input preconditions PASS | execution order `VERIFY_FRESH_CHECKOUT_AND_IMAGE` before `RUN_PREIMPORT_TEST_WRAPPER` | wrapper was not invoked | NOT RUN, correct fail-closed behavior |
| Start one materializer only after test exit 0 | execution order `STOP_ON_NONZERO` before `RUN_SINGLE_MATERIALIZER` | materializer was not started | NOT RUN; operation unconsumed |

## Ordered access-event trace

`release checkout verification → raw Git-blob package verification → reconciled manifest verification → Docker/runtime identity verification → exact image identity verification → presence-only required-host-input check → required input absent → STOP`

No custody-root resolution, directory search, private-record read, weight observation, tokenizer/config read or copy, loader import, `from_pretrained`, output-stage creation, test-container launch, or materializer launch occurred.

## Preserved boundaries and route

- The single materialization operation remains **UNCONSUMED**.
- No routed custody/model/tokenizer access, OCI test or materialization, retry, fallback, alternate runtime, generated governed input, inference, qualification, scoring, protected seeds, science, STATE/provenance mutation, model/tokenizer publication, merge, rerun, or gate decision occurred.
- **Exact next recipient:** WORKFLOW COORDINATOR to restore the required private host binding through authorized custody channels and issue a new exact release if appropriate.
