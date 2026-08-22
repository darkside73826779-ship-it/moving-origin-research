# CRITIC review — M4 final pre-scoring crash-cart beta implementation

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

## Immutable intake

- Package ref/head: `taskbuilder/m4-final-prescoring-crash-cart-beta-implementation` at `05e83a92dec4bec747c65ab279b841ed8d445f61`.
- Implementation result: `738878ab3618d6058f0725caa7e3f0f0388cb59f`.
- Substantive packaging/classification result: `169188c2621a2ba27816630713ce7136909cda0e`.
- Routing/handoff result: `05e83a92dec4bec747c65ab279b841ed8d445f61`.
- Canonical manifest: `handoffs/manifests/m4_final_prescoring_crash_cart_beta_implementation/20260822T160000Z_task_builder_to_workflow_coordinator.json`.
- Coordinator preflight-classification authority: public `main` at `82416ec6bd40dbc4c2755d6ebb42ea5dbd664721`; its classified artifact is byte-identical in the route.
- Corrected base: `a66b7ccc88e54305d231fd0b75681c09fd846555`.

Remote equality, exact base ancestry, the implementation-to-packaging-to-route chain, and helper-compatible checkout reproduce. The common handoff validator returns `VERIFIED`. All 21 listed artifact hashes, eight listed sidecars, LF constraints, and the authority byte identity reproduce. Source, tests, contracts, and sidecars are unchanged between the implementation result and routing head, so the banked 8/8 custody-free evidence remains identity-applicable.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

The package preserves `run_authorized=false`, HELD-only law semantics, and the standing no-model/no-custody/no-scoring holds. The block is implementation completeness and fail-closed validation quality, not a scientific or readiness judgment.

## Batched findings

### BF1 — the returned source is a planning stub, not the authorized exact beta implementation

`src/m4_final_prescoring_crash_cart.py` implements public prompt/fixture generators, a schedule tuple, HELD rows, a small report guard, and the no-start guard. It does not implement or bind the cleared beta's production-seam fanout/lifecycle, paired warmup barriers, episode resets, independent measured RNG insertion, request/receipt chains, bounded queue and deadline, telemetry, rollback, sanitation, deterministic rendering/export, or mandatory cleanup. `tools/run_m4_final_prescoring_crash_cart.py` is correctly fail-closed but unconditionally exits before exercising any of those implemented contracts. The promoted-beta authority required exact source, tests, schemas, launch contract, wrapper, and custody-free synthetic/public-fixture evidence for all success and staged failure paths; those return requirements are not met.

The copied gate still leaves the production runner/integration/factories, semantic validator, deterministic renderer, focused implementation test, combined tree, OCI, dependency, gofast, implementation-review, and release identities `UNBOUND`. No separate implementation inventory binds the missing executable identities. That is safe for no-start, but it cannot be classified as the exact beta implementation.

### BF2 — `validate_terminal` accepts fabricated and incomplete stage evidence

The semantic guard at `src/m4_final_prescoring_crash_cart.py:71` does not invoke the report schema and checks only a small subset of the five-stage union. Focused custody-free probes were accepted when they should fail closed:

- `PRE_ACTIVE_TERMINAL` with non-empty resource samples, fabricated trends, replica `MATCH`, and `failure_stage=CLEANUP`;
- `PARTIAL_ACTIVE_TERMINAL` with no complete warmup or active window, complete-looking trends, and `failure_stage=PRE_START`;
- `POST_ACTIVE_TERMINAL` with zero resource samples and `failure_stage=WARMUP`; and
- `COMPLETE_ACTIVE_TERMINAL` with 64 empty row objects but no samples, trends, cleanup, public-safety, export, law, or replica evidence.

The guard does not cross-check evidence stage against failure stage, validate partial-role null projections, reject fabricated telemetry/trends/replica fields across all stages, or require every complete-terminal condition. This defeats the design's central no-fabricated-later-evidence rule.

### BF3 — warmup/reset/ordinal and required adversarial evidence are incomplete

The warmup generator reproduces the four literal-LF byte strings and hashes, the schedule produces 64 offsets ending at 30 seconds, and the HELD projection reproduces 974 bytes with SHA-256 `bb2d5f838c54c404dd73d0c697ba6f45cd983fb7e5a7bb97a36b38570267b81f`. Those mechanics are clear.

However, `warmup_plan()` binds only ordinal, prompt/hash, max tokens, temperature, seed, and prefix-caching. It does not bind the remaining generation controls, RNG domain, equal-role barriers, timeouts, seven-field receipt/state chains, warmup reset, clean barrier, measured reset, measured receipt ordinals 0–63, or the no-priming invariant. `public_fixture()` generates prompts but the package contains no required 64-entry prompt-hash inventory. The eight-test suite checks only representative generator and guard behavior; it omits the required skipped/asymmetric warmup, protected substitution, RNG/KV/session carryover, one-role failure, timeout/no-retry, warmup-exclusion, rollback, cleanup, and complete five-stage success/failure regressions.

### BF4 — the canonical raw inventory omits one changed policy file

The exact base-to-route range modifies `.gitattributes` to add the package's LF rules, but `.gitattributes` is absent from the manifest `artifacts` map. The manifest otherwise reproduces, and self-exclusion is expected, but this non-self changed byte sequence must be included for a complete canonical inventory.

## Clear boundaries and focused evidence

- The wrapper returns exit 2 with `RUN_AUTHORITY_ABSENT` before runtime, model, tokenizer, OCI, WSL2, gofast, filesystem-custody, or subprocess access.
- The production integration seam is unchanged by the exact implementation range.
- All listed raw hashes and sidecars reproduce; the only inventory gap is BF4.
- Terminal public preflight over the exact base-to-route range reports 137 findings: 129 fixed-regex numeric substrings and eight gitleaks detections. Manual review maps them to the already classified public commit/digest/model/control identities; no credential, private path/value, protected input, prompt/token array, model/tokenizer bytes, score, or scientific result was found. The two `git diff --check` notices are intentional Markdown hard breaks in the byte-identical Coordinator classification artifact.
- No model/tokenizer/OCI/WSL2/gofast workload, held access, custody, scoring, qualification, science, state/provenance mutation, merge, publication, readiness declaration, retry, or gate action occurred.

## Required remediation and disposition

Return one narrow implementation correction that:

1. implements and identity-binds the complete non-executing beta seam required by the promotion authority while preserving unconditional no-start until separately released;
2. composes JSON Schema validation with a complete semantic validator for every five-stage success/failure projection and adds all required custody-free regressions;
3. binds the complete warmup/clean-barrier/reset/RNG/receipt/ordinal contract plus the exact 64 public fixture identities and deterministic lifecycle/rollback/cleanup/render/export behavior; and
4. inventories `.gitattributes` with the complete changed artifact closure.

Return **COMBINED BLOCK** to **WORKFLOW COORDINATOR**. The exact next recipient after Coordinator intake is **TASK BUILDER** for one batched BF1–BF4 implementation correction. All execution, custody, scoring, science, merge, publication, readiness, and gate holds remain binding.
