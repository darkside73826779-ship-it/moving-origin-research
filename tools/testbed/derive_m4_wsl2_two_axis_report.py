#!/usr/bin/env python3
"""Derive a non-scoring two-axis projection from a retained v1 probe report.

Date: 2026-08-22
Regime: B
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
V1_SCHEMA = ROOT / "specs/data/m4_wsl2_dual_model_probe_report_schema_v1.json"
V2_SCHEMA = ROOT / "specs/data/m4_wsl2_dual_model_probe_two_axis_report_schema_v2.json"
V1_FAILURE_CODES = {
    "ACTIVE_DURATION_SHORT", "CHILD_PROCESS_FAILURE", "CLEANUP_VRAM_NONZERO",
    "DROPPED_WINDOWS", "EXECUTIONS_DID_NOT_OVERLAP",
    "FIFO_ORDER_MISMATCH", "GPU_TELEMETRY_UNAVAILABLE", "INTERNAL_PROBE_FAILURE",
    "MODEL_FILE_IDENTITY_MISMATCH", "MODEL_FILE_UNREADABLE", "MODEL_ROOT_IDENTITY_MISMATCH",
    "MODEL_ROOT_MISSING", "MODEL_ROOT_UNREADABLE", "MODEL_ROOTS_NOT_DISTINCT",
    "NO_BACKPRESSURE_OBSERVED", "PRODUCER_FAILURE", "SUPERVISOR_TIMEOUT",
    "SYNTHETIC_FIXTURE_ONLY", "OUTPUT_DIGEST_MISMATCH",
}
REPLICA_FAILURE_CODES = {"OUTPUT_DIGEST_MISMATCH"}
STRUCTURAL_FAILURE_CODES = V1_FAILURE_CODES - REPLICA_FAILURE_CODES


class ReplicaConsistencyStop(RuntimeError):
    """Mandatory fail-closed stop for an exact-replica consumer."""


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_v1(source: object) -> dict:
    jsonschema.Draft202012Validator(_load_schema(V1_SCHEMA)).validate(source)
    if not isinstance(source, dict):
        raise ValueError("V1_REPORT_NOT_OBJECT")
    unknown = set(source["failure_codes"]) - V1_FAILURE_CODES
    if unknown:
        raise ValueError("V1_FAILURE_CODE_UNKNOWN")
    return source


def _project(source: dict, raw: bytes) -> dict:
    windows = source["windows"]
    mismatch = [row["ordinal"] for row in windows if not row["outputs_agree"]]
    compared = len(windows)
    agreement = compared - len(mismatch)
    structural_failures = set(source["failure_codes"]) & STRUCTURAL_FAILURE_CODES
    run = source["run"]
    if run["active_duration_ns"] < source["controls"]["active_duration_ns"]:
        structural_failures.add("ACTIVE_DURATION_SHORT")
    if run["windows_produced"] != run["windows_consumed"] or run["windows_consumed"] != compared:
        structural_failures.add("DROPPED_WINDOWS")
    if run["dropped_windows"] != 0:
        structural_failures.add("DROPPED_WINDOWS")
    if not run["order_preserved"] or any(not row["order_preserved"] for row in windows):
        structural_failures.add("FIFO_ORDER_MISMATCH")
    if not run["all_executions_overlap"] or any(not row["execution_overlapped"] for row in windows):
        structural_failures.add("EXECUTIONS_DID_NOT_OVERLAP")
    if not run["producer_backpressure_observed"]:
        structural_failures.add("NO_BACKPRESSURE_OBSERVED")
    if run["cleanup_gpu_used_mib"] != 0:
        structural_failures.add("CLEANUP_VRAM_NONZERO")
    if compared == 0:
        structural_failures.add("SYNTHETIC_FIXTURE_ONLY")
    structural_failures = sorted(structural_failures)
    structural_ok = not structural_failures
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


def validate_projection(report: object, source_raw: bytes | None = None) -> dict:
    """Validate schema plus all cross-field and optional source-binding invariants."""
    jsonschema.Draft202012Validator(_load_schema(V2_SCHEMA)).validate(report)
    if not isinstance(report, dict):
        raise ValueError("V2_REPORT_NOT_OBJECT")
    consistency = report["replica_consistency"]
    compared = consistency["compared_count"]
    agreement = consistency["agreement_count"]
    mismatch = consistency["mismatch_count"]
    ordinals = consistency["mismatch_ordinals"]
    if agreement + mismatch != compared:
        raise ValueError("REPLICA_COUNT_ARITHMETIC_INVALID")
    if len(ordinals) != mismatch or ordinals != sorted(set(ordinals)):
        raise ValueError("MISMATCH_ORDINALS_INVALID")
    if any(ordinal >= compared for ordinal in ordinals):
        raise ValueError("MISMATCH_ORDINAL_OUT_OF_RANGE")
    if consistency["mismatch_ordinals_sha256"] != hashlib.sha256(canonical(ordinals)).hexdigest():
        raise ValueError("MISMATCH_ORDINAL_DIGEST_INVALID")
    status = report["replica_consistency_status"]
    expected_status = "NOT_RUN" if compared == 0 else ("MATCH" if mismatch == 0 else "MISMATCH")
    if status != expected_status:
        raise ValueError("REPLICA_STATUS_INVALID")
    failures = report["structural_failure_codes"]
    if failures != sorted(set(failures)):
        raise ValueError("STRUCTURAL_FAILURES_NOT_CANONICAL")
    expected_structural = "PASS" if not failures else "BLOCKED"
    if report["structural_status"] != expected_structural:
        raise ValueError("STRUCTURAL_STATUS_INVALID")
    if source_raw is not None:
        source = _validate_v1(json.loads(source_raw))
        if report != _project(source, source_raw):
            raise ValueError("SOURCE_BINDING_MISMATCH")
    return report


def require_replica_match(report: object, *, exact_replicas_required: bool) -> str:
    """Return PROCEED or raise the mandatory STOP for exact-replica consumers."""
    validated = validate_projection(report)
    if exact_replicas_required and validated["replica_consistency_status"] != "MATCH":
        raise ReplicaConsistencyStop("REPLICA_CONSISTENCY_STOP")
    return "PROCEED"


def derive(raw: bytes) -> dict:
    source = _validate_v1(json.loads(raw))
    report = _project(source, raw)
    return validate_projection(report, raw)


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
