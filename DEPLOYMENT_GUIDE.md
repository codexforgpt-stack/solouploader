# 🚀 Uploader Bot - Deployment Guide

## ⚠️ **Important: Deployment Limitations**

### **Cannot Deploy To:**
- ❌ **Heroku** - Requires `ffmpeg`, `mp4decrypt`, and `aria2c` binaries (buildpack needed)
- ❌ **Koyeb** - Free tier doesn't support custom binary installations
- ❌ **Railway** - Similar constraints with binary dependencies

### **Why Deployment Is Difficult:**

This bot requires **3 external binaries**:
1. **ffmpeg** (~60MB) - Video/audio processing
2. **mp4decrypt** (Bento4) - DRM decryption  
3. **aria2c** (~5MB) - Fast downloads

Most free cloud services **don't allow custom binary installations** or have strict size limits.

---

## ✅ **Recommended Deployment Options:**

### **Option 1: VPS (Best Option)** ⭐
**Services:**
- **Oracle Cloud** (Free tier - 2 ARM instances)
- **Google Cloud** (Free $300 credit)
- **DigitalOcean** ($4/month droplet)
- **Contabo** (€3.99/month)

**Pros:**
- Full control over binaries
- Can install anything
- Persistent storage

**Setup Steps:**
```bash
# 1. SSH into VPS
ssh user@your-vps-ip

# 2. Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg aria2

# 3. Install Bento4 (mp4decrypt)
wget https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip
unzip Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip
sudo cp Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt /usr/local/bin/

# 4. Clone your bot
git clone <your-repo-url>
cd UPLOADER_FAST-V2

# 5. Install Python packages
pip3 install -r requirements.txt

# 6. Set environment variables
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
export DATABASE_URL="your_mongodb_url"

# 7. Run bot
python3 main.py
```

---

### **Option 2: Docker + Any Cloud** 🐳

**Services:**
- Render (Free tier with Docker)
- Railway (With Docker support)
- Any VPS

**Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    aria2 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Bento4 (mp4decrypt)
RUN wget https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip \
    && unzip Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip \
    && cp Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt /usr/local/bin/ \
    && rm -rf Bento4-SDK-1-6-0-641.x86_64-unknown-linux*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY . .

# Run bot
CMD ["python", "main.py"]
```

**Deploy to Render:**
1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: uploader-bot
    env: docker
    plan: free
    envVars:
      - key: API_ID
        value: your_api_id
      - key: API_HASH
        value: your_api_hash
      - key: BOT_TOKEN
        value: your_bot_token
      - key: DATABASE_URL
        value: your_mongodb_url
```

2. Connect GitHub repo to Render
3. Deploy automatically!

---

### **Option 3: Replit (Limited)**

Replit pe chal sakta hai but **storage limited** hai aur **24/7 running nahi hoga** free tier pe.

---

## 📦 **Requirements File**

Create `requirements.txt`:
```txt
pyrogram==2.0.106
pyromod==3.1.6
TgCrypto==1.2.5
motor==3.7.1
pymongo==4.15.5
yt-dlp==2025.12.8
requests==2.32.5
aiohttp==3.13.2
pillow==12.0.0
python-dotenv==1.2.1
beautifulsoup4==4.14.3
cloudscraper==1.2.71
m3u8==6.0.0
pycryptodome==3.23.0
```

---

## 🔧 **Environment Variables**

Set these on your deployment platform:

```env
API_ID=34439627
API_HASH=e5c7efb57949e742889aa96bf64c4552
BOT_TOKEN=8517402286:AAGXi5xBwzv2u49lbW-oKWAlAfrE3Wx3Ov8
DATABASE_URL=mongodb+srv://raja1998:KKTvc387mkPPszeQ@cluster0.vgopiet.mongodb.net/?appName=Cluster0
DATABASE_NAME=classplus_bot
OWNER_ID=7208112327
ADMINS=7208112327
```

---

## ⚡ **Quick Deploy Commands**

### **For Ubuntu/Debian VPS:**
```bash
# One-line setup
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash - && \
sudo apt-get update && \
sudo apt-get install -y python3 python3-pip ffmpeg aria2 wget unzip git && \
wget https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip && \
unzip Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip && \
sudo cp Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt /usr/local/bin/ && \
echo "✅ All dependencies installed!"
```

---

## 🎯 **Best Recommendation:**

**Use Oracle Cloud Free Tier:**
- ✅ Free forever (2 VMs)
- ✅ 200GB storage
- ✅ Full control
- ✅ Can install anything
- ✅ 24/7 uptime

**Total Cost: FREE!** 🎉

---

## ⚠️ **Notes:**

1. **Windows binaries won't work on Linux** - Use Linux binaries for deployment
2. **MongoDB Atlas** (free tier) recommended for database
3. **Keep bot token safe** - Use environment variables
4. **FFmpeg size** - Can increase deployment time

---

**Need help with specific deployment? Let me know!** 😊
