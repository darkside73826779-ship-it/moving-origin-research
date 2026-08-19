# M4 Specification v1.6 — Mirror, Stakes, and Calibration

**Serves:** Rebecca's M4 gate authorization (2026-08-17, G0-1 correction cycle 2026-08-18, Step 6 amendments 2026-08-18, advisor correction cycle 2026-08-18, Step 7 gate rulings 2026-08-18)
**Status:** ARCHITECT draft v1.6 — Rebecca's nine gate rulings implemented (L7 inference, L10 threshold, L8 severity matching, borderline handling, L7 peer conditions, graveyard-gate scope, timebox, L10 seeds, tolerance calibration)
**Date:** 2026-08-18 · **Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Base SHA:** `487843f` (v1.5, CRITIC-cleared)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this specification > agent judgment
**Prior context:** M0 GO [OP-Entry 10], M1 GREEN, M2/E1 GREEN/SEALED, M3 INSTRUMENT FAILURE (provisional advancement [BAR-Entry 52]). Provenance log reviewed through Entry 72. STATE.md reviewed. Constitution published in-repo at `docs/ARCHITECTURAL_CONSTITUTION.md` (v1, SHA-256 `509f11c3...`) and `docs/ARCHITECTURAL_CONSTITUTION_v2.md` (v2 with Amendment 1 and §5). Step 4 ruling: Option A (Entry 72) — M4 scoring gated on L3 resolution; build parallel.
**Role boundary:** The ARCHITECT proposes specification, bars, and sequencing only. No code, no execution, no mechanism implementation, no merge.

---

## 0. Source basis

**Law text source:** `docs/ARCHITECTURAL_CONSTITUTION.md` on GitHub main (P1 — repo-first law). All law quotations in this spec are verbatim from this file, cited by line number (P2 — verbatim quotation).

**Provenance source:** `docs/rulings/provenance_log.md` on GitHub main. All provenance citations verified against actual entry text before commit (P6). Provenance reviewed through Entry 76 (Rebecca's nine Step 7 gate rulings).

**Constitutional amendments:** Amendment 1 (Entry 27, L4/E1 test redefined) recorded in `docs/ARCHITECTURAL_CONSTITUTION_v2.md` Amendment Log. Amendment 2 (Entry 72, Step 4 ruling) — Option A: M4 scoring gated on L3 resolution; build parallel. No constitution law text amended.

**Step 4 ruling source:** Entry 72 [BAR-Entry 72] — Principal ruling: §6.3/L3 sequencing contradiction resolved — Option A. M4 spec §8 amended per this ruling (Amendment 5 below).

**Step 7 gate rulings source:** Entry 76 [Entry 76 — Principal ruling: Step 7 gate] — Rebecca's nine gate rulings (L7 inference, L10 threshold, L8 severity matching, borderline handling, L7 peer conditions, graveyard-gate scope, timebox, L10 seeds, tolerance calibration). All nine implemented in v1.6 and cited by ruling number below.

**This spec does NOT reconstruct any law text.** Where the constitution's law text is insufficient to fully operationalize a test, the gap is flagged as a STOP/escalation trigger (per §5.2 ARCHITECT obligation), not filled by reconstruction.

---

## 1. M4 scope

### 1.1 Laws tested

| Law | Section | Purpose | Source |
|---|---|---|---|
| L7 | §1 Component | Mirror/peer-observer: self-reports calibrated against ground truth AND beat peer-observer | [LAW-L7] |
| L8 | §1 Component | Stakes coupling: homeostatic regulation error rises when self-model calibration degraded | [LAW-L8] |
| L10 | §1 Component | Retrieval honesty: abstention under drift, not blended guess | [LAW-L10] |
| L11 | §2 Interface | One clock — continuous invariant | [LAW-L11] |
| L12 | §2 Interface | One state — continuous invariant | [LAW-L12] |
| L13 | §2 Interface | Memory writes through now — continuous invariant | [LAW-L13] |
| L14 | §2 Interface | Stakes touch everything or nothing | [LAW-L14] |
| L18 | §4 Audit | Contamination controls on every positive claim | [LAW-L18] |
| L19 | §4 Audit | Pre-registration | [LAW-L19] |
| L20 | §4 Audit | Honest naming | [LAW-L20] |

### 1.2 What M4 does NOT test

- **L15/L16/L17 (integration laws):** Fenced to M5. No integration claims, tests, or mechanisms.
- **Re-running M3:** Seeds 201–203 and 301–303 retained, never rerun [BAR-Entry 52, O-14].
- **Modifying M3 verdicts:** INSTRUMENT FAILURE retained.

### 1.3 Prerequisite: L7 graveyard-gate sign-off (v1.6 Ruling 6 — implementation-only authorization) [Entry 76]

Per [BAR-Entry 11.8], L7/M4 is a deferred graveyard gate. Rebecca has signed the graveyard gate for **M4 implementation only** — this authorizes the build (Step 8: INTEGRATOR task-spec extraction → TASK BUILDER implementation) but does NOT authorize scoring.

**Downstream gates retained:** L3 fresh-seed resolution (Option A, Entry 72), FWFP closure audit (Entry 43), CRITIC implementation review, Rebecca's courier-channel scoring authorization. All downstream gates remain in effect. [BAR-Entry 11.8]

---

## 2. L7 — Mirror standard

### 2.1 Verbatim law text (P2)

> **L7 — Mirror standard (from the introspection literature).** Self-reports about internal state must be calibrated against ground-truth internals AND must beat a peer-observer baseline (a matched model predicting this system from its outputs). *Test:* AUROC ≥ 0.75 and ECE ≤ 0.10 on self-state prediction, with the self-vs-peer margin > 0 at p < .05. No margin over the peer = portrait, not mirror — reported as such. Contamination controls (permuted/empty/shuffled) mandatory.

*Source: `docs/ARCHITECTURAL_CONSTITUTION.md`, line 24 [LAW-L7]*

### 2.2 Locked bars

| Bar | Value | Source tag |
|---|---|---|
| AUROC | ≥ 0.75 | [LAW-L7] |
| ECE | ≤ 0.10 | [LAW-L7] |
| Margin (candidate AUROC − peer AUROC) | > 0 at p < .05 | [LAW-L7] |
| Contamination controls | permuted/empty/shuffled mandatory | [LAW-L7] |
| Seeds | 5 | [BAR-Entry 11.3] |
| Inferential policy | all-seeds-direction + bootstrap-CI fallback | [BAR-Entry 11.3] |
| Graveyard gate | Rebecca must sign with prior milestone results | [BAR-Entry 11.8] (gate-decision) (NF3) |

### 2.3 Operational design

**Task:** The candidate and a peer-observer predict properties of the candidate's own recent state. The candidate uses its moving-origin internal representation. The peer-observer uses only observable inputs.

**Peer-observer construction (v1.5 Finding 1 — reconciled with M0 Decision Sheet line 20 and Constitution L7):**

The Constitution L7 text states: "a peer-observer baseline (a matched model predicting this system from its outputs)" [LAW-L7, line 24]. The M0 Decision Sheet (line 20) specifies: "Peer spec: same params/data/architecture, observation channel = behavioral outputs only, self-report channel excluded" [BAR-Entry 11].

The peer-observer is a **matched model** — same parameters, same training data, same architecture as the candidate.
- **Architecture:** Same as candidate. The peer uses the same model architecture (not a fixed linear baseline as in v1.4). [BAR-Entry 11]
- **Parameters:** Same initialization and parameter count as candidate. [BAR-Entry 11]
- **Training data:** Same fitting-origin data as candidate, completed before evaluation. No online learning. [BAR-Entry 11]
- **Observation channel:** Behavioral outputs only (append-log, query stream, external events). [BAR-Entry 11]
- **Excluded channels:** Candidate's internal state, self-report channel, confidence estimates, moving-origin representation. [BAR-Entry 11]
- **Confidence:** The peer generates its own confidence estimate from its observation channel — same method as candidate but without privileged self-state access. [PROPOSED — requires Rebecca sign-off]
- **Rationale:** A matched-model peer is the Constitution's requirement ("matched model"). If the candidate's moving origin provides privileged self-state access, it should beat an identical architecture that sees only behavioral outputs. The M0 Decision Sheet locked this specification. [BAR-Entry 11]

**Peer-observer parity conditions (v1.6 Ruling 5) [Entry 76]:**

Per Rebecca's ruling, the following parity conditions are binding on the candidate and peer:
- **Identical confidence calibration:** Both candidate and peer use the same pre-registered confidence calibration procedure. [BAR-Entry 11]
- **Identical evaluation data:** Both candidate and peer are evaluated on the same evaluation data set. [BAR-Entry 11]
- **Identical ECE definition:** Both candidate and peer use the same ECE computation (same bins, same binning method). [BAR-Entry 11]
- **Identical binning:** Both candidate and peer use the same binning for all binned metrics. [BAR-Entry 11]
- **Paired independently trained instances:** Candidate and peer are trained as a paired set — same data, same architecture, same initialization seed — but independently (the peer does not see the candidate's internal state during training). [BAR-Entry 11]

Sources: Constitution L7 line 24 [LAW-L7]; M0 Decision Sheet line 20 [BAR-Entry 11].

**Prior OLS baseline (v1.1–v1.4):** The fixed OLS baseline is superseded by the matched-model requirement. The OLS baseline was an ARCHITECT design choice that did not match the Constitution's "matched model" language or the M0 Decision Sheet's peer spec. Corrected in v1.5.

**Portrait clause [LAW-L7]:** No margin over the peer = portrait, not mirror — reported as such. If the candidate does not beat the peer, the verdict is KILL (not INSTRUMENT_FAILURE), and the result is reported as "portrait, not mirror."

### 2.4 Controls (L18 battery)

| Control arm | Expected behavior | Failure routing |
|---|---|---|
| Empty | Chance AUROC (0.5) | INSTRUMENT_FAILURE if deviates > 0.05 [PROPOSED — requires Rebecca sign-off] |
| Permuted | Labels shuffled — collapse to chance | INSTRUMENT_FAILURE if AUROC > 0.55 [PROPOSED — requires Rebecca sign-off] |
| Shuffled | Input order shuffled — degrade | INSTRUMENT_FAILURE if shuffled AUROC > candidate AUROC [PROPOSED — requires Rebecca sign-off] |
| Oracle | Full ground-truth — AUROC ≈ 1.0 | INSTRUMENT_FAILURE if AUROC < 0.95 [PROPOSED — requires Rebecca sign-off] |
| Naive | Simple heuristic — above chance, below candidate | KILL if naive AUROC ≥ candidate AUROC [PROPOSED — requires Rebecca sign-off] |
| Frozen | State frozen — chance | INSTRUMENT_FAILURE if AUROC > 0.55 [PROPOSED — requires Rebecca sign-off] |

### 2.5 Kill conditions

**L7 inference policy (v1.6 Ruling 1 — Rebecca's Option C) [Entry 76]:**

Per Rebecca's ruling, L7 bars are split into two categories:

1. **AUROC and ECE are per-seed threshold bars:** any-seed fail → KILL, no fallback. These are absolute quality bars — the candidate must meet them on every seed. [LAW-L7] [BAR-Entry 11]

2. **Candidate–peer margin is a direction test:** evaluated across 5 paired seeds using all-seed direction consistency and a pooled paired-bootstrap 95% CI excluding zero (the M0 Entry 11.3 fallback policy). The margin must be directionally positive across all seeds AND the pooled bootstrap 95% CI must exclude zero. [BAR-Entry 11.3] (M0 Decision Sheet line 29)

The v1.4 "Amendment 3" hard rule (no fallback for any L7 bar) is retracted. The v1.5 STOP/escalation is resolved by this ruling. [P5 — authorized by Rebecca's ruling]

- Candidate AUROC < 0.75 [LAW-L7] on any seed → KILL (per-seed threshold bar, no fallback)
- ECE > 0.10 [LAW-L7] on any seed → KILL (per-seed threshold bar, no fallback)
- Margin: not directionally positive across all 5 seeds OR pooled bootstrap 95% CI includes zero [BAR-Entry 11.3] → KILL (direction test with M0 fallback policy)

### 2.6 No-clean-only self-report rule (BF5 resolution, retained)

The L7 query battery includes clean and adversarial queries (distribution-shifted). AUROC and margin computed over combined set. L18 control arms serve as adversarial splits. L10 drifted regime cross-validates.

---

## 3. L8 — Stakes coupling

### 3.1 Verbatim law text (P2)

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

*Source: `docs/ARCHITECTURAL_CONSTITUTION.md`, line 26 [LAW-L8]*

### 3.2 Locked bars

| Bar | Value | Source tag |
|---|---|---|
| Minimum dose levels | ≥ 3 | [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70) |
| Spearman ρ (monotonic) | ≥ 0.8 | [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70) |
| Standardized slope | ≥ 0.2 | [BAR-Entry 11] (M0_DECISION_SHEET line 21; Entry 70) |
| Monotonic test | All-seeds-direction + bootstrap-CI fallback | [BAR-Entry 11.3] |
| Seeds | 5 | [BAR-Entry 11.3] |
| Specificity ("only then") | Self-model degradation must be the cause; non-self-model noise must NOT raise regulation error | [LAW-L8] |

**M0_DECISION_SHEET quotation (line 21, for fidelity):** "**L8** | ≥3 noise doses; Spearman ρ ≥ 0.8 monotonic; standardized slope ≥ 0.2 (ARCHITECT's candidate accepted); specificity control mandatory (self-irrelevant dose must NOT move regulation error). Seeds: 5." [BAR-Entry 11]

**Tag reconciliation note:** The ≥3-doses bar was previously tagged [OP-Entry 11.7] (supplemental). The M0_DECISION_SHEET (published via G0-4, Entry 70) attributes all L8 bars including ≥3 doses to [BAR-Entry 11] as Rebecca-locked bars. The sheet's framing is canonical; [BAR-Entry 11] is now the primary tag. [OP-Entry 11.7] remains as the §9 operationalization record that adopted the ≥3-level requirement from CRITIC Risk 2 (Entry 7) into the spec.

### 3.3 Operational design (F1.1 correction — respecified from verbatim text)

The previous v1.2 spec operationalized L8 as prediction-horizon dose-response (h=1/h=3/h=5). This was a reconstruction error — the verbatim law text specifies a different test.

#### 3.3.1 L8 homeostatic-variable prerequisite (Amendment 4)

The L8 homeostatic-variable definition is a named prerequisite with its own dedicated reviewer pass. No L8 implementation may proceed until the prerequisite is cleared. The reviewer (CRITIC or Rebecca-delegated) must verify:

| Criterion | Requirement | Source |
|---|---|---|
| Regulable | The variable has a defined regulation target and can deviate from it | [LAW-L8] |
| Target defined | The regulation target is a specific numeric value or bound, not a vague aspiration | [PROPOSED — requires Rebecca sign-off] |
| Calibratable noise dose | Noise can be injected into the self-model at ≥ 3 distinguishable levels [OP-Entry 11.7] | [OP-Entry 11.7] |
| Constructible specificity control | A non-self-model component can receive the same noise injection to test the "only then" specificity leg [LAW-L8] | [LAW-L8] |

**Reviewer pass:** Dedicated CRITIC review of the homeostatic-variable design before implementation. The reviewer verifies all four criteria are met. If any criterion is unmet, the prerequisite is BLOCKED and the design is returned to ARCHITECT for revision.

**Placement in build sequence:** After spec approval (Step 7) and before TASK BUILDER implementation (Step 8). The prerequisite review is a sub-step of the build sequence, not a scoring gate.

**Homeostatic variable:** Define ≥ 1 [LAW-L8] homeostatic variable with a regulation target. The candidate maintains this variable (e.g., a resource level, error budget, or calibration metric) that should stay within bounds for healthy operation.

**Calibrated-noise injection:** Inject calibrated noise into the self-model (the L7 mirror component — the candidate's self-state representation) at ≥ 3 dose levels [BAR-Entry 11]. Dose levels are amounts of perturbation applied to the self-model's state estimation:
- **Level 0 (zero-noise baseline):** No perturbation — self-model at full calibration. This is the reference point for the dose-response. Regulation error at Level 0 is the baseline; all higher-dose regulation errors are compared against it. [Rebecca-approved (Ruling 3, Entry 76)]
- **Level 1 (low):** Small perturbation — self-model slightly degraded
- **Level 2 (medium):** Moderate perturbation — self-model measurably degraded
- **Level 3 (high):** Large perturbation — self-model significantly degraded

**Regulation error measurement:** At each dose level, measure the regulation error of the homeostatic variable — how far it deviates from its target. The law requires regulation error to **rise dose-dependently** [LAW-L8] as self-model calibration is degraded.

**Pre-registered direction:** Regulation error INCREASES as self-model noise dose increases. regulation_error(h=1 dose) < regulation_error(h=2 dose) < regulation_error(h=3 dose). All-seeds-direction test requires this on all 5 seeds [BAR-Entry 11.3]. (NF1 resolution: replaced "accuracy" with "regulation error" for terminology clarity.)

**"Only then" specificity leg [LAW-L8] (v1.6 Ruling 3 — standardized proximal-component effect) [Entry 76]:**

Inject calibrated noise into a NON-self-model component (e.g., the controller's action selection, or the memory store). The severity matching is based on a **pre-registered standardized proximal-component effect**, not raw perturbation magnitude:

1. **Predefine the comparison component:** Which non-self-model component receives the perturbation (selected before any data exists). [Rebecca-approved (Ruling 3, Entry 76)] [LAW-L19]
2. **Predefine the perturbation type and magnitude:** The perturbation is standardized to the self-model dose at each level — the perturbation applied to the non-self-model component is calibrated to produce an equivalent standardized effect on the proximal component as the self-model dose produces on the self-model. [Rebecca-approved (Ruling 3, Entry 76)] [LAW-L19]
3. **Predefine the calibration set:** The set on which the standardized effect is calibrated (separate from scoring seeds). [Rebecca-approved (Ruling 3, Entry 76)] [LAW-L19]
4. **Predefine the tolerance:** The acceptable deviation from exact severity match (the match need not be perfect, but the tolerance is pre-registered). [Rebecca-approved (Ruling 3, Entry 76)] [LAW-L19]

The homeostatic regulation error must NOT rise when severity-matched noise is injected into non-self-model components. [LAW-L8]

**Pre-registration:** All four predefinitions above are pre-registered before any data exists. [LAW-L19]

**Supplementary probe (not load-bearing for L8 claim):** The h=1/h=3/h=5 prediction-horizon design from v1.2 may be retained as a supplementary diagnostic probe, but it does not carry the L8 claim.

### 3.4 L18 control arms for L8

| Control arm | Expected behavior | Failure routing | Source |
|---|---|---|---|
| Empty | No self-model — regulation error constant | INSTRUMENT_FAILURE if any level deviates from baseline | [PROPOSED — requires Rebecca sign-off] |
| Permuted | Self-model noise labels shuffled — no dose-response | INSTRUMENT_FAILURE if monotonic trend persists | [PROPOSED — requires Rebecca sign-off] |
| Shuffled | Self-model input order shuffled — degraded dose-response | INSTRUMENT_FAILURE if exceeds candidate at any level | [PROPOSED — requires Rebecca sign-off] |
| Oracle | Full ground-truth self-model — should show SAME or STRONGER dose-response | INSTRUMENT_FAILURE if no expected degradation pattern | [PROPOSED — requires Rebecca sign-off] |
| Naive | Fixed heuristic self-model — weaker dose-response | KILL if naive outperforms candidate (mechanism not contributing) | [PROPOSED — requires Rebecca sign-off] |
| Frozen | Self-model frozen at initial value — no dose-response (no calibration to degrade) | KILL if frozen shows monotonic trend (stakes decorative) | [LAW-L8] |

### 3.5 Kill conditions

- Non-monotonic dose-response on any seed (after bootstrap-CI fallback) [BAR-Entry 11.3] → KILL
- Frozen arm shows dose-response [LAW-L8] → KILL (stakes decorative)
- Non-self-model noise raises regulation error [LAW-L8] ("only then" violated) → KILL

### 3.6 Instrument failure conditions

- Oracle arm does not show expected degradation pattern → INSTRUMENT_FAILURE
- Empty arm shows non-chance regulation at any level → INSTRUMENT_FAILURE
- Reproducibility check fails → INSTRUMENT_FAILURE

---

## 4. L10 — Retrieval honesty

### 4.1 Verbatim law text (P2)

> **L10 — Retrieval honesty (from the paged-memory work).** Below-threshold matches produce abstention, never a blended guess; abstention calibration measured under drift, not only clean splits. *Test:* drifted-regime AUROC is the reported number; the clean number is a ceiling, not a claim.

*Source: `docs/ARCHITECTURAL_CONSTITUTION.md`, line 30 [LAW-L10]*

### 4.2 Locked bars

| Bar | Value | Source tag |
|---|---|---|
| Abstention under drift | ≥ 50% | [BAR-Entry 11.6] |
| Abstention when clean | ≤ 10% | [BAR-Entry 11.6] |
| Drifted-AUROC floor | ≥ 0.70 | [BAR-Entry 14] (CRITIC falsifiability review) |
| Seeds | 5 (confirmed by Rebecca, matching L7/L8 5-seed policy) | [BAR-Entry 11.3] (v1.6 Ruling 8) [Entry 76] |
| Reporting rule | Drifted-regime AUROC is the reported number; clean is a ceiling, not a claim | [LAW-L10] |

### 4.3 Confidence threshold and AUROC definitions (v1.6 Ruling 2 — Rebecca's ruling) [Entry 76]

**Confidence definition:** The candidate's confidence estimate is a scalar output in [0, 1] representing the candidate's assessed probability that its prediction is correct. The confidence estimate is generated by the candidate's self-model (L7 mirror component) from its internal state representation. [BAR-Entry 11]

**Primary drifted AUROC:** Computed over the complete fixed drifted population using **pre-abstention scores** — the candidate's confidence/ranking before abstention is applied. This closes the abstention-exclusion gaming surface: the candidate cannot inflate its AUROC by abstaining on hard cases. [BAR-Entry 14] [LAW-L10]

**Answered-case AUROC:** Reported separately (non-abstained drifted cases), but is **not the headline**. The primary metric is the pre-abstention drifted AUROC. [BAR-Entry 14] [LAW-L10]

**All-abstain AUROC:** If the candidate abstains on all drifted cases, the drifted-regime AUROC **fails the ≥ 0.70 floor** [BAR-Entry 14]. All-abstain is not N/A — it is a failure. The candidate cannot escape the AUROC floor by abstaining on everything. [BAR-Entry 14]

**τ calibration:** Calibrated on held-out calibration data (separate from scoring seeds) to satisfy **both** drift ≥ 50% abstention [BAR-Entry 11.6] AND clean ≤ 10% abstention [BAR-Entry 11.6]. The threshold τ is the value that satisfies both constraints on the calibration set. [BAR-Entry 11.6] [BAR-Entry 11]

**AUROC population:** The primary drifted-regime AUROC is computed over the complete fixed drifted-regime population (pre-abstention) across all scoring seeds. The clean-regime AUROC (ceiling) is computed over the complete clean-regime population. [LAW-L10]

**Drifted-AUROC floor (locked bar, preserved):** The drifted-regime AUROC ≥ 0.70 [BAR-Entry 14] is a locked bar — value unchanged. What changes in v1.6 is the population it is computed over (pre-abstention, complete fixed population) and the anti-gaming design (all-abstain = failure). [BAR-Entry 14]

**Confidence threshold:** τ is calibrated per the method above. The specific value is determined by the calibration set, not pre-specified. [BAR-Entry 11.6] [BAR-Entry 11]

### 4.4 Clean-regime specificity control

- **Clean regime:** Non-drifted inputs. Abstention ≤ 10% [BAR-Entry 11.6].
- **Drifted regime:** Distribution-shifted inputs. Abstention ≥ 50% [BAR-Entry 11.6].
- **Specificity (frozen arm):** Frozen-state candidate should NOT show differential abstention between clean and drifted. If it does, abstention is a generic input-difficulty response, not calibration [LAW-L10].

### 4.5 L18 control arms for L10

| Control arm | Expected behavior | Failure routing |
|---|---|---|
| Empty | No data — abstain 100% | INSTRUMENT_FAILURE if abstention < 100% [PROPOSED — requires Rebecca sign-off] |
| Permuted | Confidence labels shuffled — no differential abstention | INSTRUMENT_FAILURE if differential abstention persists [PROPOSED — requires Rebecca sign-off] |
| Shuffled | Input order shuffled — reduced differential abstention | INSTRUMENT_FAILURE if exceeds candidate's pattern [PROPOSED — requires Rebecca sign-off] |
| Oracle | Full ground-truth — abstain ~0% in both regimes | INSTRUMENT_FAILURE if abstains > 10% in either regime [PROPOSED — requires Rebecca sign-off] |
| Naive | Fixed confidence — minimal differential abstention | KILL if naive outperforms candidate's calibration [PROPOSED — requires Rebecca sign-off] |
| Frozen | State frozen — no differential abstention | INSTRUMENT_FAILURE if frozen shows differential abstention [PROPOSED — requires Rebecca sign-off] |

### 4.6 Kill conditions

- Abstention < 50% under drift [BAR-Entry 11.6] on any seed → KILL
- Abstention > 10% when clean [BAR-Entry 11.6] on any seed → KILL
- Drifted-AUROC < 0.70 [BAR-Entry 14] on any seed → KILL

### 4.7 Reporting rule (F1.3 correction)

Per [LAW-L10]: "drifted-regime AUROC is the reported number; the clean number is a ceiling, not a claim." The M4 scoring report must:
- Report drifted-regime AUROC as the primary accuracy metric
- Report clean-regime AUROC as a ceiling (upper bound), explicitly labeled as such
- Not cite clean-regime AUROC as a standalone claim

---

## 5. L14 — Stakes touch everything or nothing

### 5.1 Verbatim law text (P2)

> **L14 — Stakes touch everything or nothing.** The homeostatic variables (L8) must be readable by the self-model, affected by memory quality, and predictive targets for the thick present. A stakes module only one component can see is decorative.

*Source: `docs/ARCHITECTURAL_CONSTITUTION.md`, line 40 [LAW-L14]*

### 5.2 Locked bars

| Bar | Value | Source tag |
|---|---|---|
| Effect size (primary) | d ≥ 0.5 | [BAR-Entry 11.4] |
| Correlation (weakest) | corr ≥ 0.3 at 3 seeds | [BAR-Entry 14] (watch item W5) |
| Continuous invariant | Tested at every milestone | [LAW-L14] |

### 5.3 Operational design (F1.2 correction — three couplings from verbatim text)

L14 requires three couplings between the homeostatic variables (L8) and other system components:

**Coupling 1 — Readable by the self-model [LAW-L14]:** The candidate's self-model (L7 mirror component) can read the homeostatic variable's current value. Test: the self-model's state prediction includes the homeostatic variable, and its prediction accuracy for the homeostatic variable is above chance.

**Coupling 2 — Affected by memory quality [LAW-L14]:** Degrading the memory system (e.g., frozen-origin arm, shuffled input) measurably affects the homeostatic variable's regulation error. Test: compare regulation error under normal memory vs. degraded memory; degradation must increase regulation error.

**Coupling 3 — Predictive targets for the thick present [LAW-L14]:** The thick present (L3 state object) includes the homeostatic variable as a predictive target. Test: the candidate's next-input prediction at horizon H includes the homeostatic variable, and prediction accuracy for it is above chance.

**Bars:** d ≥ 0.5 [BAR-Entry 11.4] for each coupling's effect size. corr ≥ 0.3 at 3 seeds [BAR-Entry 14] as weakest inferential bar. A stakes module only one component can see is decorative [LAW-L14] → KILL.

### 5.4 Kill conditions

- d < 0.5 for any coupling [BAR-Entry 11.4] → KILL
- corr < 0.3 at 3+ seeds for any coupling [BAR-Entry 14] → KILL
- Homeostatic variable not readable by self-model [LAW-L14] → KILL (decorative)

### 5.5 No-clean-only self-report rule (BF5 resolution, retained)

L14 computed over combined query set (clean + adversarial). L18 control arms prevent clean-only PASS.

---

## 6. L18 — Full battery

### 6.1 Verbatim law text (P2)

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

*Source: `docs/ARCHITECTURAL_CONSTITUTION.md`, line 52 [LAW-L18]*

### 6.2 Required arms

Full L18 battery at every milestone [LAW-L18]: empty, permuted, shuffled, oracle, naive, frozen. 3+ seeds [LAW-L18]; 5 seeds for L7/L8 [BAR-Entry 11.3].

### 6.3 V4.4 stochastic control framework

M4 uses V4.4 framework (SHA-256-CTR-FY, 1000 null replicates, plus-one upper-tail p-value, alpha_family = 0.05, alpha_seed = 0.05/3) [OP-Entry 11.7] as implemented at M3 (V4.4 alpha_seed specifics per M3 implementation entries in provenance log). Reproducibility-contract semantic digest used for reproducibility verification.

**Stochastic families per law:** 3 per law (frozen, permuted, shuffled) — these use V4.4 RNG-driven randomization with null distributions. Oracle, naive, empty are deterministic (direct threshold evaluation). Total stochastic checks: 3 laws × 3 families × 5 seeds = 45.

**Alpha structure:** alpha_seed = alpha_family / number_of_tested_laws = 0.05/3 [OP-Entry 11.7]. Cross-law Bonferroni, not per-family-within-law.

---

## 7. Multiplicity documentation

### 7.1 M4 multiplicity plan

| Element | Value | Source tag |
|---|---|---|
| Scoring seeds | 5 (fresh, Rebecca-authorized via courier) | [BAR-Entry 11.3] |
| Seed pools | 1 pool of 5 seeds | [PROPOSED — derived from single-pool design] (NF4) |
| Familywise alpha | 0.05 | [OP-Entry 11.7] |
| alpha_seed | 0.05/3 ≈ 0.0167 (cross-law Bonferroni) | [OP-Entry 11.7] |
| Stochastic families per law | 3 (frozen, permuted, shuffled) | [OP-Entry 11.7] |
| Total stochastic checks | 45 | [PROPOSED — derived: 3 laws × 3 families × 5 seeds] (NF4) |
| L14 | Deterministic (no stochastic family; direct threshold per seed) | [LAW-L14] |
| Reproducibility | Semantic digest comparison (both passes) | [OP-Entry 11.7] |

### 7.2 Hold-out seed rule

≥ 2 seeds unseen in development per scoring run. Development seeds: 101–105 [OP-Entry 11.7, O-15].

### 7.3 FWFP closure deliverable (Amendment 1 — Entry 43 standing rule)

**Named deliverable:** M4 Pre-Scoring FWFP Closure Audit

**Standing rule source:** Entry 43 [BAR-Entry 43] — "every scoring spec's closure audit must compute FWFP of each arm's full check battery and correct any control whose FWFP exceeds 5% BEFORE scoring."

**Owner:** TASK BUILDER (computation and correction performed under O-15 diagnostic-only). The ARCHITECT specifies the deliverable; the TASK BUILDER produces it.

**Acceptance criteria:**
1. Every control arm's full check battery (all stochastic families × all checks per arm) is enumerated.
2. The FWFP (familywise false-positive rate) of each arm's full check battery is computed by direct enumeration or simulation.
3. Any arm whose FWFP exceeds 5% is corrected (e.g., by alpha adjustment, directionality restriction, or null-of-the-max procedure per Entry 43 remedy).
4. The corrected FWFP for every arm is ≤ 5%.
5. The closure audit is documented in a committed artifact with all computations traceable.
6. The closure audit is reviewed by CRITIC before scoring authorization.

**Corrected-alpha target:** Every arm's full-battery FWFP ≤ 5% [BAR-Entry 43]. The specific corrected alpha for each arm is determined by the TASK BUILDER's computation, not pre-specified by the ARCHITECT — the ARCHITECT specifies the target (≤ 5%), not the method.

**Milestone-wide family (v1.5 Finding 2 — extended scope):** In addition to the per-arm audit, the closure audit must also control the **milestone-wide family** of ALL control-triggering tests across M4. This means:
1. Enumerate every control-triggering test across all laws tested at M4 (L7, L8, L10, L14, L18 control arms).
2. Compute the milestone-wide FWFP across the full set of control-triggering tests.
3. Correct any test whose inclusion pushes the milestone-wide FWFP above 5%.
4. The milestone-wide FWFP ≤ 5% [BAR-Entry 43] is an acceptance criterion in addition to the per-arm criterion.

The per-arm audit ensures no single arm's battery is inflated; the milestone-wide audit ensures the family of all controls across the milestone is not inflated. Both must pass. [BAR-Entry 43]

**Context (why this deliverable is required):** The current §7.1 alpha_seed = 0.05/3 across 45 stochastic checks does not by itself demonstrate closure. A naive per-check reading yields ~53% familywise; even per-family ≤ 5% control leaves ≈ 1 − 0.95⁹ ≈ 37% odds of at least one spurious borderline firing across 9 family batteries. The closure audit verifies and corrects this before any scoring run. [BAR-Entry 43]

**Placement in build sequence:** Step 8 (TASK BUILDER implementation), as a pre-scoring sub-step. The closure audit must be completed and CRITIC-cleared before Rebecca authorizes scoring via courier.

### 7.4 Borderline pre-registration (Amendment 2 — draft options for Rebecca's ruling)

**Issue:** A single within-FWFP borderline control firing at M4 (i.e., a control arm that fires at a p-value within the corrected alpha but near the threshold) must have its label and handling pre-registered before any data exists. No ambiguity may remain for the JUDGE at scoring time.

**Draft options for Rebecca's ruling:**

**Option B1 (M3 precedent):** Label retained. If a borderline control fires, the INSTRUMENT_FAILURE or KILL label is retained as-is. Candidate-facing evidence (if any) may support provisional advancement to the next milestone, but the control firing is not reinterpreted, renamed, or silently dismissed. The M3 precedent (Entry 43) followed this pattern: the shuffled-arm firing was retained as INSTRUMENT_FAILURE, and the correction was a post-scoring spec amendment under the four-part test, not a relabeling. [Rebecca-confirmed B1 (Ruling 4, Entry 76)]

**Option B2 (Strict KILL):** Any borderline control firing, even within-FWFP, results in KILL with no provisional advancement. The candidate must clear all controls with margin. This is the most conservative option: it eliminates any ambiguity about borderline cases but may kill a candidate that would have survived under a more lenient rule. [PROPOSED — requires Rebecca ruling]

**Option B3 (Conditional):** A borderline control firing triggers a Rebecca gate decision at delivery time. The JUDGE reports the firing with all context (which arm, which check, p-value, corrected alpha, margin). Rebecca rules at the delivery gate whether to retain the label, authorize provisional advancement, or KILL. This defers the decision to the gate rather than pre-registering a fixed rule. [PROPOSED — requires Rebecca ruling]

**Pre-registration requirement:** Whichever option Rebecca rules, the ruling is pre-registered in the spec before any data exists. The JUDGE at scoring time applies the pre-registered rule, not an ad-hoc judgment. [LAW-L19]

### 7.5 Borderline numerical definition + B1 handling (v1.6 Ruling 4 — Rebecca confirmed B1) [Entry 76]

**Numerical definition of "borderline":** A control firing is **borderline** if its p-value falls within a pre-specified margin of the corrected-alpha threshold. The margin is defined as: p ∈ [α_corrected × 0.5, α_corrected], where α_corrected is the arm's corrected alpha from the FWFP closure audit (§7.3). This means a p-value between 50% and 100% of the corrected alpha is borderline. [BAR-Entry 43] [LAW-L19]

**The 0.5α–α band is descriptive only (v1.6 Ruling 4):** The borderline band must NOT change the verdict. A borderline firing is handled per B1 regardless of where in the band it falls. The band is for reporting context, not for altering the outcome. [BAR-Entry 43]

**B1 handling (Rebecca confirmed):**

If a borderline control fires (as defined above), the following procedure applies:
1. The INSTRUMENT_FAILURE or KILL label is **retained as-is**. The control firing is not reinterpreted, renamed, or silently dismissed.
2. The firing is reported with full context: which arm, which check, p-value, corrected alpha, margin ratio (p / α_corrected), and all-seeds pattern.
3. Candidate-facing evidence (if any) may support **provisional advancement** to the next milestone, but the control firing remains on the record.
4. Any correction (e.g., spec amendment, methodological fix) follows the Entry 43 four-part test as a post-scoring action, not a relabeling.
5. The M3 precedent (Entry 43) is the model.

[BAR-Entry 43] [LAW-L19] (Rebecca confirmed B1)

### 7.6 Control-arm tolerance calibration procedure (v1.6 Ruling 9 — Rebecca's ruling) [Entry 76]

The control-arm tolerance thresholds in the L7 (§2.4), L8 (§3.4), and L10 (§4.5) control tables are produced by a **pre-registered, candidate-blind, oracle/synthetic-grounded, frozen-before-scoring** procedure:

1. **Pre-registration:** The calibration procedure (method, data source, acceptance criterion) is pre-registered in the spec before any candidate behavior is observed. [LAW-L19] [BAR-Entry 43]

2. **Oracle/synthetic grounding:** Tolerances are calibrated against the oracle arm and synthetic ground-truth (where the true answer is known), NOT against the candidate's diagnostic-seed behavior. The oracle arm provides the positive control; synthetic ground-truth provides known-answer calibration. [BAR-Entry 43] [PROPOSED — requires Rebecca sign-off on method]

3. **Candidate-blind:** The candidate's diagnostic-seed results (seeds 101–105 under O-15) are NOT inputs to the tolerance calibration. Only oracle/synthetic ground-truth is used. The candidate's behavior cannot influence its own control thresholds. [BAR-Entry 43] [O-15]

4. **Frozen before scoring:** Once computed and CRITIC-verified, the tolerances are locked and cannot be adjusted after the candidate runs. Any post-candidate adjustment is prohibited and would be visible in the provenance. [BAR-Entry 43] [LAW-L19]

5. **Role boundary:**
   - **ARCHITECT** specifies the procedure (method, data source, acceptance criterion).
   - **TASK BUILDER** computes the actual tolerance numbers under O-15 (diagnostic-only).
   - **CRITIC** verifies the execution (candidate-blind, oracle-grounded, frozen).
   - **Rebecca** signs off on the method and criterion, not the numbers.
   [BAR-Entry 43]

6. **Acceptance criterion:** Each control arm's false-positive rate ≤ a pre-specified threshold. The ARCHITECT specifies the threshold target; the TASK BUILDER computes to satisfy it. The threshold is calibrated to be consistent with the FWFP closure audit's familywise rate (§7.3). [BAR-Entry 43] [PROPOSED — requires Rebecca sign-off on criterion]

**What this adds:** The existing failure-routing rules in the control-arm tables (Empty/Permuted/Shuffled/Oracle/Naive/Frozen) are preserved. What is added is the numerical tolerance calibration procedure that produces the thresholds those routings reference. The [PROPOSED] tags on the existing tolerance values in §2.4, §3.4, and §4.5 are now governed by this procedure — the numbers will be computed by the TASK BUILDER under this procedure, not pre-specified by the ARCHITECT.

---

## 8. Open work items — M4 scope

| Open item | Scope? | Disposition |
|---|---|---|
| Multiplicity documentation | In scope | §7 |
| Fresh-seed scoring authorization | Prerequisite | Rebecca must authorize via courier |
| L3 control calibration resolution | Prerequisite for scoring | M3 L3 issue; M4 tests different laws. Build (implementation, diagnostic runs) proceeds in parallel. M4 scoring is gated on prospective L3 calibration resolution on fresh seeds, per governance paper §6.3(3). [BAR-Entry 72] |
| Reproducibility contract independent use | In scope | M4 harness must use repaired semantic digest (§6.3) |
| Full independent recomputation from M3 raw artifact tree | Deferred | Parallel verification, not M4 scope |

**Sequencing note (Amendment 5 — Option A, Step 4 ruling [BAR-Entry 72]):** Per governance paper §6.3(3), no M4 scoring run is authorized until L3 control calibration is resolved prospectively on fresh seeds. M4 build (TASK BUILDER implementation, diagnostic runs under O-15) proceeds in parallel with L3 calibration work. The gate sequence is: (1) L3 resolution on fresh seeds; (2) M4 scoring authorization via Rebecca's courier channel; (3) M4 scoring execution.

---

## 9. Sequencing plan

### 9.1 Role assignments

| Step | Role | Deliverable |
|---|---|---|
| 1 | ARCHITECT | This specification (v1.6) + changelog + handoff |
| 2 | CRITIC | Fresh-context delta re-clear with law-diff table |
| 3 | WORKFLOW COORDINATOR | Step 7 package assembly |
| 4 | Rebecca | Approve M4 spec + L7 graveyard-gate sign-off + L10 threshold + borderline ruling + timebox |
| 5 | INTEGRATOR | Task spec extraction |
| 6 | CRITIC | L8 homeostatic-variable prerequisite review (§3.3.1) |
| 7 | TASK BUILDER | M4 harness implementation + FWFP closure audit (§7.3) |
| 8 | CRITIC | Implementation verification + FWFP closure audit review |
| 9 | INTEGRATOR | Courier packet |
| 10 | Rebecca | Supervised scoring execution (gated on L3 resolution [BAR-Entry 72]) |
| 11 | JUDGE | Scoring ruling |
| 12 | CRITIC | Results review |
| 13 | Rebecca | M4 delivery gate ruling |

### 9.2 Timebox (v1.6 Ruling 7 — Rebecca-approved) [Entry 76]

| Parameter | Value |
|---|---|
| Sessions | 6 [Rebecca-approved] |
| Calendar days | 14 [Rebecca-approved] |
| Tripwire (sessions) | 3 [Rebecca-approved] |
| Tripwire (days) | 7 [Rebecca-approved] |

**Exclusions:** External-review waiting time and L3-gate waiting time are excluded from the timebox clock. The clock runs on M4 build work only, not on waiting for dependent gates. [Rebecca-approved]

---

## 10. L15–L17 integration fence

No L15, L16, or L17 work authorized before M5. This spec does not propose integration tests, mechanisms, or claims.

---

## 11. Constraints

- No bars, controls, or scoring logic from M1–M3 modified.
- No scoring run, no fresh seeds (until Rebecca authorizes via courier).
- No rerun of seeds 201–203 or 301–303 [O-14].
- Development runs diagnostic-only [O-15].
- O-14, O-15, D1–D5, L9, L18 all binding.
- L15/L16/L17 forbidden before M5.
- ≥ 2 unseen scoring seeds per scoring run.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
- Rebecca sole gate/merge authority.
- §5 Versioned-Law Compliance Protocol (P1–P6) binding.

---

## 12. Items requiring Rebecca's decision (v1.6 — nine rulings resolved)

| Item | What | Status |
|---|---|---|
| L7 graveyard-gate sign-off | Signed for M4 implementation only (not scoring) | [BAR-Entry 11.8] — RESOLVED (Ruling 6) |
| L10 confidence threshold | τ dual-calibrated (drift ≥50%, clean ≤10%); value determined by calibration | [BAR-Entry 11.6] — RESOLVED (Ruling 2) |
| L10 confidence/threshold definitions | Pre-abstention AUROC, all-abstain=fail, τ calibration method (§4.3) | [BAR-Entry 14] — RESOLVED (Ruling 2) |
| L10 seed count | 5 confirmed by Rebecca | [BAR-Entry 11.3] — RESOLVED (Ruling 8) |
| M4 timebox | 6 sessions / 14 days, tripwire 3/7, excludes waiting time | [Rebecca-approved] — RESOLVED (Ruling 7) |
| L8 homeostatic variable | Named prerequisite with dedicated reviewer pass (§3.3.1) | RESOLVED by §3.3.1 reviewer pass |
| Control-arm tolerances | Pre-registered/candidate-blind/oracle-grounded/frozen procedure (§7.6) | [BAR-Entry 43] — RESOLVED (Ruling 9) |
| Borderline control firing handling | B1 confirmed (label retained, provisional advancement possible) | [BAR-Entry 43] — RESOLVED (Ruling 4) |
| Borderline numerical definition | p ∈ [α_corr × 0.5, α_corr]; band is descriptive only | [BAR-Entry 43] [LAW-L19] — RESOLVED (Ruling 4) |
| L7 inference policy | AUROC/ECE per-seed KILL; margin direction test with M0 fallback | [BAR-Entry 11.3] — RESOLVED (Ruling 1) |
| L7 peer confidence method | Matched-model with identical calibration/eval/ECE/binning + paired training | [BAR-Entry 11] — RESOLVED (Ruling 5) |
| L8 zero-noise baseline | Level 0 approved as dose-response reference | [Rebecca-approved] — RESOLVED (Ruling 3) |
| L8 severity-matched specificity | Standardized proximal-component effect (4 predefinitions) | [LAW-L19] — RESOLVED (Ruling 3) |

**Items still requiring Rebecca sign-off (method/criterion, not numbers):**
- L8 standardized specificity: comparison component, perturbation type, calibration set, tolerance — pre-registered [PROPOSED — requires Rebecca sign-off] (Ruling 3)
- Tolerance calibration: method and acceptance criterion — [PROPOSED — requires Rebecca sign-off] (Ruling 9)

**Provenance note (F1.5 correction):** The L7 numeric bars (AUROC ≥ 0.75, ECE ≤ 0.10, margin > 0 at p < .05) are in the constitution's law text [LAW-L7, line 24], not from Entry 5. Entry 5 [verified: provenance_log.md line 87] was the JUDGE's measurability assessment, which classified L7 as "fully numeric (judgeable now)" — it did not create the bars. Entry 8 [verified: provenance_log.md line 134] was the JUDGE's ruling on the plan, which identified corrections (L7 controls mandatory, L10 needs kill condition) — it did not lock bars. Bars were locked by Rebecca in Entry 11 [verified: provenance_log.md line 172].

---

## 13. Implementation handoff

**Next recipient:** CRITIC (fresh-context reviewer) for delta re-clear with law-diff table, then WORKFLOW COORDINATOR for the formal Step 7 gate package to Rebecca for her graveyard-gate signature (implementation-only authorization).

**Explicitly prohibited for TASK BUILDER:**
- Modifying any locked bar, threshold, or scoring predicate.
- Running any scoring seeds.
- Running seeds 201–203 or 301–303.
- Implementing L15/L16/L17 or any M5 component.
- Modifying STATE.md or provenance_log.md.
- Renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
