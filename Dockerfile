# Use an official Python image
FROM python:3.12-slim

# Install FFmpeg (for audio streaming)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and bot code
COPY requirements.txt .
COPY bot.py .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]

