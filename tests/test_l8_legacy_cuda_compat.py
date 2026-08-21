import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))
import l8_gpu_adoption as gpu
import l8_legacy_cuda_compat as compat


@pytest.mark.parametrize("alpha,v_mult,c_min,eta,sigma", [
    (0.0, 0.5, 0.5, 0.01, 1.3125890624999998),
    (0.1, 1.0, 0.7, 0.1, 3.000075),
    (0.2, 2.0, 0.8, 0.2, 12.0),
])
@pytest.mark.parametrize("arm_ordinal", [0, 1])
def test_legacy_full_dimension_paired_block(alpha, v_mult, c_min, eta,
                                             sigma, arm_ordinal):
    if gpu.torch is None or not gpu.torch.cuda.is_available():
        pytest.skip("required CUDA runtime unavailable")
    arm_sigma = sigma if arm_ordinal == 0 else 0.0
    tape = compat.make_legacy_tape((0, arm_ordinal, 0, 32, alpha, v_mult,
                                    c_min, eta, arm_sigma))
    expected = compat.evaluate_legacy_tape_cpu(tape)
    observed = compat.evaluate_legacy_tape_gpu(tape)
    assert np.array_equal(expected["d_seed"], observed["d_seed"])
    assert np.array_equal(expected["invalid"], observed["invalid"])
    valid = ~expected["invalid"]
    assert np.max(np.abs(expected["beta"][valid] - observed["beta"][valid]),
                  initial=0.0) <= 1e-12
    assert np.array_equal(expected["beta"][valid] < 0.2,
                          observed["beta"][valid] < 0.2)
