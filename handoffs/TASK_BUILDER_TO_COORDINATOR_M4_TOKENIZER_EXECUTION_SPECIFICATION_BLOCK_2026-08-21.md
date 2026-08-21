# FORMAL RETURN — TASK BUILDER → WORKFLOW COORDINATOR — M4 TOKENIZER EXECUTION SPECIFICATION BLOCK

**Date:** 2026-08-21

**Regime:** B

**Status:** SPECIFICATION BLOCK

**Gate served:** Single bounded tokenizer materialization execution after BF1 CLEAR

## Canonical intake

- Incoming handoff branch/head: `coordinator/m4-tokenizer-bf1-execution-rerelease` at `cdfc881c31d919b397fc91a2a287fd4abbcb3e57`.
- Routing authority: `85195645d5ced85c2bd0e1863d74d800122bda8b`.
- Persistent-CRITIC CLEAR: `7cecba9c93c24a826c193e0c3d609e37b1338337`.
- Amended contract result/base: `adf626b96678db58007861523fa3b9a7c763a1f3`.
- Work branch: `taskbuilder/m4-tokenizer-bf1-execution`.
- Incoming manifest schema and all inventoried raw committed Git-blob SHA-256 values verified.

## Seven blocking omission or ambiguity classes

1. **Materializer absent.** The specification prescribes `diagnostics/m4_tokenizer_materialization.py` and callable `materialize(...)`, but the file is absent from the released checkout.
2. **Pre-import test wrapper absent.** The exact verification command requires `tests/run_m4_tokenizer_materialization_tests.py`, but the file is absent from the released checkout.
3. **Selected test module absent.** The contract requires discovery of exactly `tests/test_m4_tokenizer_materialization.py`, but the file is absent from the released checkout.
4. **Executable inventory absent.** The canonical incoming manifest inventories none of those three required executable artifacts and supplies no committed raw Git-blob SHA-256 identity for them.
5. **Preserved materialization-authority commit lacks the executable.** Commit `9007260570235c1b06b104d78106ba32e8a4e9dd` does not contain `diagnostics/m4_tokenizer_materialization.py`.
6. **Prior IF2 authority lacks the executable.** Commit `902df984a2e689d41954d749fcf06570b42d9c4b` is an ancestor of the routing checkout but does not contain `diagnostics/m4_tokenizer_materialization.py`.
7. **OCI launch contract incomplete.** The named artifacts bind the in-container `python3 -I` commands and image digests but do not prescribe the exact OCI engine invocation, mount target, environment forwarding, network settings, or engine selection. Choosing them would require implementer invention.

The exact prescribed verification and materializer commands therefore cannot run from the released immutable checkout. TASK BUILDER did not fabricate the missing implementation, copy or import unmanifested executable bytes, or invent OCI launch behavior.

## Preserved boundaries

- The single authorized tokenizer-materialization operation remains unconsumed.
- No custody environment lookup occurred.
- No custody, model, tokenizer, checkpoint, cache, or adapter bytes were accessed.
- No OCI test or materializer process started; no retry, fallback, alternate runtime, inference, serving, Q2/EF3, qualification, diagnostics, scoring, protected-seed access, science, or gate action occurred.
- No implementation, test, scientific artifact, STATE, provenance, ledger, custody record, or local preserved artifact was modified.
- No result artifact was created, and no model/tokenizer bytes or private custody values are published.
- No merge was performed or requested.

## Required remediation and route

WORKFLOW COORDINATOR should route this durable BLOCK to ARCHITECT. Remediation must provide a newly reviewed and re-released canonical package whose immutable checkout contains and inventories the exact committed materializer, wrapper, and selected test artifacts and whose named contract fixes the complete OCI launch command. The single-operation status must remain unconsumed until a later exact re-release.

**Exact next recipient:** WORKFLOW COORDINATOR, then ARCHITECT.

**Explicitly prohibited:** implementation by this return, custody lookup, OCI execution, retry, model/tokenizer access, inference/serving, qualification, scoring, seeds, science, durable-state mutation, merge, or gate decision.
