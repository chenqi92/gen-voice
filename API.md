# 📡 API Documentation

The Kitten TTS Web Application provides a RESTful API for text-to-speech generation.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, no authentication is required. The API is open for all requests.

## Rate Limiting

- Maximum text length: 1000 characters
- No explicit rate limiting implemented (consider adding for production)

## Endpoints

### 1. Health Check

Check if the application is running and the TTS model is loaded.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "available_voices": 8
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `500 Internal Server Error`: Service has issues

---

### 2. Get Available Voices

Retrieve the list of available voices with their metadata.

**Endpoint:** `GET /api/voices`

**Response:**
```json
{
  "voices": [
    {
      "id": "expr-voice-2-f",
      "name": "Voice 2 F",
      "gender": "Female",
      "description": "Clear, professional, great for narration"
    },
    {
      "id": "expr-voice-2-m",
      "name": "Voice 2 M",
      "gender": "Male",
      "description": "Solid, standard male voice. The reliable choice"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Successfully retrieved voices
- `500 Internal Server Error`: Failed to load voices

---

### 3. Generate Speech

Generate speech audio from text using a specified voice.

**Endpoint:** `POST /api/generate`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Hello, this is a test message!",
  "voice": "expr-voice-2-f"
}
```

**Parameters:**
- `text` (string, required): Text to convert to speech (max 1000 characters)
- `voice` (string, required): Voice ID from the available voices list

**Response:**
```json
{
  "success": true,
  "audio": "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=",
  "format": "wav",
  "sample_rate": 24000
}
```

**Response Fields:**
- `success` (boolean): Whether the generation was successful
- `audio` (string): Base64-encoded WAV audio data
- `format` (string): Audio format (always "wav")
- `sample_rate` (integer): Sample rate in Hz (always 24000)

**Error Response:**
```json
{
  "error": "Text is required"
}
```

**Status Codes:**
- `200 OK`: Successfully generated speech
- `400 Bad Request`: Invalid input (missing text, text too long, invalid voice)
- `500 Internal Server Error`: Generation failed

---

### 4. Download Audio

Generate and download speech audio as a WAV file.

**Endpoint:** `POST /api/download`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Hello, this is a test message!",
  "voice": "expr-voice-2-f"
}
```

**Parameters:**
- `text` (string, required): Text to convert to speech (max 1000 characters)
- `voice` (string, required): Voice ID from the available voices list

**Response:**
- Content-Type: `audio/wav`
- Content-Disposition: `attachment; filename="kitten_tts_{voice}.wav"`
- Binary WAV audio data

**Status Codes:**
- `200 OK`: Successfully generated and returned audio file
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Generation failed

---

## Usage Examples

### cURL Examples

#### Health Check
```bash
curl -X GET http://localhost:5000/health
```

#### Get Available Voices
```bash
curl -X GET http://localhost:5000/api/voices
```

#### Generate Speech
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test message!",
    "voice": "expr-voice-2-f"
  }'
```

#### Download Audio
```bash
curl -X POST http://localhost:5000/api/download \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test message!",
    "voice": "expr-voice-2-f"
  }' \
  --output "speech.wav"
```

### Python Examples

#### Using requests library

```python
import requests
import base64
import io
import soundfile as sf

# Base URL
BASE_URL = "http://localhost:5000"

# Get available voices
response = requests.get(f"{BASE_URL}/api/voices")
voices = response.json()["voices"]
print("Available voices:", [v["id"] for v in voices])

# Generate speech
data = {
    "text": "Hello, this is a test message!",
    "voice": "expr-voice-2-f"
}

response = requests.post(f"{BASE_URL}/api/generate", json=data)
result = response.json()

if result["success"]:
    # Decode base64 audio
    audio_data = base64.b64decode(result["audio"])
    
    # Save to file
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    
    print("Audio saved to output.wav")
else:
    print("Error:", result.get("error"))
```

#### Download directly

```python
import requests

# Download audio file directly
data = {
    "text": "Hello, this is a test message!",
    "voice": "expr-voice-2-f"
}

response = requests.post(f"{BASE_URL}/api/download", json=data)

if response.status_code == 200:
    with open("downloaded_speech.wav", "wb") as f:
        f.write(response.content)
    print("Audio downloaded successfully")
else:
    print("Download failed:", response.status_code)
```

### JavaScript Examples

#### Using fetch API

```javascript
// Get available voices
async function getVoices() {
    const response = await fetch('/api/voices');
    const data = await response.json();
    return data.voices;
}

// Generate speech
async function generateSpeech(text, voice) {
    const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, voice })
    });
    
    const result = await response.json();
    
    if (result.success) {
        // Convert base64 to blob
        const audioData = atob(result.audio);
        const audioArray = new Uint8Array(audioData.length);
        for (let i = 0; i < audioData.length; i++) {
            audioArray[i] = audioData.charCodeAt(i);
        }
        
        const audioBlob = new Blob([audioArray], { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // Play audio
        const audio = new Audio(audioUrl);
        audio.play();
        
        return audioUrl;
    } else {
        throw new Error(result.error);
    }
}

// Usage
getVoices().then(voices => {
    console.log('Available voices:', voices);
    
    // Generate speech with first available voice
    if (voices.length > 0) {
        generateSpeech('Hello, world!', voices[0].id)
            .then(audioUrl => console.log('Audio generated:', audioUrl))
            .catch(error => console.error('Error:', error));
    }
});
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Text is required"
}
```

```json
{
  "error": "Text too long (max 1000 characters)"
}
```

```json
{
  "error": "Invalid voice ID"
}
```

#### 500 Internal Server Error
```json
{
  "error": "TTS model not loaded"
}
```

```json
{
  "error": "Failed to generate speech. Please try again."
}
```

### Best Practices

1. **Always check the response status** before processing the result
2. **Handle network errors** with appropriate retry logic
3. **Validate input** on the client side before sending requests
4. **Cache voice list** to avoid repeated API calls
5. **Implement timeouts** for long-running requests
6. **Use appropriate error messages** for user feedback

## WebSocket Support

Currently, the API only supports HTTP requests. WebSocket support for real-time streaming may be added in future versions.

## Versioning

The current API version is v1. Future versions will be backward compatible or will use versioned endpoints (e.g., `/api/v2/generate`).

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for all origins in development. For production, configure appropriate CORS policies based on your deployment needs.
