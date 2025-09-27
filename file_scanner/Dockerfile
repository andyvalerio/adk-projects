# Use the official Python image as a base
FROM python:3.13-slim

# Copy the requirements file if it exists
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for the scanner
ENV SCAN_ROOT=/data/mnt/f/tv_series/ \
    SCAN_OUTPUT=/data/root/dev/adk-projects/storage/files.json \
    SCAN_CHECKPOINT=/data/root/dev/adk-projects/storage/scanner_checkpoint.json \
    SCAN_BATCH_SIZE=1000 \
    SCAN_INTERVAL=300

# Create the data directory
RUN mkdir -p /data

# Set the entrypoint to run the scanner script
ENTRYPOINT ["python3", "scanner.py"]