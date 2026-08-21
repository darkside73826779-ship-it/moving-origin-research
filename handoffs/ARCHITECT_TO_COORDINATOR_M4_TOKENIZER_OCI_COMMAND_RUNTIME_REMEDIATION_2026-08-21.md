# ARCHITECT to WORKFLOW COORDINATOR — M4 Tokenizer OCI Command/Runtime Remediation

**Date:** 2026-08-21

**Regime:** B

**Disposition:** READY FOR PERSISTENT-CRITIC REVIEW; EXECUTION REMAINS HELD

## Authority and input

- OCI environment release: `coordinator/m4-tokenizer-oci-environment-release` at `2e7fb9ee1f9643405d7fbc40120c7dc383abf9a3`.
- Preserved materialization release: `coordinator/m4-tokenizer-materialization-release` at `9007260570235c1b06b104d78106ba32e8a4e9dd`.
- Cleared contract/CLEAR: `architect/m4-tokenizer-materialization-spec` at `ed25e3b4811a9024c8b7d7a0120a8fc073748004`; `critic/m4-tokenizer-rf1-final-combined-rereview` at `ff3976dd58009a8c6d0d8fd2cddc787fc96b63bc`.
- TASK BUILDER block: `taskbuilder/m4-tokenizer-materialization` at `c19b830547a6551657cd0fab6e3fe581cfc06983`; artifact `handoffs/TASKBUILDER_TO_COORDINATOR_M4_TOKENIZER_OCI_COMMAND_SPECIFICATION_BLOCK_2026-08-21.md`.

## Exact remediation

- Preserved the pinned OCI index and Linux/amd64 manifest identities unchanged.
- Bound the exact callable interpreter in that image as the PATH executable name `python3`.
- Replaced both operative `python -I` prefixes with exact `python3 -I` prefixes; all script/module names and arguments are unchanged.
- Added the exact materialization command to the executable test contract and a negative case requiring the unavailable `python` name to fail as `RUNTIME_IDENTITY_MISMATCH` before custody lookup.
- Recomputed the test-contract sidecar from the committed LF Git-blob bytes.

## Boundary and next event

This changes an operative command contract. It is not executable under the prior release. WORKFLOW COORDINATOR should route the exact remediation commit to persistent CRITIC and, after CLEAR, obtain Rebecca re-release before returning execution custody to TASK BUILDER. The single authorized materialization operation remains unconsumed.

No custody lookup; tokenizer/model access; image modification; command execution; inference/serving; Q2/EF3; qualification; diagnostics/scoring; protected-seed access; scientific change; STATE/provenance mutation; publication; rerun; merge; or gate decision occurred or is authorized by this artifact.

## Public-repository safety

This package contains only public repository identities, public OCI digests, deterministic command text, and sanitized disposition. Final scan and remote-equality results are supplied in the formal return.
