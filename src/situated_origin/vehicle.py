"""Injected, model-neutral orchestration chassis for the assembly alpha."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol, Sequence


FORBIDDEN_ANSWER_FIELDS = frozenset(
    {
        "answer",
        "answer_label",
        "correct_answer",
        "expected_answer",
        "ground_truth",
        "ground_truth_answer",
        "label",
        "target_label",
    }
)


class VehicleError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class OriginPort(Protocol):
    def clean_barrier(self) -> None: ...
    def commit_input(self, value: Mapping[str, Any]) -> Any: ...
    def snapshot(self) -> Any: ...
    def commit_response(self, value: Mapping[str, Any]) -> Any: ...
    def abort_response(self, code: str) -> None: ...
    def record_infrastructure_event(self, value: Mapping[str, Any]) -> Any: ...


class MemoryPort(Protocol):
    def clean_barrier(self) -> None: ...
    def retrieve(self, origin_snapshot: Any, request: Mapping[str, Any]) -> Any: ...


class ActuationPort(Protocol):
    def clean_barrier(self) -> None: ...
    def prepare(self, origin_snapshot: Any, recall: Any, request: Mapping[str, Any]) -> Any: ...


class PairDispatcher(Protocol):
    def dispatch(
        self,
        request: Mapping[str, Any],
        *,
        candidate_capability: Any | None,
        peer_capability: None,
    ) -> Mapping[str, Any]: ...


class OutputValidator(Protocol):
    def validate(self, stage: str, value: Mapping[str, Any]) -> Mapping[str, Any]: ...


class EvidencePublisher(Protocol):
    def stage(self, value: Mapping[str, Any]) -> Any: ...
    def commit(self, token: Any, value: Mapping[str, Any]) -> None: ...
    def abort(self, token: Any | None) -> None: ...
    def publish_abort(self, value: Mapping[str, Any]) -> None: ...


@dataclass(frozen=True)
class VehicleStep:
    ordinal: int
    committed_input: Any
    origin_snapshot: Any
    recall: Any
    response: Mapping[str, Any]
    committed_response: Any
    evidence: Mapping[str, Any]
    evidence_finalized: bool = True


@dataclass(frozen=True)
class VehicleRunResult:
    status: str
    steps: tuple[VehicleStep, ...]
    failure_code: str | None
    cleanup_complete: bool
    started_ns: int
    completed_ns: int


def _reject_answer_labels(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).strip().casefold() in FORBIDDEN_ANSWER_FIELDS:
                raise VehicleError("GROUND_TRUTH_LABEL_FORBIDDEN")
            _reject_answer_labels(item)
    elif isinstance(value, (tuple, list)):
        for item in value:
            _reject_answer_labels(item)


class VehicleOrchestrator:
    """Own the complete atomic route from input commit through publication.

    All effectful components are injected.  Evidence is staged before the
    response closes the origin turn.  After an input commit, any pre-response
    failure preserves that input and appends an honest abort.  Once a response
    is committed it is never represented as rolled back: a later evidence
    finalization failure blocks the run, retains the completed step, and is
    optionally recorded as a separate origin infrastructure event.
    """

    def __init__(
        self,
        *,
        origin: OriginPort,
        memory: MemoryPort,
        actuation: ActuationPort,
        pair: PairDispatcher,
        validator: OutputValidator,
        publisher: EvidencePublisher,
        clock_ns: Callable[[], int],
        sleep_until_ns: Callable[[int], None],
        cleanup: Callable[[], None],
    ) -> None:
        self.origin = origin
        self.memory = memory
        self.actuation = actuation
        self.pair = pair
        self.validator = validator
        self.publisher = publisher
        self.clock_ns = clock_ns
        self.sleep_until_ns = sleep_until_ns
        self.cleanup = cleanup

    def _dispatch_warmup(self, request: Mapping[str, Any]) -> None:
        _reject_answer_labels(request)
        response = self.pair.dispatch(
            dict(request), candidate_capability=None, peer_capability=None
        )
        self.validator.validate("WARMUP", response)

    def _clean_barrier(self) -> None:
        self.origin.clean_barrier()
        self.memory.clean_barrier()
        self.actuation.clean_barrier()

    @staticmethod
    def _failure_code(exc: BaseException) -> str:
        code = getattr(exc, "code", None)
        return code if isinstance(code, str) and code else type(exc).__name__

    def _abort_staged_evidence(self, token: Any | None) -> None:
        """Best-effort evidence cleanup must never mask origin accounting."""

        try:
            self.publisher.abort(token)
        except BaseException:
            pass

    def run(
        self,
        *,
        warmup_inputs: Sequence[Mapping[str, Any]],
        measured_inputs: Sequence[Mapping[str, Any]],
        schedule_offsets_ns: Sequence[int],
        deadline_ns: int,
    ) -> VehicleRunResult:
        if (
            len(measured_inputs) != len(schedule_offsets_ns)
            or type(deadline_ns) is not int
            or deadline_ns < 1
            or any(type(item) is not int or item < 0 for item in schedule_offsets_ns)
            or tuple(schedule_offsets_ns) != tuple(sorted(schedule_offsets_ns))
        ):
            raise VehicleError("VEHICLE_SCHEDULE_INVALID")
        started = self.clock_ns()
        steps: list[VehicleStep] = []
        failure: str | None = None
        cleanup_complete = False
        try:
            for request in (*warmup_inputs, *measured_inputs):
                if not isinstance(request, Mapping):
                    raise VehicleError("VEHICLE_INPUT_INVALID")
                _reject_answer_labels(request)
            for request in warmup_inputs:
                self._dispatch_warmup(request)
            self._clean_barrier()
            measured_start = self.clock_ns()

            for ordinal, (request, offset) in enumerate(
                zip(measured_inputs, schedule_offsets_ns)
            ):
                target = measured_start + offset
                if self.clock_ns() < target:
                    self.sleep_until_ns(target)
                if self.clock_ns() < target:
                    raise VehicleError("SCHEDULE_BYPASS")
                if self.clock_ns() - measured_start > deadline_ns:
                    raise VehicleError("ACTIVE_WINDOW_TIMEOUT_NO_RETRY")

                stage_token: Any | None = None
                evidence_staged = False
                input_committed = False
                response_committed = False
                try:
                    committed_input = self.origin.commit_input(dict(request))
                    input_committed = True
                    origin_snapshot = self.origin.snapshot()
                    recall = self.memory.retrieve(origin_snapshot, dict(request))
                    capability = self.actuation.prepare(
                        origin_snapshot, recall, dict(request)
                    )
                    response = self.pair.dispatch(
                        dict(request),
                        candidate_capability=capability,
                        peer_capability=None,
                    )
                    validated = self.validator.validate("MEASURED", response)
                    if self.clock_ns() - measured_start > deadline_ns:
                        raise VehicleError("ACTIVE_WINDOW_TIMEOUT_NO_RETRY")
                    staged_evidence = {
                        "ordinal": ordinal,
                        "input_commit": committed_input,
                        "origin_snapshot": origin_snapshot,
                        "recall": recall,
                        "response": validated,
                    }
                    stage_token = self.publisher.stage(staged_evidence)
                    evidence_staged = True
                    committed_response = self.origin.commit_response(validated)
                    response_committed = True
                    evidence = dict(
                        staged_evidence,
                        response_commit=committed_response,
                    )
                    try:
                        self.publisher.commit(stage_token, evidence)
                    except BaseException as exc:
                        underlying_code = self._failure_code(exc)
                        self._abort_staged_evidence(stage_token)
                        infrastructure_event = {
                            "kind": "EVIDENCE_FINALIZATION_FAILED",
                            "failure_code": "EVIDENCE_FINALIZATION_FAILED",
                            "underlying_failure_code": underlying_code,
                            "ordinal": ordinal,
                            "response_commit": committed_response,
                        }
                        try:
                            self.origin.record_infrastructure_event(infrastructure_event)
                        except BaseException as accounting_exc:
                            infrastructure_event = dict(
                                infrastructure_event,
                                accounting_failure_code=self._failure_code(accounting_exc),
                            )
                            failure = "INFRASTRUCTURE_ACCOUNTING_FAILED"
                        steps.append(
                            VehicleStep(
                                ordinal=ordinal,
                                committed_input=committed_input,
                                origin_snapshot=origin_snapshot,
                                recall=recall,
                                response=validated,
                                committed_response=committed_response,
                                evidence=dict(
                                    evidence,
                                    evidence_finalized=False,
                                    evidence_finalization_failure=underlying_code,
                                ),
                                evidence_finalized=False,
                            )
                        )
                        if failure is None:
                            failure = "EVIDENCE_FINALIZATION_FAILED"
                        break
                    steps.append(
                        VehicleStep(
                            ordinal=ordinal,
                            committed_input=committed_input,
                            origin_snapshot=origin_snapshot,
                            recall=recall,
                            response=validated,
                            committed_response=committed_response,
                            evidence=evidence,
                            evidence_finalized=True,
                        )
                    )
                except BaseException as exc:
                    code = self._failure_code(exc)
                    self._abort_staged_evidence(
                        stage_token if evidence_staged else None
                    )
                    # Autobiography is irreversible.  Once the input event is
                    # committed, a failed turn is represented by the next
                    # durable TURN_ABORTED event; the input is never rewound.
                    if input_committed and not response_committed:
                        self.origin.abort_response(code)
                    try:
                        if input_committed and not response_committed:
                            self.publisher.publish_abort(
                                {"ordinal": ordinal, "failure_code": code}
                            )
                    except Exception:
                        pass
                    failure = code
                    break
        except BaseException as exc:
            failure = self._failure_code(exc)
        finally:
            try:
                self.cleanup()
                cleanup_complete = True
            except Exception:
                if failure is None:
                    failure = "CLEANUP_FAILED"

        completed = self.clock_ns()
        return VehicleRunResult(
            status="PASS" if failure is None and cleanup_complete else "BLOCKED",
            steps=tuple(steps),
            failure_code=failure,
            cleanup_complete=cleanup_complete,
            started_ns=started,
            completed_ns=completed,
        )


__all__ = [
    "ActuationPort",
    "EvidencePublisher",
    "MemoryPort",
    "OriginPort",
    "OutputValidator",
    "PairDispatcher",
    "VehicleError",
    "VehicleOrchestrator",
    "VehicleRunResult",
    "VehicleStep",
]
