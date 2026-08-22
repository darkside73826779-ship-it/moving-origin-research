# CRITIC Final Rereview — M4 Tokenizer CR-FRBF1

**Date:** 2026-08-21
**Regime:** B
**Gate served:** Independent CR-FRBF1 pre-custody runtime/loading identity closure rereview with banked regression.

## Canonical intake

- Canonical implementation: `taskbuilder/m4-tokenizer-cr-frbf1-runtime-identity-remediation` at `543340f7d9f31271d80280c67813bfd84c90398c`.
- Implementation result: `7ccb3287718920225829347eb8b3b8db6bb9f71a`.
- Handoff result: `c4502b6d465c4ded9194e8b78e5a79716cdcf4a0`.
- Prior authoritative BLOCK: `critic/m4-tokenizer-cr-rbf1-final-rereview` at `1f6107f416a2ad4ce13ed0fcc8e7f0ae8ca2e2be`.

The committed common handoff manifest validated with `tools/workflow_contract_validator.py`. An independent raw `git cat-file blob` inventory reproduced all 22 declared artifact SHA-256 values. The repository checkout helper created a fresh clean checkout of the exact canonical head. The implementation delta changes only `diagnostics/m4_tokenizer_materialization.py` and `tests/test_m4_tokenizer_materialization.py`; the routing tail adds only the formal handoff and manifest.

## Law fidelity and banked preservation

The specification's P1, P2, and P3 quotation remains verbatim against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1. No constitution, specification, contract, schema, scientific identity, source-class tag, STATE, provenance, or ledger artifact changed. Invalid-request, constructor, handle, custody, identity, serialization, forbidden-field, constructor/ordinal/stop, BF3, BF5, NF2, and positive tests remain present. The later loader-exception case is now distinctly projected as `INTERNAL_ERROR`, terminal `PUBLIC_SAFETY`, exit `4`, rather than the pre-custody runtime-identity row.

**LAW_FIDELITY: CLEAR.**

## Verified remediation evidence

`verify_runtime_loading_identity()` executes before the custody environment lookup. It checks distribution availability, version, exactly one declared loader path, regular-file kind, exact byte size, and exact digest. The single production-entrypoint test exercises seven separate distribution/version/path/kind/size/digest failures. Each requires `RUNTIME_IDENTITY_MISMATCH`, terminal `AUTHORITY`, FAIL/exit `3`, the exact one-row check prefix, empty arrays, schema-valid JSON/sidecar evidence, and an exact ordered access trace excluding custody environment/root/record, weight, tokenizer/config, copy, loader import, and `from_pretrained` events. Independent host execution of that seven-subcase test passed with an isolated schema-validator stub.

## Batched blocking finding

### CR-FFRBF1 — Successful file identity does not authenticate the imported loader class before custody

The binding specification explicitly classifies installation or monkey patch, remote-code loading, and an alternate tokenizer class/loading identity as `RUNTIME_IDENTITY_MISMATCH` before custody lookup. The remediation verifies only distribution metadata and the on-disk loader file. It deliberately does not import `transformers.AutoTokenizer` until after custody resolution, private-record validation, weight observation, tokenizer/config reads, and copies. Consequently, a correct distribution/file identity combined with an alternate in-memory `transformers` module or `AutoTokenizer` object passes the new pre-custody check.

The suite itself demonstrates this gap. `_synthetic_materialize` inserts a synthetic `transformers` module into `sys.modules`, supplies a fake `AutoTokenizer` class whose `__module__` string merely names the expected module, and then exercises banked production paths after synthetic custody access. No successful-identity test requires a pre-custody loader import, proves the imported class originated from the verified file, or adversarially replaces the class while the distribution/file checks pass. The seven new subcases all fail before import and therefore cannot detect this bypass.

Verifying a file on disk is not equivalent to authenticating the runtime class that production later invokes. The successful identity branch must bind the actual loader class/import to the verified distribution before any custody access, while retaining `from_pretrained` execution after the authorized access boundary and preserving later INTERNAL_ERROR semantics.

This is one residual runtime-identity/no-access finding and must be remediated as one integrated batch. No serial finding loop is requested.

## Executability evidence

The exact OCI test command remains pinned to the declared Linux/amd64 digest with `--pull=never`, `--network none`, a read-only repository, no custody mount or environment, isolated `python3`, and the unchanged wrapper. Docker is unavailable on the CRITIC host, so the reported pinned-container 33/33 run could not be independently repeated. The isolated host execution of the new seven-subcase runtime-identity test passed; this corroborates its failure branches but does not cover the successful-file/alternate-class bypass above.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**
**COMBINED DISPOSITION: BLOCK.**

The seven declared distribution/file failure branches are closed, but the successful identity branch does not enforce the specification's pre-custody monkey-patch/alternate-class boundary. Banked evidence remains preserved.

**Exact next authorized route:** WORKFLOW COORDINATOR returns this single batched BLOCK for integrated remediation. No direct role-to-role ownership transfer is made by this review.

**Explicitly prohibited actions:** routed custody lookup; model/tokenizer access; OCI materialization; retry or fallback; inference/serving; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; merge; publication; rerun; or gate decision. The single materialization operation remains **UNCONSUMED**.

## Public-repository safety

Public-safety preflight: same-checkout `workflow_preflight.py --repo-root` with gitleaks `8.30.1`, complete resulting-file scanning, added-line patch scanning, and manual review returned two duplicate-domain `personal_contact` findings. Both matches occur wholly inside the required immutable public implementation commit on line 10; manual inspection classifies them as public reproducibility metadata, not personal-contact data. Gitleaks returned zero findings, and manual review found no routed custody/model/tokenizer data, private path, credential, task identifier, protected seed, scientific output, or prohibited durable-state mutation. The scanner findings are explicitly retained and classified, not silently suppressed.
