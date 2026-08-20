# CRITIC Handoff — Return to WORKFLOW COORDINATOR: L8 Spec v2.4 (Deterministic Diagnostic Contract) Review

**From:** CRITIC (fresh-context, focused spec review of the v2.4 §8.9 delta)
**To:** WORKFLOW COORDINATOR
**Date:** 2026-08-20 00:07 EDT
**Gate served:** CRITIC spec review of the v2.4 amendment — does §8.9 close every TASK BUILDER STOP item, is every mechanism deterministic, are the bars and constraints preserved?
**Verdict:** **CLEAR**
**Review artifact:** `reviews/critic_l8_g2g4_v2.4_spec_review.md` on `critic/l8-g2g4-v2.4-spec-review` (SHA below)

---

## Authorization context

The TASK BUILDER stopped on the v2.3 design (found the diagnostic contract under-specified), routing back to the ARCHITECT. The ARCHITECT resolved it with v2.4 "Define deterministic L8 diagnostic contract" (`4463cbc`), marking the v2.3 TASK BUILDER handoff superseded. This handoff returns the CRITIC's focused spec review of the v2.4 §8.9 delta.

---

## SHAs reviewed

| Item | Value |
|---|---|
| Spec branch | `architect/l8-g2g4-remediation` |
| Amended HEAD (v2.4, under review) | `4463cbc` |
| Prior version (v2.3) | `2819bf7` |
| Delta reviewed | `2819bf7...4463cbc` — `06_l8_instantiation_spec.md` +103/−6; changelog +20; 2 handoff files |
| M0 decision sheet (L8 bars) | `docs/rulings/M0_DECISION_SHEET.md` on main |
| Constitution v2 | `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on main |
| Provenance log (Entries 11, 12, 43, 76, 81) | `docs/rulings/provenance_log.md` on main |
| §8 power analysis code (implementation baseline per §8.9.7) | `diagnostics/l8_power_analysis.py` at `b139749` on `taskbuilder/l8-power-analysis` |
| Calibration parallelism spec v1.2 (CalibrationWorkerError/CalibrationIdentityError contracts §8.9.5 references) | `specs/l8_calibration_parallelism_spec.md` at `6979378` |

---

## Verdict: CLEAR

§8.9 "Deterministic implementation contract (v2.4 STOP closure)" closes every TASK BUILDER STOP item. All seven subsections (§8.9.1–§8.9.7) are fully specified and deterministic — the TASK BUILDER has nothing to invent. The two critical distinctions the review charge flagged are explicitly preserved: (1) the bootstrap lower-bound > 0 predicate does NOT replace the per-seed 0.2 bar; (2) per-seed statistical failures are NOT INSTRUMENT FAILURE. The locked bars are preserved. Candidate-blindness, O-15, O-14, and the G2–G4 deferral are preserved. Every new value/mechanism is `[PROPOSED]`. P1–P6 satisfied. Scope is clean.

---

## §8.9 — all seven subsections close the STOP items (every mechanism deterministic)

- **§8.9.1 Complete trend-verdict algorithms:** Spearman ρ (midrank Pearson, divisor 4, zero-variance → undefined → seed fails); OLS β_s > 0 direction (reported independently); bootstrap T=mean_s(β*_s), resample N_w window deviations within every (seed,dose) stratum (not seeds, not pooled across doses), 5,000 valid / 5,500 max attempts, two-sided 95% percentile interval, NumPy linear quantile interpolation; **lower endpoint strictly > 0 to pass (NOT > 0.2 — 0.2 bar is per-seed)**; overlapping marginal false-kill rates + bit-mask failure table (no exclusive "cause"). ✓
- **§8.9.2 Sweep, aggregation, calibration, finalists:** all 20 geometries × 240 cells; geometry primary = max cell-level Wilson upper; acceptance = conjunction all 240 upper < 0.10 (preferred < 0.05); Wilson z=1.959963984540054, standard closed form, n=0 → apparatus-invalid; per-(W,N_w,α,v) σ_dose calibration (reference (0.7,0.1) for dose strength only, not acceptance); 2,000-rep screening; finalists = <0.10 conjunction, smallest Q, ties for 10,000-rep confirmation; no geometry → STOP. ✓
- **§8.9.3 Config, serialization, identity, seed manifests:** `resolved_config.json` exact schema (unknown fields fail); canonical JSON (UTF-8 NFC, sorted keys, separators (',',':'), finite numbers, trailing LF); SHA-256 digests; seed identity = SHA256(namespace + "\n" + canonical_json(identity_object)), RNG integer = first 8 bytes mod 2^63−1; `seed_manifest.json` candidate-blind synthetic diagnostic seeds (NOT protected scoring seeds). ✓
- **§8.9.4 Output schemas and atomic publication:** `battery_sweep.json` exact schema (240 ordered cells, failure_mask_counts 0000..1111, bit order (spearman,beta_star,direction,bootstrap)); completeness predicates (Wilson recomputation within 1e-15, summaries recompute from cells, finalists recompute from rule); atomic publication (.tmp + fsync + re-read + os.replace; .failed.* retention; sidecar after JSON; sidecar mismatch = incomplete, doesn't destroy last known-good). ✓
- **§8.9.5 Faults, exceptions, exits, recovery:** `DiagnosticFaultHooks` (default no faults, test-injected, no CLI/env backdoors, 5 named boundaries); exit contracts (DiagnosticSchemaError=20, DiagnosticChecksumError=21, DiagnosticConfigMismatchError=22, DiagnosticNondeterminismError=23, CalibrationWorkerError/CalibrationIdentityError=1, unexpected=70); crash recovery candidate-blind synthetic only (O-14 absolute for scoring; fresh invocation ignores .tmp/.failed.*, recomputes from repetition zero). ✓
- **§8.9.6 Apparatus fixtures and rehearsal report:** `known_answers_v1.json` (32 fixtures, SHA-256 a38ba6a7...); estimator fixtures (§2 positive + zero-slope); config mismatch tests (mutate aggregation/W/N_w/doses/seed derivation/estimator version → DiagnosticConfigMismatchError); serial/parallel comparison (byte equality excluding elapsed_seconds, config digest, seed-manifest, checksum); `diagnostic_rehearsal.json` (12 case_ids: incomplete_output, malformed_json, truncated_temp, serial_parallel, aggregation_mismatch, W_mismatch, N_w_mismatch, dose_grid_mismatch, seed_manifest_mismatch, estimator_version_mismatch, calibration_worker_crash, calibration_identity_crash). ✓
- **§8.9.7 Repository routing:** TASK BUILDER creates `taskbuilder/l8-g2g4-diagnostic-remediation` from approved v2.4 SHA; imports `l8_power_analysis.py` from `b139749` as baseline; `6d455bb` read-only historical context, NOT copied forward; if source differs, STOP; changes only diagnostic code, tests/fixtures, `diagnostics/l8_g2g4/` artifacts. ✓

**The TASK BUILDER has nothing to invent on any of the seven subsections.**

---

## Hidden bar changes — VERIFIED preserved (CRITICAL)

Locked bars preserved: ≥3 noise doses, Spearman ρ ≥ 0.8, standardized slope ≥ 0.2, specificity mandatory, 5 seeds. `[BAR-Entry 11]` `[BAR-Entry 11.3]` Verified against `docs/rulings/M0_DECISION_SHEET.md` (L8 row).

**The bootstrap lower-bound > 0 does NOT replace the per-seed 0.2 bar.** §8.9.1 is explicit: "The bootstrap predicate passes only when the lower endpoint is strictly greater than zero. It does not require the lower endpoint to exceed 0.2; the locked 0.2 bar is applied per seed. `[BAR-Entry 11]`" The bootstrap predicate (lower bound > 0) is an additional conjunction predicate over the pooled T statistic; the locked 0.2 bar remains per-seed. The 0.2 bar is NOT weakened.

---

## INSTRUMENT FAILURE — VERIFIED apparatus-validity-only (no per-seed reclassification)

INSTRUMENT FAILURE is defined exclusively through the six independent apparatus checks (oracle_checksum, estimator_fixtures, rng_reproducibility, config_digest, artifact_integrity, dose_calibration). Per-seed statistical failures (undefined ρ, undefined β*, invalid/insufficient bootstrap sample) = ordinary false-kill / predicate failure, NOT INSTRUMENT FAILURE. §8.9.1: "Failure to obtain 5,000 valid draws is an ordinary bootstrap-predicate failure, not INSTRUMENT FAILURE." No reclassification (no-relabeling rule preserved).

---

## Constraints preserved — VERIFIED

- Candidate-blind (Ruling 9): seed manifest = synthetic diagnostic seeds, no protected seeds, no scoring-seed manifest. ✓
- O-15 (diagnostic-only): 2,000-rep screening, not scoring. ✓
- O-14 (no re-run-on-failure): crash recovery candidate-blind synthetic only; scoring absolute. ✓
- G2–G4 NOT frozen; no 10,000-rep confirmation; no stress rerun; no scoring; no seed exposure; no merger. ✓
- No L15/L16/L17 before M5. ✓
- Calibration algorithm, combo seeds, §2 XF-5 estimator, false-kill formulas, null control, sensitivity-map construction, selection rule, misspecified profiles, R8 guard, write-order fix, NF-IMPL-1/2/3, calibration parallelism (BF-MP-1) unchanged unless v2.4 explicitly amends (§8.9 references but does not amend them). ✓

---

## Scope — VERIFIED, no scope creep

Diff `2819bf7...4463cbc` touches only the spec (+103/−6), changelog (+20), and 2 handoff files. No code, constitution, STATE.md, provenance log, or artifact. Amendments confined to new §8.9 (seven subsections), G2 gate-row text, §12 sequencing (reordered: CRITIC review before Rebecca approval + TASK BUILDER), title/status/date. v2.3 content outside these sections byte-for-byte unchanged (including §1 law text).

---

## §5 P1–P6 compliance

- **P1:** PASS — no law text reconstructed; §8.9 is new normative text.
- **P2:** PASS — §1 L8/L14 law text carried byte-for-byte from v2.2 (verified against constitution in v2.2 review; v2.3→v2.4 diff did not touch §1).
- **P3:** PASS — every new numeric criterion carries `[PROPOSED]` (z, 5,000/5,500, 95%/0.025/0.975, 2,000-rep, 0.10/0.05, 1e-15, exit codes, 32 fixtures, 12 cases); locked bars `[BAR-Entry 11]`; all new mechanisms `[PROPOSED — algorithm]`/etc. Every new value/mechanism is `[PROPOSED]` (cannot gate scoring unless Rebecca approves).
- **P4:** PASS — date 2026-08-20, Regime B, post-Entry 81.
- **P5:** N/A — no deviation from `[LAW]` text (a `[PROPOSED]` diagnostic contract for Rebecca's sign-off).
- **P6:** PASS — `[BAR-Entry 11]` (M0 sheet L8 bars), `[Entry 76]` (Ruling 9), `[Entry 81]` (narrowed claim) verified; Entries 11/12/43 exist in the provenance log.

---

## Design soundness (fresh-eyes) — SOUND

Trend-verdict algorithms fully specified (Spearman tie rule, OLS direction, bootstrap strata, denominators, overlapping failures, bit-mask table) — no implementation ambiguity. Bootstrap lower-bound > 0 vs per-seed 0.2 bar correctly modeled as two separate predicates (pooled T conjunction + per-seed bar), preserving Entry 11.3 semantics without weakening 0.2. All-cell Wilson-acceptance rule (conjunction of 240 upper bounds < 0.10) is deterministic and avoids pooling/averaging for acceptance. Config/serialization/identity/seed-derivation fully specified (canonical JSON, SHA-256, deterministic mod 2^63−1) — reproducible and candidate-blind. Atomic publication prevents partial artifacts. Fault-injection/exit/recovery preserves O-14 for scoring. 12 rehearsal cases cover the full failure surface. Compute authorization boundary explicit (2,000-rep screening only; 10,000-rep deferred). **No design decision left to the TASK BUILDER.**

---

## Non-blocking findings

- **NF-G2G4-1 (trivial):** §1 L8/L14 law text carried unchanged from v2.2/v2.3 (diff didn't touch §1). P2 satisfied (byte-for-byte, verified in v2.2 review). No action.
- **NF-G2G4-2 (trivial):** §12 sequencing reordered to place CRITIC review (step 2) before Rebecca approval + TASK BUILDER (steps 3–4), matching the v2.4 status. Sound sequencing clarification, not a defect. No action.

---

## Preserved evidence

v2.3 spec content outside §8.9 / G2-row / §12 byte-for-byte unchanged. Frozen L8 instantiation spec lineage (v2.2 `c7d7bed` → v2.3 `2819bf7` → v2.4 `4463cbc`) preserved. §8 power analysis code (`b139749`) and calibration parallelism spec v1.2 (`6979378`) referenced as baselines/contracts, not modified. All prior CRITIC CLEARs (v2.2 `4ca797c`; calibration parallelism spec/implementation `a087654`/`5a16485`/`e44d27b`/`4a26611`) and BF-MP-1 BLOCK (`cade0c5`) remain valid. The amendment invalidates no prior evidence; it closes the TASK BUILDER STOP.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this handoff artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

## Explicitly prohibited actions (confirmed not performed)

- No modification of the spec, code, constitution, or any artifact (read-only + own review/handoff files).
- No merge to `main`. No merge of any kind.
- No implementation, compute, or 2,000-rep screening (deferred to TASK BUILDER after Rebecca approves).
- No 10,000-rep confirmation or stress rerun.
- No scoring, seed execution, or hold-out seed exposure.
- No L15/L16/L17 before M5.
- No reclassifying per-seed statistical failures as INSTRUMENT FAILURE.
- No G2–G4 ruling by the CRITIC (Rebecca sole gate authority).

---

## Next authorized role / routing

**Next recipient:** WORKFLOW COORDINATOR → **Rebecca** (approve the diagnostic method and authorize 2,000-rep screening) → **TASK BUILDER** (implement on `taskbuilder/l8-g2g4-diagnostic-remediation`: all-seeds estimand, battery sweep, failure-injection tests, diagnostic rehearsal; NOT final L8 scoring, NOT 10,000-rep confirmation, NOT the deferred map) → fresh-context **CRITIC** (implementation review: does the code match v2.4? does the 2,000-rep screening artifact + rehearsal pass?) → **Rebecca** (decide G2/G3). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On CLEAR (this case), Rebecca approves the diagnostic method. On BLOCK, returns to ARCHITECT.

---

*This handoff was produced read-only against the spec at `4463cbc` on `architect/l8-g2g4-remediation`. No scoring, rerun, hold-out seed exposure, 2,000-rep screening, 10,000-rep confirmation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
