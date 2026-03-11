
LITHO-SONIC Validation Suite

Sites

· 18 geophysical sites across 4 tectonic environments
· 14-year time series (2011-2025)

Benchmarks

· lsi_accuracy.py - Detection accuracy benchmark
· lead_time_analysis.py - Precursor lead time analysis

Expected Results

· LSI accuracy: 92.7%
· Mean lead time: 24 days
· False positive rate: 3.8%
  EOF

tests/README.md

cat > tests/README.md << 'EOF'

LITHO-SONIC Test Suite

Run tests with:

```bash
pytest tests/ -v
```

Test Categories

· test_biot.py - Biot coupling coefficient
· test_impedance.py - Acoustic impedance
· test_fracture_resonance.py - Fracture resonance
· test_attenuation.py - Attenuation
· test_emission.py - Acoustic emission
· test_lsi.py - LSI computation
· test_pipeline.py - Processing pipeline
  EOF

notebooks/README.md

cat > notebooks/README.md << 'EOF'

LITHO-SONIC Tutorial Notebooks

1. 01_biot_theory_primer.ipynb - Introduction to Biot theory
2. 02_five_parameters_tutorial.ipynb - The five governing parameters
3. 03_lsi_computation.ipynb - Computing the Lithospheric Stress Index
4. 04_kilauea_case_study.ipynb - Kīlauea 2018 eruption case study
5. 05_campi_flegrei_case_study.ipynb - Campi Flegrei unrest case study
6. 06_geysers_case_study.ipynb - The Geysers induced seismicity case study
7. 07_statistical_framework.ipynb - Statistical analysis framework

Run with:

```bash
jupyter notebook notebooks/
```

