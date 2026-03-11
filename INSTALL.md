# LITHO-SONIC Installation Guide v1.0.0
## Lithospheric Resonance & Infrasonic Geomechanical Observatory

**DOI**: 10.5281/zenodo.18931304  
**Repository**: github.com/gitdeeper8/lithosonic  
**Web**: lithosonic.netlify.app

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+, Debian 11+, macOS 12+
- **RAM**: 8 GB
- **Storage**: 20 GB free space
- **Python**: 3.9 - 3.11

### Recommended Requirements
- **RAM**: 16+ GB
- **Storage**: 50+ GB SSD
- **CPU**: 4+ cores
- **Python**: 3.10

### Sensor Requirements
- LITHO-GEO v2: USB 2.0+ (12 ports for array)
- LITHO-DAS: Ethernet connection
- STS-5A: Ethernet or serial
- Paros 2200A: Serial/USB adapter
- MB2005: Serial/USB adapter
- Titan accelerometers: Ethernet network

---

## 🚀 Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/gitdeeper8/lithosonic.git
cd lithosonic
```

2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

4. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your settings
```

5. Run Initial Setup

```bash
python scripts/init_lithosonic.py
python scripts/test_sensors.py --all
```

---

🐳 Docker Installation

Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

Using Docker (Individual)

```bash
# Build the image
docker build -t lithosonic:latest .

# Run the container
docker run -d \
  --name lithosonic \
  -p 5000:5000 \
  -v $(pwd)/data:/data \
  -v $(pwd)/.env:/app/.env \
  lithosonic:latest
```

---

🔧 Component Installation

Core Physics Engine

```bash
# Install numerical libraries
pip install numpy scipy numba sympy

# Install signal processing
pip install obspy librosa
```

Sensor Drivers

```bash
# Serial communication
pip install pyserial pyusb

# Network sensors
pip install sockets aiohttp

# Install sensor-specific drivers
pip install litho-geo-driver litho-das-driver
```

Web Dashboard

```bash
# Install web dependencies
pip install flask dash plotly gunicorn

# Run development server
python web/app.py
```

Database

```bash
# Install database drivers
pip install psycopg2-binary sqlalchemy

# Initialize TimescaleDB
python scripts/init_db.py
```

---

📊 Sensor-Specific Setup

LITHO-GEO v2 Geophone Array

```bash
# Configure USB permissions
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", MODE="0666"' | sudo tee /etc/udev/rules.d/99-litho.rules
sudo udevadm control --reload-rules

# Test array
python scripts/test_geophones.py --channels 12
```

LITHO-DAS Fiber Optic

```bash
# Mount DAS storage if network-attached
mkdir -p /mnt/das
sudo mount -t nfs 192.168.1.100:/data /mnt/das -o nolock

# Test connection
python scripts/test_das.py --cable-length 4000
```

STS-5A Broadband Seismometer

```bash
# Configure network
sudo ufw allow 5000/tcp

# Test connection
python scripts/test_sts5a.py --ip 192.168.1.100
```

---

🌐 Web Dashboard Deployment

Local Development

```bash
python web/app.py --debug
# Access at http://localhost:5000
```

Production with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 web.app:app
```

Netlify Deployment

```bash
# Build static files
python web/build_static.py

# Deploy with Netlify CLI
npm install -g netlify-cli
netlify deploy --prod --dir=web/build
```

---

🧪 Testing Installation

Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v --cov=lithosonic

# Run specific test modules
pytest tests/test_physics.py -v
pytest tests/test_sensors.py -v
pytest tests/test_inversion.py -v
```

Verify LSI Calculation

```bash
# Compute LSI for sample data
python scripts/compute_lsi.py --sample

# Expected output:
# LSI = 0.84 (ELEVATED)
# Parameters:
#   B_c: 0.72
#   Z_c: 0.68
#   f_n: 0.91
#   α_att: 0.77
#   Ṡ_ae: 0.83
```

System Check

```bash
# Run comprehensive diagnostic
python scripts/diagnose.py --all

# Check sensor connections
python scripts/check_sensors.py --list

# Verify database
python scripts/verify_db.py
```

---

❗ Troubleshooting

Issue Solution
Geophones not detected Check USB: lsusb \| grep FTDI Check permissions: sudo chmod 666 /dev/ttyUSB*
DAS connection failed Verify IP: ping 192.168.1.100 Check NFS: showmount -e 192.168.1.100
Database connection error Verify credentials in .env Check PostgreSQL: sudo systemctl status postgresql
High latency in processing Reduce batch size in config Increase workers: PROCESSING_WORKERS=8
LSI computation slow Enable GPU if available Use cached inversion results

Log Files

```bash
# View application logs
tail -f logs/lithosonic.log

# View sensor logs
tail -f logs/sensors/geo.log
tail -f logs/sensors/das.log

# View error logs
tail -f logs/error.log
```

---

📚 Additional Resources

· Documentation: https://lithosonic.netlify.app/docs
· API Reference: https://lithosonic.netlify.app/api
· Tutorials: https://lithosonic.netlify.app/tutorials
· GitHub Issues: https://github.com/gitdeeper8/lithosonic/issues
· Discussion Forum: https://github.com/gitdeeper8/lithosonic/discussions

---

📄 License

LITHO-SONIC is released under the MIT License.

---

For support: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
DOI: 10.5281/zenodo.18931304 · Web: lithosonic.netlify.app
