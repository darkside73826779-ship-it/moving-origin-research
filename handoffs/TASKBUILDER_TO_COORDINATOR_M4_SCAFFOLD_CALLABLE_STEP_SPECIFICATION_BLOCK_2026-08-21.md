# TASK BUILDER to WORKFLOW COORDINATOR — M4 Scaffold Callable-Step Specification Block

**Date:** 2026-08-21

**Regime:** B

**Work item:** A only — M4 scaffold-with-stubs implementation re-release

## Authoritative inputs reviewed

- Rebecca re-release: `coordinator/m4-scaffold-rerelease-tokenizer-custody` at `45d40d8b688fb7f44098d235df7f31cca1aa3b31`.
- Approved ARCHITECT head: `architect/m4-model-agnostic-scaffold` at `ade99fc13dc750b789d254316b9a7dc5de2eae8b`.
- Approved specification result: `7f3db1f9552cf87de205b0635882402e0e1be5d4`.
- Persistent-CRITIC CLEAR: `critic/m4-scaffold-cf1-cf3-rereview` at `deb49bb342a39d3ec25834a4a59b5b21a697d966`.
- Primary specification: `specs/m4_model_agnostic_scaffold_spec_v1.md`.
- Callable supplement: `specs/data/m4_model_callable_fixture_v1.json`.
- Base and supplemental fixtures: `specs/data/m4_model_scaffold_executable_fixture_v1.json` and `specs/data/m4_model_scaffold_rf1_rf3_fixture_v1.json`.

## Disposition

**SPECIFICATION BLOCK — callable step artifacts are mutually incompatible. No implementation is retained or pushed.**

The callable contract is executable through `describe`, `initialize`, and `reset_episode`: independent construction reproduced the committed operation-result digests and the committed created/described/initialized/ready state digests. The first authorized callable `step` cannot satisfy all normative fixture requirements simultaneously.

## Reproduced passing prefix

- `describe` operation-result SHA-256: `ef9f21b2285421d07b6c6ec69db1f2aed577738a329c24a23fcaaa8d48033633` — matched.
- `initialize` operation-result SHA-256: `08d4eaa0dbcba18d1af412ecee31da9772369d5be5d9ea883785803f84bb47b0` — matched.
- Initialized state SHA-256: `c33f0828e81afe0e7503b10f895f91a74bae9affe9b7a7874616581d1627af78` — matched.
- `reset_episode` operation-result SHA-256: `4e78341f4fe152277bc10f3e4e2c87c7417dace9d724c4163254273347938b40` — matched.
- Ready state SHA-256: `cf16e09282530ea32e8d5a775962ea06f28013117b0942faf637e48deda0add8` — matched.

## Exact callable-step conflicts

1. The normative reset request establishes state episode ID `callable-episode-0`. The normative varying candidate request also uses `callable-episode-0`, as required by the configuration rule. However, the normative varying response digest `7df9f5f82ba4f30bdc04218ddec2d6fbf48fb6d3a42240f3385af4c006077309` reconstructs only when the response retains base-fixture episode ID `stub-episode-0`. Replacing it with the request-correlated `callable-episode-0` changes the digest.
2. The same normative varying response digest reconstructs only with legacy envelope values `state_before_sha256 = 7777…7777` and `state_after_sha256 = 8888…8888`. Using the callable ready-state digest `cf16e092…` and callable stepped-state digest `55aa8bc2…` changes the response digest. This contradicts the callable state contract and the request-correlated-envelope rule.
3. The normative callable stepped state fixes `last_response_sha256 = 80c5faf6759fe60df9d38ecc39cb85832f649057ac5acf02118110638ba4a2e9`, the base candidate response digest. The callable varying response is fixed to `7df9f5f8…`. A successful varying-input step therefore cannot both record its actual response digest and reproduce the normative stepped-state digest `55aa8bc2737bad24417f63fb407c52c6d53702f416b8ab7da24f1783f443055c`.
4. More generally, the specification requires a response to carry `state_after_sha256` while the complete post-state carries `last_response_sha256`. If each value hashes the complete artifact containing the other, the construction is cyclic. No ordering, placeholder, projection, wrapper, or excluded-field digest domain resolves that cycle. Selecting one would invent a state/response hashing rule.

## Verification evidence

An exhaustive check over the two relevant episode IDs (`stub-episode-0`, `callable-episode-0`), the legacy and callable pre-state digests, and the legacy and callable post-state digests produced eight response constructions. Only the legacy tuple (`stub-episode-0`, `7777…7777`, `8888…8888`) reproduced `7df9f5f8…`; none of the callable-state combinations matched.

## Files and execution status

- Implementation files retained: none.
- Tests or diagnostic artifacts committed: none.
- Synthetic verification performed: only the prescribed fixture reconstruction needed to locate this contract contradiction.
- Seeds accessed or exposed: none.
- Model/tokenizer artifacts accessed: none.
- Scientific specifications, thresholds, state, or provenance modified: none.
- TASK BUILDER-authored repository artifact: this durable block only.

## Holds and routing

Return Work Item A separately to **WORKFLOW COORDINATOR** for verification and routing to persistent **ARCHITECT** for deterministic closure of the response/state digest domains and callable step fixtures, followed by persistent-CRITIC review and any required Rebecca re-release.

No scaffold implementation, model activity, tokenizer activity, acquisition/preflight, qualification, diagnostics/scoring, protected-seed access, native-CUDA L8, state/provenance mutation, merge, rerun, or gate decision is authorized from this block.

## Public-repository safety attestation

Public-safety scan: gitleaks scanned the complete two-commit introduced range and found zero leaks. Credential, secret, private-key, environment-dump, and private-absolute-path regex review found zero prohibited content. Email-pattern review found four commit-metadata matches: the repository's existing GitHub noreply author identity and the non-personal TASK BUILDER role identity; both were classified acceptable, not personal contact details. Manual review found only repository SHAs, canonical fixture digests, governance terms, and the synthetic contract contradiction; all were classified acceptable. `git diff --check` passed.
