# Appendix D: Data Availability

## Zenodo Archive

All LITHO-SONIC data, code, and supplementary materials are openly available:

**DOI**: [10.5281/zenodo.18931304](https://doi.org/10.5281/zenodo.18931304)

## Repository Contents

| Directory | Contents |
|-----------|----------|
| `data/raw/` | Raw geophone time series (MiniSEED format) |
| `data/processed/` | Processed PSD files (HDF5 format) |
| `data/inversion/` | Biot inversion results (NetCDF4 format) |
| `data/events/` | AE event catalogue (CSV format) |
| `notebooks/` | Jupyter notebooks reproducing all manuscript figures |
| `litho_physics/` | Source code with full API documentation |
| `tests/` | Unit and integration tests |
| `docs/` | Documentation |

## Validation Sites (18)

All 18 validation sites' data are available, including:
- Kīlauea East Rift, Hawaiʻi (2011-2025)
- Campi Flegrei, Italy (2014-2025)
- San Andreas Fault, Parkfield (2011-2025)
- The Geysers, California (2011-2025)
- Chicxulub Crater, Mexico (2015-2025)
- [and 13 additional sites]

## Data Formats

| Format | Description |
|--------|-------------|
| MiniSEED | Raw seismic waveform data |
| HDF5 | Hierarchical Data Format for processed data |
| NetCDF4 | Network Common Data Form for inversion results |
| CSV | Comma-separated values for event catalogues |
| JSON | Configuration and metadata |
