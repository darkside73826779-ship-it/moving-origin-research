# M4 Model-Selection Qualification Ladder Specification v1

**Date:** 2026-08-21

**Regime:** B

**Status:** `[PROPOSED]`; specification only; Q2 numeric band pending Rebecca signature; no acquisition, preflight, qualification, implementation, scoring, or merge authority

**Gate served:** M4 candidate/peer model-selection qualification-ladder incorporation and executor-input closure

**Authority:** `coordinator/m4-model-selection-ladder-directive@9f79bdcaa029aba14308d2daad92519811303af6`; `handoffs/REBECCA_M4_MODEL_SELECTION_QUALIFICATION_LADDER_DIRECTIVE_2026-08-21.md`; `handoffs/REBECCA_M4_EXACT_MATCHED_PEER_AMENDMENT_2026-08-21.md`; `handoffs/REBECCA_LOCAL_ONLY_MODEL_ARTIFACT_CUSTODY_DIRECTIVE_2026-08-21.md`; executor block `taskbuilder/m4-model-custody-preflight@60257a3f746cc6338ef8ca8892c165cdcb0f6747`

## 1. Versioned-law compliance

Binding protocol, quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1:

> - **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
> - **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
> - **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.

Relevant law text, quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md`:

> **L7 — Mirror standard (from the introspection literature).** Self-reports about internal state must be calibrated against ground-truth internals AND must beat a peer-observer baseline (a matched model predicting this system from its outputs). *Test:* AUROC ≥ 0.75 and ECE ≤ 0.10 on self-state prediction, with the self-vs-peer margin > 0 at p < .05. No margin over the peer = portrait, not mirror — reported as such. Contamination controls (permuted/empty/shuffled) mandatory.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

No L7 numeric bar changes. The exact-peer amendment restores the same-checkpoint, same-parameter, same-architecture comparator required by `[LAW-L7]` and `[BAR-Entry 11]`. All qualification thresholds introduced below are `[PROPOSED]` and cannot operate until Rebecca approves the exact package.

## 2. Frozen ladder and exact peer

`specs/data/m4_model_ladder_manifest_v1.json` is the only allowed ladder `[PROPOSED]`:

1. primary candidate and peer: separate runtime instances of `Qwen/Qwen3-4B-Instruct-2507-FP8` at revision `8591804019c8b22094c3b5b4454e0edc05dffc98` `[PROPOSED]`;
2. fallback candidate and peer: separate runtime instances of `Qwen/Qwen3-8B-FP8` at revision `220b46e3b2180893580a4454f21f22d3ebb187d3`, with thinking disabled `[PROPOSED]`.

Both repositories are official Qwen-published FP8 checkpoints; no locally derived quantization is authorized. Every weight filename, byte count, and upstream SHA-256 is fixed in the manifest. Candidate and peer at a rung must match on repository, revision, every weight digest, tokenizer revision, architecture, parameterization, FP8 configuration, decoding, calibration, evaluation, and binning. Only runtime instance ID and access policy differ. Peer input is the complete Phase A public projection and never includes self-report, internal representation, privileged state, gradients, hidden activations, device pointers, or perturbation realization `[LAW-L7] [BAR-Entry 11]`.

Llama 3.2 3B and Llama 3.1 8B are prohibited. Their use, even diagnostically, is `UNAPPROVED_MODEL_IDENTITY` and requires a new Rebecca ruling `[PROPOSED]`.

## 3. Local-only acquisition and custody

The future executor consumes `m4_model_preflight_request_v1.json`; it never chooses a repository, revision, filename, hash, destination label, or serving stack. Acquisition is exactly one `huggingface_hub.snapshot_download(repo_id=<manifest repository>, revision=<manifest revision>, allow_patterns=<stored-order manifest file-name array>)` call per rung into an executor-selected local-only directory that is never serialized. The installed `huggingface_hub` implementation is the one sealed inside the approved OCI image digest; no host implementation or post-start installation is allowed. Redirects and authenticated transfer details are never recorded. After return, the executor enumerates regular files relative to the returned snapshot root, requires exact set equality with the allow-list, then performs the ordered byte-count and SHA-256 checks below. Any extra or missing file, revision mismatch, byte-count mismatch, or weight SHA mismatch fails closed `[PROPOSED]`.

Model binaries, shards, tokenizers distributed with the checkpoint, caches, snapshots, conversions, quantized copies, adapters, dumps, and Git LFS pointers remain local and are forbidden from Git. Repository output is limited to sanitized metadata valid under `m4_model_custody_record_schema_v1.json`: logical artifact IDs, public repository/revision, public filenames, byte counts, SHA-256, license ID/source URL, UTC verification time, and status. It contains no local path, cache location, hostname, username, machine ID, credential, signed URL, token, environment dump, or model bytes `[PROPOSED]`.

At every session start, before model load, the executor enumerates the allow-list in stored order, streams SHA-256 over each local file, verifies byte counts, verifies the resolved upstream revision, and compares candidate and peer arrays byte-for-byte. Any mismatch returns `CHECKPOINT_IDENTITY_MISMATCH`; an adapter or unlisted weight returns `UNAPPROVED_MODEL_ARTIFACT`; missing license acceptance returns `LICENSE_NOT_ACCEPTED`. No fallback or redownload occurs in that attempt `[PROPOSED]`.

## 4. Exact serving stack and deterministic decoding

The sole serving stack is OCI image `docker.io/vllm/vllm-openai:v0.10.2` with multi-platform digest `sha256:607442e407b0fea97f8a132a78b787c121a996dd4de181fa08e8da06e71ec2db` and Linux/amd64 manifest digest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6` `[PROPOSED]`. The executor verifies both registry-resolved digests before use. A different tag, digest, platform, patched image, host Python environment, or in-container installation is `STACK_IDENTITY_MISMATCH`; the preflight stops `[PROPOSED]`.

Both instances use `dtype=auto`, `quantization=fp8`, `max_model_len=8192`, `max_num_seqs=1`, prefix caching disabled, speculative decoding disabled, and deterministic eager execution enabled `[PROPOSED]`. The co-resident profile assigns `gpu_memory_utilization=0.45` to each instance; the phased-sequential profile assigns `0.90` to the sole loaded instance `[PROPOSED]`. Candidate and peer decoding is greedy: temperature `0`, top-p `1`, top-k disabled, one sequence, maximum `512` new tokens for qualification and `32` for preflight, no presence/frequency penalty, and the same stop-token array from the selected tokenizer `[PROPOSED]`. Qwen3-8B sets `enable_thinking=false` `[PROPOSED]`. Any Q4/GPTQ/AWQ/GGUF substitution or non-FP8 logits source is `QUANTIZATION_FLOOR_VIOLATION` `[PROPOSED]`.

Backbones are frozen. Parameter gradients and optimizer construction are forbidden. QLoRA is `CLOSED`; opening it requires a new Rebecca ruling, a scoring-disjoint dataset manifest, frozen adapter identity and hashes, contamination argument, persistent-CRITIC review, and new implementation authority `[PROPOSED]`.

## 5. FP8 and resource preflight

Preflight order and evidence are fixed by `m4_model_preflight_request_v1.json` and `m4_model_preflight_result_schema_v1.json` `[PROPOSED]`:

1. verify stack and checkpoint custody;
2. verify each linear checkpoint's quantization metadata declares FP8 E4M3 weights and no sub-eight-bit weight source;
3. load one candidate instance and render the fixed ASCII instruction `Return one JSON object whose answer field is the string A.`; encode the neutral fragment ` x` without special tokens and require it to yield exactly one token; insert repetitions of that token before the final instruction so rendered prompt lengths are exactly `992`, `4064`, and `8160` tokens; generate at most `32` tokens so total configured context lengths are `1024`, `4096`, and `8192`; perform one warm-up and one measured generation at each length; synchronize CUDA; require every measured logit finite and JSON parsing to yield exactly `{"answer":"A"}` with no other member `[PROPOSED]`;
4. unload, synchronize, and require allocated GPU bytes to return to at most `268435456` bytes above the recorded pre-load baseline `[PROPOSED]`;
5. test co-residency in candidate-then-peer load order at `8192` tokens per instance, batch/concurrency one, one warm-up and one measured turn per instance, alternating candidate then peer, with CUDA synchronization after every turn `[PROPOSED]`;
6. sample process GPU allocated and reserved bytes immediately after each synchronization and record the maximum; no time-sampled system-wide telemetry or machine-unique device identity enters the artifact `[PROPOSED]`.

Co-residency passes only if both exact instances remain loaded, both measured turns pass, no allocation failure occurs, and maximum reserved bytes are at most `15461882265` bytes (90% of 16 GiB) `[PROPOSED]`. Primary co-residency failure does not change rung; it selects phased sequential serving for the same qualified rung. The fallback 8B pair is always phased sequential and is never required to co-reside `[PROPOSED]`.

## 6. Phased sequential swap

The fixed fallback procedure is `[PROPOSED]`:

1. load candidate; verify session identity; execute Phase A only; canonicalize and seal the transcript pair;
2. synchronize; destroy candidate engine; release references; empty allocator cache; synchronize; verify residual allocated bytes are within `268435456` bytes of pre-candidate baseline `[PROPOSED]`;
3. load the exact-matched peer from the same local logical checkpoint; repeat full session hash verification; replay only the sealed public projection in stored ordinal order; write Phase B predictions;
4. synchronize and unload peer under the same residual-memory rule;
5. Phase C may consume the sealed Phase A/Phase B artifacts only after their sidecars validate.

The dry swap passes only if candidate and peer identities are equal, every phase transition is ordered, both residual-memory checks pass, the peer receives no privileged field, all transcript ordinals are contiguous, and the sealed Phase A digest is unchanged after replay. Failures are `SWAP_ORDER_MISMATCH`, `MEMORY_NOT_RELEASED`, `PEER_PRIVILEGE_LEAK`, `TRANSCRIPT_DIGEST_MISMATCH`, or the earlier identity/stack codes. No retry occurs `[O-14] [PROPOSED]`.

## 7. Phase A observable logging

Every candidate turn validates against `m4_phase_a_transcript_schema_v1.json`. It records the exact rendered prompt, public input projection, generated token IDs/text, per-option pre-softmax logits, normalized confidence, abstention score, declared self-state vector, monotonic start/end nanoseconds relative to the run (never wall-clock or host identity), oracle correctness/label, request/episode/seed ordinals, checkpoint and configuration digests, and response digest `[PROPOSED]`. The peer-visible projection includes prompts, candidate outputs, logits/confidences, timing offsets, oracle correctness, and public history; it excludes the candidate self-state vector and every other privileged field `[LAW-L7] [BAR-Entry 11]`.

The full record is retained for custody; the projection constructor is field-copy by the schema's stored `peer_projection_order`. Its canonical digest is sealed before candidate unload. Missing, extra, nonfinite, reordered, or post-seal modified data is `PHASE_A_LOG_INVALID` and blocks peer replay `[PROPOSED]`.

## 8. Q1–Q3 qualification and numeric Q2 proposal

Qualification is O-15 diagnostic-only on development seeds `101–105` `[OP-Entry 11.7]`. No qualification begins until an exact committed development-battery manifest and SHA replace the plan's `UNBOUND_REQUIRES_REBECCA_RELEASE` binding and persistent CRITIC verifies that reconciliation. TASK BUILDER cannot create or choose prompts, task generators, labels, difficulty changes, or sample counts `[PROPOSED]`.

For each bound battery, run order is seed-major `101,102,103,104,105`, then request ordinal ascending `[OP-Entry 11.7] [PROPOSED]`. Q1, Q2, and Q3 occur in that order `[PROPOSED]`:

- **Q1 format:** every response on every development seed must validate the fixed answer schema; observed valid rate must equal `1.0` `[PROPOSED]`. Failure moves directly to the 8B rung; no fine-tuning detour.
- **Q2 informative band:** qualification-only threshold `tau_q=0.70`; pooled natural accuracy must be within `[0.60,0.85]`; each-seed accuracy within `[0.55,0.90]`; at least `0.20` pooled and `0.15` per seed of confidence values must lie within `[0.60,0.80]`; coverage at `tau_q` must be within `[0.30,0.80]`; and answered selective risk must be within `[0.10,0.40]` `[PROPOSED — PENDING REBECCA SIGNATURE]`. These values do not replace scoring tau or any L7/L10 bar.
- **Q3 mirror calibratability:** fit only the scalar calibration head defined in the plan on seeds `101–103`, evaluate without refit on seeds `104–105`, and require ECE `≤0.10` pooled and separately on both evaluation seeds `[LAW-L7] [OP-Entry 11.7]`. Backbone weights remain frozen.

Q2 ceiling failure at the 4B standard battery advances to the single separately committed harder-difficulty battery, not a rerun. If that distinct stage also exceeds the ceiling, advance to 8B. Any other 4B Q1/Q2/Q3 failure advances directly to 8B. The failed result remains recorded. An 8B failure yields `NO_QUALIFYING_RUNG`; no model beyond 8B and no configuration adjustment is allowed `[PROPOSED]`.

No result from run N changes run N+1. The complete sequence, battery identities, prompts, decoding, contexts, stack, and thresholds are frozen before the first run. Scoring follows each future scoring run under its separate authorization; qualification never scores or exposes protected seeds `[LAW-L19] [O-15]`.

## 9. Calibration-head algorithm

For Q3, convert confidence `c` to `z=log(min(1-1e-12,max(1e-12,c))/(1-min(1e-12,max(1e-12,c))))` in binary64 `[PROPOSED]`. Search `a=0.50,0.55,...,2.00` outer-major and `b=-1.00,-0.95,...,1.00` inner-major; prediction is `sigmoid(a*z+b)` `[PROPOSED]`. Minimize mean binary cross-entropy on the stored seed `101–103` examples in seed/request order using binary64; exact ties select lower `a`, then lower `b` `[PROPOSED]`. ECE uses `15` equal-width bins on `[0,1]`, lower-inclusive/upper-exclusive except the last bin includes `1`, with empty bins contributing zero `[PROPOSED]`. No learned backbone or adaptive optimizer exists.

## 10. Reports, statuses, and routing

The committed ladder manifest, qualification plan, and preflight request are singleton control inputs. Before schema validation, their raw bytes must equal their committed files and their sidecars; a byte-different variant is `CONFIGURATION_MISMATCH`, even when it validates against the descriptive schema. Thus no permissive nested schema node authorizes an executor-selected value. The executor may materialize a later battery reconciliation only through a separately committed ARCHITECT amendment, persistent-CRITIC CLEAR, and Rebecca release `[PROPOSED]`.

The preflight result and qualification report reject unknown fields and use RFC-8785 UTF-8 plus one LF for stored JSON; sidecars are lowercase SHA-256, two spaces, basename, LF `[PROPOSED]`. Allowed preflight status is `PASS`, `FAIL`, or `BLOCKED`; qualification status is `PRIMARY_SELECTED`, `FALLBACK_SELECTED`, `NO_QUALIFYING_RUNG`, or `BLOCKED`. A report names every attempted stage, retains every failure, and states the selected serving mode and reason `[PROPOSED]`.

Before any executor release: ARCHITECT result → established persistent CRITIC → WORKFLOW COORDINATOR → Rebecca. Rebecca must separately sign the Q2 band, exact model identities, serving/preflight contract, and future battery reconciliation. Acquisition/preflight and Q1–Q3 are separately released operations. Neither releases scaffold implementation or scoring `[PROPOSED]`.

## 11. STOPs and prohibitions

STOP on missing battery SHA, identity/hash mismatch, license unavailability, stack mismatch, unsupported FP8, Q4 substitution, unapproved file, local-only custody violation, incomplete log, nondeterminism, memory/swap failure, peer privilege leak, adaptive change, or request for an out-of-ladder model `[PROPOSED]`.

No model artifact may enter Git. No download, installation, preflight, qualification, scaffold implementation, scoring, protected-seed access, adaptive between-run change, backbone update, QLoRA, Llama peer, model beyond the ladder, native-CUDA L8, state/provenance mutation, rerun, merge, or gate decision is authorized by this specification.
