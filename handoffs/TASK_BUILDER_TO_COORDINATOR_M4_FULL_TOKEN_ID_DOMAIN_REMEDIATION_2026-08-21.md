# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 FULL TOKEN-ID DOMAIN REMEDIATION

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

## Canonical intake

- Implementation input: `taskbuilder/m4-tokenizer-topology-clear-materialization-execution` at `0aadbc2b120cc5cf60386775cc8d61535d722c96`.
- Consumed FAIL result/handoff commit: `67d631cdde1572fc2906b638e14d8bc05ecbf45d`.
- Authoritative classification: `critic/m4-tokenizer-materialization-execution-review` at `50e29690ccc89c51300ce1ac6c21bfbd23b2d926`.
- Work branch: `taskbuilder/m4-tokenizer-full-token-id-domain-remediation`.

## Implementation result

The production materializer now computes the complete valid token-ID domain exactly once from the authenticated tokenizer as `frozenset(tokenizer.get_vocab().values())`. Each constructed value must satisfy all three predicates: exact `int` type, nonnegative value, and membership in that complete domain. The uncontracted `item >= tokenizer.vocab_size` rejection is removed. The later decode→re-encode equality checks remain unchanged.

Every construction fake now models added-token semantics explicitly: base `vocab_size` is `100`, while valid added/special ID `151645` is present in `get_vocab()`. No fake retains the masking `vocab_size=200000` value.

The executable-package manifest and sidecar bind the corrected materializer and selected-test raw Git blobs and record the prior operation as **CONSUMED**. The committed FAIL pair and its provenance are unchanged.

## Requirement → production branch → test → evidence trace

| Requirement | Production branch | Test/evidence | Result |
|---|---|---|---|
| Preserve consumed FAIL pair/provenance | no edits under `artifacts/m4_tokenizer_materialization/` or prior execution handoffs | raw Git-blob comparison against input; result SHA-256 remains `10a14c1a4f7b257aa195636ab86b7a85a68fc084af13bead7b5d4b3ecfa55728` | PASS |
| Compute full valid domain exactly once | one `frozenset(tokenizer.get_vocab().values())` after authenticated loader/template checks | positive fake call counter equals one; source audit finds exactly one production call | PASS |
| Exact-int, nonnegative, full-membership predicate | sole production array predicate | source/fake audit plus negative production matrix | PASS |
| Valid added token above base size proceeds | production `materialize()` with added special ID `151645`, base `vocab_size=100`, full-domain membership | `test_materialize_synthetic_positive_reaches_pass`; all `ARRAY_1024/4096/8192` and `ENCODE_DECODE_1024/4096/8192` checks PASS | PASS |
| Positive nonmember fails first array | production `materialize()` with `777` excluded from full domain | `nonmember` subcase: exit `3`, `CONSTRUCTOR_INVARIANT_FAILURE`, terminal `ARRAY_1024`, `arrays=[]`, zero decode | PASS |
| Negative ID fails even when present in reported domain | production `materialize()` with `-1` included in fake `get_vocab()` | `negative` subcase: exact governed first-array projection, empty arrays, zero decode | PASS |
| Boolean fails exact-int even when present in reported domain | production `materialize()` with `False` included in fake `get_vocab()` | `bool` subcase: exact governed first-array projection, empty arrays, zero decode | PASS |
| Non-int fails exact-int even when present in reported domain | production `materialize()` with string ID included in fake `get_vocab()` | `non_int` subcase: exact governed first-array projection, empty arrays, zero decode | PASS |
| Preserve round-trip mismatch behavior | unchanged later encode/decode branches | existing 1024/4096/8192 mismatch cases retain `ENCODE_DECODE_IDENTITY_FAILURE` | PASS |
| Audit every construction fake | AST audit of every class implementing `apply_chat_template` | all six construction fakes expose `get_vocab()` and base size below the added special ID | PASS |
| Preserve banked package behavior | complete exact pinned, network-disabled, read-only, no-custody wrapper | 37 tests run, 37 passed, exit `0` | PASS |

## Adversarial mutation evidence

Each mutation was applied only in an isolated disposable worktree at the implementation commit and tested through the pinned production-path regression. Every mutated run returned nonzero as required; the disposable worktree was removed afterward.

| Mutation | Target regression | Observed exit | Result |
|---|---|---|---|
| Restore old `item >= tokenizer.vocab_size` ceiling | added-token positive | `1` | KILLED |
| Remove full-domain membership | negative matrix | `1` | KILLED |
| Weaken exact-int to `isinstance(item, int)` | negative matrix with in-domain boolean | `1` | KILLED |
| Remove nonnegative predicate | negative matrix with in-domain `-1` | `1` | KILLED |

## Ordered boundary trace

`authenticated tokenizer load → template identity → base/user/neutral construction → insertion and neutral checks → one full-domain snapshot → ARRAY_1024 exact-int/nonnegative/membership → round-trip → ARRAY_4096 exact-int/nonnegative/membership → round-trip → ARRAY_8192 exact-int/nonnegative/membership → round-trip → unchanged stop/publication checks`

Negative subcases stop at the first array predicate before decode, later arrays, row append, stop construction, or partial result arrays. Existing pre-access runtime/custody boundaries, atomic publication, topology, failure projection, and preservation tests remain passing.

## Preserved boundaries and route

- The prior materialization operation remains **CONSUMED**. No materializer, OCI topology runner, private binding, custody/model/tokenizer input, inference, qualification, diagnostics/scoring, protected seed, science, STATE/provenance mutation, merge, or gate decision occurred.
- **Exact next recipient:** WORKFLOW COORDINATOR for routing of this one canonical implementation package to the authoritative persistent CRITIC for rereview.
