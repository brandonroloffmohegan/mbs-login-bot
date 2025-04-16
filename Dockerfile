# Use an official Python runtime as a base image.
FROM python:3.11-slim

# Install system dependencies required by Playwright's browsers.
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates fonts-liberation libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libgbm1 libgtk-3-0 libnspr4 libnss3 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container.
WORKDIR /app

# Copy the dependency file and install Python packages.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your rest of the code.
COPY . .

# Install Playwright browsers using the Python CLI.
RUN python -m playwright install --with-deps

# Expose the port that your app will run on.
ENV PORT=10000
EXPOSE 10000

# Define the command to run your app.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
