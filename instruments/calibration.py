"""Sensor calibration utilities"""

import json
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

class CalibrationManager:
    """Manages sensor calibration data"""
    
    def __init__(self, calibration_file: Optional[str] = None):
        self.calibration_data = {}
        if calibration_file:
            self.load_calibration(calibration_file)
    
    def load_calibration(self, filepath: str):
        """Load calibration data from JSON file"""
        with open(filepath, 'r') as f:
            self.calibration_data = json.load(f)
    
    def save_calibration(self, filepath: str):
        """Save calibration data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.calibration_data, f, indent=2)
    
    def apply_calibration(self, sensor_type: str, raw_data: np.ndarray) -> np.ndarray:
        """Apply calibration to raw sensor data"""
        if sensor_type not in self.calibration_data:
            return raw_data
        
        cal = self.calibration_data[sensor_type]
        
        # Apply gain and offset
        gain = cal.get('gain', 1.0)
        offset = cal.get('offset', 0.0)
        
        return raw_data * gain + offset
    
    def get_response_function(self, sensor_type: str) -> Dict:
        """Get frequency response function"""
        if sensor_type not in self.calibration_data:
            return {}
        
        return self.calibration_data[sensor_type].get('response', {})
    
    def update_calibration(self, sensor_type: str, gain: float, offset: float, 
                          date: Optional[str] = None):
        """Update calibration for a sensor"""
        if sensor_type not in self.calibration_data:
            self.calibration_data[sensor_type] = {}
        
        self.calibration_data[sensor_type]['gain'] = gain
        self.calibration_data[sensor_type]['offset'] = offset
        self.calibration_data[sensor_type]['last_calibration'] = date or datetime.utcnow().isoformat()
