# CRITIC M4 Full Token-ID Domain Implementation Rereview

Date: 2026-08-21 EDT  
Regime: B  
Role: authoritative persistent CRITIC  
Terminal state: **COMBINED CLEAR**

## Immutable intake and validation

- Canonical branch/head: `taskbuilder/m4-tokenizer-full-token-id-domain-remediation @ 9d3e123948dfdca111dc730501475ed875abb00a`
- Implementation result: `d8eabeb11ce8366c522b6a4a57f8f9da10606db5`
- Handoff result: `4d0dc257eda52625b7188621c2c2a6eab986986b`
- Base and consumed execution: `0aadbc2b120cc5cf60386775cc8d61535d722c96`
- Authoritative defect classification: `critic/m4-tokenizer-materialization-execution-review @ 50e29690ccc89c51300ce1ac6c21bfbd23b2d926`
- Helper-managed checkout receipt SHA-256: `fb3903d73be2091befe49fcd2f4aa57a32128e593e96883d6bec3f7fe3e67551`

The canonical handoff manifest validates with the merged workflow contract validator. All 22 declared raw Git-blob SHA-256 identities reproduce exactly. The substantive delta is limited to the production materializer, selected tests, executable-package JSON/sidecar, and the two handoff artifacts; `git diff --check` is clean.

The permanently consumed FAIL result remains byte-identical to the execution input: 1,740 bytes and SHA-256 `10a14c1a4f7b257aa195636ab86b7a85a68fc084af13bead7b5d4b3ecfa55728`. Its 97-byte sidecar is likewise byte-identical at SHA-256 `da7a294daf21aa308cb0b7ac83dafba85323c2e0667a33a0844829a18b86756a`. The executable-package record correctly changes the operation state from its pre-execution value to **CONSUMED** and binds the corrected materializer and test bytes.

## Production correction

The implementation closes the confirmed defect exactly. After the already governed tokenizer/runtime/template identity gates and before any array row is constructed, production takes one immutable snapshot:

`valid_token_ids = frozenset(tokenizer.get_vocab().values())`

Every constructed ID must then satisfy all three predicates: `type(item) is int`, `item >= 0`, and membership in that snapshot. The unauthorized `item >= tokenizer.vocab_size` base-vocabulary ceiling is absent. This is the lawful full tokenizer-ID-domain interpretation required by the cleared specification and the prior authoritative classification: it admits authenticated added tokens while failing closed on negative, non-integer, Boolean, gap, and other nonmember values. Decode/re-encode equality and all later publication checks remain unchanged.

`get_vocab()` lookup is evaluated exactly once. `AttributeError` and `TypeError` at snapshot construction map to the governed first-array `CONSTRUCTOR_INVARIANT_FAILURE`; no partial array is published. The six construction fakes all model the relevant realism boundary with base `vocab_size=100`, an authenticated added/special ID `151645`, and an explicit `get_vocab()` domain. No inflated fake base vocabulary masks the corrected edge.

## Independent executable and regression evidence

An independent custody-free focused run through production `materialize()` passed five selected test methods covering:

- valid added-token ID above base `vocab_size`, with all three array and all three round-trip checks passing;
- nonmember integer, negative integer, Boolean, and non-integer values, each stopping at `ARRAY_1024` with exit `3`, `CONSTRUCTOR_INVARIANT_FAILURE`, `arrays=[]`, and zero decode;
- one-snapshot behavior, source/fake audit, constructor negatives, insertion uniqueness, neutral-fragment length, and stop-array preservation.

Result: **5/5 selected methods PASS** (the negative matrix contains four separately asserted subcases).

The exact full wrapper was also invoked in the available WSL interpreter. All five remediation-relevant methods passed during that discovery run, but the overall wrapper was not a valid pinned reproduction because the interpreter lacks the required Transformers distribution/version and loader identity; unrelated banked runtime/custody tests therefore failed at the pre-custody runtime-identity boundary. This environment limitation is not treated as contrary package evidence. No OCI, private binding, custody, model, or tokenizer input was accessed. The canonical handoff's exact pinned, network-disabled, read-only, no-custody evidence reports 37/37 PASS and four isolated mutation kills; its commands, identities, and claimed outcomes are consistent with the inspected code and targeted independent results.

The four mutation claims are adequately targeted: restoring the base ceiling breaks the added-token positive; removing membership admits the nonmember; weakening exact-int admits the in-domain Boolean; removing nonnegative admits the in-domain `-1`. Each is directly guarded by the focused production-path tests rather than a source-only assertion.

All preexisting round-trip, failure-projection, atomic-pair, runtime-identity, custody, topology, and public-safety branches are byte-unchanged outside the selected-test adjustments and package rebinding. No regression or law-fidelity conflict was found.

## Law fidelity, public safety, and disposition

The correction implements the active specification's “outside tokenizer vocabulary” rule as exact authenticated-domain membership, consistent with the binding architectural requirements for exact identities, fail-closed execution, deterministic evidence, and no silent substitution. It does not alter scientific meaning, held inputs, execution authority, or the permanent consumed result.

Public review found no credentials, personal contact data, private paths, custody values, model/tokenizer bytes, complete token arrays, protected seeds, scores, or scientific output. Preflight reported 15 fixed-regex duplicate-domain personal-contact findings wholly inside required public commit/artifact SHA identities; these are non-contact reproducibility metadata. Its two gitleaks generic-key findings are duplicate-domain occurrences of the declared public AutoTokenizer loader-file SHA-256, a public artifact identity rather than a credential. All 17 findings are manually classified here and none is silently suppressed.

**COMBINED CLEAR.** The prospective implementation/package is fit to return to WORKFLOW COORDINATOR. This CLEAR does not authorize a new materialization operation, retry, private execution, merge, publication, or gate decision. The prior operation remains **CONSUMED**; any new operation requires a separate exact release.
