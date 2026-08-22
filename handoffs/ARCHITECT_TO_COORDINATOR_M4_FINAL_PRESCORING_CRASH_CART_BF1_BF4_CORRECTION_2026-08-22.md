# ARCHITECT → WORKFLOW COORDINATOR — M4 FINAL PRE-SCORING CRASH-CART BF1–BF4 CORRECTION

Date: 2026-08-22 EDT

Regime: B

Terminal state: **COMPLETE — DESIGN ONLY — NO RUN AUTHORITY**

## Immutable result

- Substantive result: `fcfe47752db70f67de1a7a63a06182e6417d6e6d`.
- Base CRITIC BLOCK: `9a028cb0799807910900f29ef8a1ff8cb4af0b4d`.
- Exact Rebecca authority: `handoffs/REBECCA_M4_FINAL_PRESCORING_FULL_STACK_CRASH_CART_AND_EXPLORATORY_OBSERVATION_AUTHORITY_2026-08-22.md`, source commit `8b4a383c450e8b29f2633f7e25107abcb62dd929`, 6,087 bytes, raw SHA-256 `c759a99a563777a42ba42eb25f4679a40bb940a246bc002ef199c61e58721ecc`.

## Delta closure

- **BF1:** the four warmup prompts are bound to literal-LF UTF-8 bytes with exactly five `0x0a` bytes, no literal `0x5c 0x6e` separator, and exact sizes/digests `89/eabe6b7c…`, `122/6b569733…`, `603/763187d5…`, and `1116/5646b4c9…`. The four superseded literal-backslash-n digests are absent from active artifacts.
- **BF2:** both reset episodes are zero-based: warmup receipts use ordinals 0–3 and measured receipts use ordinals 0–63, with no priming request.
- **BF3:** the report schema is a fail-closed five-stage union for pre-active, partial-warmup, partial-active, post-active, and complete terminal evidence. Unreached fields are null or empty; unobserved role observations are null; only the complete branch requires four warmup pairs, 64 active pairs, at least 121 resource samples, complete trends, cleanup PASS, public-safety CLEAR, and export. A future semantic validator remains mandatory for exact cross-field counts, order, receipt chains, and derived values.
- **BF4:** all four substantive artifacts use permitted `[PROPOSED]` provenance. The exact Rebecca authority is bound without expansion and grants design/implementation preparation only; all Architect-selected mechanics remain proposed pending review and an exact later release.

## Focused validation

- Parsed all three JSON artifacts and validated the report schema against Draft 2020-12 metaschema.
- Validated representative reports for all five evidence stages; rejected a pre-active report containing fabricated active rows and a complete report missing one role observation.
- Reproduced every corrected prompt size/digest and all three adjacent SHA-256 sidecars.
- Verified exact authority remote equality and byte identity, LF attributes, diff whitespace, and absence of stale active prompt identities.
- No model, tokenizer, OCI, WSL2, gofast, custody, protected input, scoring, science, implementation, merge, STATE/provenance mutation, or run occurred.

## Holds and next event

`run_authorized=false`, `merge_authorized=false`, and `scoring_authorized=false` remain binding. Every future implementation, combined-tree, runtime, dependency, gofast, review, JUDGE, and Rebecca single-run identity remains fail-closed `UNBOUND` where applicable.

WORKFLOW COORDINATOR should validate the canonical manifest and helper-compatible routing tail, then route this exact delta once to the authoritative persistent CRITIC for BF1–BF4 rereview.
