# CRITIC Final Rereview — M4 Tokenizer CR-RBF1

**Date:** 2026-08-21
**Regime:** B
**Gate served:** Independent CR-RBF1-only production-path rereview with preservation regression.

## Canonical intake

- Canonical implementation: `taskbuilder/m4-tokenizer-cr-rbf1-residual-remediation` at `e7810f546b7985145c177e760cd2ca2b29b0b249`.
- Implementation result: `86374c430550349be201c56920e394343761e8a4`.
- Handoff result: `c8d67451ba344acfa56aa44c9a490b56ea8e77c0`.
- Prior authoritative BLOCK: `critic/m4-tokenizer-critic-block-rereview` at `6d86c529d7f53d827a1b8a69c910292855fee0b3`.

The committed common handoff manifest validated with `tools/workflow_contract_validator.py`. An independent raw `git cat-file blob` inventory reproduced all 22 declared artifact SHA-256 values. The repository checkout helper created a fresh clean checkout of the exact canonical head. The implementation delta changes only `diagnostics/m4_tokenizer_materialization.py` and `tests/test_m4_tokenizer_materialization.py`; the routing tail adds only the formal handoff and manifest.

## Law fidelity and banked preservation

The specification's P1, P2, and P3 quotation remains verbatim against `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1. No constitution, specification, contract, schema, scientific identity, source-class tag, STATE, provenance, or ledger artifact changed. The invalid-request and constructor projections remain banked. BF3 atomic-pair recovery and BF5's single-`lstat` weight observation are unchanged. The ten ordered NF2 pre-import negatives, exact normative identities, wrapper order, commands, pinned image controls, positive construction, and public field restrictions remain preserved.

**LAW_FIDELITY: CLEAR.**

## Resolved CR-RBF1 rows

- Separate absent, empty, and symlink-root custody-handle realizations call `materialize`, require `BLOCKED`/exit `2`, `CUSTODY_HANDLE_UNRESOLVED`, terminal `CUSTODY_HANDLE`, the full ordered prefix, a valid artifact pair, and no private artifact read. The Windows CRITIC host lacks symlink-creation privilege, so the symlink test could not run locally; static inspection confirms the asserted boundary, and the reported pinned Linux run covers it.
- Noncanonical array serialization is fault-injected at the production array-digest call and reaches `SERIALIZATION_MISMATCH`, terminal `PUBLIC_SAFETY`, FAIL/exit `3` through `materialize`.
- Forbidden public result content is injected into the production result and reaches `LOCAL_ONLY_CUSTODY_VIOLATION`, terminal `PUBLIC_SAFETY`, FAIL/exit `3` through `materialize`.

## Batched blocking finding

### CR-FRBF1 — Alternate loading/runtime rejection occurs after custody and tokenizer access

The binding specification requires host Python, another platform/runtime, installation or monkey patch, remote-code loading, or an alternate tokenizer class/loading identity to fail as `RUNTIME_IDENTITY_MISMATCH` before custody lookup. The remediation instead wraps `from transformers import AutoTokenizer` and `AutoTokenizer.from_pretrained(...)` inside the temporary-copy block. Production control flow reaches this catch only after resolving the custody environment, reading and validating the private custody record, observing the weight, reading both tokenizer artifacts, and copying those artifacts.

The new test confirms the same ordering: `_synthetic_materialize(loader_error=...)` constructs a synthetic custody root, record, weight, tokenizer/config files, patches their reads, and raises only from `from_pretrained`. It then expects terminal `TOKENIZER_COPY`. It does not assert that custody lookup and tokenizer access were absent. Therefore the test proves a post-access loader exception mapping, not the required alternate loading/runtime no-access boundary. A generic loader exception cannot substitute for deterministic pre-custody runtime/loading identity verification.

This is one residual no-access/executability finding and must be remediated as one integrated batch. No serial finding loop is requested.

## Executability evidence

The exact OCI test command remains pinned to the declared Linux/amd64 digest with `--pull=never`, `--network none`, a read-only repository, no custody mount or environment, isolated `python3`, and the unchanged wrapper. Docker is unavailable on the CRITIC host, so the reported pinned-container 32/32 run could not be independently repeated. With an isolated stub validator, the combined serialization/public-safety/runtime test passed locally; the custody-handle test reached only the host's symlink privilege error before its subcases executed. These host results are limited corroboration and do not replace pinned-container evidence.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**
**COMBINED DISPOSITION: BLOCK.**

Three residual matrix areas are closed, but the alternate loading/runtime row violates the required pre-custody no-access boundary. Banked evidence remains preserved.

**Exact next authorized route:** WORKFLOW COORDINATOR returns this single batched BLOCK for integrated remediation. No direct role-to-role ownership transfer is made by this review.

**Explicitly prohibited actions:** routed custody lookup; model/tokenizer access; OCI materialization; retry or fallback; inference/serving; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; merge; publication; rerun; or gate decision. The single materialization operation remains **UNCONSUMED**.

## Public-repository safety

Public-safety preflight: same-checkout `workflow_preflight.py --repo-root` with gitleaks `8.30.1`, complete resulting-file scanning, added-line patch scanning, and manual review returned zero findings. No routed custody/model/tokenizer data, private path, credential, task identifier, protected seed, scientific output, or prohibited durable-state mutation was introduced or accessed.
