# ARCHITECT → WORKFLOW COORDINATOR: M4 WSL2 two-axis and dependency-lock package

Date: 2026-08-22

Regime: B

Terminal state: COMPLETE — DIAGNOSTIC INFRASTRUCTURE ONLY

## Result

The retained public v1 report is committed byte-for-byte at 123,507 bytes and SHA-256 `7dde0d1587b9205a339776ad04daecfe2bf160e8ecb9ff0504335f91b57a10bc` `[PROPOSED]`. It remains `BLOCKED / OUTPUT_DIGEST_MISMATCH`; neither the v1 schema nor v1 producer was changed.

The prospective v2 projection reports independent axes `[PROPOSED]`:

- structural `PASS` over the retained identity/root enforcement, completed import/load/run, 30-second duration, 164 produced/consumed windows, zero drops, FIFO, overlap, backpressure, and zero-MiB cleanup `[PROPOSED]`;
- replica `MISMATCH` over 164 comparisons, 80 agreements, and 84 mismatches, with an ordered sanitized mismatch-ordinal list and its canonical digest `[PROPOSED]`.

The contract states that any byte-identical-replica consumer stops on `MISMATCH` `[PROPOSED]`. Neither axis is equivalence, qualification, scoring, readiness, or science.

The text-only setup now verifies resolver-produced `torchaudio==2.11.0` and the exact `libcudart.so.13` incompatibility marker, removes only that unused package, asserts absence, imports `vllm`, and verifies all unchanged direct pins `[PROPOSED]`. Any identity/outcome drift stops; there is no fallback.

## Immutable identities

- Base/routed audit-readiness checkout: `79473c93900405177e071d6eb56824ad1dcbf5e6`
- Substantive result: `8c303b3262d8ea7640e06fe23671f999f5e01d2c`
- Branch: `architect/m4-wsl2-two-axis-dependency-lock`
- Complete ordered package inventory: `specs/data/m4_wsl2_two_axis_dependency_lock_package_v1.json` and adjacent sidecar

## Verification

- Exact legacy SHA and v1 schema validation: PASS.
- Deterministic v2 derivation and schema validation: PASS.
- MATCH, MISMATCH, NOT_RUN, structural-failure, cleanup-failure, count, and stop projection tests: PASS.
- Dependency identity/exclusion and residual-package failure tests: PASS.
- Required vLLM-import invocation and locked-version checks: PASS through isolated verifier tests.
- Focused plus pre-existing testbed suite in pinned network-disabled, read-only governed OCI runtime: 28/28 PASS.
- Shell syntax: PASS.
- Complete eighteen-entry path/mode/blob/raw-SHA-256/byte package inventory: PASS.
- No model rerun, dependency/model network access, protected input, custody, scoring, qualification, science, state/provenance mutation, production merge, readiness declaration, or gate decision occurred.

Ownership transfers only after Coordinator acknowledges this direct handoff.
