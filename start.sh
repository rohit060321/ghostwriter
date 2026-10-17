#!/usr/bin/env bash
set -e

# Internal port for FastAPI backend
FASTAPI_PORT=8000

# Public port assigned by Render (defaults to 10000)
PORT="${PORT:-10000}"

echo "Starting FastAPI backend on port $FASTAPI_PORT..."
uvicorn main:app --host 127.0.0.1 --port "$FASTAPI_PORT" &
FASTAPI_PID=$!

# Ensure FastAPI process terminates when script exits
trap "kill -TERM $FASTAPI_PID 2>/dev/null || true" EXIT

# Wait for FastAPI backend to become ready
echo "Waiting for FastAPI to initialize..."
for i in $(seq 1 30); do
  if python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:$FASTAPI_PORT/')" 2>/dev/null; then
    echo "FastAPI is up and ready!"
    break
  fi
  sleep 1
done

# Point Streamlit to the local FastAPI instance
export GHOSTWRITER_API_URL="http://127.0.0.1:$FASTAPI_PORT"

echo "Starting Streamlit frontend on port $PORT..."
streamlit run app.py \
  --server.port "$PORT" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.serverAddress 0.0.0.0 \
  --server.enableCORS false \
  --server.enableXsrfProtection false
