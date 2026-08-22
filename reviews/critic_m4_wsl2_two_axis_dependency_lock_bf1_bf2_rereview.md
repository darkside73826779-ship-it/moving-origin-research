# CRITIC rereview — M4 WSL2 two-axis/dependency-lock BF1–BF2 remediation

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

Gate served: narrow BF1–BF2 repository-quality rereview

## Exact intake and repository identity

- Substantive ref: `refs/heads/architect/m4-wsl2-two-axis-dependency-lock-bf1-bf2-remediation`.
- Routing head: `6d8175edb63cf6ec03c0904d640ae6f946ebcf16`.
- Substantive remediation result: `4993711fa32ffe9ab3b2dabb2b5d5615182c6e90`.
- Base and authoritative prior BLOCK: `31dd464ad1bcdfcef713b4636b4df653782dc1c8`.
- Manifest ref/head: `refs/heads/architect/m4-wsl2-two-axis-dependency-lock-bf1-bf2-remediation-manifest` at `95cd17deabba6a0c84c02e26c408023b989e79bc`.
- Manifest: `handoffs/ARCHITECT_TO_COORDINATOR_M4_WSL2_TWO_AXIS_DEPENDENCY_LOCK_BF1_BF2_REMEDIATION.manifest.json`.
- Review branch: `critic/m4-wsl2-two-axis-dependency-lock-bf1-bf2-rereview`.

Authenticated remote equality for both supplied refs was exact at intake. The standard helper created the isolated review worktree at the exact routing head. The canonical manifest validates `VERIFIED` against the common handoff schema. Its ten raw artifact SHA-256 identities reproduce. The routing-only range changes only the named handoff. `git diff --check` and `git fsck --full --strict` returned clean.

## Verdict

- **BF1: CLEAR**
- **BF2: CLEAR**
- **LAW_FIDELITY: CLEAR**
- **COMBINED VERDICT: CLEAR**

This is a narrow repository-quality clearance of BF1–BF2 only. It is not a model result, score, scientific interpretation, qualification, readiness declaration, merge decision, or project gate decision.

## BF1 — exact v1 vocabulary and fail-closed projection

CLEAR.

- The derivation validates the complete source object against the exact bound v1 Draft 2020-12 schema before projection.
- Its nineteen-code `V1_FAILURE_CODES` set equals the v1 schema enum exactly. `OUTPUT_DIGEST_MISMATCH` is the sole replica-only code; all eighteen other valid codes project to structural `BLOCKED`. Unknown or schema-invalid codes are rejected.
- Metric-derived structural failures now use only exact v1 names: `ACTIVE_DURATION_SHORT`, `DROPPED_WINDOWS`, `FIFO_ORDER_MISMATCH`, `EXECUTIONS_DID_NOT_OVERLAP`, `NO_BACKPRESSURE_OBSERVED`, and `CLEANUP_VRAM_NONZERO`.
- Independent all-code reproduction confirms every valid non-replica code remains visible in `structural_failure_codes`; a schema-valid `CHILD_PROCESS_FAILURE` with otherwise passing measurements remains structural `BLOCKED` while replica consistency may independently be `MATCH`.

The prior invalid local vocabulary and masking negative test are removed. BF1 is fully remediated.

## BF2 — v2 semantics and mandatory exact-replica guard

CLEAR.

- The v2 schema now binds exact source and structural vocabularies, unique lists, structural status/failure equivalence, source PASS/BLOCKED failure cardinality, and MATCH/MISMATCH/NOT_RUN count/list conditionals.
- The committed semantic validator additionally enforces agreement-plus-mismatch arithmetic, list length, canonical sorted uniqueness, ordinal range, canonical ordinal digest, exact replica status, canonical structural failures, structural status, and—when source bytes are supplied—complete equality to a fresh projection of those exact bytes.
- Contradictory status, count, list, digest, vocabulary, structural, and source-binding mutations are rejected.
- `require_replica_match` first performs semantic validation and raises the single `REPLICA_CONSISTENCY_STOP` for both `MISMATCH` and `NOT_RUN` whenever exact replicas are required. It proceeds only on a valid `MATCH`; a diagnostic consumer not requiring exact replicas may proceed without changing the reported status.

The prior policy-string-only boundary is now an executable fail-closed guard. BF2 is fully remediated.

## Preservation and regression evidence

- **Retained v1 report:** byte-identical at 123,507 bytes and raw SHA-256 `7dde0d1587b9205a339776ad04daecfe2bf160e8ecb9ff0504335f91b57a10bc`; disposition remains `BLOCKED / OUTPUT_DIGEST_MISMATCH`.
- **Retained v2 projection:** byte-identical at 1,019 bytes and raw SHA-256 `d071f44c5a18a40b75aee17700028417c9275c8146f6b1eee0e65159404ca185`; structural `PASS`, replica `MISMATCH`, 164 compared, 80 agreements, and 84 mismatches remain unchanged.
- **Dependency lock and banked evidence:** `.gitattributes`, the v1 report/schema/producer, retained projection, dependency exclusion and sidecar, requirements, setup, readiness verifier, and text-only runtime verifier are byte-identical to the prior reviewed package.
- **Inventory and sidecars:** all eighteen ordered inventory entries reproduce path, mode, Git blob, byte count, and raw SHA-256. All five artifact/sidecar bindings, including the updated complete package inventory sidecar, reproduce exact basename, digest, and LF.
- **Validators and regressions:** independent public WSL2 execution passed all 34 focused and banked `test_m4_wsl2_*` tests. The focused remediation subset passed 15/15. The v2 schema passes `Draft202012Validator.check_schema`; Python compilation and shell syntax checks pass. No model or project workload was invoked.
- **Public safety:** complete remediation-range preflight returned 31 fixed-regex findings representing ten unique substrings wholly inside required public Git/SHA identities and pre-existing public metadata. Manual review found no credential, personal contact, private path/value, custody material, protected prompt/seed, score, or scientific output. Gitleaks returned zero findings.

## Findings

No blocking or non-blocking finding remains within BF1–BF2 scope.

## Exact disposition and next authorized role

Return this narrow COMBINED CLEAR to **WORKFLOW COORDINATOR**. The prior BF1–BF2 BLOCK is superseded only for this exact corrected package. All diagnostic/scientific boundaries remain in force. The Coordinator determines any next role; this review does not authorize a model rerun, implementation merge, readiness release, scoring, qualification, science, or gate decision.

## Public-safety and execution attestation

The rereview used only committed public repository bytes, static validators, canonical hashing, and custody-free synthetic/unit regressions. No model/tokenizer execution or acquisition, private custody, protected input, scoring, scientific interpretation, qualification, readiness action, merge, or project decision occurred. Review-range preflight returned two fixed-regex findings representing the same required public projection SHA-256 in commit-parent and combined-range domains; manual classification found no prohibited material, and Gitleaks returned zero findings.

Remote equality and worktree cleanliness will be reverified after publication.
