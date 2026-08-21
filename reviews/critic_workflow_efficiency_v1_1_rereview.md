# CRITIC Rereview — Workflow Efficiency v1.1 BF1–BF7 Remediation

**Date:** 2026-08-21

**Regime:** B

**Gate served:** Independent deterministic-design rereview before any Workflow Efficiency P1–P10 mechanical implementation.

## Inputs and SHAs reviewed

- Repository base: `d38f9069d9a4f2a92ffb3a29d6f80ef4e7253da9`.
- Authority package: `coordinator/efficiency-change-program-intake` at `67280dfd3ee6e00459f3f23d4d98dff637eb1760`.
- Prior review: `critic/workflow-efficiency-v1-review` at `0c6fac88424eaee6966525d45fb7385686a197d7`.
- Authoritative ARCHITECT routing head: `architect/workflow-efficiency-spec` at `6d8f6b99d3fc05cbb3de8d7885d0470fdd6d5536`.
- Remediated design result: `15db61a4beaa969a480402fb4276050ea0b07838`.
- Handoff: `handoffs/ARCHITECT_TO_CRITIC_WORKFLOW_EFFICIENCY_V1_1.md`.
- BF1–BF7 Markdown delta, five remediated/new JSON contracts and sidecars, prior preserved design artifacts, constitution §5, and provenance Entry 57.

## Verdict

- **LAW_FIDELITY: PASS**
- **SUBSTANTIVE: BLOCK**
- **Combined disposition: BLOCK**

The v1.1 design returns only to ARCHITECT for minimal remediation. The five material choices do not route to Rebecca and TASK BUILDER remains held.

## First checklist item — §5 law/provenance audit

- **P1/P2 PASS:** The P1–P6 quotation remains byte-faithful in text to `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1; every authority source exists at the named repository SHA.
- **P3 PASS:** New schemas, thresholds, transitions, custody rules, path rules, and STOP criteria remain `[PROPOSED]`; Entry 57 alone is correctly `[OP-Entry 57]`.
- **P4 PASS:** Every new normative artifact states 2026-08-21 and Regime B, including JSON Schema artifact metadata.
- **P5 PASS:** No constitutional/scientific deviation or waiver is claimed; all changes remain inoperative and Rebecca-gated.
- **P6 PASS:** Entry 57 still supports “approved/binding on new work” while separately withholding any assertion that the repository-public flip occurred.

## BF1–BF7 reconciliation

| Prior finding | Result | Independent rereview |
|---|---|---|
| BF1 manifest custody | CLOSED | Sender-role conditionals bind extensions; `artifacts` is nonempty and digest-valued; path grammar rejects absolute drives, leading slash, backslash, traversal, and duplicate object keys. Prose and verification fixtures require semantic inventory completeness. |
| BF2 trace dispositions | CLOSED | Separate CRITIC/TASK BUILDER disposition schema binds source trace digest, specification commit, source row order/digest, reviewer verification ID, row disposition, and overall result without permitting source edits. |
| BF3 preflight v2 | **BLOCK** | Path/object types and normalized findings were added, but multi-commit range reduction and combined-scan provenance remain undefined; see BF8 below. |
| BF4 immutable checkout | **BLOCK** | Root marker, collision, receipt, cleanup, and ancestry mechanics are concrete, but the exact-ref equality rule cannot represent the required routing-head/design-result pair; see BF9. |
| BF5 JUDGE custody | CLOSED | Canonical strict-base64 envelope, Coordinator byte relay, maximum size, validation, publication, idempotent replay, uncertain-push recovery, and mismatch/scan STOP behavior are fixed. |
| BF6 state metadata | CLOSED | Exact JSON schema, RFC 8785/sidecar contract, owner paths, source-commit semantics, empty supersession, checkpoint naming, and exact legacy-status insertion are fixed. |
| BF7 rollback | **BLOCK** | Authority, cascade, inverse ownership, and evidence preservation are fixed, but the exact state machine lacks pre-release failure transitions; see BF10. |

## Remaining blocking findings

### BF8 — preflight range histories cannot be reduced to the v2 path/finding schema deterministically

**Classification:** executability defect / construction ambiguity.

The tool forms a union of paths across every per-parent diff and the combined base→tip diff, then emits one `paths` row per path with one `change_type`. No reduction rule selects that single value when a path has multiple changes across the range. Examples include add→modify, add→delete where the path exists at neither endpoint, rename→modify, or type-change→delete. These cases yield materially different `added|modified|deleted|renamed|type_changed` labels and hashes, yet the specification fixes no event precedence or per-event row form.

The same issue affects findings. Every merge-parent diff and the combined base→tip diff is scanned, but no deduplication/domain rule specifies whether identical evidence found in multiple scan domains produces one or several findings. `commit_sha` is mandatory even for a combined base→tip finding, but no exact commit value is defined for that non-commit scan domain. TASK BUILDER must invent canonical report bytes, so the published schema/digest contract remains non-executable.

### BF9 — immutable checkout cannot preserve both routing-head and design-result identity

**Classification:** provenance/exact-SHA specification defect.

The package itself has two required identities: routing head `6d8f6b9…` and design result `15db61a…`. The common manifest provides only one `result_sha`, while P6 requires `git ls-remote` for `remote_ref` to equal `--sha` exactly and creates the worktree at that SHA. If `--sha` is the design result, the branch ref does not equal it because the routing handoff commit is later. If `--sha` is the routing head, the helper does not independently bind the distinct design-result SHA that the review is authorized to judge. Reachability is insufficient because it does not identify which ancestor is the result. The design needs distinct, explicitly related ref-head and review-result fields/checks; the implementer cannot choose which existing identity to discard.

### BF10 — rollback state machine cannot enter rollback from implementation failures

**Classification:** governance state-machine defect.

`workflow_stage_rollback_v1.json` permits entry to `SUSPENDED` only from `RELEASED`. The staged contract, however, requires rollback/fail-closed handling when implementation or implementation verification fails before release. There is no transition from `IMPLEMENTING` or `IMPLEMENTATION_VERIFIED` to `SUSPENDED` or `ROLLBACK_PROPOSED`, and no failure state for a rejected implementation. The prose says any reported defect suspends a stage, but the JSON is declared the exact state contract and cannot represent that event. Adding transitions or a distinct abandoned-implementation path is a governance choice, not a TASK BUILDER inference.

## Regression and preserved evidence

- P1 routing, P7 bounded preparation, P8 policy wording, and P9 prospective ID prohibition remain substantively sound.
- All ten baseline ambiguity choices and five Rebecca-gated material choices remain explicit and unchanged.
- CRITIC/JUDGE independence, three-layer executability, INTEGRATOR/RECORDER separation, O-14/O-15, scoring/seed fences, negative preservation, fresh-context review, public scanning, exact-SHA intent, Rebecca authority, and active-L8 isolation remain intact.
- All JSON artifacts parsed successfully; every available raw-byte sidecar matched independently; `git diff --check 184c25a..15db61a` passed.
- The scanner-definition literal remains visible as a non-clean `REBECCA_DECISION`, while actual content matches remain blockers; no silent suppression was introduced.

## Non-blocking findings

- Several semantic invariants are stronger in prose than in JSON Schema alone—for example disposition overall/row consistency and state owner-role/document-role coupling. The required validators and negative fixtures can enforce these during implementation; retain explicit tests rather than treating schema validation alone as sufficient.

## Exact next authorized role

**ARCHITECT**, through WORKFLOW COORDINATOR, for minimal remediation of BF8–BF10 only. Preserve the closed BF1, BF2, BF5, and BF6 work and all prior valid findings. Return a committed v1.2 delta to a fresh-context CRITIC.

## Explicitly prohibited actions

- No implementation, scientific change, scoring, diagnostics, seed access/exposure, rerun, active L8 interference, durable-state mutation, public flip, rollback execution, TASK BUILDER release, or merge.
- No CRITIC editing or co-authoring of design/specification/schema artifacts.

## Public-repository safety attestation

Before push, CRITIC scanned the complete new review commit and diff with gitleaks, credential/private-key/token/password, contact/PII, machine-identifier, environment-dump, protected-seed, task/session-ID, and private-path patterns, plus manual review and `git diff --check`. Zero prohibited findings were found. Repository SHAs, repository-relative paths, governance literals, and generic scanner-pattern discussion were classified as acceptable.

## Execution confirmation

No implementation, scientific modification, diagnostic/scoring execution, seed access or exposure, rerun, active L8 interaction, durable-state mutation, public flip, rollback, or unauthorized merge occurred.
