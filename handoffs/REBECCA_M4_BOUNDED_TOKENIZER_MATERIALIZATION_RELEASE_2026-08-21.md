# Rebecca Release — M4 Bounded Local Tokenizer Materialization

**Date:** 2026-08-21  
**Regime:** B  
**Status:** RELEASED FOR ONE BOUNDED LOCAL MATERIALIZATION AND SANITIZED EVIDENCE PACKAGE

Rebecca approves execution of the CRITIC-cleared Work Item B tokenizer-materialization contract for the sole purpose of proving identical tokenizer-level inputs for the isolated candidate and matched-peer instances.

## Cleared authority and design

- Base local-custody authority: `coordinator/m4-scaffold-rerelease-tokenizer-custody` @ `45d40d8b688fb7f44098d235df7f31cca1aa3b31`
- RF1 identity authority: `coordinator/m4-tokenizer-rf1-identity-approval` @ `9acd997bc2ee8680f4441a589923ee0aa96e60f7`
- Cleared ARCHITECT package: `architect/m4-tokenizer-materialization-spec` @ `ed25e3b4811a9024c8b7d7a0120a8fc073748004`
- Final combined CRITIC CLEAR: `critic/m4-tokenizer-rf1-final-combined-rereview` @ `ff3976dd58009a8c6d0d8fd2cddc787fc96b63bc`
- CRITIC artifact: `reviews/critic_m4_tokenizer_rf1_final_combined_rereview.md`

## Authorized execution

TASK BUILDER may perform exactly one bounded local tokenizer-materialization operation using the approved immutable local custody artifact and the exact committed constructors, schemas, runtime identities, commands, and tests. The operation may:

1. Resolve only the approved local custody handle, with no directory search or fallback.
2. Verify the approved tokenizer and `tokenizer_config.json` identities before use.
3. Render the pre-registered chat-template inputs and construct the three specified token-ID arrays.
4. Verify encode/decode identity, special-token behavior, and the fixed stop array `[151645]`.
5. Compute the prescribed canonical array lengths and digests.
6. Produce the exact sanitized PASS, BLOCKED, or FAIL evidence package.
7. Commit and push only the permitted sanitized public metadata and handoff artifacts after the required public-safety scan.

TASK BUILDER must stop fail-closed on any identity, custody, runtime, constructor, schema, digest, or test mismatch. No alternate artifact, revision, runtime, command, array construction, or retry may be substituted.

## Route after execution

TASK BUILDER returns the committed sanitized package through WORKFLOW COORDINATOR to the persistent CRITIC for independent execution-evidence review. CRITIC CLEAR returns through Coordinator to Rebecca.

## Holds preserved

This release does not authorize model inference, serving, candidate/peer qualification, Q2 numeric-band selection, EF3 battery binding, diagnostics, scoring, protected-seed access, training, adapter changes, scientific threshold/control/battery changes, model or tokenizer publication, STATE/provenance mutation, rerun, or merge. Model/tokenizer bytes, complete private token arrays, custody values, and local paths remain local-only and must never enter Git.
