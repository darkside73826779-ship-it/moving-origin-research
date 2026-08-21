# Workflow Efficiency Change Program Specification v1

**Date:** 2026-08-21

**Regime:** B

**Status:** Rebecca-approved cumulative Stages 1–5; mechanical implementation authorized 2026-08-21 under the Coordinator-owned reconciliation ruling

**Gate served:** Rebecca-approved staged specification of proposals P1–P10; governance and role contracts only

**Base:** `d38f9069d9a4f2a92ffb3a29d6f80ef4e7253da9`

**Authority package:** `coordinator/efficiency-change-program-intake@67280dfd3ee6e00459f3f23d4d98dff637eb1760`

**Implementation authority:** `handoffs/REBECCA_WORKFLOW_EFFICIENCY_P1_P10_IMPLEMENTATION_AND_COORDINATOR_ROLE_INIT_AUTHORIZATION_2026-08-21.md` at `8923112fde4ce95a6dad03f6c71f5235eeccc7e5`.

Unless another source tag is shown, `[PROPOSED]` records the design's original source class. Rebecca approved the complete P1–P10 program for mechanical implementation on 2026-08-21; that approval does not convert governance mechanisms into scientific bars or authorize scoring, seed access, or scientific changes.

## 1. Constitutional compliance

The binding Versioned-Law Compliance Protocol is quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1:

> - **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
> - **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
> - **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.
> - **P4 — Regime dating.** Every new artifact states its date and regime in its header. Acts are judged only against their own regime's text; later text is never applied backward.
> - **P5 — Deviation memorialization.** Any deviation from `[LAW]` text — however sensible, however disclosed — is inoperative for scoring until Rebecca has signed a waiver or amendment recorded in the v2 amendment log. Disclosure in a spec is necessary but not sufficient.
> - **P6 — Provenance citation check.** Any claim of the form "Entry n said X" must be verified against the entry's actual text before commit.

Nothing in this program changes constitutional law, a scientific bar/control, O-14/O-15, seed custody, negative labels, the three-layer executability defense, fresh-context review, or Rebecca's sole gate/merge authority.

## 2. Source and precedence map

For governance decisions, descending authority is `[PROPOSED]`:

1. Rebecca's committed signed ruling for the exact work item.
2. Constitutional law and §5.
3. Rebecca-approved scientific/governance specifications applicable to that work item.
4. The approved canonical routing table.
5. Role initialization contracts.
6. Current routing ledger for ball location only.
7. `STATE.md` for durable project facts only.
8. Provenance log for custody/history only.
9. Historical checkpoints as non-authoritative snapshots.

Precedence selects which document owns a field; it never silently resolves contradictory facts. Any contradiction involving a SHA, gate, scoring/seed boundary, role independence, or current ball owner is a STOP to WORKFLOW COORDINATOR and Rebecca `[PROPOSED]`.

The normative source/file mapping is in `specs/workflow_efficiency_source_precedence_map_v1.md` `[PROPOSED]`.

## 3. Stage 1 — P1 canonical routing and P7 safe batching/parallelism

`specs/data/workflow_routing_table_v1.json` is the sole default-route table after approval `[PROPOSED]`.

### 3.1 Default routes

- Governance/scientific specification: `ARCHITECT → fresh-context CRITIC → Rebecca` `[PROPOSED]`.
- Mechanical implementation: `TASK BUILDER → fresh-context CRITIC → Rebecca` `[PROPOSED]`. INTEGRATOR and RECORDER do not intervene unless the approved task route declares a state or custody event.
- State event: `INTEGRATOR → RECORDER → Rebecca` `[PROPOSED]`.
- Scoring: `Rebecca/executor → RECORDER intake custody → JUDGE → RECORDER byte-for-byte publication → Rebecca` `[PROPOSED]`.
- CRITIC BLOCK returns only to the artifact's originating role; gate ownership never transfers to TASK BUILDER `[PROPOSED]`.

A task-specific route overrides a default only when a committed Rebecca-signed ruling supplies the full ruling SHA, exact ordered route, and explicit scope `[PROPOSED]`. An override may add gates but may not omit fresh-context review, required scoring custody/JUDGE independence, INTEGRATOR/RECORDER ownership, or Rebecca's final gate `[PROPOSED]`. Conflict or missing full SHA is STOP.

### 3.2 Single-ball and consultations

Exactly one role owns each work item. Ownership transfers only through a labeled `FORMAL HANDOFF`; a `CONSULTATION REQUEST` never transfers ownership `[PROPOSED]`. Every formal pass is reported to the Coordinator with gate/work item, sender/receiver roles, remote ref/full SHA, artifact path, blockers, and next event `[PROPOSED]`.

Concurrent **preparation** is permitted only when all conditions hold: inputs are the same immutable SHAs; outputs are disjoint; neither task consumes the other's output; neither role judges/reviews its own work; no scoring/protected seed is involved; and the route declares a deterministic commit/custody order `[PROPOSED]`. Dependency-bound work is serial. INTEGRATOR output and RECORDER attestation are always serial. A failed condition is STOP and reversion to serial.

Batching may combine multiple already-authorized, low-risk state/custody events into one INTEGRATOR commit followed by one RECORDER attestation, but every constituent event and resulting STATE hash remains listed separately `[PROPOSED]`. Batching never combines scientific gates or hides negative events.

### 3.3 Stage 1 executable validation package

Stage 1 is implemented only from the exact edit boundaries in `specs/workflow_role_contract_amendments_v1.md` plus `specs/data/workflow_stage1_validator_contract_v1.json`, `specs/data/workflow_stage1_route_case_schema_v1.json`, and `specs/data/workflow_stage1_routing_fixtures_v1.json` `[PROPOSED]`. The contract fixes parsing, unknown-field rejection, route lookup/override validation, all six P7 predicates, batching eligibility, reason precedence, canonical output, fixture order, and expected SHA-256 values. TASK BUILDER may translate the prescribed algorithm mechanically but may not invent a route, reason, predicate, edit locus, fixture, or expected output. Stages 2–5 files and role text are forbidden Stage 1 outputs.

## 4. Stage 2 — P2 common handoff manifest and P3 executability trace

### 4.1 Formal handoff manifest

Every formal handoff has one committed JSON manifest conforming exactly to `specs/data/common_handoff_manifest_schema_v1.json` `[PROPOSED]`. Markdown is optional and may only render/pointer to that JSON; on conflict, the validated JSON controls routing `[PROPOSED]`. All formal manifests are stored at `handoffs/manifests/<work_item_slug>/<utc_timestamp>_<sender>_to_<receiver>.json`; filenames and content contain no task/session IDs `[PROPOSED]`. The sole transport exception is JUDGE→RECORDER: its JUDGE manifest/envelope is transmitted privately because the ruling is not yet repository-custodied; RECORDER commits a receiver-authored custody manifest and exact ruling bytes together, restoring repository durability `[PROPOSED]`.

The manifest's `artifacts` object is the complete artifact inventory: every artifact named anywhere in the manifest or its role extension appears exactly once as a repository-relative forward-slash path key with its raw-byte SHA-256 value; no unlisted handoff artifact, duplicate normalized path, absolute path, backslash, `..`, or missing/null digest is permitted `[PROPOSED]`. `sender_role` conditionally binds `role_extension` to that sender's one exact extension schema; a mismatched extension is invalid. The common fields do not become evidence merely because an upstream role asserted them. Receiver checks are recorded in a new receiver-authored manifest/review; CRITIC and JUDGE independently verify within their authority `[PROPOSED]`. Schema failure, unknown fields, incomplete/non-unique artifact inventory, non-full SHAs, or a non-repository authority basis is STOP.

### 4.2 Structured executability trace

Every executable specification contains or points to a trace conforming to `specs/data/executability_trace_schema_v1.json` `[PROPOSED]`. Each row fixes: input ID/kind; repository path; producer/consumer; exact schema/value source; canonicalization; expected SHA-256 or explicit `not_applicable`; creation phase; status; verification IDs; and failure disposition `[PROPOSED]`.

ARCHITECT authors the trace and may mark unresolved rows only `STOP_UNRESOLVED`. The source trace is RFC 8785 canonical UTF-8 without BOM with a raw-digest sidecar. Its row order is binding; `input_id` values are unique. A row digest is SHA-256 of that row alone serialized by RFC 8785 `[PROPOSED]`.

CRITIC and TASK BUILDER each author a separate artifact conforming to `specs/data/executability_trace_disposition_schema_v1.json`; neither may edit, reorder, or replace the ARCHITECT trace `[PROPOSED]`. CRITIC stores its file at `reviews/executability/<work_item_slug>_critic_disposition.json`; TASK BUILDER stores its pre-build file at `diagnostics/executability/<work_item_slug>_taskbuilder_disposition.json`. Each disposition binds the raw source-trace digest and source specification commit, contains exactly one row for every source row in identical order, repeats the same `input_id`, supplies the RFC-8785 row digest, and uses that reviewer's verification ID from the source row. Missing, extra, duplicate, reordered, or mismatched rows are invalid `[PROPOSED]`.

CRITIC independently follows actual paths and records `VERIFIED|BLOCKED`. TASK BUILDER independently checks every row only after Rebecca releases implementation and before making implementation changes. `overall_disposition=VERIFIED` is permitted only when every row is `VERIFIED`; any blocked row requires `overall_disposition=BLOCKED` and STOP/return under the canonical route `[PROPOSED]`. A checked box, upstream digest, or the other receiver's disposition never substitutes for independent checks.

## 5. Stage 3 — P4 state freshness and precedence

The ledger, STATE, provenance, and every checkpoint each receive an owner-authored adjacent `.metadata.json` conforming to `specs/data/workflow_state_metadata_schema_v1.json` `[PROPOSED]`. Exact paths are `state/COORDINATOR_LEDGER.metadata.json`, `state/STATE.metadata.json`, `docs/rulings/provenance_log.metadata.json`, and `<checkpoint-path>.metadata.json`. Metadata is RFC 8785 canonical UTF-8 without BOM plus a raw SHA-256 sidecar. `source_commit` is the full input commit whose document content is described—not the commit containing metadata—so no self-reference occurs. `document_sha256` hashes the target's raw committed LF bytes. Empty supersession is exactly `[]`; otherwise `supersedes_metadata_sha256` lists earlier metadata raw digests in lexicographic order `[PROPOSED]`.

- Ledger: current routing/ball pointer; Coordinator-owned.
- STATE.md: durable project facts; INTEGRATOR-owned; never self-authenticates.
- Provenance: append-only custody/history; RECORDER-owned.
- Checkpoint: immutable historical snapshot. New checkpoints use `state/checkpoints/<YYYYMMDDTHHMMSSZ>_<lowercase-milestone-slug>.md`; their adjacent metadata has `document_role=checkpoint`. The legacy fixed checkpoint is marked `historical` and never overwritten `[PROPOSED]`.

Metadata does not self-authenticate. RECORDER attests STATE metadata/document hashes; each owning role signs its handoff manifest. The Coordinator compares source SHAs, document hashes, statuses, and UTC timestamps. A stale checkpoint is ignored for routing but retained. A factual divergence between current ledger, STATE, or provenance is STOP to Rebecca; precedence cannot mask it `[PROPOSED]`.

## 6. Stage 4 — P5 mechanical preflight and P6 immutable-SHA checkout

### 6.1 Preflight tool contract

After Rebecca approves implementation, TASK BUILDER may implement `tools/workflow_preflight.py` and tests; until then no tool exists or is authorized `[PROPOSED]`. Exact invocation:

`python tools/workflow_preflight.py --base <40-hex> --tip <40-hex> --output <repository-relative-json>` `[PROPOSED]`.

The tool is read-only except its declared output and sidecar. It verifies both commits, enumerates every introduced commit and changed path in `base..tip`, computes raw SHA-256 for every tip artifact, runs the configured secret scanner on every introduced commit/diff, applies fixed regex classes for credentials/private keys, private absolute paths, personal contact data, machine identifiers, environment dumps, PII, protected-seed content, and persistent task/session IDs, and emits a schema-valid report plus sidecar `[PROPOSED]`.

Exact mechanics are `[PROPOSED]`: `git merge-base --is-ancestor <base> <tip>` must succeed; equality and non-ancestor ranges are rejected. Introduced commits are `git rev-list --reverse --topo-order <base>..<tip>`. For each introduced commit, parents retain commit-object order. Each commit/parent domain ID is `C:<commit>:P:<parent>`; after those domains, the combined domain is `R:<base>:<tip>`. Root commits are outside a valid non-equal ancestor range. Every domain uses `git diff-tree -r --raw -z --no-commit-id --find-renames=100% <old> <new>`; status `A|M|D|R100|T` maps exactly to `added|modified|deleted|renamed|type_changed`, and any other status is exit `5` `[PROPOSED]`.

`path_events` retains every domain event rather than collapsing history. Domains follow the order above; within a domain, events sort by new/path UTF-8 bytes, then old-path UTF-8 bytes with null first, then change type. `event_index` is one-based over that order. `old_path` is non-null only for `renamed`; `path` is the new path for rename and the affected path otherwise. `object_type` and `sha256` describe the domain's new object; deletions are `deleted/null`. Submodules are rejected; symlinks hash link-target blob bytes. Thus add→modify emits two events, add→delete emits two events even though absent at both endpoints, rename→modify emits both events, and type-change→delete emits both `[PROPOSED]`.

`paths` is a separate endpoint projection produced **only** from the combined domain using the same mapping and order, one row per combined event; an add→delete absent at both endpoints has no `paths` row but remains in `path_events`. Exact renames are detected only at `100%`; otherwise Git's exact command result controls as add/delete. No cross-domain event reduction or precedence is permitted `[PROPOSED]`.

Gitleaks and fixed regexes scan every domain independently; the combined domain is not assigned a synthetic commit SHA. Regexes come only from `specs/data/workflow_preflight_patterns_v1.json` and scan raw added/modified patch text plus new artifact bytes. A raw match identity is `(detector,class,path,line,column,evidence_sha256,context_kind,disposition,rationale_code)`; null path/line/column are literal nulls. Identical identities across domains reduce to one finding whose `scan_domain_ids` is the UTF-8-byte-sorted unique domain-ID list; any differing identity remains separate. Findings sort by path UTF-8 bytes (null last), line (null last), column (null last), detector, class, evidence digest, context, disposition, rationale, then joined domain IDs; IDs are assigned `F000001` upward. `secret_scanner.finding_count` equals the number of emitted deduplicated findings whose detector is `gitleaks`, not raw domain matches `[PROPOSED]`. Every content match is `BLOCKER`. A match whose entire evidence span lies inside the JSON string value of its own fixed scanner definition is retained as `SCANNER_DEFINITION_LITERAL/REBECCA_DECISION`; it is never suppressed or CLEAN, and a test proves a real private path elsewhere remains `BLOCKER` `[PROPOSED]`. Output validates against `specs/data/workflow_preflight_report_schema_v2.json` (v1 is preserved but superseded), is RFC 8785 canonical UTF-8 without BOM followed by exactly one LF, and has a sidecar of `<lowercase raw-file sha256><two spaces><basename><LF>` `[PROPOSED]`.

Exit codes are exactly: `0` clean; `2` prohibited finding; `3` scanner unavailable/error; `4` invalid SHA/range; `5` output/schema/digest failure `[PROPOSED]`. Any nonzero exit is STOP. The tool never pushes, modifies Git state, declares scientific validity, or replaces manual review. Every pushing role still scans every push; the narrower historical exemption in policy §3.1 is prospectively superseded by this stricter rule `[PROPOSED]`.

### 6.2 Immutable checkout

Every handoff supplies distinct `remote_ref`, `routing_ref_sha`, `review_result_sha`, `base_sha`, and `work_branch` `[PROPOSED]`. `routing_ref_sha` is the exact current head used to route the package; `review_result_sha` is the exact commit whose substantive result is under review, or null only for an intake with no produced result. Neither identity substitutes for the other. The approved workspace root is a mandatory local CLI argument whose resolved directory contains a file `.mor-workspace-root` with exact UTF-8/ASCII bytes `moving-origin-research-workspace-v1\n`; Rebecca or the workstation owner creates that marker outside Git, and neither its absolute path nor a receipt containing it may be committed `[PROPOSED]`. Missing marker/root is STOP.

Exact create invocation is `python tools/workflow_checkout.py create --repo <absolute-existing-clone> --remote origin --ref <refs/heads/name> --ref-head <routing_ref_sha> --review-result <review_result_sha-or-none> --base <40-hex> --work-branch <role/name> --workspace-root <absolute-marked-root> --work-item <slug>` `[PROPOSED]`. `git ls-remote --refs <remote> <ref>` must return exactly one row whose object ID equals `--ref-head`. The helper fetches exactly `<ref>` into private ref `refs/mor/intake/<ref-head>`, requires equality, and verifies `base==review-result` or `base` is an ancestor of `review-result`; `review-result` must equal or be an ancestor of `ref-head`. When distinct, every commit in `review-result..ref-head` must change only `handoffs/` paths; any other change is STOP. The receiver reviews substantive artifacts from `review-result` and routing/handoff artifacts from `ref-head`, recording both SHAs `[PROPOSED]`.

The helper rejects existing local/remote `work_branch` and creates detached path `<root>/mor-<work-item>-<first12-ref-head>` at `ref-head` using `git worktree add --detach`. It verifies resolved path is a strict child of the marked root, is not equal/nested with any existing worktree, `HEAD==ref-head`, `git cat-file -e <review-result>^{commit}` when non-null, and worktree cleanliness; only then it creates the declared role branch at `ref-head` `[PROPOSED]`. Collision, ambiguity, mismatch, dirty state, or command failure is STOP; no reuse, suffixing, force, reset, or cleanup guessing.

The helper writes a local canonical receipt inside the marked root, not the repository, containing resolved repo/root/worktree paths, remote ref, `routing_ref_sha`, nullable `review_result_sha`, base SHA, branch, creation UTC time, and its own SHA-256 `[PROPOSED]`. Exact cleanup invocation is `python tools/workflow_checkout.py cleanup --receipt <absolute-receipt>` `[PROPOSED]`. Cleanup verifies receipt digest, marker, strict-child relation, exact registered worktree path, `HEAD==routing_ref_sha`, review-result ancestry when non-null, clean index/worktree, and no nested registered worktree; it then runs `git worktree remove <exact-path>` without `--force` and deletes only the receipt. Any failed check is STOP for manual Rebecca/workstation-owner resolution. Rollback removes the helper through the governed state machine and returns to the same manual exact-ref/exact-SHA isolated procedure—not broad branch guessing.

## 7. Stage 5 — P8 policy metadata, P9 session-ID ban, P10 JUDGE custody

### 7.1 Public-policy status

Approved exact metadata for `PUBLIC_REPOSITORY_POLICY.md`, retaining its original source-class annotation, is:

- `Status: Rebecca-approved and binding on all new work; substantive v1.1 requirements unchanged.`
- `Publication status: This metadata does not assert that the repository-public flip occurred; that is a separate Rebecca decision.`
- `Approval provenance: docs/rulings/provenance_log.md Entry 57 — Public-repository operating policy publication + STATE.md custody attestation.` `[OP-Entry 57]`

This corrects status only. It does not rewrite historical evidence or authorize a public flip.

### 7.2 Approved task/thread/session-ID ban

New public artifacts may contain stable work-item slugs, role names, repository refs, and full SHAs, but no application task/thread/session IDs, task URLs, or private local mapping identifiers `[PROPOSED]`. Historical artifacts are not rewritten absent a separate Rebecca decision. The Coordinator may keep an ephemeral, uncommitted local mapping; it is never authority, never included in a scan artifact, and is discarded at session end `[PROPOSED]`.

### 7.3 JUDGE custody/publication

JUDGE authors a ruling from raw evidence in an isolated workspace and produces strict UTF-8 without BOM, LF-only line endings, exactly one final LF, maximum `4,194,304` bytes `[PROPOSED]`, and lowercase SHA-256. JUDGE builds the exact `judgeEnvelope` object defined in the common manifest schema: standard RFC 4648 base64, padding required when applicable, no whitespace, filename/media type/encoding/byte length/digest/content. The envelope is RFC 8785 canonical JSON and is delivered in one labeled `FORMAL HANDOFF — JUDGE → RECORDER` through the Coordinator's existing controlled collaboration transport; the Coordinator forwards the exact envelope bytes and records only its SHA-256, never content or a task/session identifier `[PROPOSED]`. The envelope is evidence transport, not binding non-repo authority; the approved repository contract defines its meaning.

RECORDER hashes received canonical envelope bytes, parses with duplicate/unknown-field rejection, base64-decodes strictly, re-encodes and requires exact base64 equality, checks maximum size/declared length/SHA-256, decodes UTF-8 strictly, rejects BOM/CR/missing-or-multiple terminal LF, and requires the filename to be unused on the target branch `[PROPOSED]`. RECORDER then scans without editing, commits the decoded bytes unchanged under `docs/rulings/` plus a receiver-authored custody manifest that records envelope SHA-256 and ruling SHA-256, appends custody provenance, and pushes `[PROPOSED]`.

The ruling becomes durable evidence only when the RECORDER commit is pushed and the byte hash matches JUDGE's envelope. It becomes an operative gate only when Rebecca rules on it; RECORDER publication is custody, not approval `[PROPOSED]`. If transfer is interrupted before verified commit, the same canonical envelope may be delivered again: RECORDER treats equal envelope/ruling digests idempotently and never requests regenerated scoring or changed bytes. If local commit exists but push confirmation failed, RECORDER first checks the remote ref; equal commit/digests complete custody, absent commit permits push of the same commit, and any mismatch is STOP. Scanning block, validation mismatch, unavailable transport/publication, or differing duplicate yields `UNPUBLISHED_JUDGE_RULING` and stops at Rebecca. RECORDER may never edit, summarize-as-substitute, or improve the ruling `[PROPOSED]`.

## 8. Exact role ownership and mechanical implementer boundary

After CRITIC CLEAR and Rebecca approval `[PROPOSED]`:

- TASK BUILDER performs only exact approved mechanical edits to role initialization files, schemas, templates, and tooling/tests.
- WORKFLOW COORDINATOR alone edits the ledger and routing pointer.
- INTEGRATOR alone edits STATE.md.
- RECORDER alone edits provenance and publishes JUDGE bytes.
- ARCHITECT alone revises this specification if implementation reveals an undefined rule.
- CRITIC independently reviews implementation; JUDGE never reviews or implements governance tooling.

Any requested edit crossing those ownership boundaries is STOP and returns to the Coordinator.

## 9. Incremental rollout, verification, and rollback

Each stage is separately gated and may not depend on an unapproved later stage `[PROPOSED]`:

1. P1/P7: install routing table and Coordinator references; dry-route synthetic non-scoring, state, scoring, BLOCK, and override cases. Rollback: revert stage commit; strict serial legacy routes resume.
2. P2/P3: install schemas/templates; validate one synthetic manifest per role and executable traces with complete/unresolved/mismatch cases. Rollback: revert stage; legacy Markdown remains readable and three defenses remain.
3. P4: add metadata and mark legacy checkpoint historical. Verify stale/conflict/current cases. Rollback: revert metadata commit; never delete history.
4. P5/P6: implement/test helper in a sandbox with clean, finding, scanner-error, invalid-range, isolated-checkout, and collision cases. Rollback: disable helper; manual full-scope scan and exact-SHA isolation remain mandatory.
5. P8/P9/P10: apply metadata, templates, and custody contract; test task-ID rejection and byte mismatch/publication failure. Rollback: revert prospective text; historical policy/rulings remain.

Every stage requires fresh-context CRITIC implementation review and Rebecca release before use. Failure rolls back only that stage and any later dependent stages; earlier cleared stages remain if dependency analysis shows no effect `[PROPOSED]`.

### 9.1 Rollback authority and state machine

`specs/data/workflow_stage_rollback_v1.json` is the exact dependency/state contract `[PROPOSED]`. Dependencies are a strict chain `S1→S2→S3→S4→S5`; rolling back a stage automatically includes every transitive descendant, never an ancestor `[PROPOSED]`. ARCHITECT produces the impact set from that graph; fresh-context CRITIC independently verifies it; Rebecca alone decides whether rollback occurs, authorizes exact inverse commits/owner edits, and later accepts the verified result `[PROPOSED]`. No role may infer that an earlier stage is unaffected outside this graph or self-authorize a rollback.

Any role may report a defect. Coordinator immediately marks the affected stage and descendants `SUSPENDED` for routing/use (without rewriting evidence) and routes to ARCHITECT `[PROPOSED]`. This transition applies from `RELEASED`; from `IMPLEMENTING` upon implementation failure or CRITIC BLOCK; and from `IMPLEMENTATION_VERIFIED` upon a pre-release defect or Rebecca's decision not to release. No failed or non-released implementation may return directly to `REBECCA_APPROVED`, `IMPLEMENTING`, or `RELEASED` `[PROPOSED]`. ARCHITECT authors a rollback proposal naming target stage, cascade set, exact released or unreleased implementation commits, inverse changes, retained evidence, owners, verification, and recovery. CRITIC CLEAR is required; BLOCK returns to ARCHITECT. Rebecca's `ROLLBACK_AUTHORIZED` ruling names exact commits and executors `[PROPOSED]`.

TASK BUILDER applies exact inverse commits only to mechanical tooling/templates. Coordinator, INTEGRATOR, and RECORDER alone apply authorized inverse changes to ledger, STATE, and provenance-owned surfaces respectively; provenance is never deleted or rewritten, only appended with rollback custody `[PROPOSED]`. A fresh-context CRITIC verifies byte/diff/state results. Rebecca alone merges/releases `ROLLED_BACK`. Reset, force push, history deletion, evidence deletion, automatic rollback, and reuse of a suspended stage are prohibited. Any rollback failure stays `SUSPENDED/ROLLING_BACK`, stops descendants, preserves partial commits as evidence, and returns to Rebecca `[PROPOSED]`.

## 10. STOP list and Rebecca decisions

Rebecca expressly accepted these material choices for mechanical implementation on 2026-08-21; they remain subject to the owner, verification, rollback, scientific, scoring, seed, and merge fences in this specification:

1. Default post-build route is TASK BUILDER → CRITIC → Rebecca, with INTEGRATOR/RECORDER only for declared state/custody events.
2. Concurrent preparation is allowed only for immutable, disjoint, non-dependent, non-scoring work; ball ownership remains singular.
3. Checkpoints become immutable historical files under `state/checkpoints/`; the legacy fixed file is marked historical.
4. Public policy is described as approved/binding on new work without asserting the repository-public flip.
5. JUDGE does not push; RECORDER publishes exact bytes, and Rebecca alone activates the ruling.

Any CRITIC BLOCK, conflicting authority SHA, missing executable schema input, policy/public-status uncertainty beyond the exact neutral wording, scoring/seed boundary, or requested main merge is STOP to Rebecca.

## 11. Prohibitions

Mechanical implementation of approved P1–P10 workflow contracts, schemas, validators, role initializations, policy metadata, and local checkout/preflight tooling is authorized under Rebecca's 2026-08-21 Coordinator-owned reconciliation ruling. This does not authorize scientific specification/bar/control changes, scoring, diagnostics, seed access, rerun, L8/M4 interference, owner-bound STATE/provenance/ledger edits by another role, public-repository visibility changes, or merge. EFFICIENCY EVALUATOR remains proposal/audit-only. Owner-specific runtime events still require their canonical route and Rebecca retains every merge/gate decision.
