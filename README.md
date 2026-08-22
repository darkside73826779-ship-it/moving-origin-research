# Moving Origin Research

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

An open, falsifiable research program testing whether a **moving-origin temporal self-index** can be operationally distinguished from simpler temporal representations.

A moving-origin index tracks “now” as a continuously updating reference point. The program compares that mechanism against frozen, naive, shuffled, permuted, oracle, and other control conditions under pre-specified tests.

This repository does **not** claim awareness, consciousness, AGI, or machine sentience. It reports evidence about temporal self-modeling mechanisms, including failures and unresolved limitations.

## Current research status

| Stage | Question | Governing result | What the result means |
|---|---|---|---|
| M1 | Is the measurement and scoring harness functioning? | **PASS** | The first scoring run delivered green. See [`runs/m1-run-1/`](runs/m1-run-1/) and the [JUDGE ruling](reviews/judge_m1_run1_ruling.md). |
| E1 | Is the moving-origin candidate correct, operationally distinct, and load-bearing? | **PASS on five seeds** | Oracle agreement was 1.0; candidate latency remained approximately constant while the fair-naive index grew approximately 6.89×; every seed showed positive downstream degradation when the moving origin was disturbed. See [`runs/e1-run-2/`](runs/e1-run-2/) and the [JUDGE ruling](reviews/judge_e1_run2_ruling.md). |
| M3 V4.4 | Does the candidate satisfy the M3 law battery under calibrated controls? | **Continuation evidence; overall INSTRUMENT FAILURE** | Every candidate-facing bar passed. Of 27 pre-registered stochastic control checks, 26 passed and one frozen-control calibration check failed on seed 303. Under the locked protocol, that single apparatus failure blocks an overall M3 PASS. See the [M3 JUDGE ruling](reviews/judge_m3_v44_scoring_ruling.md). |
| M4 tokenizer materialization | Can the governed tokenizer construction be reproduced and published safely? | **Engineering PASS; evidence independently cleared** | All 18 governed checks passed through atomic publication. This validates tokenizer construction and evidence integrity, not model quality or science. See the [final execution-evidence review](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/7274fbb1aef06d686efe07bb54b6828d0a5b41e2/reviews/critic_m4_tokenizer_pass_evidence_ex_pass2_final_rereview.md). |
| M4 post-tokenizer integration | Is the post-tokenizer implementation adequately verified for a later integration decision? | **Engineering-readiness CLEAR; integration and scoring not authorized** | The corrected mutation apparatus closed the prior evidence defect without changing the accepted production implementation or its production tests. The JUDGE returned the package to Rebecca for a separate decision. See the [Recorder-published ruling](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/3470ab1a032644eba30cbe6b4e361c9a9518d95e/docs/rulings/judge_m4_post_tokenizer_mutation_clear_readiness_reconsideration.md). |
| M4 WSL2 dual-runtime diagnostic | Can the public test bed sustain the paired runtime structure? | **Structural PASS; replica MISMATCH** | The retained diagnostic compared 164 outputs: 80 agreed and 84 differed. The original v1 result remains `BLOCKED / OUTPUT_DIGEST_MISMATCH`; the reviewed two-axis projection preserves structural feasibility separately from replica consistency. See the [independent review](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/4cdb5d89945b603c20cdd19233079be14b65946b/reviews/critic_m4_wsl2_two_axis_dependency_lock_bf1_bf2_rereview.md). |
| M4 public observation backend | Is the custody-free, non-scoring observation backend implemented fail-closed? | **Repository-quality CLEAR; `run_authorized=false`** | Design and implementation review are clear, including the corrected zero-count boundary. No public-model observation run has been authorized or performed. See the [final implementation rereview](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/98b8f466db2ad8499ea5abab9111a68a9bd1e861/reviews/critic_m4_public_model_observation_backend_bf1_zero_count_rereview.md). |
| M4 final pre-scoring crash cart | Is the full-stack non-scoring dress-rehearsal design ready to implement? | **v0.2-alpha under independent review** | The blocked v0.1-alpha design is retained. Its BF1–BF4 correction is published as v0.2-alpha, but it is not yet beta, runnable, or an authorization. See the [versioned routing record](https://github.com/darkside73826779-ship-it/moving-origin-research/blob/757dc3bf3b7eec554ee15882af94fce4a6ebb006/handoffs/ARCHITECT_TO_COORDINATOR_M4_FINAL_PRESCORING_CRASH_CART_BF1_BF4_VERSIONED_ROUTING_2026-08-22.md). |

### How to interpret the M4 status

M4 is at an engineering and diagnostic boundary, not a scoring boundary. The tokenizer and major custody-free components have independently reviewed evidence, and the WSL2 test bed demonstrated structural feasibility while exposing unresolved replica disagreement. No protected-seed M4 scoring run, model qualification, scientific verdict, or final readiness declaration has occurred.

The status labels above are intentionally narrow:

- **Engineering PASS/CLEAR** means the named construction, code, or evidence package passed its bounded review.
- **Structural PASS; replica MISMATCH** means the diagnostic structure ran, but replica outputs were not identical. It is not a scientific or model-quality result.
- **Alpha** means a versioned design artifact exists for review. It does not authorize implementation or execution.
- Only Rebecca may authorize integration, merge, qualification, protected-seed scoring, scientific interpretation, or result publication.

### How to interpret the M3 instrument failure

`INSTRUMENT FAILURE` is a defined governance outcome, not a synonym for “the candidate failed.” M3 separately tests the candidate mechanism and whether the controls used to interpret that mechanism are properly calibrated.

- The moving-origin candidate passed every candidate-facing bar on all three scoring seeds.
- L1, L5, and L6 passed on all three seeds.
- L3 candidate-facing bars passed on all three seeds, and L3 was scoreable on seeds 301 and 302.
- One L3 frozen-control calibration check failed on seed 303: its plus-one p-value was approximately 0.012 against a pre-registered per-seed threshold of approximately 0.0167.
- Because the protocol is fail-closed, that one failed control check makes L3 unscoreable on seed 303 and blocks certification of an overall M3 PASS.

The result therefore supports continued investigation while identifying a weakness in the measurement apparatus that must be resolved prospectively. It does **not** show that the candidate mechanism failed, and it does **not** justify presenting M3 as fully passed. Preserving that distinction is part of the project’s protection against selective interpretation and “green chasing.”

### M3 reproducibility status

The historical M3 scoring run separately reported `bit_identical = false`. That failed check is preserved in the original artifacts and ruling.

After the run, the discrepancy was diagnosed as a reproducibility-contract defect. A two-digest semantic reproducibility architecture was implemented and independently CRITIC-reviewed. The repair changed no locked bar, scoring threshold, candidate-facing predicate, or historical result. No protected scoring seed was rerun, so the repaired code does **not** retroactively certify the historical scoring run.

- [Implementation changes](src/M3_REPRODUCIBILITY_CONTRACT_CHANGES.md)
- [Initial implementation review](reviews/critic_m3_reproducibility_contract_impl_verification.md)
- [Corrected implementation clearance](reviews/critic_m3_reproducibility_contract_bf1_reverification.md)

## What is established—and what is not

The evidence currently supports continued investigation of the moving-origin mechanism. It establishes that the candidate passed the recorded M1 and E1 gates and passed multiple M3 candidate-facing tests. It does not establish the complete research-program claim, and it does not support claims about consciousness or AGI.

Open work includes:

- resolving the M3 L3 control calibration before any newly authorized scoring design;
- independent use of the repaired semantic reproducibility contract;
- full independent recomputation from the retained M3 raw artifact tree;
- a separate principal integration decision for the engineering-cleared M4 post-tokenizer package;
- final review, implementation, and explicit release of the M4 pre-scoring crash cart;
- separately reviewed and explicitly authorized model/runtime observation before any M4 qualification or scoring run.

See [RESEARCH_STATUS.md](RESEARCH_STATUS.md) for a compact evidence and limitation ledger.

## Conceptual lineage

The moving-origin construct does not originate with this program. It operationalizes
ideas with established lineage, cited here so the program's contribution is scoped
correctly — the contribution is the operational test battery and governance record,
not the underlying concept:

- **Tulving (1985), "Memory and consciousness"** — autonoetic consciousness: episodic
  remembering as a self located in subjective time. The direct ancestor of a "now"
  indexed to a system's own history.
- **Suddendorf & Corballis (2007)** — mental time travel as the standard modern
  framing of the Tulving lineage.
- **Husserl, *On the Phenomenology of the Consciousness of Internal Time***
  (1893–1917; Brough trans. 1991) — the thick present with retention and protention;
  the source of the "origin that moves" rather than "timeline that is scanned"
  distinction.
- **Friston (2018), "Am I Self-Conscious?"** — temporal depth in active inference;
  the computational bridge between the phenomenological and mechanistic framings.
- Optionally, for a mechanistic neuroscience anchor: hippocampal time cells
  (Eichenbaum 2014; see also Buzsáki & Llinás 2017 on brain time) — temporal
  indexing as mechanism rather than metaphor.

Methodological practices are likewise inherited: pre-registration and registered
reports (Nosek et al. 2018; Chambers 2013), and the instrument-failure /
candidate-failure distinction adapted from metrology and clinical-trial data
monitoring practice rather than from machine learning.

## Quick start: non-scoring verification

Python 3.11 is required.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r src\requirements.txt
python -m unittest discover -s src -p "test*.py"
python -m unittest discover -s tests -p "test*.py"
```

The first test command runs the source non-scoring suite. The second runs workflow and repository-mechanics tests. Their summaries for the checked-out commit are authoritative; fixed README test counts are not. Milestone-specific packages use identity-bound wrappers and may have different reviewed inventories. These commands do not authorize a scoring run or reuse of protected seeds. Read [REPRODUCING.md](REPRODUCING.md) before attempting any experiment or harness execution.

## Evidence and artifact availability

Summary artifacts, rulings, specifications, and provenance records are committed under [`runs/`](runs/), [`reviews/`](reviews/), [`specs/`](specs/), and [`docs/rulings/`](docs/rulings/).

The complete M3 raw artifact tree contains 257,636 files totaling approximately 16.3 GB. It remains retained locally and is not stored in GitHub. Its inventory, sizes, executed-source hash, and retention statement are recorded in [`RUN_PROVENANCE_AND_LOCAL_RETENTION.md`](runs/m3-scoring-v44-301-303/RUN_PROVENANCE_AND_LOCAL_RETENTION.md). Artifact-access requests may be opened as a GitHub issue until a durable research-data host and accession identifier are established.

Public-repository policy:

- no unreviewed environment dumps, credentials, or machine-personal data may be added;
- future executor logs and raw artifacts must receive a credential/PII scan before publication;
- large evidence retained outside GitHub must have a committed inventory, checksums, retention statement, and request route;
- historical negative, crash, and instrument-failure evidence is retained and never relabeled as a pass.

## Governance and provenance

The program uses separated agent roles under human principal Rebecca R. McClintic, who retains every binding gate decision:

- **Principal** — approves specifications, bars, scoring authorization, constitutional changes, and merges to `main`.
- **ARCHITECT** — proposes specifications and experimental designs.
- **CRITIC** — independently reviews specifications, code, and results and may block progression.
- **JUDGE** — scores returned evidence against locked bars and kill conditions.
- **RECORDER** — preserves repository history, rulings, and provenance.
- **INTEGRATOR** — maintains the tracked state and packages work between roles.
- **TASK BUILDER** — implements only against reviewed task specifications.
- **Local executor** — performs authorized runs from named commits and returns raw outputs, including failures.

Binding decisions and retained negatives are preserved in [`docs/rulings/provenance_log.md`](docs/rulings/provenance_log.md) and [`state/STATE.md`](state/STATE.md). The source map and limitations of the public governance record are documented in [GOVERNANCE_SOURCE_MAP.md](GOVERNANCE_SOURCE_MAP.md).

AI systems contributed to drafting, implementation, criticism, and recordkeeping. Their outputs were separated by role and governed by human authorization. See [AI_CONTRIBUTIONS.md](AI_CONTRIBUTIONS.md).

## Repository map

```text
docs/rulings/   Binding rulings, lineage attestations, and provenance
handoffs/       Role-to-role implementation and review records
reviews/        Independent CRITIC reviews and JUDGE rulings
runs/           Committed scoring summaries, logs, and manifests
specs/          Experimental specifications and amendments
src/            Harness, experiment, reproducibility, and test code
state/          Current governed project state and role initialization
verification/   Independent deterministic verification utilities
```

## Funding objective

Funding would be used to strengthen independent replication and extend the program—not to reinterpret existing results. Priority uses include durable hosting of the raw evidence, independent statistical and methodological review, reproducible compute, later-milestone implementation, model-level experiments, and qualified research collaborators.

See [FUNDING_OBJECTIVES.md](FUNDING_OBJECTIVES.md).

## Citation, contributions, and security

- Preferred citation metadata: [`CITATION.cff`](CITATION.cff)
- Contribution policy: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Private security reporting guidance: [`SECURITY.md`](SECURITY.md)

## License

Copyright 2026 Rebecca R. McClintic. Licensed under the [Apache License 2.0](LICENSE). Attribution information is provided in [`NOTICE`](NOTICE).

## History policy

Negative and null results are retained. Repository history is not rewritten or force-pushed to improve appearances. Corrections are added prospectively with their provenance preserved.
