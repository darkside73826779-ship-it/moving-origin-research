#!/usr/bin/env python3
"""M4 bounded tokenizer materializer; emits sanitized digests, never token data."""
from __future__ import annotations

import argparse
import hashlib
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
CHECKS = [
    "AUTHORITY", "CUSTODY_HANDLE", "CUSTODY_ATTESTATION", "TOKENIZER_ORIGINAL",
    "TOKENIZER_COPY", "CONSTRUCTOR_IDENTITY", "BASE_TEMPLATE", "INSERTION_UNIQUENESS",
    "NEUTRAL_FRAGMENT", "ARRAY_1024", "ARRAY_4096", "ARRAY_8192",
    "ENCODE_DECODE_1024", "ENCODE_DECODE_4096", "ENCODE_DECODE_8192",
    "STOP_ARRAY", "PUBLIC_SAFETY", "ATOMIC_PUBLICATION",
]


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
        if previous is not None:
            destination.write_bytes(previous[0])
            final_sidecar.write_bytes(previous[1])
        raise ValueError("ATOMIC_PUBLICATION_FAILURE") from error


def materialize(contract_path: str, custody_handle: str, output_path: str) -> int:
    try:
        if Path(sys.orig_argv[0]).name != "python3" or custody_handle != HANDLE:
            return 2
        request = load(contract_path, REQ_SHA)
        if request["constructor"]["artifact_sha256"] != CONSTRUCTOR:
            return 3
        raw_root = os.environ.get(ENV)
        if not raw_root or any(character in raw_root for character in "\0\r\n"):
            return 2
        literal_root = Path(raw_root)
        if literal_root.is_symlink():
            return 2
        root = literal_root.resolve(strict=True)
        if not root.is_dir():
            return 2
        record_path = root / ".mor-custody-record-v1.json"
        if record_path.is_symlink() or not record_path.is_file():
            return 2
        record = load(record_path)
        repository = Path.cwd()
        validate(repository / "specs/data/m4_tokenizer_private_custody_record_schema_v1.json", record)
        identity = request["selected_identity"]
        if any(record[key] != identity[key] for key in ("repository_id", "revision", "quantization", "weight", "tokenizer", "tokenizer_config")):
            return 3
        weight_path = root / identity["weight"]["name"]
        if weight_path.is_symlink() or not weight_path.is_file() or weight_path.stat().st_size != identity["weight"]["bytes"]:
            return 3
        tokenizer_path = root / identity["tokenizer"]["name"]
        config_path = root / identity["tokenizer_config"]["name"]
        tokenizer_bytes = file_bytes(tokenizer_path, identity["tokenizer"])
        config_bytes = file_bytes(config_path, identity["tokenizer_config"])
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            tokenizer_copy = temporary / "tokenizer.json"
            config_copy = temporary / "tokenizer_config.json"
            shutil.copyfile(tokenizer_path, tokenizer_copy)
            shutil.copyfile(config_path, config_copy)
            tokenizer_copy.chmod(stat.S_IRUSR)
            config_copy.chmod(stat.S_IRUSR)
            file_bytes(tokenizer_copy, identity["tokenizer"])
            file_bytes(config_copy, identity["tokenizer_config"])
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                str(temporary), local_files_only=True, trust_remote_code=False, use_fast=True
            )
            config = json.loads(config_bytes.decode("utf-8"), object_pairs_hook=unique)
            if not isinstance(config.get("chat_template"), str) or tokenizer.chat_template != config["chat_template"]:
                return 3
            user_text = "Return one JSON object whose answer field is the string A."
            messages = [{"role": "user", "content": user_text}]
            base = tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                continue_final_message=False, enable_thinking=False,
            )
            neutral = tokenizer.encode(" x", add_special_tokens=False)
            user = tokenizer.encode(user_text, add_special_tokens=False)
            occurrences = [index for index in range(len(base) - len(user) + 1) if base[index:index + len(user)] == user]
            if len(neutral) != 1 or len(occurrences) != 1:
                return 3
            insertion = occurrences[0]
            rows = []
            for target in request["targets"]:
                prompt_length = target["prompt_length"]
                if prompt_length < len(base):
                    return 3
                values = base[:insertion] + [neutral[0]] * (prompt_length - len(base)) + base[insertion:]
                if len(values) != prompt_length or any(type(item) is not int or item < 0 or item >= tokenizer.vocab_size for item in values):
                    return 3
                rendered = tokenizer.decode(values, skip_special_tokens=False, clean_up_tokenization_spaces=False)
                if tokenizer.encode(rendered, add_special_tokens=False) != values:
                    return 3
                rows.append({
                    "array_id": target["array_id"], "decode_reencode_equal": True,
                    "ordinal": target["ordinal"], "prompt_length": prompt_length,
                    "sha256": sha(canonical(values)),
                })
            im_end = tokenizer.convert_tokens_to_ids("<|im_end|>")
            stops = list(dict.fromkeys([tokenizer.eos_token_id, im_end]))
            if stops != [151645] or sha(canonical(stops)) != STOP:
                return 3
            if tokenizer_path.read_bytes() != tokenizer_bytes or config_path.read_bytes() != config_bytes:
                return 3
            file_bytes(tokenizer_copy, identity["tokenizer"])
            file_bytes(config_copy, identity["tokenizer_config"])
        result = base_result(request)
        result.update(
            arrays=rows,
            checks=[{"check_id": value, "ordinal": index, "status": "PASS"} for index, value in enumerate(CHECKS)],
            stop_array_length=1,
            stop_array_sha256=STOP,
        )
        publish(output_path, result, repository / "specs/data/m4_tokenizer_materialization_result_schema_v1.json")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return 3
    except Exception:
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
