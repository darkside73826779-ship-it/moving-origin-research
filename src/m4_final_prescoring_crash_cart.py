"""Custody-free, non-executing M4 crash-cart beta production seam."""
from __future__ import annotations
import hashlib, json, math, re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

WARMUP_PAYLOADS=(0,32,512,1024); WARMUP_MAX_TOKENS=(8,16,16,32); WARMUP_BYTES=(89,122,603,1116)
WARMUP_DIGESTS=("eabe6b7c5cf863599f9444019b68e0e56dde640b824bfb30756aad9faa093485","6b5697332c8ad2d6520655f4dc94133a1c17d4d228e3143f5f9bc80d685a04b4","763187d517d8b35871bc5bb6a5c41df5283fd18f0589348eb299f2d2911076db","5646b4c97252d178f3c73ccd8a2ef988674c7b3f515beb64376d4ea7ab60dd13")
FIXTURE_SIZES=(0,32,64,128,256,512,768,1024); LAW_ORDER=("L7","L8","L10","L14","L18")
HELD_REASONS={"L7":"SCORING_UNAUTHORIZED","L8":"L8_PREREQUISITE_UNCLEARED","L10":"SCORING_UNAUTHORIZED","L14":"SCORING_UNAUTHORIZED","L18":"EF3_ABSENT"}
QUEUE_CAPACITY=8; ACTIVE_DEADLINE_NS=60_000_000_000; TELEMETRY_INTERVAL_NS=250_000_000
STAGES={"PRE_ACTIVE_TERMINAL","PARTIAL_WARMUP_TERMINAL","PARTIAL_ACTIVE_TERMINAL","POST_ACTIVE_TERMINAL","COMPLETE_ACTIVE_TERMINAL"}
FAILURE_STAGES={"PRE_ACTIVE_TERMINAL":{"PRE_START","NEGATIVE_PROBES","MODEL_LOAD"},"PARTIAL_WARMUP_TERMINAL":{"WARMUP","WARMUP_CLEAN_BARRIER"},"PARTIAL_ACTIVE_TERMINAL":{"ACTIVE_WINDOW"},"POST_ACTIVE_TERMINAL":{"RENDER_VALIDATE_SCAN_EXPORT","CLEANUP"}}
RECEIPT_FIELDS={"status","backend_code","session_id","prior_backend_state_sha256","result_backend_state_sha256","request_sha256","request_ordinal"}

class CrashCartError(RuntimeError): pass
def sha256(value:bytes)->str:return hashlib.sha256(value).hexdigest()
def canonical_bytes(value:Any)->bytes:return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def _bad(condition:bool,code:str)->None:
    if condition: raise CrashCartError(code)
def warmup_prompt(ordinal:int,payload_bytes:int)->bytes:
    _bad(type(ordinal)is not int or not 0<=ordinal<4 or payload_bytes!=WARMUP_PAYLOADS[ordinal],"WARMUP_CONTRACT_MISMATCH")
    raw=(f"M4_WARMUP_PUBLIC_V1\nordinal={ordinal:04d}\npayload_bytes={payload_bytes}\npayload={'x'*payload_bytes}\nRespond with the ordinal only.\n").encode()
    _bad(raw.count(b'\n')!=5 or b'\\n'in raw or len(raw)!=WARMUP_BYTES[ordinal] or sha256(raw)!=WARMUP_DIGESTS[ordinal],"WARMUP_CONTRACT_MISMATCH")
    return raw
def warmup_plan():
    return tuple({"ordinal":i,"prompt":warmup_prompt(i,n),"prompt_sha256":WARMUP_DIGESTS[i],"max_output_tokens":WARMUP_MAX_TOKENS[i],"temperature":0,"seed":0,"rng_domain":"PUBLIC_WARMUP_V1","top_p":1.0,"top_k":-1,"n":1,"presence_penalty":0,"frequency_penalty":0,"stop":[],"logprobs":False,"prefix_caching":False,"pair_timeout_ns":30_000_000_000,"sequence_deadline_ns":120_000_000_000,"clean_barrier_deadline_ns":10_000_000_000} for i,n in enumerate(WARMUP_PAYLOADS))
def active_schedule():return tuple(0 if i<16 else(i-15)*625_000_000 for i in range(64))
def telemetry_schedule():return tuple(range(0,ACTIVE_DEADLINE_NS+1,TELEMETRY_INTERVAL_NS))
def public_fixture(i:int):
    _bad(type(i)is not int or not 0<=i<64,"ACTIVE_ORDINAL_INVALID");f,r=i%8,i//8
    text=f"M4_CRASH_CART_PUBLIC_V1\nordinal={i:04d}\nfamily={f}\nrepetition={r}\npayload={'x'*FIXTURE_SIZES[f]}\n"
    return {"ordinal":i,"fixture_id":f"family-{f}-repeat-{r}","payload_bytes":FIXTURE_SIZES[f],"public_prompt_text":text,"prompt_sha256":sha256(text.encode())}
def fixture_inventory():return tuple(public_fixture(i)for i in range(64))
def held_laws():return tuple({"law_id":law,"status":"HELD","claim_made":False,"meaning_source":f"docs/ARCHITECTURAL_CONSTITUTION_v2.md:{line}","evidence":[],"metrics":{},"failure_code":None,"held_reason":HELD_REASONS[law]}for law,line in zip(LAW_ORDER,(26,28,32,42,54)))

def _resolve(root,ref):
    node=root
    for part in ref[2:].split("/"):node=node[part.replace("~1","/").replace("~0","~")]
    return node
def _matches(value,kind):
    return {"object":isinstance(value,dict),"array":isinstance(value,list),"string":isinstance(value,str),"integer":type(value)is int,"number":isinstance(value,(int,float))and not isinstance(value,bool),"boolean":type(value)is bool,"null":value is None}.get(kind,False)
def _valid(value,schema,root):
    try:_draft_validate(value,schema,root);return True
    except CrashCartError:return False
def _draft_validate(value,schema,root):
    if schema is True:return
    if schema is False:raise CrashCartError("REPORT_SCHEMA_INVALID")
    if "$ref"in schema:return _draft_validate(value,_resolve(root,schema["$ref"]),root)
    if "const"in schema:_bad(value!=schema["const"],"REPORT_SCHEMA_INVALID")
    if "enum"in schema:_bad(value not in schema["enum"],"REPORT_SCHEMA_INVALID")
    if "type"in schema:
        kinds=schema["type"]if isinstance(schema["type"],list)else[schema["type"]];_bad(not any(_matches(value,k)for k in kinds),"REPORT_SCHEMA_INVALID")
    if "oneOf"in schema:_bad(sum(_valid(value,x,root)for x in schema["oneOf"])!=1,"REPORT_SCHEMA_INVALID")
    if "anyOf"in schema:_bad(not any(_valid(value,x,root)for x in schema["anyOf"]),"REPORT_SCHEMA_INVALID")
    for child in schema.get("allOf",[]):_draft_validate(value,child,root)
    if "if"in schema:
        if _valid(value,schema["if"],root):_draft_validate(value,schema.get("then",{}),root)
        elif "else"in schema:_draft_validate(value,schema["else"],root)
    if isinstance(value,dict):
        _bad(any(k not in value for k in schema.get("required",[])),"REPORT_SCHEMA_INVALID");props=schema.get("properties",{})
        _bad(schema.get("additionalProperties")is False and any(k not in props for k in value),"REPORT_SCHEMA_INVALID")
        _bad(len(value)>schema.get("maxProperties",math.inf),"REPORT_SCHEMA_INVALID")
        for k,v in value.items():
            if k in props:_draft_validate(v,props[k],root)
            elif isinstance(schema.get("additionalProperties"),dict):_draft_validate(v,schema["additionalProperties"],root)
    if isinstance(value,list):
        _bad(len(value)<schema.get("minItems",0)or len(value)>schema.get("maxItems",math.inf),"REPORT_SCHEMA_INVALID")
        if schema.get("uniqueItems"):_bad(len({json.dumps(x,sort_keys=True)for x in value})!=len(value),"REPORT_SCHEMA_INVALID")
        prefix=schema.get("prefixItems",[])
        for i,child in enumerate(prefix):
            if i<len(value):_draft_validate(value[i],child,root)
        items=schema.get("items")
        if items is False:_bad(len(value)>len(prefix),"REPORT_SCHEMA_INVALID")
        elif isinstance(items,(dict,bool)):
            for item in value[len(prefix):]:_draft_validate(item,items,root)
    if isinstance(value,str):_bad(len(value)<schema.get("minLength",0)or("pattern"in schema and re.search(schema["pattern"],value)is None),"REPORT_SCHEMA_INVALID")
    if isinstance(value,(int,float))and not isinstance(value,bool):_bad(not math.isfinite(value)or value<schema.get("minimum",-math.inf)or value>schema.get("maximum",math.inf),"REPORT_SCHEMA_INVALID")
def _compose_schema(report:Mapping[str,Any])->None:
    schema=json.loads((Path(__file__).resolve().parents[1]/"specs/data/m4_final_prescoring_full_stack_crash_cart_report_schema_v1.json").read_text(encoding="utf-8"));_draft_validate(report,schema,schema)
def validate_terminal(r:Mapping[str,Any])->None:
    _bad(not isinstance(r,Mapping)or r.get("evidence_stage")not in STAGES,"EVIDENCE_STAGE_INVALID");_compose_schema(r)
    s=r["evidence_stage"];rows=r["rows"];samples=r["resource_samples"];w=r["warmup"];a=r["active_window"];tr=r["trends"];rep=r["replica_consistency"]
    _bad(not isinstance(rows,list)or not isinstance(samples,list),"REPORT_SCHEMA_INVALID")
    if s=="COMPLETE_ACTIVE_TERMINAL":
        _bad(r["failure_stage"]is not None or r["failure"]is not None or r["structural_status"]!="PASS","COMPLETE_TERMINAL_INVALID")
        _bad(not isinstance(w,Mapping)or w.get("status")!="PASS"or w.get("attempted_pair_count")!=4 or len(w.get("rows",[]))!=4 or any(not isinstance(x,Mapping)or x.get("candidate")is None or x.get("peer")is None for x in w.get("rows",[])),"COMPLETE_EVIDENCE_MISSING")
        _bad(not isinstance(a,Mapping)or a.get("status")!="PASS"or a.get("attempted_pair_count")!=64 or a.get("completed_pair_count")!=64 or a.get("drop_count")!=0 or a.get("duration_ns",0)<30_000_000_000,"COMPLETE_EVIDENCE_MISSING")
        _bad(len(rows)!=64 or any(not isinstance(x,Mapping)or x.get("ordinal")!=i or x.get("candidate")is None or x.get("peer")is None for i,x in enumerate(rows))or len(samples)<121 or any(not isinstance(x,Mapping)or not x for x in samples)or not isinstance(tr,Mapping)or not tr,"COMPLETE_EVIDENCE_MISSING")
        _bad(not isinstance(rep,Mapping)or rep.get("status")not in{"MATCH","MISMATCH"}or r["laws"]not in(list(held_laws()),held_laws()),"COMPLETE_EVIDENCE_MISSING")
        cleanup=r["cleanup"];public=r["public_safety"];export=r["export"]
        _bad(not isinstance(cleanup,Mapping)or cleanup.get("status")!="PASS"or cleanup.get("attempted")is not True or not isinstance(public,Mapping)or public.get("status")!="CLEAR"or not isinstance(export,Mapping)or export.get("status")!="EXPORTED"or export.get("reproduction_equal")is not True,"COMPLETE_EVIDENCE_MISSING");return
    failure=r["failure"];fs=r["failure_stage"]
    _bad(fs not in FAILURE_STAGES.get(s,set())or not isinstance(failure,Mapping)or failure.get("stage")!=fs or failure.get("retry_count")!=0 or r["structural_status"]not in{"BLOCKED","INSTRUMENT_FAILURE"},"FAILURE_PROJECTION_INVALID")
    if s=="PRE_ACTIVE_TERMINAL":_bad(w is not None or a is not None or rows or samples or tr is not None or rep.get("status")!="NOT_RUN","FABRICATED_LATER_STAGE_EVIDENCE")
    elif s=="PARTIAL_WARMUP_TERMINAL":_bad(not isinstance(w,Mapping)or w.get("status")!="FAIL"or len(w.get("rows",[]))>4 or a is not None or rows or samples or tr is not None,"FABRICATED_LATER_STAGE_EVIDENCE")
    elif s=="PARTIAL_ACTIVE_TERMINAL":_bad(not isinstance(w,Mapping)or w.get("status")!="PASS"or w.get("attempted_pair_count")!=4 or len(w.get("rows",[]))!=4 or not isinstance(a,Mapping)or a.get("status")!="FAIL"or len(rows)>64 or tr is not None or rep.get("status")!="NOT_RUN","FABRICATED_LATER_STAGE_EVIDENCE")
    else:_bad(not isinstance(w,Mapping)or w.get("status")!="PASS"or not isinstance(a,Mapping)or a.get("status")!="PASS"or len(rows)!=64 or len(samples)<121 or not isinstance(r["cleanup"],Mapping),"FABRICATED_LATER_STAGE_EVIDENCE")

def exact_replica_consumer_stop(replica):
    if replica.get("status")=="MISMATCH":raise CrashCartError("EXACT_REPLICA_CONSUMER_STOP")
def execution_guard(value):
    if value is not False:raise CrashCartError("RUN_AUTHORITY_INVALID")
    raise CrashCartError("RUN_AUTHORITY_ABSENT")

@dataclass
class CrashCartLifecycle:
    candidate:Callable;peer:Callable;reset:Callable;cleanup:Callable
    clock_ns:Callable[[],int]|None=None;sleep_until_ns:Callable[[int],None]|None=None;sampler:Callable[[int,int],Mapping[str,Any]]|None=None
    events:list[str]=field(default_factory=list);_virtual_ns:int=0;_states:dict[str,str]=field(default_factory=lambda:{"candidate":"0"*64,"peer":"0"*64})
    def _now(self):return self.clock_ns()if self.clock_ns else self._virtual_ns
    def _wait(self,target):
        if self.sleep_until_ns:self.sleep_until_ns(target)
        else:self._virtual_ns=max(self._virtual_ns,target)
        _bad(self._now()<target,"SCHEDULE_BYPASS")
    def _pair(self,kind,ordinal,item):
        controls=warmup_plan()[ordinal]if kind=="warmup"else{"temperature":0,"top_p":1.0,"top_k":-1,"n":1,"presence_penalty":0,"frequency_penalty":0,"stop":[],"logprobs":False,"prefix_caching":False}
        req={"kind":kind,"ordinal":ordinal,"fixture_id":item.get("fixture_id"),"prompt_sha256":item["prompt_sha256"],"controls":{k:v for k,v in controls.items()if k not in{"prompt"}}};self.events.append(f"{kind}-barrier-{ordinal}")
        with ThreadPoolExecutor(max_workers=2)as pool:
            ca=pool.submit(self.candidate,req);pe=pool.submit(self.peer,req);out=(ca.result(),pe.result())
        expected_hash=sha256(canonical_bytes(req));sessions=[]
        for role,receipt in zip(("candidate","peer"),out):
            _bad(set(receipt)!=RECEIPT_FIELDS,"RECEIPT_SHAPE_INVALID")
            _bad(receipt.get("status")!="PASS","RECEIPT_STATUS_INVALID");_bad(receipt.get("backend_code")is not None,"RECEIPT_BACKEND_CODE_INVALID")
            session=receipt.get("session_id");_bad(not isinstance(session,str)or session!=role,"RECEIPT_SESSION_INVALID");sessions.append(session)
            _bad(receipt.get("request_sha256")!=expected_hash,"RECEIPT_REQUEST_DIGEST_INVALID")
            prior=receipt.get("prior_backend_state_sha256");result=receipt.get("result_backend_state_sha256")
            _bad(not isinstance(prior,str)or re.fullmatch(r"[0-9a-f]{64}",prior)is None or prior!=self._states[role],"RECEIPT_PRIOR_STATE_INVALID")
            _bad(not isinstance(result,str)or re.fullmatch(r"[0-9a-f]{64}",result)is None,"RECEIPT_RESULT_STATE_INVALID")
            _bad(receipt.get("request_ordinal")!=ordinal,"RECEIPT_ORDINAL_INVALID");self._states[role]=result
        _bad(sessions[0]==sessions[1],"SHARED_SESSION_INVALID")
        return out
    def warmup(self):
        self.reset("candidate");self.reset("peer");self._states={"candidate":"0"*64,"peer":"0"*64};out=[self._pair("warmup",x["ordinal"],x)for x in warmup_plan()]
        self.reset("candidate");self.reset("peer");self.events.extend(("clean-barrier","rng-after-clean-barrier"));return out
    def active(self):
        _bad("rng-after-clean-barrier"not in self.events,"RNG_INSERTION_INVALID")
        start=self._now();samples=[];out=[];next_sample=start
        for item,offset in zip(fixture_inventory(),active_schedule()):
            target=start+offset;self._wait(target)
            self.events.append(f"dispatch@{self._now()-start}")
            _bad(self._now()-start>ACTIVE_DEADLINE_NS,"ACTIVE_WINDOW_TIMEOUT_NO_RETRY")
            while next_sample<=self._now():
                observed=dict(self.sampler(next_sample,len(out)))if self.sampler else{"monotonic_ns":next_sample,"queue_depth_pairs":0,"completed_pair_count":len(out)}
                _bad(observed.get("monotonic_ns")!=next_sample,"TELEMETRY_OBSERVATION_INVALID");samples.append(observed);next_sample+=TELEMETRY_INTERVAL_NS
            self.events.append("queue-depth-1");_bad(1>QUEUE_CAPACITY,"QUEUE_CAPACITY_EXCEEDED");out.append(self._pair("active",item["ordinal"],item))
        _bad(self._now()-start<30_000_000_000,"ACTIVE_WINDOW_TOO_SHORT");return out,samples
    def run(self):
        try:
            warm=self.warmup();active,samples=self.active();return {"warmup_ordinals":[x[0]["request_ordinal"]for x in warm],"active_ordinals":[x[0]["request_ordinal"]for x in active],"dispatch_observed_ns":[int(x.split("@")[-1])for x in self.events if x.startswith("dispatch@")],"telemetry":samples,"max_queue_depth":1}
        except Exception as exc:
            self.events.append("rollback");self.reset("candidate");self.reset("peer")
            if isinstance(exc,CrashCartError):raise
            raise CrashCartError("PAIR_ROLLBACK")from exc
        finally:self.cleanup();self.events.append("cleanup")
