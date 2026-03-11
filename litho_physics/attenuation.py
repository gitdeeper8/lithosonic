"""Acoustic Attenuation Coefficient (α_att)"""

import numpy as np
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class AttenuationParams:
    """Parameters for attenuation calculation"""
    frequency: float        # f (Hz)
    quality_factor: float   # Q (dimensionless)
    velocity: float         # V_p (m/s)
    distance: float = 1.0   # x (m)

class AttenuationMapper:
    """Maps attenuation and quality factor from seismic data"""
    
    def __init__(self):
        self.name = "Acoustic Attenuation"
        self.symbol = "α_att"
    
    def compute_attenuation(self, params: AttenuationParams) -> float:
        """
        Compute attenuation coefficient
        
        α_att = (π · f) / (Q · V_p)
        """
        return (np.pi * params.frequency) / (params.quality_factor * params.velocity)
    
    def amplitude_decay(self, a0: float, alpha: float, distance: float) -> float:
        """
        Compute amplitude after propagation
        
        A(x) = A₀ · exp(-α · x)
        """
        return a0 * np.exp(-alpha * distance)
    
    def compute_q_from_decay(
        self,
        amplitudes: List[float],
        distances: List[float],
        frequency: float,
        velocity: float
    ) -> float:
        """
        Compute quality factor Q from amplitude decay
        
        ln(A₀/A) = (π·f·x) / (Q·V_p)
        """
        if len(amplitudes) < 2 or len(distances) < 2:
            raise ValueError("Need at least 2 measurements")
        
        # Linear regression: y = slope * x
        # where y = ln(A₀/A), slope = π·f / (Q·V_p)
        a0 = amplitudes[0]
        y = [np.log(a0 / a) for a in amplitudes[1:]]
        x = distances[1:]
        
        slope = np.polyfit(x, y, 1)[0]
        
        # Q = π·f / (slope · V_p)
        q = (np.pi * frequency) / (slope * velocity)
        
        return abs(q)
    
    def classify_rock_quality(self, q: float) -> str:
        """Classify rock quality based on Q factor"""
        if q > 200:
            return "Intact rock - Excellent"
        elif q > 100:
            return "Slightly fractured - Good"
        elif q > 50:
            return "Moderately fractured - Fair"
        elif q > 20:
            return "Highly fractured - Poor"
        else:
            return "Intensely fractured / Fluid-saturated - Very Poor"

# Convenience functions
def compute_attenuation_coefficient(frequency: float, q: float, velocity: float) -> float:
    """Compute attenuation coefficient"""
    params = AttenuationParams(frequency, q, velocity)
    mapper = AttenuationMapper()
    return mapper.compute_attenuation(params)

def compute_q_factor(amplitudes: List[float], distances: List[float], 
                     frequency: float, velocity: float) -> float:
    """Compute quality factor Q from amplitude decay"""
    mapper = AttenuationMapper()
    return mapper.compute_q_from_decay(amplitudes, distances, frequency, velocity)
