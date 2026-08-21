# CRITIC Review — Revised M4 CUDA-Ready / Parallel-CPU-L8 Phase A v1.1

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Independent law-fidelity and substantive review before Rebecca; review only.

## Inputs and SHAs reviewed

- Authoritative ARCHITECT routing head: `architect/m4-cuda-ready-cpu-l8` at `2e2b7f51f5557946bc95cc1b5503eaed286685ab`.
- Design/result commit: `1c194632138c83ae911a1146c2249122743f93fe`.
- Revised coordinator authority: `coordinator/m4-cuda-ready-cpu-l8-directive` at `4de2ace8dfba59dd5cd6698bf90bb26307b0194f` (CPU-redirection result `d821a5c534f1c4547b99a2fb0079266497ddd537`).
- Prior review: `critic/m4-harness-cuda-l8-phase-a-review` at `4a581cb5e793579e5c98478e36cc9d5e8210ff43`, artifact `reviews/critic_m4_harness_cuda_l8_phase_a_review.md`.
- Handoff: `handoffs/ARCHITECT_TO_CRITIC_M4_CUDA_READY_CPU_L8_PHASE_A_V1_1.md`.
- Primary contract: `specs/m4_harness_cuda_l8_contract_v1.md`.
- The full design delta, changed/created `specs/data/m4_*_v1.json` artifacts and sidecars, controlling M4 specifications, constitution v2 §5/L8/L18/L19, CPU-L8 directive, and cited provenance sources.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

The original BF1–BF5 are closed, and the revised backend architecture is directionally faithful. Two residual deterministic-contract defects prevent clearance. M4 implementation, compatibility execution, TASK BUILDER release, and scoring remain held.

## Law/source/provenance audit

- **P1/P2 CLEAR:** The binding law text is committed. The P1–P6 and L8/L18/L19 quotations in contract §1 match `docs/ARCHITECTURAL_CONSTITUTION_v2.md` verbatim apart from Markdown quote prefixes.
- **P3 CLEAR for reviewed locked criteria:** beta-star `0.2`, rho `0.8`, and the minimum-dose rule cite `[BAR-Entry 11]`; the five-seed/all-seeds rule cites `[BAR-Entry 11.3]`; standardized proximal-component specificity cites `[OP-Entry 76 Ruling 3]`. Proposed harness mechanics remain tagged `[PROPOSED]` and do not purport to gate before Rebecca.
- **P4 CLEAR:** New normative Markdown and JSON artifacts state 2026-08-21 and Regime B.
- **P5 CLEAR:** Native CUDA L8 is explicitly `SHELVED/INOPERATIVE`, serial CPU is unauthorized, and the contract neither claims a waiver nor changes a locked scoring bar.
- **P6 CLEAR:** The five-seed and specificity claims were checked against the controlling M4 specification/task specification and provenance references; the corrected attributions are faithful.

## BF1–BF5 closure review

1. **BF1 CLOSED:** heterogeneous provenance is separated correctly.
2. **BF2 CLOSED:** `m4_harness_config_template_v1.json` commits one ordered source with exactly one occurrence of each of the three named placeholder tokens and a matching raw-byte sidecar.
3. **BF3 CLOSED:** executable fixtures now contain a complete primitive request, literal base64 buffers, matching byte lengths/raw digests, explicit JSON-pointer mutations, deterministic constructors, and expected enums/objects.
4. **BF4 CLOSED:** expected responses fix thirteen ordered rows; the compatibility schema fixes successful-run row and failure-injection order; the constructor deterministically yields the stated 11,483-byte report and digest.
5. **BF5 CLOSED:** adapter and law schemas represent ordinary zero-pooled-variance as nullable beta, `beta_defined=false`, false predicates, non-apparatus status, and per-law `KILL`.

## Blocking findings

### BF6 — final compatibility-report identity substitution is not defined by marked placeholders

**Classification:** reconciliation/executability contradiction.

Contract §6 requires the final report to equal the committed expected report after replacing only the **schema-marked** final parallel-CPU identity/digest placeholders, with all other bytes fixed. However, `m4_l8_compatibility_expected_report_v1.json` stores `1111111111111111111111111111111111111111` and `2222222222222222222222222222222222222222` as ordinary values for `implementation_sha` and `implementation_review_sha`. They are not named placeholder tokens, and `m4_l8_compatibility_report_schema_v1.json` merely accepts any 40-character lowercase hex SHA; it does not mark either value or field as a reconciliation placeholder. The same `111...` identity is embedded in the primitive fixture.

Consequently the future reconciler must either leave false identities in authoritative expected bytes or invent which valid-looking values may be replaced, violating the exact-change rule and no-implementer-invention requirement. Commit explicit, uniquely named one-use placeholder tokens (with a materialization rule and revised digest constructor), or define an equally unambiguous schema-marked substitution mechanism.

### BF7 — law-artifact schema does not enforce its claimed ordered identities

**Classification:** schema/negative-label integrity defect.

Contract §7 says the law schema fixes L8 arm order, three L14 couplings, and twenty-four L18 law/arm control records. `m4_law_artifact_schema_v1.json` instead constrains only lengths and each item's enum. It accepts, for example, eight repeated `candidate` L8 arms, five repeated seed ordinal zero records, three repeated L14 coupling IDs, or twenty-four repeated L18 law/arm pairs. Thus an artifact can omit required negatives or reorder/duplicate identities while passing the named schema, contradicting the fixed-order and no-negative-renaming/omission contract.

Encode the exact ordered identities with `prefixItems` plus `items:false` (including seed ordinals and the complete law/arm Cartesian order), or require an explicit semantic validator and committed negative fixtures that deterministically reject every duplicate, omission, and reordering. The current generic cross-field fixtures do not cover these identity failures.

## Non-blocking observations

- `PARALLEL_CPU_L8_EXACT_SHA` (`gofast`) is consistently the sole current L8 backend; `NATIVE_CUDA_L8` (`go faster`) is shelved/inoperative and `GO!` is not authorized.
- CUDA is confined to AI-model execution. The synchronized blocking device-to-host custody boundary, immutable host digests, host-only L8 request, and no-fallback semantics are coherently separated.
- The binding manifest correctly remains `PROVISIONAL_BLOCKED` with null final CPU identities and fail-closed `M4_CPU_L8_BINDING_UNRECONCILED` routing.
- All sixteen `specs/data/m4_*_v1.json` artifacts parsed, every adjacent sidecar matched raw bytes, all four literal primitive-buffer lengths and SHA-256 values matched their base64 payloads, and the three configuration placeholders each occurred once. No harness, compatibility suite, diagnostic, scoring run, or protected-seed operation was performed.

## Exact next authorized role

Return only to **WORKFLOW COORDINATOR** for routing to ARCHITECT for minimal BF6–BF7 remediation. After a committed correction, route to a fresh-context CRITIC, then stop for Rebecca. This review does not make a gate decision.

## Explicit prohibitions preserved

No edits to reviewed work, implementation, diagnostic or scoring execution, seed access/exposure, rerun, native-CUDA adoption, backend fallback, L8 execution change, state/provenance mutation, merge, TASK BUILDER release, or routing beyond WORKFLOW COORDINATOR occurred or is authorized.

## Public-repository safety attestation

Before push, CRITIC scanned the complete review delta for credentials, keys, tokens/passwords, private absolute paths, personal contact/PII, machine identifiers, environment dumps, protected-seed material, and persistent task/session identifiers. The review contains only repository SHAs, repository-relative paths, synthetic fixture identities, and governance terms. No prohibited content was found. `git diff --check` passed.
