# L8 GPU Statistical-Equivalence Proposal

**Date:** 2026-08-20

**Regime:** B

**Status:** Proposed code only; not approved for diagnostic screening or scoring.

The proposed CUDA path is `diagnostics/l8_gpu_proposal.py`. It preserves the L8 synthetic-data equations, windowed controller sequence, four dose levels, five-seed grouping, float64 state/estimator reductions, and direct per-seed beta-star/rho verdict. It uses a CUDA random stream and is therefore not byte-identical to the legacy NumPy CPU path.

Required approval criterion: statistical equivalence must be defined before this path may replace any approved CPU diagnostic. At minimum, an approved validation protocol should compare candidate-blind fixed cells for mean beta-star, mean rho, complete-verdict false-kill rate, calibration output, and null-control false-pass rate, with pre-registered sample sizes and tolerances.

This proposal exposes no scoring mode and does not authorize a full-screen GPU run.
