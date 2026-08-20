#!/usr/bin/env python3
"""L8 calibration parallelism check. Date: 2026-08-19; Regime B.

O-15 diagnostic-only, synthetic/candidate-blind, and authorizes no scoring.
"""

import copy
import json
import os
from unittest.mock import patch

from diagnostics import l8_power_analysis as l8


def artifact_bytes(result):
    normalized = copy.deepcopy(result)
    normalized["header"].pop("elapsed_seconds", None)
    return (json.dumps(l8._sanitize_nan(normalized), indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def main():
    workers = min(os.cpu_count() or 1, len(l8.ALPHAS) * len(l8.V_MULTS))
    print("L8 calibration parallelism check: O-15 diagnostic-only; no scoring",
          flush=True)
    serial_table = l8._run_calibration_phase("repro:serial", 1)
    parallel_table = l8._run_calibration_phase("repro:parallel", workers)
    calibration_equal = serial_table == parallel_table

    with patch.object(l8, "_run_calibration_phase", return_value=serial_table):
        serial_result = l8.run_power_analysis(
            n_sims=1, include_null_control=True, progress_every=1000,
            workers=1)
    with patch.object(l8, "_run_calibration_phase", return_value=parallel_table):
        parallel_result = l8.run_power_analysis(
            n_sims=1, include_null_control=True, progress_every=1000,
            workers=workers)

    artifact_equal = artifact_bytes(serial_result) == artifact_bytes(parallel_result)
    downstream_equal = l8._sanitize_nan({
        "results": serial_result["results"],
        "sensitivity_map": serial_result["sensitivity_map"],
        "selection": serial_result["selection"],
    }) == l8._sanitize_nan({
        "results": parallel_result["results"],
        "sensitivity_map": parallel_result["sensitivity_map"],
        "selection": parallel_result["selection"],
    })

    print("workers:", workers)
    print("serial_calibrations:", sorted(serial_table.items()))
    print("parallel_calibrations:", sorted(parallel_table.items()))
    print("calibration_value_equality:", calibration_equal)
    print("artifact_byte_identity_excluding_elapsed_seconds:", artifact_equal)
    print("downstream_scientific_equality:", downstream_equal)
    if not (calibration_equal and artifact_equal and downstream_equal):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
