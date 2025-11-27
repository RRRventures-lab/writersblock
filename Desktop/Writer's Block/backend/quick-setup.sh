#!/bin/bash
set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Writer's Block - Backend Quick Setup"
echo "=========================================="
echo ""
echo "Working directory: $SCRIPT_DIR"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
  echo "✓ Virtual environment created"
else
  echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ Pip upgraded"

# Install requirements
echo ""
echo "Installing Python dependencies..."
echo "(This may take a few minutes...)"
pip install -r requirements.txt

# Create .env file
echo ""
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "✓ Created .env file"
else
  echo "✓ .env file already exists"
fi

# Create directories
echo "Creating directories..."
mkdir -p uploads/audio
mkdir -p logs
echo "✓ Directories created"

# Initialize database
echo ""
echo "Initializing database..."
python3 << 'PYTHON_SCRIPT'
from database import init_db
try:
    init_db()
    print("✓ Database initialized successfully")
except Exception as e:
    print(f"✗ Database initialization failed: {e}")
    import sys
    sys.exit(1)
PYTHON_SCRIPT

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  bash start-dev.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "API will be available at:"
echo "  http://127.0.0.1:8000"
echo "  Docs: http://127.0.0.1:8000/docs"
echo ""
