import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "diagnostics"))
import l8_g2g4_minimal_full_screen as subject

def test_rho_perfect():
    assert subject.rho_from_dose_means([0,1,2,3]) == 1.0
    assert subject.rho_pass(1.0)
def test_rho_threshold_roundoff():
    rho=subject.rho_from_dose_means([1,0,2,3]); assert abs(rho-.8) <= 1e-12; assert subject.rho_pass(rho)
def test_rho_no_softening(): assert not subject.rho_pass(.8-2*subject.RHO_COMPARE_EPS)
def test_rho_ties(): assert abs(subject.rho_from_dose_means([0,0,2,3])-math.sqrt(.9)) <= 1e-12
def test_rho_constant(): assert subject.rho_from_dose_means([1,1,1,1]) is None
def test_rho_decreasing(): assert subject.rho_from_dose_means([3,2,1,0]) == -1.0
def test_rho_nonfinite(): assert subject.rho_from_dose_means([0,float("nan"),2,3]) is None
def test_complete_aggregation():
    ok=[(.25,.8)]*5
    assert subject.complete_pass(ok)
    assert not subject.complete_pass([(.25,.8),(.19,.8),(.25,.8),(.25,.8),(.25,.8)])
    assert not subject.complete_pass([(.25,.8),(.25,None),(.25,.8),(.25,.8),(.25,.8)])
    assert not subject.complete_pass([(.25,.8),(.25,.8),(.25,.79),(.25,.8),(.25,.8)])
