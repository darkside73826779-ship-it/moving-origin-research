"""Streaming, content-addressed raw artifacts for M3 V4.4 stochastic draws."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import unicodedata
from typing import Any, Dict, Iterable, Mapping, Sequence

import numpy as np
from m3_v44_rng import (
    PROTOCOL_ID, ROOT_DOMAIN, derive_stream_key, subdraw_definition,
)


REQUIRED_DRAW_FIELDS = {
    'L1.frozen': ('draw_role', 'replicate_index', 'entries_200', 'candidate_sets_100',
                  'ranked_occurrences_500', 'log_accessibility_200', 'bin_memberships_200',
                  'bin_means_5', 'bin_age_representatives_5', 'r_squared'),
    'L1.fair_naive': ('draw_role', 'replicate_index', 'entries_200', 'candidate_sets_100',
                      'ranking_permutation_200', 'ranked_occurrences_500',
                      'log_accessibility_200', 'bin_memberships_200', 'bin_means_5',
                      'bin_age_representatives_5', 'r_squared'),
    'L1.permuted': ('draw_role', 'replicate_index', 'entry_ids_200', 'age_values_200',
                     'rehearsal_values_200', 'mapping_permutation_200',
                     'log_accessibility_200', 'paired_age_accessibility_200', 'spearman_rho'),
    'L1.shuffled': ('draw_role', 'replicate_index', 'entries_200', 'priming_queries_1200',
                    'query_to_entry_assignment_1200', 'realized_rehearsal_counts_200',
                    'candidate_sets_100', 'ranked_occurrences_500', 'log_accessibility_200',
                    'within_bin_pairs_5', 'conditional_rho_5'),
    'L3.frozen': ('draw_role', 'replicate_index', 'innovations_1110x8', 'sequence_1010x8',
                  'fitting_origin_indices', 'buffer_cycle_indices', 'evaluation_origin_indices',
                  'fit_target_indices_by_horizon', 'evaluation_target_indices_by_horizon',
                  'design_matrices_by_horizon', 'targets_by_horizon',
                  'fitted_baseline_weights_by_horizon', 'baseline_predictions_by_horizon',
                  'frozen_predictions_by_horizon',
                  'per_example_baseline_squared_errors_by_horizon',
                  'per_example_frozen_squared_errors_by_horizon', 'baseline_loss_5',
                  'frozen_loss_5', 'reduction_5'),
    'L3.oracle': ('draw_role', 'replicate_index', 'innovations_1110x8', 'sequence_1010x8',
                  'fitting_origin_indices', 'buffer_cycle_indices', 'evaluation_origin_indices',
                  'fit_target_indices_by_horizon', 'evaluation_target_indices_by_horizon',
                  'design_matrices_by_horizon', 'targets_by_horizon',
                  'fitted_baseline_weights_by_horizon', 'oracle_predictions_by_horizon',
                  'baseline_predictions_by_horizon',
                  'per_example_baseline_squared_errors_by_horizon',
                  'per_example_oracle_squared_errors_by_horizon', 'baseline_loss_5',
                  'oracle_loss_5', 'reduction_5', 'violation_score_5'),
    'L3.permuted': ('draw_role', 'replicate_index', 'innovations_1110x8', 'sequence_1010x8',
                    'fitting_origin_indices', 'buffer_cycle_indices', 'evaluation_origin_indices',
                    'fit_target_indices_by_horizon', 'evaluation_target_indices_by_horizon',
                    'design_matrices_by_horizon', 'targets_by_horizon', 'channel_derangement',
                    'fitted_weights_by_horizon', 'baseline_predictions_by_horizon',
                    'permuted_predictions_by_horizon',
                    'per_example_baseline_squared_errors_by_horizon',
                    'per_example_permuted_squared_errors_by_horizon', 'baseline_loss_5',
                    'permuted_loss_5', 'reduction_5'),
    'L3.shuffled': ('draw_role', 'replicate_index', 'innovations_1110x8',
                    'unshuffled_sequence_1010x8', 'cycle_order_permutation',
                    'shuffled_sequence_1010x8', 'fitting_origin_indices',
                    'buffer_cycle_indices', 'evaluation_origin_indices',
                    'fit_target_indices_by_horizon', 'evaluation_target_indices_by_horizon',
                    'targets_by_horizon', 'fitted_weights_by_horizon',
                    'shuffled_predictions_by_horizon',
                    'paired_shuffled_frozen_predictions_by_horizon',
                    'per_example_shuffled_squared_errors_by_horizon',
                    'per_example_paired_frozen_squared_errors_by_horizon',
                    'shuffled_loss_5', 'paired_frozen_loss_5',
                    'reduction_difference_minus_tolerance_5'),
    'L5.permuted': ('draw_role', 'replicate_index', 'facts_200', 'truth_labels_200',
                    'field_mapping_derangement_200', 'predictions_200', 'query_results_200',
                    'combo_accuracy', 'chain_nodes_200', 'chain_content_derangement_200',
                    'returned_chain_content_40', 'expected_chain_content_40',
                    'chain_content_mismatch_rate'),
}

STOCHASTIC_FAMILIES_BY_LAW = {
    'L1': ('L1.frozen', 'L1.fair_naive', 'L1.permuted', 'L1.shuffled'),
    'L3': ('L3.frozen', 'L3.oracle', 'L3.permuted', 'L3.shuffled'),
    'L5': ('L5.permuted',),
}


def _nfc(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize('NFC', value)
    if isinstance(value, dict):
        return {str(_nfc(key)): _nfc(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_nfc(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def _canonical_json_bytes(value: Any) -> bytes:
    value = _nfc(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


class RawArtifactWriter:
    """Writes content-addressed raw payloads and a draw declaration per draw."""

    def __init__(self, output_dir: str, *, expected_families=()):
        self.output_dir = Path(output_dir)
        self.root = self.output_dir / 'm3_v44_raw'
        self.payload_dir = self.root / 'objects'
        self.draw_dir = self.root / 'draws'
        self.payload_dir.mkdir(parents=True, exist_ok=True)
        self.draw_dir.mkdir(parents=True, exist_ok=True)
        self._arrays: list[Dict[str, Any]] = []
        self._draws: list[Dict[str, Any]] = []
        self.expected_families = tuple(sorted(expected_families))

    def _store(self, data: bytes, suffix: str) -> tuple[str, str, int]:
        digest = hashlib.sha256(data).hexdigest()
        relative_path = f'm3_v44_raw/objects/{digest}.{suffix}'
        path = self.output_dir / relative_path
        if not path.exists():
            with open(path, 'wb') as handle:
                handle.write(data)
        return digest, relative_path, len(data)

    def array(self, field_name: str, values: Any, *, row_key: str,
              ordering_rule: str) -> Dict[str, Any]:
        array = np.asarray(values)
        if array.dtype.kind in 'iu':
            array = np.ascontiguousarray(array.astype('<i8', copy=False))
            dtype = 'int64'
        elif array.dtype.kind == 'b':
            array = np.ascontiguousarray(array.astype('u1', copy=False))
            if not np.all((array == 0) | (array == 1)):
                raise ValueError('boolean array is not restricted to 0/1')
            dtype = 'uint8'
        else:
            array = np.ascontiguousarray(array.astype('<f8', copy=False))
            if not np.all(np.isfinite(array)):
                raise FloatingPointError(f'non-finite float in {field_name}')
            dtype = 'float64'
        raw = array.tobytes(order='C')
        digest, path, byte_length = self._store(raw, 'bin')
        item = {
            'field_name': field_name, 'relative_path': path,
            'shape': list(array.shape), 'dtype': dtype, 'byte_order': 'little',
            'row_key': _nfc(row_key), 'ordering_rule': _nfc(ordering_rule),
            'byte_length': byte_length, 'sha256': digest,
            'finite_status': bool(dtype != 'float64' or np.all(np.isfinite(array))),
        }
        self._arrays.append(item)
        return item

    def text(self, field_name: str, value: Any, *, row_key: str,
             ordering_rule: str) -> Dict[str, Any]:
        raw = _canonical_json_bytes(value)
        digest, path, byte_length = self._store(raw, 'json')
        item = {
            'field_name': field_name, 'relative_path': path, 'shape': [],
            'dtype': 'utf8_json', 'byte_order': 'not_applicable',
            'row_key': _nfc(row_key), 'ordering_rule': _nfc(ordering_rule),
            'byte_length': byte_length, 'sha256': digest, 'finite_status': True,
        }
        self._arrays.append(item)
        return item

    def columns(self, field_name: str, columns: Mapping[str, Any], *,
                row_key: str, ordering_rule: str) -> Dict[str, Any]:
        encoded = {}
        for name, values in columns.items():
            subfield = f'{field_name}.{name}'
            if isinstance(values, np.ndarray) or isinstance(values, (list, tuple)) and (
                    not values or not isinstance(values[0], str)):
                encoded[name] = self.array(subfield, values, row_key=row_key,
                                           ordering_rule=ordering_rule)
            else:
                encoded[name] = self.text(subfield, values, row_key=row_key,
                                          ordering_rule=ordering_rule)
        return {'encoding': 'columnar', 'columns': encoded}

    def declare_draw(self, family_id: str, *, draw_role: str,
                     replicate_index: int, fields: Mapping[str, Any],
                     rng_records: Sequence[Mapping[str, Any]]) -> str:
        expected = set(REQUIRED_DRAW_FIELDS[family_id])
        actual = set(fields) | {'draw_role', 'replicate_index'}
        if expected != actual:
            missing, extra = sorted(expected - actual), sorted(actual - expected)
            raise ValueError(f'{family_id} draw schema mismatch missing={missing} extra={extra}')
        declaration = {
            'schema_version': 'm3-v4.4-raw-draw-v1', 'family_id': family_id,
            'draw_role': draw_role, 'replicate_index': int(replicate_index),
            'fields': _nfc(dict(fields)), 'rng_derivation_records': _nfc(list(rng_records)),
        }
        raw = _canonical_json_bytes(declaration)
        digest = hashlib.sha256(raw).hexdigest()
        relative_path = (
            f'm3_v44_raw/draws/{family_id.replace(".", "_")}_'
            f'{draw_role.lower()}_{replicate_index:04d}_{digest}.json')
        path = self.output_dir / relative_path
        with open(path, 'wb') as handle:
            handle.write(raw)
        self._draws.append({
            'family_id': family_id, 'draw_role': draw_role,
            'replicate_index': int(replicate_index), 'relative_path': relative_path,
            'sha256': digest, 'byte_length': len(raw),
        })
        return relative_path

    def finalize(self) -> str:
        manifest = {
            'schema_version': 'm3-v4.4-raw-manifest-v1',
            'complete_raw_schema': True,
            'numeric_array_encoding': 'C-row-major little-endian int64/float64/uint8; no padding',
            'string_encoding': 'Unicode NFC UTF-8 canonical JSON',
            'expected_families': list(self.expected_families),
            'arrays': sorted(self._arrays, key=lambda item: (
                item['sha256'], item['field_name'])),
            'draws': sorted(self._draws, key=lambda item: (
                item['family_id'], item['draw_role'], item['replicate_index'])),
        }
        path = self.output_dir / 'm3_v44_raw_manifest.json'
        with open(path, 'wb') as handle:
            handle.write(_canonical_json_bytes(manifest))
        return 'm3_v44_raw_manifest.json'


def load_array(output_dir: str, item: Mapping[str, Any]) -> np.ndarray:
    dtype = {'int64': '<i8', 'float64': '<f8', 'uint8': 'u1'}[item['dtype']]
    path = Path(output_dir) / item['relative_path']
    raw = path.read_bytes()
    if len(raw) != item['byte_length'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
        raise ValueError('raw array custody check failed')
    array = np.frombuffer(raw, dtype=np.dtype(dtype)).reshape(item['shape'])
    if item['dtype'] == 'float64' and not np.all(np.isfinite(array)):
        raise ValueError('raw array finite check failed')
    return array.copy()


def _descriptor_items(value):
    if isinstance(value, dict):
        if {'relative_path', 'sha256', 'byte_length', 'dtype'}.issubset(value):
            yield value
        else:
            for child in value.values():
                yield from _descriptor_items(child)
    elif isinstance(value, list):
        for child in value:
            yield from _descriptor_items(child)


def _validate_record(record, family_id, draw_role, replicate_index, used_domains):
    law, arm = family_id.split('.', 1)
    required = {
        'rng_protocol_id', 'hash', 'root_domain_hex', 'law', 'arm',
        'draw_role', 'scoring_seed', 'replicate_index', 'subdraw_index',
        'derived_key_hex', 'stream_key_hex', 'accepted_permutation',
        'rejection_count', 'stream_block_count', 'stream_word_count',
        'sha256_digest',
    }
    if not required.issubset(record):
        raise ValueError('RNG record required-field failure')
    if (record['rng_protocol_id'] != PROTOCOL_ID
            or record['hash'] != 'SHA-256'
            or record['root_domain_hex'] != ROOT_DOMAIN.hex()
            or record['law'] != law or record['arm'] != arm
            or record['draw_role'] != draw_role
            or record['replicate_index'] != replicate_index
            or record['derived_key_hex'] != record['stream_key_hex']):
        raise ValueError('RNG record protocol/identity mismatch')
    derived = derive_stream_key(
        law, arm, draw_role, int(record['scoring_seed']),
        int(replicate_index), int(record['subdraw_index'])).hex()
    if derived != record['derived_key_hex']:
        raise ValueError('RNG record key derivation mismatch')
    definition = subdraw_definition(
        law, arm, draw_role, int(record['subdraw_index']))
    domain = (
        law, arm, draw_role, int(record['scoring_seed']),
        int(replicate_index), int(record['subdraw_index']))
    if domain in used_domains:
        raise ValueError('RNG domain reuse detected in manifest')
    used_domains.add(domain)
    accepted = record['accepted_permutation']
    if definition.accepted_permutation:
        if not isinstance(accepted, list) or len(accepted) != definition.size:
            raise ValueError('RNG accepted transform length failure')
        if sorted(accepted) != list(range(definition.size)):
            raise ValueError('RNG accepted transform permutation failure')
        if (definition.kind == 'derangement'
                and any(index == value for index, value in enumerate(accepted))):
            raise ValueError('RNG accepted derangement fixed point')
    elif accepted is not None:
        raise ValueError('Gaussian RNG record must have null accepted permutation')


def _expected_subdraws(family_id, draw_role):
    if family_id in ('L1.frozen', 'L1.fair_naive', 'L1.permuted', 'L1.shuffled'):
        return {0}
    if family_id in ('L3.frozen', 'L3.oracle'):
        return {0}
    if family_id in ('L3.permuted', 'L3.shuffled'):
        return {0, 1} if draw_role == 'OBSERVED' else {0}
    if family_id == 'L5.permuted':
        return {0, 1}
    raise ValueError(f'unknown stochastic family {family_id}')


def validate_manifest(output_dir: str, *, require_full_family: bool = True) -> Dict[str, Any]:
    path = Path(output_dir) / 'm3_v44_raw_manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if manifest.get('complete_raw_schema') is not True:
        raise ValueError('manifest does not claim complete raw schema')
    array_descriptors = {}
    for item in manifest['arrays']:
        key = (item['field_name'], item['relative_path'], item['sha256'])
        array_descriptors[key] = item
        if item['dtype'] in ('int64', 'float64', 'uint8'):
            load_array(output_dir, item)
        else:
            raw = (Path(output_dir) / item['relative_path']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != item['sha256']:
                raise ValueError('string custody check failed')
            value = json.loads(raw.decode('utf-8'))
            if _canonical_json_bytes(value) != raw:
                raise ValueError('string NFC/canonical encoding check failed')
    grouped: Dict[tuple[str, int], list[Dict[str, Any]]] = {}
    used_domains = set()
    for draw in manifest['draws']:
        raw = (Path(output_dir) / draw['relative_path']).read_bytes()
        if len(raw) != draw['byte_length'] or hashlib.sha256(raw).hexdigest() != draw['sha256']:
            raise ValueError('draw declaration custody check failed')
        declared = json.loads(raw.decode('utf-8'))
        expected = set(REQUIRED_DRAW_FIELDS[declared['family_id']])
        if set(declared['fields']) | {'draw_role', 'replicate_index'} != expected:
            raise ValueError('draw declaration field set failed')
        if declared['draw_role'] != draw['draw_role'] or declared['replicate_index'] != draw['replicate_index']:
            raise ValueError('draw declaration identity mismatch')
        descriptors = list(_descriptor_items(declared['fields']))
        if not descriptors:
            raise ValueError('draw has no raw field descriptors')
        for descriptor in descriptors:
            key = (
                descriptor.get('field_name'), descriptor.get('relative_path'),
                descriptor.get('sha256'))
            if key not in array_descriptors:
                raise ValueError('draw descriptor missing from manifest')
            manifest_descriptor = array_descriptors[key]
            for field in (
                    'shape', 'dtype', 'byte_order', 'row_key', 'ordering_rule',
                    'byte_length', 'finite_status'):
                if descriptor.get(field) != manifest_descriptor.get(field):
                    raise ValueError('draw descriptor metadata mismatch')
            if descriptor['dtype'] in ('int64', 'float64', 'uint8'):
                load_array(output_dir, descriptor)
            else:
                payload = (Path(output_dir) / descriptor['relative_path']).read_bytes()
                if (hashlib.sha256(payload).hexdigest() != descriptor['sha256']
                        or len(payload) != descriptor['byte_length']):
                    raise ValueError('draw string descriptor custody mismatch')
                value = json.loads(payload.decode('utf-8'))
                if _canonical_json_bytes(value) != payload:
                    raise ValueError('draw string descriptor canonical mismatch')
        records = declared.get('rng_derivation_records')
        if not isinstance(records, list) or not records:
            raise ValueError('draw missing RNG derivation record')
        for record in records:
            _validate_record(
                record, declared['family_id'], declared['draw_role'],
                declared['replicate_index'], used_domains)
        if {int(record['subdraw_index']) for record in records} != _expected_subdraws(
                declared['family_id'], declared['draw_role']):
            raise ValueError('RNG subdraw coverage mismatch')
        scoring_seeds = {int(record['scoring_seed']) for record in records}
        if len(scoring_seeds) != 1:
            raise ValueError('draw RNG records disagree on scoring seed')
        grouped.setdefault(
            (draw['family_id'], scoring_seeds.pop()), []).append(draw)
    expected_families = set(manifest.get('expected_families', ()))
    present_families = {family_id for family_id, _ in grouped}
    if require_full_family and present_families != expected_families:
        raise ValueError('selected stochastic family coverage mismatch')
    for (family_id, scoring_seed), draws in grouped.items():
        observed = [draw for draw in draws if draw['draw_role'] == 'OBSERVED']
        null_indices = sorted(
            draw['replicate_index'] for draw in draws
            if draw['draw_role'] == 'NULL')
        if len(observed) != 1 or observed[0]['replicate_index'] != 0:
            raise ValueError(
                f'{family_id} seed {scoring_seed} observed draw count/index failed')
        if require_full_family and null_indices != list(range(1000)):
            raise ValueError(
                f'{family_id} seed {scoring_seed} null draw coverage failed')
    return manifest
