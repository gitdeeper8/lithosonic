# 🤝 Contributing to LITHO-SONIC

## Lithospheric Resonance & Infrasonic Geomechanical Observatory

**DOI**: 10.5281/zenodo.18931304  
**Repository**: github.com/gitdeeper8/lithosonic  
**Web**: lithosonic.netlify.app

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contributing to Physics Modules](#contributing-to-physics-modules)
- [Contributing to Sensor Integration](#contributing-to-sensor-integration)
- [Contributing to Documentation](#contributing-to-documentation)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Field Data Contributions](#field-data-contributions)

---

## 📜 Code of Conduct

### Our Pledge
We as members, contributors, and leaders pledge to make participation in the LITHO-SONIC community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at gitdeeper@gmail.com. All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 Getting Started

### Prerequisites
```bash
# Install development dependencies
python --version  # 3.9-3.11 required
git --version     # 2.30+ recommended
docker --version  # 20.10+ for containerized development
```

Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/lithosonic.git
cd lithosonic

# Add upstream remote
git remote add upstream https://github.com/gitdeeper8/lithosonic.git
```

Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial setup
python scripts/init_dev.py
```

Development Tools

```bash
# Code formatting
black lithosonic/ tests/
isort lithosonic/ tests/

# Linting
flake8 lithosonic/ tests/
pylint lithosonic/ tests/

# Type checking
mypy lithosonic/ tests/

# Testing
pytest tests/ -v --cov=lithosonic
```

---

🔄 Development Workflow

Branch Naming Convention

```
feature/     # New features (e.g., feature/biot-inversion)
bugfix/      # Bug fixes (e.g., bugfix/geophone-driver)
docs/        # Documentation (e.g., docs/api-refactor)
sensor/      # Sensor integrations (e.g., sensor/new-geophone)
site/        # New field site data (e.g., site/iceland-2026)
```

Development Process

```bash
# 1. Update your main branch
git checkout main
git pull upstream main

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... code changes ...

# 4. Run tests locally
pytest tests/ -v

# 5. Commit with conventional commit message
git add .
git commit -m "feat: add new Biot inversion algorithm"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create Pull Request on GitHub
```

Commit Message Convention

We follow Conventional Commits:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:

· feat: New feature
· fix: Bug fix
· docs: Documentation only
· style: Code style (formatting)
· refactor: Code change that neither fixes bug nor adds feature
· perf: Performance improvement
· test: Adding missing tests
· chore: Changes to build process or auxiliary tools

Examples:

```
feat(biot): add full Biot equation solver with dispersion
fix(sensors): resolve geophone array sync issue on Raspberry Pi
docs(lsi): update threshold values based on 2025 field data
```

---

🔬 Contributing to Physics Modules

Core Physics Equations

LITHO-SONIC is built on five governing equations:

```python
# lithosonic/physics/biot.py
def compute_biot_coupling(porosity, permeability, fluid_viscosity,
                          bulk_modulus_frame, bulk_modulus_fluid):
    """
    Compute Biot Coupling Coefficient (B_c)
    
    B_c = Q / √(P·R)
    
    Parameters
    ----------
    porosity : float
        Rock porosity (0-1)
    permeability : float
        Permeability (m²)
    fluid_viscosity : float
        Fluid dynamic viscosity (Pa·s)
    bulk_modulus_frame : float
        Dry frame bulk modulus (Pa)
    bulk_modulus_fluid : float
        Fluid bulk modulus (Pa)
    
    Returns
    -------
    float
        Biot coupling coefficient (0-1)
    """
    # Implementation here
    pass
```

Adding New Physics Models

```python
# lithosonic/physics/new_model.py
"""
Template for contributing new physics models
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class NewModelConfig:
    """Configuration for new physics model"""
    parameter1: float
    parameter2: float
    calibration_factor: Optional[float] = 1.0

class NewPhysicsModel:
    """
    New physics model implementation
    
    References
    ----------
    [1] Author et al. (2026) - DOI: 10.xxxx/xxxxx
    """
    
    def __init__(self, config: Dict):
        self.config = NewModelConfig(**config)
        self.validate_against_field_data()
    
    def compute(self, input_data: np.ndarray) -> float:
        """
        Compute model output
        """
        # Implement your model here
        result = self.config.parameter1 * input_data.mean()
        return result * self.config.calibration_factor
    
    def validate_against_field_data(self):
        """Validate model against LITHO-SONIC field dataset"""
        # Load validation data from 18 sites
        # Compare predictions with observations
        # Report validation metrics
        pass
    
    def get_references(self) -> list:
        """Return list of academic references"""
        return [
            "Author, A. et al. (2026). Title. Journal, volume, pages."
        ]
```

---

📡 Contributing to Sensor Integration

Adding New Sensor Support

```python
# lithosonic/sensors/new_sensor.py
"""
Template for adding new sensor support
"""

import serial
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from lithosonic.sensors.base import BaseSensor

class NewGeophoneSensor(BaseSensor):
    """
    Driver for New Geophone Model X
    
    Specifications
    --------------
    - Manufacturer: GeoSpace
    - Frequency range: 0.01-100 Hz
    - Interface: RS232 / USB
    - Baud rate: 115200
    """
    
    def __init__(self, port: str, baudrate: int = 115200, **kwargs):
        super().__init__(port, baudrate, **kwargs)
        self.sensor_type = "geophone"
        self.parameters = ["velocity", "acceleration"]
        self.channel_count = kwargs.get('channels', 3)
    
    def initialize(self) -> bool:
        """Initialize sensor connection"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=2,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            
            # Send wakeup command
            self.serial.write(b"*IDN?\r\n")
            response = self.serial.readline()
            
            if b"GEOPHONE" in response:
                self.logger.info(f"Geophone initialized on {self.port}")
                return True
            else:
                raise ConnectionError(f"Unexpected response: {response}")
                
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
    
    async def read(self) -> Dict[str, Any]:
        """Read sensor data asynchronously"""
        try:
            # Request measurement
            self.serial.write(b"READ\r\n")
            await asyncio.sleep(0.1)
            
            # Read response (binary data)
            data = self.serial.read(24 * self.channel_count)  # 24-bit samples
            
            # Parse based on protocol
            velocities = self._parse_binary(data)
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "sensor_id": self.sensor_id,
                "channels": velocities.tolist(),
                "sample_rate": self.sample_rate,
                "quality_flag": "good"
            }
            
        except Exception as e:
            self.logger.error(f"Read failed: {e}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "sensor_id": self.sensor_id,
                "error": str(e),
                "quality_flag": "error"
            }
    
    def _parse_binary(self, raw_data: bytes) -> np.ndarray:
        """Parse binary data from geophone"""
        # Implementation depends on sensor protocol
        pass
```

Sensor Testing

```python
# tests/sensors/test_new_sensor.py
import pytest
import asyncio
import numpy as np
from lithosonic.sensors.new_sensor import NewGeophoneSensor

@pytest.fixture
def mock_sensor():
    """Create mock sensor for testing"""
    sensor = NewGeophoneSensor(port="/dev/ttyUSB99", channels=3)
    sensor.serial = pytest.Mock()
    return sensor

@pytest.mark.asyncio
async def test_sensor_read(mock_sensor):
    """Test sensor read operation"""
    # Mock serial response (simulated 3-channel data)
    mock_data = np.random.randn(3, 100).astype(np.float32).tobytes()
    mock_sensor.serial.read.return_value = mock_data
    
    # Read data
    data = await mock_sensor.read()
    
    # Verify
    assert "channels" in data
    assert len(data["channels"]) == 3
    assert data["quality_flag"] == "good"

def test_sensor_initialization(mock_sensor):
    """Test sensor initialization"""
    mock_sensor.serial.readline.return_value = b"GEOPHONE v2.0\r\n"
    
    result = mock_sensor.initialize()
    
    assert result == True
    mock_sensor.serial.write.assert_called_with(b"*IDN?\r\n")
```

---

📚 Contributing to Documentation

Documentation Structure

```
docs/
├── api/                    # API documentation
│   ├── physics.md
│   ├── sensors.md
│   └── processing.md
├── tutorials/              # Step-by-step tutorials
│   ├── getting-started.md
│   ├── field-deployment.md
│   └── data-analysis.md
├── explanations/           # Conceptual guides
│   ├── biot-theory.md
│   ├── fracture-resonance.md
│   └── lsi-explained.md
├── references/             # Technical references
│   ├── parameters.md
│   ├── equations.md
│   └── sensors-specs.md
└── contributing/           # Contribution guides
    └── style-guide.md
```

Docstring Style

We use NumPy/Google style docstrings:

```python
def compute_lsi(parameters: Dict[str, float], weights: Optional[Dict] = None) -> float:
    """
    Calculate Lithospheric Stress Index from five parameters.
    
    The LSI is a weighted composite of normalized parameter values,
    ranging from 0 (background) to 1 (critical instability).
    
    Parameters
    ----------
    parameters : Dict[str, float]
        Dictionary containing the five LITHO-SONIC parameters:
        - b_c : Biot coupling coefficient (0-1)
        - z_c : Acoustic impedance contrast (0-1)
        - f_n : Fracture resonance frequency (Hz)
        - alpha_att : Attenuation coefficient (dB/m)
        - s_ae : Acoustic emission rate (events/day)
    
    weights : Optional[Dict]
        Custom weights for each parameter. If None, uses PCA-derived
        weights from the 14-year reference dataset:
        w = {'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24,
             'alpha_att': 0.19, 's_ae': 0.17}
    
    Returns
    -------
    float
        Lithospheric Stress Index (0-1)
    
    Examples
    --------
    >>> params = {
    ...     'b_c': 0.72, 'z_c': 0.68, 'f_n': 0.91,
    ...     'alpha_att': 0.77, 's_ae': 0.83
    ... }
    >>> lsi = compute_lsi(params)
    >>> print(f"{lsi:.2f}")
    0.78
    
    Notes
    -----
    Reference thresholds:
    - LSI ≥ 0.80: CRITICAL - Active instability
    - 0.55 ≤ LSI < 0.80: ELEVATED - Increased monitoring
    - LSI < 0.55: BACKGROUND - Routine monitoring
    
    References
    ----------
    .. [1] Baladi, S. (2026). LITHO-SONIC Research Paper.
           DOI: 10.5281/zenodo.18931304
    """
    pass
```

Building Documentation Locally

```bash
# Install documentation tools
pip install mkdocs mkdocs-material mkdocstrings

# Build docs
mkdocs build

# Serve locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

🧪 Testing Guidelines

Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── physics/
│   │   ├── test_biot.py
│   │   ├── test_fracture.py
│   │   └── test_lsi.py
│   └── sensors/
│       ├── test_geophone.py
│       └── test_das.py
├── integration/            # Integration tests
│   ├── test_processing_pipeline.py
│   └── test_inversion.py
├── field/                  # Field data validation
│   ├── test_kilauea.py
│   └── test_campi_flegrei.py
└── conftest.py             # Shared fixtures
```

Writing Tests

```python
# tests/unit/physics/test_biot.py
import pytest
import numpy as np
from lithosonic.physics.biot import BiotCoupling, BiotParams

class TestBiotCoupling:
    """Test suite for Biot coupling calculations"""
    
    @pytest.mark.parametrize("porosity,permeability,expected_range", [
        (0.20, 1e-13, (0.6, 0.8)),  # Sandstone
        (0.05, 1e-18, (0.1, 0.3)),  # Granite
        (0.30, 1e-12, (0.7, 0.9)),  # Unconsolidated
    ])
    def test_biot_range(self, porosity, permeability, expected_range):
        """Test Biot coupling coefficient range"""
        params = BiotParams(
            porosity=porosity,
            permeability=permeability,
            fluid_viscosity=1e-3,
            bulk_modulus_frame=5e9,
            bulk_modulus_grain=40e9,
            bulk_modulus_fluid=2.2e9
        )
        
        biot = BiotCoupling()
        b_c = biot.compute(params)
        
        assert expected_range[0] <= b_c <= expected_range[1]
    
    def test_critical_frequency(self):
        """Test Biot critical frequency calculation"""
        params = BiotParams(
            porosity=0.20,
            permeability=1e-13,
            fluid_viscosity=1e-3,
            density_fluid=1000,
            tortuosity=2.0,
            bulk_modulus_frame=5e9,
            bulk_modulus_grain=40e9,
            bulk_modulus_fluid=2.2e9
        )
        
        biot = BiotCoupling()
        f_c = biot.critical_frequency(params)
        
        # For 100 mD sandstone, f_c should be ~159 Hz
        assert 100 < f_c < 200
    
    def test_validation_against_field_data(self):
        """Test model validation with field data"""
        # This test would load data from the 18 validation sites
        # and verify that the model meets the 94.2% accuracy claim
        pass
```

Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=lithosonic --cov-report=html

# Run specific test file
pytest tests/unit/physics/test_biot.py -v

# Run tests matching pattern
pytest -k "biot"

# Run with parallel execution
pytest -n auto
```

---

🔀 Pull Request Process

PR Checklist

· Code follows project style guide
· Tests added/updated and passing
· Documentation updated
· CHANGELOG.md updated
· All CI checks passing
· Reviewed by at least one maintainer

PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactor

## Related Issues
Closes #XXX

## Physics Changes
- [ ] Equations modified
- [ ] Constants updated
- [ ] Validation against field data
- [ ] Documentation updated

## Sensor Changes
- [ ] New sensor support
- [ ] Driver modifications
- [ ] Tested with hardware
- [ ] Documentation updated

## Testing Performed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Field data validation
- [ ] Performance benchmarks

## Additional Notes
Any additional information reviewers should know
```

Review Process

1. Automated Checks: CI runs tests, linting, type checking
2. Code Review: At least one maintainer reviews
3. Physics Review: If modifying core equations
4. Documentation Review: For documentation changes
5. Field Validation: For sensor/field-related changes

---

🌋 Field Data Contributions

Contributing New Site Data

If you have field data from a geophysical site that could help validate LITHO-SONIC:

1. Prepare your data in the required format:

```python
# Required columns for CSV export
# timestamp, station_id, b_c, z_c, f_n, alpha_att, s_ae, lsi, event_flag
```

1. Include metadata:

```yaml
site:
  name: "Your Site Name"
  latitude: XX.XXX
  longitude: YY.YYY
  tectonic_environment: "volcanic/fault/rift/craton"
  monitoring_period: "YYYY-YYYY"
  instrumentation: "List of sensors used"
  contact: "Your name/affiliation"
  reference: "DOI or citation if published"
```

1. Submit via pull request to the data/contributions/ directory

Data Format Example

```csv
timestamp,station_id,b_c,z_c,f_n,alpha_att,s_ae,lsi,event_flag
2024-01-01T00:00:00Z,KILAUEA_01,0.45,0.32,2.3,0.21,0.15,0.38,0
2024-01-01T01:00:00Z,KILAUEA_01,0.46,0.33,2.3,0.21,0.16,0.39,0
...
2024-05-03T00:00:00Z,KILAUEA_01,0.78,0.71,4.2,0.68,0.79,0.82,1  # Event precursor
```

---

🌍 Community Guidelines

Communication Channels

· GitHub Issues: Bug reports, feature requests
· GitHub Discussions: Q&A, ideas, community support
· Email: gitdeeper@gmail.com (project lead)
· ORCID: 0009-0003-8903-0029

Recognition

Contributors are recognized in:

· AUTHORS.md
· Release notes
· Academic publications (where applicable)

Research Contributions

If you use LITHO-SONIC in your research:

1. Cite the paper: Baladi, S. (2026). LITHO-SONIC. DOI: 10.5281/zenodo.18931304
2. Share your data/code when possible
3. Submit a case study to our repository

---

📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LITHO-SONIC! 🌍

For questions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
