# M4 Callable-Step Digest Amendment — Changelog

**Date:** 2026-08-21

**Regime:** B

## v1

- Replaced the legacy varying-response episode with the callable reset episode.
- Replaced legacy response state hashes with a complete pre-state digest and a non-cyclic post-state-projection digest.
- Bound `last_response_sha256` to the actual complete varying response.
- Recomputed exact stepped, snapshot, close, and operation-result artifacts and digests.
- Preserved the verified describe/initialize/reset prefix and all unrelated fixtures.
- Marked the operative change held for persistent-CRITIC review and Rebecca re-release.
