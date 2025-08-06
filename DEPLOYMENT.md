# 🚀 Deployment Guide

This guide covers various deployment options for the Kitten TTS Web Application.

## 📋 Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Python 3.8+ (for manual deployment)
- Git (for cloning the repository)

## 🐳 Docker Deployment (Recommended)

### Quick Start with Docker

```bash
# Pull and run the latest image
docker run -d \
  --name kitten-tts \
  -p 5000:5000 \
  --restart unless-stopped \
  your-username/kitten-tts-web:latest
```

### Using Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web
```

2. Start the application:
```bash
docker-compose up -d
```

3. Check the logs:
```bash
docker-compose logs -f
```

4. Stop the application:
```bash
docker-compose down
```

### Custom Configuration

Create a `.env` file for custom configuration:

```bash
# Copy the example file
cp .env.example .env

# Edit the configuration
nano .env
```

Then run with:
```bash
docker-compose --env-file .env up -d
```

## 🖥️ Manual Deployment

### Local Development

1. Clone and setup:
```bash
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web

# Linux/Mac
chmod +x start.sh
./start.sh

# Windows
start.bat
```

### Production Deployment

1. Setup virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
```

3. Test installation:
```bash
python test_installation.py
```

4. Run with Gunicorn (Linux/Mac):
```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app
```

## ☁️ Cloud Deployment

### Heroku

1. Create a `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Railway

1. Connect your GitHub repository to Railway
2. Set environment variables:
   - `PORT`: 5000
   - `DEBUG`: false

### DigitalOcean App Platform

1. Create a new app from your GitHub repository
2. Configure the service:
   - Build Command: `pip install -r requirements.txt && pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl`
   - Run Command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app`

## 🔧 Reverse Proxy Setup

### Nginx

Create `/etc/nginx/sites-available/kitten-tts`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for audio generation
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/kitten-tts /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Apache

Create a virtual host:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    
    ProxyPreserveHost On
    ProxyRequests Off
    ProxyPass / http://localhost:5000/
    ProxyPassReverse / http://localhost:5000/
    
    # Increase timeout for audio generation
    ProxyTimeout 300
</VirtualHost>
```

## 🔒 SSL/HTTPS Setup

### Using Certbot (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring and Logging

### Docker Logs

```bash
# View logs
docker logs kitten-tts

# Follow logs
docker logs -f kitten-tts

# With docker-compose
docker-compose logs -f
```

### System Service (Linux)

Create `/etc/systemd/system/kitten-tts.service`:

```ini
[Unit]
Description=Kitten TTS Web Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/kitten-tts-web
Environment=PATH=/path/to/kitten-tts-web/venv/bin
ExecStart=/path/to/kitten-tts-web/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable kitten-tts
sudo systemctl start kitten-tts
```

## 🔧 Performance Tuning

### Resource Requirements

- **Minimum**: 1 CPU, 1GB RAM
- **Recommended**: 2 CPU, 2GB RAM
- **Storage**: 1GB (includes model cache)

### Optimization Tips

1. **Use multiple workers** (but not too many for CPU-bound tasks):
```bash
gunicorn --workers 2 --timeout 120 app:app
```

2. **Enable caching** for static files in Nginx:
```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **Limit concurrent requests** to prevent overload:
```python
# In app.py, add rate limiting if needed
```

## 🚨 Troubleshooting

### Common Issues

1. **Model loading fails**:
   - Check internet connection for initial download
   - Verify disk space (need ~100MB for model cache)

2. **Audio generation timeout**:
   - Increase proxy timeout settings
   - Check CPU resources

3. **Memory issues**:
   - Reduce number of workers
   - Monitor memory usage with `htop` or `docker stats`

### Health Checks

The application provides a health endpoint:
```bash
curl http://localhost:5000/health
```

### Debug Mode

Enable debug mode for development:
```bash
export DEBUG=true
python app.py
```

## 📈 Scaling

For high-traffic deployments:

1. **Load Balancer**: Use multiple instances behind a load balancer
2. **Container Orchestration**: Deploy with Kubernetes or Docker Swarm
3. **CDN**: Use a CDN for static assets
4. **Caching**: Implement Redis for session/response caching

## 🔐 Security Considerations

1. **Firewall**: Only expose necessary ports
2. **Updates**: Keep dependencies updated
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: The app validates input length (max 1000 chars)
5. **HTTPS**: Always use HTTPS in production

## 📞 Support

If you encounter issues during deployment:

1. Check the logs first
2. Verify system requirements
3. Test with the provided test script
4. Open an issue on GitHub with detailed information
