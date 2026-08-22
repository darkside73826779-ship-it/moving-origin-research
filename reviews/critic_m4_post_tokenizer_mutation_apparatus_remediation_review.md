# CRITIC review — M4 post-tokenizer mutation-apparatus remediation

Date: 2026-08-22 EDT  
Role: independent recovery PERSISTENT CRITIC  
Input package: `taskbuilder/m4-post-tokenizer-mutation-apparatus-remediation @ b751ef71b3f6c7dda126ce1a28af6f0d29b572dd`  
Implementation: `6d4089ef95a14fb6b1d46c96ebf452733ff5cd98`  
Handoff/quality trace: `735cc67d8a79e9e3e6d251b4bf0f46ec038b2a6a`  
Input production package: `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`  
Durable JUDGE BLOCK: `32f72c2bb708d96060eb636cb4cf7a673c85ec24`

## Verdict

**COMBINED CLEAR.** The mutation apparatus remediation closes the JUDGE-identified false-kill defect and the two additional acceptance probes. Production implementation and production-test behavior are byte-preserved. No held or scientific action occurred. This CLEAR stops at WORKFLOW COORDINATOR for a new exact JUDGE route; it does not decide implementation readiness or authorize downstream work.

## Canonical package and preservation

- The common handoff manifest validates `VERIFIED`.
- Remote equality is exact at `b751ef71b3f6c7dda126ce1a28af6f0d29b572dd`; implementation, handoff, and manifest commits form the declared linear ancestry.
- All 72 canonical-manifest raw Git-blob SHA-256 identities reproduce.
- The combined inventory reproduces 69/69 mode, Git-blob, raw-byte-count, and SHA-256 rows; all 27 contained sidecars verify exact target basename/digest/LF grammar.
- `src/m4_post_tokenizer_integration.py` and `src/test_m4_post_tokenizer_integration.py` are byte-identical to input `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`. The implementation delta is confined to the mutation runner, its apparatus tests, mutation contract/transcript, inventory/launch identity cascade, and handoff topology. No science or production behavior changed.

## Independent instrument verification

- All 15 contract entries resolve under `src.test_m4_post_tokenizer_integration.RereviewRemediationTests` (nine distinct methods). Independent calls outside mutation replay discover the exact fully-qualified target once, execute one test once, and pass cleanly for every entry.
- The runner validates the unchanged baseline before each mutation and requires exact discovery identity, one executed test, no loader/runtime errors, skips, unexpected success, stdout, or stderr.
- KILLED is accepted only for an `AssertionError` failure from the exact discovered target whose normalized traceback matches the contract-bound mutation-sensitive regular expression. A passing mutant is SURVIVED. Unrelated assertions and discovery/import/syntax/environment/timeout/process/stderr/malformed-JSON/I/O failures are INSTRUMENT_FAILURE, never KILLED.
- Each mutation is applied only to a disposable custody-free copy. The baseline bytes and SHA-256 are restored in a `finally` boundary after every mutant. Body failure, corrupt restoration, and restoration-write failure adversaries all fail closed.
- The committed canonical transcript reproduces exactly at SHA-256 `f889582b8cabc1786729987b73f127dfa4b4db745a6bbca9439fcc74e3a99bce`; all 15 records have a clean one-test baseline, exact mutation identity, the bound assertion failure, zero errors, KILLED classification, and restored baseline identity.

## Explicit acceptance probes

1. An intentionally nonexistent fully-qualified `RereviewRemediationTests` method produced loader/discovery evidence and was classified `INSTRUMENT_FAILURE: target discovery/execution`; it was never accepted as KILLED.
2. A no-op contract probe with identical old/new bytes and baseline mutant identity left the target passing and was classified `SURVIVED`; the verification path failed closed and never accepted it as KILLED.

These probes were performed independently of the committed replay. The independent target-resolution/baseline pass likewise did not rely on accepting the runner's transcript as proof of itself.

## Executability and regression

- Windows host, custody-free: integration 49/49 PASS; apparatus 15/15 PASS; mutation replay 15/15 KILLED with exact canonical transcript equality.
- Exact locally installed pinned image `docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6`, Linux/amd64, `--pull=never`, network none, read-only repository, all capabilities dropped, no-new-privileges, private tmpfs, no custody environment/mount, no output mount:
  - integration 49/49 PASS;
  - apparatus 15/15 PASS;
  - mutation replay 15/15 KILLED with transcript SHA-256 `f889582b8cabc1786729987b73f127dfa4b4db745a6bbca9439fcc74e3a99bce`;
  - banked tokenizer source regression 37/37 PASS.
- No materializer, tokenizer operation, inference, private input, model/tokenizer custody, prompt, seed, scoring, or science was accessed or executed.

## Public safety

The complete `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41..b751ef71b3f6c7dda126ce1a28af6f0d29b572dd` preflight retained 253 findings without suppression: 241 fixed-regex personal-contact heuristics and 12 gitleaks generic-key heuristics across duplicated commit-parent/range domains. Manual inspection classifies the fixed-regex matches as numeric substrings wholly inside required public Git/SHA/digest identities, public synthetic traceback/measurement evidence, or hexadecimal validation literals. The gitleaks matches are declared public artifact/source digests. No credential, contact data, private path/value, token array, model/tokenizer byte, prompt, seed, score, or scientific result is present.

The initial review-commit preflight retained four duplicate-domain fixed-regex findings: two occurrences scanned in both commit-parent and combined-range domains, wholly inside the required public canonical transcript SHA-256. They are non-contact reproducibility metadata; gitleaks returned zero review findings. None was suppressed.

## Disposition

The mutation apparatus is independently reproducible and fail-closed for the defect class that caused the durable JUDGE BLOCK. All package identities and banked regressions are preserved. Route this CLEAR only through WORKFLOW COORDINATOR to a new exact JUDGE readiness review. All existing holds remain binding.
