# Governance Source Map

## Purpose

The research program refers to an architectural constitution and an M0 decision sheet that were originally supplied as project attachments. The architectural constitution is now persisted as standalone files in this repository (see below). The M0 decision sheet remains an external attachment; its adopted decisions are traceable through the provenance log and STATE.md.

## Publicly auditable sources

The binding decisions adopted from those sources are represented through:

1. [`docs/ARCHITECTURAL_CONSTITUTION.md`](docs/ARCHITECTURAL_CONSTITUTION.md) — architectural constitution v1 (original as adopted at M0). Published 2026-08-18 via PR #28, Entry 62. SHA-256: `509f11c316e6ed3abbdca2df4973484dd676eecc87b727f312ee8658bef93b19`. Original provided by Rebecca from local copy.
2. [`docs/ARCHITECTURAL_CONSTITUTION_v2.md`](docs/ARCHITECTURAL_CONSTITUTION_v2.md) — architectural constitution v2 with amendment log (Entry 27 amendment recorded). Published 2026-08-18 via PR #29, Entry 63. CRITIC-CLEARED (BF1 resolved), Rebecca-approved.
3. [`docs/rulings/provenance_log.md`](docs/rulings/provenance_log.md) — chronological rulings, amendments, locked bars, retained negatives, and evidence references.
4. [`state/STATE.md`](state/STATE.md) — current governed state, active gates, locked requirements, and custody attestations.
5. [`specs/`](specs/) — milestone specifications and amendments that operationalize the adopted requirements.
6. [`reviews/`](reviews/) — independent CRITIC and JUDGE checks against the recorded authority chain.
7. [`docs/rulings/`](docs/rulings/) — verbatim principal rulings and lineage attestations.

## Verification rule

Where a standalone historical attachment and the public repository record cannot both be inspected, the repository must not claim that an outside reader independently verified the attachment itself. The defensible claim is narrower: the adopted requirements can be traced through the constitution files, provenance log, state record, specifications, reviews, and principal rulings.

The architectural constitution is now persisted as [`docs/ARCHITECTURAL_CONSTITUTION.md`](docs/ARCHITECTURAL_CONSTITUTION.md) (v1) and [`docs/ARCHITECTURAL_CONSTITUTION_v2.md`](docs/ARCHITECTURAL_CONSTITUTION_v2.md) (v2 with amendment log), published 2026-08-18. The M0 decision sheet remains an external attachment; publishing an immutable copy remains a documentation objective, subject to ownership and privacy review.
