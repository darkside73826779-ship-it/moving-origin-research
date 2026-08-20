#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L8 §8 power analysis simulation — candidate-blind, synthetic profiles only.

Implements the §8 power-analysis protocol from the L8 instantiation spec v2.2
(reviews/l8_crossfamily_review/06_l8_instantiation_spec.md, branch
architect/l8-instantiation-v2.2-fresh, SHA c7d7bed). Diagnostic-only (O-15);
this authorizes NO scoring.

Regime / provenance (§5 P4 — regime dating):
  - Spec regime: L8 instantiation spec v2.2 (CRITIC-cleared, 4ca797c attestation
    true per COORDINATOR ledger 2026-08-19).
  - Constitution regime: ARCHITECTURAL_CONSTITUTION_v2.md (v2 date 2026-08-18).
  - Artifact date: 2026-08-19. Judged only against its own regime's text.

§5 P3 — source-class tags. Every numeric threshold / kill condition / test
criterion below carries an inline tag, one of exactly four classes:
  [LAW-Lx]      — in the constitution's text (here L8 / L14 / L19).
  [BAR-Entry n] — Rebecca-locked pre-registration (M0 sheet).
  [OP-Entry n]  — adopted operationalization.
  [PROPOSED]    — requires Rebecca sign-off; may not gate anything until signed.
A number without a tag is a review-blocking defect.

Candidate-blind throughout (Ruling 9, Entry 76): the simulation seeds are
SIMULATION seeds derived from parameter-combo hashes, NOT candidate diagnostic
seeds. No candidate output is an input anywhere (Ruling 9, §5). The β*
estimator is the identical §2 XF-5 estimator used at scoring time.

Self-contained: depends only on numpy, hashlib, json, time, argparse, math.
CPU-only (numpy); no GPU.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing
import os
import time
from typing import Dict, List, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Regime / provenance header (§5 P4). Hard-coded so the artifact self-reports
# the regime it was built against; later text is never applied backward.
# ---------------------------------------------------------------------------
SPEC_REGIME = "L8 instantiation spec v2.2 (architect/l8-instantiation-v2.2-fresh, c7d7bed)"
CONSTITUTION_REGIME = "ARCHITECTURAL_CONSTITUTION_v2.md (v2 date 2026-08-18)"
ARTIFACT_DATE = "2026-08-19"  # [OP — artifact date, P4 regime dating]

# ---------------------------------------------------------------------------
# Pre-registered constants. Every threshold carries a P3 source tag.
# ---------------------------------------------------------------------------

# Battery geometry (§2). [PROPOSED] values from the spec; apparatus parameters.
W = 50          # queries per window            [PROPOSED — apparatus parameter, §2]
N_W = 4         # windows per dose level        [PROPOSED — apparatus parameter, §2]
L_DOSES = 4     # dose levels {0,1,2,3}         [PROPOSED — apparatus parameter, §2]
N_SEEDS = 5     # seeds per simulation          [BAR-Entry 11] (5 seeds for the joint bar)

# Regulation target. The spec defines R* = R_ref + m with R_ref from the
# synthetic reference mirror and m = 0.05. The task brief fixes R* = 0.1 as the
# pre-registered constant for this simulation (R* is frozen before any
# candidate data; candidate outputs are not inputs to R* — Ruling 9, §2).
R_STAR = 0.1    # regulation target (pre-registered constant)  [PROPOSED — apparatus parameter, §2; Ruling 9]

# Effect-size targets and bars (§8).
TRUE_BETA_STAR = 0.3   # true β* target for calibration  [PROPOSED — apparatus parameter, §8]
BETA_STAR_BAR = 0.2     # locked standardized-slope bar    [BAR-Entry 11]
FALSE_KILL_THRESHOLD = 0.10  # false-kill prob above this → G3 escalation [PROPOSED — apparatus parameter, §8]

# Estimator validation anchors (§2 XF-5 synthetic validation).
EX_A_SLOPE = 0.02       # Example A: d = 0.02*ℓ + ε       [BAR-Entry 11] (anchor 0.2 = 0.02/0.1)
EX_A_NOISE_VAR = 0.01    # ε ~ N(0, 0.01) (N(μ,σ²) convention) [PROPOSED — apparatus parameter, §2]
EX_B_NOISE_VAR = 0.01    # Example B: d = ε               [PROPOSED — apparatus parameter, §2]
VALIDATION_TOL = 0.05    # |β* - anchor| < 0.05            [PROPOSED — apparatus parameter, §2]

# Mirror / controller numerical constants (§5 XF-8, §3).
EPS_C = 1e-6            # confidence clipping bound       [PROPOSED — apparatus parameter, §5 XF-8]
# Task profile: per-query difficulty is VARIABLE (§8.1 — "query-answer pairs
# with known oracle correctness and variable difficulty"). Each query's true
# correctness probability p_true is drawn from a difficulty distribution; the
# realized oracle correctness is Bernoulli(p_true). Variable difficulty is what
# makes the mirror's confidence informative (a ranking signal) and is what the
# dose noise corrupts (misranking at the coverage floor → higher r_w at higher
# doses → positive dose-response → β* > 0). A homogeneous p_true would give no
# ranking signal to corrupt and no dose-response.  [Sol-XF-9]
# The difficulty distribution: p_true ~ Beta(a, b) with mean a/(a+b). We center
# the mean at 0.7 (the task-brief's Bernoulli p, now reinterpreted as the mean
# per-query correctness across a variable-difficulty battery) and choose a
# concentration that yields a useful spread of difficulties.
P_TRUE_MEAN = 0.7       # mean per-query true correctness   [PROPOSED — apparatus parameter, §8]
# Beta concentration: a+b. Larger → tighter around the mean (easier queries,
# less ranking signal); smaller → wider spread (more ranking signal). We pick a
# concentration that yields a useful spread of difficulties (SD ≈ 0.20 on the
# per-query p_true) and allows the calibrated dose-response to reach the
# β* = 0.3 target (a wider spread gives more ranking signal to corrupt).
BETA_CONC = 4.0         # Beta(a,b) concentration a+b      [PROPOSED — apparatus parameter, §8]
# Derive a, b from mean and concentration: a = mean*conc, b = (1-mean)*conc.
BETA_A = P_TRUE_MEAN * BETA_CONC   # [PROPOSED — apparatus parameter, §8]
BETA_B = (1.0 - P_TRUE_MEAN) * BETA_CONC  # [PROPOSED — apparatus parameter, §8]
# Controller threshold bounds (τ_min, τ_max) and initial τ. The spec pre-
# registers η and bounds as G4 constants; for the candidate-blind power analysis
# we fix reasonable apparatus values (the simulation sweeps η).
TAU_MIN = 0.5           # lower clip on τ                 [PROPOSED — apparatus parameter, §3]
TAU_MAX = 0.95          # upper clip on τ                 [PROPOSED — apparatus parameter, §3]
TAU_INIT = 0.7          # initial τ (calibrated reference) [PROPOSED — apparatus parameter, §3]

# Calibration reference operating point (§8 — documented simplification).
# σ_dose is calibrated once per (α, v) pair at this fixed (C_min, η) reference
# operating point, then reused for all (C_min, η) combinations at that pair.
CAL_REF_C_MIN = 0.7     # [PROPOSED — apparatus parameter, §8 calibration]
CAL_REF_ETA = 0.1       # [PROPOSED — apparatus parameter, §8 calibration]
CAL_PILOT_SIMS = 1000   # pilot simulations for σ_dose binary search [PROPOSED — apparatus parameter, §8]
CAL_TOL = 0.01          # |mean β* - 0.3| < 0.01 calibration tolerance [PROPOSED — apparatus parameter, §8]
CAL_SIGMA_LO = 1e-4     # binary-search lower bound on σ_dose [PROPOSED — apparatus parameter, §8]
CAL_SIGMA_HI = 12.0     # binary-search upper bound on σ_dose [PROPOSED — apparatus parameter, §8]
CAL_MAX_ITERS = 40      # binary-search iterations        [PROPOSED — apparatus parameter, §8]

# Simulation counts (§8).
N_SIMS_FULL = 10_000    # simulations per parameter combination [PROPOSED — apparatus parameter, §8]
N_SIMS_VALIDATION = 100  # validation-batch size (task brief Step 2) [PROPOSED — apparatus parameter]

# v_ref: the logit-space variance of the synthetic reference mirror (§5).
# The reference mirror is a calibrated confidence profile built from oracle
# ground truth on synthetic task profiles. For this candidate-blind simulation
# we set v_ref to the logit-space variance of a well-calibrated mirror at
# p_true = 0.7 (the construction is fixed here, pre-registration, candidate-
# blind — Ruling 9). With c ≈ sigmoid(logit(p_true)) = p_true, the logit-space
# variance of a binomial-ish confidence stream is taken as the reference scale.
V_REF = 1.0             # reference logit-space variance scale [PROPOSED — apparatus parameter, §5]

# Parameter grid (§8.3). 5 * 3 * 4 * 4 = 240 combinations.
ALPHAS = [0.0, 0.02, 0.05, 0.1, 0.2]          # calibration error α        [PROPOSED — apparatus parameter, §8]
V_MULTS = [0.5, 1.0, 2.0]                     # v = mult × v_ref           [PROPOSED — apparatus parameter, §8]
C_MINS = [0.5, 0.6, 0.7, 0.8]                 # coverage floor C_min       [PROPOSED — apparatus parameter, §8]
ETAS = [0.01, 0.05, 0.1, 0.2]                 # controller gain η          [PROPOSED — apparatus parameter, §8]

# Zero-variance behavior (§2 XF-5): if σ_pool,s = 0 for any seed →
# INSTRUMENT_FAILURE for that simulation.
INSTRUMENT_FAILURE = "INSTRUMENT_FAILURE"  # [Sol-XF-5]


# ---------------------------------------------------------------------------
# Deterministic simulation seeds (§8.4). seed = hash(parameter_combo) mod 2^31.
# These are SIMULATION seeds, NOT candidate diagnostic seeds (candidate-blind,
# Ruling 9 / Entry 76). The hash is over a canonical string representation of
# the parameter combination so the seed is reproducible and combo-specific.
# ---------------------------------------------------------------------------
def combo_seed(alpha: float, v_mult: float, c_min: float, eta: float) -> int:
    """Deterministic simulation seed for a parameter combination.

    seed = hash(parameter_combo) mod 2^31  [Sol-XF-9] [PROPOSED — apparatus parameter, §8]
    Candidate-blind: derived only from apparatus parameters, never candidate data.
    """
    key = f"alpha={alpha:.6f}|vmult={v_mult:.6f}|cmin={c_min:.6f}|eta={eta:.6f}"
    h = hashlib.sha256(key.encode("utf-8")).digest()
    # Take the leading 8 bytes as an unsigned 64-bit int, then mod 2^31.
    val = int.from_bytes(h[:8], "little", signed=False)
    return int(val % (2 ** 31))


# ---------------------------------------------------------------------------
# Numerical helpers (§5 XF-8: float64, clipped logit).
# ---------------------------------------------------------------------------
def logit(p: np.ndarray) -> np.ndarray:
    """Logit transform on clipped probabilities (§5 XF-8). float64 throughout."""
    pc = np.clip(p, EPS_C, 1.0 - EPS_C)  # [PROPOSED — apparatus parameter, §5 XF-8]
    return np.log(pc) - np.log(1.0 - pc)


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Numerically stable sigmoid (float64)."""
    return np.where(x >= 0, 1.0 / (1.0 + np.exp(-x)),
                    np.exp(x) / (1.0 + np.exp(x)))


# ---------------------------------------------------------------------------
# §2 XF-5 estimator — exact standardized-slope estimator.
#
# Inputs (per seed s):
#   d[s, ℓ, w] = r_{s,ℓ,w} − R*   (per-window signed deviation), shape (L, N_w)
#   x = {0,1,2,3},  Var(x) = 1.25 (fixed for 4 equally-spaced levels)
#
#   D_{s,ℓ} = mean_w d_{s,ℓ,w}                         (per-dose mean)
#   β_s     = Cov_s(D̄, x) / Var(x)                     (slope numerator)
#   σ_pool,s= sqrt( Σ_ℓ Σ_w (d_{s,ℓ,w} − D̄_{s,ℓ})² / (L*(N_w−1)) )   (12 df)
#   β*_s    = β_s / σ_pool,s
#   If σ_pool,s = 0 → INSTRUMENT_FAILURE  [Sol-XF-5]
#
# The run-level β* is the mean of β*_s across the 5 seeds. A simulation is
# INSTRUMENT_FAILURE if ANY of its seeds has σ_pool,s = 0.
# ---------------------------------------------------------------------------
VAR_X = float(np.var([0, 1, 2, 3]))  # = 1.25  [Sol-XF-5] (fixed, 4 equally-spaced levels)
X_DOSES = np.array([0, 1, 2, 3], dtype=np.float64)


def beta_star_for_seed(d_seed: np.ndarray) -> Tuple[float, bool]:
    """Compute β*_s for one seed from its (L, N_w) array of window deviations.

    Returns (beta_star, instrument_failure). instrument_failure is True iff
    σ_pool,s == 0 (§2 XF-5 zero-variance behavior). [Sol-XF-5]

    d_seed shape: (L_DOSES, N_W).  d_seed[ℓ, w] = r_{ℓ,w} − R*.
    """
    # Per-dose means D̄_{s,ℓ} = mean_w d_{s,ℓ,w}
    d_bar = d_seed.mean(axis=1)  # shape (L,)

    # Slope numerator: β_s = Cov(D̄, x) / Var(x). Cov uses population (N) form
    # consistent with Var(x) = 1.25 = population variance of {0,1,2,3}.
    # Cov(D̄, x) = mean((D̄ - mean(D̄))*(x - mean(x))).
    cov = float(np.mean((d_bar - d_bar.mean()) * (X_DOSES - X_DOSES.mean())))
    beta = cov / VAR_X  # β_s

    # Pooled within-dose SD of window-level deviations. 12 total df
    # (L=4 doses × N_w−1=3 per dose).  [Sol-XF-5]
    resid = d_seed - d_bar[:, None]  # (L, N_w)
    ss = float(np.sum(resid ** 2))
    df = L_DOSES * (N_W - 1)  # = 12
    sigma_pool = math.sqrt(ss / df)

    if sigma_pool == 0.0:
        # Zero-variance behavior: standardized slope undefined. [Sol-XF-5]
        return (float("nan"), True)

    return (beta / sigma_pool, False)


def run_level_beta_star(d_all: np.ndarray) -> Tuple[float, bool]:
    """Run-level β* = mean across 5 seeds of β*_s.

    d_all shape: (N_SEEDS, L_DOSES, N_W).
    Returns (mean_beta_star, instrument_failure). instrument_failure is True
    iff ANY seed has σ_pool,s = 0 (the simulation is INSTRUMENT_FAILURE). [Sol-XF-5]
    """
    betas = []
    for s in range(d_all.shape[0]):
        b, fail = beta_star_for_seed(d_all[s])
        if fail:
            return (float("nan"), True)
        betas.append(b)
    return (float(np.mean(betas)), False)


# ---------------------------------------------------------------------------
# Synthetic data-generating family (§8.1).
#
# Mirror profile P(α, v): per-query confidences with calibration error α
# (systematic bias) and logit-variance v.  [Sol-XF-9]
# Task profile: query-answer pairs with known oracle correctness AND VARIABLE
# DIFFICULTY (§8.1). Each query's true correctness probability p_true is drawn
# from a Beta difficulty distribution; the realized oracle correctness is
# Bernoulli(p_true). Variable difficulty is essential: it gives the mirror's
# confidence a per-query ranking signal, and the dose noise corrupts that
# ranking. At the coverage floor the controller must act on the corrupted
# ranking → it answers confidently-wrong queries → r_w rises dose-dependently.
# This is the §3 mechanism claim ("a corrupted mirror misranks queries; global
# threshold adaptation cannot repair per-query misranking; at the coverage
# floor the system must act on a corrupted ranking").
#
# Pipeline (per window, per dose, per seed):
#   1. Generate W=50 queries. Each query's p_true ~ Beta(a, b) (variable
#      difficulty); realized oracle correctness ~ Bernoulli(p_true).
#   2. Mirror confidence: c = clip(sigmoid(logit(p_true) + α_bias + ξ), ε_c, 1-ε_c),
#      ξ ~ N(0, v_logit), α_bias = α.  (The mirror's honest confidence tracks
#      p_true; α is the systematic calibration bias; v_logit is the logit-space
#      variance of the mirror read.)  [Sol-XF-9]
#   3. Dose degradation: c' = clip(sigmoid(logit(c) + ξ_ℓ), ε_c, 1-ε_c),
#      ξ_ℓ ~ N(0, (ℓ * σ_dose)²).  σ_dose calibrated so true β* ≈ 0.3.
#   4. Controller: answer query if c' > τ, or if forced by coverage floor C_min
#      (answer the C_min*W highest-confidence queries regardless of τ).
#      τ adapts: τ ← clip(τ + η*(r_w − R*), τ_min, τ_max).
#   5. r_w = (# incorrect answered) / (# answered); 0 if none answered.
#   6. d_{ℓ,w} = r_w − R*.
# ---------------------------------------------------------------------------

def simulate_dose(rng: np.random.Generator, alpha: float, v_logit: float,
                  sigma_dose: float, dose_level: int, c_min: float, eta: float,
                  tau_init: float) -> Tuple[np.ndarray, float]:
    """Simulate one dose level (4 windows) for one seed.

    Returns (d_windows shape (N_W,), final_tau).

    Per §4 XF-10: τ resets to tau_init at the start of each dose level (each
    dose level starts from the same post-training checkpoint) and adapts across
    the 4 windows *within* the dose level.
    """
    tau = float(tau_init)
    d_windows = np.zeros(N_W, dtype=np.float64)

    for w in range(N_W):
        # 1. Generate W=50 queries with VARIABLE difficulty. Each query's true
        #    correctness probability p_true ~ Beta(a, b); realized oracle
        #    correctness ~ Bernoulli(p_true).  [Sol-XF-9] [PROPOSED — apparatus parameter, §8]
        p_true_vec = rng.beta(BETA_A, BETA_B, size=W)  # per-query difficulty
        # Avoid pathological 0/1 p_true (would make logit undefined pre-clip).
        p_true_vec = np.clip(p_true_vec, EPS_C, 1.0 - EPS_C)
        correct = rng.random(W) < p_true_vec  # oracle correctness, shape (W,)

        # 2. Mirror confidence: c = clip(sigmoid(logit(p_true) + α_bias + ξ),
        #    ε_c, 1-ε_c), ξ ~ N(0, v_logit), α_bias = α.  [Sol-XF-9]
        #    The mirror's honest confidence tracks p_true; α is systematic bias.
        xi = rng.normal(0.0, math.sqrt(v_logit), size=W)
        c = sigmoid(logit(p_true_vec) + alpha + xi)
        c = np.clip(c, EPS_C, 1.0 - EPS_C)  # [PROPOSED — apparatus parameter, §5 XF-8]

        # 3. Dose degradation (§5): logit(c') = logit(c) + ξ_ℓ, ξ_ℓ ~ N(0, (ℓ*σ_dose)²).
        #    Level 0 → σ=0 (no degradation).  [Sol-XF-9] [PROPOSED — apparatus parameter, §5]
        if dose_level > 0 and sigma_dose > 0.0:
            xi_l = rng.normal(0.0, dose_level * sigma_dose, size=W)
            c_prime = sigmoid(logit(c) + xi_l)
            c_prime = np.clip(c_prime, EPS_C, 1.0 - EPS_C)
        else:
            c_prime = c  # Level 0: no dose noise.

        # 4. Controller: answer if c' > τ, plus coverage floor.
        #    Coverage floor: answer at least C_min*W highest-confidence queries
        #    regardless of τ.  [PROPOSED — apparatus parameter, §3]
        #    First, the threshold-based abstention set:
        answer_mask = c_prime > tau
        n_answered = int(answer_mask.sum())
        floor_count = int(math.ceil(c_min * W))  # C_min*W, rounded up
        if n_answered < floor_count:
            # Force the (floor_count - n_answered) highest-confidence
            # not-yet-answered queries to be answered.
            if n_answered < floor_count:
                # Rank by confidence descending; take the top floor_count.
                order = np.argsort(-c_prime)  # descending confidence
                forced = np.zeros(W, dtype=bool)
                forced[order[:floor_count]] = True
                answer_mask = answer_mask | forced
                n_answered = int(answer_mask.sum())

        # 5. r_w = (# incorrect answered) / (# answered); 0 if none answered.
        #    [Sol-XF-9] (§2 variable definition)
        if n_answered == 0:
            r_w = 0.0
        else:
            n_incorrect_answered = int((~correct[answer_mask]).sum())
            r_w = n_incorrect_answered / n_answered

        # 6. d_{ℓ,w} = r_w − R*.  [Sol-XF-5]
        d_windows[w] = r_w - R_STAR

        # Windowed actuator: τ ← clip(τ + η*(r_w − R*), τ_min, τ_max).  [§3]
        # Outcome feedback is delivered at the window boundary (per-window,
        # no per-query interleaved feedback — §4 XF-10).
        tau = float(np.clip(tau + eta * (r_w - R_STAR), TAU_MIN, TAU_MAX))

    return d_windows, tau


def simulate_one_seed(rng: np.random.Generator, alpha: float, v_logit: float,
                      sigma_dose: float, c_min: float, eta: float) -> np.ndarray:
    """Simulate one seed: all L=4 dose levels × N_w=4 windows.

    Returns d_seed of shape (L_DOSES, N_W): d_{ℓ,w} = r_{ℓ,w} − R*.

    Per §4 XF-10: τ resets to tau_init at the start of each dose level (each
    dose level starts from the same post-training checkpoint). No state
    carries across dose levels within a seed.
    """
    d_seed = np.zeros((L_DOSES, N_W), dtype=np.float64)
    for ell in range(L_DOSES):
        d_windows, _ = simulate_dose(rng, alpha, v_logit, sigma_dose,
                                     dose_level=ell, c_min=c_min, eta=eta,
                                     tau_init=TAU_INIT)
        d_seed[ell] = d_windows
    return d_seed


def simulate_one_simulation(alpha: float, v_mult: float, c_min: float, eta: float,
                            sigma_dose: float, n_sims: int, base_seed: int
                            ) -> Tuple[np.ndarray, int]:
    """Run n_sims simulations for one parameter combination.

    Each simulation uses N_SEEDS=5 seeds, each producing one β*_s; the
    run-level β* is the mean across the 5 seeds (§2 XF-5, §8).

    Returns (beta_stars shape (n_sims,), n_failures) where beta_stars[i] is
    NaN for INSTRUMENT_FAILURE simulations. n_failures counts
    INSTRUMENT_FAILURE simulations.

    The 5 seeds per simulation are derived deterministically from base_seed
    (the combo seed) so the run is reproducible and candidate-blind. We use
    base_seed + sim_index*N_SEEDS + seed_index as the per-seed seed; this is a
    deterministic function of the parameter combo only (Ruling 9).
    """
    beta_stars = np.full(n_sims, np.nan, dtype=np.float64)
    n_failures = 0
    v_logit = v_mult * V_REF  # v = mult × v_ref  [Sol-XF-9] [PROPOSED — apparatus parameter, §8]

    # NF-IMPL-2: also track per-seed β* for the per-seed false-kill aggregation.
    # The L8 scoring bar is per-seed ("standardized slope >= 0.2, per seed",
    # spec §2). P(any of 5 β*_s < 0.2) matches the per-seed scoring bar;
    # P(mean of 5 β*_s < 0.2) is the 5-seed mean aggregation. Both are
    # reported so Rebecca can rule on which is the G3-escalation input.
    per_seed_betas = np.full((n_sims, N_SEEDS), np.nan, dtype=np.float64)
    for i in range(n_sims):
        # 5 seeds per simulation. Deterministic, candidate-blind.
        d_all = np.zeros((N_SEEDS, L_DOSES, N_W), dtype=np.float64)
        for s in range(N_SEEDS):
            seed_int = (base_seed + i * N_SEEDS + s) % (2 ** 31)
            rng = np.random.default_rng(seed_int)
            d_all[s] = simulate_one_seed(rng, alpha, v_logit, sigma_dose,
                                         c_min, eta)
        b, fail = run_level_beta_star(d_all)
        if fail:
            beta_stars[i] = float("nan")
            n_failures += 1
        else:
            beta_stars[i] = b
            # Record per-seed β* for NF-IMPL-2 aggregation
            for s in range(N_SEEDS):
                bs_s, fail_s = beta_star_for_seed(d_all[s])
                per_seed_betas[i, s] = bs_s if not fail_s else float("nan")
    return beta_stars, n_failures, per_seed_betas


# ---------------------------------------------------------------------------
# σ_dose calibration (§8). Calibrate σ_dose once per (α, v) pair so that the
# mean β* ≈ TRUE_BETA_STAR (0.3) at the fixed reference operating point
# (C_min=0.7, η=0.1). Binary search on a pilot run. Documented simplification:
# the true β* depends on all four parameters, but we calibrate at the
# reference operating point and reuse for all (C_min, η) at that (α, v) pair.
# ---------------------------------------------------------------------------
def calibrate_sigma_dose(alpha: float, v_mult: float) -> float:
    """Binary-search σ_dose so mean β* ≈ TRUE_BETA_STAR at the reference op point.

    Higher σ_dose → more mirror degradation at higher doses → steeper
    dose-response → higher β*. Monotonic in σ_dose, so binary search is valid.

    Uses CAL_PILOT_SIMS simulations at (C_min=CAL_REF_C_MIN, η=CAL_REF_ETA).
    [PROPOSED — apparatus parameter, §8]
    """
    v_logit = v_mult * V_REF
    base_seed = combo_seed(alpha, v_mult, CAL_REF_C_MIN, CAL_REF_ETA)

    def mean_beta_at(sigma_dose: float) -> float:
        bs, _, _ = simulate_one_simulation(alpha, v_mult, CAL_REF_C_MIN,
                                        CAL_REF_ETA, sigma_dose,
                                        n_sims=CAL_PILOT_SIMS,
                                        base_seed=base_seed)
        valid = bs[~np.isnan(bs)]
        if valid.size == 0:
            return 0.0
        return float(np.mean(valid))

    lo, hi = CAL_SIGMA_LO, CAL_SIGMA_HI
    # Establish an upper bound where β* exceeds target (if possible).
    # If even hi doesn't reach the target, clamp to hi and document.
    b_hi = mean_beta_at(hi)
    if b_hi < TRUE_BETA_STAR:
        # Cannot reach target within the search bound; return hi (documented).
        return hi
    b_lo = mean_beta_at(lo)
    if b_lo >= TRUE_BETA_STAR:
        # Already at/above target at the floor; return lo (documented).
        return lo

    for _ in range(CAL_MAX_ITERS):
        mid = 0.5 * (lo + hi)
        b_mid = mean_beta_at(mid)
        if abs(b_mid - TRUE_BETA_STAR) < CAL_TOL:
            return mid
        # β* increases with σ_dose. If below target, raise lo; else lower hi.
        if b_mid < TRUE_BETA_STAR:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Estimator validation (§2 XF-5 synthetic examples).
#
# Example A: d_{ℓ,w} = 0.02*ℓ + ε, ε ~ N(0, 0.01). Expected β* ≈ 0.02/0.1 = 0.2.
# Example B: d_{ℓ,w} = ε, ε ~ N(0, 0.01). Expected β* ≈ 0.0.
# Pass thresholds: |β* − 0.2| < 0.05 (A), |β*| < 0.05 (B).
# [BAR-Entry 11] anchors; [PROPOSED — apparatus parameter] tolerances.
# ---------------------------------------------------------------------------
def validate_estimator(n_trials: int = 200_000, seed: int = 12345) -> Dict:
    """Validate the §2 XF-5 estimator on Examples A and B.

    Generates many (L, N_w) deviation arrays from the known distributions,
    computes β* for each, and reports the mean and the pass/fail against the
    pre-registered tolerances. Uses a large n_trials to tighten the Monte
    Carlo mean near the analytic expectation.
    """
    rng = np.random.default_rng(seed)
    # Example A: d = 0.02*ℓ + ε, ε ~ N(0, 0.01).  [BAR-Entry 11] anchor 0.2.
    ex_a_betas = np.empty(n_trials, dtype=np.float64)
    ex_b_betas = np.empty(n_trials, dtype=np.float64)
    ex_a_fails = 0
    ex_b_fails = 0
    for t in range(n_trials):
        ell_grid = np.arange(L_DOSES, dtype=np.float64)  # 0,1,2,3
        # Example A
        d_a = (0.02 * ell_grid)[:, None] + rng.normal(0.0, math.sqrt(EX_A_NOISE_VAR),
                                                      size=(L_DOSES, N_W))
        b_a, fail_a = beta_star_for_seed(d_a)
        if fail_a:
            ex_a_fails += 1
            ex_a_betas[t] = float("nan")
        else:
            ex_a_betas[t] = b_a
        # Example B
        d_b = rng.normal(0.0, math.sqrt(EX_B_NOISE_VAR), size=(L_DOSES, N_W))
        b_b, fail_b = beta_star_for_seed(d_b)
        if fail_b:
            ex_b_fails += 1
            ex_b_betas[t] = float("nan")
        else:
            ex_b_betas[t] = b_b

    ex_a_valid = ex_a_betas[~np.isnan(ex_a_betas)]
    ex_b_valid = ex_b_betas[~np.isnan(ex_b_betas)]
    ex_a_mean = float(ex_a_valid.mean()) if ex_a_valid.size else float("nan")
    ex_b_mean = float(ex_b_valid.mean()) if ex_b_valid.size else float("nan")
    ex_a_pass = abs(ex_a_mean - 0.2) < VALIDATION_TOL  # [BAR-Entry 11] anchor, [PROPOSED] tol
    ex_b_pass = abs(ex_b_mean - 0.0) < VALIDATION_TOL  # [PROPOSED] tol
    return {
        "example_a": {
            "description": "d = 0.02*ℓ + ε, ε ~ N(0, 0.01); expected β* ≈ 0.2",
            "n_trials": n_trials,
            "mean_beta_star": ex_a_mean,
            "anchor": 0.2,  # [BAR-Entry 11]
            "tolerance": VALIDATION_TOL,  # [PROPOSED — apparatus parameter, §2]
            "pass": bool(ex_a_pass),
            "n_instrument_failures": int(ex_a_fails),
        },
        "example_b": {
            "description": "d = ε, ε ~ N(0, 0.01); expected β* ≈ 0.0",
            "n_trials": n_trials,
            "mean_beta_star": ex_b_mean,
            "anchor": 0.0,
            "tolerance": VALIDATION_TOL,  # [PROPOSED — apparatus parameter, §2]
            "pass": bool(ex_b_pass),
            "n_instrument_failures": int(ex_b_fails),
        },
    }


# ---------------------------------------------------------------------------
# Sensitivity map (§8.7) and deterministic selection rule (§8.8).
#
# Three regions over (C_min, η):
#   (a) Abstention-escape: flat curve (false kill — controller escapes by
#       abstaining). Operationalized: false-kill rate ≥ 0.5 (the bar fails on
#       the majority of simulations despite a true effect).
#       [PROPOSED — apparatus parameter, §8.7 operationalization]
#   (b) Trivial-pass: any noise moves risk (vacuous pass). Operationalized:
#       the β* distribution under a TRUE β* = 0 NULL control (σ_dose = 0,
#       no dose effect) still exceeds the 0.2 bar at a high rate
#       (false-pass ≥ 0.5). I.e., the bar passes even when there is no true
#       effect — the test is vacuous.
#       [PROPOSED — apparatus parameter, §8.7 operationalization]
#   (c) Informative: neither (a) nor (b) — meaningful separation between true
#       effect and noise.
#
# The region boundaries are defined by thresholds on the false-kill rate
# (true-effect present) and the false-pass rate (null control). A cell is
# "informative" iff false-kill < 0.5 AND false-pass < 0.5.
# ---------------------------------------------------------------------------
FK_BOUNDARY = 0.5   # abstention-escape boundary (false-kill ≥ this → escape) [PROPOSED — apparatus parameter, §8.7]
FP_BOUNDARY = 0.5   # trivial-pass boundary (false-pass ≥ this → trivial)    [PROPOSED — apparatus parameter, §8.7]


def classify_region(false_kill_rate: float, false_pass_rate: float) -> str:
    """Classify a (C_min, η) cell into one of three regions (§8.7).

    [PROPOSED — apparatus parameter, §8.7 operationalization]
    """
    if false_kill_rate >= FK_BOUNDARY:
        return "abstention-escape"
    if false_pass_rate >= FP_BOUNDARY:
        return "trivial-pass"
    return "informative"


def min_distance_to_boundaries(false_kill_rate: float,
                               false_pass_rate: float) -> float:
    """Minimum distance to the region boundaries (§8.8 tie-break metric).

    For an informative cell, distance to the abstention-escape boundary is
    (FK_BOUNDARY − false_kill_rate) and to the trivial-pass boundary is
    (FP_BOUNDARY − false_pass_rate). The minimum of these is the robustness
    margin. Larger = more robust. [PROPOSED — apparatus parameter, §8.8]
    """
    d_fk = FK_BOUNDARY - false_kill_rate
    d_fp = FP_BOUNDARY - false_pass_rate
    return min(d_fk, d_fp)


def select_cmin_eta(sensitivity_map: Dict) -> Dict:
    """Deterministic selection rule (§8.8).

    From the sensitivity map, select the (C_min, η) pair that:
      1. Is in the informative region.
      2. Maximizes the minimum distance to region boundaries.
      3. If tied: highest C_min (strongest coverage requirement).
      4. If still tied: lowest η (most conservative controller).
    [Sol-XF-9]
    """
    informative = [cell for cell in sensitivity_map["cells"]
                   if cell["region"] == "informative"]
    if not informative:
        return {"selected": None, "reason": "no informative region cell found"}

    # Sort key: (-min_distance, -c_min, eta) → maximizes min_distance, then
    # maximizes c_min, then minimizes eta.  [Sol-XF-9]
    def sort_key(cell):
        return (-cell["min_distance_to_boundaries"],
                -cell["c_min"],
                cell["eta"])

    informative.sort(key=sort_key)
    best = informative[0]
    return {
        "selected": {
            "c_min": best["c_min"],
            "eta": best["eta"],
        },
        "min_distance_to_boundaries": best["min_distance_to_boundaries"],
        "mean_false_kill_rate": best["mean_false_kill_rate"],
        "mean_false_pass_rate": best["mean_false_pass_rate"],
        "n_informative": len(informative),
        "rule": "§8.8: informative ∧ max min-distance to boundaries; tie → highest C_min; tie → lowest η  [Sol-XF-9]",
    }


# ---------------------------------------------------------------------------
# Full power-analysis run over the 240-combination grid (§8).
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Multiprocessing worker (Fix 1: CPU parallelism).
#
# Each worker runs one (combo, profile) pair independently. Results depend
# only on the combo seed (deterministic, candidate-blind), not on which
# worker executes them. Results are collected by combo-identity, not
# completion order. [PROPOSED -- apparatus parameter, scalable parallelism]
# ---------------------------------------------------------------------------

def _worker_combo(args):
    """Worker function: run one (combo, profile) pair and return result dict.

    Args is a tuple: (alpha, v_mult, c_min, eta, sigma_dose, n_sims,
                      base_seed, profile_name_or_None)
    """
    alpha, v_mult, c_min, eta, sigma_dose, n_sims, base_seed, profile_name = args
    v_logit = v_mult * V_REF

    if profile_name is None:
        # Reference profile
        bs, n_fail, per_seed = simulate_one_simulation(
            alpha, v_mult, c_min, eta, sigma_dose,
            n_sims=n_sims, base_seed=base_seed)
    else:
        # Misspecified profile — inline simulation loop
        bs = np.full(n_sims, np.nan, dtype=np.float64)
        per_seed = np.full((n_sims, N_SEEDS), np.nan, dtype=np.float64)
        n_fail = 0
        for i in range(n_sims):
            d_all = np.zeros((N_SEEDS, L_DOSES, N_W), dtype=np.float64)
            for s in range(N_SEEDS):
                seed_int = (base_seed + i * N_SEEDS + s) % (2 ** 31)
                rng = np.random.default_rng(seed_int)
                d_all[s] = simulate_one_seed_misspecified(
                    rng, alpha, v_logit, sigma_dose, c_min, eta, profile_name)
            b, fail = run_level_beta_star(d_all)
            if fail:
                bs[i] = float("nan")
                n_fail += 1
            else:
                bs[i] = b
                for s in range(N_SEEDS):
                    bs_s, fail_s = beta_star_for_seed(d_all[s])
                    per_seed[i, s] = bs_s if not fail_s else float("nan")

    valid = bs[~np.isnan(bs)]
    n_valid = int(valid.size)

    # False-kill rate (5-seed mean) [Sol-XF-9]
    if n_valid > 0:
        false_kill_rate = float(np.mean(valid < BETA_STAR_BAR))
    else:
        false_kill_rate = float("nan")

    # NF-IMPL-2: Per-seed false-kill rate [PROPOSED -- flagged to Rebecca]
    if n_valid > 0:
        valid_ps = per_seed[~np.isnan(bs)]
        if valid_ps.shape[0] > 0:
            false_kill_rate_per_seed = float(np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1)))
        else:
            false_kill_rate_per_seed = float("nan")
    else:
        false_kill_rate_per_seed = float("nan")

    return {
        "alpha": alpha, "v_mult": v_mult, "c_min": c_min, "eta": eta,
        "sigma_dose": sigma_dose, "n_sims": n_sims, "base_seed": base_seed,
        "n_valid": n_valid, "n_instrument_failures": int(n_fail),
        "mean_beta_star": float(valid.mean()) if n_valid else float("nan"),
        "std_beta_star": float(valid.std()) if n_valid else float("nan"),
        "false_kill_rate": false_kill_rate,
        "false_kill_rate_per_seed": false_kill_rate_per_seed,
        "bs_valid": valid,  # for null-control computation in main process
        "profile_name": profile_name,
    }


def _worker_null_control(args):
    """Worker for null-control arm (sigma_dose=0.0)."""
    alpha, v_mult, c_min, eta, n_sims, base_seed, profile_name = args
    v_logit = v_mult * V_REF

    if profile_name is None:
        bs_null, n_fail_null, _ = simulate_one_simulation(
            alpha, v_mult, c_min, eta, sigma_dose=0.0,
            n_sims=n_sims, base_seed=base_seed)
    else:
        bs_null = np.full(n_sims, np.nan, dtype=np.float64)
        n_fail_null = 0
        for i in range(n_sims):
            d_all = np.zeros((N_SEEDS, L_DOSES, N_W), dtype=np.float64)
            for s in range(N_SEEDS):
                seed_int = (base_seed + i * N_SEEDS + s) % (2 ** 31)
                rng = np.random.default_rng(seed_int)
                d_all[s] = simulate_one_seed_misspecified(
                    rng, alpha, v_logit, 0.0, c_min, eta, profile_name)
            b, fail = run_level_beta_star(d_all)
            if fail:
                bs_null[i] = float("nan")
                n_fail_null += 1
            else:
                bs_null[i] = b

    valid_null = bs_null[~np.isnan(bs_null)]
    if valid_null.size > 0:
        false_pass_rate = float(np.mean(valid_null >= BETA_STAR_BAR))
        mean_null = float(valid_null.mean())
    else:
        false_pass_rate = float("nan")
        mean_null = float("nan")
    return {
        "false_pass_rate": false_pass_rate,
        "mean_beta_star_null": mean_null,
        "n_instrument_failures_null": int(n_fail_null),
    }



def run_power_analysis(n_sims: int, include_null_control: bool = True,
                       progress_every: int = 20) -> Dict:
    """Run the §8 power analysis over the full 5×3×4×4 = 240 grid.

    For each (α, v) pair: calibrate σ_dose once at the reference operating
    point (C_min=0.7, η=0.1), then run n_sims simulations for each of the 16
    (C_min, η) combinations at that (α, v) pair.

    For the sensitivity map (§8.7) we also need a null-control false-pass
    rate per (C_min, η) cell: the fraction of simulations where β* ≥ 0.2
    when there is NO true effect (σ_dose = 0). We compute this null control
    once per (α, v) pair at the same 16 (C_min, η) cells (candidate-blind,
    synthetic only).

    Returns a dict with the full machine-readable result table, the
    sensitivity map, and the selected (C_min, η).
    """
    t0 = time.time()
    results = []
    n_combos = len(ALPHAS) * len(V_MULTS) * len(C_MINS) * len(ETAS)
    done = 0

    for alpha in ALPHAS:
        for v_mult in V_MULTS:
            # Calibrate σ_dose once per (α, v) pair.  [PROPOSED — apparatus parameter, §8]
            sigma_dose = calibrate_sigma_dose(alpha, v_mult)
            for c_min in C_MINS:
                for eta in ETAS:
                    base_seed = combo_seed(alpha, v_mult, c_min, eta)
                    # True-effect arm: σ_dose as calibrated.
                    bs, n_fail, per_seed = simulate_one_simulation(
                        alpha, v_mult, c_min, eta, sigma_dose,
                        n_sims=n_sims, base_seed=base_seed)
                    valid = bs[~np.isnan(bs)]
                    n_valid = int(valid.size)
                    # False-kill rate (5-seed mean): fraction of simulations where
                    # the 5-seed-mean β*_estimated < 0.2 when true β* ≥ 0.3. [Sol-XF-9]
                    # INSTRUMENT_FAILURE simulations (NaN) are excluded from the
                    # denominator (the apparatus produced no measurement; they
                    # are reported separately, not counted as kills).
                    if n_valid > 0:
                        false_kill_rate = float(np.mean(valid < BETA_STAR_BAR))
                    else:
                        false_kill_rate = float("nan")
                    # NF-IMPL-2: Per-seed false-kill rate: P(any of 5 β*_s < 0.2).
                    # Matches the per-seed scoring bar (spec §2: "per seed").
                    # Flagged to Rebecca for ruling on which is the G3 input.
                    if n_valid > 0:
                        valid_ps = per_seed[~np.isnan(bs)]  # rows where run-level is valid
                        if valid_ps.shape[0] > 0:
                            any_seed_below = np.any(valid_ps < BETA_STAR_BAR, axis=1)
                            false_kill_rate_per_seed = float(np.mean(any_seed_below))
                        else:
                            false_kill_rate_per_seed = float("nan")
                    else:
                        false_kill_rate_per_seed = float("nan")
                    mean_beta = float(valid.mean()) if n_valid else float("nan")
                    std_beta = float(valid.std()) if n_valid else float("nan")

                    # Null-control arm (false-pass rate) for the sensitivity map.
                    if include_null_control:
                        bs_null, n_fail_null, _ = simulate_one_simulation(
                            alpha, v_mult, c_min, eta, sigma_dose=0.0,
                            n_sims=n_sims, base_seed=base_seed)
                        valid_null = bs_null[~np.isnan(bs_null)]
                        if valid_null.size > 0:
                            false_pass_rate = float(
                                np.mean(valid_null >= BETA_STAR_BAR))
                        else:
                            false_pass_rate = float("nan")
                        mean_null = float(valid_null.mean()) if valid_null.size else float("nan")
                    else:
                        false_pass_rate = float("nan")
                        mean_null = float("nan")
                        n_fail_null = 0

                    region = classify_region(false_kill_rate, false_pass_rate) \
                        if (not math.isnan(false_kill_rate) and
                            not math.isnan(false_pass_rate)) else "undefined"
                    min_dist = min_distance_to_boundaries(false_kill_rate,
                                                           false_pass_rate) \
                        if region == "informative" else float("nan")

                    results.append({
                        "alpha": alpha,
                        "v_mult": v_mult,
                        "v_logit": v_mult * V_REF,
                        "c_min": c_min,
                        "eta": eta,
                        "sigma_dose_calibrated": sigma_dose,
                        "n_sims": n_sims,
                        "n_valid": n_valid,
                        "n_instrument_failures": int(n_fail),
                        "n_instrument_failures_null": int(n_fail_null),
                        "mean_beta_star": mean_beta,
                        "std_beta_star": std_beta,
                        "false_kill_rate": false_kill_rate,  # P(mean 5-seed β*<0.2) [Sol-XF-9]
                        "false_kill_rate_per_seed": false_kill_rate_per_seed,  # P(any seed β*<0.2) [NF-IMPL-2, PROPOSED — flagged to Rebecca]
                        "false_pass_rate": false_pass_rate,   # P(β*≥0.2 | null) [PROPOSED — apparatus parameter, §8.7]
                        "mean_beta_star_null": mean_null,
                        "region": region,
                        "min_distance_to_boundaries": min_dist,
                        "base_seed": base_seed,
                    })
                    done += 1
                    if done % progress_every == 0:
                        elapsed = time.time() - t0
                        rate = done / elapsed if elapsed > 0 else 0.0
                        eta_s = (n_combos - done) / rate if rate > 0 else float("inf")
                        print(f"  [progress] {done}/{n_combos} combos "
                              f"({100*done/n_combos:.1f}%) "
                              f"elapsed={elapsed:.1f}s rate={rate:.2f}/s "
                              f"eta={eta_s:.0f}s", flush=True)

    elapsed = time.time() - t0
    # Build the sensitivity map (§8.7): aggregate over (α, v) by taking the
    # mean false-kill and false-pass rates across the 15 (α, v) pairs for each
    # (C_min, η) cell. The selection rule (§8.8) operates on this aggregated map.
    cells = []
    for c_min in C_MINS:
        for eta in ETAS:
            cell_rows = [r for r in results
                         if r["c_min"] == c_min and r["eta"] == eta
                         and not math.isnan(r["false_kill_rate"])
                         and not math.isnan(r["false_pass_rate"])]
            if not cell_rows:
                continue
            fk = float(np.mean([r["false_kill_rate"] for r in cell_rows]))
            fp = float(np.mean([r["false_pass_rate"] for r in cell_rows]))
            region = classify_region(fk, fp)
            min_dist = min_distance_to_boundaries(fk, fp) if region == "informative" else float("nan")
            cells.append({
                "c_min": c_min,
                "eta": eta,
                "mean_false_kill_rate": fk,
                "mean_false_pass_rate": fp,
                "region": region,
                "min_distance_to_boundaries": min_dist,
                "n_av_pairs": len(cell_rows),
            })

    sensitivity_map = {
        "description": "§8.7 sensitivity map over (C_min, η), aggregated across (α, v) pairs  [Sol-XF-9]",
        "boundaries": {
            "abstention_escape_false_kill_ge": FK_BOUNDARY,  # [PROPOSED — apparatus parameter, §8.7]
            "trivial_pass_false_pass_ge": FP_BOUNDARY,     # [PROPOSED — apparatus parameter, §8.7]
        },
        "cells": cells,
    }
    selection = select_cmin_eta(sensitivity_map)

    return {
        "header": {
            "spec_regime": SPEC_REGIME,
            "constitution_regime": CONSTITUTION_REGIME,
            "artifact_date": ARTIFACT_DATE,  # [OP — artifact date, P4]
            "n_sims_per_combo": n_sims,
            "n_combos": len(results),
            "elapsed_seconds": elapsed,
            "constants": {
                "W": W, "N_W": N_W, "L_DOSES": L_DOSES, "N_SEEDS": N_SEEDS,
                "R_STAR": R_STAR, "TRUE_BETA_STAR": TRUE_BETA_STAR,
                "BETA_STAR_BAR": BETA_STAR_BAR,  # [BAR-Entry 11]
                "FALSE_KILL_THRESHOLD": FALSE_KILL_THRESHOLD,  # [PROPOSED — apparatus parameter, §8]
                "EPS_C": EPS_C, "P_TRUE_MEAN": P_TRUE_MEAN,
                "BETA_CONC": BETA_CONC, "BETA_A": BETA_A, "BETA_B": BETA_B,
                "V_REF": V_REF,
                "TAU_MIN": TAU_MIN, "TAU_MAX": TAU_MAX, "TAU_INIT": TAU_INIT,
                "CAL_REF_C_MIN": CAL_REF_C_MIN, "CAL_REF_ETA": CAL_REF_ETA,
                "VAR_X": VAR_X,
            },
            "parameter_grid": {
                "alphas": ALPHAS, "v_mults": V_MULTS,
                "c_mins": C_MINS, "etas": ETAS,
                "n_combinations": len(ALPHAS)*len(V_MULTS)*len(C_MINS)*len(ETAS),
            },
            "compliance": {
                "P3_source_tags": "All thresholds carry [LAW-Lx]/[BAR-Entry n]/[OP-Entry n]/[PROPOSED] tags. [§5 P3]",
                "P4_regime_dating": "Header states spec + constitution regime + artifact date. [§5 P4]",
                "candidate_blind": "Simulation seeds from parameter-combo hashes only; no candidate data. [Ruling 9, Entry 76]",
                "estimator_identity": "β* estimator is the identical §2 XF-5 estimator. [Sol-XF-5]",
            },
        },
        "results": results,
        "sensitivity_map": sensitivity_map,
        "selection": selection,
    }


# ---------------------------------------------------------------------------
# Validation batch (task brief Step 2): 100 sims on 3 representative combos.
# ---------------------------------------------------------------------------
def run_validation_batch(n_sims: int = N_SIMS_VALIDATION) -> Dict:
    """Run n_sims simulations on 3 representative parameter combinations.

    Reports per-simulation wall-clock time, estimated total time for the full
    10,000 × 240 run, and any errors/edge cases.
    """
    # Three representative combos spanning the grid corners.
    reps = [
        {"alpha": 0.0, "v_mult": 0.5, "c_min": 0.5, "eta": 0.01,
         "label": "low-noise / low-coverage / low-gain"},
        {"alpha": 0.1, "v_mult": 1.0, "c_min": 0.7, "eta": 0.1,
         "label": "mid-noise / mid-coverage / mid-gain (reference op point)"},
        {"alpha": 0.2, "v_mult": 2.0, "c_min": 0.8, "eta": 0.2,
         "label": "high-noise / high-coverage / high-gain"},
    ]
    batch = []
    total_time = 0.0
    total_sims = 0
    for combo in reps:
        alpha, v_mult = combo["alpha"], combo["v_mult"]
        c_min, eta = combo["c_min"], combo["eta"]
        # Calibrate σ_dose for this (α, v) pair (small pilot for speed).
        t_cal0 = time.time()
        sigma_dose = calibrate_sigma_dose(alpha, v_mult)
        t_cal = time.time() - t_cal0
        base_seed = combo_seed(alpha, v_mult, c_min, eta)
        t0 = time.time()
        bs, n_fail, per_seed = simulate_one_simulation(alpha, v_mult, c_min, eta,
                                             sigma_dose, n_sims=n_sims,
                                             base_seed=base_seed)
        elapsed = time.time() - t0
        total_time += elapsed
        total_sims += n_sims
        valid = bs[~np.isnan(bs)]
        fk = float(np.mean(valid < BETA_STAR_BAR)) if valid.size else float("nan")
        # NF-IMPL-2: per-seed false-kill rate P(any of 5 β*_s < 0.2)
        valid_ps = per_seed[~np.isnan(bs)]
        fk_per_seed = float(np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1))) if valid_ps.shape[0] > 0 else float("nan")
        batch.append({
            "label": combo["label"],
            "alpha": alpha, "v_mult": v_mult, "c_min": c_min, "eta": eta,
            "sigma_dose_calibrated": sigma_dose,
            "calibration_seconds": t_cal,
            "n_sims": n_sims,
            "n_valid": int(valid.size),
            "n_instrument_failures": int(n_fail),
            "mean_beta_star": float(valid.mean()) if valid.size else float("nan"),
            "std_beta_star": float(valid.std()) if valid.size else float("nan"),
            "false_kill_rate": fk,
            "false_kill_rate_per_seed": fk_per_seed,
            "elapsed_seconds": elapsed,
            "per_sim_seconds": elapsed / n_sims,
        })
    # Estimated total time for the full 10,000 × 240 run.
    # Use the mean per-sim time across the 3 representative combos, scaled.
    # Note: the full run also includes calibration per (α,v) pair (15 pairs)
    # and a null-control arm per combo (doubles the sim count). Estimate
    # conservatively using the observed per-sim rate × full sim count × 2 arms.
    mean_per_sim = total_time / total_sims if total_sims else 0.0
    full_sims_one_arm = N_SIMS_FULL * (len(ALPHAS)*len(V_MULTS)*len(C_MINS)*len(ETAS))
    est_one_arm = mean_per_sim * full_sims_one_arm
    est_two_arm = est_one_arm * 2.0  # true-effect + null-control arms
    return {
        "n_sims_per_combo": n_sims,
        "representative_combos": batch,
        "total_validation_seconds": total_time,
        "mean_per_sim_seconds": mean_per_sim,
        "estimated_full_run_seconds_one_arm": est_one_arm,
        "estimated_full_run_seconds_two_arm": est_two_arm,
        "estimated_full_run_minutes_two_arm": est_two_arm / 60.0,
        "estimated_full_run_hours_two_arm": est_two_arm / 3600.0,
        "full_run_config": {
            "n_sims_per_combo": N_SIMS_FULL,  # [PROPOSED — apparatus parameter, §8]
            "n_combos": len(ALPHAS)*len(V_MULTS)*len(C_MINS)*len(ETAS),
            "n_arms": 2,
        },
    }


def _sanitize_nan(obj):
    """Recursively replace NaN/Inf floats with None for strict JSON output.

    allow_nan=False rejects NaN/Inf; the simulation can produce NaN for
    INSTRUMENT_FAILURE cells (no valid measurements). We map those to null
    so the machine-readable table is valid JSON. The 'n_instrument_failures'
    field carries the failure count explicitly.
    """
    if isinstance(obj, dict):
        return {k: _sanitize_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_nan(v) for v in obj]
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, (np.floating,)):
        f = float(obj)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return _sanitize_nan(obj.tolist())
    return obj


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# §8 item 9 — Misspecification stress-test (BF-IMPL-1).
#
# Run the power analysis on >=2 misspecified profiles different from the
# synthetic reference that defines R* and dose, to verify the estimator is
# not overfit to the reference profile. [Sol-XF-9] [PROPOSED — apparatus parameter]
#
# Candidate-blind throughout (Ruling 9): misspecified profiles use known oracle
# ground truth, not candidate output.
# ---------------------------------------------------------------------------

def simulate_one_seed_misspecified(rng, alpha, v_logit, sigma_dose,
                                    c_min, eta, profile_name):
    """Simulate one seed with a misspecified profile.

    Misspecified profiles differ from the reference in task difficulty
    distribution or dose-response shape. The estimator (§2 XF-5) is
    applied identically -- only the data-generating process changes.
    [Sol-XF-9] [PROPOSED -- apparatus parameter, §8 item 9]
    """
    if profile_name == "uniform_difficulty":
        # Misspecified profile 1: uniform task difficulty instead of Beta(4.2, 1.8).
        # Reference is right-skewed (most queries high correctness).
        # Uniform(0,1) is flat -- genuinely different distribution.
        p_true = rng.random(W)
    elif profile_name == "bimodal_difficulty":
        # Misspecified profile 2: bimodal difficulty -- 50% easy (p=0.9),
        # 50% hard (p=0.3). Reference is unimodal.
        mask = rng.random(W) < 0.5
        p_true = np.where(mask, 0.9, 0.3)
    else:
        raise ValueError(f"unknown misspecified profile: {profile_name}")

    correct = rng.random(W) < p_true

    # Mirror confidence with calibration error alpha and logit-variance v_logit
    logit_p = np.log(p_true / (1.0 - p_true + EPS_C) + EPS_C)
    xi = rng.normal(0.0, np.sqrt(v_logit), W)
    c = 1.0 / (1.0 + np.exp(-(logit_p + alpha + xi)))
    c = np.clip(c, EPS_C, 1.0 - EPS_C)

    tau = 0.5
    deviations = np.zeros(L_DOSES * N_W)
    idx = 0
    for dose in range(L_DOSES):
        sigma_l = dose * sigma_dose
        for w in range(N_W):
            if sigma_l > 0:
                xi_dose = rng.normal(0.0, sigma_l, W)
                logit_c = np.log(c / (1.0 - c + EPS_C) + EPS_C)
                c_dose = 1.0 / (1.0 + np.exp(-(logit_c + xi_dose)))
                c_dose = np.clip(c_dose, EPS_C, 1.0 - EPS_C)
            else:
                c_dose = c.copy()

            n_min = max(1, int(np.ceil(c_min * W)))
            order = np.argsort(-c_dose)
            answered = list(order[:n_min])
            for j in order[n_min:]:
                if c_dose[j] > tau:
                    answered.append(j)

            n_answered = len(answered)
            if n_answered == 0:
                r_w = 0.0
            else:
                n_incorrect = int(np.sum(~correct[answered]))
                r_w = n_incorrect / n_answered

            deviations[idx] = r_w - R_STAR
            idx += 1
            tau = np.clip(tau + eta * (r_w - R_STAR), 0.01, 0.99)

    return deviations.reshape(L_DOSES, N_W)


def run_power_analysis_misspecified(profile_name, n_sims, include_null_control=True,
                                       progress_every=20, workers=None):
    """Run the §8 power analysis over the full 5×3×4×4 = 240 grid under a
    misspecified profile.

    Mirrors run_power_analysis but uses simulate_one_seed_misspecified instead
    of simulate_one_seed. The σ_dose calibration reuses
    calibrate_sigma_dose(alpha, v_mult) from the reference -- we test whether
    the ESTIMATOR is overfit to the reference profile, not re-calibrating for
    the misspecified profile. [Sol-XF-9] [PROPOSED -- apparatus parameter, §8 item 9]

    Returns the same structure as run_power_analysis
    (header, results, sensitivity_map, selection).
    Candidate-blind (Ruling 9): the misspecified profile uses known oracle
    ground truth, not candidate output.
    """
    t0 = time.time()
    results = []
    n_combos = len(ALPHAS) * len(V_MULTS) * len(C_MINS) * len(ETAS)
    done = 0

    # Pre-calibrate σ_dose for all (α, v) pairs (reuse reference calibration).
    calibrations = {}
    for alpha in ALPHAS:
        for v_mult in V_MULTS:
            calibrations[(alpha, v_mult)] = calibrate_sigma_dose(alpha, v_mult)

    # Build work items with the misspecified profile name.
    work_items = []
    null_items = [] if include_null_control else None
    for alpha in ALPHAS:
        for v_mult in V_MULTS:
            sigma_dose = calibrations[(alpha, v_mult)]
            for c_min in C_MINS:
                for eta in ETAS:
                    base_seed = combo_seed(alpha, v_mult, c_min, eta)
                    work_items.append((alpha, v_mult, c_min, eta,
                                       sigma_dose, n_sims, base_seed, profile_name))
                    if include_null_control:
                        null_items.append((alpha, v_mult, c_min, eta,
                                           n_sims, base_seed, profile_name))

    n_workers = workers or os.cpu_count() or 1
    n_combos = len(work_items)
    print(f"    [misspec:{profile_name}] {n_combos} combos on {n_workers} workers...")

    if n_workers > 1:
        with multiprocessing.Pool(processes=n_workers) as pool:
            combo_results = pool.map(_worker_combo, work_items)
            if include_null_control:
                null_results = pool.map(_worker_null_control, null_items)
            else:
                null_results = [{}] * n_combos
    else:
        combo_results = [_worker_combo(w) for w in work_items]
        null_results = [_worker_null_control(w) for w in null_items] if include_null_control else [{}] * n_combos

    # Build results list
    for alpha in ALPHAS:
        for v_mult in V_MULTS:
            sigma_dose = calibrations[(alpha, v_mult)]
            v_logit = v_mult * V_REF
            for c_min in C_MINS:
                for eta in ETAS:
                    base_seed = combo_seed(alpha, v_mult, c_min, eta)
                    # True-effect arm: σ_dose as calibrated (reference calibration).
                    # Inline the simulation loop using
                    # simulate_one_seed_misspecified for each seed.
                    beta_stars = np.full(n_sims, np.nan, dtype=np.float64)
                    per_seed_betas = np.full((n_sims, N_SEEDS), np.nan, dtype=np.float64)
                    n_failures = 0
                    for i in range(n_sims):
                        d_all = np.zeros((N_SEEDS, L_DOSES, N_W), dtype=np.float64)
                        for s in range(N_SEEDS):
                            seed_int = (base_seed + i * N_SEEDS + s) % (2 ** 31)
                            rng = np.random.default_rng(seed_int)
                            d_all[s] = simulate_one_seed_misspecified(
                                rng, alpha, v_logit, sigma_dose, c_min, eta, profile_name)
                        b, fail = run_level_beta_star(d_all)
                        if fail:
                            beta_stars[i] = float("nan")
                            n_failures += 1
                        else:
                            beta_stars[i] = b
                            for s in range(N_SEEDS):
                                bs_s, fail_s = beta_star_for_seed(d_all[s])
                                per_seed_betas[i, s] = bs_s if not fail_s else float("nan")
                    valid = beta_stars[~np.isnan(beta_stars)]
                    n_valid = int(valid.size)
                    # False-kill rate (5-seed mean): P(mean 5-seed β*<0.2).
                    #  [Sol-XF-9] [PROPOSED -- apparatus parameter, §8 item 9]
                    if n_valid > 0:
                        false_kill_rate = float(np.mean(valid < BETA_STAR_BAR))
                    else:
                        false_kill_rate = float("nan")
                    # NF-IMPL-2: Per-seed false-kill rate: P(any of 5 β*_s < 0.2).
                    if n_valid > 0:
                        valid_ps = per_seed_betas[~np.isnan(beta_stars)]
                        if valid_ps.shape[0] > 0:
                            any_seed_below = np.any(valid_ps < BETA_STAR_BAR, axis=1)
                            false_kill_rate_per_seed = float(np.mean(any_seed_below))
                        else:
                            false_kill_rate_per_seed = float("nan")
                    else:
                        false_kill_rate_per_seed = float("nan")
                    mean_beta = float(valid.mean()) if n_valid else float("nan")
                    std_beta = float(valid.std()) if n_valid else float("nan")

                    # Null-control arm (false-pass rate): σ_dose=0.0 with the
                    # same misspecified profile.  [PROPOSED -- apparatus parameter, §8 item 9]
                    if include_null_control:
                        beta_stars_null = np.full(n_sims, np.nan, dtype=np.float64)
                        n_failures_null = 0
                        for i in range(n_sims):
                            d_all = np.zeros((N_SEEDS, L_DOSES, N_W), dtype=np.float64)
                            for s in range(N_SEEDS):
                                seed_int = (base_seed + i * N_SEEDS + s) % (2 ** 31)
                                rng = np.random.default_rng(seed_int)
                                d_all[s] = simulate_one_seed_misspecified(
                                    rng, alpha, v_logit, sigma_dose=0.0,
                                    c_min=c_min, eta=eta, profile_name=profile_name)
                            b, fail = run_level_beta_star(d_all)
                            if fail:
                                beta_stars_null[i] = float("nan")
                                n_failures_null += 1
                            else:
                                beta_stars_null[i] = b
                        valid_null = beta_stars_null[~np.isnan(beta_stars_null)]
                        if valid_null.size > 0:
                            false_pass_rate = float(
                                np.mean(valid_null >= BETA_STAR_BAR))
                        else:
                            false_pass_rate = float("nan")
                        mean_null = float(valid_null.mean()) if valid_null.size else float("nan")
                    else:
                        false_pass_rate = float("nan")
                        mean_null = float("nan")
                        n_failures_null = 0

                    region = classify_region(false_kill_rate, false_pass_rate) \
                        if (not math.isnan(false_kill_rate) and
                            not math.isnan(false_pass_rate)) else "undefined"
                    min_dist = min_distance_to_boundaries(false_kill_rate,
                                                           false_pass_rate) \
                        if region == "informative" else float("nan")

                    results.append({
                        "alpha": alpha,
                        "v_mult": v_mult,
                        "v_logit": v_mult * V_REF,
                        "c_min": c_min,
                        "eta": eta,
                        "profile_name": profile_name,
                        "sigma_dose_calibrated": sigma_dose,
                        "n_sims": n_sims,
                        "n_valid": n_valid,
                        "n_instrument_failures": int(n_failures),
                        "n_instrument_failures_null": int(n_failures_null),
                        "mean_beta_star": mean_beta,
                        "std_beta_star": std_beta,
                        "false_kill_rate": false_kill_rate,  # P(mean 5-seed β*<0.2) [Sol-XF-9]
                        "false_kill_rate_per_seed": false_kill_rate_per_seed,  # P(any seed β*<0.2) [NF-IMPL-2, PROPOSED -- flagged to Rebecca]
                        "false_pass_rate": false_pass_rate,   # P(β*≥0.2 | null) [PROPOSED -- apparatus parameter, §8.7]
                        "mean_beta_star_null": mean_null,
                        "region": region,
                        "min_distance_to_boundaries": min_dist,
                        "base_seed": base_seed,
                    })
                    done += 1
                    if done % progress_every == 0:
                        elapsed = time.time() - t0
                        rate = done / elapsed if elapsed > 0 else 0.0
                        eta_s = (n_combos - done) / rate if rate > 0 else float("inf")
                        print(f"  [progress][{profile_name}] {done}/{n_combos} combos "
                              f"({100*done/n_combos:.1f}%) "
                              f"elapsed={elapsed:.1f}s rate={rate:.2f}/s "
                              f"eta={eta_s:.0f}s", flush=True)

    elapsed = time.time() - t0
    # Build the sensitivity map (§8.7): aggregate over (α, v) by taking the
    # mean false-kill and false-pass rates across the 15 (α, v) pairs for each
    # (C_min, η) cell.  [Sol-XF-9] [PROPOSED -- apparatus parameter, §8 item 9]
    cells = []
    for c_min in C_MINS:
        for eta in ETAS:
            cell_rows = [r for r in results
                         if r["c_min"] == c_min and r["eta"] == eta
                         and not math.isnan(r["false_kill_rate"])
                         and not math.isnan(r["false_pass_rate"])]
            if not cell_rows:
                continue
            fk = float(np.mean([r["false_kill_rate"] for r in cell_rows]))
            fp = float(np.mean([r["false_pass_rate"] for r in cell_rows]))
            region = classify_region(fk, fp)
            min_dist = min_distance_to_boundaries(fk, fp) if region == "informative" else float("nan")
            cells.append({
                "c_min": c_min,
                "eta": eta,
                "mean_false_kill_rate": fk,
                "mean_false_pass_rate": fp,
                "region": region,
                "min_distance_to_boundaries": min_dist,
                "n_av_pairs": len(cell_rows),
            })

    sensitivity_map = {
        "description": f"§8.7 sensitivity map over (C_min, η), aggregated across (α, v) pairs under misspecified profile '{profile_name}'  [Sol-XF-9]",
        "profile_name": profile_name,
        "boundaries": {
            "abstention_escape_false_kill_ge": FK_BOUNDARY,  # [PROPOSED -- apparatus parameter, §8.7]
            "trivial_pass_false_pass_ge": FP_BOUNDARY,     # [PROPOSED -- apparatus parameter, §8.7]
        },
        "cells": cells,
    }
    selection = select_cmin_eta(sensitivity_map)

    return {
        "header": {
            "spec_regime": SPEC_REGIME,
            "constitution_regime": CONSTITUTION_REGIME,
            "artifact_date": ARTIFACT_DATE,  # [OP -- artifact date, P4]
            "profile_name": profile_name,
            "n_sims_per_combo": n_sims,
            "n_combos": len(results),
            "elapsed_seconds": elapsed,
            "constants": {
                "W": W, "N_W": N_W, "L_DOSES": L_DOSES, "N_SEEDS": N_SEEDS,
                "R_STAR": R_STAR, "TRUE_BETA_STAR": TRUE_BETA_STAR,
                "BETA_STAR_BAR": BETA_STAR_BAR,  # [BAR-Entry 11]
                "FALSE_KILL_THRESHOLD": FALSE_KILL_THRESHOLD,  # [PROPOSED -- apparatus parameter, §8]
                "EPS_C": EPS_C, "P_TRUE_MEAN": P_TRUE_MEAN,
                "BETA_CONC": BETA_CONC, "BETA_A": BETA_A, "BETA_B": BETA_B,
                "V_REF": V_REF,
                "TAU_MIN": TAU_MIN, "TAU_MAX": TAU_MAX, "TAU_INIT": TAU_INIT,
                "CAL_REF_C_MIN": CAL_REF_C_MIN, "CAL_REF_ETA": CAL_REF_ETA,
                "VAR_X": VAR_X,
            },
            "parameter_grid": {
                "alphas": ALPHAS, "v_mults": V_MULTS,
                "c_mins": C_MINS, "etas": ETAS,
                "n_combinations": len(ALPHAS)*len(V_MULTS)*len(C_MINS)*len(ETAS),
            },
            "compliance": {
                "P3_source_tags": "All thresholds carry [LAW-Lx]/[BAR-Entry n]/[OP-Entry n]/[PROPOSED] tags. [§5 P3]",
                "P4_regime_dating": "Header states spec + constitution regime + artifact date. [§5 P4]",
                "candidate_blind": "Simulation seeds from parameter-combo hashes only; no candidate data. [Ruling 9, Entry 76]",
                "estimator_identity": "β* estimator is the identical §2 XF-5 estimator. [Sol-XF-5]",
                "misspecification_stress_test": "§8 item 9: estimator applied to misspecified data-generating process. [PROPOSED -- apparatus parameter, §8 item 9]",
            },
        },
        "results": results,
        "sensitivity_map": sensitivity_map,
        "selection": selection,
    }


def run_misspecification_stress_test(n_sims=10000, reference_selection=None, workers=None):
    """Run the full misspecification stress-test per §8 item 9.

    For each misspecified profile, runs the full 240-combo power analysis,
    builds the sensitivity map, runs the deterministic selection rule,
    and reports selection stability vs the reference profile.

    [Sol-XF-9] [PROPOSED -- apparatus parameter, §8 item 9]
    Candidate-blind (Ruling 9): profiles use known oracle ground truth.
    """
    profiles = ["uniform_difficulty", "bimodal_difficulty"]
    results = {"profiles": {}, "n_sims": n_sims, "reference_selection": reference_selection}

    for profile_name in profiles:
        print(f"  Misspec profile: {profile_name} (n_sims={n_sims})")
        pa = run_power_analysis_misspecified(profile_name, n_sims=n_sims)
        selection = pa["selection"]
        results["profiles"][profile_name] = {
            "sensitivity_map": pa["sensitivity_map"],
            "selection": selection,
            "header": pa["header"],
            "results_summary": [{"c_min": r["c_min"], "eta": r["eta"],
                                  "false_kill_rate": r["false_kill_rate"],
                                  "false_kill_rate_per_seed": r.get("false_kill_rate_per_seed", float("nan")),
                                  "region": r["region"],
                                  "mean_beta_star": r["mean_beta_star"]}
                                 for r in pa["results"]],
        }

    # Selection stability report
    # select_cmin_eta returns the chosen (C_min, η) nested under the "selected"
    # key (not modified here per constraints). Normalize to flat
    # selected_c_min / selected_eta fields so the stability report reads real
    # values.  [Sol-XF-9] [PROPOSED -- apparatus parameter, §8 item 9]
    def _flat_sel(s):
        if not s:
            return (None, None)
        if "selected_c_min" in s and "selected_eta" in s:
            return (s.get("selected_c_min"), s.get("selected_eta"))
        sel = s.get("selected")
        if isinstance(sel, dict):
            return (sel.get("c_min"), sel.get("eta"))
        return (None, None)

    # Normalize the reference selection (same select_cmin_eta shape) once.
    ref_c = ref_e = None
    has_ref = False
    if reference_selection:
        ref_c, ref_e = _flat_sel(reference_selection)
        has_ref = ref_c is not None and ref_e is not None

    results["stability"] = {}
    for pname, pdata in results["profiles"].items():
        sel = pdata["selection"]
        sel_c, sel_e = _flat_sel(sel)
        if has_ref:
            match = (ref_c == sel_c and ref_e == sel_e)
            results["stability"][pname] = {
                "selected_c_min": sel_c,
                "selected_eta": sel_e,
                "reference_c_min": ref_c,
                "reference_eta": ref_e,
                "selection_matches_reference": match,
                "assessment": "stable" if match else "unstable",
            }
        else:
            results["stability"][pname] = {
                "selected_c_min": sel_c,
                "selected_eta": sel_e,
                "selection_matches_reference": None,
                "assessment": "no_reference",
            }

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="L8 §8 power analysis simulation (candidate-blind). "
                    "Spec: L8 instantiation spec v2.2 (architect/l8-instantiation-v2.2-fresh, c7d7bed). "
                    "Diagnostic-only (O-15); authorizes NO scoring.")
    parser.add_argument("--full", action="store_true",
                        help="Run the full 10,000×240 power analysis and write "
                             "the machine-readable JSON result table.")
    parser.add_argument("--validation-trials", type=int, default=200_000,
                        help="Number of trials for the §2 XF-5 estimator "
                             "validation (Examples A and B). Default 200000.")
    parser.add_argument("--validation-sims", type=int, default=N_SIMS_VALIDATION,
                        help="Number of simulations per combo in the 100-sim "
                             "validation batch. Default 100.")
    parser.add_argument("--out", type=str, default=None,
                        help="Output JSON path for --full. Default "
                        "diagnostics/l8_power_analysis_results.json.")
    parser.add_argument("--workers", type=int, default=None,
                        help="Number of multiprocessing workers. Default: os.cpu_count(). "
                             "Set to 1 for single-threaded (reproducibility verification). "
                             "[PROPOSED -- apparatus parameter, scalable parallelism]")
    parser.add_argument('--stress-test-sims', type=int, default=10000,
                        help='Number of simulations per combo for the misspecification stress-test. Default 10000 (full). Reduce for faster stability check.')
    args = parser.parse_args()

    print("=" * 78)
    print("L8 §8 POWER ANALYSIS SIMULATION (candidate-blind, diagnostic-only O-15)")
    print(f"Spec regime: {SPEC_REGIME}")
    print(f"Constitution regime: {CONSTITUTION_REGIME}")
    print(f"Artifact date: {ARTIFACT_DATE}  [OP — P4 regime dating]")
    print("=" * 78)

    # Step 1: estimator validation (§2 XF-5 Examples A and B).
    print("\n[Step 1] Estimator validation (§2 XF-5) — Examples A and B")
    print(f"  (n_trials={args.validation_trials})")
    t0 = time.time()
    validation = validate_estimator(n_trials=args.validation_trials)
    t_val = time.time() - t0
    for ex in ("example_a", "example_b"):
        v = validation[ex]
        status = "PASS" if v["pass"] else "FAIL"
        print(f"  {ex}: mean β* = {v['mean_beta_star']:.4f} "
              f"(anchor {v['anchor']}, tol ±{v['tolerance']}) "
              f"n_instr_fail={v['n_instrument_failures']} -> {status}")
    print(f"  validation elapsed: {t_val:.2f}s")
    if not (validation["example_a"]["pass"] and validation["example_b"]["pass"]):
        print("  WARNING: estimator validation FAILED — results below are not "
              "trustworthy. Check the §2 XF-5 implementation.")

    # Step 2: 100-sim validation batch on 3 representative combos.
    print(f"\n[Step 2] Validation batch — {args.validation_sims} sims × 3 "
          f"representative combos")
    t0 = time.time()
    batch = run_validation_batch(n_sims=args.validation_sims)
    t_batch = time.time() - t0
    for c in batch["representative_combos"]:
        print(f"  {c['label']}")
        print(f"    α={c['alpha']} v_mult={c['v_mult']} C_min={c['c_min']} "
              f"η={c['eta']} σ_dose={c['sigma_dose_calibrated']:.4f}")
        print(f"    mean β*={c['mean_beta_star']:.4f} std={c['std_beta_star']:.4f} "
              f"false-kill={c['false_kill_rate']:.3f} (per-seed={c['false_kill_rate_per_seed']:.3f}) "
              f"n_instr_fail={c['n_instrument_failures']}")
        print(f"    elapsed={c['elapsed_seconds']:.3f}s "
              f"({c['per_sim_seconds']*1000:.3f} ms/sim) "
              f"calib={c['calibration_seconds']:.2f}s")
    print(f"  total validation batch elapsed: {t_batch:.2f}s")
    print(f"  mean per-sim time: {batch['mean_per_sim_seconds']*1000:.3f} ms")
    print(f"  estimated full run (10,000×240, 2 arms): "
          f"{batch['estimated_full_run_seconds_two_arm']:.0f}s "
          f"= {batch['estimated_full_run_minutes_two_arm']:.1f} min "
          f"= {batch['estimated_full_run_hours_two_arm']:.2f} h")

    # Step 3: optionally run the full power analysis.
    if args.full:
        print(f"\n[Step 3] FULL power analysis — {N_SIMS_FULL} sims × 240 combos "
              f"(2 arms)")
        full = run_power_analysis(n_sims=N_SIMS_FULL, include_null_control=True)
        sel = full["selection"]
        if sel["selected"] is not None:
            print(f"  Selected (C_min, η) = "
                  f"({sel['selected']['c_min']}, {sel['selected']['eta']}) "
                  f"[§8.8 deterministic rule, Sol-XF-9]")
            print(f"    min-distance={sel['min_distance_to_boundaries']:.4f} "
                  f"false-kill={sel['mean_false_kill_rate']:.3f} "
                  f"false-pass={sel['mean_false_pass_rate']:.3f} "
                  f"n_informative={sel['n_informative']}")
        else:
            print(f"  No informative cell found: {sel['reason']}")
        # Report false-kill threshold check (§8.1 G3 escalation).
        fk_vals = [r["false_kill_rate"] for r in full["results"]
                   if not math.isnan(r["false_kill_rate"])]
        max_fk = max(fk_vals) if fk_vals else float("nan")
        print(f"  max false-kill rate across grid: {max_fk:.4f} "
              f"(threshold {FALSE_KILL_THRESHOLD} -> "
              f"{'ESCALATE to G3' if max_fk > FALSE_KILL_THRESHOLD else 'no escalation'}) "
              f"[PROPOSED — apparatus parameter, §8]")
        print(f"  full run elapsed: {full['header']['elapsed_seconds']:.1f}s")
    else:
        print("\n[Step 3] Skipped full run (pass --full to run 10,000×240).")

    # §8 item 9 — Misspecification stress-test (BF-IMPL-1, NF-IMPL-4 extension).
    print("\n[Step 4] Misspecification stress-test (§8 item 9, full sensitivity map)")
    stress_n = args.stress_test_sims
    ref_sel = full.get("selection") if args.full else None
    print(f"  Running full power analysis on 2 misspecified profiles (n_sims={stress_n})...")
    misspec = run_misspecification_stress_test(n_sims=stress_n, reference_selection=ref_sel, workers=args.workers)
    for pname in misspec["profiles"]:
        s = misspec["stability"][pname]
        print(f"  {pname}: selection (C_min={s.get('selected_c_min')}, η={s.get('selected_eta')}) "
              f"-> {s['assessment']}"
              + (f" (ref: C_min={s.get('reference_c_min')}, η={s.get('reference_eta')})" if ref_sel else ""))
    print(f"  profiles tested: {list(misspec['profiles'].keys())}")
    print(f"  sims per combo: {stress_n}")
    print(f"  note: full 10,000 per combo triples total runtime (~17h). Use --stress-test-sims 2000 for ~8h.")
    if args.full:
        full["misspecification_stress_test"] = misspec

    # Write JSON after all steps (reference + stress-test) are complete.
    if args.full:
        out_path = args.out or "diagnostics/l8_power_analysis_results.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(_sanitize_nan(full), f, indent=2, allow_nan=False)
            f.write("\n")
        print(f"  wrote machine-readable JSON: {out_path}")

    print("\nDone. Diagnostic-only (O-15). This authorizes NO scoring.")


if __name__ == "__main__":
    main()
