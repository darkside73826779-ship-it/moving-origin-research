"""Ledger-bound single-model proof of the moving-origin soft-prefix path."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.situated_origin.hf_soft_prefix_backend import (
    FrozenQwenSoftPrefixBackend,
    SoftPrefixTensorCodec,
)
from src.situated_origin.soft_prefix_strip import (
    OpaqueTraceUpdate,
    SoftPrefixExperienceStrip,
)
from src.situated_origin.runtime import SituatedRuntime


EVENT = "The project codename is MORPHEUS-731."
PUBLIC_QUERY = "Question: What is the project codename?\nAnswer with only the codename:"
MODEL_IDENTITY = "b6154d74332140fd6dfbfbe70bbb3650dd6955861132bd59dda6789e6322b485"


class FixedLearnedTraceEncoder:
    """One-shot bridge from the proven learned tensor into a ledger event."""

    def __init__(self, prefix, gradient_norm: float) -> None:
        self.prefix = prefix
        self.gradient_norm = gradient_norm
        self.calls = 0

    def __call__(self, request) -> OpaqueTraceUpdate:
        if request.content.decode("utf-8", errors="strict") != EVENT:
            raise ValueError("UNEXPECTED_TEACHING_EVENT")
        self.calls += 1
        return OpaqueTraceUpdate(
            value=self.prefix,
            update_norm=self.gradient_norm,
            update_budget=max(1.0, self.gradient_norm),
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--gradient-norm", type=float, required=True)
    parser.add_argument("--prefix-tokens", type=int, default=16)
    args = parser.parse_args()

    output_root = Path(args.output)
    output_root.mkdir(parents=True, exist_ok=True)
    backend = FrozenQwenSoftPrefixBackend(
        args.model,
        prefix_tokens=args.prefix_tokens,
        dequantize_fp8=True,
        max_new_tokens=12,
    )
    backend.load()
    learned_prefix = backend.load_prefix(args.prefix)
    hidden_size = int(learned_prefix.shape[-1])
    codec = SoftPrefixTensorCodec(
        prefix_tokens=args.prefix_tokens,
        hidden_size=hidden_size,
        model_identity=MODEL_IDENTITY,
    )
    encoder = FixedLearnedTraceEncoder(learned_prefix, args.gradient_norm)
    strip = SoftPrefixExperienceStrip(
        "integrated-origin-prefix-proof",
        capacity=8,
        trace_encoder=encoder,
        codec=codec,
        actuator_identity_sha256=hashlib.sha256(
            b"hf-soft-prefix-inputs-embeds-actuator-v1"
        ).hexdigest(),
        decay_factor="0.95",
        max_trace_bytes=256_000,
    )
    runtime = SituatedRuntime("integrated-origin-prefix-proof")

    teaching_event = runtime.commit_input(
        {
            "id": "teaching-event-0",
            "content": EVENT,
            "kind": "PUBLIC_TEACHING_EXPERIENCE",
            "importance": 8,
        }
    )
    trace = strip.append_committed(
        teaching_event, importance=8, prediction_error=1
    )
    acknowledgement = runtime.commit_response(
        {"output_text": "Experience recorded.", "claim_kind": "acknowledgement"}
    )
    strip.advance_origin(strip.origin, acknowledgement.stamp)

    baseline = backend.generate(PUBLIC_QUERY, prefix=None)
    query_event = runtime.commit_input(
        {
            "id": "recall-query-1",
            "content": PUBLIC_QUERY,
            "question": PUBLIC_QUERY,
            "kind": "PUBLIC_RECALL_QUERY",
            "memory_limit": 4,
        }
    )
    strip.advance_origin(strip.origin, query_event.stamp)
    snapshot = runtime.snapshot()
    recall = runtime.retrieve(snapshot, {"question": PUBLIC_QUERY, "memory_limit": 4})
    retrieved = strip.retrieve_by_event_ids(
        recall.selected_event_ids, snapshot.frame, limit=2
    )
    if not retrieved.records:
        raise RuntimeError("LEDGER_RECALL_DID_NOT_RESOLVE_PREFIX")
    resolved_prefix = strip.materialize_trace(
        retrieved.records[0].experience_id, source_log_head=runtime.head
    )
    memory = backend.generate(PUBLIC_QUERY, prefix=resolved_prefix)
    response_event = runtime.commit_response(
        {
            "output_text": memory.text,
            "claim_kind": "origin-memory-recall",
            "supporting_event_ids": list(retrieved.selected_event_ids),
        }
    )
    strip.advance_origin(strip.origin, response_event.stamp)
    runtime.verify()
    replay = SituatedRuntime.replay(
        "integrated-origin-prefix-proof", runtime.kernel.events()
    )

    checkpoint_path = output_root / "integrated-soft-prefix-strip.json"
    checkpoint = strip.save(checkpoint_path, overwrite=True)
    restored_strip = SoftPrefixExperienceStrip.load(
        checkpoint_path,
        trace_encoder=encoder,
        codec=codec,
        actuator_identity_sha256=hashlib.sha256(
            b"hf-soft-prefix-inputs-embeds-actuator-v1"
        ).hexdigest(),
        expected_checkpoint_sha256=checkpoint.checkpoint_sha256,
    )
    restored_record = restored_strip.snapshot()[0]
    restored_prefix = restored_strip.materialize_trace(
        restored_record.experience_id, source_log_head=restored_strip.source_log_head
    )
    restarted = backend.generate(PUBLIC_QUERY, prefix=restored_prefix)

    result = {
        "activation_delta_nonzero": memory.activation_delta_norm > 0,
        "activation_delta_norm": memory.activation_delta_norm,
        "base_model_frozen": all(
            parameter.requires_grad is False and parameter.grad is None
            for parameter in backend.model.parameters()
        ),
        "baseline_output": baseline.text,
        "checkpoint_sha256": checkpoint.checkpoint_sha256,
        "event_count": len(runtime.kernel.events()),
        "ledger_replay_exact": replay.head == runtime.head,
        "memory_output": memory.text,
        "model_linears_dequantized_in_memory": backend.replaced_fp8_linears,
        "no_recalled_text_in_query": EVENT not in PUBLIC_QUERY and "MORPHEUS-731" not in PUBLIC_QUERY,
        "prefix_bound_to_committed_event": strip.compare_to_log(
            trace.experience_id, teaching_event
        ).matches,
        "public_prompt_token_ids_sha256": memory.public_prompt_token_ids_sha256,
        "public_prompt_tokens_identical": (
            baseline.public_prompt_token_ids_sha256
            == memory.public_prompt_token_ids_sha256
            == restarted.public_prompt_token_ids_sha256
        ),
        "recall_selected_event_ids": list(recall.selected_event_ids),
        "reloaded_output_exact": restarted.text == memory.text,
        "strip_reloaded_exact": restored_strip.to_bytes() == strip.to_bytes(),
        "target_recalled": "MORPHEUS-731" in memory.text,
        "teaching_event_id": teaching_event.event_id,
        "trace_sha256": trace.trace_sha256,
    }
    (output_root / "integrated-origin-prefix-probe.json").write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, sort_keys=True))
    required = (
        "activation_delta_nonzero",
        "base_model_frozen",
        "ledger_replay_exact",
        "no_recalled_text_in_query",
        "prefix_bound_to_committed_event",
        "public_prompt_tokens_identical",
        "reloaded_output_exact",
        "strip_reloaded_exact",
        "target_recalled",
    )
    return 0 if all(result[key] is True for key in required) else 1


if __name__ == "__main__":
    raise SystemExit(main())
