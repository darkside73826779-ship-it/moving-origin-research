# M4 WSL2 Test-bed Setup Command Index

**Date:** 2026-08-21

**Regime:** B

This is the ordered list of setup and verification scripts used to reproduce
the initial test-bed environment. System-mutating scripts are host setup only
and must never run inside a governed M4 operation.

The immutable setup baseline is annotated tag
`m4-wsl2-preexecution-testbed-v1.2` (tag object
`1994709b41c8e108e0b6f9a15936681f596823af`, peeled commit
`11ea682a7f0fadfa1437a12d882402d90ffd0579`). A future audited package should
use the recommended tag `m4-wsl2-preexecution-testbed-v1.3`; do not cite a
moving branch head as the reproduced version.

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
4. Activate that exact environment in the current shell:
   `source ABSOLUTE_VENV_PATH/bin/activate`.
5. From the clean immutable checkout and locked diagnostic environment, run the
   custody-free readiness command before setting any private variable:
   `python3 -I tools/testbed/run_m4_wsl2_audit_readiness.py`.
6. Set process-local private roots for the released checkout, output stage, and
   two model copies. Never place their values in Git, logs, shell history, or
   public reports.
7. Set the required local compatibility controls:
   `export VLLM_USE_V2_MODEL_RUNNER=0` and
   `export VLLM_USE_FLASHINFER_SAMPLER=0`. The first selects vLLM's V1 runner
   because V2 fails with `RuntimeError: UVA is not available`; it does not
   change the model version or governed OCI runtime.
8. Run the private-input identity/readiness verifier only under separately
   applicable custody authority:
   `tools/testbed/verify_m4_wsl2_testbed.sh`
9. The one-command readiness already runs the governed-image GPU-visibility
   smoke. `tools/testbed/run_m4_wsl2_governed_image_gpu_smoke.sh` remains the
   exact standalone equivalent for focused diagnosis.
10. Run the exact custody-free mount-smoke and committed no-custody wrapper from
   the currently reviewed M4 contract. Those commands remain contract-owned
   and are intentionally not duplicated by this setup index.
11. Run the synthetic dual-model probe using the controls in
   `specs/data/m4_wsl2_preexecution_testbed_environment_v1.json`; publish only
   sanitized aggregates permitted by the runbook.

Docker itself was supplied by the existing WSL2/Docker Desktop integration and
is therefore a prerequisite, not installed by these scripts. Model acquisition
is also out of scope: the scripts validate operator-supplied private roots and
never download, search for, or synthesize model or tokenizer artifacts.

Any downloadable setup bundle added later must be tag-derived and publish both
its exact archive-byte SHA-256 and a canonical LF manifest SHA-256, as specified
in `specs/data/m4_wsl2_audit_readiness_contract_v1.json`.
