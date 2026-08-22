# M4 WSL2 Test-bed Setup Command Index

**Date:** 2026-08-21

**Regime:** B

This is the ordered list of setup and verification scripts used to reproduce
the initial test-bed environment. System-mutating scripts are host setup only
and must never run inside a governed M4 operation.

The public model under test is `Qwen/Qwen3-4B-Instruct-2507-FP8` at immutable
revision `8591804019c8b22094c3b5b4454e0edc05dffc98`, quantization
`OFFICIAL_QWEN_FP8_E4M3`. Its public weight/tokenizer identities are fixed in
the environment lock. Only the two local root paths remain private.

1. Install/configure the exact NVIDIA container runtime inside Ubuntu WSL2:
   `tools/testbed/setup_m4_wsl2_nvidia_container_runtime.sh`
2. Restart Docker as performed by that script, then close/reopen the invoking
   shell only if its Docker connection has not refreshed.
3. Create the exact local synthetic-diagnostic virtual environment:
   `tools/testbed/setup_m4_wsl2_diagnostic_runtime.sh ABSOLUTE_VENV_PATH`
4. Set process-local private roots for the released checkout, output stage, and
   two model copies. Never place their values in Git, logs, shell history, or
   public reports.
5. Set the required local compatibility controls:
   `export VLLM_USE_V2_MODEL_RUNNER=0` and
   `export VLLM_USE_FLASHINFER_SAMPLER=0`. The first selects vLLM's V1 runner
   because V2 fails with `RuntimeError: UVA is not available`; it does not
   change the model version or governed OCI runtime.
6. Run the read-only identity/readiness verifier:
   `tools/testbed/verify_m4_wsl2_testbed.sh`
7. Run the governed-image GPU-visibility smoke:
   `tools/testbed/run_m4_wsl2_governed_image_gpu_smoke.sh`
8. Run the exact custody-free mount-smoke and committed no-custody wrapper from
   the currently reviewed M4 contract. Those commands remain contract-owned
   and are intentionally not duplicated by this setup index.
9. Run the synthetic dual-model probe using the controls in
   `specs/data/m4_wsl2_preexecution_testbed_environment_v1.json`; publish only
   sanitized aggregates permitted by the runbook.

Docker itself was supplied by the existing WSL2/Docker Desktop integration and
is therefore a prerequisite, not installed by these scripts. Model acquisition
is also out of scope: the scripts validate operator-supplied private roots and
never download, search for, or synthesize model or tokenizer artifacts.
