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

**Peer-observer specification (CRITIC Blocking 2 resolution + BF4 resolution):**

The peer-observer is a **fixed linear baseline** — not a trained model, not an adaptive learner. This makes the test reproducible and prevents the peer from being either too weak (trivial) or too strong (unfairly sophisticated).

- **Algorithm/model class:** Ordinary least squares (OLS) regression mapping the observable input history to the same state-property prediction task the candidate solves. No learned nonlinearity, no neural network, no adaptive mechanism.
- **Training data:** The peer is fit on the same fitting-origin data the candidate uses (e.g., cycles 0–699 in the M3 L3 pattern). Training is completed before candidate evaluation begins. No online learning.
- **Features:** The peer receives exactly the observable inputs: the append-log entries, query stream, and external event timestamps. It does NOT receive: the candidate's internal state variables, self-report channel, confidence estimates, or moving-origin representation. The peer's feature vector is the raw observable input window at query time.
- **Calibration procedure:** The peer's confidence is computed via the same method as the candidate's (e.g., normalized prediction entropy or distance-to-threshold). No separate calibration — the peer uses the raw OLS residual as its confidence proxy.
- **Rationale:** A fixed linear peer is the strongest fair baseline that does not require its own temporal machinery. If the candidate's moving origin provides privileged access, it should beat a linear model that sees the same inputs but lacks the internal representation. If the candidate cannot beat a linear peer, the moving origin is not contributing self-knowledge.

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
- **Candidate AUROC − peer AUROC ≤ 0** (margin not statistically significant: p-value of margin test ≥ .05) → KILL (NF2 resolution)
- **ECE > 0.10** on any seed → KILL

### 2.6 Instrument failure conditions

- Any L18 control arm producing an implausible result (e.g., oracle AUROC < 0.95, empty AUROC > 0.55) → INSTRUMENT_FAILURE
- Reproducibility check fails (semantic digest mismatch) → INSTRUMENT_FAILURE
- Non-finite numeric results → INSTRUMENT_FAILURE

### 2.7 No-clean-only self-report rule (BF5 resolution)

Standing rule: "No self-reports scored only on clean splits." L7 uses self-state prediction evidence, so it must not be scored only on clean (non-adversarial) queries.

**How L7 satisfies this:**
1. The L7 query battery includes both **clean queries** (standard state-property predictions from the normal distribution) and **adversarial queries** (state-property predictions under distribution shift, drawn from a different temporal region than the fitting data). Both sets are scored together.
2. The L18 control arms (permuted, shuffled, frozen) serve as adversarial splits — they test whether the candidate's self-knowledge survives perturbation. If the candidate only passes on clean queries and fails on permuted/shuffled, the overall verdict is INSTRUMENT_FAILURE (control arm failure), not PASS.
3. The AUROC and margin bars are computed over the combined query set (clean + adversarial), not over clean-only.
4. The L10 drifted regime (§4.5) provides additional adversarial evidence on the same candidate, cross-validating that self-knowledge is not clean-only.

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

**Pre-registered direction (BF1 resolution):** Performance DECREASES as stakes increase — higher prediction horizon yields lower accuracy. This direction is pre-registered before any data. The all-seeds-direction test requires accuracy(h=1) > accuracy(h=3) > accuracy(h=5) on all 5 seeds. If any seed shows a reversed direction, the bootstrap-CI fallback is applied.

**Minimum effect threshold (proposed — requires Rebecca approval):** The total accuracy drop from level 1 (h=1) to level 3 (h=5) must be ≥ 0.05 on each seed. A drop smaller than 0.05 is clinically negligible and fails the dose-dependence claim even if monotonic. This threshold is proposed; Rebecca may set a different value.

**Specificity control:** The frozen arm (state frozen at initial value) should NOT show a dose-response. If it does, the "stakes" manipulation is not actually engaging the candidate's temporal machinery — it's a general difficulty effect, not a moving-origin effect.

### 3.3a L18 control arms for L8 (BF2 resolution)

| Control arm | Expected behavior under dose-response | Failure routing |
|---|---|---|
| Empty | No data — no dose-response possible (accuracy constant at chance) | INSTRUMENT_FAILURE if any level deviates from chance |
| Permuted | Stakes-level labels shuffled — should NOT show monotonic trend (trend destroyed by label shuffling) | INSTRUMENT_FAILURE if monotonic trend persists |
| Shuffled | Input order shuffled — should show degraded or flat dose-response (temporal order disrupted) | INSTRUMENT_FAILURE if performance exceeds candidate at any level |
| Oracle | Full ground-truth access — should show the SAME or STRONGER dose-response (oracle also degrades with longer horizons, but less) | INSTRUMENT_FAILURE if oracle does not show expected degradation pattern |
| Naive | Simple heuristic (most-recent-state) — should show weaker dose-response than candidate | INSTRUMENT_FAILURE if naive outperforms candidate |
| Frozen | State frozen at initial value — should NOT show dose-response (no temporal machinery engaged) | KILL if frozen shows monotonic trend (stakes decorative) |

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

### 4.4a L18 control arms for L10 (BF2 resolution)

| Control arm | Expected behavior under abstention test | Failure routing |
|---|---|---|
| Empty | No data — should abstain at 100% (no confidence possible) | INSTRUMENT_FAILURE if abstention < 100% |
| Permuted | Confidence labels shuffled — should show NO differential abstention between clean/drifted (calibration destroyed) | INSTRUMENT_FAILURE if differential abstention persists |
| Shuffled | Input order shuffled — should show reduced or flat differential abstention | INSTRUMENT_FAILURE if abstention pattern exceeds candidate's |
| Oracle | Full ground-truth access — should abstain at ~0% in both regimes (oracle is always confident) | INSTRUMENT_FAILURE if oracle abstains > 10% in either regime |
| Naive | Simple heuristic (fixed confidence) — should show minimal differential abstention | INSTRUMENT_FAILURE if naive outperforms candidate's calibration |
| Frozen | State frozen at initial value — should NOT show differential abstention between clean and drifted | INSTRUMENT_FAILURE if frozen shows differential abstention |

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

### 5.4 No-clean-only self-report rule (BF5 resolution)

L14 uses self-reported state correlation, so it must not be scored only on clean queries.

**How L14 satisfies this:**
1. L14 is computed over the combined L7 query set (clean + adversarial, as defined in §2.7). The correlation and effect size are measured on the full query set, not clean-only.
2. The L18 control arms provide adversarial perturbations. If the candidate's self-report correlates with ground truth only on clean queries and collapses on permuted/shuffled, the L18 control arm fails (INSTRUMENT_FAILURE), preventing a clean-only PASS.
3. L14 is a continuous invariant — it was already tested at M3 (where L18 controls were active). M4 continues this pattern: L14 is scored alongside L7, L8, L10, all of which include adversarial control arms.

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

### 7.2 M4 multiplicity plan (BF3 resolution)

**Two-level alpha structure:**

| Level | Correction | Value | Applies to |
|---|---|---|---|
| Within-law | alpha_seed = alpha_family / 3 | 0.05 / 3 ≈ 0.0167 | Per stochastic family within each law (V4.4 framework, same as M3) |
| Cross-law | Bonferroni: 0.05 / number_of_tested_laws | 0.05 / 3 ≈ 0.0167 | Across L7, L8, L10 candidate-facing bars |

Note: These produce the same numerical value (0.05/3) by coincidence — 3 stochastic families per law and 3 tested laws. They are conceptually distinct corrections: within-law corrects for multiple control arms, cross-law corrects for multiple candidate-facing tests.

**L14 multiplicity status:** L14 is a deterministic correlation/effect-size measurement, not a stochastic control family. It has no null replicates, no plus-one p-value, and no V4.4 stochastic family. It is therefore EXCLUDED from the stochastic control check count. L14's bars (d ≥ 0.5, corr ≥ 0.3) are evaluated directly per seed without stochastic correction. If CRITIC or Rebecca determines L14 requires stochastic treatment, it should be added to the family count.

**Per-arm statistical test definitions:**

| Law | Arm type | Statistical test | Direction |
|---|---|---|---|
| L7 | Stochastic controls (empty, permuted, shuffled, oracle, naive, frozen) | Plus-one upper-tail p-value (V4.4) | Upper (statistic exceeds null) or two-sided-magnitude (departure from null) per arm |
| L7 | Candidate (AUROC, ECE, margin) | Direct threshold + paired test (margin) | AUROC ≥ 0.75; margin > 0 at p < .05 |
| L8 | Stochastic controls (6 arms) | Plus-one upper-tail p-value (V4.4) | Upper (statistic exceeds null) |
| L8 | Candidate (monotonic trend) | All-seeds-direction + bootstrap-CI fallback | Pre-registered: decreasing (§3.3) |
| L10 | Stochastic controls (6 arms) | Plus-one upper-tail p-value (V4.4) | Two-sided-magnitude (departure from null) |
| L10 | Candidate (abstention rates, AUROC) | Direct threshold per seed | ≥ 50% drift; ≤ 10% clean; AUROC ≥ 0.70 |
| L14 | Candidate (correlation, effect size) | Direct threshold per seed (no stochastic family) | d ≥ 0.5; corr ≥ 0.3 |

**Check count:**

| Component | Families | Seeds | Per-seed checks | Total |
|---|---|---|---|---|
| L7 stochastic controls | 6 | 5 | 1 per family per seed | 30 |
| L8 stochastic controls | 6 | 5 | 1 per family per seed | 30 |
| L10 stochastic controls | 6 | 5 | 1 per family per seed | 30 |
| L14 | 0 (deterministic) | 5 | 0 | 0 |
| **Total stochastic checks** | | | | **90** |

| Element | Value |
|---|---|
| Scoring seeds | 5 (fresh, Rebecca-authorized via courier) |
| Seed pools | 1 pool of 5 seeds |
| Familywise alpha (within-law) | 0.05 |
| Per-seed alpha (within-law) | 0.05/3 ≈ 0.0167 |
| Cross-law Bonferroni | 0.05/3 ≈ 0.0167 |
| Total stochastic control checks | 90 |
| Reproducibility | Semantic digest comparison (both passes) |

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
