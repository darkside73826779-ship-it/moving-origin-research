# FROM REBECCA — M3 Block Ruling: Specification-Error Correction Authorized (Under a General Rule)

**Date:** 2026-08-16 · **Status:** binding. RECORDER logs; this ruling refines condition 3 of the L1 permuted-arm precedent rather than excepting it.

## 1. Ruling: correction, not shopping — by a four-part test, now standing law

A post-scoring instrument change is permitted ONLY when ALL four hold:
(a) the defect is demonstrable from the spec alone, without reference to observed values (here: 1−0.95¹⁵ ≈ 54% familywise false-positive rate is arithmetic on the pre-registered rule);
(b) the change cannot benefit the candidate — no candidate-facing bar moves, and the corrected control is equally or more sensitive in its meaningful direction (here: candidate passed all bars; failures are below-band on a destroy-the-signal control, i.e., the control succeeding);
(c) the failed run's results are retained in full and the correction is logged as post-scoring with this justification;
(d) any new scoring uses FRESH seeds — never a re-run (O-14 stands untouched).
Fail any part → the change is forbidden statistic-shopping and the failure stands.

## 2. The remedy: one-sided AND multiplicity-controlled (the Critic's narrowest remedy is insufficient)

One-sided alone leaves ~32% familywise false-positive odds (1−0.975¹⁵). Required fix, O-14-consistent:
- **Directionality:** shuffled-arm check becomes one-sided, upper bound only. Below-band is logged as "shuffle exceeded typical destruction" — informational, never a failure.
- **Multiplicity:** exact control via null-of-the-max — in each of the 1000 null replicates, take the MAX ρ across the 5 bins; the per-seed threshold is a percentile of that max-distribution, chosen so the familywise false-positive rate across ALL shuffled-arm checks in one scoring run is ≤ 5%, verified by direct computation in the closure audit before scoring. ARCHITECT specifies, CRITIC verifies the computation.

## 3. Fresh scoring run

Full M3 battery on 3 fresh seeds from the authorized pool (harness is cheap; mixed-seed verdicts are messier than they're worth). Seeds 201–203 results are RETAINED: L3/L5/L6 passes and L1 candidate bars stand as valid evidence; the fresh run delivers the verdict; cross-run consistency is reported.

## 4. Systemic fix (so this never needs a ruling again)

**Standing closure-audit requirement:** every scoring spec's closure audit must compute the familywise false-positive rate of each arm's full check battery (bins × seeds × arms) and correct any control whose FWFP exceeds 5% BEFORE scoring. Directionality must be justified per control (which direction is the meaningful failure). This defect was discoverable pre-scoring; henceforth it is discovered pre-scoring.

## 5. Non-blocking dispositions: accepted as classified

Round-trip log mandatory in all future courier packets; ledger/manifest label fixes are mechanical next-implementation items. The Critic surfacing the precedent collision instead of arguing past it is logged as the apparatus honoring its own law.

Sequence: amend §2.9/§2.11 per §2 above → closure-audit FWFP verification → CRITIC clearance → fresh-seed scoring run through the executor.
