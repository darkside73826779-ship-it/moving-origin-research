"""O-15 candidate-blind L8 minimal full-screen diagnostic (Regime B, 2026-08-20).

Implements the direct per-seed rho predicate authorized in the minimal
full-screen specification. It does not expose scoring or protected-seed modes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import os
import tempfile
import time
from pathlib import Path
from typing import Any

import numpy as np

import l8_power_analysis as pa

RHO_BAR = 0.8  # [BAR-Entry 11]
BETA_STAR_BAR = 0.2  # [BAR-Entry 11]
RHO_COMPARE_EPS = 1e-12  # [PROPOSED — Rebecca directive]
FALSE_KILL_THRESHOLD = 0.10  # [PROPOSED — apparatus parameter]
N_SIMS = 2000  # [PROPOSED — authorized diagnostic workload]
N_WORKERS = 16  # [PROPOSED — authorized diagnostic workload]
CODE_SHA = "b1397498ca369067e956479e6c2bd6b0793c3e89"
REFERENCE_SHA = "6d455bb878f4b52a5b5564afac38d6fb3a20d4b3"


def rho_from_dose_means(values: np.ndarray) -> float | None:
    """Pearson(dose ranks, ascending response midranks), §5.1."""
    values = np.asarray(values, dtype=np.float64)
    if values.shape != (4,) or not np.isfinite(values).all():
        return None
    order = np.argsort(values, kind="stable")
    ranks = np.empty(4, dtype=np.float64)
    start = 0
    while start < 4:
        end = start + 1
        while end < 4 and values[order[end]] == values[order[start]]:
            end += 1
        ranks[order[start:end]] = ((start + 1) + end) / 2.0
        start = end
    doses = np.array([1.0, 2.0, 3.0, 4.0])
    dx, dy = doses - doses.mean(), ranks - ranks.mean()
    denominator = math.sqrt(float(np.mean(dx * dx)) * float(np.mean(dy * dy)))
    if denominator == 0.0:
        return None
    return float(np.mean(dx * dy) / denominator)


def rho_pass(rho: float | None) -> bool:
    return rho is not None and (rho >= RHO_BAR or abs(rho - RHO_BAR) <= RHO_COMPARE_EPS)


def complete_pass(seed_stats: list[tuple[float | None, float | None]]) -> bool:
    return all(beta is not None and beta >= BETA_STAR_BAR and rho_pass(rho)
               for beta, rho in seed_stats)


def _configure_geometry(W: int, N_w: int) -> None:
    pa.W = W
    pa.N_W = N_w


def _worker_cell(args: tuple[Any, ...]) -> dict[str, Any]:
    geometry_index, W, N_w, alpha, v_mult, c_min, eta, sigma_dose, null_arm = args
    _configure_geometry(W, N_w)
    base_seed = pa.combo_seed(alpha, v_mult, c_min, eta)
    n_instr = 0
    complete_false_kills = beta_any_false_kills = mean_false_kills = null_passes = 0
    mean_betas: list[float] = []
    for i in range(N_SIMS):
        seed_stats: list[tuple[float | None, float | None]] = []
        d_all = np.empty((pa.N_SEEDS, pa.L_DOSES, N_w), dtype=np.float64)
        for s in range(pa.N_SEEDS):
            rng = np.random.default_rng((base_seed + i * pa.N_SEEDS + s) % (2 ** 31))
            d_all[s] = pa.simulate_one_seed(rng, alpha, v_mult * pa.V_REF, sigma_dose, c_min, eta)
        per_seed_betas: list[float] = []
        apparatus_failure = False
        for s in range(pa.N_SEEDS):
            beta_star, failed = pa.beta_star_for_seed(d_all[s])
            if failed:
                apparatus_failure = True
                seed_stats.append((None, rho_from_dose_means(d_all[s].mean(axis=1))))
            else:
                beta = float(beta_star)
                per_seed_betas.append(beta)
                seed_stats.append((beta, rho_from_dose_means(d_all[s].mean(axis=1))))
        if apparatus_failure:
            n_instr += 1
            continue
        run_mean = float(np.mean(per_seed_betas))
        mean_betas.append(run_mean)
        any_beta_fail = any(beta < BETA_STAR_BAR for beta, _ in seed_stats)
        if null_arm:
            if complete_pass(seed_stats):
                null_passes += 1
        else:
            if not complete_pass(seed_stats):
                complete_false_kills += 1
            if any_beta_fail:
                beta_any_false_kills += 1
            if run_mean < BETA_STAR_BAR:
                mean_false_kills += 1
    valid = N_SIMS - n_instr
    def rate(value: int) -> float | None:
        return value / valid if valid else None
    return {"geometry_index": geometry_index, "W": W, "N_w": N_w, "alpha": alpha,
            "v_mult": v_mult, "c_min": c_min, "eta": eta, "base_seed": base_seed,
            "null_arm": null_arm, "n_attempted": N_SIMS, "n_valid": valid,
            "n_apparatus_invalid": 0, "n_instrument_failures": n_instr,
            "complete_rate": rate(complete_false_kills), "beta_any_rate": rate(beta_any_false_kills),
            "mean_rate": rate(mean_false_kills), "null_pass_rate": rate(null_passes),
            "mean_beta": float(np.mean(mean_betas)) if mean_betas else None}


def geometry_order() -> list[tuple[int, int]]:
    pairs = [(w, n) for w in [50, 100, 200, 400] for n in [4, 8, 16, 32, 64]]
    return sorted(pairs, key=lambda x: (x[0] * x[1], -x[1], x[0]))


def cells() -> list[tuple[float, float, float, float]]:
    return [(a, v, c, e) for a in pa.ALPHAS for v in pa.V_MULTS
            for c in pa.C_MINS for e in pa.ETAS]


def calibrations_for_geometry(W: int, N_w: int) -> dict[tuple[float, float], float]:
    # Baseline calculation is retained unchanged. [OP — Sol-XF-5]
    _configure_geometry(W, N_w)
    return {(a, v): pa.calibrate_sigma_dose(a, v) for a in pa.ALPHAS for v in pa.V_MULTS}


def run_geometry(index: int, W: int, N_w: int) -> dict[str, Any]:
    calibration = calibrations_for_geometry(W, N_w)
    work = []
    for alpha, v_mult, c_min, eta in cells():
        sigma = calibration[(alpha, v_mult)]
        work.append((index, W, N_w, alpha, v_mult, c_min, eta, sigma, False))
        work.append((index, W, N_w, alpha, v_mult, c_min, eta, 0.0, True))
    with mp.Pool(processes=N_WORKERS) as pool:
        results = pool.map(_worker_cell, work, chunksize=1)
    combos = [r for r in results if not r["null_arm"]]
    nulls = [r for r in results if r["null_arm"]]
    out_cells = []
    for combo, null in zip(combos, nulls):
        cell_invalid = combo["n_apparatus_invalid"] > 0 or null["n_apparatus_invalid"] > 0
        out_cells.append({"geometry_index": index, "W": W, "N_w": N_w, "alpha": combo["alpha"],
            "v_mult": combo["v_mult"], "c_min": combo["c_min"], "eta": combo["eta"],
            "base_seed": combo["base_seed"], "cell_apparatus_invalid": cell_invalid,
            "n_sims_attempted_true_effect": N_SIMS, "n_valid_true_effect": combo["n_valid"],
            "n_apparatus_invalid_true_effect": combo["n_apparatus_invalid"],
            "n_instrument_failures_true_effect": combo["n_instrument_failures"],
            "n_sims_attempted_null_control": N_SIMS, "n_valid_null_control": null["n_valid"],
            "n_apparatus_invalid_null_control": null["n_apparatus_invalid"],
            "n_instrument_failures_null_control": null["n_instrument_failures"],
            "complete_verdict_false_kill_rate": combo["complete_rate"],
            "diagnostic_beta_only_any_seed_false_kill_rate": combo["beta_any_rate"],
            "diagnostic_five_seed_mean_false_kill_rate": combo["mean_rate"],
            "null_control_false_pass_rate": null["null_pass_rate"], "mean_beta_star": combo["mean_beta"],
            "mean_beta_star_null": null["mean_beta"]})
    invalid = any(c["cell_apparatus_invalid"] for c in out_cells)
    eligible = [c["complete_verdict_false_kill_rate"] for c in out_cells if not c["cell_apparatus_invalid"]]
    maximum = max(eligible) if eligible else None
    boundary = W in (50, 400) or N_w in (4, 64)
    return {"geometry_index": index, "W": W, "N_w": N_w, "Q_per_dose": W*N_w,
            "queries_per_five_seed_run": W*N_w*4*5, "max_primary_false_kill": maximum,
            "has_apparatus_invalid_cell": invalid,
            "meets_target": (not invalid and maximum is not None and maximum <= FALSE_KILL_THRESHOLD),
            "on_tested_boundary": boundary, "cells": out_cells}


def sanitize(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value): return None
    if isinstance(value, dict): return {k: sanitize(v) for k, v in value.items()}
    if isinstance(value, list): return [sanitize(v) for v in value]
    return value


def atomic_json(path: Path, value: dict[str, Any]) -> str:
    data = (json.dumps(sanitize(value), indent=2, allow_nan=False) + "\n").encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name+".", suffix=".tmp", delete=False) as handle:
        handle.write(data); handle.flush(); os.fsync(handle.fileno()); temp = Path(handle.name)
    os.replace(temp, path)
    return digest


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    geometries = [run_geometry(i, W, N_w) for i, (W, N_w) in enumerate(geometry_order())]
    first = next((g for g in geometries if g["meets_target"]), None)
    selection = {"false_kill_target": FALSE_KILL_THRESHOLD, "primary_metric": "complete_verdict_false_kill_rate",
        "diagnostic_metrics": ["diagnostic_beta_only_any_seed_false_kill_rate", "diagnostic_five_seed_mean_false_kill_rate"],
        "minimum_geometry_satisfying_target": None if first is None else {k:first[k] for k in ("geometry_index","W","N_w","Q_per_dose")},
        "first_passing_on_tested_boundary": None if first is None else first["on_tested_boundary"],
        "rule": "first geometry in §3 Q-ordering whose max_primary_false_kill <= 0.10; null if none (STOP); if first passing geometry is on a tested boundary, STOP and escalate (§5.4)",
        "scoring_verdict_alignment_note": "primary is the complete frozen-v2.2 any-seed scoring-verdict false-kill rate (β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8); frozen-v2.2 bars only; no pooled-bootstrap predicate; see §5.1-§5.3"}
    result = {"header": {"schema_version":"l8-g2g4-minimal-fullscreen-v1", "artifact_date":"2026-08-20", "regime":"B",
        "spec_regime":"L8 v2.2 (c7d7bed) + minimal full-screen spec (2082680)", "code_baseline_sha":CODE_SHA,
        "reference_artifact_sha":REFERENCE_SHA, "constants":{"W_set":[50,100,200,400],"N_w_set":[4,8,16,32,64],"alphas":pa.ALPHAS,"v_mults":pa.V_MULTS,"c_mins":pa.C_MINS,"etas":pa.ETAS,"N_SEEDS":5,"L_DOSES":4,"R_STAR":pa.R_STAR,"TRUE_BETA_STAR":pa.TRUE_BETA_STAR,"BETA_STAR_BAR":BETA_STAR_BAR,"RHO_BAR":RHO_BAR,"RHO_COMPARE_EPS":RHO_COMPARE_EPS,"FALSE_KILL_THRESHOLD":FALSE_KILL_THRESHOLD,"V_REF":pa.V_REF,"CAL_REF_C_MIN":pa.CAL_REF_C_MIN,"CAL_REF_ETA":pa.CAL_REF_ETA},
        "run_config":{"n_geometries":20,"n_cells_per_geometry":240,"n_sims_per_cell_per_arm":N_SIMS,"arms":["combo","null_control"],"n_workers":N_WORKERS,"pool":"multiprocessing.Pool","chunksize":1},"compliance":{"P3_source_tags":"all thresholds tagged","P4_regime_dating":"header states date and regime","candidate_blind":"seeds from parameter-combo hashes only; no candidate data","O_15":"diagnostic-only; authorizes no scoring"}},"geometries":geometries,"selection":selection}
    digest = atomic_json(output, result)
    result["_artifact_sha256"] = digest
    result["_elapsed_seconds"] = time.perf_counter()-started
    return result


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,default=Path("diagnostics/l8_g2g4_minimal_full_screen.json")); args=parser.parse_args()
    run(args.output)

if __name__ == "__main__": main()
