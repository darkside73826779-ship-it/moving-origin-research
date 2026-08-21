"""Native-CUDA legacy L8 prototype (2026-08-21, Regime B).

Diagnostic-only prototype. Random inputs and scientific evaluation are created
on CUDA. The committed CPU artifact supplies only calibration values and the
comparison oracle. This artifact does not establish formal equivalence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import time
from collections import OrderedDict
from pathlib import Path

import numpy as np
import torch

import l8_power_analysis as cpu


def native_seed(alpha: float, v_mult: float, c_min: float, eta: float,
                arm: str) -> int:
    identity = (f"l8-native-cuda-v1|alpha={alpha:.6f}|vmult={v_mult:.6f}|"
                f"cmin={c_min:.6f}|eta={eta:.6f}|arm={arm}")
    return int.from_bytes(hashlib.sha256(identity.encode("ascii")).digest()[:8],
                          "little") & ((1 << 63) - 1)


def load_cpu_reference(revision: str) -> dict:
    raw = subprocess.run(
        ["git", "show", f"{revision}:diagnostics/l8_power_analysis_results.json"],
        check=True, stdout=subprocess.PIPE).stdout
    return json.loads(raw)


def _gamma(shape: tuple[int, ...], concentration: float,
           generator: torch.Generator, device: str) -> torch.Tensor:
    parameter = torch.full(shape, concentration, dtype=torch.float64,
                           device=device)
    return torch._standard_gamma(parameter, generator=generator)


def run_arm(alpha: float, v_mult: float, c_min: float, eta: float,
            sigma_dose: float, n_sims: int, arm: str,
            device: str = "cuda") -> dict:
    generator = torch.Generator(device=device)
    generator.manual_seed(native_seed(alpha, v_mult, c_min, eta, arm))
    shape = (n_sims, cpu.N_SEEDS, cpu.W)
    d = torch.empty((n_sims, cpu.N_SEEDS, cpu.L_DOSES, cpu.N_W),
                    dtype=torch.float64, device=device)
    for dose in range(cpu.L_DOSES):
        tau = torch.full((n_sims, cpu.N_SEEDS), cpu.TAU_INIT,
                         dtype=torch.float64, device=device)
        for window in range(cpu.N_W):
            gx = _gamma(shape, cpu.BETA_A, generator, device)
            gy = _gamma(shape, cpu.BETA_B, generator, device)
            p = (gx / (gx + gy)).clamp(cpu.EPS_C, 1.0 - cpu.EPS_C)
            correct = torch.rand(shape, dtype=torch.float64, device=device,
                                 generator=generator) < p
            xi = torch.randn(shape, dtype=torch.float64, device=device,
                             generator=generator) * math.sqrt(v_mult * cpu.V_REF)
            p_logit = torch.log(p) - torch.log1p(-p)
            c_logit = p_logit + alpha + xi
            if arm == "combo" and dose > 0 and sigma_dose > 0.0:
                c_logit = c_logit + torch.randn(
                    shape, dtype=torch.float64, device=device,
                    generator=generator) * (dose * sigma_dose)
            order = torch.argsort(c_logit, dim=-1, descending=True, stable=True)
            floor = max(1, math.ceil(c_min * cpu.W))
            rank = torch.empty_like(order)
            ordinal = torch.arange(cpu.W, device=device).expand_as(order)
            rank.scatter_(-1, order, ordinal)
            tau_logit = torch.log(tau) - torch.log1p(-tau)
            mask = (rank < floor) | (c_logit > tau_logit.unsqueeze(-1))
            answered = mask.sum(-1)
            incorrect = ((~correct) & mask).sum(-1)
            risk = incorrect.to(torch.float64) / answered.to(torch.float64)
            d[:, :, dose, window] = risk - cpu.R_STAR
            tau = (tau + eta * (risk - cpu.R_STAR)).clamp(cpu.TAU_MIN,
                                                           cpu.TAU_MAX)
    means = d.mean(-1)
    x = torch.tensor([0.0, 1.0, 2.0, 3.0], dtype=torch.float64, device=device)
    cov = ((means - means.mean(-1, keepdim=True)) * (x - x.mean())).mean(-1)
    beta = cov / cpu.VAR_X
    residual = d - means.unsqueeze(-1)
    sigma = torch.sqrt((residual ** 2).sum((-1, -2)) /
                       (cpu.L_DOSES * (cpu.N_W - 1)))
    invalid_seed = (sigma == 0.0) | (~torch.isfinite(d).all((-1, -2)))
    beta_seed = beta / sigma
    invalid_run = invalid_seed.any(-1)
    beta_run = beta_seed.mean(-1)
    valid = ~invalid_run
    valid_run = beta_run[valid]
    valid_seed = beta_seed[valid]
    torch.cuda.synchronize()
    return {
        "n_valid": int(valid.sum().item()),
        "n_instrument_failures": int(invalid_run.sum().item()),
        "mean_beta_star": float(valid_run.mean().item()),
        "std_beta_star": float(valid_run.std(unbiased=False).item()),
        "predicate_rate": float((valid_run < cpu.BETA_STAR_BAR).to(torch.float64).mean().item()),
        "per_seed_predicate_rate": float(
            (valid_seed < cpu.BETA_STAR_BAR).any(-1).to(torch.float64).mean().item()),
    }


def run_once(reference: dict, n_sims: int) -> dict:
    rows = []
    started = time.perf_counter()
    for ordinal, expected in enumerate(reference["results"]):
        alpha = expected["alpha"]
        v_mult = expected["v_mult"]
        c_min = expected["c_min"]
        eta = expected["eta"]
        sigma = expected["sigma_dose_calibrated"]
        combo = run_arm(alpha, v_mult, c_min, eta, sigma, n_sims, "combo")
        null = run_arm(alpha, v_mult, c_min, eta, 0.0, n_sims, "null_control")
        rows.append(OrderedDict(
            ordinal=ordinal, alpha=alpha, v_mult=v_mult, c_min=c_min, eta=eta,
            sigma_dose_calibrated=sigma, n_sims=n_sims,
            n_valid=combo["n_valid"],
            n_instrument_failures=combo["n_instrument_failures"],
            n_instrument_failures_null=null["n_instrument_failures"],
            mean_beta_star=combo["mean_beta_star"],
            std_beta_star=combo["std_beta_star"],
            false_kill_rate=combo["predicate_rate"],
            false_kill_rate_per_seed=combo["per_seed_predicate_rate"],
            false_pass_rate=float(1.0 - null["predicate_rate"]),
            mean_beta_star_null=null["mean_beta_star"],
            cpu_10000_false_kill_rate=expected["false_kill_rate"],
            cpu_10000_false_kill_rate_per_seed=expected["false_kill_rate_per_seed"],
            cpu_10000_false_pass_rate=expected["false_pass_rate"],
        ))
    return {"elapsed_seconds": time.perf_counter() - started, "rows": rows}


def canonical_payload(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":"), sort_keys=True).encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu-reference-revision", default="6d455bb")
    parser.add_argument("--n-sims", type=int, default=1000)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--output", type=Path,
                        default=Path("diagnostics/l8_native_cuda_1000_prototype.json"))
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise SystemExit("CUDA unavailable")
    reference = load_cpu_reference(args.cpu_reference_revision)
    runs = [run_once(reference, args.n_sims) for _ in range(args.repeats)]
    scientific = [canonical_payload(run["rows"]) for run in runs]
    result = OrderedDict(
        date="2026-08-21", regime="B", diagnostic_only=True,
        cpu_reference_revision=args.cpu_reference_revision,
        cpu_reference_sha256="978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21",
        rng="torch CUDA Philox (native prototype)",
        gpu=torch.cuda.get_device_name(0), n_sims=args.n_sims,
        repeats=args.repeats,
        repeat_payloads_equal=all(raw == scientific[0] for raw in scientific[1:]),
        runs=runs)
    raw = canonical_payload(result)
    args.output.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    args.output.with_name(args.output.name + ".sha256").write_text(
        f"{digest}  {args.output.name}\n", encoding="ascii", newline="\n")
    print(json.dumps({"output": str(args.output), "sha256": digest,
                      "repeat_payloads_equal": result["repeat_payloads_equal"],
                      "elapsed_seconds": [run["elapsed_seconds"] for run in runs]}))


if __name__ == "__main__":
    main()
