# ARCHITECT Handoff — Public-Repository Operating Policy

**Gate served:** Public-repository operating policy definition (Rebecca principal ruling)
**Issued by:** ARCHITECT
**Date:** 2026-08-17 17:39 EDT

---

## Input SHAs reviewed

| Item | SHA | Verified |
|---|---|---|
| GitHub main (base) | `b61ba07` (includes `91b2f0f` + PR #23 public-funding-readiness) | Verified via `git ls-remote` |
| `LICENSE` | `b61ba07` | Apache 2.0 |
| `NOTICE` | `b61ba07` | Rebecca R. McClintic attribution |
| `SECURITY.md` | `b61ba07` | Private vulnerability reporting |
| `CONTRIBUTING.md` | `b61ba07` | No credentials, no history rewriting |
| `CITATION.cff` | `b61ba07` | Citation metadata |
| `README.md` | `b61ba07` | Project overview |
| `AI_CONTRIBUTIONS.md` | `b61ba07` | AI contribution disclosure |
| `FUNDING_OBJECTIVES.md` | `b61ba07` | Funding objectives |
| `GOVERNANCE_SOURCE_MAP.md` | `b61ba07` | Governance source map |
| `REPRODUCING.md` | `b61ba07` | Reproduction instructions |
| `RESEARCH_STATUS.md` | `b61ba07` | Research status (M3 INSTRUMENT FAILURE) |
| `.github/workflows/` | `b61ba07` | CI workflow |
| Remote branches | 38 branches inventoried | `git branch -r` |

## Files created

| File | Description |
|---|---|
| `PUBLIC_REPOSITORY_POLICY.md` | Operating policy (293 lines) |
| `PUBLIC_REPOSITORY_POLICY_CHANGELOG.md` | Companion changelog (80 lines) |

## Branch/result SHA

- **Branch:** `architect/public-repository-policy`
- **Base SHA:** `b61ba07` (GitHub main)
- **Result SHA:** (to be filled after push — see below)

## Gap analysis

10 requirements assessed against existing files. 4 met, 4 partially met, 2 missing. Full table in §1 of the policy and the changelog. Key gaps:
- Credential/PII scanning procedure: missing → defined in §3
- Branches as publishable surfaces: missing → defined in §9
- Prospective application: missing → defined in §11
- Public-readable writing standard: partially met → formalized in §4

## Conflict resolutions

1. **Pre-publication scan:** Mandatory one-time scan before public flip. Findings classified as blockers (credentials/PII), Rebecca decisions (paths/internal language), or acceptable. No history rewriting by default. (§12.1)
2. **Branch-push workflow:** Each role self-scans before push and records scan attestation in handoff. (§9.2, §12.2)
3. **Existing 38 branches:** RECORDER inventories all branch names/SHAs. Each scanned. Rebecca decides per-branch: publish as-is or prune (after recording in provenance). (§12.3)

## Key definitions

- **Credential/PII scanning procedure (§3):** Secret scanning tool + regex checks + content review. Scan attestation in handoff.
- **Public-readable writing standard (§4):** Understandable by outside reader, define terms, distinguish evidence from interpretation, preserve claims boundaries, no infrastructure leakage.
- **Large artifact inventory (§6):** `LOCAL_ARTIFACT_INVENTORY.md` with file count, byte count, checksums, retention statement, access procedure. To be produced by RECORDER before publication-readiness merge.

## Verdict/status

**Policy draft complete. Ready for CRITIC review.**

No scientific content, bars, verdicts, or evidence was modified. No STATE.md or provenance_log.md was modified. No merge performed or requested.

## Blockers and non-blocking findings

**No blockers.** This is a policy document; no code implemented, no seeds run, no bars modified.

## Exact next recipient role

**CRITIC** — Review the policy for:
- Completeness of gap analysis against Rebecca's 10 requirements
- Correctness of conflict resolutions
- Adequacy of credential/PII scanning procedure
- Adequacy of public-readable writing standard
- Adequacy of large artifact inventory procedure
- No scientific content modified
- No standing constraints violated

After CRITIC approval: **Rebecca** (approve policy + decide on conflicts) → **INTEGRATOR** (update STATE.md + role initialization scripts) → **RECORDER** (attest + record) → **Rebecca** (merge — publication-readiness merge) → repo goes public.

## Explicitly prohibited actions

- No modification of scientific bars, scoring predicates, historical verdicts, or evidence.
- No modification of any historical file, SHA, ruling, or provenance entry.
- No modification of constitution laws or standing constraints.
- No merging to main (Rebecca is sole merge authority).
- No scoring, seed execution, or hold-out seed exposure.
- No running of seeds 201–203 or 301–303.
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
