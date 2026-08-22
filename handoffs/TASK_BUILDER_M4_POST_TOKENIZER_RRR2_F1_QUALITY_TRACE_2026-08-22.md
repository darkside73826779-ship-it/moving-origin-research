# M4 post-tokenizer RRR2-F1 strict cleanup-attestation quality trace

Date: 2026-08-22 EDT

Implementation: `a7e74c110ae32be0ea8918c9b0c037424fbf9b32`

## Requirement → production branch → test → evidence

| Requirement | Production branch | Production-path test | Evidence |
|---|---|---|---|
| Accept only literal Boolean `False` as verified post-disposal non-liveness | `AdapterFactory._dispose_verified` | `test_factory_requires_live_attestation_and_cleans_each_role` | After `dispose()`, the result of `is_live()` is captured once and must satisfy `is False`. `None`, integer `0`, empty tuple, `True`, and exceptions all project `BACKEND_ROLLBACK_FAILURE`; literal `False` alone permits the caller's role-specific NOT_LIVE projection. |
| Realize every named falsey non-Boolean separately through production construction | `AdapterFactory.create_pair`, `_construct`, `_attest_live`, `_dispose_verified`, and `AdapterFactory.create` | candidate `None`, peer `0`, control empty-tuple subcases in `test_factory_requires_live_attestation_and_cleans_each_role` | Candidate, peer, and control each begin with a throwing liveness probe, execute real disposal, then return the assigned falsey non-Boolean. Every subcase asserts exact `BACKEND_ROLLBACK_FAILURE`, exact constructed-backend count, and real backend live residue equal to literal `False`; the peer case also proves the already-live candidate is disposed. |
| Prove strict identity cannot regress to truthiness | canonical mutation runner, contract, and transcript | `RRR2_F1_TRUTHINESS_WEAKENING` invokes the production factory test | The exact mutation changes `if live_after_disposal is not False` to `if live_after_disposal`. It is killed, its mutant SHA-256 and fully qualified command are committed, and transcript equality reproduces in the exact pinned container. |
| Preserve RRR1/RRR3 and all banked boundaries | fanout, lifecycle, law, rollback, fixture, pair, wrappers, inventory, tokenizer bank | full integration, mutation, and tokenizer suites | The public fanout capability closure, exact eventual-request binding, law/history/rollback/fixture/frozen-provider/pair boundaries, 42 lifecycle cells, 13 fixture negatives, and tokenizer evidence all remain passing. |

## Ordered cleanup traces

1. Throwing liveness probe → enter cleanup → call `dispose()` → call `is_live()` exactly once for post-disposal observation → literal `False` → raise the role-specific `CANDIDATE_BACKEND_NOT_LIVE`, `PEER_BACKEND_NOT_LIVE`, or `CONTROL_BACKEND_NOT_LIVE` from `_attest_live`.
2. Throwing liveness probe → dispose real backend → post-disposal observation is `None`, `0`, empty tuple, `True`, or raises → `BACKEND_ROLLBACK_FAILURE`; no role-specific NOT_LIVE result is minted from an unauthenticated observation.
3. Peer construction failure → peer cleanup attestation fails closed → outer pair transaction disposes and verifies candidate → propagate `BACKEND_ROLLBACK_FAILURE` with both real live flags literal `False`.

## Adversarial and mutation evidence

- Candidate post-disposal `None`: exact rollback failure; one constructed backend; real live flag literal `False`.
- Peer post-disposal integer `0`: exact rollback failure; candidate and peer both disposed; both real live flags literal `False`.
- Control post-disposal empty tuple: exact rollback failure; one constructed backend; real live flag literal `False`.
- Banked no-op, partial, throwing-dispose, always-throwing probe, literal-`True`, ordinary dead, and literal-`False` paths remain covered.
- Canonical mutation set: 15/15 KILLED, including `RRR2_F1_TRUTHINESS_WEAKENING`.

## Exact verification

- Fresh `core.autocrlf=true` identity-first wrapper: 49/49 PASS.
- Exact pinned WSL2-backed OCI image, network disabled, read-only checkout, no custody: integration 49/49 PASS.
- Same exact pinned OCI/no-custody controls: mutation replay 15/15 KILLED; canonical transcript equality PASS.
- Same exact pinned OCI/no-custody controls: banked tokenizer suite 37/37 PASS.
- Complete lifecycle matrix: 42/42 cells PASS.
- Exact fixture sequence plus 13/13 negatives: PASS.
- Combined inventory: 68/68 raw identities and 27/27 sidecars reproduce.
- Source SHA-256: `8964de5daf745226771818ab59f2cc75ef29ccbc5d09b43b6dae102b876b2f1b`.
- Test SHA-256: `9878ec7b6c2e8f5c81bd2944e5c811cc1fcdc38a712e4607ce351c6177b18962`.
- Wrapper SHA-256: `0dbac4ce0361c2b5750e5d3000609a430da972b5f1db968cca10b9ff0d2d7d49`.
- Mutation contract SHA-256: `aa6855f2d47ac02792da96ccb4a7d638bc855012414e8cd4e0f2fbdd7a2f3fcd`.
- Mutation transcript SHA-256: `d74056396156ac96f10b5853bfc45ef3d9585c276aa71da45ced00e6cb40e265`.
- Combined inventory SHA-256: `21b46b6f68bf823900346ac07e39d181ea8b61d1854fb3dc7c30c9651c499181`.
- Launch-contract SHA-256: `d822d7bba8170e04f33592fd9cb5183a114e9de3e7e46bfcb34717c5c30b15c0`.
- `git diff --check` and `git fsck --full`: PASS; fsck reports only unreachable local development objects.
- Tokenizer/materializer invocation and private custody/model/tokenizer access: zero.
