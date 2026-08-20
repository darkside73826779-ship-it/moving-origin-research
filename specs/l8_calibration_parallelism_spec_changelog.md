# L8 §8 Calibration Parallelism Spec — Changelog

**Spec:** `specs/l8_calibration_parallelism_spec.md`
**Date:** 2026-08-19 · **Author:** ARCHITECT
**Branch:** `architect/l8-calibration-parallelism-spec` (from `7e296ec` on `taskbuilder/l8-power-analysis`)
**Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)

---

## v1 — Initial specification (2026-08-19)

**Base:** `7e296ec` (functional L8 multiprocessing remediation, BF-MP-1 remediation baseline per Coordinator handoff). The frozen L8 instantiation spec v2.2 (`c7d7bed`) is an input source only; `7e296ec` and `c7d7bed` are divergent and are not merged.

**Scope:** A standalone ARCHITECT specification for parallelizing the 15 independent `(alpha, v_mult)` sigma-dose calibrations in `diagnostics/l8_power_analysis.py` (`run_power_analysis` and `run_power_analysis_misspecified`). Scheduling optimization only — no scientific result, locked bar, control, scoring logic, or protected function is changed.

### What the spec defines

- Resolves all 10 TASK BUILDER design decisions (worker contract; failure semantics; pool lifecycle; worker allocation; reference/stress reuse; result identity validation; progress reporting; artifact compatibility; reproducibility comparison; performance verification).
- Adopts the TASK BUILDER's candidate redesign with modifications (ordinal in input record; no-nested-pools locked as a lifecycle requirement; worker-allocation cap classified as resource hygiene, not a bar; no cross-profile calibration caching; byte-compatible artifact schema with no new subphase fields; reproducibility requires both sigma_dose exact equality and byte-identical artifact plus downstream scientific equality; no numeric performance bar).
- Adopts the TASK BUILDER's verification obligations with the reproducibility standard sharpened (genuine single-vs-multi diagnostic; both value equality and byte identity; downstream scientific equality; process observation; no scoring).

### New parameters introduced

No new scientific apparatus parameters or performance bars. Two diagnostic implementation criteria are introduced and tagged: the worker-allocation cap `min(requested_workers, 15)` `[PROPOSED — resource-hygiene implementation constraint; derived from frozen ALPHAS × V_MULTS]` (§4.4) and the process-observation check `[PROPOSED — diagnostic implementation check]` (§4.10). Neither gates a scientific result; both are offered for Rebecca's sign-off. No numeric speedup/utilization bar is introduced.

### Constraints preserved

The `calibrate_sigma_dose` algorithm and return value; the 15-element calibration domain; one calibration result per `(alpha, v_mult)` identity; `combo_seed` and per-simulation RNG; the §2 XF-5 estimator; both false-kill aggregations; the null-control calculation; the sensitivity-map construction; the deterministic selection rule; the misspecified profiles; candidate-blindness (Ruling 9); O-15 diagnostic-only labeling; all fail-closed guards; the JSON write order and artifact schema; the R8 guard; the write-order fix; and the three NF-IMPL fixes. No locked bar, control, selection logic, or scoring logic changed.

### §5 P1–P6

- P1 (no reconstruction): PASS — governance text quoted verbatim from repo.
- P2 (verbatim quotation): PASS — O-14, O-15, Ruling 9, §5 P1, §5 P3 quoted with file/line citations.
- P3 (source-class tags): PASS — no new scientific apparatus parameters or performance bars; two diagnostic implementation criteria (worker-allocation cap, process-observation check) tagged `[PROPOSED — ...]`; neither gates a scientific result.
- P4 (regime dating): PASS — header states 2026-08-19, Regime B.
- P5 (deviation memorialization): N/A — no deviation from `[LAW]` text.
- P6 (provenance citations): PASS — `[Entry 76]` consistent with frozen L8 spec v2.2; O-14/O-15 cited from Rebecca rulings.

### Pre-push scan attestation

A pre-push self-scan was performed on the spec and changelog before commit. Scanned for: credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute paths, environment dumps, and PII. **Findings:** none. Content is specification text, verbatim governance quotes, code line/SHA citations, and source-class tags only. No private absolute paths, no secrets, no PII. Classified: acceptable. Reference: `PUBLIC_REPOSITORY_POLICY.md` §2/§3/§9.

---

*This spec is a diagnostic scheduling optimization. It changes no scientific result, locked bar, or scoring logic. Rebecca is sole gate and merge authority.*
