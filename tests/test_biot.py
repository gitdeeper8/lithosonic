import pytest
import numpy as np
from litho_physics.biot import BiotSolver, RockProperties, compute_biot_coupling

class TestBiot:
    def test_biot_coupling_range(self):
        props = RockProperties(
            porosity=0.20,
            permeability=1e-13,
            bulk_modulus_frame=5e9,
            bulk_modulus_grain=40e9,
            bulk_modulus_fluid=2.2e9,
            density_grain=2700,
            density_fluid=1000,
            viscosity_fluid=1e-3
        )
        
        solver = BiotSolver()
        b_c = solver.compute_biot_coupling(props)
        
        assert 0 <= b_c <= 1
    
    def test_critical_frequency(self):
        props = RockProperties(
            porosity=0.20,
            permeability=1e-13,
            bulk_modulus_frame=5e9,
            bulk_modulus_grain=40e9,
            bulk_modulus_fluid=2.2e9,
            density_grain=2700,
            density_fluid=1000,
            viscosity_fluid=1e-3,
            tortuosity=2.0
        )
        
        solver = BiotSolver()
        f_c = solver.critical_frequency(props)
        
        assert 100 < f_c < 200  # Expected ~159 Hz for sandstone
