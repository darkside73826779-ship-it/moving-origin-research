"""Legacy L8 CPU-reference compatibility adapter (2026-08-21, Regime B).

This module changes no legacy scientific rule.  It maps the committed
``l8_power_analysis.py`` primitive-tape and estimator identity to the CUDA
evaluator while preserving RNG order, alpha bias, and float64 arithmetic.
Diagnostic-only; candidate-blind parameter-derived seeds only.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

import l8_gpu_adoption as gpu
import l8_power_analysis as cpu


def make_legacy_tape(task: tuple[Any, ...]) -> dict[str, Any]:
    """Construct the legacy primitive tape without changing RNG draw order."""
    (cell_ordinal, arm_ordinal, start, count, alpha, v_mult, c_min, eta,
     sigma_dose) = task
    arm = ("combo", "null_control")[arm_ordinal]
    base_seed = cpu.combo_seed(alpha, v_mult, c_min, eta)
    shape = (count, cpu.N_SEEDS, cpu.L_DOSES, cpu.N_W, cpu.W)
    arrays = [np.empty(shape, dtype=dtype)
              for dtype in (np.float64, np.bool_, np.float64, np.float64)]
    for local, repetition in enumerate(range(start, start + count)):
        for seed_index in range(cpu.N_SEEDS):
            seed_int = (base_seed + repetition * cpu.N_SEEDS + seed_index) % (2 ** 31)
            rng = np.random.default_rng(seed_int)
            for dose in range(cpu.L_DOSES):
                for window in range(cpu.N_W):
                    p = np.clip(rng.beta(cpu.BETA_A, cpu.BETA_B, size=cpu.W),
                                cpu.EPS_C, 1.0 - cpu.EPS_C)
                    arrays[0][local, seed_index, dose, window] = p
                    arrays[1][local, seed_index, dose, window] = rng.random(cpu.W) < p
                    arrays[2][local, seed_index, dose, window] = rng.normal(
                        0.0, math.sqrt(v_mult * cpu.V_REF), size=cpu.W)
                    arrays[3][local, seed_index, dose, window] = 0.0
                    if arm == "combo" and dose > 0 and sigma_dose > 0.0:
                        arrays[3][local, seed_index, dose, window] = rng.normal(
                            0.0, dose * sigma_dose, size=cpu.W)
    return {
        "identity": (cell_ordinal, arm_ordinal, start),
        "start": start,
        "count": count,
        "W": cpu.W,
        "N_w": cpu.N_W,
        "alpha": alpha,
        "alpha_bias": alpha,
        "v_mult": v_mult,
        "c_min": c_min,
        "eta": eta,
        "sigma": sigma_dose,
        "arm": arm,
        "p_true": arrays[0],
        "correct": arrays[1],
        "xi": arrays[2],
        "xi_l": arrays[3],
    }


def evaluate_legacy_tape_cpu(tape: dict[str, Any]) -> dict[str, Any]:
    d_seed = np.empty((tape["count"], cpu.N_SEEDS, cpu.L_DOSES, cpu.N_W),
                      dtype=np.float64)
    beta = np.empty((tape["count"], cpu.N_SEEDS), dtype=np.float64)
    invalid = np.zeros_like(beta, dtype=np.bool_)
    for repetition in range(tape["count"]):
        for seed in range(cpu.N_SEEDS):
            p = tape["p_true"][repetition, seed]
            correct = tape["correct"][repetition, seed]
            xi = tape["xi"][repetition, seed]
            xi_l = tape["xi_l"][repetition, seed]
            d = np.empty((cpu.L_DOSES, cpu.N_W), dtype=np.float64)
            for dose in range(cpu.L_DOSES):
                tau = float(cpu.TAU_INIT)
                for window in range(cpu.N_W):
                    c = np.clip(cpu.sigmoid(cpu.logit(p[dose, window]) +
                                            tape["alpha_bias"] + xi[dose, window]),
                                cpu.EPS_C, 1.0 - cpu.EPS_C)
                    cp = np.clip(cpu.sigmoid(cpu.logit(c) + xi_l[dose, window]),
                                 cpu.EPS_C, 1.0 - cpu.EPS_C)
                    selected = gpu.coverage_indices(cp, tape["c_min"], tau)
                    risk = float(np.count_nonzero(~correct[dose, window, selected]) /
                                 selected.size)
                    d[dose, window] = risk - cpu.R_STAR
                    tau = float(np.clip(tau + tape["eta"] * (risk - cpu.R_STAR),
                                        cpu.TAU_MIN, cpu.TAU_MAX))
            d_seed[repetition, seed] = d
            value, failed = cpu.beta_star_for_seed(d)
            beta[repetition, seed] = np.nan if failed else value
            invalid[repetition, seed] = failed or not np.isfinite(d).all()
    return {"d_seed": d_seed, "beta": beta, "invalid": invalid}


def evaluate_legacy_tape_gpu(tape: dict[str, Any]) -> dict[str, Any]:
    result = gpu.evaluate_tape_gpu(tape)
    return {"d_seed": result["d_seed"], "beta": result["beta"],
            "invalid": result["invalid"]}
