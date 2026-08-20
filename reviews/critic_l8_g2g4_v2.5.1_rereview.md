# CRITIC Re-Review — L8 Instantiation Spec v2.5.1 (Provenance-Pointer Remediation)

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Reviewer:** Fresh-context CRITIC (independent, read-only)
**Gate served:** CRITIC re-review of the v2.5.1 amendment — provenance-pointer correction and workload clarification after the v2.5 BLOCK.

## Inputs / SHAs reviewed
- **Prior version (v2.5, CRITIC-BLOCKed):** `5209f3317232679a3c676af7944a4cc5dcdeed00`
- **Amended HEAD (v2.5.1):** `081df58131d8` ("Correct L8 law provenance pointers") on `architect/l8-g2g4-remediation`
- **Delta reviewed:** `5209f33...081df58` — `06_l8_instantiation_spec.md` (+8/−5); changelog (+14); 2 handoff files (one new, one marked superseded)
- **Constitution (verification source):** `docs/ARCHITECTURAL_CONSTITUTION_v2.md` (on `main`) — L8 at line 28, L14 at line 42 (re-confirmed)
- Files read (only those the handoff points to): the spec, its changelog, the v2.5.1 CRITIC re-review handoff, the superseded v2.5 handoff, the constitution.

## Verdict
**CLEAR** — the blocking provenance-citation defect is corrected and verified; v2.5 scientific and implementation-contract substance is byte-for-byte unchanged; the workload clarification is accurate and internally consistent; no new issues introduced; §5 P6 now passes; all standing constraints preserved.

## 1. Provenance pointers corrected and verified (blocking fix) — PASS
The v2.5 Sources line cited `[LAW-L8]` "constitution line 26" and `[LAW-L14]` "line 40" (line 26 = L7 Mirror standard; line 40 = L13 Memory writes through the now). v2.5.1 now cites `[LAW-L8]` `docs/ARCHITECTURAL_CONSTITUTION_v2.md` line 28 and `[LAW-L14]` line 42. Verified directly against the constitution: L8 header at line 28, L14 header at line 42. Pointers now resolve to the correct laws. No verbatim law text was changed — only the citation pointer (and an explicit file-path reference for L8) was corrected.

## 2. v2.5 substance genuinely unchanged — PASS
The spec delta contains exactly two hunks:
- Header: title (v2.5 → v2.5.1), status line, and Sources pointer.
- §8.10.8: one feasibility-sentence workload clarification (see §3 below).

§8.10.1–§8.10.7 (bootstrap RNG/seed-manifest scope; exact resolved-config values; status vocabulary + fail-closed apparatus checks; generalized calibration + cache; twelve rehearsal cases; transactional JSON+sidecar publication; Commit A/B lifecycle) and the remainder of §8.10.8 (benchmark mode, metrics, routing, Rebecca ruling, screening-withdrawal) are byte-for-byte unchanged. No scientific bar, threshold, estimator, predicate, schema, seed rule, apparatus rule, calibration constant, cache rule, or sequencing rule was modified. The changelog's own attestation ("No law text, locked bar, estimator, predicate, schema, seed rule, apparatus rule, workload gate, or sequencing rule changed") is confirmed by the diff.

## 3. Workload clarification accurate (non-blocking fix) — PASS
§8.10.8 now reads: "9.6 million cell repetitions and, absent short-circuiting, 48 billion **valid** bootstrap replicates or up to 52.8 billion bootstrap **attempts** at the 5,500-attempt ceiling." Internally consistent and correct:
- 9.6M = 20 × 240 × 2,000 (exact). ✓
- 48B valid = 9.6M × `valid_replicates`(5,000). ✓
- 52.8B max attempted = 9.6M × `max_attempts`(5,500). ✓
The valid-vs-attempted distinction is now stated explicitly and consistently. The feasibility gate remains fail-closed (fixed benchmark + separate Rebecca ruling); the benchmark extrapolation remains wall-time-anchored, so the count is descriptive, not load-bearing.

## 4. No new issues introduced — PASS
- The corrected line numbers are cited consistently (L8=28, L14=42; the file-path reference for L8 is inherited by the L14 citation in the same Sources line — no ambiguity).
- The workload clarification retains its existing `[PROPOSED — workload accounting]` tag; no new `[PROPOSED]` values or mechanisms were added.
- The clarification does not contradict any other workload statement in the spec.
- No new P1–P5 issues: P1 (no reconstruction) — citations point to file+line, no text reconstructed; P2 (verbatim law text) — unchanged, no law text quoted or altered; P3 (source-class tags) — `[LAW-L8]`, `[LAW-L14]`, `[PROPOSED]` present; P4 (date/regime) — unchanged (2026-08-20, Regime B); P5 (no deviation) — no deviation introduced.

## 5. §5 P6 now passes — PASS
The law-line pointers now match the constitution (L8=28, L14=42). P6 (provenance citation check) is satisfied. The §5 first-checklist law-diff that produced the v2.5 BLOCK now passes.

## 6. Constraints preserved — PASS
- Candidate-blind (Ruling 9), O-15 (diagnostic-only), O-14 (no re-run-on-failure) respected; G2–G4 NOT frozen.
- 2,000-repetition screening authorization remains WITHDRAWN pending the feasibility benchmark, CRITIC review, and a separate Rebecca ruling.
- 10,000-repetition confirmation, sensitivity map, and misspecification stress rerun remain prohibited.
- TASK BUILDER remains unauthorized at this gate.
- The bootstrap lower-endpoint > 0 pass rule still does NOT replace the per-seed 0.2 bar; INSTRUMENT FAILURE remains apparatus-validity-only (no per-seed reclassification). False kills remain false kills — negatives are not renamed.
- No scoring, protected-seed exposure, G2–G4 ruling, merger, or bar change occurred or is authorized. All v2.5/v2.5.1 mechanics remain `[PROPOSED]`.

## Preserved evidence (carried forward from v2.5 review, re-confirmed unchanged)
All fifteen second-STOP determinism/feasibility gaps remain concretely closed. No implementer is left to invent a field, literal value, ordering, state transition, exception, seed identity, cache rule, or publication action. Exceptions and exit codes (20/21/22/23/1) all named. The diff is spec-only (markdown); no `src/`, `runs/`, `state/STATE.md`, scoring artifacts, or seed manifests touched.

## Exact next authorized role
**WORKFLOW COORDINATOR** — on CLEAR, route the v2.5/v2.5.1 design to **Rebecca** for the feasibility-gate decision (Commit A + fixed benchmark first; then full screen / amended-reduced design / stop). TASK BUILDER is authorized only after Rebecca approves Commit A + benchmark.

## Explicitly prohibited actions
- No implementation, benchmark, or Commit A before Rebecca approval.
- No 2,000-repetition screening without the later, separate Rebecca ruling.
- No 10,000-repetition confirmation, sensitivity map, or misspecification stress rerun.
- No scoring, protected-seed exposure, G2–G4 freeze/ruling, merger, or bar change.
- No L15/L16/L17 before M5. No reconstruction of constitutional text (P1). No silent bar replacement.
- CRITIC did not modify the spec, code, constitution, or any artifact under review (read-only + this review file only); no merge to main.

## Confirmation
No scoring, rerun-on-failure, hold-out/protected-seed exposure, or unauthorized merge occurred during this re-review. CRITIC performed read-only checkout/diff/grep only; no implementation, benchmark, screening, simulation, artifact generation (other than this review file), seed access, or merge was performed or authorized. O-14 and O-15 respected. Rebecca remains sole gate and merge authority.

## Public-safety scan attestation (pre-push, this review file)
Before pushing this review file to `critic/l8-g2g4-v2.5.1-rereview`, CRITIC performed a regex plus manual self-scan of the file content for prohibited categories: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, PII, and protected-seed identities. The only pattern matches were legitimate public commit SHAs and policy category-label words used within this attestation sentence itself — no actual secrets, PII, private paths, or protected-seed identities are present. **Zero prohibited findings.** The file contains only spec-analysis content, public commit SHAs, constitution line numbers, and findings, all of which already exist in the public repository. Scan method: regex + manual review of this self-authored text file (gitleaks was not separately invoked for this review artifact; the content is plain markdown authored solely by CRITIC). No push to `main` occurred or is authorized; only a feature-branch push of this review artifact.
