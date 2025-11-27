#!/bin/bash

# Writer's Block Backend Development Server Starter

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup.sh..."
    bash setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Set development environment
export DEBUG=true
export LOG_LEVEL=DEBUG

echo "=========================================="
echo "Writer's Block - Development Server"
echo "=========================================="
echo ""
echo "Starting backend server..."
echo "API will be available at: http://127.0.0.1:8000"
echo "Documentation at: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
