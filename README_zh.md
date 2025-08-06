# 🐱 Kitten TTS 网页界面

为 [Kitten TTS](https://github.com/KittenML/KittenTTS) 模型打造的美观现代化网页界面 - 这是一个革命性的25MB AI语音模型，完全在CPU上运行！

[![Docker Build](https://github.com/your-username/kitten-tts-web/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/your-username/kitten-tts-web/actions/workflows/docker-publish.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/your-username/kitten-tts-web)](https://hub.docker.com/r/your-username/kitten-tts-web)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

[English](README.md) | [中文](README_zh.md)

## ✨ 功能特色

- 🎯 **美观现代界面** - 简洁响应式设计，支持深色/浅色主题
- 🗣️ **8种表现力声音** - 从多种高质量男女声音中选择
- 🌐 **多语言界面** - 支持英文和中文界面
- 🚀 **超快速度** - 基于CPU推理的实时语音生成
- 📱 **移动端友好** - 完全响应式设计，适配所有设备
- 🐳 **Docker就绪** - 使用Docker和Docker Compose轻松部署
- 🔒 **隐私优先** - 所有处理都在本地进行，不向外部服务器发送数据
- 📦 **轻量级** - 仅25MB模型大小，在最小硬件上运行

## 🚀 快速开始

### 使用Docker（推荐）

```bash
# 拉取并运行最新镜像
docker run -p 5000:5000 your-username/kitten-tts-web:latest

# 或使用docker-compose
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web
docker-compose up -d
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装Kitten TTS
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl

# 运行应用
python app.py
```

打开浏览器访问 `http://localhost:5000`

## 🎭 可用声音

| 声音ID | 性别 | 描述 |
|--------|------|------|
| `expr-voice-2-f` | 女声 | 清晰专业，适合旁白 |
| `expr-voice-2-m` | 男声 | 稳定标准男声，可靠选择 |
| `expr-voice-3-f` | 女声 | 更有表现力，适合角色配音 |
| `expr-voice-3-m` | 男声 | 深沉思考型，完美的故事讲述 |
| `expr-voice-4-f` | 女声 | 乐观友好，助手的首选 |
| `expr-voice-4-m` | 男声 | 充满活力清晰，传达要点 |
| `expr-voice-5-m` | 男声 | 默认声音，有点...独特，谨慎使用！ |
| `expr-voice-5-f` | 女声 | 富有表现力的女声 |

## 🔧 配置

### 环境变量

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `PORT` | `5000` | Web服务器运行端口 |
| `DEBUG` | `false` | 启用调试模式 |

### Docker环境

```bash
docker run -p 5000:5000 \
  -e PORT=5000 \
  -e DEBUG=false \
  your-username/kitten-tts-web:latest
```

## 🏗️ 开发

### 前置要求

- Python 3.8+
- Node.js（用于前端开发）
- Docker（可选）

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/your-username/kitten-tts-web.git
cd kitten-tts-web

# 安装Python依赖
pip install -r requirements.txt
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl

# 以开发模式运行
export DEBUG=true
python app.py
```

### 构建Docker镜像

```bash
# 构建镜像
docker build -t kitten-tts-web .

# 运行容器
docker run -p 5000:5000 kitten-tts-web
```

## 📚 API文档

### 生成语音

```http
POST /api/generate
Content-Type: application/json

{
  "text": "你好，这是一条测试消息！",
  "voice": "expr-voice-2-f"
}
```

响应：
```json
{
  "success": true,
  "audio": "base64编码的音频数据",
  "format": "wav",
  "sample_rate": 24000
}
```

### 下载音频

```http
POST /api/download
Content-Type: application/json

{
  "text": "你好，这是一条测试消息！",
  "voice": "expr-voice-2-f"
}
```

返回：WAV音频文件

### 获取可用声音

```http
GET /api/voices
```

响应：
```json
{
  "voices": [
    {
      "id": "expr-voice-2-f",
      "name": "Voice 2 F",
      "gender": "Female",
      "description": "清晰专业，适合旁白"
    }
  ]
}
```

## 🚀 部署

### GitHub Actions

本项目包含自动化Docker镜像构建和发布到Docker Hub的GitHub Actions。

#### 设置

1. Fork此仓库
2. 在GitHub仓库中设置以下secrets：
   - `DOCKER_USERNAME`：您的Docker Hub用户名
   - `DOCKER_PASSWORD`：您的Docker Hub密码或访问令牌

3. 推送到main分支或创建发布标签以触发构建

### 手动推送到Docker Hub

```bash
# 为多平台构建
docker buildx build --platform linux/amd64,linux/arm64 \
  -t your-username/kitten-tts-web:latest \
  --push .
```

## 🤝 贡献

欢迎贡献！请随时提交Pull Request。

1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用Apache License 2.0许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 🙏 致谢

- [KittenML](https://github.com/KittenML) 提供了令人惊叹的Kitten TTS模型
- 开源社区的灵感和支持

## 📞 支持

- 🐛 [报告问题](https://github.com/your-username/kitten-tts-web/issues)
- 💬 [讨论](https://github.com/your-username/kitten-tts-web/discussions)
- 📧 邮箱：your-email@example.com

---

⭐ 如果您觉得这个项目有用，请考虑在GitHub上给它一个星标！
