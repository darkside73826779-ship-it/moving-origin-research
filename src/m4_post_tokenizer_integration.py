"""Custody-free M4 post-tokenizer integration seam.

The module deliberately contains no model, tokenizer, filesystem-custody, network,
or scoring implementation.  Private token arrays enter only through an injected
provider and are exposed to a backend as an immutable canonical byte view.
"""

from __future__ import annotations

import hashlib
import json
import struct
import threading
from pathlib import Path
from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol, Sequence


ROLE_ARMS = {
    "candidate": frozenset(("candidate",)),
    "peer": frozenset(("peer",)),
    "control": frozenset(("empty", "permuted", "shuffled", "oracle", "naive", "frozen", "specificity")),
}
PAIR_EQUALITY_FIELDS = (
    "checkpoint_sha256", "checkpoint_revision", "weight_hashes",
    "training_instance_sha256", "tokenizer_sha256", "architecture_sha256",
    "parameter_count", "quantization_sha256", "decoding_sha256",
    "calibration_contract_sha256", "evaluation_data_sha256",
    "binning_definition_sha256",
)
PAIR_DIFFERENCE_FIELDS = (
    "role", "scientific_arm", "runtime_instance_id", "access_policy_id",
    "channel_policy", "redaction_receipt_sha256",
)
LAW_ORDER = ("L7", "L8", "L10", "L14", "L18")
HELD_REASONS = {
    "L7": "SCORING_UNAUTHORIZED", "L8": "L8_PREREQUISITE_UNCLEARED",
    "L10": "SCORING_UNAUTHORIZED", "L14": "SCORING_UNAUTHORIZED",
    "L18": "EF3_ABSENT",
}
LAW_LINES = {"L7": 26, "L8": 28, "L10": 32, "L14": 42, "L18": 54}
LAW_REQUIRED_EVIDENCE = {
    "L7": ("candidate_manifest","peer_manifest","channel_redaction_receipt","ground_truth_receipt","candidate_auroc","candidate_ece","paired_peer_margin","empty_permuted_shuffled_rows"),
    "L8": ("homeostatic_variable_identity","level_zero_and_dose_schedule","mirror_degradation_receipt","regulation_error_series","dose_response_statistic","specificity_panel"),
    "L10": ("threshold_identity","complete_drift_population","pre_abstention_scores","abstention_decisions","drift_primary_metric","clean_secondary_metric"),
    "L14": ("shared_variable_identity","self_model_visibility_receipt","memory_perturbation_linkage","thick_present_target_linkage","coupling_metrics"),
    "L18": ("positive_claim_inventory","empty_permuted_shuffled_oracle_frozen_naive_matrix","control_transforms","oracle_reachability","governed_seed_count"),
}
LAW_ALLOWED_FAILURES = {
    "L7": frozenset(("L7_CALIBRATION_FAIL","L7_PEER_MARGIN_FAIL","L7_PEER_CHANNEL_INVALID","L7_CONTAMINATION_FAIL")),
    "L8": frozenset(("L8_DOSE_RESPONSE_FAIL","L8_SPECIFICITY_FAIL")),
    "L10": frozenset(("L10_BLEND_BELOW_THRESHOLD","L10_DRIFT_METRIC_FAIL","L10_ABSTENTION_CALIBRATION_FAIL")),
    "L14": frozenset(("L14_VISIBILITY_FAIL","L14_MEMORY_COUPLING_FAIL","L14_THICK_PRESENT_FAIL")),
    "L18": frozenset(("L18_ARM_MISSING","L18_CONTROL_BEHAVIOR_FAIL","L18_ORACLE_FAIL","L18_SEED_REQUIREMENT_FAIL")),
}
REGISTERED_BACKEND_FAIL_CODES = frozenset(("SYNTHETIC_REJECTED",))
HEX64 = frozenset("0123456789abcdef")
COMMON_REQUEST_FIELDS = ("operation_id", "caller_session_id", "caller_thread_id")
RECEIPT_FIELDS = frozenset((
    "status", "backend_code", "session_id", "prior_backend_state_sha256",
    "result_backend_state_sha256", "request_sha256", "request_ordinal",
))


def canonical_bytes(value: Any) -> bytes:
    """Return the repository's integer/string fixture canonical JSON domain."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def realize_launch_command(contract: Mapping[str, Any], released_checkout: str) -> tuple[str, ...]:
    """Realize the sole released-checkout placeholder before any subprocess starts."""
    if type(released_checkout) is not str or not released_checkout or "," in released_checkout:
        raise IntegrationError("RELEASED_CHECKOUT_INVALID")
    root = Path(released_checkout)
    if not root.is_absolute() or not root.is_dir(): raise IntegrationError("RELEASED_CHECKOUT_INVALID")
    tokens = contract.get("command_tokens") if isinstance(contract, Mapping) else None
    if type(tokens) is not list or tokens.count("type=bind,src=${MOR_RELEASED_CHECKOUT},dst=/workspace,readonly") != 1:
        raise IntegrationError("LAUNCH_CONTRACT_INVALID")
    realized = tuple(token.replace("${MOR_RELEASED_CHECKOUT}", released_checkout) for token in tokens)
    mount = f"type=bind,src={released_checkout},dst=/workspace,readonly"
    if mount not in realized or any("src=,dst=/workspace" in token or "${" in token for token in realized):
        raise IntegrationError("LAUNCH_CONTRACT_INVALID")
    return realized


def frozen(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(k): frozen(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(frozen(v) for v in value)
    if isinstance(value, tuple):
        return tuple(frozen(v) for v in value)
    return value


class IntegrationError(RuntimeError):
    def __init__(self, code: str, *, backend_code: str | None = None):
        super().__init__(code)
        self.code = code
        self.backend_code = backend_code


@dataclass(frozen=True)
class PrivateTokenView:
    context_length: int
    bytes_view: bytes

    @property
    def byte_length(self) -> int:
        return len(self.bytes_view)

    @property
    def sha256(self) -> str:
        return sha256_bytes(self.bytes_view)


def encode_private_view(items: Sequence[int]) -> bytes:
    if len(items) > 0xFFFFFFFF:
        raise IntegrationError("PRIVATE_TOKEN_LENGTH_INVALID")
    output = bytearray(b"M4_PRIVATE_VIEW_V1\x00" + struct.pack(">I", len(items)))
    for item in items:
        if type(item) is not int or item < -(1 << 63) or item >= (1 << 63):
            raise IntegrationError("PRIVATE_TOKEN_INTEGER_INVALID")
        output.extend(struct.pack(">q", item))
    return bytes(output)


class RealBackendProtocol(Protocol):
    def capture_state(self) -> Any: ...
    def restore_state(self, snapshot: Any) -> None: ...
    def describe(self, manifest: Mapping[str, Any], config: Mapping[str, Any], request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def initialize(self, description: Mapping[str, Any], session: Mapping[str, Any], request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def reset_episode(self, prior: str, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def step(self, prior: str, request: Mapping[str, Any], tokens: PrivateTokenView) -> Mapping[str, Any]: ...
    def snapshot(self, prior: str, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def close(self, prior: str, request: Mapping[str, Any]) -> Mapping[str, Any]: ...


class ModelAdapterProtocol(Protocol):
    def describe(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def initialize(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def reset_episode(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def step(self, request: Mapping[str, Any], tokens: PrivateTokenView) -> Mapping[str, Any]: ...
    def snapshot(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def close(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...


def validate_pair_identity(candidate: Mapping[str, Any], peer: Mapping[str, Any]) -> None:
    for field in PAIR_EQUALITY_FIELDS:
        if field not in candidate or field not in peer or candidate[field] != peer[field]:
            raise IntegrationError("PAIR_IDENTITY_MISMATCH")
    if candidate.get("runtime_instance_id") == peer.get("runtime_instance_id"):
        raise IntegrationError("SESSION_ISOLATION_FAILURE")
    if candidate.get("access_policy_id") == peer.get("access_policy_id"):
        raise IntegrationError("ACCESS_ISOLATION_FAILURE")
    for field in PAIR_DIFFERENCE_FIELDS:
        if field not in candidate or field not in peer or candidate[field] == peer[field]:
            raise IntegrationError("PAIR_ISOLATION_FIELD_NOT_DISTINCT")
    if candidate.get("role") != "candidate" or candidate.get("scientific_arm") != "candidate":
        raise IntegrationError("ROLE_ARM_MISMATCH")
    if peer.get("role") != "peer" or peer.get("scientific_arm") != "peer":
        raise IntegrationError("ROLE_ARM_MISMATCH")
    if peer.get("channel_policy") not in ("REDACTED", "BEHAVIOR_ONLY", "OBSERVABLE_ONLY"):
        raise IntegrationError("PEER_CHANNEL_BYPASS")


def _initial_state() -> dict[str, Any]:
    return {
        "lifecycle_state": "CREATED", "closed": False,
        "episode_id": None, "episode_complete": False,
        "reset_ordinal": 0, "next_request_ordinal": 0,
        "snapshot_ordinal": 0, "last_response_sha256": None,
    }


def validate_state(state: Mapping[str, Any]) -> None:
    expected = {"lifecycle_state","closed","episode_id","episode_complete","reset_ordinal",
                "next_request_ordinal","snapshot_ordinal","last_response_sha256"}
    if not isinstance(state, Mapping) or set(state) != expected:
        raise IntegrationError("STATE_SEMANTIC_FAILURE")
    lifecycle = state.get("lifecycle_state")
    if (type(state.get("closed")) is not bool or type(state.get("episode_complete")) is not bool or
            any(type(state.get(k)) is not int or state[k] < 0 for k in ("reset_ordinal","next_request_ordinal","snapshot_ordinal")) or
            state["closed"] is not (lifecycle == "CLOSED") or
            lifecycle in ("CREATED","DESCRIBED","INITIALIZED") and state.get("episode_id") is not None or
            lifecycle in ("EPISODE_READY","STEPPED") and (type(state.get("episode_id")) is not str or not state["episode_id"])):
        raise IntegrationError("STATE_SEMANTIC_FAILURE")


class BaseAdapter:
    """State-validating adapter around one separately registered backend."""

    def __init__(self, role: str, arm: str, manifest: Mapping[str, Any], config: Mapping[str, Any],
                 provider: Callable[[int | str], Sequence[int]], backend: RealBackendProtocol):
        self.role, self.scientific_arm = role, arm
        self.manifest, self.config = frozen(manifest), frozen(config)
        self.private_token_provider, self.backend = provider, backend
        self.adapter_instance_id = str(config["adapter_instance_id"])
        self.session_id = str(manifest["runtime_instance_id"])
        self._state = _initial_state()
        self._backend_state = str(config.get("initial_backend_state_sha256", "0" * 64))
        self._used_episode_ids: set[str] = set()
        self._lock = threading.Lock()
        self._active_identity: str | None = None
        self._active_operation_id: str | None = None

    def durable_state(self) -> bytes:
        return canonical_bytes(self._state)

    def restore(self, snapshot: tuple[dict[str, Any], str, set[str]]) -> None:
        self._state, self._backend_state, self._used_episode_ids = deepcopy(snapshot)

    def capture(self) -> tuple[dict[str, Any], str, set[str]]:
        return deepcopy((self._state, self._backend_state, self._used_episode_ids))

    def capture_transaction(self) -> tuple[tuple[dict[str, Any], str, set[str]], Any]:
        try:
            backend = self.backend.capture_state()
        except Exception as exc:
            raise IntegrationError("BACKEND_TRANSACTION_UNAVAILABLE") from exc
        return self.capture(), deepcopy(backend)

    def restore_transaction(self, snapshot: tuple[tuple[dict[str, Any], str, set[str]], Any]) -> None:
        adapter, backend = snapshot
        try:
            self.backend.restore_state(deepcopy(backend))
        except Exception as exc:
            raise IntegrationError("BACKEND_ROLLBACK_FAILURE") from exc
        self.restore(adapter)

    @staticmethod
    def _nonempty(value: Any) -> bool:
        return type(value) is str and bool(value.strip())

    def _validate_request(self, operation: str, request: Mapping[str, Any]) -> None:
        if not isinstance(request, Mapping) or any(not self._nonempty(request.get(k)) for k in COMMON_REQUEST_FIELDS):
            raise IntegrationError("REQUEST_STRUCTURE_INVALID")
        fields: dict[str, type] = {
            "reset_episode": {"episode_id": str, "reset_ordinal": int},
            "step": {"episode_id": str, "request_ordinal": int, "context_length": int, "is_terminal_request": bool},
            "snapshot": {"snapshot_ordinal": int},
        }.get(operation, {})
        for key, expected in fields.items():
            value = request.get(key)
            if type(value) is not expected or (expected is str and not value.strip()) or (expected is int and value < 0):
                raise IntegrationError("REQUEST_STRUCTURE_INVALID")

    def _caller_digest(self, request: Mapping[str, Any]) -> str:
        identity = {
            "adapter_instance_id": self.adapter_instance_id,
            "caller_session_id": request.get("caller_session_id"),
            "caller_thread_id": request.get("caller_thread_id"),
        }
        return sha256_bytes(canonical_bytes(identity))

    def _enter(self, request: Mapping[str, Any]) -> None:
        identity = self._caller_digest(request)
        with self._lock:
            if self._active_identity is not None:
                code = "ADAPTER_REENTRANCY_FORBIDDEN" if self._active_identity == identity else "ADAPTER_OPERATION_IN_FLIGHT"
                raise IntegrationError(code)
            self._active_identity = identity
            self._active_operation_id = str(request.get("operation_id", ""))

    def _exit(self) -> None:
        with self._lock:
            self._active_identity = None
            self._active_operation_id = None

    def _call(self, method: str, args: tuple[Any, ...], request: Mapping[str, Any],
              result_state: str, mutate: Callable[[dict[str, Any]], None] | None = None) -> Mapping[str, Any]:
        before = self.capture_transaction()
        try:
            receipt = getattr(self.backend, method)(*args)
        except Exception as exc:
            self.restore_transaction(before)
            raise IntegrationError("BACKEND_EXCEPTION") from exc
        if not isinstance(receipt, Mapping) or frozenset(receipt) != RECEIPT_FIELDS:
            self.restore_transaction(before); raise IntegrationError("BACKEND_RECEIPT_INVALID")
        digest = lambda v: type(v) is str and len(v) == 64 and not (set(v) - HEX64)
        if (receipt.get("status") not in ("PASS", "FAIL") or
                not self._nonempty(receipt.get("session_id")) or
                not all(digest(receipt.get(k)) for k in ("prior_backend_state_sha256", "result_backend_state_sha256", "request_sha256")) or
                receipt.get("request_ordinal") is not None and type(receipt.get("request_ordinal")) is not int):
            self.restore_transaction(before); raise IntegrationError("BACKEND_RECEIPT_INVALID")
        expected_ordinal = request.get("request_ordinal") if method == "step" else None
        if receipt["request_sha256"] != sha256_bytes(canonical_bytes(dict(request))) or receipt["request_ordinal"] != expected_ordinal:
            self.restore_transaction(before); raise IntegrationError("RESPONSE_CORRELATION_FAILURE")
        if receipt["status"] == "FAIL":
            code = receipt.get("backend_code")
            self.restore_transaction(before)
            if code not in REGISTERED_BACKEND_FAIL_CODES:
                raise IntegrationError("BACKEND_RECEIPT_INVALID")
            raise IntegrationError("BACKEND_DECLARED_FAILURE", backend_code=code)
        if receipt.get("backend_code") is not None:
            self.restore_transaction(before); raise IntegrationError("BACKEND_RECEIPT_INVALID")
        if receipt["session_id"] != self.session_id:
            self.restore_transaction(before); raise IntegrationError("BACKEND_SESSION_MISMATCH")
        if receipt["prior_backend_state_sha256"] != self._backend_state:
            self.restore_transaction(before); raise IntegrationError("BACKEND_STATE_MISMATCH")
        new_state = deepcopy(self._state)
        new_state["lifecycle_state"] = result_state
        if mutate:
            mutate(new_state)
        self._backend_state = str(receipt["result_backend_state_sha256"])
        self._state = new_state
        return frozen(dict(receipt))

    def describe(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        self._enter(request)
        try:
            self._validate_request("describe", request)
            if self._state["lifecycle_state"] != "CREATED": raise IntegrationError("ADAPTER_LIFECYCLE_VIOLATION")
            return self._call("describe", (self.manifest, self.config, frozen(request)), request, "DESCRIBED")
        finally: self._exit()

    def initialize(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        self._enter(request)
        try:
            self._validate_request("initialize", request)
            if self._state["lifecycle_state"] != "DESCRIBED": raise IntegrationError("ADAPTER_LIFECYCLE_VIOLATION")
            session = frozen({"session_id": self.session_id, "caller_session_id": request.get("caller_session_id")})
            description = frozen({"role": self.role, "scientific_arm": self.scientific_arm})
            return self._call("initialize", (description, session, frozen(request)), request, "INITIALIZED")
        finally: self._exit()

    def reset_episode(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        self._enter(request)
        try:
            self._validate_request("reset_episode", request)
            state = self._state["lifecycle_state"]
            if state == "STEPPED" and not self._state["episode_complete"]: raise IntegrationError("EPISODE_NOT_COMPLETE")
            if state not in ("INITIALIZED", "STEPPED"): raise IntegrationError("ADAPTER_LIFECYCLE_VIOLATION")
            episode = request.get("episode_id")
            if episode in self._used_episode_ids: raise IntegrationError("EPISODE_ID_REUSE")
            if request.get("reset_ordinal") != self._state["reset_ordinal"] + 1: raise IntegrationError("RESET_ORDINAL_MISMATCH")
            def mutate(s: dict[str, Any]) -> None:
                s.update(episode_id=episode, episode_complete=False, reset_ordinal=request["reset_ordinal"],
                         next_request_ordinal=0, last_response_sha256=None)
            receipt = self._call("reset_episode", (self._backend_state, frozen(request)), request, "EPISODE_READY", mutate)
            self._used_episode_ids.add(str(episode))
            return receipt
        finally: self._exit()

    def step(self, request: Mapping[str, Any], tokens: PrivateTokenView) -> Mapping[str, Any]:
        self._enter(request)
        try:
            self._validate_request("step", request)
            state = self._state["lifecycle_state"]
            if state == "STEPPED" and self._state["episode_complete"]: raise IntegrationError("EPISODE_ALREADY_COMPLETE")
            if state not in ("EPISODE_READY", "STEPPED"): raise IntegrationError("ADAPTER_LIFECYCLE_VIOLATION")
            if request.get("episode_id") != self._state["episode_id"]: raise IntegrationError("EPISODE_ID_MISMATCH")
            if request.get("request_ordinal") != self._state["next_request_ordinal"]: raise IntegrationError("REQUEST_ORDINAL_MISMATCH")
            if request.get("context_length") != tokens.context_length: raise IntegrationError("CONTEXT_REQUEST_MISMATCH")
            before_view = tokens.sha256
            def mutate(s: dict[str, Any]) -> None:
                s["next_request_ordinal"] += 1
                s["episode_complete"] = bool(request.get("is_terminal_request"))
            before = self.capture_transaction()
            receipt = self._call("step", (self._backend_state, frozen(request), tokens), request, "STEPPED", mutate)
            if tokens.sha256 != before_view:
                self.restore_transaction(before)
                raise IntegrationError("PRIVATE_VIEW_MUTATED")
            self._state["last_response_sha256"] = sha256_bytes(canonical_bytes(dict(receipt)))
            return receipt
        finally: self._exit()

    def snapshot(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        self._enter(request)
        try:
            self._validate_request("snapshot", request)
            if self._state["lifecycle_state"] != "STEPPED": raise IntegrationError("ADAPTER_LIFECYCLE_VIOLATION")
            if request.get("snapshot_ordinal") != self._state["snapshot_ordinal"]: raise IntegrationError("SNAPSHOT_ORDINAL_MISMATCH")
            def mutate(s: dict[str, Any]) -> None: s["snapshot_ordinal"] += 1
            return self._call("snapshot", (self._backend_state, frozen(request)), request, "STEPPED", mutate)
        finally: self._exit()

    def close(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        self._enter(request)
        try:
            self._validate_request("close", request)
            if self._state["lifecycle_state"] not in ("INITIALIZED", "EPISODE_READY", "STEPPED"):
                raise IntegrationError("ADAPTER_LIFECYCLE_VIOLATION")
            def mutate(s: dict[str, Any]) -> None: s["closed"] = True
            return self._call("close", (self._backend_state, frozen(request)), request, "CLOSED", mutate)
        finally: self._exit()


class CandidateAdapter(BaseAdapter): pass
class PeerAdapter(BaseAdapter): pass
class ControlAdapter(BaseAdapter): pass


class AdapterFactory:
    def __init__(self, registry: Mapping[str, tuple[Callable[[], RealBackendProtocol], str, str, str]]):
        self._registry = dict(registry)

    def create(self, role: str, scientific_arm: str, manifest_bytes: bytes,
               backend_config_bytes: bytes, private_token_provider: Callable[[int | str], Sequence[int]]) -> BaseAdapter:
        if role not in ROLE_ARMS or scientific_arm not in ROLE_ARMS[role]: raise IntegrationError("ROLE_ARM_MISMATCH")
        try:
            manifest, config = json.loads(manifest_bytes), json.loads(backend_config_bytes)
        except Exception as exc: raise IntegrationError("STRUCTURAL_SCHEMA_FAILURE") from exc
        if (type(manifest) is not dict or type(config) is not dict or
                canonical_bytes(manifest) != manifest_bytes or canonical_bytes(config) != backend_config_bytes):
            raise IntegrationError("STRUCTURAL_SCHEMA_FAILURE")
        manifest_required = set(PAIR_EQUALITY_FIELDS) | set(PAIR_DIFFERENCE_FIELDS) | {"checkpoint_sha256"}
        config_required = {"backend_name", "implementation_sha256", "dependency_sha256", "model_sha256",
                           "tokenizer_sha256", "adapter_instance_id", "production_path"}
        if set(manifest) != manifest_required or set(config) != config_required:
            raise IntegrationError("STRUCTURAL_SCHEMA_FAILURE")
        digest = lambda v: type(v) is str and len(v) == 64 and not (set(v) - HEX64)
        if (any(not digest(manifest.get(field)) for field in PAIR_EQUALITY_FIELDS
                if field not in ("checkpoint_revision", "weight_hashes", "parameter_count")) or
                type(manifest.get("checkpoint_revision")) is not str or len(manifest["checkpoint_revision"]) != 40 or
                type(manifest.get("weight_hashes")) is not list or not manifest["weight_hashes"] or
                any(not digest(item) for item in manifest["weight_hashes"]) or
                type(manifest.get("parameter_count")) is not int or manifest["parameter_count"] < 1 or
                any(not isinstance(manifest.get(field), str) or not manifest[field] for field in PAIR_DIFFERENCE_FIELDS) or
                any(not digest(config.get(field)) for field in ("implementation_sha256", "dependency_sha256", "model_sha256", "tokenizer_sha256")) or
                type(config.get("adapter_instance_id")) is not str or not config["adapter_instance_id"] or
                type(config.get("production_path")) is not bool):
            raise IntegrationError("STRUCTURAL_SCHEMA_FAILURE")
        backend_name = config.get("backend_name")
        if backend_name == "synthetic" and config.get("production_path", True): raise IntegrationError("SYNTHETIC_FALLBACK_FORBIDDEN")
        if backend_name not in self._registry: raise IntegrationError("BACKEND_NOT_REGISTERED")
        entry = self._registry[backend_name]
        if type(entry) is not tuple or len(entry) != 4: raise IntegrationError("REGISTRY_IDENTITY_MISMATCH")
        constructor, registered_digest, registered_dependency, registered_config = entry
        if config.get("implementation_sha256") != registered_digest: raise IntegrationError("REGISTRY_IDENTITY_MISMATCH")
        if (config["dependency_sha256"] != registered_dependency or
                sha256_bytes(backend_config_bytes) != registered_config or
                config["model_sha256"] != manifest["checkpoint_sha256"] or
                config["tokenizer_sha256"] != manifest["tokenizer_sha256"]):
            raise IntegrationError("REGISTRY_IDENTITY_MISMATCH")
        if manifest.get("role") != role or manifest.get("scientific_arm") != scientific_arm: raise IntegrationError("ROLE_ARM_MISMATCH")
        if role == "peer" and manifest.get("channel_policy") not in ("REDACTED", "BEHAVIOR_ONLY", "OBSERVABLE_ONLY"):
            raise IntegrationError("PEER_CHANNEL_BYPASS")
        cls = {"candidate": CandidateAdapter, "peer": PeerAdapter, "control": ControlAdapter}[role]
        return cls(role, scientific_arm, manifest, config, private_token_provider, constructor())

    def create_pair(self, candidate_manifest_bytes: bytes, peer_manifest_bytes: bytes,
                    candidate_config_bytes: bytes, peer_config_bytes: bytes,
                    private_token_provider: Callable[[int | str], Sequence[int]]) -> tuple[BaseAdapter, BaseAdapter]:
        candidate = self.create("candidate", "candidate", candidate_manifest_bytes, candidate_config_bytes, private_token_provider)
        peer = self.create("peer", "peer", peer_manifest_bytes, peer_config_bytes, private_token_provider)
        try:
            validate_pair_identity(candidate.manifest, peer.manifest)
        except IntegrationError:
            # Construction is coupled: never expose one half of an invalid pair.
            raise
        return candidate, peer


def validate_laws(rows: Sequence[Mapping[str, Any]]) -> tuple[Mapping[str, Any], ...]:
    ids = [row.get("law_id") for row in rows]
    if len(ids) != len(set(ids)): raise IntegrationError("LAW_SET_DUPLICATE")
    if set(ids) != set(LAW_ORDER): raise IntegrationError("LAW_SET_MISSING")
    if tuple(ids) != LAW_ORDER: raise IntegrationError("LAW_ORDER_MISMATCH")
    for row in rows:
        law = row["law_id"]
        if set(row) != {"law_id","status","claim_made","meaning_source","evidence","metrics","failure_code","held_reason"}:
            raise IntegrationError("LAW_PROJECTION_INVALID")
        if row["meaning_source"] != f"docs/ARCHITECTURAL_CONSTITUTION_v2.md:{LAW_LINES[law]}":
            raise IntegrationError("LAW_PROJECTION_INVALID")
        status = row.get("status")
        if status == "HELD":
            valid = (row.get("claim_made") is False and row.get("evidence") == [] and row.get("metrics") == {} and
                     row.get("failure_code") is None and row.get("held_reason") == HELD_REASONS[law])
        elif status == "PASS":
            valid = (row.get("claim_made") is True and type(row.get("evidence")) is list and tuple(row["evidence"]) == LAW_REQUIRED_EVIDENCE[law] and
                     row.get("failure_code") is None and row.get("held_reason") is None and type(row.get("metrics")) is dict)
        elif status == "FAIL":
            valid = (row.get("claim_made") is False and type(row.get("evidence")) is list and bool(row["evidence"]) and
                     row.get("failure_code") in LAW_ALLOWED_FAILURES[law] and row.get("held_reason") is None and type(row.get("metrics")) is dict)
        elif status == "NOT_RUN":
            valid = (row.get("claim_made") is False and type(row.get("evidence")) is list and len(row["evidence"]) == 1 and
                     type(row.get("failure_code")) is str and row["failure_code"].startswith("INSTRUMENT_FAILURE:") and row.get("held_reason") is None)
        else:
            valid = False
        if not valid: raise IntegrationError("LAW_PROJECTION_INVALID")
    return tuple(frozen(row) for row in rows)


def held_law_projection() -> tuple[Mapping[str, Any], ...]:
    return validate_laws([{
        "law_id": law, "status": "HELD", "claim_made": False,
        "meaning_source": f"docs/ARCHITECTURAL_CONSTITUTION_v2.md:{LAW_LINES[law]}",
        "evidence": [], "metrics": {}, "failure_code": None,
        "held_reason": HELD_REASONS[law],
    } for law in LAW_ORDER])


class FanoutCoordinator:
    def __init__(self, provider: Callable[[int | str], Sequence[int]],
                 view_projector: Callable[[str, int, bytes], PrivateTokenView] | None = None,
                 mutation_probe: Callable[[PrivateTokenView], bool] | None = None,
                 post_return_probe: Callable[[PrivateTokenView, PrivateTokenView], bool] | None = None):
        self.provider = provider
        self.view_projector = view_projector or (lambda _role, length, raw: PrivateTokenView(length, bytes(raw)))
        self.mutation_probe = mutation_probe or (lambda _view: False)
        self.post_return_probe = post_return_probe or (lambda _candidate, _peer: False)

    def _phase_one(self, rows: Sequence[Mapping[str, Any]], stop: Mapping[str, Any], context_length: int,
                   candidate: BaseAdapter, peer: BaseAdapter, request: Mapping[str, Any]) -> tuple[PrivateTokenView, PrivateTokenView]:
        expected = (1024, 4096, 8192)
        contexts = tuple(row.get("context_length") for row in rows)
        if len(rows) < 3: raise IntegrationError("SANITIZED_RESULT_MISSING_CONTEXT")
        if len(contexts) != len(set(contexts)): raise IntegrationError("SANITIZED_RESULT_DUPLICATE_CONTEXT")
        if contexts != expected: raise IntegrationError("SANITIZED_RESULT_ORDER_MISMATCH")
        if context_length not in expected: raise IntegrationError("UNSUPPORTED_CONTEXT_LENGTH")
        selected = rows[expected.index(context_length)]
        prompt_items = self.provider(context_length)
        prompt_bytes = encode_private_view(prompt_items)
        if set(selected) != {"context_length","length","sha256","expected_sha256"}:
            raise IntegrationError("SANITIZED_RESULT_IDENTITY_INVALID")
        if selected.get("sha256") != selected.get("expected_sha256"):
            raise IntegrationError("SANITIZED_RESULT_DIGEST_MISMATCH")
        if len(prompt_items) != selected.get("length"): raise IntegrationError("SANITIZED_RESULT_LENGTH_MISMATCH")
        if sha256_bytes(prompt_bytes) != selected.get("expected_sha256"): raise IntegrationError("TOKEN_ARRAY_DIGEST_MISMATCH")
        if set(stop) != {"length", "sha256", "expected_sha256"} or type(stop.get("length")) is not int:
            raise IntegrationError("SANITIZED_STOP_IDENTITY_INVALID")
        if stop.get("sha256") != stop.get("expected_sha256"):
            raise IntegrationError("SANITIZED_STOP_DIGEST_MISMATCH")
        stop_items = self.provider("stop")
        if len(stop_items) != stop["length"]: raise IntegrationError("SANITIZED_STOP_LENGTH_MISMATCH")
        stop_bytes = encode_private_view(stop_items)
        if sha256_bytes(stop_bytes) != stop.get("sha256"): raise IntegrationError("STOP_REDERIVATION_MISMATCH")
        if request.get("context_length") != context_length: raise IntegrationError("CONTEXT_REQUEST_MISMATCH")
        cview = self.view_projector("candidate", context_length, prompt_bytes)
        pview = self.view_projector("peer", context_length, prompt_bytes)
        if type(cview.bytes_view) is not bytes or type(pview.bytes_view) is not bytes:
            raise IntegrationError("PRIVATE_VIEW_MUTATION_ATTEMPT")
        if cview.sha256 != pview.sha256: raise IntegrationError("FANOUT_RECEIVED_DIGEST_MISMATCH")
        if self.mutation_probe(cview) or self.mutation_probe(pview):
            raise IntegrationError("PRIVATE_VIEW_MUTATED")
        return cview, pview

    def step(self, rows: Sequence[Mapping[str, Any]], stop: Mapping[str, Any], context_length: int,
             request: Mapping[str, Any], candidate: BaseAdapter, peer: BaseAdapter) -> Mapping[str, Any]:
        validate_pair_identity(candidate.manifest, peer.manifest)
        candidate_before, peer_before = candidate.capture_transaction(), peer.capture_transaction()
        cview, pview = self._phase_one(rows, stop, context_length, candidate, peer, request)
        try:
            candidate_receipt = candidate.step(request, cview)
        except IntegrationError:
            candidate.restore_transaction(candidate_before); peer.restore_transaction(peer_before); raise
        try:
            peer_receipt = peer.step(request, pview)
        except IntegrationError as exc:
            candidate.restore_transaction(candidate_before); peer.restore_transaction(peer_before)
            raise IntegrationError("FANOUT_ATOMICITY_FAILURE", backend_code=exc.code) from exc
        if cview.sha256 != pview.sha256 or self.post_return_probe(cview, pview):
            candidate.restore_transaction(candidate_before); peer.restore_transaction(peer_before)
            raise IntegrationError("PRIVATE_VIEW_MUTATED")
        request_digest = sha256_bytes(canonical_bytes(dict(request)))
        return frozen({"status": "PASS", "context_id": str(context_length), "context_length": context_length,
                       "length": len(self.provider(context_length)), "expected_sha256": cview.sha256,
                       "candidate_sha256": cview.sha256, "peer_sha256": pview.sha256, "equal": True,
                       "runtime_instance_ids": [candidate.session_id, peer.session_id],
                       "request_sha256": request_digest, "stop_length": stop["length"],
                       "stop_sha256": stop["sha256"], "candidate": candidate_receipt,
                       "peer": peer_receipt, "laws": held_law_projection()})


__all__ = [
    "AdapterFactory", "BaseAdapter", "CandidateAdapter", "ControlAdapter", "FanoutCoordinator",
    "IntegrationError", "ModelAdapterProtocol", "PeerAdapter", "PrivateTokenView", "RealBackendProtocol",
    "canonical_bytes", "encode_private_view", "frozen", "held_law_projection", "sha256_bytes",
    "realize_launch_command", "validate_laws", "validate_pair_identity", "validate_state",
]
