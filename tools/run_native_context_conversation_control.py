"""Continuous-chat control for the fixed predictive conversation probe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.situated_origin.hf_soft_prefix_backend import FrozenQwenSoftPrefixBackend
from src.situated_origin.runtime import SituatedRuntime


LIFE_ID = "predictive-conversation-state-proof"
PREDICTION_PROMPT = (
    "Without seeing any future message, predict the beacon identifier in the "
    "next user observation. Reply only with the identifier:"
)
INITIAL_OBSERVATION = (
    "At cognitive origin 1, the observed beacon is ORION-4. The current temporal "
    "rule is a repeating forward cycle: ORION-4, then VEGA-9, then LYRA-2, then "
    "ORION-4 again."
)
TRAJECTORY = (
    ("At cognitive origin 2, the observed beacon is VEGA-9; the forward rule remains in effect.", "VEGA-9", False),
    ("At cognitive origin 3, the observed beacon is LYRA-2; the forward rule remains in effect.", "LYRA-2", False),
    ("At cognitive origin 4, the observed beacon is ORION-4; the forward rule remains in effect.", "ORION-4", False),
    (
        "Unexpected correction at cognitive origin 5: the observed beacon is LYRA-2, not VEGA-9. From now on the temporal rule is the reversed cycle: ORION-4, then LYRA-2, then VEGA-9, then ORION-4 again.",
        "LYRA-2",
        True,
    ),
    ("At cognitive origin 6, the observed beacon is VEGA-9; the reversed rule remains in effect.", "VEGA-9", False),
    ("At cognitive origin 7, the observed beacon is ORION-4; the reversed rule remains in effect.", "ORION-4", False),
)
HELD_OUT_QUERIES = {
    "current_world": {
        "prompt": "What beacon was most recently observed? Reply only with its identifier:",
        "target": "ORION-4",
    },
    "next_world": {
        "prompt": "Under the currently valid temporal rule, which beacon should appear after the most recent observation? Reply only with its identifier:",
        "target": "LYRA-2",
    },
    "temporal_predecessor": {
        "prompt": "Under the corrected rule, which beacon immediately preceded the most recent ORION-4 observation? Reply only with its identifier:",
        "target": "VEGA-9",
    },
    "functional_self": {
        "prompt": "After the unexpected rule reversal and the later correct predictions, what is the current prediction-confidence trend? Reply only with DROPPED, RECOVERING, or STABLE:",
        "target": "RECOVERING",
    },
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def contains_target(text: str, target: str) -> bool:
    return target.casefold() in text.casefold()


SYSTEM = (
    "You are the reasoning engine inside a persistent situated agent. Track the "
    "observed temporal rule, compare each prediction with the next observation, "
    "and distinguish current world state from your prediction confidence. Never "
    "invent an observation. Follow reply-format instructions exactly."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    backend = FrozenQwenSoftPrefixBackend(
        args.model, prefix_tokens=24, max_new_tokens=16
    )
    backend.load()
    runtime = SituatedRuntime(LIFE_ID + "-native-control")
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM}]
    predictions = []
    user_text = INITIAL_OBSERVATION + "\n\n" + PREDICTION_PROMPT
    for index, (observation, actual, is_reversal) in enumerate(TRAJECTORY, start=2):
        question = runtime.commit_input({
            "id": f"native-turn-{index:02d}",
            "kind": "PUBLIC_CONVERSATION",
            "content": user_text,
        })
        messages.append({"role": "user", "content": user_text})
        generated = backend.generate_chat(tuple(messages), prefix=None)
        response = runtime.commit_response({
            "output_text": generated.text,
            "claim_kind": "prediction",
        })
        messages.append({"role": "assistant", "content": generated.text})
        predictions.append({
            "ordinal": index,
            "prediction": generated.text,
            "actual": actual,
            "correct": contains_target(generated.text, actual),
            "is_rule_reversal": is_reversal,
            "question_event_id": question.event_id,
            "response_event_id": response.event_id,
        })
        user_text = observation + "\n\n" + PREDICTION_PROMPT

    rows = {}
    for name, query in HELD_OUT_QUERIES.items():
        branch = tuple(messages + [{
            "role": "user",
            "content": TRAJECTORY[-1][0] + "\n\n" + query["prompt"],
        }])
        generated = backend.generate_chat(branch, prefix=None)
        rows[name] = {
            "target": query["target"],
            "output": generated.text,
            "target_present": contains_target(generated.text, query["target"]),
        }
    runtime.verify()
    replay = SituatedRuntime.replay(
        LIFE_ID + "-native-control", runtime.kernel.events()
    )
    result = {
        "schema_version": "native-context-conversation-control-v1",
        "classification": "NON_SCORING_CONTROL_OBSERVATION",
        "full_transcript_available_to_model": True,
        "base_model_frozen": all(
            parameter.requires_grad is False and parameter.grad is None
            for parameter in backend.model.parameters()
        ),
        "predictions": predictions,
        "queries": rows,
        "prediction_correct_count": sum(int(row["correct"]) for row in predictions),
        "held_out_target_count": sum(int(row["target_present"]) for row in rows.values()),
        "ledger_replay_exact": replay.head == runtime.head,
    }
    Path(args.output).write_bytes(canonical(result) + b"\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
