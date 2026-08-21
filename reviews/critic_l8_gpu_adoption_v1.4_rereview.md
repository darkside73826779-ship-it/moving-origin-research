# CRITIC Re-Review — L8 GPU Diagnostic-Backend Adoption Specification v1.4

**Date:** 2026-08-21 · **Regime:** B (post-Entry 81; `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5 binding) `[P4]`

**Gate served:** Fresh-context CRITIC re-review of the ARCHITECT's B13 / NB-G–NB-I remediation of the L8 GPU diagnostic-backend equivalence contract — Part A (law fidelity, source tags, provenance/source-SHA verification) then Part B (substantive falsification), with focused attention on the §8.4 digest domain and the absence of circular, runtime-varying, or omitted scientific fields.

**Reviewer:** CRITIC (independent adversarial review; did not co-author, fix, or modify any artifact under review)

**Additive to:** `reviews/critic_l8_gpu_adoption.md` @ `6e408aec`, `reviews/critic_l8_gpu_adoption_v1.2_rereview.md` @ `3bd6b05f`, and `reviews/critic_l8_gpu_adoption_v1.3_rereview.md` @ `91b1be14`. Preserved evidence in all three stands.

---

## 1. Verdicts

| Result | Value |
|---|---|
| `LAW_FIDELITY` | **PASS** |
| `SUBSTANTIVE` | **CLEAR** |
| **Combined CRITIC ruling** | **CLEAR** |
| Next authorized recipient | **Rebecca R. McClintic** |

All thirteen blocking findings (B1–B13) and all nine non-blocking findings (NB-A–NB-I) raised across three prior reviews are verified closed against the committed artifacts. No blocking finding remains.

**What this clearance is, and is not.** It clears the reviewed specification for Rebecca's gate. It does **not** release the TASK BUILDER, does **not** authorize implementation or execution, and does **not** release the full-screen GPU diagnostic — under the operative GPU rebuild approval that run requires ARCHITECT approval **and** CRITIC clearance **and** Rebecca's explicit release, and the ruling states expressly that clearance does not auto-release it. Every `[PROPOSED]` criterion in the contract remains inoperative until Rebecca signs it.

---

## 2. Inputs and SHAs reviewed

| Item | Value | Verification |
|---|---|---|
| Required base | `b6d4556021ad38199d3bfa90fdb3ef9a99988790` | **verified ancestor**; no file present on main is missing from the result tree |
| Routing state reviewed | `530104a9886b44e633b7a6cd9ac71877082e0fc6` (branch head) | reviewed |
| v1.4 specification commit | `4c84248897fe7c0b10f669bba352a05e3268edf2` | reviewed |
| Prior reviewed SHA | `933f513bbb5847b314368f568d08f02829526745` (v1.3) | delta reviewed |
| Specification v1.4 | `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.4.md` | reviewed in full |
| Changelog | `specs/l8_gpu_diagnostic_backend_adoption_spec_CHANGELOG.md` | every v1.4 bullet verified against the diff |
| ARCHITECT routing handoff | `handoffs/ARCHITECT_L8_GPU_ADOPTION_V1.4_CRITIC_HANDOFF.md` | in-tree copy **byte-identical** to the transported copy |
| Known-good fixture + sidecar | `specs/data/l8_gpu_adoption_known_good_v1.json` (+ `.sha256`) | digest unchanged and re-verified: `65256ff4…` |
| Frozen calibration | `specs/data/l8_cpu_frozen_calibration_v1.json` | digest unchanged and re-verified: `f012849c…` |
| Controlling CPU spec package (4 files) | attested `2082680a7caba85c46e637b3b38d679fa7f80599` | **all four still byte-identical** |
| Item-1 ρ authorization | attested `69feed8d…` | byte-identical |
| Geometry-table freeze ruling | attested `5306c302…` | byte-identical |
| GPU rebuild approval | at base `b6d4556` | present in-tree |
| CPU baseline | `b1397498…` | inspected (seed derivation) |

Delta scope is tight and matches the handoff's claim: the v1.3 handoff removed, the v1.4 handoff added, the changelog extended, and the specification renamed v1.3 → v1.4 with 35 changed lines. No fixture, calibration, ruling, or controlling-specification file was touched — so no prior closure could have been silently regressed, and I confirmed each by blob identity rather than inference.

Every quantitative claim below was recomputed independently from committed artifacts. Nothing rests on a commit message, changelog, or handoff attestation. Git operations were read-only except commits to this `critic/` branch.

---

## 3. Part A — Law fidelity: `LAW_FIDELITY: PASS`

### 3.1 Law-diff (P1, P2) — PASS

Re-extracted and compared character-for-character at the reviewed SHA: L8 → `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` **exact**; L18 → `:54` **exact**; L19 → `:55` **exact**. Cited line numbers correct. No constitutional text reconstructed.

### 3.2 Source-class tags (P3) — PASS

A line-by-line scan for numerics lacking an allowed tag returned only: the document date; the three operative-ruling citations (which carry commit SHAs, not thresholds); the §8.1 enumerated configuration key list, covered by its sweep sentence "Literal strings and numeric values above are `[PROPOSED]`"; and the new §8.4 enumerated payload key list, covered by its own sweep sentence "All literals and test criteria in this list are `[PROPOSED]`". **No untagged threshold exists**, and the new section carries its own sweep rather than relying on §8.1's.

Attribution remains correct throughout: `beta_star ≥ 0.2`, `rho ≥ 0.8`, `≥ 3 doses`, `5 seeds` and the specificity control are `[BAR-Entry 11]` and all five trace to the M0 decision sheet's L8 row; `RHO_COMPARE_EPS` and `RHO_TEST_VALUE_EPS` are `[PROPOSED]` and kept distinct from the locked predicate; O-14 is `[OP-Entry 22]` at §6 and again at §8.4's no-third-run clause.

### 3.3 Provenance and source-SHA verification (P6) — PASS

| §2 item | Attested source | Result |
|---|---|---|
| 1 — GPU rebuild approval (now untagged) | at base `b6d4556` | present in-tree |
| 2 — Item-1 ρ authorization | `69feed8d…` | **byte-identical** |
| 3 — Geometry-table freeze | `5306c302…` | **byte-identical** |
| 4 — Controlling CPU spec package | `2082680…` | **byte-identical, all four files** |

The two digests the specification asserts as literals in §2, §6 and §8.4 both re-verify: fixture `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7` and frozen calibration `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e`. The sidecar matches the fixture blob.

Part A passes; substantive review was authorized to proceed.

---

## 4. Part B — Substantive: `SUBSTANTIVE: CLEAR`

### B13 — CLOSED

The undefined object is now defined. §6 no longer says "After removal of runtime metadata"; it says "Using exactly the §8.4 construction". New §8.4 fixes a twelve-key payload object in explicit source order, requires RFC 8785 serialization and a lowercase SHA-256 over those canonical bytes, enumerates the exclusions exhaustively, and forbids any alteration of included fields: "No field inside `deterministic_tests` or `cells` may be removed, masked, rounded, normalized, or reordered before hashing."

I audited the definition against the three hazards the handoff names.

**No circularity.** The excluded set removes every field whose value depends on the comparison the digest feeds: `scientific_payload_sha256` itself, each run's `run_ordinal`, top-level `equivalence` (whose `repeat_payloads_equal` flag is literally the comparison's output), and top-level `verdict` (which §10 derives from repeat-payload equality among other conditions). Nothing in the twelve keys references the digest or any value derived from it. This is the same architecture the program adopted in the M3 reproducibility contract, where `overall_verdict` was excluded from the compared digest precisely because the verdict depends on the reproducibility the digest determines. The precedent is followed, not reinvented.

**No runtime-varying field survives inclusion.** I traced each of the twelve keys to its source:

| Key | Source | Deterministic across the two runs? |
|---|---|---|
| `schema_version` | literal | yes |
| `implementation_sha` | validated configuration (Commit A) | yes |
| `config_sha256` | RFC 8785 digest of the §8.1 configuration object | yes — §8.1 carries only literals and *formula strings*, notably `producer_workers='os.cpu_count()'` and `queue_depth_formula='4*os.cpu_count()'`, so no resolved machine value enters it |
| `fixture_sha256` | literal, verified | yes |
| `frozen_calibration_sha256` | literal, verified | yes |
| `geometry`, `repetitions_per_cell_per_arm`, `arms`, `cells_config` | configuration | yes |
| `derived_seed_collision_count` | §10, pinned to `3840` | yes — independently recomputed |
| `deterministic_tests` | §8.2 rows over fixed fixture inputs | yes |
| `cells` | §8.2 run cell array over fixed seeds | yes |

The exclusions catch every field that could not be stable: `elapsed_seconds`, `producer_worker_count`, `numpy_version`, `torch_version`, `cuda_runtime_version`, `gpu_model`, and — critically — `run_ordinal`. That last one is the exact trap B13 warned of: `run_ordinal` is `0` for the first run and `1` for the second, so including it would have made byte-identity impossible and `INSTRUMENT_FAILURE` certain under a rule that forbids a third execution. It is excluded by name. I checked the §8.2 arm-row field list independently for any residual timing or environment field and found none — every arm field is a count, a mean, a maximum delta, or an equality boolean.

**No scientific field is omitted.** The included set spans the complete deterministic-test array and the complete run cell array "including every arm-level count, mean, maximum delta, undefined-mask equality, and predicate-vector equality field", with `base_seed` present per cell so seed-derivation drift would be caught. The four excluded top-level members carry no independent scientific content: `equivalence` holds booleans derivable from the included data; `verdict` is a derived conclusion; `header` re-enters through `config_sha256` minus exactly the environment fields; and `failure_rehearsal` records twelve cases that each execute in their own fresh process rather than inside the twice-run sentinel, so including them in a per-run sentinel payload would be a category error — §10 gates them separately.

Two further properties make the construction sound rather than merely complete. RFC 8785 is the right canonicalization choice here: it fixes key ordering and, through ES6 double serialization, gives an exact and reversible representation of every binary64 mean and delta, so float formatting cannot drift between runs. And §8.4 requires **both** byte-array identity and digest-string identity, which is redundant by design in the right direction.

### NB-G, NB-H, NB-I — all CLOSED

- **NB-G** — §6 now reads "raw committed-LF file SHA-256" and adds: "The fixture and frozen-calibration digests cover their committed UTF-8/LF file bytes, not RFC 8785 reserialization." The ambiguity between file digests and canonical-form digests is resolved in the direction I verified operationally.
- **NB-H** — `[PROPOSED]` removed from §2 item 1, the merged operative GPU rebuild approval. Item 4's `[PROPOSED]` correctly remains, since `2082680` is a CRITIC-cleared but unmerged specification.
- **NB-I** — §10 now defines the metric formally: `derived_seed_collision_count = sum_z m_z*(m_z-1)/2`, where `m_z` is the number of distinct full identity tuples whose derived `seed_int` equals `z` — that is, unordered pairs of distinct identity tuples sharing a derived integer. This matches the unordered-pair reading I computed independently, which yields exactly `3840` for this sentinel, so the formal definition and the pinned value agree. The gate is now portable to a future sentinel where the readings would diverge.

### Preservation of prior closures — verified, not assumed

No fixture, calibration, ruling, or controlling-specification file changed in this delta, and I confirmed by blob identity that the controlling four-file package remains byte-identical to `2082680` and both data digests are unchanged. Spot-checking the substance of the earlier closures in the v1.4 text: §3 still carries the exact ρ construction, both disjoint epsilons, the undefined-ρ predicate failure, and Rebecca's complete-verdict disjuncts; §5 still carries the exact six-decimal seed key with its digest-input clause, identity-tuple uniqueness, and the arm-scoped primitive tape with the null-arm `xi_l` rule; §7 still names backend-parity roles honestly and preserves the full L18 obligation; §10 still carries the full-screen schema and output-path constraint forward. The changelog's closing assertion — "No prior blocker closure, locked bar, law quotation, calibration value, fixture expectation, geometry, negative finding, or authorization boundary changed" — is true. Each of the six v1.4 changelog bullets was checked against the diff; none over-claims.

### Executability trace — complete

Applying the binding executability standard end-to-end, tracing the way the TASK BUILDER would:

1. **Test/rehearsal fixture** — geometry `(W=100, N_w=16)`, `Q_per_dose=1600`, three exact cells with ordinals, 256 repetitions per cell per arm, five seeds, combo-then-null ordering, per-arm sigma source (frozen artifact for combo, `0.0` for null, no calibration executed), exact RNG namespace and identity, exact result schema and ordering, and pre-registered expectations: exact values plus `RHO_TEST_VALUE_EPS` for the deterministic tests, and for the stochastic sentinel a repeat-identity gate whose payload domain is now fully enumerated. No bootstrap or maximum-attempt counts arise because no resampling and no retries are permitted.
2. **Committed artifact pair** — fixture and sidecar both committed at verified digests, with the sidecar byte format, publication paths, temp suffixes and recovery procedure fixed, and §8.3 assigning fixture freezing to Commit A.
3. **Stochastic realizations** — fixed by an exact RNG algorithm, an exact seed derivation whose digest input is declared invariant, exact draw shapes `(4,N_w,W)` per primitive, an exact recording boundary, and baseline construction order, all backstopped by §5.5's requirement that a factored CPU evaluator reproduce the unmodified `b139749` path bit-for-bit before any CPU↔GPU comparison is permitted. A distribution is nowhere substituted for a realization.
4. **Result schemas, orderings, digests** — §8.1, §8.2, §8.3 and §8.4 fix keys in source order, RFC 8785 canonical bytes, rejection of unknown keys, duplicate keys, NaN and Infinity, the publication pair, and the digest domain.

I could not find an executable input the TASK BUILDER would have to invent. That is the standard v2.6 failed, and v1.4 meets it.

### Independent verifications supporting this clearance

- Fixture expectations recomputed and all reproduce: `perfect_increasing` → `1.0`; `adjacent_inversion_threshold` decidable under `RHO_TEST_VALUE_EPS` across all three demonstrated binary64 orderings; `tied_responses` → `0.9486832980505138`; `constant_responses` and `nonfinite_without_apparatus_fault` → undefined with predicate `false`; `decreasing_responses` → `-1.0`, predicate `false`; `no_softening` fails at exactly `2 × RHO_COMPARE_EPS`. All four `complete_verdict_cases` reproduce, including `undefined_rho` → false-kill `true`.
- Sentinel arithmetic: `3 × 2 × 256 = 1,536` repetitions, `× 5 = 7,680` logical seeds, `256 mod 32 = 0` so no partial batch, `Q_per_dose = N_w × W = 1600` consistent with the tape shape.
- Collision count: base seeds `975924316`, `401917689`, `444671194`; no range wraps `2^31`; zero cross-cell overlap on all three pairs; unordered pairs `= 3840`, matching the now-formal §10 definition and its pinned value.
- Geometry `(W=100, N_w=16)` lies inside the signed frozen sets and touches no tested boundary, so it does not collide with the boundary-escalation rule.
- Sentinel coverage matches the operative ruling's required equivalence packet item-for-item: seven deterministic categories plus 2a, combo and null arms, tie case, boundary ρ, zero-variance ρ, non-finite/apparatus path, three ordinary cells, and a repeat run for determinism.
- Paired-parity model remains exactly what the ruling requires — same-seed reproduction bit-for-bit or within `RHO_COMPARE_EPS` — and §4's rule that a value within tolerance producing a different predicate boolean is `NOT_EQUIVALENT` still forecloses silent bar movement.
- No-relabeling holds: `INSTRUMENT_FAILURE` is confined to independent apparatus checks in §11, ordinary statistical failure routes to `NOT_EQUIVALENT` in §10, and undefined ρ remains a predicate failure.
- Both negatives remain named at full binary64 precision, and native GPU calibration and torch-native RNG remain unadopted.
- Scope discipline: §11's prohibitions are intact; §10 and the handoff hold TASK BUILDER; nothing claims an L8 scientific result.
- Repository safety: a private-path, credential and machine-identifier scan across every file changed between `933f513` and `530104a` returned zero hits.

### Non-blocking findings (none gate Rebecca's decision)

- **NB-J —** The artifact schema records per-cell and per-arm aggregates, maximum deltas and equality booleans, but not the per-seed `β*`/`ρ` vectors, so the repeat digest is computed over quantities that are permutation-invariant in the per-seed index. Ordering drift is separately caught by rehearsal case 9 and by identity-tuple restoration, so the gate is not weak in practice; adding a per-cell, per-arm digest over the ordered per-seed vectors would make it strictly tighter. Worth considering for the full-screen contract rather than for this gate.
- **NB-K —** §6 says the sentinel is "executed twice from a fresh process" while §8.4 requires the canonical payload bytes to be "retained in memory until the containing result validates" and both runs to appear as two rows of one result object. The party that holds both byte arrays for the comparison is therefore implicit. This cannot produce a wrong verdict, since digest-string equality is also required and is computable from either arrangement, but one sentence naming the comparing process would remove the ambiguity.
- **NB-L —** §8.2 describes `header` as "exact configuration object plus" six fields without saying whether the configuration is nested as a sub-object or flattened into `header`. §8.4 key 3 and the exclusion list both read on that structure. `config_sha256` is deterministic regardless because §8.1 defines the object independently, so nothing is at risk; stating the nesting would help a re-verifier reconstruct it identically.
- **NB-M —** §8.1 key 4 requires the configuration object to carry `implementation_sha`, while §8.3 states that Commit A — which freezes the configuration — "cannot contain its own SHA". §8.3's next clause ("Commit B … records Commit A as `implementation_sha`") resolves it in favour of the runtime-emitted configuration, but a reader can stumble; one sentence distinguishing the frozen configuration template from the emitted configuration would close it.

---

## 5. Preserved evidence

1. Everything preserved by `6e408aec`, `3bd6b05f` and `91b1be14` remains valid.
2. Part A passes in full at this SHA: exact law quotations at correct lines, no untagged threshold, correct attributions, and all four source-SHA attestations verified by blob identity.
3. B1–B13 and NB-A–NB-I are verified closed. The verified substance should not be reopened: the exact ρ predicate with its two disjoint epsilons; the authorized comparator definition; the exact seed key with declared digest input; identity-tuple uniqueness with the formally defined and pinned collision count; the arm-scoped primitive-tape pipeline with its bit-for-bit baseline gate; the enumerated configuration, result, publication and payload schemas; the twelve rehearsals; honest backend-parity role naming; the carried-forward full-screen schema constraint; and paired same-seed parity grounded in Rebecca's ruling.
4. The fixture digest, sidecar, all fixture expectations, and the frozen-calibration digest are independently verified correct and unchanged.
5. Both negatives remain correctly named at full precision — native-calibration divergence at four of fifteen pairs (`0.7499937499999998`, `0.18749843749999995`, mean `0.1624986458333333`) and the two misspecification-profile coordinate disagreements.
6. All prior M3 evidence is untouched: no scoring, seeds 201–203 and 301–303 neither accessed nor rerun, retained INSTRUMENT FAILURE labels unchanged.

---

## 6. Routing

**Exact next authorized role: Rebecca R. McClintic.**

Rebecca alone decides whether to sign the `[PROPOSED]` criteria. If she signs, the contract becomes operative as a pre-registration; the TASK BUILDER is still not released by that act alone, and the full 19.2M full-screen GPU diagnostic additionally requires her explicit release under the GPU rebuild approval, which states that clearance does not auto-release it. The geometry-table freeze ruling separately records that TASK BUILDER release requires her explicit TASK BUILDER authorization as a distinct gate.

Items for Rebecca's awareness, none blocking: NB-J through NB-M above are clarity-class and may be closed in a later editorial pass or carried into the full-screen contract at her discretion. The CRITIC takes no position on whether to require them before signature.

### Explicitly prohibited actions (this review complied)

No scoring. No scoring-mode execution. No implementation or diagnostic execution. No re-run of any failed or prior run (O-14). No development run treated as an artifact (O-15). No hold-out, protected, courier, or scoring seed accessed, named, or exposed. No merge to `main` and no push to `main`. No G2–G4 freeze, no full-screen release, and no TASK BUILDER release. No edit to any specification, implementation, fixture, ruling, review under review, `STATE.md`, or the provenance log. No co-authoring, fixing, or modification of the work under review. No bar lowered, raised, renamed, reinterpreted, or silently replaced. No negative result renamed. No L15/L16/L17 work. No claim made on Rebecca's behalf, and no statement here should be read as her decision.

### Confirmation

No scoring was conducted. No run was rerun. No hold-out or protected seed was accessed or exposed. No merge or push to `main` occurred. Read-only git inspection only, plus commits to this `critic/` branch alone. Every quantitative claim was recomputed independently from committed artifacts; none rests on a commit message, changelog, or handoff attestation. This verdict is backed by the in-repo artifact named in the handoff and is not a clearance of anything beyond the reviewed specification.

---

## 7. Pre-push safety scan attestation

A pre-push self-scan was performed over this review artifact before pushing, per `PUBLIC_REPOSITORY_POLICY.md` §3 and §12, covering credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute filesystem paths, environment dumps, and PII.

**Findings: none.** This artifact contains only public repository SHAs, blob identifiers, branch names, repository-relative paths, quotations from committed repository documents, and numeric values recomputed from committed artifacts. The three `base_seed` values reported are derived from the pre-registered public sentinel coordinates by a public formula and are candidate-blind O-15 development values, not protected, hold-out, courier or scoring seeds; no protected seed value is named. No local, private, or transport path appears. Classification: no blocker, no Rebecca-decision item, no acceptable-exception item. Scan result: **clean**.
