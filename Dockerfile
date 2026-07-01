FROM python:3.11-slim

# Install essential system dependencies and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p config reports/raw reports/daily scripts

# Copy source code and scripts
# (In development we mount volumes, but we also copy them here to make the image standalone if needed)
COPY config/ /app/config/
COPY scripts/ /app/scripts/

# Ensure the run script is executable
RUN chmod +x /app/scripts/run_pipeline.sh

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Entrypoint to run the entire pipeline
CMD ["/bin/bash", "/app/scripts/run_pipeline.sh"]
