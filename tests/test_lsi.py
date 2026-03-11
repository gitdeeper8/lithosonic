import pytest
from litho_physics.lsi import LithosphericStressIndex, compute_lsi, get_alert_level

class TestLSI:
    def test_lsi_computation(self):
        params = {
            'b_c': 0.72,
            'z_c': 0.68,
            'f_n': 2.3,
            'alpha_att': 0.77,
            's_ae': 0.83
        }
        
        lsi = compute_lsi(params)
        assert 0 <= lsi <= 1
    
    def test_alert_levels(self):
        calculator = LithosphericStressIndex()
        
        assert calculator.get_alert_code(0.5) == 0  # GREEN
        assert calculator.get_alert_code(0.7) == 1  # YELLOW
        assert calculator.get_alert_code(0.9) == 2  # RED
    
    def test_weights_sum(self):
        calculator = LithosphericStressIndex()
        assert abs(sum(calculator.weights.values()) - 1.0) < 1e-6
