# Rebecca Designation — Official M4 WSL2 Pre-execution Test Bed

**Date:** 2026-08-21

**Regime:** B

**Status:** ACTIVE FOR BOUNDED PRE-EXECUTION TESTING

Rebecca designates the established local WSL2 environment as the official M4 pre-execution test bed for implementation and executability gap discovery. This designation lets the established roles use one verified environment proactively before a governed operation, while preserving all role, custody, scientific, and gate boundaries.

Verified public environment facts:

- Ubuntu 24.04 under WSL2 with an NVIDIA RTX 5080 exposing 16,303 MiB VRAM.
- Docker client/server 29.1.3 with NVIDIA Container Toolkit 1.20.0.
- The exact contract-pinned Linux/amd64 vLLM image is locally available and has demonstrated GPU access.
- Two byte-equivalent local Qwen model copies load concurrently in the local diagnostic runtime.
- A synchronized 30.032-second synthetic run processed 174 of 174 identical windows through both models with zero drops or reordering, identical outputs, execution overlap for every pair, maximum launch skew 0.300 ms, peak 11,275 MiB VRAM, and cleanup to 0 MiB.

Authorized test-bed uses:

- Exact pinned-image, Docker runtime, and GPU-visibility checks.
- Custody-free OCI mount/topology smoke tests, including the governed read-only repository plus nested writable output topology.
- Exact test-container execution with synthetic or committed public fixtures.
- Pre-import, runtime, executable-package, schema, sidecar, and raw-identity checks.
- Negative mount, path, byte-domain, launcher, and runtime cases that perform no governed custody access.
- Synthetic dual-load, identical-input, bounded-backpressure, ordering, overlap, output-agreement, cleanup, and implementation-gap diagnostics.

Required operating boundaries:

- Repository mounts remain read-only except for an exact separately mounted output stage; network remains disabled where the governing contract requires it.
- Test-bed findings are advisory executability evidence until admitted through the established ARCHITECT, TASK BUILDER, and persistent-CRITIC route.
- Private custody values and paths remain process-local coordination data and may never enter Git, handoffs, logs, public artifacts, or diagnostic reports.
- Synthetic dual-model results do not constitute scientific evidence, qualification, scoring, or a gate verdict.
- Same-role subagents may perform bounded isolated verification lanes, but each primary role retains integration, verdict, publication, and handoff accountability.

This designation does not authorize a materializer retry, real custody/model/tokenizer access outside an exact operation release, inference or serving qualification, Q2/EF3, diagnostics scoring, protected or hold-out seeds, scientific changes, STATE or provenance mutation, model/tokenizer publication, merge, rerun, or gate decision.

Current M4 application: the feasibility-proven nested-output mount correction and its exact custody-free mount-smoke gate may use this test bed before publication and before any future single materializer release. The single bounded materialization operation remains unconsumed.
