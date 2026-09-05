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

# Pre-download the ONNX model to prevent runtime OOM crashes on Render
RUN python -c "from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2; ONNXMiniLM_L6_V2()"

# Copy the rest of the application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Cloud Run provides the PORT env var (usually 8080)
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "8080"]