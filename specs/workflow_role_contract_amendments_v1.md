# Prospective Role-Contract Amendments — Workflow Efficiency v1

**Date:** 2026-08-21

**Regime:** B

**Status:** Exact mechanical edit specification `[PROPOSED]`; do not apply before CRITIC CLEAR and Rebecca approval

## Stage 1 controlling scope — P1/P7 only

For the Stage 1 release, this section is the complete mechanical edit set and supersedes every later-stage instruction below until its stage is separately released. TASK BUILDER changes only the following loci; byte ranges outside the named insertions/replacements are immutable.

### All seven role initialization files

Insert immediately before each file's `## Standing constraints` heading (or append immediately before the final initialization-complete sentence when that heading is absent):

> ## Stage 1 canonical routing and safe preparation
>
> Default routes and P1/P7 decisions are validated against `specs/data/workflow_routing_table_v1.json` using the exact contract and fixtures in `specs/data/workflow_stage1_validator_contract_v1.json` and `specs/data/workflow_stage1_routing_fixtures_v1.json`. Exactly one role owns each work item. Ownership transfers only through a labeled FORMAL HANDOFF acknowledged by the recipient; consultation never transfers ownership. A committed Rebecca-signed full-SHA task route may add gates but may not remove mandatory independence, custody, owner-only state/provenance boundaries, or Rebecca's final gate. Missing or conflicting authority is STOP to WORKFLOW COORDINATOR.
>
> Concurrent preparation is allowed only for identical immutable inputs, disjoint outputs, no output dependency, no self-review, no scoring or protected seeds, and a declared deterministic serial commit/custody order. Failure of any condition reverts to serial and is STOP. Dependency gates, scoring custody, and INTEGRATOR-to-RECORDER attestation are always serial. Only already-authorized low-risk state/custody events may batch; every event and resulting STATE hash remains separately listed.

No Stage 1 edit mentions or activates common handoff manifests, executability traces, freshness metadata, preflight/checkout helpers, public-policy metadata, session-ID scanning, or JUDGE custody. Those are Stages 2–5 and remain held.

### `WORKFLOW_COORDINATOR_INITIALIZATION.md`

Replace only the existing `## Routing protocol` section, from that heading up to but excluding the next same-level `##` heading, with:

> ## Routing protocol
>
> `specs/data/workflow_routing_table_v1.json` is the canonical default table. Defaults are specification `ARCHITECT → FRESH_CONTEXT_CRITIC → REBECCA`, mechanical implementation `TASK_BUILDER → FRESH_CONTEXT_CRITIC → REBECCA`, state event `INTEGRATOR → RECORDER → REBECCA`, and scoring `REBECCA_EXECUTOR → RECORDER_INTAKE → JUDGE → RECORDER_PUBLICATION → REBECCA`. CRITIC BLOCK returns only to the originating role. Task-specific overrides require a repository-committed Rebecca-signed ruling path, full 40-hex SHA, exact ordered route, and scope; they may add but never remove mandatory gates.
>
> Exactly one role owns a work item. Concurrent preparation and batching use the Stage 1 universal contract and fail closed through the committed validator fixtures. Every formal pass reports work item/gate, sender, intended receiver, remote ref/full SHA, artifact path, blockers/holds, and next event to WORKFLOW COORDINATOR. Consultation is non-transferring.

Replace only the existing `## Subagent economy` section, from that heading up to but excluding the next same-level `##` heading, with:

> ## Safe preparation and batching
>
> Batch only already-authorized low-risk state/custody events. Every INTEGRATOR STATE commit routes serially to RECORDER for hash attestation. Independent preparation may run concurrently only when all six committed P7 predicates pass; ownership remains singular and outputs disjoint. Scientific gates, dependencies, scoring, protected seeds, and review of one's own output are never batched or parallelized.

The fresh-startup and checkpoint paragraphs are not edited in Stage 1; they belong to held Stage 3.

### `state/role_initialization/INTEGRATOR_INITIALIZATION.md`

Within the existing `## When you receive a handoff` section, replace the exact committed byte line (excluding its terminating LF):

> `6. Return a handoff with the STATE.md SHA-256.`

with these exact two LF-separated lines:

> `6. Return a handoff with the STATE.md SHA-256.`
> `7. Route every committed STATE.md update serially to RECORDER for hash attestation before any dependent event. Multiple already-authorized low-risk state events may share one commit only when each event and resulting STATE hash is separately enumerated. INTEGRATOR is not a mandatory post-build hop unless the approved route declares a state event.`

The replacement begins at the ASCII `6` of the existing line and ends immediately before that line's LF. Exactly one match is required; zero or multiple matches is STOP. Do not alter the adjacent `## Handoff format` section.

Do not add state metadata text; it belongs to held Stage 3.

### `state/role_initialization/RECORDER_INITIALIZATION.md`

Within the existing `## Rules` section, replace the exact committed byte line (excluding its terminating LF):

> `- Attest STATE.md hash after every INTEGRATOR update. If divergence between provenance log and STATE.md is detected, escalate to Rebecca immediately.`

with this exact line:

> `- Attest every INTEGRATOR STATE.md update serially before any dependent event. For an approved batch, verify and enumerate every constituent event and the resulting STATE hash separately; missing, dependent, scientific, scoring, or protected-seed events are STOP. If divergence between provenance log and STATE.md is detected, escalate to Rebecca immediately.`

The replacement begins at the leading hyphen and ends immediately before that line's LF. Exactly one match is required; zero or multiple matches is STOP. Do not create a custody heading or alter any other `## Rules` bullet.

Do not add JUDGE-publication or provenance-metadata text; those belong to held Stages 5 and 3 respectively. No other role-specific replacement below is part of Stage 1.

## Universal insertion — all seven role initializations

Insert before `## Standing constraints`:

> ## Canonical workflow contracts
>
> Formal routing follows `specs/data/workflow_routing_table_v1.json`. A task-specific route overrides a default only through a full-SHA, repository-committed Rebecca-signed ruling and may not remove mandatory independence, custody, or Rebecca gates. Ownership transfers only through a labeled FORMAL HANDOFF. CONSULTATION REQUEST does not transfer ownership.
>
> Every formal handoff uses `specs/data/common_handoff_manifest_schema_v1.json`. The receiver independently verifies all fields within its authority; an upstream assertion is not evidence merely because it validates. The sole pre-custody exception is the schema-valid private JUDGE→RECORDER envelope; RECORDER restores durability by committing a receiver-authored custody manifest with the exact ruling. New public artifacts must not contain application task/thread/session IDs or task URLs.
>
> Every push is scanned over the complete introduced `base..tip` range plus manual review. No role relies on the former narrow scan exemption. Tool output collects evidence and never replaces judgment.
>
> Every checkout uses the handoff's distinct exact remote-ref head SHA and review/design-result SHA in an isolated detached worktree. Verify remote-ref equality to the routing head, result ancestry/equality, handoff-only post-result commits, both commit objects, and clean isolation. Never discard or conflate either identity; failure is STOP.

## `WORKFLOW_COORDINATOR_INITIALIZATION.md`

Replace the entire `## Routing protocol` section with:

> ## Routing protocol
>
> `specs/data/workflow_routing_table_v1.json` is the canonical default table. Defaults are: specification `ARCHITECT → fresh-context CRITIC → Rebecca`; mechanical implementation `TASK BUILDER → fresh-context CRITIC → Rebecca`; state event `INTEGRATOR → RECORDER → Rebecca`; scoring `Rebecca/executor → RECORDER → JUDGE → RECORDER → Rebecca`. A CRITIC BLOCK returns only to the originating role.
>
> Exactly one role owns a work item. Concurrent preparation is permitted only for same immutable inputs, disjoint outputs, no dependency, no self-review, no scoring/protected seeds, and a declared serial commit/custody order. INTEGRATOR output and RECORDER attestation are always serial. Failure of any condition reverts to serial and is STOP until routing is corrected.
>
> Every formal ball-pass is recorded with work item/gate, sender/receiver roles, remote ref/full SHA, artifact manifest path, blockers, and next event. Local task/session mappings are ephemeral, uncommitted, non-authoritative, and discarded at session end.

Replace the `Fresh coordinator startup` paragraph and numbered startup protocol with:

> **Fresh coordinator startup:** Read current ledger routing metadata first, STATE.md durable facts second, provenance tail custody/history third, and only the ledger-pointed immutable checkpoint fourth. Checkpoints are historical snapshots and never override current routing. Any factual divergence is STOP to Rebecca; precedence must not mask it.

Replace `## Subagent economy` with:

> ## Safe preparation and batching
>
> Batch only already-authorized low-risk state/custody events. Every INTEGRATOR STATE commit is followed serially by RECORDER hash attestation. Independent preparation may run concurrently only under the canonical routing contract; ownership remains singular and outputs remain disjoint. Scientific gates, review dependencies, scoring, and protected-seed work are never batched or parallelized.

Replace the checkpoint paragraph with:

> At each clean milestone, create an immutable checkpoint under `state/checkpoints/<utc_timestamp>_<milestone>.md` with canonical freshness metadata. Record its path in the ledger. Never overwrite a checkpoint. Mark the legacy `state/COORDINATOR_HANDOFF_CHECKPOINT.md` historical through the separately approved mechanical edit.

## `ARCHITECT_INITIALIZATION.md`

Append to `## Executability verification`:

> Every executable specification must include an RFC-8785-canonical trace and sidecar conforming to `specs/data/executability_trace_schema_v1.json`. ARCHITECT fixes every uniquely identified row, its order, and all verification IDs; `STOP_UNRESOLVED` is the only permitted incomplete status. ARCHITECT never authors receiver dispositions. A trace never replaces the item-by-item post-edit and diff self-inspections already required.

## `CRITIC_INITIALIZATION.md`

Append to `## Executability review`:

> Independently follow every path and value in the specification's structured trace. Without editing the source trace, author `reviews/executability/<work_item_slug>_critic_disposition.json` and its sidecar under `specs/data/executability_trace_disposition_schema_v1.json`, bound to the raw trace digest, specification commit, source order, per-row RFC-8785 digest, and CRITIC verification IDs. Record `VERIFIED` or `BLOCKED` per row; any blocked/missing/mismatched row makes the overall disposition `BLOCKED`. Schema validity or an upstream `READY` assertion is never sufficient evidence.

## `TASK_BUILDER_INITIALIZATION.md`

Append to its executability/pre-build section:

> Only after Rebecca releases implementation and before editing, independently validate every structured-trace row. Without editing the source trace or CRITIC disposition, author `diagnostics/executability/<work_item_slug>_taskbuilder_disposition.json` and sidecar under `specs/data/executability_trace_disposition_schema_v1.json`, bound to the raw trace digest, specification commit, source order, per-row RFC-8785 digest, and TASK BUILDER verification IDs. STOP on `STOP_UNRESOLVED`, any blocked/missing/reordered row, digest/schema mismatch, missing fixed test ID, or implementer choice. After Rebecca approval, TASK BUILDER may perform exact mechanical role-contract/schema/tool edits, but never STATE.md, provenance, ledger, scientific-specification, scoring, or ruling authorship.

## `INTEGRATOR_INITIALIZATION.md`

Replace the next-recipient implication after STATE commit with:

> Every committed STATE.md update routes serially to RECORDER for hash attestation before any dependent event. Multiple already-authorized low-risk state events may be one commit only when each event is separately enumerated. INTEGRATOR is not a mandatory post-build hop unless the approved route declares a state event.

INTEGRATOR alone creates/updates `state/STATE.metadata.json` and sidecar using `workflow_state_metadata_schema_v1.json`; RECORDER attests both STATE and metadata hashes. `source_commit` names the input commit summarized by STATE, never the metadata commit.

## `RECORDER_INITIALIZATION.md`

Insert under custody rules:

> RECORDER attests every INTEGRATOR STATE update serially. For JUDGE rulings, RECORDER verifies the JUDGE-provided byte hash, scans without editing, commits the exact UTF-8/LF bytes under `docs/rulings/` on a recorder branch, appends custody provenance, and pushes. Byte mismatch, scan block, or publication failure yields `UNPUBLISHED_JUDGE_RULING` and STOP to Rebecca. Publication is custody, not gate approval.

> RECORDER alone creates/updates `docs/rulings/provenance_log.metadata.json` and sidecar. It also attests `state/STATE.metadata.json`; it never edits STATE or Coordinator metadata.

## `JUDGE_INITIALIZATION.md`

Replace step 5, `Return a ruling`, with:

> 5. Serialize the final ruling as strict UTF-8 without BOM, LF-only, exactly one final LF, and at most 4,194,304 bytes. Build the schema-defined RFC 8785 canonical JUDGE custody envelope using standard padded RFC 4648 base64 without whitespace and return it in one labeled formal handoff through the Coordinator to RECORDER. Do not commit, push, edit after hashing, split the envelope, or merge.

Append to the handoff format:

> - Ruling artifact filename
> - Ruling raw SHA-256
> - Byte length and UTF-8/LF attestation
> - Publication status: `PENDING_RECORDER_CUSTODY`

Add:

> A JUDGE ruling is durable evidence only after RECORDER publishes byte-identical content and attests its hash. It becomes operative only after Rebecca rules. If custody/publication fails, JUDGE does not rewrite or resubmit a substantively changed ruling; status is `UNPUBLISHED_JUDGE_RULING`.

## `PUBLIC_REPOSITORY_POLICY.md`

Replace only the header status/effective lines with:

> **Status:** Rebecca-approved and binding on all new work; substantive v1.1 requirements unchanged.
> **Publication status:** This metadata does not assert that the repository-public flip occurred; that remains a separate Rebecca decision.
> **Date:** 2026-08-17 · **Metadata corrected:** 2026-08-21
> **Approval provenance:** `docs/rulings/provenance_log.md` Entry 57 — Public-repository operating policy publication + STATE.md custody attestation. `[OP-Entry 57]`
> **Authority chain:** Rebecca > constitution's laws > approved specifications > this policy > agent judgment
> **Effective:** Binding prospectively on all new work. Historical files, SHAs, rulings, and evidence remain unchanged.

Append to §3 content review:

> New public artifacts must not contain persistent application task/thread/session IDs, task URLs, or private local routing-map identifiers. Use role labels, stable work-item slugs, repository refs, and full SHAs. Historical artifacts are not rewritten without Rebecca's separate authorization.

Replace §3.1's prospective scan-scope exception with:

> Every branch push is scanned across the complete introduced `base..tip` commit range and manually reviewed, regardless of path class or prior review. Unavailable/erroring scanners fail closed. The approved preflight helper may standardize evidence collection but never replaces manual review or independent custody/scoring integrity checks.

## State metadata and owner-specific edits

Metadata uses only `specs/data/workflow_state_metadata_schema_v1.json`, RFC 8785 canonicalization, and the sidecar rule in the program specification. No YAML/front-matter substitute is permitted.

- WORKFLOW COORDINATOR alone creates/updates `state/COORDINATOR_LEDGER.metadata.json`, each new `state/checkpoints/*.md.metadata.json`, and their sidecars.
- INTEGRATOR alone creates/updates `state/STATE.metadata.json` and sidecar.
- RECORDER alone creates/updates `docs/rulings/provenance_log.metadata.json` and sidecar and attests STATE metadata.
- TASK BUILDER may add schema validators/templates but may not populate or edit owner-controlled metadata instances.

For `state/COORDINATOR_HANDOFF_CHECKPOINT.md`, WORKFLOW COORDINATOR inserts immediately after the H1 title this exact line and changes no historical body text:

> **Status:** HISTORICAL SNAPSHOT — superseded for routing; retained unchanged as evidence. See adjacent metadata. `[PROPOSED]`

Coordinator creates `state/COORDINATOR_HANDOFF_CHECKPOINT.md.metadata.json` with exact values: `schema_version="workflow-state-metadata-v1"`, `as_of_utc="2026-08-19T14:51:00Z"`, `source_commit="d38f9069d9a4f2a92ffb3a29d6f80ef4e7253da9"`, `document_path="state/COORDINATOR_HANDOFF_CHECKPOINT.md"`, `document_sha256` computed after the approved one-line status insertion, `supersedes_metadata_sha256=[]`, `status="historical"`, `document_role="checkpoint"`, `owner_role="WORKFLOW_COORDINATOR"`. The target hash is implementation-time evidence and is not preclaimed by ARCHITECT `[PROPOSED]`.

No mechanical editor may modify historical content beyond that approved status line. Companion changelogs enumerate every changed file and exact inserted/replaced section.
