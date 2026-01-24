# 🤖 Uploader Bot - Features & Commands Guide

## 📋 **Complete Command List**

### **👤 User Commands:**

#### 1. `/start`
- **Description:** Start the bot and see welcome message
- **Access:** Everyone
- **Example:** `/start`

#### 2. `/drm` ⭐
- **Description:** Download and decrypt DRM-protected ClassPlus videos
- **Access:** Authorized users only
- **How to use:**
  1. Send `/drm` command
  2. Bot will ask for txt file
  3. Send txt file with format:
     ```
     Video Name 1: https://media-cdn.classplusapp.com/drm/wv/.../video.mpd
     Video Name 2: https://media-cdn.classplusapp.com/drm/wv/.../video.mpd
     ```
  4. Bot will:
     - Download encrypted video/audio
     - Decrypt using mp4decrypt
     - Merge using ffmpeg
     - Upload to Telegram
     - Generate thumbnail automatically

#### 3. `/id`
- **Description:** Get your Telegram user ID
- **Access:** Everyone
- **Example:** `/id`
- **Response:** `Your ID: 7208112327`

#### 4. `/stop`
- **Description:** Stop current download/upload process
- **Access:** Everyone
- **Example:** `/stop`

#### 5. `/t2t`
- **Description:** Convert Telegram file to text list
- **Access:** Authorized users
- **How to use:**
  1. Send `/t2t`
  2. Forward messages from channel/group
  3. Bot extracts all file names

#### 6. `/t2h`
- **Description:** Convert text to HTML formatted message
- **Access:** Authorized users
- **Example:** Send txt file after `/t2h`

---

### **🔑 Admin Commands:**

#### 1. `/setlog`
- **Description:** Set log channel for bot activities
- **Access:** Admin only
- **Format:** `/setlog -100123456789`
- **Example:** `/setlog -1001234567890`

#### 2. `/getlog`
- **Description:** Get current log channel ID
- **Access:** Admin only
- **Example:** `/getlog`

#### 3. `/logs`
- **Description:** Get bot error logs
- **Access:** Admin only
- **Example:** `/logs`

#### 4. `/cookies`
- **Description:** Set cookies for protected downloads
- **Access:** Admin only
- **How to use:**
  1. Send `/cookies` command
  2. Send cookie.txt file
  3. Bot will store for future downloads

#### 5. `/getcookies`
- **Description:** Get currently stored cookies
- **Access:** Admin only
- **Example:** `/getcookies`

---

## 🎯 **Key Features**

### **1. DRM Video Decryption** ⭐
- **Supported Platforms:**
  - ClassPlus (DRM-protected videos)
  - Media CDN URLs
  - MPD manifest files

- **Process:**
  ```
  Download → Decrypt (mp4decrypt) → Merge (ffmpeg) → Upload
  ```

- **Supported Quality:**
  - Up to 720p (configurable)
  - Auto-selects best available quality
  - Separate video + audio streams

### **2. Batch Processing**
- Upload multiple videos from single txt file
- Progress tracking for each video
- Auto-retry on failures
- Clean error handling

### **3. Smart Features**
- **Auto Thumbnail Generation:** Extracts from video
- **Custom Naming:** Uses names from txt file
- **File Size Detection:** Shows progress with size/speed/ETA
- **Auto Cleanup:** Deletes temp files after upload
- **Admin Authorization:** Only authorized users can use

### **4. Download Methods**
- **yt-dlp:** Primary downloader
- **aria2c:** Fast parallel downloads
- **Fallback:** Direct requests if others fail

### **5. File Management**
- Organized downloads folder structure
- Session-based file storage
- Auto-delete after successful upload
- Maintains original file names

---

## 📊 **Technical Capabilities**

### **Supported Video Formats:**
- MP4 (DRM-encrypted)
- M4A (Audio)
- WebM
- MPD (DASH manifests)

### **Video Processing:**
- **Decryption:** Widevine DRM (via mp4decrypt)
- **Merging:** Video + Audio mux (via ffmpeg)
- **Thumbnails:** Auto-extract at 00:00:01
- **Quality:** Configurable (default: 720p)

### **Database Features:**
- **MongoDB Integration:** User management
- **Authorization System:** Owner + Admins + Whitelisted users
- **Session Management:** Persistent login sessions
- **Log Channel:** Activity tracking

---

## 🔐 **Authorization System**

### **User Levels:**

1. **Owner (OWNER_ID)**
   - Full bot control
   - Can use all commands
   - Can add/remove admins
   - Cannot be removed

2. **Admins (ADMINS list)**
   - Can use all commands
   - Can manage users
   - Can set log channels
   - Can view logs

3. **Authorized Users**
   - Can use `/start`, `/drm`, `/id`
   - Cannot access admin commands
   - Added via database

4. **Unauthorized Users**
   - Can only use `/start` and `/id`
   - Cannot download videos
   - Get "Access Denied" message

### **Admin Check:**
```python
if db.is_admin(user_id):
    # Admin-only commands
```

---

## 📝 **TXT File Format for `/drm`**

### **Correct Format:**
```
Video 1 Introduction: https://media-cdn.classplusapp.com/drm/wv/abc123/video.mpd
Chapter 2 Tutorial: https://media-cdn.classplusapp.com/drm/wv/xyz456/video.mpd
Lesson 3 Advanced: https://media-cdn.classplusapp.com/drm/wv/def789/video.mpd
```

### **Format Rules:**
- One video per line
- Format: `Name: URL`
- Name can contain spaces
- URL must be complete MPD link
- Empty lines are ignored

---

## 🚀 **Usage Examples**

### **Example 1: Download Single DRM Video**
```
User: /drm
Bot: Send me your text file...

User: [uploads file.txt]
Content:
  Introduction Video: https://media-cdn.class...mpd

Bot: 
  ⬇️ Downloading: Introduction Video
  🔓 Decrypting...
  🎬 Merging video + audio...
  📤 Uploading...
  ✅ Done!
```

### **Example 2: Batch Download**
```
User: /drm
Bot: Send me txt file...

User: [uploads course.txt with 10 videos]

Bot:
  Processing 1/10: Video 1 ✅
  Processing 2/10: Video 2 ✅
  Processing 3/10: Video 3 ✅
  ...
  All done! 🎉
```

### **Example 3: Admin Setup**
```
Admin: /setlog -1001234567890
Bot: ✅ Log channel set!

Admin: /getlog
Bot: Current log channel: -1001234567890

[Now all bot activities logged to channel]
```

---

## ⚙️ **Configuration**

### **Environment Variables:**
```env
# Required
API_ID=34439627
API_HASH=e5c7efb57949e742889aa96bf64c4552
BOT_TOKEN=8517402286:AAGXi5xBwzv2u49lbW-oKWAlAfrE3Wx3Ov8

# MongoDB
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/
DATABASE_NAME=classplus_bot

# Authorization
OWNER_ID=7208112327
ADMINS=7208112327

# Optional
LOG_CHANNEL_ID=0
DUMP_CHANNEL_ID=0
```

### **Customization:**
- **Download Quality:** Edit line in main.py
  ```python
  -f "bv[height<=720]+ba/b"  # Change 720 to 480, 1080, etc.
  ```

- **File Naming:** Modify in DRM handler
- **Progress Format:** Edit progress_bar function
- **Thumbnail Position:** Change ffmpeg timing

---

## 🎨 **Bot Capabilities Summary**

✅ **Download:** ClassPlus DRM videos, regular videos  
✅ **Decrypt:** Widevine DRM decryption  
✅ **Process:** Video/audio merging, thumbnail extraction  
✅ **Upload:** Direct to Telegram with progress  
✅ **Manage:** User authorization, admin controls  
✅ **Track:** Logging to channel, error handling  
✅ **Batch:** Multiple videos from single file  
✅ **Smart:** Auto-cleanup, retry logic, fallbacks  

---

## 📞 **Support & Issues**

**Common Issues:**
1. **"Access Denied"** → Add user to authorized list in MongoDB
2. **"Decryption failed"** → Check if mp4decrypt is in PATH
3. **"Merge failed"** → Ensure ffmpeg is installed
4. **"Download failed"** → Check URL validity or network

**Bot Status Check:**
```
If bot responds to /start → ✅ Running
If DRM works → ✅ All tools installed
If admin commands work → ✅ Database connected
```

---

**Bot full feature-rich hai aur production-ready! 🚀**
