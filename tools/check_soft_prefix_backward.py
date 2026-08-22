"""One-shot local feasibility gate for activation-level soft-prefix learning.

Loads a frozen local causal language model, performs one teacher-forced forward
and backward pass through an injected prefix tensor, and emits a small JSON
result.  It never writes model or tokenizer data.
"""

from __future__ import annotations

import argparse
import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def dequantize_fp8_linears(module: torch.nn.Module) -> int:
    """Replace fine-grained FP8 linears with frozen BF16 linears in place."""

    from transformers.integrations.finegrained_fp8 import FP8Linear

    replaced = 0
    for name, child in list(module.named_children()):
        if isinstance(child, FP8Linear):
            rows, columns = child.weight.shape
            block_rows, block_columns = child.block_size
            if rows % block_rows or columns % block_columns:
                raise RuntimeError("FP8_BLOCK_SHAPE_INVALID")
            replacement = torch.nn.Linear(
                columns,
                rows,
                bias=child.bias is not None,
                device=child.weight.device,
                dtype=torch.bfloat16,
            )
            with torch.no_grad():
                blocks = child.weight.float().reshape(
                    rows // block_rows,
                    block_rows,
                    columns // block_columns,
                    block_columns,
                )
                scales = child.weight_scale_inv.float().reshape(
                    rows // block_rows, columns // block_columns
                )
                replacement.weight.copy_(
                    (blocks * scales[:, None, :, None])
                    .reshape(rows, columns)
                    .to(torch.bfloat16)
                )
                if child.bias is not None:
                    replacement.bias.copy_(child.bias.to(torch.bfloat16))
            replacement.requires_grad_(False)
            module._modules[name] = replacement
            replaced += 1
            del child, blocks, scales
            torch.cuda.empty_cache()
        else:
            replaced += dequantize_fp8_linears(child)
    return replaced


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--prefix-tokens", type=int, default=4)
    parser.add_argument("--dequantize-fp8", action="store_true")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(
        args.model, local_files_only=True, trust_remote_code=False, use_fast=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        local_files_only=True,
        trust_remote_code=False,
        torch_dtype="auto",
        device_map="cuda",
        attn_implementation="eager",
        low_cpu_mem_usage=True,
    )
    model.eval()
    replaced_fp8_linears = dequantize_fp8_linears(model) if args.dequantize_fp8 else 0
    for parameter in model.parameters():
        parameter.requires_grad_(False)

    encoded = tokenizer(
        "Remember that the project codename is MORPHEUS-731.",
        return_tensors="pt",
        add_special_tokens=True,
    )
    input_ids = encoded["input_ids"].to("cuda")
    token_embeddings = model.get_input_embeddings()(input_ids).detach()
    hidden_size = token_embeddings.shape[-1]
    # A zero vector is outside the model's embedding manifold and can produce
    # undefined gradients through quantized-model RMS normalization.  A real
    # experience prefix starts from event-token embeddings, so the feasibility
    # gate uses that same valid initialization domain.
    seed = token_embeddings[:, : args.prefix_tokens]
    if seed.shape[1] < args.prefix_tokens:
        seed = token_embeddings.mean(dim=1, keepdim=True).expand(
            -1, args.prefix_tokens, -1
        )
    prefix = torch.nn.Parameter(seed.detach().clone())
    inputs_embeds = torch.cat((prefix, token_embeddings), dim=1)
    attention_mask = torch.ones(
        inputs_embeds.shape[:2], device=inputs_embeds.device, dtype=torch.long
    )
    labels = torch.cat(
        (
            torch.full(
                (1, args.prefix_tokens),
                -100,
                device=input_ids.device,
                dtype=input_ids.dtype,
            ),
            input_ids,
        ),
        dim=1,
    )
    output = model(
        inputs_embeds=inputs_embeds,
        attention_mask=attention_mask,
        labels=labels,
        use_cache=False,
    )
    output.loss.backward()

    prefix_grad_norm = float(prefix.grad.float().norm().item()) if prefix.grad is not None else 0.0
    prefix_grad_finite = bool(
        prefix.grad is not None and torch.isfinite(prefix.grad).all().item()
    )
    model_grad_count = sum(parameter.grad is not None for parameter in model.parameters())
    print(
        json.dumps(
            {
                "device": torch.cuda.get_device_name(0),
                "hidden_size": int(hidden_size),
                "loss": float(output.loss.detach().float().item()),
                "model_grad_count": model_grad_count,
                "model_parameters_frozen": all(
                    parameter.requires_grad is False for parameter in model.parameters()
                ),
                "prefix_dtype": str(prefix.dtype),
                "prefix_grad_nonzero": prefix_grad_norm > 0.0,
                "prefix_grad_finite": prefix_grad_finite,
                "prefix_grad_norm": prefix_grad_norm,
                "prefix_tokens": args.prefix_tokens,
                "replaced_fp8_linears": replaced_fp8_linears,
            },
            sort_keys=True,
        )
    )
    return 0 if prefix_grad_finite and prefix_grad_norm > 0.0 and model_grad_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
