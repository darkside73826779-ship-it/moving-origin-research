# CRITIC Review — L8 Instantiation Spec v2.6 (Commit Identity and Benchmark Contract)

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Reviewer:** Fresh-context CRITIC (independent, read-only)
**Gate served:** CRITIC review of the v2.6 amendment — parallel Commit A identity and feasibility-benchmark contract before implementation or compute.

## Inputs / SHAs reviewed
- **Prior version (v2.5.1):** `081df58131d880e2a1180ef508c35467415f07e4`
- **Result (v2.6):** `e2bd8242315cb3fee88fb2f8b98bdc77ccacf515` ("Specify parallel L8 feasibility benchmark") on `architect/l8-g2g4-remediation`
- **Delta reviewed:** `081df58...e2bd824` — `06_l8_instantiation_spec.md` (+86/−14); changelog (+17); 2 handoff files (one new, v2.5.1 handoff marked superseded)
- **Constitution (verification source):** `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on `main` — L8 at line 28, L14 at line 42 (confirmed; pointers not regressed)
- Files read (only those the handoff points to): the spec, its changelog, the v2.6 handoff, the superseded v2.5.1 handoff, the constitution.

## Verdict
**CLEAR** — the A1→A2→evidence lifecycle is genuinely non-self-referential and concretely specified; the parallel multiprocessing benchmark contract is deterministic and complete (no implementer invention required); the authorization boundary is fail-closed (full screening remains withdrawn); the delta is spec-only with no prohibited artifacts; §5 P1–P6 pass and the L8/L14 pointers have not regressed. Three non-blocking findings for editorial cleanup.

## 1. Non-self-referential commit lifecycle (§8.11.1) — PASS
The prior self-referential Commit A (code + frozen config in one commit, where the config could not reference its own not-yet-known SHA) is replaced by three stages:
- **A1 — implementation:** code, tests, fixtures only; no `resolved_config.json`, no generated evidence.
- **A2 — frozen configuration:** adds `resolved_config.json` + sidecar only; `implementation_sha` = A1's full SHA; `config_parent_sha` = A1's full SHA; `config_commit_sha` is explicitly NOT stored inside the config. No code/test/fixture change.
- **Commit B — evidence:** generated rehearsal/benchmark artifacts + handoff only; every artifact stores `implementation_sha=A1`, `config_digest` from A2, `config_source_sha=A2`. No implementation or configuration change.

Each stage references only prior, already-committed, stable SHAs (A2 references A1; evidence references A1 and A2), and the config omits its own commit SHA — so no artifact's claimed identity equals its own containing commit. File-class restrictions are concrete (A1 = code/tests/fixtures; A2 = config pair only; B = evidence/handoff only), with explicit invalidation: any implementation change after A1 or configuration change after A2 invalidates evidence and requires new staged commits, and CRITIC verifies `git diff A1..A2` and `git diff A2..B` contents. This resolves the prior self-reference defect.

## 2. Parallel multiprocessing benchmark contract (§8.11.2–§8.11.6) — PASS
- **Parallelism (§8.11.2):** `backend="multiprocessing.Pool"`, `start_method="spawn"`, `chunksize=1`, `worker_count=min(32, logical_cpu_count)` with `logical_cpu_count=os.cpu_count()` and null/<1 a configuration failure; frozen into `resolved_config.parallelism`. No serial benchmark is run. Two-run parallel repeatability: same fixture twice through the frozen path, byte-identical canonical results after removing only `elapsed_seconds`; rehearsal `case_id=parallel_repeatability`, inject reversal on the second run, asserts `byte_mismatch`/`seed_order_mismatch`, exit 23.
- **RNG (§8.11.3):** benchmark RNG namespace `feasibility-benchmark`; bootstrap streams add `run_mode:"feasibility-benchmark"`; calibration namespace `feasibility-calibration`. All seeds derived from canonical identity fields only — no process-global RNG, PID, wall-clock, worker index, or fork state.
- **Calibration (§8.11.3):** six full uncached calibrations (one per benchmark `(W,N_w,alpha,v_mult)`), timed separately; the six sigma values are used only by their matching cases and are NOT promoted as the 300-entry screening cache.
- **Measurement (§8.11.4):** parent wall = `time.perf_counter_ns()` around the batch; per-worker `process_cpu_ns = time.process_time_ns(end)−start`; `total_process_tree_cpu_ns = parent + sum(worker)`; no system-wide CPU. Peak memory = aggregate RSS sampled every 10 ms over parent + recursive live children, deduplicated by PID; `peak_aggregate_rss_bytes` = max sampled sum; failure to sample = `DiagnosticSchemaError` exit 20. `psutil_version` and platform recorded. Volatile measurement fields do not affect the determinism digest — only `elapsed_seconds` is excluded from repeatability, and pass criteria for timing/memory are positivity + formula recompute within 1e-12, not exact equality.
- **Extrapolation (§8.11.5):** `E=min(1, S/(P×B))` (E≤0 fails schema); `projected_screen_wall_seconds = (9,600,000 × s_max)/(P × E)` (conservative); central uses `s_mean`; calibration projection `(300 × max_calibration_service_seconds)/(P × E)`; total conservative = screening + calibration. No alternative extrapolation permitted.
- **Artifact (§8.11.6):** exact top-level schema `{schema_version, artifact_date, regime, design_sha, implementation_sha, config_source_sha, config_digest, estimator_version, status, parallelism, calibration_cases, benchmark_cases, measurements, extrapolations, prohibitions}`; `schema_version="l8-g2g4-feasibility-v1"`; `status` exactly `COMPLETE`/`ABORTED` (only `COMPLETE` promoted); six ordered calibration cases + six ordered benchmark cases; all PASS; parallel repeatability PASS; counts match frozen config; formulas recompute within 1e-12; timing/memory positive; unknown fields fail. Uses §8.9.3 canonical JSON, SHA-256 sidecar, and §8.10.6 transactional publication/restore.

## 3. Authorization boundary (§8.11.7, §8.10.8, §12) — PASS
Rebecca's approval of v2.6 authorizes A1/A2 implementation, tests, failure rehearsal, two parallel-repeatability fixture executions, six uncached calibrations, and the six-case parallel benchmark only. It does not authorize the 2,000-repetition screen, screening evidence, 10,000-rep confirmation, sensitivity/misspecification work, scoring, or protected seeds. Benchmark results return through fresh-context CRITIC to Rebecca for the separate workload ruling (full screen / amended-reduced / stop). §12 step 4 authorizes only the benchmark/rehearsal evidence commit; step 6's screening-evidence commit requires separate authorization. The 2,000-rep screen remains withdrawn. Fail-closed.

## 4. Spec-only delta; no prohibited artifacts — PASS
Diff touches only spec markdown (+86/−14), changelog (+17), and two handoff files (new v2.6 handoff; v2.5.1 handoff marked superseded). No `src/`, `runs/`, `state/STATE.md`, scoring artifacts, seed manifests, benchmark outputs, or calibration artifacts. The changelog attests no implementation/calibration/repeatability/benchmark/screening/scoring/seed-exposure/G2–G4/merge occurred; confirmed by the diff. O-14 (no re-run-on-failure) and O-15 (diagnostic-only) respected.

## 5. §5 Versioned-Law compliance — PASS
- P1 (no reconstruction): laws cited by file + line; L8/L14 quoted verbatim from the constitution, not reconstructed.
- P2 (verbatim law quotation): L8 and L14 are quoted verbatim (spec lines 14/16) and match the constitution (L8 at line 28, L14 at line 42) exactly.
- P3 (source-class tags): `[PROPOSED]`, `[LAW-L8]`, `[LAW-L14]`, `[BAR-Entry 11]`, `[BAR-Entry 11.3]`, `[Entry 81]`, `[Entry 76]`, `[Sol-XF-n]` present on relevant lines; all new v2.6 mechanics tagged `[PROPOSED]`.
- P4 (date/regime): 2026-08-20, Regime B, in spec header, changelog, handoff.
- P5 (no deviation): no deviation from law text introduced.
- P6 (provenance): Entry 81 and Entry 76 resolve to actual entries in `docs/rulings/provenance_log.md`.
- L8/L14 pointers (line 28 / line 42) have not regressed from v2.5.1.

## Non-blocking findings (editorial / clarity)
1. **Stale serial/parallel wording (§8.9.4).** §8.9.4 retains the pre-v2.6 sentence "Serial/parallel comparison canonicalizes complete small-fixture result objects after removing exactly the top-level `elapsed_seconds` field; byte equality, config digest equality, ordered seed-manifest equality, and checksum equality are required." This is superseded by the §8.10 broad supersession clause ("supersedes conflicting or incomplete text in §8.2 and §8.9") and by §8.11.2, and is not operative — but it was not cleaned up to match the serial→parallel-repeatability rename, which could confuse an implementer. Recommend updating the sentence to "parallel repeatability comparison" wording. Not blocking: the operative test (§8.9.4 test #3) and §8.11.2 are explicit and the authorization boundary is fail-closed.
2. **"Commit B" label overload.** §8.11.1 stage 3 labels the benchmark-evidence commit "Commit B" (authorized), while §8.10.8 and §8.11.7 refer to unauthorized "Commit B screening evidence." §12 step 4/6 disambiguates the intent (benchmark/rehearsal evidence commit vs screening-evidence commit). Not blocking: §8.11.1 restricts Commit B content to rehearsal/benchmark artifacts only, and screening evidence is explicitly unauthorized, so no authorization loophole exists. Recommend distinct labels (e.g., "Commit B (benchmark evidence)" vs "screening-evidence commit") for clarity.
3. **`logical_cpu_count` vs `worker_count` schema clarity (§8.11.2).** The frozen object uses `<resolved>` for both `logical_cpu_count` and `worker_count`. The operative rule is clear (`worker_count=min(32, os.cpu_count())`), but when `os.cpu_count() > 32`, the raw logical CPU count and the capped worker count differ. Recommend clarifying that `logical_cpu_count` records the raw `os.cpu_count()` and `worker_count` records the capped `min(32, …)` value. Not blocking: the operative rule is unambiguous and the value is frozen in `resolved_config`.

## Preserved evidence
The A1→A2→evidence lifecycle is concrete and non-self-referential; the benchmark contract specifies exact schemas, statuses, RNG namespaces, calibration timing, CPU/RSS measurement, extrapolation formulas, and validation rules — no implementer is left to invent a field, literal, ordering, state transition, exception, seed identity, or publication action. Exceptions and exit codes (20/21/22/23/1) all named. False kills remain false kills (negatives not renamed); INSTRUMENT FAILURE remains apparatus-validity-only. Full 2,000-repetition screening remains withdrawn pending benchmark evidence, CRITIC review, and a separate Rebecca ruling; 10,000-rep confirmation and sensitivity/misspecification rerun remain prohibited. No scoring, protected-seed exposure, G2–G4 freeze/ruling, merger, or bar change occurred or is authorized. All v2.6 mechanics remain `[PROPOSED]`.

## Exact next authorized role
**Rebecca** — for the feasibility-gate decision: approve Commit A1 implementation, Commit A2 frozen configuration, and the fixed parallel feasibility benchmark (§12 step 3). After approval, TASK BUILDER produces A1/A2, tests, failure rehearsal, parallel repeatability, and the six-case benchmark; fresh-context CRITIC reviews that evidence before Rebecca's separate workload ruling (full screen / amended-reduced / stop). TASK BUILDER is not authorized at this review gate.

## Explicitly prohibited actions
- No implementation, A1/A2, benchmark, calibration, screening, 10,000-rep confirmation, or sensitivity/misspecification run before Rebecca approval.
- No 2,000-repetition screen or screening-evidence commit without the separate Rebecca ruling.
- No scoring, protected-seed exposure, G2–G4 freeze/ruling, merger, or bar change.
- No L15/L16/L17 before M5. No reconstruction of constitutional text (P1). No silent bar replacement.
- CRITIC did not modify the spec, code, constitution, or any artifact under review (read-only + this review file only); no merge to main.

## Confirmation
No scoring, rerun-on-failure, hold-out/protected-seed exposure, or unauthorized merge occurred during this review. CRITIC performed read-only checkout/diff/grep only; no implementation, benchmark, screening, simulation, artifact generation (other than this review file), seed access, or merge was performed or authorized. O-14 and O-15 respected. Rebecca remains sole gate and merge authority.

## Public-safety scan attestation (pre-push, this review file)
Before pushing this review file to `critic/l8-g2g4-v2.6-review`, CRITIC performed a regex plus manual self-scan of the file content for prohibited categories: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, PII, and protected-seed identities. The only pattern matches were legitimate public commit SHAs and policy category-label words used within this attestation sentence itself — no actual secrets, PII, private paths, or protected-seed identities are present. **Zero prohibited findings.** The file contains only spec-analysis content, public commit SHAs, constitution line numbers, and findings, all of which already exist in the public repository. Scan method: regex + manual review of this self-authored text file (gitleaks was not separately invoked for this review artifact; the content is plain markdown authored solely by CRITIC). No push to `main` occurred or is authorized; only a feature-branch push of this review artifact.
