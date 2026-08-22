# TASK BUILDER quality trace — M4 post-tokenizer IR1–IR7

Date: 2026-08-22 EDT

Implementation: `taskbuilder/m4-post-tokenizer-ir1-ir7-remediation @ c7bc800b9500af260c59dd81d917058eb58f11dc`

## Requirement → production branch → test → evidence

| Row | Production branch | Public/production test evidence | Result |
|---|---|---|---|
| IR1 exact launch bind | `realize_launch_command` requires one literal released-checkout placeholder, an absolute existing checkout, and realizes one read-only `/workspace` bind before subprocess use | `test_launch_contract_realizes_exact_read_only_bind_before_process`; exact committed OCI command | PASS |
| IR1 return routing | Final return uses the actual taskbuilder branch; implementation result is `c7bc800...`; the handoff commit becomes the routing SHA; the canonical manifest is committed after that handoff | schema validator plus remote-equality check | PASS |
| IR2 eight LF paths | Eight exact integration/fixture/inventory/launch JSON and sidecar paths have explicit `text eol=lf`; the wrapper rejects CR, missing LF, bad sidecars, inventory drift, launch-count drift, and placeholder drift before import | fresh detached `core.autocrlf=true` wrapper, 40/40 PASS | PASS |
| IR3 canonical coupled factory | `AdapterFactory.create` rejects noncanonical bytes and validates exact structure, complete manifest identities, registered implementation/dependency/config identities, model/tokenizer linkage, role/arm, and production-path policy; `create_pair` validates the full equality/difference relation before returning either adapter | canonical/config/dependency mutations and coupled-pair mutation through `create`/`create_pair` | PASS |
| IR3 lifecycle request completeness | `_validate_request` requires nonempty operation/caller identifiers and exact per-operation episode/ordinal/context/terminal types before backend calls | every required field omitted separately across describe/initialize/reset/step; zero matching backend calls | PASS |
| IR4 exact receipts | `_call` accepts only the seven-field PASS/FAIL receipt, exact types, 64-lower-hex state/request tokens, registered FAIL code, session/prior state, request digest, and step ordinal | omission, extra field, status type, backend-code mismatch, short digest, bool ordinal, request-digest, session, prior-state, and declared-failure cases | PASS |
| IR5 real backend rollback | Each adapter transaction captures/restores the backend’s real opaque state plus adapter state; fanout restores candidate and peer on candidate, peer, or post-return failure | stateful backend divergence assertions for 1/0, 1/1, and post-return 1/1 traces | PASS |
| IR6 stop/fanout receipt | Phase one requires exact stop shape, digest, and length; unsupported context is governed; success returns complete sanitized prompt/stop/request/runtime/candidate/peer/law evidence | stop omission/length/digest, unsupported context, exact receipt-field test | PASS |
| IR6 executable fixture | The committed fixture is parsed; its exact ordered sequence runs through factory-created candidate and peer adapters; three candidate and three peer step calls execute; each of 13 declared negatives is realized separately | `test_fixture_is_parsed_and_every_declared_row_and_sequence_executes` | PASS |
| IR7 law semantics | `validate_laws` enforces exact row fields, order, source, law-specific HELD reason, full PASS evidence, allowed FAIL code/evidence, and NOT_RUN instrument reference | HELD positive plus PASS/FAIL/NOT_RUN positives and field/status mutations | PASS |
| Banked tokenizer | Only the `.gitattributes`-dependent tokenizer wrapper/executable-package identities were rebound; materializer and tokenizer behavior remain unchanged | exact pinned custody-free OCI suite 37/37 PASS | PASS |

## Ordered access and rollback trace

1. Canonical manifest/config bytes and complete registry/model/tokenizer/dependency identities are validated.
2. Candidate and peer are constructed as a coupled pair and their equality/difference fields are validated.
3. Lifecycle request structure and semantics are validated before any backend call.
4. Sanitized context order, prompt length/digest, mandatory stop length/digest, request context, immutable candidate/peer views, and received equality are validated before either step call.
5. Candidate backend transaction snapshot is captured; candidate executes once and its receipt is validated without adapter commit on failure.
6. Peer executes once; any peer failure restores both real backend snapshots and both adapter snapshots.
7. Post-return integrity is checked; failure restores both real backends and adapters.
8. Only after all checks pass are the complete sanitized fanout receipt and exact law projections returned.

Observable stateful-spy evidence proves adapter and real backend state are byte/structure identical to their pre-call captures for candidate failure, peer-after-candidate failure, and post-return failure.

## Verification summary

- Fresh `core.autocrlf=true` detached checkout at `c7bc800b9500af260c59dd81d917058eb58f11dc`: identity-first wrapper 40/40 PASS; worktree clean.
- Exact pinned Linux/amd64 image `docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`, `--pull=never`, network none, read-only repository/root, capability drop, no-new-privileges, bounded noexec tmpfs: integration 40/40 PASS.
- Same pinned custody-free controls: banked tokenizer 37/37 PASS.
- Complete 42-cell lifecycle matrix remains exercised through public methods.
- Adversarial checks cover status, failure code, terminal receipt shape, ordered context, request/receipt correlation, access boundary, rollback, stop identity, fixture rows, and law semantics.
- Combined raw inventory SHA-256: `848ba82d2e35cadb4e042356aaf79948e488aaca2803db50f11cc37a9544b1dd`.
- Integration launch contract SHA-256: `11ae4799b6be6f0f14a5768a53fbf66b39b32d77e114a1ea581053fd8a3b6934`.
- Rebound tokenizer executable package SHA-256: `ee5f7bc601d94153d5819453d2f22a8fc6110103c88bd8242ac3ebe5c78ea2bc`.
- Materializer invocations and private custody/model/tokenizer accesses: zero.

## Public-safety classification

The implementation-range preflight retained 71 duplicate-domain `personal_contact` heuristic findings. Independent inspection found only numeric substrings wholly inside required public Git/SHA identities or the literal hexadecimal alphabet; no contact data is present. Gitleaks retained six domain findings representing three unique `generic-api-key` matches: the two public source/test SHA-256 identities embedded by the identity-first wrapper and the required cleared-tokenizer Git commit in the combined inventory. No secret is present. All findings remain visible and were manually classified; none was suppressed.
