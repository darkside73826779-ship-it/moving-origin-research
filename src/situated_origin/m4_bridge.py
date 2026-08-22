"""Fail-closed bridge from situated-origin context into the real M4 fanout seam.

The M4 coordinator remains the owner of the shared token view and adapter calls.
This bridge binds an additional situated context capability to the candidate only;
it never places that capability in the shared request or peer channel.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import threading
from typing import Any, Callable, Mapping, Protocol, Sequence

from src.m4_post_tokenizer_integration import (
    CandidateAdapter,
    FanoutCoordinator,
    IntegrationError,
    PeerAdapter,
    canonical_bytes as m4_canonical_bytes,
)

from .contracts import SituatedContextPacket, canonical_bytes, sha256_bytes


class M4BridgeError(RuntimeError):
    """Stable local error projection for pre-fanout bridge failures."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class ContextBindingPort(Protocol):
    """Candidate-only backend capability binding.

    Implementations must not expose the packet through the peer backend or the
    public M4 request.  The returned/current value is an opaque packet identity.
    """

    def bind_candidate(
        self, backend: Any, packet: SituatedContextPacket, packet_identity: str
    ) -> str: ...

    def candidate_identity(self, backend: Any) -> str | None: ...

    def peer_is_unbound(self, backend: Any) -> bool: ...

    def clear_candidate(self, backend: Any) -> None: ...


@dataclass(frozen=True)
class CapturedBehavior:
    """One backend output carried outside the seven-field public receipt."""

    role: str
    session_id: str
    request_sha256: str
    output_bytes: bytes
    output_sha256: str


class BehaviorCapturePort(Protocol):
    """Request-scoped local channel for candidate and peer behavior bytes.

    Backends write their actual output to this channel before returning the
    unchanged M4 receipt.  The dispatcher consumes both outputs only after the
    receipt identities have passed the real fanout coordinator.
    """

    def begin_pair(
        self,
        request_sha256: str,
        candidate_session_id: str,
        peer_session_id: str,
    ) -> None: ...

    def record(
        self,
        role: str,
        session_id: str,
        request_sha256: str,
        output_bytes: bytes,
    ) -> None: ...

    def consume_pair(
        self, request_sha256: str
    ) -> tuple[CapturedBehavior, CapturedBehavior]: ...

    def abort_pair(self, request_sha256: str) -> None: ...

    def is_clear(self) -> bool: ...


class LocalBehaviorCapture:
    """Single-pair, fail-closed behavior channel for local execution.

    The channel is intentionally not a backend receipt extension.  It binds
    every raw output to role, runtime session, and exact request digest, rejects
    duplicate or foreign writers, and erases its internal copy on consume or
    abort.  Returned ``CapturedBehavior`` values are immutable caller evidence.
    """

    _ROLES = frozenset(("candidate", "peer"))

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._request_sha256: str | None = None
        self._sessions: dict[str, str] = {}
        self._records: dict[str, CapturedBehavior] = {}

    @staticmethod
    def _digest(value: str) -> bool:
        return (
            type(value) is str
            and len(value) == 64
            and not (set(value) - set("0123456789abcdef"))
        )

    def begin_pair(
        self,
        request_sha256: str,
        candidate_session_id: str,
        peer_session_id: str,
    ) -> None:
        if (
            not self._digest(request_sha256)
            or type(candidate_session_id) is not str
            or not candidate_session_id
            or type(peer_session_id) is not str
            or not peer_session_id
            or candidate_session_id == peer_session_id
        ):
            raise M4BridgeError("BEHAVIOR_CAPTURE_BINDING_INVALID")
        with self._lock:
            if self._request_sha256 is not None:
                raise M4BridgeError("BEHAVIOR_CAPTURE_IN_FLIGHT")
            self._request_sha256 = request_sha256
            self._sessions = {
                "candidate": candidate_session_id,
                "peer": peer_session_id,
            }
            self._records = {}

    def record(
        self,
        role: str,
        session_id: str,
        request_sha256: str,
        output_bytes: bytes,
    ) -> None:
        with self._lock:
            if (
                self._request_sha256 is None
                or request_sha256 != self._request_sha256
                or role not in self._ROLES
                or self._sessions.get(role) != session_id
                or role in self._records
            ):
                raise M4BridgeError("BEHAVIOR_CAPTURE_CORRELATION_FAILURE")
            if type(output_bytes) is not bytes or not output_bytes:
                raise M4BridgeError("BEHAVIOR_OUTPUT_INVALID")
            try:
                output_bytes.decode("utf-8", errors="strict")
            except UnicodeDecodeError as exc:
                raise M4BridgeError("BEHAVIOR_OUTPUT_INVALID") from exc
            self._records[role] = CapturedBehavior(
                role=role,
                session_id=session_id,
                request_sha256=request_sha256,
                output_bytes=bytes(output_bytes),
                output_sha256=sha256_bytes(output_bytes),
            )

    def consume_pair(
        self, request_sha256: str
    ) -> tuple[CapturedBehavior, CapturedBehavior]:
        with self._lock:
            if (
                request_sha256 != self._request_sha256
                or set(self._records) != self._ROLES
            ):
                raise M4BridgeError("BEHAVIOR_CAPTURE_INCOMPLETE")
            candidate = self._records["candidate"]
            peer = self._records["peer"]
            self._clear_locked()
            return candidate, peer

    def abort_pair(self, request_sha256: str) -> None:
        with self._lock:
            if self._request_sha256 is not None and request_sha256 != self._request_sha256:
                raise M4BridgeError("BEHAVIOR_CAPTURE_CORRELATION_FAILURE")
            self._clear_locked()

    def is_clear(self) -> bool:
        with self._lock:
            return (
                self._request_sha256 is None
                and self._sessions == {}
                and self._records == {}
            )

    def _clear_locked(self) -> None:
        self._request_sha256 = None
        self._sessions = {}
        self._records = {}


@dataclass(frozen=True)
class M4BridgeResult:
    fanout_receipt: Mapping[str, Any]
    fanout_execution_model: str
    shared_prompt_sha256: str
    situated_context_sha256: str
    candidate_effective_prompt_sha256: str
    candidate_effective_prompt_token_count: int
    peer_effective_prompt_sha256: str
    peer_effective_prompt_token_count: int
    candidate_behavior: CapturedBehavior | None = None
    peer_behavior: CapturedBehavior | None = None


_FORBIDDEN_LABEL_KEYS = frozenset(
    {
        "answer",
        "answer_key",
        "correct_answer",
        "expected_answer",
        "ground_truth",
        "ground_truth_answer",
        "label",
        "labels",
        "control_label",
        "treatment_label",
        "score",
        "scoring_result",
    }
)
_CANDIDATE_SEPARATOR = "\n\n[SITUATED_CONTEXT_V1]\n"


def _contains_forbidden_label(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in _FORBIDDEN_LABEL_KEYS or _contains_forbidden_label(item):
                return True
    elif isinstance(value, (list, tuple)):
        return any(_contains_forbidden_label(item) for item in value)
    return False


def _token_count(counter: Callable[[str], int], text: str, limit: int) -> int:
    try:
        count = counter(text)
    except Exception as exc:
        raise M4BridgeError("EFFECTIVE_PROMPT_TOKENIZATION_FAILED") from exc
    if type(count) is not int or count < 0:
        raise M4BridgeError("EFFECTIVE_PROMPT_TOKEN_COUNT_INVALID")
    if count > limit:
        raise M4BridgeError("EFFECTIVE_PROMPT_TOKEN_BUDGET_EXCEEDED")
    return count


class SituatedM4Dispatcher:
    """Route one public view through M4 with candidate-only situated context.

    ``FanoutCoordinator.step`` is deliberately described as sequential: the
    repository implementation calls candidate and then peer.  This class makes
    no paired-parallelism claim.
    """

    def __init__(
        self,
        *,
        coordinator: FanoutCoordinator,
        candidate: CandidateAdapter,
        peer: PeerAdapter,
        context_binding: ContextBindingPort,
        token_counter: Callable[[str], int],
        candidate_token_budget: int,
        peer_token_budget: int,
        expected_rows: Sequence[Mapping[str, Any]],
        expected_stop: Mapping[str, Any],
        behavior_capture: BehaviorCapturePort | None = None,
    ):
        if type(candidate_token_budget) is not int or candidate_token_budget < 1:
            raise M4BridgeError("CANDIDATE_TOKEN_BUDGET_INVALID")
        if type(peer_token_budget) is not int or peer_token_budget < 1:
            raise M4BridgeError("PEER_TOKEN_BUDGET_INVALID")
        self._coordinator = coordinator
        self._candidate = candidate
        self._peer = peer
        self._binding = context_binding
        self._counter = token_counter
        self._candidate_budget = candidate_token_budget
        self._peer_budget = peer_token_budget
        self._behavior_capture = behavior_capture
        try:
            self._rows_identity = m4_canonical_bytes(list(deepcopy(expected_rows)))
            self._stop_identity = m4_canonical_bytes(dict(deepcopy(expected_stop)))
        except Exception as exc:
            raise M4BridgeError("SHARED_VIEW_CONTRACT_INVALID") from exc

    def _restore_outer(self, candidate_snapshot: Any, peer_snapshot: Any) -> None:
        try:
            self._candidate.restore_transaction(candidate_snapshot)
            self._peer.restore_transaction(peer_snapshot)
        except IntegrationError as exc:
            raise M4BridgeError("BRIDGE_ROLLBACK_FAILURE") from exc

    def dispatch(
        self,
        *,
        request: Mapping[str, Any],
        packet: SituatedContextPacket,
        shared_public_prompt: str,
        rows: Sequence[Mapping[str, Any]],
        stop: Mapping[str, Any],
        context_length: int,
    ) -> M4BridgeResult:
        if not isinstance(request, Mapping) or _contains_forbidden_label(request):
            raise M4BridgeError("ANSWER_OR_CONTROL_LABEL_FORBIDDEN")
        if type(packet) is not SituatedContextPacket:
            raise M4BridgeError("SITUATED_CONTEXT_PACKET_INVALID")
        if type(shared_public_prompt) is not str or not shared_public_prompt:
            raise M4BridgeError("SHARED_PUBLIC_PROMPT_INVALID")
        if _contains_forbidden_label({"packet": packet.rendered_text}):
            raise M4BridgeError("ANSWER_OR_CONTROL_LABEL_FORBIDDEN")
        if sha256_bytes(shared_public_prompt.encode("utf-8")) != packet.shared_question_sha256:
            raise M4BridgeError("SHARED_QUESTION_IDENTITY_MISMATCH")
        if sha256_bytes(packet.rendered_text.encode("utf-8")) != packet.rendered_sha256:
            raise M4BridgeError("SITUATED_CONTEXT_RENDER_IDENTITY_MISMATCH")
        try:
            if m4_canonical_bytes(list(deepcopy(rows))) != self._rows_identity:
                raise M4BridgeError("SHARED_ROWS_IDENTITY_MISMATCH")
            if m4_canonical_bytes(dict(deepcopy(stop))) != self._stop_identity:
                raise M4BridgeError("SHARED_STOP_IDENTITY_MISMATCH")
        except M4BridgeError:
            raise
        except Exception as exc:
            raise M4BridgeError("SHARED_VIEW_CONTRACT_INVALID") from exc
        if type(context_length) is not int or request.get("context_length") != context_length:
            raise M4BridgeError("CONTEXT_REQUEST_MISMATCH")

        request_snapshot = deepcopy(dict(request))
        request_identity = m4_canonical_bytes(request_snapshot)
        request_sha256 = sha256_bytes(request_identity)
        packet_identity = sha256_bytes(canonical_bytes(packet))
        candidate_prompt = shared_public_prompt + _CANDIDATE_SEPARATOR + packet.rendered_text
        peer_prompt = shared_public_prompt
        candidate_count = _token_count(self._counter, candidate_prompt, self._candidate_budget)
        peer_count = _token_count(self._counter, peer_prompt, self._peer_budget)

        candidate_before = self._candidate.capture_transaction()
        peer_before = self._peer.capture_transaction()
        bound = False
        completed = False
        capture_started = False
        capture_consumed = False
        try:
            if self._behavior_capture is not None:
                self._behavior_capture.begin_pair(
                    request_sha256,
                    self._candidate.session_id,
                    self._peer.session_id,
                )
                capture_started = True
            try:
                observed = self._binding.bind_candidate(
                    self._candidate.backend, packet, packet_identity
                )
                bound = True
                current = self._binding.candidate_identity(self._candidate.backend)
                peer_clear = self._binding.peer_is_unbound(self._peer.backend)
            except Exception as exc:
                self._restore_outer(candidate_before, peer_before)
                raise M4BridgeError("SITUATED_CONTEXT_BINDING_FAILED") from exc
            if observed != packet_identity or current != packet_identity or peer_clear is not True:
                self._restore_outer(candidate_before, peer_before)
                raise M4BridgeError("SITUATED_CONTEXT_BINDING_MISMATCH")

            try:
                receipt = self._coordinator.step(
                    rows,
                    stop,
                    context_length,
                    request_snapshot,
                    self._candidate,
                    self._peer,
                )
            except Exception:
                self._restore_outer(candidate_before, peer_before)
                raise

            try:
                current = self._binding.candidate_identity(self._candidate.backend)
                peer_clear = self._binding.peer_is_unbound(self._peer.backend)
            except Exception as exc:
                self._restore_outer(candidate_before, peer_before)
                raise M4BridgeError("SITUATED_CONTEXT_POST_RETURN_UNVERIFIABLE") from exc
            if (
                m4_canonical_bytes(request_snapshot) != request_identity
                or sha256_bytes(canonical_bytes(packet)) != packet_identity
                or current != packet_identity
                or peer_clear is not True
            ):
                self._restore_outer(candidate_before, peer_before)
                raise M4BridgeError("SITUATED_CONTEXT_POST_RETURN_DRIFT")
            candidate_behavior: CapturedBehavior | None = None
            peer_behavior: CapturedBehavior | None = None
            if self._behavior_capture is not None:
                try:
                    candidate_behavior, peer_behavior = self._behavior_capture.consume_pair(
                        request_sha256
                    )
                    capture_consumed = True
                    candidate_receipt = receipt.get("candidate")
                    peer_receipt = receipt.get("peer")
                    if (
                        not isinstance(candidate_receipt, Mapping)
                        or not isinstance(peer_receipt, Mapping)
                        or candidate_behavior.role != "candidate"
                        or peer_behavior.role != "peer"
                        or candidate_behavior.session_id
                        != candidate_receipt.get("session_id")
                        or peer_behavior.session_id != peer_receipt.get("session_id")
                        or candidate_behavior.request_sha256
                        != candidate_receipt.get("request_sha256")
                        or peer_behavior.request_sha256
                        != peer_receipt.get("request_sha256")
                        or candidate_behavior.request_sha256 != request_sha256
                        or peer_behavior.request_sha256 != request_sha256
                        or sha256_bytes(candidate_behavior.output_bytes)
                        != candidate_behavior.output_sha256
                        or sha256_bytes(peer_behavior.output_bytes)
                        != peer_behavior.output_sha256
                    ):
                        raise M4BridgeError("BEHAVIOR_CAPTURE_RECEIPT_MISMATCH")
                except Exception as exc:
                    self._restore_outer(candidate_before, peer_before)
                    if isinstance(exc, M4BridgeError):
                        raise
                    raise M4BridgeError("BEHAVIOR_CAPTURE_INVALID") from exc
            completed = True
            return M4BridgeResult(
                fanout_receipt=receipt,
                fanout_execution_model="SEQUENTIAL_CANDIDATE_THEN_PEER",
                shared_prompt_sha256=packet.shared_question_sha256,
                situated_context_sha256=packet_identity,
                candidate_effective_prompt_sha256=sha256_bytes(candidate_prompt.encode("utf-8")),
                candidate_effective_prompt_token_count=candidate_count,
                peer_effective_prompt_sha256=sha256_bytes(peer_prompt.encode("utf-8")),
                peer_effective_prompt_token_count=peer_count,
                candidate_behavior=candidate_behavior,
                peer_behavior=peer_behavior,
            )
        finally:
            if capture_started and not capture_consumed and self._behavior_capture is not None:
                try:
                    self._behavior_capture.abort_pair(request_sha256)
                except Exception as exc:
                    self._restore_outer(candidate_before, peer_before)
                    raise M4BridgeError("BEHAVIOR_CAPTURE_CLEAR_FAILED") from exc
            if bound and completed:
                try:
                    self._binding.clear_candidate(self._candidate.backend)
                except Exception as exc:
                    self._restore_outer(candidate_before, peer_before)
                    raise M4BridgeError("SITUATED_CONTEXT_CLEAR_FAILED") from exc


__all__ = [
    "BehaviorCapturePort",
    "CapturedBehavior",
    "ContextBindingPort",
    "LocalBehaviorCapture",
    "M4BridgeError",
    "M4BridgeResult",
    "SituatedM4Dispatcher",
]
