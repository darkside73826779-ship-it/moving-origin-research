# Reproducing and Verifying the Repository

## Scope

This guide supports installation and non-scoring verification of the current repository. It does not authorize protected scoring-seed execution or alteration of the historical evidence record.

## Requirements

- Python 3.11.x
- Approximately 1 GB free space for source, environment, and ordinary tests
- Windows PowerShell commands are shown; equivalent commands may be used on Linux or macOS

Pinned numerical dependencies are listed in [`src/requirements.txt`](src/requirements.txt).

## Environment setup

```powershell
git clone https://github.com/darkside73826779-ship-it/moving-origin-research.git
Set-Location moving-origin-research
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r src\requirements.txt
```

## Non-scoring test suite

```powershell
python -m unittest discover -s src -p "test*.py"
```

At main SHA `91b2f0fb27ff0b315987bf14d6870cf0d86d5929`, the suite contains 63 tests and passes in the prepared Python 3.11 environment.

The harness deliberately emits an error message when a test verifies that retained instrument-failure seeds are blocked. A passing unittest summary remains the governing test result.

## Historical M3 execution

The historical command is recorded for provenance in [`runs/m3-scoring-v44-301-303/RUN_PROVENANCE_AND_LOCAL_RETENTION.md`](runs/m3-scoring-v44-301-303/RUN_PROVENANCE_AND_LOCAL_RETENTION.md). It must not be interpreted as authorization to rerun protected seeds.

Important limitations:

1. The historical run used three explicitly authorized local seed-enablement edits. The base Git blob and executed-file SHA-256 are recorded, but the edited file was not proposed as the source change on the results branch.
2. The run generated 257,636 raw files totaling approximately 16.3 GB, plus a roughly 202 MB raw manifest.
3. The raw tree is retained locally, not in GitHub. Summary artifacts and a complete round-trip checksum inventory are committed.
4. The historical run reported `bit_identical = false`.
5. The later reproducibility-contract repair was reviewed without rerunning the protected scoring seeds.

## Interpreting exit and verdict states

- `PASS`: all applicable candidate and instrument requirements passed.
- `CANDIDATE FAILURE` or a triggered kill: the candidate did not satisfy a locked requirement.
- `INSTRUMENT FAILURE`: a control or apparatus requirement failed, so the affected evidence cannot support an overall pass even if candidate-facing bars passed.
- A nonzero process exit may encode a governed verdict rather than an unhandled software crash; consult the run manifest, log, and JUDGE ruling together.

## Large-artifact access

Until a durable data repository is established, open a GitHub issue labeled as an artifact-access request. Do not use public issues to transmit credentials, private system information, or security vulnerabilities.
