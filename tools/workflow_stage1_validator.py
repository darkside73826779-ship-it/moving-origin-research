#!/usr/bin/env python3
"""Deterministic Stage-1 P1/P7 routing validator (Regime B, 2026-08-21)."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "specs/data/workflow_routing_table_v1.json"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def output_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _exact_keys(value: dict[str, Any], allowed: set[str]) -> bool:
    return set(value) == allowed


def validate_input(value: Any) -> None:
    if not isinstance(value, dict) or "action" not in value:
        raise ValueError("SCHEMA_INVALID")
    action = value["action"]
    if action == "ROUTE":
        if value.get("block") is True:
            if not _exact_keys(value, {"action", "block", "originating_role"}) or not isinstance(value["originating_role"], str):
                raise ValueError("SCHEMA_INVALID")
        elif "override" in value:
            if not _exact_keys(value, {"action", "override"}) or not isinstance(value["override"], dict):
                raise ValueError("SCHEMA_INVALID")
            override = value["override"]
            if not _exact_keys(override, {"ruling_path", "ruling_sha", "exact_route", "scope"}):
                raise ValueError("SCHEMA_INVALID")
            path = override["ruling_path"]
            if not isinstance(path, str) or path.startswith(('/', '\\')) or '\\' in path or '..' in path.split('/'):
                raise ValueError("SCHEMA_INVALID")
            if not isinstance(override["ruling_sha"], str) or not re.fullmatch(r"[0-9a-f]{40}", override["ruling_sha"]):
                raise ValueError("SCHEMA_INVALID")
            if not isinstance(override["exact_route"], list) or not override["exact_route"] or not all(isinstance(x, str) for x in override["exact_route"]):
                raise ValueError("SCHEMA_INVALID")
            if not isinstance(override["scope"], str) or not override["scope"]:
                raise ValueError("SCHEMA_INVALID")
        elif not _exact_keys(value, {"action", "deliverable"}) or value["deliverable"] not in {
            "specification", "mechanical_implementation", "state_event", "scoring"
        }:
            raise ValueError("SCHEMA_INVALID")
    elif action == "PARALLEL":
        required = {"action", "single_owner", "same_immutable_inputs", "disjoint_outputs", "no_output_dependency", "no_self_review", "no_scoring_or_protected_seeds", "declared_serial_commit_order"}
        if not _exact_keys(value, required):
            raise ValueError("SCHEMA_INVALID")
        if not all(isinstance(value[k], bool) for k in required - {"action", "declared_serial_commit_order"}):
            raise ValueError("SCHEMA_INVALID")
        order = value["declared_serial_commit_order"]
        if not isinstance(order, list) or not all(isinstance(x, str) for x in order):
            raise ValueError("SCHEMA_INVALID")
    elif action == "BATCH":
        if not _exact_keys(value, {"action", "events", "separate_state_hashes"}) or not isinstance(value["events"], list) or not isinstance(value["separate_state_hashes"], bool):
            raise ValueError("SCHEMA_INVALID")
        for event in value["events"]:
            if not isinstance(event, dict) or not _exact_keys(event, {"event_id", "kind", "authorized", "low_risk"}):
                raise ValueError("SCHEMA_INVALID")
            if not isinstance(event["event_id"], str) or not isinstance(event["kind"], str) or not isinstance(event["authorized"], bool) or not isinstance(event["low_risk"], bool):
                raise ValueError("SCHEMA_INVALID")
    else:
        raise ValueError("SCHEMA_INVALID")


def evaluate(value: dict[str, Any]) -> dict[str, Any]:
    validate_input(value)
    action = value["action"]
    if action == "ROUTE":
        if value.get("block") is True:
            return {"reason": "BLOCK_RETURN", "route": [value["originating_role"]], "status": "ALLOW"}
        if "override" in value:
            route = value["override"]["exact_route"]
            if "FRESH_CONTEXT_CRITIC" not in route or route[-1] != "REBECCA":
                return {"reason": "INVALID_OVERRIDE", "route": [], "status": "STOP"}
            return {"reason": "VALID_OVERRIDE", "route": route, "status": "ALLOW"}
        defaults = {
            "specification": ["ARCHITECT", "FRESH_CONTEXT_CRITIC", "REBECCA"],
            "mechanical_implementation": ["TASK_BUILDER", "FRESH_CONTEXT_CRITIC", "REBECCA"],
            "state_event": ["INTEGRATOR", "RECORDER", "REBECCA"],
            "scoring": ["REBECCA_EXECUTOR", "RECORDER_INTAKE", "JUDGE", "RECORDER_PUBLICATION", "REBECCA"],
        }
        return {"reason": "DEFAULT_ROUTE", "route": defaults[value["deliverable"]], "status": "ALLOW"}
    if action == "PARALLEL":
        checks = [
            ("single_owner", "MISSING_PREDICATE"),
            ("same_immutable_inputs", "MISSING_PREDICATE"),
            ("disjoint_outputs", "MISSING_PREDICATE"),
            ("no_output_dependency", "OUTPUT_DEPENDENCY"),
            ("no_self_review", "SELF_REVIEW"),
            ("no_scoring_or_protected_seeds", "SCORING_OR_SEEDS"),
        ]
        for key, reason in checks:
            if value[key] is not True:
                return {"reason": reason, "route": [], "status": "STOP"}
        order = value["declared_serial_commit_order"]
        if not order or len(set(order)) != len(order):
            return {"reason": "MISSING_COMMIT_ORDER", "route": [], "status": "STOP"}
        return {"reason": "PARALLEL_ALLOWED", "route": [], "status": "ALLOW"}
    events = value["events"]
    eligible = (
        len(events) >= 2
        and len({e["event_id"] for e in events}) == len(events)
        and all(e["kind"] in {"state", "custody"} and e["authorized"] and e["low_risk"] for e in events)
        and value["separate_state_hashes"]
    )
    if eligible:
        return {"reason": "BATCH_ALLOWED", "route": ["INTEGRATOR", "RECORDER", "REBECCA"], "status": "ALLOW"}
    return {"reason": "BATCH_INELIGIBLE", "route": [], "status": "STOP"}
