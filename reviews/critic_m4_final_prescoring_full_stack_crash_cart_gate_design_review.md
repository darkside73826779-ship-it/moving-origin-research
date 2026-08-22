# CRITIC review — M4 final pre-scoring full-stack crash-cart gate design

Date: 2026-08-22 EDT

Regime: B

Role: sole current persistent CRITIC

## Immutable intake

- Substantive result: `b25baaac2f88bce1a5c2659e5d9b917f6bb0f158`.
- Route: `architect/m4-final-prescoring-full-stack-crash-cart-gate` at `82d380ea42ca4e43386f90eedc5ae3551632c8ea`.
- Manifest: `architect/m4-final-prescoring-full-stack-crash-cart-gate-manifest` at `ccbdcd4d1a3375a83cb35326efd1670e654bd58e`.
- Banked readiness persistent-CRITIC CLEAR: `critic/m4-real-test-readiness-bf1-bf4-rereview` at `7e077a716c92536ec15f1887c418e5b2f7b63896`.

Authenticated remote equality and ancestry reproduce. The canonical helper created the isolated review worktree and accepted the substantive-to-routing handoff-only boundary. The canonical manifest validates `VERIFIED` against the common schema.

## Verdict

- **LAW_FIDELITY: BLOCK**
- **SUBSTANTIVE REPOSITORY QUALITY: BLOCK**
- **COMBINED VERDICT: BLOCK**

This is a design review only. It is not implementation, execution, scoring, qualification, science, readiness, merge, or gate authority.

## First checklist item — law and source classification

- **P1: BLOCK.** The machine contract cites `REBECCA_USER_DIRECTIVE_2026-08-22` as authority for binding warmup and active-window criteria, but no immutable repository authority path/identity is supplied and a repository search finds that label only inside this package. Repo-first law does not permit an uncommitted directive label to become binding text.
- **P2:** No new constitutional law text is quoted or reconstructed. The exact banked HELD projection is referenced by identity.
- **P3: BLOCK.** The four substantive design artifacts contain zero permitted inline `[LAW-Lx]`, `[BAR-Entry n]`, `[OP-Entry n]`, or `[PROPOSED]` tags. Custom labels such as `REBECCA_USER_DIRECTIVE_2026-08-22` and `PROPOSED_ENGINEERING_CONTROL_REQUIRES_REBECCA_RELEASE` are not among the four constitutionally permitted source tags.
- **P4:** PASS. Every new artifact is dated 2026-08-22 and identifies Regime B.
- **P5/P6:** No scientific-bar deviation or Entry-n provenance claim was introduced. Banked bars, holds, model identity, and seed rules remain unchanged.

BF4 below gives the smallest source-classification remediation.

## Blocking findings

### BF1 — warmup byte identities encode literal backslash-n, not the required LF prompts

Classification: deterministic public-input identity defect.

The narrative and machine contract require UTF-8 with LF and no BOM. Reproducing the declared generator with five actual LF bytes yields the following `(bytes, SHA-256)` identities:

- ordinal 0: `89`, `eabe6b7c5cf863599f9444019b68e0e56dde640b824bfb30756aad9faa093485`
- ordinal 1: `122`, `6b5697332c8ad2d6520655f4dc94133a1c17d4d228e3143f5f9bc80d685a04b4`
- ordinal 2: `603`, `763187d517d8b35871bc5bb6a5c41df5283fd18f0589348eb299f2d2911076db`
- ordinal 3: `1116`, `5646b4c97252d178f3c73ccd8a2ef988674c7b3f515beb64376d4ea7ab60dd13`

The committed identities are five bytes longer and reproduce exactly only when every line separator is the two literal ASCII characters backslash and `n`. Thus an implementation cannot satisfy both the required LF generator and the declared byte/digest inventory.

Smallest safe remediation: choose the required actual-LF encoding, bind the recomputed four byte/digest identities consistently in the narrative and machine contract, add an exact generator regression, and regenerate sidecars, handoff, and manifest.

### BF2 — warmup and measured receipt ordinals conflict with the production adapter

Classification: production-seam executability defect.

The design requires warmup receipt ordinals `[1,2,3,4]`, and the report schema requires every backend receipt ordinal to be at least 1. The banked production `BaseAdapter.reset_episode` sets `next_request_ordinal=0`; its first `step` requires exact equality and the receipt echoes that ordinal. Therefore the first declared warmup request fails `REQUEST_ORDINAL_MISMATCH` before model access. After the required post-warmup reset, measured ordinal 0 must likewise produce receipt ordinal 0, which the report schema rejects.

Priming either episode with an unreported ordinal-0 request would violate the exact four-pair warmup, measured-request count, complete evidence, and no-extra-request requirements.

Smallest safe remediation: use warmup receipt ordinals `[0,1,2,3]`, allow receipt ordinal 0 in the schema, and require the future semantic validator/tests to bind exact zero-based chains independently after each warmup/measured episode reset.

### BF3 — the report schema cannot represent mandatory early terminal failures

Classification: fail-closed evidence/report executability defect.

The gate requires a negative-probe defect, skipped/asymmetric/failed/timed-out warmup, residual state/KV/RNG, protected-input substitution, or pre-start identity/release failure to stop before measured work. Yet the report schema unconditionally requires:

- four fully populated warmup rows with role observations and backend receipts;
- an active window of 30–60 seconds declaring 64 paired and 128 role requests;
- exactly 64 measured rows, at least 121 resource samples, and complete measured trends.

`structural_status=BLOCKED|INSTRUMENT_FAILURE` and `replica_consistency=NOT_RUN` do not relax those requirements. The role-observation shapes also cannot represent an unattempted request without fabricating a receipt/output. Consequently the schema cannot validate the very pre-active failure artifacts that the design mandates be retained and routed.

Smallest safe remediation: make the report a status-discriminated union. Preserve the current exact success branch; add explicit pre-active, partial-warmup, and partial-active terminal branches with exact attempted/not-attempted counts, retained real rows only, no fabricated receipts, cleanup/public-safety evidence, and `replica_consistency=NOT_RUN` where comparison never occurred. Bind cross-field semantics in the future validator and focused failure-path tests.

### BF4 — numeric gates and test criteria lack permitted P3 source tags

Classification: law-fidelity/source-provenance defect.

The warmup counts/timeouts, 64-pair schedule, 30-second minimum, 60-second deadline, queue 8, 250-ms sampling, failure/kill criteria, and schema equivalents are operational gates but carry no permitted inline source tag. A custom `source` string does not satisfy Constitution v2 §5.1 P3; an uncommitted directive label also cannot satisfy P1.

Smallest safe remediation: attach an exact permitted tag to every narrative and machine-readable threshold/kill/test equivalent. Use `[PROPOSED]` for new engineering controls unless an exact committed `[BAR-Entry n]` or `[OP-Entry n]` authority exists; keep them quarantined behind the existing Rebecca-release stop. If the cited Rebecca directive is intended to be binding repository authority, first bind its exact committed path and immutable identity without reconstructing its text.

## Cleared checks and preserved boundaries

- All 10 manifest artifact raw SHA-256 identities, all three adjacent sidecar pairs, LF bytes, modes, and routing topology reproduce. The tokenizer result/sidecar path, mode, Git blob, byte count, and raw digest reproduce at `e462e5bd61bcbad4eb03160129dec2e088de9892`.
- The banked readiness result/route/manifest/review, dependency package/review, annotated testbed tag/peeled commit, same-checkpoint model identities, and production-seam topology are exact and remotely available.
- Four-pair symmetry, clean post-warmup session/KV/RNG barrier, post-barrier measured/scoring insertion separation, 64-pair schedule, 30/60-second active controls, queue 8, 250-ms telemetry, complete-row retention, deterministic trend intent, structural/replica separation, exact-replica mismatch stop, cleanup, and export blocking are coherent apart from BF1–BF3.
- The design labels all trends `NON_SCORING_EXPLORATORY_OBSERVATION`, keeps the five law rows HELD/no-claim, forbids token-ID arrays and protected/private inputs, and retains public-safety findings without row deletion or silent suppression.
- Every future production, combined-tree, OCI, backend, evaluation-config, dependency, parallel-CPU `gofast`, validator/renderer/test, implementation-review, JUDGE, and Rebecca single-run identity remains explicitly `UNBOUND`. `run_authorized`, `merge_authorized`, and `scoring_authorized` remain false.

## Public safety and execution boundary

Public preflight over `3d1e1e4ad9039ce25f311367aff5798ad7fcec07...82d380ea42ca4e43386f90eedc5ae3551632c8ea` retained 86 findings across three scan domains. Manual review classified 78 fixed-regex matches as public timing controls or substrings inside public immutable identities. The eight gitleaks generic-key matches are repeated detections of the two declared public tokenizer/tokenizer-config SHA-256 values. No credential, contact data, private path/value, protected input, model/tokenizer bytes, token array, score, or scientific result is present.

Only committed public repository bytes and read-only validators were used. No implementation, model/OCI/WSL2 execution, custody/protected input, scoring, qualification, science, state/provenance mutation, merge, publication, readiness declaration, or gate action occurred.

## Disposition

Return one **COMBINED BLOCK** to **WORKFLOW COORDINATOR**. The exact next role is **ARCHITECT** for one batched BF1–BF4 design remediation, followed by one delta-only persistent-CRITIC rereview. All banked evidence and holds remain binding.
