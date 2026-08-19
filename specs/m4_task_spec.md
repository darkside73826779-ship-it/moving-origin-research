# M4 Task Specification — Build-Facing Extraction from Spec v1.6.2

**Date:** 2026-08-18 · **Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Base SHA:** `7acf94f` (GitHub main, includes PR #59 spec v1.6.2 merge at `66acce9`, PR #60 Entry 78 gate signature, PR #61 STATE reconciliation)
**Source spec:** `specs/m4_specification.md` v1.6.2 on GitHub main (merged PR #59, CRITIC-CLEARED per Entry 77)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this task spec > agent judgment
**Role boundary:** This is a faithful extraction from the committed spec v1.6.2. No design additions, no interpretations, no mechanism construction. Where the spec has a STOP/escalation trigger, this task spec flags it. [§5-P1: repo-first law — all binding text is in the repo]

**Law text source:** `docs/ARCHITECTURAL_CONSTITUTION.md` on GitHub main (v1, SHA-256 `509f11c316e6ed3abbdca2df4973484dd676eecc87b727f312ee8658bef93b19`) [§5-P2]
**Constitution v2 source:** `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on GitHub main (§5 + Amendments 1–2)
**M0 Decision Sheet:** `docs/rulings/M0_DECISION_SHEET.md` on GitHub main [BAR-Entry 11]
**Provenance source:** `docs/rulings/provenance_log.md` on GitHub main, through Entry 78 [§5-P6: all citations verified against actual entry text]

---

## §1. Authority and non-authorizations

### 1.1 Authorization

Rebecca signed the M4 L7 graveyard-gate (Entry 78) for **implementation only**. Spec v1.6.2 is merged to main (PR #59, `66acce9`). Step 8 (build authorization) is live. This task spec is the first build action. [BAR-Entry 11.8] [Entry 78]

### 1.2 What is NOT authorized

- **Scoring is NOT authorized.** Implementation proceeds under O-15 (diagnostic-only). [O-15]
- **No fresh-seed exposure.** Seeds 201–203 and 301–303 never rerun (O-14). [O-14]
- **No L15/L16/L17 work.** Fenced to M5. [LAW-L15/L16/L17 fence]
- **No merging to main.** Rebecca is sole merge authority.
- **No modification of the spec, constitution, STATE.md, or provenance_log.md.**

### 1.3 Five downstream scoring gates retained

All five gates must clear before any M4 scoring run: [BAR-Entry 11.8] [Entry 76 Ruling 6]

1. L3 fresh-seed resolution (Option A, Entry 72) [BAR-Entry 72]
2. FWFP closure audit (Entry 43) [BAR-Entry 43]
3. CRITIC implementation review
4. Rebecca's tolerance-calibration sign-off (Ruling 9, Entry 76) [Entry 76]
5. Rebecca's courier-channel scoring authorization

---

## §2. Verbatim law quotes and tagged bars

### 2.1 Laws tested at M4

| Law | Purpose | Constitution source | Source tag |
|---|---|---|---|
| L7 | Mirror/peer-observer: self-reports calibrated against ground truth AND beat peer-observer | `docs/ARCHITECTURAL_CONSTITUTION.md`, line 24 | [LAW-L7] |
| L8 | Stakes coupling: homeostatic regulation error rises when self-model calibration degraded | `docs/ARCHITECTURAL_CONSTITUTION.md`, line 26 | [LAW-L8] |
| L10 | Retrieval honesty: abstention under drift, not blended guess | `docs/ARCHITECTURAL_CONSTITUTION.md`, line 30 | [LAW-L10] |
| L14 | Stakes touch everything or nothing | `docs/ARCHITECTURAL_CONSTITUTION.md`, line 40 | [LAW-L14] |
| L18 | Contamination controls on every positive claim | `docs/ARCHITECTURAL_CONSTITUTION.md`, line 52 | [LAW-L18] |

### 2.2 Verbatim law text (P2 — quoted from constitution file, cited by file and line)

**L7 — Mirror standard** [LAW-L7, `docs/ARCHITECTURAL_CONSTITUTION.md` line 24]:

> Self-reports about internal state must be calibrated against ground-truth internals AND must beat a peer-observer baseline (a matched model predicting this system from its outputs). *Test:* AUROC ≥ 0.75 and ECE ≤ 0.10 on self-state prediction, with the self-vs-peer margin > 0 at p < .05. No margin over the peer = portrait, not mirror — reported as such. Contamination controls (permuted/empty/shuffled) mandatory.

**L8 — Stakes coupling** [LAW-L8, `docs/ARCHITECTURAL_CONSTITUTION.md` line 26]:

> At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

**L10 — Retrieval honesty** [LAW-L10, `docs/ARCHITECTURAL_CONSTITUTION.md` line 30]:

> Below-threshold matches produce abstention, never a blended guess; abstention calibration measured under drift, not only clean splits. *Test:* drifted-regime AUROC is the reported number; the clean number is a ceiling, not a claim.

**L14 — Stakes touch everything or nothing** [LAW-L14, `docs/ARCHITECTURAL_CONSTITUTION.md` line 40]:

> The homeostatic variables (L8) must be readable by the self-model, affected by memory quality, and predictive targets for the thick present. A stakes module only one component can see is decorative.

**L18 — Contamination controls on every positive claim** [LAW-L18, `docs/ARCHITECTURAL_CONSTITUTION.md` line 52]:

> (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

### 2.3 Locked bars with source-class tags (P3)

| Law | Bar | Value | Source tag |
|---|---|---|---|
| L7 | AUROC | ≥ 0.75 | [LAW-L7] |
| L7 | ECE | ≤ 0.10 | [LAW-L7] |
| L7 | Margin (candidate AUROC − peer AUROC) | > 0 at p < .05 | [LAW-L7] |
| L7 | Seeds | 5 | [BAR-Entry 11.3] |
| L7 | Inferential policy | all-seeds-direction + bootstrap-CI fallback | [BAR-Entry 11.3] |
| L7 | Graveyard gate | Rebecca must sign with prior milestone results | [BAR-Entry 11.8] |
| L8 | Minimum dose levels | ≥ 3 | [BAR-Entry 11] |
| L8 | Spearman ρ (monotonic) | ≥ 0.8 | [BAR-Entry 11] |
| L8 | Standardized slope | ≥ 0.2 | [BAR-Entry 11] |
| L8 | Monotonic test | All-seeds-direction + bootstrap-CI fallback | [BAR-Entry 11.3] |
| L8 | Seeds | 5 | [BAR-Entry 11.3] |
| L10 | Abstention under drift | ≥ 50% | [BAR-Entry 11.6] |
| L10 | Abstention when clean | ≤ 10% | [BAR-Entry 11.6] |
| L10 | Drifted-AUROC floor | ≥ 0.70 | [BAR-Entry 14] |
| L10 | Seeds | 5 | [BAR-Entry 11.3] (Ruling 8) |
| L14 | Effect size (primary) | d ≥ 0.5 | [BAR-Entry 11.4] |
| L14 | Correlation (weakest) | corr ≥ 0.3 at 3 seeds | [BAR-Entry 14] |
| L18 | Full battery | empty/permuted/shuffled/oracle/naive/frozen | [LAW-L18] |
| L18 | Seeds | 3+ (5 for L7/L8) | [LAW-L18] [BAR-Entry 11.3] |
| FWFP | Familywise false-positive rate | ≤ 5% per arm and milestone-wide | [BAR-Entry 43] |
| Reproducibility | Semantic digest comparison (both passes) | — | [OP-Entry 11.7] |
| Seeds (development) | 101–105 | O-15 diagnostic-only | [OP-Entry 11.7] [O-15] |
| Seeds (scoring) | ≥ 2 unseen per scoring run | — | [standing rule] |

### 2.4 [PROPOSED] items — quarantined (may NOT gate until Rebecca signs off)

| Item | Value/Description | Source tag | Status |
|---|---|---|---|
| L7 control-arm tolerances (Empty/Permuted/Shuffled/Oracle/Naive/Frozen) | Various thresholds | [PROPOSED — requires Rebecca sign-off] | Governed by tolerance calibration procedure (§7.6 of spec, Ruling 9) |
| L8 control-arm tolerances | Various thresholds | [PROPOSED — requires Rebecca sign-off] | Same procedure |
| L10 control-arm tolerances | Various thresholds | [PROPOSED — requires Rebecca sign-off] | Same procedure |
| L7 peer confidence method | Peer generates own confidence from observation channel | [PROPOSED — requires Rebecca sign-off] | Spec §2.3 |
| L8 homeostatic variable regulation target | Specific numeric value or bound | [PROPOSED — requires Rebecca sign-off] | Spec §3.3.1 |
| Tolerance calibration method and criterion | Method and acceptance criterion | [PROPOSED — requires Rebecca sign-off] | Ruling 9 — ARCHITECT specifies, TASK BUILDER computes, CRITIC verifies, Rebecca signs off on method/criterion |
| L10 seed pools | 1 pool of 5 seeds | [PROPOSED — derived from single-pool design] | Spec §7.1 NF4 |
| Total stochastic checks | 45 (3 laws × 3 families × 5 seeds) | [PROPOSED — derived] | Spec §7.1 NF4 |

---

## §3. Per-law implementation requirements

### 3.1 L7 — Mirror standard

**Verbatim law text:** See §2.2 above. [LAW-L7, line 24]

**Implementation requirements:**

1. **Candidate and peer-observer predict properties of the candidate's own recent state.** The candidate uses its moving-origin internal representation. The peer-observer uses only observable inputs. [LAW-L7]

2. **Peer-observer construction (matched model):** Same parameters, same training data, same architecture as candidate. Observation channel = behavioral outputs only (append-log, query stream, external events). Excluded channels: candidate's internal state, self-report channel, confidence estimates, moving-origin representation. [BAR-Entry 11] (M0 Decision Sheet line 20)

3. **Peer-observer parity conditions (Ruling 5, Entry 76):**
   - Identical confidence calibration (same pre-registered procedure) [BAR-Entry 11]
   - Identical evaluation data [BAR-Entry 11]
   - Identical ECE definition (same bins, same binning method) [BAR-Entry 11]
   - Identical binning for all binned metrics [BAR-Entry 11]
   - Paired independently trained instances (same data, same architecture, same initialization seed, but peer does not see candidate's internal state during training) [BAR-Entry 11]

4. **L7 inference policy (Ruling 1, Entry 76 — Option C):**
   - AUROC and ECE are per-seed threshold bars: any-seed fail → KILL, no fallback [LAW-L7] [BAR-Entry 11]
   - Candidate–peer margin is a direction test: evaluated across 5 paired seeds using all-seed direction consistency AND pooled paired-bootstrap 95% CI excluding zero [BAR-Entry 11.3]
   - The v1.4 "Amendment 3" hard rule (no fallback for any L7 bar) is retracted [P5 — authorized by Rebecca's ruling]

5. **Portrait clause:** No margin over the peer = portrait, not mirror — reported as such. KILL (not INSTRUMENT_FAILURE). [LAW-L7]

6. **No-clean-only self-report rule:** L7 query battery includes clean and adversarial queries (distribution-shifted). AUROC and margin computed over combined set. L18 control arms serve as adversarial splits. L10 drifted regime cross-validates.

**Kill conditions:**
- Candidate AUROC < 0.75 [LAW-L7] on any seed → KILL
- ECE > 0.10 [LAW-L7] on any seed → KILL
- Margin: not directionally positive across all 5 seeds OR pooled bootstrap 95% CI includes zero [BAR-Entry 11.3] → KILL

### 3.2 L8 — Stakes coupling

**Verbatim law text:** See §2.2 above. [LAW-L8, line 26]

**Implementation requirements:**

1. **Homeostatic variable:** Define ≥ 1 [LAW-L8] homeostatic variable with a regulation target. The candidate maintains this variable (e.g., a resource level, error budget, or calibration metric) that should stay within bounds for healthy operation.

2. **Level 0 zero-noise baseline (Ruling 3, Entry 76):** No perturbation — self-model at full calibration. This is the reference point for the dose-response. Regulation error at Level 0 is the baseline; all higher-dose regulation errors are compared against it. [Rebecca-approved]

3. **Calibrated-noise injection:** Inject calibrated noise into the self-model (the L7 mirror component — the candidate's self-state representation) at ≥ 3 dose levels [BAR-Entry 11]:
   - Level 0 (zero-noise baseline): No perturbation [Rebecca-approved (Ruling 3)]
   - Level 1 (low): Small perturbation
   - Level 2 (medium): Moderate perturbation
   - Level 3 (high): Large perturbation

4. **Regulation error measurement:** At each dose level, measure the regulation error of the homeostatic variable — how far it deviates from its target. Regulation error must rise dose-dependently [LAW-L8].

5. **Pre-registered direction:** Regulation error INCREASES as self-model noise dose increases. All-seeds-direction test requires this on all 5 seeds [BAR-Entry 11.3].

6. **"Only then" specificity leg (Ruling 3, Entry 76 — standardized proximal-component effect):** Inject calibrated noise into a NON-self-model component. Severity matching based on pre-registered standardized proximal-component effect:
   - Predefine the comparison component [Rebecca-approved (Ruling 3)] [LAW-L19]
   - Predefine the perturbation type and magnitude (standardized to self-model dose) [Rebecca-approved (Ruling 3)] [LAW-L19]
   - Predefine the calibration set (separate from scoring seeds) [Rebecca-approved (Ruling 3)] [LAW-L19]
   - Predefine the tolerance (acceptable deviation from exact severity match) [Rebecca-approved (Ruling 3)] [LAW-L19]
   - The homeostatic regulation error must NOT rise when severity-matched noise is injected into non-self-model components [LAW-L8]

7. **All four predefinitions are pre-registered before any data exists** [LAW-L19].

**Kill conditions:**
- Non-monotonic dose-response on any seed (after bootstrap-CI fallback) [BAR-Entry 11.3] → KILL
- Frozen arm shows dose-response [LAW-L8] → KILL (stakes decorative)
- Non-self-model noise raises regulation error [LAW-L8] ("only then" violated) → KILL

**Instrument failure conditions:**
- Oracle arm does not show expected degradation pattern → INSTRUMENT_FAILURE
- Empty arm shows non-chance regulation at any level → INSTRUMENT_FAILURE
- Reproducibility check fails → INSTRUMENT_FAILURE

### 3.3 L10 — Retrieval honesty

**Verbatim law text:** See §2.2 above. [LAW-L10, line 30]

**Implementation requirements:**

1. **Confidence definition:** The candidate's confidence estimate is a scalar output in [0, 1] representing the candidate's assessed probability that its prediction is correct. Generated by the candidate's self-model (L7 mirror component) from its internal state representation. [BAR-Entry 11]

2. **Primary drifted AUROC (Ruling 2, Entry 76):** Computed over the complete fixed drifted population using pre-abstention scores — the candidate's confidence/ranking before abstention is applied. This closes the abstention-exclusion gaming surface. [BAR-Entry 14] [LAW-L10]

3. **Answered-case AUROC:** Reported separately (non-abstained drifted cases), but is NOT the headline. [BAR-Entry 14] [LAW-L10]

4. **All-abstain AUROC:** If the candidate abstains on all drifted cases, the drifted-regime AUROC fails the ≥ 0.70 floor [BAR-Entry 14]. All-abstain is not N/A — it is a failure.

5. **τ calibration:** Calibrated on held-out calibration data (separate from scoring seeds) to satisfy BOTH drift ≥ 50% abstention [BAR-Entry 11.6] AND clean ≤ 10% abstention [BAR-Entry 11.6]. The threshold τ is the value that satisfies both constraints on the calibration set. [BAR-Entry 11.6] [BAR-Entry 11]

6. **Clean-regime specificity control:** Clean regime: abstention ≤ 10%. Drifted regime: abstention ≥ 50%. Frozen-state candidate should NOT show differential abstention between clean and drifted. [LAW-L10] [BAR-Entry 11.6]

7. **Reporting rule (F1.3 correction):** Drifted-regime AUROC is the reported number; clean is a ceiling, not a claim. Report drifted-regime AUROC as primary; clean-regime AUROC as ceiling (explicitly labeled); do not cite clean-regime AUROC as a standalone claim. [LAW-L10]

**Kill conditions:**
- Abstention < 50% under drift [BAR-Entry 11.6] on any seed → KILL
- Abstention > 10% when clean [BAR-Entry 11.6] on any seed → KILL
- Drifted-AUROC < 0.70 [BAR-Entry 14] on any seed → KILL

### 3.4 L14 — Stakes touch everything or nothing

**Verbatim law text:** See §2.2 above. [LAW-L14, line 40]

**Implementation requirements:**

Three couplings between the homeostatic variables (L8) and other system components:

1. **Coupling 1 — Readable by the self-model [LAW-L14]:** The candidate's self-model (L7 mirror component) can read the homeostatic variable's current value. Test: the self-model's state prediction includes the homeostatic variable, and its prediction accuracy for the homeostatic variable is above chance.

2. **Coupling 2 — Affected by memory quality [LAW-L14]:** Degrading the memory system (e.g., frozen-origin arm, shuffled input) measurably affects the homeostatic variable's regulation error. Test: compare regulation error under normal memory vs. degraded memory; degradation must increase regulation error.

3. **Coupling 3 — Predictive targets for the thick present [LAW-L14]:** The thick present (L3 state object) includes the homeostatic variable as a predictive target. Test: the candidate's next-input prediction at horizon H includes the homeostatic variable, and prediction accuracy for it is above chance.

**Bars:** d ≥ 0.5 [BAR-Entry 11.4] for each coupling's effect size. corr ≥ 0.3 at 3 seeds [BAR-Entry 14] as weakest inferential bar.

**Kill conditions:**
- d < 0.5 for any coupling [BAR-Entry 11.4] → KILL
- corr < 0.3 at 3+ seeds for any coupling [BAR-Entry 14] → KILL
- Homeostatic variable not readable by self-model [LAW-L14] → KILL (decorative)

### 3.5 L18 — Full battery

**Verbatim law text:** See §2.2 above. [LAW-L18, line 52]

**Implementation requirements:**

Full L18 battery at every milestone [LAW-L18]: empty, permuted, shuffled, oracle, naive, frozen. 3+ seeds [LAW-L18]; 5 seeds for L7/L8 [BAR-Entry 11.3].

L14 is deterministic (no stochastic family; direct threshold per seed) [LAW-L14].

---

## §4. Six control arms and failure routing

### 4.1 L7 control arms (§2.4 of spec)

| Control arm | Expected behavior | Failure routing | Source tag |
|---|---|---|---|
| Empty | Chance AUROC (0.5) | INSTRUMENT_FAILURE if deviates > 0.05 | [PROPOSED — requires Rebecca sign-off] |
| Permuted | Labels shuffled — collapse to chance | INSTRUMENT_FAILURE if AUROC > 0.55 | [PROPOSED — requires Rebecca sign-off] |
| Shuffled | Input order shuffled — degrade | INSTRUMENT_FAILURE if shuffled AUROC > candidate AUROC | [PROPOSED — requires Rebecca sign-off] |
| Oracle | Full ground-truth — AUROC ≈ 1.0 | INSTRUMENT_FAILURE if AUROC < 0.95 | [PROPOSED — requires Rebecca sign-off] |
| Naive | Simple heuristic — above chance, below candidate | KILL if naive AUROC ≥ candidate AUROC | [PROPOSED — requires Rebecca sign-off] |
| Frozen | State frozen — chance | INSTRUMENT_FAILURE if AUROC > 0.55 | [PROPOSED — requires Rebecca sign-off] |

### 4.2 L8 control arms (§3.4 of spec)

| Control arm | Expected behavior | Failure routing | Source tag |
|---|---|---|---|
| Empty | No self-model — regulation error constant | INSTRUMENT_FAILURE if any level deviates from baseline | [PROPOSED — requires Rebecca sign-off] |
| Permuted | Self-model noise labels shuffled — no dose-response | INSTRUMENT_FAILURE if monotonic trend persists | [PROPOSED — requires Rebecca sign-off] |
| Shuffled | Self-model input order shuffled — degraded dose-response | INSTRUMENT_FAILURE if exceeds candidate at any level | [PROPOSED — requires Rebecca sign-off] |
| Oracle | Full ground-truth self-model — should show SAME or STRONGER dose-response | INSTRUMENT_FAILURE if no expected degradation pattern | [PROPOSED — requires Rebecca sign-off] |
| Naive | Fixed heuristic self-model — weaker dose-response | KILL if naive outperforms candidate | [PROPOSED — requires Rebecca sign-off] |
| Frozen | Self-model frozen at initial value — no dose-response | KILL if frozen shows monotonic trend (stakes decorative) | [LAW-L8] |

### 4.3 L10 control arms (§4.5 of spec)

| Control arm | Expected behavior | Failure routing | Source tag |
|---|---|---|---|
| Empty | No data — abstain 100% | INSTRUMENT_FAILURE if abstention < 100% | [PROPOSED — requires Rebecca sign-off] |
| Permuted | Confidence labels shuffled — no differential abstention | INSTRUMENT_FAILURE if differential abstention persists | [PROPOSED — requires Rebecca sign-off] |
| Shuffled | Input order shuffled — reduced differential abstention | INSTRUMENT_FAILURE if exceeds candidate's pattern | [PROPOSED — requires Rebecca sign-off] |
| Oracle | Full ground-truth — abstain ~0% in both regimes | INSTRUMENT_FAILURE if abstains > 10% in either regime | [PROPOSED — requires Rebecca sign-off] |
| Naive | Fixed confidence — minimal differential abstention | KILL if naive outperforms candidate's calibration | [PROPOSED — requires Rebecca sign-off] |
| Frozen | State frozen — no differential abstention | INSTRUMENT_FAILURE if frozen shows differential abstention | [PROPOSED — requires Rebecca sign-off] |

### 4.4 Note on [PROPOSED] control-arm tolerances

All control-arm tolerance thresholds are currently tagged [PROPOSED — requires Rebecca sign-off]. These are governed by the tolerance calibration procedure (Ruling 9, Entry 76 — see §5 below and §7.6 of spec). The TASK BUILDER computes the actual tolerance numbers under O-15 (diagnostic-only) per this procedure; the ARCHITECT specifies the procedure; the CRITIC verifies; Rebecca signs off on method/criterion. The [PROPOSED] tags will be resolved to computed values once the calibration procedure is executed.

---

## §5. Entry 76 gate rulings — nine items (all implemented in spec v1.6.2)

**Source:** Entry 76 [verified: provenance_log.md, Entry 76 — Principal ruling: Step 7 gate, decided 2026-08-18 22:54 EDT]. All nine citations verified against actual entry text (P6).

| Ruling | Subject | Decision | Source tag |
|---|---|---|---|
| 1 | L7 inference | Option C: AUROC/ECE per-seed threshold bars (any-seed fail → KILL, no fallback); margin is direction test across 5 paired seeds using all-seed direction consistency and pooled paired-bootstrap CI (M0 Entry 11.3 fallback policy); v1.4 "Amendment 3" hard no-fallback rule retracted | [BAR-Entry 11.3] |
| 2 | L10 threshold | Primary drifted AUROC over complete fixed drifted population using pre-abstention scores; answered-case AUROC secondary; all-abstain fails ≥0.70; τ calibrated for drift ≥50% and clean ≤10%; floor 0.70 preserved | [BAR-Entry 14] [BAR-Entry 11.6] |
| 3 | L8 severity matching | Level 0 zero-noise baseline; standardized proximal-component severity matching (predefined component/perturbation/calibration set/tolerance) | [LAW-L8] [LAW-L19] |
| 4 | Borderline handling | B1 confirmed: label retained; 0.5α–α band descriptive only, must NOT change verdict | [BAR-Entry 43] [LAW-L19] |
| 5 | L7 peer conditions | Matched-model baseline conditioned on identical confidence calibration/evaluation data/ECE definition/binning + paired independently trained instances | [BAR-Entry 11] |
| 6 | L7 graveyard-gate scope | Signed for implementation only; scoring NOT authorized; L3/FWFP/implementation-review/courier gates retained | [BAR-Entry 11.8] |
| 7 | Timebox | 6 sessions/14 days, tripwire 3/7, excludes external-review and L3-gate waiting | [Rebecca-approved] |
| 8 | L10 seeds | 5 confirmed | [BAR-Entry 11.3] |
| 9 | Tolerance calibration | Pre-registered, candidate-blind (101–105 NOT inputs; oracle/synthetic only), frozen before scoring; ARCHITECT specifies procedure / TASK BUILDER computes under O-15 / CRITIC verifies / Rebecca signs off on method-criterion | [BAR-Entry 43] [O-15] |

**Note on Ruling 6:** The handoff bullet list omitted Ruling 6, but it is present in Entry 76 and the spec (§1.3). Ruling 6 is the graveyard-gate scope: implementation-only authorization, scoring NOT authorized, five downstream gates retained. This ruling is critical — it defines the authorization boundary for all M4 build work.

---

## §6. FWFP closure audit (§7.3 of spec, Entry 43 standing rule)

**Named deliverable:** M4 Pre-Scoring FWFP Closure Audit

**Standing rule source:** Entry 43 [BAR-Entry 43] — "every scoring spec's closure audit must compute FWFP of each arm's full check battery and correct any control whose FWFP exceeds 5% BEFORE scoring."

**Owner:** TASK BUILDER (computation and correction performed under O-15 diagnostic-only). The ARCHITECT specifies the deliverable; the TASK BUILDER produces it.

**Acceptance criteria:**
1. Every control arm's full check battery (all stochastic families × all checks per arm) is enumerated.
2. The FWFP of each arm's full check battery is computed by direct enumeration or simulation.
3. Any arm whose FWFP exceeds 5% is corrected (e.g., by alpha adjustment, directionality restriction, or null-of-the-max procedure per Entry 43 remedy).
4. The corrected FWFP for every arm is ≤ 5%. [BAR-Entry 43]
5. The closure audit is documented in a committed artifact with all computations traceable.
6. The closure audit is reviewed by CRITIC before scoring authorization.

**Milestone-wide family (extended scope):** In addition to per-arm audit, the closure audit must also control the milestone-wide family of ALL control-triggering tests across M4:
1. Enumerate every control-triggering test across all laws (L7, L8, L10, L14, L18 control arms).
2. Compute milestone-wide FWFP across the full set.
3. Correct any test whose inclusion pushes milestone-wide FWFP above 5%.
4. Milestone-wide FWFP ≤ 5% [BAR-Entry 43] — acceptance criterion in addition to per-arm.

**Placement in build sequence:** Step 8 (TASK BUILDER implementation), as a pre-scoring sub-step. Must be completed and CRITIC-cleared before Rebecca authorizes scoring.

---

## §7. L8 homeostatic-variable prerequisite (§3.3.1 of spec, Amendment 4)

The L8 homeostatic-variable definition is a named prerequisite with its own dedicated reviewer pass. No L8 implementation may proceed until the prerequisite is cleared.

**Reviewer:** CRITIC (or Rebecca-delegated). Must verify:

| Criterion | Requirement | Source |
|---|---|---|
| Regulable | The variable has a defined regulation target and can deviate from it | [LAW-L8] |
| Target defined | The regulation target is a specific numeric value or bound, not a vague aspiration | [PROPOSED — requires Rebecca sign-off] |
| Calibratable noise dose | Noise can be injected into the self-model at ≥ 3 distinguishable levels | [OP-Entry 11.7] |
| Constructible specificity control | A non-self-model component can receive the same noise injection to test the "only then" specificity leg | [LAW-L8] |

**If any criterion is unmet:** Prerequisite is BLOCKED; design returned to ARCHITECT for revision.

**Placement in build sequence:** After spec approval (Step 7) and before TASK BUILDER implementation (Step 8). The prerequisite review is a sub-step of the build sequence, not a scoring gate.

---

## §8. L3 pre-scoring gate (Option A, Entry 72)

**Source:** Entry 72 [BAR-Entry 72] — Principal ruling: §6.3/L3 sequencing contradiction resolved — Option A.

**Ruling:** M4 scoring is gated on L3 fresh-seed resolution. M4 build (implementation, diagnostic runs under O-15) proceeds in parallel with L3 calibration work.

**Gate sequence:**
1. L3 resolution on fresh seeds
2. M4 scoring authorization via Rebecca's courier channel
3. M4 scoring execution

**Note:** Build proceeds independently of the L3 gate. The L3 gate only gates scoring, not implementation or diagnostic runs.

---

## §9. V4.4 stochastic/reproducibility framework (§6.3 of spec)

M4 uses the V4.4 framework as implemented at M3:

| Parameter | Value | Source tag |
|---|---|---|
| Hash algorithm | SHA-256-CTR-FY | [OP-Entry 11.7] |
| Null replicates | 1000 | [OP-Entry 11.7] |
| p-value method | Plus-one upper-tail | [OP-Entry 11.7] |
| alpha_family | 0.05 | [OP-Entry 11.7] |
| alpha_seed | 0.05/3 ≈ 0.0167 (cross-law Bonferroni) | [OP-Entry 11.7] |
| Reproducibility | Semantic digest comparison (both passes) | [OP-Entry 11.7] |

**Stochastic families per law:** 3 per law (frozen, permuted, shuffled) — V4.4 RNG-driven randomization with null distributions. Oracle, naive, empty are deterministic (direct threshold evaluation).

**Alpha structure:** alpha_seed = alpha_family / number_of_tested_laws = 0.05/3 [OP-Entry 11.7]. Cross-law Bonferroni, not per-family-within-law.

**Reproducibility-contract semantic digest:** Used for reproducibility verification. The repaired semantic digest (from M3 reproducibility-contract implementation, PR #21) must be used.

---

## §10. Seed policy and O-14/O-15

| Policy | Value | Source tag |
|---|---|---|
| Development seeds | 101–105 (O-15 diagnostic-only) | [OP-Entry 11.7] [O-15] |
| Scoring seeds | 5 (fresh, Rebecca-authorized via courier) | [BAR-Entry 11.3] |
| Hold-out rule | ≥ 2 seeds unseen in development per scoring run | [standing rule] |
| Seeds 201–203 | Retained as INSTRUMENT FAILURE evidence, never rerun | [O-14] [BAR-Entry 52] |
| Seeds 301–303 | Retained as INSTRUMENT FAILURE evidence, never rerun | [O-14] [BAR-Entry 52] |

---

## §11. STOP/escalation triggers

The following items require escalation to the COORDINATOR if encountered during implementation. The TASK BUILDER must STOP and escalate, not improvise:

1. **Tolerance calibration procedure details:** The ARCHITECT specifies the procedure (method, data source, acceptance criterion). If the procedure is insufficient for the TASK BUILDER to compute tolerances, STOP and escalate. [Ruling 9, Entry 76]

2. **L8 homeostatic-variable design:** If the homeostatic variable cannot meet all four prerequisite criteria (regulable, target defined, calibratable noise dose, constructible specificity control), STOP and escalate to ARCHITECT for revision. [§3.3.1]

3. **L7 peer confidence method:** The peer generates its own confidence estimate from its observation channel — same method as candidate but without privileged self-state access. This is tagged [PROPOSED — requires Rebecca sign-off]. If the implementation cannot proceed without Rebecca's sign-off on this method, STOP and escalate.

4. **Any law text that cannot be operationalized from verbatim quotation:** Per §5-P1/P2, if the constitution's law text is insufficient to fully operationalize a test, STOP and escalate. Do not reconstruct law text.

5. **Any [PROPOSED] item that needs to gate implementation:** [PROPOSED] items may not gate until Rebecca signs off. If a [PROPOSED] item blocks implementation, STOP and escalate.

---

## §12. TASK BUILDER deliverables checklist

| # | Deliverable | Source | Owner |
|---|---|---|---|
| 1 | M4 harness implementation (all 5 laws: L7, L8, L10, L14, L18) | §3 of this task spec | TASK BUILDER |
| 2 | Six control arms per law (Empty, Permuted, Shuffled, Oracle, Naive, Frozen) | §4 of this task spec | TASK BUILDER |
| 3 | V4.4 stochastic control framework (1000 null replicates, SHA-256-CTR-FY, etc.) | §9 of this task spec | TASK BUILDER |
| 4 | Reproducibility-contract semantic digest (repaired version from M3 PR #21) | §9 of this task spec | TASK BUILDER |
| 5 | FWFP closure audit (per-arm + milestone-wide, ≤ 5%) | §6 of this task spec | TASK BUILDER |
| 6 | Tolerance calibration computation (under Ruling 9 procedure, O-15 diagnostic-only) | §5 Ruling 9, §4.4 | TASK BUILDER (computes); ARCHITECT (specifies procedure); CRITIC (verifies); Rebecca (signs off on method/criterion) |
| 7 | Diagnostic runs on seeds 101–105 (O-15, non-scoring) | §10 | TASK BUILDER |

**Post-TASK BUILDER steps:**
- CRITIC: L8 homeostatic-variable prerequisite review (§7) → implementation verification + FWFP closure audit review
- INTEGRATOR: Courier packet (Step 9)
- Rebecca: Supervised scoring execution (Step 10, gated on L3 resolution [BAR-Entry 72])

---

## §13. Explicitly prohibited actions

- No scoring, seed execution, or hold-out seed exposure
- No rerun of seeds 201–203 / 301–303 (O-14)
- No L15/L16/L17 work before M5
- No modification of the spec, constitution, STATE.md, or provenance_log.md
- No design decisions — extract faithfully, flag ambiguities as STOP for the COORDINATOR
- No merging to main
- No renaming or reinterpreting any negative result or INSTRUMENT FAILURE label
- No bars, controls, or scoring logic from M1–M3 modified
- No reconstruction of constitutional text (§5-P1)
- No paraphrasing law text where verbatim quotation is required (§5-P2)

---

## §14. Public-repo scan attestation

**Pre-push self-scan performed:** Yes
**Scan date:** 2026-08-18
**Findings:**
- Credentials/tokens/secrets: None found
- Private paths: None found
- Machine identifiers: None found
- PII: None found
- Scoring seed exposure: None (development seeds 101–105 referenced by policy number only, not as actual seed values in any scoring context)
**Classification:** All clear — acceptable for push

---

## §15. Timebox (Ruling 7, Entry 76)

| Parameter | Value | Source tag |
|---|---|---|
| Sessions | 6 | [Rebecca-approved] |
| Calendar days | 14 | [Rebecca-approved] |
| Tripwire (sessions) | 3 | [Rebecca-approved] |
| Tripwire (days) | 7 | [Rebecca-approved] |

**Exclusions:** External-review waiting time and L3-gate waiting time are excluded from the timebox clock. The clock runs on M4 build work only. [Rebecca-approved]

---

## §16. Borderline handling (Ruling 4, Entry 76 — B1 confirmed)

**Numerical definition of "borderline":** A control firing is borderline if its p-value falls within [α_corrected × 0.5, α_corrected], where α_corrected is the arm's corrected alpha from the FWFP closure audit. [BAR-Entry 43] [LAW-L19]

**B1 handling (Rebecca confirmed):**
1. The INSTRUMENT_FAILURE or KILL label is retained as-is.
2. The firing is reported with full context (which arm, which check, p-value, corrected alpha, margin ratio, all-seeds pattern).
3. Candidate-facing evidence may support provisional advancement, but the control firing remains on the record.
4. Any correction follows the Entry 43 four-part test as a post-scoring action, not a relabeling.
5. The M3 precedent (Entry 43) is the model.

**The 0.5α–α band is descriptive only (Ruling 4):** Must NOT change the verdict. [BAR-Entry 43]

---

*This task spec is a faithful extraction from M4 spec v1.6.2 (`specs/m4_specification.md` on GitHub main at `7acf94f`). No design additions. All law quotations are verbatim from `docs/ARCHITECTURAL_CONSTITUTION.md`. All source-class tags per §5-P3. Regime B, date 2026-08-18 per §5-P4. Provenance citations verified per §5-P6.*
