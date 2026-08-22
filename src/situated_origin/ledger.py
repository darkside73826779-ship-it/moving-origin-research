"""Append-only, hash-chained event ledger for the situated-origin kernel.

The ledger owns only ordering and identity.  Turn semantics and materialized
views live in :mod:`situated_origin.kernel`.
"""

from __future__ import annotations

import copy
from threading import RLock
from typing import Iterable

from .contracts import (
    CommittedOriginEvent,
    OriginContractError,
    OriginEventProposal,
    OriginStamp,
    SHA256_ZERO,
    sha256_canonical,
    to_primitive,
)


class AppendOnlyOriginLedger:
    """Single-writer ledger guarded by expected-head compare-and-append."""

    def __init__(self, life_id: str, epoch: int = 0) -> None:
        if not life_id:
            raise OriginContractError("LIFE_ID_REQUIRED")
        if type(epoch) is not int or epoch < 0:
            raise OriginContractError("ORIGIN_EPOCH_INVALID")
        self._life_id = life_id
        self._epoch = epoch
        self._events: list[CommittedOriginEvent] = []
        self._lock = RLock()

    @property
    def life_id(self) -> str:
        return self._life_id

    @property
    def epoch(self) -> int:
        return self._epoch

    @property
    def head(self) -> str:
        with self._lock:
            return self._events[-1].event_sha256 if self._events else SHA256_ZERO

    @property
    def cycle(self) -> int:
        with self._lock:
            return self._events[-1].stamp.cycle if self._events else -1

    @property
    def event_ordinal(self) -> int:
        with self._lock:
            return self._events[-1].stamp.event_ordinal if self._events else -1

    def commit(
        self,
        proposal: OriginEventProposal,
        *,
        expected_head: str,
        advance_cycle: bool,
    ) -> CommittedOriginEvent:
        """Append one event or fail without changing the ledger.

        ``advance_cycle=True`` starts the next origin cycle.  A terminal event
        in the same turn uses ``advance_cycle=False`` and therefore shares the
        input event's cycle while still receiving the next event ordinal.
        """
        if type(advance_cycle) is not bool:
            raise OriginContractError("ADVANCE_CYCLE_BOOLEAN_REQUIRED")
        with self._lock:
            if expected_head != self.head:
                raise OriginContractError("LOG_HEAD_MISMATCH")
            prior_cycle = self.cycle
            cycle = prior_cycle + 1 if advance_cycle else prior_cycle
            if cycle < 0:
                raise OriginContractError("ORIGIN_REWIND")
            ordinal = self.event_ordinal + 1
            prior = self.head
            event_id = f"{self._life_id}:{self._epoch}:{ordinal:020d}"
            frozen_proposal = _copy_proposal(proposal)
            identity = {
                "event_id": event_id,
                "life_id": self._life_id,
                "epoch": self._epoch,
                "cycle": cycle,
                "event_ordinal": ordinal,
                "prior_event_sha256": prior,
                "proposal": frozen_proposal,
            }
            event_sha256 = sha256_canonical(identity)
            stamp = OriginStamp(
                life_id=self._life_id,
                epoch=self._epoch,
                cycle=cycle,
                event_ordinal=ordinal,
                log_head=event_sha256,
            )
            event = CommittedOriginEvent(
                event_id=event_id,
                stamp=stamp,
                proposal=frozen_proposal,
                prior_event_sha256=prior,
                event_sha256=event_sha256,
            )
            self._events.append(event)
            return copy.deepcopy(event)

    def snapshot(self) -> tuple[CommittedOriginEvent, ...]:
        """Return a detached immutable sequence; callers cannot alter history."""
        with self._lock:
            return tuple(copy.deepcopy(self._events))

    def verify(self) -> None:
        """Recompute every link and identity, raising on the first defect."""
        with self._lock:
            prior = SHA256_ZERO
            prior_cycle = -1
            for ordinal, event in enumerate(self._events):
                if event.stamp.life_id != self._life_id or event.stamp.epoch != self._epoch:
                    raise OriginContractError("LEDGER_ORIGIN_IDENTITY_MISMATCH")
                if event.stamp.event_ordinal != ordinal:
                    raise OriginContractError("EVENT_ORDINAL_DISCONTINUITY")
                if event.stamp.cycle not in (prior_cycle, prior_cycle + 1):
                    raise OriginContractError("ORIGIN_CYCLE_DISCONTINUITY")
                if ordinal == 0 and event.stamp.cycle != 0:
                    raise OriginContractError("ORIGIN_INITIAL_CYCLE_INVALID")
                if event.prior_event_sha256 != prior:
                    raise OriginContractError("LOG_CHAIN_INVALID")
                expected_id = f"{self._life_id}:{self._epoch}:{ordinal:020d}"
                if event.event_id != expected_id:
                    raise OriginContractError("EVENT_ID_MISMATCH")
                identity = {
                    "event_id": event.event_id,
                    "life_id": self._life_id,
                    "epoch": self._epoch,
                    "cycle": event.stamp.cycle,
                    "event_ordinal": event.stamp.event_ordinal,
                    "prior_event_sha256": prior,
                    "proposal": event.proposal,
                }
                expected_digest = sha256_canonical(identity)
                if event.event_sha256 != expected_digest or event.stamp.log_head != expected_digest:
                    raise OriginContractError("EVENT_DIGEST_MISMATCH")
                prior = event.event_sha256
                prior_cycle = event.stamp.cycle

    @classmethod
    def replay(
        cls,
        life_id: str,
        events: Iterable[CommittedOriginEvent],
        *,
        epoch: int = 0,
    ) -> "AppendOnlyOriginLedger":
        """Rebuild a ledger by re-executing every declared transition."""
        ledger = cls(life_id, epoch)
        for supplied in events:
            advance = supplied.stamp.cycle == ledger.cycle + 1
            if not advance and supplied.stamp.cycle != ledger.cycle:
                raise OriginContractError("ORIGIN_CYCLE_DISCONTINUITY")
            reproduced = ledger.commit(
                supplied.proposal,
                expected_head=ledger.head,
                advance_cycle=advance,
            )
            if to_primitive(reproduced) != to_primitive(supplied):
                raise OriginContractError("LEDGER_REPLAY_MISMATCH")
        ledger.verify()
        return ledger


def _copy_proposal(proposal: OriginEventProposal) -> OriginEventProposal:
    """Detach every caller-owned mutable value before it enters the ledger."""
    return OriginEventProposal(
        kind=proposal.kind,
        content=bytes(proposal.content),
        source=proposal.source,
        context=copy.deepcopy(dict(proposal.context)),
        valid_from=proposal.valid_from,
        valid_until=proposal.valid_until,
        supersedes=proposal.supersedes,
        observed_environment=proposal.observed_environment,
        observed_space=proposal.observed_space,
    )
