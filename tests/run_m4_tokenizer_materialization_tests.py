#!/usr/bin/env python3
"""Fail-closed pre-import verifier and isolated M4 tokenizer test runner."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

ATTRIBUTE_BYTES = 2630
ATTRIBUTE_SHA256 = "87c4d948a1794a95f590cafe8f1e24df8d24ac2ef5bf92cc2283e28ed76faf2e"
MARKER_BYTES = 69
MARKER_SHA256 = "6f56eb2128751f0c5c1ab27ff461b38565aa00a3dcd29c04ab8bd56c34f4a961"
JSON_PATHS = (
    "specs/data/m4_tokenizer_materialization_blocked_v1.json",
    "specs/data/m4_tokenizer_materialization_fail_v1.json",
    "specs/data/m4_tokenizer_materialization_request_v1.json",
    "specs/data/m4_tokenizer_materialization_result_schema_v1.json",
    "specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json",
    "specs/data/m4_tokenizer_materialization_test_contract_v1.json",
    "specs/data/m4_tokenizer_private_custody_record_schema_v1.json",
    "specs/data/m4_tokenizer_runtime_unavailable_interpreter_expected_v1.json",
    "specs/data/m4_tokenizer_runtime_unavailable_interpreter_fixture_v1.json",
)
VALIDATION_ORDER = (
    "PATH_SET", "ATTRIBUTE", "FILE_KIND", "JSON_BYTE_FORM",
    "SIDECAR_GRAMMAR", "SIDECAR_BASENAME", "DIGEST",
)


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


_NEGATIVE_IDENTITY = {
    ("PATH_SET", "specs/data/m4_tokenizer_materialization_blocked_v1.json"): ("missing_path", 0),
    ("PATH_SET", "specs/data/m4_tokenizer_unexpected.json"): ("extra_path", 1),
    ("ATTRIBUTE", "specs/data/m4_tokenizer_materialization_blocked_v1.json"): ("attribute_mismatch", 2),
    ("FILE_KIND", "specs/data/m4_tokenizer_materialization_blocked_v1.json.sha256"): ("link_path", 3),
    ("JSON_BYTE_FORM", "specs/data/m4_tokenizer_materialization_fail_v1.json"): ("cr_byte", 4),
    ("JSON_BYTE_FORM", "specs/data/m4_tokenizer_materialization_request_v1.json"): ("bom_prefix", 5),
    ("JSON_BYTE_FORM", "specs/data/m4_tokenizer_materialization_result_schema_v1.json"): ("terminal_lf_missing", 6),
    ("SIDECAR_GRAMMAR", "specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json.sha256"): ("sidecar_grammar", 7),
    ("SIDECAR_BASENAME", "specs/data/m4_tokenizer_materialization_test_contract_v1.json.sha256"): ("sidecar_basename", 8),
    ("DIGEST", "specs/data/m4_tokenizer_private_custody_record_schema_v1.json"): ("digest_mismatch", 9),
}


def failure(check: str, path: str, ordinal: int) -> dict[str, object]:
    case_id, case_ordinal = _NEGATIVE_IDENTITY.get((check, path), ("runtime_snapshot", ordinal))
    return {
        "case_id": case_id,
        "custody_lookup_performed": False,
        "failed_check": check,
        "failure_code": "RUNTIME_IDENTITY_MISMATCH",
        "materialization_output_expected": False,
        "ordinal": case_ordinal,
        "path": path,
        "status": "FAIL",
        "test_module_imported": False,
    }


def _regular_non_link(path: Path) -> bool:
    try:
        mode = os.lstat(path).st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and not path.is_symlink()


def _attribute_map(raw: bytes) -> dict[str, tuple[str, str]]:
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise ValueError("ATTRIBUTE")
    result: dict[str, tuple[str, str]] = {}
    for line in raw.decode("ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split(" ")
        if len(fields) != 3 or fields[1:] != ["text", "eol=lf"] or fields[0] in result:
            raise ValueError("ATTRIBUTE")
        result[fields[0]] = ("set", "lf")
    return result


def capture_runtime_snapshot(root: Path) -> tuple[dict[str, object], ...]:
    attribute_path = root / ".gitattributes"
    if not _regular_non_link(attribute_path):
        raise ValueError("ATTRIBUTE")
    raw_attributes = attribute_path.read_bytes()
    if len(raw_attributes) != ATTRIBUTE_BYTES or hashlib.sha256(raw_attributes).hexdigest() != ATTRIBUTE_SHA256:
        raise ValueError("ATTRIBUTE")
    attributes = _attribute_map(raw_attributes)
    required = (".gitattributes", "tests/__init__.py") + tuple(
        item for path in JSON_PATHS for item in (path, path + ".sha256")
    )
    if any(attributes.get(path) != ("set", "lf") for path in required):
        raise ValueError("ATTRIBUTE")
    marker = root / "tests/__init__.py"
    if not _regular_non_link(marker):
        raise ValueError("FILE_KIND")
    marker_bytes = marker.read_bytes()
    if len(marker_bytes) != MARKER_BYTES or hashlib.sha256(marker_bytes).hexdigest() != MARKER_SHA256:
        raise ValueError("ATTRIBUTE")
    records: list[dict[str, object]] = []
    for path in JSON_PATHS:
        json_path = root / path
        sidecar_path = root / (path + ".sha256")
        records.append({
            "path": path,
            "kind": "REGULAR" if _regular_non_link(json_path) else "OTHER",
            "text": attributes.get(path, (None, None))[0],
            "eol": attributes.get(path, (None, None))[1],
            "bytes": json_path.read_bytes() if json_path.exists() else b"",
            "sidecar_path": path + ".sha256",
            "sidecar_kind": "REGULAR" if _regular_non_link(sidecar_path) else "OTHER",
            "sidecar_text": attributes.get(path + ".sha256", (None, None))[0],
            "sidecar_eol": attributes.get(path + ".sha256", (None, None))[1],
            "sidecar_bytes": sidecar_path.read_bytes() if sidecar_path.exists() else b"",
        })
    return tuple(records)


def validate_runtime_snapshot(snapshot: tuple[dict[str, object], ...]) -> dict[str, object]:
    actual_paths = tuple(record.get("path") for record in snapshot)
    if actual_paths != JSON_PATHS:
        missing = next((path for path in JSON_PATHS if path not in actual_paths), None)
        extra = next((path for path in actual_paths if path not in JSON_PATHS), None)
        path = missing or str(extra or "<ordered-path-mismatch>")
        return failure("PATH_SET", path, 0)
    for ordinal, record in enumerate(snapshot):
        path = JSON_PATHS[ordinal]
        if record.get("text") != "set" or record.get("eol") != "lf" or record.get("sidecar_text") != "set" or record.get("sidecar_eol") != "lf":
            return failure("ATTRIBUTE", path, ordinal)
        if record.get("kind") != "REGULAR":
            return failure("FILE_KIND", path, ordinal)
        if record.get("sidecar_kind") != "REGULAR":
            return failure("FILE_KIND", path + ".sha256", ordinal)
        raw = record.get("bytes")
        sidecar = record.get("sidecar_bytes")
        if not isinstance(raw, bytes) or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
            return failure("JSON_BYTE_FORM", path, ordinal)
        try:
            raw[:-1].decode("utf-8")
        except UnicodeDecodeError:
            return failure("JSON_BYTE_FORM", path, ordinal)
        if not isinstance(sidecar, bytes):
            return failure("SIDECAR_GRAMMAR", path + ".sha256", ordinal)
        try:
            sidecar_text = sidecar.decode("ascii")
        except UnicodeDecodeError:
            return failure("SIDECAR_GRAMMAR", path + ".sha256", ordinal)
        parts = sidecar_text.removesuffix("\n").split("  ") if sidecar_text.endswith("\n") else []
        if len(parts) != 2 or len(parts[0]) != 64 or any(character not in "0123456789abcdef" for character in parts[0]):
            return failure("SIDECAR_GRAMMAR", path + ".sha256", ordinal)
        if parts[1] != Path(path).name:
            return failure("SIDECAR_BASENAME", path + ".sha256", ordinal)
        if hashlib.sha256(raw).hexdigest() != parts[0]:
            return failure("DIGEST", path, ordinal)
    return {
        "custody_lookup_performed": False,
        "materialization_output_expected": False,
        "status": "PASS",
        "test_module_imported": False,
    }


def main() -> int:
    root = Path(__file__).resolve(strict=True).parent.parent
    expected_test = root / "tests/test_m4_tokenizer_materialization.py"
    selected = tuple(root.joinpath("tests").glob("test_m4_tokenizer_materialization.py"))
    if selected != (expected_test,) or not _regular_non_link(expected_test):
        sys.stderr.buffer.write(canonical(failure("PATH_SET", "tests/test_m4_tokenizer_materialization.py", 0)) + b"\n")
        return 2
    try:
        disposition = validate_runtime_snapshot(capture_runtime_snapshot(root))
    except (OSError, ValueError):
        disposition = failure("ATTRIBUTE", ".gitattributes", 0)
    if disposition["status"] != "PASS":
        sys.stderr.buffer.write(canonical(disposition) + b"\n")
        return 2
    import unittest
    suite = unittest.defaultTestLoader.discover(
        start_dir=str(root / "tests"),
        pattern="test_m4_tokenizer_materialization.py",
        top_level_dir=str(root),
    )
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
