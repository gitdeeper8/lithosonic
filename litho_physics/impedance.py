"""Acoustic Impedance Contrast (Z_c)"""

import numpy as np
from typing import Tuple

def compute_acoustic_impedance(density: float, velocity: float) -> float:
    """
    Compute acoustic impedance
    
    Z = ρ · V_p
    
    Parameters
    ----------
    density : float
        Bulk density (kg/m³)
    velocity : float
        P-wave velocity (m/s)
    
    Returns
    -------
    float
        Acoustic impedance (rayl = kg/m²·s)
    """
    return density * velocity

def reflection_coefficient(z1: float, z2: float) -> float:
    """
    Compute reflection coefficient at interface
    
    R = (Z₂ - Z₁) / (Z₂ + Z₁)
    """
    return (z2 - z1) / (z2 + z1)

def impedance_contrast(z1: float, z2: float) -> float:
    """
    Compute normalized impedance contrast
    
    Z_c = |Z₂ - Z₁| / Z₁
    """
    return abs(z2 - z1) / z1

def classify_lithology(impedance: float) -> str:
    """Classify lithology based on acoustic impedance"""
    if impedance > 15e6:
        return "Granite / High-grade metamorphic"
    elif impedance > 12e6:
        return "Basalt / Gabbro"
    elif impedance > 8e6:
        return "Limestone / Dolomite"
    elif impedance > 5e6:
        return "Sandstone"
    elif impedance > 3e6:
        return "Shale"
    else:
        return "Fracture zone / Fluid-filled void"

# Reference impedance values (rayl)
REFERENCE_IMPEDANCE = {
    'granite': 16.5e6,
    'basalt': 15.0e6,
    'sandstone': 7.5e6,
    'limestone': 10.0e6,
    'shale': 4.0e6,
    'fracture_water': 2.5e6,
    'fracture_gas': 1.0e6,
    'water': 1.5e6,
    'air': 400
}
