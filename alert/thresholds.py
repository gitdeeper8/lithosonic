"""Alert threshold management"""

from typing import Dict, Optional

class AlertThresholds:
    """Manages LSI alert thresholds"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # Default thresholds from research paper
        self.background_max = self.config.get('background_max', 0.60)
        self.critical_min = self.config.get('critical_min', 0.80)
    
    def evaluate(self, lsi: float) -> Dict:
        """Evaluate alert level for given LSI"""
        if lsi >= self.critical_min:
            return {
                'level': 'RED',
                'name': 'Active Instability',
                'code': 2,
                'action': 'Emergency protocols; civil protection liaison'
            }
        elif lsi >= self.background_max:
            return {
                'level': 'YELLOW',
                'name': 'Elevated Alert',
                'code': 1,
                'action': 'Enhanced monitoring; stakeholder notification'
            }
        else:
            return {
                'level': 'GREEN',
                'name': 'Background',
                'code': 0,
                'action': 'Routine monitoring'
            }
    
    def update_thresholds(self, background_max: Optional[float] = None,
                          critical_min: Optional[float] = None):
        """Update threshold values"""
        if background_max is not None:
            self.background_max = background_max
        if critical_min is not None:
            self.critical_min = critical_min
