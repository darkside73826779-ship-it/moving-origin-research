# CRITIC rereview — M4 public observation backend BF1–BF5 remediation

Date: 2026-08-22 EDT

Regime: B

Scope: delta-only BF1–BF5 rereview

## Immutable intake

- Remediation route: `architect/m4-public-model-observation-backend-design-bf1-bf5-remediation` at `fc22c10dfe309031705eb81e0dd358c1e6c5c053`.
- Substantive result: `171677b92597125d05004bbecc51a017687967d0`.
- Canonical manifest: `architect/m4-public-model-observation-backend-design-bf1-bf5-remediation-manifest` at `79baf58e692ee8c6b9f286c4b8964d55638b1c69`.
- Prior authoritative BLOCK: `55bf6de1ba31c295e5664170eae78dbd457a57a8`.
- Banked dependency CLEAR: `4cdb5d89945b603c20cdd19233079be14b65946b`.
- Review branch: `critic/m4-public-model-observation-backend-design-bf1-bf5-rereview`.

The standard helper accepted the exact substantive/routing topology. The routing-only tail adds only the named handoff. The canonical manifest validates `VERIFIED`; all ten artifact hashes and all three changed JSON sidecars reproduce. Ancestry, LF bindings, `git diff --check`, and `git fsck --full --strict` pass.

## Verdict

- **BF1: CLEAR**
- **BF2: CLEAR**
- **BF3: CLEAR**
- **BF4: BLOCK**
- **BF5: CLEAR**
- **COMBINED VERDICT: BLOCK**

This is a design/repository-quality result only, not implementation, model execution, scoring, science, readiness, merge, or gate authority.

## Closed findings

- **BF1:** The constructor is explicitly live before engine load, preserving cleared factory attestation. Internal observation failures traverse the unchanged seven-field seam through registered `SYNTHETIC_REJECTED`. Capture/restore now binds the complete stage inventory and removes operation-owned final artifacts for every adapter rejection and post-return private-view mutation.
- **BF2:** Independent reproduction of the five ordered eight-field `held_law_projection()` rows yields exactly 974 canonical bytes and SHA-256 `bb2d5f838c54c404dd73d0c697ba6f45cd983fb7e5a7bb97a36b38570267b81f`, matching the corrected contract.
- **BF3:** The dependency authority now binds exact substantive result `4993711fa32ffe9ab3b2dabb2b5d5615182c6e90`, routing head `6d8175edb63cf6ec03c0904d640ae6f946ebcf16`, manifest head `95cd17deabba6a0c84c02e26c408023b989e79bc`, and persistent-CRITIC CLEAR `4cdb5d89945b603c20cdd19233079be14b65946b`. Authenticated remote identities and ancestry reproduce.
- **BF5:** The handoff LF rule moved into the substantive result; the routing tail is helper-compatible and handoff-only.

## Residual blocker

### BF4-R1 — The network-denial smoke has contradictory terminal semantics

The canonical launch contract is executable and its enforcement works: exact `/usr/bin/unshare` from `util-linux 2.39.3-9ubuntu6.5` reproduces at 43,624 bytes, mode 0755, SHA-256 `51bcc77ba5db162c80028f861f0a2770d728c1de80773816d863f28d7a817adb`; the new user/network namespace positive smoke exits 0; and the outbound socket attempt receives errno 101 and exits 0 through the bound Python program.

However, the changed test contract records `outbound_socket_connect_errno_101_exit_one=true`, and the changed design prose says the negative “exits one with errno 101.” The launch contract instead requires `expected_exit: 0` and its bound program explicitly exits 0 on errno 101, 2 on an unexpected errno, and 3 on an unexpected connection. The test contract also duplicates each of the three newly added positive cases and each of the three newly added required assertions, so it is not a canonical unique affected-test inventory.

Impact: BF4's OS enforcement mechanism is sound, but its machine-readable test oracle and normative prose disagree with the canonical executable result. An implementation can reject the correct denial or accept the wrong terminal depending on which changed artifact it follows.

Smallest remediation: change the test-contract key and design prose to require errno 101 with exit 0, remove the duplicated positive cases and required assertions, regenerate their sidecars/handoff/manifest, and rerun only the two custody-free namespace smokes plus JSON/sidecar validators. Do not change the working launch argv or expand scope.

## Banked boundaries and safety

Unchanged model/runtime/prompt identities, seven-field receipt shape, HELD-only semantics, local-only evidence boundary, `run_authorized=false`, and cleared dependency evidence remain banked and were not reopened. Complete delta preflight returned eleven fixed-regex findings representing three unique public Git/SHA identities; manual review found no prohibited material, and Gitleaks returned zero findings. No model, tokenizer, private custody, protected seed, scoring, science, implementation, merge, readiness action, or gate decision occurred.

## Disposition

Return this single narrow BLOCK to **WORKFLOW COORDINATOR** for ARCHITECT remediation of BF4-R1 only, then route the exact corrected delta to the current persistent CRITIC. All existing holds remain in force.

Remote equality and worktree cleanliness will be reverified after publication.
