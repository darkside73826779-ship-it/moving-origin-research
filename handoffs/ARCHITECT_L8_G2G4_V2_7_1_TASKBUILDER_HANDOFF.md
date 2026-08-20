# ARCHITECT → TASK BUILDER Handoff — L8 1,000-Rep Parallel Feasibility Diagnostic

**Date:** 2026-08-20 · **Regime:** B

**Gate served:** Rebecca-cleared staged implementation and execution of the L8 feasibility diagnostic

**Authority:** Rebecca’s merged authorization `d08cb7eefec67609a3ea3cee0eb20da22f78c40a` and direct clearance recorded in L8 spec v2.7.1.

**Implementation source:** `diagnostics/l8_power_analysis.py` at `b1397498ca369067e956479e6c2bd6b0793c3e89`

**Destination branch:** `taskbuilder/l8-g2g4-diagnostic-remediation`, branched from the current `architect/l8-g2g4-remediation` tip supplied with this handoff.

## Authorized work only

1. Commit A1: diagnostic implementation, tests, and fixtures—no resolved config or generated evidence.
2. Commit A2: frozen config and sidecar only, with `implementation_sha=A1` exactly.
3. After A1/A2 are committed, run the fixed apparatus checks, 12-case rehearsal, two parallel-repeatability executions, six uncached calibrations, and the 1,000-repetition parallel feasibility diagnostic; Commit B contains only resulting authorized evidence and handoff.

The complete contract is L8 spec v2.7.1 §§8.9–8.12. Do not make any design choice not explicitly specified there; STOP and return to ARCHITECT if an implementation ambiguity remains.

## Fixed execution parameters

- Parallel path only: `multiprocessing.Pool`, `spawn`, chunksize 1, `worker_count=min(32, os.cpu_count())`; no serial benchmark.
- Cases are ordered and allocated exactly: `g0_low=167`, `g0_central=167`, `g0_high=167`, `g1_low=167`, `g1_central=166`, `g1_high=166`; total 1,000.
- Every repetition: five seeds; 5,000 valid bootstrap replicates; 5,500 maximum attempts; full verdict unchanged.
- Feasibility calibration: six uncached calibrations only, one per case’s `(W,N_w,alpha,v_mult)`; do not create the 300-entry screening cache.
- Repeatability fixture: `(W,N_w)=(50,4)`, `(alpha,v_mult,C_min,eta)=(0.05,1.0,0.7,0.1)`, 32 repetitions, freshly computed `g0_central` sigma, two parallel executions, exact canonical comparison from §8.12.3.
- Rehearsal prior pair and estimator fixture descriptors/digests are fixed by §§8.12.4–8.12.5.

## Required evidence

Produce only the schemas and paths fixed by the specification: resolved config/sidecar, seed manifest, calibration records, diagnostic rehearsal/sidecar, parallel-repeatability records, and `diagnostics/l8_g2g4/feasibility_benchmark.json` plus sidecar. Follow transactional pair publication exactly.

## Post-execution route

Fresh-context **CRITIC** reviews A1/A2, tests, rehearsal, repeatability, calibrations, and feasibility benchmark. Then Rebecca alone decides whether to authorize any screening.

## Explicitly prohibited

- No 2,000-repetition screening, 10,000 confirmation, sensitivity or misspecification rerun.
- No scoring, protected seeds, G2–G4 ruling/freeze, L15/L16/L17 work, or merge.
- No serial benchmark, candidate data, candidate diagnostic seeds, or scoring evidence.
- No relabeling ordinary statistical failures as INSTRUMENT FAILURE.

## Public-safety scan attestation

Public-safety scan: gitleaks plus regex/manual review over the complete v2.7.1 routing diff from `4e31eddf50819b1b9b0c67a1911ebfc53d3effbd`; zero prohibited findings; cleared. No credentials, contact details, machine identifiers, private absolute paths, environment dumps, or protected-seed identities were added.
