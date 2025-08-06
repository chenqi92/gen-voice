#!/usr/bin/env python3
"""
Enhanced TTS Manager
Supports multiple TTS engines including cloud services
"""

import os
import io
import json
import logging
import tempfile
import numpy as np
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class TTSEngine(ABC):
    """Abstract base class for TTS engines"""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_voices(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def synthesize(self, text: str, voice: str, **kwargs) -> np.ndarray:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass

class GoogleTTSEngine(TTSEngine):
    """Google TTS Engine"""
    
    def __init__(self):
        self.gtts_class = None
        try:
            from gtts import gTTS
            self.gtts_class = gTTS
        except ImportError:
            pass
    
    def get_name(self) -> str:
        return "Google TTS"
    
    def get_description(self) -> str:
        return "Google online text-to-speech service"
    
    def is_available(self) -> bool:
        return self.gtts_class is not None
    
    def get_voices(self) -> List[Dict]:
        return [
            {'id': 'en-us-standard', 'name': 'English (US) - Standard', 'lang': 'en', 'slow': False},
            {'id': 'en-us-slow', 'name': 'English (US) - Slow', 'lang': 'en', 'slow': True},
            {'id': 'en-uk-standard', 'name': 'English (UK) - Standard', 'lang': 'en-uk', 'slow': False},
            {'id': 'en-au-standard', 'name': 'English (AU) - Standard', 'lang': 'en-au', 'slow': False},
            {'id': 'en-ca-standard', 'name': 'English (CA) - Standard', 'lang': 'en-ca', 'slow': False},
            {'id': 'en-in-standard', 'name': 'English (IN) - Standard', 'lang': 'en-in', 'slow': False},
            {'id': 'zh-cn-standard', 'name': 'Chinese (CN) - Standard', 'lang': 'zh-cn', 'slow': False},
            {'id': 'zh-tw-standard', 'name': 'Chinese (TW) - Standard', 'lang': 'zh-tw', 'slow': False},
        ]
    
    def synthesize(self, text: str, voice: str, **kwargs) -> np.ndarray:
        voice_config = self._get_voice_config(voice)
        
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        try:
            tts = self.gtts_class(text=text, **voice_config)
            tts.save(temp_path)
            
            # Convert MP3 to WAV
            try:
                from pydub import AudioSegment
                audio_segment = AudioSegment.from_mp3(temp_path)
                audio_data = audio_segment.get_array_of_samples()
                audio = np.array(audio_data, dtype=np.float32) / 32768.0
                
                if audio_segment.channels == 2:
                    audio = audio.reshape((-1, 2)).mean(axis=1)
                
                return audio
            except ImportError:
                logger.warning("pydub not available for MP3 conversion")
                raise
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    def _get_voice_config(self, voice: str) -> Dict:
        voice_map = {
            'en-us-standard': {'lang': 'en', 'slow': False},
            'en-us-slow': {'lang': 'en', 'slow': True},
            'en-uk-standard': {'lang': 'en-uk', 'slow': False},
            'en-au-standard': {'lang': 'en-au', 'slow': False},
            'en-ca-standard': {'lang': 'en-ca', 'slow': False},
            'en-in-standard': {'lang': 'en-in', 'slow': False},
            'zh-cn-standard': {'lang': 'zh-cn', 'slow': False},
            'zh-tw-standard': {'lang': 'zh-tw', 'slow': False},
        }
        return voice_map.get(voice, {'lang': 'en', 'slow': False})

class OpenAITTSEngine(TTSEngine):
    """OpenAI TTS Engine"""
    
    def __init__(self):
        self.client = None
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            pass
    
    def get_name(self) -> str:
        return "OpenAI TTS"
    
    def get_description(self) -> str:
        return "OpenAI high-quality neural text-to-speech"
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def get_voices(self) -> List[Dict]:
        return [
            {'id': 'alloy', 'name': 'Alloy - Balanced', 'gender': 'Neutral'},
            {'id': 'echo', 'name': 'Echo - Male', 'gender': 'Male'},
            {'id': 'fable', 'name': 'Fable - British Male', 'gender': 'Male'},
            {'id': 'onyx', 'name': 'Onyx - Deep Male', 'gender': 'Male'},
            {'id': 'nova', 'name': 'Nova - Female', 'gender': 'Female'},
            {'id': 'shimmer', 'name': 'Shimmer - Soft Female', 'gender': 'Female'},
        ]
    
    def synthesize(self, text: str, voice: str, **kwargs) -> np.ndarray:
        try:
            response = self.client.audio.speech.create(
                model="tts-1-hd",  # Use high-definition model
                voice=voice,
                input=text,
                response_format="wav"
            )
            
            # Convert response to numpy array
            audio_data = response.content
            
            # Use soundfile to read WAV data
            import soundfile as sf
            audio, sample_rate = sf.read(io.BytesIO(audio_data))
            
            # Ensure mono and float32
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)
            
            return audio.astype(np.float32)
            
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            raise

class AzureTTSEngine(TTSEngine):
    """Azure Cognitive Services TTS Engine"""
    
    def __init__(self):
        self.speech_config = None
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            subscription_key = os.getenv('AZURE_SPEECH_KEY')
            region = os.getenv('AZURE_SPEECH_REGION', 'eastus')
            
            if subscription_key:
                self.speech_config = speechsdk.SpeechConfig(
                    subscription=subscription_key, 
                    region=region
                )
                self.speechsdk = speechsdk
        except ImportError:
            pass
    
    def get_name(self) -> str:
        return "Azure TTS"
    
    def get_description(self) -> str:
        return "Microsoft Azure Cognitive Services TTS"
    
    def is_available(self) -> bool:
        return self.speech_config is not None
    
    def get_voices(self) -> List[Dict]:
        return [
            {'id': 'en-US-AriaNeural', 'name': 'Aria (US Female)', 'gender': 'Female', 'lang': 'en-US'},
            {'id': 'en-US-DavisNeural', 'name': 'Davis (US Male)', 'gender': 'Male', 'lang': 'en-US'},
            {'id': 'en-US-JennyNeural', 'name': 'Jenny (US Female)', 'gender': 'Female', 'lang': 'en-US'},
            {'id': 'en-US-GuyNeural', 'name': 'Guy (US Male)', 'gender': 'Male', 'lang': 'en-US'},
            {'id': 'en-GB-SoniaNeural', 'name': 'Sonia (UK Female)', 'gender': 'Female', 'lang': 'en-GB'},
            {'id': 'en-GB-RyanNeural', 'name': 'Ryan (UK Male)', 'gender': 'Male', 'lang': 'en-GB'},
            {'id': 'zh-CN-XiaoxiaoNeural', 'name': 'Xiaoxiao (CN Female)', 'gender': 'Female', 'lang': 'zh-CN'},
            {'id': 'zh-CN-YunxiNeural', 'name': 'Yunxi (CN Male)', 'gender': 'Male', 'lang': 'zh-CN'},
        ]
    
    def synthesize(self, text: str, voice: str, **kwargs) -> np.ndarray:
        try:
            self.speech_config.speech_synthesis_voice_name = voice
            
            synthesizer = self.speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=None
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == self.speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Convert audio data to numpy array
                audio_data = result.audio_data
                
                import soundfile as sf
                audio, sample_rate = sf.read(io.BytesIO(audio_data))
                
                if len(audio.shape) > 1:
                    audio = audio.mean(axis=1)
                
                return audio.astype(np.float32)
            else:
                raise Exception(f"Azure TTS failed: {result.reason}")
                
        except Exception as e:
            logger.error(f"Azure TTS error: {e}")
            raise

class CoquiTTSEngine(TTSEngine):
    """Coqui TTS Engine (Simulated for Python 3.13 compatibility)"""

    def __init__(self):
        # Simulate Coqui TTS availability
        self.available = True

    def get_name(self) -> str:
        return "Coqui TTS"

    def get_description(self) -> str:
        return "High-quality neural text-to-speech (Simulated)"

    def is_available(self) -> bool:
        return self.available

    def get_voices(self) -> List[Dict]:
        return [
            {'id': 'ljspeech', 'name': 'LJSpeech - Female', 'gender': 'Female'},
            {'id': 'vctk-p225', 'name': 'VCTK P225 - Female British', 'gender': 'Female'},
            {'id': 'vctk-p226', 'name': 'VCTK P226 - Male British', 'gender': 'Male'},
            {'id': 'vctk-p227', 'name': 'VCTK P227 - Male British', 'gender': 'Male'},
            {'id': 'jenny', 'name': 'Jenny - Neural Female', 'gender': 'Female'},
            {'id': 'ryan', 'name': 'Ryan - Neural Male', 'gender': 'Male'},
        ]

    def synthesize(self, text: str, voice: str, **kwargs) -> np.ndarray:
        # Generate simulated high-quality audio
        import numpy as np

        # Create more realistic audio simulation
        duration = len(text) * 0.08  # ~80ms per character
        sample_rate = 22050
        samples = int(duration * sample_rate)

        # Generate more natural-sounding audio with multiple frequencies
        t = np.linspace(0, duration, samples)

        # Base frequency varies by voice
        voice_freqs = {
            'ljspeech': 220,
            'vctk-p225': 200,
            'vctk-p226': 150,
            'vctk-p227': 140,
            'jenny': 210,
            'ryan': 160
        }
        base_freq = voice_freqs.get(voice, 180)

        # Generate more complex waveform
        audio = (
            0.3 * np.sin(2 * np.pi * base_freq * t) +
            0.2 * np.sin(2 * np.pi * base_freq * 1.5 * t) +
            0.1 * np.sin(2 * np.pi * base_freq * 2 * t) +
            0.05 * np.random.normal(0, 1, samples)  # Add some noise
        )

        # Apply envelope to make it sound more natural
        envelope = np.exp(-t * 0.5) * (1 - np.exp(-t * 10))
        audio *= envelope

        # Normalize
        audio = audio / np.max(np.abs(audio)) * 0.8

        return audio.astype(np.float32)

class KittenTTSEngine(TTSEngine):
    """Kitten TTS Engine (Simulated for Python 3.13 compatibility)"""

    def __init__(self):
        # Simulate Kitten TTS availability
        self.available = True

    def get_name(self) -> str:
        return "Kitten TTS"

    def get_description(self) -> str:
        return "Lightweight 25MB AI voice model (Simulated)"

    def is_available(self) -> bool:
        return self.available

    def get_voices(self) -> List[Dict]:
        return [
            {'id': 'kitten-voice-1', 'name': 'Kitten Voice 1 - Expressive', 'gender': 'Female'},
            {'id': 'kitten-voice-2', 'name': 'Kitten Voice 2 - Clear', 'gender': 'Female'},
            {'id': 'kitten-voice-3', 'name': 'Kitten Voice 3 - Warm', 'gender': 'Male'},
            {'id': 'kitten-voice-4', 'name': 'Kitten Voice 4 - Professional', 'gender': 'Male'},
        ]

    def synthesize(self, text: str, voice: str, **kwargs) -> np.ndarray:
        # Generate simulated Kitten TTS audio
        import numpy as np

        duration = len(text) * 0.07  # Slightly faster than Coqui
        sample_rate = 24000  # Higher sample rate for Kitten TTS
        samples = int(duration * sample_rate)

        t = np.linspace(0, duration, samples)

        # Voice characteristics
        voice_params = {
            'kitten-voice-1': {'freq': 250, 'vibrato': 0.02},
            'kitten-voice-2': {'freq': 230, 'vibrato': 0.01},
            'kitten-voice-3': {'freq': 170, 'vibrato': 0.015},
            'kitten-voice-4': {'freq': 160, 'vibrato': 0.005},
        }

        params = voice_params.get(voice, {'freq': 200, 'vibrato': 0.01})
        base_freq = params['freq']
        vibrato = params['vibrato']

        # Generate audio with vibrato effect
        vibrato_wave = 1 + vibrato * np.sin(2 * np.pi * 5 * t)  # 5Hz vibrato
        audio = (
            0.4 * np.sin(2 * np.pi * base_freq * vibrato_wave * t) +
            0.25 * np.sin(2 * np.pi * base_freq * 1.3 * vibrato_wave * t) +
            0.15 * np.sin(2 * np.pi * base_freq * 0.7 * vibrato_wave * t)
        )

        # Apply dynamic envelope
        envelope = np.exp(-t * 0.3) * (1 - np.exp(-t * 15))
        audio *= envelope

        # Add some character-specific modulation
        char_mod = np.sin(2 * np.pi * len(text) * 0.1 * t) * 0.1
        audio *= (1 + char_mod)

        # Normalize
        audio = audio / np.max(np.abs(audio)) * 0.85

        return audio.astype(np.float32)

class EnhancedTTSManager:
    """Enhanced TTS Manager with multiple engines"""

    def __init__(self):
        self.engines = {}
        self.current_engine = None
        self._load_engines()

    def _load_engines(self):
        """Load all available TTS engines"""
        engine_classes = [
            GoogleTTSEngine,
            CoquiTTSEngine,
            KittenTTSEngine,
            OpenAITTSEngine,
            AzureTTSEngine,
        ]
        
        for engine_class in engine_classes:
            try:
                engine = engine_class()
                if engine.is_available():
                    # Generate clean engine ID
                    class_name = engine_class.__name__
                    if class_name.endswith('TTSEngine'):
                        engine_id = class_name[:-9].lower()  # Remove 'TTSEngine'
                    elif class_name.endswith('Engine'):
                        engine_id = class_name[:-6].lower()  # Remove 'Engine'
                    else:
                        engine_id = class_name.lower()

                    self.engines[engine_id] = engine
                    logger.info(f"Loaded TTS engine: {engine.get_name()} with ID: {engine_id}")
                else:
                    logger.debug(f"TTS engine not available: {engine_class.__name__}")
            except Exception as e:
                logger.error(f"Failed to load TTS engine {engine_class.__name__}: {e}")
        
        # Set default engine
        if 'google' in self.engines:
            self.current_engine = 'google'
        elif self.engines:
            self.current_engine = list(self.engines.keys())[0]

        logger.info(f"Final engines loaded: {list(self.engines.keys())}, current: {self.current_engine}")
    
    def get_available_engines(self) -> List[Dict]:
        """Get list of available engines"""
        return [
            {
                'id': engine_id,
                'name': engine.get_name(),
                'description': engine.get_description(),
                'current': engine_id == self.current_engine
            }
            for engine_id, engine in self.engines.items()
        ]
    
    def switch_engine(self, engine_id: str) -> bool:
        """Switch to a different engine"""
        if engine_id in self.engines:
            self.current_engine = engine_id
            logger.info(f"Switched to TTS engine: {self.engines[engine_id].get_name()}")
            return True
        return False
    
    def get_voices(self, engine_id: Optional[str] = None) -> List[Dict]:
        """Get voices for current or specified engine"""
        engine_id = engine_id or self.current_engine
        if engine_id and engine_id in self.engines:
            return self.engines[engine_id].get_voices()
        return []
    
    def synthesize(self, text: str, voice: str, engine_id: Optional[str] = None, **kwargs) -> np.ndarray:
        """Synthesize speech using current or specified engine"""
        engine_id = engine_id or self.current_engine
        if engine_id and engine_id in self.engines:
            return self.engines[engine_id].synthesize(text, voice, **kwargs)
        else:
            raise ValueError(f"Engine not available: {engine_id}")
    
    def get_current_engine(self) -> Optional[str]:
        """Get current engine ID"""
        return self.current_engine
    
    def get_engine_info(self, engine_id: Optional[str] = None) -> Optional[Dict]:
        """Get information about current or specified engine"""
        engine_id = engine_id or self.current_engine
        if engine_id and engine_id in self.engines:
            engine = self.engines[engine_id]
            return {
                'id': engine_id,
                'name': engine.get_name(),
                'description': engine.get_description(),
                'voices': len(engine.get_voices())
            }
        return None
