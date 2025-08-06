@echo off
setlocal enabledelayedexpansion

echo 🐱 Kitten TTS Web Application Startup
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt

REM Install Kitten TTS
echo 🐱 Installing Kitten TTS...
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl

REM Test installation
echo 🧪 Testing installation...
python test_installation.py
if errorlevel 1 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)

REM Start the application
echo 🚀 Starting Kitten TTS Web Application...
echo 📱 Open your browser and go to: http://localhost:5000
echo ⏹️  Press Ctrl+C to stop the server
echo.

python app.py

pause
