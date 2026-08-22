"""Custody-free, stub-only tests for the public observation backend."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from src.m4_post_tokenizer_integration import (
    IntegrationError,
    PrivateTokenView,
    canonical_bytes,
    encode_private_view,
)
from src import m4_public_model_observation_backend as backend_module
from src.m4_public_model_observation_backend import (
    BACKEND_NAME,
    BackendDependencies,
    DEPENDENCY_AUTHORITY,
    GENERATION_CONTROLS,
    LAW_PROJECTION_SHA256,
    MODEL_IDENTITY,
    MODEL_IDENTITY_SHA256,
    ObservationFailure,
    PROMPT_SHA256,
    PublicModelObservationBackend,
    PublicObservationFactory,
    RUNTIME_IDENTITY,
    RUNTIME_IDENTITY_SHA256,
    build_backend_constructor,
    classify_network_connect,
    generate_public_prompt,
    held_law_rows,
)


COMMON = {"caller_session_id": "caller-public", "caller_thread_id": "thread-public"}


def request(operation_id: str, **extra):
    return {"operation_id": operation_id, **COMMON, **extra}


def manifest() -> dict:
    digest = lambda character: character * 64
    return {
        "access_policy_id": "public-local-only",
        "architecture_sha256": digest("1"),
        "binning_definition_sha256": digest("2"),
        "calibration_contract_sha256": digest("3"),
        "channel_policy": "OBSERVABLE_ONLY",
        "checkpoint_revision": MODEL_IDENTITY["revision"],
        "checkpoint_sha256": MODEL_IDENTITY_SHA256,
        "decoding_sha256": digest("4"),
        "evaluation_data_sha256": digest("5"),
        "parameter_count": 4_000_000_000,
        "quantization_sha256": digest("6"),
        "redaction_receipt_sha256": digest("7"),
        "role": "control",
        "runtime_instance_id": "public-observation-session-v1",
        "scientific_arm": "naive",
        "tokenizer_sha256": MODEL_IDENTITY["tokenizer_file"]["sha256"],
        "training_instance_sha256": digest("8"),
        "weight_hashes": [MODEL_IDENTITY["model_file"]["sha256"]],
    }


class StubEngine:
    def __init__(self, box: dict, result_mode: str = "pass"):
        self.box = box
        self.result_mode = result_mode
        self.live = True
        box["live_count"] += 1
        box["engines"].append(self)

    def is_live(self):
        return self.live

    def generate(self, *, prompt_token_ids, sampling_params):
        self.box["calls"] += 1
        self.box["input_reference"] = prompt_token_ids
        self.box["controls"] = sampling_params
        if self.result_mode == "raise":
            raise RuntimeError("stub-generation-failure")
        if self.result_mode == "multiple":
            return [{"token_ids": [9], "text": "a"}, {"token_ids": [9], "text": "a"}]
        if self.result_mode == "raw_extra":
            return [{"token_ids": [9], "text": "stub", "raw_prompt": "forbidden"}]
        output = [9, 10]
        self.box["output_reference"] = output
        return [{"token_ids": output, "text": "stub-output"}]

    def shutdown(self):
        if self.live:
            self.live = False
            self.box["live_count"] -= 1


class ReceiptMutator:
    def __init__(self, backend, mutate):
        self.backend = backend
        self.mutate = mutate

    def __getattr__(self, name):
        return getattr(self.backend, name)

    def step(self, prior, request_value, tokens):
        receipt = dict(self.backend.step(prior, request_value, tokens))
        self.mutate(receipt, tokens)
        return receipt


class Fixture:
    def __init__(self, *, dependency=None, identity=None, engine_mode="pass",
                 engine_loader_raises=False, write_hook=lambda _phase: None,
                 live_count_override=None, stage_path=None, stage_mode=0o700,
                 namespace=True):
        self.temporary = tempfile.TemporaryDirectory()
        self.stage = (Path(stage_path).absolute() if stage_path is not None
                      else Path(self.temporary.name).resolve())
        self.stage.mkdir(parents=True, exist_ok=True)
        self.box = {"calls": 0, "controls": None, "engines": [], "input_reference": None,
                    "live_count": 0, "output_reference": None}
        self.clock = iter((100, 175, 200, 290, 300, 415))
        self.implementation_sha256 = "a" * 64
        self.dependency_sha256 = "b" * 64
        self.config = {
            "adapter_instance_id": "public-control-adapter",
            "backend_name": BACKEND_NAME,
            "dependency_sha256": self.dependency_sha256,
            "implementation_sha256": self.implementation_sha256,
            "model_sha256": MODEL_IDENTITY_SHA256,
            "production_path": True,
            "tokenizer_sha256": MODEL_IDENTITY["tokenizer_file"]["sha256"],
        }
        self.config_bytes = canonical_bytes(self.config)
        expected_identity = {
            "model_identity": MODEL_IDENTITY,
            "model_identity_sha256": MODEL_IDENTITY_SHA256,
            "runtime_identity": RUNTIME_IDENTITY,
            "runtime_identity_sha256": RUNTIME_IDENTITY_SHA256,
        }
        def loader():
            if engine_loader_raises:
                raise RuntimeError("stub-load-failure")
            return StubEngine(self.box, engine_mode)
        self.dependencies = BackendDependencies(
            session_id=manifest()["runtime_instance_id"], stage=self.stage,
            implementation_sha256=self.implementation_sha256,
            dependency_sha256=self.dependency_sha256, model_sha256=MODEL_IDENTITY_SHA256,
            tokenizer_sha256=MODEL_IDENTITY["tokenizer_file"]["sha256"],
            valid_token_ids=frozenset(range(1000)),
            identity_probe=lambda: deepcopy(identity if identity is not None else expected_identity),
            dependency_probe=lambda: deepcopy(dependency if dependency is not None else DEPENDENCY_AUTHORITY),
            namespace_probe=lambda: namespace, engine_loader=loader,
            stage_mode_probe=lambda _path: stage_mode, file_mode_probe=lambda _path: 0o600,
            clock_ns=lambda: next(self.clock), cleanup_runtime=lambda: None,
            live_engine_count=(live_count_override or (lambda: self.box["live_count"])),
            write_hook=write_hook,
        )
        self.instances = []
        base_constructor = build_backend_constructor(self.dependencies)
        def constructor():
            instance = base_constructor()
            self.instances.append(instance)
            return instance
        registry = {BACKEND_NAME: (
            constructor, self.implementation_sha256, self.dependency_sha256,
            hashlib.sha256(self.config_bytes).hexdigest(),
        )}
        self.factory = PublicObservationFactory(registry)

    def close(self):
        for instance in self.instances:
            if instance.is_live():
                try:
                    instance.dispose()
                except Exception:
                    pass
        self.temporary.cleanup()

    def adapter(self, constructor_override=None):
        if constructor_override is None:
            factory = self.factory
        else:
            registry = {BACKEND_NAME: (
                constructor_override, self.implementation_sha256, self.dependency_sha256,
                hashlib.sha256(self.config_bytes).hexdigest(),
            )}
            factory = PublicObservationFactory(registry)
        return factory.create("control", "naive", canonical_bytes(manifest()), self.config_bytes,
                              lambda _context: [1, 2, 3])


def initialize_adapter(fixture: Fixture, adapter=None):
    adapter = adapter or fixture.adapter()
    adapter.describe(request("describe"))
    adapter.initialize(request("initialize"))
    return adapter


def reset_adapter(adapter, ordinal=1, episode="episode-public"):
    adapter.reset_episode(request("reset", episode_id=episode, reset_ordinal=ordinal))


def step_request(ordinal=0, prompt_ordinal=0, episode="episode-public", context_length=3):
    return request("step", episode_id=episode, request_ordinal=ordinal, context_length=context_length,
                   is_terminal_request=True, prompt_ordinal=prompt_ordinal,
                   prompt_sha256=PROMPT_SHA256[prompt_ordinal])


def private_view(items=(1, 2, 3), context=3):
    return PrivateTokenView(context, encode_private_view(items))


class PublicObservationBackendTests(unittest.TestCase):
    def test_exact_public_prompt_identity_and_held_projection(self):
        expected = (
            "67b8b141b7fabd3032c8ff738634eb9d6d874683062a8250c28e2b5d2ddd9e07",
            "f8022e23ee07ab212bd0a83f279a247b98b9c8d61ed85bca0cb15781efa12048",
            "f1f2f3eeb7e2c1095e559c44bb07769d1b5bd19434889a3c17f577f35da92447",
        )
        self.assertEqual(PROMPT_SHA256, expected)
        for ordinal in range(3):
            generated = bytearray(generate_public_prompt(ordinal))
            self.assertEqual(len(generated), 122)
            self.assertEqual(hashlib.sha256(generated).hexdigest(), expected[ordinal])
            generated[:] = b"\0" * len(generated)
        rows = held_law_rows()
        self.assertEqual([row["law_id"] for row in rows], ["L7", "L8", "L10", "L14", "L18"])
        self.assertTrue(all(row["status"] == "HELD" and row["claim_made"] is False for row in rows))
        self.assertEqual(len(canonical_bytes(rows)), 974)
        self.assertEqual(hashlib.sha256(canonical_bytes(rows)).hexdigest(), LAW_PROJECTION_SHA256)

    def test_constructor_live_without_engine_and_exact_protocol_surface(self):
        fixture = Fixture()
        self.addCleanup(fixture.close)
        backend = build_backend_constructor(fixture.dependencies)()
        self.assertIs(backend.is_live(), True)
        state = backend.capture_state()
        self.assertIs(state["engine_loaded"], False)
        self.assertEqual(state["phase"], "CONSTRUCTED_LIVE_NO_ENGINE")
        for method in ("capture_state", "restore_state", "session_identity", "dispose", "is_live",
                       "describe", "initialize", "reset_episode", "step", "snapshot", "close"):
            self.assertTrue(callable(getattr(backend, method)))
        backend.dispose()
        self.assertIs(backend.is_live(), False)

    def test_registration_rejects_every_non_control_naive_before_construction(self):
        fixture = Fixture()
        self.addCleanup(fixture.close)
        cases = (("candidate", "candidate"), ("peer", "peer"), ("control", "empty"),
                 ("control", "oracle"), ("control", "frozen"))
        for role, arm in cases:
            with self.subTest(role=role, arm=arm), self.assertRaisesRegex(IntegrationError, "ROLE_ARM_MISMATCH"):
                fixture.factory.create(role, arm, canonical_bytes(manifest()), fixture.config_bytes,
                                       lambda _context: [1, 2, 3])
        with self.assertRaisesRegex(IntegrationError, "ROLE_ARM_MISMATCH"):
            fixture.factory.create_pair(b"{}", b"{}", b"{}", b"{}", lambda _context: [])
        self.assertEqual(fixture.instances, [])

    def test_describe_is_seven_field_no_engine_and_dependency_stage_fail_closed(self):
        fixture = Fixture()
        self.addCleanup(fixture.close)
        adapter = fixture.adapter()
        receipt = adapter.describe(request("describe"))
        self.assertEqual(set(receipt), backend_module.RECEIPT_FIELDS)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(fixture.box["live_count"], 0)
        self.assertIs(adapter.backend.capture_state()["engine_loaded"], False)
        for mutation in (dict(DEPENDENCY_AUTHORITY, status="BLOCK"), {}):
            failed = Fixture(dependency=mutation)
            self.addCleanup(failed.close)
            with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE") as caught:
                failed.adapter().describe(request("describe"))
            self.assertEqual(caught.exception.backend_code, "SYNTHETIC_REJECTED")
            self.assertEqual(failed.box["live_count"], 0)
        nonempty = Fixture()
        self.addCleanup(nonempty.close)
        (nonempty.stage / "unexpected").write_text("public")
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
            nonempty.adapter().describe(request("describe"))

    def test_stage_absent_linked_and_wrong_mode_are_separate_fail_closed_cases(self):
        wrong_mode = Fixture(stage_mode=0o755)
        self.addCleanup(wrong_mode.close)
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
            wrong_mode.adapter().describe(request("describe"))

        absent = Fixture()
        self.addCleanup(absent.close)
        absent.stage.rmdir()
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
            absent.adapter().describe(request("describe"))

        target = tempfile.TemporaryDirectory(); self.addCleanup(target.cleanup)
        link_parent = tempfile.TemporaryDirectory(); self.addCleanup(link_parent.cleanup)
        link = Path(link_parent.name) / "linked-stage"
        try:
            link.symlink_to(Path(target.name), target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"directory symlink unavailable: {exc}")
        linked = Fixture(stage_path=link)
        self.addCleanup(linked.close)
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
            linked.adapter().describe(request("describe"))

    def test_initialize_authenticates_identity_before_one_stub_load(self):
        fixture = Fixture()
        self.addCleanup(fixture.close)
        adapter = fixture.adapter()
        adapter.describe(request("describe"))
        receipt = adapter.initialize(request("initialize"))
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(fixture.box["live_count"], 1)
        self.assertIs(adapter.backend.capture_state()["engine_loaded"], True)
        bad_identity = {"model_identity": {}, "model_identity_sha256": "0" * 64,
                        "runtime_identity": {}, "runtime_identity_sha256": "0" * 64}
        failed = Fixture(identity=bad_identity)
        self.addCleanup(failed.close)
        bad = failed.adapter(); bad.describe(request("describe"))
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
            bad.initialize(request("initialize"))
        self.assertEqual(failed.box["live_count"], 0)
        self.assertEqual(failed.box["engines"], [])

        for namespace in (False, None, 0):
            namespace_failed = Fixture(namespace=namespace)
            self.addCleanup(namespace_failed.close)
            blocked = namespace_failed.adapter(); blocked.describe(request("describe"))
            with self.subTest(namespace=namespace), self.assertRaisesRegex(
                    IntegrationError, "BACKEND_DECLARED_FAILURE"):
                blocked.initialize(request("initialize"))
            self.assertEqual(namespace_failed.box["engines"], [])

    def test_engine_load_failure_has_no_retry_or_residue(self):
        fixture = Fixture(engine_loader_raises=True)
        self.addCleanup(fixture.close)
        adapter = fixture.adapter(); adapter.describe(request("describe"))
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
            adapter.initialize(request("initialize"))
        self.assertEqual(fixture.box["engines"], [])
        self.assertEqual(fixture.box["live_count"], 0)

    def test_three_stub_only_episodes_publish_sanitized_pairs_and_zeroize_arrays(self):
        fixture = Fixture()
        self.addCleanup(fixture.close)
        adapter = initialize_adapter(fixture)
        receipts = []
        for ordinal in range(3):
            episode = f"episode-{ordinal}"
            reset_adapter(adapter, ordinal=ordinal + 1, episode=episode)
            receipts.append(adapter.step(step_request(prompt_ordinal=ordinal, episode=episode), private_view()))
            self.assertEqual(fixture.box["input_reference"], [0, 0, 0])
            self.assertEqual(fixture.box["output_reference"], [0, 0])
        self.assertTrue(all(set(receipt) == backend_module.RECEIPT_FIELDS for receipt in receipts))
        self.assertEqual(fixture.box["calls"], 3)
        self.assertEqual(fixture.box["controls"], GENERATION_CONTROLS)
        json_paths = sorted(fixture.stage.glob("*.json"))
        sidecars = sorted(fixture.stage.glob("*.json.sha256"))
        self.assertEqual((len(json_paths), len(sidecars)), (3, 3))
        forbidden = {"prompt", "prompt_text", "token_ids", "output_text", "private_path", "environment"}
        for path in json_paths:
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw)
            value = json.loads(raw)
            PublicModelObservationBackend._validate_observation(value)
            self.assertFalse(forbidden & set(value))
            self.assertTrue(all(value[field] is False for field in (
                "scientific_evidence", "authoritative_scoring", "qualification_evidence", "readiness_evidence")))
            sidecar = path.with_name(path.name + ".sha256").read_text("ascii")
            self.assertEqual(sidecar, hashlib.sha256(raw).hexdigest() + "  " + path.name + "\n")
        before = sorted(path.name for path in fixture.stage.iterdir())
        adapter.snapshot(request("snapshot", snapshot_ordinal=0))
        self.assertEqual(sorted(path.name for path in fixture.stage.iterdir()), before)
        adapter.close(request("close"))
        self.assertEqual(fixture.box["live_count"], 0)
        self.assertIs(adapter.backend.is_live(), False)

    def test_private_view_compound_negatives_are_each_pre_generation(self):
        cases = {
            "magic": PrivateTokenView(3, b"X" * 47),
            "count": PrivateTokenView(3, encode_private_view([1, 2])),
            "length": PrivateTokenView(3, encode_private_view([1, 2, 3])[:-1]),
            "negative": private_view((1, -1, 3)),
            "nonmember": private_view((1, 1001, 3)),
            "context": PrivateTokenView(2, encode_private_view([1, 2])),
        }
        for label, view in cases.items():
            fixture = Fixture(); self.addCleanup(fixture.close)
            adapter = initialize_adapter(fixture); reset_adapter(adapter)
            expected = "CONTEXT_REQUEST_MISMATCH" if label == "context" else "BACKEND_DECLARED_FAILURE"
            with self.subTest(label=label), self.assertRaisesRegex(IntegrationError, expected):
                adapter.step(step_request(), view)
            self.assertEqual(fixture.box["calls"], 0)
            self.assertEqual(list(fixture.stage.iterdir()), [])

    def test_zero_count_private_view_is_rejected_before_engine_and_restored_exactly(self):
        fixture = Fixture(); self.addCleanup(fixture.close)
        adapter = initialize_adapter(fixture); reset_adapter(adapter)
        before_adapter = deepcopy(adapter.capture_transaction())
        before_backend = deepcopy(adapter.backend.capture_state())
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE") as caught:
            adapter.step(step_request(context_length=0), private_view((), context=0))
        self.assertEqual(caught.exception.backend_code, "SYNTHETIC_REJECTED")
        self.assertEqual(fixture.box["calls"], 0)
        self.assertEqual(list(fixture.stage.iterdir()), [])
        self.assertEqual(adapter.capture_transaction(), before_adapter)
        self.assertEqual(adapter.backend.capture_state(), before_backend)

    def test_observation_validator_enforces_positive_input_count(self):
        fixture = Fixture(); self.addCleanup(fixture.close)
        adapter = initialize_adapter(fixture); reset_adapter(adapter)
        adapter.step(step_request(), private_view())
        observation = json.loads(next(fixture.stage.glob("*.json")).read_bytes())
        observation["input_token_count"] = 0
        with self.assertRaisesRegex(ObservationFailure, "OBSERVATION_EVIDENCE_BOUNDARY_FAILURE"):
            PublicModelObservationBackend._validate_observation(observation)

    def test_prompt_ordinal_digest_and_order_negatives_are_pre_generation(self):
        mutations = (
            {"prompt_ordinal": 1, "prompt_sha256": PROMPT_SHA256[1]},
            {"prompt_ordinal": 0, "prompt_sha256": "0" * 64},
            {"prompt_ordinal": 3, "prompt_sha256": "0" * 64},
        )
        for mutation in mutations:
            fixture = Fixture(); self.addCleanup(fixture.close)
            adapter = initialize_adapter(fixture); reset_adapter(adapter)
            value = step_request(); value.update(mutation)
            with self.subTest(mutation=mutation), self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
                adapter.step(value, private_view())
            self.assertEqual(fixture.box["calls"], 0)
            self.assertEqual(list(fixture.stage.iterdir()), [])

    def test_generation_shape_exception_and_raw_field_fail_without_publication(self):
        for mode in ("raise", "multiple", "raw_extra"):
            fixture = Fixture(engine_mode=mode); self.addCleanup(fixture.close)
            adapter = initialize_adapter(fixture); reset_adapter(adapter)
            with self.subTest(mode=mode), self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
                adapter.step(step_request(), private_view())
            self.assertEqual(list(fixture.stage.iterdir()), [])

    def test_partial_local_write_is_removed_and_adapter_state_is_unchanged(self):
        def fail_sidecar(phase):
            if phase == "before_sidecar":
                raise OSError("synthetic-write-failure")
        fixture = Fixture(write_hook=fail_sidecar)
        self.addCleanup(fixture.close)
        adapter = initialize_adapter(fixture); reset_adapter(adapter)
        before = adapter.capture()
        with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
            adapter.step(step_request(), private_view())
        self.assertEqual(adapter.capture(), before)
        self.assertEqual(list(fixture.stage.iterdir()), [])

    def test_every_adapter_receipt_rejection_restores_exact_stage_inventory(self):
        def mutations():
            return (
                lambda receipt, _tokens: receipt.pop("status"),
                lambda receipt, _tokens: receipt.update(status="UNKNOWN"),
                lambda receipt, _tokens: receipt.update(request_sha256="0" * 64),
                lambda receipt, _tokens: receipt.update(request_ordinal=99),
                lambda receipt, _tokens: receipt.update(backend_code="OBSERVATION_GENERATION_FAILED"),
                lambda receipt, _tokens: receipt.update(session_id="wrong-session"),
                lambda receipt, _tokens: receipt.update(prior_backend_state_sha256="0" * 64),
                lambda receipt, _tokens: receipt.update(result_backend_state_sha256="bad"),
                lambda receipt, tokens: object.__setattr__(tokens, "bytes_view", encode_private_view([4, 5, 6])),
            )
        for index, mutate in enumerate(mutations()):
            fixture = Fixture(); self.addCleanup(fixture.close)
            raw_backend = build_backend_constructor(fixture.dependencies)()
            wrapper = ReceiptMutator(raw_backend, mutate)
            adapter = fixture.adapter(lambda: wrapper)
            initialize_adapter(fixture, adapter); reset_adapter(adapter)
            before_adapter, before_backend = adapter.capture(), deepcopy(raw_backend.capture_state())
            with self.subTest(index=index), self.assertRaises(IntegrationError):
                adapter.step(step_request(), private_view())
            self.assertEqual(adapter.capture(), before_adapter)
            self.assertEqual(raw_backend.capture_state(), before_backend)
            self.assertEqual(list(fixture.stage.iterdir()), [])

    def test_rollback_inventory_noop_partial_wrong_and_throwing_cleanup_fail_closed(self):
        modes = ("noop", "partial", "wrong", "throw")
        for mode in modes:
            fixture = Fixture(); self.addCleanup(fixture.close)
            backend = build_backend_constructor(fixture.dependencies)()
            before = deepcopy(backend.capture_state())
            extra = fixture.stage / "m4-public-observation-extra.json"
            extra.write_text("{}\n", encoding="utf-8")
            backend._owned_paths.add(extra.name)
            original = backend._remove_path
            if mode == "noop":
                backend._remove_path = lambda _name: None
            elif mode == "partial":
                backend._remove_path = lambda name: None if name == extra.name else original(name)
            elif mode == "wrong":
                backend._inventory = lambda: [{"name": "wrong"}]
            else:
                backend._remove_path = lambda _name: (_ for _ in ()).throw(OSError("restore"))
            with self.subTest(mode=mode), self.assertRaisesRegex(IntegrationError, "BACKEND_ROLLBACK_FAILURE"):
                backend.restore_state(before)
            self.assertIs(backend.is_live(), False)

    def test_cleanup_failure_prevents_close_pass(self):
        fixture = Fixture(live_count_override=lambda: 1)
        self.addCleanup(fixture.close)
        adapter = fixture.adapter(); adapter.describe(request("describe"))
        adapter.initialize(request("initialize"))
        with self.assertRaisesRegex(IntegrationError, "BACKEND_ROLLBACK_FAILURE"):
            adapter.close(request("close"))
        self.assertEqual(fixture.box["calls"], 0)

    def test_network_errno_classifier_exact_semantics(self):
        self.assertEqual(classify_network_connect(
            lambda: (_ for _ in ()).throw(OSError(101, "Network is unreachable"))), 0)
        self.assertEqual(classify_network_connect(
            lambda: (_ for _ in ()).throw(OSError(errno.ECONNREFUSED, "refused"))), 2)
        self.assertEqual(classify_network_connect(lambda: None), 3)

    def test_law_projection_cannot_be_promoted(self):
        fixture = Fixture(); self.addCleanup(fixture.close)
        invalid = held_law_rows(); invalid[0]["status"] = "PASS"; invalid[0]["claim_made"] = True
        with patch.object(backend_module, "held_law_rows", return_value=invalid):
            with self.assertRaisesRegex(IntegrationError, "BACKEND_DECLARED_FAILURE"):
                fixture.adapter().describe(request("describe"))
        self.assertEqual(fixture.box["live_count"], 0)


if __name__ == "__main__":
    unittest.main()
