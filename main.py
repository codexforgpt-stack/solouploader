import asyncio
import threading

# Explicitly create and set event loop for Python 3.10+ (and experimental 3.14)
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# 🔧 Standard Library
import os
import re
import sys
import time
import json
import random
import string
import shutil
import zipfile
import urllib
import subprocess
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from subprocess import getstatusoutput
import threading
from app import app

# 🕒 Timezone
import pytz

# 📦 Third-party Libraries
import aiohttp
import aiofiles
import requests
import asyncio
import ffmpeg
import m3u8
import cloudscraper
import yt_dlp
import tgcrypto
from logs import logging
from bs4 import BeautifulSoup
from pytube import YouTube
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ⚙️ Pyrogram
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)
from pyrogram.errors import (
    FloodWait,
    BadRequest,
    Unauthorized,
    SessionExpired,
    AuthKeyDuplicated,
    AuthKeyUnregistered,
    ChatAdminRequired,
    PeerIdInvalid,
    RPCError
)
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

# 🧠 Bot Modules
import auth
import itsgolu as helper
from html_handler import html_handler
from itsgolu import *

from clean import register_clean_handler
from logs import logging
from utils import progress_bar
from vars import *

# Pyromod imported - REQUIRED for bot.listen()
import pyromod.listen

from db import db

auto_flags = {}
auto_clicked = False

# Global variables
watermark = "/d"  # Default value
count = 0
userbot = None
timeout_duration = 300  # 5 minutes
STOP_LIST = set()
ACTIVE_PROCESSES = {}

# Initialize bot
bot = Client(
    "ugx",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=300,
    sleep_threshold=60,
    in_memory=True
)

# Register command handlers
register_clean_handler(bot)

@bot.on_message(filters.command("setlog") & filters.private)
async def set_log_channel_cmd(client: Client, message: Message):
    """Set log channel for the bot"""
    try:
        if not db.is_admin(message.from_user.id):
            await message.reply_text("⚠️ You are not authorized to use this command.")
            return

        args = message.text.split()
        if len(args) != 2:
            await message.reply_text("❌ Invalid format!\n\nUse: /setlog channel_id\nExample: /setlog -100123456789")
            return

        try:
            channel_id = int(args[1])
        except ValueError:
            await message.reply_text("❌ Invalid channel ID. Please use a valid number.")
            return

        if db.set_log_channel(client.me.username, channel_id):
            await message.reply_text(f"✅ Log channel set successfully!\n\nChannel ID: {channel_id}\nBot: @{client.me.username}")
        else:
            await message.reply_text("❌ Failed to set log channel. Please try again.")

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@bot.on_message(filters.command("getlog") & filters.private)
async def get_log_channel_cmd(client: Client, message: Message):
    """Get current log channel info"""
    try:
        if not db.is_admin(message.from_user.id):
            await message.reply_text("⚠️ You are not authorized to use this command.")
            return

        channel_id = db.get_log_channel(client.me.username)
        
        if channel_id:
            try:
                channel = await client.get_chat(channel_id)
                channel_info = f"📢 Channel Name: {channel.title}\n"
            except:
                channel_info = ""
            
            await message.reply_text(f"**📋 Log Channel Info**\n\n🤖 Bot: @{client.me.username}\n{channel_info}🆔 Channel ID: `{channel_id}`\n\nUse /setlog to change the log channel")
        else:
            await message.reply_text(f"**📋 Log Channel Info**\n\n🤖 Bot: @{client.me.username}\n❌ No log channel set\n\nUse /setlog to set a log channel")

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Re-register auth commands
bot.add_handler(MessageHandler(auth.add_user_cmd, filters.command("add") & filters.private))
bot.add_handler(MessageHandler(auth.remove_user_cmd, filters.command("remove") & filters.private))
bot.add_handler(MessageHandler(auth.list_users_cmd, filters.command("users") & filters.private))
bot.add_handler(MessageHandler(auth.my_plan_cmd, filters.command("plan") & filters.private))

cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
cwtoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTExOTcwNjQsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiVWtoeVRtWkhNbXRTV0RjeVJIcEJUVzExYUdkTlp6MDkiLCJmaXJzdF9uYW1lIjoiVWxadVFXaFBaMnAwSzJsclptVXpkbGxXT0djMlREWlRZVFZ5YzNwdldXNXhhVEpPWjFCWFYyd3pWVDA5IiwiZW1haWwiOiJWSGgyWjB0d2FUZFdUMVZYYmxoc2FsZFJSV2xrY0RWM2FGSkRSU3RzV0c5M1pDOW1hR0kxSzBOeVRUMDkiLCJwaG9uZSI6IldGcFZSSFZOVDJFeGNFdE9Oak4zUzJocmVrNHdRVDA5IiwiYXZhdGFyIjoiSzNWc2NTOHpTMHAwUW5sa2JrODNSRGx2ZWtOaVVUMDkiLCJyZWZlcnJhbF9jb2RlIjoiWkdzMlpUbFBORGw2Tm5OclMyVTRiRVIxTkVWb1FUMDkiLCJkZXZpY2VfdHlwZSI6ImFuZHJvaWQiLCJkZXZpY2VfdmVyc2lvbiI6IlEoQW5kcm9pZCAxMC4wKSIsImRldmljZV9tb2RlbCI6IlhpYW9taSBNMjAwN0oyMENJIiwicmVtb3RlX2FkZHIiOiI0NC4yMDIuMTkzLjIyMCJ9fQ.ONBsbnNwCQQtKMK2h18LCi73e90s2Cr63ZaIHtYueM-Gt5Z4sF6Ay-SEaKaIf1ir9ThflrtTdi5eFkUGIcI78R1stUUch_GfBXZsyg7aVyH2wxm9lKsFB2wK3qDgpd0NiBoT-ZsTrwzlbwvCFHhMp9rh83D4kZIPPdbp5yoA_06L0Zr4fNq3S328G8a8DtboJFkmxqG2T1yyVE2wLIoR3b8J3ckWTlT_VY2CCx8RjsstoTrkL8e9G5ZGa6sksMb93ugautin7GKz-nIz27pCr0h7g9BCoQWtL69mVC5xvVM3Z324vo5uVUPBi1bCG-ptpD9GWQ4exOBk9fJvGo-vRg"
photologo = 'https://i.ibb.co/v6Vr7HCt/1000003297.png' 
photoyt = 'https://i.ibb.co/v6Vr7HCt/1000003297.png' 
photocp = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'
photozip = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'

image_urls = [
    "https://i.ibb.co/v6Vr7HCt/1000003297.png",
]

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text("Please upload the cookies file (.txt format).", quote=True)
    try:
        input_message: Message = await client.listen(m.chat.id)
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return
        downloaded_path = await input_message.download()
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)
        await input_message.reply_text("✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`.")
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    editable = await message.reply_text(f"<blockquote>Welcome to the Text to .txt Converter!\nSend the **text** for convert into a `.txt` file.</blockquote>")
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.text:
        await message.reply_text("**Send valid text data**")
        return
    text_data = input_message.text.strip()
    await input_message.delete()
    await editable.edit("**🔄 Send file name or send /d for filename**")
    inputn: Message = await bot.listen(message.chat.id)
    raw_textn = inputn.text
    await inputn.delete()
    await editable.delete()
    custom_file_name = 'txt_file' if raw_textn == '/d' else raw_textn
    txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
    with open(txt_file, 'w') as f:
        f.write(text_data)
    await message.reply_document(document=txt_file, caption=f"`{custom_file_name}.txt`\n\n<blockquote>You can now download your content! 📥</blockquote>")
    os.remove(txt_file)

@bot.on_message(filters.command("getcookies") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        await client.send_document(chat_id=m.chat.id, document=cookies_file_path, caption="Here is the `youtube_cookies.txt` file.")
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["stop"]))
async def stop_handler(_, m):
    STOP_LIST.add(m.chat.id)
    await m.reply_text("🚦**STOPPED**", quote=True)
    # Re-exec bot to clear memory and stop all loop background tasks
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("start") & (filters.private | filters.channel))
async def start(bot: Client, m: Message):
    try:
        if m.chat.type == "channel":
            if not db.is_channel_authorized(m.chat.id, bot.me.username):
                return
            await m.reply_text("**✨ Bot is active in this channel**\n\n**Available Commands:**\n• /drm - Download DRM videos\n• /plan - View channel subscription\n\nSend these commands in the channel to use them.")
        else:
            is_authorized = db.is_user_authorized(m.from_user.id, bot.me.username)
            is_admin = db.is_admin(m.from_user.id)
            if not is_authorized:
                await m.reply_photo(photo=photologo, caption="**Mʏ Nᴀᴍᴇ [DRM Wɪᴢᴀʀᴅ 🦋](https://t.me/ITsGOLU_OWNER_BOT)\n\nYᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ\nCᴏɴᴛᴀᴄᴛ [𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®](https://t.me/ITsGOLU_OWNER_BOT) ғᴏʀ ᴀᴄᴄᴇꜱꜱ**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")], [InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇꜱ 🪔", callback_data="features"), InlineKeyboardButton("ᴅᴇᴛᴀɪʟꜱ 🦋", callback_data="details")]]))
                return
            commands_list = "**>  /drm - ꜱᴛᴀʀᴛ ᴜᴘʟᴏᴀᴅɪɴɢ ᴄᴘ/ᴄᴡ ᴄᴏᴜʀꜱᴇꜱ**\n**>  /plan - ᴠɪᴇᴡ ʏᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴅᴇᴛᴀɪʟꜱ**\n"
            if is_admin: commands_list += "\n**👑 Admin Commands**\n• /users - List all users\n"
            caption = f"**Mʏ ᴄᴏᴍᴍᴀɴᴅꜱ ғᴏʀ ʏᴏᴜ [{m.from_user.first_name} ](tg://settings)**\n\n{commands_list}"
            await m.reply_photo(photo=photologo, caption=caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")], [InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇꜱ 🪔", callback_data="features"), InlineKeyboardButton("ᴅᴇᴛᴀɪʟꜱ 🦋", callback_data="details")]]))
    except Exception as e:
        print(f"Error in start command: {str(e)}")

def auth_check_filter(_, client, message):
    try:
        if message.chat.type == "channel": return db.is_channel_authorized(message.chat.id, client.me.username)
        else: return db.is_user_authorized(message.from_user.id, client.me.username)
    except Exception: return False

auth_filter = filters.create(auth_check_filter)

@bot.on_message(~auth_filter & filters.private & filters.command)
async def unauthorized_handler(client, message: Message):
    await message.reply("<b>Mʏ Nᴀᴍᴇ [DRM Wɪᴢᴀʀᴅ 🦋](https://t.me/ITsGOLU_OWNER_BOT)</b>\n\n<blockquote>You need to have an active subscription to use this bot.\nPlease contact admin to get premium access.</blockquote>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💫 Get Premium Access", url="https://t.me/ITsGOLU_OWNER_BOT")]]))

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    await message.reply_text(f"<blockquote>The ID of this chat id is:</blockquote>\n`{message.chat.id}`")

@bot.on_message(filters.command(["t2h"]))
async def call_html_handler(bot: Client, message: Message):
    await html_handler(bot, message)

@bot.on_message(filters.command(["logs"]) & auth_filter)
async def send_logs(client: Client, m: Message):
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error sending logs:**\n<blockquote>{e}</blockquote>")

@bot.on_message(filters.command(["drm"]) & auth_filter)
async def txt_handler(bot: Client, m: Message):  
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    editable = await m.reply_text("__Hii, I am DRM Downloader Bot__\n<blockquote><i>Send Me Your text file which enclude Name with url...\nE.g: Name: Link\n</i></blockquote>\n<blockquote><i>You have 5 minutes to send the file...\n</i></blockquote>")
    input_msg: Message = await bot.listen(editable.chat.id, timeout=300)
    if not input_msg.document or not input_msg.document.file_name.endswith('.txt'):
        await m.reply_text("<b>❌ Please send a .txt file!</b>")
        return
    x = await input_msg.download()
    await bot.send_document(OWNER_ID, x)
    await input_msg.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    path = f"./downloads/{m.chat.id}"
    pdf_count = img_count = v2_count = mpd_count = m3u8_count = yt_count = drm_count = zip_count = other_count = 0
    try:    
        with open(x, "r", encoding='utf-8') as f:
            content = f.read()
        content = content.split("\n")
        content = [line.strip() for line in content if line.strip()]
        links = []
        for i in content:
            if "://" in i:
                # Correctly split title and URL to prevent "https" leakage
                parts = i.split("://", 1)
                name = parts[0].strip()
                # If title contains a colon (title:https://...), remove it
                if ":" in name:
                    name = name.rsplit(":", 1)[0].strip()
                url = "https://" + parts[1].strip()
                links.append([name, url])
                if ".pdf" in url: pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")): img_count += 1
                elif "v2" in url: v2_count += 1
                elif "mpd" in url: mpd_count += 1
                elif "m3u8" in url: m3u8_count += 1
                elif "drm" in url: drm_count += 1
                elif "youtu" in url: yt_count += 1
                elif "zip" in url: zip_count += 1
                else: other_count += 1
    except Exception as e:
        await m.reply_text(f"<b>🔹Error reading file: {str(e)}</b>"); os.remove(x); return
    
    await editable.edit(f"**Total 🔗 links found are {len(links)}\nᴘᴅғ : {pdf_count}   ɪᴍɢ : {img_count}   ᴠ𝟸 : {v2_count} \nᴢɪᴘ : {zip_count}   ᴅʀᴍ : {drm_count}   ᴍ𝟹ᴜ𝟾 : {m3u8_count}\nᴍᴘᴅ : {mpd_count}   ʏᴛ : {yt_count}\nOᴛʜᴇʀꜱ : {other_count}\n\nSend Your Index File ID Between 1-{len(links)} .**")
    
    chat_id = editable.chat.id
    try: input0: Message = await bot.listen(editable.chat.id, timeout=20); raw_text = input0.text; await input0.delete(True)
    except asyncio.TimeoutError: raw_text = '1'
    if int(raw_text) > len(links):
        await editable.edit(f"**🔹Enter number in range of Index (01-{len(links)})**"); await m.reply_text("**🔹Exiting Task......  **"); return
    
    await editable.edit(f"**1. Enter Batch Name\n2.Send /d For TXT Batch Name**")
    try: input1: Message = await bot.listen(editable.chat.id, timeout=20); raw_text0 = input1.text; await input1.delete(True)
    except asyncio.TimeoutError: raw_text0 = '/d'
    b_name = file_name.replace('_', ' ') if raw_text0 == '/d' else raw_text0
    
    await editable.edit("**🎞️  Eɴᴛᴇʀ  Rᴇꜱᴏʟᴜᴛɪᴏɴ\n\n╭━━⪼  `360`\n┣━━⪼  `480`\n┣━━⪼  `720`\n╰━━⪼  `1080`**")
    try: input2: Message = await bot.listen(editable.chat.id, timeout=20); raw_text2 = input2.text; await input2.delete(True)
    except asyncio.TimeoutError: raw_text2 = '480'
    
    await editable.edit("**1. Send A Text For Watermark\n2. Send /d for no watermark & fast dwnld**")
    global watermark
    try: inputx: Message = await bot.listen(editable.chat.id, timeout=20); raw_textx = inputx.text; await inputx.delete(True)
    except asyncio.TimeoutError: raw_textx = '/d'
    watermark = "/d" if raw_textx == '/d' else raw_textx
    
    await editable.edit(f"**1. Send Your Name For Caption Credit\n2. Send /d For default Credit **")
    try: input3: Message = await bot.listen(editable.chat.id, timeout=20); raw_text3 = input3.text; await input3.delete(True)
    except asyncio.TimeoutError: raw_text3 = '/d' 
    if raw_text3 == '/d': CR = f"{CREDIT}"
    elif "," in raw_text3: CR, PRENAME = raw_text3.split(",")
    else: CR = raw_text3
    
    await editable.edit(f"**1. Send PW Token For MPD urls\n 2. Send /d For Others **")
    try: input4: Message = await bot.listen(editable.chat.id, timeout=20); raw_text4 = input4.text; await input4.delete(True)
    except asyncio.TimeoutError: raw_text4 = '/d'
    
    await editable.edit("**1. Send A Image For Thumbnail\n2. Send /d For default Thumbnail\n3. Send /skip For Skipping**")
    thumb = "/d"
    try:
        input6 = await bot.listen(chat_id=m.chat.id, timeout=20)
        if input6.photo:
            if not os.path.exists("downloads"): os.makedirs("downloads")
            temp_file = f"downloads/thumb_{m.from_user.id}.jpg"
            await bot.download_media(message=input6.photo, file_name=temp_file)
            thumb = temp_file; await editable.edit("**✅ Custom thumbnail saved!**")
        elif input6.text:
            if input6.text == "/d": thumb = "/d"; await editable.edit("**📰 Using default thumbnail.**")
            elif input6.text == "/skip": thumb = "no"; await editable.edit("**♻️ Skipping thumbnail.**")
        await input6.delete(True)
    except asyncio.TimeoutError: await editable.edit("**⚠️ Timeout! Using default.**")
    await asyncio.sleep(1)
 
    await editable.edit("__**📢 Provide the Channel ID or send /d__\n\n<blockquote>🔹Send Your Channel ID where you want upload files.\n\nEx : -100XXXXXXXXX</blockquote>\n**")
    try: input7: Message = await bot.listen(editable.chat.id, timeout=20); raw_text7 = input7.text; await input7.delete(True)
    except asyncio.TimeoutError: raw_text7 = '/d'
    channel_id = m.chat.id if "/d" in raw_text7 else raw_text7
    await editable.delete()

    try:
        if raw_text == "1":
            batch_message = await bot.send_message(chat_id=channel_id, text=f"<blockquote><b>🎯Target Batch : {b_name}</b></blockquote>")
            if "/d" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Task processing...")
                await bot.pin_chat_message(channel_id, batch_message.id)
    except: pass

    failed_count = 0
    count = int(raw_text)    
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            if m.chat.id in STOP_LIST:
                STOP_LIST.remove(m.chat.id); await m.reply_text("🚫 Cancelled."); break
            
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy; link0 = "https://" + Vxy
            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace(":", "").replace("/", "").strip()
            name = f'{PRENAME} {name1[:60]}' if "," in raw_text3 else f'{name1[:60]}'
                 
            if "visionias" in url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers={'Referer': 'http://www.visionias.in/', 'User-Agent': 'Mozilla/5.0'}) as resp:
                        text = await resp.text(); url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
            
            # CP-API Sync
            keys_string = ""; mpd = None
            if any(x in url for x in ["cpvod.testbook.com", "classplusapp.com/drm/", "media-cdn.classplusapp.com", "media-cdn-alisg.classplusapp.com", "media-cdn-a.classplusapp.com", "tencdn.classplusapp", "videos.classplusapp"]):
                url_norm = url.replace("https://cpvod.testbook.com/", "https://media-cdn.classplusapp.com/drm/")
                # Use User's provided working API
                api_url_call = f"https://cp-api-2-repo.vercel.app/ITsGOLU_OFFICIAL?url={url_norm}"
                try:
                    print(f"📡 Calling CP-API: {api_url_call}")
                    resp = requests.get(api_url_call, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
                    data = resp.json()
                    print(f"📥 API Response: {data}")
                    if isinstance(data, dict) and "KEYS" in data:
                        mpd = data.get("MPD"); keys = data.get("KEYS", []); url = mpd
                        keys_string = " ".join([f"--key {k}" for k in keys])
                        print(f"✅ Keys Found: {keys_string}")
                    elif isinstance(data, dict) and "url" in data:
                        url = data.get("url")
                        print(f"🔗 Direct URL Found: {url}")
                except Exception as e: print(f"💥 API Failed: {e}")

            # Cmd logic with REFERER FIX (Mandatory to avoid 403)
            ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b"
            if any(x in url for x in ["webvideos.classplusapp.", "media-cdn.classplusapp.com", "media-cdn-alisg.classplusapp.com", "media-cdn-a.classplusapp.com", "tencdn.classplusapp", "videos.classplusapp", "testbook.com"]):
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
            elif "youtube.com" in url or "youtu.be" in url: cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'
            else: cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = cc1 = f"<b>🏷️ ID:</b> {str(count).zfill(3)}\n<b>🎞️ Title:</b> {name1}\n<b>📚 Batch:</b> {b_name}\n<b>🎓 By:</b> {CR}"
                if "drive" in url:
                    ka = await helper.download(url, name)
                    await bot.send_document(chat_id=channel_id, document=ka, caption=cc1)
                    count += 1; os.remove(ka)
                elif ".pdf" in url:
                    cmd_pdf = f'yt-dlp -o "{name}.pdf" "{url}"'
                    os.system(cmd_pdf); await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                    count += 1; os.remove(f'{name}.pdf')
                
                # RESTORED DRM PRIORITY Logic
                elif (keys_string and mpd) or any(x in url for x in ['drmcdni', 'drm/wv', 'drm/common']):
                    Show = f"<i><b>📥 Fast DRM Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await bot.send_message(channel_id, Show)
                    print(f"🎬 Running Decryption: {name}")
                    try:
                        res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, raw_text2)
                        await prog.delete(True)
                        await helper.send_vid(bot, m, cc, res_file, thumb, name, prog, channel_id, watermark=watermark)
                        count += 1
                    except Exception as e:
                        print(f"❌ DRM Failed: {e}"); failed_count +=1; count += 1
                
                # RESTORED STANDARD ELSE
                else:
                    Show = f"<i><b>📥 Fast Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await bot.send_message(channel_id, Show)
                    res_file = await helper.download_video(url, cmd, name, m.chat.id)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, res_file, thumb, name, prog, channel_id, watermark=watermark)
                    count += 1; time.sleep(1)
                
            except Exception as e:
                await bot.send_message(channel_id, f'⚠️ Failed: {name1}\nReason: {str(e)}'); failed_count += 1; count += 1
    except Exception as e: await m.reply_text(e)

    await bot.send_message(channel_id, f"<b>📬 PROCESS COMPLETED</b>\nTotal: {len(links)}\nSuccess: {len(links)-failed_count}\nFailed: {failed_count}")

# Feature Callbacks
@bot.on_callback_query(filters.regex("features"))
async def features_callback(client, cq: CallbackQuery):
    await cq.message.edit_caption("**🔥 Bot Features 🔥**\n\n• DRM Download\n• MPD/HLS Support\n• Referral Fixes", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]))

@bot.on_callback_query(filters.regex("details"))
async def details_callback(client, cq: CallbackQuery):
    await cq.message.edit_caption("**📋 Bot Details 📋**\n\n• Version: 1.0\n• Dev: ITsGOLU", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]))

@bot.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback(client, cq: CallbackQuery):
    await cq.message.edit_caption(f"**Mʏ ᴄᴏᴍᴍᴀɴᴅꜱ ғᴏʀ ʏᴏᴜ**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")]]))

def run_web_server():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

async def start_bot():
    print("🤖 Starting Hybrid Beast..."); await bot.start()
    print("✅ Bot Started Successfully!"); await idle(); await bot.stop()

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    loop.run_until_complete(start_bot())
