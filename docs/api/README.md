# LITHO-SONIC API Reference

## Core Modules

- `litho_physics.biot` - Biot coupling coefficient and wave equations
- `litho_physics.impedance` - Acoustic impedance contrast
- `litho_physics.fracture_resonance` - Hydraulic fracture resonance
- `litho_physics.attenuation` - Acoustic attenuation and Q factor
- `litho_physics.emission` - Acoustic emission rate
- `litho_physics.lsi` - Lithospheric Stress Index

## Pipeline Modules

- `pipeline.ingest` - Data ingestion
- `pipeline.spectral` - Spectral decomposition
- `pipeline.harmonic` - Harmonic analysis
- `pipeline.inversion` - Parameter inversion

## Instrument Drivers

- `instruments.litho_geo_v2` - LITHO-GEO v2 geophone array
- `instruments.infrasound_array` - Infrasound microphone array
- `instruments.tiltmeter` - Tiltmeter
- `instruments.calibration` - Calibration utilities

## Alert Framework

- `alert.thresholds` - Alert threshold management
- `alert.neyman_pearson` - Neyman-Pearson detector
- `alert.notifications` - Alert dispatch
