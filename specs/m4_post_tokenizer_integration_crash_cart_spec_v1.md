# M4 Post-Tokenizer Integration Crash-Cart Specification v1

Date: 2026-08-21
Regime: B
Status: design-only; no execution or release authority

## 1. Scope and precedence

This package closes the deterministic seam between a cleared tokenizer materialization and the M4 model scaffold. It specifies interfaces, lifecycle, private-token handling, semantic validation, executable synthetic evidence, and a future combined-tree construction. It does not implement a backend, select a model, consume custody, execute a materializer, score, or authorize a merge.

The Principal decision in `handoffs/REBECCA_M4_SCAFFOLD_RERELEASE_AND_LOCAL_TOKENIZER_CUSTODY_2026-08-21.md` at `45d40d8b688fb7f44098d235df7f31cca1aa3b31` is later and controls the conflicting rule at lines 70–71 of `specs/m4_model_agnostic_scaffold_spec_v1.md`. The exact-peer ladder handoff at `4e36466159744d622370ac0a9198cdf71836d354` independently binds candidate/peer equality checks. Candidate and peer are distinct runtime instances of the **same immutable checkpoint and training identity**, not independently trained peers. `parity.training_instance_sha256` therefore moves from the candidate/peer difference set to the equality set. Checkpoint revision, weight hashes, tokenizer, architecture, parameter count, quantization, decoding, calibration, evaluation, and binning must also match. Only role, scientific arm, runtime-instance identity, access/channel policy, and redaction receipts may differ. Unequal checkpoint or training identities fail closed as `PAIR_IDENTITY_MISMATCH`.

## 2. Adapter and factory seam

Implementation shall expose a structural `ModelAdapterProtocol` with `describe`, `initialize`, `reset_episode`, `step`, `snapshot`, and `close`. It shall expose a `RealBackendProtocol` whose step input is an immutable private token-array view plus request metadata and whose output is an adapter response payload. Neither protocol selects a scientific backend.

`AdapterFactory.create(role, scientific_arm, manifest_bytes, backend_config_bytes, private_token_provider)` shall:

1. schema-validate and semantic-validate the manifest and backend configuration;
2. verify the registry-bound factory, adapter, backend, dependency, runtime, model, tokenizer, and configuration identities before construction;
3. enforce the exact role/arm map;
4. build distinct `CandidateAdapter`, `PeerAdapter`, or `ControlAdapter` wrappers and distinct runtime sessions;
5. apply the peer observable-only channel before backend invocation; and
6. reject unknown backends and any implicit synthetic fallback.

`SyntheticCallableAdapter` remains permitted only when the selected registry entry is explicitly synthetic and the command is the governed synthetic test command. Production construction cannot select it.

## 3. Lifecycle

The semantic transition table is normative:

| Operation | Allowed prior state | Result | Required effects |
|---|---|---|---|
| describe | CREATED | DESCRIBED | identities fixed; no episode |
| initialize | DESCRIBED | INITIALIZED | backend initialized; no episode |
| reset_episode | INITIALIZED or STEPPED | EPISODE_READY | new episode id; increment reset ordinal; request ordinal zero; clear last response and episode cache |
| step | EPISODE_READY or STEPPED | STEPPED | same episode; request ordinal equals next ordinal; increment exactly once |
| snapshot | STEPPED | STEPPED | increment snapshot ordinal; preserve step readiness |
| close | INITIALIZED, EPISODE_READY, or STEPPED | CLOSED | `closed=true`; terminal |

Every operation validates its request, manifest correlation, complete pre-state digest, lifecycle semantics, and ordinal before calling a backend. Failure precedence is structural schema, semantic state, identity/digest, lifecycle/ordinal, private-token verification, backend, response semantics. A failure returns the first deterministic code and preserves byte-identical state. Duplicate or skipped request ordinals, episode reuse, reset from an active call, and every operation after CLOSED are rejected without mutation. Multiple steps per episode, close from every declared closable state, and reset after a completed stepped episode into a new episode are required behavior, not optional extensions. Regressions cover each happy path and every invalid transition.

## 4. Private token rederivation and fanout

The integration receives only the sanitized tokenizer result plus its exact raw-file identity and the cleared constructor/package identities. Inside the authorized private executor, `PrivateTokenProvider` reopens the preserved tokenizer, repeats the exact constructor, and canonicalizes each array as the tokenizer contract defines. Before any adapter call it verifies array length and SHA-256 against the sanitized result. Mismatch returns `TOKEN_ARRAY_DIGEST_MISMATCH`, produces no backend call, and preserves state.

After verification, a coordinator freezes one private array buffer and provides read-only byte-equivalent views to candidate and peer. Each adapter independently hashes the received canonical bytes. A sanitized fanout receipt records only context id, length, expected digest, candidate digest, peer digest, equality booleans, runtime-instance identities, and status. Token IDs, tokenizer/model bytes, private paths, environment roots, and reconstructed arrays are never serialized, logged, committed, or returned. Controls receive only the explicitly governed projection.

## 5. Semantic validation

JSON Schema validation is necessary but insufficient. `validate_state_semantics` shall enforce:

- `lifecycle_state == CLOSED` iff `closed == true`;
- CREATED, DESCRIBED, and INITIALIZED have no episode, response, or frozen episode payload and zero request ordinal;
- EPISODE_READY has a nonempty episode id, no last response, and next request ordinal zero;
- STEPPED has a nonempty episode id and last-response digest, and next request ordinal is positive;
- dependency and manifest identities never change after describe;
- reset, request, and snapshot ordinals are monotone with the transition table; and
- response role/arm/episode/request and before/after state digests correlate exactly.

`validate_harness_result_semantics` shall require exactly one row for every governed law id in this exact order: `L7`, `L8`, `L10`, `L14`, `L18`. It rejects duplicate keys even when rows are byte-different, missing/extra/reordered laws, inconsistent status/failure/evidence combinations, and top-level terminal/closed/result inconsistency. Required negative tests include CREATED with `closed=true`, duplicate L7, missing L18, and reordered rows.

## 6. Governed synthetic execution

The implementation package shall bind this single OCI command byte-for-byte (PowerShell variables are coordination placeholders and are not part of evidence):

```text
docker run --rm --pull=never --platform linux/amd64 --network none --read-only --cap-drop ALL --security-opt no-new-privileges --mount type=bind,src=<IMMUTABLE_CHECKOUT>,dst=/workspace,readonly --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m,mode=0700 --workdir /workspace --entrypoint python3 docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6 -I tests/run_m4_post_tokenizer_integration_tests.py
```

The checkout is immutable and clean; network is none; repository is read-only; no custody/model/tokenizer variables are present. The tracked `src/__init__.py` package marker and standard-library-only pre-import wrapper are executable-package members with exact mode/byte/digest bindings. Before importing project or test code, the wrapper verifies the marker, selected module paths, raw identities, sidecars, and import root; only then it inserts `/workspace` into `sys.path` and loads exactly the two selected modules. Expected exit is zero and the bound expected test count must equal discovery before release. Nonzero test exit is `INTEGRATION_TEST_FAILURE`; missing image, mount, interpreter, marker, wrapper identity, or import is `INSTRUMENT_FAILURE`. The command does not invoke the tokenizer materializer.

The smallest fixture uses a fake private rederiver and backend spies. It reconciles the ordered sanitized 1024/4096/8192 result records and stop-array digest, then verifies each private array digest before fanout. Missing, duplicated, reordered, wrong-length, wrong-digest, or wrong-stop-digest records fail before any backend call. Candidate and peer receive byte-identical private arrays in distinct sessions; episode A accepts ordinals 0 and 1; close paths are exercised; reset creates episode B and accepts ordinal 0; accepted output contains the five laws in exact order. It also proves no mutation/backend call after a tampered digest or ordinal and rejects the semantic negatives. Only sanitized digests and lengths enter evidence; synthetic array values remain process-local.

### 6.1 Custody-free crash-cart evidence bound by this design

At immutable main `cee97538893989e055f49a894f066d2083da4eb5`, custody-free probes reproduced all six motivating gaps:

1. `describe → initialize → reset → step` reaches STEPPED/ordinal 1, while a second step and second reset both return `ADAPTER_LIFECYCLE_VIOLATION` with byte-identical state (`src/m4_model_scaffold.py` lines 328–329 and 348–349).
2. Draft-2020-12 validation accepts CREATED with `closed=true`; forced describe detects only a wrapper-digest mismatch, not the cross-field invalidity.
3. The harness schema accepts five rows `L7,L7,L8,L10,L14`, omitting L18; four rows fail only through `minItems`.
4. In the exact pinned OCI topology, `python3 -I -m unittest src.test_m4_model_scaffold` and the discovery variant exit 1 because `src` is not importable and lacks `src/__init__.py`.
5. The scaffold's different-training rule conflicts with the later same-checkpoint exact-peer authorities bound in §1.
6. No current main or ladder consumer reads the sanitized tokenizer result or reconciles its ordered 1024/4096/8192 prompt identities and stop digest.

These are design inputs, not scientific evidence or execution release. No held input was accessed.

## 7. Combined-tree construction

The tokenizer and scaffold histories are not merge-compatible. Construction shall start from a fresh immutable checkout of a Coordinator-designated current-main SHA and path-selectively overlay exact cleared tokenizer blobs. A whole-tree merge or cherry-pick is forbidden.

The overlay allowlist is: `artifacts/m4_tokenizer_materialization/.gitkeep`; `diagnostics/m4_tokenizer_materialization.py`; all `specs/data/m4_tokenizer_*` JSON and sidecars; `specs/data/m4_context_format_probe_contract_v1.json` and sidecar; `specs/m4_local_tokenizer_materialization_spec_v1.md`; `specs/m4_local_tokenizer_materialization_changelog.md`; `tests/__init__.py`; the tokenizer wrapper and selected test; and `tools/testbed/run_m4_tokenizer_topology_smoke_matrix.sh`. The source is the final persistent-CRITIC-cleared descendant of the current audit head `0c418ef6aa22535c15e08cf88b45d4ced9bbee55`, never an inferred historical head.

Construct `.gitattributes` by preserving the designated main file byte-for-byte and in order, then appending one tokenizer section in the exact source order, omitting rules whose complete non-comment line already exists. A duplicate path with a different attribute expression is `ATTRIBUTE_RULE_CONFLICT`. Output is LF terminated.

This creates a new combined integration identity domain. Reproduce byte count, raw SHA-256, Git blob, and mode for the full allowlisted union. Rebind only the combined `.gitattributes` checkout-identity row in `m4_tokenizer_executable_package_v1.json` and the direct sidecar/downstream cascade unless raw reproduction proves another row changed. Preserve the other eight banked package rows exactly. Bind every scaffold baseline artifact, tokenizer overlay artifact, and new seam artifact in a complete combined inventory. Negative verification scans active files for stale source `.gitattributes`, package, sidecar, and integration digests; historical handoffs remain immutable.

## 8. Separated prerequisites

Mechanical implementation requires: (a) the Coordinator-designated combined-main base SHA, (b) the final cleared tokenizer source head, and (c) fixed implementation filenames before final raw identities are computed. These do not require Q2, EF3, or L8 decisions.

Q2/EF3/L8 still govern real backend selection, scientific output meanings and thresholds, hook semantics, model qualification, and any native L8 implementation. They do not block implementing or testing the byte/digest factory seam, lifecycle, private fanout, or semantic validators. Those scientific decisions remain held and outside this package.
