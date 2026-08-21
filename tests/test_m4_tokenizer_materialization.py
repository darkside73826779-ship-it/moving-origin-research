import copy
import hashlib
import importlib.util
import json
import tempfile
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
