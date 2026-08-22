"""Production-shaped situated-origin ports for the model-neutral vehicle."""

from __future__ import annotations

from dataclasses import dataclass
import copy
import json
from typing import Any, Mapping

from .access import AccessLedger
from .actuator import CandidateContextActuator
from .claims import ProvenanceClaimGuard
from .contracts import (
    EnvironmentFrame, MemoryQuery, OriginContractError, OriginEventProposal,
    ProvenanceHandle, SituatedContextPacket, SituatedOriginFrame, Unavailable,
    canonical_bytes, sha256_bytes, sha256_canonical,
)
from .episodes import EpisodicStore
from .facts import BiTemporalFactGraph, FactRevision
from .kernel import SituatedOriginKernel
from .origin_index import OriginIndex
from .present import ThickPresent
from .retrieval import OriginDistanceRecall


FORBIDDEN_FIELDS = frozenset({
    "answer", "answer_label", "correct_answer", "expected_answer", "ground_truth",
    "ground_truth_answer", "label", "target_label",
})


def _reject_answer_fields(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).strip().casefold() in FORBIDDEN_FIELDS:
                raise OriginContractError("GROUND_TRUTH_LABEL_FORBIDDEN")
            _reject_answer_fields(item)
    elif isinstance(value, (tuple, list)):
        for item in value:
            _reject_answer_fields(item)


def _content(value: Any) -> bytes:
    if type(value) is bytes:
        return bytes(value)
    if type(value) is str and value:
        return value.encode("utf-8")
    raise OriginContractError("PUBLIC_CONTENT_REQUIRED")


def _source(value: Mapping[str, Any], content: bytes, default_id: str) -> ProvenanceHandle:
    supplied = value.get("source")
    if supplied is None:
        return ProvenanceHandle("public-request", default_id, sha256_bytes(content))
    if not isinstance(supplied, Mapping):
        raise OriginContractError("PUBLIC_SOURCE_INVALID")
    return ProvenanceHandle(
        str(supplied.get("source_kind", "")), str(supplied.get("source_id", "")),
        str(supplied.get("source_sha256", "")),
    )


@dataclass(frozen=True)
class RuntimeSnapshot:
    frame: SituatedOriginFrame
    event_ids: tuple[str, ...]


class SituatedRuntime:
    """Own one kernel and materialize every public view in ledger order."""

    def __init__(self, life_id: str, *, kernel: SituatedOriginKernel | None = None) -> None:
        self.kernel = kernel or SituatedOriginKernel(life_id)
        self.access = AccessLedger()
        self.present = ThickPresent(8)
        self.facts = BiTemporalFactGraph()
        self.episodes = EpisodicStore()
        self.origin_index = OriginIndex(life_id)
        self.recall_engine = OriginDistanceRecall(
            self.access, self.facts, self.episodes, self.origin_index
        )
        self.claims = ProvenanceClaimGuard()
        self.actuator = CandidateContextActuator()
        self._frames: list[SituatedOriginFrame] = []
        self._event_ids: list[str] = []
        self._cycle_features: list[tuple[float, ...]] = []
        self._last_ordinal = -1
        self._pending_recall = None
        self.barrier_count = 0

    @classmethod
    def replay(cls, life_id: str, events: tuple[Any, ...]) -> "SituatedRuntime":
        kernel = SituatedOriginKernel.replay(life_id, events)
        runtime = cls(life_id, kernel=kernel)
        for event in events:
            runtime._materialize(event)
        runtime.verify()
        return runtime

    @property
    def head(self) -> str:
        return self.kernel.head

    def clean_barrier(self) -> None:
        # A barrier clears no autobiographical or materialized cognitive state.
        self.barrier_count += 1

    def snapshot(self) -> RuntimeSnapshot:
        frame = self._frames[-1] if self._frames else self._genesis_composite()
        return RuntimeSnapshot(frame, tuple(self._event_ids))

    def commit_input(self, value: Mapping[str, Any]) -> Any:
        _reject_answer_fields(value)
        turn_id = str(value.get("id", "")).strip()
        if not turn_id:
            raise OriginContractError("TURN_ID_REQUIRED")
        proposal = self._proposal(value, default_kind="PUBLIC_INPUT", default_id=turn_id)
        event = self.kernel.commit_input(turn_id, proposal, expected_head=self.head)
        self._last_recall = None
        self._pending_recall = None
        self._materialize(event)
        return event

    def commit_response(self, value: Mapping[str, Any]) -> Any:
        _reject_answer_fields(value)
        if "_situated_recall" in value:
            raise OriginContractError("RESERVED_RUNTIME_FIELD")
        turn_id = self.kernel.active_turn_id
        if turn_id is None:
            raise OriginContractError("TURN_NOT_OPEN")
        support = tuple(str(item) for item in value.get("supporting_event_ids", ()))
        if support:
            last_recall = getattr(self, "_last_recall", None)
            if last_recall is None:
                raise OriginContractError("CLAIM_WITHOUT_RECALL")
            receipt = self.claims.assess(str(value.get("claim_kind", "model-response")), support, last_recall)
            if receipt.status != "GROUNDED":
                raise OriginContractError("CLAIM_UNSUPPORTED")
        response_value = dict(value)
        if self._pending_recall is not None:
            if self._pending_recall.source_log_head != self.head:
                raise OriginContractError("VIEW_HEAD_STALE")
            response_value["_situated_recall"] = {
                "selected_event_ids": self._pending_recall.selected_event_ids,
                "selection_receipt_sha256": self._pending_recall.selection_receipt_sha256,
                "source_log_head": self._pending_recall.source_log_head,
            }
        proposal = self._proposal(
            response_value,
            default_kind="PUBLIC_OUTPUT",
            default_id=f"{turn_id}:output",
        )
        event = self.kernel.commit_output(turn_id, proposal, expected_head=self.head)
        self._materialize(event)
        self._pending_recall = None
        return event

    def abort_response(self, code: str) -> Any | None:
        turn_id = self.kernel.active_turn_id
        if turn_id is None:
            return None
        event = self.kernel.abort_turn(turn_id, code, expected_head=self.head)
        self._materialize(event)
        self._pending_recall = None
        return event

    def record_infrastructure_event(self, value: Mapping[str, Any]) -> Any:
        """Append a post-turn failure without rewriting an already closed turn."""

        _reject_answer_fields(value)
        if self.kernel.active_turn_id is not None:
            raise OriginContractError("INFRASTRUCTURE_EVENT_DURING_ACTIVE_TURN")
        failure_code = str(value.get("failure_code", "")).strip()
        if not failure_code:
            raise OriginContractError("INFRASTRUCTURE_FAILURE_CODE_REQUIRED")
        ordinal = len(self.kernel.events())
        content = canonical_bytes({
            "failure_code": failure_code,
            "ordinal": value.get("ordinal"),
            "underlying_failure_code": value.get("underlying_failure_code"),
        })
        source = ProvenanceHandle(
            "runtime-infrastructure",
            f"infrastructure-event-{ordinal}",
            sha256_bytes(content),
        )
        context = {
            key: copy.deepcopy(item)
            for key, item in value.items()
            if key != "response_commit"
        }
        response_commit = value.get("response_commit")
        if response_commit is not None:
            context["response_commit_event_id"] = getattr(
                response_commit, "event_id", None
            )
            context["response_commit_sha256"] = getattr(
                response_commit, "event_sha256", None
            )
        event = self.kernel.advance_origin(
            OriginEventProposal(
                kind="EVIDENCE_FINALIZATION_FAILED",
                content=content,
                source=source,
                context=context,
            ),
            expected_head=self.head,
        )
        self._materialize(event)
        return event

    def retrieve(self, origin_snapshot: RuntimeSnapshot, request: Mapping[str, Any]) -> Any:
        if origin_snapshot.frame.stamp.log_head != self.head:
            raise OriginContractError("VIEW_HEAD_STALE")
        text = str(request.get("question", request.get("content", ""))).strip()
        query = MemoryQuery(
            text=text, landmark_ids=tuple(str(item) for item in request.get("landmark_ids", ())),
            include_stale=bool(request.get("include_stale", False)),
            limit=int(request.get("memory_limit", 4)),
        )
        recall = self.recall_engine.recall(
            query, origin_snapshot.frame, origin_snapshot.event_ids, self.head
        )
        self._last_recall = recall
        self._pending_recall = recall
        return recall

    def prepare(self, origin_snapshot: RuntimeSnapshot, recall: Any, request: Mapping[str, Any]) -> SituatedContextPacket:
        _reject_answer_fields(request)
        question = str(request.get("question", request.get("content", ""))).encode("utf-8")
        return self.actuator.compile(question, origin_snapshot.frame, recall)

    def verify(self) -> None:
        self.kernel.verify()
        self.origin_index.verify(self.kernel.events())
        if self._last_ordinal != len(self.kernel.events()) - 1:
            raise OriginContractError("MATERIALIZATION_ORDER_INVALID")
        if self.kernel.events() and not self._frames:
            raise OriginContractError("MATERIALIZED_FRAME_MISSING")
        if self.kernel.events():
            frame = self._frames[-1]
            if not all(item == self.head for item in (
                frame.stamp.log_head, self.access.source_log_head,
                self.present.source_log_head, self.facts.source_log_head,
                self.episodes.source_log_head, self.origin_index.source_log_head,
            )):
                raise OriginContractError("VIEW_HEAD_STALE")
            if frame.fact_graph_head != self.facts.head or frame.access_ledger_head != self.access.head:
                raise OriginContractError("COMPOSITE_VIEW_HEAD_MISMATCH")

    def _proposal(self, value: Mapping[str, Any], *, default_kind: str, default_id: str) -> OriginEventProposal:
        content = _content(value.get("output_text", value.get("content")))
        source = _source(value, content, default_id)
        context = {key: copy.deepcopy(item) for key, item in value.items()
                   if key not in ("content", "output_text", "source")}
        fact = context.get("fact")
        return OriginEventProposal(
            kind=str(value.get("kind", default_kind)), content=content, source=source,
            context=context,
            valid_from=(fact.get("valid_from") if isinstance(fact, Mapping) else None),
            valid_until=(fact.get("valid_until") if isinstance(fact, Mapping) else None),
            supersedes=(fact.get("supersedes_fact_id") if isinstance(fact, Mapping) else None),
        )

    def _materialize(self, event: Any) -> None:
        if event.stamp.event_ordinal != self._last_ordinal + 1:
            raise OriginContractError("MATERIALIZATION_ORDER_INVALID")
        head, cycle = event.event_sha256, event.stamp.cycle
        self.origin_index.ingest(event)
        self.access.advance_to(cycle, head)
        self.access.register(event.event_id, cycle)
        recall_context = event.proposal.context.get("_situated_recall")
        if isinstance(recall_context, Mapping):
            selected = recall_context.get("selected_event_ids")
            if not isinstance(selected, (tuple, list)):
                raise OriginContractError("RECALL_REHEARSAL_INVALID")
            for selected_event_id in selected:
                self.access.rehearse(str(selected_event_id), cycle)
        self.facts.advance_to(cycle, head)
        fact = event.proposal.context.get("fact")
        if isinstance(fact, Mapping):
            fact_id = str(fact.get("fact_id", ""))
            valid_from = fact.get("valid_from")
            self.facts.append(FactRevision(
                fact_id=fact_id, event_id=event.event_id, content=event.proposal.content,
                acquired_cycle=cycle,
                valid_from=cycle if valid_from is None else int(valid_from),
                valid_until=fact.get("valid_until"),
                supersedes=fact.get("supersedes_fact_id"),
            ))
        if cycle == len(self._cycle_features):
            supplied = event.proposal.context.get("features")
            features = self._features(event.proposal.content, supplied)
            self._cycle_features.append(features)
        elif cycle != len(self._cycle_features) - 1:
            raise OriginContractError("MATERIALIZED_CYCLE_INVALID")
        self._rebuild_present(head)
        position = self._origin_position(event)
        self.episodes.write(event, {
            **position,
            "thick_present_state": tuple(self.present.state),
        })
        self._event_ids.append(event.event_id)
        self._last_ordinal = event.stamp.event_ordinal
        self._frames.append(self._composite_frame(event.stamp.event_ordinal))

    @staticmethod
    def _features(content: bytes, supplied: Any) -> tuple[float, ...]:
        if supplied is not None:
            if not isinstance(supplied, (tuple, list)) or len(supplied) != 8:
                raise OriginContractError("INPUT_FEATURES_INVALID")
            return tuple(float(value) for value in supplied)
        digest = bytes.fromhex(sha256_bytes(content))
        return tuple(round(digest[index] / 255.0, 12) for index in range(8))

    def _rebuild_present(self, latest_head: str) -> None:
        rebuilt = ThickPresent(8)
        events = self.kernel.events()
        cycle_heads = {}
        for item in events:
            cycle_heads[item.stamp.cycle] = item.event_sha256
        cycle_heads[len(self._cycle_features) - 1] = latest_head
        for cycle, features in enumerate(self._cycle_features):
            rebuilt.advance(cycle, features, cycle_heads[cycle])
        self.present = rebuilt

    def _composite_frame(self, event_ordinal: int) -> SituatedOriginFrame:
        base = self.kernel.frame_at_event_ordinal(event_ordinal)
        values = {
            "stamp": base.stamp,
            "environment": base.environment,
            "active_episode": base.active_episode,
            "retention": tuple(self.present.state),
            "protention": base.protention,
            "fact_graph_head": self.facts.head,
            "access_ledger_head": self.access.head,
            "homeostasis": base.homeostasis,
            "experience_strip": base.experience_strip,
            "provenance_root": base.provenance_root,
        }
        return SituatedOriginFrame(**values, frame_sha256=sha256_canonical(values))

    def _genesis_composite(self) -> SituatedOriginFrame:
        return self.kernel.current()

    def _origin_position(self, event: Any) -> Mapping[str, Any]:
        """Return exact live coordinates, including non-recallable control events."""
        snapshot = self.origin_index.snapshot()
        indexed_ids = {item.event_id for item in snapshot.indexed_events}
        if event.event_id in indexed_ids:
            coordinate = self.origin_index.coordinate(
                event.event_id, source_log_head=event.event_sha256
            )
            return {
                "event_id": coordinate.event_id,
                "indexed": True,
                "encoding_cycle": coordinate.encoding_cycle,
                "current_cycle": coordinate.current_cycle,
                "cycle_relative_distance": coordinate.cycle_relative_distance,
                "landmark_relative": dict(coordinate.landmark_relations),
                "source_log_head": coordinate.source_log_head,
            }
        relations = {}
        for landmark in snapshot.landmarks:
            if event.stamp.cycle < landmark.designated_at_cycle:
                relation = "BEFORE_L"
            elif event.stamp.cycle == landmark.designated_at_cycle:
                relation = "AT_L"
            else:
                relation = "AFTER_L"
            relations[landmark.landmark_event_id] = relation
        return {
            "event_id": event.event_id,
            "indexed": False,
            "encoding_cycle": event.stamp.cycle,
            "current_cycle": snapshot.current_cycle,
            "cycle_relative_distance": snapshot.current_cycle - event.stamp.cycle,
            "landmark_relative": relations,
            "source_log_head": snapshot.source_log_head,
        }


class RuntimeOriginPort:
    def __init__(self, runtime: SituatedRuntime) -> None: self.runtime = runtime
    def clean_barrier(self) -> None: self.runtime.clean_barrier()
    def commit_input(self, value: Mapping[str, Any]) -> Any: return self.runtime.commit_input(value)
    def snapshot(self) -> RuntimeSnapshot: return self.runtime.snapshot()
    def commit_response(self, value: Mapping[str, Any]) -> Any: return self.runtime.commit_response(value)
    def abort_response(self, code: str) -> Any | None: return self.runtime.abort_response(code)
    def record_infrastructure_event(self, value: Mapping[str, Any]) -> Any:
        return self.runtime.record_infrastructure_event(value)


class RuntimeMemoryPort:
    def __init__(self, runtime: SituatedRuntime) -> None: self.runtime = runtime
    def clean_barrier(self) -> None: pass
    def retrieve(self, origin_snapshot: RuntimeSnapshot, request: Mapping[str, Any]) -> Any:
        return self.runtime.retrieve(origin_snapshot, request)


class RuntimeActuationPort:
    def __init__(self, runtime: SituatedRuntime) -> None: self.runtime = runtime
    def clean_barrier(self) -> None: pass
    def prepare(self, origin_snapshot: RuntimeSnapshot, recall: Any, request: Mapping[str, Any]) -> Any:
        return self.runtime.prepare(origin_snapshot, recall, request)
