# REBECCA M3 CONTINUATION/SCOPE GATE RULING

**Date:** 2026-08-15  
**Authority:** Rebecca Mcclintic  
**Serves:** M3 Continuation/Scope Gate  
**Repository basis:** GitHub main `7b690a98d9e100e8625173a37113710bac690811`

## Ruling

**M3/E2 V4 scope: GO.**

I approve the M3/E2 V4 scope covering L1, L3, L5, and L6, as merged on main at `7b690a98d9e100e8625173a37113710bac690811` and independently cleared by CRITIC in `reviews/critic_m3_e2_spec_rereview_v4.md`.

The approved specification package is:

- `specs/m3_e2_spec_amended_v4.md`
- `specs/m3_e2_spec_changelog_v4.md`
- `reviews/critic_m3_e2_spec_rereview_v4.md`
- `state/STATE.md`

## Timebox

**APPROVED: 4 sessions / 8 calendar days.**

The M3 timebox starts with this ruling on 2026-08-15. The binding tripwire is reached at any of:

- session 2 elapsed;
- day 4 elapsed;
- any law's instrument-failure branch remains unresolved past one full session; or
- the pre-registered ≥2-of-4 escalation trigger fires.

At a tripwire, the only permitted dispositions are:

1. continue within the existing cap;
2. pause or stop; or
3. close M3 and separately propose a newly scoped future milestone with its own scope, bars, and gate.

There is no cap-revision branch.

## L5 §1.1 proposal

No ruling is made here on the proposed L5 scan-avoidance operational bar. It therefore remains **diagnostic-only and non-gating**:

- candidate per-walk latency growth from 250-entry to 1000-entry history ≤ 2.0×; and
- fair-naive full-scan comparator growth over the same range ≥ 4.0×.

Adoption, rejection, or modification of that proposal requires a separate explicit Rebecca ruling.

## Authorization boundary

This GO authorizes:

1. **RECORDER** to publish this ruling to the private repository, append the corresponding provenance entry, and update operational state to reflect the ruling; then
2. **INTEGRATOR** to prepare the self-contained M3 implementation task specification and courier architecture only.

This ruling does not authorize:

- implementation or code changes;
- activation of a build cell or TASK BUILDER;
- diagnostic execution;
- scoring execution or a courier scoring run;
- exposure or use of hold-out seeds; or
- any L15–L17 integration claim.

The task specification must receive independent CRITIC clearance before any build authorization returns to Rebecca.

## Standing protections

All existing governance remains binding, including:

- authority chain: Rebecca > constitution and adopted rulings > approved specification > agent judgment;
- Persistence Doctrine D1–D5;
- O-14 no re-run on failure;
- O-15 development runs are diagnostic-only;
- scoring only through Rebecca's supervised-executor courier channel;
- at least two scoring seeds unseen in development;
- full L18 control battery;
- L9 hard fence for any learned or nonlinear retrieval channel;
- no integration claim without the prescribed L15–L17 evidence; and
- no renaming, suppressing, or reframing negative results.

## Next authorized handoff

**RECORDER** first publishes this ruling and its state/provenance attestation from the verified current main. RECORDER must not alter the ruling, authorize build work, or start INTEGRATOR.

After Rebecca merges that custody-only branch, **INTEGRATOR** prepares the self-contained M3 implementation task specification and courier architecture from the approved V4 package. INTEGRATOR must stop after submitting those artifacts for independent CRITIC review.

No other role is authorized to begin out of sequence.

— Rebecca Mcclintic
