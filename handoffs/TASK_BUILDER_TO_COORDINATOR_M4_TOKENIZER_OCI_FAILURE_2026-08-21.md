# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER PRIVATE-BINDING EXECUTION INSTRUMENT FAILURE

**Date:** 2026-08-21

**Regime:** B

**Status:** INSTRUMENT FAILURE

**Terminal mapping:** `RUNTIME_IDENTITY_MISMATCH_NO_CUSTODY_NO_CONSUMPTION`

## Canonical intake

- Private-binding re-release: `coordinator/m4-tokenizer-private-binding-rerelease` at `a4d780b11c9719df77acd320212a296542e5871a`.
- Reconciled package: `architect/m4-tokenizer-executable-package-identity-reconciliation` at `bc2b82b87185d50fbdb4d77ce4482100de6feaa0`.
- Persistent-CRITIC identity CLEAR: `critic/m4-tokenizer-executable-package-identity-rereview` at `6b78259830c0aa5c7c24f71bd768745aab2a0706`.
- Prior binding-absence BLOCK: `taskbuilder/m4-tokenizer-reconciled-materialization-execution` at `db086cb4eba87049adca50d5a0d95057c7cd1640`.
- Work branch: `taskbuilder/m4-tokenizer-private-binding-materialization-execution`.

## Terminal execution result

The mandatory pre-operation gate passed. The exact no-custody pre-import wrapper then passed all 35 selected tests in the pinned, network-disabled, read-only container with exit `0`.

TASK BUILDER issued the authorized materializer invocation exactly once. The OCI engine returned exit `125` during container creation because it could not create the nested writable output mountpoint beneath the read-only repository bind mount. The container process did not start. The committed launch contract maps engine exits `125`, `126`, and `127` to `RUNTIME_IDENTITY_MISMATCH_NO_CUSTODY_NO_CONSUMPTION`.

No retry or fallback was attempted. The private output stage remained empty and was removed after verification. No sanitized result pair exists or is eligible for publication.

## Root cause and proposed minimal fix

The immutable released checkout does not contain `artifacts/m4_tokenizer_materialization/`. Git cannot represent an empty directory. During OCI setup, the engine therefore tried to create that nested destination after `/workspace` had already been mounted read-only and failed before process start.

The minimal durable correction is:

1. Add a tracked inert marker at `artifacts/m4_tokenizer_materialization/.gitkeep` (or an equivalently approved inert tracked file), so the exact nested directory exists in every fresh immutable checkout.
2. Bind the empty private output stage over `artifacts/m4_tokenizer_materialization` exactly as the current launch contract specifies. The bind hides the marker inside the container, so the stage remains initially empty and the postcondition still permits only `tokenizer_materialization.json` and its sidecar.
3. Add the marker identity to the governed package/inventory and add a mandatory custody-free mount-smoke gate using the exact repository/output mount order and security flags before any future single-operation release.

Rebecca authorized a feasibility-only, custody-free retry of this mount correction after the terminal failure. TASK BUILDER created the otherwise-absent nested directory temporarily, mounted an empty private stage over it with the same pinned image, read-only repository bind, nested writable output bind, network isolation, and security flags, and ran only `/bin/true`. The smoke test exited `0`; the stage remained empty. All temporary directories were removed and the checkout returned clean. This was not a materializer invocation and performed no custody lookup or model/tokenizer access.

## Requirement → production/gate → evidence trace

| Requirement | Production/gate branch | Evidence | Disposition |
|---|---|---|---|
| Fresh immutable released checkout | helper-created checkout at exact re-release SHA | clean checkout at `a4d780b11c9719df77acd320212a296542e5871a`; `git fsck --full --strict` PASS | PASS |
| Reconciled executable identities | raw Git-blob byte-count and SHA-256 comparison | all eight executable-package bindings and adjacent sidecar match | PASS |
| Exact pinned runtime and image | WSL2-backed Docker and local image inspection | client/server `29.1.3`, `linux/amd64`, exact platform digest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`, pull disabled | PASS |
| Private custody binding and root preconditions | presence, canonical-directory, non-link, fixed-record-kind, and distinctness checks | all passed without emitting or serializing private values | PASS |
| Mandatory no-custody test wrapper | exact production wrapper in the pinned container | 35 tests run, 35 passed, exit `0` | PASS |
| Invoke the materializer once only after all gates pass | exact committed launch token order | one invocation issued | PASS |
| Container process starts with repository read-only and nested output writable | OCI mount realization | engine exit `125` before process start; nested mountpoint creation rejected | INSTRUMENT FAILURE |
| Publish only a validated sanitized pair | postcondition after materializer exit `0` | stage contained zero files; no pair copied or published | NOT APPLICABLE, correct fail-closed behavior |
| Proposed pre-existing nested target resolves mount defect | custody-free OCI mount-smoke with identical mount order/security flags and `/bin/true` only | exit `0`; empty stage preserved; checkout clean after cleanup | FEASIBILITY PASS |

## Ordered access-event trace

`release verification → executable-package verification → runtime/image verification → private binding and root-kind verification → empty distinct output-stage verification → no-custody wrapper 35/35 PASS → single OCI invocation → engine mount construction failure → exit 125 → empty-stage verification → STOP → user-authorized custody-free mount-smoke with pre-existing target → exit 0 → empty-stage verification → temporary-directory cleanup`

The container process never started. Therefore no custody environment lookup inside the materializer, custody-root resolution by the materializer, private-record read, weight observation, tokenizer/config read or copy, loader import, `from_pretrained`, token construction, or artifact publication occurred.

## Preserved boundaries and route

- Under the binding OCI launch contract, the single materialization operation remains **UNCONSUMED**, but this release permits no retry.
- No alternate mount order, image, interpreter, runtime, output location, fallback, mutation, normalization/copy, or generated governed input was attempted.
- No model/tokenizer access, inference, qualification, diagnostics/scoring, protected seeds, science, STATE/provenance mutation, model/tokenizer publication, merge, rerun, or gate decision occurred.
- **Exact next recipient:** WORKFLOW COORDINATOR for routing of the deterministic nested-mount launch-contract defect and the feasibility-proven marker-directory correction to the authorized specification role.
