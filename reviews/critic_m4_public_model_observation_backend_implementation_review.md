# CRITIC review — M4 public-model non-scoring observation backend implementation

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

## Immutable intake

- Implementation ref/head: `taskbuilder/m4-public-model-observation-backend-implementation` at `76efc260f86028ca1fccfbe5156d97d06359c5f2`.
- Implementation result: `b6fe5de15cca6aecd4883b1bc2e4907b58f85c08`.
- Routing result: `c38934dbe57f621b6011f429582493d5e1e22d29`.
- Canonical manifest: `handoffs/manifests/m4_public_model_observation_backend_implementation/20260822T144211Z_task_builder_to_workflow_coordinator.json`.
- Cleared design route/result/manifest/review: `89bf97e53af7a8852fc6c3dc67623fc14d11650e`, `515e1d553858f4675a5ee5f347ffbc395b8fdd78`, `d7c08e7a984be38cd378769db8a4c26e36e8c00b`, and `afe468e5bedd82b0be0725860ea0ab83421da2b7`.

Authenticated remote equality and all declared ancestry relationships reproduce. The canonical helper created the isolated review worktree and accepted the routing boundary. The handoff manifest validates `VERIFIED` against the common schema.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

This is a custody-free implementation review. It is not a model run, scoring result, scientific finding, qualification, readiness ruling, merge decision, or gate action.

## Blocking finding

### BF1 — zero-token private views publish schema-invalid PASS evidence

Classification: fail-open sanitized-evidence/schema conformance defect.

The bound local-observation schema requires `input_token_count` to be an integer with minimum 1. The implementation accepts a private view with `context_length=0` and encoded count 0: `_decode_private_view` requires only count/context/length agreement, while `_validate_observation` rejects counts below 0 rather than below 1.

An independent full adapter-path reproduction used the exact public prompt identity, an authenticated `PrivateTokenView(0, encode_private_view([]))`, and the custody-free stub engine. The call returned a seven-field `PASS` receipt, invoked the engine, and atomically published a JSON/sidecar pair containing `input_token_count=0`. The committed artifact therefore fails its bound schema even though the implementation's semantic validator accepts it.

Impact: the backend can publish evidence outside the cleared local-only schema and can treat an empty tokenizer result as a successful public-model observation. This contradicts the implementation claim that every published observation is schema-valid and leaves the private-view/tokenizer boundary fail-open. The focused suite and mutation set do not exercise this lower bound.

Smallest safe remediation: reject `context_length/count < 1` before engine generation; make `_validate_observation` enforce the schema's minimum; add a production adapter-path regression proving zero engine calls, no temp/final artifact, exact adapter/backend state and stage-inventory restoration, and the registered `SYNTHETIC_REJECTED` projection; add a deterministic mutant for the lower-bound guard; then regenerate the implementation inventory, sidecars, mutation transcript, quality trace, handoff, and canonical manifest.

## Cleared checks and preserved boundaries

- All 16 manifest artifact raw SHA-256 identities and all six implementation sidecar pairs reproduce from Git objects. JSON is canonical, governed artifacts are LF-only, and `git diff --check` is clean.
- The implementation authority cascade exactly binds the cleared design and the banked dependency-lock result/routing/manifest/review. The production seam remains byte-identical to `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`: 49,119 bytes, SHA-256 `8964de5daf745226771818ab59f2cc75ef29ccbc5d09b43b6dae102b876b2f1b`.
- Static inspection confirms control/naive-only registration, exact seven-field receipts, registered failure-code projection, identity-before-loader ordering, literal namespace attestation, one injected engine call, prompt-order binding, state/inventory rollback, atomic local writes, cleanup failure stops, exact five-row HELD-only projection, and four false evidence flags. No model/runtime library import, network client, environment lookup, model acquisition, or run entrypoint exists in the production backend.
- `run_authorized=false` remains bound. Exact launch-form invocation returned `RUN_AUTHORITY_ABSENT` exit 2 before environment, model, or tokenizer access.
- The pinned WSL2 namespace identity reproduces: `/usr/bin/unshare` 43,624 bytes, mode 0755, SHA-256 `51bcc77ba5db162c80028f861f0a2770d728c1de80773816d863f28d7a817adb`, util-linux `2.39.3-9ubuntu6.5`. The custody-free positive namespace smoke and expected errno-101 outbound-denial classifier both returned exit 0.
- Windows focused execution discovered 17 cases and returned 16 PASS with the privilege-only symlink case skipped. Ubuntu 24.04 WSL2 returned 17/17 PASS. Exact-byte mutation replay killed 6/6 mutants on WSL2 and on a short isolated Windows checkout.

Non-blocking harness note: the Windows mutation runner's whole-repository `shutil.copytree` raised an unhandled legacy path-length error from the canonical long helper worktree. The exact same commit returned baseline PASS and 6/6 KILLED from the short isolated checkout, so mutation sensitivity is reproduced; narrowing the disposable copy to its affected dependency closure would make the target deterministic under canonical Windows review paths.

## Public safety

Public preflight over `89bf97e53af7a8852fc6c3dc67623fc14d11650e...76efc260f86028ca1fccfbe5156d97d06359c5f2` produced 42 fixed-regex personal-contact heuristics across five scan domains. Manual review found only numeric substrings inside required public Git/SHA-256 identities, the public model revision/byte count, and the literal hexadecimal alphabet. Gitleaks 8.30.1 returned zero findings. No credential, contact data, private path/value, protected seed, model/tokenizer byte, prompt, score, or environment dump was found.

No model execution, model/tokenizer/private-custody access, protected input, scoring, qualification, science, state/provenance mutation, merge, publication, readiness declaration, or gate decision occurred.

## Disposition

Return one **COMBINED BLOCK** to **WORKFLOW COORDINATOR**. The smallest next action is one narrow **TASK BUILDER** remediation of BF1, with the Windows mutation-copy portability correction included in the same delta if accepted. All existing holds remain binding.
