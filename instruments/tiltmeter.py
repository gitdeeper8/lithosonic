"""Biaxial Broadband Tiltmeter Driver"""

import numpy as np

class Tiltmeter:
    """Biaxial broadband tiltmeter"""
    
    def __init__(self, port: str = "/dev/ttyUSB0", sample_rate: int = 20):
        self.port = port
        self.sample_rate = sample_rate
    
    async def read(self) -> np.ndarray:
        """Read tilt data (x and y components)"""
        duration = 1.0
        samples = int(duration * self.sample_rate)
        return np.random.randn(2, samples) * 1e-6  # microradians
