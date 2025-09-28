# Use the official Python image as a base
FROM python:3.13-slim

# Copy the requirements file if it exists
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create the data directory
RUN mkdir -p /data

# Set the entrypoint to run the scanner script
ENTRYPOINT ["python3", "scanner.py"]
