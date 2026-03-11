"""Stress-Induced Acoustic Emission Rate (Ṡ_ae)"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Event:
    """Acoustic emission event"""
    timestamp: float
    magnitude: float
    location: Tuple[float, float, float]
    energy: float

class AEClassifier:
    """Acoustic Emission classifier and rate calculator"""
    
    def __init__(self):
        self.name = "Acoustic Emission Rate"
        self.symbol = "Ṡ_ae"
        self.events = []
    
    def add_event(self, event: Event):
        """Add an acoustic emission event"""
        self.events.append(event)
    
    def compute_rate(self, time_window: float = 3600) -> float:
        """
        Compute acoustic emission rate (events per second)
        
        Ṡ_ae = N / Δt
        """
        if not self.events:
            return 0.0
        
        # Count events in last time_window seconds
        latest_time = max(e.timestamp for e in self.events)
        cutoff = latest_time - time_window
        
        recent = [e for e in self.events if e.timestamp >= cutoff]
        
        return len(recent) / time_window
    
    def compute_energy_rate(self, time_window: float = 3600) -> float:
        """
        Compute energy release rate
        
        Ė = ΣE / Δt
        """
        if not self.events:
            return 0.0
        
        latest_time = max(e.timestamp for e in self.events)
        cutoff = latest_time - time_window
        
        recent = [e for e in self.events if e.timestamp >= cutoff]
        total_energy = sum(e.energy for e in recent)
        
        return total_energy / time_window
    
    def compute_b_value(self, min_magnitude: float = -2.0) -> float:
        """
        Compute Gutenberg-Richter b-value
        
        log₁₀ N = a - bM
        """
        if len(self.events) < 10:
            return 1.0
        
        magnitudes = [e.magnitude for e in self.events if e.magnitude >= min_magnitude]
        
        if not magnitudes:
            return 1.0
        
        # Sort magnitudes
        magnitudes.sort()
        
        # Create magnitude bins
        m_min = min(magnitudes)
        m_max = max(magnitudes)
        bins = np.linspace(m_min, m_max, 20)
        
        # Count events per bin
        counts, _ = np.histogram(magnitudes, bins)
        
        # Remove zero counts
        nonzero = counts > 0
        m_center = (bins[:-1] + bins[1:]) / 2
        
        # Linear regression
        log_counts = np.log10(counts[nonzero])
        m_vals = m_center[nonzero]
        
        if len(log_counts) < 2:
            return 1.0
        
        # b is negative of slope
        slope = np.polyfit(m_vals, log_counts, 1)[0]
        b_value = -slope
        
        return max(0.5, min(2.0, b_value))
    
    def get_stress_stage(self, b_value: float) -> str:
        """Identify stress stage from b-value"""
        if b_value < 0.7:
            return "Critical - Imminent failure"
        elif b_value < 0.85:
            return "Accelerating - Crack coalescence"
        elif b_value < 1.0:
            return "Elevated - Crack nucleation"
        else:
            return "Background - Stable"

# Convenience function
def compute_ae_rate(events: List[Event], time_window: float = 3600) -> float:
    """Compute acoustic emission rate"""
    classifier = AEClassifier()
    for event in events:
        classifier.add_event(event)
    return classifier.compute_rate(time_window)
