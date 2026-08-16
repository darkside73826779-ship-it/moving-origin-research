# Task Spec — E1 Moving-Origin Experiment (`e1_experiment.py`)

> **For:** TASK BUILDER · **Issued by:** INTEGRATOR · **Date:** 2026-08-15
> **Source:** `/home/user/workspace/e1_spec.md` (REVISED DRAFT v3 + Rebecca Q2/Q3 incorporations, commit `7cb78c453c58b6daa52fc718c5d8fa2c1909b194`).
> **Purpose:** This is a self-contained implementation brief. The TASK BUILDER implements `e1_experiment.py` + `requirements.txt` against this spec without reading any other file. Every value below is LOCKED (from M0 / Rebecca's ruling) unless explicitly noted as a diagnostic. Do NOT invent, lower, raise, or rename any bar.

---

## 0. Deliverable & courier packet

### 0.1 Artifacts to produce
- `e1_experiment.py` — one self-contained script.
- `requirements.txt` — pinned deps (§0.3).

### 0.2 Launch command (scoring run, through Rebecca's courier channel only)
```bash
python e1_experiment.py --seeds 42,43,44 --output-dir ./e1_output
```

### 0.3 Pinned dependencies (`requirements.txt`)
```
python==3.11
numpy==1.26.4
scipy==1.13.1
```
No other third-party packages. `hashlib` (SHA-256) is stdlib. If runtime python != 3.11.x, log it in `e1_manifest.json.deviations_logged` (non-blocking).

### 0.4 Output files (5, written to `--output-dir`)
1. `e1_run_results.json` — full results table (§8.1).
2. `e1_invariants.json` — kill-condition verdicts + invariants (§8.2).
3. `e1_manifest.json` — courier round-trip log (§8.3).
4. `e1_run.log` — raw stdout/stderr capture, UTF-8 encoded.
5. `e1_profile.json` — L20 drift baseline + self-test (§8.5).

### 0.5 Hard constraints (binding)
- **No bar invention, lowering, or raising.** All numeric bars carried forward verbatim from M0 / Rebecca's ruling.
- **No re-run-on-failure** (Ruling O-14 — result laundering is forbidden). A failing kill condition is never resolved by re-running until it passes.
- **Development runs are diagnostic-only, non-scoring** (Ruling O-15). Build-cell sandbox runs are never scored, never logged as results. Only Rebecca's courier-returned artifacts feed verdicts.
- **The candidate is the system under test** (NOT a 7th control arm). `config.candidate` is a separate field.
- All stochasticity is seeded. No external data files; all data synthesized in-process from the seed.

---

## 1. Candidate mechanism (Candidate 1.1) — data structures

Build exactly these structures. The candidate is a **landmark-relative re-resolving index over an append-only hash-chained autobiography, where landmark designation is a deferred event distinct from append.**

### 1.1 The Autobiography (append-only, hash-chained)
An append-only sequence of entries. Each entry `e`:
- `e.cycle` — the cycle counter at append time (strictly monotone; starts at 0).
- `e.created_at` — autobiography position at append time (equals `e.cycle` at append). This is the L11 "one clock" — autobiography position, NOT wall-clock.
- `e.payload` — opaque content blob. For E1, carries:
  - a `content_id` (deterministic per `i`) for comparing index answers to oracle/fair-naive by content identity.
  - a known ground-truth landmark-membership bit (`is_landmark`).
  - a 32-d synthetic feature vector `v(e)` (§6.iii consumer).
- `e.prev_hash` — SHA-256 hash of the preceding entry's serialized record. `e_0.prev_hash = SHA256("genesis")`.
- `e.self_hash` — SHA-256 hash of THIS entry's serialized record, computed over `(cycle, created_at, payload, prev_hash)`.
- The autobiography records TWO classes of events, both append-only and hash-chained, both readable by the fair-naive arm:
  1. **append events** — a new entry appended with a payload.
  2. **designation events** — an existing entry designated a landmark; recorded as a special entry with `event_type = "designation"`, a reference (`ref`) to the designated entry, and the current cycle as `designated_at`.
- No entry is ever mutated, deleted, or reordered. The cycle counter is strictly monotone across restarts (persisted).

### 1.2 The Landmark (designation event, distinct from append)
A landmark `L` is an entry that has been **designated** via `designate_landmark(entry)`. Designation is a SEPARATE event from append. Each landmark `L` carries:
- `L.cycle` — cycle at which `L` was appended (append position).
- `L.created_at` — equals `L.cycle` (append position).
- `L.designated_at` — cycle at which `L` was **designated** a landmark (designation position). `L.designated_at ≥ L.cycle` always; if designated at append time, `L.designated_at == L.cycle`.
- **The designation event — not the append event — is the reference point for landmark-relative coordinates.**
- Landmarks are designated deterministically per seed (§2.3).

### 1.3 The EgocentricIndex (re-resolving structure)
For each entry `e`, the index stores **self-relative coordinates** that are functions of the current `now` (cycle of most-recently-appended entry) and the landmark registry (set of designated landmarks + their `designated_at`):
- `coord_cycle_relative(e)` = `now − e.cycle` ("how many cycles ago was e appended, relative to now"). Re-resolved on every append.
- `coord_landmark_relative(e, L)` ∈ `{BEFORE_L, AT_L, AFTER_L}` computed as:
  - `BEFORE_L` if `e.cycle < L.designated_at`
  - `AT_L` if `e.cycle == L.designated_at`
  - `AFTER_L` if `e.cycle > L.designated_at`
  - (Reference point is `L.designated_at`, NOT `L.cycle`.)
- **Re-resolution property (heart of L4):** on append (advancing `now`), `coord_cycle_relative(e)` for every prior entry `e` changes (increases by 1). On designation of new landmark `L_new` (advancing landmark registry), `coord_landmark_relative(e, L_new)` for every existing `e` is newly computed; entries whose `cycle` falls in `[L_new.cycle, L_new.designated_at)` shift from `AFTER_L` to `BEFORE_L` relative to `L_new`.
- **Operational distinctness (heart of property (ii)):** the index does NOT recompute by scanning the full log at query time. It maintains incrementally re-resolved state:
  - `coord_cycle_relative` via an offset counter (O(1) amortized per append — store a base offset and per-entry base cycle; re-resolution is `offset += 1`, not a per-entry scan). **This is the candidate's C1.1 claim.**
  - `coord_landmark_relative` via a pre-computed lookup structure (O(1) or O(log n) per query; computed ONCE per designation, O(n) per designation, not per query).
  - Re-resolution is O(1) amortized per append (offset-increment trick) and O(n) per designation (one pass). NOT O(n) per query.

### 1.4 Feature vectors (32-d synthetic, deterministic per seed)
Each entry's `payload` carries `v(e) ∈ ℝ^32`, generated deterministically per seed:
```
v(e) = rng.standard_normal(32)  where rng = numpy.random.default_rng(seed * 100000 + e.cycle)
```
Stored at append time, never changes. Ground-truth content for the property (iii) consumer.

---

## 2. Candidate mechanism (Candidate 1.1) — operations

Implement exactly these operations. Candidate 1.1 makes 5 mechanistic choices (C1.1–C1.4, with C1.3 split into a/b):
- **C1.1** Offset-counter re-resolution: `coord_cycle_relative` stored as `(base_cycle, offset)`, re-resolved by incrementing a single offset.
- **C1.2** Categorical landmark-relative coordinates relative to designation events: `BEFORE_L / AT_L / AFTER_L` (3-valued), defined relative to `L.designated_at`.
- **C1.3a** Append-only hash-chained autobiography (SHA-256 chain).
- **C1.3b** Persisted monotone integer cycle counter.
- **C1.4** Landmark designation as a deferred event (separate `designate_landmark()` op, recorded in history, distinct from append).

### Op 1 — `append(payload, is_landmark=False)`
Append a new entry. Increment the cycle counter (strictly monotone). Compute `prev_hash` from last entry's `self_hash`. Compute `self_hash`. Store the entry. If `is_landmark`, equivalent to `append` followed immediately by `designate_landmark` at the same cycle (`L.designated_at == L.cycle` — an "immediate" landmark). **Then re-resolve the index** (Op 2). Return the new `now`.

### Op 2 — `re_resolve_index()`
Invoked after every append AND after every designation. Incremental update, NOT a full scan:
- `coord_cycle_relative(e)` for all prior `e`: increment by 1 (single bulk increment, O(1) amortized via offset counter — store base offset + per-entry base cycle; re-resolution is `offset += 1`).
- `coord_landmark_relative(e, L)` for existing `(e, L)` pairs: stable (designated_at and cycle never change). For a NEW landmark `L_new`: compute `coord_landmark_relative(e, L_new)` for all existing `e` — single comparison `e.cycle < L_new.designated_at` per entry, O(n) total, done ONCE per designation. Entries in `[L_new.cycle, L_new.designated_at)` shift from "not yet relative to L_new" to `BEFORE_L_new`.
- **Re-resolution is O(1) amortized per append and O(n) per designation, NOT O(n) per query.**

### Op 3 — `query_landmark_relative(L, relation)`
Return the set of entries with `coord_landmark_relative == relation`. Answered from the index (lookup over indexed coordinate), NOT a scan. (Unbounded variant — answer-set grows with history; latency NOT measured on this; used for raw_answer_size diagnostics only.)

### Op 4 — `query_landmark_relative_bounded(L, relation, k)`
Return the **k most recent** entries (highest `cycle`) with `coord_landmark_relative == relation`. Answered from the index. **Bounded-output variant used for the latency test (d1).**

### Op 5 — `query_membership(e, L, relation)`
Return a single boolean — whether `coord_landmark_relative(e, L) == relation`. O(1) lookup. **Second bounded-output probe for the latency test (d1).**

### Op 6 — `designate_landmark(entry)`
Designate an existing entry as a landmark. Increment the cycle counter (designation is an event in the append-only history — it advances `now`). Record a designation event in the autobiography (`event_type = "designation"`, `ref = entry`, `designated_at = new_now`). Register in `LandmarkRegistry` with `L.designated_at = new_now`. **Then re-resolve the index** (Op 2) — compute `coord_landmark_relative(e, L_new)` for all existing `e`. Return the new `now`. **This creates the deferred-designation landmarks that supply the state-dependent battery's material.**

### Op 7 — `query_cycle_relative(window)`
Return entries with `coord_cycle_relative` in a window (e.g., "last 5 cycles"). Answered from the index.

### Op 8 — `verify_chain()`
Recompute the hash chain from genesis to `now`; confirm every `prev_hash` matches the predecessor's `self_hash`. Returns `{valid: bool, broken_at: cycle|null}`. **This IS a scan by design (it audits the chain); the "without scanning" requirement applies to QUERIES, not to AUDIT. Latency bar is measured on `query_*`, NOT `verify_chain`.**

---

## 3. Synthetic autobiography generation (deterministic per seed)

All RNG from `numpy.random.default_rng(s)`.

### 3.1 Constants (all LOCKED, not tuned)
| Parameter | Value | Notes |
|---|---|---|
| `N_cycles` | 10 | locked N — shift measured over 8 appends + 2 designations = 10 cycles |
| `N_entries_initial` | 100 | 1× history baseline |
| `N_entries_final` | 1000 | 10× history latency probe (1000 = 10 × 100) |
| `N_landmarks` | 10 | deterministically per seed |
| `N_landmarks_immediate` | 8 | designated at append (`L.designated_at == L.cycle`) |
| `N_landmarks_deferred` | 2 | designated during shift probe (`L.designated_at > L.cycle`) |
| `seeds` | [42, 43, 44] | 3 seeds |
| `N_queries` | 200 | landmark-relative queries per measurement point, per seed |
| `N_state_dependent_query_points` | 5 | history sizes: 100, 250, 500, 750, 1000 |
| `N_consumer_queries` | 50 | property (iii) consumer queries per seed |
| `consumer_feature_dim` | 32 | feature vector dimension |
| `consumer_tau` | 50 | recency decay constant |
| `consumer_k` | 10 | top-k retrieval |
| `timing_repetitions` | 100 | minimum reps per query per history-size point |

### 3.2 Generation procedure (per seed `s`)
1. **Initial build (1× history, 100 entries):** append 100 entries. For entry `i ∈ {0..99}`:
   - `payload_i` = synthetic item with `is_landmark_i = True` if `i` is in a seeded random 10% subset (10 landmarks among 100) else `False`.
   - `content_id` deterministic per `i`.
   - `cycle_i = i` (cycle counter increments per append; `created_at_i = i`).
   - **Immediate landmarks:** of the 10 landmark-eligible entries, 8 are designated at append time (`is_landmark=True` on the `append` call → `L.designated_at == L.cycle`). The 8 are chosen deterministically (seeded) from the 10.
   - **Deferred landmarks:** the remaining 2 landmark-eligible entries are appended WITHOUT `is_landmark` (in the autobiography but NOT yet landmarks). Designated during the shift probe (step 2).
2. **The 10-cycle shift probe (N=10):** after initial build (`now = 99`), perform 10 cycles. Each cycle is EITHER an append OR a designation:
   - **Cycles 100–101:** designate the 2 deferred landmarks (one `designate_landmark` call per cycle, advancing `now` to 100, then 101). These are the deferred-designation events: `L.designated_at = 100` and `L.designated_at = 101` for the two deferred landmarks (whose `L.cycle` is in the initial 0–99 range).
   - **Cycles 102–109:** append 8 more entries (`i ∈ {100..107}`), one per cycle, re-resolving after each. After each append, measure `coord_cycle_relative` shift on a fixed probe set of 10 prior entries (seeded). **The shift check (kill c)** confirms `coord_cycle_relative` increased by exactly 1 per append for every probed entry.
3. **The 10× history latency probe:** after the shift probe, continue appending until `now = 999` (1000 entries total = 10× the initial 100). At `now = 999`, measure query latency. Compare to latency measured at `now = 99` (1× history).
4. **The state-dependent scaling battery (property (ii)):** at each of the 5 history-size points (100, 250, 500, 750, 1000 entries), measure per-query latency for BOTH the candidate and the fair-naive arm on the state-dependent query battery (§6.ii). Fit a scaling curve for each.

### 3.3 Intermediate artifacts (construction-bug guard — REQUIRED)
- **N11 (intermediate chain_integrity):** record `chain_integrity` as a separate boolean AFTER (a) the initial build (now=99), (b) after the shift probe (now=109), (c) after the 10× growth (now=999). Lets JUDGE distinguish construction break (chain never valid) from re-resolution break (chain valid initially, breaks later).
- **N12 (per-append shift):** for each of the 8 appends in the shift probe, record whether the shift occurred (`shift_per_append` array of 8 booleans). Lets JUDGE distinguish wiring defect (never shifts) from partial mechanism failure (some shifts, some not).

### 3.4 The query set (deterministic per seed)
`N_queries = 200` landmark-relative queries, generated per seed:
- For each query `q ∈ {0..199}`: pick a landmark `L_q` (seeded, from the 10 landmarks — 8 immediate + 2 deferred) and a relation `r_q ∈ {BEFORE_L, AFTER_L}` (seeded, ~50/50). Query asks: "return the set of content_ids of entries with `coord_landmark_relative == r_q` relative to `L_q`."
- **Ground-truth answer** computed by the independent oracle arm (§5 arm 3): perfect-knowledge structure that scans the autobiography AND designation events once and returns the exact set. Reference for property (i) (kill (f)).
- **Fair naive arm** reads the SAME event log (including designation events) and computes the SAME answers by scanning at query time. By Rebecca's theorem, fair-naive ≡ oracle on answers. Cost is the property (ii) probe.

---

## 4. The 6 control arms (exact implementation)

For each arm, produce a query-answer set per seed (the set of content_ids returned for each of the 200 queries) AND, for candidate and fair-naive, per-query latency at each history-size point. All stochasticity seeded. Each arm is a complete alternative to the candidate.

### Arm 1 — `frozen origin`
- Build the egocentric index once at the initial build (`now = 99`), then **never re-resolve** it during the shift probe (designation events, appends) or the 10× growth.
- Answer the 200 queries from the frozen index.
- The index's `coord_cycle_relative` is frozen at `now=99` values; `coord_landmark_relative` is frozen — the frozen index does NOT know about the 2 deferred landmarks designated at cycles 100–101.
- **ALSO serves as the ablation arm for property (iii):** the downstream consumer (§6.iii) is run over BOTH the candidate's re-resolved index AND the frozen-origin index; the consumer must measurably degrade over the frozen index.
- Frozen answers diverge from candidate on AFTER_L queries (frozen index doesn't include entries 100–999) and cannot answer queries relative to the 2 deferred landmarks (returns empty or stale). Agreement with oracle < candidate's agreement with oracle.
- **For property (iii):** consumer's retrieval quality over frozen index DEGRADES relative to candidate's index (effect direction consistent across seeds).
- Frozen-origin index's `coord_cycle_relative(e)` frozen at `99 - e.cycle`. For entries appended after cycle 99 (entries 100–999): frozen value is `99 - e.cycle` (negative for `e.cycle > 99`), so `exp(-(99 - e.cycle)/50) = exp((e.cycle - 99)/50)` grows exponentially — stale entries get inflated recency weights.

### Arm 2 — `shuffled cadence`
- Append the same 1000 entries but in a **shuffled order** (seeded permutation of the append sequence).
- **B3 fix (exactly one implementation):** each entry's `prev_hash` references the predecessor in the **original (unshuffled) order**, so entries are stored in shuffled order but their `prev_hash` fields point to the original predecessors.
- `verify_chain()` walks storage (shuffled) order, finds that each entry's `prev_hash` does NOT match the actual predecessor in shuffled order → `chain_integrity = False`.
- The landmark designation events are also shuffled (the 2 deferred landmarks designated at shuffled cycles).
- Answer the 200 queries from an index built over the shuffled autobiography.
- Shuffled answers diverge from candidate on landmark-relative queries (BEFORE_L / AFTER_L relations scrambled by shuffle). Agreement with oracle ≈ chance. **Chain integrity check (L2) FAILS** on the shuffled autobiography.

### Arm 3 — `oracle index`
- A perfect-knowledge structure: scan the autobiography AND the designation events once, build a complete index with ground-truth coordinates (using `L.designated_at` for landmark-relative), answer the 200 queries exactly.
- Positive control — proves the metric can leave zero (ceiling).
- Oracle answers = ground truth. Agreement with itself = 1.0. **The candidate must match the oracle exactly (`oracle_agreement = 1.0`) to pass property (i).**

### Arm 4 — `fair naive` (STRENGTHENED — was `naive now−created_at`)
- Reads the FULL event log — including designation events (`event_type = "designation"`, `ref`, `designated_at`) — exactly as the oracle does.
- Has NO maintained index state: no offset counter, no landmark registry with pre-computed coordinates, no incrementally re-resolved structure.
- At query time, for each of the 200 queries `(L_q, r_q)`, scans the autobiography and computes `fair_naive_coord_landmark_relative(e, L_q) = BEFORE_L if e.cycle < L_q.designated_at else (AT_L if == else AFTER_L)` — using `L_q.designated_at` (read from the designation event in the log). Returns the set of `content_id`s where the relation matches.
- **This is recompute-by-scan at query time, with full event-log access, no maintained index state.** The strongest honest timestamps-and-scan implementation.
- **Answers:** fair-naive answers == candidate answers == oracle answers (expected, no longer a kill). `equivalence_agreement` (candidate vs fair-naive) ≈ 1.0 — REPORTED as diagnostic (§7.2), NOT a kill.
- **Cost scaling:** fair-naive per-query latency scales LINEARLY with history length (O(n) — scans the log). Candidate's per-query latency is flat or logarithmic (O(1)/O(log n)).

### Arm 5 — `empty`
- No memory. Return the empty set for every query.
- Agreement with oracle = 0.0 (returns nothing; nothing matches). At chance floor.

### Arm 6 — `wall-clock-injection`
- Build the candidate index normally, but **inject a wall-clock perturbation**: replace `created_at` (autobiography position) with a wall-clock timestamp for a subset of entries (seeded 20%), then re-resolve and answer the 200 queries.
- **N1 acknowledgment (defensive check):** the candidate's coordinate computations use `e.cycle` and `L.designated_at`, NOT `created_at`. The injection of `created_at` has NO effect on the candidate's answers by construction. This arm is a defensive check against a BUILDER implementation bug (accidentally using `created_at` instead of `e.cycle` for coordinates, or accidentally making `designated_at` wall-clock-derived).
- It is NOT a mechanism-level L11 test — the candidate has no path to a private clock by construction.
- If the arm's answers differ from the candidate's unperturbed answers, kill (e) fires — indicating an implementation deviation.
- Expected: arm's answers == candidate's answers (wall-clock ignored). If they differ, the BUILDER has an implementation bug.

---

## 5. The three properties (exact test logic)

### 5.i Property (i) — Correctness (kill (f), SIGNED, primary correctness kill)

**What queries:** the full query battery — 200 landmark-relative queries per seed (§3.4), including the ~20% that involve deferred-designation landmarks (whose ground truth depends on designation events that occurred at different points in the history). The candidate must match the oracle on ALL of them, including the deferred-designation queries.

**What oracle:** the `oracle index` arm (§4 arm 3) — perfect-knowledge structure that scans the autobiography AND designation events once, computes ground-truth coordinates using `L.designated_at`.

**Agreement metric:** per-query agreement is binary, exact-set equality:
```
agreement_vs_oracle(q) = 1 if candidate_answer(q) == oracle_answer(q) else 0
```
where `==` is **exact set equality** on `content_id`s (same elements, regardless of order). No partial credit. No tolerance.

**Aggregate (E1-M1):**
```
oracle_agreement = (1/3) * sum_over_seeds[ (1/200) * sum_over_queries[ agreement_vs_oracle(q) ] ]
```

**Bar:** `oracle_agreement = 1.0` (strict). < 1.0 → kill (f) fires. Candidate must be correct on ALL queries on ALL seeds.

**Kill (f) trigger:** `oracle_agreement (E1-M1) < 1.0` (averaged over 3 seeds, strict `== 1.0` required).

---

### 5.ii Property (ii) — Operational distinctness (kill (d), PROMOTED to discriminator)

#### The state-dependent query battery
Measures per-query latency at 5 history-size points: `{100, 250, 500, 750, 1000}` entries. At each point, the 200 queries are issued to BOTH the candidate and the fair-naive arm; per-query latency (wall-clock seconds) recorded.

**Why state-dependent:** the queries' ground truth depends on the state of the index at query time — specifically, on the designation events that have occurred by that history size.
- At history size 100, only the 8 immediate landmarks are designated (the 2 deferred landmarks are designated at cycles 100–101, AFTER the initial 100).
- At history size 250+, all 10 landmarks are designated.
- **NB-5 (resolved):** at each history size, the query battery includes only landmarks designated by that point in the run. Deferred-designation queries against not-yet-designated landmarks are ill-posed and excluded by construction — a query about a landmark `L` that has not yet been designated is NOT issued. At history size 100, only the 8 immediate landmarks are in the query battery (the 2 deferred enter at 250+).
- **The pre-designation window IS the shift-measurement material.** During the window between `L.cycle` (append) and `L.designated_at` (designation), entries exist whose `coord_landmark_relative` relative to `L` is not yet defined. Upon designation, entries with `e.cycle` in `[L.cycle, L.designated_at)` flip from `AFTER_L` to `BEFORE_L` — this is the re-resolution event.

#### The collapse criterion (4 components, restructured per Rebecca's Q2 ruling)

**1. Candidate side (kill (d) d2 trigger — locked bar, UNCHANGED value):**
```
candidate_latency_growth_10x = latency(history=1000) / latency(history=100)
bar: candidate_latency_growth_10x ≤ 2.0
```
Same locked bar as d1, applied to the state-dependent battery.

**2. Battery-validity requirement (NEW — NOT a candidate kill):**
```
fair_naive_latency_growth_10x = fair_naive_latency(history=1000) / fair_naive_latency(history=100)
bar: fair_naive_latency_growth_10x ≥ 4.0
```
If fair-naive does NOT show ≥ 4.0× growth → battery too easy → **INSTRUMENT failure**: run is **unscoreable**, battery revised, **no kill condition or retry budget touched** (candidate neither dead nor exonerated; battery fixed and run repeated). Routed to ARCHITECT/CRITIC for battery revision, NOT to kill (d). The 4.0× threshold is pre-registered per L19.

**3. Collapse** = the candidate failing bar (1) (growth > 2.0×) on a battery validated by (2) (fair-naive growth ≥ 4.0×). If battery valid AND `candidate_latency_growth_10x > 2.0` → candidate is secretly replaying → kill (d) d2 fires.

**4. Timing methodology (mandated per Rebecca's Q2 ruling item 4; resolves NB-6):** ALL latency measurements in the state-dependent battery (and in d1) use:
- **(i) Median** over repeated executions per point: minimum 100 repetitions per query per history-size point; median per-query latency is the reported figure (not the mean).
- **(ii) Warm-up excluded:** the first 10% of repetitions at each point are discarded (JIT compilation, cache warming, allocator stabilization).
- **(iii) Monotonic clock:** `time.monotonic_ns()` or equivalent — NEVER wall-clock `time.time()`.
- **(iv) Dispersion reported alongside every latency figure:** interquartile range (IQR) or standard deviation per point, reported in the artifact.

If dispersion is large relative to median (e.g., IQR > 50% of median), the CRITIC flags timing as inconclusive and the run is repeated with more repetitions — this is an instrument-quality check, NOT a candidate kill.

#### The slope ratio (RETAINED as REPORTED diagnostic ONLY, never a trigger)
Linear regression of per-query latency on history size for both arms:
```
candidate_latency(h) = candidate_slope * h + candidate_intercept
fair_naive_latency(h) = fair_naive_slope * h + fair_naive_intercept
```
where `h` is history size (100, 250, 500, 750, 1000) and latency is median per-query latency at that history size. Ratio `scaling_collapse_ratio = candidate_slope / fair_naive_slope` is REPORTED for diagnostic transparency — carries NO kill and is NEVER a trigger. A correct candidate has `scaling_collapse_ratio ≈ 0`; a scanning candidate has `≈ 1.0`.

#### Kill (d) — full trigger (d1 OR d2)
- **(d1)** `latency_ratio` (E1-M2) > **2.0**: `latency(10× history) / latency(1× history)` on bounded-output queries (`query_membership` and `query_landmark_relative_bounded(k=10)`), averaged over 3 seeds. > 2.0 = scanning detected. (The locked latency bar, retained.)
- **(d2)** `state_dependent_collapse` (E1-M2b): candidate's 10×-history latency growth on state-dependent battery exceeds 2.0× on a battery validated by fair-naive's ≥ 4.0× growth.
- **Battery-validity (instrument check, NOT a candidate kill):** if fair-naive's 10×-history latency growth on state-dependent battery is < 4.0× → INSTRUMENT failure (run unscoreable, battery revised, no kill, no retry budget touched).
- Either d1 or d2 firing → kill (d) fires (candidate collapsed).

#### E1-M2 (latency_ratio, d1) details
- `latency_ratio` = `latency(10× history) / latency(1× history)`, where latency = mean wall-clock seconds per **bounded-output query** call over the 200 queries, per seed, then averaged over 3 seeds.
- Measured on TWO bounded-output query types (both reported, both must pass the bar):
  - (i) `query_membership(e, L, relation)` — O(1) answer (single boolean).
  - (ii) `query_landmark_relative_bounded(L, relation, k=10)` — bounded by k=10.
- Neither query type materializes an unbounded answer set, so the latency ratio isolates the lookup algorithm's complexity.
- Measured on the candidate arm only.
- Bar: ≤ 2.0. > 2.0 = scanning detected.

---

### 5.iii Property (iii) — Load-bearing coupling (E1-scale integration check, NEW)

#### The downstream consumer (FULLY SPECIFIED — NB-3 promoted to required-before-build)
A MINIMAL downstream consumer — toy recency-weighted retrieval implementing L1's access physics over the index's coordinates. NOT the full L1 system (L1 is M3). It is a test instrument that consumes the candidate's coordinates and produces a measurable output, so that ablation of re-resolution produces a measurable degradation.

**The payload feature vector (exact):** `v(e) ∈ ℝ^32`, generated deterministically per seed:
```
v(e) = rng.standard_normal(32)  where rng = numpy.random.default_rng(seed * 100000 + e.cycle)
```
Part of the opaque payload blob (stored at append time, never changes).

**The content-similarity function (exact):** dot product (NOT cosine):
```
content_similarity(e, q_item) = dot(v(e), q_item)
```
Unnormalized dot product (magnitude varies — entries with larger-magnitude feature vectors are more retrievable).

**The query set (exact):** `N_consumer_queries = 50` query items per seed. Each `q_j ∈ {0..49}` is a 32-d feature vector generated deterministically:
```
q_j = rng_q.standard_normal(32)  where rng_q = numpy.random.default_rng(seed * 1000000 + 1000 + j)
```
Each query item asks: "retrieve the top-k=10 entries by recency-weighted relevance." Query items are NOT entries from the autobiography (fresh synthetic vectors), so retrieval depends on BOTH content similarity AND recency.

**How the consumer uses the index's coordinates (exact):** uses `coord_cycle_relative(e) = now - e.cycle` (the candidate's re-resolved offset coordinate, C1.1) as the recency weight:
```
relevance(e, q_item) = exp(-coord_cycle_relative(e) / τ) * dot(v(e), q_item)
```
where `τ = 50` cycles (pinned constant). Consumer retrieves top-k=10 entries (highest `relevance`) for each query item.
- **The consumer exercises `coord_cycle_relative` ONLY** (NB-4 accepted for E1 scope — full landmark-relative coupling belongs to L15 at M5).

**How degradation is measured under frozen-origin ablation (exact):** consumer run over TWO indices:
1. **Candidate's re-resolved index:** `coord_cycle_relative(e) = now - e.cycle` (re-resolved as `now` advances). Consumer's recall@k = `quality_candidate`.
2. **Frozen-origin index (§4 arm 1, the ablation):** index built once at `now=99`, never re-resolved. `coord_cycle_relative(e)` frozen at `99 - e.cycle` (the `now=99` value). For entries appended after cycle 99 (entries 100–999), frozen `coord_cycle_relative` is `99 - e.cycle` (negative for `e.cycle > 99`), so `exp(-(99 - e.cycle)/50) = exp((e.cycle - 99)/50)` grows exponentially — stale entries get inflated recency weights. Consumer's recall@k = `quality_frozen`.
- **Ground truth:** the oracle's top-k (computed using the oracle's `coord_cycle_relative = now - e.cycle`, the ground-truth recency).
- **Retrieval quality:** recall@k = `|consumer_top_k ∩ oracle_top_k| / k`.
- **Degradation:** `degradation = quality_candidate - quality_frozen` (positive = candidate better than frozen = re-resolution is load-bearing).

#### The consistency requirement
- `degradation > 0` on ALL 3 seeds (effect direction consistent). If `degradation ≤ 0` on any seed → property (iii) fails.
- `mean_degradation ≥ 0.05` across the 3 seeds. The floor (0.05) is pre-registered per L19 (Rebecca's L15 floor of d ≥ 0.5 applies at M5 in full, not at E1's miniature).

#### Report the observed degradation magnitude (Q3 attachment 2)
The spec REQUIRES reporting the observed magnitude, not merely whether it clears the floor. Artifact ships `downstream_degradation_per_seed` (3 floats), `downstream_degradation_mean` (1 float), `downstream_quality_candidate_per_seed` (3 floats), `downstream_quality_frozen_per_seed` (3 floats). The JUDGE/CRITIC inspect the ACTUAL magnitude. **"The floor is a floor, not a finding."** A degradation of 0.06 (barely clearing) and 0.80 (overwhelming) are both "pass" on the floor but materially different findings.

#### Property (iii) failure routing (NOT a separate kill condition — a gate on earning the place)
- **Trigger:** `downstream_degradation` (E1-M6) fails: degradation ≤ 0 on any seed OR mean_degradation < 0.05.
- **What happens:** property (iii) fails — candidate's coordinates not load-bearing. Candidate has NOT earned its place, even if (i) and (ii) pass. NOT a separate kill condition (not in locked 5); it is a GATE on the E1 pass verdict. If property (iii) fails AND no kill condition fires, candidate is NOT dead (D1 does not fire) but E1 is NOT green. Program pauses for Rebecca's decision: (a) consumer/ablation mis-specified (fix and re-run, NOT a candidate death), or (b) coordinates genuinely not load-bearing (D2 retry decision). Specific cause must be identified and CRITIC-confirmed before any re-run escapes D2 budget.

---

## 6. Kill conditions (5 active: b, c, d, e, f — old (a) RETIRED)

A single kill-condition hit terminates E1. Per D1, candidate is dead immediately; idea has 2 retries under D2. Kill conditions (b, c, d, e, f) are evaluated **simultaneously** from the single run's artifacts — no priority ordering; if multiple fire, all are logged.

### Kill (b) — Hash chain breaks
- **Trigger:** `chain_integrity` (E1-M3, final stage) < 1.0 (chain fails to verify on any seed after initial build + shift probe + 10× growth).
- **Metric:** E1-M3 (final stage). Reported at THREE stages: after initial build, after shift probe, after 10× growth (N11 fix).
- **Diagnosis (D2 support):**
  - If `chain_integrity_after_initial_build == False` → **construction break** (C1.3a wrong; chain never valid). BUILDER defect, NOT a candidate death. Fix and re-run (NOT result laundering — run never scored). **Guard:** specific defect identified, fixed, CRITIC-confirmed before re-run escapes D2 budget. "Probably a bug" never does.
  - If `chain_integrity_after_initial_build == True` but `after_shift_probe == False` (or `after_10x_growth == False`) → **re-resolution break** (chain valid after construction, broke after re-resolution). This IS a mechanism death — candidate's own re-resolution breaks L2. Kill (b) fires. A Candidate 2 differing on C1.3a (Merkle-tree) would engage this cause.

### Kill (c) — No measurable shift
- **Trigger:** `coordinate_shift` (E1-M4) < 1.0 (`coord_cycle_relative` does NOT increase by exactly 1 per append for every probed entry, on any seed, over the 8 appends in shift probe).
- **Metric:** E1-M4. `shift_per_append` array of 8 booleans per seed (N12 fix).
- **Diagnosis (D2 support):**
  - If all 8 are `False` → **wiring defect** (re-resolution not connected to append path; offset-counter never increments). BUILDER defect, NOT a candidate death. Fix and re-run. **Guard:** specific defect identified, fixed, CRITIC-confirmed.
  - If some `True` and some `False` → **partial mechanism failure** (re-resolution shifts sometimes but not always). This IS a mechanism death — offset-counter design (C1.1) fundamentally broken. Kill (c) fires. A Candidate 2 differing on C1.1 (non-offset re-resolver) would engage this cause.

### Kill (d) — Scanning detected / scaling collapse
- **Trigger:** EITHER (d1) `latency_ratio` (E1-M2) > 2.0 on bounded-output queries OR (d2) `state_dependent_collapse` (E1-M2b): candidate's 10×-history latency growth > 2.0× on a battery validated by fair-naive's ≥ 4.0× growth. Plus battery-validity instrument check (fair-naive < 4.0× → INSTRUMENT failure, not a kill).
- See §5.ii for full criterion, timing methodology, and instrument-failure routing.

### Kill (e) — Coordinates shift with wall-clock perturbation
- **Trigger:** `wall_clock_shift_detected` (E1-M5) = True on any seed (wall-clock-injection arm's answer-set differs from candidate's unperturbed answer-set on ANY query).
- **Metric:** E1-M5 (qualitative → boolean). Strict equality check (no tolerance). Reported as `wall_clock_shift_detected: bool` per seed.
- **Diagnosis (D2 support):** state whether wall-clock leak is in `created_at` (C1.3b: cycle counter wall-clock-derived), in `designated_at` (C1.4: designation events wall-clock-stamped), or in re-resolution. N1: candidate uses `e.cycle` and `L.designated_at` (both autobiography-position-derived). If kill (e) fires, it indicates a BUILDER implementation bug. **Construction-bug guard:** specific defect identified, fixed, CRITIC-confirmed before re-run escapes D2 budget.

### Kill (f) — Candidate is wrong (does not match oracle)
- **Trigger:** `oracle_agreement` (E1-M1) < 1.0 (averaged over 3 seeds, strict `== 1.0` required).
- **Status:** **SIGNED** by Rebecca (ruling §4 item 3). Primary correctness kill condition (property (i)).
- **Diagnosis (D2 support):** state which re-resolution step is wrong (designation tracking buggy, offset-counter drifts, landmark registry corrupt, wrong reference for `coord_landmark_relative`). A Candidate 2 differing on C1.1/C1.2/C1.4 would engage the diagnosed cause.

### Old kill (a) — RETIRED
- **Status:** RETIRED per Rebecca's ruling. Unsatisfiable by construction (fair-naive ≡ oracle). Metric `equivalence_agreement` retained as REPORTED diagnostic (§7.2), expected ≈ 1.0. Carries NO kill and NO distinctness claim. If `equivalence_agreement` is NOT ≈ 1.0 (e.g., < 0.95), it indicates the fair naive is handicapped (BUILDER bug).

### Construction-bug guard (applies to kills b, c, e)
If a kill fires, check if it's a construction bug (intermediate chain_integrity, per-append shift measurements). Bug attribution requires: **specific defect identified, fixed, CRITIC-confirmed** before any re-run escapes the D2 budget. "Probably a bug" never does. A re-run after a confirmed construction/wiring bug fix is NOT result laundering (the run never scored — only scoring runs through Rebecca's courier channel count).

---

## 7. Reported diagnostics (NOT barred — carry NO kill)

### 7.1 `equivalence_agreement` (RETIRED metric)
Agreement between candidate's answer-set and fair-naive arm's answer-set, over 200 queries, averaged over 3 seeds. EXPECTED ≈ 1.0 (fair-naive ≡ oracle on answers per Rebecca's theorem). REPORTED to confirm the theorem holds and fair naive is not handicapped. Carries NO kill. If NOT ≈ 1.0 (e.g., < 0.95), indicates fair naive is handicapped (BUILDER bug).

### 7.2 `raw_answer_size_1x`, `raw_answer_size_10x`, `raw_answer_size_ratio` (B2 fix)
Mean number of content_ids returned by UNBOUNDED `query_landmark_relative` at 1× and 10× history, and their ratio. Expected ~10× (answer-set grows with history). REPORTED, NOT BARRED. Latency bar is NOT measured on these unbounded queries.

### 7.3 `candidate_scaling_curve` and `fair_naive_scaling_curve` (property ii)
Per-query latency at each of the 5 history-size points (100, 250, 500, 750, 1000), for both arms, plus fitted slopes. REPORTED so JUDGE/CRITIC can inspect scaling curves directly.

### 7.4 `scaling_collapse_ratio` (slope ratio — RETAINED as REPORTED diagnostic ONLY, never a trigger)
`candidate_slope / fair_naive_slope`. NO LONGER a collapse trigger — fragile at toy scale. The collapse trigger is the candidate's locked latency bar (≤ 2.0× growth) on a battery validated by fair-naive's ≥ 4.0× growth. Reported for diagnostic transparency only — carries NO kill.

---

## 8. Output schema (5 files)

### 8.1 `e1_run_results.json` — full results table

```json
{
  "run_id": "e1-<ISO8601 timestamp>",
  "schema_version": "3.0",
  "config": {
    "n_cycles": 10,
    "n_entries_initial": 100,
    "n_entries_final": 1000,
    "n_landmarks": 10,
    "n_landmarks_immediate": 8,
    "n_landmarks_deferred": 2,
    "n_queries": 200,
    "n_state_dependent_query_points": 5,
    "state_dependent_history_sizes": [100, 250, 500, 750, 1000],
    "n_consumer_queries": 50,
    "consumer_feature_dim": 32,
    "consumer_tau": 50,
    "consumer_k": 10,
    "timing_repetitions": 100,
    "timing_methodology": "median, warm-up excluded, monotonic clock, IQR reported",
    "seeds": [42, 43, 44],
    "control_arms": ["frozen_origin", "shuffled_cadence", "oracle_index", "fair_naive", "empty", "wall_clock_injection"],
    "candidate": "candidate_1_1"
  },
  "results": {
    "42": {
      "candidate": {
        "oracle_agreement": <f>,
        "equivalence_agreement_vs_fair_naive": <f>,
        "latency_1x_seconds_membership": <f>,
        "latency_10x_seconds_membership": <f>,
        "latency_ratio_membership": <f>,
        "latency_1x_seconds_bounded_k": <f>,
        "latency_10x_seconds_bounded_k": <f>,
        "latency_ratio_bounded_k": <f>,
        "raw_answer_size_1x": <f>,
        "raw_answer_size_10x": <f>,
        "raw_answer_size_ratio": <f>,
        "candidate_scaling_curve": [<5 floats: median per-query latency at history sizes 100, 250, 500, 750, 1000>],
        "candidate_latency_iqr_per_point": [<5 floats: IQR of per-query latency at each history-size point>],
        "candidate_slope": <f>,
        "candidate_intercept": <f>,
        "candidate_latency_growth_10x": <f>,
        "chain_integrity_after_initial_build": <bool>,
        "chain_integrity_after_shift_probe": <bool>,
        "chain_integrity_after_10x_growth": <bool>,
        "chain_integrity_final": <bool>,
        "shift_per_append": [<8 bools>],
        "coordinate_shift": <bool>,
        "wall_clock_shift_detected": <bool>,
        "downstream_quality_candidate": <f>,
        "downstream_quality_frozen": <f>,
        "downstream_degradation": <f>,
        "downstream_degradation_magnitude_reported": <f>
      },
      "frozen_origin":  {"oracle_agreement": <f>, "downstream_quality_frozen": <f>},
      "shuffled_cadence": {"oracle_agreement": <f>, "chain_integrity": <bool>},
      "oracle_index":   {"oracle_agreement": 1.0},
      "fair_naive": {
        "oracle_agreement": <f>,
        "equivalence_agreement_vs_candidate": <f>,
        "fair_naive_scaling_curve": [<5 floats>],
        "fair_naive_latency_iqr_per_point": [<5 floats>],
        "fair_naive_slope": <f>,
        "fair_naive_intercept": <f>,
        "fair_naive_latency_growth_10x": <f>
      },
      "empty":          {"oracle_agreement": 0.0},
      "wall_clock_injection": {"shift_vs_candidate": <bool>}
    },
    "43": { "...": "..." },
    "44": { "...": "..." }
  },
  "mean_over_seeds": {
    "candidate": {
      "oracle_agreement": <f>,
      "equivalence_agreement_vs_fair_naive": <f>,
      "latency_ratio_membership": <f>,
      "latency_ratio_bounded_k": <f>,
      "raw_answer_size_1x": <f>,
      "raw_answer_size_10x": <f>,
      "raw_answer_size_ratio": <f>,
      "candidate_slope": <f>,
      "fair_naive_slope": <f>,
      "scaling_collapse_ratio": <f>,
      "candidate_latency_growth_10x": <f>,
      "fair_naive_latency_growth_10x": <f>,
      "battery_valid": <bool>,
      "chain_integrity_final": <f>,
      "coordinate_shift": <f>,
      "wall_clock_shift_detected": <f>,
      "downstream_quality_candidate": <f>,
      "downstream_quality_frozen": <f>,
      "downstream_degradation": <f>,
      "downstream_degradation_floor": 0.05,
      "downstream_degradation_consistent": <bool>
    },
    "frozen_origin":  {"oracle_agreement": <f>, "downstream_quality_frozen": <f>},
    "shuffled_cadence": {"oracle_agreement": <f>, "chain_integrity": <f>},
    "oracle_index":   {"oracle_agreement": 1.0},
    "fair_naive": {"oracle_agreement": <f>, "equivalence_agreement_vs_candidate": <f>, "fair_naive_slope": <f>, "fair_naive_latency_growth_10x": <f>},
    "empty":          {"oracle_agreement": 0.0},
    "wall_clock_injection": {"shift_vs_candidate": <f>}
  },
  "property_i_correctness": {
    "oracle_agreement": <f>,
    "bar": 1.0,
    "passes": <bool>,
    "per_query_agreement_vs_oracle": {"42": [<200 bools>], "43": [<200 bools>], "44": [<200 bools>]}
  },
  "property_ii_operational_distinctness": {
    "latency_ratio_membership": <f>,
    "latency_ratio_bounded_k": <f>,
    "latency_bar": 2.0,
    "latency_passes": <bool>,
    "candidate_latency_growth_10x": <f>,
    "fair_naive_latency_growth_10x": <f>,
    "battery_valid": <bool>,
    "battery_validity_bar": 4.0,
    "state_dependent_collapse_bar": 2.0,
    "state_dependent_passes": <bool>,
    "instrument_failure": <bool>,
    "candidate_slope": <f>,
    "fair_naive_slope": <f>,
    "scaling_collapse_ratio": <f>,
    "scaling_collapse_note": "REPORTED diagnostic ONLY (slope ratio); never a trigger per Rebecca Q2 ruling",
    "candidate_scaling_curve_mean": [<5 floats>],
    "fair_naive_scaling_curve_mean": [<5 floats>],
    "candidate_latency_iqr_per_point_mean": [<5 floats>],
    "fair_naive_latency_iqr_per_point_mean": [<5 floats>],
    "timing_methodology": "median over >=100 reps, warm-up excluded, monotonic clock, IQR reported",
    "equivalence_agreement_vs_fair_naive": <f>,
    "equivalence_note": "REPORTED diagnostic; expected ~1.0 (fair-naive == oracle on answers per Rebecca's theorem); carries NO kill and NO distinctness claim"
  },
  "property_iii_load_bearing_coupling": {
    "downstream_degradation_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "downstream_degradation_mean": <f>,
    "downstream_degradation_floor": 0.05,
    "downstream_degradation_magnitude_note": "the floor is a floor, not a finding — observed magnitude reported (Q3 attachment 2)",
    "downstream_degradation_consistent": <bool>,
    "passes": <bool>,
    "downstream_quality_candidate_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "downstream_quality_frozen_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "consumer_spec": "dot product on 32-d feature vectors, 50 queries per seed, tau=50, k=10, coord_cycle_relative only (NB-4 accepted for E1)"
  },
  "kill_conditions": {
    "(b)_chain_breaks":           {"fires": <bool>, "metric": "chain_integrity_final", "value": <f>, "bar": 1.0, "trigger": "value < 1.0", "construction_break": <bool>, "re_resolution_break": <bool>},
    "(c)_no_shift":               {"fires": <bool>, "metric": "coordinate_shift", "value": <f>, "bar": 1.0, "trigger": "value < 1.0", "wiring_defect": <bool>, "partial_failure": <bool>},
    "(d)_scanning_or_collapse":   {"fires": <bool>, "metric": "latency_ratio AND state_dependent_collapse", "value_latency_membership": <f>, "value_latency_bounded_k": <f>, "value_candidate_latency_growth_10x": <f>, "value_fair_naive_latency_growth_10x": <f>, "value_battery_valid": <bool>, "bar_latency": 2.0, "bar_state_dependent_collapse": 2.0, "bar_battery_validity": 4.0, "trigger": "either latency > 2.0 [d1] OR (battery_valid AND candidate_growth_10x > 2.0) [d2]; if battery invalid -> instrument failure (not a kill)", "instrument_failure": <bool>},
    "(e)_wall_clock_shift":       {"fires": <bool>, "metric": "wall_clock_shift_detected", "value": <f>, "bar": 0.0, "trigger": "value > 0.0"},
    "(f)_incorrect":              {"fires": <bool>, "metric": "oracle_agreement", "value": <f>, "bar": 1.0, "trigger": "value < 1.0", "signed": true},
    "retired": {
      "(a)_collapse_to_naive": {"status": "RETIRED per Rebecca E1 gate ruling", "rationale": "unsatisfiable by construction (fair-naive == oracle on answers; the pair {naive_agreement <= 0.90, oracle_agreement = 1.0} is jointly unsatisfiable)", "metric_reported_as_diagnostic": "equivalence_agreement_vs_fair_naive"}
    },
    "any_fires": <bool>,
    "candidate_dead": <bool>
  },
  "reproducibility": {
    "method": "re-run all 3 seeds a second time within the same process; verify bit-identical results",
    "max_abs_diff_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "bit_identical": <bool>
  }
}
```

### 8.2 `e1_invariants.json` — invariant/kill-condition verdict

```json
{
  "e1_verdict": "PASS | FAIL | NOT_GREEN",
  "kill_conditions": {
    "(b)": {"fires": <bool>, "detail": "...", "construction_break": <bool>, "re_resolution_break": <bool>},
    "(c)": {"fires": <bool>, "detail": "...", "wiring_defect": <bool>, "partial_failure": <bool>},
    "(d)": {"fires": <bool>, "detail": "...", "latency_ratio_membership": <f>, "latency_ratio_bounded_k": <f>, "candidate_latency_growth_10x": <f>, "fair_naive_latency_growth_10x": <f>, "battery_valid": <bool>, "instrument_failure": <bool>, "scaling_collapse_ratio_diagnostic": <f>},
    "(e)": {"fires": <bool>, "detail": "..."},
    "(f)": {"fires": <bool>, "detail": "...", "signed": true},
    "(a)_retired": {"status": "RETIRED", "rationale": "unsatisfiable by construction per Rebecca's theorem"}
  },
  "property_i_correctness": {
    "oracle_agreement": <f>,
    "bar": 1.0,
    "passes": <bool>
  },
  "property_ii_operational_distinctness": {
    "latency_ratio_membership": <f>,
    "latency_ratio_bounded_k": <f>,
    "latency_bar": "both <= 2.0",
    "latency_passes": <bool>,
    "candidate_latency_growth_10x": <f>,
    "fair_naive_latency_growth_10x": <f>,
    "battery_valid": <bool>,
    "battery_validity_bar": "fair_naive_latency_growth_10x >= 4.0",
    "state_dependent_collapse_bar": "candidate_latency_growth_10x <= 2.0 on valid battery",
    "state_dependent_passes": <bool>,
    "instrument_failure": <bool>,
    "candidate_slope": <f>,
    "fair_naive_slope": <f>,
    "scaling_collapse_ratio_diagnostic": <f>,
    "scaling_note": "slope ratio is a REPORTED diagnostic ONLY; never a trigger (Rebecca Q2)",
    "timing_methodology": "median >=100 reps, warm-up excluded, monotonic clock, IQR reported (NB-6 resolved)",
    "equivalence_agreement_vs_fair_naive": <f>,
    "equivalence_note": "REPORTED diagnostic; expected ~1.0; carries NO kill"
  },
  "property_iii_load_bearing_coupling": {
    "downstream_degradation_per_seed": {"42": <f>, "43": <f>, "44": <f>},
    "downstream_degradation_mean": <f>,
    "floor": 0.05,
    "magnitude_note": "the floor is a floor, not a finding — observed magnitude reported (Q3 attachment 2)",
    "consistent": <bool>,
    "passes": <bool>,
    "consumer_spec": "dot product on 32-d vectors, 50 queries/seed, tau=50, k=10, coord_cycle_relative only (NB-4 accepted for E1; full landmark-relative at M5)",
    "note": "miniature of L15 (M5 applies in full); a candidate whose coordinates are consumed by nothing is a cache with a philosophy"
  },
  "l2_chain_axis": {
    "chain_integrity_final": <f>,
    "chain_integrity_after_initial_build": <f>,
    "chain_integrity_after_shift_probe": <f>,
    "chain_integrity_after_10x_growth": <f>,
    "bar": "chain_integrity_final == 1.0",
    "passes": <bool>
  },
  "l4_shift_axis": {
    "coordinate_shift": <f>,
    "shift_per_append": {"42": [<8 bools>], "43": [<8 bools>], "44": [<8 bools>]},
    "bar": "coordinate_shift == 1.0",
    "passes": <bool>
  },
  "l11_wall_clock_axis": {
    "wall_clock_shift_detected": <f>,
    "bar": "wall_clock_shift_detected == 0.0",
    "passes": <bool>,
    "defensive_check_note": "N1: tests for implementation bugs, not mechanism-level L11 violations"
  },
  "reproducibility": {
    "bit_identical": <bool>,
    "max_abs_diff_per_seed": {"42": <f>, "43": <f>, "44": <f>}
  },
  "i3_contamination": {
    "method": {
      "name": "empirical_null_self_consistency",
      "provenance": "Rebecca-locked: empirical-null method (Ruling O-14). N4 fix: null generated by running >=100 seeded replicates of EACH contamination arm (self-consistency null), NOT the naive arm.",
      "rules": "For each contamination arm, run >=100 seeded replicates of THAT arm with different seeds; compute the distribution of oracle_agreement; the I3 band = central 99% interval. The 3-seed mean must fall in the band. Re-run-on-failure is FORBIDDEN.",
      "null_replicate_count": <int, >=100>,
      "null_source_per_arm": {
        "shuffled_cadence": "self (>=100 replicates of shuffled_cadence)",
        "empty": "self (>=100 replicates of empty; degenerate distribution [0.0, 0.0] — trivially in-band)",
        "wall_clock_injection": "self (>=100 replicates of wall_clock_injection)"
      }
    },
    "per_arm_per_metric": {
      "shuffled_cadence": {"oracle_agreement": {"in_band": <bool>, "null_band_lo": <f>, "null_band_hi": <f>, "low_power": <bool>}},
      "empty": {"oracle_agreement": {"in_band": <bool>, "null_band_lo": 0.0, "null_band_hi": 0.0, "low_power": false, "note": "degenerate distribution; trivially in-band"}},
      "wall_clock_injection": {"shift_vs_candidate": {"in_band": <bool>, "null_band_lo": <f>, "null_band_hi": <f>, "low_power": <bool>}}
    }
  }
}
```

> **N4 fix (I3 null distribution source):** the null for each contamination arm is generated by running ≥100 seeded replicates of THAT SAME arm (self-consistency null), explicitly stated per arm. The `empty` arm's null is degenerate `[0.0, 0.0]` (returns nothing, nothing matches) — trivially in-band. The naive arm is NOT used as the null (in E1, fair-naive is a correct recomputation, not a chance floor — using it as the null would make every contamination arm fail I3 spuriously). Low-power flag when band width exceeds ±0.15 (correlation-scale) or ±0.10 (probability-scale). Re-run-on-failure is FORBIDDEN.

### 8.3 `e1_manifest.json` — run manifest (courier round-trip log)

```json
{
  "command": "python e1_experiment.py --seeds 42,43,44 --output-dir ./e1_output",
  "commit_hash": "<git rev-parse HEAD, 40 hex chars>",
  "purpose": "E1 moving-origin experiment (three-property test per Rebecca's E1 gate ruling + Q2/Q3 incorporations): (i) correctness (oracle_agreement == 1.0, kill f), (ii) operational distinctness (latency_ratio <= 2.0 [d1] AND candidate_latency_growth_10x <= 2.0 on a battery where fair_naive_latency_growth_10x >= 4.0 [d2]; slope ratio is diagnostic only; kill d), (iii) load-bearing coupling (downstream_degradation > 0 on all seeds AND mean >= 0.05; observed magnitude reported). Plus structural: chain integrity (kill b), coordinate shift (kill c), wall-clock independence (kill e). Old kill (a) RETIRED. 5 active kill conditions (b-f). Timing methodology: median >=100 reps, warm-up excluded, monotonic clock, IQR reported (NB-6 resolved).",
  "bars": "oracle_agreement == 1.0 (kill f); latency_ratio <= 2.0 [d1] AND candidate_latency_growth_10x <= 2.0 on battery where fair_naive_latency_growth_10x >= 4.0 [d2] (kill d; slope ratio diagnostic only); chain_integrity == 1.0 (kill b); coordinate_shift == 1.0 (kill c); wall_clock_shift_detected == 0.0 (kill e); downstream_degradation > 0 all seeds AND mean >= 0.05 (property iii; magnitude reported). Old equivalence_agreement <= 0.90 RETIRED.",
  "seeds": [42, 43, 44],
  "wall_clock_seconds": <float>,
  "deps": {"python": "3.11.x", "numpy": "1.26.4", "scipy": "1.13.1"},
  "python_version_runtime": "<filled by Rebecca's python --version output>",
  "output_files": ["e1_run_results.json", "e1_invariants.json", "e1_manifest.json", "e1_run.log", "e1_profile.json"],
  "deviations_logged": []
}
```

### 8.4 `e1_run.log`
Raw stdout/stderr capture, UTF-8 encoded (M1 hygiene fix carried forward).

### 8.5 `e1_profile.json` — L20 drift baseline for E1

```json
{
  "profile_version": "e1-locked-3.0",
  "profile_vector": [<6 floats: candidate's 6 metrics mean-over-seeds, order: oracle_agreement, latency_ratio_membership, candidate_latency_growth_10x, chain_integrity_final, coordinate_shift, downstream_degradation>],
  "metric_order": ["oracle_agreement", "latency_ratio_membership", "candidate_latency_growth_10x", "chain_integrity_final", "coordinate_shift", "downstream_degradation"],
  "drift_criterion": "pearson_corr(profile_vector, new_profile_vector) < 0.70 => drifted (locked bar); self-test threshold < 0.50",
  "l20_self_test": {
    "no_drift_corr": 1.0,
    "no_drift_passes": true,
    "perturbation_1": "metric_block_reversal",
    "perturbation_1_definition": "N5 fix: reverse the 6-element profile vector [m0,m1,m2,m3,m4,m5] -> [m5,m4,m3,m2,m1,m0]. (Before: [oracle_agreement, latency_ratio_membership, candidate_latency_growth_10x, chain_integrity_final, coordinate_shift, downstream_degradation]. After: [downstream_degradation, coordinate_shift, chain_integrity_final, candidate_latency_growth_10x, latency_ratio_membership, oracle_agreement].)",
    "perturbation_1_corr": "<float, must be < 0.50>",
    "perturbation_2": "candidate_empty_swap",
    "perturbation_2_definition": "N5 fix: swap the candidate's profile vector [m0..m5] with the empty arm's profile vector [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] (empty arm has oracle_agreement=0.0 and all other metrics at chance/zero). Resulting vector: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]. (Before: candidate's 6 metrics. After: empty arm's 6 metrics — all zeros.)",
    "perturbation_2_corr": "<float, must be < 0.50>",
    "both_perturbations_flag_drift": true
  }
}
```

**Profile vector notes:**
- 6 elements — all candidate metrics, updated for the three-property test and Q2 restructure.
- `equivalence_agreement` is NOT in the profile vector (it is a diagnostic, not a candidate metric).
- `wall_clock_shift_detected` is NOT in the profile vector (defensive check, expected False; constant-False would zero-variance the vector).
- `frozen_oracle_agreement` is NOT in the profile vector (control arm's metric).
- `scaling_collapse_ratio` (slope ratio) is NOT in the profile vector (reported diagnostic only, never a trigger).
- **NEW-1 fix (zero-variance edge case):** `pearson_corr(x, const)` is defined as `0.0` when the second vector has zero variance, which trivially satisfies `< 0.50` and flags drift. The BUILDER implements this edge-case handling.

---

## 9. The verdict assembly (what the JUDGE does — implement the logic in-script)

**E1 passes (green) iff:** properties (i), (ii), (iii) all pass AND no kill condition fires (b, c, d, e, f all false) AND I3 contamination trustworthy AND L20 self-test passes AND reproducibility passes.

**E1 fails (red) iff:** any kill condition (b, c, d, e, f) fires. Candidate is dead (D1). Routes to D2 retry decision.

**E1 not-green (candidate alive but place not earned) iff:** property (iii) fails AND no kill condition fires. Candidate not dead, but moving origin has not earned its place. Program pauses for Rebecca's decision.

---

## 10. Verification (M1-equivalent hygiene, carried forward)

- **Reproducibility check (N6 fix):** re-run all 3 seeds a second time within the same process and verify bit-identical results. Ship a per-seed `max_abs_diff` map.
- **L20 drift self-test:** no-drift corr = 1.0; both pinned perturbations (metric_block_reversal, candidate_empty_swap) corr < 0.50.
- **deviations_logged self-detection:** the script self-detects and logs deviations (e.g., python version mismatch) in the manifest.

---

## 11. Implementation notes

- The script is self-contained: generates the synthetic autobiography (with deferred landmark designation), builds the candidate mechanism (§1) and the 6 control arms (§3), runs the 200 queries × 6 arms × 3 seeds, evaluates the three properties (i, ii, iii) + structural checks, evaluates the 5 active kill conditions (b-f), runs the state-dependent scaling battery (5 history-size points × candidate + fair-naive), runs the downstream consumer over candidate and frozen-origin indices, runs the I3 empirical-null (≥100 self-consistency replicates) for contamination arms, runs the L20 drift self-test, runs the reproducibility check, and writes the 5 output files. No external data files; all data synthesized in-process from the seed.
- SHA-256 via stdlib `hashlib`.
- Timing via `time.monotonic_ns()` (NEVER `time.time()`).
- Median over ≥100 repetitions per query per history-size point; warm-up excluded (first 10% discarded); IQR reported.
- For the wall-clock-injection arm: replace `created_at` with wall-clock timestamps for a seeded 20% subset of entries, then re-resolve and answer. The candidate's coordinates use `e.cycle` and `L.designated_at` (NOT `created_at`), so this should have NO effect on answers — the arm is a defensive check for BUILDER bugs.

---

*End of task spec. Source: `/home/user/workspace/e1_spec.md` (REVISED DRAFT v3 + Rebecca Q2/Q3 incorporations). All numeric values LOCKED from M0 / Rebecca's ruling — none invented, lowered, raised, or renamed.*
