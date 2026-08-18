# M4 Specification — Changelog

**Spec:** `specs/m4_specification.md`
**Date:** 2026-08-18 · **Author:** ARCHITECT
**Base SHA:** `ac75635` (GitHub main)
**Branch:** `architect/m4-specification`

---

## What this specification does

Defines the M4 milestone ("Mirror, Stakes, and Calibration"): what it tests (L7, L8, L10), pre-registered bars and kill conditions, L18 control battery, L14 interface bar, multiplicity plan, open-items scope determination, sequencing plan, timebox proposal, and L15–L17 fence.

## What this specification does NOT do

- Does not implement code (ARCHITECT role boundary).
- Does not authorize scoring (Rebecca must authorize via courier).
- Does not modify any M1–M3 bars, controls, verdicts, or evidence.
- Does not propose L15/L16/L17 work (fenced to M5).
- Does not modify STATE.md or provenance_log.md.
- Does not sign the L7 graveyard gate (Rebecca's authority).

---

## Recovered source basis

The constitution document is not in the repository. All law definitions, bars, and constraints are reconstructed from:
- `docs/rulings/provenance_log.md` — Entries 5–14, 11.3–11.8 (locked bars, operationalizations, graveyard gates, watch items)
- `state/STATE.md` — locked bars, watch items W4/W5, milestone status
- `specs/m3_e2_spec_amended_v4.md` — L11/L13 patterns, L18 battery structure, V4.4 stochastic framework
- `specs/m3_v4_4_implementation_contract_amendment.md` — V4.4 RNG protocol details

Gap flag: exact constitution text for L7/L8/L10 not recoverable. Operational definitions are reconstructed from bars and constraints in provenance. If Rebecca identifies a discrepancy, the constitution controls.

---

## Key design decisions

1. **L7 mirror test:** Candidate vs peer-observer, AUROC ≥ 0.75, ECE ≤ 0.10, margin > 0 at p < .05. Peer sees observable inputs but not candidate's internal state or self-report channel (CRITIC Blocking 2 resolution from Entry 7/9). L18 battery mandatory (Entry 8 correction 3). 5 seeds (Entry 11.3).

2. **L8 dose-dependence:** ≥3 stakes levels, monotonic test with all-seeds-direction + bootstrap-CI fallback (Entry 11.3). Specificity control: frozen arm should NOT show dose-response. Proposed levels: h=1/h=3/h=5 (requires Rebecca approval).

3. **L10 abstention:** Dual bar 50%/10% (Entry 11.6, LOCKED). Drifted-AUROC ≥ 0.70 floor (Entry 14). Confidence threshold τ = 0.70 pre-registered (W4 resolution — requires Rebecca approval). Clean-regime specificity control added (CRITIC non-blocking from Entry 7).

4. **L14 interface bar:** d ≥ 0.5 primary (Entry 11.4, LOCKED); corr ≥ 0.3 at 3 seeds weakest (W5).

5. **Multiplicity:** 5 scoring seeds, 1 pool, Bonferroni at family level, 90 per-seed stochastic checks. ≥2 unseen seeds per scoring run.

6. **Open items:** Multiplicity in scope; L3 calibration parallel (not blocking); reproducibility contract in scope; raw artifact recomputation deferred.

7. **L15–L17 fence:** Respected. No integration claims or tests.

---

## Inputs reviewed

| File | SHA | Purpose |
|---|---|---|
| `docs/rulings/provenance_log.md` | `ac75635` | Constitution law recovery, locked bars, graveyard gates |
| `state/STATE.md` | `ac75635` | Locked bars, watch items, milestone status |
| `specs/m3_e2_spec_amended_v4.md` | `ac75635` | L11/L13 patterns, L18 battery, V4.4 framework |
| `specs/m3_v4_4_implementation_contract_amendment.md` | `ac75635` | V4.4 RNG protocol |
| `docs/governance_paper_final.md` | `ac75635` | Governance context, L3 calibration commitment |
| `GOVERNANCE_SOURCE_MAP.md` | `ac75635` | Constitution not in repo — source map |

---

## Standing constraints verified

- O-14: No seeds rerun.
- O-15: Development runs diagnostic-only.
- D1–D5: Specification committed to branch; no STATE.md or provenance_log.md modification.
- L9, L18: Not touched; L18 battery specified for M4.
- L15/L16/L17: Not introduced. Fence respected.
- ≥2 unseen scoring seeds: Specified in multiplicity plan.
- No renaming negatives: INSTRUMENT FAILURE retained.
- Rebecca sole gate/merge authority: Specification routes to CRITIC, then Rebecca.
