#!/usr/bin/env python3
"""Fail-closed verifier for the pinned text-only WSL2 diagnostic runtime.

Date: 2026-08-22
Regime: B
"""
from __future__ import annotations

import importlib
import importlib.metadata as metadata
import platform

EXPECTED = {
    "jsonschema": "4.26.0",
    "numpy": "2.3.5",
    "safetensors": "0.8.0",
    "tokenizers": "0.22.2",
    "torch": "2.13.0+cu132",
    "transformers": "5.15.1",
    "vllm": "0.27.1",
}


def verify() -> None:
    if platform.python_version() != "3.12.3":
        raise RuntimeError("PYTHON_VERSION_MISMATCH")
    try:
        metadata.version("torchaudio")
    except metadata.PackageNotFoundError:
        pass
    else:
        raise RuntimeError("TORCHAUDIO_EXCLUSION_FAILED")
    for name, version in EXPECTED.items():
        if metadata.version(name) != version:
            raise RuntimeError(f"LOCKED_VERSION_MISMATCH:{name}")
    importlib.import_module("vllm")


if __name__ == "__main__":
    verify()
    print("text-only diagnostic runtime verified")
