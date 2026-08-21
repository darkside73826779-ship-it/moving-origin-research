# L8 Native-CUDA Backend Adoption Specification v1

**Date:** 2026-08-21

**Regime:** B

**Status:** Prospective and inoperative `[PROPOSED]`; no consistency or adoption ruling

**Gate served:** Deterministic native-CUDA diagnostic-backend adoption design from committed feasibility evidence

**Base/evidence head:** `taskbuilder/l8-cuda-legacy-compat@8251d95b31107f4a710463fb0574b5bd33a44325`

Unless explicitly tagged otherwise, every new threshold, status, test criterion, interface, and execution rule in this specification is `[PROPOSED]` and cannot gate until Rebecca approves it.

## 1. Versioned-law compliance

The binding protocol is quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md:130-135`:

> - **P1 — Repo-first law.** No text is binding unless it is committed to the repo. If a role needs binding text it cannot find in the repo, it STOPS and escalates to the COORDINATOR. Reconstruction of constitutional text is forbidden — the constitution is published; reconstruction is unnecessary and therefore prohibited.
> - **P2 — Verbatim quotation.** Any artifact that operationalizes a law (spec, review, harness docstring) opens the relevant section with the law's verbatim text quoted from `docs/ARCHITECTURAL_CONSTITUTION.md` (v2 for Regime B semantics), cited by file and line. Paraphrase never substitutes for the quote.
> - **P3 — Source-class tags.** Every numeric threshold, kill condition, or test criterion carries an inline source tag, one of exactly four: `[LAW-Lx]` (in the constitution's text), `[BAR-Entry n]` (Rebecca-locked pre-registration), `[OP-Entry n]` (adopted operationalization), `[PROPOSED]` (requires Rebecca sign-off; may not gate anything until signed). A number without a tag is a review-blocking defect.
> - **P4 — Regime dating.** Every new artifact states its date and regime in its header. Acts are judged only against their own regime's text; later text is never applied backward.
> - **P5 — Deviation memorialization.** Any deviation from `[LAW]` text — however sensible, however disclosed — is inoperative for scoring until Rebecca has signed a waiver or amendment recorded in the v2 amendment log. Disclosure in a spec is necessary but not sufficient.
> - **P6 — Provenance citation check.** Any claim of the form "Entry n said X" must be verified against the entry's actual text before commit.

Relevant laws, quoted verbatim from `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28,54-55`:

> **L8 — Stakes coupling (from homeostatic RL + Damasio/Seth).** At least one homeostatic variable's regulation error must measurably increase when self-model calibration is degraded (and only then). *Test:* inject calibrated noise into the self-model; regulation error must rise dose-dependently. Stakes that don't respond to self-model quality are decorative and fail the law.

> **L18 — Contamination controls on every positive claim** (empty/permuted/shuffled → chance), oracle positive controls proving each metric can leave zero, frozen and naive baselines on every comparison, 3+ seeds.

> **L19 — Pre-registration.** Bars and kill conditions written before runs; a Critic role empowered to falsify; a Judge role forbidden to lower bars; negatives retained as findings.

This backend gate makes no positive scientific claim and does not replace L18. The beta-star `>=0.2`, rho `>=0.8`, at-least-three-dose, five-seed, and specificity requirements remain unchanged `[BAR-Entry 11]`. Existing negative labels and the 239/240 finding remain intact.

## 2. Authority, evidence, and present disposition

Committed inputs are `[PROPOSED]`:

- CPU oracle commit `6d455bb` and raw result digest `978f21c061dbee40fe3dd6d80f8b4c5abec3e13ea9babf4c361b6ba34b5e4b21`.
- Native prototype implementation `e5367fd4991713d20386619efc92afd3bd1cf76d`.
- 1,000-repetition evidence `e857908ceeaa25ebfff8351d8f34a3b99e9d8276`, raw digest `f0752bfbe95f195eb4a2b75fb4d0375fb169bf7591247a2299cfccd438adc65a`.
- 10,000-repetition evidence `9678713ef13af1d8746f9ecd9a04457a6461c270`, raw digest `032787bc6a1625ad86b63295a03980e88f982723115452f8080e6c0d606936e2`.
- Rebecca diagnostic authorization record and TASK BUILDER handoff at base head.

The existing evidence is feasibility evidence only. It predates the prospective consistency criteria below, so it cannot become qualifying adoption evidence retroactively `[LAW-L19]`. Its exact disposition is:

- aggregate operating-point selection matches at `(C_min=0.5,eta=0.2)` and all sixteen aggregate sensitivity cells are informative `[PROPOSED evidence description]`;
- individual region labels match for 239 of 240 cells `[PROPOSED evidence description]`;
- ordinal 47, `(alpha=0,v_mult=2,c_min=0.8,eta=0.2)`, is CPU `informative` with false-kill `0.4787` and native CUDA `abstention-escape` with false-kill `0.5009`, against the diagnostic region boundary `0.5` `[PROPOSED apparatus criterion]`;
- therefore the existing cell-region disposition is exactly `UNRESOLVED_BOUNDARY_CELL`; it is not an apparatus failure, is not erased, and is not a qualifying consistency result `[PROPOSED]`.

Rebecca must decide whether to authorize any future prospective adoption execution. This specification does not authorize it.

## 3. Backends and no-fallback rule

Backend identities are exactly `CPU_ORACLE`, `CUDA_TAPE_APPROVED_V1_5`, and `CUDA_NATIVE_PROPOSED_V1` `[PROPOSED]`. CPU oracle code/results remain preserved and are the comparison reference. “Reference/fallback” never means automatic execution fallback: after a native request begins, CUDA unavailability, dependency/device mismatch, crash, or statistical failure returns `INSTRUMENT_FAILURE` or `SCIENTIFIC_REGRESSION` as specified, with no CPU replacement and no retry `[PROPOSED]`.

A future authorized configuration may select `CPU_ORACLE` before RNG construction. That is a separately declared backend run, not fallback. Approved L8 v1.5's prohibitions on serial fallback, CPU fallback, native GPU calibration, torch-native RNG for its tape-backed execution, and failed-run replacement remain controlling for `CUDA_TAPE_APPROVED_V1_5` `[PROPOSED]`. This native proposal is a distinct diagnostic backend and cannot silently modify the approved v1.5 execution.

## 4. Native RNG identity and scheduling invariance

### 4.1 Frozen generator and dependency identity

Native execution requires CPython `3.11.9`, NumPy `1.26.4`, SciPy `1.13.1`, PyTorch `2.13.0+cu130`, bundled CUDA runtime `13.0`, and `rfc8785` `0.1.4` `[PROPOSED]`. Exact direct-wheel URLs, SHA-256 values, and PEP 610 source verification must be copied from the approved v1.5 dependency manifest during implementation; any absent/mismatched record fails before RNG construction `[PROPOSED]`.

The RNG is `torch.Generator(device="cuda")` using the pinned PyTorch CUDA Philox implementation `[PROPOSED]`. The implementation may use only public pinned behavior plus the exact `_standard_gamma` call already present in the committed prototype; because `_standard_gamma` is private, its code-object/module identity and a frozen output fixture are mandatory, and any library change is a new adoption gate `[PROPOSED]`.

### 4.2 Seed domain

For each controlling cell and backend arm, construct exactly this ASCII identity `[PROPOSED]`:

`l8-native-cuda-v1|alpha={alpha:.6f}|vmult={v_mult:.6f}|cmin={c_min:.6f}|eta={eta:.6f}|arm={arm}`

`arm` is exactly `combo` or `null_control`. Compute SHA-256, take digest bytes zero through seven, interpret unsigned little-endian, and bitwise-AND with `(2^63)-1`; the result is passed once to `manual_seed` `[PROPOSED]`. Six-decimal formatting, lowercase names, separators, field order, ASCII encoding, and namespace are digest input. Every 240-cell-by-two-arm identity and derived seed is checked for duplicate identity and seed collision before CUDA initialization; either collision is `INSTRUMENT_FAILURE` `[PROPOSED]`.

### 4.3 Fixed draw schedule

One new generator is created for each `(cell,arm)`. Cells execute in CPU-oracle result order, and arms execute `combo` then `null_control` `[PROPOSED]`. One cell/arm is evaluated as a single full tensor of exactly the authorized repetition count; it may not be partitioned, padded, fused with another identity, compiled into a graph, or interleaved `[PROPOSED]`.

Within each generator the loop is dose indices `0,1,2,3`, then window indices `0,1,2,3` `[PROPOSED]`. At each window, calls occur exactly: `_standard_gamma(BETA_A)`, `_standard_gamma(BETA_B)`, `torch.rand` for correctness, `torch.randn` for mirror noise, then—only for `combo` with dose greater than zero and positive sigma—`torch.randn` for dose noise `[PROPOSED]`. All draw tensors have shape `(repetitions,5,W)`, dtype binary64, and the configured CUDA device. `null_control` consumes no dose-noise draw. Changing shape, call order, call count, dtype, device, or conditional consumption changes the RNG contract and is STOP.

Execution uses one process, device ordinal zero, and the default CUDA stream with no concurrent cell/arm kernels `[PROPOSED]`. `torch.use_deterministic_algorithms(True)` is required; TF32 and reduced-precision reductions are disabled; float64 is required throughout `[PROPOSED]`. Completion scheduling may affect elapsed time only. The exact fixed call schedule and one-identity-at-a-time rule make scientific bytes independent of worker/completion scheduling because no scheduling choice can alter generator consumption `[PROPOSED]`.

## 5. Scientific evaluator preservation

Primitive distributions, clipping, alpha bias, coverage floor, controller update, beta-star estimator, arms, cell order, sigma values loaded from the CPU oracle, region classification, sensitivity aggregation, and selection rule remain those of the committed CPU oracle `[PROPOSED]`. CUDA does no calibration. CPU handles configuration, oracle loading/digest verification, launch, collection, comparison, schema validation, and publication only `[PROPOSED]`.

Coverage ordering is stable descending confidence with ascending zero-based query index for exact ties, matching approved v1.5 B11 `[PROPOSED]`. Dose summaries, beta-star, false-kill, any-seed false-kill, false-pass, mean/null beta-star, region, and selection fields are never rounded before comparison or canonicalization `[PROPOSED]`.

## 6. Prospective CPU-reference consistency contract

These criteria apply only to a new candidate-blind execution authorized after Rebecca approves them; they are not applied to the already observed evidence `[LAW-L19]`.

### 6.1 Workload and repeatability

CPU comparison data are loaded byte-for-byte from the frozen 10,000-repetition oracle; CPU is not rerun `[O-14]`. Native CUDA performs exactly 10,000 repetitions for every 240 cells and both arms, then repeats the complete native workload once in a fresh process with the identical validated configuration `[PROPOSED]`. Canonical scientific payloads must be byte-identical. No third run or failed-run replacement is permitted `[PROPOSED]`.

### 6.2 Required conclusion invariants and boundary rule

Both native runs must have zero independently proven apparatus failures; all 240 rows, identities, calibration values, and order must match the oracle; selected `(C_min,eta)` must match exactly; and all sixteen aggregate sensitivity-region labels must match exactly `[PROPOSED]`.

Each individual region must match except that a cell is `BOUNDARY_CONSISTENT` only when all of these conditions hold simultaneously `[PROPOSED]`: CPU and CUDA are on opposite sides of the same false-kill boundary `0.5`; both false-kill rates lie in the closed interval `[0.475,0.525]`; their absolute difference is `<=0.025`; false-pass differs by `<=0.005`; every underlying non-false-kill predicate truth value is identical; and neither label is an apparatus status. Every such cell remains listed by ordinal and values. More than one `BOUNDARY_CONSISTENT` cell in either native run is `SCIENTIFIC_REGRESSION_CELL_REGION` `[PROPOSED]`. This narrow rule does not rename the historic ordinal-47 finding or qualify the historic evidence.

### 6.3 One-sided regression limits

The CPU is a reference, not a target that CUDA must reproduce numerically. Improvements are allowed without an upper symmetric-distance penalty. For every cell, using unrounded values, CUDA regression relative to CPU must satisfy `[PROPOSED]`:

- `cuda_false_kill - cpu_false_kill <=0.0250`;
- `cuda_any_seed_false_kill - cpu_any_seed_false_kill <=0.0200`;
- `cuda_false_pass - cpu_false_pass <=0.0075`;
- `cpu_mean_beta_star - cuda_mean_beta_star <=0.0075`;
- `cuda_mean_null_beta_star - cpu_mean_null_beta_star <=0.0075`.

Across 240 cells, the mean of those same signed regression quantities must be `<=0.0050`, `<=0.0050`, `<=0.0025`, `<=0.0025`, and `<=0.0025`, respectively `[PROPOSED]`. A negative quantity is an improvement. No benefit on one metric offsets a regression beyond its own limit.

All limits must pass in both native runs. These are prospective backend-consistency criteria, not scientific bars and not permission to soften beta/rho predicates `[PROPOSED]`. The historic evidence remains non-qualifying regardless of how it would score under this later-written contract.

### 6.4 Verdicts

Top-level verdict is exactly one of `CPU_CONSISTENT_OR_BETTER_FOR_O15_NATIVE_DIAGNOSTICS`, `SCIENTIFIC_REGRESSION_CELL_REGION`, `SCIENTIFIC_REGRESSION_DISTRIBUTION`, or `INSTRUMENT_FAILURE` `[PROPOSED]`. Apparatus checks alone produce `INSTRUMENT_FAILURE`. Ordinary predicate/rate/region differences produce a regression verdict, never apparatus failure. Passing all criteria permits only a proposal to Rebecca; it does not itself adopt the backend.

## 7. Device and runtime identity

Configuration records exact PCI bus ID, CUDA device ordinal, GPU name, compute capability, total memory, driver version, CUDA runtime, PyTorch build/version, deterministic-algorithm flag, TF32 flags, and SHA-256 of sorted `pip freeze --all` plus every direct dependency's PEP 610 bytes `[PROPOSED]`. The qualifying device class is exact compute capability plus successful frozen fixtures; GPU marketing name is recorded but is not alone sufficient `[PROPOSED]`.

A different device, driver, runtime, PyTorch build, dependency digest, `_standard_gamma` identity, or deterministic flag is `DEPENDENCY_OR_DEVICE_MISMATCH` before RNG construction. Portability to another identity requires a new diagnostic gate; no compatible-range inference is allowed `[PROPOSED]`.

CuPy, NVRTC, custom extension compilers, and locally installed prototype helpers remain development-only and outside the adopted runtime `[PROPOSED]`. The qualifying implementation may not import, dynamically load, compile, or report them as dependencies. Their presence in the environment is irrelevant only if preflight proves they are neither imported nor loaded `[PROPOSED]`.

## 8. Schemas, failures, and publication

Configuration, result, backend request/response, mismatch fixture, and executability matrix are the committed `specs/data/l8_native_cuda_*_v1.json` artifacts plus sidecars `[PROPOSED]`. Unknown/duplicate fields, NaN/Infinity, noncanonical bytes, digest mismatch, dirty implementation tree, unapproved SHA, or missing artifact fails before RNG construction `[PROPOSED]`.

Failure stages are exactly `preflight,rng,evaluator,collector,comparison,repeat_custody,publisher`; message codes are exactly those in the result schema `[PROPOSED]`. Process/CUDA/dependency/publication faults abort without retry. Statistical difference completes both permitted native runs when apparatus remains valid, publishes the negative evidence, and returns the appropriate regression verdict `[PROPOSED]`.

JSON uses RFC 8785 canonical UTF-8 without BOM plus one LF. Sidecar is lowercase raw SHA-256, two spaces, basename, LF `[PROPOSED]`. Publication uses JSON temp write/fsync/validate, sidecar temp write/fsync, preservation of any prior valid pair, atomic replacements, and exact restoration plus `.incomplete` retention after interruption `[PROPOSED]`. The two run payload byte arrays remain in parent memory until the top-level pair validates.

Result path is `diagnostics/l8_native_cuda_adoption.json` and sidecar is `diagnostics/l8_native_cuda_adoption.json.sha256` `[PROPOSED]`. Existing prototype/evidence files are immutable inputs and never overwritten.

## 9. Performance acceptance

Performance is measured end-to-end from immediately before first cell launch through final row collection and CUDA synchronization, excluding preflight/oracle-file load and publication `[PROPOSED]`. The reference is committed parallel-CPU elapsed time `1357.6829717159271` seconds `[PROPOSED evidence]`; CPU is not rerun. Each complete native run must take at most `135.7682971715927` seconds, i.e. at least `10.0x` speedup `[PROPOSED]`. Both runs must pass; performance never overrides a scientific-consistency failure.

The observed 25.2627186000027-second prototype and 53.74255214622001x speedup are feasibility evidence only `[PROPOSED evidence description]`.

## 10. Backend-neutral M4 interface

The M4 harness requests a backend through `l8_native_cuda_backend_request_schema_v1.json` and receives `l8_native_cuda_backend_response_schema_v1.json` `[PROPOSED]`. Backend enum is exactly the three identities in §3. Request binds mode, implementation/config/dependency/device digests, CPU oracle digest, workload identity, arms, cell order, and output contract. Response returns measurement artifacts and backend status; M4 alone applies law/scoring verdicts `[PROPOSED]`.

`CUDA_NATIVE_PROPOSED_V1` is rejected for M4 unless: this adoption receives fresh-context CRITIC CLEAR and Rebecca approval; a final implementation SHA is independently reviewed; the Phase B reconciliation against `architect/m4-harness-contract` records exact field/function/digest compatibility; and Rebecca separately releases M4 implementation/use `[PROPOSED]`. Until then the interface returns `BACKEND_NOT_ADOPTED`. It is never a scoring dependency and never silently substitutes for `CUDA_TAPE_APPROVED_V1_5` or `CPU_ORACLE`.

The request chooses one backend before RNG construction. A backend failure is returned; the harness may not invoke another backend in the same work item. CPU oracle preservation therefore supplies reference and separately authorized availability, not automatic fallback `[PROPOSED]`.

## 11. Implementation, review, and rollback sequence

No implementation is released by this document. If Rebecca approves the design and separately authorizes implementation, order is `[PROPOSED]`: schemas/validators; frozen fixtures; identity/dependency preflight; RNG schedule; evaluator; comparison; repeat custody; publisher/recovery; M4 adapter; full tests; fresh-context CRITIC implementation review; Rebecca execution decision.

Every executability-matrix test must exist, collect once, and pass before any execution request. Required failures include seed/domain mutation, draw-order mutation, scheduling/concurrency attempt, device/dependency mismatch, CUDA unavailable, nonfinite apparatus, historic 239/240 fixture preservation, boundary-rule pass/fail edges, one-sided-regression failure, repeat mismatch, CPU-fallback attempt, CuPy/NVRTC import, schema drift, and interrupted publication `[PROPOSED]`.

Rollback is inverse commits only after ARCHITECT proposal, fresh-context CRITIC review, and Rebecca authorization `[PROPOSED]`. Evidence and negative results remain. Reset, force push, automatic retry, result deletion, fallback, or negative relabeling are prohibited.

## 12. Routing and STOP

This proposal routes ARCHITECT → fresh-context CRITIC → WORKFLOW COORDINATOR → Rebecca. After CRITIC return it stops at the Coordinator for Rebecca's decision. No further role receives it absent Rebecca's express ruling.

No implementation, execution, scoring, protected/hold-out/courier seed access, rerun, G2–G4 freeze, formal equivalence/adoption claim, M4 use, merge, RECORDER/INTEGRATOR/JUDGE routing, bar/control change, negative renaming, or L15/L16/L17 work before M5 is authorized.
