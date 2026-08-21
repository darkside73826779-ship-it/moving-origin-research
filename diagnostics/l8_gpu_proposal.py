"""PROPOSED, non-scoring CUDA path for L8 statistical-equivalence review.

Uses float64 tensors for simulation state and estimator reductions.  It is not
bitwise equivalent to NumPy: CUDA random streams differ.  No full screen is
enabled here; the only public entry point runs bounded equivalence diagnostics.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import l8_power_analysis as cpu

# Import, rather than duplicate, every simulation constant.  The CPU module is
# the scientific reference implementation for this proposal.
R_STAR = cpu.R_STAR
V_REF = cpu.V_REF
BETA_A = cpu.BETA_A
BETA_B = cpu.BETA_B
EPS = cpu.EPS_C
TAU_INIT = cpu.TAU_INIT
TAU_MIN = cpu.TAU_MIN
TAU_MAX = cpu.TAU_MAX
VAR_X = cpu.VAR_X

@dataclass(frozen=True)
class GpuCell:
    W:int; N_w:int; alpha:float; v_mult:float; c_min:float; eta:float; sigma_dose:float

def available() -> bool:
    return torch.cuda.is_available()


def _doses(device: torch.device) -> torch.Tensor:
    return torch.tensor([0.0, 1.0, 2.0, 3.0], device=device, dtype=torch.float64)

def _rho(means:torch.Tensor) -> torch.Tensor:
    """Ascending midrank Pearson rho; batch shape (..., 4)."""
    # Exact binary64 midranks: rank = 1 + count(lower) + (count(equal)-1)/2.
    lower=(means.unsqueeze(-1)>means.unsqueeze(-2)).sum(dim=-1,dtype=means.dtype)
    equal=(means.unsqueeze(-1)==means.unsqueeze(-2)).sum(dim=-1,dtype=means.dtype)
    ranks=1.0+lower+(equal-1.0)/2.0
    centered=ranks-ranks.mean(dim=-1,keepdim=True)
    denom=torch.sqrt((centered.square().mean(dim=-1))*VAR_X)
    doses = _doses(means.device)
    return (centered*(doses-doses.mean())).mean(dim=-1)/denom

def simulate_batch(cell:GpuCell, repetitions:int, seed:int) -> tuple[torch.Tensor,torch.Tensor]:
    """Return per-seed beta-star and rho: shape (repetitions, 5)."""
    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    if cell.N_w <= 1:
        raise ValueError("N_w must exceed one for the pooled standard deviation")
    if not available():
        raise RuntimeError("CUDA is unavailable")
    gen=torch.Generator(device="cuda"); gen.manual_seed(seed)
    shape=(repetitions,5)
    deviations=torch.empty((repetitions,5,4,cell.N_w),device="cuda",dtype=torch.float64)
    for dose in range(4):
        tau=torch.full(shape,TAU_INIT,device="cuda",dtype=torch.float64)
        for window in range(cell.N_w):
            beta_shape=shape+(cell.W,)
            a=torch.full(beta_shape,BETA_A,device="cuda",dtype=torch.float64)
            b=torch.full(beta_shape,BETA_B,device="cuda",dtype=torch.float64)
            ga=torch._standard_gamma(a,generator=gen)
            gb=torch._standard_gamma(b,generator=gen)
            p=(ga/(ga+gb)).clamp(EPS,1-EPS)
            correct=torch.rand(shape+(cell.W,),device="cuda",dtype=torch.float64,generator=gen)<p
            noise=torch.randn(shape+(cell.W,),device="cuda",dtype=torch.float64,generator=gen)
            conf=torch.sigmoid(torch.logit(p)+cell.alpha+noise*math.sqrt(cell.v_mult*V_REF)).clamp(EPS,1-EPS)
            if dose:
                conf=torch.sigmoid(torch.logit(conf)+torch.randn(shape+(cell.W,),device="cuda",dtype=torch.float64,generator=gen)*(dose*cell.sigma_dose)).clamp(EPS,1-EPS)
            threshold=conf>tau.unsqueeze(-1)
            floor=max(1,math.ceil(cell.c_min*cell.W))
            top=torch.topk(conf,floor,dim=-1).indices
            forced=torch.zeros_like(threshold).scatter_(-1,top,True)
            answered=threshold|forced
            risk=((~correct)&answered).sum(dim=-1,dtype=torch.float64)/answered.sum(dim=-1)
            deviations[:,:,dose,window]=risk-R_STAR
            tau=(tau+cell.eta*(risk-R_STAR)).clamp(TAU_MIN,TAU_MAX)
    means=deviations.mean(dim=-1)
    doses = _doses(means.device)
    beta=((means-means.mean(dim=-1,keepdim=True))*(doses-doses.mean())).mean(dim=-1)/VAR_X
    residual=deviations-means.unsqueeze(-1)
    sigma=torch.sqrt(residual.square().sum(dim=(-1,-2))/(4*(cell.N_w-1)))
    return beta/sigma,_rho(means)


def simulate_misspecified_batch(
    cell: GpuCell, repetitions: int, seed: int, profile_name: str
) -> tuple[torch.Tensor, torch.Tensor]:
    """CUDA equivalent of the CPU misspecification simulation."""
    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    if cell.N_w <= 1:
        raise ValueError("N_w must exceed one for the pooled standard deviation")
    if not available():
        raise RuntimeError("CUDA is unavailable")
    if profile_name not in {"uniform_difficulty", "bimodal_difficulty"}:
        raise ValueError(f"unknown misspecified profile: {profile_name}")

    gen = torch.Generator(device="cuda")
    gen.manual_seed(seed)
    shape = (repetitions, cpu.N_SEEDS)
    query_shape = shape + (cell.W,)
    if profile_name == "uniform_difficulty":
        p = torch.rand(query_shape, device="cuda", dtype=torch.float64, generator=gen)
    else:
        easy = torch.rand(query_shape, device="cuda", dtype=torch.float64, generator=gen) < 0.5
        p = torch.where(easy, 0.9, 0.3)
    correct = torch.rand(query_shape, device="cuda", dtype=torch.float64, generator=gen) < p
    noise = torch.randn(query_shape, device="cuda", dtype=torch.float64, generator=gen)
    # Preserve the legacy misspecification arm's logit expression exactly.
    logit_p = torch.log(p / (1.0 - p + EPS) + EPS)
    conf = torch.sigmoid(logit_p + cell.alpha + noise * math.sqrt(cell.v_mult * V_REF)).clamp(EPS, 1-EPS)

    tau = torch.full(shape, 0.5, device="cuda", dtype=torch.float64)
    deviations = torch.empty(shape + (4, cell.N_w), device="cuda", dtype=torch.float64)
    floor = max(1, math.ceil(cell.c_min * cell.W))
    for dose in range(4):
        for window in range(cell.N_w):
            if dose:
                dose_noise = torch.randn(query_shape, device="cuda", dtype=torch.float64, generator=gen)
                logit_c = torch.log(conf / (1.0 - conf + EPS) + EPS)
                dose_conf = torch.sigmoid(logit_c + dose_noise * (dose * cell.sigma_dose)).clamp(EPS, 1-EPS)
            else:
                dose_conf = conf
            threshold = dose_conf > tau.unsqueeze(-1)
            top = torch.topk(dose_conf, floor, dim=-1).indices
            forced = torch.zeros_like(threshold).scatter_(-1, top, True)
            answered = threshold | forced
            risk = ((~correct) & answered).sum(dim=-1, dtype=torch.float64) / answered.sum(dim=-1)
            deviations[:, :, dose, window] = risk - R_STAR
            tau = (tau + cell.eta * (risk - R_STAR)).clamp(0.01, 0.99)

    means = deviations.mean(dim=-1)
    doses = _doses(means.device)
    beta = ((means-means.mean(dim=-1, keepdim=True)) * (doses-doses.mean())).mean(dim=-1) / VAR_X
    residual = deviations - means.unsqueeze(-1)
    sigma = torch.sqrt(residual.square().sum(dim=(-1, -2)) / (4 * (cell.N_w - 1)))
    return beta / sigma, _rho(means)

def summary(cell:GpuCell,repetitions:int,seed:int) -> dict[str,float]:
    beta,rho=simulate_batch(cell,repetitions,seed)
    complete=((beta>=.2)&(rho>=.8)).all(dim=1)
    return {"repetitions":float(repetitions),"mean_beta_star":float(beta.mean().cpu()),
            "mean_rho":float(rho.mean().cpu()),"complete_verdict_false_kill_rate":float((~complete).double().mean().cpu())}

def calibrate(cell:GpuCell, seed:int, pilots:int=1000) -> float:
    """GPU counterpart of the baseline fixed-reference bisection calibration."""
    lo, hi = cpu.CAL_SIGMA_LO, cpu.CAL_SIGMA_HI
    def mean_at(sigma:float) -> float:
        trial=GpuCell(cell.W,cell.N_w,cell.alpha,cell.v_mult,cpu.CAL_REF_C_MIN,cpu.CAL_REF_ETA,sigma)
        beta,_=simulate_batch(trial,pilots,seed)
        return float(beta.mean().cpu())
    high=mean_at(hi)
    if high<cpu.TRUE_BETA_STAR: return hi
    low=mean_at(lo)
    if low>=cpu.TRUE_BETA_STAR: return lo
    for _ in range(cpu.CAL_MAX_ITERS):
        mid=(lo+hi)/2; value=mean_at(mid)
        if abs(value-cpu.TRUE_BETA_STAR)<cpu.CAL_TOL: return mid
        if value<cpu.TRUE_BETA_STAR: lo=mid
        else: hi=mid
    return (lo+hi)/2
