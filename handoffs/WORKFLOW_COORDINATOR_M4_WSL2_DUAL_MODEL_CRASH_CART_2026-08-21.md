# WORKFLOW COORDINATOR M4 WSL2 Dual-model Crash-cart

**Date:** 2026-08-21

**Regime:** B

**Base authority:** `coordinator/m4-wsl2-preexecution-testbed` at
`0631a019a153ec89312938982c007cf94dd3f03e`

## Scope and status

This package closes the custody-free, reproducible 30-second dual-model
crash-cart gap in the M4 pre-execution test bed. The measured disposition is
`PASS` for local synthetic readiness only. It is not scientific evidence,
authoritative scoring, qualification, a model-selection decision, or authority
to access custody or protected seeds.

## Exact public identity and runtime

- Model: `Qwen/Qwen3-4B-Instruct-2507-FP8`
- Revision: `8591804019c8b22094c3b5b4454e0edc05dffc98`
- Quantization: official Qwen FP8 E4M3
- Required compatibility switches:
  `VLLM_USE_V2_MODEL_RUNNER=0` and
  `VLLM_USE_FLASHINFER_SAMPLER=0`
- Two canonical, non-link, physically distinct local roots are supplied only as
  process-local `MOR_TESTBED_MODEL_A` and `MOR_TESTBED_MODEL_B` values.

## Exact commands

Construction tests, from the released checkout in the locked diagnostic
environment:

```bash
python3 -I -m unittest discover -s tests -t . \
  -p test_m4_wsl2_dual_model_probe.py
```

Measured probe, with the three named process-local variables already set:

```bash
VLLM_USE_V2_MODEL_RUNNER=0 \
VLLM_USE_FLASHINFER_SAMPLER=0 \
python3 -I tools/testbed/run_m4_wsl2_dual_model_probe.py \
  --output "${MOR_TESTBED_REPORT_STAGE}/m4_wsl2_dual_model_probe_report_v1.json"
```

No process-local value may be echoed, traced, or serialized.

## Sanitized measured evidence

- Active producer duration: 30,080,890,088 ns.
- Windows produced/consumed: 173 / 173.
- Dropped windows: 0; FIFO order preserved.
- Concrete full-queue backpressure observations: 164.
- All paired host-call intervals overlapped; this does not assert device-kernel
  overlap.
- All paired output SHA-256 values agreed.
- Maximum launch skew: 369,804 ns.
- Peak reported VRAM: 11,279 MiB.
- Post-cleanup reported VRAM: 0 MiB.
- Exact report SHA-256:
  `1f42c9e4ccc1b140e62e32fedcbf75124fbb514f2ae5129781183da12a8093ac`.

The report serializes only public identity, fixed controls, integer
measurements, counts, booleans, and SHA-256 values. It contains no model root,
private path, prompt text, rendered model output, token array, custody input,
protected seed, or score.

## Limits and holds

The crash-cart verifies repeatable dual residency, identical synthetic fanout,
bounded FIFO backpressure, host-call overlap, digest agreement, and cleanup. It
does not prove device-kernel concurrency or scientific equivalence. All M4
custody, materialization, inference/serving, qualification, diagnostics/scoring,
protected-seed, state/provenance, merge, and gate holds remain unchanged.

## Public-safety classification

Gitleaks reports zero findings. The fixed-regex preflight retains 2,651
duplicate scan-domain findings. Of those, 2,624 are the measured report's 1,312
matches repeated across resulting-file and combined-range domains: 1,181 occur
wholly inside integer timing/control measurements and 131 occur wholly inside
declared public SHA-256/model-revision strings. The remaining findings occur
inside the same classes of public immutable identities, byte counts, fixed
controls, synthetic fixture values, or their duplicate combined-patch domain.
They are reproducibility metadata, not personal contact data. Every finding is
retained and manually classified; none is suppressed.
