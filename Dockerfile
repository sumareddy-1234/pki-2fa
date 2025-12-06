# Use Ubuntu base for stability under WSL2
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install Python, pip, and cron
RUN apt-get update --fix-missing && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip cron && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data and cron folders
RUN mkdir -p /data /cron

# Setup cron job
COPY cron/crontab /etc/cron.d/pki-cron
RUN chmod 0644 /etc/cron.d/pki-cron && crontab /etc/cron.d/pki-cron

# Run cron in foreground and FastAPI app
CMD cron -f & uvicorn main:app --host 0.0.0.0 --port 8080
