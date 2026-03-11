import pytest
import numpy as np
from pipeline.spectral import SpectralProcessor

class TestPipeline:
    def test_spectral_processor(self):
        processor = SpectralProcessor(window_size=10, sample_rate=100)
        data = np.random.randn(1000)
        spectra = processor.compute_spectra(data)
        assert 'frequencies' in spectra
        assert 'psd' in spectra
