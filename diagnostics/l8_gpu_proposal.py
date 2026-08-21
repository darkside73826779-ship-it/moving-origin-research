"""PROPOSED, non-scoring CUDA path for L8 statistical-equivalence review.

Uses float64 tensors for simulation state and estimator reductions.  It is not
bitwise equivalent to NumPy: CUDA random streams differ.  No full screen is
enabled here; the only public entry point runs bounded equivalence diagnostics.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import torch

R_STAR=.1; V_REF=1.0; BETA_A=8.0; BETA_B=2.0; EPS=1e-6
TAU_INIT=.5; TAU_MIN=.05; TAU_MAX=.95
X=torch.tensor([0.,1.,2.,3.],device="cuda",dtype=torch.float64)
VAR_X=1.25

@dataclass(frozen=True)
class GpuCell:
    W:int; N_w:int; alpha:float; v_mult:float; c_min:float; eta:float; sigma_dose:float

def available() -> bool:
    return torch.cuda.is_available() and torch.cuda.get_device_capability(0) >= (12,0)

def _rho(means:torch.Tensor) -> torch.Tensor:
    """Ascending midrank Pearson rho; batch shape (..., 4)."""
    # No ties occur with probability one in the synthetic continuous path.
    order=torch.argsort(means,dim=-1,stable=True)
    ranks=torch.empty_like(means)
    ranks.scatter_(-1,order,torch.arange(1,5,device=means.device,dtype=means.dtype).expand_as(means))
    centered=ranks-ranks.mean(dim=-1,keepdim=True)
    denom=torch.sqrt((centered.square().mean(dim=-1))*VAR_X)
    return (centered*(X-X.mean())).mean(dim=-1)/denom

def simulate_batch(cell:GpuCell, repetitions:int, seed:int) -> tuple[torch.Tensor,torch.Tensor]:
    """Return per-seed beta-star and rho: shape (repetitions, 5)."""
    if not available(): raise RuntimeError("CUDA RTX 50-class path unavailable")
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
    beta=((means-means.mean(dim=-1,keepdim=True))*(X-X.mean())).mean(dim=-1)/VAR_X
    residual=deviations-means.unsqueeze(-1)
    sigma=torch.sqrt(residual.square().sum(dim=(-1,-2))/(4*(cell.N_w-1)))
    return beta/sigma,_rho(means)

def summary(cell:GpuCell,repetitions:int,seed:int) -> dict[str,float]:
    beta,rho=simulate_batch(cell,repetitions,seed)
    complete=((beta>=.2)&(rho>=.8)).all(dim=1)
    return {"repetitions":float(repetitions),"mean_beta_star":float(beta.mean().cpu()),
            "mean_rho":float(rho.mean().cpu()),"complete_verdict_false_kill_rate":float((~complete).double().mean().cpu())}
