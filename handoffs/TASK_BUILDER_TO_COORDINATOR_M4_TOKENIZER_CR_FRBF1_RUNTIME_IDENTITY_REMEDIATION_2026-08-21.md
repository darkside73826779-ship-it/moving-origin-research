# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER CR-FRBF1 RUNTIME IDENTITY REMEDIATION

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

**Gate served:** One integrated CR-FRBF1 pre-custody runtime/loading-identity remediation before persistent-CRITIC rereview

## Canonical intake

- Input implementation: `taskbuilder/m4-tokenizer-cr-rbf1-residual-remediation` at `e7810f546b7985145c177e760cd2ca2b29b0b249`.
- Authoritative CRITIC BLOCK: `critic/m4-tokenizer-cr-rbf1-final-rereview` at `1f6107f416a2ad4ce13ed0fcc8e7f0ae8ca2e2be`.
- Review artifact: `reviews/critic_m4_tokenizer_cr_rbf1_final_rereview.md`.
- Work branch: `taskbuilder/m4-tokenizer-cr-frbf1-runtime-identity-remediation`.

## Integrated correction

`materialize` now verifies the pinned Transformers distribution and exact `transformers/models/auto/tokenization_auto.py` regular-file identity before reading the custody environment. The fixed runtime identity is Transformers `4.56.1`, one exact loader path, `56944` bytes, and raw-file SHA-256 `b0cd25702a99bfdf1cd93edcb1f3793a7d422ed5b4f053d4a9e71cf678b79fa0`. Distribution lookup failure and every version/path/kind/size/digest mismatch map to `RUNTIME_IDENTITY_MISMATCH`, terminal `AUTHORITY`, status `FAIL`, exit `3`, with a schema-valid atomic result pair.

The actual `from transformers import AutoTokenizer` and `from_pretrained` call remain after custody and copy checks. A later loader execution exception is distinct: it follows the existing generic internal-error path (`INTERNAL_ERROR`, terminal `PUBLIC_SAFETY`, exit `4`) and is not mislabeled as the pre-custody runtime-identity row.

## CR-FRBF1 requirement → production branch → test → evidence trace

| Requirement / review finding | Production branch | Production-entrypoint test | Exact evidence |
|---|---|---|---|
| Runtime distribution unavailable | `verify_runtime_loading_identity`: distribution lookup exception | `test_materialize_alternate_loader_identity_fails_before_custody` / `distribution_error` | `materialize` returns 3; `FAIL`; `RUNTIME_IDENTITY_MISMATCH`; terminal/prefix `AUTHORITY`; schema-valid JSON/sidecar pair |
| Alternate Transformers version | version equality branch | same / `version` | same governed projection and artifact evidence |
| Missing loader identity path | exact single-path branch | same / `missing_path` | same governed projection and artifact evidence |
| Duplicate/ambiguous loader path | exact single-path branch | same / `duplicate_path` | same governed projection and artifact evidence |
| Non-regular loader file | one `lstat` kind branch | same / `loader_kind` | same governed projection and artifact evidence |
| Wrong loader byte size | same `lstat` size branch | same / `loader_size` | same governed projection and artifact evidence |
| Wrong loader byte digest | raw runtime-file SHA-256 branch | same / `loader_digest` | same governed projection and artifact evidence |
| Reject before every custody/private/model/tokenizer/loader action | `verify_runtime_loading_identity()` precedes `os.environ.get(ENV)` and all later access | all seven subcases above | forbidden-event spies raise on custody-env lookup, root resolution, private-record read, weight `lstat`, tokenizer/config read or copy, loader import, or `from_pretrained`; none fires |
| Do not conflate post-access loader exception | later import/`from_pretrained` has no `RUNTIME_IDENTITY_MISMATCH` catch | `test_materialize_serialization_public_safety_and_runtime_negatives` | injected later loader exception produces distinct `INTERNAL_ERROR`, `PUBLIC_SAFETY`, exit 4 |

## Ordered access-event evidence

The production test records events in call order and asserts exact equality, so any extra or reordered forbidden access fails:

- `distribution_error`: `[runtime_distribution]`
- `version`: `[runtime_distribution]`
- `missing_path`: `[runtime_distribution]`
- `duplicate_path`: `[runtime_distribution]`
- `loader_kind`: `[runtime_distribution, runtime_loader_lstat]`
- `loader_size`: `[runtime_distribution, runtime_loader_lstat]`
- `loader_digest`: `[runtime_distribution, runtime_loader_lstat, runtime_loader_read]`

Every trace excludes `custody_env_lookup`, `custody_root_resolution`, `private_record_read`, `weight_lstat`, `tokenizer_config_read`, `tokenizer_config_copy`, `loader_import`, and `from_pretrained`. The spies raise immediately if any excluded event occurs. The test separately asserts that `.mor-custody-record-v1.json` was never passed to production `load`.

## Banked production evidence preserved

| Banked row | Production-path regression |
|---|---|
| Invalid routed request projections | `test_materialize_invalid_requests_publish_governed_blocked_result` |
| Constructor mismatch before custody | `test_constructor_digest_is_checked_before_environment_lookup` |
| Absent/empty/symlink custody handle rows | `test_materialize_absent_empty_and_symlink_handles` |
| Custody record and identity matrix | `test_materialize_custody_attestation_negative_matrix`; `test_materialize_identity_negative_matrix` |
| Serialization and forbidden-field rows | `test_materialize_serialization_public_safety_and_runtime_negatives` |
| Constructor/encode-decode/stop matrix | `test_materialize_constructor_negative_matrix`; `test_materialize_synthetic_constructor_and_stop_failures` |
| BF3 atomic recovery | both `test_atomic_interruption_*` rows |
| BF5 one weight observation | `test_weight_identity_uses_one_lstat_observation` |
| NF2 pre-import matrix | ordered `test_runtime_validator_00` through `_09` |
| Positive materialization construction | `test_materialize_synthetic_positive_reaches_pass` |

The status, failure code, terminal check, complete ordered prefix, exit, empty arrays, schema validation, and exact sidecar digest/basename are asserted adversarially through `_assert_failure`; any mutation of those fields fails the regression. Helper-only classifier/schema tests remain supplementary and are not used to close CR-FRBF1.

## Files changed

- `diagnostics/m4_tokenizer_materialization.py`
- `tests/test_m4_tokenizer_materialization.py`

No specification, contract, schema, OCI launch contract, scientific artifact, custody record, STATE, provenance, or ledger file changed.

## Verification

- Implementation result: `7ccb3287718920225829347eb8b3b8db6bb9f71a`.
- Fresh workflow-helper-created exact-SHA checkout: clean.
- Exact Linux/amd64 image digest: `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`.
- Controls: `--pull=never`, `--network none`, read-only repository, no custody mount or environment, no writable output mount, bounded private tmpfs.
- Exact command: `python3 -I tests/run_m4_tokenizer_materialization_tests.py`.
- Result: 33 tests run, 33 passed, exit 0.

## Preserved boundaries and route

- The single materialization operation remains **UNCONSUMED**.
- No routed custody/model/tokenizer access, real materialization, retry, inference, qualification, scoring, protected seeds, science, STATE/provenance mutation, merge, publication, or gate decision occurred.
- **Exact next recipient:** WORKFLOW COORDINATOR, then one authoritative persistent-CRITIC rereview.
