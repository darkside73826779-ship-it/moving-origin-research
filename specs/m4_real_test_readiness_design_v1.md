# M4 real-test readiness design v1

Status: **DESIGN ONLY — NOT READY — NO RUN OR MERGE AUTHORITY**  
Date: 2026-08-22 EDT  
Regime: B

## Purpose and non-authority

This package is a deterministic route map for closing the remaining M4 readiness gates. It does not clear a gate, resolve a seed, calibrate a tolerance, qualify Q2/EF3, bind a final `gofast` implementation, authorize custody, authorize a protected-seed run, authorize a merge, or declare readiness. The mutation remediation and terminal persistent-CRITIC CLEAR are banked; the prior JUDGE BLOCK remains operative until a new JUDGE cycle rules. Every `UNBOUND` value is an intentional fail-closed placeholder that must be replaced only by the named authority `[PROPOSED]`.

The machine-readable gate map is `specs/data/m4_real_test_readiness_gate_map_v1.json`; proposed deliverable contracts are in `specs/data/m4_real_test_readiness_contract_catalog_v1.json`; and the path-selective construction order is in `specs/data/m4_real_test_combined_tree_plan_v1.json`. Their adjacent SHA-256 sidecars bind their raw LF bytes.

## Immutable authority baseline

The package binds current main at `69ed2929881a2dd1f0721c934225235b2f7b0f75`, including the architectural constitution, M4 specification, M4 task specification, durable state, and the independent advisor audit. Additional exact authorities are:

| Subject | Immutable authority | Effect |
|---|---|---|
| Tokenizer PASS evidence | execution `e462e5bd61bcbad4eb03160129dec2e088de9892`; final CRITIC CLEAR `7274fbb1aef06d686efe07bb54b6828d0a5b41e2` | Evidence may be selected by exact paths; it is not a scoring authorization. |
| Post-tokenizer design | final design CLEAR `013af72e7dce566e7605d8e1e68fbfbf5d5cda28` | Design is banked, but implementation selection remains blocked by a new JUDGE cycle `[PROPOSED]`. |
| Post-tokenizer implementation | implementation package `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`; JUDGE BLOCK `32f72c2bb708d96060eb636cb4cf7a673c85ec24`; mutation authority `64ec5992eb4cb81ba75834c3f17db59b6226cce1`; remediation routing head `b751ef71b3f6c7dda126ce1a28af6f0d29b572dd`; remediation result `6d4089ef95a14fb6b1d46c96ebf452733ff5cd98`; persistent-CRITIC CLEAR `e67f0538640334e1db6b5397bce808f098d2e6ac` | Mutation review is complete; no seam overlay until a new JUDGE clearance binds an exact downstream selection `[PROPOSED]`. |
| WSL2 testbed | annotated tag `m4-wsl2-preexecution-testbed-v1.2`, tag object `1994709b41c8e108e0b6f9a15936681f596823af`, commit `11ea682a7f0fadfa1437a12d882402d90ffd0579` | Custody-free synthetic feasibility only; not scientific or protected-seed evidence. |
| Model ladder | canonical remote/routing head `architect/m4-model-selection-ladder` at `4e36466159744d622370ac0a9198cdf71836d354`; design result `7a8239e9735042cddd94899ffaeaab53acf331fb`; CRITIC CLEAR `d160080d8c798c52360a543cd9953ba1741ea8d4` | Qualification remains `BLOCKED_PENDING_BATTERY_SHA_AND_REBECCA_Q2_SIGNATURE` `[PROPOSED]`. |
| L8 backend | `handoffs/REBECCA_M4_CUDA_READY_HARNESS_CPU_L8_DIRECTIVE_2026-08-21.md` and `handoffs/REBECCA_L8_BACKEND_CODENAME_DIRECTIVE_2026-08-21.md` at current main | Parallel CPU `gofast` is the sole authoritative L8 policy. Native CUDA is shelved/inoperative; serial `GO!` is unauthorized. Final implementation SHA remains unbound. |

No conflict was found among these durable authorities. Missing identities are represented as stops, not inferred resolutions.

## Gate route

The exact nine-gate record G00–G08 is in the gate-map JSON `[PROPOSED]`. In order:

1. The banked mutation persistent-CRITIC CLEAR must be followed by a new JUDGE cycle that clears the post-tokenizer implementation `[PROPOSED]`.
2. The prospective L3 fresh-seed package must be resolved before scoring; retired seeds 201–203 and 301–303 are never rerun `[OP-Entry 72]`.
3. M4 FWFP closure must show no more than 5% per arm and no more than 5% milestone-wide `[BAR-Entry 43]`.
4. Tolerance must be candidate-blind, oracle-grounded, synthetic-calibrated, frozen before scoring, exclude candidate seeds 101–105, and receive Rebecca's explicit sign-off `[BAR-Entry 76]`.
5. Q2/EF3 remains blocked until an exact battery SHA and Rebecca Q2 signature exist, followed by the governed qualification and review.
6. The final parallel-CPU `gofast` implementation and its exact SHA/inventory must be reconciled and reviewed.
7. A matched-peer 30-second smoke may occur only after its engineering prerequisites clear. It uses two distinct runtime instances of the same exact Qwen/Qwen3-4B-Instruct-2507-FP8 checkpoint. It is non-scoring `[PROPOSED]`.
8. The combined implementation requires final persistent-CRITIC review and a JUDGE readiness ruling.
9. Only an exact courier authorization can release official protected-seed scoring.

Each gate record binds its owner, immutable authorities, missing deliverable, required input identities, output contract, reviewer, and deterministic stop conditions. The route is serial where an input is produced by an earlier gate; independent preparation is allowed only where the gate map says so.

## Engineering qualification versus official scoring

Engineering qualification includes schema checks, raw-byte and sidecar verification, custody-free synthetic fixtures, import/package checks, path-selective combined-tree construction, failure-path probes, and a released matched-peer 30-second smoke `[PROPOSED]`. The v1.2 observation is evidence that the testbed can support two same-checkpoint runtime instances under its published controls `[PROPOSED]`. It does not prove scientific validity, device-kernel overlap, model selection, Q2/EF3, or scoring readiness.

Official scoring begins only after every upstream gate is cleared and an exact courier packet is authorized. It alone may bind protected inputs, protected/fresh seeds, frozen tolerance, official per-arm and aggregate results, and scoring receipts. Engineering outputs must carry `protected_seed_absent=true` and `scientific_claims_absent=true`; they cannot be promoted by renaming or inference.

## Path-selective combined-tree design

The combined-tree plan forbids whole-branch merges. An INTEGRATOR may construct a future tree only in the declared seven-overlay order `[PROPOSED]`: current main; exact tokenizer PASS result and sidecar; the banked mutation package only after new JUDGE clearance; immutable testbed v1.2 inventory; exact model-ladder inventory; a future reviewed `gofast` inventory; then a deterministic `.gitattributes` union and complete raw-byte identity/sidecar cascade. Testbed and model-ladder inventories bind ordinal, path, mode, Git blob, raw SHA-256, byte count, sidecar pairing, base blob, and per-path overlap disposition `[PROPOSED]`. The model-ladder copies of `specs/m4_specification.md` and `specs/m4_specification_changelog.md` are explicitly excluded in favor of current-main bytes `[PROPOSED]`.

For every selected path, construction must verify that the source Git blob is reachable from the declared source SHA and equals the source inventory. Any overlapping path whose bytes differ without an explicit later-authority replacement rule is a STOP. The post-tokenizer and `gofast` selections intentionally remain `UNBOUND`; therefore construction cannot begin from this design package. No artifact in this package authorizes a merge.

## Proposed deliverables

The contract catalog fixes filenames, statuses, required fields, owner/reviewer route, and stop conditions for:

- `specs/data/m3_l3_fresh_seed_resolution_request_v1.json`, its schema, and `artifacts/m3_l3_fresh_seed_resolution_package_v1.json`
- `audits/m4_fwfp_closure_audit_v1.json`
- `specs/data/m4_tolerance_calibration_signoff_packet_v1.json`
- `specs/data/m4_q2_ef3_battery_release_qualification_packet_v1.json`
- `specs/data/m4_gofast_final_sha_reconciliation_v1.json`
- `specs/data/m4_matched_peer_30s_qualification_smoke_request_v1.json` and its sanitized result
- `specs/data/m4_final_courier_scoring_packet_v1.json`

These are proposed contracts, not created operational artifacts. They contain no invented seed, battery SHA, tolerance, command, private path, custody value, or authorization.

## Work possible now and work that must wait

Custody-free work possible after the appropriate implementation handoff includes implementing public schemas and validators from a cleared design, unit and synthetic-fixture testing, raw Git-blob/sidecar verification, reproducible archive verification, and combined-tree conflict simulation against declared public SHAs. The current package authorizes none of that implementation; it merely identifies it.

Work that must wait includes post-tokenizer selection pending a new JUDGE clearance; L3 resolution; Rebecca tolerance sign-off; battery SHA and Q2 signature; any private custody binding; protected/fresh seed disclosure or use; real tokenizer/model access; official scoring; publication; merge; and gate decisions. The matched-peer smoke also waits for exact combined-tree, rung, and `gofast` releases even though it is non-scoring `[PROPOSED]`.

## Advisor and archive hygiene

All testbed citations must name both annotated tag `m4-wsl2-preexecution-testbed-v1.2` and peeled commit `11ea682a7f0fadfa1437a12d882402d90ffd0579`; a moving branch name is insufficient. No dependency redesign or duplicate environment setup is permitted.

A downloadable advisor archive may be admitted only if a Coordinator publication binds an exact archive filename, archive SHA-256 sidecar, source tag object, peeled commit, ordered member inventory, Git modes, and a fresh extraction verification showing LF bytes for every governed text member and sidecar verification after extraction. Until such a publication exists, the immutable Git tag is the sole bound distribution identity. This package intentionally invents neither an archive digest nor a download command.

## Preserved bars and holds

The per-arm and milestone-wide FWFP ceiling is 5% `[BAR-Entry 43]`. Candidate seeds 101–105 are excluded from tolerance calibration `[BAR-Entry 76]`. Retired seeds 201–203 and 301–303 are never rerun `[OP-Entry 72]`. L3 requires the prospective fresh-seed resolution route `[OP-Entry 72]`. Q2/EF3 and native L8 remain held as stated above. Candidate and peer are distinct runtime/access instances of the same checkpoint and training identity, not different scientific model families `[PROPOSED]`. No rerun, protected-seed use, scoring, science, custody access, state/provenance mutation, publication, merge, or gate decision is authorized.
