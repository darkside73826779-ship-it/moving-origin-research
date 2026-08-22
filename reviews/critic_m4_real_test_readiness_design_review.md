# CRITIC review — M4 real-test readiness design package

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

Gate served: repository-quality review of the immutable M4 real-test readiness design package only

## Exact intake and repository identity

- Substantive ref: `refs/heads/architect/m4-real-test-readiness-design-package`.
- Routing head: `1e125dd1cbd26bd6c15470a295f7d5efdba919e1`.
- Substantive design result: `4808271c2e2e649546bc77027bed31cba06507c9`.
- Base: `69ed2929881a2dd1f0721c934225235b2f7b0f75`.
- Manifest ref/head: `refs/heads/architect/m4-real-test-readiness-design-package-manifest` at `38725986f0823e8c1ac6250baa419a52d725ace8`.
- Manifest: `handoffs/ARCHITECT_TO_COORDINATOR_M4_REAL_TEST_READINESS_DESIGN_PACKAGE.manifest.json`.
- Review branch: `critic/m4-real-test-readiness-design-review`.

Remote equality for both supplied refs was exact at intake. The canonical handoff manifest validates `VERIFIED` against `specs/data/common_handoff_manifest_schema_v1.json`. Its ten listed artifact raw SHA-256 identities reproduce. The three JSON artifacts parse, contain 9 gates, 7 proposed contracts, and 7 ordered overlays respectively, and their adjacent sidecars exactly bind their raw LF bytes. The routing-only range `4808271..1e125dd` changes only the named handoff. The isolated helper-created worktree was clean before review.

## Verdict

- **LAW_FIDELITY: BLOCK**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

This is a repository-quality verdict on the design package, not a scientific result, scoring verdict, readiness ruling, merge decision, or project gate decision.

## First checklist item — law, source tags, and provenance

- **P1/P2:** No constitutional law is quoted in the new package, so there is no quoted-law byte diff to perform. The package does not reconstruct law text.
- **P3: BLOCK.** Constitutional §5.1 line 132 makes an untagged numeric threshold, kill condition, or test criterion review-blocking. The four new substantive design artifacts contain no recognized inline `[LAW-Lx]`, `[BAR-Entry n]`, `[OP-Entry n]`, or `[PROPOSED]` source tag at all. Examples include the 5%/`0.05` FWFP criteria, diagnostic seeds 101–105, retired-seed exclusions, and the 30-second matched-peer criterion in `specs/m4_real_test_readiness_design_v1.md` lines 33–38 and 84 and in the minified gate-map/catalog JSON. The underlying authorities are traceable, but an authority table is not the required inline source classification.
- **P4:** PASS. The new artifacts state date 2026-08-22 and Regime B.
- **P5:** No signed-law deviation is asserted. The later exact-peer amendment is cited through the model-ladder authority rather than silently treated as constitutional text.
- **P6:** Direct source checks reproduce the relevant durable records: provenance Entry 43 supplies the per-arm FWFP ceiling; current M4 spec §7.3 carries the approved milestone-wide extension; Entry 72 supplies the prospective fresh-seed L3 scoring gate; Entry 76 supplies candidate-blind/oracle-grounded/frozen tolerance and preserved downstream gates. The package's substantive values generally match those sources, subject to BF1 and BF2 below.

## Blocking findings

### BF1 — The gate map omits an already-committed terminal mutation review and therefore publishes stale authority identities

Classification: provenance/authority identity defect.

Affected artifacts:

- `specs/data/m4_real_test_readiness_gate_map_v1.json`, gate `G00_MUTATION_AND_JUDGE` and `G07_FINAL_IMPLEMENTATION_REVIEW` (line 1).
- `specs/data/m4_real_test_combined_tree_plan_v1.json`, overlay `POST_TOKENIZER_SEAM` (line 1).
- `specs/m4_real_test_readiness_design_v1.md`, lines 9, 24, 31, 52, and 72.

Observed evidence:

- The package says the corrected mutation apparatus and independent review are missing, leaves `MUTATION_CLEAR_SHA_UNBOUND`, and binds only the old implementation `909d2a4...`, JUDGE BLOCK `32f72c2...`, and remediation authority `64ec599...`.
- The committed remediation package already existed at `taskbuilder/m4-post-tokenizer-mutation-apparatus-remediation` @ `b751ef71b3f6c7dda126ce1a28af6f0d29b572dd`, with implementation `6d4089ef95a14fb6b1d46c96ebf452733ff5cd98` and terminal persistent-CRITIC COMBINED CLEAR `e67f0538640334e1db6b5397bce808f098d2e6ac`.
- The CLEAR commit timestamp is 08:56 EDT; the design result was committed at 09:03 EDT. The CLEAR explicitly stops at Coordinator for a new JUDGE cycle and does not itself decide readiness. Thus the safe current representation is “mutation remediation/review bound; new JUDGE ruling unbound,” not “corrected apparatus and review missing.”

Impact: the proposed route remains fail-closed because the new JUDGE ruling is still absent, but it fails the assignment's exact-authority and current-input requirements and would force a future constructor to ignore or rediscover already-valid public evidence.

Smallest safe remediation: revise G00, G07, the seam overlay, design narrative, sidecars, handoff, and manifest to bind the exact remediation package/result/review identities while leaving the new JUDGE result and downstream selection explicitly `UNBOUND`. Preserve the prior JUDGE BLOCK until that new JUDGE cycle rules.

### BF2 — The model-ladder authority names a nonexistent remote ref

Classification: repository identity defect.

Affected artifacts:

- `specs/data/m4_real_test_readiness_gate_map_v1.json`, authority `model_ladder` (line 1).
- `specs/data/m4_real_test_combined_tree_plan_v1.json`, overlay `MODEL_LADDER` (line 1).

Observed evidence:

- Both artifacts name `architect/m4-model-selection-ladder-rf1-rf2-remediation` at result `7a8239e9735042cddd94899ffaeaab53acf331fb`.
- Authenticated `git ls-remote` returns no such branch.
- The durable review names the actual ARCHITECT branch/head as `architect/m4-model-selection-ladder` @ `4e36466159744d622370ac0a9198cdf71836d354`, with substantive remediation result `7a8239e...`; the persistent review branch/head is `critic/m4-model-ladder-rf1-rf2-rereview` @ `d160080d8c798c52360a543cd9953ba1741ea8d4`.

Impact: a future immutable fetch using the declared ref must fail, so remote-ref equality and combined-tree construction are not executable as written.

Smallest safe remediation: replace the invented ref with the canonical remote ref and separately record routing head, substantive result, and review identity. Revalidate remote equality and all derived sidecars/manifests.

### BF3 — TESTBED_V1_2 and MODEL_LADDER do not define executable repository-path inventories

Classification: executability/internal-consistency defect.

Affected artifact: `specs/data/m4_real_test_combined_tree_plan_v1.json`, overlays `TESTBED_V1_2` and `MODEL_LADDER` (line 1); summarized as exact inventories in `specs/m4_real_test_readiness_design_v1.md` line 52.

Observed evidence:

- `TESTBED_V1_2` requires selection by “the immutable tag manifest,” but the immutable v1.2 tag contains no testbed repository-path manifest. Its `required_roots` mix individual files with directories and therefore do not fix an ordered path/mode/blob inventory.
- `MODEL_LADDER` requires the “exact active inventory in the canonical ladder manifest.” `specs/data/m4_model_ladder_manifest_v1.json` enumerates external checkpoint allow-files, not repository paths. The overlay's `required_roots` contain prefix-like strings such as `specs/data/m4_model_preflight_`, which require implementer glob/prefix interpretation.
- Two named MODEL_LADDER roots, `specs/m4_specification.md` and `specs/m4_specification_changelog.md`, are byte-different from the declared main base (18 added lines in total). The global rule says differing overlaps STOP without an explicit later-authority replacement, but no per-path replacement decision is supplied.

Impact: even after currently unbound gates close, an INTEGRATOR cannot deterministically select the testbed and ladder repository bytes or resolve known overlaps without inventing an inventory and precedence rule. This fails the package's claim of a deterministic path-selective construction order.

Smallest safe remediation: commit exact ordered repository inventories for both overlays, including path, mode, source Git blob, raw SHA-256, byte count, and sidecar pairing. Bind them to the tag object/peeled commit and ladder routing/result/review identities. Add explicit per-path overlap dispositions, especially for the M4 spec/changelog, or remove those paths from the overlay when the current-main bytes govern.

### BF4 — Binding thresholds and test criteria lack constitutional P3 source tags

Classification: law-fidelity/source-classification defect.

Affected artifacts:

- `specs/m4_real_test_readiness_design_v1.md`, especially lines 33–38 and 84.
- `specs/data/m4_real_test_readiness_gate_map_v1.json` (line 1).
- `specs/data/m4_real_test_readiness_contract_catalog_v1.json` (line 1).
- `specs/data/m4_real_test_combined_tree_plan_v1.json` where criteria/conditions are operationalized (line 1).

Observed evidence: a repository search across all four artifacts finds zero recognized source-class tags. The contract catalog serializes a locked `0.05` bar without a source tag; the gate map serializes the same threshold, seed exclusions, and the 30-second criterion without source-class members; the narrative likewise states these as requirements without inline tags.

Impact: the values are mostly faithful to existing authorities, but the package is not compliant with the binding versioned-law protocol and cannot safely distinguish locked, adopted, and still-proposed criteria. This is particularly material for the Qwen identity and 30-second smoke, which remain governed/non-scoring and cannot be presented as a signed scientific bar.

Smallest safe remediation: attach the exact permitted source classification to every numeric threshold, kill/test criterion, and machine-readable equivalent. Use only the actual repository authority; where no signed/adopted source exists, retain `[PROPOSED]` and the corresponding stop. Do not infer a stronger authority class.

## Checklist results and preserved evidence

- **Manifest, listed files, and sidecars:** PASS, apart from the substantive remote-ref defect in BF2. All package artifact hashes and sidecars reproduce.
- **Nine gates / seven contracts:** cardinalities PASS. L3, FWFP, tolerance, Q2/EF3, final `gofast`, final combined implementation review, and courier authorization remain explicitly unbound. G00 requires the BF1 current-evidence correction while the new JUDGE result remains unbound.
- **Engineering versus scoring:** PASS. Synthetic/schema/import/path checks and a future released matched-peer smoke are explicitly non-scoring. Protected inputs and official scoring remain behind G08 and all prior gates.
- **Immutable testbed:** tag object `1994709b41c8e108e0b6f9a15936681f596823af` is annotated and points to commit `11ea682a7f0fadfa1437a12d882402d90ffd0579`. The evidence boundary is faithfully non-scientific, subject to the missing path inventory in BF3.
- **Same-checkpoint/two-runtime peer design:** substantively faithful to the later exact-peer model-ladder authority. Candidate and peer remain distinct runtime/access instances of the exact same Qwen checkpoint; Q2/EF3 and model-use release remain blocked.
- **Parallel-CPU `gofast`:** PASS. Parallel CPU remains the sole authoritative L8 backend; native CUDA remains shelved/inoperative; serial `GO!` remains unauthorized; final implementation identity remains unbound.
- **Dependency ordering:** gate ordering is conservatively fail-closed and no scoring permission is introduced. The combined-tree overlay mechanics are BLOCKED by BF2–BF3.
- **Bars, seeds, model identity, and holds:** no value or hold is changed. The 5% per-arm/milestone-wide FWFP criteria, candidate-blind tolerance excluding diagnostic seeds 101–105, no-rerun treatment of retired seeds 201–203 and 301–303, exact-peer identity, Q2/EF3 hold, scoring hold, and Rebecca-only authorization boundaries are preserved. BF4 concerns mandatory source classification, not a detected numerical change.

## Non-blocking findings

None beyond the blocking set. Markdown hard-break lines trigger `git diff --check` trailing-whitespace notices, but the spaces are presentation-only and do not affect the verdict.

## Exact disposition and next authorized role

Return this single combined BLOCK to **WORKFLOW COORDINATOR**. The Coordinator should route one narrow package remediation to **ARCHITECT** covering BF1–BF4, then return the exact revised immutable package to the sole current persistent CRITIC. Prior valid evidence remains preserved. No TASK BUILDER, INTEGRATOR construction, JUDGE readiness decision, model/testbed executor, courier, scoring, or merge role is released by this review.

Explicitly prohibited: implementation; project workloads; model/tokenizer/private-custody access; prompt or protected-seed access; qualification or scoring; rerun; scientific interpretation; threshold/model/seed invention; state/provenance mutation; whole-branch merge; publication/merge decision; or project gate decision.

## Public-safety and execution attestation

The review used only committed public repository material and read-only validators/identity checks. No project workload was run. No private input, model/tokenizer byte, prompt, protected seed, custody path/value, or scientific output was accessed. No scoring, inference, implementation, state/provenance mutation, merge, or project decision occurred.

Public-safety preflight over the complete introduced routing-head-to-review range retained four fixed-regex findings representing two unique substrings scanned in both commit-parent and combined-range domains. Manual review confirmed both substrings occur wholly inside required public Git commit identities on lines 54 and 74; they are non-contact reproducibility metadata. Gitleaks 8.30.1 returned zero findings. No credential, personal contact, private path/value, custody material, model/tokenizer byte, prompt, seed, score, environment dump, or other prohibited content was found. Remote equality and worktree cleanliness will be reverified after publication.
