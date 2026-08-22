# Situated-Origin Final Assembly v0.1-alpha

Status: implementation architecture for the isolated final-project assembly branch.
Authority: engineering assembly only. No protected inputs, scoring, scientific verdict, model run, or release authority.

## Decision

The moving origin is the state-owning chassis. It is not a timestamp column, a prompt suffix, or an episodic-memory sidecar.

One `SituatedOriginKernel` owns:

- the irreversible cognitive cycle;
- the append-only autobiographical log;
- environment and optional spatial grounding;
- landmark-relative coordinates;
- access/rehearsal state;
- the thick present;
- bi-temporal facts and supersession;
- provenance-complete episodes;
- claim grounding;
- the future experience-strip attachment point.

Every live mechanism reads a snapshot from that kernel or writes through its transaction boundary. Model backends and evaluators do not own competing histories.

## Runtime flow

```text
public observation
  -> commit input event
  -> immutable situated-origin snapshot
  -> origin-relative retrieval
  -> grounded candidate context / observable-only peer context
  -> one M4 paired fanout
  -> validate staged outputs and claims
  -> commit responses or append TURN_ABORTED
  -> raw evidence tap
```

### Always situated, selectively deliberative

The intended final runtime is continuously situated but does not generate
tokens continuously. A low-cost cadence service keeps the origin, indexes,
current predictions, task state, and regulatory state live. Expensive model
deliberation is triggered only by a user request, a meaningful observed event,
a prediction error, a scheduled consolidation/reflection boundary, or a
future goal/regulatory policy.

```text
observe -> commit -> advance origin -> update present/predictions
        -> evaluate deliberation triggers
        -> retrieve -> deliberate/act/abstain -> commit outcome
```

This avoids confusing nonstop stochastic text generation with thought. The
continuity comes from persistent state and cadence; deliberation remains
bounded, inspectable, and resource-aware.

### Intended final product

The intended product is an always-available situated cognitive service, not an
always-generating language model.  Its inexpensive state kernel remains live
between conversations.  It can accept authenticated observations, advance its
origin, maintain goals and predictions, consolidate experience, and decide
whether an event warrants retrieval, model deliberation, action, or abstention.
The language model is invoked as a bounded reasoning engine inside that service.

At maturity, a user statement such as "yesterday I went to McDonald's" is not
handled by attaching a wall-clock string.  The system resolves "yesterday"
against the current origin and the user's provenance, keeps the user's event
separate from its own autobiography, retrieves its own relevant recorded
experience if one exists, and either relates that grounded experience or says
that it has none.  It may never invent a personal event, place, action, or
continuous experience to make the answer sound natural.

The system is intended to exhibit six coupled capabilities:

1. **Continuity:** one durable life/episode identity and one advancing cognitive
   clock survive individual model calls.
2. **Moving-origin memory:** an immutable event acquires a changing relation to
   the current origin without rewriting its history.
3. **State-conditioned access:** temporal distance, current-state divergence,
   validity, rehearsal, goals and prediction error change what becomes
   accessible, rather than merely changing metadata in a report.
4. **Anticipation and repair:** the thick present produces bounded predictions;
   later observations create grounded prediction-error events that can trigger
   learning, deliberation or correction.
5. **Provenance-grounded self-reference:** claims about the system's past,
   location, actions or goals resolve to committed evidence or abstain.
6. **Selective agency:** goals may trigger bounded deliberation and receipted
   actions, but never an unlogged hidden action or continuous stochastic loop.

This is the line the project is trying to push: from a stateless model that
reconstructs a persona from a prompt toward a persistent, temporally situated
system whose remembered history has demonstrable causal effects on future
behavior.  It is not, by itself, a claim of consciousness or AGI.

Committed autobiography never rolls back. Backend, adapter, prompt-stage, and output-stage state may roll back. After an input commit, a failed turn is recorded honestly rather than erased.

## Existing component placement

| Component | Placement | Required adapter |
|---|---|---|
| E1 `Autobiography` | canonical cadence/log semantics | persistent expected-head transaction wrapper |
| E1 `EgocentricIndex` | origin-relative coordinates | durable event/landmark IDs |
| M3 L1 formula | live access field and offline evaluator | public same-clock access ledger |
| M3 L3 state | thick present and offline evaluator | incremental update with batch equivalence |
| M3 L5 store | bi-temporal fact graph | stable identity and unified acquisition clock |
| L6 fixture | provenance-complete episodic memory | public write/query; remove global fixture ownership |
| M4 adapters/fanout | sole paired dispatch boundary | strict real backend and role-context policy |
| Crash-cart controls | vehicle schedule/deadline/telemetry rules | one orchestrator, not a second lifecycle owner |
| M1/M3/M4 evaluators | post-run evaluator plane | immutable evidence-bundle consumers only |
| Exact tokenizer and Qwen roots | runtime inputs | identity check and final-prompt token budgeting |

## Memory tiers

1. Transaction journal: staged/commit/recovery markers; not cognitive history.
2. Autobiographical ledger: immutable system of record.
3. Materialized views: origin index, fact graph, access ledger, thick present, provenance graph. Every view binds `source_log_head`.
4. Consolidated memory: regenerable summaries with exact source-event provenance.
5. Future E3 experience strip: fast-plastic projection of committed events, never the source of truth.

### Multi-resolution retention and principled forgetting

The live system must not keep every event at full resolution in the active
working set.  It separates accessibility, representation fidelity, and
evidence retention:

1. the thick present retains exact high-resolution state for the current
   interaction window;
2. a recent episodic buffer retains detailed, readily retrievable events;
3. consolidation derives durable facts, relationships, episode summaries and
   impression traces with exact `derived_from` provenance;
4. cold autobiography stores compressed/chunked source events that can be
   rehydrated and verified against their committed identities; and
5. explicitly pinned identity, commitment and safety records are exempt from
   ordinary accessibility decay.

Ordinary events may decay out of active retrieval without being rewritten or
silently deleted.  Retention is governed by an auditable signal vector rather
than a model-selected scalar: age, rehearsal, causal novelty, prediction error,
goal consequence, observed outcome, dependency count, user pinning and explicit
retention/privacy policy.  A quiet event can become cold while its consolidated
fact or fast-plastic impression remains active.  Relevance discovered later may
rehydrate the source evidence.

Deletion is a separate explicit policy operation, not an accidental consequence
of memory decay.  Every compacted or consolidated representation keeps its
encoding origin, source log range, consolidation receipt and current origin
relation.  A summary or impression never becomes evidence of an event unless
that provenance resolves.

## Situated origin

The origin includes logical time plus provenance-bound environment coordinates. Civil time and physical location are optional observations, not invented defaults. `Unavailable(reason)` is a first-class value.

Memory distance is multi-axis:

- cycle distance;
- landmark relation;
- acquisition/supersession distance;
- world-validity relation;
- task phase;
- environment/space relation when known;
- current-state divergence.

The same event therefore changes its relation to the system as the origin advances without its historical record being rewritten.

## Candidate actuation

The candidate receives grounded memory records containing useful content, source, encoding origin, current origin distance, validity, and supersession. The peer receives no privileged origin capability. Both retain the same public question and governed shared token view.

The compiler may not receive or render a requested answer label. Model output must be reasoned from memory evidence and coordinates.

The paired crash-cart path uses the structured context actuator. The separate
single-model development path implements an origin-indexed soft-prefix actuator
through `inputs_embeds`: base-model parameters remain frozen while a bounded
prefix projection may change. Both paths retain the same ledger/provenance
contract; neither permits a projection to become autobiographical truth.

## Current causal evidence and retained product boundary

One fixed, non-scoring local-model observation tested the smallest relevant
temporal behavior.  With Qwen's native chat template and the complete public
conversation in active context, the frozen 4B model correctly predicted 5 of 6
subsequent observations.  Its sole error was the deliberately unexpected rule
reversal; it then adapted on the next observation.  Four distinct final queries
about current state, next state, temporal predecessor, and its prediction-error
trajectory were all answered correctly.  Every turn was committed through the
situated ledger and deterministic replay reproduced its head.

That result establishes a capable **working-context control**, not durable
plastic memory.  Two prospective compressed-state mechanisms were also tested
and rejected:

- sequential observation-loss prefix updates answered 0 of 4 fixed held-out
  queries under the original raw interface and only the same 1 of 4 as the
  no-state baseline after the native chat interface was corrected; and
- active-context teacher answers were all correct and prefix training loss fell
  near zero, but transcript-free paraphrases again scored 1 of 4, identical to
  baseline.  This was cue memorization, not transferable state.

No parameter tuning followed those failures.  The rejected update and
consolidation implementations are not product code.  The retained alpha
therefore consists of the frozen model's native working context plus the
append-only origin/provenance system.  `SoftPrefixExperienceStrip` remains an
experimental port and is not load-bearing evidence of an evolving self or world
model.  A durable compressed neural state remains unbound until a prospective
mechanism beats active-context, no-state, wrong-state, and restart ablations on
unseen prompts.

## Claim grounding

- Self-experience claims require supporting autobiographical event IDs.
- Relative-time claims require a resolvable temporal anchor.
- place claims require an authenticated runtime, interaction, virtual-world, or physical-world anchor;
- user experiences remain attributed to the user;
- unsupported claims are rejected or rewritten as uncertainty.

Model text alone never becomes autobiographical truth.

## Fast-plastic experience strip — alpha vertical slice

The experience strip is not an episodic database, a timestamped embedding, or
a second copy of the autobiographical log.  It is intended to be a bounded,
model-adjacent **plastic impression state**: a moving field of fast weights,
low-rank deltas, learned key/value state, or an equivalent mechanism that
captures how a committed experience changed the system.

For a committed event at origin `t`, the alpha strip accepts a bounded opaque
trace from an injected model actuator and binds its exact bytes, update norm,
importance, prediction-error input, codec identity, actuator identity, and
source event to the same origin. The current learned-prefix development
actuator derives that trace from a frozen local model. Later implementations
may derive richer updates from the event representation, pre-event state, post-event state,
prediction error, confidence change, goal/relevance signal, and observed
outcome.  The update is stamped with the same origin and provenance as the
event.  As the origin advances, traces may decay, interfere, reinforce, merge,
or consolidate according to an explicit policy.  The effective strip at `t+n`
therefore represents accumulated consequences of experience, not a bag of
records.

Reading the strip must influence model computation directly through a governed
adapter/activation interface.  Merely rendering its values into a prompt or
showing them in telemetry does not count as implementation.  The immutable
ledger remains the source of truth; the plastic strip is a learned projection
whose state must be reproducible when determinism is claimed, attributable to
source events, and fail closed if it diverges from its ledger-bound receipt.

The reserved port exposes:

```text
write_experience
advance_origin
retrieve_by_origin_distance
consolidate
compare_to_log
```

`UnboundExperiencePort` remains the default fail-closed configuration.
`SoftPrefixExperienceStrip` is activated only by explicit injection. Its head
advances from the same origin, it accepts only committed ledger events, resolves
retrieval by event identity/origin distance, supports bounded supersession and
consolidation, and must reproduce provenance before supporting a claim. The
alpha soft-prefix backend is a vertical slice, not completion of every E3
acceptance criterion below.

The minimum future E3 receipt binds the prior strip head, event/log head,
update identity, update norm/budget, prediction-error input, consolidation
operation, resulting strip head, and exact actuator identity.  No update may
rewrite base-model weights silently or become autobiographical evidence by
itself.

E3 is accepted only if decisive tests show all of the following:

- the same event content can leave different impressions when pre-state,
  prediction error, or goal impact differs;
- a retained impression changes a later internal activation and observable
  response under fixed public input;
- removing or permuting the relevant trace destroys that specific effect;
- unrelated traces do not produce the effect;
- consolidation preserves declared behavior while its provenance still resolves
  to source events;
- replay or checkpoint restoration reproduces the declared strip identity; and
- the static ledger alone, prompt-only recall, and a timestamped vector store do
  not reproduce the full coupled result.

## Future deliberation and agency sockets

The chassis reserves central—not sidecar—interfaces for:

- `CadenceScheduler`: advances bounded origin cycles without invoking the LLM
  on every tick;
- `PredictionMonitor`: compares the thick present's protention to subsequent
  committed observations and emits a grounded prediction-error event;
- `GoalStatePort`: stores active goals, provenance, priority and completion in
  the canonical state;
- `DeliberationPolicy`: decides whether an event warrants model inference,
  retrieval-only handling, consolidation, an action, or abstention;
- `ActionPort`: stages externally consequential actions and commits their
  receipts only after observed completion;
- `ReflectionConsolidator`: schedules ledger-grounded summarization without
  rewriting source experience.

These remain typed unavailable until implemented. None may create a second
clock, hidden memory, unlogged goal, or unreceipted action.

## Immediate defects retired by design

The earlier local wiring alpha must not be used for a behavior conclusion because it:

- rendered the ground-truth relation into candidate context;
- proved literal formatting changes rather than semantic load-bearing behavior;
- advanced unified state outside M4 rollback ownership;
- reused private/batch/global-fixture L3/L5/L6 APIs;
- split lifecycle ownership between crash-cart and fanout;
- exercised only zero-offset schedule entries;
- did not budget-check final role-specific prompts.

The permanent alpha must close these before a model loads.

## Build order

1. Canonical types, transaction journal, append-only log, replay, and origin frame.
2. Persistent L1/L3/L5/L6 adapters and origin-relative retrieval.
3. Grounded claim guard and ground-truth-free actuator.
4. Strict candidate/peer backend and single vehicle orchestrator.
5. Semantic load-bearing tests and no-model vehicle test.
6. Real dual-model crash cart retaining raw behavior and no aggregate score.
7. Later L7/L10, L8/L14, E3, and M5 L15-L17 mechanisms under their own gates.
8. Always-live cadence, prediction-error triggers, grounded goals, bounded
   deliberation and receipted action under explicit resource limits.

## Acceptance

The assembly is testable only when:

- one committed event advances every live mechanism through one kernel;
- all views share the current ledger head and deterministic replay reproduces the frame;
- no model call occurs without a frame-bound context receipt;
- no answer label or control-arm label enters prompts;
- every claimed component changes semantic selection/content/state when made decisive;
- peer privilege is absent;
- all failure paths retain honest history, discard partial model evidence, and clean up exactly once;
- no active path depends on private evaluator fixtures;
- every missing capability is typed, visible, and non-callable.

The word “revolutionary” is not an acceptance status. The later L16 test must show a diachronic capability that no meaningful subset or frozen/static system can reproduce. Until then, this is a serious architecture hypothesis under construction.

## Standout-result acceptance

The final system is not accepted as a substantive advance merely because it
retains more text or improves one benchmark average.  A custody-free precursor
and later governed evaluation must demonstrate all of the following:

- the same public observation produces a reproducibly different grounded
  response after a relevant committed experience, with no answer label supplied;
- moving the origin while preserving event bytes changes temporal relation and,
  when decisive, retrieval or behavior;
- perturbing thick-present state, valid-time facts, access history, or goals can
  make a predeclared semantic difference, while decorative perturbations do not;
- long-horizon recall survives process restart through deterministic replay;
- prediction errors alter later retrieval or deliberation under an explicit
  policy;
- unsupported autobiographical, temporal and spatial claims abstain;
- an ablation matrix shows the coupled result is not reproduced by a timestamp,
  prompt-only memory, vector-search sidecar, or any other meaningful subset;
- resource use is bounded: the always-live kernel is cheap and model inference
  occurs only at recorded deliberation boundaries.

Until these conditions are observed, the appropriate description is
"integrated situated-origin research alpha," not AGI and not a revolutionary
result.
