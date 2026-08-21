# Rebecca Local-Only Model Artifact Custody Directive

Date: 2026-08-21
Regime: B
Authority class: Principal repository-custody directive

## Decision

Every downloaded or locally produced model artifact remains on Rebecca's local system and must never be pushed to GitHub or added to any Git branch. The primary reason is repository size: the model checkpoints are several gigabytes and are not practical GitHub content. This rule applies regardless of whether a branch is intended to be temporary, private, draft, or unmerged.

## Prohibited Git content

Do not stage, commit, push, attach to a pull request, or otherwise publish:

- model weight files or shards;
- checkpoint archives;
- model caches or snapshot directories;
- tokenizer/model binary blobs when redistributed as part of a downloaded checkpoint;
- converted or quantized model copies;
- locally produced adapter weights, including LoRA or QLoRA artifacts;
- runtime memory dumps or other binary material that could reconstruct model parameters;
- Git LFS pointers or other indirections whose purpose is to publish or transfer the prohibited model artifacts.

Repository `.gitignore` and pre-push safeguards must fail closed against common model-artifact extensions and cache layouts when implementation authority permits those mechanical changes. Until such safeguards are approved and implemented, each role must enforce this rule manually.

## Permitted repository records

Subject to public-repository safety and licensing constraints, the repository may contain text or small structured records needed for reproducibility and custody, including:

- public model/repository identifier;
- exact upstream revision or commit identifier;
- filenames and expected byte sizes;
- SHA-256 digests;
- license identifier and upstream source URL;
- download and verification timestamps without private machine details;
- verification, compatibility, memory, or preflight summaries that contain no private paths, machine identifiers, credentials, environment dumps, or model bytes.

Repository records must use logical artifact identifiers or public-safe relative labels. They must not record private absolute paths, hostnames, user account names, credentials, signed download URLs, access tokens, or local cache locations.

## Local custody

Downloaded models may remain in the authorized local environment for future M4 work. Their local location is coordination-sensitive and must not be placed in public repository artifacts. Any role needing the model receives the logical identity, revision, and expected digest through the authorized custody handoff; local path resolution remains outside the public record.

Before every branch push involving M4 model or serving work, the pushing role must verify that the proposed commit contains no model binaries, model-cache content, adapters, Git LFS pointers for such artifacts, private paths, or machine identifiers. Any finding blocks the push and returns to WORKFLOW COORDINATOR.

## Scope and holds

This directive clarifies custody only. It does not authorize a download, model selection, model execution, qualification, training, adapter creation, scoring, protected-seed access, merge, or gate decision. All existing M4 gates and holds remain unchanged.
