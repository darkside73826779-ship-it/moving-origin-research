# Coordinator Return — M4 WSL2 Test-bed Reproducibility Package

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

The official M4 WSL2 pre-execution test-bed designation is supplemented by a public environment lock and operating runbook:

- `specs/data/m4_wsl2_preexecution_testbed_environment_v1.json`
- `specs/data/m4_wsl2_preexecution_testbed_environment_v1.json.sha256`
- `docs/m4_wsl2_preexecution_testbed_runbook.md`
- `docs/m4_wsl2_preexecution_testbed_setup_command_index.md`
- `tools/testbed/requirements-m4-wsl2-diagnostic.txt`
- `tools/testbed/setup_m4_wsl2_nvidia_container_runtime.sh`
- `tools/testbed/setup_m4_wsl2_diagnostic_runtime.sh`
- `tools/testbed/verify_m4_wsl2_testbed.sh`
- `tools/testbed/run_m4_wsl2_governed_image_gpu_smoke.sh`

The package fixes the host, WSL, GPU, Docker, NVIDIA runtime, governed OCI image, governed-image packages, local diagnostic packages, required environment switches, public model identity, dual-load controls, expected observations, private-variable names, test sequence, and evidence boundaries. It publishes no private value or path.

The governed OCI runtime and local synthetic diagnostic runtime are explicitly separated. The package changes no M4 scientific, tokenizer, custody, executable, scoring, state, or provenance artifact and authorizes no held operation.
