#!/bin/bash

# 1. Start FastAPI in the background on port 8000
echo "Starting FastAPI backend on port 8000..."
PYTHONPATH=. uvicorn src.app.api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Give the API a few seconds to wake up
sleep 5

# 2. Start Chainlit in the foreground
# If $PORT is set (like on Render), use it. Otherwise, use 8001 locally.
UI_PORT=${PORT:-8001}
echo "Starting Chainlit UI on port $UI_PORT..."
PYTHONPATH=. chainlit run src/app/chainlit_app.py --host 0.0.0.0 --port $UI_PORT

# 3. When Chainlit closes, kill the background API cleanly
echo "Shutting down API..."
kill $API_PID