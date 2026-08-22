"""One-vehicle adapter joining the situated runtime to the real M4 fanout.

This module is deliberately model-neutral.  It does not synthesize behavior
from an M4 receipt: candidate and peer backends must place their actual output
bytes on the correlated local behavior channel owned by ``m4_bridge``.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .contracts import SituatedContextPacket, sha256_bytes
from .m4_bridge import CapturedBehavior, M4BridgeError, SituatedM4Dispatcher


class AssemblyError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


_FORBIDDEN_FIELDS = frozenset(
    {
        "answer",
        "answer_label",
        "correct_answer",
        "expected_answer",
        "ground_truth",
        "ground_truth_answer",
        "label",
        "target_label",
        "control_label",
        "score",
        "scoring_result",
    }
)


def _reject_forbidden_fields(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).strip().casefold().replace("-", "_") in _FORBIDDEN_FIELDS:
                raise AssemblyError("GROUND_TRUTH_OR_SCORE_FIELD_FORBIDDEN")
            _reject_forbidden_fields(item)
    elif isinstance(value, (tuple, list)):
        for item in value:
            _reject_forbidden_fields(item)


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _behavior_row(value: CapturedBehavior) -> dict[str, Any]:
    try:
        output_text = value.output_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise AssemblyError("BEHAVIOR_OUTPUT_INVALID") from exc
    return {
        "role": value.role,
        "session_id": value.session_id,
        "request_sha256": value.request_sha256,
        "output_sha256": value.output_sha256,
        "output_text": output_text,
    }


class BackendSituatedContextBinding:
    """Bind context through explicit backend methods, never shared request data."""

    def bind_candidate(
        self, backend: Any, packet: SituatedContextPacket, packet_identity: str
    ) -> str:
        method = getattr(backend, "bind_situated_context", None)
        if not callable(method):
            raise M4BridgeError("SITUATED_CONTEXT_BINDING_UNAVAILABLE")
        return method(packet, packet_identity)

    def candidate_identity(self, backend: Any) -> str | None:
        method = getattr(backend, "situated_context_identity", None)
        if not callable(method):
            raise M4BridgeError("SITUATED_CONTEXT_BINDING_UNAVAILABLE")
        return method()

    def peer_is_unbound(self, backend: Any) -> bool:
        method = getattr(backend, "situated_context_identity", None)
        if not callable(method):
            raise M4BridgeError("SITUATED_CONTEXT_BINDING_UNAVAILABLE")
        return method() is None

    def clear_candidate(self, backend: Any) -> None:
        method = getattr(backend, "clear_situated_context", None)
        if not callable(method):
            raise M4BridgeError("SITUATED_CONTEXT_BINDING_UNAVAILABLE")
        method()


class M4VehiclePairDispatcher:
    """Adapt one situated vehicle request to the real M4 pair coordinator."""

    def __init__(
        self,
        *,
        dispatcher: SituatedM4Dispatcher,
        rows: Sequence[Mapping[str, Any]],
        stop: Mapping[str, Any],
        default_context_length: int = 1024,
    ) -> None:
        if type(default_context_length) is not int or default_context_length < 1:
            raise AssemblyError("CONTEXT_LENGTH_INVALID")
        self._dispatcher = dispatcher
        self._rows = tuple(_plain(item) for item in rows)
        self._stop = _plain(stop)
        self._default_context_length = default_context_length

    @staticmethod
    def _prompt(request: Mapping[str, Any]) -> str:
        value = request.get("question", request.get("content"))
        if type(value) is not str or not value.strip():
            raise AssemblyError("SHARED_PUBLIC_PROMPT_INVALID")
        return value

    def _m4_request(self, request: Mapping[str, Any]) -> dict[str, Any]:
        request_id = str(request.get("id", "")).strip()
        if not request_id:
            raise AssemblyError("PUBLIC_REQUEST_ID_REQUIRED")
        output = _plain(request)
        output.setdefault("operation_id", f"situated-step:{request_id}")
        output.setdefault("caller_session_id", "situated-origin-vehicle")
        output.setdefault("caller_thread_id", "vehicle-main")
        output.setdefault("episode_id", "situated-origin-episode")
        output.setdefault("request_ordinal", 0)
        output.setdefault("context_length", self._default_context_length)
        output.setdefault("is_terminal_request", True)
        return output

    def dispatch(
        self,
        request: Mapping[str, Any],
        *,
        candidate_capability: Any | None,
        peer_capability: None,
    ) -> Mapping[str, Any]:
        _reject_forbidden_fields(request)
        if peer_capability is not None:
            raise AssemblyError("PEER_CONTEXT_CAPABILITY_FORBIDDEN")
        if type(candidate_capability) is not SituatedContextPacket:
            raise AssemblyError("SITUATED_CONTEXT_PACKET_REQUIRED")
        public_prompt = self._prompt(request)
        m4_request = self._m4_request(request)
        result = self._dispatcher.dispatch(
            request=m4_request,
            packet=candidate_capability,
            shared_public_prompt=public_prompt,
            rows=self._rows,
            stop=self._stop,
            context_length=m4_request["context_length"],
        )
        if result.candidate_behavior is None or result.peer_behavior is None:
            raise AssemblyError("BEHAVIOR_CAPTURE_REQUIRED")
        candidate = _behavior_row(result.candidate_behavior)
        peer = _behavior_row(result.peer_behavior)
        fanout = _plain(result.fanout_receipt)
        evidence = {
            "fanout_receipt": fanout,
            "fanout_execution_model": result.fanout_execution_model,
            "shared_prompt_sha256": result.shared_prompt_sha256,
            "situated_context_sha256": result.situated_context_sha256,
            "candidate_effective_prompt_sha256": result.candidate_effective_prompt_sha256,
            "candidate_effective_prompt_token_count": result.candidate_effective_prompt_token_count,
            "peer_effective_prompt_sha256": result.peer_effective_prompt_sha256,
            "peer_effective_prompt_token_count": result.peer_effective_prompt_token_count,
            "selected_event_ids": list(candidate_capability.selected_event_ids),
            "candidate_behavior": candidate,
            "peer_behavior": peer,
            "outputs_equal": candidate["output_sha256"] == peer["output_sha256"],
        }
        response = {
            "status": "PASS",
            "kind": "PUBLIC_OUTPUT",
            "output_text": candidate["output_text"],
            "source": {
                "source_kind": "local-behavior-capture",
                "source_id": (
                    f"candidate:{candidate['session_id']}:{candidate['request_sha256']}"
                ),
                "source_sha256": candidate["output_sha256"],
            },
            "claim_kind": "situated-model-response",
            "supporting_event_ids": list(candidate_capability.selected_event_ids),
            "m4_pair_evidence": evidence,
        }
        _reject_forbidden_fields(response)
        return response


class AssemblyOutputValidator:
    """Strictly validate the response that will enter the origin ledger."""

    _RESPONSE_FIELDS = frozenset(
        (
            "status",
            "kind",
            "output_text",
            "source",
            "claim_kind",
            "supporting_event_ids",
            "m4_pair_evidence",
        )
    )
    _EVIDENCE_FIELDS = frozenset(
        (
            "fanout_receipt",
            "fanout_execution_model",
            "shared_prompt_sha256",
            "situated_context_sha256",
            "candidate_effective_prompt_sha256",
            "candidate_effective_prompt_token_count",
            "peer_effective_prompt_sha256",
            "peer_effective_prompt_token_count",
            "selected_event_ids",
            "candidate_behavior",
            "peer_behavior",
            "outputs_equal",
        )
    )
    _BEHAVIOR_FIELDS = frozenset(
        ("role", "session_id", "request_sha256", "output_sha256", "output_text")
    )

    @staticmethod
    def _digest(value: Any) -> bool:
        return (
            type(value) is str
            and len(value) == 64
            and not (set(value) - set("0123456789abcdef"))
        )

    def validate(self, stage: str, value: Mapping[str, Any]) -> Mapping[str, Any]:
        if stage != "MEASURED" or not isinstance(value, Mapping):
            raise AssemblyError("ASSEMBLY_OUTPUT_STAGE_INVALID")
        _reject_forbidden_fields(value)
        if set(value) != self._RESPONSE_FIELDS:
            raise AssemblyError("ASSEMBLY_OUTPUT_STRUCTURE_INVALID")
        if (
            value.get("status") != "PASS"
            or value.get("kind") != "PUBLIC_OUTPUT"
            or type(value.get("output_text")) is not str
            or not value["output_text"]
            or value.get("claim_kind") != "situated-model-response"
            or type(value.get("supporting_event_ids")) is not list
        ):
            raise AssemblyError("ASSEMBLY_OUTPUT_STRUCTURE_INVALID")
        source = value.get("source")
        evidence = value.get("m4_pair_evidence")
        if (
            not isinstance(source, Mapping)
            or set(source) != {"source_kind", "source_id", "source_sha256"}
            or source.get("source_kind") != "local-behavior-capture"
            or type(source.get("source_id")) is not str
            or not source["source_id"]
            or not self._digest(source.get("source_sha256"))
            or not isinstance(evidence, Mapping)
            or set(evidence) != self._EVIDENCE_FIELDS
        ):
            raise AssemblyError("ASSEMBLY_OUTPUT_STRUCTURE_INVALID")
        candidate = evidence.get("candidate_behavior")
        peer = evidence.get("peer_behavior")
        fanout = evidence.get("fanout_receipt")
        if (
            not isinstance(candidate, Mapping)
            or not isinstance(peer, Mapping)
            or set(candidate) != self._BEHAVIOR_FIELDS
            or set(peer) != self._BEHAVIOR_FIELDS
            or candidate.get("role") != "candidate"
            or peer.get("role") != "peer"
            or not isinstance(fanout, Mapping)
            or fanout.get("status") != "PASS"
            or evidence.get("fanout_execution_model")
            != "SEQUENTIAL_CANDIDATE_THEN_PEER"
            or type(evidence.get("outputs_equal")) is not bool
        ):
            raise AssemblyError("ASSEMBLY_OUTPUT_EVIDENCE_INVALID")
        for row, receipt_name in ((candidate, "candidate"), (peer, "peer")):
            receipt = fanout.get(receipt_name)
            if (
                not isinstance(receipt, Mapping)
                or set(row) != self._BEHAVIOR_FIELDS
                or type(row.get("output_text")) is not str
                or not row["output_text"]
                or not self._digest(row.get("request_sha256"))
                or not self._digest(row.get("output_sha256"))
                or row["session_id"] != receipt.get("session_id")
                or row["request_sha256"] != receipt.get("request_sha256")
                or sha256_bytes(row["output_text"].encode("utf-8"))
                != row["output_sha256"]
            ):
                raise AssemblyError("ASSEMBLY_OUTPUT_EVIDENCE_INVALID")
        if (
            value["output_text"] != candidate["output_text"]
            or source["source_sha256"] != candidate["output_sha256"]
            or source["source_id"]
            != f"candidate:{candidate['session_id']}:{candidate['request_sha256']}"
            or evidence["outputs_equal"]
            is not (candidate["output_sha256"] == peer["output_sha256"])
            or evidence.get("selected_event_ids") != value["supporting_event_ids"]
        ):
            raise AssemblyError("ASSEMBLY_OUTPUT_CORRELATION_FAILURE")
        for name in (
            "shared_prompt_sha256",
            "situated_context_sha256",
            "candidate_effective_prompt_sha256",
            "peer_effective_prompt_sha256",
        ):
            if not self._digest(evidence.get(name)):
                raise AssemblyError("ASSEMBLY_OUTPUT_EVIDENCE_INVALID")
        for name in (
            "candidate_effective_prompt_token_count",
            "peer_effective_prompt_token_count",
        ):
            if type(evidence.get(name)) is not int or evidence[name] < 1:
                raise AssemblyError("ASSEMBLY_OUTPUT_EVIDENCE_INVALID")
        return _plain(value)


__all__ = [
    "AssemblyError",
    "AssemblyOutputValidator",
    "BackendSituatedContextBinding",
    "M4VehiclePairDispatcher",
]
