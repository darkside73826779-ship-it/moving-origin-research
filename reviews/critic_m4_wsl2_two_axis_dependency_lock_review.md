# CRITIC review — M4 WSL2 two-axis and dependency-lock package

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

Gate served: narrow repository-quality review of diagnostic infrastructure only

## Exact intake and repository identity

- Substantive ref: `refs/heads/architect/m4-wsl2-two-axis-dependency-lock`.
- Routing head: `3c581604013b6db7e12762f0ab7f16cb01708a40`.
- Substantive review result: `8c303b3262d8ea7640e06fe23671f999f5e01d2c`.
- Base: `79473c93900405177e071d6eb56824ad1dcbf5e6`.
- Manifest ref/head: `refs/heads/architect/m4-wsl2-two-axis-dependency-lock-manifest` at `27c589f5cdfb92583840f9df576e1f6856466a1e`.
- Manifest: `handoffs/ARCHITECT_TO_COORDINATOR_M4_WSL2_TWO_AXIS_DEPENDENCY_LOCK.manifest.json`, raw SHA-256 `b0808eda62e24c4ffcafbdb9a1bab26c521d394f2107bc657c419d385a2f6e0e`.
- Package inventory: `specs/data/m4_wsl2_two_axis_dependency_lock_package_v1.json`.
- Review branch: `critic/m4-wsl2-two-axis-dependency-lock-review`.

Authenticated remote equality for both supplied refs was exact at intake. The canonical handoff manifest validates `VERIFIED` against `specs/data/common_handoff_manifest_schema_v1.json`. All 20 manifest artifact raw SHA-256 identities reproduce. All 18 ordered package-inventory entries reproduce path, mode, byte count, Git blob, and raw SHA-256. Each of the five listed artifact/sidecar pairs reproduces the artifact digest and exact basename. The routing-only range `8c303b3..3c58160` changes only the handoff. The helper-created isolated worktree was clean before review, and `git fsck --full --strict` and `git diff --check` returned clean.

## Verdict

- **LAW_FIDELITY: CLEAR**
- **DIAGNOSTIC INFRASTRUCTURE: BLOCK**
- **COMBINED VERDICT: BLOCK**

The committed retained-report projection is accurate for that one report, and the dependency exclusion is fail-closed. The reusable projection contract is not fail-closed for other schema-valid v1 reports, and the v2 schema does not enforce its advertised status/count/consumer semantics. This verdict is not a score, scientific interpretation, readiness ruling, merge decision, or project gate decision.

## Blocking findings

### BF1 — The derivation uses failure-code names outside the v1 schema and can erase schema-valid structural failures

Classification: deterministic projection / fail-closed classification defect.

Affected artifacts:

- `tools/testbed/derive_m4_wsl2_two_axis_report.py`, especially lines 13–23, 28, 33–35, and 50–51.
- `tests/test_m4_wsl2_two_axis_dependency_lock.py`, especially lines 70–77.
- The governing v1 failure-code enum in `specs/data/m4_wsl2_dual_model_probe_report_schema_v1.json`, lines 67–85.

Observed evidence:

- The derivation's `STRUCTURAL_FAILURES` contains names such as `ACTIVE_DURATION_TOO_SHORT`, `CLEANUP_INCOMPLETE`, `WINDOW_DROPPED`, and `WINDOW_COUNT_MISMATCH`. The v1 schema instead permits `ACTIVE_DURATION_SHORT`, `CLEANUP_VRAM_NONZERO`, and `DROPPED_WINDOWS`, and also permits `CHILD_PROCESS_FAILURE` and `SYNTHETIC_FIXTURE_ONLY`, which are absent from the derivation set.
- The derivation parses the source with `json.loads` but does not validate it against the bound v1 schema. It derives structural failure codes only by intersecting the source list with its mismatched local set.
- A schema-valid v1 `BLOCKED` report can therefore contain `CHILD_PROCESS_FAILURE` while retaining otherwise-good measured fields; the derivation will publish `structural_status: PASS` with an empty structural-failure list. The v1 schema's `BLOCKED` branch requires a nonempty valid failure-code list but does not require a bad measurement, so this is reachable within the declared source contract.
- The focused negative test injects `CLEANUP_INCOMPLETE`, which is not a valid v1 failure code, and also changes cleanup VRAM to a failing value. The metric independently produces BLOCK, so the test masks the taxonomy defect.

Impact: the retained report happens to derive correctly because its only failure is `OUTPUT_DIGEST_MISMATCH`, but the reusable v2 derivation can turn a schema-valid structural BLOCK into structural PASS. Consumers cannot treat this as a deterministic, fail-closed projection contract.

Smallest safe remediation: validate source input against the exact bound v1 schema; use the exact v1 failure-code taxonomy; conservatively classify every valid non-replica failure, including `CHILD_PROCESS_FAILURE` and `SYNTHETIC_FIXTURE_ONLY`; and reject unknown codes. Add schema-valid negative tests for every v1 failure-code branch, including a `CHILD_PROCESS_FAILURE` case whose numeric fields otherwise pass. Keep the retained report and its current projection byte-identical unless the corrected canonical serialization necessarily changes a governed derived artifact.

### BF2 — The v2 schema does not enforce projection invariants or mandatory exact-replica stop semantics

Classification: schema / consumer fail-closed defect.

Affected artifacts:

- `specs/data/m4_wsl2_dual_model_probe_two_axis_report_schema_v2.json` (line 1).
- `tools/testbed/derive_m4_wsl2_two_axis_report.py`, lines 50–56.
- `tests/test_m4_wsl2_two_axis_dependency_lock.py`, especially lines 35–45.

Observed evidence:

- The v2 schema checks field types, simple ranges, enums, and the literal consumer-rule string, but defines no conditional or cross-field constraints.
- It consequently permits semantically contradictory reports: `replica_consistency_status: MATCH` with nonzero mismatches; `MISMATCH` with zero mismatches; `NOT_RUN` with compared windows; mismatch-list length different from `mismatch_count`; agree plus mismatch counts different from compared count; `structural_status: PASS` with nonempty failure codes; and structural failure strings unrelated to the v1 taxonomy.
- The mismatch ordinal digest is not semantically verified against the ordinal list by any committed validator.
- Mandatory consumer behavior is represented only as the constant text `REQUIRE_REPLICA_MATCH_CONSUMER_MUST_STOP_UNLESS_MATCH`. The focused tests assert that text and schema-validity of the committed sample, but no committed consumer guard or semantic validator is exercised to reject/STOP on the contradictory states above.

Impact: a document can validate against the published v2 schema while contradicting the two-axis result or permitting an exact-replica consumer to proceed. A literal policy sentence is valuable metadata, but it is not an executable mandatory-stop boundary.

Smallest safe remediation: add schema conditionals for status/failure/count/list relationships and a canonical semantic validator for invariants JSON Schema cannot express conveniently, including count arithmetic, unique ordered in-range ordinals, ordinal-list digest equality, source binding, and exact v1 failure-code membership. Add and test a single consumer guard that returns STOP for every state other than `MATCH` whenever exact replicas are required. Negative tests must demonstrate rejection of each contradictory state rather than only acceptance of the committed sample.

## Checklist results and preserved evidence

- **Retained v1 report:** PASS. The committed artifact is 123,507 bytes with raw SHA-256 `7dde0d1587b9205a339776ad04daecfe2bf160e8ecb9ff0504335f91b57a10bc`, matching the previously published advisory identity. It retains `status: BLOCKED` and sole failure code `OUTPUT_DIGEST_MISMATCH`. The v1 producer and v1 schema are unchanged from base. The report was not present at the base commit, so preservation was checked against its published digest and committed package bindings rather than a nonexistent base-tree file.
- **Committed two-axis projection:** PASS for this retained input only. Independent derivation reproduced the committed 1,019 bytes exactly: structural `PASS`; replica `MISMATCH`; 164 compared, 80 agreeing, and 84 mismatching windows; and the mismatch-ordinal digest. BF1–BF2 block the reusable contract, not those retained measurements.
- **Mandatory replica consumer stop:** BLOCK under BF2. The policy text is explicit, but its required behavior is not enforced by the schema or an executable consumer boundary.
- **Dependency exclusion:** PASS. The package binds the resolver-observed optional distribution `torchaudio==2.11.0`, the expected `libcudart.so.13` import-failure marker, and absence from the final text-only environment. Setup uses `set -euo pipefail`, rejects wrong resolver identity or failure marker, removes only the identified unused distribution, and then requires exact direct-package versions, Python 3.12.3, absence of `torchaudio`, and successful `vllm` import. There is no adaptive fallback or broad package removal.
- **Focused and banked regressions:** SOURCE REVIEW PASS / LOCAL EXECUTION LIMITED. Shell syntax checks and Python compilation passed. The focused source contains the expected artifact, derivation, runtime-verifier, setup, readiness, and historical-test invocation coverage, but its structural negative case is insufficient under BF1. The current host lacks the pinned `jsonschema` dependency and has no Docker CLI, so the claimed 28-test pinned-container result could not be independently rerun without prohibited network acquisition. No dependency was installed.
- **Inventory and sidecars:** PASS. All manifest and inventory identities, sidecar bindings, LF bytes, modes, and routing ancestry reproduce.
- **Law, authority, and scope:** PASS. New design and data are explicitly `[PROPOSED]`; the package preserves the original report and BLOCKED disposition; exact-token equality is separated as a replica-consistency axis; structural transport/load evidence remains diagnostic; and no scientific bar, seed rule, model identity, custody permission, readiness permission, scoring authority, or existing hold changes.
- **Public safety:** PASS. Only committed public repository bytes and read-only validators were used. The package-range preflight produced 2,533 fixed-regex matches representing public numeric telemetry and hashes; manual classification found no credential, contact, private path/value, custody material, protected prompt/seed, or prohibited content. Gitleaks returned zero findings.

## Non-blocking findings

None beyond the blocking set.

## Exact disposition and next authorized role

Return this single combined BLOCK to **WORKFLOW COORDINATOR** for a narrow ARCHITECT remediation of BF1–BF2, followed by persistent-CRITIC rereview of one exact immutable package. Preserve the byte-identical retained v1 report, its legacy BLOCKED disposition, the synchronized transport/load evidence, and the narrow deterministic dependency exclusion.

No model rerun, network acquisition, protected input access, custody, scoring, scientific interpretation, readiness release, implementation outside this review record, merge, or project decision is authorized by this review.

## Public-safety and publication attestation

The review used only committed public repository material, static parsing, isolated temporary mutations of public JSON outside tracked project paths, and read-only repository validators. No model/tokenizer bytes were acquired or executed. No project workload, inference, private-input access, protected-seed access, custody, qualification, scoring, scientific interpretation, implementation, merge, or gate decision occurred.

Public-safety preflight over the complete package range returned 2,533 fixed-regex findings and zero Gitleaks findings. The fixed-regex matches were public numeric telemetry, timestamps, package/model/repository hashes, and other committed diagnostic metadata expected in the retained 123,507-byte public report. Preflight over the review range returned two fixed-regex findings representing the same required public base Git commit identity in commit-parent and combined-range scan domains, with zero Gitleaks findings. Manual classification found no prohibited material. Remote equality and worktree cleanliness will be reverified after publication.
