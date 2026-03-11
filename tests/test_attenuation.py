import pytest
import numpy as np
from litho_physics.attenuation import compute_attenuation_coefficient

class TestAttenuation:
    def test_attenuation_coefficient(self):
        alpha = compute_attenuation_coefficient(10, 100, 3000)
        expected = (np.pi * 10) / (100 * 3000)
        assert alpha == pytest.approx(expected)
