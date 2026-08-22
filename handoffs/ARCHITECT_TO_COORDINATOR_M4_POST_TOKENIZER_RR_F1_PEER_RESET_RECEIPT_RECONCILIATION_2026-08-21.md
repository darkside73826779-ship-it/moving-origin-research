# ARCHITECT → WORKFLOW COORDINATOR — M4 Post-Tokenizer RR-F1 Peer Reset Receipt Reconciliation

**Date:** 2026-08-21 EDT  
**Regime:** B  
**Terminal state:** **COMPLETE**

## Intake and result

- Input: `architect/m4-post-tokenizer-rr-cc1-rr-cc3-reconciliation @ 73c8394994aa172727ffff93dc42ade4348d4823`.
- Authoritative review: `critic/m4-post-tokenizer-rr-cc1-rr-cc3-final-rereview @ 31e4e2c57c70b4b869f4102e901af613a4fe19b9`.
- Scope: RR-F1 only.

The lifecycle realization now binds four distinct canonical reset receipts: candidate reset A and B use `candidate-session-v1`; peer reset A and B use `peer-session-v1`. Each reset row references its own role/reset receipt and exact digest while preserving `backend_call_delta=1`. The precedence map and governing reconciliation prose bind the same role-specific rule.

All four receipt references resolve mechanically, all embedded object digests reproduce, and candidate/peer session identity is distinct for both resets. No RR-CC1 receipt-negative realization, lifecycle cell, close trace, fanout, law, overlay, caller, pair, or other banked evidence changed.

## Complete changed-byte inventory

| Path | Mode | Bytes | SHA-256 |
|---|---:|---:|---|
| `specs/data/m4_post_tokenizer_rr_cc2_precedence_map_v1.json` | `100644` | 1971 | `7596186d4458ca916bb9783b4761449e9a55b7858f00ea29d0a534e4c2a37904` |
| `specs/data/m4_post_tokenizer_rr_cc2_precedence_map_v1.json.sha256` | `100644` | 114 | `63b0d6e8861a03039a218e1a1e2289c63e8590f5984a12084023efed7238d174` |
| `specs/data/m4_post_tokenizer_rr_cc3_lifecycle_realizations_v1.json` | `100644` | 30474 | `1b5c3e33de5b8e452561ff14d308acddbccad14addb204b7467516d76666508b` |
| `specs/data/m4_post_tokenizer_rr_cc3_lifecycle_realizations_v1.json.sha256` | `100644` | 122 | `f8cb8136cb37ba4118a1450b6becd02078b4070af8be621d4d995b78aeb16eee` |
| `specs/m4_post_tokenizer_rr_cc1_rr_cc3_reconciliation_v1.md` | `100644` | 3734 | `7e4499463cf08001cafed47cb931fe1eb54af0802b9f6f97853cbe156c11e335` |

## Boundaries

No implementation, OCI/materializer/custody/model/tokenizer access, scoring, seeds, science, Q2/EF3/native-L8 work, durable-state mutation, publication, merge, or gate decision occurred.
