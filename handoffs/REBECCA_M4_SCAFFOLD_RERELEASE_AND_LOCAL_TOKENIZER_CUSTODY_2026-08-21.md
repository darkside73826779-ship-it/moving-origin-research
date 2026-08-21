# Rebecca M4 Scaffold Re-release and Local Tokenizer-Custody Decision

Date: 2026-08-21
Regime: B
Authority class: Principal implementation re-release and local-custody authorization

## Decisions

Rebecca R. McClintic made three separate decisions:

1. **Scaffold re-release: APPROVED.** TASK BUILDER may implement the exact persistent-CRITIC-cleared M4 model-agnostic scaffold-with-stubs contract identified below.
2. **Q2 numeric informative band: DEFERRED.** The proposed values remain unsigned and inoperative pending an explanation to Rebecca. No role may treat the proposed Q2 values as approved.
3. **Local tokenizer materialization: APPROVED.** The authorized executor may read the locally held Qwen tokenizer artifact solely to derive the committed contract's context token arrays and record sanitized lengths and SHA-256 digests. Tokenizer/model bytes and local paths remain prohibited from Git/GitHub.

## A. Scaffold implementation re-release

### Exact cleared inputs

- ARCHITECT branch/head: `architect/m4-model-agnostic-scaffold` @ `ade99fc13dc750b789d254316b9a7dc5de2eae8b`
- Specification result: `7f3db1f9552cf87de205b0635882402e0e1be5d4`
- Persistent-CRITIC CLEAR: `critic/m4-scaffold-cf1-cf3-rereview` @ `deb49bb342a39d3ec25834a4a59b5b21a697d966`
- Review: `reviews/critic_m4_scaffold_cf1_cf3_rereview.md`

### Released scope

TASK BUILDER may implement and run only the exact synthetic scaffold tests prescribed by the cleared contract. The release covers the model-neutral candidate/peer adapters, CUDA-ready model/harness interfaces, synchronized host boundary to authoritative parallel-CPU L8 (`gofast`), deterministic synthetic stubs and fixtures, lifecycle behavior, validation/failure handling, custody, reproducibility, publication, and peer-redaction behavior.

The specification stop rule remains binding: missing or ambiguous behavior returns durably through WORKFLOW COORDINATOR to ARCHITECT rather than being invented.

### Required route

TASK BUILDER implements on an isolated `taskbuilder/*` branch, performs prescribed synthetic verification, scans, commits, pushes, and returns one formal handoff to WORKFLOW COORDINATOR. Coordinator routes the exact committed implementation to the established persistent CRITIC. No merge is authorized.

## B. Local tokenizer materialization

### Authorized action

The executor may access the locally held tokenizer for the exact selected Qwen checkpoint identity solely to:

- execute the committed chat-template/context constructor;
- derive the three governed context token arrays;
- verify the encode/decode identity and stop-array construction required by the contract; and
- commit only public-safe sanitized array lengths, SHA-256 digests, and verification results in the prescribed repository artifact.

No tokenizer files, vocabulary files, model files, caches, snapshots, binary arrays, private local paths, hostnames, account names, environment dumps, or credentials may be committed or pushed.

The materialized sanitized metadata must receive persistent-CRITIC verification and a later Rebecca release before acquisition/preflight or qualification may proceed.

## C. Preserved local model artifact and runtime copies

For each authorized Qwen rung, maintain one immutable preserved checkpoint artifact in local-only custody. It is the local source of truth and must remain unmodified.

Testing must use an isolated working copy or read-only snapshot derived from that preserved artifact, never mutate the preserved artifact directly, and verify exact revision plus every weight-file SHA-256 before use.

At M4 serving time, candidate and peer are two separate runtime instances loaded from the same immutable checkpoint identity:

- candidate instance: full candidate-authorized inputs;
- peer instance: observable-only input channel with self-report/internal-state access excluded.

The two runtime instances must have identical checkpoint revision, weight hashes, tokenizer, architecture, parameters, quantization, decoding, calibration, evaluation, and binning. Their separation is runtime/custody isolation, not different weights or training.

This rule does not require publishing or duplicating multi-gigabyte model files in Git. All model and tokenizer artifacts remain local-only. Repository records contain only sanitized identity, revision, filename/size/hash/license, and verification metadata.

## D. Continuing holds

- Q2 remains unsigned and inoperative.
- Standard/harder battery manifests and SHAs remain absent.
- Acquisition/preflight and Q1–Q3 qualification remain unreleased.
- No scoring, protected-seed access, adaptive changes, backbone updates, adapters, native-CUDA L8, model publication, state/provenance mutation, merge, or gate decision is authorized.
- The local tokenizer authorization does not authorize model-weight download or model execution beyond reading the exact locally held tokenizer for the bounded materialization step.
