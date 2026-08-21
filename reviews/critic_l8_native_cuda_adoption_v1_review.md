# CRITIC Review — L8 Native-CUDA Backend Adoption v1

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Independent law-fidelity and deterministic-executability review of the prospective native-CUDA diagnostic-backend adoption contract before implementation or execution.

## Inputs and SHAs reviewed

- TASK BUILDER evidence/authority head: `taskbuilder/l8-cuda-legacy-compat` at `8251d95b31107f4a710463fb0574b5bd33a44325`.
- Authoritative ARCHITECT routing head: `architect/l8-native-cuda-adoption` at `5cee6cd19bc5a3d532700a7eb34a0e02e56bd57a`.
- Design result: `9833f83c1f2900274f10d698efdee0f9f1c6ad3e`.
- CPU oracle commit/digest: `6d455bb` / `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`.
- Native implementation evidence identity: `e5367fd4991713d20386619efc92afd3bd1cf76d`.
- 1,000-repetition evidence commit/digest: `e857908ceeaa25ebfff8351d8f34a3b99e9d8276` / `f0752bfbe95f195eb4a2b75fb4d0375fb169bf7591247a2299cfccd438adc65a`.
- 10,000-repetition evidence commit/digest: `9678713ef13af1d8746f9ecd9a04457a6461c270` / `032787bc6a1625ad86b63295a03980e88f982723115452f8080e6c0d606936e2`.
- Handoff: `handoffs/ARCHITECT_TO_CRITIC_L8_NATIVE_CUDA_ADOPTION_V1_2026-08-21.md`.
- Primary specification, changelog, seven JSON contracts/fixtures/matrix artifacts and sidecars, approved v1.5 dependency contract, Rebecca diagnostic-authorization record, constitution §5/L8/L18/L19, M0 decision sheet, and provenance Entries 11, 22, and 76.

## Verdict

- **LAW_FIDELITY: BLOCK**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

The proposal remains prospective and inoperative. It returns to WORKFLOW COORDINATOR only for Rebecca's decision and any expressly authorized routing. Existing native evidence remains feasibility evidence and does not qualify retroactively.

## First checklist item — law/source/provenance audit

- **P1/P2 PASS:** I directly compared the quoted P1–P6 and L8/L18/L19 text with `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; all quotations are verbatim after removing only Markdown quote prefixes.
- **P3 BLOCK:** The grouped L8 bars are supported by `docs/rulings/M0_DECISION_SHEET.md` line 21 and Entry 11's adoption of that sheet. However, §6.1 tags the universal CPU no-rerun claim as `[O-14]`; provenance Entry 22 defines O-14 as the M1 I3 empirical-null replacement, not a universal no-rerun law. Later shorthand does not replace the actual source text required by P3/P6.
- **P4 PASS:** The new artifacts state 2026-08-21 and Regime B. BF6 below separately addresses the invalid freezing of that design date into future runtime records.
- **P5 PASS:** No law deviation or adoption is asserted; every new gate remains proposed and Rebecca-gated.
- **P6 BLOCK:** Direct inspection of Entry 22 disproves the `[O-14]` source claim in §6.1. The M0 sheet/Entry 11 support the grouped L8 bars, and the Rebecca authorization record supports the prototype and diagnostic executions described, but neither approves the prospective adoption criteria.

## Blocking findings

### BF1 — the universal no-rerun rule is cited to the wrong provenance item

**Classification:** provenance/source-tag defect.

Specification §6.1 cites `[O-14]` for “CPU is not rerun.” Entry 22's actual O-14 ruling concerns replacement of an under-powered I3 tolerance with an empirical-null procedure. The repository later uses O-14 colloquially for no-rerun-on-failure, but P6 requires citation to actual source text. The no-rerun and no-replacement protections must remain; their source attribution cannot be reconstructed from later shorthand.

### BF2 — RNG and dependency identities are not frozen end-to-end

**Classification:** executability/provenance defect.

Section 4 requires a frozen `_standard_gamma` output fixture, but `l8_native_cuda_rng_fixture_v1.json` contains only four identity/hash/seed derivations and no generator output bytes, arrays, code-object/module digest, draw-shape result, or expected canonical digest. It also does not enumerate the required 480 `(cell,arm)` identities. The direct wheel URLs/hashes and PEP 610 rules are deferred to implementation with “must be copied” rather than bound by an exact manifest path and raw digest in this contract/configuration. TASK BUILDER must construct material inputs that the specification says are frozen.

### BF3 — the executability matrix is descriptive, not executable

**Classification:** executability defect / construction ambiguity.

The twenty rows provide no fixed pytest node IDs despite §11 requiring every test to exist and collect once. Most `fixture` values—such as `draw_schedule`, `scheduler`, `manifest`, `boundary`, `regression`, `repeat`, and `publisher`—are labels, not committed realizations. Mutations such as “each limit plus one binary64 ulp” and “interrupt at each atomic boundary” have no exact base object, mutated bytes, ordered cases, expected output object, or canonical digest. An implementer must invent the tests and fixtures.

### BF4 — the oracle/configuration identity is underbound

**Classification:** provenance/executability defect.

The configuration schema fixes only abbreviated commit `6d455bb` and accepts any single-level `diagnostics/*.json` path, rather than the full oracle commit and exact `diagnostics/l8_power_analysis_results.json` path. It contains no dependency-manifest digest, PEP 610 digest set, `_standard_gamma` identity/output-fixture digest, complete 240-row cell-order digest, or committed configuration-template instance. The backend request supplies opaque dependency/device digests without a schema that fixes their canonical source bytes. Distinct configurations can therefore validate while selecting different executable inputs.

### BF5 — fail-closed and negative outcomes cannot be serialized faithfully

**Classification:** result-schema/state defect.

The result schema always requires exactly two complete 240-row runs, even for a preflight or first-run `INSTRUMENT_FAILURE`. It fixes `repeat_payloads_identical:true`, so a `REPEAT_MISMATCH` failure listed by the same schema cannot validate. Each run limits `boundary_cells` to one, so the required two-boundary-cell regression fixture cannot preserve both offending cells. These contradictions prevent publication of several mandatory negative outcomes and would hide or fabricate evidence.

### BF6 — region/comparison/result bytes are not deterministic

**Classification:** schema/executability defect.

Individual and aggregate `region` values are unconstrained strings; their exact enum, sixteen-row order, and CPU-oracle mapping are not copied or digest-bound. `comparison.per_metric` is an arbitrary object, so the five per-cell and five mean regression results, pass/fail flags, ordering, and offending ordinals are undefined. The contract requires byte-identical “canonical scientific payloads” but does not define that payload's exact schema or digest projection. Runtime result/request schemas also require the design date `2026-08-21`, misdating any later authorized execution instead of fixing a runtime-date rule. Exact adoption bytes therefore require implementer choices.

### BF7 — performance failure has no valid disposition

**Classification:** verdict/failure-state defect.

Both native runs must meet the performance threshold, but the top-level verdict enum has no performance-regression verdict and the failure-code enum has no performance code. Performance is expressly not a scientific-consistency result, and an elapsed-time miss is not one of the defined apparatus faults. A scientifically consistent run that takes too long therefore has no contract-valid terminal classification.

## Non-blocking findings

None beyond the blocking findings.

## Preserved evidence

- Routing head `5cee6cd…` is a handoff-only child of design result `9833f83…`; both identities are preserved.
- All seven JSON artifacts parse and every raw SHA-256 sidecar matches independently.
- All four committed RNG identity/hash/seed triples independently recompute exactly.
- The committed 1,000- and 10,000-repetition evidence digests match their sidecars. The 10,000 evidence remains one prior native comparison, not a prospective qualifying run.
- For historic ordinal 47, I independently recomputed absolute false-kill difference `0.0222` and false-pass difference `0.0018`. The fixture accurately says the later boundary rule would classify the same values as `BOUNDARY_CONSISTENT` only in a new authorized run, while `qualifies_historic_evidence=false` preserves the existing `UNRESOLVED_BOUNDARY_CELL` finding.
- The signed-regression formulation correctly permits improvements without offsetting a metric-specific regression. Exact selected-point and aggregate-region invariants, no fallback, two-run custody, O-14/O-15, negative preservation, M4 Phase B hold, protected-seed fences, and Rebecca-only adoption/merge authority remain valid.

## Exact next authorized role

**WORKFLOW COORDINATOR only**, to hold the BLOCK for Rebecca's decision and route any expressly authorized remediation. No direct CRITIC handoff to ARCHITECT or any implementation/execution role is authorized.

## Explicitly prohibited actions

- No native-CUDA implementation, diagnostic execution, scoring, protected/hold-out/courier seed access or exposure, rerun, negative renaming, bar/control change, G2–G4 freeze, adoption claim, M4 use, durable-state/provenance mutation, merge, RECORDER/INTEGRATOR/JUDGE routing, or L15/L16/L17 work before M5.
- CRITIC did not edit or co-author the specification, schemas, fixtures, matrix, implementation, evidence, scoring artifacts, or STATE.md.

## Public-repository safety attestation

Before push, CRITIC scanned the complete new review commit and diff with gitleaks and manually checked for credentials, private keys, tokens/passwords, personal contact/PII, machine identifiers, environment dumps, protected-seed material, persistent task/session IDs, and private absolute paths. No prohibited content was found. Repository SHAs, repository-relative paths, public dependency identities, synthetic fixture labels, and governance terms were classified acceptable. `git diff --check` passed.

## Execution confirmation

No implementation, CUDA diagnostic, scoring, protected-seed access or exposure, rerun, evidence mutation, negative relabeling, durable-state/provenance mutation, or unauthorized merge occurred.
