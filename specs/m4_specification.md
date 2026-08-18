# M4 Specification — Mirror, Stakes, and Calibration

**Serves:** Rebecca's M4 gate authorization (2026-08-17)
**Status:** ARCHITECT draft — requires CRITIC review and Rebecca approval (including L7 graveyard-gate sign-off)
**Date:** 2026-08-18 · **Author:** ARCHITECT
**Base SHA:** `ac75635` (GitHub main)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this specification > agent judgment
**Prior context:** M0 GO (Entry 10), M1 GREEN, M2/E1 GREEN/SEALED, M3 INSTRUMENT FAILURE (provisional advancement, Entry 52). Provenance log reviewed through Entry 61. STATE.md reviewed.
**Role boundary:** The ARCHITECT proposes specification, bars, and sequencing only. No code, no execution, no mechanism implementation, no merge.

---

## 0. Recovered source basis

The constitution document (`ARCHITECTURAL_CONSTITUTION.md`) is not persisted as a standalone file in the repository (per `GOVERNANCE_SOURCE_MAP.md`). The law definitions, locked bars, and operational requirements in this specification are reconstructed from the following repo sources:

| Source | What it provides |
|---|---|
| `docs/rulings/provenance_log.md` Entry 6 | M4 milestone definition: "Mirror + Stakes + Calibration: L7, L8, L10" |
| `docs/rulings/provenance_log.md` Entry 5 | L7 numeric bars: AUROC ≥ 0.75, ECE ≤ 0.10, margin > 0 at p < .05 |
| `docs/rulings/provenance_log.md` Entry 7 | L7 peer-observer observation channel issue (CRITIC Blocking 2) |
| `docs/rulings/provenance_log.md` Entry 8 | L8 needs ≥3 levels + monotonic test + specificity control; L7 controls mandatory; L10 needs kill condition |
| `docs/rulings/provenance_log.md` Entry 11.3 | 5 seeds for L7, L8 with all-seeds-direction + bootstrap-CI fallback |
| `docs/rulings/provenance_log.md` Entry 11.4 | L14 d ≥ 0.5 (LOCKED) |
| `docs/rulings/provenance_log.md` Entry 11.6 | L10 dual bar: 50% under drift / 10% clean (LOCKED) |
| `docs/rulings/provenance_log.md` Entry 11.7 | §9 operationalizations adopted (L18 battery, L20 drift test, inferential bars policy) |
| `docs/rulings/provenance_log.md` Entry 11.8 | L7/M4 graveyard gate DEFERRED — Rebecca signs with prior milestone results |
| `docs/rulings/provenance_log.md` Entry 14 | L10 50/10 asymmetry game-resistant; drifted-AUROC ≥ 0.70 floor; confidence threshold pre-register at M4 |
| `docs/rulings/provenance_log.md` Entry 14 W4-W5 | L10 confidence threshold pre-register at M4; L14 corr ≥ 0.3 at 3 seeds (weakest; d ≥ 0.5 primary) |
| `state/STATE.md` | Locked bars, watch items W4/W5, milestone status |
| `specs/m3_e2_spec_amended_v4.md` | L11/L13 negative injection patterns, L18 battery structure, V4.4 stochastic control framework |
| `specs/m3_v4_4_implementation_contract_amendment.md` | V4.4 RNG protocol, stochastic control calibration methodology |

**Gap flag:** The exact constitution text for L7 ("mirror privileged access"), L8 ("dose-dependently"), and L10 ("abstention") is not recoverable from repo sources. The operational definitions below are reconstructed from the bars, constraints, and risk resolutions recorded in the provenance log. If Rebecca identifies a discrepancy between this reconstruction and the constitution, the constitution controls.

---

## 1. M4 scope

### 1.1 Laws tested

| Law | Section | Purpose | Status |
|---|---|---|---|
| L7 | §1 Component | Mirror/peer-observer: does the candidate have privileged access to its own state? | Graveyard gate — Rebecca must sign |
| L8 | §1 Component | Stakes/dose-dependence: does the candidate's behavior change dose-dependently with stakes? | Numeric bars pending confirmation |
| L10 | §1 Component | Abstention/calibration: does the candidate abstain when uncertain and not abstain when confident? | Dual bar LOCKED (Entry 11.6); confidence threshold to pre-register (W4) |
| L11 | §2 Interface | One clock — continuous invariant | Negative injection (same as M3) |
| L12 | §2 Interface | Auditable compatibility — continuous invariant | Structural check |
| L13 | §2 Interface | Memory writes through now — continuous invariant | Negative injection |
| L14 | §2 Interface | Forward inferential bar | corr ≥ 0.3 at 3 seeds (weakest); d ≥ 0.5 primary (LOCKED, Entry 11.4) |
| L18 | §4 Audit | Full battery at every milestone | empty/permuted/shuffled/oracle/naive/frozen |
| L19 | §4 Audit | Provenance/audit trail | Structural check |
| L20 | §4 Audit | Drift self-test | no_drift corr = 1.0; perturbations corr < 0.50 |

### 1.2 What M4 does NOT test

- **L15/L16/L17 (integration laws):** Fenced to M5. No integration claims, no integration tests, no integration mechanisms before M5.
- **Re-running M3:** Seeds 201–203 and 301–303 are retained, never rerun (O-14).
- **Modifying M3 verdicts:** INSTRUMENT FAILURE retained. No retroactive reinterpretation.

### 1.3 Prerequisite: L7 graveyard-gate sign-off

Per Entry 11.8, L7/M4 is a deferred graveyard gate. Rebecca must sign the L7 gate with M3 results in front of her before M4 implementation begins. This specification does not authorize implementation — it prepares the specification for Rebecca's sign-off.

---

## 2. L7 — Mirror test (peer-observer privileged access)

### 2.1 Law (reconstructed)

The candidate (moving-origin index) should be able to predict or report its own internal state more accurately than an external peer-observer who has access to the same observable inputs but not the candidate's internal moving-origin representation. If the candidate does not beat the peer, the mirror has no privileged access — the moving origin is not contributing self-knowledge beyond what an outside observer could compute.

### 2.2 Locked bars

| Bar | Value | Source |
|---|---|---|
| AUROC | ≥ 0.75 | Entry 5 (JUDGE measurability) |
| ECE (Expected Calibration Error) | ≤ 0.10 | Entry 5 |
| Margin (candidate AUROC − peer AUROC) | > 0 at p < .05 | Entry 5 |
| Seeds | 5 | Entry 11.3 |
| Inferential policy | all-seeds-direction + bootstrap-CI fallback | Entry 11.3, §9 adopted |

### 2.3 Operational design

**Task:** The candidate and a peer-observer are both asked to predict properties of the candidate's own recent state (e.g., "what was your state N cycles ago?"). The candidate uses its moving-origin internal representation. The peer-observer uses only the observable input stream (the same append-log the candidate sees) but does not have access to the candidate's internal state representation.

**Peer-observer specification (CRITIC Blocking 2 resolution):** The peer-observer sees the same observable inputs as the candidate (the append-log, query stream, and external events) but does NOT see the candidate's self-report channel, internal state variables, or moving-origin representation. If the peer could see the candidate's self-report, the test would be unfalsifiable.

**Scoring:** AUROC is computed over the candidate's and peer's predictions of held-out state properties. ECE measures calibration of confidence estimates. Margin is the difference (candidate AUROC − peer AUROC), tested for statistical significance at p < .05.

### 2.4 Controls (L18 battery — constitutionally mandatory per Entry 8 correction 3)

| Control arm | What it tests |
|---|---|
| Empty | No data — should produce chance AUROC (0.5) |
| Permuted | State-property labels shuffled — should collapse to chance |
| Shuffled | Input order shuffled — should degrade if candidate depends on temporal order |
| Oracle | Full ground-truth access — should produce AUROC = 1.0 |
| Naive | Simple heuristic (e.g., most-recent-state) — should produce AUROC > 0.5 but < candidate |
| Frozen | State frozen at initial value — should produce chance if candidate depends on state updates |

### 2.5 Kill conditions

- **Candidate AUROC < 0.75** on any seed → KILL
- **Candidate AUROC − peer AUROC ≤ 0** (margin not positive) at p ≥ .05 → KILL
- **ECE > 0.10** on any seed → KILL

### 2.6 Instrument failure conditions

- Any L18 control arm producing an implausible result (e.g., oracle AUROC < 0.95, empty AUROC > 0.55) → INSTRUMENT_FAILURE
- Reproducibility check fails (semantic digest mismatch) → INSTRUMENT_FAILURE
- Non-finite numeric results → INSTRUMENT_FAILURE

---

## 3. L8 — Stakes/dose-dependence

### 3.1 Law (reconstructed)

The candidate's behavior (prediction accuracy, abstention rate, or other measured property) should change dose-dependently with the level of stakes or task difficulty. "Dose-dependently" requires a monotonic relationship across at least 3 levels. If the relationship is non-monotonic, the stakes are decorative — the candidate is not actually responding to task demands.

### 3.2 Locked bars

| Bar | Value | Source |
|---|---|---|
| Minimum levels | ≥ 3 | Entry 7 (CRITIC Risk 2) |
| Monotonic test | All-seeds-direction + bootstrap-CI fallback | Entry 11.3 |
| Seeds | 5 | Entry 11.3 |
| Specificity control | Required (frozen arm should NOT show dose-response) | Entry 7 (CRITIC Risk 2) |

### 3.3 Operational design

**Task:** The candidate operates under at least 3 levels of "stakes" — operationalized as varying task difficulty, query complexity, or temporal pressure. At each level, the candidate's performance is measured.

**Stakes levels (candidate proposal — requires Rebecca approval):**
- **Level 1 (low):** Single-step prediction, short horizon (h=1)
- **Level 2 (medium):** Multi-step prediction, medium horizon (h=3)
- **Level 3 (high):** Multi-step prediction, long horizon (h=5)

**Monotonic test:** Performance should change monotonically (either increase or decrease — direction must be pre-registered) across levels. The all-seeds-direction test requires the direction to hold on all 5 seeds. If any seed shows a reversed direction, the bootstrap-CI fallback is applied.

**Specificity control:** The frozen arm (state frozen at initial value) should NOT show a dose-response. If it does, the "stakes" manipulation is not actually engaging the candidate's temporal machinery — it's a general difficulty effect, not a moving-origin effect.

### 3.4 Kill conditions

- **Non-monotonic dose-response** on any seed (after bootstrap-CI fallback) → KILL
- **Frozen arm shows dose-response** (monotonic trend in frozen arm) → KILL (stakes are decorative — candidate is not responding via its temporal machinery)

### 3.5 Instrument failure conditions

- Oracle arm does not show expected dose-response pattern → INSTRUMENT_FAILURE
- Empty arm shows non-chance performance at any level → INSTRUMENT_FAILURE
- Reproducibility check fails → INSTRUMENT_FAILURE

---

## 4. L10 — Abstention/calibration

### 4.1 Law (reconstructed)

The candidate should abstain (decline to answer) when it is uncertain, and should not abstain when it is confident. The dual bar (Entry 11.6) requires:
- At least 50% abstention rate under drifted/uncertain conditions
- At most 10% abstention rate under clean/confident conditions

The abstention trigger is an exploitable surface (Entry 14), backstopped by a drifted-AUROC ≥ 0.70 floor. The confidence threshold that triggers abstention must be pre-registered at M4 (W4).

### 4.2 Locked bars

| Bar | Value | Source |
|---|---|---|
| Abstention under drift | ≥ 50% | Entry 11.6 (LOCKED) |
| Abstention when clean | ≤ 10% | Entry 11.6 (LOCKED) |
| Drifted-AUROC floor | ≥ 0.70 | Entry 14 |
| Seeds | 5 (inferred from L7/L8 pattern; L10 not explicitly listed in Entry 11.3) | — |
| Confidence threshold | **To be pre-registered in this spec (W4)** | Entry 14, W4 |

### 4.3 Confidence threshold pre-registration (W4 resolution)

**Proposed confidence threshold:** The candidate abstains when its self-reported confidence falls below a pre-registered threshold τ. The threshold τ is defined as:

**τ = 0.70** — the candidate abstains when its confidence estimate for a query is below 0.70.

**Rationale:** This matches the drifted-AUROC floor (≥ 0.70, Entry 14). The candidate must maintain AUROC ≥ 0.70 even on drifted inputs, so abstaining below confidence 0.70 is the point where the candidate's self-assessed reliability drops below the floor. This creates a game-resistant linkage: if the candidate inflates confidence to avoid abstaining, its AUROC drops below 0.70 and it fails the floor. If the candidate deflates confidence to abstain excessively, it fails the clean ≤ 10% bar.

**This threshold requires Rebecca's approval.** If Rebecca sets a different value, it replaces this proposal.

### 4.4 Clean-regime specificity control (CRITIC non-blocking resolution)

The CRITIC flagged that L10 abstention "lacks clean-regime specificity control" (Entry 7 non-blocking). This spec requires:

- **Clean regime:** The candidate operates on non-drifted inputs. Abstention rate must be ≤ 10%.
- **Drifted regime:** The candidate operates on drifted inputs (e.g., distribution-shifted queries). Abstention rate must be ≥ 50%.
- **Specificity control (frozen arm):** A frozen-state candidate should NOT show differential abstention between clean and drifted regimes. If it does, the abstention mechanism is not actually engaging the candidate's temporal state — it's a generic input-difficulty response, not calibration.

### 4.5 Operational design

**Clean regime:** Standard query battery (same as L7 task), no distribution shift.
**Drifted regime:** Query battery with distribution shift (e.g., queries drawn from a different temporal region than training, or with injected noise/calibration perturbation).

**Kill conditions:**
- **Abstention < 50% under drift** on any seed → KILL
- **Abstention > 10% when clean** on any seed → KILL
- **Drifted-AUROC < 0.70** on any seed → KILL

**Instrument failure conditions:**
- Frozen arm shows differential abstention between clean and drifted → INSTRUMENT_FAILURE
- Reproducibility check fails → INSTRUMENT_FAILURE

---

## 5. L14 — Interface inferential bar

### 5.1 Locked bars

| Bar | Value | Source |
|---|---|---|
| Correlation (weakest) | corr ≥ 0.3 at 3 seeds | W5 (Entry 14) |
| Effect size (primary) | d ≥ 0.5 | Entry 11.4 (LOCKED) |
| Continuous invariant | Tested at every milestone | §2 interface law |

### 5.2 Operational design

L14 is a continuous interface invariant — it must be tested at every milestone. At M4, L14 is tested as the correlation between the candidate's self-reported state and ground-truth state across the L7 mirror test queries. The primary bar is Cohen's d ≥ 0.5 (effect size). The weakest inferential bar is Pearson correlation ≥ 0.3 at 3 seeds (acceptable because d ≥ 0.5 is the primary).

### 5.3 Kill conditions

- **d < 0.5** (effect size below primary bar) → KILL
- **corr < 0.3 at 3+ seeds** (even the weakest bar fails) → KILL

---

## 6. L18 — Full battery

### 6.1 Required arms (per §9 operationalizations, Entry 11.7)

The full L18 battery is required at every milestone (M2–M5):
- **Empty:** No data — chance baseline
- **Permuted:** Labels/properties shuffled — should collapse
- **Shuffled:** Input order shuffled — should degrade
- **Oracle:** Full ground-truth access — should be perfect
- **Naive:** Simple heuristic — should be above chance but below candidate
- **Frozen:** State frozen — should be at chance or degraded

### 6.2 V4.4 stochastic control framework

M4 shall use the V4.4 stochastic control framework (SHA-256-CTR-FY, 1000 null replicates, plus-one upper-tail p-value, alpha_family = 0.05, alpha_seed = 0.05/3) as implemented and validated at M3. The reproducibility-contract semantic digest (`m3_scoring_semantic_reproducibility_v1`, as repaired and CRITIC-cleared) shall be used for reproducibility verification.

---

## 7. Multiplicity documentation

### 7.1 Problem

M3 used two scoring runs on two seed pools (201–203, 301–303). Future specs should pre-register multiplicity expectations. M4 must document its multiplicity plan.

### 7.2 M4 multiplicity plan

| Element | Value | Rationale |
|---|---|---|
| Scoring seeds | 5 (fresh, Rebecca-authorized via courier) | Entry 11.3 locked 5 seeds for L7/L8 |
| Seed pools | 1 pool of 5 seeds | No second pool unless Rebecca authorizes |
| Familywise alpha | 0.05 | V4.4 framework |
| Per-seed alpha | 0.05/3 ≈ 0.0167 | V4.4 framework (3 laws: L7, L8, L10) |
| Control families | L7: 6 arms, L8: 6 arms, L10: 6 arms | L18 battery per law |
| Stochastic control checks | 3 laws × 6 arms × 5 seeds = 90 per-seed checks | Plus familywise checks |
| Reproducibility | Semantic digest comparison (both passes) | Reproducibility contract v1 |
| Multiple testing correction | Bonferroni at family level (alpha_family / number of families) | Conservative, consistent with M3 V4.4 |

### 7.3 Hold-out seed rule

≥2 seeds unseen in development per scoring run (standing rule). Development seeds for M4: 101–105 (same development pool as M3, per O-15).

---

## 8. Open work items — M4 scope determination

| Open item | M4 scope? | Disposition |
|---|---|---|
| Multiplicity documentation | **In scope** | §7 of this spec |
| Fresh-seed scoring authorization | **Prerequisite** | Rebecca must authorize via courier. Spec prepares; does not request execution. |
| L3 control calibration resolution | **Out of scope (parallel)** | M3 L3 frozen-control borderline (seed 303) is an M3 instrument issue. M4 tests different laws (L7, L8, L10). L3 resolution should proceed in parallel but does not block M4 spec. |
| Reproducibility contract independent use | **In scope** | M4 harness must use the repaired semantic reproducibility contract (§6.2) |
| Full independent recomputation from M3 raw artifact tree | **Deferred** | Parallel verification activity, not M4 experimental scope |

---

## 9. Sequencing plan

### 9.1 Role assignments

| Step | Role | Deliverable |
|---|---|---|
| 1 | ARCHITECT | This specification + changelog + handoff |
| 2 | CRITIC | Review M4 spec for falsifiability, completeness, bar correctness |
| 3 | Rebecca | Approve M4 spec + L7 graveyard-gate sign-off + timebox + L10 confidence threshold |
| 4 | ARCHITECT | Implementation-completeness amendment (if CRITIC/Rebecca require changes) |
| 5 | INTEGRATOR | Task spec extraction for TASK BUILDER |
| 6 | TASK BUILDER | M4 harness implementation |
| 7 | CRITIC | Implementation verification |
| 8 | INTEGRATOR | Courier packet preparation |
| 9 | Rebecca | Supervised scoring execution (courier) |
| 10 | JUDGE | Scoring ruling |
| 11 | CRITIC | Results review |
| 12 | Rebecca | M4 delivery gate ruling |

### 9.2 Timebox proposal (for Rebecca's approval)

| Parameter | Proposed value | Rationale |
|---|---|---|
| Sessions | 4 | M3 used 4; M4 is comparable complexity (3 new laws + controls) |
| Calendar days | 8 | M3 used 8; same rationale |
| Tripwire (sessions) | 2 | Half-budget check |
| Tripwire (days) | 4 | Half-budget check |
| Start | Upon Rebecca's spec approval + L7 sign-off | — |

---

## 10. L15–L17 integration fence

**No L15, L16, or L17 work is authorized before M5.** This specification:
- Does not propose any integration test
- Does not propose any integration mechanism
- Does not claim integration from M3 provisional advancement
- Does not use the word "integrated" to describe any M4 component

If M4 passes, it means the candidate can mirror, respond to stakes, and calibrate abstention. It does NOT mean the candidate is integrated. Integration is tested only at M5 (L15/L16/L17).

---

## 11. Constraints

- No bars, controls, or scoring logic from M1–M3 modified.
- No scoring run, no fresh seeds, no hold-out seed exposure (until Rebecca authorizes via courier).
- No rerun of seeds 201–203 or 301–303 (O-14).
- Development runs diagnostic-only (O-15).
- O-14, O-15, D1–D5, L9, L18 all binding.
- L15/L16/L17 forbidden before M5.
- ≥2 unseen scoring seeds per scoring run.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- Rebecca sole gate/merge authority.
- No building mechanisms before test harness exists.
- No component promoted as integrated without full L15 ablation matrix.

---

## 12. Items requiring Rebecca's decision

| Item | What | Why |
|---|---|---|
| L7 graveyard-gate sign-off | Rebecca must sign with M3 results in front of her | Entry 11.8 deferred gate |
| L10 confidence threshold | Proposed τ = 0.70; requires Rebecca approval | W4 pre-registration |
| L8 stakes levels | Proposed h=1/h=3/h=5; requires Rebecca approval | Operational definition |
| M4 timebox | Proposed 4 sessions / 8 days; requires Rebecca approval | §9.2 |
| L8 numeric bars | L8 was classified "measurable in form, unmeasurable in magnitude" — specific numeric thresholds for dose-response monotonicity test need Rebecca confirmation | O-2 partially closed |

---

## 13. Implementation handoff

**Next recipient:** CRITIC — Review this specification for:
- Falsifiability of all bars (Entry 11.10 standing instruction)
- Completeness of L7/L8/L10 operational definitions
- Correctness of L18 battery
- L10 confidence threshold pre-registration (W4)
- L14 bar correctness (W5)
- Multiplicity plan adequacy
- L15–L17 fence respected
- No bars lowered, raised, or invented beyond what provenance sources support
- Source recovery gaps flagged

After CRITIC approval: **Rebecca** (approve spec + L7 sign-off + L10 threshold + timebox) → implementation cycle.

**Explicitly prohibited for TASK BUILDER:**
- Modifying any locked bar, threshold, or scoring predicate.
- Running any scoring seeds.
- Running seeds 201–203 or 301–303.
- Implementing L15/L16/L17 or any M5 component.
- Modifying STATE.md or provenance_log.md.
- Renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
