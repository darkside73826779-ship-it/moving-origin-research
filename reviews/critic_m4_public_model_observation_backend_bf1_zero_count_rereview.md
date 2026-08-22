# CRITIC rereview — M4 public observation backend BF1 zero-count remediation

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

## Immutable intake

- Package ref/head: `taskbuilder/m4-public-model-observation-backend-bf1-zero-count-remediation` at `11eebe60b18e325fe64b9a1ea4a5cdbf378459c7`.
- Implementation result: `46252865c5a13a997396ac7520eb3c06d8f541e1`.
- Routing result: `9076386c6a51159bd977035ceaf431ab17c90e5e`.
- Canonical manifest: `handoffs/manifests/m4_public_model_observation_backend_bf1_remediation/20260822T150019Z_task_builder_to_workflow_coordinator.json`.
- Prior authoritative BLOCK: `critic/m4-public-model-observation-backend-implementation-review` at `eee7dd947b0ecd0a5a9c0d8be2b3ca8f108c9622`.

Remote equality and the exact implementation → routing → manifest ancestry reproduce. The repository checkout helper accepted the routing boundary. The common handoff validator returned `VERIFIED`; all 18 manifest artifact hashes, all listed sidecars, LF constraints, and Git modes reproduce. `git diff --check` and `git fsck --strict` are clean.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: CLEAR**
- **COMBINED VERDICT: CLEAR**

This is a custody-free BF1 implementation rereview. It is not a model run, scoring result, scientific finding, qualification, readiness ruling, merge decision, or gate action.

## BF1 closure

The remediation closes the prior fail-open zero-count path:

- `_decode_private_view` rejects `min(count, context_length) < 1` before engine generation. The independent observation validator separately enforces `input_token_count >= 1`, exactly matching the bound schema minimum.
- The production adapter-path regression supplies authenticated zero-count framing and obtains `BACKEND_DECLARED_FAILURE` with `backend_code=SYNTHETIC_REJECTED`. It proves zero engine calls, an empty stage, and exact equality of the complete adapter transaction plus backend snapshot before and after rejection. The backend snapshot includes the complete stage inventory.
- The deterministic `ZERO_COUNT_LOWER_BOUND_REMOVED` mutant weakens the guard to `< 0` and is killed by that exact adapter-path target. The canonical mutation contract and transcript contain the same ordered seven rows, expected exits and targets; the transcript reports 7/7 killed, zero survivors, zero instrument failures, and exact source restoration.
- The disposable mutation checkout copies exactly four affected dependencies: the production backend, byte-preserved production seam, test package marker, and focused test module. Independent Windows and WSL2 execution confirms this closure is sufficient and removes the prior long-path dependency.

The production seam remains byte-identical at SHA-256 `8964de5daf745226771818ab59f2cc75ef29ccbc5d09b43b6dae102b876b2f1b`. All implementation behavior outside the bounded guard/schema/test/mutation delta remains banked from the prior review.

## Independent focused evidence

- Windows: the two BF1 targets pass; the identity-first focused suite returns 18 PASS plus the privilege-only directory-symlink skip out of 19; deterministic mutation replay returns 7/7 KILLED.
- Ubuntu 24.04 WSL2: the two BF1 targets pass; the identity-first focused suite returns 19/19 PASS including the linked-stage case; deterministic mutation replay returns 7/7 KILLED.
- The mutation contract, transcript, implementation inventory, source/test identities, sidecars, and canonical manifest are internally consistent. `run_authorized=false` remains exact in both the implementation inventory and banked launch contract.

## Public safety and holds

Terminal public preflight over `76efc260f86028ca1fccfbe5156d97d06359c5f2...11eebe60b18e325fe64b9a1ea4a5cdbf378459c7` reports 49 fixed-regex personal-contact matches and zero gitleaks findings. Manual review maps every match to a numeric substring inside a required public hash, public model revision/byte count, or the literal hexadecimal validation alphabet; none is contact or private data.

No model/tokenizer/private-custody access, protected input, scoring, qualification, science, state/provenance mutation, merge, readiness declaration, or gate action occurred. All standing holds remain binding.

## Disposition

Return one **COMBINED CLEAR** to **WORKFLOW COORDINATOR**. BF1 is closed with no residual blocker; the Coordinator is the exact next recipient and retains all routing and gate authority.
