# ARCHITECT → Fresh-Context CRITIC — L8 GPU Adoption v1.3

**Date:** 2026-08-21

**Regime:** B

- **Gate served:** remediation of CRITIC findings B10–B12 and NB-A–NB-F while preserving verified B1–B9 closures.
- **Input SHAs reviewed:** v1.2 `678af9b9c80b1f22cf65b2bacc4901ad06450856`; CRITIC re-review `3bd6b05f9a6d843eb57e9d534f5413d1aa5cfcf4`; controlling CPU package `2082680a7caba85c46e637b3b38d679fa7f80599`; CPU baseline `b1397498ca369067e956479e6c2bd6b0793c3e89`; required base `b6d4556021ad38199d3bfa90fdb3ef9a99988790`.
- **Files changed:** authoritative four-file CPU-spec package restored from `2082680`; adoption specification v1.3; changelog; known-good JSON and sidecar; this handoff.
- **Branch/specification SHA:** `architect/l8-gpu-adoption-spec`; v1.3 specification commit `3fea7457cb3ef3cc92a1b1ac936e9625b6c6422d`.
- **Status:** REMEDIATED SPECIFICATION PROPOSED; TASK BUILDER remains held.

## Closure map

- **B10:** all four controlling CPU-spec files now match `2082680` byte-for-byte; §2 and configuration continue to cite that exact SHA.
- **B11:** finite deterministic rho values use separately named `RHO_TEST_VALUE_EPS=1e-12`; predicate parity remains exact and continues to use `RHO_COMPARE_EPS` only for the locked threshold.
- **B12:** seed key is the exact baseline string with `.6f` formatting, fixed field names/order/separators, UTF-8 encoding, first eight digest bytes little-endian, and modulo `2^31`.
- **NB-A:** backend objects are called parity roles and tagged `[PROPOSED]`, not represented as L18 controls.
- **NB-B:** count corrected to six rho categories plus no-softening; complete-verdict aggregation remains the seventh category.
- **NB-C:** tapes are arm-scoped; null consumes no dose-noise draws; exact expected collision count is `3840`.
- **NB-D:** result-cell coordinate names and order are enumerated.
- **NB-E:** operative ruling citations and empirical negative values are no longer tagged `[PROPOSED]`.
- **NB-F:** the eventual full-screen GPU remains explicitly bound to the controlling §7.1 schema, paths, NaN handling, and atomic publication.

## Required review

1. Verify `LAW_FIDELITY: PASS|BLOCK`, including byte identity of all four CPU-spec files against `2082680`.
2. Only after Part A passes, verify `SUBSTANTIVE: CLEAR|BLOCK`, focusing on B11 test-value tolerance separation, B12 seed-key bytes, arm-specific RNG draw order, and exact collision count.
3. Overall clearance requires both PASS and CLEAR.

- **Preserved:** B1–B9 closures, law quotations, locked bars, frozen calibration, native-calibration negative, misspecification-selection negatives, candidate-blindness, O-14/O-15, and all authorization boundaries.
- **Exact next recipient:** fresh-context CRITIC, then Rebecca. TASK BUILDER remains held.
- **Explicitly prohibited:** implementation, execution, scoring, protected-seed access/exposure, full-screen release, G2–G4 freeze, post-run tolerance choice, native GPU calibration/RNG adoption, automatic retry/fallback, CPU replacement, merge to main, or L15/L16/L17 before M5.
- **Public-safety scan:** gitleaks scanned the complete v1.3 commit and this handoff; credential/PII/private-path regex plus manual review found zero issues. No blocker, Rebecca-decision item, protected-seed exposure, or acceptable exception was found.
