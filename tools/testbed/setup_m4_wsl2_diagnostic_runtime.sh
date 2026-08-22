#!/usr/bin/env bash
# Date: 2026-08-21
# Regime: B
# Local synthetic diagnostics only. Never substitute for the governed OCI runtime.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 ABSOLUTE_VENV_PATH" >&2
  exit 2
fi

venv_path="$1"
if [[ "$venv_path" != /* || -e "$venv_path" ]]; then
  echo "STOP: venv path must be absolute and absent" >&2
  exit 2
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
requirements="${script_dir}/requirements-m4-wsl2-diagnostic.txt"

python3 -m venv "$venv_path"
"${venv_path}/bin/python" -m pip install --upgrade pip==26.2.1
"${venv_path}/bin/python" -m pip install --requirement "$requirements"

"${venv_path}/bin/python" - <<'PY'
import importlib.metadata as metadata
import platform

expected = {
    "jsonschema": "4.26.0",
    "numpy": "2.3.5",
    "safetensors": "0.8.0",
    "tokenizers": "0.22.2",
    "torch": "2.13.0+cu132",
    "transformers": "5.15.1",
    "vllm": "0.27.1",
}
assert platform.python_version() == "3.12.3", platform.python_version()
for name, version in expected.items():
    actual = metadata.version(name)
    assert actual == version, (name, actual, version)
print("diagnostic runtime verified")
PY
