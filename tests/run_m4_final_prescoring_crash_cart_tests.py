#!/usr/bin/env python3
"""Custody-free test target for the non-executing beta crash-cart seam."""
from __future__ import annotations
import hashlib, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IDENTITIES=(
 'specs/data/m4_final_prescoring_crash_cart_beta_contract_v1.json',
 'specs/data/m4_final_prescoring_crash_cart_prompt_inventory_v1.json',
 'specs/data/m4_final_prescoring_full_stack_crash_cart_gate_v1.json',
 'specs/data/m4_final_prescoring_full_stack_crash_cart_launch_contract_v1.json',
 'specs/data/m4_final_prescoring_full_stack_crash_cart_report_schema_v1.json',
 'src/m4_final_prescoring_crash_cart.py',
 'tools/run_m4_final_prescoring_crash_cart.py',
 'tests/test_m4_final_prescoring_crash_cart.py',
 'tests/run_m4_final_prescoring_crash_cart_tests.py',
 'tests/run_m4_final_prescoring_crash_cart_precorrection_probe.py',
 'tests/run_m4_final_prescoring_crash_cart_mutations.py',
)
def verify_identity(relative: str) -> None:
    path=ROOT/relative; sidecar=path.with_name(path.name+'.sha256')
    raw=path.read_bytes()
    if b'\r' in raw or sidecar.read_bytes()!=f'{hashlib.sha256(raw).hexdigest()}  {path.name}\n'.encode('ascii'):
        raise RuntimeError('IDENTITY_OR_LF_MISMATCH:'+relative)
def main() -> int:
    for relative in IDENTITIES: verify_identity(relative)
    contract=json.loads((ROOT/'specs/data/m4_final_prescoring_crash_cart_beta_contract_v1.json').read_text(encoding='utf-8'))
    if contract['execution']['run_authorized'] is not False or contract['artifact_version']!='beta': return 2
    sys.path.insert(0,str(ROOT)); suite=unittest.defaultTestLoader.loadTestsFromName('tests.test_m4_final_prescoring_crash_cart')
    if suite.countTestCases()!=27: return 2
    result=unittest.TextTestRunner(verbosity=2).run(suite); return 0 if result.wasSuccessful() else 1
if __name__=='__main__': raise SystemExit(main())
