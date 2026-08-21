# CRITIC Review — L8 GPU v1.5 Executability Remediation

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Independent law-fidelity and substantive executability review before Commit A and before either Rebecca-authorized L8 GPU sentinel execution.

## Inputs and SHAs reviewed

- Authoritative routing head: `architect/l8-gpu-adoption-spec` at `b402fe07570843f3d234938a80690820dde2f849`.
- Specification result: `3f7ac50a38e08fdd482786c500ac11855863328f`.
- Handoff: `handoffs/ARCHITECT_TO_CRITIC_L8_GPU_V1.5_EXECUTABILITY_REMEDIATION.md`.
- Proposed amendment: `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.5.md`.
- Operative v1.4 base: `4c84248897fe7c0b10f669bba352a05e3268edf2`.
- TASK BUILDER B1–B10 block: `5485dd2`.
- Constitution/protocol: `docs/ARCHITECTURAL_CONSTITUTION_v2.md`.
- Provenance sources: `docs/rulings/provenance_log.md` and `docs/rulings/M0_DECISION_SHEET.md`.
- Five new JSON artifacts and their raw-byte sidecars, plus the pre-existing known-good fixture pair.

## Verdict

- **LAW_FIDELITY: BLOCK**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

The proposal returns to ARCHITECT. It does not route to Rebecca as a clear amendment and does not release TASK BUILDER.

## First checklist item — mandatory §5 law/provenance audit

### P1/P2: repo-first and verbatim law diff

The quoted L8, L18, and L19 text in v1.5 §1 was compared character-for-character against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` lines 28, 54, and 55. All three quotations are verbatim, including punctuation and parenthetical text. The cited constitutional file exists in-repo. **P1 PASS; P2 PASS.**

### P3: threshold/test-criterion source tags

The amendment supplies a general `[PROPOSED]` rule and inline tags for its new criteria, and preserves the numeric beta-star `0.2` and rho `0.8` bars as `[BAR-Entry 11]`. However, the assertion that **four doses** is locked by `[BAR-Entry 11]` is not supported by Entry 11's adopted M0 sheet: that source locks **at least three noise doses**, not exactly four. Exact four-dose use may be inherited operationally, but it cannot be attributed to Entry 11 as written. **P3 BLOCK (provenance/source-class defect).**

### P4: date and regime

The specification and each new JSON artifact state `2026-08-21` and Regime B. **P4 PASS.**

### P5: deviation memorialization

The comparator change is expressly proposed, inoperative, and Rebecca-gated; the amendment does not claim an existing waiver. **P5 PASS at proposal stage.**

### P6: provenance citations

`[OP-Entry 22]` does not support v1.5 §6's claim that the parent “never starts a third child.” Provenance Entry 22 governs O-13, O-14, and O-15; its O-15 ruling establishes diagnostic-versus-scoring execution channels. It does not establish a two-child/two-execution cap. The same tag is used for no-third-execution language inherited from v1.4, but the cited entry still does not say that. **P6 BLOCK (provenance defect).**

The M0 sheet does support beta-star `0.2`, rho `0.8`, and five seeds for L8. The official PyTorch CUDA-13.0 index was independently inspected and contains CPython 3.11 wheels for `torch==2.13.0+cu130`; NumPy `1.26.4`, SciPy `1.13.1`, and rfc8785 `0.1.4` are present at their specified official indexes.

## Blocking findings

### BF1 — B2 configuration template contradicts its normative construction rule

**Classification:** specification defect / construction bug forced by the specification.

V1.5 §3.1 says the committed template uses the exact v1.4 §8.1 schema and key order, **except** that `implementation_sha` is `COMMIT_A_SHA`. V1.4 §8.1 fixes `date` to literal `2026-08-20`. The committed template instead contains `"date": "2026-08-21"`. Because the only declared exception is `implementation_sha`, an implementation cannot both validate the committed template and obey the normative construction rule. B2/B3 closure is therefore incomplete.

### BF2 — B11 is not an executable deterministic fixture

**Classification:** specification defect / missing executable inputs.

V1.5 §10.1 requires two cutoff-straddling fixtures but leaves `EPS_C` undefined and supplies only input fragments plus expected coverage indices. It does not give committed fixture rows or literal expected values for the required answered-correctness vector, risk, dose summary, beta-star, rho, and predicates. It also does not specify the additional dose/seed inputs necessary to derive beta-star and rho from the four-element selection example. TASK BUILDER would have to invent inputs, schemas, and expected values. This directly violates the binding executability rule that a distribution or sketch is not a realization and that every required expected result be fixed.

### BF3 — the seventeen-row executability matrix cannot enforce its own declared contract

**Classification:** specification defect / construction ambiguity.

V1.5 §10 requires every matrix row to have a normative section, exact schema/type definition, fixture or literal expected value, failure disposition, and test identifier. The committed matrix rows contain only `control_id`, `spec_section`, `fixture_or_manifest`, and `failure_status`. They contain no test identifier, no exact fixture path for several rows, and no literal expected value or schema/type reference capable of machine validation. Examples include `"known-good + sentinel rows"`, `"repeat protocol"`, `"controlling §7.1 schema"`, and `"lower/upper clipping tie fixtures"`. The future TASK BUILDER trace adds an `implementation_test` column, but the specification leaves those identifiers for TASK BUILDER to invent and provides no expected canonical trace digest. The required contract-coverage test is therefore not deterministically constructible.

### BF4 — dependency source-policy preflight has no executable verification method

**Classification:** specification defect / provenance-instrument ambiguity.

The exact pinned wheels are obtainable, so package availability itself passes. But v1.5 §9 requires preflight to compare “source policy” before RNG construction while neither the manifest nor the specification defines a runtime provenance record or algorithm for determining the index from which an installed distribution was obtained. Standard installed package metadata and `pip freeze --all` do not reliably retain the source index for ordinary version-pinned wheels. TASK BUILDER must invent a provenance mechanism or cannot implement the mandatory check. The dependency freeze is thus only partly executable.

### BF5 — source attribution for exact four-dose locking and the two-child cap is false

**Classification:** provenance defect / versioned-law compliance defect.

As detailed under P3/P6, `[BAR-Entry 11]` supports a minimum of three doses, not an exact four-dose lock, and `[OP-Entry 22]` does not establish the two-child cap. These citations must be corrected to the actual adopting authority or the rules must remain `[PROPOSED]` pending Rebecca. LAW_FIDELITY cannot pass while the cited sources do not say what the specification attributes to them.

## B1–B11 closure reconciliation

| Item | Result | Independent finding |
|---|---|---|
| B1 | CLOSED | Count polarity, denominators, undefined-rho treatment, and apparatus-invalid exclusions are explicit. |
| B2 | BLOCK | Header nesting is explicit, but the committed template contradicts the exact-template rule on `date`. |
| B3 | BLOCK | Runtime SHA lifecycle is mostly explicit; the invalid template prevents end-to-end construction. |
| B4 | CLOSED | Row types, nulls, predicate polarity, and literal deterministic outputs are specified. |
| B5 | CLOSED | Twelve-row status vocabulary, boundaries, preserved-path type, and assertion rule are committed. |
| B6 | CLOSED | Isolated rehearsal roots, target/temp/previous/incomplete names, and preservation semantics are explicit. |
| B7 | CLOSED subject to provenance correction | Parent/child frames and byte custody are executable; `[OP-Entry 22]` does not source the two-child cap. |
| B8 | CLOSED | Evaluator scope, calibration source, worker rule, final block, queue bound, identity restoration, and controlling publication contract are stated. |
| B9 | CLOSED | Counter invariants, scoped-failure behavior, partial-run exclusion, top-level `failure`, and verdict mapping are stated. |
| B10 | BLOCK | Versions and official wheels exist, but mandatory installed-source verification is unspecified. |
| B11 | BLOCK | `EPS_C`, full fixture inputs/schema, and required literal downstream expected outputs are absent. |

## Seventeen-control executability reconciliation

`COUNT_EVENT_POLARITY`, `HEADER_TOPOLOGY`, `CONFIG_SELF_IDENTITY`, `DETERMINISTIC_ROW_TYPES`, `REHEARSAL_STATUS_ENUM`, `REHEARSAL_FILESYSTEM`, `REPEAT_CUSTODY`, `FULLSCREEN_PIPELINE`, `COUNTER_INVARIANTS`, `RNG_IDENTITY`, `QUEUE_RESIDENCY_BOUND`, `LOCKED_BAR_LITERAL`, `UNKNOWN_FIELD_REJECTION`, `ATOMIC_PAIR_RECOVERY`, and `AUTHORIZATION_BOUNDARY` have substantive clauses, though `CONFIG_SELF_IDENTITY` is blocked by BF1 and `REPEAT_CUSTODY` has BF5's provenance defect.

`DEPENDENCY_FREEZE` is blocked by BF4. `COVERAGE_TIE_RULE` is blocked by BF2. Independently, the matrix-wide enforcement claim is blocked by BF3 because none of the seventeen rows carries the required fixed implementation-test identifier and multiple fixture references are descriptive rather than exact.

## Independent integrity checks and preserved evidence

- All six reviewed JSON files parsed successfully.
- Raw SHA-256 was independently recomputed for the config template, dependency manifest, executability matrix, rehearsal contract, rehearsal prior, and known-good fixture. Every sidecar matched.
- `git diff --check 4c842488..3f7ac50` passed.
- The exact dependency versions are available from the named official indexes, including a CPython 3.11 Windows and Linux wheel for `torch==2.13.0+cu130` at the CUDA-13.0 PyTorch index. This valid evidence is preserved; BF4 concerns installed-source verification, not wheel availability.
- B1, B4, B5, B6, B8, and B9 remediation evidence remains valid and need not be redesigned unless later edits touch it.
- No defect found here invalidates the prior known-good fixture digest `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7` or frozen-calibration digest `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e`.

## Non-blocking findings

- The full-screen arithmetic is internally consistent: sixty-two blocks of thirty-two plus one block of sixteen equals 2,000 repetitions.
- B11's proposed lexicographic comparator is clear as a rule and appropriately Rebecca-gated; the blocker is the missing executable fixture/output closure, not the comparator's stated ordering.

## Exact next authorized role

**ARCHITECT**, via WORKFLOW COORDINATOR, for minimal remediation of BF1–BF5. After a new committed handoff, route to a fresh-context CRITIC for law fidelity and executability review. Only `LAW_FIDELITY: PASS` plus `SUBSTANTIVE: CLEAR` may then route to Rebecca. TASK BUILDER remains held.

## Explicitly prohibited actions

- No implementation, sentinel execution, full-screen execution, failure rehearsal, scoring, protected/hold-out/courier seed access or exposure, rerun, failed-run replacement, G2–G4 freeze, merge to main, or L15/L16/L17 work before M5.
- No CRITIC modification of the specification, implementation, scoring artifacts, or `STATE.md`.
- No reinterpretation or replacement of locked bars and no operationalization of B11 without Rebecca's express amendment approval.

## Public-repository safety attestation

Before push, CRITIC scanned the review artifact and staged diff for credentials, API keys, tokens, passwords, private keys, personal contact details, machine identifiers, private absolute paths, environment dumps, PII, and protected-seed material; ran repository policy checks and `git diff --check`; and manually reviewed the artifact. No prohibited content was found. Public repository SHAs, repository-relative paths, package-index facts, scientific constants, and approved fixture digests were classified as acceptable.

## Execution/custody confirmation

No scoring, diagnostic execution, sentinel/full-screen run, failure rehearsal, rerun, protected/hold-out/courier seed access or exposure, or unauthorized merge occurred. Neither permitted sentinel execution was consumed.
