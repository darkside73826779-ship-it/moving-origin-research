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
try:
    actual = metadata.version("torchaudio")
except metadata.PackageNotFoundError as exc:
    raise SystemExit("STOP: expected incompatible torchaudio distribution absent before exclusion") from exc
if actual != "2.11.0":
    raise SystemExit(f"STOP: unexpected torchaudio identity: {actual}")
try:
    import torchaudio  # noqa: F401
except BaseException as exc:
    if "libcudart.so.13" not in str(exc):
        raise SystemExit("STOP: torchaudio incompatibility marker mismatch") from exc
else:
    raise SystemExit("STOP: torchaudio unexpectedly importable; lock requires review")
PY
"${venv_path}/bin/python" -m pip uninstall --yes torchaudio
"${venv_path}/bin/python" "${script_dir}/verify_m4_wsl2_text_only_runtime.py"
