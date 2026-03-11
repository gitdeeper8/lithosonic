"""Stage 1: Spectral decomposition (FFT)"""

import numpy as np
from scipy import signal
from typing import Dict, List, Tuple

class SpectralProcessor:
    """FFT-based spectral decomposition"""
    
    def __init__(self, window_size: int = 60, overlap: float = 0.5, sample_rate: int = 1000):
        self.window_size = window_size
        self.overlap = overlap
        self.sample_rate = sample_rate
        self.nperseg = window_size * sample_rate
        self.noverlap = int(self.nperseg * overlap)
    
    def compute_spectra(self, data: np.ndarray) -> Dict:
        """Compute power spectral density"""
        frequencies, psd = signal.welch(
            data,
            fs=self.sample_rate,
            nperseg=self.nperseg,
            noverlap=self.noverlap,
            scaling='density'
        )
        
        # Identify peaks (local maxima)
        peaks = signal.find_peaks(psd, height=np.mean(psd) * 2)[0]
        
        return {
            'frequencies': frequencies.tolist(),
            'psd': psd.tolist(),
            'peaks': frequencies[peaks].tolist() if len(peaks) > 0 else [],
            'peak_heights': psd[peaks].tolist() if len(peaks) > 0 else []
        }
    
    def compute_spectrogram(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute spectrogram"""
        frequencies, times, Sxx = signal.spectrogram(
            data,
            fs=self.sample_rate,
            nperseg=self.nperseg,
            noverlap=self.noverlap
        )
        return frequencies, times, Sxx
    
    def extract_frequency_bands(self, spectra: Dict, bands: List[Tuple[float, float]]) -> Dict:
        """Extract energy in specific frequency bands"""
        freqs = np.array(spectra['frequencies'])
        psd = np.array(spectra['psd'])
        
        band_energy = {}
        for low, high in bands:
            mask = (freqs >= low) & (freqs <= high)
            band_energy[f"{low}-{high}Hz"] = np.sum(psd[mask])
        
        return band_energy
