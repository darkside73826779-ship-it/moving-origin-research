# ARCHITECT Handoff — M4 Specification

**Gate served:** M4 milestone specification (Mirror, Stakes, Calibration)
**Issued by:** ARCHITECT
**Date:** 2026-08-18 12:13 EDT

---

## Input SHAs reviewed

| Item | SHA | Verified |
|---|---|---|
| GitHub main (base) | `ac75635` | Verified via clone |
| `docs/rulings/provenance_log.md` | `ac75635` | Through Entry 61 |
| `state/STATE.md` | `ac75635` | Current |
| `specs/m3_e2_spec_amended_v4.md` | `ac75635` | M3 spec (L18 battery, V4.4 framework) |
| `specs/m3_v4_4_implementation_contract_amendment.md` | `ac75635` | V4.4 RNG protocol |
| `docs/governance_paper_final.md` | `ac75635` | Governance context |
| `GOVERNANCE_SOURCE_MAP.md` | `ac75635` | Constitution source map |

## Files created

| File | Description |
|---|---|
| `specs/m4_specification.md` | M4 specification (380 lines) |
| `specs/m4_specification_changelog.md` | Companion changelog (78 lines) |

## Branch/result SHA

- **Branch:** `architect/m4-specification`
- **Base SHA:** `ac75635` (GitHub main)
- **Result SHA:** (to be verified after push)

## Verdict/status

**M4 specification draft complete. Ready for CRITIC review.**

### Key elements

1. **L7 (Mirror/peer-observer):** AUROC ≥ 0.75, ECE ≤ 0.10, margin > 0 at p < .05. 5 seeds. L18 battery (6 arms). Peer-observer sees inputs but not candidate's internal state/self-report. Graveyard gate — Rebecca must sign.

2. **L8 (Stakes/dose-dependence):** ≥3 levels, monotonic test with all-seeds-direction + bootstrap-CI fallback. 5 seeds. Specificity control: frozen arm should NOT show dose-response. Proposed levels: h=1/h=3/h=5 (Rebecca approval required).

3. **L10 (Abstention/calibration):** Dual bar 50%/10% (LOCKED). Drifted-AUROC ≥ 0.70 floor. Confidence threshold τ = 0.70 pre-registered (W4 — Rebecca approval required). Clean-regime specificity control added.

4. **L14 (Interface):** d ≥ 0.5 primary (LOCKED); corr ≥ 0.3 at 3 seeds weakest (W5).

5. **L18 battery:** Full 6-arm battery per law (empty/permuted/shuffled/oracle/naive/frozen). V4.4 stochastic control framework.

6. **Multiplicity:** 5 seeds, 1 pool, Bonferroni, 90 per-seed checks. ≥2 unseen seeds per scoring run.

7. **Open items:** Multiplicity in scope; L3 calibration parallel; reproducibility contract in scope; raw artifact recomputation deferred.

8. **L15–L17 fence:** Respected. No integration work.

## Items requiring Rebecca's decision

| Item | What |
|---|---|
| L7 graveyard-gate sign-off | Must sign with M3 results in front of her (Entry 11.8) |
| L10 confidence threshold | Proposed τ = 0.70 (W4 pre-registration) |
| L8 stakes levels | Proposed h=1/h=3/h=5 |
| M4 timebox | Proposed 4 sessions / 8 days |
| L8 numeric bars | L8 was "measurable in form, unmeasurable in magnitude" — thresholds need confirmation |

## Source recovery gap

The constitution document is not in the repository. Law definitions are reconstructed from the provenance log, STATE.md, and existing specs. If Rebecca identifies a discrepancy, the constitution controls.

## Next recipient

**CRITIC** — Review for falsifiability, completeness, bar correctness, L10 threshold pre-registration, L14 bar, multiplicity plan, L15–L17 fence, source recovery gaps.

After CRITIC approval: **Rebecca** (approve spec + L7 sign-off + L10 threshold + timebox) → implementation cycle.

## Explicitly prohibited actions

- No implementation, scoring, seed execution, or merging.
- No modification of STATE.md or provenance_log.md.
- No modification of any locked bar, threshold, or scoring predicate.
- No running of scoring seeds or seeds 201–203 or 301–303.
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
