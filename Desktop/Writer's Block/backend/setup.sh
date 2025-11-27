#!/bin/bash

# Writer's Block Backend Setup Script
# This script sets up the complete backend environment

set -e

echo "=========================================="
echo "Writer's Block - Backend Setup"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create environment file
echo ""
echo "Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file (please update with your configuration)"
else
    echo ".env file already exists"
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p uploads/audio
mkdir -p logs

# Initialize database
echo ""
echo "Initializing database..."
python3 -c "from database import init_db; init_db(); print('Database initialized successfully')"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo ""
echo "Or use uvicorn directly:"
echo "  uvicorn main:app --reload"
echo ""
echo "API will be available at: http://127.0.0.1:8000"
echo "Documentation at: http://127.0.0.1:8000/docs"
