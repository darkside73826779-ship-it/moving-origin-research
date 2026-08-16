# L3 Repair Proposal — Pending CRITIC Approval

**Authority:** Rebecca directly authorized TASK BUILDER to prepare and test this
repair after the v4.1 specification block. This document is a proposed L3-only
contract delta for CRITIC review; it is not yet a governing specification and
does not authorize scoring.

## Preserved failures

- `ec457fc`: v4 generator; oracle ceiling, candidate, and controls failed.
- `6ef3cce`: v4.1 generator/provenance; candidate and controls still failed.
- `76a8dd6`: verifier-aligned oracle; candidate h1/h3/h4, permuted h2/h5, and
  shuffled comparator still failed on every development seed.

## Proposed L3-only changes

1. **Channel phases:** retain AR coefficients `(0.3,-0.2,0.1)`, amplitude
   `0.5`, period `7`, noise variance `0.05`, and burn-in `100`; replace the
   shared sinusoid with deterministic channel phase
   `phase_c = c*pi/16`, `c=0..7`.
2. **State:** retain 16 dimensions and zero learned parameters; replace the
   dead-coordinate filter with per-channel block
   `[x_i[t], x_i[t-1]]`, equivalent to
   `A_i=[[0,0],[1,0]]`, `B[2i,i]=1`.
3. **Shuffled comparator:** keep the exact `+0.01` tolerance, but compute the
   frozen reduction on the same shuffled sequence used by the shuffled state
   and raw comparator. No numeric bar changes.

## Development phase study

The following pre-scoring sweep used seeds 101–105 only. `min candidate` is
the minimum reduction across all seeds/horizons. `max permuted` is the maximum
channel-deranged reduction. This entire study is disclosed because it informed
the proposal.

| Phase increment | Min candidate | Max permuted |
|---:|---:|---:|
| 0.05 | 0.206 | 0.630 |
| 0.10 | 0.125 | 0.393 |
| 0.15 | 0.080 | 0.085 |
| 0.20 | 0.064 | -0.262 |
| 0.25 | 0.060 | -0.598 |
| 0.30 | 0.060 | -0.881 |
| 0.35 | 0.049 | -1.090 |
| 0.40 | 0.041 | -1.257 |
| 0.45 | 0.041 | -1.372 |
| 0.50 | 0.044 | -1.416 |
| 0.55 | 0.047 | -1.391 |
| 0.60 | 0.048 | -1.344 |
| 0.65 | 0.046 | -1.287 |
| 0.70 | 0.043 | -1.229 |
| 0.75 | 0.042 | -1.173 |
| 0.80 | 0.042 | -1.150 |
| 0.85 | 0.044 | -1.185 |
| 0.90 | 0.047 | -1.290 |
| 0.95 | 0.048 | -1.466 |
| 1.00 | 0.047 | -1.708 |

The decimal sweep identified a narrow feasible region. `pi/16 = 0.1963495`
was then separately evaluated as a simple analytic phase schedule close to
the lower feasible boundary; it was not one of the 0.05-grid points.

## Five-seed validation at `pi/16`

| Seed | Min candidate | Min oracle | Max permuted | Max shuffled-minus-frozen |
|---:|---:|---:|---:|---:|
| 101 | 0.096047 | 0.103475 | -0.241144 | 0.000677 |
| 102 | 0.089808 | 0.130688 | -0.279730 | -0.006734 |
| 103 | 0.083650 | 0.111108 | -0.314924 | -0.014866 |
| 104 | 0.089580 | 0.122917 | -0.276896 | -0.011436 |
| 105 | 0.064497 | 0.111245 | -0.235937 | -0.020628 |

All candidate reductions are `>=0.05`; all oracle reductions are in
`(0.05,0.95)`; all permuted reductions are `<=0`; all shuffled differences
are `<=0.01`; the original frozen floor remains `<=0`.

## Independent and negative validation

- Independent NumPy implementation matches all harness reductions within
  `2.2e-15`.
- Cross-process L3 result files are byte-identical under `PYTHONHASHSEED=0`
  and `123`.
- Restoring the old dead-coordinate state makes every seed fail candidate.
- Restoring the shared sinusoid makes every seed fail the permuted control.
- Comparing shuffled results with the original-fixture frozen baseline makes
  every seed fail the shuffled control.

## Scope fence

No locked numeric bar, verdict meaning, seed pool, hold-out rule, other law,
scoring path, or courier behavior changes. Hold-outs remain unexposed. CRITIC
must approve or reject this proposal before any scoring packet is eligible.
