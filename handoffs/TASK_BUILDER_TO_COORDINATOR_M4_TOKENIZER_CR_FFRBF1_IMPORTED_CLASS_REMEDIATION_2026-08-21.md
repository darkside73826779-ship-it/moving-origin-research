# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER CR-FFRBF1 IMPORTED CLASS IDENTITY REMEDIATION

**Date:** 2026-08-21

**Regime:** B

**Status:** COMPLETE

**Gate served:** One integrated CR-FFRBF1 imported module/class/loading-identity remediation before persistent-CRITIC rereview

## Canonical intake

- Input: `taskbuilder/m4-tokenizer-cr-frbf1-runtime-identity-remediation` at `543340f7d9f31271d80280c67813bfd84c90398c`.
- Authoritative CRITIC BLOCK: `critic/m4-tokenizer-cr-frbf1-final-rereview` at `35bcb4209cd9b4159877856dd0b3f565fbad7573`.
- Review artifact: `reviews/critic_m4_tokenizer_cr_frbf1_final_rereview.md`.
- Work branch: `taskbuilder/m4-tokenizer-cr-ffrbf1-imported-class-remediation`.

## Integrated correction

After the banked distribution/version/path/kind/size/digest checks succeed, `verify_runtime_loading_identity()` imports the root `transformers` module and exact loader module before custody. It requires the root module file and import-spec origin to equal the `transformers/__init__.py` adjacent to the verified loader file; requires root and loader modules to expose the identical `AutoTokenizer` class; requires exact class module/name metadata; and requires both the class and `from_pretrained` source origins to equal the verified loader path. It returns that authenticated class for the later authorized loading call. `from_pretrained` is not executed during identity verification.

Every mismatch maps through `materialize` to `RUNTIME_IDENTITY_MISMATCH`, terminal `AUTHORITY`, status `FAIL`, exit `3`, empty arrays, exact ordered prefix, and a schema-valid atomic result pair. Later `from_pretrained` execution remains distinct as `INTERNAL_ERROR`, terminal `PUBLIC_SAFETY`, exit `4`.

## CR-FFRBF1 requirement → production branch → test → evidence trace

| Requirement / finding | Production branch | Production-entrypoint realization | Exact evidence |
|---|---|---|---|
| Reject monkey-patched root module | root `__file__` and import-spec origin equality | `test_materialize_imported_loader_identity_fails_before_custody` / `monkey_patched_module` | FAIL/3, `RUNTIME_IDENTITY_MISMATCH`, terminal/prefix `AUTHORITY`, valid JSON/sidecar pair, no forbidden access |
| Reject alternate `AutoTokenizer` object | root/loader class object identity | same / `alternate_class` | same governed and no-access evidence |
| Reject spoofed class metadata | exact `__module__` and `__qualname__` | same / `alternate_class_metadata` | same governed and no-access evidence |
| Reject alternate class origin | `inspect.getsourcefile(AutoTokenizer)` equals verified loader | same / `alternate_class_origin` | same governed and no-access evidence |
| Reject alternate loading method | `inspect.getsourcefile(AutoTokenizer.from_pretrained)` equals verified loader | same / `alternate_loading_method` | same governed and no-access evidence |
| Authenticate successful imported identity before custody | full successful file/module/class/method branch precedes `os.environ.get(ENV)` | `test_materialize_successful_import_origin_precedes_custody` | exact trace ends with `custody_env_lookup` only after verified loader read and both module imports; then governed missing-handle BLOCKED row |
| Never execute loader before authorization | returned class is stored; `from_pretrained` remains in later temporary-copy block | all five adversarial subcases plus successful trace | `from_pretrained` spy raises if called and is absent from every pre-custody trace |
| Preserve later loader-exception semantics | later call has no runtime-identity catch | `test_materialize_serialization_public_safety_and_runtime_negatives` | distinct `INTERNAL_ERROR`, `PUBLIC_SAFETY`, exit `4` |

## Ordered access-event traces

Every imported-identity adversarial trace begins with `[runtime_distribution, runtime_loader_lstat, runtime_loader_read, module_import:transformers, module_import:loader]` and then:

- `monkey_patched_module`: stops immediately.
- `alternate_class`: stops immediately.
- `alternate_class_metadata`: stops immediately.
- `alternate_class_origin`: appends `[class_origin, method_origin]`, then stops.
- `alternate_loading_method`: appends `[class_origin, method_origin]`, then stops.

The successful pinned identity trace is exactly `[runtime_distribution, runtime_loader_lstat, runtime_loader_read, module_import:transformers, module_import:loader, custody_env_lookup]`. Thus imported origin authentication demonstrably precedes custody lookup.

All adversarial tests install raising spies for custody environment lookup, custody-root resolution, private-record read, weight observation, tokenizer/config read, tokenizer/config copy, and `from_pretrained`. None fires. The production `load` spy separately proves `.mor-custody-record-v1.json` is never requested. `_assert_failure` adversarially verifies status, failure code, terminal check, complete ordered prefix, exit, empty arrays, schema, and exact sidecar digest/basename.

## Banked coverage preserved

- Seven disk/distribution identity subcases: `test_materialize_alternate_loader_identity_fails_before_custody`.
- Invalid request, constructor, three handle rows, custody/identity, serialization/forbidden-field, constructor/ordinal/stop, BF3, BF5, NF2, and positive construction: all prior named production regressions remain present and passing.
- Helper-only classifier/schema tests remain supplementary and close no production requirement.

## Files and verification

- Changed: `diagnostics/m4_tokenizer_materialization.py`; `tests/test_m4_tokenizer_materialization.py`.
- No specification, contract, schema, OCI launch contract, scientific artifact, custody record, STATE, provenance, or ledger file changed.
- Implementation result: `be543f91c29b9171091d3c5300102a3f634569dd`.
- Fresh workflow-helper exact-SHA checkout: clean.
- Exact pinned Linux/amd64, network-disabled, read-only, no-custody command: `python3 -I tests/run_m4_tokenizer_materialization_tests.py`.
- Result: 35 tests run, 35 passed, exit 0.

## Preserved boundaries and route

- The single materialization operation remains **UNCONSUMED**.
- No routed custody/model/tokenizer access, real materialization, retry, inference, qualification, scoring, protected seeds, science, STATE/provenance mutation, merge, publication, or gate decision occurred.
- **Exact next recipient:** WORKFLOW COORDINATOR, then one authoritative persistent-CRITIC rereview.
