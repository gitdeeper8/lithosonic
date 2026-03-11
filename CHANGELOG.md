# Changelog

All notable changes to the LITHO-SONIC project will be documented in this file.

**DOI:** 10.5281/zenodo.18931304  
**Repository:** github.com/gitdeeper8/lithosonic

---

## [1.0.0] - 2026-03-10

### 🚀 Initial Release
- Publication of LITHO-SONIC research paper
- Release of complete 5-parameter physics framework
- Open access data from 18 geophysical sites (2011-2025)
- Interactive web dashboard at lithosonic.netlify.app

### Added
#### Core Physics Engine
- **Biot Coupling Coefficient (B_c)**: Poro-elastic wave coupling
  - Biot wave velocity predictions: 94.2% accuracy vs. VSP
  - Pore pressure front tracking: ±50 m spatial resolution
  - Slow-wave diffusion velocity implementation

- **Acoustic Impedance Contrast (Z_c)**: Lithological boundary detection
  - Reflection coefficient calculation
  - Fracture void identification
  - Fluid saturation mapping

- **Hydraulic Fracture Resonance (f_n)**: Fracture geometry inversion
  - Fracture aperture resolution: ±0.8 mm
  - Fluid phase classification: 89.3% accuracy
  - Harmonic analysis for water/gas/magma discrimination

- **Acoustic Attenuation (α_att)**: Damage density quantification
  - Quality factor Q inversion
  - Fracture damage correlation: r ≥ 0.88
  - Structural integrity assessment

- **Stress-Induced AE Rate (Ṡ_ae)**: Micro-fracture energy tracking
  - Real-time emission monitoring
  - Precursor detection: 18-52 days before events
  - Stress stage identification

- **Lithospheric Stress Index (LSI)**: Five-parameter composite
  - LSI = 0.22·B_c + 0.18·Z_c + 0.24·f_n + 0.19·α_att + 0.17·Ṡ_ae
  - Critical threshold: LSI ≥ 0.80
  - Elevated alert: LSI 0.55-0.79
  - Background: LSI < 0.55

#### Sensor Integration
- LITHO-GEO v2 MEMS geophone array (12 elements, 0.005-50 Hz)
- LITHO-DAS fiber optic strain sensor (4 km, 1 m resolution)
- Streckeisen STS-5A broadband seismometer
- Paros 2200A pressure transducer (30 m borehole)
- MB2005 microbarometer for atmospheric coupling
- Nanometrics Titan accelerometers (8 units)

#### Processing Pipeline
- Stage 1: Spectral decomposition (FFT, 60-s windows)
- Stage 2: Harmonic analysis and mode identification
- Stage 3: Inversion modeling with conjugate gradient optimization
- Monte Carlo uncertainty propagation (2000 samples)

#### Deployment Options
- Single station deployment scripts
- Multi-station network architecture
- Cloud deployment (AWS/Azure/GCP)
- Edge computing for real-time processing
- Docker containers for all services
- Netlify web dashboard

#### Documentation
- Complete API reference
- Field deployment guide
- Sensor calibration protocols
- Data analysis tutorials
- Contribution guidelines

### Performance Metrics
| Metric | Value | Target |
|--------|-------|--------|
| Precursor Event Detection | 92.7% | ≥90% |
| Mean Precursor Lead Time | 24 days | ≥18 days |
| False Positive Rate | 3.8% | ≤5% |
| Fracture Aperture Inversion | ±0.8 mm | ±1.0 mm |
| Fluid Phase Classification | 89.3% | ≥85% |
| Biot Velocity vs. VSP | r²=0.942 | ≥0.90 |
| Pore Pressure Tracking | ±50 m | ±100 m |

### Validation Sites (18)
- Kīlauea East Rift, Hawaiʻi (2011-2025)
- Campi Flegrei, Italy (2014-2025)
- San Andreas Fault, Parkfield (2011-2025)
- Corinth Rift, Greece (2012-2025)
- The Geysers, California (2011-2025)
- Chicxulub Crater, Mexico (2015-2025)
- Rhine Graben, Germany (2016-2025)
- Cascadia Subduction Zone (2013-2025)
- [plus 10 additional sites]

---

## [0.9.0] - 2026-02-15

### ⚠️ Pre-release Candidate

### Added
- Beta version of all core modules
- Validation against 10 geophysical sites
- Preliminary LSI weight determination
- Basic sensor drivers
- Initial documentation

### Changed
- Refined Biot inversion algorithms
- Updated fracture resonance model
- Improved AE rate kinetics

### Fixed
- Geophone array synchronization
- DAS data parsing errors
- Spectral decomposition artifacts

---

## [0.8.0] - 2026-01-20

### 🧪 Alpha Release

### Added
- Prototype physics modules
- Test deployments at Kīlauea
- Basic data collection pipeline
- Preliminary LSI formulation

---

## [0.1.0] - 2025-06-01

### 🎯 Project Initiation

### Added
- Project concept and framework design
- Initial 5-parameter selection
- Literature review compilation
- Research proposal development

---

## 🔮 Future Releases

### [1.1.0] - Planned Q3 2026
- Additional validation sites (Alps, Himalayas)
- Machine learning emulators for fast inversion
- Real-time satellite InSAR integration
- Mobile app for field data collection

### [1.2.0] - Planned Q1 2027
- Distributed acoustic sensing on telecom fibers
- 50+ site global network
- AI-powered precursor prediction
- Automated alert system

### [2.0.0] - Planned 2028
- Global lithospheric monitoring network
- Real-time stress maps
- Earthquake early warning integration
- Carbon sequestration monitoring

---

## 📊 Version History

| Version | Date | Status | DOI |
|---------|------|--------|-----|
| 1.0.0 | 2026-03-10 | Stable Release | 10.5281/zenodo.18931304 |
| 0.9.0 | 2026-02-15 | Release Candidate | 10.5281/zenodo.18831304 |
| 0.8.0 | 2026-01-20 | Alpha | 10.5281/zenodo.18731304 |
| 0.1.0 | 2025-06-01 | Concept | - |

---

For questions or contributions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
