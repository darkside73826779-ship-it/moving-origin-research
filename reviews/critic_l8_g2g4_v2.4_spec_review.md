# CRITIC Spec Review — L8 Instantiation Spec v2.4 (Deterministic Diagnostic Contract)

**Gate served:** CRITIC spec review of the v2.4 amendment — does §8.9 close every TASK BUILDER STOP item, is every mechanism deterministic, are the bars and constraints preserved?
**Reviewer:** CRITIC (fresh-context, focused spec review of the v2.4 §8.9 delta)
**Date:** 2026-08-20 00:07 EDT · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Verdict:** **CLEAR**
**Next recipient:** WORKFLOW COORDINATOR — on CLEAR, Rebecca approves → TASK BUILDER implements on `taskbuilder/l8-g2g4-diagnostic-remediation` → fresh-context CRITIC impl review → Rebecca.

---

## Inputs / SHAs reviewed

| Item | Value |
|---|---|
| Spec branch | `architect/l8-g2g4-remediation` |
| Amended HEAD (v2.4, under review) | `4463cbc` |
| Prior version (v2.3) | `2819bf7` |
| Delta reviewed | `2819bf7...4463cbc` — `06_l8_instantiation_spec.md` +103/−6; changelog +20; 2 handoff files |
| Spec | `reviews/l8_crossfamily_review/06_l8_instantiation_spec.md` (v2.4) |
| ARCHITECT review charge | `handoffs/ARCHITECT_L8_G2G4_V2_4_CRITIC_HANDOFF.md` |
| Superseded v2.3 TASK BUILDER handoff | `handoffs/ARCHITECT_L8_G2G4_REMEDIATION_TASKBUILDER_HANDOFF.md` (marked superseded) |
| M0 decision sheet (L8 bars) | `docs/rulings/M0_DECISION_SHEET.md` on main |
| Constitution v2 | `docs/ARCHITECTURAL_CONSTITUTION_v2.md` on main |
| Provenance log (Entries 11, 12, 43, 76, 81) | `docs/rulings/provenance_log.md` on main |
| §8 power analysis code (implementation baseline per §8.9.7) | `diagnostics/l8_power_analysis.py` at `b139749` on `taskbuilder/l8-power-analysis` |
| Calibration parallelism spec v1.2 (CalibrationWorkerError/CalibrationIdentityError contracts §8.9.5 references) | `specs/l8_calibration_parallelism_spec.md` at `6979378` |

Read-only review. No spec, code, constitution, or scoring artifact modified (read-only + own review/handoff files). No scoring, seed execution, hold-out seed exposure, 2,000-rep screening, 10,000-rep confirmation, or unauthorized merge performed.

---

## Headline finding (CLEAR)

§8.9 "Deterministic implementation contract (v2.4 STOP closure)" closes every TASK BUILDER STOP item. All seven subsections (§8.9.1–§8.9.7) are fully specified and deterministic — the TASK BUILDER has nothing to invent. The two critical distinctions the review charge flagged are explicitly preserved: (1) the bootstrap lower-bound > 0 predicate does NOT replace the per-seed 0.2 bar ("It does not require the lower endpoint to exceed 0.2; the locked 0.2 bar is applied per seed `[BAR-Entry 11]`"); (2) per-seed statistical failures are NOT INSTRUMENT FAILURE ("Failure to obtain 5,000 valid draws is an ordinary bootstrap-predicate failure, not INSTRUMENT FAILURE"). The locked bars (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity, 5 seeds) are preserved. Candidate-blindness, O-15, O-14, and the G2–G4 deferral are preserved. Every new value/mechanism is `[PROPOSED]` (cannot gate scoring unless Rebecca approves). P1–P6 satisfied. Scope is clean (spec + changelog + 2 handoffs only).

---

## §8.9 — all seven subsections close the STOP items (every mechanism deterministic)

### §8.9.1 Complete trend-verdict algorithms — VERIFIED deterministic

- **Spearman ρ:** Pearson correlation of midranks; dose ranks (1,2,3,4); ties receive arithmetic mean of occupied one-based ranks; ascending stable sort; binary64 equality defines a tie; covariance/variance with divisor 4 (cancels in correlation); zero rank-vector variance → ρ undefined → seed fails Spearman predicate. ✓ Fully specified.
- **Direction predicate:** unstandardized OLS slope `β_s > 0` for every seed; reported independently (even though `β*_s ≥ 0.2` implies it); no strict adjacent-increase predicate. ✓
- **Bootstrap:** `T = mean_s(β*_s)` across 5 seeds; each replicate resamples `N_w` window deviations **within every `(seed,dose)` stratum** (NOT seeds, NOT pooled across doses), preserving 5 seeds/4 doses/N_w per stratum; recompute D, σ_pool, β, β*, then T. ✓
- 5,000 valid replicates; two-sided 95% percentile interval; endpoints 0.025/0.975; NumPy linear quantile interpolation `h=(n−1)q` between floor(h)/ceil(h). ✓
- **Bootstrap predicate passes only when lower endpoint strictly > 0.** ✓ **Does NOT require lower endpoint to exceed 0.2; the locked 0.2 bar is applied per seed.** `[BAR-Entry 11]` ✓✓ (critical distinction preserved)
- Bootstrap RNG from §8.9.3 namespace `bootstrap`; undefined-β* draws discarded; max 5,500 attempted draws to obtain 5,000 valid; **failure to obtain 5,000 valid draws = ordinary bootstrap-predicate failure, NOT INSTRUMENT FAILURE.** ✓✓ (critical distinction preserved)
- Repetition enters denominator when all apparatus checks pass; undefined ρ/β* or invalid bootstrap sample = false kill (stays in denominator); apparatus-invalid repetitions excluded/counted/reported separately; any apparatus-invalid → combination apparatus-invalid → cannot qualify geometry. ✓
- **Overlapping marginal false-kill rates** (each predicate counts every repetition it fails, / same denominator) + bit-mask frequency table over all predicate-failure combinations; no exclusive "cause." ✓

### §8.9.2 Sweep operating points, aggregation, calibration, finalists — VERIFIED deterministic

- All 20 geometries (§8.2) × 240 cells (15 (α,v) × 16 (C_min,η)); no old reference/selected operating point substitutes. ✓ Preserves G4 deferral.
- Geometry primary = max cell-level Wilson upper; acceptance = conjunction all 240 upper < 0.10; preferred = conjunction all < 0.05; **no pooling/averaging for acceptance** (means/quantiles across cells = diagnostics only). ✓
- Wilson score interval z=1.959963984540054, n=apparatus-valid repetitions, standard closed form, zero failures same formula (no special case), n=0 → apparatus-invalid; cell-level only. ✓
- σ_dose calibration per (W,N_w,α,v) tuple; reference (0.7,0.1) for dose strength only (NOT acceptance); calibration RNG includes geometry; cached calibration only when full tuple + manifest digest match. ✓
- 2,000-rep screening; finalists = geometries satisfying <0.10 conjunction; restrict to smallest total queries per dose Q; ties retained for 10,000-rep confirmation; no geometry → STOP. ✓
- This cycle runs 20 screening geometries (2,000-rep); does NOT run 10,000-rep confirmation (requires screening artifact + fresh CRITIC + separate Rebecca auth); distinct from deferred stress rerun. ✓

### §8.9.3 Configuration, serialization, identity, seed manifests — VERIFIED deterministic

- `resolved_config.json` exact schema (required top-level fields; nested schemas exact; unknown fields fail). ✓
- Canonical JSON (UTF-8 NFC, sorted keys, no whitespace, separators `(',',':')`, finite numbers, trailing LF); SHA-256 over canonical bytes, lowercase hex. ✓
- Seed identity = `SHA256(namespace + "\n" + canonical_json(identity_object))`; RNG integer = first 8 digest bytes mod 2^63−1. ✓
- `seed_manifest.json` with synthetic diagnostic seeds labeled `synthetic_diagnostic_seed`; **candidate-blind, NOT protected scoring seeds; no scoring-seed manifest read/written.** ✓ (Ruling 9)

### §8.9.4 Output schemas and atomic publication — VERIFIED deterministic

- `battery_sweep.json` exact schema (geometry + cell fields; 240 ordered cells per geometry; `failure_mask_counts` over 4-bit strings 0000..1111 with bit order (spearman,beta_star,direction,bootstrap)). ✓
- Completeness predicates (exact schema; config digest; 20 geometries; 240 cells; 2,000 attempts; denominator + apparatus-invalid = attempts; Wilson recomputation within 1e-15; summaries recompute from cells; finalists recompute from rule; no unknown fields). ✓
- Atomic publication (write .tmp, flush, fsync, re-read validate, os.replace; failed publication preserves prior complete artifact + retains .failed.* file; sidecar only after JSON replacement; sidecar mismatch = incomplete, doesn't destroy last known-good pair). ✓ No partial artifact consumable as complete.

### §8.9.5 Production-path faults, exceptions, exits, recovery — VERIFIED deterministic

- `DiagnosticFaultHooks` (default no faults; test-injected; no CLI/env backdoors; named boundaries only: after_calibration, before_artifact_section, after_temp_write, before_parallel_collect, before_atomic_replace; test-only hooks under tests/, unreachable from production CLI). ✓
- Exit contracts: DiagnosticSchemaError=20, DiagnosticChecksumError=21, DiagnosticConfigMismatchError=22, DiagnosticNondeterminismError=23, CalibrationWorkerError/CalibrationIdentityError=1, unexpected=70. ✓
- Crash recovery candidate-blind synthetic only; **O-14 absolute for scoring**; fresh invocation validates frozen manifest, ignores .tmp/.failed.* as inputs, recomputes from repetition zero, no partial state resumed. ✓

### §8.9.6 Independent apparatus fixtures and rehearsal report — VERIFIED deterministic

- `known_answers_v1.json` (32 fixtures, oracle returns expected label, canonical SHA-256 `a38ba6a7...`). ✓
- Estimator fixtures (§2 positive + zero-slope, existing tolerances); config mismatch tests (mutate aggregation, W, N_w, doses, seed derivation, estimator version → DiagnosticConfigMismatchError). ✓
- Serial/parallel comparison (byte equality after removing elapsed_seconds; config digest equality; seed-manifest equality; checksum equality). ✓
- `diagnostic_rehearsal.json` (12 case_ids: incomplete_output, malformed_json, truncated_temp, serial_parallel, aggregation_mismatch, W_mismatch, N_w_mismatch, dose_grid_mismatch, seed_manifest_mismatch, estimator_version_mismatch, calibration_worker_crash, calibration_identity_crash). ✓ All 12 cases cover incomplete output, corruption, nondeterminism, configuration mismatch, and crash recovery.

### §8.9.7 Repository routing — VERIFIED deterministic

- TASK BUILDER creates `taskbuilder/l8-g2g4-diagnostic-remediation` from approved v2.4 SHA; imports `l8_power_analysis.py` from `b139749` as executable baseline; `6d455bb` read-only historical context, NOT copied forward; if source path/blob differs, STOP; TASK BUILDER changes only diagnostic code, tests/fixtures, `diagnostics/l8_g2g4/` artifacts; does not modify the ARCHITECT specification. ✓

**The TASK BUILDER has nothing to invent on any of the seven subsections.** ✓

---

## Hidden bar changes — VERIFIED preserved (CRITICAL)

The locked bars are preserved: ≥3 noise doses, Spearman ρ ≥ 0.8, standardized slope ≥ 0.2, specificity mandatory, 5 seeds. `[BAR-Entry 11]` `[BAR-Entry 11.3]` Verified against `docs/rulings/M0_DECISION_SHEET.md` (L8 row: "≥3 noise doses; Spearman ρ ≥ 0.8 monotonic; standardized slope ≥ 0.2; specificity control mandatory; Seeds: 5").

**The bootstrap lower-bound > 0 does NOT replace the per-seed 0.2 bar.** §8.9.1 is explicit: "The bootstrap predicate passes only when the lower endpoint is strictly greater than zero. It does not require the lower endpoint to exceed 0.2; the locked 0.2 bar is applied per seed. `[BAR-Entry 11]`" The bootstrap predicate (lower bound > 0) is an additional conjunction predicate over the pooled T statistic; the locked 0.2 bar remains per-seed. The 0.2 bar is NOT weakened. ✓

---

## INSTRUMENT FAILURE — VERIFIED apparatus-validity-only (no per-seed reclassification)

INSTRUMENT FAILURE is defined exclusively through the six independent apparatus checks (`instrument_checks` ordered array: oracle_checksum, estimator_fixtures, rng_reproducibility, config_digest, artifact_integrity, dose_calibration). A per-seed statistical failure (undefined ρ, undefined β*, invalid/insufficient bootstrap sample) is an ordinary false-kill / predicate failure, NOT INSTRUMENT FAILURE. §8.9.1: "Failure to obtain 5,000 valid draws is an ordinary bootstrap-predicate failure, not INSTRUMENT FAILURE." Apparatus-invalid repetitions are excluded/counted/reported separately; any apparatus-invalid → combination apparatus-invalid → cannot qualify a geometry. No reclassification of per-seed statistical failures (no-relabeling rule preserved). ✓

---

## Constraints preserved — VERIFIED

- **Candidate-blind (Ruling 9):** seed manifest = candidate-blind synthetic diagnostic seeds labeled `synthetic_diagnostic_seed`; no protected scoring seeds; no scoring-seed manifest read/written. ✓
- **O-15 (diagnostic-only):** 2,000-rep screening, not scoring. ✓
- **O-14 (no re-run-on-failure):** crash recovery candidate-blind synthetic only; scoring runs absolute. ✓
- **G2–G4 NOT frozen:** no 10,000-rep confirmation this cycle; no stress rerun; no scoring; no seed exposure; no merger. ✓
- **No L15/L16/L17 before M5.** ✓
- The calibration algorithm, combo seeds, §2 XF-5 estimator, false-kill formulas, null control, sensitivity-map construction, selection rule, misspecified profiles, R8 guard, write-order fix, NF-IMPL-1/2/3, and calibration parallelism (BF-MP-1) unchanged unless v2.4 explicitly amends them. §8.9 references the existing CalibrationWorkerError/CalibrationIdentityError contracts (§8.9.5) and the §2 estimator (§8.9.6 fixtures) but does not amend them — it uses them. ✓

---

## Scope — VERIFIED, no scope creep

Diff `2819bf7...4463cbc` touches only `06_l8_instantiation_spec.md` (+103/−6), the changelog (+20), and the 2 handoff files. No code, constitution, STATE.md, provenance log, or artifact. The amendments are confined to the new §8.9 (with seven subsections), the G2 gate-row text, the §12 sequencing (reordered to put CRITIC review before Rebecca approval + TASK BUILDER), the title/status/date. v2.3 content outside these sections is byte-for-byte unchanged (including §1 law text).

---

## §5 P1–P6 compliance

- **P1 (repo-first, no reconstruction):** PASS — no law text reconstructed; §8.9 is new normative text, not law quotation.
- **P2 (verbatim law quotes):** PASS — the §1 L8/L14 law text is carried byte-for-byte from v2.2 (verified against the constitution in the v2.2 review; the v2.3→v2.4 diff did not touch §1).
- **P3 (source-class tags):** PASS — every new numeric criterion carries `[PROPOSED]`: z=1.959963984540054, 5,000 replicates, 5,500 max attempts, 95%/0.025/0.975, 2,000-rep screening, 0.10/0.05 thresholds, 1e-15, exit codes 20/21/22/23/1/70, 32 fixtures, 12 cases. The locked bars are `[BAR-Entry 11]`. All new mechanisms are `[PROPOSED — algorithm]`/`[PROPOSED — direction predicate]`/etc. Every new value/mechanism is `[PROPOSED]` and cannot gate scoring unless Rebecca approves. ✓
- **P4 (regime dating):** PASS — header states date 2026-08-20, Regime B, post-Entry 81.
- **P5 (deviation memorialization):** N/A — the spec deviates from no `[LAW]` text; it is a `[PROPOSED]` diagnostic contract offered for Rebecca's sign-off.
- **P6 (provenance citations):** PASS — `[BAR-Entry 11]` (M0 sheet L8 bars) verified; `[Entry 76]` (Ruling 9) verified; `[Entry 81]` (narrowed claim) verified; Entries 11/12/43 exist in the provenance log. ✓

---

## Design soundness (fresh-eyes) — SOUND

- The trend-verdict algorithms are fully specified (Spearman tie rule, OLS direction, bootstrap strata, denominators, overlapping failures, bit-mask table) — no implementation ambiguity. ✓
- The bootstrap lower-bound > 0 vs per-seed 0.2 bar distinction is correctly modeled as two separate predicates (pooled T conjunction + per-seed bar), preserving Entry 11.3 semantics without weakening the 0.2 bar. ✓
- The all-cell Wilson-acceptance rule (conjunction of 240 upper bounds < 0.10) is deterministic and avoids pooling/averaging for acceptance — the worst-cell governs. ✓
- The config/serialization/identity/seed-derivation is fully specified (canonical JSON, SHA-256, deterministic seed derivation mod 2^63−1) — reproducible and candidate-blind. ✓
- The atomic publication protocol (tmp + fsync + re-read + os.replace; .failed.* retention; sidecar-after-JSON) prevents partial artifacts from being consumed as complete. ✓
- The fault-injection/exit/recovery design (named boundaries only, no CLI/env backdoors, synthetic-only crash recovery) preserves O-14 for scoring while enabling deterministic testing. ✓
- The 12 rehearsal cases cover the full failure surface (incomplete output, corruption, nondeterminism, config mismatch, crash recovery). ✓
- The compute authorization boundary is explicit: 2,000-rep screening only this cycle; 10,000-rep confirmation deferred with separate Rebecca authorization. ✓
- **No design decision is left to the TASK BUILDER** — §8.9 fully specifies algorithms, schemas, exit codes, fixtures, rehearsal cases, and routing. ✓

---

## Non-blocking observations

- **NF-G2G4-1 (trivial — law text carry-forward):** the §1 L8/L14 law text is carried unchanged from v2.2/v2.3 (the v2.3→v2.4 diff did not touch §1). P2 is satisfied (byte-for-byte against the constitution, verified in the v2.2 review). No action required.
- **NF-G2G4-2 (trivial — §12 sequencing reorder):** the §12 sequencing was reordered to place fresh-context CRITIC review (step 2) before Rebecca approval + TASK BUILDER implementation (steps 3–4), matching the v2.4 status ("pending fresh-context CRITIC → Rebecca approval → TASK BUILDER"). This is a sound sequencing clarification, not a defect. No action required.

---

## Preserved evidence

The v2.3 spec content outside §8.9 / G2-row / §12 is byte-for-byte unchanged. The frozen L8 instantiation spec lineage (v2.2 `c7d7bed` → v2.3 `2819bf7` → v2.4 `4463cbc`) is preserved on the branch. The §8 power analysis code (`b139749`) and the calibration parallelism spec v1.2 (`6979378`) are referenced as implementation baselines/contracts, not modified. All prior CRITIC CLEARs (v2.2 spec `4ca797c`; calibration parallelism spec v1/v1.1/v1.2 `a087654`/`5a16485`/`e44d27b`; calibration parallelism implementation `4a26611`) and the BF-MP-1 BLOCK (`cade0c5`) remain valid. The amendment invalidates no prior evidence; it closes the TASK BUILDER STOP by fully specifying the deterministic diagnostic contract.

---

## Pre-push scan attestation

A pre-push self-scan was performed on this review artifact before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. The artifact contains only SHAs, branch names, line numbers, spec-structure descriptions, and review analysis. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

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

## Verdict and routing

**Verdict: CLEAR.** §8.9 closes every TASK BUILDER STOP item: all seven subsections are fully specified and deterministic — the TASK BUILDER has nothing to invent. The bootstrap lower-bound > 0 does NOT replace the per-seed 0.2 bar (explicit); per-seed statistical failures are NOT INSTRUMENT FAILURE (explicit). The locked bars (≥3 doses, ρ ≥ 0.8, slope ≥ 0.2, specificity, 5 seeds) are preserved. Candidate-blindness, O-15, O-14, and the G2–G4 deferral are preserved. Every new value/mechanism is `[PROPOSED]`. P1–P6 satisfied. Scope is clean. Two trivial non-blocking observations (law text carry-forward; §12 sequencing reorder) require no action.

**Next authorized role:** WORKFLOW COORDINATOR → **Rebecca** (approve the diagnostic method and authorize 2,000-rep screening) → **TASK BUILDER** (implement on `taskbuilder/l8-g2g4-diagnostic-remediation`: all-seeds estimand, battery sweep, failure-injection tests, diagnostic rehearsal; NOT final L8 scoring, NOT 10,000-rep confirmation, NOT the deferred map) → fresh-context **CRITIC** (implementation review: does the code match v2.4? does the 2,000-rep screening artifact + rehearsal pass?) → **Rebecca** (decide G2/G3). Scoring remains gated behind the five standing M4 gates (L3, FWFP, CRITIC, tolerance-calibration, courier). Nothing herein authorizes scoring.

On BLOCK (not the case), returns to ARCHITECT.

---

*This review was conducted read-only against the spec at `4463cbc` on `architect/l8-g2g4-remediation`. No scoring, rerun, hold-out seed exposure, 2,000-rep screening, 10,000-rep confirmation, or unauthorized merge occurred. Rebecca is sole gate and merge authority.*
