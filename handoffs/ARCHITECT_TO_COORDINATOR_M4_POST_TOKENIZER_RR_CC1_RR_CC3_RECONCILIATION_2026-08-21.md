# ARCHITECT → WORKFLOW COORDINATOR — M4 Post-Tokenizer RR-CC1–RR-CC3 Reconciliation

**Date:** 2026-08-21 EDT  
**Regime:** B  
**Terminal state:** **COMPLETE**

## Intake

- Input: `architect/m4-post-tokenizer-r-cc1-r-cc6-remediation @ 94c9a833fdaf872584ea863391c21927bdb704d2`.
- Authoritative review: `critic/m4-post-tokenizer-r-cc1-r-cc6-rereview @ ba19982f7b165821d4c207ea05d047212feb7950`.
- Review artifact: `reviews/critic_m4_post_tokenizer_r_cc1_r_cc6_rereview.md`.

## Complete reconciliation

RR-CC1 now has self-contained canonical request, prior-token, PASS-receipt, registered-FAIL, and resulting negative receipt objects. Every receipt-derived row binds the exact base, result digest, call delta, first failure, and unchanged durable-state identities. Registered FAIL changes both status and code; missing-code derives from that exact valid registered-FAIL base.

RR-CC2 now has one explicit active-artifact precedence map. It replaces the older universal zero-call answer for receipt/exception/correlation rows and the older zero-call `reset_b` trace. Pre-call faults remain zero calls; observed receipt, backend exception, and response correlation are one call. Each candidate/peer reset is exactly one call and one validated receipt.

RR-CC3 now binds exactly 42 canonical state × operation cells. Every cell has exact pre/request/post references and digests, result, and call delta. Invalid cells are mechanically byte-identical. Canonical INITIALIZED state and state-specific close requests, receipts, and CLOSED results are present.

Banked R-CC4–R-CC6 artifacts and all other unaffected input bytes are unchanged.

## Complete changed-byte inventory

| Path | Mode | Bytes | SHA-256 |
|---|---:|---:|---|
| `specs/data/m4_post_tokenizer_rr_cc1_receipt_realizations_v1.json` | `100644` | 10398 | `74fe613c2c72830928d488132b0a784c0916024514bef08990ffab7bcfdd43bc` |
| `specs/data/m4_post_tokenizer_rr_cc1_receipt_realizations_v1.json.sha256` | `100644` | 120 | `820663b104fe21600acb0d43cc27591c759a58d1cb1d4000a13171154722a348` |
| `specs/data/m4_post_tokenizer_rr_cc2_precedence_map_v1.json` | `100644` | 1906 | `f1747f4cafbec3a17412fa28aadae8315300cf35ffd8a9fb13d801752cfcccb5` |
| `specs/data/m4_post_tokenizer_rr_cc2_precedence_map_v1.json.sha256` | `100644` | 114 | `36c55ba376746246b3e607cc062da19fd5c1bdd852aeeff3ffeeef4508415cca` |
| `specs/data/m4_post_tokenizer_rr_cc3_lifecycle_realizations_v1.json` | `100644` | 28351 | `49ae30c1d52aab7d7fcb8e35fdec846f42723a018c380b12187c6cb2d8d8814c` |
| `specs/data/m4_post_tokenizer_rr_cc3_lifecycle_realizations_v1.json.sha256` | `100644` | 122 | `321549b06fb331e940b6cd20e060480396c64fdd4610c419a81fd96794608787` |
| `specs/m4_post_tokenizer_rr_cc1_rr_cc3_reconciliation_v1.md` | `100644` | 3558 | `5ce35914855df076f3659e94c09cf27d4d35d833a1bb24e52ed1526e1d240709` |

## Verification and boundaries

All JSON is canonical UTF-8 with one LF, all sidecars reproduce raw bytes, every embedded object digest reproduces, the lifecycle matrix has exactly 42 unique cells, every invalid cell has equal pre/post digest and zero backend calls, and `git diff --check` passes. Workflow preflight and canonical-manifest validation are required before delivery.

No implementation, OCI/materializer/custody/model/tokenizer access, scoring, seeds, science, Q2/EF3/native-L8 work, durable-state mutation, publication, merge, or gate decision occurred.
