# Contributing

## Current policy

External discussion, replication reports, documentation corrections, and clearly scoped pull requests are welcome. Changes to governed scientific claims, locked bars, historical verdicts, or provenance require explicit principal authorization and the existing role-review process.

Unless explicitly designated otherwise in writing, contributions accepted into this repository are licensed under the Apache License 2.0 in accordance with its contribution terms.

## Before opening a pull request

1. Open an issue describing the proposed change and whether it affects code, documentation, experimental design, or recorded evidence.
2. Do not include credentials, private system information, protected seeds, or unpublished raw artifacts.
3. Do not rewrite Git history or remove negative results to simplify the narrative.
4. For code changes, run:

   ```powershell
   python -m pip install -r src\requirements.txt
   python -m unittest discover -s src -p "test*.py"
   python -m unittest discover -s tests -p "test*.py"
   ```

   Python 3.11.x is required. Report the two suite summaries separately; test inventories are commit-specific.

5. Identify any generated or AI-assisted material in the pull-request description.

## Evidence-changing contributions

Changes that could affect scoring, thresholds, controls, seeds, or interpretation will not be accepted as ordinary maintenance. They require prospective specification, independent CRITIC review, human approval, and a new evidence record where authorized.

## Conduct

Engage with the work and other contributors respectfully. Criticism of methods and claims is welcome when it is specific and evidence-based.
