# CRITIC Review — L8 GPU Diagnostic-Backend Adoption Specification v1.1

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5 binding) `[P4]`

**Gate served:** Fresh-context CRITIC review of the ARCHITECT's L8 GPU diagnostic-backend adoption specification — Part A (law fidelity) + Part B (substantive falsification), including CPU↔GPU equivalence genuineness and equivalence to the amended (CPU) specification.

**Reviewer:** CRITIC (independent adversarial review; did not co-author, fix, or modify any artifact under review)

---

## 1. Verdicts

| Result | Value |
|---|---|
| `LAW_FIDELITY` | **PASS** |
| `SUBSTANTIVE` | **BLOCK** |
| **Combined CRITIC ruling** | **BLOCK** |
| Next authorized recipient | **ARCHITECT only** |

Per the routing handoff and specification §15, a combined `CLEAR` requires `LAW_FIDELITY: PASS` **and** `SUBSTANTIVE: CLEAR`. Part B blocks. The specification is **not** cleared and does **not** advance to Rebecca. TASK BUILDER is not released.

---

## 2. Inputs and SHAs reviewed

| Item | Value | Status |
|---|---|---|
| Named base (GitHub main) | `b6d4556` (PR #105 merged) | exists; **not an ancestor of the reviewed HEAD** — see B8 |
| ARCHITECT branch HEAD reviewed | `architect/l8-gpu-adoption-spec` @ `7c0a3c7` | reviewed |
| Actual merge-base with main | `f4e2231` (PR #101) | verified |
| Specification v1.1 | `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.1.md` (v1.1 commit `60a5acf`) | reviewed |
| Changelog | `specs/l8_gpu_diagnostic_backend_adoption_spec_CHANGELOG.md` | reviewed |
| Frozen-calibration artifact | `specs/data/l8_cpu_frozen_calibration_v1.json` | reviewed; fully verified |
| ARCHITECT's CRITIC handoff | `handoffs/ARCHITECT_L8_GPU_ADOPTION_CRITIC_HANDOFF.md` @ `7c0a3c7` | reviewed |
| Constitution | `docs/ARCHITECTURAL_CONSTITUTION_v2.md` | reviewed; byte-identical on `b6d4556` and `7c0a3c7` |
| Provenance log | `docs/rulings/provenance_log.md` | reviewed; byte-identical on `b6d4556` and `7c0a3c7` |
| M0 decision sheet | `docs/rulings/M0_DECISION_SHEET.md` | reviewed (L8 row) |
| Rebecca GPU rebuild ruling | `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` | read from `b6d4556`; **absent from the reviewed tree** |
| Rebecca Item-1 ρ authorization | `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` | present at `7c0a3c7`; **not merged to main** |
| Amended (CPU) specification | `architect/l8-g2g4-minimal-fullscreen` @ `2082680` | reviewed as the controlling comparator specification |
| CPU comparator implementation | `b139749:diagnostics/l8_power_analysis.py`, blob `b3d4b52c…` | verified identity; inspected |
| CPU evidence | `6d455bb:diagnostics/l8_power_analysis_results.json`, blob `ac691f74…` | verified identity; recomputed against |
| GPU evidence | `1bf7654:diagnostics/l8_gpu_full_comparison_results.json`, blob `4841deff…` | verified identity; recomputed against |
| ARCHITECT commits inspected individually | `1bf7654`, `60c4202`, `afc5492`, `8f945c7`, `60a5acf`, `7c0a3c7` | inspected against file contents, not commit messages |

All quantitative claims below were **recomputed independently** from the committed artifacts. No claim in this review rests on a commit message.

---

## 3. Part A — Law fidelity: `LAW_FIDELITY: PASS`

Part A was performed first and completed before any substantive assessment, per §15 and the routing handoff.

### 3.1 Law-diff (P1, P2) — PASS

Each quoted law block in the specification was extracted and compared character-for-character against the constitution file at `7c0a3c7`. No text was reconstructed from memory.

| Spec line | Law | Cited location | Verbatim match |
|---|---|---|---|
| 21 | L8 — Stakes coupling | `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` | **exact** |
| 25 | L18 — Contamination controls on every positive claim | `docs/ARCHITECTURAL_CONSTITUTION_v2.md:54` | **exact** |
| 29 | L19 — Pre-registration | `docs/ARCHITECTURAL_CONSTITUTION_v2.md:55` | **exact** |

Cited line numbers are correct as well as the text. The constitution file is byte-identical between `b6d4556` and `7c0a3c7`, so the diff is not sensitive to the base mismatch recorded in B8.

### 3.2 Source-class tags on thresholds, kill conditions, and test criteria (P3) — PASS

Every numeric threshold, kill condition, verdict value, and test criterion in the specification carries an allowed tag (`[LAW-Lx]`, `[BAR-Entry n]`, `[OP-Entry n]`, `[PROPOSED]`). Items checked included: the calibration digest and zero-difference rule (§4), the `beta_star >= 0.2` / `rho >= 0.8` predicate and the legacy/any-seed estimands (§5), the RNG modulus and namespaces (§6), the full grid and repetition counts (§7), familywise alpha `0.01`, the 1,440-endpoint family, `±0.04`, `0.01/6`, `±0.01`, `0.03`, `0.01` (§9), the `0.01` equivalence-set radius (§9.4), the retained `0.74999375` finding (§10), the six apparatus checks (§11), the twelve rehearsal cases (§12), and the adoption conjunction (§14). No untagged threshold was found. No `[PROPOSED]` item is presented as operative; §7 status and §14 correctly gate all of them behind Rebecca's signature.

Tag correctness was also checked, not merely tag presence:

- `beta_star >= 0.2` and `rho >= 0.8` tagged `[BAR-Entry 11]` — **correct**. Entry 11 §11.3 itself does not state these numbers, but the Entry 11 pre-registration was published as `docs/rulings/M0_DECISION_SHEET.md` (G0-4 ruling, PR #39), whose L8 row reads: "≥3 noise doses; Spearman ρ ≥ 0.8 monotonic; standardized slope ≥ 0.2 (ARCHITECT's candidate accepted); specificity control mandatory (self-irrelevant dose must NOT move regulation error). Seeds: 5." The `[BAR-Entry 11]` tag is the program's established, previously CRITIC-cleared attribution for these two bars (BF1 remediation, spec v1.4.1, commit `9dff1e5`). No bar is moved, raised, lowered, renamed, or reinterpreted anywhere in the specification.
- Five logical seeds tagged `[BAR-Entry 11]` — **correct** (Entry 11 §11.3, "Seeds raised to 5 for L7, L8, L15", LOCKED).
- O-14 / O-15 tagged `[OP-Entry 22]` — **correct**.
- D5 tagged `[OP-Entry 12]` — **correct**.
- L18 control enumeration tagged `[LAW-L18]` — **correct**.

### 3.3 Provenance-citation verification (P6) — PASS

Specification §2 asserts: "Entry 11.3 supplies the five-seed rule; Entry 22 supplies O-14/O-15; Entry 12 supplies D1–D5. No uncommitted ruling is used." Each was verified against the actual entry text in `docs/rulings/provenance_log.md`:

- **Entry 11.3** (line 181): "Seeds raised to 5 for L7, L8, L15, with the all-seeds-direction + bootstrap-CI fallback." — LOCKED. Supports the five-seed rule. **Verified.**
- **Entry 22 — O-15** (line 406 ff.): "Development runs (builder/Integrator sandbox, diagnostic only): PERMITTED and expected. Outputs are non-artifacts: never scored, never cited toward any invariant/bar/verdict, never logged as results." — **Verified**; supports §2, §3, §6, §14.
- **Entry 22 — O-14**: "Re-run-on-failure (Option iv) FORBIDDEN by name — result laundering, never to be proposed again." — **Verified**; supports §2, §10, §11, §14.
- **Entry 12 — D1–D5**, including D5: "no result is ever re-run, re-scored, or reframed to avoid a kill condition. Persistence is spent on new mechanisms, never on old numbers." — **Verified**; supports the §2 D5 citation.

No fabricated, mis-numbered, or overstated provenance citation was found. Part A therefore passes and substantive review was authorized to proceed.

Two Part A observations are recorded as **non-blocking** (NB6, NB7) because they concern completeness of inherited-bar enumeration and authority citation, not fidelity of quoted text, tags, or the three cited entries.

---

## 4. Part B — Substantive falsification: `SUBSTANTIVE: BLOCK`

The specification is internally consistent in its stated mechanisms. It is **not executable end-to-end**, and it does **not** preserve the controlling predicate semantics of the amended (CPU) specification. Internal consistency is not executability.

### Blocking findings

#### B1 — Spec defect (locked-bar comparison semantics omitted; silent bar movement risk)

The controlling amended CPU specification at `2082680:specs/l8_g2g4_minimal_full_screen_spec.md:125` locks the ρ predicate as:

> Predicate **passes** iff `ρ_s >= 0.8` **OR** `abs(ρ_s - 0.8) <= RHO_COMPARE_EPS` … `RHO_COMPARE_EPS = 1e-12`

and locks tie detection as exact finite binary64 equality, with a no-softening test asserting that `0.8 - 2·RHO_COMPARE_EPS` fails (spec §5.5 case 2a).

The GPU adoption specification v1.1 contains **zero** occurrences of `RHO_COMPARE_EPS`, zero occurrences of `undefined`, and no comparison-tolerance rule. Its §5 complete verdict is the bare conjunction `beta_star >= 0.2 AND rho >= 0.8`.

Consequence, independently traced: the controlling specification's own documented threshold case `D̄ = [1, 0, 2, 3]` computes `ρ_s = 0.7999999999999999` (the binary64 roundoff of exactly `0.8`) and **passes** on the CPU path via the eps tolerance. Implemented as written in the GPU specification, the same value **fails** on the GPU path. The already-committed GPU code confirms the bare form: `1bf7654:diagnostics/l8_gpu_proposal.py:146` computes `complete = ((beta>=.2)&(rho>=.8)).all(dim=1)`. The effect is an upward movement of the locked `0.8` bar on the GPU path only — a locked-bar change that the specification does not disclose and that §16 and Rebecca's Item-1 authorization both prohibit. It would also inject systematic CPU/GPU disagreement into the very complete-verdict endpoint that §9.1 gates on.

Additionally, §5's conjunction omits the `undefined ρ_s` disjunct that Rebecca's directive fixes verbatim: "Define the primary true-effect false-kill rate as: `P(any seed has β*_s < 0.2 OR undefined ρ_s OR ρ_s < 0.8)`", together with "Zero response-rank variance: ρ is undefined and counts as failure of the ρ predicate, not INSTRUMENT_FAILURE." The GPU specification never states the undefined-ρ disposition, while §11 check 5 routes nonfinite summaries toward `INSTRUMENT_FAILURE` and §8 requires JSON to reject NaN. A TASK BUILDER must therefore choose the undefined-ρ disposition, and one available choice is exactly the reclassification of a statistical failure as `INSTRUMENT_FAILURE` that Rebecca's authorization boundary explicitly forbids.

**Classification:** spec defect (locked-bar comparison semantics; equivalence-to-controlling-specification failure; unresolved TASK BUILDER discretion with a prohibited branch).

#### B2 — Spec defect (the designated CPU comparator cannot compute the compared endpoints)

§5 designates `b139749:diagnostics/l8_power_analysis.py` (blob `b3d4b52c…`) as **the** CPU comparator. §9.1 defines the primary family as six endpoints at each of 240 cells, including **mean rho**, **complete-verdict false-kill**, and **complete-verdict null false-pass**.

Independent inspection of that blob returns **zero** occurrences of `rho`, `spearman`, `midrank`, `complete_verdict`, or `any_seed`. It emits `mean_beta_star`, `std_beta_star`, `false_kill_rate`, `false_kill_rate_per_seed`, `false_pass_rate`, `mean_beta_star_null` — i.e. it can supply 3 of the 6 primary-family endpoints and **cannot** supply mean ρ, complete-verdict false-kill, or complete-verdict null false-pass.

This is not a new discovery of this review; it is the ARCHITECT's own STOP finding, recorded at `dc3185a` ("`b139749` does not compute per-seed Spearman ρ") and confirmed by Rebecca's Item-1 authorization ("The ARCHITECT's STOP was confirmed correct"). The GPU adoption specification nevertheless designates that same implementation as the comparator, requires ρ-bearing endpoints from it, defines no ρ computation of its own (no dose ranks `(1,2,3,4)`, no ascending midranks, no Pearson-on-ranks statement — `midrank` appears once, in passing, in §5), and cites no authorization to add one. The asymmetry is real, not hypothetical: the GPU side already has a `_rho` implementation (`l8_gpu_proposal.py:38`); the designated CPU side has none.

**Classification:** spec defect (construction; the pre-registered comparison cannot be executed against its own named comparator).

#### B3 — Spec defect (RNG logical-seed reduction guarantees duplicate seeds)

§6 forms a unique UTF-8 identity per (namespace, arm, profile, cell, repetition, seed index), SHA-256s it, then "reduce[s] modulo `2^31` to obtain `logical_seed`". §11 check 3 makes "RNG-identity uniqueness" an apparatus check and §12 case 8 makes "duplicate logical RNG identity → `INSTRUMENT_FAILURE`" a mandatory rehearsal.

Recomputed from §7: 240 cells × (10,000 + 10,000 + 2,000 + 2,000) repetitions × 5 seed indices = **28,800,000** identities per backend per namespace, mapped into a space of `2^31` = 2,147,483,648. Expected colliding pairs ≈ n²/(2m) ≈ **193,119**; P(no collision) ≈ `exp(-n²/2m)` ≈ 0. Duplicate `logical_seed` values are certain, not merely possible.

Both readings of the uniqueness check fail:

- If the check applies to the derived `logical_seed`, the run is guaranteed to terminate as `INSTRUMENT_FAILURE` by construction. The specification cannot be executed.
- If it applies only to the identity string, the check is satisfied trivially by construction and roughly 193,000 repetition-pairs silently share a generator seed and therefore reproduce identical draw streams — contradicting §6's own guarantee of "a separate generator stream for each logical seed" and understating endpoint variance in the intervals of §9.

The specification does not say which object the uniqueness check governs, so the TASK BUILDER must choose. The `2^31` reduction is also gratuitous: `torch.Generator.manual_seed` accepts a 64-bit seed, and the identity digest supplies ample width.

**Classification:** spec defect (executability and unresolved TASK BUILDER discretion; independently computed).

#### B4 — Spec defect (L18 parity fixtures do not exist and the specification mandates a STOP)

§12 requires, before the statistical comparison, that "the same committed CPU and GPU implementations must pass one deterministic backend-parity fixture for each L18 category: empty, permuted, shuffled, oracle, frozen, and naive", and adds: "Each fixture must preserve its existing CPU definition; if no committed CPU definition exists, TASK BUILDER must stop rather than invent one."

Independent inspection of the designated CPU comparator `b139749:diagnostics/l8_power_analysis.py` finds no such definitions. Word-boundary counts: `permuted` 0, `shuffled` 0, `naive` 0; `empty` appears twice, both as `np.empty` allocations; `oracle` appears only as task-profile language ("known oracle correctness", "oracle ground truth"); `frozen` appears only in "R* is frozen before any…". The implementation's actual arms are the reference (true-effect) arm, the null control, and two misspecified profiles (`uniform_difficulty`, `bimodal_difficulty`) — no L18 control battery. The M1 harness has such arms (`reviews/judge_m1_run1_ruling.md` records `arm_order = [empty, permuted, shuffled, oracle, naive, frozen]`), but that is a different instrument and is not the committed CPU definition for this L8 diagnostic path.

Under its own §12, the specification therefore mandates that the TASK BUILDER **stop** before the comparison can begin. A pre-registration whose first gate is an unsatisfiable precondition is not executable.

**Classification:** spec defect (executability; L18 fixture availability).

#### B5 — Spec defect (fixtures, artifact pairs, schemas, and expected digests deferred to the implementer)

§12 closes: "The rehearsal fixture and known-good JSON/sidecar pair must be committed before execution and reviewed by CRITIC. If their exact schema and digest are absent, execution is blocked." §13 opens: "TASK BUILDER must define and CRITIC must approve exact JSON Schemas for configuration, raw backend results, equivalence results, and failure rehearsal before any run."

The specification therefore names no rehearsal fixture (no `W`, `N_w`, nuisance/operating coordinates, calibration source, repetition count, RNG namespace, result schema and ordering, or expected canonical digest), no repository path or contents for the known-good JSON/sidecar pair, no sidecar filename convention, and no expected SHA-256 for any published artifact. Field order and canonicalization for the artifacts of §8 and §13 are likewise unfixed beyond a row-ordering sentence.

This is the exact defect class the binding executability standard was added to catch after the v2.6 false CLEAR: the TASK BUILDER would have to invent the fixture, the committed artifact pair, and the schemas. That is a BLOCK regardless of how internally consistent the stated mechanisms are.

**Classification:** spec defect (executability; undefined fixtures, artifact pairs, schemas, expected digests).

#### B6 — Spec defect (per-logical-seed CUDA generator conflicts with mandated maximum-capacity parallelism)

§6 requires that "CUDA must use one independently seeded `torch.Generator(device="cuda")` per logical seed, call `manual_seed(logical_seed)`, and consume draws only for that logical seed", while the same section requires "the maximum available worker/device capacity selected once at startup" and states "serial comparison is prohibited".

Per B3's recomputation this mandates 28,800,000 CUDA generator constructions and `manual_seed` calls per backend per namespace, each followed by draws confined to a single logical seed (`W`=50, `N_w`=4, `L_DOSES`=4 per the committed GPU artifact header). The specification provides no batching, substream, or counter-based mechanism reconciling per-seed generator isolation with device-saturating parallelism. The completed GPU evidence at `1bf7654` achieved its 33.33 s reference run using a single cell-wide CUDA stream, not per-logical-seed generators, and the TASK BUILDER's own proposal (`reviews/taskbuilder_to_architect_l8_gpu_adoption_handoff.md` §6.3) proposed "deterministic counter-based substreams" rather than per-seed generators. The pre-registered RNG architecture is therefore both untested and unreconciled with the parallelism the same section mandates, and the mechanism by which the TASK BUILDER is to satisfy both is left to invention.

**Classification:** spec defect (feasibility and executability; no mechanism specified).

#### B7 — Authorization-scope defect (Wilson-derived interval prescribed under a no-Wilson constraint)

§9.1 prescribes, verbatim, `statsmodels.stats.proportion.confint_proportions_2indep(..., method="newcomb", compare="diff", correction=False, alpha=0.01/1440)`. This call was verified executable as written (statsmodels 0.14.6; `newcomb` is a real and indeed default option) — the defect is not executability.

The Newcombe hybrid-score interval is constructed from **Wilson** score intervals for each proportion. The operative constraint set for this workstream prohibits "bootstrap/Wilson/quorum/fallback" procedures, and Rebecca's Item-1 authorization boundary states it "does not authorize … bootstrap/Wilson procedures; quorum or fallback rules". The specification neither notes this tension, nor scopes the prohibition to the ρ-predicate path, nor cites an authorization for a Wilson-derived construction in the equivalence family. §5 P5 requires that any deviation from constraint text be memorialized with Rebecca's signed waiver; no such memorialization exists.

The CRITIC does not choose the scientific rule and takes no position on whether a Wilson-derived interval is scientifically appropriate here. The specification must either cite the authorization that scopes the prohibition to the predicate path, or specify a construction that does not rely on a prohibited procedure. As written the criterion cannot be cleared.

**Classification:** authorization-scope / spec defect (P5 memorialization absent).

#### B8 — Provenance defect (branch is not based on the named base; would delete Rebecca's operative ruling)

The handoff names GitHub main `b6d4556` (PR #105) as the base. Verified: `b6d4556` is **not** an ancestor of `7c0a3c7`; the actual merge-base is `f4e2231` (PR #101). The reviewed tree consequently omits three files present on main:

- `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` — **Rebecca's operative ruling authorizing this entire GPU workstream**
- `handoffs/THIRD_PARTY_ADVISORY_L8_FULLSCREEN_DEFERRED_ITEMS.md`
- `handoffs/WORKFLOW_COORDINATOR_L8_FULLSCREEN_ARCHITECT_AMENDMENT_HANDOFF.md`

Two consequences. First, the specification cannot be verified in-tree against the ruling whose conditions it is required to satisfy; this review read that ruling from `b6d4556` instead, which is sound for review but is not the state the specification was drafted against. Second, and materially: a merge of this branch as constituted would **delete Rebecca's operative GPU rebuild approval ruling from main**. Under D1–D5 and the single-source-of-truth rule that outcome is not acceptable, and it is not within the CRITIC's authority to fix.

**Classification:** provenance defect (base identity and artifact preservation).

#### B9 — Attestation defect in the routing artifact (β*/ρ parity claim unsupported by the cited evidence)

The routing handoff's assertions include: "The GPU path reproduces CPU β*/ρ within the locked-bar comparison tolerance (`RHO_COMPARE_EPS = 1e-12`) for identical seeds; repeat-run determinism."

Verified against the cited evidence commit `1bf7654`, artifact blob `4841deff…`: the artifact contains **zero** occurrences of `rho`, `complete_verdict`, or `any_seed`, and **no CPU-paired fields** — its header declares a single backend ("PyTorch CUDA float64") and its 240 result rows carry only `mean_beta_star`, `std_beta_star`, `false_kill_rate`, `false_kill_rate_per_seed`, `false_pass_rate`, `mean_beta_star_null`. Its `spec_regime` header cites "L8 instantiation spec v2.2 … `c7d7bed`", not the amended specification. `diagnostics/l8_gpu_full_comparison.py` at the same commit contains zero occurrences of `rho`. There is therefore **no committed ρ parity evidence and no paired CPU↔GPU β*/ρ comparison** at the cited SHA, and no repeat-run determinism artifact at that SHA.

Attribution matters here and is recorded precisely: the **ARCHITECT's** own CRITIC handoff at `7c0a3c7` does **not** make this claim — it asserts only the 4-of-15 calibration divergence and the two misspecification-profile coordinate divergences, both of which this review verified. The unsupported parity assertion appears in the **coordinator routing artifact**. It is classified as a routing/attestation defect rather than an ARCHITECT spec defect, and it must not be relied on by Rebecca as evidence of CPU↔GPU estimator parity.

**Classification:** provenance/attestation defect (routing artifact, not the specification).

### Substantive checks that did NOT block

These were attempted as falsifications and failed to falsify. They are recorded so that remediation does not disturb them and so that a later reviewer need not redo them.

- **Numeric margins are not underpowered.** Recomputed from the committed GPU artifact (`n_valid` = 10,000 at every cell; `std_beta_star` ∈ [0.1088, 0.1165], median 0.1127) at the Bonferroni per-endpoint level α = 0.01/1440 = 6.944 × 10⁻⁶ (two-sided z = 4.4954): the Welch half-width for the mean-β* endpoints is 0.0069–0.0074, far inside `±0.04`. The Newcombe rate-endpoint half-width at the worst case p = 0.5 is 0.03176 — inside `±0.04`, verified by live call. Observed rates are far from 0.5 (false-kill ≈ 0.067, false-pass ≈ 0.026), so realized intervals are much narrower. The §9.2 aggregate margins (paired-t over 240 cells at α = 0.01/6, `±0.01`) and the §9.3 map margins (`L∞ ≤ 0.03`, `L1_mean ≤ 0.01`) are likewise comfortably feasible. The tolerances are not vacuous and not unsatisfiable.
- **The prescribed interval algorithm exists and is callable exactly as written** (statsmodels 0.14.6; `confint_proportions_2indep(..., method="newcomb", compare="diff", correction=False, alpha=0.01/1440)` returns a valid interval). Pinning the reviewed version in Commit A and requiring re-review on change is sound.
- **Bonferroni family definition is arithmetically correct**: 240 cells × 6 endpoints = 1,440 endpoints; the §9.3 map geometry is consistent (16 `(c_min, eta)` locations × 15 `(alpha, v_mult)` cells = 240).
- **Apparatus-failure exclusivity preserves no-relabeling.** §11 confines `INSTRUMENT_FAILURE` to six independent apparatus checks and states that ordinary β*, ρ, false-kill, false-pass, map, and selection outcomes "never become apparatus failure" and yield `NOT_EQUIVALENT`. §14 repeats it. This is correct and is the right direction of protection. (The one leak is the undefined-ρ path in B1.)
- **The frozen-calibration primary arm is fully verified.** The artifact's SHA-256 is exactly `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e` as §4 requires; its declared source blob `ac691f74…` at `6d455bb:diagnostics/l8_power_analysis_results.json` is the correct blob; the declared extraction rule holds (all 15 `(alpha, v_mult)` pairs have exactly 16 source rows, bit-identical within each pair); all 15 emitted `sigma_dose` values match the source bit-for-bit; entries are in ascending numeric `(alpha, v_mult)` order; exactly one entry per pair with no pair missing. Requiring bit-for-bit calibration equality in the primary arm, with any deviation routed to `INSTRUMENT_FAILURE`, is a sound design.
- **Declared blob identities are correct**: `b3d4b52c…` (CPU comparator) and `4841deff…` (GPU artifact) both resolve as stated.
- **Native GPU calibration is correctly not adopted.** §10 retains the divergence descriptively, states explicitly that `0.74999375` "is a retained finding, not an acceptance tolerance", requires an operational GPU diagnostic to consume the frozen CPU artifact, and defers any native-calibration proposal to a separate pre-registered study with fresh CRITIC review and Rebecca's approval. §9.4 keeps the two misspecification selection disagreements as "named negative findings" and refuses to convert exact-coordinate agreement into a pass. This is the correct handling and satisfies the no-relabeling and anti-score-chasing requirements.
- **No prohibited-scope creep found**: the specification claims no L8 scientific result, no scoring, no courier construction, no protected-seed access, no CPU replacement, no automatic retry or CPU fallback, no merge authority, and no L15/L16/L17 work. §3 and §14 keep `EQUIVALENT_FOR_O15_DIAGNOSTICS` narrow and expressly subordinate to Rebecca's separate clearance. §7's statement that "prior evidence cannot satisfy this gate" correctly refuses to launder the completed diagnostic into the pre-registered comparison.
- **Two-commit identity is coherent**: Commit A freezes code/tests/schemas/config/fixtures, Commit B carries returned evidence and records Commit A's SHA as `implementation_sha`, and "Commit A cannot contain its own SHA" is correctly stated. Atomic JSON-then-sidecar publication with a same-directory temporary file, fsync, validation, atomic replace, and a rule against impersonating an older pair is sound as far as it goes; it fails only for the missing concrete schema/digest inputs of B5.

### CPU↔GPU equivalence genuineness (review focus 3) — verified genuine, not renamed, not a tolerance

Independently recomputed from the committed GPU artifact against the frozen CPU calibration table:

| Pair (alpha, v_mult) | CPU `sigma_dose` | GPU native | Absolute difference |
|---|---|---|---|
| (0.0, 1.0) | 2.25008125 | 3.000075 | 0.7499937499999998 (GPU higher) |
| (0.02, 0.5) | 1.3125890624999998 | 1.125090625 | 0.18749843749999995 (GPU lower) |
| (0.02, 1.0) | 3.000075 | 2.25008125 | 0.7499937499999998 (GPU lower) |
| (0.05, 1.0) | 3.000075 | 2.25008125 | 0.7499937499999998 (GPU lower) |
| remaining 11 pairs | — | — | 0.0 (exact match) |

**4 of 15 pairs differ — confirmed.** The maximum absolute difference recomputes to `0.7499937499999998` (see NB1 on the specification's truncated statement of it). Mean absolute difference across all 15 pairs: `0.1624986458333333`. The negative is retained under its own name in §10, is explicitly denied the status of an acceptance tolerance, and native calibration is not adopted — no relabeling, no retrospective tolerance, no score-chasing. The two misspecification-profile coordinate divergences are likewise retained as named negative findings in §9.4. **This portion of the ARCHITECT's handling is correct.** The unsupported β*/ρ parity assertion is a separate matter and is recorded at B9; the ARCHITECT did not make it.

### Equivalence to the amended (CPU) specification (review focus 4) — fails

| Required element | Status |
|---|---|
| PRIMARY = `complete_verdict_false_kill_rate` | **Fails.** Name and role preserved; predicate semantics not (B1: no `RHO_COMPARE_EPS`, no undefined-ρ disjunct). |
| Locked bars β* ≥ 0.2, ρ ≥ 0.8 | Values preserved and correctly tagged; ρ comparison semantics diverge (B1). |
| Locked bar ≥ 3 doses | Not enumerated in §2 (NB6); `L_DOSES = 4` de facto in the committed artifacts. |
| 5 seeds | Preserved (§2, §5, §6). |
| Specificity control | Not enumerated (NB6). |
| Schema | **Fails.** Deferred to TASK BUILDER (B5); §8 field set omits per-seed ρ fields. |
| 7 deterministic ρ tests + case 2a (no-softening) | **Absent.** The specification's §12 battery contains L18 parity fixtures and twelve injected apparatus cases; none is the ρ threshold/tie/constant/decreasing/non-finite battery, and the 2a no-softening assertion that protects the 0.8 bar is nowhere required. |
| Seed derivation | Present but defective (B3). |
| No-relabeling | Preserved (§9.4, §10, §11, §14), except the undefined-ρ leak in B1. |
| No bootstrap/Wilson/quorum/fallback | **Contested** (B7). |
| O-15, no scoring | Preserved. |

### Non-blocking findings

- **NB1 —** §10 states the maximum absolute sigma difference as `0.74999375`; the value recomputes to `0.7499937499999998`. This is a truncated transcription of a retained negative, not a rename and not a tolerance, but it is inconsistent with the specification's own bit-exactness discipline (§4 requires binary64 loading "without rounding or reserialization" and bit-for-bit comparison). Restate the exact binary64 value.
- **NB2 —** The native-calibration negative is under-characterized. The divergences are **bidirectional** (GPU higher at one pair, lower at three) and of **two distinct magnitudes** (`0.7499937499999998` three times, `0.18749843749999995` once), with mean absolute difference `0.1624986458333333`. That pattern indicates the native calibration search lands on adjacent binary-search steps in both directions rather than carrying a one-sided offset. Recording only "4 of 15, max 0.74999375" leaves the finding partly unnamed. The fuller characterization strengthens, not weakens, §10's correct decision not to adopt native calibration.
- **NB3 —** §10 states "There is no native-calibration equivalence gate in v1.0" inside a v1.1 document. Correct the version reference.
- **NB4 —** §9.1 prescribes "the unequal-variance Welch interval" without fixing the degrees-of-freedom convention (Welch–Satterthwaite t versus normal approximation). Immaterial at n = 10,000 but it is implementer discretion in a document that elsewhere eliminates it.
- **NB5 —** §9.1 and §9.2 each apply a "familywise alpha of 0.01", so the combined level across the two families is ≤ 0.02, not 0.01. Because both families are conjunctive requirements for declaring equivalence, this is conservative in the adoption direction and is therefore not blocking; the wording should nonetheless be scoped per family.
- **NB6 —** §2's inherited-rule list omits two `[BAR-Entry 11]` L8 bars present in the M0 decision sheet's L8 row: "≥3 noise doses" and the mandatory specificity control. §2 correctly states that GPU adoption "neither waives nor satisfies a future claim's scoring battery", and the committed constants supply `L_DOSES = 4`, so no bar is moved — but this is the same omission class as the BF1 locked-bar-preservation defect, and enumeration is cheap.
- **NB7 —** The specification cites neither of the two Rebecca artifacts that authorize its existence: the GPU rebuild approval ruling (absent from the tree, B8) and the Item-1 ρ authorization, which is the sole authority for the direct per-seed Spearman ρ path and is committed on `7c0a3c7` but **not merged to main**. §2's claim that "No uncommitted ruling is used" is literally true, but the authority chain for the ρ path is unmerged and uncited. Rebecca's sequencing decision should be explicit about whether the Item-1 authorization merges before this specification is cleared.
- **NB8 —** The routing handoff describes "the full 19.2M GPU diagnostic execution". The workload actually pre-registered in §7 is 240 × (10,000 + 10,000 + 2,000 + 2,000) = **5,760,000 repetitions per backend** (11,520,000 across both backends). The 19.2M figure belongs to the CPU full-screen specification's two-arm accounting (9.6M + 9.6M, per commit `8f3e109`). Whatever Rebecca later releases should name the workload it releases.

---

## 5. Preserved evidence

Preserved and not invalidated by this BLOCK; remediation must not discard it:

1. Part A stands in full: three law quotations verbatim at correct line citations; all thresholds tagged with allowed source classes and correct attributions; Entry 11.3, Entry 12, and Entry 22 citations verified against actual entry text.
2. The frozen-calibration artifact is fully verified end-to-end (digest, source blob, extraction rule, bit-for-bit value match, ordering, completeness).
3. The 4-of-15 native-calibration divergence and the two misspecification-profile selection disagreements are genuine, independently reproduced, retained under their own names, and correctly denied tolerance status. Native GPU calibration is correctly not adopted.
4. The pre-registered numeric margins (`±0.04`, `±0.01`, `L∞ ≤ 0.03`, `L1_mean ≤ 0.01`) are feasible and non-vacuous at the Bonferroni-corrected levels — verified by independent recomputation from committed data.
5. The prescribed interval call is real and executable as written.
6. `INSTRUMENT_FAILURE` exclusivity, the `NOT_EQUIVALENT` routing of ordinary statistical failure, the two-commit implementation/evidence identity, atomic JSON/sidecar publication semantics, the refusal to let prior evidence satisfy the gate, and the narrow scope of `EQUIVALENT_FOR_O15_DIAGNOSTICS` are all sound.
7. All prior M3 evidence is untouched: no scoring occurred, seeds 201–203 and 301–303 were not accessed or rerun, and the retained INSTRUMENT FAILURE labels are unchanged.

---

## 6. Routing

**Exact next authorized role: ARCHITECT** (and only the ARCHITECT), to remediate B1–B7 and NB1–NB8 within the specification, and to re-base per B8.

B8 (base identity and the would-be deletion of Rebecca's ruling) and B9 (the unsupported parity assertion in the routing artifact) are outside the ARCHITECT's specification text and are escalated to **Rebecca** for disposition. The CRITIC does not re-base branches, does not restore deleted rulings, and does not correct another role's handoff.

On remediation the specification returns through a fresh-context CRITIC (Part A then Part B) before Rebecca. TASK BUILDER remains held.

### Explicitly prohibited actions (this review complied)

No scoring. No scoring-mode execution. No re-run of any failed or prior run (O-14). No development run treated as an artifact (O-15). No hold-out, protected, courier, or scoring seed accessed, named, or exposed. No merge to `main` and no push to `main`. No edit to any specification, implementation, scoring artifact, review under review, `STATE.md`, or the provenance log. No co-authoring, fixing, or modification of the work under review. No bar lowered, raised, renamed, reinterpreted, or silently replaced. No negative result renamed. No L15/L16/L17 work. No claim made on Rebecca's behalf.

### Confirmation

No scoring was conducted. No run was rerun. No hold-out or protected seed was accessed or exposed. No merge or push to `main` occurred. Read-only git inspection only (`clone`, `log`, `show`, `diff`, `ls-tree`, `rev-parse`, `grep`, `merge-base`) plus commits to this `critic/` branch alone. All quantitative claims in this review were recomputed independently from committed artifacts; none rests on a commit message.

---

## 7. Pre-push safety scan attestation

A pre-push self-scan was performed over this review artifact before pushing, per `PUBLIC_REPOSITORY_POLICY.md` §3 and §12, covering: credentials, API keys, tokens, passwords, secrets; personal contact details; machine identifiers (hostnames, MAC addresses, SIDs, user account names); private absolute filesystem paths; environment dumps; and PII.

**Findings: none.** This artifact contains only public repository SHAs, blob IDs, branch names, repository-relative file paths, constitution and provenance quotations already committed to the repository, and numeric values recomputed from committed artifacts. No protected seed value is named. No local or private absolute path appears. Classification: no blocker, no Rebecca-decision item, no acceptable-exception item. Scan result: **clean**.
