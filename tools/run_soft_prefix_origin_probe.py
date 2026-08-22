"""Bounded local proof that origin memory changes a frozen model's activations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.situated_origin.hf_soft_prefix_backend import FrozenQwenSoftPrefixBackend


EVENT = "The project codename is MORPHEUS-731."
PUBLIC_QUERY = "Question: What is the project codename?\nAnswer with only the codename:"
TARGET = " MORPHEUS-731"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--steps", type=int, default=24)
    parser.add_argument("--prefix-tokens", type=int, default=16)
    args = parser.parse_args()

    if "MORPHEUS-731" in PUBLIC_QUERY:
        raise RuntimeError("PUBLIC_QUERY_LEAKS_MEMORY_CONTENT")
    output_root = Path(args.output)
    output_root.mkdir(parents=True, exist_ok=True)
    backend = FrozenQwenSoftPrefixBackend(
        args.model,
        prefix_tokens=args.prefix_tokens,
        default_steps=args.steps,
        learning_rate=0.05,
        max_new_tokens=12,
        dequantize_fp8=True,
    )
    backend.load()
    frozen_before = all(
        parameter.requires_grad is False and parameter.grad is None
        for parameter in backend.model.parameters()
    )
    baseline = backend.generate(PUBLIC_QUERY, prefix=None)
    trained = backend.train_prefix(
        event_text=EVENT,
        cue_text=PUBLIC_QUERY,
        target_text=TARGET,
    )
    memory = backend.generate(PUBLIC_QUERY, prefix=trained.prefix)
    initial_loss = trained.initial_loss
    final_loss = trained.final_loss
    gradient_norm = trained.gradient_norm
    prefix_path = output_root / "morpheus-origin-prefix.safetensors"
    save_receipt = backend.save_prefix(prefix_path, trained)
    del trained
    reloaded = backend.load_prefix(prefix_path)
    restarted = backend.generate(PUBLIC_QUERY, prefix=reloaded)
    frozen_after = all(
        parameter.requires_grad is False and parameter.grad is None
        for parameter in backend.model.parameters()
    )

    result = {
        "activation_delta_nonzero": memory.activation_delta_norm > 0.0,
        "activation_delta_norm": memory.activation_delta_norm,
        "base_model_frozen_before": frozen_before,
        "base_model_frozen_after": frozen_after,
        "baseline_output": baseline.text,
        "initial_loss": initial_loss,
        "final_loss": final_loss,
        "gradient_norm": gradient_norm,
        "memory_output": memory.text,
        "model_linears_dequantized_in_memory": backend.replaced_fp8_linears,
        "no_memory_text_in_public_query": EVENT not in PUBLIC_QUERY and TARGET.strip() not in PUBLIC_QUERY,
        "prefix_receipt": save_receipt,
        "public_prompt_token_ids_sha256": memory.public_prompt_token_ids_sha256,
        "public_prompt_tokens_identical": (
            baseline.public_prompt_token_ids_sha256
            == memory.public_prompt_token_ids_sha256
            == restarted.public_prompt_token_ids_sha256
        ),
        "reload_output_exact": memory.text == restarted.text,
        "reloaded_output": restarted.text,
        "target_recalled": TARGET.strip() in memory.text,
    }
    # Persist only this compact development result; no model weights or prompt
    # embeddings are written.
    (output_root / "soft-prefix-origin-probe.json").write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if all(
        (
            result["activation_delta_nonzero"],
            result["base_model_frozen_before"],
            result["base_model_frozen_after"],
            result["no_memory_text_in_public_query"],
            result["public_prompt_tokens_identical"],
            result["reload_output_exact"],
            result["target_recalled"],
        )
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
