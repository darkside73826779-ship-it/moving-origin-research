"""Focused custody-free tests for the situated-origin ledger and kernel."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import unittest

from src.situated_origin.contracts import (
    OriginContractError,
    OriginEventProposal,
    ProvenanceHandle,
    SHA256_ZERO,
    Unavailable,
    sha256_bytes,
    to_primitive,
)
from src.situated_origin.kernel import (
    INPUT_COMMITTED,
    OUTPUT_COMMITTED,
    TURN_ABORTED,
    SituatedOriginKernel,
)
from src.situated_origin.ledger import AppendOnlyOriginLedger


def source(name: str = "public-test") -> ProvenanceHandle:
    return ProvenanceHandle("synthetic", name, sha256_bytes(name.encode("utf-8")))


def proposal(
    kind: str,
    text: str,
    *,
    episode: str = "episode-alpha",
    environment: str | Unavailable = Unavailable("NOT_OBSERVED"),
    space: str | Unavailable = Unavailable("NOT_OBSERVED"),
) -> OriginEventProposal:
    return OriginEventProposal(
        kind=kind,
        content=text.encode("utf-8"),
        source=source(),
        context={
            "episode_id": episode,
            "interaction_place": "public-test-channel",
            "active_task": "assembly-preflight",
        },
        observed_environment=environment,
        observed_space=space,
    )


class AppendOnlyLedgerTests(unittest.TestCase):
    def test_expected_head_chain_and_detached_return(self) -> None:
        ledger = AppendOnlyOriginLedger("life-alpha")
        original = proposal("OBSERVED", "one")
        first = ledger.commit(original, expected_head=SHA256_ZERO, advance_cycle=True)
        self.assertEqual((first.stamp.cycle, first.stamp.event_ordinal), (0, 0))
        self.assertEqual(first.prior_event_sha256, SHA256_ZERO)

        # Returned nested mappings are detached from the ledger's stored copy.
        first.proposal.context["episode_id"] = "tampered"
        self.assertEqual(ledger.snapshot()[0].proposal.context["episode_id"], "episode-alpha")

        with self.assertRaisesRegex(OriginContractError, "LOG_HEAD_MISMATCH"):
            ledger.commit(original, expected_head=SHA256_ZERO, advance_cycle=True)

        second = ledger.commit(
            proposal("TERMINAL", "two"),
            expected_head=ledger.head,
            advance_cycle=False,
        )
        self.assertEqual((second.stamp.cycle, second.stamp.event_ordinal), (0, 1))
        self.assertEqual(second.prior_event_sha256, ledger.snapshot()[0].event_sha256)
        ledger.verify()

    def test_genesis_cannot_commit_same_cycle_or_rewind(self) -> None:
        ledger = AppendOnlyOriginLedger("life-alpha")
        with self.assertRaisesRegex(OriginContractError, "ORIGIN_REWIND"):
            ledger.commit(
                proposal("BAD", "bad"),
                expected_head=SHA256_ZERO,
                advance_cycle=False,
            )
        self.assertEqual(ledger.head, SHA256_ZERO)
        self.assertEqual(ledger.snapshot(), ())

    def test_ledger_replay_is_byte_identity_deterministic(self) -> None:
        ledger = AppendOnlyOriginLedger("life-alpha", epoch=2)
        ledger.commit(proposal("A", "one"), expected_head=ledger.head, advance_cycle=True)
        ledger.commit(proposal("B", "two"), expected_head=ledger.head, advance_cycle=False)
        ledger.commit(proposal("C", "three"), expected_head=ledger.head, advance_cycle=True)
        replayed = AppendOnlyOriginLedger.replay(
            "life-alpha", ledger.snapshot(), epoch=2
        )
        self.assertEqual(
            [to_primitive(row) for row in replayed.snapshot()],
            [to_primitive(row) for row in ledger.snapshot()],
        )
        self.assertEqual(replayed.head, ledger.head)


class SituatedOriginKernelTests(unittest.TestCase):
    def test_success_and_abort_are_terminal_same_cycle_events(self) -> None:
        kernel = SituatedOriginKernel("life-alpha")
        first_input = kernel.commit_input(
            "turn-1",
            proposal("USER_INPUT", "hello", environment="runtime-a"),
            expected_head=kernel.head,
        )
        self.assertEqual(first_input.proposal.kind, INPUT_COMMITTED)
        self.assertEqual((first_input.stamp.cycle, first_input.stamp.event_ordinal), (0, 0))
        self.assertEqual(kernel.active_turn_id, "turn-1")

        output = kernel.commit_output(
            "turn-1",
            proposal("MODEL_OUTPUT", "response"),
            expected_head=kernel.head,
        )
        self.assertEqual(output.proposal.kind, OUTPUT_COMMITTED)
        self.assertEqual((output.stamp.cycle, output.stamp.event_ordinal), (0, 1))
        self.assertIsNone(kernel.active_turn_id)

        second_input = kernel.commit_input(
            "turn-2", proposal("USER_INPUT", "next"), expected_head=kernel.head
        )
        aborted = kernel.abort_turn(
            "turn-2", "BACKEND_FAILED", expected_head=kernel.head
        )
        self.assertEqual((second_input.stamp.cycle, aborted.stamp.cycle), (1, 1))
        self.assertEqual(aborted.proposal.kind, TURN_ABORTED)
        self.assertEqual(aborted.proposal.context["reason"], "BACKEND_FAILED")
        self.assertEqual(
            [row.status for row in kernel.journal()],
            [INPUT_COMMITTED, OUTPUT_COMMITTED, INPUT_COMMITTED, TURN_ABORTED],
        )
        self.assertEqual([row.journal_ordinal for row in kernel.journal()], list(range(4)))
        kernel.verify()

    def test_transaction_ordering_and_expected_head_fail_closed(self) -> None:
        kernel = SituatedOriginKernel("life-alpha")
        with self.assertRaisesRegex(OriginContractError, "TURN_NOT_OPEN"):
            kernel.commit_output(
                "missing", proposal("MODEL_OUTPUT", "bad"), expected_head=kernel.head
            )
        kernel.commit_input(
            "turn-1", proposal("USER_INPUT", "hello"), expected_head=kernel.head
        )
        retained_head = kernel.head
        with self.assertRaisesRegex(OriginContractError, "TURN_ALREADY_OPEN"):
            kernel.commit_input(
                "turn-2", proposal("USER_INPUT", "overlap"), expected_head=kernel.head
            )
        with self.assertRaisesRegex(OriginContractError, "TURN_ID_MISMATCH"):
            kernel.abort_turn("turn-wrong", "bad", expected_head=kernel.head)
        with self.assertRaisesRegex(OriginContractError, "LOG_HEAD_MISMATCH"):
            kernel.commit_output(
                "turn-1", proposal("MODEL_OUTPUT", "bad"), expected_head=SHA256_ZERO
            )
        self.assertEqual(kernel.head, retained_head)
        self.assertEqual(len(kernel.events()), 1)

    def test_frame_is_immutable_and_future_capabilities_are_typed_unavailable(self) -> None:
        kernel = SituatedOriginKernel("life-alpha")
        genesis = kernel.current()
        self.assertIsInstance(genesis.environment.world_place, Unavailable)
        self.assertIsInstance(genesis.protention, Unavailable)
        self.assertIsInstance(genesis.homeostasis, Unavailable)
        self.assertIsInstance(genesis.experience_strip, Unavailable)
        with self.assertRaises(FrozenInstanceError):
            genesis.active_episode = "rewritten"  # type: ignore[misc]

        kernel.commit_input(
            "turn-1",
            proposal(
                "USER_INPUT",
                "hello",
                environment="runtime-a",
                space=Unavailable("WORLD_PLACE_UNOBSERVED"),
            ),
            expected_head=kernel.head,
        )
        current = kernel.current()
        self.assertEqual(current.environment.runtime_place, "runtime-a")
        self.assertIsInstance(current.environment.world_place, Unavailable)
        self.assertEqual(current.stamp.log_head, kernel.head)
        self.assertNotEqual(current.frame_sha256, genesis.frame_sha256)
        self.assertEqual(kernel.frame_at_event_ordinal(-1), genesis)
        self.assertEqual(kernel.frame_at_event_ordinal(0), current)

    def test_view_source_heads_are_checked_against_current_origin(self) -> None:
        kernel = SituatedOriginKernel("life-alpha")
        kernel.commit_input(
            "turn-1", proposal("USER_INPUT", "hello"), expected_head=kernel.head
        )
        fact_head, access_head = kernel.assert_materialized_view_sources(
            fact_source_head=kernel.head, access_source_head=kernel.head
        )
        self.assertEqual(fact_head, kernel.current().fact_graph_head)
        self.assertEqual(access_head, kernel.current().access_ledger_head)
        with self.assertRaisesRegex(OriginContractError, "VIEW_HEAD_STALE"):
            kernel.assert_materialized_view_sources(
                fact_source_head=SHA256_ZERO, access_source_head=kernel.head
            )

    def test_replay_reproduces_frames_journal_and_open_turn(self) -> None:
        kernel = SituatedOriginKernel("life-alpha", epoch=3)
        kernel.advance_origin(
            proposal("CADENCE", "tick"), expected_head=kernel.head
        )
        kernel.commit_input(
            "turn-1", proposal("USER_INPUT", "hello"), expected_head=kernel.head
        )
        kernel.commit_output(
            "turn-1", proposal("MODEL_OUTPUT", "response"), expected_head=kernel.head
        )
        kernel.commit_input(
            "turn-open", proposal("USER_INPUT", "pending"), expected_head=kernel.head
        )
        replayed = SituatedOriginKernel.replay(
            "life-alpha", kernel.events(), epoch=3
        )
        self.assertEqual(replayed.head, kernel.head)
        self.assertEqual(replayed.active_turn_id, "turn-open")
        self.assertEqual(
            [to_primitive(row) for row in replayed.frames()],
            [to_primitive(row) for row in kernel.frames()],
        )
        self.assertEqual(
            [to_primitive(row) for row in replayed.journal()],
            [to_primitive(row) for row in kernel.journal()],
        )
        replayed.verify()


if __name__ == "__main__":
    unittest.main()
