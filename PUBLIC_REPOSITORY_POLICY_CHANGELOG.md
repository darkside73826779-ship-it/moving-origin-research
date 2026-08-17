# Public-Repository Operating Policy — Changelog

**Policy:** `PUBLIC_REPOSITORY_POLICY.md`
**Date:** 2026-08-17 · **Author:** ARCHITECT
**Base SHA:** `b61ba07` (GitHub main)
**Branch:** `architect/public-repository-policy`

---

## What this policy does

Defines the operating rules for the `moving-origin-research` repository as a public surface. Covers: prohibited content, credential/PII scanning, public-readable writing standard, negative results preservation, large local artifact inventory, funding/outreach separation, licensing consistency, branches as publishable surfaces, vulnerability disclosure, and prospective application.

Addresses three conflicts identified by WORKFLOW COORDINATOR: pre-publication scan, branch-push workflow change, and existing 38 branches.

## What this policy does NOT do

- Does not modify scientific bars, scoring predicates, historical verdicts, or evidence.
- Does not modify any historical file, SHA, ruling, or provenance entry.
- Does not modify constitution laws or standing constraints.
- Does not merge to main (Rebecca sole merge authority).
- Does not rewrite Git history.
- Does not implement code (ARCHITECT role boundary).

---

## Gap analysis summary

| # | Requirement | Existing | Status | Policy section |
|---|---|---|---|---|
| 1 | No sensitive content | SECURITY.md, CONTRIBUTING.md | Partially met | §2 |
| 2 | Credential/PII scanning | None | Missing → defined | §3 |
| 3 | Public-readable writing | README, RESEARCH_STATUS | Partially met → formalized | §4 |
| 4 | Negative results preserved | RESEARCH_STATUS, CONTRIBUTING, FUNDING_OBJECTIVES | Met → reinforced | §5 |
| 5 | Large artifact inventory | REPRODUCING.md (mentions) | Partially met → procedure defined | §6 |
| 6 | Funding/outreach separation | FUNDING_OBJECTIVES, AI_CONTRIBUTIONS | Met → reinforced | §7 |
| 7 | Licensing consistency | LICENSE, NOTICE, CITATION.cff, CONTRIBUTING | Met → reinforced | §8 |
| 8 | Branches as public surfaces | None | Missing → defined | §9 |
| 9 | No public vuln disclosure | SECURITY.md | Met → reinforced | §10 |
| 10 | Prospective application | None | Missing → defined | §11 |

## Conflict resolutions

1. **Pre-publication scan:** Mandatory one-time scan before public flip. Findings classified as blockers (credentials/PII), Rebecca decisions (paths/internal language), or acceptable. No history rewriting by default.
2. **Branch-push workflow:** Each role self-scans before push and records scan attestation in handoff. Adds one step to existing workflow.
3. **Existing 38 branches:** RECORDER inventories all branch names/SHAs. Each scanned. Rebecca decides per-branch: publish as-is or prune public ref (after recording name/SHA in provenance).

## New files

| File | Description |
|---|---|
| `PUBLIC_REPOSITORY_POLICY.md` | Operating policy (293 lines) |
| `PUBLIC_REPOSITORY_POLICY_CHANGELOG.md` | This changelog |

## Files reviewed

| File | Content |
|---|---|
| `LICENSE` | Apache License 2.0 |
| `NOTICE` | Copyright 2026 Rebecca R. McClintic |
| `SECURITY.md` | Security policy — private reporting, no public disclosure |
| `CONTRIBUTING.md` | Contribution policy — no credentials, no history rewriting |
| `CITATION.cff` | Citation metadata |
| `README.md` | Project overview — falsifiable research, milestone status |
| `AI_CONTRIBUTIONS.md` | AI contribution disclosure — role separation, human authority |
| `FUNDING_OBJECTIVES.md` | Funding objectives — independent validation, not relabeling |
| `GOVERNANCE_SOURCE_MAP.md` | Governance source map — maps governing documents |
| `REPRODUCING.md` | Reproduction instructions — 63 tests, large artifact note |
| `RESEARCH_STATUS.md` | Research status — M1/E1 PASS, M3 INSTRUMENT FAILURE |
| `.github/workflows/` | CI workflow — non-scoring tests on push/PR |

## Standing constraints verified

- O-14: Not applicable.
- O-15: Not applicable.
- D1–D5: Specification committed to GitHub branch; no STATE.md or provenance_log.md modification.
- L9, L18: Not touched.
- No L15/L16/L17 introduced.
- Rebecca sole gate/merge authority: No merge performed or requested.
