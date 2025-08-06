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
import numpy as np
from history_manager import get_history_manager
from enhanced_tts_manager import EnhancedTTSManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables to store TTS models and history manager
enhanced_tts_manager = None
history_manager = None

def load_tts_models():
    """Load all available TTS models using enhanced manager"""
    global enhanced_tts_manager, history_manager

    # Initialize history manager
    history_manager = get_history_manager()

    # Initialize enhanced TTS manager
    enhanced_tts_manager = EnhancedTTSManager()

    logger.info(f"Enhanced TTS Manager initialized with {len(enhanced_tts_manager.engines)} engines")
    logger.info(f"Available engines: {[e['id'] for e in enhanced_tts_manager.get_available_engines()]}")
    return len(enhanced_tts_manager.engines) > 0

def generate_demo_audio(text, voice):
    """Generate demo audio that sounds more like human speech"""
    import numpy as np
    import re

    # Clean and prepare text
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        words = ['hello']

    sample_rate = 24000

    # Voice characteristics - more human-like parameters
    voice_params = {
        'expr-voice-2-f': {'pitch': 200, 'resonance': 0.8, 'breathiness': 0.1, 'speed': 1.0},
        'expr-voice-3-f': {'pitch': 180, 'resonance': 0.9, 'breathiness': 0.15, 'speed': 0.9},
        'expr-voice-4-f': {'pitch': 220, 'resonance': 0.7, 'breathiness': 0.05, 'speed': 1.1},
        'expr-voice-5-f': {'pitch': 190, 'resonance': 0.85, 'breathiness': 0.12, 'speed': 1.0},
        'expr-voice-2-m': {'pitch': 120, 'resonance': 0.6, 'breathiness': 0.08, 'speed': 0.95},
        'expr-voice-3-m': {'pitch': 100, 'resonance': 0.7, 'breathiness': 0.12, 'speed': 0.85},
        'expr-voice-4-m': {'pitch': 140, 'resonance': 0.5, 'breathiness': 0.06, 'speed': 1.05},
        'expr-voice-5-m': {'pitch': 110, 'resonance': 0.65, 'breathiness': 0.1, 'speed': 0.9},
    }

    params = voice_params.get(voice, voice_params['expr-voice-2-f'])

    def generate_vowel_sound(duration, vowel, pitch, resonance, breathiness):
        """Generate a more natural vowel sound"""
        t = np.linspace(0, duration, int(duration * sample_rate), False)

        # Formant frequencies for different vowels (more realistic)
        formants = {
            'a': [730, 1090, 2440],
            'e': [530, 1840, 2480],
            'i': [270, 2290, 3010],
            'o': [570, 840, 2410],
            'u': [440, 1020, 2240]
        }

        f1, f2, f3 = formants.get(vowel, formants['a'])

        # Generate fundamental frequency with natural variation
        pitch_variation = 1 + 0.02 * np.sin(2 * np.pi * 5 * t) + 0.01 * np.random.normal(0, 1, len(t))
        fundamental = pitch * pitch_variation

        # Create the sound using additive synthesis
        sound = np.zeros_like(t)

        # Fundamental frequency (strongest component)
        sound += 0.5 * np.sin(2 * np.pi * fundamental * t)

        # Add harmonics with decreasing amplitude
        for harmonic in range(2, 8):
            amplitude = 0.3 / harmonic
            sound += amplitude * np.sin(2 * np.pi * fundamental * harmonic * t)

        # Apply formant filtering (simplified)
        # This creates the characteristic vowel sound
        formant_response = np.zeros_like(t)
        for formant_freq in [f1, f2, f3]:
            # Simple resonance simulation
            formant_response += resonance * np.sin(2 * np.pi * formant_freq * t) * np.exp(-t * 2)

        # Combine fundamental with formant response
        sound = sound * (1 + 0.3 * formant_response)

        # Add breathiness (noise component)
        if breathiness > 0:
            breath_noise = breathiness * np.random.normal(0, 0.1, len(t))
            sound += breath_noise

        # Apply natural envelope (attack, sustain, decay)
        envelope = np.ones_like(t)
        attack_time = min(0.05, duration * 0.2)
        decay_time = min(0.1, duration * 0.3)

        attack_samples = int(attack_time * sample_rate)
        decay_samples = int(decay_time * sample_rate)

        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        if decay_samples > 0:
            envelope[-decay_samples:] = np.linspace(1, 0.3, decay_samples)

        return sound * envelope

    def generate_consonant_sound(duration, consonant, pitch):
        """Generate consonant sounds (simplified)"""
        t = np.linspace(0, duration, int(duration * sample_rate), False)

        # Consonants are mostly noise-based
        if consonant in 'pbtdkg':  # Plosives
            # Short burst of noise
            sound = np.random.normal(0, 0.3, len(t))
            envelope = np.exp(-t * 20)  # Quick decay
        elif consonant in 'fvszh':  # Fricatives
            # Sustained noise
            sound = np.random.normal(0, 0.2, len(t))
            envelope = np.ones_like(t) * 0.7
        elif consonant in 'mnlr':  # Nasals and liquids
            # Mix of tone and noise
            sound = 0.3 * np.sin(2 * np.pi * pitch * 0.8 * t) + 0.2 * np.random.normal(0, 0.1, len(t))
            envelope = np.ones_like(t) * 0.8
        else:  # Other consonants
            sound = np.random.normal(0, 0.15, len(t))
            envelope = np.exp(-t * 10)

        return sound * envelope

    # Generate audio for each word
    audio_segments = []

    for word in words:
        word_duration = len(word) * 0.12 / params['speed']  # Slower, more natural timing
        syllable_duration = word_duration / max(1, len([c for c in word if c in 'aeiou']))

        word_audio = []

        for char in word:
            if char in 'aeiou':  # Vowels
                char_duration = syllable_duration * 0.8
                char_sound = generate_vowel_sound(
                    char_duration, char, params['pitch'],
                    params['resonance'], params['breathiness']
                )
            else:  # Consonants
                char_duration = syllable_duration * 0.3
                char_sound = generate_consonant_sound(char_duration, char, params['pitch'])

            word_audio.append(char_sound)

        # Concatenate character sounds
        if word_audio:
            word_sound = np.concatenate(word_audio)
            audio_segments.append(word_sound)

        # Add pause between words
        pause_duration = 0.15 / params['speed']
        pause_samples = int(pause_duration * sample_rate)
        audio_segments.append(np.zeros(pause_samples))

    # Concatenate all segments
    if audio_segments:
        audio = np.concatenate(audio_segments)
    else:
        audio = np.zeros(sample_rate)  # 1 second of silence as fallback

    # Apply sentence-level prosody
    if len(audio) > sample_rate // 2:
        # Natural sentence intonation
        prosody_envelope = np.ones_like(audio)
        mid_point = len(audio) // 2

        # Slight rise then fall (natural speech pattern)
        prosody_envelope[:mid_point] *= np.linspace(0.9, 1.1, mid_point)
        prosody_envelope[mid_point:] *= np.linspace(1.1, 0.8, len(audio) - mid_point)

        audio *= prosody_envelope

    # Add very subtle room tone
    room_tone = np.random.normal(0, 0.005, len(audio))
    audio += room_tone

    # Normalize and apply gentle compression
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.7

        # Simple compression to make it sound more natural
        compressed = np.sign(audio) * np.power(np.abs(audio), 0.8)
        audio = compressed * 0.8

    # Gentle fade in/out
    fade_samples = min(sample_rate // 40, len(audio) // 20)  # Shorter, more natural fade
    if fade_samples > 0:
        audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    return audio.astype(np.float32)

def get_available_voices():
    """Get list of available voices for current engine"""
    if not enhanced_tts_manager:
        return []

    try:
        voices = enhanced_tts_manager.get_voices()
        # Convert to expected format
        formatted_voices = []
        for voice in voices:
            formatted_voices.append({
                'id': voice['id'],
                'name': voice.get('name', voice['id']),
                'gender': voice.get('gender', 'Unknown'),
                'description': voice.get('description', f"Voice: {voice['id']}")
            })
        return formatted_voices
    except Exception as e:
        logger.error(f"Error getting voices: {e}")
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
        
        if not enhanced_tts_manager:
            return jsonify({'error': 'TTS manager not initialized'}), 500

        current_engine = enhanced_tts_manager.get_current_engine()
        logger.info(f"Generating speech for text: '{text[:50]}...' with voice: {voice} using engine: {current_engine}")

        try:
            # Use enhanced TTS manager to synthesize
            audio = enhanced_tts_manager.synthesize(text, voice)
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            # Fallback to demo audio
            audio = generate_demo_audio(text, voice)

        # Convert to bytes
        buffer = io.BytesIO()
        sf.write(buffer, audio, 24000, format='WAV')
        buffer.seek(0)
        audio_bytes = buffer.getvalue()

        # Add to history
        try:
            history_entry = history_manager.add_audio(
                text=text,
                voice=voice,
                model_type=current_engine,
                audio_data=audio_bytes
            )
            logger.info(f"Added audio to history: {history_entry['id'] if history_entry else 'failed'}")
        except Exception as e:
            logger.error(f"Failed to add audio to history: {e}")

        # Encode as base64 for JSON response
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')

        return jsonify({
            'success': True,
            'audio': audio_b64,
            'format': 'wav',
            'sample_rate': 24000,
            'engine': current_engine
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
        
        if not enhanced_tts_manager:
            return jsonify({'error': 'TTS manager not initialized'}), 500

        try:
            # Use enhanced TTS manager to synthesize
            audio = enhanced_tts_manager.synthesize(text, voice)
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            # Fallback to demo audio
            audio = generate_demo_audio(text, voice)

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
    try:
        voices = get_available_voices()
        return jsonify({
            'status': 'healthy',
            'engines_loaded': len(enhanced_tts_manager.engines) if enhanced_tts_manager else 0,
            'current_engine': enhanced_tts_manager.get_current_engine() if enhanced_tts_manager else None,
            'available_voices': len(voices)
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/test')
def test_api():
    """Test API endpoint"""
    logger.info("Test API called")
    return jsonify({'test': 'success', 'engines_count': len(enhanced_tts_manager.engines) if enhanced_tts_manager else 0})

@app.route('/api/models')
def get_models():
    """Get available TTS engines"""
    logger.info("Models API called")
    try:
        if not enhanced_tts_manager:
            logger.error("TTS manager not initialized")
            return jsonify({'error': 'TTS manager not initialized'}), 500

        engines = enhanced_tts_manager.get_available_engines()
        logger.info(f"API returning {len(engines)} engines: {[e['id'] for e in engines]}")

        return jsonify({
            'engines': engines,
            'current_engine': enhanced_tts_manager.get_current_engine()
        })
    except Exception as e:
        logger.error(f"Error getting engines: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/<engine_id>', methods=['POST'])
def switch_model(engine_id):
    """Switch to a different TTS engine"""
    try:
        if not enhanced_tts_manager:
            return jsonify({'error': 'TTS manager not initialized'}), 500

        if enhanced_tts_manager.switch_engine(engine_id):
            engine_info = enhanced_tts_manager.get_engine_info(engine_id)
            return jsonify({
                'success': True,
                'current_engine': engine_id,
                'engine_name': engine_info['name'] if engine_info else engine_id
            })
        else:
            return jsonify({'error': 'Engine not found'}), 404
    except Exception as e:
        logger.error(f"Error switching engine: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get audio generation history"""
    try:
        limit = request.args.get('limit', type=int)
        history = history_manager.get_history(limit)

        return jsonify({
            'history': history,
            'stats': history_manager.get_stats()
        })
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<audio_id>')
def get_audio_file(audio_id):
    """Get audio file by ID"""
    try:
        filepath = history_manager.get_audio_file(audio_id)
        if filepath:
            return send_file(filepath, as_attachment=False, mimetype='audio/wav')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        logger.error(f"Error getting audio file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<audio_id>', methods=['DELETE'])
def delete_audio(audio_id):
    """Delete specific audio file"""
    try:
        if history_manager.delete_audio(audio_id):
            return jsonify({'success': True, 'message': 'Audio deleted'})
        else:
            return jsonify({'error': 'Audio not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting audio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear all audio history"""
    try:
        count = history_manager.clear_all()
        return jsonify({
            'success': True,
            'message': f'Cleared {count} audio files'
        })
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup')
def cleanup_old_files():
    """Manually trigger cleanup of old files"""
    try:
        count = history_manager.cleanup_old_files()
        return jsonify({
            'success': True,
            'message': f'Cleaned up {count} old files'
        })
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load TTS models on startup
    if not load_tts_models():
        logger.error("Failed to load TTS models. Exiting...")
        exit(1)
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
