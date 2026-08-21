#!/usr/bin/env python3
"""Fail-closed validators for approved workflow contracts (2026-08-21, Regime B)."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REPO_PATH = re.compile(r"^(?!/)(?![A-Za-z]:)(?!.*(?:^|/)\.\.(?:/|$))(?!.*//)(?!.*\\)[A-Za-z0-9._/-]+$")
ROLES = {"WORKFLOW_COORDINATOR", "ARCHITECT", "CRITIC", "TASK_BUILDER", "INTEGRATOR", "RECORDER", "JUDGE", "REBECCA"}


class ContractError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    """Canonical JSON for the contract's integer/string/bool/null domains."""
    def reject_float(item: Any) -> None:
        if isinstance(item, float):
            raise ContractError("FLOAT_NOT_ALLOWED")
        if isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise ContractError("NON_STRING_KEY")
                reject_float(child)
        elif isinstance(item, list):
            for child in item:
                reject_float(child)

    reject_float(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repository_bytes(repo_root: Path, path: str) -> bytes:
    """Read the exact staged Git blob, falling back to HEAD; never hash checkout line endings."""
    for object_name in (f":{path}", f"HEAD:{path}"):
        result = subprocess.run(
            ["git", "-C", str(repo_root), "show", object_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if result.returncode == 0:
            return result.stdout
    raise ContractError("REPOSITORY_BLOB_MISSING")


def _exact_keys(value: Any, required: set[str]) -> None:
    if not isinstance(value, dict) or set(value) != required:
        raise ContractError("KEY_SET_MISMATCH")


def _repo_path(value: Any) -> str:
    if not isinstance(value, str) or not REPO_PATH.fullmatch(value):
        raise ContractError("INVALID_REPOSITORY_PATH")
    return value


def _artifact_paths(value: Any, parent_key: str = "") -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"artifacts", "remote_ref", "work_branch"}:
                continue
            if key in {"path", "ruling_path", "source_trace_path", "specification_path"} and isinstance(child, str):
                yield _repo_path(child)
            elif key.endswith("_paths") and isinstance(child, list):
                for path in child:
                    yield _repo_path(path)
            else:
                yield from _artifact_paths(child, key)
    elif isinstance(value, list):
        for child in value:
            yield from _artifact_paths(child, parent_key)


def validate_handoff(value: Any, repo_root: Path | None = None) -> None:
    required = {
        "schema_version", "date", "regime", "transfer_kind", "work_item", "gate", "sender_role",
        "receiver_role", "authority_basis", "remote_ref", "base_sha", "routing_ref_sha",
        "review_result_sha", "work_branch", "artifacts", "checks_performed", "status", "findings",
        "scan_attestation", "next_event", "prohibited_actions", "role_extension",
    }
    _exact_keys(value, required)
    if value["schema_version"] != "common-handoff-manifest-v1" or value["regime"] != "B" or value["transfer_kind"] != "FORMAL_HANDOFF":
        raise ContractError("IDENTITY_MISMATCH")
    if value["sender_role"] not in ROLES or value["receiver_role"] not in ROLES:
        raise ContractError("ROLE_INVALID")
    for field in ("base_sha", "routing_ref_sha"):
        if not isinstance(value[field], str) or not SHA.fullmatch(value[field]):
            raise ContractError("SHA_INVALID")
    if value["review_result_sha"] is not None and not SHA.fullmatch(value["review_result_sha"]):
        raise ContractError("SHA_INVALID")
    extension = value["role_extension"]
    if not isinstance(extension, dict) or extension.get("role") != value["sender_role"]:
        raise ContractError("SENDER_EXTENSION_MISMATCH")
    artifacts = value["artifacts"]
    if not isinstance(artifacts, dict) or not artifacts:
        raise ContractError("ARTIFACT_INVENTORY_EMPTY")
    normalized = []
    for path, digest in artifacts.items():
        normalized.append(_repo_path(path))
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            raise ContractError("ARTIFACT_DIGEST_INVALID")
        if repo_root is not None:
            if sha256_bytes(repository_bytes(repo_root, path)) != digest:
                raise ContractError("ARTIFACT_BYTES_MISMATCH")
    if len(set(normalized)) != len(normalized):
        raise ContractError("ARTIFACT_PATH_DUPLICATE")
    named = set(_artifact_paths(value))
    if not named.issubset(set(artifacts)):
        raise ContractError("ARTIFACT_INVENTORY_INCOMPLETE")


def validate_trace(trace: Any) -> None:
    _exact_keys(trace, {"schema_version", "date", "regime", "specification_path", "specification_sha", "rows"})
    if trace["schema_version"] != "executability-trace-v1" or trace["regime"] != "B" or not SHA.fullmatch(trace["specification_sha"]):
        raise ContractError("TRACE_IDENTITY_INVALID")
    rows = trace["rows"]
    if not isinstance(rows, list) or not rows:
        raise ContractError("TRACE_EMPTY")
    ids = []
    verification_ids: set[str] = set()
    required = {
        "input_id", "kind", "repository_path", "producer_role", "consumer_roles",
        "exact_value_or_schema_source", "canonicalization", "expected_sha256", "creation_phase", "status",
        "architect_verification_id", "critic_verification_id", "taskbuilder_verification_id", "failure_disposition",
    }
    for row in rows:
        _exact_keys(row, required)
        ids.append(row["input_id"])
        _repo_path(row["repository_path"])
        expected = row["expected_sha256"]
        if expected != "not_applicable" and (not isinstance(expected, str) or not SHA256.fullmatch(expected)):
            raise ContractError("TRACE_DIGEST_INVALID")
        for key in ("architect_verification_id", "critic_verification_id", "taskbuilder_verification_id"):
            value = row[key]
            if not isinstance(value, str) or not value or value in verification_ids:
                raise ContractError("TRACE_VERIFICATION_ID_INVALID")
            verification_ids.add(value)
    if len(ids) != len(set(ids)):
        raise ContractError("TRACE_INPUT_ID_DUPLICATE")


def validate_disposition(disposition: Any, trace: Any, trace_bytes: bytes) -> None:
    validate_trace(trace)
    required = {"schema_version", "date", "regime", "reviewer_role", "source_trace_path", "source_trace_sha256", "source_specification_sha", "rows", "overall_disposition"}
    _exact_keys(disposition, required)
    role = disposition["reviewer_role"]
    if disposition["schema_version"] != "executability-trace-disposition-v1" or disposition["regime"] != "B" or role not in {"CRITIC", "TASK_BUILDER"}:
        raise ContractError("DISPOSITION_IDENTITY_INVALID")
    if disposition["source_trace_sha256"] != sha256_bytes(trace_bytes) or disposition["source_specification_sha"] != trace["specification_sha"]:
        raise ContractError("DISPOSITION_SOURCE_MISMATCH")
    rows = disposition["rows"]
    if len(rows) != len(trace["rows"]):
        raise ContractError("DISPOSITION_ROW_COUNT_MISMATCH")
    any_blocked = False
    id_key = "critic_verification_id" if role == "CRITIC" else "taskbuilder_verification_id"
    for source, result in zip(trace["rows"], rows):
        _exact_keys(result, {"input_id", "source_row_sha256", "verification_id", "disposition", "evidence_paths", "finding"})
        if result["input_id"] != source["input_id"] or result["source_row_sha256"] != sha256_bytes(canonical_bytes(source)) or result["verification_id"] != source[id_key]:
            raise ContractError("DISPOSITION_ROW_BINDING_MISMATCH")
        any_blocked |= result["disposition"] == "BLOCKED"
        if result["disposition"] == "BLOCKED" and not result["finding"]:
            raise ContractError("BLOCKED_FINDING_MISSING")
    expected = "BLOCKED" if any_blocked else "VERIFIED"
    if disposition["overall_disposition"] != expected:
        raise ContractError("OVERALL_DISPOSITION_MISMATCH")


def validate_metadata(value: Any, repo_root: Path | None = None) -> None:
    required = {"schema_version", "as_of_utc", "source_commit", "document_path", "document_sha256", "supersedes_metadata_sha256", "status", "document_role", "owner_role"}
    _exact_keys(value, required)
    if value["schema_version"] != "workflow-state-metadata-v1" or not SHA.fullmatch(value["source_commit"]):
        raise ContractError("METADATA_IDENTITY_INVALID")
    path = _repo_path(value["document_path"])
    owner_for_role = {"routing": "WORKFLOW_COORDINATOR", "checkpoint": "WORKFLOW_COORDINATOR", "durable_state": "INTEGRATOR", "custody_history": "RECORDER"}
    if owner_for_role.get(value["document_role"]) != value["owner_role"]:
        raise ContractError("METADATA_OWNER_MISMATCH")
    if not SHA256.fullmatch(value["document_sha256"]):
        raise ContractError("METADATA_DIGEST_INVALID")
    if repo_root is not None:
        if sha256_bytes(repository_bytes(repo_root, path)) != value["document_sha256"]:
            raise ContractError("METADATA_DOCUMENT_MISMATCH")


def validate_judge_envelope(value: Any) -> bytes:
    required = {"schema_version", "filename", "media_type", "encoding", "byte_length", "sha256", "content_base64"}
    _exact_keys(value, required)
    if value["schema_version"] != "judge-custody-envelope-v1" or value["media_type"] != "text/markdown; charset=utf-8" or value["encoding"] != "base64-rfc4648-no-whitespace":
        raise ContractError("JUDGE_ENVELOPE_IDENTITY_INVALID")
    encoded = value["content_base64"]
    if not isinstance(encoded, str) or re.search(r"\s", encoded):
        raise ContractError("JUDGE_BASE64_INVALID")
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ContractError("JUDGE_BASE64_INVALID") from exc
    if len(raw) != value["byte_length"] or sha256_bytes(raw) != value["sha256"]:
        raise ContractError("JUDGE_ENVELOPE_DIGEST_MISMATCH")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise ContractError("JUDGE_TEXT_ENCODING_INVALID")
    raw.decode("utf-8", errors="strict")
    return raw


def rollback_cascade(target: str, contract: Any) -> list[str]:
    stages = contract.get("stages") if isinstance(contract, dict) else None
    if not isinstance(stages, list):
        raise ContractError("ROLLBACK_CONTRACT_INVALID")
    dependencies = {row["stage"]: set(row["depends_on"]) for row in stages}
    if target not in dependencies:
        raise ContractError("ROLLBACK_TARGET_INVALID")
    result = {target}
    changed = True
    while changed:
        changed = False
        for stage, parents in dependencies.items():
            if stage not in result and parents & result:
                result.add(stage)
                changed = True
    order = [row["stage"] for row in stages]
    return [stage for stage in order if stage in result]


def _load(path: Path) -> tuple[Any, bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ContractError("BOM_FORBIDDEN")
    return json.loads(raw.decode("utf-8")), raw


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("handoff", "trace", "metadata", "judge-envelope"):
        item = sub.add_parser(name)
        item.add_argument("json_path", type=Path)
        item.add_argument("--repo-root", type=Path, default=ROOT)
    disposition = sub.add_parser("disposition")
    disposition.add_argument("json_path", type=Path)
    disposition.add_argument("--trace", required=True, type=Path)
    rollback = sub.add_parser("rollback-cascade")
    rollback.add_argument("stage")
    rollback.add_argument("--contract", type=Path, default=ROOT / "specs/data/workflow_stage_rollback_v1.json")
    args = parser.parse_args()
    try:
        if args.command == "rollback-cascade":
            contract, _ = _load(args.contract)
            print(json.dumps(rollback_cascade(args.stage, contract), separators=(",", ":")))
            return 0
        value, raw = _load(args.json_path)
        if args.command == "handoff":
            validate_handoff(value, args.repo_root)
        elif args.command == "trace":
            validate_trace(value)
        elif args.command == "metadata":
            validate_metadata(value, args.repo_root)
        elif args.command == "judge-envelope":
            validate_judge_envelope(value)
        else:
            trace, trace_raw = _load(args.trace)
            validate_disposition(value, trace, trace_raw)
    except (ContractError, json.JSONDecodeError, OSError) as exc:
        print(f"BLOCKED: {exc}")
        return 2
    print("VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
