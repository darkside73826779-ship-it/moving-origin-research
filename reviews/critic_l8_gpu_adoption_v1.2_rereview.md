# CRITIC Re-Review — L8 GPU Diagnostic-Backend Adoption Specification v1.2

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5 binding) `[P4]`

**Gate served:** Fresh-context CRITIC re-review of the ARCHITECT's B1–B8 remediation of the L8 GPU diagnostic-backend equivalence contract — Part A (law fidelity, source tags, provenance/source-SHA verification) then Part B (substantive falsification).

**Reviewer:** CRITIC (independent adversarial review; did not co-author, fix, or modify any artifact under review)

**Supersedes:** nothing. This re-review is additive to `reviews/critic_l8_gpu_adoption.md` @ `6e408aece2836d07a5a21b716e1f7c3b7db5bc04` (branch `critic/l8-gpu-adoption-review`), whose preserved evidence remains valid.

---

## 1. Verdicts

| Result | Value |
|---|---|
| `LAW_FIDELITY` | **BLOCK** |
| `SUBSTANTIVE` | **BLOCK** (reported as blocking observations; never a clearance) |
| **Combined CRITIC ruling** | **BLOCK** |
| Next authorized recipient | **ARCHITECT only** |

Part A blocks on one finding: a misattested controlling-specification source SHA whose actual in-tree content contradicts the remediated locked-bar comparison semantics (**B10**). Per §10 of v1.2 and §15 of v1.1, a Part A block stops the review and returns the artifact to the ARCHITECT; the CRITIC may list substantive observations but may not clear the specification.

Substantive tracing was nevertheless performed and is reported so the ARCHITECT can close every open item in one cycle rather than two. Two further blocking substantive findings (**B11**, **B12**) exist independently of B10. `SUBSTANTIVE: BLOCK` is reported in that sense and is not, and must not be read as, a partial clearance.

**Eight of the nine prior findings are genuinely closed.** The remediation is substantial and largely correct; the block is narrow, concrete, and cheap to fix.

---

## 2. Inputs and SHAs reviewed

| Item | Value | Verification |
|---|---|---|
| Required base | `b6d4556021ad38199d3bfa90fdb3ef9a99988790` | **verified ancestor** of the result SHA |
| Result SHA reviewed | `678af9b9c80b1f22cf65b2bacc4901ad06450856` | reviewed |
| Branch | `architect/l8-gpu-adoption-spec` (force-updated from `7c0a3c7`) | reviewed |
| Commits in `b6d4556..678af9b9` | `51ddbd5`, `096572c`, `417c881`, `bd00817`, `e247c6b`, `678af9b` | inspected individually against file contents |
| Specification v1.2 | `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.2.md` (commit `e247c6b`) | reviewed |
| Changelog | `specs/l8_gpu_diagnostic_backend_adoption_spec_CHANGELOG.md` | reviewed |
| Known-good fixture | `specs/data/l8_gpu_adoption_known_good_v1.json` | digest verified; **every expectation recomputed** |
| Fixture sidecar | `specs/data/l8_gpu_adoption_known_good_v1.json.sha256` | verified against the blob |
| Frozen calibration | `specs/data/l8_cpu_frozen_calibration_v1.json` | digest re-verified unchanged at the result SHA |
| ARCHITECT routing handoff | `handoffs/ARCHITECT_L8_GPU_ADOPTION_V1.2_CRITIC_HANDOFF.md` | reviewed |
| Rebecca GPU rebuild ruling | `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` | **present in-tree from base**; read in full |
| Rebecca Item-1 ρ authorization | `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` | present; **byte-identical** to cited source `69feed8d…` |
| Rebecca geometry-table freeze | `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` | present; **byte-identical** to cited source `5306c302…` |
| Controlling CPU spec package (4 files) | attested source `2082680a7caba85c46e637b3b38d679fa7f80599` | **FAILS — actual source is `69feed8d…`** (B10) |
| CPU baseline | `b1397498ca369067e956479e6c2bd6b0793c3e89` | inspected (seed derivation, draw structure) |
| CPU evidence / GPU evidence | `6d455bb…` / `1bf7654…` | reachability confirmed after the force-update |

All quantitative claims below were recomputed independently from committed artifacts. No claim rests on a commit message or on the routing handoff's blocker-closure map. Git operations were read-only except commits to this `critic/` branch.

---

## 3. Part A — Law fidelity: `LAW_FIDELITY: BLOCK`

### 3.1 Law-diff (P1, P2) — PASS

The three quoted law blocks were re-extracted from v1.2 and compared character-for-character against the constitution at the result SHA:

| Spec line | Law | Cited location | Verbatim match |
|---|---|---|---|
| 15 | L8 — Stakes coupling | `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` | **exact** |
| 19 | L18 — Contamination controls on every positive claim | `docs/ARCHITECTURAL_CONSTITUTION_v2.md:54` | **exact** |
| 23 | L19 — Pre-registration | `docs/ARCHITECTURAL_CONSTITUTION_v2.md:55` | **exact** |

No constitutional text is reconstructed. Cited line numbers are correct.

### 3.2 Source-class tags (P3) — PASS, with one attribution observation

Every numeric threshold, kill condition, verdict value, and test criterion carries an allowed tag. A line-by-line scan for numerics without a tag returned only the document date and the §8.1 enumerated key list, and the latter is covered by the explicit sweep at §8.1: "Literal strings and numeric values above are `[PROPOSED]`." No untagged threshold exists.

Attribution correctness was checked, not merely tag presence. `beta_star ≥ 0.2`, `rho ≥ 0.8`, `≥ 3 doses`, `5 seeds`, and the specificity control are tagged `[BAR-Entry 11]` and all five are present in the M0 decision sheet's L8 row — **the prior NB6 omission of the ≥3-doses bar and the specificity control is now closed** (§3, final paragraph). `RHO_COMPARE_EPS = 1e-12` is correctly tagged `[PROPOSED]` while the predicate it serves is tagged `[BAR-Entry 11]`, which is the right split: the bar is locked, the roundoff tolerance is Rebecca-gated. O-14 is tagged `[OP-Entry 22]` at §6. One attribution observation is recorded as non-blocking at NB-A.

### 3.3 Provenance and source-SHA verification (P6) — **BLOCK**

Four of the five source-SHA attestations in §2 verify. One does not, and its failure is material.

#### B10 — Provenance defect (blocking): the controlling CPU specification in-tree is not the attested `2082680`

Specification §2 item 4 attests: "Controlling CPU specification `specs/l8_g2g4_minimal_full_screen_spec.md`, source SHA `2082680a7caba85c46e637b3b38d679fa7f80599`." §8.1 key 7 compounds it by requiring the executed configuration to record `cpu_spec_sha` as the literal `2082680a7caba85c46e637b3b38d679fa7f80599`. The routing handoff repeats it and adds: "The Item-1 ruling, controlling CPU-spec package, and geometry ruling were preserved from their committed source commits."

Verified by blob identity:

| File | In-tree blob at `678af9b9` | Blob at `2082680` | Actual source commit |
|---|---|---|---|
| `specs/l8_g2g4_minimal_full_screen_spec.md` | `5209560841898e595ee0b0036b4f85e7e64a1a1f` | `ea3c3e97ca461eb6ddca74a6bee244f568f606fb` | **`69feed8d…`** |
| `specs/l8_g2g4_minimal_full_screen_CHANGELOG.md` | differs from `2082680` | — | **`69feed8d…`** |
| `specs/l8_g2g4_minimal_full_screen_EXECUTABILITY_TRACE.md` | differs from `2082680` | — | **`69feed8d…`** |
| `specs/l8_g2g4_minimal_full_screen_TASKBUILDER_HANDOFF.md` | differs from `2082680` | — | **`69feed8d…`** |

The entire four-file controlling package was copied from `69feed8d` — the *first* amendment commit — not from `2082680`. The five subsequent ARCHITECT commits on `architect/l8-g2g4-minimal-fullscreen` (`09f605e`, `e3bbd6c`, `17e8364`, `548d4b9`, `2082680`) carry precisely the advisor-round remediations that the attestation claims are present. None of them is in this tree.

The content difference is not cosmetic. The in-tree copy contains **zero** occurrences of `RHO_COMPARE_EPS` and **no** case 2a. Consequently the tree now holds two committed artifacts that give **opposite** answers on the locked-bar boundary case:

- `specs/l8_g2g4_minimal_full_screen_spec.md:173` (in-tree, attested as controlling): "**Adjacent-inversion / threshold case:** `D̄ = [1, 0, 2, 3]` … assert the value and the predicate outcome (**ρ_s < 0.8 → fail**)."
- `specs/data/l8_gpu_adoption_known_good_v1.json` (in-tree, digest-verified): `adjacent_inversion_threshold` … `"expected_predicate": true`.
- v1.2 §3 (correct, matching `2082680` and Rebecca's directive): passes via `abs(rho - 0.8) <= RHO_COMPARE_EPS`.

This is the B1 defect reintroduced through provenance rather than through the contract text. The GPU contract's §3 is itself correct and complete; but a TASK BUILDER instructed by §2 that the controlling CPU specification is the in-tree `specs/l8_g2g4_minimal_full_screen_spec.md` would read the opposite predicate outcome at the locked 0.8 threshold, and the executed configuration would attest a `cpu_spec_sha` that does not describe any artifact in the tree. The in-tree copy also lacks the §5.6 three-branch apparatus-validity decision tree, the separate true-effect/null-control denominators, the apparatus-invalid geometry disqualification, and the `RHO_COMPARE_EPS` entry in the constants block — all of which v1.2 §3 and §8 rely on.

The signed geometry-table freeze ruling in this same tree independently names `2082680` three times as the CRITIC-cleared amended specification, and Rebecca's GPU rebuild approval states: "The amended spec `architect/l8-g2g4-minimal-fullscreen` @ `2082680` remains the authoritative specification." So the operative authority chain and the tree disagree about which specification is controlling.

**Classification:** provenance defect (source-SHA misattestation) with a consequent in-tree contradiction on a locked-bar comparison. Under P6 this fails Part A. The remedy is mechanical: copy the four-file package from `2082680`, or correct §2/§8.1 to attest the SHA actually present — the former, since `2082680` is the authoritative version by Rebecca's ruling.

### 3.4 Provenance checks that passed

- `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` is byte-identical to `69feed8d…`, its attested source.
- `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` is byte-identical to `5306c302…`, its attested source.
- `docs/rulings/REBECCA_L8_FULLSCREEN_GPU_REBUILD_APPROVAL.md` is present in-tree from base `b6d4556`, as §2 item 1 states.
- The frozen-calibration artifact digest is unchanged at the result SHA: `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e`. The new `.gitattributes` pins the two data files and the sidecar to LF, which strengthens rather than threatens digest stability; the digest was re-verified after that change.
- `b1397498…`, `6d455bb…` and `1bf7654…` all remain reachable after the force-update (from `taskbuilder/l8-power-analysis` and `proposal/l8-gpu-statistical-equivalence`), so no cited evidence was orphaned by the rebase.

---

## 4. Prior blocker closure — verified against the diff, not the closure map

| Prior finding | Status | Basis |
|---|---|---|
| **B1** ρ tolerance / undefined-ρ semantics | **CLOSED in the contract text**; undermined in-tree by B10 | §3 fixes dose ranks `(1,2,3,4)`, one-based ascending midranks with exact-binary64 tie averaging, binary64 Pearson, `RHO_COMPARE_EPS = 1e-12`, the pass rule, the `0.8 − 2·eps` must-fail assertion, and constant-response undefined ρ as a **ρ-predicate failure, not `INSTRUMENT_FAILURE`**. The complete verdict now reads "false-kill iff any of five seeds has `beta_star < 0.2`, undefined rho, or a failing rho predicate", which matches Rebecca's directive disjunct-for-disjunct, and null false-pass matches. §3's final clause correctly confines `INSTRUMENT_FAILURE` to proven independent apparatus faults and otherwise retains the repetition in the denominator with a failing predicate. |
| **B2** comparator cannot compute the endpoints | **CLOSED** | §2 item 5 and §2 closing paragraph define the comparator as `b139749` **plus only** the Rebecca-authorized direct-ρ/complete-verdict extension of §3, with "No other CPU scientific behavior may change". This is within the Item-1 authorization, which authorizes specification of the extension while withholding implementation. |
| **B3** RNG collision semantics | **CLOSED** | §5 restores the baseline derivation and asserts uniqueness over the identity tuple `(cell_ordinal, arm_ordinal, repetition_index, seed_index)` rather than the reduced integer, while counting equal derived integers as `derived_seed_collision_count` and expressly refusing to relabel them as identity duplication. Case 8 of the rehearsal now injects a duplicate **identity tuple**, which is the decidable object. |
| **B4** L18 fixtures absent / self-blocking STOP | **CLOSED as an executability defect** | §7 no longer demands six nonexistent fixtures. It states plainly that "Empty/permuted/shuffled scientific arms are not present in the controlling L8 comparator and are not invented here" and preserves the full L18 obligation for any later scientific claim. The self-blocking precondition is gone. One tag/naming observation remains at NB-A. |
| **B5** fixtures, artifact pairs, schemas, digests deferred | **CLOSED** | §6 names the fixture with its digest (verified) and sidecar; §8 fixes UTF-8/RFC 8785 canonicalization, rejection of unknown keys, duplicate keys, NaN and Infinity, the full configuration key list in source order, the full result-object key list, the exact publication and sidecar paths, the sidecar byte format, temp suffixes, and a concrete recovery procedure with `.previous`/`.incomplete` semantics. A pre-registered expected digest for a stochastic artifact is correctly replaced by the run-0/run-1 byte-identity requirement of §6. |
| **B6** per-seed CUDA generator vs parallelism | **CLOSED** | §5 replaces it with a concrete primitive-draw-tape pipeline: NumPy producers at `os.cpu_count()` (≥ 2 or `INSTRUMENT_FAILURE`), `multiprocessing.Pool(...).imap_unordered(..., chunksize=1)`, bounded pinned queue of depth `4*os.cpu_count()`, 32-repetition blocks, whole-block GPU batches, results restored by identity tuple, no serial fallback. Torch-native RNG is expressly **not** adopted. Verified arithmetic: 256 repetitions per cell per arm is divisible by 32, so §5's claim that no partial batch can occur holds; 3 cells × 2 arms × 256 = 1,536 repetitions and × 5 seeds = 7,680 logical seeds, exactly as §6 states; `Q_per_dose = N_w × W = 16 × 100 = 1600`, consistent with the `(4, N_w, W)` tape shape. The workload is trivially feasible. §5's requirement that a factored CPU evaluator first reproduce the unmodified `b139749` path bit-for-bit for every `d_seed`, β*, and diagnostic verdict is a genuinely strong self-check: an incomplete or misordered tape is caught before any CPU↔GPU comparison is permitted. |
| **B7** Wilson-derived interval under a no-Wilson constraint | **CLOSED and positively grounded** | §4 retires the Newcombe/Bonferroni/aggregate/map/equivalence-set machinery outright and replaces it with paired same-seed parity. This is not merely permissible — it is what the operative ruling requires: "**The GPU path must reproduce the CPU path's per-seed `β*` and `ρ` values for identical seeds** — bit-for-bit, or provably-equivalent within the locked-bar comparison tolerance (`RHO_COMPARE_EPS = 1e-12`)". §4's tolerance choice of `1e-12`, its demand for identical undefined-ρ masks, exactly identical predicate booleans and counts, and its rule that "A numeric value within tolerance but producing a different predicate boolean is `NOT_EQUIVALENT`" together close the silent-bar-movement path: tolerance can never rescue a predicate disagreement. |
| **B8** base identity / would-delete Rebecca's ruling | **CLOSED** | `b6d4556` is a verified ancestor of `678af9b9`, and a set-difference over the two trees shows **no** file present on main is missing from the result — the GPU rebuild approval and both PR #102 handoffs are all restored. |
| **B9** unsupported β*/ρ parity assertion | **CLOSED** | v1.2 does not repeat the claim. §10 restates the retained negative at full binary64 precision — `0.7499937499999998`, second magnitude `0.18749843749999995`, mean `0.1624986458333333` — every value matching this reviewer's independent recomputation exactly. **Prior NB1 (truncated value) and NB2 (under-characterized negative) are both closed.** Prior NB8 is also closed: Rebecca's ruling supplies the 19.2M figure and its derivation (20 geometries × 240 cells × 2,000 sims × 2 arms = 19,200,000, verified), which is the full screen and is properly distinct from the 1,536-repetition sentinel. |

Prior NB3, NB4 and NB5 are moot: the version reference, the Welch degrees-of-freedom convention and the two-family alpha wording all lived in machinery that §4 retired. Prior NB7 is substantially closed — §2 now cites both Rebecca rulings and both are in-tree — with one residual tagging observation at NB-E.

---

## 5. Part B — Substantive observations (blocking; not a clearance)

### B11 — Spec defect (blocking): the pre-registered exact `expected_rho` is arithmetic-order dependent and undecidable as written

§3 defines ρ only as "the binary64 Pearson correlation between dose ranks and response ranks". §6 states that the deterministic cases "are exactly those in the known-good contract", and §8.2 requires `deterministic_tests` rows carrying `cpu_observed`, `gpu_observed` and `pass`. The fixture pre-registers `adjacent_inversion_threshold` with `"expected_rho": 0.7999999999999999`.

That literal is not a property of the mathematics; it is a property of one particular order of binary64 operations. Recomputed here from dose ranks `[1,2,3,4]` and midranks `[2,1,3,4]`, all of the following are mathematically valid Pearson evaluations and they disagree in the last bits:

| Evaluation order | binary64 result |
|---|---|
| `numpy.corrcoef` | `0.7999999999999999` |
| `cov / sqrt(sa) / sqrt(sb)` | `0.7999999999999999` |
| `cov / sqrt(sa * sb)` | `0.8` |
| pure-Python sum-based | `0.8` |
| `scipy.stats.pearsonr` | `0.8` |
| `cov / (sqrt(sa) * sqrt(sb))` | `0.7999999999999998` |
| numpy `std`-based | `0.7999999999999998` |

`0.8 == 0.7999999999999999` is `False`. All three values pass the ρ predicate under `RHO_COMPARE_EPS`, so **predicate parity is safe** — but the deterministic test asserts the *value*, and v1.2 fixes neither the operation order nor a value-comparison tolerance. A conforming implementation that computes exactly `0.8` fails a mandatory deterministic test, and per §10 every deterministic test must pass for `EQUIVALENT_FOR_O15_DIAGNOSTICS`. The GPU reduction order will almost certainly differ from NumPy's, so the same exposure applies to `gpu_observed`.

The controlling specification at `2082680` anticipated exactly this: "deterministic test value checks may use a fixed numeric tolerance such as `abs(actual − expected) <= 1e-12`". That mitigation is absent from v1.2 **and** absent from the in-tree CPU-spec copy (B10), so the remediation dropped it on both paths at once.

Remedy is the ARCHITECT's to choose, not the CRITIC's: either fix the exact evaluation order that yields the pre-registered literal, or pre-register a value-comparison tolerance distinct from `RHO_COMPARE_EPS`. Note that `tied_responses` at `0.9486832980505138` (= `sqrt(0.9)`) and the `±1.0` cases reproduced exactly under every ordering tried, so the exposure is specific to the threshold case — which is the one case that matters most for the locked bar.

**Classification:** spec defect (executability; order-dependent expected value in a mandatory pass/fail gate). Independently demonstrated.

### B12 — Spec defect (blocking): the seed-derivation key string is under-specified

§5 states "CPU seed derivation is preserved exactly" and writes it out as:

`base_seed = int.from_bytes(sha256("alpha=<a>|vmult=<v>|cmin=<c>|eta=<e>").digest()[:8], "little") mod 2^31`

The baseline at `b139749:diagnostics/l8_power_analysis.py:161–165` is:

`key = f"alpha={alpha:.6f}|vmult={v_mult:.6f}|cmin={c_min:.6f}|eta={eta:.6f}"`

The **fixed six-decimal formatting is the digest input** and is omitted from §5. `alpha=0.1` versus `alpha=0.100000` are different byte strings and therefore different `base_seed` values, so an implementer who substitutes the placeholders with default float formatting silently breaks the "preserved exactly" guarantee and every downstream seed. §8.1 key 14 compounds this by requiring the executed configuration to record `rng.seed_formula`, which would then memorialize the under-specified form.

The per-seed offset is correct and verified: §5's `seed_int = (base_seed + i*5 + s) mod 2^31` matches the baseline's `(base_seed + i * N_SEEDS + s) % (2 ** 31)` exactly, with `N_SEEDS = 5`.

**Classification:** spec defect (executability; unspecified digest input). Verified against the named baseline.

### Substantive checks that did NOT block

- **Sentinel coverage matches the operative ruling's required equivalence packet item-for-item.** Rebecca requires the 7 deterministic categories plus the 2a no-softening test on GPU, and a CPU-vs-GPU sentinel "covering: combo + null arms; tie cases; boundary ρ; zero-variance ρ; non-finite / apparatus-validity paths; and a few ordinary cells", plus a repeat run for determinism. Traced: combo and null arms (§6), tie case (`tied_responses`), boundary ρ (`adjacent_inversion_threshold`), zero-variance ρ (`constant_responses`), non-finite/apparatus path (`nonfinite_without_apparatus_fault`), three ordinary cells (§6), repeat execution from a fresh process with byte-identical canonical payload required (§6), no third execution permitted under O-14. Coverage is complete.
- **Every fixture expectation was recomputed independently and all reproduce**, except the order-dependence recorded at B11: `perfect_increasing` → `1.0`; `tied_responses` → `0.9486832980505138`; `constant_responses` → undefined with predicate `false`; `decreasing_responses` → `-1.0` with predicate `false`; `nonfinite_without_apparatus_fault` → undefined with predicate `false`; `no_softening` at `direct_rho = 0.799999999998` is exactly `2 × RHO_COMPARE_EPS` below the bar and correctly **fails**, which is the assertion that keeps the 0.8 bar from moving. All four `complete_verdict_cases` reproduce, including `undefined_rho` → false-kill `true`.
- **Fixture and sidecar integrity verified.** The fixture blob hashes to `d1ee4f56dfafcbb1c18e84c36e2110e9038ceaa1f9f4699753140578e4f19a2a`, matching both §6 and the committed sidecar, and the sidecar's `<digest>␣␣<basename>` form matches the §8.3 convention.
- **Sentinel geometry is a legitimate interior geometry under the signed freeze.** `(W=100, N_w=16)` lies inside the frozen sets `W ∈ {50,100,200,400}` and `N_w ∈ {4,8,16,32,64}` and touches no tested boundary (`W ∉ {50,400}`, `N_w ∉ {4,64}`), so it does not collide with the boundary-escalation rule.
- **The twelve rehearsals are decidable and correctly routed.** Each names a concrete injection point, preserves the committed input pair, runs in a fresh process, and emits a fixed row shape. Case 5 correctly conditions `INSTRUMENT_FAILURE` on an independent apparatus fault rather than on non-finiteness as such; case 9 asserts payload identity under shuffled completion order; case 10 asserts prior-pair preservation with `.incomplete` temps; case 12 keeps an ordinary predicate failure out of `INSTRUMENT_FAILURE`. "No failure case is retried" preserves O-14.
- **Adoption rule and no-relabeling are intact.** §10 requires the full conjunction, routes parity failure on a valid apparatus to `NOT_EQUIVALENT`, routes independent apparatus-check failure to `INSTRUMENT_FAILURE`, and states that ordinary statistical failures never become apparatus failure.
- **Scope discipline holds.** §1 disclaims any L8 scientific claim; §11 prohibits implementation and execution by the ARCHITECT, scoring, courier construction, protected-seed use or exposure, G2–G4 freeze, full-screen release, bootstrap/Wilson/quorum/fallback/unpaired intervals/post-run tolerance choice, serial benchmark, automatic retry, CPU fallback, failed-run replacement, native GPU calibration or torch-native RNG adoption, changes to bars/controls/negative names/geometry table/CPU equations/selection semantics, merge to main, and L15–L17 before M5. §10 and the handoff both hold TASK BUILDER.
- **Repository safety.** A private-path and machine-identifier scan across every file changed between `b6d4556` and `678af9b9` returned one hit, which is the public repository name `darkside73826779-ship-it/moving-origin-research` in a document header and is present on main. No private absolute path, hostname, username, device identifier, credential or PII appears in any reviewed artifact. Separately: the local Windows paths used to transport the artifacts in the routing message must not be copied into any repository artifact; they are not present in the tree.

### Non-blocking findings

- **NB-A —** §7 tags with `[LAW-L18]` a mapping that the law does not contain: "its frozen baseline is the CPU comparator, its naive baseline is the unextended beta-only `b139749` output …, its oracle is the deterministic rho/aggregation contract, and its contamination controls are the combo and null-control arms". Re-using L18's control vocabulary for objects that are not L18 controls is an ARCHITECT construction and should be tagged `[PROPOSED]`, not `[LAW-L18]`; L20 (honest naming) argues for saying plainly that these are backend-parity roles rather than L18 controls. Non-blocking only because §7's second paragraph explicitly forecloses the dangerous reading: "This narrow backend-equivalence battery does not waive L18 for a later L8 positive claim." No reader may treat §7 as L18 satisfaction.
- **NB-B —** §6 says "The seven rho categories, the no-softening subtest, and four complete-verdict cases", implying eight ρ rows. The fixture's `rho_cases` array holds seven rows **including** `no_softening`, i.e. six ρ categories plus the no-softening subtest, with the seventh CPU-spec category (complete-verdict aggregation) correctly relocated to `complete_verdict_cases`. Total coverage is complete — all 7 categories plus 2a are asserted — but the count sentence is off by one and an implementer or reviewer checking arity will not find eight rows.
- **NB-C —** `derived_seed_collision_count` is **guaranteed nonzero by construction and its value is predictable**: the baseline key contains only `(alpha, v_mult, c_min, eta)`, so `base_seed` is arm-invariant and the combo and null arms of a cell generate identical `seed_int` sets of 1,280 values each — 3,840 colliding pairs across the three sentinel cells, before any hash coincidence. §5 is right not to relabel these as identity duplication, but the expected value should be pre-registered so a nonzero count is not later mistaken for a defect. Relatedly, §5 specifies "one immutable primitive tape per seed" while the identity tuple includes `arm_ordinal` and `seed_int` does not; the contract should state whether the tape is arm-invariant (and therefore shareable between the combo and null arms, which differ only in `sigma_dose`) or arm-scoped. §5's bit-for-bit baseline-reproduction gate will catch a wrong choice, but the intent should not be left to inference.
- **NB-D —** §8.2 describes each cell row as "`cell_ordinal`, coordinates, `base_seed`" without enumerating the coordinate keys or their order, inside a section that otherwise claims exact source-order keying and rejects unknown fields. Enumerate them.
- **NB-E —** §2 items 2 and 3 tag `docs/rulings/REBECCA_L8_FULLSCREEN_ITEM1_RHO_AUTHORIZATION.md` and `docs/rulings/REBECCA_L8_GEOMETRY_TABLE_FREEZE.md` `[PROPOSED]`. Both documents declare themselves operative and signed. Tagging an operative Principal ruling `[PROPOSED]` mis-states its status; a citation of operative authority needs no `[PROPOSED]` tag. The same applies to the retained empirical negative in §10, which is observed evidence rather than a proposal.
- **NB-F —** Rebecca's ruling makes binding, for the GPU implementation, "Same §7.1 output schema (fields, order, types, NaN→null, atomic write); same output paths (`diagnostics/l8_g2g4_minimal_full_screen.json` + `_HANDOFF.md`)". v1.2 defines a new equivalence-packet schema and path, which is appropriate for this gate, but never carries that constraint forward for the eventual full-screen GPU run. This is non-blocking because §1 scopes v1.2 to backend equivalence, §2 incorporates the ruling as operative authority, and §11 prohibits full-screen release — but under the BF1 precedent on enumerating locked content, the constraint should be stated explicitly rather than left to incorporation by reference.

---

## 6. Preserved evidence

Preserved and not invalidated by this BLOCK:

1. Everything preserved by the prior review at `6e408aec` remains valid: the three verbatim law quotations, the Entry 11.3 / Entry 12 / Entry 22 verifications, the fully verified frozen-calibration artifact, the independently reproduced 4-of-15 native-calibration divergence, and the verified reachability of the cited CPU and GPU evidence blobs.
2. Part A §3.1 and §3.2 of this re-review pass: law-diff exact, no untagged threshold, and the previously omitted `≥3 doses` and specificity bars now enumerated.
3. B1–B9 closure findings above stand as verified closures. The remediation's substance — the exact ρ predicate, the authorized comparator definition, identity-tuple uniqueness, the primitive-tape pipeline with its baseline bit-for-bit gate, the fixed schemas and publication semantics, the twelve rehearsals, and paired same-seed parity grounded in Rebecca's ruling — should not be reworked.
4. The known-good fixture's digest, sidecar, and all expectations other than the threshold-case literal are independently verified correct.
5. The retained negatives are correctly named and stated at full precision: native-calibration divergence at four of fifteen pairs, and the two misspecification-profile coordinate disagreements. Native GPU calibration and torch-native RNG remain unadopted.
6. All prior M3 evidence is untouched: no scoring, seeds 201–203 and 301–303 neither accessed nor rerun, retained INSTRUMENT FAILURE labels unchanged.

---

## 7. Routing

**Exact next authorized role: ARCHITECT** (and only the ARCHITECT), to close **B10**, **B11**, **B12** and NB-A through NB-F. B10 is mechanical: bring the four-file controlling CPU-spec package from `2082680` into the tree, since Rebecca's ruling names `2082680` as authoritative, and keep §2 item 4 and §8.1 key 7 consistent with whatever is actually committed.

On remediation the contract returns through a fresh-context CRITIC (Part A then Part B) before Rebecca. TASK BUILDER remains held; the full-screen GPU execution additionally requires Rebecca's explicit release, which this specification does not and cannot supply.

### Explicitly prohibited actions (this review complied)

No scoring. No scoring-mode execution. No implementation or diagnostic execution. No re-run of any failed or prior run (O-14). No development run treated as an artifact (O-15). No hold-out, protected, courier, or scoring seed accessed, named, or exposed. No merge to `main` and no push to `main`. No G2–G4 freeze and no full-screen release. No edit to any specification, implementation, fixture, ruling, review under review, `STATE.md`, or the provenance log. No co-authoring, fixing, or modification of the work under review. No bar lowered, raised, renamed, reinterpreted, or silently replaced. No negative result renamed. No L15/L16/L17 work. No claim made on Rebecca's behalf.

### Confirmation

No scoring was conducted. No run was rerun. No hold-out or protected seed was accessed or exposed. No merge or push to `main` occurred. Read-only git inspection only (`fetch`, `log`, `show`, `diff`, `ls-tree`, `rev-parse`, `rev-list`, `merge-base`, `cat-file`, `grep`) plus commits to this `critic/` branch alone. Every quantitative claim was recomputed independently from committed artifacts; none rests on a commit message or on the routing handoff's blocker-closure map.

---

## 8. Pre-push safety scan attestation

A pre-push self-scan was performed over this review artifact before pushing, per `PUBLIC_REPOSITORY_POLICY.md` §3 and §12, covering credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute filesystem paths, environment dumps, and PII.

**Findings: none.** This artifact contains only public repository SHAs, blob identifiers, branch names, repository-relative paths, quotations from committed repository documents, and numeric values recomputed from committed artifacts. No protected or hold-out seed value is named; the seed-pool identifiers referenced are already published across `main`. No local, private, or transport path appears. Classification: no blocker, no Rebecca-decision item, no acceptable-exception item. Scan result: **clean**.
