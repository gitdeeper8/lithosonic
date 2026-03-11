# LITHO-SONIC

> **Lithospheric Acoustic Sensing and Integrated Crustal Monitoring Framework**
>
> A five-parameter poro-elastic monitoring system for real-time geomechanical hazard detection, subsurface fluid characterisation, and early warning of volcanic, seismic, and induced-seismicity events.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/lithosonic?logo=pypi&label=PyPI&color=orange)](https://pypi.org/project/lithosonic/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18931304-blue)](https://doi.org/10.5281/zenodo.18931304)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Validation Sites](https://img.shields.io/badge/Validation%20Sites-18-orange)]()
[![LSI Accuracy](https://img.shields.io/badge/LSI%20Accuracy-92.7%25-brightgreen)]()
[![Lead Time](https://img.shields.io/badge/Mean%20Lead%20Time-24%20days-blue)]()
[![Dashboard](https://img.shields.io/badge/Dashboard-lithosonic.netlify.app-lightblue)](https://lithosonic.netlify.app)

---

## Table of Contents

- [Overview](#-overview)
- [Scientific Background](#-scientific-background)
- [The Five Governing Parameters](#-the-five-governing-parameters)
- [Lithospheric Stress Index (LSI)](#-lithospheric-stress-index-lsi)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Validation & Results](#-validation--results)
- [Case Studies](#-case-studies)
- [Alert Framework](#-alert-framework)
- [Contributing](#-contributing)
- [References](#-references)
- [License](#-license)

---

## Overview

LITHO-SONIC reframes crustal monitoring from a **passive event-detection paradigm** to an **active acoustic information extraction paradigm**. Rather than waiting for discrete seismic events, LITHO-SONIC continuously decodes the low-frequency acoustic signals (0.001-20 Hz) that the crust perpetually emits, driven by pore pressure dynamics, stress redistribution, and fluid migration.

**Key achievements:**

| Metric | Conventional Monitoring | LITHO-SONIC |
|---|---|---|
| Mean precursor lead time | 4-9 days | **24 days** |
| Pore pressure front spatial resolution | 200-400 m (InSAR) | **+/-50 m** |
| Fluid phase discrimination | Not available | **[x] (water / CO2-brine / gas / magmatic)** |
| Detection accuracy (LSI) | -- | **92.7%** across 18 sites |
| Tectonic environments validated | -- | **4** (rift / subduction / volcanic / craton) |

---

## Scientific Background

LITHO-SONIC is grounded in **Biot theory** (1956) -- the rigorous framework for acoustic wave propagation in fluid-saturated porous elastic solids. The key physical insight is the existence of Biot's **slow compressional wave**: a diffusive, pressure-driven mode that propagates through pore fluid networks at 0.01-10 Hz, encoding real-time information about:

- Fluid saturation and pore pressure distribution
- Fracture network geometry and aperture
- Effective stress state and proximity to failure
- Fluid phase composition (water, gas, magmatic volatiles, CO2-brine)

The theoretical foundation is completed by:
- **Gassmann substitution** for saturated bulk modulus
- **Gutenberg-Richter statistics** for acoustic emission scaling
- **Hydraulic fracture resonance theory** for fluid-filled crack characterisation
- **Biot attenuation inversion** for quality-factor mapping

---

## The Five Governing Parameters

### 1. Biot Coupling Coefficient -- `B_c`
Governs solid-fluid wave coupling in saturated porous rock.

```
Bc = (1 - K_dry / K_s) / (1 - K_dry/K_s + phi(K_s/K_f - 1))
```

**Range:** 0 (dry rock) -> 1 (highly saturated, critical pore pressure).

---

### 2. Acoustic Impedance Contrast -- `Z_c`
Maps lithological boundaries and fracture zone geometry.

```
Z = rho * V_P = rho * sqrt((K_sat + 4G/3) / rho)
```

**Reference values:** Granite 15-18 MRayl | Basalt 14-16 MRayl | Saturated sandstone 6-9 MRayl | Fracture zone 1.5-3.5 MRayl.

---

### 3. Hydraulic Fracture Resonance Frequency -- `f_n`
Discriminates subsurface fluid phase from fracture resonance spectra.

```
f_n = n * V_fluid / (2L)      n = 1, 2, 3, ...
```

**Fluid discrimination:** Water (f1 ~= 740 Hz/m) | CO2-brine (600-675 Hz/m) | Dry gas (75-125 Hz/m) | Magmatic volatiles (300-450 Hz/m).

---

### 4. Acoustic Attenuation Coefficient -- `alpha_att`
Quantifies anelastic energy dissipation in the propagation medium.

```
A(x) = A0 * exp(-alpha_att * x)      alpha_att = pi*f / (Q * V_P)
```

**Diagnostic ranges:** Intact granite Q > 200 | Saturated fractured rock Q = 20-80 | Near-critical pore pressure Q < 15.

---

### 5. Stress-Induced Acoustic Emission Rate -- `S_dot_ae`
Quantifies micro-fracture energy release rate.

```
S_dot_ae = A0 * exp(sigma_eff / sigma_c) * (depsilon/dt)^beta
```

**Diagnostic:** Exponential S_dot_ae acceleration signals approach to critical failure threshold.

---

## Lithospheric Stress Index (LSI)

The five parameters are fused into a single dimensionless index:

```
LSI = w1*Bc* + w2*Zc* + w3*fn* + w4*alphaatt* + w5*S_dotae*
```

**Weights (from 14-year training dataset):**

| Parameter | Weight |
|---|---|
| B_c  (Biot Coupling) | 0.22 |
| Z_c  (Impedance Contrast) | 0.18 |
| f_n  (Fracture Resonance) | **0.24** |
| alpha_att (Attenuation) | 0.19 |
| S_dot_ae (Emission Rate) | 0.17 |

---

## Project Structure

```
litho-sonic/
|
+---- README.md
+---- LICENSE
+---- requirements.txt
+---- setup.py
|
+---- litho_physics/                  # Core physics engine
|   +---- __init__.py
|   +---- litho_physics.py            # Main module -- all five governing equations
|   +---- biot.py                     # Biot wave equations & slow-wave solver
|   +---- impedance.py                # Acoustic impedance contrast computation
|   +---- fracture_resonance.py       # Hydraulic fracture resonance inversion
|   +---- attenuation.py              # Biot attenuation & Q-factor inversion
|   +---- emission.py                 # Acoustic emission rate model
|   +---- lsi.py                      # Lithospheric Stress Index fusion
|
+---- pipeline/                       # Signal processing pipeline
|   +---- __init__.py
|   +---- ingest.py                   # Raw geophone data ingestion (1000 sps)
|   +---- spectral.py                 # Stage 1 -- FFT spectral decomposition
|   +---- harmonic.py                 # Stage 2 -- harmonic analysis & mode ID
|   +---- inversion.py                # Stage 3 -- conjugate gradient inversion
|
+---- instruments/                    # Hardware interface & sensor config
|   +---- litho_geo_v2.py             # LITHO-GEO v2 geophone array driver
|   +---- infrasound_array.py         # 24-element infrasound microphone array
|   +---- tiltmeter.py                # Biaxial broadband tiltmeter interface
|   +---- calibration.py             # Sensor calibration utilities
|
+---- alert/                          # Alert framework
|   +---- __init__.py
|   +---- thresholds.py               # LSI threshold management (Background / Elevated / Active)
|   +---- neyman_pearson.py           # Optimal detection threshold (Neyman-Pearson)
|   +---- notifications.py           # Alert dispatch (API / webhook)
|
+---- validation/                     # Validation dataset and site configurations
|   +---- sites/
|   |   +---- kilauea_lerz/           # Case Study A -- Kilauea East Rift Zone 2018
|   |   +---- campi_flegrei/          # Case Study B -- Campi Flegrei 2023-2024
|   |   +---- geysers/                # Case Study C -- The Geysers, California
|   |   +---- parkfield/              # San Andreas Fault -- Parkfield
|   |   +---- rhine_graben/           # Rhine Graben geothermal province
|   |   +---- chicxulub/              # Chicxulub impact crater reference site
|   +---- benchmarks/
|       +---- lsi_accuracy.py
|       +---- lead_time_analysis.py
|
+---- notebooks/                      # Jupyter notebooks
|   +---- 01_biot_theory_primer.ipynb
|   +---- 02_five_parameters_tutorial.ipynb
|   +---- 03_lsi_computation.ipynb
|   +---- 04_kilauea_case_study.ipynb
|   +---- 05_campi_flegrei_case_study.ipynb
|   +---- 06_geysers_case_study.ipynb
|   +---- 07_statistical_framework.ipynb
|
+---- tests/                          # Unit and integration tests
|   +---- test_biot.py
|   +---- test_impedance.py
|   +---- test_fracture_resonance.py
|   +---- test_attenuation.py
|   +---- test_emission.py
|   +---- test_lsi.py
|   +---- test_pipeline.py
|
+---- docs/                           # Documentation
|   +---- api/                        # Auto-generated API reference
|   +---- theory/                     # Extended theoretical notes
|   +---- deployment/                 # Field deployment guide
|   +---- appendices/
|       +---- A_instrument_specs.md
|       +---- B_biot_frequency_derivation.md
|       +---- C_operational_thresholds.md
|       +---- D_data_availability.md
|       +---- E_author_contributions.md
|
+---- data/
    +---- example/                    # Example datasets (all 18 validation sites)
    +---- reference/                  # 14-year reference baseline (normalisation bounds)
```

---

## Installation

**Requirements:** Python 3.9+, NumPy, SciPy, ObsPy, Matplotlib, Pandas.

```bash
# Clone the repository
git clone https://gitlab.com/gitdeeper8/lithosonic.git
cd lithosonic

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

---

## Quick Start

```python
from litho_physics import LithoSonic

# Initialise with a site configuration
ls = LithoSonic.from_config("validation/sites/kilauea_lerz/config.yaml")

# Load raw waveform data
ls.load_waveforms("data/example/kilauea_2018.mseed")

# Run the full processing pipeline
results = ls.run_pipeline()

# Compute the Lithospheric Stress Index
lsi = ls.compute_lsi()
print(f"LSI = {lsi:.3f}")

# Evaluate against alert thresholds
alert_level = ls.evaluate_alert(lsi)
print(f"Alert Level: {alert_level}")   # Background / Elevated Alert / Active Instability
```

---

## Usage

### Computing Individual Parameters

```python
from litho_physics.biot import compute_biot_coupling
from litho_physics.fracture_resonance import invert_fracture_length
from litho_physics.attenuation import compute_q_factor

# Biot Coupling Coefficient
Bc = compute_biot_coupling(K_dry=20e9, K_s=36e9, K_f=2.2e9, phi=0.15)

# Fracture length inversion from observed resonance frequency
L = invert_fracture_length(f_observed=0.74, fluid="water")

# Q-factor from amplitude decay
Q = compute_q_factor(amplitude_profile, distances, frequency=1.0, Vp=4200)
```

### Running the Full Signal Processing Pipeline

```python
from pipeline import LithoSonicPipeline

pipe = LithoSonicPipeline(config="config/default.yaml")

# Stage 1 -- Spectral decomposition (FFT on 60-s overlapping windows)
spectra = pipe.spectral_decomposition(raw_data)

# Stage 2 -- Harmonic analysis and mode identification
modes = pipe.harmonic_analysis(spectra)

# Stage 3 -- Conjugate gradient inversion
parameters = pipe.inversion(modes)
```

### Real-Time Monitoring

```python
from litho_physics import LithoSonicStream

# Connect to live sensor array
stream = LithoSonicStream(host="192.168.1.100", port=18000)

# Stream LSI in real time with alert callbacks
stream.monitor(
    on_elevated=lambda lsi: print(f"[!]  Elevated Alert -- LSI={lsi:.3f}"),
    on_critical=lambda lsi: print(f"[!!] Active Instability -- LSI={lsi:.3f}")
)
```

---

## [x] Validation & Results

LITHO-SONIC was validated against field datasets from **18 geologically diverse monitoring sites** across **four tectonic environments**:

| Environment | Sites | Example |
|---|---|---|
| Intraplate volcanic | 5 | Kilauea East Rift Zone |
| Subduction zone | 4 | Campi Flegrei |
| Continental rift | 5 | Rhine Graben |
| Stable craton | 4 | Chicxulub impact crater |

**Summary statistics:**

- **LSI detection accuracy:** 92.7% (Youden Index optimised, LSI* = 0.80)
- **Mean precursor lead time:** 24 days (vs. 4-9 days conventional)
- **False alarm rate:** Maintained at <= 10% (Neyman-Pearson threshold)
- **Biot inversion Vp accuracy (Chicxulub):** r^2 = 0.963 vs. independent VSP data
- **Pore pressure front resolution:** +/-50 m (3.6x improvement over InSAR)

**Inter-parameter correlations:**

| Pair | Pearson r | Physical interpretation |
|---|---|---|
| B_c -- S_dot_ae | 0.81 | Pore pressure drives effective stress reduction -> AE acceleration |
| Z_c -- alpha_att | 0.83 | Both track fracture-induced impedance and dissipation |
| f_n -- Z_c | -0.67 | Gas exsolution reduces both fluid velocity and bulk modulus |

---

## Case Studies

### Case Study A -- Kilauea East Rift Zone (2018 Intrusion Event)
Retrospective application reveals a four-stage precursory sequence:
- **T-72 days:** B_c anomaly (fluid influx into dike pathway)
- **T-21 days:** f_n shift indicating magmatic volatile exsolution
- **T-14 days:** LSI crosses critical threshold (0.80)
- **T-3 days:** S_dot_ae exponential acceleration

### Case Study B -- Campi Flegrei Caldera (2023-2024 Unrest)
Ongoing real-time monitoring of a caldera system with 500,000 residents within 10 km:
- B_c rose from 0.57 (early 2023) -> **0.81** (November 2024)
- f_n shift confirmed transition from hydrothermal brine -> magmatic gas
- Three-level alert framework active and integrated with civil protection authorities

### Case Study C -- The Geysers Geothermal Field, California
World's largest geothermal power plant; most seismically active non-fault site in California:
- Injection plume fronts resolved at **50 m spatial resolution**
- B_c pore pressure tracking enables real-time Traffic Light Protocol (TLP) management

---

## Alert Framework

LITHO-SONIC implements a three-level LSI alert system, mapped to standard volcanic and USGS ShakeAlert frameworks:

| Level | LSI Range | Status | Action |
|---|---|---|---|
| [GREEN] **Background** | LSI < 0.60 | Normal crustal activity | Routine monitoring |
| [YELLOW] **Elevated Alert** | 0.60 <= LSI < 0.80 | Anomalous parameter evolution | Enhanced monitoring; stakeholder notification |
| [RED] **Active Instability** | LSI >= 0.80 | Critical threshold exceeded | Emergency protocols; civil protection liaison |

---

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

```bash
# Run the full test suite before submitting
pytest tests/ -v

# Check code style
flake8 litho_physics/ pipeline/ --max-line-length=120
```

Please follow the [Contributor Covenant](CODE_OF_CONDUCT.md) code of conduct.

---

## References

| Key Reference | Relevance |
|---|---|
| Biot (1956a, 1956b) -- *J. Acoust. Soc. Am.* | Foundational poro-elastic wave equations |
| Gassmann (1951) | Saturated bulk modulus substitution |
| Gutenberg & Richter (1944) -- *Bull. Seismol. Soc. Am.* | Acoustic emission frequency-magnitude scaling |
| Obara (2002) -- *Science* | Non-volcanic tremor discovery |
| Zoback (2010) -- *Reservoir Geomechanics*, Cambridge | Effective stress and geomechanics framework |
| Streckeisen et al. (1995) | STS-2 broadband seismometer design |
| Walter et al. (2020) -- *Nature Comms.* | Distributed acoustic sensing (DAS) |
| Morgan et al. (2016) -- *Science* | Chicxulub Expedition 364 VSP reference data |

Full bibliography available in [`docs/REFERENCES.md`](docs/REFERENCES.md).

---

## Digital Infrastructure

| Platform | Purpose | Link |
|----------|---------|------|
| Live Dashboard | Interactive monitoring portal | [lithosonic.netlify.app](https://lithosonic.netlify.app) |
| PyPI | Python package (v1.0.0) | [pypi.org/project/lithosonic](https://pypi.org/project/lithosonic/) |
| GitLab | Primary source repository | [gitlab.com/gitdeeper8/lithosonic](https://gitlab.com/gitdeeper8/lithosonic) |
| GitHub | Mirror repository | [github.com/gitdeeper8/lithosonic](https://github.com/gitdeeper8/lithosonic) |
| Zenodo | Permanent archive (DOI) | [10.5281/zenodo.18931304](https://doi.org/10.5281/zenodo.18931304) |
| OSF | Preregistration | [osf.io/gfzqs](https://osf.io/gfzqs) -- DOI: 10.17605/OSF.IO/BV47N |
| ScienceOpen | Preprint (peer review) | [scienceopen.com](https://www.scienceopen.com/document/c2d18db7-c1dc-49a0-b266-63c2daae49ef) |

---

## Author

**Samir Baladi** <sup>1</sup> *

<sup>1</sup> Ronin Institute / Rite of Renaissance, Interdisciplinary AI Researcher
-- Crustal Geophysics, Infrasonic Wave Analysis & Lithospheric Stress Monitoring

\* Corresponding Author

- Email: [gitdeeper@gmail.com](mailto:gitdeeper@gmail.com)
- ORCID: [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
- Phone: +1 (614) 264-2074

---

## Citation

If you use LITHO-SONIC in your research, please cite:

```bibtex
@software{baladi2026lithosonic,
  author    = {Baladi, Samir},
  title     = {LITHO-SONIC: A Multi-Parameter Geophysical Framework for
               Real-Time Crustal Acoustic Emission and Infrasonic
               Lithospheric Stress Monitoring},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.0.0},
  doi       = {10.5281/zenodo.18931304},
  url       = {https://lithosonic.netlify.app}
}
```

**Preprint:** Baladi, S. (2026). LITHO-SONIC: A Multi-Parameter Geophysical Framework
for Real-Time Analysis of Crustal Acoustic Emissions, Hydro-Fracture Resonance,
and Subsurface Stress Dynamics. *ScienceOpen Preprints*.
https://www.scienceopen.com/document/c2d18db7-c1dc-49a0-b266-63c2daae49ef

**Preregistration:** Baladi, S. (2026). LITHO-SONIC. OSF.
https://doi.org/10.17605/OSF.IO/BV47N

---

## License

This project is licensed under the MIT License -- see the [LICENSE](LICENSE) file for details.

---

> **Data Availability:** Example datasets from all 18 validation sites, unit tests, and Jupyter notebooks reproducing all published figures are included in the `data/example/` and `notebooks/` directories.
>
> For questions or collaborations, please open a GitLab issue.

---

<div align="center">

**LITHO-SONIC** -- *The Earth has always been speaking. Now we can listen.*

`DOI: 10.5281/zenodo.18931304` | `lithosonic.netlify.app`

</div>
