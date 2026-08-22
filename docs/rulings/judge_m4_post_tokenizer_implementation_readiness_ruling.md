# JUDGE Ruling — M4 Post-Tokenizer Implementation Readiness

Date: 2026-08-22 EDT
Regime: B
Role: Persistent JUDGE
Publication status: PENDING_RECORDER_CUSTODY

## Authorized question

Whether the exact custody-free M4 post-tokenizer integration implementation package is ready to return to Rebecca for a later explicit gate/merge decision.

## Exact intake

- Coordinator route: `refs/heads/coordinator/m4-post-tokenizer-implementation-judge-route` at `2bb9e04adc73ea324c8be58f66db16c62f2aa1ba`.
- Coordinator manifest: `handoffs/WORKFLOW_COORDINATOR_TO_JUDGE_M4_POST_TOKENIZER_IMPLEMENTATION_READINESS.manifest.json` at `cbf7ad4dc1292fd907e92d50cfbbc3e053a8b481`.
- Rebecca authority artifact raw SHA-256: `0cb7d51fa8cbe2e088d2be4b0c21275845b89c36fd35a7bbec2b5369d504dfc9`.
- TASK BUILDER package: `taskbuilder/m4-post-tokenizer-rrr2-f1-strict-cleanup-attestation` at `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`.
- Implementation result: `a7e74c110ae32be0ea8918c9b0c037424fbf9b32`.
- TASK BUILDER routing result: `d175f7eb003348777d6e6e3e2811350089ad329b`.
- Recovery-CRITIC COMBINED CLEAR: `bc1bd5a1c86f0e2cd9f316e6e0fb339278fb60f2`.
- Original implementation release: `071392aadfcdf6c76b47f3f959578661658f7791`.

The Coordinator-to-JUDGE manifest, remote identities, ancestry, named raw Git blobs, and authority-artifact digest were independently verified.

## Independently reproduced valid evidence

- Custody-free integration suite: 49/49 PASS.
- Combined raw inventory: 68/68 exact mode, byte count, Git-blob SHA-1, and raw SHA-256 identities reproduced.
- Inventory sidecars: 27/27 exact target digest and canonical sidecar grammar reproduced.
- Lifecycle matrix: 42 cells, exercised by the passing production-path suite.
- Synthetic fanout fixture negatives: 13 rows, exercised by the passing production-path suite.
- RRR2-F1 source change is narrow and fail-closed: after disposal, exactly one liveness observation is accepted only when it is literal Boolean `False`; `None`, integer `0`, empty tuple, `True`, and exceptions project `BACKEND_ROLLBACK_FAILURE` in the passing integration suite.
- Worktree cleanliness, `git diff --check`, and `git fsck --full --strict`: PASS.

The banked 37-test tokenizer result and real-tokenizer PASS evidence were treated only as immutable prior evidence. JUDGE did not invoke tokenizer/materializer code or access tokenizer/model/custody inputs.

## Blocking evidence defect

The claimed deterministic mutation result `15/15 KILLED` is not valid mutation evidence.

All 15 mutation-contract commands name test methods under `src.test_m4_post_tokenizer_integration.RemediationProductionTests`. None of the 15 named methods exists on that class in the exact implementation package. The relevant methods are defined under `RereviewRemediationTests`.

Independent resolution of every fully qualified mutation target therefore returned MISSING: 15/15. The committed mutation transcript independently confirms the same defect: every record contains unittest `_FailedTest`/`AttributeError` output stating that the named `RemediationProductionTests` method does not exist.

The mutation runner labels a mutant `KILLED` solely when the subprocess exit code equals the contract's expected exit code `1`. It does not require successful test discovery or distinguish an assertion failure caused by the mutant from an unresolved test target. Consequently, all 15 records are false-positive kills caused by test-discovery errors. The newly added `RRR2_F1_TRUTHINESS_WEAKENING` record is affected identically.

This defect invalidates the complete 15/15 mutation claim, its canonical transcript as evidence of mutation sensitivity, and the CRITIC closure that relied on it. It does not negate the independently passing 49-test integration suite or prove an implementation defect. It is an executable-evidence apparatus failure.

## Final disposition

**IMPLEMENTATION READINESS: BLOCK.**

**Evidence classification: INSTRUMENT FAILURE — mutation apparatus/test-target binding.**

The package is not eligible to advance to the separately governed integration/merge workflow on the supplied evidence. No implementation failure, candidate failure, scientific failure, or scoring verdict is inferred.

Required next event: WORKFLOW COORDINATOR routes one batched remediation of the mutation contract/runner/transcript and all identity cascades through the authorized implementation and independent-review sequence. Any later JUDGE consideration requires a new complete Rebecca-authorized cycle and exact canonical handoff. No rerun of scoring, tokenizer materialization, inference, or science is authorized by this ruling.

## Holds and custody

No scoring, protected-seed access, tokenizer/materializer operation, private custody access, inference, science, model/tokenizer publication, merge, STATE/provenance mutation, JUDGE commit, or JUDGE push occurred.

Exact next recipient: WORKFLOW COORDINATOR, for unchanged private-envelope routing to RECORDER. This ruling becomes durable only after RECORDER publishes byte-identical content and attests its hash. It becomes operative only after Rebecca rules.
