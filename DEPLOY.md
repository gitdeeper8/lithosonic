# 🌍 LITHO-SONIC Deployment Guide v1.0.0
## Lithospheric Resonance & Infrasonic Geomechanical Observatory

**DOI**: 10.5281/zenodo.18931304  
**Repository**: github.com/gitdeeper8/lithosonic  
**Web**: lithosonic.netlify.app

---

## 📋 Deployment Overview

This guide covers deployment options for LITHO-SONIC monitoring stations and data processing pipelines across different environments.

### Deployment Architectures

| Architecture | Use Case | Resources | Scalability |
|-------------|----------|-----------|-------------|
| **Single Station** | Remote geophysical monitoring | 1 server | Limited |
| **Multi-Station Network** | Regional monitoring (volcanic/fault) | 3-10 servers | Moderate |
| **Cloud-Based** | Global monitoring network | Auto-scaling | High |
| **Edge Computing** | Real-time alerts at field sites | IoT devices | Distributed |

---

## 🏗️ Architecture Components

```

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Sensor Array   │────▶│  Edge Gateway   │────▶│  Local Storage  │
│  (12 geophones) │     │  (Raspberry Pi) │     │  (SSD/RAID)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│                          │
▼                          ▼
┌─────────────────┐     ┌─────────────────┐
│  Real-time      │     │  Daily Batch    │
│  Processing     │     │  Processing     │
└─────────────────┘     └─────────────────┘
│                          │
└──────────────┬───────────┘
▼
┌─────────────────┐
│  Cloud Sync     │
│  (Optional)     │
└─────────────────┘
│
┌─────────┴─────────┐
▼                   ▼
┌─────────────────┐ ┌─────────────────┐
│  Web Dashboard  │ │  Data Archive   │
│  (Netlify)      │ │  (Zenodo)       │
└─────────────────┘ └─────────────────┘

```

---

## 🔧 Local Deployment (Single Station)

### 1. Hardware Requirements
```yaml
Minimum Specifications:
  CPU: Intel NUC i5 / Raspberry Pi 4 (8GB)
  RAM: 8GB
  Storage: 1TB SSD (for raw data)
  Network: 4G/LTE modem (for remote sites)
  Power: Solar + Battery backup (200W panel, 200Ah battery)
  Enclosure: IP67 weatherproof case
  Sensors: LITHO-GEO v2 (12 elements), LITHO-DAS, STS-5A, Paros, MB2005
```

2. Installation Steps

```bash
# 1. Prepare the system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip docker.io docker-compose

# 2. Clone repository
git clone https://github.com/gitdeeper8/lithosonic.git
cd lithosonic

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your station details

# 4. Install dependencies
pip install -r requirements.txt
pip install -e .

# 5. Test sensors
python scripts/test_sensors.py --all

# 6. Start services
docker-compose -f docker-compose.dev.yml up -d

# 7. Verify deployment
curl http://localhost:5000/health
```

3. Station Configuration Example

```yaml
# config/station_kilauea.yaml
station:
  id: "KILAUEA_ERZ_01"
  name: "Kīlauea East Rift Zone"
  latitude: 19.41
  longitude: -155.28
  elevation: 1100
  environment: "intraplate_volcanic"
  deployment_date: "2026-03-10"

sensors:
  geophone_array:
    enabled: true
    base_port: "/dev/ttyUSB"
    channels: 12
    sample_rate: 1000
    spacing: 50  # meters
    pattern: "cross"
  
  das:
    enabled: true
    cable_length: 4000  # meters
    spatial_resolution: 1  # meter
    sample_rate: 500
  
  sts5a:
    enabled: true
    ip: "192.168.1.100"
    port: 5000
    sample_rate: 200
  
  paros:
    enabled: true
    port: "/dev/ttyUSB12"
    interval: 60  # seconds
    borehole_depth: 30  # meters
  
  mb2005:
    enabled: true
    port: "/dev/ttyUSB13"
    sample_rate: 100
  
  titan:
    enabled: true
    count: 8
    base_ip: "192.168.1.200"
    sample_rate: 500
    spacing: 500  # meters

processing:
  interval: 300  # seconds
  batch_size: 1000
  workers: 4
  lsi_update: 3600  # seconds

storage:
  data_dir: "/data/lithosonic"
  retention_days: 365
  backup_interval: 86400  # seconds

network:
  sync_interval: 3600  # seconds
  cloud_endpoint: "https://api.lithosonic.netlify.app"
  use_4g: true

power:
  source: "solar"
  panel_wattage: 200
  battery_ah: 200
  low_power_mode: true
```

---

🌐 Multi-Station Network Deployment

Network Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Station 1  │────▶│  Station 2  │────▶│  Station 3  │
│ Kīlauea     │     │ Mauna Loa   │     │ Hualālai    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ▼
                    ┌─────────────┐
                    │   Cloud     │
                    │   Hub       │
                    └─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  TimescaleDB│    │  Dashboard  │    │  Alert      │
│  Cluster    │    │  Servers    │    │  System     │
└─────────────┘    └─────────────┘    └─────────────┘
```

Central Hub Configuration

```yaml
# config/hub_config.yaml
hub:
  id: "LITHOSONIC_HUB_01"
  region: "hawaii"
  endpoints:
    api: "https://api.lithosonic.netlify.app"
    websocket: "wss://ws.lithosonic.netlify.app"
    mqtt: "mqtt.lithosonic.netlify.app:8883"

database:
  type: "timescaledb"
  host: "timescaledb.lithosonic.net"
  port: 5432
  name: "lithosonic"
  user: "lithouser"
  pool_size: 100
  retention_period: "10 years"
  
  replication:
    enabled: true
    replicas: 2

cache:
  type: "redis"
  host: "redis.lithosonic.net"
  port: 6379
  max_memory: "8gb"

message_queue:
  type: "rabbitmq"
  cluster: 
    - host: "rabbit1.lithosonic.net"
    - host: "rabbit2.lithosonic.net"

stations:
  - id: "KILAUEA_ERZ_01"
    sync_interval: 300
    priority: 1
  - id: "MAUNA_LOA_01"
    sync_interval: 600
    priority: 2
  - id: "HUALALAI_01"
    sync_interval: 900
    priority: 3

alerts:
  lsi_critical: 0.80
  lsi_elevated: 0.55
  check_interval: 300
  channels:
    - type: "email"
      recipients: ["monitor@lithosonic.org"]
    - type: "slack"
      webhook: "https://hooks.slack.com/services/xxx"
    - type: "sms"
      enabled: false
```

---

☁️ Cloud Deployment

AWS Deployment (Terraform)

```hcl
# main.tf - AWS Infrastructure
provider "aws" {
  region = "us-west-2"  # Oregon (good for geophysical data)
}

# VPC
resource "aws_vpc" "lithosonic" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  
  tags = {
    Name = "lithosonic-vpc"
    Project = "LITHO-SONIC"
  }
}

# RDS for TimescaleDB
resource "aws_db_instance" "timescaledb" {
  identifier = "lithosonic-timescaledb"
  engine = "postgres"
  engine_version = "15.3"
  instance_class = "db.r5.2xlarge"
  allocated_storage = 1000
  storage_encrypted = true
  
  db_name = "lithosonic"
  username = "lithoadmin"
  password = random_password.db_password.result
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
  
  backup_retention_period = 30
  backup_window = "03:00-04:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql"]
}

# ECS Fargate for Processing
resource "aws_ecs_cluster" "lithosonic" {
  name = "lithosonic-cluster"
  
  setting {
    name = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "processor" {
  family = "lithosonic-processor"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = "4096"
  memory = "16384"
  execution_role_arn = aws_iam_role.ecs_execution.arn
  
  container_definitions = jsonencode([
    {
      name = "processor"
      image = "${aws_ecr_repository.lithosonic.repository_url}:latest"
      essential = true
      
      environment = [
        { name = "DB_HOST", value = aws_db_instance.timescaledb.address },
        { name = "DB_NAME", value = "lithosonic" }
      ]
      
      secrets = [
        { name = "DB_PASSWORD", valueFrom = aws_secretsmanager_secret.db_password.arn }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group" = "/ecs/lithosonic-processor"
          "awslogs-region" = "us-west-2"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

# S3 for Raw Data Archive
resource "aws_s3_bucket" "lithosonic_data" {
  bucket = "lithosonic-raw-data-${random_id.bucket_suffix.hex}"
  
  lifecycle_rule {
    id = "archive_old_data"
    enabled = true
    
    transition {
      days = 90
      storage_class = "GLACIER"
    }
    
    expiration {
      days = 3650  # 10 years
    }
  }
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "lsi_critical" {
  alarm_name = "lithosonic-lsi-critical"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods = 2
  metric_name = "LSI"
  namespace = "LITHO-SONIC"
  period = 3600
  statistic = "Maximum"
  threshold = 0.80
  alarm_description = "LSI critical threshold exceeded"
  alarm_actions = [aws_sns_topic.alerts.arn]
  
  dimensions = {
    StationID = "KILAUEA_ERZ_01"
  }
}
```

Deploy with Terraform

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan deployment
terraform plan -var-file=environments/production.tfvars

# Apply deployment
terraform apply -var-file=environments/production.tfvars -auto-approve
```

GCP Deployment

```bash
# Create GKE cluster
gcloud container clusters create lithosonic-cluster \
  --num-nodes=3 \
  --machine-type=e2-standard-8 \
  --zone=us-west1-a \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=10

# Deploy with Helm
helm repo add lithosonic https://lithosonic.netlify.app/charts
helm install lithosonic lithosonic/lithosonic \
  --set environment=production \
  --set database.type=CloudSQL \
  --set storage.type=GCS
```

Azure Deployment

```powershell
# Create AKS cluster
az aks create `
  --resource-group lithosonic-rg `
  --name lithosonic-aks `
  --node-count 3 `
  --node-vm-size Standard_D8s_v3 `
  --enable-addons monitoring `
  --enable-cluster-autoscaler `
  --min-count 3 `
  --max-count 10
```

---

📡 Edge Computing Deployment

Raspberry Pi Field Station

```bash
# setup_raspberry_pi.sh
#!/bin/bash

echo "🌍 Setting up LITHO-SONIC Edge Station on Raspberry Pi"

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git \
  libatlas-base-dev libhdf5-dev libopenblas-dev

# Enable interfaces (I2C, SPI for sensors)
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Configure USB permissions for geophones
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", MODE="0666"' | sudo tee /etc/udev/rules.d/99-litho.rules
sudo udevadm control --reload-rules

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker pi

# Clone repository
git clone https://github.com/gitdeeper8/lithosonic.git
cd lithosonic

# Create optimized config for edge
cat > config/edge.yaml << 'YAML'
mode: "edge"
processing:
  batch_size: 100
  max_workers: 2
  use_gpu: false
  precision: "float16"
  lsi_update: 3600  # Update LSI every hour
storage:
  local_path: "/mnt/data/lithosonic"
  max_size_gb: 100
  retention_days: 30
network:
  sync_interval: 3600
  compress_data: true
  use_4g: true
alerts:
  local: true
  cloud: true
  lsi_critical: 0.80
  lsi_elevated: 0.55
YAML

# Install Python packages
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir -e .

# Create systemd service
sudo cat > /etc/systemd/system/lithosonic.service << 'SERVICE'
[Unit]
Description=LITHO-SONIC Edge Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/lithosonic/scripts/edge_controller.py
WorkingDirectory=/home/pi/lithosonic
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
SERVICE

# Enable service
sudo systemctl enable lithosonic.service
sudo systemctl start lithosonic.service
```

Edge Inference Optimization

```python
# scripts/edge_inference.py
import numpy as np
import tensorflow as tf
from lithosonic.physics import LSI

class EdgeInference:
    """Optimized inference for edge devices"""
    
    def __init__(self, model_path):
        # Load quantized TFLite model
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        # Get input/output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Initialize LSI calculator
        self.lsi_calc = LSI()
    
    def predict_lsi(self, sensor_data):
        """Run edge inference for LSI prediction"""
        # Prepare input tensor
        input_data = self.preprocess(sensor_data)
        self.interpreter.set_tensor(
            self.input_details[0]['index'], 
            input_data
        )
        
        # Run inference
        self.interpreter.invoke()
        
        # Get output
        output = self.interpreter.get_tensor(
            self.output_details[0]['index']
        )
        
        # Calculate LSI from physics
        lsi = self.lsi_calc.compute(sensor_data)
        
        return {
            'lsi': float(lsi),
            'lsi_predicted': float(output[0]),
            'status': self.lsi_calc.get_status(lsi),
            'timestamp': sensor_data['timestamp']
        }
    
    def preprocess(self, data):
        """Optimize data for edge inference"""
        # Extract 5 parameters
        params = np.array([
            data['b_c'], data['z_c'], data['f_n'],
            data['alpha_att'], data['s_ae']
        ], dtype=np.float32)
        
        # Normalize
        params = (params - self.mean) / self.std
        
        # Add batch dimension
        return params.reshape(1, -1)
```

---

🔌 Sensor Integration

USB Device Rules

```bash
# /etc/udev/rules.d/99-lithosonic.rules

# LITHO-GEO v2 Geophone Array (12 channels)
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="geo0", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6002", SYMLINK+="geo1", MODE="0666"
# ... repeat for all 12 channels

# Paros 2200A Pressure Transducer
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", SYMLINK+="paros", MODE="0666"

# MB2005 Microbarometer
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="mb2005", MODE="0666"
```

Sensor Testing

```bash
# Test all sensors
python scripts/test_sensors.py --all

# Test specific sensor
python scripts/test_sensor.py --type geophone --channel 0

# Check data stream
python scripts/monitor_stream.py --duration 60
```

---

🔔 Monitoring & Alerts

Prometheus Configuration

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'lithosonic-stations'
    static_configs:
      - targets:
        - 'kilauea:9100'
        - 'mauna-loa:9100'
        - 'campi-flegrei:9100'
    metrics_path: '/metrics'
    
  - job_name: 'lithosonic-processors'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: lithosonic-processor
        action: keep
```

Alert Rules

```yaml
# prometheus/alerts.yml
groups:
  - name: lithosonic_alerts
    rules:
      - alert: LSICritical
        expr: lithosonic_lsi > 0.80
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "LSI critical at {{ $labels.station }}"
          description: "LSI has exceeded 0.80 for 1 hour"
          
      - alert: LSIElevated
        expr: lithosonic_lsi > 0.55 and lithosonic_lsi < 0.80
        for: 24h
        labels:
          severity: warning
        annotations:
          summary: "LSI elevated at {{ $labels.station }}"
          
      - alert: BiotAnomaly
        expr: lithosonic_b_c > 0.75
        for: 12h
        labels:
          severity: warning
        annotations:
          summary: "Biot coupling anomaly detected"
          
      - alert: SensorOffline
        expr: up{job="lithosonic-stations"} == 0
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Sensor offline: {{ $labels.instance }}"
```

Grafana Dashboard

```json
{
  "dashboard": {
    "title": "LITHO-SONIC Real-Time Monitor",
    "panels": [
      {
        "title": "Lithospheric Stress Index (LSI)",
        "type": "graph",
        "targets": [
          {
            "expr": "lithosonic_lsi{station=\"$station\"}",
            "legendFormat": "LSI"
          }
        ],
        "thresholds": [
          { "value": 0.80, "color": "red" },
          { "value": 0.55, "color": "yellow" },
          { "color": "green" }
        ],
        "yaxes": [
          { "format": "percent", "max": 1.0 }
        ]
      },
      {
        "title": "Five Parameters",
        "type": "graph",
        "targets": [
          { "expr": "lithosonic_b_c{station=\"$station\"}", "legendFormat": "B_c" },
          { "expr": "lithosonic_z_c{station=\"$station\"}", "legendFormat": "Z_c" },
          { "expr": "lithosonic_f_n{station=\"$station\"}", "legendFormat": "f_n" },
          { "expr": "lithosonic_alpha_att{station=\"$station\"}", "legendFormat": "α_att" },
          { "expr": "lithosonic_s_ae{station=\"$station\"}", "legendFormat": "Ṡ_ae" }
        ]
      },
      {
        "title": "Geophone Spectrogram",
        "type": "heatmap",
        "targets": [
          {
            "expr": "lithosonic_spectrogram{station=\"$station\"}",
            "format": "heatmap"
          }
        ]
      }
    ]
  }
}
```

---

💾 Backup & Recovery

Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/data/backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="lithosonic_backup_${DATE}.tar.gz"
S3_BUCKET="s3://lithosonic-backups"

echo "Starting LITHO-SONIC backup: $DATE"

# Backup PostgreSQL (TimescaleDB)
pg_dump -U lithouser -h localhost lithosonic > ${BACKUP_DIR}/database/lithosonic_${DATE}.sql

# Backup configuration
tar -czf ${BACKUP_DIR}/config/config_${DATE}.tar.gz config/ .env

# Backup processed data (keep raw data on site)
tar -czf ${BACKUP_DIR}/processed/processed_${DATE}.tar.gz /data/lithosonic/processed/

# Backup ML models
tar -czf ${BACKUP_DIR}/models/models_${DATE}.tar.gz models/

# Create manifest
cat > ${BACKUP_DIR}/manifest_${DATE}.txt << EOF
Backup Date: $DATE
Database: lithosonic_${DATE}.sql
Config: config_${DATE}.tar.gz
Processed Data: processed_${DATE}.tar.gz
Models: models_${DATE}.tar.gz
Sites: KILAUEA_ERZ_01, CAMPI_FLEGREI_01, SAN_ANDREAS_01
