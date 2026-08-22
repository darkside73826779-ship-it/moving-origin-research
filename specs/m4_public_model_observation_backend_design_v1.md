# M4 public-model non-scoring observation backend design v1

Date: 2026-08-22

Regime: B

Status: DESIGN ONLY — NO RUN AUTHORITY `[PROPOSED]`

## Boundary

This design adds one future backend registration without changing `RealBackendProtocol`, `AdapterFactory`, any adapter, the private-view encoding, receipt fields, lifecycle, rollback semantics, law semantics, scoring, or protected-seed handling. Its only permitted registration is `role=control`, `scientific_arm=naive`; candidate, peer, and every other arm fail before backend construction `[PROPOSED]`. It performs a local behavioral observation of one public model. It is not scoring, qualification, readiness, model selection, equivalence evidence, or scientific evidence.

The implementation authority remains future and unbound. Persistent-CRITIC clearance of the WSL2 dependency-lock result `8c303b3262d8ea7640e06fe23671f999f5e01d2c`, persistent-CRITIC clearance of this design, a separate TASK BUILDER implementation/review cycle, and an exact Coordinator run release are all mandatory stops `[PROPOSED]`.

## Immutable identities

The seam is read from `src/m4_post_tokenizer_integration.py` at `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`. The final design clearance is `013af72e7dce566e7605d8e1e68fbfbf5d5cda28`. The public runtime is anchored to annotated testbed tag object `1994709b41c8e108e0b6f9a15936681f596823af`, peeled commit `11ea682a7f0fadfa1437a12d882402d90ffd0579`, and the exact prospective dependency-lock result above `[PROPOSED]`.

The sole model is `Qwen/Qwen3-4B-Instruct-2507-FP8` revision `8591804019c8b22094c3b5b4454e0edc05dffc98`, official FP8 E4M3 `[PROPOSED]`. The model file is 5,190,053,264 bytes with SHA-256 `b6154d74332140fd6dfbfbe70bbb3650dd6955861132bd59dda6789e6322b485`; tokenizer is 11,422,654 bytes with SHA-256 `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4`; tokenizer config is 9,377 bytes with SHA-256 `a62ff0a2472a0fa1b8eaabcb57c59b58afa42a22831dc141400b6e0cf2b65ce3` `[PROPOSED]`.

The local runtime is Python 3.12.3, torch 2.13.0+cu132, vLLM 0.27.1, transformers 5.15.1, tokenizers 0.22.2, safetensors 0.8.0, and numpy 2.3.5 `[PROPOSED]`. V1 and the sampler compatibility override remain mandatory. There is no network acquisition or fallback.

## Public synthetic inputs and private view

The prompt generator is public and deterministic. It produces exactly three ordered 122-byte strict-ASCII messages from the domain separators, zero-padded ordinal, and payload-digest algorithm in `m4_public_model_observation_prompt_contract_v1.json` `[PROPOSED]`. Only the generator and expected byte hashes are committed; no generated prompt bytes, prompt text, or token arrays are retained in Git.

A separately authorized local launcher generates a prompt, authenticates the exact tokenizer identity, tokenizes locally without added special tokens, and supplies the resulting array through the existing private-token provider `[PROPOSED]`. The cleared adapter authenticates the private view before calling the backend. The backend then parses only `M4_PRIVATE_VIEW_V1`, validates its framing/count/context/request correlation, materializes token IDs in mutable process-local memory, and invokes vLLM with `prompt_token_ids`. It never decodes prompt text. A `finally` block overwrites mutable token storage and releases every reference `[PROPOSED]`.

## Protocol implementation contract

All six public lifecycle methods plus `capture_state`, `restore_state`, `session_identity`, `dispose`, and `is_live` implement the exact cleared signatures. Every receipt has exactly the existing seven fields; no payload field is added `[PROPOSED]`.

- `describe` performs identity, registration, local-stage, dependency-clearance, and configuration checks without loading an engine.
- `initialize` verifies every model/runtime identity with network disabled, creates exactly one local vLLM engine, and commits only after liveness succeeds `[PROPOSED]`.
- `reset_episode` changes only canonical local episode state.
- `step` validates and privately decodes one authenticated view, performs exactly one generation, canonicalizes only sanitized hashes/counts/timings, atomically publishes one mode-0600 local observation, binds its digest into the result backend-state digest, and destroys raw prompt/output material `[PROPOSED]`.
- `snapshot` emits no raw material and returns only the standard receipt.
- `close` commits only after engine destruction and cleanup postconditions pass.

Generation is fixed at `dtype=auto`, `quantization=fp8`, maximum model length 2,048, one sequence at a time, GPU utilization 360,000 ppm, temperature zero, sampling seed zero, maximum 12 output tokens, one result, no remote code, no speculative decoding, no prefix caching, and disabled log statistics `[PROPOSED]`. These are diagnostic execution controls, not scientific bars.

## Local observation and publication boundary

The output stage comes only from `MOR_M4_PUBLIC_OBSERVATION_STAGE`; its value is never logged or committed. It must be an absolute, pre-existing, empty, non-symlink directory with mode 0700 `[PROPOSED]`. Each observation contains only hashes, counts, monotonic timings, exact identity digests, and four false evidence flags. Prompt/output text, input/output token IDs, model/tokenizer bytes, environment values, and private paths are forbidden.

Publication is temp-write, fsync, schema/semantic validation, mode 0600, atomic rename, directory fsync, then receipt commit `[PROPOSED]`. Git status must remain unchanged. Local observations are diagnostic operator artifacts; the design does not authorize committing them.

## Rollback, cleanup, and failure

`capture_state` excludes engine objects and raw arrays but binds all canonical lifecycle and observation digests. On any error, `restore_state` deletes the operation temp, restores the exact snapshot, and proves its canonical identity `[PROPOSED]`. If engine liveness or state identity cannot be restored, the backend disposes and returns rollback failure; it never retries.

`dispose` is idempotent: block new operations, destroy the engine, release references, empty the allocator cache, synchronize, remove temp files, require zero backend-owned live engines and no temp artifacts, and set `is_live()` to literal false `[PROPOSED]`. Cleanup failure prevents a close PASS receipt. A failed method yields no adapter/public commit and byte-identical adapter state through the already-cleared transaction mechanism.

## HELD law projection

The observation always uses the existing exact order L7, L8, L10, L14, L18 and existing HELD rows `[PROPOSED]`. Every row has `claim_made=false`, empty evidence, empty metrics, null failure, and its already-bound held reason. The backend cannot emit PASS or FAIL law rows. No behavioral observation can be promoted into a law claim.

## Deterministic local-only launch

The launch contract fixes environment names, environment values, argv, immutable checkout checks, network disablement, empty-stage checks, expected local observation count of three, zero Git changes, cleanup, and failure mapping `[PROPOSED]`. It contains no private value and `run_authorized=false`. A missing clearance, unbound implementation SHA, identity mismatch, nonempty stage, unknown field, prompt mismatch, backend error, local-write error, cleanup error, Git change, or request to run without an exact Coordinator release is a STOP.
