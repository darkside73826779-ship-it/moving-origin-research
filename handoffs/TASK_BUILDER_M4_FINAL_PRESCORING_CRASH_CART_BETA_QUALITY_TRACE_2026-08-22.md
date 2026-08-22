# TASK BUILDER QUALITY TRACE — M4 final pre-scoring crash-cart beta

Active implementation: `3f9f685a1f88c9f18f916688ce9a574f19e246e8`.

| Requirement | Production branch | Focused evidence |
|---|---|---|
| Literal-LF four-prompt warmup | `warmup_prompt` / `warmup_plan` | all byte sizes, LF count, and SHA-256 values asserted |
| Post-clean-barrier measured sequence | `active_schedule` | 64 ordinals, zero offsets through 15, final 30s offset |
| Eight public fixture families | `public_fixture` | exact payload family sequence asserted |
| HELD-only laws | `held_laws` | ordered five-row no-claim projection asserted |
| Staged evidence | `validate_terminal` | fabricated pre-active evidence and incomplete complete-stage evidence rejected |
| Replica-consumer boundary | `exact_replica_consumer_stop` | mismatch stops consumer |
| No execution authority | `execution_guard`, wrapper | wrapper exits 2 before runtime access |

Focused custody-free result: `python -I tests/run_m4_final_prescoring_crash_cart_tests.py` — exit 0, 13 discovered, 13/13 PASS. Production tests are `ProductionPathCorrectionTests.test_candidate_warmup_zero_failure_rolls_back_resets_and_cleans`, `test_symmetric_barriers_resets_rng_no_priming_and_receipt_ordinals`, `test_schedule_queue_deadline_and_telemetry`, `test_inventory_is_committed_ordered_unique_and_exact`, and `test_strict_schema_counterexamples`.

Pre-correction proof: `python -I tests/run_m4_final_prescoring_crash_cart_precorrection_probe.py` — exit 0 with `PRECORRECTION_KILLED tests=13 prior=ff163541 failures=6`. The probe runs the committed tests against the exact prior source in a disposable checkout. Wrapper: `python tools/run_m4_final_prescoring_crash_cart.py` — governed exit 2 `RUN_AUTHORITY_ABSENT`.

No model, tokenizer, OCI, WSL2, gofast, custody, protected input, scoring, science, or result publication occurred.

BF1–BF4 correction: the injected lifecycle now binds paired warmup barriers, reset, post-clean-barrier RNG insertion, all 64 public fixtures, rollback boundary, and cleanup; `validate_terminal` rejects invalid stage/failure pairings and fabricated/incomplete staged evidence; `.gitattributes` is included in the return inventory.
