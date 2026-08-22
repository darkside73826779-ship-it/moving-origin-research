#!/usr/bin/env python3
"""Non-executing beta wrapper: it must stop before any runtime access."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.m4_final_prescoring_crash_cart import CrashCartError, execution_guard

def main() -> int:
    try: execution_guard(False)
    except CrashCartError as exc:
        print(exc, file=sys.stderr); return 2
    return 2
if __name__ == "__main__": raise SystemExit(main())
