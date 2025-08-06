# 🚀 Quick Start Guide

## 🎯 Ready to Use - Choose Your Method

### Option 1: Docker (Recommended - 2 minutes)
```bash
# Pull and run (replace with your Docker Hub username)
docker run -p 5000:5000 your-username/kitten-tts-web:latest

# Open browser: http://localhost:5000
```

### Option 2: Local Development (5 minutes)
```bash
# Windows
start.bat

# Linux/macOS
chmod +x start.sh
./start.sh

# Open browser: http://localhost:5000
```

### Option 3: Manual Setup (10 minutes)
```bash
# 1. Clone repository
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test installation
python test_installation.py

# 5. Run application
python app.py

# Open browser: http://localhost:5000
```

## 🧪 Test Everything Works

Run the comprehensive test suite:
```bash
python test_functionality.py
```

Expected output: `🎉 All functionality tests passed!`

## 🔧 GitHub Actions Setup

To enable automatic Docker builds:

1. **Fork this repository**
2. **Set GitHub Secrets**:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/token
3. **Trigger build**: Edit the `VERSION` file and push to main branch

## 📝 Version Management

The GitHub Actions workflow only triggers when the `VERSION` file changes:

```bash
# Update version to trigger new Docker build
echo "1.0.1" > VERSION
git add VERSION
git commit -m "Release v1.0.1"
git push origin main
```

This will automatically:
- Build Docker image for multiple platforms
- Push to Docker Hub with version tag
- Update Docker Hub description

## 🎨 Features Overview

- **8 Voice Options**: Choose from different male/female voices
- **Real-time Generation**: Instant audio generation (demo mode)
- **Download Support**: Save generated audio as WAV files
- **Multilingual UI**: Switch between English and Chinese
- **Mobile Friendly**: Works on all devices
- **API Access**: RESTful API for integration

## 🔍 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python 3.8+ from python.org
- Make sure to check "Add Python to PATH"

**"Module not found"**
- Activate virtual environment first
- Run `pip install -r requirements.txt`

**"Port 5000 in use"**
- Change port: `export PORT=8080` (Linux/macOS) or `set PORT=8080` (Windows)

**"Docker build fails"**
- Check Docker is running
- Verify GitHub secrets are set correctly

### Demo vs Full Mode

**Demo Mode** (default):
- ✅ Full web interface
- ✅ All 8 voices selectable  
- ⚠️ Generates silent audio (for testing)

**Full Mode** (with Kitten TTS):
```bash
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
```
- ✅ Real speech synthesis
- ✅ High-quality audio output

## 📚 Next Steps

1. **Explore the Interface**: Try different voices and text inputs
2. **Read API Docs**: Check `API.md` for integration details
3. **Deploy to Production**: See `DEPLOYMENT.md` for hosting options
4. **Customize**: Modify CSS/JS for your needs

## 🎉 You're Ready!

The Kitten TTS Web Interface is now running and ready to use. Enjoy generating high-quality speech with this lightweight, CPU-only AI model!
