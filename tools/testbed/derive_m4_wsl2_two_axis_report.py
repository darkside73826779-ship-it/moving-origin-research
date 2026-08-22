#!/usr/bin/env python3
"""Derive a non-scoring two-axis projection from a retained v1 probe report.

Date: 2026-08-22
Regime: B
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

STRUCTURAL_FAILURES = {
    "ACTIVE_DURATION_TOO_SHORT", "CLEANUP_INCOMPLETE", "EXECUTIONS_DID_NOT_OVERLAP",
    "FIFO_ORDER_MISMATCH", "GPU_TELEMETRY_UNAVAILABLE", "INTERNAL_PROBE_FAILURE",
    "MODEL_FILE_IDENTITY_MISMATCH", "MODEL_FILE_UNREADABLE", "MODEL_ROOT_IDENTITY_MISMATCH",
    "MODEL_ROOT_MISSING", "MODEL_ROOT_UNREADABLE", "MODEL_ROOTS_NOT_DISTINCT",
    "NO_BACKPRESSURE_OBSERVED", "PRODUCER_FAILURE", "SUPERVISOR_TIMEOUT",
    "WINDOW_DROPPED", "WINDOW_COUNT_MISMATCH",
}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def derive(raw: bytes) -> dict:
    source = json.loads(raw)
    windows = source["windows"]
    mismatch = [row["ordinal"] for row in windows if not row["outputs_agree"]]
    compared = len(windows)
    agreement = compared - len(mismatch)
    structural_failures = sorted(set(source["failure_codes"]) & STRUCTURAL_FAILURES)
    run = source["run"]
    structural_ok = not structural_failures and compared > 0 and all((
        run["active_duration_ns"] >= source["controls"]["active_duration_ns"],
        run["windows_produced"] == run["windows_consumed"] == compared,
        run["dropped_windows"] == 0,
        run["order_preserved"], run["all_executions_overlap"],
        run["producer_backpressure_observed"], run["cleanup_gpu_used_mib"] == 0,
    ))
    replica = "NOT_RUN" if compared == 0 else ("MATCH" if not mismatch else "MISMATCH")
    return {
        "schema_version": "m4-wsl2-dual-model-probe-two-axis-report-v2",
        "date": "2026-08-22", "regime": "B", "synthetic_only": True,
        "authoritative_scoring": False, "scientific_evidence": False,
        "qualification_evidence": False,
        "source_v1": {"sha256": hashlib.sha256(raw).hexdigest(), "status": source["status"],
                      "failure_codes": source["failure_codes"]},
        "structural_status": "PASS" if structural_ok else "BLOCKED",
        "structural_failure_codes": structural_failures,
        "replica_consistency_status": replica,
        "replica_consistency": {"compared_count": compared, "agreement_count": agreement,
                                "mismatch_count": len(mismatch), "mismatch_ordinals": mismatch,
                                "mismatch_ordinals_sha256": hashlib.sha256(canonical(mismatch)).hexdigest()},
        "consumer_rule": "BYTE_IDENTICAL_REPLICA_CONSUMER_MUST_STOP_ON_MISMATCH",
    }


def main(source_path: str, output_path: str) -> None:
    raw = Path(source_path).read_bytes()
    output = Path(output_path)
    output.write_bytes(canonical(derive(raw)) + b"\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()
    main(args.source, args.output)
