# moving-origin-research

## What this is

A research program testing whether a **moving-origin temporal self-index** — a
data structure that tracks "now" as a self-referential, continuously updating
origin point rather than a fixed timestamp — can be operationally
distinguished from simpler alternatives (a fixed/frozen origin, a naive
timestamp index, a shuffled-cadence index, and other control arms).

The program is governed by a 20-law constitution and run by a small team of
specialized agent roles under a human principal (Rebecca), who holds final
authority over every binding decision: what counts as a pass, what counts as
a kill, and what gets merged into the historical record.

This is not a claim about awareness, consciousness, or AGI. It is a narrow,
falsifiable empirical question: does a moving origin behave differently, in
measurable ways, from things that only look like one?

## What's proven

- **M1 (the measurement instrument/harness) delivered green.** The harness
  that runs experiments and scores their output against locked bars was
  built, reviewed, and validated on its first scoring run. See
  [`runs/m1-run-1/`](runs/m1-run-1/) and
  [`reviews/judge_m1_run1_ruling.md`](reviews/judge_m1_run1_ruling.md).

- **E1 (the first real experiment) delivered green on 5 seeds** (42–46,
  including the pre-registered hold-out seeds 45 and 46). This is the first
  scored evidence about the moving origin. E1 tests three properties,
  jointly, all of which must hold:
  1. **Correctness** — the candidate agrees with an oracle index
     (`oracle_agreement = 1.0`).
  2. **Operational distinctness** — the candidate's query latency does not
     degrade like a naive index's does under growth (candidate ≈ 1.0×,
     fair-naive ≈ 6.89×).
  3. **Load-bearing coupling** — a downstream consumer measurably degrades
     when the moving origin is disturbed (mean degradation ≈ 0.1076,
     required > 0 on every seed).

  No kill condition fired. See
  [`runs/e1-run-2/`](runs/e1-run-2/) (the green run — E1-RUN-1 crashed on a
  construction bug, fixed and re-run, crash artifacts retained uncurated in
  [`runs/e1-run-1/`](runs/e1-run-1/)) and
  [`reviews/judge_e1_run2_ruling.md`](reviews/judge_e1_run2_ruling.md).

## What's open

**M3 and beyond** — the continuation gate. E1's result clears the bar for the
moving-origin candidate to keep going, but it does not by itself establish
the full research claim. Later milestones extend the test battery, and the
program can still fail forward: negative and null results are committed
proudly, not hidden, because the retained-negatives chain is itself part of
the program's evidence.

## Governance model

- **Rebecca** — the principal. Sole merger to `main`. Every merge is one
  click, made on the RECORDER's plain-language summary of what the merge
  adds. She does not otherwise operate this repository.
- **ARCHITECT** — proposes specifications and experimental designs.
- **CRITIC** — independently reviews specs, code, and results; can block.
- **JUDGE** — scores runs against locked bars and kill conditions from raw
  returned artifacts only.
- **RECORDER** — full custodian of this repository: all committing,
  structure, `.gitignore`/hygiene, commit-message discipline, the
  provenance log in [`docs/rulings/`](docs/rulings/), and coordination with
  the INTEGRATOR on `state/STATE.md` (the INTEGRATOR authors its content;
  the RECORDER commits it and attests its hash).
- **INTEGRATOR** — authors `state/STATE.md`, packages courier/scoring
  requests, merges implementation work into the build cell's tracked state.
- **TASK BUILDER** — implements against task specs issued by the
  INTEGRATOR/ARCHITECT.
- **Local agent (Rebecca's executor)** — a peer participant with repository
  access. Executes every scoring run from a fresh checkout of a named
  commit, and returns everything it produces — including crashes and
  failures — raw and complete to `runs/<run-id>/`, uncurated.
- **Binding rulings** from Rebecca supersede prior process documents where
  they conflict. All of them are recorded in
  [`docs/rulings/`](docs/rulings/), verbatim.
- A **20-law constitution** (amendable only by Rebecca, and only explicitly)
  governs what counts as evidence, what triggers a kill condition, and what
  the agent team is and is not allowed to decide on its own.

## Repository structure

```
/
  README.md                  — this file
  .gitignore
  docs/
    rulings/                 — Rebecca's binding rulings, verbatim, and the provenance log
  src/                        — implementation code (experiments, harness, dependencies)
  specs/                      — specifications and their changelogs
  reviews/                    — CRITIC reviews, JUDGE rulings, ARCHITECT working notes/verification scripts
  state/
    STATE.md                  — current system state (INTEGRATOR-authored, RECORDER-attested)
  runs/
    e1-run-1/                 — E1 first attempt (crashed; construction bug; kept raw and uncurated)
    e1-run-2/                 — E1 second attempt (green; the scored evidence)
    m1-run-1/                 — M1 harness validation run (green)
```

## Conventions

- Commit messages are written for strangers, using the conventional
  `chore:` / `fix:` / `docs:` / `feat:` prefixes — this history may be read
  by people with no other context.
- Nothing personal or machine-identifying is deliberately introduced into
  non-artifact files (specs, docs, reviews). Raw run artifacts returned by
  the local executor are committed as-is, uncurated, per Rebecca's current
  ruling for this private repository — see the addendum in
  [`docs/rulings/2026-08-15_repository_arrangement.md`](docs/rulings/2026-08-15_repository_arrangement.md).
  This is a deferred, not permanent, position: if the repository is ever
  made public, that policy will be revisited.
- Negative and null results are committed proudly, not hidden.
- History in this repository is never rewritten and never force-pushed.
  Rebecca is the only one who merges to `main`.
