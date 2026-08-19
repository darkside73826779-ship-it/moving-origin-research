# WORKFLOW COORDINATOR LEDGER

**Purpose:** Working routing state — who has the ball, what handoff is in flight, the immediate next action, active role sessions. Maintained locally by the coordinator, pushed to GitHub at each CRITIC CLEAR (not on every ball-pass — git operations are batched to the clear). A fresh coordinator reads this first to see where the ball is, then STATE.md for durable context.

**Discipline:** Update locally in-place on every ball-pass. Push to GitHub only at CRITIC CLEAR milestones, alongside the RECORDER entry and STATE.md reconciliation. The local checkout is the working copy; GitHub is the durable checkpoint.

---

## Current state — updated 2026-08-19 15:28 EDT (§8 code fully CRITIC-cleared; ready for Rebecca's local run)

**Ball:** REBECCA — the §8 power analysis code (including the full misspec stress-test extension) is fully CRITIC-cleared (`ad3a405` on `critic/l8-stress-test-extension-rereview`). Code at `cbe4dfb` on `taskbuilder/l8-power-analysis` (1435 lines). Rebecca runs locally:
```
git fetch origin && git checkout taskbuilder/l8-power-analysis
python diagnostics/l8_power_analysis.py --full
```
Use `--stress-test-sims 2000` for the reduced stress-test (~8h total instead of ~17h). Output: `diagnostics/l8_power_analysis_results.json` (relative path, ~200 KB). Produces the reference sensitivity map + misspecification stability report feeding Rebecca's G2–G5 gate rulings.

**Still pending Rebecca's decisions:**
1. **NF-IMPL-2 (false-kill aggregation):** which is the G3-escalation input — 5-seed mean (lower) or per-seed any-seed (higher, matches scoring bar)? Decide when you see both numbers in the output.
2. **NF-EXT-1 (trivial, optional):** a bare invocation (no `--full`) triggers the full stress-test. You use `--full`, so this doesn't affect you. Could be gated optionally if desired.

**After the local run:** Rebecca's G2–G5 gate rulings on the (C_min, η) operating point + the [PROPOSED] values → pre-registration freeze → §12 step 4 (L7/L10 delta review) → M4 harness build (L8 homeostat, three-control panel, real estimator) → compatibility check (sim's synthetic profiles through the harness's real estimator, diagnostic-only, O-15) → scoring authorization (gated on the five downstream M4 gates).

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
