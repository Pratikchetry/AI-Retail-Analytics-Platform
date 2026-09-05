# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies for PostgreSQL and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Manually download and extract the ONNX model to the exact cache path ChromaDB expects
# This prevents the 79MB download/extraction memory spike at runtime (fixes Render OOM crash)
RUN mkdir -p /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2/ && \
    curl -L https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz \
    -o /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz && \
    tar -xzf /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz \
    -C /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2/ && \
    rm /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz

# Copy the rest of the application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Cloud Run provides the PORT env var (usually 8080)
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "8080"]