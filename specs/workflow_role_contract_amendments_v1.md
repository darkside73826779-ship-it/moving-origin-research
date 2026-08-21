# Prospective Role-Contract Amendments — Workflow Efficiency v1

**Date:** 2026-08-21

**Regime:** B

**Status:** Exact mechanical edit specification `[PROPOSED]`; do not apply before CRITIC CLEAR and Rebecca approval

## Universal insertion — all seven role initializations

Insert before `## Standing constraints`:

> ## Canonical workflow contracts
>
> Formal routing follows `specs/data/workflow_routing_table_v1.json`. A task-specific route overrides a default only through a full-SHA, repository-committed Rebecca-signed ruling and may not remove mandatory independence, custody, or Rebecca gates. Ownership transfers only through a labeled FORMAL HANDOFF. CONSULTATION REQUEST does not transfer ownership.
>
> Every formal handoff uses `specs/data/common_handoff_manifest_schema_v1.json`. The receiver independently verifies all fields within its authority; an upstream assertion is not evidence merely because it validates. New public artifacts must not contain application task/thread/session IDs or task URLs.
>
> Every push is scanned over the complete introduced `base..tip` range plus manual review. No role relies on the former narrow scan exemption. Tool output collects evidence and never replaces judgment.
>
> Every checkout uses the exact remote ref and full SHA from the handoff in an isolated detached worktree. Failure to prove ref/object/SHA identity, isolate the worktree, or obtain a clean checkout is STOP.

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

> Every executable specification must include a trace conforming to `specs/data/executability_trace_schema_v1.json`. ARCHITECT fixes every row and verification ID; `STOP_UNRESOLVED` is the only permitted incomplete status. A trace never replaces the item-by-item post-edit and diff self-inspections already required.

## `CRITIC_INITIALIZATION.md`

Append to `## Executability review`:

> Independently follow every path and value in the specification's structured trace. Record `VERIFIED` or `BLOCKED` per row without editing the source trace. Schema validity or an upstream `READY` assertion is never sufficient evidence.

## `TASK_BUILDER_INITIALIZATION.md`

Append to its executability/pre-build section:

> Before implementation, independently validate every structured-trace row and STOP on `STOP_UNRESOLVED`, digest/schema mismatch, missing fixed test ID, or implementer choice. After Rebecca approval, TASK BUILDER may perform exact mechanical role-contract/schema/tool edits, but never STATE.md, provenance, ledger, scientific-specification, scoring, or ruling authorship.

## `INTEGRATOR_INITIALIZATION.md`

Replace the next-recipient implication after STATE commit with:

> Every committed STATE.md update routes serially to RECORDER for hash attestation before any dependent event. Multiple already-authorized low-risk state events may be one commit only when each event is separately enumerated. INTEGRATOR is not a mandatory post-build hop unless the approved route declares a state event.

Add freshness keys to its STATE handoff requirement: `schema_version`, `as_of_utc`, `authoritative_commit`, `supersedes`, `status`, `document_role`.

## `RECORDER_INITIALIZATION.md`

Insert under custody rules:

> RECORDER attests every INTEGRATOR STATE update serially. For JUDGE rulings, RECORDER verifies the JUDGE-provided byte hash, scans without editing, commits the exact UTF-8/LF bytes under `docs/rulings/` on a recorder branch, appends custody provenance, and pushes. Byte mismatch, scan block, or publication failure yields `UNPUBLISHED_JUDGE_RULING` and STOP to Rebecca. Publication is custody, not gate approval.

## `JUDGE_INITIALIZATION.md`

Replace step 5, `Return a ruling`, with:

> 5. Serialize the final ruling as UTF-8/LF bytes, compute lowercase SHA-256, and return both to RECORDER through the authorized custody channel. Do not commit, push, edit after hashing, or merge.

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

## State document templates

The authorized mechanical owners add this exact front-matter block to new ledger/checkpoint/STATE-handoff/custody-package templates:

```yaml
schema_version: workflow-state-metadata-v1
as_of_utc: YYYY-MM-DDTHH:MM:SSZ
authoritative_commit: 40-lowercase-hex
supersedes: [40-lowercase-hex-or-empty]
status: current|superseded|historical
document_role: routing|durable_state|custody_history|checkpoint
```

No mechanical editor may modify historical content beyond adding approved metadata/status. Companion changelogs must enumerate every changed file and exact inserted/replaced section.
