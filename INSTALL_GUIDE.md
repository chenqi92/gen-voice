# 📦 Installation Guide

This guide will help you install and run the Kitten TTS Web Application on your system.

## 🐍 Python Installation

### Windows

1. **Download Python**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.8 or later
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify Installation**:
   ```cmd
   python --version
   # or
   py --version
   ```

### macOS

1. **Using Homebrew** (recommended):
   ```bash
   brew install python3
   ```

2. **Or download from python.org**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Download and install Python 3.8+

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Linux (CentOS/RHEL/Fedora)

```bash
# CentOS/RHEL
sudo yum install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

## 🚀 Quick Start

### Option 1: Docker (Easiest - No Python needed)

1. **Install Docker**:
   - Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Linux: Follow [Docker installation guide](https://docs.docker.com/engine/install/)

2. **Run the application**:
   ```bash
   docker run -p 5000:5000 your-username/kitten-tts-web:latest
   ```

3. **Open your browser**: http://localhost:5000

### Option 2: Automated Setup Scripts

#### Windows
```cmd
# Double-click start.bat or run in Command Prompt
start.bat
```

#### Linux/macOS
```bash
# Make executable and run
chmod +x start.sh
./start.sh
```

### Option 3: Manual Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/kitten-tts-web.git
   cd kitten-tts-web
   ```

2. **Create virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install Kitten TTS** (optional - app works in demo mode without it):
   ```bash
   pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
   ```

5. **Test installation**:
   ```bash
   python test_installation.py
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Open your browser**: http://localhost:5000

## 🔧 Troubleshooting

### Common Issues

#### "Python not found" or "Command not found"

**Windows**:
- Reinstall Python and check "Add Python to PATH"
- Try using `py` instead of `python`
- Restart Command Prompt after installation

**Linux/macOS**:
- Use `python3` instead of `python`
- Install Python using your package manager

#### "pip not found"

```bash
# Windows
python -m ensurepip --upgrade

# Linux/macOS
sudo apt install python3-pip  # Ubuntu/Debian
```

#### "Permission denied" errors

**Windows**:
- Run Command Prompt as Administrator
- Or use `--user` flag: `pip install --user -r requirements.txt`

**Linux/macOS**:
- Use `sudo` for system-wide installation
- Or use virtual environment (recommended)

#### "Module not found" errors

Make sure you're in the correct directory and virtual environment:
```bash
# Check current directory
pwd  # Linux/macOS
cd   # Windows

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Kitten TTS installation fails

The app will work in demo mode without Kitten TTS. To install it:

1. **Check internet connection**
2. **Try manual download**:
   ```bash
   wget https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
   pip install kittentts-0.1.0-py3-none-any.whl
   ```

#### Port 5000 already in use

Change the port:
```bash
# Set environment variable
export PORT=8080  # Linux/macOS
set PORT=8080     # Windows

# Or run directly
python app.py
```

Then open: http://localhost:8080

### System Requirements

**Minimum**:
- Python 3.8+
- 1GB RAM
- 1GB free disk space
- Any modern CPU (no GPU required)

**Recommended**:
- Python 3.9+
- 2GB RAM
- 2GB free disk space
- Multi-core CPU for better performance

### Demo Mode vs Full Mode

**Demo Mode** (no Kitten TTS installed):
- ✅ Full web interface
- ✅ Voice selection
- ✅ Text input
- ⚠️ Generates silent audio files
- ⚠️ No actual speech synthesis

**Full Mode** (with Kitten TTS):
- ✅ Everything from demo mode
- ✅ Real speech synthesis
- ✅ High-quality audio generation
- ✅ Multiple expressive voices

## 🐳 Docker Alternative

If you have issues with Python installation, Docker is the easiest option:

### Install Docker

1. **Windows/Mac**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. **Linux**: 
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

### Run with Docker

```bash
# Pull and run
docker run -d --name kitten-tts -p 5000:5000 your-username/kitten-tts-web:latest

# Check logs
docker logs kitten-tts

# Stop
docker stop kitten-tts
```

### Build from source

```bash
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web
docker build -t kitten-tts-web .
docker run -p 5000:5000 kitten-tts-web
```

## 📱 Accessing the Application

Once running, open your web browser and go to:
- **Local**: http://localhost:5000
- **Network**: http://YOUR_IP_ADDRESS:5000

### Features to Test

1. **Language Toggle**: Switch between English and Chinese
2. **Voice Selection**: Click on different voice cards
3. **Text Input**: Type some text (max 1000 characters)
4. **Generate Speech**: Click the generate button
5. **Audio Playback**: Use the built-in audio player
6. **Download**: Download the generated audio file

## 🆘 Getting Help

If you're still having issues:

1. **Check the logs**: Look for error messages in the terminal
2. **Test installation**: Run `python test_installation.py`
3. **Check system requirements**: Ensure you meet minimum requirements
4. **Try Docker**: If Python issues persist, use Docker
5. **Open an issue**: Create a GitHub issue with:
   - Your operating system
   - Python version
   - Error messages
   - Steps you tried

## 🎯 Next Steps

Once you have the application running:

1. **Explore the interface**: Try different voices and text inputs
2. **Read the API documentation**: Check `API.md` for integration
3. **Deploy to production**: See `DEPLOYMENT.md` for hosting options
4. **Contribute**: Fork the repository and submit improvements

Happy voice generation! 🎉
