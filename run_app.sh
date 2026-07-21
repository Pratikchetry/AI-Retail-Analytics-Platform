#!/bin/bash

# 1. Start FastAPI in the background (no auto-reload to keep it fast)
echo "Starting FastAPI backend on port 8000..."
PYTHONPATH=. uvicorn src.app.api:app --port 8000 &
API_PID=$!

# Give the API a few seconds to wake up
sleep 5

# 2. Start Chainlit in the foreground
echo "Starting Chainlit UI on port 8001..."
PYTHONPATH=. chainlit run src/app/chainlit_app.py --port 8001

# 3. When Chainlit closes (Ctrl+C), kill the background API cleanly
echo "Shutting down API..."
kill $API_PID