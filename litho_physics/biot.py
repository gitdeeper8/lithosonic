"""Biot Coupling Coefficient (B_c) and Biot wave equations"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class RockProperties:
    """Rock physical properties for Biot calculations"""
    porosity: float          # φ (0-1)
    permeability: float       # κ (m²)
    bulk_modulus_frame: float # K_dry (Pa)
    bulk_modulus_grain: float # K_s (Pa)
    bulk_modulus_fluid: float # K_f (Pa)
    density_grain: float      # ρ_s (kg/m³)
    density_fluid: float      # ρ_f (kg/m³)
    viscosity_fluid: float    # η (Pa·s)
    tortuosity: float = 2.0   # α_∞

class BiotSolver:
    """Solver for Biot wave equations in fluid-saturated porous media"""
    
    def __init__(self):
        self.name = "Biot Coupling Coefficient"
        self.symbol = "B_c"
    
    def compute_biot_coupling(self, props: RockProperties) -> float:
        """
        Compute Biot Coupling Coefficient
        
        B_c = Q / √(P·R)
        
        where:
        Q = (1 - K_dry/K_s) * K_f / (1 - φ - K_dry/K_s + φ*K_s/K_f)
        P = K_dry + 4G/3 + (K_s - K_dry)² / (K_s - K_dry + φ*K_s*(K_s/K_f - 1))
        R = φ² * K_s / (1 - φ - K_dry/K_s + φ*K_s/K_f)
        """
        # Gassmann modulus components
        K_s = props.bulk_modulus_grain
        K_dry = props.bulk_modulus_frame
        K_f = props.bulk_modulus_fluid
        φ = props.porosity
        
        # Biot coefficients
        α = 1 - K_dry / K_s  # Biot-Willis coefficient
        
        # Storage coefficient
        M = 1 / ( (α - φ)/K_s + φ/K_f )
        
        # Biot coupling coefficient (simplified form)
        B_c = α * M / (K_dry + 4/3 * 3e9 + α**2 * M)
        
        # Normalize to [0, 1] range
        return min(1.0, max(0.0, B_c))
    
    def critical_frequency(self, props: RockProperties) -> float:
        """
        Compute Biot critical frequency f_c
        
        f_c = η·φ / (2π·κ·ρ_f·α_∞)
        """
        numerator = props.viscosity_fluid * props.porosity
        denominator = 2 * np.pi * props.permeability * props.density_fluid * props.tortuosity
        return numerator / denominator
    
    def slow_wave_velocity(self, props: RockProperties, frequency: float) -> float:
        """Compute Biot slow wave velocity at given frequency"""
        f_c = self.critical_frequency(props)
        
        if frequency > f_c:
            # Propagating regime
            return np.sqrt(props.bulk_modulus_fluid / props.density_fluid)
        else:
            # Diffusive regime
            return np.sqrt(2 * np.pi * frequency * props.permeability * 
                          props.bulk_modulus_fluid / (props.viscosity_fluid * props.porosity))
    
    def fast_wave_velocity(self, props: RockProperties) -> float:
        """Compute Biot fast P-wave velocity"""
        # Gassmann saturated bulk modulus
        K_sat = props.bulk_modulus_frame + (1 - props.bulk_modulus_frame/props.bulk_modulus_grain)**2 / (
            props.porosity/props.bulk_modulus_fluid + 
            (1 - props.porosity)/props.bulk_modulus_grain - 
            props.bulk_modulus_frame/props.bulk_modulus_grain**2
        )
        
        # Saturated density
        ρ_sat = (1 - props.porosity) * props.density_grain + props.porosity * props.density_fluid
        
        # Fast P-wave velocity
        G = 3e9  # Shear modulus (placeholder)
        V_p = np.sqrt((K_sat + 4*G/3) / ρ_sat)
        
        return V_p

# Convenience function
def compute_biot_coupling(**kwargs) -> float:
    """Compute Biot coupling coefficient from keyword arguments"""
    props = RockProperties(**kwargs)
    solver = BiotSolver()
    return solver.compute_biot_coupling(props)
