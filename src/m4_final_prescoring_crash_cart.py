"""Custody-free, non-executing M4 crash-cart beta production seam."""
from __future__ import annotations

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

from jsonschema import Draft202012Validator

WARMUP_PAYLOADS = (0, 32, 512, 1024)
WARMUP_MAX_TOKENS = (8, 16, 16, 32)
WARMUP_BYTES = (89, 122, 603, 1116)
WARMUP_DIGESTS = (
    "eabe6b7c5cf863599f9444019b68e0e56dde640b824bfb30756aad9faa093485",
    "6b5697332c8ad2d6520655f4dc94133a1c17d4d228e3143f5f9bc80d685a04b4",
    "763187d517d8b35871bc5bb6a5c41df5283fd18f0589348eb299f2d2911076db",
    "5646b4c97252d178f3c73ccd8a2ef988674c7b3f515beb64376d4ea7ab60dd13",
)
FIXTURE_SIZES = (0, 32, 64, 128, 256, 512, 768, 1024)
LAW_ORDER = ("L7", "L8", "L10", "L14", "L18")
HELD_REASONS = {
    "L7": "SCORING_UNAUTHORIZED",
    "L8": "L8_PREREQUISITE_UNCLEARED",
    "L10": "SCORING_UNAUTHORIZED",
    "L14": "SCORING_UNAUTHORIZED",
    "L18": "EF3_ABSENT",
}
QUEUE_CAPACITY = 8
ACTIVE_DEADLINE_NS = 60_000_000_000
TELEMETRY_INTERVAL_NS = 250_000_000
WARMUP_RNG_DOMAIN = "M4_FINAL_CRASH_CART_WARMUP_V1"
STAGES = {
    "PRE_ACTIVE_TERMINAL",
    "PARTIAL_WARMUP_TERMINAL",
    "PARTIAL_ACTIVE_TERMINAL",
    "POST_ACTIVE_TERMINAL",
    "COMPLETE_ACTIVE_TERMINAL",
}
FAILURE_STAGES = {
    "PRE_ACTIVE_TERMINAL": {"PRE_START", "NEGATIVE_PROBES", "MODEL_LOAD"},
    "PARTIAL_WARMUP_TERMINAL": {"WARMUP", "WARMUP_CLEAN_BARRIER"},
    "PARTIAL_ACTIVE_TERMINAL": {"ACTIVE_WINDOW"},
    "POST_ACTIVE_TERMINAL": {"RENDER_VALIDATE_SCAN_EXPORT", "CLEANUP"},
}
RECEIPT_FIELDS = {
    "status",
    "backend_code",
    "session_id",
    "prior_backend_state_sha256",
    "result_backend_state_sha256",
    "request_sha256",
    "request_ordinal",
}
ACTIVE_CONTROLS = {
    "temperature": 0,
    "top_p": 1.0,
    "top_k": -1,
    "n": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "stop": [],
    "logprobs": False,
    "prefix_caching": False,
}


class CrashCartError(RuntimeError):
    """Governed structural crash-cart failure."""


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _bad(condition: bool, code: str) -> None:
    if condition:
        raise CrashCartError(code)


def warmup_prompt(ordinal: int, payload_bytes: int) -> bytes:
    invalid_identity = type(ordinal) is not int or not 0 <= ordinal < 4
    _bad(invalid_identity or payload_bytes != WARMUP_PAYLOADS[ordinal], "WARMUP_CONTRACT_MISMATCH")
    raw = (
        f"M4_WARMUP_PUBLIC_V1\n"
        f"ordinal={ordinal:04d}\n"
        f"payload_bytes={payload_bytes}\n"
        f"payload={'x' * payload_bytes}\n"
        "Respond with the ordinal only.\n"
    ).encode()
    invalid_bytes = (
        raw.count(b"\n") != 5
        or b"\\n" in raw
        or len(raw) != WARMUP_BYTES[ordinal]
        or sha256(raw) != WARMUP_DIGESTS[ordinal]
    )
    _bad(invalid_bytes, "WARMUP_CONTRACT_MISMATCH")
    return raw


def warmup_plan() -> tuple[dict[str, Any], ...]:
    plan = []
    for ordinal, payload_bytes in enumerate(WARMUP_PAYLOADS):
        plan.append({
            "ordinal": ordinal,
            "prompt": warmup_prompt(ordinal, payload_bytes),
            "prompt_sha256": WARMUP_DIGESTS[ordinal],
            "max_output_tokens": WARMUP_MAX_TOKENS[ordinal],
            "temperature": 0,
            "seed": 0,
            "rng_domain": WARMUP_RNG_DOMAIN,
            "top_p": 1.0,
            "top_k": -1,
            "n": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "stop": [],
            "logprobs": False,
            "prefix_caching": False,
            "pair_timeout_ns": 30_000_000_000,
            "sequence_deadline_ns": 120_000_000_000,
            "clean_barrier_deadline_ns": 10_000_000_000,
        })
    return tuple(plan)


def active_schedule() -> tuple[int, ...]:
    return tuple(0 if ordinal < 16 else (ordinal - 15) * 625_000_000 for ordinal in range(64))


def telemetry_schedule() -> tuple[int, ...]:
    return tuple(range(0, ACTIVE_DEADLINE_NS + 1, TELEMETRY_INTERVAL_NS))


def public_fixture(ordinal: int) -> dict[str, Any]:
    _bad(type(ordinal) is not int or not 0 <= ordinal < 64, "ACTIVE_ORDINAL_INVALID")
    family, repetition = ordinal % 8, ordinal // 8
    text = (
        "M4_CRASH_CART_PUBLIC_V1\n"
        f"ordinal={ordinal:04d}\n"
        f"family={family}\n"
        f"repetition={repetition}\n"
        f"payload={'x' * FIXTURE_SIZES[family]}\n"
    )
    return {
        "ordinal": ordinal,
        "fixture_id": f"family-{family}-repeat-{repetition}",
        "payload_bytes": FIXTURE_SIZES[family],
        "public_prompt_text": text,
        "prompt_sha256": sha256(text.encode()),
    }


def fixture_inventory() -> tuple[dict[str, Any], ...]:
    return tuple(public_fixture(ordinal) for ordinal in range(64))


def held_laws() -> tuple[dict[str, Any], ...]:
    rows = []
    for law, line in zip(LAW_ORDER, (26, 28, 32, 42, 54)):
        rows.append({
            "law_id": law,
            "status": "HELD",
            "claim_made": False,
            "meaning_source": f"docs/ARCHITECTURAL_CONSTITUTION_v2.md:{line}",
            "evidence": [],
            "metrics": {},
            "failure_code": None,
            "held_reason": HELD_REASONS[law],
        })
    return tuple(rows)


def _compose_schema(report: Mapping[str, Any]) -> None:
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "specs/data/m4_final_prescoring_full_stack_crash_cart_report_schema_v1.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(
        schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
    if next(validator.iter_errors(report), None) is not None:
        raise CrashCartError("REPORT_SCHEMA_INVALID")


def validate_terminal(report: Mapping[str, Any]) -> None:
    invalid_stage = not isinstance(report, Mapping) or report.get("evidence_stage") not in STAGES
    _bad(invalid_stage, "EVIDENCE_STAGE_INVALID")
    _compose_schema(report)

    stage = report["evidence_stage"]
    rows = report["rows"]
    samples = report["resource_samples"]
    warmup = report["warmup"]
    active = report["active_window"]
    trends = report["trends"]
    replica = report["replica_consistency"]

    if stage == "COMPLETE_ACTIVE_TERMINAL":
        invalid_terminal = (
            report["failure_stage"] is not None
            or report["failure"] is not None
            or report["structural_status"] != "PASS"
        )
        _bad(invalid_terminal, "COMPLETE_TERMINAL_INVALID")
        invalid_warmup = (
            warmup.get("status") != "PASS"
            or warmup.get("attempted_pair_count") != 4
            or len(warmup.get("rows", [])) != 4
            or any(row.get("candidate") is None or row.get("peer") is None for row in warmup["rows"])
        )
        _bad(invalid_warmup, "COMPLETE_EVIDENCE_MISSING")
        invalid_active = (
            active.get("status") != "PASS"
            or active.get("attempted_pair_count") != 64
            or active.get("completed_pair_count") != 64
            or active.get("drop_count") != 0
            or active.get("duration_ns", 0) < 30_000_000_000
        )
        _bad(invalid_active, "COMPLETE_EVIDENCE_MISSING")
        invalid_rows = len(rows) != 64 or any(
            row.get("ordinal") != ordinal or row.get("candidate") is None or row.get("peer") is None
            for ordinal, row in enumerate(rows)
        )
        invalid_derived = (
            len(samples) < 121
            or any(not sample for sample in samples)
            or not trends
            or replica.get("status") not in {"MATCH", "MISMATCH"}
            or report["laws"] not in (list(held_laws()), held_laws())
        )
        _bad(invalid_rows or invalid_derived, "COMPLETE_EVIDENCE_MISSING")
        cleanup = report["cleanup"]
        public_safety = report["public_safety"]
        export = report["export"]
        invalid_publication = (
            cleanup.get("status") != "PASS"
            or cleanup.get("attempted") is not True
            or public_safety.get("status") != "CLEAR"
            or export.get("status") != "EXPORTED"
            or export.get("reproduction_equal") is not True
        )
        _bad(invalid_publication, "COMPLETE_EVIDENCE_MISSING")
        return

    failure = report["failure"]
    failure_stage = report["failure_stage"]
    invalid_failure = (
        failure_stage not in FAILURE_STAGES.get(stage, set())
        or failure.get("stage") != failure_stage
        or failure.get("retry_count") != 0
        or report["structural_status"] not in {"BLOCKED", "INSTRUMENT_FAILURE"}
    )
    _bad(invalid_failure, "FAILURE_PROJECTION_INVALID")

    if stage == "PRE_ACTIVE_TERMINAL":
        fabricated = (
            warmup is not None
            or active is not None
            or bool(rows)
            or bool(samples)
            or trends is not None
            or replica.get("status") != "NOT_RUN"
        )
    elif stage == "PARTIAL_WARMUP_TERMINAL":
        fabricated = (
            warmup.get("status") != "FAIL"
            or len(warmup.get("rows", [])) > 4
            or active is not None
            or bool(rows)
            or bool(samples)
            or trends is not None
        )
    elif stage == "PARTIAL_ACTIVE_TERMINAL":
        fabricated = (
            warmup.get("status") != "PASS"
            or warmup.get("attempted_pair_count") != 4
            or len(warmup.get("rows", [])) != 4
            or active.get("status") != "FAIL"
            or len(rows) > 64
            or trends is not None
            or replica.get("status") != "NOT_RUN"
        )
    else:
        fabricated = (
            warmup.get("status") != "PASS"
            or active.get("status") != "PASS"
            or len(rows) != 64
            or len(samples) < 121
            or not isinstance(report["cleanup"], Mapping)
        )
    _bad(fabricated, "FABRICATED_LATER_STAGE_EVIDENCE")


def exact_replica_consumer_stop(replica: Mapping[str, Any]) -> None:
    if replica.get("status") == "MISMATCH":
        raise CrashCartError("EXACT_REPLICA_CONSUMER_STOP")


def execution_guard(value: Any) -> None:
    if value is not False:
        raise CrashCartError("RUN_AUTHORITY_INVALID")
    raise CrashCartError("RUN_AUTHORITY_ABSENT")


@dataclass
class CrashCartLifecycle:
    candidate: Callable[[Mapping[str, Any]], Mapping[str, Any]]
    peer: Callable[[Mapping[str, Any]], Mapping[str, Any]]
    reset: Callable[[str], Mapping[str, Any]]
    cleanup: Callable[[], None]
    clock_ns: Callable[[], int] | None = None
    sleep_until_ns: Callable[[int], None] | None = None
    sampler: Callable[[int, int], Mapping[str, Any]] | None = None
    events: list[str] = field(default_factory=list)
    _virtual_ns: int = 0
    _states: dict[str, str] = field(
        default_factory=lambda: {"candidate": "0" * 64, "peer": "0" * 64}
    )

    def _now(self) -> int:
        return self.clock_ns() if self.clock_ns else self._virtual_ns

    def _wait(self, target: int) -> None:
        if self.sleep_until_ns:
            self.sleep_until_ns(target)
        else:
            self._virtual_ns = max(self._virtual_ns, target)
        _bad(self._now() < target, "SCHEDULE_BYPASS")

    @staticmethod
    def _digest(value: Any) -> bool:
        return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None

    def _validate_reset_receipt(self, role: str, receipt: Mapping[str, Any]) -> str:
        _bad(not isinstance(receipt, Mapping) or set(receipt) != RECEIPT_FIELDS,
             "RESET_RECEIPT_SHAPE_INVALID")
        _bad(receipt.get("status") != "PASS" or receipt.get("backend_code") is not None,
             "RESET_RECEIPT_STATUS_INVALID")
        _bad(receipt.get("session_id") != role, "RESET_RECEIPT_SESSION_INVALID")
        _bad(not self._digest(receipt.get("prior_backend_state_sha256")),
             "RESET_PRIOR_STATE_INVALID")
        result = receipt.get("result_backend_state_sha256")
        _bad(not self._digest(result), "RESET_RESULT_STATE_INVALID")
        invalid_correlation = (
            not self._digest(receipt.get("request_sha256"))
            or receipt.get("request_ordinal") is not None
        )
        _bad(invalid_correlation, "RESET_RECEIPT_CORRELATION_INVALID")
        return result

    def _reset_pair(self, phase: str) -> None:
        receipts = {role: self.reset(role) for role in ("candidate", "peer")}
        rebound = {
            role: self._validate_reset_receipt(role, receipts[role])
            for role in ("candidate", "peer")
        }
        _bad(receipts["candidate"]["session_id"] == receipts["peer"]["session_id"],
             "SHARED_SESSION_INVALID")
        self._states = rebound
        self.events.append(f"reset-{phase}")

    def _request(self, kind: str, ordinal: int, item: Mapping[str, Any]) -> dict[str, Any]:
        controls = warmup_plan()[ordinal] if kind == "warmup" else ACTIVE_CONTROLS
        return {
            "kind": kind,
            "ordinal": ordinal,
            "fixture_id": item.get("fixture_id"),
            "prompt_sha256": item["prompt_sha256"],
            "controls": {key: value for key, value in controls.items() if key != "prompt"},
        }

    def _validate_role_receipt(
        self,
        role: str,
        receipt: Mapping[str, Any],
        expected_request_sha256: str,
        ordinal: int,
    ) -> str:
        _bad(not isinstance(receipt, Mapping) or set(receipt) != RECEIPT_FIELDS,
             "RECEIPT_SHAPE_INVALID")
        _bad(receipt.get("status") != "PASS", "RECEIPT_STATUS_INVALID")
        _bad(receipt.get("backend_code") is not None, "RECEIPT_BACKEND_CODE_INVALID")
        _bad(receipt.get("session_id") != role, "RECEIPT_SESSION_INVALID")
        _bad(receipt.get("request_sha256") != expected_request_sha256,
             "RECEIPT_REQUEST_DIGEST_INVALID")
        prior = receipt.get("prior_backend_state_sha256")
        result = receipt.get("result_backend_state_sha256")
        _bad(not self._digest(prior) or prior != self._states[role],
             "RECEIPT_PRIOR_STATE_INVALID")
        _bad(not self._digest(result), "RECEIPT_RESULT_STATE_INVALID")
        _bad(receipt.get("request_ordinal") != ordinal, "RECEIPT_ORDINAL_INVALID")
        return result

    def _pair(
        self,
        kind: str,
        ordinal: int,
        item: Mapping[str, Any],
    ) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
        request = self._request(kind, ordinal, item)
        self.events.append(f"{kind}-barrier-{ordinal}")
        with ThreadPoolExecutor(max_workers=2) as pool:
            candidate_future = pool.submit(self.candidate, request)
            peer_future = pool.submit(self.peer, request)
            receipts = (candidate_future.result(), peer_future.result())

        expected_request_sha256 = sha256(canonical_bytes(request))
        rebound = {}
        for role, receipt in zip(("candidate", "peer"), receipts):
            rebound[role] = self._validate_role_receipt(
                role,
                receipt,
                expected_request_sha256,
                ordinal,
            )
        _bad(receipts[0]["session_id"] == receipts[1]["session_id"], "SHARED_SESSION_INVALID")
        self._states.update(rebound)
        return receipts

    def warmup(self) -> list[tuple[Mapping[str, Any], Mapping[str, Any]]]:
        self._reset_pair("warmup")
        rows = [self._pair("warmup", item["ordinal"], item) for item in warmup_plan()]
        self._reset_pair("measured")
        self.events.extend(("clean-barrier", "rng-after-clean-barrier"))
        return rows

    def _collect_samples(
        self,
        samples: list[Mapping[str, Any]],
        next_sample: int,
        now: int,
        completed: int,
    ) -> int:
        while next_sample <= now:
            observed = (
                dict(self.sampler(next_sample, completed))
                if self.sampler
                else {
                    "monotonic_ns": next_sample,
                    "queue_depth_pairs": 0,
                    "completed_pair_count": completed,
                }
            )
            _bad(observed.get("monotonic_ns") != next_sample,
                 "TELEMETRY_OBSERVATION_INVALID")
            samples.append(observed)
            next_sample += TELEMETRY_INTERVAL_NS
        return next_sample

    @staticmethod
    def _assert_within_deadline(start: int, observed: int) -> None:
        _bad(observed - start > ACTIVE_DEADLINE_NS, "ACTIVE_WINDOW_TIMEOUT_NO_RETRY")

    @staticmethod
    def _assert_pair_completion_within_deadline(start: int, observed: int) -> None:
        _bad(observed - start > ACTIVE_DEADLINE_NS, "ACTIVE_WINDOW_TIMEOUT_NO_RETRY")

    def active(self) -> tuple[list[tuple[Mapping[str, Any], Mapping[str, Any]]], list[Mapping[str, Any]]]:
        _bad("rng-after-clean-barrier" not in self.events, "RNG_INSERTION_INVALID")
        start = self._now()
        samples: list[Mapping[str, Any]] = []
        rows: list[tuple[Mapping[str, Any], Mapping[str, Any]]] = []
        next_sample = start

        for item, offset in zip(fixture_inventory(), active_schedule()):
            self._wait(start + offset)
            observed_before = self._now()
            self._assert_within_deadline(start, observed_before)
            next_sample = self._collect_samples(samples, next_sample, observed_before, len(rows))
            self.events.append(f"dispatch@{observed_before - start}")
            self.events.append("queue-depth-1")
            _bad(1 > QUEUE_CAPACITY, "QUEUE_CAPACITY_EXCEEDED")

            completed_pair = self._pair("active", item["ordinal"], item)
            observed_after = self._now()
            self._assert_pair_completion_within_deadline(start, observed_after)
            rows.append(completed_pair)
            next_sample = self._collect_samples(samples, next_sample, observed_after, len(rows))

        terminal_now = self._now()
        self._assert_within_deadline(start, terminal_now)
        _bad(terminal_now - start < 30_000_000_000, "ACTIVE_WINDOW_TOO_SHORT")
        return rows, samples

    def run(self) -> dict[str, Any]:
        try:
            warmup_rows = self.warmup()
            active_rows, samples = self.active()
            return {
                "warmup_ordinals": [row[0]["request_ordinal"] for row in warmup_rows],
                "active_ordinals": [row[0]["request_ordinal"] for row in active_rows],
                "dispatch_observed_ns": [
                    int(event.split("@")[-1])
                    for event in self.events
                    if event.startswith("dispatch@")
                ],
                "telemetry": samples,
                "max_queue_depth": 1,
            }
        except Exception as exc:
            self.events.append("rollback")
            try:
                self._reset_pair("rollback")
            except Exception as rollback_exc:
                raise CrashCartError("PAIR_ROLLBACK") from rollback_exc
            if isinstance(exc, CrashCartError):
                raise
            raise CrashCartError("PAIR_ROLLBACK") from exc
        finally:
            self.cleanup()
            self.events.append("cleanup")
