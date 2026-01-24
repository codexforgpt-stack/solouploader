FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    aria2 \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Bento4 (mp4decrypt)
RUN wget -q https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip && \
    unzip -q Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip && \
    cp Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt /usr/local/bin/ && \
    chmod +x /usr/local/bin/mp4decrypt && \
    rm -rf Bento4-SDK-1-6-0-641.x86_64-unknown-linux*

# Verify installations
RUN ffmpeg -version && \
    aria2c --version && \
    mp4decrypt 2>&1 | head -1

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all bot files
COPY . .

# Create downloads directory
RUN mkdir -p downloads

# Expose port (Koyeb needs this)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('ugx.session') else 1)"

# Run the bot
CMD ["python", "main.py"]
