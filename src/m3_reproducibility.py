"""M3 Reproducibility-Contract v1 implementation.

Implements the CRITIC-cleared reproducibility-contract specification v1.1
(specs/m3_reproducibility_contract_v1.md at SHA 3c8480c).

Two-digest architecture:
  - Digest 1 (compared): per-law results + configuration only.
  - Digest 2 (non-compared): complete output bundle integrity hash.

Fail-closed: any field not in Classification A, B, or C triggers
ReproducibilityProjectionError.
"""
from __future__ import annotations

import hashlib
import json
import math
import unicodedata
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ReproducibilityProjectionError(Exception):
    """Raised when a field is not found in any classification (A, B, or C)."""

    def __init__(self, path: str, value_type: str):
        self.path = path
        self.value_type = value_type
        super().__init__(
            f"Unclassified field at '{path}' (type={value_type}). "
            f"Update the projection classification or remove the field.")


class ReproducibilityInvariantError(Exception):
    """Raised when a Classification C invariant check fails."""

    def __init__(self, duplicate_path: str, canonical_path: str,
                 duplicate_value: Any, canonical_value: Any):
        self.duplicate_path = duplicate_path
        self.canonical_path = canonical_path
        self.duplicate_value = duplicate_value
        self.canonical_value = canonical_value
        super().__init__(
            f"Classification C invariant failed: '{duplicate_path}' does not "
            f"match canonical '{canonical_path}'. "
            f"Duplicate={duplicate_value!r}, Canonical={canonical_value!r}")


# ---------------------------------------------------------------------------
# Canonical serialization (§3.3)
# ---------------------------------------------------------------------------

def _normalize_value(value: Any) -> Any:
    """NFC-normalize strings, convert numpy scalars, check finiteness."""
    if isinstance(value, str):
        return unicodedata.normalize('NFC', value)
    if isinstance(value, dict):
        return {str(_normalize_value(k)): _normalize_value(v)
                for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_value(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"non-finite float in reproducibility projection: {value}")
        return value
    if isinstance(value, bool):
        return value
    return value


def canonical_bytes(value: Any) -> bytes:
    """Serialize to canonical JSON bytes per §3.3."""
    normalized = _normalize_value(value)
    return json.dumps(
        normalized, ensure_ascii=True, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode('utf-8')


def canonical_digest(value: Any) -> str:
    """Compute SHA-256 hex digest of canonical serialization."""
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


# ---------------------------------------------------------------------------
# Normalized RNG derivation summary (§2.5)
# ---------------------------------------------------------------------------

_RNG_SUMMARY_FIELDS = (
    'rng_protocol_id', 'hash', 'root_domain_hex', 'law', 'arm',
    'draw_role', 'scoring_seed', 'replicate_index', 'subdraw_index',
    'derived_key_hex', 'stream_key_hex', 'accepted_permutation',
    'rejection_count', 'stream_block_count', 'stream_word_count',
    'sha256_digest',
)


def normalize_rng_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Extract normalized RNG derivation summary fields from an artifact record."""
    return {field: record[field] for field in _RNG_SUMMARY_FIELDS
            if field in record}


def build_rng_derivation_summaries(
    records: Sequence[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Build a list of normalized RNG summaries from artifact record dicts."""
    return [normalize_rng_record(r) for r in records]


# ---------------------------------------------------------------------------
# Classification tables
# ---------------------------------------------------------------------------

# --- L1 Classification A ---

_L1_TOP_LEVEL_A = frozenset({
    'seed', 'law', 'verdict', 'kill_reasons', 'instrument_failure_reasons',
})

_L1_TOP_LEVEL_B = frozenset({
    'v44_artifact_support',
})

# Standard arm fields (candidate, oracle, frozen, fair_naive, recency_only,
# rehearsal_only, shuffled) — all have the same structure from _l1_run_arm
_L1_ARM_A = frozenset({
    'r_squared', 'beta_age', 'bin_means', 'bin_age_representatives',
    'conditional_rhos', 'age_conditional_slopes', 'log_accessibility',
    'priority_values',
})

# per_set_ranks is A in candidate/oracle, B elsewhere
_L1_ARM_PER_SET_RANKS_A = frozenset({'candidate', 'oracle'})

# Permuted arm (top-level, not V4.4 stochastic control)
_L1_PERMUTED_A = frozenset({
    'spearman_rho_200entry', 'rho_null_p95', 'null_p95_le_0_15',
    'plus_one_p_value', 'within_mean_pm_2sd_band',
    'diagnostic_5bin_r_squared_non_gating',
})
_L1_PERMUTED_C = frozenset({'rho_null_1000_values'})

# Empty arm
_L1_EMPTY_A = frozenset({'returned_defined_error', 'observed'})

# V4.4 stochastic controls — base summary fields (all families)
_V44_SUMMARY_A = frozenset({
    'protocol_id', 'null_replicate_count', 'meaningful_failure_direction',
    'observed_statistic', 'null_statistics', 'null_upper_order_statistic_985',
    'exceed_or_tie_count', 'plus_one_p_value', 'alpha_family', 'alpha_seed',
    'per_seed_pass', 'rng_derivation_summaries',
})

_V44_SUMMARY_B = frozenset({
    'rng_derivation_records', 'raw_draw_manifest_refs',
})

# L1 V4.4 stochastic family-specific extras (Classification A)
_L1_V44_FROZEN_FAIR_NAIVE_EXTRA_A = frozenset({
    'r_squared_observed', 'draw_role_observed',
})
_L1_V44_FROZEN_FAIR_NAIVE_EXTRA_C = frozenset({'r_squared_null_1000'})

_L1_V44_PERMUTED_EXTRA_A = frozenset({
    'spearman_rho_200entry', 'null_abs_rho_p95', 'null_p95_le_0_15',
    'observed_mapping_permutation_200', 'paired_age_accessibility_200',
})
_L1_V44_PERMUTED_EXTRA_C = frozenset({'abs_rho_null_1000'})

_L1_V44_SHUFFLED_EXTRA_A = frozenset({
    'conditional_rho_values_5', 'rho_null_1000x5', 'observed_max',
    'age_tests_pass', 'below_threshold_labels',
    'observed_query_to_entry_assignment_1200',
    'observed_realized_rehearsal_counts_200',
})
_L1_V44_SHUFFLED_EXTRA_C = frozenset({'null_max_1000'})

# L1 V4.4 deterministic controls
_L1_V44_DET_RECENCY_A = frozenset({
    'r_squared', 'beta_age', 'conditional_rho_5', 'structural_fixture_hash',
    'candidate_set_schedule_hash',
    'deterministic_reproduction_equal_across_seed_slots',
    'all_exact_checks_pass', 'cross_slot_hashes',
})
_L1_V44_DET_REHEARSAL_A = frozenset({
    'beta_age', 'conditional_rho_5', 'structural_fixture_hash',
    'candidate_set_schedule_hash',
    'deterministic_reproduction_equal_across_seed_slots',
    'all_exact_checks_pass', 'cross_slot_hashes',
})
_L1_V44_DET_ORACLE_A = frozenset({
    'r_squared', 'beta_age', 'conditional_rho_5', 'structural_fixture_hash',
    'candidate_set_schedule_hash', 'all_exact_checks_pass',
})
_L1_V44_DET_EMPTY_A = frozenset({
    'returned_defined_error', 'numeric_result_absent',
})

# "where present" fields — conditionally absent, valid
_L1_WHERE_PRESENT = frozenset({
    'deterministic_reproduction_equal_across_seed_slots',
    'cross_slot_hashes', 'all_exact_checks_pass',
    'per_set_ranks',  # only in candidate/oracle
    'rho_null_1000_values',  # only when artifact_writer is None
    'r_squared_null_1000',  # only when artifact_writer is None
    'abs_rho_null_1000',  # Classification C
    'null_max_1000',  # Classification C
})

# --- L3 Classification A ---

_L3_TOP_LEVEL_A = frozenset({
    'seed', 'law', 'verdict', 'kill_reasons', 'instrument_failure_reasons',
})
_L3_TOP_LEVEL_B = frozenset({'v44_artifact_support'})

_L3_REDUCTION_FIELDS_A = frozenset({
    'reductions', 'frozen_reductions', 'oracle_reductions',
    'permuted_reductions', 'shuffled_reductions', 'shuffled_frozen_reductions',
})
_L3_EMPTY_A = frozenset({'returned_defined_error'})

_L3_V44_FAMILY_EXTRA_A = frozenset({
    'observed_reductions_5', 'observed_violation_score_5',
})

# --- L5 Classification A ---

_L5_TOP_LEVEL_A = frozenset({
    'seed', 'law', 'verdict', 'kill_reasons', 'instrument_failure_reasons',
})
_L5_TOP_LEVEL_B = frozenset({'v44_artifact_support'})

_L5_CANDIDATE_A = frozenset({
    'world_validity_accuracy', 'self_acquisition_accuracy',
    'chain_walk_accuracy', 'access_count_matches_k',
})
_L5_FAIR_NAIVE_A = frozenset({
    'combo_accuracy_world_validity', 'chain_walk_accuracy',
})
_L5_FROZEN_A = frozenset({
    'chain_walk_accuracy_post_freeze', 'label', 'chain_walk_results',
})
_L5_ORACLE_A = frozenset({
    'world_validity_accuracy', 'self_acquisition_accuracy',
    'chain_walk_accuracy', 'chain_walk_results',
})
_L5_PERMUTED_A = frozenset({
    'combo_accuracy', 'chain_content_mismatch_rate',
    'plus_one_p_value', 'pooled_center',
})
_L5_SHUFFLED_A = frozenset({
    'combo_query_order_accuracy', 'self_acquisition_query_order_accuracy',
    'query_order_equal_to_original', 'chain_walk_accuracy', 'edge_count',
    'chain_walk_results',
})
_L5_FULL_SCAN_A = frozenset({
    'chain_walk_accuracy', 'access_count_deltas',
    'chain_walk_results', 'log',
})
_L5_EMPTY_A = frozenset({
    'combination_returned_defined_error', 'chain_returned_defined_error',
})

_L5_V44_PERMUTED_EXTRA_A = frozenset({
    'observed_accuracy', 'null_accuracies_1000', 'pooled_center',
    'observed_absolute_departure', 'null_absolute_departures_1000',
    'chain_content_mismatch_rate', 'field_mapping_derangement_200',
    'chain_content_derangement_200', 'query_results_200',
})

# --- L6 Classification A ---

_L6_FIELDS_A = frozenset({
    'seed', 'law', 'reachability_audit', 'module_public_names',
    'module_namespace_complete', 'attacks', 'l18_arms',
    'verdict', 'kill_reasons', 'instrument_failure_reasons',
})

# Chain walk results row schema (used in L5 frozen/oracle/shuffled/full_scan)
_CHAIN_WALK_ROW_A = frozenset({
    'chain_id', 'query_type', 'k', 'visited', 'expected',
    'accuracy', 'access_count_delta', 'access_count_matches_k',
})

# L5 permuted query_results_200 row schema
_QUERY_RESULT_ROW_A = frozenset({
    'query_id', 'prediction', 'truth', 'correct',
})

# L6 reachability_audit row schema
_AUDIT_ROW_A = frozenset({
    'module', 'callable_name', 'return_type_observed',
    'is_tagged_union', 'verdict',
})

# L6 attack row schema
_ATTACK_ROW_A = frozenset({
    'attack_id', 'path_type', 'caught', 'diagnosis',
})


# ---------------------------------------------------------------------------
# Fail-closed traversal helpers
# ---------------------------------------------------------------------------

def _check_leaf(path: str, field: str, value: Any, allowed: frozenset,
                where_present: frozenset = frozenset()) -> None:
    """Check a single field against the allowed set."""
    if field in allowed:
        return
    if field in where_present:
        return
    raise ReproducibilityProjectionError(
        f"{path}.{field}", type(value).__name__)


def _check_dict_fields(path: str, d: Dict[str, Any], allowed: frozenset,
                       where_present: frozenset = frozenset()) -> None:
    """Check that all keys in dict are classified."""
    for key in d:
        if key not in allowed and key not in where_present:
            raise ReproducibilityProjectionError(
                f"{path}.{key}", type(d[key]).__name__)


# ---------------------------------------------------------------------------
# Classification C invariant checks
# ---------------------------------------------------------------------------

def _check_l1_classification_c(law_result: Dict[str, Any]) -> List[str]:
    """Check L1 Classification C invariants. Returns list of failure messages."""
    failures = []
    controls = law_result.get('v44_stochastic_controls', {})

    # permuted.rho_null_1000_values (top-level L1 permuted arm)
    permuted = law_result.get('permuted', {})
    if 'rho_null_1000_values' in permuted:
        ctrl_permuted = controls.get('permuted', {})
        if 'null_statistics' in ctrl_permuted:
            signed_rhos = permuted['rho_null_1000_values']
            null_stats = ctrl_permuted['null_statistics']
            if [abs(x) for x in signed_rhos] != list(null_stats):
                raise ReproducibilityInvariantError(
                    'permuted.rho_null_1000_values',
                    'v44_stochastic_controls.permuted.null_statistics',
                    signed_rhos, null_stats)

    # frozen/fair_naive r_squared_null_1000
    for arm in ('frozen', 'fair_naive'):
        ctrl = controls.get(arm, {})
        if 'r_squared_null_1000' in ctrl and 'null_statistics' in ctrl:
            if ctrl['r_squared_null_1000'] != ctrl['null_statistics']:
                raise ReproducibilityInvariantError(
                    f'v44_stochastic_controls.{arm}.r_squared_null_1000',
                    f'v44_stochastic_controls.{arm}.null_statistics',
                    ctrl['r_squared_null_1000'], ctrl['null_statistics'])

    # permuted abs_rho_null_1000
    ctrl_permuted = controls.get('permuted', {})
    if 'abs_rho_null_1000' in ctrl_permuted and 'null_statistics' in ctrl_permuted:
        if ctrl_permuted['abs_rho_null_1000'] != ctrl_permuted['null_statistics']:
            raise ReproducibilityInvariantError(
                'v44_stochastic_controls.permuted.abs_rho_null_1000',
                'v44_stochastic_controls.permuted.null_statistics',
                ctrl_permuted['abs_rho_null_1000'],
                ctrl_permuted['null_statistics'])

    # shuffled null_max_1000
    ctrl_shuffled = controls.get('shuffled', {})
    if 'null_max_1000' in ctrl_shuffled and 'rho_null_1000x5' in ctrl_shuffled:
        expected = [max(row) for row in ctrl_shuffled['rho_null_1000x5']]
        if ctrl_shuffled['null_max_1000'] != expected:
            raise ReproducibilityInvariantError(
                'v44_stochastic_controls.shuffled.null_max_1000',
                'v44_stochastic_controls.shuffled.rho_null_1000x5[max]',
                ctrl_shuffled['null_max_1000'], expected)

    return failures


# ---------------------------------------------------------------------------
# Projection extraction (Classification A)
# ---------------------------------------------------------------------------

def _project_l1(law_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract Classification A fields from L1 results."""
    projected = {}
    # Top-level
    for field in _L1_TOP_LEVEL_A:
        if field in law_result:
            projected[field] = law_result[field]

    # Standard arms
    for arm in ('candidate', 'oracle', 'frozen', 'fair_naive',
                'recency_only', 'rehearsal_only', 'shuffled'):
        if arm not in law_result:
            continue
        arm_data = law_result[arm]
        projected[arm] = {}
        for field in _L1_ARM_A:
            if field in arm_data:
                projected[arm][field] = arm_data[field]
        if arm in _L1_ARM_PER_SET_RANKS_A and 'per_set_ranks' in arm_data:
            projected[arm]['per_set_ranks'] = arm_data['per_set_ranks']

    # Permuted arm
    if 'permuted' in law_result:
        projected['permuted'] = {}
        for field in _L1_PERMUTED_A:
            if field in law_result['permuted']:
                projected['permuted'][field] = law_result['permuted'][field]

    # Empty arm
    if 'empty' in law_result:
        projected['empty'] = {}
        for field in _L1_EMPTY_A:
            if field in law_result['empty']:
                projected['empty'][field] = law_result['empty'][field]

    # V4.4 stochastic controls
    if 'v44_stochastic_controls' in law_result:
        projected['v44_stochastic_controls'] = {}
        controls = law_result['v44_stochastic_controls']
        for family, ctrl in controls.items():
            projected['v44_stochastic_controls'][family] = _project_v44_summary(
                ctrl, _get_l1_family_extra_a(family))

    # V4.4 deterministic controls
    if 'v44_deterministic_controls' in law_result:
        projected['v44_deterministic_controls'] = {}
        det = law_result['v44_deterministic_controls']
        for arm in ('recency_only', 'rehearsal_only', 'oracle', 'empty'):
            if arm in det:
                projected['v44_deterministic_controls'][arm] = dict(det[arm])

    return projected


def _get_l1_family_extra_a(family: str) -> frozenset:
    if family in ('frozen', 'fair_naive'):
        return _L1_V44_FROZEN_FAIR_NAIVE_EXTRA_A
    elif family == 'permuted':
        return _L1_V44_PERMUTED_EXTRA_A
    elif family == 'shuffled':
        return _L1_V44_SHUFFLED_EXTRA_A
    return frozenset()


def _project_v44_summary(summary: Dict[str, Any],
                          extra_a: frozenset) -> Dict[str, Any]:
    """Project a V4.4 stochastic control summary to Classification A fields."""
    projected = {}
    for field in _V44_SUMMARY_A:
        if field in summary:
            projected[field] = summary[field]
    for field in extra_a:
        if field in summary:
            projected[field] = summary[field]
    return projected


def _project_l3(law_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract Classification A fields from L3 results."""
    projected = {}
    for field in _L3_TOP_LEVEL_A:
        if field in law_result:
            projected[field] = law_result[field]

    for field in _L3_REDUCTION_FIELDS_A:
        if field in law_result:
            projected[field] = law_result[field]

    if 'empty' in law_result:
        projected['empty'] = {}
        for field in _L3_EMPTY_A:
            if field in law_result['empty']:
                projected['empty'][field] = law_result['empty'][field]

    if 'v44_stochastic_controls' in law_result:
        projected['v44_stochastic_controls'] = {}
        controls = law_result['v44_stochastic_controls']
        for family, ctrl in controls.items():
            projected['v44_stochastic_controls'][family] = _project_v44_summary(
                ctrl, _L3_V44_FAMILY_EXTRA_A)

    return projected


def _project_l5(law_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract Classification A fields from L5 results."""
    projected = {}
    for field in _L5_TOP_LEVEL_A:
        if field in law_result:
            projected[field] = law_result[field]

    arm_schemas = {
        'candidate': _L5_CANDIDATE_A,
        'fair_naive': _L5_FAIR_NAIVE_A,
        'frozen': _L5_FROZEN_A,
        'oracle': _L5_ORACLE_A,
        'permuted': _L5_PERMUTED_A,
        'shuffled': _L5_SHUFFLED_A,
        'full_scan': _L5_FULL_SCAN_A,
        'empty': _L5_EMPTY_A,
    }
    for arm, schema in arm_schemas.items():
        if arm in law_result:
            projected[arm] = {}
            for field in schema:
                if field in law_result[arm]:
                    projected[arm][field] = law_result[arm][field]

    if 'v44_stochastic_controls' in law_result:
        projected['v44_stochastic_controls'] = {}
        controls = law_result['v44_stochastic_controls']
        for family, ctrl in controls.items():
            projected['v44_stochastic_controls'][family] = _project_v44_summary(
                ctrl, _L5_V44_PERMUTED_EXTRA_A)

    return projected


def _project_l6(law_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract Classification A fields from L6 results."""
    projected = {}
    for field in _L6_FIELDS_A:
        if field in law_result:
            projected[field] = law_result[field]
    return projected


_LAW_PROJECTORS = {
    'L1': _project_l1,
    'L3': _project_l3,
    'L5': _project_l5,
    'L6': _project_l6,
}


# ---------------------------------------------------------------------------
# Fail-closed traversal
# ---------------------------------------------------------------------------

def _traverse_check(path: str, value: Any, law: str) -> None:
    """Recursively traverse a value and check all fields are classified."""
    if isinstance(value, dict):
        for key, val in value.items():
            child_path = f"{path}.{key}"
            _traverse_check(child_path, val, law)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            child_path = f"{path}[{i}]"
            _traverse_check(child_path, item, law)
    # Leaf values are OK — we check at the dict-key level


def _fail_closed_l1(law_result: Dict[str, Any], path: str) -> None:
    """Check all fields in L1 results are classified."""
    # Top-level
    for key in law_result:
        if key in _L1_TOP_LEVEL_A or key in _L1_TOP_LEVEL_B:
            continue
        if key == 'permuted':
            _fail_closed_l1_permuted(law_result[key], f"{path}.permuted")
        elif key == 'empty':
            _check_dict_fields(f"{path}.empty", law_result[key], _L1_EMPTY_A)
        elif key in ('candidate', 'oracle', 'frozen', 'fair_naive',
                     'recency_only', 'rehearsal_only', 'shuffled'):
            _fail_closed_l1_arm(law_result[key], f"{path}.{key}", key)
        elif key == 'v44_stochastic_controls':
            _fail_closed_l1_v44_controls(law_result[key], f"{path}.{key}")
        elif key == 'v44_deterministic_controls':
            _fail_closed_l1_v44_det(law_result[key], f"{path}.{key}")
        else:
            raise ReproducibilityProjectionError(
                f"{path}.{key}", type(law_result[key]).__name__)

    # Check permuted C fields
    permuted = law_result.get('permuted', {})
    for key in permuted:
        if key not in _L1_PERMUTED_A and key not in _L1_PERMUTED_C:
            raise ReproducibilityProjectionError(
                f"{path}.permuted.{key}", type(permuted[key]).__name__)


def _fail_closed_l1_arm(arm: Dict[str, Any], path: str, arm_name: str) -> None:
    for key in arm:
        if key in _L1_ARM_A:
            continue
        if key == 'per_set_ranks':
            if arm_name not in _L1_ARM_PER_SET_RANKS_A:
                raise ReproducibilityProjectionError(
                    f"{path}.{key}", type(arm[key]).__name__)
            continue
        raise ReproducibilityProjectionError(
            f"{path}.{key}", type(arm[key]).__name__)


def _fail_closed_l1_permuted(permuted: Dict[str, Any], path: str) -> None:
    for key in permuted:
        if key in _L1_PERMUTED_A or key in _L1_PERMUTED_C:
            continue
        raise ReproducibilityProjectionError(
            f"{path}.{key}", type(permuted[key]).__name__)


def _fail_closed_l1_v44_controls(controls: Dict[str, Any], path: str) -> None:
    for family, summary in controls.items():
        extra_a = _get_l1_family_extra_a(family)
        extra_c = _get_l1_family_extra_c(family)
        for key in summary:
            if key in _V44_SUMMARY_A or key in _V44_SUMMARY_B:
                continue
            if key in extra_a or key in extra_c:
                continue
            raise ReproducibilityProjectionError(
                f"{path}.{family}.{key}", type(summary[key]).__name__)


def _get_l1_family_extra_c(family: str) -> frozenset:
    if family in ('frozen', 'fair_naive'):
        return _L1_V44_FROZEN_FAIR_NAIVE_EXTRA_C
    elif family == 'permuted':
        return _L1_V44_PERMUTED_EXTRA_C
    elif family == 'shuffled':
        return _L1_V44_SHUFFLED_EXTRA_C
    return frozenset()


def _fail_closed_l1_v44_det(det: Dict[str, Any], path: str) -> None:
    schemas = {
        'recency_only': _L1_V44_DET_RECENCY_A,
        'rehearsal_only': _L1_V44_DET_REHEARSAL_A,
        'oracle': _L1_V44_DET_ORACLE_A,
        'empty': _L1_V44_DET_EMPTY_A,
    }
    for arm, schema in schemas.items():
        if arm not in det:
            continue
        for key in det[arm]:
            if key in schema:
                continue
            raise ReproducibilityProjectionError(
                f"{path}.{arm}.{key}", type(det[arm][key]).__name__)


def _fail_closed_l3(law_result: Dict[str, Any], path: str) -> None:
    for key in law_result:
        if key in _L3_TOP_LEVEL_A or key in _L3_TOP_LEVEL_B:
            continue
        if key in _L3_REDUCTION_FIELDS_A:
            continue
        if key == 'empty':
            _check_dict_fields(f"{path}.empty", law_result[key], _L3_EMPTY_A)
        elif key == 'v44_stochastic_controls':
            for family, summary in law_result[key].items():
                for field in summary:
                    if field not in _V44_SUMMARY_A and \
                       field not in _V44_SUMMARY_B and \
                       field not in _L3_V44_FAMILY_EXTRA_A:
                        raise ReproducibilityProjectionError(
                            f"{path}.{key}.{family}.{field}",
                            type(summary[field]).__name__)
        else:
            raise ReproducibilityProjectionError(
                f"{path}.{key}", type(law_result[key]).__name__)


def _fail_closed_l5(law_result: Dict[str, Any], path: str) -> None:
    arm_schemas = {
        'candidate': _L5_CANDIDATE_A,
        'fair_naive': _L5_FAIR_NAIVE_A,
        'frozen': _L5_FROZEN_A,
        'oracle': _L5_ORACLE_A,
        'permuted': _L5_PERMUTED_A,
        'shuffled': _L5_SHUFFLED_A,
        'full_scan': _L5_FULL_SCAN_A,
        'empty': _L5_EMPTY_A,
    }
    for key in law_result:
        if key in _L5_TOP_LEVEL_A or key in _L5_TOP_LEVEL_B:
            continue
        if key in arm_schemas:
            _check_dict_fields(f"{path}.{key}", law_result[key],
                               arm_schemas[key])
        elif key == 'v44_stochastic_controls':
            for family, summary in law_result[key].items():
                for field in summary:
                    if field not in _V44_SUMMARY_A and \
                       field not in _V44_SUMMARY_B and \
                       field not in _L5_V44_PERMUTED_EXTRA_A:
                        raise ReproducibilityProjectionError(
                            f"{path}.{key}.{family}.{field}",
                            type(summary[field]).__name__)
        else:
            raise ReproducibilityProjectionError(
                f"{path}.{key}", type(law_result[key]).__name__)


def _fail_closed_l6(law_result: Dict[str, Any], path: str) -> None:
    for key in law_result:
        if key not in _L6_FIELDS_A:
            raise ReproducibilityProjectionError(
                f"{path}.{key}", type(law_result[key]).__name__)


_FAIL_CLOSED = {
    'L1': _fail_closed_l1,
    'L3': _fail_closed_l3,
    'L5': _fail_closed_l5,
    'L6': _fail_closed_l6,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

PROJECTION_SCHEMA_VERSION = "m3_scoring_semantic_reproducibility_v1"


def compute_scoring_semantic_digest(
    results: Dict[str, Any],
    config: Dict[str, Any],
) -> Tuple[str, Dict[str, Any]]:
    """Compute the compared scoring-semantic digest (§3.1).

    Args:
        results: per-law results dict, keyed by seed string -> law -> result.
        config: configuration block dict (§2.3).

    Returns:
        (digest_hex, projection_payload) where projection_payload is the
        canonical dict that was hashed.
    """
    projection = {
        'projection_schema_version': PROJECTION_SCHEMA_VERSION,
        'config': config,
        'laws': {},
    }

    for seed_key, seed_data in results.items():
        projection['laws'][seed_key] = {}
        for law, law_result in seed_data.items():
            # Fail-closed: verify all fields are classified
            fail_closed_fn = _FAIL_CLOSED.get(law)
            if fail_closed_fn is None:
                raise ReproducibilityProjectionError(
                    f"{seed_key}.{law}", "unknown_law")
            fail_closed_fn(law_result, f"{seed_key}.{law}")

            # Classification C invariant checks (L1 only for now)
            if law == 'L1':
                _check_l1_classification_c(law_result)

            # Extract Classification A projection
            projector = _LAW_PROJECTORS.get(law)
            if projector is None:
                raise ReproducibilityProjectionError(
                    f"{seed_key}.{law}", "no_projector")
            projection['laws'][seed_key][law] = projector(law_result)

    digest = canonical_digest(projection)
    return digest, projection


def compute_final_report_digest(
    compared_payload: Dict[str, Any],
    pass1_digest: Optional[str],
    pass2_digest: Optional[str],
    digests_equal: Optional[bool],
    reproducibility: Dict[str, Any],
    interface_invariants: Dict[str, Any],
    finite_numeric_results: bool,
    l20_self_test: Dict[str, Any],
    raw_artifact_validation: Dict[str, Any],
    overall_verdict: str,
) -> str:
    """Compute the non-compared final-report digest (§3.2).

    This is a single integrity hash over the complete output bundle.
    It is NOT compared between passes and does NOT affect overall_verdict.
    """
    payload = {
        'compared_digest_payload': compared_payload,
        'pass1_digest': pass1_digest,
        'pass2_digest': pass2_digest,
        'digests_equal': digests_equal,
        'reproducibility': reproducibility,
        'interface_invariants': interface_invariants,
        'finite_numeric_results': finite_numeric_results,
        'l20_self_test': l20_self_test,
        'raw_artifact_validation': raw_artifact_validation,
        'overall_verdict': overall_verdict,
    }
    return canonical_digest(payload)


# ---------------------------------------------------------------------------
# Mode-aware label helper (§6.2)
# ---------------------------------------------------------------------------

_LABELS = {
    'scope': {
        'development': 'M3 development diagnostics only',
        'scoring': 'M3 supervised scoring run',
    },
    'scoring_seed_pool': {
        'development': 'WITHHELD; forbidden in development',
        'scoring': ('WITHHELD; supplied by courier, recorded in this artifact; '
                    'future scoring seed pools remain withheld'),
    },
    'r3_note': {
        'development': ('Scoring-only seed identities are absent from this '
                        'development implementation and its artifacts.'),
        'scoring': ('Scoring seed identities were supplied by Rebecca\'s '
                    'supervised-executor courier channel and recorded in the '
                    'seed exposure ledger; future scoring seed pools remain '
                    'withheld.'),
    },
}


def mode_label(mode: str, key: str) -> str:
    """Return the mode-aware label string (§6.2)."""
    if key not in _LABELS:
        raise KeyError(f"unknown label key: {key}")
    if mode not in _LABELS[key]:
        raise KeyError(f"unknown mode: {mode}")
    return _LABELS[key][mode]
