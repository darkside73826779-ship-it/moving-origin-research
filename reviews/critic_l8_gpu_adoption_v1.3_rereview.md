# CRITIC Re-Review — L8 GPU Diagnostic-Backend Adoption Specification v1.3

**Date:** 2026-08-21 · **Regime:** B (post-Entry 81; `docs/ARCHITECTURAL_CONSTITUTION_v2.md` §5 binding) `[P4]`

**Gate served:** Fresh-context CRITIC re-review of the ARCHITECT's B10–B12 / NB-A–NB-F remediation of the L8 GPU diagnostic-backend equivalence contract — Part A (law fidelity, source tags, provenance/source-SHA verification) then Part B (substantive falsification).

**Reviewer:** CRITIC (independent adversarial review; did not co-author, fix, or modify any artifact under review)

**Additive to:** `reviews/critic_l8_gpu_adoption.md` @ `6e408aec` and `reviews/critic_l8_gpu_adoption_v1.2_rereview.md` @ `3bd6b05f`. Preserved evidence in both stands.

---

## 1. Verdicts

| Result | Value |
|---|---|
| `LAW_FIDELITY` | **PASS** |
| `SUBSTANTIVE` | **BLOCK** |
| **Combined CRITIC ruling** | **BLOCK** |
| Next authorized recipient | **ARCHITECT only** |

**All twelve prior blocking findings (B1–B12) and all six non-blocking findings (NB-A–NB-F) are verified closed.** The remediation is accurate and does not over-claim: every bullet in the v1.3 changelog was checked against the diff and each is true.

The block rests on **one** finding, **B13**, newly surfaced by tracing the executable paths of the now-concrete contract: a mandatory, failure-producing determinism gate depends on a digest whose input domain the specification never defines. It is narrow and cheap to fix. Nothing else stands between this contract and clearance.

---

## 2. Inputs and SHAs reviewed

| Item | Value | Verification |
|---|---|---|
| Required base | `b6d4556021ad38199d3bfa90fdb3ef9a99988790` | **verified ancestor**; no file present on main is missing from the result tree |
| Result SHA reviewed | `933f513bbb5847b314368f568d08f02829526745` | reviewed |
| Prior reviewed SHA | `678af9b9c80b1f22cf65b2bacc4901ad06450856` (v1.2) | delta reviewed |
| Remediation commits | `3fea745` (remediate), `933f513` (route) | inspected against file contents |
| Specification v1.3 | `specs/l8_gpu_diagnostic_backend_adoption_spec_v1.3.md` | reviewed in full |
| Changelog | `specs/l8_gpu_diagnostic_backend_adoption_spec_CHANGELOG.md` | every v1.3 bullet verified against the diff |
| Known-good fixture + sidecar | `specs/data/l8_gpu_adoption_known_good_v1.json` (+ `.sha256`) | digest verified; all expectations recomputed |
| Frozen calibration | `specs/data/l8_cpu_frozen_calibration_v1.json` | digest re-verified unchanged |
| Controlling CPU spec package (4 files) | attested source `2082680a7caba85c46e637b3b38d679fa7f80599` | **all four byte-identical to `2082680`** |
| Item-1 ρ authorization | attested source `69feed8d…` | byte-identical |
| Geometry-table freeze ruling | attested source `5306c302…` | byte-identical |
| GPU rebuild approval | at base `b6d4556` | present in-tree; read in full |
| CPU baseline | `b1397498…` | inspected (seed derivation) |

Every quantitative claim below was recomputed independently from committed artifacts. Nothing rests on a commit message, changelog, or handoff attestation. Git operations were read-only except commits to this `critic/` branch.

---

## 3. Part A — Law fidelity: `LAW_FIDELITY: PASS`

### 3.1 Law-diff (P1, P2) — PASS

Re-extracted and compared character-for-character at the result SHA: L8 → `docs/ARCHITECTURAL_CONSTITUTION_v2.md:28` **exact**; L18 → `:54` **exact**; L19 → `:55` **exact**. Cited line numbers correct. No constitutional text reconstructed.

### 3.2 Source-class tags (P3) — PASS

A line-by-line scan for numerics lacking an allowed tag returned only the document date, the two operative-ruling citations whose `[PROPOSED]` tags were deliberately removed under NB-E (these carry commit SHAs, not thresholds), and the §8.1 enumerated key list, which is covered by its explicit sweep sentence. **No untagged threshold exists.**

Attribution remains correct. `beta_star ≥ 0.2`, `rho ≥ 0.8`, `≥ 3 doses`, `5 seeds` and the specificity control are `[BAR-Entry 11]`, all five traceable to the M0 decision sheet's L8 row. The new `RHO_TEST_VALUE_EPS` is correctly `[PROPOSED]` and correctly kept distinct from the `[BAR-Entry 11]` predicate it does not govern. O-14 remains `[OP-Entry 22]` at §6.

### 3.3 Provenance and source-SHA verification (P6) — PASS

All four §2 attestations now verify by blob identity:

| §2 item | Attested source | Result |
|---|---|---|
| 1 — GPU rebuild approval | at base `b6d4556` | present in-tree |
| 2 — Item-1 ρ authorization | `69feed8d…` | **byte-identical** |
| 3 — Geometry-table freeze | `5306c302…` | **byte-identical** |
| 4 — Controlling CPU spec package | `2082680…` | **byte-identical, all four files** |

`specs/data/l8_cpu_frozen_calibration_v1.json` still hashes to `f012849c57f7aadac3af69a345572674a6fdcc3de5eaf9eb642973b7d3cdfb5e` as §2 item 6 states.

**B10 is closed.** Part A therefore passes and substantive review was authorized to proceed.

---

## 4. Blocker closure — verified against the diff

### B10 — CLOSED

The in-tree controlling package is now byte-identical to `2082680` across all four files: `specs/l8_g2g4_minimal_full_screen_spec.md`, its `CHANGELOG`, its `EXECUTABILITY_TRACE`, and its `TASKBUILDER_HANDOFF`. `RHO_COMPARE_EPS` now appears five times in the in-tree controlling spec (previously zero) and case 2a is present (previously absent). Decisively, the in-tree contradiction is gone — line 173 now reads:

> **Adjacent-inversion / threshold case:** `D̄ = [1, 0, 2, 3]` → response ranks `[2,1,3,4]` → `ρ_s = 0.8` (computed `0.7999999999999999`, the binary64 roundoff of exactly `0.8`) → **passes** the ρ predicate via `abs(ρ_s - 0.8) <= RHO_COMPARE_EPS` (at the locked threshold).

This agrees with the digest-verified fixture and with §3. The tree, the fixture, the controlling specification and Rebecca's directive now say the same thing at the locked 0.8 boundary. `cpu_spec_sha` in §8.1 key 7 now describes an artifact that is actually in the tree.

### B11 — CLOSED

§3 adds `RHO_TEST_VALUE_EPS = 1e-12`, scoped explicitly to "deterministic-test value comparison only", and a new paragraph:

> Deterministic finite-rho value checks pass iff `abs(observed_rho - expected_rho) <= RHO_TEST_VALUE_EPS`. This comparison is distinct from `RHO_COMPARE_EPS`: it accommodates valid binary64 evaluation-order differences such as `0.7999999999999998`, `0.7999999999999999`, and `0.8`, while predicate outcomes must still be exactly identical. Undefined expected rho passes the value check only when observed rho is also undefined.

The fixture carries the matching `"rho_value_compare_epsilon": 1e-12`, and its digest and sidecar were updated consistently. Verified by recomputation: each of the three orderings I demonstrated in the prior review sits `1.11e-16` or `0` from the pre-registered literal, well inside `1e-12`, and all three pass the ρ predicate — so the deterministic test is now decidable without touching predicate parity. The no-softening guard is unaffected and still bites: `direct_rho = 0.799999999998` is exactly `2 × RHO_COMPARE_EPS` below the bar and correctly **fails** the predicate. Two epsilons of the same magnitude with disjoint jobs is the right structure, and the value chosen matches the mitigation the controlling specification itself suggested.

### B12 — CLOSED

§5 now states the digest input exactly, and it matches `b139749:diagnostics/l8_power_analysis.py:161` character-for-character:

`key = f"alpha={alpha:.6f}|vmult={v_mult:.6f}|cmin={c_min:.6f}|eta={eta:.6f}"`

with an explicit binding clause: "The six-decimal formatting, field names, separators, field order, and lowercase spellings are digest input and may not vary." §8.1 key 14 records the literal formula string. The offset relation `seed_int = (base_seed + i*5 + s) mod 2^31` continues to match the baseline exactly.

### NB-A through NB-F — all CLOSED

- **NB-A** — §7 is retagged `[PROPOSED]` and now says plainly: "These are backend-parity roles, not renamed L18 controls." The `[LAW-L18]` mis-attribution is gone; the L18 preservation paragraph is retained.
- **NB-B** — §6 now reads "six rho categories plus the no-softening subtest, and four complete-verdict cases … cover the controlling CPU specification's seven deterministic categories plus case 2a". Verified against the fixture: `rho_cases` has 7 rows (6 categories + `no_softening`) and `complete_verdict_cases` has 4. The arity statement is now correct and coverage remains complete.
- **NB-C** — Both halves fixed. §8.1 key 14 pre-registers `expected_derived_seed_collision_count=3840`, and §10 makes it a hard gate with its derivation, any other count being `INSTRUMENT_FAILURE`. Independently recomputed from the §5 formula: `base_seed` values are `975924316`, `401917689`, `444671194`; no range wraps `2^31`; **zero** cross-cell overlap on all three pairs; and the count is `3840` under every plausible reading of "collision count" (distinct colliding values, extra occurrences, and unordered pairs all equal 3840). The hard equality gate is therefore well-founded and the metric's residual definitional ambiguity is moot for this exact sentinel. Separately, the tape is now "arm-scoped" with the sharing question answered explicitly: "Combo and null tapes are not shared: the null arm follows the baseline by consuming no `xi_l` draws and storing positive-zero `xi_l` values, while the combo arm consumes positive-dose `xi_l` draws in baseline order."
- **NB-D** — §8.2 now enumerates the cell keys in order: `cell_ordinal`, `alpha`, `v_mult`, `c_min`, `eta`, `base_seed`, then `arms`.
- **NB-E** — `[PROPOSED]` removed from the two operative-ruling citations and from the observed negative in §10, which is now correctly described as "an observed named negative".
- **NB-F** — §10 now carries the constraint forward explicitly: "Any later full-screen GPU run remains bound to the controlling §7.1 schema, field order, types, NaN-to-null handling, atomic write, and output paths `diagnostics/l8_g2g4_minimal_full_screen.json` and `diagnostics/l8_g2g4_minimal_full_screen_HANDOFF.md`. This equivalence-packet schema does not replace or amend that full-screen contract." This matches Rebecca's binding equivalence constraint verbatim in substance.

### Changelog accuracy — verified, no over-claim

Each of the ten v1.3 changelog bullets was checked against the diff and each is true. The closing assertion — "No locked bar, law quotation, calibration value, geometry, control, negative name, or authorization boundary changed" — holds: law text byte-identical, `0.2` / `0.8` / `≥3 doses` / `5 seeds` / specificity intact, calibration digest unchanged, geometry table untouched, both negatives retained at full binary64 precision.

---

## 5. Part B — Substantive: `SUBSTANTIVE: BLOCK`

### B13 — Spec defect (blocking): the "canonical scientific payload" is never defined, yet gates a failure-producing determinism check

Three binding provisions depend on this object:

- §6: "After removal of runtime metadata, the second canonical scientific payload must be byte-identical to the first. Failure produces `INSTRUMENT_FAILURE`; no third execution is permitted."
- §8.2: each of the two `runs` rows carries `scientific_payload_sha256`.
- §9 case 9 (`completion_order_shuffle`): "expect identical canonical scientific payload."
- §10 gates `EQUIVALENT_FOR_O15_DIAGNOSTICS` on "repeat-payload equality".

Neither "scientific payload" nor the "runtime metadata" that must be removed is defined anywhere in v1.3, and the controlling CPU specification at `2082680` contains no such definition either — a search for `payload`, `runtime metadata`, and `canonical` across both documents returns only the four gating uses above plus §8's general RFC 8785 sentence. The implementer must therefore invent the digest's input domain, and the candidate fields sit immediately adjacent to it: `elapsed_seconds` is in the same `runs` row, while `numpy_version`, `torch_version`, `cuda_runtime_version`, `gpu_model`, `producer_worker_count` and `derived_seed_collision_count` are in `header`.

The consequences are asymmetric and both bad:

- Include `elapsed_seconds` (or any timing/environment field) and run 0 can never equal run 1, so the sentinel is **guaranteed** to terminate as `INSTRUMENT_FAILURE` and O-14 forbids a third execution. This is the same failure geometry as the original B3.
- Exclude too much — for example the arm-level counts and predicate-parity flags — and the determinism check becomes toothless while still reporting as passed.

§8 fixes canonicalization (RFC 8785) and key order but not *which object* is canonicalized for this digest, so the RFC 8785 requirement does not close the gap. This is squarely the "every published artifact's exact schema, field order, canonicalization, and expected SHA-256 must be fixed in the spec; if left to the implementer, BLOCK" condition of the binding executability standard, and a determinism gate whose input set an implementer chooses is not a pre-registration.

The remedy is the ARCHITECT's to choose, not the CRITIC's. Enumerating the exact field set that enters `scientific_payload_sha256` — or equivalently naming the exact excluded runtime-metadata keys — closes it.

**Classification:** spec defect (executability; undefined digest domain in a mandatory pass/fail gate).

### Substantive checks that did NOT block

- **Executability trace of every other implementer input is now complete.** The rehearsal fixture is concrete (geometry `(W=100, N_w=16)`, `Q_per_dose=1600`, three exact cells with ordinals, 256 repetitions per cell per arm, five seeds, combo-then-null ordering, sigma source per arm, exact RNG identity and seed formula, primitive-tape shapes `(4,N_w,W)` and their recording boundary, block size 32, worker and queue formulas). The committed artifact pair exists with a verified digest and a specified sidecar byte format. The stochastic realization is fixed by an exact RNG algorithm, seed derivation, draw shapes and construction order rather than by a distribution. Result schemas and orderings are enumerated. The only remaining undefined executable input is B13.
- **Fixture integrity and every expectation re-verified.** The fixture blob hashes to `65256ff48fb48399536c3e499242400267aa044459d247a9ecc51eb77e6cd7f7`, matching both §6 and the updated sidecar. `perfect_increasing` → `1.0`; `tied_responses` → `0.9486832980505138` (= `sqrt(0.9)`); `constant_responses` and `nonfinite_without_apparatus_fault` → undefined with predicate `false`; `decreasing_responses` → `-1.0`, predicate `false`; `no_softening` correctly fails at exactly `2 × RHO_COMPARE_EPS`. All four `complete_verdict_cases` reproduce, including `undefined_rho` → false-kill `true`.
- **Sentinel arithmetic re-verified.** `3 × 2 × 256 = 1,536` repetitions and `× 5 = 7,680` logical seeds as §6 states; `256 mod 32 = 0`, so §5's claim that no partial batch can arise holds; `Q_per_dose = N_w × W = 1600`, consistent with the tape shape.
- **The paired-parity model remains correctly grounded** in Rebecca's operative ruling, which requires the GPU path to "reproduce the CPU path's per-seed `β*` and `ρ` values for identical seeds — bit-for-bit, or provably-equivalent within the locked-bar comparison tolerance (`RHO_COMPARE_EPS = 1e-12`)". §4's rule that "A numeric value within tolerance but producing a different predicate boolean is `NOT_EQUIVALENT`" continues to foreclose any silent bar movement, and the new `RHO_TEST_VALUE_EPS` does not weaken it because predicate outcomes must still be exactly identical.
- **Sentinel coverage still matches the ruling's required equivalence packet item-for-item**: the seven deterministic categories plus 2a, combo and null arms, tie case, boundary ρ, zero-variance ρ, non-finite/apparatus path, three ordinary cells, and a repeat run for determinism.
- **Sentinel geometry remains legitimate** under the signed freeze: `(W=100, N_w=16)` is inside the frozen sets and touches no tested boundary.
- **No-relabeling, apparatus-failure exclusivity, the twelve rehearsals, the two-commit identity, and the publication/recovery semantics are unchanged** from v1.2 and remain sound. Scope discipline holds: §11's prohibitions are intact and TASK BUILDER remains held.
- **Repository safety.** A private-path, credential and machine-identifier scan across every file changed between `678af9b9` and `933f513` returned zero hits.

### Non-blocking findings

- **NB-G —** The fixture's pinned digest is a digest of the committed file bytes (verified as such, with `.gitattributes` pinning LF), while §8 requires RFC 8785 canonical bytes for "all JSON". The committed sidecar resolves the intent operationally, but §6 should say explicitly that the fixture and calibration digests are committed-file digests rather than canonical-form digests, as §2 item 6 already does for the calibration artifact.
- **NB-H —** NB-E is closed for the two citations it named, but §2 item 1 — Rebecca's operative, signed, merged-to-main GPU rebuild approval — still carries `[PROPOSED]`. Item 4's `[PROPOSED]` is defensible since `2082680` is an unmerged specification, but an operative Principal ruling should not be tagged as a proposal.
- **NB-I —** `derived_seed_collision_count` is pinned to a required value and its derivation is given, but the metric itself is still described only as "equal derived integers from distinct tuples". For this sentinel every reading yields 3840, so nothing is at risk here; stating it as a formula would make the gate portable to a future sentinel where the readings diverge.

---

## 6. Preserved evidence

1. Everything preserved by `6e408aec` and `3bd6b05f` remains valid.
2. Part A of this re-review passes in full: exact law quotations, no untagged threshold, correct attributions, and all four source-SHA attestations verified by blob identity.
3. B1–B12 and NB-A–NB-F are verified closed. None of that work should be reopened: the exact ρ predicate and its two disjoint epsilons, the authorized comparator definition, the exact seed key, identity-tuple uniqueness with the pinned collision count, the arm-scoped primitive-tape pipeline with its bit-for-bit baseline gate, the enumerated schemas and publication semantics, the twelve rehearsals, honest backend-parity role naming, and the carried-forward full-screen schema constraint.
4. The fixture's digest, sidecar and all expectations are independently verified correct; the frozen-calibration artifact is unchanged and re-verified.
5. Both negatives remain correctly named at full precision — native-calibration divergence at four of fifteen pairs (`0.7499937499999998`, `0.18749843749999995`, mean `0.1624986458333333`) and the two misspecification-profile coordinate disagreements. Native GPU calibration and torch-native RNG remain unadopted.
6. All prior M3 evidence is untouched: no scoring, seeds 201–203 and 301–303 neither accessed nor rerun, retained INSTRUMENT FAILURE labels unchanged.

---

## 7. Routing

**Exact next authorized role: ARCHITECT** (and only the ARCHITECT), to close **B13** and, if it chooses, NB-G–NB-I. B13 is a single enumeration: define the exact field set entering `scientific_payload_sha256`, or equivalently name the exact runtime-metadata keys excluded from the repeat comparison.

On remediation the contract returns through a fresh-context CRITIC (Part A then Part B) before Rebecca. TASK BUILDER remains held; the full-screen GPU execution additionally requires Rebecca's explicit release, which this specification does not and cannot supply.

### Explicitly prohibited actions (this review complied)

No scoring. No scoring-mode execution. No implementation or diagnostic execution. No re-run of any failed or prior run (O-14). No development run treated as an artifact (O-15). No hold-out, protected, courier, or scoring seed accessed, named, or exposed. No merge to `main` and no push to `main`. No G2–G4 freeze and no full-screen release. No edit to any specification, implementation, fixture, ruling, review under review, `STATE.md`, or the provenance log. No co-authoring, fixing, or modification of the work under review. No bar lowered, raised, renamed, reinterpreted, or silently replaced. No negative result renamed. No L15/L16/L17 work. No claim made on Rebecca's behalf.

### Confirmation

No scoring was conducted. No run was rerun. No hold-out or protected seed was accessed or exposed. No merge or push to `main` occurred. Read-only git inspection only, plus commits to this `critic/` branch alone. Every quantitative claim was recomputed independently from committed artifacts; none rests on a commit message, changelog, or handoff attestation.

---

## 8. Pre-push safety scan attestation

A pre-push self-scan was performed over this review artifact before pushing, per `PUBLIC_REPOSITORY_POLICY.md` §3 and §12, covering credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers (hostnames, MAC addresses, SIDs, user account names), private absolute filesystem paths, environment dumps, and PII.

**Findings: none.** This artifact contains only public repository SHAs, blob identifiers, branch names, repository-relative paths, quotations from committed repository documents, and numeric values recomputed from committed artifacts. The three `base_seed` values reported are derived from the pre-registered public sentinel coordinates and are candidate-blind development values, not protected, hold-out, courier or scoring seeds; no protected seed value is named. No local, private, or transport path appears. Classification: no blocker, no Rebecca-decision item, no acceptable-exception item. Scan result: **clean**.
