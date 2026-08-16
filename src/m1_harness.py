#!/usr/bin/env python3
"""
M1 Harness — instrumentation validation for the L18 control battery.

Single self-contained script. Generates a synthetic retrieval-ranking toy
problem with known ground truth (deterministic per seed), runs the 6-arm
control battery (empty/permuted/shuffled/oracle/naive/frozen) over 4
higher-is-better metrics (auroc, ndcg_at_k, spearman_rho, recall_at_k) across
3 seeds, evaluates the 5 invariants (I1-I5), runs the L20 drift self-test, and
writes 5 output files.

One launch command:
    python m1_harness.py --seeds 42,43,44 --output-dir ./m1_output

All numeric bars/tolerances/thresholds are LOCKED (Rebecca-approved M0
decision sheet). No value here is tuned. Only numpy, scipy, and the standard
library are imported.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
from scipy.stats import spearmanr, pearsonr, rankdata

# ---------------------------------------------------------------------------
# LOCKED constants (do not tune)
# ---------------------------------------------------------------------------
N_ITEMS = 200
N_CYCLES = 50
N_RELEVANT = 20  # R
K = 20            # retrieval cutoff == R so oracle Recall@k = 1.0
BASE_RATE = N_RELEVANT / N_ITEMS  # 0.10 (L19 pre-registered)

# feature weights for ground-truth relevance (locked)
W_F1 = 0.4
W_F2 = 0.3
W_F3 = 0.3
W_Z = 0.1

# landmark subset size = 20% of N
N_LANDMARK = N_ITEMS // 5  # 40

# shuffled arm independent stream offset (deterministic, distinct)
SHUFFLED_SEED_OFFSET = 1000

ARM_ORDER = ["empty", "permuted", "shuffled", "oracle", "naive", "frozen"]
METRIC_ORDER = ["auroc", "ndcg_at_k", "spearman_rho", "recall_at_k"]

# Invariant bars (locked)
I2_FLOOR = 0.95
I4_BAR = 0.30
I3_TOLERANCE = {
    "auroc": {"scale": "probability", "tolerance": 0.05},
    "ndcg_at_k": {"scale": "probability", "tolerance": 0.05},
    "spearman_rho": {"scale": "correlation", "tolerance": 0.15},
    "recall_at_k": {"scale": "probability", "tolerance": 0.05},
}
CONTAMINATION_ARMS = ["empty", "permuted", "shuffled"]

# O-14 empirical-null configuration.
# Distinct seed range for the chance-floor (naive arm) null distribution; must
# not collide with the main battery seeds [42, 43, 44]. >=100 replicates
# (Rebecca prerequisite: raised from 30 to 100 for a more stable empirical band).
NULL_SEED_START = 100
NULL_SEED_END_EXCLUSIVE = 200  # => seeds 100..199 (100 replicates)

# Empirical-null band: central 99% interval.
NULL_LOW_PCT = 0.5
NULL_HIGH_PCT = 99.5

# Low-power flag thresholds (band width = high_pct - low_pct).
# correlation-scale metrics (range [-1,1]): 2 * 0.15 = 0.30
# probability-scale metrics (range [0,1]):  2 * 0.10 = 0.20
LOWPOWER_WIDTH = {
    "correlation": 0.30,
    "probability": 0.20,
}

# L20 drift (locked)
L20_DRIFT_CRITERION = 0.70
L20_SELFTEST_THRESHOLD = 0.50  # stricter, for margin

SCHEMA_VERSION = "1.0"
PROFILE_VERSION = "m1-locked-1.0"


# ---------------------------------------------------------------------------
# Toy problem construction (deterministic per seed)
# ---------------------------------------------------------------------------
# RNG DRAW ORDER (fixed contract for I1 reproducibility), per seed s, using a
# single Generator g = np.random.default_rng(s):
#   1. f2 = g.random(N)                      # salience, per item
#   2. landmark_idx = g.choice(N, N_LANDMARK, replace=False)  # 20% subset
#   3. z  = g.standard_normal(N)             # noise, per item
#   --- ground truth g_i / label y built from above (deterministic) ---
#   4. empty_perm   = g.permutation(N)       # empty-arm tie-break permutation
#   5. permuted_pi  = g.permutation(N)       # permuted-arm label permutation
#   6. naive_s      = g.random(N)            # naive-arm scores
# The shuffled arm uses a SEPARATE Generator default_rng(s + SHUFFLED_SEED_OFFSET)
# with the same draw order (steps 1-3) to build g' (independent probe).

def build_ground_truth(seed: int):
    """Return (f1, f2, f3, g, y, z, rng) for the given seed."""
    rng = np.random.default_rng(seed)

    # deterministic cycle / age / f1
    c = np.arange(N_ITEMS) % N_CYCLES          # cycle position 0..49
    age = N_CYCLES - 1 - c                      # age 0..49
    f1 = np.exp(-age / 25.0)                    # recency signal in (0,1]

    # seeded draws (order documented above)
    f2 = rng.random(N_ITEMS)                    # step 1
    landmark_idx = rng.choice(N_ITEMS, size=N_LANDMARK, replace=False)  # step 2
    f3 = np.zeros(N_ITEMS)
    f3[landmark_idx] = 1.0
    z = rng.standard_normal(N_ITEMS)            # step 3

    g = np.clip(W_F1 * f1 + W_F2 * f2 + W_F3 * f3 + W_Z * z, 0.0, 1.0)

    # binary label: y_i = 1 iff g_i in top-R values, ties broken by lower index.
    # np.argsort with stable kind on -g gives ascending -g => descending g,
    # ties resolved by lower index.
    top_idx = np.argsort(-g, kind="stable")[:N_RELEVANT]
    y = np.zeros(N_ITEMS, dtype=int)
    y[top_idx] = 1

    return f1, f2, f3, g, y, z, rng


def build_shuffled_truth(seed: int):
    """Independent g' for the shuffled arm (separate RNG stream).

    O-13 fix: the original implementation recomputed f1' from the SAME
    deterministic age map (age = N_CYCLES-1 - (i % N_CYCLES)), which is
    identical to f1 and carries 40% weight, producing a structural
    corr(g, g') that is seed-invariant and non-chance. f1 is deterministic
    given i, NOT drawn from the RNG, so giving the probe its own seed did not
    decouple f1.

    Fix: before computing f1', independently permute the item<->age map with a
    seeded permutation sigma drawn from the probe's RNG (rng2). Then
        age'_i   = age_{sigma(i)}
        f1'_i    = exp(-age'_i / 25)        # now decoupled from f1
        f2',f3',z' drawn from rng2 as before
        g'_i     = clip(0.4*f1' + 0.3*f2' + 0.3*f3' + 0.1*z', 0, 1)
    The score vector is s = g'; metrics are computed against the original g/y.
    """
    rng2 = np.random.default_rng(seed + SHUFFLED_SEED_OFFSET)
    c = np.arange(N_ITEMS) % N_CYCLES
    age = N_CYCLES - 1 - c
    # 1. seeded permutation sigma from the probe's RNG
    sigma = rng2.permutation(N_ITEMS)
    # 2. age'_i = age_{sigma(i)}
    age_p = age[sigma]
    # 3. f1'_i = exp(-age'_i / 25) -- decoupled from the original f1
    f1p = np.exp(-age_p / 25.0)
    # 4. f2', f3', z' from rng2 as before
    f2p = rng2.random(N_ITEMS)
    landmark_idx = rng2.choice(N_ITEMS, size=N_LANDMARK, replace=False)
    f3p = np.zeros(N_ITEMS)
    f3p[landmark_idx] = 1.0
    zp = rng2.standard_normal(N_ITEMS)
    # 5. g'_i = clip(0.4*f1' + 0.3*f2' + 0.3*f3' + 0.1*z', 0, 1)
    gp = np.clip(W_F1 * f1p + W_F2 * f2p + W_F3 * f3p + W_Z * zp, 0.0, 1.0)
    # 6. score vector is s = g' (handled by caller); return g'
    return gp


def build_arm_scores(seed: int, f1, g, y, rng):
    """Return dict arm_name -> score vector s (length N).

    Also returns the empty-arm tie-break permutation (inverse) used for ranking.
    """
    # step 4: empty-arm random tie-break permutation
    empty_perm = rng.permutation(N_ITEMS)
    # step 5: permuted-arm label permutation
    permuted_pi = rng.permutation(N_ITEMS)
    # step 6: naive scores
    naive_s = rng.random(N_ITEMS)

    # empty: all zeros; ranking determined by empty_perm (random order)
    s_empty = np.zeros(N_ITEMS)
    # permuted: s_i = g_{pi(i)}
    s_permuted = g[permuted_pi]
    # shuffled: independent probe
    g_shuffled = build_shuffled_truth(seed)
    s_shuffled = g_shuffled
    # oracle: s = g
    s_oracle = g.copy()
    # naive: random uniform
    s_naive = naive_s
    # frozen: f1 normalized to [0,1] (min-max; f1 in (0,1] so near-identity)
    f1_min = f1.min()
    f1_max = f1.max()
    if f1_max > f1_min:
        s_frozen = (f1 - f1_min) / (f1_max - f1_min)
    else:
        s_frozen = np.zeros_like(f1)

    # empty-arm tie-break key: we want ranked order == empty_perm.
    # topk_order uses lexsort((tiebreak, -s)); with s all 0 it sorts by tiebreak
    # ascending. We set tiebreak[empty_perm[j]] = j so argsort(tiebreak) ==
    # empty_perm.
    empty_tiebreak = np.empty(N_ITEMS, dtype=np.int64)
    empty_tiebreak[empty_perm] = np.arange(N_ITEMS)

    scores = {
        "empty": s_empty,
        "permuted": s_permuted,
        "shuffled": s_shuffled,
        "oracle": s_oracle,
        "naive": s_naive,
        "frozen": s_frozen,
    }
    tiebreaks = {
        "empty": empty_tiebreak,
        # all other arms: ties measure-zero; break by lower index
    }
    return scores, tiebreaks


# ---------------------------------------------------------------------------
# Metrics (higher-is-better)
# ---------------------------------------------------------------------------
def auroc(s, y):
    """AUROC via Mann-Whitney U form: P(s_pos > s_neg), ties contribute 0.5.

    Computed with average-rank rankdata. Constant scores => 0.5 exactly.
    Perfect s=g (positives all outrank negatives) => 1.0 exactly.
    """
    n_pos = int(y.sum())
    n_neg = N_ITEMS - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.0
    ranks = rankdata(s, method="average")
    rank_sum_pos = ranks[y == 1].sum()
    u = rank_sum_pos - n_pos * (n_pos + 1) / 2.0
    return float(u / (n_pos * n_neg))


def _topk_order(s, k, tiebreak):
    """Indices of top-k items by s descending; ties by tiebreak ascending."""
    if tiebreak is None:
        tiebreak = np.arange(len(s))
    order = np.lexsort((tiebreak, -s))  # primary -s (desc), secondary tiebreak asc
    return order[:k]


def ndcg_at_k(s, g, k, tiebreak=None):
    """NDCG@k using graded relevance g. Oracle (s=g) => 1.0 exactly."""
    order = _topk_order(s, k, tiebreak)
    discounts = 1.0 / np.log2(np.arange(2, k + 2))
    dcg = float(np.sum(g[order] * discounts))
    ideal_order = np.argsort(-g, kind="stable")[:k]
    idcg = float(np.sum(g[ideal_order] * discounts))
    if idcg == 0.0:
        return 0.0
    return dcg / idcg


def recall_at_k(s, y, k, R, tiebreak=None):
    """Recall@k = |top-k by s ∩ relevant| / R. Oracle => 1.0 exactly."""
    order = _topk_order(s, k, tiebreak)
    return float(np.sum(y[order])) / R


def spearman_rho(s, g):
    """Spearman rho between s and g. Constant s => 0.0 (NaN handled)."""
    if np.std(s) == 0.0:
        return 0.0
    r = spearmanr(s, g).correlation
    if r is None or (isinstance(r, float) and np.isnan(r)):
        return 0.0
    return float(r)


def compute_metrics(s, g, y, tiebreak=None):
    return {
        "auroc": auroc(s, y),
        "ndcg_at_k": ndcg_at_k(s, g, K, tiebreak),
        "spearman_rho": spearman_rho(s, g),
        "recall_at_k": recall_at_k(s, y, K, N_RELEVANT, tiebreak),
    }


# ---------------------------------------------------------------------------
# Full battery for one seed
# ---------------------------------------------------------------------------
def run_seed(seed: int):
    """Run all 6 arms x 4 metrics for one seed. Returns dict arm->{metric:val}."""
    f1, f2, f3, g, y, z, rng = build_ground_truth(seed)
    scores, tiebreaks = build_arm_scores(seed, f1, g, y, rng)
    out = {}
    for arm in ARM_ORDER:
        tb = tiebreaks.get(arm)
        out[arm] = compute_metrics(scores[arm], g, y, tb)
    return out


def run_battery(seeds):
    """Run the battery for all seeds. Returns {seed_str: {arm: {metric: val}}}."""
    return {str(s): run_seed(s) for s in seeds}


def run_naive_arm_only(seed: int):
    """Run ONLY the naive arm for one seed (chance floor).

    Used by the O-14 empirical-null distribution. Returns {metric: val}.
    Reuses build_ground_truth + build_arm_scores so the naive arm here is
    constructed identically to the naive arm in the main battery.
    """
    f1, f2, f3, g, y, z, rng = build_ground_truth(seed)
    scores, tiebreaks = build_arm_scores(seed, f1, g, y, rng)
    tb = tiebreaks.get("naive")
    return compute_metrics(scores["naive"], g, y, tb)


# ---------------------------------------------------------------------------
# Helpers for aggregation
# ---------------------------------------------------------------------------
def mean_over_seeds(results, seeds):
    """Return {arm: {metric: mean}}."""
    out = {arm: {m: 0.0 for m in METRIC_ORDER} for arm in ARM_ORDER}
    for s in seeds:
        for arm in ARM_ORDER:
            for m in METRIC_ORDER:
                out[arm][m] += results[str(s)][arm][m]
    for arm in ARM_ORDER:
        for m in METRIC_ORDER:
            out[arm][m] /= len(seeds)
    return out


def profile_vector(profile_mean):
    """Flatten arm x metric mean-over-seeds into 24 floats."""
    vec = []
    for arm in ARM_ORDER:
        for m in METRIC_ORDER:
            vec.append(float(profile_mean[arm][m]))
    return vec


# ---------------------------------------------------------------------------
# L20 drift self-test
# ---------------------------------------------------------------------------
def _safe_pearson(a, b):
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return 0.0
    r = pearsonr(a, b)[0]
    if r is None or (isinstance(r, float) and np.isnan(r)):
        return 0.0
    return float(r)


def l20_self_test(pv):
    """Run the two pinned perturbations. Returns the l20_self_test dict."""
    pv = np.array(pv, dtype=float)
    blocks = [pv[i * 4:(i + 1) * 4] for i in range(6)]  # 6 blocks of 4

    # no-drift: unchanged
    no_drift = _safe_pearson(pv, pv)

    # perturbation 1: full arm-block reversal
    reversed_vec = np.concatenate(blocks[::-1])
    corr1 = _safe_pearson(pv, reversed_vec)

    # perturbation 2: empty(0) <-> oracle(3) block swap
    swapped = [blocks[i] for i in range(6)]
    swapped[0], swapped[3] = swapped[3], swapped[0]
    swapped_vec = np.concatenate(swapped)
    corr2 = _safe_pearson(pv, swapped_vec)

    return {
        "no_drift_corr": no_drift,
        "no_drift_passes": bool(no_drift == 1.0),
        "perturbation_1": "full_arm_block_reversal",
        "perturbation_1_corr": corr1,
        "perturbation_2": "empty_oracle_swap",
        "perturbation_2_corr": corr2,
        "both_perturbations_flag_drift": bool(corr1 < L20_SELFTEST_THRESHOLD
                                             and corr2 < L20_SELFTEST_THRESHOLD),
    }


# ---------------------------------------------------------------------------
# Invariant suite
# ---------------------------------------------------------------------------
def check_I1(results_run1, results_run2, seeds):
    per_seed = {}
    all_zero = True
    for s in seeds:
        max_diff = 0.0
        for arm in ARM_ORDER:
            for m in METRIC_ORDER:
                d = abs(results_run1[str(s)][arm][m] - results_run2[str(s)][arm][m])
                if d > max_diff:
                    max_diff = d
        per_seed[str(s)] = float(max_diff)
        if max_diff != 0.0:
            all_zero = False
    return {
        "passes": bool(all_zero),
        "detail": "rerun matches run for all 3 seeds",
        "per_seed_max_abs_diff": per_seed,
    }


def check_I2(results, seeds):
    per_metric = {}
    passes = True
    for m in METRIC_ORDER:
        min_val = min(results[str(s)]["oracle"][m] for s in seeds)
        per_metric[m] = float(min_val)
        if min_val < I2_FLOOR:
            passes = False
    return {"passes": bool(passes), "per_metric": per_metric, "floor": I2_FLOOR}


def check_I3(profile_mean, seeds, results, null_naive_values, null_seeds):
    """I3: contamination arms at the chance floor.

    O-14 empirical-null method. Replaces the fixed two-tier tolerance
    (±0.05 / ±0.15) with a data-driven band derived from the naive arm's
    actual metric distribution across >=100 null-replicate seeds
    (Rebecca prerequisite: raised from 30 to 100).

    # ------------------------------------------------------------------
    # LESSON: Never assume an arm's chance value; derive it from the arm's
    # actual null distribution.
    # ------------------------------------------------------------------
    A contamination arm passes I3 for a metric iff its 3-seed mean falls
    within the central 99% interval [0.5th, 99.5th percentile] of the naive
    arm's empirical null distribution for that metric.
    """
    # 1-3. empirical band per metric from the naive arm null distribution
    per_metric_band = {}
    per_metric_null_stats = {}
    for m in METRIC_ORDER:
        vals = np.array(null_naive_values[m], dtype=float)
        lower = float(np.percentile(vals, NULL_LOW_PCT))
        upper = float(np.percentile(vals, NULL_HIGH_PCT))
        width = upper - lower
        scale = I3_TOLERANCE[m]["scale"]
        low_power = bool(width > LOWPOWER_WIDTH[scale])
        per_metric_band[m] = {
            "lower": lower,
            "upper": upper,
            "width": width,
            "low_power": low_power,
        }
        per_metric_null_stats[m] = {
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals, ddof=1)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals)),
        }

    # 4-5. each contamination arm's 3-seed mean within the empirical band
    per_arm_in_band = {}
    all_pass = True
    for arm in CONTAMINATION_ARMS:
        per_arm_in_band[arm] = {}
        for m in METRIC_ORDER:
            arm_mean = profile_mean[arm][m]
            band = per_metric_band[m]
            in_band = bool(band["lower"] <= arm_mean <= band["upper"])
            per_arm_in_band[arm][m] = in_band
            if not in_band:
                all_pass = False

    # O-13 verification: shuffled arm's across-seed mean per metric, for
    # Rebecca's verification duty.
    shuffled_post_fix_verification = {
        m: float(profile_mean["shuffled"][m]) for m in METRIC_ORDER
    }

    return {
        "passes": bool(all_pass),
        "method": "empirical_null",
        "null_replicate_count": len(null_seeds),
        "null_seeds": list(null_seeds),
        "per_metric_empirical_band": per_metric_band,
        "per_metric_null_stats": per_metric_null_stats,
        "per_arm_per_metric_in_band": per_arm_in_band,
        "shuffled_post_fix_verification": shuffled_post_fix_verification,
        "method_note": (
            "central 99% interval [0.5th, 99.5th percentile] of the naive "
            "arm over null replicate seeds; an arm passes a metric iff its "
            "3-seed mean falls within that band."
        ),
    }


def check_I4(results, profile_mean, seeds):
    per_metric = {}
    all_pass = True
    for m in METRIC_ORDER:
        oracle_mean = profile_mean["oracle"][m]
        naive_mean = profile_mean["naive"][m]
        margin = oracle_mean - naive_mean
        passes_per_seed = []
        for s in seeds:
            ok = results[str(s)]["oracle"][m] - results[str(s)]["naive"][m] >= I4_BAR
            passes_per_seed.append(bool(ok))
            if not ok:
                all_pass = False
        mean_pass = margin >= I4_BAR
        if not mean_pass:
            all_pass = False
        per_metric[m] = {
            "oracle_mean": float(oracle_mean),
            "naive_mean": float(naive_mean),
            "margin": float(margin),
            "bar": I4_BAR,
            "passes_per_seed": passes_per_seed,
            "passes": bool(mean_pass and all(ok for ok in passes_per_seed)),
        }
    return {"passes": bool(all_pass), "bar": I4_BAR, "per_metric": per_metric}


def check_I5(profile_mean, results, seeds):
    """Frozen ordering with pre-registered fallback.

    Spearman: strict naive < frozen < oracle (construction-guaranteed, no fallback).
    auroc/ndcg_at_k/recall_at_k: strict frozen < oracle AND non-strict frozen > naive;
      if frozen <= naive on any seed for that metric, mark N/A (logged) but do not fail.
    """
    per_metric = {}
    na_metrics = []
    spearman_ok = True
    nonstrict_ok = True

    # Spearman: strict on every seed
    for m in ["spearman_rho"]:
        n_below_oracle = all(profile_mean["frozen"][m] < profile_mean["oracle"][m] for _ in [0])
        strict_seed_ok = all(
            results[str(s)]["naive"][m] < results[str(s)]["frozen"][m] < results[str(s)]["oracle"][m]
            for s in seeds
        )
        mean_ok = (profile_mean["naive"][m] < profile_mean["frozen"][m]
                   < profile_mean["oracle"][m])
        per_metric[m] = "naive<frozen<oracle"
        if not (mean_ok and strict_seed_ok):
            spearman_ok = False

    # non-Spearman: strict frozen < oracle (mean), non-strict frozen > naive per seed
    for m in ["auroc", "ndcg_at_k", "recall_at_k"]:
        frozen_below_oracle = profile_mean["frozen"][m] < profile_mean["oracle"][m]
        frozen_above_naive_seeds = []
        for s in seeds:
            ok = results[str(s)]["frozen"][m] > results[str(s)]["naive"][m]
            frozen_above_naive_seeds.append(ok)
        if not frozen_below_oracle:
            nonstrict_ok = False
            per_metric[m] = "FAIL: frozen >= oracle"
            continue
        if all(frozen_above_naive_seeds):
            per_metric[m] = "naive<frozen<oracle"
        else:
            # fallback: N/A on this metric, logged. Build an EXPLICIT per-seed
            # strict/non-strict rationale string (RUN-2 hygiene: the old generic
            # "non-strict not met" wording was misleading because the mean-level
            # non-strict condition actually held). Report, per seed, whether
            # frozen > naive (strict) and frozen < oracle (strict), with the
            # actual values, plus the mean-level comparison and the N/A reason.
            passing_seeds = [str(s) for s, ok in zip(seeds, frozen_above_naive_seeds) if ok]
            failing_seeds = []
            for s, ok in zip(seeds, frozen_above_naive_seeds):
                if not ok:
                    fv = results[str(s)]["frozen"][m]
                    nv = results[str(s)]["naive"][m]
                    ov = results[str(s)]["oracle"][m]
                    # characterize the failure: tie (frozen == naive) or inversion
                    if fv == nv:
                        reason = f"frozen=naive={fv:.4f} (tie at metric granularity)"
                    else:
                        reason = f"frozen={fv:.4f} <= naive={nv:.4f} (inversion)"
                    failing_seeds.append(f"seed {s}: {reason}; frozen<oracle strict={fv < ov}")
            frozen_mean = profile_mean["frozen"][m]
            naive_mean = profile_mean["naive"][m]
            oracle_mean = profile_mean["oracle"][m]
            mean_holds = frozen_mean > naive_mean
            per_metric[m] = (
                f"N/A on {m}: " + "; ".join(failing_seeds) +
                f"; seeds {','.join(passing_seeds)} pass strict. "
                f"Mean-level: frozen_mean={frozen_mean:.4f} "
                f"{'>' if mean_holds else '<='} naive_mean={naive_mean:.4f} "
                f"({'holds' if mean_holds else 'NOT held'}); "
                f"frozen_mean={frozen_mean:.4f} < oracle_mean={oracle_mean:.4f} "
                f"({'holds' if frozen_mean < oracle_mean else 'NOT held'}). "
                f"N/A per pre-registered fallback (non-strict frozen>naive not met on "
                f"{len(failing_seeds)} seed(s); suite does not fail on this alone)."
            )
            na_metrics.append(m)
            # per fallback rule: require strict only on Spearman + non-strict frozen>naive
            # on remaining three. If frozen<=naive on a non-Spearman metric, that metric
            # is N/A but does NOT fail the suite; the suite still requires the strict
            # Spearman plus non-strict on the OTHER non-Spearman metrics that did pass.
            # Here we record N/A; suite passes if spearman strict holds and all non-Spearman
            # that are NOT N/A satisfy frozen<oracle and frozen>naive.

    passes = bool(spearman_ok and nonstrict_ok)
    # If any non-Spearman metric is N/A, the suite does not fail on that alone
    # (pre-registered fallback). It passes iff Spearman strict AND every non-Spearman
    # metric satisfies frozen<oracle AND (frozen>naive OR marked N/A).
    if na_metrics:
        # recompute: spearman strict must hold; non-Spearman must have frozen<oracle;
        # frozen>naive either holds (strict pass) or is N/A.
        passes = bool(spearman_ok)
        for m in ["auroc", "ndcg_at_k", "recall_at_k"]:
            if profile_mean["frozen"][m] >= profile_mean["oracle"][m]:
                passes = False

    return {"passes": bool(passes), "per_metric": per_metric}


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def get_commit_hash():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=os.path.dirname(os.path.abspath(__file__)) or ".",
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            return out.stdout.strip()
        return "pending -- no git repo"
    except Exception:
        return "pending -- no git repo"


def get_python_version():
    """Exact 'Python X.Y.Z' string via platform.python_version()."""
    return "Python " + platform.python_version()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="M1 harness (L18 control battery validation).")
    parser.add_argument("--seeds", default="42,43,44",
                        help="comma-separated integer seeds (default 42,43,44)")
    parser.add_argument("--output-dir", default="./m1_output",
                        help="output directory (default ./m1_output)")
    args = parser.parse_args()

    seeds = [int(x) for x in args.seeds.split(",") if x.strip() != ""]
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    log_path = os.path.join(output_dir, "m1_run.log")
    log_fh = open(log_path, "w")

    def tee(msg):
        print(msg)
        log_fh.write(msg + "\n")
        log_fh.flush()

    t_start = time.perf_counter()

    tee("=" * 72)
    tee("M1 HARNESS -- L18 control battery validation")
    tee(f"seeds={seeds}  output_dir={output_dir}")
    tee(f"python_version_runtime={get_python_version()}")
    tee(f"numpy={np.__version__}  scipy={__import__('scipy').__version__}")
    tee("=" * 72)

    # --- Run 1 ---
    tee("[run1] running battery over seeds...")
    results_run1 = run_battery(seeds)
    for s in seeds:
        tee(f"  seed {s}: " + ", ".join(
            f"{arm}=" + ", ".join(f"{m}={results_run1[str(s)][arm][m]:.4f}"
                                  for m in METRIC_ORDER)
            for arm in ARM_ORDER))

    # --- I1: re-run all seeds ---
    tee("[I1] reproducibility: re-running all seeds (run 2)...")
    results_run2 = run_battery(seeds)
    i1 = check_I1(results_run1, results_run2, seeds)
    tee(f"[I1] passes={i1['passes']}  per_seed_max_abs_diff={i1['per_seed_max_abs_diff']}")

    # --- aggregates ---
    profile_mean = mean_over_seeds(results_run1, seeds)
    pv = profile_vector(profile_mean)

    # --- invariants ---
    i2 = check_I2(results_run1, seeds)
    tee(f"[I2] passes={i2['passes']}  per_metric={i2['per_metric']} floor={i2['floor']}")

    # --- O-14: empirical null distribution (naive arm, >=100 distinct seeds) ---
    null_seeds = list(range(NULL_SEED_START, NULL_SEED_END_EXCLUSIVE))
    # guard: ensure no collision with main battery seeds
    if set(null_seeds) & set(seeds):
        raise RuntimeError(
            f"null seeds collide with main seeds: "
            f"{set(null_seeds) & set(seeds)}")
    tee(f"[I3] building empirical null from naive arm over {len(null_seeds)} "
        f"seeds ({null_seeds[0]}..{null_seeds[-1]})...")
    null_naive_values = {m: [] for m in METRIC_ORDER}
    for ns in null_seeds:
        nm = run_naive_arm_only(ns)
        for m in METRIC_ORDER:
            null_naive_values[m].append(nm[m])

    i3 = check_I3(profile_mean, seeds, results_run1, null_naive_values, null_seeds)
    tee(f"[I3] passes={i3['passes']}  method={i3['method']}  "
        f"null_replicates={i3['null_replicate_count']}")
    for m in METRIC_ORDER:
        b = i3["per_metric_empirical_band"][m]
        tee(f"      band {m}: [{b['lower']:.4f}, {b['upper']:.4f}] "
            f"width={b['width']:.4f} low_power={b['low_power']}")
    for arm in CONTAMINATION_ARMS:
        tee(f"      {arm}: " + ", ".join(
            f"{m}={profile_mean[arm][m]:.4f}"
            f"({'in' if i3['per_arm_per_metric_in_band'][arm][m] else 'OUT'})"
            for m in METRIC_ORDER))
    tee(f"      shuffled_post_fix_verification: " + ", ".join(
        f"{m}={i3['shuffled_post_fix_verification'][m]:.4f}"
        for m in METRIC_ORDER))

    i4 = check_I4(results_run1, profile_mean, seeds)
    tee(f"[I4] passes={i4['passes']} bar={i4['bar']}")
    for m in METRIC_ORDER:
        d = i4["per_metric"][m]
        tee(f"      {m}: oracle_mean={d['oracle_mean']:.4f} naive_mean={d['naive_mean']:.4f} "
            f"margin={d['margin']:.4f} passes_per_seed={d['passes_per_seed']} passes={d['passes']}")

    i5 = check_I5(profile_mean, results_run1, seeds)
    tee(f"[I5] passes={i5['passes']}  per_metric={i5['per_metric']}")

    invariant_suite_green = bool(i1["passes"] and i2["passes"] and i3["passes"]
                                 and i4["passes"] and i5["passes"])

    # --- L20 self-test ---
    l20 = l20_self_test(pv)
    tee(f"[L20] no_drift_corr={l20['no_drift_corr']} no_drift_passes={l20['no_drift_passes']}")
    tee(f"[L20] pert1({l20['perturbation_1']})_corr={l20['perturbation_1_corr']:.4f} "
        f"(<{L20_SELFTEST_THRESHOLD}: {l20['perturbation_1_corr'] < L20_SELFTEST_THRESHOLD})")
    tee(f"[L20] pert2({l20['perturbation_2']})_corr={l20['perturbation_2_corr']:.4f} "
        f"(<{L20_SELFTEST_THRESHOLD}: {l20['perturbation_2_corr'] < L20_SELFTEST_THRESHOLD})")
    tee(f"[L20] both_perturbations_flag_drift={l20['both_perturbations_flag_drift']}")

    t_end = time.perf_counter()
    wall = t_end - t_start

    # --- build results JSON ---
    run_id = "m1-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    config = {
        "n_items": N_ITEMS,
        "n_relevant": N_RELEVANT,
        "n_cycles": N_CYCLES,
        "k": K,
        "base_rate": BASE_RATE,
        "seeds": list(seeds),
        "metrics": list(METRIC_ORDER),
        "arms": list(ARM_ORDER),
    }
    # round floats for readability but keep precision
    def round_metrics(d):
        return {m: float(d[m]) for m in METRIC_ORDER}

    results_obj = {
        "run_id": run_id,
        "schema_version": SCHEMA_VERSION,
        "config": config,
        "results": {
            str(s): {arm: round_metrics(results_run1[str(s)][arm]) for arm in ARM_ORDER}
            for s in seeds
        },
        "profile_mean_over_seeds": {
            arm: {m: float(profile_mean[arm][m]) for m in METRIC_ORDER}
            for arm in ARM_ORDER
        },
        "discrimination": {
            m: i4["per_metric"][m] for m in METRIC_ORDER
        },
    }

    invariants_obj = {
        "invariant_suite_green": invariant_suite_green,
        "invariants": {
            "I1_reproducibility": i1,
            "I2_oracle_ceiling": i2,
            "I3_contamination_floor": i3,
            "I4_discrimination_bar": i4,
            "I5_frozen_ordering": i5,
        },
    }

    # --- RUN-2 hygiene: self-detecting deviations_logged ---
    # The harness cannot know about external deviation files (e.g.
    # run1_deviations.txt) at runtime, so instead it self-detects the most
    # common deviation: a Python runtime whose major.minor does not match the
    # pinned 3.11.x. If it differs, deviations_logged is populated with a
    # one-line note (rather than being empty), making the deviation
    # self-documenting in the manifest itself.
    PINNED_PY_MAJOR_MINOR = "3.11"
    runtime_py_version = platform.python_version()
    runtime_major_minor = ".".join(platform.python_version_tuple()[:2])
    deviations_logged = []
    if runtime_major_minor != PINNED_PY_MAJOR_MINOR:
        deviations_logged.append(
            f"Python runtime {runtime_py_version} differs from pinned "
            f"{PINNED_PY_MAJOR_MINOR}.x"
        )
    if deviations_logged:
        tee(f"[manifest] deviations_logged (self-detected): {deviations_logged}")

    manifest_obj = {
        "command": "python m1_harness.py --seeds 42,43,44 --output-dir ./m1_output",
        "commit_hash": get_commit_hash(),
        "purpose": "M1 harness: validate L18 control battery discriminates oracle from naive by >= 0.30 on every metric, 3 seeds.",
        "bar": "oracle >= naive + 0.30 on every metric; invariant suite green (I1-I5).",
        "seeds": list(seeds),
        "wall_clock_seconds": float(wall),
        "deps": {
            "python": "3.11.x (exact version recorded at runtime via python --version)",
            "numpy": "1.26.4",
            "scipy": "1.13.1",
        },
        "python_version_runtime": get_python_version(),
        "output_files": ["m1_run_results.json", "m1_invariants.json",
                         "m1_manifest.json", "m1_run.log", "m1_profile.json"],
        "deviations_logged": deviations_logged,
    }

    profile_obj = {
        "profile_version": PROFILE_VERSION,
        "profile_vector": pv,
        "arm_order": list(ARM_ORDER),
        "metric_order": list(METRIC_ORDER),
        "drift_criterion": (
            f"pearson_corr(profile_vector, new_profile_vector) < {L20_DRIFT_CRITERION} "
            f"=> drifted (locked bar); self-test threshold < {L20_SELFTEST_THRESHOLD} "
            f"(stricter, for margin)"
        ),
        "l20_self_test": l20,
    }

    # --- write files ---
    write_json(os.path.join(output_dir, "m1_run_results.json"), results_obj)
    write_json(os.path.join(output_dir, "m1_invariants.json"), invariants_obj)
    write_json(os.path.join(output_dir, "m1_manifest.json"), manifest_obj)
    write_json(os.path.join(output_dir, "m1_profile.json"), profile_obj)

    tee("-" * 72)
    tee(f"invariant_suite_green = {invariant_suite_green}")
    tee(f"wall_clock_seconds = {wall:.4f}")
    tee(f"python_version_runtime = {get_python_version()}")
    tee("Output files written:")
    for fn in ["m1_run_results.json", "m1_invariants.json", "m1_manifest.json",
               "m1_run.log", "m1_profile.json"]:
        tee(f"  {os.path.join(output_dir, fn)}")
    tee("-" * 72)
    if not invariant_suite_green:
        tee("WARNING: invariant suite NOT green. See invariants above.")
    if not l20["both_perturbations_flag_drift"] or not l20["no_drift_passes"]:
        tee("WARNING: L20 self-test did NOT pass.")

    log_fh.close()

    # Re-open log to append the final summary line already printed (log was
    # being teed above, so it is already complete). Nothing more to do.
    return 0 if (invariant_suite_green and l20["both_perturbations_flag_drift"]
                 and l20["no_drift_passes"]) else 1


if __name__ == "__main__":
    sys.exit(main())
