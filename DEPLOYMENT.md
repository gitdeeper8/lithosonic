# 🌍 LITHO-SONIC Deployment Guide (Detailed)
## Lithospheric Resonance & Infrasonic Geomechanical Observatory

**DOI**: 10.5281/zenodo.18931304  
**Repository**: github.com/gitdeeper8/lithosonic  
**Web**: lithosonic.netlify.app

---

## 📋 Table of Contents
- [Deployment Architectures](#deployment-architectures)
- [Single Station Deployment](#single-station-deployment)
- [Multi-Station Network](#multi-station-network)
- [Cloud Deployment](#cloud-deployment)
- [Edge Computing](#edge-computing)
- [Sensor Integration](#sensor-integration)
- [Data Pipeline](#data-pipeline)
- [Monitoring & Alerts](#monitoring--alerts)
- [Backup & Recovery](#backup--recovery)
- [Security](#security)
- [Performance Tuning](#performance-tuning)
- [Troubleshooting](#troubleshooting)

---

## 🏗️ Deployment Architectures

### Architecture Comparison

| Architecture | Use Case | Pros | Cons | Cost |
|-------------|----------|------|------|------|
| **Single Station** | Remote geophysical site | Simple, low latency | Limited coverage | Low |
| **Multi-Station Network** | Volcanic/fault monitoring | Comprehensive, redundant | Complex setup | Medium |
| **Cloud-Based** | Global monitoring network | Highly scalable, accessible | Internet dependent | High |
| **Edge Computing** | Real-time alerts | Low latency, offline capable | Limited compute | Medium |

---

## 🖥️ Single Station Deployment

### Hardware Requirements
```yaml
Minimum Specifications:
  CPU: Intel NUC i5 / Raspberry Pi 4 (8GB)
  RAM: 8GB
  Storage: 1TB SSD (expandable)
  Network: 4G/LTE modem (for remote sites)
  Power: Solar + Battery backup (200W panel, 200Ah battery)
  Enclosure: IP67 weatherproof case
  Sensors: 
    - LITHO-GEO v2 (12-element geophone array)
    - LITHO-DAS (4 km fiber optic cable)
    - STS-5A broadband seismometer
    - Paros 2200A pressure transducer (30 m borehole)
    - MB2005 microbarometer
    - Titan accelerometers (8 units)
```

Installation Steps

```bash
# 1. Prepare the system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip docker.io docker-compose git

# 2. Clone repository
git clone https://github.com/gitdeeper8/lithosonic.git
cd lithosonic

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your station details

# 4. Install dependencies
pip install -r requirements.txt
pip install -e .

# 5. Configure USB permissions for sensors
sudo cp config/udev/99-lithosonic.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules

# 6. Test sensors
python scripts/test_sensors.py --all

# 7. Initialize database
python scripts/init_db.py

# 8. Start services
docker-compose -f docker-compose.dev.yml up -d

# 9. Verify deployment
curl http://localhost:5000/health
python scripts/verify_deployment.py
```

Station Configuration

```yaml
# config/station.yaml
station:
  id: "KILAUEA_ERZ_01"
  name: "Kīlauea East Rift Zone"
  latitude: 19.41
  longitude: -155.28
  elevation: 1100
  environment: "intraplate_volcanic"
  deployment_date: "2026-03-10"

sensors:
  geophone:
    enabled: true
    base_port: "/dev/ttyUSB"
    channels: 12
    sample_rate: 1000
    spacing: 50
    pattern: "cross"
    calibration_file: "config/calibration/geo_2026.json"
  
  das:
    enabled: true
    cable_length: 4000
    spatial_resolution: 1
    sample_rate: 500
    calibration_file: "config/calibration/das_2026.json"
  
  sts5a:
    enabled: true
    ip: "192.168.1.100"
    port: 5000
    sample_rate: 200
    response_file: "config/response/sts5a.xml"
  
  paros:
    enabled: true
    port: "/dev/ttyUSB12"
    baudrate: 9600
    interval: 60
    borehole_depth: 30
    calibration_file: "config/calibration/paros_2026.json"
  
  mb2005:
    enabled: true
    port: "/dev/ttyUSB13"
    sample_rate: 100
    wind_height: 1.5
  
  titan:
    enabled: true
    count: 8
    base_ip: "192.168.1.200"
    sample_rate: 500
    spacing: 500

processing:
  spectral:
    window: 60
    overlap: 0.5
    fft_size: 2048
  
  inversion:
    method: "conjugate_gradient"
    max_iterations: 100
    tolerance: 1e-6
    monte_carlo_samples: 2000
  
  lsi:
    update_interval: 3600
    critical_threshold: 0.80
    elevated_threshold: 0.55

storage:
  data_dir: "/data/lithosonic"
  raw_dir: "/data/lithosonic/raw"
  processed_dir: "/data/lithosonic/processed"
  backup_dir: "/data/lithosonic/backup"
  retention_days: 365
  compression: "gzip"

network:
  sync_interval: 3600
  cloud_endpoint: "https://api.lithosonic.netlify.app"
  mqtt_broker: "mqtt.lithosonic.netlify.app"
  mqtt_port: 8883
  use_tls: true
  compress_data: true

power:
  source: "solar"
  panel_wattage: 200
  battery_ah: 200
  voltage: 12
  low_power_mode: true
  low_power_threshold: 11.5

alerts:
  enabled: true
  check_interval: 300
  channels:
    email:
      enabled: true
      recipients: ["monitor@lithosonic.org"]
      smtp_server: "smtp.gmail.com"
      smtp_port: 587
    slack:
      enabled: false
      webhook: "https://hooks.slack.com/services/xxx"
    sms:
      enabled: false
```

---

🌐 Multi-Station Network

Network Architecture

```
                    ┌─────────────────────────────────────┐
                    │         Regional Hub                 │
                    │    (TimescaleDB + Processing)        │
                    └─────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   Station 1     │     │   Station 2     │     │   Station 3     │
    │   Kīlauea ERZ   │     │   Mauna Loa     │     │   Hualālai      │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │  12 Geophones   │     │  12 Geophones   │     │  12 Geophones   │
    │  4km DAS        │     │  4km DAS        │     │  4km DAS        │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
```

Hub Configuration

```yaml
# config/hub.yaml
hub:
  id: "HAWAII_HUB_01"
  region: "hawaii"
  endpoints:
    api: "https://api.lithosonic.net"
    websocket: "wss://ws.lithosonic.net"
    mqtt: "mqtt.lithosonic.net:8883"

database:
  type: "timescaledb"
  host: "timescaledb.lithosonic.net"
  port: 5432
  name: "lithosonic"
  user: "lithouser"
  password: "${DB_PASSWORD}"
  pool_size: 100
  ssl_mode: "require"
  
  timescale:
    chunk_interval: "7 days"
    retention_period: "10 years"
    compression: true
    compression_after: "30 days"

cache:
  type: "redis"
  host: "redis.lithosonic.net"
  port: 6379
  max_memory: "8gb"
  eviction_policy: "allkeys-lru"

message_queue:
  type: "rabbitmq"
  hosts:
    - "rabbit1.lithosonic.net"
    - "rabbit2.lithosonic.net"
    - "rabbit3.lithosonic.net"
  port: 5672
  vhost: "lithosonic"
  user: "lithouser"
  password: "${RABBITMQ_PASSWORD}"

stations:
  - id: "KILAUEA_ERZ_01"
    sync_interval: 300
    priority: 1
    data_types: ["raw", "processed", "lsi"]
    
  - id: "MAUNA_LOA_01"
    sync_interval: 600
    priority: 2
    data_types: ["processed", "lsi"]
    
  - id: "HUALALAI_01"
    sync_interval: 900
    priority: 3
    data_types: ["lsi"]

processing:
  distributed:
    enabled: true
    workers: 10
    queue: "processing_queue"
    
  lsi_aggregation:
    interval: 3600
    method: "weighted_average"
    
  alerting:
    check_interval: 300
    rules:
      - name: "LSI Critical Any Station"
        condition: "any(lsi > 0.80)"
        severity: "critical"
      - name: "LSI Elevated Multiple Stations"
        condition: "count(lsi > 0.55) >= 2"
        severity: "warning"
```

Station-to-Hub Sync

```python
# scripts/sync_client.py
import asyncio
import aiomqtt
import aiohttp
import json
import zlib
from datetime import datetime

class LithoSyncClient:
    """Sync client for field station"""
    
    def __init__(self, station_id, hub_config):
        self.station_id = station_id
        self.hub = hub_config
        self.queue = asyncio.Queue()
        self.running = True
    
    async def mqtt_sync(self):
        """Real-time sync via MQTT"""
        async with aiomqtt.Client(
            self.hub['mqtt_broker'],
            port=self.hub['mqtt_port'],
            username=self.hub['mqtt_user'],
            password=self.hub['mqtt_password'],
            tls_params=aiomqtt.TLSParameters()
        ) as client:
            
            # Publish LSI every 5 minutes
            while self.running:
                lsi_data = await self.get_current_lsi()
                await client.publish(
                    f"lithosonic/{self.station_id}/lsi",
                    json.dumps(lsi_data)
                )
                await asyncio.sleep(300)
    
    async def batch_sync(self):
        """Batch sync of raw data"""
        while self.running:
            await asyncio.sleep(3600)  # Every hour
            
            # Get unsynced data
            data = await self.get_unsynced_data()
            if not data:
                continue
            
            # Compress
            compressed = zlib.compress(json.dumps(data).encode())
            
            # Send to hub
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.hub['api_endpoint']}/sync",
                    data=compressed,
                    headers={
                        "X-Station-ID": self.station_id,
                        "Content-Type": "application/octet-stream",
                        "X-API-Key": self.hub['api_key']
                    }
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        await self.mark_as_synced(result['synced_ids'])
    
    async def get_current_lsi(self):
        """Get current LSI value"""
        # Read from local database
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "station_id": self.station_id,
            "lsi": 0.72,
            "parameters": {
                "b_c": 0.68,
                "z_c": 0.71,
                "f_n": 2.3,
                "alpha_att": 0.65,
                "s_ae": 0.69
            }
        }
    
    async def run(self):
        """Run sync service"""
        await asyncio.gather(
            self.mqtt_sync(),
            self.batch_sync()
        )
```

---

☁️ Cloud Deployment

AWS CloudFormation Template

```yaml
# cloudformation/lithosonic.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'LITHO-SONIC Cloud Infrastructure'

Parameters:
  EnvironmentName:
    Type: String
    Default: production
    AllowedValues: [development, staging, production]
  
  DBPassword:
    Type: String
    NoEcho: true

Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-vpc

  # RDS TimescaleDB
  TimescaleDB:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: postgres
      EngineVersion: '15.3'
      DBInstanceClass: db.r5.2xlarge
      AllocatedStorage: 1000
      StorageEncrypted: true
      DBName: lithosonic
      MasterUsername: lithoadmin
      MasterUserPassword: !Ref DBPassword
      VPCSecurityGroups: [!Ref DBSecurityGroup]
      DBSubnetGroupName: !Ref DBSubnetGroup
      BackupRetentionPeriod: 30
      MultiAZ: true
      EnableCloudwatchLogsExports: ['postgresql']
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-timescaledb

  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub ${EnvironmentName}-cluster
      ClusterSettings:
        - Name: containerInsights
          Value: enabled

  # S3 Bucket for Raw Data
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub lithosonic-${EnvironmentName}-${AWS::AccountId}
      LifecycleConfiguration:
        Rules:
          - Id: ArchiveOldData
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER
            ExpirationInDays: 3650
      VersioningConfiguration:
        Status: Enabled

  # CloudWatch Alarms
  LSICriticalAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub ${EnvironmentName}-lsi-critical
      ComparisonOperator: GreaterThanThreshold
      EvaluationPeriods: 2
      MetricName: LSI
      Namespace: LITHO-SONIC
      Period: 3600
      Statistic: Maximum
      Threshold: 0.80
      AlarmActions: [!Ref AlertTopic]
```

Deployment Script

```bash
#!/bin/bash
# deploy_aws.sh

echo "Deploying LITHO-SONIC to AWS..."

# Set variables
ENVIRONMENT=${1:-production}
STACK_NAME="lithosonic-${ENVIRONMENT}"
REGION="us-west-2"

# Generate random password
DB_PASSWORD=$(openssl rand -base64 32)

# Deploy CloudFormation
aws cloudformation deploy \
  --template-file cloudformation/lithosonic.yaml \
  --stack-name ${STACK_NAME} \
  --region ${REGION} \
  --parameter-overrides \
    EnvironmentName=${ENVIRONMENT} \
    DBPassword=${DB_PASSWORD} \
  --capabilities CAPABILITY_IAM

# Get outputs
aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --query 'Stacks[0].Outputs' \
  --region ${REGION}

# Configure ECS
aws ecs update-service \
  --cluster ${STACK_NAME}-cluster \
  --service lithosonic-processor \
  --desired-count 3 \
  --region ${REGION}

echo "Deployment complete!"
echo "DB Password: ${DB_PASSWORD} (save this securely)"
```

GCP Deployment

```bash
#!/bin/bash
# deploy_gcp.sh

PROJECT_ID="lithosonic-2026"
REGION="us-west1"

# Create project
gcloud projects create ${PROJECT_ID} --name="LITHO-SONIC"

# Enable APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Create GKE cluster
gcloud container clusters create lithosonic-cluster \
  --project=${PROJECT_ID} \
  --region=${REGION} \
  --num-nodes=3 \
  --machine-type=e2-standard-8 \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=10

# Create Cloud SQL instance
gcloud sql instances create lithosonic-db \
  --project=${PROJECT_ID} \
  --region=${REGION} \
  --database-version=POSTGRES_15 \
  --tier=db-custom-8-32768 \
  --storage-size=1000 \
  --storage-auto-increase \
  --backup-start-time=03:00

# Create bucket for data
gsutil mb -l ${REGION} gs://lithosonic-${PROJECT_ID}/

# Deploy with Helm
gcloud container clusters get-credentials lithosonic-cluster --region=${REGION}
helm repo add lithosonic https://lithosonic.netlify.app/charts
helm install lithosonic lithosonic/lithosonic \
  --set environment=production \
  --set database.type=CloudSQL \
  --set storage.type=GCS
```

Azure Deployment

```powershell
# deploy_azure.ps1

$resourceGroup = "lithosonic-rg"
$location = "westus2"
$clusterName = "lithosonic-aks"

# Create resource group
az group create --name $resourceGroup --location $location

# Create AKS cluster
az aks create `
  --resource-group $resourceGroup `
  --name $clusterName `
  --node-count 3 `
  --node-vm-size Standard_D8s_v3 `
  --enable-addons monitoring `
  --enable-cluster-autoscaler `
  --min-count 3 `
  --max-count 10

# Create PostgreSQL flexible server
az postgres flexible-server create `
  --resource-group $resourceGroup `
  --name lithosonic-db `
  --location $location `
  --admin-user lithoadmin `
  --admin-password (Read-Host -AsSecureString "Enter password") `
  --sku-name Standard_D4ds_v4 `
  --storage-size 1024 `
  --version 15

# Create storage account
az storage account create `
  --resource-group $resourceGroup `
  --name lithosonicdata `
  --location $location `
  --sku Standard_LRS

# Get credentials
az aks get-credentials --resource-group $resourceGroup --name $clusterName

# Deploy with Helm
helm repo add lithosonic https://lithosonic.netlify.app/charts
helm install lithosonic lithosonic/lithosonic `
  --set environment=production `
  --set database.type=AzurePostgreSQL `
  --set storage.type=AzureBlob
```

---

📡 Edge Computing Deployment

Raspberry Pi 4 Field Station

```bash
#!/bin/bash
# setup_edge_station.sh

echo "🌍 Setting up LITHO-SONIC Edge Station on Raspberry Pi"

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git \
  libatlas-base-dev libhdf5-dev libopenblas-dev \
  libusb-1.0-0-dev i2c-tools

# Enable interfaces
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_serial 2

# Configure USB permissions
cat << EOF | sudo tee /etc/udev/rules.d/99-lithosonic.rules
# LITHO-GEO v2 Geophones
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="geo%n", MODE="0666"
# Paros 2200A
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", SYMLINK+="paros", MODE="0666"
# MB2005
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="mb2005", MODE="0666"
