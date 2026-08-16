# M3/E2 V4.4 Systemic Closure — Companion Changelog

**Base:** `8259e01a1dfac6a09074027d9a48f034bf51d9b9`

**Gate:** M3 V4.3 Systemic Pre-Scoring Closure Gate

## Requested finding map

| Finding/request | Exact V4.4 resolution |
|---|---|
| NB1 / stale §2.10 | Consolidated spec §2.10 now uses the same one-sided shuffled null-of-the-max plus-one rule as §§2.9 and 2.11. |
| NB2 / mixed closure phases | §7 separates Phase A pre-scoring framework closure from Phase B post-scoring JUDGE recomputation. Phase A expressly forbids fresh observed values and p-values. |
| NB3 / other multiplicity failures | §1 establishes family-level law; §§2–4 correct six stochastic families; inventory audits every family. |
| NB4 / exchangeability | §6 freezes identical observed/null sample spaces and algorithms with disjoint domains and mandatory derivation artifacts. |
| NB5 / incomplete RNG | §6 names SHA-256, exact domain bytes, encodings, formula, stream, rejection sampler, Fisher–Yates, derangement rule, and reuse prohibition. |
| Full 26-family inventory | Machine-readable inventory contains L1=8, L3=5, L5=7, L6=6 exactly once. |
| Known L1 frozen/fair-naive failures | §2.9 replaces independent 95th-percentile decisions with upper-tail plus-one p-values and three-seed Bonferroni control. |
| Known L1 permuted failure | §2.9 retains V4.2's 200-entry rho but calibrates `abs(rho)` by plus-one randomization and Bonferroni; p95≤0.15 remains a single power check. |
| Known L1 recency-only concern | §2.9 classifies it as a fixed-fixture exact family, proves scoring seed non-entry, requires seven-value satisfiability and cross-slot identity, and does not invent a 5% per-check rate. |
| Other multi-check failure: L3 permuted | §3 retires the unproved exact probability claim, preserving the direction and transform while applying upper null-of-max plus-one control. |
| Other multi-check failure: L5 permuted | §4 replaces three independent 95% bands with a symmetric two-sided randomization rank plus Bonferroni. |
| Required artifacts | Inventory freezes independent-verification fields for all 26 families; stochastic rows include raw nulls, ranks, p-values, and RNG records. |

## Corrections and numerical closure

| Family | Old full-family FWFP | V4.4 method | Corrected bound |
|---|---:|---|---:|
| L1.frozen | `1-.95^3=0.142625` | upper plus-one p, Bonferroni across seeds | `48/1001=0.047952...` |
| L1.fair_naive | `0.142625` | upper plus-one p, Bonferroni | `0.047952...` |
| L1.permuted | `0.142625` | two-sided magnitude plus-one p, Bonferroni | `0.047952...` |
| L1.shuffled | `1-.95^15=0.536708...` | upper null-of-max plus-one p, Bonferroni | `0.047952...` |
| L3.permuted | unproved/unbounded (`1.0` conservative) | upper five-horizon null-of-max plus-one p, Bonferroni | `0.047952...` |
| L5.permuted | `0.142625` for stochastic combo check | symmetric two-sided departure rank, Bonferroni | `0.047952...` |

All other 20 families are exact deterministic predicates, not level-alpha tests. Their inventory rows give the finite/algebraic/paired/schema rationale and required proof artifacts. Their stochastic FWFP is inapplicable and audit value is zero.

## No-change audit

- Candidate-facing bars and KILL branches unchanged.
- No production code, harness, scoring artifact, preserved verdict, STATE.md, or provenance entry changed.
- No M3 harness execution, diagnostic run, scoring run, or seed exposure occurred.
- First scoring remains `INSTRUMENT FAILURE`; seeds 201–203 never rerun.
- O-14/O-15, D1–D5, L9, L15–L18, L20, supervised execution, and fresh-seed requirements retained.
- V4.4 grants no implementation, scoring, merge, CRITIC-clearance, or Rebecca-approval claim.

## Deliverable map

- Consolidated specification: `specs/m3_e2_spec_amended_v4_4.md`
- Changelog: `specs/m3_e2_spec_changelog_v4_4.md`
- Inventory: `verification/m3_control_family_closure_inventory.json`
- Verifier: `verification/verify_m3_control_family_closure.py`
- Results: `verification/m3_control_family_closure_results.json`

