# CRITIC M4 Tokenizer Materialization Execution Review

Date: 2026-08-21 EDT  
Regime: B  
Role: authoritative persistent CRITIC  
Terminal state: **CONFIRMED FAIL — CONSTRUCTION/IMPLEMENTATION DEFECT**

## Immutable intake and lineage

- Execution branch/head: `taskbuilder/m4-tokenizer-topology-clear-materialization-execution @ 0aadbc2b120cc5cf60386775cc8d61535d722c96`
- Result/handoff commit: `67d631cdde1572fc2906b638e14d8bc05ecbf45d`
- Exact re-release: `coordinator/m4-tokenizer-topology-clear-rerelease @ 5e6a6eb4d7de5c634c5b9a5881076d066c397c7c`
- Cleared package head: `522b01d42ceef90ee2390c169f29fb163e610470`
- Persistent-CRITIC topology CLEAR: `41d844063416b68090c933a76f31e82c4d83e458`
- Checkout: repository `tools/workflow_checkout.py`; receipt SHA-256 `0b65e731ff469bb123945a984764b1d8ea86b1542b565778409edfd98f5a8b1a`

The lineage is exact and linear from the cleared package through re-release, result publication, manifest, and scan-classification head. The release names the independent CLEAR and authorizes exactly one start after the wrapper, topology matrix, and private preconditions.

The canonical handoff manifest validates with `tools/workflow_contract_validator.py`. All 21 declared artifact SHA-256 values reproduce from raw Git blobs with exact modes.

## Execution and consumption evidence

- Fresh immutable release checkout, Git integrity, nine-entry package, pinned runtime/image, and private preconditions are recorded PASS.
- Exact no-custody wrapper ran first: **35/35 PASS**, exit `0`.
- Four-case custody-free topology matrix ran second: PASS, exit `0`, cleanup complete.
- Exactly one materializer process started. It returned governed exit `3`; no retry, fallback, alternate binding/runtime/topology/command, or later diagnostic execution occurred.
- The operation is **CONSUMED** and remains so. This review performed no rerun or private access.

## Sanitized FAIL result validity

The committed raw Git blob for `tokenizer_materialization.json` is mode `100644`, 1740 bytes, Git blob `c260aaab0b62c351175c1c6fc862c24a59178b01`, and SHA-256 `10a14c1a4f7b257aa195636ab86b7a85a68fc084af13bead7b5d4b3ecfa55728`. It is strict minified canonical UTF-8/ASCII JSON with no BOM or CR and exactly one terminal LF. Its 97-byte sidecar binds that digest and basename exactly.

The Windows worktree presents transformed CRLF bytes for this newly published path; those presentation bytes are not substituted for the governed raw Git blob. Canonicality, schema, sidecar, and inventory conclusions use the committed raw object.

The result satisfies the Draft 2020-12 result schema and active failure-projection rules:

- checks 0–8 are ordered PASS: `AUTHORITY`, `CUSTODY_HANDLE`, `CUSTODY_ATTESTATION`, `TOKENIZER_ORIGINAL`, `TOKENIZER_COPY`, `CONSTRUCTOR_IDENTITY`, `BASE_TEMPLATE`, `INSERTION_UNIQUENESS`, `NEUTRAL_FRAGMENT`;
- ordinal 9 is `ARRAY_1024` / FAIL;
- status is `FAIL`, failure code is `CONSTRUCTOR_INVARIANT_FAILURE`;
- `arrays=[]`, stop length is zero, stop digest is null, and no later or partial rows appear.

The result contains only schema-permitted sanitized public identity/status fields. It exposes no token IDs, arrays, tokenizer/model bytes, private paths or custody values, host/environment values, seeds, scores, or scientific output.

## Failure-cause classification

### Input-identity mismatch — rejected

The exact tokenizer/config/constructor identities are recorded, and the production checks through tokenizer original/copy, constructor identity, base template, insertion uniqueness, and neutral fragment all passed. The failure is in the first constructed-array check, not input identity or custody identity.

### Expected-binding/specification defect — rejected for the vocabulary predicate

The cleared specification requires failure when an integer is “outside tokenizer vocabulary.” It does not mandate the base-vocabulary property `tokenizer.vocab_size`. The same contract depends on chat-template special tokens and later requires special token ID `151645`, so “tokenizer vocabulary” must mean the complete valid tokenizer ID domain, including added tokens.

### Construction/implementation defect — confirmed

Production code rejects any constructed ID satisfying `item >= tokenizer.vocab_size`. In the tokenizer API, that property is the base vocabulary size; valid added special-token IDs used by the Qwen chat template may lie above it. The check therefore narrows the cleared full-vocabulary predicate without authority. `ARRAY_1024` is simply the first target evaluated by this shared predicate; the sanitized evidence does not establish a 1024-specific digest defect.

The existing synthetic tokenizers set `vocab_size=200000`, while their special IDs are approximately 151645. They cannot exercise the valid-added-token-above-base boundary, which explains the wrapper’s false-negative 35/35 PASS.

The public result deliberately does not expose the offending private ID or base length. Thus it cannot by itself distinguish the two internal predicates grouped under `ARRAY_1024` (`prompt_length >= len(base)` versus full array validation). Nevertheless, the unauthorized base-vocabulary bound is independently present in production and is the construction defect consistent with the advisory and first-array failure. This classification does not authorize a rerun.

## Required lawful correction and regression

Replace the base-size comparison with a full-domain membership check computed once from the verified tokenizer, for example:

`valid_token_ids = frozenset(tokenizer.get_vocab().values())`

For every constructed value require `type(item) is int`, `item >= 0`, and `item in valid_token_ids`. Do not infer validity solely from `tokenizer.vocab_size`; membership also fails closed on any gap or nonexistent ID.

Add at least these exact synthetic regressions:

1. A tokenizer whose base `vocab_size` is below a valid added chat-template token ID, whose `get_vocab()` includes that ID, and whose constructed array contains it; construction must pass the array-domain predicate and proceed to encode/decode validation.
2. The same fixture with one nonmember ID; the first affected array must fail `CONSTRUCTOR_INVARIANT_FAILURE`, publish no partial array, and preserve ordered failure projection.
3. Assertions that the Qwen chat-template special-token domain is not modeled by an inflated fake `vocab_size`.

Any correction is prospective implementation work only. The consumed execution is permanent evidence and must not be replaced, relabeled, retried, or rerun.

## Public safety and disposition

Public-safety review found no prohibited content. Scanner matches wholly inside required public Git/artifact/model/tokenizer digest strings are reproducibility metadata requiring explicit manual classification; generic-key matches on the schema-authorized public tokenizer digests are public identities, not credentials, and are not suppressed.

**CONFIRMED FAIL — CONSTRUCTION/IMPLEMENTATION DEFECT.** The sanitized FAIL evidence is valid, the operation is consumed, and no retry is authorized. Return through WORKFLOW COORDINATOR for routing of the prospective code/test defect through the established role chain. No merge, publication of held data, execution release, or gate decision is made.
