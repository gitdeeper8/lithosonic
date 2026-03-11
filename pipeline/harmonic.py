"""Stage 2: Harmonic analysis and mode identification"""

import numpy as np
from typing import List, Dict

class HarmonicAnalyzer:
    """Identifies harmonic series in spectral peaks"""
    
    def __init__(self, tolerance: float = 0.05):
        self.tolerance = tolerance  # 5% tolerance
    
    def identify_harmonics(self, peaks: List[float]) -> List[Dict]:
        """Identify harmonic series in peaks"""
        peaks = sorted(peaks)
        harmonics = []
        
        for i, f0 in enumerate(peaks):
            series = [f0]
            
            # Look for integer multiples
            for n in range(2, 6):
                target = f0 * n
                closest = min(peaks, key=lambda x: abs(x - target))
                if abs(closest - target) / target < self.tolerance:
                    series.append(closest)
            
            if len(series) >= 2:
                # Determine fracture end condition
                ratios = [f / f0 for f in series]
                is_open = all(abs(r - (i+1)) < self.tolerance for i, r in enumerate(ratios))
                
                harmonics.append({
                    'fundamental': f0,
                    'series': series,
                    'ratios': ratios,
                    'type': 'open' if is_open else 'closed'
                })
        
        return harmonics
    
    def classify_fluid_from_ratios(self, ratios: List[float]) -> str:
        """Classify fluid type from harmonic ratios"""
        # Placeholder - would use more sophisticated ML in real implementation
        if len(ratios) >= 3:
            if abs(ratios[1] - 2.0) < 0.1 and abs(ratios[2] - 3.0) < 0.1:
                return "water"
            elif abs(ratios[1] - 1.5) < 0.1:
                return "gas"
        return "unknown"
