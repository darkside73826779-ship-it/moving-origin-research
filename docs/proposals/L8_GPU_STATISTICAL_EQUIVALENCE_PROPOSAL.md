# L8 GPU Statistical-Equivalence Proposal

**Date:** 2026-08-20

**Regime:** B

**Status:** Proposed code only; not approved for diagnostic screening or scoring.

The proposed CUDA path is `diagnostics/l8_gpu_proposal.py`. It imports the CPU reference constants rather than copying them, preserves the L8 synthetic-data equations, windowed controller sequence, four dose levels, five-seed grouping, float64 state/estimator reductions, pooled within-dose standard deviation, and direct per-seed beta-star/rho verdict. The rho implementation uses exact tied midranks, matching the direct-rho implementation. It uses a CUDA random stream and is therefore not byte-identical to the legacy NumPy CPU path.

Required approval criterion: statistical equivalence must be defined before this path may replace any approved CPU diagnostic. At minimum, an approved validation protocol should compare candidate-blind fixed cells for mean beta-star, mean rho, complete-verdict false-kill rate, calibration output, and null-control false-pass rate, with pre-registered sample sizes and tolerances. Development-only diagnostics must remain O-15-labelled and use only seeds 101–105; neither exploratory output nor a speed measurement is an acceptance result.

The included regression tests cover CPU-constant binding, tied-rank rho parity, and fixed-seed CUDA replay. This proposal exposes no scoring mode and does not authorize a full-screen GPU run, final-screen replacement, or merge.
