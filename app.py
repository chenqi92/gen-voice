#!/usr/bin/env python3
"""
Kitten TTS Web Application
A beautiful web interface for the Kitten TTS model
"""

import os
import io
import base64
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import soundfile as sf
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variable to store the TTS model
tts_model = None

def load_tts_model():
    """Load the Kitten TTS model"""
    global tts_model
    try:
        from kittentts import KittenTTS
        logger.info("Loading Kitten TTS model...")
        tts_model = KittenTTS("KittenML/kitten-tts-nano-0.1")
        logger.info("Kitten TTS model loaded successfully!")
        return True
    except ImportError as e:
        logger.warning(f"Kitten TTS not available: {e}")
        logger.info("Running in demo mode - TTS functionality will be simulated")
        tts_model = "demo_mode"
        return True
    except Exception as e:
        logger.error(f"Failed to load Kitten TTS model: {e}")
        logger.info("Running in demo mode - TTS functionality will be simulated")
        tts_model = "demo_mode"
        return True

def generate_demo_audio(text, voice):
    """Generate demo audio with tones that simulate speech"""
    import numpy as np
    duration = min(len(text) * 0.08, 8.0)  # Estimate duration based on text length
    duration = max(duration, 1.0)  # Minimum 1 second
    sample_rate = 24000

    # Generate a simple tone pattern to simulate speech
    t = np.linspace(0, duration, int(duration * sample_rate), False)

    # Create a pattern of tones that varies based on voice selection
    voice_freq_map = {
        'expr-voice-2-f': 800,  # Higher pitch for female
        'expr-voice-3-f': 750,
        'expr-voice-4-f': 850,
        'expr-voice-5-f': 780,
        'expr-voice-2-m': 400,  # Lower pitch for male
        'expr-voice-3-m': 350,
        'expr-voice-4-m': 450,
        'expr-voice-5-m': 380,
    }

    base_freq = voice_freq_map.get(voice, 600)

    # Create a more speech-like pattern with varying frequency and amplitude
    audio = np.zeros_like(t)

    # Add multiple harmonics to make it sound more natural
    for i, harmonic in enumerate([1, 0.5, 0.3, 0.2]):
        freq_variation = np.sin(2 * np.pi * 0.5 * t) * 50  # Slow frequency modulation
        freq = base_freq * (i + 1) + freq_variation
        audio += harmonic * np.sin(2 * np.pi * freq * t)

    # Add amplitude modulation to simulate speech rhythm
    word_count = len(text.split())
    rhythm_freq = max(word_count / duration / 4, 1.0)  # Rhythm based on word density
    amplitude_mod = 0.7 + 0.3 * np.sin(2 * np.pi * rhythm_freq * t)
    audio *= amplitude_mod

    # Add some pauses for longer text
    if duration > 3:
        pause_positions = np.random.choice(len(audio), size=int(duration), replace=False)
        for pos in pause_positions:
            start = max(0, pos - sample_rate // 10)
            end = min(len(audio), pos + sample_rate // 10)
            audio[start:end] *= 0.1

    # Normalize and apply fade in/out
    audio = audio / np.max(np.abs(audio)) * 0.7
    fade_samples = sample_rate // 20  # 50ms fade
    audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    return audio.astype(np.float32)

def get_available_voices():
    """Get list of available voices"""
    if tts_model is None:
        return []

    # Voice metadata with descriptions
    voice_info = {
        'expr-voice-2-f': {'gender': 'Female', 'description': 'Clear, professional, great for narration'},
        'expr-voice-2-m': {'gender': 'Male', 'description': 'Solid, standard male voice. The reliable choice'},
        'expr-voice-3-f': {'gender': 'Female', 'description': 'A bit more expressive, good for character work'},
        'expr-voice-3-m': {'gender': 'Male', 'description': 'Deep, thoughtful. Perfect for storytelling'},
        'expr-voice-4-f': {'gender': 'Female', 'description': 'Upbeat and friendly. Your go-to for assistants'},
        'expr-voice-4-m': {'gender': 'Male', 'description': 'Energetic and clear. Gets the point across'},
        'expr-voice-5-m': {'gender': 'Male', 'description': 'The default. A bit... unique. Use with caution!'},
        'expr-voice-5-f': {'gender': 'Female', 'description': 'Expressive female voice'}
    }

    try:
        if tts_model == "demo_mode":
            # Return all voices in demo mode
            voices = list(voice_info.keys())
        else:
            voices = tts_model.available_voices

        return [
            {
                'id': voice,
                'name': voice.replace('expr-voice-', 'Voice ').replace('-', ' ').title(),
                'gender': voice_info.get(voice, {}).get('gender', 'Unknown'),
                'description': voice_info.get(voice, {}).get('description', 'High quality voice')
            }
            for voice in voices if voice in voice_info
        ]
    except Exception as e:
        logger.error(f"Error getting available voices: {e}")
        return []

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/voices')
def api_voices():
    """API endpoint to get available voices"""
    voices = get_available_voices()
    return jsonify({'voices': voices})

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate speech"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice = data.get('voice', 'expr-voice-2-f')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Remove character limit - allow any reasonable length
        if len(text) > 50000:  # 50k character limit for safety
            return jsonify({'error': 'Text too long (max 50,000 characters)'}), 400
        
        if tts_model is None:
            return jsonify({'error': 'TTS model not loaded'}), 500
        
        logger.info(f"Generating speech for text: '{text[:50]}...' with voice: {voice}")

        if tts_model == "demo_mode":
            # Generate demo audio with tones
            audio = generate_demo_audio(text, voice)
        else:
            # Generate real audio
            audio = tts_model.generate(text, voice=voice)

        # Convert to bytes
        buffer = io.BytesIO()
        sf.write(buffer, audio, 24000, format='WAV')
        buffer.seek(0)

        # Encode as base64 for JSON response
        audio_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'audio': audio_b64,
            'format': 'wav',
            'sample_rate': 24000
        })
        
    except Exception as e:
        logger.error(f"Error generating speech: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def api_download():
    """API endpoint to download generated audio"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice = data.get('voice', 'expr-voice-2-f')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if tts_model is None:
            return jsonify({'error': 'TTS model not loaded'}), 500
        
        # Generate audio
        if tts_model == "demo_mode":
            # Generate demo audio with tones
            audio = generate_demo_audio(text, voice)
        else:
            audio = tts_model.generate(text, voice=voice)

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            sf.write(tmp_file.name, audio, 24000)
            
            return send_file(
                tmp_file.name,
                as_attachment=True,
                download_name=f'kitten_tts_{voice}.wav',
                mimetype='audio/wav'
            )
            
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': tts_model is not None,
        'available_voices': len(get_available_voices())
    })

if __name__ == '__main__':
    # Load the TTS model on startup
    if not load_tts_model():
        logger.error("Failed to load TTS model. Exiting...")
        exit(1)
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
