#!/bin/bash

# 1. Start FastAPI in the background on port 8000
echo "Starting FastAPI backend..."
PYTHONPATH=. uvicorn src.app.api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Give the API a few seconds to wake up
sleep 5

# 2. Start Chainlit in the foreground on Render's required port
echo "Starting Chainlit UI..."
PYTHONPATH=. chainlit run src/app/chainlit_app.py --host 0.0.0.0 --port ${PORT:-8000}

# 3. When Chainlit closes, kill the background API cleanly
echo "Shutting down API..."
kill $API_PID