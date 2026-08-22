# CRITIC rereview — M4 crash-cart beta BF1–BF4 correction

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

## Immutable intake

- Corrected package ref/head: `taskbuilder/m4-final-prescoring-crash-cart-beta-implementation` at `67f9b8198c5081e1ada054d7820868d610dd6247`.
- Corrected substantive implementation: `ff1635412cab8a2754ecaeab14daf3c0d7892b65`.
- Routing/inventory result: `67f9b8198c5081e1ada054d7820868d610dd6247`.
- Canonical manifest: `handoffs/manifests/m4_final_prescoring_crash_cart_beta_implementation/20260822T160000Z_task_builder_to_workflow_coordinator.json`.
- Prior authoritative BLOCK: `critic/m4-final-prescoring-crash-cart-beta-implementation-review` at `e205adc445a46500b9e221df815fb554de0abc29`.

Remote equality, ancestry from the prior package head `05e83a92dec4bec747c65ab279b841ed8d445f61`, and helper-compatible checkout reproduce. The common handoff validator returns `VERIFIED`. All 22 manifest artifact hashes, all listed sidecars, raw LF, and the corrected `.gitattributes` inventory entry reproduce.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

BF4 is closed. BF1–BF3 remain open for the corrected bytes. This is a custody-free implementation-quality result only; it is not execution, scoring, science, qualification, readiness, publication, merge, or gate authority.

## Delta findings

### BF1-R1 — the injected lifecycle does not realize the governed lifecycle, rollback, or cleanup contract

`CrashCartLifecycle.warmup()` appends a textual `barrier-N` event and then calls candidate followed by peer synchronously. It provides no symmetric barrier, timeout, receipt/state/ordinal validation, warmup-episode reset before ordinal 0, zero-active/in-flight wait, GPU synchronization, session/KV/RNG-clear assertion, or independent RNG initialization beyond appending the strings `clean-barrier` and `rng-after-clean-barrier`. `active()` ignores `active_schedule()`, queue capacity eight, the 60-second deadline, 250-ms telemetry, receipt correlation, retry/drop rules, rollback, and paired atomicity; it again invokes candidate then peer sequentially.

Cleanup is caller-optional rather than mandatory on every terminal path. A directly injected candidate failure at warmup ordinal 0 produced only `candidate(0)` with event `barrier-0`: peer, both resets, rollback, clean barrier, and cleanup were never called. There is no `try/finally`, terminal orchestration, deterministic sanitation, renderer, export, or cleanup validation. The correction therefore remains a synthetic call loop rather than the exact non-executing beta lifecycle required by BF1.

### BF2-R1 — five-stage semantic validation remains fail-open and is not composed with the schema

`validate_terminal()` still never loads or applies the committed JSON Schema. It validates only counts and a few status strings, not the required row, receipt, telemetry, trend, replica, cleanup, public-safety, export, law, or cross-field structures. Directly necessary probes were accepted for:

- a `COMPLETE_ACTIVE_TERMINAL` containing four empty warmup rows, 64 empty active rows, 121 empty samples, empty trends, a bare replica status, and status-only cleanup/public-safety/export objects;
- a `PARTIAL_ACTIVE_TERMINAL` with no four-row clean warmup proof, one empty row/sample, and replica `MATCH`; and
- a `POST_ACTIVE_TERMINAL` with partial trends and no cleanup object.

These records violate the banked schema and staged evidence contract. Partial-role nullability, actual compared-pair replica counts, exact row ordinals, complete trends, complete cleanup postconditions, reproduction equality, HELD laws, and no-fabricated-field rules remain unenforced.

### BF3-R1 — complete controls, fixed identities, and correction regressions remain absent

The warmup plan adds several generation fields, but it still omits the bound RNG domain, full-sequence and clean-barrier deadlines, synchronized equal-role execution, exact seven-field receipt/state chains, warmup and measured episode-reset proofs, measured receipt ordinals 0–63, and no-priming enforcement. The lifecycle does not consume the governed active schedule. `fixture_inventory()` deterministically returns 64 distinct prompt digests, but no immutable expected 64-digest inventory or regression detects generator drift.

The test files are byte-identical to the prior blocked package. The eight tests do not call `CrashCartLifecycle` or `fixture_inventory()` and do not exercise any new BF1–BF3 behavior, staged adversary, rollback, cleanup, barrier, reset, RNG, receipt, or 64-identity invariant. Consequently, the manifest claim `staged semantic adversaries and lifecycle regression PASS` has no committed focused-test support. The quality trace also still labels the implementation as the superseded `738878ab3618d6058f0725caa7e3f0f0388cb59f` rather than corrected result `ff1635412cab8a2754ecaeab14daf3c0d7892b65`.

## BF4 closure and banked clear boundaries

- `.gitattributes` is now present in the 22-entry manifest artifact map with the correct raw SHA-256. No changed non-self artifact is omitted.
- The changed source sidecar reproduces, and every unchanged listed identity remains byte-identical and banked.
- The unchanged focused target returns 8/8, and the wrapper still exits 2 with `RUN_AUTHORITY_ABSENT` before any runtime access. Because the implementation source changed while the tests did not, 8/8 does not close BF1–BF3.
- The HELD-law projection, no-start boundary, production integration seam, model/runtime identities, and all standing holds remain unchanged.
- Correction-range public preflight reports 18 fixed-regex matches and zero gitleaks findings. Manual review maps every match to public commit/SHA-256 identity substrings in the manifest or sidecar; no credential, private value/path, protected input, model/tokenizer bytes, token array, score, or scientific result is present.
- `git diff --check` is clean. No model/tokenizer/OCI/WSL2/gofast workload, held access, custody, scoring, science, state/provenance mutation, merge, publication, retry, readiness declaration, or gate action occurred.

## Required remediation and disposition

Return one narrow BF1–BF3 correction that:

1. implements deterministic injected orchestration with real paired barriers, explicit warmup/measured resets, post-clean-barrier RNG insertion, governed schedule/queue/deadlines/telemetry, receipt/ordinal checks, fail-closed rollback, and mandatory `finally` cleanup on every injected failure;
2. composes the committed JSON Schema with complete semantic checks for all five terminal stages and their cross-field invariants; and
3. commits focused positive/adversarial regressions for every corrected path, binds the fixed 64 prompt identities, and updates the quality trace to the exact corrected implementation identity.

Return **COMBINED BLOCK** to **WORKFLOW COORDINATOR**. BF4 may remain banked CLEAR. The exact next recipient after Coordinator intake is **TASK BUILDER** for one batched BF1–BF3 correction. All holds remain binding.
