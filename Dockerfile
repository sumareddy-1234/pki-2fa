FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data /cron

COPY cron/crontab /etc/cron.d/pki-cron
RUN chmod 0644 /etc/cron.d/pki-cron && crontab /etc/cron.d/pki-cron

CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080
