# Public-Repository Operating Policy

**Status:** ARCHITECT draft — requires CRITIC review and Rebecca approval
**Date:** 2026-08-17 · **Author:** ARCHITECT
**Base SHA:** `b61ba07` (GitHub main, includes PR #23 public-funding-readiness)
**Authority chain:** Rebecca > constitution's laws > approved specifications > this policy > agent judgment
**Effective:** Upon Rebecca's publication-readiness merge. All rules apply prospectively; historical files, SHAs, rulings, and evidence are preserved unchanged.

---

## 0. Purpose

This policy governs the operation of the `darkside73826779-ship-it/moving-origin-research` repository as a public surface. It defines what may be pushed, how content must be reviewed before push, how public writing must be structured, how negative results are preserved, how large local artifacts are inventoried, and how the transition from private to public is managed.

This policy does not modify scientific bars, scoring predicates, historical verdicts, or evidence. It does not modify constitution laws or standing constraints. It applies prospectively only.

---

## 1. Gap analysis — existing files vs. Rebecca's 10 requirements

| # | Requirement | Existing coverage | Status |
|---|---|---|---|
| 1 | No sensitive content in pushes | SECURITY.md: don't disclose in public issues. CONTRIBUTING.md: don't include credentials in PRs. | **Partially met** — no pre-push scanning procedure |
| 2 | Credential/PII scanning before push | None | **Missing** — §3 defines procedure |
| 3 | Public-readable writing standard | README, RESEARCH_STATUS, AI_CONTRIBUTIONS are well-written for public readers | **Partially met** — no formal standard for handoffs, STATE.md, provenance, commit messages; §4 defines |
| 4 | Negative results preserved | RESEARCH_STATUS: INSTRUMENT FAILURE accurately labeled. CONTRIBUTING.md: "Do not rewrite Git history or remove negative results." FUNDING_OBJECTIVES: "would not be used to relabel historical failures." | **Met** — §5 reinforces |
| 5 | Large local artifact inventory | REPRODUCING.md: mentions 257,636 files / 16.3 GB locally. No committed inventory, checksums, or access procedure beyond "open a GitHub issue." | **Partially met** — §6 defines procedure |
| 6 | Funding/outreach separation | FUNDING_OBJECTIVES.md clearly labeled as communications. AI_CONTRIBUTIONS.md: "AI-generated output is not treated as independent scientific validation." | **Met** — §7 reinforces |
| 7 | Licensing/attribution consistency | LICENSE (Apache 2.0), NOTICE (Rebecca R. McClintic), CITATION.cff, CONTRIBUTING.md (Apache 2.0 contribution terms) | **Met** — §8 reinforces |
| 8 | Branches as publishable surfaces | None | **Missing** — §9 defines |
| 9 | No public vulnerability disclosure | SECURITY.md: "Do not disclose credentials, exploitable vulnerabilities, private machine information, or sensitive artifact contents in a public issue." | **Met** — §10 reinforces |
| 10 | Prospective application | None | **Missing** — §11 defines |

---

## 2. Prohibited content in pushes

No branch, commit, handoff, log, artifact, or tag may contain:

- Credentials, API keys, tokens, passwords, or secrets of any kind
- Private contact details (personal email addresses beyond Rebecca's published attribution, phone numbers, physical addresses)
- Personal machine identifiers (hostnames, MAC addresses, Windows SIDs, user account names)
- Private absolute paths (e.g., `/home/user/workspace/...`, `C:\Users\...`)
- Environment dumps, shell history, or runtime configuration containing secrets
- Unreviewed executor logs, session transcripts, or raw model outputs not intended for publication
- Scoring seed identities (seeds 201–203, 301–303, or any future scoring seeds) beyond what is already recorded in the historical provenance

**Historical content note:** Existing commits, handoffs, and STATE.md entries may contain absolute paths (`/home/user/workspace/...`) and internal operational language. Per §11 (prospective application), these are preserved unchanged. The pre-publication scan (§12) classifies whether any historical content requires redaction before the repository goes public.

---

## 3. Credential/PII scanning procedure

### 3.1 When to scan

Every role must run a public-safety scan **before pushing any branch** that contains:
- New or modified files in `handoffs/`, `state/`, `docs/`, `runs/`, `diagnostics/`, or `verification/`
- New or modified log files, artifact manifests, or JSON outputs
- Any file not previously scanned

Scans are not required for pushes that only modify files under `src/` (code) or `specs/` (specifications) that have already been reviewed, unless those files embed paths, credentials, or PII.

### 3.2 Required checks

1. **Secret scanning:** Run a secret-detection tool (e.g., `gitleaks`, `trufflehog`, or equivalent) against the full diff of the push. Any finding is a publication blocker.
2. **Pattern checks:** Regex scan for:
   - API keys and tokens (e.g., `ghp_`, `sk-`, `AKIA`, `xox`, bearer tokens)
   - Private keys (`-----BEGIN`)
   - Email addresses other than Rebecca's published attribution (`darkside73826779@gmail.com` is the principal's published contact)
   - Phone numbers, physical addresses
   - Absolute paths matching `/home/`, `/Users/`, `C:\Users\`, or sandbox hostnames
   - Environment variable dumps (`API_KEY=`, `SECRET=`, `TOKEN=`)
3. **Content review:** Manually review any new handoff, STATE.md entry, provenance entry, or commit message for:
   - Internal operational language not understandable by an outside reader
   - Session references, agent model names, or infrastructure details not relevant to the scientific record
   - Unreviewed executor logs or raw model outputs

### 3.3 Scan evidence

Each handoff that precedes a push must include a scan attestation:
```
Public-safety scan: <tool(s) used>, <scope>, <findings count>, <disposition>
```

If findings are zero: `"Public-safety scan: gitleaks + regex, full diff, 0 findings, cleared."`

If findings are nonzero: the push is blocked until findings are resolved or explicitly waived by Rebecca.

---

## 4. Public-readable writing standard

### 4.1 Scope

This standard applies to all content that will be visible in the public repository: handoffs, STATE.md entries, provenance log entries, commit messages, issue text, PR descriptions, and any documentation file.

### 4.2 Requirements

1. **Understandable by an outside reader:** Define specialized terminology on first use. Do not assume the reader knows the project's internal vocabulary (e.g., "CRITIC," "TASK BUILDER," "INSTRUMENT FAILURE"). Provide context.
2. **Distinguish evidence from interpretation:** Clearly separate what was measured from what it means. Use "measured" or "observed" for data; use "interpreted as" or "suggests" for conclusions.
3. **Preserve claims boundaries:** Do not overstate. If a result is an INSTRUMENT FAILURE, say so. If evidence is preliminary, say so. Do not use language that implies peer review, institutional validation, or consciousness/AGI claims.
4. **No internal jargon without definition:** Terms like "D1–D5," "O-14," "L9," "V4.4" must be defined or cross-referenced on first use in any public-facing document.
5. **No infrastructure leakage:** Do not reference sandbox environments, agent model names, session IDs, or execution infrastructure in public writing unless directly relevant to the scientific record.

### 4.3 Commit message standard

Commit messages must:
- State what was done and why, in language a reviewer outside the project can understand
- Reference relevant specs, reviews, or rulings by file path
- Not contain absolute paths, session references, or internal operational shorthand

---

## 5. Negative results preservation

### 5.1 Binding rule

INSTRUMENT FAILURE, negative results, crashes, unresolved limitations, and borderline cases must remain accurately labeled. They must not be hidden, softened, renamed, reinterpreted, or silently replaced.

### 5.2 Existing protections (reinforced)

- `CONTRIBUTING.md` §3: "Do not rewrite Git history or remove negative results to simplify the narrative."
- `FUNDING_OBJECTIVES.md`: "It would not be used to relabel historical failures or tune locked results after observation."
- `RESEARCH_STATUS.md`: M3 V4.4 is labeled "Overall INSTRUMENT FAILURE" with full context.

### 5.3 Additional protections

- Commit messages must not reframe a negative result as a positive one. If a fix addresses a construction bug, the fix must state that the original result is preserved and was not re-run.
- PR descriptions must not omit failed checks from summaries.
- The `RESEARCH_STATUS.md` table must include all milestone outcomes, including failures.

---

## 6. Large local artifact inventory procedure

### 6.1 What exists

The M3 V4.4 scoring runs (seeds 201–203 and 301–303) generated 257,636 raw artifact files totaling approximately 16.3 GB, plus a ~202 MB raw manifest. These are retained locally on Rebecca's system, not in the GitHub repository.

### 6.2 Required committed inventory

Before the publication-readiness merge, the RECORDER (or Rebecca-authorized custodian) must commit a file `LOCAL_ARTIFACT_INVENTORY.md` to the repository containing:

| Field | Value |
|---|---|
| Artifact set name | M3 V4.4 scoring raw artifacts |
| Local retention owner | Rebecca R. McClintic |
| File count | 257,636 |
| Total byte count | (to be computed by custodian) |
| Raw manifest | `m3_v44_raw_manifest.json` (~202 MB, committed summary only) |
| Root checksum | SHA-256 of the artifact root directory (to be computed) |
| Manifest checksum | SHA-256 of `m3_v44_raw_manifest.json` |
| Scoring seeds | 201, 202, 203, 301, 302, 303 (identities already in provenance) |
| Retention statement | Artifacts retained locally; not silently replaced; not deleted |
| Access procedure | Open a GitHub issue labeled "artifact-access request"; do not transmit credentials in public issues |

### 6.3 Future artifacts

Any future scoring run that generates large local artifacts must have its inventory added to `LOCAL_ARTIFACT_INVENTORY.md` before the results are merged.

---

## 7. Funding and outreach separation

Funding and outreach documents (`FUNDING_OBJECTIVES.md`, `AI_CONTRIBUTIONS.md`, future outreach materials) are communications materials. They:
- Must not be cited as scientific evidence or authority for changing specifications, bars, or controls
- Must not reframe negative results
- Must clearly state the project's evidence status (M3 does not hold an overall pass)
- Must preserve the claims boundary (no consciousness, AGI, or sentience claims)

---

## 8. Licensing and attribution consistency

All files must maintain consistency with:
- **License:** Apache License 2.0 (`LICENSE`)
- **Attribution:** Copyright 2026 Rebecca R. McClintic (`NOTICE`)
- **Citation:** `CITATION.cff` metadata
- **Contribution terms:** Apache 2.0 (`CONTRIBUTING.md`)
- **Security reporting:** `SECURITY.md`

New files that include copyright or license headers must use the same form. No file may introduce a different license.

---

## 9. Branches as publishable surfaces

### 9.1 All branches are public

Every branch, tag, commit, handoff, and log pushed to the remote repository is a public surface. Public-safety review (§3) occurs **before push**, not only before merge.

### 9.2 Role workflow change

The existing branch-per-role convention is modified:

1. **Before push:** The role runs the public-safety scan (§3) and records the scan attestation in the handoff.
2. **Push:** The role pushes the branch to GitHub.
3. **Before merge:** CRITIC reviews the branch (existing process, unchanged).

### 9.3 What this means for each role

- **ARCHITECT:** Scan specification files and handoffs before push. Specifications rarely contain sensitive content, but handoffs may reference absolute paths.
- **TASK BUILDER:** Scan code, test files, and handoffs before push. Code rarely contains sensitive content, but test fixtures or log outputs might.
- **CRITIC:** Scan review files and handoffs before push.
- **RECORDER:** Scan provenance entries, custody attestations, and STATE.md updates before push. These are the highest-risk files for path leakage and internal language.
- **INTEGRATOR:** Scan STATE.md updates and role initialization scripts before push.

---

## 10. No public vulnerability disclosure

Reinforces `SECURITY.md`:
- Security vulnerabilities, credentials, and exploitable issues must never be disclosed through public issues, PRs, or commit messages.
- Use GitHub's private vulnerability reporting feature.
- If private reporting is unavailable, open a public issue with no sensitive details and request a private channel.

---

## 11. Prospective application

### 11.1 Historical content preserved

All existing files, commits, branches, SHAs, rulings, provenance entries, and evidence are preserved unchanged. This policy applies prospectively only.

### 11.2 What this means

- Existing content that may contain absolute paths, internal operational language, or session references is not rewritten.
- The pre-publication scan (§12) determines whether any historical content requires Rebecca's decision before going public.
- No `git rebase`, `git filter-branch`, `git filter-repo`, or history-rewriting operation is authorized on the main branch or any merged branch.

---

## 12. Pre-publication scan and conflict resolutions

### 12.1 Conflict 1 — Pre-publication scan of existing content

**Recommendation:** A mandatory one-time pre-publication scan must run before the repository is flipped to public. The scan covers:
- All branches (§12.3)
- All commit messages across all branches
- All handoffs, STATE.md entries, and provenance entries
- All file contents in `handoffs/`, `state/`, `docs/`, `runs/`

**Classification of findings:**
- **Blockers (must fix before public):** Credentials, tokens, API keys, private keys, personal contact details beyond Rebecca's published attribution.
- **Rebecca decisions (flag for principal):** Absolute paths (`/home/user/workspace/...`), internal operational language, session references, agent model names. Rebecca decides whether to accept these as historical artifacts of the development process or require redaction.
- **Acceptable as-is:** Internal role names (ARCHITECT, CRITIC, TASK BUILDER, etc.) that are already documented in `AI_CONTRIBUTIONS.md`. Governance terminology (O-14, D1–D5, etc.) that is cross-referenced in `GOVERNANCE_SOURCE_MAP.md`.

**No history rewriting by default.** If Rebecca classifies content as requiring redaction, the preferred approach is a prospective cleanup commit that adds a `PUBLIC_SAFETY_NOTES.md` documenting what was redacted and why, rather than rewriting Git history.

### 12.2 Conflict 2 — Branch-push workflow change

**Recommendation:** Implement the workflow change described in §9.2. Each role self-scans before pushing and records the scan attestation in the handoff. This adds one step (scan + attest) to the existing role workflow, before the push step.

The handoff format is extended with a required field:
```
Public-safety scan: <tool(s)>, <scope>, <findings>, <disposition>
```

### 12.3 Conflict 3 — Existing 38 branches

**Recommendation:** A two-step approach:

1. **Inventory and scan (before public flip):** The RECORDER records all branch names and head SHAs in `LOCAL_ARTIFACT_INVENTORY.md` or a dedicated `BRANCH_INVENTORY.md`. Each branch is scanned per §3. Findings classified per §12.1.

2. **Rebecca's decision per branch:** For each branch with findings:
   - **Option A (publish as-is):** Rebecca accepts the content as a historical artifact of the development process. The branch remains public.
   - **Option B (prune public ref):** Rebecca authorizes removal of the remote branch ref. The branch name and head SHA are recorded by the RECORDER before pruning. No silent branch deletion — the record is preserved in provenance.

Stale branches (e.g., `state-m2-complete`) that have been fully merged and serve no ongoing purpose may be pruned with Rebecca's authorization after RECORDER records their names and head SHAs.

---

## 13. Effective date and transition

This policy becomes effective upon Rebecca's publication-readiness merge. Between CRITIC approval and Rebecca's merge:
- The policy is binding on all new work (new branches, new handoffs, new commits)
- The pre-publication scan (§12) is conducted
- Rebecca decides on flagged content
- The repository is flipped to public only after all blockers are resolved and Rebecca's decisions are recorded

---

## 14. Standing constraints

- O-14 (no re-run-on-failure): Not applicable to this policy.
- O-15 (development runs diagnostic-only): Not applicable to this policy.
- D1–D5 (Persistence Doctrine): Binding. This policy is committed to a branch; no STATE.md or provenance_log.md modification.
- L9 (hard fence): Not touched.
- L18 (full battery): Not modified.
- No L15/L16/L17 before M5.
- Rebecca sole gate/merge authority: No merge performed or requested.
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label.
