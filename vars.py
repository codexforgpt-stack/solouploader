import os
from os import environ

# API Configuration (From Extractor Bot)
API_ID = int(os.environ.get("API_ID", "34439627"))  # Added from extractor bot
API_HASH = os.environ.get("API_HASH", "e5c7efb57949e742889aa96bf64c4552")  # Added from extractor bot
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8241066268:AAFxKhfnk35j4cij-zU-hxJYo6VJB0jVlmU")  # Uploader bot token

CREDIT = os.environ.get("CREDIT", "𝐒𝐨𝐥𝐨 𝐁𝐞𝐚𝐬𝐭")
# MongoDB Configuration (From Extractor Bot)
DATABASE_NAME = os.environ.get("DATABASE_NAME", "classplus_bot")  # Updated from extractor bot
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://rajaualkhan33729_db_user:hlYTpjnHZzGDljKX@cluster0.vylyp51.mongodb.net/?appName=Cluster0")  # Updated from extractor bot
MONGO_URL = DATABASE_URL  # For auth system

# Owner and Admin Configuration (From Extractor Bot)
OWNER_ID = int(os.environ.get("OWNER_ID", "7208112327"))  # Super Admin from extractor bot
ADMINS = [int(x) for x in os.environ.get("ADMINS", "8349955493").split()]  # Default to owner ID

# Channel Configuration (From Extractor Bot)
PREMIUM_CHANNEL = "-1003224108968"  # Set if needed
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", "-1003527673593"))  # Log channel from extractor bot (set to 0 if not used)
DUMP_CHANNEL_ID = int(os.environ.get("DUMP_CHANNEL_ID", "-1003642795989"))  # Dump channel from extractor bot (set to 0 if not used)

# Thumbnail Configuration
THUMBNAILS = list(map(str, os.environ.get("THUMBNAILS", "").split())) # Image Link For Default Thumbnail 

# Web Server Configuration
WEB_SERVER = os.environ.get("WEB_SERVER", "False").lower() == "true"
WEBHOOK = True  # Don't change this
PORT = int(os.environ.get("PORT", 8000))

# Message Formats
AUTH_MESSAGES = {
    "subscription_active": """<b>🎉 Subscription Activated!</b>

<blockquote>Your subscription has been activated and will expire on {expiry_date}.
You can now use the bot!</blockquote>\n\n Type /start to start uploading """,

    "subscription_expired": """<b>⚠️ Your Subscription Has Ended</b>

<blockquote>Your access to the bot has been revoked as your subscription period has expired.
Please contact the admin to renew your subscription.</blockquote>""",

    "user_added": """<b>✅ User Added Successfully!</b>

<blockquote>👤 Name: {name}
🆔 User ID: {user_id}
📅 Expiry: {expiry_date}</blockquote>""",

    "user_removed": """<b>✅ User Removed Successfully!</b>

<blockquote>User ID {user_id} has been removed from authorized users.</blockquote>""",

    "access_denied": """<b>⚠️ Access Denied!</b>

<blockquote>You are not authorized to use this bot.
Please contact the admin to get access.</blockquote>""",

    "not_admin": "⚠️ You are not authorized to use this command!",
    
    "invalid_format": """❌ <b>Invalid Format!</b>

<blockquote>Use format: {format}</blockquote>"""
}

















