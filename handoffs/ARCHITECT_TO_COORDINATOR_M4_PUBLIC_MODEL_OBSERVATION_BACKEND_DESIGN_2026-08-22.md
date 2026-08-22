# FORMAL HANDOFF — ARCHITECT → WORKFLOW COORDINATOR — M4 public-model non-scoring observation backend design

Date: 2026-08-22 EDT

Status: COMPLETE — DESIGN ONLY — NO RUN AUTHORITY

## Result

The smallest fail-closed public-model observation backend is fully specified against the cleared `RealBackendProtocol` without modifying the production seam. The future backend has one explicit `control` / `naive` registration, no implicit fallback, exact public Qwen and runtime identities, deterministic public synthetic-prompt generation, process-local consumption of the already-authenticated private token view, standard seven-field receipts, local-only sanitized observations, exact rollback, and deterministic cleanup.

The design makes no scientific claim. It is not scoring, qualification, readiness, equivalence evidence, or a gate decision. It does not authorize a run.

## Immutable result

- Base and cleared seam: `909d2a4a6b4ceafb871e11c1757d873cfa1a4c41`
- Design result: `6644d02337db29fcdceeb38f22afe8801c98cc2b`
- Public testbed tag object: `1994709b41c8e108e0b6f9a15936681f596823af`
- Public testbed peeled commit: `11ea682a7f0fadfa1437a12d882402d90ffd0579`
- Prospective dependency-lock result: `8c303b3262d8ea7640e06fe23671f999f5e01d2c`; persistent-CRITIC review remains explicitly unbound.

## Bound package

| Path | Mode | Git blob | Bytes | Raw SHA-256 |
|---|---:|---|---:|---|
| `.gitattributes` | 100644 | `6e11d8bf98242f18f663e7ac7edf5673bb37c29a` | 7,510 | `7bf33e77f7d76291b180fa4778fbe6007d45119d5e89cfc1e4e6947540c58ca5` |
| `specs/m4_public_model_observation_backend_design_v1.md` | 100644 | `a71a631a1a27c5905603aeaf2717f24f34dd0483` | 7,428 | `ccf746bf7ef98f125bcc7179d28a5baba9bac10baaf7c8e9970b2c14279fac2a` |
| `specs/data/m4_public_model_local_observation_schema_v1.json` | 100644 | `4a16588d0cb6c1adca4f91ee7ed23db8da19c6b1` | 1,982 | `f59829c3baef8a0a4614c2e5a38ed7cb228f09630afcdb39f3609dc00d383a0c` |
| `specs/data/m4_public_model_local_observation_schema_v1.json.sha256` | 100644 | `e79906708a1af10b708da3688060f1b806d56ccb` | 115 | `93b3f6fd7e12a5c3cb81aee43def3804c28efe9ca394202e0e9e0f7efb26a318` |
| `specs/data/m4_public_model_observation_backend_contract_v1.json` | 100644 | `d7d147bb98381f305b0526f5dbbd4d0da3f58188` | 6,314 | `3a4014619a34e79d6bcc2570306af119c14c6d6fb96ece34a52e5ccee4f7dad0` |
| `specs/data/m4_public_model_observation_backend_contract_v1.json.sha256` | 100644 | `1886511228a5d0a44dc7264649b74d084ec6778e` | 119 | `78f04906a7cc2c1e225c8a2cd164961ce2eaf5c1b55f1b8bf03749660b4bf0e7` |
| `specs/data/m4_public_model_observation_backend_test_contract_v1.json` | 100644 | `fa6517da3ac72b0070e14dd59d7f427864953adb` | 2,538 | `ee301de553b324e286223821f84e7ef47809b3d33a7a782030b0b75964d6d4c3` |
| `specs/data/m4_public_model_observation_backend_test_contract_v1.json.sha256` | 100644 | `b202c3d87c61a8cf90ea5f68f4933b76e5f7fdb2` | 124 | `90d2761381824c5ea3af4673ca52181dba012431dbe4a064a8dfd3841c60fe94` |
| `specs/data/m4_public_model_observation_launch_contract_v1.json` | 100644 | `7f44147d2eff6e3bf8117687fb318ff50af1ba05` | 1,724 | `348ca3a14db58967c70fa80ef457028cb0761b309f385f66a689850236f758dd` |
| `specs/data/m4_public_model_observation_launch_contract_v1.json.sha256` | 100644 | `ca3e1498a977c51862290244164beef380ac07ef` | 118 | `108d75dfa0defac23a95e166626484d8f08cfda68d3a7ef153f607886a355999` |
| `specs/data/m4_public_model_observation_prompt_contract_v1.json` | 100644 | `abe964f67707852c9948142d536e264cc2a09362` | 982 | `d1b40087c5cb35cb63d07005ed9450df87116fe8268724b017cfd914983bde76` |
| `specs/data/m4_public_model_observation_prompt_contract_v1.json.sha256` | 100644 | `401a47d52902254f346fd771c0e59bebcd0e24d0` | 118 | `13b343544620ed8cbda1198f35e865aba475780636ebb0bf420e2f39e87d0dd8` |

The canonical manifest adds the routing artifact and the routing-tip `.gitattributes` identity to the complete normalized raw-SHA-256 inventory.

## Verification

- Exact protocol surface and immutable authority objects independently read.
- All five JSON artifacts parsed; the local observation schema passed Draft 2020-12 metaschema validation in the pinned governed OCI without model access.
- All sidecars, model/runtime/law digests, law-semantics raw digest, and three exact generated prompt identities independently reproduced.
- LF attributes, modes, raw bytes, Git blobs, and diff were inspected.
- No model, tokenizer, custody input, protected seed, scoring process, or observation backend was accessed or executed.

## Mandatory stops

Implementation remains blocked until persistent CRITIC clears this design. Any future run additionally requires a reviewed TASK BUILDER implementation, persistent-CRITIC clearance of the dependency lock and implementation, an exact immutable implementation SHA, and a separate Coordinator release. A mismatch or missing authority is a STOP with no retry.

Next event: WORKFLOW COORDINATOR validates the canonical manifest and routes this exact package once to persistent CRITIC for design review.
