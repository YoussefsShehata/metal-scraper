# Use a slim Python image
FROM python:3.10-slim

# Install Chromium and its driver (for headless scraping)
RUN apt-get update \
    && apt-get install -y chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Tell Docker how to start your server
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
