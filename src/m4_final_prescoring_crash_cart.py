"""Custody-free, non-executing M4 crash-cart beta production seam."""
from __future__ import annotations
import hashlib,json
from dataclasses import dataclass,field
from typing import Any,Callable,Mapping
P=(0,32,512,1024); M=(8,16,16,32); B=(89,122,603,1116)
D=("eabe6b7c5cf863599f9444019b68e0e56dde640b824bfb30756aad9faa093485","6b5697332c8ad2d6520655f4dc94133a1c17d4d228e3143f5f9bc80d685a04b4","763187d517d8b35871bc5bb6a5c41df5283fd18f0589348eb299f2d2911076db","5646b4c97252d178f3c73ccd8a2ef988674c7b3f515beb64376d4ea7ab60dd13")
FIX=(0,32,64,128,256,512,768,1024); LAW=("L7","L8","L10","L14","L18"); REASON={"L7":"SCORING_UNAUTHORIZED","L8":"L8_PREREQUISITE_UNCLEARED","L10":"SCORING_UNAUTHORIZED","L14":"SCORING_UNAUTHORIZED","L18":"EF3_ABSENT"}
WARMUP_PAYLOADS=P; WARMUP_MAX_TOKENS=M; WARMUP_BYTES=B; WARMUP_DIGESTS=D; FIXTURE_SIZES=FIX; LAW_ORDER=LAW
STAGES={"PRE_ACTIVE_TERMINAL","PARTIAL_WARMUP_TERMINAL","PARTIAL_ACTIVE_TERMINAL","POST_ACTIVE_TERMINAL","COMPLETE_ACTIVE_TERMINAL"}; FS={"PRE_ACTIVE_TERMINAL":{"PRE_START","NEGATIVE_PROBES","MODEL_LOAD"},"PARTIAL_WARMUP_TERMINAL":{"WARMUP","WARMUP_CLEAN_BARRIER"},"PARTIAL_ACTIVE_TERMINAL":{"ACTIVE_WINDOW"},"POST_ACTIVE_TERMINAL":{"RENDER_VALIDATE_SCAN_EXPORT","CLEANUP"}}
class CrashCartError(RuntimeError):pass
def sha256(x:bytes)->str:return hashlib.sha256(x).hexdigest()
def warmup_prompt(o:int,n:int)->bytes:
 if type(o)is not int or not 0<=o<4 or n!=P[o]:raise CrashCartError('WARMUP_CONTRACT_MISMATCH')
 x=(f"M4_WARMUP_PUBLIC_V1\nordinal={o:04d}\npayload_bytes={n}\npayload={'x'*n}\nRespond with the ordinal only.\n").encode()
 if x.count(b'\n')!=5 or b'\\n'in x or len(x)!=B[o] or sha256(x)!=D[o]:raise CrashCartError('WARMUP_CONTRACT_MISMATCH')
 return x
def warmup_plan():return tuple({'ordinal':i,'prompt':warmup_prompt(i,n),'prompt_sha256':D[i],'max_output_tokens':M[i],'temperature':0,'seed':0,'top_p':1.0,'top_k':-1,'n':1,'presence_penalty':0,'frequency_penalty':0,'stop':[],'logprobs':False,'prefix_caching':False,'pair_timeout_ns':30_000_000_000}for i,n in enumerate(P))
def active_schedule():return tuple(0 if i<16 else(i-15)*625_000_000 for i in range(64))
def public_fixture(i:int):
 if type(i)is not int or not 0<=i<64:raise CrashCartError('ACTIVE_ORDINAL_INVALID')
 f,r=i%8,i//8;t=f"M4_CRASH_CART_PUBLIC_V1\nordinal={i:04d}\nfamily={f}\nrepetition={r}\npayload={'x'*FIX[f]}\n";return {'ordinal':i,'fixture_id':f'family-{f}-repeat-{r}','payload_bytes':FIX[f],'public_prompt_text':t,'prompt_sha256':sha256(t.encode())}
def fixture_inventory():return tuple(public_fixture(i)for i in range(64))
def held_laws():return tuple({'law_id':x,'status':'HELD','claim_made':False,'meaning_source':f'docs/ARCHITECTURAL_CONSTITUTION_v2.md:{n}','evidence':[],'metrics':{},'failure_code':None,'held_reason':REASON[x]}for x,n in zip(LAW,(26,28,32,42,54)))
def _bad(c:bool,s:str):
 if c:raise CrashCartError(s)
def validate_terminal(r:Mapping[str,Any])->None:
 _bad(not isinstance(r,Mapping)or r.get('evidence_stage')not in STAGES,'EVIDENCE_STAGE_INVALID');s=r['evidence_stage'];rows=r.get('rows',[]);samples=r.get('resource_samples',[]);w=r.get('warmup');a=r.get('active_window');tr=r.get('trends');rep=r.get('replica_consistency');f=r.get('failure');fs=r.get('failure_stage')
 _bad(not isinstance(rows,list)or not isinstance(samples,list),'REPORT_INVALID')
 if s=='COMPLETE_ACTIVE_TERMINAL':
  _bad(fs is not None or f is not None or r.get('structural_status')!='PASS','COMPLETE_TERMINAL_INVALID');_bad(not isinstance(w,Mapping)or w.get('status')!='PASS'or w.get('attempted_pair_count')!=4 or len(w.get('rows',[]))!=4,'COMPLETE_EVIDENCE_MISSING');_bad(not isinstance(a,Mapping)or a.get('status')!='PASS'or a.get('attempted_pair_count')!=64 or a.get('completed_pair_count')!=64 or a.get('drop_count')!=0 or a.get('duration_ns',0)<30_000_000_000,'COMPLETE_EVIDENCE_MISSING');_bad(len(rows)!=64 or len(samples)<121 or not isinstance(tr,Mapping)or not isinstance(rep,Mapping)or rep.get('status')not in{'MATCH','MISMATCH'},'COMPLETE_EVIDENCE_MISSING');_bad(not isinstance(r.get('cleanup'),Mapping)or r['cleanup'].get('status')!='PASS'or not isinstance(r.get('public_safety'),Mapping)or r['public_safety'].get('status')!='CLEAR'or not isinstance(r.get('export'),Mapping)or r['export'].get('status')!='EXPORTED','COMPLETE_EVIDENCE_MISSING');return
 _bad(fs not in FS.get(s,set())or not isinstance(f,Mapping)or f.get('retry_count')!=0 or f.get('stage')!=fs or r.get('structural_status')not in{'BLOCKED','INSTRUMENT_FAILURE'},'FAILURE_PROJECTION_INVALID')
 if s=='PRE_ACTIVE_TERMINAL':_bad(w is not None or a is not None or rows or samples or tr is not None or(isinstance(rep,Mapping)and rep.get('status')!='NOT_RUN'),'FABRICATED_LATER_STAGE_EVIDENCE')
 elif s=='PARTIAL_WARMUP_TERMINAL':_bad(not isinstance(w,Mapping)or w.get('status')!='FAIL'or len(w.get('rows',[]))>4 or a is not None or rows or samples or tr is not None,'FABRICATED_LATER_STAGE_EVIDENCE')
 elif s=='PARTIAL_ACTIVE_TERMINAL':_bad(not isinstance(w,Mapping)or w.get('status')!='PASS'or not isinstance(a,Mapping)or a.get('status')!='FAIL'or len(rows)>64 or tr is not None,'FABRICATED_LATER_STAGE_EVIDENCE')
 else:_bad(not isinstance(w,Mapping)or w.get('status')!='PASS'or not isinstance(a,Mapping)or a.get('status')!='PASS'or len(rows)!=64 or len(samples)<121,'FABRICATED_LATER_STAGE_EVIDENCE')
def exact_replica_consumer_stop(x):
 if x.get('status')=='MISMATCH':raise CrashCartError('EXACT_REPLICA_CONSUMER_STOP')
def execution_guard(x):
 if x is not False:raise CrashCartError('RUN_AUTHORITY_INVALID')
 raise CrashCartError('RUN_AUTHORITY_ABSENT')
@dataclass
class CrashCartLifecycle:
 candidate:Callable;peer:Callable;reset:Callable;cleanup:Callable;events:list[str]=field(default_factory=list)
 def warmup(self):
  for x in warmup_plan():self.events.append(f"barrier-{x['ordinal']}");self.candidate(x);self.peer(x)
  self.reset('candidate');self.reset('peer');self.events+=['clean-barrier','rng-after-clean-barrier']
 def active(self):
  _bad('rng-after-clean-barrier'not in self.events,'RNG_INSERTION_INVALID')
  return tuple((self.candidate(x),self.peer(x))for x in fixture_inventory())
 def close(self):self.cleanup();self.events.append('cleanup')
