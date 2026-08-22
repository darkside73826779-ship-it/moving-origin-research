#!/usr/bin/env python3
"""Prove the committed BF1-BF3 tests fail against ff163541."""
from __future__ import annotations
import shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIOR="3f9f685a1f88c9f18f916688ce9a574f19e246e8"
def main()->int:
 with tempfile.TemporaryDirectory(prefix="m4-crash-cart-probe-")as raw:
  dst=Path(raw)
  for rel in ("tests/__init__.py","tests/test_m4_final_prescoring_crash_cart.py","specs/data/m4_final_prescoring_full_stack_crash_cart_report_schema_v1.json","specs/data/m4_final_prescoring_crash_cart_prompt_inventory_v1.json"):
   (dst/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dst/rel)
  (dst/"src").mkdir(exist_ok=True);(dst/"src/__init__.py").write_bytes(b"")
  prior=subprocess.check_output(["git","show",f"{PRIOR}:src/m4_final_prescoring_crash_cart.py"],cwd=ROOT)
  (dst/"src/m4_final_prescoring_crash_cart.py").write_bytes(prior)
  run=subprocess.run([sys.executable,"-m","unittest","tests.test_m4_final_prescoring_crash_cart"],cwd=dst,text=True,capture_output=True)
  combined=run.stdout+run.stderr
  expected=("dispatch_observed_ns","CrashCartError not raised")
  if run.returncode==0 or not all(item in combined for item in expected):
   print(combined);return 2
  print("PRECORRECTION_KILLED tests=15 prior=3f9f685")
  return 0
if __name__=="__main__":raise SystemExit(main())
