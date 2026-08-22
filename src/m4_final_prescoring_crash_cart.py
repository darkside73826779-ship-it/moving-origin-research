"""Fail-closed, non-executing M4 crash-cart beta planning seam.

This module deliberately contains no model, tokenizer, subprocess, OCI, WSL, or
filesystem-custody access.  It produces only deterministic public planning and
validation data; a later reviewed release must supply every runtime identity.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

WARMUP_PAYLOADS = (0, 32, 512, 1024)
WARMUP_MAX_TOKENS = (8, 16, 16, 32)
WARMUP_DIGESTS = (
    "eabe6b7c5cf863599f9444019b68e0e56dde640b824bfb30756aad9faa093485",
    "6b5697332c8ad2d6520655f4dc94133a1c17d4d228e3143f5f9bc80d685a04b4",
    "763187d517d8b35871bc5bb6a5c41df5283fd18f0589348eb299f2d2911076db",
    "5646b4c97252d178f3c73ccd8a2ef988674c7b3f515beb64376d4ea7ab60dd13",
)
WARMUP_BYTES = (89, 122, 603, 1116)
FIXTURE_SIZES = (0, 32, 64, 128, 256, 512, 768, 1024)
LAW_ORDER = ("L7", "L8", "L10", "L14", "L18")
HELD_REASONS = {"L7":"SCORING_UNAUTHORIZED", "L8":"L8_PREREQUISITE_UNCLEARED", "L10":"SCORING_UNAUTHORIZED", "L14":"SCORING_UNAUTHORIZED", "L18":"EF3_ABSENT"}

class CrashCartError(RuntimeError):
    pass

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def warmup_prompt(ordinal: int, payload_bytes: int) -> bytes:
    if type(ordinal) is not int or ordinal < 0 or ordinal > 3 or payload_bytes != WARMUP_PAYLOADS[ordinal]:
        raise CrashCartError("WARMUP_CONTRACT_MISMATCH")
    text = ("M4_WARMUP_PUBLIC_V1\n"
            f"ordinal={ordinal:04d}\n"
            f"payload_bytes={payload_bytes}\n"
            f"payload={'x' * payload_bytes}\n"
            "Respond with the ordinal only.\n")
    raw = text.encode("utf-8")
    if raw.count(b"\n") != 5 or b"\\n" in raw or len(raw) != WARMUP_BYTES[ordinal] or sha256(raw) != WARMUP_DIGESTS[ordinal]:
        raise CrashCartError("WARMUP_CONTRACT_MISMATCH")
    return raw

def warmup_plan() -> tuple[Mapping[str, Any], ...]:
    return tuple({"ordinal": i, "prompt": warmup_prompt(i, n), "prompt_sha256": WARMUP_DIGESTS[i],
                  "max_output_tokens": WARMUP_MAX_TOKENS[i], "temperature": 0, "seed": 0,
                  "prefix_caching": False} for i, n in enumerate(WARMUP_PAYLOADS))

def active_schedule() -> tuple[int, ...]:
    return tuple(0 if i < 16 else (i - 15) * 625_000_000 for i in range(64))

def public_fixture(ordinal: int) -> Mapping[str, Any]:
    if type(ordinal) is not int or not 0 <= ordinal < 64: raise CrashCartError("ACTIVE_ORDINAL_INVALID")
    family = ordinal % 8; repetition = ordinal // 8; size = FIXTURE_SIZES[family]
    text = f"M4_CRASH_CART_PUBLIC_V1\nordinal={ordinal:04d}\nfamily={family}\nrepetition={repetition}\npayload={'x'*size}\n"
    raw = text.encode("ascii")
    return {"ordinal": ordinal, "fixture_id": f"family-{family}-repeat-{repetition}", "payload_bytes": size,
            "public_prompt_text": text, "prompt_sha256": sha256(raw)}

def held_laws() -> tuple[Mapping[str, Any], ...]:
    return tuple({"law_id": law, "status": "HELD", "claim_made": False,
                  "meaning_source": f"docs/ARCHITECTURAL_CONSTITUTION_v2.md:{line}", "evidence": [],
                  "metrics": {}, "failure_code": None, "held_reason": HELD_REASONS[law]}
                 for law, line in zip(LAW_ORDER, (26, 28, 32, 42, 54)))

def validate_terminal(report: Mapping[str, Any]) -> None:
    """Semantic guard for the five-stage public report representation."""
    stage = report.get("evidence_stage")
    allowed = {"PRE_ACTIVE_TERMINAL", "PARTIAL_WARMUP_TERMINAL", "PARTIAL_ACTIVE_TERMINAL", "POST_ACTIVE_TERMINAL", "COMPLETE_ACTIVE_TERMINAL"}
    if stage not in allowed: raise CrashCartError("EVIDENCE_STAGE_INVALID")
    rows = report.get("rows", []); warmup = report.get("warmup"); active = report.get("active_window")
    if stage == "PRE_ACTIVE_TERMINAL" and (warmup is not None or active is not None or rows): raise CrashCartError("FABRICATED_LATER_STAGE_EVIDENCE")
    if stage == "PARTIAL_WARMUP_TERMINAL" and (active is not None or rows): raise CrashCartError("FABRICATED_LATER_STAGE_EVIDENCE")
    if stage in {"POST_ACTIVE_TERMINAL", "COMPLETE_ACTIVE_TERMINAL"}:
        if not isinstance(warmup, Mapping) or warmup.get("status") != "PASS" or len(rows) != 64: raise CrashCartError("COMPLETE_EVIDENCE_MISSING")
        if not isinstance(active, Mapping) or active.get("attempted_pair_count") != 64: raise CrashCartError("COMPLETE_EVIDENCE_MISSING")
    if stage == "COMPLETE_ACTIVE_TERMINAL":
        if report.get("structural_status") != "PASS" or report.get("failure") is not None or report.get("failure_stage") is not None:
            raise CrashCartError("COMPLETE_TERMINAL_INVALID")
    else:
        if not isinstance(report.get("failure"), Mapping) or report["failure"].get("retry_count") != 0:
            raise CrashCartError("FAILURE_PROJECTION_INVALID")

def exact_replica_consumer_stop(replica: Mapping[str, Any]) -> None:
    if replica.get("status") == "MISMATCH":
        raise CrashCartError("EXACT_REPLICA_CONSUMER_STOP")

def execution_guard(run_authorized: bool) -> None:
    if run_authorized is not False: raise CrashCartError("RUN_AUTHORITY_INVALID")
    raise CrashCartError("RUN_AUTHORITY_ABSENT")
