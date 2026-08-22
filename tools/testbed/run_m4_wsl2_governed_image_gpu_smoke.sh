#!/usr/bin/env bash
# Date: 2026-08-21
# Regime: B
# GPU-visibility smoke only. No custody or repository mount.
set -euo pipefail

image='docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6'
docker run --rm --pull=never --platform linux/amd64 --network none \
  --gpus all --read-only --cap-drop ALL \
  --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m,mode=0700 \
  --entrypoint python3 "$image" -I -c \
  'import torch; assert torch.cuda.is_available(); print(torch.__version__, torch.cuda.get_device_name(0))'
