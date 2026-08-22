#!/usr/bin/env python3
"""Deterministic custody-free BF1-R2/BF2-R2 mutation runner."""
from __future__ import annotations
import shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS={
 "telemetry_observed":('samples.append(observed)','samples.extend([])','test_schedule_queue_deadline_and_telemetry'),
 "required_key_schema":('_draft_validate(report,schema,schema)','_bad(any(k not in report for k in schema["required"]),"REPORT_SCHEMA_INVALID")','test_full_top_level_complete_schema_counterexample'),
 "receipt_backend_code":('_bad(receipt.get("backend_code")is not None,"RECEIPT_BACKEND_CODE_INVALID")','pass # mutant','test_invalid_receipt_fails_first_field_and_no_later_evidence'),
 "schedule_wait":('self._wait(target)','pass # mutant','test_schedule_queue_deadline_and_telemetry'),
 "queue_bound":('"max_queue_depth":1','"max_queue_depth":9','test_schedule_queue_deadline_and_telemetry'),
 "deadline":('ACTIVE_DEADLINE_NS=60_000_000_000','ACTIVE_DEADLINE_NS=1','test_schedule_queue_deadline_and_telemetry'),
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
