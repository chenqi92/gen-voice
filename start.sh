#!/bin/bash

# Kitten TTS Web Application Startup Script

set -e

echo "🐱 Kitten TTS Web Application Startup"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Install Kitten TTS
echo "🐱 Installing Kitten TTS..."
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl

# Test installation
echo "🧪 Testing installation..."
python3 test_installation.py

# Start the application
echo "🚀 Starting Kitten TTS Web Application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python3 app.py
