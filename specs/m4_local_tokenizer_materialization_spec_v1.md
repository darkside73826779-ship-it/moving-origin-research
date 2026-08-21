# M4 Bounded Local Tokenizer Materialization Specification v1

**Date:** 2026-08-21

**Regime:** B

**Status:** `[PROPOSED]`; Work Item B only; no access or execution authority

**Gate served:** deterministic specification closure before bounded local tokenizer materialization

## 1. Versioned-law compliance

Binding protocol, quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1:

> - **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
> - **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
> - **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.

Authority is `coordinator/m4-scaffold-rerelease-tokenizer-custody@45d40d8b688fb7f44098d235df7f31cca1aa3b31`. The referenced ladder constructor is `specs/data/m4_context_format_probe_contract_v1.json` at `architect/m4-model-selection-ladder@7a8239e9735042cddd94899ffaeaab53acf331fb`, raw SHA-256 `eab77b9f44a4e9378f5889f5aa368eabd87959a5ddafab9ca38685228f12feec` `[PROPOSED]`.

## 2. Selected immutable identity

The sole materialization target is `PRIMARY_QWEN3_4B_FP8`: repository `Qwen/Qwen3-4B-Instruct-2507-FP8`, revision `8591804019c8b22094c3b5b4454e0edc05dffc98`, official Qwen FP8 E4M3 checkpoint, Apache-2.0 `[PROPOSED]`. Weight identity is exactly `model.safetensors`, `5190053264` bytes, SHA-256 `b6154d74332140fd6dfbfbe70bbb3650dd6955861132bd59dda6789e6322b485` `[PROPOSED]`. The only readable tokenizer payloads are `tokenizer.json`, `11422654` bytes, SHA-256 `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4`, and `tokenizer_config.json`, `9377` bytes, at that same immutable revision `[PROPOSED]`. The latter is the sole source of `chat_template`, `eos_token_id`, and special-token declarations. Its raw SHA-256 is taken from the validated private custody record described below; the executor may neither substitute nor synthesize those values. No other checkpoint, rung, tokenizer file, weight, or cache is readable under this work item.

## 3. Local-only custody lookup

The public handle is exactly `M4_QWEN3_4B_FP8_PRESERVED_V1` `[PROPOSED]`. The authorized executor obtains its private local root only from environment variable `MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1`; absence, empty value, multiple resolution, symlink/junction root, or non-directory is `CUSTODY_HANDLE_UNRESOLVED`. The variable value and resolved path must never be logged, serialized, committed, or included in an exception `[PROPOSED]`.

The local root must contain exactly one regular, non-link file at the literal relative name `.mor-custody-record-v1.json`; recursive search, globbing, alternate names, and fallback locations are forbidden. Its bytes are UTF-8 RFC 8785 JSON plus one LF and must validate against `specs/data/m4_tokenizer_private_custody_record_schema_v1.json`. The resolver reads only the single named environment variable, rejects a value containing NUL, CR, or LF, resolves it once with the platform absolute-path resolver, requires one directory, then joins the literal record name and the three literal artifact names. It does not split the value on `;`, `:`, commas, or path-list syntax. A missing/non-regular/link record, schema error, noncanonical bytes, duplicate JSON member, or unexpected field is `CUSTODY_ATTESTATION_INVALID`; absent/empty/invalid root is `CUSTODY_HANDLE_UNRESOLVED` `[PROPOSED]`.

The executor may read the private record but serializes none of it except the public fields prescribed here. The record attests the exact repository, revision, quantization, weight filename/bytes/hash, `tokenizer.json` filename/bytes/hash, `tokenizer_config.json` filename/bytes/raw SHA-256, immutable status, and most recent custody verification status `PASS`. The record's configuration digest is authoritative only after the file's `9377` byte count and raw SHA-256 reproduce locally and the repository/revision fields match this specification. The materializer does not open the weight file. A mismatch is `CHECKPOINT_IDENTITY_MISMATCH`; stale/non-PASS custody evidence is `CUSTODY_ATTESTATION_INVALID` `[PROPOSED]`.

Before tokenizer read, create an OS-private temporary directory, copy only `tokenizer.json` and `tokenizer_config.json`, verify each byte count and SHA-256 before and after copy, then make both copies read-only. Record neither temporary nor preserved paths. After materialization, hash both source files and both copies again, require all digests unchanged, then delete only the temporary copies using the platform temporary-directory owner. The preserved artifact is never modified. Candidate/peer serving later uses two separate runtime instances from the same preserved identity; this work item creates neither instance `[PROPOSED]`.

## 4. Exact arrays and constructor

Input messages are the single ordered object `[{'role':'user','content':'Return one JSON object whose answer field is the string A.'}]` (JSON spelling is normative; single quotes here are explanatory) `[PROPOSED]`. Loading is exactly `transformers.AutoTokenizer.from_pretrained(temp_directory, local_files_only=true, trust_remote_code=false, use_fast=true)` inside the sealed runtime in §7. Invocation is `apply_chat_template(messages, tokenize=true, add_generation_prompt=true, continue_final_message=false, enable_thinking=false)` `[PROPOSED]`. The loaded object's `chat_template` must equal the `chat_template` JSON string decoded from the verified `tokenizer_config.json`; missing, null, non-string, or unequal values are `TOKENIZER_CONFIG_IDENTITY_MISMATCH` `[PROPOSED]`.

Define base array `B` as the exact integer list returned by that call. Define `N=encode(' x', add_special_tokens=false)` and require `len(N)==1` `[PROPOSED]`. Encode the exact user content without special tokens as `U_TEXT`; require exactly one contiguous occurrence of `U_TEXT` in `B`; its first index is `u`. For each target prompt length `T` in stored order `992`, `4064`, `8160` `[PROPOSED]`, define:

`R_T = B[0:u] + repeat(N[0], T-len(B)) + B[u:len(B)]` `[PROPOSED]`.

The three arrays are named, respectively, `CONTEXT_1024_PROMPT_IDS`, `CONTEXT_4096_PROMPT_IDS`, and `CONTEXT_8192_PROMPT_IDS`; their prompt lengths are `992`, `4064`, and `8160`, paired with maximum new-token count `32` to yield total contexts `1024`, `4096`, and `8192` `[PROPOSED]`. If `T < len(B)`, occurrence count is not one, or an integer is outside tokenizer vocabulary, return `CONSTRUCTOR_INVARIANT_FAILURE` without partial output.

## 5. Encode/decode identity and stop array

For each `R_T`, compute `S_T=decode(R_T, skip_special_tokens=false, clean_up_tokenization_spaces=false)`, then `E_T=encode(S_T, add_special_tokens=false)` `[PROPOSED]`. Identity means equal integer-array length and equal integer at every ordinal; Unicode normalization, whitespace rewriting, special-token stripping, and lossy replacement are forbidden. A mismatch is `ENCODE_DECODE_IDENTITY_FAILURE`; the artifact records only lengths and digests, never text or token IDs `[PROPOSED]`.

Require `convert_tokens_to_ids('<|im_end|>') == 151645` and `eos_token_id == 151645` `[PROPOSED]`. Construct sources in stored order `[eos_token_id, im_end_token_id]`, retain the first occurrence of each integer and discard later duplicates; the required stop array is therefore exactly `[151645]` `[PROPOSED]`. Any other source or result is `STOP_ARRAY_MISMATCH`.

## 6. Digest and publication contract

The request is a singleton input: its raw bytes must match `specs/data/m4_tokenizer_materialization_request_v1.json` and SHA-256 `85f7eba2c872fc10fba00f088c1bbf6f6334ee69cfe35a856364e58d949a98b2` before any custody lookup `[PROPOSED]`. A byte-different request is `CONSTRUCTOR_IDENTITY_MISMATCH`; no schema-valid variation or command-line override is authorized.

For each integer array, serialize the array itself using RFC 8785/JCS JSON: ASCII `[` and `]`, comma separators, base-ten JSON integers with no leading plus or zero padding, no whitespace, UTF-8, and no trailing LF. SHA-256 hashes those exact bytes `[PROPOSED]`. The stop-array digest uses the identical domain. The rendered text is never serialized or hashed into the public result.

The only repository result is `artifacts/m4_tokenizer_materialization/tokenizer_materialization.json`, validated by `specs/data/m4_tokenizer_materialization_result_schema_v1.json`; its sidecar is the same path plus `.sha256` `[PROPOSED]`. Stored JSON is RFC 8785 UTF-8 plus one LF. The sidecar is lowercase digest, two spaces, basename, LF. Publication is an atomic JSON/sidecar pair; failure leaves `.incomplete` and preserves the previous valid pair `[PROPOSED]`.

Allowed status is `PASS`, `FAIL`, or `BLOCKED`. Pre-access missing authority/handle/contract is `BLOCKED`; an executed identity/constructor/serialization check failure is `FAIL`; `PASS` requires all checks, three array rows, exact stop-array length/value/digest `580af853441f1d705732a492fe363f022bdd177c37d2b8f82035cbdf9a604b8c`, and no forbidden field `[PROPOSED]`.

`m4_tokenizer_materialization_synthetic_pass_v1.json` is a schema/topology fixture only: its all-zero context-array digests are literal synthetic values and may never be published as materialized evidence `[PROPOSED]`. Its stop-array digest is the real digest of canonical `[151645]`. The BLOCKED fixture is the exact no-authority outcome.

## 7. Prescribed implementation and verification interface

Future TASK BUILDER target is `diagnostics/m4_tokenizer_materialization.py` with callable `materialize(contract_path: str, custody_handle: str, output_path: str) -> int` `[PROPOSED]`. Execution is allowed only inside OCI image `docker.io/vllm/vllm-openai:v0.10.2`, multi-platform digest `sha256:607442e407b0fea97f8a132a78b787c121a996dd4de181fa08e8da06e71ec2db`, Linux/amd64 manifest digest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6` `[PROPOSED]`. Those immutable image digests are the complete Python/Transformers dependency manifest; host Python, a tag-only image, another platform manifest, installation, upgrade, monkey patch, remote-code loading, or alternate tokenizer class is `RUNTIME_IDENTITY_MISMATCH` before custody lookup. Exit codes are `0=PASS`, `2=BLOCKED`, `3=FAIL`, `4=INTERNAL_ERROR` `[PROPOSED]`. The only authorized invocation is:

`python -I diagnostics/m4_tokenizer_materialization.py --contract specs/data/m4_tokenizer_materialization_request_v1.json --custody-handle M4_QWEN3_4B_FP8_PRESERVED_V1 --output artifacts/m4_tokenizer_materialization/tokenizer_materialization.json` `[PROPOSED]`.

Prescribed verification is `python -I -m unittest tests.test_m4_tokenizer_materialization` followed by the invocation above only after a separate Rebecca execution release `[PROPOSED]`. The unit suite must cover: exact request acceptance; wrong repository/revision/weight/tokenizer/config/quantization rejection; absent/empty/symlink custody handle; absent, linked, noncanonical, duplicate-member, extra-field, and schema-invalid `.mor-custody-record-v1.json`; tokenizer/config byte mismatch; missing/null/non-string/unequal chat template; wrong OCI index/platform digest and alternate loading API; non-unique content insertion; multi-token neutral fragment; each encode/decode mismatch ordinal; wrong/doubled/reordered stop source; serialization ambiguity; PASS/BLOCKED/FAIL schema reachability; forbidden path/host/token-array fields; atomic interruption and previous-pair recovery. Expected codes are those defined in the schema; no network is permitted `[PROPOSED]`.

## 8. Holds

This specification authorizes no tokenizer/model access, download, package/environment mutation, acquisition, preflight, qualification, diagnostics, scoring, protected seeds, scaffold change, state/provenance mutation, merge, or gate decision. Q2 remains unsigned/deferred and EF3 remains held. Materialized metadata requires persistent-CRITIC verification and later Rebecca release.
