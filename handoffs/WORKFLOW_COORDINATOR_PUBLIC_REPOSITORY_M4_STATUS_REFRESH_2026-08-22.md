# WORKFLOW COORDINATOR public-repository M4 status refresh

Date: 2026-08-22 EDT

Authority: Rebecca directed the WORKFLOW COORDINATOR to bring the public GitHub landing material up to date and authorized same-role subagents for bounded fact checking, with the Coordinator retaining sole responsibility for review and publication.

## Scope

This maintenance change:

- updates `README.md` and `RESEARCH_STATUS.md` with bounded M4 engineering and diagnostic status;
- distinguishes engineering clearance, structural diagnostic results, alpha design status, and protected-seed scoring;
- replaces stale floating test-count language with commit-specific test discovery;
- removes the invalid `python==3.11` pip requirement while retaining Python 3.11.x as an environment prerequisite;
- makes GitHub Actions and contributor guidance run the source suite and workflow/repository suite separately; and
- extends `GOVERNANCE_SOURCE_MAP.md` through the M4 v1.6.2 specification, task specification, and implementation-only authority boundary.

## Accuracy boundary

The M4 landing-page claims are tied to immutable public commits and records. They state:

- tokenizer materialization has engineering PASS evidence and final independent evidence clearance;
- post-tokenizer engineering readiness is clear for return to Rebecca for a separate integration decision;
- the WSL2 paired diagnostic achieved structural PASS with replica MISMATCH while retaining its original blocked v1 disposition;
- the custody-free public observation backend implementation is independently clear but remains `run_authorized=false`; and
- the final pre-scoring crash cart is a corrected, independently cleared `v0.2-alpha` design, but is not promoted, implemented, runnable, released, or authorized for execution.

No M4 protected-seed scoring result or scientific verdict is claimed. No historical result, threshold, seed rule, model identity, scientific bar, or retained negative is changed.

## Publication discipline

Same-role subagents performed read-only audits of facts, landing-page consistency, and recovery-critical wording. The WORKFLOW COORDINATOR independently checked the cited repository objects and authored, reviewed, validated, and publishes the final change under Rebecca's authority.

This refresh is public-repository maintenance. It performs no model or tokenizer execution, protected-input access, scoring, science, result reinterpretation, or gate decision.

## Verification

In a fresh Python 3.11 virtual environment created outside the Git worktree:

- `python -m pip install -r src/requirements.txt` completed successfully with the corrected dependency file;
- `python -m unittest discover -s src -p "test*.py"` passed 75/75;
- `python -m unittest discover -s tests -p "test*.py"` passed 21/21; and
- the expected retained-seed denial message was emitted by its passing guard test and did not represent a scoring run.

Repository checks also include `git diff --check`, immutable-object/path verification for every M4 landing-page citation, and `git fsck --full --strict`. Unreachable local development objects, if reported, are not reachable corruption and are not introduced by this change.
