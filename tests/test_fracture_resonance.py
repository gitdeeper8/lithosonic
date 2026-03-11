import pytest
from litho_physics.fracture_resonance import compute_resonance_frequency, FluidPhase

class TestFractureResonance:
    def test_compute_frequency(self):
        f = compute_resonance_frequency(100, FluidPhase.WATER)
        assert f == 1480 / (2 * 100)
        assert f > 0
    
    def test_harmonics(self):
        f1 = compute_resonance_frequency(100, FluidPhase.WATER, 1)
        f2 = compute_resonance_frequency(100, FluidPhase.WATER, 2)
        assert f2 == 2 * f1
