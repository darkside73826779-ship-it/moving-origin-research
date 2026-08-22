# TASK BUILDER → WORKFLOW COORDINATOR — M4 crash-cart reset prior-state equality closure

Terminal state: **COMPLETE — IMPLEMENTATION ONLY — PENDING PERSISTENT-CRITIC REVIEW**.

Substantive implementation `f9d5541b327f65b730b2a73735b8be3fc4f0f8e0` closes the single BF1-R3/BF3-R3 reset prior-state equality finding:

- each candidate and peer reset receipt must bind `prior_backend_state_sha256` to that role's currently bound pre-reset state;
- both receipts validate before either new state is committed;
- valid-wrong-prior candidate and peer regressions prove `RESET_PRIOR_STATE_INVALID`, unchanged pre-rollback state, paired rollback/reset, exactly-once cleanup, zero active dispatch, and no later evidence.

Focused evidence: 28/28 PASS; exact reviewed substantive `56fadc894eb228927ba904b5c0db3e5032385259` killed by the new committed regression; 11/11 deterministic mutants killed with zero survivor/instrument failure; wrapper remains governed exit 2 `RUN_AUTHORITY_ABSENT`. The adjacent quality trace records the reset-boundary audit and exact commands.

Standard `workflow_checkout.py create` and cleanup PASS with review result `56fadc894eb228927ba904b5c0db3e5032385259` and a handoffs-only routing tail.

Substantive-range preflight: gitleaks zero. Two repeated scan-domain findings reduce to one numeric substring wholly inside the required immutable public reviewed-source Git SHA; manually classified as public reproducibility metadata, with no prohibited content or suppression.

All banked BF2-R3, deadline, RNG-domain, LAW_FIDELITY, WF1, BF4, 64-prompt inventory, HELD-law, wrapper, production-seam, and public identity evidence remains preserved. No workload, model/tokenizer/OCI/WSL2/gofast execution, custody/held access, scoring, science, merge, publication, readiness, retry, or gate action occurred.

Next route: WORKFLOW COORDINATOR → authoritative persistent CRITIC for the narrow reset prior-state equality closure review.
