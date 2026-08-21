# CRITIC Review — L8 Native-CUDA Backend Adoption Specification v1

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Independent law-fidelity and substantive-executability review of a prospective, inoperative native-CUDA diagnostic-backend adoption design.

## Formal receipt and scope

FORMAL HANDOFF received from ARCHITECT through `handoffs/ARCHITECT_TO_CRITIC_L8_NATIVE_CUDA_ADOPTION_V1_2026-08-21.md`. I reviewed `architect/l8-native-cuda-adoption@5cee6cd19bc5a3d532700a7eb34a0e02e56bd57a`, whose design commit is `9833f83c1f2900274f10d698efdee0f9f1c6ad3e`, against the named TASK BUILDER authority head `8251d95b31107f4a710463fb0574b5bd33a44325`, the committed schemas/fixtures/sidecars, the constitution, the M0 decision sheet, the provenance log, the approved v1.5 dependency manifest, and the cited committed evidence identities.

The artifact under review was not edited. This review did not implement or execute diagnostics, recompute or score scientific results, access protected/hold-out/courier seeds, merge, or authorize adoption.

## First checklist item — versioned-law compliance

1. **Law diff (P1/P2): PASS.** The P1–P6, L8, L18, and L19 quotations in the proposal are verbatim matches to `docs/ARCHITECTURAL_CONSTITUTION_v2.md` at the cited lines. No constitutional text was reconstructed.
2. **Threshold-source audit (P3): PARTIAL FAIL.** The locked L8 bars are supported by `docs/rulings/M0_DECISION_SHEET.md` line 21 and provenance Entry 70's recovery/confirmation of Entry 11. New consistency, boundary, runtime, workload, and performance criteria are visibly prospective. However, §6.1 tags “CPU is not rerun” as `[O-14]`; the actual Entry 22 O-14 ruling is the M1 I3 empirical-null replacement, not a universal no-rerun rule. Later provenance uses “O-14” colloquially for non-rerun, but that does not cure the mismatch with Entry 22's actual text. The citation must be corrected to its real authority (for example the applicable Persistence Doctrine/no-replacement rule) rather than perpetuated.
3. **Provenance audit (P6): FAIL as above.** Evidence SHAs and non-retroactivity are disclosed consistently, and the historic 239/240 result remains `UNRESOLVED_BOUNDARY_CELL`. The O-14 source claim does not match the actual entry text.

## Verdict

**BLOCK.** The prospective scientific direction is reasonable—one-sided regression permits genuine CUDA improvements while independently bounding degradation; the one-cell exception is narrow; non-retroactivity is explicit; and M4 remains fenced. But the committed contract is not substantively executable end-to-end and its result/failure schema cannot faithfully publish several required outcomes. CLEAR would force the TASK BUILDER to invent normative fixtures, dependency identities, comparison payloads, failure encodings, and recovery behavior.

## Blocking findings

### BF1 — Missing mandatory CUDA RNG/output fixture and unresolved private API identity

**Classification:** executability / RNG-runtime identity.

Section 4.1 makes both `_standard_gamma` code-object/module identity and a frozen output fixture mandatory. The committed `l8_native_cuda_rng_fixture_v1.json` contains only four ASCII identity hashes and derived seeds; it contains no CUDA generator outputs, tensor shapes/values/digests, `_standard_gamma` callable/module/code identity, PyTorch build identity, or expected scientific-payload digest. The executability matrix's NC-003 refers generically to a `draw_schedule` fixture that does not exist. Consequently an implementation cannot prove the pinned private operation or exact draw schedule against a committed known answer without inventing the fixture and its expected result.

### BF2 — Runtime/dependency and qualifying-device identity are deferred to implementation

**Classification:** executability / provenance / device identity.

Section 4.1 says exact wheel URLs, SHA-256 values, and PEP 610 verification “must be copied ... during implementation.” Those normative values are absent from the new config schema and artifact set. Section 7 simultaneously says any dependency/device difference fails before RNG construction, but the config schema accepts arbitrary nonempty PCI ID/name/driver, arbitrary positive memory, and arbitrary compute capability; no committed qualifying device manifest or expected `dependency_sha256`/`device_sha256` exists. “Exact compute capability plus successful frozen fixtures” is circular because the required frozen output fixture is missing. A task builder must choose the accepted device and construct both digests.

### BF3 — Result schema is incapable of expressing the specified comparison and failure semantics

**Classification:** schema / publication / failure semantics.

The result schema requires exactly two complete 240-row runs even when `status="failed"`; requires `comparison.repeat_payloads_identical=true`, so it cannot encode the required NC-014 repeat mismatch; and always requires comparison/verdict fields after preflight/CUDA/publication failures that occur before runs exist. `comparison.per_metric` is an unconstrained object, while no schema fixes the five per-cell signed regressions, five 240-cell means, thresholds, pass/fail decisions, ordering, or values. Rows omit identities, sigma/calibration, underlying non-false-kill predicate truth values, apparatus counts, and boundary classification/details that §§6.2 and 8 require to be proven and published. `region` and aggregate-region strings are unconstrained rather than bound to the frozen CPU classifications. Performance above threshold has neither a top-level verdict nor a result-schema failure code, despite NC-020 requiring an “acceptance failure.” These defects permit invalid positives and make required negative/failure artifacts schema-invalid.

### BF4 — Executability matrix names abstract fixtures and expected prose, not concrete realized tests

**Classification:** end-to-end executability / fixtures.

NC-004, NC-005, NC-007, NC-009 through NC-018, and NC-020 reference abstract fixtures such as `scheduler`, `manifest`, `boundary`, `regression`, `repeat`, and `publisher`, but no committed input artifacts fix their exact bytes, schema, mutations, expected canonical outputs, or expected digests. In particular there is no realized one-cell inclusive-boundary case, ULP-outside case, two-cell case, per-metric one-sided regression case, publication-interruption state set, or valid prior artifact pair. The binding CRITIC executability rule requires concrete fixtures and artifact pairs; prose test names are insufficient.

### BF5 — Oracle/evaluator and publication/recovery bindings remain underdetermined

**Classification:** evaluator fidelity / publication executability.

The config schema fixes the CPU oracle digest but permits an arbitrary `diagnostics/*.json` path, and the spec imports evaluator semantics wholesale from a short commit reference without fixing the exact oracle path, the exact row/region enums, the exact configuration instance, or its canonical digest. The proposal says scientific fields are never rounded before canonicalization but does not define how binary64 values are converted for RFC 8785 JSON, nor the canonical scientific-payload subobject whose two run digests must match. Publication requires preservation, restoration, and `.incomplete` retention but does not fix temporary names, recovery-state precedence, startup behavior, or the schema/content/digest of `.incomplete`; it also requires both full payload byte arrays in parent memory without bounding the resulting memory requirement. These choices materially affect reproducibility, failure recovery, and performance and cannot be left to implementation.

### BF6 — Provenance source mismatch for the no-rerun rule

**Classification:** versioned-law/provenance defect.

As recorded in the mandatory first checklist, §6.1's `[O-14]` citation does not match provenance Entry 22's actual O-14 ruling. Correct non-retry/non-retroactivity protections should remain, but must be sourced to the actual governing text. A later shorthand usage cannot substitute for P6 verification against the entry itself.

## Non-blocking findings

- The one-sided signs are directionally coherent: false-kill, any-seed false-kill, false-pass, and null beta-star increases are regressions, while true-effect mean beta-star decreases are regressions. Improvements cannot offset a per-metric exceedance. Exact operating-point and all-16 aggregate-region equality preserve the CPU conclusion.
- The one-cell `BOUNDARY_CONSISTENT` rule is narrow, conjunctive, capped at one cell per run, and does not retroactively relabel ordinal 47. This logic is acceptable in form pending Rebecca's approval and concrete executable fixtures.
- The performance interval is clearly prospective and subordinate to scientific consistency. The task should nevertheless specify a performance-failure verdict/code and address memory pressure from retaining two complete payload byte arrays.
- The M4 boundary is appropriately fail-closed in prose: native CUDA remains unavailable pending CRITIC review, Rebecca approval, implementation review, Phase B reconciliation, and a separate M4 release. The backend request/response schemas should eventually be reconciled against the actual M4 contract rather than treated as operative now.

## Preserved evidence and boundaries

- The CPU oracle, approved tape-backed CUDA v1.5 backend, 1,000- and 10,000-repetition native feasibility evidence, and historic ordinal-47 finding remain unchanged.
- The existing native evidence remains feasibility-only and nonqualifying; this review does not apply later-written criteria retroactively.
- No bar, control, negative label, G2–G4 freeze, M4 dependency, or scoring status was changed.

## Public-safety scan attestation

Public-safety scan: gitleaks `detect --no-git --source reviews --redact` plus regex checks for credentials/tokens/private keys, environment secrets, email, IP-like machine identifiers, and private absolute paths; scope was the sole new review artifact and the full critic diff relative to `5cee6cd19bc5a3d532700a7eb34a0e02e56bd57a`; 0 findings; cleared. `git diff --check` also passed.

## Ball-pass and exact next recipient

Formal ball-pass: **WORKFLOW COORDINATOR only**, for Rebecca R. McClintic's decision and any authorized return to ARCHITECT. The CRITIC does not route directly to ARCHITECT, TASK BUILDER, RECORDER, INTEGRATOR, JUDGE, or M4.

No implementation, execution, diagnostic rerun, scoring, protected/hold-out/courier seed access, G2–G4 freeze, formal consistency/adoption claim, M4 use, merge, bar/control change, negative renaming, or L15/L16/L17 work before M5 is authorized by this BLOCK.
