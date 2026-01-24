#!/bin/bash

echo "🚀 Starting Solo Beast Bot VPS Setup..."

# Update and install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip ffmpeg aria2 wget unzip curl git

# Install Bento4 (mp4decrypt)
echo "📦 Installing mp4decrypt..."
wget -q https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip
unzip -q Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip
sudo cp Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt /usr/local/bin/
sudo chmod +x /usr/local/bin/mp4decrypt
rm -rf Bento4-SDK-1-6-0-641.x86_64-unknown-linux*

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install --no-cache-dir -r requirements.txt

# Create downloads directory
mkdir -p downloads

# Verification
echo "✅ Checking installations..."
ffmpeg -version | head -n 1
aria2c --version | head -n 1
mp4decrypt 2>&1 | head -n 1

echo "✨ Setup complete! Please configure your .env file and start the bot."
