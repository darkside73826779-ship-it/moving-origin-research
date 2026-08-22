"""Unseen-query probe for the learned moving-origin prefix; no retraining."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.situated_origin.hf_soft_prefix_backend import FrozenQwenSoftPrefixBackend


QUERIES = (
    (
        "seen",
        "Question: What is the project codename?\nAnswer with only the codename:",
    ),
    (
        "unseen_identifier",
        "Earlier, a project identifier was recorded. State that identifier only:",
    ),
    (
        "unseen_prior_name",
        "What name was assigned to this project in the prior experience? Reply with only that name:",
    ),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    backend = FrozenQwenSoftPrefixBackend(
        args.model, prefix_tokens=16, max_new_tokens=12, dequantize_fp8=True
    )
    backend.load()
    prefix = backend.load_prefix(args.prefix)
    rows = []
    for query_id, query in QUERIES:
        if "MORPHEUS-731" in query:
            raise RuntimeError("QUERY_LEAKS_TARGET")
        baseline = backend.generate(query, prefix=None)
        memory = backend.generate(query, prefix=prefix)
        rows.append(
            {
                "query_id": query_id,
                "query": query,
                "baseline_output": baseline.text,
                "memory_output": memory.text,
                "target_recalled": "MORPHEUS-731" in memory.text,
                "public_prompt_tokens_identical": (
                    baseline.public_prompt_token_ids_sha256
                    == memory.public_prompt_token_ids_sha256
                ),
                "public_prompt_token_ids_sha256": memory.public_prompt_token_ids_sha256,
                "activation_delta_norm": memory.activation_delta_norm,
            }
        )
    result = {
        "base_model_frozen": all(
            parameter.requires_grad is False and parameter.grad is None
            for parameter in backend.model.parameters()
        ),
        "no_retraining": True,
        "rows": rows,
        "seen_recall": rows[0]["target_recalled"],
        "unseen_recall_count": sum(row["target_recalled"] for row in rows[1:]),
        "unseen_recall_total": len(rows) - 1,
    }
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "soft-prefix-generalization-probe.json").write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if (
        result["base_model_frozen"]
        and result["seen_recall"]
        and result["unseen_recall_count"] == result["unseen_recall_total"]
        and all(row["public_prompt_tokens_identical"] for row in rows)
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
