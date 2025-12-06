# PKI 2FA Microservice 🔐

A FastAPI microservice that demonstrates **Public Key Infrastructure (PKI)** and **Two-Factor Authentication (2FA)** using Docker and cron jobs.  
It decrypts a seed, generates TOTP codes, verifies them, and refreshes codes automatically every 70 seconds.

---

## 🚀 Features
- **Decrypt Seed** → Securely decrypts an encrypted seed via API.
- **Generate 2FA** → Produces time-based one-time codes (TOTP).
- **Verify 2FA** → Validates user-provided codes.
- **Cron Integration** → Refreshes codes every 70 seconds and stores them in `/cron/last_code.txt`.
- **Dockerized** → Runs consistently across environments with Docker Compose.

---

## 🛠 Tech Stack
- **FastAPI** (Python web framework)
- **Ubuntu 22.04** (base image)
- **Docker + Docker Compose**
- **Cron** (scheduled jobs)

---

## 📦 Setup & Run

### 1. Build the image
```bash
docker compose build --no-cache
