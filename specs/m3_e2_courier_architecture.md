# M3 / E2 COURIER ARCHITECTURE

**Serves: M3 Build/Task-Specification Clearance Gate**
**Status: DRAFT — requires independent CRITIC review; no build authorization**

**Date:** 2026-08-15 · **Author:** INTEGRATOR · **Governing state:** main `856c1868a78a2b0c87275ed53120677cce236fc7`; M2 GREEN/SEALED/ACCEPTED; M3/E2 V4 CRITIC CLEAR; Rebecca M3 GO ruling issued (docs/rulings/REBECCA_M3_GO.md).
**Authority chain:** Rebecca > constitution > M0 decision sheet as adopted > approved M3/E2 V4 specification > this courier architecture > agent judgment.
**Source specification:** `specs/m3_e2_spec_amended_v4.md` · **Implementation task spec:** `specs/m3_e2_implementation_task_spec.md`
**Role boundary:** This document defines the courier architecture for M3 scoring runs. It is architecture, not a scoring packet. It does not contain a scoring command, scoring seeds, or any executable artifact. It does not authorize a build cell, task specification execution, scoring packet creation, diagnostic execution, or M3 timebox activation.

---

## 0. Authorization basis

This courier architecture is prepared per Rebecca's M3 GO ruling (docs/rulings/REBECCA_M3_GO.md), Authorization boundary item 2: "INTEGRATOR to prepare the self-contained M3 implementation task specification and courier architecture only."

The ruling explicitly does NOT authorize:
- implementation or code changes;
- activation of a build cell or TASK BUILDER;
- diagnostic execution;
- scoring execution or a courier scoring run;
- exposure or use of hold-out seeds; or
- any L15–L17 integration claim.

This document must receive independent CRITIC clearance before any build authorization returns to Rebecca.

---

## 1. Courier lifecycle

The M3 courier lifecycle follows the established protocol from M0 (Entry 13, courier execution protocol) and M1/M2 (Entries 23–24, 32–34), adapted for M3's four-law scope.

### 1.1 Preconditions (all must be satisfied before any courier packet is prepared)

1. **CRITIC clearance of this task specification and courier architecture** — independent review, no collaboration with ARCHITECT or INTEGRATOR.
2. **Rebecca's build authorization** — separate from the M3 GO ruling, which authorized task-spec/courier-architecture preparation only.
3. **TASK BUILDER implementation** — code committed to the repository, CRITIC-verified (including hold-out seed exposure check per R3 precedent).
4. **INTEGRATOR pre-flight smoke test** — development seeds only (pool {101–105}), NOT hold-out seeds, per O-15. Non-scoring. Deleted after verification.
5. **Current STATE.md** — hash attested, GitHub main verified.

### 1.2 Lifecycle stages

```
[Pre-conditions met]
    ↓
CRITIC reviews task spec + courier architecture → CLEAR or BLOCK
    ↓ (if CLEAR)
Rebecca authorizes build
    ↓
TASK BUILDER implements → CRITIC verifies implementation
    ↓ (if VERIFIED)
INTEGRATOR packages courier scoring packet (one command, expected-output schema, scoring seeds)
    ↓
Rebecca executes scoring run on supervised executor
    ↓
Rebecca returns raw and complete output to RECORDER
    ↓
JUDGE scores from returned artifacts only
    ↓
CRITIC reviews results
    ↓
RECORDER logs provenance entry, updates STATE.md hash
    ↓
Rebecca rules at M3 delivery gate
```

### 1.3 One scoring channel

Per O-15 (Entry 22): all scoring runs execute exclusively through Rebecca's supervised-executor courier channel. Development runs (builder/INTEGRATOR sandbox) are diagnostic-only — never scored, never cited, never logged as results. "One scoring channel."

### 1.4 No re-run-on-failure

Per O-14 (Entry 22): re-run-on-failure is FORBIDDEN — result laundering, never to be proposed again. If a scoring run fails, the failure is diagnosed and logged. A construction-bug fix (specific defect identified, fixed, CRITIC-confirmed) does not consume D2 budget, but the fix must be a genuine construction bug, not "probably a bug."

---

## 2. Packet contents template

When a courier scoring packet is eventually prepared (after all preconditions in §1.1 are met), it must contain:

### 2.1 Required elements

| Element | Description |
|---|---|
| Run ID | Unique identifier (e.g., M3-L1-RUN-1, M3-L3-RUN-1, M3-L5-RUN-1, M3-L6-RUN-1) |
| Command | Verbatim one-command launcher (e.g., `python m3_harness.py --law L1 --seeds ... --output-dir ...`) |
| Scored commit hash | The exact git commit being scored (from GitHub main, verified) |
| Pinned dependencies | Python version, numpy, scipy versions |
| Expected output files | List of expected artifact files with schema |
| Scoring criteria | Pass/fail/KILL/INSTRUMENT FAILURE conditions for each law |
| Scoring seeds | The hold-out pool seeds used (all 3: {201, 202, 203}, ascending order) |
| Hold-out seed policy | Statement that seeds are unseen in development, per standing rule |
| Return obligations | Rebecca returns entire output directory, raw and complete |
| Deviation reporting | Rebecca logs any deviation from pinned deps or command |

### 2.2 What this architecture does NOT contain

- No scoring command (this is architecture, not a packet).
- No hold-out seed values in any development artifact.
- No executable code.
- No diagnostic or scoring output.

**Hold-out seed protection:** Hold-out pool seeds {201, 202, 203} are never exposed in any development artifact, diagnostic run, pre-registration validation, or task specification. They enter the workflow only when INTEGRATOR packages the actual courier scoring packet, at which point they are embedded in the verbatim command sent to Rebecca's supervised executor. The RECORDER's append-only exposure ledger records each seed-use event per `[V4 §8.1]`.

---

## 3. Provenance requirements

### 3.1 Manifest

Every scoring run's manifest must include:
- Commit hash (from GitHub main, verified).
- Scoring seeds (hold-out pool).
- Wall-clock time.
- Python runtime version (self-detected by the script).
- Deviation log (any departure from pinned deps or command).
- File hash list (SHA-256 of each output file).

### 3.2 Round-trip log

Rebecca's executor log must include:
- The verbatim command executed.
- The scored commit hash (fresh checkout verification).
- Repository verification (file count, SHA-256 match or CRLF→LF normalization).
- Exit status.
- Output file list with sizes and hashes.

### 3.3 Lineage attestation

Following the E1 provenance-cure precedent (lineage_attestation.md, commit a85ec91f), the RECORDER must verify:
- The scored commit matches GitHub main at the time of scoring.
- All files in the repository are verified (byte-identical or normalized).
- No unmapped, missing, or substantively different files.
- The manifest's commit_hash is a real repository hash (not "pending — no git repo").

### 3.4 STATE.md attestation

The RECORDER records STATE.md's SHA-256 hash at every merge, making the file tamper-evident. If the RECORDER detects divergence between the provenance log and STATE.md's claims, that is an immediate escalation to Rebecca. STATE.md never self-authenticates (BUILD_PHASE_ORG Ruling 1, binding).

---

## 4. Scoring protections (restated from governing documents)

| Protection | Source | Binding |
|---|---|---|
| ≥2 scoring seeds unseen in development | O-35 standing rule; V4 §8.1 | All milestones |
| Development runs diagnostic-only | O-15 (Entry 22) | All milestones |
| Scoring only through Rebecca's courier channel | O-15 (Entry 22) | All milestones |
| Re-run-on-failure FORBIDDEN | O-14 (Entry 22) | All milestones |
| Returned outputs are ground truth | Entry 13 courier protocol | All milestones |
| JUDGE scores only from returned artifacts | Entry 13 courier protocol | All milestones |
| Incomplete provenance = unscoreable | Entry 13 courier protocol | All milestones |
| Full L18 battery on every positive claim | V4 §2.10, §3.9, §4.8, §5.5 | M3 |
| L9 hard fence (no learned/nonlinear channel) | V4 §9 | M3 |
| D1–D5 Persistence Doctrine | Entry 12 | All milestones |
| No L15–L17 integration claim | V4 §9, §11 | M3 |
| No renaming/suppressing/reframing negatives | Team prompt (Entry 2) | All milestones |
| Construction-bug guard | Entry 27 ruling 4 | D2 budget protection |

---

## 5. §1.1 growth-bar diagnostic-only routing

The L5 growth-bar proposal (candidate per-walk latency growth ≤ 2.0×, fair-naive ≥ 4.0×) remains diagnostic-only and non-gating per Rebecca's ruling (REBECCA_M3_GO.md §"L5 §1.1 proposal"). Adoption, rejection, or modification requires a separate explicit Rebecca ruling.

**Courier routing:** the scoring packet's expected output schema must include the growth-threshold measurements as reported fields, but the JUDGE's scoring criteria must gate solely on the M0-adopted accuracy/chain-walk bars (≥ 0.95 accuracy, chain-walk = 1.00). The growth measurements are reported alongside the verdict, not within it.

---

## 6. Multi-law scoring architecture

M3 tests four laws (L1, L3, L5, L6). The courier architecture supports both per-law and batched scoring:

### 6.1 Per-law scoring packets

Each law may be scored as a separate courier packet with its own run ID, command, and output directory:
- M3-L1-RUN-1: L1 access physics (creation-phase fixture, 2,200 entries, candidate sets, R²/ρ bars).
- M3-L3-RUN-1: L3 thick present (AR(3) generator, 1,010 cycles, state vs raw loss reduction).
- M3-L5-RUN-1: L5 bi-temporality (400 facts: 200 combination + 200 chain, accuracy + walk integrity).
- M3-L6-RUN-1: L6 episodic completeness (3-module graph, 8 attacks, 4-row audit, 6 L18 arms).

### 6.2 Batched scoring (preferred where feasible)

Per BUILD_PHASE_ORG Ruling 2 (Entry 17): INTEGRATOR bundles pending merge candidates, task tests, and smoke tests into single courier sessions wherever possible. If the four laws share a common harness entry point, a single scoring command may run all four laws in one pass, provided:
- Each law's output is in a separate subdirectory.
- Each law's verdict is independently computable from its own subdirectory's artifacts.
- The scoring seeds are the same hold-out pool for all laws.
- The manifest records per-law results.

### 6.3 Per-seed isolation

Per V4 §3.3 (L3 fitting procedure): each scoring seed is fit and evaluated in isolation. No weight reuse across seeds. This principle applies to all laws: each seed's results are computed independently, and the verdict is the conjunction across all scoring seeds.

---

## 7. Instrument-failure handling

### 7.1 Instrument failure is not a candidate kill

Per V4 §2.11, §3.10, §4.9, §5.6: INSTRUMENT FAILURE means the test apparatus is broken, not that the candidate failed. An instrument failure triggers investigation (under the construction-bug guard if a specific defect is identified) and does not consume D2 retry budget. The run is unscoreable, the apparatus is fixed, and the run is repeated — but only after the fix is CRITIC-confirmed, and the repeat is a new scoring run, not a re-run of a failed one.

### 7.2 NF8 operational routing

The L3 permuted arm's exact bound (reduction_h ≤ 0%) is very likely correct but not rigorously proven for all possible fitted weights (NF8, CRITIC V4 review). If a false positive occurs (permuted reduction_h > 0% for some seed), it triggers INSTRUMENT FAILURE, not KILL. The builder must route any such violation to INSTRUMENT FAILURE handling.

### 7.3 NF9 operational labeling

The L5 frozen arm's binary walk accuracy (0.00 or 1.00) is a corner by the Option E lesson's letter but acceptable for an L18 negative control (NF9, CRITIC V4 review). The artifact must label this arm as "L18 negative control" and note the binary nature is inherent to the chain-walk accuracy definition.

---

## 8. NF7–NF10 operational summary

| Finding | Operational handling in courier architecture |
|---|---|
| NF7 (R² reproducibility) | Scoring artifacts must emit raw per-entry accessibility values, per-set ranks, and exact candidate-set construction data. The verification script or exact numpy call sequence must be included or referenced for independent recomputation. |
| NF8 (L3 permuted bound) | Any permuted-arm violation routes to INSTRUMENT FAILURE, never KILL. Builder implements derangement exactly as specified. |
| NF9 (L5 binary walk accuracy) | Frozen arm labeled "L18 negative control." Exact-match walk accuracy (no partial credit). Binary outcome noted as inherent to definition. |
| NF10 (STATE.md currency) | STATE.md updated to reflect V4 CLEAR + M3 GO ruling + B1-B3 fixes; governing commit updated to verified main `856c1868`. RECORDER provenance attestation still pending. NF10 in progress. |

---

## 9. What this courier architecture does NOT authorize

- No build cell activation.
- No TASK BUILDER assignment.
- No diagnostic execution.
- No scoring execution.
- No courier scoring packet creation.
- No hold-out seed exposure.
- No M3 timebox activation by this document. (Rebecca's M3 GO ruling activates the timebox; these documents do not.)
- No L15–L17 integration claim.

This document is architecture for independent CRITIC review only. Build authorization returns to Rebecca only after CRITIC clears both this courier architecture and the companion task specification.

---

## 10. Source manifest

| Document | Project Files path |
|---|---|
| Rebecca M3 GO ruling | `docs/rulings/REBECCA_M3_GO.md` |
| M3/E2 V4 specification | `specs/m3_e2_spec_amended_v4.md` |
| M3/E2 V4 changelog | `specs/m3_e2_spec_changelog_v4.md` |
| CRITIC V4 review (CLEAR) | `reviews/critic_m3_e2_spec_rereview_v4.md` |
| M3 implementation task spec | `specs/m3_e2_implementation_task_spec.md` |
| STATE.md (current) | `state/STATE.md` |
| Provenance log | `docs/rulings/provenance_log.md` |
| ROLE_SESSIONS.md | `state/ROLE_SESSIONS.md` |
| GitHub repository | `darkside73826779-ship-it/moving-origin-research` (main `856c1868`) |

---

— INTEGRATOR, 2026-08-15
