"""Hydraulic Fracture Resonance Frequency (f_n)"""

import numpy as np
from enum import Enum
from typing import List, Optional

class FluidPhase(Enum):
    """Fluid phase types"""
    WATER = "water"
    BRINE = "brine"
    CO2_BRINE = "co2_brine"
    DRY_GAS = "dry_gas"
    MAGMATIC = "magmatic"
    HYDROGEN = "hydrogen"

# Fluid velocities (m/s) at reservoir conditions
FLUID_VELOCITIES = {
    FluidPhase.WATER: 1480,
    FluidPhase.BRINE: 1350,
    FluidPhase.CO2_BRINE: 1200,
    FluidPhase.DRY_GAS: 400,
    FluidPhase.MAGMATIC: 750,
    FluidPhase.HYDROGEN: 1270,
}

# Fluid bulk moduli (Pa)
FLUID_BULK_MODULI = {
    FluidPhase.WATER: 2.2e9,
    FluidPhase.BRINE: 2.4e9,
    FluidPhase.CO2_BRINE: 1.8e9,
    FluidPhase.DRY_GAS: 0.1e9,
    FluidPhase.MAGMATIC: 1.0e9,
    FluidPhase.HYDROGEN: 0.15e9,
}

def compute_resonance_frequency(
    length: float,
    fluid_phase: FluidPhase,
    harmonic: int = 1,
    aperture: Optional[float] = None,
    shear_modulus: float = 3e9
) -> float:
    """
    Compute hydraulic fracture resonance frequency
    
    f_n = (n · V_fluid) / (2L) · √(1 + 2a·K_f / (π·L·μ_rock))
    
    Parameters
    ----------
    length : float
        Fracture half-length (m)
    fluid_phase : FluidPhase
        Type of fluid in fracture
    harmonic : int
        Harmonic number (n = 1, 2, 3, ...)
    aperture : float, optional
        Fracture aperture (m). If None, assumes thin fracture.
    shear_modulus : float
        Rock shear modulus (Pa)
    
    Returns
    -------
    float
        Resonance frequency (Hz)
    """
    v_fluid = FLUID_VELOCITIES[fluid_phase]
    
    # Base frequency
    f_base = (harmonic * v_fluid) / (2 * length)
    
    # Radiation loading correction
    if aperture and aperture > 0:
        k_f = FLUID_BULK_MODULI[fluid_phase]
        correction = np.sqrt(1 + (2 * aperture * k_f) / (np.pi * length * shear_modulus))
    else:
        correction = 1.0
    
    return f_base * correction

def invert_fracture_length(
    frequency: float,
    fluid_phase: FluidPhase,
    harmonic: int = 1
) -> float:
    """
    Invert fracture length from observed resonance frequency
    
    L = (n · V_fluid) / (2f)
    """
    v_fluid = FLUID_VELOCITIES[fluid_phase]
    return (harmonic * v_fluid) / (2 * frequency)

def invert_fracture_aperture(
    frequency: float,
    length: float,
    fluid_phase: FluidPhase,
    shear_modulus: float = 3e9
) -> float:
    """
    Invert fracture aperture from observed frequency
    
    a = (π · L · μ_rock) / (2 · K_f) · ((f/f_base)² - 1)
    """
    v_fluid = FLUID_VELOCITIES[fluid_phase]
    k_f = FLUID_BULK_MODULI[fluid_phase]
    f_base = v_fluid / (2 * length)
    
    if frequency <= f_base:
        return 0.0
    
    ratio = (frequency / f_base) ** 2 - 1
    aperture = (np.pi * length * shear_modulus) * ratio / (2 * k_f)
    
    return max(0, aperture)

def identify_fluid_phase(
    frequency: float,
    length: float,
    aperture: Optional[float] = None
) -> Optional[FluidPhase]:
    """
    Identify fluid phase from measured frequency
    
    Returns
    -------
    FluidPhase or None
        Best matching fluid phase, or None if no good match
    """
    best_match = None
    min_error = float('inf')
    
    for phase in FluidPhase:
        f_pred = compute_resonance_frequency(length, phase, aperture=aperture)
        error = abs(frequency - f_pred) / f_pred
        
        if error < min_error:
            min_error = error
            best_match = phase
    
    # Return best match if error < 15%
    return best_match if min_error < 0.15 else None

def harmonic_series(
    length: float,
    fluid_phase: FluidPhase,
    max_harmonics: int = 5
) -> List[float]:
    """Compute harmonic series up to max_harmonics"""
    return [
        compute_resonance_frequency(length, fluid_phase, n)
        for n in range(1, max_harmonics + 1)
    ]
