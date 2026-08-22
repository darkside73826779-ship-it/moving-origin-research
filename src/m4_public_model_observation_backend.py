"""Public-model, control/naive-only, non-scoring M4 observation backend.

This module contains no model import, acquisition, or run entrypoint.  A separately
authorized launcher must inject an exact local engine loader and authenticated
identity probes.  Custody-free tests inject a deterministic stub engine only.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import struct
import time
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from src.m4_post_tokenizer_integration import (
    AdapterFactory,
    IntegrationError,
    PrivateTokenView,
    canonical_bytes,
    held_law_projection,
    sha256_bytes,
)


BACKEND_NAME = "public_qwen_observation_v1"
REGISTERED_FAILURE_CODE = "SYNTHETIC_REJECTED"
STAGE_ENVIRONMENT = "MOR_M4_PUBLIC_OBSERVATION_STAGE"
PRIVATE_MAGIC = b"M4_PRIVATE_VIEW_V1\x00"
ZERO_SHA256 = "0" * 64
HEX64 = frozenset("0123456789abcdef")
RECEIPT_FIELDS = frozenset({
    "status", "backend_code", "session_id", "prior_backend_state_sha256",
    "result_backend_state_sha256", "request_sha256", "request_ordinal",
})
OBSERVATION_FIELDS = frozenset({
    "schema_version", "date", "regime", "status", "session_id_sha256",
    "episode_id_sha256", "request_sha256", "request_ordinal", "prompt_ordinal",
    "input_token_count", "input_private_view_sha256", "output_token_count",
    "output_token_ids_sha256", "output_text_utf8_sha256", "monotonic_start_ns",
    "monotonic_end_ns", "duration_ns", "model_identity_sha256",
    "runtime_identity_sha256", "law_projection_sha256", "scientific_evidence",
    "authoritative_scoring", "qualification_evidence", "readiness_evidence",
})
DEPENDENCY_AUTHORITY = {
    "dependency_lock_manifest_sha": "95cd17deabba6a0c84c02e26c408023b989e79bc",
    "dependency_lock_result": "4993711fa32ffe9ab3b2dabb2b5d5615182c6e90",
    "dependency_lock_review": "4cdb5d89945b603c20cdd19233079be14b65946b",
    "dependency_lock_routing_sha": "6d8175edb63cf6ec03c0904d640ae6f946ebcf16",
    "status": "CLEAR",
}
MODEL_IDENTITY = {
    "repository_id": "Qwen/Qwen3-4B-Instruct-2507-FP8",
    "revision": "8591804019c8b22094c3b5b4454e0edc05dffc98",
    "quantization": "OFFICIAL_QWEN_FP8_E4M3",
    "model_file": {"name": "model.safetensors", "bytes": 5190053264,
                   "sha256": "b6154d74332140fd6dfbfbe70bbb3650dd6955861132bd59dda6789e6322b485"},
    "tokenizer_file": {"name": "tokenizer.json", "bytes": 11422654,
                       "sha256": "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4"},
    "tokenizer_config_file": {"name": "tokenizer_config.json", "bytes": 9377,
                              "sha256": "a62ff0a2472a0fa1b8eaabcb57c59b58afa42a22831dc141400b6e0cf2b65ce3"},
}
RUNTIME_IDENTITY = {
    "python": "3.12.3", "torch": "2.13.0+cu132", "vllm": "0.27.1",
    "transformers": "5.15.1", "tokenizers": "0.22.2", "safetensors": "0.8.0",
    "numpy": "2.3.5", "runner": "V1",
    "environment": {"PYTHONHASHSEED": "0", "VLLM_USE_FLASHINFER_SAMPLER": "0",
                    "VLLM_USE_V2_MODEL_RUNNER": "0"},
}
MODEL_IDENTITY_SHA256 = "6973ea4c819681ea66bebfb8c21ab3a9016b5968a07f83de92c88e57aaca2918"
RUNTIME_IDENTITY_SHA256 = "4840d66729bdf1a8f07db0c96be5b9be92d81dd0b7200d7e7a6660c108497567"
LAW_PROJECTION_SHA256 = "bb2d5f838c54c404dd73d0c697ba6f45cd983fb7e5a7bb97a36b38570267b81f"
GENERATION_CONTROLS = {
    "dtype": "auto", "quantization": "fp8", "max_model_len": 2048,
    "max_num_seqs": 1, "gpu_memory_utilization": 0.36, "temperature": 0.0,
    "seed": 0, "max_tokens": 12, "n": 1, "trust_remote_code": False,
    "speculative_decoding": False, "prefix_caching": False, "disable_log_stats": True,
}


class ObservationFailure(RuntimeError):
    """Private internal failure; its value never enters a receipt or artifact."""


def _digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def _mutable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _mutable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_mutable(item) for item in value]
    return value


def generate_public_prompt(ordinal: int) -> bytes:
    """Generate one fixed public prompt without retaining prompt bytes in Git."""
    if type(ordinal) is not int or ordinal not in (0, 1, 2):
        raise ObservationFailure("OBSERVATION_PROMPT_CONTRACT_MISMATCH")
    payload = b"M4_PUBLIC_OBSERVATION_PAYLOAD_V1\x00" + struct.pack(">I", ordinal)
    payload_sha256 = hashlib.sha256(payload).hexdigest()
    prompt = (
        f"M4_PUBLIC_OBSERVATION_V1 ordinal={ordinal:08d} "
        f"payload_sha256={payload_sha256}\n"
    ).encode("ascii", "strict")
    if len(prompt) != 122:
        raise ObservationFailure("OBSERVATION_PROMPT_CONTRACT_MISMATCH")
    return prompt


PROMPT_SHA256 = tuple(hashlib.sha256(generate_public_prompt(i)).hexdigest() for i in range(3))


def held_law_rows() -> list[dict[str, Any]]:
    rows = _mutable(held_law_projection())
    if len(canonical_bytes(rows)) != 974 or _digest(rows) != LAW_PROJECTION_SHA256:
        raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
    if any(row["status"] != "HELD" or row["claim_made"] is not False for row in rows):
        raise ObservationFailure("OBSERVATION_EVIDENCE_BOUNDARY_FAILURE")
    return rows


def classify_network_connect(connect: Callable[[], None]) -> int:
    """Return the exact launch-contract classifier exit without opening a socket here."""
    try:
        connect()
    except OSError as exc:
        return 0 if exc.errno == 101 else 2
    return 3


@dataclass(frozen=True)
class BackendDependencies:
    session_id: str
    stage: Path
    implementation_sha256: str
    dependency_sha256: str
    model_sha256: str
    tokenizer_sha256: str
    valid_token_ids: frozenset[int]
    identity_probe: Callable[[], Mapping[str, Any]]
    dependency_probe: Callable[[], Mapping[str, Any]]
    namespace_probe: Callable[[], bool]
    engine_loader: Callable[[], Any]
    stage_mode_probe: Callable[[Path], int] = lambda path: stat.S_IMODE(path.stat().st_mode)
    file_mode_probe: Callable[[Path], int] = lambda path: stat.S_IMODE(path.stat().st_mode)
    clock_ns: Callable[[], int] = time.monotonic_ns
    cleanup_runtime: Callable[[], None] = lambda: None
    live_engine_count: Callable[[], int] = lambda: 0
    write_hook: Callable[[str], None] = lambda _phase: None

    def validate(self) -> None:
        digest = lambda value: type(value) is str and len(value) == 64 and not (set(value) - HEX64)
        if (type(self.session_id) is not str or not self.session_id or
                any(not digest(value) for value in (
                    self.implementation_sha256, self.dependency_sha256,
                    self.model_sha256, self.tokenizer_sha256)) or
                type(self.valid_token_ids) is not frozenset or not self.valid_token_ids or
                any(type(item) is not int or item < 0 for item in self.valid_token_ids)):
            raise IntegrationError("STRUCTURAL_SCHEMA_FAILURE")


def build_backend_constructor(dependencies: BackendDependencies) -> Callable[[], "PublicModelObservationBackend"]:
    dependencies.validate()
    return lambda: PublicModelObservationBackend(dependencies)


class PublicObservationFactory:
    """Guard registration before construction without changing AdapterFactory."""

    def __init__(self, registry: Mapping[str, tuple[Callable[[], Any], str, str, str]]):
        self._factory = AdapterFactory(registry)

    def create(self, role: str, scientific_arm: str, manifest_bytes: bytes,
               backend_config_bytes: bytes, private_token_provider: Callable[[int | str], Sequence[int]]):
        if role != "control" or scientific_arm != "naive":
            raise IntegrationError("ROLE_ARM_MISMATCH")
        return self._factory.create(role, scientific_arm, manifest_bytes, backend_config_bytes,
                                    private_token_provider)

    def create_pair(self, *_args: Any, **_kwargs: Any):
        raise IntegrationError("ROLE_ARM_MISMATCH")


class PublicModelObservationBackend:
    """RealBackendProtocol implementation with an injected, separately authorized engine."""

    def __init__(self, dependencies: BackendDependencies):
        dependencies.validate()
        self._deps = dependencies
        self._live = True
        self._engine_loaded = False
        self._engine: Any = None
        self._busy = False
        self._phase = "CONSTRUCTED_LIVE_NO_ENGINE"
        self._episode_id: str | None = None
        self._prompt_ordinal = 0
        self._observation_digests: list[str] = []
        self._owned_paths: set[str] = set()
        self._last_state_sha256 = ZERO_SHA256

    def session_identity(self) -> str:
        return self._deps.session_id

    def is_live(self) -> bool:
        return self._live is True

    def _state_value(self) -> dict[str, Any]:
        return {
            "engine_loaded": self._engine_loaded,
            "episode_id": self._episode_id,
            "live": self._live,
            "observation_digests": list(self._observation_digests),
            "phase": self._phase,
            "prompt_ordinal": self._prompt_ordinal,
        }

    def _state_digest(self) -> str:
        return _digest(self._state_value())

    def _stage_root_status(self) -> str:
        stage = self._deps.stage
        if not stage.is_absolute():
            return "RELATIVE"
        try:
            info = stage.lstat()
        except FileNotFoundError:
            return "ABSENT"
        except OSError:
            return "UNREADABLE"
        if stat.S_ISLNK(info.st_mode):
            return "LINKED"
        if not stat.S_ISDIR(info.st_mode):
            return "NOT_DIRECTORY"
        return "VALID"

    @staticmethod
    def _invalid_inventory(status: str) -> list[dict[str, Any]]:
        return [{"bytes": 0, "mode": 0, "name": "!invalid-stage-" + status.lower(),
                 "sha256": ZERO_SHA256}]

    def _inventory(self) -> list[dict[str, Any]]:
        stage = self._deps.stage
        status = self._stage_root_status()
        if status != "VALID":
            return self._invalid_inventory(status)
        rows: list[dict[str, Any]] = []
        try:
            for child in sorted(stage.iterdir(), key=lambda item: item.name):
                info = child.lstat()
                if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                    return self._invalid_inventory("INVALID_CHILD")
                raw = child.read_bytes()
                rows.append({"bytes": len(raw), "mode": stat.S_IMODE(info.st_mode),
                             "name": child.name, "sha256": hashlib.sha256(raw).hexdigest()})
        except OSError:
            return self._invalid_inventory("UNREADABLE_CHILD")
        return rows

    def capture_state(self) -> Mapping[str, Any]:
        return {
            "engine_loaded": self._engine_loaded,
            "episode_id": self._episode_id,
            "inventory": self._inventory(),
            "last_state_sha256": self._last_state_sha256,
            "live": self._live,
            "observation_digests": list(self._observation_digests),
            "owned_paths": sorted(self._owned_paths),
            "phase": self._phase,
            "prompt_ordinal": self._prompt_ordinal,
        }

    def _shutdown_engine(self) -> None:
        engine, self._engine = self._engine, None
        self._engine_loaded = False
        if engine is not None:
            closer = getattr(engine, "shutdown", None) or getattr(engine, "close", None)
            if callable(closer):
                closer()
        self._deps.cleanup_runtime()

    def _fsync_directory(self) -> None:
        # Windows does not permit opening a directory through os.open.  The governed
        # OCI execution domain is Linux; Windows is a custody-free validation domain
        # where os.replace still supplies atomic publication but directory fsync is
        # unavailable through the standard library.
        if os.name == "nt":
            return
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        descriptor = os.open(self._deps.stage, flags)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _remove_path(self, name: str) -> None:
        path = self._deps.stage / name
        if path.exists() or path.is_symlink():
            if path.is_symlink() or not path.is_file():
                raise ObservationFailure("OBSERVATION_ROLLBACK_FAILED")
            path.unlink()

    def _force_dispose(self) -> None:
        try:
            self._shutdown_engine()
        except Exception:
            self._engine = None
            self._engine_loaded = False
        self._live = False
        self._phase = "DISPOSED"

    def restore_state(self, snapshot: Any) -> None:
        required = {"engine_loaded", "episode_id", "inventory", "last_state_sha256", "live",
                    "observation_digests", "owned_paths", "phase", "prompt_ordinal"}
        try:
            if type(snapshot) is not dict or set(snapshot) != required:
                raise ObservationFailure("OBSERVATION_ROLLBACK_FAILED")
            expected_owned = set(snapshot["owned_paths"])
            for name in sorted(self._owned_paths - expected_owned):
                self._remove_path(name)
            if self._engine_loaded and snapshot["engine_loaded"] is False:
                self._shutdown_engine()
            elif not self._engine_loaded and snapshot["engine_loaded"] is True:
                raise ObservationFailure("OBSERVATION_ROLLBACK_FAILED")
            self._episode_id = snapshot["episode_id"]
            self._live = snapshot["live"]
            self._observation_digests = list(snapshot["observation_digests"])
            self._owned_paths = expected_owned
            self._phase = snapshot["phase"]
            self._prompt_ordinal = snapshot["prompt_ordinal"]
            self._last_state_sha256 = snapshot["last_state_sha256"]
            if self._stage_root_status() == "VALID":
                self._fsync_directory()
            if self._inventory() != snapshot["inventory"]:
                raise ObservationFailure("OBSERVATION_ROLLBACK_FAILED")
            observed = self.capture_state()
            if observed != snapshot:
                raise ObservationFailure("OBSERVATION_ROLLBACK_FAILED")
        except Exception as exc:
            self._force_dispose()
            if isinstance(exc, IntegrationError):
                raise
            raise IntegrationError("BACKEND_ROLLBACK_FAILURE") from exc

    def _receipt(self, status: str, prior: str, result: str, request: Mapping[str, Any],
                 ordinal: int | None, backend_code: str | None = None) -> dict[str, Any]:
        receipt = {
            "backend_code": backend_code,
            "prior_backend_state_sha256": prior,
            "request_ordinal": ordinal,
            "request_sha256": sha256_bytes(canonical_bytes(dict(request))),
            "result_backend_state_sha256": result,
            "session_id": self._deps.session_id,
            "status": status,
        }
        if frozenset(receipt) != RECEIPT_FIELDS:
            raise ObservationFailure("OBSERVATION_EVIDENCE_BOUNDARY_FAILURE")
        return receipt

    def _operate(self, prior: str, request: Mapping[str, Any], ordinal: int | None,
                 body: Callable[[], None]) -> Mapping[str, Any]:
        if self._busy or self._live is not True:
            return self._receipt("FAIL", prior, prior, request, ordinal, REGISTERED_FAILURE_CODE)
        snapshot = deepcopy(dict(self.capture_state()))
        self._busy = True
        try:
            if prior != self._last_state_sha256:
                raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
            body()
            result = self._state_digest()
            self._last_state_sha256 = result
            return self._receipt("PASS", prior, result, request, ordinal)
        except Exception:
            try:
                self.restore_state(snapshot)
            except Exception:
                raise
            return self._receipt("FAIL", prior, prior, request, ordinal, REGISTERED_FAILURE_CODE)
        finally:
            self._busy = False

    def _validate_stage(self, require_empty: bool) -> None:
        stage = self._deps.stage
        if (self._stage_root_status() != "VALID" or self._deps.stage_mode_probe(stage) != 0o700):
            raise ObservationFailure("OBSERVATION_STAGE_INVALID")
        inventory = self._inventory()
        if require_empty and inventory:
            raise ObservationFailure("OBSERVATION_STAGE_INVALID")

    def _validate_description(self, manifest: Mapping[str, Any], config: Mapping[str, Any]) -> None:
        if manifest.get("role") != "control" or manifest.get("scientific_arm") != "naive":
            raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
        expected = {
            "backend_name": BACKEND_NAME,
            "implementation_sha256": self._deps.implementation_sha256,
            "dependency_sha256": self._deps.dependency_sha256,
            "model_sha256": self._deps.model_sha256,
            "tokenizer_sha256": self._deps.tokenizer_sha256,
        }
        if any(config.get(key) != value for key, value in expected.items()):
            raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
        if dict(self._deps.dependency_probe()) != DEPENDENCY_AUTHORITY:
            raise ObservationFailure("OBSERVATION_DEPENDENCY_MISMATCH")
        self._validate_stage(True)
        laws = held_law_rows()
        if (len(canonical_bytes(laws)) != 974 or _digest(laws) != LAW_PROJECTION_SHA256 or
                any(type(row) is not dict or row.get("status") != "HELD" or
                    row.get("claim_made") is not False for row in laws)):
            raise ObservationFailure("OBSERVATION_EVIDENCE_BOUNDARY_FAILURE")

    def _validate_runtime_identity(self) -> None:
        observed = dict(self._deps.identity_probe())
        expected = {
            "model_identity": MODEL_IDENTITY,
            "model_identity_sha256": MODEL_IDENTITY_SHA256,
            "runtime_identity": RUNTIME_IDENTITY,
            "runtime_identity_sha256": RUNTIME_IDENTITY_SHA256,
        }
        if observed != expected or self._deps.namespace_probe() is not True:
            raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")

    def describe(self, manifest: Mapping[str, Any], config: Mapping[str, Any],
                 request: Mapping[str, Any]) -> Mapping[str, Any]:
        prior = self._last_state_sha256
        def body() -> None:
            if self._phase != "CONSTRUCTED_LIVE_NO_ENGINE" or self._engine_loaded:
                raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
            self._validate_description(manifest, config)
            self._phase = "DESCRIBED"
        return self._operate(prior, request, None, body)

    def initialize(self, description: Mapping[str, Any], session: Mapping[str, Any],
                   request: Mapping[str, Any]) -> Mapping[str, Any]:
        prior = self._last_state_sha256
        def body() -> None:
            if (self._phase != "DESCRIBED" or self._engine_loaded or
                    description.get("role") != "control" or description.get("scientific_arm") != "naive" or
                    session.get("session_id") != self._deps.session_id):
                raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
            self._validate_runtime_identity()
            engine = self._deps.engine_loader()
            self._engine = engine
            self._engine_loaded = True
            if getattr(engine, "is_live", lambda: False)() is not True:
                raise ObservationFailure("OBSERVATION_ENGINE_LOAD_FAILED")
            if self._deps.live_engine_count() != 1:
                raise ObservationFailure("OBSERVATION_ENGINE_LOAD_FAILED")
            self._phase = "INITIALIZED"
        return self._operate(prior, request, None, body)

    def reset_episode(self, prior: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
        def body() -> None:
            episode = request.get("episode_id")
            if self._phase not in ("INITIALIZED", "STEPPED") or type(episode) is not str or not episode:
                raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
            self._episode_id = episode
            self._phase = "EPISODE_READY"
        return self._operate(prior, request, None, body)

    def _decode_private_view(self, request: Mapping[str, Any], tokens: PrivateTokenView) -> tuple[bytearray, list[int]]:
        mutable = bytearray(tokens.bytes_view)
        if (tokens.context_length != request.get("context_length") or len(mutable) < 23 or
                bytes(mutable[:19]) != PRIVATE_MAGIC):
            raise ObservationFailure("OBSERVATION_PRIVATE_VIEW_INVALID")
        count = struct.unpack(">I", mutable[19:23])[0]
        if (min(count, tokens.context_length) < 1 or count != tokens.context_length or
                len(mutable) != 23 + 8 * count):
            raise ObservationFailure("OBSERVATION_PRIVATE_VIEW_INVALID")
        items = [struct.unpack(">q", mutable[23 + 8 * i:31 + 8 * i])[0] for i in range(count)]
        if any(item < 0 or item not in self._deps.valid_token_ids for item in items):
            raise ObservationFailure("OBSERVATION_PRIVATE_VIEW_INVALID")
        return mutable, items

    def _validate_prompt_request(self, request: Mapping[str, Any]) -> int:
        ordinal = request.get("prompt_ordinal")
        if (type(ordinal) is not int or ordinal != self._prompt_ordinal or ordinal not in (0, 1, 2) or
                request.get("prompt_sha256") != PROMPT_SHA256[ordinal]):
            raise ObservationFailure("OBSERVATION_PROMPT_CONTRACT_MISMATCH")
        prompt = bytearray(generate_public_prompt(ordinal))
        try:
            if hashlib.sha256(prompt).hexdigest() != request["prompt_sha256"]:
                raise ObservationFailure("OBSERVATION_PROMPT_CONTRACT_MISMATCH")
        finally:
            for index in range(len(prompt)):
                prompt[index] = 0
        return ordinal

    @staticmethod
    def _validate_observation(value: Mapping[str, Any]) -> None:
        if type(value) is not dict or frozenset(value) != OBSERVATION_FIELDS:
            raise ObservationFailure("OBSERVATION_EVIDENCE_BOUNDARY_FAILURE")
        digest_fields = ("session_id_sha256", "episode_id_sha256", "request_sha256",
                         "input_private_view_sha256", "output_token_ids_sha256",
                         "output_text_utf8_sha256", "model_identity_sha256",
                         "runtime_identity_sha256", "law_projection_sha256")
        if any(type(value[field]) is not str or len(value[field]) != 64 or set(value[field]) - HEX64
               for field in digest_fields):
            raise ObservationFailure("OBSERVATION_EVIDENCE_BOUNDARY_FAILURE")
        if (value["schema_version"] != "m4-public-model-local-observation-v1" or
                value["date"] != "2026-08-22" or value["regime"] != "B" or value["status"] != "PASS" or
                any(value[field] is not False for field in (
                    "scientific_evidence", "authoritative_scoring", "qualification_evidence", "readiness_evidence")) or
                any(type(value[field]) is not int or value[field] < 0 for field in (
                    "request_ordinal", "prompt_ordinal", "input_token_count", "output_token_count",
                    "monotonic_start_ns", "monotonic_end_ns", "duration_ns")) or
                value["input_token_count"] < 1 or value["prompt_ordinal"] > 2 or
                value["output_token_count"] > 12 or
                value["monotonic_end_ns"] < value["monotonic_start_ns"] or
                value["duration_ns"] != value["monotonic_end_ns"] - value["monotonic_start_ns"] or
                value["model_identity_sha256"] != MODEL_IDENTITY_SHA256 or
                value["runtime_identity_sha256"] != RUNTIME_IDENTITY_SHA256 or
                value["law_projection_sha256"] != LAW_PROJECTION_SHA256):
            raise ObservationFailure("OBSERVATION_EVIDENCE_BOUNDARY_FAILURE")

    def _write_exclusive(self, path: Path, raw: bytes) -> None:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags, 0o600)
        try:
            with os.fdopen(descriptor, "wb", closefd=False) as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
        finally:
            os.close(descriptor)
        os.chmod(path, 0o600)

    def _publish(self, observation: dict[str, Any], request_sha256: str) -> str:
        self._validate_observation(observation)
        raw = canonical_bytes(observation) + b"\n"
        digest = hashlib.sha256(raw).hexdigest()
        stem = "m4-public-observation-" + request_sha256
        final_json, final_sidecar = stem + ".json", stem + ".json.sha256"
        temp_json, temp_sidecar = "." + final_json + ".tmp", "." + final_sidecar + ".tmp"
        names = (temp_json, temp_sidecar, final_json, final_sidecar)
        if any((self._deps.stage / name).exists() or (self._deps.stage / name).is_symlink() for name in names):
            raise ObservationFailure("OBSERVATION_LOCAL_WRITE_FAILED")
        sidecar = f"{digest}  {final_json}\n".encode("ascii")
        try:
            self._deps.write_hook("before_json")
            self._write_exclusive(self._deps.stage / temp_json, raw)
            self._owned_paths.add(temp_json)
            if (self._deps.stage / temp_json).read_bytes() != raw:
                raise ObservationFailure("OBSERVATION_LOCAL_WRITE_FAILED")
            self._deps.write_hook("before_sidecar")
            self._write_exclusive(self._deps.stage / temp_sidecar, sidecar)
            self._owned_paths.add(temp_sidecar)
            self._deps.write_hook("before_rename")
            os.replace(self._deps.stage / temp_json, self._deps.stage / final_json)
            self._owned_paths.remove(temp_json); self._owned_paths.add(final_json)
            os.replace(self._deps.stage / temp_sidecar, self._deps.stage / final_sidecar)
            self._owned_paths.remove(temp_sidecar); self._owned_paths.add(final_sidecar)
            self._fsync_directory()
            if (self._deps.file_mode_probe(self._deps.stage / final_json) != 0o600 or
                    self._deps.file_mode_probe(self._deps.stage / final_sidecar) != 0o600 or
                    (self._deps.stage / final_json).read_bytes() != raw or
                    (self._deps.stage / final_sidecar).read_bytes() != sidecar):
                raise ObservationFailure("OBSERVATION_LOCAL_WRITE_FAILED")
        except Exception as exc:
            for name in names:
                try:
                    self._remove_path(name)
                except Exception:
                    pass
                self._owned_paths.discard(name)
            self._fsync_directory()
            if isinstance(exc, ObservationFailure):
                raise
            raise ObservationFailure("OBSERVATION_LOCAL_WRITE_FAILED") from exc
        return digest

    def step(self, prior: str, request: Mapping[str, Any], tokens: PrivateTokenView) -> Mapping[str, Any]:
        ordinal = request.get("request_ordinal") if type(request.get("request_ordinal")) is int else None
        def body() -> None:
            if self._phase not in ("EPISODE_READY", "STEPPED") or not self._engine_loaded or self._engine is None:
                raise ObservationFailure("OBSERVATION_GENERATION_FAILED")
            if request.get("episode_id") != self._episode_id:
                raise ObservationFailure("OBSERVATION_PRIVATE_VIEW_INVALID")
            prompt_ordinal = self._validate_prompt_request(request)
            mutable = bytearray()
            input_ids: list[int] = []
            output_ids: list[int] = []
            output_text: str | None = None
            try:
                mutable, input_ids = self._decode_private_view(request, tokens)
                start = self._deps.clock_ns()
                results = self._engine.generate(prompt_token_ids=input_ids,
                                                sampling_params=deepcopy(GENERATION_CONTROLS))
                end = self._deps.clock_ns()
                if type(results) is not list or len(results) != 1 or type(results[0]) is not dict or set(results[0]) != {"token_ids", "text"}:
                    raise ObservationFailure("OBSERVATION_GENERATION_FAILED")
                output_ids = results[0]["token_ids"]
                output_text = results[0]["text"]
                if (type(output_ids) is not list or len(output_ids) > 12 or
                        any(type(item) is not int or item < 0 for item in output_ids) or type(output_text) is not str):
                    raise ObservationFailure("OBSERVATION_GENERATION_FAILED")
                request_sha256 = sha256_bytes(canonical_bytes(dict(request)))
                observation = {
                    "authoritative_scoring": False,
                    "date": "2026-08-22",
                    "duration_ns": end - start,
                    "episode_id_sha256": hashlib.sha256(self._episode_id.encode("utf-8")).hexdigest(),
                    "input_private_view_sha256": tokens.sha256,
                    "input_token_count": len(input_ids),
                    "law_projection_sha256": LAW_PROJECTION_SHA256,
                    "model_identity_sha256": MODEL_IDENTITY_SHA256,
                    "monotonic_end_ns": end,
                    "monotonic_start_ns": start,
                    "output_text_utf8_sha256": hashlib.sha256(output_text.encode("utf-8")).hexdigest(),
                    "output_token_count": len(output_ids),
                    "output_token_ids_sha256": hashlib.sha256(canonical_bytes(output_ids)).hexdigest(),
                    "prompt_ordinal": prompt_ordinal,
                    "qualification_evidence": False,
                    "readiness_evidence": False,
                    "regime": "B",
                    "request_ordinal": request["request_ordinal"],
                    "request_sha256": request_sha256,
                    "runtime_identity_sha256": RUNTIME_IDENTITY_SHA256,
                    "schema_version": "m4-public-model-local-observation-v1",
                    "scientific_evidence": False,
                    "session_id_sha256": hashlib.sha256(self._deps.session_id.encode("utf-8")).hexdigest(),
                    "status": "PASS",
                }
                observation_digest = self._publish(observation, request_sha256)
                self._observation_digests.append(observation_digest)
                self._prompt_ordinal += 1
                self._phase = "STEPPED"
            finally:
                for index in range(len(mutable)):
                    mutable[index] = 0
                for index in range(len(input_ids)):
                    input_ids[index] = 0
                for index in range(len(output_ids)):
                    output_ids[index] = 0
                output_text = None
        return self._operate(prior, request, ordinal, body)

    def snapshot(self, prior: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
        def body() -> None:
            if self._phase != "STEPPED":
                raise ObservationFailure("OBSERVATION_IDENTITY_MISMATCH")
            self._phase = "STEPPED"
        return self._operate(prior, request, None, body)

    def close(self, prior: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
        def body() -> None:
            self._shutdown_engine()
            for row in list(self._inventory()):
                if row["name"].endswith(".tmp") and row["name"] in self._owned_paths:
                    self._remove_path(row["name"]); self._owned_paths.discard(row["name"])
            if self._deps.live_engine_count() != 0 or any(row["name"].endswith(".tmp") for row in self._inventory()):
                raise ObservationFailure("OBSERVATION_CLEANUP_FAILED")
            self._live = False
            self._phase = "CLOSED"
        return self._operate(prior, request, None, body)

    def dispose(self) -> None:
        if self._busy:
            raise IntegrationError("BACKEND_ROLLBACK_FAILURE")
        try:
            self._shutdown_engine()
            for row in list(self._inventory()):
                if row["name"].endswith(".tmp") and row["name"] in self._owned_paths:
                    self._remove_path(row["name"]); self._owned_paths.discard(row["name"])
            if self._deps.live_engine_count() != 0 or any(row["name"].endswith(".tmp") for row in self._inventory()):
                raise ObservationFailure("OBSERVATION_CLEANUP_FAILED")
            self._live = False
            self._phase = "DISPOSED"
        except Exception as exc:
            self._force_dispose()
            raise IntegrationError("OBSERVATION_CLEANUP_FAILED") from exc


__all__ = [
    "BACKEND_NAME", "BackendDependencies", "DEPENDENCY_AUTHORITY", "GENERATION_CONTROLS",
    "LAW_PROJECTION_SHA256", "MODEL_IDENTITY", "MODEL_IDENTITY_SHA256", "PROMPT_SHA256",
    "PublicModelObservationBackend", "PublicObservationFactory", "RUNTIME_IDENTITY",
    "RUNTIME_IDENTITY_SHA256", "build_backend_constructor", "classify_network_connect",
    "generate_public_prompt", "held_law_rows",
]
