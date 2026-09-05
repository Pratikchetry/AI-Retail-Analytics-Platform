FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and extract the ONNX model directly into the app folder during build
RUN mkdir -p /app/onnx_model && \
    curl -L https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz \
    -o /tmp/onnx.tar.gz && \
    tar -xzf /tmp/onnx.tar.gz -C /app/onnx_model && \
    rm /tmp/onnx.tar.gz

COPY . .

ENV PYTHONPATH=/app
EXPOSE 8080

CMD ["uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "8080"]