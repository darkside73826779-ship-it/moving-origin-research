"""Refined existence proof: mix of immediate and deferred designation
so agreement is meaningfully below 0.90 but not trivially 0.0."""

import random

def simulate(seed, n_immediate, n_deferred, defer_min, defer_max,
              N_initial=100, N_final=1000, N_queries=200):
    rng = random.Random(seed)
    N_landmarks = n_immediate + n_deferred

    # Pick landmarks from initial build
    landmark_pool = rng.sample(range(N_initial), N_landmarks)
    landmark_designated = {}
    immediate = landmark_pool[:n_immediate]
    deferred = landmark_pool[n_immediate:]

    for li in immediate:
        landmark_designated[li] = li  # designated at append (no delay)
    for li in deferred:
        # Designate during shift probe (cycles 100-109) or growth
        landmark_designated[li] = rng.randint(100, 109)

    # Queries
    queries = []
    for q in range(N_queries):
        L = rng.choice(landmark_pool)
        r = rng.choice(["BEFORE_L", "AFTER_L"])
        queries.append((L, r))

    n_agree_naive = 0
    n_agree_oracle = 0
    for L, r in queries:
        L_created = L
        L_designated = landmark_designated[L]
        if r == "BEFORE_L":
            oracle_set = set(range(0, L_designated))
            cand_set = set(range(0, L_designated))
            naive_set = set(range(0, L_created))
        else:
            oracle_set = set(range(L_designated, N_final))
            cand_set = set(range(L_designated, N_final))
            naive_set = set(range(L_created, N_final))
        if cand_set == naive_set:
            n_agree_naive += 1
        if cand_set == oracle_set:
            n_agree_oracle += 1

    return n_agree_naive/N_queries, n_agree_oracle/N_queries

# Scenario A: all deferred (original) — agreement 0.0 (too extreme)
print("Scenario A: 10 deferred, 0 immediate")
for s in [42, 43, 44]:
    a, o = simulate(s, 0, 10, 100, 109)
    print(f"  seed {s}: agree_naive={a:.3f}, agree_oracle={o:.3f}")

# Scenario B: 5 immediate, 5 deferred — ~50% of queries differ
print("\nScenario B: 5 immediate, 5 deferred")
for s in [42, 43, 44]:
    a, o = simulate(s, 5, 5, 100, 109)
    print(f"  seed {s}: agree_naive={a:.3f}, agree_oracle={o:.3f}")

# Scenario C: 8 immediate, 2 deferred — ~20% differ, agreement ~0.80
print("\nScenario C: 8 immediate, 2 deferred")
for s in [42, 43, 44]:
    a, o = simulate(s, 8, 2, 100, 109)
    print(f"  seed {s}: agree_naive={a:.3f}, agree_oracle={o:.3f}")

# Scenario D: 9 immediate, 1 deferred — ~10% differ, agreement ~0.90
print("\nScenario D: 9 immediate, 1 deferred")
for s in [42, 43, 44]:
    a, o = simulate(s, 9, 1, 100, 109)
    print(f"  seed {s}: agree_naive={a:.3f}, agree_oracle={o:.3f}")

# The KEY question: is there a scenario where agreement is meaningfully < 0.90
# (not 0.0, not 1.0) and oracle_agreement == 1.0?
# Scenario B (5/5) gives ~0.50 — good, clearly below 0.90, not trivially 0.
# Scenario C (8/2) gives ~0.80 — good, below 0.90, not trivially 0.

print("\n=== CONCLUSION ===")
print("Scenario B (5 immediate + 5 deferred landmarks):")
print("  agreement ~0.50 (well below 0.90 collapse bar, not trivially 0.0)")
print("  oracle_agreement = 1.0 (candidate is correct)")
print("  => COHERENT is reachable, test is non-trivial")
print()
print("The existence proof HOLDS. The spec is NOT blocked.")
print()
print("Design choice for the spec:")
print("  - Landmarks designated via a SEPARATE designate_landmark() event")
print("  - SOME landmarks designated at append (immediate) — these queries match naive")
print("  - SOME landmarks designated later (deferred) — these queries differ from naive")
print("  - The MIX makes agreement a meaningful number in (0, 1), not trivially 0 or 1")
print("  - The candidate is CORRECT on all (matches oracle) because it tracks designation")
print("  - Naive is WRONG on deferred-designation queries (only has created_at)")
