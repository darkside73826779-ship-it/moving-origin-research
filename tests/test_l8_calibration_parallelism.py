"""L8 calibration parallelism tests. Date: 2026-08-19; Regime B.

O-15 diagnostic-only, synthetic/candidate-blind, and authorizes no scoring.
"""

import io
import json
import pickle
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from diagnostics import l8_power_analysis as l8


HOSTILE = (
    "C:" + "\\" + "Users" + "\\private\\secret.txt " +
    "host-01 " + "S-" + "1-5-21-123 " +
    "person" + "@" + "example.test " +
    "ghp" + "_FAKE_TOKEN\nsecond line"
)


class FakePool:
    results = None
    error = None
    processes_seen = []

    def __init__(self, processes):
        self.processes = processes
        type(self).processes_seen.append(processes)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def map(self, function, items):
        if self.error is not None:
            raise self.error
        if self.results is not None:
            return self.results
        return [function(item) for item in items]


def canonical_items():
    return [(i, a, v) for i, (a, v) in enumerate(
            (a, v) for a in l8.ALPHAS for v in l8.V_MULTS)]


def canonical_results():
    return [{"ordinal": i, "alpha": a, "v_mult": v,
             "sigma_dose": float(i) / 10.0}
            for i, a, v in canonical_items()]


class CalibrationParallelismContractTest(unittest.TestCase):
    def setUp(self):
        FakePool.results = None
        FakePool.error = None
        FakePool.processes_seen = []

    def test_worker_error_pickle_round_trip(self):
        error = l8.CalibrationWorkerError(3, 0.02, 1.0, "ValueError")
        restored = pickle.loads(pickle.dumps(error))
        fields = ("ordinal", "alpha", "v_mult", "exception_type",
                  "exception_message")
        self.assertEqual(tuple(getattr(error, f) for f in fields),
                         tuple(getattr(restored, f) for f in fields))

    def test_worker_failure_identity_type_fixed_message_and_no_leak(self):
        def fail(alpha, v_mult):
            raise ValueError(HOSTILE)

        with patch.object(l8, "calibrate_sigma_dose", side_effect=fail):
            with self.assertRaises(l8.CalibrationWorkerError) as caught:
                l8._worker_calibration((7, 0.05, 2.0))
        error = caught.exception
        self.assertEqual((error.ordinal, error.alpha, error.v_mult),
                         (7, 0.05, 2.0))
        self.assertEqual(error.exception_type, "ValueError")
        self.assertEqual(error.exception_message, "calibration worker failed")
        self.assertNotIn(HOSTILE.encode(), pickle.dumps(error))

    def test_worker_failure_record_and_system_exit(self):
        FakePool.error = l8.CalibrationWorkerError(
            4, 0.02, 1.0, "RuntimeError")
        stderr, stdout = io.StringIO(), io.StringIO()
        with patch.object(l8.multiprocessing, "Pool", FakePool), \
             redirect_stderr(stderr), redirect_stdout(stdout):
            with self.assertRaises(SystemExit) as caught:
                l8._run_calibration_phase("reference", 4)
        self.assertEqual(caught.exception.code, 1)
        record = json.loads(stderr.getvalue())
        self.assertEqual(set(record), {
            "phase", "analysis_label", "ordinal", "alpha", "v_mult",
            "exception_type", "exception_message"})
        self.assertEqual(record["exception_message"], "calibration worker failed")
        self.assertNotIn(HOSTILE, stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        self.assertEqual(stdout.getvalue().count("[calibration:reference]"), 1)

    def test_no_simulation_dispatch_after_calibration_failure(self):
        FakePool.error = l8.CalibrationWorkerError(
            0, 0.0, 0.5, "RuntimeError")
        with patch.object(l8.multiprocessing, "Pool", FakePool), \
             patch.object(l8, "_worker_combo") as combo, \
             patch.object(l8, "_worker_null_control") as null, \
             redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):
                l8.run_power_analysis(1, workers=2)
        combo.assert_not_called()
        null.assert_not_called()

    def test_identity_error_pickle_round_trip(self):
        error = l8.CalibrationIdentityError(
            ["duplicate", "missing"], 15, 16, [[0.0, 0.5]])
        restored = pickle.loads(pickle.dumps(error))
        self.assertEqual(restored.mismatch_kinds, error.mismatch_kinds)
        self.assertEqual(restored.expected_count, error.expected_count)
        self.assertEqual(restored.seen_count, error.seen_count)
        self.assertEqual(restored.canonical_identities,
                         error.canonical_identities)
        self.assertEqual(restored.message,
                         "calibration identity validation failed")

    def test_duplicate_missing_unexpected_and_malformed_contracts(self):
        items = canonical_items()
        base = canonical_results()
        cases = [
            (base + [base[0]], ["duplicate"]),
            (base[:-1], ["missing"]),
            (base[:-1] + [{"alpha": 9.0, "v_mult": 9.0}],
             ["missing", "unexpected"]),
            (base[:-1] + [None], ["missing", "unexpected"]),
            (base[:-1] + [{"alpha": 0.0}], ["missing", "unexpected"]),
        ]
        for results, expected_kinds in cases:
            with self.subTest(expected_kinds=expected_kinds):
                with self.assertRaises(l8.CalibrationIdentityError) as caught:
                    l8._validate_calibration_identities(results, items)
                self.assertEqual(caught.exception.mismatch_kinds,
                                 expected_kinds)
                self.assertEqual(caught.exception.expected_count, len(items))
                self.assertEqual(caught.exception.seen_count, len(results))

    def test_identity_failure_record_and_system_exit(self):
        FakePool.results = canonical_results()[:-1]
        stderr = io.StringIO()
        with patch.object(l8.multiprocessing, "Pool", FakePool), \
             redirect_stderr(stderr), redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                l8._run_calibration_phase("misspec:uniform_difficulty", 4)
        self.assertEqual(caught.exception.code, 1)
        record = json.loads(stderr.getvalue())
        self.assertEqual(set(record), {
            "phase", "analysis_label", "message", "mismatch_kinds",
            "expected_count", "seen_count", "canonical_identities"})
        self.assertEqual(record["mismatch_kinds"], ["missing"])
        self.assertEqual(record["seen_count"], 14)

    def test_dispatch_once_consume_once_and_worker_cap(self):
        FakePool.results = canonical_results()
        with patch.object(l8.multiprocessing, "Pool", FakePool), \
             redirect_stdout(io.StringIO()):
            table = l8._run_calibration_phase("reference", 64)
        self.assertEqual(FakePool.processes_seen, [15])
        self.assertEqual(len(table), 15)
        self.assertEqual(set(table), {(a, v) for _, a, v in canonical_items()})


if __name__ == "__main__":
    unittest.main()
