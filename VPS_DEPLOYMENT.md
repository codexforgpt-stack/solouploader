# VPS Deployment Guide - Solo Beast Bot

This guide explains how to deploy the **Solo Beast Bot** on a Linux VPS (Ubuntu/Debian).

## 1. Prerequisites
- A VPS running Ubuntu 20.04+ or Debian 10+.
- SSH access to your VPS.

## 2. Clone the Repository
```bash
git clone <your-repo-link>
cd uploader-golu-babu-with-port-binding-edit-main
```

## 3. Automatic Setup
Run the provided setup script to install all system dependencies (ffmpeg, aria2, mp4decrypt) and Python packages.
```bash
chmod +x setup.sh
./setup.sh
```

## 4. Configuration
Create a `.env` file from the example and fill in your details.
```bash
cp .env.example .env
nano .env
```
Press `Ctrl+O` then `Enter` to save, and `Ctrl+X` to exit.

## 5. Running the Bot
### Method 1: Simple Run (stops if you close SSH)
```bash
python3 main.py
```

### Method 2: Using PM2 (Recommended for VPS)
Keep the bot running in the background and auto-restart on crashes.
```bash
# Install PM2
sudo apt install npm -y
sudo npm install -g pm2

# Start the bot
pm2 start main.py --name "solo-beast" --interpreter python3

# Check status
pm2 status
pm2 logs solo-beast
```

## 6. Keeping the Bot Alive
To ensure PM2 starts on boot:
```bash
pm2 startup
pm2 save
```

---
**Solo Beast Bot** is now ready on your VPS! 🚀
