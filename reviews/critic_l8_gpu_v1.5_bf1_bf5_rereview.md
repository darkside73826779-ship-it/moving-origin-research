# CRITIC Rereview — L8 GPU v1.5 BF1–BF5 Remediation

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Independent law-fidelity and deterministic-executability rereview before Commit A and before either Rebecca-authorized L8 GPU sentinel execution.

## Inputs and SHAs reviewed

- Authoritative routing head: `architect/l8-gpu-adoption-spec` at `e05550f494b2c6dffb2ea9645067395beaf56fe1`.
- Remediation result: `a25398e599622c09d130b597b7bc83ce62a966d5`.
- Handoff: `handoffs/ARCHITECT_TO_CRITIC_L8_GPU_V1.5_BF1_BF5_REMEDIATION.md`.
- Primary amendment: `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.5.md`.
- Prior authoritative BLOCK: `635e56f63ce61be537cfdfa026f24adf17e91b3a`, `reviews/critic_l8_gpu_v1.5_executability_review.md`.
- Operative v1.4 base: `4c84248897fe7c0b10f669bba352a05e3268edf2`.
- Constitution/protocol and provenance: `docs/ARCHITECTURAL_CONSTITUTION_v2.md`, `docs/rulings/provenance_log.md`, and `docs/rulings/M0_DECISION_SHEET.md`.

## Verdict

- **LAW_FIDELITY: PASS**
- **SUBSTANTIVE: CLEAR**
- **Combined disposition: PASS + CLEAR**

The amendment may route to Rebecca for her sole decision whether to approve/re-release v1.5. This verdict does not itself activate the specification, release TASK BUILDER, authorize B11, or authorize either execution.

## First checklist item — §5 law/provenance audit

### P1/P2 — repo-first and verbatim law diff: PASS

The L8, L18, and L19 quotations in v1.5 §1 were re-diffed character-for-character against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` lines 28, 54, and 55. Each quotation is verbatim and each source exists in-repo.

### P3 — source-class tags: PASS

Beta-star `0.2`, rho `0.8`, at least three doses, and five seeds remain attributed to `[BAR-Entry 11]`, matching the adopted M0 decision sheet. Exact four-dose use is now expressly `[PROPOSED]` and supersedes v1.4's incorrect exact-four-dose attribution without changing the locked at-least-three-dose bar. New fixture constants, dependency requirements, matrix criteria, comparator behavior, and execution rules remain `[PROPOSED]` pending Rebecca.

### P4 — date and regime: PASS

The amended specification and every new normative JSON artifact state `2026-08-21` and Regime B. The config template correctly retains v1.4's literal `2026-08-20` because it is the inherited runtime-schema value, not the amendment artifact's creation date.

### P5 — deviation memorialization: PASS

B11 remains expressly inoperative and Rebecca-gated. The proposal does not claim an existing constitutional waiver or execution release.

### P6 — provenance citations: PASS

The exact two-child/no-third-child rule is now `[PROPOSED]`, not attributed to Entry 22, and v1.5 expressly supersedes conflicting v1.4 Entry 22 attributions. Entry 22 is referenced only for O-14's independently binding no-rerun rule and O-15 execution-channel semantics, which its text supports. The exact-four-dose provenance correction matches Entry 11 and the adopted M0 sheet.

## BF1–BF5 disposition

| Finding | Result | Independent verification |
|---|---|---|
| BF1 — template date | CLOSED | Template `date` is restored to literal `2026-08-20`, so v1.5 §3.1's sole placeholder exception is again true. Raw sidecar matches. |
| BF2 — B11 fixture | CLOSED | The committed two-row fixture fixes `EPS_C`, `R_STAR`, dose/window realization, selection inputs, exact ordered selections, correctness, risk, deviation, full `d_seed`, dose summaries, beta-star, rho, and predicates. Independent recomputation reproduced both selection rows, beta-star values `1.0205040771249136` and `0.18516401995451037`, and rho values `1.0` and `0.8`. |
| BF3 — matrix/trace | CLOSED | Matrix v2 has exactly seventeen ordered seven-key rows with fixed pytest node IDs, exact artifact bindings, assertion literals, and dispositions. The expected trace has exactly seventeen ordered rows; all five shared fields match row-for-row. Its independently recomputed raw SHA-256 is `531148c6f1927c9b3f9f7946ec931ac9f16e6a82716619b881fcf4854c6f28ff`, matching the spec and sidecar. |
| BF4 — dependency provenance | CLOSED | Each direct dependency now has one exact CPython-3.11 Windows wheel URL and SHA-256. All four URLs returned HTTP 200. The specified PEP 610 `direct_url.json` read, exact URL-without-fragment comparison, archive-hash comparison, field rejection, version comparison, and index-install fail-closed rule are executable without inferring source from `pip freeze`. |
| BF5 — source attribution | CLOSED | Exact four doses and the two-child cap are correctly classified `[PROPOSED]`; the supported Entry 11 minimum and Entry 22/O-14/O-15 rules remain distinct. |

## Regression against preserved closures

- B1 count polarity and valid-denominator semantics remain unchanged and executable.
- B4 deterministic row schemas/polarities, B5 status vocabulary, B6 rehearsal filesystem, B8 full-screen pipeline, and B9 counter/failure envelope are unchanged by the remediation delta.
- B7 custody mechanics remain executable; only the unsupported provenance tag changed.
- B10's exact versions remain unchanged; the delta adds deterministic wheel and installed-source custody.
- All seventeen executability controls retain a normative clause, exact schema/type reference, exact fixture/manifest binding, failure disposition, and fixed implementation-test identifier.
- No scientific bar, negative name, geometry, seed derivation, result ordering, or authorization boundary changed.

## Independent integrity and availability checks

- Every `specs/data/l8_gpu_adoption_*.json` file at the routing head parsed successfully.
- Every corresponding raw-byte `.sha256` sidecar matched independently.
- Matrix-v2/expected-trace ordering and shared fields matched exactly for all seventeen controls.
- Both tie fixtures were recomputed from the locked baseline estimator equations. For the lower fixture, one incorrect answer among three yields risk `1/3`, deviation `0.2333333333333333`, beta-star `1.0205040771249136`, and rho `1.0`. For the upper fixture, the ascending-index tie rule selects index zero, yielding risk `1.0`, deviation `0.9`, beta-star `0.18516401995451037`, and rho `0.8`.
- The exact NumPy, SciPy, PyTorch CUDA-13.0, and rfc8785 wheel URLs returned HTTP 200; no package was installed.
- `git diff --check b402fe0..a25398e` passed.

## Blocking findings

None within the authorized BF1–BF5 delta and preserved-closure regression scope.

## Non-blocking findings

None.

## Preserved evidence

- The prior review's sidecar-validity, official-wheel-availability, B1/B4/B5/B6/B8/B9 closure, known-good fixture digest, and frozen-calibration digest evidence remains valid.
- The v1 executability matrix remains historical evidence only; matrix v2 is explicitly the executable authority.
- B11's comparator is clear and executable but remains merely proposed until Rebecca expressly approves it.

## Exact next authorized role

**Rebecca**, through WORKFLOW COORDINATOR, for the sole amendment gate and explicit decision whether to approve/re-release v1.5 implementation and the two permitted executions. If Rebecca approves and re-releases, the exact next role is **TASK BUILDER**. Until then TASK BUILDER remains held.

## Explicitly prohibited actions

- No implementation, sentinel/full-screen/failure-rehearsal execution, scoring, protected/hold-out/courier seed access or exposure, rerun, failed-run replacement, G2–G4 freeze, or merge based on this CRITIC verdict alone.
- No B11 operationalization before Rebecca's express approval.
- No bar/control/negative renaming or reinterpretation, CPU fallback, native GPU calibration, torch-native RNG, or L15/L16/L17 work before M5.
- No CRITIC modification of the specification, implementation, scoring artifacts, or `STATE.md`.

## Public-repository safety attestation

Before push, CRITIC scanned the complete new review commit and diff with gitleaks, credential/private-key/token/password patterns, personal-data and private-absolute-path patterns, `git diff --check`, and manual review. Zero prohibited findings were found. Public repository SHAs, repository-relative paths, public wheel URLs and hashes, approved fixture digests, and synthetic scientific constants were classified as acceptable.

## Execution/custody confirmation

No scoring, diagnostic execution, sentinel/full-screen/failure-rehearsal run, package installation, rerun, protected/hold-out/courier seed access or exposure, or unauthorized merge occurred. Neither permitted sentinel execution was consumed.
