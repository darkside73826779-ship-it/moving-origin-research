#!/usr/bin/env python3
"""Run the custody-free, 30-second M4 dual-model crash-cart probe.

The two model roots and the output path are process-local inputs.  The report
contains only public identities, digests, integer timings, counts, and status.
It is synthetic diagnostic evidence, never governed scientific evidence.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import gc
import hashlib
import json
import os
import queue
import signal
import stat
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator


DATE = "2026-08-21"
REGIME = "B"
SCHEMA_VERSION = "m4-wsl2-dual-model-probe-report-v1"
MODEL_REPOSITORY = "Qwen/Qwen3-4B-Instruct-2507-FP8"
MODEL_REVISION = "8591804019c8b22094c3b5b4454e0edc05dffc98"
MODEL_FILES = {
    "model.safetensors": (5190053264, "b6154d74332140fd6dfbfbe70bbb3650dd6955861132bd59dda6789e6322b485"),
    "tokenizer.json": (11422654, "aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4"),
    "tokenizer_config.json": (9377, "a62ff0a2472a0fa1b8eaabcb57c59b58afa42a22831dc141400b6e0cf2b65ce3"),
}
ACTIVE_DURATION_NS = 30_000_000_000
PRODUCER_INTERVAL_NS = 5_000_000
QUEUE_CAPACITY = 8
GPU_MEMORY_UTILIZATION = 0.36
MAX_MODEL_LEN = 2048
MAX_NUM_SEQS = 8
SAMPLING_MAX_TOKENS = 12
SAMPLING_SEED = 0
TEMPERATURE = 0.0
SUPERVISOR_TIMEOUT_SECONDS = 300
PROMPT_PREFIX = (
    "This is a synthetic deterministic observation window. "
    "Return only the ordinal as an integer. Window="
)


class ProbeFailure(RuntimeError):
    """A sanitized fail-closed diagnostic disposition."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class Window:
    ordinal: int
    generated_ns: int
    enqueue_started_ns: int
    enqueued_ns: int
    producer_block_ns: int
    producer_observed_full: bool


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_model_root(raw: str | None) -> Path:
    if not raw:
        raise ProbeFailure("MODEL_ROOT_MISSING")
    root = Path(raw)
    if not root.is_absolute():
        raise ProbeFailure("MODEL_ROOT_IDENTITY_MISMATCH")
    try:
        if Path(os.path.abspath(root)) != root.resolve(strict=True):
            raise ProbeFailure("MODEL_ROOT_IDENTITY_MISMATCH")
        root_stat = root.lstat()
    except OSError as exc:
        raise ProbeFailure("MODEL_ROOT_UNREADABLE") from exc
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise ProbeFailure("MODEL_ROOT_IDENTITY_MISMATCH")
    for name, (expected_bytes, expected_digest) in MODEL_FILES.items():
        path = root / name
        try:
            file_stat = path.lstat()
        except OSError as exc:
            raise ProbeFailure("MODEL_FILE_UNREADABLE") from exc
        if stat.S_ISLNK(file_stat.st_mode) or not stat.S_ISREG(file_stat.st_mode):
            raise ProbeFailure("MODEL_FILE_IDENTITY_MISMATCH")
        if file_stat.st_size != expected_bytes or sha256_file(path) != expected_digest:
            raise ProbeFailure("MODEL_FILE_IDENTITY_MISMATCH")
    return root


def verify_distinct_model_roots(model_a: Path, model_b: Path) -> None:
    try:
        if os.path.samefile(model_a, model_b):
            raise ProbeFailure("MODEL_ROOTS_NOT_DISTINCT")
        for name in MODEL_FILES:
            if os.path.samefile(model_a / name, model_b / name):
                raise ProbeFailure("MODEL_ROOTS_NOT_DISTINCT")
    except OSError as exc:
        raise ProbeFailure("MODEL_ROOT_IDENTITY_MISMATCH") from exc


def gpu_used_mib() -> int:
    try:
        completed = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=memory.used",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        rows = [row.strip() for row in completed.stdout.splitlines() if row.strip()]
        if len(rows) != 1:
            raise ValueError
        return int(rows[0])
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        raise ProbeFailure("GPU_TELEMETRY_UNAVAILABLE") from exc


@contextlib.contextmanager
def silence_process_fds() -> Iterator[None]:
    """Prevent runtime logs from disclosing process-local model roots."""
    null_fd = os.open(os.devnull, os.O_WRONLY)
    saved_stdout = os.dup(1)
    saved_stderr = os.dup(2)
    try:
        os.dup2(null_fd, 1)
        os.dup2(null_fd, 2)
        yield
    finally:
        os.dup2(saved_stdout, 1)
        os.dup2(saved_stderr, 2)
        os.close(saved_stdout)
        os.close(saved_stderr)
        os.close(null_fd)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def prompt_for(ordinal: int) -> bytes:
    payload = {
        "feature_a": (ordinal * 17 + 3) % 101,
        "feature_b": (ordinal * ordinal + 11) % 97,
        "logical_time": ordinal * 100,
        "ordinal": ordinal,
    }
    return PROMPT_PREFIX.encode("utf-8") + canonical_bytes(payload)


def build_engine(root: Path) -> tuple[Any, int]:
    from vllm import LLM

    started_ns = time.monotonic_ns()
    engine = LLM(
        model=os.fspath(root),
        tokenizer=os.fspath(root),
        trust_remote_code=False,
        gpu_memory_utilization=GPU_MEMORY_UTILIZATION,
        max_model_len=MAX_MODEL_LEN,
        max_num_seqs=MAX_NUM_SEQS,
        seed=SAMPLING_SEED,
        disable_log_stats=True,
    )
    return engine, time.monotonic_ns() - started_ns


def infer(engine: Any, prompt: bytes, barrier: threading.Barrier, epoch_ns: int) -> dict[str, Any]:
    from vllm import SamplingParams

    barrier.wait(timeout=10)
    started_ns = time.monotonic_ns()
    result = engine.generate(
        [prompt.decode("utf-8")],
        SamplingParams(
            temperature=TEMPERATURE,
            max_tokens=SAMPLING_MAX_TOKENS,
            seed=SAMPLING_SEED,
        ),
        use_tqdm=False,
    )[0].outputs[0]
    completed_ns = time.monotonic_ns()
    output_bytes = result.text.encode("utf-8")
    return {
        "completed_ns": completed_ns - epoch_ns,
        "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
        "output_token_count": len(result.token_ids),
        "started_ns": started_ns - epoch_ns,
    }


def stop_engine(engine: Any) -> None:
    if engine is None:
        return
    llm_engine = getattr(engine, "llm_engine", None)
    shutdown = getattr(llm_engine, "shutdown", None)
    if callable(shutdown):
        shutdown()


def validate_report(report: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError as exc:
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED") from exc
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(report)
        validate_report_semantics(report)
    except (OSError, ValueError, jsonschema.exceptions.ValidationError) as exc:
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED") from exc


def validate_report_semantics(report: dict[str, Any]) -> None:
    rows = report["windows"]
    run = report["run"]
    if run["windows_consumed"] != len(rows):
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    if run["windows_produced"] - run["dropped_windows"] != len(rows):
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    if run["producer_blocked_count"] != sum(
        1 for row in rows if row["producer_observed_full"]
    ):
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    expected_order = list(range(len(rows)))
    if [row["ordinal"] for row in rows] != expected_order:
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    for expected, row in enumerate(rows):
        candidate = row["candidate"]
        peer = row["peer"]
        expected_overlap = max(
            0,
            min(candidate["completed_ns"], peer["completed_ns"])
            - max(candidate["started_ns"], peer["started_ns"]),
        )
        if (
            row["consumption_ordinal"] != expected
            or row["dropped"]
            or not row["order_preserved"]
            or candidate["completed_ns"] < candidate["started_ns"]
            or peer["completed_ns"] < peer["started_ns"]
            or row["queue_wait_ns"] != row["dequeued_ns"] - row["enqueue_ns"]
            or (row["producer_observed_full"] and row["producer_block_ns"] <= 0)
            or row["execution_overlap_ns"] != expected_overlap
            or row["execution_overlapped"] != (expected_overlap > 0)
            or row["launch_skew_ns"]
            != abs(candidate["started_ns"] - peer["started_ns"])
            or row["outputs_agree"]
            != (candidate["output_sha256"] == peer["output_sha256"])
            or row["prompt_sha256"] != hashlib.sha256(prompt_for(expected)).hexdigest()
        ):
            raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    if rows:
        if run["max_launch_skew_ns"] != max(row["launch_skew_ns"] for row in rows):
            raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
        if run["all_executions_overlap"] != all(
            row["execution_overlapped"] for row in rows
        ):
            raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
        if run["all_outputs_agree"] != all(row["outputs_agree"] for row in rows):
            raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    if run["order_preserved"] != all(row["order_preserved"] for row in rows):
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    if run["producer_backpressure_observed"] != (
        run["producer_blocked_count"] > 0
    ):
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")
    if report["status"] == "PASS" and not (
        len(rows) > 0
        and run["windows_produced"] == len(rows)
        and run["windows_consumed"] == len(rows)
        and len({row["ordinal"] for row in rows}) == len(rows)
    ):
        raise ProbeFailure("REPORT_SCHEMA_VALIDATION_FAILED")


def atomic_write(path: Path, payload: bytes) -> None:
    if path.exists() and path.is_symlink():
        raise ProbeFailure("OUTPUT_PATH_INVALID")
    if not path.parent.is_dir() or path.parent.is_symlink():
        raise ProbeFailure("OUTPUT_PATH_INVALID")
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists():
        raise ProbeFailure("OUTPUT_PATH_INVALID")
    try:
        with temporary.open("xb") as handle:
            handle.write(payload)
            handle.write(b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def base_report() -> dict[str, Any]:
    return {
        "authoritative_scoring": False,
        "controls": {
            "active_duration_ns": ACTIVE_DURATION_NS,
            "disable_log_stats": True,
            "gpu_memory_utilization_per_instance_ppm": 360000,
            "max_model_len": MAX_MODEL_LEN,
            "max_num_seqs": MAX_NUM_SEQS,
            "producer_interval_ns": PRODUCER_INTERVAL_NS,
            "queue_capacity": QUEUE_CAPACITY,
            "sampling_max_tokens": SAMPLING_MAX_TOKENS,
            "sampling_seed": SAMPLING_SEED,
            "temperature_millionths": 0,
            "trust_remote_code": False,
        },
        "date": DATE,
        "failure_codes": [],
        "model_identity": {
            "quantization": "OFFICIAL_QWEN_FP8_E4M3",
            "repository_id": MODEL_REPOSITORY,
            "revision": MODEL_REVISION,
        },
        "protected_seed_access": False,
        "regime": REGIME,
        "run": {
            "active_duration_ns": 0,
            "all_executions_overlap": False,
            "all_outputs_agree": False,
            "cleanup_gpu_used_mib": -1,
            "dropped_windows": 0,
            "max_launch_skew_ns": 0,
            "order_preserved": True,
            "peak_gpu_used_mib": 0,
            "producer_backpressure_observed": False,
            "producer_blocked_count": 0,
            "windows_consumed": 0,
            "windows_produced": 0,
        },
        "runtime": {
            "VLLM_USE_FLASHINFER_SAMPLER": "0",
            "VLLM_USE_V2_MODEL_RUNNER": "0",
            "runner": "V1",
        },
        "schema_version": SCHEMA_VERSION,
        "scientific_evidence": False,
        "status": "BLOCKED",
        "synthetic_only": True,
        "windows": [],
    }


def execute_probe(model_a: Path, model_b: Path, report: dict[str, Any]) -> None:
    verify_distinct_model_roots(model_a, model_b)
    engine_a = None
    engine_b = None
    work_queue: queue.Queue[Window | None] = queue.Queue(maxsize=QUEUE_CAPACITY)
    produced: list[int] = []
    consumed: list[int] = []
    rows: list[dict[str, Any]] = []
    producer_started_ns = 0
    producer_stopped_ns = 0
    peak_gpu_used_mib = gpu_used_mib()
    monitor_stop = threading.Event()
    monitor_failed = threading.Event()
    cancel = threading.Event()
    producer_errors: list[str] = []
    producer: threading.Thread | None = None

    def monitor_gpu() -> None:
        nonlocal peak_gpu_used_mib
        while not monitor_stop.wait(0.05):
            try:
                peak_gpu_used_mib = max(peak_gpu_used_mib, gpu_used_mib())
            except ProbeFailure:
                monitor_failed.set()
                monitor_stop.set()

    monitor = threading.Thread(target=monitor_gpu, name="m4-testbed-gpu-monitor", daemon=True)
    monitor.start()

    try:
        with silence_process_fds():
            engine_a, init_a_ns = build_engine(model_a)
            engine_b, init_b_ns = build_engine(model_b)
            epoch_ns = time.monotonic_ns()

            def produce() -> None:
                nonlocal producer_started_ns, producer_stopped_ns
                try:
                    producer_started_ns = time.monotonic_ns()
                    ordinal = 0
                    while (
                        not cancel.is_set()
                        and time.monotonic_ns() - producer_started_ns < ACTIVE_DURATION_NS
                    ):
                        generated_ns = time.monotonic_ns()
                        enqueue_started_ns = time.monotonic_ns()
                        observed_full = False
                        while not cancel.is_set():
                            try:
                                work_queue.put_nowait(ordinal)
                                break
                            except queue.Full:
                                observed_full = True
                                cancel.wait(0.01)
                        if cancel.is_set():
                            break
                        enqueued_ns = time.monotonic_ns()
                        timing_by_ordinal[ordinal] = Window(
                            ordinal,
                            generated_ns,
                            enqueue_started_ns,
                            enqueued_ns,
                            enqueued_ns - enqueue_started_ns,
                            observed_full,
                        )
                        produced.append(ordinal)
                        ordinal += 1
                        cancel.wait(PRODUCER_INTERVAL_NS / 1_000_000_000)
                    producer_stopped_ns = time.monotonic_ns()
                    while not cancel.is_set():
                        try:
                            work_queue.put_nowait(None)
                            break
                        except queue.Full:
                            cancel.wait(0.01)
                except Exception:
                    producer_errors.append("PRODUCER_FAILURE")
                    cancel.set()

            timing_by_ordinal: dict[int, Window] = {}
            producer = threading.Thread(target=produce, name="m4-testbed-window-producer")
            producer.start()
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                while True:
                    if cancel.is_set() and producer_errors:
                        raise ProbeFailure("PRODUCER_FAILURE")
                    try:
                        ordinal = work_queue.get(timeout=0.25)
                    except queue.Empty:
                        if not producer.is_alive():
                            raise ProbeFailure("PRODUCER_FAILURE")
                        continue
                    if ordinal is None:
                        break
                    while ordinal not in timing_by_ordinal and not cancel.is_set():
                        time.sleep(0)
                    if cancel.is_set():
                        raise ProbeFailure("PRODUCER_FAILURE")
                    window = timing_by_ordinal.pop(ordinal)
                    dequeued_ns = time.monotonic_ns()
                    prompt = prompt_for(window.ordinal)
                    barrier = threading.Barrier(2)
                    future_a = pool.submit(infer, engine_a, prompt, barrier, epoch_ns)
                    future_b = pool.submit(infer, engine_b, prompt, barrier, epoch_ns)
                    result_a = future_a.result()
                    result_b = future_b.result()
                    consumed.append(window.ordinal)
                    overlap_ns = max(
                        0,
                        min(result_a["completed_ns"], result_b["completed_ns"])
                        - max(result_a["started_ns"], result_b["started_ns"]),
                    )
                    rows.append(
                        {
                            "candidate": result_a,
                            "consumption_ordinal": len(consumed) - 1,
                            "dequeued_ns": dequeued_ns - epoch_ns,
                            "dropped": False,
                            "enqueue_ns": window.enqueued_ns - epoch_ns,
                            "execution_overlap_ns": overlap_ns,
                            "execution_overlapped": overlap_ns > 0,
                            "launch_skew_ns": abs(result_a["started_ns"] - result_b["started_ns"]),
                            "ordinal": window.ordinal,
                            "order_preserved": window.ordinal == len(consumed) - 1,
                            "outputs_agree": result_a["output_sha256"] == result_b["output_sha256"],
                            "peer": result_b,
                            "producer_block_ns": window.producer_block_ns,
                            "producer_observed_full": window.producer_observed_full,
                            "prompt_sha256": hashlib.sha256(prompt).hexdigest(),
                            "queue_wait_ns": dequeued_ns - window.enqueued_ns,
                        }
                    )
            producer.join()
            stop_engine(engine_a)
            stop_engine(engine_b)
    finally:
        cancel.set()
        if producer is not None:
            producer.join(timeout=5)
        monitor_stop.set()
        monitor.join(timeout=12)
        if monitor.is_alive():
            monitor_failed.set()
        with silence_process_fds():
            try:
                stop_engine(engine_a)
            except Exception:
                pass
            try:
                stop_engine(engine_b)
            except Exception:
                pass
            engine_a = None
            engine_b = None
            gc.collect()
            try:
                import torch

                torch.cuda.empty_cache()
            except Exception:
                pass
        if producer is not None and producer.is_alive():
            raise ProbeFailure("PRODUCER_FAILURE")

    cleanup_used = gpu_used_mib()
    cleanup_deadline = time.monotonic_ns() + 30_000_000_000
    while cleanup_used != 0 and time.monotonic_ns() < cleanup_deadline:
        time.sleep(0.25)
        cleanup_used = gpu_used_mib()

    active_duration_ns = max(0, producer_stopped_ns - producer_started_ns)
    blocked_count = sum(1 for row in rows if row["producer_observed_full"])
    run = {
        "active_duration_ns": active_duration_ns,
        "all_executions_overlap": bool(rows)
        and all(row["execution_overlapped"] for row in rows),
        "all_outputs_agree": bool(rows) and all(row["outputs_agree"] for row in rows),
        "cleanup_gpu_used_mib": cleanup_used,
        "dropped_windows": len(produced) - len(consumed),
        "initialization_a_ns": init_a_ns,
        "initialization_b_ns": init_b_ns,
        "max_launch_skew_ns": max((row["launch_skew_ns"] for row in rows), default=0),
        "order_preserved": produced == consumed,
        "peak_gpu_used_mib": peak_gpu_used_mib,
        "producer_backpressure_observed": blocked_count > 0,
        "producer_blocked_count": blocked_count,
        "windows_consumed": len(consumed),
        "windows_produced": len(produced),
    }
    report["run"] = run
    report["windows"] = rows
    invariants = {
        "ACTIVE_DURATION_SHORT": active_duration_ns < ACTIVE_DURATION_NS,
        "CLEANUP_VRAM_NONZERO": cleanup_used != 0,
        "DROPPED_WINDOWS": run["dropped_windows"] != 0,
        "EXECUTIONS_DID_NOT_OVERLAP": not run["all_executions_overlap"],
        "FIFO_ORDER_MISMATCH": not run["order_preserved"],
        "NO_BACKPRESSURE_OBSERVED": not run["producer_backpressure_observed"],
        "OUTPUT_DIGEST_MISMATCH": not run["all_outputs_agree"],
        "GPU_TELEMETRY_UNAVAILABLE": monitor_failed.is_set(),
        "PRODUCER_FAILURE": bool(producer_errors),
    }
    report["failure_codes"] = [code for code, failed in invariants.items() if failed]
    report["status"] = "PASS" if not report["failure_codes"] else "BLOCKED"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[2]
        / "specs/data/m4_wsl2_dual_model_probe_report_schema_v1.json",
    )
    return parser.parse_args(argv)


def run_worker() -> dict[str, Any]:
    os.environ["VLLM_USE_V2_MODEL_RUNNER"] = "0"
    os.environ["VLLM_USE_FLASHINFER_SAMPLER"] = "0"
    report = base_report()
    try:
        model_a = verify_model_root(os.environ.get("MOR_TESTBED_MODEL_A"))
        model_b = verify_model_root(os.environ.get("MOR_TESTBED_MODEL_B"))
        execute_probe(model_a, model_b, report)
    except ProbeFailure as exc:
        report["failure_codes"] = [exc.code]
    except Exception:
        report["failure_codes"] = ["INTERNAL_PROBE_FAILURE"]
    return report


def terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
        process.wait(timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            pass


def blocked_supervisor_report(code: str) -> dict[str, Any]:
    report = base_report()
    report["failure_codes"] = [code]
    cleanup_deadline = time.monotonic_ns() + 30_000_000_000
    try:
        cleanup_used = gpu_used_mib()
        while cleanup_used != 0 and time.monotonic_ns() < cleanup_deadline:
            time.sleep(0.25)
            cleanup_used = gpu_used_mib()
        report["run"]["cleanup_gpu_used_mib"] = cleanup_used
        if cleanup_used != 0:
            report["failure_codes"].append("CLEANUP_VRAM_NONZERO")
    except ProbeFailure:
        report["failure_codes"].append("GPU_TELEMETRY_UNAVAILABLE")
    return report


def supervise_worker(schema_path: Path) -> dict[str, Any]:
    command = [
        sys.executable,
        "-I",
        os.fspath(Path(__file__).resolve()),
        "--worker",
        "--schema",
        os.fspath(schema_path.resolve()),
    ]
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        start_new_session=(os.name == "posix"),
    )
    try:
        stdout, _ = process.communicate(timeout=SUPERVISOR_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        terminate_process_group(process)
        return blocked_supervisor_report("SUPERVISOR_TIMEOUT")
    if process.returncode != 0:
        return blocked_supervisor_report("CHILD_PROCESS_FAILURE")
    try:
        report = json.loads(stdout.decode("utf-8"))
        if not isinstance(report, dict):
            raise ValueError
        return report
    except (UnicodeError, ValueError):
        return blocked_supervisor_report("CHILD_PROCESS_FAILURE")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.worker:
        report = run_worker()
        try:
            validate_report(report, args.schema)
        except ProbeFailure:
            return 3
        sys.stdout.buffer.write(canonical_bytes(report))
        return 0
    if args.output is None:
        print(json.dumps({"failure_code": "OUTPUT_PATH_INVALID", "status": "BLOCKED"}, sort_keys=True))
        return 2
    report = supervise_worker(args.schema)
    try:
        validate_report(report, args.schema)
        atomic_write(args.output, canonical_bytes(report))
    except ProbeFailure as exc:
        print(json.dumps({"failure_code": exc.code, "status": "BLOCKED"}, sort_keys=True))
        return 2
    summary = {
        "failure_codes": report["failure_codes"],
        "report_sha256": hashlib.sha256(canonical_bytes(report) + b"\n").hexdigest(),
        "status": report["status"],
    }
    print(json.dumps(summary, separators=(",", ":"), sort_keys=True))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
