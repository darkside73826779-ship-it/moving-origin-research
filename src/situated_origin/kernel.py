"""Transactional situated-origin kernel built over the append-only ledger."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Iterable

from .contracts import (
    CommittedOriginEvent,
    EnvironmentFrame,
    OriginContractError,
    OriginEventProposal,
    OriginStamp,
    ProvenanceHandle,
    SHA256_ZERO,
    SituatedOriginFrame,
    Unavailable,
    sha256_canonical,
    to_primitive,
)
from .ledger import AppendOnlyOriginLedger


INPUT_COMMITTED = "INPUT_COMMITTED"
OUTPUT_COMMITTED = "OUTPUT_COMMITTED"
TURN_ABORTED = "TURN_ABORTED"
CADENCE_COMMITTED = "CADENCE_COMMITTED"


@dataclass(frozen=True)
class TransactionJournalEntry:
    journal_ordinal: int
    turn_id: str
    status: str
    input_event_id: str
    terminal_event_id: str | None
    cycle: int
    event_ordinal: int
    log_head: str
    reason: str | None


class SituatedOriginKernel:
    """One-clock, single-writer coordinator for durable origin transitions."""

    def __init__(self, life_id: str, epoch: int = 0) -> None:
        self._ledger = AppendOnlyOriginLedger(life_id, epoch)
        self._lock = RLock()
        self._journal: list[TransactionJournalEntry] = []
        self._active_turn_id: str | None = None
        self._active_input_event_id: str | None = None
        self._active_input_cycle: int | None = None
        self._active_source: ProvenanceHandle | None = None
        self._frames: list[SituatedOriginFrame] = [
            _genesis_frame(life_id, epoch)
        ]

    @property
    def head(self) -> str:
        return self._ledger.head

    @property
    def active_turn_id(self) -> str | None:
        with self._lock:
            return self._active_turn_id

    def current(self) -> SituatedOriginFrame:
        """Return the immutable current frame snapshot."""
        with self._lock:
            return self._frames[-1]

    def frames(self) -> tuple[SituatedOriginFrame, ...]:
        with self._lock:
            return tuple(self._frames)

    def events(self) -> tuple[CommittedOriginEvent, ...]:
        return self._ledger.snapshot()

    def journal(self) -> tuple[TransactionJournalEntry, ...]:
        with self._lock:
            return tuple(self._journal)

    def commit_input(
        self,
        turn_id: str,
        proposal: OriginEventProposal,
        *,
        expected_head: str,
    ) -> CommittedOriginEvent:
        """Commit the observed input as the first event of a new cycle."""
        _require_turn_id(turn_id)
        with self._lock:
            if self._active_turn_id is not None:
                raise OriginContractError("TURN_ALREADY_OPEN")
            canonical = _transition_proposal(INPUT_COMMITTED, turn_id, proposal)
            event = self._ledger.commit(
                canonical, expected_head=expected_head, advance_cycle=True
            )
            self._active_turn_id = turn_id
            self._active_input_event_id = event.event_id
            self._active_input_cycle = event.stamp.cycle
            self._active_source = event.proposal.source
            self._journal.append(
                TransactionJournalEntry(
                    journal_ordinal=len(self._journal),
                    turn_id=turn_id,
                    status=INPUT_COMMITTED,
                    input_event_id=event.event_id,
                    terminal_event_id=None,
                    cycle=event.stamp.cycle,
                    event_ordinal=event.stamp.event_ordinal,
                    log_head=event.event_sha256,
                    reason=None,
                )
            )
            self._append_frame(event)
            return event

    def commit_output(
        self,
        turn_id: str,
        proposal: OriginEventProposal,
        *,
        expected_head: str,
    ) -> CommittedOriginEvent:
        """Commit the successful response in the input event's cycle."""
        _require_turn_id(turn_id)
        with self._lock:
            self._require_active_turn(turn_id)
            canonical = _transition_proposal(OUTPUT_COMMITTED, turn_id, proposal)
            event = self._ledger.commit(
                canonical, expected_head=expected_head, advance_cycle=False
            )
            self._finish_turn(event, OUTPUT_COMMITTED, reason=None)
            return event

    def abort_turn(
        self,
        turn_id: str,
        reason: str,
        *,
        expected_head: str,
    ) -> CommittedOriginEvent:
        """Record failure after input commit without erasing that history."""
        _require_turn_id(turn_id)
        if not reason:
            raise OriginContractError("TURN_ABORT_REASON_REQUIRED")
        with self._lock:
            self._require_active_turn(turn_id)
            if self._active_source is None:
                raise OriginContractError("TRANSACTION_JOURNAL_INVALID")
            proposal = OriginEventProposal(
                kind=TURN_ABORTED,
                content=b"",
                source=self._active_source,
                context={"turn_id": turn_id, "reason": reason},
            )
            event = self._ledger.commit(
                proposal, expected_head=expected_head, advance_cycle=False
            )
            self._finish_turn(event, TURN_ABORTED, reason=reason)
            return event

    def advance_origin(
        self,
        proposal: OriginEventProposal,
        *,
        expected_head: str,
    ) -> CommittedOriginEvent:
        """Advance the origin outside a turn through an explicit cadence event."""
        with self._lock:
            if self._active_turn_id is not None:
                raise OriginContractError("TURN_IN_PROGRESS")
            canonical = OriginEventProposal(
                kind=CADENCE_COMMITTED,
                content=bytes(proposal.content),
                source=proposal.source,
                context={"source_kind": proposal.kind, **dict(proposal.context)},
                valid_from=proposal.valid_from,
                valid_until=proposal.valid_until,
                supersedes=proposal.supersedes,
                observed_environment=proposal.observed_environment,
                observed_space=proposal.observed_space,
            )
            event = self._ledger.commit(
                canonical, expected_head=expected_head, advance_cycle=True
            )
            self._append_frame(event)
            return event

    def assert_materialized_view_sources(
        self, *, fact_source_head: str, access_source_head: str
    ) -> tuple[str, str]:
        """Reject any view that was not derived from the current log head."""
        with self._lock:
            if fact_source_head != self.head or access_source_head != self.head:
                raise OriginContractError("VIEW_HEAD_STALE")
            frame = self.current()
            return frame.fact_graph_head, frame.access_ledger_head

    def frame_at_event_ordinal(self, event_ordinal: int) -> SituatedOriginFrame:
        if type(event_ordinal) is not int or event_ordinal < -1:
            raise OriginContractError("EVENT_ORDINAL_INVALID")
        with self._lock:
            index = event_ordinal + 1
            if index >= len(self._frames):
                raise OriginContractError("FRAME_NOT_FOUND")
            return self._frames[index]

    def verify(self) -> None:
        """Verify the ledger and deterministic frame/journal reconstruction."""
        with self._lock:
            self._ledger.verify()
            replayed = self.replay(
                self._ledger.life_id,
                self._ledger.snapshot(),
                epoch=self._ledger.epoch,
            )
            if [to_primitive(row) for row in replayed.frames()] != [
                to_primitive(row) for row in self._frames
            ]:
                raise OriginContractError("FRAME_REPLAY_MISMATCH")
            if [to_primitive(row) for row in replayed.journal()] != [
                to_primitive(row) for row in self._journal
            ]:
                raise OriginContractError("JOURNAL_REPLAY_MISMATCH")

    @classmethod
    def replay(
        cls,
        life_id: str,
        events: Iterable[CommittedOriginEvent],
        *,
        epoch: int = 0,
    ) -> "SituatedOriginKernel":
        supplied = tuple(events)
        ledger = AppendOnlyOriginLedger.replay(life_id, supplied, epoch=epoch)
        kernel = cls(life_id, epoch)
        kernel._ledger = ledger
        for event in ledger.snapshot():
            kernel._apply_replayed_transition(event)
            kernel._append_frame(event)
        return kernel

    def _require_active_turn(self, turn_id: str) -> None:
        if self._active_turn_id is None:
            raise OriginContractError("TURN_NOT_OPEN")
        if self._active_turn_id != turn_id:
            raise OriginContractError("TURN_ID_MISMATCH")

    def _finish_turn(
        self, event: CommittedOriginEvent, status: str, *, reason: str | None
    ) -> None:
        if (
            self._active_turn_id is None
            or self._active_input_event_id is None
            or self._active_input_cycle is None
        ):
            raise OriginContractError("TRANSACTION_JOURNAL_INVALID")
        if event.stamp.cycle != self._active_input_cycle:
            raise OriginContractError("TURN_CYCLE_MISMATCH")
        self._journal.append(
            TransactionJournalEntry(
                journal_ordinal=len(self._journal),
                turn_id=self._active_turn_id,
                status=status,
                input_event_id=self._active_input_event_id,
                terminal_event_id=event.event_id,
                cycle=event.stamp.cycle,
                event_ordinal=event.stamp.event_ordinal,
                log_head=event.event_sha256,
                reason=reason,
            )
        )
        self._active_turn_id = None
        self._active_input_event_id = None
        self._active_input_cycle = None
        self._active_source = None
        self._append_frame(event)

    def _append_frame(self, event: CommittedOriginEvent) -> None:
        history = self._ledger.snapshot()[: event.stamp.event_ordinal + 1]
        self._frames.append(
            _frame_after(self._frames[-1], event, history)
        )

    def _apply_replayed_transition(self, event: CommittedOriginEvent) -> None:
        kind = event.proposal.kind
        context = event.proposal.context
        turn_id = context.get("turn_id")
        if kind == CADENCE_COMMITTED:
            if self._active_turn_id is not None:
                raise OriginContractError("REPLAY_CADENCE_DURING_TURN")
            if event.stamp.cycle != self._frames[-1].stamp.cycle + 1:
                raise OriginContractError("ORIGIN_CYCLE_DISCONTINUITY")
            return
        if type(turn_id) is not str or not turn_id:
            raise OriginContractError("REPLAY_TURN_ID_MISSING")
        if kind == INPUT_COMMITTED:
            if self._active_turn_id is not None:
                raise OriginContractError("REPLAY_OVERLAPPING_TURNS")
            if event.stamp.cycle != self._frames[-1].stamp.cycle + 1:
                raise OriginContractError("ORIGIN_CYCLE_DISCONTINUITY")
            self._active_turn_id = turn_id
            self._active_input_event_id = event.event_id
            self._active_input_cycle = event.stamp.cycle
            self._active_source = event.proposal.source
            self._journal.append(
                TransactionJournalEntry(
                    len(self._journal), turn_id, INPUT_COMMITTED, event.event_id,
                    None, event.stamp.cycle, event.stamp.event_ordinal,
                    event.event_sha256, None,
                )
            )
            return
        if kind not in (OUTPUT_COMMITTED, TURN_ABORTED):
            raise OriginContractError("REPLAY_EVENT_KIND_INVALID")
        self._require_active_turn(turn_id)
        reason = context.get("reason") if kind == TURN_ABORTED else None
        if kind == TURN_ABORTED and (type(reason) is not str or not reason):
            raise OriginContractError("TURN_ABORT_REASON_REQUIRED")
        self._finish_replayed_turn(event, kind, reason)

    def _finish_replayed_turn(
        self, event: CommittedOriginEvent, status: str, reason: str | None
    ) -> None:
        if (
            self._active_turn_id is None
            or self._active_input_event_id is None
            or self._active_input_cycle is None
            or event.stamp.cycle != self._active_input_cycle
        ):
            raise OriginContractError("TURN_CYCLE_MISMATCH")
        self._journal.append(
            TransactionJournalEntry(
                len(self._journal), self._active_turn_id, status,
                self._active_input_event_id, event.event_id, event.stamp.cycle,
                event.stamp.event_ordinal, event.event_sha256, reason,
            )
        )
        self._active_turn_id = None
        self._active_input_event_id = None
        self._active_input_cycle = None
        self._active_source = None


def _transition_proposal(
    status: str, turn_id: str, proposal: OriginEventProposal
) -> OriginEventProposal:
    context = dict(proposal.context)
    context["source_kind"] = proposal.kind
    context["turn_id"] = turn_id
    return OriginEventProposal(
        kind=status,
        content=bytes(proposal.content),
        source=proposal.source,
        context=context,
        valid_from=proposal.valid_from,
        valid_until=proposal.valid_until,
        supersedes=proposal.supersedes,
        observed_environment=proposal.observed_environment,
        observed_space=proposal.observed_space,
    )


def _require_turn_id(turn_id: str) -> None:
    if type(turn_id) is not str or not turn_id:
        raise OriginContractError("TURN_ID_REQUIRED")


def _genesis_frame(life_id: str, epoch: int) -> SituatedOriginFrame:
    stamp = OriginStamp(life_id, epoch, -1, -1, SHA256_ZERO)
    environment = EnvironmentFrame(
        runtime_place=Unavailable("NOT_OBSERVED"),
        interaction_place=Unavailable("NOT_OBSERVED"),
        world_place=Unavailable("NOT_OBSERVED"),
        active_task=Unavailable("NOT_OBSERVED"),
    )
    values = {
        "stamp": stamp,
        "environment": environment,
        "active_episode": f"life:{life_id}:epoch:{epoch}",
        "retention": (0.0,),
        "protention": Unavailable("PROTENTION_NOT_IMPLEMENTED"),
        "fact_graph_head": SHA256_ZERO,
        "access_ledger_head": SHA256_ZERO,
        "homeostasis": Unavailable("HOMEOSTASIS_NOT_IMPLEMENTED"),
        "experience_strip": Unavailable("E3_FUTURE_MILESTONE"),
        "provenance_root": SHA256_ZERO,
    }
    return SituatedOriginFrame(**values, frame_sha256=sha256_canonical(values))


def _frame_after(
    prior: SituatedOriginFrame,
    event: CommittedOriginEvent,
    history: tuple[CommittedOriginEvent, ...],
) -> SituatedOriginFrame:
    proposal = event.proposal
    context = proposal.context
    runtime_place = (
        proposal.observed_environment
        if isinstance(proposal.observed_environment, str)
        else prior.environment.runtime_place
    )
    world_place = (
        proposal.observed_space
        if isinstance(proposal.observed_space, str)
        else prior.environment.world_place
    )
    interaction = context.get("interaction_place")
    task = context.get("active_task")
    environment = EnvironmentFrame(
        runtime_place=runtime_place,
        interaction_place=(
            interaction
            if type(interaction) is str and interaction
            else prior.environment.interaction_place
        ),
        world_place=world_place,
        active_task=(
            task if type(task) is str and task else prior.environment.active_task
        ),
    )
    episode = context.get("episode_id")
    active_episode = (
        episode if type(episode) is str and episode else prior.active_episode
    )
    retention = tuple(
        round(int(row.event_sha256[:8], 16) / 0xFFFFFFFF, 12)
        for row in history[-4:]
    ) or (0.0,)
    fact_head = sha256_canonical(
        {"view": "fact_graph", "source_log_head": event.event_sha256}
    )
    access_head = sha256_canonical(
        {"view": "access_ledger", "source_log_head": event.event_sha256}
    )
    provenance_root = sha256_canonical(
        {
            "source_log_head": event.event_sha256,
            "source_sha256": [row.proposal.source.source_sha256 for row in history],
        }
    )
    values = {
        "stamp": event.stamp,
        "environment": environment,
        "active_episode": active_episode,
        "retention": retention,
        "protention": Unavailable("PROTENTION_NOT_IMPLEMENTED"),
        "fact_graph_head": fact_head,
        "access_ledger_head": access_head,
        "homeostasis": Unavailable("HOMEOSTASIS_NOT_IMPLEMENTED"),
        "experience_strip": Unavailable("E3_FUTURE_MILESTONE"),
        "provenance_root": provenance_root,
    }
    return SituatedOriginFrame(**values, frame_sha256=sha256_canonical(values))
