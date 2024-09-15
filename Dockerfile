# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install necessary build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev musl-dev

# Copy requirements.txt and install dependencies, including Hypercorn
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src/ /app/src

# Expose the necessary port
EXPOSE 8000

# Ensure the application runs as a non-root user for security
USER 1001

# Set the entrypoint to use Hypercorn to serve the FastAPI app
CMD ["hypercorn", "src.main:app", "--bind", "0.0.0.0:8000"]
