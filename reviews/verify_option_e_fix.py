"""
ARCHITECT's fix for the Option E consumer parameterization (CRITIC BLOCKING ISSUE 1).

PROBLEM (CRITIC): tau=50 multiplicative exp recency spans 9 orders of magnitude
(exp(-999/50) ~ 2e-9 to 1.0), overwhelming the 32-d Gaussian content signal
(~1 order of magnitude). The oracle is recency-dominated on ALL queries, so the
frozen arm (content-only) fails on content-unique (CU) queries too: CU degradation
~0.93, aggregate ~0.89 (near the 1.0 ceiling corner).

ROOT CAUSE: with random Gaussian features, the content signal among ranks 2-10 of
the top-k is essentially flat (top-2:top-10 ratio ~1.06). ANY recency gradient
(>1.06x) overturns ranks 2-10, so the frozen arm's content-based top-k never matches
the oracle's recency-weighted top-k on CU queries. The spec's intended separation
(CU -> content dominates; RD -> recency breaks tie) is unachievable with the
multiplicative product form and random Gaussian features at any tau.

FIX (this script): ADDITIVE relevance + BUCKETED "spike" content features.

  relevance(e, q) = dot(v(e), q)  +  lambda * w(e)
  where  w(e) = exp(-coord_cycle_relative(e) / tau)   (recency weight, same exp / tau=50)

  Feature vectors are BUCKETED: each entry e belongs to a content bucket b(e); its
  feature vector has a large spike (amplitude A) at dimension b(e) plus small noise.
  A query targeting bucket b has a spike at dimension b, so dot(v(e), q) ~ A^2 for
  entries in bucket b and ~ O(A*sigma) for entries in other buckets -- a large,
  clean content gap that recency (additive, bounded contribution lambda*w in [0,lambda])
  CANNOT overturn. This DECOUPLES content from recency:
    * CU queries target buckets of size EXACTLY k (=10): content determines the
      top-k SET (the bucket), recency only reorders WITHIN the set -> recall@k = 1.0
      -> CU degradation ~ 0.  (content dominates, as the spec intends)
    * RD queries target buckets of size K > k: content ties the K entries; recency
      (additive lambda*w) reorders them, so the oracle keeps the k most-recent while
      the frozen arm (w=1.0 constant -> ranks by content-noise) picks k of K at random
      -> the sets differ -> RD degradation = 1 - k/K > 0.  (recency breaks the tie)

  The frozen-arm spec (Option E: coord_cycle_relative = 0 at birth for all entries,
  never re-resolved) is UNCHANGED: w collapses to exp(0)=1.0 for all entries under
  the frozen arm, exactly as Option E specifies. Only the consumer's relevance
  function (additive instead of multiplicative) and the feature/query distribution
  (bucketed spikes instead of random Gaussians) change -- these are consumer
  parameterization, not the frozen arm.

This script simulates the design over seeds 42/43/44 and reports CU / RD / aggregate
degradation, verifying:
  * CU degradation ~ 0  (frozen matches oracle on content-unique queries)
  * RD degradation > 0   (frozen fails to match oracle on recency-discriminative queries)
  * aggregate in (0.05, 0.5) -- comfortably in the open interval, NOT a corner
"""

import numpy as np

# ---------------------------------------------------------------------------
# Config (defaults match the revised spec; swept below for tuning)
# ---------------------------------------------------------------------------
D = 32            # feature dimension (UNCHANGED from spec: consumer_feature_dim)
TAU = 50          # recency decay constant (UNCHANGED from spec: consumer_tau, pinned per Q3-1)
K = 10            # top-k retrieval (UNCHANGED from spec: consumer_k)
N_ENTRIES = 1000  # autobiography size (UNCHANGED: N_entries_final)
NOW = 999         # now at consumer measurement (UNCHANGED: measured at 10x history)
SEEDS = [42, 43, 44]

N_CU = 30         # content-unique queries (UNCHANGED)
N_RD = 20         # recency-discriminative queries (UNCHANGED: 40% of 50)
N_QUERIES = N_CU + N_RD  # 50 (UNCHANGED)

# --- NEW consumer parameters (the fix) ---
A_SIG = 10.0      # spike amplitude (content signal strength)
SIGMA_F = 0.10    # feature noise std (small -> tight content within a bucket)
SIGMA_Q = 0.10    # query noise std
LAMBDA = 16.0     # additive recency coupling (content + lambda * w); 16% of content signal A^2=100
RD_BUCKET_SIZE = 30   # K_rd > k: content-tied group whose recency reorders the top-k


def build_autobiography(seed, n_entries=N_ENTRIES, d=D,
                         n_cu=N_CU, n_rd=N_RD, rd_bucket_size=RD_BUCKET_SIZE,
                         a_sig=A_SIG, sigma_f=SIGMA_F):
    """Build the 1000-entry autobiography with bucketed spike features.

    Bucket assignment (explicit, deterministic, spread across the timeline so
    recency differs within a bucket):
      * n_rd recency-discriminative buckets, each of size rd_bucket_size (> k).
      * n_cu content-unique buckets, each of size exactly k (=10).
      * remaining entries are "fillers" with noise-only features (no spike) --
        they never enter any query's top-k.
    The member cycles of each bucket are spread across 0..n_entries-1 by a seeded
    strided permutation, guaranteeing recency differences within every bucket.
    """
    cycles = np.arange(n_entries)

    # --- assign cycles to bucket members, SPREAD across the timeline ---
    # Each bucket's members must be at DIFFERENT cycles (so recency differs within a
    # bucket -> the oracle's recency weight can reorder them). We round-robin a seeded
    # permutation across buckets so each bucket's members land at permuted positions
    # b, b+n_buckets, b+2*n_buckets, ... -- i.e. at cycles spread across 0..n_entries-1.
    n_buckets_total = n_rd + n_cu
    sizes = [rd_bucket_size]*n_rd + [K]*n_cu          # RD buckets first (size>10), CU buckets (size 10)
    n_labeled = int(sum(sizes))
    assert n_labeled <= n_entries, f"too many labeled entries {n_labeled} > {n_entries}"

    rng_perm = np.random.default_rng(seed * 7_000_000 + 1)
    spread_cycles = rng_perm.permutation(n_entries)[:n_labeled]   # random, hence spread

    # Round-robin assign: member 0 of every bucket, then member 1 of every bucket that
    # still needs members, etc. Buckets hit their target size and drop out; RD buckets
    # (size>10) keep receiving after CU buckets (size 10) are full.
    bucket_of = np.full(n_entries, -1, dtype=np.int64)
    bucket_type = np.full(n_entries, 0, dtype=np.int64)  # 0 filler, 1 cu, 2 rd
    member_idx = [0]*n_buckets_total
    slot = 0
    while slot < n_labeled:
        progressed = False
        for b in range(n_buckets_total):
            if member_idx[b] < sizes[b]:
                c = int(spread_cycles[slot]); slot += 1
                bucket_of[c] = b
                bucket_type[c] = 2 if b < n_rd else 1
                member_idx[b] += 1
                progressed = True
                if slot >= n_labeled:
                    break
        if not progressed:
            break
    assert all(member_idx[b] == sizes[b] for b in range(n_buckets_total)), member_idx

    # --- feature vectors: spike along the bucket's (seeded random unit) direction ---
    # Each bucket b gets a seeded random unit direction u_b in R^d. Entries in bucket b
    # have v(e) = A*u_b + small noise; a query targeting bucket b is q = A*u_b + small
    # noise. Then dot(v(e_b), q_b) ~ A^2 (since ||u_b||=1) -- a large, clean signal --
    # while dot(v(e_b'), q_b) ~ A*dot(u_b', u_b) ~ O(A/sqrt(d)) for other buckets (random
    # directions are near-orthogonal in R^d). This gives a large content gap (A^2 vs
    # ~A*0.2) that the additive recency term (bounded in [0, lambda]) cannot overturn,
    # WITHOUT requiring one reserved dimension per bucket (so d=32 suffices for any
    # number of buckets).
    n_buckets_total = n_rd + n_cu
    directions = np.zeros((n_buckets_total, d))
    for b in range(n_buckets_total):
        rng_dir = np.random.default_rng(seed * 9_000_000 + b)
        u = rng_dir.standard_normal(d)
        directions[b] = u / np.linalg.norm(u)
    # rd buckets -> direction index b in [0..n_rd); cu buckets -> [n_rd..n_rd+n_cu)
    features = np.zeros((n_entries, d))
    for e in range(n_entries):
        bt = bucket_type[e]
        b = bucket_of[e]
        rng = np.random.default_rng(seed * 100_000 + e)
        noise = rng.standard_normal(d) * sigma_f
        if bt == 2:      # rd bucket b (global index 0..n_rd) -> direction b
            features[e] = a_sig * directions[b] + noise
        elif bt == 1:    # cu bucket b (global index n_rd..n_rd+n_cu) -> direction b
            features[e] = a_sig * directions[b] + noise
        else:            # filler (no spike)
            features[e] = noise
    return cycles, features, bucket_of, bucket_type, directions


def build_queries(seed, directions=None, n_cu=N_CU, n_rd=N_RD, d=D,
                   a_sig=A_SIG, sigma_q=SIGMA_Q):
    """Build the 50-query set: 20 recency-discriminative + 30 content-unique.

    Each query targets a bucket: a spike along that bucket's (seeded random unit)
    direction + small noise. RD query j targets rd bucket j (direction index j);
    CU query j targets cu bucket j (direction index n_rd + j)."""
    assert directions is not None
    queries = []
    q_types = []
    q_target_bucket = []
    # RD queries
    for j in range(n_rd):
        rng = np.random.default_rng(seed * 10_000_000 + 500 + j)
        q = a_sig * directions[j] + rng.standard_normal(d) * sigma_q
        queries.append(q); q_types.append('rd'); q_target_bucket.append(j)
    # CU queries
    for j in range(n_cu):
        rng = np.random.default_rng(seed * 1_000_000 + 1000 + n_rd + j)
        q = a_sig * directions[n_rd + j] + rng.standard_normal(d) * sigma_q
        queries.append(q); q_types.append('cu'); q_target_bucket.append(j)
    return np.array(queries), q_types, q_target_bucket


def recency_weight(coord_cycle_relative, tau=TAU):
    """w(e) = exp(-coord / tau). Frozen arm: coord=0 -> w=1.0 for all."""
    return np.exp(-coord_cycle_relative / tau)


def relevance_additive(features, q, coord_cr, lam=LAMBDA, tau=TAU):
    """relevance(e,q) = dot(v(e), q) + lambda * exp(-coord(e)/tau)."""
    content = features @ q
    w = recency_weight(coord_cr, tau=tau)
    return content + lam * w


def topk_indices(relevance, k=K):
    return set(np.argsort(-relevance, kind='stable')[:k])


def recall_k(predicted_topk, oracle_topk, k=K):
    return len(predicted_topk & oracle_topk) / k


def run_seed(seed, lam=LAMBDA, rd_bucket_size=RD_BUCKET_SIZE,
             a_sig=A_SIG, sigma_f=SIGMA_F, sigma_q=SIGMA_Q, k=K, verbose=False):
    cycles, features, bucket_of, bucket_type, directions = build_autobiography(
        seed, rd_bucket_size=rd_bucket_size, a_sig=a_sig, sigma_f=sigma_f)
    queries, q_types, q_targets = build_queries(
        seed, directions=directions, a_sig=a_sig, sigma_q=sigma_q)

    oracle_cr = NOW - cycles.astype(float)   # re-resolved (candidate / oracle)
    frozen_cr = np.zeros(N_ENTRIES)           # Option E: coord=0 at birth for all

    rd_degs, cu_degs = [], []
    for qi, (q, qt) in enumerate(zip(queries, q_types)):
        rel_o = relevance_additive(features, q, oracle_cr, lam=lam)
        rel_f = relevance_additive(features, q, frozen_cr, lam=lam)
        ot = topk_indices(rel_o, k=k)
        ft = topk_indices(rel_f, k=k)
        qf = recall_k(ft, ot, k=k)
        deg = 1.0 - qf
        (rd_degs if qt == 'rd' else cu_degs).append(deg)

    return {
        'seed': seed,
        'rd_deg': float(np.mean(rd_degs)),
        'cu_deg': float(np.mean(cu_degs)),
        'all_deg': float(np.mean(rd_degs + cu_degs)),
        'rd_per': rd_degs, 'cu_per': cu_degs,
    }


# ---------------------------------------------------------------------------
# Baseline reproduction (original multiplicative spec) for sanity
# ---------------------------------------------------------------------------
def run_baseline_multiplicative(seed, tau=TAU, k=K):
    """Reproduce the CRITIC's finding: multiplicative product, random Gaussian features."""
    rng_feat = np.random.default_rng(seed)
    features = np.empty((N_ENTRIES, D))
    for e in range(N_ENTRIES):
        features[e] = np.random.default_rng(seed * 100_000 + e).standard_normal(D)
    # random CU queries + near-dup-pair RD queries (CRITIC's build)
    from verify_option_e import build_queries as crit_queries, build_autobiography as crit_auto
    cycles, features2, _, _, v_base = crit_auto(seed)
    queries, q_types = crit_queries(seed, v_base=v_base)
    oracle_cr = NOW - cycles.astype(float)
    frozen_cr = np.zeros(N_ENTRIES)
    rd_degs, cu_degs = [], []
    for q, qt in zip(queries, q_types):
        dots = features2 @ q
        ro = np.exp(-oracle_cr / tau) * dots
        rf = np.exp(-frozen_cr / tau) * dots
        ot = topk_indices(ro, k=k); ft = topk_indices(rf, k=k)
        deg = 1.0 - recall_k(ft, ot, k=k)
        (rd_degs if qt == 'rd' else cu_degs).append(deg)
    return float(np.mean(rd_degs)), float(np.mean(cu_degs)), float(np.mean(rd_degs + cu_degs))


if __name__ == '__main__':
    print("=" * 88)
    print("ARCHITECT FIX SIMULATION: additive relevance + bucketed spike content")
    print("=" * 88)

    # --- baseline (reproduce CRITIC's 0.89) ---
    print("\n[baseline] original multiplicative spec (reproduce CRITIC):")
    bs = [run_baseline_multiplicative(s) for s in SEEDS]
    print(f"  RD={np.mean([b[0] for b in bs]):.3f}  CU={np.mean([b[1] for b in bs]):.3f}  ALL={np.mean([b[2] for b in bs]):.3f}")

    # --- the fix: FINAL config (lam=16, Krd=30) ---
    print("\n[fix] FINAL config: additive + bucketed")
    print(f"  A={A_SIG} sigma_f={SIGMA_F} sigma_q={SIGMA_Q} lambda={LAMBDA} rd_bucket_size={RD_BUCKET_SIZE} tau={TAU} k={K}")
    rs = [run_seed(s) for s in SEEDS]
    for r in rs:
        print(f"  seed {r['seed']}: RD={r['rd_deg']:.4f} CU={r['cu_deg']:.4f} ALL={r['all_deg']:.4f}  (RD per-query min={min(r['rd_per']):.2f} max={max(r['rd_per']):.2f})")
    rd_m = np.mean([r['rd_deg'] for r in rs]); cu_m = np.mean([r['cu_deg'] for r in rs]); al_m = np.mean([r['all_deg'] for r in rs])
    print(f"  MEAN: RD={rd_m:.4f} CU={cu_m:.4f} ALL={al_m:.4f}")
    print(f"  per-seed ALL > 0 on all seeds: {all(r['all_deg'] > 0 for r in rs)}  (consistency req)")
    print(f"  per-seed ALL > 0.05 floor: {all(r['all_deg'] >= 0.05 for r in rs)}")
    print(f"  CU < 0.1 on all seeds: {all(r['cu_deg'] < 0.1 for r in rs)}  (verification a: content-only succeeds on CU)")
    print(f"  RD > 0 on all seeds: {all(r['rd_deg'] > 0 for r in rs)}  (verification b: recency breaks tie on RD)")
    print(f"  aggregate in (0.05, 0.5): {0.05 < al_m < 0.5}")
    print(f"  --> NOT a corner: aggregate {al_m:.3f} is ~{al_m/0.05:.1f}x the floor and ~{0.5/al_m:.1f}x below the ceiling")

    # --- mechanism verification (seed 42): show the oracle picks recent, frozen picks by content-noise ---
    print("\n[mechanism] seed 42, RD query 0: does recency select the recent subset?")
    cycles, features, bucket_of, bucket_type, directions = build_autobiography(42)
    queries, q_types, q_targets = build_queries(42, directions=directions)
    oracle_cr = NOW - cycles.astype(float); frozen_cr = np.zeros(N_ENTRIES)
    q = queries[0]
    rel_o = relevance_additive(features, q, oracle_cr); rel_f = relevance_additive(features, q, frozen_cr)
    ot = topk_indices(rel_o); ft = topk_indices(rel_f)
    o_cycles = sorted(int(cycles[i]) for i in ot); f_cycles = sorted(int(cycles[i]) for i in ft)
    print(f"  RD bucket 0 members (cycles, spread): {sorted(int(cycles[i]) for i in range(N_ENTRIES) if bucket_of[i]==0)}")
    print(f"  oracle top-10 cycles (recency-selected, recent first): {o_cycles}")
    print(f"  frozen top-10 cycles (content-noise, scattered):      {f_cycles}")
    print(f"  overlap (recall@10): {len(ot & ft)/10:.2f}  degradation: {1-len(ot & ft)/10:.2f}")
    print("\n[mechanism] seed 42, CU query 0: does content alone determine top-10?")
    q = queries[N_RD]
    rel_o = relevance_additive(features, q, oracle_cr); rel_f = relevance_additive(features, q, frozen_cr)
    ot = topk_indices(rel_o); ft = topk_indices(rel_f)
    cu_bucket = N_RD  # cu bucket 0 is global index n_rd
    cu_members = sorted(int(cycles[i]) for i in range(N_ENTRIES) if bucket_of[i]==cu_bucket)
    print(f"  CU bucket 0 members (exactly 10, the content-determined top-10): {cu_members}")
    print(f"  oracle top-10 == CU bucket? {ot == set(i for i in range(N_ENTRIES) if bucket_of[i]==cu_bucket)}")
    print(f"  frozen top-10 == CU bucket? {ft == set(i for i in range(N_ENTRIES) if bucket_of[i]==cu_bucket)}")
    print(f"  recall@10: {len(ot & ft)/10:.2f}  degradation: {1-len(ot & ft)/10:.2f}")

    # --- save final results to JSON ---
    import json
    results_out = {
        'config': {'A_sig': A_SIG, 'sigma_f': SIGMA_F, 'sigma_q': SIGMA_Q, 'lambda': LAMBDA,
                   'rd_bucket_size': RD_BUCKET_SIZE, 'tau': TAU, 'k': K, 'd': D,
                   'n_entries': N_ENTRIES, 'now': NOW, 'n_cu': N_CU, 'n_rd': N_RD},
        'baseline_critic': {'RD': float(np.mean([b[0] for b in bs])), 'CU': float(np.mean([b[1] for b in bs])), 'ALL': float(np.mean([b[2] for b in bs]))},
        'final': {
            'per_seed': [{'seed': r['seed'], 'RD': r['rd_deg'], 'CU': r['cu_deg'], 'ALL': r['all_deg']} for r in rs],
            'mean': {'RD': rd_m, 'CU': cu_m, 'ALL': al_m},
            'checks': {
                'all_seeds_positive': bool(all(r['all_deg'] > 0 for r in rs)),
                'all_seeds_above_floor': bool(all(r['all_deg'] >= 0.05 for r in rs)),
                'cu_below_0.1_all_seeds': bool(all(r['cu_deg'] < 0.1 for r in rs)),
                'rd_positive_all_seeds': bool(all(r['rd_deg'] > 0 for r in rs)),
                'aggregate_in_open_interval': bool(0.05 < al_m < 0.5),
            },
        },
    }
    with open('verify_option_e_fix_results.json', 'w') as f:
        json.dump(results_out, f, indent=2)
    print("\n[results saved] verify_option_e_fix_results.json")

    # --- sweep RD bucket size (the main tuning knob) ---
    print("\n[sweep] rd_bucket_size (lambda=8, tau=50):")
    print(f"  {'Krd':>4} | {'RD':>6} | {'CU':>6} | {'ALL':>6} | theory(1-k/Krd)")
    for krd in [11, 12, 13, 15, 17, 20, 25, 30, 33, 35]:
        rs = [run_seed(s, rd_bucket_size=krd) for s in SEEDS]
        rd = np.mean([r['rd_deg'] for r in rs]); cu = np.mean([r['cu_deg'] for r in rs]); al = np.mean([r['all_deg'] for r in rs])
        print(f"  {krd:>4} | {rd:>6.3f} | {cu:>6.3f} | {al:>6.3f} | {1-K/krd:.3f}")

    # --- sweep tau (does a gentler recency over the full range help RD while CU stays 0?) ---
    print("\n[sweep] tau (rd_bucket_size=15, lambda=8) -- CU must stay 0:")
    print(f"  {'tau':>5} | {'RD':>6} | {'CU':>6} | {'ALL':>6}")
    for tau in [50, 100, 150, 200, 300, 500, 1000]:
        rs = [run_seed(s, rd_bucket_size=15, lam=8) for s in SEEDS] if tau==50 else None
        # patch tau via monkeypatch of the module constant used inside run_seed
        import verify_option_e_fix as M
        old = M.TAU; M.TAU = tau
        rs = [run_seed(s, rd_bucket_size=15, lam=8) for s in SEEDS]
        M.TAU = old
        rd = np.mean([r['rd_deg'] for r in rs]); cu = np.mean([r['cu_deg'] for r in rs]); al = np.mean([r['all_deg'] for r in rs])
        print(f"  {tau:>5} | {rd:>6.3f} | {cu:>6.3f} | {al:>6.3f}")

    # --- sweep lambda x Krd combos for a comfortable aggregate in (0.05, 0.5) ---
    print("\n[sweep] lambda x Krd (tau=50) -- looking for ALL in (0.08, 0.30), CU=0:")
    print(f"  {'lam':>4} {'Krd':>4} | {'RD':>6} | {'CU':>6} | {'ALL':>6}")
    for lam in [8, 16, 32]:
        for krd in [20, 25, 30, 35]:
            rs = [run_seed(s, lam=lam, rd_bucket_size=krd) for s in SEEDS]
            rd = np.mean([r['rd_deg'] for r in rs]); cu = np.mean([r['cu_deg'] for r in rs]); al = np.mean([r['all_deg'] for r in rs])
            print(f"  {lam:>4} {krd:>4} | {rd:>6.3f} | {cu:>6.3f} | {al:>6.3f}")
