# 🐱 Kitten TTS Web Interface

A beautiful, modern web interface for the [Kitten TTS](https://github.com/KittenML/KittenTTS) model - the revolutionary 25MB AI voice model that runs entirely on CPU!

[![Docker Build](https://github.com/your-username/kitten-tts-web/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/your-username/kitten-tts-web/actions/workflows/docker-publish.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/your-username/kitten-tts-web)](https://hub.docker.com/r/your-username/kitten-tts-web)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

[English](README.md) | [中文](README_zh.md)

## ✨ Features

- 🎯 **Beautiful Modern UI** - Clean, responsive design with dark/light theme support
- 🗣️ **8 Expressive Voices** - Choose from multiple high-quality male and female voices
- 🌐 **Multilingual Interface** - Support for English and Chinese languages
- 🚀 **Ultra Fast** - Real-time speech generation powered by CPU-only inference
- 📱 **Mobile Friendly** - Fully responsive design works on all devices
- 🐳 **Docker Ready** - Easy deployment with Docker and Docker Compose
- 🔒 **Privacy First** - All processing happens locally, no data sent to external servers
- 📦 **Lightweight** - Only 25MB model size, runs on minimal hardware

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the latest image
docker run -p 5000:5000 your-username/kitten-tts-web:latest

# Or use docker-compose
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web
docker-compose up -d
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Kitten TTS
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl

# Run the application
python app.py
```

Open your browser and navigate to `http://localhost:5000`

## 🎭 Available Voices

| Voice ID | Gender | Description |
|----------|--------|-------------|
| `expr-voice-2-f` | Female | Clear, professional, great for narration |
| `expr-voice-2-m` | Male | Solid, standard male voice. The reliable choice |
| `expr-voice-3-f` | Female | A bit more expressive, good for character work |
| `expr-voice-3-m` | Male | Deep, thoughtful. Perfect for storytelling |
| `expr-voice-4-f` | Female | Upbeat and friendly. Your go-to for assistants |
| `expr-voice-4-m` | Male | Energetic and clear. Gets the point across |
| `expr-voice-5-m` | Male | The default. A bit... unique. Use with caution! |
| `expr-voice-5-f` | Female | Expressive female voice |

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Port to run the web server |
| `DEBUG` | `false` | Enable debug mode |

### Docker Environment

```bash
docker run -p 5000:5000 \
  -e PORT=5000 \
  -e DEBUG=false \
  your-username/kitten-tts-web:latest
```

## 🏗️ Development

### Prerequisites

- Python 3.8+
- Node.js (for frontend development)
- Docker (optional)

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web

# Install Python dependencies
pip install -r requirements.txt
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl

# Run in development mode
export DEBUG=true
python app.py
```

### Building Docker Image

```bash
# Build image
docker build -t kitten-tts-web .

# Run container
docker run -p 5000:5000 kitten-tts-web
```

## 📚 API Documentation

### Generate Speech

```http
POST /api/generate
Content-Type: application/json

{
  "text": "Hello, this is a test message!",
  "voice": "expr-voice-2-f"
}
```

Response:
```json
{
  "success": true,
  "audio": "base64_encoded_audio_data",
  "format": "wav",
  "sample_rate": 24000
}
```

### Download Audio

```http
POST /api/download
Content-Type: application/json

{
  "text": "Hello, this is a test message!",
  "voice": "expr-voice-2-f"
}
```

Returns: WAV audio file

### Get Available Voices

```http
GET /api/voices
```

Response:
```json
{
  "voices": [
    {
      "id": "expr-voice-2-f",
      "name": "Voice 2 F",
      "gender": "Female",
      "description": "Clear, professional, great for narration"
    }
  ]
}
```

## 🚀 Deployment

### GitHub Actions

This project includes automated Docker image building and publishing to Docker Hub using GitHub Actions.

#### Setup

1. Fork this repository
2. Set up the following secrets in your GitHub repository:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or access token

3. Push to main branch or create a release tag to trigger the build

### Manual Docker Hub Push

```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 \
  -t your-username/kitten-tts-web:latest \
  --push .
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [KittenML](https://github.com/KittenML) for the amazing Kitten TTS model
- The open-source community for inspiration and support

## 📞 Support

- 🐛 [Report Issues](https://github.com/your-username/kitten-tts-web/issues)
- 💬 [Discussions](https://github.com/your-username/kitten-tts-web/discussions)
- 📧 Email: your-email@example.com

---

⭐ If you find this project useful, please consider giving it a star on GitHub!
