import unittest
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
