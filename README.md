# 🐍 Python System Watchdog

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Status](https://img.shields.io/badge/Status-Stable-green)

A lightweight, containerized agent that monitors Linux system resources (CPU, RAM, Disk) and sends real-time alerts via Telegram when critical thresholds are exceeded.

Designed with **DevOps best practices** in mind:
- 🐳 **Dockerized** for easy deployment anywhere.
- 🔒 **Secure** configuration via Environment Variables (no hardcoded secrets).
- ⚡ **Low footprint** using `psutil`.

## 🚀 Features
- **Real-time Monitoring:** Checks system health every minute (configurable via Cron).
- **Smart Alerting:** Sends Telegram notifications only when resources are critical:
  - 💿 Disk Usage > 80%
  - 💾 RAM Usage > 90%
- **Cross-Platform:** Runs on any Linux distro, macOS, or Cloud Server (AWS/Azure) via Docker.

## 🛠️ Installation & Usage

### Option 1: Run with Docker (Recommended)
No Python installation required. Just run the container:

```bash
# Build the image
docker build -t system-watchdog .

# Run the container (replace with your tokens)
docker run --rm \
  -e TELEGRAM_TOKEN="YOUR_BOT_TOKEN" \
  -e TELEGRAM_CHAT_ID="YOUR_CHAT_ID" \
  system-watchdog
