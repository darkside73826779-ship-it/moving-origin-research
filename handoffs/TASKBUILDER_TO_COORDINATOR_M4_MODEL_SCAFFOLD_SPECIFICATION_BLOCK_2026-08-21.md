# TASK BUILDER to WORKFLOW COORDINATOR — M4 Model Scaffold Specification Block

**Date:** 2026-08-21

**Regime:** B

**Gate served:** M4 model-agnostic scaffold-with-stubs implementation

## Authoritative inputs reviewed

- Rebecca implementation release: `coordinator/m4-scaffold-rebecca-implementation-release` at `81bc7991b8c05672b84cc5b52a3a6a321fa047c2`.
- Approved ARCHITECT head: `architect/m4-model-agnostic-scaffold` at `2c655fbb1bac6ba419327198062c5230e87c44db`.
- Approved ARCHITECT result: `b84f470af415ead5ae36ca01bb1d8e7394e7cc97`.
- Final persistent-CRITIC CLEAR: `critic/m4-model-agnostic-scaffold-rf1a-rereview` at `e76ecb98e80e5bded57afe3d318a32fcfbbfe463`.
- Primary specification: `specs/m4_model_agnostic_scaffold_spec_v1.md`.
- Executable fixtures: `specs/data/m4_model_scaffold_executable_fixture_v1.json` and `specs/data/m4_model_scaffold_rf1_rf3_fixture_v1.json`.
- Machine-readable task boundary: `specs/data/m4_model_scaffold_task_boundary_v1.json`.

## Disposition

**SPECIFICATION BLOCK — no implementation started.**

The committed fixtures fully determine their stored canonical artifacts and digests, but the released contract does not define enough callable behavior to implement the adapter scaffold without inventing rules.

## Exact specification gaps

1. `reset_episode(reset_request_bytes)` has no committed reset-request schema, canonical fixture bytes, field names, digest contract, or validation/failure behavior.
2. `snapshot(snapshot_request_bytes)` has no committed snapshot-request schema, canonical fixture bytes, field names, digest contract, or validation/failure behavior.
3. `initialize(manifest_bytes, dependency_manifest_bytes)` names a dependency-manifest input, but no schema or generic validation contract is committed; only two concrete dependency objects exist.
4. The nine adapters are required as callable stubs, but complete manifest/request bases are committed only for candidate and peer, plus a frozen construction. No deterministic manifest/request constructors are specified for oracle, empty, permuted, shuffled, naive, or specificity.
5. “Stub functions are arithmetic specified by the fixture,” but the fixture supplies expected outputs for one base request rather than arithmetic functions for valid varying requests. Implementing callable adapters beyond exact lookup would require inventing formulas; restricting them to exact fixture lookup and choosing a rejection code would also invent behavior.
6. `SELF_MODEL_REPRESENTATION` and `NON_SELF_PROXIMAL_COMPONENT` hooks require behavior and receipts, but no schema-valid positive hook request, perturbation payload, hook-receipt constructor, or expected digest is committed.
7. The adapter’s state-transition digests are fixed for stored rows, but no state-object construction/hash rule is specified for callable lifecycle execution. Hard-coding row digests or defining state fields would be an invented rule.
8. Atomic publication prescribes recovery semantics but does not define the public callable contract or the names/layout for previous-pair and `.incomplete` artifacts. Exposing or testing those paths requires inventing data/file names.

## Files and verification status

- Implementation files changed or created: none.
- Tests or diagnostics run: none.
- Seeds accessed: none.
- Scientific specifications, thresholds, state, and provenance modified: none.
- This handoff is the only TASK BUILDER-authored artifact for the blocked work item.

## Holds

No implementation, invented remediation, tests, diagnostics, real-model activity, non-synthetic execution, scoring, protected-seed access or exposure, native-CUDA L8 (`go faster`), serial-CPU L8 (`GO!`), scientific or threshold change, state/provenance mutation, rerun, gate decision, or merge is authorized.

## Exact next recipient and route

Return to **WORKFLOW COORDINATOR**, which may verify the committed lineage and route the durable block to the persistent **ARCHITECT** for deterministic specification closure. Any amended operative contract remains subject to the required persistent-CRITIC review and Rebecca authority before TASK BUILDER implementation resumes.

## Public-repository safety attestation

Public-safety scan: gitleaks scanned the complete two-commit introduced range and found zero leaks. Credential, secret, private-key, environment-dump, and private-absolute-path regex review found zero prohibited content. Email-pattern review found four commit-metadata matches: the repository's existing GitHub noreply author identity and the non-personal TASK BUILDER role identity; both were classified acceptable, not personal contact details. Manual content review found only repository SHAs, repository-relative paths, governance terms, and the durable specification block, all classified acceptable. `git diff --check` passed.
