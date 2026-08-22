# M4 WSL2 Pre-execution Test-bed Runbook

**Date:** 2026-08-21

**Regime:** B

**Authority:** `coordinator/m4-wsl2-preexecution-testbed`

## Purpose and evidence boundary

This runbook reproduces the official M4 pre-execution test bed. It supports pinned-image verification, custody-free OCI topology smoke tests, committed synthetic tests, dual-model readiness, bounded-backpressure diagnostics, and implementation-gap discovery. It does not authorize scientific scoring, protected seeds, governed custody access, materializer retry, or a gate decision.

The canonical dependency and identity lock is `specs/data/m4_wsl2_preexecution_testbed_environment_v1.json`. Private paths and custody values are deliberately absent. Operators supply them process-locally through the named environment variables and must never print or commit their values.

The model under test is the public identity
`Qwen/Qwen3-4B-Instruct-2507-FP8` at immutable revision
`8591804019c8b22094c3b5b4454e0edc05dffc98`, using the official FP8 E4M3
artifact. The environment lock binds its exact public weight, tokenizer, and
tokenizer-configuration sizes and SHA-256 values; only local root paths remain
private.

## Host prerequisites

1. Windows 11 Pro build 26200 with WSL package 2.7.12.0.
2. Ubuntu 24.04.4 LTS under WSL2 kernel 6.18.33.2.
3. NVIDIA RTX 5080 with driver 610.88 and 16,303 MiB VRAM.
4. Docker client/server 29.1.3 configured for the NVIDIA runtime.
5. NVIDIA Container Toolkit 1.20.0.
6. The exact Linux/amd64 OCI platform digest in the environment lock must already exist locally. Acquisition is outside this test-bed runbook.

Verify without mutation:

```bash
uname -r
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits
docker version --format 'CLIENT={{.Client.Version}} SERVER={{.Server.Version}} OS={{.Server.Os}} ARCH={{.Server.Arch}}'
nvidia-ctk --version
docker image inspect docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6
```

Every mismatch is a test-bed readiness failure. Do not install, pull, upgrade, or substitute dependencies inside a governed operation.

## Runtime separation

The test bed has two deliberately separate runtimes:

- The governed OCI runtime is the exact pinned vLLM 0.10.2 image. M4 executable tests, mount smoke, and any separately released materializer invocation use this runtime only.
- The local WSL diagnostic virtual environment uses vLLM 0.27.1 for synthetic dual-model readiness. Under the verified WSL2 configuration, its V2 model runner fails because UVA is unavailable. Set `VLLM_USE_V2_MODEL_RUNNER=0` and `VLLM_USE_FLASHINFER_SAMPLER=0`; do not interpret this local runtime as the governed materializer runtime.

The first setting is a mandatory runner-compatibility override: it selects
vLLM's working V1 model runner after the V2 runner produces
`RuntimeError: UVA is not available`. “V1” here names the vLLM runner path; it
does not change the candidate model version, model bytes, tokenizer identity,
or the separately pinned governed OCI runtime. A readiness report must record
the two settings and selected runner so a replacement environment does not
silently regress to V2.

## Private inputs

Set these only in the process that needs them:

```text
MOR_RELEASED_CHECKOUT
MOR_TOKENIZER_OUTPUT_STAGE
MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1
MOR_TESTBED_MODEL_A
MOR_TESTBED_MODEL_B
```

All roots must be canonical existing non-link directories. Model A and Model B must independently reproduce the locked public identity. Never echo these variables, include them in command traces, or serialize them into results.

## Required pre-operation sequence

1. Verify the immutable released checkout and complete raw Git-blob inventory.
2. Verify Docker version, platform, and the exact locally present OCI digest with pull disabled.
3. Run the exact committed pre-import test wrapper in the pinned image with a read-only repository, no network, bounded private `/tmp`, no custody mount, and no writable output mount.
4. Run the committed custody-free mount-smoke gate. The repository remains read-only; a distinct empty output stage is mounted at the already tracked nested destination; the exact no-access entrypoint exits zero; the stage remains empty.
5. Stop on any mismatch. A materializer may start only under a separate exact release and only after every preceding gate passes.

## Synthetic dual-model readiness sequence

1. Verify both private model roots against the locked model identity.
2. Set the two required vLLM environment switches.
3. Load two independent model/runtime instances with the exact controls in the environment lock.
4. Produce synthetic windows into a bounded FIFO with capacity eight and a 5 ms producer interval.
5. For at least 30 seconds, submit each byte-identical prompt to both models through a two-party launch barrier.
6. Record prompt digest, per-model start/end times, launch skew, execution overlap, queue wait, ordering, dropped windows, output agreement, peak VRAM, and post-cleanup VRAM.
7. PASS requires at least 30 active seconds, zero drops, exact order, overlap for every pair, producer backpressure, and cleanup to zero reported VRAM. Output agreement is reported separately and is not a scientific score.

## Reproducibility report

Each report must contain only public environment versions, public model identity, test controls, aggregate timing/memory observations, and PASS/BLOCKED status. It must state `synthetic_only=true`, `authoritative_scoring=false`, `protected_seed_access=false`, and `scientific_evidence=false`. Private paths, prompts derived from held data, model bytes, token arrays, environment dumps, and machine identifiers are prohibited.

Before publication, run the repository preflight tool against the exact checkout and complete introduced range, preserve every scanner finding, classify only documented public reproducibility false positives manually, verify remote equality, and return through WORKFLOW COORDINATOR.
