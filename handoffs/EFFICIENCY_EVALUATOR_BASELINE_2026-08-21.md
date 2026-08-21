# EFFICIENCY EVALUATOR — Read-Only Baseline Report

**Date:** 2026-08-21  
**Regime:** B  
**Audience:** Rebecca, routed through the WORKFLOW COORDINATOR  
**Authority:** Proposal-only efficiency audit; no gate, merge, scoring, implementation, or approval authority exercised

## 1. Scope, method, and evidence boundary

This report maps the repository-controlled workflow as it exists on the default branch and proposes only prospective, Rebecca-gated improvements. The repository was cloned read-only for inspection and remained on default branch `main`. No file in the repository was edited; no diagnostic, scoring, seed, commit, push, PR, or merge action occurred.

Required sources were read completely:

- `state/role_initialization/ARCHITECT_INITIALIZATION.md`
- `state/role_initialization/CRITIC_INITIALIZATION.md`
- `state/role_initialization/INTEGRATOR_INITIALIZATION.md`
- `state/role_initialization/JUDGE_INITIALIZATION.md`
- `state/role_initialization/RECORDER_INITIALIZATION.md`
- `state/role_initialization/TASK_BUILDER_INITIALIZATION.md`
- `state/role_initialization/WORKFLOW_COORDINATOR_INITIALIZATION.md`
- `state/COORDINATOR_LEDGER.md`
- `state/COORDINATOR_HANDOFF_CHECKPOINT.md`
- `PUBLIC_REPOSITORY_POLICY.md`
- `docs/ARCHITECTURAL_CONSTITUTION_v2.md`, including binding §5

Only narrow, directly cited durable records were additionally checked to resolve whether the public-repository policy had in fact been approved and to test routing conflicts: `state/STATE.md` lines 556–558 and `docs/rulings/provenance_log.md` lines 1753–1780. No conversation transcript was replayed and no missing law was inferred.

## 2. Executive findings

The workflow’s main costs arise from fragmentation, not from the existence of independent checks. The same required facts—gate, input SHA, branch/result SHA, next recipient, prohibited actions, safety scan, provenance basis, and source tags—are copied across role handoffs, reviews, STATE.md, the provenance log, the coordinator ledger, and milestone checkpoints. Those copies are often protective, but there is no single canonical schema or routing table. This creates drift, repeated reading, reformatting, omission risk, and manual reconciliation.

The highest-value safe improvements are:

1. Establish one Rebecca-approved canonical routing table and resolve current contradictory chains.
2. Establish one versioned handoff/evidence-manifest schema used by every role, while preserving role-specific sections and independent verification.
3. Turn the existing executability obligations into a structured trace produced by ARCHITECT and independently adjudicated by CRITIC, with TASK BUILDER retaining the fail-closed final check.
4. Make durable-state documents explicitly hierarchical and freshness-marked so stale checkpoints cannot compete with the current ledger/STATE.md.
5. Standardize immutable-SHA checkout, diff, hash, and public-safety scan commands as approved mechanical tooling.

No proposal below removes CRITIC independence, JUDGE recomputation, RECORDER custody, INTEGRATOR ownership of STATE.md, public-safety scanning, source-class tags, raw-artifact scoring, no-rerun protection, seed separation, or Rebecca’s sole gate authority.

## 3. Current workflow map by role

### 3.1 WORKFLOW COORDINATOR

| Dimension | Current state |
|---|---|
| Inputs / prerequisite | Rebecca routing instruction or a role return handoff; startup sources are ledger first, then STATE.md, provenance tail, project instructions/checkpoint, and knowledge index (`WORKFLOW_COORDINATOR_INITIALIZATION.md` 56–63). If durable sources are ambiguous, STOP and ask Rebecca (lines 14, 45–46). |
| May read | Routing ledger, STATE.md, provenance tail, return handoffs, pointed-to repository artifacts; should not replay transcripts (`WORKFLOW_COORDINATOR_INITIALIZATION.md` 56–73). |
| May write | Sole author/custodian of `state/COORDINATOR_LEDGER.md`; milestone checkpoint package; narrow handoff files. Must not author scientific deliverables, specs, reviews, rulings, or code (lines 21–25, 42–50, 75–76). |
| Checks | Target role, gate, authoritative commit, scope, constraints, output expectations, next chain; role-boundary check; ambiguity stop; public scan before ledger merge; Gate 0 and fresh-context review routing (§5 obligations at lines 99–107). |
| Branch / commit / push | Coordinator branch convention. Ledger updated locally on every routing change, pushed and merged only at CRITIC CLEAR; coordinator’s exceptional merge authority covers only its ledger (lines 42–52). |
| Handoff fields | Gate, base SHA, input artifacts, authorized scope, constraints, output expectations, next chain (lines 35–40). |
| Stop conditions | Ambiguous state; blocked work without Rebecca instruction; non-repo authoritative text; role-scope collision; any sensitive scan finding before ledger merge. |
| Required consultations | Rebecca for ambiguity, gates, non-ledger merges, or resumption of blocked work. Fresh-context CRITIC for milestone law fidelity/compliance spot-checks (lines 103–107). |
| Downstream | Dedicated role named by routing protocol; Rebecca transports handoffs (lines 27–33, 70–73). |
| Main costs | Reformatting the same routing facts; reconciling ledger vs STATE/checkpoint; branch discovery; manually ensuring every handoff contains all repeated constraints. Low compute, moderate token/human-attention cost, potentially high delay when routing sources conflict. |

### 3.2 ARCHITECT

| Dimension | Current state |
|---|---|
| Inputs / prerequisite | Narrow handoff naming base SHA, files, gate, defects or design question. Must use repo-first binding text; missing binding law is a STOP (`ARCHITECT_INITIALIZATION.md` 31–39, 69–82; constitution §5.1 P1 at 130). |
| May read | Only files named by handoff (line 33), plus binding constitution/policy sources required by initialization. |
| May write | Specifications, amendments, contract clarifications, sequencing documents, and companion changelogs; not code, scores, judgments, or main merges (lines 5–18). |
| Checks | Locked bars and honest controls; implementer-invention test; complete executable-input trace; item-by-item post-edit verification; own diff inspection; changelog/diff match; comprehensive sweep when ordered; P1/P2/P3 and P4–P6; public-safety scan (lines 20–45, 61–82). |
| Branch / commit / push | Commit to `architect/` branch and push after scan; no main merge (lines 31–39, 61–67; ledger 13–19). |
| Handoff fields | Gate; input SHAs; files changed; branch/result SHA; status; blockers; diff self-inspection with exhaustive change list; exact next recipient; prohibited actions (lines 47–56). |
| Stop conditions | Undefined executable input; missing binding law; unresolved locked-bar authority; diff/changelog mismatch; incomplete comprehensive sweep; public-safety blocker. |
| Required consultations | Route output to independent CRITIC before Rebecca gates (line 16). Rebecca decides any proposed bar/rule/waiver. |
| Downstream | CRITIC, then Rebecca. |
| Main costs | Deep design and trace work; repeated manual enumeration of fixtures/schemas/digests; full-diff inspection; changelog duplication; review/remediation loops when executability gaps survive. High token/human-attention cost; variable latency; usually low compute. |

### 3.3 CRITIC

| Dimension | Current state |
|---|---|
| Inputs / prerequisite | Named base/result SHAs, pointed files, gate, and authorized scope (`CRITIC_INITIALIZATION.md` 26–32). Must remain independent and never co-author (lines 5–18). |
| May read | Only pointed files, relevant diff, constitution and cited provenance needed for P1–P6; raw implementation/diagnostic material within review scope. |
| May write | Only independent review artifact under `reviews/` and its handoff; cannot edit specs, code, scoring artifacts, or STATE.md (lines 12–19, 45–57). |
| Checks | First: law quote diff, threshold source tags, provenance citations (lines 85–98; constitution 140). Then authorized substance, executability end-to-end, quantitative recomputation when required, evidence preservation, classification, own review reread, scan. |
| Branch / commit / push | Review must be committed to `reviews/critic_<name>.md` on a `critic/` branch and pushed; an uncommitted review is invalid. Main checkout is read-only; no main mutation (lines 45–57). |
| Handoff fields | Gate; SHAs; one CLEAR/BLOCK/VERIFIED verdict; blocking/non-blocking findings; preserved evidence; next authorized role; prohibitions; confirmation no scoring/rerun/seed exposure/unauthorized merge; branch and review SHA; scan attestation (lines 34–57, 75–81). |
| Stop conditions | Cannot commit/push; non-executable contract; missing law diff/source tags/provenance verification; public-safety blocker. |
| Required consultations | May reconcile read-only helper reviews but issues one independent verdict (line 31). Must not co-author or advise how to pass. Rebecca alone gates/merges. |
| Downstream | CLEAR/VERIFIED follows approved routing; BLOCK returns only to originator. |
| Main costs | Independent re-reading and recomputation are intentionally expensive protections. Avoidable cost comes from unstructured executable-input searching and reconstructing evidence locations already known upstream. Moderate/high tokens and attention; quantitative review may incur compute. |

### 3.4 TASK BUILDER

| Dimension | Current state |
|---|---|
| Inputs / prerequisite | Rebecca-approved spec/task handoff; named base SHA and pointed files. No implementation before approval (`TASK_BUILDER_INITIALIZATION.md` 11–19, 33–40). |
| May read | Handoff-pointed approved specs/task specs and files necessary to implement/test. No hold-out/scoring seeds. |
| May write | Code, tests, diagnostic runners, diagnostic output, implementation handoff; not specifications, scoring packets, bars, controls, or scoring logic absent explicit authorization (lines 5–19). |
| Checks | Before build, trace executable fixtures, artifact pairs, stochastic realizations, schemas/order/digests; STOP rather than invent. Test critical paths; use only seeds 101–105; run diagnostic-only verification; scan before push; implement only tagged criteria and keep guards fail-closed (lines 21–31, 33–40, 56–79). |
| Branch / commit / push | Commit implementation/tests/diagnostics to `taskbuilder/` branch; scan and push; never main merge. |
| Handoff fields | Gate; input SHAs; changed files; branch/result SHA; implementation; diagnostic verification; blockers; next role; prohibited actions (lines 42–51). |
| Stop conditions | Any implementer-invention gap; absent approved handoff; forbidden seed/scoring access; public-safety blocker; authorization mismatch. |
| Required consultations | Specification block routes to ARCHITECT. Independent implementation review routes to CRITIC. Rebecca controls build/run/gate authorization. |
| Downstream | Ambiguous in current sources: coordinator init says TASK BUILDER → INTEGRATOR → CRITIC → RECORDER → Rebecca (lines 27–33), but ledger says code → CRITIC → Rebecca (ledger 38–43), while current durable state has task-specific variants. |
| Main costs | Implementation/tests/diagnostics dominate compute. Avoidable cost arises when executability defects reach the last defense, producing stop/remediation cycles; repeated output formatting and scan/hash commands add smaller costs. |

### 3.5 INTEGRATOR

| Dimension | Current state |
|---|---|
| Inputs / prerequisite | Named base SHA and pointed handoff/artifacts; authorized state-management gate (`INTEGRATOR_INITIALIZATION.md` 22–28). |
| May read | Only pointed files and authoritative returned artifacts. |
| May write | Sole writer of `state/STATE.md`; operational assembly/state management. Cannot edit provenance log, specs, or code (lines 5–20). |
| Checks | Exact commit hash of artifact run/to be run; milestone/session/timebox/bars/watch items/run requests/artifacts/status/blockers/next action; preserve negative labels; source-tag discipline and proposed quarantine; public scan (lines 11–20, 38–64). |
| Branch / commit / push | Commit STATE.md on `integrator/` branch; return STATE hash; no main merge without Rebecca. |
| Handoff fields | Gate; input SHAs; STATE summary; STATE SHA-256; branch/result SHA; next role (lines 30–36). |
| Stop conditions | Provenance/state uncertainty; role-scope request; unauthorized merge; public-safety blocker. Divergence detected by RECORDER escalates immediately to Rebecca. |
| Required consultations | RECORDER must attest each update; Rebecca resolves divergence and merges. |
| Downstream | RECORDER for hash attestation/custody, or task-specific next role according to routing. |
| Main costs | Manual transcription and reconciliation of facts already in handoffs/ledger/provenance; branch/commit cycle per state update; downstream hash attestation. Low compute, moderate attention and latency. |

### 3.6 RECORDER

| Dimension | Current state |
|---|---|
| Inputs / prerequisite | Named base SHA, pointed source branch/commit, STATE.md update or artifact custody event (`RECORDER_INITIALIZATION.md` 22–27). |
| May read | Pointed source artifacts, STATE.md, applicable hashes/commits, seed exposure facts, constitution hash. |
| May write | Append-only `docs/rulings/provenance_log.md`; custody/publication artifacts; no STATE.md, specs, implementation, scoring artifacts, or reviews (lines 5–20). |
| Checks | Timestamp/actor/action/predecessors/hashes/commit/custody chain; attest every INTEGRATOR STATE hash; detect divergence; seed-exposure ledger; preserve negatives; verify constitution SHA unchanged at milestones; date new artifacts; public scan (lines 11–20, 38–64). |
| Branch / commit / push | Commit/push on `recorder/` branch under authorization; Rebecca merges. |
| Handoff fields | Gate; base SHA; source commit/branch; STATE hash; provenance entries; artifacts published; next role (lines 29–36). |
| Stop conditions | STATE/provenance divergence; missing custody inputs; public-safety blocker; unauthorized publication/merge. |
| Required consultations | Immediate Rebecca escalation for divergence; coordinates with INTEGRATOR but cannot collapse ownership. |
| Downstream | JUDGE in scoring custody chain, or Rebecca / next authorized role. |
| Main costs | Re-encoding facts from prior handoffs into append-only provenance; hashing and publication; high attention for custody accuracy, low compute except large artifact inventories. |

### 3.7 JUDGE

| Dimension | Current state |
|---|---|
| Inputs / prerequisite | Raw returned scoring artifacts and pre-registered criteria; named spec/commit/seeds (`JUDGE_INITIALIZATION.md` 30–35). |
| May read | Only scoring artifacts pointed to; approved spec/bars and provenance needed to establish basis/integrity. Agent summaries and expected outcomes are not evidence (lines 11–20). |
| May write | Ruling/handoff only; no code, experiment specification, rerun, or merge. |
| Checks | Raw-artifact recomputation; integer-count p-values; file hashes/package integrity/provenance; failure classification; prior evidence preservation; per-law/per-seed tables; reproducibility; L20; interfaces; cross-run consistency; bar tags before scoring (lines 11–28, 37–49, 64–77). |
| Branch / commit / push | Initialization does not define a required judge branch/commit/push path, although public-safety language assumes content may be pushed. This is an unresolved workflow specification gap. |
| Handoff fields | Scoring basis; integrity; per-law/per-seed recomputation; kills; reproducibility; L20; interfaces; provenance; consistency; verdict; non-blocking issues; next role (lines 37–49). |
| Stop conditions | Untagged or `[PROPOSED]` scoring criterion; incomplete artifacts/provenance; law-level instrument failure; request to rerun or reinterpret bars. |
| Required consultations | Independence from implementers/agent summaries; Rebecca is sole gate. No consultation may be used to make evidence pass. |
| Downstream | RECORDER for ruling custody, then Rebecca (coordinator routing line 31). |
| Main costs | Intentionally duplicated independent metric/hash/provenance recomputation. High attention and potentially high compute; avoidable cost is mainly evidence discovery and noncanonical package schemas. |

## 4. Redundancy matrix

| Repeated work | Roles / artifacts | Why repeated | Classification | Root cause and avoidable portion |
|---|---|---|---|---|
| Gate, input SHA, result SHA, next recipient, prohibitions | Every role handoff; ledger; STATE; provenance | Scope control, reproducibility, routing | Protection with avoidable re-entry | No shared schema or machine-readable manifest. Facts are manually copied and can drift. |
| Public-safety scan and attestation | Every pushing role; coordinator ledger merge | Every remote branch is a public surface (`PUBLIC_REPOSITORY_POLICY.md` 205–225) | Mandatory protection | The scan cannot be removed. Commands, scope calculation, and evidence format can be standardized; unchanged commits need not be re-discovered manually. |
| Source tags / law quotes / provenance citations | ARCHITECT creates; CRITIC independently verifies; TB/JUDGE/INTEGRATOR enforce | Prevents bar laundering and reconstructed law (§5 P1–P6, lines 128–145) | Mandatory independent protection | Upstream trace can be structured; CRITIC verification must remain independent. |
| Executability trace | ARCHITECT, CRITIC, TASK BUILDER | Three defenses after false-deterministic/false-CLEAR event | Mandatory layered protection | Each role currently searches prose anew. A canonical trace artifact would reduce discovery cost while retaining three distinct dispositions. |
| Diff/review self-inspection | ARCHITECT and CRITIC | Prevent false attestations and malformed reviews | Mandatory self-control | Mechanical checklist and diff summary can reduce manual omission; cannot replace inspection. |
| Hash computation / verification | INTEGRATOR, RECORDER, JUDGE; often CRITIC | State custody, artifact integrity, independent scoring | Mostly mandatory | Standard manifest generation reduces repeated path enumeration. Independent recomputation remains necessary at custody/scoring boundaries. |
| Negative-result classification | CRITIC, INTEGRATOR, RECORDER, JUDGE, coordinator | Preserve honest labels and O-14 evidence | Mandatory protection | Canonical enum/field prevents prose relabeling while reducing rephrasing. |
| State facts copied across ledger, STATE, checkpoint, provenance | Coordinator, INTEGRATOR, RECORDER | Fast routing, durable operational state, append-only custody, session continuity | Distinct purposes, but avoidable overlap/drift | Document precedence/freshness is insufficiently explicit; checkpoint and ledger can conflict in time. |
| Branch discovery / clone-or-checkout | Every role | Isolation and exact-SHA review | Protection with avoidable mechanics | Every init repeats “clone or checkout”; no approved common read-only checkout recipe or handoff-provided remote ref verification. |
| Review publication plus handoff | CRITIC review file and return message | Durable evidence and routing pointer | Necessary two-layer record | Handoff should be a compact pointer generated from review metadata, not a second free-form account. |

## 5. Ranked efficiency opportunities

| Rank | Opportunity | Likely benefit | Governance risk | Reason |
|---:|---|---|---|---|
| 1 | Canonical routing table with explicit precedence and task-specific override mechanism | High latency and error reduction | Medium | Current controlling files disagree about post-build order and parallelism. Routing error can waste entire role cycles. |
| 2 | Versioned common handoff/evidence-manifest schema | High token and attention reduction | Low–medium | Replaces repeated free-form copying without changing authority or checks. |
| 3 | Structured executability trace with independent dispositions | High rework reduction | Medium | Targets the documented root cause of repeated spec/build stops while preserving all three defenses. |
| 4 | State hierarchy and freshness markers | Medium–high routing/continuity benefit | Low | Prevents stale checkpoint or duplicated state from being treated as current. |
| 5 | Approved scan/hash/diff tooling | Medium recurring attention benefit | Low | Mechanizes mandatory procedures without altering their standards. |
| 6 | Immutable-SHA checkout recipe and handoff ref verification | Medium setup benefit | Low | Reduces clone/branch discovery repetition and accidental base mismatch. |
| 7 | Event batching rules for INTEGRATOR/RECORDER/ledger | Medium git and latency benefit | Medium | Existing text encourages batching but also strict serial execution; clarification is needed before use. |
| 8 | Repair policy status header and future task-ID/session-reference handling | Moderate governance/public-safety benefit | Low | Removes a misleading draft marker and avoids future prohibited metadata publication. |

## 6. Safeguards that must not be removed

1. **Rebecca’s sole gate and general merge authority.** Coordinator’s exception remains limited to its own ledger at CRITIC CLEAR (`WORKFLOW_COORDINATOR_INITIALIZATION.md` 8–9, 42–52).
2. **CRITIC independence.** No co-authoring, fixing, or advice on how evidence can pass (`CRITIC_INITIALIZATION.md` 5–19).
3. **JUDGE raw-artifact independence and recomputation.** Summaries and implementation claims are not evidence (`JUDGE_INITIALIZATION.md` 11–21).
4. **Three-layer executability defense.** ARCHITECT must fully specify, CRITIC must independently block non-executable contracts, and TASK BUILDER must stop rather than invent (`ARCHITECT_INITIALIZATION.md` 20–29; `CRITIC_INITIALIZATION.md` 59–70; `TASK_BUILDER_INITIALIZATION.md` 21–31).
5. **Versioned-law P1–P6.** Especially repo-first law, verbatim quotation, source tags, regime dating, signed waivers, and provenance checking (constitution §5.1, lines 124–145).
6. **Role-separated state and provenance custody.** INTEGRATOR alone writes STATE.md; RECORDER alone appends the provenance log and attests STATE hashes (`INTEGRATOR_INITIALIZATION.md` 5–20; `RECORDER_INITIALIZATION.md` 5–20).
7. **O-14/no rerun, development/scoring seed separation, and negative-label preservation.** These prevent score chasing and evidence laundering (role initializations’ standing constraints; coordinator lines 78–89).
8. **Public-safety scan before every relevant push and scan of all introduced commits.** Intermediate commits can retain secrets even when the net diff is clean (`PUBLIC_REPOSITORY_POLICY.md` 52–91, 205–225).
9. **Immutable artifact and SHA provenance.** Handoffs must identify exact bases/results; scoring/custody must independently verify integrity.
10. **Fresh-context constitutional review at milestone gates.** Standing CRITIC review does not substitute for the designated law-fidelity review (constitution 145).

## 7. One-by-one proposed changes

Every proposal is inoperative unless Rebecca explicitly approves it. Governance/role-contract changes follow ARCHITECT → CRITIC → Rebecca before TASK BUILDER implements approved text/tooling.

### Proposal 1 — One canonical routing contract

- **Problem / evidence:** `WORKFLOW_COORDINATOR_INITIALIZATION.md` 27–33 states “TASK BUILDER → INTEGRATOR → CRITIC → RECORDER → Rebecca.” `state/COORDINATOR_LEDGER.md` 38–43 states code goes TASK BUILDER → CRITIC → Rebecca and treats state/provenance as housekeeping. `WORKFLOW_COORDINATOR_INITIALIZATION.md` 28 says exactly one role active, while lines 65–68 allow parallel RECORDER/INTEGRATOR housekeeping. Current task-specific durable records contain further legitimate variants.
- **Smallest change:** Add a canonical routing table to the coordinator initialization with: default route by deliverable; prerequisites; allowed parallelism; mandatory state/custody points; and a rule that a Rebecca-approved, repository-committed task route may override the default when cited by SHA. Make the ledger reference rather than restate the table.
- **Affected files/text:** `state/role_initialization/WORKFLOW_COORDINATOR_INITIALIZATION.md` 27–33 and 65–68; `state/COORDINATOR_LEDGER.md` 9–46. Conforming references may be required in other role initialization “next recipient” language.
- **Benefit:** High; prevents wrong-role cycles and removes repeated routing reconstruction.
- **Risks / independence:** A poorly designed table could collapse required review or custody. Preserve role independence, scoring route, and Rebecca override explicitly.
- **Approval path:** ARCHITECT drafts role-contract amendment → fresh CRITIC law/governance review → Rebecca approval → TASK BUILDER performs exact approved mechanical edits/tests if assigned.
- **Rollback:** Revert only the approved routing-contract commit; prior initialization files remain in git history.
- **Rebecca decision request:** **Does Rebecca approve commissioning ARCHITECT to draft one canonical routing table that resolves the post-build and parallel-housekeeping contradictions without removing any gate or independent role?**

### Proposal 2 — Versioned common handoff/evidence manifest

- **Problem / evidence:** Role-specific handoff lists repeat gate, SHAs, branch, next recipient, prohibitions, scan evidence, and status (`ARCHITECT_INITIALIZATION.md` 47–56; CRITIC 34–57; TASK BUILDER 42–51; INTEGRATOR 30–36; RECORDER 29–36; JUDGE 37–49; coordinator 35–40).
- **Smallest change:** Define one repository schema/template with common required fields plus role-specific extensions. Include `schema_version`, `date`, `regime`, `gate`, `authority_basis`, `base_sha`, `result_sha`, `artifact_paths`, `artifact_hashes`, `branch`, `checks_performed`, `findings`, `scan_attestation`, `next_role`, and `prohibited_actions`. Human-readable Markdown may be generated from or embed a small canonical YAML/JSON block.
- **Affected files/text:** All seven role initialization handoff sections; new approved template/schema under a governance/tooling path chosen by ARCHITECT.
- **Benefit:** High recurring token/attention savings; fewer omissions; easier coordinator ingestion.
- **Risks / independence:** A shared schema must not turn upstream claims into downstream evidence. Each role must independently verify fields within its authority and record its own disposition.
- **Approval path:** ARCHITECT specification → CRITIC review → Rebecca approval → TASK BUILDER schema validator/template generator → CRITIC implementation review → Rebecca release.
- **Rollback:** Stop invoking the validator and revert schema references; existing Markdown handoffs remain readable.
- **Rebecca decision request:** **Does Rebecca approve specification of a shared handoff manifest while retaining each role’s independent checks and role-specific fields?**

### Proposal 3 — Structured executability trace, not fewer defenses

- **Problem / evidence:** The same fixture/artifact-pair/stochastic-realization/schema/digest categories are manually traced by ARCHITECT, CRITIC, and TASK BUILDER (`ARCHITECT_INITIALIZATION.md` 20–29; CRITIC 59–70; TASK BUILDER 21–31). The repetition is protective, but unstructured prose makes gaps costly to find and remediate.
- **Smallest change:** Require each executable spec to include a fixed trace table: executable input, repository source/path, exact value/schema, canonicalization, expected digest, producer, consumer, creation time, and unresolved status. ARCHITECT fills it; CRITIC independently checks every row and may add findings but never edits it; TASK BUILDER rechecks and stops on any unresolved/mismatched row.
- **Affected files/text:** The three initialization executability sections and the specification template(s), after exact ARCHITECT scoping.
- **Benefit:** High rework savings; should catch omissions earlier and make review bounded.
- **Risks / independence:** Checklist complacency. Require CRITIC to trace actual executable paths, not merely accept checked boxes; retain TASK BUILDER’s independent STOP.
- **Approval path:** ARCHITECT → CRITIC → Rebecca; TASK BUILDER may implement only validator/tooling after the behavior is completely specified.
- **Rollback:** Remove trace requirement prospectively; no prior evidence altered.
- **Rebecca decision request:** **Does Rebecca approve commissioning a structured executability-trace contract that preserves all three independent defensive layers?**

### Proposal 4 — Explicit state precedence and freshness

- **Problem / evidence:** Coordinator startup reads ledger, STATE.md, provenance tail, and checkpoint (`WORKFLOW_COORDINATOR_INITIALIZATION.md` 56–63). The checkpoint dated 2026-08-19 describes an in-flight state superseded by the 2026-08-20 ledger. The ledger itself contains current state plus long historical detail despite its compact-state purpose (`COORDINATOR_LEDGER.md` 48–155). Without explicit machine-readable freshness and precedence, agents spend tokens reconciling documents.
- **Smallest change:** Put `as_of`, `authoritative_commit`, `supersedes`, and `status: current|superseded` headers in ledger/checkpoint/STATE handoff packages. State precedence: current ledger for routing; STATE.md for durable project facts; provenance for custody/history; checkpoint only if marked current and newer than the ledger’s last milestone boundary. Keep checkpoint immutable or clearly superseded rather than silently competing.
- **Affected files/text:** `WORKFLOW_COORDINATOR_INITIALIZATION.md` 42–76; `state/COORDINATOR_LEDGER.md` header/current-state structure; `state/COORDINATOR_HANDOFF_CHECKPOINT.md` header/template; possibly STATE.md metadata specification.
- **Benefit:** Medium–high; faster startup and fewer ambiguous-state stops.
- **Risks / independence:** Incorrect precedence could hide a divergence. Any mismatch between durable sources must still STOP/escalate; metadata is not self-authentication.
- **Approval path:** ARCHITECT governance design → CRITIC → Rebecca → assigned role(s) make approved prospective template edits; INTEGRATOR/RECORDER ownership remains intact.
- **Rollback:** Revert metadata/template changes; provenance and prior checkpoint content remain preserved.
- **Rebecca decision request:** **Does Rebecca approve explicit freshness/precedence metadata for routing-state documents, with fail-closed escalation on mismatch?**

### Proposal 5 — Approved mechanical preflight tooling

- **Problem / evidence:** Each role must calculate diffs, hashes, scan scope, introduced commits, and attestation text manually. Policy requires all introduced commits, including intermediate diffs, be scanned (`PUBLIC_REPOSITORY_POLICY.md` 63–91); ARCHITECT/CRITIC additionally self-inspect diffs/reviews.
- **Smallest change:** Specify a read-only/pre-push command that takes an explicit base and tip SHA and emits: commit range; changed files; SHA-256 manifest; secret-tool result; regex result; prohibited-path/session-ID findings; and a canonical attestation block. It must fail closed, never push, never alter files, and never declare scientific validity.
- **Affected files/text:** `PUBLIC_REPOSITORY_POLICY.md` §3 evidence format; all role public-safety sections; optional new script and tests at an approved path.
- **Benefit:** Medium recurring attention savings and stronger consistency.
- **Risks / independence:** Tool false negatives and misplaced trust. Manual content review remains required; CRITIC/RECORDER/JUDGE retain independent integrity checks.
- **Approval path:** ARCHITECT completely specifies behavior and threat model → CRITIC review → Rebecca approval → TASK BUILDER implementation/tests → CRITIC verification → Rebecca release.
- **Rollback:** Disable/revert tool; manual policy remains binding.
- **Rebecca decision request:** **Does Rebecca approve specification of fail-closed scan/hash/diff preflight tooling that automates evidence collection but not judgment?**

### Proposal 6 — Immutable-SHA checkout recipe

- **Problem / evidence:** Every operational role repeats “clone or checkout the named base SHA” and reads only pointed files. Branch discovery in the ledger uses a broad branch listing (`COORDINATOR_LEDGER.md` 13–35), which adds latency and can select the wrong similarly named branch.
- **Smallest change:** Require handoffs to carry remote ref plus full base/result SHA. Define one safe recipe: verify remote object exists; fetch only required ref/object where possible; use isolated worktree or detached read-only inspection for review; confirm `HEAD` equals named SHA before work. No automatic pulls, resets, or main mutation.
- **Affected files/text:** “When you receive a handoff” sections for operational roles; common handoff schema; ledger branch-discovery guidance.
- **Benefit:** Medium setup savings and lower base-selection risk.
- **Risks / independence:** Shared working trees can contaminate evidence. Isolation and exact-SHA assertions must be mandatory.
- **Approval path:** ARCHITECT specifies safe repository procedure → CRITIC governance/safety review → Rebecca approval → TASK BUILDER may provide tested helper tooling.
- **Rollback:** Return to manual clone/checkout instructions.
- **Rebecca decision request:** **Does Rebecca approve a standardized exact-SHA isolated-checkout procedure to replace repeated broad branch discovery?**

### Proposal 7 — Clarify and batch state/custody events

- **Problem / evidence:** INTEGRATOR commits every STATE update and RECORDER attests after every update (`INTEGRATOR_INITIALIZATION.md` 22–28; `RECORDER_INITIALIZATION.md` 11–16). Coordinator guidance says batch RECORDER/INTEGRATOR housekeeping and even run them in parallel where possible (coordinator 65–68), while strict serial execution says exactly one role active (27–33). Parallel operation is unsafe if RECORDER must attest an INTEGRATOR output that does not yet exist.
- **Smallest change:** Define event classes: (A) dependency-bound STATE update → RECORDER attestation, strictly serial; (B) independent custody and state updates from the same already-frozen source, possibly prepared concurrently but committed/merged in a specified order; (C) multiple low-risk events batched into one authorized state/custody milestone. Do not weaken “attest after every INTEGRATOR update.”
- **Affected files/text:** `WORKFLOW_COORDINATOR_INITIALIZATION.md` 27–33, 42–52, 65–68; INTEGRATOR and RECORDER handoff sections.
- **Benefit:** Medium latency/git-operation reduction.
- **Risks / independence:** Race-induced hash divergence or custody gaps. Dependency graph and commit order must be explicit and fail closed.
- **Approval path:** ARCHITECT → CRITIC → Rebecca; implementation only after exact workflow specification.
- **Rollback:** Revert to strict serial one-event-per-cycle processing.
- **Rebecca decision request:** **Does Rebecca approve clarification of which housekeeping can be batched or prepared concurrently, while keeping hash-dependent custody serial?**

### Proposal 8 — Repair public-policy status metadata

- **Problem / evidence:** `PUBLIC_REPOSITORY_POLICY.md` lines 3 and 293 describe a draft/effectiveness boundary, but `state/STATE.md` 556–558 says v1.1 was CRITIC-CLEAR and Rebecca-approved, and provenance lines 1753–1780 record that approval/publication. Every role initialization calls the policy governing. The policy’s own status header therefore misleads readers even though the approval record exists.
- **Smallest change:** After provenance verification, amend only the status/effective metadata to cite the approval/provenance entry and clearly distinguish “approved and binding on new work” from “repository public flip not yet authorized,” if that remains the intended state. Do not change substantive requirements.
- **Affected files/text:** `PUBLIC_REPOSITORY_POLICY.md` 3–7 and 291–297; optional changelog entry.
- **Benefit:** Moderate; eliminates repeated authority reconciliation and accidental under-enforcement.
- **Risks / independence:** Misstating current publication status. Exact language must be ARCHITECT-drafted and CRITIC-verified against provenance.
- **Approval path:** ARCHITECT → CRITIC → Rebecca → authorized mechanical edit.
- **Rollback:** Revert metadata commit; approval evidence remains in provenance.
- **Rebecca decision request:** **Does Rebecca approve a metadata-only correction so the policy itself accurately states its approved/binding status and separately states whether the public flip occurred?**

### Proposal 9 — Prohibit persistent task/session IDs in future public artifacts

- **Problem / evidence:** Public policy prohibits session references and infrastructure leakage in public writing (`PUBLIC_REPOSITORY_POLICY.md` 77–80, 118–129). The historical checkpoint contains a canonical task URL and session identifiers (`COORDINATOR_HANDOFF_CHECKPOINT.md` 5, 25–32). The present audit mandate also says task IDs are local coordination metadata and must never be committed publicly. Historical content must not be rewritten by default (policy 238–266).
- **Smallest change:** Prospective template rule: public ledger/checkpoint/handoff files use stable role/task labels and repository SHAs only; local task IDs remain outside the repository. Do not rewrite historical artifacts absent Rebecca’s separate public-safety decision.
- **Affected files/text:** Coordinator checkpoint and ledger templates; all handoff templates; policy content-review examples may add task/session IDs explicitly.
- **Benefit:** Moderate public-safety and clarity benefit.
- **Risks / independence:** Loss of local coordination linkage. Keep an uncommitted/private local mapping under Rebecca’s control, never referenced as authority.
- **Approval path:** ARCHITECT governance clarification → CRITIC → Rebecca → prospective template edits.
- **Rollback:** Re-enable fields only by new Rebecca-approved amendment; historical provenance unchanged.
- **Rebecca decision request:** **Does Rebecca approve a prospective ban on committing task/session IDs, while leaving historical content untouched pending her separate public-safety classification?**

### Proposal 10 — Define JUDGE ruling custody/publication mechanics

- **Problem / evidence:** JUDGE has detailed scoring and handoff requirements but no explicit commit, branch, push, scan-evidence, or STOP-if-publication-unavailable procedure (`JUDGE_INITIALIZATION.md` 30–60), unlike CRITIC’s binding in-repo review rule. Coordinator routing says scoring goes Rebecca/executor → RECORDER → JUDGE → RECORDER → Rebecca (`WORKFLOW_COORDINATOR_INITIALIZATION.md` 27–33), suggesting RECORDER may be the sole publisher, but this is not explicit.
- **Smallest change:** Specify that JUDGE returns a signed/hashable ruling artifact to RECORDER for custody and authorized publication, or define a judge branch if Rebecca prefers. State who scans, who commits, and when the ruling becomes durable evidence. Preserve JUDGE independence and RECORDER custody.
- **Affected files/text:** `JUDGE_INITIALIZATION.md` handoff/public-safety sections; `RECORDER_INITIALIZATION.md` custody scope; coordinator scoring route.
- **Benefit:** Medium; prevents an uncommitted-ruling ambiguity at the most consequential gate.
- **Risks / independence:** RECORDER must not edit the JUDGE ruling; publication must be byte-for-byte with hash attestation.
- **Approval path:** ARCHITECT → CRITIC → Rebecca; mechanical template/tool changes only after approval.
- **Rollback:** Revert prospective mechanics; retained rulings and provenance remain intact.
- **Rebecca decision request:** **Does Rebecca approve commissioning an explicit byte-for-byte JUDGE-to-RECORDER custody/publication contract?**

## 8. Unresolved ambiguities requiring ARCHITECT clarification

These should not be resolved by evaluator judgment:

1. **Post-build default route:** Is the general default TASK BUILDER → INTEGRATOR → CRITIC → RECORDER → Rebecca, or TASK BUILDER → CRITIC → Rebecca with housekeeping later? Which repository-committed task documents may override it, and by what precedence?
2. **Strict serial versus parallel housekeeping:** Does “exactly one role session active” prohibit concurrent preparation by RECORDER and INTEGRATOR, or only concurrent work on a shared dependency/artifact?
3. **Checkpoint authority:** Is `state/COORDINATOR_HANDOFF_CHECKPOINT.md` a mutable current pointer, an immutable historical snapshot, or a replace-at-milestone file? How must a stale checkpoint identify itself?
4. **Public-policy effective status:** The durable record says approved and role inits treat it as governing, while the file header says draft and effective upon publication-readiness merge. Did that merge occur, or was the intended rule “binding on new work after approval even before public flip” as §13 suggests?
5. **JUDGE durability:** Is the ruling committed by JUDGE, or passed byte-for-byte to RECORDER for publication? When does it become official evidence?
6. **Integrator position in implementation flow:** Is INTEGRATOR always an assembly/state step before implementation review, only used when a task/courier spec must be extracted, or a post-review reconciliation role?
7. **Handoff storage:** Are return handoffs required in-repo for all roles, optional attachments, or pointers generated from durable artifacts? CRITIC is explicit; others are not.
8. **Scan scope mismatch:** Policy §3.1 exempts some previously reviewed `src/`/`specs/`-only pushes unless they embed sensitive content, while every initialization says self-scan before any branch push. Which stricter rule is intended prospectively?
9. **Task/session metadata:** How should the coordinator retain local role-session mappings needed for routing without committing them to public surfaces?
10. **Who implements role-contract text after approval:** The audit mandate routes governance changes through ARCHITECT → CRITIC → Rebecca before TASK BUILDER implementation, but some role-contract edits historically appear to be authored directly by governance roles. ARCHITECT should specify the exact mechanical implementer boundary.

## 9. Recommended Rebecca decision order

To minimize design churn, decide proposals in this order:

1. Proposal 1 (canonical routing) and Proposal 7 (safe batching/parallelism) together.
2. Proposal 2 (common manifest) and Proposal 3 (executability trace) together.
3. Proposal 4 (state freshness/precedence).
4. Proposal 5 and 6 (mechanical tooling and checkout).
5. Proposal 8, 9, and 10 (status/public metadata and ruling custody).

This sequencing first settles authority and dependencies, then schemas, then tooling. No proposed change should be implemented until its exact behavior, risks, review path, and rollback are approved by Rebecca.

## 10. Audit handoff

- **Gate served:** Rebecca-authorized read-only efficiency baseline audit
- **Repository inspected:** `darkside73826779-ship-it/moving-origin-research`, default branch `main`
- **Repository changes:** None
- **Diagnostics/scoring/seeds:** None accessed or run
- **Verdict/status:** Baseline complete; ten proposal-only opportunities and ten ARCHITECT ambiguities identified
- **Next recipient:** WORKFLOW COORDINATOR, for delivery to Rebecca and routing only after Rebecca’s decisions
- **Explicitly prohibited:** No proposal is operative; no role should edit, implement, score, rerun, expose seeds, commit, push, PR, or merge based on this report without the required approval path

