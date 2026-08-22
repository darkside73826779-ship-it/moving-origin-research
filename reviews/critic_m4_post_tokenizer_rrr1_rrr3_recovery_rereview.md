# CRITIC Recovery Rereview — M4 Post-Tokenizer RRR1–RRR3

Date: 2026-08-22 EDT

Regime: B

Role: independent CRITIC recovery

Terminal state: **COMBINED BLOCK**

## Canonical intake and identity evidence

- Package: `taskbuilder/m4-post-tokenizer-rrr1-rrr3-remediation @ 19b6562efe739d0e9265f4a2f0274a9f3e577dc1`
- Implementation result: `1663d6d46b96412373af610bf3c83f397a2dfc0b`
- Routing result: `d31fe9e15f572b0c3dceec7665a058c802b19614`
- Base: `taskbuilder/m4-post-tokenizer-rrir1-rrir4-remediation @ 1990b387d510cfc690b8bfd156c551751007aea5`
- Prior review: `critic/m4-post-tokenizer-rrir1-rrir4-rereview @ 3571916555480a72c69226d040c409d38876f125`
- Canonical manifest: `handoffs/TASK_BUILDER_TO_WORKFLOW_COORDINATOR_M4_POST_TOKENIZER_RRR1_RRR3_REMEDIATION.manifest.json`

The repository validator returned `VERIFIED`. All 19 manifest artifact SHA-256 identities reproduce. The combined inventory reproduces all 68 raw Git blobs, including mode, byte count, Git blob SHA-1, and raw SHA-256; all 27 adjacent sidecars have exact lowercase-digest, two-space, basename, and one-LF grammar and verify their targets. Base/result/routing/manifest ancestry is linear and exact. `git diff --check` and `git fsck --full --strict` pass.

## Banked closure

### RRR1 — closed

`_VerifiedFanoutInput`, `_validate_verified`, and `_step_verified` are absent. `FanoutCoordinator.step` is the sole execution path. It deep-copies the eventual request before reconciliation, rederives prompt and stop through the configured process-local provider, verifies the ordered sanitized rows and exact length/digests, freezes the two backend views, supplies the same request snapshot to both adapters, and computes the public request digest from that snapshot. The focused forgery and caller-drift cases pass. Independent inspection found no separately callable verified-capability bypass.

### RRR3 — closed

The mutation runner, canonical mutation contract, and canonical transcript are committed and raw-identity bound. Independent execution of `python -I tests/run_m4_post_tokenizer_mutation_tests.py --verify` reproduced `14/14` killed mutants and exact transcript SHA-256 `2882a172d9f0ca76bb698a00ca50aebc7d253519aa60e31a12094cd60c352cfd`. The runner authenticates indexed blobs, exact occurrence counts, mutant identities and fully qualified commands, records normalized exit/output evidence, and restores the baseline after every mutant.

The identity-first custody-free integration wrapper independently ran `49/49 PASS`. Banked 42-cell lifecycle, 13 fixture-negative, rollback, law fail-closed, episode-history, pair-prevalidation, frozen-provider, tokenizer PASS-pair, and no-held-access evidence remains present and identity-consistent.

## Residual blocker RRR2-F1 — non-Boolean cleanup attestation is accepted as verified disposal

The remediation correctly routes throwing liveness probes through `_dispose_verified`, and it rejects a second probe that returns true or raises. However, `_dispose_verified` currently uses:

```python
if backend.is_live(): raise IntegrationError("BACKEND_ROLLBACK_FAILURE")
```

This accepts any falsey non-Boolean value—including `None`, `0`, or an empty object—as proof that the backend is non-live. That contradicts the package's own bound rule that only a **verifiably false** post-disposal liveness result may produce the role-specific `*_BACKEND_NOT_LIVE` result and that unobservable cleanup must project `BACKEND_ROLLBACK_FAILURE`.

An independent production-path adversary used a candidate backend whose first `is_live()` call raised and whose post-disposal probe returned `None`. `AdapterFactory.create_pair` returned `CANDIDATE_BACKEND_NOT_LIVE`; the cleanup state was not authenticated as literal Boolean false. The 49-test suite covers true, false, throwing, no-op, partial, and throwing-dispose cases, but not a non-Boolean post-disposal result. The mutation contract likewise changes the conditional to `if False` and does not test strict Boolean identity.

Required narrow remediation: require the post-disposal observation to be literal `False` (for example, fail when `backend.is_live() is not False`), add candidate/peer/control production adversaries for `None`, `0`, and another falsey non-Boolean result, and add a mutation that weakens literal-false authentication back to truthiness. Preserve RRR1/RRR3 and all banked evidence.

## Executability and public safety

- Canonical manifest validator: `VERIFIED`.
- Independent custody-free wrapper: `49/49 PASS`.
- Independent deterministic mutation replay: `14/14 KILLED`, transcript equality PASS.
- No private inputs, custody/model/tokenizer data, scoring, science, durable state, merge, publication, or gate action was accessed or performed.

Package preflight retained 144 duplicate-domain findings: 124 fixed-regex personal-contact heuristics occur wholly inside required public Git/SHA/digest identities or literal hexadecimal alphabets, and 20 gitleaks generic-key findings are repeated matches on declared public source/test/artifact digests. Manual inspection found no credential, contact data, private path/value, token array, model/tokenizer bytes, seed, score, or scientific output. No finding was suppressed.

The review-only preflight retained two duplicate-domain fixed-regex findings at the same artifact location. Both are numeric substrings wholly inside the required public implementation commit identity `1663d6d46b96412373af610bf3c83f397a2dfc0b`; they are reproducibility metadata, not contact data. Gitleaks returned zero review findings.

## Disposition

**COMBINED BLOCK.** RRR1 and RRR3 are closed. Return only RRR2-F1 as one narrow implementation/test/mutation-evidence correction through WORKFLOW COORDINATOR. All standing holds remain binding.
