# ARCHITECT → WORKFLOW COORDINATOR: M4 real-test readiness BF1–BF4 remediation

Date: 2026-08-22 EDT

Regime: B

Terminal state: COMPLETE — DESIGN ONLY / NOT READY / NOT AUTHORIZED

## Result

The four CRITIC findings at `845cabe416bdcf5073f14cb7fb69d13dba7743bd` are remediated in one design-only batch `[PROPOSED]`.

- BF1: binds mutation remediation routing head `b751ef71b3f6c7dda126ce1a28af6f0d29b572dd`, result `6d4089ef95a14fb6b1d46c96ebf452733ff5cd98`, and persistent-CRITIC CLEAR `e67f0538640334e1db6b5397bce808f098d2e6ac`; the new JUDGE ruling remains `UNBOUND` and the prior JUDGE BLOCK remains operative `[PROPOSED]`.
- BF2: binds canonical remote/routing ref `architect/m4-model-selection-ladder` at `4e36466159744d622370ac0a9198cdf71836d354`, independently reproduced result `7a8239e9735042cddd94899ffaeaab53acf331fb`, and review `d160080d8c798c52360a543cd9953ba1741ea8d4` `[PROPOSED]`.
- BF3: adds ordered exact inventories for twenty testbed paths and forty-six model-ladder paths, including mode, Git blob, raw SHA-256, byte count, sidecar pairing, base blob, and overlap disposition `[PROPOSED]`. The two differing ladder overlaps, `specs/m4_specification.md` and its changelog, explicitly retain current-main bytes and exclude ladder-source bytes `[PROPOSED]`.
- BF4: adds inline and machine-readable P3 classifications. The FWFP ceiling is 5% `[BAR-Entry 43]`; candidate diagnostic seeds 101–105 and tolerance criteria are `[BAR-Entry 76]`; retired-seed no-rerun and prospective L3 sequencing are `[OP-Entry 72]`; package-introduced counts, order, smoke, negative, and construction criteria remain `[PROPOSED]`.

## Immutable identity

- Base package routing head: `1e125dd1cbd26bd6c15470a295f7d5efdba919e1`
- Remediation result: `ae1cd578f3e5f2211480f73205a618710ba02319`
- Branch: `architect/m4-real-test-readiness-design-bf1-bf4-remediation`
- Authority review: `critic/m4-real-test-readiness-design-review` at `845cabe416bdcf5073f14cb7fb69d13dba7743bd`

## Complete substantive raw Git-blob inventory

Format: `path | mode | bytes | Git blob identity`.

```text
.gitattributes | 100644 | 3988 | 87c9a4e2d91408213823b006e9fa1ed9428e4ef4
specs/data/m4_real_test_combined_tree_plan_v1.json | 100644 | 4814 | 6486a08fd2e1d1a1bb793a1503ec7964f97780e6
specs/data/m4_real_test_combined_tree_plan_v1.json.sha256 | 100644 | 106 | fa8ca95ed8da1a314252e7fc28ab16910d35e49b
specs/data/m4_real_test_model_ladder_overlay_inventory_v1.json | 100644 | 17790 | bc1f81a4583c815cf6a34e7b9da200fb2441e63e
specs/data/m4_real_test_model_ladder_overlay_inventory_v1.json.sha256 | 100644 | 118 | 2ada3d4b9fccf5a4da0829368a5175c358f5ec77
specs/data/m4_real_test_readiness_contract_catalog_v1.json | 100644 | 5713 | da7daea42aa1b332cd9702b5d10b8ac4e0b981d4
specs/data/m4_real_test_readiness_contract_catalog_v1.json.sha256 | 100644 | 114 | ba21976109acacdf2bab2032b31703eadf4181c6
specs/data/m4_real_test_readiness_gate_map_v1.json | 100644 | 10784 | 81bcf1488cf6ec29e241924b62b73e5c85b8bc2e
specs/data/m4_real_test_readiness_gate_map_v1.json.sha256 | 100644 | 106 | 1b3e51ac84ed64cbb77d2d2f63b857f1e2c9d2bd
specs/data/m4_real_test_testbed_v1_2_overlay_inventory_v1.json | 100644 | 7850 | e743f794a0fbeeb0e5e2c00819c8de47c91f2817
specs/data/m4_real_test_testbed_v1_2_overlay_inventory_v1.json.sha256 | 100644 | 118 | 9e9c64cdd9f41bf4ca2c6809a7d8d69473116af5
specs/m4_real_test_readiness_design_v1.md | 100644 | 10565 | 06d21596f374867c3c6645767e981b9bbf8649aa
```

## Verification boundary

All inventory entries were independently reproduced from source Git objects. Source refs and authority paths were authenticated and read. JSON parsing, source-tag presence, sidecars, LF attributes, ordered ordinals, sidecar pairs, overlap dispositions, and raw identity replay passed. No WSL2 feasibility operation, implementation, model/tokenizer/custody access, protected seed, scoring, merge, readiness declaration, state/provenance mutation, or gate decision occurred.

Ownership transfers only after Coordinator acknowledges this direct handoff.
