#!/usr/bin/env python3
"""Reproducibility-contract test suite for M3 (§5.1, §5.2, §6.2).

Implements:
  - §5.1 Automated leaf-traversal mutation tests (L1, L3, L5, L6)
  - Fail-closed projection tests (unknown fields, missing required fields,
    Classification C invariants)
  - Non-digest field tests (Classification B invariance, key-order
    invariance, Classification C exclusion from digest)
  - Final-report (non-compared) digest mutation tests
  - Stale-label regression tests (§6.2 mode-aware labels)

All tests use synthetic in-memory fixtures — no harness run required.
"""
import unittest
import copy
import json
import hashlib
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import m3_reproducibility as rep
import m3_harness as m3  # noqa: F401  (imported per contract; ensures module loads)
import numpy as np  # noqa: F401  (required dependency of m3_reproducibility)


# ---------------------------------------------------------------------------
# Config helper
# ---------------------------------------------------------------------------

def _make_config():
    """Return a fresh minimal config dict (§2.3)."""
    return {
        'projection_schema_version': 'm3_scoring_semantic_reproducibility_v1',
        'mode': 'development',
        'seeds': [101],
        'laws_selected': ['L1'],
        'protocol_id': 'M3-V4.4-SHA256-CTR-FY-v1',
        'null_replicate_count': 1000,
        'alpha_family': 0.05,
        'alpha_seed': 0.05 / 3.0,
        'locked_bars': {},
        'stochastic_families_by_law': {},
        'seed_policy': [101, 102, 103, 104, 105],
    }


# ---------------------------------------------------------------------------
# V4.4 summary helper
# ---------------------------------------------------------------------------

def _make_v44_summary(observed, direction, extra=None):
    """Build a minimal V4.4 stochastic-control summary (§2.5)."""
    s = {
        'protocol_id': 'M3-V4.4-SHA256-CTR-FY-v1',
        'null_replicate_count': 1000,
        'meaningful_failure_direction': direction,
        'observed_statistic': float(observed),
        'null_statistics': [float(observed)] * 3,
        'null_upper_order_statistic_985': float(observed),
        'exceed_or_tie_count': 1,
        'plus_one_p_value': 0.25,
        'alpha_family': 0.05,
        'alpha_seed': 0.05 / 3.0,
        'per_seed_pass': True,
        'rng_derivation_records': [],
        'rng_derivation_summaries': [
            {
                'rng_protocol_id': 'M3-V4.4-SHA256-CTR-FY-v1',
                'hash': 'SHA-256',
                'root_domain_hex': 'abc',
                'law': 'L1',
                'arm': 'frozen',
                'draw_role': 'OBSERVED',
                'scoring_seed': 101,
                'replicate_index': 0,
                'subdraw_index': 0,
                'derived_key_hex': 'def',
                'stream_key_hex': 'def',
                'accepted_permutation': None,
                'rejection_count': 0,
                'stream_block_count': 1,
                'stream_word_count': 1,
                'sha256_digest': 'ghi',
            }
        ],
    }
    if extra:
        s.update(extra)
    return s


# ---------------------------------------------------------------------------
# Synthetic law-result fixtures
# ---------------------------------------------------------------------------

def _make_l1_result():
    """Minimal valid L1 result dict (V4.4 structure)."""
    arm_fields = {
        'r_squared': 0.99,
        'beta_age': -0.001,
        'bin_means': [0.1] * 5,
        'bin_age_representatives': [1.0] * 5,
        'conditional_rhos': [0.7] * 5,
        'age_conditional_slopes': [-0.01] * 5,
        'log_accessibility': {str(i): 0.5 for i in range(5)},
        'priority_values': [0.5] * 5,
    }

    def _arm(r_squared, beta_age, rhos, slopes, with_ranks=False):
        a = {
            'r_squared': r_squared,
            'beta_age': beta_age,
            'bin_means': [0.1] * 5,
            'bin_age_representatives': [1.0] * 5,
            'conditional_rhos': [rhos] * 5,
            'age_conditional_slopes': [slopes] * 5,
            'log_accessibility': {str(i): 0.5 for i in range(5)},
            'priority_values': [0.5] * 5,
        }
        if with_ranks:
            a['per_set_ranks'] = {
                '0': [[i, i] for i in range(5)],
            }
        return a

    return {
        'seed': 101,
        'law': 'L1',
        'verdict': 'PASS',
        'kill_reasons': [],
        'instrument_failure_reasons': [],
        'candidate': _arm(0.99, -0.001, 0.7, -0.01, with_ranks=True),
        'oracle': _arm(0.99, -0.001, 0.7, -0.01, with_ranks=True),
        'frozen': _arm(0.236, 0.0, 0.3, 0.0),
        'fair_naive': _arm(0.320, 0.0, 0.3, 0.0),
        'recency_only': _arm(0.85, -0.001, 0.6, -0.01),
        'rehearsal_only': _arm(0.85, 0.5, 0.6, -0.01),
        'shuffled': _arm(0.1, 0.0, 0.1, 0.0),
        'permuted': {
            'spearman_rho_200entry': -0.01,
            'rho_null_p95': 0.12,
            'null_p95_le_0_15': True,
            'plus_one_p_value': 0.5,
            'within_mean_pm_2sd_band': True,
            'diagnostic_5bin_r_squared_non_gating': None,
        },
        'empty': {
            'returned_defined_error': True,
            'observed': {'error': 'empty_fixture'},
        },
        'v44_stochastic_controls': {
            'frozen': _make_v44_summary(
                0.236, 'upper',
                {'r_squared_observed': 0.236,
                 'draw_role_observed': {
                     'ranking_permutation_200': list(range(5)),
                     'r_squared': 0.236}},
            ),
            'fair_naive': _make_v44_summary(
                0.320, 'upper',
                {'r_squared_observed': 0.320,
                 'draw_role_observed': {
                     'ranking_permutation_200': list(range(5)),
                     'r_squared': 0.320}},
            ),
            'permuted': _make_v44_summary(
                0.01, 'two_sided_magnitude',
                {'spearman_rho_200entry': -0.01,
                 'null_abs_rho_p95': 0.12,
                 'null_p95_le_0_15': True,
                 'observed_mapping_permutation_200': list(range(5)),
                 'paired_age_accessibility_200': [
                     {'entry_id': i, 'age': float(i),
                      'accessibility': 0.5} for i in range(5)],
                 },
            ),
            'shuffled': _make_v44_summary(
                0.3, 'upper',
                {'conditional_rho_values_5': [0.3] * 5,
                 'rho_null_1000x5': [[0.1] * 5] * 3,
                 'null_max_1000': [0.1] * 3,
                 'observed_max': 0.3,
                 'age_tests_pass': True,
                 'below_threshold_labels': [],
                 'observed_query_to_entry_assignment_1200': list(range(10)),
                 'observed_realized_rehearsal_counts_200': [1] * 5},
            ),
        },
        'v44_deterministic_controls': {
            'recency_only': {
                'r_squared': 0.85, 'beta_age': -0.001,
                'conditional_rho_5': [0.6] * 5,
                'structural_fixture_hash': 'abc123',
                'candidate_set_schedule_hash': 'def456',
                'deterministic_reproduction_equal_across_seed_slots': True,
                'all_exact_checks_pass': True,
                'cross_slot_hashes': ['h1', 'h2', 'h3'],
            },
            'rehearsal_only': {
                'beta_age': 0.5,
                'conditional_rho_5': [0.6] * 5,
                'structural_fixture_hash': 'abc123',
                'candidate_set_schedule_hash': 'def456',
                'deterministic_reproduction_equal_across_seed_slots': True,
                'all_exact_checks_pass': True,
                'cross_slot_hashes': ['h1', 'h2', 'h3'],
            },
            'oracle': {
                'r_squared': 0.99, 'beta_age': -0.001,
                'conditional_rho_5': [0.7] * 5,
                'structural_fixture_hash': 'abc123',
                'candidate_set_schedule_hash': 'def456',
                'all_exact_checks_pass': True,
            },
            'empty': {
                'returned_defined_error': True,
                'numeric_result_absent': True,
            },
        },
        'v44_artifact_support': {
            'status': 'in_memory_test_mode',
            'raw_array_writer': 'm3_v44_raw_manifest.json',
            'full_per_draw_raw_schema_complete': False,
        },
    }


def _make_l3_result():
    """Minimal valid L3 result dict (V4.4 structure)."""
    return {
        'seed': 101,
        'law': 'L3',
        'verdict': 'PASS',
        'kill_reasons': [],
        'instrument_failure_reasons': [],
        'reductions': {str(i): 0.1 for i in range(1, 6)},
        'frozen_reductions': {str(i): 0.05 for i in range(1, 6)},
        'oracle_reductions': {str(i): 0.1 for i in range(1, 6)},
        'permuted_reductions': {str(i): 0.05 for i in range(1, 6)},
        'shuffled_reductions': {str(i): 0.05 for i in range(1, 6)},
        'shuffled_frozen_reductions': {str(i): 0.05 for i in range(1, 6)},
        'empty': {'returned_defined_error': True},
        'v44_stochastic_controls': {
            'frozen': _make_v44_summary(
                0.1, 'upper',
                {'observed_reductions_5': [0.05] * 5,
                 'observed_violation_score_5': [0.0] * 5},
            ),
            'oracle': _make_v44_summary(
                0.1, 'upper',
                {'observed_reductions_5': [0.1] * 5,
                 'observed_violation_score_5': [0.0] * 5},
            ),
            'permuted': _make_v44_summary(
                0.1, 'upper',
                {'observed_reductions_5': [0.05] * 5,
                 'observed_violation_score_5': [0.0] * 5},
            ),
            'shuffled': _make_v44_summary(
                0.1, 'upper',
                {'observed_reductions_5': [0.05] * 5,
                 'observed_violation_score_5': [0.0] * 5},
            ),
        },
        'v44_artifact_support': {
            'status': 'in_memory_test_mode',
            'raw_array_writer': 'm3_v44_raw_manifest.json',
            'full_per_draw_raw_schema_complete': False,
        },
    }


def _make_l5_result():
    """Minimal valid L5 result dict (V4.4 structure)."""
    chain_row = {
        'chain_id': 0,
        'query_type': 'full',
        'k': 10,
        'visited': [0, 1],
        'expected': [0, 1],
        'accuracy': 1.0,
        'access_count_delta': 10,
        'access_count_matches_k': True,
    }
    return {
        'seed': 101,
        'law': 'L5',
        'verdict': 'PASS',
        'kill_reasons': [],
        'instrument_failure_reasons': [],
        'candidate': {
            'world_validity_accuracy': 1.0,
            'self_acquisition_accuracy': 1.0,
            'chain_walk_accuracy': 1.0,
            'access_count_matches_k': True,
        },
        'fair_naive': {
            'combo_accuracy_world_validity': 0.75,
            'chain_walk_accuracy': 'N/A',
        },
        'frozen': {
            'chain_walk_accuracy_post_freeze': 0.0,
            'label': 'L18 negative control',
            'chain_walk_results': [chain_row],
        },
        'oracle': {
            'world_validity_accuracy': 1.0,
            'self_acquisition_accuracy': 1.0,
            'chain_walk_accuracy': 1.0,
            'chain_walk_results': [chain_row],
        },
        'permuted': {
            'combo_accuracy': 0.5,
            'chain_content_mismatch_rate': 1.0,
            'plus_one_p_value': 0.5,
            'pooled_center': 0.5,
        },
        'shuffled': {
            'combo_query_order_accuracy': 1.0,
            'self_acquisition_query_order_accuracy': 1.0,
            'query_order_equal_to_original': True,
            'chain_walk_accuracy': 0.0,
            'edge_count': 180,
            'chain_walk_results': [chain_row],
        },
        'full_scan': {
            'chain_walk_accuracy': 1.0,
            'access_count_deltas': [10],
            'chain_walk_results': [chain_row],
            'log': 'chain_fixture_separate',
        },
        'empty': {
            'combination_returned_defined_error': True,
            'chain_returned_defined_error': True,
        },
        'v44_stochastic_controls': {
            'permuted': _make_v44_summary(
                0.1, 'two_sided_magnitude',
                {'observed_accuracy': 0.5,
                 'null_accuracies_1000': [0.5] * 3,
                 'pooled_center': 0.5,
                 'observed_absolute_departure': 0.0,
                 'null_absolute_departures_1000': [0.0] * 3,
                 'chain_content_mismatch_rate': 1.0,
                 'field_mapping_derangement_200': list(range(5)),
                 'chain_content_derangement_200': list(range(5)),
                 'query_results_200': [
                     {'query_id': 0, 'prediction': True,
                      'truth': True, 'correct': True}],
                 },
            ),
        },
        'v44_artifact_support': {
            'status': 'in_memory_test_mode',
            'raw_array_writer': 'm3_v44_raw_manifest.json',
            'full_per_draw_raw_schema_complete': False,
        },
    }


def _make_l6_result():
    """Minimal valid L6 result dict (V4.4 structure)."""
    return {
        'seed': 101,
        'law': 'L6',
        'reachability_audit': [
            {
                'module': 'episodic_store',
                'callable_name': 'read',
                'return_type_observed': 'dict',
                'is_tagged_union': True,
                'verdict': 'pass',
            }
        ],
        'module_public_names': {
            'episodic_store': ['read', 'write'],
        },
        'module_namespace_complete': True,
        'attacks': [
            {
                'attack_id': 1,
                'path_type': 'direct',
                'caught': True,
                'diagnosis': 'blocked',
            }
        ],
        'l18_arms': {
            'empty': {'expected': True, 'observed': True, 'pass': True},
        },
        'verdict': 'PASS',
        'kill_reasons': [],
        'instrument_failure_reasons': [],
    }


_FIXTURE_BUILDERS = {
    'L1': _make_l1_result,
    'L3': _make_l3_result,
    'L5': _make_l5_result,
    'L6': _make_l6_result,
}


# ---------------------------------------------------------------------------
# Mutation helpers
# ---------------------------------------------------------------------------

def _mutate_value(val):
    """Return a mutated copy of *val* (§5.1 mutation rules)."""
    if isinstance(val, bool):
        return not val
    elif isinstance(val, (int, float)):
        return val + 1e-9
    elif isinstance(val, str):
        return val + 'x'
    elif isinstance(val, list):
        return val + [0] if val else [0]
    elif isinstance(val, dict):
        return {**val, '_mutation_key': 0}
    elif val is None:
        return 0
    return val


def _collect_leaf_paths(obj, path=()):
    """Recursively yield every leaf path in *obj*.

    Leaves are scalars (including ``None``) and empty containers.
    Non-empty dicts and lists are recursed into.
    """
    if isinstance(obj, dict):
        if not obj:
            yield path
        else:
            for k, v in obj.items():
                yield from _collect_leaf_paths(v, path + (k,))
    elif isinstance(obj, list):
        if not obj:
            yield path
        else:
            for i, v in enumerate(obj):
                yield from _collect_leaf_paths(v, path + (i,))
    else:
        yield path


def _set_at_path(root, path, value):
    """Navigate *root* along *path* (minus the final element) and set
    ``value`` at the terminal key/index."""
    node = root
    for part in path[:-1]:
        node = node[part]
    node[path[-1]] = value


def _get_at_path(root, path):
    """Return the value at *path* in *root*."""
    node = root
    for part in path:
        node = node[part]
    return node


# ---------------------------------------------------------------------------
# §5.1 — Automated leaf-traversal mutation tests
# ---------------------------------------------------------------------------

class MutationTestLeafTraversal(unittest.TestCase):
    """For each law, traverse every Classification A leaf, mutate it, and
    assert the compared digest changes (or a Classification C invariant
    fires — an even stronger detection)."""

    def _run_mutation_test(self, law):
        config = _make_config()
        fixture = _FIXTURE_BUILDERS[law]()
        results = {'101': {law: fixture}}
        orig_digest, proj = rep.compute_scoring_semantic_digest(
            copy.deepcopy(results), config)
        law_proj = proj['laws']['101'][law]
        paths = list(_collect_leaf_paths(law_proj))
        self.assertGreater(len(paths), 0,
                           f'no Classification A leaf paths for {law}')
        for path in paths:
            rc = copy.deepcopy(results)
            orig_val = _get_at_path(rc['101'][law], path)
            _set_at_path(rc['101'][law], path, _mutate_value(orig_val))
            try:
                new_digest, _ = rep.compute_scoring_semantic_digest(
                    rc, config)
            except rep.ReproducibilityInvariantError:
                # The mutation was caught by a Classification C invariant
                # check — this is a stronger guarantee than a digest change.
                continue
            self.assertNotEqual(
                new_digest, orig_digest,
                f'mutation at {law}:{path} did not change digest '
                f'(value was {orig_val!r})')

    def test_l1_leaf_mutation(self):
        self._run_mutation_test('L1')

    def test_l3_leaf_mutation(self):
        self._run_mutation_test('L3')

    def test_l5_leaf_mutation(self):
        self._run_mutation_test('L5')

    def test_l6_leaf_mutation(self):
        self._run_mutation_test('L6')


# ---------------------------------------------------------------------------
# Fail-closed projection tests
# ---------------------------------------------------------------------------

class FailClosedTests(unittest.TestCase):
    """Verify the fail-closed enforcement (§3.4 / §5.2)."""

    def test_unknown_field_raises(self):
        """An unclassified top-level field must raise."""
        config = _make_config()
        results = {'101': {'L1': _make_l1_result()}}
        results['101']['L1']['unexpected_field'] = 'x'
        with self.assertRaises(rep.ReproducibilityProjectionError):
            rep.compute_scoring_semantic_digest(results, config)

    def test_missing_required_field_raises(self):
        """Spec §5.2: removing a Classification A field must raise."""
        config = _make_config()
        results = {'101': {'L1': _make_l1_result()}}
        del results['101']['L1']['verdict']
        with self.assertRaises(rep.ReproducibilityProjectionError):
            rep.compute_scoring_semantic_digest(results, config)

    def test_classification_c_invariant_rho_null(self):
        """permuted.rho_null_1000_values must match abs(null_statistics)."""
        config = _make_config()
        results = {'101': {'L1': _make_l1_result()}}
        results['101']['L1']['permuted']['rho_null_1000_values'] = \
            [0.5, 0.5, 0.5]
        with self.assertRaises(rep.ReproducibilityInvariantError):
            rep.compute_scoring_semantic_digest(results, config)

    def test_classification_c_invariant_abs_rho(self):
        """abs_rho_null_1000 must equal null_statistics."""
        config = _make_config()
        results = {'101': {'L1': _make_l1_result()}}
        results['101']['L1']['v44_stochastic_controls']['permuted'][
            'abs_rho_null_1000'] = [0.5, 0.5, 0.5]
        with self.assertRaises(rep.ReproducibilityInvariantError):
            rep.compute_scoring_semantic_digest(results, config)

    def test_classification_c_invariant_null_max(self):
        """null_max_1000 must match max of each rho_null_1000x5 row."""
        config = _make_config()
        results = {'101': {'L1': _make_l1_result()}}
        results['101']['L1']['v44_stochastic_controls']['shuffled'][
            'null_max_1000'] = [0.5, 0.5, 0.5]
        with self.assertRaises(rep.ReproducibilityInvariantError):
            rep.compute_scoring_semantic_digest(results, config)


# ---------------------------------------------------------------------------
# Non-digest field tests
# ---------------------------------------------------------------------------

class NonDigestFieldTests(unittest.TestCase):
    """Classification B and C fields must not affect the compared digest."""

    def test_artifact_field_change_doesnt_alter_digest(self):
        """Changing a Classification B field (v44_artifact_support) must
        not change the compared digest."""
        config = _make_config()
        r1 = {'101': {'L1': _make_l1_result()}}
        r2 = {'101': {'L1': _make_l1_result()}}
        r2['101']['L1']['v44_artifact_support']['status'] = 'changed'
        d1, _ = rep.compute_scoring_semantic_digest(r1, config)
        d2, _ = rep.compute_scoring_semantic_digest(r2, config)
        self.assertEqual(d1, d2)

    def test_key_order_doesnt_alter_digest(self):
        """Canonical serialization sorts keys, so insertion order is
        irrelevant."""
        config = _make_config()
        r1 = {'101': {'L1': _make_l1_result()}}
        d1, _ = rep.compute_scoring_semantic_digest(r1, config)
        # Rebuild L1 dict with reversed key order
        l1 = r1['101']['L1']
        reordered = {k: l1[k] for k in reversed(list(l1.keys()))}
        r2 = {'101': {'L1': reordered}}
        d2, _ = rep.compute_scoring_semantic_digest(r2, config)
        self.assertEqual(d1, d2)

    def test_classification_c_mutation_doesnt_alter_digest(self):
        """A Classification C field (abs_rho_null_1000) is excluded from
        the compared digest, but its invariant check must still catch a
        mismatch."""
        config = _make_config()
        results = {'101': {'L1': _make_l1_result()}}
        l1 = results['101']['L1']
        null_stats = l1['v44_stochastic_controls']['permuted'][
            'null_statistics']
        # Add matching abs_rho_null_1000 so invariant passes
        l1['v44_stochastic_controls']['permuted']['abs_rho_null_1000'] = \
            list(null_stats)
        d1, proj = rep.compute_scoring_semantic_digest(
            copy.deepcopy(results), config)
        # Classification C field is NOT in the projection
        self.assertNotIn(
            'abs_rho_null_1000',
            proj['laws']['101']['L1']['v44_stochastic_controls']['permuted'])
        # Mutate to a wrong value
        l1['v44_stochastic_controls']['permuted']['abs_rho_null_1000'] = \
            [x + 1.0 for x in null_stats]
        # Invariant must catch it
        with self.assertRaises(rep.ReproducibilityInvariantError):
            rep.compute_scoring_semantic_digest(
                copy.deepcopy(results), config)


# ---------------------------------------------------------------------------
# Final-report (non-compared) digest tests
# ---------------------------------------------------------------------------

def _make_final_report_kwargs():
    """Return default kwargs for compute_final_report_digest."""
    return {
        'compared_payload': {
            'projection_schema_version':
                'm3_scoring_semantic_reproducibility_v1',
            'config': {},
            'laws': {},
        },
        'pass1_digest': 'aaa111',
        'pass2_digest': 'aaa111',
        'digests_equal': True,
        'reproducibility': {'passes': True, 'mode': 'development'},
        'interface_invariants': {'all_passed': True, 'count': 12},
        'finite_numeric_results': True,
        'l20_self_test': {'ran': True, 'passed': True, 'checks': 5},
        'raw_artifact_validation': {
            'validated': True, 'files_checked': 3},
        'overall_verdict': 'PASS',
    }


class FinalReportDigestTests(unittest.TestCase):
    """Mutating any field in the non-compared final-report bundle must
    change its digest."""

    def test_overall_verdict_mutation_changes_final_digest(self):
        kw = _make_final_report_kwargs()
        d1 = rep.compute_final_report_digest(**kw)
        kw['overall_verdict'] = 'FAIL'
        d2 = rep.compute_final_report_digest(**kw)
        self.assertNotEqual(d1, d2)

    def test_interface_invariants_mutation_changes_final_digest(self):
        kw = _make_final_report_kwargs()
        d1 = rep.compute_final_report_digest(**kw)
        kw['interface_invariants'] = {'all_passed': False, 'count': 12}
        d2 = rep.compute_final_report_digest(**kw)
        self.assertNotEqual(d1, d2)

    def test_l20_self_test_mutation_changes_final_digest(self):
        kw = _make_final_report_kwargs()
        d1 = rep.compute_final_report_digest(**kw)
        kw['l20_self_test'] = {'ran': True, 'passed': False, 'checks': 5}
        d2 = rep.compute_final_report_digest(**kw)
        self.assertNotEqual(d1, d2)

    def test_raw_artifact_validation_mutation_changes_final_digest(self):
        kw = _make_final_report_kwargs()
        d1 = rep.compute_final_report_digest(**kw)
        kw['raw_artifact_validation'] = {
            'validated': False, 'files_checked': 3}
        d2 = rep.compute_final_report_digest(**kw)
        self.assertNotEqual(d1, d2)


# ---------------------------------------------------------------------------
# §6.2 — Stale-label regression tests
# ---------------------------------------------------------------------------

class StaleLabelRegressionTests(unittest.TestCase):
    """Guard against stale mode-aware labels leaking between modes."""

    def test_scoring_mode_labels(self):
        """Scoring-mode labels must never reference 'development'."""
        scope = rep.mode_label('scoring', 'scope')
        self.assertNotIn('development', scope)
        pool = rep.mode_label('scoring', 'scoring_seed_pool')
        self.assertNotIn('development', pool)

    def test_development_mode_labels(self):
        """Development-mode labels must carry the diagnostic-only
        disclaimer and the seed-pool withholding notice."""
        scope = rep.mode_label('development', 'scope')
        self.assertIn('development diagnostics only', scope)
        pool = rep.mode_label('development', 'scoring_seed_pool')
        self.assertIn('WITHHELD; forbidden in development', pool)


if __name__ == '__main__':
    unittest.main(verbosity=2)
