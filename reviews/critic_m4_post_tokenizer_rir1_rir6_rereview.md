# CRITIC M4 Post-Tokenizer RIR1–RIR6 Rereview

Date: 2026-08-22 EDT

Regime: B

Role: authoritative persistent CRITIC

Terminal state: **COMBINED BLOCK**

## Immutable intake and verified evidence

- Package head: `taskbuilder/m4-post-tokenizer-rir1-rir6-remediation @ 656a0fa611619a9d19158efae4675ef165769434`
- Implementation result: `cf80b99862cf8bd1f6ee3145e98f543f61121daa`
- Handoff/routing result: `e90940edba2726c1dc676e0d4a15554c0966c2f7`
- Prior authoritative BLOCK: `critic/m4-post-tokenizer-ir1-ir7-rereview @ 1a8a4557715d7d3e07fd507ca17f335df7845aef`
- Helper checkout receipt SHA-256: `724eff31deaf1ff9c5ecdeb7638cf58947e191c572cfa385e3a6c4e387d8c4b0`

The canonical manifest validates. All 14 declared raw artifact hashes, all 63 inventory rows, and all 25 contained JSON sidecars reproduce exactly. Base, implementation, routing/scan, manifest, and remote heads form the declared ancestry. The changed tree is confined to the expected implementation/test/wrapper, inventory cascade, and handoff topology; the tokenizer package, consumed PASS pair, design inputs, and all unrelated bytes remain preserved.

The exact custody-free integration wrapper ran 45/45 PASS locally, including the 42-cell lifecycle test. Docker was unavailable, so the reported pinned OCI 45/45 remains corroborating rather than independently rerun. The tokenizer materializer and 37-test module are byte-identical to the banked cleared source; no tokenizer/materializer invocation occurred. The six mutation kills are described but have no committed mutant runner/transcript, so they remain an attestation; the selected tests do exercise the named boundaries.

RIR3 rollback-state recapture, RIR5 sequence/close/13-negative dispatch, and the ordinary RIR6 `step()` frozen-provider path are banked closed. Pair prevalidation and failure cleanup materially improve RIR1. The following related residuals remain.

## RRIR1 — Public verified-fanout entry bypasses reconciliation

`VerifiedFanoutInput` is publicly constructible and exported, while `FanoutCoordinator.step_verified` accepts it without proving provenance or revalidating its frozen identities. It checks only pair identity and request context before invoking both backends. It does not bind the candidate/peer views to `expected_sha256`, validate `length` against encoded bytes, validate stop identity, or prove the object came from `_phase_one` for the same request.

A direct production-path reproduction constructed a one-token view with a false 64-zero expected digest, false length `1`, and false stop metadata. `step_verified` returned `PASS` and called both backends. The fixture also creates cached phase-one objects under `verify-*` operation IDs and uses them for different fanout requests without a request digest binding.

Make the verified capability private/unforgeable or revalidate its complete canonical content and bind it to the exact eventual request identity. No public route may skip ordered sanitized-result, private rederivation, stop, digest, length, and request-correlation checks.

## RRIR2 — PASS law validation accepts false law claims

The new exact metric key/type checks do not enforce the law predicates or even elementary value domains. A five-row PASS set was accepted with negative/out-of-domain L7/L8/L10/L14 metrics and L18 values `governed_seed_count=0`, `arms_present=0`, and `controls_passed=false`. This directly contradicts the claimed PASS meanings and RIR4's required exact five-law row semantics.

Bind PASS to each law's authoritative thresholds, domains, arm/seed/control predicates, and evidence semantics, or keep PASS unavailable until the full lawful artifact validator supplies those decisions. Type/finiteness alone cannot authorize `claim_made=true`.

## RRIR3 — Lifecycle history is not part of the validated invariant

`validate_state` checks `_state` only. `_used_episode_ids` is omitted from durable state and `restore` checks only that it is a set, not that its members are nonempty strings or that it is consistent with `episode_id` and `reset_ordinal`. A restored snapshot can therefore describe a later episode while carrying an empty history, allowing an already-used episode ID to be accepted again even though every public state check passes.

Validate the complete lifecycle identity, including episode history, on capture/restore and every operation, and mutation-kill history/state inconsistencies and episode reuse after restoration.

## RRIR4 — Factory accepts an already non-live backend

Construction binds session identity and verifies disposal after failures, but the successful path never requires `backend.is_live()` before returning the adapter/pair. A constructor may return an already disposed backend with the correct session identity and be accepted as a usable production adapter.

Require and test live-state attestation for each constructed backend before exposing either half, while preserving verified disposal and zero-residue behavior on all pair failures.

## Public safety and disposition

Preflight counts through the exact package head reproduce the declared 107 fixed-regex personal-contact and 20 gitleaks-domain findings. Manual review classifies the former as phone-shaped substrings wholly inside required public hashes/commit identities and the latter as duplicated matches of three public source/test/tokenizer identities. No credential, contact data, private path/value, custody content, token arrays, seeds, scores, or scientific output were found; none was silently suppressed.

**COMBINED BLOCK.** Bank all exact identity evidence and the closed RIR3/RIR5 portions. Return the single RRIR1–RRIR4 batch through WORKFLOW COORDINATOR. No held access, execution, durable-state mutation, merge, publication, or gate decision occurred.
