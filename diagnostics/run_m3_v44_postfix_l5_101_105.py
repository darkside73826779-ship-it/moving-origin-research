#!/usr/bin/env python3
"""One-pass post-fix L5 development diagnostic for seeds 101 through 105."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import m3_harness as m3  # noqa: E402


def main() -> int:
    output = {
        "scope": "development_postfix_l5_only",
        "reason": "L5 exact-control implementation changed after the preserved full pass",
        "seeds": {},
    }
    failed = False
    for seed in m3.DEVELOPMENT_SEEDS:
        started = time.monotonic()
        result = m3.run_l5(seed)
        output["seeds"][str(seed)] = {
            "elapsed_seconds": time.monotonic() - started,
            "verdict": result["verdict"],
            "kill_reasons": result.get("kill_reasons", []),
            "instrument_failure_reasons": result.get(
                "instrument_failure_reasons", []
            ),
            "permuted_plus_one_p_value": result["permuted"][
                "plus_one_p_value"
            ],
            "exact_controls": {
                key: result[key]
                for key in (
                    "fair_naive",
                    "frozen",
                    "oracle",
                    "shuffled",
                    "full_scan",
                    "empty",
                )
            },
        }
        failed |= result["verdict"] != "PASS"
    target = Path(__file__).with_name("m3_v44_postfix_l5_101_105.json")
    target.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
