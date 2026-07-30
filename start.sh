#!/usr/bin/env bash

set -e

echo "Starting FastAPI backend..."

python -m uvicorn backend.main:app \
    --host 127.0.0.1 \
    --port 8000 &

BACKEND_PID=$!

# Stop FastAPI when the Render service shuts down.
cleanup() {
    echo "Stopping FastAPI backend..."
    kill "$BACKEND_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

echo "Waiting for FastAPI backend..."

for attempt in $(seq 1 30); do
    if python -c "
import urllib.request
urllib.request.urlopen(
    'http://127.0.0.1:8000/health',
    timeout=2
)
" >/dev/null 2>&1; then
        echo "FastAPI backend is ready."
        break
    fi

    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "FastAPI backend stopped unexpectedly."
        wait "$BACKEND_PID"
        exit 1
    fi

    if [ "$attempt" -eq 30 ]; then
        echo "FastAPI backend failed to become ready."
        exit 1
    fi

    sleep 1
done

echo "Starting Streamlit frontend..."

exec python -m streamlit run frontend/login.py \
    --server.address 0.0.0.0 \
    --server.port "${PORT:-8501}" \
    --server.headless true
