# REBECCA REQUEST — INDEPENDENT M4 ADVISOR AUDIT PACKAGE

Date: 2026-08-22 EDT
Regime: B
Requested by: Rebecca
Prepared by: WORKFLOW COORDINATOR
Audit posture: read-only, independent, evidence-first

## Purpose

Rebecca requests an independent outside audit of the current M4 project state, the work performed, the evidence supporting it, the disclosed process failures, and the remaining path to scientific execution.

The advisor has GitHub read access. Do not rely on role summaries as proof. Independently inspect the named Git objects, manifests, sidecars, ancestry, code, tests, transcripts, and rulings. Clearly separate reproduced fact, static assessment, inference, and unverified attestation.

This audit conveys no project-role authority and authorizes no repository write, merge, model/tokenizer access, protected-seed access, inference, scoring, or science. Return the audit directly to Rebecca unless she separately authorizes repository publication.

## Executive state

- No official candidate behavioral run or scoring run has occurred.
- No protected scoring seeds have been accessed.
- The preserved M4 Qwen3-4B FP8 candidate asset has not been evaluated for scientific performance in this phase.
- A real governed tokenizer materialization completed with sanitized `PASS` evidence.
- The post-tokenizer integration implementation passes its ordinary custody-free integration suite.
- Implementation readiness is currently `BLOCK`, because the committed mutation runner targeted nonexistent methods on the wrong test class and counted test-discovery failures as successful mutation kills.
- Rebecca has authorized correction of that mutation apparatus only, explicitly excluding changes to production behavior or science.
- Project artifacts remain on named remote branches. They have not been merged to `main`.

## Current GitHub anchors

| Subject | Remote ref | Exact head | Primary evidence |
|---|---|---|---|
| Current main | `refs/heads/main` | `cee97538893989e055f49a894f066d2083da4eb5` | merged workflow infrastructure baseline |
| Official WSL2 test bed v1.1 | `refs/heads/coordinator/m4-wsl2-preexecution-testbed` | `0631a019a153ec89312938982c007cf94dd3f03e` | `docs/m4_wsl2_preexecution_testbed_runbook.md`, setup scripts, environment lock |
| Successful tokenizer execution | `refs/heads/taskbuilder/m4-tokenizer-topology-fixture-clear-execution` | `e462e5bd61bcbad4eb03160129dec2e088de9892` | `artifacts/m4_tokenizer_materialization/tokenizer_materialization.json` and sidecar |
| Final tokenizer evidence review | `refs/heads/critic/m4-tokenizer-pass-evidence-ex-pass2-final-rereview` | `7274fbb1aef06d686efe07bb54b6828d0a5b41e2` | `reviews/critic_m4_tokenizer_pass_evidence_ex_pass2_final_rereview.md` |
| Final cleared post-tokenizer design | `refs/heads/critic/m4-post-tokenizer-rr-f1-final-rereview` | `013af72e7dce566e7605d8e1e68fbfbf5d5cda28` | `reviews/critic_m4_post_tokenizer_rr_f1_final_rereview.md` |
| Current integration implementation package | `refs/heads/taskbuilder/m4-post-tokenizer-rrr2-f1-strict-cleanup-attestation` | `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41` | Task Builder handoff, quality trace, manifest, code, tests, mutation artifacts |
| Recovery-CRITIC review preceding JUDGE | `refs/heads/critic/m4-post-tokenizer-rrr2-f1-final-recovery-rereview` | `bc1bd5a1c86f0e2cd9f316e6e0fb339278fb60f2` | `reviews/critic_m4_post_tokenizer_rrr2_f1_final_recovery_rereview.md` |
| Durable JUDGE readiness ruling | `refs/heads/recorder/m4-post-tokenizer-implementation-readiness-ruling` | `32f72c2bb708d96060eb636cb4cf7a673c85ec24` | `docs/rulings/judge_m4_post_tokenizer_implementation_readiness_ruling.md` |
| Mutation-remediation authority | `refs/heads/coordinator/m4-post-tokenizer-mutation-apparatus-remediation-route` | `64ec5992eb4cb81ba75834c3f17db59b6226cce1` | `handoffs/REBECCA_M4_POST_TOKENIZER_MUTATION_APPARATUS_REMEDIATION_AUTHORITY_2026-08-22.md` |
| Mutation-remediation canonical manifest | `refs/heads/coordinator/m4-post-tokenizer-mutation-apparatus-remediation-manifest` | `8e7514afe5ba4cc6ed4f90d180ae1e40b8dd017c` | `handoffs/WORKFLOW_COORDINATOR_TO_TASK_BUILDER_M4_MUTATION_APPARATUS_REMEDIATION.manifest.json` |
| Cleanup-helper infrastructure fix | `refs/heads/coordinator/workflow-efficiency-maintenance` | `332d8336887a2599183d6b292843bf38bec83c88` | `tools/workflow_checkout.py`, `tests/test_workflow_checkout.py` |

Verify every remote head independently with `git ls-remote`. Do not infer that any branch is merged to main. At preparation time, none of the tokenizer execution, integration implementation, JUDGE ruling, mutation authority, or cleanup hotfix heads above was an ancestor of `origin/main`.

## Tokenizer materialization evidence

The accepted execution reports:

- exactly one governed materializer invocation for the successful operation;
- exit `0`, status `PASS`, terminal check `ATOMIC_PUBLICATION`;
- all 18 ordered checks passed;
- sanitized result length 2,779 raw bytes;
- result SHA-256 `19a49a9262be81d30866befda3801b2fc97ef23a8d946d3cc1e4b5de189b3158`;
- exact sidecar and LF worktree-byte binding under `core.autocrlf=true`;
- public array records contain lengths and digests, not token IDs;
- recorded constructed lengths 992, 4,064, and 8,160, plus a one-token stop array;
- the successful operation is `CONSUMED`.

There is also a preserved earlier consumed `FAIL` caused by an implementation defect that incorrectly bounded valid IDs by base `vocab_size`. That failure was not erased or relabeled. A later operation was separately authorized after the code, topology, identities, and evidence contracts changed. Determine independently whether this operation separation and permanent preservation satisfy the repository's no-retry/no-relabeling rules.

## Post-tokenizer implementation evidence

Primary code and apparatus in the current package include:

- `src/m4_post_tokenizer_integration.py`
- `src/test_m4_post_tokenizer_integration.py`
- `tests/run_m4_post_tokenizer_integration_tests.py`
- `tests/run_m4_post_tokenizer_mutation_tests.py`
- `specs/data/m4_post_tokenizer_mutation_contract_v1.json`
- `artifacts/m4_post_tokenizer_mutation_transcript_v1.json`
- `specs/data/m4_post_tokenizer_combined_integration_inventory_v1.json`

Reported ordinary evidence:

- custody-free integration suite: 49/49 pass;
- lifecycle matrix: 42/42 cells;
- synthetic fixture negatives: 13/13;
- combined inventory: 68/68;
- contained sidecars: 27/27;
- strict backend cleanup and rollback behavior;
- frozen identical request identity for candidate and peer fanout;
- no candidate or peer model inference.

Independently determine whether the ordinary suite meaningfully covers the real backend protocol, pair construction, lifecycle invariants, receipt validation, rollback, frozen-input fanout, evidence sanitation, and exact law-status projections. Identify any behavior that synthetic backends cannot validate.

## Current blocking defect

The durable JUDGE ruling classifies the package as:

`BLOCK — INSTRUMENT FAILURE — mutation apparatus/test-target binding`

The ruling found that all 15 mutation-contract commands target methods under:

`src.test_m4_post_tokenizer_integration.RemediationProductionTests`

The named methods do not exist on that class; the relevant methods are under `RereviewRemediationTests`. Each command therefore produced test-discovery `AttributeError`/`_FailedTest` output. The runner treated exit code `1` alone as a successful kill, so all 15 reported kills were false positives.

Audit the ruling directly. Reproduce the fully qualified target lookup and examine the committed transcript. Determine whether any additional mutation-runner failure mode could manufacture a false kill.

## Authorized remediation requirements

Rebecca authorized only the mutation apparatus correction. The production integration implementation must remain byte-identical.

For every predefined mutant, the corrected apparatus must establish:

1. the exact target test exists;
2. that test is discovered and executed;
3. the unmodified baseline passes that test;
4. the exact predefined mutation is applied only in a disposable custody-free checkout;
5. `KILLED` requires the expected mutation-sensitive assertion failure;
6. discovery, import, syntax, environment, timeout, harness, or unrelated failures are instrument failures, never kills;
7. original source bytes are restored and identity-verified after every mutant; and
8. restoration or identity failure stops fail closed.

The remediation is currently owned by persistent TASK BUILDER. No completed remediation result existed when this audit package was prepared.

## Disclosed governance and process defects

Review these as potential control failures rather than assuming their later correction eliminates their significance:

1. An initial Coordinator-to-JUDGE chat handoff lacked a canonical manifest and incorrectly instructed JUDGE to commit/push, contrary to the active private-envelope custody contract. JUDGE stopped; a schema-valid route later corrected it.
2. TASK BUILDER and recovery CRITIC both accepted the false-positive 15/15 mutation transcript. JUDGE independently found the defect.
3. RECORDER disclosed an intermediate inventory-incomplete draft manifest commit during ruling custody. The immediately following commit corrected it without rewriting history; validate the final manifest and assess the retained intermediate public history.
4. The mandatory checkout helper hit Windows path-length failures. A shorter marked workspace root allowed the required helper to succeed without an ad hoc checkout.
5. The cleanup helper initially rejected a clean published worktree because its HEAD advanced beyond the receipt's routing SHA. The infrastructure hotfix now permits cleanup only for a clean exact receipt-bound branch whose descendant HEAD exactly equals its published remote tip. Review the safety of that change independently.
6. Original persistent CRITIC tasks suffered system errors. A same-role recovery review was used under Rebecca's authorization, but its later CLEAR missed the mutation target defect.
7. Numerous public-safety scans produced fixed-regex and generic-key findings on immutable public hashes/digests. Those findings were retained and manually classified rather than silently suppressed. Sample the classifications and determine whether any represent actual prohibited content.

## Scientific boundary

Since the start of this overnight work, the project reports no:

- candidate or peer inference;
- official 30-second behavioral run;
- protected-seed access;
- official L8 simulation;
- Q2 or EF3 execution;
- qualification or scoring;
- threshold adjustment;
- scientific pass/fail claim;
- model or tokenizer publication;
- merge to main.

Audit the commit ranges and artifacts for evidence contradicting those claims. Pay special attention to public results, handoffs, transcripts, environment references, generated arrays, prompts, seed values, and any wording that might improperly convert engineering evidence into a scientific claim.

## Requested audit questions

Return an evidence-cited answer to each question:

1. Are the named remote heads, ancestry relationships, artifact hashes, sidecars, and manifests internally consistent?
2. Is the accepted tokenizer `PASS` evidence reproducible from public sanitized artifacts, and were prior failures preserved honestly?
3. Did any action constitute an unauthorized rerun, relabeling, scoring attempt, protected-data access, threshold change, scientific claim, or merge?
4. Does the 49-test ordinary integration suite support the claims made for it? What remains inherently untested without real backends?
5. Does the JUDGE mutation finding reproduce exactly? Are there additional false-kill or false-survival paths?
6. Are Rebecca's mutation-remediation safeguards sufficient to prevent temporary false code from affecting production or science?
7. Did role separation and independent review function adequately? Which controls failed, and which fail-closed controls worked?
8. Are any public branches carrying credentials, private paths, custody values, protected prompts/seeds, model/tokenizer bytes, complete token arrays, personal data, or misleading scientific claims?
9. Is the cleanup-helper hotfix safe against deletion of dirty, detached, unpublished, rewound, switched, or unrelated worktrees?
10. What exact prerequisites remain before a responsible scientific authorization package can be presented to Rebecca?
11. What are the five highest residual risks, ordered by severity and likelihood?
12. Would you recommend `PROCEED_WITH_REMEDIATION`, `PAUSE_FOR_CORRECTION`, or `STOP_AND_REBASE_GOVERNANCE`? Explain without issuing a project gate decision.

## Requested report format

For every finding, provide:

- identifier;
- severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `INFORMATIONAL`;
- classification: reproduced fact, static concern, inference, or unverified attestation;
- affected ref, commit, path, and line/object where possible;
- expected rule or behavior;
- observed evidence;
- impact;
- smallest safe remediation;
- whether it blocks mutation remediation, implementation readiness, or later science.

Include separate sections for:

- executive conclusion;
- verified facts;
- contradictions or unsupported claims;
- governance assessment;
- scientific-boundary assessment;
- security/publication assessment;
- reproducibility assessment;
- residual risks;
- recommended next sequence.

Do not request or inspect private custody paths, model weights, tokenizer files, prompts, protected seeds, or unpublished scientific data. The audit must remain within public repository evidence.
