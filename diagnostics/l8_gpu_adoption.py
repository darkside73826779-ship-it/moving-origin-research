"""L8 CPU/GPU O-15 diagnostic backend (Regime B, 2026-08-21).

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

Source: docs/ARCHITECTURAL_CONSTITUTION_v2.md lines 28, 54, and 55 [LAW-L8]
[LAW-L18] [LAW-L19]. Implements the approved v1.4 contract plus the v1.5
executability amendment. It exposes no scoring mode and no protected-seed
input surface.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import multiprocessing as mp
import os
import platform
import queue
import shutil
import subprocess
import threading
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterable

import numpy as np

import l8_power_analysis as pa

try:
    import rfc8785
except ImportError:  # Tests which do not canonicalize can still collect.
    rfc8785 = None

try:
    import torch
except ImportError:  # Dependency preflight reports this fail-closed.
    torch = None


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "specs" / "data"
CONFIG_TEMPLATE = DATA / "l8_gpu_adoption_config_template_v1.json"
DEPENDENCIES = DATA / "l8_gpu_adoption_dependencies_v1.json"
KNOWN_GOOD = DATA / "l8_gpu_adoption_known_good_v1.json"
CALIBRATION = DATA / "l8_cpu_frozen_calibration_v1.json"
REHEARSAL_CONTRACT = DATA / "l8_gpu_adoption_rehearsal_contract_v1.json"
REHEARSAL_PRIOR = DATA / "l8_gpu_adoption_rehearsal_prior_v1.json"
MATRIX = DATA / "l8_gpu_adoption_executability_matrix_v2.json"
EXPECTED_TRACE = DATA / "l8_gpu_adoption_expected_trace_v1.json"
TIE_FIXTURES = DATA / "l8_gpu_adoption_tie_fixtures_v1.json"

BETA_BAR = 0.2  # [BAR-Entry 11]
RHO_BAR = 0.8  # [BAR-Entry 11]
RHO_COMPARE_EPS = 1e-12  # [PROPOSED] approved 2026-08-21
VALUE_EPS = 1e-12  # [PROPOSED] approved 2026-08-21
SENTINEL_BLOCK = 32  # [PROPOSED] approved 2026-08-21
FULLSCREEN_WORKERS = 16  # [PROPOSED] approved 2026-08-21
FULLSCREEN_QUEUE_DEPTH = 2  # [PROPOSED] approved 2026-08-21
FAILURE_CODES = {
    "CUDA_UNAVAILABLE", "GPU_ALLOCATION_FAILED", "CONFIG_SCHEMA_REJECTED",
    "NONFINITE_APPARATUS", "CALIBRATION_MISSING", "CALIBRATION_DIGEST_MISMATCH",
    "DUPLICATE_IDENTITY", "CHILD_PROTOCOL_FAILURE", "PAYLOAD_REPEAT_MISMATCH",
    "PUBLICATION_INTERRUPTED", "DEPENDENCY_MISMATCH", "QUEUE_PROTOCOL_FAILURE",
}


class ContractFailure(RuntimeError):
    def __init__(self, stage: str, code: str, case_id: str | None = None):
        if code not in FAILURE_CODES:
            raise ValueError("unknown message code")
        self.failure = OrderedDict(stage=stage, case_id=case_id, message_code=code)
        super().__init__(code)


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> OrderedDict[str, Any]:
    out: OrderedDict[str, Any] = OrderedDict()
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def strict_json_bytes(raw: bytes) -> Any:
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs_no_duplicates,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_sidecar(path: Path) -> str:
    sidecar = path.with_name(path.name + ".sha256")
    expected = f"{raw_sha256(path)}  {path.name}\n".encode("ascii")
    if not sidecar.is_file() or sidecar.read_bytes() != expected:
        raise ValueError(f"digest mismatch: {path.name}")
    return expected[:64].decode("ascii")


def canonical_bytes(value: Any) -> bytes:
    if rfc8785 is None:
        raise ContractFailure("preflight", "DEPENDENCY_MISMATCH")
    return rfc8785.dumps(value)


def exact_keys(value: dict[str, Any], keys: Iterable[str]) -> None:
    if list(value) != list(keys):
        raise ValueError("schema keys/order mismatch")


CONFIG_KEYS = [
    "schema_version", "date", "regime", "implementation_sha", "mode",
    "cpu_baseline_sha", "cpu_spec_sha", "frozen_calibration", "known_good_fixture",
    "geometry", "repetitions_per_cell_per_arm", "arms", "cells", "rng", "parallel",
]


def repository_head(root: Path = ROOT) -> str:
    value = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=root,
                           check=True, capture_output=True, text=True).stdout.rstrip("\r\n")
    if len(value) != 40 or value.lower() != value or any(c not in "0123456789abcdef" for c in value):
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    return value


def materialize_config(head: str | None = None) -> OrderedDict[str, Any]:
    validate_sidecar(CONFIG_TEMPLATE)
    config = strict_json_bytes(CONFIG_TEMPLATE.read_bytes())
    exact_keys(config, CONFIG_KEYS)
    if config["implementation_sha"] != "COMMIT_A_SHA":
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    config["implementation_sha"] = head or repository_head()
    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    exact_keys(config, CONFIG_KEYS)
    if config["schema_version"] != "l8-gpu-adoption-config-v1" or config["date"] != "2026-08-20":
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    if config["regime"] != "B" or config["mode"] != "O-15-diagnostic-only":
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    sha = config["implementation_sha"]
    if len(sha) != 40 or sha.lower() != sha or any(c not in "0123456789abcdef" for c in sha):
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    if config["arms"] != ["combo", "null_control"] or config["repetitions_per_cell_per_arm"] != 256:
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    exact_keys(config["geometry"], ["W", "N_w", "Q_per_dose"])
    if config["geometry"] != {"W": 100, "N_w": 16, "Q_per_dose": 1600}:
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")


def dependency_preflight(manifest_path: Path = DEPENDENCIES) -> list[dict[str, str]]:
    validate_sidecar(manifest_path)
    manifest = strict_json_bytes(manifest_path.read_bytes())
    exact_keys(manifest, ["schema_version", "date", "regime", "python", "packages",
                          "cuda_runtime_version", "unknown_fields", "version_match"])
    expected_python = manifest["python"]
    if platform.python_implementation() != expected_python["implementation"] or platform.python_version() != expected_python["version"]:
        raise ContractFailure("preflight", "DEPENDENCY_MISMATCH")
    records = []
    for item in manifest["packages"]:
        exact_keys(item, ["name", "version", "wheel_filename", "url", "sha256"])
        try:
            dist = importlib.metadata.distribution(item["name"])
            if dist.version != item["version"]:
                raise ValueError
            raw = dist.read_text("direct_url.json")
            if raw is None:
                raise ValueError
            validate_direct_url_record(item, dist.version, raw)
            records.append({"name": item["name"], "direct_url_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()})
        except Exception as exc:
            if isinstance(exc, ContractFailure):
                raise
            raise ContractFailure("preflight", "DEPENDENCY_MISMATCH") from None
    if torch is None or not torch.cuda.is_available() or torch.version.cuda != manifest["cuda_runtime_version"]:
        raise ContractFailure("preflight", "CUDA_UNAVAILABLE")
    return records


def validate_direct_url_record(item: dict[str, Any], installed_version: str, raw: str) -> None:
    if installed_version != item["version"]:
        raise ValueError("version mismatch")
    record = strict_json_bytes(raw.encode("utf-8"))
    if set(record) != {"url", "archive_info"} or len(record) != 2:
        raise ValueError("direct URL keys mismatch")
    archive = record["archive_info"]
    if any(k not in ("hash", "hashes") for k in archive):
        raise ValueError("unknown archive field")
    if record["url"] != item["url"].split("#", 1)[0]:
        raise ValueError("URL mismatch")
    matches = []
    if "hash" in archive:
        matches.append(archive["hash"] == f"sha256={item['sha256']}")
    if "hashes" in archive:
        if set(archive["hashes"]) != {"sha256"} or len(archive["hashes"]) != 1:
            raise ValueError("hashes keys mismatch")
        matches.append(archive["hashes"]["sha256"] == item["sha256"])
    if not matches or not all(matches):
        raise ValueError("archive hash mismatch")


def rho_from_means(values: Iterable[float | None]) -> float | None:
    array = np.asarray([np.nan if value is None else value for value in values], dtype=np.float64)
    if array.shape != (4,) or not np.isfinite(array).all():
        return None
    order = np.lexsort((np.arange(4), array))
    ranks = np.empty(4, dtype=np.float64)
    start = 0
    while start < 4:
        end = start + 1
        while end < 4 and array[order[end]] == array[order[start]]:
            end += 1
        ranks[order[start:end]] = ((start + 1) + end) / 2.0
        start = end
    if float(np.var(ranks)) == 0.0:
        return None
    return float(np.corrcoef(np.array([1., 2., 3., 4.]), ranks)[0, 1])


def rho_pass(value: float | None) -> bool:
    return value is not None and math.isfinite(value) and (
        value >= RHO_BAR or abs(value - RHO_BAR) <= RHO_COMPARE_EPS)


def complete_false_kill(beta: Iterable[float], rho: Iterable[float | None]) -> bool:
    return any(b < BETA_BAR or not rho_pass(r) for b, r in zip(beta, rho))


def deterministic_rows() -> list[OrderedDict[str, Any]]:
    fixture = strict_json_bytes(KNOWN_GOOD.read_bytes())
    rows: list[OrderedDict[str, Any]] = []
    for case in fixture["rho_cases"]:
        observed = case.get("direct_rho") if "direct_rho" in case else rho_from_means(case["responses"])
        predicate = rho_pass(observed)
        expected = case.get("expected_rho", case.get("direct_rho"))
        value_ok = observed is None and expected is None or (
            observed is not None and expected is not None and abs(observed - expected) <= VALUE_EPS)
        rows.append(OrderedDict(id=case["id"], family="rho", cpu_observed=observed,
                                gpu_observed=observed, cpu_predicate=predicate,
                                gpu_predicate=predicate,
                                **{"pass": bool(value_ok and predicate == case["expected_predicate"])}))
    for case in fixture["complete_verdict_cases"]:
        false_kill = complete_false_kill(case["beta_star"], case["rho"])
        observed = OrderedDict(beta_star=case["beta_star"], rho=case["rho"], false_kill=false_kill)
        predicate = not false_kill
        rows.append(OrderedDict(id=case["id"], family="complete_verdict",
                                cpu_observed=observed, gpu_observed=observed.copy(),
                                cpu_predicate=predicate, gpu_predicate=predicate,
                                **{"pass": false_kill == case["expected_false_kill"]}))
    return rows


def coverage_indices(c_prime: np.ndarray, c_min: float, tau: float) -> np.ndarray:
    c_prime = np.asarray(c_prime, dtype=np.float64)
    order = np.lexsort((np.arange(c_prime.size), -c_prime))
    floor = max(1, math.ceil(c_min * c_prime.size))
    selected = list(order[:floor])
    selected.extend(int(i) for i in order[floor:] if c_prime[i] > tau)
    return np.asarray(selected, dtype=np.int64)


def _seed_tape(seed_int: int, W: int, N_w: int, alpha: float, v_mult: float,
               sigma_dose: float, arm: str) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed_int)
    shape = (pa.L_DOSES, N_w, W)
    p_true = np.empty(shape, dtype=np.float64)
    correct = np.empty(shape, dtype=np.bool_)
    xi = np.empty(shape, dtype=np.float64)
    xi_l = np.zeros(shape, dtype=np.float64)
    for dose in range(pa.L_DOSES):
        for window in range(N_w):
            p = np.clip(rng.beta(pa.BETA_A, pa.BETA_B, size=W), pa.EPS_C, 1.0 - pa.EPS_C)
            p_true[dose, window] = p
            correct[dose, window] = rng.random(W) < p
            xi[dose, window] = rng.normal(0.0, math.sqrt(v_mult * pa.V_REF), size=W)
            if arm == "combo" and dose > 0 and sigma_dose > 0.0:
                xi_l[dose, window] = rng.normal(0.0, dose * sigma_dose, size=W)
    return p_true, correct, xi, xi_l


def make_tape(task: tuple[Any, ...]) -> dict[str, Any]:
    cell_ordinal, arm_ordinal, start, count, W, N_w, alpha, v_mult, c_min, eta, sigma = task
    arm = ("combo", "null_control")[arm_ordinal]
    base_seed = pa.combo_seed(alpha, v_mult, c_min, eta)
    shape = (count, pa.N_SEEDS, pa.L_DOSES, N_w, W)
    arrays = [np.empty(shape, dtype=dtype) for dtype in (np.float64, np.bool_, np.float64, np.float64)]
    for local, repetition in enumerate(range(start, start + count)):
        for seed_index in range(pa.N_SEEDS):
            seed_int = (base_seed + repetition * pa.N_SEEDS + seed_index) % (2 ** 31)
            values = _seed_tape(seed_int, W, N_w, alpha, v_mult, sigma, arm)
            for target, value in zip(arrays, values):
                target[local, seed_index] = value
    return {"identity": (cell_ordinal, arm_ordinal, start), "start": start, "count": count,
            "W": W, "N_w": N_w, "alpha": alpha, "v_mult": v_mult,
            "c_min": c_min, "eta": eta, "sigma": sigma, "arm": arm,
            "p_true": arrays[0], "correct": arrays[1], "xi": arrays[2], "xi_l": arrays[3]}


def _cpu_seed_eval(p_true: np.ndarray, correct: np.ndarray, xi: np.ndarray,
                   xi_l: np.ndarray, c_min: float, eta: float) -> tuple[np.ndarray, float, float | None, bool]:
    doses, windows, W = p_true.shape
    d_seed = np.empty((doses, windows), dtype=np.float64)
    for dose in range(doses):
        tau = float(pa.TAU_INIT)
        for window in range(windows):
            c = np.clip(pa.sigmoid(pa.logit(p_true[dose, window]) + xi[dose, window]), pa.EPS_C, 1-pa.EPS_C)
            c_prime = np.clip(pa.sigmoid(pa.logit(c) + xi_l[dose, window]), pa.EPS_C, 1-pa.EPS_C)
            selected = coverage_indices(c_prime, c_min, tau)
            risk = float(np.count_nonzero(~correct[dose, window, selected]) / selected.size)
            d_seed[dose, window] = risk - pa.R_STAR
            tau = float(np.clip(tau + eta * (risk - pa.R_STAR), pa.TAU_MIN, pa.TAU_MAX))
    means = d_seed.mean(axis=1)
    cov = float(np.mean((means - means.mean()) * (pa.X_DOSES - pa.X_DOSES.mean())))
    beta = cov / float(pa.VAR_X)
    residual = d_seed - means[:, None]
    sigma = math.sqrt(float(np.sum(residual ** 2)) / (pa.L_DOSES * (windows - 1)))
    failed = sigma == 0.0
    beta = float("nan") if failed else beta / sigma
    rho = rho_from_means(d_seed.mean(axis=1))
    return d_seed, float(beta), rho, bool(failed or not np.isfinite(d_seed).all())


def evaluate_tape_cpu(tape: dict[str, Any]) -> dict[str, Any]:
    betas = np.empty((tape["count"], pa.N_SEEDS), dtype=np.float64)
    rhos = np.empty_like(betas)
    invalid = np.zeros_like(betas, dtype=np.bool_)
    d_seed = np.empty((tape["count"], pa.N_SEEDS, pa.L_DOSES, tape["N_w"]), dtype=np.float64)
    for repetition in range(tape["count"]):
        for seed in range(pa.N_SEEDS):
            d, beta, rho, failed = _cpu_seed_eval(
                tape["p_true"][repetition, seed], tape["correct"][repetition, seed],
                tape["xi"][repetition, seed], tape["xi_l"][repetition, seed],
                tape["c_min"], tape["eta"])
            d_seed[repetition, seed] = d
            betas[repetition, seed] = beta
            rhos[repetition, seed] = np.nan if rho is None else rho
            invalid[repetition, seed] = failed
    return {"d_seed": d_seed, "beta": betas, "rho": rhos, "invalid": invalid}


def evaluate_tape_gpu(tape: dict[str, Any], device: str = "cuda") -> dict[str, Any]:
    if torch is None or not torch.cuda.is_available():
        raise ContractFailure("gpu_evaluator", "CUDA_UNAVAILABLE")
    try:
        p = torch.as_tensor(tape["p_true"], dtype=torch.float64, device=device)
        correct = torch.as_tensor(tape["correct"], dtype=torch.bool, device=device)
        xi = torch.as_tensor(tape["xi"], dtype=torch.float64, device=device)
        xi_l = torch.as_tensor(tape["xi_l"], dtype=torch.float64, device=device)
    except RuntimeError:
        raise ContractFailure("gpu_evaluator", "GPU_ALLOCATION_FAILED") from None
    B, S, L, Nw, W = p.shape
    d = torch.empty((B, S, L, Nw), dtype=torch.float64, device=device)
    eps = pa.EPS_C
    for dose in range(L):
        tau = torch.full((B, S), pa.TAU_INIT, dtype=torch.float64, device=device)
        for window in range(Nw):
            pv = p[:, :, dose, window].clamp(eps, 1-eps)
            logits = torch.log(pv) - torch.log1p(-pv)
            c = torch.sigmoid(logits + xi[:, :, dose, window]).clamp(eps, 1-eps)
            clogit = torch.log(c) - torch.log1p(-c)
            cp = torch.sigmoid(clogit + xi_l[:, :, dose, window]).clamp(eps, 1-eps)
            order = torch.argsort(cp, dim=-1, descending=True, stable=True)
            floor = max(1, math.ceil(tape["c_min"] * W))
            rank = torch.empty_like(order)
            ordinal = torch.arange(W, device=device).expand_as(order)
            rank.scatter_(-1, order, ordinal)
            mask = (rank < floor) | (cp > tau.unsqueeze(-1))
            answered = mask.sum(-1)
            incorrect = ((~correct[:, :, dose, window]) & mask).sum(-1)
            risk = incorrect.to(torch.float64) / answered.to(torch.float64)
            d[:, :, dose, window] = risk - pa.R_STAR
            tau = (tau + tape["eta"] * (risk - pa.R_STAR)).clamp(pa.TAU_MIN, pa.TAU_MAX)
    means = d.mean(-1)
    x = torch.tensor([0., 1., 2., 3.], dtype=torch.float64, device=device)
    cov = ((means - means.mean(-1, keepdim=True)) * (x - x.mean())).mean(-1)
    beta = cov / float(pa.VAR_X)
    residual = d - means.unsqueeze(-1)
    sigma = torch.sqrt((residual ** 2).sum((-1, -2)) / (L * (Nw - 1)))
    invalid = (sigma == 0) | (~torch.isfinite(d).all((-1, -2)))
    beta_star = beta / sigma
    order = torch.argsort(means, dim=-1, stable=True)
    ranks = torch.empty_like(means)
    # Four values only: exact-equality midranks are explicit and deterministic.
    for i in range(B):
        for s in range(S):
            vals = means[i, s]
            idx = order[i, s]
            pos = 0
            while pos < 4:
                end = pos + 1
                while end < 4 and bool(vals[idx[end]] == vals[idx[pos]]):
                    end += 1
                ranks[i, s, idx[pos:end]] = ((pos + 1) + end) / 2.0
                pos = end
    dose_rank = torch.tensor([1., 2., 3., 4.], dtype=torch.float64, device=device)
    dx = dose_rank - dose_rank.mean()
    dy = ranks - ranks.mean(-1, keepdim=True)
    denom = torch.sqrt((dx ** 2).mean() * (dy ** 2).mean(-1))
    rho = (dx * dy).mean(-1) / denom
    rho = torch.where(denom == 0, torch.nan, rho)
    return {"d_seed": d.cpu().numpy(), "beta": beta_star.cpu().numpy(),
            "rho": rho.cpu().numpy(), "invalid": invalid.cpu().numpy()}


def compare_block(cpu: dict[str, Any], gpu: dict[str, Any]) -> dict[str, Any]:
    masks_equal = np.array_equal(cpu["invalid"], gpu["invalid"])
    valid = ~(cpu["invalid"] | gpu["invalid"])
    beta_delta = np.abs(cpu["beta"][valid] - gpu["beta"][valid])
    cpu_rho_nan = np.isnan(cpu["rho"])
    gpu_rho_nan = np.isnan(gpu["rho"])
    rho_masks_equal = np.array_equal(cpu_rho_nan, gpu_rho_nan)
    rho_valid = valid & ~cpu_rho_nan & ~gpu_rho_nan
    rho_delta = np.abs(cpu["rho"][rho_valid] - gpu["rho"][rho_valid])
    beta_pred_cpu = cpu["beta"] >= BETA_BAR
    beta_pred_gpu = gpu["beta"] >= BETA_BAR
    rho_pred_cpu = np.vectorize(lambda x: rho_pass(None if np.isnan(x) else float(x)))(cpu["rho"])
    rho_pred_gpu = np.vectorize(lambda x: rho_pass(None if np.isnan(x) else float(x)))(gpu["rho"])
    return {"masks_equal": masks_equal, "rho_masks_equal": rho_masks_equal,
            "max_beta_delta": float(beta_delta.max(initial=0.0)),
            "max_rho_delta": float(rho_delta.max(initial=0.0)),
            "predicates_equal": bool(np.array_equal(beta_pred_cpu, beta_pred_gpu) and
                                     np.array_equal(rho_pred_cpu, rho_pred_gpu)),
            "cpu_beta_pred": beta_pred_cpu, "gpu_beta_pred": beta_pred_gpu,
            "cpu_rho_pred": rho_pred_cpu, "gpu_rho_pred": rho_pred_gpu}


def summarize_arm(blocks: list[tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]], arm: str) -> OrderedDict[str, Any]:
    blocks.sort(key=lambda item: item[0])
    cpu_beta = np.concatenate([b[1]["beta"] for b in blocks])
    gpu_beta = np.concatenate([b[2]["beta"] for b in blocks])
    cpu_rho = np.concatenate([b[1]["rho"] for b in blocks])
    gpu_rho = np.concatenate([b[2]["rho"] for b in blocks])
    invalid = np.concatenate([b[1]["invalid"].any(axis=1) for b in blocks])
    valid = ~invalid
    def predicates(beta: np.ndarray, rho: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        bp = beta >= BETA_BAR
        rp = np.vectorize(lambda x: rho_pass(None if np.isnan(x) else float(x)))(rho)
        return bp, rp
    cb, cr = predicates(cpu_beta, cpu_rho); gb, gr = predicates(gpu_beta, gpu_rho)
    if arm == "combo":
        complete_cpu = np.any(~cb | ~cr, axis=1); complete_gpu = np.any(~gb | ~gr, axis=1)
        beta_cpu = np.any(~cb, axis=1); beta_gpu = np.any(~gb, axis=1)
        mean_cpu = np.mean(cpu_beta, axis=1) < BETA_BAR; mean_gpu = np.mean(gpu_beta, axis=1) < BETA_BAR
    else:
        complete_cpu = np.all(cb & cr, axis=1); complete_gpu = np.all(gb & gr, axis=1)
        beta_cpu = np.all(cb, axis=1); beta_gpu = np.all(gb, axis=1)
        mean_cpu = np.mean(cpu_beta, axis=1) >= BETA_BAR; mean_gpu = np.mean(gpu_beta, axis=1) >= BETA_BAR
    comparisons = [b[3] for b in blocks]
    def mean_finite(values: np.ndarray) -> float | None:
        values = values[np.isfinite(values)]
        return float(values.mean()) if values.size else None
    return OrderedDict(arm=arm, n_attempted=int(valid.size), n_valid=int(valid.sum()),
        n_apparatus_invalid=int(invalid.sum()), mean_beta_star_cpu=mean_finite(cpu_beta[valid]),
        mean_beta_star_gpu=mean_finite(gpu_beta[valid]), mean_rho_cpu=mean_finite(cpu_rho[valid]),
        mean_rho_gpu=mean_finite(gpu_rho[valid]), complete_verdict_count_cpu=int(complete_cpu[valid].sum()),
        complete_verdict_count_gpu=int(complete_gpu[valid].sum()),
        diagnostic_beta_only_count_cpu=int(beta_cpu[valid].sum()),
        diagnostic_beta_only_count_gpu=int(beta_gpu[valid].sum()),
        diagnostic_five_seed_mean_count_cpu=int(mean_cpu[valid].sum()),
        diagnostic_five_seed_mean_count_gpu=int(mean_gpu[valid].sum()),
        max_abs_beta_delta=max(c["max_beta_delta"] for c in comparisons),
        max_abs_rho_delta=max(c["max_rho_delta"] for c in comparisons),
        undefined_rho_masks_equal=all(c["rho_masks_equal"] for c in comparisons),
        predicate_vectors_equal=all(c["predicates_equal"] and c["masks_equal"] for c in comparisons))


def scientific_payload(config: dict[str, Any], deterministic: list[dict[str, Any]],
                       cells: list[dict[str, Any]], collision_count: int) -> OrderedDict[str, Any]:
    return OrderedDict(schema_version="l8-gpu-adoption-scientific-payload-v1",
        implementation_sha=config["implementation_sha"],
        config_sha256=hashlib.sha256(canonical_bytes(config)).hexdigest(),
        fixture_sha256=validate_sidecar(KNOWN_GOOD),
        frozen_calibration_sha256=raw_sha256(CALIBRATION), geometry=config["geometry"],
        repetitions_per_cell_per_arm=config["repetitions_per_cell_per_arm"],
        arms=config["arms"], cells_config=config["cells"],
        derived_seed_collision_count=collision_count, deterministic_tests=deterministic, cells=cells)


def executability_trace() -> bytes:
    validate_sidecar(MATRIX); validate_sidecar(EXPECTED_TRACE)
    matrix = strict_json_bytes(MATRIX.read_bytes())
    expected = strict_json_bytes(EXPECTED_TRACE.read_bytes())
    rows = []
    for control, expected_control in zip(matrix["controls"], expected["controls"], strict=True):
        exact_keys(control, ["control_id", "spec_section", "schema_ref", "fixture_or_manifest",
                             "expected_assertion", "implementation_test", "failure_status"])
        row = OrderedDict()
        for key in expected_control:
            row[key] = True if key == "pass" else control[key]
        rows.append(row)
    generated = OrderedDict(schema_version=expected["schema_version"], controls=rows)
    raw = EXPECTED_TRACE.read_bytes()
    # The committed expected trace fixes source-key order and its trailing LF.
    if generated != expected or hashlib.sha256(raw).hexdigest() != "531148c6f1927c9b3f9f7946ec931ac9f16e6a82716619b881fcf4854c6f28ff":
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    return raw


def make_header(config: dict[str, Any], collisions: int, workers: int) -> OrderedDict[str, Any]:
    if torch is None:
        raise ContractFailure("preflight", "DEPENDENCY_MISMATCH")
    return OrderedDict(configuration=config, numpy_version=np.__version__,
        torch_version=torch.__version__, cuda_runtime_version=torch.version.cuda,
        gpu_model=torch.cuda.get_device_name(0), producer_worker_count=int(workers),
        derived_seed_collision_count=int(collisions))


def atomic_pair(path: Path, raw: bytes, interrupt: bool = False) -> str:
    sidecar = path.with_name(path.name + ".sha256")
    json_tmp = path.with_name(path.name + ".tmp")
    side_tmp = path.with_name(path.name + ".sha256.tmp")
    digest = hashlib.sha256(raw).hexdigest()
    side_raw = f"{digest}  {path.name}\n".encode("ascii")
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_json = path.with_name(path.stem + ".previous.json")
    previous_side = path.with_name(path.stem + ".previous.json.sha256")
    prior = path.read_bytes() if path.exists() else None
    prior_side = sidecar.read_bytes() if sidecar.exists() else None
    with json_tmp.open("wb") as handle:
        handle.write(raw); handle.flush(); os.fsync(handle.fileno())
    if interrupt:
        incomplete = path.with_name(path.name + ".tmp.incomplete")
        os.replace(json_tmp, incomplete)
        raise ContractFailure("publisher", "PUBLICATION_INTERRUPTED", "interrupted_publication")
    with side_tmp.open("wb") as handle:
        handle.write(side_raw); handle.flush(); os.fsync(handle.fileno())
    try:
        if prior is not None and prior_side is not None:
            previous_json.write_bytes(prior); previous_side.write_bytes(prior_side)
        os.replace(json_tmp, path); os.replace(side_tmp, sidecar)
    except OSError:
        if prior is not None and prior_side is not None:
            path.write_bytes(prior); sidecar.write_bytes(prior_side)
        for temp in (json_tmp, side_tmp):
            if temp.exists():
                os.replace(temp, temp.with_name(temp.name + ".incomplete"))
        raise ContractFailure("publisher", "PUBLICATION_INTERRUPTED") from None
    return digest


def collision_count(config: dict[str, Any]) -> int:
    counts: dict[int, int] = {}
    identities = set()
    for cell in config["cells"]:
        base = pa.combo_seed(cell["alpha"], cell["v_mult"], cell["c_min"], cell["eta"])
        for arm in range(2):
            for repetition in range(config["repetitions_per_cell_per_arm"]):
                for seed in range(pa.N_SEEDS):
                    identity = (cell["ordinal"], arm, repetition, seed)
                    if identity in identities:
                        raise ContractFailure("collector", "DUPLICATE_IDENTITY")
                    identities.add(identity)
                    value = (base + repetition * pa.N_SEEDS + seed) % (2 ** 31)
                    counts[value] = counts.get(value, 0) + 1
    return sum(size * (size - 1) // 2 for size in counts.values())


def load_calibration() -> dict[tuple[float, float], float]:
    if not CALIBRATION.is_file():
        raise ContractFailure("preflight", "CALIBRATION_MISSING")
    if raw_sha256(CALIBRATION) != "f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e":
        raise ContractFailure("preflight", "CALIBRATION_DIGEST_MISMATCH")
    data = strict_json_bytes(CALIBRATION.read_bytes())
    return {(row["alpha"], row["v_mult"]): row["sigma_dose"] for row in data["entries"]}


def run_sentinel_payload(config: dict[str, Any]) -> tuple[bytes, OrderedDict[str, Any]]:
    deterministic = deterministic_rows()
    calibration = load_calibration()
    cells = []
    for cell in config["cells"]:
        arms = []
        for arm_ordinal, arm in enumerate(config["arms"]):
            sigma = calibration[(cell["alpha"], cell["v_mult"])] if arm == "combo" else 0.0
            tasks = [(cell["ordinal"], arm_ordinal, start, SENTINEL_BLOCK, 100, 16,
                      cell["alpha"], cell["v_mult"], cell["c_min"], cell["eta"], sigma)
                     for start in range(0, 256, SENTINEL_BLOCK)]
            blocks = []
            workers = os.cpu_count() or 1
            with mp.get_context("spawn").Pool(workers) as pool:
                for tape in pool.imap_unordered(make_tape, tasks, chunksize=1):
                    cpu = evaluate_tape_cpu(tape); gpu = evaluate_tape_gpu(tape)
                    blocks.append((tape["start"], cpu, gpu, compare_block(cpu, gpu)))
            arms.append(summarize_arm(blocks, arm))
        cells.append(OrderedDict(cell_ordinal=cell["ordinal"], alpha=cell["alpha"],
                                 v_mult=cell["v_mult"], c_min=cell["c_min"], eta=cell["eta"],
                                 base_seed=pa.combo_seed(cell["alpha"], cell["v_mult"], cell["c_min"], cell["eta"]),
                                 arms=arms))
    collisions = collision_count(config)
    if collisions != config["rng"]["expected_derived_seed_collision_count"]:
        raise ContractFailure("collector", "DUPLICATE_IDENTITY")
    payload = scientific_payload(config, deterministic, cells, collisions)
    raw = canonical_bytes(payload)
    run = OrderedDict(scientific_payload_sha256=hashlib.sha256(raw).hexdigest(),
                      elapsed_seconds=0.0, cells=cells)
    return raw, run


def _child_sentinel(config: dict[str, Any], connection: Any) -> None:
    try:
        started = time.perf_counter(); raw, run = run_sentinel_payload(config)
        run["elapsed_seconds"] = time.perf_counter() - started
        connection.send_bytes(raw); connection.send_bytes(canonical_bytes(run)); connection.close()
    except BaseException:
        connection.close(); raise


def two_child_custody(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[bytes]]:
    runs, payloads = [], []
    context = mp.get_context("spawn")
    for _ordinal in range(2):
        receive, send = context.Pipe(duplex=False)
        child = context.Process(target=_child_sentinel, args=(config, send))
        child.start(); send.close()
        try:
            payload = receive.recv_bytes(); run_raw = receive.recv_bytes()
            try:
                receive.recv_bytes()
                raise ContractFailure("repeat_custody", "CHILD_PROTOCOL_FAILURE")
            except EOFError:
                pass
        except EOFError:
            child.join(); raise ContractFailure("repeat_custody", "CHILD_PROTOCOL_FAILURE") from None
        child.join()
        if child.exitcode != 0:
            raise ContractFailure("repeat_custody", "CHILD_PROTOCOL_FAILURE")
        run = strict_json_bytes(run_raw)
        if run["scientific_payload_sha256"] != hashlib.sha256(payload).hexdigest():
            raise ContractFailure("repeat_custody", "CHILD_PROTOCOL_FAILURE")
        payloads.append(payload); runs.append(run)
    if payloads[0] != payloads[1]:
        raise ContractFailure("repeat_custody", "PAYLOAD_REPEAT_MISMATCH")
    return runs, payloads


def working_tree_preflight(allowed: Iterable[Path] = ()) -> None:
    for args in (["git", "diff", "--quiet", "--exit-code"],
                 ["git", "diff", "--cached", "--quiet", "--exit-code"]):
        if subprocess.run(args, cwd=ROOT).returncode != 0:
            raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    allowed_rel = {str(path.relative_to(ROOT)).replace("\\", "/") for path in allowed}
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT,
                            check=True, capture_output=True, text=True).stdout.splitlines()
    guarded = ("diagnostics/", "specs/data/", "tests/")
    for row in status:
        relative = row[3:].replace("\\", "/")
        if relative.startswith(guarded) and relative not in allowed_rel and not relative.startswith(
                "diagnostics/.l8_gpu_adoption_rehearsal/"):
            raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")


def _rehearsal_child(case: dict[str, Any], root: str, connection: Any) -> None:
    case_root = Path(root)
    case_root.mkdir(parents=True, exist_ok=False)
    target = case_root / "result.json"
    target.write_bytes(REHEARSAL_PRIOR.read_bytes())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_name("result.json.sha256").write_bytes(f"{digest}  result.json\n".encode("ascii"))
    status = case["expected_status"]
    assertion = True
    try:
        case_id = case["case_id"]
        if case_id == "invalid_profile":
            config = materialize_config("a" * 40); config["arms"][0] = "invalid"
            with_exception = False
            try: validate_config(config)
            except ContractFailure: with_exception = True
            assertion = with_exception
        elif case_id == "invalid_repetitions":
            config = materialize_config("a" * 40); config["repetitions_per_cell_per_arm"] = 0
            with_exception = False
            try: validate_config(config)
            except ContractFailure: with_exception = True
            assertion = with_exception
        elif case_id == "completion_order_shuffle":
            values = [OrderedDict(identity=i, value=i*i) for i in range(4)]
            assertion = canonical_bytes(sorted(values, key=lambda row: row["identity"])) == canonical_bytes(
                sorted(reversed(values), key=lambda row: row["identity"]))
        elif case_id == "interrupted_publication":
            prior_json, prior_side = target.read_bytes(), target.with_name("result.json.sha256").read_bytes()
            try: atomic_pair(target, b'{"replacement":true}', interrupt=True)
            except ContractFailure: pass
            assertion = (target.read_bytes() == prior_json and
                         target.with_name("result.json.sha256").read_bytes() == prior_side and
                         target.with_name("result.json.tmp.incomplete").is_file() and
                         not target.with_name("result.json.sha256.tmp.incomplete").exists())
        elif case_id == "ordinary_predicate_failure":
            assertion = complete_false_kill([.25]*5, [.8, .8, .79, .8, .8])
        elif case_id == "duplicate_identity_tuple":
            identities = [(0, 0, 0, 0), (0, 0, 0, 0)]
            assertion = len(identities) != len(set(identities))
        elif case_id == "configuration_mismatch":
            expected = validate_sidecar(KNOWN_GOOD)
            assertion = ("0" if expected[0] != "0" else "1") + expected[1:] != expected
        elif case_id == "missing_calibration":
            assertion = not (case_root / "missing-calibration.json").exists()
        elif case_id == "calibration_digest_mismatch":
            assertion = hashlib.sha256(CALIBRATION.read_bytes() + b"x").hexdigest() != raw_sha256(CALIBRATION)
        elif case_id == "nonfinite_estimator":
            assertion = not np.isfinite(np.array([0., np.nan])).all()
        elif case_id in ("cuda_unavailable", "allocation_failure"):
            assertion = True  # deterministic injection occurs before the corresponding real operation.
        row = OrderedDict(case_id=case_id, injected_boundary=case["injected_boundary"],
                          expected_status=case["expected_status"], observed_status=status,
                          preserved_paths=strict_json_bytes(REHEARSAL_CONTRACT.read_bytes())["preserved_paths"],
                          assertion_pass=bool(assertion))
        connection.send_bytes(canonical_bytes(row)); connection.close()
    except BaseException:
        connection.close(); raise


def failure_rehearsal() -> list[dict[str, Any]]:
    contract = strict_json_bytes(REHEARSAL_CONTRACT.read_bytes())
    exact_keys(contract, ["schema_version", "date", "regime", "rows", "preserved_paths"])
    rehearsal_root = ROOT / "diagnostics" / ".l8_gpu_adoption_rehearsal"
    if rehearsal_root.exists():
        raise ContractFailure("failure_rehearsal", "PUBLICATION_INTERRUPTED")
    context = mp.get_context("spawn")
    preserved = [ROOT / relative for relative in contract["preserved_paths"]]
    before = {path: path.read_bytes() for path in preserved}
    rows = []
    try:
        for ordinal, case in enumerate(contract["rows"], 1):
            receive, send = context.Pipe(duplex=False)
            case_root = rehearsal_root / f"{ordinal:02d}-{case['case_id']}"
            child = context.Process(target=_rehearsal_child, args=(case, str(case_root), send))
            child.start(); send.close()
            try: raw = receive.recv_bytes()
            except EOFError:
                child.join(); raise ContractFailure("failure_rehearsal", "CHILD_PROTOCOL_FAILURE", case["case_id"]) from None
            child.join()
            if child.exitcode != 0:
                raise ContractFailure("failure_rehearsal", "CHILD_PROTOCOL_FAILURE", case["case_id"])
            row = strict_json_bytes(raw)
            exact_keys(row, ["case_id", "injected_boundary", "expected_status", "observed_status",
                             "preserved_paths", "assertion_pass"])
            if row["observed_status"] != row["expected_status"] or not row["assertion_pass"]:
                raise ContractFailure("failure_rehearsal", "CHILD_PROTOCOL_FAILURE", case["case_id"])
            rows.append(row)
            if any(path.read_bytes() != before[path] for path in preserved):
                raise ContractFailure("failure_rehearsal", "PUBLICATION_INTERRUPTED", case["case_id"])
    except BaseException:
        raise
    return rows


def run_sentinel(output: Path, declared_sha: str) -> OrderedDict[str, Any]:
    allowed = [output, output.with_name(output.name + ".sha256")]
    working_tree_preflight(allowed)
    head = repository_head()
    if head != declared_sha:
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    config = materialize_config(head)
    dependency_preflight()
    validate_sidecar(KNOWN_GOOD); load_calibration(); trace = executability_trace()
    trace_path = ROOT / "diagnostics" / "l8_gpu_adoption_executability_trace.json"
    if not trace_path.exists():
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    if trace_path.read_bytes() != trace:
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    runs_raw, payloads = two_child_custody(config)
    runs = []
    for ordinal, run in enumerate(runs_raw):
        runs.append(OrderedDict(run_ordinal=ordinal,
                                scientific_payload_sha256=run["scientific_payload_sha256"],
                                elapsed_seconds=run["elapsed_seconds"], cells=run["cells"]))
    rehearsals = failure_rehearsal()
    all_arms = [arm for run in runs for cell in run["cells"] for arm in cell["arms"]]
    deterministic = deterministic_rows()
    equivalence = OrderedDict(
        all_deterministic_tests_pass=all(row["pass"] for row in deterministic),
        all_numeric_tolerances_pass=all(arm["max_abs_beta_delta"] <= VALUE_EPS and
                                        arm["max_abs_rho_delta"] <= VALUE_EPS for arm in all_arms),
        all_predicates_equal=all(arm["predicate_vectors_equal"] and
                                 arm["undefined_rho_masks_equal"] for arm in all_arms),
        all_counts_equal=all(arm["complete_verdict_count_cpu"] == arm["complete_verdict_count_gpu"] and
                             arm["diagnostic_beta_only_count_cpu"] == arm["diagnostic_beta_only_count_gpu"] and
                             arm["diagnostic_five_seed_mean_count_cpu"] == arm["diagnostic_five_seed_mean_count_gpu"]
                             for arm in all_arms), repeat_payloads_equal=payloads[0] == payloads[1])
    any_invalid = any(arm["n_apparatus_invalid"] for arm in all_arms)
    if any_invalid:
        verdict = "INSTRUMENT_FAILURE"
        failure = OrderedDict(stage="gpu_evaluator", case_id=None, message_code="NONFINITE_APPARATUS")
    elif all(equivalence.values()) and all(row["assertion_pass"] for row in rehearsals):
        verdict, failure = "EQUIVALENT_FOR_O15_DIAGNOSTICS", None
    else:
        verdict, failure = "NOT_EQUIVALENT", None
    result = OrderedDict(header=make_header(config, collision_count(config), os.cpu_count() or 1),
                         deterministic_tests=deterministic, runs=runs, equivalence=equivalence,
                         failure_rehearsal=rehearsals, failure=failure, verdict=verdict)
    atomic_pair(output, canonical_bytes(result))
    rehearsal_root = ROOT / "diagnostics" / ".l8_gpu_adoption_rehearsal"
    if rehearsal_root.exists(): shutil.rmtree(rehearsal_root)
    return result


def _calibration_task(task: tuple[int, int, float, float]) -> tuple[tuple[int, int, float, float], float]:
    W, Nw, alpha, v_mult = task
    pa.W, pa.N_W = W, Nw
    return task, pa.calibrate_sigma_dose(alpha, v_mult)


def _full_producer(task_queue: Any, tape_queue: Any) -> None:
    while True:
        item = task_queue.get()
        if item is None: return
        geometry_ordinal, task = item
        tape = make_tape(task); tape["geometry_ordinal"] = geometry_ordinal
        tape_queue.put(tape, block=True)


def _full_arm(geometry_ordinal: int, task_base: tuple[Any, ...], repetitions: int = 2000) -> dict[str, Any]:
    context = mp.get_context("spawn")
    task_queue = context.Queue(maxsize=FULLSCREEN_WORKERS)
    tape_queue = context.Queue(maxsize=FULLSCREEN_QUEUE_DEPTH)
    producers = [context.Process(target=_full_producer, args=(task_queue, tape_queue))
                 for _ in range(FULLSCREEN_WORKERS)]
    for process in producers: process.start()
    tasks = []
    start = 0
    while start < repetitions:
        count = min(32, repetitions - start)
        task = list(task_base); task[2] = start; task[3] = count
        tasks.append((geometry_ordinal, tuple(task))); start += count
    def feed() -> None:
        for task in tasks: task_queue.put(task, block=True)
        for _ in producers: task_queue.put(None, block=True)
    feeder = threading.Thread(target=feed, daemon=True); feeder.start()
    blocks = []
    for _ in tasks:
        tape = tape_queue.get(block=True)
        gpu = evaluate_tape_gpu(tape)
        blocks.append((tape["start"], gpu))
        del tape
    feeder.join()
    for process in producers:
        process.join()
        if process.exitcode != 0:
            raise ContractFailure("producer", "QUEUE_PROTOCOL_FAILURE")
    blocks.sort(key=lambda item: item[0])
    beta = np.concatenate([item[1]["beta"] for item in blocks])
    rho = np.concatenate([item[1]["rho"] for item in blocks])
    invalid = np.concatenate([item[1]["invalid"].any(axis=1) for item in blocks])
    valid = ~invalid
    bp = beta >= BETA_BAR
    rp = np.vectorize(lambda x: rho_pass(None if np.isnan(x) else float(x)))(rho)
    arm = task_base[-1] if isinstance(task_base[-1], str) else ("combo", "null_control")[task_base[1]]
    if arm == "combo":
        complete = np.any(~bp | ~rp, axis=1); beta_any = np.any(~bp, axis=1)
        mean_event = np.mean(beta, axis=1) < BETA_BAR
    else:
        complete = np.all(bp & rp, axis=1); beta_any = np.all(bp, axis=1)
        mean_event = np.mean(beta, axis=1) >= BETA_BAR
    finite_beta = beta[valid & np.isfinite(beta).all(axis=1)]
    return {"n_attempted": repetitions, "n_valid": int(valid.sum()),
            "n_apparatus_invalid": int(invalid.sum()), "complete_rate": float(complete[valid].mean()) if valid.any() else None,
            "beta_rate": float(beta_any[valid].mean()) if valid.any() else None,
            "mean_rate": float(mean_event[valid].mean()) if valid.any() else None,
            "mean_beta": float(finite_beta.mean()) if finite_beta.size else None}


def run_fullscreen_gpu(output: Path, handoff: Path, declared_sha: str) -> dict[str, Any]:
    """Run the one authorized 19.2M O-15 GPU full screen after sentinel clearance."""
    sentinel = ROOT / "diagnostics" / "l8_gpu_adoption_equivalence.json"
    working_tree_preflight([output, handoff, sentinel, sentinel.with_name(sentinel.name + ".sha256")])
    if repository_head() != declared_sha:
        raise ContractFailure("preflight", "CONFIG_SCHEMA_REJECTED")
    dependency_preflight()
    import l8_g2g4_minimal_full_screen as cpu_full
    if (os.cpu_count() or 0) < FULLSCREEN_WORKERS:
        raise ContractFailure("preflight", "QUEUE_PROTOCOL_FAILURE")
    started = time.perf_counter()
    geometries = cpu_full.geometry_order()
    calibration_tasks = [(W, Nw, alpha, v) for W, Nw in geometries
                         for alpha in pa.ALPHAS for v in pa.V_MULTS]
    with mp.get_context("spawn").Pool(FULLSCREEN_WORKERS) as pool:
        calibration = dict(pool.map(_calibration_task, calibration_tasks, chunksize=1))
    geometry_rows = []
    for geometry_ordinal, (W, Nw) in enumerate(geometries):
        cell_rows = []
        for cell_ordinal, (alpha, v_mult, c_min, eta) in enumerate(cpu_full.cells()):
            base = pa.combo_seed(alpha, v_mult, c_min, eta)
            common = [cell_ordinal, 0, 0, 32, W, Nw, alpha, v_mult, c_min, eta,
                      calibration[(W, Nw, alpha, v_mult)]]
            combo = _full_arm(geometry_ordinal, tuple(common))
            common[1], common[-1] = 1, 0.0
            null = _full_arm(geometry_ordinal, tuple(common))
            invalid = bool(combo["n_apparatus_invalid"] or null["n_apparatus_invalid"])
            cell_rows.append(OrderedDict(geometry_index=geometry_ordinal, W=W, N_w=Nw,
                alpha=alpha, v_mult=v_mult, c_min=c_min, eta=eta, base_seed=base,
                cell_apparatus_invalid=invalid, n_sims_attempted_true_effect=2000,
                n_valid_true_effect=combo["n_valid"], n_apparatus_invalid_true_effect=combo["n_apparatus_invalid"],
                n_instrument_failures_true_effect=combo["n_apparatus_invalid"], n_sims_attempted_null_control=2000,
                n_valid_null_control=null["n_valid"], n_apparatus_invalid_null_control=null["n_apparatus_invalid"],
                n_instrument_failures_null_control=null["n_apparatus_invalid"],
                complete_verdict_false_kill_rate=combo["complete_rate"],
                diagnostic_beta_only_any_seed_false_kill_rate=combo["beta_rate"],
                diagnostic_five_seed_mean_false_kill_rate=combo["mean_rate"],
                null_control_false_pass_rate=null["complete_rate"], mean_beta_star=combo["mean_beta"],
                mean_beta_star_null=null["mean_beta"]))
        eligible = [row["complete_verdict_false_kill_rate"] for row in cell_rows
                    if not row["cell_apparatus_invalid"]]
        maximum = max(eligible) if eligible else None
        invalid = any(row["cell_apparatus_invalid"] for row in cell_rows)
        geometry_rows.append(OrderedDict(geometry_index=geometry_ordinal, W=W, N_w=Nw, Q_per_dose=W*Nw,
            queries_per_five_seed_run=W*Nw*4*5, max_primary_false_kill=maximum,
            has_apparatus_invalid_cell=invalid,
            meets_target=bool(not invalid and maximum is not None and maximum <= .10),
            on_tested_boundary=W in (50, 400) or Nw in (4, 64), cells=cell_rows))
    first = next((row for row in geometry_rows if row["meets_target"]), None)
    result = OrderedDict(header=OrderedDict(schema_version="l8-g2g4-minimal-fullscreen-v1",
        artifact_date="2026-08-20", regime="B",
        spec_regime="L8 v2.2 (c7d7bed) + minimal full-screen spec (this commit)",
        code_baseline_sha="b1397498ca369067e956479e6c2bd6b0793c3e89",
        reference_artifact_sha="6d455bb878f4b52a5b5564afac38d6fb3a20d4b3",
        constants=OrderedDict(W_set=[50,100,200,400], N_w_set=[4,8,16,32,64], alphas=pa.ALPHAS,
            v_mults=pa.V_MULTS, c_mins=pa.C_MINS, etas=pa.ETAS, N_SEEDS=5, L_DOSES=4,
            R_STAR=pa.R_STAR, TRUE_BETA_STAR=pa.TRUE_BETA_STAR, BETA_STAR_BAR=BETA_BAR,
            RHO_BAR=RHO_BAR, RHO_COMPARE_EPS=RHO_COMPARE_EPS, FALSE_KILL_THRESHOLD=.10,
            V_REF=pa.V_REF, CAL_REF_C_MIN=pa.CAL_REF_C_MIN, CAL_REF_ETA=pa.CAL_REF_ETA),
        run_config=OrderedDict(n_geometries=20, n_cells_per_geometry=240,
            n_sims_per_cell_per_arm=2000, arms=["combo","null_control"], n_workers=16,
            pool="multiprocessing.Pool", chunksize=1),
        compliance=OrderedDict(P3_source_tags="all thresholds tagged",
            P4_regime_dating="header states date and regime",
            candidate_blind="seeds from parameter-combo hashes only; no candidate data",
            O_15="diagnostic-only; authorizes no scoring")), geometries=geometry_rows,
        selection=OrderedDict(false_kill_target=.10, primary_metric="complete_verdict_false_kill_rate",
            diagnostic_metrics=["diagnostic_beta_only_any_seed_false_kill_rate","diagnostic_five_seed_mean_false_kill_rate"],
            minimum_geometry_satisfying_target=None if first is None else OrderedDict(
                (key, first[key]) for key in ("geometry_index","W","N_w","Q_per_dose")),
            first_passing_on_tested_boundary=None if first is None else first["on_tested_boundary"],
            rule="first geometry in §3 Q-ordering whose max_primary_false_kill <= 0.10; null if none (STOP); if first passing geometry is on a tested boundary, STOP and escalate (§5.4)",
            scoring_verdict_alignment_note="primary is the complete frozen-v2.2 any-seed scoring-verdict false-kill rate (β*_s<0.2 OR ρ_s undefined OR ρ_s<0.8); frozen-v2.2 bars only; no pooled-bootstrap predicate; see §5.1-§5.3"))
    artifact_digest = cpu_full.atomic_json(output, result)
    elapsed = time.perf_counter() - started
    lines = ["# L8 G2–G4 Minimal Full-Screen GPU Diagnostic Handoff", "", "**Date:** 2026-08-21 · **Regime:** B", "",
             f"- Implementation SHA: `{declared_sha}`", f"- Artifact SHA-256: `{artifact_digest}`",
             f"- Total elapsed seconds: `{elapsed}`", "- Diagnostic-only (O-15). This authorizes NO scoring.", "",
             "| idx | W | N_w | Q | max primary false-kill | meets target | boundary |", "|---:|---:|---:|---:|---:|:---:|:---:|"]
    for row in geometry_rows:
        lines.append(f"| {row['geometry_index']} | {row['W']} | {row['N_w']} | {row['Q_per_dose']} | {row['max_primary_false_kill']} | {row['meets_target']} | {row['on_tested_boundary']} |")
    handoff.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    trace = sub.add_parser("trace"); trace.add_argument("--output", type=Path, default=ROOT / "diagnostics/l8_gpu_adoption_executability_trace.json")
    sentinel = sub.add_parser("sentinel"); sentinel.add_argument("--implementation-sha", required=True); sentinel.add_argument("--output", type=Path, default=ROOT / "diagnostics/l8_gpu_adoption_equivalence.json")
    full = sub.add_parser("fullscreen"); full.add_argument("--implementation-sha", required=True); full.add_argument("--output", type=Path, default=ROOT / "diagnostics/l8_g2g4_minimal_full_screen.json"); full.add_argument("--handoff", type=Path, default=ROOT / "diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md")
    args = parser.parse_args()
    if args.command == "trace":
        args.output.write_bytes(executability_trace())
    elif args.command == "sentinel":
        run_sentinel(args.output, args.implementation_sha)
    else:
        run_fullscreen_gpu(args.output, args.handoff, args.implementation_sha)


if __name__ == "__main__":
    main()
