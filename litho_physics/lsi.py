"""Lithospheric Stress Index (LSI) - Composite of 5 parameters"""

import numpy as np
from typing import Dict, Optional

class LithosphericStressIndex:
    """
    Lithospheric Stress Index calculator
    
    LSI = w₁·B_c + w₂·Z_c + w₃·f_n + w₄·α_att + w₅·Ṡ_ae
    """
    
    def __init__(self):
        # Weights from 14-year training dataset (PCA-derived)
        self.weights = {
            'b_c': 0.22,
            'z_c': 0.18,
            'f_n': 0.24,
            'alpha_att': 0.19,
            's_ae': 0.17
        }
        
        # Normalization bounds from reference dataset
        self.normalization = {
            'b_c': {'min': 0.0, 'max': 1.0},
            'z_c': {'min': 0.0, 'max': 2.0},
            'f_n': {'min': 0.0, 'max': 10.0},
            'alpha_att': {'min': 0.0, 'max': 1.0},
            's_ae': {'min': 0.0, 'max': 2.0}
        }
        
        # Alert thresholds
        self.critical_threshold = 0.80
        self.elevated_threshold = 0.60
    
    def normalize(self, value: float, param: str) -> float:
        """Normalize parameter to [0, 1] range"""
        bounds = self.normalization[param]
        normalized = (value - bounds['min']) / (bounds['max'] - bounds['min'])
        return min(1.0, max(0.0, normalized))
    
    def compute(self, params: Dict[str, float], custom_weights: Optional[Dict] = None) -> float:
        """
        Compute LSI from five parameters
        
        Parameters
        ----------
        params : dict
            Dictionary with keys: b_c, z_c, f_n, alpha_att, s_ae
        custom_weights : dict, optional
            Custom weights for each parameter
        
        Returns
        -------
        float
            Lithospheric Stress Index (0-1)
        """
        weights = custom_weights or self.weights
        
        lsi = 0.0
        for key, weight in weights.items():
            if key in params:
                normalized = self.normalize(params[key], key)
                lsi += weight * normalized
        
        return min(1.0, max(0.0, lsi))
    
    def get_alert_level(self, lsi: float) -> str:
        """Get alert level string from LSI value"""
        if lsi >= self.critical_threshold:
            return "RED - Active Instability"
        elif lsi >= self.elevated_threshold:
            return "YELLOW - Elevated Alert"
        else:
            return "GREEN - Background"
    
    def get_alert_code(self, lsi: float) -> int:
        """Get alert code (0=GREEN, 1=YELLOW, 2=RED)"""
        if lsi >= self.critical_threshold:
            return 2
        elif lsi >= self.elevated_threshold:
            return 1
        else:
            return 0

# Convenience function
def compute_lsi(params: Dict[str, float]) -> float:
    """Compute LSI from parameters"""
    calculator = LithosphericStressIndex()
    return calculator.compute(params)

def get_alert_level(lsi: float) -> str:
    """Get alert level from LSI"""
    calculator = LithosphericStressIndex()
    return calculator.get_alert_level(lsi)
