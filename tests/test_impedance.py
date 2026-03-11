import pytest
import numpy as np
from litho_physics.impedance import compute_acoustic_impedance, reflection_coefficient, impedance_contrast

class TestImpedance:
    def test_compute_impedance(self):
        z = compute_acoustic_impedance(2700, 5000)
        assert z == 2700 * 5000
        assert z > 0
    
    def test_reflection_coefficient(self):
        R = reflection_coefficient(10e6, 15e6)
        assert -1 <= R <= 1
        assert R > 0
