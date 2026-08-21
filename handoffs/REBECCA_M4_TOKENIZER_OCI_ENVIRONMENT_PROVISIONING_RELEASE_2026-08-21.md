# Rebecca Release — M4 Tokenizer OCI Environment Provisioning

**Date:** 2026-08-21  
**Regime:** B  
**Status:** RELEASED FOR EXACT ENVIRONMENT PROVISIONING AND THE PREVIOUSLY AUTHORIZED SINGLE OPERATION

Rebecca directs the bounded tokenizer-materialization work to continue using the exact pinned OCI runtime required by the CRITIC-cleared contract. This resolves the TASK BUILDER safe pause caused by the absence of a callable Docker runtime; it does not authorize an alternate host-runtime execution.

## Authority and inputs

- Materialization release: `coordinator/m4-tokenizer-materialization-release` @ `9007260570235c1b06b104d78106ba32e8a4e9dd`
- Cleared contract: `architect/m4-tokenizer-materialization-spec` @ `ed25e3b4811a9024c8b7d7a0120a8fc073748004`
- Final combined CRITIC CLEAR: `critic/m4-tokenizer-rf1-final-combined-rereview` @ `ff3976dd58009a8c6d0d8fd2cddc787fc96b63bc`
- TASK BUILDER disposition: `SAFE PAUSE / RUNTIME_IDENTITY_MISMATCH BEFORE CUSTODY LOOKUP`; the one authorized materialization operation was not started or consumed.

## Authorized environment action

TASK BUILDER may use a compliant WSL2-backed Docker/OCI environment and may acquire the exact image, index digest, and platform digest already fixed by the cleared contract. It may verify the runtime and image identities before custody lookup. No substitute image, tag, digest, host Python environment, serving engine, or alternate runtime is authorized.

After exact environment verification, TASK BUILDER may perform the same single bounded tokenizer-materialization operation authorized by `9007260570235c1b06b104d78106ba32e8a4e9dd`. The prior safe pause did not consume the operation. Any mismatch stops fail-closed; no retry or fallback is authorized.

## Resource sequencing

The local WSL2 inference fact-finding process has terminated and GPU memory has been verified free. OCI provisioning and tokenizer materialization must not overlap another GPU/model workload. The tokenizer operation remains a lightweight contract-verification task and authorizes no model inference.

## Route and holds

TASK BUILDER returns sanitized execution evidence through WORKFLOW COORDINATOR to the established persistent CRITIC. CRITIC CLEAR returns through Coordinator to Rebecca.

All inference, serving, qualification, Q2/EF3, diagnostics, scoring, protected-seed, training, scientific-change, STATE/provenance, rerun, publication, and merge holds remain binding. Model/tokenizer bytes, complete token arrays, custody values, credentials, machine identifiers, and private local paths remain prohibited from Git.
