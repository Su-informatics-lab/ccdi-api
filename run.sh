#!/bin/bash

# CCDI API Start Script
# This script starts the CCDI FastAPI server using uv

echo "Starting CCDI Data Federation API server..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
