# TASK BUILDER → INTEGRATOR — L8 GPU v1.5 sentinel STOP

**Date:** 2026-08-21  
**Regime:** B  
**Gate served:** Approved L8 GPU v1.5 implementation and execution release; Commit A plus the single authorized sentinel execution [PROPOSED].

## Input SHAs reviewed

- Base: `d38f9069d9a4f2a92ffb3a29d6f80ef4e7253da9`
- Approved specification branch: `architect/l8-gpu-adoption-spec` at `e05550f494b2c6dffb2ea9645067395beaf56fe1`
- Approved specification result: `a25398e599622c09d130b597b7bc83ce62a966d5`
- Independent CRITIC CLEAR: `e0aad1dabde9546e0074a7a375135eb92ee2072a`
- Rebecca approval/release intake: `50260d3`
- TASK BUILDER Commit A: `447556275e0f31682c38a53cb03f5a583e598110`

## Files changed or created

- Commit A contains the approved v1.5 specification inputs, implementation, exact fixtures, tests, and executability trace.
- `diagnostics/.l8_gpu_adoption_rehearsal/01-cuda_unavailable/result.json` — retained failure-rehearsal target; raw SHA-256 `fb62456973525f6b14001f2e4fb243a01b9ba3ed4d19925b45e4399e6a601727`.
- `diagnostics/.l8_gpu_adoption_rehearsal/01-cuda_unavailable/result.json.sha256` — retained sidecar; raw SHA-256 `ad9b592594ff3ae57fcc6ff3759a710a273e43a858854ca0a28a57ec9a8d3da9`.
- This handoff.

## Branch/result SHA

- Branch: `taskbuilder/l8-gpu-v1.5-release`
- Commit A: `447556275e0f31682c38a53cb03f5a583e598110`
- Failure-evidence Commit B: recorded by the commit containing this handoff.

## What was implemented

The approved GPU diagnostic backend, deterministic fixtures, exact dependency preflight, CPU↔GPU sentinel custody, failure rehearsal, bounded full-screen producer/GPU pipeline, atomic publication, and required tests were implemented under the approved v1.5 contract. Commit A was frozen and pushed before execution.

## What was verified

- Python `3.11.9`; NumPy `1.26.4`; SciPy `1.13.1`; Torch `2.13.0+cu130`; RFC 8785 `0.1.4`.
- CUDA available on NVIDIA GeForce RTX 5080.
- Exact dependency source/hash preflight passed.
- Test battery: `36 passed in 90.84s`, including all 17 required matrix node IDs exactly once and one live-CUDA primitive-tape parity test.
- Live-CUDA parity diagnostic: masks, rho masks, and predicates identical; maximum beta delta `1.3877787807814457e-17`; maximum rho delta `0`.
- Executability trace raw SHA-256: `531148c6f1927c9b3f9f7946ec931ac9f16e6a82716619b881fcf4854c6f28ff`.

## STOP event and blocker

At `2026-08-21 02:41 EDT`, the single authorized sentinel execution was launched from clean Commit A after environment and CUDA identity checks passed. It stopped during the mandatory `failure_rehearsal` before any sentinel result publication:

`ValueError: schema keys/order mismatch`

The exception arose when the parent decoded the first child rehearsal row and applied its ordered-key check. The child canonicalizes the row before transfer; canonical JSON key ordering therefore does not match the separately required semantic field order. This is an implementation/apparatus defect requiring independent review. It is not renamed as a statistical failure or as a completed sentinel verdict.

No sentinel result JSON or sidecar was published. No full-screen result JSON or sidecar exists. The full-screen execution was not launched because the prerequisite `EQUIVALENT_FOR_O15_DIAGNOSTICS` verdict was not obtained. The sentinel was not retried or replaced [OP-Entry 14].

## Rebecca repair and replacement-execution authorization

After receiving the STOP report and repair options on 2026-08-21, Rebecca R. McClintic expressly authorized TASK BUILDER to implement the recommended RFC 8785 canonical-order repair and run the sentinel again. This authorizes one new replacement sentinel execution after the repair passes tests; it is not an automatic retry. The conditional full-screen execution remains permitted only if that replacement sentinel returns `EQUIVALENT_FOR_O15_DIAGNOSTICS`.

## Authorized repair and replacement-sentinel result

- Repair commit: `44046ae40f3e2f381f7c4227b5dd4bf1db874063`.
- Full post-repair battery: `37 passed in 86.27s`.
- The one Rebecca-authorized replacement sentinel completed without an apparatus failure.
- Published result: `diagnostics/l8_gpu_adoption_equivalence.json`.
- Published raw SHA-256: `1178de6f7ad40d282d2ffb102fb02809ad6b9370d92c5189eee088a66414017b`.
- Verdict: `NOT_EQUIVALENT`.
- Both runs were byte-repeatable; all deterministic cases and all twelve failure rehearsals passed.
- Equivalence failures: counts were not all equal, numeric tolerances did not all pass, and predicates were not all equal.
- Maximum beta difference was `5.551115123125783e-16`; maximum rho difference was `0.4000000000000001` in nonzero-alpha cells.
- One reported combo complete-verdict count differed: CPU `122`, GPU `121`.

Because the approved prerequisite verdict was not obtained, the full-screen execution was not launched. This completed negative sentinel result is preserved without renaming. Any rho-path remediation and any further execution require a new reviewed design and explicit Rebecca authorization.

## Proposed rho-path remediation for review

At Rebecca's direction, TASK BUILDER implemented the narrowest accuracy-preserving remediation without changing the published primitive-tape schema:

- Construct selection-critical `c_prime` from the existing tape using the unchanged NumPy/SciPy CPU reference primitives before transfer to CUDA. This prevents transcendental-library rounding near `c_prime > tau` from changing answered sets.
- Compute the discontinuous four-dose rho midrank statistic from the returned GPU `d_seed` using the unchanged CPU reference reduction. This prevents CUDA reduction ordering from splitting CPU-exact ties.
- Retain CUDA batching for stable sorting, selection, incorrect-answer counting, risk updates, beta, and the large tensor workload.

Two new nonzero-alpha regression cases cover the sentinel geometries that previously diverged. They require identical `d_seed`, validity masks, rho masks, and predicates, plus the existing numeric tolerances. Targeted result: `21 passed in 1.58s`. Full battery: `39 passed in 88.26s`. No new sentinel or full-screen execution was performed as part of this proposed remediation.

## Public-repository safety attestation

Before Commit A was pushed, gitleaks scanned the complete one-commit delta and found zero leaks. A separate regex/manual scan found no credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, protected seeds, or other prohibited PII. The role-local Git author address was classified acceptable. `git diff --check` found only three intentional Markdown hard-break spaces in Rebecca's immutable approval artifact; they were preserved. The failure-evidence commit received the same pre-push scan before publication.

## Exact next recipient role

INTEGRATOR, then CRITIC for independent implementation/failure review, through WORKFLOW COORDINATOR. Any redesign or specification ambiguity must route to ARCHITECT; only Rebecca may authorize another execution.

## Explicitly prohibited actions

No rerun or replacement of the failed sentinel; no full-screen execution; no scoring; no scoring-mode execution; no protected/hold-out/courier seed access or exposure; no G2–G4 freeze; no negative renaming; no automatic retry/fallback; no unrelated scientific work; no merge to main; and no L15/L16/L17 work before M5. A new execution requires a new explicit Rebecca release after the defect is reviewed and remediated.
