import copy
import hashlib
import importlib.util
import json
import os
import stat
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("m4_tokenizer_materialization", ROOT / "diagnostics/m4_tokenizer_materialization.py")
MATERIALIZER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATERIALIZER)
WRAPPER_SPEC = importlib.util.spec_from_file_location(
    "run_m4_tokenizer_materialization_tests",
    ROOT / "tests/run_m4_tokenizer_materialization_tests.py",
)
WRAPPER = importlib.util.module_from_spec(WRAPPER_SPEC)
WRAPPER_SPEC.loader.exec_module(WRAPPER)


class TokenizerMaterializationTests(unittest.TestCase):
    def _read_result(self, output):
        result = json.loads(output.read_text())
        MATERIALIZER.validate(ROOT / "specs/data/m4_tokenizer_materialization_result_schema_v1.json", result)
        return result

    def _synthetic_materialize(self, tokenizer=None, record_mutator=None, file_bytes=None):
        request = MATERIALIZER.load(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json")
        identity = request["selected_identity"]
        record = {key: identity[key] for key in ("repository_id", "revision", "quantization", "weight", "tokenizer", "tokenizer_config")}
        record.update(immutable=True, status="PASS")
        if record_mutator:
            record_mutator(record)

        class FakeTokenizer:
            chat_template = "synthetic-template"
            eos_token_id = 151645
            vocab_size = 200000
            def __init__(self): self.rendered = {}
            def apply_chat_template(self, *args, **kwargs): return [1, 10, 11, 2]
            def encode(self, value, add_special_tokens=False):
                if value == " x": return [12]
                if value == "Return one JSON object whose answer field is the string A.": return [10, 11]
                return self.rendered[value]
            def decode(self, values, **kwargs):
                key = "synthetic-" + str(len(self.rendered))
                self.rendered[key] = list(values)
                return key
            def convert_tokens_to_ids(self, value): return 151645

        fake = tokenizer or FakeTokenizer()
        module = types.SimpleNamespace(
            AutoTokenizer=types.SimpleNamespace(from_pretrained=lambda *args, **kwargs: fake)
        )
        published = []
        def capture_publish(output, result, schema):
            MATERIALIZER.validate(schema, result)
            published.append(result)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".mor-custody-record-v1.json").write_bytes(MATERIALIZER.canonical(record) + b"\n")
            weight = root / identity["weight"]["name"]
            weight.write_bytes(b"")
            (root / identity["tokenizer"]["name"]).write_bytes(b"synthetic-tokenizer")
            (root / identity["tokenizer_config"]["name"]).write_bytes(b'{"chat_template":"synthetic-template"}')
            output = root / "tokenizer_materialization.json"
            real_lstat = MATERIALIZER.os.lstat
            def selected_lstat(path, *args, **kwargs):
                if Path(path) == weight:
                    return types.SimpleNamespace(st_mode=stat.S_IFREG | stat.S_IRUSR, st_size=identity["weight"]["bytes"])
                return real_lstat(path, *args, **kwargs)
            with mock.patch.object(MATERIALIZER.sys, "orig_argv", ["python3"]), \
                 mock.patch.dict(os.environ, {MATERIALIZER.ENV: str(root)}, clear=True), \
                 mock.patch.dict(MATERIALIZER.sys.modules, {"transformers": module}), \
                 mock.patch.object(MATERIALIZER.os, "lstat", side_effect=selected_lstat), \
                 mock.patch.object(MATERIALIZER, "file_bytes", side_effect=file_bytes or (lambda path, metadata: Path(path).read_bytes())), \
                 mock.patch.object(MATERIALIZER, "publish", side_effect=capture_publish):
                code = MATERIALIZER.materialize(
                    str(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json"),
                    MATERIALIZER.HANDLE,
                    str(output),
                )
            self.assertTrue(published, f"materialize returned {code} without a governed result")
            return code, published[-1]
    def _runtime_negative(self, ordinal):
        cases = json.loads((ROOT / "specs/data/m4_tokenizer_runtime_validation_negative_cases_v1.json").read_text())["cases"]
        expected_rows = json.loads((ROOT / "specs/data/m4_tokenizer_runtime_validation_negative_expected_v1.json").read_text())["rows"]
        case = cases[ordinal]
        mutation = case["mutation"]
        snapshot = [copy.deepcopy(record) for record in WRAPPER.capture_runtime_snapshot(ROOT)]
        operation = mutation["operation"]
        target = mutation["path"]
        if operation == "REMOVE_ORDERED_ENTRY":
            snapshot = [record for record in snapshot if record["path"] != target]
        elif operation == "APPEND_ORDERED_ENTRY":
            snapshot.append({"path": target})
        else:
            record = next(record for record in snapshot if record["path"] == target or record["sidecar_path"] == target)
            sidecar = record["sidecar_path"] == target
            if operation == "REPLACE_ATTRIBUTE":
                record[("sidecar_" if sidecar else "") + mutation["field"]] = mutation["value"]
            elif operation == "REPLACE_LSTAT_KIND":
                record["sidecar_kind" if sidecar else "kind"] = mutation["value"]
            else:
                field = "sidecar_bytes" if sidecar else "bytes"
                data = record[field]
                if operation == "INSERT_BYTES":
                    data = data[:-1] + bytes.fromhex(mutation["before_final_lf_hex"]) + data[-1:]
                elif operation == "PREPEND_BYTES":
                    data = bytes.fromhex(mutation["hex"]) + data
                elif operation == "REMOVE_FINAL_BYTES":
                    suffix = bytes.fromhex(mutation["hex"])
                    self.assertTrue(data.endswith(suffix))
                    data = data[:-len(suffix)]
                elif operation == "REPLACE_BYTES":
                    old = bytes.fromhex(mutation["from_hex"])
                    self.assertEqual(data.count(old), mutation["occurrence"])
                    data = data.replace(old, bytes.fromhex(mutation["to_hex"]), 1)
                elif operation == "REPLACE_UTF8":
                    old = mutation["from_utf8"].encode()
                    self.assertEqual(data.count(old), mutation["occurrence"])
                    data = data.replace(old, mutation["to_utf8"].encode(), 1)
                elif operation == "XOR_BYTE":
                    mutable = bytearray(data)
                    mutable[mutation["offset"]] ^= int(mutation["hex"], 16)
                    data = bytes(mutable)
                else:
                    self.fail(f"unsupported mutation {operation}")
                record[field] = data
        actual = WRAPPER.validate_runtime_snapshot(tuple(snapshot))
        self.assertEqual(actual.pop("failure_code"), "RUNTIME_IDENTITY_MISMATCH")
        self.assertEqual(actual, expected_rows[ordinal])

    def test_runtime_validator_00_missing_path(self): self._runtime_negative(0)
    def test_runtime_validator_01_extra_path(self): self._runtime_negative(1)
    def test_runtime_validator_02_attribute_mismatch(self): self._runtime_negative(2)
    def test_runtime_validator_03_link_path(self): self._runtime_negative(3)
    def test_runtime_validator_04_cr_byte(self): self._runtime_negative(4)
    def test_runtime_validator_05_bom_prefix(self): self._runtime_negative(5)
    def test_runtime_validator_06_terminal_lf_missing(self): self._runtime_negative(6)
    def test_runtime_validator_07_sidecar_grammar(self): self._runtime_negative(7)
    def test_runtime_validator_08_sidecar_basename(self): self._runtime_negative(8)
    def test_runtime_validator_09_digest_mismatch(self): self._runtime_negative(9)

    def test_unavailable_python_launcher_disposition(self):
        fixture = ROOT / "specs/data/m4_tokenizer_runtime_unavailable_interpreter_fixture_v1.json"
        expected = ROOT / "specs/data/m4_tokenizer_runtime_unavailable_interpreter_expected_v1.json"
        contract = json.loads((ROOT / "specs/data/m4_tokenizer_materialization_test_contract_v1.json").read_text())
        negative = contract["negative_cases"][0]
        self.assertEqual(hashlib.sha256(fixture.read_bytes()).hexdigest(), negative["fixture_sha256"])
        self.assertEqual(hashlib.sha256(expected.read_bytes()).hexdigest(), negative["expected_artifact_sha256"])
        values = json.loads(fixture.read_text())["input"]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tokenizer_materialization.json"
            self.assertFalse(output.exists())
            actual = MATERIALIZER.classify_oci_start_disposition(
                values["requested_executable"], values["process_started"],
                values["engine_error_class"], values["custody_lookup_performed"],
            )
            self.assertEqual(MATERIALIZER.canonical(actual), expected.read_bytes()[:-1])
            self.assertFalse(output.exists())

    def test_classifier_domain(self):
        for executable in ("python", "python3"):
            for started in (False, True):
                for error in ("NONE", "EXECUTABLE_NOT_FOUND", "OTHER"):
                    for custody in (False, True):
                        if (executable, started, error, custody) == ("python", False, "EXECUTABLE_NOT_FOUND", False):
                            continue
                        with self.assertRaises(ValueError):
                            MATERIALIZER.classify_oci_start_disposition(executable, started, error, custody)

    def test_canonical_request_and_schema_reachability(self):
        request = MATERIALIZER.load(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json", MATERIALIZER.REQ_SHA)
        self.assertEqual(request["custody_handle"], MATERIALIZER.HANDLE)
        schema = ROOT / "specs/data/m4_tokenizer_materialization_result_schema_v1.json"
        for name in (
            "m4_tokenizer_materialization_synthetic_pass_v1.json",
            "m4_tokenizer_materialization_fail_v1.json",
            "m4_tokenizer_materialization_blocked_v1.json",
        ):
            MATERIALIZER.validate(schema, json.loads((ROOT / "specs/data" / name).read_text()))
        invalid = json.loads((ROOT / "specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json").read_text())
        invalid["arrays"][0]["sha256"] = 7
        with self.assertRaisesRegex(ValueError, "SCHEMA_INVALID"):
            MATERIALIZER.validate(schema, invalid)

    def test_private_numeric_hash_and_extra_rejected(self):
        request = MATERIALIZER.load(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json")
        identity = request["selected_identity"]
        schema = ROOT / "specs/data/m4_tokenizer_private_custody_record_schema_v1.json"
        record = {key: identity[key] for key in ("repository_id", "revision", "quantization", "weight", "tokenizer", "tokenizer_config")}
        record.update(immutable=True, status="PASS")
        MATERIALIZER.validate(schema, record)
        invalid = json.loads(json.dumps(record))
        invalid["tokenizer_config"]["sha256"] = 7
        with self.assertRaisesRegex(ValueError, "SCHEMA_INVALID"):
            MATERIALIZER.validate(schema, invalid)

    def test_atomic_publication_and_safety(self):
        result = json.loads((ROOT / "specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json").read_text())
        schema = ROOT / "specs/data/m4_tokenizer_materialization_result_schema_v1.json"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tokenizer_materialization.json"
            MATERIALIZER.publish(output, result, schema)
            self.assertEqual(output.read_bytes(), MATERIALIZER.canonical(result) + b"\n")
            self.assertEqual(
                Path(str(output) + ".sha256").read_text(),
                hashlib.sha256(output.read_bytes()).hexdigest() + "  " + output.name + "\n",
            )
            result["host"] = "forbidden"
            with self.assertRaisesRegex(ValueError, "LOCAL_ONLY"):
                MATERIALIZER.publish(output, result, schema)

    def test_atomic_interruption_preserves_previous_pair(self):
        result = json.loads((ROOT / "specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json").read_text())
        schema = ROOT / "specs/data/m4_tokenizer_materialization_result_schema_v1.json"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tokenizer_materialization.json"
            MATERIALIZER.publish(output, result, schema)
            previous_json = output.read_bytes()
            previous_sidecar = Path(str(output) + ".sha256").read_bytes()
            real_replace = MATERIALIZER.os.replace
            calls = 0
            def interrupted(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("synthetic interruption")
                return real_replace(source, destination)
            with mock.patch.object(MATERIALIZER.os, "replace", side_effect=interrupted):
                with self.assertRaisesRegex(ValueError, "ATOMIC_PUBLICATION_FAILURE"):
                    MATERIALIZER.publish(output, result, schema)
            self.assertEqual(output.read_bytes(), previous_json)
            self.assertEqual(Path(str(output) + ".sha256").read_bytes(), previous_sidecar)
            self.assertTrue(Path(str(output) + ".incomplete").exists())
            self.assertTrue(Path(str(output) + ".sha256.incomplete").exists())

    def test_atomic_interruption_without_previous_pair_leaves_no_orphan(self):
        result = json.loads((ROOT / "specs/data/m4_tokenizer_materialization_synthetic_pass_v1.json").read_text())
        schema = ROOT / "specs/data/m4_tokenizer_materialization_result_schema_v1.json"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tokenizer_materialization.json"
            real_replace = MATERIALIZER.os.replace
            calls = 0
            def interrupted(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("synthetic interruption")
                return real_replace(source, destination)
            with mock.patch.object(MATERIALIZER.os, "replace", side_effect=interrupted):
                with self.assertRaisesRegex(ValueError, "ATOMIC_PUBLICATION_FAILURE"):
                    MATERIALIZER.publish(output, result, schema)
            self.assertFalse(output.exists())
            self.assertFalse(Path(str(output) + ".sha256").exists())
            self.assertTrue(Path(str(output) + ".incomplete").exists())
            self.assertTrue(Path(str(output) + ".sha256.incomplete").exists())

    def test_materialize_publishes_governed_blocked_results(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tokenizer_materialization.json"
            with mock.patch.object(MATERIALIZER.sys, "orig_argv", ["not-python3"]):
                code = MATERIALIZER.materialize(
                    str(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json"),
                    MATERIALIZER.HANDLE,
                    str(output),
                )
            self.assertEqual(code, 2)
            result = self._read_result(output)
            self.assertEqual((result["status"], result["failure_code"]), ("BLOCKED", "AUTHORITY_MISSING"))
            self.assertEqual(result["checks"], [{"check_id": "AUTHORITY", "ordinal": 0, "status": "FAIL"}])

            output.unlink(); Path(str(output) + ".sha256").unlink()
            with mock.patch.object(MATERIALIZER.sys, "orig_argv", ["python3"]), mock.patch.dict(os.environ, {}, clear=True):
                code = MATERIALIZER.materialize(
                    str(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json"),
                    MATERIALIZER.HANDLE,
                    str(output),
                )
            self.assertEqual(code, 2)
            result = self._read_result(output)
            self.assertEqual((result["status"], result["failure_code"]), ("BLOCKED", "CUSTODY_HANDLE_UNRESOLVED"))
            self.assertEqual([row["status"] for row in result["checks"]], ["PASS", "FAIL"])

    def test_constructor_digest_is_checked_before_environment_lookup(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tokenizer_materialization.json"
            real_sha = MATERIALIZER.sha
            constructor_bytes = (ROOT / "specs/data/m4_context_format_probe_contract_v1.json").read_bytes()
            def changed_constructor(data):
                return "0" * 64 if data == constructor_bytes else real_sha(data)
            with mock.patch.object(MATERIALIZER.sys, "orig_argv", ["python3"]), \
                 mock.patch.object(MATERIALIZER, "sha", side_effect=changed_constructor), \
                 mock.patch.dict(os.environ, {}, clear=True):
                code = MATERIALIZER.materialize(
                    str(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json"),
                    MATERIALIZER.HANDLE,
                    str(output),
                )
            self.assertEqual(code, 3)
            result = self._read_result(output)
            self.assertEqual((result["status"], result["failure_code"]), ("FAIL", "CONSTRUCTOR_IDENTITY_MISMATCH"))
            self.assertEqual(result["checks"][-1], {"check_id": "CONSTRUCTOR_IDENTITY", "ordinal": 5, "status": "FAIL"})

    def test_materialize_invalid_requests_publish_governed_blocked_result(self):
        canonical = (ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json").read_bytes()
        cases = {
            "missing": None,
            "digest": canonical.replace(b'"regime":"B"', b'"regime":"A"'),
            "duplicate": b'{"date":"2026-08-21","date":"2026-08-21"}\n',
            "noncanonical": b'{ "date": "2026-08-21" }\n',
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, payload in cases.items():
                with self.subTest(name=name):
                    contract = root / f"{name}.json"
                    if payload is not None:
                        contract.write_bytes(payload)
                    output = root / f"{name}-result.json"
                    code = MATERIALIZER.materialize(str(contract), MATERIALIZER.HANDLE, str(output))
                    self.assertEqual(code, 2)
                    result = self._read_result(output)
                    self.assertEqual((result["status"], result["failure_code"]), ("BLOCKED", "AUTHORITY_MISSING"))
                    self.assertEqual(result["checks"], [{"check_id": "AUTHORITY", "ordinal": 0, "status": "FAIL"}])

    def test_failure_projection_covers_every_governed_code(self):
        request = MATERIALIZER.load(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json")
        cases = [
            ("AUTHORITY", "AUTHORITY_MISSING", True),
            ("CUSTODY_HANDLE", "CUSTODY_HANDLE_UNRESOLVED", True),
            ("CUSTODY_ATTESTATION", "CUSTODY_ATTESTATION_INVALID", False),
            ("CUSTODY_ATTESTATION", "CHECKPOINT_IDENTITY_MISMATCH", False),
            ("TOKENIZER_ORIGINAL", "TOKENIZER_IDENTITY_MISMATCH", False),
            ("TOKENIZER_ORIGINAL", "TOKENIZER_CONFIG_IDENTITY_MISMATCH", False),
            ("INSERTION_UNIQUENESS", "CONSTRUCTOR_INVARIANT_FAILURE", False),
            ("ENCODE_DECODE_1024", "ENCODE_DECODE_IDENTITY_FAILURE", False),
            ("STOP_ARRAY", "STOP_ARRAY_MISMATCH", False),
            ("PUBLIC_SAFETY", "SERIALIZATION_MISMATCH", False),
            ("PUBLIC_SAFETY", "LOCAL_ONLY_CUSTODY_VIOLATION", False),
            ("PUBLIC_SAFETY", "INTERNAL_ERROR", False),
        ]
        schema = ROOT / "specs/data/m4_tokenizer_materialization_result_schema_v1.json"
        for check, code, blocked in cases:
            with self.subTest(code=code):
                result = MATERIALIZER.failure_result(request, check, code, blocked)
                MATERIALIZER.validate(schema, result)
                self.assertEqual(result["failure_code"], code)
                self.assertEqual(result["checks"][-1]["status"], "FAIL")
                self.assertNotIn("NOT_RUN", [row["status"] for row in result["checks"]])

    def test_weight_identity_uses_one_lstat_observation(self):
        request = MATERIALIZER.load(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json")
        identity = request["selected_identity"]
        record = {key: identity[key] for key in ("repository_id", "revision", "quantization", "weight", "tokenizer", "tokenizer_config")}
        record.update(immutable=True, status="PASS")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".mor-custody-record-v1.json").write_bytes(MATERIALIZER.canonical(record) + b"\n")
            weight = root / identity["weight"]["name"]
            weight.write_bytes(b"")
            output = root / "result.json"
            fake_stat = types.SimpleNamespace(st_mode=stat.S_IFREG | stat.S_IRUSR, st_size=identity["weight"]["bytes"])
            with mock.patch.object(MATERIALIZER.sys, "orig_argv", ["python3"]), \
                 mock.patch.dict(os.environ, {MATERIALIZER.ENV: str(root)}, clear=True), \
                 mock.patch.object(MATERIALIZER.os, "lstat", return_value=fake_stat) as observed:
                code = MATERIALIZER.materialize(
                    str(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json"),
                    MATERIALIZER.HANDLE,
                    str(output),
                )
            self.assertEqual(code, 3)
            self.assertEqual([call for call in observed.call_args_list if call.args == (weight,)], [mock.call(weight)])
            self.assertEqual(self._read_result(output)["failure_code"], "TOKENIZER_IDENTITY_MISMATCH")

    def test_materialize_synthetic_positive_reaches_pass(self):
        code, result = self._synthetic_materialize()
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(result["arrays"]), 3)
        self.assertEqual(len(result["checks"]), len(MATERIALIZER.CHECKS))

    def test_materialize_identity_negative_matrix(self):
        cases = [
            ("repository_id", "CHECKPOINT_IDENTITY_MISMATCH"),
            ("revision", "CHECKPOINT_IDENTITY_MISMATCH"),
            ("quantization", "CHECKPOINT_IDENTITY_MISMATCH"),
            ("weight", "CHECKPOINT_IDENTITY_MISMATCH"),
            ("tokenizer", "TOKENIZER_IDENTITY_MISMATCH"),
            ("tokenizer_config", "TOKENIZER_CONFIG_IDENTITY_MISMATCH"),
        ]
        for field, expected in cases:
            with self.subTest(field=field):
                def mutate(record, field=field):
                    if isinstance(record[field], dict):
                        record[field][next(iter(record[field]))] = "wrong"
                    else:
                        record[field] = "wrong"
                code, result = self._synthetic_materialize(record_mutator=mutate)
                self.assertEqual((code, result["failure_code"]), (3, expected))

        for filename, expected in (("tokenizer.json", "TOKENIZER_IDENTITY_MISMATCH"),
                                   ("tokenizer_config.json", "TOKENIZER_CONFIG_IDENTITY_MISMATCH")):
            with self.subTest(file=filename):
                def reject(path, metadata, filename=filename):
                    if Path(path).name == filename:
                        raise ValueError("IDENTITY_MISMATCH")
                    return Path(path).read_bytes()
                code, result = self._synthetic_materialize(file_bytes=reject)
                self.assertEqual((code, result["failure_code"]), (3, expected))

    def test_materialize_custody_attestation_negative_matrix(self):
        request = MATERIALIZER.load(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json")
        identity = request["selected_identity"]
        valid = {key: identity[key] for key in
                 ("repository_id", "revision", "quantization", "weight", "tokenizer", "tokenizer_config")}
        valid.update(immutable=True, status="PASS")
        extra = copy.deepcopy(valid); extra["unexpected"] = True
        stale = copy.deepcopy(valid); stale["status"] = "STALE"
        numeric = copy.deepcopy(valid); numeric["immutable"] = "yes"
        cases = {
            "absent": None,
            "noncanonical": json.dumps(valid, indent=2).encode() + b"\n",
            "duplicate": b'{"status":"PASS","status":"PASS"}\n',
            "extra": MATERIALIZER.canonical(extra) + b"\n",
            "stale": MATERIALIZER.canonical(stale) + b"\n",
            "schema_invalid": MATERIALIZER.canonical(numeric) + b"\n",
        }
        for name, payload in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                if payload is not None:
                    (root / ".mor-custody-record-v1.json").write_bytes(payload)
                output = root / "result.json"
                with mock.patch.object(MATERIALIZER.sys, "orig_argv", ["python3"]), \
                     mock.patch.dict(os.environ, {MATERIALIZER.ENV: str(root)}, clear=True):
                    code = MATERIALIZER.materialize(
                        str(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json"),
                        MATERIALIZER.HANDLE, str(output))
                self.assertEqual((code, self._read_result(output)["failure_code"]),
                                 (3, "CUSTODY_ATTESTATION_INVALID"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "record-target.json"
            target.write_bytes(MATERIALIZER.canonical(valid) + b"\n")
            (root / ".mor-custody-record-v1.json").symlink_to(target)
            output = root / "result.json"
            with mock.patch.object(MATERIALIZER.sys, "orig_argv", ["python3"]), \
                 mock.patch.dict(os.environ, {MATERIALIZER.ENV: str(root)}, clear=True):
                code = MATERIALIZER.materialize(
                    str(ROOT / "specs/data/m4_tokenizer_materialization_request_v1.json"),
                    MATERIALIZER.HANDLE, str(output))
            self.assertEqual((code, self._read_result(output)["failure_code"]),
                             (3, "CUSTODY_ATTESTATION_INVALID"))

    def test_materialize_constructor_negative_matrix(self):
        class ConfigurableTokenizer:
            eos_token_id = 151645
            vocab_size = 200000
            def __init__(self, chat_template="synthetic-template", neutral=(12,), mismatch=None, stops=151645):
                self.chat_template = chat_template
                self.neutral = list(neutral)
                self.mismatch = mismatch
                self.stop = stops
                self.rendered = {}
            def apply_chat_template(self, *args, **kwargs): return [1, 10, 11, 2]
            def encode(self, value, add_special_tokens=False):
                if value == " x": return self.neutral
                if value.startswith("Return one"): return [10, 11]
                values = list(self.rendered[value])
                if self.mismatch is not None and len(values) == self.mismatch:
                    values[-1] += 1
                return values
            def decode(self, values, **kwargs):
                key = "rendered-" + str(len(values)); self.rendered[key] = list(values); return key
            def convert_tokens_to_ids(self, value): return self.stop

        for value in (None, 7, "unequal"):
            with self.subTest(chat_template=value):
                code, result = self._synthetic_materialize(ConfigurableTokenizer(chat_template=value))
                self.assertEqual((code, result["failure_code"]), (3, "TOKENIZER_CONFIG_IDENTITY_MISMATCH"))
        code, result = self._synthetic_materialize(ConfigurableTokenizer(neutral=(12, 13)))
        self.assertEqual((code, result["failure_code"]), (3, "CONSTRUCTOR_INVARIANT_FAILURE"))
        for length, check in ((992, "ENCODE_DECODE_1024"), (4064, "ENCODE_DECODE_4096"), (8160, "ENCODE_DECODE_8192")):
            with self.subTest(check=check):
                code, result = self._synthetic_materialize(ConfigurableTokenizer(mismatch=length))
                self.assertEqual((code, result["failure_code"], result["checks"][-1]["check_id"]),
                                 (3, "ENCODE_DECODE_IDENTITY_FAILURE", check))
        for eos, im_end in ((151644, 151645), (151645, 151646), (151646, 151645)):
            with self.subTest(eos=eos, im_end=im_end):
                tokenizer = ConfigurableTokenizer(stops=im_end)
                tokenizer.eos_token_id = eos
                code, result = self._synthetic_materialize(tokenizer)
                self.assertEqual((code, result["failure_code"]), (3, "STOP_ARRAY_MISMATCH"))

    def test_materialize_synthetic_constructor_and_stop_failures(self):
        class NonUnique:
            chat_template = "synthetic-template"; eos_token_id = 151645; vocab_size = 200000
            def apply_chat_template(self, *args, **kwargs): return [10, 11, 10, 11]
            def encode(self, value, add_special_tokens=False): return [12] if value == " x" else [10, 11]
            def convert_tokens_to_ids(self, value): return 151645
        code, result = self._synthetic_materialize(NonUnique())
        self.assertEqual((code, result["failure_code"]), (3, "CONSTRUCTOR_INVARIANT_FAILURE"))

        class BadStop:
            chat_template = "synthetic-template"; eos_token_id = 151644; vocab_size = 200000
            def __init__(self): self.rendered = {}
            def apply_chat_template(self, *args, **kwargs): return [1, 10, 11, 2]
            def encode(self, value, add_special_tokens=False):
                if value == " x": return [12]
                if value.startswith("Return one"): return [10, 11]
                return self.rendered[value]
            def decode(self, values, **kwargs):
                key = "rendered" + str(len(self.rendered)); self.rendered[key] = list(values); return key
            def convert_tokens_to_ids(self, value): return 151645
        code, result = self._synthetic_materialize(BadStop())
        self.assertEqual((code, result["failure_code"]), (3, "STOP_ARRAY_MISMATCH"))

    def test_constructor_contract_is_present_and_exact(self):
        constructor = ROOT / "specs/data/m4_context_format_probe_contract_v1.json"
        self.assertEqual(hashlib.sha256(constructor.read_bytes()).hexdigest(), MATERIALIZER.CONSTRUCTOR)
        self.assertEqual(
            (constructor.with_suffix(constructor.suffix + ".sha256")).read_text(),
            MATERIALIZER.CONSTRUCTOR + "  " + constructor.name + "\n",
        )

    def test_oci_launch_contract_is_fail_closed(self):
        contract_path = ROOT / "specs/data/m4_tokenizer_oci_launch_contract_v1.json"
        contract = MATERIALIZER.load(contract_path)
        test_tokens = contract["test_launch"]["command_tokens"]
        materializer_tokens = contract["materialization_launch"]["command_tokens"]
        for tokens in (test_tokens, materializer_tokens):
            self.assertIn("--pull=never", tokens)
            self.assertEqual(tokens[tokens.index("--network") + 1], "none")
            self.assertEqual(tokens[tokens.index("--platform") + 1], "linux/amd64")
            self.assertEqual(tokens[tokens.index("--entrypoint") + 1], "python3")
            self.assertIn(contract["image"]["reference"], tokens)
        self.assertNotIn("MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1=/run/mor-custody", test_tokens)
        self.assertIn("MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1=/run/mor-custody", materializer_tokens)
        self.assertFalse(contract["materialization_launch"]["retry"])

    def test_strict_json_rejects_duplicate_and_noncanonical_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            duplicate = Path(directory) / "duplicate.json"
            duplicate.write_bytes(b'{"a":1,"a":2}\n')
            with self.assertRaisesRegex(ValueError, "duplicate"):
                MATERIALIZER.load(duplicate)
            noncanonical = Path(directory) / "noncanonical.json"
            noncanonical.write_bytes(b'{"b": 2, "a": 1}\n')
            with self.assertRaisesRegex(ValueError, "SERIALIZATION_MISMATCH"):
                MATERIALIZER.load(noncanonical)


if __name__ == "__main__":
    unittest.main()
