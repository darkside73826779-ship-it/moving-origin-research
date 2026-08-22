#!/usr/bin/env bash
# Date: 2026-08-21
# Regime: B
# Host setup only. Never run inside a governed M4 operation.
set -euo pipefail

expected_version="24.04"
actual_version="$(. /etc/os-release && printf '%s' "$VERSION_ID")"
if [[ "$actual_version" != "$expected_version" ]]; then
  echo "STOP: expected Ubuntu ${expected_version}" >&2
  exit 2
fi

keyring=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
source_list=/etc/apt/sources.list.d/nvidia-container-toolkit.list

curl --fail --silent --show-error --location \
  https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor --yes --output "$keyring"
curl --fail --silent --show-error --location \
  https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed "s#deb https://#deb [signed-by=${keyring}] https://#g" \
  | sudo tee "$source_list" >/dev/null

sudo apt-get update
sudo apt-get install --yes \
  libnvidia-container-tools=1.20.0-1 \
  nvidia-container-toolkit-base=1.20.0-1 \
  nvidia-container-toolkit=1.20.0-1
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

nvidia-ctk --version
docker version --format 'CLIENT={{.Client.Version}} SERVER={{.Server.Version}} OS={{.Server.Os}} ARCH={{.Server.Arch}}'
