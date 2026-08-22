# CRITIC M4 Post-Tokenizer Integration Implementation Review

Date: 2026-08-22 EDT

Regime: B

Role: authoritative persistent CRITIC

Terminal state: **COMBINED BLOCK**

## Immutable intake and banked evidence

- Package head: `taskbuilder/m4-post-tokenizer-integration-implementation @ 94ea2c05fcdb74b314f23c229b673bc90ec485f0`
- Implementation commit: `6b82328f0d61e4dd3bf330b0cd5d4b825fbf6af6`
- Release/base: `coordinator/m4-post-tokenizer-integration-implementation-release @ 071392aadfcdf6c76b47f3f959578661658f7791`
- Cleared design: `b5b8028a7126e838c239ba0927b526f9cec8b7e2`
- Cleared tokenizer source: `ddae7c3b8f664cbc94654198916e1940c9006c1e`
- Helper checkout receipt SHA-256: `f598cfca712beacc446139148810efe613e7d70282018e94ac834e5e59a742e1`

The handoff manifest validates with the workflow contract validator, and all 50 declared artifact SHA-256 values reproduce from raw Git blobs. The separate combined inventory is exactly 63 rows with zero mode, blob, size, or SHA-256 mismatches. Its source groups are one COMBINED, 35 TOKENIZER, three REBOUND, four SEAM, and 20 DESIGN rows. All 35 tokenizer rows equal the cleared tokenizer source; all 20 design rows equal the cleared design. All 25 inventory-contained JSON sidecars verify. Raw combined-inventory SHA-256 `acfc96c1ebed0841ded7e7e69e5823decec2174ec23016710321c126718ee450` and launch-contract SHA-256 `3c2fc8709e5b73988d095aef2576e4f98de0e51428a894767819532fb81412b0` reproduce. The consumed tokenizer PASS pair is preserved exactly.

The committed tests provide useful banked coverage for the 42 lifecycle cells, private-view digests, receipt faults, fanout call counts, and held projections. The reported Linux 32/32 integration and 37/37 tokenizer runs remain corroborating evidence. They do not close the production defects below.

## IR1 — Exact launch and handoff topology are not executable identities

The committed integration OCI launch contract contains the literal mount token `type=bind,src=,dst=/workspace,readonly`. Its source is empty. It cannot mount the released checkout and cannot be the exact pinned command claimed by the handoff. Bind an exact private variable placeholder without shell-time erasure, validate it before process start, and add a custody-free command-token realization that proves the repository is mounted read-only at `/workspace`.

The canonical handoff manifest also binds `remote_ref` to the incoming Coordinator release and sets `routing_ref_sha` to that same release `071392aadfcdf6c76b47f3f959578661658f7791`, while its artifacts are from package head `94ea2c05fcdb74b314f23c229b673bc90ec485f0` and its scan tip is implementation commit `6b82328f0d61e4dd3bf330b0cd5d4b825fbf6af6`. The attestation therefore omits the handoff/manifest commits even though their retained public-digest scanner matches require classification. Rebind the manifest and scan attestation to the actual implementation return branch/head and preserve the release as authority/base only.

## IR2 — Governed checkout bytes are not LF self-binding

The combined `.gitattributes` binds the four seam Python files but omits governed post-tokenizer JSON pairs. At minimum, the integration contract/sidecar, synthetic integration fixture/sidecar, combined inventory/sidecar, and integration launch contract/sidecar all report `text: unspecified` and `eol: unspecified`.

This clean helper checkout has `core.autocrlf=true`. The standard-library identity-first wrapper stops before test import with `INSTRUMENT_FAILURE: raw identity specs/data/m4_post_tokenizer_integration_contract_v1.json`; the raw Git contract digest is `9b562397...`, while the transformed worktree digest is `8247b1c8...`. The terminal inventory and launch worktree bytes likewise differ from their raw Git/sidecar identities while Git reports a clean tree. Add exact `text eol=lf` bindings for every governed raw-worktree JSON/sidecar path, reconcile the attribute/wrapper/package/inventory/launch/manifest cascade, and prove a fresh `core.autocrlf=true` checkout runs the identity-first wrapper before import.

## IR3 — Factory and request validation are incomplete

`AdapterFactory.create` performs permissive `json.loads`, role/arm checks, backend lookup, one implementation digest check, and construction. It does not enforce canonical/duplicate-free bytes, the cleared structural schema, complete registry/dependency/model/tokenizer/config identities, or pair identity/isolation at construction. Because candidate and peer are created independently, the factory cannot establish the required twelve equality and six difference fields for the actual pair. Malformed or incomplete manifests can reach construction or incidental `KeyError` instead of governed validation failures.

Lifecycle requests are similarly permissive: missing/empty episode IDs can be accepted, missing `is_terminal_request` becomes false, and operation/caller fields are not structurally validated before backend calls. Implement exact schema-plus-semantic prevalidation with deterministic codes and zero-call boundaries, plus pair construction/validation over the actual candidate and peer.

## IR4 — Receipt validation is fail-open

`BaseAdapter._call` requires only status and three fields for PASS. It accepts arbitrary/non-digest result state tokens, does not require an exact immutable receipt shape or operation-specific payload, and checks episode/request correlation only when the backend elects to include those fields. Omitting correlation fields therefore bypasses correlation. The tests even use a one-character result token as valid.

Require exact per-operation receipt schemas, canonical digest/state-token domains, backend-code consistency, session/prior/result identities, and mandatory request/episode/ordinal correlation before any adapter commit. Add omission, extra-field, type/length/digest, wrong role/arm/request, and operation-payload negatives with exact one-call/no-commit evidence.

## IR5 — Fanout rollback is not backend-atomic

`FanoutCoordinator.step` completes `candidate.step` before calling peer. On peer failure it restores only adapter snapshots (`_state`, `_backend_state`, used episode IDs). It cannot restore state already advanced inside the real candidate backend/session. The adapter is rewound to an old token while the backend may remain advanced. Tests assert adapter durable bytes and call counts only, so this divergence is invisible. The same irreversibility occurs if post-return private-view mutation is detected after a backend step.

Implement a genuine prepare/validate/commit or compensating backend protocol that proves both backend and adapter state are unchanged on candidate/peer/post-return failure. The test backend must be stateful enough to expose partial advancement, and evidence must include exact backend plus adapter pre/post identities.

## IR6 — Reconciliation and fanout evidence are incomplete

Stop validation is optional: sanitized-stop mismatch is checked only when callers supply `expected_sha256`, and stop length is never enforced. Omitting the optional field allows caller-selected metadata that merely matches injected rederivation. Unsupported context length raises raw `ValueError` through `expected.index` instead of a governed first-failure code. Candidate and peer arguments are unused during phase-one binding.

The successful fanout result exposes one private digest but omits the bound sanitized candidate/peer received-digest identities/equality evidence, runtime/session association, request/context receipt fields, and stop receipt. Make the sanitized result schema exact, require all stop/context fields unconditionally, bind projections to the actual adapters, and add omission/unsupported-context/output-shape negatives.

The claimed exact synthetic fixture is only raw-hash checked by the wrapper; production and tests never parse or execute it. Its `tampered_private_rederivation` row expects `TOKEN_ARRAY_DIGEST_MISMATCH`, while production and tests use `SANITIZED_RESULT_DIGEST_MISMATCH`. Its `created_closed_true` row expects `STATE_SEMANTIC_FAILURE`, but no state-semantic validator or test exists. Its declared three-candidate/three-peer sequence is replaced by independent fresh-pair positives. Execute every fixture row/sequence through production paths and require exact fixture projections rather than leaving the artifact disconnected.

## IR7 — Law validation does not enforce law fidelity

`validate_laws` checks uniqueness/order and only a subset of HELD fields. It does not require exact law-specific meaning source, held reason, complete row field set, or valid PASS/FAIL/NOT_RUN evidence/failure shapes. Arbitrary HELD reasons and empty positive rows can pass. `held_law_projection` happens to emit the intended rows, but downstream validation does not protect them from mutation.

Validate every field and status-specific shape against the exact L7/L8/L10/L14/L18 contract, including exact v2 source references and held reasons, with one mutation kill per field/status branch. Preserve the separation from Q2/EF3/native-L8/science.

## Public safety, regression, and disposition

No private path/value, custody content, model/tokenizer bytes, token array, seed, score, or scientific output was found. Review preflight findings F000001–F000014 comprise twelve duplicate-domain fixed-regex personal-contact matches wholly inside required immutable public commit/artifact SHA values and two duplicate-domain gitleaks generic-key matches on the required cleared-tokenizer commit identity. All are public reproducibility metadata, manually classified here; none is suppressed and no credential/contact data is present. No held execution or data access occurred.

**COMBINED BLOCK.** Return one batched IR1–IR7 remediation through WORKFLOW COORDINATOR. Preserve the exact 63-row raw identity evidence, all verified sidecars, the consumed tokenizer PASS pair, banked lifecycle/negative evidence, and every standing hold.
