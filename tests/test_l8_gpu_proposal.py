import sys
from pathlib import Path

import pytest


torch = pytest.importorskip("torch")
sys.path.insert(0, str(Path(__file__).parents[1] / "diagnostics"))
import l8_gpu_proposal as subject
import l8_power_analysis as cpu


def test_gpu_uses_cpu_reference_constants():
    assert subject.R_STAR == cpu.R_STAR
    assert subject.V_REF == cpu.V_REF
    assert subject.BETA_A == cpu.BETA_A
    assert subject.BETA_B == cpu.BETA_B
    assert subject.TAU_INIT == cpu.TAU_INIT


def test_rho_matches_cpu_reference_for_ties_when_cuda_available():
    if not subject.available():
        pytest.skip("CUDA unavailable")
    values = torch.tensor([[0.0, 0.0, 2.0, 3.0]], device="cuda", dtype=torch.float64)
    actual = float(subject._rho(values).cpu()[0])
    # The approved CPU direct-rho implementation uses exact equality ties.
    from l8_g2g4_minimal_full_screen import rho_from_dose_means
    assert actual == pytest.approx(rho_from_dose_means(values.cpu().numpy()[0]), abs=1e-15)


def test_fixed_seed_replay_when_cuda_available():
    if not subject.available():
        pytest.skip("CUDA unavailable")
    cell = subject.GpuCell(50, 4, 0.05, 1.0, 0.7, 0.1, 1.0)
    first = subject.summary(cell, repetitions=4, seed=101)
    second = subject.summary(cell, repetitions=4, seed=101)
    assert first == second
