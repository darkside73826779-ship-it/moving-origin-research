# Workflow Efficiency Change Program Specification v1

**Date:** 2026-08-21

**Regime:** B

**Status:** ARCHITECT prospective design; inoperative pending fresh-context CRITIC clearance and Rebecca's approval of the exact text

**Gate served:** Rebecca-approved staged specification of proposals P1–P10; governance and role contracts only

**Base:** `d38f9069d9a4f2a92ffb3a29d6f80ef4e7253da9`

**Authority package:** `coordinator/efficiency-change-program-intake@67280dfd3ee6e00459f3f23d4d98dff637eb1760`

Unless another source tag is shown, every threshold, test criterion, precedence choice, route, schema, and STOP rule introduced here is `[PROPOSED]` and remains inoperative until Rebecca approves it.

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

## 4. Stage 2 — P2 common handoff manifest and P3 executability trace

### 4.1 Formal handoff manifest

Every formal handoff has one committed JSON manifest conforming exactly to `specs/data/common_handoff_manifest_schema_v1.json` `[PROPOSED]`. Markdown is optional and may only render/pointer to that JSON; on conflict, the validated JSON controls routing `[PROPOSED]`. All formal manifests are stored at `handoffs/manifests/<work_item_slug>/<utc_timestamp>_<sender>_to_<receiver>.json`; filenames and content contain no task/session IDs `[PROPOSED]`.

The common fields do not become evidence merely because an upstream role asserted them. Receiver checks are recorded in a new receiver-authored manifest/review; CRITIC and JUDGE independently verify within their authority `[PROPOSED]`. Schema failure, unknown fields, missing hashes, non-full SHAs, or a non-repository authority basis is STOP.

### 4.2 Structured executability trace

Every executable specification contains or points to a trace conforming to `specs/data/executability_trace_schema_v1.json` `[PROPOSED]`. Each row fixes: input ID/kind; repository path; producer/consumer; exact schema/value source; canonicalization; expected SHA-256 or explicit `not_applicable`; creation phase; status; verification IDs; and failure disposition `[PROPOSED]`.

ARCHITECT authors the trace and may mark unresolved rows only `STOP_UNRESOLVED`. CRITIC independently follows actual paths and records `VERIFIED|BLOCKED` without editing the trace. TASK BUILDER independently checks every row before implementation and stops on unresolved/mismatch `[PROPOSED]`. A checked box or upstream digest never substitutes for those independent checks.

## 5. Stage 3 — P4 state freshness and precedence

The ledger, STATE handoff, provenance custody package, and checkpoint metadata each contain exact keys: `schema_version`, `as_of_utc`, `authoritative_commit`, `supersedes`, `status`, and `document_role` `[PROPOSED]`. `status` is `current|superseded|historical`; SHAs are full lowercase hexadecimal `[PROPOSED]`.

- Ledger: current routing/ball pointer; Coordinator-owned.
- STATE.md: durable project facts; INTEGRATOR-owned; never self-authenticates.
- Provenance: append-only custody/history; RECORDER-owned.
- Checkpoint: immutable historical snapshot. New checkpoints use `state/checkpoints/<utc_timestamp>_<milestone>.md`; the legacy fixed checkpoint is marked `historical` and never overwritten `[PROPOSED]`.

Metadata does not self-authenticate. The Coordinator compares full SHAs and timestamps. A stale checkpoint is ignored for routing but retained. A factual divergence between current ledger, STATE, or provenance is STOP to Rebecca; precedence cannot mask it `[PROPOSED]`.

## 6. Stage 4 — P5 mechanical preflight and P6 immutable-SHA checkout

### 6.1 Preflight tool contract

After Rebecca approves implementation, TASK BUILDER may implement `tools/workflow_preflight.py` and tests; until then no tool exists or is authorized `[PROPOSED]`. Exact invocation:

`python tools/workflow_preflight.py --base <40-hex> --tip <40-hex> --output <repository-relative-json>` `[PROPOSED]`.

The tool is read-only except its declared output and sidecar. It verifies both commits, enumerates every introduced commit and changed path in `base..tip`, computes raw SHA-256 for every tip artifact, runs the configured secret scanner on every introduced commit/diff, applies fixed regex classes for credentials/private keys, private absolute paths, personal contact data, machine identifiers, environment dumps, PII, protected-seed content, and persistent task/session IDs, and emits a schema-valid report plus sidecar `[PROPOSED]`.

Exact mechanics are `[PROPOSED]`: introduced commits are `git rev-list --reverse <base>..<tip>`; paths are the UTF-8 byte-order-sorted union of `git diff-tree --no-commit-id --name-only -r` over every introduced commit, with duplicates removed; hashes are over raw tip Git-blob bytes from `git show <tip>:<path>`; deleted paths are listed but have no artifact hash; submodules are rejected; symlinks are hashed as their Git-blob link-target bytes and reported as symlinks. Gitleaks receives the explicit range and no credentials. Regexes come only from `specs/data/workflow_preflight_patterns_v1.json` and scan raw added/modified patch text plus new artifact bytes. Output validates against `specs/data/workflow_preflight_report_schema_v1.json`, is RFC 8785 canonical UTF-8 with no BOM, and has a sidecar of `<lowercase sha256><two spaces><basename><LF>` `[PROPOSED]`.

Exit codes are exactly: `0` clean; `2` prohibited finding; `3` scanner unavailable/error; `4` invalid SHA/range; `5` output/schema/digest failure `[PROPOSED]`. Any nonzero exit is STOP. The tool never pushes, modifies Git state, declares scientific validity, or replaces manual review. Every pushing role still scans every push; the narrower historical exemption in policy §3.1 is prospectively superseded by this stricter rule `[PROPOSED]`.

### 6.2 Immutable checkout

Every handoff supplies `remote_ref`, `base_sha`, and, when reviewing, `result_sha` `[PROPOSED]`. The receiver fetches only the named ref, verifies the fetched object contains the named full SHA, creates a new isolated detached worktree at that SHA, confirms `HEAD` equality and cleanliness, and performs work there `[PROPOSED]`. Broad branch discovery, automatic pull, shared mutable worktrees across roles, reset, and main mutation are prohibited. Failure to prove the object/ref/SHA relationship or isolate the checkout is STOP.

The mechanical helper may create/remove only a specifically named isolated worktree after validating its resolved path is outside existing worktrees and inside an approved workspace root `[PROPOSED]`. Rollback is deletion of the helper and return to manual exact-SHA isolated checkout—not return to broad branch guessing.

## 7. Stage 5 — P8 policy metadata, P9 session-ID ban, P10 JUDGE custody

### 7.1 Public-policy status

Prospective exact metadata for `PUBLIC_REPOSITORY_POLICY.md` is `[PROPOSED]`:

- `Status: Rebecca-approved and binding on all new work; substantive v1.1 requirements unchanged.`
- `Publication status: This metadata does not assert that the repository-public flip occurred; that is a separate Rebecca decision.`
- `Approval provenance: docs/rulings/provenance_log.md Entry 57 — Public-repository operating policy publication + STATE.md custody attestation.` `[OP-Entry 57]`

This corrects status only. It does not rewrite historical evidence or authorize a public flip.

### 7.2 Prospective task/session-ID ban

New public artifacts may contain stable work-item slugs, role names, repository refs, and full SHAs, but no application task/thread/session IDs, task URLs, or private local mapping identifiers `[PROPOSED]`. Historical artifacts are not rewritten absent a separate Rebecca decision. The Coordinator may keep an ephemeral, uncommitted local mapping; it is never authority, never included in a scan artifact, and is discarded at session end `[PROPOSED]`.

### 7.3 JUDGE custody/publication

JUDGE authors a ruling from raw evidence in an isolated workspace and outputs UTF-8/LF bytes plus lowercase SHA-256; JUDGE does not push or merge the ruling `[PROPOSED]`. RECORDER receives those bytes through the authorized custody channel, independently verifies the hash, performs public-safety scanning without editing content, commits the bytes unchanged under `docs/rulings/` on a `recorder/` branch, appends custody provenance, and pushes `[PROPOSED]`.

The ruling becomes durable evidence only when the RECORDER commit is pushed and the byte hash matches JUDGE's handoff. It becomes an operative gate only when Rebecca rules on it; RECORDER publication is custody, not approval `[PROPOSED]`. If scanning blocks publication, hash/bytes differ, or RECORDER cannot publish, status is `UNPUBLISHED_JUDGE_RULING` and the chain stops at Rebecca. RECORDER may never edit, summarize-as-substitute, or improve the ruling.

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

## 10. STOP list and Rebecca decisions

The design is complete enough for independent review, but these material choices remain inoperative until Rebecca expressly accepts them `[PROPOSED]`:

1. Default post-build route is TASK BUILDER → CRITIC → Rebecca, with INTEGRATOR/RECORDER only for declared state/custody events.
2. Concurrent preparation is allowed only for immutable, disjoint, non-dependent, non-scoring work; ball ownership remains singular.
3. Checkpoints become immutable historical files under `state/checkpoints/`; the legacy fixed file is marked historical.
4. Public policy is described as approved/binding on new work without asserting the repository-public flip.
5. JUDGE does not push; RECORDER publishes exact bytes, and Rebecca alone activates the ruling.

Any CRITIC BLOCK, conflicting authority SHA, missing executable schema input, policy/public-status uncertainty beyond the exact neutral wording, scoring/seed boundary, or requested main merge is STOP to Rebecca.

## 11. Prohibitions

No implementation, scientific specification/bar/control change, scoring, diagnostics, seed access, rerun, L8 GPU interference, STATE/provenance/ledger edit by ARCHITECT, public flip, or merge is authorized. EFFICIENCY EVALUATOR remains proposal/audit-only. TASK BUILDER remains held until the exact applicable stage clears CRITIC and Rebecca.
