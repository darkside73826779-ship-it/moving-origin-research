# JUDGE ruling — M4 post-tokenizer mutation-clear implementation-readiness reconsideration

Date: 2026-08-22 EDT
Regime: B
Publication status: PENDING_RECORDER_CUSTODY

## Disposition

**CLEAR — PRIOR INSTRUMENT FAILURE CLOSED; ENGINEERING READINESS ADEQUATE FOR RETURN TO REBECCA.**

The corrected mutation apparatus closes the sole blocking reason in the durable prior JUDGE ruling. The production implementation and its production tests are byte-identical to the accepted package, and the corrected public evidence is sufficiently fail-closed and reproducible to return the package to Rebecca for a later, separate integration decision.

This ruling is a bounded, non-scoring implementation-readiness determination. It is not an operative gate, merge authorization, scientific result, model or tokenizer qualification, scoring authorization, or publication decision.

## Exact authority and intake

- Canonical v4 route: `coordinator/m4-post-tokenizer-mutation-clear-judge-route-v4` at `3b5fbaa74668e563ea0005b7e7488473976d0b95`.
- Canonical v4 manifest: `coordinator/m4-post-tokenizer-mutation-clear-judge-manifest-v4` at `b9e37b5647624e28452a1acd334e1de62528d933`.
- Corrected package: `taskbuilder/m4-post-tokenizer-mutation-apparatus-remediation` at `b751ef71b3f6c7dda126ce1a28af6f0d29b572dd`.
- Corrected apparatus implementation: `6d4089ef95a14fb6b1d46c96ebf452733ff5cd98`.
- Independent CRITIC result: `e67f0538640334e1db6b5397bce808f098d2e6ac`.
- Accepted production baseline: `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`.

The repository validator accepted the canonical Coordinator-to-JUDGE manifest and its five exact Git-blob artifacts. The declared ancestry is linear from the accepted baseline through the corrected implementation, package, independent review, and v4 route. Remote equality reproduced for the route, manifest, corrected package, and CRITIC refs. The v4 routing tail adds only its authority handoff; the manifest tail adds only the canonical manifest.

The historical ruling binding also reproduces directly from `recorder/m4-post-tokenizer-implementation-readiness-ruling` at `32f72c2bb708d96060eb636cb4cf7a673c85ec24`: ruling path `docs/rulings/judge_m4_post_tokenizer_implementation_readiness_ruling.md`, Git blob `3841cfc260ff9c639e32a1119cb4d1041c0c77eb`, 5,140 raw bytes, SHA-256 `ca77333e20c8a2f6accbd32d2f79b9ca3b256f8050faa7981f7f14bf10e0c5b0`. Its receiver-authored custody manifest likewise reproduces as Git blob `d7a43ed0fba02940823e339c8e1eda3b1753623d`, 4,786 raw bytes, SHA-256 `8774a0fb0eee86c572cbdd5ca5440e38668bb76e8b021cc267e17749ff46a628`.

## Delta findings

1. **Production bytes are unchanged.** The diff from `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41` to `6d4089ef95a14fb6b1d46c96ebf452733ff5cd98` is empty for `src/m4_post_tokenizer_integration.py` and `src/test_m4_post_tokenizer_integration.py`. Their Git blobs remain `4ad3edb932c78ceeed056302c7e2ec2c6cac3b12` and `087c2f9340206a3676978eeb157f0f99d797a551`; raw SHA-256 remains `8964de5daf745226771818ab59f2cc75ef29ccbc5d09b43b6dae102b876b2f1b` and `9878ec7b6c2e8f5c81bd2944e5c811cc1fcdc38a712e4607ce351c6177b18962`.

2. **The invalid-target false-kill defect is closed.** All fifteen governed entries now target real methods under `src.test_m4_post_tokenizer_integration.RereviewRemediationTests`. For every unchanged and mutated probe, the apparatus requires the exact fully qualified discovered ID, exactly one executed test, and no loader error, runtime error, skip, unexpected success, stdout, or stderr. A missing method becomes `INSTRUMENT_FAILURE`, never `KILLED`.

3. **A kill is bound to mutation-sensitive evidence.** Every unchanged baseline must pass before its temporary predefined change. A mutant counts as `KILLED` only when the same exact test fails by assertion and its traceback matches the contract-bound expected-failure expression. A passing or no-op mutant is `SURVIVED`; unrelated assertions and discovery, import, syntax, environment, timeout, subprocess, malformed-output, and I/O failures fail closed as instrument failures.

4. **Mutation custody and restoration are fail-closed.** Mutations occur only in a disposable copy of committed public package trees. Baseline bytes and SHA-256 are staged before each case and restored in a `finally` boundary. Body failure, corrupt restoration, and restoration-write failure probes cannot produce successful sensitivity evidence.

5. **Focused executable evidence reproduces.** The apparatus adversarial suite passed 15/15. The governed mutation replay passed 15/15 with canonical Git-blob transcript SHA-256 `f889582b8cabc1786729987b73f127dfa4b4db745a6bbca9439fcc74e3a99bce`. Each transcript row records one passing baseline execution, one exact mutant execution, the bound assertion failure, zero errors, `KILLED`, and restored baseline identity. No `_FailedTest`, missing-method `AttributeError`, or instrument-failure marker appears in the canonical transcript.

6. **Affected identity closures reproduce.** The TASK BUILDER common manifest validates all 72 declared raw Git-blob artifacts. The combined inventory reproduces 69/69 rows by mode, Git blob, byte length, and raw SHA-256; all 27 governed sidecars reproduce their target digest, basename, and LF grammar. The launch contract binds the updated inventory digest. The independent CRITIC COMBINED CLEAR and its banked Windows and pinned-container results are coherent with these identities.

7. **Routing scans are manually classified.** The v4 authority range has four duplicate-domain fixed-regex findings, and the manifest-only range has fourteen. Gitleaks reports zero in both ranges. Every fixed-regex match lies wholly inside a required immutable public Git/SHA identity; none is contact data or a credential, and none was suppressed.

The exact v4 worktree is clean, and `git fsck --full` reports no integrity error.

## Judgment and limits

The earlier `INSTRUMENT FAILURE — mutation apparatus/test-target binding` reason is closed. The byte-unchanged M4 post-tokenizer implementation now has adequate engineering-readiness evidence to return to Rebecca for a later explicit integration decision.

All standing holds remain. JUDGE performed no tokenizer or materializer operation, inference, private custody access, model/tokenizer/prompt/seed access, scoring, science, merge, publication, STATE/provenance mutation, or final gate decision. Banked unchanged suites were not rerun. Rebecca alone may make any later operative integration, merge, qualification, scoring, scientific, or result-publication decision.

This ruling must remain private and non-operative until RECORDER publishes these exact bytes under the active custody contract and attests the byte length and SHA-256. JUDGE has not committed or pushed this ruling.
