#!/usr/bin/env python3
"""Deterministic custody-free crash-cart invariant mutation runner."""
from __future__ import annotations
import shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS={
 "telemetry_observed":('samples.append(observed)','samples.extend([])','test_schedule_queue_deadline_and_telemetry'),
 "required_key_schema":('if next(validator.iter_errors(report), None) is not None:','if any(k not in report for k in schema["required"]):','test_full_top_level_complete_schema_counterexample'),
 "receipt_backend_code":('_bad(receipt.get("backend_code") is not None, "RECEIPT_BACKEND_CODE_INVALID")','pass # mutant','test_invalid_receipt_fails_first_field_and_no_later_evidence'),
 "schedule_wait":('self._wait(start + offset)','pass # mutant','test_schedule_queue_deadline_and_telemetry'),
 "queue_bound":('"max_queue_depth": 1','"max_queue_depth": 9','test_schedule_queue_deadline_and_telemetry'),
 "deadline":('ACTIVE_DEADLINE_NS = 60_000_000_000','ACTIVE_DEADLINE_NS = 1','test_schedule_queue_deadline_and_telemetry'),
 "reset_rebind":('self._states = rebound','pass # mutant: retain prior states','test_reset_rebinds_fresh_measured_state_and_active_zero'),
 "post_pair_deadline":('self._assert_pair_completion_within_deadline(start, observed_after)','pass # mutant: accept pair overrun','test_earlier_overrun_and_sleeper_underwait_fail_closed'),
 "warmup_rng_domain":('WARMUP_RNG_DOMAIN = "M4_FINAL_CRASH_CART_WARMUP_V1"','WARMUP_RNG_DOMAIN = "STALE_WARMUP_DOMAIN"','test_governed_constants_and_every_warmup_request_are_exact'),
 "schema_min_properties":('schema = json.loads(schema_path.read_text(encoding="utf-8"))','schema = json.loads(schema_path.read_text(encoding="utf-8"));schema["properties"]["identities"].pop("minProperties",None)','test_schema_rejects_min_properties_and_keyword_neighborhood'),
 "reset_prior_equality":('_bad(not self._digest(prior) or prior != self._states[role],\n             "RESET_PRIOR_STATE_INVALID")','_bad(not self._digest(prior) or False, # mutant: bypass reset prior equality\n             "RESET_PRIOR_STATE_INVALID")','test_reset_valid_wrong_prior_is_atomic_rolls_back_and_cleans'),
}
def main()->int:
 for name,(old,new,test)in TARGETS.items():
  with tempfile.TemporaryDirectory(prefix='m4-mutant-')as raw:
   dst=Path(raw)
   for rel in ('tests/__init__.py','tests/test_m4_final_prescoring_crash_cart.py','specs/data/m4_final_prescoring_full_stack_crash_cart_report_schema_v1.json','specs/data/m4_final_prescoring_crash_cart_prompt_inventory_v1.json'):
    (dst/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dst/rel)
   (dst/'src').mkdir();(dst/'src/__init__.py').write_bytes(b'');shutil.copy2(ROOT/'src/m4_final_prescoring_crash_cart.py',dst/'src/m4_final_prescoring_crash_cart.py')
   p=dst/'src/m4_final_prescoring_crash_cart.py';text=p.read_text();
   if text.count(old)!=1:print('INSTRUMENT_FAILURE',name);return 2
   p.write_text(text.replace(old,new),newline='\n')
   target=f'tests.test_m4_final_prescoring_crash_cart.ProductionPathCorrectionTests.{test}'
   run=subprocess.run([sys.executable,'-m','unittest',target],cwd=dst,text=True,capture_output=True)
   if run.returncode==0 or not('FAIL' in run.stderr or 'ERROR' in run.stderr):print('SURVIVED',name);return 1
   print('KILLED',name,flush=True)
 return 0
if __name__=='__main__':raise SystemExit(main())
