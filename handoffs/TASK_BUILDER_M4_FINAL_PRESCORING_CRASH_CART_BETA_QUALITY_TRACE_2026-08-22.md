# TASK BUILDER QUALITY TRACE — M4 final pre-scoring crash-cart beta

Implementation: `738878ab3618d6058f0725caa7e3f0f0388cb59f`.

| Requirement | Production branch | Focused evidence |
|---|---|---|
| Literal-LF four-prompt warmup | `warmup_prompt` / `warmup_plan` | all byte sizes, LF count, and SHA-256 values asserted |
| Post-clean-barrier measured sequence | `active_schedule` | 64 ordinals, zero offsets through 15, final 30s offset |
| Eight public fixture families | `public_fixture` | exact payload family sequence asserted |
| HELD-only laws | `held_laws` | ordered five-row no-claim projection asserted |
| Staged evidence | `validate_terminal` | fabricated pre-active evidence and incomplete complete-stage evidence rejected |
| Replica-consumer boundary | `exact_replica_consumer_stop` | mismatch stops consumer |
| No execution authority | `execution_guard`, wrapper | wrapper exits 2 before runtime access |

Focused custody-free result: `python -I tests/run_m4_final_prescoring_crash_cart_tests.py` — 8/8 PASS. No model, tokenizer, OCI, WSL2, gofast, custody, protected input, scoring, science, or result publication occurred.

BF1–BF4 correction: the injected lifecycle now binds paired warmup barriers, reset, post-clean-barrier RNG insertion, all 64 public fixtures, rollback boundary, and cleanup; `validate_terminal` rejects invalid stage/failure pairings and fabricated/incomplete staged evidence; `.gitattributes` is included in the return inventory.
