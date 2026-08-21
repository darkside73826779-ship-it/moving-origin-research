# TASK BUILDER to WORKFLOW COORDINATOR — M4 Tokenizer OCI Command Specification Block

**Date:** 2026-08-21

**Regime:** B

**Work item:** Bounded tokenizer materialization — exact OCI environment and command

## Authoritative inputs

- OCI environment release: `coordinator/m4-tokenizer-oci-environment-release` at `2e7fb9ee1f9643405d7fbc40120c7dc383abf9a3`.
- Preserved materialization release: `coordinator/m4-tokenizer-materialization-release` at `9007260570235c1b06b104d78106ba32e8a4e9dd`.
- Cleared contract: `architect/m4-tokenizer-materialization-spec` at `ed25e3b4811a9024c8b7d7a0120a8fc073748004`.
- Persistent-CRITIC CLEAR: `critic/m4-tokenizer-rf1-final-combined-rereview` at `ff3976dd58009a8c6d0d8fd2cddc787fc96b63bc`.

## Disposition

**SPECIFICATION BLOCK — the exact pinned OCI image cannot execute the exact prescribed command.**

The single authorized materialization operation remains unconsumed. No custody lookup or tokenizer/model access occurred.

## Exact conflict

The cleared contract requires both:

1. execution only inside the pinned Linux/amd64 image manifest `sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`; and
2. the exact verification/materialization invocation beginning with `python -I`.

The pinned image was acquired by the exact platform digest after its parent index and Linux/amd64 child identity were verified. Its committed image configuration declares the entrypoint executable as `python3`, and its configured PATH contains no executable named `python`.

An attempted synthetic unit-test container using the contract's exact `python -I` prefix failed during OCI process creation with executable-not-found. The container did not start and no test code ran.

Using `python3`, adding a `python` symlink, modifying the image, changing its entrypoint contract, or using host Python would alter the exact command or runtime construction. The releases expressly forbid alternate commands, image modification, host-runtime substitution, retry, and fallback. Selecting any of those options would require implementer invention.

## Environment verification

- WSL distribution: WSL2-backed Linux.
- OCI engine: Docker, Linux/amd64.
- Pinned parent index: verified.
- Required Linux/amd64 child manifest digest: verified as a member of that index.
- Local pulled image digest: exact required child manifest.
- No alternate image or tag-only image was used.

## Custody and execution attestation

- No private custody value or path appears in this artifact.
- No custody record, tokenizer payload, tokenizer configuration, model weight, token array, or rendered text was opened, read, copied, hashed, serialized, or published.
- No directory search occurred.
- No model inference, serving, qualification, diagnostics, scoring, protected-seed access, or scientific execution occurred.
- The single bounded materialization operation was not started or consumed.
- The failed container-start attempt is not a rerun or materialization attempt because no container process or prescribed Python code executed.
- No implementation draft is retained in the committed result.

## Required resolution

Return through WORKFLOW COORDINATOR for an exact deterministic contract amendment specifying a runnable command within the already pinned image, followed by persistent-CRITIC review and any required Rebecca re-release. TASK BUILDER must not choose the replacement command or image construction.

## Holds

No retry, `python3` substitution, symlink, image modification, host Python, alternate image/runtime, custody access, materialization, inference/serving, Q2/EF3, qualification, diagnostics/scoring, seeds, scientific change, STATE/provenance mutation, merge, or publication is authorized from this block.

## Public-repository safety attestation

This artifact contains only public repository SHAs, public OCI digests, contract command names, and sanitized execution disposition. It contains no credentials, machine identifiers, private paths, custody values, model/tokenizer bytes, token arrays, or personal routing metadata. The final pre-push scan and remote equality are reported in the formal return.
