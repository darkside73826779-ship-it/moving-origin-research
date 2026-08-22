# ARCHITECT → WORKFLOW COORDINATOR — M4 PASS Evidence EX-PASS2 Execution-Manifest Preservation

**Date:** 2026-08-22 EDT  
**Regime:** B  
**Terminal state:** **COMPLETE**

## Exact lineage and correction

- Accepted execution base: `taskbuilder/m4-tokenizer-topology-fixture-clear-execution @ e462e5bd61bcbad4eb03160129dec2e088de9892`.
- Authoritative review: `critic/m4-tokenizer-pass-evidence-ex-pass1-final-rereview @ a9c059611a06a04bd86d5cd914f878acdf3f8931`.
- Scope: EX-PASS2 only; EX-PASS1 is banked.

The banked LF reconciliation was reconstructed directly on the exact accepted execution head. The active TASK BUILDER execution manifest retains its accepted 8,022-byte topology and every field except the six strictly necessary LF-cascade artifact digests. In particular it preserves:

- `routing_ref_sha=d1f41b81642d70745fe8669d06581cadbfacabed`;
- formal handoff digest `a76477ef267ad06cfbe2a9a249dfdbac856937192f65f747ecbb0a211628334b`;
- the pre-start orchestration-string/no-process check entry;
- final preflight tip `d1f41b81642d70745fe8669d06581cadbfacabed` and complete 25-finding/gitleaks classifications;
- every other execution check, artifact identity, status, finding, hold, and role-extension field.

Mechanical JSON comparison against the accepted execution head proves that only these artifact-map values changed: `.gitattributes`, executable-package JSON/sidecar, test-contract JSON/sidecar, and pre-import wrapper. The active execution manifest validates with the workflow contract validator.

## EX-PASS1 and PASS evidence preservation

A new fresh checkout of this reconstructed lineage with `core.autocrlf=true` again reported `text: set` / `eol: lf` and reproduced direct worktree bytes:

- result: 2,779 bytes / SHA-256 `19a49a9262be81d30866befda3801b2fc97ef23a8d946d3cc1e4b5de189b3158`;
- sidecar: 97 bytes / SHA-256 `9ca61b765be8558551a70966eda34cba8f8978d8c6c968d62bce0e5977e026b4`;
- exact sidecar verification with one LF.

The consumed PASS pair and all execution-evidence bytes outside the declared identity cascade remain unchanged.

## Complete changed active-artifact inventory

| Path | Mode | Bytes | SHA-256 |
|---|---:|---:|---|
| `.gitattributes` | `100644` | 2630 | `87c4d948a1794a95f590cafe8f1e24df8d24ac2ef5bf92cc2283e28ed76faf2e` |
| `handoffs/TASK_BUILDER_TO_COORDINATOR_M4_TOKENIZER_TOPOLOGY_FIXTURE_CLEAR_MATERIALIZATION_PASS.manifest.json` | `100644` | 8022 | `9b3eca4441c4dbc0b1a264a54ffdcdacd249a6df24bc3aec7369296fe75c92dd` |
| `specs/data/m4_tokenizer_executable_package_v1.json` | `100644` | 1948 | `1cf28ddf8aafe608cc92055dcf7ae0cae828ad3abe953bbbd425f1a06a95bd8f` |
| `specs/data/m4_tokenizer_executable_package_v1.json.sha256` | `100644` | 106 | `976b15ac82242cbcd815abb2b5cc7221aedc938fd3d751f04191ac38ccf21d2d` |
| `specs/data/m4_tokenizer_materialization_test_contract_v1.json` | `100644` | 9448 | `edc7f64ba2f1f27d7e5fe62a53e9e3f5e59fea26a527cfe650860298084d936a` |
| `specs/data/m4_tokenizer_materialization_test_contract_v1.json.sha256` | `100644` | 117 | `fed4e0ce79507cefeb09cc9acdac8da19268966517487f38ea03811d5ee3321d` |
| `specs/m4_local_tokenizer_materialization_spec_v1.md` | `100644` | 33561 | `ed4ce57fe935d6576655ba6ee1c9296c94af39c2ded0137063ce61d1a4aa53b1` |
| `tests/run_m4_tokenizer_materialization_tests.py` | `100644` | 9062 | `283afedcd9e53bbf773f82afb664b5174bc6085651baf07a46fa61bccd0942cb` |

No rerun/new operation, OCI/materializer/custody/model/tokenizer access, inference, scoring, seeds, science, durable-state mutation, publication, merge, or gate decision occurred.
