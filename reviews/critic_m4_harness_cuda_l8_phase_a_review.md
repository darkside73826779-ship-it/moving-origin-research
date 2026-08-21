# CRITIC Review — M4 Harness CUDA-L8 Phase A Contract

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Independent Phase A law-fidelity and deterministic-executability review before any M4 harness implementation.

## Inputs and SHAs reviewed

- Repository base: `7d6e499cb8a0cf9859cc05b37ec4e97767c4839e`.
- Rebecca directive: `coordinator/m4-harness-architect-intake` at `b32992e7162e129312d2b2493ddbea18b234db81`.
- Authoritative ARCHITECT routing head: `architect/m4-harness-contract` at `60e515c4b14160d282c5ba0b7b6b8c2a8f63dd54`.
- Design result: `76fb37ee359abf2539131c854befe0f695178036`.
- Handoff: `handoffs/ARCHITECT_TO_CRITIC_M4_HARNESS_CUDA_L8_PHASE_A.md`.
- Primary contract, changelog, eleven `specs/data/m4_*.json` artifacts and sidecars, the named M4 specifications, approved L8 v1.5 authority, constitution §5/L8/L18/L19, and cited provenance Entries 11, 43, 72, and 76.

## Verdict

- **LAW_FIDELITY: BLOCK**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

Phase A returns only to ARCHITECT through WORKFLOW COORDINATOR. Phase B remains `PROVISIONAL_BLOCKED`; TASK BUILDER remains held.

## First checklist item — law/source/provenance audit

- **P1/P2 PASS:** I compared P1–P6 and the L8/L18/L19 quotations directly with `docs/ARCHITECTURAL_CONSTITUTION_v2.md`; each quoted paragraph is verbatim after removing only Markdown quote prefixes.
- **P3 BLOCK:** Contract §1 assigns beta-star, rho, minimum doses, five scoring seeds, and the specificity leg collectively to `[BAR-Entry 11]`. Entry 11 distinguishes the five-seed rule as Entry 11.3, while the standardized specificity design was approved by Entry 76 Ruling 3. The M4 task specification itself uses `[BAR-Entry 11.3]` for five L8 seeds. The grouped tag therefore misstates two sources and fails the required threshold/source audit.
- **P4 PASS:** Every new normative Markdown and JSON artifact states 2026-08-21 and Regime B.
- **P5 PASS:** The contract remains proposed and expressly withholds implementation/scoring authority. No signed waiver is claimed.
- **P6 BLOCK:** I verified Entries 11 and 76 against their actual text; they do not support the grouped attribution described above. Entries 43 and 72 do support the retained FWFP and L3 sequencing gates.

## Blocking findings

### BF1 — five-seed and specificity provenance is misclassified

**Classification:** provenance/source-tag defect.

Contract §1 collapses heterogeneous sources into `[BAR-Entry 11]`. Entry 11.3 is the locked five-seed source for L8; Entry 76 Ruling 3 is the approval source for the standardized proximal-component specificity design. The current sentence does not pass P3/P6 and cannot be routed as law-faithful.

### BF2 — required runtime configuration template is absent

**Classification:** executability defect / missing committed input.

Contract §7 requires runtime configuration to be materialized from a committed template by replacing only implementation/result identity placeholders. No configuration template is committed or named in the Phase A package. The schema is not an instance and supplies no fixed placeholder bytes, values, ordering, or expected digest. TASK BUILDER would have to invent the executable configuration source.

### BF3 — executability-matrix fixture names are not concrete fixtures

**Classification:** executability defect / construction ambiguity.

The matrix claims to fix every fixture and assertion, but rows reference undefined labels such as `synthetic_wrong_sha`, `synthetic_request`, `synthetic_all_arms`, `fault_cuda_unavailable`, `fault_gpu_calibration_call`, `six_fixed_faults`, `beta_failure`, `fault_second_replace`, `synthetic_gate_matrix`, and `synthetic_invalid_cross_fields`. No committed arrays/objects, deterministic constructor, exact mutation rule, canonical bytes, or expected digest exists for them. The compatibility fixture also does not contain a complete primitive-tape request/buffer realization. These are fixture descriptions, not executable realizations.

### BF4 — compatibility report rows and canonical expected outputs are undefined

**Classification:** result-schema/executability defect.

The report schema constrains each run's `rows` only as an arbitrary JSON object and sets only `minItems:13`; it does not define the row schema, exact 13-row ordering, required observed fields, or canonical expected report/response digest. The prose demands literal-field and canonical-response-byte equality, but the package commits no expected response array or digest. The six failure-injection records similarly allow unconstrained string codes and do not bind each named case to a literal mutation and expected enum. TASK BUILDER must invent report bytes and expected digests, violating the end-to-end executability requirement.

### BF5 — a valid zero-variance statistical failure cannot be represented consistently

**Classification:** schema/contract inconsistency.

Contract §4.2 says zero pooled variance remains an included statistical predicate failure unless an independent apparatus check proves a fault. The adapter response schema permits `beta_star:null`, but the per-law L8 seed schema requires `beta_star` to be a JSON number. A valid non-apparatus zero-variance seed therefore has no consistent representation in the required published L8 artifact. Treating it as apparatus failure would contradict the contract; emitting null would fail the law schema.

## Non-blocking findings

None beyond the blocking findings.

## Preserved evidence

- The routing head is a handoff-only child of the design result; both identities are preserved.
- All eleven JSON artifacts parse. I independently recomputed every raw sidecar digest and all match.
- The compatibility fixture contains exactly seven rho, four complete-verdict, and two tie cases. I independently recomputed both tie-case dose summaries and beta-star values; they match the committed literals exactly at the available binary64 representation.
- The binding manifest correctly remains `PROVISIONAL_BLOCKED`, requires both `PRIMITIVE_TAPE` and `ESTIMATOR_ONLY`, and contains no invented final implementation identity.
- The full L18 arm names, negative-label preservation, O-14/O-15 boundaries, five downstream scoring gates, no-fallback rule, protected-seed fence, and Rebecca-only release/merge authority remain valid and are not invalidated by these defects.

## Exact next authorized role

**ARCHITECT**, routed through **WORKFLOW COORDINATOR**, for minimal remediation of BF1–BF5. Return a committed Phase A delta to a fresh-context CRITIC. Phase B reconciliation and M4 implementation remain held.

## Explicitly prohibited actions

- No harness implementation, diagnostic execution, scoring, protected/hold-out/courier seed access or exposure, rerun, L8 execution change, G2–G4 freeze, L15/L16/L17 work, durable-state/provenance mutation, TASK BUILDER release, merge, or gate decision.
- CRITIC did not edit or co-author the contract, schemas, fixtures, matrix, scoring artifacts, or STATE.md.

## Public-repository safety attestation

Before push, CRITIC scanned the complete new review commit and diff with gitleaks and manually checked for credentials, keys, tokens/passwords, personal contact/PII, machine identifiers, environment dumps, protected-seed material, persistent task/session IDs, and private absolute paths. No prohibited content was found. Repository SHAs, repository-relative paths, synthetic fixture labels, and governance/scanner terms were classified acceptable. `git diff --check` passed.

## Execution confirmation

No implementation, diagnostic/scoring execution, protected-seed access or exposure, rerun, L8 execution change, durable-state/provenance mutation, or unauthorized merge occurred.
