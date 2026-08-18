# ARCHITECT Handoff — M4 Specification v1.3

**Gate served:** M4 spec correction cycle (F1 — reconstruction-infidelity, G0-1 authorized)
**Issued by:** ARCHITECT
**Date:** 2026-08-18 16:00 EDT
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)

---

## Input SHAs reviewed

| Item | SHA | Source |
|---|---|---|
| GitHub main HEAD (base) | `e26d05f` | Verified via clone |
| Constitution v1 | `docs/ARCHITECTURAL_CONSTITUTION.md`, SHA-256 `509f11c3...` | Line numbers verified: L7=24, L8=26, L10=30, L14=40 |
| Constitution v2 | `docs/ARCHITECTURAL_CONSTITUTION_v2.md` | Amendment 1 + §5 |
| Provenance log | Entries 1–62 at `e26d05f` | All citations verified (P6) |

## Files created

| File | Description |
|---|---|
| `specs/m4_specification.md` | M4 spec v1.3 (399 lines) |
| `specs/m4_specification_changelog.md` | Changelog (71 lines) |

## Branch/result SHA

- **Branch:** `architect/m4-spec-v1.3`
- **Base SHA:** `e26d05f` (GitHub main)
- **Result SHA:** (to be verified after push)

## F1 corrections summary

1. **F1.1 (L8 respecified):** Replaced prediction-horizon dose-response with verbatim law test: homeostatic variable + calibrated noise into self-model + dose-dependent regulation error + "only then" specificity. [LAW-L8, line 26]
2. **F1.2 (L14 rewritten):** Three couplings from verbatim text: readable by self-model, affected by memory quality, predictive targets for thick present. [LAW-L14, line 40]
3. **F1.3 (L10 reporting rule):** Added: drifted-regime AUROC is reported; clean is ceiling. [LAW-L10, line 30]
4. **F1.4 (L7 portrait clause):** Added: no margin over peer = portrait, not mirror. [LAW-L7, line 24]
5. **F1.5 (§12 provenance):** L7 bars correctly attributed to [LAW-L7] (constitution text), not Entry 5 (assessment only). Entries 5, 8, 11 verified against actual text (P6).
6. **F1.6 (W4 changelog):** W4 resolved — τ = 0.70 pre-registered as [PROPOSED].

## §5 compliance

- **P1:** All law text from `docs/ARCHITECTURAL_CONSTITUTION.md` on main. No reconstruction.
- **P2:** §2.1, §3.1, §4.1, §5.1, §6.1 open with verbatim quotes, cited by file and line.
- **P3:** Every threshold tagged: [LAW-Lx], [BAR-Entry n], [OP-Entry n], or [PROPOSED].
- **P4:** Header states date, Regime B.
- **P5:** No deviations from law text.
- **P6:** All provenance citations verified before commit.

## Confirmation

- No law text modified (only quoted verbatim).
- No bars, thresholds, scoring predicates, historical verdicts, or evidence modified.
- No STATE.md or provenance_log.md modified.
- No scoring, seed execution, or hold-out seed exposure.
- INSTRUMENT FAILURE label retained.
- L15/L16/L17 fence respected.

## Next recipient

Reviewer TBD per G0-3 ruling (Rebecca has not yet ruled on who reviews the corrected spec).

## Explicitly prohibited actions

- No reconstruction of constitutional law text (P1).
- No modification of §1–§4 law text in the constitution.
- No modification of any historical file, SHA, ruling, or provenance entry.
- No modification of scientific bars, scoring predicates, historical verdicts, or evidence.
- No merging to main (Rebecca is sole merge authority).
- No scoring, seed execution, or hold-out seed exposure.
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
