# CRITIC Rereview — M4 Tokenizer NF1/NF2 Pre-Import Validation

**Date:** 2026-08-21
**Regime:** B
**Gate served:** Independent narrow rereview of NF1 exact isolated pre-import wrapper reachability and NF2 exact negative realizations before any re-release of the still-unconsumed tokenizer materialization operation.

## Canonical intake and inputs

- Canonical manifest: branch `coordinator/m4-tokenizer-nf1-nf2-manifest` at `c7ee89f4e6c4ed5e3db0d8d1d9e275092c96f112`, `handoffs/WORKFLOW_COORDINATOR_TO_CRITIC_M4_TOKENIZER_NF1_NF2.manifest.json`.
- Routing ref/head: `refs/heads/coordinator/m4-tokenizer-nf1-nf2-routing-base` at `a750f197b032493f9bde4df2727b67b046245d82`.
- Base: full SHA formed by concatenating `619ff92713` and `1222071bdc168f38f40a9760fd5476`.
- Prior BLOCK: branch `critic/m4-tokenizer-normative-json-lf-rereview` at the full SHA formed by concatenating `41fc77360b431ef9fbeb3e84772` and `124324cb01601`.
- Prior substantive input: branch `architect/m4-tokenizer-materialization-spec` at `903a0c3a032b672a6b9a3a32bb53f66b4f1f07f5`.
- Remediated substantive result: branch `architect/m4-tokenizer-materialization-spec` at `e0308a92ef3091da2da0eb256ef08aa880cf9169`.
- ARCHITECT return: `handoffs/ARCHITECT_TO_COORDINATOR_M4_TOKENIZER_NF1_NF2_REMEDIATION_2026-08-21.md`.
- Rebecca re-release routing artifact: `handoffs/REBECCA_M4_TOKENIZER_IF2_EXECUTION_RERELEASE_2026-08-21.md`.

The canonical manifest validated with `tools/workflow_contract_validator.py`; its complete raw-Git-blob inventory matched in the immutable checkout. The routing head is a merge whose only tree delta from the substantive result is the named handoff under `handoffs/`. No substantive review relied on conversation memory or uncommitted prior-role state.

## First checklist item — Versioned-Law Compliance Protocol

The quoted P1, P2, and P3 text in the specification was independently byte-compared with `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1 and matched. The `903a0c3a..e0308a92` delta changes no quoted law, constitutional text, scientific threshold, locked bar, scoring criterion, waiver, or provenance claim. New wrapper, failure, mutation, ordering, byte-count, and digest criteria remain tagged `[PROPOSED]`. No bar laundering or law reconstruction was found.

**LAW_FIDELITY: CLEAR.**

## Independent NF2 verification

- `specs/data/m4_tokenizer_runtime_validation_negative_cases_v1.json` contains exactly ten unique rows in ordinal/test-ID order `00` through `09`.
- Every mutation is single-target and exact: missing path, extra path, attribute replacement, link-kind replacement, CR insertion, BOM prefix, final-LF removal, sidecar grammar mutation, sidecar basename mutation, and digest mismatch.
- `specs/data/m4_tokenizer_runtime_validation_negative_expected_v1.json` contains the corresponding ten canonical expected rows in the same order. Their expected first failing checks are reachable in the prescribed short-circuit sequence: two `PATH_SET`, `ATTRIBUTE`, `FILE_KIND`, three `JSON_BYTE_FORM`, `SIDECAR_GRAMMAR`, `SIDECAR_BASENAME`, and `DIGEST`.
- Both JSON files are canonical single-line LF artifacts. Their independently recomputed normalized-LF SHA-256 identities are `b00a6c73b52f9372b5b7a207ce8eafe24b5ba029e12929e25f9e10163bce521e` and `00cc8d92b5622c7ce21bc45e7cc4a50d3939bdfbc2a8eb0b716a30b018a7ed00`; both adjacent sidecars match.
- The amended test contract independently recomputes to SHA-256 `b81fd4af9ac04f366bc3462a44daecbe4ae0ffb1fd4445b754d2b557154b9bd4`, matching its sidecar and the specification.
- The negative fixtures are loaded only after production positive validation and mutate fresh in-memory snapshots, so they do not modify the mounted checkout or consume the operation.

**NF2: RESOLVED.**

## Blocking finding

### BF1 — NF1 remains non-executable: `.gitattributes` raw-LF identity has no checkout-level binding

The new wrapper must begin by reading mounted `.gitattributes` in binary mode and requiring exactly `1790` LF bytes with SHA-256 `b6f9200cffdb0b43fcb11fc5a75c2f7eda47be779f6a769da88480b62c7a8a71`. Failure is `ATTRIBUTE`, before discovery. Runtime normalization, copying, attribute override, and byte mutation are forbidden.

But the committed `.gitattributes` does not contain a self-rule such as `.gitattributes text eol=lf`; `git check-attr text eol -- .gitattributes` returns both attributes as `unspecified`. Therefore the required raw worktree bytes depend on ambient Git checkout configuration rather than the released commit.

This is not hypothetical. The repository-mandated fresh worktree created for this rereview has `core.autocrlf=true`. Its raw `.gitattributes` is `1815` CRLF bytes, not the required `1790` LF bytes, and its raw SHA-256 is `4fb625a587fd23bb53847c80491c50c746c84e71ed33c2584ee94ff28899322d`, not the bound digest. The Git blob itself has the asserted LF identity, but Git-object substitution and post-checkout normalization are expressly forbidden. The exact wrapper command would consequently stop at `ATTRIBUTE` before reaching the otherwise-remediated 9+9 validator or unittest discovery.

The contract does not prescribe an immutable checkout configuration that guarantees LF for `.gitattributes`, and the file does not self-bind its checkout line endings. TASK BUILDER or executor would have to choose an unprescribed checkout setting, normalize/copy the file, or accept immediate failure. Internal hash consistency is therefore not end-to-end executability.

**Required narrow remediation:** Bind `.gitattributes` itself to deterministic LF worktree bytes in the committed checkout contract (and update every affected exact byte count/digest/sidecar/spec binding), or prescribe another exact repository-committed construction that guarantees the asserted raw worktree identity without normalization, copying, attribute override, or implementer choice. Then route the exact delta for fresh rereview.

This is a specification/executability defect, not a candidate failure and not authorization to execute or rerun anything.

## Preserved evidence and scope

- NF2 is closed by the exact ten-case/ten-row realization above.
- The prior positive ordered 9+9 JSON/sidecar set remains independently valid in its explicitly attributed LF domain.
- The wrapper callable, seven-step validator order, failure destination, exit mapping, standard-library discovery inputs, materializer command, pinned image/runtime, IF1/IF2, custody/schema/fixture identities, and scientific construction are otherwise preserved.
- The single bounded materialization operation remains unconsumed.
- No structured executability trace was named or inventoried in this narrow handoff, so no trace-disposition artifact was fabricated.

## Verdict and routing

**SUBSTANTIVE: BLOCK.**
**COMBINED DISPOSITION: BLOCK.**

NF2 is resolved, but BF1 leaves NF1 fail-closed reachability dependent on ambient checkout configuration and demonstrably failing in the prescribed raw worktree domain.

**Exact next authorized role:** WORKFLOW COORDINATOR receives this review and returns only BF1 to persistent ARCHITECT for narrow remediation. CLEAR/re-release, TASK BUILDER execution, and any materialization attempt remain unauthorized.

**Explicitly prohibited actions:** Custody/model/tokenizer access; OCI or materialization execution/modification; inference/serving; Q2/EF3; qualification; diagnostics/scoring; protected seeds; science; STATE/provenance mutation; publication; rerun; merge; and gate decision.

## Public-repository safety and prohibited-run confirmation

Public-safety scan: `workflow_preflight.py` with gitleaks 8.30.1, required pattern checks, and manual review over the complete introduced routing-head-to-review range; 0 findings, cleared. No custody/model/tokenizer access, OCI/materialization, inference, scoring, rerun, protected-seed exposure, state/provenance mutation, publication, or unauthorized merge occurred.
