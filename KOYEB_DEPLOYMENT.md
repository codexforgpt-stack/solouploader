# 🚀 Koyeb Deployment Guide - Uploader Bot

## ⚠️ **Important Notes:**

**Koyeb Limitations:**
- ✅ **Docker support** - Can deploy with Docker
- ⚠️ **Free tier:** 512MB RAM, may struggle with large videos
- ⚠️ **Ephemeral storage** - Files deleted after restart
- ⚠️ **No persistent disk** - Session files may be lost
- ✅ **Good for:** Testing, small videos (<100MB)

**Recommendation:** Use Koyeb for testing, VPS for production.

---

## 📋 **Prerequisites:**

1. **GitHub Account** - To host your code
2. **Koyeb Account** - Sign up at https://www.koyeb.com/
3. **MongoDB Atlas** - Free database (https://www.mongodb.com/cloud/atlas)
4. **Bot Token** - From @BotFather

---

## 🔧 **Step-by-Step Deployment:**

### **Step 1: Prepare GitHub Repository**

1. **Create a new GitHub repo** (or use existing)

2. **Copy bot files to repo:**
   ```bash
   # Navigate to bot folder
   cd UPLOADER_FAST-V2
   
   # Initialize git (if not already)
   git init
   
   # Add files
   git add Dockerfile .dockerignore requirements.txt *.py
   
   # Commit
   git commit -m "Initial commit for Koyeb deployment"
   
   # Add remote (replace with your repo URL)
   git remote add origin https://github.com/YOUR_USERNAME/uploader-bot.git
   
   # Push
   git push -u origin main
   ```

3. **Verify these files are in repo:**
   - ✅ `Dockerfile`
   - ✅ `.dockerignore`
   - ✅ `requirements.txt`
   - ✅ `main.py`
   - ✅ `vars.py`
   - ✅ `db.py`
   - ✅ All other .py files

---

### **Step 2: Setup MongoDB Atlas (Free)**

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up / Log in
3. Create **Free Cluster** (M0 tier)
4. Click **Connect** → **Connect your application**
5. Copy connection string:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `username` and `password` with actual values
7. Keep this URL safe - needed for Koyeb!

---

### **Step 3: Deploy to Koyeb**

#### **3.1: Login to Koyeb**
- Go to https://app.koyeb.com/
- Sign up using GitHub (recommended)

#### **3.2: Create New Service**
1. Click **"Create Service"**
2. Select **"Docker"** as deployment method
3. Choose **"GitHub"** as source

#### **3.3: Configure Deployment**

**Builder Settings:**
- **Git Repository:** Select your `uploader-bot` repo
- **Branch:** `main`
- **Dockerfile:** `Dockerfile` (auto-detected)

**Instance Settings:**
- **Service Name:** `uploader-bot`
- **Region:** Choose closest to you
- **Instance Type:** `Free` (Eco)

**Environment Variables:** (Click "Add Variable")
```
API_ID = 34439627
API_HASH = e5c7efb57949e742889aa96bf64c4552
BOT_TOKEN = 8517402286:AAGXi5xBwzv2u49lbW-oKWAlAfrE3Wx3Ov8
DATABASE_URL = mongodb+srv://raja1998:KKTvc387mkPPszeQ@cluster0.vgopiet.mongodb.net/?appName=Cluster0
DATABASE_NAME = classplus_bot
OWNER_ID = 7208112327
ADMINS = 7208112327
LOG_CHANNEL_ID = 0
DUMP_CHANNEL_ID = 0
```

**⚠️ Important:** Replace with your actual values!

**Port Settings:**
- **Exposed Port:** `8000`
- **Protocol:** `HTTP`

**Health Checks:**
- **Path:** `/` (or leave default)
- **Port:** `8000`

#### **3.4: Deploy!**
1. Click **"Deploy"**
2. Wait 5-10 minutes for build
3. Check **Logs** tab for progress

---

### **Step 4: Verify Deployment**

#### **Check Logs:**
```
[DATABASE] Initializing ITsGOLU_UPLOADER Bot Database
[OK] MongoDB Connected Successfully!
Bot Started...
```

If you see this → ✅ **Success!**

#### **Test Bot:**
1. Open Telegram
2. Search your bot (@your_bot_username)
3. Send `/start`
4. If bot responds → ✅ **Working!**

---

## 🔥 **Quick Deploy (Alternative)**

If GitHub setup is complex, use **Koyeb CLI:**

```bash
# Install Koyeb CLI
curl -fsSL https://cli.koyeb.com/install.sh | sh

# Login
koyeb login

# Deploy from local directory
koyeb app init uploader-bot \
  --docker . \
  --ports 8000:http \
  --routes /:8000 \
  --env API_ID=34439627 \
  --env API_HASH=e5c7efb57949e742889aa96bf64c4552 \
  --env BOT_TOKEN=your_bot_token \
  --env DATABASE_URL=your_mongodb_url

# Deploy
koyeb app deploy uploader-bot
```

---

## ⚡ **Post-Deployment:**

### **Monitor Bot:**
```bash
# View logs
koyeb service logs uploader-bot

# Check status
koyeb service get uploader-bot

# Restart if needed
koyeb service redeploy uploader-bot
```

### **Update Bot:**
```bash
# Make changes locally
git add .
git commit -m "Update bot"
git push

# Koyeb auto-deploys on push! ✅
```

---

## ⚠️ **Known Issues & Solutions:**

### **Issue 1: Bot keeps restarting**
**Cause:** Free tier RAM limit (512MB)  
**Solution:** 
- Reduce video quality to 480p
- Process one video at a time
- Upgrade to Starter plan ($5/month)

### **Issue 2: Session file lost on restart**
**Cause:** Ephemeral storage  
**Solution:**
- Bot will re-authenticate automatically
- Use persistent storage (paid plan)
- Or use VPS instead

### **Issue 3: Large video downloads fail**
**Cause:** RAM/disk limits  
**Solution:**
- Limit video size in code
- Use VPS for large files
- Split into smaller chunks

### **Issue 4: Build failed**
**Cause:** Dockerfile errors  
**Solution:**
- Check logs in Koyeb dashboard
- Verify all files in GitHub
- Ensure Dockerfile syntax is correct

---

## 💡 **Optimization Tips:**

### **1. Reduce Docker Image Size:**
```dockerfile
# Use alpine instead of slim
FROM python:3.10-alpine

# Multi-stage build
FROM python:3.10-slim as builder
# ... build steps
FROM python:3.10-slim
COPY --from=builder /usr/local /usr/local
```

### **2. Faster Builds:**
```bash
# Cache Python packages
RUN pip install --no-cache-dir -r requirements.txt
```

### **3. Better Logging:**
```python
# Add to main.py
import logging
logging.basicConfig(level=logging.INFO)
```

---

## 📊 **Resource Usage:**

**Free Tier Limits:**
- RAM: 512MB
- Disk: 2GB (ephemeral)
- CPU: Shared
- Executions: 100,000/month

**Typical Bot Usage:**
- Idle: ~150MB RAM
- Downloading: ~300MB RAM
- Processing: ~400MB RAM
- **Risk of OOM** on large videos!

---

## 🎯 **Alternatives if Koyeb Doesn't Work:**

### **1. Render.com** (Docker support)
- Free tier: 750 hours/month
- More RAM: 512MB-1GB
- Better for bots

### **2. Railway.app** (Docker support)
- Free tier: $5 credit/month
- Good performance
- Easy setup

### **3. Oracle Cloud** (Best - Forever Free!)
- 2 VMs free forever
- 1GB RAM each
- Full control
- **Highly Recommended!**

---

## ✅ **Success Checklist:**

Before deploying, verify:
- [ ] Dockerfile exists and is valid
- [ ] .dockerignore exists
- [ ] requirements.txt has all packages
- [ ] GitHub repo is public (or Koyeb has access)
- [ ] MongoDB Atlas cluster is created
- [ ] Environment variables are correct
- [ ] Bot token is valid (test with /start locally first)

---

## 🆘 **Getting Help:**

**Check Logs:**
```bash
# Koyeb dashboard → Services → uploader-bot → Logs
```

**Common Log Messages:**
- ✅ `Bot Started...` = Success!
- ❌ `ModuleNotFoundError` = Missing in requirements.txt
- ❌ `MongoDB connection failed` = Check DATABASE_URL
- ❌ `Invalid token` = Check BOT_TOKEN

---

## 🚀 **Ready to Deploy?**

1. ✅ Push code to GitHub
2. ✅ Setup MongoDB Atlas
3. ✅ Create Koyeb service
4. ✅ Add environment variables
5. ✅ Deploy and monitor logs!

**Good luck! Bot deploy ho jayega! 🎉**

---

**Need help?** Check bot logs first, then ping me! 😊
