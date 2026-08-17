# CRITIC Handoff — Public-Repository Policy Review

**Gate served:** Public-repository operating policy review (ARCHITECT → CRITIC)
**Date:** 2026-08-17 17:44 EDT
**Verdict:** BLOCK

---

## Inputs/SHAs reviewed

| Item | SHA | Source |
|---|---|---|
| GitHub main (base) | `b61ba07` | Verified — includes PR #23 |
| ARCHITECT branch | `architect/public-repository-policy` | Verified on GitHub |
| ARCHITECT result SHA | `d658d7b` | Branch HEAD — verified |

**Files reviewed:**

| File | Lines | Source |
|---|---|---|
| `PUBLIC_REPOSITORY_POLICY.md` | 292 | Fetched from `d658d7b` |
| `PUBLIC_REPOSITORY_POLICY_CHANGELOG.md` | 79 | Fetched from `d658d7b` |
| `handoffs/ARCHITECT_PUBLIC_REPOSITORY_POLICY_HANDOFF.md` | 93 | Fetched from `d658d7b` |

**Existing repo files verified at base `b61ba07`:** LICENSE, NOTICE, SECURITY.md, CONTRIBUTING.md, CITATION.cff, README.md, AI_CONTRIBUTIONS.md, FUNDING_OBJECTIVES.md, GOVERNANCE_SOURCE_MAP.md, REPRODUCING.md, RESEARCH_STATUS.md. All exist and match policy references.

**Branch count:** 39 total (38 non-main), matching the policy's "38 branches" claim.

---

## Verdict: BLOCK

Three blocking findings. The policy framework is sound — gap analysis is complete, all 10 requirements are addressed, claims discipline and governance are preserved, and no scientific content is modified. The blocking findings are narrow gaps in the scanning and remediation procedures that could leave credentials or sensitive content exposed when the repository goes public.

---

## Blocking findings

### BF1 — Credential/PII remediation path under-specified for git history (§12.1)

**Issue:** §12.1 classifies credentials, tokens, API keys, private keys, and personal contact details as "Blockers (must fix before public)." But it then says: "No history rewriting by default. If Rebecca classifies content as requiring redaction, the preferred approach is a prospective cleanup commit that adds a `PUBLIC_SAFETY_NOTES.md` documenting what was redacted and why, rather than rewriting Git history."

A prospective cleanup commit does NOT remove credentials from git history. Once the repository is public, any credential in any historical commit is accessible via `git log`, `git show`, or GitHub's commit browsing interface. A cleanup commit only adds a note — it doesn't redact the historical content.

§11.2 prohibits history rewriting: "No `git rebase`, `git filter-branch`, `git filter-repo`, or history-rewriting operation is authorized on the main branch or any merged branch." This creates a contradiction: credentials are blockers, but the only remediation path offered (cleanup commit) doesn't actually remove them, and the effective remediation (history rewriting) is prohibited.

**Required fix (ARCHITECT scope):** The policy must explicitly state that for credential/PII blockers found in git history:
1. The credential must be rotated or revoked before the repository goes public (making the historical exposure moot).
2. If rotation/revocation is not possible, the repository must not go public until the credential-containing commits are remediated through an authorized exception to the history-rewriting prohibition.
3. A cleanup commit alone is insufficient for credential remediation — it documents but does not remediate.

### BF2 — Pre-publication scan file-content scope too narrow (§12.1)

**Issue:** §12.1 specifies the pre-publication scan covers:
- All branches ✓
- All commit messages across all branches ✓
- All handoffs, STATE.md entries, and provenance entries ✓
- All file contents in `handoffs/`, `state/`, `docs/`, `runs/` ✗

The file-content scan is limited to 4 directories. The repository also contains `src/` (code), `specs/` (specifications), `reviews/` (review documents), `verification/` (verification scripts), `diagnostics/` (diagnostic runs), root-level documentation files, `.github/` (CI workflows), and `packages/`. While these are less likely to contain credentials or PII, a pre-publication scan for public release must be comprehensive.

Existing handoffs and review documents may contain absolute paths, session references, or internal operational language in any directory. Test fixtures in `src/` might contain seed values or path references. Verification scripts might contain hardcoded paths.

**Required fix (ARCHITECT scope):** Expand the file-content scan scope to "all file contents across all directories" or explicitly list all directories including `src/`, `specs/`, `reviews/`, `verification/`, `diagnostics/`, `packages/`, `.github/`, and root-level files.

### BF3 — Branch-push scan may miss secrets in intermediate commits (§3.2)

**Issue:** §3.2 says: "Run a secret-detection tool (e.g., `gitleaks`, `trufflehog`, or equivalent) against the full diff of the push."

"The full diff of the push" is ambiguous. If interpreted as the diff between the branch tip and its base (i.e., the cumulative diff), it would miss secrets that were added in an intermediate commit and later removed. Those intermediate commits become public when the branch is pushed, exposing the secret even though it doesn't appear in the final diff.

For example, if a developer accidentally commits an API key in commit A, then removes it in commit B, the final diff (A→B net) doesn't show the key — but commit A is still in the branch history and will be publicly accessible.

**Required fix (ARCHITECT scope):** Change "full diff of the push" to "all new commits introduced by the push, including intermediate commits and their diffs." Explicitly state that the scan must cover every commit in the push range, not just the net diff. Note that tools like `gitleaks` typically scan commit history by default, but the policy should be unambiguous.

---

## Non-blocking findings

### NF1 — Branch pruning should preserve content, not just metadata (§12.3)

§12.3 says: "Rebecca authorizes removal of the remote branch ref. The branch name and head SHA are recorded by the RECORDER before pruning." For D1–D5 (Persistence Doctrine), recording the name and SHA is insufficient if the branch contains unmerged scientific content. The RECORDER should preserve a private archive (e.g., `git bundle`) of the branch before pruning the public ref, or explicitly attest that the branch content is fully merged into main and no unique content is lost.

### NF2 — Regex pattern list should be labeled as minimum (§3.2)

The regex patterns listed in §3.2 cover common credential families (`ghp_`, `sk-`, `AKIA`, `xox`, `-----BEGIN`). The list should be explicitly labeled as "minimum examples, not exhaustive" and should mention that the binding secret-scanning tool (gitleaks/trufflehog) provides additional coverage. Consider adding JWT patterns, `.env` file detection, service-account JSON, SSH keys, and cloud provider tokens.

### NF3 — Large artifact inventory should specify canonical checksum method (§6.2)

§6.2 requires "Root checksum: SHA-256 of the artifact root directory" and "Manifest checksum: SHA-256 of `m3_v44_raw_manifest.json`." The policy should specify the canonical method for computing a directory checksum (e.g., `sha256sum` of sorted file list with per-file hashes, or `tar` + `sha256sum`).

### NF4 — Rebecca's email publication status should be verified

§3.2 allows Rebecca's email (`darkside73826779@gmail.com`) as an exception. The policy should verify this email is already intentionally published in `CITATION.cff`, `README.md`, or `SECURITY.md` at the base SHA. If not, its publication should be a Rebecca decision, not an automatic exception.

---

## Verified correct

1. **Completeness (10 requirements):** All 10 requirements addressed. Gap analysis accurate: 4 met, 4 partially met, 2 missing. All gaps have corresponding policy sections. ✓
2. **Claims discipline (§5):** INSTRUMENT FAILURE, negative results, crashes, and unresolved limitations must remain accurately labeled. Commit messages must not reframe negatives as positives. RESEARCH_STATUS.md must include all milestone outcomes including failures. ✓
3. **Funding/outreach separation (§7):** Funding documents must not be cited as scientific evidence or authority. Must preserve claims boundary (no consciousness, AGI, sentience claims). Must state evidence status (M3 does not hold overall pass). ✓
4. **Licensing consistency (§8):** Apache 2.0, Rebecca R. McClintic attribution, CITATION.cff metadata. All verified at base SHA. ✓
5. **Rebecca's sole gate/merge authority (§14):** "Rebecca sole gate/merge authority: No merge performed or requested." Policy routes to Rebecca for approval and conflict decisions. ✓
6. **Prospective application (§11):** Historical content preserved unchanged. No history rewriting on main/merged branches. Policy applies prospectively only. ✓
7. **No scientific content modified:** Branch diff shows only 3 new files (policy, changelog, handoff). No bars, scoring predicates, verdicts, evidence, STATE.md, or provenance_log.md modified. ✓
8. **Standing constraints (§14):** O-14, O-15 not applicable. D1–D5 binding. L9, L18 not touched. No L15/L16/L17. ✓
9. **Existing file references:** All 11 referenced files verified to exist at base SHA `b61ba07`. ✓
10. **Branch count:** 39 total branches (38 non-main), matching policy's claim. ✓

---

## Conflict resolution assessment

**Conflict 1 (pre-publication scan):** Sound framework — mandatory scan, findings classified by severity, no going public until blockers resolved. Gaps in remediation path (BF1) and scan scope (BF2) need fixing.

**Conflict 2 (branch-push workflow):** Sound — self-scan before push, attestation in handoff. Gap in scan scope (BF3) needs fixing.

**Conflict 3 (existing 38 branches):** Sound two-step approach — inventory and scan, then Rebecca decides per-branch. Gap in preservation before pruning (NF1) should be addressed.

---

## Preserved evidence

- Policy framework is sound: 10 requirements addressed, governance preserved, claims discipline maintained.
- No scientific content, bars, verdicts, or evidence modified.
- INSTRUMENT FAILURE label retained.
- No scoring run, seed execution, or hold-out seed exposure occurred.
- All referenced files verified at base SHA.
- Branch count verified.

---

## Exact next authorized role

**ARCHITECT** — Resolve BF1–BF3, re-submit for CRITIC review.

After CRITIC approval: **Rebecca** (approve policy + decide on conflicts) → **INTEGRATOR** (update STATE.md + role initialization scripts) → **RECORDER** (attest + record) → **Rebecca** (merge — publication-readiness merge) → repo goes public.

---

## Explicitly prohibited actions

- No modification of scientific bars, scoring predicates, historical verdicts, or evidence.
- No modification of any historical file, SHA, ruling, or provenance entry.
- No merging to main (Rebecca is sole merge authority).
- No scoring, seed execution, or hold-out seed exposure.
- No running of seeds 201–203 or 301–303.
- No modification of STATE.md (INTEGRATOR custody).
- No L15/L16/L17 before M5.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.

---

## Confirmation

No scoring, rerun of failed scoring, hold-out seed exposure, or unauthorized merge occurred during this review. The CRITIC reviewed the policy read-only and did not modify any specification, implementation, scoring artifact, or STATE.md.

Standing constraints verified: O-14 (no re-run-on-failure) — not applicable; O-15 (development runs diagnostic-only) — not applicable; D1–D5 (Persistence Doctrine) — binding, policy committed to branch; L9 (hard fence) — not touched; L18 (full battery) — not modified; no L15/L16/L17 introduced; Rebecca sole gate/merge authority — no merge performed or requested.
