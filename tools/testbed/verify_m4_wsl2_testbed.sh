#!/usr/bin/env bash
# Date: 2026-08-21
# Regime: B
# Read-only readiness verification. Prints no private environment value.
set -euo pipefail

image='docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6'
expected_kernel='6.18.33.2-microsoft-standard-WSL2'

[[ "$(uname -r)" == "$expected_kernel" ]] || {
  echo "STOP: kernel mismatch" >&2
  exit 2
}

gpu_line="$(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits)"
[[ "$gpu_line" == 'NVIDIA GeForce RTX 5080, 610.88, 16303' ]] || {
  echo "STOP: GPU identity mismatch" >&2
  exit 2
}

docker_line="$(docker version --format 'CLIENT={{.Client.Version}} SERVER={{.Server.Version}} OS={{.Server.Os}} ARCH={{.Server.Arch}}')"
[[ "$docker_line" == 'CLIENT=29.1.3 SERVER=29.1.3 OS=linux ARCH=amd64' ]] || {
  echo "STOP: Docker identity mismatch" >&2
  exit 2
}

image_id="$(docker image inspect "$image" --format '{{.Id}}|{{.Os}}|{{.Architecture}}')"
[[ "$image_id" == 'sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6|linux|amd64' ]] || {
  echo "STOP: image identity mismatch" >&2
  exit 2
}

for variable in MOR_RELEASED_CHECKOUT MOR_TOKENIZER_OUTPUT_STAGE MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1 MOR_TESTBED_MODEL_A MOR_TESTBED_MODEL_B; do
  if [[ -z "${!variable:-}" ]]; then
    echo "STOP: required private variable absent: ${variable}" >&2
    exit 2
  fi
  value="${!variable}"
  if [[ "$value" != /* || ! -d "$value" || -L "$value" ]]; then
    echo "STOP: required private directory invalid: ${variable}" >&2
    exit 2
  fi
done

custody_record="${MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1}/.mor-custody-record-v1.json"
if [[ ! -f "$custody_record" || -L "$custody_record" ]]; then
  echo 'STOP: fixed private custody record absent or linked' >&2
  exit 2
fi

if find "$MOR_TOKENIZER_OUTPUT_STAGE" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
  echo 'STOP: output stage must be empty' >&2
  exit 2
fi

verify_model_identity() {
  local root="$1"
  [[ "$(stat -c '%s' "$root/model.safetensors")" == '5190053264' ]]
  [[ "$(stat -c '%s' "$root/tokenizer.json")" == '11422654' ]]
  [[ "$(stat -c '%s' "$root/tokenizer_config.json")" == '9377' ]]
  [[ "$(sha256sum "$root/model.safetensors" | cut -d' ' -f1)" == 'b6154d74332140fd6dfbfbe70bbb3650dd6955861132bd59dda6789e6322b485' ]]
  [[ "$(sha256sum "$root/tokenizer.json" | cut -d' ' -f1)" == 'aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4' ]]
  [[ "$(sha256sum "$root/tokenizer_config.json" | cut -d' ' -f1)" == 'a62ff0a2472a0fa1b8eaabcb57c59b58afa42a22831dc141400b6e0cf2b65ce3' ]]
}

verify_model_identity "$MOR_TESTBED_MODEL_A" || {
  echo 'STOP: model A public identity mismatch' >&2
  exit 2
}
verify_model_identity "$MOR_TESTBED_MODEL_B" || {
  echo 'STOP: model B public identity mismatch' >&2
  exit 2
}

[[ "${VLLM_USE_V2_MODEL_RUNNER:-}" == '0' ]] || {
  echo "STOP: V1 runner compatibility override absent" >&2
  exit 2
}
[[ "${VLLM_USE_FLASHINFER_SAMPLER:-}" == '0' ]] || {
  echo "STOP: sampler compatibility setting absent" >&2
  exit 2
}

"$(command -v python)" "$(dirname -- "${BASH_SOURCE[0]}")/verify_m4_wsl2_text_only_runtime.py" || {
  echo 'STOP: text-only dependency closure invalid' >&2
  exit 2
}

echo 'M4 WSL2 test-bed readiness verified; private values not emitted'
