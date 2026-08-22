# M4 WSL2 two-axis and text-only dependency-lock amendment v1

Date: 2026-08-22

Regime: B

Status: `[PROPOSED]` diagnostic infrastructure only

## Preserved result

`artifacts/m4_wsl2_preexecution_testbed/m4_wsl2_dual_model_probe_report_2026-08-22.json` is preserved at exactly 123,507 raw bytes and SHA-256 `7dde0d1587b9205a339776ad04daecfe2bf160e8ecb9ff0504335f91b57a10bc` `[PROPOSED]`. Its v1 disposition remains `BLOCKED / OUTPUT_DIGEST_MISMATCH`; no field is reinterpreted or replaced.

## Two independent axes

The prospective v2 projection is a deterministic function of the retained v1 bytes `[PROPOSED]`.

- Structural status is `PASS` or `BLOCKED`. The derivation first validates the complete source against the exact bound v1 schema and accepts only its exact failure-code vocabulary. Every valid non-replica v1 failure code projects `BLOCKED`; unknown codes are rejected. `PASS` requires exact identity/root checks already enforced by the v1 producer, successful import/load evidenced by a completed report, at least 30 seconds active duration, a positive paired-window count, produced/consumed/row equality, zero drops, FIFO preservation, overlap on every execution, observed backpressure, no structural failure code, and cleanup at zero reported MiB `[PROPOSED]`.
- Replica consistency is independently `MATCH`, `MISMATCH`, or `NOT_RUN`. It binds compared, agreement, and mismatch counts; ordered mismatch ordinals; and SHA-256 of their canonical JSON bytes `[PROPOSED]`.
- The v2 schema enforces status/failure/count/list conditionals. The committed semantic validator additionally enforces count arithmetic, canonical unique ordered in-range mismatch ordinals, their canonical digest, exact source binding, and exact v1 failure-code membership `[PROPOSED]`. A byte-identical-replica consumer calls the single committed guard and receives mandatory `REPLICA_CONSISTENCY_STOP` for every state other than `MATCH`; policy text alone is not authority `[PROPOSED]`. Structural `PASS` does not imply deterministic replica output, equivalence, qualification, scoring fitness, or a scientific claim.

The retained projection is structural `PASS` and replica `MISMATCH`: 164 compared, 80 agreements, and 84 mismatches `[PROPOSED]`. It preserves the full synchronized transport/load evidence while retaining the legacy overall BLOCK.

## Dependency exclusion

The direct requirements remain unchanged. Setup must observe `torchaudio==2.11.0`, require its exact `libcudart.so.13` incompatibility marker beside `torch==2.13.0+cu132`, remove only `torchaudio`, assert the distribution is absent, import `vllm`, and verify every existing direct pin `[PROPOSED]`. Any unexpected identity or outcome stops. No alternate package, floating version, index change, retry, or adaptive fallback is allowed `[PROPOSED]`.

## Evidence boundary

The projection is derived from public sanitized bytes; it does not rerun a model. No protected seed, custody value, prompt text, token array, private path, scoring input, qualification result, scientific conclusion, production merge, readiness decision, or gate decision is authorized.
