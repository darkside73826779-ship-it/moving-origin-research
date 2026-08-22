# CRITIC final rereview — M4 public observation backend BF4-R1

Date: 2026-08-22 EDT

Regime: B

Scope: BF4-R1 correction only

## Immutable intake

- Correction route: `architect/m4-public-model-observation-backend-bf4-r1-correction` at `89bf97e53af7a8852fc6c3dc67623fc14d11650e`.
- Substantive result: `515e1d553858f4675a5ee5f347ffbc395b8fdd78`.
- Canonical manifest: `architect/m4-public-model-observation-backend-bf4-r1-correction-manifest` at `d7c08e7a984be38cd378769db8a4c26e36e8c00b`.
- Prior authoritative BLOCK: `632426122e8d3d308640b05f4484b61404667c2a`.
- Review branch: `critic/m4-public-model-observation-backend-bf4-r1-final-rereview`.

The standard helper accepted the exact package and its handoff-only routing tail. The canonical manifest validates `VERIFIED`; all six artifact hashes and the changed JSON sidecar reproduce. Ancestry, LF, `git diff --check`, and `git fsck --full --strict` pass.

## Verdict

- **BF4-R1: CLEAR**
- **BF1/BF2/BF3/BF5: BANKED CLEAR**
- **COMBINED VERDICT: CLEAR**

This is a design/repository-quality clearance only. It is not implementation, model execution, scoring, science, readiness, merge, run authorization, or a project gate decision.

## Delta verification

- The design now states the exact classifier semantics: errno 101 (`Network is unreachable`) exits 0; an unexpected errno exits 2; an unexpected successful connection exits 3.
- The test contract replaces `outbound_socket_connect_errno_101_exit_one` with `outbound_socket_connect_errno_101_exit_zero`.
- The three duplicated positive cases—constructor liveness, eight-field HELD digest, and OS namespace before Python—are each reduced to one occurrence. The three duplicated required assertions—stage-inventory restoration, exact HELD projection, and OS network denial—are each reduced to one occurrence. The resulting positive-case and assertion arrays are unique.
- The launch contract and sidecar are byte-identical to the prior BLOCK. Its bound negative program still maps errno 101 to exit 0, unexpected errno to exit 2, and unexpected connection to exit 3.
- Independent custody-free execution reproduced positive namespace exit 0 and errno-101 denial classifier exit 0. No model or tokenizer was accessed.

No residual finding remains in BF4-R1 scope.

## Banked boundaries and safety

BF1, BF2, BF3, BF5, launch argv, model/runtime/prompt identities, receipt shape, HELD-only semantics, local-only evidence, dependency CLEAR, and `run_authorized=false` remain banked and unchanged. Delta preflight returned two fixed-regex matches wholly inside unchanged required public model/tokenizer SHA-256 identities; manual review found no prohibited content, and Gitleaks returned zero findings.

## Disposition

Return this COMBINED CLEAR to **WORKFLOW COORDINATOR**. All existing holds remain binding; the Coordinator determines the next role.

Remote equality and worktree cleanliness will be reverified after publication.
