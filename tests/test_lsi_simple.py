import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from litho_physics.lsi import LithosphericStressIndex

def test_lsi_computation():
    params = {
        'b_c': 0.72,
        'z_c': 0.68,
        'f_n': 2.3,
        'alpha_att': 0.77,
        's_ae': 0.83
    }
    
    lsi_calc = LithosphericStressIndex()
    lsi = lsi_calc.compute(params)
    
    assert 0 <= lsi <= 1
    print(f"✅ LSI = {lsi:.3f}")

def test_alert_levels():
    lsi_calc = LithosphericStressIndex()
    
    assert lsi_calc.get_alert_code(0.5) == 0  # GREEN
    assert lsi_calc.get_alert_code(0.7) == 1  # YELLOW
    assert lsi_calc.get_alert_code(0.9) == 2  # RED
    
    print("✅ Alert levels test passed")

if __name__ == "__main__":
    test_lsi_computation()
    test_alert_levels()
    print("🎉 All tests passed!")
