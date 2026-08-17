#!/usr/bin/env python3
"""Development-only direct-call diagnostic runner for M3 V4.4."""
import contextlib
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

REPO = Path('/home/user/workspace/m3_v44_repo')
SRC = REPO / 'src'
OUT = REPO / 'diagnostics' / 'm3_v44_development_101_105.json'
LOG = REPO / 'diagnostics' / 'm3_v44_development_101_105.log'
SEEDS = [101, 102, 103, 104, 105]
LAWS = [('L1', 'run_l1'), ('L3', 'run_l3'), ('L5', 'run_l5'), ('L6', 'run_l6')]
sys.path.insert(0, str(SRC))
import numpy as np
import scipy
import m3_harness as m3


def json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f'not JSON serializable: {type(value).__name__}')


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def git_text(args):
    return subprocess.run(['git', '-C', str(REPO), *args], check=False,
                          text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT).stdout


def atomic_write_json(data):
    tmp = OUT.with_suffix('.json.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True, allow_nan=False,
                  default=json_default)
        f.write('\n')
    os.replace(tmp, OUT)


def log(message):
    line = f'{utc_now()} {message}'
    print(line, flush=True)
    with LOG.open('a', encoding='utf-8') as f:
        f.write(line + '\n')


data = {
    'run_name': 'm3_v44_development_101_105',
    'scope': 'development diagnostics only',
    'execution_policy': {
        'requested_seeds': SEEDS,
        'executed_seeds': [],
        'excluded_scoring_seeds': [201, 202, 203],
        'scoring_mode_invoked': False,
        'invocation_style': 'direct public run_l1/run_l3/run_l5/run_l6 calls',
        'artifact_mode': 'no-output summary mode (artifact_writer=None)',
        'retry_policy': 'no retries; each seed/law call attempted at most once',
    },
    'environment': {
        'started_at_utc': utc_now(),
        'python': platform.python_version(),
        'numpy': np.__version__,
        'scipy': scipy.__version__,
        'git_head': git_text(['rev-parse', 'HEAD']).strip(),
        'git_status_porcelain_before': git_text(['status', '--short']).splitlines(),
    },
    'seeds': {},
    'run_failures': [],
}
LOG.write_text('', encoding='utf-8')
log('START scope=development direct_calls=yes artifact_writer=none seeds=101,102,103,104,105 scoring_mode=no')
atomic_write_json(data)

for seed in SEEDS:
    log(f'SEED_START seed={seed}')
    seed_entry = {'seed': seed, 'started_at_utc': utc_now(), 'laws': {}}
    data['seeds'][str(seed)] = seed_entry
    data['execution_policy']['executed_seeds'].append(seed)
    for law, function_name in LAWS:
        log(f'LAW_START seed={seed} law={law}')
        started = time.perf_counter()
        wall_started = utc_now()
        try:
            # Direct public call, summary-only/no-output operation; no main(), no writer.
            result = getattr(m3, function_name)(seed, log_lines=None)
            elapsed = time.perf_counter() - started
            law_entry = {
                'status': 'completed',
                'started_at_utc': wall_started,
                'completed_at_utc': utc_now(),
                'elapsed_seconds': elapsed,
                'result': result,
                'exception': None,
            }
            seed_entry['laws'][law] = law_entry
            log(f'LAW_END seed={seed} law={law} status=completed verdict={result.get("verdict", "MISSING")} elapsed_seconds={elapsed:.6f}')
        except BaseException as exc:
            elapsed = time.perf_counter() - started
            law_entry = {
                'status': 'failed',
                'started_at_utc': wall_started,
                'completed_at_utc': utc_now(),
                'elapsed_seconds': elapsed,
                'result': None,
                'exception': {
                    'type': type(exc).__name__,
                    'message': str(exc),
                    'traceback': traceback.format_exc(),
                },
            }
            seed_entry['laws'][law] = law_entry
            data['run_failures'].append({
                'seed': seed, 'law': law, 'reason': f'{type(exc).__name__}: {exc}',
            })
            log(f'LAW_END seed={seed} law={law} status=failed exception={type(exc).__name__} elapsed_seconds={elapsed:.6f}')
        atomic_write_json(data)
    seed_entry['completed_at_utc'] = utc_now()
    law_statuses = {law: item['status'] for law, item in seed_entry['laws'].items()}
    log('SEED_END seed={} statuses={}'.format(seed, ','.join(f'{law}:{status}' for law, status in law_statuses.items())))
    atomic_write_json(data)

data['environment']['completed_at_utc'] = utc_now()
data['environment']['elapsed_seconds_total'] = time.perf_counter() - time.perf_counter()  # replaced below
# Use monotonic total only from recorded law times to avoid non-execution setup ambiguity.
data['elapsed_seconds_laws_total'] = sum(
    entry['elapsed_seconds']
    for seed in data['seeds'].values()
    for entry in seed['laws'].values()
)
data['environment']['git_status_porcelain_after'] = git_text(['status', '--short']).splitlines()
atomic_write_json(data)
log(f'END completed_seeds={len(data["seeds"])} failed_law_calls={len(data["run_failures"])} law_elapsed_seconds_total={data["elapsed_seconds_laws_total"]:.6f}')
