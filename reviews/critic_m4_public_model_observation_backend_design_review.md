# CRITIC review — M4 public-model non-scoring observation backend design

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

Gate served: narrow design-only repository review

## Exact intake and repository identity

- Substantive ref: `refs/heads/architect/m4-public-model-observation-backend-design`.
- Routing head: `0945a5e7debf87c15c1985137cd056d6b32bdbda`.
- Design result: `6644d02337db29fcdceeb38f22afe8801c98cc2b`.
- Base and cleared production seam: `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`.
- Manifest ref/head: `refs/heads/architect/m4-public-model-observation-backend-design-manifest` at `a7eb763ac3d9a02ad0a613da6b07a4f7b612586e`.
- Manifest: `handoffs/ARCHITECT_TO_COORDINATOR_M4_PUBLIC_MODEL_OBSERVATION_BACKEND_DESIGN.manifest.json`.
- Review branch: `critic/m4-public-model-observation-backend-design-review`.

Authenticated remote equality for both supplied refs was exact at intake. The canonical manifest validates `VERIFIED` against the common handoff schema. All 15 manifest raw SHA-256 identities reproduce. All five JSON/sidecar pairs reproduce exact basename, digest, and LF. The five JSON documents parse. `git diff --check` and `git fsck --full --strict` returned clean.

The standard isolated-checkout helper refused the package because the routing-only range changes `.gitattributes` in addition to the handoff; BF5 records that packaging defect. Review continued in a plain isolated Git worktree at the exact routing head, without changing package bytes.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **DESIGN / REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

This verdict is limited to the proposed non-scoring diagnostic design. It is not a model observation, scientific interpretation, score, qualification, readiness ruling, implementation clearance, merge decision, or run release.

## Blocking findings

### BF1 — The proposed lifecycle and failures cannot traverse the cleared `RealBackendProtocol` transaction seam

Classification: protocol mapping / rollback defect.

Affected artifacts:

- `specs/m4_public_model_observation_backend_design_v1.md`, lines 11, 31–38, 46, and 48–52.
- `specs/data/m4_public_model_observation_backend_contract_v1.json`, especially `failure_codes`, `failure_projection`, and `protocol_methods` (line 1).
- `specs/data/m4_public_model_observation_backend_test_contract_v1.json` (line 1).
- Cleared seam `src/m4_post_tokenizer_integration.py`, lines 74, 77–80, 334–377, 417–437, and 517–559.

Observed evidence:

- The design says `initialize` creates the sole engine and `is_live()` is true only while the engine and stage are valid. The cleared `AdapterFactory._construct` calls `_attest_live` immediately after the zero-argument backend constructor and before `describe` or `initialize`; anything other than literal `True` is disposed and rejected. A backend obeying the proposed `is_live` rule therefore cannot be constructed.
- The contract requires its eleven `OBSERVATION_*` failures to return seven-field `FAIL` receipts and map through `BACKEND_DECLARED_FAILURE`. The cleared seam accepts a declared failure only when `backend_code` belongs to `REGISTERED_BACKEND_FAIL_CODES`, currently the singleton `SYNTHETIC_REJECTED`. Every proposed code is therefore converted to `BACKEND_RECEIPT_INVALID`, contrary to the published mapping.
- `step` atomically renames the local observation before returning its receipt. The cleared adapter can still reject that receipt for field, session, state, request-correlation, or post-return private-view mutation faults and then invoke `restore_state`. The design explicitly removes only the operation temp; neither the contract nor the tests require removal of the already-renamed observation and restoration of the exact pre-call stage inventory.

Impact: the future backend cannot enter the cleared lifecycle as specified, cannot expose its declared fail-closed codes as specified, and can leave a local final artifact after an adapter-level rollback. These are exact-seam contradictions, not implementation choices.

Smallest safe remediation: specify a construction-time liveness state compatible with `_attest_live` while distinguishing engine-loaded state; explicitly authorize and bind the exact registered-failure-code expansion (or use only existing mappings); and define transaction-aware publication so no final observation exists until the adapter commit is irreversible, or require `restore_state` to remove every operation-owned final artifact. Add seam-level negatives for every receipt rejection and the post-return mutation path, asserting exact backend snapshot and exact stage-directory restoration.

### BF2 — The bound HELD projection digest is not the digest of the actual protocol rows

Classification: law-projection identity defect.

Affected artifact: `specs/data/m4_public_model_observation_backend_contract_v1.json`, `identity_digests.held_law_projection_sha256` and `laws.projection` (line 1); summarized in `specs/m4_public_model_observation_backend_design_v1.md` line 56.

Observed evidence:

- The contract binds `0a1f75c67f0d1a67b55f6da0c5985a8957e47b09ff594b32f79197396962cf48` as the held-law projection digest.
- That value reproduces only for the five seven-field nested `held_projection` objects from `specs/data/m4_post_tokenizer_crash_cart_law_semantics_v1.json`.
- The cleared protocol requires and emits eight-field rows; `meaning_source` is mandatory under `validate_laws` and is present in `held_law_projection()`. Canonicalizing the five actual ordered rows gives `bb2d5f838c54c404dd73d0c697ba6f45cd983fb7e5a7bb97a36b38570267b81f`, not the bound digest.

Impact: an observation cannot both bind the contract's advertised digest and bind the exact existing HELD rows used by the cleared protocol. The law statuses and reasons themselves remain correct and HELD-only; the blocker is their immutable identity.

Smallest safe remediation: bind the canonical digest of the exact eight-field ordered protocol rows, specify the canonical object shape unambiguously, regenerate affected sidecars and manifests, and test equality against `held_law_projection()` at the exact seam SHA.

### BF3 — The dependency-lock prerequisite targets an immutable package already authoritatively BLOCKED

Classification: stale authority / unsatisfiable prerequisite defect.

Affected artifacts:

- `specs/m4_public_model_observation_backend_design_v1.md`, lines 13 and 17.
- `specs/data/m4_public_model_observation_backend_contract_v1.json`, `authority.dependency_lock_result` and `authority.dependency_lock_review` (line 1).
- `specs/data/m4_public_model_observation_launch_contract_v1.json`, `prerequisites` (line 1).

Observed evidence: the design repeatedly requires persistent-CRITIC CLEAR of exact result `8c303b3262d8ea7640e06fe23671f999f5e01d2c`. Persistent-CRITIC review `31dd464ad1bcdfcef713b4636b4df653782dc1c8` had already returned COMBINED BLOCK on that immutable package before this design result was committed, and the Coordinator routed BF1–BF2 remediation. A corrected package must have a new substantive result identity; the blocked immutable result cannot later become CLEAR.

Impact: the launch prerequisite is permanently unsatisfiable as written and does not point future implementation at the pending corrected dependency contract.

Smallest safe remediation: bind the existing BLOCK review as current authority, leave the corrected dependency result and CLEAR review explicitly unbound, and STOP. After remediation exists, replace both placeholders with the exact corrected result and terminal review identities; do not describe CLEAR of `8c303b3` as a possible future event.

### BF4 — The launch contract declares network disablement but contains no mechanism that enforces it

Classification: launch-contract / local-safety defect.

Affected artifacts:

- `specs/m4_public_model_observation_backend_design_v1.md`, lines 21 and 58–60.
- `specs/data/m4_public_model_observation_launch_contract_v1.json`, `argv`, `environment_exact`, and `network` (line 1).
- `specs/data/m4_public_model_observation_backend_test_contract_v1.json`, required assertion `no_network_and_no_retry` (line 1).

Observed evidence: the sole argv directly starts a local virtual-environment Python interpreter. `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` constrain those libraries but do not prevent Python, vLLM, dependencies, or future implementation code from opening sockets. The `network` member is only the string `disabled_before_process_start`; no namespace, container `--network none`, firewall rule, socket-denial wrapper, or independently checkable enforcement identity is present.

Impact: the exact launch contract cannot establish its stated no-network boundary before model-process start. A test assertion cannot supply the missing launch mechanism.

Smallest safe remediation: bind one exact OS-enforced no-network launch mechanism in the executable argv or a separately hashed launcher contract, require it before Python starts, and add a custody-free negative proving outbound socket creation is denied. Preserve offline library flags as defense in depth.

### BF5 — The routing-only commit changes a non-handoff path

Classification: immutable packaging defect.

Affected range: `6644d02337db29fcdceeb38f22afe8801c98cc2b..0945a5e7debf87c15c1985137cd056d6b32bdbda`.

Observed evidence: the range adds the handoff and also modifies `.gitattributes` to add that handoff's LF rule. The repository's standard isolated-checkout helper stops with `routing-only range changes a non-handoffs path`.

Impact: the package cannot pass the canonical isolated-review construction despite the manifest faithfully listing the resulting routing-tip identity.

Smallest safe remediation: include the needed `.gitattributes` rule in the substantive design result, make the routing-only descendant add only the handoff, regenerate the handoff identities and canonical manifest, and verify the standard helper succeeds.

## Checklist results and preserved evidence

- **Exact model and runtime identities:** PASS. The Qwen repository/revision, weight/tokenizer/config sizes and hashes trace existing public repository records. Model and runtime canonical digests reproduce. The annotated testbed tag object is a tag and peels exactly to `11ea682a7f0fadfa1437a12d882402d90ffd0579`.
- **Deterministic public prompts:** PASS. Independent generation reproduced three ordered strict-ASCII 122-byte messages and all three bound SHA-256 values. No generated prompt text, prompt bytes, or token arrays are committed by this package.
- **Private-view encoding and retention boundary:** PASS at design level, subject to BF1 rollback. The 23-plus-8-times-count framing matches `M4_PRIVATE_VIEW_V1`, and the design forbids decoding prompt text and retaining token arrays outside process-local step lifetime.
- **Seven-field receipts:** field shape matches the cleared `RECEIPT_FIELDS`; failure-code traversal is BLOCKED by BF1.
- **HELD-only rows:** semantic statuses, order, reasons, empty evidence/metrics, false claims, and null failures match the existing law record. PASS/FAIL publication remains forbidden. Exact digest identity is BLOCKED by BF2.
- **Lifecycle, cleanup, and rollback:** cleanup and no-retry intent is conservative; construction and post-publication rollback are BLOCKED by BF1.
- **Local-only evidence boundary:** PASS in scope. Observations are forbidden from Git and from carrying prompt/output text, token arrays, model/tokenizer bytes, environment values, or private paths. They carry only sanitized digests, counts, timings, and four false evidence flags.
- **Launch and authority:** `run_authorized` is literal `false`; model test authorization is also false. Implementation SHA, implementation review, design review, dependency clearance, and Coordinator release remain stops. Exact dependency identity and no-network enforcement are BLOCKED by BF3–BF4.
- **No changed science or permissions:** PASS. All new execution controls are `[PROPOSED]` diagnostic controls, not scientific bars. No protected seed, score, qualification, readiness, evidence promotion, custody grant, or model-selection authority is added.
- **Public safety:** PASS. Complete package preflight returned 27 fixed-regex findings representing seven unique substrings wholly inside required public Git/SHA identities; manual classification found no contact, credential, private path/value, prompt/output, token array, protected seed, score, or scientific output. Gitleaks returned zero findings.

## Non-blocking findings

None beyond the blocking set.

## Exact disposition and next authorized role

Return this single combined BLOCK to **WORKFLOW COORDINATOR** for one narrow ARCHITECT remediation of BF1–BF5, followed by persistent-CRITIC rereview of one exact immutable package. Preserve the deterministic public prompts, exact public model/runtime identities, seven-field receipts, HELD-only semantics, local-only evidence boundary, `run_authorized=false`, and every existing custody/scoring/readiness hold.

No model run, tokenizer/model acquisition, private custody, protected-seed access, scoring, science, implementation, merge, readiness decision, or run release is authorized by this review.

## Public-safety and execution attestation

The review used only committed public repository bytes, static parsing, canonical hashing, Git identity validators, and import of the cleared public seam for law-row validation. No project workload, model, tokenizer, observation backend, private input, protected seed, custody material, scoring process, or network acquisition was accessed or executed. No implementation, merge, readiness decision, or run authorization occurred. Review-range preflight returned two fixed-regex findings representing the same required public SHA-256 value in commit-parent and combined-range domains; manual classification found no prohibited material, and Gitleaks returned zero findings.

Remote equality and worktree cleanliness will be reverified after publication.
