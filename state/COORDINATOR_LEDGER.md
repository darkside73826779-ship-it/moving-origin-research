# WORKFLOW COORDINATOR LEDGER

**Purpose:** Working routing state — who has the ball, what handoff is in flight, the immediate next action, active role sessions. Maintained locally by the coordinator, pushed to GitHub at each CRITIC CLEAR (not on every ball-pass — git operations are batched to the clear). A fresh coordinator reads this first to see where the ball is, then STATE.md for durable context.

**Discipline:** Update locally in-place on every ball-pass. Push to GitHub only at CRITIC CLEAR milestones, alongside the RECORDER entry and STATE.md reconciliation. The local checkout is the working copy; GitHub is the durable checkpoint.

---

## Routing manual (applicable logic — how to deduce the next action from the ball-state)

A fresh coordinator reading "ball with ROLE on TASK" should be able to deduce, from this manual, what to do next and where to find the role's deliverable — without replaying conversation history.

### Branch naming conventions (where each role commits)
- ARCHITECT → `architect/`-prefixed branches (e.g., `architect/l8-instantiation-v2`)
- CRITIC → `critic/`-prefixed branches (e.g., `critic/l8-spec-v2.2-fresh-rereview`)
- TASK BUILDER → `taskbuilder/`-prefixed branches (e.g., `taskbuilder/l8-power-analysis`)
- RECORDER → `recorder/`-prefixed branches
- INTEGRATOR → `integrator/`-prefixed branches
- COORDINATOR → `coordinator/`-prefixed branches

To find a role's latest work: `gh api repos/darkside73826779-ship-it/moving-origin-research/branches --jq '.[].name' | grep <role-prefix>`

### Deliverable location patterns (where each role's product lives)
- Code (TASK BUILDER): `diagnostics/` for analysis scripts, `src/` for harness/experiment code
- Specs (ARCHITECT): `specs/` for M4-spec-family documents, `reviews/l8_crossfamily_review/` for the L8 instantiation spec and its chain documents
- Reviews (CRITIC): `reviews/` (e.g., `reviews/critic_l8_*.md`)
- Provenance entries (RECORDER): appended to `docs/rulings/provenance_log.md`
- State (INTEGRATOR): `state/STATE.md` and `GOVERNANCE_SOURCE_MAP.md`
- Handoffs: `handoffs/` (role return handoffs) or attached by Rebecca

### When Rebecca reports a role is complete (the trigger)
When Rebecca says a role is complete (or any phrasing suggesting it — "architect finished," "critic clear," "task builder complete"), the coordinator:
1. Checks for the role's branch: `gh api repos/darkside73826779-ship-it/moving-origin-research/branches --jq '.[].name' | grep <role-prefix>`
2. Reads the role's return handoff (either committed to `handoffs/` on the branch, or attached by Rebecca as a .md file)
3. Routes per the routing protocol below
4. Does NOT poll the role session — Rebecca is the courier; she reports completion

### Routing protocol (what to do with each deliverable type)
- **Spec deliverable** (ARCHITECT produces a spec revision): → CRITIC for fresh-context delta re-clear with law-diff table → on CLEAR, to Rebecca for ruling/sign-off
- **Code deliverable** (TASK BUILDER produces implementation): → CRITIC for implementation review (code-vs-spec fidelity, candidate-blindness) → on CLEAR, to Rebecca for the run decision / gate ruling
- **Review deliverable** (CRITIC returns CLEAR): → coordinator pushes+merges the ledger (coordinator's own authority) → routes the next handoff per the plan
- **Review deliverable** (CRITIC returns BLOCK): → returns to the originating role for remediation; the ledger stays local until the next CLEAR
- **Provenance/state housekeeping** (RECORDER/INTEGRATOR): → merge to main under Rebecca's authorization (the coordinator does not merge these — only the ledger)

### What to do when state is ambiguous
If the ledger, STATE.md, or a return handoff doesn't tell you what to do next: STOP and ask Rebecca. Do not start digging through GitHub main, replaying conversation history, or launching subagents to explore — that is what burned the fresh coordinator's credits. The ledger + STATE.md + the return handoff should be sufficient; if they're not, the right move is to ask Rebecca for a routing instruction, not to reconstruct the state independently.

---

## Runtime routing directive — 2026-08-21 01:35 EDT (Rebecca-authorized; local metadata)

**Scope:** Routing/governance only. This directive authorizes controlled Codex task-to-task handoff movement and consultation. It does **not** authorize scientific work, scoring, execution, reruns, merges, or gate decisions, and it does not resolve the conflicting durable ball states currently visible in this checkout.

**Single-ball protocol:**
- Exactly one role owns each work item.
- Only a labeled **FORMAL HANDOFF** transfers ownership. Ownership changes when the recipient acknowledges receipt.
- A labeled **CONSULTATION REQUEST** does not transfer ownership. The owner retains the ball; the consulted role answers only within its authority and does not edit, co-author, judge, score, merge, or take over absent a later formal handoff.
- Every formal handoff and acknowledgement is reported to the WORKFLOW COORDINATOR with timestamp, work item/gate, sender, receiver, authoritative branch/SHA, artifact path, blockers, and next expected event.
- Material consultation resolutions become durable only when the owning role captures them in its committed artifact or handoff.
- CRITIC and JUDGE independence remains protected. CRITIC does not co-author work it will review. JUDGE is not consulted about how to make candidate results pass.
- Separate isolated workspaces and branches remain mandatory; no cross-role editing in another role's checkout.
- Automated routing stops and escalates to Rebecca for ambiguity, conflicting SHAs, missing executable inputs, failed gates, protected-seed/scoring boundaries, destructive or external actions requiring approval, and any requested merge.
- O-14, O-15, constitutional law, locked bars, public-repository safety, and Rebecca's sole gate/merge authority remain unchanged.
- Keep collaboration bounded: one formal owner per work item, narrow consultation questions, one authoritative handoff artifact, and no broadcast discussion unless multiple roles need the same notice.

**Rebecca scan-timing clarification (2026-08-21):** Do not run public-safety scans merely on local or pre-merge working state. Run the required scan at the authorization boundary before content is sent to public GitHub by push or merge; merge only when authorized and clean. Because every branch push to this repository is potentially public, a push remains a public-GitHub boundary. Routine local ledger edits and read-only routing checks require no scan.

**L8 backend codenames (Rebecca directive `4de2ace`):** `gofast` = parallel-CPU L8; `GO!` = serial-CPU L8; `go faster` = native-CUDA L8. These are exact, case-sensitive human-facing aliases only. Canonical identities and SHAs/digests remain mandatory; codenames never replace scientific labels, negative classifications, or failure enums and do not change backend status.

**Established-role subagent rule (Rebecca directive `429d462`):** Nobody may spawn or use a subagent to perform another established project role without Rebecca's direct, explicit, per-instance authority. A same-role assisting subagent may help its parent role, which retains authorship, responsibility, the ball, and authority. An advisor-role subagent may provide bounded non-authoritative advice only. Neither exception may manufacture independence, issue/sign authoritative deliverables or verdicts, move the ball, clear a gate, release work, or substitute for the designated persistent role task. Unauthorized surrogate-role output is advisory only; stop reliance, preserve it, report to Coordinator, and route exact committed inputs to the proper persistent role.

**Coordinator-centered automatic handoff routing (Rebecca directive `77d86be`):** Every established role returns each formal completion/remediation/review handoff to WORKFLOW COORDINATOR. Coordinator verifies committed lineage, updates the ledger, auto-routes the exact package to the next authorized persistent role, and records acknowledgement without waiting for a manual “pass the ball.” When Rebecca owns the next decision, Coordinator stops and presents the package. Rebecca interruption overrides immediately. Automation stops on ambiguity, conflicting SHAs, missing executable inputs, unprescribed BLOCK/material choices, protected-seed/scoring/courier boundaries, merge requests, destructive/external actions, or any standing constitutional/public-safety/role-independence stop.

**Authorized protocol-amendment sequence:** ARCHITECT drafts a narrow Codex Collaboration Protocol amendment → CRITIC independently reviews → Rebecca approves or rejects → TASK BUILDER implements approved initialization-file changes and consistency checks → approved amendment is sent to existing role tasks and governs future initialization.

**Shelved work item — L8 native-CUDA backend adoption:** By Rebecca directive recorded at `coordinator/m4-cuda-ready-cpu-l8-directive` @ `d821a5c`, native-CUDA L8 adoption is `SHELVED/INOPERATIVE` as a possible future path. Existing implementation, diagnostic evidence, ARCHITECT design (`5cee6cd…` / `9833f83…`), sibling CRITIC BLOCK reviews (`f79df075…`, supporting; reconciled authoritative `e50d0a40…`) remain preserved historical evidence. No remediation, implementation, qualifying execution, adoption routing, M4 dependency, or merge may resume without Rebecca explicitly reopening the item. The approved parallel-CPU L8 remains the sole authoritative L8 backend for current M4.

**Active priority work item — CUDA-ready M4 harness with authoritative parallel-CPU L8:** Persistent CRITIC independently rereviewed the CF1–CF3 remediation (`architect/m4-model-agnostic-scaffold` @ `ade99fc13dc750b789d254316b9a7dc5de2eae8b`, result `7f3db1f9552cf87de205b0635882402e0e1be5d4`) at `critic/m4-scaffold-cf1-cf3-rereview` @ `deb49bb342a39d3ec25834a4a59b5b21a697d966`, artifact `reviews/critic_m4_scaffold_cf1_cf3_rereview.md`. Verdict: LAW_FIDELITY CLEAR; SUBSTANTIVE CLEAR; combined CLEAR; no findings. CF1–CF3 are closed and preserved regressions remain valid. The ball is with Rebecca for explicit re-release of the exact changed scaffold contract; TASK BUILDER remains held until that decision. No implementation/tests occurred; all scoring, seed, L8-backend, state, and merge holds remain.

**Parallel Principal-directed M4 model-selection work item:** Rebecca's qualification-ladder ruling and size-based local-only model custody are durably recorded at `coordinator/m4-model-selection-ladder-directive` @ `f6cdafe`, artifacts `handoffs/REBECCA_M4_MODEL_SELECTION_QUALIFICATION_LADDER_DIRECTIVE_2026-08-21.md` and `handoffs/REBECCA_LOCAL_ONLY_MODEL_ARTIFACT_CUSTODY_DIRECTIVE_2026-08-21.md`. Persistent TASK BUILDER returned a durable nine-class executor BLOCK at `taskbuilder/m4-model-custody-preflight` @ `60257a3f746cc6338ef8ca8892c165cdcb0f6747`; no download or environment contact occurred. Persistent ARCHITECT acknowledged the BLOCK and custody clarification as additive inputs to its separate isolated ladder amendment and owns deterministic closure of repository IDs, FP8 authority/revisions, custody schema, serving stack, FP8 criteria, context lengths, co-residency measurement, and swap procedure. RECORDER provenance memorialization remains active. No qualification, scoring, seed access, backbone update, merge, or model rung selection is authorized.

**Suspended side project — workflow-efficiency staged change program:** Rebecca approved the exact CRITIC-cleared v1.2 design and five material choices, but Stage 1 implementation returned `SPECIFICATION BLOCK` SB1–SB3 because Stage-1-only role-edit boundaries and an executable validator/fixture contract are absent. Authority remains `coordinator/workflow-efficiency-v1.2-rebecca-approval` @ `2e8dc1c`, artifact `handoffs/REBECCA_WORKFLOW_EFFICIENCY_V1_2_APPROVAL_AND_STAGE1_RELEASE_2026-08-21.md`; design `189a9740837037ca2fd390e0422be8ff89cfcf8f` / `0d64b187f316e2eb5cf48f2ca082cc6f6aa64f27`; CRITIC CLEAR `e61ea24`. By Rebecca directive, all efficiency activity is consolidated in a dedicated isolated side-project task and status is `SUSPENDED/PENDING_REBECCA_RESUME`; active shared ARCHITECT/TASK BUILDER lanes must not continue it. On resume: dedicated ARCHITECT remediation of SB1–SB3 → fresh-context CRITIC → Rebecca re-release → dedicated TASK BUILDER. Stages 2–5 remain held. Immediate workflow priority is M4. No efficiency edits, tests, commits, pushes, review routing, merge, or protected activity is authorized while suspended.

**Separate pending governance item:** The Codex Collaboration Protocol repository amendment has not been formally handed to ARCHITECT. Do not conflate it with the active L8 work item or choose among other conflicting pre-existing durable ball states.

**Persistent task roster (coordination metadata only; never repository authority):**
- WORKFLOW COORDINATOR: `01a022ca-63c4-7651-9521-c89ae81d0e7c`
- ARCHITECT: `01a01d0c-38cc-7a12-a86f-cb9a8b3098b5`
- TASK BUILDER: `01a01cb4-e496-7d92-a475-28dd557b6db8`
- CRITIC: `01a022ca-6677-7c13-97c2-29ce0efda5e7`
- INTEGRATOR: `01a022ca-6942-7c31-a8f5-48049ebecbf3`
- RECORDER: `01a022ca-6c2b-7393-96b5-bf1a6553ca77`
- JUDGE: `01a022ca-6ef9-7271-b089-46ff3ea4e22d`

---
## Current state — updated 2026-08-20 10:22 EDT (role inits FIXED — binding executability obligation added to ARCHITECT, CRITIC, TASK BUILDER; reinitialize ARCHITECT + CRITIC next)

**Ball:** REBECCA — reinitialize the ARCHITECT + CRITIC (fresh sessions with the updated inits). The three role inits now carry a binding executability obligation (PR #100, main `63c0a66e`): same executable-input categories (fixtures, committed artifact pairs, stochastic fixture realizations — committed arrays OR exact RNG/seed/draw-count/shape/construction-order, result schemas, expected digests) across all three.

- **ARCHITECT INIT:** before claiming "deterministic / no implementer invention required," trace every executable input and confirm each is concretely specified. If any is undefined, the spec is NOT deterministic — do not claim it is. (Fixes the v2.6 false-"deterministic" failure — the spec claimed deterministic while the rehearsal fixture, artifact pair, and estimator realizations were undefined.)
- **CRITIC INIT:** check executability end-to-end, not just internal consistency — a non-executable spec is a BLOCK, not a CLEAR. Do NOT CLEAR "deterministic / no implementer invention required" unless executability is independently confirmed. (Fixes the v2.6 false CLEAR.)
- **TASK BUILDER INIT:** the stop discipline (inherent) made explicit with the same categories — reinforcing that the stop is correct behavior, the last defense against a false-"deterministic" spec. The role stays scrapped; the obligation is in place for when Rebecca reinstates it.

**Root-cause addressed:** the v2.6 spiral was caused by the ARCHITECT under-specifying the executable core while claiming "deterministic" and the CRITIC false-CLEARing by checking internal consistency, not executability. The TASK BUILDER's stop was the one correct behavior (it exposed the gaps). The executability obligation on ARCHITECT + CRITIC catches the gap at spec-production and review, not at implementation.

**Still parked (from last night):** the v2.3→v2.6 spec chain + A1/A2/B lifecycle + elaborate benchmark design are superseded by Rebecca's 1,000-rep ruling. Durable verified artifacts retained: §8 code `b139749` + artifact `6d455bb` (6.22%/76.23% + stress instability), calibration parallelism, CRITIC INIT commit-and-push fix, the 1,000-rep ruling, provenance Entries 82–88. No screening, no scoring, no seed exposure, no merger.

**The v2.4 design (what Rebecca approves):** §8.9 deterministic contract — complete trend-verdict algorithms (Spearman ρ, OLS β, bootstrap T = mean_s(β*_s) with stratum-level resampling, lower bound > 0 conjunction, per-seed 0.2 bar preserved); all-cell battery sweep (20 geometries × 240 cells, worst-cell Wilson acceptance conjunction < 0.10, preferred < 0.05); config/serialization/seed manifests (canonical JSON + SHA-256, candidate-blind synthetic seeds); atomic publication; fault injection + exit contracts (20–23/1/70) + synthetic-only crash recovery; apparatus fixtures + 12-case rehearsal; exact TASK BUILDER routing (import b139749, 6d455bb read-only).

**The remediation (7 items, routed ARCHITECT → TASK BUILDER → fresh-context CRITIC → Rebecca):**
1. Verify the exact scoring verdict rule (5-seed-mean vs all-seeds-independently-passing); align spec, harness, power-analysis estimand exactly.
2. Designate the false-kill rate of the actual verdict rule as primary; retain the other as diagnostic. If any failed seed kills the run, 76.23% is unacceptable.
3. Candidate-blind battery-size sweep: minimum queries/windows → operational false-kill below 10% (preferably below 5%).
4. Recompute sensitivity map + (C_min, η) selection only after aggregation + battery size frozen (design only — not run this cycle).
5. Pre-registered equivalence/tie margin for statistically indistinguishable operating points.
6. INSTRUMENT FAILURE defined exclusively through independent apparatus-validity checks; NO reclassification of per-seed statistical failures.
7. Failure-injection tests + diagnostic rehearsal (incomplete output, corruption, nondeterminism, configuration mismatch, crash recovery).

**Consultation package corrected (4 items):** (a) MC uncertainty — more sims narrow CI, don't necessarily raise estimate; (b) aggregation descriptions corrected — both cell-level values are means across 15 per-combo rates (the prior any-seed description was wrong); (c) informative-classification reconciliation flagged (43.22% FK cell called "informative" — ARCHITECT resolves); (d) failure-injection tests routed to ARCHITECT. The package is now a pre-remediation draft; revised design + power analysis + CRITIC ruling return to Rebecca before any G2–G4 decision.

**Key finding driving the remediation:** the false-kill aggregation choice (5-seed-mean 6.22% vs any-seed 76.23%) and the battery size are entangled — if the verdict rule is any-seed-kills, 76.23% is unacceptable and a battery-size sweep is needed to bring it below 10%. The G4 robustness assessment depends on the NF-IMPL-2 aggregation choice (reference point is robust under 5-seed-mean, less so under any-seed).

**Task builder note (2026-08-19):** the local frontier GPT TASK BUILDER stopped three times rather than implement an under-specified spec (serial-calibration spec request; §4.1/§4.2 contradiction; sanitization/termination/identity-validation gaps) — correctly routing each to the ARCHITECT. The ARCHITECT's v1.2 (binding normative code + implementation trace + 14-point test contract) closed every gap. The TASK BUILDER then implemented cleanly (all verification PASS, genuine reproducibility, BF-MP-1 defect fixed). The CRITIC verified claims against the actual diff and results — the false-attestation pattern did not recur.

**Still pending (from the sim results, for the G2–G5 rulings):**
1. The calibration problem: 5-seed-mean false-kill 6.22% (lenient) vs per-seed any-seed 76.23% (harsh, matches scoring bar). Advisor consultation needed.
2. The stress-test instability: selected operating point (0.5, 0.2) did not generalize to misspecified profiles. Advisor consultation needed.
3. NF-IMPL-2: which false-kill aggregation is the G3 input.
4. The proposed per-seed diagnostic data + INSTRUMENT_FAILURE fault-tolerance ruling (draft prepared, not yet ruled).

**Immediate next:** Coordinator routes the §8 artifacts handoff to the TASK BUILDER (item 5: candidate-blind power analysis + sensitivity map per XF-9). This is the first real compute — synthetic simulations (10,000 per parameter combination per the XF-9 protocol), candidate-blind, feeding Rebecca's G2–G5 gate rulings on the [PROPOSED] values. The TASK BUILDER runs a 100-sim validation batch first to measure per-simulation cost before the full run; if genuinely compute-heavy, escalate to Rebecca's local system (sandbox has 2 vCPUs, 7.8 GB RAM, no GPU — but the workload is synthetic scalar computations, likely CPU-sufficient).

**The hybrid build plan (durable routing decision — survives coordinator initialization):**
1. Build the §8 simulation (TASK BUILDER, candidate-blind, 100-sim validation first, full 10,000 run, produces the sensitivity map) + R8 fail-closed hold-out guard as secondary deliverable → feeds Rebecca's G2–G5 rulings
2. Rebecca's G2–G5 gate rulings on the operating point (C_min, η) + the [PROPOSED] values → freezes the parameters
3. Pre-registration freeze → build the M4 harness (the L8 selective-risk homeostat, the three-control panel, the real estimator)
4. Compatibility check (diagnostic-only, O-15): the §8 simulation's synthetic profiles and seeds are fed through the harness's REAL estimator (not the sim's standalone function) to verify the harness produces the same β* on the same inputs. This catches interface bugs before any scoring seed is spent — preventing a bug from breaking a scoring run on Rebecca's system (which under O-14 cannot be rerun). Uses the frozen operating point from the G2–G5 rulings so it's a true dry run of the scoring configuration.
5. Then: scoring authorization (gated on the five downstream M4 gates)

This hybrid (build sim on spec-text estimator, then verify against the harness's real estimator) is Rebecca's design — it catches interface failures in the diagnostic phase where O-15 permits iteration, before the irreversible scoring phase where O-14 forbids reruns.

**L8 spec status:** v2.2 at `c7d7bed` on `architect/l8-instantiation-v2.2-fresh` — CRITIC-cleared (`4ca797c`). The L8 spec is frozen — no further spec-text changes without a signed waiver (P5).

**Active context:** the fresh ARCHITECT (updated init, session `2a9d6a41`) passed the test — the comprehensive P3 sweep was genuine, all nine items fixed, the changelog matched the diff. The prior ARCHITECT's false attestation (`45fd755` on `architect/l8-instantiation-v2`) is preserved as evidence. The ARCHITECT init fix (pre-commit verification, diff self-inspection, attestation integrity, comprehensive-sweep obligations) is confirmed effective.

**Five downstream M4 scoring gates (all retained):** L3 fresh-seed resolution · FWFP closure audit · CRITIC implementation review · Rebecca's tolerance-calibration sign-off · courier-channel scoring authorization. Scoring is NOT authorized.

**Open auditor R-items:** R6, R7-completion, R8 (before M4 harness build), R9. R5 closed (Entry 73).

**Key SHAs:** main `ed7f348` · M4 spec v1.6.2 on main at `90a7e56` · L8 instantiation spec v2.2 (frozen) at `c7d7bed` on `architect/l8-instantiation-v2.2-fresh` · false-attestation evidence at `45fd755` on `architect/l8-instantiation-v2` (do not build on) · cross-family corpus `reviews/l8_crossfamily_review/` (PR #65, Entry 80) · §2 ruling Entry 81.

**Provenance log:** through Entry 81. (Next RECORDER entry: L8 spec v2.2 freeze + §8 artifacts — at the next housekeeping milestone.)

---

## Handoff history (compact — current state overwrites prior; full history in provenance log + git log)

- 2026-08-21 — PERSISTENT CRITIC CLEAR RECEIVED (`deb49bb342a39d3ec25834a4a59b5b21a697d966`): CF1–CF3 closed; exact changed scaffold package → Rebecca for explicit re-release. TASK BUILDER held.
- 2026-08-21 — MODEL CUSTODY PREFLIGHT BLOCK ACKNOWLEDGED (`60257a3f746cc6338ef8ca8892c165cdcb0f6747`): nine executable-input classes added to ARCHITECT's active ladder amendment; local-only size rationale at `f6cdafe`; no download occurred.
- 2026-08-21 — PRINCIPAL DIRECTIVE MEMORIALIZED / PARALLEL HANDOFFS ACKNOWLEDGED (`0c19121`): model-selection ladder → ARCHITECT specification incorporation; RECORDER provenance entry; TASK BUILDER checkpoint-custody/serving preflight only. Scaffold implementation and scoring held.
- 2026-08-21 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: ARCHITECT CF1–CF3 remediation (`ade99fc13dc750b789d254316b9a7dc5de2eae8b`, result `7f3db1f9552cf87de205b0635882402e0e1be5d4`) → persistent CRITIC. CRITIC owns that ball; new CLEAR + Rebecca re-release required.
- 2026-08-21 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: persistent CRITIC LAW_FIDELITY CLEAR + SUBSTANTIVE BLOCK (`3f937c7a03e7ffcc10ac45a84609f5c80cb39a92`) → persistent ARCHITECT for CF1–CF3 only. ARCHITECT owns the ball; preserved closures retained; implementation held.
- 2026-08-21 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: ARCHITECT eight-gap remediation (`de4c661a3d9c6caaa9be53d14bc6035b559aaa70`, result `c33a5e0c94610b47dda783b18af06ca0472edd69`) → persistent CRITIC. CRITIC owns the ball; new CLEAR + Rebecca re-release required; implementation held.
- 2026-08-21 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: durable TASK BUILDER SPECIFICATION BLOCK (`cb43b7a94ef8ea54d6e689398f68cec793707005`) → persistent ARCHITECT for eight-gap deterministic remediation. Exact release-artifact path corrected; ARCHITECT owns the ball; implementation held.
- 2026-08-21 — TASK BUILDER SPECIFICATION BLOCK / DURABILITY CORRECTION: implementation stopped before edits on eight specification gaps. TASK BUILDER retains the ball only to commit/push the unchanged BLOCK handoff; Coordinator then auto-routes it to persistent ARCHITECT. Implementation held.
- 2026-08-21 — REBECCA APPROVAL / FORMAL HANDOFF ACKNOWLEDGED (`81bc799`): Rebecca → persistent TASK BUILDER for exact M4 model-agnostic scaffold-with-stubs implementation. TASK BUILDER owns the ball; real-model activity, non-synthetic execution, scoring, seeds, native-CUDA L8, and merge held.
- 2026-08-21 07:13 — ROUTING IDENTITY CORRECTED / PERSISTENT CRITIC CLEAR RECEIVED: CRITIC (`e76ecb98e80e5bded57afe3d318a32fcfbbfe463`) → WORKFLOW COORDINATOR → Rebecca for the exact scaffold implementation-release decision. No implementation role released.
- 2026-08-21 07:11 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: ARCHITECT RF1A remediation (`2c655fbb1bac6ba419327198062c5230e87c44db`, result `b84f470af415ead5ae36ca01bb1d8e7394e7cc97`) → persistent CRITIC for narrow rereview. CRITIC owns the ball; prior closures preserved; implementation held.
- 2026-08-21 07:09 — ROUTING IDENTITY CORRECTED / AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: persistent CRITIC LAW_FIDELITY CLEAR + SUBSTANTIVE BLOCK (`397d4d622fb9ab4064f4a67411726a10856c3e32`) → persistent ARCHITECT for RF1A only. ARCHITECT owns the ball; BF1/BF4/RF2/RF3 preserved closed; implementation held.
- 2026-08-21 07:05 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: ARCHITECT RF1–RF3 remediation (`9162cff769f7d20b811fb6fbfc5d572869bc42d5`, result `b776083d78e75e4562c76f49166f7ca1224e8807`) → persistent CRITIC for rereview. CRITIC owns the ball; BF1/BF4 preserved closed; implementation held.
- 2026-08-21 06:57 — ROUTING IDENTITY CORRECTED / AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: persistent CRITIC LAW_FIDELITY CLEAR + SUBSTANTIVE BLOCK (`6a56680bcdd8aa3c7460e66aa9ba8c42352db94f`) → persistent ARCHITECT for RF1–RF3 only. ARCHITECT owns the ball; BF1/BF4 preserved closed; implementation held.
- 2026-08-21 06:53 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: ARCHITECT BF1–BF4 remediation (`a5716c18a54f3ef1d47778c158ae63d220c8f76d`, result `697e0343457cd1d0619a34053574b63385204c35`) → persistent CRITIC for rereview. CRITIC owns the ball; implementation held.
- 2026-08-21 06:41 — ROUTING IDENTITY CORRECTED / AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED: persistent CRITIC BLOCK (`528810f403350fd2023c32f83992064e16226cc1`) → persistent ARCHITECT for BF1–BF4 remediation. ARCHITECT owns the ball; TASK BUILDER and implementation held.
- 2026-08-21 06:38 — AUTOMATIC FORMAL HANDOFF ACKNOWLEDGED, M4 model-agnostic scaffold: ARCHITECT (`7afa624093e6cc69c7a5e9f1a4d8dff13f2b729d`, result `09980ffc3b421a8112ed35d653f88213109c1faa`) → persistent CRITIC. Implementation held.
- 2026-08-21 — REBECCA SCOPE CORRECTION ACKNOWLEDGED (`a4d8dc0`): ARCHITECT owns model-agnostic adapter/scaffold and later selection procedure; concrete model choice deferred.
- 2026-08-21 — REBECCA PHASE A APPROVAL / FORMAL HANDOFF ACKNOWLEDGED (`5c078d2`): Rebecca → ARCHITECT for candidate-model/training/exact-binding specification. No implementation/training release.
- 2026-08-21 05:58 — ROUTING IDENTITY CORRECTED / PERSISTENT CRITIC CLEAR RECEIVED: CRITIC (`0790b4a24a868df84739199f1eab7bb16ebe0609`) → WORKFLOW COORDINATOR → Rebecca. BF1–BF7 closed; binding `PROVISIONAL_BLOCKED`; TASK BUILDER held.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED, M4 BF7 executable remediation: ARCHITECT (`e5edb1e804cc4a6553507c98140fa9fa49586a0d`, result `e7419633f34c7eebadfe3cea33c84aff3883a4aa`) → persistent CRITIC. TASK BUILDER held.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED after persistent CRITIC BLOCK: CRITIC (`b6b12dcfedaaa25c23788b80d8adef40718f35ef`) → ARCHITECT for BF7 only. BF1–BF6 closed; TASK BUILDER held.
- 2026-08-21 — CORRECTION/FORMAL HANDOFF ACKNOWLEDGED: spawned-review CLEAR `9b8083…` is non-authoritative for role independence. ARCHITECT package `baa8ce5…` / `bd38e6a…` transferred to persistent CRITIC for independent rereview. TASK BUILDER held.
- 2026-08-21 — SUPERSEDED ROUTING RECORD: spawned reviewer reported CLEAR at `9b8083bbc1bd5a2020770ab2e4bc6acd955a59af`; later identified as non-authoritative for persistent-role independence. It does not place the ball with Rebecca or release TASK BUILDER.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED after revised M4 v1.1 combined BLOCK: CRITIC (`4e194ddcec819f1f96c75b36ad2fb2cebbe9f385`) → ARCHITECT for BF6–BF7 only. BF1–BF5 closed; TASK BUILDER held.
- 2026-08-21 — REBECCA DIRECTIVE (`d821a5c`): shelf native-CUDA L8; retain parallel-CPU L8 as authoritative; redesign M4 as CUDA-ready for AI-model execution with a fail-closed CPU-L8 boundary. ARCHITECT authority amended; implementation held.
- 2026-08-21 — L8 native-CUDA review identity resolved: `f79df075…` and `e50d0a40…` are sibling BLOCK reviews from parent `5cee6cd…`; `e50d0a40…` is the reconciled authoritative return, `f79df075…` supporting evidence. Item remains held at Coordinator.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED after M4 Phase A combined BLOCK: CRITIC (`4a581cb5e793579e5c98478e36cc9d5e8210ff43`) → ARCHITECT for BF1–BF5 remediation. Phase B/TASK BUILDER held.
- 2026-08-21 — REBECCA SUSPENSION: Workflow Efficiency moved to a dedicated isolated side-project task as `SUSPENDED/PENDING_REBECCA_RESUME`; SB1–SB3 preserved; active priority returns to M4.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED after Rebecca approval: Rebecca (`2e8dc1c`) → TASK BUILDER for Workflow Efficiency Stage 1 only (P1/P7). Stages 2–5 remain implementation-held.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED, L8 native-CUDA adoption: TASK BUILDER (`8251d95b31107f4a710463fb0574b5bd33a44325`) → ARCHITECT for deterministic prospective specification. Diagnostic evidence remains proposed/inoperative; route stops at Rebecca after CRITIC.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED, M4 harness CUDA-L8 Phase A: ARCHITECT (`60e515c4b14160d282c5ba0b7b6b8c2a8f63dd54`, design `76fb37ee359abf2539131c854befe0f695178036`) → CRITIC. CRITIC owns review; Phase B remains `PROVISIONAL_BLOCKED`.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED, M4 harness CUDA-L8 contract-first design: Rebecca (`b32992e`) → ARCHITECT. ARCHITECT owns Phase A; final L8 implementation reconciliation is mandatory before M4 implementation release.
- 2026-08-21 — CRITIC CLEAR FORMAL RETURN, Workflow Efficiency v1.2: CRITIC (`e61ea24`) → Rebecca for the exact package and five material choices. TASK BUILDER remains held for efficiency work pending Rebecca.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED, Workflow Efficiency v1.2 BF8–BF10 remediation: ARCHITECT (`189a9740837037ca2fd390e0422be8ff89cfcf8f`, design `0d64b187f316e2eb5cf48f2ca082cc6f6aa64f27`) → CRITIC. CRITIC owns the efficiency ball.
- 2026-08-21 02:42 — FORMAL HANDOFF ACKNOWLEDGED after Workflow Efficiency v1.1 combined BLOCK: CRITIC (`9e34c63bf8d7ec2ccbf21240f686d194f0600ddf`) → ARCHITECT for BF8–BF10 only. L8 remains separately active.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED, Workflow Efficiency v1.1 BF1–BF7 remediation: ARCHITECT (`6d8f6b99d3fc05cbb3de8d7885d0470fdd6d5536`) → CRITIC. CRITIC owns the efficiency ball; all proposals remain inoperative.
- 2026-08-21 02:26 — FORMAL HANDOFF ACKNOWLEDGED after Workflow Efficiency v1 combined BLOCK: CRITIC (`0c6fac88424eaee6966525d45fb7385686a197d7`) → ARCHITECT for minimal BF1–BF7 remediation. L8 TASK BUILDER work remains separately active.
- 2026-08-21 02:17 — FORMAL HANDOFF ACKNOWLEDGED, Workflow Efficiency v1: ARCHITECT (`aab33625b38319a6bad30f7dc71db323cbdda62d`) → CRITIC for independent P1–P10 review. CRITIC owns the efficiency ball; all text remains inoperative.
- 2026-08-21 — FORMAL HANDOFF ACKNOWLEDGED after Rebecca approval/release: Rebecca (`50260d3`) → TASK BUILDER for L8 GPU v1.5 implementation and exactly two contract-permitted executions. TASK BUILDER owns the L8 ball; all stated holds remain binding.
- 2026-08-21 02:06 — FORMAL HANDOFF ACKNOWLEDGED, workflow-efficiency staged change program: WORKFLOW COORDINATOR (`coordinator/efficiency-change-program-intake` @ `67280df`) → ARCHITECT. ARCHITECT owns this separate ball; next is a staged prospective design package for fresh-context CRITIC.
- 2026-08-21 — Rebecca approved the efficiency baseline proposals for a staged ARCHITECT → CRITIC → Rebecca design program, with TASK BUILDER only after exact approval. Formal ARCHITECT transfer is blocked on §5 P1 repository-first intake; Coordinator holds this separate ball pending Rebecca's publication instruction.
- 2026-08-21 01:57 — CRITIC CLEAR FORMAL HANDOFF, L8 GPU v1.5: CRITIC (`e0aad1dabde9546e0074a7a375135eb92ee2072a`) → Rebecca for sole amendment approval/re-release decision. BF1–BF5 closed; TASK BUILDER and executions remain held pending Rebecca.
- 2026-08-21 — FORMAL HANDOFF recorded for the separate read-only workflow-efficiency baseline audit: Rebecca → EFFICIENCY EVALUATOR. L8 ownership and holds unaffected; evaluator task ID excluded from repository metadata.
- 2026-08-21 01:50 — FORMAL HANDOFF ACKNOWLEDGED, L8 GPU v1.5 BF1–BF5 remediation: ARCHITECT (`e05550f494b2c6dffb2ea9645067395beaf56fe1`) → CRITIC for independent rereview. CRITIC owns the L8 ball; TASK BUILDER and execution held.
- 2026-08-21 01:42 — FORMAL HANDOFF ACKNOWLEDGED after CRITIC combined BLOCK: CRITIC (`635e56f63ce61be537cfdfa026f24adf17e91b3a`) → ARCHITECT for minimal BF1–BF5 remediation. ARCHITECT owns the ball; TASK BUILDER and execution held.
- 2026-08-21 01:38 — FORMAL HANDOFF ACKNOWLEDGED, L8 GPU v1.5 executability remediation: ARCHITECT (`b402fe07570843f3d234938a80690820dde2f849`) → CRITIC. CRITIC owns the ball; TASK BUILDER held; awaiting committed independent review and formal return handoff.
- 2026-08-21 01:35 — Rebecca authorized the runtime single-ball Codex collaboration protocol and persistent task roster as local routing metadata. No formal handoff issued; conflicting durable ball states remain unresolved; awaiting Rebecca's instruction before routing the protocol-amendment work item to ARCHITECT.
- 2026-08-20 10:22 — role inits FIXED (PR #100, main 63c0a66e): binding executability obligation added to ARCHITECT, CRITIC, TASK BUILDER (addresses v2.6 false-deterministic + false-CLEAR). Reinitialize ARCHITECT + CRITIC next; TASK BUILDER init updated, role stays scrapped.
- 2026-08-20 01:49 — ARCHITECT + TASK BUILDER SCRAPPED (proved faulty/fallible); awaiting Rebecca's routing instruction
- 2026-08-20 01:38 — REBECCA RULING (REBECCA_L8_1000_REP_FEASIBILITY_AUTHORIZATION, main d6bc5c9+d08cb7e): 1,000-rep parallel feasibility diagnostic replaces the v2.6 60-rep benchmark
- 2026-08-20 01:12 — Rebecca APPROVED v2.6 (A1/A2 + parallel benchmark); routing to TASK BUILDER (taskbuilder/l8-g2g4-diagnostic-remediation, from e2bd824) [NOTE: superseded by the 1,000-rep ruling]
- 2026-08-20 01:10 — v2.6 CRITIC CLEAR in-repo (88e238b on critic/l8-g2g4-v2.6-review); INIT fix confirmed working (CRITIC committed v2.5.1 + v2.6 reviews in-repo); ready for Rebecca's v2.6 approval (A1/A2 + parallel benchmark)
- 2026-08-20 01:05 — L8 spec v2.6 landed (e2bd824, §8.11): A1/A2/B commit lifecycle (no self-referential SHA) + parallel-only benchmark + parallel repeatability (no serial). CRITIC reviewing v2.6.
- 2026-08-20 00:48 — v2.5.1 CRITIC CLEAR in-repo (1338d28 on critic/l8-g2g4-v2.5.1-rereview); INIT fix worked (CRITIC committed+pushed); v2.5/v2.5.1 design ready for Rebecca's feasibility-gate decision (Commit A + benchmark first)
- 2026-08-20 00:45 — CRITIC INIT fix MERGED (PR #92, edf7a78): binding commit-and-push obligation added (reviews must be in-repo on a critic/ branch, not attachments). One-time handoff sent to current CRITIC to commit its v2.5.1 review.
- 2026-08-20 00:37 — v2.5 CRITIC BLOCK (P6 provenance pointers: L8 line 26→28, L14 line 40→42); ARCHITECT corrected to v2.5.1 (081df58); ball back to CRITIC re-review. v2.5 substance unchanged; screening still withdrawn.
- 2026-08-20 00:29 — L8 spec v2.5 landed (5209f33, §8.10, 2nd STOP closed); 2,000-rep screening authorization WITHDRAWN pending feasibility gate (9.6M cell reps / up to 48B bootstrap replicates); CRITIC reviewing v2.5
- 2026-08-20 00:26 — RECORDER+INTEGRATOR backlog catchup MERGED (PR #88, eead511): provenance Entries 82-88 + STATE.md reconciliation. Provenance log now through Entry 88; STATE.md current to v2.4 approval.
- 2026-08-20 00:11 — Rebecca APPROVED the v2.4 diagnostic method + AUTHORIZED 2,000-rep screening; routing to TASK BUILDER (taskbuilder/l8-g2g4-diagnostic-remediation) [NOTE: screening authorization later WITHDRAWN by v2.5 feasibility gate]
- 2026-08-20 00:10 — L8 spec v2.4 (4463cbc) CRITIC-cleared; all 7 §8.9 subsections deterministic; bootstrap > 0 doesn't replace 0.2 bar; INSTRUMENT FAILURE apparatus-only; awaiting Rebecca's approval + 2,000-rep screening authorization
- 2026-08-20 00:06 — TASK BUILDER stopped on v2.3 (diagnostic contract under-specified); ARCHITECT resolved with v2.4 (4463cbc) + CRITIC handoff; v2.3 TASK BUILDER handoff marked superseded
- 2026-08-19 23:56 — ARCHITECT remediation design v2.3 COMPLETE (2819bf7); TASK BUILDER implementing locally
- 2026-08-19 23:42 — Rebecca directed G2–G4 remediation (7 items); G2–G4 NOT frozen; advisor package corrected; routing ARCHITECT → TASK BUILDER → CRITIC → Rebecca. No stress rerun, no scoring, no seed exposure.
- 2026-08-19 23:31 — L8 power analysis rerun COMPLETE (6d455bb); reproduces prior numbers; 7.51x speedup; both false-kill aggregations + stress-test instability unchanged; preparing advisor consultation
- 2026-08-19 22:53 — local rerun authorized + running on Rebecca's executor (b139749, --full --workers 16)
- 2026-08-19 22:52 — calibration parallelism implementation CRITIC-cleared (b139749); BF-MP-1 defect genuinely fixed; local rerun prompt prepared
- 2026-08-19 22:46 — TASK BUILDER implemented spec v1.2 (b139749); all verification PASS (genuine reproducibility, 14-point test contract, multicore confirmed)
- 2026-08-19 22:28 — calibration parallelism spec v1.2 (6979378) CRITIC-cleared; all three failure-path gaps closed; awaiting Rebecca's approval (should be the last amendment)
- 2026-08-19 22:24 — ARCHITECT closed failure-path gaps (spec v1.2, 6979378); CRITIC re-review CLEAR
- 2026-08-19 22:12 — TASK BUILDER stopped on sanitization/termination/identity-validation gaps; routed to ARCHITECT
- 2026-08-19 22:05 — calibration parallelism spec v1.1 (b4419f9) CRITIC-cleared + Rebecca-approved; routing to TASK BUILDER for implementation. Option 1 (CalibrationWorkerError) chosen.
- 2026-08-19 22:01 — ARCHITECT resolved §4.1/§4.2 contradiction (spec v1.1, b4419f9); CRITIC re-review CLEAR
- 2026-08-19 21:55 — TASK BUILDER stopped on contradiction (§4.1 no-catch vs §4.2 failure-record identity); routed to ARCHITECT
- 2026-08-19 21:48 — calibration parallelism spec CRITIC-cleared (a087654); awaiting Rebecca's approval. 10/10 design decisions resolved.
- 2026-08-19 21:42 — ARCHITECT calibration parallelism spec v1 (90d8835)
- 2026-08-19 21:05 — TASK BUILDER (local frontier GPT) found serial calibration bottleneck; routed spec request (10 design decisions) — specify-vs-produce boundary held correctly
- 2026-08-19 21:00 — §8 multiprocessing CRITIC BLOCK (BF-MP-1: worker results discarded, reference not parallelized, vacuous reproducibility check)
- 2026-08-19 20:35 — §8 sim completed (selected (0.5, 0.2); 5-seed-mean FK 6.22%, any-seed FK 76.23%; stress-test unstable; write-order defect in artifact)
- 2026-08-19 15:28 — §8 stress-test extension CRITIC-cleared (ad3a405); §8 code fully cleared; ball to Rebecca for local run
- 2026-08-19 15:20 — TASK BUILDER stress-test extension (full 2D sensitivity map + selection on misspecified profiles, NF-IMPL-4 scope extension)
- 2026-08-19 13:16 — §8 code CRITIC-cleared (remediation re-review, 0da3953); ball to Rebecca for local run. NF-IMPL-2 (false-kill aggregation ruling) + NF-IMPL-4 (partial stress-test) flagged to Rebecca.
- 2026-08-19 12:53 — TASK BUILDER §8 remediation (BF-IMPL-1 + NF-IMPL-1/2/3)
- 2026-08-19 12:48 — CRITIC §8 implementation review BLOCK (BF-IMPL-1 misspec stress-test absent + 3 non-blocking)
- 2026-08-19 12:46 — TASK BUILDER §8 validation complete (estimator verified, R8 guard, 5.6hr full run → Rebecca local)
- 2026-08-19 11:48 — ball passed coordinator → TASK BUILDER (§8 power analysis; 100-sim validation first)
- 2026-08-19 11:28 — first CRITIC CLEAR (ledger push+merge, first use of the coordinator ledger system). L8 spec v2.2 frozen. Hybrid build plan added to ledger.
- 2026-08-19 11:12 — ball passed fresh ARCHITECT → CRITIC (v2.2 fresh re-review); ledger updated locally
- 2026-08-19 10:51 — coordinator handoff checkpoint published (PR #68); fresh ARCHITECT initialized with updated init to test the false-attestation fix
- 2026-08-19 10:40 — CRITIC v2.2 re-review BLOCKed (false attestation: 8/9 items unfixed, changelog claimed all fixed); prior ARCHITECT retired; ARCHITECT init updated (PR #67)
- 2026-08-19 10:17 — ARCHITECT v2.2 P3 sweep (false attestation)
- 2026-08-19 01:00 — ARCHITECT v2.1 (three fixes); CRITIC re-review BLOCKed (two residual P3 tolerances)
- 2026-08-19 00:49 — first cross-family review corpus custody (Entry 80, PR #65); §2 construct-interpretation ruling (Entry 81, PR #66)
