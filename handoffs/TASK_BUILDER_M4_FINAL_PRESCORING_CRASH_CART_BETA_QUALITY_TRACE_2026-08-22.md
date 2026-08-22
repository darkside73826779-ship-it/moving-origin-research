# TASK BUILDER QUALITY TRACE — M4 final pre-scoring crash-cart beta

Active implementation: `ba5ddda7811c776dc70347d3ae549b4c822c31be`.

| Requirement | Production branch | Focused evidence |
|---|---|---|
| Literal-LF four-prompt warmup | `warmup_prompt` / `warmup_plan` | all byte sizes, LF count, and SHA-256 values asserted |
| Post-clean-barrier measured sequence | `active_schedule` | 64 ordinals, zero offsets through 15, final 30s offset |
| Eight public fixture families | `public_fixture` | exact payload family sequence asserted |
| HELD-only laws | `held_laws` | ordered five-row no-claim projection asserted |
| Staged evidence | `validate_terminal` | fabricated pre-active evidence and incomplete complete-stage evidence rejected |
| Replica-consumer boundary | `exact_replica_consumer_stop` | mismatch stops consumer |
| No execution authority | `execution_guard`, wrapper | wrapper exits 2 before runtime access |

Focused custody-free result: `python -I tests/run_m4_final_prescoring_crash_cart_tests.py` — exit 0, 15 discovered, 15/15 PASS. Added production tests include `test_invalid_receipt_fails_first_field_and_no_later_evidence` and `test_full_top_level_complete_schema_counterexample`; scheduling/telemetry tests now execute `CrashCartLifecycle.run` and inspect observed dispatch/sample evidence.

Pre-correction proof: `python -I tests/run_m4_final_prescoring_crash_cart_precorrection_probe.py` — exit 0 with `PRECORRECTION_KILLED tests=15 prior=3f9f685`. Mutation command: `python -I tests/run_m4_final_prescoring_crash_cart_mutations.py` — exit 0; required-key schema, receipt backend-code, schedule wait, queue bound, deadline, and observed-telemetry mutants all KILLED. Wrapper: `python tools/run_m4_final_prescoring_crash_cart.py` — governed exit 2 `RUN_AUTHORITY_ABSENT`.

No model, tokenizer, OCI, WSL2, gofast, custody, protected input, scoring, science, or result publication occurred.

WF1 checkout: standard `workflow_checkout.py create` accepted head `a541491fb5a5c5db5e68e3c275f991444888666c` with review result `ba5ddda7811c776dc70347d3ae549b4c822c31be`; `cleanup` removed the verification checkout and receipt successfully.

Final correction-range preflight through `a541491fb5a5c5db5e68e3c275f991444888666c`: gitleaks zero; 12 scan-domain findings reduce to four unique fixed-regex numeric substrings wholly inside required public SHA-256 identities in the canonical manifest. Manual classification: public reproducibility metadata, no personal-contact data or prohibited content, and no suppression.

BF1–BF4 correction: the injected lifecycle now binds paired warmup barriers, reset, post-clean-barrier RNG insertion, all 64 public fixtures, rollback boundary, and cleanup; `validate_terminal` rejects invalid stage/failure pairings and fabricated/incomplete staged evidence; `.gitattributes` is included in the return inventory.
