# L8 §8 Calibration Parallelism Specification v1.2 — Diagnostic Scheduling Optimization

**Component:** M4 / L8 §8 power analysis (`diagnostics/l8_power_analysis.py`)
**Author:** ARCHITECT
**Status:** DRAFT v1.2 — pending CRITIC re-review (failure-path determinism: sanitization, termination, identity-validation contract) → Rebecca re-approval → TASK BUILDER implementation → CRITIC code review → Rebecca authorization
**Date:** 2026-08-19 · **Regime:** B (post-Entry 81; constitution v1 + Amendments 1–2; §5 binding) (P4)
**Base code SHA:** `7e296ec` on `taskbuilder/l8-power-analysis` (functional multiprocessing remediation, BF-MP-1 remediation baseline per Coordinator handoff). This spec branches from `7e296ec`; it does not modify the frozen L8 instantiation spec v2.2 (`c7d7bed` on `architect/l8-instantiation-v2.2-fresh`, cited as input source only). `7e296ec` and `c7d7bed` are divergent; they are not merged to produce this spec.
**Sources:** `diagnostics/l8_power_analysis.py` at `7e296ec` `[Code-7e296ec]`; frozen L8 instantiation spec v2.2 at `c7d7bed` `[Spec-c7d7bed]`; CRITIC multiprocessing re-review at `cade0c5` `[Critic-cade0c5]`; constitution v2 §5 `docs/ARCHITECTURAL_CONSTITUTION_v2.md` `[Const-v2]`; Rebecca M3 GO ruling `docs/rulings/REBECCA_M3_GO.md` `[Ruling-M3-GO]`; Ruling 9 (candidate-blindness) Entry 76 `[Entry 76]`.
**Standing constraints inherited:** O-14 (no re-run-on-failure), O-15 (development diagnostic-only), §5 P1–P6, Ruling 9 (candidate-blindness). This spec authorizes a diagnostic scheduling optimization only. It does not authorize scoring, hold-out-seed exposure, or any change to a scientific result.

---

## §1 Purpose and scope

### 1.1 Problem

The §8 power analysis (`run_power_analysis` and `run_power_analysis_misspecified`) parallelizes the 240 parameter-combination simulations (BF-MP-1 remediation baseline at `7e296ec`, functional per Coordinator handoff). Before each 240-combo batch, however, each analysis computes 15 independent `(alpha, v_mult)` sigma-dose calibrations **serially** in a single process nested loop (`[Code-7e296ec]` lines 779–780 reference, 1129–1130 misspecified). The 15 calibrations are mutually independent and each is deterministic in its `(alpha, v_mult)` identity.

> **Non-normative diagnostic context (not a bar, not a target):** A local O-15 diagnostic at `workers=16` observed one Python process and low CPU utilization during the calibration phase, followed by a 16-worker burst during the 240-combo simulation, repeated per profile. The first profile's 240-combo batch completed at ~190.4 s elapsed including its serial calibration phase. This is a development diagnostic observation only. It is not scoring evidence, not a performance bar, and does not gate anything.

### 1.2 What this spec authorizes

This spec authorizes **changing only the scheduling of the 15 calibration calls from serial to parallel** within `diagnostics/l8_power_analysis.py`. It authorizes a new top-level calibration worker, a separate calibration pool lifecycle, focused multiprocessing tests, and O-15 diagnostic progress. Nothing else.

### 1.3 What this spec does NOT authorize (scope fence)

This spec must NOT be read to authorize modification of: the L8 instantiation spec v2.2, the constitution, STATE.md, the provenance log, `calibrate_sigma_dose` itself, `combo_seed`, any per-simulation RNG derivation, the §2 XF-5 estimator, the false-kill aggregations, the null-control calculation, the sensitivity-map construction, the deterministic selection rule, the misspecified profiles, the artifact schema or JSON write order, candidate-blindness, the R8 guard, the write-order fix, or the three NF-IMPL fixes. No locked bar, control, scoring logic, or scientific interpretation is changed.

---

## §2 Verbatim governance text (P2 — no reconstruction; quoted from repo)

This spec operationalizes no scientific law (L8/L14 are not re-operationalized here); it invokes the following governance constraints verbatim from their repo sources.

> **O-14 — no re-run-on-failure.** From `docs/rulings/REBECCA_M3_GO.md` line 73: "O-14 no re-run on failure;" and from `docs/rulings/REBECCA_M3_DELIVERY_RULING.md` line 14: "Neither set of seeds may ever be rerun (O-14)." This spec uses O-14 only in this standing no-rerun-on-failure sense; it does not operationalize the historical Entry 22 O-14 I3-tolerance ruling (±0.05, withdrawn). `[Ruling-M3-GO]` `[Ruling-M3-Delivery]`

> **O-15 — development diagnostic-only.** From `docs/rulings/REBECCA_M3_GO.md` line 74: "O-15 development runs are diagnostic-only;" and from `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.2 (TASK BUILDER): "Diagnostic runs stay O-15-labeled, development-pool-only." `[Ruling-M3-GO]` `[Const-v2]`

> **Ruling 9 — candidate-blind tolerance calibration.** From `docs/rulings/provenance_log.md` Entry 76, Ruling 9: "tolerance calibration is pre-registered, candidate-blind (the candidate's diagnostic-seed results 101-105 are NOT inputs; only oracle/synthetic-ground-truth is), oracle/synthetic-grounded, and frozen before scoring..." The calibration and simulation in this spec remain synthetic/oracle-only; no candidate output is an input. `[Entry 76]`

> **§5 P1 — Repo-first law.** From `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1 line 130: "No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden." `[Const-v2]`

> **§5 P3 — Source-class tags.** From `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5.1 line 132: "Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect." `[Const-v2]`

---

## §3 The calibration phase (non-normative description of current behavior)

For each analysis (reference and each misspecified profile), the current code at `7e296ec`:

1. Builds the 15-element calibration domain as the Cartesian product of the frozen `ALPHAS = [0.0, 0.02, 0.05, 0.1, 0.2]` `[PROPOSED — apparatus parameter, §8]` and `V_MULTS = [0.5, 1.0, 2.0]` `[PROPOSED — apparatus parameter, §8]` (5 × 3 = 15 identities).
2. Computes `calibrations[(alpha, v_mult)] = calibrate_sigma_dose(alpha, v_mult)` for each of the 15 identities **serially** in a nested loop (`[Code-7e296ec]` lines 779–780, 1129–1130).
3. Reuses each calibration result for all 16 `(C_min, eta)` cells beneath that `(alpha, v_mult)` identity when building the 240 simulation work items.
4. Opens a `multiprocessing.Pool(processes=n_workers)` and runs `pool.map(_worker_combo, work_items)` (and the null-control map) for the 240 combos.

`calibrate_sigma_dose(alpha, v_mult) -> float` is a pure, deterministic binary search seeded from `combo_seed(alpha, v_mult, CAL_REF_C_MIN, CAL_REF_ETA)`; its return value depends only on `(alpha, v_mult)`. Parallelizing its 15 invocations changes only scheduling, not values.

---

## §4 The 10 design decisions (normative)

### 4.1 Worker function and data contract

- A **top-level, picklable** worker function named **`_worker_calibration`** wraps `calibrate_sigma_dose`. (Name is fixed; the TASK BUILDER may not choose an alternative.)
- **Input record:** a tuple `(ordinal: int, alpha: float, v_mult: float)` where `ordinal` is the deterministic dispatch index over the canonical nested-loop order `(alpha in ALPHAS, v_mult in V_MULTS)`. The ordinal is a defensive identity field only; it does not feed any scientific computation.
- **Output (success):** a JSON-serializable dict with exact keys `ordinal`, `alpha`, `v_mult`, `sigma_dose`, carrying the same identity plus the calibrated `sigma_dose` float. No alternative output shape is permitted.
- **Exceptions (wrap-and-re-raise):** the worker is a thin wrapper. It MUST catch `Exception` (not `BaseException`) **only** around the call to `calibrate_sigma_dose(alpha, v_mult)` and **only** to raise a top-level, picklable **`CalibrationWorkerError`** carrying the failed task's identity and a fixed public-safe error descriptor (see §4.2.1; normative code in §4.2.1). The original exception's message, `repr`, traceback, `__cause__`, `__context__`, `args`, and object are **never** stored, serialized, logged, or attached. It MUST NOT swallow the exception, MUST NOT return a result on failure, MUST NOT return `sigma_dose`, MUST NOT convert the exception into a usable calibration result, and MUST NOT retry. The re-raised `CalibrationWorkerError` propagates through `pool.map` to the parent and is treated as a calibration failure (see §4.2).

### 4.2 Failure semantics

- **First-exception fail-closed.** The first worker exception terminates the diagnostic immediately. `pool.map` already propagates the first exception and discards not-yet-computed results; the implementation must rely on this and must not add retry logic.
- **No retry.** O-14 forbids re-run-on-failure. No calibration or simulation may be retried after a failure.
- **Discard completed results.** Already-completed calibration results are discarded; no partial calibration table may be constructed or used.
- **No simulation after calibration failure.** No simulation work item may be built or dispatched after a calibration failure.
- **Parent-owned failure boundary.** A single shared function `_run_calibration_phase(analysis_label: str, workers: int | None) -> dict` is the parent-owned failure boundary, used independently by the reference analysis and each misspecified-profile analysis. It builds the canonical ordered work list, opens the dedicated calibration pool, calls `pool.map(_worker_calibration, work_items)`, validates identities, catches `CalibrationWorkerError` and `CalibrationIdentityError`, emits the corresponding failure record, and raises `SystemExit(1)`; on full success it returns the calibrations table. Normative code in §4.2.2.
- **Exact logging sink.** Each failure record is emitted as exactly one JSON line to `sys.stderr` via `sys.stderr.write(json.dumps(record, sort_keys=True) + "\n"); sys.stderr.flush()`. No other sink, no stdout, no print, no traceback.
- **Termination mechanism.** Immediately after emitting the failure record, the parent raises `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]`. This is the sole non-zero termination mechanism; no alternate exit code, return, or exception is permitted.
- **Worker failure record (7 fields).** On a worker exception, the parent emits a record with exactly seven fields, sourced from the propagated `CalibrationWorkerError` (§4.2.1) plus `phase` and `analysis_label`: `{"phase": "calibration", "analysis_label": <reference|misspec:profile>, "ordinal": <int>, "alpha": <float>, "v_mult": <float>, "exception_type": <str>, "exception_message": <str>}`. The parent MUST NOT log `repr(error)`, `str(error)`, `error.__cause__`, `error.__context__`, traceback text, or the original exception object; it may read only the five named fields. Sanitized (no traceback, no remote-worker traceback, no private absolute paths, no hostnames/SIDs/PII), log-only, never written into the artifact JSON.

### 4.2.1 CalibrationWorkerError contract (exception identity channel)

- **Class.** A top-level, picklable exception class named **`CalibrationWorkerError`** (name fixed; the TASK BUILDER may not choose an alternative) is the sole channel by which a failed calibration task's identity reaches the parent. It is raised by `_worker_calibration` (§4.1) and caught by the parent (§4.2).
- **Constructor fields.** `CalibrationWorkerError(ordinal: int, alpha: float, v_mult: float, exception_type: str, exception_message: str)` — JSON-safe, sanitized fields only. `exception_type` is the original exception's class name (`type(original).__name__`); `exception_message` is always exactly the fixed string `"calibration worker failed"` and MUST NOT vary by platform, process, task, or underlying exception. The constructor MUST pass exactly these five fields to `Exception.__init__` so default pickling reconstructs the object with the required signature.
- **Original exception handling.** The worker catches `Exception` only (not `BaseException`). The original exception's message, `repr`, traceback, `__cause__`, `__context__`, `args`, and object are never stored, serialized, logged, or attached. The worker raises `CalibrationWorkerError(...) from None` to suppress explicit exception chaining.
- **Picklability.** The class and its fields MUST be picklable (Python multiprocessing serializes the exception object to propagate it from worker to parent). It MUST NOT carry non-picklable objects (e.g., numpy arrays, file handles, traceback objects).
- **Sanitization source.** The parent MUST build the §4.2 failure record from the `CalibrationWorkerError` fields only — never from `repr(e)`, `str(e.__cause__)`, or traceback text, because multiprocessing may attach remote-worker traceback text that can contain private paths or identifiers.
- **No inference by re-execution.** Identity is carried by the exception; the parent MUST NOT identify a failed task by re-running or probing work items (O-14).

Normative contract code (binding; the TASK BUILDER may not alter the field set, the fixed message, the `from None`, or the `Exception`-only catch):

```python
class CalibrationWorkerError(Exception):
    def __init__(self, ordinal, alpha, v_mult, exception_type,
                 exception_message="calibration worker failed"):
        self.ordinal = int(ordinal)
        self.alpha = float(alpha)
        self.v_mult = float(v_mult)
        self.exception_type = str(exception_type)
        self.exception_message = "calibration worker failed"
        super().__init__(ordinal, alpha, v_mult, self.exception_type,
                         self.exception_message)


def _worker_calibration(args):
    ordinal, alpha, v_mult = args
    try:
        sigma_dose = calibrate_sigma_dose(alpha, v_mult)
    except Exception as original_exception:
        raise CalibrationWorkerError(
            ordinal, alpha, v_mult,
            type(original_exception).__name__,
            "calibration worker failed",
        ) from None
    return {
        "ordinal": ordinal,
        "alpha": alpha,
        "v_mult": v_mult,
        "sigma_dose": sigma_dose,
    }
```

### 4.2.2 Identity-validation failure contract + parent boundary (normative)

- **Class.** A top-level, picklable exception class named **`CalibrationIdentityError`** (name fixed) is the sole contract by which an identity-validation failure surfaces. Raised by `_validate_calibration_identities`; caught by the parent (§4.2). It carries no raw returned records and no unexpected values.
- **Fixed message.** `"calibration identity validation failed"` — fixed public-safe message; MUST NOT vary and MUST NOT include raw returned records.
- **Identity failure record (7 fields).** `{"phase": "calibration", "analysis_label": <reference|misspec:profile>, "message": "calibration identity validation failed", "mismatch_kinds": <sorted list, a subset of ["duplicate","missing","unexpected"] in this fixed order>, "expected_count": <int>, "seen_count": <int>, "canonical_identities": <list-of-lists of [alpha, v_mult] in canonical nested-loop order>}`. `mismatch_kinds` is a sorted list (not a single value) because duplicate/missing/unexpected may co-occur; its element set and order are fixed as `["duplicate","missing","unexpected"]`. `seen_count` is the number of returned result records (NOT the number of unique identities) so duplicates are visible (e.g., 15 canonical + 1 duplicate → `seen_count` = 16).
- **Public-safety of canonical_identities.** `canonical_identities` are the frozen, already-published synthetic apparatus parameters `ALPHAS × V_MULTS` (`[PROPOSED — apparatus parameter, §8]`); they are not candidate output or private data (Ruling 9). Raw returned records and raw unexpected values are NOT logged.
- **Validation helper.** `_validate_calibration_identities(results, canonical_work_items) -> None` raises `CalibrationIdentityError` on any duplicate, missing, or unexpected identity; unit-testable in isolation. Malformed returned records (non-dict, missing `alpha`/`v_mult`, or non-canonical identity values) are treated as `unexpected` (caught via `TypeError`/`KeyError` around key extraction and skipped); raw returned records and raw unexpected values are never logged.
- **Parent boundary.** `_run_calibration_phase(analysis_label, workers) -> dict` wraps `pool.map` and validation in a try/except catching `(CalibrationWorkerError, CalibrationIdentityError)`, emits the corresponding failure record (one JSON line to stderr per §4.2), and raises `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]`. Returns the calibrations table only on full success. The reference analysis and each misspecified-profile analysis call this shared function; they do not implement their own failure handling.

Normative contract code (binding field set, fixed messages, `Exception`-only catches, `SystemExit(1)` termination, stderr JSON sink):

```python
import json, sys, os, multiprocessing

class CalibrationIdentityError(Exception):
    def __init__(self, mismatch_kinds, expected_count, seen_count,
                 canonical_identities,
                 message="calibration identity validation failed"):
        self.mismatch_kinds = list(mismatch_kinds)
        self.expected_count = int(expected_count)
        self.seen_count = int(seen_count)
        self.canonical_identities = [list(x) for x in canonical_identities]
        self.message = "calibration identity validation failed"
        super().__init__(self.mismatch_kinds, self.expected_count,
                         self.seen_count, self.canonical_identities,
                         self.message)


def _emit_calibration_failure(record):
    sys.stderr.write(json.dumps(record, sort_keys=True) + "\n")
    sys.stderr.flush()


def _validate_calibration_identities(results, canonical_work_items):
    canonical = {(a, v) for (_, a, v) in canonical_work_items}
    seen_keys = set()
    result_count = len(results)
    duplicate = missing = unexpected = False
    for r in results:
        try:
            key = (r["alpha"], r["v_mult"])
        except (TypeError, KeyError):
            unexpected = True
            continue
        if key in seen_keys:
            duplicate = True
        seen_keys.add(key)
        if key not in canonical:
            unexpected = True
    if seen_keys != canonical:
        missing = True
    kinds = [k for k, p in [("duplicate", duplicate),
                           ("missing", missing),
                           ("unexpected", unexpected)] if p]
    if kinds:
        canonical_identities = [[a, v] for (_, a, v) in canonical_work_items]
        raise CalibrationIdentityError(
            kinds, len(canonical), result_count, canonical_identities)


def _run_calibration_phase(analysis_label, workers):
    work_items = [(i, a, v)
                  for i, (a, v) in enumerate(
                      (a, v) for a in ALPHAS for v in V_MULTS)]
    n_workers = min(workers or os.cpu_count() or 1, len(work_items))
    try:
        with multiprocessing.Pool(processes=n_workers) as pool:
            results = pool.map(_worker_calibration, work_items)
        _validate_calibration_identities(results, work_items)
    except CalibrationWorkerError as e:
        _emit_calibration_failure({
            "phase": "calibration",
            "analysis_label": analysis_label,
            "ordinal": e.ordinal, "alpha": e.alpha, "v_mult": e.v_mult,
            "exception_type": e.exception_type,
            "exception_message": e.exception_message,
        })
        raise SystemExit(1)
    except CalibrationIdentityError as e:
        _emit_calibration_failure({
            "phase": "calibration",
            "analysis_label": analysis_label,
            "message": "calibration identity validation failed",
            "mismatch_kinds": e.mismatch_kinds,
            "expected_count": e.expected_count,
            "seen_count": e.seen_count,
            "canonical_identities": e.canonical_identities,
        })
        raise SystemExit(1)
    return {(r["alpha"], r["v_mult"]): r["sigma_dose"] for r in results}
```

### 4.2.3 Implementation trace for every failure path

A design decision is resolved only when implementation and test behavior are deterministic without the TASK BUILDER inferring a rule. The v1.2 spec satisfies this trace for every failure path:

| Path | Input identity available at | Object crossing process boundary | Picklable under spawn | Exact text reaching logs | Parent exception/exit | Partial results to simulation? | Unit-test assertion contract |
|---|---|---|---|---|---|---|---|
| Worker exception | `_worker_calibration` scope (`ordinal`, `alpha`, `v_mult` from `args`) | `CalibrationWorkerError(ordinal, alpha, v_mult, exception_type, exception_message)` | Yes — top-level class; fields int/float/str; `from None` suppresses chaining; default pickling reconstructs via 5-arg constructor | Exactly `exception_type` (= original class name) and `exception_message` (= `"calibration worker failed"`); never repr/traceback/cause/context/args | Catches `CalibrationWorkerError`, emits 7-field JSON line to stderr, raises `SystemExit(1)` | No — `pool.map` raises before returning results; `SystemExit(1)` before table built | Assert `SystemExit(1)`; assert stderr has exactly one 7-field JSON line with `exception_message == "calibration worker failed"`; assert original message absent from pickled exception, log, and record |
| Identity validation (duplicate/missing/unexpected) | `_validate_calibration_identities` scope (`results` from `pool.map`, `canonical_work_items`) | Success result dicts `{ordinal, alpha, v_mult, sigma_dose}` (all JSON-safe) | Yes — plain dict of JSON-safe scalars | Exactly `"calibration identity validation failed"`, `mismatch_kinds` (sorted subset of `[duplicate,missing,unexpected]`), `expected_count`, `seen_count`, `canonical_identities`; never raw returned records or unexpected values | Catches `CalibrationIdentityError`, emits 7-field JSON line to stderr, raises `SystemExit(1)` | No — validation runs before the table is returned; `SystemExit(1)` before simulation work items built | Assert `_validate_calibration_identities` raises `CalibrationIdentityError` with correct `mismatch_kinds`; assert `_run_calibration_phase` emits the 7-field identity record and raises `SystemExit(1)` |
| Partial-result prevention | (structural — no failure path) | (n/a) | (n/a) | (none beyond the above records) | `SystemExit(1)` on any worker or identity failure | No — calibration table is returned only after `pool.map` succeeds AND identities validate; no simulation work item is constructed before the table returns | Assert no `_worker_combo`/`_worker_null_control` call occurs after a calibration failure |
| Termination | parent (`_run_calibration_phase`) | (n/a) | (n/a) | (the failure record line above) | `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]` | (n/a) | Assert exit status 1; assert no return value, no alternate exception, no stdout |

### 4.3 Pool lifecycle

- **Separate, sequential pools.** Each analysis opens a dedicated **calibration pool**, completes all 15 calibrations, and closes/joins it (context-managed: `with multiprocessing.Pool(...) as pool:`) **before** the simulation pool starts.
- **No nested pools — locked.** "No nested pools" is a **locked lifecycle requirement**, not an implementation detail. A calibration worker must never spawn its own pool; the simulation pool must not start until the calibration pool has exited. (The current code already uses per-call, non-nested pools; this spec preserves that property.)
- **One explicitly designed pool lifecycle per phase.** Calibration pool → close → build simulation work items → simulation pool → close. The TASK BUILDER may not introduce a single pool reused across both phases unless a future spec authorizes it.

### 4.4 Worker allocation

- **Cap.** `effective_calibration_workers = min(requested_workers, len(calibration_work_items))`, where `len(calibration_work_items) = |ALPHAS| × |V_MULTS| = 5 × 3 = 15`. The cap carries an inline source tag: `[PROPOSED — resource-hygiene implementation constraint; derived from frozen ALPHAS × V_MULTS]`.
- **Classification — resource hygiene, not a scientific bar.** This cap is resource hygiene derived from the **frozen, already-tagged** calibration-domain cardinality (`ALPHAS` and `V_MULTS` each carry `[PROPOSED — apparatus parameter, §8]` at `[Code-7e296ec]` lines 138–139). It is not a new scientific threshold, kill condition, or performance bar. It is tagged `[PROPOSED — resource-hygiene implementation constraint; derived from frozen ALPHAS × V_MULTS]` for provenance and Rebecca's awareness/sign-off; it may not gate any scientific result. The "15" is a count of frozen parameters, not a new bar value.

### 4.5 Reference / stress (misspecified) reuse

- **No cross-profile caching.** The reference analysis and each misspecified-profile analysis must each independently construct its own calibration table by parallel invocation of `calibrate_sigma_dose` over the 15 identities — exactly as both do today (`[Code-7e296ec]` lines 779–780 and 1129–1130). Only the serial→parallel scheduling changes.
- **Rationale.** The misspecified analysis re-**invokes** `calibrate_sigma_dose` (reuses the function, not a cached table) to test whether the estimator is overfit to the reference profile (`[Code-7e296ec]` docstring lines 1111–1120). Caching the reference table into the misspecified analysis would change runtime behavior and is therefore **not authorized** by this spec. Cross-profile reuse is out of scope and would require a separate spec.

### 4.6 Result identity validation

- **Exact set equality.** After collection, the set of returned `(alpha, v_mult)` identities must equal the canonical 15-element domain exactly. A duplicate, missing, or unexpected identity is a fail-closed defect.
- **Fail closed before simulation.** Identity validation must complete (and pass) before any simulation work item is built or dispatched. No partial calibration table may feed simulation.
- **Order.** Collection uses order-preserving `pool.map`; results are keyed by exact `(alpha, v_mult)` identity. Ordering is defensive, not a scientific input.

### 4.7 Progress reporting

- **Separate O-15 calibration progress permitted.** A distinct calibration progress line (e.g., `[calibration] 15 identities on N workers...`) is permitted, modeled on the existing `[reference]` / `[misspec:profile]` progress lines.
- **Deterministic ordering preserved.** Progress must not drive result ordering. Results remain keyed by `(alpha, v_mult)` identity via order-preserving `pool.map`.
- **Diagnostic-only.** Progress goes to the O-15 diagnostic log (stderr/print) only. It must not be written into the artifact JSON schema.

### 4.8 Artifact compatibility

- **Byte-compatible schema.** The current artifact schema and JSON write order are preserved byte-for-byte. No new calibration-phase or simulation-phase subphase fields may be added to the result JSON.
- **`elapsed_seconds` unchanged.** The `header.elapsed_seconds` field remains the total run elapsed time (inherently non-reproducible). No per-phase timing field is added to the artifact.
- **Timing/progress in logs only.** Any calibration timing or progress lives in the O-15 diagnostic log, not in the serialized artifact.

### 4.9 Reproducibility comparison

The reproducibility standard requires **both** value equality and serialized byte identity, plus downstream scientific equality:

- **(a) Calibration value equality.** Exact Python `==` equality of all 15 `sigma_dose` values between `workers=1` and `workers=N`.
- **(b) Artifact byte identity.** Byte-identical serialized artifact output (`json.dump` with `_sanitize_nan`, `indent=2`, `allow_nan=False`) between `workers=1` and `workers=N`, excluding only `header.elapsed_seconds` (inherently non-deterministic).
- **(c) Downstream scientific equality.** Exact equality of: `mean_beta_star`, `std_beta_star`, `false_kill_rate`, `false_kill_rate_per_seed`, `false_pass_rate`, `n_valid`, `n_instrument_failures`, `n_instrument_failures_null`, `mean_beta_star_null`, `region`, `min_distance_to_boundaries`, all `sensitivity_map` cells, and the deterministic `selection` — between `workers=1` and `workers=N`.

The equality standard is exact (not approximate). Tolerance-based comparison is not permitted.

### 4.10 Performance verification

- **No numeric speedup or utilization bar.** This spec introduces **no** numeric speedup, utilization, or CPU performance threshold. No `[PROPOSED]` performance/speedup criterion is created. (The two tagged diagnostic implementation criteria in §4.4 and §4.10 — the worker-allocation cap and the process-observation check — are not performance bars and gate no scientific result.)
- **What is required.** (a) Demonstrated non-serial calibration execution on a multicore diagnostic run; (b) process observation confirming more than one worker is active during the calibration phase (e.g., >1 Python process observed during calibration on a multicore system) `[PROPOSED — diagnostic implementation check]`.
- **Classification.** This is a **diagnostic implementation check (O-15)**, not a performance threshold and not a scoring criterion. Failure of the process-observation check blocks implementation sign-off but is not a scientific result and not a bar.

---

## §5 Candidate redesign — adopted with modifications

The TASK BUILDER's candidate redesign (`[Handoff]` §"candidate redesign") is **adopted**, with the following modifications clarifying and hardening it. The redesign parallelizes independent work scheduling only; it does not change calibration mathematics, constants, RNG, thresholds, or scientific interpretation.

| # | TASK BUILDER proposal | Disposition |
|---|---|---|
| 1 | Build calibration work items in deterministic nested-loop order over `(alpha, v_mult)` | **Adopted.** Work items carry a deterministic `ordinal` (§4.1) for defensive identity validation. |
| 2 | Execute one `calibrate_sigma_dose(alpha, v_mult)` call per work item in a multiprocessing pool | **Adopted.** Worker is top-level picklable `_worker_calibration`; on failure it narrowly wraps the original exception and re-raises picklable `CalibrationWorkerError` carrying identity (§4.1, §4.2.1); no swallowing, no partial result (§4.2). |
| 3 | Each worker returns an immutable record containing `alpha`, `v_mult`, `sigma_dose` | **Adopted.** Record also carries `ordinal` (§4.1). |
| 4 | Collect with order-preserving `pool.map`; reconstruct lookup keyed by exact `(alpha, v_mult)` identity | **Adopted.** Plus mandatory exact-set-equality identity validation, fail-closed before simulation (§4.6). |
| 5 | Build 240 simulation work items only after every calibration completes successfully | **Adopted.** Plus: separate calibration pool closed/joined before simulation pool; no nested pools locked (§4.3); no simulation after calibration failure (§4.2). |
| 6 | Reuse the simulation worker-count policy: explicit `--workers N`, else `os.cpu_count() or 1` | **Adopted with clarification.** Calibration uses `effective_calibration_workers = min(requested_workers, len(calibration_work_items))` as resource hygiene (§4.4). |
| 7 | Avoid nested pools | **Adopted and locked** as a lifecycle requirement, not an implementation detail (§4.3). |
| 8 | Preserve deterministic failure behavior: no retry, no completion-order aggregation, no partial sensitivity-map from incomplete calibration | **Adopted.** Plus fail-closed identity validation (§4.6) and no cross-profile caching (§4.5). |

**Modifications beyond the proposal:** (i) input record carries `ordinal`; (ii) no nested pools is a locked requirement; (iii) worker-allocation cap classified as resource hygiene (no new tag); (iv) no cross-profile calibration caching; (v) artifact schema byte-compatible, no new subphase fields; (vi) reproducibility requires both sigma_dose exact equality and byte-identical artifact plus downstream scientific equality; (vii) no numeric performance bar.

---

## §6 Verification obligations

The TASK BUILDER's recommended verification list is **adopted** as the spec's binding test contract (deterministic failure-path tests + reproducibility/protected-logic/process-observation/no-scoring). All verification is O-15 diagnostic-only.

1. **`CalibrationWorkerError` pickle round-trip.** `CalibrationWorkerError` survives `pickle.dumps`/`pickle.loads` with all five fields identical (`ordinal`, `alpha`, `v_mult`, `exception_type`, `exception_message`).
2. **Worker failure identity.** A worker failure carries the correct `ordinal`, `alpha`, `v_mult`.
3. **`exception_type` correctness.** `exception_type` equals the original exception's class name (`type(original).__name__`).
4. **Fixed message under hostile input.** `exception_message` is exactly `"calibration worker failed"` even when the original message contains a private absolute path, hostname, SID, email address, token-shaped text, or newline.
5. **Original message absent.** The original message is absent from the pickled exception, the captured diagnostic log, and the failure record.
6. **Failure record shape.** The worker failure record contains exactly the seven approved fields and no traceback.
7. **Termination mechanism.** The parent terminates through `SystemExit(1)` `[PROPOSED — diagnostic termination mechanism]`.
8. **No simulation after failure.** No simulation worker (`_worker_combo`/`_worker_null_control`) is called after a calibration failure.
9. **Identity-validation contract.** Duplicate, missing, and unexpected calibration identities (including malformed returned records — non-dict, missing `alpha`/`v_mult`, or non-canonical values, treated as `unexpected`) fail through `CalibrationIdentityError` (correct `mismatch_kinds`, `expected_count`, `seen_count` = number of returned records, `canonical_identities`; fields preserved across `pickle.dumps`/`pickle.loads`), emitting the 7-field identity record and `SystemExit(1)`.
10. **Happy-path equality.** Happy-path serial and parallel calibration tables remain exactly identical: (a) `sigma_dose` exact `==` equality (§4.9a) AND (b) byte-identical serialized artifact excluding `elapsed_seconds` (§4.9b) AND (c) downstream scientific equality (§4.9c).
11. **Genuine single-vs-multi diagnostic.** A genuine single-vs-multi diagnostic using the actually consumed calibration table (not vacuous). The prior BF-MP-1 defect (worker outputs discarded, making the reproducibility test vacuous) must not recur (`[Critic-cade0c5]`).
12. **Protected-logic static/diff check.** Static/diff confirmation that `calibrate_sigma_dose` itself and all protected scientific logic (estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, `combo_seed`, per-simulation RNG, candidate-blindness, R8 guard, write-order fix, three NF-IMPL fixes) remain unchanged.
13. **Process observation.** Confirmation that more than one worker is active during the calibration phase on a multicore system (§4.10).
14. **No scoring.** No full scoring run, no hold-out-seed exposure, no rerun-on-failure (O-14).

---

## §7 Constraints preserved (carry-forward)

This spec preserves, unchanged: the `calibrate_sigma_dose` numerical algorithm and return value; the 15-element calibration domain (frozen `ALPHAS` × `V_MULTS`); one calibration result per `(alpha, v_mult)` identity reused by all 16 `(C_min, eta)` cells; `combo_seed` and all per-simulation RNG derivations; the §2 XF-5 estimator; both false-kill aggregations (mean and per-seed); the null-control calculation; the sensitivity-map construction; the deterministic selection rule; the misspecified profiles; candidate-blindness (Ruling 9); O-15 diagnostic-only labeling; all fail-closed guards; the JSON write order and artifact schema; the R8 guard; the write-order fix; and the three NF-IMPL fixes. No locked bar, control, selection logic, or scoring logic is changed.

---

## §8 Compliance (§5 P1–P6)

- **P1 (repo-first, no reconstruction):** PASS. All governance text quoted verbatim from repo sources (§2). No law text reconstructed.
- **P2 (verbatim quotation):** PASS. O-14, O-15, Ruling 9, §5 P1, §5 P3 quoted verbatim with file/line citations (§2).
- **P3 (source-class tags):** PASS. This spec introduces **no new scientific apparatus parameters or performance bars**. All scientific counts are derived from the frozen, already-tagged `ALPHAS` × `V_MULTS` calibration domain (`[PROPOSED — apparatus parameter, §8]`). Diagnostic implementation criteria are tagged: the worker-allocation cap `min(requested_workers, 15)` `[PROPOSED — resource-hygiene implementation constraint; derived from frozen ALPHAS × V_MULTS]` (§4.4); the process-observation check `[PROPOSED — diagnostic implementation check]` (§4.10); and the `SystemExit(1)` termination mechanism `[PROPOSED — diagnostic termination mechanism]` (§4.2). The `expected_count` / `seen_count` identity-record fields are diagnostic record fields derived from the frozen calibration domain, not thresholds or bars. None of these gates a scientific result; all are offered for Rebecca's sign-off. No numeric performance/speedup bar is introduced.
- **P4 (regime dating):** PASS. Header states date 2026-08-19, Regime B, post-Entry 81.
- **P5 (deviation memorialization):** N/A. This spec deviates from no `[LAW]` text. It is a diagnostic scheduling optimization; it does not operationalize a scientific law or alter any locked bar.
- **P6 (provenance citations):** PASS. `[Entry 76]` (Ruling 9) cited consistent with the frozen L8 spec v2.2 (`c7d7bed`). O-14/O-15 cited from `docs/rulings/REBECCA_M3_GO.md` and `docs/rulings/REBECCA_M3_DELIVERY_RULING.md`.

---

## §9 Routing

**ARCHITECT** (this spec, draft v1.2) → **CRITIC** (design review: is the design sound? are all 10 decisions resolved? is every failure path deterministic? are constraints preserved?) → **Rebecca** (approve the spec) → **TASK BUILDER** (implement the approved spec, local frontier GPT) → **CRITIC** (code review: does the code match the approved spec? genuine reproducibility per §4.9/§6?) → **Rebecca** (authorize → rerun locally).

The CRITIC sees the spec first (design review), then the finished implementation (code review) — two passes on different artifacts, no double-dipping.

---

## §10 Explicitly prohibited (pending spec approval and after)

- No implementation of calibration parallelism until this spec is approved by Rebecca.
- No merge to `main`.
- No scoring, seed execution, or hold-out-seed exposure.
- No rerun of seeds 201–203 / 301–303 (O-14).
- No candidate output as input (Ruling 9).
- No L15/L16/L17 before M5.
- No changes to: the L8 instantiation spec, the constitution, STATE.md, the provenance log, `calibrate_sigma_dose`, `combo_seed`, per-simulation RNG, the estimator, false-kill formulas, null control, sensitivity map, selection rule, misspecified profiles, the artifact schema, JSON write order, candidate-blindness, the R8 guard, the write-order fix, the three NF-IMPL fixes, or any locked bar, control, or scoring logic.
- No numeric speedup or utilization bar (§4.10). The only new `[PROPOSED]` items are diagnostic implementation criteria (the worker-allocation cap, the process-observation check, and the `SystemExit(1)` termination mechanism); none gates a scientific result. No new scientific apparatus parameter is introduced by this spec.

---

*This spec authorizes a diagnostic scheduling optimization only. It does not change any scientific result, locked bar, or scoring logic. Rebecca is sole gate and merge authority.*
