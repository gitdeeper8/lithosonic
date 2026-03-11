# LITHO-SONIC Instrument Drivers

## Supported Sensors

- **LITHO-GEO v2**: 12-element MEMS geophone array
- **Infrasound Array**: 24-element microphone array (0.01-20 Hz)
- **Tiltmeter**: Biaxial broadband tiltmeter
- **Calibration**: Sensor calibration utilities

## Usage

```python
from instruments.litho_geo_v2 import GeophoneArray

geo = GeophoneArray()
data = await geo.read()
```

