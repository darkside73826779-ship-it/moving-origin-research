# CRITIC M4 Post-Tokenizer RRIR1–RRIR4 Rereview

Date: 2026-08-22 EDT

Regime: B

Role: authoritative persistent CRITIC continuation

Terminal state: **COMBINED BLOCK**

## Immutable intake and banked evidence

- Package head: `taskbuilder/m4-post-tokenizer-rrir1-rrir4-remediation @ 1990b387d510cfc690b8bfd156c551751007aea5`
- Implementation: `f44ad96b133096d0096a5c43574f47d69f489756`
- Handoff/routing: `6501f24f041af0bf4d4d3923d2a5b6b2696772e1`
- Prior BLOCK: `critic/m4-post-tokenizer-rir1-rir6-rereview @ ba3bd68f111370331444a21cd73dad1f6004fe5b`
- Helper checkout receipt SHA-256: `904c8d827aaf927f33a985abdf21ec991f83ce79a2f764e0bd31955e4b267425`

The canonical manifest validates. All 14 declared artifacts, all 63 inventory rows, and all 25 contained sidecars reproduce exactly. Base, implementation, routing/scan, terminal manifest, and remote head have the declared ancestry. The changed tree is confined to the expected implementation/test/wrapper, inventory cascade, and handoff topology; tokenizer sources, the consumed PASS pair, package, design artifacts, `.gitattributes`, and unrelated bytes remain preserved.

The fresh custody-free integration wrapper ran 49/49 PASS locally and retains the 42-cell lifecycle matrix and 13 fixture negatives. The exact pinned OCI 49/49 and tokenizer 37/37 results remain corroborating because Docker was unavailable and no tokenizer/materializer operation was invoked. RRIR2 summary PASS now fails closed as `LAW_PASS_UNAVAILABLE`; exact HELD/FAIL/NOT_RUN shapes and domain guards remain. RRIR3 durable episode history and restored reuse protection are materially closed.

## RRR1 — The internal verified-fanout capability remains forgeable

Renaming the capability and execution method with leading underscores removes them from the advertised public API, but does not make the capability authentic. Module-visible `_VerifiedFanoutInput` can still be constructed directly and passed to `_step_verified`. `_validate_verified` proves only internal self-consistency; it has no coordinator-issued identity and cannot prove that the object came from `_phase_one`, the committed sanitized rows, or provider rederivation.

Production-path reproduction encoded an arbitrary 1024-token prompt and arbitrary stop array, constructed a fully self-consistent `_VerifiedFanoutInput` with the exact request digest, installed a provider that raises if called, and invoked `_step_verified`. It returned `PASS` and both backends were called; the provider and sanitized rows were never consulted. The new test covers malformed capabilities through patched public `step`, but not a fully self-consistent direct forgery.

Use an unforgeable coordinator-issued capability (for example, a private identity registry consumed once) or collapse execution into the public reconciler so no separately callable path can authenticate caller-created content.

## RRR2 — Throwing liveness probes can leave live residue

`AdapterFactory._attest_live` catches an `is_live()` exception, calls `dispose()`, and immediately raises the role-specific NOT_LIVE code. Unlike `_dispose_verified`, this branch does not verify the disposal postcondition. A backend whose liveness probe throws and whose disposal is a no-op remains live while the factory reports only `CANDIDATE_BACKEND_NOT_LIVE`/peer/control equivalent.

This was reproduced with the production `_attest_live` path: the probe raised, disposal returned without changing live state, and the caught terminal state was `CANDIDATE_BACKEND_NOT_LIVE` with backend `live=true`. The committed test uses a cooperative disposer and therefore does not cover this residue.

Require an authenticated disposal receipt or independently verified non-live identity on this path. If cleanup cannot be verified, project `BACKEND_ROLLBACK_FAILURE` and never claim zero residue.

## RRR3 — The declared executable 11/11 mutation transcript is not retained

The quality trace contains a prose table naming mutations, generic killing-test labels, and `KILLED` results. It does not retain mutant patches/identities, fully qualified exact commands (the stated command contains the literal placeholder `<test>`), per-mutant exit/output records, or a runner that reapplies and verifies the eleven changes. Consequently the claimed executable 11/11 transcript cannot be independently executed or authenticated from the canonical package.

Retain a custody-free deterministic mutation runner or exact per-mutant patch/command/result identities, and prove clean restoration between mutations. Preserve all presently passing regression evidence.

## Public safety and disposition

Package scan classifications were independently reviewed: fixed-regex contact matches occur within required public immutable hashes/commit identities, and gitleaks-domain matches are public source/test/tokenizer digests. No credential, contact data, private path/value, custody content, token arrays, seeds, scores, or scientific output were found or suppressed.

**COMBINED BLOCK.** Bank exact identity/inventory evidence, RRIR2 law fail-closed closure, RRIR3 lifecycle-history closure, 49-test regression, lifecycle/fixture coverage, and all preserved holds. Return one RRR1–RRR3 batch through WORKFLOW COORDINATOR. No held access, new operation, durable-state mutation, merge, publication, or gate decision occurred.
