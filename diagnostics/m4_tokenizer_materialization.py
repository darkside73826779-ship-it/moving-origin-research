#!/usr/bin/env python3
"""M4 bounded tokenizer materializer; emits sanitized digests, never token data."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

REQ_SHA = "b39061fd4b19321d58dd418eb5ecd486c0cf26662d70a5d0de4185c6dd7e9992"
INDEX = "sha256:607442e407b0fea97f8a132a78b787c121a996dd4de181fa08e8da06e71ec2db"
PLATFORM = "sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6"
HANDLE = "M4_QWEN3_4B_FP8_PRESERVED_V1"
ENV = "MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1"
CONSTRUCTOR = "eab77b9f44a4e9378f5889f5aa368eabd87959a5ddafab9ca38685228f12feec"
STOP = "580af853441f1d705732a492fe363f022bdd177c37d2b8f82035cbdf9a604b8c"
TRANSFORMERS_VERSION = "4.56.1"
AUTO_TOKENIZER_BYTES = 56944
AUTO_TOKENIZER_SHA256 = "b0cd25702a99bfdf1cd93edcb1f3793a7d422ed5b4f053d4a9e71cf678b79fa0"
AUTO_TOKENIZER_PATH = "transformers/models/auto/tokenization_auto.py"
CHECKS = [
    "AUTHORITY", "CUSTODY_HANDLE", "CUSTODY_ATTESTATION", "TOKENIZER_ORIGINAL",
    "TOKENIZER_COPY", "CONSTRUCTOR_IDENTITY", "BASE_TEMPLATE", "INSERTION_UNIQUENESS",
    "NEUTRAL_FRAGMENT", "ARRAY_1024", "ARRAY_4096", "ARRAY_8192",
    "ENCODE_DECODE_1024", "ENCODE_DECODE_4096", "ENCODE_DECODE_8192",
    "STOP_ARRAY", "PUBLIC_SAFETY", "ATOMIC_PUBLICATION",
]


class GovernedFailure(Exception):
    def __init__(self, check: str, code: str, blocked: bool = False):
        super().__init__(code)
        self.check = check
        self.code = code
        self.blocked = blocked


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate member")
        result[key] = value
    return result


def load(path: str | Path, expected: str | None = None) -> object:
    raw = Path(path).read_bytes()
    if expected and sha(raw) != expected:
        raise ValueError("IDENTITY_MISMATCH")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    if not raw.endswith(b"\n") or raw != canonical(value) + b"\n":
        raise ValueError("SERIALIZATION_MISMATCH")
    return value


def validate(schema_path: str | Path, value: object) -> None:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    if next(Draft202012Validator(schema).iter_errors(value), None):
        raise ValueError("SCHEMA_INVALID")


def classify_oci_start_disposition(
    requested_executable: str,
    process_started: bool,
    engine_error_class: str,
    custody_lookup_performed: bool,
) -> dict[str, object]:
    if (
        requested_executable not in {"python", "python3"}
        or type(process_started) is not bool
        or engine_error_class not in {"NONE", "EXECUTABLE_NOT_FOUND", "OTHER"}
        or type(custody_lookup_performed) is not bool
    ):
        raise ValueError("invalid launcher disposition input")
    if custody_lookup_performed and not process_started:
        raise ValueError("custody cannot precede process start")
    if (requested_executable, process_started, engine_error_class, custody_lookup_performed) == (
        "python", False, "EXECUTABLE_NOT_FOUND", False
    ):
        return {
            "custody_lookup_performed": False,
            "date": "2026-08-21",
            "failure_code": "RUNTIME_IDENTITY_MISMATCH",
            "outcome": "PROCESS_NOT_STARTED",
            "phase": "OCI_PROCESS_CREATION",
            "project_result_artifact_expected": False,
            "regime": "B",
            "requested_executable": "python",
            "schema_version": "m4-tokenizer-runtime-launcher-disposition-v1",
        }
    raise ValueError("tuple outside governed negative")


def file_bytes(path: str | Path, metadata: dict[str, object]) -> bytes:
    candidate = Path(path)
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError("IDENTITY_MISMATCH")
    data = candidate.read_bytes()
    if len(data) != metadata["bytes"] or sha(data) != metadata["sha256"]:
        raise ValueError("IDENTITY_MISMATCH")
    return data


def base_result(request: dict[str, object]) -> dict[str, object]:
    identity = request["selected_identity"]
    config = identity["tokenizer_config"]
    return {
        "arrays": [], "checks": [], "constructor_sha256": CONSTRUCTOR,
        "custody_handle": HANDLE, "date": "2026-08-21",
        "digest_domain": "RFC8785_JSON_INTEGER_ARRAY_UTF8_NO_LF", "failure_code": None,
        "regime": "B", "repository_id": identity["repository_id"], "revision": identity["revision"],
        "runtime_image_index_digest": INDEX, "runtime_image_platform_digest": PLATFORM,
        "schema_version": "m4-tokenizer-materialization-result-v1", "status": "PASS",
        "stop_array_length": 0, "stop_array_sha256": None,
        "tokenizer_sha256": identity["tokenizer"]["sha256"],
        "tokenizer_config_git_blob_sha1": config["git_blob_sha1"],
        "tokenizer_config_bytes": config["bytes"], "tokenizer_config_name": config["name"],
        "tokenizer_config_sha256": config["sha256"], "weight_sha256": identity["weight"]["sha256"],
    }


def failure_result(request: dict[str, object], check: str, code: str, blocked: bool = False) -> dict[str, object]:
    ordinal = CHECKS.index(check)
    result = base_result(request)
    result.update(
        arrays=[],
        checks=[
            {"check_id": value, "ordinal": index, "status": "FAIL" if index == ordinal else "PASS"}
            for index, value in enumerate(CHECKS[:ordinal + 1])
        ],
        failure_code=code,
        status="BLOCKED" if blocked else "FAIL",
        stop_array_length=0,
        stop_array_sha256=None,
    )
    return result


def require(condition: bool, check: str, code: str, blocked: bool = False) -> None:
    if not condition:
        raise GovernedFailure(check, code, blocked)


def runtime_file_bytes(path: str | Path) -> bytes:
    return Path(path).read_bytes()


def verify_runtime_loading_identity() -> None:
    try:
        distribution = importlib.metadata.distribution("transformers")
        require(distribution.version == TRANSFORMERS_VERSION,
                "AUTHORITY", "RUNTIME_IDENTITY_MISMATCH")
        matches = [path for path in distribution.files or () if str(path).replace("\\", "/") == AUTO_TOKENIZER_PATH]
        require(len(matches) == 1, "AUTHORITY", "RUNTIME_IDENTITY_MISMATCH")
        loader_path = Path(distribution.locate_file(matches[0]))
        loader_lstat = os.lstat(loader_path)
        require(stat.S_ISREG(loader_lstat.st_mode) and loader_lstat.st_size == AUTO_TOKENIZER_BYTES,
                "AUTHORITY", "RUNTIME_IDENTITY_MISMATCH")
        require(sha(runtime_file_bytes(loader_path)) == AUTO_TOKENIZER_SHA256,
                "AUTHORITY", "RUNTIME_IDENTITY_MISMATCH")
    except GovernedFailure:
        raise
    except Exception as error:
        raise GovernedFailure("AUTHORITY", "RUNTIME_IDENTITY_MISMATCH") from error


def _keys(value: object):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _keys(child)


def publish(output: str | Path, result: dict[str, object], schema: str | Path) -> None:
    if any(key.lower() in {"path", "host", "hostname", "text", "token_ids", "tokens"} for key in _keys(result)):
        raise ValueError("LOCAL_ONLY_CUSTODY_VIOLATION")
    validate(schema, result)
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(result) + b"\n"
    sidecar = (sha(payload) + "  " + destination.name + "\n").encode("ascii")
    incomplete_json = Path(str(destination) + ".incomplete")
    incomplete_sidecar = Path(str(destination) + ".sha256.incomplete")
    final_sidecar = Path(str(destination) + ".sha256")
    previous = None
    if destination.exists() or final_sidecar.exists():
        if not destination.is_file() or not final_sidecar.is_file():
            raise ValueError("ATOMIC_PUBLICATION_FAILURE")
        previous = (destination.read_bytes(), final_sidecar.read_bytes())
    for path, data in ((incomplete_json, payload), (incomplete_sidecar, sidecar)):
        with path.open("wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    try:
        os.replace(incomplete_json, destination)
        os.replace(incomplete_sidecar, final_sidecar)
    except OSError as error:
        # Recover the newly staged JSON so failure evidence remains incomplete-only.
        if destination.exists() and not incomplete_json.exists():
            os.replace(destination, incomplete_json)
        if previous is not None:
            restore_json = Path(str(destination) + ".restore")
            restore_sidecar = Path(str(destination) + ".sha256.restore")
            restore_json.write_bytes(previous[0])
            restore_sidecar.write_bytes(previous[1])
            os.replace(restore_json, destination)
            os.replace(restore_sidecar, final_sidecar)
        raise ValueError("ATOMIC_PUBLICATION_FAILURE") from error


def materialize(contract_path: str, custody_handle: str, output_path: str) -> int:
    repository = Path.cwd()
    schema = repository / "specs/data/m4_tokenizer_materialization_result_schema_v1.json"
    authority_request_path = repository / "specs/data/m4_tokenizer_materialization_request_v1.json"
    # The committed authority request supplies only public identity fields for a
    # governed projection when the routed request cannot itself be trusted.
    authority_request = load(authority_request_path, REQ_SHA)
    request: dict[str, object] = authority_request
    try:
        try:
            request = load(contract_path, REQ_SHA)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
            raise GovernedFailure("AUTHORITY", "AUTHORITY_MISSING", True) from error
        require(Path(sys.orig_argv[0]).name == "python3" and custody_handle == HANDLE,
                "AUTHORITY", "AUTHORITY_MISSING", True)
        constructor_path = repository / "specs/data/m4_context_format_probe_contract_v1.json"
        require(request["constructor"]["artifact_sha256"] == CONSTRUCTOR
                and sha(constructor_path.read_bytes()) == CONSTRUCTOR,
                "CONSTRUCTOR_IDENTITY", "CONSTRUCTOR_IDENTITY_MISMATCH")
        verify_runtime_loading_identity()
        raw_root = os.environ.get(ENV)
        require(bool(raw_root) and not any(character in raw_root for character in "\0\r\n"),
                "CUSTODY_HANDLE", "CUSTODY_HANDLE_UNRESOLVED", True)
        literal_root = Path(raw_root)
        require(not literal_root.is_symlink(), "CUSTODY_HANDLE", "CUSTODY_HANDLE_UNRESOLVED", True)
        try:
            root = literal_root.resolve(strict=True)
        except OSError as error:
            raise GovernedFailure("CUSTODY_HANDLE", "CUSTODY_HANDLE_UNRESOLVED", True) from error
        require(root.is_dir(), "CUSTODY_HANDLE", "CUSTODY_HANDLE_UNRESOLVED", True)
        record_path = root / ".mor-custody-record-v1.json"
        require(not record_path.is_symlink() and record_path.is_file(),
                "CUSTODY_ATTESTATION", "CUSTODY_ATTESTATION_INVALID")
        try:
            record = load(record_path)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
            raise GovernedFailure("CUSTODY_ATTESTATION", "CUSTODY_ATTESTATION_INVALID") from error
        identity = request["selected_identity"]
        try:
            require(not any(record[key] != identity[key] for key in
                            ("repository_id", "revision", "quantization", "weight")),
                    "CUSTODY_ATTESTATION", "CHECKPOINT_IDENTITY_MISMATCH")
            require(record["tokenizer"] == identity["tokenizer"],
                    "CUSTODY_ATTESTATION", "TOKENIZER_IDENTITY_MISMATCH")
            require(record["tokenizer_config"] == identity["tokenizer_config"],
                    "CUSTODY_ATTESTATION", "TOKENIZER_CONFIG_IDENTITY_MISMATCH")
            validate(repository / "specs/data/m4_tokenizer_private_custody_record_schema_v1.json", record)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
            raise GovernedFailure("CUSTODY_ATTESTATION", "CUSTODY_ATTESTATION_INVALID") from error
        weight_path = root / identity["weight"]["name"]
        try:
            weight_lstat = os.lstat(weight_path)
        except OSError as error:
            raise GovernedFailure("TOKENIZER_ORIGINAL", "CHECKPOINT_IDENTITY_MISMATCH") from error
        require(stat.S_ISREG(weight_lstat.st_mode) and weight_lstat.st_size == identity["weight"]["bytes"],
                "TOKENIZER_ORIGINAL", "CHECKPOINT_IDENTITY_MISMATCH")
        tokenizer_path = root / identity["tokenizer"]["name"]
        config_path = root / identity["tokenizer_config"]["name"]
        try:
            tokenizer_bytes = file_bytes(tokenizer_path, identity["tokenizer"])
        except (OSError, ValueError) as error:
            raise GovernedFailure("TOKENIZER_ORIGINAL", "TOKENIZER_IDENTITY_MISMATCH") from error
        try:
            config_bytes = file_bytes(config_path, identity["tokenizer_config"])
        except (OSError, ValueError) as error:
            raise GovernedFailure("TOKENIZER_ORIGINAL", "TOKENIZER_CONFIG_IDENTITY_MISMATCH") from error
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            tokenizer_copy = temporary / "tokenizer.json"
            config_copy = temporary / "tokenizer_config.json"
            shutil.copyfile(tokenizer_path, tokenizer_copy)
            shutil.copyfile(config_path, config_copy)
            tokenizer_copy.chmod(stat.S_IRUSR)
            config_copy.chmod(stat.S_IRUSR)
            try:
                file_bytes(tokenizer_copy, identity["tokenizer"])
                file_bytes(config_copy, identity["tokenizer_config"])
            except (OSError, ValueError) as error:
                raise GovernedFailure("TOKENIZER_COPY", "TOKENIZER_IDENTITY_MISMATCH") from error
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                str(temporary), local_files_only=True, trust_remote_code=False, use_fast=True
            )
            config = json.loads(config_bytes.decode("utf-8"), object_pairs_hook=unique)
            require(isinstance(config.get("chat_template"), str) and tokenizer.chat_template == config["chat_template"],
                    "BASE_TEMPLATE", "TOKENIZER_CONFIG_IDENTITY_MISMATCH")
            user_text = "Return one JSON object whose answer field is the string A."
            messages = [{"role": "user", "content": user_text}]
            base = tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                continue_final_message=False, enable_thinking=False,
            )
            neutral = tokenizer.encode(" x", add_special_tokens=False)
            user = tokenizer.encode(user_text, add_special_tokens=False)
            occurrences = [index for index in range(len(base) - len(user) + 1) if base[index:index + len(user)] == user]
            require(len(occurrences) == 1, "INSERTION_UNIQUENESS", "CONSTRUCTOR_INVARIANT_FAILURE")
            require(len(neutral) == 1, "NEUTRAL_FRAGMENT", "CONSTRUCTOR_INVARIANT_FAILURE")
            insertion = occurrences[0]
            rows = []
            for target in request["targets"]:
                prompt_length = target["prompt_length"]
                check = CHECKS[9 + target["ordinal"]]
                require(prompt_length >= len(base), check, "CONSTRUCTOR_INVARIANT_FAILURE")
                values = base[:insertion] + [neutral[0]] * (prompt_length - len(base)) + base[insertion:]
                require(len(values) == prompt_length and not any(
                    type(item) is not int or item < 0 or item >= tokenizer.vocab_size for item in values
                ), check, "CONSTRUCTOR_INVARIANT_FAILURE")
                rendered = tokenizer.decode(values, skip_special_tokens=False, clean_up_tokenization_spaces=False)
                require(tokenizer.encode(rendered, add_special_tokens=False) == values,
                        CHECKS[12 + target["ordinal"]], "ENCODE_DECODE_IDENTITY_FAILURE")
                try:
                    array_sha256 = sha(canonical(values))
                except (TypeError, ValueError) as error:
                    raise GovernedFailure("PUBLIC_SAFETY", "SERIALIZATION_MISMATCH") from error
                rows.append({
                    "array_id": target["array_id"], "decode_reencode_equal": True,
                    "ordinal": target["ordinal"], "prompt_length": prompt_length,
                    "sha256": array_sha256,
                })
            im_end = tokenizer.convert_tokens_to_ids("<|im_end|>")
            stops = list(dict.fromkeys([tokenizer.eos_token_id, im_end]))
            require(stops == [151645] and sha(canonical(stops)) == STOP,
                    "STOP_ARRAY", "STOP_ARRAY_MISMATCH")
            require(tokenizer_path.read_bytes() == tokenizer_bytes and config_path.read_bytes() == config_bytes,
                    "PUBLIC_SAFETY", "TOKENIZER_IDENTITY_MISMATCH")
            try:
                file_bytes(tokenizer_copy, identity["tokenizer"])
                file_bytes(config_copy, identity["tokenizer_config"])
            except (OSError, ValueError) as error:
                raise GovernedFailure("PUBLIC_SAFETY", "TOKENIZER_IDENTITY_MISMATCH") from error
        result = base_result(request)
        result.update(
            arrays=rows,
            checks=[{"check_id": value, "ordinal": index, "status": "PASS"} for index, value in enumerate(CHECKS)],
            stop_array_length=1,
            stop_array_sha256=STOP,
        )
        try:
            publish(output_path, result, schema)
        except ValueError as error:
            if str(error) == "ATOMIC_PUBLICATION_FAILURE":
                return 3
            if str(error) == "LOCAL_ONLY_CUSTODY_VIOLATION":
                raise GovernedFailure("PUBLIC_SAFETY", "LOCAL_ONLY_CUSTODY_VIOLATION") from error
            raise
        return 0
    except GovernedFailure as failure:
        try:
            publish(output_path, failure_result(request, failure.check, failure.code, failure.blocked), schema)
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            return 3
        return 2 if failure.blocked else 3
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        try:
            publish(output_path, failure_result(request, "PUBLIC_SAFETY", "INTERNAL_ERROR"), schema)
        except Exception:
            pass
        return 3
    except Exception:
        try:
            publish(output_path, failure_result(request, "PUBLIC_SAFETY", "INTERNAL_ERROR"), schema)
        except Exception:
            pass
        return 4


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--custody-handle", required=True)
    parser.add_argument("--output", required=True)
    arguments = parser.parse_args()
    return materialize(arguments.contract, arguments.custody_handle, arguments.output)


if __name__ == "__main__":
    raise SystemExit(main())
