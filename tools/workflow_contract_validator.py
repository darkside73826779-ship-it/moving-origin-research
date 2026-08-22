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
from datetime import date
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
UTC_SECOND = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
WORK_ITEM = re.compile(r"^[a-z0-9][a-z0-9_-]{2,79}$")
JUDGE_FILENAME = re.compile(r"^[a-z0-9][a-z0-9_-]{2,79}\.md$")
REMOTE_REF = re.compile(r"refs/heads/[A-Za-z0-9._/-]+")
WORK_BRANCH = re.compile(r"(?!-)(?!.*(?:^|/)\.\.?($|/))[A-Za-z0-9._/-]+")
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


def repository_bytes_at(repo_root: Path, commit: str, path: str) -> bytes:
    """Read an exact committed blob; metadata may never bind mutable checkout bytes."""
    commit_check = subprocess.run(
        ["git", "-C", str(repo_root), "cat-file", "-e", f"{commit}^{{commit}}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if commit_check.returncode != 0:
        raise ContractError("METADATA_SOURCE_COMMIT_MISSING")
    result = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{commit}:{path}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ContractError("METADATA_SOURCE_BLOB_MISSING")
    return result.stdout


def _exact_keys(value: Any, required: set[str]) -> None:
    if not isinstance(value, dict) or set(value) != required:
        raise ContractError("KEY_SET_MISMATCH")


def _repo_path(value: Any) -> str:
    if not isinstance(value, str) or not REPO_PATH.fullmatch(value):
        raise ContractError("INVALID_REPOSITORY_PATH")
    return value


def _nonempty_string(value: Any, error: str = "STRING_INVALID") -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(error)
    return value


def _enum_value(value: Any, allowed: set[str], error: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise ContractError(error)
    return value


def _string_list(value: Any, *, nonempty: bool = False, error: str = "STRING_LIST_INVALID") -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        raise ContractError(error)
    if any(not isinstance(item, str) or not item for item in value):
        raise ContractError(error)
    return value


def _date(value: Any) -> None:
    if not isinstance(value, str):
        raise ContractError("DATE_INVALID")
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError
    except ValueError as exc:
        raise ContractError("DATE_INVALID") from exc


def _remote_ref(value: Any) -> None:
    if not isinstance(value, str) or not REMOTE_REF.fullmatch(value) or ".." in value.split("/"):
        raise ContractError("REMOTE_REF_INVALID")


def _work_branch(value: Any) -> None:
    if (not isinstance(value, str) or not WORK_BRANCH.fullmatch(value)
            or value.endswith((".", "/")) or ".." in value):
        raise ContractError("WORK_BRANCH_INVALID")


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
    _date(value["date"])
    if not isinstance(value["work_item"], str) or not WORK_ITEM.fullmatch(value["work_item"]):
        raise ContractError("WORK_ITEM_INVALID")
    _nonempty_string(value["gate"], "GATE_INVALID")
    if (not isinstance(value["sender_role"], str) or value["sender_role"] not in ROLES
            or not isinstance(value["receiver_role"], str) or value["receiver_role"] not in ROLES):
        raise ContractError("ROLE_INVALID")
    authority = value["authority_basis"]
    if not isinstance(authority, list) or not authority:
        raise ContractError("AUTHORITY_BASIS_INVALID")
    for pointer in authority:
        _exact_keys(pointer, {"path", "sha"})
        _repo_path(pointer["path"])
        if not isinstance(pointer["sha"], str) or not SHA.fullmatch(pointer["sha"]):
            raise ContractError("AUTHORITY_BASIS_INVALID")
    _remote_ref(value["remote_ref"])
    _work_branch(value["work_branch"])
    for field in ("base_sha", "routing_ref_sha"):
        if not isinstance(value[field], str) or not SHA.fullmatch(value[field]):
            raise ContractError("SHA_INVALID")
    if (value["review_result_sha"] is not None
            and (not isinstance(value["review_result_sha"], str) or not SHA.fullmatch(value["review_result_sha"]))):
        raise ContractError("SHA_INVALID")
    extension = value["role_extension"]
    _validate_role_extension(value["sender_role"], extension)
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
    _string_list(value["checks_performed"], error="CHECKS_INVALID")
    _enum_value(value["status"], {"READY", "BLOCKED", "CLEAR", "VERIFIED", "PENDING_REBECCA", "PENDING_RECORDER_CUSTODY", "UNPUBLISHED_JUDGE_RULING"}, "STATUS_INVALID")
    if not isinstance(value["findings"], list):
        raise ContractError("FINDINGS_INVALID")
    for finding in value["findings"]:
        _exact_keys(finding, {"classification", "severity", "text"})
        if (not isinstance(finding["classification"], str)
                or not isinstance(finding["severity"], str) or finding["severity"] not in {"blocking", "non_blocking"}
                or not isinstance(finding["text"], str)):
            raise ContractError("FINDINGS_INVALID")
    scan = value["scan_attestation"]
    _exact_keys(scan, {"base_sha", "tip_sha", "tool_status", "manual_review", "findings"})
    if (not isinstance(scan["base_sha"], str) or not SHA.fullmatch(scan["base_sha"])
            or not isinstance(scan["tip_sha"], str) or not SHA.fullmatch(scan["tip_sha"])
            or not isinstance(scan["tool_status"], str) or scan["tool_status"] not in {"clean", "blocked", "error"}
            or not isinstance(scan["manual_review"], bool)):
        raise ContractError("SCAN_ATTESTATION_INVALID")
    _string_list(scan["findings"], error="SCAN_ATTESTATION_INVALID")
    _nonempty_string(value["next_event"], "NEXT_EVENT_INVALID")
    _string_list(value["prohibited_actions"], nonempty=True, error="PROHIBITED_ACTIONS_INVALID")
    named = set(_artifact_paths(value))
    if not named.issubset(set(artifacts)):
        raise ContractError("ARTIFACT_INVENTORY_INCOMPLETE")


def _validate_role_extension(role: str, extension: Any) -> None:
    if not isinstance(extension, dict) or extension.get("role") != role:
        raise ContractError("SENDER_EXTENSION_MISMATCH")
    if role == "ARCHITECT":
        _exact_keys(extension, {"role", "changelog_paths", "diff_self_inspection"})
        if not isinstance(extension["changelog_paths"], list) or not isinstance(extension["diff_self_inspection"], bool):
            raise ContractError("SENDER_EXTENSION_INVALID")
        for path in extension["changelog_paths"]:
            _repo_path(path)
    elif role == "CRITIC":
        _exact_keys(extension, {"role", "verdict", "law_fidelity", "substantive"})
        if (not isinstance(extension["verdict"], str) or extension["verdict"] not in {"CLEAR", "BLOCK", "VERIFIED"}
                or not isinstance(extension["law_fidelity"], str) or extension["law_fidelity"] not in {"PASS", "BLOCK", "NOT_APPLICABLE"}
                or not isinstance(extension["substantive"], str) or extension["substantive"] not in {"CLEAR", "BLOCK", "VERIFIED"}):
            raise ContractError("SENDER_EXTENSION_INVALID")
    elif role == "TASK_BUILDER":
        _exact_keys(extension, {"role", "tests", "diagnostics_executed"})
        _string_list(extension["tests"], error="SENDER_EXTENSION_INVALID")
        if not isinstance(extension["diagnostics_executed"], bool):
            raise ContractError("SENDER_EXTENSION_INVALID")
    elif role == "INTEGRATOR":
        _exact_keys(extension, {"role", "state_sha256"})
        if not isinstance(extension["state_sha256"], str) or not SHA256.fullmatch(extension["state_sha256"]):
            raise ContractError("SENDER_EXTENSION_INVALID")
    elif role == "RECORDER":
        _exact_keys(extension, {"role", "custody_hashes"})
        hashes = extension["custody_hashes"]
        if not isinstance(hashes, list) or not hashes or any(not isinstance(item, str) or not SHA256.fullmatch(item) for item in hashes):
            raise ContractError("SENDER_EXTENSION_INVALID")
    elif role == "JUDGE":
        _exact_keys(extension, {"role", "custody_envelope", "publication_status"})
        if extension["publication_status"] != "PENDING_RECORDER_CUSTODY":
            raise ContractError("SENDER_EXTENSION_INVALID")
        validate_judge_envelope(extension["custody_envelope"])
    elif role == "WORKFLOW_COORDINATOR":
        _exact_keys(extension, {"role", "ball_recorded"})
        if not isinstance(extension["ball_recorded"], bool):
            raise ContractError("SENDER_EXTENSION_INVALID")
    elif role == "REBECCA":
        _exact_keys(extension, {"role", "ruling_path"})
        _repo_path(extension["ruling_path"])


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
    if (value["schema_version"] != "workflow-state-metadata-v1"
            or not isinstance(value["source_commit"], str) or not SHA.fullmatch(value["source_commit"])):
        raise ContractError("METADATA_IDENTITY_INVALID")
    if not isinstance(value["as_of_utc"], str) or not UTC_SECOND.fullmatch(value["as_of_utc"]):
        raise ContractError("METADATA_TIMESTAMP_INVALID")
    path = _repo_path(value["document_path"])
    owner_for_role = {"routing": "WORKFLOW_COORDINATOR", "checkpoint": "WORKFLOW_COORDINATOR", "durable_state": "INTEGRATOR", "custody_history": "RECORDER"}
    if not isinstance(value["document_role"], str) or not isinstance(value["owner_role"], str):
        raise ContractError("METADATA_OWNER_MISMATCH")
    if owner_for_role.get(value["document_role"]) != value["owner_role"]:
        raise ContractError("METADATA_OWNER_MISMATCH")
    _enum_value(value["status"], {"current", "superseded", "historical"}, "METADATA_STATUS_INVALID")
    supersedes = value["supersedes_metadata_sha256"]
    if (not isinstance(supersedes, list) or len(supersedes) != len(set(supersedes))
            or any(not isinstance(item, str) or not SHA256.fullmatch(item) for item in supersedes)):
        raise ContractError("METADATA_SUPERSEDES_INVALID")
    if not isinstance(value["document_sha256"], str) or not SHA256.fullmatch(value["document_sha256"]):
        raise ContractError("METADATA_DIGEST_INVALID")
    if repo_root is not None:
        if sha256_bytes(repository_bytes_at(repo_root, value["source_commit"], path)) != value["document_sha256"]:
            raise ContractError("METADATA_DOCUMENT_MISMATCH")


def validate_judge_envelope(value: Any) -> bytes:
    required = {"schema_version", "filename", "media_type", "encoding", "byte_length", "sha256", "content_base64"}
    _exact_keys(value, required)
    if value["schema_version"] != "judge-custody-envelope-v1" or value["media_type"] != "text/markdown; charset=utf-8" or value["encoding"] != "base64-rfc4648-no-whitespace":
        raise ContractError("JUDGE_ENVELOPE_IDENTITY_INVALID")
    if not isinstance(value["filename"], str) or not JUDGE_FILENAME.fullmatch(value["filename"]):
        raise ContractError("JUDGE_FILENAME_INVALID")
    if not isinstance(value["byte_length"], int) or isinstance(value["byte_length"], bool) or not 1 <= value["byte_length"] <= 4194304:
        raise ContractError("JUDGE_BYTE_LENGTH_INVALID")
    if not isinstance(value["sha256"], str) or not SHA256.fullmatch(value["sha256"]):
        raise ContractError("JUDGE_DIGEST_INVALID")
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
    try:
        raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ContractError("JUDGE_TEXT_ENCODING_INVALID") from exc
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


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise ContractError("DUPLICATE_JSON_KEY")
        value[key] = child
    return value


def _reject_json_constant(value: str) -> None:
    raise ContractError(f"NONFINITE_JSON_NUMBER:{value}")


def _load(path: Path) -> tuple[Any, bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ContractError("BOM_FORBIDDEN")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_pairs,
                      parse_constant=_reject_json_constant), raw


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
    except (ContractError, json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(f"BLOCKED: {exc}")
        return 2
    print("VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
