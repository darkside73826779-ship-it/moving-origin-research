#!/usr/bin/env python3
"""Emit a custody-free M4 WSL2 audit-readiness report.

This command never resolves model, tokenizer, custody, prompt, seed, scoring,
or inference inputs. It validates only public immutable repository identities,
the already-installed diagnostic runtime, and a mount-free/no-network GPU
visibility smoke in the pinned image.
"""

from __future__ import annotations

import hashlib
import importlib.metadata as metadata
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

import jsonschema


DATE = "2026-08-22"
REGIME = "B"
SCHEMA_VERSION = "m4-wsl2-audit-readiness-report-v1"
BASE_TAG = "m4-wsl2-preexecution-testbed-v1.2"
BASE_TAG_OBJECT = "1994709b41c8e108e0b6f9a15936681f596823af"
BASE_COMMIT = "11ea682a7f0fadfa1437a12d882402d90ffd0579"
RECOMMENDED_TAG = "m4-wsl2-preexecution-testbed-v1.3"
IMAGE = "docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6"
IMAGE_ID = "sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6"
IMAGE_INDEX = "sha256:607442e407b0fea97f8a132a78b787c121a996dd4de181fa08e8da06e71ec2db"
EXPECTED_KERNEL = "6.18.33.2-microsoft-standard-WSL2"
EXPECTED_GPU = "NVIDIA GeForce RTX 5080, 610.88, 16303"
EXPECTED_DOCKER = "CLIENT=29.1.3 SERVER=29.1.3 OS=linux ARCH=amd64"
EXPECTED_TOOLKIT = (
    "NVIDIA Container Toolkit CLI version 1.20.0\n"
    "commit: 5505e2f94d9aaa08561490db974ba3cd676af209"
)
DIAGNOSTIC_PACKAGES = {
    "jsonschema": "4.26.0",
    "numpy": "2.3.5",
    "safetensors": "0.8.0",
    "tokenizers": "0.22.2",
    "torch": "2.13.0+cu132",
    "transformers": "5.15.1",
    "vllm": "0.27.1",
}
CHECK_IDS = [
    "IMMUTABLE_BASE_TAG",
    "IMMUTABLE_CHECKOUT",
    "LF_AND_SIDECAR_DISCIPLINE",
    "PYTHON_RUNTIME",
    "PYTHON_DEPENDENCIES",
    "V1_COMPATIBILITY",
    "WSL_GPU_IDENTITY",
    "DOCKER_TOOLKIT_IDENTITY",
    "OCI_PLATFORM_IDENTITY",
    "NO_CUSTODY_NETWORK_MOUNT_CONTROLS",
    "PUBLIC_SYNTHETIC_TESTS",
    "OCI_GPU_VISIBILITY_SMOKE",
]


class ReadinessStop(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def run(*args: str, cwd: Path, timeout: int = 30) -> str:
    try:
        completed = subprocess.run(
            list(args),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        raise ReadinessStop("COMMAND_FAILED") from exc
    return completed.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_contract(root: Path) -> dict[str, Any]:
    path = root / "specs/data/m4_wsl2_audit_readiness_contract_v1.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReadinessStop("CONTRACT_INVALID") from exc
    return value


def check_immutable_base(root: Path, _: dict[str, Any]) -> None:
    if run("git", "rev-parse", f"refs/tags/{BASE_TAG}", cwd=root) != BASE_TAG_OBJECT:
        raise ReadinessStop("TAG_OBJECT_MISMATCH")
    if run("git", "rev-parse", f"refs/tags/{BASE_TAG}^{{}}", cwd=root) != BASE_COMMIT:
        raise ReadinessStop("TAG_COMMIT_MISMATCH")


def check_immutable_locks(root: Path, contract: dict[str, Any]) -> None:
    for key in ("dependency_lock", "environment_lock"):
        binding = contract.get(key)
        if not isinstance(binding, dict) or set(binding) != {"path", "raw_sha256"}:
            raise ReadinessStop("CONTRACT_INVALID")
        relative = binding["path"]
        expected = binding["raw_sha256"]
        if not isinstance(relative, str) or not re.fullmatch(r"[0-9a-f]{64}", expected or ""):
            raise ReadinessStop("CONTRACT_INVALID")
        path = root / relative
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise ReadinessStop("LOCK_IDENTITY_MISMATCH")


def check_checkout(root: Path, _: dict[str, Any]) -> None:
    if run("git", "status", "--porcelain=v1", "--untracked-files=all", cwd=root):
        raise ReadinessStop("CHECKOUT_DIRTY")
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", BASE_COMMIT, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode:
        raise ReadinessStop("BASE_ANCESTRY_MISMATCH")


def check_lf_and_sidecars(root: Path, contract: dict[str, Any]) -> None:
    paths = contract.get("lf_paths")
    if not isinstance(paths, list) or not paths or len(paths) != len(set(paths)):
        raise ReadinessStop("LF_PATH_SET_INVALID")
    for relative in paths:
        if not isinstance(relative, str) or relative.startswith(("/", "\\")) or ".." in Path(relative).parts:
            raise ReadinessStop("LF_PATH_SET_INVALID")
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise ReadinessStop("LF_PATH_IDENTITY_MISMATCH")
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
            raise ReadinessStop("LF_BYTES_MISMATCH")
        attributes = run("git", "check-attr", "text", "eol", "--", relative, cwd=root).splitlines()
        if attributes != [f"{relative}: text: set", f"{relative}: eol: lf"]:
            raise ReadinessStop("LF_ATTRIBUTE_MISMATCH")
        if relative.endswith(".json"):
            sidecar = path.with_name(path.name + ".sha256")
            if not sidecar.is_file() or sidecar.is_symlink():
                raise ReadinessStop("SIDECAR_MISSING")
            expected = f"{sha256(path)}  {path.name}\n".encode("ascii")
            if sidecar.read_bytes() != expected:
                raise ReadinessStop("SIDECAR_MISMATCH")


def check_python_runtime(_: Path, __: dict[str, Any]) -> None:
    if platform.python_version() != "3.12.3":
        raise ReadinessStop("PYTHON_VERSION_MISMATCH")


def check_python_dependencies(_: Path, __: dict[str, Any]) -> None:
    for name, expected in DIAGNOSTIC_PACKAGES.items():
        try:
            actual = metadata.version(name)
        except metadata.PackageNotFoundError as exc:
            raise ReadinessStop("PYTHON_PACKAGE_MISSING") from exc
        if actual != expected:
            raise ReadinessStop("PYTHON_PACKAGE_VERSION_MISMATCH")


def check_v1_compatibility(_: Path, __: dict[str, Any]) -> None:
    if os.environ.get("VLLM_USE_V2_MODEL_RUNNER") != "0" or os.environ.get("VLLM_USE_FLASHINFER_SAMPLER") != "0":
        raise ReadinessStop("V1_COMPATIBILITY_MISSING")


def check_wsl_gpu(root: Path, _: dict[str, Any]) -> None:
    if run("uname", "-r", cwd=root) != EXPECTED_KERNEL:
        raise ReadinessStop("WSL_KERNEL_MISMATCH")
    gpu = run(
        "nvidia-smi",
        "--query-gpu=name,driver_version,memory.total",
        "--format=csv,noheader,nounits",
        cwd=root,
    )
    if gpu != EXPECTED_GPU:
        raise ReadinessStop("GPU_IDENTITY_MISMATCH")


def check_docker_toolkit(root: Path, _: dict[str, Any]) -> None:
    docker = run(
        "docker",
        "version",
        "--format",
        "CLIENT={{.Client.Version}} SERVER={{.Server.Version}} OS={{.Server.Os}} ARCH={{.Server.Arch}}",
        cwd=root,
    )
    if docker != EXPECTED_DOCKER:
        raise ReadinessStop("DOCKER_IDENTITY_MISMATCH")
    if run("nvidia-ctk", "--version", cwd=root) != EXPECTED_TOOLKIT:
        raise ReadinessStop("TOOLKIT_IDENTITY_MISMATCH")


def check_image(root: Path, _: dict[str, Any]) -> None:
    identity = run(
        "docker", "image", "inspect", IMAGE,
        "--format", "{{.Id}}|{{.Os}}|{{.Architecture}}", cwd=root,
    )
    if identity != f"{IMAGE_ID}|linux|amd64":
        raise ReadinessStop("OCI_PLATFORM_IDENTITY_MISMATCH")


def gpu_smoke_command() -> list[str]:
    return [
        "docker", "run", "--rm", "--pull=never", "--platform", "linux/amd64",
        "--network", "none", "--gpus", "all", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=64m,mode=0700",
        "--entrypoint", "python3", IMAGE, "-I", "-c",
        "import torch; assert torch.cuda.is_available(); assert torch.__version__ == '2.8.0+cu128'",
    ]


def check_controls(_: Path, __: dict[str, Any]) -> None:
    command = gpu_smoke_command()
    joined = "\0".join(command)
    required = ("--pull=never", "--network\0none", "--read-only", "--cap-drop\0ALL", "no-new-privileges")
    forbidden = ("--mount", "-v\0", "--volume", "--env", "-e\0")
    if any(value not in joined for value in required) or any(value in joined for value in forbidden):
        raise ReadinessStop("RUNTIME_CONTROL_MISMATCH")


def check_public_tests(root: Path, _: dict[str, Any]) -> None:
    run(
        sys.executable, "-I", "-m", "unittest", "discover", "-s", "tests", "-t", ".",
        "-p", "test_m4_wsl2_audit_readiness.py", cwd=root, timeout=60,
    )


def check_gpu_smoke(root: Path, _: dict[str, Any]) -> None:
    run(*gpu_smoke_command(), cwd=root, timeout=120)


CHECKS: list[tuple[str, Callable[[Path, dict[str, Any]], None]]] = [
    (CHECK_IDS[0], check_immutable_base),
    (CHECK_IDS[1], check_checkout),
    (CHECK_IDS[2], check_lf_and_sidecars),
    (CHECK_IDS[3], check_python_runtime),
    (CHECK_IDS[4], check_python_dependencies),
    (CHECK_IDS[5], check_v1_compatibility),
    (CHECK_IDS[6], check_wsl_gpu),
    (CHECK_IDS[7], check_docker_toolkit),
    (CHECK_IDS[8], check_image),
    (CHECK_IDS[9], check_controls),
    (CHECK_IDS[10], check_public_tests),
    (CHECK_IDS[11], check_gpu_smoke),
]


def base_report() -> dict[str, Any]:
    return {
        "authoritative_scoring": False,
        "base_commit_sha1": BASE_COMMIT,
        "base_tag": BASE_TAG,
        "base_tag_object_sha1": BASE_TAG_OBJECT,
        "checks": [],
        "custody_access": False,
        "date": DATE,
        "failure_code": None,
        "image_index_digest": IMAGE_INDEX,
        "image_platform_digest": IMAGE_ID,
        "inference_executed": False,
        "network_access": False,
        "protected_seed_access": False,
        "recommended_tag": RECOMMENDED_TAG,
        "regime": REGIME,
        "schema_version": SCHEMA_VERSION,
        "scientific_evidence": False,
        "status": "BLOCKED",
        "synthetic_only": True,
    }


def execute(root: Path) -> dict[str, Any]:
    contract = load_contract(root)
    report = base_report()
    failed = False
    for ordinal, (check_id, operation) in enumerate(CHECKS):
        if failed:
            status = "NOT_RUN"
        else:
            try:
                if check_id == "IMMUTABLE_CHECKOUT":
                    check_immutable_locks(root, contract)
                operation(root, contract)
                status = "PASS"
            except ReadinessStop as exc:
                status = "FAIL"
                report["failure_code"] = exc.code
                failed = True
        report["checks"].append({"check_id": check_id, "ordinal": ordinal, "status": status})
    if not failed:
        report["status"] = "PASS"
    return report


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def validate_report_semantics(report: dict[str, Any]) -> None:
    rows = report.get("checks")
    if not isinstance(rows, list) or len(rows) != len(CHECK_IDS):
        raise ReadinessStop("REPORT_VALIDATION_FAILED")
    if [(row.get("ordinal"), row.get("check_id")) for row in rows] != list(enumerate(CHECK_IDS)):
        raise ReadinessStop("REPORT_VALIDATION_FAILED")
    statuses = [row.get("status") for row in rows]
    failures = [index for index, value in enumerate(statuses) if value == "FAIL"]
    if report.get("status") == "PASS":
        if statuses != ["PASS"] * len(CHECK_IDS) or report.get("failure_code") is not None:
            raise ReadinessStop("REPORT_VALIDATION_FAILED")
    elif len(failures) != 1:
        raise ReadinessStop("REPORT_VALIDATION_FAILED")
    else:
        failed = failures[0]
        if statuses[:failed] != ["PASS"] * failed or statuses[failed + 1:] != ["NOT_RUN"] * (len(CHECK_IDS) - failed - 1):
            raise ReadinessStop("REPORT_VALIDATION_FAILED")


def repository_root() -> Path:
    root = Path(__file__).resolve(strict=True).parents[2]
    if run("git", "rev-parse", "--show-toplevel", cwd=root) != str(root):
        raise ReadinessStop("REPOSITORY_ROOT_MISMATCH")
    return root


def main() -> int:
    os.environ["VLLM_USE_V2_MODEL_RUNNER"] = "0"
    os.environ["VLLM_USE_FLASHINFER_SAMPLER"] = "0"
    try:
        root = repository_root()
        report = execute(root)
        schema = json.loads((root / "specs/data/m4_wsl2_audit_readiness_report_schema_v1.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(report)
        validate_report_semantics(report)
    except (ReadinessStop, OSError, UnicodeError, json.JSONDecodeError, jsonschema.ValidationError) as exc:
        code = exc.code if isinstance(exc, ReadinessStop) else "REPORT_VALIDATION_FAILED"
        print(json.dumps({"failure_code": code, "status": "BLOCKED"}, sort_keys=True))
        return 2
    sys.stdout.buffer.write(canonical(report) + b"\n")
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
