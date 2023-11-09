# Use a minimal base image
FROM python:3.8-alpine as builder

# Set the working directory
WORKDIR /app

# Copy only the necessary files for installation
COPY requirements.txt .

# Install dependencies
RUN apk add --no-cache build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-base

# Copy the application code
COPY . .

# Set the timezone to UTC
ENV TZ=UTC

# Command to run the application
CMD ["python", "-u", "main.py"]
