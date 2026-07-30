# docker/Dockerfile
FROM python:3.11-slim

# System deps for psycopg2 + sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn streamlit requests

# Copy the project
COPY . .

# Default command (overridden per-service in compose)
ENV PYTHONPATH=/app
EXPOSE 8000 8001

# Run both API and UI together
CMD ["bash", "run_app.sh"]
