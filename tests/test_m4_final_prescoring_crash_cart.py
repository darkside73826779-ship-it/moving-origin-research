import unittest
from pathlib import Path
import json
from src.m4_final_prescoring_crash_cart import *

class CrashCartBetaTests(unittest.TestCase):
 def test_warmup_exact(self):
  plan=warmup_plan(); self.assertEqual([len(x['prompt']) for x in plan], list(WARMUP_BYTES)); self.assertEqual([x['prompt_sha256'] for x in plan], list(WARMUP_DIGESTS))
 def test_warmup_rejects_drift(self):
  with self.assertRaises(CrashCartError): warmup_prompt(0, 32)
 def test_schedule_and_fixtures(self):
  self.assertEqual(len(active_schedule()),64); self.assertEqual(active_schedule()[15],0); self.assertEqual(active_schedule()[16],625_000_000); self.assertEqual(active_schedule()[-1],30_000_000_000)
  self.assertEqual([public_fixture(i)['payload_bytes'] for i in range(8)],list(FIXTURE_SIZES))
 def test_held_laws_are_exact_and_non_scoring(self):
  laws=held_laws(); self.assertEqual([x['law_id'] for x in laws],list(LAW_ORDER)); self.assertTrue(all(not x['claim_made'] and x['evidence']==[] and x['metrics']=={} for x in laws))
 def test_pre_active_rejects_fabricated_rows(self):
  with self.assertRaises(CrashCartError): validate_terminal({'evidence_stage':'PRE_ACTIVE_TERMINAL','warmup':None,'active_window':None,'rows':[{}],'failure':{'retry_count':0}})
 def test_complete_requires_full_evidence(self):
  with self.assertRaises(CrashCartError): validate_terminal({'evidence_stage':'COMPLETE_ACTIVE_TERMINAL','warmup':{},'active_window':{},'rows':[],'failure':None,'failure_stage':None,'structural_status':'PASS'})
 def test_replica_mismatch_stops_consumer(self):
  with self.assertRaisesRegex(CrashCartError,'EXACT_REPLICA'): exact_replica_consumer_stop({'status':'MISMATCH'})
 def test_wrapper_guard_never_starts_runtime(self):
  with self.assertRaisesRegex(CrashCartError,'RUN_AUTHORITY_ABSENT'): execution_guard(False)

if __name__ == '__main__': unittest.main()

class ProductionPathCorrectionTests(unittest.TestCase):
 def _role(self,name,events,fail=None):
  def call(req):
   events.append((name,req['kind'],req['ordinal']))
   if fail==(req['kind'],req['ordinal']): raise RuntimeError('injected')
   z='0'*64
   return {'status':'PASS','backend_code':None,'session_id':name,'prior_backend_state_sha256':z,'result_backend_state_sha256':'1'*64,'request_sha256':sha256(json.dumps(req,sort_keys=True,separators=(',',':')).encode()),'request_ordinal':req['ordinal']}
  return call
 def test_candidate_warmup_zero_failure_rolls_back_resets_and_cleans(self):
  e=[];life=CrashCartLifecycle(self._role('candidate',e,('warmup',0)),self._role('peer',e),lambda r:e.append(('reset',r)),lambda:e.append(('cleanup',)))
  with self.assertRaises(CrashCartError): life.run()
  self.assertIn(('cleanup',),e);self.assertIn(('reset','candidate'),e);self.assertIn(('reset','peer'),e);self.assertTrue(any(x[:2]==('peer','warmup') for x in e if len(x)>1))
 def test_symmetric_barriers_resets_rng_no_priming_and_receipt_ordinals(self):
  e=[];life=CrashCartLifecycle(self._role('candidate',e),self._role('peer',e),lambda r:e.append(('reset',r)),lambda:e.append(('cleanup',)))
  out=life.run();self.assertEqual(out['active_ordinals'],list(range(64)));self.assertEqual(out['warmup_ordinals'],list(range(4)));self.assertEqual(life.events.count('clean-barrier'),1);self.assertLess(life.events.index('clean-barrier'),life.events.index('rng-after-clean-barrier'));self.assertNotIn(-1,out['active_ordinals'])
 def test_schedule_queue_deadline_and_telemetry(self):
  self.assertEqual(active_schedule()[-1],30_000_000_000);self.assertEqual(QUEUE_CAPACITY,8);self.assertEqual(ACTIVE_DEADLINE_NS,60_000_000_000);self.assertEqual(TELEMETRY_INTERVAL_NS,250_000_000)
  self.assertEqual(len(telemetry_schedule()),241)
 def test_inventory_is_committed_ordered_unique_and_exact(self):
  bound=json.loads(Path('specs/data/m4_final_prescoring_crash_cart_prompt_inventory_v1.json').read_text())['sha256']
  actual=[x['prompt_sha256'] for x in fixture_inventory()];self.assertEqual(actual,bound);self.assertEqual(len(set(actual)),64)
 def test_strict_schema_counterexamples(self):
  cases=[
   {'evidence_stage':'PRE_ACTIVE_TERMINAL','failure_stage':'CLEANUP','failure':{'stage':'CLEANUP','retry_count':0},'structural_status':'BLOCKED','rows':[],'resource_samples':[],'warmup':None,'active_window':None,'trends':{},'replica_consistency':{'status':'MATCH'}},
   {'evidence_stage':'PARTIAL_ACTIVE_TERMINAL','failure_stage':'ACTIVE_WINDOW','failure':{'stage':'ACTIVE_WINDOW','retry_count':0},'structural_status':'BLOCKED','rows':[{}],'resource_samples':[{}],'warmup':{'status':'PASS'},'active_window':{'status':'FAIL'},'trends':None,'replica_consistency':{'status':'MATCH'}},
   {'evidence_stage':'POST_ACTIVE_TERMINAL','failure_stage':'CLEANUP','failure':{'stage':'CLEANUP','retry_count':0},'structural_status':'BLOCKED','rows':[{}]*64,'resource_samples':[{}]*121,'warmup':{'status':'PASS'},'active_window':{'status':'PASS'},'trends':{},'replica_consistency':{'status':'MATCH'}},
   {'evidence_stage':'COMPLETE_ACTIVE_TERMINAL','failure_stage':None,'failure':None,'structural_status':'PASS','rows':[{}]*64,'resource_samples':[{}]*121,'warmup':{'status':'PASS','attempted_pair_count':4,'rows':[{}]*4},'active_window':{'status':'PASS','attempted_pair_count':64,'completed_pair_count':64,'drop_count':0,'duration_ns':30_000_000_000},'trends':{},'replica_consistency':{'status':'MATCH'},'cleanup':{'status':'PASS'},'public_safety':{'status':'CLEAR'},'export':{'status':'EXPORTED'}}]
  for case in cases:
   with self.subTest(stage=case['evidence_stage']),self.assertRaises(CrashCartError):validate_terminal(case)
