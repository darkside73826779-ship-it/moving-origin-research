"""Multiprocessing remediation tests. Date: 2026-08-19; Regime B.

Diagnostic-only (O-15), synthetic/candidate-blind, and authorizes no scoring.
"""

import math
import unittest
from unittest.mock import patch

from diagnostics import l8_power_analysis as l8


COMPARISON_FIELDS = (
    "mean_beta_star",
    "false_kill_rate",
    "false_kill_rate_per_seed",
    "n_valid",
    "n_instrument_failures",
)


def normalized_metrics(result):
    rows = []
    for row in result["results"]:
        rows.append(tuple(
            "NaN" if isinstance(row[field], float) and math.isnan(row[field])
            else row[field]
            for field in COMPARISON_FIELDS
        ))
    return rows


class MultiprocessingReproducibilityTest(unittest.TestCase):
    def run_three_combos(self, runner, workers, **kwargs):
        with patch.object(l8, "ALPHAS", (0.0,)), \
             patch.object(l8, "V_MULTS", (0.5,)), \
             patch.object(l8, "C_MINS", (0.5, 0.6, 0.7)), \
             patch.object(l8, "ETAS", (0.01,)):
            return runner(n_sims=1, include_null_control=True,
                          progress_every=1000, workers=workers, **kwargs)

    def test_reference_consumed_output_is_identical(self):
        single = self.run_three_combos(l8.run_power_analysis, workers=1)
        multi = self.run_three_combos(l8.run_power_analysis, workers=2)
        print("reference single:", normalized_metrics(single))
        print("reference multi: ", normalized_metrics(multi))
        self.assertEqual(normalized_metrics(single), normalized_metrics(multi))

    def test_misspecified_consumed_output_is_identical(self):
        single = self.run_three_combos(
            l8.run_power_analysis_misspecified, workers=1,
            profile_name="uniform_difficulty")
        multi = self.run_three_combos(
            l8.run_power_analysis_misspecified, workers=2,
            profile_name="uniform_difficulty")
        print("misspecified single:", normalized_metrics(single))
        print("misspecified multi: ", normalized_metrics(multi))
        self.assertEqual(normalized_metrics(single), normalized_metrics(multi))


if __name__ == "__main__":
    unittest.main()
