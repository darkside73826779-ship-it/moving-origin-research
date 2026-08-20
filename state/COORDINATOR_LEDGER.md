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
## Current state — updated 2026-08-19 22:05 EDT (calibration parallelism spec v1.1 CRITIC-cleared + Rebecca-approved; routing to TASK BUILDER)

**Ball:** TASK BUILDER (local frontier GPT) — implementing the approved calibration parallelism spec v1.1 (`b4419f9` on `architect/l8-calibration-parallelism-spec`; CRITIC-cleared; Rebecca-approved). Option 1: identity-carrying picklable `CalibrationWorkerError` (worker wraps and re-raises; parent reads identity from the exception, no re-execution).

**After implementation:** CRITIC implementation review (code matches spec? genuine reproducibility?) → Rebecca authorizes → rerun locally at full parallelism (`python diagnostics/l8_power_analysis.py --full --workers N`) → complete artifact → G2–G5 gate rulings (with advisor consultation).

**Task builder note (2026-08-19):** the local frontier GPT TASK BUILDER has twice stopped rather than implement an ambiguous/contradictory spec (the serial-calibration spec request; the §4.1/§4.2 contradiction) — correctly routing design decisions to the ARCHITECT instead of inferring. This is the specify-vs-produce boundary working, and it's the opposite of the false-attestation pattern. The implementation handoff carries emphatic verification obligations (verify each edit, inspect git diff, changelog tied to the diff, genuine reproducibility on the consumed parallel output).

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
