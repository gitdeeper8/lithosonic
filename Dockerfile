# LITHO-SONIC Dockerfile
# Lithospheric Resonance & Infrasonic Geomechanical Observatory
# Version: 1.0.0 | DOI: 10.5281/zenodo.18931304

FROM python:3.10-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# -----------------------------------------------------------------------------
# Final image
# -----------------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Install package
RUN pip install --no-cache-dir -e .

# Create data directories
RUN mkdir -p /data/lithosonic/raw \
    /data/lithosonic/processed \
    /data/lithosonic/backup \
    /logs \
    /config

# Copy default config
COPY config/*.yaml /config/

# Expose ports
EXPOSE 5000 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LITHOSONIC_HOME=/app \
    LITHOSONIC_DATA=/data/lithosonic \
    LITHOSONIC_CONFIG=/config \
    LITHOSONIC_LOGS=/logs

# Default command
CMD ["lithosonic-serve", "--host", "0.0.0.0", "--port", "5000"]

# Labels
LABEL org.opencontainers.image.title="LITHO-SONIC"
LABEL org.opencontainers.image.description="Lithospheric Resonance & Infrasonic Geomechanical Observatory"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Samir Baladi <gitdeeper@gmail.com>"
LABEL org.opencontainers.image.url="https://github.com/gitdeeper8/lithosonic"
LABEL org.opencontainers.image.documentation="https://lithosonic.netlify.app/docs"
LABEL org.opencontainers.image.doi="10.5281/zenodo.18931304"
