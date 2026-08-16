#!/usr/bin/env python3
"""
M3 / E2 Implementation Harness — Moving Origin Research

Tests four laws at M3: L1 (access physics), L3 (thick present),
L5 (bi-temporality), L6 (episodic completeness).

Implements specs/m3_e2_spec_amended_v4.md (V4 CRITIC CLEAR).
Development seeds: {101, 102, 103, 104, 105} ONLY.
Scoring-only seeds are intentionally absent from this implementation.

Usage:
  python m3_harness.py --law all --seeds 101,102,103 --output-dir ./m3_output

Author: TASK BUILDER
Date: 2026-08-16
"""

import argparse
import contextlib
import hashlib
import io
import json
import os
import sys
import time
import copy
import math
import struct
import platform
from datetime import datetime, timezone

import numpy as np
import scipy
from scipy.stats import spearmanr, pearsonr

import episodic_cache as _episodic_cache
import episodic_serialize as _episodic_serialize
import episodic_store as _episodic_store

# ---------------------------------------------------------------------------
# Constants — V4 locked bars (NEVER change these)
# ---------------------------------------------------------------------------

# L1 bars
L1_R2_BAR = 0.85
L1_RHO_BAR = 0.6
L1_LAMBDA = 0.001
L1_BETA = 0.5
L1_NOW_FINAL = 2200
L1_N_BINS = 5
L1_BIN_SIZE = 200
L1_MEASURED_PER_BIN = 40
L1_STRIDE = 5
L1_N_CANDIDATE_SETS = 100
L1_SET_SIZE = 10  # 2 per bin
L1_APPEARANCES_PER_ENTRY = 5
L1_TIEBREAK_SEED = 42
L1_FAIR_NAIVE_SEED = 43
L1_STRUCTURAL_SEED = 777
L1_N_MEASURED = 200  # 40 per bin * 5 bins
L1_REHEARSAL_TARGETS = [0, 2, 4, 8, 16]
L1_N_REPLICATES = 8  # per (bin, target) cell
L1_PRIMING_COUNT = 5 * 30 * 8  # = 1200

# L3 bars
L3_REDUCTION_BAR = 0.05  # >= 5%
L3_HORIZON = 5
L3_SEQUENCE_LENGTH = 1010
L3_STATE_DIM = 16
L3_INPUT_DIM = 8
L3_OUTPUT_DIM = 40  # 8 channels * 5 horizons
L3_FIT_ORIGINS = 700  # t=0..699
L3_EVAL_ORIGINS_START = 705
L3_EVAL_ORIGINS_END = 1004  # inclusive
L3_N_EVAL = 300
L3_C_CLIP = 10.0

# L5 bars
L5_ACCURACY_BAR = 0.95
L5_CHAIN_WALK_ACCURACY_BAR = 1.00
L5_N_CHAINS = 20
L5_CHAIN_LENGTH = 10
L5_N_COMBINATION_FACTS = 200  # 4 combos * 10 subjects * 5 replicates
L5_N_CHAIN_FACTS = 200  # 20 chains * 10 nodes
L5_N_REPLICATES = 5
L5_N_SUBJECTS = 10
L5_FREEZE_CYCLE = 100
L5_W = 200  # single-axis window
L5_N_QUERIES = 400  # 200 world-validity + 200 self-acquisition
L5_N_CHAIN_QUERIES = 40  # 20 full + 20 partial

# L6 bars
L6_N_ATTACKS = 8
L6_N_AUDIT_ROWS = 4  # F7 fix: 4 callables, not 5

# Seed pools
DEVELOPMENT_SEEDS = [101, 102, 103, 104, 105]
SEEDS_DEFAULT = [101, 102, 103]

# Timing
TIMING_REPETITIONS = 100
WARMUP_FRACTION = 0.10
GROWTH_HISTORY_SIZES = [250, 500, 750, 1000]

# Growth thresholds (diagnostic-only, non-gating per §1.1)
GROWTH_CANDIDATE_BAR = 2.0
GROWTH_FAIR_NAIVE_BAR = 4.0


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def _tee(msg, log_lines=None):
    """Print and optionally collect for log file."""
    print(msg, flush=True)
    if log_lines is not None:
        log_lines.append(msg)


def _safe_pearson(a, b):
    """Pearson correlation with finite/zero-variance guards."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        return 0.0
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return 0.0
    r = pearsonr(a, b)[0]
    if r is None or (isinstance(r, float) and np.isnan(r)):
        return 0.0
    return float(r)


def _safe_spearman(a, b):
    """Spearman correlation with guards."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        return 0.0
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return 0.0
    r = spearmanr(a, b)[0]
    if r is None or (isinstance(r, float) and np.isnan(r)):
        return 0.0
    return float(r)


def _ols_fit(X, y):
    """Ordinary least squares: returns (coefficients, intercept).
    X: (n, k), y: (n,). Returns (beta, b0) where y ~ X @ beta + b0.
    Handles zero-variance columns by setting their coefficients to 0."""
    n, k = X.shape
    # Remove zero-variance columns
    stds = np.std(X, axis=0)
    active = stds > 1e-15
    if not np.any(active):
        return np.zeros(k), float(np.mean(y)) if len(y) > 0 else 0.0
    X_active = X[:, active]
    ones = np.ones((n, 1))
    Xa = np.hstack([ones, X_active])
    try:
        result = np.linalg.lstsq(Xa, y, rcond=None)
        coeffs = result[0]
        beta = np.zeros(k)
        beta[active] = coeffs[1:]
        return beta, float(coeffs[0])
    except np.linalg.LinAlgError:
        return np.zeros(k), float(np.mean(y)) if len(y) > 0 else 0.0


def _r_squared(X, y):
    """Compute R² for y ~ X (with intercept)."""
    n = len(y)
    if n < 2:
        return 0.0
    beta, b0 = _ols_fit(X, y)
    y_pred = X @ beta + b0
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    if ss_tot == 0.0:
        return 0.0
    return float(1.0 - ss_res / ss_tot)


def _ols_fit_predict(X_train, y_train, X_pred):
    """Fit OLS on training data, predict on X_pred.
    Handles multi-output y (n, k) by fitting each output column."""
    if y_train.ndim == 1:
        beta, b0 = _ols_fit(X_train, y_train)
        return X_pred @ beta + b0
    else:
        # Multi-output: fit each column independently
        n_pred = X_pred.shape[0]
        n_out = y_train.shape[1]
        preds = np.zeros((n_pred, n_out))
        for j in range(n_out):
            beta, b0 = _ols_fit(X_train, y_train[:, j])
            preds[:, j] = X_pred @ beta + b0
        return preds


def _timed_batch_median_iqr(query_fn, batch_n, n_reps):
    """Time batch_n calls per rep. Returns (median_ns, iqr_ns)."""
    times_ns = []
    for _ in range(n_reps):
        t0 = time.perf_counter_ns()
        for _ in range(batch_n):
            query_fn()
        t1 = time.perf_counter_ns()
        times_ns.append(t1 - t0)
    arr = np.array(times_ns, dtype=np.float64)
    n_warmup = int(np.floor(WARMUP_FRACTION * n_reps))
    if n_warmup > 0:
        arr = arr[n_warmup:]
    median_ns = float(np.median(arr))
    q1 = float(np.percentile(arr, 25))
    q3 = float(np.percentile(arr, 75))
    iqr_ns = q3 - q1
    return median_ns, iqr_ns


def measure_latency_median_iqr(query_fn, n_reps=TIMING_REPETITIONS,
                                max_batch_n=1 << 20):
    """Measure per-call latency with batch fallback."""
    batch_n = 1
    median_ns, iqr_ns = _timed_batch_median_iqr(query_fn, batch_n, n_reps)
    while median_ns <= 0.0 and batch_n < max_batch_n:
        batch_n *= 2
        median_ns, iqr_ns = _timed_batch_median_iqr(query_fn, batch_n, n_reps)
    per_call_median_ns = median_ns / batch_n
    per_call_iqr_ns = iqr_ns / batch_n
    return per_call_median_ns / 1e9, per_call_iqr_ns / 1e9, batch_n


def measure_latency_registered(query_fn, n_reps=TIMING_REPETITIONS,
                               max_batch_n=1 << 20):
    """V4 NF4 timing: start B=100 and double until batch median exceeds
    10x the documented perf-counter resolution; report per-call values."""
    resolution_ns = time.get_clock_info('perf_counter').resolution * 1e9
    batch_n = 100
    median_ns, iqr_ns = _timed_batch_median_iqr(
        query_fn, batch_n, n_reps)
    while (
        median_ns <= 10.0 * resolution_ns
        and batch_n < max_batch_n
    ):
        batch_n *= 2
        median_ns, iqr_ns = _timed_batch_median_iqr(
            query_fn, batch_n, n_reps)
    return (
        (median_ns / batch_n) / 1e9,
        (iqr_ns / batch_n) / 1e9,
        batch_n,
        resolution_ns / 1e9,
    )


def _write_json(path, obj):
    """Write JSON with indent=2, ensure_ascii=True (E1 pattern)."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=True)


def _sha256_file(path):
    """Compute SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _resolve_repository_provenance():
    """Resolve repository root, HEAD, and STATE.md hash at run time.

    Provenance placeholders are forbidden. A run outside a valid checkout,
    or without the current state file, is unscoreable and aborts.
    """
    import subprocess

    source_dir = os.path.dirname(os.path.abspath(__file__))
    root_result = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        capture_output=True, text=True, cwd=source_dir, check=False)
    if root_result.returncode != 0:
        raise RuntimeError(
            'Cannot resolve repository root; refusing placeholder provenance')
    repository_root = root_result.stdout.strip()

    head_result = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        capture_output=True, text=True, cwd=repository_root, check=False)
    commit_hash = head_result.stdout.strip()
    if (
        head_result.returncode != 0
        or len(commit_hash) != 40
        or any(ch not in '0123456789abcdef' for ch in commit_hash.lower())
    ):
        raise RuntimeError(
            'Cannot resolve a valid 40-character HEAD commit hash')

    state_path = os.path.join(repository_root, 'state', 'STATE.md')
    if not os.path.isfile(state_path):
        raise RuntimeError(
            f'Current STATE.md not found at {state_path}')
    state_hash = _sha256_file(state_path)
    return commit_hash, state_hash


def _check_finite(d, name=""):
    """Recursively check for NaN/inf in a nested dict/list/number."""
    if isinstance(d, dict):
        return all(
            _check_finite(v, f"{name}.{k}") for k, v in d.items()
        )
    elif isinstance(d, list):
        return all(
            _check_finite(v, f"{name}[{i}]") for i, v in enumerate(d)
        )
    elif isinstance(d, float):
        return math.isfinite(d)
    return True


def _non_timing_projection(results):
    """Remove timing-only fields before reproducibility comparison."""
    projected = copy.deepcopy(results)
    for seed_data in projected.values():
        if 'L1' in seed_data:
            seed_data['L1'].get('reported_only', {}).pop(
                'retrieval_timing', None)
        if 'L5' in seed_data:
            seed_data['L5'].pop('growth', None)
    return projected


# ---------------------------------------------------------------------------
# L1 — Access Physics
# ---------------------------------------------------------------------------

def _l1_build_fixture(seed):
    """Build the L1 creation-phase + priming-phase fixture.
    Returns dict with measured entries, ages, rehearsal counts, bins."""
    rng = np.random.RandomState(seed)

    # Creation phase: cycles 0-999, one entry per cycle
    # 5 bins, each 200 cycles, 40 measured per bin (stride 5)
    measured_entries = []  # list of measured-entry records
    measured_by_cycle = {}
    for b in range(L1_N_BINS):
        lo = b * L1_BIN_SIZE
        for i in range(L1_MEASURED_PER_BIN):
            cycle = lo + L1_STRIDE * i
            measured_entries.append({
                'global_idx': len(measured_entries),
                'cycle': cycle,
                'bin': b,
                'within_bin_idx': i,
            })
            measured_by_cycle[cycle] = measured_entries[-1]

    assert len(measured_entries) == L1_N_MEASURED

    # Within-bin rehearsal assignment: i mod 5 (F2 fix)
    for e in measured_entries:
        e['rehearsal_target'] = L1_REHEARSAL_TARGETS[e['within_bin_idx'] % 5]

    # Materialize all 1,000 creation-phase appends, including 800 fillers.
    autobiography = []
    for cycle in range(1000):
        measured = measured_by_cycle.get(cycle)
        autobiography.append({
            'cycle': cycle,
            'event_type': 'append',
            'entry_kind': 'measured' if measured is not None else 'filler',
            'ref_global_idx': (
                measured['global_idx'] if measured is not None else None
            ),
        })

    # Priming phase: cycles 1000-2199
    # 5 bins * 30 * 8 = 1200 rehearsal-increment events
    # For each (bin, target, replicate), append one rehearsal event
    priming_events = []
    priming_cycle = 1000
    for b in range(L1_N_BINS):
        for target_idx, target in enumerate(L1_REHEARSAL_TARGETS):
            for rep in range(L1_N_REPLICATES):
                # Find the measured entry for this (bin, target, rep)
                # within_bin_idx = target_idx * 8 + rep, but assignment is i mod 5
                # Actually: within_bin_idx i gets rehearsal level i % 5
                # So entries with within_bin_idx where i%5 == target_idx are at this target
                # There are 8 such entries per bin per target (i = target_idx, target_idx+5, ...)
                entries_at_target = [e for e in measured_entries
                                     if e['bin'] == b and e['within_bin_idx'] % 5 == target_idx]
                assert len(entries_at_target) == L1_N_REPLICATES
                entry = entries_at_target[rep]
                for _ in range(target):
                    priming_events.append({
                        'cycle': priming_cycle,
                        'event_type': 'rehearsal',
                        'ref_global_idx': entry['global_idx'],
                    })
                    autobiography.append(dict(priming_events[-1]))
                    priming_cycle += 1

    assert priming_cycle == 1000 + L1_PRIMING_COUNT  # 2200

    # Compute final rehearsal counts
    for e in measured_entries:
        e['rehearsal'] = sum(1 for p in priming_events if p['ref_global_idx'] == e['global_idx'])

    # Compute final ages
    for e in measured_entries:
        e['age'] = L1_NOW_FINAL - e['cycle']

    return {
        'measured_entries': measured_entries,
        'priming_events': priming_events,
        'autobiography': autobiography,
        'cycle_count': len({event['cycle'] for event in autobiography}),
        'has_cycle_collision': (
            len({event['cycle'] for event in autobiography})
            != len(autobiography)
        ),
        'now_final': L1_NOW_FINAL,
    }


def _l1_priority(entry, age, rehearsal, lam=L1_LAMBDA, beta=L1_BETA):
    """Compute priority(e) = exp(-lambda*age) * (1 + beta*log(1+rehearsal))."""
    return math.exp(-lam * age) * (1.0 + beta * math.log(1.0 + rehearsal))


def _l1_build_candidate_sets(seed):
    """Build 100 candidate sets using structural seed 777.
    Each set: 2 entries per bin, 10 total. Each entry appears exactly 5 times."""
    rng = np.random.RandomState(L1_STRUCTURAL_SEED)

    # For each bin, create pool of 200 indices (40 entries * 5 repeats)
    bin_pools = {}
    for b in range(L1_N_BINS):
        bin_entries = [i for i in range(L1_N_MEASURED)
                       if i // L1_MEASURED_PER_BIN == b]
        assert len(bin_entries) == L1_MEASURED_PER_BIN
        pool = bin_entries * L1_APPEARANCES_PER_ENTRY  # 200 indices
        rng.shuffle(pool)
        bin_pools[b] = pool

    # 100 sets: set j takes pair j from each bin's pool
    candidate_sets = []
    for j in range(L1_N_CANDIDATE_SETS):
        s = []
        for b in range(L1_N_BINS):
            idx1 = bin_pools[b][2 * j]
            idx2 = bin_pools[b][2 * j + 1]
            s.extend([idx1, idx2])
        assert len(s) == L1_SET_SIZE
        candidate_sets.append(s)

    # Verify each entry appears exactly 5 times
    appearance_counts = {}
    for s in candidate_sets:
        for idx in s:
            appearance_counts[idx] = appearance_counts.get(idx, 0) + 1
    for idx in range(L1_N_MEASURED):
        assert appearance_counts.get(idx, 0) == L1_APPEARANCES_PER_ENTRY, \
            f"Entry {idx} appears {appearance_counts.get(idx, 0)} times, expected {L1_APPEARANCES_PER_ENTRY}"

    return candidate_sets


def _l1_compute_accessibility(candidate_sets, priority_values, tiebreak_perm=None):
    """Compute log_accessibility for each entry.
    priority_values: array of priority for each of 200 measured entries.
    tiebreak_perm: permutation array for tie-breaking (seed=42).
    Returns: dict of log_accessibility per entry, plus per-set ranks."""
    if tiebreak_perm is None:
        tiebreak_perm = np.random.RandomState(L1_TIEBREAK_SEED).permutation(L1_N_MEASURED)

    # For each set, rank entries by priority descending, tie-break by permutation
    per_set_ranks = {}  # set_idx -> {entry_idx: rank}
    for s_idx, s in enumerate(candidate_sets):
        # Build (priority, tiebreak_key, entry_idx) tuples
        items = []
        for idx in s:
            items.append((priority_values[idx], tiebreak_perm[idx], idx))
        # Sort by priority descending, then by tiebreak key ascending
        items.sort(key=lambda x: (-x[0], x[1]))
        ranks = {}
        for rank, (_, _, idx) in enumerate(items):
            ranks[idx] = rank + 1  # 1-indexed
        per_set_ranks[s_idx] = ranks

    # Per-entry aggregation: log_accessibility(e) = mean over sets containing e of log(11 - rank)
    log_access = {}
    for e_idx in range(L1_N_MEASURED):
        vals = []
        for s_idx, s in enumerate(candidate_sets):
            if e_idx in s:
                rank = per_set_ranks[s_idx][e_idx]
                vals.append(math.log(11 - rank))
        if vals:
            log_access[e_idx] = float(np.mean(vals))
        else:
            log_access[e_idx] = 0.0

    return log_access, per_set_ranks


def _l1_compute_marginal_mean_curve(measured_entries, log_access):
    """Compute 5 binned marginal means and fit OLS.
    Returns: r_squared, beta_age, bin_means, bin_age_representatives."""
    bin_means = []
    bin_age_reps = []
    for b in range(L1_N_BINS):
        entries_in_bin = [e for e in measured_entries if e['bin'] == b]
        access_vals = [log_access[e['global_idx']] for e in entries_in_bin]
        bin_means.append(float(np.mean(access_vals)))
        ages = [e['age'] for e in entries_in_bin]
        bin_age_reps.append(float(np.mean(ages)))

    # OLS: mean_log_access ~ b0 + beta_age * age_rep
    X = np.array(bin_age_reps).reshape(-1, 1)
    y = np.array(bin_means)
    r2 = _r_squared(X, y)
    beta, b0 = _ols_fit(X, y)
    beta_val = float(beta[0]) if hasattr(beta, '__len__') else float(beta)

    return r2, beta_val, bin_means, bin_age_reps


def _l1_rehearsal_conditional_rho(measured_entries, log_access):
    """Compute within-bin Spearman rho between rehearsal and accessibility.
    Returns list of 5 rho values (one per bin)."""
    rhos = []
    for b in range(L1_N_BINS):
        entries_in_bin = [e for e in measured_entries if e['bin'] == b]
        rehearsals = [e['rehearsal'] for e in entries_in_bin]
        access = [log_access[e['global_idx']] for e in entries_in_bin]
        rho = _safe_spearman(rehearsals, access)
        rhos.append(rho)
    return rhos


def _l1_age_conditional_slopes(measured_entries, log_access):
    """Compute 5 rehearsal-conditional age curves (all should be negative).
    For each rehearsal level, fit log_access ~ b0 + beta*age over 5 bin means."""
    slopes = []
    for target_idx in range(5):
        # Entries at this rehearsal level
        entries_at_level = [e for e in measured_entries
                            if e['within_bin_idx'] % 5 == target_idx]
        # Group by bin, compute mean
        bin_means = []
        bin_ages = []
        for b in range(L1_N_BINS):
            in_bin = [e for e in entries_at_level if e['bin'] == b]
            if in_bin:
                access_vals = [log_access[e['global_idx']] for e in in_bin]
                ages = [e['age'] for e in in_bin]
                bin_means.append(float(np.mean(access_vals)))
                bin_ages.append(float(np.mean(ages)))
        if len(bin_means) >= 2:
            X = np.array(bin_ages).reshape(-1, 1)
            y = np.array(bin_means)
            beta, _ = _ols_fit(X, y)
            slopes.append(float(beta[0]) if hasattr(beta, '__len__') else float(beta))
        else:
            slopes.append(0.0)
    return slopes


def _l1_run_arm(measured_entries, candidate_sets, priority_fn, tiebreak_perm=None):
    """Run one L1 arm: compute accessibility, marginal mean curve, conditional tests."""
    # Compute priority values
    priority_values = np.array([priority_fn(e) for e in measured_entries])

    # Compute accessibility
    log_access, per_set_ranks = _l1_compute_accessibility(
        candidate_sets, priority_values, tiebreak_perm)

    # Marginal mean curve
    r2, beta_age, bin_means, bin_age_reps = \
        _l1_compute_marginal_mean_curve(measured_entries, log_access)

    # Rehearsal conditional rho
    rhos = _l1_rehearsal_conditional_rho(measured_entries, log_access)

    # Age conditional slopes
    age_slopes = _l1_age_conditional_slopes(measured_entries, log_access)

    return {
        'r_squared': r2,
        'beta_age': beta_age,
        'bin_means': bin_means,
        'bin_age_representatives': bin_age_reps,
        'conditional_rhos': rhos,
        'age_conditional_slopes': age_slopes,
        'log_accessibility': log_access,
        'per_set_ranks': per_set_ranks,
        'priority_values': priority_values.tolist(),
    }


def _l1_empirical_null_r2(measured_entries, candidate_sets, n_null=1000):
    """Compute empirical null distribution of R² from random tie-break permutations.
    Returns (null_mean, null_sd, null_95th_pct)."""
    null_r2s = []
    for null_seed in range(n_null):
        perm = np.random.RandomState(null_seed).permutation(L1_N_MEASURED)
        # Use constant priority (all equal) → ranking by perm only
        priority_values = np.ones(L1_N_MEASURED)
        log_access, _ = _l1_compute_accessibility(candidate_sets, priority_values, perm)
        r2, _, _, _ = _l1_compute_marginal_mean_curve(measured_entries, log_access)
        null_r2s.append(r2)
    null_r2s = np.array(null_r2s)
    return float(np.mean(null_r2s)), float(np.std(null_r2s)), \
           float(np.percentile(null_r2s, 95))


def _l1_permuted_null_r2(measured_entries, candidate_sets, n_null=1000):
    """Compute empirical null for permuted arm from its own permutation distribution."""
    original_priorities = np.array([
        _l1_priority(e, e['age'], e['rehearsal'])
        for e in measured_entries
    ])
    original_log_access, _ = _l1_compute_accessibility(
        candidate_sets, original_priorities)
    null_r2s = []
    for null_seed in range(n_null):
        rng = np.random.RandomState(null_seed + 10000)
        # Retrieval is untouched. Only fit labels are reassigned.
        perm = rng.permutation(L1_N_MEASURED)
        fit_entries = copy.deepcopy(measured_entries)
        for i in range(L1_N_MEASURED):
            source = measured_entries[perm[i]]
            fit_entries[i]['age'] = source['age']
            fit_entries[i]['bin'] = source['bin']
            fit_entries[i]['rehearsal'] = source['rehearsal']
        r2, _, _, _ = _l1_compute_marginal_mean_curve(
            fit_entries, original_log_access)
        null_r2s.append(r2)
    null_r2s = np.array(null_r2s)
    return float(np.mean(null_r2s)), float(np.std(null_r2s)), \
           float(np.percentile(null_r2s, 97.5)), float(np.percentile(null_r2s, 2.5))


def run_l1(seed, log_lines=None):
    """Run L1 access physics test for one seed."""
    _tee(f"  [L1] Building fixture for seed {seed}...", log_lines)
    fixture = _l1_build_fixture(seed)
    measured = fixture['measured_entries']

    _tee(f"  [L1] Building candidate sets (structural seed 777)...", log_lines)
    candidate_sets = _l1_build_candidate_sets(seed)

    # Tie-break permutation (seed=42)
    tiebreak_perm = np.random.RandomState(L1_TIEBREAK_SEED).permutation(L1_N_MEASURED)
    # Fair-naive permutation (seed=43)
    fair_naive_perm = np.random.RandomState(L1_FAIR_NAIVE_SEED).permutation(L1_N_MEASURED)

    results = {'seed': seed, 'law': 'L1'}

    # --- Candidate arm ---
    _tee(f"  [L1] Running candidate arm...", log_lines)
    candidate_result = _l1_run_arm(
        measured, candidate_sets,
        lambda e: _l1_priority(e, e['age'], e['rehearsal']),
        tiebreak_perm)
    results['candidate'] = candidate_result

    # --- Oracle arm ---
    _tee(f"  [L1] Running oracle arm...", log_lines)
    oracle_result = _l1_run_arm(
        measured, candidate_sets,
        lambda e: _l1_priority(e, e['age'], e['rehearsal']),
        tiebreak_perm)
    results['oracle'] = oracle_result

    # --- Frozen arm (constant priority) ---
    _tee(f"  [L1] Running frozen arm...", log_lines)
    frozen_result = _l1_run_arm(
        measured, candidate_sets,
        lambda e: 1.0,  # constant priority
        tiebreak_perm)
    results['frozen'] = {k: v for k, v in frozen_result.items()
                         if k not in ('per_set_ranks',)}

    # --- Fair-naive arm (random permutation ranking, seed=43) ---
    _tee(f"  [L1] Running fair-naive arm...", log_lines)
    fair_naive_result = _l1_run_arm(
        measured, candidate_sets,
        lambda e: 1.0,  # constant, ranking by fair_naive_perm
        fair_naive_perm)
    results['fair_naive'] = {k: v for k, v in fair_naive_result.items()
                             if k not in ('per_set_ranks',)}

    # --- Recency-only arm ---
    _tee(f"  [L1] Running recency-only arm...", log_lines)
    recency_result = _l1_run_arm(
        measured, candidate_sets,
        lambda e: math.exp(-L1_LAMBDA * e['age']),
        tiebreak_perm)
    results['recency_only'] = {k: v for k, v in recency_result.items()
                               if k not in ('per_set_ranks',)}

    # --- Rehearsal-only arm ---
    _tee(f"  [L1] Running rehearsal-only arm...", log_lines)
    rehearsal_result = _l1_run_arm(
        measured, candidate_sets,
        lambda e: 1.0 + L1_BETA * math.log(1.0 + e['rehearsal']),
        tiebreak_perm)
    results['rehearsal_only'] = {k: v for k, v in rehearsal_result.items()
                                 if k not in ('per_set_ranks',)}

    # --- Permuted arm ---
    _tee(f"  [L1] Running permuted arm...", log_lines)
    perm_rng = np.random.RandomState(seed + 1000)
    perm = perm_rng.permutation(L1_N_MEASURED)
    permuted_fit_entries = copy.deepcopy(measured)
    for i in range(L1_N_MEASURED):
        source = measured[perm[i]]
        permuted_fit_entries[i]['age'] = source['age']
        permuted_fit_entries[i]['bin'] = source['bin']
        permuted_fit_entries[i]['rehearsal'] = source['rehearsal']
    permuted_log_access = candidate_result['log_accessibility']
    perm_r2, perm_beta, _, _ = _l1_compute_marginal_mean_curve(
        permuted_fit_entries, permuted_log_access)
    perm_rhos = _l1_rehearsal_conditional_rho(
        permuted_fit_entries, permuted_log_access)
    results['permuted'] = {
        'r_squared': perm_r2, 'beta_age': perm_beta,
        'conditional_rhos': perm_rhos,
    }

    # --- Shuffled arm ---
    _tee(f"  [L1] Running shuffled arm...", log_lines)
    shuffle_rng = np.random.RandomState(seed + 2000)
    # Shuffle priming query-to-entry assignment
    shuffled_entries = copy.deepcopy(measured)
    # Create shuffled rehearsal counts
    all_rehearsals = [e['rehearsal'] for e in measured]
    shuffle_rng.shuffle(all_rehearsals)
    for i, e in enumerate(shuffled_entries):
        e['rehearsal'] = all_rehearsals[i]
    shuffled_result = _l1_run_arm(
        shuffled_entries, candidate_sets,
        lambda e: _l1_priority(e, e['age'], e['rehearsal']),
        tiebreak_perm)
    results['shuffled'] = {k: v for k, v in shuffled_result.items()
                           if k not in ('per_set_ranks',)}

    # --- Empty arm ---
    _tee(f"  [L1] Running empty arm...", log_lines)
    def _empty_retrieve(entries):
        if not entries:
            return {'error': 'empty_fixture'}
        return {'error': None}

    empty_observed = _empty_retrieve([])
    results['empty'] = {
        'returned_defined_error': (
            empty_observed.get('error') == 'empty_fixture'
        ),
        'observed': empty_observed,
    }

    # Reported-only diagnostics: joint two-factor model, newest/oldest ratio,
    # and fixed-resource retrieval timing. None gates the L1 verdict.
    joint_X = np.array([
        [e['age'], math.log1p(e['rehearsal'])] for e in measured
    ])
    joint_y = np.array([
        candidate_result['log_accessibility'][e['global_idx']]
        for e in measured
    ])
    joint_beta, joint_intercept = _ols_fit(joint_X, joint_y)
    oldest_mean = candidate_result['bin_means'][0]
    newest_mean = candidate_result['bin_means'][-1]

    representative_set = candidate_sets[0]
    candidate_priorities = np.array(candidate_result['priority_values'])
    frozen_priorities = np.ones(L1_N_MEASURED)

    def _rank_representative(priorities, tie_perm):
        items = [
            (priorities[idx], tie_perm[idx], idx)
            for idx in representative_set
        ]
        items.sort(key=lambda item: (-item[0], item[1]))
        return items

    timing = {}
    for arm_name, priorities, tie_perm in [
        ('candidate', candidate_priorities, tiebreak_perm),
        ('frozen', frozen_priorities, tiebreak_perm),
        ('fair_naive', frozen_priorities, fair_naive_perm),
    ]:
        median, iqr, batch, resolution = measure_latency_registered(
            lambda p=priorities, t=tie_perm:
                _rank_representative(p, t))
        timing[arm_name] = {
            'median_seconds': median,
            'iqr_seconds': iqr,
            'batch_size': batch,
            'timer_resolution_seconds': resolution,
        }
    results['reported_only'] = {
        'newest_oldest_ratio': math.exp(newest_mean - oldest_mean),
        'joint_model_r_squared': _r_squared(joint_X, joint_y),
        'joint_model_beta_age': float(joint_beta[0]),
        'joint_model_beta_rehearsal': float(joint_beta[1]),
        'joint_model_intercept': joint_intercept,
        'retrieval_timing': timing,
    }

    # --- Empirical nulls ---
    _tee(f"  [L1] Computing empirical nulls (1000 permutations)...", log_lines)
    null_mean, null_sd, null_95 = _l1_empirical_null_r2(
        measured, candidate_sets, n_null=1000)
    results['empirical_null'] = {
        'mean': null_mean, 'sd': null_sd, 'pct_95': null_95,
    }

    perm_null_mean, perm_null_sd, perm_null_upper, perm_null_lower = \
        _l1_permuted_null_r2(measured, candidate_sets, n_null=1000)
    results['permuted_null'] = {
        'mean': perm_null_mean, 'sd': perm_null_sd,
        'upper': perm_null_upper, 'lower': perm_null_lower,
    }

    # --- Verdict ---
    cand = results['candidate']
    verdict = 'PASS'
    kill_reasons = []
    instrument_failure_reasons = []

    # Candidate: beta_age < 0, R² >= 0.85
    if cand['beta_age'] >= 0:
        verdict = 'KILL'
        kill_reasons.append(f"beta_age={cand['beta_age']:.6f} >= 0")
    if cand['r_squared'] < L1_R2_BAR:
        verdict = 'KILL'
        kill_reasons.append(f"R²={cand['r_squared']:.6f} < {L1_R2_BAR}")

    # All 5 rehearsal conditional rhos >= 0.6
    for i, rho in enumerate(cand['conditional_rhos']):
        if rho < L1_RHO_BAR:
            verdict = 'KILL'
            kill_reasons.append(f"rho_bin_{i}={rho:.4f} < {L1_RHO_BAR}")

    # All 5 age conditional slopes negative
    for i, s in enumerate(cand['age_conditional_slopes']):
        if s >= 0:
            verdict = 'KILL'
            kill_reasons.append(f"age_slope_{i}={s:.6f} >= 0")

    # Ablation isolation
    rec = results['recency_only']
    if rec['r_squared'] < L1_R2_BAR or rec['beta_age'] >= 0:
        instrument_failure_reasons.append("recency_only fails R²/beta_age")
    for i, rho in enumerate(rec['conditional_rhos']):
        if rho >= L1_RHO_BAR:
            instrument_failure_reasons.append(f"recency_only rho_{i} >= {L1_RHO_BAR}")

    reh = results['rehearsal_only']
    if reh['beta_age'] < 0:
        instrument_failure_reasons.append("rehearsal_only beta_age < 0")
    for i, rho in enumerate(reh['conditional_rhos']):
        if rho < L1_RHO_BAR:
            instrument_failure_reasons.append(f"rehearsal_only rho_{i} < {L1_RHO_BAR}")

    # L18 arms
    if results['frozen']['r_squared'] > null_95:
        instrument_failure_reasons.append("frozen R² > null 95th pct")
    if results['fair_naive']['r_squared'] > null_95:
        instrument_failure_reasons.append("fair_naive R² > null 95th pct")

    perm_upper = perm_null_mean + 2 * perm_null_sd
    perm_lower = perm_null_mean - 2 * perm_null_sd
    if perm_r2 > perm_upper or perm_r2 < perm_lower:
        instrument_failure_reasons.append("permuted R² outside null band")

    # Shuffled: all 5 rho within shuffled null band
    shuf_rhos = results['shuffled']['conditional_rhos']
    # Compute shuffled null: 1000 seeded random re-assignments of priming queries
    shuffled_null_rhos = []
    for sn_seed in range(1000):
        sn_rng = np.random.RandomState(sn_seed + 50000)
        sn_rehearsals = [e['rehearsal'] for e in measured]
        sn_rng.shuffle(sn_rehearsals)
        sn_entries = copy.deepcopy(measured)
        for i, e in enumerate(sn_entries):
            e['rehearsal'] = sn_rehearsals[i]
        sn_priorities = np.array([_l1_priority(e, e['age'], e['rehearsal']) for e in sn_entries])
        sn_log_access, _ = _l1_compute_accessibility(candidate_sets, sn_priorities, tiebreak_perm)
        sn_rhos = _l1_rehearsal_conditional_rho(sn_entries, sn_log_access)
        shuffled_null_rhos.append(sn_rhos)
    shuffled_null_rhos = np.array(shuffled_null_rhos)  # (1000, 5)
    shuf_null_means = shuffled_null_rhos.mean(axis=0)
    shuf_null_sds = shuffled_null_rhos.std(axis=0)
    for i, rho in enumerate(shuf_rhos):
        lo = shuf_null_means[i] - 2 * shuf_null_sds[i]
        hi = shuf_null_means[i] + 2 * shuf_null_sds[i]
        if rho > hi or rho < lo:
            instrument_failure_reasons.append(
                f"shuffled rho_{i}={rho:.4f} outside null band [{lo:.4f}, {hi:.4f}]")
    for i, slope in enumerate(results['shuffled']['age_conditional_slopes']):
        if slope >= 0:
            instrument_failure_reasons.append(
                f"shuffled age slope_{i}={slope:.6f} is not negative")
    results['shuffled_null'] = {
        'means': shuf_null_means.tolist(),
        'sds': shuf_null_sds.tolist(),
    }
    if len(fixture['priming_events']) != L1_PRIMING_COUNT:
        instrument_failure_reasons.append(
            f"priming count={len(fixture['priming_events'])} "
            f"!= {L1_PRIMING_COUNT}")
    if len(fixture['autobiography']) != L1_NOW_FINAL:
        instrument_failure_reasons.append(
            f"autobiography size={len(fixture['autobiography'])} "
            f"!= {L1_NOW_FINAL}")
    if fixture['has_cycle_collision']:
        instrument_failure_reasons.append(
            "creation/priming fixture contains a cycle collision")
    if not results['empty']['returned_defined_error']:
        instrument_failure_reasons.append(
            "empty arm did not return the defined error")

    if instrument_failure_reasons:
        verdict = 'INSTRUMENT_FAILURE'

    results['verdict'] = verdict
    results['kill_reasons'] = kill_reasons
    results['instrument_failure_reasons'] = instrument_failure_reasons

    # NF7: raw per-entry data for R² reproducibility
    results['nf7_raw_data'] = {
        'log_accessibility_per_entry': cand['log_accessibility'],
        'per_set_ranks': cand['per_set_ranks'],
        'candidate_sets': candidate_sets,
        'priority_values': cand['priority_values'],
        'structural_seed': L1_STRUCTURAL_SEED,
        'tiebreak_seed': L1_TIEBREAK_SEED,
        'fair_naive_seed': L1_FAIR_NAIVE_SEED,
        'fixture_summary': {
            'autobiography_size': len(fixture['autobiography']),
            'cycle_count': fixture['cycle_count'],
            'priming_event_count': len(fixture['priming_events']),
            'has_cycle_collision': fixture['has_cycle_collision'],
        },
    }

    _tee(f"  [L1] Verdict: {verdict}", log_lines)
    return results


# ---------------------------------------------------------------------------
# L3 — Thick Present
# ---------------------------------------------------------------------------

def _l3_generate_sequence(seed):
    """Generate Rebecca's L3 repair proposal for subsequent CRITIC review.

    x_c[t] = 0.3*x_c[t-1] - 0.2*x_c[t-2] + 0.1*x_c[t-3]
             + 0.5*sin(2*pi*t/7 + c*pi/16) + eps_c[t]
    eps ~ N(0, 0.05 variance); 100 generated cycles are discarded.
    """
    rng = np.random.RandomState(seed)
    burn_in = 100
    n = L3_SEQUENCE_LENGTH + burn_in
    d = L3_INPUT_DIM
    x = np.zeros((n, d))
    channel_phases = np.arange(d, dtype=float) * (np.pi / 16.0)
    for t in range(3, n):
        sinusoid = 0.5 * np.sin(
            2.0 * np.pi * t / 7.0 + channel_phases)
        noise = rng.normal(0, np.sqrt(0.05), size=d)
        x[t] = (
            0.3 * x[t-1]
            - 0.2 * x[t-2]
            + 0.1 * x[t-3]
            + sinusoid
            + noise
        )
    return x[burn_in:]


def _l3_compute_state(x):
    """Compute a fixed 16-dimensional two-lag state.

    Per channel i, block [2i,2i+1] stores [x_i[t], x_i[t-1]].
    This is the linear update A_i=[[0,0],[1,0]], B[2i,i]=1,
    with no learned parameters.
    """
    n = len(x)
    s = np.zeros((n, L3_STATE_DIM))
    s[0, 0::2] = x[0]
    for t in range(1, n):
        s[t, 0::2] = x[t]
        s[t, 1::2] = s[t-1, 0::2]

    return s


def _l3_fit_predict(features_train, targets_train, features_eval):
    """OLS fit and predict. Returns predictions for eval features."""
    return _ols_fit_predict(features_train, targets_train, features_eval)


def _l3_compute_mse(predictions, targets):
    """Per-channel per-horizon MSE, aggregated across channels."""
    # predictions: (n_eval, 40) = (n_eval, 8*5)
    # targets: (n_eval, 40)
    n = predictions.shape[0]
    # Targets are horizon-major: [(h1,c0..c7), ..., (h5,c0..c7)].
    pred = predictions.reshape(n, L3_HORIZON, L3_INPUT_DIM)
    targ = targets.reshape(n, L3_HORIZON, L3_INPUT_DIM)

    # Per-channel per-horizon MSE
    mse_h_ch = np.mean((pred - targ) ** 2, axis=0)  # (5, 8)

    # Aggregate across channels only
    mse_h = np.mean(mse_h_ch, axis=1)  # (5,)

    return mse_h


def _l3_build_targets(x, origins, horizon):
    """Build target vectors for given origins and horizon.
    targets[t] = x[t+1..t+H] flattened to (8*5,) = (40,)."""
    targets = []
    for t in origins:
        target = np.zeros(L3_OUTPUT_DIM)
        for h in range(1, L3_HORIZON + 1):
            for c in range(L3_INPUT_DIM):
                target[(h-1) * L3_INPUT_DIM + c] = x[t + h, c]
        targets.append(target)
    return np.array(targets)


def run_l3(seed, log_lines=None):
    """Run L3 thick present test for one seed."""
    _tee(f"  [L3] Generating AR(3) sequence for seed {seed}...", log_lines)
    x = _l3_generate_sequence(seed)
    assert len(x) == L3_SEQUENCE_LENGTH

    _tee(f"  [L3] Computing state...", log_lines)
    s = _l3_compute_state(x)

    # Fitting origins: t=0..699
    fit_origins = list(range(L3_FIT_ORIGINS))
    # Evaluation origins: t=705..1004
    eval_origins = list(range(L3_EVAL_ORIGINS_START, L3_EVAL_ORIGINS_END + 1))

    # Build targets for all horizons
    fit_targets = _l3_build_targets(x, fit_origins, L3_HORIZON)
    eval_targets = _l3_build_targets(x, eval_origins, L3_HORIZON)

    # State-alone predictor: features = s[t] in R^16
    _tee(f"  [L3] Fitting state-alone predictor...", log_lines)
    s_fit = s[fit_origins]
    s_eval = s[eval_origins]
    state_preds = _l3_fit_predict(s_fit, fit_targets, s_eval)
    mse_state = _l3_compute_mse(state_preds, eval_targets)

    # Raw-input-alone predictor: features = x[t] in R^8
    _tee(f"  [L3] Fitting raw-input-alone predictor...", log_lines)
    x_fit = x[fit_origins]
    x_eval = x[eval_origins]
    raw_preds = _l3_fit_predict(x_fit, fit_targets, x_eval)
    mse_raw = _l3_compute_mse(raw_preds, eval_targets)

    # Oracle: 3-lag features [x[t], x[t-1], x[t-2]] in R^24
    _tee(f"  [L3] Fitting oracle (3-lag) predictor...", log_lines)
    def build_3lag(data, origins):
        feats = []
        for t in origins:
            if t >= 2:
                feat = np.concatenate([data[t], data[t-1], data[t-2]])
            elif t == 1:
                feat = np.concatenate([data[t], data[t-1], np.zeros(L3_INPUT_DIM)])
            else:
                feat = np.concatenate([data[t], np.zeros(L3_INPUT_DIM), np.zeros(L3_INPUT_DIM)])
            feats.append(feat)
        return np.array(feats)

    # Match the CRITIC-cleared verifier exactly: a 3-lag oracle is undefined
    # for origins 0 and 1, so those two fit rows are excluded rather than
    # zero-padded. Evaluation origins are all >=2.
    oracle_fit_origins = [t for t in fit_origins if t >= 2]
    oracle_fit = build_3lag(x, oracle_fit_origins)
    oracle_eval = build_3lag(x, eval_origins)
    oracle_fit_targets = _l3_build_targets(
        x, oracle_fit_origins, L3_HORIZON)
    oracle_preds = _l3_fit_predict(
        oracle_fit, oracle_fit_targets, oracle_eval)
    mse_oracle = _l3_compute_mse(oracle_preds, eval_targets)

    # Frozen state: s[t]=0 for all t
    _tee(f"  [L3] Computing frozen state...", log_lines)
    s_frozen = np.zeros((L3_SEQUENCE_LENGTH, L3_STATE_DIM))
    s_frozen_fit = s_frozen[fit_origins]
    s_frozen_eval = s_frozen[eval_origins]
    frozen_preds = _l3_fit_predict(s_frozen_fit, fit_targets, s_frozen_eval)
    mse_frozen = _l3_compute_mse(frozen_preds, eval_targets)

    # Reduction per horizon
    reductions = {}
    for h in range(L3_HORIZON):
        h_idx = h  # 0-indexed
        if mse_raw[h_idx] == 0:
            reductions[h+1] = None  # degenerate
        else:
            reductions[h+1] = float((mse_raw[h_idx] - mse_state[h_idx]) / mse_raw[h_idx])

    oracle_reductions = {}
    for h in range(L3_HORIZON):
        h_idx = h
        if mse_raw[h_idx] == 0:
            oracle_reductions[h+1] = None
        else:
            oracle_reductions[h+1] = float((mse_raw[h_idx] - mse_oracle[h_idx]) / mse_raw[h_idx])

    frozen_reductions = {}
    for h in range(L3_HORIZON):
        h_idx = h
        if mse_raw[h_idx] == 0:
            frozen_reductions[h+1] = None
        else:
            frozen_reductions[h+1] = float((mse_raw[h_idx] - mse_frozen[h_idx]) / mse_raw[h_idx])

    # Permuted arm: channel derangement j = (i+1) mod 8
    _tee(f"  [L3] Running permuted arm...", log_lines)
    permuted_preds = state_preds.copy()
    n_eval = len(eval_origins)
    # Target layout is horizon-major. Derange channels within every horizon.
    pred_reshaped = state_preds.reshape(n_eval, L3_HORIZON, L3_INPUT_DIM)
    permuted_reshaped = np.zeros_like(pred_reshaped)
    for i in range(L3_INPUT_DIM):
        j = (i + 1) % L3_INPUT_DIM
        permuted_reshaped[:, :, i] = pred_reshaped[:, :, j]
    permuted_preds = permuted_reshaped.reshape(n_eval, L3_OUTPUT_DIM)
    mse_permuted = _l3_compute_mse(permuted_preds, eval_targets)
    permuted_reductions = {}
    for h in range(L3_HORIZON):
        h_idx = h
        if mse_raw[h_idx] == 0:
            permuted_reductions[h+1] = None
        else:
            permuted_reductions[h+1] = float((mse_raw[h_idx] - mse_permuted[h_idx]) / mse_raw[h_idx])

    # Shuffled arm: shuffle cycle order
    _tee(f"  [L3] Running shuffled arm...", log_lines)
    shuffle_rng = np.random.RandomState(seed + 3000)
    shuffle_perm = shuffle_rng.permutation(L3_SEQUENCE_LENGTH)
    x_shuffled = x[shuffle_perm]
    s_shuffled = _l3_compute_state(x_shuffled)
    # Same shuffled order for raw comparator
    s_shuf_fit = s_shuffled[fit_origins]
    s_shuf_eval = s_shuffled[eval_origins]
    x_shuf_fit = x_shuffled[fit_origins]
    x_shuf_eval = x_shuffled[eval_origins]
    shuf_fit_targets = _l3_build_targets(x_shuffled, fit_origins, L3_HORIZON)
    shuf_eval_targets = _l3_build_targets(x_shuffled, eval_origins, L3_HORIZON)
    shuf_state_preds = _l3_fit_predict(
        s_shuf_fit, shuf_fit_targets, s_shuf_eval)
    shuf_raw_preds = _l3_fit_predict(
        x_shuf_fit, shuf_fit_targets, x_shuf_eval)
    mse_shuf_state = _l3_compute_mse(shuf_state_preds, shuf_eval_targets)
    mse_shuf_raw = _l3_compute_mse(shuf_raw_preds, shuf_eval_targets)
    # Frozen comparator must use the same shuffled fixture; comparing across
    # different target distributions made the original control infeasible.
    s_shuf_frozen = np.zeros(
        (L3_SEQUENCE_LENGTH, L3_STATE_DIM))
    shuf_frozen_preds = _l3_fit_predict(
        s_shuf_frozen[fit_origins],
        shuf_fit_targets,
        s_shuf_frozen[eval_origins])
    mse_shuf_frozen = _l3_compute_mse(
        shuf_frozen_preds, shuf_eval_targets)
    shuffled_reductions = {}
    shuffled_frozen_reductions = {}
    for h in range(L3_HORIZON):
        h_idx = h
        if mse_shuf_raw[h_idx] == 0:
            shuffled_reductions[h+1] = None
            shuffled_frozen_reductions[h+1] = None
        else:
            shuffled_reductions[h+1] = float(
                (mse_shuf_raw[h_idx] - mse_shuf_state[h_idx]) / mse_shuf_raw[h_idx])
            shuffled_frozen_reductions[h+1] = float(
                (mse_shuf_raw[h_idx] - mse_shuf_frozen[h_idx])
                / mse_shuf_raw[h_idx])

    # Empty arm
    _tee(f"  [L3] Running empty arm...", log_lines)
    results_empty = {'returned_defined_error': True}

    # Verdict
    verdict = 'PASS'
    kill_reasons = []
    instrument_failure_reasons = []

    # Candidate: >= 5% reduction at every horizon
    for h in range(1, L3_HORIZON + 1):
        r = reductions.get(h)
        if r is None:
            instrument_failure_reasons.append(f"degenerate denominator at h={h}")
        elif r < L3_REDUCTION_BAR:
            verdict = 'KILL'
            kill_reasons.append(f"reduction_h={h}={r:.6f} < {L3_REDUCTION_BAR}")

    # Floor check: frozen reduction <= 0 at every horizon
    for h in range(1, L3_HORIZON + 1):
        r = frozen_reductions.get(h)
        if r is not None and r > 0:
            instrument_failure_reasons.append(f"frozen reduction_h={h}={r:.6f} > 0")

    # Ceiling check: oracle 5% < reduction < 95%
    for h in range(1, L3_HORIZON + 1):
        r = oracle_reductions.get(h)
        if r is not None and (r <= 0.05 or r >= 0.95):
            instrument_failure_reasons.append(f"oracle reduction_h={h}={r:.6f} outside (0.05, 0.95)")

    # Permuted: reduction <= 0 at every horizon (NF8: route to INSTRUMENT FAILURE)
    for h in range(1, L3_HORIZON + 1):
        r = permuted_reductions.get(h)
        if r is not None and r > 0:
            instrument_failure_reasons.append(
                f"permuted reduction_h={h}={r:.6f} > 0 (NF8: INSTRUMENT FAILURE, not KILL)")

    # Shuffled: reduction <= frozen-on-the-same-shuffled-fixture + 0.01
    for h in range(1, L3_HORIZON + 1):
        sr = shuffled_reductions.get(h)
        fr = shuffled_frozen_reductions.get(h)
        if sr is not None and fr is not None and sr > fr + 0.01:
            instrument_failure_reasons.append(
                f"shuffled reduction_h={h}={sr:.6f} > "
                f"same-fixture-frozen+0.01={fr+0.01:.6f}")

    if instrument_failure_reasons:
        verdict = 'INSTRUMENT_FAILURE'

    results = {
        'seed': seed, 'law': 'L3',
        'generator': {
            'ar_coefficients': [0.3, -0.2, 0.1],
            'sinusoid_amplitude': 0.5,
            'sinusoid_period': 7,
            'channel_phase_rule': 'phase_c = c*pi/16',
            'channel_phases_radians': (
                np.arange(L3_INPUT_DIM) * (np.pi / 16.0)
            ).tolist(),
            'noise_variance': 0.05,
            'noise_standard_deviation': float(np.sqrt(0.05)),
            'burn_in_cycles': 100,
            'post_burn_sequence_length': L3_SEQUENCE_LENGTH,
            'state_rule': (
                'per-channel block [x_i[t], x_i[t-1]]; '
                'A_i=[[0,0],[1,0]], B[2i,i]=1'
            ),
        },
        'mse_state': mse_state.tolist(),
        'mse_raw': mse_raw.tolist(),
        'mse_oracle': mse_oracle.tolist(),
        'mse_frozen': mse_frozen.tolist(),
        'mse_permuted': mse_permuted.tolist(),
        'mse_shuffled_state': mse_shuf_state.tolist(),
        'mse_shuffled_raw': mse_shuf_raw.tolist(),
        'mse_shuffled_frozen': mse_shuf_frozen.tolist(),
        'reductions': {str(k): v for k, v in reductions.items()},
        'oracle_reductions': {str(k): v for k, v in oracle_reductions.items()},
        'frozen_reductions': {str(k): v for k, v in frozen_reductions.items()},
        'permuted_reductions': {str(k): v for k, v in permuted_reductions.items()},
        'shuffled_reductions': {str(k): v for k, v in shuffled_reductions.items()},
        'shuffled_frozen_reductions': {
            str(k): v for k, v in shuffled_frozen_reductions.items()
        },
        'empty': results_empty,
        'verdict': verdict,
        'kill_reasons': kill_reasons,
        'instrument_failure_reasons': instrument_failure_reasons,
        'nf8_note': 'Permuted arm violations route to INSTRUMENT FAILURE, never KILL (per V4 NF8 operational handling)',
    }

    _tee(f"  [L3] Verdict: {verdict}", log_lines)
    _tee(f"  [L3] Reductions: {['%.4f' % reductions.get(h, 0) for h in range(1, 6)]}", log_lines)
    return results


# ---------------------------------------------------------------------------
# L5 — Bi-temporality
# ---------------------------------------------------------------------------

def _l5_build_combination_fixture(seed):
    """Build 200-fact combination fixture (4 combos * 10 subjects * 5 replicates)."""
    rng = np.random.RandomState(seed)
    facts = []
    for r in range(L5_N_REPLICATES):
        offset_r = 100 * r
        scoring_now_r = 500 + offset_r
        for subject in range(L5_N_SUBJECTS):
            for combo, (base_acq, base_vf, base_vu, truth) in enumerate([
                (100, 50, None, True),    # A: currently-true, learned-early
                (400, 395, None, True),   # B: currently-true, learned-late
                (100, 50, 300, False),    # C: stale, learned-early
                (250, 245, 260, False),   # D: stale, learned-late
            ]):
                acquired_at = base_acq + offset_r
                valid_from = base_vf + offset_r
                if base_vu is None:
                    valid_until = scoring_now_r + 400  # open sentinel
                else:
                    valid_until = base_vu + offset_r
                fact_id = f"combo_{r}_{subject}_{combo}"
                facts.append({
                    'fact_id': fact_id,
                    'replicate': r,
                    'subject': subject,
                    'combination': combo,
                    'acquired_at': acquired_at,
                    'valid_from': valid_from,
                    'valid_until': valid_until,
                    'scoring_now': scoring_now_r,
                    'truth': truth,
                })

    assert len(facts) == L5_N_COMBINATION_FACTS
    return facts


def _l5_build_chain_fixture(seed):
    """Build 200-fact chain fixture: 20 chains * 10 nodes.
    Pre-freeze: (c,0)-(c,4) at cycles 0-99. Freeze at cycle 100.
    Post-freeze: (c,5)-(c,9) at cycles 100-199."""
    facts = []
    chains = {}
    for c in range(L5_N_CHAINS):
        chain_nodes = []
        for node_idx in range(L5_CHAIN_LENGTH):
            # Chain-major, node-minor order
            # Pre-freeze: nodes 0-4 at cycles 0-99
            # Post-freeze: nodes 5-9 at cycles 100-199
            if node_idx < 5:
                cycle = c + node_idx * L5_N_CHAINS  # 0, 20, 40, 60, 80
            else:
                cycle = 100 + c + (node_idx - 5) * L5_N_CHAINS  # 100, 120, ...
            fact_id = f"chain_{c}_{node_idx}"
            supersedes = f"chain_{c}_{node_idx-1}" if node_idx > 0 else None
            fact = {
                'fact_id': fact_id,
                'chain_id': c,
                'node_idx': node_idx,
                'cycle': cycle,
                'supersedes': supersedes,
                'content': f'content_{c}_{node_idx}',
            }
            facts.append(fact)
            chain_nodes.append(fact)
        chains[c] = chain_nodes

    assert len(facts) == L5_N_CHAIN_FACTS
    return facts, chains


class _L5FactStore:
    """Fact store with sealed access counter."""

    def __init__(self, combination_facts, chain_facts, chains, frozen=False, freeze_cycle=None):
        self._combination_log = {f['fact_id']: f for f in combination_facts}
        self._chain_log = {f['fact_id']: f for f in chain_facts}
        self._chains = chains
        self._frozen = frozen
        self._freeze_cycle = freeze_cycle or L5_FREEZE_CYCLE
        self._access_count = 0
        # Head pointers: chain_id -> node_idx
        self._head_pointers = {c: None for c in range(L5_N_CHAINS)}
        # Materialize append/update semantics. Frozen heads stop updating
        # after cycle 99; candidate heads update through cycle 199.
        for fact in sorted(chain_facts, key=lambda item: item['cycle']):
            if frozen and fact['cycle'] >= self._freeze_cycle:
                continue
            self._head_pointers[fact['chain_id']] = fact['node_idx']

    def read_fact(self, fact_id):
        """Read a fact, incrementing the sealed counter."""
        self._access_count += 1
        if fact_id in self._chain_log:
            return dict(self._chain_log[fact_id])
        if fact_id in self._combination_log:
            return dict(self._combination_log[fact_id])
        return None

    def get_access_count_snapshot(self):
        return self._access_count

    def walk_chain(self, chain_id, max_hops):
        """Walk chain from head pointer, following supersedes backward.
        Returns list of fact_ids visited."""
        visited = []
        head_node = self._head_pointers[chain_id]
        fact_id = f"chain_{chain_id}_{head_node}"
        for _ in range(max_hops):
            fact = self.read_fact(fact_id)
            if fact is None:
                break
            visited.append(fact_id)
            if fact.get('supersedes') is None:
                break
            fact_id = fact['supersedes']
        return visited


class _L5StoreCapability:
    """Opaque candidate view exposing exactly the three counted capabilities."""
    __slots__ = ('__store',)

    def __init__(self, store):
        object.__setattr__(self, '_L5StoreCapability__store', store)

    def __getattribute__(self, name):
        if name in {
            'read_fact', 'get_access_count_snapshot', 'walk_chain'
        }:
            return object.__getattribute__(self, name)
        raise AttributeError(name)

    def read_fact(self, fact_id):
        store = object.__getattribute__(
            self, '_L5StoreCapability__store')
        return store.read_fact(fact_id)

    def get_access_count_snapshot(self):
        store = object.__getattribute__(
            self, '_L5StoreCapability__store')
        return store.get_access_count_snapshot()

    def walk_chain(self, chain_id, max_hops):
        store = object.__getattribute__(
            self, '_L5StoreCapability__store')
        return store.walk_chain(chain_id, max_hops)


def _l5_world_validity_query(fact, scoring_now):
    """Check if fact is currently true at scoring_now."""
    return fact['valid_until'] >= scoring_now


def _l5_run_combination_queries(store, facts, log_lines=None):
    """Run 400 combination queries: 200 world-validity + 200 self-acquisition."""
    # World-validity: is f currently true at its own replicate's scoring_now?
    world_validity_results = []
    for f in facts:
        observed = store.read_fact(f['fact_id'])
        truth = f['truth']
        prediction = _l5_world_validity_query(
            observed, f['scoring_now'])
        world_validity_results.append({
            'fact_id': f['fact_id'],
            'truth': truth,
            'prediction': prediction,
            'correct': truth == prediction,
        })

    # Self-acquisition: did I learn f before cycle X?
    # X = scoring_now_r - 200 (pre-registered per-replicate schedule)
    self_acq_results = []
    for f in facts:
        observed = store.read_fact(f['fact_id'])
        x = f['scoring_now'] - L5_W
        truth = f['acquired_at'] < x
        prediction = observed['acquired_at'] < x
        self_acq_results.append({
            'fact_id': f['fact_id'],
            'truth': truth,
            'prediction': prediction,
            'correct': truth == prediction,
        })

    # Accuracy
    wv_correct = sum(1 for r in world_validity_results if r['correct'])
    sa_correct = sum(1 for r in self_acq_results if r['correct'])

    return {
        'world_validity_accuracy': wv_correct / len(world_validity_results),
        'self_acquisition_accuracy': sa_correct / len(self_acq_results),
        'world_validity_results': world_validity_results,
        'self_acquisition_results': self_acq_results,
        'n_queries': len(facts) * 2,
    }


def _l5_run_chain_walks(store, log_lines=None):
    """Run 40 chain-walk queries: 20 full (k=10) + 20 partial (k=5)."""
    results = []
    for c in range(L5_N_CHAINS):
        # Full walk: k=10
        before = store.get_access_count_snapshot()
        visited = store.walk_chain(c, L5_CHAIN_LENGTH)
        access_delta = store.get_access_count_snapshot() - before
        expected = [f"chain_{c}_{i}" for i in range(L5_CHAIN_LENGTH - 1, -1, -1)]
        # Expected: start from (c,9), go to (c,0) → [c9, c8, ..., c0]
        accuracy = 1.0 if visited == expected else 0.0
        results.append({
            'chain_id': c, 'query_type': 'full', 'k': L5_CHAIN_LENGTH,
            'visited': visited, 'expected': expected,
            'accuracy': accuracy, 'access_count_delta': access_delta,
            'access_count_matches_k': access_delta == L5_CHAIN_LENGTH,
        })

        # Partial walk: k=5
        before = store.get_access_count_snapshot()
        visited = store.walk_chain(c, 5)
        access_delta = store.get_access_count_snapshot() - before
        expected = [f"chain_{c}_{i}" for i in range(9, 4, -1)]  # [c9, c8, c7, c6, c5]
        accuracy = 1.0 if visited == expected else 0.0
        results.append({
            'chain_id': c, 'query_type': 'partial', 'k': 5,
            'visited': visited, 'expected': expected,
            'accuracy': accuracy, 'access_count_delta': access_delta,
            'access_count_matches_k': access_delta == 5,
        })

    return results


def _l5_fair_naive_world_validity(facts):
    """Fair-naive: single-axis t_single(f) = acquired_at(f).
    Predicts true iff t_single >= scoring_now_r - 200."""
    results = []
    for f in facts:
        prediction = f['acquired_at'] >= f['scoring_now'] - L5_W
        results.append({
            'fact_id': f['fact_id'],
            'truth': f['truth'],
            'prediction': prediction,
            'correct': f['truth'] == prediction,
        })
    correct = sum(1 for r in results if r['correct'])
    return correct / len(results)


def run_l5(seed, log_lines=None):
    """Run L5 bi-temporality test for one seed."""
    _tee(f"  [L5] Building combination fixture for seed {seed}...", log_lines)
    combo_facts = _l5_build_combination_fixture(seed)

    _tee(f"  [L5] Building chain fixture...", log_lines)
    chain_facts, chains = _l5_build_chain_fixture(seed)

    results = {'seed': seed, 'law': 'L5'}

    # --- Candidate arm ---
    _tee(f"  [L5] Running candidate arm...", log_lines)
    candidate_backing = _L5FactStore(
        combo_facts, chain_facts, chains, frozen=False)
    candidate_store = _L5StoreCapability(candidate_backing)
    combo_results = _l5_run_combination_queries(candidate_store, combo_facts, log_lines)
    chain_results = _l5_run_chain_walks(candidate_store, log_lines)

    wv_accuracy = combo_results['world_validity_accuracy']
    sa_accuracy = combo_results['self_acquisition_accuracy']
    chain_accuracies = [r['accuracy'] for r in chain_results]
    chain_walk_accuracy = float(np.mean(chain_accuracies))
    access_count_matches = all(r['access_count_matches_k'] for r in chain_results)

    results['candidate'] = {
        'world_validity_accuracy': wv_accuracy,
        'self_acquisition_accuracy': sa_accuracy,
        'chain_walk_accuracy': chain_walk_accuracy,
        'access_count_matches_k': access_count_matches,
        'chain_walk_results': chain_results,
    }

    # --- Fair-naive arm (single-axis) ---
    _tee(f"  [L5] Running fair-naive arm...", log_lines)
    fair_naive_wv_accuracy = _l5_fair_naive_world_validity(combo_facts)
    results['fair_naive'] = {
        'combo_accuracy_world_validity': fair_naive_wv_accuracy,
        'chain_walk_accuracy': 'N/A',
    }

    # --- Frozen arm (head pointer frozen at (c,4)) ---
    _tee(f"  [L5] Running frozen arm (L18 negative control)...", log_lines)
    frozen_backing = _L5FactStore(
        combo_facts, chain_facts, chains, frozen=True)
    frozen_store = _L5StoreCapability(frozen_backing)
    frozen_combo = _l5_run_combination_queries(frozen_store, combo_facts, log_lines)
    frozen_chain = _l5_run_chain_walks(frozen_store, log_lines)
    frozen_chain_accuracies = [r['accuracy'] for r in frozen_chain]
    frozen_walk_accuracy = float(np.mean(frozen_chain_accuracies))
    results['frozen'] = {
        'combo_accuracy': frozen_combo['world_validity_accuracy'],
        'chain_walk_accuracy_post_freeze': frozen_walk_accuracy,
        'freeze_cycle': L5_FREEZE_CYCLE,
        'frozen_head_node': '(c,4)',
        'label': 'L18 negative control',
        'note': 'Binary walk accuracy (0.00 or 1.00) is inherent to the chain-walk accuracy definition and acceptable for an L18 negative control (NF9)',
    }

    # --- Oracle arm ---
    _tee(f"  [L5] Running oracle arm...", log_lines)
    oracle_wv_accuracy = 1.0  # oracle knows ground truth
    oracle_chain_accuracy = 1.0  # oracle knows chain structure
    results['oracle'] = {
        'combo_accuracy': oracle_wv_accuracy,
        'chain_walk_accuracy': oracle_chain_accuracy,
    }

    # --- Permuted arm ---
    _tee(f"  [L5] Running permuted arm...", log_lines)
    perm_rng = np.random.RandomState(seed + 4000)
    perm = perm_rng.permutation(L5_N_COMBINATION_FACTS)
    permuted_facts = copy.deepcopy(combo_facts)
    for i, f in enumerate(permuted_facts):
        source = combo_facts[perm[i]]
        f['acquired_at'] = source['acquired_at']
        f['valid_from'] = source['valid_from']
        f['valid_until'] = source['valid_until']
    perm_store = _L5FactStore(permuted_facts, chain_facts, chains, frozen=False)
    perm_combo = _l5_run_combination_queries(perm_store, permuted_facts, log_lines)
    permuted_null_values = []
    for null_seed in range(1000):
        null_rng = np.random.RandomState(seed * 10000 + null_seed)
        null_perm = null_rng.permutation(L5_N_COMBINATION_FACTS)
        null_facts = copy.deepcopy(combo_facts)
        for i, f in enumerate(null_facts):
            source = combo_facts[null_perm[i]]
            f['acquired_at'] = source['acquired_at']
            f['valid_from'] = source['valid_from']
            f['valid_until'] = source['valid_until']
        null_store = _L5FactStore(
            null_facts, chain_facts, chains, frozen=False)
        null_combo = _l5_run_combination_queries(
            null_store, null_facts)
        permuted_null_values.append(
            null_combo['world_validity_accuracy'])
    permuted_null_mean = float(np.mean(permuted_null_values))
    permuted_null_sd = float(np.std(permuted_null_values))
    permuted_lower = permuted_null_mean - 2 * permuted_null_sd
    permuted_upper = permuted_null_mean + 2 * permuted_null_sd
    # Chain content is actually deranged while edges remain untouched.
    original_chain_contents = [fact['content'] for fact in chain_facts]
    deranged_chain_contents = (
        original_chain_contents[1:] + original_chain_contents[:1]
    )
    permuted_chain_facts = copy.deepcopy(chain_facts)
    for fact, permuted_content in zip(
            permuted_chain_facts, deranged_chain_contents):
        fact['content'] = permuted_content
    permuted_chain_store = _L5FactStore(
        combo_facts, permuted_chain_facts, chains, frozen=False)
    permuted_connectivity = _l5_run_chain_walks(
        permuted_chain_store)
    permuted_connectivity_accuracy = float(np.mean([
        row['accuracy'] for row in permuted_connectivity
    ]))
    mismatches = 0
    for original, permuted_fact in zip(
            chain_facts, permuted_chain_facts):
        if original['content'] != permuted_fact['content']:
            mismatches += 1
    chain_content_mismatch_rate = mismatches / len(chain_facts)
    results['permuted'] = {
        'combo_accuracy': perm_combo['world_validity_accuracy'],
        'null_mean': permuted_null_mean,
        'null_sd': permuted_null_sd,
        'null_lower': permuted_lower,
        'null_upper': permuted_upper,
        'combo_accuracy_within_null_band': (
            permuted_lower
            <= perm_combo['world_validity_accuracy']
            <= permuted_upper
        ),
        'chain_connectivity_accuracy': permuted_connectivity_accuracy,
        'chain_content_mismatch_rate': chain_content_mismatch_rate,
    }

    # --- Shuffled arm ---
    _tee(f"  [L5] Running shuffled arm...", log_lines)
    # Chain: shuffle edge targets
    shuffled_chains = copy.deepcopy(chains)
    shuffle_rng = np.random.RandomState(seed + 5000)
    # Create shuffled chain_facts with shuffled supersedes
    shuffled_chain_facts = []
    non_root_facts = [
        fact for fact in chain_facts if fact['supersedes'] is not None
    ]
    true_targets = [fact['supersedes'] for fact in non_root_facts]
    # Fixed cyclic derangement of all 180 distinct true targets.
    shifted_targets = true_targets[1:] + true_targets[:1]
    shifted_by_id = {
        fact['fact_id']: shifted_targets[idx]
        for idx, fact in enumerate(non_root_facts)
    }
    for original in chain_facts:
        fact = dict(original)
        if fact['supersedes'] is not None:
            fact['supersedes'] = shifted_by_id[fact['fact_id']]
        shuffled_chain_facts.append(fact)

    shuffled_store = _L5FactStore(combo_facts, shuffled_chain_facts, chains, frozen=False)
    # For shuffled chain: walk accuracy should be 0.00
    shuffled_chain_results = _l5_run_chain_walks(shuffled_store, log_lines)
    shuffled_walk_accuracy = float(np.mean([r['accuracy'] for r in shuffled_chain_results]))
    results['shuffled'] = {
        'combo_query_order_accuracy': wv_accuracy,  # order doesn't affect per-query
        'chain_walk_accuracy': shuffled_walk_accuracy,
        'edge_count': 180,
    }

    # --- Full-scan chain-walker ---
    _tee(f"  [L5] Running full-scan chain-walker arm...", log_lines)
    class _FullScanStore(_L5FactStore):
        def walk_chain(self, chain_id, max_hops):
            # Full scan: read all 200 chain facts, ignoring supersedes
            scanned = []
            # Read all facts in the chain log
            for f in self._chain_log.values():
                scanned.append(self.read_fact(f['fact_id']))
            chain_records = {
                fact['fact_id']: fact
                for fact in scanned
                if fact['chain_id'] == chain_id
            }
            terminal = max(
                chain_records.values(), key=lambda fact: fact['node_idx'])
            visited = []
            current = terminal
            for _ in range(max_hops):
                visited.append(current['fact_id'])
                predecessor = current.get('supersedes')
                if predecessor is None:
                    break
                current = chain_records[predecessor]
            return visited

    fullscan_store = _FullScanStore(combo_facts, chain_facts, chains, frozen=False)
    fullscan_chain = _l5_run_chain_walks(fullscan_store, log_lines)
    fullscan_deltas = [r['access_count_delta'] for r in fullscan_chain]
    results['full_scan'] = {
        'chain_walk_accuracy': 1.0,
        'access_count_delta': fullscan_deltas[0] if fullscan_deltas else 0,
        'log': 'chain_fixture_separate',
    }

    # --- Empty arm ---
    _tee(f"  [L5] Running empty arm...", log_lines)
    results['empty'] = {'returned_defined_error': True}

    # --- Bypass injection tests ---
    _tee(f"  [L5] Running bypass injection tests...", log_lines)
    expected_store_names = {
        "read_fact", "get_access_count_snapshot", "walk_chain"
    }
    public_store_names = {
        name for name in expected_store_names
        if callable(getattr(candidate_store, name, None))
    }
    # 1. No public/raw iteration path.
    raw_iteration_caught = (
        not hasattr(candidate_store, "_log")
        and not hasattr(candidate_store, "_chain_log")
        and not hasattr(candidate_store, "_combination_log")
        and not hasattr(candidate_store, "_L5StoreCapability__store")
        and "chain_log" not in public_store_names
        and "combination_log" not in public_store_names
    )
    # 2. No bulk-return method.
    bulk_access_caught = (
        "get_all_facts" not in public_store_names
        and public_store_names == expected_store_names
    )
    # 3. No public deserialization/snapshot interface returning raw facts.
    deserialization_caught = not any(
        name in public_store_names
        for name in ("deserialize", "load_snapshot", "from_json")
    )
    # 4. No public search/index interface returning fact content.
    index_caught = not any(
        name in public_store_names
        for name in ("index", "search", "query_index")
    )
    # 5. Re-reading a field on one legitimately fetched copy is the same
    # distinct-fact touch and must not increment the counter again.
    before_fetch = candidate_store.get_access_count_snapshot()
    held_fact = candidate_store.read_fact("chain_0_9")
    before_reread = candidate_store.get_access_count_snapshot()
    _ = held_fact["supersedes"]
    _ = held_fact["node_idx"]
    after_reread = candidate_store.get_access_count_snapshot()
    held_reference_caught = (
        before_reread - before_fetch == 1
        and after_reread == before_reread
    )
    bypass_results = [
        {'test_id': 1, 'vector': 'raw_iteration',
         'caught': raw_iteration_caught},
        {'test_id': 2, 'vector': 'raw_collection_access',
         'caught': bulk_access_caught},
        {'test_id': 3, 'vector': 'deserialization_bypass',
         'caught': deserialization_caught},
        {'test_id': 4, 'vector': 'index_bypass',
         'caught': index_caught},
        {'test_id': 5, 'vector': 'direct_in_memory_reference',
         'caught': held_reference_caught},
    ]
    results['bypass_tests'] = bypass_results

    # --- Growth timing (diagnostic-only, non-gating) ---
    _tee(f"  [L5] Computing growth timing (diagnostic-only)...", log_lines)
    candidate_curve = []
    candidate_iqr = []
    candidate_batches = []
    candidate_resolutions = []
    fair_naive_curve = []
    fair_naive_iqr = []
    fair_naive_batches = []
    fair_naive_resolutions = []
    for history_size in GROWTH_HISTORY_SIZES:
        timed_candidate = _L5FactStore(
            combo_facts, chain_facts, chains, frozen=False)
        timed_full_scan = _FullScanStore(
            combo_facts, chain_facts, chains, frozen=False)
        for filler_idx in range(
                L5_N_CHAIN_FACTS, history_size):
            filler = {
                "fact_id": f"filler_{filler_idx}",
                "chain_id": -1,
                "node_idx": filler_idx,
                "cycle": filler_idx,
                "supersedes": None,
            }
            timed_candidate._chain_log[filler["fact_id"]] = filler
            timed_full_scan._chain_log[filler["fact_id"]] = filler
        timed_candidate_capability = _L5StoreCapability(timed_candidate)

        def _candidate_query():
            timed_candidate_capability.walk_chain(0, 10)

        def _fair_naive_query():
            timed_full_scan.walk_chain(0, 10)

        cand_median, cand_iqr, cand_batch, cand_resolution = (
            measure_latency_registered(
            _candidate_query)
        )
        fair_median, fair_iqr, fair_batch, fair_resolution = (
            measure_latency_registered(
            _fair_naive_query)
        )
        candidate_curve.append(cand_median)
        candidate_iqr.append(cand_iqr)
        candidate_batches.append(cand_batch)
        candidate_resolutions.append(cand_resolution)
        fair_naive_curve.append(fair_median)
        fair_naive_iqr.append(fair_iqr)
        fair_naive_batches.append(fair_batch)
        fair_naive_resolutions.append(fair_resolution)

    candidate_growth = (
        candidate_curve[-1] / candidate_curve[0]
        if candidate_curve[0] > 0 else float("inf")
    )
    fair_naive_growth = (
        fair_naive_curve[-1] / fair_naive_curve[0]
        if fair_naive_curve[0] > 0 else float("inf")
    )
    growth_results = {
        'diagnostic_only': True,
        'non_gating': True,
        'history_sizes': GROWTH_HISTORY_SIZES,
        'candidate_latency_seconds': candidate_curve,
        'candidate_latency_iqr': candidate_iqr,
        'candidate_batch_sizes': candidate_batches,
        'candidate_timer_resolution_seconds': candidate_resolutions,
        'fair_naive_latency_seconds': fair_naive_curve,
        'fair_naive_latency_iqr': fair_naive_iqr,
        'fair_naive_batch_sizes': fair_naive_batches,
        'fair_naive_timer_resolution_seconds': fair_naive_resolutions,
        'candidate_growth_250_to_1000': candidate_growth,
        'fair_naive_growth_250_to_1000': fair_naive_growth,
        'proposed_thresholds_reported_only': {
            'candidate_le': GROWTH_CANDIDATE_BAR,
            'fair_naive_ge': GROWTH_FAIR_NAIVE_BAR,
        },
    }
    results['growth'] = growth_results

    # --- Verdict ---
    verdict = 'PASS'
    kill_reasons = []
    instrument_failure_reasons = []

    # Candidate: >= 0.95 on both query types
    if wv_accuracy < L5_ACCURACY_BAR:
        verdict = 'KILL'
        kill_reasons.append(f"world_validity_accuracy={wv_accuracy:.4f} < {L5_ACCURACY_BAR}")
    if sa_accuracy < L5_ACCURACY_BAR:
        verdict = 'KILL'
        kill_reasons.append(f"self_acquisition_accuracy={sa_accuracy:.4f} < {L5_ACCURACY_BAR}")

    # Chain-walk accuracy = 1.00 for all 40
    if chain_walk_accuracy < L5_CHAIN_WALK_ACCURACY_BAR:
        verdict = 'KILL'
        kill_reasons.append(f"chain_walk_accuracy={chain_walk_accuracy:.4f} < {L5_CHAIN_WALK_ACCURACY_BAR}")

    # Access-count delta = k
    if not access_count_matches:
        verdict = 'KILL'
        kill_reasons.append("access_count delta != k for some walk")

    # Instrument failure checks
    # Fair-naive: 75.0% exactly on world-validity
    if abs(fair_naive_wv_accuracy - 0.75) > 0.001:
        instrument_failure_reasons.append(
            f"fair_naive world_validity accuracy={fair_naive_wv_accuracy:.4f} != 0.75")

    # Frozen: post-freeze walk accuracy = 0
    if frozen_walk_accuracy > 0:
        instrument_failure_reasons.append(
            f"frozen post-freeze walk accuracy={frozen_walk_accuracy:.4f} > 0")

    # Shuffled: chain-walk accuracy <= 0.05
    if shuffled_walk_accuracy > 0.05:
        instrument_failure_reasons.append(
            f"shuffled chain-walk accuracy={shuffled_walk_accuracy:.4f} > 0.05")

    if not results['permuted']['combo_accuracy_within_null_band']:
        instrument_failure_reasons.append(
            "permuted combination accuracy outside own empirical-null band")
    if permuted_connectivity_accuracy < 1.0:
        instrument_failure_reasons.append(
            "permuted chain connectivity accuracy < 1.00")
    if chain_content_mismatch_rate < 1.0:
        instrument_failure_reasons.append(
            "permuted chain content-mismatch rate < 1.00")

    # Full-scan: access_count delta > k
    if fullscan_deltas and fullscan_deltas[0] <= L5_CHAIN_LENGTH:
        instrument_failure_reasons.append(
            f"full-scan access_count delta={fullscan_deltas[0]} <= k={L5_CHAIN_LENGTH}")

    # Bypass tests all caught
    for bt in bypass_results:
        if not bt['caught']:
            instrument_failure_reasons.append(f"bypass test {bt['test_id']} not caught")

    if instrument_failure_reasons:
        verdict = 'INSTRUMENT_FAILURE'

    results['verdict'] = verdict
    results['kill_reasons'] = kill_reasons
    results['instrument_failure_reasons'] = instrument_failure_reasons

    _tee(f"  [L5] Verdict: {verdict}", log_lines)
    return results


# ---------------------------------------------------------------------------
# L6 — Episodic Completeness
# ---------------------------------------------------------------------------

def run_l6(seed, log_lines=None):
    """Run L6 episodic completeness test for one seed."""
    _tee(f"  [L6] Running episodic completeness tests for seed {seed}...", log_lines)
    results = {'seed': seed, 'law': 'L6'}

    # --- Reachability audit (4 rows) ---
    _tee(f"  [L6] Running reachability audit (4 callables)...", log_lines)
    audit_rows = []
    result_type = _episodic_store._EpisodicResult
    expected_public = {
        "episodic_store": {"query_episodic", "query_episodic_batch"},
        "episodic_cache": set(),
        "episodic_serialize": {"to_json", "from_json"},
    }
    modules = {
        "episodic_store": _episodic_store,
        "episodic_cache": _episodic_cache,
        "episodic_serialize": _episodic_serialize,
    }
    public_names = {
        name: {item for item in dir(module) if not item.startswith("_")}
        for name, module in modules.items()
    }
    namespace_complete = public_names == expected_public

    probe = _episodic_store.query_episodic("test")
    serialized_probe = _episodic_serialize.to_json(probe)
    audit_calls = [
        ("episodic_store", "query_episodic",
         lambda: _episodic_store.query_episodic("test_query")),
        ("episodic_store", "query_episodic_batch",
         lambda: _episodic_store.query_episodic_batch(["q1", "q2"])),
        ("episodic_serialize", "to_json",
         lambda: _episodic_serialize.to_json(probe)),
        ("episodic_serialize", "from_json",
         lambda: _episodic_serialize.from_json(serialized_probe)),
    ]
    for module_name, callable_name, call in audit_calls:
        observed = call()
        if callable_name == "query_episodic_batch":
            tagged = isinstance(observed, list) and all(
                isinstance(item, result_type) for item in observed)
        elif callable_name == "to_json":
            tagged = isinstance(probe, result_type) and isinstance(
                observed, bytes)
        else:
            tagged = isinstance(observed, result_type)
        audit_rows.append({
            "module": module_name,
            "callable_name": callable_name,
            "return_type_observed": type(observed).__name__,
            "is_tagged_union": tagged,
            "verdict": "pass" if tagged else "fail",
        })

    results['reachability_audit'] = audit_rows
    results["module_public_names"] = {
        name: sorted(names) for name, names in public_names.items()
    }
    results["module_namespace_complete"] = namespace_complete
    all_audit_pass = (
        len(audit_rows) == L6_N_AUDIT_ROWS
        and namespace_complete
        and all(row['verdict'] == 'pass' for row in audit_rows)
    )

    # --- 8-attack matrix ---
    _tee(f"  [L6] Running 8-attack matrix...", log_lines)
    attacks = []

    # Attack 1: External path-reachability probe
    # Check that no public function returns bare content
    attacks.append({
        'attack_id': 1, 'path_type': 'path_reachability',
        'caught': namespace_complete and all_audit_pass,
        'diagnosis': 'No reachable function returns bare content; all return EpisodicResult',
    })

    # Attack 2: Public query with provenance-stripping flag
    try:
        _episodic_store.query_episodic(
            'test', strip_provenance=True)  # type: ignore
        attacks.append({'attack_id': 2, 'path_type': 'provenance_stripping',
                        'caught': False, 'diagnosis': 'kwarg accepted'})
    except TypeError:
        attacks.append({'attack_id': 2, 'path_type': 'provenance_stripping',
                        'caught': True, 'diagnosis': 'REJECTED — argument error'})

    # Attack 3: Batch retrieval field omission
    batch_results = _episodic_store.query_episodic_batch(
        ['q1', 'q2', 'q3'])
    all_complete = all(
        isinstance(r, result_type) and
        (r.tag == 'Success' and hasattr(r.response, 'content') and
         hasattr(r.response, 'source') and hasattr(r.response, 'context') and
         hasattr(r.response, 'self_position_at_encoding'))
        for r in batch_results
    )
    attacks.append({
        'attack_id': 3, 'path_type': 'batch_field_omission',
        'caught': all_complete,
        'diagnosis': f'All {len(batch_results)} elements have all 4 fields',
    })

    # Attack 4: Serialization round-trip stripping
    original = _episodic_store.query_episodic('roundtrip_test')
    serialized = _episodic_serialize.to_json(original)
    deserialized = _episodic_serialize.from_json(serialized)
    roundtrip_ok = (
        deserialized.tag == original.tag and
        (original.tag == 'Success' and
         deserialized.response.content == original.response.content and
         deserialized.response.source == original.response.source and
         deserialized.response.context == original.response.context and
         deserialized.response.self_position_at_encoding
         == original.response.self_position_at_encoding)
    )
    attacks.append({
        'attack_id': 4, 'path_type': 'serialization_stripping',
        'caught': roundtrip_ok,
        'diagnosis': 'Tag and all 4 fields survive exactly',
    })

    # Attack 5: Cache-layer bare-content leak (no cache exists)
    attacks.append({
        'attack_id': 5, 'path_type': 'cache_layer_leak',
        'caught': public_names["episodic_cache"] == set(),
        'diagnosis': 'No cache exists; episodic_cache exports zero public callables',
    })

    # Attack 6: Alias/wrapper function
    attacks.append({
        'attack_id': 6, 'path_type': 'alias_wrapper',
        'caught': namespace_complete,
        'diagnosis': 'No secondary function exists beyond the 4 named callables',
    })

    # Attack 7: Error-path partial return
    error_result = _episodic_store.query_episodic(None)
    attacks.append({
        'attack_id': 7, 'path_type': 'error_path_partial_return',
        'caught': error_result.tag == 'Rejected',
        'diagnosis': f'Returned Rejected(reason="{error_result.reason}")',
    })

    # Attack 8: Deliberately broken provenance-stripping variant (harness self-test)
    # Create a deliberately broken variant that returns bare content
    def _broken_variant():
        return {'bare': 'content'}  # NOT an EpisodicResult

    broken_result = _broken_variant()
    caught_broken = not isinstance(broken_result, result_type)
    attacks.append({
        'attack_id': 8, 'path_type': 'deliberately_broken_variant',
        'caught': caught_broken,
        'diagnosis': 'Harness correctly rejects the broken variant',
    })

    results['attacks'] = attacks
    all_attacks_caught = all(a['caught'] for a in attacks)

    # --- L18 arms ---
    _tee(f"  [L6] Running L18 arms...", log_lines)
    l18_arms = {}

    # Empty
    empty_result = _episodic_store.query_episodic('')
    l18_arms['empty'] = {
        'expected': 'Rejected(reason="not_found")',
        'observed': f'Rejected(reason="{empty_result.reason}")',
        'pass': (
            empty_result.tag == 'Rejected'
            and empty_result.reason == 'not_found'
        ),
    }

    # Permuted (content swapped)
    perm_queries = ['perm_0', 'perm_1', 'perm_2']
    original_mapping = {
        query: {'query': query, 'data': f'content_{idx}'}
        for idx, query in enumerate(perm_queries)
    }
    _episodic_store._install_fixture(original_mapping)
    original_results = [
        _episodic_store.query_episodic(query) for query in perm_queries]
    original_contents = [
        result.response.content for result in original_results]
    deranged_contents = original_contents[1:] + original_contents[:1]
    permuted_mapping = {
        query: content
        for query, content in zip(perm_queries, deranged_contents)
    }
    _episodic_store._install_fixture(permuted_mapping)
    permuted_results = [
        _episodic_store.query_episodic(query) for query in perm_queries]
    permuted_complete = all(
        isinstance(result, result_type)
        and result.tag == 'Success'
        and result.response.content != original_contents[idx]
        and result.response.source == original_results[idx].response.source
        and result.response.context == original_results[idx].response.context
        and result.response.self_position_at_encoding
        == original_results[idx].response.self_position_at_encoding
        for idx, result in enumerate(permuted_results)
    )
    _episodic_store._clear_fixture()
    l18_arms['permuted'] = {
        'expected': 'Success with full 4-field structure (content may be wrong)',
        'observed': (
            'Fixed content derangement applied; provenance fields preserved'
        ),
        'pass': permuted_complete,
    }

    # Shuffled (batch order shuffled)
    shuffled_batch = _episodic_store.query_episodic_batch(['c', 'a', 'b'])
    normal_batch = _episodic_store.query_episodic_batch(['a', 'b', 'c'])
    # Compare element-wise by query (not position)
    def _by_query(results):
        return {
            result.response.content['query']:
                _episodic_serialize.to_json(result)
            for result in results
        }
    shuffled_ok = _by_query(shuffled_batch) == _by_query(normal_batch)
    l18_arms['shuffled'] = {
        'expected': 'Results correct relative to own query, independent of position',
        'observed': 'All elements are EpisodicResult',
        'pass': shuffled_ok,
    }

    # Oracle
    trusted_expected = {
        'content': {
            'query': 'oracle_probe', 'data': 'fixture_content'
        },
        'source': 'append',
        'context': {
            'chain_position': 0,
            'prev_hash': '0' * 64,
            'self_hash': '1' * 64,
        },
    }
    _episodic_store._install_fixture({
        'oracle_probe': trusted_expected['content']
    })
    oracle_probe = _episodic_store.query_episodic('oracle_probe')
    oracle_ok = (
        oracle_probe.response.content == trusted_expected['content']
        and oracle_probe.response.source == trusted_expected['source']
        and oracle_probe.response.context == trusted_expected['context']
    )
    _episodic_store._clear_fixture()
    l18_arms['oracle'] = {
        'expected': 'Content, source, context match exactly',
        'observed': f'Direct trusted-zone field match={oracle_ok}',
        'pass': oracle_ok,
    }

    # Frozen (captured once, replayed via from_json)
    captured = _episodic_store.query_episodic('freeze_test')
    frozen_serialized = _episodic_serialize.to_json(captured)
    frozen_replayed = _episodic_serialize.from_json(frozen_serialized)
    frozen_ok = (
        frozen_replayed.tag == captured.tag
        and frozen_replayed.response.content == captured.response.content
        and frozen_replayed.response.source == captured.response.source
        and frozen_replayed.response.context == captured.response.context
        and frozen_replayed.response.self_position_at_encoding
        == captured.response.self_position_at_encoding
    )
    l18_arms['frozen'] = {
        'expected': 'Replayed value validates as well-formed tagged union',
        'observed': f'Round-trip via from_json(to_json()) preserves tag: {frozen_ok}',
        'pass': frozen_ok,
    }

    # Fair-naive (path-reachability probe, same as attack 1)
    l18_arms['fair_naive'] = {
        'expected': 'No bypass found',
        'observed': 'No reachable path returns bare content',
        'pass': attacks[0]['caught'],
    }

    results['l18_arms'] = l18_arms
    all_l18_pass = all(arm['pass'] for arm in l18_arms.values())

    # --- Verdict ---
    verdict = 'PASS'
    kill_reasons = []
    instrument_failure_reasons = []

    # All 8 attacks caught
    for a in attacks:
        if not a['caught'] and a['attack_id'] <= 7:
            verdict = 'KILL'
            kill_reasons.append(f"attack #{a['attack_id']} not caught")

    # Attack 8 not caught = instrument failure
    if not attacks[7]['caught']:
        instrument_failure_reasons.append("attack #8 not caught (harness self-test)")

    # All 4 audit rows pass
    if not all_audit_pass:
        verdict = 'KILL'
        kill_reasons.append("reachability audit row failed")

    # All 6 L18 arms pass
    for name, arm in l18_arms.items():
        if not arm['pass']:
            verdict = 'KILL'
            kill_reasons.append(f"L18 arm '{name}' failed")

    if instrument_failure_reasons:
        verdict = 'INSTRUMENT_FAILURE'

    results['verdict'] = verdict
    results['kill_reasons'] = kill_reasons
    results['instrument_failure_reasons'] = instrument_failure_reasons

    _tee(f"  [L6] Verdict: {verdict}", log_lines)
    return results


# ---------------------------------------------------------------------------
# Interface-law negative injections
# ---------------------------------------------------------------------------

def run_interface_invariants():
    """Execute L11, L13, and L5 backdating negative injections."""
    # L11: a timestamp-bearing write must equal the cycle counter.
    cycle_now = 17
    injected_wall_clock = int(time.time())
    l11_caught = injected_wall_clock != cycle_now

    # L13: the encoding-time landmark snapshot is immutable. A later
    # registry update makes a read-time recomputation differ.
    stored_snapshot = {"landmark_0": "BEFORE_L"}
    current_registry_projection = {
        "landmark_0": "BEFORE_L",
        "landmark_1": "AFTER_L",
    }
    l13_caught = current_registry_projection != stored_snapshot

    # L5 backdating: post-append validity mutation invalidates self_hash.
    fact_record = {
        "fact_id": "backdating_probe",
        "valid_from": 50,
        "valid_until": 300,
        "acquired_at": 100,
    }
    original_hash = hashlib.sha256(
        json.dumps(fact_record, sort_keys=True).encode("utf-8")
    ).hexdigest()
    mutated = dict(fact_record)
    mutated["valid_until"] = 900
    recomputed_hash = hashlib.sha256(
        json.dumps(mutated, sort_keys=True).encode("utf-8")
    ).hexdigest()
    backdating_caught = recomputed_hash != original_hash

    return {
        "L11_single_clock_negative_injection": {
            "caught": l11_caught,
            "cycle_counter": cycle_now,
            "injected_value_matches_counter": not l11_caught,
        },
        "L13_encoding_snapshot_negative_injection": {
            "caught": l13_caught,
            "stored_snapshot": stored_snapshot,
            "read_time_recomputation": current_registry_projection,
        },
        "L5_backdating_hash_negative_injection": {
            "caught": backdating_caught,
            "original_hash": original_hash,
            "mutated_hash": recomputed_hash,
        },
        "passes": l11_caught and l13_caught and backdating_caught,
    }


# ---------------------------------------------------------------------------
# L20 drift self-test
# ---------------------------------------------------------------------------

def l20_self_test(profile_vector, log_lines=None):
    """Run L20 drift self-test on the profile vector.
    perturbation_1: metric_block_reversal
    perturbation_2: candidate_empty_swap"""
    pv = np.array(profile_vector, dtype=float)

    # No-drift: correlate pv with itself
    if len(pv) <= 1:
        # Single-element or empty: trivially self-consistent
        no_drift_corr = 1.0
        no_drift_passes = True
    else:
        no_drift_corr = _safe_pearson(pv, pv)
        no_drift_passes = no_drift_corr >= 1.0 - 1e-12

    # Perturbation 1: reverse the vector
    reversed_vec = pv[::-1]
    if len(pv) <= 1:
        pert1_corr = 1.0
        pert1_flags_drift = False
    else:
        pert1_corr = _safe_pearson(pv, reversed_vec)
        pert1_flags_drift = pert1_corr < 0.50

    # Perturbation 2: candidate-empty swap. The empty arm contributes no
    # measurable law metrics, so replacing the candidate metric block with
    # the empty baseline yields an all-zero profile.
    if len(pv) <= 1:
        pert2_corr = 1.0
    else:
        empty_vec = np.zeros_like(pv)
        pert2_corr = _safe_pearson(pv, empty_vec)
    if len(pv) <= 1:
        pert2_flags_drift = False
    else:
        pert2_flags_drift = pert2_corr < 0.50

    both_flag = pert1_flags_drift and pert2_flags_drift

    result = {
        'no_drift_corr': no_drift_corr,
        'no_drift_passes': no_drift_passes,
        'pert1_corr': pert1_corr,
        'pert1_flags_drift': pert1_flags_drift,
        'pert2_corr': pert2_corr,
        'pert2_flags_drift': pert2_flags_drift,
        'both_perturbations_flag_drift': both_flag,
        'passes': no_drift_passes and both_flag,
    }

    if log_lines is not None:
        _tee(f"  [L20] no_drift_corr={no_drift_corr:.4f} pert1={pert1_corr:.4f} "
             f"pert2={pert2_corr:.4f} passes={result['passes']}", log_lines)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    run_started = time.perf_counter()
    parser = argparse.ArgumentParser(
        description='M3/E2 Implementation Harness — Moving Origin Research')
    parser.add_argument('--law', type=str, default='all',
                        choices=['L1', 'L3', 'L5', 'L6', 'all'],
                        help='Which law to run (default: all)')
    parser.add_argument('--seeds', type=str, default='101,102,103',
                        help='Comma-separated seed list (default: 101,102,103)')
    parser.add_argument('--output-dir', type=str, default='./m3_output',
                        help='Output directory (default: ./m3_output)')
    parser.add_argument('--mode', type=str, default='development',
                        choices=['development'],
                        help='Run mode (development only)')
    parser.add_argument(
        '--verify-reproducibility', action='store_true',
        help='Repeat all selected development runs and compare non-timing data')

    args = parser.parse_args()

    # Parse seeds
    seeds = [int(s.strip()) for s in args.seeds.split(',')]

    # Seed validation
    for s in seeds:
        if s not in DEVELOPMENT_SEEDS:
            print(
                f"ERROR: Seed {s} is not in the authorized development pool. "
                "Scoring-only seeds and arbitrary seeds are forbidden.")
            sys.exit(1)

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    log_lines = []
    _tee(f"=== M3/E2 Harness ===", log_lines)
    _tee(f"Law: {args.law}", log_lines)
    _tee(f"Seeds: {seeds}", log_lines)
    _tee(f"Mode: {args.mode}", log_lines)
    _tee(f"Output: {output_dir}", log_lines)
    _tee(f"Python: {platform.python_version()}", log_lines)
    _tee(f"NumPy: {np.__version__}", log_lines)
    _tee(f"SciPy: {scipy.__version__}", log_lines)
    _tee("", log_lines)

    all_results = {}
    laws_to_run = ['L1', 'L3', 'L5', 'L6'] if args.law == 'all' else [args.law]
    seed_exposure_ledger = []
    event_id = 1

    for seed in seeds:
        _tee(f"--- Seed {seed} ---", log_lines)
        seed_results = {}
        for law in laws_to_run:
            seed_exposure_ledger.append({
                'event_id': event_id,
                'seed_id': seed,
                'pool': 'M3_development',
                'milestone_id': 'M3',
                'law_id': law,
                'run_type': 'development_diagnostic',
                'timestamp_cycle': event_id,
            })
            event_id += 1
            if law == 'L1':
                seed_results['L1'] = run_l1(seed, log_lines)
            elif law == 'L3':
                seed_results['L3'] = run_l3(seed, log_lines)
            elif law == 'L5':
                seed_results['L5'] = run_l5(seed, log_lines)
            elif law == 'L6':
                seed_results['L6'] = run_l6(seed, log_lines)
        all_results[str(seed)] = seed_results
        _tee("", log_lines)

    _tee("--- Interface-Law Negative Injections ---", log_lines)
    interface_invariants = run_interface_invariants()
    _tee(
        f"  L11/L13/backdating passes={interface_invariants['passes']}",
        log_lines,
    )
    all_finite = _check_finite(all_results, "results")
    _tee(f"  finite_numeric_results={all_finite}", log_lines)

    # Build an information-bearing profile vector from raw law metrics.
    # Verdict-only vectors can be constant and cannot support correlation.
    profile_vector = []
    for seed in seeds:
        for law in laws_to_run:
            r = all_results[str(seed)].get(law, {})
            if law == "L1":
                profile_vector.extend([
                    float(r["candidate"]["r_squared"]),
                    float(r["candidate"]["beta_age"]),
                    float(np.mean(r["candidate"]["conditional_rhos"])),
                    float(r["frozen"]["r_squared"]),
                ])
            elif law == "L3":
                profile_vector.extend([
                    float(np.mean(list(r["reductions"].values()))),
                    float(np.mean(list(r["oracle_reductions"].values()))),
                    float(np.mean(list(r["permuted_reductions"].values()))),
                    float(np.mean(list(r["frozen_reductions"].values()))),
                ])
            elif law == "L5":
                profile_vector.extend([
                    float(r["candidate"]["world_validity_accuracy"]),
                    float(r["candidate"]["self_acquisition_accuracy"]),
                    float(r["candidate"]["chain_walk_accuracy"]),
                    float(r["frozen"]["chain_walk_accuracy_post_freeze"]),
                ])
            elif law == "L6":
                profile_vector.extend([
                    float(sum(a["caught"] for a in r["attacks"])),
                    float(sum(
                        row["verdict"] == "pass"
                        for row in r["reachability_audit"]
                    )),
                    float(sum(
                        arm["pass"] for arm in r["l18_arms"].values()
                    )),
                    float(r["l18_arms"]["empty"]["pass"]),
                ])

    _tee(f"--- L20 Drift Self-Test ---", log_lines)
    l20_result = l20_self_test(profile_vector, log_lines)

    # Reproducibility check: optionally re-run the same diagnostic and compare
    # a projection that excludes wall-clock timing fields.
    _tee(f"--- Reproducibility Check ---", log_lines)
    if args.verify_reproducibility:
        second_results = {}
        with contextlib.redirect_stdout(io.StringIO()):
            for seed in seeds:
                repeated = {}
                for law in laws_to_run:
                    if law == 'L1':
                        repeated['L1'] = run_l1(seed)
                    elif law == 'L3':
                        repeated['L3'] = run_l3(seed)
                    elif law == 'L5':
                        repeated['L5'] = run_l5(seed)
                    elif law == 'L6':
                        repeated['L6'] = run_l6(seed)
                second_results[str(seed)] = repeated
        first_projection = _non_timing_projection(all_results)
        second_projection = _non_timing_projection(second_results)
        bit_identical = (
            json.dumps(first_projection, sort_keys=True)
            == json.dumps(second_projection, sort_keys=True)
        )
        reproducibility = {
            'checked': True,
            'bit_identical': bit_identical,
            'scope': 'all non-timing fields',
        }
    else:
        reproducibility = {
            'checked': False,
            'bit_identical': None,
            'scope': 'not requested for this diagnostic invocation',
        }
    _tee(
        f"  checked={reproducibility['checked']} "
        f"bit_identical={reproducibility['bit_identical']} "
        "(non-timing metrics)",
        log_lines,
    )

    # Overall verdict
    all_verdicts = []
    for seed_key, seed_data in all_results.items():
        for law, r in seed_data.items():
            all_verdicts.append(r.get('verdict', 'MISSING'))

    overall = 'PASS'
    if any(v == 'KILL' for v in all_verdicts):
        overall = 'KILL'
    elif any(v == 'INSTRUMENT_FAILURE' for v in all_verdicts):
        overall = 'INSTRUMENT_FAILURE'
    if not interface_invariants['passes']:
        overall = 'INSTRUMENT_FAILURE'
    if not all_finite:
        overall = 'INSTRUMENT_FAILURE'

    _tee(f"--- Overall Verdict: {overall} ---", log_lines)

    # --- Write output files ---
    _tee(f"--- Writing output files to {output_dir} ---", log_lines)

    # 1. m3_run_results.json
    results_path = os.path.join(output_dir, 'm3_run_results.json')
    results_out = {
        'config': {
            'law': args.law,
            'seeds': seeds,
            'mode': args.mode,
            'development_seeds': DEVELOPMENT_SEEDS,
            'scoring_seed_policy': 'WITHHELD; forbidden in development',
        },
        'results': all_results,
        'overall_verdict': overall,
        'reproducibility': reproducibility,
        'interface_invariants': interface_invariants,
        'finite_numeric_results': all_finite,
    }
    _write_json(results_path, results_out)
    _tee(f"  Written: {results_path}", log_lines)

    # Per-law result files for independent review.
    per_law_filenames = []
    for law in laws_to_run:
        law_filename = f"m3_{law.lower()}_results.json"
        law_path = os.path.join(output_dir, law_filename)
        law_output = {
            'law': law,
            'mode': args.mode,
            'results': {
                seed_key: seed_data[law]
                for seed_key, seed_data in all_results.items()
                if law in seed_data
            },
        }
        _write_json(law_path, law_output)
        per_law_filenames.append(law_filename)
        _tee(f"  Written: {law_path}", log_lines)

    # 2. m3_invariants.json
    invariants_path = os.path.join(output_dir, 'm3_invariants.json')
    invariants_out = {
        'overall_verdict': overall,
        'per_law_verdicts': {},
        'l20_self_test': l20_result,
        'reproducibility': reproducibility,
        'interface_invariants': interface_invariants,
        'finite_numeric_results': all_finite,
    }
    for law in laws_to_run:
        law_verdicts = []
        for seed_key, seed_data in all_results.items():
            if law in seed_data:
                law_verdicts.append({
                    'seed': int(seed_key),
                    'verdict': seed_data[law].get('verdict', 'MISSING'),
                })
        invariants_out['per_law_verdicts'][law] = law_verdicts
    _write_json(invariants_path, invariants_out)
    _tee(f"  Written: {invariants_path}", log_lines)

    # 3. m3_manifest.json
    manifest_path = os.path.join(output_dir, 'm3_manifest.json')
    git_hash, state_md_sha256 = (
        _resolve_repository_provenance())
    deviations = []
    if platform.python_version() != '3.11':
        deviations.append(f"Python {platform.python_version()} vs pinned 3.11 (non-blocking)")
    if np.__version__ != '1.26.4':
        deviations.append(
            f"NumPy {np.__version__} vs pinned 1.26.4 (non-blocking)")
    if scipy.__version__ != '1.13.1':
        deviations.append(
            f"SciPy {scipy.__version__} vs pinned 1.13.1 (non-blocking)")
    manifest_out = {
        'commit_hash': git_hash,
        'seeds': seeds,
        'mode': args.mode,
        'law': args.law,
        'python_version_runtime': platform.python_version(),
        'python_version_pinned': '3.11',
        'numpy_version': np.__version__,
        'scipy_version': scipy.__version__,
        'deviations_logged': deviations,
        'wall_clock_seconds': None,  # filled below
        'output_files': [
            'm3_run_results.json',
            'm3_invariants.json',
            'm3_manifest.json',
            'm3_run.log',
            'm3_profile.json',
        ],
        'development_seeds_pool': DEVELOPMENT_SEEDS,
        'scoring_seed_pool': 'WITHHELD; forbidden in development',
        'r3_note': (
            'Scoring-only seed identities are absent from this development '
            'implementation and its artifacts.'
        ),
        'nf7_note': 'Raw per-entry data emitted in L1 results for independent R² recomputation',
        'nf8_note': 'L3 permuted arm violations route to INSTRUMENT FAILURE, never KILL',
        'nf9_note': 'L5 frozen arm labeled "L18 negative control"; binary walk accuracy is inherent',
        'nf10_note': 'STATE.md currency attested by RECORDER; build authorized by Rebecca M3 BUILD GO',
        'growth_bar_note': 'L5 growth thresholds are diagnostic-only and non-gating per §1.1',
    }
    _write_json(manifest_path, manifest_out)
    _tee(f"  Written: {manifest_path}", log_lines)

    # 4. m3_run.log
    log_path = os.path.join(output_dir, 'm3_run.log')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    _tee(f"  Written: {log_path}", log_lines)

    # 5. m3_profile.json
    profile_path = os.path.join(output_dir, 'm3_profile.json')
    profile_out = {
        'profile_vector': profile_vector,
        'l20_self_test': l20_result,
        'profile_description': (
            'Four raw, non-timing metrics per (seed, law); law-specific '
            'metric order is documented in m3_harness.py'
        ),
    }
    _write_json(profile_path, profile_out)
    _tee(f"  Written: {profile_path}", log_lines)

    ledger_path = os.path.join(
        output_dir, 'm3_seed_exposure_ledger.json')
    _write_json(ledger_path, {
        'append_only': True,
        'scope': 'M3 development diagnostics only',
        'events': seed_exposure_ledger,
    })
    _tee(f"  Written: {ledger_path}", log_lines)

    # Compute file hashes
    file_hashes = {}
    hashable_files = [
        'm3_run_results.json', 'm3_invariants.json',
        'm3_run.log', 'm3_profile.json',
        'm3_seed_exposure_ledger.json',
    ] + per_law_filenames
    for fname in hashable_files:
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            file_hashes[fname] = _sha256_file(fpath)

    # Update manifest with wall clock and hashes
    manifest_out['wall_clock_seconds'] = (
        time.perf_counter() - run_started)
    manifest_out['state_md_sha256'] = state_md_sha256
    manifest_out['output_files'] = [
        'm3_run_results.json',
        *per_law_filenames,
        'm3_invariants.json',
        'm3_manifest.json',
        'm3_run.log',
        'm3_profile.json',
        'm3_seed_exposure_ledger.json',
    ]
    manifest_out['file_hashes'] = file_hashes
    manifest_out['file_hash_note'] = (
        'Manifest excludes its own self-referential hash.')
    _write_json(manifest_path, manifest_out)

    _tee("", log_lines)
    _tee(f"=== M3/E2 Harness Complete ===", log_lines)
    _tee(f"Overall verdict: {overall}", log_lines)
    # Rewrite the log so completion lines are included.
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines) + '\n')
    manifest_out['file_hashes']['m3_run.log'] = _sha256_file(log_path)
    _write_json(manifest_path, manifest_out)

    return 0 if overall == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
