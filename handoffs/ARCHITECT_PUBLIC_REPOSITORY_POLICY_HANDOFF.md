# ARCHITECT Handoff — Public-Repository Operating Policy (v1.1)

**Gate served:** Public-repository operating policy definition (Rebecca principal ruling)
**Issued by:** ARCHITECT
**Date:** 2026-08-17 17:48 EDT

---

## Input SHAs reviewed

| Item | SHA | Verified |
|---|---|---|
| GitHub main (base) | `b61ba07` | Verified via `git ls-remote` |
| ARCHITECT branch | `architect/public-repository-policy` | Verified on GitHub |
| ARCHITECT result SHA | `b767e53eb30eca3671b9bc8b61695719bbeb28d6` | Verified via `git ls-remote` |

## Files created

| File | Description |
|---|---|
| `PUBLIC_REPOSITORY_POLICY.md` | Operating policy v1.1 (311 lines) |
| `PUBLIC_REPOSITORY_POLICY_CHANGELOG.md` | Companion changelog (97 lines) |

## CRITIC BF1–BF3 + NF1–NF4 resolution summary

**BF1 (Credential remediation in git history):** New §3.5 defines the remediation path: rotate/revoke credentials before going public; if impossible, authorized exception to history-rewriting prohibition requires Rebecca's explicit authorization; cleanup commit alone is insufficient.

**BF2 (Pre-publication scan scope):** §12.1 scan now covers all directories: `src/`, `specs/`, `reviews/`, `verification/`, `diagnostics/`, `packages/`, `.github/`, root-level files, plus previously listed `handoffs/`, `state/`, `docs/`, `runs/`.

**BF3 (Intermediate commit scanning):** §3.2 now specifies scanning all new commits including intermediate commits and their diffs, not just the net diff.

**NF1 (Branch pruning preservation):** §12.3 Option B requires RECORDER to preserve a private archive (`git bundle`) or attest that branch content is fully merged before pruning.

**NF2 (Regex patterns as minimum):** §3.2 pattern list labeled "minimum examples, not exhaustive." Added JWT, `.env`, service-account JSON, SSH keys, cloud provider tokens.

**NF3 (Checksum method):** §6.2 specifies `find . -type f | sort | xargs sha256sum` for directory checksum, `sha256sum` for manifest.

**NF4 (Email publication):** New §3.4: Principal's email is not in any existing public file. Publication of any email is a Rebecca decision.

## Gap analysis

10 requirements assessed. 4 met, 4 partially met, 2 missing. All gaps have corresponding policy sections. Full table in §1 of the policy.

## Conflict resolutions

1. **Pre-publication scan:** Mandatory scan covering all directories. Findings classified as blockers/Rebecca decisions/acceptable. Credential blockers require rotation/revocation or authorized exception (§3.5).
2. **Branch-push workflow:** Self-scan before push + attestation in handoff.
3. **Existing 38 branches:** RECORDER inventories all names/SHAs. Each scanned. Rebecca decides per-branch: publish or prune (with private archive preservation).

## Verdict/status

**Policy v1.1 complete. CRITIC BF1–BF3 resolved. Ready for CRITIC re-review.**

No scientific content, bars, verdicts, or evidence modified. No STATE.md or provenance_log.md modified.

## Next recipient

**CRITIC** — Re-review v1.1 for BF1–BF3 + NF1–NF4 resolution correctness, then Rebecca (approve + decide conflicts) → INTEGRATOR → RECORDER → Rebecca (merge).

## Explicitly prohibited actions

- No modification of scientific bars, scoring predicates, historical verdicts, or evidence.
- No modification of any historical file, SHA, ruling, or provenance entry.
- No merging to main (Rebecca sole merge authority).
- No scoring, seed execution, or hold-out seed exposure.
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
