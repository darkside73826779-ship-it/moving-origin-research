#!/usr/bin/env python3
"""Prove the new reset-chain regression fails against the reviewed R3 source."""
from __future__ import annotations
import shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIOR="56fadc894eb228927ba904b5c0db3e5032385259"
def main()->int:
 with tempfile.TemporaryDirectory(prefix="m4-crash-cart-probe-")as raw:
  dst=Path(raw)
  for rel in ("tests/__init__.py","tests/test_m4_final_prescoring_crash_cart.py","specs/data/m4_final_prescoring_full_stack_crash_cart_report_schema_v1.json","specs/data/m4_final_prescoring_crash_cart_prompt_inventory_v1.json"):
   (dst/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dst/rel)
  (dst/"src").mkdir(exist_ok=True);(dst/"src/__init__.py").write_bytes(b"")
  prior=subprocess.check_output(["git","show",f"{PRIOR}:src/m4_final_prescoring_crash_cart.py"],cwd=ROOT)
  (dst/"src/m4_final_prescoring_crash_cart.py").write_bytes(prior)
  target="tests.test_m4_final_prescoring_crash_cart.ProductionPathCorrectionTests.test_reset_valid_wrong_prior_is_atomic_rolls_back_and_cleans"
  run=subprocess.run([sys.executable,"-m","unittest",target],cwd=dst,text=True,capture_output=True)
  combined=run.stdout+run.stderr
  if run.returncode==0 or "test_reset_valid_wrong_prior_is_atomic_rolls_back_and_cleans" not in combined:
   print(combined);return 2
  print("PRECORRECTION_KILLED test=reset_valid_wrong_prior prior=56fadc8")
  return 0
if __name__=="__main__":raise SystemExit(main())
