# Existence Proof Analysis — Working Notes

## The core problem (B1/B5)

CRITIC's claim: candidate's `coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.cycle`
is IDENTICAL to naive's `BEFORE_L if e.created_at < L.created_at` because `created_at == cycle`.

So a correct candidate always agrees with naive → agreement = 1.0 → kill (a) fires.
The only way to differ is to be buggy → oracle_agreement < 1.0 → "broken".
"Coherent" (distinguishable AND correct) is unreachable.

## What would make a candidate distinguishable-but-correct?

The candidate must produce answers that:
- MATCH the oracle (correct), AND
- DIFFER from naive `now − created_at` recomputation (distinguishable)

Naive recomputation, as specified, only computes:
`naive_coord_landmark_relative(e, L) = BEFORE_L if e.created_at < L.created_at else (AT_L if == else AFTER_L)`

This is a STATIC comparison of two fixed integers. It does NOT depend on `now`.
A `created_at` column + scan can ONLY answer static "before/after L" queries.

## The key insight: naive CANNOT answer now-dependent queries

If we introduce a query class whose ground truth DEPENDS on `now` (the current cycle),
then naive recomputation from a `created_at` column CANNOT answer it correctly —
because naive only does `e.created_at < L.created_at`, which has no `now` term.

But the candidate's RE-RESOLVING index CAN answer now-dependent queries correctly,
because its coordinates re-resolve as `now` advances.

## Concrete existence proof candidate: "recent-before-L" window queries

Define a NEW query class:
  query_recent_before_L(L, k): "return content_ids of entries e with
    coord_landmark_relative(e, L) == BEFORE_L AND coord_cycle_relative(e) <= k"
  i.e., "entries before L that are within the last k cycles of now"

Ground truth (oracle): { e : e.cycle < L.cycle AND (now - e.cycle) <= k }
  = { e : e.cycle < L.cycle AND e.cycle >= now - k }

Naive recomputation from created_at column:
  naive can compute `e.created_at < L.created_at` (the BEFORE_L part) — YES
  naive can compute `now - e.created_at` (the cycle-relative part) — YES, because
    naive ALSO has `now` (the spec says naive reads `now` too, §6.1 step 2)

WAIT. This is the trap. Naive CAN compute `now - created_at` because it reads `now`.
So naive CAN answer "recent-before-L" queries: { e : e.created_at < L.created_at AND (now - e.created_at) <= k }

So "recent-before-L" does NOT distinguish candidate from naive. Both compute the same thing.
This is the CRITIC's point: naive reads the SAME inputs (created_at, L.created_at, now).

## Re-examining: what does naive NOT have that the candidate DOES have?

Naive has: created_at column, L.created_at, now. (all the raw inputs)
Candidate has: the re-resolving index (stores re-resolved coordinates as first-class values)

The candidate's coordinates are FUNCTIONS of (created_at, L.created_at, now).
Naive recomputes the SAME functions from the same inputs.
→ They MUST agree. This is the CRITIC's correct argument.

## So how can they differ while both being correct?

They can ONLY differ if:
(a) The candidate carries information that naive does NOT have access to, OR
(b) The query's ground truth depends on information naive cannot reconstruct from its inputs

Option (a): The candidate would need to store something beyond (created_at, L.created_at, now).
  But the spec says the candidate's coordinates are functions of exactly these.
  → No extra information by construction.

Option (b): The query's ground truth must depend on something naive cannot compute
  from (created_at, L.created_at, now).

  What can naive NOT compute from (created_at, L.created_at, now)?
  - Anything that depends on the ORDER of appends (naive has created_at = cycle = append order, so it CAN)
  - Anything that depends on the hash chain (naive doesn't read the chain — but the chain is a function of append order, which naive has)
  - Anything that depends on RE-RESOLUTION HISTORY (the sequence of coordinate values over time)

## THE BREAKTHROUGH: re-resolution history / coordinate trajectories

The candidate's re-resolving index, by re-resolving on every append, produces a
TRAJECTORY of coordinate values for each entry over time. This trajectory is information
that a `created_at` column + scan-at-query-time does NOT have.

Specifically: at each append (each `now`), the candidate's `coord_cycle_relative(e)` takes
a value. The SEQUENCE of values (e.g., [99, 98, 97, ..., 0] as now advances from 99 onward)
is a trajectory. Naive recomputes only the CURRENT value (now - created_at); it does not
store the history of values.

BUT: the trajectory is DETERMINISTIC given created_at and now. (now - created_at) at each
step is just (now_t - created_at). So naive COULD recompute the trajectory too, if asked.
→ Still no distinction. The trajectory is a function of the same inputs.

## Re-examining the CRITIC's fix option 1: "incorporate now in a non-canceling way"

CRITIC: "Redefine coord_landmark_relative to incorporate now in a non-canceling way —
e.g., 'is e in the window between L and now' (changes as now advances)"

Let's test this. Define:
  coord_window_relative(e, L) = IN_WINDOW if (L.cycle < e.cycle <= now) else OUTSIDE
  i.e., "e was appended AFTER landmark L but NOT later than now" = "between L and now"

Ground truth (oracle): { e : L.cycle < e.cycle <= now }
Naive: { e : L.created_at < e.created_at <= now }  — naive CAN compute this (it has now)
→ STILL identical. Naive has `now`.

## The real problem: naive has `now`. Any function of (created_at, L.created_at, now) is computable by naive.

The CRITIC is RIGHT that as long as the candidate's coordinates are functions of
(created_at, L.created_at, now), and naive has all three, they cannot differ while both correct.

## So the existence proof requires: a coordinate that depends on something naive does NOT have.

What does naive NOT have?
- Naive does NOT re-resolve incrementally. It recomputes at query time.
- Naive does NOT store intermediate coordinate states.
- Naive does NOT maintain the index structure.

But all of these are IMPLEMENTATION details. The VALUES naive computes at query time
are identical to the values the candidate stores. So the answers are identical.

UNLESS: the candidate's re-resolution introduces information that is NOT recoverable from
(created_at, L.created_at, now) alone.

## What information is NOT recoverable from (created_at, L.created_at, now)?

1. **Whether re-resolution actually happened** — but this is a process fact, not a query answer.
2. **The hash chain state** — naive doesn't read it, but it's a function of append order.
3. **Landmark REGISTRATION timing** — when was L designated a landmark?

WAIT. Here's a real one. Let me think about LANDMARK REGISTRATION.

In the current spec, landmarks are designated at append time (is_landmark flag on the entry).
So L.created_at == L.cycle, and naive knows L.created_at. No distinction.

But what if landmark designation is a SEPARATE event from append? I.e., an entry is appended
at cycle c, and LATER designated a landmark at cycle c' > c. Then:
  - L.designated_at = c' (when it became a landmark)
  - L.cycle = c (when it was appended)
  - L.created_at = c (append position)

Now the candidate's `coord_landmark_relative(e, L)` could be defined relative to
L.designated_at (when L became a landmark) rather than L.cycle (when L was appended).

Naive, reading only created_at, would compute relative to L.created_at = L.cycle = c.
The candidate, tracking landmark designation events, computes relative to L.designated_at = c'.

If c' != c (designation is deferred), these DIFFER. And the candidate is CORRECT
(because the ground truth is "before/after L became a landmark"), while naive is WRONG
(because naive doesn't know about designation events — it only has created_at).

THIS IS THE EXISTENCE PROOF.

## Let me verify this carefully.

Setup:
- Entry e_appended at cycle 5 (e.cycle = 5, e.created_at = 5)
- Entry L_appended at cycle 10 (L.cycle = 10, L.created_at = 10)
- L is designated a landmark at cycle 15 (L.designated_at = 15) — a separate event
- now = 20

Query: "return entries before landmark L"
  - Ground truth (oracle, knows designation): { e : e.cycle < L.designated_at } = { e : e.cycle < 15 }
    → e (cycle 5) IS before L (designated at 15). Oracle includes e.
  - Candidate (tracks designation): coord_landmark_relative(e, L) = BEFORE_L if e.cycle < L.designated_at
    → 5 < 15 → BEFORE_L. Candidate includes e. MATCHES ORACLE. ✓
  - Naive (only created_at): naive_coord_landmark_relative(e, L) = BEFORE_L if e.created_at < L.created_at
    → 5 < 10 → BEFORE_L. Naive includes e. MATCHES candidate here.

Hmm, in this case they agree. Let me find a case where they differ.

Take entry f appended at cycle 12 (f.cycle = 12, f.created_at = 12).
  - Oracle: f.cycle < L.designated_at → 12 < 15 → BEFORE_L. Oracle includes f.
  - Candidate: 12 < 15 → BEFORE_L. Candidate includes f. MATCHES ORACLE. ✓
  - Naive: f.created_at < L.created_at → 12 < 10 → FALSE → AFTER_L. Naive EXCLUDES f.
    → Naive does NOT include f. DIFFERS from candidate. ✓✓✓

So for entry f (appended at cycle 12, which is AFTER L was appended at cycle 10 but
BEFORE L was designated a landmark at cycle 15):
  - Candidate says BEFORE_L (correct: f existed before L became a landmark)
  - Naive says AFTER_L (wrong: naive thinks f is after L because f.created_at > L.created_at)
  - Oracle says BEFORE_L (correct)

candidate_answer == oracle_answer (CORRECT) ✓
candidate_answer != naive_answer (DISTINGUISHABLE) ✓

THIS IS THE EXISTENCE PROOF. The query class is "entries before landmark L" where
landmark designation is a deferred event distinct from append.

## Why this works (the structural reason)

The candidate's `coord_landmark_relative` is defined relative to L.designated_at
(the landmark-designation event), NOT L.created_at (the append event).
Naive recomputes relative to L.created_at (the only timestamp it has).
When designation is deferred (designated_at > created_at), entries appended in the
window [L.created_at, L.designated_at) are:
  - BEFORE_L for the candidate (and oracle) — they existed before L became a landmark
  - AFTER_L for naive — naive compares append positions, not designation positions

The candidate carries information naive does NOT have: the landmark-designation event
timing, which is a SEPARATE event from append. A `created_at` column cannot recover
designation timing because designation is not an append.

## Does this satisfy L4?

L4: "coordinates re-resolve as now advances."
  - coord_landmark_relative(e, L) relative to L.designated_at: when a NEW landmark is
    designated (advancing the landmark registry), existing entries' coordinates relative
    to the NEW landmark are computed. This IS re-resolution (new landmark → new coordinates).
  - coord_cycle_relative(e) = now - e.cycle: re-resolves as now advances. ✓

L4: "A created_at column FAILS this law."
  - A created_at column + scan CANNOT answer "before L" correctly when L's designation
    is deferred, because created_at doesn't record designation events. ✓
  - The candidate's index DOES record designation events (the LandmarkRegistry tracks them). ✓

L4: "the index does NOT collapse to recomputing now - created_at."
  - The candidate's coord_landmark_relative depends on L.designated_at, which is NOT
    recoverable from created_at. So it does NOT collapse. ✓

## Does this satisfy the constitution's L4 test?

L4 test: "self-relative queries ('what did I hold before E?') answered from the index
without scanning; the same item's coordinates measurably shift after N new cycles."

- "what did I hold before E?" → query_landmark_relative(L, BEFORE_L) → answered from
  the index (the LandmarkRegistry + the indexed coordinates). ✓
- "coordinates measurably shift after N new cycles" → when N new landmarks are designated
  over N cycles, existing entries gain new landmark-relative coordinates (re-resolution).
  The coord_cycle_relative shifts by N. ✓

## Is this a MATERIAL change to the candidate mechanism?

YES. The original Candidate 1 defined landmarks as designated at append time
(is_landmark flag on the entry). The revised candidate defines landmark designation
as a SEPARATE event (a designate_landmark(entry) operation that can occur after append).

This is a material change to C1.2 (categorical landmark-relative coordinates) and
potentially C1.3 (the autobiography structure, since designation events must be
recorded in the append-only history).

Per D2 provenance (acceptance criterion 5): this must be labeled as a REVISED DRAFT
CANDIDATE with a distinctness note, NOT silently presented as the same mechanism.

## Does this require changing the locked bars?

NO. The locked bar is `equivalence_agreement <= 0.90`. This bar is PRESERVED.
The candidate now CAN produce agreement < 0.90 (distinguishable) while being correct
(oracle_agreement = 1.0). So "coherent" is REACHABLE. The bar is not flipped, softened,
or redefined. ✓ (acceptance criterion 2)

## Does this fix B5 (L4 violation)?

YES. The candidate no longer IS a created_at column. Its coord_landmark_relative
depends on L.designated_at, which is NOT a created_at column value. L4 is satisfied. ✓

## Summary of the existence proof

Query class: "return content_ids of entries with coord_landmark_relative == BEFORE_L
relative to landmark L" where landmark designation is a deferred event.

Concrete instance:
- L appended at cycle 10, designated a landmark at cycle 15.
- f appended at cycle 12 (after L's append, before L's designation).
- now = 20.
- Oracle: f.cycle (12) < L.designated_at (15) → BEFORE_L → include f. ✓
- Candidate: 12 < 15 → BEFORE_L → include f. MATCHES ORACLE. ✓
- Naive: f.created_at (12) < L.created_at (10) → FALSE → AFTER_L → exclude f. DIFFERS. ✓

candidate == oracle (correct), candidate != naive (distinguishable).
agreement_with_naive < 1.0 is reachable WITHOUT being wrong.
"Coherent" (agreement <= 0.90 AND oracle_agreement == 1.0) is REACHABLE.

The spec is NOT blocked.
