"""Custody-free full-assembly crash-cart composition.

This module exercises the assembled situated-origin runtime through the real M4
``CandidateAdapter``/``PeerAdapter`` contract.  It deliberately supplies no
model or tokenizer implementation: public synthetic backends may be injected
for topology tests, while a later run can bind the same ports to reviewed local
backends.

Unlike the banked ``FanoutCoordinator.step`` implementation, the pair executor
below is explicitly concurrent.  It reuses the coordinator's phase-one private
view reconciliation, but dispatches the two already-validated adapters on two
workers behind one barrier and restores both complete transactions on any
failure.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, wait
from copy import deepcopy
from dataclasses import asdict, dataclass
import queue
import threading
from typing import Any, Callable, Mapping, Sequence

from src.m4_final_prescoring_crash_cart import (
    ACTIVE_DEADLINE_NS,
    QUEUE_CAPACITY,
    TELEMETRY_INTERVAL_NS,
    active_schedule,
    fixture_inventory,
    held_laws,
    telemetry_schedule,
    warmup_plan,
)
from src.m4_post_tokenizer_integration import (
    CandidateAdapter,
    FanoutCoordinator,
    IntegrationError,
    PeerAdapter,
    RECEIPT_FIELDS,
    canonical_bytes as m4_canonical_bytes,
    validate_pair_identity,
)

from .contracts import SituatedContextPacket, canonical_bytes, sha256_bytes
from .m4_bridge import (
    BehaviorCapturePort,
    CapturedBehavior,
    ContextBindingPort,
    M4BridgeError,
)
from .runtime import SituatedRuntime


class FullCrashCartError(RuntimeError):
    """Stable failure projection for the full-assembly observation runner."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class ParallelPairObservation:
    request_sha256: str
    execution_model: str
    candidate_receipt: Mapping[str, Any]
    peer_receipt: Mapping[str, Any]
    candidate_behavior: CapturedBehavior
    peer_behavior: CapturedBehavior
    shared_prompt_sha256: str
    situated_context_sha256: str | None
    candidate_effective_prompt_sha256: str
    peer_effective_prompt_sha256: str
    candidate_effective_prompt_token_count: int
    peer_effective_prompt_token_count: int


def _digest(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and not (set(value) - set("0123456789abcdef"))
    )


def _failure_code(exc: BaseException) -> str:
    code = getattr(exc, "code", None)
    return code if type(code) is str and code else type(exc).__name__


def _behavior(value: CapturedBehavior) -> dict[str, Any]:
    try:
        text = value.output_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise FullCrashCartError("BEHAVIOR_OUTPUT_INVALID") from exc
    return {
        "role": value.role,
        "session_id": value.session_id,
        "request_sha256": value.request_sha256,
        "output_sha256": value.output_sha256,
        "raw_output_text": text,
    }


class ParallelAtomicM4Pair:
    """Two-worker atomic executor over the real M4 adapters.

    Phase-one token/stop reconciliation is owned by the existing
    ``FanoutCoordinator``.  Adapter/backend/capture snapshots are taken before
    candidate context binding, and both roles are restored on every failure.
    """

    EXECUTION_MODEL = "PARALLEL_TWO_WORKER_SINGLE_BARRIER"
    _CANDIDATE_SEPARATOR = "\n\n[SITUATED_CONTEXT_V1]\n"

    def __init__(
        self,
        *,
        coordinator: FanoutCoordinator,
        candidate: CandidateAdapter,
        peer: PeerAdapter,
        context_binding: ContextBindingPort,
        behavior_capture: BehaviorCapturePort,
        token_counter: Callable[[str], int],
        candidate_token_budget: int,
        peer_token_budget: int,
        rows: Sequence[Mapping[str, Any]],
        stop: Mapping[str, Any],
        barrier_timeout_seconds: float = 5.0,
    ) -> None:
        if type(candidate_token_budget) is not int or candidate_token_budget < 1:
            raise FullCrashCartError("CANDIDATE_TOKEN_BUDGET_INVALID")
        if type(peer_token_budget) is not int or peer_token_budget < 1:
            raise FullCrashCartError("PEER_TOKEN_BUDGET_INVALID")
        if barrier_timeout_seconds <= 0:
            raise FullCrashCartError("PAIR_BARRIER_TIMEOUT_INVALID")
        validate_pair_identity(candidate.manifest, peer.manifest)
        self.coordinator = coordinator
        self.candidate = candidate
        self.peer = peer
        self.binding = context_binding
        self.capture = behavior_capture
        self.token_counter = token_counter
        self.candidate_token_budget = candidate_token_budget
        self.peer_token_budget = peer_token_budget
        self.rows = tuple(deepcopy(list(rows)))
        self.stop = deepcopy(dict(stop))
        self.barrier_timeout_seconds = float(barrier_timeout_seconds)
        self.reset_receipts: list[dict[str, Any]] = []
        self.cleanup_count = 0
        self.finalize_call_count = 0
        self._finalized = False
        # Both adapters are required to arrive initialized.  This clean session
        # baseline makes failure cleanup able to perform a legal final reset
        # even when the active episode stopped before its terminal request.
        self._candidate_session_base = self.candidate.capture_transaction()
        self._peer_session_base = self.peer.capture_transaction()

    def _count(self, text: str, limit: int) -> int:
        try:
            value = self.token_counter(text)
        except Exception as exc:
            raise FullCrashCartError("EFFECTIVE_PROMPT_TOKENIZATION_FAILED") from exc
        if type(value) is not int or value < 1:
            raise FullCrashCartError("EFFECTIVE_PROMPT_TOKEN_COUNT_INVALID")
        if value > limit:
            raise FullCrashCartError("EFFECTIVE_PROMPT_TOKEN_BUDGET_EXCEEDED")
        return value

    @staticmethod
    def _restore(adapter: CandidateAdapter | PeerAdapter, snapshot: Any) -> None:
        try:
            adapter.restore_transaction(snapshot)
        except Exception as exc:
            raise FullCrashCartError("PAIR_ROLLBACK_FAILURE") from exc

    def _restore_pair(self, candidate_snapshot: Any, peer_snapshot: Any) -> None:
        first: BaseException | None = None
        for adapter, snapshot in (
            (self.candidate, candidate_snapshot),
            (self.peer, peer_snapshot),
        ):
            try:
                self._restore(adapter, snapshot)
            except BaseException as exc:
                first = first or exc
        if first is not None:
            raise first

    @staticmethod
    def _validate_receipt(
        receipt: Mapping[str, Any],
        *,
        role: str,
        session_id: str,
        request_sha256: str,
        request_ordinal: int | None,
        prior_state_sha256: str,
    ) -> None:
        if (
            not isinstance(receipt, Mapping)
            or set(receipt) != set(RECEIPT_FIELDS)
            or receipt.get("status") != "PASS"
            or receipt.get("backend_code") is not None
            or receipt.get("session_id") != session_id
            or receipt.get("request_sha256") != request_sha256
            or receipt.get("request_ordinal") != request_ordinal
            or receipt.get("prior_backend_state_sha256") != prior_state_sha256
            or not _digest(receipt.get("result_backend_state_sha256"))
        ):
            raise FullCrashCartError(f"{role.upper()}_RECEIPT_INVALID")

    def _run_two(
        self,
        candidate_call: Callable[[], Mapping[str, Any]],
        peer_call: Callable[[], Mapping[str, Any]],
    ) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
        barrier = threading.Barrier(2)

        def invoke(call: Callable[[], Mapping[str, Any]]) -> Mapping[str, Any]:
            try:
                barrier.wait(timeout=self.barrier_timeout_seconds)
            except threading.BrokenBarrierError as exc:
                raise FullCrashCartError("PAIR_BARRIER_FAILED") from exc
            return call()

        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="m4-pair") as pool:
            futures = (pool.submit(invoke, candidate_call), pool.submit(invoke, peer_call))
            wait(futures)
            errors = [future.exception() for future in futures if future.exception()]
            if errors:
                raise errors[0]  # both workers have crossed the barrier and terminated
            return futures[0].result(), futures[1].result()

    def reset_pair(self, *, phase: str, episode_id: str, reset_ordinal: int) -> None:
        if not phase or not episode_id or type(reset_ordinal) is not int or reset_ordinal < 0:
            raise FullCrashCartError("RESET_REQUEST_INVALID")
        candidate_before = self.candidate.capture_transaction()
        peer_before = self.peer.capture_transaction()
        common = {
            "operation_id": f"full-crash-cart-reset:{phase}",
            "caller_session_id": "full-crash-cart",
            "caller_thread_id": "pair-controller",
            "episode_id": episode_id,
            "reset_ordinal": reset_ordinal,
        }
        request_sha256 = sha256_bytes(m4_canonical_bytes(common))
        try:
            candidate_receipt, peer_receipt = self._run_two(
                lambda: self.candidate.reset_episode(common),
                lambda: self.peer.reset_episode(common),
            )
            self._validate_receipt(
                candidate_receipt,
                role="candidate",
                session_id=self.candidate.session_id,
                request_sha256=request_sha256,
                request_ordinal=None,
                prior_state_sha256=candidate_before[0][1],
            )
            self._validate_receipt(
                peer_receipt,
                role="peer",
                session_id=self.peer.session_id,
                request_sha256=request_sha256,
                request_ordinal=None,
                prior_state_sha256=peer_before[0][1],
            )
            if candidate_receipt["session_id"] == peer_receipt["session_id"]:
                raise FullCrashCartError("SHARED_SESSION_INVALID")
        except BaseException:
            self._restore_pair(candidate_before, peer_before)
            raise
        self.reset_receipts.append(
            {
                "phase": phase,
                "episode_id": episode_id,
                "reset_ordinal": reset_ordinal,
                "candidate": dict(candidate_receipt),
                "peer": dict(peer_receipt),
            }
        )

    def clean_barrier_receipt(self, *, episode_id: str) -> dict[str, Any]:
        """Attest that the measured episode is clean before RNG insertion."""

        candidate_state, candidate_backend_state = self.candidate.capture()
        peer_state, peer_backend_state = self.peer.capture()
        for role, state in (("candidate", candidate_state), ("peer", peer_state)):
            if (
                state.get("lifecycle_state") != "EPISODE_READY"
                or state.get("episode_id") != episode_id
                or state.get("next_request_ordinal") != 0
                or state.get("episode_complete") is not False
            ):
                raise FullCrashCartError(f"{role.upper()}_CLEAN_BARRIER_INVALID")
        if (
            self.capture.is_clear() is not True
            or self.binding.candidate_identity(self.candidate.backend) is not None
            or self.binding.peer_is_unbound(self.peer.backend) is not True
        ):
            raise FullCrashCartError("CLEAN_BARRIER_RESIDUE")
        return {
            "status": "PASS",
            "episode_id": episode_id,
            "candidate_backend_state_sha256": candidate_backend_state,
            "peer_backend_state_sha256": peer_backend_state,
            "candidate_adapter_state_sha256": sha256_bytes(
                m4_canonical_bytes(candidate_state)
            ),
            "peer_adapter_state_sha256": sha256_bytes(m4_canonical_bytes(peer_state)),
            "next_request_ordinal": 0,
            "capture_clear": True,
            "candidate_context_clear": True,
            "peer_context_clear": True,
        }

    def dispatch(
        self,
        *,
        request: Mapping[str, Any],
        shared_public_prompt: str,
        packet: SituatedContextPacket | None,
        context_length: int = 1024,
    ) -> ParallelPairObservation:
        if not isinstance(request, Mapping) or type(shared_public_prompt) is not str:
            raise FullCrashCartError("PAIR_REQUEST_INVALID")
        request_snapshot = deepcopy(dict(request))
        request_identity = m4_canonical_bytes(request_snapshot)
        request_sha256 = sha256_bytes(request_identity)
        shared_prompt_sha256 = sha256_bytes(shared_public_prompt.encode("utf-8"))
        if packet is not None:
            if type(packet) is not SituatedContextPacket:
                raise FullCrashCartError("SITUATED_CONTEXT_PACKET_INVALID")
            if packet.shared_question_sha256 != shared_prompt_sha256:
                raise FullCrashCartError("SHARED_QUESTION_IDENTITY_MISMATCH")
            if sha256_bytes(packet.rendered_text.encode("utf-8")) != packet.rendered_sha256:
                raise FullCrashCartError("SITUATED_CONTEXT_RENDER_IDENTITY_MISMATCH")

        cview, pview, _length, _prompt_digest, _stop_length, _stop_digest = (
            self.coordinator._phase_one(
                self.rows,
                self.stop,
                context_length,
                self.candidate,
                self.peer,
                request_snapshot,
            )
        )
        if cview.sha256 != pview.sha256:
            raise FullCrashCartError("FANOUT_RECEIVED_DIGEST_MISMATCH")
        candidate_prompt = shared_public_prompt
        packet_identity: str | None = None
        if packet is not None:
            packet_identity = sha256_bytes(canonical_bytes(packet))
            candidate_prompt += self._CANDIDATE_SEPARATOR + packet.rendered_text
        candidate_count = self._count(candidate_prompt, self.candidate_token_budget)
        peer_count = self._count(shared_public_prompt, self.peer_token_budget)

        candidate_before = self.candidate.capture_transaction()
        peer_before = self.peer.capture_transaction()
        capture_started = False
        consumed = False
        try:
            self.capture.begin_pair(
                request_sha256, self.candidate.session_id, self.peer.session_id
            )
            capture_started = True
            if packet is None:
                if (
                    self.binding.candidate_identity(self.candidate.backend) is not None
                    or self.binding.peer_is_unbound(self.peer.backend) is not True
                ):
                    raise FullCrashCartError("WARMUP_SITUATED_PRIVILEGE_FORBIDDEN")
            else:
                observed = self.binding.bind_candidate(
                    self.candidate.backend, packet, packet_identity
                )
                if (
                    observed != packet_identity
                    or self.binding.candidate_identity(self.candidate.backend)
                    != packet_identity
                    or self.binding.peer_is_unbound(self.peer.backend) is not True
                ):
                    raise FullCrashCartError("SITUATED_CONTEXT_BINDING_MISMATCH")

            candidate_receipt, peer_receipt = self._run_two(
                lambda: self.candidate.step(request_snapshot, cview),
                lambda: self.peer.step(request_snapshot, pview),
            )
            if (
                m4_canonical_bytes(request_snapshot) != request_identity
                or cview.sha256 != pview.sha256
                or self.coordinator.post_return_probe(cview, pview)
            ):
                raise FullCrashCartError("PAIR_POST_RETURN_DRIFT")
            self._validate_receipt(
                candidate_receipt,
                role="candidate",
                session_id=self.candidate.session_id,
                request_sha256=request_sha256,
                request_ordinal=request_snapshot.get("request_ordinal"),
                prior_state_sha256=candidate_before[0][1],
            )
            self._validate_receipt(
                peer_receipt,
                role="peer",
                session_id=self.peer.session_id,
                request_sha256=request_sha256,
                request_ordinal=request_snapshot.get("request_ordinal"),
                prior_state_sha256=peer_before[0][1],
            )
            if candidate_receipt["session_id"] == peer_receipt["session_id"]:
                raise FullCrashCartError("SHARED_SESSION_INVALID")
            if packet is not None and (
                self.binding.candidate_identity(self.candidate.backend) != packet_identity
                or self.binding.peer_is_unbound(self.peer.backend) is not True
            ):
                raise FullCrashCartError("SITUATED_CONTEXT_POST_RETURN_DRIFT")
            candidate_behavior, peer_behavior = self.capture.consume_pair(request_sha256)
            consumed = True
            for behavior, receipt, role in (
                (candidate_behavior, candidate_receipt, "candidate"),
                (peer_behavior, peer_receipt, "peer"),
            ):
                if (
                    behavior.role != role
                    or behavior.session_id != receipt["session_id"]
                    or behavior.request_sha256 != request_sha256
                    or sha256_bytes(behavior.output_bytes) != behavior.output_sha256
                ):
                    raise FullCrashCartError("BEHAVIOR_CAPTURE_RECEIPT_MISMATCH")
            if packet is not None:
                self.binding.clear_candidate(self.candidate.backend)
                if self.binding.candidate_identity(self.candidate.backend) is not None:
                    raise FullCrashCartError("SITUATED_CONTEXT_CLEAR_FAILED")
            return ParallelPairObservation(
                request_sha256=request_sha256,
                execution_model=self.EXECUTION_MODEL,
                candidate_receipt=dict(candidate_receipt),
                peer_receipt=dict(peer_receipt),
                candidate_behavior=candidate_behavior,
                peer_behavior=peer_behavior,
                shared_prompt_sha256=shared_prompt_sha256,
                situated_context_sha256=packet_identity,
                candidate_effective_prompt_sha256=sha256_bytes(
                    candidate_prompt.encode("utf-8")
                ),
                peer_effective_prompt_sha256=shared_prompt_sha256,
                candidate_effective_prompt_token_count=candidate_count,
                peer_effective_prompt_token_count=peer_count,
            )
        except BaseException as exc:
            try:
                self._restore_pair(candidate_before, peer_before)
            except BaseException as rollback_exc:
                raise FullCrashCartError("PAIR_ROLLBACK_FAILURE") from rollback_exc
            if isinstance(exc, (FullCrashCartError, IntegrationError, M4BridgeError)):
                raise
            raise FullCrashCartError("PAIR_ATOMICITY_FAILURE") from exc
        finally:
            if capture_started and not consumed:
                try:
                    self.capture.abort_pair(request_sha256)
                except Exception:
                    pass

    def finalize(self, *, reset_ordinal: int, episode_id: str) -> dict[str, Any]:
        """Perform the successful terminal reset, close, dispose, and residue check once."""

        if self._finalized:
            raise FullCrashCartError("PAIR_FINALIZE_REPEATED")
        self._finalized = True
        self.finalize_call_count += 1
        reset_complete = False
        close_complete = False
        try:
            self.reset_pair(
                phase="final", episode_id=episode_id, reset_ordinal=reset_ordinal
            )
            reset_complete = True
            candidate_before = self.candidate.capture_transaction()
            peer_before = self.peer.capture_transaction()
            request = {
                "operation_id": "full-crash-cart-close",
                "caller_session_id": "full-crash-cart",
                "caller_thread_id": "pair-controller",
            }
            request_sha256 = sha256_bytes(m4_canonical_bytes(request))
            candidate_receipt, peer_receipt = self._run_two(
                lambda: self.candidate.close(request),
                lambda: self.peer.close(request),
            )
            self._validate_receipt(
                candidate_receipt,
                role="candidate",
                session_id=self.candidate.session_id,
                request_sha256=request_sha256,
                request_ordinal=None,
                prior_state_sha256=candidate_before[0][1],
            )
            self._validate_receipt(
                peer_receipt,
                role="peer",
                session_id=self.peer.session_id,
                request_sha256=request_sha256,
                request_ordinal=None,
                prior_state_sha256=peer_before[0][1],
            )
            close_complete = True
        finally:
            for backend in (self.candidate.backend, self.peer.backend):
                try:
                    backend.dispose()
                finally:
                    self.cleanup_count += 1
            if self.capture.is_clear() is not True:
                raise FullCrashCartError("BEHAVIOR_CAPTURE_RESIDUE")
            for backend in (self.candidate.backend, self.peer.backend):
                try:
                    live = backend.is_live()
                except Exception as exc:
                    raise FullCrashCartError("BACKEND_RESIDUE_UNVERIFIABLE") from exc
                if live is not False:
                    raise FullCrashCartError("BACKEND_RESIDUE_PRESENT")
        return {
            "final_reset_complete": reset_complete,
            "close_complete": close_complete,
            "disposed_backend_count": self.cleanup_count,
            "finalize_call_count": self.finalize_call_count,
            "capture_clear": self.capture.is_clear(),
            "backend_residue": False,
        }

    def finalize_after_failure(self, *, episode_id: str) -> dict[str, Any]:
        """Restore the initialized session, then perform reset/close/cleanup once."""

        if self._finalized:
            raise FullCrashCartError("PAIR_FINALIZE_REPEATED")
        self._restore_pair(
            self._candidate_session_base,
            self._peer_session_base,
        )
        # The restored canonical initialized state starts with reset ordinal 0.
        return self.finalize(reset_ordinal=1, episode_id=episode_id)


class FullAssemblyCrashCart:
    """Run the public four-warmup/64-measured full assembled topology."""

    def __init__(
        self,
        *,
        runtime: SituatedRuntime,
        pair: ParallelAtomicM4Pair,
        clock_ns: Callable[[], int],
        sleep_until_ns: Callable[[int], None],
        sampler: Callable[[int, int, int], Mapping[str, Any]],
        insert_diagnostic_rng: Callable[[], Mapping[str, Any]],
    ) -> None:
        self.runtime = runtime
        self.pair = pair
        self.clock_ns = clock_ns
        self.sleep_until_ns = sleep_until_ns
        self.sampler = sampler
        self.insert_diagnostic_rng = insert_diagnostic_rng

    @staticmethod
    def _m4_request(
        *,
        phase: str,
        episode_id: str,
        ordinal: int,
        prompt: str,
        controls: Mapping[str, Any],
    ) -> dict[str, Any]:
        return {
            "operation_id": f"full-crash-cart:{phase}:{ordinal}",
            "caller_session_id": "full-crash-cart",
            "caller_thread_id": "pair-controller",
            "episode_id": episode_id,
            "request_ordinal": ordinal,
            "context_length": 1024,
            "is_terminal_request": ordinal == (3 if phase == "warmup" else 63),
            "id": f"{phase}-{ordinal:04d}",
            "question": prompt,
            "content": prompt,
            "controls": deepcopy(dict(controls)),
        }

    @staticmethod
    def _pair_row(
        observation: ParallelPairObservation,
        *,
        ordinal: int,
        prompt: str,
        selected_event_ids: Sequence[str] = (),
    ) -> dict[str, Any]:
        return {
            "ordinal": ordinal,
            "public_prompt_text": prompt,
            "public_prompt_sha256": observation.shared_prompt_sha256,
            "execution_model": observation.execution_model,
            "request_sha256": observation.request_sha256,
            "situated_context_sha256": observation.situated_context_sha256,
            "selected_event_ids": list(selected_event_ids),
            "candidate": _behavior(observation.candidate_behavior),
            "peer": _behavior(observation.peer_behavior),
            "candidate_receipt": dict(observation.candidate_receipt),
            "peer_receipt": dict(observation.peer_receipt),
            "candidate_effective_prompt_sha256": (
                observation.candidate_effective_prompt_sha256
            ),
            "peer_effective_prompt_sha256": observation.peer_effective_prompt_sha256,
            "candidate_effective_prompt_token_count": (
                observation.candidate_effective_prompt_token_count
            ),
            "peer_effective_prompt_token_count": (
                observation.peer_effective_prompt_token_count
            ),
        }

    def _telemetry_until(
        self,
        *,
        samples: list[Mapping[str, Any]],
        next_ns: int,
        observed_ns: int,
        completed: int,
        depth: int,
    ) -> int:
        while next_ns <= observed_ns:
            row = dict(self.sampler(next_ns, completed, depth))
            if row.get("monotonic_ns") != next_ns:
                raise FullCrashCartError("TELEMETRY_OBSERVATION_INVALID")
            samples.append(row)
            next_ns += TELEMETRY_INTERVAL_NS
        return next_ns

    def run(self) -> dict[str, Any]:
        warmup_rows: list[dict[str, Any]] = []
        active_rows: list[dict[str, Any]] = []
        samples: list[Mapping[str, Any]] = []
        failure_code: str | None = None
        cleanup: dict[str, Any] = {
            "final_reset_complete": False,
            "close_complete": False,
            "disposed_backend_count": 0,
            "finalize_call_count": 0,
            "capture_clear": False,
            "backend_residue": None,
        }
        queue_metrics = {
            "capacity": QUEUE_CAPACITY,
            "max_depth": 0,
            "producer_block_count": 0,
            "drop_count": 0,
            "consumed_ordinals": [],
        }
        rng_receipt: Mapping[str, Any] | None = None
        clean_barrier_receipt: Mapping[str, Any] | None = None
        measured_started_ns: int | None = None
        measured_completed_ns: int | None = None
        active_episode = "full-crash-cart-measured"
        active_turn_open = False
        producer: threading.Thread | None = None

        try:
            self.pair.reset_pair(
                phase="warmup", episode_id="full-crash-cart-warmup", reset_ordinal=1
            )
            for plan in warmup_plan():
                prompt = plan["prompt"].decode("utf-8", errors="strict")
                controls = {key: value for key, value in plan.items() if key != "prompt"}
                request = self._m4_request(
                    phase="warmup",
                    episode_id="full-crash-cart-warmup",
                    ordinal=plan["ordinal"],
                    prompt=prompt,
                    controls=controls,
                )
                observation = self.pair.dispatch(
                    request=request, shared_public_prompt=prompt, packet=None
                )
                warmup_rows.append(
                    self._pair_row(observation, ordinal=plan["ordinal"], prompt=prompt)
                )

            self.pair.reset_pair(
                phase="measured", episode_id=active_episode, reset_ordinal=2
            )
            self.runtime.clean_barrier()
            clean_barrier_receipt = self.pair.clean_barrier_receipt(
                episode_id=active_episode
            )
            clean_barrier_head = self.runtime.head
            rng_receipt = dict(self.insert_diagnostic_rng())
            if rng_receipt.get("inserted_after_log_head") != clean_barrier_head:
                raise FullCrashCartError("POST_BARRIER_RNG_INSERTION_INVALID")

            work_queue: queue.Queue[Any] = queue.Queue(maxsize=QUEUE_CAPACITY)
            inventory = fixture_inventory()
            inventory_ready = threading.Event()
            refilled = threading.Event()
            producer_done = threading.Event()
            sentinel = object()

            def produce() -> None:
                for index, (fixture, offset) in enumerate(
                    zip(inventory, active_schedule())
                ):
                    if index >= QUEUE_CAPACITY:
                        # The consumer/refill handshake below guarantees that
                        # this is a real bounded put behind a full queue.
                        queue_metrics["producer_block_count"] += 1
                    work_queue.put((fixture, offset))
                    queue_metrics["max_depth"] = max(
                        queue_metrics["max_depth"], work_queue.qsize()
                    )
                    if index >= QUEUE_CAPACITY:
                        refilled.set()
                    if work_queue.qsize() == QUEUE_CAPACITY:
                        inventory_ready.set()
                work_queue.put(sentinel)
                producer_done.set()
                refilled.set()

            producer = threading.Thread(
                target=produce, name="full-crash-cart-producer", daemon=False
            )
            producer.start()
            if not inventory_ready.wait(timeout=5.0):
                raise FullCrashCartError("BOUNDED_QUEUE_START_FAILED")

            measured_started_ns = self.clock_ns()
            next_sample_ns = measured_started_ns
            while True:
                refilled.clear()
                queued = work_queue.get()
                if queued is sentinel:
                    work_queue.task_done()
                    break
                # Do not take another item until the producer has used the
                # newly available slot.  This preserves a real full-capacity
                # bounded queue while making diagnostic queue telemetry
                # deterministic under the injected fake clock.
                if not producer_done.is_set() and not refilled.wait(timeout=5.0):
                    raise FullCrashCartError("BOUNDED_QUEUE_REFILL_FAILED")
                fixture, offset = queued
                ordinal = fixture["ordinal"]
                expected_ordinal = len(active_rows)
                if ordinal != expected_ordinal:
                    raise FullCrashCartError("ACTIVE_ORDINAL_ORDER_INVALID")
                target = measured_started_ns + offset
                if self.clock_ns() < target:
                    self.sleep_until_ns(target)
                observed_before = self.clock_ns()
                if observed_before < target:
                    raise FullCrashCartError("SCHEDULE_BYPASS")
                if observed_before - measured_started_ns > ACTIVE_DEADLINE_NS:
                    raise FullCrashCartError("ACTIVE_WINDOW_TIMEOUT_NO_RETRY")
                next_sample_ns = self._telemetry_until(
                    samples=samples,
                    next_ns=next_sample_ns,
                    observed_ns=observed_before,
                    completed=len(active_rows),
                    depth=work_queue.qsize(),
                )
                prompt = fixture["public_prompt_text"]
                controls = {
                    "temperature": 0,
                    "top_p": 1.0,
                    "top_k": -1,
                    "n": 1,
                    "presence_penalty": 0,
                    "frequency_penalty": 0,
                    "stop": [],
                    "logprobs": False,
                    "prefix_caching": False,
                    "fixture_id": fixture["fixture_id"],
                    "prompt_sha256": fixture["prompt_sha256"],
                }
                request = self._m4_request(
                    phase="measured",
                    episode_id=active_episode,
                    ordinal=ordinal,
                    prompt=prompt,
                    controls=controls,
                )
                self.runtime.commit_input(request)
                active_turn_open = True
                origin_snapshot = self.runtime.snapshot()
                recall = self.runtime.retrieve(origin_snapshot, request)
                packet = self.runtime.prepare(origin_snapshot, recall, request)
                observation = self.pair.dispatch(
                    request=request,
                    shared_public_prompt=prompt,
                    packet=packet,
                )
                observed_after = self.clock_ns()
                if observed_after - measured_started_ns > ACTIVE_DEADLINE_NS:
                    raise FullCrashCartError("ACTIVE_WINDOW_TIMEOUT_NO_RETRY")
                candidate = _behavior(observation.candidate_behavior)
                response = {
                    "kind": "PUBLIC_OUTPUT",
                    "output_text": candidate["raw_output_text"],
                    "source": {
                        "source_kind": "local-behavior-capture",
                        "source_id": (
                            f"candidate:{candidate['session_id']}:"
                            f"{candidate['request_sha256']}"
                        ),
                        "source_sha256": candidate["output_sha256"],
                    },
                    "claim_kind": "situated-model-response",
                    "supporting_event_ids": list(packet.selected_event_ids),
                    "comparison_output_sha256": (
                        observation.peer_behavior.output_sha256
                    ),
                }
                committed = self.runtime.commit_response(response)
                active_turn_open = False
                row = self._pair_row(
                    observation,
                    ordinal=ordinal,
                    prompt=prompt,
                    selected_event_ids=packet.selected_event_ids,
                )
                row["origin_input_event_id"] = origin_snapshot.event_ids[-1]
                row["origin_output_event_id"] = committed.event_id
                row["origin_log_head"] = self.runtime.head
                row["observed_dispatch_ns"] = observed_before - measured_started_ns
                row["observed_completion_ns"] = observed_after - measured_started_ns
                active_rows.append(row)
                queue_metrics["consumed_ordinals"].append(ordinal)
                next_sample_ns = self._telemetry_until(
                    samples=samples,
                    next_ns=next_sample_ns,
                    observed_ns=observed_after,
                    completed=len(active_rows),
                    depth=work_queue.qsize(),
                )
                work_queue.task_done()

            producer.join(timeout=5.0)
            if producer.is_alive():
                raise FullCrashCartError("BOUNDED_QUEUE_DRAIN_FAILED")
            measured_completed_ns = self.clock_ns()
            if measured_completed_ns - measured_started_ns < 30_000_000_000:
                raise FullCrashCartError("ACTIVE_WINDOW_TOO_SHORT")
            if tuple(queue_metrics["consumed_ordinals"]) != tuple(range(64)):
                raise FullCrashCartError("ACTIVE_ORDINAL_ORDER_INVALID")
            if queue_metrics["max_depth"] > QUEUE_CAPACITY:
                raise FullCrashCartError("QUEUE_CAPACITY_EXCEEDED")
            self.runtime.verify()
        except BaseException as exc:
            failure_code = _failure_code(exc)
            if active_turn_open:
                try:
                    self.runtime.abort_response(failure_code)
                except Exception:
                    failure_code = "ORIGIN_ABORT_ACCOUNTING_FAILED"
        finally:
            if producer is not None and producer.is_alive():
                producer.join(timeout=5.0)
            try:
                if failure_code is None:
                    cleanup = self.pair.finalize(
                        reset_ordinal=3,
                        episode_id="full-crash-cart-final",
                    )
                else:
                    cleanup = self.pair.finalize_after_failure(
                        episode_id="full-crash-cart-failure-final"
                    )
            except BaseException as cleanup_exc:
                failure_code = failure_code or _failure_code(cleanup_exc)

        report = {
            "schema_version": "situated-origin-full-assembly-crash-cart-v0.1-alpha",
            "observation_classification": "NON_SCORING_PUBLIC_BEHAVIOR_OBSERVATION",
            "structural_status": "PASS" if failure_code is None else "BLOCKED",
            "failure_code": failure_code,
            "controls": {
                "warmup_pair_count": 4,
                "measured_pair_count": 64,
                "queue_capacity": QUEUE_CAPACITY,
                "active_deadline_ns": ACTIVE_DEADLINE_NS,
                "telemetry_interval_ns": TELEMETRY_INTERVAL_NS,
                "active_schedule_ns": list(active_schedule()),
                "telemetry_schedule_ns": list(telemetry_schedule()),
                "run_uses_public_inputs_only": True,
            },
            "warmup": {
                "rows": warmup_rows,
                "situated_privilege": False,
            },
            "clean_barrier": {
                "count": self.runtime.barrier_count,
                "receipt": dict(clean_barrier_receipt or {}),
                "diagnostic_rng_receipt": dict(rng_receipt or {}),
            },
            "active_window": {
                "started_ns": measured_started_ns,
                "completed_ns": measured_completed_ns,
                "duration_ns": (
                    None
                    if measured_started_ns is None or measured_completed_ns is None
                    else measured_completed_ns - measured_started_ns
                ),
                "rows": active_rows,
            },
            "queue": queue_metrics,
            "telemetry": samples,
            "origin": {
                "log_head": self.runtime.head,
                "event_count": len(self.runtime.kernel.events()),
                "replay_verified": failure_code is None,
            },
            "replica_consistency": {
                "classification": "DIAGNOSTIC_ONLY",
                "match_count": sum(
                    row["candidate"]["output_sha256"]
                    == row["peer"]["output_sha256"]
                    for row in active_rows
                ),
                "mismatch_count": sum(
                    row["candidate"]["output_sha256"]
                    != row["peer"]["output_sha256"]
                    for row in active_rows
                ),
            },
            "laws": list(held_laws()),
            "cleanup": cleanup,
            "limitations": [
                "No model or tokenizer was loaded.",
                "The token provider and backends are injected custody-free test doubles.",
                "No protected inputs, scoring thresholds, or scientific claims were used.",
                "A passing report proves assembly topology, not model behavior or scoring readiness.",
            ],
        }
        # Canonicalizability is part of the observation contract.
        canonical_bytes(report)
        return report


__all__ = [
    "FullAssemblyCrashCart",
    "FullCrashCartError",
    "ParallelAtomicM4Pair",
    "ParallelPairObservation",
]
