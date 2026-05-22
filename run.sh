#!/bin/bash

# Green Repository - FastAPI Server Runner

cd "$(dirname "$0")" || exit 1

echo "Starting Green Repository server..."
echo "Server will run on http://0.0.0.0:8000"
echo "Press Ctrl+C to stop"
echo ""

./.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
