# CRITIC M4 Post-Tokenizer IR1–IR7 Rereview

Date: 2026-08-22 EDT

Regime: B

Role: authoritative persistent CRITIC

Terminal state: **COMBINED BLOCK**

## Immutable intake and banked closure

- Package head: `taskbuilder/m4-post-tokenizer-ir1-ir7-remediation @ 232c4e93ae4061e7190079e8797f4ba3aa46dad7`
- Implementation result: `c7bc800b9500af260c59dd81d917058eb58f11dc`
- Handoff/quality result: `342171993600360c3146030aa893b5a364cb82c2`
- Prior authoritative BLOCK: `critic/m4-post-tokenizer-integration-implementation-review @ 7b88242f96a7ff1004cc5b0b97d3339cac7b8969`
- Helper checkout receipt SHA-256: `1ac5ff30b332691e6fef0976f9098055f6530ed15b7f39cb0992c751df38ddb5`

The canonical handoff manifest validates, and all fourteen declared raw artifact hashes reproduce. Base, implementation result, routing result, scan tip, branch, and terminal head form the declared ancestry. The combined inventory remains exactly 63 rows with zero mode/blob/size/SHA mismatches; all 25 contained sidecars verify. All 35 TOKENIZER rows remain byte-identical to cleared source `ddae7c3b8f664cbc94654198916e1940c9006c1e`, including the consumed PASS pair. Only the three declared REBOUND rows changed.

IR1 launch/topology and IR2 LF binding are banked closed. The launch contract contains exactly one `${MOR_RELEASED_CHECKOUT}` read-only bind and rejects empty/unrealized sources before process start. All eight governed integration JSON/sidecar paths have exactly one `text eol=lf` binding. In this clean `core.autocrlf=true` checkout, worktree bytes equal raw Git blobs. The exact identity-first wrapper ran 40/40 PASS. The 42-cell lifecycle suite remains present. The reported pinned 40/40 integration and banked 37/37 tokenizer results remain corroborating; no held runtime was invoked in this rereview.

## RIR1 — Pair construction can leak a half-created runtime

`AdapterFactory.create_pair` constructs the candidate backend and adapter, then constructs the peer, and only afterward validates pair equality/isolation. If peer construction/registry validation or final pair validation fails, the already-created candidate backend/session—and possibly peer—is neither closed nor rolled back. The comment prevents returning one half but does not prevent a live leaked half.

Validate the complete candidate/peer manifest and config pair before either backend constructor is invoked, or provide an exact cleanup transaction that proves zero live backend/session state on every second-half or pair-validation failure. Also bind constructed backend session identity to the claimed distinct runtime identities before returning. Preserve deterministic `ROLE_ARM_MISMATCH` and `PEER_CHANNEL_BYPASS` projections instead of shadowing them with generic difference-field collapse.

## RIR2 — State semantic validation is disconnected and incomplete

`validate_state` is not called by adapter operations. The function itself rejects the single fixture mutation `CREATED + closed=true` but permits other impossible objects: unknown lifecycle values; early states with completion/nonzero ordinals; EPISODE_READY with inconsistent request/response state; STEPPED with missing or malformed response digest; and CLOSED with inconsistent episode/ordinal fields.

Define the exact cross-field state machine for every lifecycle state, validate it before and after every public transition and restore, and add one mutation kill for each field/state relation. Fail before backend access when the pre-state is semantically invalid.

## RIR3 — Backend rollback is trusted, not verified

The new transaction protocol calls `backend.capture_state()` and later `backend.restore_state(snapshot)`, but production never captures the backend again and compares it to the authoritative snapshot. A backend may return successfully from a no-op or partial restore; the adapter is then rewound while the real backend remains advanced, and rollback is reported as successful. Cooperative `SpyBackend` tests cannot prove fail-closed behavior against this adversary.

Require a canonical backend-state identity or rollback receipt and verify it after every restoration. A mismatch or unverifiable restoration must project `BACKEND_ROLLBACK_FAILURE` without claiming atomic restoration. Cover candidate 1/0, peer 1/1, post-return mutation, and every receipt/exception rollback with no-op, wrong-state, and throwing restorers.

## RIR4 — Law status semantics remain underspecified

The law validator now enforces exact fields, sources, held reasons, and PASS evidence key names, but status-specific content is still weak. PASS accepts an empty/arbitrary metrics object; FAIL accepts any nonempty evidence list and arbitrary metrics; NOT_RUN accepts any single evidence value and any string beginning `INSTRUMENT_FAILURE:` and does not require empty metrics. Tests exercise PASS/FAIL/NOT_RUN only for L7 and omit metrics mutation.

Bind exact law-specific metric schemas and failure/instrument evidence identities for L7/L8/L10/L14/L18. Exercise every status for every law, including extra/missing/wrong-type metrics and unbound evidence artifacts. HELD/no-claim rows remain banked.

## RIR5 — Exact fixture sequence/boundaries are not fully realized

The fixture is now parsed and its three-candidate/three-peer fanout calls run, and all thirteen negative IDs receive the declared code. However, the fixture-driven sequence asserts `exercise_close_paths` without dispatching close operations in that sequence; separate legacy close tests do not prove the fixture trace. Most fixture negatives also record only the raised code, not their declared zero backend calls and `expected_state_mutation=false` boundary.

Use an explicit fixture dispatcher that executes every sequence entry in order and records exact candidate/peer/control calls plus pre/post adapter and backend identities for every negative row. Compare the complete realized trace to the fixture, not only its ID→code map.

## RIR6 — Fanout evidence rereads private input after execution

After both backends return, the sanitized fanout receipt computes `length` by calling `self.provider(context_length)` a second time. A stateful or nondeterministic provider can return different private data, so the public receipt may describe a different array than the bytes validated and delivered. The second call is not revalidated and violates the frozen phase-one evidence boundary.

Return verified length/digest metadata from phase one and build the receipt solely from that immutable snapshot. Add a provider that changes on its second call and prove it cannot alter evidence or trigger ungoverned private re-access.

## Public safety and disposition

No private path/value, custody content, model/tokenizer bytes, token arrays, seeds, scores, or scientific output were found. Review preflight findings F000001–F000004 are duplicate scan-domain fixed-regex personal-contact matches wholly inside two required immutable commit identities on lines 15 and 19; all four are non-contact reproducibility metadata, manually classified here, and none is suppressed. Gitleaks findings are zero. Package-range scanner matches remain classified as public immutable identity/hexadecimal substrings. No materializer, custody, model/tokenizer, inference, scoring, seed, science, durable-state, merge, publication, or gate action occurred.

**COMBINED BLOCK.** IR1–IR2 infrastructure closure and all exact identity/regression evidence are banked. Return one batched RIR1–RIR6 semantic remediation through WORKFLOW COORDINATOR, preserving the 63-row inventory, sidecars, 40-test wrapper, 42-cell matrix, tokenizer PASS pair, and every standing hold.
