"""O-15 GPU reproduction of the completed CPU L8 power-analysis workload.

Date: 2026-08-20. Regime B. Candidate-blind synthetic diagnostics only.
The CPU implementation is controlling; CUDA changes execution and RNG stream,
not equations, grids, repetition counts, controls, or aggregation.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import torch

import l8_gpu_proposal as gpu
import l8_power_analysis as cpu


def _cell(cell: gpu.GpuCell, repetitions: int, seed: int, profile: str | None) -> dict:
    simulate = gpu.simulate_batch if profile is None else gpu.simulate_misspecified_batch
    if profile is None:
        per_seed, _ = simulate(cell, repetitions, seed)
    else:
        per_seed, _ = simulate(cell, repetitions, seed, profile)
    failed = ~torch.isfinite(per_seed).all(dim=1)
    run_mean = per_seed.mean(dim=1)
    valid = run_mean[~failed]
    valid_per_seed = per_seed[~failed]
    n_valid = int(valid.numel())
    return {
        "n_valid": n_valid,
        "n_instrument_failures": int(failed.sum().cpu()),
        "mean_beta_star": float(valid.mean().cpu()) if n_valid else float("nan"),
        "std_beta_star": float(valid.std(unbiased=False).cpu()) if n_valid else float("nan"),
        "false_kill_rate": float((valid < cpu.BETA_STAR_BAR).double().mean().cpu()) if n_valid else float("nan"),
        "false_kill_rate_per_seed": float((valid_per_seed < cpu.BETA_STAR_BAR).any(dim=1).double().mean().cpu()) if n_valid else float("nan"),
        "false_pass_rate": float((valid >= cpu.BETA_STAR_BAR).double().mean().cpu()) if n_valid else float("nan"),
    }


def calibrations(pilots: int) -> dict[tuple[float, float], float]:
    values = {}
    for alpha in cpu.ALPHAS:
        for v_mult in cpu.V_MULTS:
            seed = cpu.combo_seed(alpha, v_mult, cpu.CAL_REF_C_MIN, cpu.CAL_REF_ETA)
            cell = gpu.GpuCell(cpu.W, cpu.N_W, alpha, v_mult, cpu.CAL_REF_C_MIN, cpu.CAL_REF_ETA, 0.0)
            values[(alpha, v_mult)] = gpu.calibrate(cell, seed=seed, pilots=pilots)
            print(f"calibration {len(values)}/15 alpha={alpha} v_mult={v_mult} sigma={values[(alpha, v_mult)]:.8f}", flush=True)
    return values


def run_grid(repetitions: int, calibration: dict, profile: str | None) -> dict:
    started = time.time()
    results = []
    label = profile or "reference"
    for alpha in cpu.ALPHAS:
        for v_mult in cpu.V_MULTS:
            sigma = calibration[(alpha, v_mult)]
            for c_min in cpu.C_MINS:
                for eta in cpu.ETAS:
                    seed = cpu.combo_seed(alpha, v_mult, c_min, eta)
                    effect_cell = gpu.GpuCell(cpu.W, cpu.N_W, alpha, v_mult, c_min, eta, sigma)
                    null_cell = gpu.GpuCell(cpu.W, cpu.N_W, alpha, v_mult, c_min, eta, 0.0)
                    effect = _cell(effect_cell, repetitions, seed, profile)
                    null = _cell(null_cell, repetitions, seed, profile)
                    fk, fp = effect["false_kill_rate"], null["false_pass_rate"]
                    region = (cpu.classify_region(fk, fp)
                              if math.isfinite(fk) and math.isfinite(fp)
                              else "undefined")
                    distance = cpu.min_distance_to_boundaries(fk, fp) if region == "informative" else float("nan")
                    results.append({
                        "alpha": alpha, "v_mult": v_mult, "v_logit": v_mult * cpu.V_REF,
                        "c_min": c_min, "eta": eta, "sigma_dose_calibrated": sigma,
                        "n_sims": repetitions, "n_valid": effect["n_valid"],
                        "n_instrument_failures": effect["n_instrument_failures"],
                        "n_instrument_failures_null": null["n_instrument_failures"],
                        "mean_beta_star": effect["mean_beta_star"],
                        "std_beta_star": effect["std_beta_star"],
                        "false_kill_rate": fk,
                        "false_kill_rate_per_seed": effect["false_kill_rate_per_seed"],
                        "false_pass_rate": fp,
                        "mean_beta_star_null": null["mean_beta_star"],
                        "region": region, "min_distance_to_boundaries": distance,
                        "base_seed": seed,
                    })
                    if len(results) % 10 == 0 or len(results) == 240:
                        torch.cuda.synchronize()
                        print(f"{label} cells={len(results)}/240 elapsed={time.time()-started:.1f}s", flush=True)

    cells = []
    for c_min in cpu.C_MINS:
        for eta in cpu.ETAS:
            rows = [r for r in results
                    if r["c_min"] == c_min and r["eta"] == eta
                    and math.isfinite(r["false_kill_rate"])
                    and math.isfinite(r["false_pass_rate"])]
            if not rows:
                continue
            fk = float(np.mean([r["false_kill_rate"] for r in rows]))
            fp = float(np.mean([r["false_pass_rate"] for r in rows]))
            region = cpu.classify_region(fk, fp)
            cells.append({
                "c_min": c_min, "eta": eta, "mean_false_kill_rate": fk,
                "mean_false_pass_rate": fp, "region": region,
                "min_distance_to_boundaries": cpu.min_distance_to_boundaries(fk, fp) if region == "informative" else float("nan"),
                "n_av_pairs": len(rows),
            })
    sensitivity = {
        "description": "§8.7 sensitivity map over (C_min, η), aggregated across (α, v) pairs  [Sol-XF-9]",
        "boundaries": {"abstention_escape_false_kill_ge": cpu.FK_BOUNDARY,
                       "trivial_pass_false_pass_ge": cpu.FP_BOUNDARY},
        "cells": cells,
    }
    return {"results": results, "sensitivity_map": sensitivity,
            "selection": cpu.select_cmin_eta(sensitivity),
            "elapsed_seconds": time.time() - started}


def run(output: Path, reference_sims: int, stress_sims: int, pilots: int) -> dict:
    started = time.time()
    calibration = calibrations(pilots)
    print("calibration complete", flush=True)
    reference = run_grid(reference_sims, calibration, None)
    result = {
        "header": {
            "spec_regime": cpu.SPEC_REGIME, "constitution_regime": cpu.CONSTITUTION_REGIME,
            "artifact_date": "2026-08-20", "mode": "O-15 diagnostic-only",
            "backend": "PyTorch CUDA float64", "rng": "torch CUDA generator",
            "n_sims_per_combo": reference_sims, "stress_sims_per_combo": stress_sims,
            "calibration_pilots": pilots, "n_combos": len(reference["results"]),
            "reference_elapsed_seconds": reference["elapsed_seconds"],
            "constants": {"W": cpu.W, "N_W": cpu.N_W, "L_DOSES": cpu.L_DOSES,
                          "N_SEEDS": cpu.N_SEEDS, "R_STAR": cpu.R_STAR,
                          "BETA_STAR_BAR": cpu.BETA_STAR_BAR},
        },
        "results": reference["results"], "sensitivity_map": reference["sensitivity_map"],
        "selection": reference["selection"], "misspecification_stress_test": {
            "profiles": {}, "n_sims": stress_sims, "reference_selection": reference["selection"],
            "stability": {},
        },
    }
    reference_selected = reference["selection"].get("selected")
    for profile in ("uniform_difficulty", "bimodal_difficulty"):
        profile_result = run_grid(stress_sims, calibration, profile)
        result["misspecification_stress_test"]["profiles"][profile] = profile_result
        selected = profile_result["selection"].get("selected")
        matches = selected == reference_selected
        result["misspecification_stress_test"]["stability"][profile] = {
            "selected_c_min": selected.get("c_min") if selected else None,
            "selected_eta": selected.get("eta") if selected else None,
            "reference_c_min": reference_selected.get("c_min") if reference_selected else None,
            "reference_eta": reference_selected.get("eta") if reference_selected else None,
            "selection_matches_reference": matches,
            "assessment": "stable" if matches else "unstable",
        }
    result["header"]["elapsed_seconds"] = time.time() - started
    output.write_text(json.dumps(cpu._sanitize_nan(result), indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("diagnostics/l8_gpu_full_comparison_results.json"))
    parser.add_argument("--reference-sims", type=int, default=cpu.N_SIMS_FULL)
    parser.add_argument("--stress-sims", type=int, default=2000)
    parser.add_argument("--calibration-pilots", type=int, default=cpu.CAL_PILOT_SIMS)
    args = parser.parse_args()
    run(args.output, args.reference_sims, args.stress_sims, args.calibration_pilots)


if __name__ == "__main__":
    main()
