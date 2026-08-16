"""
CRITIC's INDEPENDENT re-derivation of the Option E fix (additive + bucketed),
implemented from scratch directly from the spec text (e1_spec.md §6.iii + §2.2),
NOT by importing the ARCHITECT's verify_option_e_fix.py.

Purpose: confirm the claimed numbers (CU=0.000, RD=0.255, ALL=0.102, per-seed
0.120/0.094/0.092) are genuine and not an artifact of the ARCHITECT's script.
"""
import numpy as np

# Pinned constants straight from the spec §2.2 / §6.iii
D = 32
TAU = 50
K = 10
N = 1000
NOW = 999
SEEDS = [42, 43, 44]
A = 10.0
SIGMA_F = 0.10
SIGMA_Q = 0.10
LAMBDA = 16.0
K_RD = 30
N_CU = 30
N_RD = 20


def build(seed):
    """Build autobiography + queries exactly per §6.iii spec text."""
    # 50 buckets: RD 0..19 (size 30), CU 20..49 (size 10). 100 fillers.
    sizes = [K_RD] * N_RD + [K] * N_CU
    n_labeled = sum(sizes)
    # seeded permutation, round-robined across buckets
    rng_perm = np.random.default_rng(seed * 7_000_000 + 1)
    spread = rng_perm.permutation(N)[:n_labeled]
    bucket_of = np.full(N, -1, dtype=np.int64)
    member = [0] * 50
    slot = 0
    while slot < n_labeled:
        for b in range(50):
            if member[b] < sizes[b]:
                bucket_of[int(spread[slot])] = b
                member[b] += 1
                slot += 1
                if slot >= n_labeled:
                    break
    # seeded random unit directions per bucket
    dirs = np.zeros((50, D))
    for b in range(50):
        r = np.random.default_rng(seed * 9_000_000 + b)
        u = r.standard_normal(D)
        dirs[b] = u / np.linalg.norm(u)
    # feature vectors per §6.iii: v(e) = A*u_b + sigma_f*noise ; fillers noise-only
    cycles = np.arange(N)
    feats = np.zeros((N, D))
    for e in range(N):
        r = np.random.default_rng(seed * 100_000 + e)  # spec: e.cycle == e (cycles=arange)
        noise = r.standard_normal(D) * SIGMA_F
        b = bucket_of[e]
        if b >= 0:
            feats[e] = A * dirs[b] + noise
        else:
            feats[e] = noise
    # queries: 20 RD (target bucket 0..19), 30 CU (target bucket 20..49)
    qs = np.zeros((50, D))
    for j in range(N_RD):
        r = np.random.default_rng(seed * 10_000_000 + 500 + j)
        qs[j] = A * dirs[j] + r.standard_normal(D) * SIGMA_Q
    for j in range(N_CU):
        r = np.random.default_rng(seed * 1_000_000 + 1000 + (N_RD + j))
        qs[N_RD + j] = A * dirs[N_RD + j] + r.standard_normal(D) * SIGMA_Q
    return cycles, feats, bucket_of, dirs, qs


def topk(rel, k=K):
    # stable argsort descending
    return set(np.argsort(-rel, kind='stable')[:k])


def run(seed):
    cycles, feats, bucket_of, dirs, qs = build(seed)
    oracle_cr = (NOW - cycles).astype(float)   # re-resolved
    frozen_cr = np.zeros(N)                      # Option E
    rd_deg, cu_deg = [], []
    for j in range(50):
        q = qs[j]
        content = feats @ q
        rel_o = content + LAMBDA * np.exp(-oracle_cr / TAU)
        rel_f = content + LAMBDA * np.exp(-frozen_cr / TAU)   # = content + LAMBDA (constant)
        ot = topk(rel_o); ft = topk(rel_f)
        recall = len(ot & ft) / K
        deg = 1.0 - recall
        (rd_deg if j < N_RD else cu_deg).append(deg)
    return (np.mean(rd_deg), np.mean(cu_deg), np.mean(rd_deg + cu_deg), rd_deg, cu_deg)


print("CRITIC INDEPENDENT re-derivation (additive + bucketed, from spec text)")
print(f"config: A={A} sigma_f={SIGMA_F} sigma_q={SIGMA_Q} lambda={LAMBDA} "
      f"K_rd={K_RD} tau={TAU} k={K} d={D} N={N} now={NOW}")
agg = []
for s in SEEDS:
    rd, cu, all_, rdp, cup = run(s)
    agg.append(all_)
    print(f"  seed {s}: RD={rd:.4f} CU={cu:.4f} ALL={all_:.4f} "
          f"(RD per-query min={min(rdp):.2f} max={max(rdp):.2f}; "
          f"CU per-query min={min(cup):.2f} max={max(cup):.2f})")
print(f"  MEAN: RD={np.mean([run(s)[0] for s in SEEDS]):.4f} "
      f"CU={np.mean([run(s)[1] for s in SEEDS]):.4f} "
      f"ALL={np.mean(agg):.4f}")
print(f"  per-seed ALL above 0.05 floor: {all(a >= 0.05 for a in agg)} -> {agg}")
print(f"  CU exactly 0 on all seeds: {all(run(s)[1] == 0.0 for s in SEEDS)}")
print(f"  RD > 0 on all seeds: {all(run(s)[0] > 0 for s in SEEDS)}")
print(f"  aggregate in (0.05, 0.5): {0.05 < np.mean(agg) < 0.5}")

# Verify the bound: aggregate <= 0.4 (since CU=0, RD<=1, frac=0.4)
print(f"  bound check aggregate<=0.4: {np.mean(agg) <= 0.4}")

# Plausible-below-floor scenario: bootstrap-style — how often would aggregate<0.05?
rng = np.random.default_rng(0)
below = 0; trials = 200
for t in range(trials):
    s = int(rng.integers(1, 10_000_000))
    _, _, a, _, _ = run(s)
    if a < 0.05:
        below += 1
print(f"  across {trials} random seeds, fraction with aggregate<0.05: {below}/{trials}")
