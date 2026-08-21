"""M4 deterministic synthetic callable scaffold (Regime B, 2026-08-21).

This module implements only the Rebecca-released synthetic contract in
``specs/m4_model_agnostic_scaffold_spec_v1.md`` and the controlling callable
step overlay.  It performs no model, tokenizer, seed, scoring, or L8 work.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "specs" / "data"
DATE = "2026-08-21"
REGIME = "B"


class ContractError(ValueError):
    """Fail-closed synthetic-contract error with the prescribed failure code."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code


def _number(value: float) -> str:
    if not math.isfinite(value):
        raise ContractError("NONFINITE_OUTPUT")
    if value == 0:
        return "0"
    rendered = repr(value)
    if "e" in rendered or "E" in rendered:
        mantissa, exponent = re.split("[eE]", rendered)
        sign = "+" if int(exponent) >= 0 else "-"
        rendered = f"{mantissa}e{sign}{abs(int(exponent))}"
    elif rendered.endswith(".0"):
        rendered = rendered[:-2]
    return rendered


def canonical_json(value: Any) -> bytes:
    """Return RFC-8785 bytes for the contract's JSON/binary64 domain."""
    if value is None:
        return b"null"
    if value is True:
        return b"true"
    if value is False:
        return b"false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value).encode("ascii")
    if isinstance(value, float):
        return _number(value).encode("ascii")
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if isinstance(value, list):
        return b"[" + b",".join(canonical_json(item) for item in value) + b"]"
    if isinstance(value, Mapping):
        members = []
        for key in sorted(value):
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            members.append(canonical_json(key) + b":" + canonical_json(value[key]))
        return b"{" + b",".join(members) + b"}"
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: Any) -> str:
    return digest_bytes(canonical_json(value))


def repository_text_bytes(path: Path) -> bytes:
    """Return Git's LF-normalized text bytes, failing on ambiguous lone CRs."""
    raw = path.read_bytes()
    without_pairs = raw.replace(b"\r\n", b"")
    if b"\r" in without_pairs:
        raise ContractError("CONFIGURATION_MISMATCH", "lone CR in governed text artifact")
    return raw.replace(b"\r\n", b"\n")


def load_json(name: str) -> dict[str, Any]:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


BASE = load_json("m4_model_scaffold_executable_fixture_v1.json")
CALLABLE = load_json("m4_model_callable_fixture_v1.json")
AMENDMENT = load_json("m4_callable_step_digest_amendment_v1.json")


def decode_canonical(data: bytes) -> Any:
    try:
        if data.startswith(b"\xef\xbb\xbf") or data.endswith(b"\n") or data.endswith(b"\r"):
            raise ValueError
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ContractError("SCHEMA_DRIFT") from exc
    if canonical_json(value) != data:
        raise ContractError("SCHEMA_DRIFT", "input is not canonical RFC-8785 JSON")
    return value


def _matches_type(value: Any, expected: str) -> bool:
    return {
        "null": value is None,
        "boolean": isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "string": isinstance(value, str),
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
    }[expected]


def _resolve_ref(root: Mapping[str, Any], ref: str) -> Mapping[str, Any]:
    if not ref.startswith("#/"):
        raise ContractError("SCHEMA_DRIFT", "external schema references are prohibited")
    node: Any = root
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _valid(value: Any, schema: Mapping[str, Any], root: Mapping[str, Any]) -> bool:
    try:
        _validate(value, schema, root)
        return True
    except ContractError:
        return False


def _validate(value: Any, schema: Mapping[str, Any], root: Mapping[str, Any]) -> None:
    if "$ref" in schema:
        _validate(value, _resolve_ref(root, schema["$ref"]), root)
        return
    if "const" in schema and value != schema["const"]:
        raise ContractError("SCHEMA_DRIFT")
    if "enum" in schema and value not in schema["enum"]:
        raise ContractError("SCHEMA_DRIFT")
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_matches_type(value, item) for item in types):
            raise ContractError("SCHEMA_DRIFT")
    if "anyOf" in schema and not any(_valid(value, item, root) for item in schema["anyOf"]):
        raise ContractError("SCHEMA_DRIFT")
    if "oneOf" in schema and sum(_valid(value, item, root) for item in schema["oneOf"]) != 1:
        raise ContractError("SCHEMA_DRIFT")
    if "allOf" in schema:
        for item in schema["allOf"]:
            _validate(value, item, root)
    if "not" in schema and _valid(value, schema["not"], root):
        raise ContractError("SCHEMA_DRIFT")
    if "if" in schema and _valid(value, schema["if"], root):
        _validate(value, schema.get("then", {}), root)
    elif "else" in schema:
        _validate(value, schema["else"], root)
    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                raise ContractError("SCHEMA_DRIFT")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and any(k not in properties for k in value):
            raise ContractError("SCHEMA_DRIFT")
        for key, child in properties.items():
            if key in value:
                _validate(value[key], child, root)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", math.inf):
            raise ContractError("SCHEMA_DRIFT")
        if "items" in schema:
            for item in value:
                _validate(item, schema["items"], root)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or not re.search(schema.get("pattern", ".*"), value):
            raise ContractError("SCHEMA_DRIFT")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value) or value < schema.get("minimum", -math.inf) or value > schema.get("maximum", math.inf):
            raise ContractError("SCHEMA_DRIFT")


def validate_schema(value: Any, schema_name: str) -> None:
    schema = load_json(schema_name)
    _validate(value, schema, schema)


def verify_wrapper(wrapper: Mapping[str, Any]) -> None:
    artifact = wrapper["artifact"]
    raw = canonical_json(artifact)
    if base64.b64decode(wrapper["canonical_utf8_base64"], validate=True) != raw:
        raise ContractError("DIGEST_MISMATCH", "wrapper base64 mismatch")
    if digest_bytes(raw) != wrapper["expected_sha256"]:
        raise ContractError("DIGEST_MISMATCH", "wrapper SHA-256 mismatch")


def verify_released_fixtures() -> dict[str, str]:
    """Reconstruct the released prefix and amended step/snapshot/close chain."""
    raw_callable = (DATA / "m4_model_callable_fixture_v1.json").read_bytes()
    if digest_bytes(raw_callable) != AMENDMENT["base"]["raw_sha256"]:
        raise ContractError("CONFIGURATION_MISMATCH", "callable fixture base mismatch")
    sidecar = (DATA / "m4_callable_step_digest_amendment_v1.json.sha256").read_text("utf-8")
    expected_raw = sidecar.split("  ", 1)[0]
    amendment_path = DATA / "m4_callable_step_digest_amendment_v1.json"
    if digest_bytes(repository_text_bytes(amendment_path)) != expected_raw:
        raise ContractError("DIGEST_MISMATCH", "amendment sidecar mismatch")

    prefix = CALLABLE["lifecycle_state_contract"]
    for key in ("created", "described", "initialized", "ready"):
        verify_wrapper(prefix["states"][key])
        validate_schema(prefix["states"][key]["artifact"], "m4_model_adapter_state_schema_v1.json")
    for key in ("describe", "initialize", "reset_episode"):
        verify_wrapper(prefix["operation_results"][key])
        validate_schema(prefix["operation_results"][key]["artifact"], "m4_model_adapter_operation_result_schema_v1.json")

    wrappers = (
        "varying_response", "stepped_state_projection", "stepped_state",
        "step_operation_result", "snapshot_request", "snapshotted_state",
        "snapshot_operation_result", "closed_state", "close_operation_result",
    )
    for key in wrappers:
        verify_wrapper(AMENDMENT[key])
    validate_schema(AMENDMENT["varying_response"]["artifact"], "m4_model_adapter_response_schema_v1.json")
    for key in ("stepped_state", "snapshotted_state", "closed_state"):
        validate_schema(AMENDMENT[key]["artifact"], "m4_model_adapter_state_schema_v1.json")
    for key in ("step_operation_result", "snapshot_operation_result", "close_operation_result"):
        validate_schema(AMENDMENT[key]["artifact"], "m4_model_adapter_operation_result_schema_v1.json")
    validate_schema(AMENDMENT["snapshot_request"]["artifact"], "m4_model_snapshot_request_schema_v1.json")
    return {key: AMENDMENT[key]["expected_sha256"] for key in wrappers}


class SyntheticCallableAdapter:
    """Exact candidate callable used by the released first-step fixture chain."""

    def __init__(self) -> None:
        self.manifest = copy.deepcopy(BASE["manifest_pair"]["candidate"])
        self.manifest_bytes = canonical_json(self.manifest)
        self.manifest_sha256 = digest(self.manifest)
        self.state = copy.deepcopy(CALLABLE["lifecycle_state_contract"]["states"]["created"]["artifact"])

    def _failure(self, operation: str, code: str) -> bytes:
        before = digest(self.state)
        artifact = {
            "adapter_version": "m4-model-adapter-v1", "date": DATE,
            "failure_code": code, "manifest_sha256": self.manifest_sha256,
            "operation": operation, "post_state_sha256": before,
            "prior_state": self.state["lifecycle_state"],
            "prior_state_sha256": before, "regime": REGIME,
            "result_state": "FAILED", "schema_version": "m4-model-adapter-operation-result-v1",
            "status": "FAIL",
        }
        validate_schema(artifact, "m4_model_adapter_operation_result_schema_v1.json")
        return canonical_json(artifact)

    def _commit_success(
        self,
        operation: str,
        next_state_wrapper: Mapping[str, Any],
        operation_wrapper: Mapping[str, Any],
    ) -> bytes:
        """Validate a complete success transition before committing its state."""
        prior_state = self.state
        next_state = next_state_wrapper["artifact"]
        result = operation_wrapper["artifact"]

        verify_wrapper(next_state_wrapper)
        validate_schema(next_state, "m4_model_adapter_state_schema_v1.json")
        verify_wrapper(operation_wrapper)
        validate_schema(result, "m4_model_adapter_operation_result_schema_v1.json")

        if (
            result["operation"] != operation
            or result["status"] != "PASS"
            or result["failure_code"] is not None
            or result["prior_state"] != prior_state["lifecycle_state"]
            or result["result_state"] != next_state["lifecycle_state"]
            or result["prior_state_sha256"] != digest(prior_state)
            or result["post_state_sha256"] != digest(next_state)
        ):
            raise ContractError("DIGEST_MISMATCH", "success transition binding mismatch")

        result_bytes = canonical_json(result)
        self.state = copy.deepcopy(next_state)
        return result_bytes

    def describe(self) -> tuple[bytes, bytes]:
        if self.state["lifecycle_state"] != "CREATED":
            return self.manifest_bytes, self._failure("describe", "ADAPTER_LIFECYCLE_VIOLATION")
        try:
            result = self._commit_success(
                "describe",
                CALLABLE["lifecycle_state_contract"]["states"]["described"],
                CALLABLE["lifecycle_state_contract"]["operation_results"]["describe"],
            )
        except ContractError as exc:
            result = self._failure("describe", exc.code)
        return self.manifest_bytes, result

    def initialize(self, manifest_bytes: bytes, dependency_manifest_bytes: bytes) -> bytes:
        if self.state["lifecycle_state"] != "DESCRIBED":
            return self._failure("initialize", "ADAPTER_LIFECYCLE_VIOLATION")
        try:
            manifest = decode_canonical(manifest_bytes)
            dependency = decode_canonical(dependency_manifest_bytes)
            validate_schema(manifest, "m4_model_adapter_manifest_schema_v1.json")
            validate_schema(dependency, "m4_model_dependency_manifest_schema_v1.json")
        except ContractError as exc:
            return self._failure("initialize", exc.code)
        if digest(manifest) != self.manifest_sha256 or digest(dependency) != CALLABLE["dependency_manifest"]["expected_sha256"]:
            return self._failure("initialize", "CONFIGURATION_MISMATCH")
        try:
            return self._commit_success(
                "initialize",
                CALLABLE["lifecycle_state_contract"]["states"]["initialized"],
                CALLABLE["lifecycle_state_contract"]["operation_results"]["initialize"],
            )
        except ContractError as exc:
            return self._failure("initialize", exc.code)

    def reset_episode(self, reset_request_bytes: bytes) -> bytes:
        if self.state["lifecycle_state"] != "INITIALIZED":
            return self._failure("reset_episode", "ADAPTER_LIFECYCLE_VIOLATION")
        try:
            request = decode_canonical(reset_request_bytes)
            validate_schema(request, "m4_model_reset_request_schema_v1.json")
        except ContractError as exc:
            return self._failure("reset_episode", exc.code)
        if request != CALLABLE["reset_fixture"]["request"]:
            code = "DIGEST_MISMATCH" if request.get("prior_state_sha256") != digest(self.state) else "CONFIGURATION_MISMATCH"
            return self._failure("reset_episode", code)
        try:
            return self._commit_success(
                "reset_episode",
                CALLABLE["lifecycle_state_contract"]["states"]["ready"],
                CALLABLE["lifecycle_state_contract"]["operation_results"]["reset_episode"],
            )
        except ContractError as exc:
            return self._failure("reset_episode", exc.code)

    def step(self, request_bytes: bytes, perturbation_payload_bytes_or_empty: bytes) -> tuple[bytes, bytes]:
        if self.state["lifecycle_state"] != "EPISODE_READY":
            return b"", self._failure("step", "ADAPTER_LIFECYCLE_VIOLATION")
        try:
            request = decode_canonical(request_bytes)
            validate_schema(request, "m4_model_adapter_request_schema_v1.json")
        except ContractError as exc:
            return b"", self._failure("step", exc.code)
        expected_request = base64.b64decode(CALLABLE["varying_candidate"]["canonical_request_utf8_base64"])
        if request_bytes != expected_request or perturbation_payload_bytes_or_empty != b"":
            return b"", self._failure("step", "CONFIGURATION_MISMATCH")
        if request["episode_id"] != self.state["episode_id"] or request["request_ordinal"] != self.state["next_request_ordinal"]:
            return b"", self._failure("step", "CONFIGURATION_MISMATCH")

        projection = copy.deepcopy(AMENDMENT["stepped_state"]["artifact"])
        projection["last_response_sha256"] = None
        del projection["last_response_sha256"]
        if digest(projection) != AMENDMENT["stepped_state_projection"]["expected_sha256"]:
            return b"", self._failure("step", "DIGEST_MISMATCH")
        response = copy.deepcopy(AMENDMENT["varying_response"]["artifact"])
        if response["state_before_sha256"] != digest(self.state) or response["state_after_sha256"] != digest(projection):
            return b"", self._failure("step", "DIGEST_MISMATCH")
        response_bytes = canonical_json(response)
        try:
            verify_wrapper(AMENDMENT["varying_response"])
            validate_schema(response, "m4_model_adapter_response_schema_v1.json")
        except ContractError as exc:
            return b"", self._failure("step", exc.code)
        post = copy.deepcopy(AMENDMENT["stepped_state"]["artifact"])
        if post["last_response_sha256"] != digest_bytes(response_bytes):
            return b"", self._failure("step", "DIGEST_MISMATCH")
        try:
            operation_bytes = self._commit_success(
                "step", AMENDMENT["stepped_state"], AMENDMENT["step_operation_result"]
            )
        except ContractError as exc:
            return b"", self._failure("step", exc.code)
        return response_bytes, operation_bytes

    def snapshot(self, request_bytes: bytes) -> tuple[bytes, bytes]:
        if self.state["lifecycle_state"] != "STEPPED":
            return b"", self._failure("snapshot", "ADAPTER_LIFECYCLE_VIOLATION")
        try:
            request = decode_canonical(request_bytes)
            validate_schema(request, "m4_model_snapshot_request_schema_v1.json")
        except ContractError as exc:
            return b"", self._failure("snapshot", exc.code)
        if request != AMENDMENT["snapshot_request"]["artifact"] or request["expected_state_sha256"] != digest(self.state):
            return b"", self._failure("snapshot", "DIGEST_MISMATCH")
        checkpoint = copy.deepcopy(BASE["checkpoint"]["artifact"])
        validate_schema(checkpoint, "m4_model_checkpoint_metadata_schema_v1.json")
        try:
            result = self._commit_success(
                "snapshot", AMENDMENT["snapshotted_state"], AMENDMENT["snapshot_operation_result"]
            )
        except ContractError as exc:
            return b"", self._failure("snapshot", exc.code)
        return canonical_json(checkpoint), result

    def close(self) -> bytes:
        if self.state != AMENDMENT["snapshotted_state"]["artifact"]:
            return self._failure("close", "ADAPTER_LIFECYCLE_VIOLATION")
        try:
            return self._commit_success(
                "close", AMENDMENT["closed_state"], AMENDMENT["close_operation_result"]
            )
        except ContractError as exc:
            return self._failure("close", exc.code)


__all__ = [
    "AMENDMENT", "BASE", "CALLABLE", "ContractError", "SyntheticCallableAdapter",
    "canonical_json", "decode_canonical", "digest", "digest_bytes", "validate_schema",
    "repository_text_bytes", "verify_released_fixtures", "verify_wrapper",
]
