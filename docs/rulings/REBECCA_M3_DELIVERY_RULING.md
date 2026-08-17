# Rebecca M3 Delivery Gate Ruling — Provisional Advancement with Qualified Instrument Certification

**Date:** 2026-08-17 (00:28 EDT)
**Status:** Binding
**Ruling file:** `docs/rulings/REBECCA_M3_DELIVERY_RULING.md`
**Authority:** Rebecca McClintic (sole gate authority)

---

## Ruling

### M3 verdict: INSTRUMENT FAILURE (retained)

The official M3 V4.4 scoring verdict remains INSTRUMENT FAILURE. Seeds 301–303 are retained as scored evidence. Seeds 201–203 remain retained as INSTRUMENT FAILURE evidence from the first scoring run. Neither set of seeds may ever be rerun (O-14).

### Candidate-facing evidence: sufficient for provisional advancement

The candidate passed every candidate-facing bar across all six scoring seeds (201–203, 301–303) and triggered no kill conditions in either run. This evidence is accepted as sufficient for provisional advancement to M4.

The milestone delivers with a qualified instrument certification: the candidate-facing evidence is strong and consistent, but the instrument (control arms) produced instrument failures in both runs — one specification defect (now fixed) and one borderline case within the pre-registered false-positive rate.

### What is NOT authorized

- No additional scoring run to obtain a PASS
- No modification of the L3 frozen-control test
- No retroactive multiplicity correction applied to V4.4
- No reinterpretation, renaming, or deletion of any prior run or label

### Required actions before future scoring work

1. Fix the reproducibility-checker construction bug (pass `artifact_writer` to the second pass or strip artifact-dependent fields from the projection)
2. Fix stale scoring labels (seed ledger scope, manifest boilerplate) for scoring mode
3. Document milestone-wide multiplicity as a consideration for future specifications, not as a correction to V4.4

### Preserved evidence (unchanged)

- First scoring run (seeds 201–203): INSTRUMENT FAILURE — L1 shuffled-arm spec defect (54% FWFP, now fixed in V4.4). L3/L5/L6 PASS. Candidate passed all bars.
- Second scoring run (seeds 301–303): INSTRUMENT FAILURE — L3 frozen-arm borderline case (p=0.012 vs alpha_seed=0.0167, within 4.8% FWFP). L1/L5/L6 PASS. Candidate passed all bars.
- V4.4 L1 fix confirmed: one-sided null-of-the-max resolved the first run's L1 false positives. L1 PASS on all 3 fresh seeds.
- No kill conditions fired in either run. Candidate mechanism is stable across 6 scoring seeds.
- O-14, O-15, D1–D5, L9, L18, L15 integration fence, four-part test (Entry 43) all remain binding.
- No L15–L17 integration claim follows from M3 provisional advancement.

### Standing note

The L3 control produced a valid borderline rejection under the pre-registered rule. It does not indicate candidate failure. Changing rules or rerunning after observing the result would weaken the evidence record. The instrument's honesty — catching its own borderline case — is the discipline working as designed.
