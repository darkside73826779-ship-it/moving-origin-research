from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import threading
import unittest

from src.m4_post_tokenizer_integration import (
    CandidateAdapter,
    FanoutCoordinator,
    IntegrationError,
    PeerAdapter,
    canonical_bytes as m4_canonical_bytes,
    encode_private_view,
    sha256_bytes as m4_sha256,
)
from src.situated_origin.contracts import SituatedContextPacket
from src.situated_origin.full_crash_cart import (
    FullAssemblyCrashCart,
    FullCrashCartError,
    ParallelAtomicM4Pair,
)
from src.situated_origin.m4_bridge import LocalBehaviorCapture
from src.situated_origin.runtime import SituatedRuntime


ROOT = Path(__file__).resolve().parents[1]


def provider(key):
    if key == "stop":
        return [700001, 700003]
    return [((key * 19) + index * 37) % 32749 for index in range(key)]


def rows():
    result = []
    for length in (1024, 4096, 8192):
        digest = m4_sha256(encode_private_view(provider(length)))
        result.append(
            {
                "context_length": length,
                "length": length,
                "sha256": digest,
                "expected_sha256": digest,
            }
        )
    return result


def stop():
    digest = m4_sha256(encode_private_view(provider("stop")))
    return {"length": 2, "sha256": digest, "expected_sha256": digest}


def plain(value):
    if isinstance(value, dict) or hasattr(value, "items"):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [plain(item) for item in value]
    return value


def pair_manifest(role: str):
    fixture = json.loads(
        (ROOT / "specs/data/m4_post_tokenizer_r_cc1_r_cc6_pair_fixture_v1.json")
        .read_text(encoding="utf-8")
    )
    return deepcopy(fixture[role]["artifact"])


class FakeClock:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def now(self):
        with self.lock:
            return self.value

    def sleep_until(self, target):
        with self.lock:
            self.value = max(self.value, target)

    def advance(self, delta):
        with self.lock:
            self.value += delta


class FullAssemblyBackend:
    """Public synthetic backend implementing the exact real-backend contract."""

    def __init__(self, role, session, capture, *, clock=None):
        self.role = role
        self.session = session
        self.capture = capture
        self.clock = clock
        self.state = {
            "generation": 0,
            "events": [],
            "live": True,
            "bound_context_identity": None,
            "bound_packet": None,
        }
        self.dispose_calls = 0
        self.step_observations = []
        self.fail_on_ordinal = None
        self.bad_backend_code_on_ordinal = None
        self.advance_after_ordinal = None
        self.advance_ns = 0

    def capture_state(self):
        return deepcopy(self.state)

    def restore_state(self, snapshot):
        self.state = deepcopy(snapshot)

    def session_identity(self):
        return self.session

    def dispose(self):
        self.dispose_calls += 1
        self.state["live"] = False

    def is_live(self):
        return self.state["live"]

    def bind_situated_context(self, packet, packet_identity):
        self.state["bound_context_identity"] = packet_identity
        self.state["bound_packet"] = {
            "rendered_sha256": packet.rendered_sha256,
            "source_log_head": packet.source_log_head,
        }
        return packet_identity

    def situated_context_identity(self):
        return self.state["bound_context_identity"]

    def clear_situated_context(self):
        self.state["bound_context_identity"] = None
        self.state["bound_packet"] = None

    def _receipt(self, operation, prior, request, *, request_ordinal=None):
        self.state["generation"] += 1
        self.state["events"].append(operation)
        return {
            "status": "PASS",
            "backend_code": None,
            "session_id": self.session,
            "prior_backend_state_sha256": prior,
            "result_backend_state_sha256": m4_sha256(
                (prior + operation + str(self.state["generation"])).encode()
            ),
            "request_sha256": m4_sha256(m4_canonical_bytes(plain(request))),
            "request_ordinal": request_ordinal,
        }

    def describe(self, _manifest, _config, request):
        return self._receipt("describe", "0" * 64, request)

    def initialize(self, _description, _session, request):
        prior = m4_sha256((("0" * 64) + "describe1").encode())
        return self._receipt("initialize", prior, request)

    def reset_episode(self, prior, request):
        return self._receipt("reset", prior, request)

    def step(self, prior, request, tokens):
        ordinal = request["request_ordinal"]
        situated = self.state["bound_context_identity"] is not None
        self.step_observations.append(
            {
                "thread_id": threading.get_ident(),
                "episode_id": request["episode_id"],
                "ordinal": ordinal,
                "token_sha256": tokens.sha256,
                "situated": situated,
                "context_identity": self.state["bound_context_identity"],
            }
        )
        if self.role == "peer" and situated:
            raise AssertionError("peer received situated context")
        if request["episode_id"].endswith("measured") and self.role == "candidate" and not situated:
            raise AssertionError("candidate did not receive situated context")
        if ordinal == self.fail_on_ordinal:
            raise IntegrationError("SYNTHETIC_BACKEND_FAILURE")
        output = (
            f"{self.role}|episode={request['episode_id']}|ordinal={ordinal}|"
            f"situated={str(situated).lower()}"
        ).encode()
        request_sha = m4_sha256(m4_canonical_bytes(plain(request)))
        self.capture.record(self.role, self.session, request_sha, output)
        receipt = self._receipt("step", prior, request, request_ordinal=ordinal)
        if ordinal == self.bad_backend_code_on_ordinal:
            receipt["backend_code"] = "NON_NULL"
        if self.clock is not None and ordinal == self.advance_after_ordinal:
            self.clock.advance(self.advance_ns)
        return receipt

    def snapshot(self, prior, request):
        return self._receipt("snapshot", prior, request)

    def close(self, prior, request):
        return self._receipt("close", prior, request)


class Binding:
    def bind_candidate(self, backend, packet, packet_identity):
        return backend.bind_situated_context(packet, packet_identity)

    def candidate_identity(self, backend):
        return backend.situated_context_identity()

    def peer_is_unbound(self, backend):
        return backend.situated_context_identity() is None

    def clear_candidate(self, backend):
        backend.clear_situated_context()


def request(operation_id, **values):
    return {
        "operation_id": operation_id,
        "caller_session_id": "full-crash-cart",
        "caller_thread_id": "pair-controller",
        **values,
    }


def ready_adapter(role, capture, *, clock=None):
    manifest = pair_manifest(role)
    backend = FullAssemblyBackend(
        role, manifest["runtime_instance_id"], capture, clock=clock
    )
    adapter_type = CandidateAdapter if role == "candidate" else PeerAdapter
    adapter = adapter_type(
        role,
        role,
        manifest,
        {"adapter_instance_id": f"full-crash-cart-{role}"},
        provider,
        backend,
    )
    adapter.describe(request(f"{role}-describe"))
    adapter.initialize(request(f"{role}-initialize"))
    return adapter, backend


def make_pair(*, clock=None):
    capture = LocalBehaviorCapture()
    candidate, candidate_backend = ready_adapter("candidate", capture, clock=clock)
    peer, peer_backend = ready_adapter("peer", capture, clock=clock)
    pair = ParallelAtomicM4Pair(
        coordinator=FanoutCoordinator(provider),
        candidate=candidate,
        peer=peer,
        context_binding=Binding(),
        behavior_capture=capture,
        token_counter=lambda text: max(1, len(text.encode("utf-8"))),
        candidate_token_budget=1_000_000,
        peer_token_budget=1_000_000,
        rows=rows(),
        stop=stop(),
    )
    return pair, candidate_backend, peer_backend, capture


def make_runner(*, clock=None):
    clock = clock or FakeClock()
    pair, candidate_backend, peer_backend, capture = make_pair(clock=clock)
    runtime = SituatedRuntime("full-assembly-test-life")
    rng_calls = []

    def insert_rng():
        rng_calls.append(runtime.head)
        return {
            "domain": "M4_FULL_ASSEMBLY_DIAGNOSTIC_RNG_V1",
            "inserted_after_log_head": runtime.head,
            "seed_class": "PUBLIC_DIAGNOSTIC",
        }

    runner = FullAssemblyCrashCart(
        runtime=runtime,
        pair=pair,
        clock_ns=clock.now,
        sleep_until_ns=clock.sleep_until,
        sampler=lambda target, completed, depth: {
            "monotonic_ns": target,
            "completed_pair_count": completed,
            "queue_depth_pairs": depth,
            "synthetic_ram_bytes": 1_000_000 + completed,
            "synthetic_vram_bytes": 0,
        },
        insert_diagnostic_rng=insert_rng,
    )
    return runner, pair, runtime, candidate_backend, peer_backend, capture, rng_calls


class FullAssemblyCrashCartTests(unittest.TestCase):
    def test_full_success_exercises_one_vehicle_topology(self):
        (
            runner,
            pair,
            runtime,
            candidate_backend,
            peer_backend,
            capture,
            rng_calls,
        ) = make_runner()
        report = runner.run()

        self.assertEqual(report["structural_status"], "PASS")
        self.assertIsNone(report["failure_code"])
        self.assertEqual(len(report["warmup"]["rows"]), 4)
        self.assertFalse(report["warmup"]["situated_privilege"])
        from src.m4_final_prescoring_crash_cart import fixture_inventory, warmup_plan
        self.assertEqual(
            [row["public_prompt_text"].encode("utf-8") for row in report["warmup"]["rows"]],
            [row["prompt"] for row in warmup_plan()],
        )
        self.assertEqual(len(report["active_window"]["rows"]), 64)
        self.assertEqual(
            [row["public_prompt_text"] for row in report["active_window"]["rows"]],
            [row["public_prompt_text"] for row in fixture_inventory()],
        )
        self.assertEqual(report["active_window"]["duration_ns"], 30_000_000_000)
        self.assertEqual(report["queue"]["capacity"], 8)
        self.assertLessEqual(report["queue"]["max_depth"], 8)
        self.assertGreaterEqual(report["queue"]["producer_block_count"], 1)
        self.assertEqual(report["queue"]["drop_count"], 0)
        self.assertEqual(report["queue"]["consumed_ordinals"], list(range(64)))
        self.assertEqual(len(report["telemetry"]), 121)
        self.assertEqual(report["telemetry"][0]["monotonic_ns"], 0)
        self.assertEqual(report["telemetry"][-1]["monotonic_ns"], 30_000_000_000)
        self.assertEqual([row["status"] for row in report["laws"]], ["HELD"] * 5)
        self.assertEqual(report["origin"]["event_count"], 128)
        self.assertTrue(report["origin"]["replay_verified"])
        replay = SituatedRuntime.replay(
            "full-assembly-test-life", runtime.kernel.events()
        )
        self.assertEqual(replay.head, runtime.head)

        self.assertEqual([row["phase"] for row in pair.reset_receipts], [
            "warmup", "measured", "final"
        ])
        self.assertEqual(report["cleanup"]["disposed_backend_count"], 2)
        self.assertTrue(report["cleanup"]["final_reset_complete"])
        self.assertTrue(report["cleanup"]["close_complete"])
        self.assertTrue(report["cleanup"]["capture_clear"])
        self.assertFalse(report["cleanup"]["backend_residue"])
        self.assertEqual(report["cleanup"]["finalize_call_count"], 1)
        self.assertEqual(report["clean_barrier"]["receipt"]["status"], "PASS")
        self.assertEqual(
            report["clean_barrier"]["receipt"]["next_request_ordinal"], 0
        )
        self.assertEqual(candidate_backend.dispose_calls, 1)
        self.assertEqual(peer_backend.dispose_calls, 1)
        self.assertTrue(capture.is_clear())
        self.assertEqual(len(rng_calls), 1)

        candidate_warmup = candidate_backend.step_observations[:4]
        candidate_active = candidate_backend.step_observations[4:]
        peer_all = peer_backend.step_observations
        self.assertTrue(all(not row["situated"] for row in candidate_warmup))
        self.assertTrue(all(row["situated"] for row in candidate_active))
        self.assertTrue(all(not row["situated"] for row in peer_all))
        self.assertEqual(
            [row["token_sha256"] for row in candidate_backend.step_observations],
            [row["token_sha256"] for row in peer_backend.step_observations],
        )
        self.assertNotEqual(
            candidate_backend.step_observations[0]["thread_id"],
            peer_backend.step_observations[0]["thread_id"],
        )
        self.assertTrue(all(
            row["execution_model"] == "PARALLEL_TWO_WORKER_SINGLE_BARRIER"
            for row in report["active_window"]["rows"]
        ))
        self.assertTrue(all(
            row["candidate"]["raw_output_text"]
            and row["peer"]["raw_output_text"]
            for row in report["active_window"]["rows"]
        ))

    def test_invalid_receipt_rolls_back_both_and_clears_capture(self):
        pair, candidate_backend, peer_backend, capture = make_pair()
        pair.reset_pair(phase="measured", episode_id="rollback-episode", reset_ordinal=1)
        candidate_before = pair.candidate.capture_transaction()
        peer_before = pair.peer.capture_transaction()
        candidate_backend.bad_backend_code_on_ordinal = 0
        prompt = "public rollback probe"
        runtime = SituatedRuntime("rollback-life")
        req = request(
            "rollback-step",
            episode_id="rollback-episode",
            request_ordinal=0,
            context_length=1024,
            is_terminal_request=True,
            id="rollback-step",
            content=prompt,
            question=prompt,
        )
        runtime.commit_input(req)
        snapshot = runtime.snapshot()
        recall = runtime.retrieve(snapshot, req)
        packet = runtime.prepare(snapshot, recall, req)

        with self.assertRaises((IntegrationError, FullCrashCartError)):
            pair.dispatch(request=req, shared_public_prompt=prompt, packet=packet)

        self.assertEqual(pair.candidate.capture_transaction(), candidate_before)
        self.assertEqual(pair.peer.capture_transaction(), peer_before)
        self.assertTrue(capture.is_clear())
        self.assertIsNone(candidate_backend.situated_context_identity())
        self.assertIsNone(peer_backend.situated_context_identity())
        candidate_backend.dispose()
        peer_backend.dispose()

    def test_post_pair_deadline_blocks_without_fabricating_final_row(self):
        clock = FakeClock()
        (
            runner,
            _pair,
            runtime,
            candidate_backend,
            peer_backend,
            capture,
            _rng_calls,
        ) = make_runner(clock=clock)
        candidate_backend.advance_after_ordinal = 63
        candidate_backend.advance_ns = 31_000_000_000
        report = runner.run()

        self.assertEqual(report["structural_status"], "BLOCKED")
        self.assertEqual(report["failure_code"], "ACTIVE_WINDOW_TIMEOUT_NO_RETRY")
        self.assertEqual(len(report["active_window"]["rows"]), 63)
        self.assertEqual(runtime.kernel.events()[-1].proposal.kind, "TURN_ABORTED")
        self.assertEqual(runtime.kernel.events()[-2].proposal.kind, "INPUT_COMMITTED")
        self.assertEqual(candidate_backend.dispose_calls, 1)
        self.assertEqual(peer_backend.dispose_calls, 1)
        self.assertTrue(capture.is_clear())
        self.assertFalse(report["cleanup"]["backend_residue"])
        self.assertTrue(report["cleanup"]["final_reset_complete"])
        self.assertTrue(report["cleanup"]["close_complete"])

    def test_report_contains_no_answer_labels_or_scientific_scores(self):
        report = make_runner()[0].run()
        encoded = json.dumps(report, sort_keys=True)
        for forbidden in (
            '"answer"',
            '"answer_label"',
            '"correct_answer"',
            '"ground_truth"',
            '"scientific_score"',
            '"qualification_result"',
        ):
            self.assertNotIn(forbidden, encoded)
        self.assertIn("NON_SCORING_PUBLIC_BEHAVIOR_OBSERVATION", encoded)


if __name__ == "__main__":
    unittest.main()
