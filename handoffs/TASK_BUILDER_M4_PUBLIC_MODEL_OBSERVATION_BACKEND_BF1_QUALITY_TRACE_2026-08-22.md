# TASK BUILDER M4 public observation backend BF1 quality trace

Date: 2026-08-22

Regime: B

Result: COMPLETE — pending persistent-CRITIC rereview

Implementation: `46252865c5a13a997396ac7520eb3c06d8f541e1`

## Delta-only closure

| Requirement | Production branch | Production-path test | Evidence |
|---|---|---|---|
| Reject authenticated context/count below one before engine access | `PublicModelObservationBackend._decode_private_view`: `min(count, tokens.context_length) < 1` | `test_zero_count_private_view_is_rejected_before_engine_and_restored_exactly` through the public adapter path | `BACKEND_DECLARED_FAILURE`, `backend_code=SYNTHETIC_REJECTED`, engine calls 0, stage empty |
| Preserve exact adapter/backend state and stage inventory | backend `_operate` plus cleared adapter transaction restoration | same zero-count test captures and compares complete pre/post adapter transaction and backend snapshot | exact equality including stage inventory; no temp/final artifact |
| Enforce bound schema minimum independently | `_validate_observation`: `input_token_count < 1` | `test_observation_validator_enforces_positive_input_count` | zero input count raises `OBSERVATION_EVIDENCE_BOUNDARY_FAILURE` |
| Prove the lower bound is test-sensitive | `ZERO_COUNT_LOWER_BOUND_REMOVED` changes `< 1` to `< 0` in a disposable checkout | exact zero-count adapter-path target | mutant KILLED with target assertion failure, exit 1 |
| Remove Windows legacy long-path dependence without changing semantics | mutation runner copies only source, seam, test package marker, and focused test module | Windows mutation replay from the canonical long worktree | baseline 19/19; 7/7 mutants KILLED; no copy failure |

Ordered zero-count trace: adapter request/private-view authentication → backend prior-state and prompt checks → private-view framing → decoded unsigned count → positive count/context lower-bound rejection → seven-field FAIL receipt with registered code → adapter `BACKEND_DECLARED_FAILURE` → exact backend and stage rollback. The stub engine, sanitizer, temp writer, rename, and publication branches are never reached.

## Exact verification

- Windows identity-first focused suite: 19 discovered; 18 PASS; one host-privilege directory-symlink skip.
- Ubuntu 24.04 WSL2 identity-first focused suite: 19/19 PASS, including the linked-stage case.
- Windows and WSL2 deterministic mutation replay: baseline PASS; 7/7 KILLED; zero survivors/instrument failures; source restored byte-for-byte after every mutant.
- Mutation contract is canonical, sidecar-bound, and checked by the executable runner before baseline or mutation work.
- `run_authorized=false` remains exact. No model, tokenizer, private custody, protected input, scoring, qualification, science, merge, publication, readiness, or gate action occurred.

All banked CLEAR identities and behaviors outside BF1 remain byte-identical or regression-covered and passing.
